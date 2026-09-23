#!/usr/bin/env python3
"""H19 (a): while no odour is held, a whiff actually sensed resets the cast clock.

Usage: python ph14.py demo | dev | eval

The diagnosis (ph13b) found that a whiff reaches navigation only if its odour is the one
currently held; about 11 percent of whiffs are dropped and 7-10 percent of agents receive odour
and never act on it again. The owner opened option (a) alone, with boundaries: identity and
learned valence untouched; the reset never overrides avoidance of a negative valence; whiffs
arriving while ANOTHER odour is held stay excluded. It addresses the blackout after the hold is
lost, not the stretch where A is held and B is ignored.

Agent3 is ph13.Agent2 with one signal changed. Opened by decision:h19-open-option-a. Criteria
N1-N6, the distractor definition and the seeds: record:h19-success-criteria, stored before this
file existed. Seeds 1620/1720 and 9600/9700 are development seeds; 1630/1730 and 1631/1731 give
the verdict and are run once.
"""
import sys
import numpy as np
from ph9 import UPWIND, CAST_PERIOD, CAST_GROW, MAXOFF, GAIN, MAXTURN, TURN_NOISE, STEPS, angdiff, compare
from ph11 import RESET_AFTER, MARGIN
from ph12 import SAT, Nav2, med
from ph13 import World4, Agent2, R, BLOCKS

T = BLOCKS*STEPS
P_DISTRACT = 0.03
SEEDS = dict(dev=((9600, 9700), (9601, 9701)), eval=((1630, 1730), (1631, 1731)))


class World5(World4):
    """World4 plus an optional background of the PUNISHING odour, anywhere, p_d per step."""

    def __init__(self, runs, rng, p_d=0.0):
        super().__init__(runs, rng); self.p_d = p_d

    def sense(self):
        whiffs = super().sense()
        self.plume = whiffs.any(1)             # from a plume, before any background is added
        if self.p_d:
            bg = self.rng.random(self.R) < self.p_d
            whiffs[bg, 1 - self.good[bg]] = True
        return whiffs


