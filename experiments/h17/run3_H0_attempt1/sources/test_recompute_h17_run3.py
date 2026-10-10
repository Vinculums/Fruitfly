"""Saved-data root arithmetic fixtures; no generator/controller construction."""
from pathlib import Path
import copy
import json
import sys
import tempfile
import unittest
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import recompute_h17_run3 as parent


class RootArithmeticTests(unittest.TestCase):
    def test_reference_shadow_is_not_actual_intervention(self):
        whiffs = np.zeros((600, 2, 2), bool)
        reach = np.zeros_like(whiffs)
        actual = np.zeros((600, 2), bool)
        shadow_entry = np.zeros_like(actual)
        shadow_entry[249] = True
        end = parent.row_endpoints(whiffs, reach, np.array([0, 1], np.int64), actual, shadow_entry)
        self.assertEqual(end['first_entry_step'].tolist(), [249, 249])
        self.assertEqual(end['entry_event_count'].tolist(), [1, 1])
        self.assertFalse(end['ever_engaged'].any())

    def test_endpoint_horizon_identity_and_tie(self):
        whiffs = np.zeros((600, 2, 2), bool)
        whiffs[599, 0, 1] = True
        reach = np.zeros_like(whiffs)
        reach[:20, 0, 1] = True
        reach[:20, 1] = True
        end = parent.row_endpoints(whiffs, reach, np.array([1, 0], np.int64), np.zeros((600, 2), bool))
        self.assertEqual(end['E'].tolist(), [True, False])
        self.assertEqual(end['L'].tolist(), [False, True])
        self.assertEqual(end['V'].tolist(), [True, False])
        self.assertEqual(end['D_other'].tolist(), [0, 20])

    def test_derived_phase_survives_hold_and_off_has_no_entry(self):
        whiffs = np.zeros((600, 1, 2), bool)
        held = np.full((600, 1), -1, np.int64)
        held[249:299] = 0
        signs = np.ones((600, 1), np.float64)
        tgt = np.full((600, 1), 180.0)
        est = np.full_like(tgt, 180.0)
        turn = np.full_like(tgt, 2.0)
        data = parent.policy_arrays(whiffs, held, signs, tgt, turn, est, True)
        self.assertEqual(data['u'][299, 0], 50)
        self.assertEqual(data['leg'][299, 0], 2)
        self.assertEqual(data['remaining'][299, 0], 40)
        self.assertEqual(data['SEARCH_TGT'][299, 0], 105.0)
        self.assertEqual(data['SEARCH_TURN'][299, 0], -38.0)
        off = parent.policy_arrays(whiffs, held, signs, tgt, turn, est, False)
        self.assertTrue(off['eligible'][299, 0])
        self.assertFalse(off['engaged'].any())
        self.assertFalse(off['entry'].any())
        self.assertTrue((off['u'] == -1).all())

    def test_interval_classification_keeps_inconclusive(self):
        self.assertEqual(parent.judge(0.0, (-.06, .01), -.05, 'lower')['status'], 'INCONCLUSIVE')
        self.assertEqual(parent.judge(.1, (.08, .12), .05, 'upper')['status'], 'FAIL')
        self.assertEqual(parent.judge(.6, (.55, .65), .5, 'lower')['status'], 'PASS')
        lo = parent.wilson_interval(np.arange(400) < 219)[1][0]
        hi = parent.wilson_interval(np.arange(400) < 220)[1][0]
        self.assertLess(lo, .5)
        self.assertGreaterEqual(hi, .5)

    def test_same_bytes_rejects_negative_zero(self):
        with self.assertRaises(ValueError):
            parent.same(np.array([-0.0]), np.array([0.0]), 'native bits')

    def test_all_nine_clauses_and_one_regression_stop(self):
        fixtures = {}
        for condition in parent.CONDITIONS:
            fixtures[condition] = {}
            for arm in ('Fly', 'GS250'):
                fixtures[condition][arm] = dict(E=np.zeros(400, bool),
                    L=np.zeros(400, bool), V=np.zeros(400, bool),
                    D_other=np.zeros(400, np.int64), ever_engaged=np.zeros(400, bool))
        fixtures['C0']['GS250']['E'][:] = True
        indices = np.broadcast_to(np.arange(400, dtype=np.int64), (5000, 400)).copy()
        clauses, verdict = parent.required_clauses(fixtures, indices)
        self.assertEqual(len(clauses), 9)
        self.assertEqual(verdict, 'PASS')
        fixtures['T3']['GS250']['L'][:30] = True
        clauses, verdict = parent.required_clauses(fixtures, indices)
        self.assertEqual(clauses['T3_L']['status'], 'FAIL')
        self.assertEqual(verdict, 'NOT_SHOWN')
        with self.assertRaises(ValueError):
            parent.required_clauses(fixtures, indices.astype(np.int32))

    def test_stale_verification_is_rejected_before_archive_or_pins(self):
        provenance = {'source_closure_sha256_alpha': 'a' * 64}
        identity = dict(complete=True, passed=True, smoke=True, stage='H0',
                        provenance=provenance, raw_arrays={'sha256_alpha': 'a' * 64})
        verification = dict(complete=True, passed=True, smoke=True, stage='H0',
                            provenance=provenance, raw_sha256_alpha='a' * 64)
        metrics = dict(complete=True, smoke=True, stage='H0', provenance=provenance)
        for artifact, field, replacement, error in (
                ('verification', 'raw_sha256_alpha', 'b' * 64, 'raw binding'),
                ('verification', 'stage', 'bench', 'stage binding'),
                ('metrics', 'provenance', {'source_closure_sha256_alpha': 'b' * 64}, 'provenance binding'),
                ('metrics', 'smoke', False, 'H0/MAIN mode')):
            with self.subTest(artifact=artifact, field=field), tempfile.TemporaryDirectory() as name:
                fixture = copy.deepcopy(dict(identity=identity, verification=verification, metrics=metrics))
                fixture[artifact][field] = replacement
                directory = Path(name)
                for key, value in fixture.items():
                    (directory / (key + '.json')).write_text(json.dumps(value), encoding='utf-8')
                with self.assertRaisesRegex(ValueError, error):
                    parent.recompute(directory, True)


if __name__ == '__main__':
    unittest.main()
