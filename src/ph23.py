#!/usr/bin/env python3
"""H24: presence-scoped value filter (v_max over odours present by a per-odour counter, window N 60, starting ON).

Usage: python ph23.py demo | bench | dev | eval

Design v3 FINAL, confirmed by the owner (decision:h24-open): doc dafaa132a0267d56b, hash 9a217a98...b06c, stored
before this file existed. ONE change to the adopted agent (ph21.Agent8): v_max is taken over the odours present,
present_k = (c_k < N) or k held, c_k = steps since odour k was last sensed (c = 0 at construction, the PRIOR of
decision:classification-rule-relaxed-presence-counter; updated before nav). act is ph21.Agent8.act copied verbatim
with its lines 69-72 replaced by the design's block (section 3). scope 'off' IS Agent8 (checked bitwise). nav6, nav8,
differs, differs8 and present are exposed for measurement only. Worlds: T1 = ph16.World7; T2 = ph22.Masked (W1, W3);
T3 = ph22.Masked with the valued column's mask switched on from the run loop's step t0 = 150. No adopted module is
edited. The bar constants BARS were written in after the bench, from the bench numbers, by decision:h24-t2-dwell-bar
and decision:h24-t3-bars: that is the registered order (design v3 sections 4, 9), not an amendment. dev and eval
refuse to run while they are unset. Nothing changes after the table.
"""
import sys, os, re, math, hashlib
import numpy as np
import ph15, ph19, ph21, ph22
from ph16 import World7, Still, cast_draw, outcome, diagnostics, describe, interval, crit, med, identity_agent3, R, T, DOWN
from ph17 import Agent5
from ph18 import majority, describe_majority, agg
from ph19 import Agent6, same, no_whiff_last_third, no_nav_last_third, h21_diag, priority_check6
from ph16 import Agent4
from ph21 import Agent8, G_STAR, q3, first_true, hold600, h23_diag
from ph11 import RESET_AFTER, MARGIN
from ph12 import SAT
from ph9 import UPWIND, CAST_PERIOD, MAXOFF, GAIN, MAXTURN, TURN_NOISE, angdiff

sys.stdout.reconfigure(newline="\n")            # LF output, so the recorded sha256 equals the committed blob
DESIGN = "v3 FINAL doc dafaa132a0267d56b hash 9a217a989023530644d5573d6fb1d89683eeb5c70b61f1ea400830aa9db1b06c"
PH21_SHA = "3a1d79d9a0d235f1bef7e435ec594cff4048180e27b28dcd892598c58413cfc1"   # the version H23 ran (doc ddcec8520fcd8e23c)
PH22_SHA = "03ab8c4706b19557af5d64edd83f812abba91b618439618b35837a49dd44ca1c"   # the version the absent-odour check ran
N_WIN, T0 = 60, 150
SEEDS = dict(dev=(9885, 9985), eval=(1785, 1885))
BENCH = dict(rows=400, rows_c=800, p=0.30, steps_stub=200, steps_held=260, steps=600, seed_w=20261011, seed_a=20261012)
BS = (BENCH["seed_w"], BENCH["seed_a"])
ph15.BOOT_SEED = 20261013            # design section 7 (set after the imports, which set their own); ph16 set the 95 percent level
# ---- bar constants: filled from bench (d) and (f) by decision:h24-t2-dwell-bar and decision:h24-t3-bars (registered order) ----
BARS = dict(T2=None, D=None, D6=None)   # T2 = bar_T2 (M5 b); D = bar_D (M7 c); D6 = Agent6's bench (f) mean, for M7(c)'s readability
# ----
#            class, (valued value, other value), G, gate, filt, fixed identity
ARMS = {"scoped": (None, (1.0, 0.0), G_STAR, True, True, False), "filter": (Agent8, (1.0, 0.0), G_STAR, True, True, False),
        "maintain": (Agent6, (1.0, 0.0), G_STAR, True, False, False), "pathway-off": (Agent8, (1.0, 0.0), 0.0, False, False, False),
        "known-answer": (Agent8, (1.0, 0.0), 0.0, False, False, True), "neutral": (None, (0.0, 0.0), G_STAR, True, True, False),
        "priority-identity": (None, (1.0, -1.0), G_STAR, True, True, False)}


def sha(p=__file__): return hashlib.sha256(open(p, "rb").read()).hexdigest()


class Agent9(Agent8):
    """ph21.Agent8 plus the H24 presence scope on v_max (design v3 section 3). scope 'off' must BE Agent8 step for step."""

    def __init__(self, runs, rng, scope="prior", N=N_WIN, **kw):
        super().__init__(runs, rng, **kw); self.scope, self.N = scope, N
        self.c = np.zeros((runs, 2)); self.present = np.ones((runs, 2), bool)
        self.nav8 = np.zeros(runs, bool); self.differs8 = np.zeros(runs, bool)

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
        v = self.chan_valence(); vh = v[rows, np.maximum(h, 0)]
        top8 = (v >= 0) & (v == v.max(1)[:, None])                                                   # Agent8's line 69, measurement only
        self.nav8 = np.where((h >= 0) & ((vh == v.max(1)) | (vh < 0)), hit, (whiffs & top8).any(1))  # Agent8's lines 71-72, measurement only
        if self.scope == "prior":                                                                    # H24: the presence scope
            self.c = np.where(whiffs, 0.0, self.c + 1.0)                                              # steps since last sensed; starts at 0 (the prior)
            held = np.zeros_like(whiffs); held[rows, np.maximum(h, 0)] = h >= 0
            self.present = (self.c < self.N) | held
        else:
            self.present = np.ones_like(whiffs)
        vmax = np.where(self.present, v, -np.inf).max(1)
        top = self.present & (v >= 0) & (v == vmax[:, None])
        self.nav6 = hit | ((h < 0) & (whiffs & (v >= 0)).any(1))                                    # Agent6's line, measurement only
        keep = (h >= 0) & ((vh == vmax) | (vh < 0))
        nav = np.where(keep, hit, (whiffs & top).any(1)) if self.filt else self.nav6
        self.differs = nav != self.nav6; self.differs8 = nav != self.nav8
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


def make(cls, runs, rng, G, known, gate, filt, scope="prior"):
    if cls is Agent9: return Agent9(runs, rng, G=G, known=known, rule=gate, filt=filt, scope=scope)
    return ph21.make(cls, runs, rng, G, known, gate, filt)


class Lost(ph22.Masked):
    """T3: ph22.Masked with its mask switched on by the run loop (`on`, set from the step index); World7 exactly while off"""
    on = False

    def sense(self):
        if self.on: return super().sense()
        self.raw = World7.sense(self)
        return self.raw.copy()


