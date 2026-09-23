#!/usr/bin/env python3
"""H21: hold maintenance by value in the H20 choice task.

Usage: python ph19.py demo | bench | dev | eval

Design v2 FINAL, confirmed by the owner (decision:h21-open): doc d7fd5abcc95169698, hash e83c9de2...965a,
stored before this file existed. ONE change to the Run 2 agent (ph16.Agent4): while an odour is held,
the response of a lower-valued NON-NEGATIVE odour is gated to zero before it enters the selection circuit
and the evidence-release comparison (gate_k = 0 iff h >= 0 and 0 <= v_k < v_h). Equal values, nothing
held and negative odours are never gated, so in those cases the agent IS Agent4 (checked bitwise).
No adopted module is edited. Task, measure, seeds and criteria as the design; nothing changes after the table.
"""
import sys, os, re, hashlib
import numpy as np
import ph15, ph16
from ph16 import World7, Agent4, Still, cast_draw, outcome, diagnostics, describe, interval, crit, med, identity_agent3, CELLS, R, T
from ph17 import Agent5
from ph18 import majority, describe_majority, agg
from ph11 import RESET_AFTER, MARGIN
from ph12 import SAT
from ph9 import UPWIND, CAST_PERIOD, MAXOFF, GAIN, MAXTURN, TURN_NOISE, HIT_R, angdiff

DESIGN = "v2 FINAL doc d7fd5abcc95169698 hash e83c9de2acba49d65893000f453ee384134ab33a3c916466010327736535965a"
G_STAR = 2.0
SEEDS = dict(dev=(9860, 9960), eval=(1725, 1825))
BENCH = dict(rows=400, phase1=60, phase2=200, p_hold=0.30, p_other=(0.30, 0.057), seed_w=20260926, seed_a=20260927)
#            valued value, other value, G, rule, fixed identity
ARMS = {"maintain": (1.0, 0.0, G_STAR, True, False), "rule-off": (1.0, 0.0, G_STAR, False, False),
        "rule-only": (1.0, 0.0, 0.0, True, False), "pathway-off": (1.0, 0.0, 0.0, False, False),
        "neutral": (0.0, 0.0, G_STAR, True, False), "known-answer": (1.0, 0.0, 0.0, False, True),
        "priority-identity": (1.0, -1.0, G_STAR, True, False)}
ph15.BOOT_SEED = 20260928            # design section 7; ph16 set the 95 percent level

def sha(): return hashlib.sha256(open(__file__, "rb").read()).hexdigest()


