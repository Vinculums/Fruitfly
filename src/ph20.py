#!/usr/bin/env python3
"""H22: value-gated surge (leave and resample) in the H21 choice task.

Usage: python ph20.py demo | bench | dev | eval

Design v1 FINAL, confirmed by the owner (decision:h22-open): doc dfd041adf77911e7c, hash 1ce2717e...7f83,
stored before this file existed. ONE change to the H21 maintain agent (ph19.Agent6, G 2, gate on): while a
non-negative odour whose value is below the highest value in the agent's own read-out is held
(h >= 0 and 0 <= v_h < v_max), its whiffs do not reach navigation: nav = (hit AND surge_ok) OR H19 (a).
The silence timer still counts hit. resample=False, equal values, nothing held and a negative held odour:
the agent IS Agent6 (checked bitwise). No adopted module is edited. Nothing changes after the table.
"""
import sys, os, re, hashlib
import numpy as np
import ph15, ph19
from ph16 import World7, Agent4, Still, cast_draw, outcome, diagnostics, describe, interval, crit, med, identity_agent3, CELLS, R, T
from ph17 import Agent5
from ph18 import majority, describe_majority, agg
from ph19 import Agent6, same, no_whiff_last_third, no_nav_last_third, h21_diag, priority_check6
from ph11 import RESET_AFTER, MARGIN
from ph12 import SAT
from ph9 import UPWIND, CAST_PERIOD, MAXOFF, GAIN, MAXTURN, TURN_NOISE, angdiff

DESIGN = "v1 FINAL doc dfd041adf77911e7c hash 1ce2717e95d3444c79d8eeeec6b618d553edede71069b61ece7eb3cd13037f83"
G_STAR = 2.0
SEEDS = dict(dev=(9870, 9970), eval=(1755, 1855))
BENCH = dict(rows=400, phase1=60, phase2=200, p=0.30, steps_c=200, steps_c_held=260, steps_d=300, seed_w=20260929, seed_a=20260930)
#            valued value, other value, G, gate, resample rule, fixed identity
ARMS = {"resample": (1.0, 0.0, G_STAR, True, True, False), "maintain": (1.0, 0.0, G_STAR, True, False, False),
        "pathway-off": (1.0, 0.0, 0.0, False, False, False), "known-answer": (1.0, 0.0, 0.0, False, False, True),
        "neutral": (0.0, 0.0, G_STAR, True, True, False), "priority-identity": (1.0, -1.0, G_STAR, True, True, False)}
ph15.BOOT_SEED = 20260931            # design section 7; ph16 set the 95 percent level

def sha(): return hashlib.sha256(open(__file__, "rb").read()).hexdigest()


class Agent7(Agent6):
    """Agent6 (Agent4 + the H21 gate) plus the H22 rule. act is Agent6.act with nav formed through surge_ok;
    resample=False must BE Agent6 step for step (checked in demo and in the run). `withheld` marks a whiff of the
    held odour on a step on which surge_ok is 0."""

    def __init__(self, runs, rng, resample=True, **kw):
        super().__init__(runs, rng, **kw); self.resample = resample; self.withheld = np.zeros(runs, bool)

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
        v = self.chan_valence(); vh = v[rows, np.maximum(h, 0)]                                       # H22: the rule
        surge_ok = ~((h >= 0) & (vh >= 0.0) & (vh < v.max(1))) if self.resample else np.ones(self.R, bool)
        nav = (hit & surge_ok) | ((h < 0) & (whiffs & (v >= 0)).any(1))
        self.withheld = hit & ~surge_ok
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


def make(cls, runs, rng, G, known, gate, resample):
    if cls is Agent7: return Agent7(runs, rng, G=G, known=known, rule=gate, resample=resample)
    return ph19.make(cls, runs, rng, G, known, gate)


