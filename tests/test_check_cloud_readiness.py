"""Synthetic archival fixtures only: no scientific imports or reserved claims."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location(
    "cloud_readiness", Path(__file__).resolve().parents[1] / "tools/check_cloud_readiness.py")
cloud = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cloud)


class CloudReadinessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.sources = []
        for index, pin_path in enumerate(cloud.PIN_PATHS):
            path = "src/source_" + chr(ord("a") + index) + ".py"
            value = self.write(path, b"fixture source\n" + chr(ord("a") + index).encode())
            self.write_json(pin_path, {"files_sha256_alpha": {path: value}})
            self.sources.append(path)
        path = "experiments/fixture/receipt.json"
        value = self.write(path, b"{}\n")
        self.entries = [{"path": path, "bytes": 3, "sha256_alpha": value}]
        self.manifest()

    def write(self, path, value):
        destination = self.root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(value)
        return hashlib.sha256(value).hexdigest().translate(cloud.AP)

    def write_json(self, path, value):
        self.write(path, json.dumps(value).encode())

    def manifest(self):
        self.write_json(cloud.MANIFEST_PATH, {"files": self.entries})

    def test_all_three_maps_are_checked_and_execution_stays_closed(self):
        result = cloud.inspect(self.root, True)
        self.assertTrue(result["plan_ready"])
        self.assertEqual(set(result["source_map_counts"]), set(cloud.PIN_PATHS))
        self.assertEqual(result["unique_source_files"], len(self.sources))
        self.assertFalse(result["execution_ready"])
        self.assertFalse(result["scientific_acceptance_checked"])

    def test_missing_small_source_fails_even_sources_only(self):
        (self.root / self.sources[-1]).unlink()
        result = cloud.inspect(self.root, True)
        self.assertFalse(result["plan_ready"])
        self.assertEqual(result["errors"][0]["path"], self.sources[-1])

    def test_source_drift_fails_full_and_sources_only(self):
        self.write(self.sources[0], b"different bytes")
        for sources_only in (False, True):
            result = cloud.inspect(self.root, sources_only)
            self.assertFalse(result["plan_ready"])
            self.assertIn("frozen byte digest mismatch", str(result["errors"]))

    def test_large_deferral_is_explicit_and_full_requires_bytes(self):
        path = "experiments/fixture/raw.npz.ap"
        self.entries.append({"path": path, "bytes": cloud.LARGE_BYTES + 1,
                             "sha256_alpha": "a" * 64, "defer_allowed": True})
        self.manifest()
        result = cloud.inspect(self.root, True)
        self.assertTrue(result["plan_ready"])
        self.assertFalse(result["archival_bytes_complete"])
        self.assertEqual(result["deferred_files"][0]["path"], path)
        self.assertFalse(cloud.inspect(self.root, False)["plan_ready"])

    def test_large_without_explicit_permission_is_not_deferred(self):
        self.entries.append({"path": "experiments/fixture/absent.ap",
                             "bytes": cloud.LARGE_BYTES + 1, "sha256_alpha": "a" * 64})
        self.manifest()
        result = cloud.inspect(self.root, True)
        self.assertFalse(result["plan_ready"])
        self.assertEqual(result["deferred_files"], [])

    def test_small_evidence_cannot_be_deferred(self):
        self.entries[0]["defer_allowed"] = True
        self.manifest()
        (self.root / self.entries[0]["path"]).unlink()
        self.assertFalse(cloud.inspect(self.root, True)["plan_ready"])

    def test_missing_pin_or_manifest_is_explicit_failure(self):
        (self.root / cloud.PIN_PATHS[1]).unlink()
        (self.root / cloud.MANIFEST_PATH).unlink()
        result = cloud.inspect(self.root, True)
        self.assertFalse(result["plan_ready"])
        self.assertEqual(len(result["errors"]), 2)

    def test_manifest_hash_conflict_with_source_fails(self):
        path = self.sources[0]
        self.entries.append({"path": path, "bytes": (self.root / path).stat().st_size,
                             "sha256_alpha": "a" * 64})
        self.manifest()
        result = cloud.inspect(self.root, True)
        self.assertFalse(result["plan_ready"])
        self.assertIn("source/evidence digest conflict", str(result["errors"]))

    def test_manifest_duplicate_and_traversal_rejected(self):
        for entry in (dict(self.entries[0]),
                      {"path": "../outside", "bytes": 0, "sha256_alpha": "a" * 64}):
            self.entries.append(entry)
            self.manifest()
            self.assertFalse(cloud.inspect(self.root, True)["plan_ready"])
            self.entries.pop()

    def test_cli_outputs_json_and_protects_existing_receipt(self):
        (self.root / "notes/handoffs").mkdir(parents=True)
        argv = ["--sources-only", "--root", str(self.root),
                "--output", "notes/handoffs/fixture.json"]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(cloud.main(argv), 0)
        self.assertTrue(json.loads(output.getvalue())["plan_ready"])
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            cloud.main(argv)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            cloud.main(["--full", "--root", str(self.root), "--output", self.sources[0]])


if __name__ == "__main__":
    unittest.main()