# ------------------------------------------------------------------ one run (task and bench; design sections 4-6)
def run(world, cls, vals, seeds, G=G_STAR, gate=True, filt=True, scope="prior", fixed=False, runs=R, steps=T, start="task", hold=False, t0=T0):
    """world 'T1' (World7), 'W1' / 'W3' (ph22.Masked: the valued source A = `good` silenced), 'T3' (Lost, mask on from t0).
    Construction order as ph21.run / ph22.run: world, values, agent, cast draw, position, hold."""
    masked = world != "T1"
    w = (Lost if world == "T3" else ph22.Masked if masked else World7)(runs, np.random.default_rng(seeds[0]), seeds[0])
    rows = np.arange(runs); g = w.good; neutral = 1 - g
    if masked: w.pres = neutral.copy(); w.absent = g.copy()
    tw = World7(runs, np.random.default_rng(seeds[0]), seeds[0]) if masked else None           # the unmasked twin (ph22 R0 iv)
    kv = np.zeros((runs, 2)); kv[rows, g] = vals[0]; kv[rows, neutral] = vals[1]
    rng = np.random.default_rng(seeds[1])
    a = Agent5(runs, rng, fixed=g.copy(), G=0.0, known=kv) if fixed else make(cls, runs, rng, G, kv, gate, filt, scope)
    a.cast_sign = cast_draw(seeds[1], runs)
    if start == "variant": w.pos = w.src[rows, neutral] + np.array([DOWN, 0.0]); w.head = np.full(runs, UPWIND)
    if hold: a.sel.s[rows, neutral] = 2.0
    nine = isinstance(a, Agent9)
    o = dict(world=world, arm=type(a).__name__, good=g, cell=w.cell, plus_y=w.plus_y, pres=neutral, absent=g, G=a.G, fixed=fixed, cast=a.cast_sign.copy(), steps=steps,
             src=w.src[rows, neutral].copy() if world in ("W1", "W3") else w.src.copy(), src2=w.src.copy(), draws_equal=True,
             first=np.full((runs, 2), -1), dwell=np.zeros((runs, 2)), H=np.full((steps, runs), -1, np.int8), W=np.zeros((steps, runs, 2), bool),
             NAV=np.zeros((steps, runs), bool), NAV6=np.zeros((steps, runs), bool), NAV8=np.zeros((steps, runs), bool), PRES=np.ones((steps, runs), bool),
             CNT=np.zeros((steps, runs), np.float32), DIFF=np.zeros((steps, runs), bool), DIFF8=np.zeros((steps, runs), bool),
             TO=np.zeros((steps, runs), bool), EV=np.zeros((steps, runs), bool), SINCE=np.zeros((steps, runs), np.float32), TGT=np.zeros((steps, runs)),
             POS=np.zeros((steps, runs, 2)), HEAD=np.zeros((steps, runs)), S=np.zeros((steps, runs, 2)), AT2=np.zeros((steps, runs, 2), bool),
             AT=np.zeros((steps, runs), bool), C=np.zeros((steps, runs), bool),
             contacts=np.zeros(runs), viol=0, neg_steps=0, neg_rows=np.zeros(runs, bool), ymax=0.0, y_over=0, sat=0, smax=0.0, exit=np.full(runs, -1))
    for t in range(steps):
        if world == "T3": w.on = t >= t0
        if masked: tw.pos, tw.head = w.pos.copy(), w.head.copy()
        whiffs = w.sense()
        if masked: tr = tw.sense()
        on = w.wind_on()
        if masked:
            mon = world != "T3" or t >= t0
            o["draws_equal"] &= bool(np.array_equal(tr, w.raw) and np.array_equal(on, tw.wind_on()) and np.array_equal(whiffs[rows, neutral], tr[rows, neutral])
                                     and np.array_equal(whiffs[rows, g], np.zeros(runs, bool) if mon else tr[rows, g]))
        turn, h = a.act(w, whiffs, on)
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
        o["NAV6"][t] = getattr(a, "nav6", a.nav_hit); o["NAV8"][t] = a.nav8 if nine else a.nav_hit
        if nine: o["PRES"][t] = a.present[rows, g]; o["CNT"][t] = a.c[rows, g]; o["DIFF8"][t] = a.differs8
        o["DIFF"][t] = getattr(a, "differs", False); o["SINCE"][t] = a.since; o["TGT"][t] = a.tgt
        o["POS"][t] = w.pos; o["HEAD"][t] = w.head; o["S"][t] = a.sel.s; o["AT2"][t] = at; o["AT"][t] = at[rows, neutral]; o["C"][t] = w.bumped
        o["contacts"] += w.bumped
    if masked: o["rng_equal"] = w.rng.bit_generator.state == tw.rng.bit_generator.state
    return o


def arm_run(arm, seeds, world="T1", **kw):
    cls, vals, G, gate, filt, fixed = ARMS[arm]
    p = dict(cls=cls or Agent9, vals=vals, G=G, gate=gate, filt=filt, fixed=fixed); p.update(kw)
    return run(world, seeds=seeds, **p)


def r9(world, seeds, vals=(1.0, 0.0), **kw): return run(world, Agent9, vals, seeds, **kw)
def r8(world, seeds, vals=(1.0, 0.0), **kw): return run(world, Agent8, vals, seeds, **kw)
def r6(world, seeds, vals=(1.0, 0.0), **kw): return run(world, Agent6, vals, seeds, filt=False, **kw)


FULL = ("POS", "HEAD", "S", "H", "NAV", "SINCE", "TGT", "W")
def full(o1, o2, n=None, keys=FULL): return all(np.array_equal(o1[k][:n], o2[k][:n]) for k in keys)
def wv(o): return o["W"][:, np.arange(len(o["good"])), o["good"]]
def wn(o): return o["W"][:, np.arange(len(o["good"])), 1 - o["good"]]
def presence_identity(o): return bool(np.array_equal(o["NAV"], np.where(o["PRES"], o["NAV8"], o["NAV6"])))
def held_only(o): return int(((o["H"] == o["good"][None, :]) & (o["CNT"] >= N_WIN)).sum())
def eqmask(o, ref): return (o["POS"] == ref["POS"]).all(2) & (o["HEAD"] == ref["HEAD"]) & (o["S"] == ref["S"]).all(2)


def separation(o, ref, key):
    """bitwise equal to the reference (positions, headings, circuit states) up to the step before the first `key` step"""
    eq = eqmask(o, ref); fd = first_true(o[key]); never = fd < 0; steps = eq.shape[0]
    before = np.arange(steps)[:, None] < np.where(never, steps, fd)[None, :]
    pre = (eq | ~before).all(0); whole = eq.all(0)
    return bool(pre.all() and (whole | ~never).all()), dict(never=int(never.sum()), never_equal=int((never & whole).sum()), differ=int((~never).sum()),
                                                          differ_pre_equal=int((~never & pre).sum()), equal_throughout=int(whole.sum()),
                                                          first_departure=q3(fd[~never]))


def pass_prob(diff, bar):
    """design section 7 arithmetic: normal approximation, se = sd / sqrt(n); the bound clears when the mean >= bar + 1.96 se"""
    m, se = float(np.mean(diff)), float(np.std(diff))/math.sqrt(len(diff))
    return 0.5*(1.0 + math.erf((m - bar - 1.96*se)/se/math.sqrt(2.0))) if se > 0 else float(m >= bar), m, float(np.std(diff))


# ------------------------------------------------------------------ W1 and T3 measures (design sections 5, 7)
def first_surge_ok(o, n0=N_WIN - 1):
    """M5(e) / bench (d): the first surge is the first B whiff at or after step N - 1 (exact, per row)"""
    tt = np.arange(o["steps"])[:, None]; fb = first_true(wn(o) & (tt >= n0)); fs = first_true(o["NAV"])
    return fs == fb, fs, fb


def t3(o, t0=T0):
    """per-row T3 quantities: eligible, L, M7(a) exactness, S (neutral surge in L+1..L+100), delay, dwell 400-599"""
    r = np.arange(len(o["good"])); g = o["good"]; ng = 1 - g; st = o["steps"]; tt = np.arange(st)[:, None]
    v = wv(o); n = wn(o); elig = v[:t0].any(0); L = np.where(elig, t0 - 1 - np.argmax(v[:t0][::-1], 0), -1)
    win = (tt > L) & (tt <= L + N_WIN - 1); after = tt >= L + N_WIN
    a1 = ~(o["NAV"] & win).any(0)
    a2 = first_true(o["NAV"] & (tt > L)) == first_true(n & after)
    a3 = ~((o["H"] == g[None, :]) & after).any(0)
    surge = o["NAV"] & n; S = (surge & (tt > L) & (tt <= L + 100)).any(0); fsa = first_true(surge & (tt > L))
    return dict(elig=elig, L=L, exact=elig & a1 & a2 & a3, a1=a1, a2=a2, a3=a3, S=S, delay=np.where(fsa >= 0, fsa - L, -1),
                dwell=o["AT2"][400:600, r, ng].sum(0).astype(float), hold_n=o["H"][-1] == ng, da=o["POS"][-1, :, 0] - o["src2"][r, ng, 0],
                late=elig & (L >= t0 - N_WIN), nav_n_only=int((o["NAV"] & n & ~v).sum()))