class Agent6(Agent4):
    """Agent4 (Run 2's agent: Agent3 + the H20 gain) plus the H21 gate. act is Agent4.act with the gate
    inserted where y' is formed; rule=False must BE Agent4 step for step (checked in demo and in the run)."""

    def __init__(self, runs, rng, rule=True, **kw):
        super().__init__(runs, rng, **kw); self.rule = rule

    def act(self, w, whiffs, wind_on):
        rows = np.arange(self.R)
        y = self.up.step(whiffs.astype(float))*(1.0 + self.G*np.maximum(self.chan_valence(), 0.0))   # H20: the gain
        hp = self.held()
        if self.rule:                                                                                 # H21: the gate
            v = self.chan_valence(); vh = v[rows, np.maximum(hp, 0)]
            y = y*~((hp >= 0)[:, None] & (v >= 0.0) & (v < vh[:, None]))
        self.yp = y
        committed = hp >= 0; hi = np.maximum(hp, 0); other = 1 - hi
        self.due_timeout = self.silence > RESET_AFTER
        self.due_evidence = committed & ((y[rows, other] - y[rows, hi]) > MARGIN)
        due = self.due_timeout | self.due_evidence
        rst = np.where(due, 10.0, 0.0)[:, None]
        self.silence = np.where(due, 0.0, self.silence)
        self.sel.step(y, reset=rst)
        h = self.held()
        est = self.est = self.estimate(w, wind_on)
        val = np.where(h >= 0, self.known[rows, np.maximum(h, 0)], 0.0)
        hit = np.where(h >= 0, whiffs[rows, np.maximum(h, 0)], False)
        nav = hit | ((h < 0) & (whiffs & (self.chan_valence() >= 0)).any(1))
        self.nav_hit = nav
        self.since = np.where(nav, 0.0, self.since + 1.0)
        self.silence = np.where(hit, 0.0, self.silence + 1.0)
        side = np.where((self.since // CAST_PERIOD) % 2 == 0, 1.0, -1.0)*self.cast_sign
        off = MAXOFF*(1.0 - np.abs((self.since/SAT) % 2.0 - 1.0))
        tgt = np.where(nav, UPWIND, (UPWIND + side*off) % 360.0)
        self.tgt = tgt = np.where(val < 0, self.flee_side, tgt)
        turn = np.clip(GAIN*angdiff(tgt, est), -MAXTURN, MAXTURN)
        turn = turn + TURN_NOISE*self.rng.standard_normal(self.R)
        self.last_turn = turn
        return turn, h


def make(cls, runs, rng, G, known, rule):
    return cls(runs, rng, G=G, known=known, rule=rule) if cls is Agent6 else cls(runs, rng, G=G, known=known)


# ------------------------------------------------------------------ the task (design sections 5, 6)
def run(arm, seeds, runs=R, steps=T, G=None, rule=None, cls=Agent6):
    vg, vo, g, rl, fixed = ARMS[arm]; g = g if G is None else G; rl = rl if rule is None else rule
    w = World7(runs, np.random.default_rng(seeds[0]), seeds[0]); rows = np.arange(runs); neutral = 1 - w.good
    kv = np.zeros((runs, 2)); kv[rows, w.good] = vg; kv[rows, neutral] = vo
    rng = np.random.default_rng(seeds[1])
    a = Agent5(runs, rng, fixed=w.good.copy(), G=0.0, known=kv) if fixed else make(cls, runs, rng, g, kv, rl)
    a.cast_sign = cast_draw(seeds[1], runs)
    o = dict(good=w.good, cell=w.cell, plus_y=w.plus_y, src=w.src.copy(), G=a.G, rule=rl and not fixed, fixed=fixed, cast=a.cast_sign.copy(),
             first=np.full((runs, 2), -1), dwell=np.zeros((runs, 2)), H=np.full((steps, runs), -1, np.int8), W=np.zeros((steps, runs, 2), bool),
             NAV=np.zeros((steps, runs), bool), TO=np.zeros((steps, runs), bool), EV=np.zeros((steps, runs), bool),
             POS=np.zeros((steps, runs, 2)), HEAD=np.zeros((steps, runs)), S=np.zeros((steps, runs, 2)),
             contacts=np.zeros(runs), viol=0, neg_steps=0, neg_rows=np.zeros(runs, bool), ymax=0.0, y_over=0, sat=0, smax=0.0, exit=np.full(runs, -1))
    for t in range(steps):
        whiffs = w.sense()
        turn, h = a.act(w, whiffs, w.wind_on())
        neg = (h >= 0) & (kv[rows, np.maximum(h, 0)] < 0)
        o["viol"] += int((neg & (a.tgt != a.flee_side)).sum()); o["neg_steps"] += int(neg.sum()); o["neg_rows"] |= neg
        o["ymax"] = max(o["ymax"], float(a.yp.max())); o["y_over"] += int((a.yp > 1.8).sum())
        o["sat"] += int((a.sel.s >= 4.9).any(1).sum()); o["smax"] = max(o["smax"], float(a.sel.s.max()))
        w.move(turn); a.bump(w.bumped)
        at = w.at_source()
        o["first"] = np.where((o["first"] < 0) & at, t, o["first"]); o["dwell"] += at
        d_neg = np.linalg.norm(w.pos - w.src[rows, neutral], axis=1)
        o["exit"] = np.where((o["exit"] < 0) & (o["first"][rows, neutral] >= 0) & (d_neg > 6.0), t, o["exit"])
        o["H"][t] = h; o["W"][t] = whiffs; o["NAV"][t] = a.nav_hit; o["TO"][t] = a.due_timeout; o["EV"][t] = a.due_evidence
        o["POS"][t] = w.pos; o["HEAD"][t] = w.head; o["S"][t] = a.sel.s; o["contacts"] += w.bumped
    return o


def same(o1, o2): return all(np.array_equal(o1[k], o2[k]) for k in ("POS", "HEAD", "S"))
def no_whiff_last_third(o): return ~o["W"][-T//3:].any(axis=(0, 2))
def no_nav_last_third(o): return ~o["NAV"][-T//3:].any(0)


def h21_diag(arm, o, ref=None):
    """design section 5, 'added from the diagnosis': dwell by hold state, gaps, hold endings, revision, paired flips"""
    good = o["good"]; n = len(good); rows = np.arange(n); H = o["H"]; d = diagnostics(o)
    at = np.linalg.norm(o["POS"][:, :, None, :] - o["src"][None], axis=3) < HIT_R
    assert np.array_equal(at.sum(0), o["dwell"])
    def split(k):
        a = at[:, rows, k]; return tuple(int((a & (H == x[None, :])).sum()) for x in (good, 1 - good)) + (int((a & (H < 0)).sum()),)
    prev = np.vstack([np.full((1, n), -1, np.int8), H[:-1]]); committed = prev >= 0; ended = committed & (H != prev)
    s_prev = np.vstack([np.zeros((1, n)), o["S"][:-1][np.arange(T - 1)[:, None], rows[None, :], np.maximum(prev[:-1], 0)]])
    TO, EV = o["TO"], o["EV"]; k = int(ended.sum())
    fhn = d["fh_n"]; rev = fhn & d["ever_v"]
    print(f"      H21 diag: dwell steps at valued (valued-held, neutral-held, nothing) {split(good)} | at neutral {split(1 - good)};"
          f" nothing held {float((H < 0).mean()):.3f} of steps")
    print(f"      H21 diag: holds ended {k} (on the timeout flag {int((ended & TO & ~EV).sum())}, evidence {int((ended & EV & ~TO).sum())},"
          f" both {int((ended & TO & EV).sum())}, neither {int((ended & ~TO & ~EV).sum())}); held unit's s the step before, median {med(s_prev[ended]):.2f};"
          f" timeout firings while held {int((TO & committed).sum())}, of which ended the hold {int((ended & TO).sum())};"
          f" valued holds ended {int((ended & (prev == good[None, :])).sum())}, neutral holds ended {int((ended & (prev == (1 - good)[None, :])).sum())}")
    print(f"      H21 diag: revision, first hold neutral and later held valued {int(rev.sum())}/{int(fhn.sum())}"
          f"{f' = {rev.sum()/fhn.sum():.3f}' if fhn.sum() else ''}; no whiff of either plume in the last third {int(no_whiff_last_third(o).sum())};"
          f" no navigation hit in the last third {int(no_nav_last_third(o).sum())}; wall contacts per row {o['contacts'].mean():.2f}")
    if ref is not None:
        c, cr = np.select(list(majority(o)), [0, 1, 2]), np.select(list(majority(ref)), [0, 1, 2])
        print(f"      H21 diag: paired against rule-off, same rows: into V {int(((c == 0) & (cr != 0)).sum())}, out of V {int(((c != 0) & (cr == 0)).sum())},"
              f" unchanged class {int((c == cr).sum())}/{n}; first hold valued here {int(d['fh_v'].sum())} against {int(diagnostics(ref)['fh_v'].sum())}")


# ------------------------------------------------------------------ the mechanism bench (design section 4)
def bench_run(cls, G, rule, known, sched, rows=BENCH["rows"]):
    """sched: list of (steps, p channel 0, p channel 1). The same uniform draws for every condition."""
    steps = sum(s for s, _, _ in sched); u = np.random.default_rng(BENCH["seed_w"]).random((steps, rows, 2))
    a = make(cls, rows, np.random.default_rng(BENCH["seed_a"]), G, np.tile(known, (rows, 1)), rule); w = Still(rows)
    H, S, TO, Y = [], [], [], []; t = 0
    for n, p0, p1 in sched:
        for _ in range(n):
            x = np.stack([u[t, :, 0] < p0, u[t, :, 1] < p1], 1)
            _, h = a.act(w, x, np.ones(rows, bool)); H.append(h.copy()); S.append(a.sel.s.copy()); TO.append(a.due_timeout.copy()); Y.append(a.yp.copy()); t += 1
    return dict(H=np.array(H), S=np.array(S), TO=np.array(TO), Y=np.array(Y))


def bench_a(G, rule, p_other, quiet=False):
    p1, p2 = BENCH["phase1"], BENCH["phase2"]
    r = bench_run(Agent6, G, rule, [1.0, 0.0], [(p1, BENCH["p_hold"], 0.0), (p2, 0.0, p_other)])
    h60 = r["H"][p1 - 1]; denom = h60 == 0; kept = denom & (r["H"][p1:] == 0).all(0)
    k, pt, lo, hi = interval("P", kept[denom]) if denom.any() else (0, float("nan"), float("nan"), float("nan"))
    s_held = r["S"][p1:, :, 0][:, denom]; TO = r["TO"][p1:][:, denom]; H2 = r["H"][p1:][:, denom]
    prev = np.vstack([h60[denom][None, :], H2[:-1]]); ended_on_to = int(((prev == 0) & (H2 != 0) & TO).sum())
    if not quiet:
        print(f"   G {G:.1f} rule {'on ' if rule else 'off'} p_other {p_other:.3f}: holding channel 0 at step {p1}: {int(denom.sum())}/{BENCH['rows']}"
              f" (nothing {int((h60 < 0).sum())}, channel 1 {int((h60 == 1).sum())}); kept on every phase-2 step {k}/{int(denom.sum())} = {pt:.3f} [{lo:.3f}, {hi:.3f}];"
              f" timeout firings in phase 2 {int(TO.sum())}, ended the hold {ended_on_to}; held unit's s in phase 2 median {med(s_held.ravel()):.2f} min {s_held.min() if s_held.size else float('nan'):.2f};"
              f" y'' max {r['Y'].max():.2f}, y'' > 1.8 {100*(r['Y'] > 1.8).mean():.2f}%, s >= 4.9 {100*(r['S'] >= 4.9).any(2).mean():.2f}%, s max {r['S'].max():.2f}")
    return lo, int(denom.sum())


def bench_identity(label, G, known, sched):
    r6 = bench_run(Agent6, G, True, known, sched); r4 = bench_run(Agent4, G, False, known, sched)
    ok = np.array_equal(r6["S"], r4["S"]) and np.array_equal(r6["H"], r4["H"])
    return ok, r6, r4


def bench(verbose=True):
    print(f"== H21 mechanism bench (design section 4). design {DESIGN}; this file sha256 {sha()}; {BENCH} ==")
    print("(a) maintenance: phase 1 channel 0 (+1) alone, phase 2 channel 1 (0) alone, channel 0 silent; statistic = held channel 0 on EVERY phase-2 step, over the rows holding it at step 60")
    lo_bar = None
    for G in (G_STAR, 0.0):
        for rule in (True, False):
            for p in BENCH["p_other"]:
                lo, nd = bench_a(G, rule, p)
                if G == G_STAR and rule and p == BENCH["p_other"][0]: lo_bar, n_bar = lo, nd
    ok_b, r6, r4 = bench_identity("b", G_STAR, [1.0, 0.0], [(BENCH["phase1"], 0.0, BENCH["p_hold"]), (BENCH["phase2"], BENCH["p_hold"], 0.0)])
    h60 = r6["H"][BENCH["phase1"] - 1]; dn = h60 == 1; revised = dn & (r6["H"][BENCH["phase1"]:] == 0).any(0)
    print(f"(b) asymmetry, identity: neutral (channel 1, value 0) held first, then channel 0 (+1) alone: circuit states bitwise equal to the Run 2 agent's {ok_b};"
          f" rows holding channel 1 at step 60: {int(dn.sum())}; revised to channel 0 within phase 2: {int(revised.sum())} (both agents)")
    oks = []
    for name, kv in (("0/0", [0.0, 0.0]), ("+1/+1", [1.0, 1.0]), ("+1/-1", [1.0, -1.0])):
        ok, _, _ = bench_identity(name, G_STAR, kv, [(BENCH["phase2"], BENCH["p_hold"], BENCH["p_hold"])]); oks.append(ok)
        print(f"(c) inertness, identity: values {name}, both channels p {BENCH['p_hold']}, {BENCH['phase2']} steps: bitwise equal to the Run 2 agent's {ok}")
    verdict = lo_bar >= 0.95 and ok_b and all(oks)
    print(f"== M4: (a) at G {G_STAR} with the rule, p_other {BENCH['p_other'][0]}: lower bound {lo_bar:.3f} >= 0.95 over {n_bar} holding rows -> {'PASS' if lo_bar >= 0.95 else 'FAIL'};"
          f" (b) identity {ok_b}; (c) identities {oks} -> {'PASS: the task may be run' if verdict else 'NO CANDIDATE: the rule as specified does not maintain the hold; the task is NOT run'} ==")
    return verdict


# ------------------------------------------------------------------ self-checks
def priority_check6(G, rows=50, steps=20):
    """M5: the H21 agent SET to hold the negative odour (channel 1) while the valued odour is presented, G on:
    flee target on every negative-held step, equal to the same state's target at G = 0."""
    out = []
    for g in (G, 0.0):
        a = Agent6(rows, np.random.default_rng(11), G=g, known=np.tile([1.0, -1.0], (rows, 1)), rule=True)
        a.sel.s[:, 1] = 2.0; w = Still(rows); tg, hh = [], []
        for _ in range(steps):
            _, h = a.act(w, np.ones((rows, 2), bool), np.ones(rows, bool)); tg.append(a.tgt.copy()); hh.append(h.copy())
        out.append((np.array(tg), np.array(hh), a.flee_side))
    (tg1, h1, f1), (tg0, h0, f0) = out
    neg1 = h1 == 1; both = neg1 & (h0 == 1)
    assert neg1.any() and (tg1[neg1] == np.broadcast_to(f1, tg1.shape)[neg1]).all() and np.array_equal(tg1[both], tg0[both])
    return int(neg1.sum()), int(both.sum()), int((h1 == 0).sum())


def seeds_unused():
    """design section 9: none of this run's seeds appears in any other script or output on record (local record)"""
    pat = re.compile(r"(?<!\d)(9860|9960|1725|1825)(?!\d)"); hits = []
    for root in (os.path.dirname(os.path.abspath(__file__)), os.path.dirname(os.path.dirname(os.path.abspath(__file__)))):
        for f in os.listdir(root):
            if f.startswith("ph19") or f.startswith("h21_") or f.startswith("master_plan") or not f.endswith((".py", ".txt", ".md")): continue
            try: txt = open(os.path.join(root, f), encoding="utf-8", errors="ignore").read()
            except OSError: continue
            if pat.search(txt): hits.append(f)
    return hits


def pair(cls_a, cls_b, kv_fn, G, rule_a, n=40, steps=200, seed=(5, 6)):
    ws = [World7(n, np.random.default_rng(seed[0]), seed[0]) for _ in (0, 1)]; kv = kv_fn(ws[0])
    ag = [make(cls_a, n, np.random.default_rng(seed[1]), G, kv, rule_a), make(cls_b, n, np.random.default_rng(seed[1]), G, kv, False)]
    for a in ag: a.cast_sign = cast_draw(seed[1], n)
    for _ in range(steps):
        for w, a in zip(ws, ag):
            t, _ = a.act(w, w.sense(), w.wind_on()); w.move(t); a.bump(w.bumped)
    return np.array_equal(ws[0].pos, ws[1].pos) and np.array_equal(ws[0].head, ws[1].head) and np.array_equal(ag[0].sel.s, ag[1].sel.s)


def demo():
    ph16.demo()                                        # Agent3 identity, geometry, pre-hold, priority in a constructed state (Agent4)
    n = 40; rows = np.arange(n)
    def kv(w, vg, vo): k = np.zeros((n, 2)); k[rows, w.good] = vg; k[rows, 1 - w.good] = vo; return k
    assert pair(Agent6, Agent4, lambda w: kv(w, 1.0, 0.0), G_STAR, False), "rule off is not Agent4"
    assert pair(Agent6, Agent4, lambda w: kv(w, 0.0, 0.0), G_STAR, True), "rule on at 0/0 is not Agent4"
    assert pair(Agent6, Agent4, lambda w: kv(w, 1.0, 1.0), G_STAR, True), "rule on at +1/+1 is not Agent4"
    assert pair(Agent6, Agent4, lambda w: kv(w, 1.0, -1.0), G_STAR, True), "rule on at +1/-1 is not Agent4"
    assert not pair(Agent6, Agent4, lambda w: kv(w, 1.0, 0.0), G_STAR, True), "rule on at +1/0 changed nothing over 40 rows x 200 steps"
    print("ok  Agent6 with the rule off is Agent4 bitwise; with the rule on it is Agent4 at 0/0, +1/+1 and +1/-1, and differs at +1/0 (40 rows x 200 steps)")
    # the gate in a constructed state: valued held, neutral presented
    res = {}
    for rule in (True, False):
        a = Agent6(100, np.random.default_rng(3), G=G_STAR, known=np.tile([1.0, 0.0], (100, 1)), rule=rule); a.sel.s[:, 0] = 2.0; w = Still(100)
        held, y1 = [], []
        for _ in range(100):
            x = np.zeros((100, 2), bool); x[:, 1] = True
            _, h = a.act(w, x, np.ones(100, bool)); held.append(h == 0); y1.append(a.yp[:, 1].copy())
        res[rule] = (np.array(held).all(0).mean(), np.array(y1).max())
    assert res[True][0] == 1.0 and res[True][1] == 0.0, f"gate: valued hold not kept or neutral response not zero {res[True]}"
    assert res[False][0] < 0.5, f"without the rule the valued hold survived in {res[False][0]:.2f}"
    print(f"ok  constructed state, valued held and neutral presented 100 steps: with the rule the hold is kept in 100% and the neutral response entering the circuit is 0;"
          f" without it the hold is kept in {res[False][0]*100:.0f}%")
    # asymmetry: neutral held, valued presented -> revised, identically to Agent4
    st = []
    for cls, rule in ((Agent6, True), (Agent4, False)):
        a = make(cls, 100, np.random.default_rng(4), G_STAR, np.tile([1.0, 0.0], (100, 1)), rule); a.sel.s[:, 1] = 2.0; w = Still(100); hh = []
        for _ in range(100):
            x = np.zeros((100, 2), bool); x[:, 0] = True
            _, h = a.act(w, x, np.ones(100, bool)); hh.append(h.copy())
        st.append((np.array(hh), a.sel.s.copy()))
    assert np.array_equal(st[0][0], st[1][0]) and np.array_equal(st[0][1], st[1][1]), "asymmetry: rule on differs from Agent4 with a neutral hold"
    rv = (st[0][0] == 0).any(0).mean(); assert rv > 0.5, f"neutral hold revised to valued in only {rv:.2f}"
    print(f"ok  constructed state, neutral held and valued presented: revised to the valued odour in {rv*100:.0f}% of rows, bitwise the same as Agent4")
    exp1, cmp1, took = priority_check6(G_STAR)
    print(f"ok  priority (M5) with the H21 agent: negative odour held on {exp1} (row, step), target = flee side on every one, equal to G 0's on the {cmp1} steps both hold it;"
          f" the valued odour took the hold on {took} afterwards")
    seeds = (5, 6)
    o = run("known-answer", seeds, runs=n, steps=200); b = run("maintain", seeds, runs=n, steps=200)
    assert (o["H"] == o["good"][None, :]).all() and np.array_equal(o["NAV"], o["W"][:, rows, o["good"]]), "known-answer: h or hit wrong"
    assert np.array_equal(o["cast"], b["cast"]) and np.array_equal(o["good"], b["good"]), "arms differ in cast draw or assignment"
    V, N, Z = majority(dict(good=np.array([0, 0, 1]), dwell=np.array([[3.0, 1.0], [2.0, 2.0], [0.0, 5.0]])))
    assert V.tolist() == [True, False, True] and Z.tolist() == [False, True, False], "majority classes"
    assert same(run("rule-off", seeds, runs=n, steps=200), run("rule-off", seeds, runs=n, steps=200, cls=Agent4)), "rule-off arm is not Agent4"
    assert same(run("priority-identity", seeds, runs=n, steps=200), run("priority-identity", seeds, runs=n, steps=200, cls=Agent4)), "priority-identity arm is not Agent4"
    assert same(run("neutral", seeds, runs=n, steps=200), run("neutral", seeds, runs=n, steps=200, G=0.0, rule=False)), "neutral arm is not G 0"
    print("ok  known-answer h and hit; same cast draw and assignment across arms; majority classes; rule-off and priority-identity arms equal Agent4's runs; neutral equals G 0 (40 rows x 200 steps)")
    hits = seeds_unused(); assert not hits, f"a seed of this run appears in {hits}"
    print(f"ok  seeds {SEEDS} appear in no other script or output on the local record")


# ------------------------------------------------------------------ criteria (design section 7)
def judge(res, maj, first, seeds):
    rows = np.arange(R); ok = lambda z: "PASS" if z else "FAIL"
    print("\n== criteria (design v2 section 7; 95 percent, one evaluation, no extension; aggregation: PASS if every part passes, FAIL if any fails, else INCONCLUSIVE) ==")
    m1 = []
    for arm in ("neutral", "pathway-off", "known-answer"):
        z = maj[arm][2]; m1.append(ok(z.mean() <= 0.20)); print(f"   M1(a) {arm}: ties {z.sum()}/{R} = {z.mean():.3f}  at most 0.20 -> {m1[-1]}")
    o = res["neutral"]; V, N, Z = maj["neutral"]; which = np.where(V, o["good"], np.where(N, 1 - o["good"], -1))
    m1.append(crit("M1(b) neutral, P(+y source majority | chose)", "P", (0.35, 0.65), False, (which == o["plus_y"])[~Z]))
    V, N, Z = maj["pathway-off"]; m1.append(crit("M1(c) floor: pathway-off, P(V | chose)", "P", (0.35, 0.65), False, V[~Z]))
    m1.append(crit("M1(d) ceiling: known-answer, P(V) over all rows", "P", 0.85, False, maj["known-answer"][0]))
    M1 = agg(m1); print(f"   M1 -> {M1}{'' if M1 == 'PASS' else '  (the run is UNREADABLE under section 8)'}")
    Vm, Nm, Zm = maj["maintain"]; Vr = maj["rule-off"][0]; Vp = maj["pathway-off"][0]; Vk = maj["known-answer"][0]; Vo = maj["rule-only"][0]
    m2 = [crit("M2(a) maintain, P(V) over all rows", "P", 0.70, False, Vm)]
    for c in range(4): m2.append(crit(f"M2(b) maintain, cell {c} ({CELLS[c]}), P(V)", "P", 0.55, False, Vm[res["maintain"]["cell"] == c]))
    m2.append(crit("M2(c) DP = P(V) maintain - rule-off, same rows", "DP", 0.15, False, Vm.astype(float), Vr.astype(float)))
    M2 = agg(m2); print(f"   M2 -> {M2}")
    _, pt, lo, hi = interval("DP", Vm.astype(float), Vp.astype(float)); print(f"      reported, no bar: DP maintain - pathway-off {pt:+.3f} [{lo:+.3f}, {hi:+.3f}]")
    print(f"      reported: maintain N {Nm.sum()} tie {Zm.sum()}; P(V) maintain / known-answer = {Vm.mean():.3f} / {Vk.mean():.3f} = {Vm.mean()/Vk.mean() if Vk.mean() else float('nan'):.3f} of the ceiling")
    k, pt, lo, hi = interval("P", Vo); _, dpt, dlo, dhi = interval("DP", Vo.astype(float), Vp.astype(float))
    print(f"      reported: rule-only P(V) {k}/{R} = {pt:.3f} [{lo:.3f}, {hi:.3f}]; DP rule-only - pathway-off {dpt:+.3f} [{dlo:+.3f}, {dhi:+.3f}]")
    for arm in ("maintain", "rule-off", "pathway-off", "known-answer"):
        Vf, Nf, Zf = first[arm]; k, pt, lo, hi = interval("P", Vf)
        print(f"      reported, secondary first reach, {arm}: V {Vf.sum()} N {Nf.sum()} none {Zf.sum()}; P(V first) {k}/{R} = {pt:.3f} [{lo:.3f}, {hi:.3f}]")
    i1 = same(res["neutral"], run("neutral", seeds, G=0.0, rule=False)); ag3 = identity_agent3(seeds)
    i2 = same(res["priority-identity"], run("priority-identity", seeds, cls=Agent4)); i3 = same(res["rule-off"], run("rule-off", seeds, cls=Agent4))
    ka = res["known-answer"]; i4 = bool((ka["H"] == ka["good"][None, :]).all() and np.array_equal(ka["NAV"], ka["W"][:, rows, ka["good"]]))
    M3 = agg([ok(i1 and ag3), ok(i2), ok(i3), ok(i4)])
    print(f"   M3 identities: (i) neutral at G {G_STAR} with the rule == G 0 {i1}, G 0 == ph14.Agent3 {ag3}; (ii) priority-identity == ph16.Agent4 at +1/-1 {i2};"
          f" (iii) rule-off == ph16.Agent4 at +1/0 {i3}; (iv) known-answer h = valued and hit = its whiffs {i4} -> {M3}")
    lo_b, n_b = bench_a(G_STAR, True, BENCH["p_other"][0], quiet=True)
    M4 = ok(lo_b >= 0.95); print(f"   M4 mechanism bench (a), re-run here with the bench seeds: kept lower bound {lo_b:.3f} over {n_b} holding rows >= 0.95 -> {M4}")
    exp1, cmp1, took = priority_check6(G_STAR)
    M5 = "PASS" if i2 else "FAIL"
    print(f"   M5 avoidance: +1/-1 agent is the Run 2 agent by construction (M3 ii {i2}); constructed state: negative odour held on {exp1} (row, step), target = flee side on every one,"
          f" equal to G 0's on the {cmp1} steps both hold it; the valued odour took the hold on {took} afterwards -> {M5}")
    nw_m, nw_r = no_whiff_last_third(res["maintain"]).astype(float), no_whiff_last_third(res["rule-off"]).astype(float)
    m6 = [crit("M6(a) no whiff of either plume in the last third, maintain - rule-off", "DP", 0.05, True, nw_m, nw_r)]
    cm = res["maintain"]["contacts"].mean(); m6.append(ok(cm <= 0.10)); print(f"   M6(b) maintain, wall contacts per row: mean {cm:.3f}  at most 0.10 -> {m6[-1]}")
    M6 = agg(m6)
    print(f"   M6 -> {M6}      reported: no whiff in the last third maintain {int(nw_m.sum())} rule-off {int(nw_r.sum())} rule-only {int(no_whiff_last_third(res['rule-only']).sum())}"
          f" known-answer {int(no_whiff_last_third(res['known-answer']).sum())}; no navigation hit in the last third " + ", ".join(f"{a} {int(no_nav_last_third(res[a]).sum())}" for a in ARMS)
          + f"; rule-only contacts per row {res['rule-only']['contacts'].mean():.2f}")
    verdict = all(x == "PASS" for x in (M1, M2, M3, M4, M5, M6))
    print(f"\n== H21 ==  M1 {M1}  M2 {M2}  M3 {M3}  M4 {M4}  M5 {M5}  M6 {M6}  -> "
          + ("the rule maintains a valued hold and a maintained valued hold decides which source the agent stays at, without adding lost rows"
             if verdict else "UNREADABLE (M1)" if M1 != "PASS" else "NOT shown under the registered criteria"))


def main(mode):
    seeds = SEEDS[mode]
    print(f"== H21, {mode.upper()}. design {DESIGN}; this file sha256 {sha()}; G {G_STAR}; world seed {seeds[0]}, agent seed {seeds[1]};"
          f" {R} rows x {T} steps; geometry C0; {'operation check only' if mode == 'dev' else 'the one evaluation'} ==")
    res = {arm: run(arm, seeds) for arm in ARMS}
    maj = {arm: majority(res[arm]) for arm in ARMS}; first = {arm: outcome(res[arm]) for arm in ARMS}
    for arm in ARMS:
        describe_majority(arm, res[arm], *maj[arm]); h21_diag(arm, res[arm], res["rule-off"] if arm in ("maintain", "rule-only") else None)
        print("      secondary, first reach and diagnostics:"); describe(arm, res[arm], *first[arm])
    judge(res, maj, first, seeds)


if __name__ == "__main__":
    mode = ([m for m in sys.argv[1:] if m in ("demo", "bench", "dev", "eval")] or ["demo"])[0]
    if mode == "demo": demo(); sys.exit(0)
    if mode == "bench": sys.exit(0 if bench() else 1)
    main(mode)
