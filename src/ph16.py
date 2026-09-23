#!/usr/bin/env python3
"""H20 Stage A: does a SUPPLIED positive value decide which of two available odours is pursued?

Usage: python ph16.py demo | bench | dev G=<g> | eval G=<g>

One change to the adopted agent (ph14.Agent3): the upstream response of an odour with a positive
value is multiplied by (1 + G*max(v, 0)) before the evidence-release comparison and the selection
circuit. Nothing else changes. Negative avoidance keeps its pathway and overrides the bias.

Design v3 FINAL (task, bench, arms, criteria A1-A5, seeds, statistics) is doc dd947882bd962eebe,
hash e563bd60...f0a3, stored before this file existed. Order fixed there: self-checks (demo) ->
bench -> G* recorded -> dev -> one evaluation. G* is passed on the command line from the bench
record; the task never chooses it.
"""
import sys, hashlib
import numpy as np
import ph15
from ph9 import UPWIND, CAST_PERIOD, MAXOFF, GAIN, MAXTURN, TURN_NOISE, STEPS, W0, SLOPE, LMAX, angdiff
from ph11 import RESET_AFTER, MARGIN
from ph12 import SAT
from ph14 import World5, Agent3

DESIGN = "v3 doc dd947882bd962eebe hash e563bd60c7517afc545b9031265e0559f381cd189b34a162bd4ace5f35f0f0a3"
R, T, PREHOLD, SEP, DOWN = 400, STEPS, 30, 10.0, 20.0
SEEDS = dict(dev=(9820, 9920), eval=(1680, 1780))
BENCH = dict(rows=400, steps=200, rates=(0.057, 0.30), cands=(0.0, 0.5, 1.0, 2.0), seed_w=20260921, seed_a=20260922)
ARMS = {"bias": (1.0, 0.0, True), "bias-revise": (1.0, 0.0, True), "neutral": (0.0, 0.0, True),
        "pathway-off": (1.0, 0.0, False), "priority": (1.0, -1.0, True), "priority-off": (1.0, -1.0, False)}
CELLS = ("odour A valued, +y", "odour A valued, -y", "odour B valued, +y", "odour B valued, -y")
ph15.Z, ph15.QLO, ph15.QHI, ph15.BOOT_SEED = 1.959964, 2.5, 97.5, 20260923     # 95 percent, one evaluation (7)

def sha(): return hashlib.sha256(open(__file__, "rb").read()).hexdigest()
def med(x): return float(np.median(x)) if len(x) else float("nan")

def cast_draw(seed_a, runs):
    """record:h20-amendment-initial-cast-side (owner, before the evaluation). The adopted agent starts
    every row with cast_sign +1, which from the midline sends every first cast swing to -y: on the
    development seeds the -y source was reached first in 94 percent of rows in every arm (A1(b) FAIL,
    ph16c.py). The initial cast side is drawn per row, the same draw in every arm; agents untouched."""
    return np.random.default_rng(seed_a + 20_000).choice([1.0, -1.0], runs)


class World7(World5):
    """Two sources SEP apart crosswind at one downwind coordinate; the start on the midline DOWN
    downwind, heading World2's uniform draw. 2 x 2 balance by seeded permutation: `good` is the
    valued odour (= its source's index), `side` +1 if the valued source sits at +y."""

    def __init__(self, runs, rng, seed):
        super().__init__(runs, rng)                       # World4's draw: x, translation, walls
        cell = np.empty(runs, int); cell[np.random.default_rng(seed + 10_000).permutation(runs)] = np.arange(runs) % 4
        self.cell, self.good, self.side = cell, cell // 2, np.where(cell % 2 == 0, 1.0, -1.0)
        rows = np.arange(runs); x = self.src[:, 0, 0]; yc = self.src[:, 0, 1] + SEP/2
        self.src = np.zeros((runs, 2, 2)); self.src[:, :, 0] = x[:, None]
        self.src[rows, self.good, 1] = yc + self.side*SEP/2; self.src[rows, 1 - self.good, 1] = yc - self.side*SEP/2
        self.pos = np.stack([x + DOWN, yc], 1)
        self.plus_y = np.where(self.side > 0, self.good, 1 - self.good)


