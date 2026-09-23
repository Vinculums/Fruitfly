#!/usr/bin/env python3
"""H23: value-filtered navigation in the H21 choice task.

Usage: python ph21.py demo | bench | dev | eval

Design v2 FINAL, confirmed by the owner (decision:h23-open): doc db6df2e0013ab96e7, hash c19751f4...0087,
stored before this file existed. ONE change to the H21 maintain agent (ph19.Agent6, G 2, gate on): the
navigation signal. keep = h >= 0 and (v_h = v_max or v_h < 0); nav = hit where keep, otherwise a whiff of a
top-valued non-negative odour (v_k >= 0 and v_k = v_max). The silence timer still counts hit; the circuit,
gain, gate, releases, cast and ring are untouched. filt=False, equal values, +1/-1 and +1/0 with the valued
odour held: the agent IS Agent6 (checked bitwise). `nav6` (Agent6's expression) and `differs` are exposed for
measurement only. No adopted module is edited. Bench (b) is reported, not a gate. Nothing changes after the table.
"""
import sys, os, re, hashlib
import numpy as np
import ph15, ph19, ph20b
from ph16 import World7, Agent4, Still, cast_draw, outcome, diagnostics, describe, interval, crit, med, identity_agent3, CELLS, R, T, DOWN
from ph17 import Agent5
from ph18 import majority, describe_majority, agg
from ph19 import Agent6, same, no_whiff_last_third, no_nav_last_third, h21_diag, priority_check6
from ph11 import RESET_AFTER, MARGIN
from ph12 import SAT
from ph9 import UPWIND, CAST_PERIOD, MAXOFF, GAIN, MAXTURN, TURN_NOISE, angdiff

sys.stdout.reconfigure(newline="\n")            # LF output, so the recorded sha256 equals the committed blob
DESIGN = "v2 FINAL doc db6df2e0013ab96e7 hash c19751f427363da9456a681659e23bf19bdb5463bdff966af99d04783bb30087"
G_STAR = 2.0
SEEDS = dict(dev=(9880, 9980), eval=(1765, 1865))
BENCH = dict(rows=400, rows_b=800, p=0.30, steps_stub=200, steps_held=260, steps=600, seed_w=20261001, seed_a=20261002)
BS = (BENCH["seed_w"], BENCH["seed_a"])
#            (valued value, other value), G, gate, filter rule, fixed identity
ARMS = {"filter": ((1.0, 0.0), G_STAR, True, True, False), "maintain": ((1.0, 0.0), G_STAR, True, False, False),
        "pathway-off": ((1.0, 0.0), 0.0, False, False, False), "known-answer": ((1.0, 0.0), 0.0, False, False, True),
        "neutral": ((0.0, 0.0), G_STAR, True, True, False), "priority-identity": ((1.0, -1.0), G_STAR, True, True, False)}
ph15.BOOT_SEED = 20261003            # design section 7 (set after the imports, which set their own); ph16 set the 95 percent level

def sha(): return hashlib.sha256(open(__file__, "rb").read()).hexdigest()
def q3(x): return f"{np.percentile(x, 25):.0f}/{np.median(x):.0f}/{np.percentile(x, 75):.0f}" if len(x) else "n/a"
def first_true(m): return np.where(m.any(0), m.argmax(0), -1)