def t3_describe(name, o, d, say=print):
    e = d["elig"]; ne = ~e; k, pt, lo, hi = interval("P", d["S"][e]) if e.sum() else (0, float("nan"), float("nan"), float("nan"))
    say(f"   [T3 {name}] eligible (a valued whiff on steps 0-{T0 - 1}) {int(e.sum())}/{len(e)}, never sensed before t0 {int(ne.sum())}; L quartiles {q3(d['L'][e])};"
        f" L >= t0 - 60 (valued present at t0, lost by the mask) {int(d['late'].sum())}; S (neutral surge on L+1..L+100, eligible rows) {k}/{int(e.sum())} = {pt:.3f} [{lo:.3f}, {hi:.3f}];"
        f" first-neutral-surge delay after L {q3(d['delay'][e & (d['delay'] >= 0)])} (none {int((e & (d['delay'] < 0)).sum())})")
    say(f"      dwell within 3.0 of the neutral source, steps 400-599: mean {d['dwell'].mean():.2f}, quartiles {q3(d['dwell'])} (eligible {d['dwell'][e].mean() if e.any() else float('nan'):.2f},"
        f" never sensed {d['dwell'][ne].mean() if ne.any() else float('nan'):.2f}); holding neutral at 600 {int(d['hold_n'].sum())} (never-sensed rows {int((d['hold_n'] & ne).sum())});"
        f" d_along from the neutral source at 600 {q3(d['da'])}; nav on a neutral-only whiff (row, step) {d['nav_n_only']}; held-only valued presence (row, step) {held_only(o)}")


# ------------------------------------------------------------------ the mechanism bench (design section 4)
def stub(known, sched, cls=Agent9, scope="prior", filt=True, rows=BENCH["rows"], hold=None):
    """Still stub; sched: list of (steps, p channel 0, p channel 1); the same uniform draws for every condition; hold: channel set to s 2.0"""
    steps = sum(s for s, _, _ in sched); u = np.random.default_rng(BENCH["seed_w"]).random((steps, rows, 2))
    a = make(cls, rows, np.random.default_rng(BENCH["seed_a"]), G_STAR, np.tile(known, (rows, 1)), True, filt, scope); w = Still(rows)
    if hold is not None: a.sel.s[:, hold] = 2.0
    rec = {k: [] for k in ("H", "s", "S", "NAV", "SINCE", "TGT", "X", "P", "C", "N8", "N6")}; t = 0
    for n, p0, p1 in sched:
        for _ in range(n):
            x = np.stack([u[t, :, 0] < p0, u[t, :, 1] < p1], 1)
            _, h = a.act(w, x, np.ones(rows, bool)); t += 1
            for k, v in (("H", h), ("s", a.sel.s), ("S", a.sel.S), ("NAV", a.nav_hit), ("SINCE", a.since), ("TGT", a.tgt), ("X", x),
                         ("P", getattr(a, "present", np.ones((rows, 2), bool))), ("C", getattr(a, "c", np.zeros((rows, 2)))),
                         ("N8", getattr(a, "nav8", a.nav_hit)), ("N6", getattr(a, "nav6", a.nav_hit))): rec[k].append(np.array(v).copy())
    return {k: np.array(v) for k, v in rec.items()}


K_STUB = ("H", "s", "S", "NAV", "SINCE", "TGT")
def equal(r1, r2, keys=K_STUB): return all(np.array_equal(r1[k], r2[k]) for k in keys)


def counter_exact(r):
    """bench (b): per row, c follows c <- 0 on a whiff else c + 1 from 0 exactly, and present == (c < N) or held"""
    X = r["X"]; steps, rows, _ = X.shape; c = np.zeros((rows, 2)); ok = np.ones(rows, bool); ho = 0
    for t in range(steps):
        c = np.where(X[t], 0.0, c + 1.0); held = np.zeros((rows, 2), bool); h = r["H"][t]; held[np.arange(rows), np.maximum(h, 0)] = h >= 0
        ok &= (r["C"][t] == c).all(1) & (r["P"][t] == ((c < N_WIN) | held)).all(1); ho += int((held & (c >= N_WIN)).sum())
    return ok, ho


