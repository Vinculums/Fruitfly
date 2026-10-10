#!/usr/bin/env python3
"""Check frozen source and archival bytes without scientific imports or execution."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

PIN_PATHS = (
    "config/h17-run3-specification-pins.json",
    "config/h17-run3-execution-pins.json",
    "config/h17-run3-dev-pins.json",
)
MANIFEST_PATH = "config/cloud-evidence-manifest.json"
AP = str.maketrans("0123456789abcdef", "abcdefghijklmnop")
LARGE_BYTES = 45 * 1024 * 1024


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest().translate(AP)


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)


def relative_path(root: Path, value: str) -> Path:
    if not isinstance(value, str) or not value or "\\" in value:
        raise ValueError("invalid relative path")
    part = PurePosixPath(value)
    if part.is_absolute() or ".." in part.parts or ":" in value:
        raise ValueError("path outside checkout")
    path = (root / value).resolve()
    if not path.is_relative_to(root):
        raise ValueError("path outside checkout")
    return path


def valid_hash(value) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[a-p]{64}", value) is not None


def inspect(root: Path, sources_only: bool) -> dict:
    root = root.resolve()
    errors = []
    deferred = []
    checked = []
    sources = {}
    map_counts = {}
    evidence = {}
    try:
        manifest = read_json(root / MANIFEST_PATH)
        items = manifest["files"]
        if isinstance(items, dict):
            items = [dict(value, path=path) for path, value in items.items()]
        if not isinstance(items, list) or not items:
            raise ValueError("nonempty files list required")
        for entry in items:
            path = entry["path"]
            relative_path(root, path)
            if path in evidence:
                raise ValueError("duplicate evidence path")
            if not valid_hash(entry.get("sha256_alpha")):
                raise ValueError("invalid evidence digest")
            size = entry.get("bytes")
            if type(size) is not int or size < 0:
                raise ValueError("invalid evidence byte count")
            evidence[path] = entry
    except (OSError, ValueError, KeyError, TypeError):
        errors.append({"path": MANIFEST_PATH, "reason": "missing or malformed evidence manifest"})

    for pin_path in PIN_PATHS:
        try:
            pins = read_json(root / pin_path)["files_sha256_alpha"]
            if not isinstance(pins, dict) or not pins:
                raise ValueError("nonempty source map required")
            map_counts[pin_path] = len(pins)
            for path, expected in pins.items():
                relative_path(root, path)
                if not valid_hash(expected):
                    raise ValueError("invalid source digest")
                if path in sources and sources[path] != expected:
                    raise ValueError("source map conflict")
                sources[path] = expected
        except (OSError, ValueError, KeyError, TypeError):
            errors.append({"path": pin_path, "reason": "missing or malformed frozen source map"})

    targets = dict(sources)
    for path, entry in evidence.items():
        expected = entry["sha256_alpha"]
        if path in targets and targets[path] != expected:
            errors.append({"path": path, "reason": "source/evidence digest conflict"})
        else:
            targets[path] = expected
    for path, expected in sorted(targets.items()):
        file_path = relative_path(root, path)
        entry = evidence.get(path)
        # Defer even a present large file in this mode: source preparation must
        # never be mistaken for a completed archival integrity check.
        if (sources_only and entry and entry.get("defer_allowed") is True
                and entry["bytes"] > LARGE_BYTES):
            deferred.append({"path": path, "bytes": entry["bytes"],
                             "reason": "large archival bytes not checked in sources-only mode"})
            continue
        try:
            if entry and file_path.stat().st_size != entry["bytes"]:
                errors.append({"path": path, "reason": "evidence byte count mismatch"})
                continue
            actual = digest(file_path)
        except OSError:
            errors.append({"path": path, "reason": "missing or unreadable file"})
            continue
        if actual != expected:
            errors.append({"path": path, "reason": "frozen byte digest mismatch"})
            continue
        checked.append(path)
    return {
        "format": "fruitfly-cloud-readiness-v1",
        "mode": "sources-only" if sources_only else "full",
        "plan_ready": not errors,
        "execution_ready": False,
        "scientific_acceptance_checked": False,
        "archival_bytes_complete": not errors and not deferred,
        "execution_blockers": ["frozen Windows runtime requires separate comparability decision",
                               "EVAL remains unopened behind separate owner gate",
                               "scientific execution on hosted runners is not authorized"],
        "source_map_counts": map_counts,
        "unique_source_files": len(sources),
        "checked_files": checked,
        "deferred_files": deferred,
        "errors": errors,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--sources-only", action="store_true")
    modes.add_argument("--full", action="store_true")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", help="new receipt path under notes/handoffs; never overwrite")
    args = parser.parse_args(argv)
    result = inspect(args.root, args.sources_only)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        try:
            output = relative_path(args.root.resolve(), args.output)
            if not output.is_relative_to((args.root / "notes/handoffs").resolve()):
                raise ValueError("receipt must be under notes/handoffs")
            with output.open("x", encoding="utf-8", newline="\n") as handle:
                handle.write(payload)
        except (OSError, ValueError):
            parser.error("receipt path is unavailable, outside notes/handoffs, or already exists")
    print(payload, end="")
    return 0 if result["plan_ready"] else 1


if __name__ == "__main__":
    sys.exit(main())
