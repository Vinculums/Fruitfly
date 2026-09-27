#!/usr/bin/env python3
"""H12 Package E interpretation note: measurement only on the three preserved 400-row records.

Usage: python src/h12_expression_interpret.py > experiments/h12/h12_expression_interpret.txt

Written after the owner's review of the Package E result (2026-09-27). It runs no simulation and changes no verdict. It reads
the unmodified rows.json of calibration, development and evaluation and prints:
  (1) the input hashes;
  (2) whether every no-decay arm (D0_off, D1200_off, D5000_off) gives the same dwell in every row, although their eligibility
      traces differ after 1200 and 5000 silent steps (only the V value is shared);
  (3) V-majority by the retained V value, pooled over the D0_off, D1200_on and D5000_on arms of the three stages;
  (4) per stage, the primary effect predicted as (rows whose V value crosses N = +0.5 at D 5000) x (supplied high minus low
      V-majority), against the observed paired difference;
  (5) zero-contact ties per arm (design section 3 asks for them apart from equal positive dwell);
  (6) the overlap of the no-decay V-majority rows between stages (each stage has 69 of 400).
The code path behind (2)-(4): during the read-out src/h12_expression.py writes the retained V value into `a.known` before every
act (lines 150, 164); with `known` set the agent reads its valence from `known` only (ph14.py:52-53 chan_valence, ph11.py:183-184,
ph16.py:88), so the transplanted module (line 146) is never read by the body.
"""
import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
H12 = ROOT / "experiments/h12"
STAGES = {"calibration": H12 / "expression_calibration/calibration/rows.json",
          "development": H12 / "expression_development/development/rows.json",
          "evaluation": H12 / "expression_evaluation/evaluation/rows.json"}
ARMS = ("D0_off", "D0_on", "D1200_off", "D1200_on", "D5000_off", "D5000_on",
        "supplied_high", "supplied_low", "supplied_equal")
C = 0.5
BINS = ((-1.0, 0.30), (0.30, 0.40), (0.40, 0.45), (0.45, 0.50), (0.50, 0.55), (0.55, 0.60), (0.60, 0.80), (0.80, 1.01))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def choice(rows, arm, field):
    return np.array([r[arm + "_choice"][field] for r in rows])


def value(rows, arm):
    return np.array([r[arm]["value"] for r in rows])


def main():
    print("H12 Package E interpretation note (measurement only; no simulation; verdicts unchanged)")
    print(f"script sha256 {sha(__file__)}")
    data = {}
    for stage, path in STAGES.items():
        data[stage] = json.loads(path.read_text(encoding="utf-8"))
        print(f"input {path.relative_to(ROOT).as_posix()} sha256 {sha(path)} rows {len(data[stage])}")

    print("\n(2) no-decay arms: identical dwell per row although the traces differ")
    for stage, rows in data.items():
        same = all(np.array_equal(choice(rows, "D0_off", f), choice(rows, arm, f))
                   for arm in ("D1200_off", "D5000_off") for f in ("dwell_v", "dwell_n"))
        vsame = all(np.array_equal(value(rows, "D0_off"), value(rows, arm)) for arm in ("D1200_off", "D5000_off"))
        print(f"  {stage:12s} dwell identical in all 400 rows: {same}; V value identical: {vsame}")

    print("\n(3) V-majority by retained V value, pooled over D0_off, D1200_on, D5000_on of the three stages")
    v = np.concatenate([value(rows, arm) for rows in data.values() for arm in ("D0_off", "D1200_on", "D5000_on")])
    c = np.concatenate([choice(rows, arm, "v_majority") for rows in data.values()
                        for arm in ("D0_off", "D1200_on", "D5000_on")])
    print(f"  rows {len(v)}")
    for lo, hi in BINS:
        m = (v >= lo) & (v < hi)
        print(f"  V in [{lo:+.2f}, {hi:+.2f}): n {int(m.sum()):4d}  V-majority {c[m].mean():.3f}")
    print(f"  V <= +0.5: n {int((v <= C).sum())}  V-majority {c[v <= C].mean():.3f}")
    print(f"  V >  +0.5: n {int((v > C).sum())}  V-majority {c[v > C].mean():.3f}")

    print("\n(4) primary effect predicted from the value rank crossing and the supplied-value contrast")
    for stage, rows in data.items():
        cross = np.array([r["rank_cross_5000"] for r in rows]).mean()
        high = choice(rows, "supplied_high", "v_majority").mean()
        low = choice(rows, "supplied_low", "v_majority").mean()
        observed = (choice(rows, "D5000_on", "v_majority").astype(float) -
                    choice(rows, "D5000_off", "v_majority")).mean()
        print(f"  {stage:12s} crossing {cross:.4f} x (high {high:.4f} - low {low:.4f} = {high - low:.4f})"
              f" = predicted {cross * (high - low):.4f}; observed {observed:.4f}; difference {observed - cross * (high - low):+.4f}")

    print("\n(5) zero-contact ties (tie with dwell_v = dwell_n = 0) per arm")
    for stage, rows in data.items():
        counts = {arm: int((choice(rows, arm, "tie") & choice(rows, arm, "zero_contact")).sum()) for arm in ARMS}
        ties = {arm: int(choice(rows, arm, "tie").sum()) for arm in ARMS}
        print(f"  {stage:12s} zero-contact {counts}")
        print(f"  {'':12s} all ties     {ties}")

    print("\n(6) no-decay V-majority rows (D5000_off) and their overlap between stages")
    sets = {stage: set(np.flatnonzero(choice(rows, "D5000_off", "v_majority")).tolist()) for stage, rows in data.items()}
    for stage, s in sets.items():
        print(f"  {stage:12s} {len(s)} of 400")
    names = list(sets)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = sets[names[i]], sets[names[j]]
            print(f"  {names[i]} and {names[j]}: {len(a & b)} rows in common (chance expectation {len(a) * len(b) / 400:.1f})")


if __name__ == "__main__":
    main()
