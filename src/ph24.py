#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H25: silence-timeout release (a reset-control change).

Usage: python ph24.py demo | bench | dev | eval

Design v2 FINAL, confirmed by the owner (decision:h25-open, '추천안으로 확정'): doc dce297e76390fa854, hash 6fbb293b...e60b,
stored before this file existed. ONE change, a mixin on the adopted act (no adopted module edited, no act copied):
(S) while the timeout's drive is being delivered and any selection unit is still above 1.0 after the drive step, the
silence counter is set to RESET_AFTER + 1 so the base's own line delivers the same 10.0 drive again on the next step;
it stops when both units are at or below 1.0, on a whiff of the held odour, or when the evidence release fires.
(Z) the counter is zeroed on the step a hold forms. Agent10 = Release + ph21.Agent8 (the adopted agent; identity and
regression arm), Agent10g = Release + ph19.Agent6 (the H21 gate agent; the behavioural arm). release=False IS the
base agent bitwise (checked). The flag is called `release`, not `fix`, because ph14.Agent3 already owns `self.fix`
(its H19 (a) switch). Measurement only: `sustain` (a drive continues next step), `zreset` (Z lowered the counter).
Worlds: T1 ph16.World7; W1 ph22.Masked (valued column False from step 0); T3a ph22.Masked from step 0 with the start
at the valued source and a valued hold constructed; T3b ph23.Lost (mask on from t0 150). Nothing changes after the table.
"""
import sys, os, re, math, hashlib
import numpy as np
import ph2, ph9, ph11, ph13, ph14, ph14b, ph15, ph16, ph17, ph18, ph19, ph21, ph22, ph23
from ph16 import World7, Agent4, Still, cast_draw, diagnostics, describe, interval, crit, med, R, T
from ph17 import Agent5
from ph18 import majority, describe_majority, agg
from ph19 import Agent6, h21_diag
from ph21 import Agent8, G_STAR, q3, first_true
from ph13 import World4
from ph14 import Agent3
from ph11 import RESET_AFTER, MARGIN

sys.stdout.reconfigure(newline="\n")            # LF output, so the recorded sha256 equals the committed blob
DESIGN = "v2 FINAL doc dce297e76390fa854 hash 6fbb293bfb14acbc941998ccc1b7934ec20d0b873131bf9c2ba90e925fcce60b"
T0 = ph23.T0                                    # 150
SEEDS = dict(dev=(9896, 9996), eval=(1805, 1905))
BENCH = dict(rows=400, steps_b=200, steps_c=600, steps=600, seed_w=20261031, seed_a=20261032)
BS = (BENCH["seed_w"], BENCH["seed_a"])
REPRO = dict(h21=(1725, 1825), h23=(1765, 1865), h19=(9600, 9700))   # reused on purpose, read for no criterion; NOT in the seed scan
ph15.BOOT_SEED = 20261033                       # design section 7 (set after the imports, which set their own); ph16 set 95 percent
MODS = (ph2, ph9, ph11, ph13, ph14, ph14b, ph15, ph16, ph17, ph18, ph19, ph21, ph22, ph23)


def sha(p=__file__): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def q3f(x, f=".1f"): return f"{np.percentile(x, 25):{f}}/{np.median(x):{f}}/{np.percentile(x, 75):{f}}" if len(x) else "n/a"


# ------------------------------------------------------------------ the change (design section 3)
class Release:
    """H25 reset control, wrapped around the adopted act. release=False: the base act, untouched."""

    def __init__(self, *a, release=True, **kw):
        super().__init__(*a, **kw); self.release = release
        self.sustain = np.zeros(self.R, bool); self.zreset = np.zeros(self.R, bool)

    def act(self, w, whiffs, wind_on):
        if not self.release: return super().act(w, whiffs, wind_on)
        rows = np.arange(self.R); hp = self.held()
        turn, h = super().act(w, whiffs, wind_on)
        hit = (h >= 0) & whiffs[rows, np.maximum(h, 0)]
        new = (h >= 0) & (h != hp)
        sustain = self.due_timeout & ~self.due_evidence & (self.sel.s > 1.0).any(1) & ~hit          # (S)
        self.sustain, self.zreset = sustain, new & ~sustain & (self.silence > 0)                     # measurement
        self.silence = np.where(sustain, RESET_AFTER + 1.0, np.where(new, 0.0, self.silence))        # (S), (Z)
        return turn, h


class Agent10(Release, Agent8): """the adopted full agent (H23 filter) + H25"""
class Agent10g(Release, Agent6): """the H21 gate agent + H25"""
class Agent4R(Release, Agent4): """bench (e), the design's agent: Agent4 at G 0 with zero values (= ph14.Agent3 with H19 (a) on) + H25"""


class Agent3x(Agent3):
    """bench (e), ph14b's own agent (ph14.Agent3, fix=False, learning off) exposing the two release flags. The timeout flag is
    read before act (the base's own expression); the evidence flag is read at the circuit call from the arguments Agent3 passes
    (the ph14b spy method: the instance's step is wrapped, the circuit is untouched)."""

    def __init__(self, runs, rng, **kw):
        super().__init__(runs, rng, **kw)
        self.due_timeout = self.due_evidence = np.zeros(runs, bool); orig = self.sel.step
        def step(y, reset=0.0):
            rows = np.arange(self.R); hp = self.held(); hi = np.maximum(hp, 0)
            self.due_evidence = (hp >= 0) & ((y[rows, 1 - hi] - y[rows, hi]) > MARGIN)
            return orig(y, reset=reset)
        self.sel.step = step

    def act(self, w, whiffs, wind_on):
        self.due_timeout = self.silence > RESET_AFTER
        return super().act(w, whiffs, wind_on)


class Agent3R(Release, Agent3x): """bench (e), ph14b's agent + H25"""


def make(cls, runs, rng, G, known, gate=True, filt=True, release=True):
    kw = dict(rule=gate, filt=filt) if cls in (Agent10, Agent8) else dict(rule=gate) if cls in (Agent10g, Agent6) else {}
    if cls in (Agent10, Agent10g): kw["release"] = release
    return cls(runs, rng, G=G, known=known, **kw)


# ------------------------------------------------------------------ runs (design sections 4-6)
def record(o, t, a, h, x, pa):
    rows = np.arange(a.R)
    o["H"][t] = h; o["W"][t] = x; o["PA"][t] = pa; o["NAV"][t] = a.nav_hit; o["TO"][t] = a.due_timeout; o["EV"][t] = a.due_evidence
    o["SUS"][t] = getattr(a, "sustain", False); o["Z"][t] = getattr(a, "zreset", False); o["SIL"][t] = a.silence
    o["SINCE"][t] = a.since; o["TGT"][t] = getattr(a, "tgt", 0.0); o["S"][t] = a.sel.s; o["SG"][t] = a.sel.S[:, 0]


def blank(steps, runs):
    b = lambda dt=bool: np.zeros((steps, runs), dt)
    return dict(H=np.full((steps, runs), -1, np.int8), W=np.zeros((steps, runs, 2), bool), PA=b(), NAV=b(), TO=b(), EV=b(), SUS=b(), Z=b(),
                SIL=b(np.float32), SINCE=b(np.float32), TGT=b(float), S=np.zeros((steps, runs, 2)), SG=b(float))