def bench(quiet=False):
    say = (lambda *a, **k: None) if quiet else print; p = BENCH["p"]; n = BENCH["rows"]; st = BENCH["steps"]; t = np.arange(st)[:, None]
    say(f"== H24 mechanism bench (design v3 section 4). design {DESIGN}; this file sha256 {sha()}; ph21.py {sha(ph21.__file__)}; ph22.py {sha(ph22.__file__)};"
        f" {BENCH}; N {N_WIN}; t0 {T0}; bootstrap seed {ph15.BOOT_SEED} ==")
    say("   rows share no state: one generator per world and one per agent population, fixed-size draws consumed in row order every step")
    ids, bars, out = {}, {}, {}
    both = [(BENCH["steps_stub"], p, p)]
    ids["a1 stub"] = equal(stub([1.0, 0.0], both, scope="off"), stub([1.0, 0.0], both, cls=Agent8))
    ids["a1 stub, channel 1 held"] = equal(stub([1.0, 0.0], both, scope="off", hold=1), stub([1.0, 0.0], both, cls=Agent8, hold=1))
    o9 = r9("T1", BS); o9off = r9("T1", BS, scope="off"); o8 = r8("T1", BS); o6 = r6("T1", BS)
    ids["a1 World7 +1/0"] = full(o9off, o8)
    say(f"(a1) scope 'off' == Agent8 bitwise: stub +1/0 both channels p {p} {BENCH['steps_stub']} steps (H, s, S, nav, since, target) {ids['a1 stub']}; the same with channel 1 held"
        f" {ids['a1 stub, channel 1 held']}; World7 task start {n} x {st} (positions, headings, circuit, H, nav, since, target, whiffs) {ids['a1 World7 +1/0']}")
    for name, kv in (("0/0", (0.0, 0.0)), ("+1/+1", (1.0, 1.0)), ("+1/-1", (1.0, -1.0))):
        s_ok = equal(stub(list(kv), both), stub(list(kv), both, cls=Agent6))
        a9 = r9("T1", BS, kv); w_ok = full(a9, r6("T1", BS, kv)); ids[f"a2 {name}"] = s_ok and w_ok
        say(f"(a2) scope 'prior' at {name} == Agent6 bitwise: stub {s_ok}; World7 {n} x {st} {w_ok}; `differs` (row, step) {int(a9['DIFF'].sum())}; valued-present fraction {a9['PRES'].mean():.3f}")
    held_sched = [(BENCH["steps_held"], p, 0.0)]; s9 = stub([1.0, 0.0], held_sched)
    ids["a3"] = equal(s9, stub([1.0, 0.0], held_sched, cls=Agent8)) and equal(s9, stub([1.0, 0.0], held_sched, cls=Agent6))
    say(f"(a3) +1/0, channel 0 alone p {p} {BENCH['steps_held']} steps (the valued odour held): == Agent8 == Agent6 bitwise {ids['a3']}")
    ids["a4 presence identity"] = presence_identity(o9)
    say(f"(a4) presence identity, World7 +1/0 {n} x {st}: nav == nav8 where the valued odour is present and == nav6 where it is not, every (row, step): {ids['a4 presence identity']};"
        f" valued present on {o9['PRES'].mean():.3f} of (row, step); `differs8` (row, step) {int(o9['DIFF8'].sum())} in {int(o9['DIFF8'].any(0).sum())} rows;"
        f" rows bitwise Agent8 throughout {int(eqmask(o9, o8).all(0).sum())}, bitwise Agent6 throughout {int(eqmask(o9, o6).all(0).sum())}")
    w9, w8, w6 = r9("W1", BS), r8("W1", BS), r6("W1", BS)
    ids["a5 W1 == Agent8 on 0-58"] = full(w9, w8, N_WIN - 1); ids["a5 W1 nav == nav6 from 59"] = bool(np.array_equal(w9["NAV"][N_WIN - 1:], w9["NAV6"][N_WIN - 1:]))
    ids["a5 W1 presence 0-58 only, draws"] = bool(w9["PRES"][:N_WIN - 1].all() and not w9["PRES"][N_WIN - 1:].any() and all(o["draws_equal"] and o["rng_equal"] for o in (w9, w8, w6)))
    say(f"(a5) W1 (ph22.Masked, A silenced) {n} x {st}: Agent9 == Agent8 bitwise on steps 0-{N_WIN - 2} {ids['a5 W1 == Agent8 on 0-58']}; nav == nav6 on every step from {N_WIN - 1}"
        f" {ids['a5 W1 nav == nav6 from 59']}; A present exactly on steps 0-{N_WIN - 2}, masked draws == World7's twin, generator state equal {ids['a5 W1 presence 0-58 only, draws']}")
    # (b) counter dynamics
    sch = {"no whiff": [(200, 0.0, 0.0)], "one whiff on channel 0 at step 0": [(1, 1.0, 0.0), (199, 0.0, 0.0)], "20-step p 0.30 burst on channel 0": [(20, p, 0.0), (180, 0.0, 0.0)]}
    rb = {k: stub([1.0, 0.0], s) for k, s in sch.items()}; okb = np.ones(n, bool); ho = 0; tb = np.arange(200)[:, None]
    for k, r in rb.items():
        ok, h = counter_exact(r); okb &= ok; ho += h
        pat = ""
        if k == "no whiff": pat = f"c == t + 1 {bool((r['C'] == tb[:, :, None] + 1).all())}, present exactly on steps 0-58 {bool((r['P'] == (tb <= 58)[:, :, None]).all())}"
        if k.startswith("one"): pat = f"c_0 == t {bool((r['C'][:, :, 0] == tb).all())}, channel 0 present exactly on steps 0-59 {bool((r['P'][:, :, 0] == (tb <= 59)).all())}"
        if k.startswith("20"):
            x0 = r["X"][:, :, 0]; had = x0.any(0); Lr = 199 - np.argmax(x0[::-1], 0)
            pat = (f"rows with a whiff {int(had.sum())}, last whiff step quartiles {q3(Lr[had])}; channel 0 absent from exactly 60 steps after the last whiff in"
                   f" {int((had & (r['P'][:, :, 0] == (tb < Lr[None, :] + 60)).all(0)).sum())}/{int(had.sum())}")
        say(f"(b) {k}: rows exact {int(ok.sum())}/{n}; {pat}; valued holds in this stub {int((r['H'] == 0).any(0).sum())} rows; held-only presence with c >= 60 {h}")
    k_, pt, lo_b, hi = interval("P", okb); bars["b"] = lo_b
    say(f"(b) counter exact in every schedule: {k_}/{n} = {pt:.3f} [{lo_b:.3f}, {hi:.3f}] (bar lower bound >= 0.95); held clause the only reason for presence with c >= 60: {ho} (row, step), expected 0")
    # (c) task-like neutral-hold start, reported
    nc = BENCH["rows_c"]; c9, c8, c6 = (f("T1", BS, runs=nc, start="variant", hold=True) for f in (r9, r8, r6))
    hn = c9["H"] == (1 - c9["good"])[None, :]; frac = c9["PRES"][hn].mean() if hn.any() else float("nan")
    say(f"(c) task-like neutral-hold start (ph20b VARIANT state, neutral hold s 2.0), {nc} rows x {st} steps, REPORTED, not a gate: neutral-held (row, step) {int(hn.sum())},"
        f" fraction with the valued odour present (Agent9) {frac:.3f} (of them within the first 59 steps {(c9['PRES'] & hn)[:59].sum() / max(hn.sum(), 1):.3f});"
        f" rows with a valued whiff by 600 {int(wv(c9).any(0).sum())}; held-only presence {held_only(c9)}")
    for name, o in (("Agent9", c9), ("Agent8", c8), ("Agent6", c6)):
        k, pt, l, h = interval("P", hold600(o)); say(f"      {name}: holding the valued odour at step {st} {k}/{nc} = {pt:.3f} [{l:.3f}, {h:.3f}]")
    for name, o in (("Agent8", c8), ("Agent6", c6)):
        _, dp, l, h = interval("DP", hold600(c9).astype(float), hold600(o).astype(float)); say(f"      paired DP holding valued at 600, Agent9 - {name}: {dp:+.4f} [{l:+.4f}, {h:+.4f}]")
    # (d) W1 on bench seeds: implementation bar and the measurement that fixes M5(b)'s bar
    ok_d, fs, fb = first_surge_ok(w9); k_, pt, lo_d, hi = interval("P", ok_d); bars["d"] = lo_d
    d9, d8, d6 = (o["AT"].sum(0).astype(float) for o in (w9, w8, w6)); D6W1 = float(d6.mean()); bar_t2 = round(-0.20*D6W1, 1)
    pp, m, sd = pass_prob(d9 - d6, bar_t2); _, _, blo, bhi = interval("DP", d9, d6)
    say(f"(d) W1, bench seeds, {n} x {st}: first surge == first B whiff at or after step {N_WIN - 1} in {k_}/{n} = {pt:.3f} [{lo_d:.3f}, {hi:.3f}] (bar lower bound >= 0.95);"
        f" first-surge step quartiles {q3(fs[fs >= 0])} (rows {int((fs >= 0).sum())}), within N + 40 = step 99 {int(((fs >= 0) & (fs <= 99)).sum())}")
    for name, o, d in (("Agent9", w9, d9), ("Agent8", w8, d8), ("Agent6", w6, d6)):
        s = ph22.summary(o); say(f"      {name}: mean dwell within 3.0 over {st} steps {d.mean():.3f} (median {med(d):.1f}); reach {int(s['reach'].sum())}/{n}; lost rows {int(s['lost'].sum())};"
                                 f" wall contacts per row {s['contacts'].mean():.3f}; holding B at {st} {int(s['heldB_end'].sum())}; d_along at {st} {ph22.q3(s['da_end'], '.1f')}")
    say(f"   (d) measured: D6_W1 (Agent6's mean W1 dwell) = {D6W1:.4f}; rule bar_T2 = -0.20 x D6_W1 rounded to 0.1 = {bar_t2:+.1f}; paired Agent9 - Agent6 mean {m:+.4f} sd {sd:.4f}"
        f" (bootstrap [{blo:+.4f}, {bhi:+.4f}]); Agent8 - Agent6 mean {(d8 - d6).mean():+.4f}; M5(b) pass probability at the measured difference (design arithmetic) {pp:.4f}")
    out.update(D6_W1=D6W1, bar_T2=bar_t2, m_T2=m, sd_T2=sd, pp_T2=pp, d9_W1=float(d9.mean()), d8_W1=float(d8.mean()))
    # (e) H23's implementation bars re-run
    ra = stub([1.0, 0.0], both, hold=1); ok_e1 = ((ra["NAV"] == ra["X"][:, :, 0]) | ~ra["P"][:, :, 0]).all(0); _, pt1, lo_e1, _ = interval("P", ok_e1)
    ok_e2 = ~(o9["NAV"] & o9["PRES"] & ~wv(o9)).any(0); _, pt2, lo_e2, _ = interval("P", ok_e2); bars["e a4'"] = lo_e1; bars["e c'"] = lo_e2
    say(f"(e) (a4') channel 1 held by construction, both channels p {p}, {BENCH['steps_stub']} steps: nav == channel 0's whiff on every step on which channel 0 is present in"
        f" {int(ok_e1.sum())}/{n} = {pt1:.3f}, lower bound {lo_e1:.3f} (>= 0.95); (c') task start: every nav step with the valued odour present has a valued whiff in {int(ok_e2.sum())}/{n}"
        f" = {pt2:.3f}, lower bound {lo_e2:.3f} (>= 0.95)")
    # (f) T3 construction and bar measurement
    f9, f8, f6 = r9("T3", BS), r8("T3", BS), r6("T3", BS)
    ids["f construction: draws"] = all(o["draws_equal"] and o["rng_equal"] for o in (f9, f8, f6))
    ids["f construction: T3 == World7 run before t0"] = full(f9, o9, T0) and full(f8, o8, T0) and full(f6, o6, T0)
    say(f"(f) T3 (Lost, mask on from step {T0}), bench seeds {n} x {st}: whiffs == the World7 twin's in both columns before t0, valued column False and neutral == twin from t0,"
        f" wind draws equal, generator state equal, all three arms {ids['f construction: draws']}; each arm's T3 run == its World7 run on steps 0-{T0 - 1} bitwise"
        f" {ids['f construction: T3 == World7 run before t0']}; Agent9 presence identity {presence_identity(f9)}")
    dd = {name: t3(o) for name, o in (("Agent9", f9), ("Agent8", f8), ("Agent6", f6))}
    for name, o in (("Agent9", f9), ("Agent8", f8), ("Agent6", f6)): t3_describe(name, o, dd[name], say)
    e9 = dd["Agent9"]["elig"]; k_, pt, lo_f, hi = interval("P", dd["Agent9"]["exact"][e9]); bars["f M7(a)"] = lo_f
    D6 = float(dd["Agent6"]["dwell"].mean()); bar_d = -0.20*D6; S6 = float(dd["Agent6"]["S"][dd["Agent6"]["elig"]].mean())
    ppd, md, sdd = pass_prob(dd["Agent9"]["dwell"] - dd["Agent6"]["dwell"], bar_d); _, _, dlo, dhi = interval("DP", dd["Agent9"]["dwell"], dd["Agent6"]["dwell"])
    eb = e9 & dd["Agent6"]["elig"]; _, sdp, slo, shi = interval("DP", dd["Agent9"]["S"][eb].astype(float), dd["Agent6"]["S"][eb].astype(float))
    say(f"(f) M7(a) exactness, Agent9, eligible rows: {k_}/{int(e9.sum())} = {pt:.3f} [{lo_f:.3f}, {hi:.3f}] (bar lower bound >= 0.95); parts (no nav on L+1..L+59, first neutral surge"
        f" = first neutral whiff at or after L+60, valued not held from L+60): {int(dd['Agent9']['a1'][e9].sum())}/{int(dd['Agent9']['a2'][e9].sum())}/{int(dd['Agent9']['a3'][e9].sum())}")
    say(f"   (f) measured: D6 (Agent6's mean neutral dwell, steps 400-599) = {D6:.4f}; rule bar_D = -0.20 x D6 = {bar_d:+.4f}; paired Agent9 - Agent6 mean {md:+.4f} sd {sdd:.4f}"
        f" (bootstrap [{dlo:+.4f}, {dhi:+.4f}]); Agent8 - Agent6 {(dd['Agent8']['dwell'] - dd['Agent6']['dwell']).mean():+.4f}; M7(c) pass probability at the measured difference {ppd:.4f}")
    say(f"   (f) reported: S6 (Agent6's S, eligible rows) = {S6:.4f} (readability note for M7(b): pinned if < 0.10 -> {'PINNED' if S6 < 0.10 else 'not pinned'});"
        f" S Agent9 {dd['Agent9']['S'][e9].mean():.4f}, Agent8 {dd['Agent8']['S'][dd['Agent8']['elig']].mean():.4f}; paired S Agent9 - Agent6 over rows eligible in both ({int(eb.sum())})"
        f" {sdp:+.4f} [{slo:+.4f}, {shi:+.4f}]")
    out.update(D6=D6, bar_D=bar_d, m_D=md, sd_D=sdd, pp_D=ppd, S6=S6)
    idok = all(ids.values()); bok = all(v >= 0.95 for v in bars.values()); verdict = idok and bok
    say(f"== M4: identities (a1-a5, (f) construction) {idok} {ids}; implementation bars (lower bounds >= 0.95) {bok} " + str({k: round(v, 4) for k, v in bars.items()})
        + f" -> M4 {'PASS: the tasks may be run' if verdict else 'FAIL, NO CANDIDATE: the rule as specified does not do what section 3 says; the tasks are NOT run'}; (c) reported beside it ==")
    return verdict, out, ids, bars


