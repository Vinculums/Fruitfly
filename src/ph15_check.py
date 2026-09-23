#!/usr/bin/env python3
"""Bench check of the 'cross-channel division term removed' control, before any task run.

decision:h19a-adopt-and-run2-direction, item 3. The control is ph2.Upstream with k = 0. It keeps
the stage's own-channel saturation and its temporal filtering, so it is NOT 'no normalisation'.
Two things must hold: with one odour present the output time series equals the adopted stage's,
and with both present the ONLY thing that differs is the k*others term in the denominator.
"""
import numpy as np
from ph2 import Upstream

UP = dict(n=1.5, sig=0.05, Rmax=1.8, k=0.8)
T = 2000
rng = np.random.default_rng(0)

for ch in (0, 1):
    a, b = Upstream(runs=1, chans=2, **UP), Upstream(runs=1, chans=2, **{**UP, "k": 0.0})
    worst = 0.0
    for _ in range(T):
        x = np.zeros((1, 2)); x[0, ch] = float(rng.random() < 0.2)
        worst = max(worst, float(np.abs(a.step(x) - b.step(x)).max()))
    assert worst == 0.0
    print(f"ok  one odour (channel {ch}), {T} steps of random whiffs: largest output difference {worst}")

a, b = Upstream(runs=1, chans=2, **UP), Upstream(runs=1, chans=2, **{**UP, "k": 0.0})
resid, ratio = 0.0, []
for _ in range(T):
    x = (rng.random((1, 2)) < 0.2).astype(float)
    ya, yb = a.step(x), b.step(x)
    assert np.array_equal(a.P, b.P), "the filtered drive differs: more than the intended term changed"
    others = a.P.sum(1, keepdims=True) - a.P                      # N - 1 = 1
    resid = max(resid, float(np.abs(ya*(a.sig_n + a.P + UP["k"]*others) - yb*(b.sig_n + b.P)).max()))
    m = (a.P > 1e-3).all()
    if m: ratio.append(float((ya/yb).mean()))
assert resid < 1e-12
print(f"ok  both odours, {T} steps: the filtered drive is identical in the two stages, and"
      f" y_adopted*(sig^n + P + k*others) == y_control*(sig^n + P) to {resid:.1e}")
print(f"    when both odours are active the adopted output is on average {np.mean(ratio):.2f} of the control's"
      f" ({len(ratio)} steps)")
