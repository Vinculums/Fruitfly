#!/usr/bin/env python3
"""Phase 7.3: H13 -- wind, stochastic encounters, and surge-and-cast.

Usage: python3 ph9.py [--quick] [demo|calib|all]

Phase 5's world had no wind and a smooth Gaussian concentration field, and its agent steered
by whether that concentration was rising. Phase 6.1 recorded that as a mismatch: real flies
surge upwind on an odour encounter and cast crosswind when they lose it, using wind direction
and the timing of encounters rather than a spatial gradient (Alvarez-Salvado et al 2018;
van Breugel and Dickinson 2014; Demir et al 2020; Kadakia et al 2022).

Phase 5's intermittent condition never discriminated, at any episode length up to 3200 steps.
Phase 6 read that as strategic rather than a matter of the clock. H13 tests that reading.

The world here deliberately has NO usable concentration gradient. An encounter is a boolean:
inside a cone extending downwind of the source, the odour is detected with a probability that
falls with distance. There is nothing to climb. Scope is navigation only -- one source, no
odour identity, no learning -- so the strategy is isolated from selection and valence.

Criteria: record:phase7-3-success-criteria, stored before this file existed. G1 in particular
fixes the world's geometry against two probes BEFORE any agent comparison is looked at.
"""
import sys
import numpy as np
from ph3 import RingDiv, cue, circdiff

R = 200
QUICK = "--quick" in sys.argv
if QUICK: R = 40

ARENA, HIT_R, SPEED, STEPS = 40.0, 3.0, 0.6, 600
# wind blows toward +x, i.e. heading 0. Upwind, toward the source, is heading 180.
UPWIND = 180.0
W0, SLOPE, LAM, LMAX = 1.5, 0.25, 12.0, 25.0     # plume cone geometry, frozen by G1
# MAXOFF is the widest the cast swings away from upwind. It must exceed 90 degrees. At 90 the
# reachable target headings are exactly [90, 270], every one of which has a non-positive x
# component, so an agent that overshoots the source can never turn back downwind and the plume
# is behind it forever. Measured at MAXOFF 90: agents reached the source, scored the ten steps
# it takes to cross it, and left for good.
CAST_PERIOD, CAST_GROW, MAXOFF = 30, 1.2, 170.0
GAIN, MAXTURN, TURN_NOISE = 0.6, 40.0, 6.0