# ------------------------------------------------------------------ self-checks
def seeds_unused():
    """design section 9: none of the H24 seeds or their derived generators appears in any other file under the repository (recursive, digit-boundary;
    excluded by name: this file, its outputs ph23_*.txt, the H24 documents h24_*.md, master_plan.md, notes/*.md)"""
    base = [*SEEDS["dev"], *SEEDS["eval"], BENCH["seed_w"], BENCH["seed_a"], ph15.BOOT_SEED]
    derived = [s + 10_000 for s in (SEEDS["dev"][0], SEEDS["eval"][0], BENCH["seed_w"])] + [s + 20_000 for s in (SEEDS["dev"][1], SEEDS["eval"][1], BENCH["seed_a"])]
    nums = base + derived + [30261011, 40261012]
    pat = re.compile(rb"(?<!\d)(" + "|".join(map(str, nums)).encode() + rb")(?!\d)"); hits = []; nf = 0
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for f in files:
            if f == "ph23.py" or (f.startswith("ph23_") and f.endswith(".txt")) or (f.startswith("h24_") and f.endswith(".md")) or f == "master_plan.md": continue
            if os.path.basename(root) == "notes" and f.endswith(".md"): continue
            nf += 1
            if pat.search(open(os.path.join(root, f), "rb").read()): hits.append(os.path.relpath(os.path.join(root, f), repo))
    return hits, nums, nf


