#!/usr/bin/env python3
"""H15: the integrated agent on the wind world, with every adopted change in place.

Usage: python3 ph11.py [--quick] [demo|calib|all]

Phase 5's task, rebuilt on Phase 7.3's world: two odour sources, each emitting its own channel
as a cone of intermittent whiffs downwind, one rewarding and one punishing, which is which not
innate and learned only by arriving. There is no concentration gradient anywhere.

Modules, each at its adopted setting and none edited here:
  normalisation   ph2.Upstream, Phase 2.1                                   (unchanged)
  select and hold ph2.Circuit, theta 1 k 12, with Phase 5 Run 2's two resets: a silence
                  timeout of 40 steps and an evidence release at margin 0.2   (unchanged)
  heading memory  ph10.RingExact, tau 1 sigma 0.5 vgain=tau n=16              (H14 adoption)
  learning        ph8.MB4, gated=True parallel=False                          (7.2 adoption)
  navigation      surge-and-cast on a wind reference                          (7.3)

Criteria: record:h15-success-criteria, stored before this file. J1 freezes the world against
two probes before any agent is compared. Predictions on record in
concept:h15-integrated-agent-on-wind-world; the one this file is built to test hardest is P2,
that Select-and-Hold finally earns its place because whiffs are intermittent and holding an
identity between them is what the circuit is for.

The world persists across episodes, as ph5 did: the agent keeps its position and its weights,
and only the score is reset. The ceiling per episode is therefore STEPS.
"""
import sys
import numpy as np
from ph2 import Upstream, Circuit
from ph3 import cue
from ph8 import MB4
from ph10 import RingExact
from ph9 import (ARENA, HIT_R, SPEED, UPWIND, W0, SLOPE, LAM, LMAX, CAST_PERIOD, CAST_GROW,
                 MAXOFF, GAIN, MAXTURN, TURN_NOISE, angdiff)

R, EPISODES, STEPS = 200, 9, 600
QUICK = "--quick" in sys.argv
if QUICK: R, EPISODES = 40, 3
RESET_AFTER, MARGIN = 40, 0.2          # Phase 5 Run 2's two release conditions
# How strongly the wind sense drives the ring. Agent wiring, not a ring parameter. Phase 5 used
# 1.5 for the old ring (tau 10) and it was carried over unchanged; with the H14 ring at tau 1
# and the agent's noise of 0.3 it does not hold the heading. Measured in this agent with a
# true-heading cue on EVERY step: at 1.5, between 51 and 70 percent of agents were more than 45
# degrees wrong at every sample from step 50 to 600 (sigma 0.3 no better, so it is not the H14
# sigma). At tau 1 nothing averages the noise, and once the bump is a kernel width from the cue
# a weak cue cannot recapture it, which is the sharp boundary Phase 3's stress test recorded.
# Chosen by a rule fixed before any task score was consulted: the smallest of {1.5, 3.0, 6.0}
# leaving under 5 percent of agents more than 45 degrees wrong at every sampled time. 3.0 gives
# 15.5 percent at step 50; 6.0 gives at most 4.5. H14's adoption check ran at noise 0.01 only
# and never saw this; recorded as a finding in the H15 report.
WIND_CUE = 6.0
RING = dict(J=0.5, c=2.0, p=2.0, sigma=0.5, Rmax=2.0, width=1.2, tau=1.0, vgain=1.0)
MB = dict(K=200, C=4, sparsity=0.05, eta_d=0.10, eta_p=0.30, beta=0.15)


