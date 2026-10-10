"""DEV authority and saved-result boundaries; no generators or simulation."""
import copy
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import recompute_h17_run3_dev as D
R = D.R


class DevRootTests(unittest.TestCase):
    def put(self, path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(R.canonical(value) + b'\n')

    def fixture(self, root):
        self.root = root
        for name in D.FILES:
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b'reviewed stage fixture')
        (root / 'base.txt').write_bytes(b'unchanged base')
        main = dict(runtime={}, schema_sha256_alpha='a' * 64,
            keysets_sha256_alpha='b' * 64, specification_pins_sha256_alpha='c' * 64,
            files_sha256_alpha={'base.txt': D.file_digest(root / 'base.txt')})
        main['source_closure_sha256_alpha'] = R.digest(R.canonical(main))
        self.put(root / D.MAIN, main)
        prior = root / 'experiments/h17/run3/bench'
        prior.mkdir(parents=True)
        (prior / 'raw.npz.ap').write_bytes(b'saved raw fixture')
        raw = D.file_digest(prior / 'raw.npz.ap')
        gates = {str(i): dict(complete=True, passed=True, rows=400, steps=600) for i in range(20)}
        clauses = {str(i): dict(status='PASS') for i in range(9)}
        common = dict(complete=True, passed=True, stage='bench', smoke=False,
                      rows=400, steps=600, verdict='PASS', clauses=clauses, gates=gates)
        self.put(prior / 'identity.json', dict(common, raw_arrays={'sha256_alpha': raw}))
        self.put(prior / 'metrics.json', common)
        self.put(prior / 'verification.json', dict(common, raw_sha256_alpha=raw))
        self.put(prior / 'parent_recomputation.json', dict(common, raw_sha256_alpha=raw,
            source_closure_sha256_alpha=main['source_closure_sha256_alpha'], rng_created=False,
            draws=0, verification_sha256_alpha=D.file_digest(prior / 'verification.json')))
        self.pins = dict(complete=True, stage='dev', decision='decision:h17-run3-dev-open',
            MAIN_pins_sha256_alpha=D.file_digest(root / D.MAIN),
            source_closure_sha256_alpha=main['source_closure_sha256_alpha'],
            files_sha256_alpha={name: D.file_digest(root / name) for name in D.FILES})
        self.gate = dict(complete=True, opened=True, stage='dev', decision=self.pins['decision'],
            owner_instruction='approved DEV operation', source_closure_sha256_alpha=main['source_closure_sha256_alpha'])
        self.rebind()

    def rebind(self):
        root = self.root
        prior = root / 'experiments/h17/run3/bench'
        self.pins['prior_artifacts_sha256_alpha'] = {
            name + '_sha256_alpha': D.file_digest(prior / (name + ('.npz.ap' if name == 'raw' else '.json')))
            for name in ('identity', 'metrics', 'raw', 'verification', 'parent_recomputation')}
        self.pins['stage_closure_sha256_alpha'] = R.digest(R.canonical({k: self.pins[k]
            for k in ('MAIN_pins_sha256_alpha', 'source_closure_sha256_alpha', 'files_sha256_alpha')}))
        self.put(root / D.PINS, self.pins)
        self.gate.update(stage_pins_sha256_alpha=D.file_digest(root / D.PINS),
            prior_verification_sha256_alpha=self.pins['prior_artifacts_sha256_alpha']['verification_sha256_alpha'])
        self.put(root / D.GATE, self.gate)

    def test_authorized_saved_bench_binds_exact_stage_files(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name).resolve()
            self.fixture(root)
            binding = D.stage_bindings(root)
            self.assertEqual(binding['stage'], 'dev')
            self.assertEqual(binding['stage_pins_sha256_alpha'], D.file_digest(root / D.PINS))
            self.assertEqual(binding['opening_sha256_alpha'], D.file_digest(root / D.GATE))

    def test_closed_or_unsigned_gate_rejected(self):
        for field, value in [('opened', False), ('owner_instruction', ''), ('stage', 'eval')]:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as name:
                root = Path(name).resolve()
                self.fixture(root)
                self.gate[field] = value
                self.rebind()
                with self.assertRaisesRegex(ValueError, 'owner gate'):
                    D.stage_bindings(root)

    def test_changed_stage_source_and_base_source_rejected(self):
        for source in ['tools/recompute_h17_run3_dev.py', 'base.txt']:
            with self.subTest(source=source), tempfile.TemporaryDirectory() as name:
                root = Path(name).resolve()
                self.fixture(root)
                (root / source).write_bytes(b'changed')
                with self.assertRaisesRegex(ValueError, 'source bytes'):
                    D.stage_bindings(root)

    def test_unbound_prior_evidence_rejected(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name).resolve()
            self.fixture(root)
            (root / 'experiments/h17/run3/bench/raw.npz.ap').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'prerequisite bytes'):
                D.stage_bindings(root)

    def test_prior_validity_pass_does_not_waive_failed_bench_clause(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name).resolve()
            self.fixture(root)
            path = root / 'experiments/h17/run3/bench/metrics.json'
            metric = R.read(path)
            metric['clauses']['0']['status'] = 'FAIL'
            self.put(path, metric)
            self.rebind()
            with self.assertRaisesRegex(ValueError, 'all nine PASS'):
                D.stage_bindings(root)

    def test_incomplete_or_rng_parent_rejected(self):
        for field, value, message in [('complete', False, 'validity'), ('rng_created', True, 'parent/evidence')]:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as name:
                root = Path(name).resolve()
                self.fixture(root)
                path = root / 'experiments/h17/run3/bench/parent_recomputation.json'
                parent = R.read(path)
                parent[field] = value
                self.put(path, parent)
                self.rebind()
                with self.assertRaisesRegex(ValueError, message):
                    D.stage_bindings(root)

    def test_incomplete_stage_inventory_rejected(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name).resolve()
            self.fixture(root)
            self.pins['files_sha256_alpha'].pop('tests/test_recompute_h17_run3_dev.py')
            self.rebind()
            with self.assertRaisesRegex(ValueError, 'source inventory'):
                D.stage_bindings(root)

    def input_fixture(self):
        common = dict(complete=True, passed=True, stage='dev', smoke=False,
            rows=400, steps=600, conditions=list(R.CONDITIONS), provenance={'bound': 'a' * 64})
        identity = dict(common, raw_arrays={'sha256_alpha': 'b' * 64})
        verifier = dict(common, raw_sha256_alpha='b' * 64,
            gates={str(i): dict(complete=True, passed=True, rows=400, steps=600) for i in range(20)})
        return identity, verifier, copy.deepcopy(common)

    def test_dev_failed_and_inconclusive_clauses_are_transparency_only(self):
        for verdict, status in [('NOT_SHOWN', 'FAIL'), ('INCONCLUSIVE/NOT_SHOWN', 'INCONCLUSIVE')]:
            with self.subTest(verdict=verdict):
                identity, verifier, metrics = self.input_fixture()
                clauses = {'example': dict(estimate=0.0, interval=[-.1, .1], bar=.1, direction='lower', status=status)}
                for saved in (metrics, verifier):
                    saved.update(verdict=verdict, clauses=copy.deepcopy(clauses))
                D.check_input(identity, verifier, metrics)
                D.check_clauses(clauses, verdict, metrics)
                D.check_clauses(clauses, verdict, verifier)

    def test_dev_validity_fault_is_not_waived_by_statistical_pass(self):
        identity, verifier, metrics = self.input_fixture()
        verifier['passed'] = False
        metrics['verdict'] = 'PASS'
        with self.assertRaisesRegex(ValueError, 'prerequisite'):
            D.check_input(identity, verifier, metrics)

    def test_stage_sample_provenance_and_raw_corruption_rejected(self):
        for object_name, field, value, message in [
                ('verifier', 'stage', 'bench', 'stage binding'),
                ('metrics', 'rows', 40, 'fixed sample'),
                ('verifier', 'raw_sha256_alpha', 'c' * 64, 'raw binding'),
                ('metrics', 'provenance', {}, 'provenance binding')]:
            with self.subTest(field=field):
                identity, verifier, metrics = self.input_fixture()
                {'identity': identity, 'verifier': verifier, 'metrics': metrics}[object_name][field] = value
                with self.assertRaisesRegex(ValueError, message):
                    D.check_input(identity, verifier, metrics)

    def test_saved_interval_mismatch_rejected(self):
        clauses = {'example': dict(estimate=.2, interval=[.1, .3], bar=.1, direction='lower', status='PASS')}
        saved = dict(clauses=copy.deepcopy(clauses), verdict='PASS')
        saved['clauses']['example']['interval'][1] = .4
        with self.assertRaisesRegex(ValueError, 'interval'):
            D.check_clauses(clauses, 'PASS', saved)

    def test_post_recompute_rejects_changed_saved_evidence(self):
        for name in ('identity.json', 'metrics.json', 'verification.json',
                     'stage_binding.json', 'claim.json', 'raw.npz.ap'):
            with self.subTest(artifact=name), tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / name
                path.write_bytes(b'initial saved artifact')
                initial = {path: D.file_digest(path)}
                D.check_saved_artifacts(initial)
                path.write_bytes(b'changed while recomputing')
                with self.assertRaisesRegex(ValueError, 'saved artifact changed'):
                    D.check_saved_artifacts(initial)


if __name__ == '__main__':
    unittest.main()
