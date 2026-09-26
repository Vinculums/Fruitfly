#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H28: a burst-ranked value tie (Agent16 = Agent15 + Act16) discounting a ubiquitous, never-reinforced odour D (value 0, p_D 0.03).

Usage: python ph33.py demo | bench | dev | eval

Design: H28 design v2 FINAL, doc da2c1c079a1766d3e, sha256 b12137f6...6b8c (experiments/h28/h28_design_v2.md), opened by
decision:h28-open (owner, 2026-09-26, '권고안으로 진행하고 다음작업 설계 진행', gloss 'proceed with the recommended options, then
proceed with the next work's design': every recommended option of design v1 section 12 confirmed). Signed before this file existed,
H14 format, H28 only: decision:classification-rule-relaxed-burst-record-h28 (per odour the step of its second most recent whiff and of
its last burst, read only to rank odours tied at the top value), decision:evidence-release-composition-rule-h28 (the H27 composition
rule re-signed in form) and decision:classification-rule-relaxed-presence-prior-h28 (the H27 three-counter presence relaxation re-signed
in form).

Composition only; NO adopted file is edited and ph32.py is NOT edited. ph32 (Agent15, Act15, Circuit3, evidence_due, the harness's
recording, the D generator rule, the measures) and every module ph32 imports are imported unchanged; ph32.py's sha256 is checked at run
time against d9f585d5599ea9a4f218e87bd884fa8246a826be0111f495cfbec299a9222743 (the version H27 ran) and ph23, ph24, ph28, ph30 against
the prefixes ph32 records. Agent16 = (ReleaseN2, Agent14, Act16) with Act16(Act15): Act16.act repeats ph32.Act15.act (ph32.py:158-203)
term for term with three changes only (design 3.2): (A) the burst record updated together with the presence counter (after
ph32.py:182); (B) the ranked top set in place of ph32.py:188; (C) keep in place of ph32.py:190. nav, the cast clock, the target, the
flee, the circuit, gain, gate, evidence release and the release wrapper are unchanged. Method order: Agent16, ReleaseN2, Agent14,
Release, Act16, Act15, Agent9, ...; ReleaseN2's `super(Release, self).act` reaches Act16.act (checked in the demo). The constructor
repeats Agent15's (ph32.py:210-218) and adds the burst record.

