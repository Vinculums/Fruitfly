#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H17 post-bench diagnosis (measurement only; owner 2026-09-24, '3번 진단 먼저 진행해', decision:h17-post-bench-diagnosis).

Usage: python ph26b.py      (writes experiments/h17/ph26b_diag.txt, LF line ends)

ph26.py (sha256 checked below, must equal the bench's), design v2 FINAL and the bench verdict (B FAIL, no candidate on part (d),
record:h17-bench-result) are untouched: the Search rule, S, gamma, L0, U1, every bar and every adopted module are imported as
they are; no rule is changed, no agent variant is added, no S is swept. Bench seeds only (ph26.BS and ph26's bootstrap seed,
not written out here, so ph26's seed self-check stays valid); the development and evaluation seeds are not used.

Reproduction first: ph26.bench is re-run in this process and its output must equal experiments/h17/ph26_bench.txt line for line
(the file's sha256 is checked first); then the four T1 runs measured here (World7 +1/0 and +1/-1, Agent12 and Agent10, through
ph26.run) must reproduce the bench's (d), (h1) and (h2) lines character for character. On any mismatch nothing is measured.

(A) the (d) silences, World7 +1/0, Agent10 (Agent12 alongside): the longest any-odour silence per row; every row whose silence
    reaches q >= S: where it starts and ends, what preceded it (last whiff, the hold and how it ended), positions at its start and
    at the engagement step relative to both sources, walls, the cast's `since`; Agent12 in the same rows; a position-based
    classification of the silence steps (design section 2 categories); the timing against the row's dwell.
(B) the (h2) wall contacts, World7 +1/-1, Agent12 vs Agent10: every Agent12 contact (step, engaged, u, leg, slant, wall, position,
    stranded row, whiff after it, outcome) and summaries; the stranded-row decomposition and the paired transitions; P(V | contact)
    and P(lost | contact) with Wilson intervals.
Positions are the position a step's sense used (the position after the previous step's move; the start for step 0), as ph24c.rel.
Names no cause beyond what is measured; tests no change.
"""
import sys, os, hashlib, math
import numpy as np
import ph26                                      # sets ph15's bootstrap seed and the 95 percent level, as the bench did
import ph9, ph11, ph12b, ph13, ph15, ph16, ph18, ph19, ph21, ph22, ph24, ph24b, ph24c
from ph26 import Agent12, Agent10, run, qrec, lost, cls3, BS, S_ON, leg_of, slant_of, pp_dp, pp_prop, fmt_ci, row_identity
from ph16 import interval, CELLS
from ph18 import majority
from ph21 import q3, first_true
from ph24 import events, on_hold, q3f
from ph24c import released, cone_geom
from ph12b import ARENA2
from ph9 import LMAX, LAM

PH26_SHA = "1c9b6f5b6e3f0341e60c707cd577d748292ecdb720062ecada33336101e167cf"
BENCH_TXT_SHA = "ec9df782aa429492462849c9577e853bade96eefd18917626ee9a08e9643ff6d"
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
BENCH_TXT = os.path.join(REPO, "experiments", "h17", "ph26_bench.txt"); OUT = os.path.join(REPO, "experiments", "h17", "ph26b_diag.txt")
WALL_NEAR = 1.0                                  # 'at a wall' = within 1.0 of a wall (ph12b's wall-time convention)
P_HIT = 0.3                                      # World2's p_hit (ph11), the cone's whiff probability at d_along 0
N = 400


def sha(p=__file__): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def frac(k, n): return f"{k}/{n} = {k / n:.3f}" if n else f"{k}/0"
def wil(k, n):
    if n == 0: return f"{k}/0"
    p, lo, hi = ph15.wilson(k, n); return f"{k}/{n} = {p:.3f} [{lo:.3f}, {hi:.3f}]"


_lines = []
def say(s=""): _lines.append(s); print(s, flush=True)


# ------------------------------------------------------------------ geometry
def sensed(o, t, r):
    return o["POS"][t - 1, r] if t > 0 else o["start"][r]


def geo(o, t, r):
    """the position step t sensed at, relative to both sources. d_along = x - x_src (downwind > 0; the sources share x);
    d_cross signed outward: + = on the far side of that source's axis from the other source."""
    p = sensed(o, t, r); g = o["good"][r]; out = {}
    for lab, k in (("val", g), ("oth", 1 - g)):
        s = o["src"][r, k]; so = o["src"][r, 1 - k]; da = p[0] - s[0]; dc = p[1] - s[1]; sg = np.sign(s[1] - so[1])
        ins, dist = cone_geom(np.array(da), np.array(dc)); out[lab] = (float(da), float(dc*sg), bool(ins), float(dist))
    wall = min(p[0], ARENA2 - p[0], p[1], ARENA2 - p[1])
    out["wall"] = float(wall); out["pos"] = p
    return out


def pclass(g):
    """design section 2 categories, position only, mutually exclusive in this order: (iv) at a wall (within 1.0); (v) inside a whiff
    region (no whiff drawn); (i) upwind of both sources (d_along < 0); (ii) beyond LMAX downwind (d_along >= 25); (iii) crosswind
    outside both cones (0 <= d_along < 25). The partition leaves no step for (vi); (vi) is used for silences with no majority class."""
    if g["wall"] < WALL_NEAR: return "iv"
    if g["val"][2] or g["oth"][2]: return "v"
    da = g["val"][0]
    if da < 0: return "i"
    if da >= LMAX: return "ii"
    return "iii"


CLS_NAMES = {"i": "(i) upwind of both sources", "ii": "(ii) beyond LMAX 25 downwind", "iii": "(iii) crosswind outside both cones (0 <= d_along < 25)",
             "iv": "(iv) at a wall (within 1.0)", "v": "(v) inside a whiff region, no whiff drawn", "vi": "(vi) other: no class holds at least half the steps"}


def fmt_geo(g):
    v, n = g["val"], g["oth"]
    return (f"d_along {v[0]:+.1f}; d_cross valued axis {v[1]:+.1f}, other axis {n[1]:+.1f} (outward +); inside valued/other region {int(v[2])}/{int(n[2])};"
            f" distance to the nearest region {min(v[3], n[3]):.1f}; nearest wall {g['wall']:.1f}")


