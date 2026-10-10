"""D0 exact arithmetic against independent enumeration, and hold event timing."""
import itertools
from pathlib import Path
import sys
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from hold_d0_metrics import exact_proxy, hold_records


class D0Tests(unittest.TestCase):
    def test_proxy_against_enumerated_draws(self):
        # Four uncertain whiffs per channel, separated to exercise bursts,
        # persistence, replacement and a nonburst whiff after the window.
        times = (0, 1, 2, 11)
        pb = np.zeros((12, 1)); pd = pb.copy()
        pb[list(times), 0] = (.2, .4, .7, .6)
        pd[list(times), 0] = (.3, .8, .5, .9)
        expected = np.zeros(3)
        for bits in itertools.product((0, 1), repeat=8):
            whiffs = np.zeros((12, 2), bool)
            whiffs[list(times), 0] = bits[:4]; whiffs[list(times), 1] = bits[4:]
            weight = 1.0
            for chan, probabilities in enumerate((pb, pd)):
                for t in times:
                    weight *= probabilities[t, 0] if whiffs[t, chan] else 1-probabilities[t, 0]
            recent = [[], []]; bb = [-1, -1]; counts = np.zeros(3)
            for t, x in enumerate(whiffs):
                burst = [bool(x[c] and sum(t-s <= 9 for s in recent[c]) >= 2) for c in range(2)]
                for c in range(2):
                    if burst[c]: bb[c] = t
                    if x[c]: recent[c].append(t)
                tied = bb[0] == bb[1] and bb[0] >= 0
                counts += (all(burst), tied, tied and bool(x[0] != x[1]) and not any(burst))
            expected += weight*counts
        result = exact_proxy(pb, pd)
        actual = [result[key]['expected_total'] for key in
                  ('simultaneous_bursts', 'latest_burst_tie_row_steps', 'tied_single_nonburst_row_steps')]
        np.testing.assert_allclose(actual, expected, rtol=1e-13, atol=1e-14)

    def test_never_tie_is_not_a_tie(self):
        result = exact_proxy(np.zeros((20, 2)), np.zeros((20, 2)))
        self.assertEqual(result['latest_burst_tie_row_steps']['expected_total'], 0)
        self.assertEqual(result['probability_at_least_40_rows_upper_bound'], 0)

    def test_reset_request_is_separate_from_identity_exit(self):
        initial = dict(h=np.array([0]), c=np.array([[140., 0.]]))
        samples = [dict(h=np.array([h]), c=np.array([[c, 0.]]),
                        timeout=np.array([to]), evidence=np.array([ev]))
                   for h, c, to, ev in ((0, 141, False, True), (0, 142, False, True),
                                       (-1, 143, True, True))]
        record, = hold_records(np, samples, initial)
        self.assertTrue(record['inherited_at_start'])
        self.assertEqual(record['maximum_held_counter'], 142)
        self.assertEqual(record['reset_to_exit_lag'], 2)
        self.assertEqual(record['max_consecutive_reset_steps'], 3)
        self.assertEqual(record['survived_evidence_reset_steps'], 2)
        self.assertEqual(record['exit_reset_cause'], 'both')

    def test_right_censored_hold(self):
        initial = dict(h=np.array([-1]), c=np.array([[0., 0.]]))
        samples = [dict(h=np.array([1]), c=np.array([[1., 0.]]),
                        timeout=np.array([False]), evidence=np.array([False]))]
        record, = hold_records(np, samples, initial)
        self.assertFalse(record['inherited_at_start'])
        self.assertTrue(record['right_censored'])
        self.assertIsNone(record['reset_to_exit_lag'])


if __name__ == '__main__': unittest.main()
