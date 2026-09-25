#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H20 Stage C: the adopted agent (Agent14) with its learning module ON in the H15 Run 2 world (the integration check).

Usage: python ph30.py demo | bench | dev | eval

Design: H20 Stage C design v2 FINAL, confirmed by the owner (decision:h20-stage-c-open, '권고안대로 확정하고 Stage C 진행', gloss
'confirm as recommended and proceed with Stage C'): doc d27e6dfe2e2c16183, sha256 f1e19095...453a, stored before this file existed.
The release at negative holds by (N2), signed for Stage C only before any code (decision:release-value-gated-stage-c); the release
stays ON HOLD at negative values outside Stage C (decision:release-negative-scope-on-hold). No adopted module is edited (ph4, ph8,
ph11, ph13, ph14, ph15, ph16, ph19, ph21, ph23, ph24, ph28 are imported unchanged; their sha256 is printed in every output header):
  - the harness `Sim` is ph15.simulate (ph15.py:79-118) step for step, plus (1) the per-step mirror (design 3.3 A): before every act
    the module's own read-out stack(mb.valence(codes[:, 0]), mb.valence(codes[:, 1])) (or its min(v, 0), positive-off) is written
    into the agent's existing attribute `known`; (2) the Stage C measures (design section 5); (3) optional per-step snapshots for
    lockstep identity checks. Its measure test is `rule not in ('random', 'oracle')` instead of ph15's `rule == 'agent'` (for Agent3
    the same set of rows; Agent6 reuses `rule` as the gate flag, ph19.py:42).
  - (N2): ReleaseN2 repeats the eight lines of ph24.Release.act (ph24.py:54-63) with one row mask; Agent14N2 = ReleaseN2 + ph28.Agent14
    (MRO Agent14N2, ReleaseN2, Agent14, Release, Agent9, ...: the base act is Agent9's, the counter starts at 240 as in Agent14).
Run-time hooks: ph15.simulate is replaced by this harness only inside the reproduction (r) (context `ph15_sim`), and ph24.make only
inside identity (i5) (inside i5_check); both are restored afterwards. ph15's statistics constants are set to this design's (95
percent, bootstrap seed 20261093) and to H15 Run 2's (97.5 percent, 20260920) only inside the reproduction.

Readings where the design is silent, chosen so that the identities stay exact (printed again in the bench output):
 (R1) The mirror is written after the step's sense and wind draws and before act (no generator is consumed by the read-out; the
      weights do not change between the previous step's update and act, so the value equals the read-out 'immediately before act').
 (R2) 'Bitwise on every recorded field' (i1, i3, i4, i6, i7): the arms run in lockstep and are compared on every (step, row) on POS,
      HEAD, H, NAV, S, SG, SIL, SINCE, EST, TURN, W and mb.w, plus TGT, TO, EV, C (the counter) where both agents expose them, and on
      every end-of-run array of the harness record (g, b, first/last steps, visits, val, w_end, pos_end, contacts, ...).
 (R3) (N2), as recorded with decision:release-value-gated-stage-c: the held odour of (S) is the odour held when the step begins (hp);
      of (Z) the odour whose hold forms on the step (h); the value is chan_valence() (the mirror or the supplied known).
 (R4) (i7): (N2) vs (N1) compared on every row on every step before the first step on which the (N1) arm holds a negatively valued
      odour (rows that never do: every step); the no-learning pair (0/0) on every step of every row.
 (R5) (i8): row 0 displaced to the other source after construction (ph15.run_e1's displace) in E1, to the rewarding source after
      training in E2; every per-row record of rows 1-399 equal; learning calls == steps in learning-on arms, 0 in frozen arms; the
      mirror compared with a fresh read-out after act on EVERY step (which includes steps 0, 2699, 5399 and every step a value changes).
 (R6) (v) exactness claims (the no-candidate rule) are read where the design states them (3.1 'v_R rises by 0.1 per reinforced step
      from 0'; section 10 'v_R = 0.1k exactly for k <= 10 then 1.0 ... the punisher's residual +0.01uk while R is learned, exactly 0.0
      where u = 0'): the rewarding odour learned from the naive state, sequences (1) and (3) reward-first, every row: v_R == 0.1k to
      1e-12 for k <= 10, and v_P exactly 0.0 in u = 0 rows on every step before the first punished step. In the punisher-first
      sequences ((2), (3) punish-first) v_R starts at -0.01um (design 3.8) and, in (3) punish-first, the punisher's reinforcement trace
      is still alive after the 50-step gap, so the potentiation term the design names in 3.1 (0.3 x 0.8^gap per step) enters; there the
      increment and the offsets are printed and reported, not claimed. Masks (gate, top, keep, H19 (a) v >= 0, flee v < 0) recomputed for
      h in {-1, 0, 1}, both odours present, with the values and with an order-and-sign canonical pair; printed.
 (R7) (g): ph24.stub's construction (Still world, uniform draws from the world seed, agent from the agent seed; bench E1 seeds), a
      whiff on channel 1 at step 0 and none after, 40 steps, known (1.0, v); peak = max over steps of the median over rows of s_1;
      holds = channel 1 held on any step. Agent14N2 (no negative value: == Agent14).
 (R8) (n): the same stub, known (1.0, -0.9), channel 1 held (s 2.0) at step 0, 260 silent steps; the evidence variant: 100 silent
      steps, then channel-0 whiffs at p 0.30 for 160 steps.
 (R9) (i9): Still world, channel 1 held (s 2.0), the module stepped once with channel 1's code and punishment (compartment 0): v_1
      0 -> -0.1; one act with the mirror and one with `known` left at 0/0 (the same construction and seeds).
 (R10) Pass probabilities (design section 7): b = discordant fraction, sd = sqrt(b - DP^2), se = sd / sqrt(n), n the group size;
      'at most' Phi((bar - DP)/se - 1.96), 'at least' Phi((DP - bar)/se - 1.96); sd 0: the point decides.
 (R11) G3 = P-start rows with a punished step in the learned arm, used for every arm; G5 = rows rewarded at least once in the learned
      arm; M5(a) each arm's own first punished step (ph15.py:280-281: last_g > first_b); G3+ = G3 rows whose Agent14 no-learning
      last-third punishing dwell is above 0.
 (R12) (hR): the GM's 95 percent bootstrap lower bound >= 10 on the bench G3.
 (R13) The E2 bench seeds 20261094/20261095 carry the E2-C harness checks (identical training in every arm, (i8) in E2) and the E2-C
      arms are printed beside; no rule reads them.
 (R14) dev and eval re-run the bench for M9 (as ph28 and ph29 did) and report whether every re-run bench line equals ph30_bench.txt.
 (R15) (i5): the harness's builder is hooked into ph24.make for Agent14 during one ph28.run('T1', ...) call on 2005/2107.
 (R16) E2 'reach the rewarding source' = first_g >= 0 over the test; E2 punishing dwell = b summed over the three test blocks.
 (R17) M1(b) arms: learned, H15 Run 2's agent, positive-off, no-learning, known-answer, as composed, H15 no-learning, H15 known.
 (R18) Arms run in parallel processes (fork); each builds its own generators from the seeds (one world generator and one agent
      generator per arm); the demo checks that a parallel result equals a sequential one bitwise.
 (R19) A punisher hold at a positive residual: a hold on the punisher's odour forms (held after the step, not held before) while the
      punisher's LEARNED value in the module's own read-out is > 0 (not the arm's read-out, which positive-off clips; fixed after the
      first bench run, see the demo header). R absent before the first punisher visit: Agent14's counter for R >= 300 at that step; and,
      for every arm, 300 or more steps since the last R whiff.
 (R20) Wall between: a contact on any step after the first punished step up to and including the first rewarded step after it (to
      the end of the run if there is none).
Nothing changes after the table.
"""
import sys, os, re, io, math, hashlib, contextlib
import multiprocessing as mp
import numpy as np
import ph28                                               # Agent14; hooks ph24.make / ph23.make (sets its own bootstrap seed)
import ph4, ph8, ph9, ph11, ph13, ph14, ph15, ph16, ph19, ph21, ph23, ph24, ph25, ph25b
from ph9 import STEPS
from ph11 import RESET_AFTER, MB
from ph14 import Agent3
from ph15 import World6, inputs, valences, make_agent, late, unrec
from ph16 import Still, World7
from ph18 import majority, agg
from ph21 import Agent8, G_STAR
from ph24 import Release, Agent10
from ph28 import Agent14

sys.stdout.reconfigure(newline="\n")            # LF output, so the recorded sha256 equals the committed blob
DESIGN = "H20 Stage C v2 FINAL doc d27e6dfe2e2c16183 hash f1e1909566310ecafaeb589491d946b9d9526a8f1a5dc9d4b6ee46d2ae27453a"
R, T1, T2 = 400, ph15.BLOCKS*STEPS, ph15.TEST_BLOCKS*STEPS         # 400 rows, 5400 steps (E1-C), 1800 test steps (E2-C)
SEEDS = dict(dev=((9982, 9984), (9986, 9988)), eval=((2037, 2115), (2043, 2141)))
BENCH = dict(e1=(20261091, 20261092), e2=(20261094, 20261095), boot=20261093, steps_g=40, steps_n=260)
REPRO = ((1640, 1740), (1641, 1741))            # H15 Run 2's evaluation seeds: the reproduction (r) only; NOT in the seed scan
RUN2_TXT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "experiments", "h15", "ph15_run2.txt")
BENCH_TXT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "experiments", "h20", "ph30_bench.txt")
STAGEB_SUPPLIED = dict(V=369, N=30, tie=1, cells=((91, 8, 1), (90, 10, 0), (95, 5, 0), (93, 7, 0)))   # experiments/h20/ph29_eval.txt:26-27
Z95, QLO95, QHI95 = 1.959964, 2.5, 97.5
RUN2_STATS = (2.2414, 1.25, 98.75, 20260920)    # ph15.py:25
MODS = (ph4, ph8, ph9, ph11, ph13, ph14, ph15, ph16, ph19, ph21, ph23, ph24, ph25, ph25b, ph28)
NPROC = int(os.environ.get("PH30_PROCS", "4"))


def set_stats(z, lo, hi, seed):
    ph15.Z, ph15.QLO, ph15.QHI, ph15.BOOT_SEED = z, lo, hi, seed; ph15._idx.clear()


set_stats(Z95, QLO95, QHI95, BENCH["boot"])      # design section 7 (after the imports, which set their own); the resample cache emptied


def sha(p=__file__): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def Phi(x): return 0.5*(1.0 + math.erf(x/math.sqrt(2.0)))
def q3(x, f=".0f"): return f"{np.percentile(x, 25):{f}}/{np.median(x):{f}}/{np.percentile(x, 75):{f}}" if len(x) else "n/a"
def fx(x): return f"{x:.15g}"


# ------------------------------------------------------------------ (N2): the release only at non-negative held values (decision:release-value-gated-stage-c)
class ReleaseN2(Release):
    """ph24.Release.act (ph24.py:54-63) with one row mask: (S) is not applied while the odour held when the step begins has a negative
    value in the agent's own read-out, (Z) not while the odour whose hold forms has one (reading R3). No negative held value: IS Release."""

    def act(self, w, whiffs, wind_on):
        if not self.release: return Release.act(self, w, whiffs, wind_on)
        rows = np.arange(self.R); hp = self.held()
        turn, h = super(Release, self).act(w, whiffs, wind_on)                                       # the base act (Agent9's)
        v = self.chan_valence()
        hit = (h >= 0) & whiffs[rows, np.maximum(h, 0)]
        new = (h >= 0) & (h != hp)
        negS = (hp >= 0) & (v[rows, np.maximum(hp, 0)] < 0.0)                                          # (N2), reading R3
        negZ = (h >= 0) & (v[rows, np.maximum(h, 0)] < 0.0)
        base = self.due_timeout & ~self.due_evidence & (self.sel.s > 1.0).any(1) & ~hit
        sustain = base & ~negS                                                                          # (S)
        newz = new & ~negZ                                                                              # (Z)
        self.sustain, self.zreset = sustain, newz & ~sustain & (self.silence > 0)                       # measurement
        self.n2S, self.n2Z = base & negS, new & negZ                                                    # measurement: withheld
        self.silence = np.where(sustain, RESET_AFTER + 1.0, np.where(newz, 0.0, self.silence))
        return turn, h


class Agent14N2(ReleaseN2, Agent14):
    """Agent14 (Release + Agent9, counter start 240, window 300) with the release applied only at non-negative held values (N2)"""


# ------------------------------------------------------------------ construction
def kv_of(vals, good):
    n = len(good); r = np.arange(n)
    if vals == "zero": return np.zeros((n, 2))
    if vals == "pm": k = np.full((n, 2), -1.0); k[r, good] = 1.0; return k
    return np.zeros((n, 2))                                                                             # placeholder; the mirror overwrites it


def build(kind, runs, rng, w, vals):
    """kind: 'A14N2' | 'A14' (N1) | 'A10' | 'A8po' | Agent3 arms of ph15.make_agent ('intact', 'no-learning', 'known', 'random', 'oracle')"""
    if kind in ("A14N2", "A14"):
        cls = Agent14N2 if kind == "A14N2" else Agent14
        return cls(runs, rng, P=ph28.P_PRIOR, N_hi=ph28.N_HI, G=G_STAR, known=kv_of(vals, w.good), rule=True, filt=True, scope="prior", release=True)
    if kind == "A10": return Agent10(runs, rng, G=G_STAR, known=kv_of(vals, w.good), rule=True, filt=True, release=True)
    if kind == "A8po": return Agent8(runs, rng, G=0.0, known=None, rule=False, filt=False)
    return make_agent(kind, runs, rng, w)


#            kind, values, learn, mirror
E1ARMS = {"learned": ("A14N2", None, True, "v"), "H15 agent": ("intact", None, True, None), "positive-off": ("A14N2", None, True, "min"),
          "no-learning": ("A14N2", "zero", False, None), "known-answer": ("A14N2", "pm", False, None), "as composed (N1)": ("A14", None, True, "v"),
          "H15 no-learning": ("no-learning", None, False, None), "H15 known": ("known", None, False, None),
          "random": ("random", None, False, None), "oracle": ("oracle", None, False, None),
          # identity arms
          "H15 agent + mirror": ("intact", None, True, "v"), "H15 agent + min mirror": ("intact", None, True, "min"),
          "Agent8 pathway-off": ("A8po", None, True, "v"), "Agent10 0/0": ("A10", "zero", False, None), "N1 no-learning": ("A14", "zero", False, None)}
AGENT_ARMS = ("learned", "H15 agent", "positive-off", "no-learning", "known-answer", "as composed (N1)", "H15 no-learning", "H15 known")
LEARN_ON = ("learned", "H15 agent", "positive-off", "as composed (N1)", "H15 agent + mirror", "H15 agent + min mirror", "Agent8 pathway-off")
#            kind, group, learn in the test, mirror
E2ARMS = {"trained, learning on": ("A14N2", "trained", True, "v"), "H15 agent trained, learning on": ("intact", "trained", True, None),
          "sham, frozen": ("A14N2", "sham", False, "v"), "trained, frozen": ("A14N2", "trained", False, "v"),
          "trained, learning on, as composed (N1)": ("A14", "trained", True, "v")}
E2_LEARN_ON = ("trained, learning on", "H15 agent trained, learning on", "trained, learning on, as composed (N1)")


def readout(a):
    return np.stack([a.mb.valence(a.codes[:, 0]), a.mb.valence(a.codes[:, 1])], 1)


def mirror_of(a, mode):
    v = readout(a); return np.minimum(v, 0.0) if mode == "min" else v


def agentish(a): return getattr(a, "rule", None) not in ("random", "oracle")


# ------------------------------------------------------------------ the harness: ph15.simulate step for step (ph15.py:79-118) + mirror + measures
class Sim:
    def __init__(self, w, a, steps, learn, mirror=None, legacy=False, keep_src=False, trace=False):
        self.w, self.a, self.steps, self.learn, self.mirror, self.legacy, self.trace = w, a, steps, learn, mirror, legacy, trace
        n = a.R; nb = steps // STEPS; self.rows = rows = np.arange(n)
        self.o = o = dict(g=np.zeros((nb, n)), b=np.zeros((nb, n)), first_g=np.full(n, -1), first_b=np.full(n, -1),
                          last_g=np.full(n, -1), last_b=np.full(n, -1), plume_late=np.zeros(n, bool), contacts=np.zeros(n),
                          nearwall=np.zeros(n), none_held=np.zeros(n), w_none=np.zeros(n), h_none=np.zeros(n),
                          w_other=np.zeros(n), h_other=np.zeros(n), visits_g=np.zeros(n), visits_b=np.zeros(n),
                          long_g=np.zeros(n), val=np.zeros((nb, n, 2)), calls=0, merged=0,
                          good=w.good.copy(), pstart=w.start != w.good, codes=a.codes.copy())
        self.src = np.full((steps, n), -1, np.int8) if keep_src else None
        self.pg = np.zeros(n, bool); self.pb = np.zeros(n, bool); self.run_g = np.zeros(n)
        self.ag = agentish(a)
        # Stage C measures (design section 5; readings R19, R20)
        o.update(mirror_bad=0, viol_h19=0, viol_flee=0, neg_steps=np.zeros(n), first_neg=np.full(n, -1), hold_pos=np.zeros(n),
                 sinceR=np.zeros(n), sinceR_b=np.full(n, -1.0), cR_b=np.full(n, -1.0), g_after_b=np.full(n, -1), wall_between=np.zeros(n, bool),
                 n2S=np.zeros(n), n2Z=np.zeros(n))

    def step(self, t):
        w, a, o, rows = self.w, self.a, self.o, self.rows
        k = t // STEPS
        whiffs = w.sense(); plume = w.plume
        on = w.wind_on()
        if self.mirror is not None: a.known = mirror_of(a, self.mirror)                                  # the per-step mirror (R1)
        hp = a.held() if self.ag else None
        turn, h = a.act(w, whiffs, on)
        if self.ag:
            v = a.chan_valence()
            if self.mirror is not None: o["mirror_bad"] += int(not np.array_equal(a.known, mirror_of(a, self.mirror)))   # R5
            vh = v[rows, np.maximum(h, 0)]; neg = (h >= 0) & (vh < 0)
            o["neg_steps"] += neg; o["first_neg"] = np.where((o["first_neg"] < 0) & neg, t, o["first_neg"])
            bad = 1 - w.good
            o["hold_pos"] += (h == bad) & (hp != bad) & (readout(a)[rows, bad] > 0)                    # R19: the module's learned residual
            o["viol_h19"] += int(((h < 0) & a.nav_hit & ~(whiffs & (v >= 0)).any(1)).sum())
            if hasattr(a, "tgt"): o["viol_flee"] += int((neg & (a.tgt != a.flee_side)).sum())
            if hasattr(a, "n2S"): o["n2S"] += a.n2S; o["n2Z"] += a.n2Z
        snap = None
        if self.trace:
            snap = dict(H=h.copy(), S=a.sel.s.copy(), SG=a.sel.S[:, 0].copy(), SIL=np.array(a.silence, float).copy(), SINCE=np.array(a.since, float).copy(),
                        TURN=np.array(turn, float).copy(), W=whiffs.copy(), EST=np.array(getattr(a, "est", np.zeros(a.R)), float).copy())
            if hasattr(a, "nav_hit"): snap["NAV"] = a.nav_hit.copy()
            for key, att in (("TGT", "tgt"), ("TO", "due_timeout"), ("EV", "due_evidence"), ("C", "c")):
                if hasattr(a, att): snap[key] = np.array(getattr(a, att)).copy()
        w.move(turn); a.bump(w.bumped)
        at = w.at_source()
        if self.learn:
            if self.legacy: ph15.learn_legacy(a, w)
            else:
                code, rv = inputs(a.codes, w.good, at); a.mb.step(code=code, reinf=rv)
            o["calls"] += 1; o["merged"] += int((at.sum(1) == 2).sum())
        g = at[rows, w.good]; b = at[rows, 1 - w.good]
        o["g"][k] += g; o["b"][k] += b
        newb = (o["first_b"] < 0) & b
        for key, x in (("g", g), ("b", b)):
            o["first_" + key] = np.where((o["first_" + key] < 0) & x, t, o["first_" + key])
            o["last_" + key] = np.where(x, t, o["last_" + key])
        o["visits_g"] += g & ~self.pg; o["visits_b"] += b & ~self.pb; self.pg, self.pb = g, b
        self.run_g = (self.run_g + 1)*g; o["long_g"] = np.maximum(o["long_g"], self.run_g)
        if t >= self.steps - 3*STEPS: o["plume_late"] |= plume
        o["contacts"] += w.bumped
        if t >= self.steps - 3*STEPS: o["nearwall"] += np.minimum(w.pos, w.arena - w.pos).min(1) < 1.0
        if self.ag:
            anyw = whiffs.any(1); held = np.where(h >= 0, whiffs[rows, np.maximum(h, 0)], False)
            none = h < 0; other = (h >= 0) & anyw & ~held
            o["none_held"] += none; o["w_none"] += none & anyw; o["h_none"] += none & anyw & a.nav_hit
            o["w_other"] += other; o["h_other"] += other & a.nav_hit
        if self.src is not None: self.src[t] = np.where(at[:, 0] & at[:, 1], 2, np.where(at[:, 0], 0, np.where(at[:, 1], 1, -1)))
        if (t + 1) % STEPS == 0 and self.ag: o["val"][k] = valences(a.mb, a.codes, w.good)
        # Stage C measures
        o["sinceR"] = np.where(whiffs[rows, w.good], 0.0, o["sinceR"] + 1.0)
        o["sinceR_b"] = np.where(newb, o["sinceR"], o["sinceR_b"])
        if hasattr(a, "c"): o["cR_b"] = np.where(newb, a.c[rows, w.good], o["cR_b"])
        pend = (o["first_b"] >= 0) & (o["first_b"] < t) & (o["g_after_b"] < 0)
        o["wall_between"] |= pend & w.bumped
        o["g_after_b"] = np.where(pend & g, t, o["g_after_b"])
        if snap is not None: snap.update(POS=w.pos.copy(), HEAD=w.head.copy(), MBW=a.mb.w)
        return snap

    def finish(self):
        o = self.o; o["src"] = self.src; o["steps"] = self.steps; o["w_end"] = self.a.mb.w.copy(); o["pos_end"] = self.w.pos.copy()
        return o

    def run(self):
        for t in range(self.steps): self.step(t)
        return self.finish()


def sim_ph15(w, a, steps, learn, legacy=False, keep_src=False):
    """ph15.simulate's signature on this harness (mirror off), for the reproduction (r)"""
    o = Sim(w, a, steps, learn, None, legacy, keep_src).run()
    for k in list(o):
        if k in STAGEC_KEYS: del o[k]
    return o


STAGEC_KEYS = ("mirror_bad", "viol_h19", "viol_flee", "neg_steps", "first_neg", "hold_pos", "sinceR", "sinceR_b", "cR_b", "g_after_b", "wall_between", "n2S", "n2Z")


@contextlib.contextmanager
def ph15_sim():
    keep = ph15.simulate; ph15.simulate = sim_ph15
    try: yield
    finally: ph15.simulate = keep


@contextlib.contextmanager
def run2_stats():
    set_stats(*RUN2_STATS)
    try: yield
    finally: set_stats(Z95, QLO95, QHI95, BENCH["boot"])


# ------------------------------------------------------------------ arms (one world generator and one agent generator per arm)
def e1_sim(name, seeds, runs=R, steps=T1, displace=None, trace=False):
    kind, vals, learn, mirror = E1ARMS[name]
    w = World6(runs, np.random.default_rng(seeds[0]), seeds[0], "balanced")
    a = build(kind, runs, np.random.default_rng(seeds[1]), w, vals)
    if displace is not None: w.pos[displace] = w.src[displace, 1 - w.good[displace]]                    # ph15.py:124
    return Sim(w, a, steps, learn, mirror, trace=trace)


def train(a, w, seeds, group, gap=ph15.GAP):
    """ph15.run_e2's training (ph15.py:148-160), verbatim in effect, on the agent's own module"""
    runs = a.R; rows = np.arange(runs); rf = np.zeros(runs, bool)
    rf[np.random.default_rng(seeds[0] + 20_000).permutation(runs)[:runs // 2]] = True      # reward first
    calls = 0
    for phase in (0, 1):
        at_good = rf if phase == 0 else ~rf
        k = np.where(at_good, w.good, 1 - w.good); code = a.codes[rows, k]
        rv = np.zeros((runs, 4))
        if group != "sham": rv[rows, np.where(at_good, 1, 0)] = 1.0
        for _ in range(ph15.TRAIN): a.mb.step(code=code, reinf=rv); calls += 1
        if phase == 0:
            for _ in range(gap): a.mb.step()
    pre = valences(a.mb, a.codes, w.good)
    a.mb.tc[:] = 0.0; a.mb.tr[:] = 0.0
    return pre, calls, rf


def e2_sim(name, seeds, runs=R, steps=T2, displace=None, trace=False):
    kind, group, learn, mirror = E2ARMS[name]
    w = World6(runs, np.random.default_rng(seeds[0]), seeds[0], "all_p")
    a = build(kind, runs, np.random.default_rng(seeds[1]), w, None)
    pre, calls, rf = train(a, w, seeds, group)
    if displace is not None: w.pos[displace] = w.src[displace, w.good[displace]]
    s = Sim(w, a, steps, learn, mirror, trace=trace); s.o.update(pre=pre, train_calls=calls, reward_first=rf, w_train=a.mb.w.copy()); return s


def rowequal(s1, s2):
    ks = [k for k in s1 if k in s2]; n = s1["H"].shape[0]; e = np.ones(n, bool)
    for k in ks: e &= (np.asarray(s1[k]) == np.asarray(s2[k])).reshape(n, -1).all(1)
    return e, ks


def end_equal(o1, o2, skip=()):
    diff = []
    for k in sorted(set(o1) & set(o2)):
        if k in skip: continue
        x, y = o1[k], o2[k]
        if isinstance(x, np.ndarray) or isinstance(y, np.ndarray):
            if x is None or y is None:
                if not (x is None and y is None): diff.append(k)
            elif not np.array_equal(x, y): diff.append(k)
        elif isinstance(x, (int, float, np.integer, np.floating)) and x != y: diff.append(k)
    return diff


def lockstep(sims):
    """run the sims step for step; eq[j][t, r]: sim j+1 equal to sim 0 at step t on the common snapshot fields (reading R2)"""
    steps, n = sims[0].steps, sims[0].a.R; eq = [np.ones((steps, n), bool) for _ in sims[1:]]; keys = [None]*(len(sims) - 1)
    for t in range(steps):
        sn = [s.step(t) for s in sims]
        for j in range(1, len(sims)): eq[j - 1][t], keys[j - 1] = rowequal(sn[0], sn[j])
    return [s.finish() for s in sims], eq, keys


# ------------------------------------------------------------------ jobs (run in worker processes; reading R18)
def job(spec):
    kind = spec[0]
    if kind == "e1":
        _, name, seeds, runs, steps, displace = spec; return e1_sim(name, seeds, runs, steps, displace).run()
    if kind == "e2":
        _, name, seeds, runs, steps, displace = spec; return e2_sim(name, seeds, runs, steps, displace).run()
    if kind == "lock1":
        _, names, seeds, runs, steps = spec
        outs, eq, keys = lockstep([e1_sim(nm, seeds, runs, steps, trace=True) for nm in names]); return dict(outs=outs, eq=eq, keys=keys)
    if kind == "lock2":
        _, names, seeds, runs, steps = spec
        outs, eq, keys = lockstep([e2_sim(nm, seeds, runs, steps, trace=True) for nm in names]); return dict(outs=outs, eq=eq, keys=keys)
    if kind == "repro_e1":
        _, arm = spec
        with ph15_sim(): return ph15.run_e1(arm, REPRO[0], keep_src=arm == "intact")
    if kind == "repro_field":
        _, which = spec
        if which == "e1":
            ref = ph15.run_e1("intact", REPRO[0], keep_src=True)
            with ph15_sim(): mine = ph15.run_e1("intact", REPRO[0], keep_src=True)
        else:
            ref = ph15.run_e2("trained", REPRO[1], learn_on=True)
            with ph15_sim(): mine = ph15.run_e2("trained", REPRO[1], learn_on=True)
        return dict(diff=end_equal(ref, mine), keys=sorted(ref), same_keys=sorted(ref) == sorted(mine))
    raise ValueError(kind)


def pool_run(specs):
    if NPROC <= 1: return [job(s) for s in specs]
    ctx = mp.get_context("fork")
    with ctx.Pool(NPROC) as p: return p.map(job, specs, chunksize=1)


# ------------------------------------------------------------------ statistics (design section 7)
def pp(dp, b, n, bar, most):
    """reading R10"""
    sd = math.sqrt(max(b - dp*dp, 0.0))
    if sd <= 0: return float(dp <= bar) if most else float(dp >= bar)
    se = sd/math.sqrt(n); return Phi(((bar - dp) if most else (dp - bar))/se - Z95)


def pp_pair(x, y, bar, most):
    x, y = np.asarray(x, bool), np.asarray(y, bool); dp = float(x.mean() - y.mean()); b = float((x != y).mean())
    return pp(dp, b, len(x), bar, most), dp, b


def binom_le(k, n, p): return float(sum(math.comb(n, j)*p**j*(1 - p)**(n - j) for j in range(0, k + 1)))


def wilson95(k, n):
    z = Z95; p = k/n; d = 1 + z*z/n; c = (p + z*z/(2*n))/d; h = z*math.sqrt(p*(1 - p)/n + z*z/(4*n*n))/d; return c - h, c + h


def crit(label, kind, thr, most, a, b=None, n_min=50, say=print):
    n = len(a)
    if n < n_min: say(f"   {label}: n {n} < {n_min} -> UNREADABLE"); return "UNREADABLE"
    extra = ""
    if kind == "P":
        k = int(np.sum(a)); pt, lo, hi = ph15.wilson(k, n); extra = f"k {k} "
    elif kind == "WIN":
        k = int(np.sum(np.asarray(a) < np.asarray(b))); ties = float(np.mean(np.asarray(a) == np.asarray(b))); extra = f"k {k} ties {ties*100:.1f}% "
        if ties > 0.20: say(f"   {label}: WIN {extra}n {n} -> UNREADABLE (ties)"); return "UNREADABLE"
        pt, lo, hi = ph15.wilson(k, n)
    else:
        pt, lo, hi = ph15.boot(kind, a, b)
    out = ph15.verdict(lo, hi, thr, most)
    say(f"   {label}: {kind} {extra}n {n}  value {pt:.3f}  95% interval [{lo:.3f}, {hi:.3f}]  {'at most' if most else 'at least'} {thr} -> {out}")
    return out


# ------------------------------------------------------------------ constructed states: stub, (v), (g), (n), (i9)
def stub(kind, known, sched, hold=None, rows=R, seeds=BENCH["e1"]):
    """ph24.stub's construction (ph24.py:152-162) with this harness's builder (readings R7, R8)"""
    steps = sum(s for s, _, _ in sched); u = np.random.default_rng(seeds[0]).random((steps, rows, 2))
    good = np.zeros(rows, int)
    class Wd: pass
    wd = Wd(); wd.good = good
    a = build(kind, rows, np.random.default_rng(seeds[1]), wd, None); a.known = np.tile(np.asarray(known, float), (rows, 1)); w = Still(rows)
    if hold is not None: a.sel.s[:, hold] = 2.0
    H = np.full((steps, rows), -1, np.int8); S = np.zeros((steps, rows, 2)); TO = np.zeros((steps, rows), bool); EV = np.zeros((steps, rows), bool)
    FL = np.zeros((steps, rows), bool); t = 0
    for n, p0, p1 in sched:
        for _ in range(n):
            x = np.stack([u[t, :, 0] < p0, u[t, :, 1] < p1], 1)
            _, h = a.act(w, x, np.ones(rows, bool)); H[t] = h; S[t] = a.sel.s; TO[t] = a.due_timeout; EV[t] = a.due_evidence; FL[t] = a.tgt == a.flee_side; t += 1
    return dict(H=H, S=S, TO=TO, EV=EV, FL=FL, H0=np.full(rows, -1 if hold is None else hold))


def overlap(codes): return (codes[:, 0]*codes[:, 1]).sum(1).astype(int)


def canon(v):
    """an order-and-sign canonical pair: negative -1 or -2 (by order), zero 0, positive 1 or 2 (by order); ties kept"""
    s = np.sign(v); a = np.abs(v); o = a[:, ::-1]
    bigger = (a > o) & (s == s[:, ::-1])
    return s*(1.0 + bigger)


def masks_all(v):
    """gate (ph23.py:66), top (:88-89), keep (:91), H19 (a) (v >= 0), flee (val < 0), for h in {-1, 0, 1}, both odours present"""
    n = len(v); r = np.arange(n); out = {}
    ge = v >= 0; vmax = v.max(1); top = ge & (v == vmax[:, None]); out["top"] = top; out["h19"] = ge
    for hh in (-1, 0, 1):
        hp = np.full(n, hh); vh = v[r, max(hh, 0)]
        out[f"gate h{hh}"] = (hp >= 0)[:, None] & ge & (v < vh[:, None])
        out[f"keep h{hh}"] = (hp >= 0) & ((vh == vmax) | (vh < 0)); out[f"flee h{hh}"] = (hp >= 0) & (vh < 0)
    return out


def value_trajectories(good, say):
    """bench (v), reading R6"""
    n = len(good); r = np.arange(n); m = ph8.MB4(n, parallel=False, gated=True, rng=np.random.default_rng(0), **MB)
    codes = np.stack([m.odour(101), m.odour(102)], 1); u = overlap(codes); cR, cP = codes[r, good], codes[r, 1 - good]
    seqs = {"(1) R 8, silent 200, P 9": [("R", 8), ("-", 200), ("P", 9)], "(2) P 9, silent 200, R 8": [("P", 9), ("-", 200), ("R", 8)],
            "(3a) E2 reward-first R 30, gap 50, P 30": [("R", 30), ("-", 50), ("P", 30)], "(3b) E2 punish-first P 30, gap 50, R 30": [("P", 30), ("-", 50), ("R", 30)]}
    ok = dict(inc=True, abs=True, p0=True); masks_ok = {}; dev = {}
    for lab, seq in seqs.items():
        mm = ph8.MB4(n, parallel=False, gated=True, rng=np.random.default_rng(0), **MB)
        rv = np.zeros((n, 4)); z = np.zeros((n, 4)); vs = []; phase = []
        for kind, k in seq:
            for i in range(k):
                if kind == "R": rr = z.copy(); rr[:, 1] = 1.0; mm.step(code=cR, reinf=rr)
                elif kind == "P": rr = z.copy(); rr[:, 0] = 1.0; mm.step(code=cP, reinf=rr)
                else: mm.step()
                vs.append(np.stack([mm.valence(cR), mm.valence(cP)], 1)); phase.append((kind, i + 1))
        V = np.array(vs); rfirst = seq[0][0] == "R"; nsil = [s for s in seq if s[0] == "-"][0][1]
        # exactness
        idx = [j for j, (kd, i) in enumerate(phase) if kd == "R"]; start = idx[0] - 1
        vR0 = V[start, :, 0] if start >= 0 else np.zeros(n)
        incdev, absdev = 0.0, 0.0
        for j in idx:
            kk = phase[j][1]
            if kk <= 10:
                incdev = max(incdev, float(np.abs(V[j, :, 0] - vR0 - 0.1*kk).max())); absdev = max(absdev, float(np.abs(V[j, :, 0] - 0.1*kk).max()))
        if rfirst: ok["abs"] &= absdev <= 1e-12
        else:
            offs = float(np.abs(vR0 + 0.01*u*[p for p in seq if p[0] == "P"][0][1]).max())
            say(f"      (reported, not an exactness claim: R learned after the punisher) max |increment - 0.1k| over k <= 10 {incdev:.3g}; max |v_R before R - (-0.01um)| {offs:.3g};"
                f" max |v_R - 0.1k| {absdev:.3g} (u = 0 rows {float(np.abs(V[idx[:10], :, 0][:, u == 0] - 0.1*np.arange(1, 11)[:len(idx[:10]), None]).max()):.3g})")
        if rfirst:
            pre = [j for j, (kd, i) in enumerate(phase) if not any(p[0] == "P" for p in phase[:j + 1])]
            ok["p0"] &= bool((V[pre][:, u == 0, 1] == 0.0).all())
        # masks order-only
        mo = True
        for j in range(len(V)):
            a1, a2 = masks_all(V[j]), masks_all(canon(V[j]))
            mo &= all(np.array_equal(a1[k], a2[k]) for k in a1)
        masks_ok[lab] = mo
        # printed per step by u (reinforced phases and the first and last silent step)
        say(f"   (v) {lab}: per step, median by u (u=0 {int((u == 0).sum())} / u=1 {int((u == 1).sum())} / u=2 {int((u == 2).sum())} / u=3 {int((u == 3).sum())} rows) v_R | v_P:")
        lines = []
        for j, (kd, i) in enumerate(phase):
            if (kd == "-" and i not in (1, nsil)) or (kd != "-" and 12 < i < dict(seq)[kd]): continue
            cells = " ".join(f"{np.median(V[j, u == q, 0]):+.4f}|{np.median(V[j, u == q, 1]):+.4f}" for q in range(int(u.max()) + 1) if (u == q).any())
            lines.append(f"{kd}{i}: {cells}")
        for s0 in range(0, len(lines), 4): say("        " + "; ".join(lines[s0:s0 + 4]))
        leave = [np.where((V[:, :, c] != 0).any(0), (V[:, :, c] != 0).argmax(0) + 1, -1) for c in (0, 1)]
        say(f"      step on which each value leaves 0 (per row, quartiles; step counted from 1): v_R {q3(leave[0][leave[0] > 0])} (rows {int((leave[0] > 0).sum())}), v_P {q3(leave[1][leave[1] > 0])} (rows {int((leave[1] > 0).sum())})")
        # the design's formulas (reported): residual +0.01 u k while R is learned; R falling by 0.01 u m; v_P = -0.1 m + 0.1 u once R saturated
        jR = [j for j in idx if phase[j][1] <= 10]
        if rfirst:
            devres = max(float(np.abs(V[j, :, 1] - 0.01*u*phase[j][1]).max()) for j in jR)
            jP = [j for j, (kd, i) in enumerate(phase) if kd == "P"][:10]; mP = len(jP); vRb = V[jP[0] - 1, :, 0]
            devR = float(np.abs(V[jP[-1], :, 0] - (vRb - 0.01*u*mP)).max()); vpend = V[jP[-1], :, 1]
            devP = float(np.abs(vpend - (-0.1*mP + 0.1*u)).max()) if seq[0][1] >= 10 else float("nan")
            say(f"      design 3.8 (reported): max |v_P - 0.01uk| while R learned (k <= 10) {devres:.3g}; after {mP} punished steps max |v_R - (v_R before - 0.01um)| {devR:.3g};"
                f" max |v_P - (-0.1m + 0.1u)| {devP:.3g}{' (R saturated)' if seq[0][1] >= 10 else ' (R not saturated: not the formula case)'}; v_P at the end by u: "
                + ", ".join(f"u={q}: {np.median(vpend[u == q]):+.4f}" for q in range(int(u.max()) + 1) if (u == q).any()))
            dev[lab] = (devres, devR, devP)
    say(f"   (v) masks recomputed from the values == from the order-and-sign canonical pair on every step (gate, top, keep, H19 (a), flee; h -1/0/1): "
        + "; ".join(f"{k} {v}" for k, v in masks_ok.items()))
    exact = {"v_R == 0.1k to 1e-12 for k <= 10 (R learned from the naive state: (1), (3a); every row)": ok["abs"],
             "v_P exactly 0.0 in u = 0 rows before punishment ((1), (3a); every pre-punishment step)": ok["p0"]}
    return exact, masks_ok, u


# ------------------------------------------------------------------ header, readings, seed scan
def header(say=print):
    say(f"   ph30.py sha256 {sha()}; design {DESIGN}")
    say("   imported modules: " + "; ".join(f"{os.path.basename(m.__file__)} {sha(m.__file__)}" for m in MODS))
    say(f"   seeds: E1-C dev {SEEDS['dev'][0]}, eval {SEEDS['eval'][0]}; E2-C dev {SEEDS['dev'][1]}, eval {SEEDS['eval'][1]}; bench E1 {BENCH['e1']}, E2 {BENCH['e2']};"
        f" bootstrap {BENCH['boot']} (95 percent, 5000); reproduction (r) on H15 Run 2's {REPRO} only (reused on purpose, read for no criterion, NOT in the seed scan);"
        f" (i5) on Stage B's (2005, 2107) only; demo seeds (3, 4), (5, 6) used deliberately")
    say("   decisions: decision:h20-stage-c-open (the ten points); decision:release-value-gated-stage-c ((N2), Stage C only; decision:release-negative-scope-on-hold stays in"
        " force outside Stage C); the adopted agent: decision:h26-adaptive-presence-adopted-within-tested-conditions")
    say(f"   rows share no state: one world generator and one agent generator per arm, fixed-size draws consumed in row order every step; arms in {NPROC} parallel processes (reading R18)")


def readings(say=print):
    say("   readings where the design is silent (file header R1-R20): R1 mirror written after sense and wind, before act; R2 bitwise = lockstep (step, row) equality on POS, HEAD,"
        " H, NAV, S, SG, SIL, SINCE, EST, TURN, W, mb.w (+ TGT, TO, EV, C where both expose them) and every end-of-run record; R3 (N2): held odour of (S) = hp, of (Z) = h,"
        " value = chan_valence(); R4 (i7) up to the first negative hold of the (N1) arm (exclusive); R5 (i8) row 0 displaced, rows 1-399 equal, calls == steps / 0, mirror"
        " checked every step; R6 (v) exactness claims where R is learned from the naive state ((1), (3a), every row: v_R == 0.1k, k <= 10; v_P == 0.0 at u = 0 before punishment), punisher-first sequences printed, not claimed; R7 (g) ph24.stub construction, bench E1"
        " seeds; R8 (n) known (1.0, -0.9), channel 1 held s 2.0, 260 silent steps, evidence variant 100 silent + channel-0 p 0.30; R9 (i9) one punished module step, mirror vs"
        " stale; R10 pass probabilities se = sqrt(b - DP^2)/sqrt(n); R11 G3/G5 from the learned arm, M5(a) each arm's own first punished step, G3+ from Agent14 no-learning;"
        " R12 (hR) GM lower bound >= 10; R13 E2 bench seeds: E2-C harness checks, arms printed beside; R14 dev/eval re-run the bench for M9; R15 (i5) builder hooked into"
        " ph24.make; R16 E2 reach = first_g >= 0, P dwell = b over the test; R17 M1(b) arms = the eight agent arms; R18 parallel processes; R19 punisher hold at a positive"
        " learned residual (module read-out), R absent (counter >= 300 / 300 steps since an R whiff) at the first punisher visit; R20 wall contact between the first punished step and the next rewarded step")


def seed_numbers():
    base = [*SEEDS["dev"][0], *SEEDS["eval"][0], *SEEDS["dev"][1], *SEEDS["eval"][1], *BENCH["e1"], *BENCH["e2"], BENCH["boot"]]
    worlds = [SEEDS["dev"][0][0], SEEDS["dev"][1][0], SEEDS["eval"][0][0], SEEDS["eval"][1][0], BENCH["e1"][0], BENCH["e2"][0]]
    agents = [SEEDS["dev"][0][1], SEEDS["dev"][1][1], SEEDS["eval"][0][1], SEEDS["eval"][1][1], BENCH["e1"][1], BENCH["e2"][1]]
    return base + [s + 10_000 for s in worlds] + [s + 20_000 for s in worlds] + [s + 20_000 for s in agents] + [BENCH["e1"][0] + 10_000_000, BENCH["e1"][1] + 20_000_000]


def seeds_unused():
    """design section 9: none of the numbers appears in any other file under the repository (recursive, digit-boundary; .git and __pycache__
    excluded; excluded by name: this file, its outputs ph30_*.txt, the Stage C documents h20_stage_c_*.md, master_plan.md, notes/*.md, viewer/*).
    The demo seeds and the reproduction seeds are used deliberately and are NOT part of this check."""
    nums = seed_numbers(); pat = re.compile(rb"(?<!\d)(" + "|".join(map(str, nums)).encode() + rb")(?!\d)"); hits = []; nf = 0
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        top = os.path.relpath(root, repo).replace("\\", "/").split("/")[0]
        for f in files:
            if f == "ph30.py" or (f.startswith("ph30_") and f.endswith(".txt")) or (f.startswith("h20_stage_c_") and f.endswith(".md")) or f == "master_plan.md": continue
            if (os.path.basename(root) == "notes" and f.endswith(".md")) or top == "viewer": continue
            nf += 1
            if pat.search(open(os.path.join(root, f), "rb").read()): hits.append(os.path.relpath(os.path.join(root, f), repo))
    return hits, nums, nf


# ------------------------------------------------------------------ E1-C / E2-C collections
def e1_specs(seeds, runs=R, steps=T1, arms=None, displaced=True):
    """lockstep groups for the identities, single arms, and displaced learning-on arms (i8)"""
    arms = arms or list(AGENT_ARMS) + ["random", "oracle"]
    specs = [("lock1", ["H15 agent", "H15 agent + mirror", "H15 agent + min mirror", "Agent8 pathway-off"], seeds, runs, steps),
             ("lock1", ["learned", "as composed (N1)"], seeds, runs, steps),
             ("lock1", ["no-learning", "Agent10 0/0", "N1 no-learning"], seeds, runs, steps)]
    grouped = {"H15 agent", "learned", "as composed (N1)", "no-learning"}
    specs += [("e1", a, seeds, runs, steps, None) for a in arms if a not in grouped]
    if displaced: specs += [("e1", a, seeds, runs, steps, 0) for a in LEARN_ON]
    return specs


def e2_specs(seeds, runs=R, steps=T2, displaced=True):
    specs = [("lock2", ["trained, learning on", "trained, learning on, as composed (N1)"], seeds, runs, steps)]
    specs += [("e2", a, seeds, runs, steps, None) for a in E2ARMS if a not in ("trained, learning on", "trained, learning on, as composed (N1)")]
    if displaced: specs += [("e2", a, seeds, runs, steps, 0) for a in E2_LEARN_ON]
    return specs


def collect(specs, results):
    arms, disp, locks = {}, {}, []
    for s, r in zip(specs, results):
        if s[0] in ("lock1", "lock2"):
            for nm, o in zip(s[1], r["outs"]): arms[nm] = o
            locks.append((s[1], r["eq"], r["keys"]))
        elif s[5] is None: arms[s[1]] = r
        else: disp[s[1]] = r
    return arms, disp, locks


def drop0(o, n):
    out = {}
    for k, x in o.items():
        if not isinstance(x, np.ndarray) or x.ndim == 0: continue
        if x.shape[0] == n: out[k] = np.delete(x, 0, 0)
        elif x.ndim > 1 and x.shape[1] == n: out[k] = np.delete(x, 0, 1)
    return out


def row_indep(o, od, n):
    a, b = drop0(o, n), drop0(od, n); ks = sorted(set(a) & set(b)); bad = [k for k in ks if not np.array_equal(a[k], b[k])]
    return not bad, bad, len(ks)


def identities(arms, disp, locks, steps, e2=None, say=print):
    """M8 / bench (i): (i1), (i3), (i4), (i6), (i7), (i8) and the mirror check (readings R2, R4, R5)"""
    ids = {}; n = R
    for names, eq, keys in locks:
        src = e2[0] if (names[0] in E2ARMS and e2 is not None) else arms
        ref = src[names[0]]
        for j, nm in enumerate(names[1:]):
            e = eq[j]; o = src[nm]; dif = end_equal(ref, o, skip=("mirror_bad", "viol_flee", "n2S", "n2Z", "cR_b"))
            if names[0] == "H15 agent":
                lab = {"H15 agent + mirror": "(i1) Agent3 + mirror == Agent3 live", "H15 agent + min mirror": "(i4) Agent3 + min(v, 0) mirror == Agent3 live",
                       "Agent8 pathway-off": "(i3) Agent8 G 0, gate off, filter off, mirror == Agent3 live"}[nm]
                ok = bool(e.all()) and not dif
                say(f"   {lab}: every (step, row) equal {bool(e.all())} ({int(e.all(0).sum())}/{n} rows; fields {keys[j]}); end-of-run records equal {not dif}{'' if not dif else ' ' + str(dif)} -> {ok}")
                ids[lab] = ok
            elif names[0] == "no-learning":
                lab = {"Agent10 0/0": "(i6) Agent14 (N2) at 0/0 == Agent10 at 0/0", "N1 no-learning": "(i7) no-learning pair: (N2) == (N1) at 0/0"}[nm]
                ok = bool(e.all()) and not dif
                say(f"   {lab}: every (step, row) equal {bool(e.all())} ({int(e.all(0).sum())}/{n} rows; fields {keys[j]}); end-of-run records equal {not dif}{'' if not dif else ' ' + str(dif)} -> {ok}")
                ids[lab] = ok
            elif names[0] == "learned":
                fn = o["first_neg"]; lim = np.where(fn < 0, steps, fn); before = np.arange(steps)[:, None] < lim[None, :]
                ok = bool((e | ~before).all()); never = fn < 0; whole = e.all(0); ps = arms["learned"]["pstart"]
                fd = np.where((~e).any(0), (~e).argmax(0), -1)
                say(f"   (i7) (N2) == (N1) on every row before its first negative hold (reading R4): {ok}; rows never holding a negative odour in (N1) {int(never.sum())},"
                    f" of them equal throughout {int((never & whole).sum())}; rows with a negative hold {int((~never).sum())} (P-start {int((~never & ps).sum())}, R-start {int((~never & ~ps).sum())}),"
                    f" first negative hold step {q3(fn[~never])}; rows departing at all {int((fd >= 0).sum())}, first departing step {q3(fd[fd >= 0])};"
                    f" departing before the first negative hold {int(((fd >= 0) & (fd < lim)).sum())}")
                ids["(i7) (N2) == (N1) before the first negative hold"] = ok
            elif names[0] == "trained, learning on":
                say(f"      E2 (reported): (N2) vs (N1) trained learning on, rows equal throughout {int(e.all(0).sum())}/{n}")
    # (i8)
    i8 = True; parts = []
    for nm, od in disp.items():
        o = arms[nm]; ok, bad, nk = row_indep(o, od, n); i8 &= ok; parts.append(f"{nm} {ok}{'' if ok else ' ' + str(bad)}")
    say(f"   (i8) row independence (row 0 displaced; every per-row record of rows 1-{n - 1}, reading R5): " + "; ".join(parts))
    calls = {nm: o["calls"] for nm, o in arms.items()}
    c_ok = all(calls[nm] == steps for nm in LEARN_ON if nm in calls) and all(calls[nm] == 0 for nm in calls if nm not in LEARN_ON)
    say(f"   (i8) learning calls: " + ", ".join(f"{nm} {c}" for nm, c in calls.items()) + f" (learning-on arms == {steps}, frozen arms 0) -> {c_ok}")
    mb = {nm: o["mirror_bad"] for nm, o in arms.items() if E1ARMS[nm][3] is not None}
    m_ok = all(v == 0 for v in mb.values())
    say(f"   mirror == a fresh read-out after act on every step (steps with a mismatch): " + ", ".join(f"{nm} {v}" for nm, v in mb.items()) + f" -> {m_ok}")
    ids["(i8) row independence, E1-C learning-on arms"] = i8; ids["(i8) learning calls == steps / 0"] = c_ok; ids["mirror == live read-out on every step"] = m_ok
    if e2 is not None:
        e2arms, e2disp = e2
        i8e = True; parts = []
        for nm, od in e2disp.items():
            ok, bad, nk = row_indep(e2arms[nm], od, n); i8e &= ok; parts.append(f"{nm} {ok}{'' if ok else ' ' + str(bad)}")
        c2 = {nm: (o["calls"], o["train_calls"]) for nm, o in e2arms.items()}
        c2ok = all(c2[nm][0] == T2 if nm in E2_LEARN_ON else c2[nm][0] == 0 for nm in c2) and all(c[1] == 2*ph15.TRAIN for c in c2.values())
        pre_eq = all(np.array_equal(e2arms[nm]["pre"], e2arms["trained, learning on"]["pre"]) for nm in e2arms if E2ARMS[nm][1] == "trained")
        wtr = all(np.array_equal(e2arms[nm]["w_train"], e2arms["trained, learning on"]["w_train"]) for nm in e2arms if E2ARMS[nm][1] == "trained")
        mb2 = {nm: o["mirror_bad"] for nm, o in e2arms.items() if E2ARMS[nm][3] is not None}
        say(f"   (i8) E2-C row independence (row 0 moved to the rewarding source after training): " + "; ".join(parts))
        say(f"   (i8) E2-C calls (test, training): " + ", ".join(f"{nm} {c}" for nm, c in c2.items()) + f" -> {c2ok}; identical training in every trained arm (pre-test values and"
            f" weights bitwise): {pre_eq and wtr}; mirror mismatches " + ", ".join(f"{nm} {v}" for nm, v in mb2.items()))
        ids["(i8) row independence, E2-C learning-on arms"] = i8e; ids["(i8) E2-C calls"] = c2ok; ids["E2-C identical training"] = pre_eq and wtr
        ids["E2-C mirror == live read-out"] = all(v == 0 for v in mb2.values())
    vio = {nm: (o["viol_h19"], o["viol_flee"]) for nm, o in arms.items() if nm in AGENT_ARMS}
    say("   integrity (H19 (a) boundary: a whiff of a negatively valued odour handed to navigation while nothing is held; flee: a negative hold whose target is not the flee side):"
        " " + ", ".join(f"{nm} {a}/{b}" for nm, (a, b) in vio.items()))
    ids["H19 (a) boundary and flee on every (row, step)"] = all(a == 0 and b == 0 for a, b in vio.values())
    return ids


# ------------------------------------------------------------------ Stage C measures, printed per arm (design section 5)
def extras(name, o, g3, say=print):
    ps = o["pstart"]; vb = o["first_b"] >= 0; rs = ~ps; n = len(ps)
    fr = o["first_b"][rs & vb]
    hp = o["hold_pos"]; hasc = (o["cR_b"] >= 0).any()
    ab_c = int(((o["cR_b"] >= 300) & rs & vb).sum()) if hasc else None; ab_s = int(((o["sinceR_b"] >= 300) & rs & vb).sum())
    reach = (o["last_g"] > o["first_b"])[g3]; wb = o["wall_between"][g3]
    say(f"      [{name}] visited P: P-start {int((vb & ps).sum())}/{int(ps.sum())}, R-start {int((vb & rs).sum())}/{int(rs.sum())} (first P visit step, R-start {q3(fr)});"
        f" punisher holds formed at a positive residual: rows {int((hp > 0).sum())}, events {int(hp.sum())} (R-start rows {int(((hp > 0) & rs).sum())});"
        f" R-start first P visits with R absent (counter >= 300) {ab_c if hasc else 'n/a'} / 300+ steps since an R whiff {ab_s} of {int((rs & vb).sum())}")
    say(f"         G3 ({int(g3.sum())} rows): reach after the first punished step {int(reach.sum())}; with a wall contact between it and the next rewarded step {int((reach & wb).sum())},"
        f" without {int((reach & ~wb).sum())}; not reached {int((~reach).sum())} (of them with a wall contact after the first punished step {int((~reach & wb).sum())});"
        f" contacts per agent {o['contacts'].mean():.2f} (P-start {o['contacts'][ps].mean():.2f}, R-start {o['contacts'][rs].mean():.2f}); near wall {o['nearwall'].mean()/(3*STEPS)*100:.2f}%;"
        f" steps holding a negative odour per row {o['neg_steps'].mean():.1f}" + (f"; (N2) withheld (S) {int(o['n2S'].sum())}, (Z) {int(o['n2Z'].sum())}" if o['n2S'].any() or o['n2Z'].any() or name in ('learned', 'positive-off', 'known-answer') else ""))


def print_arm(name, o, g3, groups=True):
    allr = np.ones(len(o["pstart"]), bool); ps = o["pstart"]
    print()
    for m, lab in ((allr, "all"), (ps, "P-start"), (~ps, "R-start")):
        if groups or lab != "R-start": ph15.measures(name[:13], o, m, lab)
    if o["calls"]: print(f"      learning calls {o['calls']} over {o['steps']} steps; two sources in reach on {o['merged']} row-steps")
    if agentish_name(name): extras(name, o, g3)


def agentish_name(name): return name in AGENT_ARMS or name in E2ARMS


# ------------------------------------------------------------------ the mechanism bench (design section 4)
def reproduction(say=print):
    """(r): H15 Run 2 reproduced on its own seeds, every line of experiments/h15/ph15_run2.txt (reading: ph15's own printing code, with
    this harness as ph15.simulate); ph15.simulate's arrays field for field (E1 intact, E2 trained with learning on)"""
    res = pool_run([("repro_e1", arm) for arm in ph15.E1_ARMS] + [("repro_field", "e1"), ("repro_field", "e2")])
    cache = dict(zip(ph15.E1_ARMS, res[:len(ph15.E1_ARMS)])); f1, f2 = res[-2], res[-1]
    buf = io.StringIO(); keep = ph15.run_e1
    ph15.run_e1 = lambda arm, seeds, **kw: cache[arm] if tuple(seeds) == REPRO[0] else keep(arm, seeds, **kw)
    try:
        with run2_stats(), ph15_sim(), contextlib.redirect_stdout(buf):
            print(f"== H15 Run 2, EVAL. specification {ph15.SPEC} ==")
            print("== one amendment recorded before the evaluation: record:h15-run2-dev-log (E2 training gap). Q3(c) not amended. ==")
            ph15.e1("eval"); ph15.e2("eval")
    finally: ph15.run_e1 = keep
    mine = buf.getvalue().split("\n"); ref = open(RUN2_TXT, encoding="utf-8").read().split("\n")
    eqn = sum(1 for a, b in zip(mine, ref) if a == b); same = mine == ref
    say(f"(r) REPRODUCTION of H15 Run 2 (world/agent {REPRO[0]} for E1, {REPRO[1]} for E2; ph15's own e1/e2 printing with this harness as ph15.simulate; H15 Run 2's statistics"
        f" 97.5 percent, bootstrap 20260920): {len(mine)} lines against {len(ref)} in experiments/h15/ph15_run2.txt (sha256 {sha(RUN2_TXT)}); equal line for line {eqn}; identical {same}")
    for i, (a, b) in enumerate(zip(mine, ref)):
        say(f"   (r) {i + 1:3d} {'==' if a == b else '!='} {a}")
        if a != b: say(f"   (r) {i + 1:3d} ref {b}")
    say(f"(r) ph15.simulate's arrays field for field (the original ph15.simulate against this harness): E1 intact {not f1['diff'] and f1['same_keys']} (keys {len(f1['keys'])}, differing {f1['diff']});"
        f" E2 trained, learning on {not f2['diff'] and f2['same_keys']} (keys {len(f2['keys'])}, differing {f2['diff']})")
    return same and not f1["diff"] and not f2["diff"] and f1["same_keys"] and f2["same_keys"]


def constructed(say=print):
    """(v), (g), (n), (i9), (i5)"""
    ids, exact = {}, {}
    w = World6(R, np.random.default_rng(BENCH["e1"][0]), BENCH["e1"][0], "balanced")
    ex, masks_ok, u = value_trajectories(w.good, say); exact.update(ex)
    say(f"   (v) exactness claims (reading R6): " + "; ".join(f"{k} {v}" for k, v in ex.items()))
    # (g)
    one = [(1, 0.0, 1.0), (BENCH["steps_g"] - 1, 0.0, 0.0)]; g = {}
    for v in (0.0, 0.01, 0.025, 0.05, 0.1):
        o = stub("A14N2", (1.0, v), one); s1 = o["S"][:, :, 1]; peak = float(np.median(s1, 1).max()); held = int((o["H"] == 1).any(0).sum()); g[v] = (peak, held)
        say(f"(g) one punisher whiff at step 0 from rest, gain {1 + G_STAR*v:.2f} (v_P {v}): peak of the median s_1 {peak:.3f}; per-row peak quartiles {q3(s1.max(0), '.3f')};"
            f" rows holding the punisher odour on some step {held}/{R}")
    say(f"   (g) Stage B reproduced first: 0.756 at gain 1.0 {round(g[0.0][0], 3) == 0.756}; every row holding at gain 1.2 {g[0.1][1] == R}")
    # (n)
    sil = [(BENCH["steps_n"], 0.0, 0.0)]; ev = [(100, 0.0, 0.0), (BENCH["steps_n"] - 100, 0.30, 0.0)]
    for lab, sch in (("silent", sil), ("R whiffs p 0.30 from step 100", ev)):
        for kind in ("A14", "A14N2"):
            o = stub(kind, (1.0, -0.9), sch, hold=1); H = o["H"]; st = H.shape[0]
            end = np.where((H != 1).any(0), (H != 1).argmax(0), -1); r = np.arange(R)
            byev = (end >= 0) & o["EV"][np.maximum(end, 0), r]; byto = (end >= 0) & ~byev
            flee = o["FL"][H == 1].mean() if (H == 1).any() else float("nan")
            say(f"(n) {'(N1) as composed' if kind == 'A14' else '(N2)'}, negative hold (known (1.0, -0.9), channel 1 held s 2.0), {lab}: hold ended in {int((end >= 0).sum())}/{R} rows"
                f" (step {q3(end[end >= 0])}; at step 47: {int((end == 47).sum())}); ended with the evidence release flag {int(byev.sum())}, without it {int(byto.sum())};"
                f" still held at step {st - 1}: {int((H[-1] == 1).sum())}; timeout firings while held {int((o['TO'] & (H == 1)).sum())}; target == flee side on held steps {flee:.3f}")
    # (i9)
    res = {}
    for lab in ("mirror", "stale"):
        class Wd: pass
        wd = Wd(); wd.good = np.zeros(R, int)
        a = build("A14N2", R, np.random.default_rng(BENCH["e1"][1]), wd, None); a.known = np.zeros((R, 2)); a.sel.s[:, 1] = 2.0
        rv = np.zeros((R, 4)); rv[:, 0] = 1.0; a.mb.step(code=a.codes[:, 1], reinf=rv)
        if lab == "mirror": a.known = readout(a)
        _, h = a.act(Still(R), np.zeros((R, 2), bool), np.ones(R, bool)); res[lab] = (int(((a.tgt == a.flee_side) & (h == 1)).sum()), int((h == 1).sum()), readout(a)[:, 1])
    v1 = res["mirror"][2]
    ids["(i9) the flee reads the learned sign (mirror all rows, stale none)"] = res["mirror"][0] == R and res["stale"][0] == 0
    say(f"(i9) constructed (reading R9): v_1 after one punished step {uniq(v1)}; with the mirror target == flee side in {res['mirror'][0]}/{R} rows (channel 1 held {res['mirror'][1]});"
        f" with known left at 0/0 {res['stale'][0]}/{R} (held {res['stale'][1]}) -> {ids['(i9) the flee reads the learned sign (mirror all rows, stale none)']}")
    # (i5)
    ok5, txt = i5_check(); ids["(i5) the harness's Agent14 in World7 T1 == Stage B's supplied arm (2005/2107)"] = ok5; say(txt)
    return ids, exact


def uniq(x):
    u, c = np.unique(np.round(x, 15), return_counts=True); return ", ".join(f"{fx(a)} x{b}" for a, b in zip(u, c))


def i5_check(seeds=(2005, 2107)):
    prev = ph24.make; out = {}
    for kind in ("A14", "A14N2"):
        def mk(cls, runs, rng, G, known, gate=True, filt=True, release=True, _k=kind):
            if cls is Agent14:
                assert G == G_STAR and gate and filt and release
                class Wd: pass
                wd = Wd(); wd.good = np.zeros(runs, int); a = build(_k, runs, rng, wd, None); a.known = known; return a
            return prev(cls, runs, rng, G, known, gate, filt, release)
        ph24.make = mk
        try: out[kind] = ph28.run("T1", Agent14, (1.0, 0.0), seeds)
        finally: ph24.make = prev
    ref = ph28.run("T1", Agent14, (1.0, 0.0), seeds); ks = ph28.ALLK + ("P2", "C2")
    lines = []; ok = True
    for kind, o in out.items():
        V, N, Z = majority(o); c = o["cell"]; cells = tuple((int(V[c == k].sum()), int(N[c == k].sum()), int(Z[c == k].sum())) for k in range(4))
        bw = ph24.bitwise(o, ref, ks); cnt = (int(V.sum()), int(N.sum()), int(Z.sum())) == (STAGEB_SUPPLIED["V"], STAGEB_SUPPLIED["N"], STAGEB_SUPPLIED["tie"]) and cells == STAGEB_SUPPLIED["cells"]
        ok &= bw and cnt
        lines.append(f"{'Agent14 (N1)' if kind == 'A14' else 'Agent14 (N2)'}: == ph28's Agent14 bitwise {bw}; V/N/tie {int(V.sum())}/{int(N.sum())}/{int(Z.sum())}, cells {cells}"
                     f" (Stage B supplied {STAGEB_SUPPLIED['V']}/{STAGEB_SUPPLIED['N']}/{STAGEB_SUPPLIED['tie']}, {STAGEB_SUPPLIED['cells']})")
    return ok, f"(i5) World7 T1, supplied +1/0, learning off, {seeds[0]}/{seeds[1]} (reading R15): " + "; ".join(lines) + f" -> {ok}"


def e1_bench_arms(arms, g3, say):
    for nm in ("learned", "H15 agent", "positive-off", "no-learning", "known-answer", "as composed (N1)"):
        o = arms[nm]; ps = o["pstart"]; vb = o["first_b"] >= 0
        say(f"   [{nm}] R-start rows visiting P {int((vb & ~ps).sum())}/{int((~ps).sum())}; P-start late unrecovered {int(unrec(o)[ps].sum())}/{int(ps.sum())}, R-start {int(unrec(o)[~ps].sum())}/{int((~ps).sum())};"
            f" all {int(unrec(o).sum())}/{R}; G3 reach after the first punished step {int((o['last_g'] > o['first_b'])[g3].sum())}/{int(g3.sum())};"
            f" last-third dwell median R {np.median(late(o['g'])):.1f} P {np.median(late(o['b'])):.1f}; first rewarded step {q3(o['first_g'][o['first_g'] >= 0])};"
            f" contacts/agent {o['contacts'].mean():.2f}")


def bench(say=print):
    say(f"== H20 Stage C mechanism bench (design v2 FINAL section 4). design {DESIGN}; {BENCH}; bootstrap seed {ph15.BOOT_SEED}, 95 percent ==")
    header(say); readings(say)
    out = dict(stop=False, nocand=False, repro=False)
    # ---- (r) first; nothing else is read before it holds
    rep = reproduction(say); out["repro"] = rep
    if not rep:
        say("== (r) NOT reproduced: no comparison is read; the run stops here (design section 4) =="); return False, out
    say("== (r) holds: every line of experiments/h15/ph15_run2.txt reproduced; the bench continues ==")
    # ---- constructed states and (i5)
    ids, exact = constructed(say)
    # ---- E1-C on bench seeds (identities, stop rules) and E2-C on the E2 bench seeds (checks, printed beside)
    s1 = e1_specs(BENCH["e1"], arms=["learned", "H15 agent", "positive-off", "no-learning", "known-answer", "as composed (N1)"])
    s2 = e2_specs(BENCH["e2"]); res = pool_run(s1 + s2)
    arms, disp, locks = collect(s1, res[:len(s1)]); e2a, e2d, e2l = collect(s2, res[len(s1):])
    say(f"(i) identities on the E1 bench seeds {BENCH['e1']}, {R} x {T1} (lockstep, reading R2):")
    ids.update(identities(arms, disp, locks + e2l, T1, e2=(e2a, e2d), say=say))
    L, A3, PO, NL = arms["learned"], arms["H15 agent"], arms["positive-off"], arms["no-learning"]
    ps = L["pstart"]; rs = ~ps; g3 = ps & (L["first_b"] >= 0)
    say(f"(h) E1-C on bench seeds {BENCH['e1']}, {R} x {T1}; G3 (learned arm) {int(g3.sum())}/{int(ps.sum())}:")
    e1_bench_arms(arms, g3, say)
    Vl, Va, Vp = (L["first_b"] >= 0)[rs], (A3["first_b"] >= 0)[rs], (PO["first_b"] >= 0)[rs]
    pa, dpa, ba = pp_pair(Vl, Va, -0.05, True); pb, dpb, bb = pp_pair(Vl, Vp, -0.05, True)
    _, d_a, l_a, h_a = (None, *ph15.boot("DP", Vl.astype(float), Va.astype(float)))
    say(f"   (h) M2(a) R-start punisher visits learned {int(Vl.sum())} vs H15 agent {int(Va.sum())}: DP {dpa:+.4f} [{l_a:+.4f}, {h_a:+.4f}], discordant b {ba:.4f}"
        f" (learned only {int((Vl & ~Va).sum())}, H15 agent only {int((~Vl & Va).sum())}); pass probability {pa:.4f}")
    say(f"   reported: M2(b) learned vs positive-off {int(Vp.sum())}: DP {dpb:+.4f}, b {bb:.4f}, pass probability {pb:.4f}")
    stop_h = pa < 0.5
    say(f"   (h) STOP RULE: M2(a) pass probability {pa:.4f} {'< 0.5 -> STOP: the run returns to the owner after the bench record' if stop_h else '>= 0.5 -> continue'}")
    ul, ua = unrec(L)[ps], unrec(A3)[ps]; p3, dp3, b3 = pp_pair(ul, ua, 0.10, True)
    rl, ra = (L["last_g"] > L["first_b"])[g3], (A3["last_g"] > A3["first_b"])[g3]; p5, dp5, b5 = pp_pair(rl, ra, -0.10, False)
    say(f"   (hS) M3(b) P-start late unrecovered learned {int(ul.sum())} vs H15 agent {int(ua.sum())} of {int(ps.sum())}: DP {dp3:+.4f}, b {b3:.4f}, pass probability {p3:.4f};"
        f" M5(a) G3 reach after the first punished step learned {int(rl.sum())} vs H15 agent {int(ra.sum())} of {int(g3.sum())}: DP {dp5:+.4f}, b {b5:.4f}, pass probability {p5:.4f}")
    pr3, dpr3, _ = pp_pair(unrec(L)[rs], unrec(A3)[rs], 0.10, True)
    say(f"   reported: M3(b) R-start DP {dpr3:+.4f}, pass probability {pr3:.4f}; M3(a) learned late unrecovered {int(unrec(L).sum())}/{R}")
    stop_hs = p3 < 0.5 or p5 < 0.5
    say(f"   (hS) STOP RULE: {'STOP: the run returns to the owner after the bench record' if stop_hs else 'both >= 0.5 -> continue'}")
    nlb = late(NL["b"])[g3]; hr = crit("(hR) Agent14 no-learning, GM last-third punishing dwell in the bench G3 (reading R12)", "GM", 10, False, nlb, say=say)
    stop_hr = hr != "PASS"
    say(f"   (hR) STOP RULE: {'STOP: M4(c) would be unreadable' if stop_hr else 'PASS -> continue'}; G3+ (no-learning dwell > 0) {int((nlb > 0).sum())}/{int(g3.sum())}")
    say("   printed beside (no rule): Stage C measures per arm")
    for nm in ("learned", "H15 agent", "positive-off", "no-learning", "known-answer", "as composed (N1)"): extras(nm, arms[nm], g3, say)
    say(f"(E2 bench seeds {BENCH['e2']}, reading R13, printed beside, no rule): pre-test medians trained rewarded {np.median(e2a['trained, learning on']['pre'][:, 0]):+.3f},"
        f" punished {np.median(e2a['trained, learning on']['pre'][:, 1]):+.3f}; sham {np.median(e2a['sham, frozen']['pre'][:, 0]):+.3f}/{np.median(e2a['sham, frozen']['pre'][:, 1]):+.3f};"
        + "; ".join(f" {nm}: reach R {int((o['first_g'] >= 0).sum())}/{R}, P dwell median {np.median(o['b'].sum(0)):.1f}" for nm, o in e2a.items()))
    idok = all(ids.values()); exok = all(exact.values()); nocand = not (idok and exok); stop = stop_h or stop_hs or stop_hr
    verdict = rep and idok and exok and not stop; out.update(stop=stop, nocand=nocand, pa=pa, p3=p3, p5=p5, hr=hr, stop_h=stop_h, stop_hs=stop_hs, stop_hr=stop_hr)
    say(f"== M9: (r) {rep}; identities {idok}; failed {[k for k, v in ids.items() if not v]}; exactness claims of (v) {exok}; failed {[k for k, v in exact.items() if not v]};"
        f" (h) {'STOP' if stop_h else 'continue'}; (hS) {'STOP' if stop_hs else 'continue'}; (hR) {'STOP' if stop_hr else 'continue'} -> M9 "
        + ("PASS: the tasks may be run" if verdict else ("FAIL, NO CANDIDATE: the design reading is wrong there; the tasks are NOT run" if nocand else
                                                        "STOPPED by a stop rule: the tasks are NOT run; the owner decides")) + " ==")
    return verdict, out


# ------------------------------------------------------------------ the tasks (design sections 5-8)
def main(mode_):
    s1, s2 = SEEDS[mode_]
    print(f"== H20 Stage C, {mode_.upper()}. design {DESIGN}; Agent14 (P 60, N_hi 300), G {G_STAR}, gate, filter, release (N2); E1-C world {s1[0]} agent {s1[1]},"
          f" E2-C world {s2[0]} agent {s2[1]}; {R} rows; E1-C {T1} steps, E2-C training {ph15.TRAIN}/{ph15.GAP}/{ph15.TRAIN} then {T2} test steps; bootstrap {ph15.BOOT_SEED},"
          f" 95 percent; {'operation check only (not a verdict)' if mode_ == 'dev' else 'the one evaluation'} ==")
    header(); readings()
    hits, nums, nf = seeds_unused(); print(f"   seed self-check: every Stage C seed and derived number in no other file ({nf} scanned): {not hits}{'' if not hits else ' ' + str(hits)}")
    print("   amendments: none")
    sp1 = e1_specs(s1); sp2 = e2_specs(s2); res = pool_run(sp1 + sp2)
    arms, disp, locks = collect(sp1, res[:len(sp1)]); e2a, e2d, e2l = collect(sp2, res[len(sp1):])
    L = arms["learned"]; ps = L["pstart"]; g3 = ps & (L["first_b"] >= 0)
    print(f"\n==== E1-C natural search. world seed {s1[0]}, agent seed {s1[1]}, {R} rows, {T1} steps, learning on from step 0 ====")
    for nm in list(AGENT_ARMS) + ["random", "oracle"]: print_arm(nm, arms[nm], g3, groups=nm in AGENT_ARMS)
    print(f"\n==== E2-C controlled experience, learning ON in the test. world seed {s2[0]}, agent seed {s2[1]}, {R} rows, every row a P-start row ====")
    allr = np.ones(R, bool)
    for nm, o in e2a.items():
        rf = o["reward_first"]
        print(); ph15.measures(nm[:13], o, allr, "all")
        print(f"      [{nm}] training calls {o['train_calls']}; test learning calls {o['calls']}; reward-first rows {int(rf.sum())}; pre-test valence rewarded {np.median(o['pre'][:, 0]):+.3f}"
              f" (first {np.median(o['pre'][rf, 0]):+.3f} / second {np.median(o['pre'][~rf, 0]):+.3f}) punished {np.median(o['pre'][:, 1]):+.3f}"
              f" (first {np.median(o['pre'][~rf, 1]):+.3f} / second {np.median(o['pre'][rf, 1]):+.3f}); reach R {int((o['first_g'] >= 0).sum())}/{R}; P dwell over the test median {np.median(o['b'].sum(0)):.1f}")
    judge(mode_, arms, disp, locks, e2a, e2d, e2l, g3)


def judge(mode_, arms, disp, locks, e2a, e2d, e2l, g3):
    ok = lambda z: "PASS" if z else "FAIL"
    L, A3, PO, NL, KA = arms["learned"], arms["H15 agent"], arms["positive-off"], arms["no-learning"], arms["known-answer"]
    ps = L["pstart"]; rs = ~ps
    print("\n== criteria (design v2 FINAL section 7; 95 percent, one evaluation, no extension; a multi-part criterion PASS if every part passes, FAIL if any fails, else INCONCLUSIVE) ==")
    print("\n== M1 validity (all rows, last third) ==")
    m1 = [crit("(a) rewarding dwell, oracle - random", "DGM", 10, False, late(arms["oracle"]["g"]), late(arms["random"]["g"]))]
    for nm in AGENT_ARMS:
        for key in ("g", "b"): m1.append(crit(f"(b) {nm} dwell at {'R' if key == 'g' else 'P'}", "GM", 594, True, late(arms[nm][key])))
    m1.append(crit("(c) total dwell, learned - random", "DGM", 10, False, late(L["g"]) + late(L["b"]), late(arms["random"]["g"]) + late(arms["random"]["b"])))
    M1 = agg(m1); print(f"   M1 -> {M1}")
    print("\n== M2 the gain (E1-C, R-start rows): visited the punishing source at least once over the run ==")
    Vl, Va, Vp = ((o["first_b"] >= 0)[rs].astype(float) for o in (L, A3, PO))
    print(f"   R-start rows visiting P: learned {int(Vl.sum())}/{int(rs.sum())}, H15 agent {int(Va.sum())}, positive-off {int(Vp.sum())}, known-answer {int((KA['first_b'] >= 0)[rs].sum())},"
          f" no-learning {int((NL['first_b'] >= 0)[rs].sum())}, as composed (N1) {int((arms['as composed (N1)']['first_b'] >= 0)[rs].sum())}, H15 no-learning {int((arms['H15 no-learning']['first_b'] >= 0)[rs].sum())}")
    m2 = [crit("(a) DP learned Agent14 - H15 Run 2's agent", "DP", -0.05, True, Vl, Va), crit("(b) DP learned Agent14 - Agent14 positive-off", "DP", -0.05, True, Vl, Vp)]
    M2 = agg(m2); print(f"   M2 -> {M2}")
    print("\n== M3 search kept (late unrecovered: no plume whiff in blocks 7-9) ==")
    m3 = [crit("(a) learned, all rows", "P", 0.100, True, unrec(L))]
    for m, lab in ((ps, "P-start"), (rs, "R-start")):
        m3.append(crit(f"(b) DP learned - H15 agent, {lab}", "DP", 0.10, True, unrec(L)[m].astype(float), unrec(A3)[m].astype(float)))
        crit(f"    reported: DP learned - known-answer, {lab}", "DP", 0.10, True, unrec(L)[m].astype(float), unrec(KA)[m].astype(float))
    M3 = agg(m3); print(f"   M3 -> {M3}")
    print(f"\n== M4 avoidance kept. G3 = P-start rows punished at least once in the learned arm: {int(g3.sum())}/{int(ps.sum())} ==")
    if g3.sum() < 50: m4 = ["UNREADABLE"]; print("   G3 under 50 -> UNREADABLE")
    else:
        base = crit("    readability: Agent14 no-learning punishing dwell in G3", "GM", 10, False, late(NL["b"])[g3])
        m4 = [crit("(a) learned value of the punished odour at the end", "GM", -0.5, True, L["val"][-1][g3, 1])]
        if base == "PASS":
            g3p = g3 & (late(NL["b"]) > 0)
            print(f"    G3+ = G3 rows whose no-learning last-third punishing dwell is above 0: {int(g3p.sum())}")
            m4 += [crit("(b) punishing dwell, learned", "GM", 1.0, True, late(L["b"])[g3]),
                   agg([crit("(c) punishing dwell, learned / no-learning", "RGM", 0.75, True, late(L["b"])[g3], late(NL["b"])[g3]),
                        crit("(c) learned below no-learning, WIN on G3+", "WIN", 0.60, False, late(L["b"])[g3p], late(NL["b"])[g3p])])]
            print(f"   (c) -> {m4[-1]}")
        else: m4 += ["UNREADABLE"]*2; print("   (b), (c): UNREADABLE, the no-learning baseline does not PASS 'at least 10'")
    M4 = agg(m4); print(f"   M4 -> {M4}")
    print("\n== M5 reach and dwell after avoidance (G3, H15 Run 2's agent as the reference) ==")
    if g3.sum() < 50: m5 = ["UNREADABLE"]
    else:
        m5 = [crit("(a) reach the rewarding source after the first punished step, learned - H15 agent", "DP", -0.10, False,
                   (L["last_g"] > L["first_b"])[g3].astype(float), (A3["last_g"] > A3["first_b"])[g3].astype(float))]
        rb = crit("    readability: H15 agent rewarding dwell in G3", "GM", 10, False, late(A3["g"])[g3])
        m5.append(crit("(b) rewarding dwell, learned / H15 agent", "RGM", 0.75, False, late(L["g"])[g3], late(A3["g"])[g3]) if rb == "PASS" else "UNREADABLE")
    M5 = agg(m5); print(f"   M5 -> {M5}")
    g5 = L["first_g"] >= 0
    print(f"\n== M6 the rewarded value, weight level. G5 = rows rewarded at least once in the learned arm: {int(g5.sum())}/{R} ==")
    M6 = crit("learned value of the rewarded odour at the end", "GM", 0.5, False, L["val"][-1][g5, 0]); print(f"   M6 -> {M6}")
    print("\n== M7 controlled experience with learning ON (E2-C, all 400 rows) ==")
    T, S, A = e2a["trained, learning on"], e2a["sham, frozen"], e2a["H15 agent trained, learning on"]
    mc = [crit("    manipulation check: trained, punished odour before the test", "GM", -0.5, True, T["pre"][:, 1]),
          crit("    manipulation check: sham >= -0.1", "GM", -0.1, False, S["pre"][:, 1]), crit("    manipulation check: sham <= +0.1", "GM", 0.1, True, S["pre"][:, 1])]
    tb, sb = T["b"].sum(0), S["b"].sum(0)
    if not all(x == "PASS" for x in mc): m7 = ["UNREADABLE"]; print("   M7: UNREADABLE, the training did not install the memory")
    else:
        base = crit("    readability: sham punishing dwell over the test", "GM", 10, False, sb)
        m7 = [crit("(a) punishing dwell, trained learning on / sham frozen", "RGM", 0.5, True, tb, sb) if base == "PASS" else "UNREADABLE",
              crit("(b) trained below sham", "WIN", 0.60, False, tb, sb),
              crit("(c) reach the rewarding source, trained - sham", "DP", 0.25, False, (T["first_g"] >= 0).astype(float), (S["first_g"] >= 0).astype(float)),
              crit("(d) reach the rewarding source, Agent14 trained learning on - H15 agent trained learning on", "DP", -0.10, False,
                   (T["first_g"] >= 0).astype(float), (A["first_g"] >= 0).astype(float))]
    for nm in ("trained, frozen", "trained, learning on, as composed (N1)"):
        o = e2a[nm]; print(f"      reported: {nm}: reach R {int((o['first_g'] >= 0).sum())}/{R}, P dwell over the test median {np.median(o['b'].sum(0)):.1f};"
                           f" DP reach vs trained learning on {float((o['first_g'] >= 0).mean() - (T['first_g'] >= 0).mean()):+.4f}")
    M7 = agg(m7); print(f"   M7 -> {M7}")
    print("\n== M8 identities (task seeds) ==")
    ids = identities(arms, disp, locks + e2l, T1, e2=(e2a, e2d))
    c9 = constructed_i9()
    ids["(i9) the flee reads the learned sign (constructed)"] = c9
    print(f"   (i9) constructed (bench construction, reading R9): {c9}")
    M8 = ok(all(ids.values())); print(f"   M8 -> {M8}; failed {[k for k, v in ids.items() if not v]}")
    print("\n== M9 the mechanism bench, re-run here on the bench seeds (reading R14) ==")
    lines = []; v9, bo = bench(say=lines.append); M9 = ok(v9)
    try: ref = open(BENCH_TXT, encoding="utf-8").read().split("\n")
    except OSError: ref = []
    same = [ln for ln in lines if ln in ref]
    for ln in lines:
        if ln.startswith("== M9") or "STOP RULE" in ln or ln.startswith("(r) REPRODUCTION") or "exactness claims" in ln: print("      " + ln.strip())
    print(f"   every re-run bench line equal to experiments/h20/ph30_bench.txt: {len(same) == len(lines) and len(lines) > 0} ({len(same)}/{len(lines)} lines found in the file)")
    print(f"   M9 -> {M9}")
    print("\n== M10 lost rows and walls (reported, no bar) ==")
    for nm in AGENT_ARMS:
        o = arms[nm]; reach = (o["last_g"] > o["first_b"])[g3]; wb = o["wall_between"][g3]
        print(f"   {nm}: contacts per agent {o['contacts'].mean():.2f}; near-wall dwell {o['nearwall'].mean()/(3*STEPS)*100:.2f}%; late unrecovered {int(unrec(o).sum())}/{R};"
              f" G3 reach after the first punished step {int(reach.sum())} (with an intervening wall contact {int((reach & wb).sum())})")
    Ms = dict(M1=M1, M2=M2, M3=M3, M4=M4, M5=M5, M6=M6, M7=M7, M8=M8, M9=M9)
    verdict = all(x == "PASS" for x in Ms.values()); fail = any(x == "FAIL" for x in (M2, M3, M4, M5, M6, M7))
    unread = any(x == "UNREADABLE" for x in Ms.values()) or M1 != "PASS" or M8 != "PASS" or M9 != "PASS"
    lab = "PASS" if verdict else "FAIL" if fail else "UNREADABLE" if unread else "INCONCLUSIVE"
    print(f"\n== H20 Stage C ==  " + "  ".join(f"{k} {v}" for k, v in Ms.items()) + " (M10 reported) -> " + lab + ": "
          + ("SHOWN: with learning on during the run in the H15 Run 2 world, the adopted agent (Agent14, with the release applied at non-negative holds only) uses the positive"
             " value it learns at the rewarding source: fewer R-start rows visit the not-yet-learned punisher than with H15 Run 2's agent and than with its own positive values"
             " removed; and it keeps H15 Run 2's long-horizon search, its avoidance of the learned punisher and its reach of the reward after avoidance, within Run 2's allowed"
             " gaps on the same rows; with a trained memory and learning on in the test it dwells less at the punisher and reaches the reward more than a sham, as H15 Run 2's agent does."
             if verdict else "NOT shown under the registered criteria" + (" (UNREADABLE, section 8)" if lab == "UNREADABLE" else "")))


def constructed_i9():
    res = {}
    for lab in ("mirror", "stale"):
        class Wd: pass
        wd = Wd(); wd.good = np.zeros(R, int)
        a = build("A14N2", R, np.random.default_rng(BENCH["e1"][1]), wd, None); a.known = np.zeros((R, 2)); a.sel.s[:, 1] = 2.0
        rv = np.zeros((R, 4)); rv[:, 0] = 1.0; a.mb.step(code=a.codes[:, 1], reinf=rv)
        if lab == "mirror": a.known = readout(a)
        _, h = a.act(Still(R), np.zeros((R, 2), bool), np.ones(R, bool)); res[lab] = int(((a.tgt == a.flee_side) & (h == 1)).sum())
    return res["mirror"] == R and res["stale"] == 0


# ------------------------------------------------------------------ self-checks
def demo():
    print(f"== H20 Stage C self-checks (demo). design {DESIGN} ==")
    header()
    print("   fixed before this recorded demo (code-path runs only, on unregistered demo seeds (3, 4), (5, 6), (7, 8), (9, 10), (11, 12) with 40-120 rows and 600-1200 steps;"
          " their numbers are not used anywhere): check 7 first ran 300 steps, fewer than one 600-step block (IndexError in the check itself; now 600 steps); an f-string quoting"
          " error in check 7's print; the identity loop looked up the E2 lockstep arms in the E1 table (KeyError in a bench-path smoke run); (v)'s reported design-3.8 lines"
          " were evaluated after all 30 punished steps of (3a) (now at min(m, 10), where the formula applies) and repeated identical steps are no longer printed; i5_check"
          " takes its seeds as a parameter (default 2005/2107) so that its code path could be run on demo seeds (5, 6) (counts not used). Reading R6"
          " was written in the header before any of these runs. FIXED AFTER THE FIRST BENCH RUN (sha256 0b34907f..d380c, output kept as ph30_bench_before_fix.txt):"
          " the reported measure 'punisher holds formed at a positive residual' read the arm's own read-out (chan_valence), which the positive-off arm clips at 0, so"
          " identity (i4) failed on that end-of-run record alone although every (step, row) and every other record was equal; it now reads the module's learned value"
          " (reading R19); no behavioural quantity, rule or bar is touched.")
    n, st = 40, 1200; sd = (3, 4)
    # 1. the harness is ph15.simulate field for field (mirror off)
    for arm in ("intact", "no-learning", "known", "random", "oracle", "ungated", "no-hold"):
        ref = ph15.run_e1(arm, sd, runs=n, steps=st, keep_src=True)
        with ph15_sim(): mine = ph15.run_e1(arm, sd, runs=n, steps=st, keep_src=True)
        d = end_equal(ref, mine); assert not d and sorted(ref) == sorted(mine), (arm, d)
    for lo in (False, True):
        ref = ph15.run_e2("trained", sd, runs=n, learn_on=lo)
        with ph15_sim(): mine = ph15.run_e2("trained", sd, runs=n, learn_on=lo)
        assert not end_equal(ref, mine), ("e2", lo)
    print("ok 1  the harness with the mirror off == ph15.simulate field for field (E1 intact, no-learning, known, random, oracle, ungated, no-hold; E2 trained frozen and learning on; 40 rows)")
    # 2. identities on a small run
    outs, eq, keys = lockstep([e1_sim(nm, sd, n, st, trace=True) for nm in ("H15 agent", "H15 agent + mirror", "H15 agent + min mirror", "Agent8 pathway-off")])
    assert all(e.all() for e in eq) and all(not end_equal(outs[0], o, skip=("mirror_bad",)) for o in outs[1:]), [e.all(0).sum() for e in eq]
    outs2, eq2, _ = lockstep([e1_sim(nm, sd, n, st, trace=True) for nm in ("no-learning", "Agent10 0/0", "N1 no-learning")])
    assert all(e.all() for e in eq2)
    print("ok 2  (i1) Agent3 + mirror, (i4) Agent3 + min mirror, (i3) Agent8 pathway-off == Agent3 live; (i6) Agent14 (N2) 0/0 == Agent10 0/0 == Agent14 (N1) 0/0 (40 x 1200, lockstep, every field)")
    # 3. the lockstep comparison can fail
    o3, eq3, _ = lockstep([e1_sim(nm, sd, n, st, trace=True) for nm in ("H15 agent", "learned")])
    assert not eq3[0].all()
    print(f"ok 3  the lockstep comparison detects a difference: Agent3 vs Agent14 learned, rows departing {int((~eq3[0].all(0)).sum())}/{n}")
    # 4. (N2) MRO and inertness without a negative hold; it acts at a negative hold
    assert [c.__name__ for c in Agent14N2.__mro__[:6]] == ["Agent14N2", "ReleaseN2", "Agent14", "Release", "Agent9", "Agent8"]
    a = build("A14N2", 5, np.random.default_rng(1), World6(5, np.random.default_rng(2), 2), "zero"); assert (a.c == 240.0).all() and a.N == 300 and a.G == G_STAR and a.release
    o_n1 = stub("A14", (1.0, -0.9), [(120, 0.0, 0.0)], hold=1, rows=n); o_n2 = stub("A14N2", (1.0, -0.9), [(120, 0.0, 0.0)], hold=1, rows=n)
    assert (o_n1["H"][47] != 1).all() and not np.array_equal(o_n1["H"], o_n2["H"])
    o_p1 = stub("A14", (1.0, 0.0), [(200, 0.3, 0.3)], rows=n); o_p2 = stub("A14N2", (1.0, 0.0), [(200, 0.3, 0.3)], rows=n)
    assert all(np.array_equal(o_p1[k], o_p2[k]) for k in o_p1)
    print("ok 4  Agent14N2's MRO (ReleaseN2, Agent14, Release, Agent9, ...), counter 240, window 300; == Agent14 on a +1/0 stub; differs at a -0.9 hold (N1 ends it at step 47)")
    # 5. E2 training == ph15.run_e2's
    t = ph15.run_e2("trained", sd, runs=n, test=False); s = e2_sim("H15 agent trained, learning on", sd, n)
    assert np.array_equal(t["pre"], s.o["pre"]) and np.array_equal(t["reward_first"], s.o["reward_first"]) and t["train_calls"] == s.o["train_calls"]
    s14 = e2_sim("trained, learning on", sd, n); assert np.array_equal(s14.o["pre"], s.o["pre"]) and np.array_equal(s14.o["w_train"], s.o["w_train"])
    print("ok 5  E2-C training == ph15.run_e2's (pre-test values, order, calls); Agent14 and Agent3 get bitwise the same training")
    # 6. row independence for the learning-on Agent14 arms; one call per step
    for nm in ("learned", "positive-off", "as composed (N1)"):
        o = e1_sim(nm, sd, n, st).run(); od = e1_sim(nm, sd, n, st, displace=0).run(); ok, bad, _ = row_indep(o, od, n); assert ok, (nm, bad); assert o["calls"] == st and o["mirror_bad"] == 0
    print("ok 6  row independence (row 0 displaced) and one learning call per step for learned, positive-off, as composed (N1); the mirror equals a fresh read-out on every step")
    # 7. the mirror check can fail
    s = e1_sim("learned", sd, n, 600); orig = s.a.act
    def stale_act(w, x, on):
        s.a.known = s.a.known*0.0; return orig(w, x, on)
    s.a.act = stale_act; o = s.run(); assert o["mirror_bad"] > 0
    print(f"ok 7  the mirror check detects a read-out changed before act (steps flagged {o['mirror_bad']}/600)")
    # 8. parallel == sequential
    par = pool_run([("e1", "learned", sd, n, 600, None), ("e2", "trained, learning on", sd, n, 600, None)])
    seq = [job(("e1", "learned", sd, n, 600, None)), job(("e2", "trained, learning on", sd, n, 600, None))]
    assert all(not end_equal(p, q) for p, q in zip(par, seq))
    print("ok 8  an arm run in a worker process == the same arm run in this process (every record)")
    # 9. pass-probability arithmetic (design section 7)
    tab = {52: (0.0, 0.0), 42: (0.0250, 0.0250), 36: (0.3460, 0.2257), 30: (0.7739, 0.5973), 24: (0.9562, 0.8694), 20: (0.9888, 0.9518), 10: (0.9998, 0.9982)}
    for k, (p0, p5) in tab.items():
        dp = (k - 52)/200; a0 = pp(dp, abs(dp), 200, -0.05, True); a5 = pp(dp, abs(dp) + 10/200, 200, -0.05, True)
        assert abs(a0 - p0) < 6e-5 and abs(a5 - p5) < 6e-5, (k, a0, a5)
    thr = max(k for k in range(0, 60) if pp((k - 52)/200, abs(k - 52)/200, 200, -0.05, True) > 0.5); thr5 = max(k for k in range(0, 60) if pp((k - 52)/200, abs(k - 52)/200 + 0.05, 200, -0.05, True) > 0.5)
    assert thr == 34 and thr5 == 31, (thr, thr5)
    kmax = max(k for k in range(60) if wilson95(k, 400)[1] <= 0.100); assert kmax == 28 and abs(wilson95(28, 400)[1] - 0.0993) < 5e-5
    m3a = {0.0525: 0.9485, 0.06: 0.8294, 0.07: 0.5501, 0.10: 0.0235}
    assert all(abs(binom_le(28, 400, p) - v) < 6e-5 for p, v in m3a.items()), {p: binom_le(28, 400, p) for p in m3a}
    m3b = {(0.0, 0.04): 1.0000, (0.02, 0.06): 0.9963, (0.04, 0.08): 0.8578, (0.06, 0.10): 0.4451}
    assert all(abs(pp(d, b, 200, 0.10, True) - v) < 6e-5 for (d, b), v in m3b.items())
    m5a = {(0.0, 0.04): 1.0000, (-0.02, 0.06): 0.9961, (-0.05, 0.08): 0.7169, (-0.07, 0.10): 0.2784}
    assert all(abs(pp(d, b, 199, -0.10, False) - v) < 6e-5 for (d, b), v in m5a.items())
    assert abs(pp(-0.05, 0.08, 400, -0.10, False) - 0.9487) < 6e-5
    win = min(k for k in range(141) if wilson95(k, 140)[0] >= 0.60); w7 = min(k for k in range(401) if wilson95(k, 400)[0] >= 0.60)
    assert win == 96 and w7 == 260, (win, w7)
    print("ok 9  pass-probability arithmetic reproduces the design's section 7: the M2(a) table (both churn columns), the 34 / 31 row limits, M3(a) 28/400 (Wilson upper 0.0993) and"
          " 0.9485/0.8294/0.5501/0.0235, M3(b) 1.0000/0.9963/0.8578/0.4451 (n 200), M5(a) 1.0000/0.9961/0.7169/0.2784 (n 199), M7(d) 0.9487, WIN limits 96/140 and 260/400")
    hits, nums, nf = seeds_unused(); assert not hits, f"a seed of this run appears in {hits}"
    print(f"ok 10 seeds {nums} appear in no other file under the repository ({nf} files scanned; excluded by name ph30.py, ph30_*.txt, h20_stage_c_*.md, master_plan.md, notes/*.md, viewer/*)")


if __name__ == "__main__":
    m = ([x for x in sys.argv[1:] if x in ("demo", "bench", "dev", "eval")] or ["demo"])[0]
    if m == "demo": demo(); sys.exit(0)
    if m == "bench":
        v, o = bench(); sys.exit(0 if v else 2 if not o["repro"] else 1 if o["nocand"] else 3)
    main(m)