def run(world, cls, vals, seeds, G=G_STAR, gate=True, filt=True, release=True, fixed=None, runs=R, steps=T, t0=T0):
    """world 'T1' (World7), 'W1' (ph22.Masked, valued column False from step 0), 'T3a' (W1's world, start at the valued source,
    valued hold s 2.0 constructed), 'T3b' (ph23.Lost, mask on from t0). fixed: None | 'valued' | 'neutral' | 'valued-then-neutral'
    (Agent5, G 0). Construction order as ph23.run: world, mask, twin, values, agent, cast draw, position, hold."""
    masked = world != "T1"
    w = (ph23.Lost if world == "T3b" else ph22.Masked if masked else World7)(runs, np.random.default_rng(seeds[0]), seeds[0])
    rows = np.arange(runs); g = w.good; neutral = 1 - g
    if masked: w.pres = neutral.copy(); w.absent = g.copy()
    tw = World7(runs, np.random.default_rng(seeds[0]), seeds[0]) if masked else None
    kv = np.zeros((runs, 2)); kv[rows, g] = vals[0]; kv[rows, neutral] = vals[1]
    rng = np.random.default_rng(seeds[1])
    if fixed: a = Agent5(runs, rng, fixed=(neutral if fixed == "neutral" else g).copy(), G=0.0, known=kv)
    else: a = make(cls, runs, rng, G, kv, gate, filt, release)
    a.cast_sign = cast_draw(seeds[1], runs)
    if world == "T3a":
        w.pos = w.src[rows, g].copy(); a.sel.s[rows, g] = 2.0
    o = dict(world=world, arm=type(a).__name__, good=g, cell=w.cell, plus_y=w.plus_y, src=w.src.copy(), G=a.G, fixed=bool(fixed), steps=steps,
             cast=a.cast_sign.copy(), start=w.pos.copy(), s0=a.sel.s.copy(), H0=a.held(), draws_equal=True, rng_equal=True,
             POS=np.zeros((steps, runs, 2)), HEAD=np.zeros((steps, runs)), AT2=np.zeros((steps, runs, 2), bool), C=np.zeros((steps, runs), bool), **blank(steps, runs))
    for t in range(steps):
        if world == "T3b": w.on = t >= t0
        if fixed == "valued-then-neutral" and t == t0: a.fixed = neutral.copy()
        if masked: tw.pos, tw.head = w.pos.copy(), w.head.copy()
        pa = (a.sel.s > 1.0).any(1)
        x = w.sense(); on = w.wind_on()
        if masked:
            tr = tw.sense(); mon = world != "T3b" or t >= t0
            o["draws_equal"] &= bool(np.array_equal(tr, w.raw) and np.array_equal(on, tw.wind_on()) and np.array_equal(x[rows, neutral], tr[rows, neutral])
                                     and np.array_equal(x[rows, g], np.zeros(runs, bool) if mon else tr[rows, g]))
        turn, h = a.act(w, x, on)
        record(o, t, a, h, x, pa)
        w.move(turn); a.bump(w.bumped)
        o["POS"][t] = w.pos; o["HEAD"][t] = w.head; o["AT2"][t] = w.at_source(); o["C"][t] = w.bumped
    if masked: o["rng_equal"] = w.rng.bit_generator.state == tw.rng.bit_generator.state
    at = o["AT2"]; o["dwell"] = at.sum(0).astype(float); o["contacts"] = o["C"].sum(0).astype(float)
    o["first"] = np.where(at.any(0), at.argmax(0), -1)
    return o


def stub(cls, known, sched, hold=None, release=True, rows=BENCH["rows"], seeds=BS):
    """ph16.Still stub; sched: list of (steps, p channel 0, p channel 1); the same uniform draws for every condition; hold: channel set to s 2.0"""
    steps = sum(s for s, _, _ in sched); u = np.random.default_rng(seeds[0]).random((steps, rows, 2))
    a = make(cls, rows, np.random.default_rng(seeds[1]), G_STAR, np.tile(known, (rows, 1)), release=release); w = Still(rows)
    if hold is not None: a.sel.s[:, hold] = 2.0
    o = dict(H0=a.held(), steps=steps, **blank(steps, rows)); t = 0
    for n, p0, p1 in sched:
        for _ in range(n):
            x = np.stack([u[t, :, 0] < p0, u[t, :, 1] < p1], 1); pa = (a.sel.s > 1.0).any(1)
            _, h = a.act(w, x, np.ones(rows, bool)); record(o, t, a, h, x, pa); t += 1
    return o


# ------------------------------------------------------------------ identities
FIELDS = ("POS", "HEAD", "S", "SG", "H", "NAV", "SINCE", "TGT")            # section 3's list; the counter excluded
TRAJ = ("POS", "HEAD", "NAV", "SINCE", "TGT")
def keys(o, ks): return [k for k in ks if k in o]
def bitwise(o1, o2, ks=FIELDS + ("SIL", "TO", "EV"), n=None): return all(np.array_equal(o1[k][:n], o2[k][:n]) for k in keys(o1, ks))
def traj(o1, o2, n=None): return bitwise(o1, o2, TRAJ, n)


def separation(of, ob):
    """identity (b): every field of section 3 equal on every step before the row's first BASE timeout firing while a unit is above
    threshold (before the step); rows without such a firing equal throughout. Returns (ok, counts)."""
    ks = keys(of, FIELDS); steps = of["H"].shape[0]
    eq = np.ones(of["H"].shape, bool)
    for k in ks:
        e = of[k] == ob[k]
        eq &= e.reshape(e.shape[0], e.shape[1], -1).all(2)
    fd = first_true(ob["TO"] & ob["PA"]); never = fd < 0
    before = np.arange(steps)[:, None] < np.where(never, steps, fd)[None, :]
    pre = (eq | ~before).all(0); whole = eq.all(0)
    ok = bool(pre.all() and (whole | ~never).all())
    return ok, dict(rows_without_firing=int(never.sum()), with_firing=int((~never).sum()), with_firing_equal_throughout=int((~never & whole).sum()),
                    first_firing_step=q3(fd[~never]))


# ------------------------------------------------------------------ events: holds, drives, gaps
def events(o):
    """per (row) hold segments and timeout drives. A drive starts at a timeout step not preceded by a sustain step; it lasts while
    `sustain` stays True. origin = the step of the held odour's last hit or of the hold's formation (formation at -1 for a hold held
    at construction). Returns a dict of flat lists."""
    H, W, TO, SUS, EV, S = o["H"], o["W"], o["TO"], o["SUS"], o["EV"], o["S"]; steps, n = H.shape; rows = np.arange(n)
    prev = np.vstack([o["H0"][None, :].astype(np.int8), H[:-1]])
    hit = (H >= 0) & W[np.arange(steps)[:, None], rows[None, :], np.maximum(H, 0)]
    form = (H >= 0) & (H != prev)
    ORG = np.zeros((steps, n)); last = np.where(o["H0"] >= 0, -1.0, -1e9)
    for t in range(steps):
        ORG[t] = last; last = np.where(form[t] | hit[t], t, last)
    ds = TO & ~np.vstack([np.zeros((1, n), bool), SUS[:-1]])
    dr = dict(t=[], r=[], D=[], hp=[], silent=[], ended=[], end=[], interrupted=[], empty=[], trunc=[])
    for t, r in zip(*np.nonzero(ds)):
        e = t
        while SUS[e, r] and e + 1 < steps: e += 1
        hp = int(prev[t, r]); seg = H[t:e + 1, r]
        ch = np.flatnonzero(seg != hp) if hp >= 0 else np.array([], int)
        dr["t"].append(t); dr["r"].append(r); dr["D"].append(e - t + 1); dr["hp"].append(hp)
        dr["silent"].append(int(t - ORG[t, r] - 1) if hp >= 0 else -1); dr["ended"].append(len(ch) > 0); dr["end"].append(int(t + ch[0]) if len(ch) else -1)
        dr["interrupted"].append(bool(hit[e, r] or EV[e, r])); dr["empty"].append(bool((S[e, r] <= 1.0).all())); dr["trunc"].append(bool(SUS[e, r] and e == steps - 1))
    dr = {k: np.array(v, dtype=bool if k in ("ended", "interrupted", "empty", "trunc") else int) for k, v in dr.items()}
    segs, gaps, gaps_in = [], [], []
    for r in range(n):
        h = H[:, r]; t = 0
        while t < steps:
            if h[t] < 0: t += 1; continue
            k = h[t]; s0 = t
            while t < steps and h[t] == k: t += 1
            segs.append((r, s0, t - s0, t < steps)); hh = hit[s0:t, r]; hi = np.flatnonzero(hh)
            if len(hi) == 0: gaps.append(t - s0); continue
            gaps += [hi[0]] + list(np.diff(hi) - 1) + [t - s0 - 1 - hi[-1]]; gaps_in += list(np.diff(hi) - 1)
    return dict(drives=dr, segs=np.array(segs).reshape(-1, 4), gaps=np.array(gaps), gaps_in=np.array(gaps_in), ORG=ORG, hit=hit, prev=prev, form=form)