def demo():
    print(f"== H24 self-checks (demo). design {DESIGN}; this file sha256 {sha()}; ph21.py sha256 {sha(ph21.__file__)}; ph22.py sha256 {sha(ph22.__file__)} ==")
    assert sha(ph21.__file__) == PH21_SHA and sha(ph22.__file__) == PH22_SHA, "ph21.py or ph22.py is not the version that ran"
    ph19.demo()                                       # the H21 chain: Agent6 = Agent4 identities, gate, geometry, priority
    seeds, n, steps = (5, 6), 40, 300
    kw = dict(runs=n, steps=steps)
    o9off, o8 = r9("T1", seeds, scope="off", **kw), r8("T1", seeds, **kw)
    assert full(o9off, o8), "scope 'off' is not Agent8"
    ref = ph21.run((1.0, 0.0), seeds, G_STAR, True, True, runs=n, steps=steps)
    assert all(np.array_equal(o8[k], ref[k]) for k in ("POS", "HEAD", "S", "H", "NAV", "W", "SINCE")), "this file's World7 run is not ph21.run"
    for kv in ((0.0, 0.0), (1.0, 1.0), (1.0, -1.0)):
        assert full(r9("T1", seeds, kv, **kw), r6("T1", seeds, kv, **kw)), f"scope 'prior' at {kv} is not Agent6"
    o9 = r9("T1", seeds, **kw); o6 = r6("T1", seeds, **kw)
    assert presence_identity(o9) and not full(o9, o6) and o9["PRES"][:59].all(), "presence identity, or no difference from Agent6, or the prior"
    ok8, c8 = separation(o9, o8, "DIFF8"); ok6, c6 = separation(o9, o6, "DIFF"); assert ok8 and ok6, f"separation {c8} {c6}"
    print(f"ok  Agent9 scope 'off' == Agent8 bitwise and this file's World7 run == ph21.run (40 x 300); scope 'prior' == Agent6 at 0/0, +1/+1, +1/-1; at +1/0 the presence identity"
          f" holds on every (row, step); separation vs Agent8 {c8}, vs Agent6 {c6}")
    for arm in ("Agent8", "Agent6"):
        mine = (r8 if arm == "Agent8" else r6)("W1", seeds, **kw); theirs = ph22.run("W1", arm, seeds, n, steps)
        assert all(np.array_equal(mine[k], theirs[k]) for k in ("POS", "HEAD", "S", "H", "NAV", "W", "AT")) and mine["draws_equal"] and mine["rng_equal"], f"W1 {arm} is not ph22.run's"
    w9, w8 = r9("W1", seeds, **kw), r8("W1", seeds, **kw)
    assert full(w9, w8, 59) and np.array_equal(w9["NAV"][59:], w9["NAV6"][59:]) and w9["PRES"][:59].all() and not w9["PRES"][59:].any(), "W1 identity"
    assert full(r9("W3", seeds, (0.0, 0.0), **kw), r6("W3", seeds, (0.0, 0.0), **kw)), "W3: Agent9 is not Agent6"
    ok, fs, fb = first_surge_ok(w9); assert ok.all(), "W1 first surge"
    print(f"ok  W1 runs here == ph22.run (Agent8, Agent6; positions, circuit, holds, nav, whiffs, at-source); Agent9 in W1 == Agent8 on steps 0-58, nav == nav6 from 59, A present on 0-58 only,"
          f" first surge = first B whiff at or after 59 in every row; W3 Agent9 == Agent6")
    for f, name in ((r9, "Agent9"), (r8, "Agent8"), (r6, "Agent6")):
        a, b = f("T3", seeds, **kw), f("T1", seeds, **kw)
        assert a["draws_equal"] and a["rng_equal"] and full(a, b, T0) and not full(a, b, T0 + 30) and not wv(a)[T0:].any(), f"T3 construction {name}"
    f9 = r9("T3", seeds, **kw); d = t3(f9); assert presence_identity(f9), "T3 presence identity"
    assert not (r8("T3", seeds, **kw)["NAV"] & ~wv(r8("T3", seeds, **kw))).any(), "Agent8 surged on a neutral-only whiff"
    e = d["elig"]      # M7(a) is the bench's measurement (bench (f), M4), not a self-check: printed here, not asserted
    print(f"ok  T3 (mask on from step {T0}): masked draws == World7 twin, generator state equal; every arm == its T1 run on steps 0-{T0 - 1} and departs after; presence identity;"
          f" Agent8's nav never on a neutral-only whiff (40 x 300). Printed, not asserted: M7(a) exact in {int(d['exact'][e].sum())}/{int(e.sum())} eligible rows (parts: no nav on"
          f" L+1..L+59 {int(d['a1'][e].sum())}, first neutral surge = first neutral whiff at or after L+60 {int(d['a2'][e].sum())}, valued not held from L+60 {int(d['a3'][e].sum())})")
    r = stub([1.0, 0.0], [(1, 1.0, 0.0), (99, 0.0, 0.0)], rows=20); ok, ho = counter_exact(r)
    tb = np.arange(100)[:, None]
    assert ok.all() and (r["C"][:, :, 0] == tb).all() and (r["C"][:, :, 1] == tb + 1).all() and (r["P"][:, :, 1] == (tb <= 58)).all(), "counter convention"
    print(f"ok  counter convention: c = 0 at construction, updated before nav (one whiff on channel 0 at step 0: c_0 = t, c_1 = t + 1; present == (c < 60) or held on every step;"
          f" channel 1, never sensed, present exactly on steps 0-58). Printed, not asserted (bench (b) measures it): channel 0 present exactly on steps 0-59 in"
          f" {int((r['P'][:, :, 0] == (tb <= 59)).all(0).sum())}/20 rows; held clause the only reason for presence with c >= 60 on {ho} (row, step); channel 0 held at step 99 in"
          f" {int((r['H'][-1] == 0).sum())}/20 rows")
    hits, nums, nf = seeds_unused(); assert not hits, f"a seed of this run appears in {hits}"
    print(f"ok  seeds {SEEDS}, bench {BENCH['seed_w']}/{BENCH['seed_a']}, bootstrap {ph15.BOOT_SEED} and derived {nums[7:]} appear in no other file under the repository"
          f" ({nf} files scanned; excluded by name ph23.py, ph23_*.txt, h24_*.md, master_plan.md, notes/*.md)")