class Still:
    """the bench's stub world: no movement, heading 0, rotation 0"""
    def __init__(self, runs): self.head, self.rot = np.zeros(runs), np.zeros(runs)


class Agent4(Agent3):
    """Agent3 (values supplied, H19 (a) on, return cast, rotation made) plus ONE change: the upstream
    output of an odour with a positive value is multiplied by (1 + G*max(v, 0)). G = 0 must BE
    Agent3 step for step, and all-zero values must BE G = 0 (checked in demo and in the run, A3).
    Exposes the navigation target, y' and the two release conditions for measurement."""

    def __init__(self, runs, rng, G=0.0, **kw):
        super().__init__(runs, rng, **kw)
        self.G, self.yp, self.tgt = G, np.zeros((runs, 2)), np.zeros(runs)
        self.due_evidence = self.due_timeout = np.zeros(runs, bool)

    def act(self, w, whiffs, wind_on):
        rows = np.arange(self.R)
        y = self.up.step(whiffs.astype(float))*(1.0 + self.G*np.maximum(self.chan_valence(), 0.0))   # H20: the pathway
        self.yp = y
        hp = self.held(); committed = hp >= 0; hi = np.maximum(hp, 0); other = 1 - hi
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


def prehold(a, w):
    """T-revise: PREHOLD steps of the neutral odour to the upstream stage, the agent standing still.
    Returns which rows hold the neutral odour afterwards."""
    x = np.zeros((a.R, 2), bool); x[np.arange(a.R), 1 - w.good] = True
    for _ in range(PREHOLD): a.act(w, x, np.ones(a.R, bool))
    return a.held() == 1 - w.good


def run(arm, seeds, G, runs=R, steps=T):
    vg, vo, gain = ARMS[arm]
    w = World7(runs, np.random.default_rng(seeds[0]), seeds[0]); rows = np.arange(runs); neutral = 1 - w.good
    kv = np.zeros((runs, 2)); kv[rows, w.good] = vg; kv[rows, neutral] = vo
    a = Agent4(runs, np.random.default_rng(seeds[1]), G=G if gain else 0.0, known=kv)
    a.cast_sign = cast_draw(seeds[1], runs)
    o = dict(good=w.good, cell=w.cell, plus_y=w.plus_y, G=a.G, pre=None, first=np.full((runs, 2), -1),
             dwell=np.zeros((runs, 2)), H=np.full((steps, runs), -1, np.int8), W=np.zeros((steps, runs, 2), bool),
             POS=np.zeros((steps, runs, 2)), HEAD=np.zeros((steps, runs)), S=np.zeros((steps, runs, 2)),
             contacts=np.zeros(runs), viol=0, neg_steps=0, neg_rows=np.zeros(runs, bool), ymax=0.0, y_over=0, sat=0, smax=0.0,
             rel=np.full(runs, -1), rel_kind=np.full(runs, -1), rev=np.full(runs, -1), exit=np.full(runs, -1))
    if arm == "bias-revise": o["pre"] = prehold(a, w)
    for t in range(steps):
        whiffs = w.sense()
        turn, h = a.act(w, whiffs, w.wind_on())
        neg = (h >= 0) & (kv[rows, np.maximum(h, 0)] < 0)                     # A4(a)(ii)
        o["viol"] += int((neg & (a.tgt != a.flee_side)).sum()); o["neg_steps"] += int(neg.sum()); o["neg_rows"] |= neg
        o["ymax"] = max(o["ymax"], float(a.yp.max())); o["y_over"] += int((a.yp > 1.8).sum())   # section 2 range
        o["sat"] += int((a.sel.s >= 4.9).any(1).sum()); o["smax"] = max(o["smax"], float(a.sel.s.max()))
        newly = (o["rel"] < 0) & (h != neutral)                                # A5 events
        o["rel"] = np.where(newly, t, o["rel"])
        o["rel_kind"] = np.where(newly, np.where(a.due_evidence, 0, np.where(a.due_timeout, 1, 2)), o["rel_kind"])
        o["rev"] = np.where((o["rev"] < 0) & (h == w.good), t, o["rev"])
        w.move(turn); a.bump(w.bumped)
        at = w.at_source()
        o["first"] = np.where((o["first"] < 0) & at, t, o["first"]); o["dwell"] += at
        d_neg = np.linalg.norm(w.pos - w.src[rows, neutral], axis=1)
        o["exit"] = np.where((o["exit"] < 0) & (o["first"][rows, neutral] >= 0) & (d_neg > 6.0), t, o["exit"])
        o["H"][t] = h; o["W"][t] = whiffs; o["POS"][t] = w.pos; o["HEAD"][t] = w.head; o["S"][t] = a.sel.s
        o["contacts"] += w.bumped
    return o