# ------------------------------------------------------------------ the task (design sections 5, 6)
def run(arm, seeds, runs=R, steps=T, G=None, gate=None, resample=None, cls=Agent7):
    vg, vo, g, gt, rs, fixed = ARMS[arm]
    g = g if G is None else G; gt = gt if gate is None else gate; rs = rs if resample is None else resample
    w = World7(runs, np.random.default_rng(seeds[0]), seeds[0]); rows = np.arange(runs); neutral = 1 - w.good
    kv = np.zeros((runs, 2)); kv[rows, w.good] = vg; kv[rows, neutral] = vo
    rng = np.random.default_rng(seeds[1])
    a = Agent5(runs, rng, fixed=w.good.copy(), G=0.0, known=kv) if fixed else make(cls, runs, rng, g, kv, gt, rs)
    a.cast_sign = cast_draw(seeds[1], runs)
    o = dict(good=w.good, cell=w.cell, plus_y=w.plus_y, src=w.src.copy(), G=a.G, rule=rs and not fixed, fixed=fixed, cast=a.cast_sign.copy(),
             first=np.full((runs, 2), -1), dwell=np.zeros((runs, 2)), H=np.full((steps, runs), -1, np.int8), W=np.zeros((steps, runs, 2), bool),
             NAV=np.zeros((steps, runs), bool), TO=np.zeros((steps, runs), bool), EV=np.zeros((steps, runs), bool),
             WH=np.zeros((steps, runs), bool), SINCE=np.zeros((steps, runs), np.float32),
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
        o["WH"][t] = getattr(a, "withheld", False); o["SINCE"][t] = a.since
        o["POS"][t] = w.pos; o["HEAD"][t] = w.head; o["S"][t] = a.sel.s; o["contacts"] += w.bumped
    return o


def first_withheld(o): return np.where(o["WH"].any(0), o["WH"].argmax(0), -1)


def separation(o, ref):
    """M3 (iii): bitwise equal to the reference up to the step before the first withheld surge; rows never withheld equal throughout"""
    eq = (o["POS"] == ref["POS"]).all(2) & (o["HEAD"] == ref["HEAD"]) & (o["S"] == ref["S"]).all(2)
    fw = first_withheld(o); never = fw < 0; steps = eq.shape[0]
    before = np.arange(steps)[:, None] < np.where(never, steps, fw)[None, :]
    pre = (eq | ~before).all(0); whole = eq.all(0)
    return bool(pre.all()), dict(never=int(never.sum()), never_equal=int((never & whole).sum()), withheld=int((~never).sum()),
                                 withheld_pre_equal=int((~never & pre).sum()), withheld_equal_throughout=int((~never & whole).sum()))


def h22_diag(arm, o, ref=None):
    """design section 5, 'added for H22', and the section 10 decomposition"""
    good = o["good"]; n = len(good); rows = np.arange(n); H = o["H"]; neutral = 1 - good; d = diagnostics(o); V = majority(o)[0]
    fw = first_withheld(o); nh = H == neutral[None, :]; vw = (o["W"][:, rows, good] & nh).sum(0); fhn, fhv = d["fh_n"], d["fh_v"]
    rev = fhn & d["ever_v"]; vt = (H == good[None, :]); rt = np.where(vt.any(0), vt.argmax(0), -1)
    cm = np.where(nh.any(0), np.where(nh, o["SINCE"], -1).max(0), -1)
    q = lambda x: f"{np.percentile(x, 25):.0f}/{np.median(x):.0f}/{np.percentile(x, 75):.0f}" if len(x) else "nan"
    print(f"      H22 diag: rows with a withheld surge {int((fw >= 0).sum())}/{n}, first withheld step quartiles {q(fw[fw >= 0])}; withheld (row, step) {int(o['WH'].sum())};"
          f" valued whiffs received while the neutral odour was held {int(vw.sum())} (neutral-first rows: mean {vw[fhn].mean() if fhn.any() else float('nan'):.2f} per row,"
          f" at least one in {int((vw[fhn] > 0).sum())}/{int(fhn.sum())}); cast clock max while the neutral odour was held {int(cm.max())}"
          f" (per-row max, quartiles over the {int((cm >= 0).sum())} rows that held it {q(cm[cm >= 0])})")
    f = fhv.mean(); c = V[fhv].mean() if fhv.any() else float("nan"); qq = V[fhn].mean() if fhn.any() else float("nan"); none = d["ft"] < 0
    print(f"      H22 diag: revision of neutral-first rows {int(rev.sum())}/{int(fhn.sum())}{f' = {rev.sum()/fhn.sum():.3f}' if fhn.any() else ''}, first valued-held step median {med(rt[rev]):.0f};"
          f" decomposition P(V) = f c + (1 - f) q: f {f:.3f} c {c:.3f} q {qq:.3f} -> {f*c + (1 - f)*qq if fhn.any() else f*c:.4f} (observed P(V) {V.mean():.4f}; rows with no hold {int(none.sum())})")
    if ref is not None:
        cl, cr = np.select(list(majority(o)), [0, 1, 2]), np.select(list(majority(ref)), [0, 1, 2]); dr = diagnostics(ref)
        print(f"      H22 diag: paired against maintain, same rows: into V {int(((cl == 0) & (cr != 0)).sum())}, out of V {int(((cl != 0) & (cr == 0)).sum())},"
              f" unchanged class {int((cl == cr).sum())}/{n}; first hold identical row for row {int((d['fh'] == dr['fh']).sum())}/{n} (valued here {int(fhv.sum())} against {int(dr['fh_v'].sum())});"
              f" into V among neutral-first rows {int(((cl == 0) & (cr != 0) & fhn).sum())}, among valued-first rows {int(((cl == 0) & (cr != 0) & fhv).sum())}")


# ------------------------------------------------------------------ the mechanism bench (design section 4)
def bench_run(cls, known, sched, resample=True, G=G_STAR, gate=True, rows=BENCH["rows"]):
    """Still stub; sched: list of (steps, p channel 0, p channel 1). The same uniform draws for every condition."""
    steps = sum(s for s, _, _ in sched); u = np.random.default_rng(BENCH["seed_w"]).random((steps, rows, 2))
    a = make(cls, rows, np.random.default_rng(BENCH["seed_a"]), G, np.tile(known, (rows, 1)), gate, resample); w = Still(rows)
    rec = {k: [] for k in ("H", "s", "S", "NAV", "SINCE", "TGT", "TO")}; t = 0
    for n, p0, p1 in sched:
        for _ in range(n):
            x = np.stack([u[t, :, 0] < p0, u[t, :, 1] < p1], 1)
            _, h = a.act(w, x, np.ones(rows, bool)); t += 1
            for k, v in (("H", h), ("s", a.sel.s), ("S", a.sel.S), ("NAV", a.nav_hit), ("SINCE", a.since), ("TGT", a.tgt), ("TO", a.due_timeout)): rec[k].append(v.copy())
    return {k: np.array(v) for k, v in rec.items()}


def equal(r1, r2, keys): return all(np.array_equal(r1[k], r2[k]) for k in keys)


def bench_a(resample, quiet=False):
    p, p1 = BENCH["p"], BENCH["phase1"]
    r = bench_run(Agent7, [1.0, 0.0], [(p1, 0.0, p), (BENCH["phase2"], 0.0, p)], resample)
    h60 = r["H"][p1 - 1]; denom = h60 == 1; held2 = r["H"][p1:] == 1; navheld = r["NAV"][p1:] & held2
    ok = denom & ~navheld.any(0); k, pt, lo, hi = interval("P", ok[denom]) if denom.any() else (0, float("nan"), float("nan"), float("nan"))
    if not quiet:
        hd = held2[:, denom]; offs = np.abs(angdiff(r["TGT"][p1:][:, denom], UPWIND))
        print(f"   rule {'on ' if resample else 'off'}: holding channel 1 (value 0) at step {p1}: {int(denom.sum())}/{BENCH['rows']} (nothing {int((h60 < 0).sum())}, channel 0 {int((h60 == 0).sum())});"
              f" no phase-2 step with channel 1 held has nav True in {k}/{int(denom.sum())} = {pt:.3f} [{lo:.3f}, {hi:.3f}];"
              f" nav True on {navheld[:, denom].sum()}/{hd.sum()} = {navheld[:, denom].sum()/max(hd.sum(), 1):.3f} of held phase-2 steps;"
              f" hold kept on every phase-2 step {int(hd.all(0).sum())}/{int(denom.sum())}; cast clock max in phase 2 {r['SINCE'][p1:][:, denom].max():.0f};"
              f" target's largest offset from upwind {offs.max():.1f} deg")
    return lo, int(denom.sum())


def bench_d(resample, quiet=False, rows=BENCH["rows"], steps=BENCH["steps_d"]):
    sw, sa = BENCH["seed_w"], BENCH["seed_a"]
    w = World7(rows, np.random.default_rng(sw), sw); r = np.arange(rows); good = w.good; neutral = 1 - good
    kv = np.zeros((rows, 2)); kv[r, good] = 1.0
    a = Agent7(rows, np.random.default_rng(sa), G=G_STAR, known=kv, rule=True, resample=resample); a.cast_sign = cast_draw(sa, rows)
    w.pos = w.src[r, neutral].copy(); a.sel.s[r, neutral] = 2.0                  # placed at the neutral source, neutral hold constructed
    H = np.zeros((steps, rows), np.int8); W = np.zeros((steps, rows, 2), bool); TO = np.zeros((steps, rows), bool); EV = TO.copy(); WH = TO.copy(); contacts = np.zeros(rows)
    for t in range(steps):
        whiffs = w.sense(); turn, h = a.act(w, whiffs, w.wind_on())
        H[t] = h; W[t] = whiffs; TO[t] = a.due_timeout; EV[t] = a.due_evidence; WH[t] = a.withheld
        w.move(turn); a.bump(w.bumped); contacts += w.bumped
    end = H[-1] == good; k, pt, lo, hi = interval("P", end)
    if not quiet:
        wv = W[:, r, good]; vt = H == good[None, :]; ever = vt.any(0)
        fv = np.where(wv.any(0), wv.argmax(0), -1); rv = np.where(ever, vt.argmax(0), -1)
        prev = np.vstack([np.full((1, rows), -1, np.int8), H[:-1]]); ended = (prev >= 0) & (H != prev)
        dn = np.linalg.norm(w.pos - w.src[r, neutral], axis=1); dv = np.linalg.norm(w.pos - w.src[r, good], axis=1)
        print(f"   rule {'on ' if resample else 'off'}: holding the valued odour at step {steps} {k}/{rows} = {pt:.3f} [{lo:.3f}, {hi:.3f}];"
              f" rows with at least one valued whiff {int(wv.any(0).sum())}, valued whiffs per row {wv.sum(0).mean():.2f};"
              f" first valued whiff step median {med(fv[fv >= 0]):.0f}, revision step median {med(rv[ever]):.0f}; revised {int(ever.sum())}, revised and later lost {int((ever & ~end).sum())};"
              f" distance at step {steps} from the neutral source median {med(dn):.1f}, from the valued source median {med(dv):.1f};"
              f" no whiff of either plume in the last 100 steps {int((~W[-100:].any((0, 2))).sum())}; wall contacts {int(contacts.sum())} ({contacts.mean():.2f} per row);"
              f" holds ended {int(ended.sum())} (timeout flag {int((ended & TO & ~EV).sum())}, evidence {int((ended & EV & ~TO).sum())}, both {int((ended & TO & EV).sum())},"
              f" neither {int((ended & ~TO & ~EV).sum())}); withheld (row, step) {int(WH.sum())}")
    return lo, pt, k


def bench():
    p = BENCH["p"]
    print(f"== H22 mechanism bench (design section 4). design {DESIGN}; this file sha256 {sha()}; {BENCH} ==")
    print("(a) surge withheld, Still stub, values +1/0, G 2, gate on: phase 1 channel 1 (0) alone p 0.30 60 steps, phase 2 the same 200 steps;"
          " statistic = no phase-2 step with channel 1 held has nav True, over the rows holding channel 1 at step 60")
    lo_a, n_a = bench_a(True); bench_a(False)
    k_b = ("H", "s", "S")
    ok_b1 = equal(bench_run(Agent7, [1.0, 0.0], [(BENCH["phase1"], 0.0, p), (BENCH["phase2"], 0.0, p)]),
                  bench_run(Agent6, [1.0, 0.0], [(BENCH["phase1"], 0.0, p), (BENCH["phase2"], 0.0, p)]), k_b)
    ok_b2 = equal(bench_run(Agent7, [1.0, 0.0], [(BENCH["phase1"], p, 0.0), (BENCH["phase2"], 0.0, p)]),
                  bench_run(Agent6, [1.0, 0.0], [(BENCH["phase1"], p, 0.0), (BENCH["phase2"], 0.0, p)]), k_b)
    print(f"(b) selection untouched, identity: circuit states (s, S) and the held odour with the rule bitwise equal to Agent6's: protocol (a) {ok_b1};"
          f" the H21 bench (a) protocol (channel 0 held, then channel 1 alone) {ok_b2}")
    oks = []
    k_c = ("H", "s", "S", "NAV", "SINCE", "TGT")
    for name, kv, sched in (("0/0", [0.0, 0.0], [(BENCH["steps_c"], p, p)]), ("+1/+1", [1.0, 1.0], [(BENCH["steps_c"], p, p)]),
                            ("+1/-1", [1.0, -1.0], [(BENCH["steps_c"], p, p)]), ("+1/0 valued held", [1.0, 0.0], [(BENCH["steps_c_held"], p, 0.0)])):
        oks.append(equal(bench_run(Agent7, kv, sched), bench_run(Agent6, kv, sched), k_c))
        print(f"(c) inertness, identity: values {name}, {sched[0][0]} steps: nav, cast clock, target and circuit states bitwise equal to Agent6's {oks[-1]}")
    print("(d) leave and resample, task geometry: World7 on the bench seeds, placed at the neutral source, neutral hold constructed (s 2.0 / 0, S 0), 300 steps;"
          " statistic = holding the valued odour at step 300")
    lo_d, pt_d, k_d = bench_d(True); _, pt_off, k_off = bench_d(False)
    print(f"   diagnosis check (design section 2): without the rule {k_off}/{BENCH['rows']} = {pt_off:.3f} hold the valued odour at step 300"
          f" -> {'at most 0.5: consistent with the reading that non-revision is a sampling failure' if pt_off <= 0.5 else 'ABOVE 0.5: the sampling-failure reading is WRONG'}")
    verdict = lo_a >= 0.95 and lo_d >= 0.50 and ok_b1 and ok_b2 and all(oks)
    print(f"== M4: (a) lower bound {lo_a:.3f} >= 0.95 over {n_a} holding rows -> {'PASS' if lo_a >= 0.95 else 'FAIL'}; (b) identities {[ok_b1, ok_b2]};"
          f" (c) identities {oks}; (d) {k_d}/{BENCH['rows']} lower bound {lo_d:.3f} >= 0.50 -> {'PASS' if lo_d >= 0.50 else 'FAIL'}"
          f" -> {'PASS: the task may be run' if verdict else 'NO CANDIDATE: the rule as specified does not do what section 3 says; the task is NOT run'} ==")
    return verdict


# ------------------------------------------------------------------ self-checks
def seeds_unused():
    """design section 9: none of the seven numbers appears in any other file under the repository (recursive; excluded:
    this file, its outputs, the H22 design and report, and master_plan.md, which cite them by construction)"""
    pat = re.compile(rb"(?<!\d)(9870|9970|1755|1855|20260929|20260930|20260931)(?!\d)"); hits = []
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for f in files:
            if f == "ph20.py" or (f.startswith("ph20_") and f.endswith(".txt")) or f.startswith("h22_") or f == "master_plan.md": continue
            if pat.search(open(os.path.join(root, f), "rb").read()): hits.append(os.path.relpath(os.path.join(root, f), repo))
    return hits


def pair7(kv_fn, resample, n=40, steps=200, seed=(5, 6)):
    ws = [World7(n, np.random.default_rng(seed[0]), seed[0]) for _ in (0, 1)]; kv = kv_fn(ws[0])
    ag = [Agent7(n, np.random.default_rng(seed[1]), G=G_STAR, known=kv, rule=True, resample=resample), Agent6(n, np.random.default_rng(seed[1]), G=G_STAR, known=kv, rule=True)]
    for a in ag: a.cast_sign = cast_draw(seed[1], n)
    for _ in range(steps):
        for w, a in zip(ws, ag):
            t, _ = a.act(w, w.sense(), w.wind_on()); w.move(t); a.bump(w.bumped)
    return np.array_equal(ws[0].pos, ws[1].pos) and np.array_equal(ws[0].head, ws[1].head) and np.array_equal(ag[0].sel.s, ag[1].sel.s)


def demo():
    print(f"== H22 self-checks (demo). design {DESIGN}; this file sha256 {sha()} ==")
    ph19.demo()                                       # the H21 chain: Agent6 = Agent4 identities, gate, geometry, priority
    n = 40; rows = np.arange(n)
    def kv(w, vg, vo): k = np.zeros((n, 2)); k[rows, w.good] = vg; k[rows, 1 - w.good] = vo; return k
    assert pair7(lambda w: kv(w, 1.0, 0.0), False), "resample off is not Agent6"
    for vg, vo in ((0.0, 0.0), (1.0, 1.0), (1.0, -1.0)):
        assert pair7(lambda w: kv(w, vg, vo), True), f"resample on at {vg}/{vo} is not Agent6"
    assert not pair7(lambda w: kv(w, 1.0, 0.0), True), "resample on at +1/0 changed nothing over 40 rows x 200 steps"
    print("ok  Agent7 with the rule off is Agent6 bitwise; with the rule on it is Agent6 at 0/0, +1/+1 and +1/-1, and differs at +1/0 (40 rows x 200 steps)")
    res = {}
    for rs in (True, False):                          # constructed state: neutral held, neutral whiff every step
        a = Agent7(100, np.random.default_rng(3), G=G_STAR, known=np.tile([1.0, 0.0], (100, 1)), rule=True, resample=rs); a.sel.s[:, 1] = 2.0; w = Still(100); nv, hh = [], []
        for _ in range(100):
            x = np.zeros((100, 2), bool); x[:, 1] = True
            _, h = a.act(w, x, np.ones(100, bool)); nv.append(a.nav_hit.copy()); hh.append(h == 1)
        nv, hh = np.array(nv), np.array(hh); res[rs] = (hh.mean(), nv[hh].mean(), a.silence.max())
    assert res[True][0] == 1.0 and res[True][1] == 0.0 and res[False][1] == 1.0 and res[True][2] == res[False][2] == 0.0, f"constructed state {res}"
    print(f"ok  constructed state, neutral held and a neutral whiff every step for 100 steps: held on every step; nav True on {res[True][1]*100:.0f}% of held steps with the rule,"
          f" {res[False][1]*100:.0f}% without; the silence timer still reset by every hit (max {res[True][2]:.0f}) in both")
    seeds = (5, 6)
    rsm, mnt = run("resample", seeds, runs=n, steps=200), run("maintain", seeds, runs=n, steps=200)
    assert same(mnt, run("maintain", seeds, runs=n, steps=200, cls=Agent6)), "maintain arm is not Agent6"
    for arm in ("neutral", "priority-identity"):
        assert same(run(arm, seeds, runs=n, steps=200), run(arm, seeds, runs=n, steps=200, cls=Agent6)), f"{arm} arm is not Agent6"
    ok3, cnt = separation(rsm, mnt); assert ok3 and cnt["withheld"] > 0 and cnt["never_equal"] == cnt["never"], f"separation {cnt}"
    ka = run("known-answer", seeds, runs=n, steps=200)
    assert (ka["H"] == ka["good"][None, :]).all() and np.array_equal(ka["NAV"], ka["W"][:, rows, ka["good"]]), "known-answer: h or hit wrong"
    assert np.array_equal(ka["cast"], rsm["cast"]) and np.array_equal(ka["good"], rsm["good"]), "arms differ in cast draw or assignment"
    assert not rsm["WH"][rsm["H"] != (1 - rsm["good"])[None, :]].any(), "a surge was withheld while the neutral odour was not held"
    print(f"ok  run level (40 rows x 200 steps): maintain, neutral and priority-identity arms equal Agent6's runs; resample vs maintain separation {cnt};"
          " withheld only while the neutral odour is held; known-answer h and hit; same cast draw and assignment across arms")
    hits = seeds_unused(); assert not hits, f"a seed of this run appears in {hits}"
    print(f"ok  seeds {SEEDS}, bench {BENCH['seed_w']}/{BENCH['seed_a']}, bootstrap {ph15.BOOT_SEED} appear in no other file under the repository")


# ------------------------------------------------------------------ criteria (design section 7)
def judge(res, maj, first, seeds):
    rows = np.arange(R); ok = lambda z: "PASS" if z else "FAIL"
    print("\n== criteria (design v1 FINAL section 7; 95 percent, one evaluation, no extension; aggregation: PASS if every part passes, FAIL if any fails, else INCONCLUSIVE) ==")
    m1 = []
    for arm in ("neutral", "pathway-off", "known-answer"):
        z = maj[arm][2]; m1.append(ok(z.mean() <= 0.20)); print(f"   M1(a) {arm}: ties {z.sum()}/{R} = {z.mean():.3f}  at most 0.20 -> {m1[-1]}")
    o = res["neutral"]; V, N, Z = maj["neutral"]; which = np.where(V, o["good"], np.where(N, 1 - o["good"], -1))
    m1.append(crit("M1(b) neutral, P(+y source majority | chose)", "P", (0.35, 0.65), False, (which == o["plus_y"])[~Z]))
    V, N, Z = maj["pathway-off"]; m1.append(crit("M1(c) floor: pathway-off, P(V | chose)", "P", (0.35, 0.65), False, V[~Z]))
    m1.append(crit("M1(d) ceiling: known-answer, P(V) over all rows", "P", 0.85, False, maj["known-answer"][0]))
    M1 = agg(m1); print(f"   M1 -> {M1}{'' if M1 == 'PASS' else '  (the run is UNREADABLE under section 8)'}")
    ties = {arm: maj[arm][2].mean() for arm in ("resample", "maintain")}
    print(f"   section 8: ties in the arms under test, resample {ties['resample']:.3f}, maintain {ties['maintain']:.3f} (unreadable above 0.20)")
    Vr, Nr, Zr = maj["resample"]; Vm = maj["maintain"][0]; Vp = maj["pathway-off"][0]; Vk = maj["known-answer"][0]
    m2 = [crit("M2(a) resample, P(V) over all rows", "P", 0.75, False, Vr)]
    for c in range(4): m2.append(crit(f"M2(b) resample, cell {c} ({CELLS[c]}), P(V)", "P", 0.55, False, Vr[res["resample"]["cell"] == c]))
    m2.append(crit("M2(c) DP = P(V) resample - maintain, same rows", "DP", 0.05, False, Vr.astype(float), Vm.astype(float)))
    M2 = agg(m2); print(f"   M2 -> {M2}")
    _, pt, lo, hi = interval("DP", Vr.astype(float), Vp.astype(float)); print(f"      reported, no bar: DP resample - pathway-off {pt:+.3f} [{lo:+.3f}, {hi:+.3f}]")
    print(f"      reported: resample N {Nr.sum()} tie {Zr.sum()}; P(V) resample / known-answer = {Vr.mean():.3f} / {Vk.mean():.3f} = {Vr.mean()/Vk.mean() if Vk.mean() else float('nan'):.3f} of the ceiling")
    for arm in ("resample", "maintain"):
        d = diagnostics(res[arm]); V = maj[arm][0]
        print(f"      reported: {arm} P(V | first hold valued) {int((V & d['fh_v']).sum())}/{int(d['fh_v'].sum())}, P(V | first hold neutral) {int((V & d['fh_n']).sum())}/{int(d['fh_n'].sum())}")
    for arm in ("resample", "maintain", "pathway-off", "known-answer"):
        Vf, Nf, Zf = first[arm]; k, pt, lo, hi = interval("P", Vf)
        print(f"      reported, secondary first reach, {arm}: V {Vf.sum()} N {Nf.sum()} none {Zf.sum()}; P(V first) {k}/{R} = {pt:.3f} [{lo:.3f}, {hi:.3f}]")
    i1 = same(res["maintain"], run("maintain", seeds, cls=Agent6))
    n6 = run("neutral", seeds, cls=Agent6); i2n = same(res["neutral"], n6); i2g0 = same(n6, run("neutral", seeds, cls=Agent6, G=0.0, gate=False)); ag3 = identity_agent3(seeds)
    p6 = run("priority-identity", seeds, cls=Agent6); i2p = same(res["priority-identity"], p6); i2p4 = same(p6, run("priority-identity", seeds, cls=Agent4))
    i3, cnt = separation(res["resample"], res["maintain"])
    ka = res["known-answer"]; i4 = bool((ka["H"] == ka["good"][None, :]).all() and np.array_equal(ka["NAV"], ka["W"][:, rows, ka["good"]]))
    M3 = agg([ok(i1), ok(i2n and i2g0 and ag3 and i2p and i2p4), ok(i3), ok(i4)])
    print(f"   M3 identities: (i) maintain (Agent7, rule off) == ph19.Agent6 {i1}; (ii) neutral with the rule == Agent6 {i2n}, Agent6 at 0/0 == G 0 {i2g0}, G 0 == ph14.Agent3 {ag3};"
          f" priority-identity with the rule == Agent6 {i2p}, Agent6 at +1/-1 == ph16.Agent4 {i2p4}; (iii) resample vs maintain bitwise equal up to the first withheld surge {i3}"
          f" {cnt}; (iv) known-answer h = valued and hit = its whiffs {i4} -> {M3}")
    lo_a, n_a = bench_a(True, quiet=True); lo_d, pt_d, k_d = bench_d(True, quiet=True)
    M4 = agg([ok(lo_a >= 0.95), ok(lo_d >= 0.50)])
    print(f"   M4 mechanism bench, (a) and (d) re-run here with the bench seeds: (a) lower bound {lo_a:.3f} over {n_a} holding rows >= 0.95; (d) {k_d}/{BENCH['rows']} = {pt_d:.3f},"
          f" lower bound {lo_d:.3f} >= 0.50 -> {M4}")
    exp1, cmp1, took = priority_check6(G_STAR)
    M5 = ok(i2p and i2p4)
    print(f"   M5 avoidance: +1/-1 agent is Agent6 = the Run 2 agent by construction (M3 ii {i2p and i2p4}); H21's constructed state: negative odour held on {exp1} (row, step),"
          f" target = flee side on every one, equal to G 0's on the {cmp1} steps both hold it; the valued odour took the hold on {took} afterwards -> {M5}")
    nw_r, nw_m = no_whiff_last_third(res["resample"]).astype(float), no_whiff_last_third(res["maintain"]).astype(float)
    m6 = [crit("M6(a) no whiff of either plume in the last third, resample - maintain", "DP", 0.05, True, nw_r, nw_m)]
    cm = res["resample"]["contacts"].mean(); m6.append(ok(cm <= 0.10)); print(f"   M6(b) resample, wall contacts per row: mean {cm:.3f}  at most 0.10 -> {m6[-1]}")
    M6 = agg(m6)
    print(f"   M6 -> {M6}      reported: no whiff in the last third resample {int(nw_r.sum())} maintain {int(nw_m.sum())} known-answer {int(no_whiff_last_third(res['known-answer']).sum())};"
          f" no navigation hit in the last third " + ", ".join(f"{a} {int(no_nav_last_third(res[a]).sum())}" for a in ARMS)
          + f"; cast clock max resample {res['resample']['SINCE'].max():.0f} maintain {res['maintain']['SINCE'].max():.0f}; withheld (row, step) resample {int(res['resample']['WH'].sum())}")
    unread = M1 != "PASS" or max(ties.values()) > 0.20
    verdict = all(x == "PASS" for x in (M1, M2, M3, M4, M5, M6))
    print(f"\n== H22 ==  M1 {M1}  M2 {M2}  M3 {M3}  M4 {M4}  M5 {M5}  M6 {M6}  -> "
          + ("the rule makes a neutral-holding agent leave the neutral source and take the valued odour, and with it the agent stays at the valued source"
             " in more rows than the H21 maintain agent, without adding lost rows" if verdict else "UNREADABLE (section 8)" if unread else "NOT shown under the registered criteria"))


def main(mode):
    seeds = SEEDS[mode]
    print(f"== H22, {mode.upper()}. design {DESIGN}; this file sha256 {sha()}; G {G_STAR}, gate on where G 2; world seed {seeds[0]}, agent seed {seeds[1]};"
          f" {R} rows x {T} steps; geometry C0; {'operation check only' if mode == 'dev' else 'the one evaluation'} ==")
    print("   rows share no state: one generator per world and one per agent population, fixed-size draws consumed in row order every step")
    res = {arm: run(arm, seeds) for arm in ARMS}
    maj = {arm: majority(res[arm]) for arm in ARMS}; first = {arm: outcome(res[arm]) for arm in ARMS}
    for arm in ARMS:
        describe_majority(arm, res[arm], *maj[arm]); h21_diag(arm, res[arm]); h22_diag(arm, res[arm], res["maintain"] if arm == "resample" else None)
        print("      secondary, first reach and diagnostics:"); describe(arm, res[arm], *first[arm])
    judge(res, maj, first, seeds)


if __name__ == "__main__":
    mode = ([m for m in sys.argv[1:] if m in ("demo", "bench", "dev", "eval")] or ["demo"])[0]
    if mode == "demo": demo(); sys.exit(0)
    if mode == "bench": sys.exit(0 if bench() else 1)
    main(mode)
