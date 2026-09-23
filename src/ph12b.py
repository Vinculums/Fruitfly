#!/usr/bin/env python3
"""H16 Run 2: the unchanged `return` rule in a pre-registered low-boundary environment.

Usage: python ph12b.py demo | contract | dev | eval

Run 1 (ph12.py) stands as not supported: `return` cut the late unrecovered fraction from 98 to
1 percent but only matched a random walk in H15's 40x40 arena, where it spent a third of its
steps against a wall. Run 2 moves the walls and nothing else. Every position is drawn in Run 1's
40x40 frame by Run 1's code and translated by +60, inside walls 160 apart; rules come from
ph12.Nav2 unchanged. A pass is valid only for environments with little boundary influence.

Opened by decision:h16-run2-open. Pre-registration: record:h16-run2-success-criteria (geometry,
what is kept, K1-K4 unchanged, Stage B changes), stored before this file existed.
`contract` is Stage B's step 0: does the rotation handed to the integrator equal the rotation
the body made? Development seeds, measurement only.
"""
import sys
import numpy as np
from ph9 import angdiff, compare, SPEED, STEPS
from ph12 import World1, Nav2, R, BLOCKS, LOST, last, first, absorbed, reached, med

ARENA2, SHIFT = 160.0, 60.0
SEEDS = dict(dev=(9200, 9300), eval=(1610, 1710))
CONDS = [("W-cone", "cone", True), ("W-lost", "lost", True),
         ("O-cone", "cone", False), ("O-lost", "lost", False)]
ARMS = ["random", "oracle", "control", "return"]


class World3(World1):
    """Run 1's world, drawn by Run 1's code in its 40x40 frame, then translated by `shift`
    inside walls `arena` apart. arena 40 with shift 0 IS Run 1's world (checked in demo)."""

    def __init__(self, runs, rng, start="cone", walls=True, wind="always", arena=ARENA2, shift=SHIFT):
        super().__init__(runs, rng, start, walls, wind)
        self.arena = arena
        self.src = self.src + shift; self.pos = self.pos + shift
        self.rot = np.zeros(runs)

    def wind_on(self):
        # record:h16-run2-stage-b-amendment. Under dropout every agent senses the wind for the
        # first 50 steps. With a random phase alone, half the agents began blind inside a cue-off
        # block, left the cone and faced a cold search: on development seeds the PERFECT
        # integrator reached the source in 85.5 percent of agents against 100 for exact heading.
        return super().wind_on() | (self.t < 50)

    def move(self, turn):
        self.t += 1
        h0 = self.head.copy()
        self.head = (self.head + turn) % 360.0
        a = np.radians(self.head)
        p = self.pos + SPEED*np.stack([np.cos(a), np.sin(a)], 1)
        bumped = np.zeros(self.R, bool)
        if self.walls:                                   # ph11.World2.move with the arena a field
            for k, flip in ((0, 180.0), (1, 0.0)):
                out = (p[:, k] < 0) | (p[:, k] > self.arena)
                if out.any():
                    p[out, k] = np.clip(2*np.clip(p[out, k], 0.0, self.arena) - p[out, k], 0.0, self.arena)
                    self.head[out] = (flip - self.head[out]) % 360.0
                    bumped |= out
        self.pos, self.bumped = p, bumped
        self.rot = angdiff(self.head, h0)                # what the body did, reflection included


class Nav3(Nav2):
    """Nav2 plus one measurement-only heading mode: a perfect integrator fed the ACTUAL rotation."""

    def estimate(self, w, wind_on):
        if self.head != "integrate_actual": return super().estimate(w, wind_on)
        self.belief = np.where(wind_on, w.head, (self.belief + w.rot) % 360.0)
        return self.belief


