#!/usr/bin/env python3
"""Two-source discriminability check, before H15 Run 2.

Usage: python ph13.py demo | dev | eval

Can the two-source world measure search, valence-driven behaviour and (later) learning
separately? Nothing is learned here. Two arms answer two different questions: `neutral` gives
both odours zero valence, which is the agent before it has learned anything; `known` supplies
the correct valence, which asks only whether valence, once there, is USED.

The agent is ph11.Agent with two changes, both owner decisions: the cast is the return rule
(decision:h16-close-limited-adoption) and the ring is fed the rotation made
(decision:heading-input-rotation-made). The world is ph11.World2 drawn in its own 40x40 frame
and translated +60 inside walls 160 apart, as H16 Run 2 did for one source.

Opened by decision:h15-two-source-check-open. Geometry, measures and criteria M1-M5:
record:two-source-check-criteria, stored before this file existed. No net score is used
anywhere: H15's +1/-1 sum is what hid a random walk's occupancy floor.
"""
import sys
import numpy as np
from ph3 import cue
from ph9 import UPWIND, CAST_PERIOD, CAST_GROW, MAXOFF, GAIN, MAXTURN, TURN_NOISE, STEPS, angdiff, compare
from ph11 import World2, Agent, WIND_CUE, RESET_AFTER, MARGIN
from ph12 import SAT, med
from ph12b import World3

R, BLOCKS = 200, 9
SEEDS = dict(dev=(9600, 9700), eval=(1620, 1720))
ARMS = ["random", "oracle", "neutral", "known"]


class World4(World2):
    """ph11's two-source world, drawn by ph11's code, translated by `shift` inside walls `arena`
    apart. `start` is the index of the source whose cone the agent begins in."""

    def __init__(self, runs, rng, arena=160.0, shift=60.0):
        super().__init__(runs, rng)
        self.arena, self.walls, self.t = arena, True, 0
        self.src = self.src + shift; self.pos = self.pos + shift
        self.rot = np.zeros(runs); self.bumped = np.zeros(runs, bool)
        self.start = np.abs(self.pos[:, None, 1] - self.src[:, :, 1]).argmin(1)

    def move(self, turn): World3.move(self, turn)        # walls as a field, contacts, rotation made