# ------------------------------------------------------------------ holds
def segments(o, r):
    """hold segments of row r: (odour, first step held, end step = first step not holding it or -1, kind). kind: 'evidence release' if the
    evidence flag is on the end step, 'H25 timeout drive' if the timeout flag is on it or a sustain was on the step before, else 'other'."""
    H = o["H"][:, r]; T_ = len(H); out = []; t = 0; prev = int(o["H0"][r])
    if prev >= 0 and H[0] == prev: pass
    while t < T_:
        if H[t] < 0: t += 1; continue
        k = int(H[t]); s = t
        while t < T_ and H[t] == k: t += 1
        e = t if t < T_ else -1
        kind = "open at the run's end" if e < 0 else "evidence release" if o["EV"][e, r] else "H25 timeout drive" if (o["TO"][e, r] or o["SUS"][e - 1, r]) else "other"
        out.append((k, s, e, kind))
    return out


def odour(o, r, k): return "valued" if k == o["good"][r] else "other"


def whiff_lab(o, t, r):
    w = o["W"][t, r]; g = o["good"][r]
    return "both" if w.all() else "valued" if w[g] else "other" if w[1 - g] else "none"


def outcome(o):
    V, Nn, Z = majority(o); return np.where(V, "V", np.where(Nn, "N", "tie"))


# ------------------------------------------------------------------ dry-spell reference arithmetic
def p_no_run(n, L, p):
    """P(no run of >= L consecutive no-whiff steps in n steps at whiff probability p), exact recursion A_k = A_{k-1} - p f^L A_{k-L-1}"""
    f = 1.0 - p; fl = f**L
    if L > n: return 1.0
    A = np.ones(n + 1); A[L] = 1.0 - fl
    for k in range(L + 1, n + 1): A[k] = A[k - 1] - p*fl*A[k - L - 1]
    return float(A[n])


def e_longest(n, p): return sum(1.0 - p_no_run(n, L, p) for L in range(1, n + 1))


# ------------------------------------------------------------------ reproduction
def reproduce():
    say("\n== (0) reproduction (nothing is measured unless every check holds) ==")
    ok_sha = sha(ph26.__file__) == PH26_SHA; ok_txt = sha(BENCH_TXT) == BENCH_TXT_SHA
    say(f"   ph26.py sha256 equals the bench's ({PH26_SHA[:8]}...{PH26_SHA[-4:]}): {ok_sha}; ph26_bench.txt sha256 equals the recorded ({BENCH_TXT_SHA[:8]}...{BENCH_TXT_SHA[-4:]}): {ok_txt}")
    if not (ok_sha and ok_txt): return None
    want = open(BENCH_TXT, encoding="utf-8").read().split("\n")
    if want and want[-1] == "": want = want[:-1]
    got = []; ph26.bench(say=got.append)
    same = got == want; diff = [i + 1 for i in range(max(len(got), len(want))) if i >= len(got) or i >= len(want) or got[i] != want[i]]
    say(f"   ph26.bench re-run in this process ({len(got)} lines) equals ph26_bench.txt ({len(want)} lines) line for line: {same}" + ("" if same else f"; differing line numbers {diff[:20]}"))
    if not same: return None
    # the four runs measured here, through ph26.run on the bench seeds; the bench's (d), (h1), (h2) lines recomputed from them
    T1 = {(k, v): run("T1", c, v, BS) for v in ((1.0, 0.0), (1.0, -1.0)) for k, c in (("Agent12", Agent12), ("Agent10", Agent10))}
    mine = []
    for lab, o in (("World7 +1/0 Agent10", T1[("Agent10", (1.0, 0.0))]), ("World7 +1/-1 Agent10", T1[("Agent10", (1.0, -1.0))])):
        Q = qrec(o["W"]); mx = Q.max(0)
        mine.append(f"   [{lab}] longest any-odour silence per row: quartiles {q3(mx)}, p90 {np.percentile(mx, 90):.0f}, max {mx.max():.0f}; rows reaching q >= {S_ON} {int((mx >= S_ON).sum())};"
                    f" fraction of (row, step) with q >= 150/180/210/250: " + "/".join(f"{(Q >= c).mean():.5f}" for c in (150, 180, 210, 250)))
    for lab, v in (("+1/0", (1.0, 0.0)), ("+1/-1", (1.0, -1.0))):
        o = T1[("Agent12", v)]; er = o["ENG"].any(0); k_, pt, lo, hi = interval("P", er)
        mine.append(f"   [World7 {lab} Agent12] rows with any engaged step {fmt_ci(k_, N, pt, lo, hi)}; engaged (row, step) {int(o['ENG'].sum())}; first engaged step {q3(first_true(o['ENG'])[er])}"
                    + (f" -> bar upper bound <= 0.05: {'PASS' if hi <= 0.05 else 'FAIL'} (pass probability at the point, section 7: {pp_prop(pt, 0.05, True):.4f})" if v == (1.0, 0.0) else " (reported)"))
    o12, o10 = T1[("Agent12", (1.0, 0.0))], T1[("Agent10", (1.0, 0.0))]; V12, V10 = majority(o12)[0], majority(o10)[0]; c12, c10 = cls3(o12), cls3(o10)
    P1, dp1, b1, sd1, P1m = pp_dp(V12, V10, -0.05, False); _, _, blo, bhi = interval("DP", V12.astype(float), V10.astype(float))
    e_ = o12["ENG"].any(0); l12, l10 = lost(o12), lost(o10)
    mine.append(f"(h1) T1 on bench seeds, World7 +1/0 {N} x 600: " + "; ".join(f"{k} V {int(majority(o)[0].sum())} N {int(majority(o)[1].sum())} tie {int(majority(o)[2].sum())} P(V) "
                f"{interval('P', majority(o)[0])[1]:.3f} [{interval('P', majority(o)[0])[2]:.3f}, {interval('P', majority(o)[0])[3]:.3f}]" for k, o in (("Agent12", o12), ("Agent10", o10))))
    mine.append(f"   (h1) paired DP P(V) Agent12 - Agent10 {dp1:+.4f} [{blo:+.4f}, {bhi:+.4f}] (bootstrap 5000, seed {ph15.BOOT_SEED}); engaged rows {int(e_.sum())}; into V {int(((c12 == 0) & (c10 != 0)).sum())},"
                f" out of V {int(((c12 != 0) & (c10 == 0)).sum())}; V among engaged rows Agent12 {int(V12[e_].sum())} vs Agent10 {int(V10[e_].sum())}; lost rows {int(l12.sum())} vs {int(l10.sum())};"
                f" contacts per row {o12['contacts'].mean():.3f} vs {o10['contacts'].mean():.3f}")
    o12, o10 = T1[("Agent12", (1.0, -1.0))], T1[("Agent10", (1.0, -1.0))]; V12, V10 = majority(o12)[0], majority(o10)[0]; l12, l10 = lost(o12), lost(o10)
    P2, dp2, b2, sd2, P2m = pp_dp(l12, l10, -0.05, True); _, _, llo, lhi = interval("DP", l12.astype(float), l10.astype(float))
    Pb, dpv, bv, sdv, Pbm = pp_dp(V12, V10, -0.02, False); _, _, vlo, vhi = interval("DP", V12.astype(float), V10.astype(float))
    cm = o12["contacts"].mean(); e_ = o12["ENG"].any(0)
    _, r10, _ = released(o10); _, r12, _ = released(o12); s10, s12 = np.unique(r10), np.unique(r12)
    mine.append(f"(h2) T3 on bench seeds, World7 +1/-1 {N} x 600: " + "; ".join(f"{k} V {int(majority(o)[0].sum())} N {int(majority(o)[1].sum())} tie {int(majority(o)[2].sum())},"
                f" lost rows {int(lost(o).sum())}, contacts per row {o['contacts'].mean():.3f}" for k, o in (("Agent12", o12), ("Agent10", o10))))
    mine.append(f"   (h2) stranded rows (a drive-ended negative hold, as R3): Agent10 {len(s10)} (releases {len(r10)}), Agent12 {len(s12)}; Agent12 engaged rows {int(e_.sum())}, engaged (row, step) {int(o12['ENG'].sum())};"
                f" lost among Agent10's stranded rows: Agent10 {int(l10[s10].sum())}, Agent12 {int(l12[s10].sum())}")
    mine.append(f"   (h2) lost-row paired DP Agent12 - Agent10 {dp2:+.4f} [{llo:+.4f}, {lhi:+.4f}]; P(V) paired DP {dpv:+.4f} [{vlo:+.4f}, {vhi:+.4f}]; contacts per row {cm:.3f}")
    hit = [m in want for m in mine]
    say(f"   the four runs measured below (ph26.run, World7 +1/0 and +1/-1, Agent12 and Agent10, bench seeds, {N} x 600): the bench's (d) gap lines (+1/0, +1/-1), (d) engaged-row lines (+1/0, +1/-1),"
        f" (h1) two lines and (h2) three lines recomputed from them are each present verbatim in ph26_bench.txt: {hit} -> {all(hit)}")
    for m in mine: say("      " + m.strip().replace(str(ph15.BOOT_SEED), "<ph26's bootstrap seed>"))
    ok_id = all(row_identity(T1[("Agent12", v)], T1[("Agent10", v)])[0] for v in ((1.0, 0.0), (1.0, -1.0)))
    say(f"   never-engaged rows bitwise Agent10 and engaged rows equal before their first engaged step, both value pairs (bench (a2)): {ok_id}")
    return T1 if all(hit) and ok_id else None


