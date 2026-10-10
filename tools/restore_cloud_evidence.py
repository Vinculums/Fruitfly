#!/usr/bin/env python3
"""Restore byte-exact saved evidence from split gzip release assets.

This utility uses only the standard library. It never imports an experiment,
creates a scientific claim, or changes an existing different evidence file.
"""
import argparse
import gzip
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, build_opener

FORMAT = 'fruitfly-cloud-evidence-v1'
ALPHABET = str.maketrans('0123456789abcdef', 'abcdefghijklmnop')
CHUNK = 1024 * 1024


class EvidenceError(ValueError):
    """Invalid metadata or evidence; restoration must stop."""


def require(condition, message):
    if not condition:
        raise EvidenceError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result


def safe_relative(value, label):
    require(isinstance(value, str) and bool(value), label + ': expected a relative path')
    require('\\' not in value and ':' not in value and '\x00' not in value,
            label + ': unsafe path')
    parts = value.split('/')
    require(not value.startswith('/') and all(x not in ('', '.', '..') for x in parts),
            label + ': unsafe path')
    require(all(not x.endswith((' ', '.')) for x in parts), label + ': unsafe path')
    reserved = {'con', 'prn', 'aux', 'nul'}
    reserved.update('com' + str(i) for i in range(1, 10))
    reserved.update('lpt' + str(i) for i in range(1, 10))
    require(all(x.split('.')[0].lower() not in reserved for x in parts),
            label + ': reserved path')
    require(all(not any(ord(c) < 32 or c in '<>"|?*' for c in x) for x in parts),
            label + ': unsafe path')
    return PurePosixPath(value)


def https_url(value):
    require(isinstance(value, str), 'Asset URL must be text')
    try:
        parsed = urlsplit(value)
        valid = (parsed.scheme == 'https' and bool(parsed.hostname) and
                 parsed.username is None and parsed.password is None and not parsed.fragment)
        parsed.port  # Reject malformed ports.
    except ValueError as error:
        raise EvidenceError('Invalid asset URL') from error
    require(valid and not any(ord(c) < 33 for c in value),
            'Asset URL must be HTTPS without credentials or a fragment')
    return value


class HTTPSRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        https_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _metadata(record, keys, label):
    require(isinstance(record, dict) and set(record) == set(keys), label + ': invalid keys')


def _size_and_hash(record, label):
    require(type(record['bytes']) is int and record['bytes'] >= 0, label + ': invalid size')
    require(isinstance(record['sha256_alpha'], str) and
            re.fullmatch('[a-p]{64}', record['sha256_alpha']) is not None,
            label + ': invalid SHA256 alphabet')


def validate_manifest(manifest):
    _metadata(manifest, ('format', 'release_tag', 'repository', 'files'), 'Manifest')
    require(manifest['format'] == FORMAT, 'Unsupported manifest format')
    for field in ('release_tag', 'repository'):
        require(isinstance(manifest[field], str) and bool(manifest[field]),
                'Manifest: missing ' + field)
    require(isinstance(manifest['files'], list) and bool(manifest['files']),
            'Manifest must contain files')
    destinations, assets = set(), set()
    for record in manifest['files']:
        _metadata(record, ('path', 'bytes', 'sha256_alpha', 'parts'), 'File')
        safe_relative(record['path'], 'File path')
        key = record['path'].casefold()
        require(key not in destinations, 'Duplicate evidence destination')
        destinations.add(key)
        _size_and_hash(record, record['path'])
        require(isinstance(record['parts'], list) and bool(record['parts']), 'File has no parts')
        for part in record['parts']:
            _metadata(part, ('name', 'bytes', 'sha256_alpha', 'url'), 'Part')
            name = safe_relative(part['name'], 'Asset name')
            require(len(name.parts) == 1, 'Asset name must be a basename')
            require(part['name'].casefold() not in assets, 'Duplicate asset name')
            assets.add(part['name'].casefold())
            _size_and_hash(part, part['name'])
            require(part['bytes'] > 0, 'Asset part must not be empty')
            https_url(part['url'])
    require(not any('/'.join(path.split('/')[:i]) in destinations
                    for path in destinations for i in range(1, len(path.split('/')))),
            'Evidence destinations overlap')
    return manifest


def read_manifest(path):
    with Path(path).open('r', encoding='utf-8') as stream:
        value = json.load(stream, object_pairs_hook=unique_object,
                          parse_constant=lambda _: (_ for _ in ()).throw(EvidenceError('Nonfinite JSON')))
    return validate_manifest(value)


def digest_file(path):
    digest, count = hashlib.sha256(), 0
    with Path(path).open('rb') as stream:
        while data := stream.read(CHUNK):
            count += len(data)
            digest.update(data)
    return count, digest.hexdigest().translate(ALPHABET)


def verify_file(path, record):
    require(path.is_file() and not path.is_symlink(), 'Missing or unsafe file: ' + str(path))
    require(digest_file(path) == (record['bytes'], record['sha256_alpha']),
            'Evidence size/hash mismatch: ' + str(path))


