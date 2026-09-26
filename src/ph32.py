#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H27: a third, irrelevant odour D (value 0, background whiffs at p_D 0.03) on the adopted agent composed with three channels.

Usage: python ph32.py demo | bench | dev | eval

Design: H27 design v2 FINAL, doc d8c8949f2896cf1ec, sha256 88fdfdf7...7ddb (experiments/h27/h27_design_v2.md), opened by
decision:h27-open (owner, 2026-09-25, '권고안으로 이어서 진행', gloss 'continue with the recommended options': every recommended
option of design v1 section 12 confirmed). Signed before this file existed, H14 format, H27 only:
decision:evidence-release-composition-rule-h27 (the evidence release compares the held channel with the strongest non-held
channel; identical at N 2) and decision:classification-rule-relaxed-presence-prior-h27 (the H26 relaxation re-signed in form for
one presence counter per odour, the third odour D included). The adopted agent is Agent14N2 = ph30.ReleaseN2 + ph28.Agent14
(decision:n2-release-adopted-within-tested-conditions).

Composition only; NO adopted file is edited. ph2, ph11, ph14, ph16, ph17, ph22, ph23, ph24, ph28, ph30 are imported unchanged (their
sha256 is printed in every output header and ph23, ph24, ph28, ph30 are checked against the recorded versions). The six two-channel
sites the design cites are handled here, by composition or override:
  ph11.py:112 (Upstream chans 2)      -> Agent15.__init__ rebuilds the stage with chans 3 after the adopted constructor ran
  ph11.py:113 (Circuit n 2)           -> Agent15.__init__ rebuilds it as Circuit3, n 3 (the third unit's noise on its own generator)
  ph11.py:116 (two odour codes)       -> Agent15.__init__ appends odour(103) (ph8.MB4.odour draws from its own seed; unused here)
  ph14.py:55  (learned read-out, 2)   -> not reached: values are supplied (`known` of width 3 is returned by ph14.py:53)
  ph23.py:57  (counter shape (R, 2))  -> Agent15.__init__ sets the counter to (R, 3) at N_hi - P = 240 (ph28.py:97's value)
  ph23.py:68  (`other = 1 - hi`)      -> Act15.act, Agent9.act (ph23.py:60-104) repeated with that line replaced by evidence_due()
  ph28.py:97  (counter start (R, 2))  -> as ph23.py:57 above
Method order: Agent15(ReleaseN2, Agent14, Act15) -> MRO Agent15, ReleaseN2, Agent14, Release, Act15, Agent9, ...; ReleaseN2.act's
`super(Release, self).act` therefore reaches Act15.act, which stands where Agent9.act stood (checked in the demo).

Readings where the design is silent, chosen so that the identities stay exact (printed again in every output header):
 (R1) The D stream: each step, after the world's own sense and wind draws, D = u < p_D with u from numpy default_rng(world seed +
      30000), one uniform per row per step, drawn in every arm (p_D 0 in the D-off arms, so D is never True there). The plume
      columns come from the world unchanged (World7, or ph22.Masked checked against its World7 twin every step).
 (R2) Circuit3 draws the first two units' noise as standard_normal((R, 2)) from the agent's shared generator (the values and order
      of ph2.py:40 at n 2) and the third unit's as standard_normal((R, 1)) from default_rng(agent seed + 30000); the step is ph2.py:33-41
      otherwise, term for term.
 (R3) evidence_due: other = argmax over the non-held channels of y (the held column set to -inf); at N 2 this is 1 - hi exactly, so
      y[rows, other] - y[rows, hi] is the same float (identity (I1)).
 (R4) The hold-not-read arm (design section 6): the circuit, gate, evidence release and the release wrapper run on the circuit's hold
      (the act returns the circuit's hold, so ReleaseN2's (S) and (Z) read it); val, hit, keep, vh, nav's held clause, nav6/nav8 and the
      counter's held clause read hr = where(max y > 0.05, argmax y, -1) with y the act's own y (gain and gate applied, ph23.py:62-66),
      the form of ph14.py:62-63. `hit` also drives the base act's silence clock (ph23.py:96), as it is the same variable there. In W1
      the valued column is zero and the gate never masks at equal values, so there y equals the ungated, unbiased stage output.
 (R5) 'Trajectory fields' (I3)-(I5): POS, HEAD, NAV, SINCE, TURN, EST and W for V and B (W[:, :, :2]); 'every field' (I1), (I2): those
      plus TGT, S, SG, H, SIL, TO, EV, SUS, Z, C2, P2, PRES, NAV6, NAV8, DIFF8, VAL, AT2, C and W (all columns; in (I2) the D column is
      left out, since it is the input that differs, and the measurement-only argmax HR is added; Agent14N2 has no HR, so (I1) leaves it out).
 (R6) (I2) compares D on and D off per row on every step before that row's first D whiff (the step whose act first receives D).
 (R7) (I5)'s population: T1 rows in which V is present by its counter on every step of the D-off run (c_V < 300 throughout, i.e. a V
      whiff by step 58 and no V silence of 300 steps); (m) counts the complement ('V ever absent').
 (R8) (I6), read as the navigation law exact by code (design 2.2: with B held a D whiff does not steer, so the literal 'first surge =
      first B or D whiff at or after 59' can fail in rows holding B or D at that whiff): nav False on steps 0-58, and on every step
      >= 59 nav == (held odour in {B, D} ? its whiff : any B or D whiff), the held odour being the arm's own read hold (H, or HR in the
      hold-not-read arm); no flee (no step with a negatively valued read hold). The literal first-surge count is printed beside it.
 (R9) Bench (b2) keeps the release on (Agent15 as adopted), so a silent constructed hold is ended by the release near step 47 whatever
      D does; rows holding at 200 and the hold's end step are printed. Reported, no bar (design section 4).
 (R10) Bench (c): exact checks on constructed states through the act itself (Still stub): top/nav law and presence for every
      combination of whiffs (2^3), held channel (none, V, B, D) and V present/absent; the gate's mask (the gated y equal to the ungated
      agent's y times the expected mask, one step, same construction); the three counters' recursion from 240 and presence; (S)/(Z) on
      a D hold: a constructed D hold with one D whiff at step 0 ends at step 48 with every unit <= 1.0, and the counter is 0 on every
      step a D hold forms from whiffs.
 (R11) Bench (d): D's whiff fraction over the T1D Agent15 run's (row, step) pairs: p_D inside its Wilson 95 percent interval; D
      fraction on (row, step) pairs sensed inside either plume cone (or within 3.0 of a source) and outside: the two Wilson intervals
      overlap.
 (R12) M5(b)'s bar: bar_W = -0.20 x D_off rounded to 0.1 (the H26 rule, decision:h26-t2-dwell-bar's rounding), D_off Agent15's mean
      W1 dwell without D at the bench; (hW) reads M5(b) by ph23.pass_prob at that bar and M5(d) by the DP formula.
 (R13) Pass probabilities (design section 7): a paired DP with b the discordant fraction, sd = sqrt(b - DP^2), se = sd / 20 (ph28.pp_dp);
      a paired mean by ph23.pass_prob (se = sd / 20); M2(a)'s binomial P(K >= 365 of 400) printed, reported.
 (R14) M1's arms are H26's (two channels, no D): neutral = Agent14N2 at 0/0 (identical to H26's Agent14 at non-negative values by
      ph30.py:128-132), pathway-off = ph24.Agent8 at G 0, gate off, filter off (H26's reading R9), known-answer = ph17.Agent5 with the
      valued odour fixed, G 0. The three-channel versions with D: pathway-off = Agent15 at G 0, gate off, filter off, release off (the
      same act as Agent8's with the filter off); neutral = Agent15 at 0/0/0.
 (R15) Agent15g (the filter-off arm) = Agent15 with filt False: nav is ph23.py:90's nav6 line; gain, gate, counter and N2 release as
      Agent15. The release-off arm = Agent15 with release False.
 (R16) dev and eval re-run the bench on the bench seeds for M4 (as H26 did, its reading R11) and print whether its M4 line equals the
      line in experiments/h27/ph32_bench.txt.
 (R17) Arms run in parallel processes (fork); each arm builds its own generators from the seeds; the demo checks that a parallel result
      equals a sequential one bitwise.
Seed scan (design section 9): every file under the repository except by name ph32.py, ph32_*.txt, h27_*.md, master_plan.md, notes/*.md,
viewer/*, and the (file, number) pair of decision:seed-scan-exclusion-ph31-eval (experiments/h20/ph31_eval.txt with Stage C Run 1's E1
evaluation agent seed, taken from ph30's seed constants, not written here). BARS is filled after the bench by decision:h27-w1d-dwell-bar
(the registered order, not an amendment); dev and eval refuse to run while it is unset. Nothing changes after the table.
"""
import sys, os, re, math, hashlib
import multiprocessing as mp
import numpy as np
import ph30                                              # Agent14N2; imports ph28 (Agent14; hooks ph24.make / ph23.make) and sets its own statistics
import ph2, ph11, ph14, ph15, ph16, ph17, ph18, ph22, ph23, ph24, ph25, ph28
from ph2 import Upstream, Circuit
from ph9 import UPWIND, CAST_PERIOD, MAXOFF, GAIN, MAXTURN, TURN_NOISE, W0, SLOPE, LMAX, angdiff
from ph11 import RESET_AFTER, MARGIN
from ph12 import SAT
from ph16 import World7, Still, cast_draw, interval, crit, R, T
from ph17 import Agent5
from ph18 import majority, agg
from ph21 import G_STAR, q3, first_true
from ph23 import Agent9, pass_prob
from ph24 import Release, Agent8
from ph28 import Agent14, pp_dp, Phi
from ph30 import ReleaseN2, Agent14N2
from ffcore import sigmoid

sys.stdout.reconfigure(newline="\n")            # LF output, so the recorded sha256 equals the committed blob
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
DESIGN = "H27 v2 FINAL doc d8c8949f2896cf1ec hash 88fdfdf7a68c4a8d254bd505ac8aaea0f1e2a2697b68fc105701fda9940c7ddb"
RECORDED = dict(ph23="ae180492", ph24="f344f178", ph28="64ce7d0c", ph30="98822834")   # sha256 prefixes cited by the design (HEAD 8c50e9f)
P_D, P_PRIOR, N_HI = 0.03, ph28.P_PRIOR, ph28.N_HI
PR = P_PRIOR - 1                                 # 59: first step on which a never-sensed odour is absent
SEEDS = dict(dev=(9937, 9947), eval=(2083, 2173))
BENCH = dict(rows=400, steps=600, seed_w=20261121, seed_a=20261122, boot=20261123, steps_b1=40, steps_b2=200, steps_c=100)
BS = (BENCH["seed_w"], BENCH["seed_a"])
D_OFF, A3_OFF = 30_000, 30_000                    # world + 30000: the D generator; agent + 30000: the third unit's noise
ph30.set_stats(ph30.Z95, ph30.QLO95, ph30.QHI95, BENCH["boot"])      # design section 7: 95 percent, bootstrap 20261123 (after the imports)
# ---- bar constant: filled from bench (hW) by decision:h27-w1d-dwell-bar (registered order) ----
BARS = dict(W=None)                             # bar_W = -0.20 x D_off rounded to 0.1 (M5 b)
# ----
MODS = (ph2, ph11, ph14, ph15, ph16, ph17, ph22, ph23, ph24, ph25, ph28, ph30)
NPROC = int(os.environ.get("PH32_PROCS", "4"))
BENCH_TXT = os.path.join(REPO, "experiments", "h27", "ph32_bench.txt")
V_ = 0                                           # read-out order of `known` columns is (world column 0, world column 1, D); V is `good`


def sha(p=__file__): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def qq(x): x = np.asarray(x); return q3(x[x >= 0]) + f" (rows {int((x >= 0).sum())})"


# ------------------------------------------------------------------ the change (design 3.2, 3.3)
class Circuit3(Circuit):
    """ph2.Circuit (ph2.py:19-42) with the noise of units 3.. on a separate generator (reading R2); n 2 draws exactly as ph2.py:40"""

    def __init__(self, runs, rng3=None, **kw):
        super().__init__(runs, **kw); self.rng3 = rng3

    def step(self, y, reset=0.0):
        q = self.pool_c*np.maximum(self.s, 0.0)**self.pool_p
        pool = q.sum(1, keepdims=True) + reset
        if self.gsat is not None:
            Smax, kappa = self.gsat
            pool = Smax*pool/(kappa + pool)
        self.S += (self.DT/self.tau_g)*(-self.S + pool)
        z = self.rng.standard_normal((self.R, 2))
        if self.n > 2: z = np.concatenate([z, self.rng3.standard_normal((self.R, self.n - 2))], 1)
        u = (y + self.g*sigmoid(self.k*(self.s - self.theta)) + self.w_i*q - self.w_i*self.S + self.noise*z)
        self.s += (self.DT/self.tau)*(-self.s + np.clip(u, 0, self.S_MAX))
        return self.s


def evidence_due(y, hp):
    """decision:evidence-release-composition-rule-h27: committed & (max over j != hi of y_j - y_hi > MARGIN); reading R3"""
    rows = np.arange(len(hp)); committed = hp >= 0; hi = np.maximum(hp, 0)
    yo = y.copy(); yo[rows, hi] = -np.inf; other = yo.argmax(1)
    return committed & ((y[rows, other] - y[rows, hi]) > MARGIN)


class Act15(Agent9):
    """ph23.Agent9.act (ph23.py:60-104) with ONE line replaced: `other = 1 - hi` (ph23.py:68, :70) by evidence_due(). hold_read False:
    the hold-not-read arm (reading R4)."""

    hold_read = True

    def act(self, w, whiffs, wind_on):
        rows = np.arange(self.R)
        y = self.up.step(whiffs.astype(float))*(1.0 + self.G*np.maximum(self.chan_valence(), 0.0))   # H20: the gain
        hp = self.held()
        if self.rule:                                                                                 # H21: the gate
            v = self.chan_valence(); vh = v[rows, np.maximum(hp, 0)]
            y = y*~((hp >= 0)[:, None] & (v >= 0.0) & (v < vh[:, None]))
        self.yp = y
        self.due_timeout = self.silence > RESET_AFTER
        self.due_evidence = evidence_due(y, hp)                                                      # H27: the composition rule
        due = self.due_timeout | self.due_evidence
        rst = np.where(due, 10.0, 0.0)[:, None]
        self.silence = np.where(due, 0.0, self.silence)
        self.sel.step(y, reset=rst)
        h = self.held()
        self.hr = np.where(y.max(1) > 0.05, y.argmax(1), -1)                                          # reading R4 (measurement in every arm)
        hh = h if self.hold_read else self.hr
        est = self.est = self.estimate(w, wind_on)
        val = np.where(hh >= 0, self.known[rows, np.maximum(hh, 0)], 0.0)
        hit = np.where(hh >= 0, whiffs[rows, np.maximum(hh, 0)], False)
        v = self.chan_valence(); vh = v[rows, np.maximum(hh, 0)]
        top8 = (v >= 0) & (v == v.max(1)[:, None])
        self.nav8 = np.where((hh >= 0) & ((vh == v.max(1)) | (vh < 0)), hit, (whiffs & top8).any(1))
        if self.scope == "prior":
            self.c = np.where(whiffs, 0.0, self.c + 1.0)
            held = np.zeros_like(whiffs); held[rows, np.maximum(hh, 0)] = hh >= 0
            self.present = (self.c < self.N) | held
        else:
            self.present = np.ones_like(whiffs)
        vmax = np.where(self.present, v, -np.inf).max(1)
        top = self.present & (v >= 0) & (v == vmax[:, None])
        self.nav6 = hit | ((hh < 0) & (whiffs & (v >= 0)).any(1))
        keep = (hh >= 0) & ((vh == vmax) | (vh < 0))
        nav = np.where(keep, hit, (whiffs & top).any(1)) if self.filt else self.nav6
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
        return turn, h


class Agent15(ReleaseN2, Agent14, Act15):
    """Agent14N2 with N channels (design 3.2 (A)): the adopted constructor runs first (every draw of the agent's generator unchanged),
    then the stage, the circuit, the codes and the counter are rebuilt for nch 3. nch 2: nothing rebuilt (identity (I1))."""

    def __init__(self, runs, rng, rng3=None, nch=3, hold_read=True, **kw):
        super().__init__(runs, rng, **kw)
        self.nch, self.hold_read = nch, hold_read; self.hr = np.full(runs, -1); self.val = np.zeros(runs)
        if nch == 3:
            self.up = Upstream(n=1.5, sig=0.05, Rmax=1.8, k=0.8, runs=runs, chans=3)                  # ph11.py:112 with chans 3
            self.sel = Circuit3(runs, rng3=rng3, n=3, theta=1.0, k=12.0, noise=0.01, rng=rng)         # ph11.py:113 with n 3
            self.codes = np.concatenate([self.codes, self.mb.odour(103)[:, None, :]], 1)              # ph11.py:116 plus odour(103)
            self.c = np.full((runs, 3), float(self.N_hi - self.P))                                     # ph28.py:97 with 3 columns
            self.present = np.ones((runs, 3), bool); self.yp = np.zeros((runs, 3))


# ------------------------------------------------------------------ arms (design section 6)
#   name: (kind, nch, D on)          kind: A15 | A15g | A15hnr | A15ro | A15po | A15n2 | A14N2 | A8po | A5ka
ARMS = {"Agent15 D on": ("A15", 3, True), "Agent15 D off": ("A15", 3, False), "Agent14N2": ("A14N2", 2, False),
        "Agent15g D on": ("A15g", 3, True), "hold-not-read D on": ("A15hnr", 3, True), "hold-not-read D off": ("A15hnr", 3, False),
        "release-off D on": ("A15ro", 3, True), "Agent15 at N 2": ("A15n2", 2, False), "pathway-off": ("A8po", 2, False),
        "known-answer": ("A5ka", 2, False), "neutral": ("A14N2", 2, False), "pathway-off D on": ("A15po", 3, True),
        "neutral D on": ("A15", 3, True)}


def kv_of(vals, g, nch):
    n = len(g); r = np.arange(n); kv = np.zeros((n, nch)); kv[r, g] = vals[0]; kv[r, 1 - g] = vals[1]
    if nch == 3: kv[:, 2] = vals[2] if len(vals) > 2 else 0.0
    return kv


def build(kind, runs, seed_a, g, kv):
    rng = np.random.default_rng(seed_a); rng3 = np.random.default_rng(seed_a + A3_OFF)
    base = dict(P=P_PRIOR, N_hi=N_HI, G=G_STAR, known=kv, rule=True, filt=True, scope="prior", release=True)
    if kind == "A14N2": return Agent14N2(runs, rng, **base)
    if kind == "A8po": return Agent8(runs, rng, G=0.0, known=kv, rule=False, filt=False)
    if kind == "A5ka": return Agent5(runs, rng, fixed=g.copy(), G=0.0, known=kv)
    kw = dict(base)
    if kind == "A15g": kw["filt"] = False
    if kind == "A15ro": kw["release"] = False
    if kind == "A15po": kw.update(G=0.0, rule=False, filt=False, release=False)
    return Agent15(runs, rng, rng3=rng3, nch=2 if kind == "A15n2" else 3, hold_read=kind != "A15hnr", **kw)


FLOATS = ("SIL", "SINCE", "TGT", "TURN", "EST", "SG")
BOOLS = ("NAV", "TO", "EV", "SUS", "Z", "PRES", "NAV6", "NAV8", "DIFF8", "C", "CONE")


def blank(steps, runs, nch):
    o = {k: np.zeros((steps, runs)) for k in FLOATS}
    o.update({k: np.zeros((steps, runs), bool) for k in BOOLS})
    o.update(H=np.full((steps, runs), -1, np.int8), HR=np.full((steps, runs), -1, np.int8), W=np.zeros((steps, runs, 3), bool),
             S=np.zeros((steps, runs, nch)), C2=np.zeros((steps, runs, nch), np.float32), P2=np.ones((steps, runs, nch), bool),
             POS=np.zeros((steps, runs, 2)), HEAD=np.zeros((steps, runs)), AT2=np.zeros((steps, runs, 2), bool), VAL=np.zeros((steps, runs)))
    return o


def record(o, t, a, h, x, turn, g):
    rows = np.arange(len(h))
    o["H"][t] = h; o["HR"][t] = getattr(a, "hr", h); o["NAV"][t] = a.nav_hit; o["TO"][t] = a.due_timeout; o["EV"][t] = a.due_evidence
    o["SUS"][t] = getattr(a, "sustain", False); o["Z"][t] = getattr(a, "zreset", False); o["SIL"][t] = a.silence; o["SINCE"][t] = a.since
    o["TGT"][t] = getattr(a, "tgt", 0.0); o["TURN"][t] = turn; o["EST"][t] = getattr(a, "est", 0.0); o["S"][t] = a.sel.s; o["SG"][t] = a.sel.S[:, 0]
    o["NAV6"][t] = getattr(a, "nav6", a.nav_hit); o["NAV8"][t] = getattr(a, "nav8", a.nav_hit); o["DIFF8"][t] = getattr(a, "differs8", False)
    if isinstance(a, Agent9): o["C2"][t] = a.c; o["P2"][t] = a.present; o["PRES"][t] = a.present[rows, g]
    hh = h if getattr(a, "hold_read", True) or not hasattr(a, "hr") else a.hr
    o["VAL"][t] = np.where(hh >= 0, a.known[rows, np.maximum(hh, 0)], 0.0)
    o["W"][t, :, :x.shape[1]] = x


def cone_of(w, pos):
    """inside either plume cone, or within 3.0 of a source (World2.sense's geometry, ph11.py:78-81), at the sensing position"""
    out = np.zeros(len(pos), bool)
    for k in (0, 1):
        da = pos[:, 0] - w.src[:, k, 0]; dc = np.abs(pos[:, 1] - w.src[:, k, 1])
        out |= ((da > 0) & (da < LMAX) & (dc < W0 + SLOPE*da)) | (np.linalg.norm(pos - w.src[:, k], axis=1) < 3.0)
    return out


def run(world, arm, vals, seeds, runs=R, steps=T):
    """world 'T1' (World7), 'W1' (ph22.Masked, valued column False from step 0), 'T3a' (W1's world, start at the valued source, valued
    hold s 2.0 constructed). Construction order as ph24.run: world, mask, twin, values, agent, cast draw, position, hold (reading R1)."""
    kind, nch, d_on = ARMS[arm]; masked = world != "T1"
    w = (ph22.Masked if masked else World7)(runs, np.random.default_rng(seeds[0]), seeds[0])
    rows = np.arange(runs); g = w.good; neutral = 1 - g
    if masked: w.pres = neutral.copy(); w.absent = g.copy()
    tw = World7(runs, np.random.default_rng(seeds[0]), seeds[0]) if masked else None
    rngD = np.random.default_rng(seeds[0] + D_OFF); pD = P_D if d_on else 0.0
    kv = kv_of(vals, g, nch); a = build(kind, runs, seeds[1], g, kv)
    a.cast_sign = cast_draw(seeds[1], runs)
    if world == "T3a": w.pos = w.src[rows, g].copy(); a.sel.s[rows, g] = 2.0
    o = dict(world=world, arm=arm, cls=type(a).__name__, vals=tuple(vals), d_on=d_on, nch=nch, good=g, cell=w.cell, plus_y=w.plus_y, src=w.src.copy(),
             steps=steps, start=w.pos.copy(), s0=a.sel.s.copy(), H0=a.held(), draws_equal=True, rng_equal=True, viol=0, neg=0, **blank(steps, runs, nch))
    for t in range(steps):
        if masked: tw.pos, tw.head = w.pos.copy(), w.head.copy()
        ps = w.pos.copy(); base = w.sense(); on = w.wind_on(); dw = rngD.random(runs) < pD
        if masked:
            tr = tw.sense()
            o["draws_equal"] &= bool(np.array_equal(tr, w.raw) and np.array_equal(on, tw.wind_on()) and np.array_equal(base[rows, neutral], tr[rows, neutral])
                                     and not base[rows, g].any())
        x = np.concatenate([base, dw[:, None]], 1) if nch == 3 else base
        turn, h = a.act(w, x, on)
        record(o, t, a, h, x, turn, g); o["W"][t, :, 2] = dw; o["CONE"][t] = cone_of(w, ps)
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


def runs_of(specs, keys):
    return dict(zip(keys, pool_run(specs)))


def stub(kind, known, sched, hold=None, rows=BENCH["rows"], seeds=BS, nch=3, pre=None):
    """ph16.Still stub (as ph24.stub): sched = list of (steps, p per channel); the same uniform draws for every condition; hold: channel set
    to s 2.0; pre(a): optional constructed state set after construction"""
    steps = sum(s for s, _ in sched); u = np.random.default_rng(seeds[0]).random((steps, rows, nch))
    g = np.zeros(rows, int); kv = np.tile(np.asarray(known, float), (rows, 1))
    a = build(kind, rows, seeds[1], g, kv); w = Still(rows)
    if hold is not None: a.sel.s[:, hold] = 2.0
    if pre is not None: pre(a)
    o = dict(H0=a.held(), steps=steps, **blank(steps, rows, nch)); t = 0
    for n, ps in sched:
        for _ in range(n):
            x = np.stack([u[t, :, k] < ps[k] for k in range(nch)], 1)
            turn, h = a.act(w, x, np.ones(rows, bool)); record(o, t, a, h, x, turn, g); o.setdefault("YP", []).append(a.yp.copy()); t += 1
    o["YP"] = np.array(o["YP"]); return o, a


# ------------------------------------------------------------------ measures
TRAJ = ("POS", "HEAD", "NAV", "SINCE", "TURN", "EST")
EVERY = TRAJ + ("TGT", "S", "SG", "H", "SIL", "TO", "EV", "SUS", "Z", "C2", "P2", "PRES", "NAV6", "NAV8", "DIFF8", "W", "AT2", "C", "VAL")


def rowmask(o1, o2, keys, w2=False):
    """per (step, row): equal on every key (W restricted to V and B columns when w2)"""
    st, n = o1["H"].shape; eq = np.ones((st, n), bool)
    for k in keys:
        a, b = o1[k], o2[k]
        if a.shape != b.shape: return None
        e = (a == b); eq &= e.reshape(st, n, -1).all(2)
    if w2: eq &= (o1["W"][:, :, :2] == o2["W"][:, :, :2]).all(2)
    return eq


def same(o1, o2, keys, w2=False, n=None):
    eq = rowmask(o1, o2, keys, w2)
    return eq is not None and bool(eq[:n].all())


def traj(o1, o2): return same(o1, o2, TRAJ, w2=True)
def every(o1, o2): return same(o1, o2, EVERY)


def wv(o): r = np.arange(len(o["good"])); return o["W"][:, r, o["good"]]
def wb(o): r = np.arange(len(o["good"])); return o["W"][:, r, 1 - o["good"]]
def wd(o): return o["W"][:, :, 2]


def w1sum(o):
    r = np.arange(len(o["good"])); B = 1 - o["good"]; AT = o["AT2"][:, r, B]
    return dict(reach=AT.any(0), dwell=AT.sum(0).astype(float), lost=~o["W"][400:, r, B].any(0), contacts=o["C"].sum(0).astype(float))


def lost_t1(o): return ~o["W"][-T//3:, :, :2].any((0, 2))
def cls3(o): return np.select(list(majority(o)), [0, 1, 2])
def binom_ge(p, k=365, n=400): return float(sum(math.comb(n, j)*p**j*(1 - p)**(n - j) for j in range(k, n + 1)))
def t3_dwell(o, lo, hi): r = np.arange(len(o["good"])); return o["AT2"][lo:hi, r, 1 - o["good"]].sum(0).astype(float)


def v_absent(o):
    """reading R7: V absent by its counter on some step (c_V >= 300); needs a counter-bearing arm"""
    r = np.arange(len(o["good"])); return (o["C2"][:, r, o["good"]] >= N_HI).any(0)


def i2_rows(on, off):
    """reading R6: per row, D on == D off on every field on every step before the row's first D whiff"""
    fd = first_true(wd(on)); st = on["H"].shape[0]; fdx = np.where(fd < 0, st, fd)
    eq = rowmask(on, off, tuple(k for k in EVERY if k != "W") + ("HR",)) & (on["W"][:, :, :2] == off["W"][:, :, :2]).all(2)
    before = np.arange(st)[:, None] < fdx[None, :]
    return (eq | ~before).all(0), fd


def i6_rows(o):
    """reading R8: nav False on 0-58; from 59 nav == (read hold in {B, D} ? its whiff : any B or D whiff); no flee. Returns (exact rows, literal)"""
    g = o["good"]; B = 1 - g; st, n = o["H"].shape; r = np.arange(n); tt = np.arange(st)[:, None]
    hh = o["HR"] if o["arm"].startswith("hold-not-read") else o["H"]
    hh = hh.astype(int); bd = (hh == B[None, :]) | (hh == 2)
    held_w = np.take_along_axis(o["W"], np.maximum(hh, 0)[:, :, None], 2)[:, :, 0]
    anyBD = wb(o) | wd(o)
    law = np.where(bd, held_w, anyBD)
    ok = ~o["NAV"][:PR].any(0) & (o["NAV"][PR:] == law[PR:]).all(0) & (o["VAL"] >= 0).all(0)
    fs = first_true(o["NAV"]); fb = first_true(anyBD & (tt >= PR))
    return ok, fs == fb


def pair_dp(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float); return float(a.mean() - b.mean()), float((a != b).mean())


# ------------------------------------------------------------------ header, readings, seed scan
def seed_numbers():
    w = [SEEDS["dev"][0], SEEDS["eval"][0], BENCH["seed_w"]]; a = [SEEDS["dev"][1], SEEDS["eval"][1], BENCH["seed_a"]]
    base = [*SEEDS["dev"], *SEEDS["eval"], BENCH["seed_w"], BENCH["seed_a"], BENCH["boot"]]
    derived = [s + 10_000 for s in w] + [s + D_OFF for s in w] + [s + 20_000 for s in a] + [s + A3_OFF for s in a]
    extra = [s + 20_000 for s in w] + [BENCH["seed_w"] + 10_000_000, BENCH["seed_a"] + 20_000_000]
    return base + derived + extra


EXCLUDED_PAIRS = {("experiments/h20/ph31_eval.txt", ph30.SEEDS["eval"][0][1])}     # decision:seed-scan-exclusion-ph31-eval (number from ph30)


def seeds_unused():
    """design section 9: none of the 24 numbers appears in any other file under the repository (recursive, digit boundary; .git and
    __pycache__ excluded; excluded by name: ph32.py, ph32_*.txt, h27_*.md, master_plan.md, notes/*.md, viewer/*; and the excluded pair)"""
    nums = seed_numbers(); pat = re.compile(rb"(?<!\d)(" + "|".join(map(str, nums)).encode() + rb")(?!\d)"); hits = []; nf = 0
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        top = os.path.relpath(root, REPO).replace("\\", "/").split("/")[0]
        for f in files:
            if f == "ph32.py" or (f.startswith("ph32_") and f.endswith(".txt")) or (f.startswith("h27_") and f.endswith(".md")) or f == "master_plan.md": continue
            if (os.path.basename(root) == "notes" and f.endswith(".md")) or top == "viewer": continue
            nf += 1; rel = os.path.relpath(os.path.join(root, f), REPO).replace("\\", "/")
            found = {int(m) for m in pat.findall(open(os.path.join(root, f), "rb").read())}
            found -= {n for (p, n) in EXCLUDED_PAIRS if p == rel}
            if found: hits.append((rel, sorted(found)))
    return hits, nums, nf


def header(say=print):
    say(f"   ph32.py sha256 {sha()}; design {DESIGN}")
    say("   imported modules (unchanged): " + "; ".join(f"{os.path.basename(m.__file__)} {sha(m.__file__)}" for m in MODS))
    chk = {k: sha(getattr(sys.modules[k], "__file__")).startswith(v) for k, v in RECORDED.items()}
    say(f"   recorded versions (design's prefixes) {chk}")
    say(f"   seeds: dev {SEEDS['dev']}, eval {SEEDS['eval']}, bench {BS}, bootstrap {BENCH['boot']} (95 percent, 5000); D generator world + {D_OFF}; third-unit noise agent + {A3_OFF};"
        f" demo seeds (5, 6) used deliberately, NOT part of the seed scan; p_D {P_D}; BARS {BARS}")
    say("   seed scan exclusions by name: ph32.py, ph32_*.txt, h27_*.md, master_plan.md, notes/*.md, viewer/*; the (file, number) pair of decision:seed-scan-exclusion-ph31-eval"
        " (experiments/h20/ph31_eval.txt with Stage C Run 1's E1 evaluation agent seed, read from ph30, not written here)")
    say("   decisions: decision:h27-open; decision:evidence-release-composition-rule-h27; decision:classification-rule-relaxed-presence-prior-h27; the adopted agent:"
        " decision:n2-release-adopted-within-tested-conditions; bar: decision:h27-w1d-dwell-bar")
    if not all(chk.values()): say("== an adopted file is not the recorded version: STOP, nothing is run =="); raise SystemExit(4)


def readings(say=print):
    say("   readings where the design is silent (file header R1-R17): R1 D = u < p_D from default_rng(world + 30000), one uniform per row per step after the world's own draws, in"
        " every arm (p_D 0 when off); R2 Circuit3: units 1-2 standard_normal((R, 2)) from the shared generator, unit 3 from default_rng(agent + 30000); R3 other = argmax of the"
        " non-held y (= 1 - hi at N 2); R4 hold-not-read: circuit, gate, evidence release and ReleaseN2 on the circuit's hold; val, hit (and the base's silence clock), keep,"
        " nav's and the counter's held clauses read argmax(y) above 0.05, y the act's own (gain, gate); R5 trajectory fields POS, HEAD, NAV, SINCE, TURN, EST, W[V, B]; every"
        " field adds TGT, S, SG, H, SIL, TO, EV, SUS, Z, C2, P2, PRES, NAV6, NAV8, DIFF8, W, AT2, C, VAL ((I2) adds HR and drops D's column); R6 (I2) per row before its first D whiff; R7 (I5) rows with V"
        " present by its counter on every step of the D-off run, (m) the complement; R8 (I6) nav False on 0-58, from 59 nav == (read hold B or D ? its whiff : any B or D whiff),"
        " no flee, the literal first-surge count beside; R9 (b2) with the release on; R10 (c) exact on constructed states through the act; R11 (d) p_D in the Wilson interval,"
        " inside/outside-cone intervals overlap; R12 bar_W = -0.20 x D_off rounded to 0.1; R13 pass probabilities: DP by sqrt(b - DP^2)/20, paired mean by ph23.pass_prob;"
        " R14 M1 arms H26's (Agent14N2 0/0, Agent8 G 0 off/off, Agent5 fixed), three-channel versions with D; R15 Agent15g = filt False, release-off = release False;"
        " R16 dev/eval re-run the bench for M4; R17 arms in parallel processes")


# ------------------------------------------------------------------ the mechanism bench (design section 4)
def bench_specs(seeds, runs=R, steps=T):
    v3, v2 = (1.0, 0.0, 0.0), (1.0, 0.0); kw = dict(runs=runs, steps=steps); sp = {}
    for wd_ in ("T1", "W1", "T3a"):
        for arm in ("Agent15 D on", "Agent15 D off", "hold-not-read D on", "hold-not-read D off"): sp[(wd_, arm)] = (wd_, arm, v3, seeds, kw)
        for arm in ("Agent14N2", "Agent15 at N 2"): sp[(wd_, arm)] = (wd_, arm, v2, seeds, kw)
    sp[("T1", "Agent15g D on")] = ("T1", "Agent15g D on", v3, seeds, kw); sp[("W1", "Agent15g D on")] = ("W1", "Agent15g D on", v3, seeds, kw)
    sp[("W1", "release-off D on")] = ("W1", "release-off D on", v3, seeds, kw)
    for lab, vv in (("0/0", (0.0, 0.0)), ("+1/-1", (1.0, -1.0))):
        sp[("T1", "Agent14N2", lab)] = ("T1", "Agent14N2", vv, seeds, kw); sp[("T1", "Agent15 at N 2", lab)] = ("T1", "Agent15 at N 2", vv, seeds, kw)
    return sp


def identities(res, say=print, label=""):
    ids = {}
    for wd_ in ("T1", "W1", "T3a"):
        ids[f"I1 {wd_} +1/0"] = every(res[(wd_, "Agent15 at N 2")], res[(wd_, "Agent14N2")])
    for lab in ("0/0", "+1/-1"):
        ids[f"I1 T1 {lab}"] = every(res[("T1", "Agent15 at N 2", lab)], res[("T1", "Agent14N2", lab)])
    say(f"(I1) Agent15's code at N 2 == Agent14N2 on every field (reading R5): " + "; ".join(f"{k[3:]} {v}" for k, v in ids.items() if k.startswith("I1")))
    for wd_ in ("T1", "W1", "T3a"):
        for arm in ("Agent15", "hold-not-read"):
            ok, fd = i2_rows(res[(wd_, f"{arm} D on")], res[(wd_, f"{arm} D off")]); ids[f"I2 {wd_} {arm}"] = bool(ok.all())
            say(f"(I2) {wd_} {arm}: D on == D off on every field before each row's first D whiff: rows {int(ok.sum())}/{len(ok)} -> {bool(ok.all())}; first D whiff step {qq(fd)}")
    for wd_ in ("T1", "W1", "T3a"):
        on, off, ref, hn = res[(wd_, "Agent15 D on")], res[(wd_, "Agent15 D off")], res[(wd_, "Agent14N2")], res[(wd_, "hold-not-read D off")]
        ids[f"I3 {wd_}"] = traj(off, ref); ids[f"I4 {wd_}"] = traj(hn, off)
        cf = {k: bool(np.array_equal(off[k][:, :, :2] if off[k].ndim == 3 else off[k], ref[k])) for k in ("S", "H", "SG", "SIL", "TO", "EV")}
        rows_s = int(rowmask(off, ref, TRAJ, True).all(0).sum())
        say(f"(I3) {wd_}: Agent15 D off == Agent14N2 on the trajectory fields in every row {ids[f'I3 {wd_}']} (rows {rows_s}/{len(off['good'])}); circuit fields, reported, not claimed:"
            f" equal on {cf}; rows with any circuit difference {int((~(rowmask(off, ref, ('H', 'SIL', 'TO', 'EV')) ).all(0)).sum())}")
        say(f"(I4) {wd_}: hold-not-read D off == Agent15 D off on the trajectory fields {ids[f'I4 {wd_}']}")
    on, off = res[("T1", "Agent15 D on")], res[("T1", "Agent15 D off")]; vab = v_absent(off); pres = ~vab
    eqr = rowmask(on, off, TRAJ, True).all(0); ids["I5 T1"] = bool(eqr[pres].all())
    say(f"(I5) T1: rows with V present by its counter on every step of the D-off run (reading R7) {int(pres.sum())}/{len(pres)}; of them D on == D off on the trajectory fields"
        f" {int(eqr[pres].sum())} -> {ids['I5 T1']}; rows with V ever absent {int(vab.sum())}, of them equal {int(eqr[vab].sum())}")
    for wd_ in ("W1", "T3a"):
        for arm in ("Agent15 D on", "hold-not-read D on"):
            ok, lit = i6_rows(res[(wd_, arm)]); ids[f"I6 {wd_} {arm}"] = bool(ok.all())
            say(f"(I6) {wd_}D {arm}: nav False on 0-{PR - 1}, the navigation law from {PR} and no flee (reading R8): rows {int(ok.sum())}/{len(ok)} -> {bool(ok.all())};"
                f" literal 'first surge = first B or D whiff at or after {PR}' (printed, not claimed) {int(lit.sum())}/{len(lit)}")
    fl = {k: v["neg"] for k, v in res.items() if v["vals"] in ((1.0, 0.0, 0.0), (1.0, 0.0))}; ids["I6 no flee at +1/0/0"] = all(x == 0 for x in fl.values())
    dr = all(o["draws_equal"] and o["rng_equal"] for o in res.values())
    ids["masked draws == World7 twin"] = dr
    t3c = all(np.array_equal(res[("T3a", a)]["start"], res[("T3a", a)]["src"][np.arange(len(res[("T3a", a)]["good"])), res[("T3a", a)]["good"]])
              and (res[("T3a", a)]["H0"] == res[("T3a", a)]["good"]).all() for a in ("Agent15 D on", "Agent15 D off", "Agent14N2", "hold-not-read D on", "hold-not-read D off"))
    ids["T3a construction"] = bool(t3c)
    say(f"(I6) no flee command (steps with a negatively valued read hold) in any arm at +1/0(/0): {ids['I6 no flee at +1/0/0']}; masked draws == the World7 twin, generator state"
        f" equal, every W1/T3a run {dr}; T3a construction (start at the valued source, valued hold s 2.0) {bool(t3c)}")
    return ids


def b1(say):
    out = {}
    for nch, kind in ((3, "A15"), (2, "A14N2")):
        for k in range(nch):
            for val in (0.0, 1.0):
                kn = [0.0]*nch; kn[k] = val; sched = [(1, [1.0 if j == k else 0.0 for j in range(nch)]), (BENCH["steps_b1"] - 1, [0.0]*nch)]
                o, _ = stub(kind, kn, sched, nch=nch); pk = float(np.median(o["S"][:, :, k], 1).max()); held = (o["H"] == k).any(0)
                out[(nch, k, val)] = (pk, int(held.sum()))
        say(f"(b1) N {nch}: single whiff from rest at step 0, {BENCH['steps_b1']} steps (peak = max over steps of the median s over rows; holds = rows holding that channel on any step): "
            + "; ".join(f"ch {k} v {int(v)}: peak {out[(nch, k, v)][0]:.3f}, holds {out[(nch, k, v)][1]}/{BENCH['rows']}" for k in range(nch) for v in (0.0, 1.0)))
    return out


def b2(say):
    for p in (0.03, 0.30):
        for k, lab in ((0, "V held (D gated)"), (1, "B held (D not gated)")):
            o, _ = stub("A15", [1.0, 0.0, 0.0], [(BENCH["steps_b2"], [0.0, 0.0, p])], hold=k)
            H = o["H"]; end = first_true(H != k); dh = (H == 2).any(0)
            say(f"(b2) {lab}, D only at p {p}, {BENCH['steps_b2']} steps, release on (reading R9): holding at 200 {int((H[-1] == k).sum())}/{BENCH['rows']}; hold end step {qq(end)};"
                f" ended with an evidence flag {int(((end >= 0) & o['EV'][np.maximum(end, 0), np.arange(len(end))]).sum())}; rows forming a D hold {int(dh.sum())}; D whiffs per row"
                f" {o['W'][:, :, 2].sum(0).mean():.2f}")


def b3(say, seeds=BS):
    rng = np.random.default_rng(seeds[0]); n = 20000; ok = True; tot = 0
    for hp_ in (-1, 0, 1, 2):
        y = rng.random((n, 3))*1.8; y[: n//4] = np.round(y[: n//4]/0.2)*0.2                    # exact 0.2 steps included
        y[n//4: n//2, :] = y[n//4: n//2, :1] + np.array([0.0, 0.2, 0.2 + 1e-12])                 # margins at and just above 0.2
        hp = np.full(n, hp_); got = evidence_due(y, hp)
        exp = np.array([hp_ >= 0 and max(y[i, j] for j in range(3) if j != hp_) - y[i, hp_] > MARGIN for i in range(n)])
        ok &= bool(np.array_equal(got, exp)); tot += int(got.sum())
    y2 = rng.random((n, 2))*1.8
    for hp_ in (-1, 0, 1):
        hp = np.full(n, hp_); hi = np.maximum(hp, 0); r = np.arange(n)
        ok &= bool(np.array_equal(evidence_due(y2, hp), (hp >= 0) & ((y2[r, 1 - hi] - y2[r, hi]) > MARGIN)))
    o, a = stub("A15", [1.0, 0.0, 0.0], [(BENCH["steps_c"], [0.3, 0.3, 0.3])], seeds=seeds)
    HP = np.vstack([o["H0"][None, :], o["H"][:-1]]).astype(int)
    cons = all(np.array_equal(o["EV"][t], evidence_due(o["YP"][t], HP[t])) for t in range(o["steps"]))
    say(f"(b3) evidence release exact on constructed y (4 x {n} rows, held channel -1/0/1/2, grid and margin cases; fired {tot}): == the brute-force 'strongest other channel exceeds"
        f" the held one by more than 0.2' {ok}; at N 2 == `1 - hi` {ok}; in a stub run (all channels p 0.3, {BENCH['steps_c']} steps) the act's flag == the rule on its own y and"
        f" held channel on every step {cons}")
    return ok and cons


def c_bench(say, seeds=BS):
    res = {}; n_combo = 8*4*2
    # top / nav law and presence through the act (reading R10)
    combos = [(m, hk, vp) for m in range(8) for hk in (-1, 0, 1, 2) for vp in (True, False)]; rows = len(combos)*5
    X = np.array([[bool(m & 1), bool(m & 2), bool(m & 4)] for m, _, _ in combos]*5); HK = np.array([hk for _, hk, _ in combos]*5); VP = np.array([vp for _, _, vp in combos]*5)

    def pre(a):
        r = np.arange(rows); a.sel.s[r[HK >= 0], HK[HK >= 0]] = 2.0
        a.c = np.zeros((rows, 3)); a.c[~VP, 0] = 1000.0
    kv = np.tile([1.0, 0.0, 0.0], (rows, 1)); a = build("A15", rows, seeds[1], np.zeros(rows, int), kv); pre(a)
    a.act(Still(rows), X, np.ones(rows, bool)); h = a.held(); r = np.arange(rows)
    held = np.zeros((rows, 3), bool); held[r, np.maximum(h, 0)] = h >= 0
    c_exp = np.where(X, 0.0, np.where(np.arange(3)[None, :] == 0, np.where(VP, 1.0, 1001.0)[:, None], 1.0))
    pres_exp = (c_exp < N_HI) | held
    vpres = pres_exp[:, 0]; vmax = np.where(vpres, 1.0, 0.0); vv = np.array([1.0, 0.0, 0.0])
    top = pres_exp & (vv[None, :] >= 0) & (vv[None, :] == vmax[:, None])
    vh = np.where(h >= 0, vv[np.maximum(h, 0)], 0.0); keep = (h >= 0) & (vh == vmax)
    nav_exp = np.where(keep, X[r, np.maximum(h, 0)], (X & top).any(1))
    res["top/nav law"] = bool(np.array_equal(a.present, pres_exp) and np.array_equal(a.nav_hit, nav_exp) and np.array_equal(a.c, c_exp))
    res["top with V present is {V}, absent is {B, D}"] = bool((top[vpres] == [True, False, False]).all() and (top[~vpres] == [False, True, True]).all())
    say(f"(c) top / keep / nav law at (+1, 0, 0) through the act, {rows} rows (every combination of whiffs 2^3, held none/V/B/D, V present/absent by its counter, x5): nav, presence"
        f" and counters exact {res['top/nav law']}; top = {{V}} with V present and {{B, D}} with V absent {res['top with V present is {V}, absent is {B, D}']};"
        f" held after the step as constructed {int((h == HK).sum())}/{rows}")
    # the gate's mask, one step, same construction with and without the gate
    for hk in (-1, 0, 1, 2):
        n = 50; x = np.ones((n, 3), bool); kvg = np.tile([1.0, 0.0, 0.0], (n, 1))
        ag = build("A15", n, seeds[1], np.zeros(n, int), kvg); au = build("A15", n, seeds[1], np.zeros(n, int), kvg); au.rule = False
        if hk >= 0: ag.sel.s[:, hk] = 2.0; au.sel.s[:, hk] = 2.0
        ag.act(Still(n), x, np.ones(n, bool)); au.act(Still(n), x, np.ones(n, bool))
        mask = np.array([[True, not (hk == 0), not (hk == 0)]]*n) if hk >= 0 else np.ones((n, 3), bool)
        res[f"gate held {hk}"] = bool(np.array_equal(ag.yp, au.yp*mask))
    say("(c) gate mask at (+1, 0, 0), one step, all channels whiffing, gated y == ungated y x expected mask (V held: B and D zeroed; B, D or nothing held: nothing zeroed): "
        + "; ".join(f"held {hk} {res[f'gate held {hk}']}" for hk in (-1, 0, 1, 2)))
    # counters: recursion from 240 and presence, three channels
    ok_all = True
    for lab, sched in (("no whiff", [(400, [0.0, 0.0, 0.0])]), ("one whiff per channel at step 0", [(1, [1.0, 1.0, 1.0]), (399, [0.0, 0.0, 0.0])]),
                       ("p 0.30 bursts", [(20, [0.3, 0.3, 0.3]), (380, [0.0, 0.0, 0.0])])):
        o, _ = stub("A15", [1.0, 0.0, 0.0], sched, seeds=seeds); X_ = o["W"]; st, nr, _ = X_.shape; c = np.full((nr, 3), float(N_HI - P_PRIOR)); ok = np.ones(nr, bool)
        for t in range(st):
            c = np.where(X_[t], 0.0, c + 1.0); hd = np.zeros((nr, 3), bool); hh = o["H"][t].astype(int); hd[np.arange(nr), np.maximum(hh, 0)] = hh >= 0
            ok &= (o["C2"][t] == c).all(1) & (o["P2"][t] == ((c < N_HI) | hd)).all(1)
        extra = True
        if lab == "no whiff": tb = np.arange(st)[:, None]; extra = bool((o["P2"] == (tb <= PR - 1)[:, :, None]).all())
        res[f"counter {lab}"] = bool(ok.all() and extra); ok_all &= res[f"counter {lab}"]
    say("(c) three counters (start 240, c <- 0 on a whiff else c + 1, present == c < 300 or held), 400 rows x 400 steps: " + "; ".join(f"{k[8:]} {v}" for k, v in res.items() if k.startswith("counter")))
    # (S) and (Z) on a D hold (value 0)
    o, _ = stub("A15", [1.0, 0.0, 0.0], [(1, [0.0, 0.0, 1.0]), (BENCH["steps_c"] - 1, [0.0, 0.0, 0.0])], hold=2, seeds=seeds)
    H = o["H"]; end = first_true(H != 2); rr = np.arange(len(end))
    s_end = (end == 48) & (o["S"][np.maximum(end, 0), rr] <= 1.0).all(1) & (H[:48] == 2).all(0)
    res["(S) D hold ends at 48"] = bool(s_end.all())
    o2, _ = stub("A15", [1.0, 0.0, 0.0], [(20, [0.0, 0.0, 0.3]), (BENCH["steps_c"] - 20, [0.0, 0.0, 0.0])], seeds=seeds)
    H2 = o2["H"]; prev = np.vstack([o2["H0"][None, :], H2[:-1]]); form = (H2 == 2) & (prev != 2)
    res["(Z) counter 0 on D-hold formation"] = bool(form.any() and (o2["SIL"][form] == 0).all())
    say(f"(c) (S) a constructed D hold (s 2.0) with one D whiff at step 0 ends at step 48 with every unit <= 1.0: rows {int(s_end.sum())}/{len(end)} (end step {qq(end)}) ->"
        f" {res['(S) D hold ends at 48']}; (Z) the silence counter is 0 on every step a D hold forms from D whiffs (p 0.30, 20 steps): formations {int(form.sum())} -> "
        f"{res['(Z) counter 0 on D-hold formation']}; sustain steps on the D hold {int(o['SUS'].sum())}")
    return all(res.values()), res


def d_bench(o, say):
    D = wd(o); k, n = int(D.sum()), D.size; pt, lo, hi = ph15.wilson(k, n); ok1 = lo <= P_D <= hi
    cin = o["CONE"]; ki, ni = int(D[cin].sum()), int(cin.sum()); ko, no = int(D[~cin].sum()), int((~cin).sum())
    pi, li, hi_i = ph15.wilson(ki, ni); po, lo_o, hi_o = ph15.wilson(ko, no); ok2 = not (hi_i < lo_o or hi_o < li)
    say(f"(d) D stream, T1D Agent15 run {o['H'].shape[1]} x {o['H'].shape[0]}: D whiffs {k}/{n} = {pt:.5f} [{lo:.5f}, {hi:.5f}], p_D {P_D} inside {ok1}; inside the cones or within 3.0"
        f" {ki}/{ni} = {pi:.5f} [{li:.5f}, {hi_i:.5f}], outside {ko}/{no} = {po:.5f} [{lo_o:.5f}, {hi_o:.5f}], intervals overlap {ok2} (reading R11)")
    return ok1 and ok2


def bench(say=print, seeds=BS, runs=R, steps=T):
    say(f"== H27 mechanism bench (design v2 FINAL section 4). design {DESIGN}; {BENCH}; p_D {P_D}; P {P_PRIOR}, N_hi {N_HI}; bootstrap seed {ph15.BOOT_SEED} ==")
    header(say); readings(say)
    say("   rows share no state: one generator per world, one for D, one per agent population and one for the third unit, fixed-size draws consumed in row order every step")
    sp = bench_specs(seeds, runs, steps); res = runs_of(list(sp.values()), list(sp.keys()))
    ids = identities(res, say); bars = {}; out = {}
    b1(say); b2(say); bars["b3"] = b3(say)
    okc, rc = c_bench(say); bars["c"] = okc
    bars["d"] = d_bench(res[("T1", "Agent15 D on")], say)
    # ---- (m), printed first
    on, off, ref, g15 = res[("T1", "Agent15 D on")], res[("T1", "Agent15 D off")], res[("T1", "Agent14N2")], res[("T1", "Agent15g D on")]
    con, coff, cref, cg = cls3(on), cls3(off), cls3(ref), cls3(g15); vab = v_absent(off)
    fv = first_true(wv(off)); nx = np.where(fv < 0, 10**6, fv)
    say(f"(m) T1 rows with V ever absent (no V whiff by step {PR - 1}, or a V silence of {N_HI} steps; Agent15 D off, reading R7): {int(vab.sum())}/{runs} (H26 eval's at-risk count 20"
        f" is the reference); of them no V whiff by {PR - 1}: {int((vab & (nx > PR - 1)).sum())}; first V whiff step {qq(fv)}")
    for lab, m_ in (("V ever absent", vab), ("V always present", ~vab)):
        say(f"      [{lab}, {int(m_.sum())}] outcome V/N/tie: D on {int((con[m_] == 0).sum())}/{int((con[m_] == 1).sum())}/{int((con[m_] == 2).sum())};"
            f" D off {int((coff[m_] == 0).sum())}/{int((coff[m_] == 1).sum())}/{int((coff[m_] == 2).sum())}")
    Von, Voff, Vg, Vref = (con == 0), (coff == 0), (cg == 0), (cref == 0)
    into, outv = int((Von & ~Voff).sum()), int((~Von & Voff).sum())
    say(f"      D on vs D off: into V {into}, out of V {outv}; rows equal on the trajectory fields {int(rowmask(on, off, TRAJ, True).all(0).sum())}/{runs}")
    # ---- (h)
    dp, b = pair_dp(Von, Voff); _, _, dlo, dhi = interval("DP", Von.astype(float), Voff.astype(float)); ppb = pp_dp(dp, b, -0.05)
    dpc, bc = pair_dp(Von, Vg); ppc = pp_dp(dpc, bc, 0.05); stop_h = ppb < 0.5
    say(f"(h) T1 on bench seeds, +1/0/0 {runs} x {steps}: " + "; ".join(f"{k} V {int((c == 0).sum())} N {int((c == 1).sum())} tie {int((c == 2).sum())} P(V) {interval('P', c == 0)[1]:.3f}"
                                                                    f" [{interval('P', c == 0)[2]:.3f}, {interval('P', c == 0)[3]:.3f}]"
                                                                    for k, c in (("Agent15 D on", con), ("Agent15 D off", coff), ("Agent14N2", cref), ("Agent15g D on", cg))))
    say(f"   (h) paired DP P(V) Agent15 D on - D off {dp:+.4f} [{dlo:+.4f}, {dhi:+.4f}] (bootstrap 5000, seed {ph15.BOOT_SEED}); discordant b {b:.4f}, sd sqrt(b - DP^2)"
        f" {math.sqrt(max(b - dp*dp, 0.0)):.4f}; M2(b) pass probability {ppb:.4f}; M2(c) vs Agent15g at DP {dpc:+.4f} (b {bc:.4f}): {ppc:.4f}; M2(a) reported, P(K >= 365 of 400)"
        f" at P(V) {Von.mean():.3f}: {binom_ge(Von.mean()):.4f}; lost rows (no whiff of either plume in the last third) D on {int(lost_t1(on).sum())}, D off {int(lost_t1(off).sum())}")
    say(f"   (h) STOP RULE (design section 4): M2(b) pass probability {ppb:.4f} {'< 0.5 -> STOP' if stop_h else '>= 0.5 -> continue'}")
    out.update(dp_T1=dp, dp_lo=dlo, dp_hi=dhi, pp_M2b=ppb, pp_M2c=ppc, stop_h=stop_h, m=int(vab.sum()), into=into, outv=outv)
    # ---- (hW)
    won, woff, wref, whn, wro, wg = (res[("W1", a)] for a in ("Agent15 D on", "Agent15 D off", "Agent14N2", "hold-not-read D on", "release-off D on", "Agent15g D on"))
    s = {k: w1sum(o) for k, o in (("Agent15 D on", won), ("Agent15 D off", woff), ("Agent14N2", wref), ("hold-not-read D on", whn), ("hold-not-read D off", res[("W1", "hold-not-read D off")]),
                                  ("release-off D on", wro), ("Agent15g D on", wg))}
    for k, v in s.items():
        say(f"      [W1 {k}] mean dwell within 3.0 of B over {steps} steps {v['dwell'].mean():.3f} (quartiles {q3(v['dwell'])}); reach {int(v['reach'].sum())}/{runs}; lost rows"
            f" {int(v['lost'].sum())}; wall contacts per row {v['contacts'].mean():.3f}")
    Doff = float(s["Agent15 D off"]["dwell"].mean()); bar_w = round(-0.20*Doff, 1)
    pp5b, m5b, sd5b = pass_prob(s["Agent15 D on"]["dwell"] - s["Agent15 D off"]["dwell"], bar_w)
    _, _, blo, bhi = interval("DP", s["Agent15 D on"]["dwell"], s["Agent15 D off"]["dwell"])
    dpl, bl = pair_dp(s["Agent15 D on"]["lost"], s["Agent15 D off"]["lost"]); pp5d = pp_dp(dpl, bl, 0.05, most=True)
    _, _, llo, lhi = interval("DP", s["Agent15 D on"]["lost"].astype(float), s["Agent15 D off"]["lost"].astype(float))
    k5a, pt5a, lo5a, hi5a = interval("P", s["Agent15 D on"]["reach"])
    say(f"   (hW) measured: D_off (Agent15's mean W1 dwell without D) = {Doff:.4f}; rule bar_W = -0.20 x D_off rounded to 0.1 = {bar_w:+.1f} (reading R12); paired dwell D on - D off"
        f" {m5b:+.4f} sd {sd5b:.4f} (bootstrap [{blo:+.4f}, {bhi:+.4f}]); M5(b) pass probability {pp5b:.4f}; lost rows DP D on - D off {dpl:+.4f} [{llo:+.4f}, {lhi:+.4f}]"
        f" (b {bl:.4f}); M5(d) pass probability {pp5d:.4f}; M5(a) reach {k5a}/{runs} = {pt5a:.3f} [{lo5a:.3f}, {hi5a:.3f}]; M5(c) contacts per row {s['Agent15 D on']['contacts'].mean():.3f}")
    stop_hw = min(pp5b, pp5d) < 0.5
    say(f"   (hW) STOP RULE (design section 4): M5(b) {pp5b:.4f}, M5(d) {pp5d:.4f} -> {'< 0.5 -> STOP' if stop_hw else 'both >= 0.5 -> continue'}")
    out.update(D_off=Doff, bar_W=bar_w, m5b=m5b, sd5b=sd5b, pp_M5b=pp5b, dp5d=dpl, pp_M5d=pp5d, stop_hw=stop_hw)
    # ---- (hH)
    dph, bh = pair_dp(s["hold-not-read D on"]["lost"], s["Agent15 D on"]["lost"]); pp6 = pp_dp(dph, bh, 0.05)
    _, _, hlo, hhi = interval("DP", s["hold-not-read D on"]["lost"].astype(float), s["Agent15 D on"]["lost"].astype(float)); stop_hh = pp6 < 0.5
    dp0, _ = pair_dp(s["hold-not-read D off"]["lost"], s["Agent15 D off"]["lost"])
    say(f"   (hH) the hold's benefit: lost rows DP hold-not-read D on - Agent15 D on {dph:+.4f} [{hlo:+.4f}, {hhi:+.4f}] (b {bh:.4f}); M6 pass probability {pp6:.4f};"
        f" without D (hold-not-read D off - Agent15 D off) {dp0:+.4f}")
    say(f"   (hH) STOP RULE (design section 4): M6 pass probability {pp6:.4f} {'< 0.5 -> STOP' if stop_hh else '>= 0.5 -> continue'}")
    out.update(dp6=dph, pp_M6=pp6, stop_hh=stop_hh)
    for wd_ in ("T3a",):
        say(f"      [T3a reported] neutral dwell 100-599: " + ", ".join(f"{a} {t3_dwell(res[(wd_, a)], 100, steps).mean():.3f}" for a in ("Agent15 D on", "Agent15 D off", "Agent14N2", "hold-not-read D on")))
    idok = all(ids.values()); bok = all(bars.values()); verdict = idok and bok; stop = stop_h or stop_hw or stop_hh; out["stop"] = stop; out["ids"] = ids
    say(f"== M4: identities {idok}; failed {[k for k, v in ids.items() if not v]}; implementation bars (b3) {bars['b3']}, (c) {bars['c']}, (d) {bars['d']} -> M4"
        f" {'PASS: the tasks may be run' if verdict else 'FAIL, NO CANDIDATE: an implementation error (design section 4); the tasks are NOT run'}; stop rules (h)"
        f" {'STOP' if stop_h else 'continue'}, (hW) {'STOP' if stop_hw else 'continue'}, (hH) {'STOP' if stop_hh else 'continue'} ==")
    return verdict, out, res


# ------------------------------------------------------------------ self-checks
def demo():
    print(f"== H27 self-checks (demo). design {DESIGN} ==")
    header(); readings()
    print("   fixed before this recorded demo (one earlier trial run of this demo on the demo seeds 5/6 only, no registered seed): the demo's own check that the pass-probability"
          " formula reproduces the design's M5(b) illustration table asserted every entry within 0.02 and stopped at difference -3.0 (design 0.99, formula 0.955, a hand-arithmetic"
          " slip in the design); the check now asserts the other entries and prints that one; no model, harness, bar or rule code changed")
    n, st, sd = 40, 200, (5, 6); kw = dict(runs=n, steps=st); v3, v2 = (1.0, 0.0, 0.0), (1.0, 0.0)
    mro = [c.__name__ for c in Agent15.__mro__[:7]]
    assert mro == ["Agent15", "ReleaseN2", "Agent14", "Release", "Act15", "Agent9", "Agent8"], mro
    a = build("A15", 4, 5, np.zeros(4, int), np.zeros((4, 3)))
    assert super(Release, a).act.__func__ is Act15.act and a.sel.n == 3 and a.up.P.shape == (4, 3) and a.c.shape == (4, 3) and (a.c == 240).all() and a.codes.shape[1] == 3
    print(f"ok  method order {mro}; ReleaseN2's base act is Act15.act; stage chans 3, circuit n 3, counter (R, 3) at 240, three codes")
    # Circuit3 draws
    c3 = Circuit3(6, rng3=np.random.default_rng(2), n=3, theta=1.0, k=12.0, noise=1.0, rng=np.random.default_rng(1)); c2 = Circuit(6, n=2, theta=1.0, k=12.0, noise=1.0, rng=np.random.default_rng(1))
    y3 = np.zeros((6, 3)); c3.step(y3); c2.step(y3[:, :2]); r1, r2 = np.random.default_rng(1).standard_normal((6, 2)), np.random.default_rng(2).standard_normal((6, 1))
    assert np.array_equal(c3.rng.bit_generator.state["state"], c2.rng.bit_generator.state["state"])
    c3b = Circuit3(6, rng3=np.random.default_rng(2), n=2, theta=1.0, k=12.0, noise=0.01, rng=np.random.default_rng(1)); c2b = Circuit(6, n=2, theta=1.0, k=12.0, noise=0.01, rng=np.random.default_rng(1))
    for _ in range(50): yy = np.random.default_rng(3).random((6, 2)); c3b.step(yy, reset=0.5); c2b.step(yy, reset=0.5)
    assert np.array_equal(c3b.s, c2b.s) and np.array_equal(c3b.S, c2b.S)
    print("ok  Circuit3: the shared generator is consumed as ph2.Circuit at n 2 (state equal after a step at n 3); at n 2 Circuit3 == ph2.Circuit bitwise over 50 steps")
    # harness fidelity: my Agent14N2 == ph28.run's Agent14 (H26's harness) at +1/0
    for wd_ in ("T1", "W1", "T3a"):
        mine = run(wd_, "Agent14N2", v2, sd, **kw); ref = ph28.run(wd_, Agent14, v2, sd, runs=n, steps=st)
        keys = ("POS", "HEAD", "H", "S", "SG", "NAV", "SINCE", "TGT", "SIL", "TO", "EV")
        assert all(np.array_equal(mine[k], ref[k]) for k in keys) and np.array_equal(mine["W"][:, :, :2], ref["W"]) and np.array_equal(mine["AT2"], ref["AT2"]), wd_
        assert np.array_equal(mine["C2"], ref["C2"]) and np.array_equal(mine["P2"], ref["P2"]), wd_
    print(f"ok  this harness's Agent14N2 == H26's harness (ph28.run, Agent14) at +1/0 on {n} x {st}, T1, W1, T3a: positions, headings, holds, circuit, nav, clocks, flags, whiffs, counters")
    # identities on demo seeds
    sp = bench_specs(sd, n, st); res = runs_of(list(sp.values()), list(sp.keys()))
    seq = run("W1", "Agent15 D on", v3, sd, **kw); assert every(seq, res[("W1", "Agent15 D on")]), "parallel != sequential"
    print("ok  a parallel result equals a sequential one bitwise (W1 Agent15 D on)")
    lines = []; ids = identities(res, lines.append)
    for ln in lines: print("    " + ln)
    assert all(ids.values()), [k for k, v in ids.items() if not v]
    print(f"ok  identities (I1)-(I6) on demo seeds {n} x {st}: all True")
    ok3 = b3(lambda s: print("    " + s), seeds=sd); assert ok3
    okc, rc = c_bench(lambda s: print("    " + s), seeds=sd); assert okc, rc
    print("ok  bench (b3) and (c) exact on constructed states built on the demo seeds (the bench re-runs them on the bench seeds)")
    # pass-probability arithmetic against the design's tables
    tab = {k: pp_dp(-k/400.0, k/400.0, -0.05) for k in (8, 10, 12, 13, 15)}; exp = {8: 0.990, 10: 0.893, 12: 0.650, 13: 0.506, 15: 0.26}
    assert all(abs(tab[k] - exp[k]) < 0.01 for k in exp), tab
    pw = {x: pass_prob(np.array([x - 9.85, x + 9.85]*200), -4.8)[0] for x in (-2.0, -3.0, -3.5, -4.0, -4.5)}; expw = {-2.0: 1.00, -3.0: 0.99, -3.5: 0.75, -4.0: 0.37, -4.5: 0.07}
    slips = {x: (expw[x], round(pw[x], 3)) for x in expw if abs(pw[x] - expw[x]) >= 0.02}
    assert set(slips) <= {-3.0, -4.5} and all(abs(pw[x] - expw[x]) < 0.02 for x in expw if x not in slips), pw
    p6 = {x: pp_dp(x, x, 0.05) for x in (0.075, 0.08, 0.10, 0.15)}; exp6 = {0.075: 0.50, 0.08: 0.60, 0.10: 0.91, 0.15: 1.00}
    assert all(abs(p6[x] - exp6[x]) < 0.03 for x in exp6), p6
    pd = {k: pp_dp(k/400.0, k/400.0, 0.05, most=True) for k in (5, 10, 12, 13, 15)}; expd = {5: 1.00, 10: 0.89, 12: 0.65, 13: 0.50, 15: 0.26}
    assert all(abs(pd[k] - expd[k]) < 0.01 for k in expd), pd
    print("ok  pass-probability arithmetic reproduces the design's section 7 tables: M2(b) k 8/10/12/13/15 = " + "/".join(f"{tab[k]:.3f}" for k in exp)
          + "; M5(b) at bar -4.8, sd 9.85, differences -2.0/-3.0/-3.5/-4.0/-4.5 = " + "/".join(f"{pw[x]:.3f}" for x in expw)
          + f" (the design's hand table differs by 0.02 or more at {sorted(slips)}: design value, formula value {slips}; hand-arithmetic slips in the design's illustration,"
          " which no bar or stop rule reads; the stop rule (hW) computes the formula at the bench values)"
          + "; M5(d) k_L 5/10/12/13/15 = " + "/".join(f"{pd[k]:.3f}" for k in expd) + "; M6 DP 0.075/0.08/0.10/0.15 (b = DP) = " + "/".join(f"{p6[x]:.3f}" for x in exp6))
    hits, nums, nf = seeds_unused(); assert not hits, f"a seed of this run appears in {hits}"
    print(f"ok  seeds {nums} appear in no other file under the repository ({nf} files scanned; excluded by name ph32.py, ph32_*.txt, h27_*.md, master_plan.md, notes/*.md, viewer/*;"
          f" the pair of decision:seed-scan-exclusion-ph31-eval)")
    print(f"    BARS {BARS} ({'unset: dev and eval refuse to run until decision:h27-w1d-dwell-bar is written in' if BARS['W'] is None else 'set'})")


# ------------------------------------------------------------------ the tasks (design sections 5-8)
T1ARMS = {"Agent15 D on": (1.0, 0.0, 0.0), "Agent15 D off": (1.0, 0.0, 0.0), "Agent14N2": (1.0, 0.0), "Agent15g D on": (1.0, 0.0, 0.0),
          "hold-not-read D on": (1.0, 0.0, 0.0), "hold-not-read D off": (1.0, 0.0, 0.0), "Agent15 at N 2": (1.0, 0.0), "neutral": (0.0, 0.0),
          "pathway-off": (1.0, 0.0), "known-answer": (1.0, 0.0), "pathway-off D on": (1.0, 0.0, 0.0), "neutral D on": (0.0, 0.0, 0.0)}
W1ARMS = ("Agent15 D on", "Agent15 D off", "Agent14N2", "hold-not-read D on", "hold-not-read D off", "release-off D on", "Agent15g D on", "Agent15 at N 2")
T3ARMS = ("Agent15 D on", "Agent15 D off", "Agent14N2", "hold-not-read D on", "hold-not-read D off", "Agent15 at N 2")


def task_specs(seeds):
    kw = dict(runs=R, steps=T); sp = {}
    for a, v in T1ARMS.items(): sp[("T1", a)] = ("T1", a, v, seeds, kw)
    for a in W1ARMS: sp[("W1", a)] = ("W1", a, (1.0, 0.0) if ARMS[a][1] == 2 else (1.0, 0.0, 0.0), seeds, kw)
    for a in T3ARMS: sp[("T3a", a)] = ("T3a", a, (1.0, 0.0) if ARMS[a][1] == 2 else (1.0, 0.0, 0.0), seeds, kw)
    for lab, vv in (("0/0", (0.0, 0.0)), ("+1/-1", (1.0, -1.0))):
        sp[("T1", "Agent14N2", lab)] = ("T1", "Agent14N2", vv, seeds, kw); sp[("T1", "Agent15 at N 2", lab)] = ("T1", "Agent15 at N 2", vv, seeds, kw)
    sp[("T4", "Agent14N2")] = ("T1", "Agent14N2", (1.0, -1.0), seeds, kw); sp[("T4", "Agent15 D on")] = ("T1", "Agent15 D on", (1.0, -1.0, 0.0), seeds, kw)
    return sp


def cells_line(o, c):
    return " | ".join(f"cell {k}: V {int(((c == 0) & (o['cell'] == k)).sum())} N {int(((c == 1) & (o['cell'] == k)).sum())} 0 {int(((c == 2) & (o['cell'] == k)).sum())}" for k in range(4))


def main(mode):
    if None in BARS.values():
        print(f"== H27 {mode}: REFUSED. BARS {BARS} is unset: decision:h27-w1d-dwell-bar must be recorded from the bench and written into this file first (design section 8) =="); sys.exit(2)
    seeds = SEEDS[mode]
    print(f"== H27, {mode.upper()}. design {DESIGN}; G {G_STAR}, gate on; P {P_PRIOR}, N_hi {N_HI}; p_D {P_D}; world seed {seeds[0]}, agent seed {seeds[1]}; {R} rows x {T} steps;"
          f" geometry C0; bootstrap seed {ph15.BOOT_SEED}; BARS {BARS}; {'operation check only (not a verdict)' if mode == 'dev' else 'the one evaluation'} ==")
    header(); readings()
    hits, nums, nf = seeds_unused(); print(f"   seed self-check: every H27 seed and derived number in no other file ({nf} scanned): {not hits}{'' if not hits else ' ' + str(hits)}")
    print("   amendments: none")
    print("   rows share no state: one generator per world, one for D, one per agent population and one for the third unit")
    sp = task_specs(seeds); res = runs_of(list(sp.values()), list(sp.keys()))
    t1 = {a: res[("T1", a)] for a in T1ARMS}; c = {a: cls3(o) for a, o in t1.items()}
    print("\n== T1 / T1D, the H21 choice task (+1/0 without D, +1/0/0 with D) ==")
    for a, o in t1.items():
        V, N, Z = (c[a] == 0), (c[a] == 1), (c[a] == 2); k, pt, lo, hi = interval("P", V)
        print(f"   [T1 {a} {o['cls']} values {o['vals']}{' D on' if o['d_on'] else ''}] V {int(V.sum())} N {int(N.sum())} tie {int(Z.sum())}; P(V) {pt:.3f} [{lo:.3f}, {hi:.3f}];"
              f" lost rows {int(lost_t1(o).sum())}; wall contacts per row {o['contacts'].mean():.3f}; {cells_line(o, c[a])}")
    print("\n== W1 / W1D, the absent-odour world (valued column masked from step 0) ==")
    s = {a: w1sum(res[("W1", a)]) for a in W1ARMS}
    for a in W1ARMS:
        o = res[("W1", a)]; f1 = first_true(o["NAV"]); fd = (o["H"] == 2).any(0) if o["nch"] == 3 else np.zeros(R, bool)
        print(f"   [W1 {a} {o['cls']}] dwell at B mean {s[a]['dwell'].mean():.3f} (quartiles {q3(s[a]['dwell'])}); reach {int(s[a]['reach'].sum())}/{R}; lost rows {int(s[a]['lost'].sum())};"
              f" wall contacts per row {s[a]['contacts'].mean():.3f}; first surge step {qq(f1)}; rows forming a D hold {int(fd.sum())}; D whiffs per row {wd(o).sum(0).mean():.2f}")
    print("\n== T3a / T3aD, the constructed loss (valued column masked, start at the valued source, valued hold s 2.0; REPORTED) ==")
    D3 = {a: t3_dwell(res[("T3a", a)], 100, T) for a in T3ARMS}
    for a in T3ARMS:
        o = res[("T3a", a)]; end = first_true(o["H"] != o["good"][None, :])
        print(f"   [T3a {a} {o['cls']}] neutral dwell 100-599 mean {D3[a].mean():.3f} (quartiles {q3(D3[a])}); valued hold end step {qq(end)}")
    print("\n== T4, +1/-1 (World7; Agent15 +1/-1/0 with D; REPORTED, outside the verdict) ==")
    for a in ("Agent14N2", "Agent15 D on"):
        o = res[("T4", a)]; cc = cls3(o); V = cc == 0; k, pt, lo, hi = interval("P", V)
        print(f"   [T4 {a} {o['cls']} values {o['vals']}] V {int(V.sum())} N {int((cc == 1).sum())} tie {int((cc == 2).sum())}; P(V) {pt:.3f} [{lo:.3f}, {hi:.3f}]; lost rows"
              f" (no whiff of either plume in the last third) {int(lost_t1(o).sum())}; wall contacts per row {o['contacts'].mean():.3f}; flee violations {o['viol']} of {o['neg']}"
              f" negatively-held (row, step); dwell at the negative source mean {o['dwell'][np.arange(R), 1 - o['good']].mean():.3f}")
    _, t4dp, t4lo, t4hi = interval("DP", (cls3(res[("T4", "Agent15 D on")]) == 0).astype(float), (cls3(res[("T4", "Agent14N2")]) == 0).astype(float))
    print(f"      reported: paired DP P(V) Agent15 D on - Agent14N2 at +1/-1 {t4dp:+.4f} [{t4lo:+.4f}, {t4hi:+.4f}]")
    judge(mode, res, t1, c, s, D3)


def judge(mode, res, t1, c, s, D3):
    ok = lambda z: "PASS" if z else "FAIL"
    print("\n== criteria (design v2 FINAL section 7; 95 percent, one evaluation, no extension; PASS if every part passes, FAIL if any fails, else INCONCLUSIVE; the unrounded bound decides) ==")
    print(f"   bar read from BARS: bar_W {BARS['W']} (decision:h27-w1d-dwell-bar)")
    m1 = []
    for a in ("neutral", "pathway-off", "known-answer"):
        z = c[a] == 2; m1.append(ok(z.mean() <= 0.20)); print(f"   M1(a) {a}: ties {int(z.sum())}/{R} = {z.mean():.3f}  at most 0.20 -> {m1[-1]}")
    o = t1["neutral"]; V, N, Z = (c["neutral"] == 0), (c["neutral"] == 1), (c["neutral"] == 2); which = np.where(V, o["good"], np.where(N, 1 - o["good"], -1))
    m1.append(crit("M1(b) neutral, P(+y source majority | chose)", "P", (0.35, 0.65), False, (which == o["plus_y"])[~Z]))
    V, Z = (c["pathway-off"] == 0), (c["pathway-off"] == 2); m1.append(crit("M1(c) floor: pathway-off, P(V | chose)", "P", (0.35, 0.65), False, V[~Z]))
    m1.append(crit("M1(d) ceiling: known-answer, P(V) over all rows", "P", 0.85, False, c["known-answer"] == 0))
    M1 = agg(m1); print(f"   M1 -> {M1}{'' if M1 == 'PASS' else '  (the run is UNREADABLE under section 8)'}")
    for a in ("neutral D on", "pathway-off D on"):
        z = c[a] == 2; V = c[a] == 0; print(f"      reported (D-on floors): {a} ties {int(z.sum())}; P(V | chose) {V[~z].mean() if (~z).any() else float('nan'):.3f}")
    ties = {a: float((c[a] == 2).mean()) for a in ("Agent15 D on", "Agent15 D off")}
    print("   section 8: ties in the adopted arm " + ", ".join(f"{a} {v:.3f}" for a, v in ties.items()) + " (unreadable above 0.20)")
    Von, Voff, Vg = (c["Agent15 D on"] == 0), (c["Agent15 D off"] == 0), (c["Agent15g D on"] == 0)
    k2, p2, l2, h2 = interval("P", Von)
    print(f"   M2(a) REPORTED, not a gate: Agent15 D on P(V) {k2}/{R} = {p2:.3f} [{l2:.3f}, {h2:.3f}] against 0.88 -> {'lower bound >= 0.88' if l2 >= 0.88 else 'lower bound < 0.88'} (reported)")
    m2 = [crit("M2(b) DP = P(V) Agent15 D on - Agent15 D off, same rows", "DP", -0.05, False, Von.astype(float), Voff.astype(float)),
          crit("M2(c) DP = P(V) Agent15 D on - Agent15g D on, same rows", "DP", 0.05, False, Von.astype(float), Vg.astype(float))]
    M2 = agg(m2); print(f"   M2 -> {M2}")
    for lab in ("Agent14N2", "hold-not-read D on", "hold-not-read D off"):
        _, dp, lo, hi = interval("DP", Von.astype(float), (c[lab] == 0).astype(float)); print(f"      reported: DP Agent15 D on - {lab} {dp:+.4f} [{lo:+.4f}, {hi:+.4f}]")
    print(f"      where the value goes: into V {int((Von & ~Voff).sum())}, out of V {int((~Von & Voff).sum())}; rows with V ever absent (D off) {int(v_absent(t1['Agent15 D off']).sum())}")
    # M3
    lines = []; ids = identities(res, lines.append)
    for ln in lines: print("      " + ln)
    M3 = ok(all(ids.values())); print(f"   M3 identities (I1)-(I6) on the task seeds: failed {[k for k, v in ids.items() if not v]} -> {M3}")
    # M4
    blines = []; v4, bo, _ = bench(say=blines.append); M4 = ok(v4)
    m4line = [ln for ln in blines if ln.startswith("== M4")]
    rec = [ln.rstrip("\n") for ln in open(BENCH_TXT, encoding="utf-8")] if os.path.exists(BENCH_TXT) else []
    rec4 = [ln for ln in rec if ln.startswith("== M4")]
    for ln in blines:
        if ln.startswith("== M4") or "STOP RULE" in ln or "(hW) measured" in ln: print("      " + ln.strip())
    print(f"   M4 mechanism bench, re-run here on the bench seeds (reading R16) -> {M4}; its M4 line equals ph32_bench.txt's: {m4line == rec4}")
    # M5
    s_on, s_off = s["Agent15 D on"], s["Agent15 D off"]
    m5 = [crit("M5(a) W1D Agent15, reach within 3.0 of B by 600", "P", 0.80, False, s_on["reach"]),
          crit("M5(b) W1 dwell at B, Agent15 D on - D off, paired mean", "DP", BARS["W"], False, s_on["dwell"], s_off["dwell"])]
    cm = s_on["contacts"].mean(); m5.append(ok(cm <= 0.10)); print(f"   M5(c) W1D Agent15, wall contacts per row: mean {cm:.3f}  at most 0.10 -> {m5[-1]}")
    m5.append(crit("M5(d) W1 lost rows (no B whiff in 400-599), Agent15 D on - D off", "DP", 0.05, True, s_on["lost"].astype(float), s_off["lost"].astype(float)))
    M5 = agg(m5); pp, mm, sdd = pass_prob(s_on["dwell"] - s_off["dwell"], BARS["W"])
    print(f"   M5 -> {M5}      reported: dwell mean D on {s_on['dwell'].mean():.3f} / D off {s_off['dwell'].mean():.3f} / Agent14N2 {s['Agent14N2']['dwell'].mean():.3f} / hold-not-read D on"
          f" {s['hold-not-read D on']['dwell'].mean():.3f} / release-off D on {s['release-off D on']['dwell'].mean():.3f} / Agent15g D on {s['Agent15g D on']['dwell'].mean():.3f};"
          f" paired D on - D off {mm:+.3f} sd {sdd:.3f}; lost rows D on {int(s_on['lost'].sum())}, D off {int(s_off['lost'].sum())}")
    # M6
    m6 = [crit("M6 the hold's benefit: W1D lost rows, hold-not-read D on - Agent15 D on", "DP", 0.05, False, s["hold-not-read D on"]["lost"].astype(float), s_on["lost"].astype(float))]
    M6 = agg(m6); dp0, _ = pair_dp(s["hold-not-read D off"]["lost"], s_off["lost"])
    print(f"   M6 -> {M6}      reported: lost rows hold-not-read D on {int(s['hold-not-read D on']['lost'].sum())} vs Agent15 D on {int(s_on['lost'].sum())}; without D the DP is {dp0:+.4f}")
    _, dr, lr, hr_ = interval("DP", s["release-off D on"]["dwell"], s_on["dwell"]); _, dl, ll, hl = interval("DP", s["release-off D on"]["lost"].astype(float), s_on["lost"].astype(float))
    print(f"      reported (2.4): release-off D on - Agent15 D on, dwell {dr:+.3f} [{lr:+.3f}, {hr_:+.3f}], lost rows {dl:+.4f} [{ll:+.4f}, {hl:+.4f}]")
    print(f"   M7 T3aD (REPORTED): neutral dwell 100-599 " + ", ".join(f"{a} {D3[a].mean():.3f}" for a in D3))
    print("   M8 T4 (REPORTED): printed above")
    unread = M1 != "PASS" or max(ties.values()) > 0.20 or M3 != "PASS" or M4 != "PASS" or "UNREADABLE" in (M2, M5, M6)
    verdict = all(x == "PASS" for x in (M1, M2, M3, M4, M5, M6)); fail = any(x == "FAIL" for x in (M2, M5, M6))
    lab = "PASS" if verdict else "UNREADABLE" if unread and not fail else "FAIL" if fail else "INCONCLUSIVE"
    print(f"\n== H27 ==  M1 {M1}  M2 {M2}  M3 {M3}  M4 {M4}  M5 {M5}  M6 {M6}  (M2(a), M7 T3aD, M8 T4 reported) -> {lab}: "
          + ("with a third, irrelevant odour arriving as background whiffs at p_D, the adopted agent composed with three channels keeps its choice in the H21 task within 0.05 of"
             " itself without the distractor; in the absent-odour world it keeps tracking the only relevant plume within the registered dwell and lost-row gaps of itself without"
             " the distractor, and loses at least 5 points fewer rows than the same agent whose navigation does not read the hold" if verdict else
             "UNREADABLE (section 8)" if lab == "UNREADABLE" else "NOT shown under the registered criteria"))


if __name__ == "__main__":
    mode = ([m for m in sys.argv[1:] if m in ("demo", "bench", "dev", "eval")] or ["demo"])[0]
    if mode == "demo": demo(); sys.exit(0)
    if mode == "bench":
        v, o, _ = bench(); sys.exit(0 if v and not o["stop"] else 3 if v else 1)
    main(mode)