# ------------------------------------------------------------------ (A)
def part_a(o10, o12):
    say("\n== (A) the bench (d) silences: World7 +1/0, 400 x 600, Agent10 (Agent12 alongside); q = steps since the last whiff of either odour (ph26.qrec) ==")
    say("\n(A1) longest any-odour silence per row (descriptive; no S is chosen from it)")
    Q10, Q12 = qrec(o10["W"]), qrec(o12["W"]); rows_tab = {}
    for lab, Q in (("Agent10", Q10), ("Agent12", Q12)):
        mx = Q.max(0); rows_tab[lab] = mx
        say(f"   [{lab}] quartiles {q3(mx)}, p90 {np.percentile(mx, 90):.0f}, p95 {np.percentile(mx, 95):.0f}, p99 {np.percentile(mx, 99):.0f}, max {mx.max():.0f}; mean {mx.mean():.1f}")
        say(f"   [{lab}] rows with a silence >= c:  " + "; ".join(f"{c}: {int((mx >= c).sum())} ({(mx >= c).mean():.4f})" for c in (120, 150, 180, 193, 200, 210, 220, 230, 240, 250, 260, 280, 300, 350, 400, 500)))
        say(f"   [{lab}] fraction of (row, step) with q >= c:  " + "; ".join(f"{c}: {(Q >= c).mean():.5f}" for c in (150, 180, 210, 250, 300, 350)))
    say("   reference arithmetic (not measured): the Wilson 95 percent upper bound of k rows of 400 (the (d) bar is an upper bound <= 0.05): "
        + "; ".join(f"{k}: {ph15.wilson(k, N)[2]:.4f}" for k in range(6, 21)))
    ne = ~o12["ENG"].any(0)
    say(f"   the two arms' longest silences are equal in the {int(ne.sum())} never-engaged rows: {bool((rows_tab['Agent10'][ne] == rows_tab['Agent12'][ne]).all())};"
        f" differing rows {int((rows_tab['Agent10'] != rows_tab['Agent12']).sum())} (all engaged rows)")
    hist = np.histogram(rows_tab["Agent10"], bins=[0, 100, 120, 140, 150, 160, 170, 180, 190, 200, 210, 250, 300, 350, 601])
    say("   [Agent10] histogram of the longest silence per row: " + "; ".join(f"[{int(a)}, {int(b)}) {int(c)}" for a, b, c in zip(hist[1][:-1], hist[1][1:], hist[0])))
    # where the ordinary long silences sit: rows 150-209 for reference
    mx = rows_tab["Agent10"]; rows = np.flatnonzero(mx >= S_ON); rows12 = np.flatnonzero(o12["ENG"].any(0))
    say(f"\n(A2) the rows whose Agent10 silence reaches q >= {S_ON}: {len(rows)} rows {rows.tolist()}; Agent12's engaged rows {rows12.tolist()}; the same set: {rows.tolist() == rows12.tolist()}")
    g = o10["good"]; cls10, cls12 = outcome(o10), outcome(o12); AT = o10["AT2"]; rr_all = np.arange(N)
    recs = []
    for r in rows:
        t210 = int(np.argmax(Q10[:, r] >= S_ON)); s = t210 - (S_ON - 1); lw = s - 1
        after = np.flatnonzero(o10["W"][t210:, r].any(1)); end = t210 + int(after[0]) if len(after) else 600
        segs = segments(o10, r); held_lw = int(o10["H"][lw, r]) if lw >= 0 else -1; held_s = int(o10["H"][s, r])
        if held_lw >= 0:
            seg = [x for x in segs if x[1] <= lw and (x[2] > lw or x[2] < 0)][0]
            hold_txt = f"held {odour(o10, r, seg[0])} at the last whiff (formed {seg[1]}), ended at step {seg[2]} by {seg[3]} ({seg[2] - lw if seg[2] >= 0 else -1} steps after the last whiff)"
            hk = seg[3]
        else:
            prevs = [x for x in segs if 0 <= x[2] <= lw]
            hold_txt = "nothing held at the last whiff" + (f"; the last hold before it: {odour(o10, r, prevs[-1][0])}, steps {prevs[-1][1]}-{prevs[-1][2] - 1}, ended by {prevs[-1][3]}" if prevs else "; no hold before it in the row")
            hk = "nothing held at the last whiff"
        g0, ge = geo(o10, s, r), geo(o10, t210, r)
        steps = np.arange(s, end); cl = [pclass(geo(o10, t, r)) for t in steps]; cnt = {c: cl.count(c) for c in ("i", "ii", "iii", "iv", "v")}
        share = {c: cnt[c]/len(cl) for c in cnt}; dom = max(share, key=share.get); dom = dom if share[dom] >= 0.5 else "vi"
        ins = np.array([c == "v" for c in cl]); runs_in = 0; best = 0
        for x in ins: runs_in = runs_in + 1 if x else 0; best = max(best, runs_in)
        cont = int(o10["C"][s:end, r].sum()); dmin_wall = min(geo(o10, t, r)["wall"] for t in steps)
        dv_b, dn_b = int(AT[:s, r, g[r]].sum()), int(AT[:s, r, 1 - g[r]].sum()); at_b = AT[:s, r].any(1); last_at = int(np.flatnonzero(at_b)[-1]) if at_b.any() else -1
        dv_a, dn_a = int(AT[s:, r, g[r]].sum()), int(AT[s:, r, 1 - g[r]].sum())
        fe = int(first_true(o12["ENG"][:, r:r + 1])[0]); w12 = np.flatnonzero(o12["W"][fe:, r].any(1)); tw = fe + int(w12[0]) if len(w12) else -1
        recs.append(dict(r=r, s=s, t210=t210, end=end, lw=lw, hk=hk, held_s=held_s, g0=g0, ge=ge, share=share, dom=dom, c0=pclass(g0), ce=pclass(ge), best_in=best, cont=cont,
                         dmin_wall=dmin_wall, since0=float(o10["SINCE"][s, r]), since_e=float(o10["SINCE"][t210, r]), dv_b=dv_b, dn_b=dn_b, last_at=last_at, dv_a=dv_a, dn_a=dn_a,
                         fe=fe, tw=tw, w_lab=whiff_lab(o12, tw, r) if tw >= 0 else "none", c10=cls10[r], c12=cls12[r], L=end - s, lwlab=whiff_lab(o10, lw, r) if lw >= 0 else "construction"))
        say(f"   row {r}: cell {o10['cell'][r]} ({CELLS[o10['cell'][r]]}); silence steps {s}-{end - 1} (start = the step after the last whiff at {lw}; ends {'with a whiff at ' + str(end) if end < 600 else 'at the run end, 600'});"
            f" length {end - s}; the row's longest {int(mx[r])}; q reaches {S_ON} at step {t210}")
        say(f"      last whiff (step {lw}): {recs[-1]['lwlab']}; {hold_txt}; held at the silence start: {'nothing' if held_s < 0 else odour(o10, r, held_s)}; held at step {t210}: {'nothing' if o10['H'][t210, r] < 0 else odour(o10, r, int(o10['H'][t210, r]))}")
        say(f"      at the silence start: {fmt_geo(g0)}; class {c_short(pclass(g0))}; cast `since` {o10['SINCE'][s, r]:.0f}")
        say(f"      at step {t210} (Agent12's engagement step): {fmt_geo(ge)}; class {c_short(pclass(ge))}; cast `since` {o10['SINCE'][t210, r]:.0f}")
        say(f"      over the silence (Agent10): steps by class " + ", ".join(f"({c}) {cnt[c]}" for c in ("i", "ii", "iii", "iv", "v")) + f" -> majority {c_short(dom)}; longest run inside a whiff region {best};"
            f" nearest approach to a wall {dmin_wall:.1f}, contacts {cont}")
        say(f"      dwell before the silence valued/other {dv_b}/{dn_b} (last step at a source {last_at}); after it {dv_a}/{dn_a}; outcome Agent10 {cls10[r]}, Agent12 {cls12[r]}"
            f"{' DIFFERS' if cls10[r] != cls12[r] else ''}; Agent12 engaged at step {fe}, first whiff after it {'step ' + str(tw) + ' (' + recs[-1]['w_lab'] + '), u ' + str(tw - fe) + ', leg ' + str(int(leg_of(tw - fe))) if tw >= 0 else 'none to the run end'}")
    say(f"\n(A2) summary over the {len(recs)} silences (Agent10)")
    arr = lambda k: np.array([x[k] for x in recs], float)
    say(f"   silence start step {q3(arr('s'))} (min {int(arr('s').min())}, max {int(arr('s').max())}); step q reaches {S_ON} {q3(arr('t210'))}; silence length {q3(arr('L'))} (ended by a whiff {int((arr('end') < 600).sum())},"
        f" open at the run end {int((arr('end') >= 600).sum())})")
    lw_lab = [x["lwlab"] for x in recs]
    say(f"   last whiff before the silence: valued {lw_lab.count('valued')}, other (neutral) {lw_lab.count('other')}, both {lw_lab.count('both')}, from construction {lw_lab.count('construction')}")
    hk = [x["hk"] for x in recs]
    say(f"   the hold at the last whiff: " + "; ".join(f"{k} {hk.count(k)}" for k in sorted(set(hk))) + f"; held at the silence start: nothing {sum(x['held_s'] < 0 for x in recs)},"
        f" valued {sum(x['held_s'] == g[x['r']] for x in recs)}, other {sum(x['held_s'] == 1 - g[x['r']] for x in recs)}")
    for lab, key in (("the silence start", "g0"), ("the engagement step", "ge")):
        da = np.array([x[key]["val"][0] for x in recs]); cv = np.array([x[key]["val"][1] for x in recs]); co = np.array([x[key]["oth"][1] for x in recs])
        dn = np.array([min(x[key]["val"][3], x[key]["oth"][3]) for x in recs]); ins = np.array([x[key]["val"][2] or x[key]["oth"][2] for x in recs]); wl = np.array([x[key]["wall"] for x in recs])
        say(f"   at {lab}: d_along {q3f(da)} (min {da.min():.1f}, max {da.max():.1f}); upwind of both (d_along < 0) {int((da < 0).sum())}; beyond LMAX (d_along >= 25) {int((da >= LMAX).sum())};"
            f" d_cross valued axis (outward +) {q3f(cv)}, other axis {q3f(co)}; |d_cross| to the nearer axis {q3f(np.minimum(np.abs(cv), np.abs(co)))}; inside a whiff region {int(ins.sum())};"
            f" distance to the nearest region {q3f(dn)} (max {dn.max():.1f}); nearest wall {q3f(wl)} (within {WALL_NEAR}: {int((wl < WALL_NEAR).sum())})")
    say(f"   cast `since` at the silence start equal to 1 (the last whiff was a navigation event, which resets it) {int((arr('since0') == 1).sum())}/{len(recs)}")
    say(f"   cast `since` at the silence start {q3(arr('since0'))} (min {int(arr('since0').min())}, max {int(arr('since0').max())}); at the engagement step {q3(arr('since_e'))}")
    say(f"   rows with a wall contact during the silence {sum(x['cont'] > 0 for x in recs)}; nearest approach to a wall during the silence {q3f(arr('dmin_wall'))}")
    say(f"\n(A3) Agent12 in the same rows: engagement step {q3(arr('fe'))}; equal to the step Agent10's q reaches {S_ON} in {sum(x['fe'] == x['t210'] for x in recs)}/{len(recs)};"
        f" a whiff after engagement {sum(x['tw'] >= 0 for x in recs)}/{len(recs)} (first odour valued {sum(x['w_lab'] == 'valued' for x in recs)}, other {sum(x['w_lab'] == 'other' for x in recs)},"
        f" both {sum(x['w_lab'] == 'both' for x in recs)}); u at that whiff {q3(np.array([x['tw'] - x['fe'] for x in recs if x['tw'] >= 0]))}; engaged to the run end {sum(x['tw'] < 0 for x in recs)}")
    tab = {(a, b): sum(x["c10"] == a and x["c12"] == b for x in recs) for a in ("V", "N", "tie") for b in ("V", "N", "tie")}
    say("   outcome Agent10 -> Agent12 in these rows: " + "; ".join(f"{a}->{b} {n}" for (a, b), n in tab.items() if n) + f"; Agent10 V {sum(x['c10'] == 'V' for x in recs)}, Agent12 V {sum(x['c12'] == 'V' for x in recs)}")
    dif = [x for x in recs if x["c10"] != x["c12"]]
    for x in dif:
        r = x["r"]; d10 = o10["dwell"][r]; d12 = o12["dwell"][r]
        say(f"   differing row {r}: cell {o10['cell'][r]} ({CELLS[o10['cell'][r]]}); Agent10 {x['c10']} (dwell valued/other {int(d10[g[r]])}/{int(d10[1 - g[r]])}), Agent12 {x['c12']}"
            f" (dwell {int(d12[g[r]])}/{int(d12[1 - g[r]])}); engaged at {x['fe']}, first whiff after it {x['tw']} ({x['w_lab']}); dwell before the silence {x['dv_b']}/{x['dn_b']}")
    others = np.flatnonzero(cls10 != cls12)
    say(f"   rows whose outcome differs between the arms, all 400: {others.tolist()} (never-engaged rows are bitwise equal, so any difference is in an engaged row)")
    say(f"\n(A4) position-based classification of the {len(recs)} silences (design section 2 categories; position only, no cause):")
    for key, lab in (("dom", "majority class over the silence's steps (a class holding at least half of them; else (vi))"), ("c0", "class at the silence start"), ("ce", "class at the engagement step")):
        v = [x[key] for x in recs]
        say(f"   {lab}: " + "; ".join(f"{CLS_NAMES[c]} {v.count(c)}" for c in ("i", "ii", "iii", "iv", "v", "vi")))
    tot = {c: sum(x["share"][c]*x["L"] for x in recs) for c in ("i", "ii", "iii", "iv", "v")}; T_ = sum(tot.values())
    say(f"   pooled silence steps {int(T_)}: " + "; ".join(f"({c}) {int(round(tot[c]))} ({tot[c]/T_:.3f})" for c in ("i", "ii", "iii", "iv", "v")))
    say(f"   longest run of consecutive steps inside a whiff region without a whiff, per silence: {q3(arr('best_in'))} (max {int(arr('best_in').max())})")
    say("   reference arithmetic (not measured): a stay inside the cone at fixed d_along, whiff probability p = 0.3 exp(-d_along / 12) per step:")
    for d in (0.0, 5.0, 10.0, 15.0, 20.0, 24.0):
        p = P_HIT*math.exp(-d/LAM)
        say(f"      d_along {d:4.1f}: p {p:.4f}; P(210 steps without a whiff) = (1 - p)^210 = {(1 - p)**210:.2e}; expected longest dry spell in 600 steps {e_longest(600, p):.1f};"
            f" P(a dry spell >= 210 within 600 steps) {1 - p_no_run(600, 210, p):.2e}")
    # the ordinary long silences for comparison: rows with longest silence 150-209
    say(f"\n(A5) timing against the dwell: silences starting after the agent had reached a source {sum(x['last_at'] >= 0 for x in recs)}/{len(recs)} (valued dwell before > 0: {sum(x['dv_b'] > 0 for x in recs)},"
        f" other dwell before > 0: {sum(x['dn_b'] > 0 for x in recs)}); never reached a source before the silence {sum(x['last_at'] < 0 for x in recs)}")
    gap = np.array([x["s"] - x["last_at"] for x in recs if x["last_at"] >= 0])
    say(f"   steps from the last step at a source to the silence start {q3(gap)} (min {int(gap.min()) if len(gap) else -1}, max {int(gap.max()) if len(gap) else -1}); dwell before the silence valued {q3(arr('dv_b'))},"
        f" other {q3(arr('dn_b'))}; dwell after the silence start valued {q3(arr('dv_a'))}, other {q3(arr('dn_a'))}")
    for lab, m in (("reached a source before the silence", [x["last_at"] >= 0 for x in recs]), ("never reached one", [x["last_at"] < 0 for x in recs])):
        sub = [x for x, k in zip(recs, m) if k]
        say(f"   {lab} ({len(sub)}): dwell-majority outcome Agent10 V/N/tie {[sum(x['c10'] == c for x in sub) for c in ('V', 'N', 'tie')]}, Agent12 {[sum(x['c12'] == c for x in sub) for c in ('V', 'N', 'tie')]}")
    ord_ = np.flatnonzero((mx >= 150) & (mx < S_ON))
    if len(ord_):
        st_ = []
        for r in ord_:
            t0 = int(np.argmax(Q10[:, r] == mx[r])); s0 = t0 - int(mx[r]) + 1; st_.append((s0, pclass(geo(o10, s0, r)), bool(AT[:s0, r].any())))
        say(f"   for comparison, the {len(ord_)} rows whose longest silence is 150-209 (never engaged): start step {q3(np.array([x[0] for x in st_]))}; class at the start "
            + ", ".join(f"({c}) {sum(x[1] == c for x in st_)}" for c in ("i", "ii", "iii", "iv", "v")) + f"; reached a source before it {sum(x[2] for x in st_)}")
    return recs