def safe_destination(root, relative):
    safe_relative(relative, 'Destination')
    target = root.joinpath(*PurePosixPath(relative).parts)
    current = root
    require(not root.is_symlink(), 'Root must not be a symlink')
    for component in PurePosixPath(relative).parts:
        current = current / component
        require(not current.is_symlink(), 'Symlink in destination: ' + str(current))
    require(target.resolve().is_relative_to(root.resolve()), 'Destination leaves root')
    return target


def publish_exclusive(temporary, target, record):
    """Publish atomically without the overwrite behavior of POSIX rename."""
    try:
        os.link(temporary, target)
    except FileExistsError:
        verify_file(target, record)


def fetch_part(part, cache, opener=None):
    target = safe_destination(cache, part['name'])
    if target.exists():
        verify_file(target, part)
        return target
    cache.mkdir(parents=True, exist_ok=True)
    opener = opener or build_opener(HTTPSRedirect()).open
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(prefix='.download-', dir=cache, delete=False) as output:
            temporary = Path(output.name)
            with opener(part['url'], timeout=60) as response:
                https_url(response.geturl())
                count, digest = 0, hashlib.sha256()
                while data := response.read(CHUNK):
                    count += len(data)
                    require(count <= part['bytes'], 'Asset exceeds declared size: ' + part['name'])
                    digest.update(data)
                    output.write(data)
            require((count, digest.hexdigest().translate(ALPHABET)) ==
                    (part['bytes'], part['sha256_alpha']), 'Asset size/hash mismatch: ' + part['name'])
            output.flush()
            os.fsync(output.fileno())
        publish_exclusive(temporary, target, part)
        return target
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


class JoinedParts(io.RawIOBase):
    """Read ordered files as one byte stream, holding only one file open."""
    def __init__(self, paths):
        super().__init__()
        self.paths = iter(paths)
        self.stream = None

    def readable(self):
        return True

    def readinto(self, buffer):
        while True:
            if self.stream is None:
                path = next(self.paths, None)
                if path is None:
                    return 0
                self.stream = Path(path).open('rb')
            count = self.stream.readinto(buffer)
            if count:
                return count
            self.stream.close()
            self.stream = None

    def close(self):
        if self.stream is not None:
            self.stream.close()
            self.stream = None
        super().close()


def restore(manifest, root, cache, only=(), verify_only=False, opener=None):
    validate_manifest(manifest)
    root, cache = Path(root).absolute(), Path(cache).absolute()
    chosen = set(only)
    known = {entry['path'] for entry in manifest['files']}
    require(chosen <= known, 'Requested path is absent from manifest')
    selected = [entry for entry in manifest['files'] if not chosen or entry['path'] in chosen]
    # Fail before any download if existing destinations differ or are unsafe.
    targets = [(entry, safe_destination(root, entry['path'])) for entry in selected]
    verified = set()
    for entry, target in targets:
        if target.exists() or verify_only:
            verify_file(target, entry)
            verified.add(entry['path'])
    receipts = []
    for entry, target in targets:
        if entry['path'] in verified:
            receipts.append({'path': entry['path'], 'status': 'verified'})
            continue
        if target.exists():
            verify_file(target, entry)
            receipts.append({'path': entry['path'], 'status': 'verified'})
            continue
        parts = [fetch_part(part, cache, opener) for part in entry['parts']]
        target.parent.mkdir(parents=True, exist_ok=True)
        safe_destination(root, entry['path'])
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(prefix='.restore-', dir=target.parent, delete=False) as output:
                temporary = Path(output.name)
                with JoinedParts(parts) as joined, io.BufferedReader(joined) as buffered:
                    with gzip.GzipFile(fileobj=buffered, mode='rb') as compressed:
                        count, digest = 0, hashlib.sha256()
                        while data := compressed.read(CHUNK):
                            count += len(data)
                            require(count <= entry['bytes'], 'Evidence exceeds declared size: ' + entry['path'])
                            digest.update(data)
                            output.write(data)
                require((count, digest.hexdigest().translate(ALPHABET)) ==
                        (entry['bytes'], entry['sha256_alpha']),
                        'Restored evidence size/hash mismatch: ' + entry['path'])
                output.flush()
                os.fsync(output.fileno())
            safe_destination(root, entry['path'])
            publish_exclusive(temporary, target, entry)
            receipts.append({'path': entry['path'], 'status': 'restored'})
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    return receipts


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', default='config/cloud-evidence-manifest.json')
    parser.add_argument('--root', default='.')
    parser.add_argument('--cache-dir', default='.git/cloud-evidence-cache',
                        help='Download cache (default: .git/cloud-evidence-cache)')
    parser.add_argument('--only', action='append', default=[], metavar='RELATIVE_PATH')
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args(argv)
    try:
        receipts = restore(read_manifest(args.manifest), args.root, args.cache_dir,
                           args.only, args.verify_only)
    except (EvidenceError, OSError, EOFError) as error:
        print('Evidence restoration failed: ' + str(error), file=sys.stderr)
        return 1
    print(json.dumps({'format': FORMAT, 'complete': True, 'files': receipts}, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
