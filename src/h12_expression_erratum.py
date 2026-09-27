#!/usr/bin/env python3
"""H12 Package E erratum: the equal-value control stratified by the valued source's physical side.

Usage: python src/h12_expression_erratum.py --output experiments/h12/erratum > experiments/h12/erratum/stdout.log

Design v2 FINAL section 3 registers 'equal-value V-majority intervals within [0.35,0.65] in each of the two valued-side
strata'. The harness stratified on baseline["good"] (src/h12_expression.py:333), which is the valued odour's identity
(World7: good = cell // 2, src/ph16.py:51), not its side (side = +1 if cell % 2 == 0, the valued source at +y). This script
runs no simulation. It reads the three preserved rows.json and summary.json files, rebuilds each stage's registered bootstrap
index matrix (default_rng(bootstrap_seed).integers(0, 400, size=(5000, 400)), as the harness), reproduces the recorded
identity-strata intervals and the primary interval exactly, and then computes the same side_interval on the physical side.
Every original file is left unchanged.
"""
import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(newline="\n")  # LF output, so the recorded sha256 equals the committed blob
ROOT = Path(__file__).resolve().parents[1]
H12 = ROOT / "experiments/h12"
STAGES = {"calibration": H12 / "expression_calibration/calibration",
          "development": H12 / "expression_development/development",
          "evaluation": H12 / "expression_evaluation/evaluation"}
BOOTSTRAP = {"calibration": 20261283, "development": 31013, "evaluation": 71013}   # the registered manifest
NROWS, NBOOT = 400, 5000
GATE = (0.35, 0.65)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def interval(x, draws):
    """src/h12_expression.py:230-232, unchanged."""
    values = np.asarray(x, float)[draws].mean(1)
    return [float(np.percentile(values, q)) for q in (2.5, 97.5)]


def side_interval(x, side, draws):
    """src/h12_expression.py:235-240, unchanged (message text aside)."""
    chosen = side[draws]
    denom = chosen.sum(1)
    require(bool(np.all(denom)), "bootstrap draw has empty stratum")
    samples = (x[draws] * chosen).sum(1) / denom
    return [float(np.percentile(samples, q)) for q in (2.5, 97.5)]


def inside(ci):
    return ci[0] >= GATE[0] and ci[1] <= GATE[1]


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--output", type=Path, required=True)
    args = cli.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    print("H12 Package E erratum: equal-value control by physical side (no simulation; original files unchanged)")
    print(f"script sha256 {sha(__file__)}")
    print(f"python {sys.version.split()[0]}  numpy {np.__version__}  platform {platform.platform()}")
    stages = {}
    for stage, folder in STAGES.items():
        rows_path, summary_path = folder / "rows.json", folder / "summary.json"
        rows = json.loads(rows_path.read_text(encoding="utf-8"))
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        print(f"\n== {stage}")
        print(f"input {rows_path.relative_to(ROOT).as_posix()} sha256 {sha(rows_path)}")
        print(f"input {summary_path.relative_to(ROOT).as_posix()} sha256 {sha(summary_path)}")
        require(len(rows) == NROWS and summary["bootstrap_seed"] == BOOTSTRAP[stage], "stage identity differs")
        draws = np.random.default_rng(BOOTSTRAP[stage]).integers(0, NROWS, size=(NBOOT, NROWS))
        good = np.array([r["readout_good"] for r in rows])
        cell = np.array([r["readout_cell"] for r in rows])
        require(np.array_equal(good, cell // 2), "readout_good is not cell // 2")
        plus_y = cell % 2 == 0                        # World7 side +1: the valued source at +y
        eq = np.array([r["supplied_equal_choice"]["v_majority"] for r in rows])
        on = np.array([r["D5000_on_choice"]["v_majority"] for r in rows], float)
        off = np.array([r["D5000_off_choice"]["v_majority"] for r in rows], float)

        # Reproduction of the recorded numbers with the rebuilt draws.
        prim = interval(on - off, draws)
        ident = {str(i): side_interval(eq, good == i, draws) for i in (0, 1)}
        prim_ok = prim == summary["primary_effect"]["ci95"]
        ident_ok = ident == summary["equal_side_v_majority_ci95"]
        print(f"reproduced primary interval {prim} equal to summary: {prim_ok}")
        print(f"reproduced identity-strata intervals {ident} equal to summary: {ident_ok}")
        require(prim_ok and ident_ok, "recorded intervals not reproduced; draws differ")

        strata = {}
        for label, mask in (("identity: valued odour index 0", good == 0), ("identity: valued odour index 1", good == 1),
                            ("physical side: valued source at +y (cell % 2 == 0)", plus_y),
                            ("physical side: valued source at -y (cell % 2 == 1)", ~plus_y)):
            ci = side_interval(eq, mask, draws)
            strata[label] = dict(n=int(mask.sum()), v_majority=int(eq[mask].sum()),
                                 point=float(eq[mask].mean()), ci95=ci, inside_gate=inside(ci))
            print(f"  {label:52s} n {int(mask.sum()):3d}  V-majority {int(eq[mask].sum()):3d}"
                  f"  point {eq[mask].mean():.4f}  95% [{ci[0]:.4f}, {ci[1]:.4f}]  inside [0.35, 0.65]: {inside(ci)}")
        phys_ok = all(v["inside_gate"] for k, v in strata.items() if k.startswith("physical"))
        other = (summary["supplied_high_minus_low"]["ci95"][0] >= 0.30 and summary["supplied_high_v_majority_ci95"][0] >= 0.70
                 and all(ci[1] <= 0.20 for ci in summary["tie_ci95"].values()))
        readable = other and phys_ok
        print(f"  other readability clauses (as recorded) pass: {other}")
        print(f"  equal-value clause on the physical side passes: {phys_ok}")
        print(f"  task readable with the registered side strata: {readable}; recorded status {summary['status']}")
        stages[stage] = dict(rows_sha256=sha(rows_path), summary_sha256=sha(summary_path),
                             bootstrap_seed=BOOTSTRAP[stage], primary_ci95=prim,
                             identity_strata_reproduced=ident_ok, strata=strata,
                             physical_side_clause_passes=phys_ok, other_readability_clauses_pass=other,
                             readable_with_physical_side=readable, recorded_status=summary["status"])
    result = dict(script_sha256=sha(__file__), numpy=np.__version__, python=sys.version, stages=stages)
    (args.output / "result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"\nwrote {args.output.as_posix()}/result.json")


if __name__ == "__main__":
    main()