class World2:
    """Two sources, two channels, one wind. Cones as in Phase 7.3, geometry frozen by J1."""

    def __init__(self, runs, rng, p_hit=0.3, p_wind=1.0):
        self.R, self.rng, self.p_hit, self.p_wind = runs, rng, p_hit, p_wind
        x = rng.uniform(8.0, 14.0, runs)
        yA = rng.uniform(8.0, 14.0, runs)
        yB = yA + rng.uniform(14.0, 18.0, runs)
        self.src = np.stack([np.stack([x, yA], 1), np.stack([x, yB], 1)], 1)   # (R, 2, 2)
        self.good = rng.integers(0, 2, runs)
        # start inside the cone of one source at random, downwind of it, as 7.3 did
        k = rng.integers(0, 2, runs); rows = np.arange(runs)
        along = rng.uniform(5.0, 18.0, runs); halfw = W0 + SLOPE*along
        self.pos = np.stack([np.clip(self.src[rows, k, 0] + along, 0, ARENA),
                             np.clip(self.src[rows, k, 1] + rng.uniform(-1, 1, runs)*halfw,
                                     0, ARENA)], 1)
        self.head = rng.uniform(0, 360, runs)

    def sense(self):
        """(R, 2) boolean whiffs, one column per source. No gradient anywhere."""
        out = np.zeros((self.R, 2), bool)
        for k in (0, 1):
            d_along = self.pos[:, 0] - self.src[:, k, 0]
            d_cross = np.abs(self.pos[:, 1] - self.src[:, k, 1])
            cone = (d_along > 0) & (d_along < LMAX) & (d_cross < W0 + SLOPE*d_along)
            at_src = np.linalg.norm(self.pos - self.src[:, k], axis=1) < 3.0
            p = self.p_hit*np.exp(-np.maximum(d_along, 0.0)/LAM)
            out[:, k] = (cone | at_src) & (self.rng.random(self.R) < p)
        return out

    def wind_on(self): return self.rng.random(self.R) < self.p_wind

    def move(self, turn):
        self.head = (self.head + turn) % 360.0
        a = np.radians(self.head)
        p = self.pos + SPEED*np.stack([np.cos(a), np.sin(a)], 1)
        bumped = np.zeros(self.R, bool)
        for k, flip in ((0, 180.0), (1, 0.0)):
            out = (p[:, k] < 0) | (p[:, k] > ARENA)
            if out.any():
                p[out, k] = np.clip(2*np.clip(p[out, k], 0.0, ARENA) - p[out, k], 0.0, ARENA)
                self.head[out] = (flip - self.head[out]) % 360.0
                bumped |= out
        self.pos = p
        self.bumped = bumped

    def at_source(self):
        return np.linalg.norm(self.pos[:, None, :] - self.src, axis=2) < HIT_R     # (R, 2)