Readings where the design is silent, chosen so that the identities stay exact (printed again in every output header):
 (R1) As H27 (ph32 readings R1-R3, imported unchanged): the D stream u < p_D from default_rng(world seed + 30000) in every arm (p_D 0
      when off); Circuit3's third unit on default_rng(agent seed + 30000); the evidence release against the strongest non-held channel.
 (R2) The burst record's step index t is the agent's own act count (0 on the first act after construction). The most recent whiff of k
      before step t is read from the presence counter before its update (w1_k = t - 1 - c_k if c_k <= t - 1, else 'never': the counter
      is steps since k was last sensed, and a never-sensed odour has c_k = 240 + t > t - 1); so the stored state is exactly the signed
      pair: w2_k (the second most recent whiff) and b_k (the last burst). On step t: burst_k = whiff_k and t - w2_k <= 9; b_k <- t where
      burst_k; then w2_k <- w1_k where whiff_k. 'never' is -1e9. No random number is drawn. The record is updated in the counter's
      branch (scope 'prior'; every Agent16 arm uses it).
 (R3) The ranked top set reads b after this step's update (a burst completed on this step counts on this step). T = present & v >= 0 &
      v == v_max (ph32.py:188 as is); if T holds two or more odours: the odours of T whose b equals the largest b over T, and none if that
      largest b is 'never' (several odours bursting on the same step all stay); if T holds one odour or none: T.
 (R4) keep = hh >= 0 & (the ranked top set holds hh, or v_hh < 0), hh the read hold (the circuit's hold; the read argmax in the
      hold-not-read arm, H27 reading R4, ph32.py:173-174 unchanged). Agent15's own top set and keep (ph32.py:188, :190) are computed on the
      same state and kept for measurement only (TOP, KEEP15, NAV15), as is ACT = (ranked top set != T on any odour) | (keep != keep15):
      'the rule acts'.
 (R5) Fields: 'trajectory' and 'every field' as H27 reading R5 (ph32.TRAJ, ph32.EVERY; HR added where both arms carry it). Agent16's
      measurement fields (TOP, TOPR, KEEP15, KEEP, NAV15, ACT, BURST, BB, BW2) are not in any comparison with Agent15 or Agent14N2.
 (R6) (I2') per row on every step before the row's first D whiff (H27 R6, ph32.i2_rows). (I5') population: T1 rows with V present by its
      counter on every step of the Agent16 D-off run (H27 R7). (I6'): per row, Agent16 D on == Agent15 D on on every field (EVERY + HR)
      on every step strictly before the row's first ACT step (all steps if none); rows with an action and the first action step printed.
 (R7) (m) three definitions side by side on the T1 Agent16 D-off run: H27's (V absent by its counter on some step, reading R7), H26's
      at-risk (ph28.at_risk, from step 59; the literal from step 0 beside it) and the literal prior-expiry count (no V whiff on 0-58).
      (w) W1 rows with no B whiff on steps 0-58, printed for the Agent16 D-off and D-on runs (identical before 59).
 (R8) (e) Entry points: a nav event is D-driven when its steering set is {D} alone (the held odour's whiff if keep, else the whiffing
      odours of the ranked top set; ph32b reading D2). Classes, exclusive: E2 keep with D read as held; E1 not keep, T of two or more,
      nothing held; E1b not keep, T of two or more, a non-kept odour held; E3 not keep, T of one odour (D the lone top odour); E4 a
      D-driven nav in a tie in which no odour of T has burst (checked 0). E5 the same classes in the hold-not-read arm (hh = the read
      argmax). Agent15 D on, the floor, classified with its own unranked T. N1 (the rule's cost path): on Agent16 D-on's own state, steps
      on which Agent15's law (NAV15) steers on a V or B whiff and Agent16 does not steer; literal counts across runs are not defined
      after the runs diverge, so N1 is counted on the run's own state (a reading).
 (R9) Pass probabilities (design section 7): a paired DP with b the discordant fraction, sd = sqrt(b - DP^2), se = sd / 20 (ph28.pp_dp),
      lower-bound bar for M2(b), M2(c), upper-bound bar (most=True) for M5(a'). (h) STOP if M2(b)'s < 0.5; (hW) STOP if M5(a')'s < 0.5.
 (R10) H27's W1D bars, REPORTED only: (a) reach Wilson lower bound >= 0.80; (b) paired dwell Agent16 D on - D off against bar_W = -0.20 x
      the bench's Agent16 D-off mean W1 dwell rounded to 0.1 (H27 reading R12); (c) contacts per row <= 0.10; (d) lost-row DP D on - D off
      upper bound <= +0.05.
 (R11) M1's arms are H26's, two channels, no D (H27 reading R14: Agent14N2 at 0/0, ph24.Agent8 at G 0 gate off filter off, ph17.Agent5
      with the valued odour fixed). The filter-off arm is H27's Agent15g (Agent15, filt False); the release-off arm is Agent16 with release
      False; the hold-not-read arm is Agent16 with hold_read False.
 (R12) Bench (b): Still stub (ph32.stub's construction, Agent16), 400 rows, the same uniform draws for every schedule; the brute force
      from the recorded whiffs: burst on t iff whiff on t and at least two whiffs on t-9..t-1; b the last burst step at or before t; w2 the
      second most recent whiff step at or before t. Independence: in the two-channel schedule each channel's record equals its record in
      the one-channel schedule with the same draws. (c): constructed states through the act (every combination of whiffs 2^3, held
      none/V/B/D, V, B and D each present or absent, burst order none/B only/D only/B more recent/D more recent; x2), expected values
      by a per-row Python loop written separately from the vectorised act; H27's (b3), (c) re-run on the new seeds (Agent15), and (d)
      on the T1D Agent16 run.
 (R13) dev and eval re-run the bench on the bench seeds for M4 (H27 reading R16) and print whether its M4 line equals ph33_bench.txt's.
 (R14) Arms run in parallel processes (fork), each building its own generators from the seeds; the demo checks a parallel result equals
      a sequential one bitwise, and this harness's Agent15 and Agent14N2 equal ph32.run's bitwise.
Seed scan (design section 9): every file under the repository except by name ph33.py, ph33_*.txt, h28_*.md, master_plan.md,
notes/*.md, viewer/*, and the (file, number) pair of decision:seed-scan-exclusion-ph31-eval (experiments/h20/ph31_eval.txt with Stage C
Run 1's E1 evaluation agent seed, taken from ph30's seed constants through ph32, not written here). Nothing changes after the table.
"""
import sys, os, re, math, hashlib
import multiprocessing as mp
import numpy as np
import ph32                                              # Agent15 (H27); imports ph30, ph28 and every adopted module unchanged
import ph2, ph11, ph14, ph15, ph16, ph17, ph22, ph23, ph24, ph25, ph28, ph30
from ph32 import (Act15, Circuit3, blank, record, cone_of, rowmask, same, traj, TRAJ, EVERY, wv, wb, wd, w1sum, lost_t1, cls3, binom_ge,
                  t3_dwell, v_absent, i2_rows, pair_dp, qq, P_D, P_PRIOR, N_HI, PR, D_OFF, A3_OFF)
from ph2 import Upstream
from ph9 import UPWIND, CAST_PERIOD, MAXOFF, GAIN, MAXTURN, TURN_NOISE, angdiff
from ph11 import RESET_AFTER
from ph12 import SAT
from ph16 import World7, Still, cast_draw, interval, crit, R, T
from ph18 import agg
from ph21 import G_STAR, q3, first_true
from ph23 import pass_prob
from ph24 import Release
from ph28 import Agent14, pp_dp, Phi
from ph30 import ReleaseN2, Agent14N2

sys.stdout.reconfigure(newline="\n")            # LF output, so the recorded sha256 equals the committed blob
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
DESIGN = "H28 v2 FINAL doc da2c1c079a1766d3e hash b12137f684fb44d80f5a780fccfd1dc0f63669b5530d2a3eaf834b8df0316b8c"
PH32_SHA = "d9f585d5599ea9a4f218e87bd884fa8246a826be0111f495cfbec299a9222743"
SEEDS = dict(dev=(9907, 9917), eval=(2093, 2197))
BENCH = dict(rows=400, steps=600, seed_w=20261131, seed_a=20261132, boot=20261133)
BS = (BENCH["seed_w"], BENCH["seed_a"])
ph30.set_stats(ph30.Z95, ph30.QLO95, ph30.QHI95, BENCH["boot"])      # design section 7: 95 percent, bootstrap 20261133 (after ph32 set its own)
NEVER = -1.0e9
WIN = 9                                          # a burst: three whiffs within 10 consecutive steps t-9..t (design 3.2 (A))
MODS = ph32.MODS + (ph32,)
NPROC = int(os.environ.get("PH33_PROCS", "4"))
BENCH_TXT = os.path.join(REPO, "experiments", "h28", "ph33_bench.txt")


def sha(p=__file__): return hashlib.sha256(open(p, "rb").read()).hexdigest()


# ------------------------------------------------------------------ the change (design 3.2)
class Act16(Act15):
    """ph32.Act15.act (ph32.py:158-203) with (A) the burst record, (B) the ranked top set, (C) keep (readings R2-R4)"""

    def act(self, w, whiffs, wind_on):
        rows = np.arange(self.R)
        y = self.up.step(whiffs.astype(float))*(1.0 + self.G*np.maximum(self.chan_valence(), 0.0))   # H20: the gain
        hp = self.held()
        if self.rule:                                                                                 # H21: the gate
            v = self.chan_valence(); vh = v[rows, np.maximum(hp, 0)]
            y = y*~((hp >= 0)[:, None] & (v >= 0.0) & (v < vh[:, None]))
        self.yp = y
        self.due_timeout = self.silence > RESET_AFTER
        self.due_evidence = ph32.evidence_due(y, hp)                                                 # H27: the composition rule
        due = self.due_timeout | self.due_evidence
        rst = np.where(due, 10.0, 0.0)[:, None]
        self.silence = np.where(due, 0.0, self.silence)
        self.sel.step(y, reset=rst)
        h = self.held()
        self.hr = np.where(y.max(1) > 0.05, y.argmax(1), -1)                                          # H27 reading R4
        hh = h if self.hold_read else self.hr
        est = self.est = self.estimate(w, wind_on)
        val = np.where(hh >= 0, self.known[rows, np.maximum(hh, 0)], 0.0)
        hit = np.where(hh >= 0, whiffs[rows, np.maximum(hh, 0)], False)
        v = self.chan_valence(); vh = v[rows, np.maximum(hh, 0)]
        top8 = (v >= 0) & (v == v.max(1)[:, None])
        self.nav8 = np.where((hh >= 0) & ((vh == v.max(1)) | (vh < 0)), hit, (whiffs & top8).any(1))
        if self.scope == "prior":
            cp = self.c
            self.c = np.where(whiffs, 0.0, self.c + 1.0)
            t = float(self.t16)                                                                       # H28 (A): the burst record (R2)
            w1 = np.where(cp <= t - 1.0, t - 1.0 - cp, NEVER)
            self.burst = whiffs & ((t - self.w2) <= WIN)
            self.bb = np.where(self.burst, t, self.bb)
            self.w2 = np.where(whiffs, w1, self.w2)
            held = np.zeros_like(whiffs); held[rows, np.maximum(hh, 0)] = hh >= 0
            self.present = (self.c < self.N) | held
        else:
            self.present = np.ones_like(whiffs)
        vmax = np.where(self.present, v, -np.inf).max(1)
        top = self.present & (v >= 0) & (v == vmax[:, None])                                         # ph32.py:188 (Agent15's T)
        nT = top.sum(1); bT = np.where(top, self.bb, -np.inf).max(1)                                  # H28 (B): the ranked top set (R3)
        ranked = top & (self.bb == bT[:, None]) & (bT > NEVER)[:, None]
        topr = np.where((nT >= 2)[:, None], ranked, top)
        self.nav6 = hit | ((hh < 0) & (whiffs & (v >= 0)).any(1))
        keep15 = (hh >= 0) & ((vh == vmax) | (vh < 0))                                                # ph32.py:190 (measurement)
        keep = (hh >= 0) & (topr[rows, np.maximum(hh, 0)] | (vh < 0))                                 # H28 (C): keep (R4)
        nav = np.where(keep, hit, (whiffs & topr).any(1)) if self.filt else self.nav6
        self.top15, self.topr, self.keep15, self.keep16 = top, topr, keep15, keep
        self.nav15 = np.where(keep15, hit, (whiffs & top).any(1)); self.acts = (topr != top).any(1) | (keep != keep15)
        self.differs = nav != self.nav6; self.differs8 = nav != self.nav8
        self.nav_hit = nav; self.val = val
        self.since = np.where(nav, 0.0, self.since + 1.0)
        self.silence = np.where(hit, 0.0, self.silence + 1.0)
        side = np.where((self.since // CAST_PERIOD) % 2 == 0, 1.0, -1.0)*self.cast_sign
        off = MAXOFF*(1.0 - np.abs((self.since/SAT) % 2.0 - 1.0))
        tgt = np.where(nav, UPWIND, (UPWIND + side*off) % 360.0)
        self.tgt = tgt = np.where(val < 0, self.flee_side, tgt)
        turn = np.clip(GAIN*angdiff(tgt, est), -MAXTURN, MAXTURN)
        turn = turn + TURN_NOISE*self.rng.standard_normal(self.R)
        self.last_turn = turn
        self.t16 += 1
        return turn, h


class Agent16(ReleaseN2, Agent14, Act16):
    """Agent15 (ph32.py:206-218) with Act16 where Act15 sits; the constructor repeats Agent15's and adds the burst record"""

    def __init__(self, runs, rng, rng3=None, nch=3, hold_read=True, **kw):
        super().__init__(runs, rng, **kw)
        self.nch, self.hold_read = nch, hold_read; self.hr = np.full(runs, -1); self.val = np.zeros(runs)
        if nch == 3:
            self.up = Upstream(n=1.5, sig=0.05, Rmax=1.8, k=0.8, runs=runs, chans=3)                  # ph11.py:112 with chans 3
            self.sel = Circuit3(runs, rng3=rng3, n=3, theta=1.0, k=12.0, noise=0.01, rng=rng)         # ph11.py:113 with n 3
            self.codes = np.concatenate([self.codes, self.mb.odour(103)[:, None, :]], 1)              # ph11.py:116 plus odour(103)
            self.c = np.full((runs, 3), float(self.N_hi - self.P))                                     # ph28.py:97 with 3 columns
            self.present = np.ones((runs, 3), bool); self.yp = np.zeros((runs, 3))
        self.t16 = 0; self.w2 = np.full((runs, nch), NEVER); self.bb = np.full((runs, nch), NEVER)   # H28: the burst record, 'never'
        self.burst = np.zeros((runs, nch), bool); self.top15 = self.topr = np.zeros((runs, nch), bool)
        self.keep15 = self.keep16 = self.nav15 = self.acts = np.zeros(runs, bool)


# ------------------------------------------------------------------ arms (design section 6)
ARMS = {"Agent16 D on": ("A16", 3, True), "Agent16 D off": ("A16", 3, False), "Agent15 D on": ("A15", 3, True), "Agent15 D off": ("A15", 3, False),
        "Agent14N2": ("A14N2", 2, False), "Agent16 at N 2": ("A16n2", 2, False), "Agent15g D on": ("A15g", 3, True),
        "hold-not-read D on": ("A16hnr", 3, True), "hold-not-read D off": ("A16hnr", 3, False), "release-off D on": ("A16ro", 3, True),
        "pathway-off": ("A8po", 2, False), "known-answer": ("A5ka", 2, False), "neutral": ("A14N2", 2, False), "neutral D on": ("A16", 3, True)}
A16KINDS = ("A16", "A16n2", "A16hnr", "A16ro")


def build(kind, runs, seed_a, g, kv):
    if kind not in A16KINDS: return ph32.build(kind, runs, seed_a, g, kv)
    rng = np.random.default_rng(seed_a); rng3 = np.random.default_rng(seed_a + A3_OFF)
    kw = dict(P=P_PRIOR, N_hi=N_HI, G=G_STAR, known=kv, rule=True, filt=True, scope="prior", release=kind != "A16ro")
    return Agent16(runs, rng, rng3=rng3, nch=2 if kind == "A16n2" else 3, hold_read=kind != "A16hnr", **kw)


def blank16(steps, runs, nch):
    o = blank(steps, runs, nch)
    o.update(TOP=np.zeros((steps, runs, nch), bool), TOPR=np.zeros((steps, runs, nch), bool), BURST=np.zeros((steps, runs, nch), bool),
             BB=np.full((steps, runs, nch), NEVER, np.float32), BW2=np.full((steps, runs, nch), NEVER, np.float32),
             KEEP15=np.zeros((steps, runs), bool), KEEP=np.zeros((steps, runs), bool), NAV15=np.zeros((steps, runs), bool), ACT=np.zeros((steps, runs), bool))
    return o


def record16(o, t, a):
    if isinstance(a, Agent16):
        o["TOP"][t] = a.top15; o["TOPR"][t] = a.topr; o["BURST"][t] = a.burst; o["BB"][t] = a.bb; o["BW2"][t] = a.w2
        o["KEEP15"][t] = a.keep15; o["KEEP"][t] = a.keep16; o["NAV15"][t] = a.nav15; o["ACT"][t] = a.acts


def run(world, arm, vals, seeds, runs=R, steps=T):
    """ph32.run (ph32.py:283-312) with this file's build and Agent16's measurement fields (reading R5)"""
    kind, nch, d_on = ARMS[arm]; masked = world != "T1"
    w = (ph22.Masked if masked else World7)(runs, np.random.default_rng(seeds[0]), seeds[0])
    rows = np.arange(runs); g = w.good; neutral = 1 - g
    if masked: w.pres = neutral.copy(); w.absent = g.copy()
    tw = World7(runs, np.random.default_rng(seeds[0]), seeds[0]) if masked else None
    rngD = np.random.default_rng(seeds[0] + D_OFF); pD = P_D if d_on else 0.0
    kv = ph32.kv_of(vals, g, nch); a = build(kind, runs, seeds[1], g, kv)
    a.cast_sign = cast_draw(seeds[1], runs)
    if world == "T3a": w.pos = w.src[rows, g].copy(); a.sel.s[rows, g] = 2.0
    o = dict(world=world, arm=arm, cls=type(a).__name__, kind=kind, vals=tuple(vals), kv=kv, d_on=d_on, nch=nch, good=g, cell=w.cell, plus_y=w.plus_y,
             src=w.src.copy(), steps=steps, start=w.pos.copy(), s0=a.sel.s.copy(), H0=a.held(), draws_equal=True, rng_equal=True, viol=0, neg=0,
             **blank16(steps, runs, nch))
    for t in range(steps):
        if masked: tw.pos, tw.head = w.pos.copy(), w.head.copy()
        ps = w.pos.copy(); base = w.sense(); on = w.wind_on(); dw = rngD.random(runs) < pD
        if masked:
            tr = tw.sense()
            o["draws_equal"] &= bool(np.array_equal(tr, w.raw) and np.array_equal(on, tw.wind_on()) and np.array_equal(base[rows, neutral], tr[rows, neutral])
                                     and not base[rows, g].any())
        x = np.concatenate([base, dw[:, None]], 1) if nch == 3 else base
        turn, h = a.act(w, x, on)
        record(o, t, a, h, x, turn, g); record16(o, t, a); o["W"][t, :, 2] = dw; o["CONE"][t] = cone_of(w, ps)
        negm = o["VAL"][t] < 0; o["neg"] += int(negm.sum()); o["viol"] += int((negm & (a.tgt != a.flee_side)).sum())
        w.move(turn); a.bump(w.bumped)
        o["POS"][t] = w.pos; o["HEAD"][t] = w.head; o["AT2"][t] = w.at_source(); o["C"][t] = w.bumped
    if masked: o["rng_equal"] = w.rng.bit_generator.state == tw.rng.bit_generator.state
    o["dwell"] = o["AT2"].sum(0).astype(float); o["contacts"] = o["C"].sum(0).astype(float)
    return o


def job(spec): return run(*spec[:4], **spec[4])


def pool_run(specs):
    if NPROC <= 1: return [job(s) for s in specs]
    with mp.get_context("fork").Pool(NPROC) as p: return p.map(job, specs, chunksize=1)


def runs_of(specs, keys): return dict(zip(keys, pool_run(specs)))


def stub(known, sched, rows=BENCH["rows"], seeds=BS, pre=None, kind="A16"):
    """ph32.stub (ph32.py:327-340) with this file's build: Still world; sched = [(steps, p per channel)]; the same uniform draws for every
    schedule; pre(a) sets a constructed state after construction"""
    nch = 3; steps = sum(s for s, _ in sched); u = np.random.default_rng(seeds[0]).random((steps, rows, nch))
    g = np.zeros(rows, int); kv = np.tile(np.asarray(known, float), (rows, 1)); a = build(kind, rows, seeds[1], g, kv); w = Still(rows)
    if pre is not None: pre(a)
    o = dict(H0=a.held(), steps=steps, **blank16(steps, rows, nch)); t = 0
    for n, ps in sched:
        for _ in range(n):
            x = np.stack([u[t, :, k] < ps[k] for k in range(nch)], 1)
            turn, h = a.act(w, x, np.ones(rows, bool)); record(o, t, a, h, x, turn, g); record16(o, t, a); t += 1
    return o, a


# ------------------------------------------------------------------ measures
def top_of(o):
    """the unranked top set T per (step, row, odour) from the recorded presence and the arm's values (ph32.py:187-188)"""
    kv = o["kv"]; P = o["P2"]; vmax = np.where(P, kv[None], -np.inf).max(2)
    return P & (kv[None] >= 0) & (kv[None] == vmax[:, :, None])


def steering(o):
    """(R8) steering set per (step, row, odour), keep and T (ranked top set for Agent16 arms, T for others), read hold hh"""
    hh = (o["HR"] if o["kind"] == "A16hnr" else o["H"]).astype(int)
    T_ = top_of(o); TR = o["TOPR"] if o["kind"] in A16KINDS else T_
    W = o["W"][:, :, :T_.shape[2]]; kv = o["kv"]; st, n, k = W.shape; r = np.arange(n)
    vh = np.where(hh >= 0, kv[r[None, :], np.maximum(hh, 0)], 0.0)
    held1 = np.zeros((st, n, k), bool); np.put_along_axis(held1, np.maximum(hh, 0)[:, :, None], (hh >= 0)[:, :, None], 2)
    keep = (hh >= 0) & ((TR & held1).any(2) | (vh < 0))
    steer = np.where(keep[:, :, None], held1 & W, W & TR)
    return steer, keep, T_, TR, hh


def entry_lines(tag, o, say, rows=None):
    """(e): D-driven nav events by path (reading R8); returns the counts"""
    n = o["H"].shape[1]; rows = np.ones(n, bool) if rows is None else rows
    steer, keep, T_, TR, hh = steering(o); nav = o["NAV"]
    ok = bool(np.array_equal(nav, steer.any(2))) and (o["kind"] not in A16KINDS or bool(np.array_equal(T_, o["TOP"])))
    D = nav & steer[:, :, 2] & ~steer[:, :, :2].any(2); nT = T_.sum(2)
    burstT = (np.where(T_, o["BB"], NEVER) > NEVER).any(2) if o["kind"] in A16KINDS else np.ones_like(nav)
    cls = {"E2 keep, D read as held": D & keep & (hh == 2), "E1 tie, nothing held": D & ~keep & (nT >= 2) & (hh < 0),
           "E1b tie, a non-kept odour held": D & ~keep & (nT >= 2) & (hh >= 0), "E3 D the lone top odour": D & ~keep & (nT == 1),
           "E4 tie with no burst in T": D & ~keep & (nT >= 2) & ~burstT}
    rr = rows[None, :]; c = {k: int((m & rr).sum()) for k, m in cls.items()}; tot = int((nav & rr).sum()); nD = int((D & rr).sum())
    other = nD - sum(v for k, v in c.items() if not k.startswith("E4"))
    say(f"   [{tag}] nav events {tot}; D-driven {nD} ({nD/max(tot, 1):.3f}); rows with any D-driven nav {int((D & rr).any(0).sum())}/{int(rows.sum())}; "
        + "; ".join(f"{k} {v}" for k, v in c.items()) + f"; unclassified {other} (expected 0); steering law rebuilt == recorded NAV (and T == recorded TOP) {ok}")
    return c, nD, ok, other


def n1_lines(tag, o, say, rows=None):
    """(R8) N1 on the Agent16 D-on run's own state: Agent15's law steers on a V or B whiff, Agent16 does not"""
    n = o["H"].shape[1]; rows = np.ones(n, bool) if rows is None else rows
    hh = o["H"].astype(int); W = o["W"]; st = W.shape[0]; r = np.arange(n)
    held1 = np.zeros(W.shape, bool); np.put_along_axis(held1, np.maximum(hh, 0)[:, :, None], (hh >= 0)[:, :, None], 2)
    steer15 = np.where(o["KEEP15"][:, :, None], held1 & W, W & o["TOP"])
    vb = steer15[:, :, :2].any(2); m = vb & o["NAV15"] & ~o["NAV"] & rows[None, :]
    act = o["ACT"] & rows[None, :]
    say(f"   [{tag}] the rule acts on {int(act.sum())} (step, row), rows with any {int(act.any(0).sum())}/{int(rows.sum())}, first action step {qq(np.where(act.any(0), first_true(act), -1))};"
        f" N1 (Agent15's law steers on a V or B whiff, Agent16 does not) {int(m.sum())} (step, row) in {int(m.any(0).sum())} rows; ties with no burst in T"
        f" (the rule lets nothing steer) {int(((o['TOP'].sum(2) >= 2) & ~o['TOPR'].any(2) & rows[None, :]).sum())} (step, row)")
    return int(m.sum())


def first_act_rows(on16, on15):
    """(R6) (I6'): per row, every field (EVERY + HR) equal on every step strictly before the first ACT step"""
    st = on16["H"].shape[0]; fa = first_true(on16["ACT"]); fax = np.where(fa < 0, st, fa)
    eq = rowmask(on16, on15, EVERY + ("HR",))
    before = np.arange(st)[:, None] < fax[None, :]
    return (eq | ~before).all(0), fa


# ------------------------------------------------------------------ header, readings, seed scan
def seed_numbers():
    w = [SEEDS["dev"][0], SEEDS["eval"][0], BENCH["seed_w"]]; a = [SEEDS["dev"][1], SEEDS["eval"][1], BENCH["seed_a"]]
    base = [*SEEDS["dev"], *SEEDS["eval"], BENCH["seed_w"], BENCH["seed_a"], BENCH["boot"]]
    derived = [s + 10_000 for s in w] + [s + D_OFF for s in w] + [s + 20_000 for s in a] + [s + A3_OFF for s in a]
    extra = [s + 20_000 for s in w] + [BENCH["seed_w"] + 10_000_000, BENCH["seed_a"] + 20_000_000]
    return base + derived + extra


def seeds_unused():
    """design section 9: none of the 24 numbers appears in any other file under the repository (recursive, digit boundary; .git and
    __pycache__ excluded; excluded by name: ph33.py, ph33_*.txt, h28_*.md, master_plan.md, notes/*.md, viewer/*; and the excluded pair)"""
    nums = seed_numbers(); pat = re.compile(rb"(?<!\d)(" + "|".join(map(str, nums)).encode() + rb")(?!\d)"); hits = []; nf = 0
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        top = os.path.relpath(root, REPO).replace("\\", "/").split("/")[0]
        for f in files:
            if f == "ph33.py" or (f.startswith("ph33_") and f.endswith(".txt")) or (f.startswith("h28_") and f.endswith(".md")) or f == "master_plan.md": continue
            if (os.path.basename(root) == "notes" and f.endswith(".md")) or top == "viewer": continue
            nf += 1; rel = os.path.relpath(os.path.join(root, f), REPO).replace("\\", "/")
            found = {int(m) for m in pat.findall(open(os.path.join(root, f), "rb").read())}
            found -= {n for (p, n) in ph32.EXCLUDED_PAIRS if p == rel}
            if found: hits.append((rel, sorted(found)))
    return hits, nums, nf


def header(say=print):
    say(f"   ph33.py sha256 {sha()}; design {DESIGN}")
    say("   imported modules (unchanged): " + "; ".join(f"{os.path.basename(m.__file__)} {sha(m.__file__)}" for m in MODS))
    chk = {k: sha(getattr(sys.modules[k], "__file__")).startswith(v) for k, v in ph32.RECORDED.items()}
    chk["ph32"] = sha(ph32.__file__) == PH32_SHA
    say(f"   recorded versions (ph32's prefixes; ph32.py's full sha256 as H27 ran it) {chk}")
    say(f"   seeds: dev {SEEDS['dev']}, eval {SEEDS['eval']}, bench {BS}, bootstrap {BENCH['boot']} (95 percent, 5000); D generator world + {D_OFF}; third-unit noise agent + {A3_OFF};"
        f" demo seeds (5, 6) used deliberately, NOT part of the seed scan; p_D {P_D}; burst: three whiffs within {WIN + 1} steps")
    say("   seed scan exclusions by name: ph33.py, ph33_*.txt, h28_*.md, master_plan.md, notes/*.md, viewer/*; the (file, number) pair of decision:seed-scan-exclusion-ph31-eval"
        " (experiments/h20/ph31_eval.txt with Stage C Run 1's E1 evaluation agent seed, read from ph30 through ph32, not written here)")
    say("   decisions: decision:h28-open; decision:classification-rule-relaxed-burst-record-h28; decision:evidence-release-composition-rule-h28;"
        " decision:classification-rule-relaxed-presence-prior-h28; the adopted agent: decision:n2-release-adopted-within-tested-conditions")
    if not all(chk.values()): say("== an imported file is not the recorded version: STOP, nothing is run =="); raise SystemExit(4)


def readings(say=print):
    say("   readings where the design is silent (file header R1-R14): R1 as H27 (D = u < p_D from default_rng(world + 30000) in every arm; Circuit3's third unit from"
        " default_rng(agent + 30000); the evidence release against the strongest non-held channel); R2 the burst record: t = the agent's own act count; the most recent"
        " whiff read from the presence counter before its update (t - 1 - c, 'never' if c > t - 1); burst_k = whiff_k and t - w2_k <= 9; b_k <- t on a burst; then"
        " w2_k <- that most recent whiff on a whiff; 'never' -1e9; no random number; R3 the ranked top set reads b after this step's update; T = present, v >= 0, v == v_max;"
        " two or more in T: those with the largest b over T, none if it is 'never'; one or none in T: T; R4 keep = hh >= 0 and (hh in the ranked top set or v_hh < 0);"
        " Agent15's T, keep and nav on the same state kept for measurement (ACT = the rule acts); R5 trajectory and every field as H27 R5, Agent16's measurement fields"
        " never compared; R6 (I2') before each row's first D whiff; (I5') V present by its counter on every step of Agent16 D off; (I6') every field (and HR) before each row's"
        " first ACT step; R7 (m) three definitions (H27 R7; H26 at-risk from 59 and from 0; literal no V whiff on 0-58); (w) no B whiff on 0-58; R8 (e) D-driven = steering"
        " set {D} alone; E2 keep with D held, E1 tie nothing held, E1b tie with a non-kept odour held, E3 D the lone top odour, E4 a D-driven nav in a tie with no burst in T"
        " (checked 0), E5 the classes in the hold-not-read arm; N1 on Agent16 D-on's own state (Agent15's law steers on a V or B whiff, Agent16 does not); R9 pass"
        " probabilities by sqrt(b - DP^2)/20, (h) M2(b) lower bar -0.05, (hW) M5(a') upper bar -0.20, STOP below 0.5; R10 H27's W1D bars reported (reach 0.80,"
        " bar_W = -0.20 x the bench's Agent16 D-off W1 dwell rounded to 0.1, contacts 0.10, lost-row DP +0.05); R11 M1 arms H26's (two channels, no D), Agent15g = H27's"
        " filter-off arm, release-off and hold-not-read = Agent16 with release off / hold not read; R12 bench (b) brute force from the recorded whiffs, (c) a per-row Python"
        " loop, H27's (b3), (c) on the new seeds, (d) on the T1D Agent16 run; R13 dev/eval re-run the bench for M4; R14 arms in parallel processes")


# ------------------------------------------------------------------ bench parts (b), (c)
def brute_record(Wk):
    """(R12) per channel column Wk (steps, rows): burst, b (last burst at or before t), w2 (second most recent whiff at or before t)"""
    st, n = Wk.shape; burst = np.zeros((st, n), bool); b = np.full((st, n), NEVER); w2 = np.full((st, n), NEVER)
    for i in range(n):
        wh = []; lb = NEVER
        for t in range(st):
            if Wk[t, i]:
                if sum(1 for s in wh if s >= t - WIN) >= 2: burst[t, i] = True; lb = t
                wh.append(t)
            b[t, i] = lb; w2[t, i] = wh[-2] if len(wh) >= 2 else NEVER
    return burst, b, w2


def b_bench(say, seeds=BS, rows=BENCH["rows"]):
    res = {}; kn = (1.0, 0.0, 0.0)
    scheds = {"ubiquitous p 0.03, D only, 600 steps": [(600, [0.0, 0.0, 0.03])],
              "plume-like p 0.30 for 20 steps then silence, B only": [(20, [0.0, 0.30, 0.0]), (580, [0.0, 0.0, 0.0])],
              "silence from construction": [(600, [0.0, 0.0, 0.0])],
              "two channels: B's burst and D's stream together": [(20, [0.0, 0.30, 0.03]), (580, [0.0, 0.0, 0.03])],
              "three channels, each p 0.03": [(600, [0.03, 0.03, 0.03])]}
    runs = {k: stub(kn, s, rows=rows, seeds=seeds)[0] for k, s in scheds.items()}
    for k, o in runs.items():
        ok = True; parts = []
        for ch in range(3):
            bu, b, w2 = brute_record(o["W"][:, :, ch])
            e = bool(np.array_equal(o["BURST"][:, :, ch], bu) and np.array_equal(o["BB"][:, :, ch].astype(float), b) and np.array_equal(o["BW2"][:, :, ch].astype(float), w2))
            ok &= e; nw, nb = int(o["W"][:, :, ch].sum()), int(bu.sum())
            if nw: parts.append(f"ch {ch}: whiffs {nw}, bursts {nb} ({nb/nw:.4f} per whiff)")
        extra = ""
        if k.startswith("plume"):
            B = o["BB"][:, :, 1]; unch = bool((B[20:] == B[19][None, :]).all()); fb = first_true(o["BURST"][:, :, 1])
            extra = f"; b unchanged over the 580 silent steps {unch}; rows with a burst {int((fb >= 0).sum())}/{rows}, first burst step {qq(fb)}"; ok &= unch
        if k.startswith("silence"):
            none = bool((~o["BURST"]).all() and (o["BB"] == NEVER).all()); extra = f"; no burst and b 'never' on every channel and step {none}"; ok &= none
        if k.startswith("ubiquitous"):
            nw, nb = int(o["W"][:, :, 2].sum()), int(o["BURST"][:, :, 2].sum()); p, lo, hi = ph15.wilson(nb, nw)
            extra = f"; burst fraction per D whiff {nb}/{nw} = {nb/nw:.4f} [{lo:.4f}, {hi:.4f}] beside the design's 0.0282 (reported)"
        res[k] = ok
        say(f"(b) {k}: record (burst, b, w2) == brute force on every step, row and channel {ok}; " + "; ".join(parts) + extra)
    o1, o2, o4 = runs["ubiquitous p 0.03, D only, 600 steps"], runs["plume-like p 0.30 for 20 steps then silence, B only"], runs["two channels: B's burst and D's stream together"]
    ind = all(np.array_equal(o4[f][:, :, 1], o2[f][:, :, 1]) and np.array_equal(o4[f][:, :, 2], o1[f][:, :, 2]) for f in ("BURST", "BB", "BW2", "W"))
    res["independent channels"] = ind
    say(f"(b) independence: in the two-channel schedule B's record == the B-only schedule's and D's == the D-only schedule's (same draws) {ind}")
    return all(res.values()), res


def c16_bench(say, seeds=BS):
    """(R12) the ranked top set, keep and nav on constructed states through the act, against a per-row Python loop"""
    combos = [(m, hk, vp, bp, dp, bo) for m in range(8) for hk in (-1, 0, 1, 2) for vp in (True, False) for bp in (True, False)
              for dp in (True, False) for bo in range(5)]*2
    n = len(combos); t0 = 50
    X = np.array([[bool(m & 1), bool(m & 2), bool(m & 4)] for m, *_ in combos]); HK = np.array([c[1] for c in combos])
    PR_ = np.array([[c[2], c[3], c[4]] for c in combos]); BO = np.array([c[5] for c in combos])
    bpre = np.full((n, 3), NEVER); bpre[BO == 1, 1] = 30; bpre[BO == 2, 2] = 30; bpre[BO == 3, 1] = 40; bpre[BO == 3, 2] = 30; bpre[BO == 4, 1] = 30; bpre[BO == 4, 2] = 40

    def pre(a):
        r = np.arange(n); a.sel.s[r[HK >= 0], HK[HK >= 0]] = 2.0
        a.c = np.where(PR_, 0.0, 1000.0); a.bb = bpre.copy(); a.w2 = np.full((n, 3), NEVER); a.t16 = t0
    kv = np.tile([1.0, 0.0, 0.0], (n, 1)); a = build("A16", n, seeds[1], np.zeros(n, int), kv); pre(a)
    a.act(Still(n), X, np.ones(n, bool)); h = a.held()
    ok = True; bad = 0; cnt = {"tie, none burst": 0, "tie, one ranked": 0, "no tie": 0}
    for i in range(n):
        v = [1.0, 0.0, 0.0]; hi = int(h[i]); c = [0.0 if X[i, k] else (1.0 if PR_[i, k] else 1001.0) for k in range(3)]
        pres = [c[k] < N_HI or hi == k for k in range(3)]
        vmax = max([v[k] for k in range(3) if pres[k]], default=-math.inf)
        T_ = [pres[k] and v[k] >= 0 and v[k] == vmax for k in range(3)]
        b = [float(bpre[i, k]) for k in range(3)]                                          # w2 'never': no burst on this step
        if sum(T_) >= 2:
            bm = max(b[k] for k in range(3) if T_[k])
            TR = [T_[k] and b[k] == bm and bm > NEVER for k in range(3)]
            cnt["tie, none burst" if bm == NEVER else "tie, one ranked"] += 1
        else:
            TR = T_; cnt["no tie"] += 1
        vh = v[hi] if hi >= 0 else 0.0
        keep = hi >= 0 and (TR[hi] or vh < 0)
        nav = bool(X[i, hi]) if keep else any(X[i, k] and TR[k] for k in range(3))
        e = (nav == bool(a.nav_hit[i]) and keep == bool(a.keep16[i]) and TR == [bool(x) for x in a.topr[i]] and pres == [bool(x) for x in a.present[i]]
             and T_ == [bool(x) for x in a.top15[i]] and not a.burst[i].any())
        ok &= e; bad += int(not e)
    held_ok = int((h == HK).sum())
    # named cases (V absent, B and D present, nothing held, both whiffing)
    sel = lambda bo: (HK == -1) & ~PR_[:, 0] & PR_[:, 1] & PR_[:, 2] & X[:, 1] & X[:, 2] & ~X[:, 0] & (BO == bo)
    named = {"no burst: nothing steers": bool((~a.nav_hit[sel(0)]).all() and (~a.topr[sel(0)]).all()),
             "B only burst: {B}": bool((a.topr[sel(1)] == [False, True, False]).all()), "D only burst: {D}": bool((a.topr[sel(2)] == [False, False, True]).all()),
             "B more recent: {B}": bool((a.topr[sel(3)] == [False, True, False]).all()), "D more recent: {D}": bool((a.topr[sel(4)] == [False, False, True]).all())}
    vp = PR_[:, 0]; named["V present: top {V} whatever the bursts"] = bool((a.topr[vp] == [True, False, False]).all())
    say(f"(c) ranked top set, keep, nav, presence and T through the act at (+1, 0, 0), {n} rows (whiffs 2^3 x held none/V/B/D x V, B, D present/absent x burst order"
        f" none/B only/D only/B more recent/D more recent, x2), against a per-row Python loop: exact {ok} (rows differing {bad}); states: {cnt}; held after the step as"
        f" constructed {held_ok}/{n}; named cases " + "; ".join(f"{k} {v}" for k, v in named.items()))
    return ok and all(named.values())


# ------------------------------------------------------------------ the mechanism bench (design section 4)
def bench_specs(seeds, runs=R, steps=T):
    v3, v2, vpm = (1.0, 0.0, 0.0), (1.0, 0.0), (1.0, -1.0); kw = dict(runs=runs, steps=steps); sp = {}
    for wd_ in ("T1", "W1", "T3a"):
        for arm in ("Agent16 D on", "Agent16 D off", "Agent15 D on", "Agent15 D off", "hold-not-read D on", "hold-not-read D off"): sp[(wd_, arm)] = (wd_, arm, v3, seeds, kw)
        for arm in ("Agent14N2", "Agent16 at N 2"):
            sp[(wd_, arm)] = (wd_, arm, v2, seeds, kw); sp[(wd_, arm, "+1/-1")] = (wd_, arm, vpm, seeds, kw)
    for wd_ in ("T1", "W1"): sp[(wd_, "Agent15g D on")] = (wd_, "Agent15g D on", v3, seeds, kw)
    sp[("W1", "release-off D on")] = ("W1", "release-off D on", v3, seeds, kw)
    return sp


def identities(res, say=print):
    ids = {}
    for wd_ in ("T1", "W1", "T3a"):
        ids[f"I1' {wd_} +1/0"] = ph32.every(res[(wd_, "Agent16 at N 2")], res[(wd_, "Agent14N2")])
        ids[f"I1' {wd_} +1/-1"] = ph32.every(res[(wd_, "Agent16 at N 2", "+1/-1")], res[(wd_, "Agent14N2", "+1/-1")])
    say("(I1') Agent16's code at N 2 == Agent14N2 on every field (reading R5): " + "; ".join(f"{k[4:]} {v}" for k, v in ids.items()))
    for wd_ in ("T1", "W1", "T3a"):
        for arm in ("Agent16", "hold-not-read"):
            ok, fd = i2_rows(res[(wd_, f"{arm} D on")], res[(wd_, f"{arm} D off")]); ids[f"I2' {wd_} {arm}"] = bool(ok.all())
            say(f"(I2') {wd_} {arm}: D on == D off on every field before each row's first D whiff: rows {int(ok.sum())}/{len(ok)} -> {bool(ok.all())}; first D whiff step {qq(fd)}")
    for wd_ in ("T1", "W1", "T3a"):
        off16, off15, ref, hn = res[(wd_, "Agent16 D off")], res[(wd_, "Agent15 D off")], res[(wd_, "Agent14N2")], res[(wd_, "hold-not-read D off")]
        e = same(off16, off15, EVERY + ("HR",)); tr = traj(off16, ref); ids[f"I3' {wd_} every field == Agent15 D off"] = e; ids[f"I3' {wd_} trajectory == Agent14N2"] = tr
        na = int(off16["ACT"].sum()); ids[f"I3' {wd_} the rule never acts without D"] = na == 0
        i4 = traj(hn, off16); ids[f"I4' {wd_}"] = i4
        say(f"(I3') {wd_}: Agent16 D off == Agent15 D off on every field (and HR) {e}; == Agent14N2 on the trajectory fields {tr} (rows"
            f" {int(rowmask(off16, ref, TRAJ, True).all(0).sum())}/{len(off16['good'])}); (step, row) on which the rule acts without D {na}; (I4') hold-not-read D off =="
            f" Agent16 D off on the trajectory fields {i4}")
    on, off = res[("T1", "Agent16 D on")], res[("T1", "Agent16 D off")]; vab = v_absent(off); pres = ~vab
    eqr = rowmask(on, off, TRAJ, True).all(0); i5 = bool(eqr[pres].all()); ids["I5' T1"] = i5
    say(f"(I5') T1: rows with V present by its counter on every step of the Agent16 D-off run {int(pres.sum())}/{len(pres)}; of them D on == D off on the trajectory fields"
        f" {int(eqr[pres].sum())} -> {i5}; rows with V ever absent {int(vab.sum())}, of them equal {int(eqr[vab].sum())}")
    for wd_ in ("T1", "W1", "T3a"):
        ok, fa = first_act_rows(res[(wd_, "Agent16 D on")], res[(wd_, "Agent15 D on")]); ids[f"I6' {wd_}"] = bool(ok.all())
        say(f"(I6') {wd_}D: Agent16 D on == Agent15 D on on every field (and HR) before each row's first action of the rule (reading R6): rows {int(ok.sum())}/{len(ok)} ->"
            f" {bool(ok.all())}; rows in which the rule acts {int((fa >= 0).sum())}, first action step {qq(fa)}")
    fl = {k: v["neg"] for k, v in res.items() if v["vals"] in ((1.0, 0.0, 0.0), (1.0, 0.0))}; nofl = all(x == 0 for x in fl.values()); ids["I6' no flee at +1/0/0"] = nofl
    dr = all(o["draws_equal"] and o["rng_equal"] for o in res.values()); ids["masked draws == World7 twin"] = dr
    t3c = all(np.array_equal(res[("T3a", a)]["start"], res[("T3a", a)]["src"][np.arange(len(res[("T3a", a)]["good"])), res[("T3a", a)]["good"]])
              and (res[("T3a", a)]["H0"] == res[("T3a", a)]["good"]).all() for a in ("Agent16 D on", "Agent16 D off", "Agent15 D on", "Agent14N2", "hold-not-read D on"))
    ids["T3a construction"] = bool(t3c)
    say(f"(I6') no flee command (steps with a negatively valued read hold) in any arm at +1/0(/0): {nofl}; masked draws =="
        f" the World7 twin, generator state equal, every W1/T3a run {dr}; T3a construction (start at the valued source, valued hold s 2.0) {bool(t3c)}")
    return ids


def w1_line(say, k, v, steps):
    say(f"      [W1 {k}] mean dwell within 3.0 of B over {steps} steps {v['dwell'].mean():.3f} (quartiles {q3(v['dwell'])}); reach {int(v['reach'].sum())}/{len(v['dwell'])}; lost rows"
        f" {int(v['lost'].sum())}; wall contacts per row {v['contacts'].mean():.3f}")


def bench(say=print, seeds=BS, runs=R, steps=T):
    say(f"== H28 mechanism bench (design v2 FINAL section 4). design {DESIGN}; {BENCH}; p_D {P_D}; P {P_PRIOR}, N_hi {N_HI}; bootstrap seed {ph15.BOOT_SEED} ==")
    header(say); readings(say)
    say("   rows share no state: one generator per world, one for D, one per agent population and one for the third unit, fixed-size draws consumed in row order every step;"
        " the burst record draws none")
    sp = bench_specs(seeds, runs, steps); res = runs_of(list(sp.values()), list(sp.keys())); out = {}
    t1 = {a: res[("T1", a)] for a in ("Agent16 D on", "Agent16 D off", "Agent15 D on", "Agent15 D off", "Agent14N2", "Agent15g D on", "hold-not-read D on")}
    w1 = {a: res[("W1", a)] for a in ("Agent16 D on", "Agent16 D off", "Agent15 D on", "Agent15 D off", "Agent14N2", "Agent15g D on", "hold-not-read D on", "hold-not-read D off", "release-off D on")}
    # ---- (m), (w): printed first
    off = t1["Agent16 D off"]; vab = v_absent(off); fv = first_true(wv(off)); lit = (fv < 0) | (fv > PR - 1)
    risk, _ = ph28.at_risk(off); risk0, _ = ph28.at_risk(off, lo=0)
    say(f"(m) T1 rows with V ever absent (H27's definition, reading R7; Agent16 D off): {int(vab.sum())}/{runs}; H26's at-risk definition (ph28 reading R3, from step {PR}):"
        f" {int(risk.sum())} (literal from step 0: {int(risk0.sum())}); literal prior expiry (no V whiff on 0-{PR - 1}): {int(lit.sum())}; of the (m) rows prior expiry"
        f" {int((vab & lit).sum())}, silence {int((vab & ~lit).sum())}; first V whiff step {qq(fv)}")
    for tag, o in (("W1 Agent16 D off", w1["Agent16 D off"]), ("W1D Agent16 D on", w1["Agent16 D on"])):
        nb = ~wb(o)[:PR].any(0); out.setdefault("w", int(nb.sum()))
        say(f"(w) {tag}: rows with no B whiff on steps 0-{PR - 1}: {int(nb.sum())}/{runs}")
    say(f"   (w) the two runs agree row by row on it: {bool(np.array_equal(~wb(w1['Agent16 D off'])[:PR].any(0), ~wb(w1['Agent16 D on'])[:PR].any(0)))}")
    # ---- (e) entry points and N1, printed first
    say("(e) entry points of D into navigation (reading R8):")
    eok = True; ecnt = {}
    for tag, o in (("T1D Agent16 D on", t1["Agent16 D on"]), ("T1D hold-not-read D on (E5)", t1["hold-not-read D on"]), ("T1D Agent15 D on (floor)", t1["Agent15 D on"]),
                   ("W1D Agent16 D on", w1["Agent16 D on"]), ("W1D hold-not-read D on (E5)", w1["hold-not-read D on"]), ("W1D Agent15 D on (floor)", w1["Agent15 D on"])):
        c, nD, ok, other = entry_lines(tag, o, say); ecnt[tag] = (c, nD); eok &= ok and other == 0
        if o["kind"] in A16KINDS: eok &= c["E4 tie with no burst in T"] == 0
    entry_lines("T1D Agent16 D on, the (m) rows", t1["Agent16 D on"], say, vab); entry_lines("W1D Agent16 D on, the (w) rows", w1["Agent16 D on"], say, ~wb(w1["Agent16 D off"])[:PR].any(0))
    out["N1_T1"] = n1_lines("T1D Agent16 D on", t1["Agent16 D on"], say); n1_lines("T1D Agent16 D on, the (m) rows", t1["Agent16 D on"], say, vab)
    out["N1_W1"] = n1_lines("W1D Agent16 D on", w1["Agent16 D on"], say)
    say(f"   (e) E4 == 0 in every Agent16 arm and the steering law == the recorded NAV in every classified run: {eok}")
    # ---- implementation parts
    ids = identities(res, say); bars = {}
    bars["b"], _ = b_bench(say, seeds)
    bars["c"] = c16_bench(say, seeds)
    bars["b3 (H27)"] = ph32.b3(lambda s: say(s.replace("(b3)", "(b3, H27's, Agent15)", 1)), seeds=seeds)
    okc, rc = ph32.c_bench(lambda s: say(s.replace("(c)", "(c, H27's, Agent15)", 1)), seeds=seeds); bars["c (H27)"] = okc
    bars["d (H27)"] = ph32.d_bench(t1["Agent16 D on"], lambda s: say(s.replace("Agent15 run", "Agent16 run", 1)))
    bars["e"] = eok
    # ---- (h)
    cl = {k: cls3(o) for k, o in t1.items()}; V = {k: c == 0 for k, c in cl.items()}
    for k in ("Agent16 D on", "Agent16 D off", "Agent15 D on", "Agent14N2", "Agent15g D on", "hold-not-read D on"):
        c = cl[k]; kk, pt, lo, hi = interval("P", V[k])
        say(f"      [T1 {k}] V {int((c == 0).sum())} N {int((c == 1).sum())} tie {int((c == 2).sum())}; P(V) {pt:.3f} [{lo:.3f}, {hi:.3f}]; lost rows {int(lost_t1(t1[k]).sum())}")
    into, outv = int((V["Agent16 D on"] & ~V["Agent16 D off"]).sum()), int((~V["Agent16 D on"] & V["Agent16 D off"]).sum())
    say(f"      [(m) rows, {int(vab.sum())}] outcome V/N/tie: Agent16 D on {int((cl['Agent16 D on'][vab] == 0).sum())}/{int((cl['Agent16 D on'][vab] == 1).sum())}/{int((cl['Agent16 D on'][vab] == 2).sum())};"
        f" Agent16 D off {int((cl['Agent16 D off'][vab] == 0).sum())}/{int((cl['Agent16 D off'][vab] == 1).sum())}/{int((cl['Agent16 D off'][vab] == 2).sum())};"
        f" Agent15 D on {int((cl['Agent15 D on'][vab] == 0).sum())}/{int((cl['Agent15 D on'][vab] == 1).sum())}/{int((cl['Agent15 D on'][vab] == 2).sum())}")
    say(f"      Agent16 D on vs D off: into V {into}, out of V {outv} (all out-of-V rows in (m): {bool(((~V['Agent16 D on'] & V['Agent16 D off']) <= vab).all())});"
        f" rows equal on the trajectory fields {int(rowmask(t1['Agent16 D on'], off, TRAJ, True).all(0).sum())}/{runs}")
    dp, b = pair_dp(V["Agent16 D on"], V["Agent16 D off"]); _, _, dlo, dhi = interval("DP", V["Agent16 D on"].astype(float), V["Agent16 D off"].astype(float))
    ppb = pp_dp(dp, b, -0.05); stop_h = ppb < 0.5
    dpc, bc = pair_dp(V["Agent16 D on"], V["Agent15g D on"]); ppc = pp_dp(dpc, bc, 0.05)
    dpd, _ = pair_dp(V["Agent16 D on"], V["Agent15 D on"]); _, _, ddlo, ddhi = interval("DP", V["Agent16 D on"].astype(float), V["Agent15 D on"].astype(float))
    say(f"(h) T1D on bench seeds, +1/0/0 {runs} x {steps}: paired DP P(V) Agent16 D on - Agent16 D off {dp:+.4f} [{dlo:+.4f}, {dhi:+.4f}] (bootstrap 5000, seed {ph15.BOOT_SEED});"
        f" discordant b {b:.4f}, sd sqrt(b - DP^2) {math.sqrt(max(b - dp*dp, 0.0)):.4f}; M2(b) pass probability {ppb:.4f}; M2(c) vs Agent15g at DP {dpc:+.4f} (b {bc:.4f}): {ppc:.4f};"
        f" M2(d) reported: Agent16 D on - Agent15 D on {dpd:+.4f} [{ddlo:+.4f}, {ddhi:+.4f}]; M2(a) reported, P(K >= 365 of 400) at P(V) {V['Agent16 D on'].mean():.3f}:"
        f" {binom_ge(V['Agent16 D on'].mean()):.4f}; floor Agent15 D on P(V) {V['Agent15 D on'].mean():.3f}, ceiling Agent16 D off {V['Agent16 D off'].mean():.3f}")
    say(f"   (h) STOP RULE (design section 4): M2(b) pass probability {ppb:.4f} {'< 0.5 -> STOP' if stop_h else '>= 0.5 -> continue'}")
    out.update(dp_T1=dp, dp_lo=dlo, dp_hi=dhi, b_T1=b, pp_M2b=ppb, pp_M2c=ppc, dp_M2c=dpc, dp_M2d=dpd, stop_h=stop_h, m=int(vab.sum()), into=into, outv=outv,
               PV={k: float(v.mean()) for k, v in V.items()})
    # ---- (hW)
    s = {k: w1sum(o) for k, o in w1.items()}
    for k, v in s.items(): w1_line(say, k, v, steps)
    dpl, bl = pair_dp(s["Agent16 D on"]["lost"], s["Agent15 D on"]["lost"]); ppw = pp_dp(dpl, bl, -0.20, most=True); stop_hw = ppw < 0.5
    _, _, llo, lhi = interval("DP", s["Agent16 D on"]["lost"].astype(float), s["Agent15 D on"]["lost"].astype(float))
    say(f"(hW) W1D on bench seeds: lost rows (no B whiff in 400-599) Agent16 D on {int(s['Agent16 D on']['lost'].sum())}, Agent15 D on (floor) {int(s['Agent15 D on']['lost'].sum())},"
        f" Agent16 D off (ceiling) {int(s['Agent16 D off']['lost'].sum())}; paired DP Agent16 D on - Agent15 D on {dpl:+.4f} [{llo:+.4f}, {lhi:+.4f}] (b {bl:.4f},"
        f" sd {math.sqrt(max(bl - dpl*dpl, 0.0)):.4f}); M5(a') pass probability (upper bound <= -0.20) {ppw:.4f}")
    say(f"   (hW) STOP RULE (design section 4): M5(a') pass probability {ppw:.4f} {'< 0.5 -> STOP' if stop_hw else '>= 0.5 -> continue'}")
    Doff = float(s["Agent16 D off"]["dwell"].mean()); bar_w = round(-0.20*Doff, 1)
    pp5b, m5b, sd5b = pass_prob(s["Agent16 D on"]["dwell"] - s["Agent16 D off"]["dwell"], bar_w)
    dpd5, bd5 = pair_dp(s["Agent16 D on"]["lost"], s["Agent16 D off"]["lost"]); pp5d = pp_dp(dpd5, bd5, 0.05, most=True)
    k5a, pt5a, lo5a, hi5a = interval("P", s["Agent16 D on"]["reach"])
    say(f"   (hW) H27's W1D bars against D off, READINGS, no stop (reading R10): (a) reach {k5a}/{runs} = {pt5a:.3f} [{lo5a:.3f}, {hi5a:.3f}] against 0.80; (b) D_off"
        f" (Agent16's W1 dwell without D) {Doff:.4f}, bar_W {bar_w:+.1f}, paired dwell D on - D off {m5b:+.4f} sd {sd5b:.4f}, pass probability {pp5b:.4f}; (c) contacts per row"
        f" {s['Agent16 D on']['contacts'].mean():.3f} against 0.10; (d) lost-row DP D on - D off {dpd5:+.4f} (b {bd5:.4f}), pass probability {pp5d:.4f}")
    dp6, b6 = pair_dp(s["hold-not-read D on"]["lost"], s["Agent16 D on"]["lost"]); _, _, l6, h6 = interval("DP", s["hold-not-read D on"]["lost"].astype(float), s["Agent16 D on"]["lost"].astype(float))
    say(f"   M6 the hold's benefit, REPORTED (no stop): lost-row DP hold-not-read D on - Agent16 D on {dp6:+.4f} [{l6:+.4f}, {h6:+.4f}] (b {b6:.4f}); release-off D on lost"
        f" {int(s['release-off D on']['lost'].sum())}, Agent15g D on lost {int(s['Agent15g D on']['lost'].sum())}")
    out.update(dp_W1=dpl, lo_W1=llo, hi_W1=lhi, b_W1=bl, pp_M5a=ppw, stop_hw=stop_hw, D_off=Doff, bar_W=bar_w, lost={k: int(v["lost"].sum()) for k, v in s.items()},
               dwell={k: float(v["dwell"].mean()) for k, v in s.items()}, dp6=dp6)
    say("      [T3a reported] neutral dwell 100-599: " + ", ".join(f"{a} {t3_dwell(res[('T3a', a)], 100, steps).mean():.3f}" for a in ("Agent16 D on", "Agent16 D off", "Agent15 D on", "Agent14N2", "hold-not-read D on")))
    idok = all(ids.values()); bok = all(bars.values()); verdict = idok and bok; stop = stop_h or stop_hw; out["stop"] = stop; out["ids"] = ids; out["bars"] = bars
    say(f"== M4: identities {idok}; failed {[k for k, v in ids.items() if not v]}; implementation parts {bars} -> M4"
        f" {'PASS: the tasks may be run' if verdict else 'FAIL, NO CANDIDATE: an implementation error (design section 4); the tasks are NOT run'}; stop rules (h)"
        f" {'STOP' if stop_h else 'continue'}, (hW) {'STOP' if stop_hw else 'continue'} ==")
    return verdict, out, res


# ------------------------------------------------------------------ self-checks
def demo():
    print(f"== H28 self-checks (demo). design {DESIGN} ==")
    header(); readings()
    print("   fixed before this recorded demo (one earlier trial run of this demo on the demo seeds 5/6 only, no registered seed, every check passing): the (I1')"
          " line printed its labels with the first letter cut ('1 +1/0' for 'T1 +1/0'); the label slice corrected; no model, harness, bar or rule code changed")
    n, st, sd = 40, 200, (5, 6); kw = dict(runs=n, steps=st); v3, v2 = (1.0, 0.0, 0.0), (1.0, 0.0)
    mro = [c.__name__ for c in Agent16.__mro__[:8]]
    assert mro == ["Agent16", "ReleaseN2", "Agent14", "Release", "Act16", "Act15", "Agent9", "Agent8"], mro
    a = build("A16", 4, 5, np.zeros(4, int), np.zeros((4, 3)))
    assert super(Release, a).act.__func__ is Act16.act and a.sel.n == 3 and a.up.P.shape == (4, 3) and a.c.shape == (4, 3) and (a.c == 240).all() and a.codes.shape[1] == 3
    assert a.bb.shape == (4, 3) and (a.bb == NEVER).all() and (a.w2 == NEVER).all() and a.t16 == 0
    a2 = build("A16n2", 4, 5, np.zeros(4, int), np.zeros((4, 2))); assert a2.sel.n == 2 and a2.c.shape == (4, 2) and a2.bb.shape == (4, 2)
    print(f"ok  method order {mro}; ReleaseN2's base act is Act16.act; stage chans 3, circuit n 3, counter (R, 3) at 240, three codes; burst record (R, 3) 'never', t 0; at N 2 all (R, 2)")
    # harness fidelity: this run() == ph32.run for H27's arms
    for wd_ in ("T1", "W1", "T3a"):
        for arm, vv in (("Agent15 D on", v3), ("Agent15 D off", v3), ("Agent14N2", v2), ("Agent15g D on", v3)):
            if arm == "Agent15g D on" and wd_ == "T3a": continue
            mine = run(wd_, arm, vv, sd, **kw); ref = ph32.run(wd_, arm, vv, sd, **kw)
            assert all(np.array_equal(mine[k], ref[k]) for k in EVERY + ("HR", "CONE")), (wd_, arm)
    print(f"ok  this harness == ph32.run (H27's harness) bitwise on every field, HR and CONE for Agent15 D on/off, Agent14N2, Agent15g D on, {n} x {st}, T1, W1, T3a")
    sp = bench_specs(sd, n, st); res = runs_of(list(sp.values()), list(sp.keys()))
    seq = run("W1", "Agent16 D on", v3, sd, **kw)
    assert all(np.array_equal(seq[k], res[("W1", "Agent16 D on")][k]) for k in EVERY + ("HR", "TOPR", "BB", "BW2", "ACT")), "parallel != sequential"
    print("ok  a parallel result equals a sequential one bitwise (W1 Agent16 D on, every field and the burst record)")
    lines = []; ids = identities(res, lines.append)
    for ln in lines: print("    " + ln)
    assert all(ids.values()), [k for k, v in ids.items() if not v]
    print(f"ok  identities (I1')-(I6') on demo seeds {n} x {st}: all True")
    okb, rb = b_bench(lambda s: print("    " + s), seeds=sd, rows=100); assert okb, rb
    okc = c16_bench(lambda s: print("    " + s), seeds=sd); assert okc
    assert ph32.b3(lambda s: print("    " + s), seeds=sd); okc2, rc2 = ph32.c_bench(lambda s: print("    " + s), seeds=sd); assert okc2, rc2
    print("ok  bench (b) and (c) exact on constructed schedules and states built on the demo seeds; H27's (b3) and (c) re-run (the bench re-runs all on the bench seeds)")
    ec = []
    for tag, o in (("T1D Agent16 D on (demo seeds)", res[("T1", "Agent16 D on")]), ("W1D Agent16 D on (demo seeds)", res[("W1", "Agent16 D on")]),
                   ("W1D hold-not-read D on (demo seeds)", res[("W1", "hold-not-read D on")]), ("W1D Agent15 D on (demo seeds)", res[("W1", "Agent15 D on")])):
        c, nD, ok, other = entry_lines(tag, o, lambda s: print("    " + s)); assert ok and other == 0 and (o["kind"] not in A16KINDS or c["E4 tie with no burst in T"] == 0)
    print("ok  entry-point classification (e): the steering law rebuilt from the recorded fields == the recorded NAV, every D-driven event classified, E4 0 (demo seeds;"
          " a smoke run on unregistered seeds, its counts not used)")
    # pass-probability arithmetic against the design's section 7 tables
    tab = {k: pp_dp(-k/400.0, k/400.0, -0.05) for k in (5, 8, 10, 12, 13, 15)}; exp = {5: 1.00, 8: 0.99, 10: 0.89, 12: 0.65, 13: 0.51, 15: 0.26}
    assert all(abs(tab[k] - exp[k]) < 0.01 for k in exp), tab
    tw = {L: pp_dp((L - 400)/400.0, (400 - L)/400.0, -0.20, most=True) for L in (250, 280, 300, 320)}; expw = {250: 1.00, 280: 0.99, 300: 0.64, 320: 0.03}
    assert all(abs(tw[L] - expw[L]) < 0.01 for L in expw), tw
    print("ok  pass-probability arithmetic reproduces the design's section 7 tables: M2(b) k 5/8/10/12/13/15 = " + "/".join(f"{tab[k]:.3f}" for k in exp)
          + "; M5(a') L 250/280/300/320 (Agent15 400, lost in Agent16 only 0) = " + "/".join(f"{tw[L]:.3f}" for L in expw))
    hits, nums, nf = seeds_unused(); assert not hits, f"a seed of this run appears in {hits}"
    print(f"ok  seeds {nums} appear in no other file under the repository ({nf} files scanned; excluded by name ph33.py, ph33_*.txt, h28_*.md, master_plan.md, notes/*.md,"
          f" viewer/*; the pair of decision:seed-scan-exclusion-ph31-eval)")


# ------------------------------------------------------------------ the tasks (design sections 5-8)
def task_specs(seeds):
    sp = bench_specs(seeds); kw = dict(runs=R, steps=T)
    for a, v in (("neutral", (0.0, 0.0)), ("pathway-off", (1.0, 0.0)), ("known-answer", (1.0, 0.0)), ("neutral D on", (0.0, 0.0, 0.0))): sp[("T1", a)] = ("T1", a, v, seeds, kw)
    sp[("T4", "Agent14N2")] = ("T1", "Agent14N2", (1.0, -1.0), seeds, kw); sp[("T4", "Agent16 D on")] = ("T1", "Agent16 D on", (1.0, -1.0, 0.0), seeds, kw)
    return sp


def cells_line(o, c):
    return " | ".join(f"cell {k}: V {int(((c == 0) & (o['cell'] == k)).sum())} N {int(((c == 1) & (o['cell'] == k)).sum())} 0 {int(((c == 2) & (o['cell'] == k)).sum())}" for k in range(4))


T1SHOW = ("Agent16 D on", "Agent16 D off", "Agent15 D on", "Agent15 D off", "Agent14N2", "Agent15g D on", "hold-not-read D on", "neutral D on", "neutral", "pathway-off", "known-answer")
W1SHOW = ("Agent16 D on", "Agent16 D off", "Agent15 D on", "Agent15 D off", "Agent14N2", "hold-not-read D on", "release-off D on", "Agent15g D on")


def main(mode):
    seeds = SEEDS[mode]
    print(f"== H28, {mode.upper()}. design {DESIGN}; G {G_STAR}, gate on; P {P_PRIOR}, N_hi {N_HI}; p_D {P_D}; world seed {seeds[0]}, agent seed {seeds[1]}; {R} rows x {T} steps;"
          f" geometry C0; bootstrap seed {ph15.BOOT_SEED}; {'operation check only (not a verdict)' if mode == 'dev' else 'the one evaluation'} ==")
    header(); readings()
    hits, nums, nf = seeds_unused(); print(f"   seed self-check: every H28 seed and derived number in no other file ({nf} scanned): {not hits}{'' if not hits else ' ' + str(hits)}")
    if hits: print("== a seed appears in another file: STOP =="); sys.exit(5)
    print("   amendments: none")
    print("   rows share no state: one generator per world, one for D, one per agent population and one for the third unit; the burst record draws none")
    sp = task_specs(seeds); res = runs_of(list(sp.values()), list(sp.keys()))
    t1 = {a: res[("T1", a)] for a in T1SHOW}; c = {a: cls3(o) for a, o in t1.items()}
    print("\n== T1 / T1D, the H21 choice task (+1/0 without D, +1/0/0 with D) ==")
    for a, o in t1.items():
        V, N, Z = (c[a] == 0), (c[a] == 1), (c[a] == 2); k, pt, lo, hi = interval("P", V)
        print(f"   [T1 {a} {o['cls']} values {o['vals']}{' D on' if o['d_on'] else ''}] V {int(V.sum())} N {int(N.sum())} tie {int(Z.sum())}; P(V) {pt:.3f} [{lo:.3f}, {hi:.3f}];"
              f" lost rows {int(lost_t1(o).sum())}; wall contacts per row {o['contacts'].mean():.3f}; {cells_line(o, c[a])}")
    vab = v_absent(t1["Agent16 D off"])
    print(f"      rows with V ever absent (Agent16 D off, H27 reading R7) {int(vab.sum())}; the rule acts (Agent16 D on) in {int(t1['Agent16 D on']['ACT'].any(0).sum())} rows")
    print("\n== W1 / W1D, the absent-odour world (valued column masked from step 0) ==")
    s = {a: w1sum(res[("W1", a)]) for a in W1SHOW}
    for a in W1SHOW:
        o = res[("W1", a)]; f1 = first_true(o["NAV"]); fd = (o["H"] == 2).any(0) if o["nch"] == 3 else np.zeros(R, bool)
        print(f"   [W1 {a} {o['cls']}] dwell at B mean {s[a]['dwell'].mean():.3f} (quartiles {q3(s[a]['dwell'])}); reach {int(s[a]['reach'].sum())}/{R}; lost rows {int(s[a]['lost'].sum())};"
              f" wall contacts per row {s[a]['contacts'].mean():.3f}; first surge step {qq(f1)}; rows forming a D hold {int(fd.sum())}; D whiffs per row {wd(o).sum(0).mean():.2f}")
    nb = ~wb(res[("W1", "Agent16 D off")])[:PR].any(0)
    print(f"      rows with no B whiff on steps 0-{PR - 1} (the population no rule of the odours' own streams reaches, design 2.4) {int(nb.sum())}; of them lost in Agent16 D on"
          f" {int((nb & s['Agent16 D on']['lost']).sum())}; lost rows of Agent16 D on outside them {int((~nb & s['Agent16 D on']['lost']).sum())}")
    print("\n== T3a / T3aD, the constructed loss (REPORTED) ==")
    T3A = ("Agent16 D on", "Agent16 D off", "Agent15 D on", "Agent14N2", "hold-not-read D on")
    D3 = {a: t3_dwell(res[("T3a", a)], 100, T) for a in T3A}
    for a in T3A:
        o = res[("T3a", a)]; end = first_true(o["H"] != o["good"][None, :])
        print(f"   [T3a {a} {o['cls']}] neutral dwell 100-599 mean {D3[a].mean():.3f} (quartiles {q3(D3[a])}); valued hold end step {qq(end)}")
    print("\n== T4, +1/-1 (World7; Agent16 +1/-1/0 with D; REPORTED, outside the verdict) ==")
    for a in ("Agent14N2", "Agent16 D on"):
        o = res[("T4", a)]; cc = cls3(o); V = cc == 0; k, pt, lo, hi = interval("P", V)
        print(f"   [T4 {a} {o['cls']} values {o['vals']}] V {int(V.sum())} N {int((cc == 1).sum())} tie {int((cc == 2).sum())}; P(V) {pt:.3f} [{lo:.3f}, {hi:.3f}]; lost rows"
              f" (no whiff of either plume in the last third) {int(lost_t1(o).sum())}; wall contacts per row {o['contacts'].mean():.3f}; flee violations {o['viol']} of {o['neg']}"
              f" negatively-held (row, step); dwell at the negative source mean {o['dwell'][np.arange(R), 1 - o['good']].mean():.3f}")
    _, t4dp, t4lo, t4hi = interval("DP", (cls3(res[("T4", "Agent16 D on")]) == 0).astype(float), (cls3(res[("T4", "Agent14N2")]) == 0).astype(float))
    print(f"      reported: paired DP P(V) Agent16 D on - Agent14N2 at +1/-1 {t4dp:+.4f} [{t4lo:+.4f}, {t4hi:+.4f}]")
    judge(mode, res, t1, c, s, D3)


def judge(mode, res, t1, c, s, D3):
    ok = lambda z: "PASS" if z else "FAIL"
    print("\n== criteria (design v2 FINAL section 7; 95 percent, one evaluation, no extension; PASS if every part passes, FAIL if any fails, else INCONCLUSIVE; the unrounded bound decides) ==")
    m1 = []
    for a in ("neutral", "pathway-off", "known-answer"):
        z = c[a] == 2; m1.append(ok(z.mean() <= 0.20)); print(f"   M1(a) {a}: ties {int(z.sum())}/{R} = {z.mean():.3f}  at most 0.20 -> {m1[-1]}")
    o = t1["neutral"]; V, N, Z = (c["neutral"] == 0), (c["neutral"] == 1), (c["neutral"] == 2); which = np.where(V, o["good"], np.where(N, 1 - o["good"], -1))
    m1.append(crit("M1(b) neutral, P(+y source majority | chose)", "P", (0.35, 0.65), False, (which == o["plus_y"])[~Z]))
    V, Z = (c["pathway-off"] == 0), (c["pathway-off"] == 2); m1.append(crit("M1(c) floor: pathway-off, P(V | chose)", "P", (0.35, 0.65), False, V[~Z]))
    m1.append(crit("M1(d) ceiling: known-answer, P(V) over all rows", "P", 0.85, False, c["known-answer"] == 0))
    M1 = agg(m1); print(f"   M1 -> {M1}{'' if M1 == 'PASS' else '  (the run is UNREADABLE under section 8)'}")
    z = c["neutral D on"] == 2; Vn = c["neutral D on"] == 0
    print(f"      reported: Agent16 at 0/0/0 with D (the rule acts in value ties) ties {int(z.sum())}; P(V | chose) {Vn[~z].mean() if (~z).any() else float('nan'):.3f}")
    ties = {a: float((c[a] == 2).mean()) for a in ("Agent16 D on", "Agent16 D off")}
    print("   section 8: ties in Agent16 " + ", ".join(f"{a} {v:.3f}" for a, v in ties.items()) + " (unreadable above 0.20)")
    Von, Voff, Vg, V15 = (c["Agent16 D on"] == 0), (c["Agent16 D off"] == 0), (c["Agent15g D on"] == 0), (c["Agent15 D on"] == 0)
    k2, p2, l2, h2 = interval("P", Von)
    print(f"   M2(a) REPORTED, not a gate: Agent16 D on P(V) {k2}/{R} = {p2:.3f} [{l2:.3f}, {h2:.3f}] against 0.88 -> {'lower bound >= 0.88' if l2 >= 0.88 else 'lower bound < 0.88'} (reported)")
    m2 = [crit("M2(b) DP = P(V) Agent16 D on - Agent16 D off, same rows", "DP", -0.05, False, Von.astype(float), Voff.astype(float)),
          crit("M2(c) DP = P(V) Agent16 D on - Agent15g D on, same rows", "DP", 0.05, False, Von.astype(float), Vg.astype(float))]
    M2 = agg(m2); print(f"   M2 -> {M2}")
    _, dpd, lod, hid = interval("DP", Von.astype(float), V15.astype(float))
    print(f"   M2(d) REPORTED: DP P(V) Agent16 D on - Agent15 D on (the rule's gain over H27's agent) {dpd:+.4f} [{lod:+.4f}, {hid:+.4f}]")
    for lab in ("Agent14N2", "hold-not-read D on"):
        _, dp, lo, hi = interval("DP", Von.astype(float), (c[lab] == 0).astype(float)); print(f"      reported: DP Agent16 D on - {lab} {dp:+.4f} [{lo:+.4f}, {hi:+.4f}]")
    print(f"      where the value goes: into V {int((Von & ~Voff).sum())}, out of V {int((~Von & Voff).sum())}; rows with V ever absent (Agent16 D off) {int(v_absent(t1['Agent16 D off']).sum())}")
    lines = []; ids = identities(res, lines.append)
    for ln in lines: print("      " + ln)
    M3 = ok(all(ids.values())); print(f"   M3 identities (I1')-(I6') on the task seeds: failed {[k for k, v in ids.items() if not v]} -> {M3}")
    blines = []; v4, bo, _ = bench(say=blines.append); M4 = ok(v4)
    m4line = [ln for ln in blines if ln.startswith("== M4")]
    rec = [ln.rstrip("\n") for ln in open(BENCH_TXT, encoding="utf-8")] if os.path.exists(BENCH_TXT) else []
    rec4 = [ln for ln in rec if ln.startswith("== M4")]
    for ln in blines:
        if ln.startswith("== M4") or "STOP RULE" in ln: print("      " + ln.strip())
    print(f"   M4 mechanism bench, re-run here on the bench seeds (reading R13) -> {M4}; its M4 line equals ph33_bench.txt's: {m4line == rec4}")
    s_on, s_15, s_off = s["Agent16 D on"], s["Agent15 D on"], s["Agent16 D off"]
    m5 = [crit("M5(a') W1D lost rows (no B whiff in 400-599), DP Agent16 D on - Agent15 D on, same rows", "DP", -0.20, True, s_on["lost"].astype(float), s_15["lost"].astype(float))]
    M5 = agg(m5); print(f"   M5 -> {M5}      lost rows Agent16 D on {int(s_on['lost'].sum())}, Agent15 D on {int(s_15['lost'].sum())}, Agent16 D off {int(s_off['lost'].sum())}")
    print("   H27's W1D bars against D off, REPORTED (no bar in this verdict; reading R10; bar_W from this run's bench re-run):")
    k5, p5, l5, h5 = interval("P", s_on["reach"])
    print(f"      (a) reach within 3.0 of B by 600 {k5}/{R} = {p5:.3f} [{l5:.3f}, {h5:.3f}] against 0.80 -> {'at least' if l5 >= 0.80 else 'below'} (reported)")
    _, m5b, lb5, hb5 = interval("DP", s_on["dwell"], s_off["dwell"])
    print(f"      (b) paired dwell at B Agent16 D on - D off {m5b:+.3f} [{lb5:+.3f}, {hb5:+.3f}] against bar_W {bo['bar_W']:+.1f} (bench D_off {bo['D_off']:.4f}) ->"
          f" {'lower bound at or above' if lb5 >= bo['bar_W'] else 'lower bound below'} (reported)")
    cm = s_on["contacts"].mean(); print(f"      (c) wall contacts per row {cm:.3f} against 0.10 (reported)")
    _, dl, ll, hl = interval("DP", s_on["lost"].astype(float), s_off["lost"].astype(float))
    print(f"      (d) lost-row DP Agent16 D on - D off {dl:+.4f} [{ll:+.4f}, {hl:+.4f}] against +0.05 -> {'upper bound at or below' if hl <= 0.05 else 'upper bound above'} (reported)")
    print(f"      dwell means: Agent16 D on {s_on['dwell'].mean():.3f} / D off {s_off['dwell'].mean():.3f} / Agent15 D on {s_15['dwell'].mean():.3f} / hold-not-read D on"
          f" {s['hold-not-read D on']['dwell'].mean():.3f} / release-off D on {s['release-off D on']['dwell'].mean():.3f} / Agent15g D on {s['Agent15g D on']['dwell'].mean():.3f}")
    _, d6, l6, h6 = interval("DP", s["hold-not-read D on"]["lost"].astype(float), s_on["lost"].astype(float))
    print(f"   M6 REPORTED: the hold's benefit, W1D lost-row DP hold-not-read D on - Agent16 D on {d6:+.4f} [{l6:+.4f}, {h6:+.4f}] (lost {int(s['hold-not-read D on']['lost'].sum())}"
          f" vs {int(s_on['lost'].sum())})")
    _, dr, lr, hr_ = interval("DP", s["release-off D on"]["lost"].astype(float), s_on["lost"].astype(float))
    print(f"      reported: release-off D on - Agent16 D on lost-row DP {dr:+.4f} [{lr:+.4f}, {hr_:+.4f}]; Agent15g D on lost {int(s['Agent15g D on']['lost'].sum())}")
    print(f"   M7 T3aD (REPORTED): neutral dwell 100-599 " + ", ".join(f"{a} {D3[a].mean():.3f}" for a in D3))
    print("   M8 T4 (REPORTED): printed above")
    unread = M1 != "PASS" or max(ties.values()) > 0.20 or M3 != "PASS" or M4 != "PASS" or "UNREADABLE" in (M2, M5)
    verdict = all(x == "PASS" for x in (M1, M2, M3, M4, M5)); fail = any(x == "FAIL" for x in (M2, M5))
    lab = "PASS" if verdict else "UNREADABLE" if unread and not fail else "FAIL" if fail else "INCONCLUSIVE"
    print(f"\n== H28 ==  M1 {M1}  M2 {M2}  M3 {M3}  M4 {M4}  M5(a') {M5}  (M2(a), M2(d), H27's W1D bars, M6, M7 T3aD, M8 T4 reported) -> {lab}: "
          + ("with a ubiquitous, never-reinforced odour arriving as background whiffs at p_D 0.03, the adopted agent whose value ties are ranked by the recency of each"
             " odour's last burst (three whiffs within 10 steps) keeps its choice in the H21 task within 0.05 of itself without the distractor, and in the absent-odour world"
             " loses at least 20 points fewer rows than the same agent without the ranking" if verdict else
             "UNREADABLE (section 8)" if lab == "UNREADABLE" else "NOT shown under the registered criteria"))


if __name__ == "__main__":
    mode = ([m for m in sys.argv[1:] if m in ("demo", "bench", "dev", "eval")] or ["demo"])[0]
    if mode == "demo": demo(); sys.exit(0)
    if mode == "bench":
        v, o, _ = bench(); sys.exit(0 if v and not o["stop"] else 3 if v else 1)
    main(mode)
