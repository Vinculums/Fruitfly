#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T3b diagnosis (measurement only; owner 2026-09-26, '그래 그럼 권고안으로 진행', decision:t3b-diagnosis): the H26 T3b limit, a loss after
tracking, measured on the adopted agent Agent14N2 before any H29 run (H29 design v1 DRAFT section 12 point 1).

Usage: python ph34b.py      (writes experiments/h29/ph34b_diag.txt, LF line ends)

Nothing is changed: ph28.py (Agent14, the H26 counter), ph30.py (ReleaseN2, Agent14N2, the adopted agent), ph22.py (the Masked world),
ph23.py (Agent9's counter and filter, the Lost world), ph24.py and ph25.py (the harness and its record) and every module they import are
imported as they are (sha256 prefixes checked below against the ones H29 design v1 cites); no rule, bar or adopted file is changed, no
hypothesis is opened, nothing is tuned. Agent17 (Agent14N2 with N_hi 200, counter start 140) and the window arms (N_hi 60, 150, 250) are
MEASUREMENT ARMS only, built through Agent14's existing constructor arguments (ph28.py:95-97), as the H24 Run 2 N sweep ran its N arms.
Seeds: H26's bench seeds (ph28.BS) and H26's bootstrap seed (set on ph15 by ph28's import) are reused ON PURPOSE (spent, registered to
H26; decision:t3b-diagnosis, after the R3 and H17 post-bench diagnosis precedents); H26's evaluation seeds (ph28.SEEDS['eval']) are used
for the reproduction check ONLY (the R3 diagnosis precedent, experiments/avoidance_check/r3_diagnosis.md: 'the H25 evaluation seeds are
reused for a reproduction, not for new evidence'). Every seed is read from the imported scripts; no seed digit is written in this file
or its output (checked at the end against every seed constant of ph22, ph24, ph25, ph28 and ph30 and their derived numbers). No H29
registered seed is used. This script registers no seed and runs no repository seed scan; the one registered scan exclusion pair,
experiments/h20/ph31_eval.txt with decision:seed-scan-exclusion-ph31-eval, is cited by reference and not touched.

Reproduction first: H26's T3b arm (Agent14, the Lost world, 400 x 600) and its T1 twin are re-run through ph28's own functions
(ph28.run, run11, warm, t1arm, lost300) and the lines they print must equal experiments/h26/ph28_bench.txt's (f) Lost-world lines and the
Agent14 part of its (h) line, and experiments/h26/ph28_eval.txt's T3b lines (adaptive, fixed N 60) and the T1 twin lines (the adaptive
arm's V/N/tie and its H26 diag line), character for character. Agent14N2 must equal Agent14 on every recorded field in those runs (by
code, ph30.py:128-132, at non-negative values). On any mismatch nothing is measured.

Readings where decision:t3b-diagnosis is silent (fixed before the first run; printed again in the output):
 (R1) Agent14N2 is built by a run-time hook on ph24.make, as ph30's i5_check did: for the class Agent14N2, Agent14N2(runs, rng, P, N_hi,
      G, known, rule=gate, filt, scope, release) with (P, N_hi) from ph28's own context (ph28.pn); everything else goes to ph28's make.
      Agent17 = (P 60, N_hi 200); the window arms = (P 60, N_hi W): the 59-step prior unchanged in every arm.
 (R2) L: the valued column of the Lost world is masked from t0, so no valued whiff is sensed at or after t0; 'the last valued whiff' is
      the last one before t0 (ph28 reading R8); eligible rows have one. Every F2, F3, F4, F6 population is the eligible rows.
 (R3) F1 'every field': every per-step array the harness records (the list is printed), compared on steps 0 .. F_r - 1, F_r = the T1
      twin's first valued whiff at or after t0 (600 if none); the whiffs W included (the masked column is False in both before F_r).
 (R4) Positions: the position step t sensed at (POS[t - 1]; ph26b's convention). Relative to the NEUTRAL source: d_along = x - x_src
      (downwind > 0; both sources share x), d_cross = |y - y_src|. Classes: inside the cone (0 < d_along < 25 and d_cross < W0 + SLOPE
      d_along, ph11.py:80), in the along range outside the width, upwind (d_along <= 0), beyond LMAX (d_along >= 25); 'at a wall' (within
      1.0 of a wall, walls at 0 and 160; ph26b's WALL_NEAR) is a flag printed beside, and also as ph26b's first exclusive class. F2's
      threshold reads the along range only: outside = d_along <= 0 or d_along >= 25. Rows with L + k > 599 use step 599.
 (R5) F3: the first neutral surge at or after L + 300 = the first step s >= L + 300 with nav and a neutral whiff; 'within 200 steps'
      = s - (L + 300) <= 200; the denominator is every eligible row with L + 300 <= 599 (a row censored at 599 with no surge counts as
      not within); the uncensored subset (L + 500 <= 599) printed beside.
 (R6) F4: L' = the twin's first valued whiff after L (== F_r: the rows are equal before t0 and L is the last before t0). The fraction
      <= 200 over all eligible rows ('never by 599' is not within); the median over all eligible rows with 'never' ranked above every
      delay; the median among twins that whiff printed beside.
 (R7) F5: V = the dwell majority (ph18.majority); DP P(V) Agent17 - Agent14N2 with ph16.interval('DP') (paired bootstrap, 5000, H26's
      bootstrap seed). W1 and T3a identity: ph28.ALLK bitwise (PRES included) and the valued counter exactly 100 lower on every (row,
      step). T3b dwell = steps within 3.0 of the neutral source over 400-599 (ph24.t3_dwell); R = (D - D_floor) / (D_ceiling - D_floor),
      floor Agent10, ceiling Agent5 fixed to the valued odour then to the neutral from t0 (ph24's T3b ceiling), ph24.ratio_boot; R_b =
      (D_17 - D_14N2) / (D_60 - D_14N2), D_60 the window-60 arm.
 (R8) F6: step t of a row's whiff record is a valued burst iff a valued whiff on t and at least two valued whiffs on t-9 .. t-1 (the H28
      definition, ph33 reading R12); b10(t) = bursts on t-9 .. t, b30(t) = bursts on t-29 .. t. The state at step t is the recorded value
      after that step's act: held odour (none / valued / neutral), since, silence, cast phase = since mod 2 SAT (SAT from ph12), the valued
      and neutral presence counters. Population A: the T3b eligible rows at L and L + 48. Population B: every valued silence of Agent14N2's
      T1 run that reaches >= 210 steps (a valued whiff at s, the next at s' with s' - s - 1 >= 210, or none and 599 - s >= 210), at s and
      s + 48. A cut: q <= c and q > c for every observed value c (each category and its complement for the held odour); fA, fB the
      fractions of A and B on that side. 'Separates at 0.80 vs 0.20': one fraction >= 0.80 and the other <= 0.20; 'better than 0.65 vs
      0.35': one > 0.65 and the other < 0.35. Per-pair identity: eligible rows whose twin silence from L is itself >= 210.
 (R9) (t) profile: re-scored = the first neutral whiff at or after L + W in Agent14N2's own T3b run (a window-W agent's surge where its
      trajectory equals Agent14N2's before that step, by the construction of H29 design (I5)); measured = the window-W arm's own first
      neutral surge after L. Both printed, with the rows where they agree and the rows where the arm's trajectory equals Agent14N2's on
      every step before the re-scored step.
Names no cause beyond what is measured; tests no change. Nothing changes after the table.
"""
import sys, os, hashlib
import numpy as np
import ph28                                      # Agent14; hooks ph24.make / ph23.make; sets H26's bootstrap seed on ph15
import ph15
_STATS26 = (ph15.Z, ph15.QLO, ph15.QHI, ph15.BOOT_SEED)
import ph30                                      # Agent14N2 (its import sets its own statistics; H26's are restored below)
import ph11, ph12, ph12b, ph16, ph18, ph21, ph22, ph23, ph24, ph25, ph25b
ph30.set_stats(*_STATS26)                        # H26's 95 percent level and bootstrap seed (read from ph28's import), cache emptied
from ph28 import Agent14, BS, N_HI, P_PRIOR, ALLK, BEHK, lost300, first_valued
from ph30 import Agent14N2
from ph24 import Agent10, t3_dwell, ratio_boot, q3f
from ph25 import Agent11, cls3, w1sum
from ph23 import T0, wv, wn, presence_identity
from ph21 import q3, first_true
from ph18 import majority
from ph16 import interval, R, T
from ph12 import SAT
from ph12b import ARENA2
from ph9 import W0, SLOPE, LMAX

sys.stdout.reconfigure(newline="\n")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
BENCH_TXT = os.path.join(REPO, "experiments", "h26", "ph28_bench.txt"); EVAL_TXT = os.path.join(REPO, "experiments", "h26", "ph28_eval.txt")
OUT = os.path.join(REPO, "experiments", "h29", "ph34b_diag.txt")
DESIGN29 = os.path.join(REPO, "experiments", "h29", "h29_design_v1.md")
PREFIX = dict(ph11="e80f40bd", ph12="e1035e09", ph22="03ab8c47", ph23="ae180492", ph24="f344f178", ph25b="ad12a912", ph28="64ce7d0c", ph30="98822834")
V10 = (1.0, 0.0)
N17 = 200                                        # Agent17's window (H29 design 3.2)
WINS = (60, 150, 200, 250, 300)                  # the (t) profile's windows
WALL_NEAR = 1.0                                  # ph26b's 'at a wall'
LONG = 210                                       # F6: the H17 table's long-silence length
MODS = (ph11, ph12, ph12b, ph15, ph16, ph18, ph21, ph22, ph23, ph24, ph25, ph25b, ph28, ph30)


def sha(p=__file__): return hashlib.sha256(open(p, "rb").read()).hexdigest()


_lines = []
def say(s=""): _lines.append(s); print(s, flush=True)
def fr(k, n): return f"{k}/{n} = {k / n:.3f}" if n else f"{k}/0"
def pct(x, qs=(25, 50, 75, 90)): return "/".join(f"{np.percentile(x, q):.0f}" for q in qs) if len(x) else "n/a"


# ------------------------------------------------------------------ the builder hook (reading R1)
_make_prev = ph24.make                            # ph28.make


def make(cls, runs, rng, G, known, gate=True, filt=True, release=True):
    if cls is Agent14N2:
        P, N = ph28._PN[0]
        return Agent14N2(runs, rng, P=P, N_hi=N, G=G, known=known, rule=gate, filt=filt, scope=ph25._SCOPE[0], release=release)
    return _make_prev(cls, runs, rng, G, known, gate, filt, release)


ph24.make = make


def n2(world, seeds, N_hi=N_HI, vals=V10, **kw): return ph28.run(world, Agent14N2, vals, seeds, P=P_PRIOR, N_hi=N_hi, **kw)


def fields(o): return sorted(k for k, v in o.items() if isinstance(v, np.ndarray) and v.ndim >= 2 and v.shape[0] == o["steps"])


def every(o1, o2, n=None):
    ks = fields(o1); return ks == fields(o2) and all(np.array_equal(o1[k][:n], o2[k][:n]) for k in ks)


# ------------------------------------------------------------------ reproduction
def file_lines(p): return open(p, encoding="utf-8").read().split("\n")


def reproduce():
    say("== reproduction (H26's own functions; lines compared character for character) ==")
    bl, el = file_lines(BENCH_TXT), file_lines(EVAL_TXT); ok = True; n = R
    # ---- bench: (f) Lost-world lines and the Agent14 part of (h)
    lw = {"Agent14": ph28.run("T3b", Agent14, V10, BS), "Agent11 (N 60)": ph28.run11("T3b", 60, V10, BS)}
    o14 = ph28.run("T1", Agent14, V10, BS)
    dl = lost300(lw["Agent14"]); e = dl["elig"]; k_, pt, lo_l, hi = interval("P", dl["exact"][e])
    got = [f"(f) post-whiff window exact in the Lost world, Agent14, eligible rows (a valued whiff before t0, L = the last one; reading R8): {k_}/{int(e.sum())} = {pt:.3f} [{lo_l:.3f}, {hi:.3f}]"
           f" (bar lower bound >= 0.95) -> {'PASS' if lo_l >= 0.95 else 'FAIL'}; parts (no nav on a neutral-only whiff on L+1..L+{N_HI - 1}, first neutral surge after L = first neutral"
           f" whiff at or after L+{N_HI}, valued not held from L+60): {int(dl['a1'][e].sum())}/{int(dl['a2'][e].sum())}/{int(dl['a3'][e].sum())}; any nav on L+1..L+{N_HI - 1}"
           f" {int(dl['anynav'][e].sum())} rows; L {q3(dl['L'][e])}; first-neutral-surge delay after L {q3(dl['delay'][e & (dl['delay'] >= 0)])} (none {int((e & (dl['delay'] < 0)).sum())})"]
    for k in lw:
        hold, end, rel = ph24.t3b_release(lw[k]); mm = hold & (end >= 0)
        got.append(f"      [Lost {k}] holding valued at t0 {int(hold.sum())}/{n}; ended {int(mm.sum())} (never {int((hold & (end < 0)).sum())}), relative to the origin {q3(rel[mm])};"
                   f" neutral dwell 400-599 mean {t3_dwell(lw[k], 400, 600).mean():.3f}")
    for g_ in got:
        m = g_ in bl; ok &= m; say(f"   bench {'MATCH' if m else 'MISMATCH'}: {g_.strip()}")
    V, N_, Z = majority(o14); _, p1, l1, h1 = interval("P", V)
    t1s = f"Agent14 V {int(V.sum())} N {int(N_.sum())} tie {int(Z.sum())} P(V) {p1:.3f} [{l1:.3f}, {h1:.3f}]"
    m = any(ln.startswith("(h) T1 on bench seeds") and t1s in ln for ln in bl); ok &= m; say(f"   bench (h) T1 twin {'MATCH' if m else 'MISMATCH'}: {t1s}")
    # ---- Agent14N2 == Agent14 (bench)
    b3, b1 = n2("T3b", BS), n2("T1", BS)
    idb = every(b3, lw["Agent14"]) and every(b1, o14); ok &= idb
    say(f"   bench: Agent14N2 (hook, reading R1) == ph28's Agent14 on every recorded field ({len(fields(b3))} per-step arrays), T3b and T1: {idb}")
    # ---- evaluation seeds: the reproduction check only
    es = ph28.SEEDS["eval"]
    ta, t60, t1a = ph28.warm("T3b", Agent14, es), ph28.warm("T3b", Agent11, es), ph28.t1arm("adaptive", es)
    got = []
    for a, o in (("adaptive", ta), ("fixed N 60", t60)):
        Db = t3_dwell(o, 400, T); hold, end, rel = ph24.t3b_release(o); mm = hold & (end >= 0)
        d = lost300(o) if a == "adaptive" else ph25.t3_lost(o); e = d["elig"]
        got.append(f"   [T3b {a} {o['arm']}] neutral dwell 400-599 mean {Db.mean():.3f} (quartiles {q3f(Db)}); eligible {int(e.sum())}/{R}; holding valued at t0 {int(hold.sum())}, ended"
                   f" {int(mm.sum())} at origin + {q3(rel[mm])}; first-neutral-surge delay after L {q3(d['delay'][e & (d['delay'] >= 0)])} (none {int((e & (d['delay'] < 0)).sum())})"
                   + (f"; post-whiff window exact at L + {N_HI} {int(d['exact'][e].sum())}/{int(e.sum())}" if a == "adaptive" else f"; window-60 exact (ph25's check) {int(d['exact'][e].sum())}/{int(e.sum())}"))
    V, N_, Z = majority(t1a); k, pt, lo, hi = interval("P", V)
    got.append(f"      reported: adaptive ({t1a['arm']}) V {V.sum()} N {N_.sum()} tie {Z.sum()}; P(V) {k}/{R} = {pt:.3f} [{lo:.3f}, {hi:.3f}]")
    fd = first_true(t1a["DIFF8"]); hn = t1a["H"] == (1 - t1a["good"])[None, :]
    got.append(f"      H26 diag [adaptive]: `differs8` rows {int((fd >= 0).sum())}/{R}, first `differs8` step {q3(fd[fd >= 0])}, (row, step) {int(t1a['DIFF8'].sum())}; valued present on"
               f" {t1a['PRES'].mean():.3f} of (row, step), on {t1a['PRES'][hn].mean() if hn.any() else float('nan'):.3f} of neutral-held (row, step); presence identity {presence_identity(t1a)}")
    for g_ in got:
        m = g_ in el; ok &= m; say(f"   evaluation {'MATCH' if m else 'MISMATCH'}: {g_.strip()}")
    e3, e1 = n2("T3b", es), n2("T1", es)
    ide = every(e3, ta) and every(e1, t1a); ok &= ide
    say(f"   evaluation: Agent14N2 == ph28's Agent14 on every recorded field, T3b and T1: {ide} (so the evaluation's 4.412 and 'none 173' of 379 are the adopted agent's own)")
    say(f"== reproduction {'PASSED: every line MATCH, identities True' if ok else 'FAILED: nothing is measured'} ==")
    return ok, dict(b3=b3, b1=b1, a60=lw["Agent11 (N 60)"])


# ------------------------------------------------------------------ geometry and helpers
def at(o, t, r): return o["POS"][t - 1, r] if t > 0 else o["start"][r]


def geo(o, ts, rows):
    """reading R4: per row at step ts[i], relative to the neutral source"""
    ng = 1 - o["good"]; out = []
    for r, t in zip(rows, ts):
        p = at(o, int(t), r); s = o["src"][r, ng[r]]; da = p[0] - s[0]; dc = abs(p[1] - s[1])
        wall = min(p[0], ARENA2 - p[0], p[1], ARENA2 - p[1]) < WALL_NEAR
        cone = (0 < da < LMAX) and dc < W0 + SLOPE*da
        cls = "cone" if cone else "range" if 0 < da < LMAX else "upwind" if da <= 0 else "beyond"
        out.append(dict(da=da, dc=dc, wall=wall, cls=cls, excl="wall" if wall else cls, p=p))
    return out


CLS = (("cone", "inside the neutral cone"), ("range", "in the along range, outside the cone's width"), ("upwind", "upwind (d_along <= 0)"), ("beyond", "beyond LMAX (d_along >= 25)"))


def bursts(x):
    """reading R8: x (steps, rows) bool whiffs -> burst (steps, rows)"""
    c = np.cumsum(np.vstack([np.zeros((1, x.shape[1]), int), x.astype(int)]), 0)        # c[t] = whiffs on 0..t-1
    prev9 = c[np.arange(x.shape[0])] - c[np.maximum(np.arange(x.shape[0]) - 9, 0)]      # whiffs on t-9..t-1
    return x & (prev9 >= 2)


def wsum(b, t, r, k): return int(b[max(t - k + 1, 0):t + 1, r].sum())


def state(o, B, t, r):
    g = o["good"][r]; h = int(o["H"][t, r]); sn = float(o["SINCE"][t, r])
    return dict(b10=wsum(B, t, r, 10), b30=wsum(B, t, r, 30), held="none" if h < 0 else "valued" if h == g else "neutral", since=sn,
                silence=float(o["SIL"][t, r]), phase=float(sn % (2*SAT)), cv=float(o["C2"][t, r, g]), cn=float(o["C2"][t, r, 1 - g]))


QK = ("b10", "b30", "held", "since", "silence", "phase", "cv", "cn")
QN = dict(b10="valued bursts in the last 10 steps", b30="valued bursts in the last 30 steps", held="held odour", since="since", silence="silence",
          phase="cast phase (since mod 2 SAT)", cv="valued presence counter", cn="neutral presence counter")


def best_cut(a, b):
    """reading R8: every cut; returns (best |fA - fB| cut, sep80 cut or None, better65 cut or None)"""
    a, b = np.asarray(a, object), np.asarray(b, object); cuts = []
    if isinstance(a[0], str) or isinstance(b[0], str):
        for c in sorted(set(a) | set(b)):
            fa, fb = float(np.mean(a == c)), float(np.mean(b == c)); cuts += [(f"== {c}", fa, fb), (f"!= {c}", 1 - fa, 1 - fb)]
    else:
        af, bf = a.astype(float), b.astype(float)
        for c in np.unique(np.concatenate([af, bf])):
            fa, fb = float(np.mean(af <= c)), float(np.mean(bf <= c)); cuts += [(f"<= {c:g}", fa, fb), (f"> {c:g}", 1 - fa, 1 - fb)]
    best = max(cuts, key=lambda z: abs(z[1] - z[2]))
    s80 = next((z for z in cuts if (z[1] >= 0.80 and z[2] <= 0.20) or (z[2] >= 0.80 and z[1] <= 0.20)), None)
    b65 = next((z for z in cuts if (z[1] > 0.65 and z[2] < 0.35) or (z[2] > 0.65 and z[1] < 0.35)), None)
    return best, s80, b65


def summ(v):
    v = np.asarray(v, object)
    if isinstance(v[0], str): return ", ".join(f"{c} {int(np.sum(v == c))}" for c in ("none", "valued", "neutral"))
    x = v.astype(float); return f"{np.percentile(x, 25):.1f}/{np.median(x):.1f}/{np.percentile(x, 75):.1f} (min {x.min():.1f}, max {x.max():.1f})"


# ------------------------------------------------------------------ the measurements (bench seeds only)
def measure(b3, b1, a60):
    n = R; tt = np.arange(T)[:, None]; rows = np.arange(n); table = []
    g = b3["good"]; ng = 1 - g
    dl = lost300(b3); e = dl["elig"]; L = dl["L"]; er = np.flatnonzero(e); ne = len(er)
    say(f"\n== bench runs (H26's bench seeds, digits not printed): Agent14N2 T1 and T3b (the reproduction's runs), 400 x 600, +1/0, t0 {T0} ==")
    say(f"   T3b eligible rows (a valued whiff before t0): {ne}/{n}; L {q3(L[e])} (min {L[e].min()}, max {L[e].max()}); window exact at L + {N_HI} {int(dl['exact'][e].sum())}/{ne};"
        f" first neutral surge after L, delay {q3(dl['delay'][e & (dl['delay'] >= 0)])}, none before 600 {int((e & (dl['delay'] < 0)).sum())}/{ne}")
    # ---------------- F1
    vt = wv(b1); Fr = first_true(vt & (tt >= T0)); Fx = np.where(Fr < 0, T, Fr); ks = fields(b3)
    eqrow = np.ones(n, bool); first_bad = None
    for r in rows:
        for k in ks:
            a_, b_ = b3[k][:Fx[r], r], b1[k][:Fx[r], r]
            if not np.array_equal(a_, b_):
                eqrow[r] = False
                if first_bad is None:
                    bad = np.flatnonzero((a_ != b_).reshape(len(a_), -1).any(1))[0]; first_bad = (int(r), int(bad), k)
                break
    after = np.array([not all(np.array_equal(b3[k][:, r], b1[k][:, r]) for k in ks) for r in rows])
    F1 = "MET" if eqrow.all() else "NOT MET"
    say(f"\n== F1 twin identity (reading R3; fields: {', '.join(ks)}) ==")
    say(f"   rows equal on every field on steps 0 .. F_r - 1: {int(eqrow.sum())}/{n}; first differing (row, step, field): {first_bad if first_bad else 'none'};"
        f" F_r (the twin's first valued whiff at or after t0) {q3(Fr[Fr >= 0])} (none {int((Fr < 0).sum())}); rows that differ somewhere after F_r {int(after.sum())}/{n}")
    say(f"   F1 -> {F1} (registered: MET iff 400/400 rows equal)")
    table.append(("F1 twin identity", f"{int(eqrow.sum())}/{n} rows equal before F_r" + (f"; first difference {first_bad}" if first_bad else ""), "MET iff 400/400", F1))
    # ---------------- F2
    say(f"\n== F2 the blind-window trajectory (reading R4; eligible rows {ne}) ==")
    within = e & (L + N_HI <= T - 1); nw = int(within.sum()); G2 = {}
    for kk in (100, 200, N_HI):
        ts = np.minimum(L[er] + kk, T - 1); G2[kk] = gg = geo(b3, ts, er)
        cnt = {c: sum(x["cls"] == c for x in gg) for c, _ in CLS}; ex = {c: sum(x["excl"] == c for x in gg) for c in ("wall", "cone", "range", "upwind", "beyond")}
        outr = cnt["upwind"] + cnt["beyond"]
        say(f"   at L + {kk}: " + "; ".join(f"{lab} {fr(cnt[c], ne)}" for c, lab in CLS) + f"; at a wall (flag) {sum(x['wall'] for x in gg)};"
            f" outside the along range {fr(outr, ne)}; ph26b-style exclusive (wall first): " + ", ".join(f"{c} {v}" for c, v in ex.items()))
        say(f"      d_along {q3f(np.array([x['da'] for x in gg]))} (min {min(x['da'] for x in gg):.1f}, max {max(x['da'] for x in gg):.1f}); d_cross {q3f(np.array([x['dc'] for x in gg]))};"
            f" since {q3(b3['SINCE'][ts, er])}; cast loop number (since / 2 SAT) {q3f(b3['SINCE'][ts, er]/(2*SAT), '.2f')}")
    g3 = G2[N_HI]; out300 = sum(x["cls"] in ("upwind", "beyond") for x in g3)
    fo = out300/ne if ne else float("nan")
    F2 = "UNREADABLE" if nw < 50 else "NOT MET" if fo >= 0.50 else "MET"
    upboth = sum(x["da"] < 0 for x in g3)
    say(f"   rows with L + 300 <= 599: {nw}/{ne}; outside the cone's along range at L + 300: {fr(out300, ne)}; upwind of both sources at L + 300 (the W1 drift signature): {fr(upboth, ne)}")
    say(f"   F2 -> {F2} (registered: NOT MET iff the fraction outside the along range at L + 300 >= 0.50; MET iff < 0.50; UNREADABLE if fewer than 50 rows have L + 300 <= 599)")
    table.append(("F2 blind-window position at L + 300", f"outside the along range {fr(out300, ne)} (upwind {sum(x['cls'] == 'upwind' for x in g3)}, beyond LMAX {sum(x['cls'] == 'beyond' for x in g3)}; inside the cone {sum(x['cls'] == 'cone' for x in g3)})",
                  "NOT MET iff >= 0.50; MET iff < 0.50", F2))
    # ---------------- F3
    say(f"\n== F3 recovery after the window opens (reading R5) ==")
    s3 = first_true(b3["NAV"] & wn(b3) & (tt >= (L + N_HI)[None, :]) & e[None, :]); d3 = np.where(s3 >= 0, s3 - (L + N_HI), -1)
    d3w = d3[within]; got = d3w >= 0; win200 = int(((d3w >= 0) & (d3w <= 200)).sum()); unc = within & (L + N_HI + 200 <= T - 1)
    f3 = win200/nw if nw else float("nan")
    F3 = "UNREADABLE" if nw < 50 else "MET" if f3 >= 0.80 else "NOT MET" if f3 < 0.50 else "INCONCLUSIVE"
    say(f"   rows {nw}; a neutral surge at or after L + 300 by 599: {fr(int(got.sum()), nw)}; surge step {q3(s3[within & (s3 >= 0)])}, delay after L + 300 {q3(d3w[got])} (p90 {pct(d3w[got], (90,))})")
    say(f"   within 200 steps of L + 300: {fr(win200, nw)} (strictly under 200: {int(((d3w >= 0) & (d3w < 200)).sum())}); uncensored subset (L + 500 <= 599): {fr(int(((d3[unc] >= 0) & (d3[unc] <= 200)).sum()), int(unc.sum()))}")
    reach = np.array([bool(b3["AT2"][s3[r]:, r, ng[r]].any()) if s3[r] >= 0 else False for r in rows])
    say(f"   of the rows that surge after L + 300, within 3.0 of the neutral source by 599: {fr(int(reach[within & (s3 >= 0)].sum()), int((within & (s3 >= 0)).sum()))}")
    say(f"   F3 -> {F3} (registered: MET iff >= 0.80 surge within 200 steps of L + 300; NOT MET iff < 0.50; INCONCLUSIVE between)")
    table.append(("F3 recovery within 200 steps of L + 300", f"{fr(win200, nw)}; any surge by 599 {fr(int(got.sum()), nw)}", "MET iff >= 0.80; NOT MET iff < 0.50", F3))
    # ---------------- F4
    say(f"\n== F4 the T1 twins' next valued whiff after L (reading R6) ==")
    Lp = first_true(vt & (tt > L[None, :])); d4 = np.where(Lp >= 0, Lp - L, -1)[er]; has = d4 >= 0
    assert np.array_equal(Lp[er], Fr[er]), "L' != F_r"
    k200 = int(((d4 >= 0) & (d4 <= 200)).sum()); f4 = k200/ne
    med_all = float(np.median(np.where(has, d4, 10**9))); med_has = float(np.median(d4[has])) if has.any() else float("nan")
    F4 = "NOT MET" if (f4 >= 0.80 and med_all < 100) else "MET" if f4 <= 0.50 else "INCONCLUSIVE"
    say(f"   twins with a valued whiff after L by 599: {fr(int(has.sum()), ne)}; delay L' - L quartiles/p90 {pct(d4[has])} (min {d4[has].min() if has.any() else 'n/a'}, max {d4[has].max() if has.any() else 'n/a'})")
    say(f"   delay <= 200: {fr(k200, ne)}; median over all eligible rows ('never' ranked last) {'never' if med_all >= 10**9 else f'{med_all:.1f}'}; median among twins that whiff {med_has:.1f};"
        f" delay <= 100 {int(((d4 >= 0) & (d4 <= 100)).sum())}, 101-200 {int(((d4 > 100) & (d4 <= 200)).sum())}, 201-300 {int(((d4 > 200) & (d4 <= 300)).sum())}, > 300 {int((d4 > 300).sum())}")
    nv = ~has; Ln = L[er][nv]
    say(f"   twins that never whiff the valued odour again by 599: {int(nv.sum())}; their L {q3(Ln)}; their censoring bound 599 - L {q3(T - 1 - Ln)} (every such delay exceeds it)")
    say(f"   F4 -> {F4} (registered: NOT MET iff the fraction <= 200 is >= 0.80 AND the median < 100; MET iff the fraction <= 0.50; INCONCLUSIVE between)")
    table.append(("F4 twins' next valued whiff", f"<= 200 steps {fr(k200, ne)}; median {'never' if med_all >= 10**9 else f'{med_all:.1f}'} (among whiffing twins {med_has:.1f})", "NOT MET iff >= 0.80 and median < 100; MET iff <= 0.50", F4))
    # ---------------- F5
    say(f"\n== F5 Agent17 measurement arm (Agent14N2 with N_hi {N17}, counter start {N17 - P_PRIOR}; reading R7) ==")
    r17 = {w: n2(w, BS, N_hi=N17) for w in ("T1", "W1", "T3a", "T3b")}; rn2 = {"T1": b1, "T3b": b3, "W1": n2("W1", BS), "T3a": n2("T3a", BS)}
    idw = {}
    for w in ("W1", "T3a"):
        a_, b_ = r17[w], rn2[w]; gg = a_["good"]
        c_ok = bool(np.array_equal(a_["C2"][:, rows, gg], b_["C2"][:, rows, gg] - (N_HI - N17)))
        idw[w] = ph24.bitwise(a_, b_, ALLK) and c_ok
        say(f"   {w}: Agent17 == Agent14N2 on ph28.ALLK (PRES included) {ph24.bitwise(a_, b_, ALLK)}; valued counter exactly {N_HI - N17} lower on every (row, step) {c_ok}")
    V17, N17_, Z17 = majority(r17["T1"]); Vn, Nn, Zn = majority(b1)
    _, dp, dlo, dhi = interval("DP", V17.astype(float), Vn.astype(float)); disc = int((V17 != Vn).sum())
    dep = ~ph28.roweq(r17["T1"], b1, BEHK); fdep = first_true(~ph23.eqmask(r17["T1"], b1))
    F5 = "MET" if -0.03 <= dp <= 0.01 else "NOT MET" if (dp < -0.05 or dp > 0.02) else "INCONCLUSIVE"
    say(f"   T1: Agent17 V {int(V17.sum())} N {int(N17_.sum())} tie {int(Z17.sum())}; Agent14N2 V {int(Vn.sum())} N {int(Nn.sum())} tie {int(Zn.sum())}; paired DP P(V) Agent17 - Agent14N2"
        f" {dp:+.4f} [{dlo:+.4f}, {dhi:+.4f}] (bootstrap 5000, H26's bootstrap seed); into V {int((V17 & ~Vn).sum())}, out of V {int((~V17 & Vn).sum())}, discordant {disc}")
    say(f"   T1: rows departing from Agent14N2 (ph28 reading R4 fields) {int(dep.sum())}, first departure step {q3(fdep[dep])}; `differs8` rows Agent17 {int(first_true(r17['T1']['DIFF8']).__ge__(0).sum())},"
        f" Agent14N2 {int(first_true(b1['DIFF8']).__ge__(0).sum())}; lost rows (no whiff in the last third) {int(ph25.lost_t1(r17['T1']).sum())} vs {int(ph25.lost_t1(b1).sum())};"
        f" wall contacts per row {r17['T1']['contacts'].mean():.3f} vs {b1['contacts'].mean():.3f}")
    say(f"   F5 -> {F5} (registered: MET iff the T1 DP point estimate is within [-0.03, +0.01]; NOT MET iff outside [-0.05, +0.02]; INCONCLUSIVE between)")
    fl, ce = ph28.run("T3b", Agent10, V10, BS), ph28.run("T3b", None, V10, BS, fixed="valued-then-neutral")
    arms = {W: (b3 if W == N_HI else r17["T3b"] if W == N17 else n2("T3b", BS, N_hi=W)) for W in WINS}
    D = {W: t3_dwell(arms[W], 400, T) for W in WINS}; Df, Dc = t3_dwell(fl, 400, T), t3_dwell(ce, 400, T)
    gain = D[N17] - D[N_HI]; _, gm, glo, ghi = interval("DP", D[N17], D[N_HI])
    R17, R17lo, R17hi = ratio_boot(D[N17], Df, Dc); Rn, Rnlo, Rnhi = ratio_boot(D[N_HI], Df, Dc); Rb, Rblo, Rbhi = ratio_boot(D[N17], D[N_HI], D[60])
    a60same = ph24.bitwise(arms[60], a60, ALLK)
    w17 = lost300(r17["T3b"], W=N17); e17 = w17["elig"]
    say(f"   T3b (the first direct measurement of the window; no bar): neutral dwell 400-599 Agent17 {D[N17].mean():.3f} (quartiles {q3f(D[N17])}), Agent14N2 {D[N_HI].mean():.3f}"
        f" (quartiles {q3f(D[N_HI])}); paired gain {gain.mean():+.3f} [{glo:+.3f}, {ghi:+.3f}] (bootstrap), paired sd {gain.std():.3f}; rows gaining {int((gain > 0).sum())}, losing {int((gain < 0).sum())}, equal {int((gain == 0).sum())}")
    say(f"   T3b R (floor Agent10 {Df.mean():.3f}, ceiling Agent5 valued then neutral {Dc.mean():.3f}): Agent17 {R17:.4f} [{R17lo:.4f}, {R17hi:.4f}], Agent14N2 {Rn:.4f} [{Rnlo:.4f}, {Rnhi:.4f}];"
        f" R_b = (D_17 - D_14N2) / (D_60 - D_14N2) = {Rb:.4f} [{Rblo:.4f}, {Rbhi:.4f}] (D_60 {D[60].mean():.3f}; the window-60 arm == ph28.run11 N 60 on ph28.ALLK {a60same})")
    say(f"   T3b Agent17 window exact at L + {N17} (ph28 reading R8 with {N17}): {int(w17['exact'][e17].sum())}/{int(e17.sum())}; first neutral surge after L {q3(w17['delay'][e17 & (w17['delay'] >= 0)])}"
        f" (none {int((e17 & (w17['delay'] < 0)).sum())})")
    table.append(("F5 Agent17 T1 DP P(V) vs Agent14N2", f"{dp:+.4f} [{dlo:+.4f}, {dhi:+.4f}]; W1, T3a identity {idw['W1'] and idw['T3a']}; T3b gain {gain.mean():+.3f} [{glo:+.3f}, {ghi:+.3f}]",
                  "MET iff in [-0.03, +0.01]; NOT MET iff outside [-0.05, +0.02]", F5))
    # ---------------- F6
    say(f"\n== F6 own-state signature at the loss (reading R8) ==")
    B3, B1 = bursts(wv(b3)), bursts(vt)
    A0 = [state(b3, B3, int(L[r]), r) for r in er]; A48 = [state(b3, B3, int(L[r]) + 48, r) for r in er]
    sil = []
    for r in rows:
        s = np.flatnonzero(vt[:, r])
        for i, s0 in enumerate(s):
            ln = (s[i + 1] - s0 - 1) if i + 1 < len(s) else (T - 1 - s0)
            if ln >= LONG: sil.append((int(r), int(s0), int(ln)))
    B0 = [state(b1, B1, s0, r) for r, s0, _ in sil]; B48 = [state(b1, B1, s0 + 48, r) for r, s0, _ in sil]
    say(f"   population A: T3b eligible rows {ne} (at L and L + 48); population B: Agent14N2 T1 valued silences reaching >= {LONG} steps: {len(sil)} silences in"
        f" {len(set(r for r, _, _ in sil))} rows; their start step {q3(np.array([s for _, s, _ in sil]))}, length {q3(np.array([x for _, _, x in sil]))}; starting before t0 {sum(s < T0 for _, s, _ in sil)}")
    pairs = [(i, r) for i, r in enumerate(er) if (r, int(L[r])) in {(a, b) for a, b, _ in sil}]
    same = sum(all(A0[i][q] == state(b1, B1, int(L[r]), r)[q] and A48[i][q] == state(b1, B1, int(L[r]) + 48, r)[q] for q in QK) for i, r in pairs)
    sameL = sum(all(A0[i][q] == state(b1, B1, int(L[r]), r)[q] for q in QK) for i, r in enumerate(er))
    say(f"   per-pair identity: every eligible T3b row's state at L equals its T1 twin's {sameL}/{ne}; pairs whose twin silence from L is itself >= {LONG} (in both populations):"
        f" {len(pairs)}, identical at L and L + 48 {same}/{len(pairs)}")
    s80s, b65s, rowsq = [], [], []
    for tag, PA_, PB_ in (("L", A0, B0), ("+48", A48, B48)):
        for q in QK:
            a_, b_ = [x[q] for x in PA_], [x[q] for x in PB_]; best, s80, b65 = best_cut(a_, b_)
            if s80: s80s.append((f"{QN[q]} at {tag}", s80))
            if b65: b65s.append((f"{QN[q]} at {tag}", b65))
            say(f"   [{tag}] {QN[q]}: A {summ(a_)}; B {summ(b_)}; best cut {best[0]}: A {best[1]:.3f}, B {best[2]:.3f}"
                f"{'; separates >= 0.80 vs <= 0.20' if s80 else ''}{'' if s80 or not b65 else '; better than 0.65 vs 0.35'}")
    F6 = "NOT MET" if s80s else "MET" if not b65s else "INCONCLUSIVE"
    say(f"   quantities separating at >= 0.80 vs <= 0.20: {[(k, z[0], round(z[1], 3), round(z[2], 3)) for k, z in s80s] or 'none'}; better than 0.65 vs 0.35 (first cut each):"
        f" {[(k, z[0], round(z[1], 3), round(z[2], 3)) for k, z in b65s] or 'none'}")
    say(f"   F6 -> {F6} (registered: NOT MET iff some single own-state quantity separates at >= 0.80 vs <= 0.20; MET iff none does better than 0.65 vs 0.35; INCONCLUSIVE between)")
    top = s80s[0] if s80s else b65s[0] if b65s else None
    table.append(("F6 own-state signature, T3b losses vs T1 long silences", (f"{top[0]} {top[1][0]}: A {top[1][1]:.3f}, B {top[1][2]:.3f}" if top else "no cut better than 0.65 vs 0.35")
                  + f"; {len(s80s)} quantity-cuts >= 0.80 vs <= 0.20, {len(b65s)} better than 0.65 vs 0.35", "NOT MET iff >= 0.80 vs <= 0.20; MET iff none better than 0.65 vs 0.35", F6))
    # ---------------- the (t) profile and the reported quantities
    say(f"\n== (t) profile, T3b, eligible rows {ne} (reading R9; no threshold) ==")
    for W in WINS:
        rs = first_true(wn(b3) & (tt >= (L + W)[None, :]) & e[None, :]); o = arms[W]
        ms = first_true(o["NAV"] & wn(o) & (tt > L[None, :]) & e[None, :])
        agree = int((rs[er] == ms[er]).sum())
        eqb = sum(bool(all(np.array_equal(o[k][:(rs[r] if rs[r] >= 0 else T), r], b3[k][:(rs[r] if rs[r] >= 0 else T), r]) for k in ("POS", "HEAD", "NAV", "SINCE", "H"))) for r in er)
        say(f"   window {W}: re-scored first neutral surge delay after L {q3(rs[er][rs[er] >= 0] - L[er][rs[er] >= 0])} (none before 600 {int((rs[er] < 0).sum())}); measured arm"
            f" ({'Agent14N2 itself' if W == N_HI else 'Agent17' if W == N17 else f'Agent14N2 at N_hi {W}'}) {q3(ms[er][ms[er] >= 0] - L[er][ms[er] >= 0])} (none {int((ms[er] < 0).sum())});"
            f" rows where they agree {agree}/{ne}; rows equal to Agent14N2 before the re-scored step {eqb}/{ne}; T3b dwell 400-599 {D[W].mean():.3f}")
    Ct = b3["C"]; blind = (tt > L[None, :]) & (tt < (L + N_HI)[None, :]) & e[None, :]
    say(f"   wall contacts in T3b (Agent14N2): per row {b3['contacts'].mean():.3f}; rows with any {int((b3['contacts'] > 0).sum())}; in the blind window L+1..L+299 {int((Ct & blind).sum())}"
        f" in {int((Ct & blind).any(0).sum())} rows; from L + 300 {int((Ct & (tt >= (L + N_HI)[None, :]) & e[None, :]).sum())}; Agent17 per row {r17['T3b']['contacts'].mean():.3f}")
    say(f"   upwind of both sources at L + 300: {fr(upboth, ne)}; at L + 200 {fr(sum(x['da'] < 0 for x in G2[200]), ne)}; at L + 100 {fr(sum(x['da'] < 0 for x in G2[100]), ne)}")
    say(f"   never steer on the neutral odour by 600 (bench): {int((e & (dl['delay'] < 0)).sum())}/{ne} (the evaluation's 173/379 reproduced above)")
    return table


def seed_check(texts):
    """no seed constant of the imported scripts (and their derived numbers) appears in this file or its output; the numbers are read, not written"""
    import re
    nums = set()
    for m in (ph22, ph24, ph25, ph28, ph30):
        for name in ("SEEDS", "BENCH", "REPRO"):
            v = getattr(m, name, None)
            stack = [v]
            while stack:
                x = stack.pop()
                if isinstance(x, dict): stack += list(x.values())
                elif isinstance(x, (tuple, list)): stack += list(x)
                elif isinstance(x, int) and x >= 1000: nums |= {x, x + 10_000, x + 20_000, x + 10_000_000, x + 20_000_000}
    nums |= {_STATS26[3], ph15.BOOT_SEED}
    pat = re.compile(r"(?<!\d)(" + "|".join(map(str, sorted(nums))) + r")(?!\d)")
    return [i for i, t in enumerate(texts) if pat.search(t)], len(nums)


def main():
    say("== T3b diagnosis (ph34b.py, measurement only; decision:t3b-diagnosis; H29 design v1 DRAFT section 12 point 1) ==")
    say(f"   ph34b.py sha256 {sha()}")
    say("   imported: " + "; ".join(f"{os.path.basename(m.__file__)} {sha(m.__file__)}" for m in MODS))
    pre = {k: sha(os.path.join(HERE, k + ".py"))[:8] == v for k, v in PREFIX.items()}
    say(f"   sha256 prefixes equal to those H29 design v1 cites (ph11, ph12, ph22, ph23, ph24, ph25b, ph28, ph30): {all(pre.values())} {'' if all(pre.values()) else pre}")
    say(f"   reproduced files: experiments/h26/ph28_bench.txt {sha(BENCH_TXT)}; experiments/h26/ph28_eval.txt {sha(EVAL_TXT)}; design experiments/h29/h29_design_v1.md {sha(DESIGN29)}")
    say("   seeds: H26's bench seeds (ph28.BS) and bootstrap seed (set by ph28's import) reused on purpose; H26's evaluation seeds (ph28.SEEDS['eval']) for the reproduction only;"
        " digits not printed; no H29 seed; seed-scan exclusion pair by reference only (experiments/h20/ph31_eval.txt, decision:seed-scan-exclusion-ph31-eval)")
    say(f"   statistics: 95 percent (Z {ph15.Z}), bootstrap 5000; P {P_PRIOR}, N_hi {N_HI} (adopted), Agent17 N_hi {N17}; t0 {T0}; SAT {SAT:.4f}; {R} rows x {T} steps")
    say("   readings (file header): R1 Agent14N2 via a ph24.make hook (as ph30's i5_check), (P, N_hi) from ph28.pn; R2 L = last valued whiff before t0 (masked from t0); R3 F1 every"
        " recorded per-step array on 0..F_r-1; R4 sensed position, relative to the neutral source, along range 0 < d_along < 25, wall within 1.0; R5 F3 within 200 = s - (L+300) <= 200,"
        " censored rows count as not within; R6 F4 L' = F_r, 'never' not within and ranked last for the median; R7 F5 DP via ph16.interval, R floor Agent10 ceiling Agent5"
        " valued-then-neutral, R_b vs the window-60 arm; R8 F6 burst = whiff + >= 2 whiffs on t-9..t-1, cuts q <= c / q > c, categories and complements; R9 (t) re-scored and measured")
    if not all(pre.values()):
        say("== an imported file differs from the version H29 design v1 cites: nothing measured =="); return 1
    ok, runs = reproduce()
    table = []
    if ok:
        table = measure(runs["b3"], runs["b1"], runs["a60"])
        say("\n== the six registered falsification readings (decision:t3b-diagnosis; thresholds registered before this run) ==")
        say("| criterion | measured | registered threshold | reading |")
        say("|---|---|---|---|")
        for c, m, t, v in table: say(f"| {c} | {m} | {t} | {v} |")
    hits, nn = seed_check([open(__file__, encoding="utf-8").read()] + _lines)
    say(f"   seed self-check: none of {nn} seed numbers of the imported scripts (ph22, ph24, ph25, ph28, ph30 SEEDS / BENCH / REPRO, derived, bootstrap) appears in this file or its output: {not hits}")
    with open(OUT, "w", encoding="utf-8", newline="\n") as f: f.write("\n".join(_lines) + "\n")
    return 0 if ok and not hits else 2


if __name__ == "__main__":
    sys.exit(main())
