#!/usr/bin/env python3
"""Input contract change: the heading memory is fed the rotation MADE, not the commanded turn.

Usage: python ph12c.py [demo]

decision:heading-input-rotation-made. H16 Run 2's step 0 showed that the two differ only at wall
contacts (100 percent of differing steps) and that a perfect integrator fed the rotation made
reproduces the heading exactly. What was not known is whether the RING can follow a reflection,
which may be a rotation of up to 180 degrees in one step, far outside what H14 measured.

Plan and readings: record:input-contract-change-verification-plan, stored before this file.
Run 1's 40x40 arena, return rule, seeds 9400/9500. Measurement of an instrument; nothing here is
a hypothesis test, and no stored file is edited.
"""
import sys
import numpy as np
from ph3 import cue
from ph9 import angdiff, STEPS
from ph11 import WIND_CUE
from ph12 import R, BLOCKS, last, med
from ph12b import World3, Nav3

SEEDS = (9400, 9500)
BINS = ((0, 45), (45, 135), (135, 181))


class Nav4(Nav3):
    """'ring_made' and 'integrate_made' receive w.rot; 'ring' and 'integrate' the commanded turn."""

    def __init__(self, runs, rng, rule, head):
        super().__init__(runs, rng, rule, "ring" if head == "ring_made" else head)
        self.head = head

    def estimate(self, w, wind_on):
        if self.head == "integrate_made":
            self.belief = np.where(wind_on, w.head, (self.belief + w.rot) % 360.0)
            return self.belief
        if self.head != "ring_made": return super().estimate(w, wind_on)
        self.ring.step(v=w.rot)
        if wind_on.any():
            self.ring.step(x=cue(self.R, 16, w.head, WIND_CUE, width=1.2)*wind_on[:, None])
        return self.ring.pos()


def measure(head, wind):
    w = World3(R, np.random.default_rng(SEEDS[0]), wind=wind, arena=40.0, shift=0.0)
    a = Nav4(R, np.random.default_rng(SEEDS[1]), "return", head)
    score = np.zeros((BLOCKS, R)); n = bad = tot = 0; contacts = 0
    ev = []                                     # (size of the reflection, error before, error after)
    p_err = np.zeros(R); p_off = np.zeros(R, bool); p_bump = np.zeros(R, bool); p_refl = np.zeros(R)
    for t in range(BLOCKS*STEPS):
        hit = w.sense(); won = w.wind_on()
        turn = a.act(w, hit, won)
        e = np.abs(angdiff(a.est, w.head))
        n += R; bad += int((e > 45).sum()); tot += float(e.sum())
        m = p_bump & p_off & ~won               # a contact with the cue off on both sides of it
        if m.any(): ev.append(np.stack([p_refl[m], p_err[m], e[m]], 1))
        w.move(turn); a.bump(w.bumped)
        p_err, p_off, p_bump = e, ~won, w.bumped.copy()
        p_refl = np.abs(angdiff(w.rot, turn)); contacts += int(w.bumped.sum())
        score[t // STEPS] += w.at_source()
    ev = np.concatenate(ev) if ev else np.zeros((0, 3))
    return dict(over45=bad/n*100, mean=tot/n, contacts=contacts/n*100, ev=ev,
                last=med(last(dict(score=score))))


def report():
    print(f"== input contract change. Run 1's 40x40 arena, return rule, seeds {SEEDS}, {R} agents,"
          f" {BLOCKS*STEPS} steps ==")
    print("\n(1) wind cue on EVERY step, H15's condition")
    for h in ("integrate", "integrate_made", "ring", "ring_made"):
        o = measure(h, "always")
        print(f"   {h:15s} heading error > 45 deg on {o['over45']:5.2f}% of agent-steps, mean |error|"
              f" {o['mean']:5.2f} deg;  contacts on {o['contacts']:5.2f}% of steps;  last third {o['last']:5.1f}")
    print("\n(2) cue dropout 50/50: does the memory FOLLOW a reflection with no cue on either side of it?")
    print("    median heading error just before the contact -> at the next step, by size of the reflection")
    for h in ("integrate", "integrate_made", "ring", "ring_made"):
        o = measure(h, "blocks"); ev = o["ev"]; cells = []
        for lo, hi in BINS:
            m = (ev[:, 0] >= lo) & (ev[:, 0] < hi)
            cells.append(f"{lo:3d}-{hi - 1 if hi > 180 else hi:3d} deg: n {int(m.sum()):6d}  "
                         f"{np.median(ev[m, 1]) if m.any() else float('nan'):6.1f} -> "
                         f"{np.median(ev[m, 2]) if m.any() else float('nan'):6.1f}")
        print(f"   {h:15s} " + "   |   ".join(cells))
        print(f"   {'':15s} over all steps: error > 45 deg {o['over45']:5.2f}%, mean |error| {o['mean']:5.2f} deg")


def demo():
    # known answer: with no wall there is no reflection, so the two contracts are the same agent
    a = Nav4(8, np.random.default_rng(0), "return", "ring_made")
    assert a.ring is not None and a.head == "ring_made"
    w = World3(50, np.random.default_rng(1), walls=False); n = Nav4(50, np.random.default_rng(2), "return", "integrate_made")
    for _ in range(300):
        turn = n.act(w, w.sense(), w.wind_on()); w.move(turn)
        assert np.allclose(np.abs(angdiff(w.rot, turn)), 0, atol=1e-6)
    print("ok  modes construct; with no wall the rotation made equals the commanded turn on every step")


if __name__ == "__main__":
    if "demo" in sys.argv[1:]: demo(); sys.exit(0)
    report()