class Agent2(Agent):
    """ph11.Agent with the cast and the ring's input selectable. Defaults are the adopted ones;
    cast='saturate' with rot='commanded' must BE ph11.Agent (checked in demo). The Phase 5
    navigation ablation is not carried over; nothing here ablates navigation."""

    def __init__(self, runs, rng, abl=(), rule="agent", known=None, cast="return", rot="made"):
        super().__init__(runs, rng, abl, rule, known)
        self.cast, self.rot_in, self.est = cast, rot, np.zeros(runs)

    def estimate(self, w, wind_on):
        if self.rot_in == "commanded" or "head" in self.abl: return super().estimate(w, wind_on)
        self.ring.step(v=w.rot)
        if wind_on.any():
            self.ring.step(x=cue(self.R, 16, w.head, WIND_CUE, width=1.2)*wind_on[:, None])
        return self.ring.pos()

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
        self.since = np.where(hit, 0.0, self.since + 1.0)
        self.silence = np.where(hit, 0.0, self.silence + 1.0)
        side = np.where((self.since // CAST_PERIOD) % 2 == 0, 1.0, -1.0)*self.cast_sign
        if self.cast == "return":                        # ph12.Nav2's rule, clock == since here
            off = MAXOFF*(1.0 - np.abs((self.since/SAT) % 2.0 - 1.0))
        else:
            off = np.minimum(MAXOFF, CAST_GROW*self.since)
        tgt = np.where(hit, UPWIND, (UPWIND + side*off) % 360.0)
        tgt = np.where(val < 0, self.flee_side, tgt)
        turn = np.clip(GAIN*angdiff(tgt, est), -MAXTURN, MAXTURN)
        turn = turn + TURN_NOISE*self.rng.standard_normal(self.R)
        self.last_turn = turn
        return turn, h


def run(arm, seeds, arena=160.0, shift=60.0, runs=None, steps=BLOCKS*STEPS, **agent_kw):
    n = runs or R
    w = World4(n, np.random.default_rng(seeds[0]), arena, shift)
    rows = np.arange(n); kv, abl, rule = None, ("learn",), "agent"
    if arm == "known":
        kv = np.full((n, 2), -1.0); kv[rows, w.good] = 1.0; abl = ()
    if arm in ("random", "oracle"): rule = arm
    a = Agent2(n, np.random.default_rng(seeds[1]), abl=abl, rule=rule, known=kv, **agent_kw)
    z = lambda: np.zeros((BLOCKS, n))
    o = dict(g=z(), b=z(), whiff=z(), contact=z(), wall=z(), err=np.zeros(2),
             first_g=np.full(n, -1), first_b=np.full(n, -1), start_good=w.start == w.good, world=w)
    for t in range(steps):
        k = t // STEPS
        whiffs = w.sense()
        turn, _ = a.act(w, whiffs, w.wind_on())
        if rule == "agent":
            o["err"] += ((np.abs(angdiff(a.est, w.head)) > 45.0).sum(), n)
        w.move(turn); a.bump(w.bumped)
        at = w.at_source(); g = at[rows, w.good]; b = at[rows, 1 - w.good]
        o["g"][k] += g; o["b"][k] += b; o["whiff"][k] += whiffs.any(1); o["contact"][k] += w.bumped
        o["wall"][k] += np.minimum(w.pos, w.arena - w.pos).min(1) < 1.0
        o["first_g"] = np.where((o["first_g"] < 0) & g, t, o["first_g"])
        o["first_b"] = np.where((o["first_b"] < 0) & b, t, o["first_b"])
    return o


def late(x, m=slice(None)): return x[-3:].mean(0)[m]
def unrecovered(o, m=slice(None)): return float((o["whiff"][-3:].sum(0)[m] == 0).mean())
def nearwall(o, m=slice(None)): return float(o["wall"][-3:].mean(0)[m].mean()/STEPS)


def describe(name, o, m, label):
    fg, fb = o["first_g"][m], o["first_b"][m]; n = int(np.sum(m)) if m is not Ellipsis else len(fg)
    vg, vb = fg >= 0, fb >= 0; both = vg & vb
    early = lambda f: float(((f >= 0) & (f < 3*STEPS)).mean())*100
    first = np.where(vg & vb, np.minimum(fg, fb), np.where(vg, fg, fb))[vg | vb]
    move = np.abs(fg - fb)[both]
    fmt = lambda v: " ".join(f"{x:5.1f}" for x in v)
    print(f"   {name:8s} {label:22s} n {n:3d} | visited rewarding {vg.mean()*100:5.1f}% punishing {vb.mean()*100:5.1f}%"
          f" both {both.mean()*100:5.1f}%  (in the first third: {early(fg):5.1f} / {early(fb):5.1f}"
          f" / {float(((fg >= 0) & (fg < 3*STEPS) & (fb >= 0) & (fb < 3*STEPS)).mean())*100:5.1f})")
    print(f"            first visit to any source: median step {med(first) if len(first) else float('nan'):6.0f}"
          f" ({len(first)} agents);  first of one source -> first of the other: median"
          f" {med(move) if len(move) else float('nan'):6.0f} steps ({len(move)} agents)")
    print(f"            dwell, last third: rewarding median {med(late(o['g'], m)):6.1f} mean {late(o['g'], m).mean():6.1f}"
          f" | punishing median {med(late(o['b'], m)):6.1f} mean {late(o['b'], m).mean():6.1f}"
          f" | late unrecovered {unrecovered(o, m)*100:5.1f}%  contacts/agent {o['contact'].sum(0)[m].mean():7.1f}"
          f"  near wall (last third) {nearwall(o, m)*100:5.2f}%")
    print(f"            per block median dwell  rewarding {fmt(np.median(o['g'][:, m], 1))}")
    print(f"                                    punishing {fmt(np.median(o['b'][:, m], 1))}")


def table(mode):
    seeds = SEEDS[mode]; res = {}
    print(f"\n== two sources, walls 160 apart, ph11 frame + 60. world seed {seeds[0]}, agent seed {seeds[1]} ==")
    for arm in ARMS:
        res[arm] = o = run(arm, seeds); sg = o["start_good"]
        if arm == "random":
            w = o["world"]; s = np.abs(w.src[:, 0, 1] - w.src[:, 1, 1])
            print(f"   geometry check: source separation {s.min():.1f}-{s.max():.1f} crosswind, 0 along the wind;"
                  f" cones overlap in {float((s < 15.5).mean())*100:.1f}% of worlds;"
                  f" start in the rewarding cone {float(sg.mean())*100:.1f}%;"
                  f" nearest wall to any source {float(np.minimum(w.src, w.arena - w.src).min()):.1f}")
        print()
        describe(arm, o, Ellipsis, "all agents")
        if arm in ("neutral", "known"):
            describe(arm, o, sg, "start: rewarding cone"); describe(arm, o, ~sg, "start: punishing cone")
            print(f"            heading error > 45 deg on {o['err'][0]/o['err'][1]*100:.2f}% of agent-steps")
    return res


def verdict(res):
    rnd, orc, neu, kno = (res[a] for a in ARMS)
    print("\n== M1 validity, last third, per source ==")
    m1a = med(late(orc["g"])) - med(late(rnd["g"])) >= 10
    m1b = all(med(late(o[k])) < 0.99*STEPS for o in (neu, kno) for k in ("g", "b"))
    print(f"   oracle rewarding dwell {med(late(orc['g'])):.1f} - random {med(late(rnd['g'])):.1f} >= 10: {m1a};"
          f"  random punishing dwell {med(late(rnd['b'])):.1f};  no agent arm at the ceiling: {m1b}")
    print("\n== M2 search and persistence without valence (neutral arm) ==")
    tot = late(neu["g"]) + late(neu["b"]); floor = med(late(rnd["g"]) + late(rnd["b"]))
    m2 = [med(tot) >= floor + 10, unrecovered(neu) <= 0.10]
    print(f"   total dwell median {med(tot):.1f} >= random {floor:.1f} + 10: {m2[0]};"
          f"  late unrecovered {unrecovered(neu)*100:.1f}% <= 10: {m2[1]}")
    print("\n== M3 valence is used (known against neutral) ==")
    dk = late(kno["g"]) - late(kno["b"]); dn = late(neu["g"]) - late(neu["b"])
    p = ~neu["start_good"]
    # record:two-source-check-m3-amendment. A valence of +1 changes nothing in ph11's agent, so an
    # agent that never holds the punished odour is the same agent in both arms and its pair is an
    # exact tie. Over all agents the 60 percent bar is out of reach by construction; (a) is read
    # where valence has something to act on, and the all-agent figure is printed as first registered.
    reg = compare(dk, dn, "(a) AS FIRST REGISTERED, all agents")[0]
    print(f"       exactly tied pairs: {float((dk == dn).mean())*100:.1f}% of all agents,"
          f" {float((dk == dn)[~p].mean())*100:.1f}% of those starting in the rewarding cone")
    m3a = compare(dk[p], dn[p], "(a) AS AMENDED, start in the punishing cone")[0]
    bn, bk = med(late(neu["b"], p)), med(late(kno["b"], p))
    readable = bn >= 10                                   # standing rule: a baseline pinned near zero is not read
    m3b = readable and bk <= 0.5*bn
    print(f"   (b) start in the punishing cone: punishing dwell known {bk:.1f} <= half of neutral {bn:.1f}:"
          f" {m3b if readable else 'UNREADABLE, the neutral baseline is below 10'}")
    print("\n== M4 exposure label (not a gate) ==")
    both = lambda o: float(((o["first_g"] >= 0) & (o["first_b"] >= 0)).mean())
    print(f"   agents visiting BOTH sources: neutral {both(neu)*100:.1f}%, known {both(kno)*100:.1f}%  ->"
          f" natural exposure {'SUFFICIENT' if both(neu) >= 0.75 else 'insufficient; two separate evaluations needed'}")
    print("\n== M5 boundary label ==")
    for name, o in (("neutral", neu), ("known", kno)):
        nw = nearwall(o)
        print(f"   {name:8s} near wall in the last third {nw*100:.2f}%  contacts/agent {o['contact'].sum(0).mean():.1f}"
              f"  -> {'FLAGGED, outside the adoption scope' if nw > 0.10 else 'within the adoption scope'}")
    base = m1a and m1b and all(m2) and m3b
    print(f"\n== two-source check ==  M1 {'pass' if m1a and m1b else 'FAIL'}  M2 {'pass' if all(m2) else 'FAIL'}"
          f"  M3 as amended {'pass' if m3a and m3b else 'FAIL'} (as first registered {'pass' if reg and m3b else 'FAIL'})"
          f"  -> {'DISCRIMINABLE' if base and m3a else 'not discriminable'} as amended;"
          f" {'discriminable' if base and reg else 'not discriminable'} as first registered")


def demo():
    # the copied act() must BE ph11.Agent when both changes are switched off, in ph11's own world
    for arm_kw in (dict(abl=("learn",)), dict(abl=())):
        w1 = World2(40, np.random.default_rng(3)); w2 = World4(40, np.random.default_rng(3), arena=40.0, shift=0.0)
        kv = np.full((40, 2), -1.0); kv[np.arange(40), w1.good] = 1.0
        known = None if arm_kw["abl"] else kv
        a1 = Agent(40, np.random.default_rng(4), known=known, **arm_kw)
        a2 = Agent2(40, np.random.default_rng(4), known=known, cast="saturate", rot="commanded", **arm_kw)
        for _ in range(400):
            t1, _ = a1.act(w1, w1.sense(), w1.wind_on()); w1.move(t1); a1.bump(w1.bumped)
            t2, _ = a2.act(w2, w2.sense(), w2.wind_on()); w2.move(t2); a2.bump(w2.bumped)
        assert np.allclose(w1.pos, w2.pos) and np.allclose(w1.head, w2.head), "Agent2 is not ph11.Agent"
    w = World4(400, np.random.default_rng(0)); s = np.abs(w.src[:, 0, 1] - w.src[:, 1, 1])
    assert s.min() >= 14 and s.max() <= 18 and np.allclose(w.src[:, 0, 0], w.src[:, 1, 0])
    assert np.minimum(w.src, w.arena - w.src).min() >= 68
    rows = np.arange(400); d = w.pos - w.src[rows, w.start]
    assert (d[:, 0] >= 5).all() and (d[:, 0] <= 18).all(), "start is not 5-18 downwind of its own source"
    print("ok  Agent2 with the old cast and the old input contract reproduces ph11.Agent over 400 steps,"
          " neutral and known")
    print("ok  sources 14-18 apart crosswind, every wall at least 68 away, start inside its own cone")


if __name__ == "__main__":
    mode = ([m for m in sys.argv[1:] if m in ("demo", "dev", "eval")] or ["demo"])[0]
    if mode == "demo": demo(); sys.exit(0)
    print(f"== two-source check, {mode.upper()}. {R} agents, {BLOCKS} blocks of {STEPS} steps, one persistent world ==")
    print("== Criteria: record:two-source-check-criteria, stored before this file existed ==")
    verdict(table(mode))
