#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H12 Stage 2: the behavioural stage. Agent17 with learning on in W7X (reward withdrawn at 600, V masked 2400-3599, reinstated
3600-4199, a supplied competitor at +0.5), the H12 module (MB5, tau_ext* 5000) against the adopted module (gate only).

Usage: python ph36b.py demo | bench | dev | eval     (stdout, LF line ends; redirected to experiments/h12/ph36b_<mode>.txt)

Design: H12 design v2 FINAL, doc d27ec95924fe49be1, sha256 3d3aab80...95f1 (experiments/h12/h12_design_v2.md), section 5.5 (the
Stage 2 registration, written before any run), opened by decision:h12-open (owner, 2026-09-26, '권고안으로 확정하고 H12 진행', gloss
'confirm as recommended and proceed with H12'). Stage 1 PASSED (record:h12-bench-result; tau_ext* = 5000). The composition was
signed before this file existed (decision:h12-stage2-composition, H14 format): the agent is Agent17 built unchanged through ph35's
hook (ph24.make with Agent17 inside ph28.pn(60, 200); src/ph35.py:111-118), and this harness replaces the instance attribute `a.mb`
(built at src/ph11.py:115) by MB5(parallel True, gated True, tau (None, None, 5000, 5000), **ph11.MB) from src/ph36.py, before the
off-world training and the cast draw. No adopted file is edited: ph36.py (sha256 on record), ph29.py, ph35.py and every adopted module
are imported unchanged and hash-checked at run time.