def c_short(c): return f"({c})"


# ------------------------------------------------------------------ (B)
def part_b(o10, o12):
    say("\n== (B) the bench (h2) wall contacts: World7 +1/-1, 400 x 600, Agent12 vs Agent10 ==")
    g = o12["good"]; neg = 1 - g; c10, c12 = outcome(o10), outcome(o12); l10, l12 = lost(o10), lost(o12)
    say("\n(B1) contacts")
    for lab, o in (("Agent12", o12), ("Agent10", o10)):
        c = o["contacts"]; cr = c > 0
        say(f"   [{lab}] contacts {int(c.sum())} = {c.mean():.3f} per row; rows with any contact {int(cr.sum())}; contacts per contacting row {q3f(c[cr]) if cr.any() else 'n/a'} (max {int(c.max())})")
    E10, R10, _ = released(o10); E12, R12, _ = released(o12); S10 = set(np.unique(R10).tolist()); S12 = set(np.unique(R12).tolist())
    fe = first_true(o12["ENG"])
    tt, rr = np.nonzero(o12["C"]); order = np.lexsort((tt, rr)); tt, rr = tt[order], rr[order]
    say(f"\n(B2) every Agent12 contact ({len(tt)}); the contact is registered by the move after step t's act, so engaged/u/leg/slant/hold are step t's;"
        f" position = after the move (reflected); wall by that position; stranded = the row has a drive-ended negative hold (ph24c.released) in that arm")
    recs = []
    for t, r in zip(tt, rr):
        p = o12["POS"][t, r]; walls = []
        if p[0] <= 0.6: walls.append("upwind (x = 0)")
        if p[0] >= ARENA2 - 0.6: walls.append("downwind (x = 160)")
        for yw, lab in ((0.0, "y = 0"), (ARENA2, "y = 160")):
            if abs(p[1] - yw) <= 0.6:
                vy = o12["src"][r, g[r], 1]; ny = o12["src"][r, neg[r], 1]; vside = (yw > 0) == (vy > ny)
                walls.append(f"side, {'valued' if vside else 'negative'} source's side ({lab})")
        wall = "; ".join(walls) if walls else "unclassified"
        eng = bool(o12["ENG"][t, r]); u = int(o12["U"][t, r]); k = int(o12["LEG"][t, r]); al = int(slant_of(max(u, 0))) if eng else 0
        h = int(o12["H"][t, r]); hl = "nothing" if h < 0 else "valued" if h == g[r] else "negative"
        xs = o12["src"][r, 0, 0]; da = p[0] - xs; dyv = p[1] - o12["src"][r, g[r], 1]; dyn = p[1] - o12["src"][r, neg[r], 1]
        wa = np.flatnonzero(o12["W"][t + 1:, r].any(1)); wt = t + 1 + int(wa[0]) if len(wa) else -1
        wl = whiff_lab(o12, wt, r) if wt >= 0 else "none"
        rel12 = [e for e, x in zip(E12, R12) if x == r]; after_rel = any(e <= t for e in rel12)
        rec = dict(t=t, r=r, eng=eng, u=u, k=k, al=al, hl=hl, wall=wall, da=da, dyv=dyv, dyn=dyn, wt=wt, wl=wl, s10=r in S10, s12=r in S12, after_rel=after_rel, c12=c12[r], c10=c10[r],
                   l12=bool(l12[r]), l10=bool(l10[r]), fe=int(fe[r]))
        recs.append(rec)
        say(f"   row {r:3d} step {t:3d}: engaged {int(eng)}{f', u {u}, leg {k}, slant {al:+d}' if eng else ''}; held {hl}; wall {wall}; d_along {da:+.1f}, y - y_source valued/negative {dyv:+.1f}/{dyn:+.1f};"
            f" stranded row Agent10/Agent12 {int(rec['s10'])}/{int(rec['s12'])} (after an Agent12 release {int(after_rel)}); next whiff {'step ' + str(wt) + ' ' + wl if wt >= 0 else 'none'};"
            f" outcome Agent12 {c12[r]}{' lost' if l12[r] else ''} (Agent10 {c10[r]}{' lost' if l10[r] else ''})")
    n = len(recs)
    if n == 0: say("   no contacts"); return
    say(f"\n(B2) summary over {n} contacts in {len(set(x['r'] for x in recs))} rows")
    E = [x for x in recs if x["eng"]]
    say(f"   engaged at the contact {len(E)}/{n}; not engaged {n - len(E)} (held then: " + ", ".join(f"{h} {sum(x['hl'] == h for x in recs if not x['eng'])}" for h in ("nothing", "valued", "negative")) + ")")
    say("   by leg (engaged contacts): " + "; ".join(f"leg {k} {sum(x['k'] == k for x in E)}" for k in range(1, 9) if any(x['k'] == k for x in E))
        + f"; legs 5-6 {sum(x['k'] in (5, 6) for x in E)}; u >= 300 {sum(x['u'] >= 300 for x in E)} = {sum(x['u'] >= 300 for x in E)/max(len(E), 1):.3f} of engaged contacts,"
        f" {sum(x['u'] >= 300 for x in E)/n:.3f} of all contacts; u at the contact {q3(np.array([x['u'] for x in E]))} (min {min(x['u'] for x in E) if E else -1}, max {max(x['u'] for x in E) if E else -1})")
    say(f"   by slant (engaged): upwind (+1) {sum(x['al'] == 1 for x in E)}, downwind (-1) {sum(x['al'] == -1 for x in E)}")
    wl_ = [x["wall"] for x in recs]
    say("   by wall: " + "; ".join(f"{w} {wl_.count(w)}" for w in sorted(set(wl_))))
    say("   by wall, rows: " + "; ".join(f"{w} {len(set(x['r'] for x in recs if x['wall'] == w))}" for w in sorted(set(wl_))) + "; contacts per row by row: "
        + ", ".join(f"{r}: {sum(x['r'] == r for x in recs)}" for r in sorted(set(x['r'] for x in recs))))
    da = np.array([x["da"] for x in recs]); say(f"   d_along at the contact {q3f(da)} (upwind of the sources {int((da < 0).sum())}); |d_cross| to the valued axis {q3f(np.abs([x['dyv'] for x in recs]))}")
    say(f"   contacts in Agent10-stranded rows {sum(x['s10'] for x in recs)}/{n}; in Agent12-stranded rows {sum(x['s12'] for x in recs)}/{n} (after an Agent12 release in the row {sum(x['after_rel'] for x in recs)})")
    say(f"   a whiff of either odour after the contact in the row {sum(x['wt'] >= 0 for x in recs)}/{n} (first valued {sum(x['wl'] == 'valued' for x in recs)}, negative {sum(x['wl'] == 'other' for x in recs)},"
        f" both {sum(x['wl'] == 'both' for x in recs)}); steps to it {q3(np.array([x['wt'] - x['t'] for x in recs if x['wt'] >= 0]))}")
    for kk in sorted(set(x["k"] for x in E)):
        sub = [x for x in E if x["k"] == kk]; say(f"      leg {kk}: contacts {len(sub)} in {len(set(x['r'] for x in sub))} rows, followed by a whiff {sum(x['wt'] >= 0 for x in sub)};"
                                                   f" contacts in rows ending V {sum(x['c12'] == 'V' for x in sub)}, in lost rows {sum(x['l12'] for x in sub)}")
    rows = sorted(set(x["r"] for x in recs)); rows_a = np.array(rows)
    say(f"   contacting rows {len(rows)}: Agent12 V {int((c12[rows_a] == 'V').sum())} ({(c12[rows_a] == 'V').mean():.3f}), N {int((c12[rows_a] == 'N').sum())}, tie {int((c12[rows_a] == 'tie').sum())}; lost {int(l12[rows_a].sum())}"
        f" ({l12[rows_a].mean():.3f}); engaged rows {int(o12['ENG'].any(0)[rows_a].sum())}; Agent10-stranded {sum(r in S10 for r in rows)}; Agent12-stranded {sum(r in S12 for r in rows)}")
    fc = np.array([min(x["t"] for x in recs if x["r"] == r) for r in rows]); ff = np.array([fe[r] for r in rows])
    say(f"   first contact step in the contacting rows {q3(fc)}; first engaged step {q3(ff[ff >= 0])}; first contact before the first engaged step {int(((ff < 0) | (fc < ff)).sum())}")
    er = np.flatnonzero(o12["ENG"].any(0)); crow = set(rows)
    for lab, sub in (("contacting rows", [r for r in er if r in crow]), ("engaged rows without a contact", [r for r in er if r not in crow])):
        gs = [geo(o12, int(fe[r]), r) for r in sub]; da_ = np.array([x["val"][0] for x in gs]); dcn = np.array([min(abs(x["val"][1]), abs(x["oth"][1])) for x in gs])
        side = np.array([min(x["pos"][1], ARENA2 - x["pos"][1]) for x in gs]); upw = np.array([x["pos"][0] for x in gs])
        say(f"   at the first engaged step, {lab} ({len(sub)}): d_along {q3f(da_)}; |d_cross| to the nearer axis {q3f(dcn)}; distance to the nearer side wall {q3f(side)} (min {side.min():.1f});"
            f" distance to the upwind wall {q3f(upw)} (min {upw.min():.1f}); Agent10-stranded {sum(r in S10 for r in sub)}")
    # (B3)
    say("\n(B3) the (h2) effect decomposed")
    s10 = np.array(sorted(S10)); e12 = o12["ENG"].any(0)
    say(f"   Agent10 stranded rows (a drive-ended negative hold) {len(s10)}; Agent12 stranded rows {len(S12)} (both {len(S10 & S12)}, Agent12 only {len(S12 - S10)}, Agent10 only {len(S10 - S12)})")
    f10 = np.array([min(e for e, x in zip(E10, R10) if x == r) for r in s10]); fe_s = fe[s10]
    say(f"   of Agent10's stranded rows: engaged in Agent12 {int(e12[s10].sum())}; the first release precedes the first engaged step (the same release in both arms, rows identical before engagement)"
        f" {int(((fe_s >= 0) & (f10 < fe_s)).sum())}; first engaged step - first release {q3((fe_s - f10)[fe_s >= 0])}; not engaged {int((~e12[s10]).sum())} (their last-third whiff: lost in Agent10 {int(l10[s10][~e12[s10]].sum())})")
    se = s10[e12[s10]]
    wh = np.array([bool(o12["W"][fe[r]:, r].any()) for r in se]); fo = []
    for r in se:
        w = np.flatnonzero(o12["W"][fe[r]:, r].any(1)); fo.append(whiff_lab(o12, fe[r] + int(w[0]), r) if len(w) else "none")
    ev12 = events(o12); form = ev12["form"]
    reneg = np.array([bool((form[fe[r] + 1:, r] & (o12["H"][fe[r] + 1:, r] == neg[r])).any()) for r in se])
    reval = np.array([bool((form[fe[r] + 1:, r] & (o12["H"][fe[r] + 1:, r] == g[r])).any()) for r in se])
    restr = np.array([any((x == r) and (e > fe[r]) for e, x in zip(E12, R12)) for r in se])
    rv = np.array([bool(o12["AT2"][fe[r]:, r, g[r]].any()) for r in se])
    say(f"   engaged stranded rows {len(se)}: a whiff after the first engaged step {int(wh.sum())} (first odour valued {fo.count('valued')}, negative {fo.count('other')}, both {fo.count('both')}, none {fo.count('none')});"
        f" a negative hold re-formed after engagement {int(reneg.sum())}; stranded again (a drive-ended negative hold after engagement) {int(restr.sum())}; a valued hold formed after engagement {int(reval.sum())};"
        f" the valued source reached after engagement {int(rv.sum())}")
    for lab, m in (("first whiff valued", np.array([x == "valued" for x in fo])), ("first whiff negative", np.array([x == "other" for x in fo])), ("no whiff", np.array([x == "none" for x in fo]))):
        sub = se[m]
        if len(sub): say(f"      {lab} ({len(sub)}): Agent12 V/N/tie {[int((c12[sub] == c).sum()) for c in ('V', 'N', 'tie')]}, lost {int(l12[sub].sum())}; re-formed negative hold {int(reneg[m].sum())}, stranded again {int(restr[m].sum())};"
                         f" rows with a contact {int((o12['contacts'][sub] > 0).sum())}")
    for lab, o, cc, ll in (("Agent10", o10, c10, l10), ("Agent12", o12, c12, l12)):
        say(f"   Agent10's stranded rows, outcome in {lab}: V {int((cc[s10] == 'V').sum())} N {int((cc[s10] == 'N').sum())} tie {int((cc[s10] == 'tie').sum())}; lost {int(ll[s10].sum())}")
    ns = np.setdiff1d(np.arange(N), s10)
    say(f"   Agent12 engaged rows not stranded in Agent10: {int(e12[ns].sum())} (Agent10 outcome V/N/tie {[int((c10[ns][e12[ns]] == c).sum()) for c in ('V', 'N', 'tie')]}, lost {int(l10[ns][e12[ns]].sum())};"
        f" Agent12 V/N/tie {[int((c12[ns][e12[ns]] == c).sum()) for c in ('V', 'N', 'tie')]}, lost {int(l12[ns][e12[ns]].sum())}; held nothing at any step before engagement"
        f" {int(np.array([bool((o10['H'][:fe[r], r] < 0).all()) for r in ns[e12[ns]]]).sum())})")
    say("   paired outcome table, all 400 rows (rows Agent10, columns Agent12):")
    for a in ("V", "N", "tie"):
        say(f"      Agent10 {a:3s}: " + "  ".join(f"-> {b} {int(((c10 == a) & (c12 == b)).sum()):3d}" for b in ("V", "N", "tie")))
    cr = o12["contacts"] > 0; s10m = np.isin(np.arange(N), s10)
    iv = (c12 == "V") & (c10 != "V"); ov = (c12 != "V") & (c10 == "V"); il = l12 & ~l10; ol = ~l12 & l10
    say(f"   into V {int(iv.sum())}, out of V {int(ov.sum())} (net {int(iv.sum() - ov.sum()):+d} = P(V) DP {(iv.sum() - ov.sum())/N:+.4f}); into lost {int(il.sum())}, out of lost {int(ol.sum())}"
        f" (net {int(il.sum() - ol.sum()):+d} = lost DP {(il.sum() - ol.sum())/N:+.4f})")
    for lab, m in (("Agent10-stranded rows", s10m), ("other rows", ~s10m), ("Agent12 contact rows", cr), ("Agent12 no-contact rows", ~cr), ("engaged, no contact", e12 & ~cr), ("never engaged", ~e12)):
        say(f"      {lab} ({int(m.sum())}): into V {int((iv & m).sum())}, out of V {int((ov & m).sum())}; into lost {int((il & m).sum())}, out of lost {int((ol & m).sum())}")
    # (B4)
    say("\n(B4) P(V | wall contact) and P(lost | wall contact), Agent12's contact rows (Wilson 95 percent)")
    V12, V10 = c12 == "V", c10 == "V"
    say(f"   Agent12 P(V | contact) {wil(int((V12 & cr).sum()), int(cr.sum()))}; P(V | no contact) {wil(int((V12 & ~cr).sum()), int((~cr).sum()))}")
    say(f"   Agent12 P(lost | contact) {wil(int((l12 & cr).sum()), int(cr.sum()))}; P(lost | no contact) {wil(int((l12 & ~cr).sum()), int((~cr).sum()))}")
    say(f"   paired on the same rows: in Agent12's contact rows Agent12 V {int((V12 & cr).sum())}/{int(cr.sum())}, Agent10 V {int((V10 & cr).sum())}/{int(cr.sum())}; lost Agent12 {int((l12 & cr).sum())}, Agent10 {int((l10 & cr).sum())};"
        f" in the no-contact rows Agent12 V {int((V12 & ~cr).sum())}/{int((~cr).sum())}, Agent10 V {int((V10 & ~cr).sum())}/{int((~cr).sum())}; lost Agent12 {int((l12 & ~cr).sum())}, Agent10 {int((l10 & ~cr).sum())}")
    em = e12
    say(f"   engaged rows only ({int(em.sum())}): P(V | contact) {wil(int((V12 & cr & em).sum()), int((cr & em).sum()))}, P(V | no contact) {wil(int((V12 & ~cr & em).sum()), int((~cr & em).sum()))};"
        f" P(lost | contact) {wil(int((l12 & cr & em).sum()), int((cr & em).sum()))}, P(lost | no contact) {wil(int((l12 & ~cr & em).sum()), int((~cr & em).sum()))}")
    say(f"   Agent10-stranded rows ({len(s10)}): P(V | Agent12 contact) {wil(int((V12 & cr & s10m).sum()), int((cr & s10m).sum()))}, without {wil(int((V12 & ~cr & s10m).sum()), int((~cr & s10m).sum()))};"
        f" P(lost | contact) {wil(int((l12 & cr & s10m).sum()), int((cr & s10m).sum()))}, without {wil(int((l12 & ~cr & s10m).sum()), int((~cr & s10m).sum()))}")
    return recs