def on_hold(dr): return dr["hp"] >= 0


def drive_summary(o, name, say):
    ev = events(o); dr = ev["drives"]; m = on_hold(dr); sg = ev["segs"]
    fz = int(o["Z"].sum()); D = dr["D"][m]
    say(f"      [{name}] timeout drives started on a hold {int(m.sum())} (drive steps delivered {int(D.sum())}), D quartiles {q3(D) if len(D) else 'n/a'}, D max {D.max() if len(D) else 0};"
        f" ended the hold {int(dr['ended'][m].sum())}; circuit empty at the drive's end {int(dr['empty'][m].sum())}; interrupted by a hit or the evidence release {int(dr['interrupted'][m].sum())};"
        f" silent steps before the drive (quartiles) {q3(dr['silent'][m]) if m.any() else 'n/a'}, stale (< 41) {int((dr['silent'][m] < 41).sum())}; nothing-held drives {int((~m).sum())}"
        f" (D > 1 among them {int((dr['D'][~m] > 1).sum())}); counter lowered by (Z) {fz}")
    if len(sg): say(f"      [{name}] holds {len(sg)}; duration quartiles {q3(sg[:, 2])} (ended within the run {int(sg[:, 3].sum())}); held odour's silent gaps while held {len(ev['gaps'])},"
                    f" quartiles {q3(ev['gaps'])}, >= 41 {int((ev['gaps'] >= 41).sum())} ({(ev['gaps'] >= 41).mean() if len(ev['gaps']) else float('nan'):.4f})")
    return ev


# ------------------------------------------------------------------ bench (e): the H19 ph14b protocol
def chain(kind, release, seeds=REPRO["h19"], runs=200, steps=2400):
    w = World4(runs, np.random.default_rng(seeds[0])); rng = np.random.default_rng(seeds[1])
    a = Agent3R(runs, rng, release=release, fix=False, abl=("learn",)) if kind == "Agent3" else Agent4R(runs, rng, release=release, G=0.0, known=np.zeros((runs, 2)))
    o = dict(H0=a.held(), steps=steps, **blank(steps, runs)); HP = np.full((steps, runs), -1)
    for t in range(steps):
        HP[t] = a.held(); pa = (a.sel.s > 1.0).any(1); x = w.sense()
        turn, h = a.act(w, x, w.wind_on()); w.move(turn); a.bump(w.bumped); record(o, t, a, h, x, pa)
    o["HP"] = HP; return o


def chain_stats(o, say, label):
    TO, EV, H, S, G, HP = o["TO"], o["EV"], o["H"], o["S"], o["SG"], o["HP"]; steps = H.shape[0]; RST = np.where(TO | EV, 10.0, 0.0)
    out = {}
    for lab, m in (("silence timeout", TO & (HP >= 0)), ("evidence release", (RST > 0) & ~TO & (HP >= 0))):        # ph14b.chain's measurement
        tt, rr = np.nonzero(m); keep = tt < steps - 9; tt, rr = tt[keep], rr[keep]; ch = HP[tt, rr]
        before = S[np.maximum(tt - 1, 0), rr, ch]; after = np.array([S[t:t + 9, r, c].min() for t, r, c in zip(tt, rr, ch)])
        glob = np.array([G[t:t + 9, r].max() for t, r in zip(tt, rr)]); rel = np.array([(H[t:t + 9, r] == -1).any() for t, r in zip(tt, rr)])
        runl = np.array([int(np.argmin(np.r_[RST[t:t + 12, r] > 0, False])) for t, r in zip(tt, rr)])
        out[lab] = (len(tt), float(np.median(runl)), float(rel.mean()))
        say(f"      {label} {lab:16s} requests {len(tt):5d} | value delivered {np.unique(RST[tt, rr])} | consecutive steps with a reset: median {np.median(runl):3.0f} |"
            f" held unit before {np.median(before):4.2f}, lowest in the next 8 steps {np.median(after):4.2f} | global unit peak {np.median(glob):5.2f} | released within 8 steps {rel.mean()*100:5.1f}%")
    dr = events(o)["drives"]; m = on_hold(dr) & ~dr["interrupted"] & ~dr["trunc"]
    k, pt, lo, hi = interval("P", dr["empty"][m]) if m.any() else (0, float("nan"), float("nan"), float("nan"))
    stay = np.array([bool((S[e + 1:e + 9, r] <= 1.0).all()) for t, r, D in zip(dr["t"][m], dr["r"][m], dr["D"][m]) for e in [t + D - 1]])
    say(f"      {label} drives started on a held unit {int(on_hold(dr).sum())}, not interrupted by a hit or the evidence release {int(m.sum())}: circuit empty at the drive's end {k}/{int(m.sum())}"
        f" = {pt:.3f} [{lo:.3f}, {hi:.3f}]; D quartiles {q3(dr['D'][m]) if m.any() else 'n/a'}, max {dr['D'][m].max() if m.any() else 0}; both units <= 1.0 on the 8 steps after {int(stay.sum())}/{len(stay)}")
    return out, lo


# ------------------------------------------------------------------ T3 measures
def t3a_release(o):
    """M7(a): the valued hold constructed at step 0 ends at a step <= 49 with both units <= 1.0 at the end step"""
    g = o["good"]; H = o["H"]; n = len(g); r = np.arange(n)
    notv = H != g[None, :]; end = first_true(notv)
    ok = (end >= 0) & (end <= 49) & (o["S"][np.maximum(end, 0), r] <= 1.0).all(1)
    return ok, end


def t3_dwell(o, lo, hi): r = np.arange(len(o["good"])); return o["AT2"][lo:hi, r, 1 - o["good"]].sum(0).astype(float)


def ratio_boot(d, f, c):
    """R = (mean d - mean f) / (mean c - mean f); rows resampled together (ph15's seeded indices, 5000)"""
    i = ph15._resample(len(d)); num = d[i].mean(1) - f[i].mean(1); den = c[i].mean(1) - f[i].mean(1)
    with np.errstate(divide="ignore", invalid="ignore"): bs = num/den
    pt = (d.mean() - f.mean())/(c.mean() - f.mean()) if c.mean() != f.mean() else float("nan")
    lo, hi = np.nanpercentile(bs, [ph15.QLO, ph15.QHI]); return float(pt), float(lo), float(hi)


def pass_prob_R(R0, sd, span, n=400, bar=0.5):
    se = sd/math.sqrt(n)*math.sqrt(1 + R0*R0)/span
    return 0.5*(1.0 + math.erf(((R0 - bar)/se - 1.959964)/math.sqrt(2.0)))


def t3b_release(o, t0=T0):
    """rows holding the valued odour at t0 (end of step t0 - 1): the step the valued hold ends relative to its origin"""
    g = o["good"]; H = o["H"]; n = len(g); ev = events(o); ORG = ev["ORG"]; hold = H[t0 - 1] == g
    tt = np.arange(H.shape[0])[:, None]; end = first_true((H != g[None, :]) & (tt >= t0))
    org = np.array([ORG[e, r] if e >= 0 else np.nan for r, e in enumerate(end)]); rel = end - org
    return hold, end, rel


