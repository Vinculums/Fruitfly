#!/usr/bin/env python3
"""Two defects tracked apart from H19: the silence timeout, and what 'no normalisation' removes.

Usage: python ph14b.py

Measurement only (decision:h19-open-option-a, 'separate tracks'). Nothing is fixed.

1. The silence timeout fires and never releases the hold (0 of 566 losses, ph13b). Followed as a
   chain: reset requested -> value delivered to the circuit -> internal state -> selection output,
   inside the agent (the circuit's step is wrapped on the instance to log its arguments; no file
   is edited), then on a bench across pulse strength and duration.
2. Removing normalisation leaves the agent anosmic. Checked as input range against selection
   threshold: what one isolated whiff does to the circuit with and without the upstream stage,
   and whether a control that keeps the stage's gain and removes only the cross-channel division
   is well defined WITHOUT reference to any task score.
"""
import numpy as np
from ph2 import Upstream, Circuit
from ph11 import RESET_AFTER
from ph13 import World4
from ph14 import Agent3

UP = dict(n=1.5, sig=0.05, Rmax=1.8, k=0.8)
CI = dict(n=2, theta=1.0, k=12.0, noise=0.01)


def chain(seeds=(9600, 9700), runs=200, steps=2400):
    w = World4(runs, np.random.default_rng(seeds[0]))
    a = Agent3(runs, np.random.default_rng(seeds[1]), fix=False, abl=("learn",))
    log = []; orig = a.sel.step
    def spy(y, reset=0.0):
        out = orig(y, reset=reset); log.append((np.asarray(reset).ravel().copy(), a.sel.s.copy(), a.sel.S.ravel().copy()))
        return out
    a.sel.step = spy
    TO = np.zeros((steps, runs), bool); HP = np.full((steps, runs), -1); H = np.full((steps, runs), -1)
    for t in range(steps):
        TO[t] = a.silence > RESET_AFTER; HP[t] = a.held()
        turn, h = a.act(w, w.sense(), w.wind_on()); w.move(turn); a.bump(w.bumped); H[t] = h
    RST = np.array([l[0] for l in log]); S = np.array([l[1] for l in log]); G = np.array([l[2] for l in log])
    print("== 1a. the chain inside the agent (neutral, seeds 9600/9700, 2400 steps) ==")
    for label, m in (("silence timeout", TO & (HP >= 0)), ("evidence release", (RST > 0) & ~TO & (HP >= 0))):
        tt, rr = np.nonzero(m); keep = tt < steps - 9; tt, rr = tt[keep], rr[keep]; ch = HP[tt, rr]
        before = S[np.maximum(tt - 1, 0), rr, ch]
        after = np.array([S[t:t + 9, r, c].min() for t, r, c in zip(tt, rr, ch)])
        glob = np.array([G[t:t + 9, r].max() for t, r in zip(tt, rr)])
        rel = np.array([(H[t:t + 9, r] == -1).any() for t, r in zip(tt, rr)])
        run = np.array([int(np.argmin(np.r_[RST[t:t + 12, r] > 0, False])) for t, r in zip(tt, rr)])
        print(f"   {label:16s} requests {len(tt):5d} | value delivered to the circuit: {np.unique(RST[tt, rr])} |"
              f" consecutive steps with a reset: median {np.median(run):3.0f} | held unit before {np.median(before):4.2f},"
              f" lowest in the next 8 steps {np.median(after):4.2f} (threshold 1.0) | global unit peak {np.median(glob):5.2f} |"
              f" hold released within 8 steps {rel.mean()*100:5.1f}%")


def bench_reset():
    print("\n== 1b. bench: a committed circuit, reset of amplitude A for D consecutive steps; lowest value of the held unit, released? ==")
    for A in (10.0, 20.0, 40.0):
        cells = []
        for D in (1, 2, 3, 4, 6, 8):
            c = Circuit(100, rng=np.random.default_rng(0), **CI)
            for _ in range(40): c.step(np.tile([1.7, 0.0], (100, 1)))
            for _ in range(30): c.step(np.zeros((100, 2)))
            low = c.s[:, 0].copy()
            for d in range(D + 30):
                c.step(np.zeros((100, 2)), reset=np.full((100, 1), A if d < D else 0.0)); low = np.minimum(low, c.s[:, 0])
            cells.append(f"D{D}: low {np.median(low):4.2f} released {(c.s[:, 0] < 1.0).mean()*100:3.0f}%")
        print(f"   A {A:4.0f} | " + " | ".join(cells))


def bench_input():
    print("\n== 2. input range against the selection threshold: ONE isolated whiff (x = 1 for one step) ==")
    up = Upstream(runs=1, chans=2, **UP); ys = []
    for t in range(30): ys.append(up.step(np.array([[1.0 if t == 0 else 0.0, 0.0]]))[0, 0])
    ys = np.array(ys)
    print(f"   upstream output: peak {ys.max():4.2f}, above 1.0 for {(ys > 1.0).sum()} steps, above 0.05 for {(ys > 0.05).sum()} steps"
          f"  (a raw whiff is 1.0 for 1 step)")
    for label, norm in (("with the upstream stage", True), ("raw, no upstream stage", False)):
        need = None
        for nwh in range(1, 13):
            for gap in (1,):
                up = Upstream(runs=50, chans=2, **UP); c = Circuit(50, rng=np.random.default_rng(1), **CI); peak = 0.0
                for t in range(nwh*gap + 60):
                    x = np.zeros((50, 2)); x[:, 0] = 1.0 if (t < nwh*gap and t % gap == 0) else 0.0
                    c.step(up.step(x) if norm else x); peak = max(peak, float(np.median(c.s[:, 0])))
                if nwh == 1: one = peak
                if need is None and np.median(c.s[:, 0]) > 1.0: need = nwh
        print(f"   {label:26s} held unit's peak after one whiff {one:4.2f} (threshold 1.0);"
              f" consecutive whiffs needed to commit: {need if need else 'more than 12'}")
    a, b = Upstream(runs=1, chans=2, **UP), Upstream(runs=1, chans=2, **{**UP, "k": 0.0})
    one = [np.array([[1.0, 0.0]]), np.zeros((1, 2)), np.zeros((1, 2))]
    same = all(np.allclose(a.step(x), b.step(x)) for x in one)
    a, b = Upstream(runs=1, chans=2, **UP), Upstream(runs=1, chans=2, **{**UP, "k": 0.0})
    ya, yb = a.step(np.ones((1, 2)))[0, 0], b.step(np.ones((1, 2)))[0, 0]
    print(f"   control 'k = 0' (keep the stage's gain and persistence, remove only the cross-channel division):"
          f" identical to the adopted stage when one odour is present: {same};"
          f" with both odours present its output is {yb:4.2f} against {ya:4.2f}")


if __name__ == "__main__":
    chain(); bench_reset(); bench_input()
