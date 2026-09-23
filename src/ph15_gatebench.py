#!/usr/bin/env python3
"""Bench evidence for what the extinction gate prevents, at the agent's own learning parameters.

Phase 7.2's probe (ph8.f2_sustained): the odour code and its reinforcement together on EVERY step,
i.e. one unbroken stay at a source. Reported for the gated rule (adopted) and the ungated rule,
for reward (compartment 1) and punishment (compartment 0): the learned valence after n continuous
steps. This ties the gate comparison's readability in H15 Run 2 to CONTINUOUS exposure length,
not to a cumulative count. No task, no score.
"""
import numpy as np
import ph8
from ph8 import MB4, f2_sustained
from ph11 import MB

for comp, name in ((1, "reward"), (0, "punishment")):
    for gated in (True, False):
        make = lambda: MB4(ph8.R, parallel=False, gated=gated, rng=np.random.default_rng(0), **MB)
        peak, final, kept, traj = f2_sustained(make, comp=comp)
        print(f"{name:10s} {'gated  ' if gated else 'ungated'} peak |valence| {peak:5.3f}, after 400 steps {final:5.3f}"
              f" ({kept:5.1f}% of peak) | " + "  ".join(f"n={t}: {v:+.3f}" for t, v in traj))