Readings where the design is silent, chosen so that the identities stay exact (printed again in every output header):
 (R1) The harness is ph24.run's loop (ph24.py:113-149) for the T3b world (ph23.Lost with the valued column masked while `on`, the
      unmasked World7 twin checking the draws), with `on` = 2400 <= t < 3600, plus: the per-step value write (the mirror in the
      learning arms, the supplied schedule otherwise) after the step's sense and wind draws and before act (ph30.py reading R1); the
      module step after the move (ph15.simulate's order); and the records below. The record hook chain ph24.record (ph29 -> ph25 ->
      ph24) is called unchanged; ph29's frozen-module check stays inert because no agent carries its training marker.
 (R2) Construction order: world, mask, twin, placeholder values (V +1, N c), agent (ph24.make inside ph28.pn(60, 200)), module
      replaced (H12: MB5; H11 full: ph8.MB4(parallel True)), off-world training (ph29.train, trained or sham group, neutral-first as
      Stage B), the step-0 values written, the cast draw (ph16.cast_draw(agent seed)). The module's generator is the agent's own
      module generator (never drawn from); codes are the agent's own (a.codes, ph11.py:116).
 (R3) 'Every recorded field' (I5, the supplied-trajectory identities, K2(c), H11 full): ph28.ALLK (ph24's fields + SIL, TO, EV, W,
      NAV6, NAV8, DIFF, DIFF8, PRES) plus P2, C2 (ph25's record), AT2, C (contacts) and KV (the V value written on the step), compared
      per (step, row). (I5) on steps 0..FU inclusive per row, FU = the row's first step at V's source without reinforcement in the H12
      arm (the module update of step FU happens after that step's record); rows with none: every step.
 (R4) Dwell majority per block: V dwell > N dwell (ph18.majority's rule on the block); ties = equal dwell (both 0 included).
 (R5) Crossing rows: KV < c on some step of P2 (600-2399). Time to leave: the first t in 600..2399 with V outside the top set on each
      of the steps t..t+199 (top set recomputed from the recorded presence P2 and the written values: V present, v_V >= 0 and
      v_V >= the value of every present odour); -1 if none. Time to re-form: first step at V's source at or after 3600, minus 3600;
      and the first 100-step sub-block of P4 with V dwell > N dwell (index 0-5); -1 if none.
 (R6) Value trajectories at 599, 1199, ..., 4199 after the step's update: on V's code, the behavioural valence, out0 - out1,
      out2 - out3, out1 and out0 (mb.out, ph4.py:37-39); learning-off arms print none.
 (R7) bar_B = 0.5 x (P4 P(V) ceiling - P4 P(V) floor) on the bench, rounded to 0.01 half up, computed exactly from the counts
      (floor(dk / 8 + 1/2) / 100 with dk the difference of the two V counts over 400 rows).
 (R8) (hS): ph28.pp_dp(DP, b, bar_B, most=False) (sd = sqrt(b - DP^2), se = sd / 20, Phi((DP - bar_B)/se - 1.96); sd 0: the point).
 (R9) K1: ph15.boot('DP', H12 P4 V indicator, gate-only P4 V indicator), 95 percent, 5000 resamples, seed 20261153 (set through
      ph30.set_stats after every import), ph15.verdict 'at least' bar_B.
 (R10) K2(c): the ceiling arm is run a second time with the H12 module constructed (learning off) and compared on every recorded
      field; the module call count is 0 in every learning-off arm.
 (R11) Arms run in parallel processes (fork); each builds its own world and agent generators from the seed pair; the two
      supplied-trajectory arms run after the learning arms whose written values they replay. The demo checks parallel == sequential.
 (R12) dev and eval refuse to run while BARS['K1'] is unset; the bench prints the K1 reference numbers and (hS) and runs no task seed.
 (R13) Seed scan: ph36.seeds_unused() (ph36's reading R13; ph36b.py and ph36b_*.txt are excluded by name there). The demo's smoke
      seeds (5, 6) are unregistered and are used for smoke checks only.
Nothing changes after the table.
"""
import sys, os, math, hashlib, copy
from fractions import Fraction
import multiprocessing as mp
import numpy as np
import ph35                                      # Agent17 and its ph24.make hook (imports ph34b, ph28, ph30 unchanged)
import ph29                                      # Stage B's off-world training (its hooks are inert without a training mode)
import ph36                                      # MB5 (Stage 1), its seed scan
import ph4, ph8, ph11, ph15, ph16, ph22, ph23, ph24, ph25, ph28, ph30
from ph35 import Agent17, N17
from ph36 import MB5
from ph8 import MB4
from ph16 import World7, cast_draw
from ph21 import G_STAR
from ph28 import ALLK, P_PRIOR, pp_dp

sys.stdout.reconfigure(newline="\n")            # LF output, so the recorded sha256 equals the committed blob
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
DESIGN = ph36.DESIGN
PH36_SHA = "b83bd9e9d1bd9b191d771779b1cd907d9eb057797105c05e82acb15d2a99ca71"             # record:h12-bench-result, decision:h12-stage2-composition
SHA_ON_RECORD = dict(ph29="122c19250ea5d67d0dbd997fa20493c63c6c1101faff83d3cc6b3e907d4c799c", ph30="98822834043de5f31615e73cd4a83444adcef2f1d5e56478356d70ca905059bd",
                     ph35="e4a3ceda25628e7026a64861ad51f84974f1e2a720794276df706d006a52b1b1", ph4="d009568cda4dba358f1857268e21a105ad8eac10add665b40792c1c82238646a",
                     ph8="ada2fc4b38c9d0083d083667ae3fbeb615f544b45f80199ec5b2bc86e6d3b43e", ph11="e80f40bd710aca43252f04329846ffa29943251d19e718450e9a7ff49e947a23")
TAU = 5000                                       # tau_ext*, fixed at the Stage 1 bench (record:h12-bench-result)
C = 0.5                                          # the supplied competitor (design 5.1)
R, T = 400, 4200
P1, P2E, P3E, P4E = 600, 2400, 3600, 4200        # phase ends: P1 0-599, P2 600-2399, P3 2400-3599, P4 3600-4199
BLK = 600; NB = T // BLK
SEEDS = dict(bench=(20261151, 20261152), dev=(9911, 9921), eval=(2129, 2243))
BOOT = 20261153
BARS = dict(K1=None)                             # bar_B, fixed after the bench by decision:h12-k1-bar (design 5.5)
NPROC = int(os.environ.get("PH36B_PROCS", "4"))
KEYS = ALLK + ("P2", "C2", "AT2", "C", "KV")
ph30.set_stats(ph30.Z95, ph30.QLO95, ph30.QHI95, BOOT)   # 95 percent, bootstrap 20261153 (after every import set its own)

#          module, training, learning, V source reinforces in P1/P4, values
ARMS = {"H12": ("P", "trained", True, True, "mirror"),
        "gate only": ("A0", "trained", True, True, "mirror"),
        "H11 full": ("A1", "trained", True, True, "mirror"),
        "ceiling": ("A0", None, False, False, "ceiling"),
        "floor": ("A0", None, False, False, "floor"),
        "sham": ("P", "sham", True, False, "mirror"),
        "ceiling (H12 module)": ("P", None, False, False, "ceiling"),
        "supplied H12 trajectory": ("A0", None, False, False, "traj"),
        "supplied gate-only trajectory": ("A0", None, False, False, "traj")}
FIRST = ("H12", "gate only", "H11 full", "ceiling", "floor", "sham", "ceiling (H12 module)")


def sha(p=__file__): return hashlib.sha256(open(p, "rb").read()).hexdigest()


# ------------------------------------------------------------------ one run (design 5.5; readings R1, R2)
def run(arm, seeds, runs=R, steps=T, traj=None, c=C, mask=(P2E, P3E), mbf=None):
    mod, trn, learn, reinf, vals = ARMS[arm]
    w = ph23.Lost(runs, np.random.default_rng(seeds[0]), seeds[0]); g = w.good; rows = np.arange(runs); nu = 1 - g
    w.pres = nu.copy(); w.absent = g.copy()
    tw = World7(runs, np.random.default_rng(seeds[0]), seeds[0])
    kv = np.zeros((runs, 2)); kv[rows, g] = 1.0; kv[rows, nu] = c                                  # placeholder (the constructor does not read it)
    rng = np.random.default_rng(seeds[1])
    with ph28.pn(P_PRIOR, N17): a = ph24.make(Agent17, runs, rng, G_STAR, kv, True, True, True)
    assert type(a) is Agent17 and a.N_hi == N17
    if mod == "P": a.mb = MB5(runs, parallel=True, gated=True, tau=(None, None, TAU, TAU), rng=a.mb.rng, **ph11.MB)
    elif mod == "A1": a.mb = MB4(runs, parallel=True, gated=True, rng=a.mb.rng, **ph11.MB)
    if mbf is not None: a.mb = mbf(runs, a.mb.rng)                                                   # demo check 4 only
    v_train = ph29.train(a, g, trn) if trn else None
    codeV = a.codes[rows, g]
    def values(t):
        k = np.zeros((runs, 2)); k[rows, nu] = c
        if vals == "mirror": k[rows, g] = a.mb.valence(codeV)
        elif vals == "ceiling": k[rows, g] = 1.0
        elif vals == "floor": k[rows, g] = 1.0 if t < P1 else c - 0.05
        else: k[rows, g] = traj[t]
        return k
    a.known = values(0)
    a.cast_sign = cast_draw(seeds[1], runs)
    o = dict(arm=arm, good=g, cell=w.cell, steps=steps, draws_equal=True, v_train=v_train, calls=0, **ph24.blank(steps, runs),
             POS=np.zeros((steps, runs, 2)), HEAD=np.zeros((steps, runs)), AT2=np.zeros((steps, runs, 2), bool), C=np.zeros((steps, runs), bool),
             KV=np.zeros((steps, runs)), VT={}, FU=np.full(runs, -1), unreinf=np.zeros(runs, int))
    for t in range(steps):
        w.on = mask[0] <= t < mask[1]
        tw.pos, tw.head = w.pos.copy(), w.head.copy()
        pa = (a.sel.s > 1.0).any(1)
        x = w.sense(); on = w.wind_on()
        tr = tw.sense(); ton = tw.wind_on()
        o["draws_equal"] &= bool(np.array_equal(tr, w.raw) and np.array_equal(on, ton) and np.array_equal(x[rows, nu], tr[rows, nu])
                                 and np.array_equal(x[rows, g], np.zeros(runs, bool) if w.on else tr[rows, g]))
        a.known = values(t)                                                                            # R1: before act
        o["KV"][t] = a.known[rows, g]
        turn, h = a.act(w, x, on)
        ph24.record(o, t, a, h, x, pa)
        w.move(turn); a.bump(w.bumped)
        at = w.at_source()
        o["POS"][t] = w.pos; o["HEAD"][t] = w.head; o["AT2"][t] = at; o["C"][t] = w.bumped
        if learn:
            atV = at[rows, g]; rv = np.zeros((runs, a.mb.C))
            reinforced = reinf and (t < P1 or t >= P3E)
            if reinforced: rv[:, 1] = atV
            nr = atV & ~reinforced
            o["FU"] = np.where((o["FU"] < 0) & nr, t, o["FU"]); o["unreinf"] += nr
            a.mb.step(code=codeV*atV[:, None], reinf=rv); o["calls"] += 1
            if (t + 1) % BLK == 0:
                oo = a.mb.out(codeV)
                o["VT"][t] = dict(v=a.mb.valence(codeV), acq=oo[:, 0] - oo[:, 1], par=oo[:, 2] - oo[:, 3], out1=oo[:, 1], out0=oo[:, 0])
    o["rng_equal"] = w.rng.bit_generator.state == tw.rng.bit_generator.state
    o["mb_calls_attr"] = o["calls"]
    return o


def run_job(job):
    arm, seeds, kw = job
    return run(arm, seeds, **kw)


# ------------------------------------------------------------------ measures (design 5.5; readings R4, R5)
def dwell(o):
    r = np.arange(len(o["good"])); g = o["good"]; at = o["AT2"]
    dv = at[:, r, g].reshape(NB, BLK, -1).sum(1); dn = at[:, r, 1 - g].reshape(NB, BLK, -1).sum(1)
    return dv, dn                                                                                      # (NB, rows)


def p4v(o): dv, dn = dwell(o); return dv[-1] > dn[-1]


def block_table(o):
    dv, dn = dwell(o); n = dv.shape[1]
    return [(float((dv[b] > dn[b]).mean()), float((dn[b] > dv[b]).mean()), float((dv[b] == dn[b]).mean()), float(dv[b].mean()), float(dn[b].mean()),
             float(np.median(dv[b])), float(np.median(dn[b]))) for b in range(NB)]


def top_v(o):
    r = np.arange(len(o["good"])); g = o["good"]; P = o["P2"]; v = o["KV"]
    presV, presN = P[:, r, g], P[:, r, 1 - g]
    return presV & (v >= 0) & (~presN | (v >= C))


def time_to_leave(o, win=200):
    out = ~top_v(o); st, n = out.shape
    cs = np.vstack([np.zeros((1, n), int), np.cumsum(out, 0)])
    full = (cs[win:] - cs[:-win]) == win                                                              # full[t]: steps t..t+win-1 all outside
    res = np.full(n, -1)
    for t in range(P1, P2E):
        if t + win > st: break
        res = np.where((res < 0) & full[t], t, res)
    return res


def reform(o):
    r = np.arange(len(o["good"])); g = o["good"]; at = o["AT2"]
    a4 = at[P3E:, r, g]; first = np.where(a4.any(0), a4.argmax(0), -1)
    sv = a4.reshape(6, 100, -1).sum(1); sn = at[P3E:, r, 1 - g].reshape(6, 100, -1).sum(1); maj = sv > sn
    sub = np.where(maj.any(0), maj.argmax(0), -1)
    return first, sub


def crossing(o): return (o["KV"][P1:P2E] < C).any(0)


def med_q(x, f=".3f"):
    x = np.asarray(x, float)
    if len(x) == 0: return "n/a"
    return f"{np.median(x):{f}} [{np.percentile(x, 25):{f}}, {np.percentile(x, 75):{f}}]"


def roweq(o1, o2, cut=None, keys=KEYS):
    """per-row equality over steps 0..cut[row] inclusive (cut < 0: every step)"""
    st, n = o1["H"].shape; eq = np.ones((st, n), bool)
    for k in keys:
        e = o1[k] == o2[k]; eq &= e.reshape(st, n, -1).all(2)
    if cut is None: return eq.all(0)
    tt = np.arange(st)[:, None]; lim = np.where(cut < 0, st, cut + 1)[None, :]
    return (eq | (tt >= lim)).all(0)


def first_dep(o1, o2, keys=KEYS):
    st, n = o1["H"].shape; eq = np.ones((st, n), bool)
    for k in keys:
        e = o1[k] == o2[k]; eq &= e.reshape(st, n, -1).all(2)
    bad = ~eq; return np.where(bad.any(0), bad.argmax(0), -1)


def describe(name, o, say):
    tb = block_table(o); n = len(o["good"])
    say(f"\n   [{name}] draws_equal {o['draws_equal']}, rng_equal {o['rng_equal']}, module calls {o['calls']}")
    say("      block  P(V)   P(N)   ties   mean dwell V/N   median dwell V/N")
    for b, (pv, pn, pz, mv, mn, qv, qn) in enumerate(tb):
        ph = "P1" if b == 0 else "P2" if b <= 3 else "P3" if b <= 5 else "P4"
        say(f"      b{b} {ph}  {pv:.3f}  {pn:.3f}  {pz:.3f}   {mv:6.2f} / {mn:6.2f}    {qv:5.1f} / {qn:5.1f}")
    ARM = ARMS[name]
    if ARM[4] == "mirror":
        cr = crossing(o); tl = time_to_leave(o); f, s = reform(o)
        say(f"      crossing rows (V below c in P2): {int(cr.sum())}/{n}; unreadable rows (never below c in P2): {int((~cr).sum())}")
        say(f"      time to leave (first t in P2 with V outside the top set for 200 steps): rows {int((tl >= 0).sum())}, median t {med_q(tl[tl >= 0], '.0f')}")
        say(f"      time to re-form: first arrival at V after 3600 in {int((f >= 0).sum())} rows, median {med_q(f[f >= 0], '.0f')} steps; first 100-step P4 sub-block with V majority in {int((s >= 0).sum())} rows, median index {med_q(s[s >= 0], '.0f')}")
        say(f"      P3 contacts at V's source: {int(o['AT2'][P2E:P3E, np.arange(n), o['good']].sum())} steps in {int(o['AT2'][P2E:P3E, np.arange(n), o['good']].any(0).sum())} rows;"
            f" unreinforced at-source steps over the run: {int(o['unreinf'].sum())}; rows with one: {int((o['FU'] >= 0).sum())}")
        say(f"      V value written at step 0: min {o['KV'][0].min():.6f} max {o['KV'][0].max():.6f}; at 2400 (start of P3): {med_q(o['KV'][P2E])}")
        say("      value trajectory on V's code (median [quartiles]; after the step's update):")
        for t, d in sorted(o["VT"].items()):
            say(f"        t {t:4d}: v {med_q(d['v'])}  acq out0-out1 {med_q(d['acq'])}  parallel out2-out3 {med_q(d['par'])}  out1 {med_q(d['out1'])}  out0 {med_q(d['out0'])}")
    else:
        f, s = reform(o)
        say(f"      time to re-form: first arrival at V after 3600 in {int((f >= 0).sum())} rows, median {med_q(f[f >= 0], '.0f')}; P4 sub-block with V majority in {int((s >= 0).sum())} rows")


# ------------------------------------------------------------------ header and readings
def header(say=print):
    say(f"   ph36b.py sha256 {sha()}; design {DESIGN}; tau_ext* {TAU} (record:h12-bench-result); composition decision:h12-stage2-composition")
    mods = (ph4, ph8, ph11, ph15, ph16, ph22, ph23, ph24, ph25, ph28, ph29, ph30, ph35, ph36)
    say("   imported: " + "; ".join(f"{os.path.basename(m.__file__)} {sha(m.__file__)}" for m in mods))
    ok = {k: sha(os.path.join(HERE, k + ".py")) == v for k, v in SHA_ON_RECORD.items()}
    p36 = sha(ph36.__file__) == PH36_SHA; dz = sha(ph36.DESIGN_FILE) == DESIGN.split("hash ")[1]
    say(f"   sha256 equal to the record: ph36.py {p36}; {ok}; design file {dz}")
    say(f"   seeds: bench {SEEDS['bench']}, dev {SEEDS['dev']}, eval {SEEDS['eval']}; derived world + 10000, agent + 20000; bootstrap {ph15.BOOT_SEED} (95 percent, Z {ph15.Z});"
        f" c {C}; {R} rows x {T} steps; phases P1 0-599, P2 600-2399, P3 2400-3599 (V masked), P4 3600-4199; BARS {BARS}")
    return p36 and all(ok.values()) and dz


def readings(say=print):
    doc = __doc__; i = doc.index("Readings where"); j = doc.index("Nothing changes after the table.")
    for line in doc[i:j].rstrip().splitlines(): say("   " + line)


def pool(): return mp.get_context("fork").Pool(NPROC)


def run_all(seeds, say):
    with pool() as p: res = dict(zip(FIRST, p.map(run_job, [(a, seeds, {}) for a in FIRST])))
    jobs = [("supplied H12 trajectory", seeds, dict(traj=res["H12"]["KV"])), ("supplied gate-only trajectory", seeds, dict(traj=res["gate only"]["KV"]))]
    with pool() as p: res.update(dict(zip([j[0] for j in jobs], p.map(run_job, jobs))))
    return res


def checks(res, say):
    """identities (design 5.5): I5, K2(c), supplied trajectories, H11 full, learning arms == ceiling before FU, sham exactly 0"""
    H, G = res["H12"], res["gate only"]; n = len(H["good"])
    i5 = roweq(H, G, cut=H["FU"]); I5 = bool(i5.all())
    say(f"   (I5) H12 == gate only on every recorded field on steps 0..FU per row: {int(i5.sum())}/{n} rows -> {I5}; FU equal in the two arms: {bool(np.array_equal(H['FU'], G['FU']))}")
    k2c = bool(roweq(res["ceiling"], res["ceiling (H12 module)"]).all())
    calls0 = all(res[a]["calls"] == 0 for a in ARMS if not ARMS[a][2])
    say(f"   K2(c) ceiling with the H12 module == ceiling with the adopted module, every field, every step: {k2c}; module calls 0 in every learning-off arm: {calls0}")
    st1 = bool(roweq(res["supplied H12 trajectory"], H).all()); st2 = bool(roweq(res["supplied gate-only trajectory"], G).all())
    say(f"   supplied trajectories == their learning arms on every field and step: H12 {st1}, gate only {st2}")
    h11 = roweq(res["H11 full"], G); fd = first_dep(res["H11 full"], G); dep = fd >= 0
    mxv = float(np.abs(res["H11 full"]["KV"] - G["KV"]).max())
    rr = np.where(dep)[0]; atd = np.abs(res["H11 full"]["KV"][fd[rr], rr] - G["KV"][fd[rr], rr]) if dep.any() else np.zeros(0)
    say(f"   H11 full == gate only on every field and step: {int(h11.sum())}/{n} rows; departing rows {int(dep.sum())}"
        + (f" (first departures at steps {sorted(fd[dep].tolist())[:10]}...; |V value difference| at the departure: max {atd.max():.3e})" if dep.any() else "")
        + f"; max |V value difference| over the run {mxv:.3e} (reported, not in the verdict)")
    pre = [bool(roweq(res[a], res["ceiling"], cut=H["FU"], keys=tuple(k for k in KEYS)).all()) for a in ("H12", "gate only")]
    say(f"   learning arms == ceiling on every field before and at FU (V exactly 1.0 until the first unreinforced step): H12 {pre[0]}, gate only {pre[1]}")
    sham0 = bool((res["sham"]["KV"] == 0.0).all())
    say(f"   sham: V exactly 0.0 on every step and row: {sham0}; sham module calls {res['sham']['calls']}")
    draws = all(o["draws_equal"] and o["rng_equal"] for o in res.values())
    say(f"   every arm: the mask consumed no draw (draws_equal, rng_equal): {draws}")
    return dict(I5=I5, K2c=k2c and calls0, st=st1 and st2, draws=draws, sham0=sham0)


def pair_stats(res):
    vh, vg = p4v(res["H12"]).astype(float), p4v(res["gate only"]).astype(float)
    dp = float(vh.mean() - vg.mean()); b = float((vh != vg).mean())
    return vh, vg, dp, b


def bar_rule(kc, kf):
    """reading R7: 0.5 x (kc - kf) / 400 rounded to 0.01 half up, exactly"""
    x = Fraction(kc - kf, 2*R)*100
    return math.floor(x + Fraction(1, 2))/100.0


# ------------------------------------------------------------------ the bench (design 5.5)
def bench(say=print):
    seeds = SEEDS["bench"]
    say(f"== H12 Stage 2 bench (design v2 FINAL section 5.5). design {DESIGN}; world seed {seeds[0]}, agent seed {seeds[1]} ==")
    hok = header(say); readings(say)
    hits, nums, nf = ph36.seeds_unused()
    say(f"   seed scan: {len(nums)} numbers, {nf} files, hits: {hits if hits else 'none'}")
    if not hok or hits: say("   STOP: a hash check or the seed scan failed"); return
    res = run_all(seeds, say)
    for a in ARMS: describe(a, res[a], say)
    say("\n== identities and checks ==")
    ck = checks(res, say)
    n = R
    kc, kf = int(p4v(res["ceiling"]).sum()), int(p4v(res["floor"]).sum())
    span = (kc - kf)/n
    ties = {a: float(block_table(res[a])[-1][2]) for a in ARMS}
    cr = int(crossing(res["gate only"]).sum())
    say("\n== K0 readability and the unreadable conditions (design 5.5) ==")
    say(f"   P4 P(V): ceiling {kc}/{n} = {kc/n:.4f}, floor {kf}/{n} = {kf/n:.4f}; ceiling - floor = {span:+.4f} (>= 0.30 required)")
    say("   P4 ties per arm: " + "; ".join(f"{a} {v:.3f}" for a, v in ties.items()) + " (each <= 0.20 required)")
    say(f"   crossing rows in the gate-only arm: {cr} (>= 50 required); (I5) {ck['I5']}")
    K0 = span >= 0.30 and all(v <= 0.20 for v in ties.values())
    unread = (not K0) or cr < 50 or not ck["I5"]
    say(f"   K0 -> {'READABLE' if K0 else 'UNREADABLE'}; unreadable conditions: {'none' if not unread else 'HOLD'}")
    bar = bar_rule(kc, kf)
    vh, vg, dp, b = pair_stats(res)
    say(f"\n== the K1 reference numbers (design 5.5; the bar is fixed by decision:h12-k1-bar, not here) ==")
    say(f"   bar_B = 0.5 x (ceiling - floor) = 0.5 x ({kc} - {kf})/{n} = {0.5*span:.5f} -> rounded to 0.01 half up: {bar:.2f}")
    say(f"   bench paired DP P4 P(V), H12 - gate only: {dp:+.4f} (H12 {int(vh.sum())}/{n}, gate only {int(vg.sum())}/{n}); discordant fraction b {b:.4f};"
        f" into V {int(((vh == 1) & (vg == 0)).sum())}, out of V {int(((vh == 0) & (vg == 1)).sum())}")
    v1 = p4v(res["H11 full"]).astype(float)
    say(f"   reported beside it: H11 full - gate only paired DP P4 P(V) {float(v1.mean() - vg.mean()):+.4f} (the same valence in real arithmetic; the size of the last-bit divergence between the two layouts)")
    if unread:
        say("   STOP: Stage 2 UNREADABLE at the bench as designed (K0 or an unreadable condition); redesigned, not retuned; (hS) not computed"); return
    pp = pp_dp(dp, b, bar=bar, most=False)
    say(f"   (hS) pass probability of K1 at the bench (reading R8): {pp:.4f} (STOP below 0.5) -> {'continue' if pp >= 0.5 else 'STOP'}")


def judge_run(mode, say=print):
    seeds = SEEDS[mode]
    if BARS["K1"] is None: sys.exit("BARS['K1'] is unset: decision:h12-k1-bar must fix it first (reading R12)")
    say(f"== H12 Stage 2, {mode.upper()} ({'operation errors only' if mode == 'dev' else 'the one evaluation'}). design {DESIGN}; world seed {seeds[0]}, agent seed {seeds[1]}; bar_B {BARS['K1']} ==")
    hok = header(say); readings(say)
    hits, nums, nf = ph36.seeds_unused()
    say(f"   seed scan: {len(nums)} numbers, {nf} files, hits: {hits if hits else 'none'}")
    if not hok or hits: say("   STOP: a hash check or the seed scan failed"); return
    res = run_all(seeds, say)
    for a in ARMS: describe(a, res[a], say)
    say("\n== identities and checks ==")
    ck = checks(res, say)
    n = R
    kc, kf = int(p4v(res["ceiling"]).sum()), int(p4v(res["floor"]).sum())
    ties = {a: float(block_table(res[a])[-1][2]) for a in ARMS}
    cr = int(crossing(res["gate only"]).sum())
    say("\n== unreadable conditions (design 5.5) ==")
    say(f"   P4 P(V) ceiling {kc/n:.4f}, floor {kf/n:.4f} (span {(kc - kf)/n:+.4f}, reported; K0 was read at the bench)")
    say("   P4 ties per arm: " + "; ".join(f"{a} {v:.3f}" for a, v in ties.items()))
    say(f"   crossing rows in the gate-only arm: {cr}; (I5) {ck['I5']}")
    unread = any(v > 0.20 for v in ties.values()) or cr < 50 or not ck["I5"]
    vh, vg, dp, b = pair_stats(res)
    _, lo, hi = ph15.boot("DP", vh, vg)
    k1 = ph15.verdict(lo, hi, BARS["K1"], False)
    say("\n== K1, K2 (design 5.5) ==")
    say(f"   K1 paired DP P4 P(V), H12 - gate only: {dp:+.4f} 95% interval [{lo:+.4f}, {hi:+.4f}] (H12 {int(vh.sum())}/{n}, gate only {int(vg.sum())}/{n};"
        f" into V {int(((vh == 1) & (vg == 0)).sum())}, out of V {int(((vh == 0) & (vg == 1)).sum())}); at least {BARS['K1']} -> {k1}")
    v1 = p4v(res["H11 full"]).astype(float); _, l1, h1 = ph15.boot("DP", v1, vg)
    say(f"   reported beside it: H11 full - gate only paired DP P4 P(V) {float(v1.mean() - vg.mean()):+.4f} [{l1:+.4f}, {h1:+.4f}] (the same valence in real arithmetic; the last-bit divergence between the two layouts)")
    k2 = "PASS" if (ck["I5"] and ck["K2c"]) else "FAIL"
    say(f"   K2 (a) (I4) True (record:h12-bench-result, experiments/h12/ph36_bench.txt); (b) (I5) {ck['I5']}; (c) {ck['K2c']} -> {k2}")
    if mode == "dev":
        say("\n   development run: operation errors only; no criterion is judged on these seeds"); return
    if unread: verdict = "UNREADABLE"
    elif k1 == "PASS" and k2 == "PASS": verdict = "SHOWN"
    elif k1 == "FAIL": verdict = "NOT SHOWN"
    elif k1 == "INCONCLUSIVE": verdict = "INCONCLUSIVE"
    else: verdict = "NOT SHOWN (K2 FAIL)"
    say(f"\n   Stage 1 PASS (record:h12-bench-result); Stage 2: K0 READABLE (bench), unreadable conditions {'HOLD' if unread else 'none'}, K1 {k1}, K2 {k2}")
    say(f"   H12 VERDICT: {verdict}")


# ------------------------------------------------------------------ demo (smoke seeds 5, 6 only)
def demo(say=print):
    say(f"== H12 Stage 2 demo self-checks. design {DESIGN} ==")
    say("   smoke runs on the unregistered seeds (5, 6) only; no registered seed is used and no number here is read for any criterion")
    hok = header(say); assert hok, "a hash check failed"; say("ok 1  ph36.py, ph29.py, ph30.py, ph35.py, ph4.py, ph8.py, ph11.py sha256 and the design file hash equal the record")
    hits, nums, nf = ph36.seeds_unused(); assert not hits, hits; say(f"ok 2  seed scan clean ({len(nums)} numbers, {nf} files)")
    sd, n = (5, 6), 40
    o = run("ceiling", sd, runs=n, steps=600, c=0.0)
    ref = ph35.run("T1", Agent17, (1.0, 0.0), sd, runs=n, steps=600)
    same = all(np.array_equal(o[k], ref[k]) for k in ALLK + ("P2", "C2", "AT2", "C"))
    assert same, [k for k in ALLK + ("P2", "C2", "AT2", "C") if not np.array_equal(o[k], ref[k])]
    say("ok 3  the harness with supplied +1/0 and the mask off (600 steps) == ph35.run('T1', Agent17, (1, 0)) on every recorded field: the adopted agent and world, bitwise")
    a = run("gate only", sd, runs=n, steps=1800)
    o2 = run("gate only", sd, runs=n, steps=1800, mbf=lambda runs, rng: MB5(runs, parallel=False, gated=True, rng=rng, **ph11.MB))
    assert bool(roweq(a, o2).all())
    say("ok 4  replacing the module by MB5 with every tau None and parallel False (== ph8.MB4) leaves the learning arm bitwise unchanged (1800 steps)")
    assert np.all(a["KV"][0] == 1.0) and np.all(a["v_train"][np.arange(n), a["good"]] == 1.0)
    say("ok 5  pre-acquisition off-world (ph29.train): V's value exactly 1.0 at step 0 in every row")
    res = {k: run(k, sd, runs=n) for k in FIRST}
    res["supplied H12 trajectory"] = run("supplied H12 trajectory", sd, runs=n, traj=res["H12"]["KV"])
    res["supplied gate-only trajectory"] = run("supplied gate-only trajectory", sd, runs=n, traj=res["gate only"]["KV"])
    ck = checks(res, say)
    assert ck["I5"] and ck["K2c"] and ck["st"] and ck["draws"] and ck["sham0"]
    say("ok 6  (I5), K2(c), the supplied-trajectory identities, the draw checks and the sham's exact 0 hold on the smoke seeds (40 rows x 4200 steps)")
    assert (res["H12"]["unreinf"] >= 0).all() and res["H12"]["calls"] == T and res["ceiling"]["calls"] == 0
    tl = time_to_leave(res["gate only"]); f, s = reform(res["H12"])
    say(f"ok 7  the measures compute (smoke, not read): crossing rows {int(crossing(res['gate only']).sum())}, leave rows {int((tl >= 0).sum())}, re-form rows {int((f >= 0).sum())}; learning calls {res['H12']['calls']} == steps")
    with pool() as p: par = p.map(run_job, [("H12", sd, dict(runs=n, steps=1200))])[0]
    seq = run("H12", sd, runs=n, steps=1200)
    assert bool(roweq(par, seq).all())
    say("ok 8  a run in a worker process == the same run sequentially, bitwise (reading R11)")
    assert bar_rule(300, 100) == 0.25 and bar_rule(301, 100) == 0.25 and bar_rule(302, 100) == 0.25 and bar_rule(303, 100) == 0.25 and bar_rule(304, 100) == 0.26
    say("ok 9  the bar rule rounds 0.5 x (kc - kf)/400 to 0.01 half up exactly (reading R7)")
    say("ok    all demo self-checks passed")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "demo"
    if mode == "demo": demo()
    elif mode == "bench": bench()
    elif mode in ("dev", "eval"): judge_run(mode)
    else: sys.exit("usage: python ph36b.py demo | bench | dev | eval")
