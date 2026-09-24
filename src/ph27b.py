#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H17 Run 2 post-bench diagnosis (measurement only; owner 2026-09-24, '2번 진단 먼저 진행', decision:h17-run2-post-bench-diagnosis).

Usage: python ph27b.py      (writes experiments/h17/ph27b_diag.txt, LF line ends)

ph27.py and ph26.py (sha256 checked below against the bench's), design v2 FINAL and the bench verdict (B NOT passed: STOPPED by
the registered (h2) stop rule, record:h17-run2-bench-result) are untouched: the Search rule, S 250, gamma, L0, U1, every bar and
every adopted module are imported as they are; no rule is changed, no agent variant is added, no S is swept. Bench seeds only
(ph27.BS and the bootstrap seed as ph27 sets it; not written out here, so ph27's seed self-check stays valid); the development and
evaluation seeds are not used.

Reproduction first: ph27.bench is re-run in this process and its output must equal experiments/h17/ph27_bench.txt line for line
(the file's sha256 is checked first); then the runs measured here (ph27.run, World7 +1/-1 and +1/0, Agent13 and Agent10; ph27.stub,
the (b'2) constructed stranded state) must reproduce the bench's (d), (h1), (h2) and (b'2) lines character for character, and the
row identity (bench (a2)) must hold. On any mismatch nothing is measured.

(A) T3 (+1/-1): the stranded rows (a drive-ended negative hold in Agent10, ph24c.released): which engage, where the search starts
    and goes, which find a whiff after engagement and which do not (positions at engagement, 100 / 200 / 300 steps later and at step
    599 relative to both sources, the leg reached, the closest approach to each whiff region, a position class), the release-to-
    engagement displacement, the rows that stay lost after a whiff, the paired transitions, the effect-size chain.
(B) `since` - q at the first engaged step: per row with a non-zero value (task stranded rows and the (b'2) constructed rows), the last
    whiff before the engagement silence and the last navigation event (step, odour, what was held), classified by the code line
    that makes the whiff not a navigation event; outcomes by `since` - q; the same quantities in the T1 +1/0 silences for reference.
Positions are the position a step's sense used (the position after the previous step's move; the start for step 0), as ph26b.geo.
q at step t is recorded after that step's act (ph26.py:90), so q = t - (the last step with a whiff); `since` likewise resets on a
navigation event (ph21.py:75), so `since` - q = (last whiff step) - (last navigation step) at any step.
Names no cause beyond what is measured; tests no change.
"""
import sys, os, hashlib, math
import numpy as np
import ph27                                      # installs ph27's run-time hooks and sets the bootstrap seed, as the bench did
import ph26, ph26b
import ph9, ph11, ph12b, ph13, ph15, ph16, ph18, ph19, ph21, ph22, ph24, ph24b, ph24c
from ph27 import Agent13, Agent10, run, stub, BS, BENCH, S_RUN2, pp_d, neg_after, fmt_ci
from ph26 import lost, cls3, qrec, pp_dp, leg_of, search_target, row_identity
from ph26b import geo, pclass, CLS_NAMES, whiff_lab, outcome, sensed, WALL_NEAR
from ph16 import interval
from ph18 import majority
from ph21 import q3, first_true
from ph24 import q3f
from ph24c import released, cone_geom, hold_start, toward
from ph9 import LMAX

PH27_SHA = "d12fa65174e9688c99cda8b00c747c1f69d540e0d82e87db6a528e8d518c143a"
PH26_SHA = ph27.PH26_SHA
BENCH_TXT_SHA = "7176278acbff279565ee2a7bc8a88c857d3c9b78073220fe8a84d5fe08c69b71"
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
BENCH_TXT = os.path.join(REPO, "experiments", "h17", "ph27_bench.txt"); OUT = os.path.join(REPO, "experiments", "h17", "ph27b_diag.txt")
N = BENCH["rows"]; LAST = BENCH["steps"] - 1


def sha(p=__file__): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def wil(k, n):
    if n == 0: return f"{k}/0"
    p, lo, hi = ph15.wilson(k, n); return f"{k}/{n} = {p:.3f} [{lo:.3f}, {hi:.3f}]"
def fr(k, n): return f"{k}/{n} = {k / n:.3f}" if n else f"{k}/0"
def cnt(v, keys): return ", ".join(f"{k} {list(v).count(k)}" for k in keys)
def mm(x, f=".1f"): return f"(min {np.min(x):{f}}, max {np.max(x):{f}})" if len(x) else ""


_lines = []
def say(s=""): _lines.append(s); print(s, flush=True)


# ------------------------------------------------------------------ reproduction
def h2_lines(o13, o10):
    """the bench's (h2) lines 1-5, the `since` - q line and the engaged-stranded line, with ph27.bench's own format strings"""
    V13, V10 = majority(o13)[0], majority(o10)[0]; l13, l10 = lost(o13), lost(o10)
    P2, dp2, b2, sd2, P2m = pp_dp(l13, l10, -0.05, True); _, _, llo, lhi = interval("DP", l13.astype(float), l10.astype(float)); stop2 = P2 < 0.5
    Pb, dpv, bv, sdv, Pbm = pp_dp(V13, V10, -0.02, False); _, _, vlo, vhi = interval("DP", V13.astype(float), V10.astype(float))
    cm = o13["contacts"].mean(); e_ = o13["ENG"].any(0); c13, c10 = cls3(o13), cls3(o10)
    _, r10, _ = released(o10); _, r13, _ = released(o13); s10, s13 = np.unique(r10), np.unique(r13)
    out = [f"(h2) T3 on bench seeds, World7 +1/-1 {N} x {BENCH['steps']}: " + "; ".join(f"{k} V {int(majority(o)[0].sum())} N {int(majority(o)[1].sum())} tie {int(majority(o)[2].sum())},"
           f" lost rows {int(lost(o).sum())}, contacts per row {o['contacts'].mean():.3f}" for k, o in (("Agent13", o13), ("Agent10", o10))),
           f"   (h2) stranded rows (a drive-ended negative hold, as R3): Agent10 {len(s10)} (releases {len(r10)}), Agent13 {len(s13)}; Agent13 engaged rows {int(e_.sum())}, engaged (row, step) {int(o13['ENG'].sum())};"
           f" lost among Agent10's stranded rows: Agent10 {int(l10[s10].sum())}, Agent13 {int(l13[s10].sum())}",
           f"   (h2) lost-row paired DP Agent13 - Agent10 {dp2:+.4f} [{llo:+.4f}, {lhi:+.4f}]; P(V) paired DP {dpv:+.4f} [{vlo:+.4f}, {vhi:+.4f}]; contacts per row {cm:.3f};"
           f" into V {int(((c13 == 0) & (c10 != 0)).sum())}, out of V {int(((c13 != 0) & (c10 == 0)).sum())}; out of lost {int((l10 & ~l13).sum())}, into lost {int((l13 & ~l10).sum())}",
           f"   (h2) M3 (a)'s pass probability (upper bound <= -0.05) at the bench DP {dp2:+.4f}, discordant b {b2:.4f}, sd {sd2:.4f}: {P2:.4f} (measured paired sd: {P2m:.4f});"
           f" reported: M3 (b) (lower bound >= -0.02) at {dpv:+.4f}, b {bv:.4f}: {Pb:.4f} (measured sd: {Pbm:.4f})",
           f"   (h2) STOP RULE (design section 4): pass probability {P2:.4f} {'< 0.5 -> STOP: the run returns to the owner after the bench record' if stop2 else '>= 0.5 -> continue'}"]
    fe = first_true(o13["ENG"]); se_ = np.array([r for r in s10 if fe[r] >= 0], int)
    dsq = np.array([o13["SINCE"][fe[r], r] - o13["Q"][fe[r], r] for r in se_])
    out.append(f"   (h2) `since` - q at the first engaged step in Agent10-stranded rows engaged in Agent13 ({len(se_)}): {q3(dsq)} (min {int(dsq.min())}, max {int(dsq.max())});"
               f" equal to 0 in {int((dsq == 0).sum())}/{len(dsq)}; first engaged step - first release {q3(np.array([fe[r] - min(ee for ee, x in zip(released(o10)[0], r10) if x == r) for r in se_]))}")
    fo, reneg, restr = neg_after(o13, se_, fe)
    out.append(f"   (h2) engaged stranded rows {len(se_)}: first whiff after the first engaged step valued {fo.count('valued')}, negative {fo.count('other')}, both {fo.count('both')}, none {fo.count('none')};"
               f" a negative hold re-formed after engagement {int(reneg.sum())}; stranded again {int(restr.sum())}; Agent13 V {int(V13[se_].sum())}, lost {int(l13[se_].sum())} (Agent10 V {int(V10[se_].sum())}, lost {int(l10[se_].sum())})")
    return out, dict(dp=dp2, lo=llo, hi=lhi, P=P2)


def t1_lines(T):
    out = []
    for lab, o in (("World7 +1/0 Agent10", T[("Agent10", (1.0, 0.0))]), ("World7 +1/-1 Agent10", T[("Agent10", (1.0, -1.0))])):
        Q = qrec(o["W"]); mx = Q.max(0)
        out.append(f"   [{lab}] longest any-odour silence per row: quartiles {q3(mx)}, p90 {np.percentile(mx, 90):.0f}, p95 {np.percentile(mx, 95):.0f}, max {mx.max():.0f}; rows reaching q >= 150/180/210/250/300: "
                   + "/".join(str(int((mx >= c).sum())) for c in (150, 180, 210, 250, 300)) + "; fraction of (row, step) with q >= 150/180/210/250/300: " + "/".join(f"{(Q >= c).mean():.5f}" for c in (150, 180, 210, 250, 300)))
    for lab, v in (("+1/0", (1.0, 0.0)), ("+1/-1", (1.0, -1.0))):
        o = T[("Agent13", v)]; er = o["ENG"].any(0); k_, pt, lo, hi = interval("P", er)
        mx10 = qrec(T[("Agent10", v)]["W"]).max(0); same = bool(np.array_equal(er, mx10 >= S_RUN2))
        out.append(f"   [World7 {lab} Agent13] rows with any engaged step {fmt_ci(k_, N, pt, lo, hi)}; engaged (row, step) {int(o['ENG'].sum())}; first engaged step {q3(first_true(o['ENG'])[er])};"
                   f" the engaged rows are exactly the rows whose Agent10 silence reaches 250: {same}"
                   + (f" -> bar upper bound <= 0.05: {'PASS' if hi <= 0.05 else 'FAIL'} (pass probability, exact binomial P(K <= 11 of 400) at p {pt:.4f}, reading R13: {pp_d(k_):.4f})" if v == (1.0, 0.0) else " (reported)"))
    o13, o10 = T[("Agent13", (1.0, 0.0))], T[("Agent10", (1.0, 0.0))]; V13, V10 = majority(o13)[0], majority(o10)[0]; c13, c10 = cls3(o13), cls3(o10)
    P1, dp1, b1, sd1, P1m = pp_dp(V13, V10, -0.05, False); _, _, blo, bhi = interval("DP", V13.astype(float), V10.astype(float))
    e_ = o13["ENG"].any(0); l13, l10 = lost(o13), lost(o10)
    out.append(f"(h1) T1 on bench seeds, World7 +1/0 {N} x {BENCH['steps']}: " + "; ".join(f"{k} V {int(majority(o)[0].sum())} N {int(majority(o)[1].sum())} tie {int(majority(o)[2].sum())} P(V) "
               f"{interval('P', majority(o)[0])[1]:.3f} [{interval('P', majority(o)[0])[2]:.3f}, {interval('P', majority(o)[0])[3]:.3f}]" for k, o in (("Agent13", o13), ("Agent10", o10))))
    out.append(f"   (h1) paired DP P(V) Agent13 - Agent10 {dp1:+.4f} [{blo:+.4f}, {bhi:+.4f}] (bootstrap 5000, seed {ph15.BOOT_SEED}); engaged rows {int(e_.sum())}; into V {int(((c13 == 0) & (c10 != 0)).sum())},"
               f" out of V {int(((c13 != 0) & (c10 == 0)).sum())}; V among engaged rows Agent13 {int(V13[e_].sum())} vs Agent10 {int(V10[e_].sum())}; lost rows {int(l13.sum())} vs {int(l10.sum())};"
               f" contacts per row {o13['contacts'].mean():.3f} vs {o10['contacts'].mean():.3f}")
    return out


def b2_line(o):
    fe = first_true(o["ENG"]); r_ = np.arange(o["H"].shape[1]); fes = np.maximum(fe, 0)
    dsq = (o["SINCE"][fes, r_] - o["Q"][fes, r_])[fe >= 0]; formed = (o["H"] == 1).any(0)
    return (f"      `since` - q on the first engaged step: {q3(dsq)} (min {int(dsq.min()) if len(dsq) else 0}, max {int(dsq.max()) if len(dsq) else 0}); equal to 0 in {int((dsq == 0).sum())}/{len(dsq)} rows",
            f"constructed state: hold of the negative odour formed {int(formed.sum())}/{N}")


def reproduce():
    say("\n== (0) reproduction (nothing is measured unless every check holds) ==")
    ok27, ok26, okt = sha(ph27.__file__) == PH27_SHA, sha(ph26.__file__) == PH26_SHA, sha(BENCH_TXT) == BENCH_TXT_SHA
    say(f"   ph27.py sha256 equals the bench's ({PH27_SHA[:8]}...{PH27_SHA[-4:]}): {ok27}; ph26.py sha256 equals the bench's ({PH26_SHA[:8]}...{PH26_SHA[-4:]}): {ok26};"
        f" ph27_bench.txt sha256 equals the recorded ({BENCH_TXT_SHA[:8]}...{BENCH_TXT_SHA[-4:]}): {okt}")
    if not (ok27 and ok26 and okt): return None
    want = open(BENCH_TXT, encoding="utf-8").read().split("\n")
    if want and want[-1] == "": want = want[:-1]
    got = []; ph27.bench(say=got.append)
    same = got == want; diff = [i + 1 for i in range(max(len(got), len(want))) if i >= len(got) or i >= len(want) or got[i] != want[i]]
    say(f"   ph27.bench re-run in this process ({len(got)} lines) equals ph27_bench.txt ({len(want)} lines) line for line: {same}" + ("" if same else f"; differing line numbers {diff[:20]}"))
    if not same: return None
    T = {(k, v): run("T1", c, v, BS) for v in ((1.0, 0.0), (1.0, -1.0)) for k, c in (("Agent13", Agent13), ("Agent10", Agent10))}
    b2 = stub(Agent13, [1.0, -1.0], [(20, 0.0, 0.30), (BENCH["steps_b"] - 20, 0.0, 0.0)])
    h2, head = h2_lines(T[("Agent13", (1.0, -1.0))], T[("Agent10", (1.0, -1.0))])
    bl, bform = b2_line(b2)
    mine = t1_lines(T) + h2 + [bl]
    hit = [m in want for m in mine]; hit_form = any(bform in w for w in want)
    say(f"   the runs measured below (ph27.run, World7 +1/0 and +1/-1, Agent13 and Agent10, bench seeds, {N} x {BENCH['steps']}; ph27.stub, the (b'2) schedule, {BENCH['steps_b']} steps):"
        f" the bench's (d) gap lines (+1/0, +1/-1), (d) engaged-row lines (+1/0, +1/-1), (h1) two lines, (h2) five lines, the (h2) `since` - q line, the (h2) engaged-stranded line and the"
        f" (b'2) `since` - q line recomputed from them are each present verbatim in ph27_bench.txt: {hit} -> {all(hit)}; (b'2) '{bform}' present: {hit_form}")
    for m in mine: say("      " + m.strip().replace(str(ph15.BOOT_SEED), "<ph27's bootstrap seed>"))
    ok_id = all(row_identity(T[("Agent13", v)], T[("Agent10", v)])[0] for v in ((1.0, 0.0), (1.0, -1.0)))
    say(f"   never-engaged rows bitwise Agent10 and engaged rows equal before their first engaged step, both value pairs (bench (a2)): {ok_id}")
    heads = (f"{head['dp']:+.4f} [{head['lo']:+.4f}, {head['hi']:+.4f}]", f"{head['P']:.4f}")
    say(f"   headline (h2) numbers reproduced: lost-row DP {heads[0]}, M3 (a) pass probability {heads[1]} (bench: -0.0650 [-0.0900, -0.0425], 0.2287):"
        f" {heads == ('-0.0650 [-0.0900, -0.0425]', '0.2287')}")
    ok = all(hit) and hit_form and ok_id and heads == ("-0.0650 [-0.0900, -0.0425]", "0.2287")
    return (T, b2) if ok else None


# ------------------------------------------------------------------ helpers
def sensed_all(o): return np.concatenate([o["start"][None], o["POS"][:-1]], 0)


def side(gg):
    """which side of the pair: beyond the valued source (outward of the valued axis), beyond the negative one, or between the axes"""
    return "beyond valued" if gg["val"][1] > 0 else "beyond negative" if gg["oth"][1] > 0 else "between"


def nearer(gg): return min(abs(gg["val"][1]), abs(gg["oth"][1]))
def dnear(gg): return min(gg["val"][3], gg["oth"][3])


def leg1_toward_pair(o, t, r):
    """leg 1's crosswind direction at step t (the first engaged step) points toward the pair's midline (the sign of sin(target) vs y_mid - y)"""
    ts = search_target(np.array([0.0]), np.array([o["CS"][t, r]]))[0]; y = sensed(o, t, r)[1]; ym = o["src"][r, :, 1].mean()
    return bool(np.sign(np.sin(np.radians(ts))) == np.sign(ym - y))


def region_track(o, SP, r, t0, t1):
    """per step t0..t1 (sensed positions): distance to the valued and to the negative whiff region (0 inside)"""
    g = o["good"][r]; out = {}
    for lab, k in (("val", g), ("neg", 1 - g)):
        s = o["src"][r, k]; ins, d = cone_geom(SP[t0:t1 + 1, r, 0] - s[0], SP[t0:t1 + 1, r, 1] - s[1]); out[lab] = (ins, d)
    return out


def geo_line(gg):
    return (f"{pclass(gg)} d_along {gg['val'][0]:+.1f}, d_cross valued/negative axis {gg['val'][1]:+.1f}/{gg['oth'][1]:+.1f}, {side(gg)}, nearest region {dnear(gg):.1f},"
            f" wall {gg['wall']:.1f}")


def geo_summary(gs):
    da = np.array([x["val"][0] for x in gs]); cv = np.array([x["val"][1] for x in gs]); cn = np.array([x["oth"][1] for x in gs])
    dn = np.array([dnear(x) for x in gs]); ins = np.array([x["val"][2] or x["oth"][2] for x in gs]); wl = np.array([x["wall"] for x in gs])
    near = np.array([nearer(x) for x in gs]); sd = [side(x) for x in gs]; cl = [pclass(x) for x in gs]
    return (f"d_along {q3f(da)} {mm(da)}; upwind of both (d_along < 0) {int((da < 0).sum())}; beyond LMAX (d_along >= {LMAX:.0f}) {int((da >= LMAX).sum())};"
            f" d_cross valued axis (outward +) {q3f(cv)}, negative axis {q3f(cn)}; |d_cross| to the nearer axis {q3f(near)}; side {cnt(sd, ('beyond valued', 'between', 'beyond negative'))};"
            f" inside a whiff region {int(ins.sum())}; distance to the nearest region {q3f(dn)} {mm(dn)}; nearest wall {q3f(wl)} (within {WALL_NEAR}: {int((wl < WALL_NEAR).sum())});"
            f" class {cnt(cl, ('i', 'ii', 'iii', 'iv', 'v'))}")


def majority_class(o, r, t0, t1):
    cl = [pclass(geo(o, t, r)) for t in range(t0, t1 + 1)]; share = {c: cl.count(c)/len(cl) for c in ("i", "ii", "iii", "iv", "v")}
    dom = max(share, key=share.get); return (dom if share[dom] >= 0.5 else "vi"), share, len(cl)


def cross_near(P, src, r, t0, t1):
    """the first step in [t0, t1] at which the position is on the other side of the axis of the source nearer (crosswind) at t0:
    (step, d_along there) or None"""
    ys = src[r, :, 1]; y0 = P[t0, r, 1]; k = int(np.argmin(np.abs(y0 - ys))); s0 = np.sign(y0 - ys[k])
    idx = np.flatnonzero(np.sign(P[t0:t1 + 1, r, 1] - ys[k]) != s0)
    if not len(idx): return None
    t = t0 + int(idx[0]); return t, float(P[t, r, 0] - src[r, k, 0])


def cross_summary(recs):
    """recs: list of (crossing or None, u of the first whiff or -1)"""
    cr = [(c, w) for c, w in recs if c is not None]; da = np.array([c[1] for c, _ in cr]); u = np.array([c[0] for c, _ in cr])
    wb = sum(1 for c, w in cr if 0 <= w <= c[0])
    return (f"crossed the nearer source's axis {len(cr)}/{len(recs)}; u at the crossing {q3(u)}; d_along there {q3f(da)} {mm(da)} (upwind of the sources {int((da < 0).sum())}, 0-25 {int(((da >= 0) & (da < LMAX)).sum())},"
            f" beyond LMAX {int((da >= LMAX).sum())}); a whiff at or before the crossing {wb}")


# ------------------------------------------------------------------ (A)
def part_a(o13, o10):
    say("\n== (A) T3 +1/-1, 400 x 600, Agent13 vs Agent10 (bench seeds): the stranded rows and where the search does or does not find a whiff ==")
    g = o13["good"]; c13, c10 = outcome(o13), outcome(o10); l13, l10 = lost(o13), lost(o10)
    E10, R10, _ = released(o10); rel = {}
    for e, r in zip(E10, R10): rel.setdefault(int(r), []).append(int(e))
    s10 = np.array(sorted(rel)); fe = first_true(o13["ENG"]); e13 = fe >= 0
    se = s10[e13[s10]]; sn = s10[~e13[s10]]; en = np.setdiff1d(np.flatnonzero(e13), s10); SP = sensed_all(o13)
    Q = o13["Q"]; W = o13["W"].any(2); r_all = np.arange(N)
    first_rel = {r: min(rel[r]) for r in s10}; last_rel_before = {r: max(e for e in rel[r] if e <= fe[r]) for r in se}
    fl = dict(FLEE=o13["FS"], plus_y=o13["plus_y"], good=g)

    say("\n(A1) stranded-row decomposition (as Run 1's diagnosis (B3))")
    nrel = np.array([len(rel[r]) for r in s10])
    say(f"   Agent10 stranded rows (a drive-ended negative hold, ph24c.released) {len(s10)}; releases {len(E10)}; rows with more than one release {int((nrel > 1).sum())} (max {nrel.max()})")
    say(f"   Agent13 engaged rows {int(e13.sum())} = Agent10-stranded and engaged {len(se)} + engaged but not Agent10-stranded {len(en)}; Agent10-stranded but never engaged {len(sn)}")
    say(f"   first release step, all stranded rows: {q3(np.array([first_rel[r] for r in s10]))} {mm(np.array([first_rel[r] for r in s10]), '.0f')}; engaged {q3(np.array([first_rel[r] for r in se]))};"
        f" never engaged {q3(np.array([first_rel[r] for r in sn]))}")
    d_first = np.array([fe[r] - first_rel[r] for r in se]); d_last = np.array([fe[r] - last_rel_before[r] for r in se])
    vals, cts = np.unique(d_last, return_counts=True)
    say(f"   engaged stranded rows {len(se)}: first engaged step {q3(fe[se])} {mm(fe[se], '.0f')}; steps left at engagement (599 - step) {q3(LAST - fe[se])} {mm(LAST - fe[se], '.0f')};"
        f" engaged at step <= 399 (>= 200 steps left) {int((fe[se] <= 399).sum())}")
    say(f"   first engaged step - first release {q3(d_first)} {mm(d_first, '.0f')}; - the last release before it {q3(d_last)} {mm(d_last, '.0f')}; values: "
        + ", ".join(f"{int(v)}: {int(c)}" for v, c in zip(vals, cts)))
    say(f"   the release precedes engagement in every engaged stranded row: {all(first_rel[r] <= fe[r] for r in se)}")
    # the not-engaged stranded rows
    say(f"   Agent10-stranded rows never engaged ({len(sn)}): why q never reached 250 with nothing held")
    why = []
    for r in sn:
        lr = max(rel[r]); fr_ = first_rel[r]; wafter = np.flatnonzero(W[lr + 1:, r]) + lr + 1; qmax = int(Q[fr_:, r].max())
        held250 = int(((Q[:, r] >= S_RUN2) & (o13["H"][:, r] >= 0)).sum()); lw = int(np.flatnonzero(W[:, r])[-1]) if W[:, r].any() else -1
        if held250: k = "q >= 250 only while something is held"
        elif len(wafter) == 0: k = "no whiff after the last release; the run ends before q reaches 250"
        else: k = "a whiff after the last release reset q"
        why.append(k)
        wl = [whiff_lab(o13, int(t), r) for t in wafter]
        hl = [("nothing" if o13["H"][t, r] < 0 else "valued" if o13["H"][t, r] == g[r] else "negative") for t in wafter]
        say(f"      row {r:3d}: releases {rel[r]}; steps left after the last release {LAST - lr}; last whiff step {lw} (q at step 599 {int(Q[LAST, r])}); max q after the first release {qmax};"
            f" whiff steps after the last release {len(wafter)} (first {int(wafter[0]) if len(wafter) else '-'}: odours {cnt(wl, ('valued', 'other', 'both'))}; held at them {cnt(hl, ('nothing', 'valued', 'negative'))});"
            f" -> {k}; outcome Agent10 {c10[r]}{' lost' if l10[r] else ''}")
    say("   never-engaged stranded rows by reason: " + "; ".join(f"{k} {why.count(k)}" for k in sorted(set(why))))
    lrs = np.array([max(rel[r]) for r in sn])
    say(f"   never-engaged stranded rows: last release step {q3(lrs)} {mm(lrs, '.0f')}; steps left after it {q3(LAST - lrs)}; last release after step 397 (fewer than 202 steps left) {int((lrs > 397).sum())};"
        f" Agent10 outcome V/N/tie {[int((c10[sn] == c).sum()) for c in ('V', 'N', 'tie')]}, lost {int(l10[sn].sum())}")
    # whiff after engagement
    tw = {r: (int(np.flatnonzero(W[fe[r] + 1:, r])[0]) + fe[r] + 1 if W[fe[r] + 1:, r].any() else -1) for r in se}
    wr = np.array([r for r in se if tw[r] >= 0], int); nw = np.array([r for r in se if tw[r] < 0], int)
    fo = {r: whiff_lab(o13, tw[r], r) for r in wr}; u_ = np.array([tw[r] - fe[r] for r in wr])
    say(f"   engaged stranded rows with a whiff after the first engaged step {len(wr)} (first whiffed odour valued {sum(fo[r] == 'valued' for r in wr)}, negative {sum(fo[r] == 'other' for r in wr)},"
        f" both {sum(fo[r] == 'both' for r in wr)}); u at the first whiff {q3(u_)} {mm(u_, '.0f')}; leg at it (leg of u) {cnt(leg_of(u_).tolist(), range(1, 8))}; without a whiff {len(nw)}")
    for lab, sub in (("with a whiff after engagement", wr), ("no whiff after engagement", nw)):
        say(f"      {lab} ({len(sub)}): Agent13 V/N/tie {[int((c13[sub] == c).sum()) for c in ('V', 'N', 'tie')]}, lost {int(l13[sub].sum())}; Agent10 V/N/tie {[int((c10[sub] == c).sum()) for c in ('V', 'N', 'tie')]},"
            f" lost {int(l10[sub].sum())}")
    say("   per row with a whiff after engagement: row, first engaged step, first whiff step (u, leg, odour), held at it, outcome Agent10 -> Agent13")
    for r in wr:
        h = o13["H"][tw[r], r]; say(f"      row {r:3d}: engaged {fe[r]}; whiff {tw[r]} (u {tw[r] - fe[r]}, leg {int(leg_of(tw[r] - fe[r]))}, {fo[r]}); held {'nothing' if h < 0 else 'valued' if h == g[r] else 'negative'};"
                                     f" {c10[r]}{' lost' if l10[r] else ''} -> {c13[r]}{' lost' if l13[r] else ''}")

    # (A2)
    say(f"\n(A2) the {len(nw)} engaged stranded rows with no whiff after engagement: positions (the position the step sensed at) relative to both sources")
    for k in (0, 100, 200, 300, "599"):
        rows = [r for r in nw if (k == "599" or fe[r] + k <= LAST)]; ts = [LAST if k == "599" else fe[r] + k for r in rows]
        gs = [geo(o13, t, r) for t, r in zip(ts, rows)]
        say(f"   at {'the first engaged step' if k == 0 else 'step 599' if k == '599' else str(k) + ' steps after it'} ({len(rows)} rows): {geo_summary(gs)}")
    recs = []
    for r in nw:
        t0 = int(fe[r]); rt = region_track(o13, SP, r, t0, LAST); y0 = SP[t0, r, 1]; ym = o13["src"][r, :, 1].mean(); sgn = np.sign(ym - y0)
        dy = (SP[t0:, r, 1] - y0)*sgn; g0, g1 = geo(o13, t0, r), geo(o13, LAST, r); dom, share, L = majority_class(o13, r, t0, LAST)
        iv = int(np.argmin(rt["val"][1])); inn = int(np.argmin(rt["neg"][1]))
        recs.append(dict(r=r, fe=t0, leg=int(o13["LEG"][LAST, r]), u=int(o13["U"][LAST, r]), exc=float(np.abs(SP[t0:, r, 1] - y0).max()), tow=float(dy.max()), awy=float(-dy.min()),
                         cv=float(rt["val"][1].min()), cn=float(rt["neg"][1].min()), uv=iv, un=inn, insv=int(rt["val"][0].sum()), insn=int(rt["neg"][0].sum()), g0=g0, g1=g1, dom=dom, share=share, L=L,
                         c0=pclass(g0), c1=pclass(g1), l1t=leg1_toward_pair(o13, t0, r)))
    arr = lambda k: np.array([x[k] for x in recs], float)
    say(f"   leg reached at step 599 (still engaged: {sum(bool(o13['ENG'][LAST, x['r']]) for x in recs)}/{len(recs)}): " + cnt([x["leg"] for x in recs], range(1, 9)) + f"; u at step 599 {q3(arr('u'))} {mm(arr('u'), '.0f')}")
    say(f"   maximum crosswind excursion from the engagement position |y - y_eng| over the search {q3f(arr('exc'))} {mm(arr('exc'))}; toward the pair's midline {q3f(arr('tow'))}, away from it {q3f(arr('awy'))};"
        f" leg 1 pointed toward the pair's midline {sum(x['l1t'] for x in recs)}/{len(recs)}")
    say(f"   closest approach over the search (engagement to step 599): to the valued region {q3f(arr('cv'))} {mm(arr('cv'))} (u at it {q3(arr('uv'))}), to the negative region {q3f(arr('cn'))} {mm(arr('cn'))}"
        f" (u {q3(arr('un'))}); to either {q3f(np.minimum(arr('cv'), arr('cn')))}; rows entering a whiff region without a whiff drawn: valued {sum(x['insv'] > 0 for x in recs)}, negative {sum(x['insn'] > 0 for x in recs)}"
        f" (steps inside per such row {q3(np.array([x['insv'] + x['insn'] for x in recs if x['insv'] + x['insn'] > 0]))})")
    say(f"   ends (step 599) upwind of both sources {sum(x['g1']['val'][0] < 0 for x in recs)}; beyond LMAX {sum(x['g1']['val'][0] >= LMAX for x in recs)}; 0 <= d_along < 25 {sum(0 <= x['g1']['val'][0] < LMAX for x in recs)}")
    say(f"   position classes (ph26b.pclass, Run 1's categories, in this order: (iv) within {WALL_NEAR} of a wall; (v) inside a whiff region, no whiff drawn; (i) upwind of both, d_along < 0;"
        f" (ii) d_along >= 25; (iii) 0 <= d_along < 25 outside both regions; (vi) no class holds at least half of the steps):")
    for key, lab in (("c0", "at the first engaged step"), ("c1", "at step 599"), ("dom", "majority over the steps from engagement to 599")):
        v = [x[key] for x in recs]; say(f"      {lab}: " + "; ".join(f"{CLS_NAMES[c]} {v.count(c)}" for c in ("i", "ii", "iii", "iv", "v", "vi")))
    say("      at engagement -> at step 599: " + "; ".join(f"({a}) -> ({b}) {n}" for (a, b), n in sorted({(x['c0'], x['c1']): sum(1 for y in recs if y['c0'] == x['c0'] and y['c1'] == x['c1']) for x in recs}.items())))
    tot = {c: sum(x["share"][c]*x["L"] for x in recs) for c in ("i", "ii", "iii", "iv", "v")}; TT = sum(tot.values())
    say(f"      pooled search steps {int(TT)}: " + "; ".join(f"({c}) {int(round(tot[c]))} ({tot[c]/TT:.3f})" for c in ("i", "ii", "iii", "iv", "v")))
    say("   per row: row, first engaged step, at engagement (class, d_along, d_cross valued/negative outward, side, nearest region, wall), at step 599 (the same), leg/u at 599, max excursion toward/away,"
        " closest approach valued/negative, majority class, outcome Agent10 -> Agent13")
    for x in recs:
        r = x["r"]
        say(f"      row {r:3d}: eng {x['fe']}; at eng ({geo_line(x['g0'])}); at 599 ({geo_line(x['g1'])}); leg {x['leg']} u {x['u']}; excursion toward/away {x['tow']:.1f}/{x['awy']:.1f};"
            f" closest valued/negative {x['cv']:.1f}/{x['cn']:.1f}; majority ({x['dom']}); {c10[r]}{' lost' if l10[r] else ''} -> {c13[r]}{' lost' if l13[r] else ''}")

    # (A3)
    say(f"\n(A3) where the two groups start: engaged stranded rows with a whiff after engagement ({len(wr)}) vs without ({len(nw)}), at the first engaged step and at the release")
    for lab, sub in (("whiff after engagement", wr), ("no whiff after engagement", nw)):
        gs = [geo(o13, int(fe[r]), r) for r in sub]; gr = [geo(o13, last_rel_before[r], r) for r in sub]
        tw_ = [toward(fl, hold_start(o13, last_rel_before[r], r), r) for r in sub]; l1 = [leg1_toward_pair(o13, int(fe[r]), r) for r in sub]
        say(f"   [{lab}, {len(sub)}] at engagement: {geo_summary(gs)}")
        say(f"   [{lab}] at the release before engagement: {geo_summary(gr)}")
        say(f"   [{lab}] the released hold's flee side pointed toward the valued source {sum(tw_)}/{len(sub)}; leg 1 pointed toward the pair's midline {sum(l1)}/{len(sub)}; first engaged step {q3(fe[sub])};"
            f" steps left {q3(LAST - fe[sub])}; engaged at step <= 399 {int((fe[sub] <= 399).sum())}")

    l1all = {r: leg1_toward_pair(o13, int(fe[r]), r) for r in se}; sdall = {r: side(geo(o13, int(fe[r]), r)) for r in se}
    for lab, key in (("leg 1 (and so legs 3, 5) toward the pair's midline", lambda r: l1all[r]), ("side of the pair at engagement", lambda r: sdall[r])):
        ks = sorted(set(key(r) for r in se), key=str)
        say(f"   whiff after engagement by {lab}: " + "; ".join(f"{k}: {sum(tw[r] >= 0 for r in se if key(r) == k)}/{sum(1 for r in se if key(r) == k)}" for k in ks))
    say("   whiff after engagement by side x leg 1 toward the midline: " + "; ".join(f"{a}, leg 1 {'toward' if b else 'away'}: {sum(tw[r] >= 0 for r in se if sdall[r] == a and l1all[r] == b)}/{sum(1 for r in se if sdall[r] == a and l1all[r] == b)}"
                                                                          for a in ("beyond valued", "beyond negative") for b in (True, False)))

    fsm = np.array([ph27.flee_side_match(o13, r, 0) for r in r_all]); ee = np.array([r for r in se if fe[r] <= 399], int); el = np.array([r for r in se if fe[r] > 399], int)
    say(f"   leg 1's crosswind side (cast_sign, reading R12) equal to the flee side's (both constant over the run: cast_sign changed in {int((o13['CS'] != o13['CS'][0]).any(0).sum())} rows,"
        f" flee_side in {int((o13['FS'] != o13['FS'][0]).any(0).sum())}): all 400 rows {int(fsm.sum())}/{N}; Agent10-stranded {int(fsm[s10].sum())}/{len(s10)}: engaged at step <= 399 {int(fsm[ee].sum())}/{len(ee)},"
        f" engaged after 399 {int(fsm[el].sum())}/{len(el)}, never engaged {int(fsm[sn].sum())}/{len(sn)}; first release step equal side {q3(np.array([first_rel[r] for r in s10 if fsm[r]]))},"
        f" opposite side {q3(np.array([first_rel[r] for r in s10 if not fsm[r]]))}")
    say(f"   engaged at step <= 399 ({len(ee)}): leg 1 toward the pair's midline {sum(l1all[r] for r in ee)}; whiff after engagement: leg 1 toward {sum(tw[r] >= 0 for r in ee if l1all[r])}/{sum(1 for r in ee if l1all[r])},"
        f" away {sum(tw[r] >= 0 for r in ee if not l1all[r])}/{sum(1 for r in ee if not l1all[r])}; leg 1 on the flee side {int(fsm[ee].sum())} (whiff {sum(tw[r] >= 0 for r in ee if fsm[r])}),"
        f" opposite {int((~fsm[ee]).sum())} (whiff {sum(tw[r] >= 0 for r in ee if not fsm[r])}); engaged after 399 ({len(el)}): whiff {sum(tw[r] >= 0 for r in el)}, leg 1 toward {sum(l1all[r] for r in el)},"
        f" u at step 599 {q3(np.array([LAST - fe[r] for r in el]))}")

    # (A4)
    say(f"\n(A4) the stranded geometry: release -> engagement displacement and the search's d_along, all {len(se)} engaged stranded rows (positions sensed at the step)")
    gr = [geo(o13, last_rel_before[r], r) for r in se]; ge = [geo(o13, int(fe[r]), r) for r in se]
    dx = np.array([SP[fe[r], r, 0] - SP[last_rel_before[r], r, 0] for r in se])
    dyo = np.array([(SP[fe[r], r, 1] - SP[last_rel_before[r], r, 1])*-np.sign(o13["src"][r, :, 1].mean() - SP[last_rel_before[r], r, 1]) for r in se])
    say(f"   at the release: d_along {q3f(np.array([x['val'][0] for x in gr]))}; |d_cross| to the nearer axis {q3f(np.array([nearer(x) for x in gr]))}; inside a whiff region {sum(x['val'][2] or x['oth'][2] for x in gr)}")
    say(f"   release -> first engaged step: along-wind displacement (downwind +) {q3f(dx)} {mm(dx)}; crosswind displacement away from the pair's midline (+ away) {q3f(dyo)} {mm(dyo)}")
    say(f"   at engagement: d_along {q3f(np.array([x['val'][0] for x in ge]))} {mm(np.array([x['val'][0] for x in ge]))}; beyond LMAX {sum(x['val'][0] >= LMAX for x in ge)}; upwind {sum(x['val'][0] < 0 for x in ge)};"
        f" |d_cross| to the nearer axis {q3f(np.array([nearer(x) for x in ge]))}")
    for u in (30, 90, 180, 300, 450):
        rows = [r for r in se if fe[r] + u <= LAST and (tw[r] < 0 or tw[r] > fe[r] + u)]
        if not rows: say(f"   at u {u}: no row"); continue
        da = np.array([geo(o13, int(fe[r] + u), r)["val"][0] for r in rows]); dy = np.array([abs(SP[fe[r] + u, r, 1] - SP[fe[r], r, 1]) for r in rows])
        say(f"   at u {u} (rows still engaged and not yet whiffed, step <= 599: {len(rows)}): d_along {q3f(da)} {mm(da)}; |y - y_eng| {q3f(dy)}")

    for lab, sub in (("whiff after engagement", wr), ("no whiff after engagement", nw)):
        recs_c = []
        for r in sub:
            c_ = cross_near(SP, o13["src"], r, int(fe[r]), LAST); c_ = (c_[0] - int(fe[r]), c_[1]) if c_ else None; recs_c.append((c_, tw[r] - fe[r] if tw[r] >= 0 else -1))
        say(f"   [{lab}, {len(sub)}] after engagement: {cross_summary(recs_c)}")

    # (A4') the bench's (c1) construction, for comparison (walls off, Agent13; the same run as the bench's (c1) primary arm)
    c = ph27.cold("c1", Agent13, False); e = ph27.E_C1; n = c["W"].shape[1]; r_ = np.arange(n); xs = c["src"][:, 0, 0]; ym = c["src"][:, :, 1].mean(1)
    Pc = np.concatenate([c["start"][None], c["POS"][:-1]], 0); w300 = c["W"][e:e + 300].any((0, 2))
    l1c = np.array([bool(np.sign(np.sin(np.radians(search_target(np.array([0.0]), np.array([c["CS"][e, r]]))[0]))) == np.sign(ym[r] - Pc[e, r, 1])) for r in r_])
    say(f"\n(A4') for comparison, the bench's (c1) construction (ph27.cold, walls off, Agent13, {n} rows; engagement at step index {e}): whiff within 300 steps of engagement {wil(int(w300.sum()), n)};"
        f" leg 1 toward the pair's midline {int(l1c.sum())}/{n}; whiff by leg 1 toward {int(w300[l1c].sum())}/{int(l1c.sum())}, away {int(w300[~l1c].sum())}/{int((~l1c).sum())};"
        f" start on the outer side of the valued/negative-coded source index 0/1 (values 0/0): {np.bincount(c['meta']['k'], minlength=2).tolist()}")
    fwc = first_true(c["W"][e:].any(2))
    for lab, m in (("whiff within 300", w300), ("no whiff within 300", ~w300)):
        recs_c = []
        for r in np.flatnonzero(m):
            c_ = cross_near(Pc, c["src"], r, e, e + 299); c_ = (c_[0] - e, c_[1]) if c_ else None; recs_c.append((c_, int(fwc[r])))
        say(f"   (c1) [{lab}, {int(m.sum())}] within 300 steps of engagement: {cross_summary(recs_c)}")
    for u in (0, 30, 90, 180, 300):
        m = ~c["W"][e:e + u + 1].any((0, 2)) if u else np.ones(n, bool); da = Pc[e + u, m, 0] - xs[m]; dy = np.abs(Pc[e + u, m, 1] - Pc[e, m, 1])
        say(f"   (c1) at u {u} (rows not yet whiffed {int(m.sum())}): d_along {q3f(da)} {mm(da)}; |y - y_eng| {q3f(dy)}")

    # (A5)
    ws = np.array([r for r in wr if l13[r]], int)
    say(f"\n(A5) whiff rows that stay lost (lost = no whiff of either plume on steps 400-599): {len(ws)} of {len(wr)}")
    fo_, reneg, restr = neg_after(o13, wr, fe)
    for lab, m in (("first whiff valued", np.array([x == "valued" for x in fo_])), ("first whiff negative", np.array([x == "other" for x in fo_])), ("first whiff both", np.array([x == "both" for x in fo_]))):
        sub = wr[m]
        if len(sub): say(f"   {lab} ({len(sub)}): a negative hold re-formed after engagement {int(reneg[m].sum())}, stranded again {int(restr[m].sum())}; Agent13 V/N/tie {[int((c13[sub] == c).sum()) for c in ('V', 'N', 'tie')]},"
                         f" lost {int(l13[sub].sum())}; out of lost {int((l10[sub] & ~l13[sub]).sum())}")
    for r in ws:
        i = list(wr).index(r); lwh = int(np.flatnonzero(W[:, r])[-1]); dom, _, _ = majority_class(o13, r, 400, LAST)
        say(f"      row {r:3d}: engaged {fe[r]}, whiff {tw[r]} (u {tw[r] - fe[r]}, {fo[r]}); negative hold re-formed {bool(reneg[i])}, stranded again {bool(restr[i])}; last whiff in the row {lwh};"
            f" at step 400 ({geo_line(geo(o13, 400, r))}); at 599 ({geo_line(geo(o13, LAST, r))}); majority class 400-599 ({dom}); engaged at 599 {bool(o13['ENG'][LAST, r])}")

    # (A6)
    say("\n(A6) paired outcomes, all 400 rows (rows Agent10, columns Agent13)")
    for a in ("V", "N", "tie"):
        say(f"      Agent10 {a:3s}: " + "  ".join(f"-> {b} {int(((c10 == a) & (c13 == b)).sum()):3d}" for b in ("V", "N", "tie")))
    iv = (c13 == "V") & (c10 != "V"); ov = (c13 != "V") & (c10 == "V"); il = l13 & ~l10; ol = ~l13 & l10
    say(f"   into V {int(iv.sum())}, out of V {int(ov.sum())} (net {int(iv.sum() - ov.sum()):+d}); into lost {int(il.sum())}, out of lost {int(ol.sum())} (net {int(il.sum() - ol.sum()):+d})")
    s10m = np.isin(r_all, s10); sem = np.isin(r_all, se); snm = np.isin(r_all, sn); enm = np.isin(r_all, en); nev = ~e13
    for lab, m in (("Agent10-stranded rows", s10m), ("  engaged", sem), ("  never engaged", snm), ("not stranded, engaged", enm), ("not stranded, never engaged", ~s10m & nev)):
        say(f"      {lab} ({int(m.sum())}): into V {int((iv & m).sum())}, out of V {int((ov & m).sum())}; into lost {int((il & m).sum())}, out of lost {int((ol & m).sum())}; lost Agent10 {int((l10 & m).sum())}, Agent13 {int((l13 & m).sum())}")
    orow = np.flatnonzero(ol)
    say(f"   the {len(orow)} rows leaving lost: row, Agent10-stranded, first engaged step, first whiff after it (u, leg, odour), first whiff in 400-599 (odour), outcome Agent10 -> Agent13")
    oo = []
    for r in orow:
        f = int(fe[r]); t = int(np.flatnonzero(W[f + 1:, r])[0]) + f + 1 if f >= 0 and W[f + 1:, r].any() else -1; t4 = int(np.flatnonzero(W[400:, r])[0]) + 400
        lab = whiff_lab(o13, t, r) if t >= 0 else "none"; oo.append((r, f, t, lab, whiff_lab(o13, t4, r)))
        say(f"      row {r:3d}: stranded {int(r in rel)}; engaged {f}; first whiff after it {t} (u {t - f if t >= 0 else '-'}, leg {int(leg_of(t - f)) if t >= 0 else '-'}, {lab}); first whiff in 400-599 at {t4} ({whiff_lab(o13, t4, r)});"
            f" {c10[r]} -> {c13[r]}")
    ua = np.array([t - f for r, f, t, _, _ in oo if t >= 0])
    say(f"   rows leaving lost: Agent10-stranded {sum(r in rel for r, *_ in oo)}; first whiff after engagement valued {sum(x[3] == 'valued' for x in oo)}, negative {sum(x[3] == 'other' for x in oo)},"
        f" both {sum(x[3] == 'both' for x in oo)}, none {sum(x[3] == 'none' for x in oo)}; u at it {q3(ua)} {mm(ua, '.0f')}; first whiff in 400-599 valued {sum(x[4] == 'valued' for x in oo)}, negative {sum(x[4] == 'other' for x in oo)},"
        f" both {sum(x[4] == 'both' for x in oo)}; outcome Agent13 V/N/tie {[int((c13[orow] == c).sum()) for c in ('V', 'N', 'tie')]} (Agent10 {[int((c10[orow] == c).sum()) for c in ('V', 'N', 'tie')]})")

    # (A7)
    say("\n(A7) the effect-size chain, measured: Agent10-lost stranded rows -> engaged with >= 200 steps left (first engaged step <= 399) -> a whiff after engagement -> not lost in Agent13")
    L = np.array([r for r in s10 if l10[r]], int); Le = np.array([r for r in L if fe[r] >= 0], int); L2 = np.array([r for r in Le if fe[r] <= 399], int)
    Lw = np.array([r for r in L2 if tw[r] >= 0], int); Lo = np.array([r for r in Lw if not l13[r]], int)
    say(f"   Agent10-lost stranded rows {len(L)}; engaged {len(Le)} ({fr(len(Le), len(L))}); engaged at step <= 399 {len(L2)} ({fr(len(L2), len(L))}); of those, a whiff after engagement {len(Lw)}"
        f" ({fr(len(Lw), len(L2))}); of those, not lost in Agent13 {len(Lo)} ({fr(len(Lo), len(Lw))})")
    Lw_late = [r for r in Le if fe[r] > 399 and tw[r] >= 0]; Lnw = [r for r in L if l10[r] and not l13[r] and r not in set(Lo.tolist())]
    say(f"   also: engaged after step 399 with a whiff {len(Lw_late)}; Agent10-lost stranded rows leaving lost by another route {len(Lnw)} {Lnw}; Agent10-lost stranded rows leaving lost in all {int((l10[s10] & ~l13[s10]).sum())}")
    w300 = np.array([bool(W[fe[r] + 1:min(fe[r] + 300, LAST) + 1, r].any()) for r in se]); full = fe[se] + 299 <= LAST
    say(f"   whiff within 300 steps of engagement (the (c1) (i) window), engaged stranded rows: all {wil(int(w300.sum()), len(se))}; rows with the full window (engaged at step <= 300) {wil(int(w300[full].sum()), int(full.sum()))}")
    w_all = np.array([tw[r] >= 0 for r in se])
    say(f"   whiff at any time after engagement, engaged stranded rows: {wil(int(w_all.sum()), len(se))}; in those engaged at step <= 399 {wil(int(w_all[fe[se] <= 399].sum()), int((fe[se] <= 399).sum()))}")
    P2, dp2, b2, sd2, _ = pp_dp(l13, l10, -0.05, True); se2 = sd2/math.sqrt(N)
    say(f"   reference arithmetic (not measured; design section 7's normal approximation, reading R6, at the bench's lost-row DP {dp2:+.4f}, discordant b {b2:.4f}, sd {sd2:.4f}, se {se2:.4f}):"
        f" pass probability of an upper-bound bar at " + "; ".join(f"{bar:+.3f}: {ph26.Phi((bar - dp2)/se2 - ph26.Z95):.4f}" for bar in (-0.05, -0.045, -0.04, -0.035, -0.03, -0.02))
        + f"; the bar at which it is 0.5: {dp2 + ph26.Z95*se2:+.4f}; 0.8: {dp2 + (ph26.Z95 + 0.841621)*se2:+.4f}")
    return dict(s10=s10, se=se, sn=sn, fe=fe, wr=wr, nw=nw, tw=tw, rel=rel, last_rel=last_rel_before)


# ------------------------------------------------------------------ (B)
def mech(h, w, vc, vo):
    """why the whiff at a step was not a navigation event, by the code (ph21.py:68-72). h = the hold after this step's selection; w = the
    step's whiffs; vc = the valued channel; vo = the other odour's value"""
    held = "nothing" if h < 0 else "valued" if h == vc else "other"; wv, wo = bool(w[vc]), bool(w[1 - vc])
    wl = "both" if wv and wo else "valued" if wv else "other" if wo else "none"
    if held == "nothing" and wl == "other": return "A"
    if held == "other" and vo < 0 and wl == "valued": return "B"
    if held == "valued" and wl == "other": return "C"
    if held == "other" and vo >= 0 and wl == "other": return "D"
    return "E"


MECH = {"A": "nothing held, a whiff of the other odour only: with nothing held nav = (whiffs & top).any(1) (ph21.py:72), and top requires v >= 0 and v = v_max (ph21.py:69),"
             " so a whiff of the negative (or, at +1/0, the neutral) odour is not nav",
        "B": "the negative odour held, a whiff of the valued odour only: keep is True because v_h < 0 (ph21.py:71), so nav = hit (ph21.py:72), and hit is the held odour's whiff"
             " (ph21.py:68), False",
        "C": "the valued odour held, a whiff of the other odour only: keep is True because v_h = v_max (ph21.py:71), nav = hit (ph21.py:72), hit False (ph21.py:68)",
        "D": "the other odour held at a value >= 0 but below v_max (the neutral at +1/0), a whiff of it: keep is False (ph21.py:71), nav = a whiff of a top odour (ph21.py:72), and"
             " the held odour is not top (ph21.py:69)",
        "E": "other combination"}


def odour_of(w, vc):
    wv, wo = bool(w[vc]), bool(w[1 - vc]); return "both" if wv and wo else "valued" if wv else "other" if wo else "none"


def held_of(h, vc): return "nothing" if h < 0 else "valued" if h == vc else "other"


def row_since(o, r, t, vc, vo):
    """at step t: q, since, the last whiff step (<= t) and the last navigation step (<= t), and what each was"""
    Wr = o["W"][:, r].any(1); nav = o["NAV"][:, r]
    lw = int(np.flatnonzero(Wr[:t + 1])[-1]) if Wr[:t + 1].any() else -1; ln = int(np.flatnonzero(nav[:t + 1])[-1]) if nav[:t + 1].any() else -1
    d = dict(q=int(o["Q"][t, r]) if "Q" in o and o["Q"][t, r] >= 0 else None, since=int(o["SINCE"][t, r]), lw=lw, ln=ln)
    d["w_od"] = odour_of(o["W"][lw, r], vc) if lw >= 0 else "none"; d["w_held"] = held_of(o["H"][lw, r], vc) if lw >= 0 else "-"; d["w_nav"] = bool(nav[lw]) if lw >= 0 else False
    d["n_od"] = odour_of(o["W"][ln, r], vc) if ln >= 0 else "none"; d["n_held"] = held_of(o["H"][ln, r], vc) if ln >= 0 else "-"
    d["m"] = mech(o["H"][lw, r], o["W"][lw, r], vc, vo) if lw >= 0 else "E"
    return d


def part_b(o13, o10, b2, A, T):
    say("\n== (B) `since` - q at the first engaged step: which whiff was not a navigation event, by the code ==")
    say("   the mechanisms (h = the hold after the step's selection, as recorded; the whiff = the last whiff before the engagement silence, i.e. the step at which q last reset):")
    for k in ("A", "B", "C", "D", "E"): say(f"      ({k}) {MECH[k]}")
    say("   q resets on any whiff (ph26.py:90); `since` resets only on nav (ph21.py:75); so `since` - q = (last whiff step) - (last nav step), and it is > 0 iff the last whiff was not nav")
    g = o13["good"]; se, fe = A["se"], A["fe"]; c13, c10 = outcome(o13), outcome(o10); l13, l10 = lost(o13), lost(o10)
    recs = {}
    for r in se: recs[r] = row_since(o13, r, int(fe[r]), int(g[r]), -1.0)
    dsq = np.array([recs[r]["since"] - recs[r]["q"] for r in se]); chk = all((recs[r]["since"] - recs[r]["q"]) == (recs[r]["lw"] - recs[r]["ln"]) for r in se)
    pos = np.array([r for r, d in zip(se, dsq) if d > 0], int); zer = np.array([r for r, d in zip(se, dsq) if d == 0], int)
    say(f"\n(B1) task, T3 +1/-1: the {len(se)} engaged Agent10-stranded rows; `since` - q at the first engaged step {q3(dsq)} {mm(dsq, '.0f')}; 0 in {len(zer)}, > 0 in {len(pos)}, < 0 in {int((dsq < 0).sum())};"
        f" identity `since` - q == last whiff step - last nav step in every row: {chk}")
    say("   the last whiff before the engagement silence, all engaged stranded rows (held at it / odour; nav or not):")
    for lab, sub in (("`since` - q = 0", zer), ("`since` - q > 0", pos)):
        combos = {}
        for r in sub:
            d = recs[r]; k = f"held {'negative' if d['w_held'] == 'other' else d['w_held']}, whiff {'negative' if d['w_od'] == 'other' else d['w_od']}, nav {int(d['w_nav'])}"; combos[k] = combos.get(k, 0) + 1
        say(f"      {lab} ({len(sub)}): " + "; ".join(f"{k} {v}" for k, v in sorted(combos.items())))
    ms = [recs[r]["m"] for r in pos]
    say(f"   `since` - q > 0 ({len(pos)}) by mechanism: " + "; ".join(f"({k}) {ms.count(k)}" + (f" [`since` - q {q3(np.array([recs[r]['since'] - recs[r]['q'] for r in pos if recs[r]['m'] == k]))}]" if ms.count(k) else "") for k in ("A", "B", "C", "D", "E")))
    # relation of the last whiff to the negative hold released before engagement
    rel_k = []
    for r in pos:
        e = A["last_rel"][r]; hs = hold_start(o13, e, r); lw = recs[r]["lw"]
        rel_k.append("after the release" if lw >= e else "before the released hold formed" if lw < hs else "during the released hold")
    say("   where that last whiff falls relative to the drive-ended negative hold released before engagement: " + "; ".join(f"{k} {rel_k.count(k)}" for k in sorted(set(rel_k))))
    nk = [("none since construction" if recs[r]["ln"] < 0 else f"held {'negative' if recs[r]['n_held'] == 'other' else recs[r]['n_held']}, whiff {'negative' if recs[r]['n_od'] == 'other' else recs[r]['n_od']}") for r in pos]
    say("   the last nav event before engagement, `since` - q > 0 rows: " + "; ".join(f"{k} {nk.count(k)}" for k in sorted(set(nk))))
    neg_ = 1 - g
    for lab, sub in (("`since` - q > 0", pos), ("`since` - q = 0", zer)):
        hs_ = np.array([hold_start(o13, A["last_rel"][r], r) for r in sub]); lw_ = np.array([recs[r]["lw"] for r in sub]); e_ = np.array([A["last_rel"][r] for r in sub])
        hits = np.array([int(o13["W"][h:e, r, neg_[r]].sum()) for h, e, r in zip(hs_, e_, sub)]); fw = np.array([bool(o13["W"][h, r, neg_[r]]) for h, r in zip(hs_, sub)])
        say(f"   [{lab}, {len(sub)}] the released negative hold: formed at step {q3(hs_)}; steps from the last whiff to the formation {q3(hs_ - lw_)} {mm(hs_ - lw_, '.0f')}; a negative whiff on the formation step {int(fw.sum())};"
            f" negative hits while held {q3(hits)} {mm(hits, '.0f')} (rows with none {int((hits == 0).sum())}); release - formation {q3(e_ - hs_)}; release - last whiff {q3(e_ - lw_)}")
    say("   per row (`since` - q > 0): row, first engaged step, `since` - q, last whiff (step, held, odour, nav), last nav (step, held, odour), the released hold (formed, released), mechanism, whiff after engagement, outcome")
    for r, k in zip(pos, rel_k):
        d = recs[r]; e = A["last_rel"][r]; hs = hold_start(o13, e, r)
        say(f"      row {r:3d}: eng {fe[r]}; since - q {d['since'] - d['q']}; last whiff {d['lw']} (held {'negative' if d['w_held'] == 'other' else d['w_held']}, {'negative' if d['w_od'] == 'other' else d['w_od']}, nav {int(d['w_nav'])}); last nav {d['ln']}"
            f" (held {'negative' if d['n_held'] == 'other' else d['n_held']}, {'negative' if d['n_od'] == 'other' else d['n_od']}); released hold {hs}-{e - 1}, release {e} ({k}); ({d['m']}); whiff after engagement {A['tw'][r] if A['tw'][r] >= 0 else 'none'};"
            f" {c10[r]}{' lost' if l10[r] else ''} -> {c13[r]}{' lost' if l13[r] else ''}")
    # engagement offset and positions by group
    for lab, sub in (("`since` - q = 0", zer), ("`since` - q > 0", pos)):
        off = np.array([fe[r] - A["last_rel"][r] for r in sub]); w_ = np.array([A["tw"][r] >= 0 for r in sub]); fo = [whiff_lab(o13, A["tw"][r], r) for r in sub if A["tw"][r] >= 0]
        da = np.array([geo(o13, int(fe[r]), r)["val"][0] for r in sub])
        say(f"\n(B2) [{lab}, {len(sub)}] first engaged step {q3(fe[sub])}; - the last release {q3(off)} (equal to 202: {int((off == 202).sum())}); d_along at engagement {q3f(da)};"
            f" a whiff after engagement {wil(int(w_.sum()), len(sub))} (valued {fo.count('valued')}, negative {fo.count('other')}, both {fo.count('both')}); out of lost {int((l10[sub] & ~l13[sub]).sum())};"
            f" Agent13 V {int((c13[sub] == 'V').sum())}, lost {int(l13[sub].sum())}; Agent10 V {int((c10[sub] == 'V').sum())}, lost {int(l10[sub].sum())}; into V {int(((c13[sub] == 'V') & (c10[sub] != 'V')).sum())}")
    # (b'2)
    say("\n(B1') the (b'2) constructed stranded state (ph27.stub, values +1/-1, 20 steps of the negative channel at p 0.30, then silence; valued channel 0, negative channel 1)")
    feb = first_true(b2["ENG"]); rb = np.flatnonzero(feb >= 0); br = {r: row_since(b2, r, int(feb[r]), 0, -1.0) for r in rb}
    db = np.array([br[r]["since"] - br[r]["q"] for r in rb]); nz = [r for r in rb if br[r]["since"] != br[r]["q"]]
    formed = (b2["H"] == 1).any(0)
    say(f"   engaged rows {len(rb)}; `since` - q {q3(db)} {mm(db, '.0f')}; 0 in {int((db == 0).sum())}, non-zero in {len(nz)}; identity with last whiff - last nav: {all((br[r]['since'] - br[r]['q']) == (br[r]['lw'] - br[r]['ln']) for r in rb)};"
        f" negative hold formed {int(formed.sum())}/{len(rb)}")
    mb = [br[r]["m"] for r in nz]
    say(f"   non-zero rows by mechanism: " + "; ".join(f"({k}) {mb.count(k)}" for k in ("A", "B", "C", "D", "E")) + f"; last nav: none since construction {sum(br[r]['ln'] < 0 for r in nz)}")
    for r in nz:
        d = br[r]; H = b2["H"][:, r]; fh = int(np.flatnonzero(H == 1)[0]) if (H == 1).any() else -1; he = int(np.flatnonzero((H != 1) & (np.arange(len(H)) > fh))[0]) if fh >= 0 else -1
        ws = np.flatnonzero(b2["W"][:, r].any(1)); navs = np.flatnonzero(b2["NAV"][:, r])
        say(f"      row {r:3d}: since - q {d['since'] - d['q']}; whiff steps {ws.tolist()}; nav steps {navs.tolist()}; " + (f"negative hold {fh}-{he - 1 if he >= 0 else 'end'}" if fh >= 0 else "no negative hold formed")
            + f"; last whiff {d['lw']} (held {d['w_held']}), ({d['m']})")
    zb = [r for r in rb if br[r]["since"] == br[r]["q"]]
    fhz = np.array([int(np.flatnonzero(b2["H"][:, r] == 1)[0]) - int(np.flatnonzero(b2["W"][:, r].any(1))[0]) for r in zb if (b2["H"][:, r] == 1).any()])
    fhn = np.array([int(np.flatnonzero(b2["H"][:, r] == 1)[0]) - int(np.flatnonzero(b2["W"][:, r].any(1))[0]) for r in nz if (b2["H"][:, r] == 1).any()])
    lwz = np.array([br[r]["lw"] for r in zb]); lwn = np.array([br[r]["lw"] for r in nz])
    say(f"   steps from the first whiff to the hold's formation: `since` - q = 0 rows {q3(fhz)} {mm(fhz, '.0f')}; non-zero rows {q3(fhn)} {mm(fhn, '.0f') if len(fhn) else ''}; last whiff step {q3(lwz)} vs {q3(lwn)}")

    # (B3) the T1 +1/0 silences on the same bench seeds, for reference
    say("\n(B3) for reference, T1 +1/0 on the same bench seeds: `since` - q where Agent10's any-odour silence reaches q 210 and at Agent13's engagement")
    a13, a10 = T[("Agent13", (1.0, 0.0))], T[("Agent10", (1.0, 0.0))]; g1 = a10["good"]; Q10 = qrec(a10["W"]); rows = np.flatnonzero(Q10.max(0) >= 210)
    t10 = {r: int(np.argmax(Q10[:, r] >= 210)) for r in rows}
    o10q = dict(a10); o10q["Q"] = Q10
    rr = {r: row_since(o10q, r, t10[r], int(g1[r]), 0.0) for r in rows}; d10 = np.array([rr[r]["since"] - rr[r]["q"] for r in rows])
    say(f"   Agent10 rows reaching q >= 210: {len(rows)}; `since` - q at that step {q3(d10)} {mm(d10, '.0f')}; 0 in {int((d10 == 0).sum())}/{len(rows)}; last whiff valued {sum(rr[r]['w_od'] == 'valued' for r in rows)},"
        f" other (neutral) {sum(rr[r]['w_od'] == 'other' for r in rows)}, both {sum(rr[r]['w_od'] == 'both' for r in rows)}; non-zero rows by mechanism " + cnt([rr[r]['m'] for r in rows if rr[r]['since'] != rr[r]['q']], ("A", "B", "C", "D", "E")))
    for r in rows:
        if rr[r]["since"] != rr[r]["q"]:
            d = rr[r]; say(f"      row {r:3d}: q 210 at step {t10[r]}; since - q {d['since'] - d['q']}; last whiff {d['lw']} (held {d['w_held']}, {d['w_od']}); last nav {d['ln']} (held {d['n_held']}, {d['n_od']}); ({d['m']})")
    fe1 = first_true(a13["ENG"]); er = np.flatnonzero(fe1 >= 0); ra = {r: row_since(a13, r, int(fe1[r]), int(g1[r]), 0.0) for r in er}
    say(f"   Agent13 engaged rows {len(er)} {er.tolist()}: `since` - q at the first engaged step {[ra[r]['since'] - ra[r]['q'] for r in er]}; last whiff {[ra[r]['w_od'] for r in er]} (held {[ra[r]['w_held'] for r in er]});"
        f" mechanism of the non-zero {[ra[r]['m'] for r in er if ra[r]['since'] != ra[r]['q']]}")
    # the last whiffed odour's value sign (design section 3.1 (b4) quantity)
    lv = [recs[r]["w_od"] for r in se]
    say(f"   the last whiffed odour before the engagement silence (the quantity a one-bit valence memory, design section 3.1 (b4), would hold): T3 engaged stranded rows negative {lv.count('other')},"
        f" valued {lv.count('valued')}, both {lv.count('both')} of {len(se)}; T1 +1/0 rows reaching q 210 valued {sum(rr[r]['w_od'] == 'valued' for r in rows)}, neutral {sum(rr[r]['w_od'] == 'other' for r in rows)} of {len(rows)}"
        f" (none negative: the T1 world has no negative odour)")
    say(f"   T3 engaged stranded rows by `since` - q and the last whiffed odour: " + "; ".join(f"{a}, last whiff {b} {sum(1 for r, d in zip(se, dsq) if ((d == 0) == (a == '= 0')) and ('negative' if recs[r]['w_od'] == 'other' else recs[r]['w_od']) == b)}"
                                                                                   for a in ("= 0", "> 0") for b in ("negative", "valued", "both")))


def main():
    mods = ph27.MODS + (ph27,)
    say(f"== H17 Run 2 post-bench diagnosis (measurement only; owner 2026-09-24, '2번 진단 먼저 진행'). ph27b.py sha256 {sha()}; ph27.py sha256 {sha(ph27.__file__)}; ph26.py sha256 {sha(ph26.__file__)};"
        f" design {ph27.DESIGN}; reproduces experiments/h17/ph27_bench.txt sha256 {BENCH_TXT_SHA} (record:h17-run2-bench-result) ==")
    say("   imported modules (unchanged): " + "; ".join(f"{os.path.basename(m.__file__)} {sha(m.__file__)}" for m in mods))
    say("   bench seeds only (ph27.BS, bootstrap seed as ph27 sets it; not written out here); development and evaluation seeds untouched. Nothing is changed or adopted; the H17 Run 2 verdict"
        " (stopped at the bench by the (h2) stop rule, no bar decision) is not re-judged; S, gamma, L0, U1 and every bar as registered; no sweep; no new agent variant")
    say(f"   S {S_RUN2}; walls 160 apart (World7); 'at a wall' = within {WALL_NEAR} of a wall; LMAX {LMAX:.0f}; whiff region = the cone 0 < d_along < 25, |d_cross| < 1.5 + 0.25 d_along, or within 3.0 of a source")
    res = reproduce()
    if res is None:
        say("== reproduction FAILED: nothing measured =="); return 1
    T, b2 = res
    A = part_a(T[("Agent13", (1.0, -1.0))], T[("Agent10", (1.0, -1.0))])
    part_b(T[("Agent13", (1.0, -1.0))], T[("Agent10", (1.0, -1.0))], b2, A, T)
    say("\n== end (measurement only; positions, counts and code lines, no cause named; no change tested; bench seeds only) ==")
    return 0


if __name__ == "__main__":
    rc = main()
    with open(OUT, "w", encoding="utf-8", newline="\n") as f: f.write("\n".join(_lines) + "\n")
    hits, _, nf = ph27.seeds_unused()
    print(f"[written {OUT}; sha256 {sha(OUT)}; ph27's seed self-check after writing it: no H17 Run 2 seed in any other file {not hits} ({nf} files scanned){'' if not hits else ' ' + str(hits)}]")
    sys.exit(rc)