def main():
    mods = (ph9, ph11, ph12b, ph13, ph15, ph16, ph18, ph19, ph21, ph22, ph24, ph24b, ph24c)
    say(f"== H17 post-bench diagnosis (measurement only; owner 2026-09-24, '3번 진단 먼저 진행해'). ph26b.py sha256 {sha()}; ph26.py sha256 {sha(ph26.__file__)};"
        f" design {ph26.DESIGN}; reproduces experiments/h17/ph26_bench.txt sha256 {BENCH_TXT_SHA} (record:h17-bench-result) ==")
    say("   imported modules (unchanged): " + "; ".join(f"{os.path.basename(m.__file__)} {sha(m.__file__)}" for m in mods))
    say("   bench seeds only (ph26.BS, bootstrap seed as ph26 sets it; not written out here); dev and eval seeds untouched. Nothing is changed or adopted; the H17 verdict"
        " (stopped at the bench, no candidate on part (d)) is not re-judged; S, gamma, L0, U1 and every bar as registered; no sweep")
    say(f"   S {S_ON}; walls 160 apart (World7); 'at a wall' = within {WALL_NEAR} of a wall; LMAX {LMAX:.0f}; whiff probability 0.3 exp(-d_along / {LAM:.0f}) inside a region")
    T1 = reproduce()
    if T1 is None:
        say("== reproduction FAILED: nothing measured =="); return 1
    part_a(T1[("Agent10", (1.0, 0.0))], T1[("Agent12", (1.0, 0.0))])
    part_b(T1[("Agent10", (1.0, -1.0))], T1[("Agent12", (1.0, -1.0))])
    say("\n== end (measurement only; positions and counts, no cause named; no change tested; bench seeds only) ==")
    return 0


if __name__ == "__main__":
    rc = main()
    with open(OUT, "w", encoding="utf-8", newline="\n") as f: f.write("\n".join(_lines) + "\n")
    hits, _, nf = ph26.seeds_unused()
    print(f"[written {OUT}; sha256 {sha(OUT)}; ph26's seed self-check after writing it: no H17 seed in any other file {not hits} ({nf} files scanned){'' if not hits else ' ' + str(hits)}]")
    sys.exit(rc)
