#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H17: cold-start and reacquisition search (a navigation hypothesis).

Usage: python ph26.py demo | bench | dev | eval

Design v2 FINAL, confirmed by the owner (decision:h17-open, '그래 그방향으로 진행'): doc d83a917ea4152b4a7, hash f94d6ace...7516,
stored before this file existed; the classification-rule relaxation signed for H17 only
(decision:classification-rule-relaxed-any-odour-silence-counter-h17: ONE counter q = steps since the last whiff of any odour).
ONE change, a mixin on the adopted act (no adopted module edited, no act copied), design section 3:
  q <- 0 if any channel whiffs this step, else q + 1 (q = 0 at construction);
  engaged = search and q >= S and nothing held after this step's selection (h < 0);
  u = q - S; leg k = 1, 2, 3, ... lasts 30 k steps (L0 = CAST_PERIOD); sigma_k = cast_sign x (+1 odd k, -1 even k);
  slant alpha = +1 for (u mod 2 U1) < U1, else -1; search target = (UPWIND + sigma_k (90 - alpha gamma)) mod 360;
  on engaged rows only: tgt = the search target and turn = clip(0.6 angdiff(tgt, est), +-40) + (turn_base - clip(0.6 angdiff(tgt_base, est), +-40)),
  i.e. the base's own noise sample, so no random number is drawn; last_turn updated on those rows only. Everything else is the base act.
