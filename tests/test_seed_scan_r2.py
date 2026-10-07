"""Scratch-only contract tests; real seed values come from trusted source constants."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import verify_seed_scan_r2 as r2


class R2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        r2.verify_sources(r2.ROOT)
        sys.path.insert(0, str(r2.ROOT / 'src'))
        import ph33, ph35
        cls.originals = {'ph33': ph33, 'ph35': ph35}
        cls.entries = r2.load_manifest(r2.ROOT)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'src').mkdir()
        self.checkers = {}
        for name in self.originals:
            target = self.root / 'src' / (name + '.py')
            shutil.copyfile(r2.ROOT / 'src' / target.name, target)
            spec = importlib.util.spec_from_file_location('scratch_' + name, target)
            checker = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(checker)
            self.checkers[name] = checker
        # Source copies are excluded only when named for their respective checker.
        # Their bytes contain no hits for the other checker, as in the real tree.

    def write(self, path, data):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    def fixture(self, name, path='fixture.bin', alias='dev_w', data=None, optional=False):
        number = r2.aliases_for(self.checkers[name])[alias]
        data = str(number).encode() + b'\n' if data is None else data
        self.write(path, data)
        row = dict(checker=name, path=path, alias=alias, occurrences=r2.count_number(data, number),
                   file_sha256_ap=r2.digest_ap(data), reason='incidental_match',
                   presence='owner_local_optional' if optional else 'required')
        return row, data

    def scan(self, name, rows):
        return r2.scan_checker(self.root, name, self.checkers[name], rows)

    def test_cloud_and_exact_owner_entries(self):
        owner = subprocess.check_output(['git', 'show',
            'ee415d09a5bac4f100077f371f647b2f1878550f:notes/recommendations/2026-10-07-r2-step3-owner-entries.json'], cwd=r2.ROOT)
        self.assertEqual(self.entries, json.loads(owner))
        self.assertEqual(len({e['path'] for e in self.entries}), 12)
        for name, pairs, occurrences in [('ph33', 25, 29), ('ph35', 17, 17)]:
            rows = [e for e in self.entries if e['checker'] == name]
            self.assertEqual(len(rows), pairs)
            self.assertEqual(sum(e['occurrences'] for e in rows), occurrences)
            result = r2.scan_checker(r2.ROOT, name, self.originals[name], self.entries)
            self.assertFalse(result['errors'])

    def test_positive_binary_and_boundaries(self):
        for name in self.checkers:
            with self.subTest(checker=name):
                n = str(r2.aliases_for(self.checkers[name])['dev_w']).encode()
                data = b'\x00' + n + b' x' + n + b'! 8' + n + b' ' + n + b'8 \xff'
                row, _ = self.fixture(name, data=data)
                self.assertEqual(row['occurrences'], 2)
                result = self.scan(name, [row])
                self.assertFalse(result['errors'])
                self.assertEqual(result['applied_rows'], 1)

    def test_unregistered_and_file_and_checker_scope(self):
        for name in self.checkers:
            row, data = self.fixture(name)
            self.assertTrue(self.scan(name, [])['errors'])
            wrong = {**row, 'checker': 'ph35' if name == 'ph33' else 'ph33'}
            self.assertTrue(self.scan(name, [wrong])['errors'])
            self.write('elsewhere.bin', data)
            self.assertTrue(self.scan(name, [row])['errors'])
            (self.root / 'elsewhere.bin').unlink()

    def test_count_digest_drift_and_other_seed(self):
        for name in self.checkers:
            row, data = self.fixture(name)
            other = str(r2.aliases_for(self.checkers[name])['eval_w']).encode()
            for changed in (data + data, data + b'edit', b'none\n', data.replace(b'\n', b'\r\n'), data + other):
                with self.subTest(checker=name, mutation=r2.digest_ap(changed)):
                    self.write(row['path'], changed)
                    self.assertTrue(self.scan(name, [row])['errors'])
            # Isolate count drift even when scratch bytes have a matching digest.
            self.write(row['path'], data + data)
            self.assertTrue(self.scan(name, [{**row, 'file_sha256_ap': r2.digest_ap(data + data)}])['errors'])
            self.write(row['path'], data + other)
            updated = {**row, 'file_sha256_ap': r2.digest_ap(data + other)}
            self.assertTrue(self.scan(name, [updated])['errors'])
            # A matching digest cannot hide a different alias or checker resolution.
            wrong = {**row, 'alias': 'eval_w'}
            self.write(row['path'], data)
            self.assertTrue(self.scan(name, [wrong])['errors'])
            other_checker = self.checkers['ph35' if name == 'ph33' else 'ph33']
            wrong_data = str(r2.aliases_for(other_checker)['dev_w']).encode()
            self.write(row['path'], wrong_data)
            self.assertTrue(self.scan(name, [{**row, 'file_sha256_ap': r2.digest_ap(wrong_data)}])['errors'])

    def test_missing_required_and_optional_lifecycle(self):
        for name in self.checkers:
            path = sorted(r2.OPTIONAL_PATHS)[0]
            row, data = self.fixture(name, path=path, optional=True)
            self.assertFalse(self.scan(name, [row])['errors'])
            (self.root / path).unlink()
            result = self.scan(name, [row])
            self.assertFalse(result['errors'])
            self.assertEqual(result['applied_rows'], 0)
            self.assertEqual(result['unused'][0]['status'], 'absent/unused')
            self.assertTrue(self.scan(name, [{**row, 'presence': 'required'}])['errors'])
            self.write(path, b'different')
            self.assertTrue(self.scan(name, [row])['errors'])
            (self.root / path).unlink()

    def test_existing_pair_and_return_contract(self):
        for name, checker in self.checkers.items():
            path = 'experiments/h20/ph31_eval.txt'
            number = checker.ph30.SEEDS['eval'][0][1]
            self.write(path, b' '.join([str(number).encode()] * 2))
            hits, nums, nf = checker.seeds_unused()
            self.assertIsInstance(hits, list)
            self.assertEqual(nums, checker.seed_numbers())
            self.assertIsInstance(nf, int)
            self.assertFalse(hits)
            other = r2.aliases_for(checker)['dev_w']
            self.write(path, str(number).encode() + b' ' + str(other).encode())
            hits, _, _ = checker.seeds_unused()
            self.assertTrue(hits)
            self.assertIsInstance(hits[0], tuple if name == 'ph33' else str)
            self.assertTrue(self.scan(name, [])['errors'])
            (self.root / path).unlink()

    def manifest(self, raw, matching=True):
        self.write(r2.MANIFEST, raw)
        # Only scratch parsing tests replace the module constant; the CLI has no override.
        if matching:
            with patch.object(r2, 'MANIFEST_PIN', r2.digest_ap(raw)):
                return r2.load_manifest(self.root)
        return r2.load_manifest(self.root)

    def test_manifest_schema_negative_cases(self):
        document = json.loads((r2.ROOT / r2.MANIFEST).read_bytes())
        mutations = []
        for field, value in [('checker', 'unknown'), ('alias', 'unknown'), ('occurrences', True),
                             ('occurrences', 'one'), ('occurrences', 1.0), ('occurrences', 0),
                             ('file_sha256_ap', ''), ('file_sha256_ap', 'z' * 64),
                             ('reason', 'unknown'), ('presence', 'owner_local_optional'),
                             ('path', '../escape'), ('path', '/absolute'), ('path', 'glob/*'),
                             ('path', 'dir//file')]:
            mutated = copy.deepcopy(document)
            mutated['entries'][0][field] = value
            mutations.append(mutated)
        for field, value in [('schema', 'wrong'), ('decision', 'wrong'), ('extra', True), ('entries', []), ('entries', {})]:
            mutated = copy.deepcopy(document); mutated[field] = value; mutations.append(mutated)
        mutated = copy.deepcopy(document); mutated['entries'].append(mutated['entries'][0]); mutations.append(mutated)
        mutated = copy.deepcopy(document); mutated['entries'].reverse(); mutations.append(mutated)
        mutated = copy.deepcopy(document); mutated['entries'][0]['extra'] = 'x'; mutations.append(mutated)
        for mutated in mutations:
            with self.assertRaises(r2.VerificationError):
                self.manifest((json.dumps(mutated) + '\n').encode())
        for raw in (b'{"schema":"r2-v1","schema":"r2-v1"}\n', b'{}\r\n', b'{}', b'{}\n\n', b'\xef\xbb\xbf{}\n'):
            with self.assertRaises(r2.VerificationError):
                self.manifest(raw)
        with self.assertRaises(r2.VerificationError):
            self.manifest(b'{}\n', matching=False)
        (self.root / r2.MANIFEST).unlink()
        with self.assertRaises(FileNotFoundError):
            r2.load_manifest(self.root)

    def test_manifest_is_scanned_even_with_scratch_pin(self):
        document = json.loads((r2.ROOT / r2.MANIFEST).read_bytes())
        for name in self.checkers:
            mutated = copy.deepcopy(document)
            number = r2.aliases_for(self.checkers[name])['dev_w']
            # A valid path containing a real seed introduces a manifest-text collision.
            mutated['entries'][0]['path'] = 'collision/' + str(number) + '.bin'
            mutated['entries'].sort(key=lambda r: (r['checker'], r['path'], r['alias']))
            raw = (json.dumps(mutated) + '\n').encode()
            self.manifest(raw)
            result = self.scan(name, [])
            self.assertIn('uncovered hit in ' + r2.MANIFEST, result['errors'])

    def test_source_and_downstream_tamper_guards(self):
        for source in r2.SOURCE_PINS:
            shutil.copyfile(r2.ROOT / 'src' / (source + '.py'), self.root / 'src' / (source + '.py'))
        r2.verify_sources(self.root)
        for name in ('ph32', 'ph33', 'ph35', 'ph36b', 'ph38'):
            path = self.root / 'src' / (name + '.py')
            original = path.read_bytes()
            path.write_bytes(original + b'\n')
            with self.assertRaises(r2.VerificationError):
                r2.verify_sources(self.root)
            path.write_bytes(original)
        # Test the recorded full and prefix guards independently of the outer pins.
        for name, variable in [('ph33', 'PH32_SHA'), ('ph36b', 'SHA_ON_RECORD'), ('ph38', 'REGISTERED')]:
            path = self.root / 'src' / (name + '.py')
            original = path.read_bytes()
            value = r2.recorded_value(self.root, name, variable)
            old = value if isinstance(value, str) else value['ph35']
            path.write_bytes(original.replace(old.encode(), b'a' * len(old)))
            with patch.dict(r2.SOURCE_PINS, {name: r2.digest_ap(path.read_bytes())}):
                with self.assertRaises(r2.VerificationError):
                    r2.verify_sources(self.root)
            path.write_bytes(original)

    def test_optimized_cli_rejected(self):
        for flag in ('-O', '-OO'):
            result = subprocess.run([sys.executable, flag, str(r2.ROOT / 'tools/verify_seed_scan_r2.py')], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(b'assertions must be enabled', result.stderr)

    def test_pfive_new_files(self):
        paths = [r2.MANIFEST, 'tools/verify_seed_scan_r2.py', 'tests/test_seed_scan_r2.py']
        paths += [str(p.relative_to(r2.ROOT)) for p in (r2.ROOT / 'notes/recommendations').glob('*r2-step3-cloud*')]
        for path in paths:
            data = (r2.ROOT / path).read_bytes()
            for name, checker in self.originals.items():
                self.assertFalse(any(r2.count_number(data, n) for n in checker.seed_numbers()), (path, name))


if __name__ == '__main__':
    unittest.main()