def outcome(o):
    """every row is exactly one of V (valued source reached first), N (neutral first), Z (no choice)"""
    rows = np.arange(len(o["good"])); fv, fn = o["first"][rows, o["good"]], o["first"][rows, 1 - o["good"]]
    V = (fv >= 0) & ((fn < 0) | (fv < fn)); N = (fn >= 0) & ((fv < 0) | (fn < fv)); Z = (fv < 0) & (fn < 0)
    assert (V.astype(int) + N + Z == 1).all()
    return V, N, Z


def diagnostics(o):
    H, W, good = o["H"], o["W"], o["good"]; n = len(good); rows = np.arange(n); neutral = 1 - good
    held = H >= 0
    ft = np.where(held.any(0), held.argmax(0), -1); fh = np.where(ft >= 0, H[np.maximum(ft, 0), rows], -1)
    changes = np.zeros(n, int); last = np.full(n, -1)
    for h in H:
        changes += (h >= 0) & (last >= 0) & (h != last); last = np.where(h >= 0, h, last)
    f = np.where(o["first"] < 0, 10**9, o["first"]); reached = (o["first"] >= 0).any(1)
    rs = np.where(reached, f.min(1), -1); which = np.where(reached, f.argmin(1), -1)
    har = np.where(reached, H[np.maximum(rs, 0), rows], -2)
    return dict(ft=ft, fh=fh, fh_v=fh == good, fh_n=fh == neutral, changes=changes, rs=rs, which=which, har=har, reached=reached,
                wv=W[:, rows, good].sum(0), wn=W[:, rows, neutral].sum(0), both=W.all(2).sum(0),
                ever_v=(H == good[None, :]).any(0), ever_n=(H == neutral[None, :]).any(0))


# ------------------------------------------------------------------ statistics (section 7)
def interval(kind, a, b=None):
    if kind == "P": k = int(np.sum(a)); return (k, *ph15.wilson(k, len(a)))
    return (None, *ph15.boot(kind, a, b))

def crit(label, kind, thr, most, a, b=None, n_min=50):
    n = len(a)
    if n < n_min: print(f"   {label}: n {n} < {n_min} -> UNREADABLE"); return "UNREADABLE"
    k, pt, lo, hi = interval(kind, a, b)
    if isinstance(thr, tuple): out = "PASS" if lo >= thr[0] and hi <= thr[1] else "FAIL"; rule = f"within [{thr[0]}, {thr[1]}]"
    else: out = ph15.verdict(lo, hi, thr, most); rule = f"{'at most' if most else 'at least'} {thr}"
    print(f"   {label}: {kind} {'' if k is None else f'k {k} '}n {n}  value {pt:.3f}  95% interval [{lo:.3f}, {hi:.3f}]  {rule} -> {out}")
    return out