# ------------------------------------------------------------------ bench (design section 4)
def bench(say=print):
    p = 0.30; n = BENCH["rows"]; out = {}; ids = {}
    say(f"== H25 mechanism bench (design v2 section 4). design {DESIGN}; this file sha256 {sha()}; {BENCH}; bootstrap seed {ph15.BOOT_SEED} ==")
    header(say)
    say("   rows share no state: one generator per world and one per agent population, fixed-size draws consumed in row order every step")
    # (b) constructed holds then silence
    say(f"(b) release on constructed states: stub, {n} rows, no input for {BENCH['steps_b']} steps, s 2.0 on the held channel, counter 0; statistic per row: the hold ends at a step <= 49,"
        f" both units <= 1.0 at the end step, no unit above 1.0 from then to step {BENCH['steps_b'] - 1}; bar lower bound >= 0.95")
    sb = [(BENCH["steps_b"], 0.0, 0.0)]; lo_b = []
    for lab, cls, base, hold in (("b1 valued hold, Agent10g", Agent10g, Agent6, 0), ("b2 neutral hold, Agent10g", Agent10g, Agent6, 1), ("b3 valued hold, Agent10", Agent10, Agent8, 0)):
        o = stub(cls, [1.0, 0.0], sb, hold=hold); ob = stub(base, [1.0, 0.0], sb, hold=hold); out[lab] = (o, ob)
        H, S = o["H"], o["S"]; end = first_true(H != hold); r = np.arange(n)
        above_after = np.array([bool((S[e:, i] > 1.0).any()) if e >= 0 else True for i, e in enumerate(end)])
        ok = (end >= 0) & (end <= 49) & (S[np.maximum(end, 0), r] <= 1.0).all(1) & ~above_after
        k, pt, lo, hi = interval("P", ok); lo_b.append(lo)
        dr = events(o)["drives"]; m = on_hold(dr); first = first_true(o["TO"])
        say(f"   ({lab}) exact {k}/{n} = {pt:.3f} [{lo:.3f}, {hi:.3f}] -> {'PASS' if lo >= 0.95 else 'FAIL'}; end step quartiles {q3(end[end >= 0])} (never {int((end < 0).sum())});"
            f" first drive step quartiles {q3(first[first >= 0])}; D per row quartiles {q3(dr['D'][m])}, max {dr['D'][m].max() if m.any() else 0}; S peak median {np.median(o['SG'].max(0)):.2f} max {o['SG'].max():.2f};"
            f" base ({base.__name__}) holding at step {BENCH['steps_b'] - 1}: {int((ob['H'][-1] == hold).sum())}/{n}, its timeout firings {int(ob['TO'].sum())}")
    # (b4) H21 bench (a)'s protocol
    for p1 in (0.30, 0.057):
        for cls in (Agent10g, Agent6):
            o = stub(cls, [1.0, 0.0], [(60, p, 0.0), (200, 0.0, p1)]); h60 = o["H"][59]; dn = h60 == 0; kept = dn & (o["H"][60:] == 0).all(0)
            lastw = np.where(o["W"][:60, :, 0].any(0), 59 - np.argmax(o["W"][:60, :, 0][::-1], 0), -1)
            rel = first_true(o["H"][60:] != 0) + 60; nh = first_true(o["H"][60:] == 1) + 60
            say(f"   (b4) H21 bench (a) protocol, {cls.__name__}, channel 1 p {p1}: holding channel 0 at step 60 {int(dn.sum())}/{n}; kept on every phase-2 step {int(kept.sum())}/{int(dn.sum())};"
                f" release step after the last channel-0 whiff, quartiles {q3((rel - lastw)[dn & (rel >= 60)])}; step the neutral odour is held, quartiles {q3(nh[dn & (nh >= 60)])} (rows {int((dn & (nh >= 60)).sum())})")
    # (c) no false release
    say(f"(c) no false release: stub, {n} rows, {BENCH['steps_c']} steps, a constructed hold with its own channel fed, the other silent, Agent10g; false = a hold ended by a timeout drive that started"
        f" <= {RESET_AFTER} steps after the held odour's last whiff or the hold's formation; bar lower bound >= 0.95")
    lo_c = []
    for hold in (0, 1):
        for pr in (0.30, 0.057):
            sched = [(BENCH["steps_c"], pr if hold == 0 else 0.0, pr if hold == 1 else 0.0)]
            o = stub(Agent10g, [1.0, 0.0], sched, hold=hold); ob = stub(Agent6, [1.0, 0.0], sched, hold=hold); out[f"c{hold}{pr}"] = (o, ob)
            dr = events(o)["drives"]; m = on_hold(dr) & dr["ended"]
            false = np.zeros(n, bool); np.logical_or.at(false, dr["r"][m & (dr["silent"] <= RESET_AFTER)], True)
            leg = np.bincount(dr["r"][m & (dr["silent"] > RESET_AFTER)], minlength=n)
            x = o["W"][:, :, hold]; gaps = [int(np.sum(np.diff(np.flatnonzero(np.r_[True, x[:, i], True])) - 1 >= 41)) for i in range(n)]
            k, pt, lo, hi = interval("P", ~false); lo_c.append(lo)
            say(f"   ({'valued' if hold == 0 else 'neutral'} hold, p {pr}) rows with no false release {k}/{n} = {pt:.3f} [{lo:.3f}, {hi:.3f}] -> {'PASS' if lo >= 0.95 else 'FAIL'};"
                f" legitimate releases (drive after >= 41 silent steps) per row mean {leg.mean():.3f} (rows with any {int((leg > 0).sum())}); feed gaps >= 41 per row mean {np.mean(gaps):.3f}"
                f" (expected {BENCH['steps_c']*pr*(1 - pr)**41:.4f}); holding the fed odour at step {BENCH['steps_c'] - 1}: fix {int((o['H'][-1] == hold).sum())}, base {int((ob['H'][-1] == hold).sum())};"
                f" drive D quartiles {q3(dr['D'][on_hold(dr)]) if on_hold(dr).any() else 'n/a'}")
    # (a) identities
    sp = [(BENCH["steps_b"], p, p)]
    for lab, cls, base in (("Agent10", Agent10, Agent8), ("Agent10g", Agent10g, Agent6)):
        ids[f"a0 release off == base, stub, {lab}"] = bitwise(stub(cls, [1.0, 0.0], sp, release=False), stub(base, [1.0, 0.0], sp))
        ids[f"a0 release off == base, World7, {lab}"] = bitwise(run("T1", cls, (1.0, 0.0), BS, release=False), run("T1", base, (1.0, 0.0), BS))
    sep = {}
    for lab, (o, ob) in out.items(): sep[f"stub {lab}"] = separation(o, ob)
    w = {k: run("T1", c, (1.0, 0.0), BS) for k, c in (("Agent10", Agent10), ("Agent8", Agent8), ("Agent10g", Agent10g), ("Agent6", Agent6))}
    sep["World7 Agent10 vs Agent8"] = separation(w["Agent10"], w["Agent8"]); sep["World7 Agent10g vs Agent6"] = separation(w["Agent10g"], w["Agent6"])
    for k, (ok, cnt) in sep.items(): ids[f"a1 {k}"] = ok
    say("(a0) release=False == the base agent bitwise (every field, counter included): " + "; ".join(f"{k[3:]} {v}" for k, v in ids.items() if k.startswith("a0")))
    say("(a1) identity (b), separation up to the first base timeout firing while a unit is above threshold:")
    for k, (ok, cnt) in sep.items(): say(f"      {k}: {ok} {cnt}")
    wl = {k: run(wd, c, (1.0, 0.0), BS) for wd in ("W1", "T3a", "T3b") for k, c in ((f"{wd} Agent10", Agent10), (f"{wd} Agent8", Agent8), (f"{wd} Agent10g", Agent10g), (f"{wd} Agent6", Agent6))}
    for wd in ("T1", "W1", "T3a", "T3b"):
        a, b = (w["Agent10"], w["Agent8"]) if wd == "T1" else (wl[f"{wd} Agent10"], wl[f"{wd} Agent8"]); ids[f"a2 {wd} Agent10 == Agent8 trajectory"] = traj(a, b)
    ids["a3 W1 Agent10g == Agent6 trajectory"] = traj(wl["W1 Agent10g"], wl["W1 Agent6"])
    say("(a2) Agent10 == Agent8 in trajectory (POS, HEAD, NAV, SINCE, TGT), every row: " + "; ".join(f"{wd} {ids[f'a2 {wd} Agent10 == Agent8 trajectory']}" for wd in ("T1", "W1", "T3a", "T3b"))
        + f" | (a3) Agent10g == Agent6 in trajectory in W1: {ids['a3 W1 Agent10g == Agent6 trajectory']}")
    for wd in ("W1", "T3a", "T3b"):
        for k in ("Agent10", "Agent10g"):
            ok, cnt = separation(wl[f"{wd} {k}"], wl[f"{wd} {'Agent8' if k == 'Agent10' else 'Agent6'}"]); ids[f"a1 {wd} {k}"] = ok
            say(f"      (a1) {wd} {k} vs base: {ok} {cnt}")
    arms3 = [(k, w[k.split()[-1]]) for k in ("T3b Agent10", "T3b Agent8", "T3b Agent10g", "T3b Agent6")]
    ids["a4 T3b draws"] = all(wl[k]["draws_equal"] and wl[k]["rng_equal"] for k, _ in arms3)
    ids["a4 T3b == World7 run on steps 0-149"] = all(bitwise(wl[k], ref, n=T0) for k, ref in arms3) and not any(bitwise(wl[k], ref, n=T0 + 60) for k, ref in arms3)
    t3 = [wl[f"T3a {k}"] for k in ("Agent10", "Agent8", "Agent10g", "Agent6")]
    ids["a4 T3a draws"] = all(o["draws_equal"] and o["rng_equal"] for o in t3)
    ids["a4 T3a start and hold"] = all(np.array_equal(o["start"], o["src"][np.arange(n), o["good"]]) and (o["s0"][np.arange(n), o["good"]] == 2.0).all()
                                       and (o["H0"] == o["good"]).all() for o in t3)
    say(f"(a4) constructions: T3b draws == the World7 twin (both columns before t0, valued False and neutral equal from t0), wind and generator state equal {ids['a4 T3b draws']};"
        f" each arm's T3b run == its World7 run on steps 0-{T0 - 1} (every field) and departs after {ids['a4 T3b == World7 run on steps 0-149']}; T3a draws (valued False from step 0) {ids['a4 T3a draws']};"
        f" T3a start at the valued source with s_valued 2.0 held {ids['a4 T3a start and hold']}")
    # (a5) reproduction on the recorded seeds (no criterion read)
    r6 = run("T1", Agent6, (1.0, 0.0), REPRO["h21"]); r10g = run("T1", Agent10g, (1.0, 0.0), REPRO["h21"])
    r8 = run("T1", Agent8, (1.0, 0.0), REPRO["h23"]); r10 = run("T1", Agent10, (1.0, 0.0), REPRO["h23"])
    c6, c8, c10 = [tuple(int(x.sum()) for x in majority(o)) for o in (r6, r8, r10)]
    ids["a5 H21 maintain 300/96/4"] = c6 == (300, 96, 4); ids["a5 H23 filter 381/14/5"] = c8 == (381, 14, 5)
    ids["a5 Agent10 == Agent8 V row for row"] = bool(np.array_equal(majority(r10)[0], majority(r8)[0]))
    s1 = separation(r10g, r6); s2 = separation(r10, r8); ids["a5 separation Agent10g vs Agent6 (1725/1825)"] = s1[0]; ids["a5 separation Agent10 vs Agent8 (1765/1865)"] = s2[0]
    say(f"(a5) reproduction on the recorded seeds (identity checks, not new evidence): H21 maintain (Agent6) on {REPRO['h21']} V/N/tie {c6} (recorded 300/96/4) {ids['a5 H21 maintain 300/96/4']};"
        f" H23 filter (Agent8) on {REPRO['h23']} {c8} (recorded 381/14/5) {ids['a5 H23 filter 381/14/5']}; Agent10 {c10}, V row for row == Agent8 {ids['a5 Agent10 == Agent8 V row for row']};"
        f" separation Agent10g vs Agent6 {s1}; Agent10 vs Agent8 {s2}")
    # (d) realistic silent gaps
    say(f"(d) realistic silent gaps, World7 task start, bench seeds, {n} x {BENCH['steps']} (reported, not a gate)")
    for base, fixk in (("Agent6", "Agent10g"), ("Agent8", "Agent10")):
        ev = events(w[base]); dr = ev["drives"]; m = on_hold(dr); gen = m & (dr["silent"] >= 41); stale = m & (dr["silent"] < 41)
        nof = n - len(np.unique(dr["r"][m]))
        g, gi = ev["gaps"], ev["gaps_in"]
        say(f"   [{base}] held odour's silent gaps while held: {len(g)} runs, quartiles {q3(g)}, >= 41 {int((g >= 41).sum())} = {(g >= 41).mean():.4f}; between two hits only {len(gi)},"
            f" quartiles {q3(gi)}, >= 41 {(gi >= 41).mean() if len(gi) else float('nan'):.4f}; base timeout firings on a hold {int(m.sum())} (genuine, >= 41 silent steps since the last hit or formation,"
            f" {int(gen.sum())}; stale {int(stale.sum())}); ended the hold {int(dr['ended'][m].sum())}; rows with no firing on a hold {nof}/{n}; holds formed {len(ev['segs'])}")
        drive_summary(w[fixk], fixk, say)
        ok, cnt = sep[f"World7 {fixk} vs {base}"]; say(f"      identity (b) class on these rows: {cnt}")
    # (e) the ph14b protocol
    say(f"(e) the H19 ph14b protocol re-run: World4, seeds {REPRO['h19']}, 200 rows x 2400 steps, neutral; the circuit table 1b (circuit only, untouched) follows")
    ph14b.bench_reset() if say is print else None
    lo_e = []
    for kind, lab in (("Agent4", "the design's agent: Agent4 at G 0, zero values (= Agent3 with H19 (a) ON)"), ("Agent3", "ph14b's own agent: ph14.Agent3 fix=False, learning off")):
        say(f"   [{lab}]")
        ob = chain(kind, False); rb, _ = chain_stats(ob, say, "base")
        of = chain(kind, True); rf, lo = chain_stats(of, say, "fix ")
        rep = rb["silence timeout"][0] == 8652 and rb["evidence release"][0] == 761
        say(f"      base reproduces ph14b 1a (8652 timeout / 761 evidence requests): {rep}  | fix bar: circuit empty at the end of an uninterrupted drive, lower bound {lo:.3f} >= 0.95 -> {'PASS' if lo >= 0.95 else 'FAIL'}")
        lo_e.append(lo); ids[f"e reproduction {kind}"] = rep
    # T3a ceiling and floor on bench seeds; pass probability restated
    c = run("T3a", None, (1.0, 0.0), BS, fixed="neutral"); f = wl["T3a Agent6"]
    Dc, Df = t3_dwell(c, 100, 600), t3_dwell(f, 100, 600); _, sp_, slo, shi = interval("DP", Dc, Df); sd = float(np.std(Dc - Df))
    say(f"   T3a on bench seeds: dwell at the neutral source, steps 100-599: ceiling (Agent5 fixed neutral) mean {Dc.mean():.3f}, floor (Agent6) mean {Df.mean():.3f}; span {sp_:.3f} [{slo:.3f}, {shi:.3f}];"
        f" per-row paired sd {sd:.3f}; M7(b) pass probability at R 0.9 {pass_prob_R(0.9, sd, sp_):.3f}, at R 0.6 {pass_prob_R(0.6, sd, sp_):.3f} (the bar does not move)")
    rep_ok = {k: v for k, v in ids.items() if not k.startswith("e reproduction")}
    bars = dict(b=all(x >= 0.95 for x in lo_b), c=all(x >= 0.95 for x in lo_c), e=all(x >= 0.95 for x in lo_e))
    idok = all(rep_ok.values()); verdict = idok and all(bars.values())
    say(f"== M4: identities (a0-a5) {idok}; failed: {[k for k, v in rep_ok.items() if not v]}; bars (b) {bars['b']} (lower bounds {[round(x, 4) for x in lo_b]}), (c) {bars['c']} ({[round(x, 4) for x in lo_c]}),"
        f" (e) {bars['e']} ({[round(x, 4) for x in lo_e]}); (e) base reproduces ph14b 1a: {[(k[15:], v) for k, v in ids.items() if k.startswith('e reproduction')]} (reported)"
        f" -> M4 {'PASS: the tasks may be run' if verdict else 'FAIL, NO CANDIDATE: the change as specified does not do what section 3 says; the tasks are NOT run'} ==")
    return verdict


