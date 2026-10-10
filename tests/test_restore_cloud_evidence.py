"""Pure byte restoration fixtures; no scientific modules or claims."""
import copy
import gzip
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import restore_cloud_evidence as R


def alpha(data):
    return hashlib.sha256(data).hexdigest().translate(R.ALPHABET)


class Response(io.BytesIO):
    def __init__(self, data, url):
        super().__init__(data)
        self.url = url

    def geturl(self):
        return self.url


class RestoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root, self.cache = self.base / 'root', self.base / 'cache'
        self.data = (b'Exact saved bytes\x00\xff' * 127) + b'final'
        packed = gzip.compress(self.data, compresslevel=1, mtime=0)
        pieces = [packed[:3], packed[3:19], packed[19:]]
        self.payloads = {}
        parts = []
        for i, piece in enumerate(pieces):
            url = 'https://github.com/example/evidence/releases/download/fixture/part-' + str(i)
            self.payloads[url] = piece
            parts.append(dict(name='part-' + str(i), bytes=len(piece), sha256_alpha=alpha(piece), url=url))
        self.manifest = dict(format=R.FORMAT, release_tag='fixture', repository='example/evidence',
                             files=[dict(path='evidence/saved.bin', bytes=len(self.data),
                                         sha256_alpha=alpha(self.data), parts=parts)])
        self.calls = []

    def opener(self, url, timeout):
        self.calls.append(url)
        self.assertEqual(timeout, 60)
        return Response(self.payloads[url], url)

    def run_restore(self, **kwargs):
        return R.restore(self.manifest, self.root, self.cache, opener=self.opener, **kwargs)

    def test_split_gzip_restores_exact_bytes_and_skips_existing(self):
        result = self.run_restore()
        self.assertEqual(result[0]['status'], 'restored')
        self.assertEqual((self.root / 'evidence/saved.bin').read_bytes(), self.data)
        self.assertEqual(len(self.calls), 3)
        self.assertEqual(self.run_restore()[0]['status'], 'verified')
        self.assertEqual(len(self.calls), 3)
        self.assertEqual(list(self.root.rglob('.restore-*')), [])

    def test_verified_cache_is_reused(self):
        self.run_restore()
        (self.root / 'evidence/saved.bin').unlink()
        self.run_restore()
        self.assertEqual(len(self.calls), 3)

    def test_corrupt_cached_part_fails_without_overwriting_it(self):
        self.cache.mkdir()
        target = self.cache / 'part-0'
        target.write_bytes(b'changed')
        with self.assertRaises(R.EvidenceError):
            self.run_restore()
        self.assertEqual(target.read_bytes(), b'changed')
        self.assertEqual(self.calls, [])

    def test_verify_only_hashes_each_existing_file_once(self):
        self.run_restore()
        with patch.object(R, 'digest_file', wraps=R.digest_file) as digest:
            self.run_restore(verify_only=True)
        self.assertEqual(digest.call_count, 1)

    def test_truncated_download_is_rejected(self):
        first = self.manifest['files'][0]['parts'][0]
        self.payloads[first['url']] = self.payloads[first['url']][:-1]
        with self.assertRaises(R.EvidenceError):
            self.run_restore()
        self.assertFalse((self.root / 'evidence/saved.bin').exists())

    def test_symlink_destination_is_rejected_without_download(self):
        self.root.mkdir()
        outside = self.base / 'outside'
        outside.mkdir()
        try:
            (self.root / 'evidence').symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest('Host cannot create a symlink')
        with self.assertRaises(R.EvidenceError):
            self.run_restore()
        self.assertEqual(self.calls, [])
        self.assertEqual(list(outside.iterdir()), [])

    def test_verify_only_never_downloads(self):
        with self.assertRaises(R.EvidenceError):
            self.run_restore(verify_only=True)
        self.assertEqual(self.calls, [])
        self.assertFalse(self.cache.exists())
        self.run_restore()
        self.calls.clear()
        self.assertEqual(self.run_restore(verify_only=True)[0]['status'], 'verified')
        self.assertEqual(self.calls, [])

    def test_existing_mismatch_is_preserved_before_download(self):
        target = self.root / 'evidence/saved.bin'
        target.parent.mkdir(parents=True)
        target.write_bytes(b'original different bytes')
        with self.assertRaises(R.EvidenceError):
            self.run_restore()
        self.assertEqual(target.read_bytes(), b'original different bytes')
        self.assertEqual(self.calls, [])

    def test_path_traversal_and_platform_aliases_rejected(self):
        for path in ('../escape', '/absolute', 'C:/absolute', 'a\\escape',
                     'a/../escape', 'a//escape', 'a/./escape', 'CON.bin', 'a./file', 'a/file '):
            with self.subTest(path=path):
                manifest = copy.deepcopy(self.manifest)
                manifest['files'][0]['path'] = path
                with self.assertRaises(R.EvidenceError):
                    R.validate_manifest(manifest)

    def test_duplicate_and_nested_destinations_rejected(self):
        for path in ('EVIDENCE/SAVED.BIN', 'evidence/saved.bin/child'):
            manifest = copy.deepcopy(self.manifest)
            extra = copy.deepcopy(manifest['files'][0])
            extra['path'] = path
            for part in extra['parts']:
                part['name'] += '-other'
            manifest['files'].append(extra)
            with self.assertRaises(R.EvidenceError):
                R.validate_manifest(manifest)

    def test_invalid_schema_hash_size_and_asset_names(self):
        variants = []
        value = copy.deepcopy(self.manifest); value['format'] = 'other'; variants.append(value)
        value = copy.deepcopy(self.manifest); value['files'][0]['bytes'] = True; variants.append(value)
        value = copy.deepcopy(self.manifest); value['files'][0]['sha256_alpha'] = 'z' * 64; variants.append(value)
        value = copy.deepcopy(self.manifest); value['files'][0]['parts'][1]['name'] = 'part-0'; variants.append(value)
        value = copy.deepcopy(self.manifest); value['files'][0]['parts'][0]['name'] = '../part'; variants.append(value)
        value = copy.deepcopy(self.manifest); value['files'][0]['parts'] = []; variants.append(value)
        value = copy.deepcopy(self.manifest); value['extra'] = True; variants.append(value)
        for value in variants:
            with self.assertRaises(R.EvidenceError):
                R.validate_manifest(value)

    def test_non_https_credentials_and_redirect_rejected(self):
        for url in ('http://github.com/part', 'https://name:secret@github.com/part',
                    'https://github.com/part#fragment', 'https://github.com:bad/part'):
            with self.assertRaises(R.EvidenceError):
                R.https_url(url)
        with self.assertRaises(R.EvidenceError):
            R.HTTPSRedirect().redirect_request(None, None, 302, '', {}, 'http://example.com/part')

    def test_bad_download_hash_and_size_leave_no_final_evidence(self):
        for mode in ('hash', 'size'):
            with self.subTest(mode=mode):
                manifest = copy.deepcopy(self.manifest)
                part = manifest['files'][0]['parts'][0]
                if mode == 'hash':
                    part['sha256_alpha'] = 'a' * 64
                else:
                    part['bytes'] -= 1
                with self.assertRaises(R.EvidenceError):
                    R.restore(manifest, self.root, self.cache, opener=self.opener)
                self.assertFalse((self.root / 'evidence/saved.bin').exists())
                self.assertEqual(list(self.cache.glob('.download-*')), [])

    def test_bad_original_hash_size_or_gzip_leave_no_final_evidence(self):
        for mode in ('hash', 'size', 'gzip'):
            with self.subTest(mode=mode):
                manifest = copy.deepcopy(self.manifest)
                if mode == 'hash':
                    manifest['files'][0]['sha256_alpha'] = 'a' * 64
                elif mode == 'size':
                    manifest['files'][0]['bytes'] -= 1
                else:
                    bad = b'not gzip'
                    url = 'https://github.com/bad'
                    self.payloads[url] = bad
                    manifest['files'][0]['parts'] = [dict(name='bad', bytes=len(bad), sha256_alpha=alpha(bad), url=url)]
                with self.assertRaises((R.EvidenceError, OSError)):
                    R.restore(manifest, self.root, self.cache, opener=self.opener)
                self.assertFalse((self.root / 'evidence/saved.bin').exists())
                self.assertEqual(list(self.root.rglob('.restore-*')), [])

    def test_only_requires_exact_known_path(self):
        with self.assertRaises(R.EvidenceError):
            self.run_restore(only=['not/in/manifest'])
        self.assertEqual(self.calls, [])
        self.assertEqual(self.run_restore(only=['evidence/saved.bin'])[0]['status'], 'restored')

    def test_duplicate_json_key_rejected(self):
        path = self.base / 'manifest.json'
        path.write_text('{"format":"x","format":"y"}', encoding='utf-8')
        with self.assertRaises(R.EvidenceError):
            R.read_manifest(path)

    def test_publish_race_preserves_other_file(self):
        target = self.base / 'target'
        temporary = self.base / 'temporary'
        target.write_bytes(b'other writer')
        temporary.write_bytes(self.data)
        with self.assertRaises(R.EvidenceError):
            R.publish_exclusive(temporary, target, self.manifest['files'][0])
        self.assertEqual(target.read_bytes(), b'other writer')

    def test_cli_reports_failure_and_success(self):
        path = self.base / 'manifest.json'
        path.write_text(json.dumps(self.manifest), encoding='utf-8')
        with patch('sys.stderr', new=io.StringIO()):
            self.assertEqual(R.main(['--manifest', str(path), '--root', str(self.root), '--verify-only']), 1)
        self.run_restore()
        with patch('sys.stdout', new=io.StringIO()) as output:
            self.assertEqual(R.main(['--manifest', str(path), '--root', str(self.root), '--verify-only']), 0)
        self.assertTrue(json.loads(output.getvalue())['complete'])


if __name__ == '__main__':
    unittest.main()