# ------------------------------------------------------------------ reporting (section 6)
def describe(arm, o, V, N, Z):
    n = len(V); d = diagnostics(o); cell = o["cell"]; rows = np.arange(n); good = o["good"]; steps = o["H"].shape[0]
    print(f"\n   [{arm}] G {o['G']:.1f}  V {V.sum()}  N {N.sum()}  no-choice {Z.sum()}  (of {n})")
    print("      cells: " + " | ".join(f"{c} {CELLS[c]}: V {V[m].sum()} N {N[m].sum()} 0 {Z[m].sum()}" for c in range(4) for m in [cell == c]))
    k, pt, lo, hi = interval("P", V[~Z])
    print(f"      P(V | reached) {k}/{(~Z).sum()} = {pt:.3f} [{lo:.3f}, {hi:.3f}]; first-approach step median V {med(d['rs'][V]):.0f} N {med(d['rs'][N]):.0f};"
          f" dwell median valued {med(o['dwell'][rows, good]):.1f} other {med(o['dwell'][rows, 1 - good]):.1f};"
          f" contacts/row {o['contacts'].mean():.2f}; no whiff in the last third {int((~o['W'][-steps//3:].any((0, 2))).sum())}")
    r = d["reached"]; fh_ok = (d["fh"] == d["which"]) & r; har_ok = (d["har"] == d["which"]) & r
    pv = lambda m: f"{int((V & m).sum())}/{int(m.sum())}"
    print(f"      first hold: valued {d['fh_v'].sum()} neutral {d['fh_n'].sum()} none {(d['ft'] < 0).sum()}, step median {med(d['ft'][d['ft'] >= 0]):.0f};"
          f" hold changes mean {d['changes'].mean():.2f}; agreement: first hold == source reached {fh_ok.sum()}/{r.sum()},"
          f" held at reach == source reached {har_ok.sum()}/{r.sum()} (nothing held at reach {int(((d['har'] == -1) & r).sum())});"
          f" P(V | first hold valued) {pv(d['fh_v'])}; P(V | first hold neutral) {pv(d['fh_n'])}")
    ev, en = d["ever_v"], d["ever_n"]
    print(f"      whiffs/row: valued plume {d['wv'].mean():.1f} neutral plume {d['wn'].mean():.1f} both same step {d['both'].mean():.2f};"
          f" no-choice rows' hold history: never {int((Z & ~ev & ~en).sum())} valued only {int((Z & ev & ~en).sum())}"
          f" neutral only {int((Z & ~ev & en).sum())} both {int((Z & ev & en).sum())}")
    sat = o["sat"]/(steps*n)
    print(f"      input range: y' max {o['ymax']:.2f}, y' > 1.8 on {o['y_over']/(steps*n*2)*100:.2f}% of (row, step, channel),"
          f" s >= 4.9 on {sat*100:.2f}% of (row, step){' FLAG > 1%' if sat > 0.01 else ''}, s max {o['smax']:.2f}")
    # segments (decision:h20-stage-a-run-g2): where a non-V outcome first departs from 'valued selected and reached'.
    # Reported as a diagnosis of the relation between selection, hold and navigation; it names no cause by itself.
    H = o["H"]; before = np.arange(steps)[:, None] <= d["rs"][None, :]
    v_before = ((H == good[None, :]) & before).any(0); har = d["har"]; neutral = 1 - good
    seg = lambda m: (int((m & (har == neutral) & ~v_before).sum()), int((m & (har == neutral) & v_before).sum()),
                     int((m & (har == good)).sum()), int((m & (har == -1)).sum()))
    print(f"      segments, N rows: neutral selected first and held at reach {seg(N)[0]}; valued held earlier, neutral held at reach"
          f" {seg(N)[1]}; valued held at reach yet neutral reached first {seg(N)[2]}; nothing held at reach {seg(N)[3]}"
          f" | V rows: valued held at reach {int((V & (har == good)).sum())} (of which first hold was neutral"
          f" {int((V & (har == good) & d['fh_n']).sum())}), neutral held at reach {int((V & (har == neutral)).sum())}, nothing held {int((V & (har == -1)).sum())}")