class WindWorld:
    """A cone of intermittent whiffs extending downwind of a point source.

    p_hit 1.0 gives a continuous plume (still a cone, still no gradient along it beyond the
    exponential fall-off); p_hit 0.3 gives the intermittent case Phase 5 could not read.
    """

    def __init__(self, runs, rng, p_hit=0.3, p_wind=1.0, mode="plume"):
        # mode 'gradient' replaces the boolean cone with Phase 5's smooth Gaussian field, as a
        # control. ADDED after the first comparison, because G4 as written could not be read:
        # the gradient rule scores exactly 0.0 in both cone conditions, so a percentage gap
        # against it is 100 percent by construction. A cone with p_hit 1.0 is still boolean and
        # still has nothing to climb, so it was never the control G4 was reaching for. This is.
        self.mode = mode
        self.R, self.rng, self.p_hit, self.p_wind = runs, rng, p_hit, p_wind
        self.src = rng.uniform(8.0, ARENA - 8.0, (runs, 2))
        # Start INSIDE the cone, downwind of the source. The task is then "track this plume
        # to its source", which is what H13 is about, rather than "find a needle first".
        # An earlier version scattered the start over +-8 crosswind, which put about half the
        # agents outside a cone only 4 units wide at that distance; they got 1.4 encounters
        # each in 600 steps and no strategy could have been told apart from any other.
        along = rng.uniform(5.0, 18.0, runs)
        halfw = W0 + SLOPE*along
        self.pos = np.stack([np.clip(self.src[:, 0] + along, 0, ARENA),
                             np.clip(self.src[:, 1] + rng.uniform(-1.0, 1.0, runs)*halfw,
                                     0, ARENA)], 1)
        self.head = rng.uniform(0, 360, runs)

    def sense(self):
        if self.mode == "gradient":
            # Phase 5's world: a smooth Gaussian the gradient rule can actually climb.
            d = np.linalg.norm(self.pos - self.src, axis=1)
            return np.exp(-0.5*(d/9.0)**2)
        d_along = self.pos[:, 0] - self.src[:, 0]          # > 0 means downwind of the source
        d_cross = np.abs(self.pos[:, 1] - self.src[:, 1])
        cone = (d_along > 0) & (d_along < LMAX) & (d_cross < W0 + SLOPE*d_along)
        # the source itself emits. Without this the cone has a dead spot exactly where the
        # agent has to lock on: measured hit rate at d_along 0 was 0.000 against 0.93 at 0.5,
        # so an agent that arrived could not tell it had arrived.
        at_src = np.linalg.norm(self.pos - self.src, axis=1) < 3.0
        p = self.p_hit*np.exp(-np.maximum(d_along, 0.0)/LAM)
        return (cone | at_src) & (self.rng.random(self.R) < p)

    def wind_on(self):
        return self.rng.random(self.R) < self.p_wind

    def move(self, turn):
        self.head = (self.head + turn) % 360.0
        a = np.radians(self.head)
        p = self.pos + SPEED*np.stack([np.cos(a), np.sin(a)], 1)
        for k, flip in ((0, 180.0), (1, 0.0)):
            out = (p[:, k] < 0) | (p[:, k] > ARENA)
            if out.any():
                p[out, k] = np.clip(2*np.clip(p[out, k], 0.0, ARENA) - p[out, k], 0.0, ARENA)
                self.head[out] = (flip - self.head[out]) % 360.0
        self.pos = p

    def at_source(self):
        return np.linalg.norm(self.pos - self.src, axis=1) < HIT_R


def angdiff(a, b): return (np.asarray(a) - np.asarray(b) + 180.0) % 360.0 - 180.0


