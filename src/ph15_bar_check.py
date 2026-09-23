#!/usr/bin/env python3
"""Unrounded interval of the as-registered (no gap) manipulation check in H15 Run 2's evaluation.

The report said it 'passed at its bar'. The registered rule is: 'at most t' PASSES if the
interval's upper bound <= t, FAILS if the lower bound > t, otherwise INCONCLUSIVE. This reprints
the same deterministic numbers (evaluation seeds, fixed bootstrap seed) without rounding, to say
whether the interval crossed -0.5 or stopped on the passing side of it. Measurement only.
"""
import numpy as np
from ph15 import run_e2, boot, verdict, SEEDS

pre = run_e2("trained", SEEDS["eval"][1], gap=0, test=False)["pre"][:, 1]
pt, lo, hi = boot("GM", pre)
print(f"point {pt!r}  lower {lo!r}  upper {hi!r}  bar -0.5  upper <= bar: {hi <= -0.5}  -> {verdict(lo, hi, -0.5, True)}")
vals, counts = np.unique(np.round(pre, 6), return_counts=True)
print("distinct pre-test values of the punished odour (rounded to 1e-6) and their counts:")
for v, c in zip(vals, counts): print(f"   {v:+.6f}  x {c}")