# ------------------------------------------------------------------ self-checks (section 9, step 2)
def identity_agent3(seeds, n=40, steps=400):
    """A3's second identity: with G = 0 the H20 agent IS ph14.Agent3, whatever the values"""
    ws = [World7(n, np.random.default_rng(seeds[0]), seeds[0]) for _ in (0, 1)]
    kv = np.zeros((n, 2)); kv[np.arange(n), ws[0].good] = 1.0; kv[np.arange(n), 1 - ws[0].good] = -1.0
    ag = [Agent3(n, np.random.default_rng(seeds[1]), known=kv), Agent4(n, np.random.default_rng(seeds[1]), G=0.0, known=kv)]
    for a in ag: a.cast_sign = cast_draw(seeds[1], n)
    for _ in range(steps):
        for w, a in zip(ws, ag):
            t, _ = a.act(w, w.sense(), w.wind_on()); w.move(t); a.bump(w.bumped)
    return np.array_equal(ws[0].pos, ws[1].pos) and np.array_equal(ws[0].head, ws[1].head)


def priority_check(G, rows=50, steps=20):
    """A4(a)(i): the circuit is SET to hold the negative odour (channel 1) while the valued odour
    (channel 0) is presented with the gain on. On every negative-held step the target must be the
    flee side, and the same as the target the same state gives at G = 0."""
    out = []
    for g in (G, 0.0):
        a = Agent4(rows, np.random.default_rng(11), G=g, known=np.tile([1.0, -1.0], (rows, 1)))
        a.sel.s[:, 1] = 2.0; w = Still(rows); tg, hh = [], []
        for _ in range(steps):
            _, h = a.act(w, np.ones((rows, 2), bool), np.ones(rows, bool)); tg.append(a.tgt.copy()); hh.append(h.copy())
        out.append((np.array(tg), np.array(hh), a.flee_side))
    (tg1, h1, f1), (tg0, h0, f0) = out
    neg1 = h1 == 1; both = neg1 & (h0 == 1)
    assert neg1.any(), "the constructed state did not hold the negative odour"
    assert (tg1[neg1] == np.broadcast_to(f1, tg1.shape)[neg1]).all(), "target is not the flee side while the negative odour is held"
    assert np.array_equal(tg1[both], tg0[both]), "the gain changed the flee target"
    return int(neg1.sum()), int(both.sum()), int((h1 == 0).sum())


def demo():
    assert identity_agent3((5, 6)), "with G = 0 the H20 agent is not Agent3"
    ws = [World7(40, np.random.default_rng(5), 5) for _ in (0, 1)]
    ag = [Agent4(40, np.random.default_rng(6), G=g, known=np.zeros((40, 2))) for g in (1.0, 0.0)]
    for _ in range(400):
        for w, a in zip(ws, ag):
            t, _ = a.act(w, w.sense(), w.wind_on()); w.move(t); a.bump(w.bumped)
    assert np.array_equal(ws[0].pos, ws[1].pos) and np.array_equal(ag[0].sel.s, ag[1].sel.s), "all-zero values are not G = 0"
    w = World7(400, np.random.default_rng(0), 0); d = w.pos[:, None, :] - w.src
    assert np.allclose(d[:, :, 0], DOWN) and np.allclose(np.abs(d[:, :, 1]), SEP/2) and DOWN < LMAX and SEP/2 < W0 + SLOPE*DOWN
    assert np.minimum(w.src, w.arena - w.src).min() >= 68 and np.bincount(w.cell).tolist() == [100]*4
    assert np.allclose(w.src[np.arange(400), w.plus_y, 1] - w.src[np.arange(400), 1 - w.plus_y, 1], SEP)
    rate = sum(w.sense().astype(float) for _ in range(2000))/2000
    assert abs(rate[:, 0].mean() - rate[:, 1].mean()) < 0.01 and abs(rate.mean() - 0.3*np.exp(-DOWN/12.0)) < 0.01
    w = World7(400, np.random.default_rng(1), 1); kv = np.zeros((400, 2)); kv[np.arange(400), w.good] = 1.0
    a = Agent4(400, np.random.default_rng(2), G=1.0, known=kv); ok = prehold(a, w)
    assert (a.held() == w.good).sum() == 0 and ok.mean() >= 0.9, f"pre-hold: {ok.mean():.3f} hold the neutral odour"
    exp1, cmp1, took = priority_check(1.0)
    print("ok  G = 0 reproduces Agent3 over 400 steps; all-zero values reproduce G = 0 bitwise (positions and circuit state)")
    print(f"ok  every start 20 downwind and 5 crosswind of both sources, inside both cones; walls >= 68; cells 100 each;"
          f" whiff rate per plume {rate[:, 0].mean():.4f} / {rate[:, 1].mean():.4f} (expected {0.3*np.exp(-DOWN/12.0):.4f})")
    print(f"ok  pre-hold: {ok.mean()*100:.1f}% hold the neutral odour, none the valued")
    print(f"ok  priority in a constructed state: negative odour held on {exp1} (row, step), target = flee side on every one,"
          f" equal to G = 0's target on the {cmp1} steps both hold it; the valued odour took the hold on {took} (row, step) afterwards")


