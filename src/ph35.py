#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H29: the H26 T3b limit (a loss after tracking); Agent17 = Agent14N2 with the presence window after a whiff shortened to 200.

Usage: python ph35.py demo | bench | dev | eval     (stdout, LF line ends; redirected to experiments/h29/ph35_<mode>.txt)

Design: H29 design v2 FINAL, doc d724287aa203d256d, sha256 552e2ee1...6aa7 (experiments/h29/h29_design_v2.md), opened by
decision:h29-open (owner, 2026-09-26, '(i) 권고안대로 진행', gloss 'branch (i), proceed as recommended': branch (i) of the T3b
diagnosis, every recommended option of design v1 section 12 except point 1, which the diagnosis resolved; plus a REPORTED cast-phase
sensitivity condition, T3b at t0 100 and t0 200, no bar). Signed before this file existed, H14 format, H29 only:
decision:classification-rule-relaxed-presence-prior-h29 (one presence counter per odour, window 200, start 140, the 59-step prior
unchanged).

Composition only; NO adopted file is edited. ph28.py (Agent14, the H26 counter, its harness hooks and measures), ph30.py (ReleaseN2,
Agent14N2, the adopted agent) and every module they import are imported unchanged; ph28.py and ph30.py are checked at run time
against the sha256 on record (64ce7d0c...e7aa, 98822834...59bd), and ph34b.py (the T3b diagnosis, whose ph24.make hook builds
Agent14N2 with (P, N_hi) from ph28's context and whose geo() gives the position classes) against 1de70167...bf25. Agent17 is a
subclass of Agent14N2 with NO body: it is built by this file's hook through Agent14's existing constructor arguments (ph28.py:95-97)
with P 60 and N_hi 200, so its counter starts at 140; identity (I1) (Agent17 built with N_hi 300 == Agent14N2 on every field) checks
that the subclass adds nothing.

Readings where the design is silent, chosen so that the identities stay exact (printed again in every output header):
 (R1) Construction: Agent14N2 through ph34b's hook (the diagnosis's; ph30 reading R15's pattern), Agent17 through this file's hook,
      both with (P, N_hi) from ph28's context (ph28.pn): Agent14N2 at (60, 300), Agent17 at (60, 200); every other class goes to the
      earlier hooks unchanged (checked in the demo).
 (R2) Fields: 'every field' = every per-step array the harness records (ph34b.every; (I1)); 'behavioural fields' = ph28.BEHK (ph24's
      identity fields + SIL, TO, EV, W; ph28 reading R4); (I2), (I3) on ph28.ALLK (PRES included) plus the valued counter exactly 100
      lower on every (row, step). The neutral counter and presence differ by construction and are not compared.
 (R3) The exposure set (x) of (I4), from Agent14N2's own T1 run: a step t on which the valued counter (recorded after the step's
      update) is in [200, 300), the row has sensed the valued odour at or before t (not the prior), the valued odour is not held (H
      after the step's selection), and a neutral whiff arrives. At such a step Agent14N2 has the valued odour present and Agent17 not,
      so the neutral whiff steers only in Agent17. A row 'departs' when it is not equal on ph28.BEHK over all 600 steps. Checked
      exactly: departing rows == rows of (x), each first departure == the first exposure step, rows equal before it.
 (R4) T3b: L = the last valued whiff before t0 (masked from t0; ph28 reading R8); eligible rows have one. M8(a) = ph28.lost300(o,
      W=200) over the eligible rows. M8(b) over all 400 rows (a non-eligible row never senses the valued odour and is identical in the
      two agents by (I5), difference 0; H26 and the diagnosis averaged over 400 rows): paired mean difference, ph16.interval('DP')
      (5000 resamples, seed 20261143); the strict bar 'lower bound > 0': PASS iff lower > 0, FAIL iff upper <= 0, else INCONCLUSIVE.
 (R5) (h): V = dwell majority; b = the discordant fraction of V between Agent17 and Agent14N2; M2(b) pass probability ph28.pp_dp(DP,
      b) (sd = sqrt(b - DP^2), se = sd / 20); k = out of V minus into V. M2(a) exact binomial P(K >= 365 of 400) at Agent17's P(V).
 (R6) (hB): ph23.pass_prob(D17 - D14N2, 0.0): Phi(m / (sd / 20) - 1.96), sd ddof 0, over the 400 rows.
 (R7) M1: H26's arms; the neutral arm is Agent17 at 0/0 (H26 used its main agent at 0/0), with Agent14N2 at 0/0 beside it for (I6);
      pathway-off and known-answer = ph28.t1arm's (Agent8 G 0 gate off filter off; Agent5 fixed to the valued odour).
 (R8) M3 on the task seeds: (I1) Agent17 at N_hi 300 in T1 and T3b; (I2), (I3) W1, T3a; (I4) T1; (I5) T3b (and at the reported t0);
      (I6) 0/0 (the M1 neutral pair), +1/-1 (T4) and +1/+1 (one identity pair); (I7) held-only presence in Agent17's T1 and T3b runs.
 (R9) The reported t0 condition (design v2 section 5): ph24.run's t0 argument through ph28.run, t0 100 and t0 200, Agent17 and
      Agent14N2, development and evaluation seeds only; ph28.lost300(o, t0, W).
 (R10) (t): the first neutral whiff at or after L + W in Agent14N2's own T3b run (W 60, 150, 200, 250, 300); position classes at
      L + 200 and L + 300 by ph34b.geo (the diagnosis's reading R4: relative to the neutral source, along range 0 < d_along < 25, cone
      width W0 + SLOPE d_along, wall within 1.0); 'upwind of both sources' d_along < 0 (both sources share x).
 (R11) dev and eval re-run the bench on the bench seeds for M4 (as ph28 and ph33 did) and report whether its M4 line equals
      ph35_bench.txt's.
 (R12) Reported W1 (H26's M5): reach within 3.0 (Wilson), dwell (ph25.w1sum), paired dwell Agent17 - Agent6, contacts, lost rows,
      first surge == first neutral whiff at or after 59. Reported T3a (H26's M7): M7(a) exact (ph25.m7a_t3a), R over 100-599 with
      floor Agent10 and ceiling Agent5 fixed to the neutral odour, the span and its readability bound 5.0. Reported T3b R (H25's):
      floor Agent10, ceiling Agent5 valued then neutral from t0, over 400-599; R_b against Agent11 (N 60).
 (R13) Seed scan (design section 9): the 18 numbers of design section 9 (7 seeds, 6 derived, 5 extra checks), digit-boundary, every
      file under the repository except .git and __pycache__, excluded by name: ph35.py, ph35_*.txt, h29_*.md, master_plan.md,
      notes/*.md, viewer/*; and the (file, number) pair of decision:seed-scan-exclusion-ph31-eval (experiments/h20/ph31_eval.txt with
      Stage C Run 1's E1 evaluation agent seed, taken from ph30's seed constants, not written here). The demo seeds 5/6 are used
      deliberately for smoke checks only and are not part of the scan.
Nothing changes after the table.
"""
import sys, os, re, math, hashlib
import numpy as np
import ph34b                                     # the T3b diagnosis: imports ph28, ph30 unchanged; its hook builds Agent14N2 (reading R1)
import ph28, ph30, ph15, ph16, ph22, ph23, ph24, ph25, ph25b, ph11, ph12, ph21
from ph28 import P_PRIOR, N_HI, ALLK, BEHK, lost300, at_risk, roweq, pp_dp, counter_exact, first_valued
from ph30 import Agent14N2
from ph24 import Agent10, Agent10g, Agent6, bitwise, t3_dwell, ratio_boot, q3f
from ph25 import Agent11, w1sum, lost_t1, binom_ge, cls3, construct_ok, m7a_t3a, t3a_steps, qq
from ph23 import T0, wv, wn, presence_identity, pass_prob, first_surge_ok
from ph21 import q3, first_true
from ph18 import majority, agg
from ph16 import interval, crit, R, T
from ph12 import SAT

sys.stdout.reconfigure(newline="\n")            # LF output, so the recorded sha256 equals the committed blob
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
DESIGN = "H29 v2 FINAL doc d724287aa203d256d hash 552e2ee17df346a4e8eb9fd06525eabd51db2a8d88040d6e44d632700fa56aa7"
DESIGN_FILE = os.path.join(REPO, "experiments", "h29", "h29_design_v2.md")
SHA_ON_RECORD = dict(ph28="64ce7d0ce123f912aa675e86627d5b6b0ae3d89976b093666316e6b78441e7aa",
                     ph30="98822834043de5f31615e73cd4a83444adcef2f1d5e56478356d70ca905059bd",
                     ph34b="1de70167c1bddd07a559c73033f3686b5ff71db3d2c8dd662dac808407f3bf25")
PREFIX = dict(ph11="e80f40bd", ph12="e1035e09", ph22="03ab8c47", ph23="ae180492", ph24="f344f178", ph25b="ad12a912")   # design v2 header
SEEDS = dict(dev=(9903, 9913), eval=(2111, 2221))
BENCH = dict(rows=400, steps=600, steps_b=400, p=0.30, seed_w=20261141, seed_a=20261142, boot=20261143)
BS = (BENCH["seed_w"], BENCH["seed_a"])
ph30.set_stats(ph30.Z95, ph30.QLO95, ph30.QHI95, BENCH["boot"])   # design section 7: 95 percent, bootstrap 20261143 (after the imports set theirs)
N17 = 200                                        # Agent17's window after a whiff (design 3.2); the counter starts at N17 - P_PRIOR = 140
PR = P_PRIOR - 1                                 # 59: the first step on which a never-sensed odour is absent (both agents)
T0_REP = (100, 200)                              # the reported phase-sensitivity condition (design v2 section 5)
WINS = (60, 150, 200, 250, 300)                  # the (t) profile
V10 = (1.0, 0.0)
MODS = (ph11, ph12, ph15, ph16, ph21, ph22, ph23, ph24, ph25, ph25b, ph28, ph30, ph34b)
BENCH_TXT = os.path.join(REPO, "experiments", "h29", "ph35_bench.txt")


def sha(p=__file__): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def fr(k, n): return f"{k}/{n} = {k / n:.3f}" if n else f"{k}/0"
def Phi(x): return 0.5*(1.0 + math.erf(x/math.sqrt(2.0)))


# ------------------------------------------------------------------ the agent (design 3.2) and the hook (reading R1)
class Agent17(Agent14N2):
    """H29: Agent14N2 constructed with N_hi 200 (counter start N_hi - P = 140). No method and no state added (identity (I1))."""


_make_prev = ph24.make                           # ph34b.make (Agent14N2) -> ph28.make (Agent14) -> ph25b -> ph25 -> ph24


def make(cls, runs, rng, G, known, gate=True, filt=True, release=True):
    if cls is Agent17:
        P, N = ph28._PN[0]
        return Agent17(runs, rng, P=P, N_hi=N, G=G, known=known, rule=gate, filt=filt, scope=ph25._SCOPE[0], release=release)
    return _make_prev(cls, runs, rng, G, known, gate, filt, release)


ph24.make = make


def run(world, cls, vals, seeds, N_hi=None, **kw):
    """Agent17 at N_hi 200 and Agent14N2 at 300 by default; any other class through ph28.run unchanged"""
    return ph28.run(world, cls, vals, seeds, P=P_PRIOR, N_hi=N_hi if N_hi is not None else (N17 if cls is Agent17 else N_HI), **kw)


def stub(cls, known, sched, seeds=BS, N_hi=None, **kw):
    return ph28.stub(cls, known, sched, P=P_PRIOR, N_hi=N_hi if N_hi is not None else (N17 if cls is Agent17 else N_HI), seeds=seeds, **kw)


every = ph34b.every


# ------------------------------------------------------------------ measures
def valued_c(o): r = np.arange(len(o["good"])); return o["C2"][:, r, o["good"]]


def c2_off(o17, o14, d=N_HI - N17): return bool(np.array_equal(valued_c(o17), valued_c(o14) - d))


def exposure(o):
    """reading R3, on Agent14N2's T1 run: per (step, row) exposure, first exposure step per row"""
    g = o["good"]; st = o["H"].shape[0]; tt = np.arange(st)[:, None]; fv = first_valued(o); cv = valued_c(o)
    sensed = (fv >= 0)[None, :] & (tt >= fv[None, :])
    ex = sensed & (cv >= N17) & (cv < N_HI) & (o["H"] != g[None, :]) & wn(o)
    return ex, first_true(ex)


def first_dep(o1, o2, ks=BEHK):
    st, n = o1["H"].shape; eq = np.ones((st, n), bool)
    for k in ks:
        if k in o1:
            e = o1[k] == o2[k]; eq &= e.reshape(st, n, -1).all(2)
    return first_true(~eq)


def i4_check(o17, o14):
    ex, fx = exposure(o14); inx = fx >= 0; fd = first_dep(o17, o14); dep = fd >= 0
    ok = bool(np.array_equal(dep, inx) and np.array_equal(fd[dep], fx[dep]))
    return ok, dict(x=int(inx.sum()), dep=int(dep.sum()), dep_in_x=int((dep & inx).sum()), at_fx=int((dep & inx & (fd == fx)).sum()), fx=fx, fd=fd, inx=inx, dep_=dep)


def i5_check(o17, o14, t1_17, t1_14, t0=T0):
    """(I5): each arm == its T1 run before t0 (ALLK); Agent17 == Agent14N2 on BEHK before the first neutral whiff at or after L + 200 in
    eligible rows, throughout in rows with no valued whiff before t0"""
    pre = bitwise(o17, t1_17, ALLK, n=t0) and bitwise(o14, t1_14, ALLK, n=t0)
    d = lost300(o14, t0=t0, W=N17); e = d["elig"]; L = d["L"]; st = o14["H"].shape[0]; tt = np.arange(st)[:, None]
    fn = first_true(wn(o14) & (tt >= (L + N17)[None, :]) & e[None, :]); lim = np.where(e & (fn >= 0), fn, st)
    fd = first_dep(o17, o14); ok_rows = (fd < 0) | (fd >= lim)
    draws = all(o["draws_equal"] and o["rng_equal"] for o in (o17, o14))
    return bool(pre and ok_rows.all() and draws), dict(pre=pre, rows=int(ok_rows.sum()), dep_at_lim=int(((fd >= 0) & (fd == lim)).sum()), draws=draws)


def held_only(o, N=N17):
    """(I7): (row, step) on which an odour is held with its counter >= N (present only by the held clause)"""
    H = o["H"]; st, n = H.shape; held = np.zeros((st, n, 2), bool)
    for k in (0, 1): held[:, :, k] = H == k
    return int((held & (o["C2"] >= N)).sum())


def t3line(o, t0=T0, W=None):
    """T3b per arm: dwell 400-599, eligible, L, first neutral surge after L, window check at W"""
    D = t3_dwell(o, 400, T); d = lost300(o, t0=t0, W=W or N_HI); e = d["elig"]
    return D, d, e


def verdict_gt0(lo, hi): return "PASS" if lo > 0 else "FAIL" if hi <= 0 else "INCONCLUSIVE"


# ------------------------------------------------------------------ header and readings
def header(say=print):
    say(f"   ph35.py sha256 {sha()}; design {DESIGN}")
    say("   imported: " + "; ".join(f"{os.path.basename(m.__file__)} {sha(m.__file__)}" for m in MODS))
    shaok = {k: sha(os.path.join(HERE, k + ".py")) == v for k, v in SHA_ON_RECORD.items()}
    pre = {k: sha(os.path.join(HERE, k + ".py"))[:8] == v for k, v in PREFIX.items()}
    dz = sha(DESIGN_FILE) == DESIGN.split("hash ")[1]
    say(f"   ph28.py, ph30.py, ph34b.py sha256 equal to the record: {shaok}; prefixes of ph11, ph12, ph22, ph23, ph24, ph25b equal to design v2's: {all(pre.values())};"
        f" experiments/h29/h29_design_v2.md sha256 equal to the design's hash: {dz}")
    say(f"   seeds: dev {SEEDS['dev']}, eval {SEEDS['eval']}, bench {BS}, bootstrap {ph15.BOOT_SEED}; demo seeds (5, 6) used deliberately for smoke checks only, NOT in the seed scan;"
        f" statistics 95 percent (Z {ph15.Z}), 5000 resamples; P {P_PRIOR}; Agent17 N_hi {N17} (counter start {N17 - P_PRIOR}); Agent14N2 N_hi {N_HI} (start {N_HI - P_PRIOR}); t0 {T0};"
        f" reported t0 {T0_REP}; {R} rows x {T} steps")
    say("   decisions: decision:h29-open; decision:classification-rule-relaxed-presence-prior-h29 (signed before this file); seed-scan exclusion pair by reference:"
        " experiments/h20/ph31_eval.txt with decision:seed-scan-exclusion-ph31-eval")
    return all(shaok.values()) and all(pre.values()) and dz


def readings(say=print):
    say("   readings (file header R1-R13): R1 Agent14N2 via ph34b's hook, Agent17 (a body-less subclass) via this file's, (P, N_hi) from ph28.pn: (60, 300) and (60, 200);"
        " R2 'every field' = every recorded per-step array, 'behavioural' = ph28.BEHK, (I2)/(I3) on ph28.ALLK + the valued counter exactly 100 lower; R3 exposure (x) from"
        " Agent14N2's T1 run: valued counter in [200, 300) after a valued whiff, valued not held, a neutral whiff; departing rows == (x) rows, first departure == first"
        " exposure; R4 L = last valued whiff before t0, M8(a) = ph28.lost300(W 200) on eligible rows, M8(b) paired over 400 rows, PASS iff lower > 0, FAIL iff upper <= 0;"
        " R5 (h) b = discordant fraction of V, ph28.pp_dp, k = out of V - into V; R6 (hB) ph23.pass_prob(D17 - D14N2, 0); R7 M1 neutral arm = Agent17 at 0/0; R8 M3 on the"
        " task seeds incl. (I1) in T1 and T3b and (I6) at 0/0, +1/-1, +1/+1; R9 reported t0 100, 200 via ph24.run's t0 (dev and eval only); R10 (t) re-scored from"
        " Agent14N2's run, positions by ph34b.geo; R11 dev/eval re-run the bench for M4; R12 W1, T3a, T3b reported quantities as H26's; R13 seed scan, 18 numbers,"
        " exclusions by name, the ph31_eval pair by reference")


# ------------------------------------------------------------------ seed scan (design section 9; reading R13)
def seed_numbers():
    (dw, da), (ew, ea) = SEEDS["dev"], SEEDS["eval"]
    base = [dw, da, ew, ea, BENCH["seed_w"], BENCH["seed_a"], BENCH["boot"]]
    derived = [dw + 10_000, ew + 10_000, BENCH["seed_w"] + 10_000, da + 20_000, ea + 20_000, BENCH["seed_a"] + 20_000]
    extra = [dw + 20_000, ew + 20_000, BENCH["seed_w"] + 20_000, BENCH["seed_w"] + 10_000_000, BENCH["seed_a"] + 20_000_000]
    return base + derived + extra


def seeds_unused():
    nums = seed_numbers(); pair_num = ph30.SEEDS["eval"][0][1]; pair_file = os.path.join("experiments", "h20", "ph31_eval.txt")
    hits, nf = [], 0
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        rel = os.path.relpath(root, REPO).replace("\\", "/"); top = rel.split("/")[0]
        for f in files:
            if f == "ph35.py" or (f.startswith("ph35_") and f.endswith(".txt")) or (f.startswith("h29_") and f.endswith(".md")) or f == "master_plan.md": continue
            if (os.path.basename(root) == "notes" and f.endswith(".md")) or top == "viewer": continue
            nf += 1; p = os.path.join(root, f); relp = os.path.relpath(p, REPO)
            ns = [x for x in nums if not (relp == pair_file and x == pair_num)]
            pat = re.compile(rb"(?<!\d)(" + "|".join(map(str, ns)).encode() + rb")(?!\d)")
            if pat.search(open(p, "rb").read()): hits.append(relp)
    return hits, nums, nf


# ------------------------------------------------------------------ the mechanism bench (design section 4)
def bench(say=print, seeds=BS):
    n = BENCH["rows"]; p = BENCH["p"]; ids, bars, out = {}, {}, {}; kn = [1.0, 0.0]
    say(f"== H29 mechanism bench (design v2 FINAL section 4). design {DESIGN}; {BENCH} ==")
    hok = header(say); readings(say)
    say("   rows share no state: one generator per world and one per agent population, fixed-size draws consumed in row order every step")
    # ---- runs
    o17, o14, o10g = run("T1", Agent17, V10, seeds), run("T1", Agent14N2, V10, seeds), run("T1", Agent10g, V10, seeds)
    w17, w14 = run("W1", Agent17, V10, seeds), run("W1", Agent14N2, V10, seeds)
    a17, a14 = run("T3a", Agent17, V10, seeds), run("T3a", Agent14N2, V10, seeds)
    b17, b14 = run("T3b", Agent17, V10, seeds), run("T3b", Agent14N2, V10, seeds)
    b60, b10 = ph28.run11("T3b", 60, V10, seeds), run("T3b", Agent10, V10, seeds)
    # ---- (m), (x), (t) printed first
    risk, fv14 = at_risk(o14); risk0, _ = at_risk(o14, lo=0); c17, c14 = cls3(o17), cls3(o14)
    say(f"(m) H26's at-risk rows (ph28 reading R3) in Agent14N2's T1 run, {n} x {BENCH['steps']}: {int(risk.sum())} rows (literal reading, any step before the first valued whiff:"
        f" {int(risk0.sum())}); first valued whiff step {qq(fv14)} (never {int((fv14 < 0).sum())}); outcome V/N/tie in them: Agent17 {int((c17[risk] == 0).sum())}/{int((c17[risk] == 1).sum())}/"
        f"{int((c17[risk] == 2).sum())}, Agent14N2 {int((c14[risk] == 0).sum())}/{int((c14[risk] == 1).sum())}/{int((c14[risk] == 2).sum())}")
    ok4, x = i4_check(o17, o14); inx, fx = x["inx"], x["fx"]; r_ = np.arange(n)
    age = valued_c(o14)[np.maximum(fx, 0), r_][inx]; ph = (o14["SINCE"][np.maximum(fx, 0), r_][inx]) % (2*SAT)
    say(f"(x) the exposure set of (I4) (reading R3), Agent14N2's T1 run: {x['x']} rows; first exposure step {q3(fx[inx])}; silence age there (steps since the last valued whiff)"
        f" {q3(age)}; cast phase there (since mod 2 SAT) {q3(ph)}; rows departing from Agent14N2 on the behavioural fields {x['dep']}, of them in (x) {x['dep_in_x']},"
        f" departing exactly at their first exposure step {x['at_fx']}; departing rows == (x) rows and first departure == first exposure: {ok4}")
    for lab, m_ in (("(x) rows", inx),):
        say(f"      [{lab}, {int(m_.sum())}] outcome V/N/tie: Agent17 {int((c17[m_] == 0).sum())}/{int((c17[m_] == 1).sum())}/{int((c17[m_] == 2).sum())};"
            f" Agent14N2 {int((c14[m_] == 0).sum())}/{int((c14[m_] == 1).sum())}/{int((c14[m_] == 2).sum())}")
    d14 = lost300(b14); e = d14["elig"]; L = d14["L"]; er = np.flatnonzero(e); ne = len(er); tt = np.arange(T)[:, None]
    say(f"(t) T3b profile (reading R10), Agent14N2's own run, eligible rows (a valued whiff before t0 {T0}) {ne}/{n}; L {q3(L[e])} (min {L[e].min()}, max {L[e].max()}):")
    for W in WINS:
        rs = first_true(wn(b14) & (tt >= (L + W)[None, :]) & e[None, :]); has = rs[er] >= 0
        say(f"      window {W}: first neutral whiff at or after L + {W}: delay after L {q3(rs[er][has] - L[er][has])} (rows {int(has.sum())}); none before 600 {int((~has).sum())}/{ne}")
    for k in (200, N_HI):
        ts = np.minimum(L[er] + k, T - 1); gg = ph34b.geo(b14, ts, er)
        cnt = {c: sum(z["cls"] == c for z in gg) for c, _ in ph34b.CLS}
        say(f"      position at L + {k}: " + "; ".join(f"{lab} {fr(cnt[c], ne)}" for c, lab in ph34b.CLS) + f"; at a wall {sum(z['wall'] for z in gg)}; upwind of both sources"
            f" {fr(sum(z['da'] < 0 for z in gg), ne)}; d_along {q3f(np.array([z['da'] for z in gg]))}")
    # ---- (a) identities
    i1 = {"T1": every(run("T1", Agent17, V10, seeds, N_hi=N_HI), o14), "W1": every(run("W1", Agent17, V10, seeds, N_hi=N_HI), w14),
          "T3a": every(run("T3a", Agent17, V10, seeds, N_hi=N_HI), a14), "T3b": every(run("T3b", Agent17, V10, seeds, N_hi=N_HI), b14)}
    pm17, pm14 = run("T1", Agent17, (1.0, -1.0), seeds), run("T1", Agent14N2, (1.0, -1.0), seeds)
    i1["+1/-1"] = every(run("T1", Agent17, (1.0, -1.0), seeds, N_hi=N_HI), pm14)
    ids["I1 Agent17 at N_hi 300 == Agent14N2, every field"] = all(i1.values())
    say(f"(a) (I1) Agent17 built with N_hi 300 == Agent14N2 on every recorded field: " + "; ".join(f"{k} {v}" for k, v in i1.items()))
    ids["I2 W1"] = bitwise(w17, w14, ALLK) and c2_off(w17, w14); ids["I3 T3a"] = bitwise(a17, a14, ALLK) and c2_off(a17, a14)
    say(f"(a) (I2) W1 Agent17 == Agent14N2 on ph28.ALLK (PRES included) {bitwise(w17, w14, ALLK)}, valued counter exactly {N_HI - N17} lower on every (row, step) {c2_off(w17, w14)};"
        f" (I3) T3a {bitwise(a17, a14, ALLK)}, {c2_off(a17, a14)}")
    ids["I4 T1 exposure"] = ok4
    say(f"(a) (I4) T1: rows outside (x) equal on the behavioural fields throughout {int((~inx & ~x['dep_']).sum())}/{int((~inx).sum())}; rows in (x) equal before their first exposure step"
        f" and departing exactly there {x['at_fx']}/{x['x']} -> {ok4}")
    ok5, i5 = i5_check(b17, b14, o17, o14); ids["I5 T3b"] = ok5
    say(f"(a) (I5) T3b: each arm == its T1 run on steps 0-{T0 - 1} (ALLK) {i5['pre']}; masked draws == the World7 twin, generator state equal {i5['draws']}; Agent17 == Agent14N2 on the"
        f" behavioural fields before the first neutral whiff at or after L + {N17} (throughout in rows with no valued whiff before t0) {i5['rows']}/{n}; departing exactly there {i5['dep_at_lim']} -> {ok5}")
    i6 = {"+1/-1": bool(roweq(pm17, pm14, BEHK).all())}
    for name, kv in (("0/0", (0.0, 0.0)), ("+1/+1", (1.0, 1.0))):
        i6[name] = bool(roweq(run("T1", Agent17, kv, seeds), run("T1", Agent14N2, kv, seeds), BEHK).all())
    ids["I6 0/0, +1/+1, +1/-1"] = all(i6.values())
    say(f"(a) (I6) Agent17 == Agent14N2 on the behavioural fields, World7 T1 {n} x {BENCH['steps']}: " + "; ".join(f"{k} {v}" for k, v in i6.items()))
    ho = held_only(o17) + held_only(b17); out["ho_runs"] = ho
    # ---- (b) counter exact on constructed schedules
    sb = BENCH["steps_b"]; tb = np.arange(sb)[:, None]
    sch = {"no whiff": [(sb, 0.0, 0.0)], "one whiff on channel 0 at step 0": [(1, 1.0, 0.0), (sb - 1, 0.0, 0.0)], "20-step p 0.30 burst on channel 0": [(20, p, 0.0), (sb - 20, 0.0, 0.0)]}
    okb = np.ones(n, bool); hot = 0; c0 = N17 - P_PRIOR
    for k, s in sch.items():
        o = stub(Agent17, kn, s, seeds=seeds); P2, C, H = o["P2"], o["C2"], o["H"]; ok, hh = counter_exact(o, c0=c0, N=N17); hot += int(hh.sum())
        if k == "no whiff": pat = (C == c0 + tb[:, :, None] + 1).all((0, 2)) & (P2 == (tb <= PR - 1)[:, :, None]).all((0, 2)); ptxt = f"c == {c0} + t + 1 and present exactly on steps 0-{PR - 1}, both channels"
        elif k.startswith("one"): pat = (C[:, :, 0] == tb).all(0) & (P2[:, :, 0] == (tb <= N17 - 1)).all(0); ptxt = f"c_0 == t and channel 0 present exactly on steps 0-{N17 - 1}, absent from {N17}"
        else:
            x0 = o["W"][:, :, 0]; had = x0.any(0); Lr = np.where(had, sb - 1 - np.argmax(x0[::-1], 0), -1)
            pat = (P2[:, :, 0] == np.where(had[None, :], tb < Lr[None, :] + N17, tb <= PR - 1)).all(0)
            ptxt = f"channel 0 absent from exactly {N17} steps after the last whiff (rows with a whiff {int(had.sum())}, last whiff step {q3(Lr[had])})"
        ex_ = ok & pat & (hh == 0); okb &= ex_
        fh = first_true(H == 0); end = first_true((H != 0) & (tb > fh[None, :]) & (fh >= 0)[None, :])
        say(f"(b) {k}: rows exact {int(ex_.sum())}/{n} (recursion from {c0} and present == (c < {N17}) or held {int(ok.sum())}; {ptxt} {int(pat.sum())}; no held-only presence"
            f" {int((hh == 0).sum())}); valued hold formed in {int((fh >= 0).sum())} rows, at step {qq(fh)}, ended at step {qq(end)}")
    k_, pt, lo, hi = interval("P", okb); bars["b counter"] = lo
    ids["I7 held-only presence 0"] = hot == 0 and ho == 0
    say(f"(b) counter exact in every schedule ({n} rows x {sb} steps): {k_}/{n} = {pt:.3f} [{lo:.3f}, {hi:.3f}] (bar lower bound >= 0.95) -> {'PASS' if lo >= 0.95 else 'FAIL'};"
        f" (I7) held-only presence (an odour held with its counter >= {N17}): stubs {hot}, Agent17 T1 and T3b runs {ho} (row, step), expected 0 -> {ids['I7 held-only presence 0']}")
    # ---- (f) the window exact at L + 200; T3a M7(a)
    d17 = lost300(b17, W=N17); e17 = d17["elig"]; k_, pt, lo_f, hi = interval("P", d17["exact"][e17]); bars["f window T3b (L + 200)"] = lo_f
    say(f"(f) T3b post-whiff window exact at L + {N17}, Agent17, eligible rows (reading R4): {k_}/{int(e17.sum())} = {pt:.3f} [{lo_f:.3f}, {hi:.3f}] (bar lower bound >= 0.95) ->"
        f" {'PASS' if lo_f >= 0.95 else 'FAIL'}; parts (no nav on a neutral-only whiff on L+1..L+{N17 - 1}, first neutral surge after L = first neutral whiff at or after L+{N17},"
        f" valued not held from L+60): {int(d17['a1'][e17].sum())}/{int(d17['a2'][e17].sum())}/{int(d17['a3'][e17].sum())}; L {q3(d17['L'][e17])}; first-neutral-surge delay after L"
        f" {q3(d17['delay'][e17 & (d17['delay'] >= 0)])} (none {int((e17 & (d17['delay'] < 0)).sum())})")
    say(f"      Agent14N2 beside it: window exact at L + {N_HI} {int(d14['exact'][e].sum())}/{ne}; first-neutral-surge delay after L {q3(d14['delay'][e & (d14['delay'] >= 0)])}"
        f" (none {int((e & (d14['delay'] < 0)).sum())})")
    ex7, parts = m7a_t3a(a17); k_, pt, lo7, hi = interval("P", ex7); bars["f T3a M7(a)"] = lo7
    say(f"(f) T3a M7(a) exact, Agent17 (valued hold ends at 47 with both units <= 1.0, not held from 47, no nav on 0-{PR - 1}, first neutral surge = first neutral whiff at or after"
        f" {PR}): {k_}/{n} = {pt:.3f} [{lo7:.3f}, {hi:.3f}] (bar lower bound >= 0.95) -> {'PASS' if lo7 >= 0.95 else 'FAIL'}; construction {construct_ok(a17)}")
    # ---- (h) T1 stop rule
    V17, V14, V10g = (c17 == 0), (c14 == 0), (cls3(o10g) == 0)
    _, dp, dlo, dhi = interval("DP", V17.astype(float), V14.astype(float)); b = float((V17 != V14).mean()); pph = pp_dp(dp, b)
    into, outv = int((V17 & ~V14).sum()), int((~V17 & V14).sum()); kk = outv - into
    ppc = pp_dp(float(V17.mean() - V10g.mean()), float((V17 != V10g).mean()), bar=0.05); stop_h = pph < 0.5
    for k, o in (("Agent17", o17), ("Agent14N2", o14), ("Agent10g", o10g)):
        Vv, Nn, Zz = majority(o); _, pv, lv, hv = interval("P", Vv)
        say(f"(h) T1 on bench seeds, World7 +1/0 {n} x {BENCH['steps']}: {k} V {int(Vv.sum())} N {int(Nn.sum())} tie {int(Zz.sum())} P(V) {pv:.3f} [{lv:.3f}, {hv:.3f}];"
            f" lost rows {int(lost_t1(o).sum())}; wall contacts per row {o['contacts'].mean():.3f}")
    say(f"   (h) paired DP P(V) Agent17 - Agent14N2 {dp:+.4f} [{dlo:+.4f}, {dhi:+.4f}] (bootstrap 5000, seed {ph15.BOOT_SEED}); into V {into}, out of V {outv}, k = {kk}; discordant fraction b {b:.4f}")
    say(f"   (h) pass probabilities at the bench values (design section 7, reading R5): M2(b) at DP {dp:+.4f}, b {b:.4f}, sd sqrt(b - DP^2) {math.sqrt(max(b - dp*dp, 0.0)):.4f}: {pph:.4f};"
        f" M2(a) P(K >= 365 of 400) at P(V) {V17.mean():.3f}: {binom_ge(V17.mean()):.4f}; M2(c) vs Agent10g at DP {(V17.mean() - V10g.mean()):+.4f}: {ppc:.4f}")
    say(f"   (h) STOP RULE (design v2 FINAL section 4, section 12 point 7): M2(b) pass probability {pph:.4f} {'< 0.5 -> STOP: the run returns to the owner after the bench record' if stop_h else '>= 0.5 -> continue'}")
    # ---- (hB) T3b stop rule
    D17, D14, D60, D10 = (t3_dwell(o, 400, T) for o in (b17, b14, b60, b10)); g_ = D17 - D14
    ppB, mB, sdB = pass_prob(g_, 0.0); _, gm, glo, ghi = interval("DP", D17, D14); stop_hB = ppB < 0.5
    say(f"(hB) T3b (Lost world, t0 {T0}) neutral dwell 400-599 on bench seeds: Agent17 {D17.mean():.3f} (quartiles {q3f(D17)}), Agent14N2 {D14.mean():.3f} ({q3f(D14)}); beside it"
        f" Agent11 (N 60) {D60.mean():.3f} ({q3f(D60)}), Agent10 {D10.mean():.3f} ({q3f(D10)})")
    say(f"   (hB) paired Agent17 - Agent14N2 mean {mB:+.4f}, sd {sdB:.4f} (bootstrap [{glo:+.4f}, {ghi:+.4f}]); rows gaining {int((g_ > 0).sum())}, losing {int((g_ < 0).sum())}, equal {int((g_ == 0).sum())};"
        f" M8(b) pass probability (reading R6) Phi({mB:+.4f} / ({sdB:.4f} / 20) - 1.96) = {ppB:.4f}")
    say(f"   (hB) STOP RULE (design v2 FINAL section 4, section 12 point 7): M8(b) pass probability {ppB:.4f} {'< 0.5 -> STOP: the run returns to the owner after the bench record' if stop_hB else '>= 0.5 -> continue'}")
    if D60.mean() != D14.mean():
        Rb, Rblo, Rbhi = ratio_boot(D17, D14, D60); say(f"      reported: R_b = (D_17 - D_14N2) / (D_60 - D_14N2) = {Rb:.4f} [{Rblo:.4f}, {Rbhi:.4f}]")
    out.update(dp=dp, dlo=dlo, dhi=dhi, b=b, pph=pph, k=kk, into=into, outv=outv, mB=mB, sdB=sdB, ppB=ppB, glo=glo, ghi=ghi, stop_h=stop_h, stop_hB=stop_hB, x=x["x"], risk=int(risk.sum()))
    idok = all(ids.values()); bok = all(v >= 0.95 for v in bars.values()); verdict = idok and bok and hok; stop = stop_h or stop_hB; out["stop"] = stop
    say(f"== M4: identities {idok}; failed {[k for k, v in ids.items() if not v]}; implementation bars (lower bounds >= 0.95) {bok} " + str({k: round(float(v), 4) for k, v in bars.items()})
        + f"; imported files as on record {hok} -> M4 {'PASS: the tasks may be run' if verdict else 'FAIL, NO CANDIDATE: an implementation error; the tasks are NOT run'};"
        f" (m), (x), (t) printed first; (h) stop rule {'STOP' if stop_h else 'continue'}; (hB) stop rule {'STOP' if stop_hB else 'continue'} ==")
    return verdict, out


# ------------------------------------------------------------------ self-checks
def demo():
    print(f"== H29 self-checks (demo). design {DESIGN} ==")
    header(); readings()
    print("   smoke checks only, on the demo seeds (5, 6), few rows and steps; no number here is used for anything")
    print("   fixed before this recorded demo: none")
    n, st = 40, 200; kw = dict(runs=n, steps=st); sd = (5, 6); sp = [(st, 0.30, 0.30)]; kn = [1.0, 0.0]
    hits, nums, nf = seeds_unused(); assert not hits, f"a seed of this run appears in {hits}"
    print(f"ok  seed scan: the 18 numbers {nums} appear in no other file ({nf} files scanned; excluded by name ph35.py, ph35_*.txt, h29_*.md, master_plan.md, notes/*.md,"
          f" viewer/*; the ph31_eval pair by reference)")
    assert all(sha(os.path.join(HERE, k + ".py")) == v for k, v in SHA_ON_RECORD.items()), "an imported file differs from the version on record"
    print("ok  ph28.py, ph30.py and ph34b.py are the versions on record (sha256)")
    for cls in (Agent10, Agent10g, Agent6, Agent11, Agent14N2):
        ph24.make = _make_prev; a = ph28.run("T1", cls, V10, sd, **kw); sa = ph28.stub(cls, kn, sp, rows=n, seeds=sd)
        ph24.make = make; b = ph28.run("T1", cls, V10, sd, **kw); sb = ph28.stub(cls, kn, sp, rows=n, seeds=sd)
        assert every(a, b) and every(sa, sb), f"this file's hook changed a run of {cls.__name__}"
    print("ok  this file's hook leaves every recorded field of ph28.run and ph28.stub unchanged for Agent10, Agent10g, Agent6, Agent11 and Agent14N2 (World7 40 x 200 and stub)")
    got = {}
    def spy(cls, *a, **k):
        x = make(cls, *a, **k); got[cls.__name__] = (type(x).__name__, x.P, x.N_hi, float(x.c[0, 0]), x.N); return x
    ph24.make = spy
    try: run("T1", Agent17, V10, sd, runs=4, steps=2); run("T1", Agent14N2, V10, sd, runs=4, steps=2)
    finally: ph24.make = make
    assert got["Agent17"] == ("Agent17", 60, 200, 140.0, 200) and got["Agent14N2"] == ("Agent14N2", 60, 300, 240.0, 300), got
    assert [c.__name__ for c in Agent17.__mro__][:6] == ["Agent17", "Agent14N2", "ReleaseN2", "Agent14", "Release", "Agent9"] and not set(vars(Agent17)) - {"__module__", "__doc__", "__qualname__"}
    print(f"ok  construction: Agent17 {got['Agent17']}, Agent14N2 {got['Agent14N2']} (class, P, N_hi, counter at construction, window); Agent17's MRO starts Agent17, Agent14N2, ReleaseN2,"
          " Agent14, Release, Agent9 and its class body is empty")
    for w in ("T1", "W1", "T3a", "T3b"):
        assert every(run(w, Agent17, V10, sd, N_hi=N_HI, **kw), run(w, Agent14N2, V10, sd, **kw)), f"(I1) {w}"
    assert every(run("T1", Agent17, (1.0, -1.0), sd, N_hi=N_HI, **kw), run("T1", Agent14N2, (1.0, -1.0), sd, **kw)), "(I1) +1/-1"
    print("ok  (I1) Agent17 built with N_hi 300 == Agent14N2 on every recorded field, T1, W1, T3a, T3b, +1/-1 (40 x 200)")
    w17, w14 = run("W1", Agent17, V10, sd, **kw), run("W1", Agent14N2, V10, sd, **kw); a17, a14 = run("T3a", Agent17, V10, sd, **kw), run("T3a", Agent14N2, V10, sd, **kw)
    assert bitwise(w17, w14, ALLK) and c2_off(w17, w14) and bitwise(a17, a14, ALLK) and c2_off(a17, a14) and not every(w17, w14), "(I2)/(I3)"
    print("ok  (I2) W1, (I3) T3a: Agent17 == Agent14N2 on ph28.ALLK (PRES included), the valued counter exactly 100 lower, the counters themselves differ as constructed")
    o17, o14 = run("T1", Agent17, V10, sd, runs=n), run("T1", Agent14N2, V10, sd, runs=n); ok4, x = i4_check(o17, o14); assert ok4, x
    print(f"ok  (I4) T1 40 x 600: departing rows == exposure rows ({x['dep']} == {x['x']}), each departing exactly at its first exposure step ({x['at_fx']})")
    b17, b14 = run("T3b", Agent17, V10, sd, runs=n), run("T3b", Agent14N2, V10, sd, runs=n); ok5, i5 = i5_check(b17, b14, o17, o14); assert ok5, i5
    d = lost300(b17, W=N17); e = d["elig"]
    print(f"ok  (I5) T3b 40 x 600: == T1 before t0, draws == twin, Agent17 == Agent14N2 before the first neutral whiff at or after L + 200 ({i5['rows']}/{n}). Printed, not asserted:"
          f" window exact at L + 200 {int(d['exact'][e].sum())}/{int(e.sum())}")
    for t0 in T0_REP:
        r17, r14 = run("T3b", Agent17, V10, sd, runs=n, t0=t0), run("T3b", Agent14N2, V10, sd, runs=n, t0=t0); ok, ii = i5_check(r17, r14, o17, o14, t0=t0); assert ok, (t0, ii)
        assert not wv(r14)[t0:].any() and wv(r14)[:t0].sum() == wv(o14)[:t0].sum()
    print(f"ok  reported t0 {T0_REP}: the mask switches on at t0 (no valued whiff from t0; before t0 the T1 whiffs), == T1 before t0, draws == twin, (I5) at that t0")
    for kv in ((0.0, 0.0), (1.0, 1.0), (1.0, -1.0)):
        assert roweq(run("T1", Agent17, kv, sd, **kw), run("T1", Agent14N2, kv, sd, **kw), BEHK).all(), f"(I6) {kv}"
    print("ok  (I6) Agent17 == Agent14N2 on the behavioural fields at 0/0, +1/+1, +1/-1 (40 x 200)")
    r = stub(Agent17, kn, [(1, 1.0, 0.0), (399, 0.0, 0.0)], rows=20, seeds=sd); ok, ho = counter_exact(r, c0=140, N=200); tb = np.arange(400)[:, None]
    assert ok.all() and (ho == 0).all() and (r["C2"][:, :, 0] == tb).all() and (r["C2"][:, :, 1] == 140 + tb + 1).all() and (r["P2"][:, :, 1] == (tb <= 58)).all() \
        and (r["P2"][:, :, 0] == (tb <= 199)).all() and held_only(r) == 0, "counter convention"
    print("ok  counter convention (Agent17 stub, one whiff on channel 0 at step 0): c_0 = t, c_1 = 140 + t + 1; channel 1 present exactly on 0-58, channel 0 exactly on 0-199;"
          " held-only presence 0")
    tabb = {k: pp_dp(-k/400.0, k/400.0) for k in (5, 8, 10, 12, 13, 15)}; expb = {5: 1.00, 8: 0.99, 10: 0.89, 12: 0.65, 13: 0.51, 15: 0.26}
    assert all(abs(tabb[k] - expb[k]) < 0.006 for k in expb), tabb
    tab8 = {(m, s): Phi(m/(s/20.0) - 1.96) for m in (0.5, 0.9, 1.3) for s in (3, 4, 5, 6)}
    exp8 = {(0.5, 3): 0.91, (0.5, 4): 0.71, (0.5, 5): 0.52, (0.5, 6): 0.39, (0.9, 3): 1.00, (0.9, 4): 0.99, (0.9, 5): 0.95, (0.9, 6): 0.85,
            (1.3, 3): 1.00, (1.3, 4): 1.00, (1.3, 5): 1.00, (1.3, 6): 0.99}
    assert all(abs(tab8[k] - exp8[k]) < 0.006 for k in exp8), tab8
    pw = pass_prob(np.array([0.9 - 5.0, 0.9 + 5.0]*200), 0.0)[0]; assert abs(pw - tab8[(0.9, 5)]) < 1e-9
    print("ok  pass-probability arithmetic reproduces design section 7: M2(b) at k 5/8/10/12/13/15 = " + "/".join(f"{tabb[k]:.3f}" for k in expb)
          + "; M8(b) table (m 0.5/0.9/1.3 x s 3/4/5/6) = " + ", ".join(f"{tab8[k]:.2f}" for k in exp8) + f"; ph23.pass_prob at m 0.9, s 5 = {pw:.4f}")


# ------------------------------------------------------------------ the tasks (design sections 5-8)
def task_runs(seeds):
    t1 = {"Agent17": run("T1", Agent17, V10, seeds), "Agent14N2": run("T1", Agent14N2, V10, seeds), "Agent10g": run("T1", Agent10g, V10, seeds),
          "pathway-off": ph28.t1arm("pathway-off", seeds), "known-answer": ph28.t1arm("known-answer", seeds),
          "neutral": run("T1", Agent17, (0.0, 0.0), seeds), "neutral-ref": run("T1", Agent14N2, (0.0, 0.0), seeds)}
    w1 = {"Agent17": run("W1", Agent17, V10, seeds), "Agent14N2": run("W1", Agent14N2, V10, seeds), "Agent6": run("W1", Agent6, V10, seeds)}
    t3a = {"Agent17": run("T3a", Agent17, V10, seeds), "Agent14N2": run("T3a", Agent14N2, V10, seeds), "floor": run("T3a", Agent10, V10, seeds),
           "ceiling": ph28.run("T3a", None, V10, seeds, fixed="neutral")}
    t3b = {"Agent17": run("T3b", Agent17, V10, seeds), "Agent14N2": run("T3b", Agent14N2, V10, seeds), "Agent11 (N 60)": ph28.run11("T3b", 60, V10, seeds),
           "Agent10": run("T3b", Agent10, V10, seeds), "Agent10g": run("T3b", Agent10g, V10, seeds),
           "ceiling": ph28.run("T3b", None, V10, seeds, fixed="valued-then-neutral")}
    t4 = {"Agent17": run("T1", Agent17, (1.0, -1.0), seeds), "Agent14N2": run("T1", Agent14N2, (1.0, -1.0), seeds)}
    rep = {t0: {"Agent17": run("T3b", Agent17, V10, seeds, t0=t0), "Agent14N2": run("T3b", Agent14N2, V10, seeds, t0=t0)} for t0 in T0_REP}
    idr = {"I1 T1": run("T1", Agent17, V10, seeds, N_hi=N_HI), "I1 T3b": run("T3b", Agent17, V10, seeds, N_hi=N_HI),
           "I6 +1/+1 Agent17": run("T1", Agent17, (1.0, 1.0), seeds), "I6 +1/+1 Agent14N2": run("T1", Agent14N2, (1.0, 1.0), seeds)}
    return t1, w1, t3a, t3b, t4, rep, idr


def main(mode):
    seeds = SEEDS[mode]
    print(f"== H29, {mode.upper()}. design {DESIGN}; G 2, gate on; P {P_PRIOR}; Agent17 N_hi {N17}, Agent14N2 N_hi {N_HI}; t0 {T0} (reported t0 {T0_REP}); world seed {seeds[0]},"
          f" agent seed {seeds[1]}; {R} rows x {T} steps; geometry C0; bootstrap seed {ph15.BOOT_SEED}; {'operation check only (not a verdict)' if mode == 'dev' else 'the one evaluation'} ==")
    hok = header(); readings()
    hits, nums, nf = seeds_unused(); print(f"   seed self-check: the 18 numbers in no other file ({nf} scanned): {not hits}{'' if not hits else ' ' + str(hits)}")
    if hits or not hok: print("== REFUSED: a seed appears elsewhere or an imported file is not the version on record =="); sys.exit(2)
    print("   amendments: none")
    print("   rows share no state: one generator per world and one per agent population, fixed-size draws consumed in row order every step")
    t1, w1, t3a, t3b, t4, rep, idr = task_runs(seeds); maj = {a: majority(o) for a, o in t1.items()}
    print("\n== T1, the H21 choice task (+1/0; M1 arms as H26) ==")
    for a, o in t1.items():
        V, N, Z = maj[a]; k, pt, lo, hi = interval("P", V)
        print(f"   [T1 {a} {o['arm']}] V {int(V.sum())} N {int(N.sum())} tie {int(Z.sum())}; P(V) {k}/{R} = {pt:.3f} [{lo:.3f}, {hi:.3f}]; lost rows {int(lost_t1(o).sum())};"
              f" wall contacts per row {o['contacts'].mean():.3f}")
    c17, c14 = cls3(t1["Agent17"]), cls3(t1["Agent14N2"]); ok4, x = i4_check(t1["Agent17"], t1["Agent14N2"]); risk, _ = at_risk(t1["Agent14N2"]); risk0, _ = at_risk(t1["Agent14N2"], lo=0)
    print(f"   where the value goes: into V {int(((c17 == 0) & (c14 != 0)).sum())}, out of V {int(((c17 != 0) & (c14 == 0)).sum())}; exposure set (x) {x['x']} rows (first exposure step"
          f" {q3(x['fx'][x['inx']])}), departing rows {x['dep']}, departing exactly at their first exposure step {x['at_fx']}; H26's at-risk rows (m) {int(risk.sum())} (literal {int(risk0.sum())})")
    print("\n== W1, the absent-odour world (identity world; H26's M5 numbers REPORTED) ==")
    s2 = {a: w1sum(o) for a, o in w1.items()}
    for a, o in w1.items():
        s = s2[a]; f1 = first_true(o["NAV"])
        print(f"   [W1 {a} {o['arm']}] dwell at the present source mean {s['dwell'].mean():.3f} (quartiles {q3f(s['dwell'].astype(float))}); reach {int(s['reach'].sum())}/{R};"
              f" lost rows {int(s['lost'].sum())}; wall contacts per row {s['contacts'].mean():.3f}; first surge step {qq(f1)}; draws == twin {o['draws_equal'] and o['rng_equal']}")
    print("\n== T3a, the constructed loss (identity world; H26's M7 numbers REPORTED) ==")
    D3 = {a: t3_dwell(o, 100, T) for a, o in t3a.items()}
    for a, o in t3a.items():
        line = f"   [T3a {a} {o['arm']}] neutral dwell 100-599 mean {D3[a].mean():.3f} (quartiles {q3f(D3[a])})"
        if a != "ceiling":
            s3 = t3a_steps(o); line += f"; valued hold end step {qq(s3['end'])}; first neutral surge {qq(s3['surge'])}; first within 3.0 of the neutral source {qq(s3['arrive'])}"
        print(line)
    print(f"\n== T3b, the Lost world (mask from t0 {T0}; registered, M8) ==")
    Db = {a: t3_dwell(o, 400, T) for a, o in t3b.items()}
    for a, o in t3b.items():
        W = N17 if a == "Agent17" else 60 if a.startswith("Agent11") else N_HI
        d = lost300(o, W=W); e = d["elig"]
        if a != "ceiling": hold, end, rel = ph24.t3b_release(o); mm = hold & (end >= 0); hl = f"; holding valued at t0 {int(hold.sum())}, ended {int(mm.sum())} at origin + {q3(rel[mm])}"
        else: hl = "; the held odour fixed (valued, then neutral from t0)"
        print(f"   [T3b {a} {o['arm']}] neutral dwell 400-599 mean {Db[a].mean():.3f} (quartiles {q3f(Db[a])}); eligible {int(e.sum())}/{R}; L {q3(d['L'][e])}{hl};"
              f" first-neutral-surge delay after L {q3(d['delay'][e & (d['delay'] >= 0)])} (none {int((e & (d['delay'] < 0)).sum())})"
              + (f"; post-whiff window exact at L + {W} {int(d['exact'][e].sum())}/{int(e.sum())}" if a in ("Agent17", "Agent14N2", "Agent11 (N 60)") else ""))
    print("\n== T4, +1/-1 (World7; REPORTED) ==")
    for a, o in t4.items():
        V, N, Z = majority(o); k, pt, lo, hi = interval("P", V)
        print(f"   [T4 {a} {o['arm']}] V {int(V.sum())} N {int(N.sum())} tie {int(Z.sum())}; P(V) {pt:.3f} [{lo:.3f}, {hi:.3f}]; lost rows {int(lost_t1(o).sum())}; wall contacts per row {o['contacts'].mean():.3f}")
    judge(mode, seeds, t1, maj, w1, s2, t3a, D3, t3b, Db, t4, rep, idr, hok)


def judge(mode, seeds, t1, maj, w1, s2, t3a, D3, t3b, Db, t4, rep, idr, hok):
    ok = lambda z: "PASS" if z else "FAIL"
    print("\n== criteria (design v2 FINAL section 7; 95 percent, one evaluation, no extension; a multi-part criterion PASS if every part passes, FAIL if any fails, else INCONCLUSIVE;"
          " the unrounded bound decides) ==")
    # M1
    m1 = []
    for a in ("neutral", "pathway-off", "known-answer"):
        z = maj[a][2]; m1.append(ok(z.mean() <= 0.20)); print(f"   M1(a) {a}: ties {int(z.sum())}/{R} = {z.mean():.3f}  at most 0.20 -> {m1[-1]}")
    o = t1["neutral"]; V, N, Z = maj["neutral"]; which = np.where(V, o["good"], np.where(N, 1 - o["good"], -1))
    m1.append(crit("M1(b) neutral (Agent17 at 0/0), P(+y source majority | chose)", "P", (0.35, 0.65), False, (which == o["plus_y"])[~Z]))
    V, N, Z = maj["pathway-off"]; m1.append(crit("M1(c) floor: pathway-off, P(V | chose)", "P", (0.35, 0.65), False, V[~Z]))
    m1.append(crit("M1(d) ceiling: known-answer, P(V) over all rows", "P", 0.85, False, maj["known-answer"][0]))
    M1 = agg(m1); print(f"   M1 -> {M1}{'' if M1 == 'PASS' else '  (the run is UNREADABLE under section 8)'}")
    ties = {a: float(maj[a][2].mean()) for a in ("Agent17", "Agent14N2")}
    print("   section 8: ties in the arms under test " + ", ".join(f"{a} {v:.3f}" for a, v in ties.items()) + " (unreadable above 0.20)")
    # M2
    V17, V14, V10g = (maj[a][0] for a in ("Agent17", "Agent14N2", "Agent10g"))
    k, pt, lo, hi = interval("P", V17)
    print(f"   M2(a) Agent17 P(V) (REPORTED against 0.88): {k}/{R} = {pt:.3f} [{lo:.3f}, {hi:.3f}]; lower bound {'>=' if lo >= 0.88 else '<'} 0.88 (reported, not a criterion)")
    m2 = [crit("M2(b) DP = P(V) Agent17 - Agent14N2, same rows", "DP", -0.05, False, V17.astype(float), V14.astype(float)),
          crit("M2(c) DP = P(V) Agent17 - Agent10g, same rows", "DP", 0.05, False, V17.astype(float), V10g.astype(float))]
    M2 = agg(m2); print(f"   M2 -> {M2} (parts (b), (c))")
    _, dp, dlo, dhi = interval("DP", V17.astype(float), V14.astype(float))
    c17, c14 = cls3(t1["Agent17"]), cls3(t1["Agent14N2"]); into, outv = int(((c17 == 0) & (c14 != 0)).sum()), int(((c17 != 0) & (c14 == 0)).sum())
    print(f"      M2(b) unrounded: {dp:+.4f} [{dlo:+.4f}, {dhi:+.4f}]; into V {into}, out of V {outv}, k = {outv - into}")
    # M3
    i = {}; a17, a14 = t1["Agent17"], t1["Agent14N2"]
    i["(I1) Agent17 at N_hi 300 == Agent14N2 every field, T1"] = every(idr["I1 T1"], a14)
    i["(I1) T3b"] = every(idr["I1 T3b"], t3b["Agent14N2"])
    i["(I2) W1 == Agent14N2 on ALLK, valued counter 100 lower"] = bitwise(w1["Agent17"], w1["Agent14N2"], ALLK) and c2_off(w1["Agent17"], w1["Agent14N2"])
    i["(I3) T3a"] = bitwise(t3a["Agent17"], t3a["Agent14N2"], ALLK) and c2_off(t3a["Agent17"], t3a["Agent14N2"])
    ok4, x = i4_check(a17, a14); i["(I4) T1 departing rows == exposure rows, departing at the first exposure step"] = ok4
    ok5, i5 = i5_check(t3b["Agent17"], t3b["Agent14N2"], a17, a14); i["(I5) T3b"] = ok5
    i["(I6) 0/0"] = bool(roweq(t1["neutral"], t1["neutral-ref"], BEHK).all())
    i["(I6) +1/-1"] = bool(roweq(t4["Agent17"], t4["Agent14N2"], BEHK).all())
    i["(I6) +1/+1"] = bool(roweq(idr["I6 +1/+1 Agent17"], idr["I6 +1/+1 Agent14N2"], BEHK).all())
    ho = held_only(a17) + held_only(t3b["Agent17"]); i["(I7) held-only presence 0 (Agent17 T1, T3b)"] = ho == 0
    i["masked draws == World7 twin (W1, T3a, T3b)"] = all(o["draws_equal"] and o["rng_equal"] for o in list(w1.values()) + list(t3a.values()) + list(t3b.values()))
    i["T3a construction, every arm"] = all(construct_ok(o, a != "ceiling") for a, o in t3a.items())
    i["T3b == T1 on steps 0-149 (Agent17, Agent14N2, Agent10g)"] = bitwise(t3b["Agent17"], a17, n=T0) and bitwise(t3b["Agent14N2"], a14, n=T0) and bitwise(t3b["Agent10g"], t1["Agent10g"], n=T0)
    i["imported files as on record"] = hok
    M3 = ok(all(i.values()))
    print("   M3 identities: " + "; ".join(f"{k} {v}" for k, v in i.items()) + f" -> {M3}")
    print(f"      (I4) counts: (x) {x['x']} rows, departing {x['dep']}, at the first exposure step {x['at_fx']}; (I5) rows {i5['rows']}/{R}, departing exactly at the first neutral whiff"
          f" at or after L + {N17} {i5['dep_at_lim']}")
    # M4
    lines = []; v4, bo = bench(say=lines.append); M4 = ok(v4)
    m4line = next((ln for ln in lines if ln.startswith("== M4")), ""); same = False
    if os.path.exists(BENCH_TXT): same = m4line in open(BENCH_TXT, encoding="utf-8").read().split("\n")
    for ln in lines:
        if ln.startswith("== M4") or ln.startswith("(b) counter exact") or ln.startswith("(f)") or "STOP RULE" in ln or ln.startswith("(x)"):
            print("      " + ln.strip())
    print(f"   M4 mechanism bench, re-run here with the bench seeds (reading R11) -> {M4}; its M4 line equal to ph35_bench.txt's: {same}")
    # M6
    ls, l14 = lost_t1(a17).astype(float), lost_t1(a14).astype(float)
    m6 = [crit("M6(a) T1 no whiff of either plume in the last third, Agent17 - Agent14N2", "DP", 0.05, True, ls, l14)]
    cm = a17["contacts"].mean(); m6.append(ok(cm <= 0.10)); print(f"   M6(b) T1 Agent17, wall contacts per row: mean {cm:.3f}  at most 0.10 -> {m6[-1]}")
    M6 = agg(m6); print(f"   M6 -> {M6}")
    # M8
    d17 = lost300(t3b["Agent17"], W=N17); e17 = d17["elig"]
    m8a = crit(f"M8(a) T3b Agent17, the window exact at L + {N17} (eligible rows)", "P", 0.95, False, d17["exact"][e17])
    print(f"      M8(a) parts: no nav on a neutral-only whiff on L+1..L+{N17 - 1} {int(d17['a1'][e17].sum())}, first neutral surge = first neutral whiff at or after L+{N17}"
          f" {int(d17['a2'][e17].sum())}, valued not held from L+60 {int(d17['a3'][e17].sum())} of {int(e17.sum())}")
    D17, D14 = Db["Agent17"], Db["Agent14N2"]; g_ = D17 - D14
    _, gm, glo, ghi = interval("DP", D17, D14); m8b = verdict_gt0(glo, ghi)
    print(f"   M8(b) paired T3b neutral dwell 400-599 Agent17 - Agent14N2 (400 rows, reading R4): {gm:+.4f} [{glo:+.4f}, {ghi:+.4f}] (sd {g_.std():.4f}; rows gaining {int((g_ > 0).sum())},"
          f" losing {int((g_ < 0).sum())}, equal {int((g_ == 0).sum())}); lower bound > 0 -> {m8b}")
    M8 = agg([m8a, m8b]); print(f"   M8 -> {M8}")
    D60, Dfl, Dce = Db["Agent11 (N 60)"], Db["Agent10"], Db["ceiling"]
    Rb, Rblo, Rbhi = ratio_boot(D17, D14, D60); R17, R17lo, R17hi = ratio_boot(D17, Dfl, Dce); R14, R14lo, R14hi = ratio_boot(D14, Dfl, Dce)
    _, spn, slo, shi = interval("DP", Dce, Dfl)
    print(f"      reported (no bar): R_b = (D_17 - D_14N2) / (D_60 - D_14N2) = {Rb:.4f} [{Rblo:.4f}, {Rbhi:.4f}] (D_60 {D60.mean():.3f}); H25's R (floor Agent10 {Dfl.mean():.3f},"
          f" ceiling Agent5 valued then neutral {Dce.mean():.3f}, span {spn:.3f} [{slo:.3f}, {shi:.3f}]): Agent17 {R17:.4f} [{R17lo:.4f}, {R17hi:.4f}], Agent14N2 {R14:.4f} [{R14lo:.4f}, {R14hi:.4f}]")
    # reported: W1 (H26's M5), T3a (H26's M7), T4, the phase-sensitivity condition
    s17, s14, s6 = s2["Agent17"], s2["Agent14N2"], s2["Agent6"]; k, pt, lo, hi = interval("P", s17["reach"]); _, dm, dlo_, dhi_ = interval("DP", s17["dwell"].astype(float), s6["dwell"].astype(float))
    ex5, _, _ = first_surge_ok(w1["Agent17"], PR)
    print(f"   REPORTED W1 (H26's M5 quantities; identity world): Agent17 reach {k}/{R} = {pt:.3f} [{lo:.3f}, {hi:.3f}]; dwell {s17['dwell'].mean():.3f} vs Agent14N2 {s14['dwell'].mean():.3f}"
          f" vs Agent6 {s6['dwell'].mean():.3f}, paired Agent17 - Agent6 {dm:+.3f} [{dlo_:+.3f}, {dhi_:+.3f}]; wall contacts per row {s17['contacts'].mean():.3f}; lost rows Agent17"
          f" {int(s17['lost'].sum())}, Agent14N2 {int(s14['lost'].sum())}, Agent6 {int(s6['lost'].sum())}; first surge == first neutral whiff at or after {PR} {int(ex5.sum())}/{R}")
    ex7, _ = m7a_t3a(t3a["Agent17"]); Dc3, Df3 = D3["ceiling"], D3["floor"]; _, sp3, sp3lo, sp3hi = interval("DP", Dc3, Df3); R3, R3lo, R3hi = ratio_boot(D3["Agent17"], Df3, Dc3)
    print(f"   REPORTED T3a (H26's M7 quantities; identity world): M7(a) exact Agent17 {int(ex7.sum())}/{R}; R = {R3:.4f} [{R3lo:.4f}, {R3hi:.4f}] (floor Agent10 {Df3.mean():.3f},"
          f" ceiling {Dc3.mean():.3f}, span {sp3:.3f} [{sp3lo:.3f}, {sp3hi:.3f}], {'readable' if sp3lo >= 5.0 else 'UNREADABLE'} at the bound 5.0); Agent17 == Agent14N2 in dwell row for row"
          f" {bool(np.array_equal(D3['Agent17'], D3['Agent14N2']))}")
    for a in ("Agent17", "Agent14N2"):
        V, N, Z = majority(t4[a]); k, pt, lo, hi = interval("P", V)
        print(f"   REPORTED M9 T4 +1/-1 [{a}]: V {int(V.sum())} N {int(N.sum())} tie {int(Z.sum())}; P(V) {pt:.3f} [{lo:.3f}, {hi:.3f}]; lost rows {int(lost_t1(t4[a]).sum())};"
              f" wall contacts per row {t4[a]['contacts'].mean():.3f}")
    print(f"\n== REPORTED: the phase-sensitivity condition (design v2 section 5; T3b at t0 {T0_REP}; no bar, no stop rule, outside the verdict) ==")
    L150 = lost300(t3b["Agent14N2"])["L"]
    for t0, rr in rep.items():
        o17, o14 = rr["Agent17"], rr["Agent14N2"]; d17r, d14r = lost300(o17, t0=t0, W=N17), lost300(o14, t0=t0, W=N_HI); e = d14r["elig"]; ne = int(e.sum()); L = d14r["L"]
        D17r, D14r = t3_dwell(o17, 400, T), t3_dwell(o14, 400, T); gr = D17r - D14r; _, gmr, glr, ghr = interval("DP", D17r, D14r); okr, ir = i5_check(o17, o14, a17, a14, t0=t0)
        print(f"   [t0 {t0}] eligible rows {ne}/{R}{'' if ne >= 50 else ' (under 50: UNREADABLE)'}; L {q3(L[e])} (min {L[e].min() if ne else 'n/a'}, max {L[e].max() if ne else 'n/a'}); t0 - L"
              f" {q3(t0 - L[e])}; rows whose L equals the row's L at t0 {T0}: {int((e & (L == L150)).sum())}")
        print(f"      neutral dwell 400-599: Agent17 {D17r.mean():.3f} (quartiles {q3f(D17r)}), Agent14N2 {D14r.mean():.3f} ({q3f(D14r)}); paired Agent17 - Agent14N2 {gmr:+.4f}"
              f" [{glr:+.4f}, {ghr:+.4f}] (sd {gr.std():.4f}); rows gaining {int((gr > 0).sum())}, losing {int((gr < 0).sum())}, equal {int((gr == 0).sum())}")
        e17r = d17r["elig"]
        print(f"      window exact: Agent17 at L + {N17} {int(d17r['exact'][e17r].sum())}/{int(e17r.sum())}, Agent14N2 at L + {N_HI} {int(d14r['exact'][e].sum())}/{ne}; first neutral surge"
              f" after L: Agent17 {q3(d17r['delay'][e17r & (d17r['delay'] >= 0)])} (none {int((e17r & (d17r['delay'] < 0)).sum())}), Agent14N2 {q3(d14r['delay'][e & (d14r['delay'] >= 0)])}"
              f" (none {int((e & (d14r['delay'] < 0)).sum())}); (I5) at t0 {t0}: {okr} (== T1 before t0 {ir['pre']}, rows {ir['rows']}/{R}, draws {ir['draws']})")
    unread = M1 != "PASS" or max(ties.values()) > 0.20 or M3 != "PASS" or M4 != "PASS" or "UNREADABLE" in (M2, M6, M8)
    verdict = all(z == "PASS" for z in (M1, M2, M3, M4, M6, M8)); fail = any(z == "FAIL" for z in (M2, M6, M8))
    lab = "PASS" if verdict else "UNREADABLE" if unread and not fail else "FAIL" if fail else "INCONCLUSIVE"
    print(f"\n== H29 ==  M1 {M1}  M2 {M2}  M3 {M3}  M4 {M4}  M6 {M6}  M8 {M8}  (M2(a), M9 T4, W1, T3a, R_b, R and the t0 condition reported) -> {lab}: "
          + ("with the presence window after a whiff shortened from 300 to 200 steps and the 59-step prior unchanged, the adopted agent keeps its choice in the H21 task within 0.05"
             " of itself with the 300-step window, is unchanged in the absent-odour world and after a loss from step 0, and after the valued odour is lost following tracking opens"
             " the filter exactly 200 steps after the last valued whiff and dwells longer at the neutral source late in the run than the adopted agent on the same rows"
             if verdict else "UNREADABLE (section 8)" if lab == "UNREADABLE" else "NOT shown under the registered criteria")
          + (" [development run: an operation check, not a verdict]" if mode == "dev" else ""))


if __name__ == "__main__":
    mode = ([m for m in sys.argv[1:] if m in ("demo", "bench", "dev", "eval")] or ["demo"])[0]
    if mode == "demo": demo(); sys.exit(0)
    if mode == "bench":
        hits, nums, nf = seeds_unused()
        if hits: print(f"== REFUSED: a seed of this run appears in {hits} =="); sys.exit(2)
        print(f"   seed self-check before the first run: the 18 numbers in no other file ({nf} scanned): True")
        v, o = bench(); sys.exit(0 if v and not o["stop"] else 3 if v else 1)
    main(mode)