class Agent:
    """abl: any of 'norm', 'hold', 'head', 'learn', 'nav'. rule: 'agent' | 'random' | 'oracle'.
    known: (R, 2) valence supplied from the world for the J4 probe; implies no learning."""

    def __init__(self, runs, rng, abl=(), rule="agent", known=None):
        self.R, self.rng, self.abl, self.rule, self.known = runs, rng, set(abl), rule, known
        self.up = Upstream(n=1.5, sig=0.05, Rmax=1.8, k=0.8, runs=runs, chans=2)
        self.sel = Circuit(runs, n=2, theta=1.0, k=12.0, noise=0.01, rng=rng)
        self.ring = RingExact(runs, n=16, noise=0.3, rng=rng, **RING)
        self.mb = MB4(runs, parallel=False, gated=True, rng=rng, **MB)
        self.codes = np.stack([self.mb.odour(101), self.mb.odour(102)], 1)     # (R, 2, K)
        self.last_turn = np.zeros(runs); self.belief = np.zeros(runs)
        # Two timers, deliberately separate. `since` drives the cast and resets only on a whiff;
        # `silence` is the hold's timeout and resets when the hold is released. An earlier
        # version used one variable for both. The timeout returned it to zero every 40 steps,
        # so the cast offset could never pass 1.2*40 = 48 degrees about upwind, every reachable
        # target kept a negative x component, and an agent that overshot the sources was pinned
        # against the upwind wall for good. That is the trap Phase 7.3 removed by raising MAXOFF,
        # brought back through a shared counter. Measured: 67 percent of the exact-heading arm's
        # steps were spent within 0.7 of a wall, turning at the 40 degree limit.
        self.since = np.zeros(runs); self.silence = np.zeros(runs); self.prev = np.zeros(runs)
        self.flee_side = rng.choice([90.0, 270.0], runs)     # which crosswind exit an agent takes
        self.cast_sign = np.ones(runs)

    def bump(self, mask):
        """Wall reflex: on being reflected, turn the crosswind exit and the cast side around.

        Without it a constant crosswind target that points into a wall pins the agent there:
        the wall flips the heading, the controller flips it back, every step. Measured before
        this was added: the no-heading-memory arm, whose heading estimate is exact at p_wind 1,
        spent 67.4 percent of its steps within 0.7 of a wall turning at the 40 degree limit,
        and scored 0.0; the more precisely an arm steers, the more precisely it pins itself.
        """
        if mask.any():
            self.flee_side = np.where(mask, (self.flee_side + 180.0) % 360.0, self.flee_side)
            self.cast_sign = np.where(mask, -self.cast_sign, self.cast_sign)

    def held(self):
        on = self.sel.memory() > 1.0
        return np.where(on.sum(1) == 1, on.argmax(1), -1)

    def estimate(self, w, wind_on):
        if "head" in self.abl:
            self.belief = np.where(wind_on, w.head, self.belief)
            return self.belief
        self.ring.step(v=self.last_turn)
        if wind_on.any():
            self.ring.step(x=cue(self.R, 16, w.head, WIND_CUE, width=1.2)*wind_on[:, None])
        return self.ring.pos()

    def act(self, w, whiffs, wind_on):
        rows = np.arange(self.R)
        if self.rule == "random":
            turn = 18.0*self.rng.standard_normal(self.R); self.last_turn = turn
            return turn, np.full(self.R, -1)
        if self.rule == "oracle":
            d = w.src[rows, w.good] - w.pos
            tgt = np.degrees(np.arctan2(d[:, 1], d[:, 0])) % 360.0
            turn = np.clip(GAIN*angdiff(tgt, w.head), -MAXTURN, MAXTURN); self.last_turn = turn
            return turn, np.full(self.R, -1)

        x = whiffs.astype(float)
        y = x if "norm" in self.abl else self.up.step(x)
        # selection and hold, with Phase 5 Run 2's two release conditions
        if "hold" in self.abl:
            h = np.where(y.max(1) > 0.05, y.argmax(1), -1)
        else:
            hp = self.held(); committed = hp >= 0; hi = np.maximum(hp, 0); other = 1 - hi
            due = self.silence > RESET_AFTER
            due |= committed & ((y[rows, other] - y[rows, hi]) > MARGIN)
            rst = np.where(due, 10.0, 0.0)[:, None]
            self.silence = np.where(due, 0.0, self.silence)
            self.sel.step(y, reset=rst)
            h = self.held()
        est = self.estimate(w, wind_on)
        # valence of the held odour
        val = np.zeros(self.R)
        if self.known is not None:
            val = np.where(h >= 0, self.known[rows, np.maximum(h, 0)], 0.0)
        elif "learn" not in self.abl:
            for k in (0, 1):
                m = h == k
                if m.any(): val[m] = self.mb.valence(self.codes[:, k])[m]
        # a whiff on the held channel
        hit = np.where(h >= 0, whiffs[rows, np.maximum(h, 0)], False)
        self.since = np.where(hit, 0.0, self.since + 1.0)
        self.silence = np.where(hit, 0.0, self.silence + 1.0)
        # navigation
        if "nav" in self.abl:
            cur = hit.astype(float)                       # Phase 5's rule on the whiff signal
            turn = np.where(cur > self.prev, 0.0, 35.0) + TURN_NOISE*self.rng.standard_normal(self.R)
            self.prev = cur
        else:
            side = np.where((self.since // CAST_PERIOD) % 2 == 0, 1.0, -1.0)*self.cast_sign
            off = np.minimum(MAXOFF, CAST_GROW*self.since)
            tgt = np.where(hit, UPWIND, (UPWIND + side*off) % 360.0)
            tgt = np.where(val < 0, self.flee_side, tgt)   # avoid: leave the plume crosswind
            turn = np.clip(GAIN*angdiff(tgt, est), -MAXTURN, MAXTURN)
            turn = turn + TURN_NOISE*self.rng.standard_normal(self.R)
        self.last_turn = turn
        return turn, h


def episode(w, a, steps=STEPS, train=True):
    score = np.zeros(a.R); rows = np.arange(a.R)
    for _ in range(steps):
        turn, h = a.act(w, w.sense(), w.wind_on())
        w.move(turn)
        a.bump(w.bumped)
        hit = w.at_source()
        for k in (0, 1):
            arrived = hit[:, k]
            if not arrived.any(): continue
            rewarding = w.good == k
            score += arrived*np.where(rewarding, 1.0, -1.0)
            if train and a.rule == "agent" and a.known is None and "learn" not in a.abl:
                comp = np.where(rewarding, 1, 0)
                code = a.codes[:, k]*arrived[:, None]
                rv = np.zeros((a.R, 4)); rv[rows, comp] = arrived*1.0
                a.mb.step(code=code, reinf=rv)
    return score


def run(abl=(), rule="agent", known=False, p_hit=0.3, seed_w=0, seed_a=1):
    w = World2(R, np.random.default_rng(seed_w), p_hit=p_hit)
    kv = None
    if known:
        rows = np.arange(R)
        kv = np.full((R, 2), -1.0); kv[rows, w.good] = 1.0
    a = Agent(R, np.random.default_rng(seed_a), abl=abl, rule=rule, known=kv)
    s = np.array([episode(w, a) for _ in range(EPISODES)])
    return s, w, a


def last(s): return s[-3:].mean(0) if EPISODES >= 3 else s.mean(0)


def learned(a, w):
    v0 = a.mb.valence(a.codes[:, 0]); v1 = a.mb.valence(a.codes[:, 1])
    good = np.where(w.good == 0, v0, v1); bad = np.where(w.good == 0, v1, v0)
    return good, bad


# ---------------------------------------------------------------- J1
def calibrate():
    print("\n== J1 calibration: two fixed probes, before any agent is compared ==")
    lo = last(run(rule="random")[0]); hi = last(run(rule="oracle")[0])
    mlo, mhi = float(np.median(lo)), float(np.median(hi))
    # J1 as STORED has two halves: the oracle must clear the floor by 10, and no AGENT ARM may
    # reach 99 percent of the ceiling. The second half is checked where the arms are run, in
    # table(). An earlier version of this function applied it to the oracle instead, which is
    # backwards: the oracle is the probe that DEFINES the ceiling, and because the world
    # persists across episodes it is already sitting on the rewarding source when the last
    # third begins, so it scores exactly 600 there. That version stopped the first full run
    # after the two probes and before any agent; nothing had been compared.
    ok = (mhi - mlo) >= 10.0
    print(f"   floor probe (random walk)   median {mlo:7.1f}")
    print(f"   ceiling probe (oracle)      median {mhi:7.1f}   arithmetic ceiling {STEPS}")
    print(f"   -> {'READABLE' if ok else 'NOT readable'} (oracle clears the floor by"
          f" {mhi - mlo:.1f}); agent-arm saturation is checked in the table."
          f" World geometry frozen here.")
    return ok


# ---------------------------------------------------------------- the table
ARMS = [("intact", (), True), ("no normalisation", ("norm",), True),
        ("no select-and-hold", ("hold",), True), ("no learned valence", ("learn",), True),
        ("no surge-and-cast", ("nav",), True), ("no heading memory", ("head",), False)]


def table():
    print(f"\n== H15, {R} agents, {EPISODES} episodes of {STEPS} steps, p_hit 0.3 ==")
    res = {}
    for name, abl, _ in ARMS:
        s, w, a = run(abl); res[name] = (s, w, a)
        L = last(s)
        print(f"   {name:22s} median {np.median(L):7.1f}"
              f"   first third {np.median(s[:3].mean(0)):7.1f} -> last {np.median(L):7.1f}"
              f"   | mean {L.mean():7.1f}  >10: {float((L > 10).mean())*100:4.0f}%"
              f"  <-10: {float((L < -10).mean())*100:4.0f}%")
    sk, _, _ = run(known=True); res["known valence (J4)"] = (sk, None, None)
    Lk = last(sk)
    print(f"   {'known valence (J4)':22s} median {np.median(Lk):7.1f}   <- navigation ceiling"
          f"            | mean {Lk.mean():7.1f}  >10: {float((Lk > 10).mean())*100:4.0f}%"
          f"  <-10: {float((Lk < -10).mean())*100:4.0f}%")
    print("   (mean and the two tail fractions are REPORTED only; J3 is judged on medians as stored."
          " The score distribution is strongly skewed, so the median alone hides its shape.)")
    sat = [n for n, (s, _, _) in res.items() if float(np.median(last(s))) >= 0.99*STEPS]
    if sat: print(f"   CEILING: {sat}. Under J1 this table is not read.")

    print("\n   J3 matched pairs against the intact agent (same worlds, same seeds):")
    base = last(res["intact"][0]); passed = 0; gated = 0
    for name, _, is_gated in ARMS[1:]:
        other = last(res[name][0])
        win = float((base > other).mean())
        mi, mo = float(np.median(base)), float(np.median(other))
        gap = (mi - mo)/abs(mi) if mi else float("nan")
        if name == "no surge-and-cast":
            ok = win >= 0.60; how = "pairs only, baseline expected near zero"
        else:
            ok = gap >= 0.25 and win >= 0.60; how = ""
        tag = "gated" if is_gated else "reported"
        if is_gated: gated += 1; passed += ok
        print(f"     vs {name:22s} {mi:7.1f} vs {mo:7.1f}  wins {win*100:5.1f}%"
              f"  gap {gap*100:+8.1f}%  -> {'YES' if ok else 'no'}  [{tag}] {how}")
    print(f"   J3: intact beats {passed} of {gated} gated ablations"
          f" -> {'GATE MET' if passed == gated else 'gate NOT met'}")

    print("\n   J2 two-sided learning, intact agent, end of run:")
    _, w, a = res["intact"]
    good, bad = learned(a, w)
    mg, mb = float(np.median(good)), float(np.median(bad))
    ok2 = mg >= 0.05 and mb <= -0.05
    print(f"     rewarding odour  median {mg:+.3f}  mean {good.mean():+.3f}"
          f"  positive in {int((good > 0.05).sum())}/{R}")
    print(f"     punishing odour  median {mb:+.3f}  mean {bad.mean():+.3f}"
          f"  negative in {int((bad < -0.05).sum())}/{R}")
    print(f"     -> J2 {'pass' if ok2 else 'FAIL'}")

    mk = float(np.median(last(sk))); mi = float(np.median(base))
    print(f"\n   J4: intact {mi:.1f} is {mi/mk*100 if mk else 0:.0f}% of the known-valence probe {mk:.1f}")
    return passed == gated, ok2


def demo():
    w = World2(100, np.random.default_rng(0))
    sep = np.abs(w.src[:, 0, 1] - w.src[:, 1, 1])
    assert sep.min() >= 14.0, "sources too close"
    s = w.sense(); assert s.dtype == bool and s.shape == (100, 2)
    a = Agent(100, np.random.default_rng(1))
    for _ in range(30): w.move(a.act(w, w.sense(), w.wind_on())[0])
    rows = np.arange(100); kv = np.full((100, 2), -1.0); kv[rows, w.good] = 1.0
    b = Agent(100, np.random.default_rng(1), known=kv)
    for _ in range(30): b.act(w, w.sense(), w.wind_on())
    assert b.mb.w.min() == 1.0 and b.mb.w.max() == 1.0, "known-valence probe must not learn"
    print("ok  two separated cones, boolean whiffs, agent steps, known-valence probe does not learn")
    print(f"ok  ring is RingExact tau {a.ring.tau} sigma {a.ring.sigma}; learning gated={a.mb.gated}"
          f" parallel={a.mb.parallel}")


if __name__ == "__main__":
    what = [x for x in sys.argv[1:] if x in ("demo", "calib", "all")] or ["all"]
    if "demo" in what: demo(); sys.exit(0)
    print(f"== H15. Criteria: record:h15-success-criteria, stored before this file existed ==")
    ok = calibrate()
    if "calib" in what: sys.exit(0)
    if not ok: print("   world not readable, no verdict drawn"); sys.exit(0)
    j3, j2 = table()
    print(f"\n== H15 verdict ==  J2 {'pass' if j2 else 'FAIL'}   J3 {'pass' if j3 else 'FAIL'}"
          f"   -> {'SUPPORTED' if (j2 and j3) else 'not supported'}")