class Agent3(Agent2):
    """fix=False must BE ph13.Agent2 (checked in demo). fix=True changes one signal: what is
    handed to navigation. `nav_hit` exposes that signal for measurement."""

    def __init__(self, runs, rng, fix=True, **kw):
        super().__init__(runs, rng, **kw); self.fix, self.nav_hit = fix, np.zeros(runs, bool)

    def chan_valence(self):
        if self.known is not None: return self.known
        if "learn" in self.abl: return np.zeros((self.R, 2))
        return np.stack([self.mb.valence(self.codes[:, 0]), self.mb.valence(self.codes[:, 1])], 1)

    def act(self, w, whiffs, wind_on):
        if self.rule != "agent": return super().act(w, whiffs, wind_on)
        rows = np.arange(self.R)
        x = whiffs.astype(float)
        y = x if "norm" in self.abl else self.up.step(x)
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
        est = self.est = self.estimate(w, wind_on)
        val = np.zeros(self.R)
        if self.known is not None:
            val = np.where(h >= 0, self.known[rows, np.maximum(h, 0)], 0.0)
        elif "learn" not in self.abl:
            for k in (0, 1):
                m = h == k
                if m.any(): val[m] = self.mb.valence(self.codes[:, k])[m]
        hit = np.where(h >= 0, whiffs[rows, np.maximum(h, 0)], False)
        nav = hit
        if self.fix:        # H19 (a): nothing held, and the odour sensed is not one to be avoided
            nav = hit | ((h < 0) & (whiffs & (self.chan_valence() >= 0)).any(1))
        self.nav_hit = nav
        self.since = np.where(nav, 0.0, self.since + 1.0)          # the cast clock
        self.silence = np.where(hit, 0.0, self.silence + 1.0)      # the hold's own clock: unchanged
        side = np.where((self.since // CAST_PERIOD) % 2 == 0, 1.0, -1.0)*self.cast_sign
        if self.cast == "return":
            off = MAXOFF*(1.0 - np.abs((self.since/SAT) % 2.0 - 1.0))
        else:
            off = np.minimum(MAXOFF, CAST_GROW*self.since)
        tgt = np.where(nav, UPWIND, (UPWIND + side*off) % 360.0)
        tgt = np.where(val < 0, self.flee_side, tgt)
        turn = np.clip(GAIN*angdiff(tgt, est), -MAXTURN, MAXTURN)
        turn = turn + TURN_NOISE*self.rng.standard_normal(self.R)
        self.last_turn = turn
        return turn, h


def run(arm, cond, seeds, runs=R, steps=T):
    w = World5(runs, np.random.default_rng(seeds[0]), p_d=P_DISTRACT if cond == "distractor" else 0.0)
    rows = np.arange(runs); kv = None
    if cond != "neutral":
        kv = np.full((runs, 2), -1.0); kv[rows, w.good] = 1.0
    if arm == "bare":
        a = Nav2(runs, np.random.default_rng(seeds[1]), "return", "exact")
    else:
        abl = (() if kv is not None else ("learn",)) + (("hold",) if arm == "no-hold" else ())
        a = Agent3(runs, np.random.default_rng(seeds[1]), fix=arm == "fix", abl=abl, known=kv)
    b = lambda: np.zeros((steps, runs), bool)
    o = dict(W=np.zeros((steps, runs, 2), bool), H=np.full((steps, runs), -1, np.int8), NAV=b(), G=b(), B=b(),
             C=b(), P=b(), good=w.good.copy(), start_good=w.start == w.good)
    for t in range(steps):
        whiffs = w.sense(); o["P"][t] = w.plume
        if arm == "bare":
            nav = whiffs.any(1); turn = a.act(w, nav, w.wind_on()); h = np.full(runs, -1)
        else:
            turn, h = a.act(w, whiffs, w.wind_on()); nav = a.nav_hit
        w.move(turn); a.bump(w.bumped)
        at = w.at_source()
        o["W"][t] = whiffs; o["H"][t] = h; o["NAV"][t] = nav; o["C"][t] = w.bumped
        o["G"][t] = at[rows, w.good]; o["B"][t] = at[rows, 1 - w.good]
    return o


def late(x): return x[-3*STEPS:].sum(0)/3.0
def unrec(o):
    # record:h19-amendment-before-evaluation: plume whiffs only. Counting the distractor's background
    # whiffs made every agent 'recovered' by construction.
    return ~o["P"][-3*STEPS:].any(0)


def holds(o):
    """share of steps with nothing held; after each loss of the hold, steps to the next hold"""
    H = o["H"]; again, never = [], 0
    for r in range(H.shape[1]):
        col = H[:, r]
        for t in np.flatnonzero((col[:-1] >= 0) & (col[1:] == -1)) + 1:
            nxt = np.flatnonzero(col[t:] >= 0)
            if len(nxt): again.append(int(nxt[0]))
            else: never += 1
    k = len(again) + never
    return float((H == -1).mean()), (med(again) if again else float("nan")), (never/k if k else float("nan")), k


def handed(o):
    """N3: what reaches navigation, by the state it arrives in"""
    W, H, NAV = o["W"], o["H"], o["NAV"]; good = o["good"][None, :]
    wg = np.where(good == 0, W[:, :, 0], W[:, :, 1]); wb = np.where(good == 0, W[:, :, 1], W[:, :, 0])
    none = H == -1
    held_w = np.where(H == 0, W[:, :, 0], np.where(H == 1, W[:, :, 1], False))
    other_only = (H >= 0) & W.any(2) & ~held_w
    f = lambda m: float(NAV[m].mean())*100 if m.any() else float("nan")
    return dict(none_any=f(none & W.any(2)), none_good_only=f(none & wg & ~wb), none_bad_only=f(none & wb & ~wg),
                other_held=f(other_only), n_none=int((none & W.any(2)).sum()))


def describe(name, o, known):
    u = unrec(o); sg = o["start_good"]; g, b = late(o["G"]), late(o["B"])
    vg, vb = o["G"].any(0), o["B"].any(0)
    nh, again, never, k = holds(o) if name != "bare" else (float("nan"),)*3 + (0,)
    hd = handed(o)
    print(f"   {name:8s} late unrecovered {u.mean()*100:5.1f}% ({int(u.sum())}/{len(u)};"
          f" start rewarding {int(u[sg].sum())}/{int(sg.sum())}, start punishing {int(u[~sg].sum())}/{int((~sg).sum())})"
          f" | dwell last third: rewarding {med(g):5.1f} punishing {med(b):5.1f} total {med(g + b):5.1f}"
          f" | visited rewarding {vg.mean()*100:5.1f}% punishing {vb.mean()*100:5.1f}% both {(vg & vb).mean()*100:5.1f}%"
          f" | contacts/agent {o['C'].sum(0).mean():5.1f}")
    print(f"            nothing held on {nh*100:5.1f}% of steps; losses of the hold {k}, held again after median {again:5.0f} steps,"
          f" never again {never*100:5.1f}% | handed to navigation: nothing held {hd['none_any']:5.1f}% of {hd['n_none']} whiffs"
          + (f" (rewarded odour {hd['none_good_only']:5.1f}%, punished odour {hd['none_bad_only']:5.1f}%)" if known else "")
          + f", other odour held {hd['other_held']:5.1f}%")
    if known:
        p = ~sg
        print(f"            start in the punishing plume: punishing dwell median {med(b[p]):5.1f},"
              f" reached the rewarding source {vg[p].mean()*100:5.1f}%, rewarding dwell median {med(g[p]):5.1f}")
    return dict(u=u, g=g, b=b, vg=vg, hd=hd, never=never, sg=sg)


def main(mode):
    (s_main, s_dis) = SEEDS[mode]; res = {}
    for cond, seeds in (("neutral", s_main), ("known", s_main), ("distractor", s_dis)):
        print(f"\n== {cond}{' (known valence + background whiffs of the punished odour, p 0.03)' if cond == 'distractor' else ''}."
              f" world seed {seeds[0]}, agent seed {seeds[1]} ==")
        arms = (["bare"] if cond == "neutral" else []) + ["full", "fix", "no-hold"]
        res[cond] = {a: describe(a, run(a, cond, seeds), cond != "neutral") for a in arms}
    n, k, d = res["neutral"], res["known"], res["distractor"]
    ub = n["bare"]["u"].mean()
    n1 = [n["fix"]["u"].mean() <= ub + 0.02] + [n["fix"]["u"][m].mean() <= ub + 0.04 for m in (n["fix"]["sg"], ~n["fix"]["sg"])]
    n2 = [c["fix"]["u"].mean() <= 0.5*c["full"]["u"].mean() for c in (n, k)]
    n3 = [n["fix"]["hd"]["none_any"] >= 99, k["fix"]["hd"]["none_good_only"] >= 99,
          n["fix"]["hd"]["other_held"] == 0, k["fix"]["hd"]["other_held"] == 0, k["fix"]["hd"]["none_bad_only"] == 0]
    p = ~k["fix"]["sg"]
    n4 = [med(k["fix"]["b"][p]) <= 1.0, k["fix"]["vg"][p].mean() >= k["full"]["vg"][p].mean() - 0.05]
    n5 = [med(n["fix"]["g"] + n["fix"]["b"]) >= 0.9*med(n["full"]["g"] + n["full"]["b"]),
          med(k["fix"]["g"]) >= 0.9*med(k["full"]["g"])]
    print("\n== criteria ==")
    print(f"   N1 recovery, neutral: fix {n['fix']['u'].mean()*100:.1f}% vs bare {ub*100:.1f}% + 2.0 (all), + 4.0 (each start group): {n1}")
    print(f"   N2 at most half of full's: neutral {n['fix']['u'].mean()*100:.1f} vs {n['full']['u'].mean()*100:.1f}, known"
          f" {k['fix']['u'].mean()*100:.1f} vs {k['full']['u'].mean()*100:.1f}: {n2}")
    print(f"   N3 mechanism and boundary (>=99 handed when nothing held: neutral, known rewarded odour; 0 handed: other held"
          f" neutral, other held known, punished odour with nothing held): {n3}")
    print(f"   N4 avoidance kept, punishing-plume start: punishing dwell {med(k['fix']['b'][p]):.1f} <= 1.0; reached rewarding"
          f" {k['fix']['vg'][p].mean()*100:.1f}% vs full {k['full']['vg'][p].mean()*100:.1f}% - 5: {n4}")
    print(f"   N5 no harm: neutral total dwell {med(n['fix']['g'] + n['fix']['b']):.1f} vs {med(n['full']['g'] + n['full']['b']):.1f};"
          f" known rewarding dwell {med(k['fix']['g']):.1f} vs {med(k['full']['g']):.1f}: {n5}")
    label = n["fix"]["never"] >= n["full"]["never"]
    print(f"   separate reading: losses never followed by a hold, neutral: fix {n['fix']['never']*100:.1f}% vs full"
          f" {n['full']['never']*100:.1f}% -> {'cast clock normalised, identity selection NOT recovered' if label else 'selection recovers as well'}")
    print("   reported, known condition (the second plume as a distractor of a kind), rewarding dwell last third:")
    compare(k["full"]["g"], k["no-hold"]["g"], "full vs no-hold")
    compare(k["fix"]["g"], k["no-hold"]["g"], "fix vs no-hold")
    floored = all(med(d[a]["g"]) < 10 for a in d)
    print(f"   N6 distractor, rewarding dwell last third (reported){': EVERY ARM AT THE FLOOR, NOT READ' if floored else ''}:")
    e1 = compare(d["full"]["g"], d["no-hold"]["g"], "full vs no-hold")[0]
    e2 = compare(d["fix"]["g"], d["no-hold"]["g"], "fix vs no-hold")[0]
    print(f"      late unrecovered: full {d['full']['u'].mean()*100:.1f}%  fix {d['fix']['u'].mean()*100:.1f}%  no-hold"
          f" {d['no-hold']['u'].mean()*100:.1f}%  -> "
          + ("not read: the condition is floored" if floored else
             f"the hold {'EARNS its place here' if e1 or e2 else 'does NOT earn its place here'}"))
    ok = all(n1) and all(n2) and all(n3) and all(n4) and all(n5)
    print(f"\n== H19 (a) ==  N1 {'pass' if all(n1) else 'FAIL'}  N2 {'pass' if all(n2) else 'FAIL'}  N3 {'pass' if all(n3) else 'FAIL'}"
          f"  N4 {'pass' if all(n4) else 'FAIL'}  N5 {'pass' if all(n5) else 'FAIL'}  -> {'SUPPORTED' if ok else 'not supported'}")


def demo():
    for known in (False, True):
        w1, w2 = World4(40, np.random.default_rng(3)), World5(40, np.random.default_rng(3))
        kv = None
        if known: kv = np.full((40, 2), -1.0); kv[np.arange(40), w1.good] = 1.0
        abl = () if known else ("learn",)
        a1 = Agent2(40, np.random.default_rng(4), abl=abl, known=kv)
        a2 = Agent3(40, np.random.default_rng(4), fix=False, abl=abl, known=kv)
        for _ in range(400):
            t1, _ = a1.act(w1, w1.sense(), w1.wind_on()); w1.move(t1); a1.bump(w1.bumped)
            t2, _ = a2.act(w2, w2.sense(), w2.wind_on()); w2.move(t2); a2.bump(w2.bumped)
        assert np.allclose(w1.pos, w2.pos), "Agent3 with the change off is not Agent2"
    o = run("fix", "distractor", (5, 6), runs=60, steps=600)
    assert (o["NAV"] <= o["W"].any(2)).all(), "navigation was handed a hit with no whiff"
    hd = handed(o); assert hd["other_held"] == 0 and hd["none_bad_only"] == 0, "a boundary is broken"
    print("ok  with the change off Agent3 reproduces ph13.Agent2 over 400 steps, neutral and known")
    print("ok  boundaries hold: nothing handed on without a whiff, while the other odour is held, or for the punished odour")


if __name__ == "__main__":
    mode = ([m for m in sys.argv[1:] if m in ("demo", "dev", "eval")] or ["demo"])[0]
    if mode == "demo": demo(); sys.exit(0)
    print(f"== H19 (a), {mode.upper()}. {R} agents, {T} steps, two-source world ==")
    print("== Criteria: record:h19-success-criteria, stored before this file existed ==")
    main(mode)