def run2(rule, head="exact", start="cone", walls=True, wind="always", seeds=(0, 1),
         arena=ARENA2, shift=SHIFT):
    w = World3(R, np.random.default_rng(seeds[0]), start, walls, wind, arena, shift)
    a = Nav3(R, np.random.default_rng(seeds[1]), rule, head)
    z = lambda: np.zeros((BLOCKS, R))
    o = dict(score=z(), whiff=z(), wall=z(), contact=z(), events=0, gaps=[], wallfree=[],
             err=np.zeros(2), err_off=np.zeros(2), abs_off=0.0, mismatch=np.zeros(3))
    touched = np.zeros(R, bool)
    for t in range(BLOCKS*STEPS):
        b = t // STEPS
        hit = w.sense(); won = w.wind_on()
        back = hit & (a.since > LOST)
        if back.any():
            o["gaps"].append(a.since[back].copy()); o["wallfree"].append(~touched[back])
        touched &= ~hit
        turn = a.act(w, hit, won)
        o["events"] += int((a.since == LOST + 1).sum())
        if head != "exact":
            e = np.abs(angdiff(a.est, w.head)); bad = e > 45.0
            o["err"] += (bad.sum(), R); o["err_off"] += (bad[~won].sum(), (~won).sum())
            o["abs_off"] += e[~won].sum()
        w.move(turn); a.bump(w.bumped); touched |= w.bumped
        differ = np.abs(angdiff(w.rot, turn)) > 1e-6     # handed to the integrator vs actually made
        o["mismatch"] += (differ.sum(), (differ & w.bumped).sum(), R)
        o["score"][b] += w.at_source(); o["whiff"][b] += hit; o["contact"][b] += w.bumped
        if walls: o["wall"][b] += np.minimum(w.pos, w.arena - w.pos).min(1) < 1.0
    o["lost_end"] = a.since > LOST
    o["gaps"] = np.concatenate(o["gaps"]) if o["gaps"] else np.zeros(0)
    o["wallfree"] = np.concatenate(o["wallfree"]) if o["wallfree"] else np.zeros(0, bool)
    return o


def describe2(name, o, floor, walls):
    L, F = last(o), first(o)
    q = np.percentile(L, [10, 25, 50, 75, 90])
    print(f"   {name:9s} last third: median {q[2]:6.1f} mean {L.mean():6.1f}"
          f"  p10/25/75/90 {q[0]:5.1f} {q[1]:5.1f} {q[3]:5.1f} {q[4]:5.1f}"
          f"  >floor+10: {float((L > floor + 10).mean())*100:5.1f}%"
          f" | first third median {med(F):6.1f} | late unrecovered {absorbed(o)*100:5.1f}%"
          f"  lost at end {float(o['lost_end'].mean())*100:5.1f}%  reached ever {reached(o)*100:5.1f}%")
    fmt = lambda v: " ".join(f"{x:5.1f}" for x in v)
    if name != "oracle":
        print(f"             per block  median score   {fmt(np.median(o['score'], 1))}")
        print(f"                        % scoring      {fmt((o['score'] > 0).mean(1)*100)}")
        print(f"                        % with whiff   {fmt((o['whiff'] > 0).mean(1)*100)}")
        if walls:
            print(f"                        % near wall    {fmt(o['wall'].mean(1)/STEPS*100)}")
            print(f"                        contacts/agent {fmt(o['contact'].mean(1))}")
            print(f"                        % touching     {fmt((o['contact'] > 0).mean(1)*100)}")
    if walls:
        c = o["contact"].sum(0)
        print(f"             exposure   contacts per agent over the run: mean {c.mean():7.1f} median {med(c):6.0f};"
              f"  never touch a wall {float((c == 0).mean())*100:5.1f}%,"
              f" never after block 1 {float((o['contact'][1:].sum(0) == 0).mean())*100:5.1f}%")
    if name in ("random", "oracle"): return
    g = o["gaps"]; ev = o["events"]
    rec = f"{len(g)/ev*100:5.1f}%" if ev else "  n/a"
    tim = f"median {med(g):6.0f}  p90 {np.percentile(g, 90):6.0f}" if len(g) else "none"
    wf = f"{float(o['wallfree'].mean())*100:5.1f}%" if len(g) else "  n/a"
    print(f"             recovery   lost events {ev:5d}  recovered {rec}  reacquisition {tim}"
          f"  without wall contact {wf}")


def stage_a(mode):
    sw, sa = SEEDS[mode]; res = {}
    for c, (cname, start, walls) in enumerate(CONDS):
        print(f"\n== {cname}: {'walls 160 apart' if walls else 'NO walls'}, {start} start, Run 1 frame + 60."
              f" world seed {sw + c}, agent seed {sa + c} ==")
        res[cname] = {arm: run2(arm, start=start, walls=walls, seeds=(sw + c, sa + c)) for arm in ARMS}
        floor = med(last(res[cname]["random"]))
        for arm in ARMS: describe2(arm, res[cname][arm], floor, walls)
    print(f"\n== Reference, reported only: Run 1's 40x40 arena on W-cone's seeds ({sw}, {sa})."
          f" Same initial states, only the walls moved. ==")
    ref = {arm: run2(arm, seeds=(sw, sa), arena=40.0, shift=0.0) for arm in ("random", "control", "return")}
    floor = med(last(ref["random"]))
    for arm, o in ref.items(): describe2(arm, o, floor, True)
    return res