# ------------------------------------------------------------------ self-checks
def seeds_unused():
    """design section 9: none of the H25 seeds or derived generators appears in any other file under the repository (recursive, digit-boundary;
    excluded by name: this file, its outputs ph24_*.txt, the H25 documents h25_*.md, master_plan.md, notes/*.md). The reproduction seeds
    1725/1825, 1765/1865 and 9600/9700 are reused on purpose and are NOT part of this check."""
    base = [*SEEDS["dev"], *SEEDS["eval"], BENCH["seed_w"], BENCH["seed_a"], ph15.BOOT_SEED]
    derived = [s + 10_000 for s in (SEEDS["dev"][0], SEEDS["eval"][0], BENCH["seed_w"])] + [s + 20_000 for s in (SEEDS["dev"][1], SEEDS["eval"][1], BENCH["seed_a"])]
    nums = base + derived + [30261031, 40261032]
    pat = re.compile(rb"(?<!\d)(" + "|".join(map(str, nums)).encode() + rb")(?!\d)"); hits = []; nf = 0
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for f in files:
            if f == "ph24.py" or (f.startswith("ph24_") and f.endswith(".txt")) or (f.startswith("h25_") and f.endswith(".md")) or f == "master_plan.md": continue
            if os.path.basename(root) == "notes" and f.endswith(".md"): continue
            nf += 1
            if pat.search(open(os.path.join(root, f), "rb").read()): hits.append(os.path.relpath(os.path.join(root, f), repo))
    return hits, nums, nf