# ------------------------------------------------------------------ criteria (design v3 section 7)
def judge(t1, maj, first, t2, t3r, seeds):
    rows = np.arange(R); ok = lambda z: "PASS" if z else "FAIL"
    print("\n== criteria (design v3 FINAL section 7; 95 percent, one evaluation, no extension; aggregation: PASS if every part passes, FAIL if any fails, else INCONCLUSIVE;"
          " the unrounded bound decides) ==")
    print(f"   bars read from BARS: bar_T2 {BARS['T2']} (decision:h24-t2-dwell-bar), bar_D {BARS['D']} and D6 {BARS['D6']} (decision:h24-t3-bars)")
    m1 = []
    for arm in ("neutral", "pathway-off", "known-answer"):
        z = maj[arm][2]; m1.append(ok(z.mean() <= 0.20)); print(f"   M1(a) {arm}: ties {z.sum()}/{R} = {z.mean():.3f}  at most 0.20 -> {m1[-1]}")
    o = t1["neutral"]; V, N, Z = maj["neutral"]; which = np.where(V, o["good"], np.where(N, 1 - o["good"], -1))
    m1.append(crit("M1(b) neutral, P(+y source majority | chose)", "P", (0.35, 0.65), False, (which == o["plus_y"])[~Z]))
    V, N, Z = maj["pathway-off"]; m1.append(crit("M1(c) floor: pathway-off, P(V | chose)", "P", (0.35, 0.65), False, V[~Z]))
    m1.append(crit("M1(d) ceiling: known-answer, P(V) over all rows", "P", 0.85, False, maj["known-answer"][0]))
    M1 = agg(m1); print(f"   M1 -> {M1}{'' if M1 == 'PASS' else '  (the run is UNREADABLE under section 8)'}")
    ties = {arm: maj[arm][2].mean() for arm in ("scoped", "filter", "maintain")}
    print("   section 8: ties in the arms under test " + ", ".join(f"{a} {v:.3f}" for a, v in ties.items()) + " (unreadable above 0.20)")
    Vs, Ns, Zs = maj["scoped"]; Vf = maj["filter"][0]; Vm = maj["maintain"][0]; Vk = maj["known-answer"][0]
    m2 = [crit("M2(a) scoped, P(V) over all rows", "P", 0.88, False, Vs),
          crit("M2(b) DP = P(V) scoped - filter, same rows", "DP", -0.05, False, Vs.astype(float), Vf.astype(float)),
          crit("M2(c) DP = P(V) scoped - maintain, same rows", "DP", 0.05, False, Vs.astype(float), Vm.astype(float))]
    M2 = agg(m2); print(f"   M2 -> {M2}")
    e8, e6 = eqmask(t1["scoped"], t1["filter"]).all(0), eqmask(t1["scoped"], t1["maintain"]).all(0)
    for a in ("scoped", "filter", "maintain"):
        k, pt, lo, hi = interval("P", maj[a][0]); print(f"      reported: {a} V {maj[a][0].sum()} N {maj[a][1].sum()} tie {maj[a][2].sum()}; P(V) {k}/{R} = {pt:.3f} [{lo:.3f}, {hi:.3f}]")
    print(f"      reported: scoped rows bitwise Agent8 throughout {int(e8.sum())}, bitwise Agent6 throughout {int(e6.sum())}, both {int((e8 & e6).sum())}, neither {int((~e8 & ~e6).sum())};"
          f" P(V) scoped / known-answer {Vs.mean() / Vk.mean() if Vk.mean() else float('nan'):.3f}; V among rows bitwise Agent8 {int(Vs[e8].sum())}, Agent6-only {int(Vs[e6 & ~e8].sum())}, neither {int(Vs[~e8 & ~e6].sum())}")
    # M3
    i = {}
    i["scope off == Agent8"] = full(arm_run("scoped", seeds, scope="off"), t1["filter"])
    i["maintain == ph19.Agent6 run"] = same(t1["maintain"], ph19.run("maintain", seeds))
    n6 = arm_run("neutral", seeds, cls=Agent6, filt=False); pi6 = arm_run("priority-identity", seeds, cls=Agent6, filt=False)
    i["neutral == Agent6"] = full(t1["neutral"], n6); i["priority-identity == Agent6"] = full(t1["priority-identity"], pi6)
    i["H21 chain: Agent6 0/0 == G 0 gate off, G 0 == Agent3, Agent6 +1/-1 == Agent4"] = (same(n6, arm_run("neutral", seeds, cls=Agent6, filt=False, G=0.0, gate=False))
                                                                                         and identity_agent3(seeds) and same(pi6, arm_run("priority-identity", seeds, cls=Agent4, filt=False)))
    i["presence identity T1, T2, T3"] = presence_identity(t1["scoped"]) and presence_identity(t2[("W1", "scoped")]) and presence_identity(t3r["scoped"])
    s8, c8 = separation(t1["scoped"], t1["filter"], "DIFF8"); s6, c6 = separation(t1["scoped"], t1["maintain"], "DIFF")
    s83, c83 = separation(t3r["scoped"], t3r["filter"], "DIFF8"); i["separation T1 vs filter, vs maintain; T3 vs filter"] = s8 and s6 and s83
    i["W3 Agent9 == Agent6"] = full(t2[("W3", "scoped")], t2[("W3", "maintain")])
    w9 = t2[("W1", "scoped")]
    i["W1 == Agent8 on 0-58, nav == nav6 from 59"] = full(w9, t2[("W1", "filter")], N_WIN - 1) and bool(np.array_equal(w9["NAV"][N_WIN - 1:], w9["NAV6"][N_WIN - 1:]))
    i["masked draws == World7 twin (W1, W3, T3)"] = all(o["draws_equal"] and o["rng_equal"] for o in list(t2.values()) + list(t3r.values()))
    i["T3 == T1 on steps 0-149, every arm"] = all(full(t3r[a], t1[a], T0) for a in ("scoped", "filter", "maintain"))
    i["Agent8 nav on a neutral-only whiff False (T1, W1, T3)"] = all(not (o["NAV"] & ~wv(o)).any() for o in (t1["filter"], t2[("W1", "filter")], t3r["filter"]))
    ka = t1["known-answer"]; i["known-answer h = valued, hit = its whiffs"] = bool((ka["H"] == ka["good"][None, :]).all() and np.array_equal(ka["NAV"], ka["W"][:, rows, ka["good"]]))
    M3 = ok(all(i.values()))
    print(f"   M3 identities: " + "; ".join(f"{k} {v}" for k, v in i.items()) + f" -> {M3}")
    print(f"      separation T1 scoped vs filter (first `differs8`) {c8}; vs maintain (first `differs`) {c6}; T3 scoped vs filter {c83}")
    # M4
    v4, bo, ids4, bars4 = bench(quiet=True); M4 = ok(v4)
    print(f"   M4 mechanism bench re-run here with the bench seeds: identities {all(ids4.values())}, implementation bars " + str({k: round(v, 4) for k, v in bars4.items()})
          + f" -> {M4}; bench (d) D6_W1 {bo['D6_W1']:.4f} (bar rule gives {bo['bar_T2']:+.1f}; BARS {BARS['T2']}), bench (f) D6 {bo['D6']:.4f} (rule gives {bo['bar_D']:+.4f}; BARS {BARS['D']})")
    # M5
    wf, wm = t2[("W1", "filter")], t2[("W1", "maintain")]; s9, s8_, s6_ = ph22.summary(w9), ph22.summary(wf), ph22.summary(wm)
    m5 = [crit("M5(a) W1 scoped, reach within 3.0 by 600", "P", 0.80, False, s9["reach"]),
          crit("M5(b) W1 dwell, scoped - maintain (Agent6), paired mean", "DP", BARS["T2"], False, s9["dwell"].astype(float), s6_["dwell"].astype(float))]
    cm = s9["contacts"].mean(); m5.append(ok(cm <= 0.10)); print(f"   M5(c) W1 scoped, wall contacts per row: mean {cm:.3f}  at most 0.10 -> {m5[-1]}")
    m5.append(crit("M5(d) W1 lost rows (no B whiff in the last third), scoped - maintain", "DP", 0.05, True, s9["lost"].astype(float), s6_["lost"].astype(float)))
    ex, fs, fb = first_surge_ok(w9); m5.append(ok(ex.all())); print(f"   M5(e) W1 first surge == first B whiff at or after step {N_WIN - 1}: {int(ex.sum())}/{R} rows exact -> {m5[-1]}")
    M5 = agg(m5); pp, m, sd = pass_prob(s9["dwell"] - s6_["dwell"], BARS["T2"])
    print(f"   M5 -> {M5}      reported: first surge within N + 40 = step 99 {int(((fs >= 0) & (fs <= 99)).sum())}/{R}; first-surge quartiles {q3(fs[fs >= 0])} (rows {int((fs >= 0).sum())});"
          f" dwell mean scoped {s9['dwell'].mean():.2f} / filter {s8_['dwell'].mean():.2f} / maintain {s6_['dwell'].mean():.2f}; paired scoped - maintain mean {m:+.3f} sd {sd:.3f};"
          f" scoped - filter {(s9['dwell'] - s8_['dwell']).mean():+.3f}; reach filter {int(s8_['reach'].sum())}, maintain {int(s6_['reach'].sum())}")
    # M6
    nw_s, nw_m = no_whiff_last_third(t1["scoped"]).astype(float), no_whiff_last_third(t1["maintain"]).astype(float)
    m6 = [crit("M6(a) T1 no whiff of either plume in the last third, scoped - maintain", "DP", 0.05, True, nw_s, nw_m)]
    cm = t1["scoped"]["contacts"].mean(); m6.append(ok(cm <= 0.10)); print(f"   M6(b) T1 scoped, wall contacts per row: mean {cm:.3f}  at most 0.10 -> {m6[-1]}")
    M6 = agg(m6); print(f"   M6 -> {M6}")
    # M7
    d = {a: t3(t3r[a]) for a in ("scoped", "filter", "maintain")}; e9 = d["scoped"]["elig"]
    m7 = [crit("M7(a) T3 scoped, the window exact, eligible rows", "P", 0.95, False, d["scoped"]["exact"][e9])]
    print(f"      M7(a) every eligible row exact: {bool(d['scoped']['exact'][e9].all())}")
    if BARS["D6"] < 1.0: print(f"   M7(c): D6 {BARS['D6']:.3f} < 1 step (pinned baseline) -> UNREADABLE"); m7.append("UNREADABLE")
    else: m7.append(crit("M7(c) T3 neutral dwell steps 400-599, scoped - maintain, paired mean", "DP", BARS["D"], False, d["scoped"]["dwell"], d["maintain"]["dwell"]))
    m7d = full(t3r["scoped"], t1["scoped"], T0) and full(t3r["filter"], t1["filter"], T0) and full(t3r["maintain"], t1["maintain"], T0) and s83
    m7.append(ok(m7d)); print(f"   M7(d) T3 == T1 on steps 0-{T0 - 1} for every arm and scoped == filter up to its first `differs8` step: {m7d} -> {m7[-1]}")
    M7 = agg(m7)
    eb = e9 & d["maintain"]["elig"]; _, sdp, slo, shi = interval("DP", d["scoped"]["S"][eb].astype(float), d["maintain"]["S"][eb].astype(float))
    print(f"   M7 -> {M7}      M7(b) REPORTED, not a bar: S " + ", ".join(f"{a} {int(d[a]['S'][d[a]['elig']].sum())}/{int(d[a]['elig'].sum())} = {d[a]['S'][d[a]['elig']].mean():.3f}"
          f" [{interval('P', d[a]['S'][d[a]['elig']])[2]:.3f}, {interval('P', d[a]['S'][d[a]['elig']])[3]:.3f}]" for a in d)
          + f"; paired S scoped - maintain over rows eligible in both ({int(eb.sum())}) {sdp:+.3f} [{slo:+.3f}, {shi:+.3f}]; S6 (bench) readability note in the report")
    pd_, md, sdd = pass_prob(d["scoped"]["dwell"] - d["maintain"]["dwell"], BARS["D"])
    print(f"      reported: T3 dwell 400-599 mean scoped {d['scoped']['dwell'].mean():.2f} / filter {d['filter']['dwell'].mean():.2f} / maintain {d['maintain']['dwell'].mean():.2f};"
          f" paired scoped - maintain {md:+.3f} sd {sdd:.3f}; scoped - filter {(d['scoped']['dwell'] - d['filter']['dwell']).mean():+.3f}")
    unread = M1 != "PASS" or max(ties.values()) > 0.20 or M3 != "PASS" or M4 != "PASS" or "UNREADABLE" in (M2, M5, M6, M7)
    verdict = all(x == "PASS" for x in (M1, M2, M3, M4, M5, M6, M7))
    fail = any(x == "FAIL" for x in (M2, M5, M6, M7))
    lab = "PASS" if verdict else "UNREADABLE" if unread and not fail else "FAIL" if fail else "INCONCLUSIVE"
    print(f"\n== H24 ==  M1 {M1}  M2 {M2}  M3 {M3}  M4 {M4}  M5 {M5}  M6 {M6}  M7 {M7}  -> {lab}: "
          + ("with v_max scoped to odours present by a per-odour counter (window 60, starting ON), the agent keeps H23's result in the H21 task within 0.05 of the adopted filter"
             " and at P(V) of at least 0.88; in the absent-odour world it tracks the only odour present within the registered dwell gap of the unfiltered agent; and after the valued"
             " odour is lost it releases the neutral odour exactly 60 steps after the last valued whiff [M7(a)] and tracks it within the registered gap of the unfiltered agent over"
             " steps 400 to 599 [M7(c)]" if verdict else "UNREADABLE (section 8)" if lab == "UNREADABLE" else "NOT shown under the registered criteria")
          + "; M7(b) reported beside it, not part of it")