def verdict(res):
    wc, wl, oc = res["W-cone"], res["W-lost"], res["O-cone"]
    fl = {k: med(last(v["random"])) for k, v in res.items()}
    L, F = last(wc["return"]), first(wc["return"])
    print("\n== K1 validity, W-cone, last third ==")
    k1 = [med(last(wc["oracle"])) - fl["W-cone"] >= 10,
          all(med(last(wc[a])) < 0.99*STEPS for a in ("control", "return")),
          absorbed(wc["control"]) >= 0.5]
    print(f"   (a) oracle {med(last(wc['oracle'])):.1f} - random {fl['W-cone']:.1f} >= 10: {k1[0]}")
    print(f"   (b) no rule arm at 99 percent of {STEPS}: {k1[1]}")
    print(f"   (c) control late unrecovered {absorbed(wc['control'])*100:.1f}% >= 50%: {k1[2]}")
    print(f"   (d) return clears random + 10: {med(L) >= fl['W-cone'] + 10}")
    print("\n== return ==")
    k2 = [med(L) >= fl["W-cone"] + 10, med(L) >= 0.5*med(F),
          compare(L, last(wc["control"]), "K2 return vs control, last third")[0]]
    k3 = [absorbed(wc["return"]) <= 0.10, reached(wl["return"]) >= 0.75, absorbed(wl["return"]) <= 0.10,
          med(last(wl["return"])) >= fl["W-lost"] + 10]
    k4 = absorbed(oc["return"]) <= 0.10 and med(last(oc["return"])) >= fl["O-cone"] + 10
    print(f"   K2 clears floor ({med(L):.1f} >= {fl['W-cone'] + 10:.1f}) {k2[0]}, sustained (>= half of first"
          f" {med(F):.1f}) {k2[1]}, beats control {k2[2]} -> {'pass' if all(k2) else 'FAIL'}"
          f"   [reported: clears Run 1's absolute bar of 20.0: {med(L) >= 20.0}]")
    print(f"   K3 W-cone late unrecovered {absorbed(wc['return'])*100:.1f}% <= 10: {k3[0]};  W-lost reached"
          f" {reached(wl['return'])*100:.1f}% >= 75: {k3[1]}, late unrecovered {absorbed(wl['return'])*100:.1f}%"
          f" <= 10: {k3[2]}, last third {med(last(wl['return'])):.1f} >= {fl['W-lost'] + 10:.1f}: {k3[3]}"
          f" -> {'pass' if all(k3) else 'FAIL'}")
    print(f"   K4 O-cone late unrecovered {absorbed(oc['return'])*100:.1f}%, last third"
          f" {med(last(oc['return'])):.1f} (random {fl['O-cone']:.1f}) ->"
          f" {'boundary-INDEPENDENT' if k4 else 'boundary-dependent'}")
    ok = all(k1) and all(k2) and all(k3)
    print(f"\n== H16 Run 2 Stage A verdict ==  K1 {'pass' if all(k1) else 'FAIL'}  K2 {'pass' if all(k2) else 'FAIL'}"
          f"  K3 {'pass' if all(k3) else 'FAIL'} -> {'SUPPORTED, for low-boundary environments only' if ok else 'not supported'}")
    return all(k1) and all(k2) and k3[0]                 # Stage B's trigger, as registered