class Agent8(Agent6):
    """Agent6 (Agent4 + the H21 gate) plus the H23 value filter on nav. act is Agent6.act with only the nav line
    replaced; filt=False must BE Agent6 step for step (checked in demo, bench and run)."""

    def __init__(self, runs, rng, filt=True, **kw):
        super().__init__(runs, rng, **kw); self.filt = filt
        self.nav6 = np.zeros(runs, bool); self.differs = np.zeros(runs, bool)

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
        v = self.chan_valence(); vmax = v.max(1); vh = v[rows, np.maximum(h, 0)]; top = (v >= 0) & (v == vmax[:, None])   # H23: the filter
        self.nav6 = hit | ((h < 0) & (whiffs & (v >= 0)).any(1))                                    # Agent6's line, measurement only
        keep = (h >= 0) & ((vh == vmax) | (vh < 0))
        nav = np.where(keep, hit, (whiffs & top).any(1)) if self.filt else self.nav6
        self.differs = nav != self.nav6
        self.nav_hit = nav
        self.since = np.where(nav, 0.0, self.since + 1.0)
        self.silence = np.where(hit, 0.0, self.silence + 1.0)                                        # the hold's clock: hit
        side = np.where((self.since // CAST_PERIOD) % 2 == 0, 1.0, -1.0)*self.cast_sign
        off = MAXOFF*(1.0 - np.abs((self.since/SAT) % 2.0 - 1.0))
        tgt = np.where(nav, UPWIND, (UPWIND + side*off) % 360.0)
        self.tgt = tgt = np.where(val < 0, self.flee_side, tgt)
        turn = np.clip(GAIN*angdiff(tgt, est), -MAXTURN, MAXTURN)
        turn = turn + TURN_NOISE*self.rng.standard_normal(self.R)
        self.last_turn = turn
        return turn, h


def make(cls, runs, rng, G, known, gate, filt):
    if cls is Agent8: return Agent8(runs, rng, G=G, known=known, rule=gate, filt=filt)
    return ph19.make(cls, runs, rng, G, known, gate)


# ------------------------------------------------------------------ one World7 run (task and bench; design sections 4-6)
def run(vals, seeds, G, gate, filt, fixed=False, cls=Agent8, runs=R, steps=T, start="task", hold=False):
    """start 'task': World7's start. 'variant': ph20b's VARIANT (neutral source + (DOWN, 0), heading upwind).
    'source': ph20.bench_d's (placed at the neutral source, World7 heading). hold: s_neutral 2.0 constructed at step 0.
    Construction order as ph20b.simulate / ph20.bench_d: world, values, agent, cast draw, position, hold."""
    w = World7(runs, np.random.default_rng(seeds[0]), seeds[0]); rows = np.arange(runs); neutral = 1 - w.good
    kv = np.zeros((runs, 2)); kv[rows, w.good] = vals[0]; kv[rows, neutral] = vals[1]
    rng = np.random.default_rng(seeds[1])
    a = Agent5(runs, rng, fixed=w.good.copy(), G=0.0, known=kv) if fixed else make(cls, runs, rng, G, kv, gate, filt)
    a.cast_sign = cast_draw(seeds[1], runs)
    if start == "variant": w.pos = w.src[rows, neutral] + np.array([DOWN, 0.0]); w.head = np.full(runs, UPWIND)
    elif start == "source": w.pos = w.src[rows, neutral].copy()
    if hold: a.sel.s[rows, neutral] = 2.0
    o = dict(good=w.good, cell=w.cell, plus_y=w.plus_y, src=w.src.copy(), G=a.G, fixed=fixed, cast=a.cast_sign.copy(), steps=steps,
             first=np.full((runs, 2), -1), dwell=np.zeros((runs, 2)), H=np.full((steps, runs), -1, np.int8), W=np.zeros((steps, runs, 2), bool),
             NAV=np.zeros((steps, runs), bool), DIFF=np.zeros((steps, runs), bool), TO=np.zeros((steps, runs), bool), EV=np.zeros((steps, runs), bool),
             SINCE=np.zeros((steps, runs), np.float32), POS=np.zeros((steps, runs, 2)), HEAD=np.zeros((steps, runs)), S=np.zeros((steps, runs, 2)),
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
        o["DIFF"][t] = getattr(a, "differs", False); o["SINCE"][t] = a.since
        o["POS"][t] = w.pos; o["HEAD"][t] = w.head; o["S"][t] = a.sel.s; o["contacts"] += w.bumped
    return o


def task(arm, seeds, **kw):
    p = dict(zip(("vals", "G", "gate", "filt", "fixed"), ARMS[arm])); p.update(kw)
    return run(seeds=seeds, **p)


def wv(o): return o["W"][:, np.arange(len(o["good"])), o["good"]]
def hold600(o): return o["H"][-1] == o["good"]
def traj(o1, o2): return np.array_equal(o1["POS"], o2["POS"]) and np.array_equal(o1["HEAD"], o2["HEAD"])
def full(o1, o2): return same(o1, o2) and all(np.array_equal(o1[k], o2[k]) for k in ("H", "NAV"))
def navlaw(o): return bool(np.array_equal(o["NAV"], wv(o)))


def separation(o, ref):
    """M3 (iv): bitwise equal to the reference (positions, headings, circuit states) up to the step before the first `differs` step"""
    eq = (o["POS"] == ref["POS"]).all(2) & (o["HEAD"] == ref["HEAD"]) & (o["S"] == ref["S"]).all(2)
    fd = first_true(o["DIFF"]); never = fd < 0; steps = eq.shape[0]
    before = np.arange(steps)[:, None] < np.where(never, steps, fd)[None, :]
    pre = (eq | ~before).all(0); whole = eq.all(0)
    return bool(pre.all() and (whole | ~never).all()), dict(never=int(never.sum()), never_equal=int((never & whole).sum()), differ=int((~never).sum()),
                                                          differ_pre_equal=int((~never & pre).sum()), differ_equal_throughout=int((~never & whole).sum()))


def h23_diag(arm, o, ref=None):
    """design section 5, 'added for H23'"""
    d = diagnostics(o); V = majority(o)[0]; fd = first_true(o["DIFF"]); n = len(V)
    print(f"      H23 diag: rows with a `differs` step {int((fd >= 0).sum())}/{n}, first `differs` step quartiles {q3(fd[fd >= 0])}; `differs` (row, step) {int(o['DIFF'].sum())};"
          f" nav == valued whiff on every (row, step) {navlaw(o)}; holding the valued odour at step {o['steps']} {int(hold600(o).sum())}/{n}"
          f" (neutral {int((o['H'][-1] == 1 - o['good']).sum())}, nothing {int((o['H'][-1] < 0).sum())});"
          f" P(V | first hold valued) {int((V & d['fh_v']).sum())}/{int(d['fh_v'].sum())}, P(V | first hold neutral) {int((V & d['fh_n']).sum())}/{int(d['fh_n'].sum())};"
          f" cast clock max {o['SINCE'].max():.0f}")
    if ref is not None:
        cl, cr = np.select(list(majority(o)), [0, 1, 2]), np.select(list(majority(ref)), [0, 1, 2]); dr = diagnostics(ref); fhn = d["fh_n"]; fhv = d["fh_v"]
        print(f"      H23 diag: paired against maintain, same rows: into V {int(((cl == 0) & (cr != 0)).sum())}, out of V {int(((cl != 0) & (cr == 0)).sum())},"
              f" unchanged class {int((cl == cr).sum())}/{n}; first hold identical row for row {int((d['fh'] == dr['fh']).sum())}/{n} (valued here {int(fhv.sum())} against {int(dr['fh_v'].sum())});"
              f" into V among neutral-first rows {int(((cl == 0) & (cr != 0) & fhn).sum())}, among valued-first rows {int(((cl == 0) & (cr != 0) & fhv).sum())};"
              f" holding valued at step {o['steps']} here {int(hold600(o).sum())} against {int(hold600(ref).sum())}"
              f" (among maintain's neutral-first rows {int((hold600(o) & dr['fh_n']).sum())} against {int((hold600(ref) & dr['fh_n']).sum())} of {int(dr['fh_n'].sum())})")


# ------------------------------------------------------------------ the mechanism bench (design section 4)
def stub(known, sched, filt=True, cls=Agent8, G=G_STAR, gate=True, rows=BENCH["rows"], hold=None):
    """Still stub; sched: list of (steps, p channel 0, p channel 1); the same uniform draws for every condition; hold: channel set to s 2.0"""
    steps = sum(s for s, _, _ in sched); u = np.random.default_rng(BENCH["seed_w"]).random((steps, rows, 2))
    a = make(cls, rows, np.random.default_rng(BENCH["seed_a"]), G, np.tile(known, (rows, 1)), gate, filt); w = Still(rows)
    if hold is not None: a.sel.s[:, hold] = 2.0
    rec = {k: [] for k in ("H", "s", "S", "NAV", "SINCE", "TGT", "X")}; t = 0
    for n, p0, p1 in sched:
        for _ in range(n):
            x = np.stack([u[t, :, 0] < p0, u[t, :, 1] < p1], 1)
            _, h = a.act(w, x, np.ones(rows, bool)); t += 1
            for k, v in (("H", h), ("s", a.sel.s), ("S", a.sel.S), ("NAV", a.nav_hit), ("SINCE", a.since), ("TGT", a.tgt), ("X", x)): rec[k].append(v.copy())
    return {k: np.array(v) for k, v in rec.items()}


K_STUB = ("H", "s", "S", "NAV", "SINCE", "TGT")
def equal(r1, r2, keys=K_STUB): return all(np.array_equal(r1[k], r2[k]) for k in keys)


def bench_a4(quiet=False):
    p = BENCH["p"]; r = stub([1.0, 0.0], [(BENCH["steps_stub"], p, p)], hold=1)
    ok = (r["NAV"] == r["X"][:, :, 0]).all(0); k, pt, lo, hi = interval("P", ok)
    if not quiet:
        h1 = r["H"] == 1
        print(f"   (a4) +1/0, channel 1 (value 0) held by construction (s 2.0), both channels p {p}, {BENCH['steps_stub']} steps: nav == channel 0's whiff on every step in {k}/{len(ok)}"
              f" = {pt:.3f} [{lo:.3f}, {hi:.3f}] (bar lower bound >= 0.95); channel 1 held on {int(h1.sum())} (row, step), nav True on {int((r['NAV'] & h1).sum())} of them,"
              f" all with a channel-0 whiff {bool((r['X'][:, :, 0] | ~(r['NAV'] & h1)).all())}; Agent6 on the same draws: nav on channel-1-held steps from channel 1's whiff"
              f" {int((stub([1.0, 0.0], [(BENCH['steps_stub'], p, p)], cls=Agent6, hold=1)['NAV'] & h1).sum())}")
    return lo


def bench_b(quiet=False):
    """task-like neutral-hold start (ph20b VARIANT state), 800 rows, 600 steps; statistic holding valued at 600; paired DP bar > 0 (reported, not a gate)"""
    n = BENCH["rows_b"]
    o8 = run((1.0, 0.0), BS, G_STAR, True, True, runs=n, steps=BENCH["steps"], start="variant", hold=True)
    o6 = run((1.0, 0.0), BS, G_STAR, True, False, cls=Agent6, runs=n, steps=BENCH["steps"], start="variant", hold=True)
    a, b = hold600(o8).astype(float), hold600(o6).astype(float); _, dp, lo, hi = interval("DP", a, b)
    lab = "PASS" if lo > 0 else "FAIL" if hi <= 0 else "INCONCLUSIVE"
    if not quiet:
        for name, o in (("Agent8 (filter)", o8), ("Agent6 (maintain)", o6)):
            k, pt, l, h = interval("P", hold600(o)); V, N, Z = majority(o); r = np.arange(n); g = o["good"]
            fv = first_true(wv(o)); fs = first_true(o["NAV"] & wv(o)); fn = first_true(o["NAV"])
            fnn = np.where(fn >= 0, ~wv(o)[np.maximum(fn, 0), r], False)
            prev = np.vstack([(1 - g)[None, :].astype(np.int8), o["H"][:-1]]); ended = (prev >= 0) & (o["H"] != prev); TO, EV = o["TO"], o["EV"]
            print(f"   [{name}] holding the valued odour at step {BENCH['steps']}: {k}/{n} = {pt:.3f} [{l:.3f}, {h:.3f}]; dwell majority V {V.sum()} N {N.sum()} tie {Z.sum()};"
                  f" rows with a valued whiff {int((fv >= 0).sum())}, first valued whiff step quartiles {q3(fv[fv >= 0])};"
                  f" first surge on a valued whiff: rows {int((fs >= 0).sum())}, step quartiles {q3(fs[fs >= 0])}, at the first valued whiff itself {int(((fs >= 0) & (fs == fv)).sum())};"
                  f" first surge of any kind on a neutral-only whiff {int(fnn.sum())} rows, first surge step quartiles {q3(fn[fn >= 0])}")
            print(f"      holds ended {int(ended.sum())} (timeout flag {int((ended & TO & ~EV).sum())}, evidence {int((ended & EV & ~TO).sum())}, both {int((ended & TO & EV).sum())},"
                  f" neither {int((ended & ~TO & ~EV).sum())}); no whiff of either plume in the last 100 steps {int((~o['W'][-100:].any((0, 2))).sum())};"
                  f" wall contacts {int(o['contacts'].sum())}; cast clock max {o['SINCE'].max():.0f}; `differs` (row, step) {int(o['DIFF'].sum())}")
            ph20b.revision(o, f"{name}: holding valued against time")
            ph20b.transitions(o, f"{name}: revision route")
        pd = first_true((o8["POS"] != o6["POS"]).any(2)); fd = first_true(o8["DIFF"])
        c8, c6 = np.select(list(majority(o8)), [0, 1, 2]), np.select(list(majority(o6)), [0, 1, 2])
        print(f"   Agent8 vs Agent6, same rows: positions first differ in {int((pd >= 0).sum())}/{n} rows, step quartiles {q3(pd[pd >= 0])};"
              f" Agent8's first `differs` step quartiles {q3(fd[fd >= 0])} ({int((fd >= 0).sum())} rows); holding valued at 600 both {int(((a > 0) & (b > 0)).sum())},"
              f" Agent8 only {int(((a > 0) & (b == 0)).sum())}, Agent6 only {int(((a == 0) & (b > 0)).sum())}; dwell class into V {int(((c8 == 0) & (c6 != 0)).sum())}, out of V {int(((c8 != 0) & (c6 == 0)).sum())}")
        print(f"   (b) paired DP holding valued at 600, Agent8 - Agent6: {dp:+.4f} [{lo:+.4f}, {hi:+.4f}] (bootstrap 5000, seed {ph15.BOOT_SEED}); bar lower bound > 0 -> {lab}"
              f" (REPORTED, not a gate; design v2 section 4)")
    return lab, dp, lo, hi


def bench_c(o8, o6, quiet=False):
    """task start, nothing held: every step with nav True has a valued whiff (implementation bar)"""
    ok = ~(o8["NAV"] & ~wv(o8)).any(0); k, pt, lo, hi = interval("P", ok)
    if not quiet:
        n = len(ok); r = np.arange(n); d8, d6 = diagnostics(o8), diagnostics(o6)
        print(f"   (c) Agent8: rows in which every nav step has a valued whiff {k}/{n} = {pt:.3f} [{lo:.3f}, {hi:.3f}] (bar lower bound >= 0.95)")
        for name, o, d in (("Agent8", o8, d8), ("Agent6", o6, d6)):
            fn = first_true(o["NAV"]); has = fn >= 0; t = np.maximum(fn, 0); v = wv(o)[t, r]; nv = o["W"][t, r, 1 - o["good"]]
            V, N, Z = majority(o); kk, p_, l_, h_ = interval("P", V)
            print(f"      {name}: first surge on valued only {int((has & v & ~nv).sum())}, neutral only {int((has & ~v & nv).sum())}, both {int((has & v & nv).sum())}, none {int((~has).sum())};"
                  f" first hold valued {int(d['fh_v'].sum())} neutral {int(d['fh_n'].sum())} none {int((d['ft'] < 0).sum())}, step median {med(d['ft'][d['ft'] >= 0]):.0f};"
                  f" dwell-majority P(V) {kk}/{n} = {p_:.3f} [{l_:.3f}, {h_:.3f}] (preview, no bar); holding valued at 600 {int(hold600(o).sum())}")
        print(f"      first hold identical row for row {int((d8['fh'] == d6['fh']).sum())}/{n}, and at the same step {int(((d8['fh'] == d6['fh']) & (d8['ft'] == d6['ft'])).sum())}")
    return lo


def bench_d(quiet=False):
    res = {}
    for name, cls, f in (("Agent8", Agent8, True), ("Agent6", Agent6, False)):
        o = run((1.0, 0.0), BS, G_STAR, True, f, cls=cls, runs=BENCH["rows"], steps=BENCH["steps"], start="source", hold=True); res[name] = o
        g = o["good"]; parts = []
        for t in (300, 600):
            k, pt, lo, hi = interval("P", o["H"][t - 1] == g); parts.append(f"at {t} {k}/{len(g)} = {pt:.3f} [{lo:.3f}, {hi:.3f}]")
        if not quiet: print(f"   (d) {name}: holding the valued odour " + "; ".join(parts) + f"; no whiff of either plume in the last 100 steps {int((~o['W'][-100:].any((0, 2))).sum())}")
    return res


def bench():
    p = BENCH["p"]
    print(f"== H23 mechanism bench (design v2 section 4). design {DESIGN}; this file sha256 {sha()}; {BENCH}; bootstrap seed {ph15.BOOT_SEED} ==")
    print("   rows share no state: one generator per world and one per agent population, fixed-size draws consumed in row order every step")
    ids = {}
    ids["a1 stub"] = equal(stub([1.0, 0.0], [(BENCH["steps_stub"], p, p)], filt=False), stub([1.0, 0.0], [(BENCH["steps_stub"], p, p)], cls=Agent6))
    ids["a1 stub, channel 1 held"] = equal(stub([1.0, 0.0], [(BENCH["steps_stub"], p, p)], filt=False, hold=1), stub([1.0, 0.0], [(BENCH["steps_stub"], p, p)], cls=Agent6, hold=1))
    o8 = run((1.0, 0.0), BS, G_STAR, True, True); o8f = run((1.0, 0.0), BS, G_STAR, True, False); o6 = run((1.0, 0.0), BS, G_STAR, True, False, cls=Agent6)
    ids["a1 World7 +1/0"] = full(o8f, o6)
    print(f"(a1) filt=False == Agent6 bitwise: stub +1/0 both channels p {p} {BENCH['steps_stub']} steps (H, s, S, nav, since, target) {ids['a1 stub']}; the same with channel 1 held"
          f" {ids['a1 stub, channel 1 held']}; World7 task start {BENCH['rows']} rows x {BENCH['steps']} steps (positions, headings, circuit, H, nav) {ids['a1 World7 +1/0']}")
    for name, kv in (("0/0", (0.0, 0.0)), ("+1/+1", (1.0, 1.0)), ("+1/-1", (1.0, -1.0))):
        s_ok = equal(stub(list(kv), [(BENCH["steps_stub"], p, p)]), stub(list(kv), [(BENCH["steps_stub"], p, p)], cls=Agent6))
        r8 = run(kv, BS, G_STAR, True, True); w_ok = full(r8, run(kv, BS, G_STAR, True, False, cls=Agent6))
        ids[f"a2 {name}"] = s_ok and w_ok
        print(f"(a2) filt=True at {name} == Agent6 bitwise: stub {s_ok}; World7 {BENCH['rows']} x {BENCH['steps']} {w_ok}; `differs` (row, step) {int(r8['DIFF'].sum())}")
    ids["a3"] = equal(stub([1.0, 0.0], [(BENCH["steps_held"], p, 0.0)]), stub([1.0, 0.0], [(BENCH["steps_held"], p, 0.0)], cls=Agent6))
    print(f"(a3) +1/0, channel 0 alone p {p} {BENCH['steps_held']} steps (the valued odour held): bitwise Agent6 {ids['a3']}")
    lo_a4 = bench_a4()
    og0 = run((1.0, 0.0), BS, 0.0, False, True); oh = run((1.0, 0.0), BS, G_STAR, True, True, hold=True)
    ids["a5 G0 gate off"] = traj(o8, og0); ids["a5 neutral hold"] = traj(o8, oh); ids["a5 nav law"] = navlaw(o8) and navlaw(og0) and navlaw(oh)
    print(f"(a5) circuit independence at +1/0, World7 task start {BENCH['rows']} x {BENCH['steps']}: positions and headings of Agent8 (G 2, gate on) == Agent8 at G 0 gate off"
          f" {ids['a5 G0 gate off']}; == Agent8 with a neutral hold constructed at step 0 {ids['a5 neutral hold']}; nav == valued whiff on every (row, step) in all three {ids['a5 nav law']};"
          f" circuit states differ (G 2 vs G 0) {not np.array_equal(o8['S'], og0['S'])}; holding valued at 600: {int(hold600(o8).sum())} / {int(hold600(og0).sum())} / {int(hold600(oh).sum())}")
    print(f"(b) task-like neutral-hold start (ph20b VARIANT state), {BENCH['rows_b']} rows x {BENCH['steps']} steps, Agent8 and Agent6 on the same rows and draws; REPORTED, not a gate")
    lab_b = bench_b()[0]
    print(f"(c) task start, nothing held, {BENCH['rows']} rows x {BENCH['steps']} steps, Agent8 and Agent6 on the same draws")
    lo_c = bench_c(o8, o6)
    print(f"(d) placed at the neutral source with a neutral hold (ph20.bench_d's state) on the H23 bench seeds, {BENCH['rows']} rows x {BENCH['steps']} steps (reported, no bar)")
    bench_d()
    idok = all(ids.values()); verdict = idok and lo_a4 >= 0.95 and lo_c >= 0.95
    print(f"== M4: identities (a1, a2, a3, a5) {idok} {ids}; (a4) lower bound {lo_a4:.3f} >= 0.95 -> {'PASS' if lo_a4 >= 0.95 else 'FAIL'};"
          f" (c) lower bound {lo_c:.3f} >= 0.95 -> {'PASS' if lo_c >= 0.95 else 'FAIL'} -> M4 {'PASS: the task may be run' if verdict else 'FAIL, NO CANDIDATE: the rule as specified does not do what section 3 says; the task is NOT run'};"
          f" bench (b), reported beside it: {lab_b} ==")
    return verdict


# ------------------------------------------------------------------ self-checks
def seeds_unused():
    """design section 9: none of the H23 seeds or their derived generators appears in any other file under the repository
    (recursive; excluded by name: this file, its outputs ph21_*.txt, the H23 documents h23_*.md and master_plan.md)"""
    base = [*SEEDS["dev"], *SEEDS["eval"], BENCH["seed_w"], BENCH["seed_a"], ph15.BOOT_SEED]
    derived = [s + 10_000 for s in (SEEDS["dev"][0], SEEDS["eval"][0], BENCH["seed_w"])] + [s + 20_000 for s in (SEEDS["dev"][1], SEEDS["eval"][1], BENCH["seed_a"])]
    listed = [30261001, 40261002]      # design v2 section 9 lists these as the bench's derived generators (its arithmetic); checked as well
    nums = base + derived + listed
    pat = re.compile(rb"(?<!\d)(" + "|".join(map(str, nums)).encode() + rb")(?!\d)"); hits = []
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for f in files:
            if f == "ph21.py" or (f.startswith("ph21_") and f.endswith(".txt")) or (f.startswith("h23_") and f.endswith(".md")) or f == "master_plan.md": continue
            if pat.search(open(os.path.join(root, f), "rb").read()): hits.append(os.path.relpath(os.path.join(root, f), repo))
    return hits, nums


def pair8(kv_fn, filt, n=40, steps=200, seed=(5, 6)):
    ws = [World7(n, np.random.default_rng(seed[0]), seed[0]) for _ in (0, 1)]; kv = kv_fn(ws[0])
    ag = [Agent8(n, np.random.default_rng(seed[1]), G=G_STAR, known=kv, rule=True, filt=filt), Agent6(n, np.random.default_rng(seed[1]), G=G_STAR, known=kv, rule=True)]
    for a in ag: a.cast_sign = cast_draw(seed[1], n)
    for _ in range(steps):
        for w, a in zip(ws, ag):
            t, _ = a.act(w, w.sense(), w.wind_on()); w.move(t); a.bump(w.bumped)
    return np.array_equal(ws[0].pos, ws[1].pos) and np.array_equal(ws[0].head, ws[1].head) and np.array_equal(ag[0].sel.s, ag[1].sel.s)


def demo():
    print(f"== H23 self-checks (demo). design {DESIGN}; this file sha256 {sha()} ==")
    ph19.demo()                                       # the H21 chain: Agent6 = Agent4 identities, gate, geometry, priority
    n = 40; rows = np.arange(n)
    def kv(w, vg, vo): k = np.zeros((n, 2)); k[rows, w.good] = vg; k[rows, 1 - w.good] = vo; return k
    assert pair8(lambda w: kv(w, 1.0, 0.0), False), "filter off is not Agent6"
    for vg, vo in ((0.0, 0.0), (1.0, 1.0), (1.0, -1.0)):
        assert pair8(lambda w: kv(w, vg, vo), True), f"filter on at {vg}/{vo} is not Agent6"
    assert not pair8(lambda w: kv(w, 1.0, 0.0), True), "filter on at +1/0 changed nothing over 40 rows x 200 steps"
    print("ok  Agent8 with the filter off is Agent6 bitwise; with the filter on it is Agent6 at 0/0, +1/+1 and +1/-1, and differs at +1/0 (40 rows x 200 steps)")
    res = {}
    for f in (True, False):                           # constructed state: neutral held, then neutral-only and valued-only whiffs
        a = Agent8(100, np.random.default_rng(3), G=G_STAR, known=np.tile([1.0, 0.0], (100, 1)), rule=True, filt=f); a.sel.s[:, 1] = 2.0; w = Still(100); nv, hh = [], []
        for ch in (1, 0):
            for _ in range(50):
                x = np.zeros((100, 2), bool); x[:, ch] = True
                _, h = a.act(w, x, np.ones(100, bool)); nv.append((ch, a.nav_hit.copy(), h == 1, a.silence.copy()))
        nn = np.array([z[1] for z in nv[:50]]); hn = np.array([z[2] for z in nv[:50]]); nvv = np.array([z[1] for z in nv[50:]]); hv = np.array([z[2] for z in nv[50:]])
        res[f] = (hn.mean(), nn[hn].mean(), nvv[hv].mean() if hv.any() else float("nan"), max(z[3].max() for z in nv[:50]))
    assert res[True][0] == 1.0 and res[True][1] == 0.0 and res[False][1] == 1.0 and res[True][3] == res[False][3] == 0.0, f"constructed state, neutral whiffs {res}"
    assert res[True][2] == 1.0 and res[False][2] == 0.0, f"constructed state, valued whiffs while neutral held {res}"
    print(f"ok  constructed state, neutral held: with neutral whiffs every step nav True on {res[True][1]*100:.0f}% of held steps with the filter, {res[False][1]*100:.0f}% without,"
          f" the silence timer reset by every hit in both; then with valued whiffs every step, while the neutral odour is still held, nav True on {res[True][2]*100:.0f}% with the filter,"
          f" {res[False][2]*100:.0f}% without")
    seeds = (5, 6)
    flt, mnt = task("filter", seeds, runs=n, steps=200), task("maintain", seeds, runs=n, steps=200)
    assert same(mnt, task("maintain", seeds, runs=n, steps=200, cls=Agent6)), "maintain arm is not Agent6"
    for arm in ("neutral", "priority-identity"):
        assert same(task(arm, seeds, runs=n, steps=200), task(arm, seeds, runs=n, steps=200, cls=Agent6)), f"{arm} arm is not Agent6"
    assert navlaw(flt) and traj(flt, task("filter", seeds, runs=n, steps=200, G=0.0, gate=False)), "filter arm: nav is not the valued whiff, or the circuit steers"
    ok4, cnt = separation(flt, mnt); assert ok4 and cnt["differ"] > 0, f"separation {cnt}"
    ka = task("known-answer", seeds, runs=n, steps=200)
    assert (ka["H"] == ka["good"][None, :]).all() and np.array_equal(ka["NAV"], ka["W"][:, rows, ka["good"]]), "known-answer: h or hit wrong"
    assert np.array_equal(ka["cast"], flt["cast"]) and np.array_equal(ka["good"], flt["good"]), "arms differ in cast draw or assignment"
    assert not flt["DIFF"][(flt["H"] >= 0) & (flt["H"] == flt["good"][None, :])].any(), "a `differs` step while the valued odour was held"
    print(f"ok  run level (40 rows x 200 steps): maintain, neutral and priority-identity arms equal Agent6's runs; filter nav == valued whiff on every (row, step) and its"
          f" trajectory == G 0 gate off; filter vs maintain separation {cnt}; no `differs` step while the valued odour is held; known-answer h and hit; same cast draw and assignment")
    # the bench (b) and (d) states are ph20b's / ph20.bench_d's exactly: rebuilt here on the H22 bench seeds and compared with ph20b.simulate (Agent7, rule off = Agent6)
    hs = (ph20b.ph20.BENCH["seed_w"], ph20b.ph20.BENCH["seed_a"]); nb = ph20b.ph20.BENCH["rows"]
    for start, lab, steps in (("variant", "variant", 600), ("source", "bench", 300)):
        ref = ph20b.simulate(False, steps, lab)
        for cls, f in ((Agent6, False), (Agent8, False)):
            o = run((1.0, 0.0), hs, G_STAR, True, f, cls=cls, runs=nb, steps=steps, start=start, hold=True)
            assert np.array_equal(o["H"], ref["H"]) and np.array_equal(o["W"], ref["W"]), f"{start} start is not ph20b's ({cls.__name__})"
        print(f"ok  the '{start}' start rebuilt here equals ph20b.simulate(rule off, '{lab}') bitwise over {nb} rows x {steps} steps (H, whiffs), with Agent6 and with Agent8 filter off;"
              f" holding valued at step {steps} {int((ref['H'][-1] == ref['good']).sum())}/{nb}")
    hits, nums = seeds_unused(); assert not hits, f"a seed of this run appears in {hits}"
    print(f"ok  seeds {SEEDS}, bench {BENCH['seed_w']}/{BENCH['seed_a']}, bootstrap {ph15.BOOT_SEED} and derived {nums[7:]} appear in no other file under the repository")


# ------------------------------------------------------------------ criteria (design v2 section 7)
def judge(res, maj, first, seeds):
    rows = np.arange(R); ok = lambda z: "PASS" if z else "FAIL"
    print("\n== criteria (design v2 FINAL section 7; 95 percent, one evaluation, no extension; aggregation: PASS if every part passes, FAIL if any fails, else INCONCLUSIVE) ==")
    m1 = []
    for arm in ("neutral", "pathway-off", "known-answer"):
        z = maj[arm][2]; m1.append(ok(z.mean() <= 0.20)); print(f"   M1(a) {arm}: ties {z.sum()}/{R} = {z.mean():.3f}  at most 0.20 -> {m1[-1]}")
    o = res["neutral"]; V, N, Z = maj["neutral"]; which = np.where(V, o["good"], np.where(N, 1 - o["good"], -1))
    m1.append(crit("M1(b) neutral, P(+y source majority | chose)", "P", (0.35, 0.65), False, (which == o["plus_y"])[~Z]))
    V, N, Z = maj["pathway-off"]; m1.append(crit("M1(c) floor: pathway-off, P(V | chose)", "P", (0.35, 0.65), False, V[~Z]))
    m1.append(crit("M1(d) ceiling: known-answer, P(V) over all rows", "P", 0.85, False, maj["known-answer"][0]))
    M1 = agg(m1); print(f"   M1 -> {M1}{'' if M1 == 'PASS' else '  (the run is UNREADABLE under section 8)'}")
    ties = {arm: maj[arm][2].mean() for arm in ("filter", "maintain")}
    print(f"   section 8: ties in the arms under test, filter {ties['filter']:.3f}, maintain {ties['maintain']:.3f} (unreadable above 0.20)")
    Vf, Nf, Zf = maj["filter"]; Vm = maj["maintain"][0]; Vp = maj["pathway-off"][0]; Vk = maj["known-answer"][0]
    m2 = [crit("M2(a) filter, P(V) over all rows", "P", 0.88, False, Vf)]
    for c in range(4): m2.append(crit(f"M2(b) filter, cell {c} ({CELLS[c]}), P(V)", "P", 0.70, False, Vf[res["filter"]["cell"] == c]))
    m2.append(crit("M2(c) DP = P(V) filter - maintain, same rows", "DP", 0.05, False, Vf.astype(float), Vm.astype(float)))
    M2 = agg(m2); print(f"   M2 -> {M2}")
    _, pt, lo, hi = interval("DP", Vf.astype(float), Vp.astype(float)); print(f"      reported, no bar: DP filter - pathway-off {pt:+.3f} [{lo:+.3f}, {hi:+.3f}]")
    print(f"      reported: filter N {Nf.sum()} tie {Zf.sum()}; P(V) filter / known-answer = {Vf.mean():.3f} / {Vk.mean():.3f} = {Vf.mean()/Vk.mean() if Vk.mean() else float('nan'):.3f}"
          f" (predicted 0.97 to 1.03; outside 0.94 to 1.06 would show the random-stream difference matters more than sampling); P(V) maintain / known-answer {Vm.mean()/Vk.mean() if Vk.mean() else float('nan'):.3f}")
    for arm in ("filter", "maintain", "known-answer"):
        d = diagnostics(res[arm]); V = maj[arm][0]
        print(f"      reported: {arm} P(V | first hold valued) {int((V & d['fh_v']).sum())}/{int(d['fh_v'].sum())}, P(V | first hold neutral) {int((V & d['fh_n']).sum())}/{int(d['fh_n'].sum())};"
              f" holding the valued odour at step {T} {int(hold600(res[arm]).sum())}/{R}")
    for arm in ("filter", "maintain", "pathway-off", "known-answer"):
        Vr, Nr, Zr = first[arm]; k, pt, lo, hi = interval("P", Vr)
        print(f"      reported, secondary first reach, {arm}: V {Vr.sum()} N {Nr.sum()} none {Zr.sum()}; P(V first) {k}/{R} = {pt:.3f} [{lo:.3f}, {hi:.3f}]")
    i1 = same(res["maintain"], task("maintain", seeds, cls=Agent6))
    n6 = task("neutral", seeds, cls=Agent6); i2n = same(res["neutral"], n6); i2g0 = same(n6, task("neutral", seeds, cls=Agent6, G=0.0, gate=False)); ag3 = identity_agent3(seeds)
    p6 = task("priority-identity", seeds, cls=Agent6); i2p = same(res["priority-identity"], p6); i2p4 = same(p6, task("priority-identity", seeds, cls=Agent4))
    i3n = navlaw(res["filter"]); i3t = traj(res["filter"], task("filter", seeds, G=0.0, gate=False))
    i4, cnt = separation(res["filter"], res["maintain"])
    ka = res["known-answer"]; i5 = bool((ka["H"] == ka["good"][None, :]).all() and np.array_equal(ka["NAV"], ka["W"][:, rows, ka["good"]]))
    M3 = agg([ok(i1), ok(i2n and i2g0 and ag3 and i2p and i2p4), ok(i3n and i3t), ok(i4), ok(i5)])
    print(f"   M3 identities: (i) maintain (Agent8, filter off) == ph19.Agent6 {i1}; (ii) neutral with the filter == Agent6 {i2n}, Agent6 at 0/0 == G 0 {i2g0}, G 0 == ph14.Agent3 {ag3};"
          f" priority-identity with the filter == Agent6 {i2p}, Agent6 at +1/-1 == ph16.Agent4 {i2p4}; (iii) filter nav == valued whiff on every (row, step) {i3n}, filter positions and"
          f" headings == Agent8 at G 0 gate off {i3t}; (iv) filter vs maintain bitwise equal up to the first `differs` step {i4} {cnt}; (v) known-answer h = valued and hit = its whiffs {i5} -> {M3}")
    lo_a4 = bench_a4(quiet=True); lab_b, dp_b, lo_b, hi_b = bench_b(quiet=True)
    c8 = run((1.0, 0.0), BS, G_STAR, True, True); c6 = run((1.0, 0.0), BS, G_STAR, True, False, cls=Agent6); lo_c = bench_c(c8, c6, quiet=True)
    M4 = agg([ok(lo_a4 >= 0.95), ok(lo_c >= 0.95)])
    print(f"   M4 mechanism bench, (a4), (b) and (c) re-run here with the bench seeds: (a4) lower bound {lo_a4:.3f} >= 0.95; (c) lower bound {lo_c:.3f} >= 0.95 -> {M4};"
          f" reported beside it, not a gate: (b) paired DP holding valued at 600 {dp_b:+.4f} [{lo_b:+.4f}, {hi_b:+.4f}], bar lower bound > 0 -> {lab_b}")
    exp1, cmp1, took = priority_check6(G_STAR)
    M5 = ok(i2p and i2p4)
    print(f"   M5 avoidance: +1/-1 agent is Agent6 = the Run 2 agent by construction (M3 ii {i2p and i2p4}); H21's constructed state: negative odour held on {exp1} (row, step),"
          f" target = flee side on every one, equal to G 0's on the {cmp1} steps both hold it; the valued odour took the hold on {took} afterwards -> {M5}")
    nw_f, nw_m = no_whiff_last_third(res["filter"]).astype(float), no_whiff_last_third(res["maintain"]).astype(float)
    m6 = [crit("M6(a) no whiff of either plume in the last third, filter - maintain", "DP", 0.05, True, nw_f, nw_m)]
    cm = res["filter"]["contacts"].mean(); m6.append(ok(cm <= 0.10)); print(f"   M6(b) filter, wall contacts per row: mean {cm:.3f}  at most 0.10 -> {m6[-1]}")
    M6 = agg(m6)
    print(f"   M6 -> {M6}      reported: no whiff in the last third filter {int(nw_f.sum())} maintain {int(nw_m.sum())} known-answer {int(no_whiff_last_third(res['known-answer']).sum())};"
          f" no navigation hit in the last third " + ", ".join(f"{a} {int(no_nav_last_third(res[a]).sum())}" for a in ARMS)
          + f"; cast clock max filter {res['filter']['SINCE'].max():.0f} maintain {res['maintain']['SINCE'].max():.0f}; `differs` (row, step) filter {int(res['filter']['DIFF'].sum())}")
    unread = M1 != "PASS" or max(ties.values()) > 0.20 or M3 != "PASS"
    verdict = all(x == "PASS" for x in (M1, M2, M3, M4, M5, M6))
    print(f"\n== H23 ==  M1 {M1}  M2 {M2}  M3 {M3}  M4 {M4}  M5 {M5}  M6 {M6}  -> "
          + ("the rule steers only on a top-valued odour whatever is held, and with it the agent stays at the valued source in more rows than the H21 maintain agent,"
             " at P(V) of at least 0.88, without adding lost rows (value-driven navigation in the full agent; not selection controlling navigation)"
             if verdict else "UNREADABLE (section 8)" if unread else "NOT shown under the registered criteria")
          + f"; reported beside it, not part of it: bench (b) {lab_b}")


def main(mode):
    seeds = SEEDS[mode]
    print(f"== H23, {mode.upper()}. design {DESIGN}; this file sha256 {sha()}; G {G_STAR}, gate on where G 2; world seed {seeds[0]}, agent seed {seeds[1]};"
          f" {R} rows x {T} steps; geometry C0; bootstrap seed {ph15.BOOT_SEED}; {'operation check only' if mode == 'dev' else 'the one evaluation'} ==")
    print("   rows share no state: one generator per world and one per agent population, fixed-size draws consumed in row order every step")
    res = {arm: task(arm, seeds) for arm in ARMS}
    maj = {arm: majority(res[arm]) for arm in ARMS}; first = {arm: outcome(res[arm]) for arm in ARMS}
    for arm in ARMS:
        describe_majority(arm, res[arm], *maj[arm]); h21_diag(arm, res[arm]); h23_diag(arm, res[arm], res["maintain"] if arm == "filter" else None)
        print("      secondary, first reach and diagnostics:"); describe(arm, res[arm], *first[arm])
    judge(res, maj, first, seeds)


if __name__ == "__main__":
    mode = ([m for m in sys.argv[1:] if m in ("demo", "bench", "dev", "eval")] or ["demo"])[0]
    if mode == "demo": demo(); sys.exit(0)
    if mode == "bench": sys.exit(0 if bench() else 1)
    main(mode)