class Nav:
    """rule: 'cast' | 'grad' | 'freq' | 'ideal' | 'random'.

    head_mem controls ONE thing: whether the agent integrates its own turns between wind
    samples. Wind direction is mechanosensory and instantaneous, so sensing it is never
    ablated; what the ring buys is dead reckoning while the reference is unavailable. With
    p_wind 1.0 the reference is always there and the ring should be redundant, which is what
    G3 will say. The intermittent-wind condition is where it can earn its place.
    """

    def __init__(self, runs, rng, rule="cast", head_mem="integrate"):
        self.R, self.rng, self.rule, self.head_mem = runs, rng, rule, head_mem
        self.ring = RingDiv(runs, n=16, J=0.5, c=2.0, p=2.0, sigma=0.3, Rmax=2.0,
                            width=1.2, vgain=10.0, noise=0.3,
                            rng=rng) if head_mem == "ring" else None
        self.last_turn = np.zeros(runs)
        self.belief = np.zeros(runs)           # the agent's own heading estimate
        self.since = np.zeros(runs)            # steps since the last encounter
        self.prev = np.zeros(runs)
        self.ever = np.zeros(runs, bool)
        self.rate = np.zeros(runs)             # low-passed encounter rate

    def estimate(self, w, wind_on):
        """The agent's belief about its own heading.

        Three modes, because the adopted Phase 3 ring turns out not to be usable here:
          'ring'       Phase 3's RingDiv, as adopted. Reported, and expected to fail. Its
                       velocity integration was calibrated at 0.225 deg/step, where its gain
                       is 0.99; measured at 5 deg/step the gain is 0.13 and at 20 deg/step it
                       is -0.06, sign reversed. This agent turns up to 40 deg/step.
          'integrate'  plain dead reckoning, corrected whenever the wind is sensed. This is
                       what a working heading memory would do, and is the arm G3 tests.
          'none'       no dead reckoning at all: the belief is whatever the wind last showed
                       and is never updated for turns made since.
        """
        if self.head_mem == "ring":
            self.ring.step(v=self.last_turn)
            if wind_on.any():
                self.ring.step(x=cue(self.R, 16, w.head, 1.5, width=1.2)*wind_on[:, None])
            return self.ring.pos()
        if self.head_mem == "integrate":
            self.belief = (self.belief + self.last_turn) % 360.0
        self.belief = np.where(wind_on, w.head, self.belief)
        return self.belief

    def act(self, w, signal, wind_on):
        # `signal` is boolean in the plume world and a smooth concentration in the gradient
        # control. The gradient rule reads the raw value, so it has a gradient to climb where
        # one exists; everything else reads an encounter, thresholded the way Phase 5 did.
        cur = np.asarray(signal, dtype=float)
        hit = cur > 0.02
        self.ever |= hit
        self.since = np.where(hit, 0.0, self.since + 1.0)
        self.rate += 0.05*(cur - self.rate)
        est = self.estimate(w, wind_on)

        if self.rule == "random":
            turn = TURN_NOISE*3*self.rng.standard_normal(self.R)
        elif self.rule == "grad":
            # Phase 5's rule, unchanged: keep going while the signal is rising, else turn.
            turn = np.where(cur > self.prev, 0.0, 35.0)
            turn = turn + TURN_NOISE*self.rng.standard_normal(self.R)
        elif self.rule == "ideal":
            # ORACLE probe: knows where the source is and steers straight at it. It is not a
            # model of anything and could not be built from the senses the agent has; it exists
            # only to establish that the task is solvable and where the practical ceiling sits.
            #
            # An earlier version of this probe went straight upwind once it had encountered the
            # odour, and scored BELOW the random walker. That is a fact about plume geometry,
            # not a bug in the world: flying straight upwind never corrects crosswind error, so
            # an agent that starts off axis passes the source at its starting offset. Correcting
            # that error is what casting is for, which is the hypothesis, so it cannot also be
            # the probe.
            d = w.src - w.pos
            tgt = np.degrees(np.arctan2(d[:, 1], d[:, 0])) % 360.0
            turn = np.clip(GAIN*angdiff(tgt, w.head), -MAXTURN, MAXTURN)
        else:
            # surge upwind on an encounter; cast crosswind, widening, when there is none
            side = np.where((self.since // CAST_PERIOD) % 2 == 0, 1.0, -1.0)
            off = np.minimum(MAXOFF, CAST_GROW*self.since)
            if self.rule == "freq":
                # Alvarez-Salvado: a higher encounter rate biases the course further upwind
                off = off*np.clip(1.0 - 4.0*self.rate, 0.0, 1.0)
            tgt = np.where(hit, UPWIND, (UPWIND + side*off) % 360.0)
            turn = np.clip(GAIN*angdiff(tgt, est), -MAXTURN, MAXTURN)
            turn = turn + TURN_NOISE*self.rng.standard_normal(self.R)

        self.prev = cur
        self.last_turn = turn
        return turn


def episode(w, a, steps=STEPS):
    score = np.zeros(a.R)
    for _ in range(steps):
        hit = w.sense()
        w.move(a.act(w, hit, w.wind_on()))
        score += w.at_source().astype(float)
    return score


def run(rule, p_hit, head_mem="integrate", p_wind=1.0, mode="plume", seed_w=0, seed_a=1):
    w = WindWorld(R, np.random.default_rng(seed_w), p_hit=p_hit, p_wind=p_wind, mode=mode)
    a = Nav(R, np.random.default_rng(seed_a), rule=rule, head_mem=head_mem)
    return episode(w, a)


def compare(base, other, label):
    """the project's usual margin: 25 percent of the base median and 60 percent of pairs."""
    mb, mo = float(np.median(base)), float(np.median(other))
    win = float((base > other).mean())
    gap = (mb - mo)/abs(mb) if mb else float("nan")
    ok = gap >= 0.25 and win >= 0.60
    print(f"     {label:44s} {mb:7.1f} vs {mo:7.1f}   wins {win*100:5.1f}%"
          f"   gap {gap*100:+7.1f}%   -> {'YES' if ok else 'no'}")
    return ok, gap, win


# ---------------------------------------------------------------- G1, before anything else
def calibrate(p_hit, label):
    print(f"\n== G1 calibration, {label} (p_hit {p_hit}) ==")
    print("   two fixed probes only. No surge-and-cast agent is run here.")
    lo = run("random", p_hit)
    hi = run("ideal", p_hit)
    mlo, mhi = float(np.median(lo)), float(np.median(hi))
    ceil = float(STEPS)
    floor_ok = mhi >= 10.0
    ceil_ok = mhi < 0.99*ceil
    print(f"   floor probe  (random walk)      median {mlo:7.1f}")
    print(f"   ceiling probe(ideal upwind)     median {mhi:7.1f}   arithmetic ceiling {ceil:.0f}")
    print(f"   discriminates (ideal >= 10): {'yes' if floor_ok else 'NO'};"
          f"   does not saturate (< {0.99*ceil:.0f}): {'yes' if ceil_ok else 'NO'}")
    ok = floor_ok and ceil_ok
    print(f"   -> condition is {'READABLE' if ok else 'NOT readable, no verdict will be drawn'}")
    return ok, mlo, mhi


# ---------------------------------------------------------------- the comparisons
def table(p_hit, label, mode="plume"):
    print(f"\n== {label} (p_hit {p_hit}, mode {mode}), {R} agents, {STEPS} steps ==")
    arms = {}
    for rule in ("random", "grad", "cast", "freq", "ideal"):
        arms[rule] = run(rule, p_hit, mode=mode)
        print(f"   {rule:10s} median {np.median(arms[rule]):7.1f}")
    sat = [k for k, v in arms.items() if float(np.median(v)) >= 0.99*STEPS]
    if sat:
        print(f"   CEILING: {sat} at 99 percent of {STEPS}. Under G1 this condition is not read.")
    print("   matched-pair comparisons (same worlds, same seeds):")
    g2 = compare(arms["cast"], arms["grad"], "G2  surge-and-cast vs the Phase 5 gradient rule")
    compare(arms["freq"], arms["cast"], "    encounter-frequency variant vs plain cast")
    return arms, g2


def g3_heading(p_hit=0.3):
    """G3 is only askable where dead reckoning can matter.

    With the wind always available the heading reference is exact every step, so a memory of
    it has nothing to add and the two arms are the same agent. That is not a finding about
    heading memory, it is a property of the condition. G3 is therefore asked across wind
    availability, and the p_wind 1.0 row is kept in the table to show why.
    """
    print("\n== G3, does the heading memory earn its place? ==")
    print("   Wind direction is mechanosensory and instantaneous. Dead reckoning can only pay")
    print("   when that reference goes away, so the question is asked across p_wind.")
    print(f"   {'p_wind':>7} {'integrate':>10} {'none':>8} {'ring':>8}   int vs none")
    out = {}
    for pw in (1.0, 0.5, 0.2):
        a = run("cast", p_hit, head_mem="integrate", p_wind=pw)
        b = run("cast", p_hit, head_mem="none", p_wind=pw)
        c = run("cast", p_hit, head_mem="ring", p_wind=pw)
        ma, mb, mc = (float(np.median(x)) for x in (a, b, c))
        win = float((a > b).mean()); gap = (ma - mb)/abs(ma) if ma else float("nan")
        ok = gap >= 0.25 and win >= 0.60
        out[pw] = (ok, gap, win)
        print(f"   {pw:7.1f} {ma:10.1f} {mb:8.1f} {mc:8.1f}"
              f"   wins {win*100:5.1f}% gap {gap*100:+7.1f}% -> {'YES' if ok else 'no'}")
    print("   The `ring` column is Phase 3's adopted RingDiv. Its velocity integration was")
    print("   calibrated at 0.225 deg/step (gain 0.99); measured here it is 0.13 at 5 deg/step")
    print("   and -0.06, sign reversed, at 20. This agent turns up to 40 deg/step.")
    return out


def demo():
    """self-check: the world has no climbable gradient, and the cone is where it should be."""
    w = WindWorld(200, np.random.default_rng(0), p_hit=1.0)
    # on-axis, downwind of the source: detected. upwind of the source: never.
    w.pos = w.src + np.array([6.0, 0.0])
    assert w.sense().mean() > 0.4, "no detection on axis downwind"
    w.pos = w.src - np.array([6.0, 0.0])
    assert w.sense().mean() == 0.0, "detected upwind of the source, which the cone forbids"
    # far off axis at the same downwind distance: outside the cone
    w.pos = w.src + np.array([6.0, 12.0])
    assert w.sense().mean() == 0.0, "detected outside the cone"
    # the signal carries no usable gradient: it is boolean
    w.pos = w.src + np.array([6.0, 0.0])
    s = w.sense()
    assert s.dtype == bool and set(np.unique(s)).issubset({True, False}), "signal is not boolean"
    print(f"ok  cone detects downwind on axis ({w.sense().mean():.2f}), never upwind, never off cone")
    print("ok  the encounter signal is boolean, so there is no concentration to climb")


if __name__ == "__main__":
    what = [a for a in sys.argv[1:] if a in ("demo", "calib", "all")] or ["all"]
    if "demo" in what:
        demo(); sys.exit(0)
    print(f"== Phase 7.3, H13. {R} agents, {STEPS} steps ==")
    print("== Criteria: record:phase7-3-success-criteria, stored before this file existed ==")
    ok_i, _, _ = calibrate(0.3, "intermittent plume")
    ok_c, _, _ = calibrate(1.0, "continuous plume")
    if "calib" in what: sys.exit(0)

    gi = gc = None; arms_i = {}
    if ok_i: arms_i, gi = table(0.3, "Intermittent plume")
    else: print("\n== Intermittent plume: NOT readable under G1, not run ==")
    if ok_c: _, gc = table(1.0, "Continuous plume")
    else: print("\n== Continuous plume: NOT readable under G1, not run ==")

    g3 = g3_heading(0.3) if ok_i else {}

    if gi and gc:
        print("\n== G4 as written: the advantage across the two cone conditions ==")
        print(f"   surge-and-cast advantage over the gradient rule:"
              f" intermittent {gi[1]*100:+.1f}%, continuous cone {gc[1]*100:+.1f}%")
        print("   UNREADABLE. The gradient rule scores exactly 0.0 in both, so a percentage")
        print("   gap against it is 100 percent by construction. A cone at p_hit 1.0 is still")
        print("   a boolean signal with nothing to climb, so it was never the right control.")

    print("\n== G4 control, ADDED after the run: Phase 5's smooth Gaussian world ==")
    print("   The gradient rule is given the world it was designed for. If surge-and-cast")
    print("   still beats it here, the advantage is about the two rules and not about plumes.")
    ag = table(1.0, "Smooth gradient world", mode="gradient")[0]
    mg, mc = float(np.median(ag["grad"])), float(np.median(ag["cast"]))
    if arms_i:
        print(f"\n   smooth world: gradient rule {mg:.1f}, surge-and-cast {mc:.1f}")
        print(f"   plume world:  gradient rule {float(np.median(arms_i['grad'])):.1f},"
              f" surge-and-cast {float(np.median(arms_i['cast'])):.1f}")
    spec = mg > mc
    print(f"   -> the advantage IS {'specific to the plume' if spec else 'NOT specific'}:"
          f" the gradient rule {'wins' if spec else 'still loses'} where it has a gradient")

    g3_any = any(v[0] for v in g3.values())
    print("\n== H13 verdict ==")
    print(f"   G2 {'pass' if gi and gi[0] else 'FAIL'}"
          f"   G3 {'pass' if g3_any else 'FAIL'} (at any wind availability)"
          f"   G4 as written unreadable; control says"
          f" {'specific' if spec else 'not specific'}")