def stage_b(mode, res):
    sw, sa = SEEDS[mode]
    print("\n== K5 Stage B: `return`, ring exactly as adopted (H14) and cued (H15), noise 0.3. Nothing changed. ==")
    print(f"   (a) W-cone, wind cue every step, seeds ({sw}, {sa}) so `exact` IS the Stage A arm")
    exact = res["W-cone"]["return"]; ring = run2("return", head="ring", seeds=(sw, sa))
    describe2("exact", exact, 0.0, True); describe2("ring", ring, 0.0, True)
    e45 = ring["err"][0]/ring["err"][1]
    ka = [med(last(ring)) >= 0.75*med(last(exact)), absorbed(ring) <= 0.10, e45 < 0.05]
    print(f"   ring last third {med(last(ring)):.1f} >= 75% of exact {med(last(exact)):.1f}: {ka[0]};"
          f"  late unrecovered {absorbed(ring)*100:.1f}% <= 10: {ka[1]};"
          f"  heading error > 45 deg in {e45*100:.2f}% of agent-steps < 5: {ka[2]}"
          f"  -> K5(a) {'pass' if all(ka) else 'FAIL'}")
    print(f"\n   (b) OPEN PLANE, cue dropout 50 off / 50 on, seeds ({sw + 2}, {sa + 2}) so `exact` IS Stage A's O-cone arm")
    exact = res["O-cone"]["return"]; describe2("exact", exact, 0.0, False)
    arms = {h: run2("return", head=h, walls=False, wind="blocks", seeds=(sw + 2, sa + 2))
            for h in ("none", "ring", "integrate")}
    for h, o in arms.items():
        describe2(h, o, 0.0, False)
        print(f"             heading error > 45 deg: {o['err'][0]/o['err'][1]*100:5.2f}% of all steps,"
              f" {o['err_off'][0]/o['err_off'][1]*100:5.2f}% of cue-off steps;"
              f"  mean |error| on cue-off steps {o['abs_off']/o['err_off'][1]:5.1f} deg")
    inst = arms["integrate"]["err_off"][0]/arms["integrate"]["err_off"][1]
    print(f"   instrument check: perfect integrator > 45 deg wrong on {inst*100:.2f}% of cue-off steps < 1:"
          f" {inst < 0.01}{'' if inst < 0.01 else '  -> (b) is NOT read'}")
    kept = med(last(arms["ring"])) >= 0.75*med(last(exact)) and absorbed(arms["ring"]) <= 0.10
    print(f"   ring under dropout {med(last(arms['ring'])):.1f} vs exact {med(last(exact)):.1f}, late unrecovered"
          f" {absorbed(arms['ring'])*100:.1f}% -> {'maintained' if kept else 'NOT maintained'} under cue loss")
    compare(last(arms["ring"]), last(arms["none"]), "memory effect: ring vs none under dropout")
    compare(last(arms["integrate"]), last(arms["none"]), "reference: perfect integrator vs none")


def contract():
    """Stage B step 0. Is the rotation handed to the integrator the rotation the body made?"""
    sw, sa = SEEDS["dev"]
    print("== input contract, development seeds, measurement only ==")
    for label, kw in (("Run 1's 40x40 arena", dict(arena=40.0, shift=0.0)), ("160x160 arena", {}),
                      ("open plane", dict(walls=False))):
        print(f"\n   {label}, `return`, cue dropout 50/50:")
        for h in ("integrate", "integrate_actual"):
            o = run2("return", head=h, wind="blocks", seeds=(sw, sa), **kw)
            d, db, n = o["mismatch"]
            print(f"     {h:17s} handed != made on {d/(n)*100:6.3f}% of agent-steps,"
                  f" {db/d*100 if d else float('nan'):5.1f}% of those are wall contacts;"
                  f"  heading error > 45 deg on {o['err_off'][0]/o['err_off'][1]*100:5.2f}% of cue-off steps"
                  f" (mean |error| {o['abs_off']/o['err_off'][1]:5.1f} deg);  last third {med(last(o)):5.1f}")


def demo():
    from ph12 import run
    # arena 40, shift 0 must BE Run 1's world: same walls, same contacts, same scores
    a = run("return", seeds=(5, 6)); b = run2("return", seeds=(5, 6), arena=40.0, shift=0.0)
    assert np.array_equal(a["score"], b["score"]) and np.array_equal(a["wall"], b["wall"])
    # translation only: relative geometry is Run 1's, and the open plane cannot tell the difference
    w0 = World1(200, np.random.default_rng(7), "lost"); w1 = World3(200, np.random.default_rng(7), "lost")
    assert np.allclose(w1.src - w0.src, SHIFT) and np.allclose(w1.pos - w0.pos, SHIFT)
    assert w1.src.min() >= 68 and w1.src.max() <= 92 and w1.pos.min() >= 60 and w1.pos.max() <= 100
    a = run("return", walls=False, seeds=(5, 6)); b = run2("return", walls=False, seeds=(5, 6))
    assert np.array_equal(a["score"], b["score"])
    # with no wall, handed and made rotation agree on every step, and the two integrators are one
    assert b["mismatch"][0] == 0
    print("ok  arena 40 / shift 0 reproduces ph12 exactly; geometry is Run 1's frame + 60")
    print("ok  the open plane is translation-invariant; handed == made rotation when nothing is hit")


if __name__ == "__main__":
    mode = ([m for m in sys.argv[1:] if m in ("demo", "contract", "dev", "eval")] or ["demo"])[0]
    if mode == "demo": demo(); sys.exit(0)
    if mode == "contract": contract(); sys.exit(0)
    print(f"== H16 Run 2 {mode.upper()}. {R} agents, {BLOCKS} blocks of {STEPS} steps, one persistent world ==")
    print("== Pre-registration: record:h16-run2-success-criteria, stored before this file existed ==")
    res = stage_a(mode)
    if verdict(res) or mode == "dev": stage_b(mode, res)     # dev always exercises Stage B's code
    else: print("\n== K5 Stage B not run: return did not pass K1, K2 and K3's W-cone clause ==")
