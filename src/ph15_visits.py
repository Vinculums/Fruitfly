#!/usr/bin/env python3
"""How many steps does ONE visit to a source deliver? Measurement only, development seeds.

The H15 Run 2 draft justified a training dose of 30 reinforced steps as 'about what one natural
visit delivers (20-28 steps)'. Those 20-28 were dwell PER BLOCK of 600 steps, not per visit. A
visit is measured here as a maximal run of consecutive steps within 3.0 of a source, and also
with gaps of up to 10 steps merged, for the adopted agent (ph14 `fix`) on seeds 9600/9700.
"""
import numpy as np
from ph9 import STEPS
from ph14 import run


def runs_of(x, gap=0):
    """lengths of the True runs in each column of a (T, R) array, runs separated by <= gap merged"""
    out, per_agent = [], []
    for r in range(x.shape[1]):
        idx = np.flatnonzero(x[:, r])
        if not len(idx): per_agent.append(0); continue
        cut = np.flatnonzero(np.diff(idx) > gap + 1)
        starts = np.r_[idx[0], idx[cut + 1]]; ends = np.r_[idx[cut], idx[-1]]
        out.extend((x[s:e + 1, r].sum() for s, e in zip(starts, ends))); per_agent.append(len(starts))
    return np.array(out), np.array(per_agent)


for cond in ("neutral", "known"):
    o = run("fix", cond, (9600, 9700))
    for name, x in (("rewarding", o["G"]), ("punishing", o["B"])):
        tot = x.sum(0); vis = tot > 0
        if not vis.any(): continue
        print(f"\n{cond}, {name} source: visited by {int(vis.sum())}/200 agents;"
              f" steps within 3.0 per block of {STEPS}, among visitors: median {np.median(tot[vis])/9:5.1f};"
              f" over the whole run: median {np.median(tot[vis]):5.0f}")
        for gap in (0, 10):
            L, n = runs_of(x, gap)
            first = [runs_of(x[:, [r]], gap)[0][0] for r in np.flatnonzero(vis)[:200]]
            print(f"   visit = run of steps within 3.0{', gaps <= 10 merged' if gap else ''}: {len(L)} visits,"
                  f" steps per visit median {np.median(L):4.0f} (p25 {np.percentile(L, 25):3.0f}, p75 {np.percentile(L, 75):3.0f}, p90"
                  f" {np.percentile(L, 90):3.0f}); visits per visiting agent median {np.median(n[vis]):4.0f};"
                  f" FIRST visit median {np.median(first):4.0f} steps")
