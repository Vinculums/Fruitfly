#!/usr/bin/env python3
"""Read-only inspection of the already generated H12 Package D retention arrays.

Requires NumPy; uses no simulation, module import, random generator, or task seed.
  python notes/reviews/h12_inspect_retention.py --events events.npz --output inspection.json
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

TAU = 5000
TOL = 1e-10


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def number(x):
    return float(x)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    with np.load(args.events, allow_pickle=False) as z:
        code = z["H11_full_code_V"]
        weights = z["H11_full_P2_boundary_weights"]
        p1 = z["H11_full_P1_boundary_acquisition_value"]
        actual = {d: z[f"retention_decay_on_D{d}_value"] for d in (0, 1200, 5000)}
        off = {d: z[f"retention_decay_off_D{d}_value"] for d in (0, 1200, 5000)}
    n = len(code)
    require(n == 400 and weights.shape[:2] == (n, 4) and len(p1) == n,
            "A1 checkpoint shape is not the registered 400-row protocol")
    norm = np.maximum(code.sum(1, keepdims=True), 1)
    outputs = np.einsum("rck,rk->rc", weights, code) / norm
    acq = outputs[:, 0] - outputs[:, 1]
    par = outputs[:, 2] - outputs[:, 3]
    expected = {d: acq + par*((1.0-1.0/TAU)**d) for d in (0, 1200, 5000)}
    errors = {str(d): number(np.max(np.abs(actual[d]-expected[d]))) for d in expected}
    require(all(np.isfinite(actual[d]).all() for d in actual), "nonfinite retained value")
    require(all(err <= TOL for err in errors.values()),
            f"zero-input analytical decay disagrees with stored retention values: {errors}")
    require(np.array_equal(actual[0], off[0]), "D0 clones not equal")
    require(np.array_equal(off[0], off[1200]) and np.array_equal(off[0], off[5000]),
            "decay-off value changed under zero input")
    sign = np.sign(p1)
    denominator = sign*(p1-actual[0])
    finite = np.isfinite(denominator)
    valid = (sign != 0) & finite & (denominator > 1e-12)
    invalid = ~valid
    negative = {d: set(np.flatnonzero(actual[d] < 0).tolist()) for d in actual}
    negative_union = sorted(set().union(*negative.values()))
    records = []
    for row in negative_union:
        records.append({
            "row": row,
            "P1_acquisition_value": number(p1[row]),
            "P2_acquisition_output_component": number(acq[row]),
            "P2_parallel_output_component": number(par[row]),
            "P2_extinguished_value": number(actual[0][row]),
            "D1200_value": number(actual[1200][row]),
            "D5000_value": number(actual[5000][row]),
            "P1_sign_preserved_at_D5000": bool(sign[row]*actual[5000][row] > 0),
            "acquisition_component_negative_at_P2": bool(acq[row] < 0),
            "valid_recovery_denominator": bool(valid[row]),
            "recovery_denominator": number(denominator[row])})
    invalid_records = []
    for row in np.flatnonzero(invalid):
        reasons = []
        if sign[row] == 0:
            reasons.append("zero_P1_sign")
        if not finite[row]:
            reasons.append("nonfinite_denominator")
        if finite[row] and denominator[row] <= 1e-12:
            reasons.append("nonpositive_or_tiny_signed_denominator")
        invalid_records.append({"row": int(row), "reasons": reasons,
                                "P1_value": number(p1[row]),
                                "P2_value": number(actual[0][row]),
                                "signed_denominator": (number(denominator[row]) if finite[row] else None),
                                "P2_acquisition_component": number(acq[row]),
                                "P2_parallel_component": number(par[row]),
                                "D5000_value": number(actual[5000][row])})
    result = {
        "events_sha256": hashlib.sha256(args.events.read_bytes()).hexdigest(),
        "rows": n, "tau": TAU, "formula": "acq_P2 + par_P2 * (1 - 1/5000)^D",
        "analytic_max_abs_error_by_D": errors, "analytic_tolerance": TOL,
        "decay_off_invariant": True, "D0_clones_equal": True,
        "negative_row_ids_by_D": {str(d): sorted(negative[d]) for d in negative},
        "same_negative_indices_at_D0_D1200_D5000": negative[0] == negative[1200] == negative[5000],
        "negative_rows_union": records,
        "sign_preserved_count_D5000": int(np.sum(sign*actual[5000] > 0)),
        "valid_signed_recovery_denominator_count": int(valid.sum()),
        "invalid_signed_recovery_denominator_count": int(invalid.sum()),
        "invalid_denominator_rows": invalid_records,
        "negative_D5000_with_negative_acquisition_component": int(np.sum(
            (actual[5000] < 0) & (acq < 0))),
        "negative_D5000_with_nonnegative_acquisition_component": int(np.sum(
            (actual[5000] < 0) & (acq >= 0)))}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(f"retention inspection complete: {len(negative_union)} ever-negative rows, "
          f"{int(invalid.sum())} invalid denominators; max analytic error {max(errors.values()):.3e}", flush=True)


if __name__ == "__main__":
    main()