def main(mode):
    if None in BARS.values():
        print(f"== H24 {mode}: REFUSED. BARS {BARS} are unset: decision:h24-t2-dwell-bar and decision:h24-t3-bars must be recorded from the bench and written into this file first"
              " (design v3 section 8) =="); sys.exit(2)
    seeds = SEEDS[mode]
    print(f"== H24, {mode.upper()}. design {DESIGN}; this file sha256 {sha()}; ph21.py {sha(ph21.__file__)} (H23's: {sha(ph21.__file__) == PH21_SHA});"
          f" ph22.py {sha(ph22.__file__)} (the check's: {sha(ph22.__file__) == PH22_SHA}); G {G_STAR}, gate on where G 2; N {N_WIN}; t0 {T0}; world seed {seeds[0]}, agent seed {seeds[1]};"
          f" {R} rows x {T} steps; bootstrap seed {ph15.BOOT_SEED}; BARS {BARS}; {'operation check only' if mode == 'dev' else 'the one evaluation'} ==")
    hits, nums, nf = seeds_unused()
    print(f"   seed self-check: {SEEDS[mode]} and all H24 seeds and derived in no other file ({nf} scanned): {not hits}{'' if not hits else ' ' + str(hits)}")
    print("   rows share no state: one generator per world and one per agent population, fixed-size draws consumed in row order every step")
    print("\n== T1, the H21 choice task ==")
    t1 = {arm: arm_run(arm, seeds) for arm in ARMS}
    maj = {arm: majority(t1[arm]) for arm in ARMS}; first = {arm: outcome(t1[arm]) for arm in ARMS}
    for arm in ARMS:
        describe_majority(arm, t1[arm], *maj[arm]); h21_diag(arm, t1[arm])
        h23_diag(arm, t1[arm], t1["maintain"] if arm in ("scoped", "filter") else None)
        o = t1[arm]
        if o["arm"] == "Agent9":
            hn = o["H"] == (1 - o["good"])[None, :]; fd = first_true(o["DIFF8"])
            print(f"      H24 diag: `differs8` rows {int((fd >= 0).sum())}/{R}, first `differs8` step quartiles {q3(fd[fd >= 0])}, (row, step) {int(o['DIFF8'].sum())};"
                  f" valued present on {o['PRES'].mean():.3f} of (row, step), on {o['PRES'][hn].mean() if hn.any() else float('nan'):.3f} of neutral-held (row, step);"
                  f" held-only valued presence (row, step) {held_only(o)}; presence identity {presence_identity(o)}")
        print("      secondary, first reach and diagnostics:"); describe(arm, o, *first[arm])
    print("\n== T2, the absent-odour world W1 (and W3) ==")
    t2 = {("W1", a): arm_run(a, seeds, world="W1") for a in ("scoped", "filter", "maintain")}
    t2[("W3", "scoped")] = arm_run("neutral", seeds, world="W3"); t2[("W3", "maintain")] = arm_run("neutral", seeds, world="W3", cls=Agent6, filt=False)
    for (wd, a), o in t2.items():
        o["arm"] = f"{a} ({o['arm']})"; ph22.describe(o)
        if wd == "W1":
            ex, fs, fb = first_surge_ok(o); fn = first_true(o["NAV"])
            print(f"      H24 diag: first surge step quartiles {q3(fn[fn >= 0])} (rows {int((fn >= 0).sum())}); first B whiff at or after 59 {q3(fb[fb >= 0])}; first surge == it {int(ex.sum())}/{R}")
    print("\n== T3, the 'sensed then lost' world (mask on from step 150) ==")
    t3r = {a: arm_run(a, seeds, world="T3") for a in ("scoped", "filter", "maintain")}
    for a, o in t3r.items(): t3_describe(a, o, t3(o))
    judge(t1, maj, first, t2, t3r, seeds)


if __name__ == "__main__":
    mode = ([m for m in sys.argv[1:] if m in ("demo", "bench", "dev", "eval")] or ["demo"])[0]
    if mode == "demo": demo(); sys.exit(0)
    if mode == "bench": sys.exit(0 if bench()[0] else 1)
    main(mode)
