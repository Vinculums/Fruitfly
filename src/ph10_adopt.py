#!/usr/bin/env python3
"""H14 adoption check, under decision:h14-adopt-tau1 (owner, 2026-09-20).

The owner chose to adopt the exact-kernel ring at tau 1, sigma 0.5, after restating the drift
bound in fly-referenced terms. This script is the check that the adopted setting passes the
restated battery at ALL three ring sizes and across the whole velocity range. I2b only tested
n=16, so this is not a formality.

Restated drift bound (the only criterion that changed):
    Phase 3's own stress table records the adopted design drifting 4.3 degrees median over 1000
    dark steps at noise sd 0.3 (the noise the Phase 5 agent actually used), and 17.6 at sd 1.0
    (the level Phase 3 recorded as fly-like). The bound is now: drift at noise 0.01 must not
    exceed 4.3 degrees, i.e. the new ring at its cleanest must be no less stable than the old
    ring at the noise it was actually run at. That anchors the bound to something already
    accepted rather than to the number that happened to come out.
Every other Phase 3 bound is unchanged.
"""
import sys
import numpy as np
from ph3 import cue, circdiff, nbumps
from ph10 import RingExact, KW

R = 200
DRIFT_BOUND = 4.3          # restated, see docstring
ADOPT = dict(tau=1.0, sigma=0.5)
VS = (0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 40.0)


def ring(n, seed=0, noise=0.01):
    kw = {**KW, "sigma": ADOPT["sigma"]}
    return RingExact(R, n=n, vgain=ADOPT["tau"], tau=ADOPT["tau"], noise=noise,
                     rng=np.random.default_rng(seed), **kw)


def battery(n):
    H = np.random.default_rng(5).uniform(0, 360, R)
    r = ring(n); c = cue(R, n, H, 1.0, width=KW["width"])
    for _ in range(200): r.step(x=c)
    single = int((nbumps(r.s) == 1).sum()); a0 = r.amp().copy(); p0 = r.pos()
    for _ in range(1000): r.step()
    alive = int((r.amp() > 0.5*a0).sum())
    drift = float(np.median(np.abs(circdiff(r.pos(), p0))))
    before = float(np.median(np.abs(circdiff(r.pos(), H))))
    for _ in range(100): r.step(x=c)
    after = float(np.median(np.abs(circdiff(r.pos(), H))))
    ratio = before/max(after, 1e-9)
    q = ring(n, seed=1)
    for _ in range(1000): q.step()
    quiet = int((q.amp() < 0.5).sum())
    gains = []
    for v in VS:
        g = ring(n);
        for _ in range(200): g.step(x=c)
        prev = g.pos(); tot = np.zeros(R)
        for _ in range(100):
            g.step(v=v); now = g.pos(); tot += circdiff(now, prev); prev = now
        gains.append(float(np.median(tot))/(v*100))
    ok = (single >= 0.95*R and alive >= 0.95*R and drift <= DRIFT_BOUND and ratio > 1.0
          and quiet >= 0.95*R and all(0.90 <= g <= 1.10 for g in gains))
    return dict(single=single, alive=alive, drift=drift, ratio=ratio, quiet=quiet,
                gains=gains, ok=ok)


if __name__ == "__main__":
    print(f"== H14 adoption check: exact kernel, tau {ADOPT['tau']}, sigma {ADOPT['sigma']},"
          f" {R} runs ==")
    print(f"   drift bound restated to {DRIFT_BOUND} deg (Phase 3's adopted ring at noise 0.3)")
    allok = True
    for n in (8, 16, 32):
        b = battery(n); allok &= b["ok"]
        print(f"\n   n={n:2d}  bump {b['single']:3d}/{R}  alive {b['alive']:3d}/{R}"
              f"  drift {b['drift']:5.2f} (bound {DRIFT_BOUND})  cue x{b['ratio']:5.1f}"
              f"  quiet {b['quiet']:3d}/{R}")
        print(f"         gain " + " ".join(f"{g:5.3f}" for g in b["gains"]) + f"   -> {'pass' if b['ok'] else 'FAIL'}")
    print(f"\n   -> adoption {'CONFIRMED at all three ring sizes' if allok else 'NOT confirmed'}")
    # and the old ring's drift at the noise it was actually used at, for the record
    from ph3 import RingDiv
    H = np.random.default_rng(5).uniform(0, 360, R)
    o = RingDiv(R, n=16, vgain=10.0, noise=0.3, rng=np.random.default_rng(0), **KW)
    c = cue(R, 16, H, 1.0, width=KW["width"])
    for _ in range(200): o.step(x=c)
    p0 = o.pos()
    for _ in range(1000): o.step()
    print(f"   reference: adopted Phase 3 ring at noise 0.3 drifts"
          f" {float(np.median(np.abs(circdiff(o.pos(), p0)))):.1f} deg over 1000 dark steps")
