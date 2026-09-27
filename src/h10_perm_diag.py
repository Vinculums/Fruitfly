#!/usr/bin/env python3
"""H10 calibration: why the label-permutation check failed on the ambiguous condition (measurement only).

Usage: python src/h10_perm_diag.py > experiments/h10/calibration/perm_diag.txt

The calibration's implementation check 'label_permutation_equivariance' was False: on the ambiguous condition (cue d 0,
calibration seed 45110) the maximum state deviation between the permuted and the unpermuted 40-row runs was 1.06e-12
against the registered tolerance 1e-12. This script imports src/h10.py unchanged, rebuilds that condition exactly as the
calibration did, and reports, per arm and per output stream: whether the outputs permute exactly, the deviation over
steps, and how many rows exceed the tolerance. It re-uses only the calibration seed already spent; no other seed is used.
Nothing here changes a criterion or a verdict.
"""
import hashlib
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import h10                                                      # noqa: E402  (unchanged)

sys.stdout.reconfigure(newline="\n")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    print("H10 calibration, label-permutation check diagnosis (measurement only; calibration seeds already spent)")
    print(f"script sha256 {sha(__file__)}")
    print(f"src/h10.py sha256 {sha(h10.__file__)}  numpy {np.__version__}")
    for key, kind in (("ambiguous", "ambiguous"), ("hard_1", "hard")):
        seed = h10.SEEDS["calibration"][key]
        ch = np.random.SeedSequence(seed).spawn(3)
        tgt = h10.balanced_targets(ch[0])
        tape, _ = h10.build(kind, h10.ROWS, tgt, np.random.default_rng(ch[1]), 1.0)
        src = np.random.default_rng(ch[2])
        noise = np.asarray([src.standard_normal((h10.ROWS, h10.N)) for _ in range(len(tape))])
        r = h10.PERM_ROWS
        x0, n0 = tape[:, :r], noise[:, :r]
        plain = h10.run(x0, lambda: h10.TapeRNG(n0), keep_rows=r)
        permd = h10.run(x0[:, :, h10.PERM], lambda: h10.TapeRNG(n0[:, :, h10.PERM]), keep_rows=r)
        inv = np.argsort(h10.PERM)
        print(f"\n== {key} (seed {seed}), first {r} rows, permutation {h10.PERM.tolist()} ==")
        for a in ("bistable", "graded", "cand"):
            d = np.abs(permd["kept"][a] - plain["kept"][a][:, :, h10.PERM]).max(2)       # (T, rows)
            per_step = d.max(1)
            first = int(np.argmax(per_step > 1e-12)) + 1 if (per_step > 1e-12).any() else None
            print(f"  {a:8s} max deviation {per_step.max():.3e}; at steps 100/300/600: "
                  f"{per_step[99]:.1e} / {per_step[299]:.1e} / {per_step[-1]:.1e}; rows ever above 1e-12: "
                  f"{int((d > 1e-12).any(0).sum())} of {r}; first step above 1e-12: {first}")
        bad = []
        for n in plain["out"]:
            o = plain["out"][n].astype(int)
            mapped = np.where(o >= 0, inv[np.clip(o, 0, h10.N - 1)], -1)
            diff = permd["out"][n] != mapped
            if diff.any():
                bad.append(f"{n}: {int(diff.sum())} (row, step) in {int(diff.any(0).sum())} rows")
        print("  outputs permute exactly in every stream" if not bad else "  outputs differ: " + "; ".join(bad))


if __name__ == "__main__":
    main()