Agent12 = Search + ph24.Agent10 (the adopted agent: H23 filter + H25 release; the main arm), Agent12g = Search + ph24.Agent10g (reported).
search=False IS the base agent bitwise (checked). Measurement fields: q, engaged, u, leg (and tgt_base, the base's target).
Two run-time hooks, as ph25 did (the files are not edited): ph24.make also builds Agent12 / Agent12g; ph24.record also stores the search fields
(Q, ENG, U, LEG, CS, TGTB, NZB, NZ); the demo asserts the hooks leave every ph24.run / ph24.stub field bitwise equal. ph25 is NOT imported
(it hooks ph24 itself). Helpers reused by import: ph15's Wilson interval and seeded paired percentile bootstrap (via ph16.interval / crit),
ph18.majority / agg, ph24's run, stub, bitwise, events, t3_dwell; ph24c's drive-ended negative hold detection (released) and whiff-region geometry
(cone_geom); ph22.summary for W1. Nothing is copied.

Readings where the design is silent, chosen so that never-engaged rows stay bitwise Agent10 (printed again in the bench output):
 (R1) Step counting. q is updated at the top of each act from that step's whiffs. With silence from construction q = t + 1 at step index t, so the
      first engaged step is index 209, the 210th step (the design's 'step 210 after construction'); with one whiff at step index 0 the first engaged
      step is index 210 (S steps after the whiff). In (c1) q = since = 45 at construction, so engagement is at step index 164, the 165th step (the
      design's 'step 165'); window (i) is the 300 steps from the engagement step (indices 164-463), window (ii) the 600 steps from it
      (indices 164-763); the run is 765 steps (indices 0-764).
 (R2) (c2) since = q = S at construction, read literally: the first step is already engaged, with u = 1.
 (R3) The oracle ceiling (c): until the row's first whiff of any odour, target = the bearing to the nearest point of the nearest whiff region
      (ph11's cone 0 < d_along < 25, |d_cross| < 1.5 + 0.25 d_along, or within 3.0 of a source); inside a region without a whiff yet, the bearing to
      that region's source; the turn recomputed with the base's noise sample, as Search does. From the first whiff on, the adopted rule (Agent10).
 (R4) (c) constructions draw from the world generator right after World7's own draw (identical for every arm and wall setting); the agent's other
      state is the base construction (nothing held, silence 0, flee side and cast side as the base draws them); since (and q) set as the design says.
      Walls off = World3.move's `walls` attribute set False after construction (ph12b.py:53); walls on = World7's default.
 (R5) (b) schedules put the whiffs on channel 0 (the valued odour, known [1, 0]); (d)'s stub gap distribution uses 600 steps with both channels at p.
 (R6) Pass probabilities (section 7): a paired DP with b = the discordant fraction (rows whose indicator differs, both directions), sd = sqrt(b - DP^2),
      se = sd / 20; P = Phi((DP - bar) / se - 1.96) for a lower-bound bar, Phi((bar - DP) / se - 1.96) for an upper-bound bar; with sd 0 the
      point decides. The measured paired sd version is printed beside it.
 (R7) 'Reach' = within 3.0 of a source after a step's move (ph24.run's AT2 convention). u = -1 and leg = 0 on non-engaged steps (fields only).
Nothing changes after the table.
"""
import sys, os, re, math, hashlib
import numpy as np
import ph9, ph11, ph12b, ph13, ph15, ph16, ph18, ph19, ph21, ph22, ph24, ph24c
from ph16 import World7, Still, cast_draw, interval, crit, R, T
from ph18 import majority, describe_majority, agg
from ph19 import h21_diag
from ph21 import G_STAR, q3, first_true
from ph24 import Agent10, Agent10g, Agent8, Agent6, bitwise, traj, t3_dwell, q3f, events, on_hold
from ph24c import released, cone_geom
from ph9 import UPWIND, CAST_PERIOD, GAIN, MAXTURN, W0, SLOPE, LMAX, HIT_R, angdiff

sys.stdout.reconfigure(newline="\n")            # LF output, so the recorded sha256 equals the committed blob
DESIGN = "v2 FINAL doc d83a917ea4152b4a7 hash f94d6ace552816313e366c810267353e585d516c33621913aec0f3a1c9c87516"
S_ON, L0, GAMMA, U1 = 210, CAST_PERIOD, 15.0, 360          # design section 3 (S, L0 = CAST_PERIOD 30, gamma, U1)
SEEDS = dict(dev=(9943, 9953), eval=(1945, 2045))
BENCH = dict(rows=400, steps=600, steps_b=800, steps_stub=200, steps_c1=765, steps_c2=600, steps_c3=1800, q_c1=45, seed_w=20261051, seed_a=20261052)
BS = (BENCH["seed_w"], BENCH["seed_a"])
ph15.BOOT_SEED = 20261053                       # design section 7 (set after the imports, which set their own); ph16 set 95 percent
MODS = (ph9, ph11, ph12b, ph13, ph15, ph16, ph18, ph19, ph21, ph22, ph24, ph24c)
Z95 = 1.959964


def sha(p=__file__): return hashlib.sha256(open(p, "rb").read()).hexdigest()


# ------------------------------------------------------------------ the search rule (design section 3)
_BOUNDS = np.array([15*k*(k + 1) for k in range(1, 400)])        # leg k spans u in [15 k (k - 1), 15 k (k + 1)): 30, 90, 180, 300, 450, 630, ...
def leg_of(u): return np.searchsorted(_BOUNDS, np.asarray(u), side="right") + 1
def slant_of(u): return np.where(np.mod(u, 2*U1) < U1, 1.0, -1.0)
def search_target(u, cast_sign):
    k = leg_of(u); sig = cast_sign*np.where(k % 2 == 1, 1.0, -1.0)
    return (UPWIND + sig*(90.0 - slant_of(u)*GAMMA)) % 360.0


class Search:
    """H17 search mode, wrapped around the adopted act. search=False: the base act, untouched."""

    def __init__(self, *a, search=True, **kw):
        super().__init__(*a, **kw); self.search = search; n = self.R
        self.q = np.zeros(n); self.engaged = np.zeros(n, bool); self.u = np.full(n, -1.0); self.leg = np.zeros(n, int)
        self.tgt_base = np.zeros(n); self.nz_base = np.zeros(n); self.nz = np.zeros(n)

    def act(self, w, whiffs, wind_on):
        if not self.search: return super().act(w, whiffs, wind_on)
        turn, h = super().act(w, whiffs, wind_on)
        self.q = np.where(whiffs.any(1), 0.0, self.q + 1.0)
        eng = (self.q >= S_ON) & (h < 0)
        self.engaged = eng; self.tgt_base = np.array(self.tgt, float, copy=True)
        self.u = np.where(eng, self.q - S_ON, -1.0); self.leg = np.where(eng, leg_of(np.maximum(self.u, 0.0)), 0)
        self.nz_base = self.nz = np.zeros(self.R)
        if eng.any():
            est = self.est; ts = search_target(np.maximum(self.u, 0.0), self.cast_sign)
            nz = turn - np.clip(GAIN*angdiff(self.tgt_base, est), -MAXTURN, MAXTURN)          # the base's noise sample, recovered
            new = np.clip(GAIN*angdiff(ts, est), -MAXTURN, MAXTURN) + nz
            turn = np.where(eng, new, turn); self.tgt = np.where(eng, ts, self.tgt); self.last_turn = turn
            self.nz_base = np.where(eng, nz, 0.0); self.nz = np.where(eng, turn - np.clip(GAIN*angdiff(self.tgt, est), -MAXTURN, MAXTURN), 0.0)
        return turn, h


class Agent12(Search, Agent10): """H17: the search mode on the adopted agent (Agent10 = Release + Agent8)"""
class Agent12g(Search, Agent10g): """H17: the search mode on the H21 gate agent + H25 (Agent10g = Release + Agent6); reported"""


def region_near(pos, src):
    """nearest whiff region of either source: (inside any, distance, target point). Inside a region: that region's source (reading R3)."""
    n = len(pos); best_d = np.full(n, np.inf); best_p = np.zeros((n, 2)); inside = np.zeros(n, bool); in_src = np.zeros((n, 2))
    P = np.array([[0.0, -W0], [LMAX, -(W0 + SLOPE*LMAX)], [LMAX, W0 + SLOPE*LMAX], [0.0, W0]])
    for k in (0, 1):
        s = src[:, k]; p = pos - s; ins, _ = cone_geom(p[:, 0], p[:, 1])
        in_src = np.where((ins & ~inside)[:, None], s, in_src); inside |= ins
        for i in range(4):
            a, b = P[i], P[(i + 1) % 4]; ab = b - a; t = np.clip(((p - a) @ ab)/(ab @ ab), 0.0, 1.0); c = a + t[:, None]*ab
            d = np.linalg.norm(p - c, axis=1); m = d < best_d; best_d = np.where(m, d, best_d); best_p = np.where(m[:, None], s + c, best_p)
        r = np.maximum(np.linalg.norm(p, axis=1), 1e-12); c = p*(3.0/r)[:, None]; d = np.maximum(r - 3.0, 0.0)
        m = d < best_d; best_d = np.where(m, d, best_d); best_p = np.where(m[:, None], s + c, best_p)
    return inside, np.where(inside, 0.0, best_d), np.where(inside[:, None], in_src, best_p)


class Oracle:
    """bench (c) ceiling (a ceiling arm only, like known-answer): until the row's first whiff, steer to the nearest whiff region (reading R3)"""

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw); self.found = np.zeros(self.R, bool)

    def act(self, w, whiffs, wind_on):
        turn, h = super().act(w, whiffs, wind_on)
        self.found = self.found | whiffs.any(1); m = ~self.found
        if m.any():
            _, _, pt = region_near(w.pos, w.src); d = pt - w.pos; to = np.degrees(np.arctan2(d[:, 1], d[:, 0])) % 360.0
            nz = turn - np.clip(GAIN*angdiff(self.tgt, self.est), -MAXTURN, MAXTURN)
            new = np.clip(GAIN*angdiff(to, self.est), -MAXTURN, MAXTURN) + nz
            turn = np.where(m, new, turn); self.tgt = np.where(m, to, self.tgt); self.last_turn = turn
        return turn, h


class AgentO(Oracle, Agent10): """bench (c) ceiling: the oracle bearing, then Agent10"""


# ------------------------------------------------------------------ hooks (run time; ph24 is not edited)
_make24, _record24 = ph24.make, ph24.record
_SEARCH = [True]


def make(cls, runs, rng, G, known, gate=True, filt=True, release=True):
    if cls in (Agent12, AgentO): kw = dict(rule=gate, filt=filt, release=release)
    elif cls is Agent12g: kw = dict(rule=gate, release=release)
    else: return _make24(cls, runs, rng, G, known, gate, filt, release)
    if cls is not AgentO: kw["search"] = _SEARCH[0]
    return cls(runs, rng, G=G, known=known, **kw)


def record(o, t, a, h, x, pa):
    """ph24.record, plus the search fields; every other field untouched"""
    _record24(o, t, a, h, x, pa)
    st, n = o["H"].shape
    if "Q" not in o:
        o.update(Q=np.full((st, n), -1.0), ENG=np.zeros((st, n), bool), U=np.full((st, n), -1.0), LEG=np.zeros((st, n), int), CS=np.zeros((st, n)),
                 TGTB=np.zeros((st, n)), NZB=np.zeros((st, n)), NZ=np.zeros((st, n)), SRCH=False)
    o["CS"][t] = a.cast_sign
    if isinstance(a, Search) and a.search:
        o["SRCH"] = True; o["Q"][t] = a.q; o["ENG"][t] = a.engaged; o["U"][t] = a.u; o["LEG"][t] = a.leg
        o["TGTB"][t] = a.tgt_base; o["NZB"][t] = a.nz_base; o["NZ"][t] = a.nz
    else: o["TGTB"][t] = getattr(a, "tgt", 0.0)


ph24.make, ph24.record = make, record


def run(world, cls, vals, seeds, search=True, **kw):
    _SEARCH[0] = search
    try: return ph24.run(world, cls, vals, seeds, **kw)
    finally: _SEARCH[0] = True


def stub(cls, known, sched, search=True, **kw):
    kw.setdefault("seeds", BS); _SEARCH[0] = search                # ph24.stub's default seeds are H25's bench seeds
    try: return ph24.stub(cls, known, sched, **kw)
    finally: _SEARCH[0] = True


# ------------------------------------------------------------------ the cold-start constructions (bench (c))
def construct(w, klass):
    """design section 4 (c): positions and headings drawn from the world generator after World7's draw (reading R4)"""
    n = w.R; r = np.arange(n); x = w.src[:, 0, 0]; yc = w.src[:, :, 1].mean(1); g = w.rng
    if klass == "c1":
        k = g.integers(0, 2, n); da = g.uniform(5.0, 14.0, n); dc = g.uniform(26.0, 31.0, n)
        out = np.sign(w.src[r, k, 1] - w.src[r, 1 - k, 1]); w.pos = np.stack([x + da, w.src[r, k, 1] + out*dc], 1); meta = dict(k=k, da=da, dc=dc, out=out)
    elif klass == "c2":
        da = g.uniform(-60.0, -20.0, n); dy = g.uniform(-10.0, 10.0, n); w.pos = np.stack([x + da, yc + dy], 1); meta = dict(da=da, dy=dy)
    else:
        w.pos = np.stack([g.uniform(x - 11.0, x + 29.0), yc + g.uniform(-20.0, 20.0, n)], 1)
        while (bad := inside(w.pos, w.src)).any(): w.pos[bad] = np.stack([g.uniform(x[bad] - 11.0, x[bad] + 29.0), yc[bad] + g.uniform(-20.0, 20.0, int(bad.sum()))], 1)
        meta = {}
    w.head = g.uniform(0.0, 360.0, n)
    return meta


def inside(pos, src):
    ins = np.zeros(len(pos), bool)
    for k in (0, 1): i, _ = cone_geom(pos[:, 0] - src[:, k, 0], pos[:, 1] - src[:, k, 1]); ins |= i
    return ins


def cold(klass, cls, walls, seeds=BS, runs=BENCH["rows"], steps=None):
    steps = steps or BENCH[f"steps_{klass}"]; q0 = {"c1": BENCH["q_c1"], "c2": S_ON, "c3": 0}[klass]
    w = World7(runs, np.random.default_rng(seeds[0]), seeds[0]); meta = construct(w, klass)
    if not walls: w.walls = False
    a = make(cls, runs, np.random.default_rng(seeds[1]), G_STAR, np.zeros((runs, 2)))
    a.cast_sign = cast_draw(seeds[1], runs); a.since[:] = float(q0)
    if isinstance(a, Search): a.q[:] = float(q0)
    o = dict(world=klass, arm=type(a).__name__, src=w.src.copy(), start=w.pos.copy(), head0=w.head.copy(), meta=meta, steps=steps, walls=walls, **ph24.blank(steps, runs),
             POS=np.zeros((steps, runs, 2)), HEAD=np.zeros((steps, runs)), AT2=np.zeros((steps, runs, 2), bool), C=np.zeros((steps, runs), bool))
    for t in range(steps):
        pa = (a.sel.s > 1.0).any(1); x = w.sense(); on = w.wind_on()
        turn, h = a.act(w, x, on); record(o, t, a, h, x, pa)
        w.move(turn); a.bump(w.bumped)
        o["POS"][t] = w.pos; o["HEAD"][t] = w.head; o["AT2"][t] = w.at_source(); o["C"][t] = w.bumped
    o["contacts"] = o["C"].sum(0).astype(float)
    return o


# ------------------------------------------------------------------ measures
FIELDS = ph24.FIELDS + ("SIL", "TO", "EV")
def roweq(o1, o2, ks=FIELDS):
    st, n = o1["H"].shape; eq = np.ones((st, n), bool)
    for k in ks:
        e = o1[k] == o2[k]; eq &= e.reshape(st, n, -1).all(2)
    return eq


def row_identity(o, ob):
    """never-engaged rows bitwise the base on every field and step; engaged rows bitwise the base on every step before their first engaged step"""
    eq = roweq(o, ob); st = eq.shape[0]; fe = first_true(o["ENG"]); nev = fe < 0
    before = np.arange(st)[:, None] < np.where(nev, st, fe)[None, :]
    ok = bool((eq | ~before).all()); whole = eq.all(0)
    return ok, dict(never_engaged=int(nev.sum()), never_equal=int((nev & whole).sum()), engaged=int((~nev).sum()),
                    engaged_equal_before=int((~nev & (eq | ~before).all(0)).sum()), first_engaged_step=q3(fe[~nev]))


def qrec(W, q0=0.0):
    """the counter's recursion from the recorded whiffs: q_t = 0 if any whiff at t, else q_{t-1} + 1; q_{-1} = q0"""
    any_ = W.any(2); Q = np.zeros(any_.shape); q = np.full(any_.shape[1], float(q0))
    for t in range(any_.shape[0]): q = np.where(any_[t], 0.0, q + 1.0); Q[t] = q
    return Q


def engagement_exact(o, q0=0.0):
    """per row: q, engaged, u, leg, slant and the target equal the rule on every step; the base target kept on every other step; the same noise sample"""
    Q = qrec(o["W"], q0); E = (Q >= S_ON) & (o["H"] < 0); U = np.where(E, Q - S_ON, -1.0); Lg = np.where(E, leg_of(np.maximum(U, 0.0)), 0)
    TS = search_target(np.maximum(U, 0.0), o["CS"])
    ok = (o["Q"] == Q).all(0) & (o["ENG"] == E).all(0) & (o["U"] == U).all(0) & (o["LEG"] == Lg).all(0)
    ok &= np.where(E, o["TGT"] == TS, o["TGT"] == o["TGTB"]).all(0)
    ok &= (np.abs(o["NZ"] - o["NZB"]) <= 1e-9).all(0)
    held_q = ((Q >= S_ON) & (o["H"] >= 0)).sum()
    return ok, int(held_q)


def lost(o): return ~o["W"][-T//3:].any((0, 2))
def cls3(o): return np.select(list(majority(o)), [0, 1, 2])
def Phi(x): return 0.5*(1.0 + math.erf(x/math.sqrt(2.0)))


def pp_dp(a, b, bar, most):
    """reading R6: section 7's pass probability for a paired DP of 0/1 indicators; returns (P, DP, discordant b, sd, P with the measured sd)"""
    d = a.astype(float) - b.astype(float); n = len(d); dp = float(d.mean()); disc = float((d != 0).mean()); var = disc - dp*dp
    def p_of(sd):
        if sd <= 0: return float(dp <= bar) if most else float(dp >= bar)
        se = sd/math.sqrt(n); return Phi(((bar - dp) if most else (dp - bar))/se - Z95)
    return p_of(math.sqrt(max(var, 0.0))), dp, disc, math.sqrt(max(var, 0.0)), p_of(float(np.std(d)))


def pp_prop(p, theta, most, n=400):
    se = math.sqrt(p*(1 - p)/n) if 0 < p < 1 else 0.0
    if se == 0: return float(p <= theta) if most else float(p >= theta)
    return Phi(((theta - p) if most else (p - theta))/se - Z95)


def rel_pos(o, t, r):
    """position sensed at step t (after step t - 1's move), relative to the start's source (c1): d_along, d_cross signed outward"""
    pos = o["POS"][t - 1, r] if t > 0 else o["start"][r]; m = o["meta"]; k = m["k"][r]
    return pos[0] - o["src"][r, k, 0], (pos[1] - o["src"][r, k, 1])*m["out"][r]


def fmt_ci(k, n, pt, lo, hi): return f"{k}/{n} = {pt:.3f} [{lo:.3f}, {hi:.3f}]"


# ------------------------------------------------------------------ the mechanism bench (design section 4)
def bench(say=print):
    n = BENCH["rows"]; p = 0.30; kn = [1.0, 0.0]; ids = {}; bars = {}; out = {}
    say(f"== H17 mechanism bench (design v2 section 4). design {DESIGN}; {BENCH}; S {S_ON}, L0 {L0}, gamma {GAMMA}, U1 {U1}; bootstrap seed {ph15.BOOT_SEED} ==")
    header(say)
    say("   readings where the design is silent (see the file header R1-R7): R1 q updated at the top of each act (silence from construction: first engaged step index 209,"
        " the 210th step; (c1) q = since = 45 at construction: engagement at step index 164, the 165th step; window (i) indices 164-463, window (ii) indices 164-763,"
        " run 765 steps); R2 (c2) q = since = S at construction (first step engaged, u = 1); R3 oracle: nearest point of the nearest whiff region, inside a region its"
        " source, until the first whiff, same noise sample; R4 constructions drawn from the world generator after World7's draw, walls off = `walls` False;"
        " R5 (b) whiffs on channel 0, (d) stub 600 steps both channels; R6 pass probability b = discordant fraction, sd = sqrt(b - DP^2); R7 reach = within 3.0 after the move")
    both = [(BENCH["steps_stub"], p, p)]
    # (a1) search False == base
    ids["a1 stub Agent12 off == Agent10"] = bitwise(stub(Agent12, kn, both, search=False), stub(Agent10, kn, both))
    ids["a1 stub Agent12g off == Agent10g"] = bitwise(stub(Agent12g, kn, both, search=False), stub(Agent10g, kn, both))
    T1 = {(k, v): run("T1", c, v, BS) for v in ((1.0, 0.0), (1.0, -1.0)) for k, c in (("Agent12", Agent12), ("Agent10", Agent10))}
    ids["a1 World7 Agent12 off == Agent10"] = bitwise(run("T1", Agent12, (1.0, 0.0), BS, search=False), T1[("Agent10", (1.0, 0.0))])
    ids["a1 World7 Agent12g off == Agent10g"] = bitwise(run("T1", Agent12g, (1.0, 0.0), BS, search=False), run("T1", Agent10g, (1.0, 0.0), BS))
    say(f"(a1) search False == the base bitwise (H, s, S, nav, since, silence, target, positions, headings, timeout/evidence flags): stub both channels p {p} {BENCH['steps_stub']} steps:"
        f" Agent12 == Agent10 {ids['a1 stub Agent12 off == Agent10']}, Agent12g == Agent10g {ids['a1 stub Agent12g off == Agent10g']}; World7 +1/0 {n} x {BENCH['steps']}:"
        f" Agent12 == Agent10 {ids['a1 World7 Agent12 off == Agent10']}, Agent12g == Agent10g {ids['a1 World7 Agent12g off == Agent10g']}")
    # (a2) never-engaged rows
    sp = stub(Agent12, kn, both); ids["a2 stub == Agent10 (never engaged)"] = bitwise(sp, stub(Agent10, kn, both)) and not sp["ENG"].any()
    say(f"(a2) search True, stub both channels p {p}: == Agent10 bitwise and never engaged {ids['a2 stub == Agent10 (never engaged)']} (engaged (row, step) {int(sp['ENG'].sum())})")
    for v in ((1.0, 0.0), (1.0, -1.0)):
        ok, cnt = row_identity(T1[("Agent12", v)], T1[("Agent10", v)]); ids[f"a2 World7 {v}"] = ok
        say(f"(a2) World7 {v[0]:+.0f}/{v[1]:+.0f} {n} x {BENCH['steps']}: never-engaged rows bitwise Agent10, engaged rows equal before their first engaged step: {ok} {cnt}")
    WT = {}
    for wd in ("W1", "T3a"):
        WT[wd] = (run(wd, Agent12, (1.0, 0.0), BS), run(wd, Agent10, (1.0, 0.0), BS)); ok, cnt = row_identity(*WT[wd]); ids[f"a2 {wd}"] = ok
        say(f"(a2) {wd} {n} x {BENCH['steps']}: {ok} {cnt}; masked draws == the World7 twin {WT[wd][0]['draws_equal'] and WT[wd][0]['rng_equal']}")
    # (a3) chains
    for v in ((0.0, 0.0), (1.0, 1.0), (1.0, -1.0)):
        b10 = T1[("Agent10", v)] if v in ((1.0, -1.0),) else run("T1", Agent10, v, BS); off = bitwise(run("T1", Agent12, v, BS, search=False), b10)
        on_ = T1[("Agent12", v)] if v == (1.0, -1.0) else run("T1", Agent12, v, BS); ok, cnt = row_identity(on_, b10)
        s_off = bitwise(stub(Agent12, list(v), both, search=False), stub(Agent10, list(v), both)); s_on = bitwise(stub(Agent12, list(v), both), stub(Agent10, list(v), both))
        ids[f"a3 {v}"] = off and ok and s_off and s_on
        say(f"(a3) chain {v[0]:+.0f}/{v[1]:+.0f}: search False == Agent10 World7 {off}, stub {s_off}; search True stub == Agent10 {s_on}; World7 never-engaged rows bitwise {ok} {cnt}")
    # (b) engagement exact
    sch = {"one whiff at step 0 then silence": [(1, 1.0, 0.0), (BENCH["steps_b"] - 1, 0.0, 0.0)], "a 20-step p 0.30 burst then silence": [(20, p, 0.0), (BENCH["steps_b"] - 20, 0.0, 0.0)],
           "silence from construction": [(BENCH["steps_b"], 0.0, 0.0)]}
    okb = np.ones(n, bool); hq = 0
    for k, s in sch.items():
        o = stub(Agent12, kn, s); ex, held_q = engagement_exact(o); okb &= ex; hq += held_q
        fe = first_true(o["ENG"]); anyw = o["W"].any(2); lastw = np.where(anyw.any(0), o["H"].shape[0] - 1 - np.argmax(anyw[::-1], 0), -1)
        rel = np.where(lastw >= 0, fe - lastw, fe); fh = first_true(o["H"] >= 0)
        hold_end = np.where(fh >= 0, first_true((o["H"] < 0) & (np.arange(o["H"].shape[0])[:, None] > fh[None, :])), -1)
        ul = o["U"][o["ENG"]]; bl = [int(u) for u in (30, 90, 180, 300, 450) if (ul == u).any()]
        say(f"(b) {k}: rows exact {int(ex.sum())}/{n}; first engaged step index {q3(fe[fe >= 0])} (never {int((fe < 0).sum())}); first engaged step - last whiff step {q3(rel[fe >= 0])}"
            f" (rows with a whiff {int((lastw >= 0).sum())}); engaged until the run's end in {int(o['ENG'][-1].sum())} rows; hold formed {int((fh >= 0).sum())} rows, ended at step"
            f" {q3(hold_end[hold_end >= 0])}; q >= S with a hold (row, step) {held_q}; u max {int(ul.max()) if len(ul) else -1}, leg boundaries crossed {bl}; legs seen {sorted(set(o['LEG'][o['ENG']].tolist()))};"
            f" slant -1 steps {int((o['ENG'] & (slant_of(np.maximum(o['U'], 0)) < 0)).sum())}")
    k_, pt, lo, hi = interval("P", okb); bars["b"] = lo
    say(f"(b) engagement exact in every schedule (q recursion, engaged = q >= S and nothing held, u, leg, slant, the target = the search target on engaged steps and the base's"
        f" target on every other, the same noise sample): {fmt_ci(k_, n, pt, lo, hi)} (bar lower bound >= 0.95) -> {'PASS' if lo >= 0.95 else 'FAIL'}; q >= S with a hold, all schedules: {hq} (expected 0)")
    # (c) cold start
    say(f"(c) cold start, values 0/0, nothing held, {n} rows per class and wall setting; arms floor Agent10, Agent12, ceiling oracle (reading R3); walls OFF is the primary reading")
    C = {}
    for klass in ("c1", "c2", "c3"):
        for walls in (False, True):
            for k, c in (("Agent10", Agent10), ("Agent12", Agent12), ("oracle", AgentO)): C[(klass, walls, k)] = cold(klass, c, walls)
    ids["c constructions equal across arms and wall settings"] = all(np.array_equal(C[(kl, wl, k)]["start"], C[(kl, False, "Agent10")]["start"])
                                                                   for kl in ("c1", "c2", "c3") for wl in (False, True) for k in ("Agent10", "Agent12", "oracle"))
    o0 = C[("c1", False, "Agent10")]; ins0 = inside(o0["start"], o0["src"]); m = o0["meta"]
    geo_ok = bool(not ins0.any() and (m["da"] >= 5).all() and (m["da"] <= 14).all() and (m["dc"] >= 26).all() and (m["dc"] <= 31).all())
    ids["c1 start outside both regions, d_along [5, 14], |d_cross| [26, 31] outer side"] = geo_ok
    c3in = any(inside(C[("c3", False, "Agent10")]["start"], C[("c3", False, "Agent10")]["src"]))
    ids["c3 start outside both regions"] = not c3in
    say(f"   constructions identical across arms and wall settings {ids['c constructions equal across arms and wall settings']}; (c1) start outside both whiff regions, d_along in [5, 14],"
        f" |d_cross| in [26, 31] on the outer side: {geo_ok} (d_along {q3f(m['da'])}, |d_cross| {q3f(m['dc'])}, source index 0/1 {np.bincount(m['k'], minlength=2).tolist()});"
        f" (c3) starts outside both regions {not c3in}")
    e = 164; W1_, W2_ = slice(e, e + 300), slice(e, e + 600)
    res = {}
    for walls in (False, True):
        lab = "walls OFF (primary)" if not walls else "walls ON (reported)"
        o10, o12, oo = (C[("c1", walls, k)] for k in ("Agent10", "Agent12", "oracle"))
        wi = {k: o["W"][W1_].any((0, 2)) for k, o in (("Agent10", o10), ("Agent12", o12), ("oracle", oo))}
        re = {k: o["AT2"][W2_].any((0, 2)) for k, o in (("Agent10", o10), ("Agent12", o12), ("oracle", oo))}
        pre = {k: o["W"][:e].any((0, 2)) for k, o in (("Agent10", o10), ("Agent12", o12), ("oracle", oo))}
        eng = o12["ENG"][e]; fe = first_true(o12["ENG"])
        say(f"   (c1) R3 stranded state, {lab}, {BENCH['steps_c1']} steps; Agent12 engaged at step index {e} in {int(eng.sum())}/{n} rows (first engaged step {q3(fe[fe >= 0])},"
            f" never {int((fe < 0).sum())}); any whiff before the engagement step: Agent10 {int(pre['Agent10'].sum())}, Agent12 {int(pre['Agent12'].sum())}, oracle {int(pre['oracle'].sum())}")
        for k in ("Agent10", "Agent12", "oracle"):
            o = C[("c1", walls, k)]; k1, p1, l1, h1 = interval("P", wi[k]); k2, p2, l2, h2 = interval("P", re[k]); fw = first_true(o["W"].any(2)); fa = first_true(o["AT2"].any(2))
            say(f"      [{k}] (i) any whiff in the 300 steps from the engagement step {fmt_ci(k1, n, p1, l1, h1)}; (ii) a source reached in the 600 steps from it {fmt_ci(k2, n, p2, l2, h2)};"
                f" first whiff step {q3(fw[fw >= 0])} (rows {int((fw >= 0).sum())}); first reach step {q3(fa[fa >= 0])} (rows {int((fa >= 0).sum())}); ever reached by {BENCH['steps_c1']}"
                f" {int((fa >= 0).sum())}; wall contacts per row {o['contacts'].mean():.3f}; engaged (row, step) {int(o['ENG'].sum())}")
            res[(walls, k)] = (wi[k], re[k], l1, l2)
        _, dp, dlo, dhi = interval("DP", wi["Agent12"].astype(float), wi["Agent10"].astype(float))
        _, dpr, drlo, drhi = interval("DP", re["Agent12"].astype(float), re["Agent10"].astype(float))
        say(f"      paired DP (i) Agent12 - Agent10 {dp:+.4f} [{dlo:+.4f}, {dhi:+.4f}]; paired DP (ii) {dpr:+.4f} [{drlo:+.4f}, {drhi:+.4f}] (bootstrap 5000, seed {ph15.BOOT_SEED})")
        rr = np.flatnonzero(eng)
        if len(rr):
            ep = np.array([rel_pos(o12, e, r) for r in rr]); insd = inside(o12["POS"][e - 1, rr], o12["src"][rr])
            _, dist, _ = region_near(o12["POS"][e - 1, rr], o12["src"][rr])
            say(f"      engagement position (Agent12, the position step {e} sensed at, relative to the start's source): d_along {q3f(ep[:, 0])} (min {ep[:, 0].min():.1f}, max {ep[:, 0].max():.1f};"
                f" beyond LMAX 25 {int((ep[:, 0] > LMAX).sum())}, upwind of the source {int((ep[:, 0] < 0).sum())}), d_cross outward {q3f(ep[:, 1])} (min {ep[:, 1].min():.1f}, max {ep[:, 1].max():.1f});"
                f" inside a whiff region {int(insd.sum())}; distance to the nearest region {q3f(dist)}; start d_along {q3f(m['da'][rr])}, |d_cross| {q3f(m['dc'][rr])}")
        if not walls:
            bars["c1 (i) whiff within 300, Agent12 (>= 0.40)"] = res[(False, "Agent12")][2]; bars["c1 (ii) reach within 600, Agent12 (>= 0.30)"] = res[(False, "Agent12")][3]
            bars["c1 (iii) paired DP (i) Agent12 - Agent10 (>= +0.30)"] = dlo; out.update(c1_i=float(wi["Agent12"].mean()), c1_ii=float(re["Agent12"].mean()), c1_dp=dp, c1_dplo=dlo)
            say(f"   (c1) BARS, walls off: (i) lower bound {res[(False, 'Agent12')][2]:.4f} >= 0.40 -> {'PASS' if res[(False, 'Agent12')][2] >= 0.40 else 'FAIL'};"
                f" (ii) lower bound {res[(False, 'Agent12')][3]:.4f} >= 0.30 -> {'PASS' if res[(False, 'Agent12')][3] >= 0.30 else 'FAIL'};"
                f" (iii) lower bound {dlo:+.4f} >= +0.30 -> {'PASS' if dlo >= 0.30 else 'FAIL'}; floor (Agent10) (i) {wi['Agent10'].mean():.3f}; ceiling (oracle) (i) {wi['oracle'].mean():.3f}, (ii) {re['oracle'].mean():.3f}")
    for klass, wins in (("c2", (300, 600)), ("c3", (600, 1800))):
        for walls in (False, True):
            parts = []
            for k in ("Agent10", "Agent12", "oracle"):
                o = C[(klass, walls, k)]; wv = [int(o["W"][:t].any((0, 2)).sum()) for t in wins]; rv = [int(o["AT2"][:t].any((0, 2)).sum()) for t in wins]
                parts.append(f"{k}: whiff by {wins[0]}/{wins[1]} {wv[0]}/{wv[1]}, reached by {wins[0]}/{wins[1]} {rv[0]}/{rv[1]} (= {rv[0]/n:.3f}/{rv[1]/n:.3f}), contacts per row {o['contacts'].mean():.3f},"
                             f" engaged rows {int(o['ENG'].any(0).sum())}")
            say(f"   ({klass}) {'upwind of the sources' if klass == 'c2' else 'the H16 cold-start square'}, {'walls OFF' if not walls else 'walls ON'}, {BENCH['steps_' + klass]} steps, REPORTED: " + "; ".join(parts))
    # (d) no false engagement
    say(f"(d) no false engagement: any-odour silence (q from the recorded whiffs) for Agent10, and Agent12's engaged rows")
    for lab, o in (("World7 +1/0 Agent10", T1[("Agent10", (1.0, 0.0))]), ("World7 +1/-1 Agent10", T1[("Agent10", (1.0, -1.0))]),
                   ("stub p 0.057 Agent10", stub(Agent10, kn, [(BENCH["steps"], 0.057, 0.057)])), ("stub p 0.30 Agent10", stub(Agent10, kn, [(BENCH["steps"], 0.30, 0.30)]))):
        Q = qrec(o["W"]); mx = Q.max(0)
        say(f"   [{lab}] longest any-odour silence per row: quartiles {q3(mx)}, p90 {np.percentile(mx, 90):.0f}, max {mx.max():.0f}; rows reaching q >= {S_ON} {int((mx >= S_ON).sum())};"
            f" fraction of (row, step) with q >= 150/180/210/250: " + "/".join(f"{(Q >= c).mean():.5f}" for c in (150, 180, 210, 250)))
    for lab, v in (("+1/0", (1.0, 0.0)), ("+1/-1", (1.0, -1.0))):
        o = T1[("Agent12", v)]; er = o["ENG"].any(0); k_, pt, lo, hi = interval("P", er)
        say(f"   [World7 {lab} Agent12] rows with any engaged step {fmt_ci(k_, n, pt, lo, hi)}; engaged (row, step) {int(o['ENG'].sum())}; first engaged step {q3(first_true(o['ENG'])[er])}"
            + (f" -> bar upper bound <= 0.05: {'PASS' if hi <= 0.05 else 'FAIL'} (pass probability at the point, section 7: {pp_prop(pt, 0.05, True):.4f})" if v == (1.0, 0.0) else " (reported)"))
        if v == (1.0, 0.0): bars["d engaged rows T1 +1/0 (upper <= 0.05)"] = hi; out["d_hi"] = hi
    for pp_ in (0.057, 0.30):
        o = stub(Agent12, kn, [(BENCH["steps"], pp_, pp_)]); say(f"   [stub p {pp_} Agent12] engaged (row, step) {int(o['ENG'].sum())}; == Agent10 bitwise {bitwise(o, stub(Agent10, kn, [(BENCH['steps'], pp_, pp_)]))}")
    # (h1) T1 on bench seeds
    o12, o10 = T1[("Agent12", (1.0, 0.0))], T1[("Agent10", (1.0, 0.0))]; V12, V10 = majority(o12)[0], majority(o10)[0]; c12, c10 = cls3(o12), cls3(o10)
    P1, dp1, b1, sd1, P1m = pp_dp(V12, V10, -0.05, False); _, _, blo, bhi = interval("DP", V12.astype(float), V10.astype(float)); stop1 = P1 < 0.5
    e_ = o12["ENG"].any(0); l12, l10 = lost(o12), lost(o10)
    say(f"(h1) T1 on bench seeds, World7 +1/0 {n} x {BENCH['steps']}: " + "; ".join(f"{k} V {int(majority(o)[0].sum())} N {int(majority(o)[1].sum())} tie {int(majority(o)[2].sum())} P(V) "
        f"{interval('P', majority(o)[0])[1]:.3f} [{interval('P', majority(o)[0])[2]:.3f}, {interval('P', majority(o)[0])[3]:.3f}]" for k, o in (("Agent12", o12), ("Agent10", o10))))
    say(f"   (h1) paired DP P(V) Agent12 - Agent10 {dp1:+.4f} [{blo:+.4f}, {bhi:+.4f}] (bootstrap 5000, seed {ph15.BOOT_SEED}); engaged rows {int(e_.sum())}; into V {int(((c12 == 0) & (c10 != 0)).sum())},"
        f" out of V {int(((c12 != 0) & (c10 == 0)).sum())}; V among engaged rows Agent12 {int(V12[e_].sum())} vs Agent10 {int(V10[e_].sum())}; lost rows {int(l12.sum())} vs {int(l10.sum())};"
        f" contacts per row {o12['contacts'].mean():.3f} vs {o10['contacts'].mean():.3f}")
    say(f"   (h1) T1 (b)'s pass probability (lower bound >= -0.05) at the bench DP {dp1:+.4f}, discordant b {b1:.4f}, sd sqrt(b - DP^2) {sd1:.4f}: {P1:.4f} (with the measured paired sd: {P1m:.4f})")
    say(f"   (h1) STOP RULE (design v2 section 4 / section 12 point 4): pass probability {P1:.4f} {'< 0.5 -> STOP: the run returns to the owner after the bench record' if stop1 else '>= 0.5 -> continue'}")
    # (h2) T3 on bench seeds
    o12, o10 = T1[("Agent12", (1.0, -1.0))], T1[("Agent10", (1.0, -1.0))]; V12, V10 = majority(o12)[0], majority(o10)[0]; l12, l10 = lost(o12), lost(o10)
    P2, dp2, b2, sd2, P2m = pp_dp(l12, l10, -0.05, True); _, _, llo, lhi = interval("DP", l12.astype(float), l10.astype(float)); stop2 = P2 < 0.5
    Pb, dpv, bv, sdv, Pbm = pp_dp(V12, V10, -0.02, False); _, _, vlo, vhi = interval("DP", V12.astype(float), V10.astype(float))
    cm = o12["contacts"].mean(); e_ = o12["ENG"].any(0)
    _, r10, _ = released(o10); _, r12, _ = released(o12); s10, s12 = np.unique(r10), np.unique(r12)
    say(f"(h2) T3 on bench seeds, World7 +1/-1 {n} x {BENCH['steps']}: " + "; ".join(f"{k} V {int(majority(o)[0].sum())} N {int(majority(o)[1].sum())} tie {int(majority(o)[2].sum())},"
        f" lost rows {int(lost(o).sum())}, contacts per row {o['contacts'].mean():.3f}" for k, o in (("Agent12", o12), ("Agent10", o10))))
    say(f"   (h2) stranded rows (a drive-ended negative hold, as R3): Agent10 {len(s10)} (releases {len(r10)}), Agent12 {len(s12)}; Agent12 engaged rows {int(e_.sum())}, engaged (row, step) {int(o12['ENG'].sum())};"
        f" lost among Agent10's stranded rows: Agent10 {int(l10[s10].sum())}, Agent12 {int(l12[s10].sum())}")
    say(f"   (h2) lost-row paired DP Agent12 - Agent10 {dp2:+.4f} [{llo:+.4f}, {lhi:+.4f}]; P(V) paired DP {dpv:+.4f} [{vlo:+.4f}, {vhi:+.4f}]; contacts per row {cm:.3f}")
    say(f"   (h2) T3 (a)'s pass probability (upper bound <= -0.05) at the bench DP {dp2:+.4f}, discordant b {b2:.4f}, sd {sd2:.4f}: {P2:.4f} (measured paired sd: {P2m:.4f});"
        f" reported: T3 (b) (lower bound >= -0.02) at {dpv:+.4f}, b {bv:.4f}: {Pb:.4f} (measured sd: {Pbm:.4f}); T3 (c) contacts {cm:.3f} <= 0.10 at the point: {cm <= 0.10}")
    say(f"   (h2) STOP RULE (design v2 section 4 / section 12 point 4): pass probability {P2:.4f} {'< 0.5 -> STOP: the run returns to the owner after the bench record' if stop2 else '>= 0.5 -> continue'}")
    out.update(h1_dp=dp1, h1_pp=P1, h2_dp=dp2, h2_pp=P2, stop1=stop1, stop2=stop2)
    # verdict
    idok = all(ids.values())
    cb = {k: v for k, v in bars.items() if k.startswith("c1")}
    cok = cb["c1 (i) whiff within 300, Agent12 (>= 0.40)"] >= 0.40 and cb["c1 (ii) reach within 600, Agent12 (>= 0.30)"] >= 0.30 and cb["c1 (iii) paired DP (i) Agent12 - Agent10 (>= +0.30)"] >= 0.30
    bok, dok = bars["b"] >= 0.95, bars["d engaged rows T1 +1/0 (upper <= 0.05)"] <= 0.05
    cand = idok and bok and cok and dok; B = cand and not stop1 and not stop2
    out.update(ids=idok, b=bok, c1=cok, d=dok, cand=cand, B=B)
    say(f"== B: (a) identities {idok} (failed {[k for k, v in ids.items() if not v]}); (b) exact {bok} (lower bound {bars['b']:.4f}); (c1) bars {cok} "
        + str({k: round(float(v), 4) for k, v in cb.items()}) + f"; (d) {dok} (upper bound {bars['d engaged rows T1 +1/0 (upper <= 0.05)']:.4f}); stop rules (h1) {'STOP' if stop1 else 'continue'} ({P1:.4f}),"
        f" (h2) {'STOP' if stop2 else 'continue'} ({P2:.4f}) -> B {'PASS: the tasks may be run' if B else ('FAIL, NO CANDIDATE: the search as specified does not do what section 3 says (or (d) fails); the tasks are NOT run' if not cand else 'NOT passed: a registered stop rule fired; the tasks are NOT run and the run returns to the owner')} ==")
    return B, out


# ------------------------------------------------------------------ self-checks
def seeds_unused():
    """design section 9 (1): none of the fifteen numbers appears in any other file under the repository (recursive, digit-boundary; .git and __pycache__
    excluded; excluded by name: this file, its outputs ph26_*.txt, the H17 documents h17_*.md, master_plan.md, notes/*.md, viewer/*). The demo seeds 5/6 are
    used deliberately and are NOT part of this check; no reproduction seed is used."""
    base = [*SEEDS["dev"], *SEEDS["eval"], BENCH["seed_w"], BENCH["seed_a"], ph15.BOOT_SEED]
    derived = [s + 10_000 for s in (SEEDS["dev"][0], SEEDS["eval"][0], BENCH["seed_w"])] + [s + 20_000 for s in (SEEDS["dev"][1], SEEDS["eval"][1], BENCH["seed_a"])]
    nums = base + derived + [30261051, 40261052]
    pat = re.compile(rb"(?<!\d)(" + "|".join(map(str, nums)).encode() + rb")(?!\d)"); hits = []; nf = 0
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        top = os.path.relpath(root, repo).replace("\\", "/").split("/")[0]
        for f in files:
            if f == "ph26.py" or (f.startswith("ph26_") and f.endswith(".txt")) or (f.startswith("h17_") and f.endswith(".md")) or f == "master_plan.md": continue
            if (os.path.basename(root) == "notes" and f.endswith(".md")) or top == "viewer": continue
            nf += 1
            if pat.search(open(os.path.join(root, f), "rb").read()): hits.append(os.path.relpath(os.path.join(root, f), repo))
    return hits, nums, nf


def header(say=print):
    say(f"   ph26.py sha256 {sha()}; design {DESIGN}")
    say("   imported modules: " + "; ".join(f"{os.path.basename(m.__file__)} {sha(m.__file__)}" for m in MODS))
    say(f"   seeds: dev {SEEDS['dev']}, eval {SEEDS['eval']}, bench {BS}, bootstrap {ph15.BOOT_SEED}; demo seeds (5, 6) used deliberately, NOT part of the seed scan; no reproduction seed used")


def demo():
    print(f"== H17 self-checks (demo). design {DESIGN} ==")
    header()
    print("   fixed before this recorded demo (two failed self-checks on the first runs, neither in the rule): (1) a self-check expectation error: the demo expected the search"
          " target 75 at u 390, but u 390 lies in leg 5 (u 300-449, sigma +1) where the rule gives 285; the check point moved to u 450 (leg 6, sigma -1, downwind slant: 75);"
          " (2) the new cold-start runner did not record HEAD, so the row identity check raised a KeyError; HEAD is now recorded as ph24.run records it. The Search rule was not changed.")
    n, st = 40, 200; kw = dict(runs=n, steps=st); sd = (5, 6); sp = [(st, 0.30, 0.30)]; kn = [1.0, 0.0]
    for cls in (Agent10, Agent10g, Agent8, Agent6):
        ph24.record, ph24.make = _record24, _make24; a = ph24.run("T1", cls, (1.0, 0.0), sd, **kw); sa = ph24.stub(cls, kn, sp, rows=n, seeds=BS)
        ph24.record, ph24.make = record, make; b = ph24.run("T1", cls, (1.0, 0.0), sd, **kw); sb = ph24.stub(cls, kn, sp, rows=n, seeds=BS)
        assert all(np.array_equal(a[k], b[k]) for k in a if isinstance(a[k], np.ndarray)), f"a hook changed a ph24.run field ({cls.__name__})"
        assert all(np.array_equal(sa[k], sb[k]) for k in sa if isinstance(sa[k], np.ndarray)), f"a hook changed a ph24.stub field ({cls.__name__})"
    print("ok  the make and record hooks leave every field of ph24.run and ph24.stub bitwise equal for ph24's agents (World7 40 x 200 and stub; Agent10, Agent10g, Agent8, Agent6)")
    for cls, base in ((Agent12, Agent10), (Agent12g, Agent10g)):
        assert bitwise(run("T1", cls, (1.0, 0.0), sd, search=False, **kw), run("T1", base, (1.0, 0.0), sd, **kw)), f"{cls.__name__} search off is not {base.__name__}"
        assert bitwise(stub(cls, kn, sp, search=False, rows=n), stub(base, kn, sp, rows=n)), f"{cls.__name__} search off (stub) is not {base.__name__}"
        assert bitwise(stub(cls, kn, sp, rows=n), stub(base, kn, sp, rows=n)), f"{cls.__name__} stub (never engaged) is not {base.__name__}"
    print("ok  search=False: Agent12 == Agent10 and Agent12g == Agent10g bitwise (World7 and stub, 40 x 200); search True in the stub at p 0.30 == the base (never engaged)")
    assert list(leg_of(np.array([0, 29, 30, 89, 90, 179, 180, 299, 300, 449, 450, 629, 630]))) == [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7], "leg index"
    assert list(slant_of(np.array([0, 359, 360, 719, 720]))) == [1, 1, -1, -1, 1], "slant"
    assert np.allclose(search_target(np.array([0, 30, 360, 450]), np.ones(4)), [255.0, 105.0, 285.0, 75.0]), "search target"
    print("ok  leg k spans u in [15 k (k - 1), 15 k (k + 1)) (boundaries 30, 90, 180, 300, 450, 630); slant +1 for (u mod 720) < 360; target = 180 + sigma_k (90 - alpha 15): u 0 -> 255,"
          " u 30 -> 105, u 360 -> 285, u 450 -> 75 (cast_sign +1)")
    for lab, sched, first in (("silence from construction", [(400, 0.0, 0.0)], 209), ("one whiff at step 0", [(1, 1.0, 0.0), (399, 0.0, 0.0)], 210)):
        o = stub(Agent12, kn, sched, rows=n); ex, hq = engagement_exact(o); fe = first_true(o["ENG"])
        assert ex.all() and hq == 0 and (fe == first).all() and o["ENG"][first:].all(), f"engagement ({lab}): exact {int(ex.sum())}, held {hq}, first {set(fe.tolist())}"
        print(f"ok  stub {lab}, 40 rows x 400: engagement exact in every row (q, engaged, u, leg, slant, target, same noise sample); first engaged step index {first} in every row;"
              f" engaged to the end; q >= S with a hold 0")
    o = run("T1", Agent12, (1.0, 0.0), sd, runs=n, steps=400); ok, cnt = row_identity(o, run("T1", Agent10, (1.0, 0.0), sd, runs=n, steps=400)); ex, hq = engagement_exact(o)
    assert ok and ex.all(), f"World7 row identity {cnt}"
    print(f"ok  World7 +1/0 40 x 400: never-engaged rows bitwise Agent10, engaged rows equal before their first engaged step {cnt}; engagement exact in every row (q >= S with a hold: {hq})")
    c = {k: cold("c1", cl, False, seeds=sd, runs=n, steps=300) for k, cl in (("Agent10", Agent10), ("Agent12", Agent12), ("oracle", AgentO))}
    assert all(np.array_equal(c[k]["start"], c["Agent10"]["start"]) for k in c) and not inside(c["Agent10"]["start"], c["Agent10"]["src"]).any()
    pre = c["Agent12"]["W"][:164].any((0, 2)); fe = first_true(c["Agent12"]["ENG"]); ex, _ = engagement_exact(c["Agent12"], q0=BENCH["q_c1"])
    assert ex.all() and (fe[~pre] == 164).all(), f"(c1) engagement at step index 164 in rows without an earlier whiff {set(fe[~pre].tolist())}"
    ok, cnt = row_identity(c["Agent12"], c["Agent10"]); assert ok, f"(c1) Agent12 vs Agent10 before engagement {cnt}"
    fo = first_true(c["oracle"]["W"].any(2))
    print(f"ok  (c1) construction 40 rows: identical start in every arm, outside both whiff regions; Agent12 engaged at step index 164 in every row without an earlier whiff"
          f" ({int((~pre).sum())} rows), engagement exact, equal to Agent10 before it {cnt}. Printed, not asserted (the bench measures it; this demo run is 300 steps): any whiff in steps 164-299"
          f" Agent10 {int(c['Agent10']['W'][164:].any((0, 2)).sum())}, Agent12 {int(c['Agent12']['W'][164:].any((0, 2)).sum())}; oracle first whiff step {q3(fo[fo >= 0])} (rows {int((fo >= 0).sum())})")
    oo = c["oracle"]; P0 = oo["start"]; _, d0, pt0 = region_near(P0, oo["src"]); to = np.degrees(np.arctan2(pt0[:, 1] - P0[:, 1], pt0[:, 0] - P0[:, 0])) % 360.0
    assert np.allclose(oo["TGT"][0], to) and (d0 > 0).all(), "oracle target at step 0"
    print(f"ok  oracle: target at step 0 = the bearing to the nearest point of the nearest whiff region (distance {q3f(d0)}); the adopted rule after the first whiff")
    cw = cold("c1", Agent12, True, seeds=sd, runs=n, steps=50); cn = cold("c1", Agent12, False, seeds=sd, runs=n, steps=50)
    assert not cn["C"].any()
    print(f"ok  walls off: no contact is ever registered (40 x 50); walls on is World7's default (contacts {int(cw['C'].sum())} in 40 x 50)")
    for wd in ("W1", "T3a"):
        o = run(wd, Agent12, (1.0, 0.0), sd, **kw); ok, cnt = row_identity(o, run(wd, Agent10, (1.0, 0.0), sd, **kw)); assert ok and o["draws_equal"] and o["rng_equal"], wd
    print("ok  W1 and T3a (40 x 200): row identity vs Agent10 and the masked draws == the World7 twin")
    hits, nums, nf = seeds_unused(); assert not hits, f"a seed of this run appears in {hits}"
    print(f"ok  seeds {nums} appear in no other file under the repository ({nf} files scanned; excluded by name ph26.py, ph26_*.txt, h17_*.md, master_plan.md, notes/*.md, viewer/*)")


# ------------------------------------------------------------------ the tasks (design sections 5-8)
T1ARMS = {"search": Agent12, "base": Agent10, "search-gate": Agent12g, "base-gate": Agent10g}
T2ARMS = {"search": Agent12, "base": Agent10, "reference": Agent6}
T3ARMS = {"search": Agent12, "base": Agent10, "wall-reflex base": Agent8, "search-gate": Agent12g, "base-gate": Agent10g}
T4ARMS = {"search": Agent12, "base": Agent10, "ceiling": None}


def w1sum(o):
    r = np.arange(len(o["good"])); p = 1 - o["good"]
    return ph22.summary(dict(o, pres=p, AT=o["AT2"][:, r, p], src=o["src"][r, p]))


def main(mode):
    seeds = SEEDS[mode]; rows = np.arange(R); ok = lambda z: "PASS" if z else "FAIL"
    print(f"== H17, {mode.upper()}. design {DESIGN}; G {G_STAR}, gate on; S {S_ON}; world seed {seeds[0]}, agent seed {seeds[1]}; {R} rows x {T} steps; geometry C0;"
          f" bootstrap seed {ph15.BOOT_SEED}; {'operation check only (not a verdict)' if mode == 'dev' else 'the one evaluation'} ==")
    header()
    hits, nums, nf = seeds_unused(); print(f"   seed self-check: every H17 seed and derived in no other file ({nf} scanned): {not hits}{'' if not hits else ' ' + str(hits)}")
    print("   rows share no state: one generator per world and one per agent population, fixed-size draws consumed in row order every step")
    print("\n== B, the mechanism bench, re-run first with the bench seeds (section 4; the tasks run only if B passes) ==")
    lines = []; B, bo = bench(say=lines.append)
    for ln in lines:
        if ln.startswith("== B") or ln.startswith("(b) engagement exact") or "(c1) BARS" in ln or "bar upper bound" in ln or "STOP RULE" in ln or "pass probability" in ln: print("   " + ln.strip())
    if not B:
        print("\n== B did not pass: the tasks are NOT run (design section 4 / 8). =="); return
    t1 = {a: run("T1", c, (1.0, 0.0), seeds) for a, c in T1ARMS.items()}; maj = {a: majority(t1[a]) for a in t1}
    print("\n== T1, the H21 choice task (+1/0) ==")
    for a, o in t1.items():
        describe_majority(a, o, *maj[a]); h21_diag(a, o)
        if "ENG" in o and o["SRCH"]: er = o["ENG"].any(0); print(f"      [{a}] engaged rows {int(er.sum())}/{R}, engaged (row, step) {int(o['ENG'].sum())}, first engaged step {q3(first_true(o['ENG'])[er])}")
    print("\n== T2, the absent-odour world W1 (valued column masked from step 0) ==")
    t2 = {a: run("W1", c, (1.0, 0.0), seeds) for a, c in T2ARMS.items()}; s2 = {a: w1sum(o) for a, o in t2.items()}
    for a, o in t2.items():
        s = s2[a]; print(f"   [W1 {a} {o['arm']}] dwell at the present source mean {s['dwell'].mean():.3f} (quartiles {q3f(s['dwell'].astype(float))}); reach {int(s['reach'].sum())}/{R};"
                         f" lost rows {int(s['lost'].sum())}; wall contacts per row {s['contacts'].mean():.3f}; engaged rows {int(o['ENG'].any(0).sum())}; draws == twin {o['draws_equal'] and o['rng_equal']}")
    print("\n== T3, the +1/-1 stranded condition (World7 at +1/-1) ==")
    t3 = {a: run("T1", c, (1.0, -1.0), seeds) for a, c in T3ARMS.items()}; m3 = {a: majority(o) for a, o in t3.items()}; L3 = {a: lost(o) for a, o in t3.items()}
    st = {a: released(o) for a, o in t3.items()}
    for a, o in t3.items():
        V, N, Z = m3[a]; E, Rr, _ = st[a]; sr = np.unique(Rr); wc = o["contacts"] > 0
        after = np.array([bool(o["W"][e + 1:, r].any()) for e, r in zip(E, Rr)], bool); left = T - 1 - E
        pvw = f"{V[wc].mean():.3f} ({int(V[wc].sum())}/{int(wc.sum())})" if wc.any() else "n/a"
        print(f"   [T3 {a} {o['arm']}] V {int(V.sum())} N {int(N.sum())} tie {int(Z.sum())}; lost rows {int(L3[a].sum())}; wall contacts per row {o['contacts'].mean():.3f} (rows with any {int(wc.sum())});"
              f" P(V | wall contact) {pvw}; stranded rows {len(sr)} (drive-ended negative holds {len(E)}); any whiff after the release {int(after.sum())}/{len(E)}, among releases with >= 200 steps left"
              f" {int(after[left >= 200].sum())}/{int((left >= 200).sum())}; engaged rows {int(o['ENG'].any(0).sum())}")
    o12 = t3["search"]; eng_before = np.maximum.accumulate(o12["ENG"], 0); neg = 1 - o12["good"]; ev = events(o12)
    reneg = ev["form"] & (o12["H"] == neg[None, :]) & np.vstack([np.zeros((1, R), bool), eng_before[:-1]])
    print(f"      [T3 search] negative holds formed after an engaged step {int(reneg.sum())} in {int(reneg.any(0).sum())} rows; lost among the base's stranded rows: search"
          f" {int(L3['search'][np.unique(st['base'][1])].sum())}, base {int(L3['base'][np.unique(st['base'][1])].sum())}")
    print("\n== T4, the constructed loss T3a (reported) ==")
    t4 = {a: (run("T3a", c, (1.0, 0.0), seeds) if c is not None else run("T3a", None, (1.0, 0.0), seeds, fixed="neutral")) for a, c in T4ARMS.items()}
    D4 = {a: t3_dwell(o, 100, T) for a, o in t4.items()}
    for a, o in t4.items():
        g = o["good"]; dv = np.linalg.norm(o["POS"] - o["src"][rows, g][None], axis=2)
        print(f"   [T4 {a} {o['arm']}] neutral dwell 100-599 mean {D4[a].mean():.3f} (quartiles {q3f(D4[a])}); steps within 10 of the valued source per row {(dv < 10).sum(0).mean():.1f};"
              f" distance to the valued source median at steps 100/300/599 {np.median(dv[100]):.1f}/{np.median(dv[300]):.1f}/{np.median(dv[599]):.1f};"
              f" engaged-step fraction {o['ENG'].mean():.4f}")
    judge(seeds, B, t1, maj, t2, s2, t3, m3, L3, st, t4, D4)


def judge(seeds, B, t1, maj, t2, s2, t3, m3, L3, st, t4, D4):
    ok = lambda z: "PASS" if z else "FAIL"
    print("\n== criteria (design v2 FINAL section 7; 95 percent, one evaluation, no extension; aggregation: PASS if every part passes, FAIL if any fails, else INCONCLUSIVE; the unrounded bound decides) ==")
    Bv = "PASS" if B else "FAIL"; print(f"   B bench -> {Bv}")
    # identities in the run
    i = {}
    i["T1 search False == Agent10"] = bitwise(run("T1", Agent12, (1.0, 0.0), seeds, search=False), t1["base"])
    i["T1 Agent12g search False == Agent10g"] = bitwise(run("T1", Agent12g, (1.0, 0.0), seeds, search=False), t1["base-gate"])
    cnts = {}
    for lab, a, b in (("T1", t1["search"], t1["base"]), ("T1 gate", t1["search-gate"], t1["base-gate"]), ("T2", t2["search"], t2["base"]), ("T3", t3["search"], t3["base"]),
                      ("T3 gate", t3["search-gate"], t3["base-gate"]), ("T4", t4["search"], t4["base"])):
        ok_, cnt = row_identity(a, b); i[f"{lab} never-engaged rows bitwise the base"] = ok_; cnts[lab] = cnt
        ex, hq = engagement_exact(a); i[f"{lab} engagement exact every row"] = bool(ex.all()); cnts[lab]["q>=S with a hold"] = hq
    idok = all(i.values())
    print("   identities in the run: " + "; ".join(f"{k} {v}" for k, v in i.items()) + f" -> {'all True' if idok else 'FAILED (UNREADABLE, section 8)'}")
    for k, v in cnts.items(): print(f"      {k}: {v}")
    # M1
    V12, V10 = maj["search"][0], maj["base"][0]; ties = maj["base"][2].mean(); e1 = t1["search"]["ENG"].any(0)
    print(f"   M1(a) rows bitwise Agent10 (never engaged) {cnts['T1']['never_equal']}/{R}; engaged rows {int(e1.sum())} (reported); base ties {maj['base'][2].sum()}/{R} = {ties:.3f} (unreadable above 0.20)")
    m1 = [crit("M1(b) T1 paired DP P(V) Agent12 - Agent10", "DP", -0.05, False, V12.astype(float), V10.astype(float)),
          crit("M1(c) T1 lost rows (no whiff of either plume on 400-599), Agent12 - Agent10", "DP", 0.05, True, lost(t1["search"]).astype(float), lost(t1["base"]).astype(float))]
    cm = t1["search"]["contacts"].mean(); m1.append(ok(cm <= 0.10)); print(f"   M1(c) T1 Agent12 wall contacts per row: mean {cm:.3f}  at most 0.10 -> {m1[-1]}")
    M1 = agg(m1); c12, c10 = cls3(t1["search"]), cls3(t1["base"])
    print(f"   M1 -> {M1}      reported: into V {int(((c12 == 0) & (c10 != 0)).sum())}, out of V {int(((c12 != 0) & (c10 == 0)).sum())}; P(V) Agent12 {V12.mean():.3f}, Agent10 {V10.mean():.3f},"
          f" Agent12g {maj['search-gate'][0].mean():.3f}, Agent10g {maj['base-gate'][0].mean():.3f}; lost rows {int(lost(t1['search']).sum())} vs {int(lost(t1['base']).sum())}")
    # M2
    d12, d10, d6 = (s2[a]["dwell"].astype(float) for a in ("search", "base", "reference"))
    M2 = crit("M2(a) T2 W1 paired dwell Agent12 - Agent10", "DP", -1.2, False, d12, d10)
    _, a6, a6l, a6h = interval("DP", d12, d6)
    print(f"   M2 -> {M2}      M2(b) reported: dwell Agent12 {d12.mean():.3f}, Agent10 {d10.mean():.3f}, Agent6 {d6.mean():.3f}; Agent12 - Agent6 {a6:+.3f} [{a6l:+.3f}, {a6h:+.3f}];"
          f" reach {int(s2['search']['reach'].sum())}/{int(s2['base']['reach'].sum())}/{int(s2['reference']['reach'].sum())}; lost rows {int(s2['search']['lost'].sum())}/{int(s2['base']['lost'].sum())}/"
          f"{int(s2['reference']['lost'].sum())}; contacts per row {s2['search']['contacts'].mean():.3f}/{s2['base']['contacts'].mean():.3f}/{s2['reference']['contacts'].mean():.3f} (Agent12/Agent10/Agent6)")
    # M3
    nstr = len(np.unique(st["base"][1])); readable = nstr >= 50
    print(f"   M3 readability: stranded rows in the base arm {nstr} (at least 50 -> {'readable' if readable else 'UNREADABLE'})")
    m3a = crit("M3(a) T3 lost rows, paired DP Agent12 - Agent10", "DP", -0.05, True, L3["search"].astype(float), L3["base"].astype(float)) if readable else "UNREADABLE"
    if not readable: print("   M3(a) -> UNREADABLE (fewer than 50 stranded rows in the base arm)")
    m3b = crit("M3(b) T3 P(V), paired DP Agent12 - Agent10", "DP", -0.02, False, m3["search"][0].astype(float), m3["base"][0].astype(float))
    cm3 = t3["search"]["contacts"].mean(); m3c = ok(cm3 <= 0.10); print(f"   M3(c) T3 Agent12 wall contacts per row: mean {cm3:.3f}  at most 0.10 -> {m3c}")
    M3 = agg([m3a, m3b, m3c])
    _, g8, g8l, g8h = interval("DP", m3["search"][0].astype(float), m3["wall-reflex base"][0].astype(float))
    print(f"   M3 -> {M3}      reported: P(V) Agent12 {m3['search'][0].mean():.3f}, Agent10 {m3['base'][0].mean():.3f}, Agent8 {m3['wall-reflex base'][0].mean():.3f}, Agent12g {m3['search-gate'][0].mean():.3f},"
          f" Agent10g {m3['base-gate'][0].mean():.3f}; gap Agent12 - Agent8 {g8:+.3f} [{g8l:+.3f}, {g8h:+.3f}]; lost rows " + "/".join(str(int(L3[a].sum())) for a in L3) + f" ({'/'.join(L3)})")
    # M4 reported
    _, x1, x1l, x1h = interval("DP", D4["search"], D4["base"])
    print(f"   M4 T4 (REPORTED): neutral dwell 100-599 Agent12 {D4['search'].mean():.3f}, Agent10 {D4['base'].mean():.3f}, ceiling {D4['ceiling'].mean():.3f}; Agent12 - Agent10 {x1:+.3f} [{x1l:+.3f}, {x1h:+.3f}];"
          f" engaged-step fraction Agent12 {t4['search']['ENG'].mean():.4f}")
    unread = (not idok) or ties > 0.20 or m3a == "UNREADABLE"
    parts = (Bv, M1, M2, M3); verdict = all(x == "PASS" for x in parts)
    lab = "PASS" if verdict else "UNREADABLE" if unread else "FAIL" if any(x == "FAIL" for x in parts) else "INCONCLUSIVE"
    print(f"\n== H17 ==  B {Bv}  M1 {M1}  M2 {M2}  M3 {M3}  (M4 reported) -> {lab}"
          + (": after S silent steps with nothing held, a crosswind cast of growing amplitude slanted along the wind lets the adopted agent find a plume from the stranded state outside it"
             " without the wall reflex, and changes nothing where a whiff arrives within S (supplied values, G 2, C0, these worlds, learning off, the wind sensed every step; q under the"
             " H17-scoped relaxation)" if verdict else " under the registered criteria")
          + (" [development run: operation check only, not a verdict]" if seeds == SEEDS["dev"] else ""))


if __name__ == "__main__":
    mode = ([m for m in sys.argv[1:] if m in ("demo", "bench", "dev", "eval")] or ["demo"])[0]
    if mode == "demo": demo(); sys.exit(0)
    if mode == "bench":
        B, o = bench(); sys.exit(0 if B else 3 if o["cand"] else 1)
    main(mode)