# ------------------------------------------------------------------ the G bench (section 3)
def bench(G, p):
    n, steps = BENCH["rows"], BENCH["steps"]; rw = np.random.default_rng(BENCH["seed_w"])
    a = Agent4(n, np.random.default_rng(BENCH["seed_a"]), G=G, known=np.tile([1.0, 0.0], (n, 1)))
    w = Still(n); on = np.ones(n, bool)
    first = np.full(n, -1); last = np.full(n, -1); changes = np.zeros(n, int); ymax = smax = 0.0; y_over = sat = 0
    for _ in range(steps):
        _, h = a.act(w, rw.random((n, 2)) < p, on)
        first = np.where((first < 0) & (h >= 0), h, first)
        changes += (h >= 0) & (last >= 0) & (h != last); last = np.where(h >= 0, h, last)
        ymax = max(ymax, float(a.yp.max())); y_over += int((a.yp > 1.8).sum())
        sat += int((a.sel.s >= 4.9).any(1).sum()); smax = max(smax, float(a.sel.s.max()))
    return dict(first=first, end=h, changes=changes, ymax=ymax, y_over=y_over/(n*steps*2), sat=sat/(n*steps), smax=smax)


def bench_main():
    n = BENCH["rows"]
    print(f"== H20 G bench. design {DESIGN}; this file sha256 {sha()}; {BENCH} ==")
    res = {}
    for G in BENCH["cands"]:
        for p in BENCH["rates"]:
            r = bench(G, p); held = r["first"] >= 0; nh = int(held.sum()); k = int((r["first"] == 0).sum())
            pt, lo, hi = ph15.wilson(k, nh) if nh else (float("nan"),)*3
            print(f"   G {G:3.1f} p {p:.3f}: selection rate {nh}/{n} (no selection {n - nh}); first hold on the biased channel"
                  f" {k}/{nh} = {pt:.3f} [{lo:.3f}, {hi:.3f}]; held at step {BENCH['steps']}: ch0 {int((r['end'] == 0).sum())}"
                  f" ch1 {int((r['end'] == 1).sum())} none {int((r['end'] < 0).sum())}; hold changes mean {r['changes'].mean():.2f};"
                  f" y' max {r['ymax']:.2f}, y' > 1.8 {r['y_over']*100:.2f}%, s >= 4.9 {r['sat']*100:.2f}%, s max {r['smax']:.2f}")
            res[(G, p)] = (nh, k, lo, hi)
    p0 = BENCH["rates"][0]; nh, k, lo, hi = res[(0.0, p0)]
    neutral_ok = nh > 0 and lo >= 0.35 and hi <= 0.65
    print(f"   neutral tolerance at G 0, p {p0}: interval [{lo:.3f}, {hi:.3f}] over {nh} holding rows within [0.35, 0.65] -> {'PASS' if neutral_ok else 'FAIL'}")
    ok = [G for G in BENCH["cands"] if G > 0 and res[(G, p0)][2] >= 0.85 and res[(G, p0)][0] >= 200]
    for G in BENCH["cands"]:
        if G > 0: print(f"   candidate G {G:3.1f}: lower bound {res[(G, p0)][2]:.3f} >= 0.85 and holding rows {res[(G, p0)][0]} >= 200 -> {'meets' if G in ok else 'does not meet'}")
    if not neutral_ok: print("== BENCH UNREADABLE: the neutral case is outside its tolerance; Stage A is not run =="); sys.exit(1)
    if not ok: print("== NO CANDIDATE meets the selection rule; Stage A is not run =="); sys.exit(1)
    print(f"== G* = {min(ok)} (the smallest candidate meeting the rule) ==")


