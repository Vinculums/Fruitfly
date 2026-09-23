#!/usr/bin/env python3
"""H16: can surge-and-cast recover from the lost state, and keep reaching the source late?

Usage: python ph12.py demo | dev | eval

H15 Run 1 could not judge the integrated agent because navigation failed first. The 7.3 rule
grows its cast offset 1.2 degrees per whiff-free step and saturates at 170, so after about 142
silent steps the target heading is downwind for good; only a whiff resets the clock. In H15's
geometry every cone ends short of the downwind wall, the wall has no odour, and 92 percent of
agents were absorbed there within the first 600 steps.

This file tests the navigation rule alone: one source, no odour identity, no learning, no
selection. Stage A supplies the TRUE heading, so the rule is isolated from heading memory.
Stage B then connects the ring exactly as adopted in H14 and used in H15, changing nothing.

Criteria: record:h16-success-criteria (K1-K6), stored before this file existed. Opened by
decision:h16-open. `dev` uses development seeds and exists to find operation errors; `eval`
uses the evaluation seeds and is run once. A change after the eval table is a new Run.
"""
import sys
import numpy as np
from ph9 import (WindWorld, Nav, angdiff, compare, ARENA, SPEED, STEPS, UPWIND, W0, SLOPE, LMAX,
                 CAST_PERIOD, CAST_GROW, MAXOFF, GAIN, MAXTURN, TURN_NOISE)
from ph10 import RingExact
from ph3 import cue
from ph11 import World2, RING, WIND_CUE

R, BLOCKS = 200, 9
SAT = MAXOFF/CAST_GROW       # 141.7 steps: where the control's cast saturates
LOST = 142                   # whiff-free steps after which an agent counts as lost (H15's measure)
SEEDS = dict(dev=(9000, 9100), eval=(1600, 1700))
CONDS = [("W-cone", "cone", True), ("W-lost", "lost", True),
         ("O-cone", "cone", False), ("O-lost", "lost", False)]
RULES = ["control", "wall", "return", "both"]
ARMS = ["random", "oracle"] + RULES


class World1(WindWorld):
    """One source in H15's geometry: x in [8, 14], so every cone ends at x 33 to 39, short of
    the downwind wall at 40. 7.3's own world put sources up to x 32, whose cones reach the wall
    and hand a pinned agent whiffs; that world does not contain the problem being tested."""

    def __init__(self, runs, rng, start="cone", walls=True, wind="always"):
        self.R, self.rng, self.p_hit, self.mode = runs, rng, 0.3, "plume"
        self.walls, self.wind, self.t = walls, wind, 0
        self.src = np.stack([rng.uniform(8.0, 14.0, runs), rng.uniform(8.0, 32.0, runs)], 1)
        along = rng.uniform(5.0, 18.0, runs); halfw = W0 + SLOPE*along
        self.pos = np.stack([self.src[:, 0] + along,
                             self.src[:, 1] + rng.uniform(-1, 1, runs)*halfw], 1)
        if start == "lost":
            self.pos = rng.uniform(0, ARENA, (runs, 2))
            while (bad := self.in_odour()).any():
                self.pos[bad] = rng.uniform(0, ARENA, (int(bad.sum()), 2))
        self.head = rng.uniform(0, 360, runs)
        self.phase = rng.integers(0, 100, runs)
        self.bumped = np.zeros(runs, bool)

    def in_odour(self):
        da = self.pos[:, 0] - self.src[:, 0]; dc = np.abs(self.pos[:, 1] - self.src[:, 1])
        return ((da > 0) & (da < LMAX) & (dc < W0 + SLOPE*da)) | \
               (np.linalg.norm(self.pos - self.src, axis=1) < 3.0)

    def wind_on(self):
        if self.wind == "always": return np.ones(self.R, bool)
        return (self.t + self.phase) % 100 >= 50          # blocks: 50 steps off, 50 on

    def move(self, turn):
        self.t += 1
        if self.walls: return World2.move(self, turn)     # H15's walls and `bumped`, verbatim
        self.head = (self.head + turn) % 360.0
        a = np.radians(self.head)
        self.pos = self.pos + SPEED*np.stack([np.cos(a), np.sin(a)], 1)