def header(say=print):
    say(f"   ph24.py sha256 {sha()}; design {DESIGN}")
    say("   imported modules: " + "; ".join(f"{os.path.basename(m.__file__)} {sha(m.__file__)}" for m in MODS))
    say(f"   seeds: dev {SEEDS['dev']}, eval {SEEDS['eval']}, bench {BS}, bootstrap {ph15.BOOT_SEED}; reproduction seeds {REPRO} reused on purpose, NOT part of the seed scan")


def demo():
    print(f"== H25 self-checks (demo). design {DESIGN} ==")
    header()
    n, st = 40, 200; kw = dict(runs=n, steps=st); sp = [(st, 0.30, 0.30)]
    for cls, base in ((Agent10, Agent8), (Agent10g, Agent6)):
        assert bitwise(run("T1", cls, (1.0, 0.0), (5, 6), release=False, **kw), run("T1", base, (1.0, 0.0), (5, 6), **kw)), f"{cls.__name__} release off is not {base.__name__}"
        assert bitwise(stub(cls, [1.0, 0.0], sp, release=False, rows=n), stub(base, [1.0, 0.0], sp, rows=n)), f"{cls.__name__} release off (stub) is not {base.__name__}"
    print("ok  release=False: Agent10 == Agent8 and Agent10g == Agent6 bitwise, every field and the counter (World7 and stub, 40 rows x 200 steps)")
    for cls, base in ((Agent10, Agent8), (Agent10g, Agent6)):
        ok, cnt = separation(run("T1", cls, (1.0, 0.0), (5, 6), **kw), run("T1", base, (1.0, 0.0), (5, 6), **kw)); assert ok, f"separation {cls.__name__} {cnt}"
        print(f"ok  identity (b) {cls.__name__} vs {base.__name__}, World7 40 x 200: {cnt}")
    assert traj(run("T1", Agent10, (1.0, 0.0), (5, 6), **kw), run("T1", Agent8, (1.0, 0.0), (5, 6), **kw)), "Agent10 trajectory is not Agent8's"
    print("ok  Agent10 == Agent8 in trajectory at +1/0 (40 x 200)")
    o = stub(Agent10g, [1.0, 0.0], [(100, 0.0, 0.0)], hold=0, rows=n); end = first_true(o["H"] != 0); first = first_true(o["TO"])
    assert (first == 41).all(), f"constructed hold, counter 0: first drive not at step 41 {set(first)}"
    assert not (o["SUS"] & ~(o["S"] > 1.0).any(2)).any() and not (o["SUS"] & ~o["TO"]).any(), "a sustain step with the circuit empty or without a drive"
    ob = stub(Agent6, [1.0, 0.0], [(100, 0.0, 0.0)], hold=0, rows=n)
    print(f"ok  constructed valued hold, no input: first drive at step 41 in every row; sustain only on drive steps with a unit above 1.0. Printed, not asserted (bench (b) measures it):"
          f" hold ends at step {q3(end[end >= 0])} (never {int((end < 0).sum())}), both units <= 1.0 at step 99 in {int((o['S'][-1] <= 1.0).all(1).sum())}/{n}; the base keeps it in {int((ob['H'][-1] == 0).sum())}/{n}")
    sched = [(30, 0.0, 0.0), (1, 1.0, 0.0), (99, 0.0, 0.0)]; z = stub(Agent10g, [1.0, 0.0], sched, rows=n); zb = stub(Agent6, [1.0, 0.0], sched, rows=n)
    ez, eb = events(z), events(zb); fz = first_true(z["Z"])
    assert z["Z"].any() and not (z["Z"] & ~ez["form"]).any(), "(Z) lowered the counter on a step that is not a hold formation"
    fd = lambda ev: ev["drives"]["t"][on_hold(ev["drives"])]
    print(f"ok  (Z) acts only on formation steps: a whiff at step 30 after 30 silent steps; counter zeroed at step {q3(fz[fz >= 0])} (rows {int((fz >= 0).sum())});"
          f" first drive on a hold at step {q3(fd(ez))} (base's first firing on a hold {q3(fd(eb))})")
    for kind in ("Agent3", "Agent4"):
        a = chain(kind, False, runs=20, steps=200)
        w = World4(20, np.random.default_rng(9600)); b = Agent3(20, np.random.default_rng(9700), fix=False, abl=("learn",)) if kind == "Agent3" else Agent4(20, np.random.default_rng(9700), G=0.0, known=np.zeros((20, 2)))
        H = []
        for t in range(200): turn, h = b.act(w, w.sense(), w.wind_on()); w.move(turn); b.bump(w.bumped); H.append(h)
        assert np.array_equal(np.array(H), a["H"]), f"bench (e) {kind} release off is not the base"
    print("ok  bench (e) agents with release off (Agent3x spy, Agent4R) reproduce ph14.Agent3 fix=False and ph16.Agent4 G 0 (20 rows x 200 steps, held odour)")
    t3a = run("T3a", Agent10g, (1.0, 0.0), (5, 6), **kw)
    assert t3a["draws_equal"] and t3a["rng_equal"] and (t3a["H0"] == t3a["good"]).all() and np.array_equal(t3a["start"], t3a["src"][np.arange(n), t3a["good"]])
    t3b = run("T3b", Agent10g, (1.0, 0.0), (5, 6), **kw); t1 = run("T1", Agent10g, (1.0, 0.0), (5, 6), **kw)
    assert t3b["draws_equal"] and t3b["rng_equal"] and bitwise(t3b, t1, n=T0) and not bitwise(t3b, t1, n=st)
    c = run("T3b", None, (1.0, 0.0), (5, 6), fixed="valued-then-neutral", **kw)
    assert (c["H"][:T0] == c["good"]).all() and (c["H"][T0:] == 1 - c["good"]).all()
    print("ok  T3a (mask from step 0, start at the valued source, valued hold) and T3b (mask from t0, == T1 before t0) constructions; T3b ceiling switches its fixed odour at t0")
    hits, nums, nf = seeds_unused(); assert not hits, f"a seed of this run appears in {hits}"
    print(f"ok  seeds {nums} appear in no other file under the repository ({nf} files scanned; excluded by name ph24.py, ph24_*.txt, h25_*.md, master_plan.md, notes/*.md)")