# ------------------------------------------------------------------ the task (sections 4-7)
def judge(res, outs, seeds, G):
    rows = np.arange(R)
    print("\n== criteria (design v3 section 7; 95 percent, one evaluation, no extension) ==")
    print("   A1 task validity: a check that excludes a large overall asymmetry; the cells of every arm are printed above")
    a1 = []
    for arm in ("neutral", "pathway-off"):
        z = outs[arm][2]; ok = z.mean() <= 0.20; a1.append(ok)
        print(f"   A1(a) {arm}: no-choice {z.sum()}/{R} = {z.mean():.3f}  at most 0.20 -> {'PASS' if ok else 'FAIL'}")
    o = res["neutral"]; d = diagnostics(o); m = d["reached"]
    a1.append(crit("A1(b) neutral, P(+y first | reached)", "P", (0.35, 0.65), False, (d["which"] == o["plus_y"])[m]) == "PASS")
    V, N, Z = outs["pathway-off"]
    a1.append(crit("A1(c) pathway-off, P(V | reached)", "P", (0.35, 0.65), False, V[~Z]) == "PASS")
    Vb, Nb, Zb = outs["bias"]; Vp = outs["pathway-off"][0]
    a2 = [crit("A2(a) bias, P(V) over all rows", "P", 0.70, False, Vb) == "PASS"]
    for c in range(4): a2.append(crit(f"A2(b) bias, cell {c} ({CELLS[c]}), P(V)", "P", 0.55, False, Vb[res["bias"]["cell"] == c]) == "PASS")
    a2.append(crit("A2(c) DP = P(V) bias - pathway-off, same rows", "DP", 0.20, False, Vb.astype(float), Vp.astype(float)) == "PASS")
    k, pt, lo, hi = interval("P", Vb[~Zb])
    print(f"      reported: bias N {Nb.sum()}, no-choice {Zb.sum()}; P(V | reached) {k}/{(~Zb).sum()} = {pt:.3f} [{lo:.3f}, {hi:.3f}]")
    n0 = run("neutral", seeds, 0.0); o = res["neutral"]
    same = all(np.array_equal(o[key], n0[key]) for key in ("POS", "HEAD", "S")); ag3 = identity_agent3(seeds)
    a3 = same and ag3
    print(f"   A3 identity: neutral at G {G} vs G 0, {R} rows x {T} steps, positions, headings and circuit states bitwise equal: {same};"
          f" G 0 vs ph14.Agent3 (values +1/-1, 40 rows x 400 steps): {ag3} -> {'PASS' if a3 else 'FAIL'}")
    exp1, cmp1, took = priority_check(G)
    print(f"   A4(a)(i) constructed state: negative odour held on {exp1} (row, step), target = flee side on every one, equal to G 0's on the"
          f" {cmp1} steps both hold it; the valued odour took the hold on {took} afterwards -> PASS")
    a4 = []
    for arm in ("priority", "priority-off"):
        o = res[arm]
        if o["neg_steps"] == 0: print(f"   A4(a)(ii) {arm}: negative odour never held (0 rows, 0 steps): no violation, no opportunity to verify operation")
        else:
            ok = o["viol"] == 0; a4.append(ok)
            print(f"   A4(a)(ii) {arm}: negative odour held in {int(o['neg_rows'].sum())} rows over {o['neg_steps']} (row, step); violations {o['viol']} -> {'PASS' if ok else 'FAIL'}")
    dn = lambda arm: res[arm]["dwell"][rows, 1 - res[arm]["good"]]
    a4.append(crit("A4(b) dwell at the negative source, priority - priority-off (mean)", "DP", 1.0, True, dn("priority"), dn("priority-off")) == "PASS")
    for arm in ("priority", "priority-off"):
        o = res[arm]; entry = o["first"][rows, 1 - o["good"]]; near = entry >= 0; ex = o["exit"] - entry
        print(f"      {arm}: ever within 3.0 of the negative source {near.sum()}/{R}; first entry to exit beyond 6.0: median"
              f" {med(ex[near & (o['exit'] >= 0)]):.0f} steps, never exited {int((near & (o['exit'] < 0)).sum())}")
    a4.append(crit("A4(c) priority, P(V) over all rows", "P", 0.70, False, outs["priority"][0]) == "PASS")
    _, pt, lo, hi = interval("DP", outs["priority"][0].astype(float), outs["priority-off"][0].astype(float))
    print(f"      reported, no bar: DP = P(V) priority - priority-off {pt:+.3f} [{lo:+.3f}, {hi:+.3f}]")
    o = res["bias-revise"]; grp = o["pre"]; V = outs["bias-revise"][0]
    print(f"   A5 T-revise (reported, not a gate): pre-hold holds the neutral odour in {grp.sum()}/{R} rows (failed {(~grp).sum()})")
    if grp.sum() < 50: print("      group under 50 rows -> UNREADABLE")
    else:
        rev = o["rev"] >= 0; k, pt, lo, hi = interval("P", rev[grp])
        reading = "meets the bar that at least half revise" if lo >= 0.5 else "revision rate below half" if hi < 0.5 else "uncertain"
        print(f"      revision (valued odour held) within {T} steps: {k}/{grp.sum()} = {pt:.3f} [{lo:.3f}, {hi:.3f}] -> {reading};"
              f" revision step median {med(o['rev'][grp & rev]):.0f}")
        rel, kind = o["rel"][grp], o["rel_kind"][grp]
        print(f"      release of the neutral hold: {(rel >= 0).sum()} rows (evidence {(kind == 0).sum()}, timeout {(kind == 1).sum()},"
              f" neither {(kind == 2).sum()}), never released {(rel < 0).sum()}; release step median {med(rel[rel >= 0]):.0f}")
        k, pt, lo, hi = interval("P", V[grp])
        print(f"      P(reached valued first | group) {k}/{grp.sum()} = {pt:.3f} [{lo:.3f}, {hi:.3f}]; revised and reached valued {int((grp & rev & V).sum())},"
              f" revised without reaching valued {int((grp & rev & ~V).sum())}, reached valued without revision {int((grp & ~rev & V).sum())}")
    ok = all(a1) and all(a2) and a3 and all(a4)
    f = lambda x: "PASS" if x else "FAIL"
    print(f"\n== Stage A ==  A1 {f(all(a1))}  A2 {f(all(a2))}  A3 {f(a3)}  A4 {f(all(a4))}  -> "
          + ("the pathway carries a supplied positive value into the choice of source" if ok else "NOT shown under the registered criteria")
          + "; A5 reported above, not a gate")


def main(mode, G):
    seeds = SEEDS[mode]
    print(f"== H20 Stage A, {mode.upper()}. design {DESIGN}; this file sha256 {sha()}; G* {G}; world seed {seeds[0]},"
          f" agent seed {seeds[1]}; {R} rows x {T} steps; {'operation check only' if mode == 'dev' else 'the one evaluation'} ==")
    res = {arm: run(arm, seeds, G) for arm in ARMS}
    outs = {arm: outcome(res[arm]) for arm in ARMS}
    for arm in ARMS: describe(arm, res[arm], *outs[arm])
    judge(res, outs, seeds, G)


if __name__ == "__main__":
    mode = ([m for m in sys.argv[1:] if m in ("demo", "bench", "dev", "eval")] or ["demo"])[0]
    if mode == "demo": demo(); sys.exit(0)
    if mode == "bench": bench_main(); sys.exit(0)
    g = [float(a[2:]) for a in sys.argv[1:] if a.startswith("G=")]
    assert g, "dev and eval need G=<g> from the bench record"
    main(mode, g[0])