class Nav2:
    """rule: 'control' | 'wall' | 'return' | 'both' | 'random' | 'oracle' ('wall0': dev only).
    head: 'exact' | 'ring' | 'none' | 'integrate'.

    `clock` drives the cast and `since` only measures silence. They differ in the wall rules,
    where a contact may restart the search without the agent having smelled anything."""

    def __init__(self, runs, rng, rule="control", head="exact"):
        self.R, self.rng, self.rule, self.head = runs, rng, rule, head
        self.ring = RingExact(runs, n=16, noise=0.3, rng=rng, **RING) if head == "ring" else None
        self.clock = np.zeros(runs); self.since = np.zeros(runs); self.cast_sign = np.ones(runs)
        self.last_turn = np.zeros(runs); self.belief = np.zeros(runs); self.est = np.zeros(runs)

    def bump(self, mask):
        if not mask.any(): return
        self.cast_sign = np.where(mask, -self.cast_sign, self.cast_sign)   # H15's reflex, every arm
        if self.rule in ("wall", "both"):
            # only while lost. Unconditionally ('wall0') the upwind wall becomes a pin: restart
            # from upwind steers back into the wall, which restarts the search again.
            self.clock = np.where(mask & (self.clock >= SAT), 0.0, self.clock)
        elif self.rule == "wall0":
            self.clock = np.where(mask, 0.0, self.clock)

    def offset(self):
        if self.rule in ("return", "both"):                # triangle wave: 0 -> 170 -> 0 -> ...
            return MAXOFF*(1.0 - np.abs((self.clock/SAT) % 2.0 - 1.0))
        return np.minimum(MAXOFF, CAST_GROW*self.clock)

    def estimate(self, w, wind_on):
        if self.head == "exact": return w.head
        if self.head == "ring":                            # as ph11.Agent.estimate
            self.ring.step(v=self.last_turn)
            if wind_on.any():
                self.ring.step(x=cue(self.R, 16, w.head, WIND_CUE, width=1.2)*wind_on[:, None])
            return self.ring.pos()
        if self.head == "integrate": self.belief = (self.belief + self.last_turn) % 360.0
        self.belief = np.where(wind_on, w.head, self.belief)
        return self.belief

    def act(self, w, hit, wind_on):
        self.since = np.where(hit, 0.0, self.since + 1.0)
        self.clock = np.where(hit, 0.0, self.clock + 1.0)
        if self.rule == "random":
            turn = 18.0*self.rng.standard_normal(self.R)
        elif self.rule == "oracle":
            d = w.src - w.pos
            tgt = np.degrees(np.arctan2(d[:, 1], d[:, 0])) % 360.0
            turn = np.clip(GAIN*angdiff(tgt, w.head), -MAXTURN, MAXTURN)
        else:
            self.est = self.estimate(w, wind_on)
            side = np.where((self.clock // CAST_PERIOD) % 2 == 0, 1.0, -1.0)*self.cast_sign
            tgt = np.where(hit, UPWIND, (UPWIND + side*self.offset()) % 360.0)
            turn = np.clip(GAIN*angdiff(tgt, self.est), -MAXTURN, MAXTURN)
            turn = turn + TURN_NOISE*self.rng.standard_normal(self.R)
        self.last_turn = turn
        return turn


def run(rule, head="exact", start="cone", walls=True, wind="always", seeds=(0, 1), runs=None):
    n = runs or R
    w = World1(n, np.random.default_rng(seeds[0]), start, walls, wind)
    a = Nav2(n, np.random.default_rng(seeds[1]), rule, head)
    o = dict(score=np.zeros((BLOCKS, n)), whiff=np.zeros((BLOCKS, n)), wall=np.zeros((BLOCKS, n)),
             events=0, gaps=[], wallfree=[], err=np.zeros(2), err_off=np.zeros(2))
    touched = np.zeros(n, bool)                # any wall contact since the last whiff
    for t in range(BLOCKS*STEPS):
        b = t // STEPS
        hit = w.sense(); won = w.wind_on()
        back = hit & (a.since > LOST)          # a lost agent has just reacquired the plume
        if back.any():
            o["gaps"].append(a.since[back].copy()); o["wallfree"].append(~touched[back])
        touched &= ~hit
        turn = a.act(w, hit, won)
        o["events"] += int((a.since == LOST + 1).sum())
        if head != "exact":
            bad = np.abs(angdiff(a.est, w.head)) > 45.0
            o["err"] += (bad.sum(), n); o["err_off"] += (bad[~won].sum(), (~won).sum())
        w.move(turn); a.bump(w.bumped); touched |= w.bumped
        o["score"][b] += w.at_source(); o["whiff"][b] += hit
        if walls: o["wall"][b] += np.minimum(w.pos, ARENA - w.pos).min(1) < 1.0
    o["lost_end"] = a.since > LOST
    o["end_pos"] = w.pos.copy()
    o["gaps"] = np.concatenate(o["gaps"]) if o["gaps"] else np.zeros(0)
    o["wallfree"] = np.concatenate(o["wallfree"]) if o["wallfree"] else np.zeros(0, bool)
    return o


def last(o): return o["score"][-3:].mean(0)
def first(o): return o["score"][:3].mean(0)
def absorbed(o): return float((o["whiff"][-3:].sum(0) == 0).mean())
def reached(o): return float((o["score"].sum(0) > 0).mean())
def med(x): return float(np.median(x))


def describe(name, o, floor, walls):
    L, F = last(o), first(o)
    q = np.percentile(L, [10, 25, 50, 75, 90])
    print(f"   {name:8s} last third: median {q[2]:6.1f} mean {L.mean():6.1f}"
          f"  p10/25/75/90 {q[0]:5.1f} {q[1]:5.1f} {q[3]:5.1f} {q[4]:5.1f}"
          f"  >floor+10: {float((L > floor + 10).mean())*100:5.1f}%"
          f" | first third median {med(F):6.1f} | absorbed {absorbed(o)*100:5.1f}%"
          f"  lost at end {float(o['lost_end'].mean())*100:5.1f}%  reached ever {reached(o)*100:5.1f}%")
    if name in ("random", "oracle"): return
    fmt = lambda v: " ".join(f"{x:5.1f}" for x in v)
    print(f"            per block  median score {fmt(np.median(o['score'], 1))}")
    print(f"                       mean score   {fmt(o['score'].mean(1))}")
    print(f"                       % scoring    {fmt((o['score'] > 0).mean(1)*100)}")
    print(f"                       % with whiff {fmt((o['whiff'] > 0).mean(1)*100)}")
    if walls:
        print(f"                       % near wall  {fmt(o['wall'].mean(1)/STEPS*100)}")
    g = o["gaps"]; ev = o["events"]
    rec = f"{len(g)/ev*100:5.1f}%" if ev else "  n/a"
    tim = f"median {med(g):6.0f}  p90 {np.percentile(g, 90):6.0f}" if len(g) else "none"
    wf = f"{float(o['wallfree'].mean())*100:5.1f}%" if len(g) else "  n/a"
    print(f"            recovery   lost events {ev:5d}  recovered {rec}  reacquisition {tim}"
          f"  without wall contact {wf}")


def stage_a(mode):
    sw, sa = SEEDS[mode]; res = {}
    for c, (cname, start, walls) in enumerate(CONDS):
        print(f"\n== {cname}: {'walled' if walls else 'NO walls'}, {start} start."
              f" world seed {sw + c}, agent seed {sa + c} ==")
        res[cname] = {arm: run(arm, start=start, walls=walls, seeds=(sw + c, sa + c)) for arm in ARMS}
        floor = med(last(res[cname]["random"]))
        for arm in ARMS: describe(arm, res[cname][arm], floor, walls)
    return res


def verdict_a(res):
    wc, wl, oc = res["W-cone"], res["W-lost"], res["O-cone"]
    fl = {k: med(last(v["random"])) for k, v in res.items()}
    print("\n== K1 validity, W-cone, last third ==")
    k1a = med(last(wc["oracle"])) - fl["W-cone"] >= 10
    k1b = all(med(last(wc[a])) < 0.99*STEPS for a in RULES)
    k1c = absorbed(wc["control"]) >= 0.5
    clear = [a for a in RULES[1:] if med(last(wc[a])) >= fl["W-cone"] + 10]
    print(f"   (a) oracle {med(last(wc['oracle'])):.1f} - random {fl['W-cone']:.1f} >= 10: {k1a}")
    print(f"   (b) no rule arm at 99 percent of {STEPS}: {k1b}")
    print(f"   (c) control absorbed {absorbed(wc['control'])*100:.1f}% >= 50%: {k1c}")
    print(f"   (d) candidates clearing random + 10: {clear or 'NONE, table is floored'}")
    k1 = k1a and k1b and k1c
    if not k1c: print("   -> world is NOT H15-comparable. No verdict is drawn.")
    passed = {}
    for cand in RULES[1:]:
        print(f"\n== {cand} ==")
        L, F = last(wc[cand]), first(wc[cand])
        k2 = [med(L) >= fl["W-cone"] + 10, med(L) >= 0.5*med(F),
              compare(L, last(wc["control"]), f"K2 {cand} vs control, last third")[0]]
        k3 = [absorbed(wc[cand]) <= 0.10, reached(wl[cand]) >= 0.75, absorbed(wl[cand]) <= 0.10,
              med(last(wl[cand])) >= fl["W-lost"] + 10]
        k4 = absorbed(oc[cand]) <= 0.10 and med(last(oc[cand])) >= fl["O-cone"] + 10
        print(f"   K2 clears floor {k2[0]}, sustained (last {med(L):.1f} >= half of first"
              f" {med(F):.1f}) {k2[1]}, beats control {k2[2]} -> {'pass' if all(k2) else 'FAIL'}")
        print(f"   K3 W-cone absorbed {absorbed(wc[cand])*100:.1f}% <= 10: {k3[0]};  W-lost reached"
              f" {reached(wl[cand])*100:.1f}% >= 75: {k3[1]}, absorbed {absorbed(wl[cand])*100:.1f}%"
              f" <= 10: {k3[2]}, last third {med(last(wl[cand])):.1f} >= {fl['W-lost'] + 10:.1f}:"
              f" {k3[3]} -> {'pass' if all(k3) else 'FAIL'}")
        print(f"   K4 O-cone absorbed {absorbed(oc[cand])*100:.1f}%, last third"
              f" {med(last(oc[cand])):.1f} (random {fl['O-cone']:.1f}) ->"
              f" {'boundary-INDEPENDENT' if k4 else 'boundary-dependent'};"
              f"  W-cone recoveries without wall contact:"
              f" {float(wc[cand]['wallfree'].mean())*100 if len(wc[cand]['gaps']) else float('nan'):.1f}%")
        if k1 and all(k2) and all(k3):
            passed[cand] = (not k4, absorbed(wc[cand]), -med(L))
    singles = [passed[c] for c in ("wall", "return") if c in passed]
    if "both" in passed and singles and not all(passed["both"] < s for s in singles):
        del passed["both"]
    sel = min(passed, key=passed.get) if passed else None
    print(f"\n== H16 Stage A verdict ==  K1 {'pass' if k1 else 'FAIL'};"
          f" candidates passing K2 and K3: {list(passed) or 'none'}"
          f" -> {'SUPPORTED' if passed else 'not supported'}; selected for Stage B: {sel}")
    return sel


def stage_b(rule, mode, exact):
    sw, sa = SEEDS[mode]
    print(f"\n== K5 Stage B: rule `{rule}`, ring exactly as adopted (H14) and cued (H15): {RING},"
          f" noise 0.3, cue {WIND_CUE} ==")
    print("   (a) wind cue on every step, W-cone, same seeds as Stage A so `exact` IS the Stage A arm")
    ring = run(rule, head="ring", seeds=(sw, sa))
    describe("exact", exact, 0.0, True); describe("ring", ring, 0.0, True)
    e45 = ring["err"][0]/ring["err"][1]
    ka = [med(last(ring)) >= 0.75*med(last(exact)), absorbed(ring) <= 0.10, e45 < 0.05]
    print(f"   ring last third {med(last(ring)):.1f} >= 75% of exact {med(last(exact)):.1f}: {ka[0]};"
          f"  absorbed {absorbed(ring)*100:.1f}% <= 10: {ka[1]};"
          f"  heading error > 45 deg in {e45*100:.2f}% of agent-steps < 5: {ka[2]}"
          f"  -> K5(a) {'pass' if all(ka) else 'FAIL'}")
    print(f"   (b) cue dropout, 50 off / 50 on. world seed {sw + 4}, agent seed {sa + 4}. Reported.")
    arms = {h: run(rule, head=h, wind="blocks", seeds=(sw + 4, sa + 4))
            for h in ("none", "ring", "integrate")}
    for h, o in arms.items():
        describe(h, o, 0.0, True)
        print(f"            heading error > 45 deg: {o['err'][0]/o['err'][1]*100:5.2f}% of all steps,"
              f" {o['err_off'][0]/o['err_off'][1]*100:5.2f}% of cue-off steps")
    compare(last(arms["ring"]), last(arms["none"]), "memory effect: ring vs none under dropout")
    compare(last(arms["integrate"]), last(arms["none"]), "reference: perfect integrator vs none")
    return all(ka)


def demo():
    a = Nav2(3, np.random.default_rng(0), "return")
    a.clock = np.array([0.0, SAT, 2*SAT]); assert np.allclose(a.offset(), [0, MAXOFF, 0])
    a = Nav2(2, np.random.default_rng(0), "wall"); a.clock = np.array([10.0, 200.0])
    a.bump(np.array([True, True])); assert list(a.clock) == [10.0, 0.0] and list(a.cast_sign) == [-1, -1]
    w = World1(300, np.random.default_rng(0), start="lost"); assert not w.in_odour().any()
    assert World1(300, np.random.default_rng(0)).in_odour().all(), "cone start is outside the odour"
    w = World1(50, np.random.default_rng(0), wind="blocks"); on = 0
    for _ in range(200): on += w.wind_on(); w.move(np.zeros(50))
    assert (on == 100).all() and (w.pos.min() >= 0) and (w.pos.max() <= ARENA)
    # with no walls there is no reflex, so `control` must BE 7.3's cast rule, step for step
    w1 = World1(40, np.random.default_rng(3), walls=False); w2 = World1(40, np.random.default_rng(3), walls=False)
    n1 = Nav2(40, np.random.default_rng(4), "control"); n2 = Nav(40, np.random.default_rng(4), "cast", "none")
    for _ in range(400):
        w1.move(n1.act(w1, w1.sense(), w1.wind_on())); w2.move(n2.act(w2, w2.sense(), w2.wind_on()))
    assert np.allclose(w1.pos, w2.pos), "control is not the 7.3 rule"
    assert not w1.bumped.any()
    print("ok  triangle offset, conditional wall restart, start conditions, wind blocks, walls hold")
    print("ok  `control` reproduces ph9's cast rule exactly over 400 steps in the open world")


if __name__ == "__main__":
    mode = ([m for m in sys.argv[1:] if m in ("demo", "dev", "eval")] or ["demo"])[0]
    if mode == "demo": demo(); sys.exit(0)
    print(f"== H16 {mode.upper()} run. {R} agents, {BLOCKS} blocks of {STEPS} steps, one persistent world ==")
    print("== Criteria: record:h16-success-criteria, stored before this file existed ==")
    res = stage_a(mode)
    if mode == "dev":
        o = run("wall0", seeds=SEEDS["dev"])
        print(f"\n== dev only: unconditional wall restart (`wall0`), W-cone ==")
        describe("wall0", o, 0.0, True)
        print(f"            at the upwind wall (x < 1) at the end: {float((o['end_pos'][:, 0] < 1).mean())*100:.1f}%")
    sel = verdict_a(res)
    if sel: stage_b(sel, mode, res["W-cone"][sel])
    elif mode == "dev":
        print("\n== dev only: no candidate passed, so Stage B is FORCED with `return` to exercise"
              " its code. Not a verdict. ==")
        stage_b("return", mode, res["W-cone"]["return"])
    else: print("\n== K5 Stage B not run: no candidate passed K1-K3 ==")