# ------------------------------------------------------------------ the task (design sections 5-8)
T1ARMS = {"filter-fix": (Agent10, (1.0, 0.0), G_STAR, True, True, None), "filter": (Agent8, (1.0, 0.0), G_STAR, True, True, None),
          "maintain-fix": (Agent10g, (1.0, 0.0), G_STAR, True, False, None), "maintain": (Agent6, (1.0, 0.0), G_STAR, True, False, None),
          "pathway-off": (Agent8, (1.0, 0.0), 0.0, False, False, None), "known-answer": (None, (1.0, 0.0), 0.0, False, False, "valued"),
          "neutral": (Agent10, (0.0, 0.0), G_STAR, True, True, None)}
T2ARMS = {"filter-fix": Agent10, "filter": Agent8, "maintain-fix": Agent10g, "maintain": Agent6}
T3ARMS = {"maintain-fix": (Agent10g, None), "maintain": (Agent6, None), "filter-fix": (Agent10, None), "filter": (Agent8, None)}


def arm(world, name, seeds):
    if world == "T1":
        cls, vals, G, gate, filt, fixed = T1ARMS[name]; return run("T1", cls, vals, seeds, G=G, gate=gate, filt=filt, fixed=fixed)
    if world == "W1": return run("W1", T2ARMS[name], (1.0, 0.0), seeds)
    if name == "ceiling": return run(world, None, (1.0, 0.0), seeds, fixed="neutral" if world == "T3a" else "valued-then-neutral")
    return run(world, T3ARMS[name][0], (1.0, 0.0), seeds)


def main(mode):
    seeds = SEEDS[mode]; rows = np.arange(R); ok = lambda z: "PASS" if z else "FAIL"
    print(f"== H25, {mode.upper()}. design {DESIGN}; G {G_STAR}, gate on where G 2; world seed {seeds[0]}, agent seed {seeds[1]}; {R} rows x {T} steps; geometry C0; t0 {T0};"
          f" bootstrap seed {ph15.BOOT_SEED}; {'operation check only' if mode == 'dev' else 'the one evaluation'} ==")
    header()
    print("   rows share no state: one generator per world and one per agent population, fixed-size draws consumed in row order every step")
    t1 = {a: arm("T1", a, seeds) for a in T1ARMS}; t2 = {a: arm("W1", a, seeds) for a in T2ARMS}
    t3a = {a: arm("T3a", a, seeds) for a in list(T3ARMS) + ["ceiling"]}; t3b = {a: arm("T3b", a, seeds) for a in list(T3ARMS) + ["ceiling"]}
    maj = {a: majority(t1[a]) for a in T1ARMS}
    print("\n== T1, the H21 choice task ==")
    for a in T1ARMS:
        describe_majority(a, t1[a], *maj[a]); h21_diag(a, t1[a])
        if a in ("filter-fix", "maintain-fix", "filter", "maintain", "neutral"): drive_summary(t1[a], a, print)
    print("\n== T2, the absent-odour world W1 (valued source silenced from step 0) ==")
    for a in T2ARMS:
        d = t3_dwell(t2[a], 0, T); print(f"   [W1 {a}] dwell at the neutral (present) source mean {d.mean():.3f}, quartiles {q3f(d)}; rows reaching it {int((d > 0).sum())}; draws == twin {t2[a]['draws_equal'] and t2[a]['rng_equal']}")
        drive_summary(t2[a], f"W1 {a}", print)
    print("\n== T3a, lost at the valued source (constructed: valued column masked from step 0, start at the valued source, valued hold s 2.0) ==")
    D = {a: t3_dwell(t3a[a], 100, T) for a in t3a}
    for a in t3a:
        o = t3a[a]; line = f"   [T3a {a}] dwell at the neutral source, steps 100-599: mean {D[a].mean():.3f}, quartiles {q3f(D[a])}, rows > 0 {int((D[a] > 0).sum())}"
        if a != "ceiling":
            okr, end = t3a_release(o); hn = first_true(o["H"] == 1 - o["good"][None, :])
            line += (f"; valued hold ended at step quartiles {q3(end[end >= 0])} (never {int((end < 0).sum())}), exact (<= 49, circuit empty) {int(okr.sum())}/{R};"
                     f" neutral first held at step {q3(hn[hn >= 0])} (rows {int((hn >= 0).sum())}); first within 3.0 of the neutral source {q3(first_true(o['AT2'][:, rows, 1 - o['good']])[first_true(o['AT2'][:, rows, 1 - o['good']]) >= 0])}")
        print(line)
        if a != "ceiling": drive_summary(o, f"T3a {a}", print)
    print("\n== T3b, sensed then lost (ph23.Lost, valued column masked from t0 150; reported) ==")
    Db = {a: t3_dwell(t3b[a], 400, T) for a in t3b}
    for a in t3b:
        line = f"   [T3b {a}] dwell at the neutral source, steps 400-599: mean {Db[a].mean():.3f}, quartiles {q3f(Db[a])}"
        if a != "ceiling":
            hold, end, rel = t3b_release(t3b[a]); m = hold & (end >= 0)
            line += (f"; holding the valued odour at t0 {int(hold.sum())}/{R}; its hold ended in {int(m.sum())} (never {int((hold & (end < 0)).sum())}), step after t0 quartiles {q3(end[m] - T0)},"
                     f" relative to the counter's origin quartiles {q3(rel[m])}, <= +49 {int((rel[m] <= 49).sum())}/{int(m.sum())}")
        print(line)
    # ------------------------------------------------ criteria (design v2 section 7)
    print("\n== criteria (design v2 FINAL section 7; 95 percent, one evaluation, no extension; aggregation: PASS if every part passes, FAIL if any fails, else INCONCLUSIVE) ==")
    m1 = []
    for a in ("pathway-off", "known-answer"):
        z = maj[a][2]; m1.append(ok(z.mean() <= 0.20)); print(f"   M1(a) {a}: ties {z.sum()}/{R} = {z.mean():.3f}  at most 0.20 -> {m1[-1]}")
    print(f"      reported: neutral ties {maj['neutral'][2].sum()}/{R}")
    o = t1["neutral"]; V, N, Z = maj["neutral"]; which = np.where(V, o["good"], np.where(N, 1 - o["good"], -1))
    m1.append(crit("M1(b) neutral, P(+y source majority | chose)", "P", (0.35, 0.65), False, (which == o["plus_y"])[~Z]))
    V, N, Z = maj["pathway-off"]; m1.append(crit("M1(c) floor: pathway-off, P(V | chose)", "P", (0.35, 0.65), False, V[~Z]))
    m1.append(crit("M1(d) ceiling: known-answer, P(V) over all rows", "P", 0.85, False, maj["known-answer"][0]))
    M1 = agg(m1); print(f"   M1 -> {M1}{'' if M1 == 'PASS' else '  (the run is UNREADABLE under section 8)'}")
    Vf, Vb = maj["filter-fix"][0], maj["filter"][0]
    m2a = traj(t1["filter-fix"], t1["filter"]); print(f"   M2(a) Agent10 trajectory == Agent8's on every row (POS, HEAD, NAV, SINCE, TGT): {m2a} -> {ok(m2a)}")
    m2 = [ok(m2a), crit("M2(b) Agent10 (filter-fix), P(V) over all rows", "P", 0.88, False, Vf)]
    M2 = agg(m2); print(f"   M2 -> {M2}")
    _, pt, lo, hi = interval("DP", Vf.astype(float), Vb.astype(float)); nwf = ~t1["filter-fix"]["W"][-T//3:].any((0, 2)); nwb = ~t1["filter"]["W"][-T//3:].any((0, 2))
    print(f"      reported: DP Agent10 - Agent8 {pt:+.3f} [{lo:+.3f}, {hi:+.3f}]; lost rows (no whiff of either plume in the last third) {int(nwf.sum())} vs {int(nwb.sum())}, equal row for row"
          f" {bool(np.array_equal(nwf, nwb))}; wall contacts {int(t1['filter-fix']['contacts'].sum())} vs {int(t1['filter']['contacts'].sum())}, equal row for row"
          f" {bool(np.array_equal(t1['filter-fix']['contacts'], t1['filter']['contacts']))}")
    # M3
    i = {}
    for wd, runs_ in (("T1", t1), ("W1", t2), ("T3a", t3a), ("T3b", t3b)):
        for fx, bs in (("filter-fix", "filter"), ("maintain-fix", "maintain")):
            ok_, cnt = separation(runs_[fx], runs_[bs]); i[f"(a1) {wd} {fx} vs {bs}"] = ok_; print(f"      M3 (a1) {wd} {fx} vs {bs}: {ok_} {cnt}")
        i[f"(a2) {wd} Agent10 == Agent8 trajectory"] = traj(runs_["filter-fix"], runs_["filter"])
    i["(a3) W1 Agent10g == Agent6 trajectory"] = traj(t2["maintain-fix"], t2["maintain"])
    i["T2 draws"] = all(t2[a]["draws_equal"] and t2[a]["rng_equal"] for a in t2)
    i["T3a draws, start, hold"] = all(t3a[a]["draws_equal"] and t3a[a]["rng_equal"] and np.array_equal(t3a[a]["start"], t3a[a]["src"][rows, t3a[a]["good"]]) for a in t3a) \
        and all((t3a[a]["H0"] == t3a[a]["good"]).all() for a in T3ARMS)
    i["T3b draws"] = all(t3b[a]["draws_equal"] and t3b[a]["rng_equal"] for a in t3b)
    i["T3b == T1 before t0"] = all(bitwise(t3b[a], t1[a], n=T0) for a in T3ARMS) and bitwise(t3b["ceiling"], t1["known-answer"], n=T0)
    M3 = agg([ok(v) for v in i.values()])
    print("   M3 identities: " + "; ".join(f"{k} {v}" for k, v in i.items()) + f" -> {M3}")
    # M4
    print("   M4 mechanism bench, re-run here with the bench seeds (section 4); its lines:")
    lines = []; m4 = bench(say=lines.append)
    for ln in lines:
        if ln.startswith("== M4") or ln.startswith("   (b") or ln.startswith("   (valued") or ln.startswith("   (neutral") or "fix bar" in ln: print("      " + ln.strip())
    M4 = ok(m4); print(f"   M4 -> {M4}")
    # M5
    m5a = bool(np.array_equal(t3_dwell(t2["filter-fix"], 0, T), t3_dwell(t2["filter"], 0, T))); m5b = bool(np.array_equal(t3_dwell(t2["maintain-fix"], 0, T), t3_dwell(t2["maintain"], 0, T)))
    M5 = agg([ok(m5a), ok(m5b)])
    print(f"   M5(a) W1 Agent10 dwell == Agent8's row for row {m5a}; M5(b) W1 Agent10g dwell == Agent6's row for row {m5b} -> {M5}"
          f"   (means: Agent10 {t3_dwell(t2['filter-fix'], 0, T).mean():.3f}, Agent8 {t3_dwell(t2['filter'], 0, T).mean():.3f}, Agent10g {t3_dwell(t2['maintain-fix'], 0, T).mean():.3f}, Agent6 {t3_dwell(t2['maintain'], 0, T).mean():.3f})")
    # M6 reported
    Vg, V6 = maj["maintain-fix"][0], maj["maintain"][0]; _, pt, lo, hi = interval("DP", Vg.astype(float), V6.astype(float))
    lg = ~t1["maintain-fix"]["W"][-T//3:].any((0, 2)); l6 = ~t1["maintain"]["W"][-T//3:].any((0, 2))
    _, lpt, llo, lhi = interval("DP", lg.astype(float), l6.astype(float)); _, cpt, clo, chi = interval("DP", t1["maintain-fix"]["contacts"], t1["maintain"]["contacts"])
    cg, c6 = np.select(list(maj["maintain-fix"]), [0, 1, 2]), np.select(list(maj["maintain"]), [0, 1, 2])
    print(f"   M6 (REPORTED, no bar; not part of the PASS condition): DP = P(V) Agent10g - Agent6 {pt:+.4f} [{lo:+.4f}, {hi:+.4f}] (P(V) {Vg.mean():.3f} vs {V6.mean():.3f}; predicted [-0.18, 0], centre -0.05);"
          f" into V {int(((cg == 0) & (c6 != 0)).sum())}, out of V {int(((cg != 0) & (c6 == 0)).sum())}; lost rows {int(lg.sum())} vs {int(l6.sum())}, DP {lpt:+.4f} [{llo:+.4f}, {lhi:+.4f}];"
          f" contacts per row {t1['maintain-fix']['contacts'].mean():.3f} vs {t1['maintain']['contacts'].mean():.3f}, DP {cpt:+.4f} [{clo:+.4f}, {chi:+.4f}]")
    # M7
    m7 = []
    for a in ("maintain-fix", "filter-fix"):
        okr, end = t3a_release(t3a[a]); m7.append(crit(f"M7(a) T3a {a} ({'Agent10g' if a == 'maintain-fix' else 'Agent10'}): valued hold ends at a step <= 49 with both units <= 1.0, rows exact", "P", 0.95, False, okr))
    Dg, Df, Dc = D["maintain-fix"], D["maintain"], D["ceiling"]
    _, spn, slo, shi = interval("DP", Dc, Df); readable = slo >= 5.0
    Rp, Rlo, Rhi = ratio_boot(Dg, Df, Dc)
    print(f"   M7(b) readability: span D_ceiling - D_floor = {Dc.mean():.3f} - {Df.mean():.3f} = {spn:.3f} [{slo:.3f}, {shi:.3f}], lower bound >= 5.0 -> {'readable' if readable else 'UNREADABLE'}")
    m7b = ("PASS" if Rlo >= 0.5 else "FAIL" if Rhi < 0.5 else "INCONCLUSIVE") if readable else "UNREADABLE"
    print(f"   M7(b) R = (D_Agent10g - D_floor) / (D_ceiling - D_floor) = ({Dg.mean():.3f} - {Df.mean():.3f}) / {spn:.3f} = {Rp:.4f} [{Rlo:.4f}, {Rhi:.4f}] (bootstrap 5000, rows resampled together, seed {ph15.BOOT_SEED});"
          f" at least 0.50 -> {m7b}")
    m7.append(m7b); M7 = agg(m7); print(f"   M7 -> {M7}")
    # M8 reported
    _, a1, a1l, a1h = interval("DP", Db["maintain-fix"], Db["maintain"]); _, a2, a2l, a2h = interval("DP", Db["maintain-fix"], Db["ceiling"])
    print(f"   M8 T3b (REPORTED): neutral dwell 400-599 Agent10g {Db['maintain-fix'].mean():.3f}, Agent6 {Db['maintain'].mean():.3f}, Agent10 {Db['filter-fix'].mean():.3f}, Agent8 {Db['filter'].mean():.3f},"
          f" ceiling {Db['ceiling'].mean():.3f}; Agent10g - Agent6 {a1:+.3f} [{a1l:+.3f}, {a1h:+.3f}]; Agent10g - ceiling {a2:+.3f} [{a2l:+.3f}, {a2h:+.3f}]")
    unread = M1 != "PASS" or m7b == "UNREADABLE"
    parts = (M2, M3, M4, M5, M7); verdict = M1 == "PASS" and all(x == "PASS" for x in parts)
    lab = "SHOWN" if verdict else "UNREADABLE" if unread else agg(list(parts)).replace("FAIL", "NOT shown")
    print(f"\n== H25 ==  M1 {M1}  M2 {M2}  M3 {M3}  M4 {M4}  M5 {M5}  M7 {M7}  (M6, M8 reported) -> "
          + ("H25 SHOWN under its registered criteria: the sustained drive ends a hold whose odour is silent for more than RESET_AFTER steps, leaves the circuit empty and ends no recently"
             " whiffed hold, and with it the gate agent tracks the remaining neutral odour after the valued odour is lost, recovering at least half of the ceiling-floor span; in the adopted"
             " agent the change is behaviour-inert at +1/0" if verdict else f"H25 {lab} under its registered criteria"))


if __name__ == "__main__":
    mode = ([m for m in sys.argv[1:] if m in ("demo", "bench", "dev", "eval")] or ["demo"])[0]
    if mode == "demo": demo(); sys.exit(0)
    if mode == "bench": sys.exit(0 if bench() else 1)
    main(mode)
