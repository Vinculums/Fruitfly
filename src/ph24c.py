#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R3 diagnosis: where the H25 release loses the valued outcome under supplied values +1/-1 (measurement only).

Usage: python ph24c.py      (output experiments/avoidance_check/ph24c_diag.txt, LF)

Owner, 2026-09-24 ('1 -> 2(a) -> 3.4.5', point 1): a measurement-only diagnosis of the avoidance check's R3 result.
ph24 and ph24b are imported unchanged; the runs are ph24b's R3 runs (ph24.run('T1', cls, (+1, -1), (1805, 1905)) with
ph24b's record hook, which adds the flee side per step and leaves every other field bitwise equal). The recorded R3
counts are asserted before anything is measured; on a mismatch the script stops. No new seed, no new rule, no change tested.
Agent10 (Release + Agent8) against Agent8; at +1/-1 Agent10 == Agent10g and Agent8 == Agent6 bitwise (R0), so one pair.
"""
import sys, os, hashlib
import numpy as np
import ph24, ph24b
from ph24 import Agent10, Agent8, run, events, on_hold, first_true, T
from ph24b import VALS, EVAL, arm_stats, neg_events, neg_held
from ph9 import W0, SLOPE, LMAX, HIT_R

sys.stdout.reconfigure(newline="\n")
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def q(x, f=".1f"): return "n/a" if len(x) == 0 else f"{np.percentile(x, 25):{f}}/{np.median(x):{f}}/{np.percentile(x, 75):{f}}"
def frac(k, n): return f"{k}/{n} = {k / n:.3f}" if n else f"{k}/0"
HERE = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------------------ geometry (the World2.sense cone, ph11)
def cone_geom(da, dc):
    """inside the whiff region of one source (cone or within 3.0), and the distance to it (0 inside). da = x - x_src, dc = y - y_src."""
    inside = ((da > 0) & (da < LMAX) & (np.abs(dc) < W0 + SLOPE*da)) | (np.hypot(da, dc) < 3.0)
    P = np.array([[0.0, -W0], [LMAX, -(W0 + SLOPE*LMAX)], [LMAX, W0 + SLOPE*LMAX], [0.0, W0]])      # the cone as a trapezoid
    p = np.stack([da, dc], -1); d = np.full(da.shape, np.inf)
    for i in range(4):
        a, b = P[i], P[(i + 1) % 4]; ab = b - a
        t = np.clip(((p - a) @ ab)/(ab @ ab), 0.0, 1.0)
        d = np.minimum(d, np.linalg.norm(p - (a + t[..., None]*ab), axis=-1))
    d = np.minimum(d, np.maximum(np.hypot(da, dc) - 3.0, 0.0))
    return inside, np.where(inside, 0.0, d)


def rel(o, t, r):
    """position used by step t's sense (the position after step t - 1's move; the start for t = 0), relative to both sources"""
    pos = o["POS"][t - 1, r] if t > 0 else o["start"][r]
    g = o["good"][r]; out = {}
    for lab, k in (("val", g), ("neg", 1 - g)):
        da, dc = pos[0] - o["src"][r, k, 0], pos[1] - o["src"][r, k, 1]
        ins, dist = cone_geom(np.array(da), np.array(dc)); out[lab] = (float(da), float(dc), bool(ins), float(dist))
    return out


def inside_any(o):
    """(steps, rows): the position used by each step's sense lies inside either whiff region"""
    P = np.concatenate([o["start"][None], o["POS"][:-1]], 0); n = P.shape[1]; r = np.arange(n); ins = np.zeros(P.shape[:2], bool); dist = np.full(P.shape[:2], np.inf)
    for k in (0, 1):
        i, d = cone_geom(P[:, :, 0] - o["src"][r, k, 0][None], P[:, :, 1] - o["src"][r, k, 1][None]); ins |= i; dist = np.minimum(dist, d)
    return ins, dist


# ------------------------------------------------------------------ reproduction
def reproduce(o):
    ok = True
    for k, want in (("Agent10", (306, 27, 67, 127, 0.000)), ("Agent8", (370, 16, 14, 33, 0.307))):
        V, N, Z, _, lost = arm_stats(o[k]); got = (int(V.sum()), int(N.sum()), int(Z.sum()), int(lost.sum()), round(float(o[k]["contacts"].mean()), 3))
        m = got == want; ok &= m; print(f"   {k} V/N/tie, lost rows, wall contacts per row: got {got}, recorded {want} -> {'MATCH' if m else 'MISMATCH'}")
    for k, want in (("Agent10", (237, 236, 131)), ("Agent8", (200, 168, 0))):
        e = neg_events(o[k]); got = (e["formed"], e["ended"], e["by_drive"]); m = got == want; ok &= m
        print(f"   {k} negative holds formed / ended / ended by the drive: got {got}, recorded {want} -> {'MATCH' if m else 'MISMATCH'}")
    return ok


# ------------------------------------------------------------------ measurements
def cls_of(o):
    V, N, Z = ph24.majority(o); return np.select([V, N], ["V", "N"], "tie")


def released(o):
    """Agent10's drive-ended negative holds: (release step e, row r)"""
    dr = events(o)["drives"]; neg = 1 - o["good"]; m = on_hold(dr) & (dr["hp"] == neg[dr["r"]]) & dr["ended"]
    return dr["end"][m], dr["r"][m], dr["t"][m]


def part_a(o, say):
    say("\n== A. Agent10: the drive-ended negative holds (release step e = the step on which nothing is held after the drive; position = the position step e sensed at) ==")
    E, Rr, Tt = released(o); n = len(E); H, W, AT = o["H"], o["W"], o["AT2"]; g = o["good"]; C = cls_of(o); lost = arm_stats(o)[4]
    ins_all, _ = inside_any(o)
    geo = [rel(o, e, r) for e, r in zip(E, Rr)]
    iv = np.array([x["val"][2] for x in geo]); ineg = np.array([x["neg"][2] for x in geo]); dmin = np.array([min(x["val"][3], x["neg"][3]) for x in geo])
    S0 = np.array([hold_start(o, e, r) for e, r in zip(E, Rr)]); tw = np.array([toward(o, s, r) for s, r in zip(S0, Rr)])
    say(f"   events {n} in {len(np.unique(Rr))} rows (max per row {np.bincount(Rr).max()}); hold formed at step {q(S0, '.0f')}; drive start {q(Tt, '.0f')}; release step {q(E, '.0f')};"
        f" hold length to the release {q(E - S0, '.0f')}; held on the release step: nothing {int((H[E, Rr] < 0).sum())}/{n};"
        f" flee side at the hold's formation points toward the valued source {int(tw.sum())}/{n}, away {int((~tw).sum())}/{n}")
    vs = np.array([abs(x["val"][1]) < abs(x["neg"][1]) for x in geo])
    say(f"   at the release the agent is beyond the valued source (nearer the valued axis than the negative one) {int(vs.sum())}/{n} (flee toward the valued source {int((vs & tw).sum())}/{int(tw.sum())}),"
        f" beyond the negative source {int((~vs).sum())}/{n} (flee away {int((~vs & ~tw).sum())}/{int((~tw).sum())}); |d_cross| to the nearer axis {q(np.array([min(abs(x['val'][1]), abs(x['neg'][1])) for x in geo]))}")
    for lab in ("val", "neg"):
        da = np.array([x[lab][0] for x in geo]); dc = np.array([x[lab][1] for x in geo]); ds = np.array([x[lab][3] for x in geo])
        say(f"   relative to the {'valued (+1)' if lab == 'val' else 'negative (-1)'} source: d_along {q(da)} (downwind > 0; upwind of the source {int((da < 0).sum())}),"
            f" |d_cross| {q(np.abs(dc))}; inside its whiff region {int(np.array([x[lab][2] for x in geo]).sum())}/{n}; distance to it when outside {q(ds[ds > 0])}")
    say(f"   inside either whiff region at the release: {int((iv | ineg).sum())}/{n}; outside both {int((~iv & ~ineg).sum())}/{n}; distance to the nearest region, outside rows {q(dmin[dmin > 0])}, max {dmin.max():.1f};"
        f" beyond the cone's far end (d_along to both > {LMAX:.0f}) {int(np.array([min(x['val'][0], x['neg'][0]) > LMAX for x in geo]).sum())}")
    res = {}
    for w in (60, 200):
        full = E + w < T; wh = np.array([bool(W[e + 1:e + 1 + w, r].any()) for e, r in zip(E, Rr)])
        wv = np.array([bool(W[e + 1:e + 1 + w, r, g[r]].any()) for e, r in zip(E, Rr)]); wn = np.array([bool(W[e + 1:e + 1 + w, r, 1 - g[r]].any()) for e, r in zip(E, Rr)])
        reent = np.array([bool(ins_all[e + 1:e + 1 + w, r].any()) for e, r in zip(E, Rr)])
        reach = np.array([bool(AT[e:e + w, r].any()) for e, r in zip(E, Rr)])
        hl = np.array([H[e + w, r] if e + w < T else -9 for e, r in zip(E, Rr)])
        held = [int(((hl >= 0) & (hl == g[Rr])).sum()), int(((hl >= 0) & (hl != g[Rr])).sum()), int((hl == -1).sum())]
        dd = [min(x["val"][3], x["neg"][3]) for x in (rel(o, e + w, r) for e, r in zip(E, Rr) if e + w < T)]
        res[w] = (wh, reent)
        say(f"   within {w} steps after the release (windows cut by the run's end {int((~full).sum())}): any whiff {int(wh.sum())}/{n} (valued {int(wv.sum())}, negative {int(wn.sum())});"
            f" re-entered a whiff region {int(reent.sum())}/{n}; reached a source {int(reach.sum())}/{n}; held at e + {w} (full windows) valued/negative/nothing {held};"
            f" distance to the nearest region at e + {w} {q(np.array(dd))} (inside {int((np.array(dd) == 0).sum())}/{len(dd)})")
    rest_w = np.array([bool(W[e + 1:, r].any()) for e, r in zip(E, Rr)]); rest_in = np.array([bool(ins_all[e + 1:, r].any()) for e, r in zip(E, Rr)])
    rest_v = np.array([bool(AT[e:, r, g[r]].any()) for e, r in zip(E, Rr)]); rest_n = np.array([bool(AT[e:, r, 1 - g[r]].any()) for e, r in zip(E, Rr)])
    say(f"   until the run's end: any whiff {int(rest_w.sum())}/{n}; re-entered a whiff region {int(rest_in.sum())}/{n}; reached the valued source {int(rest_v.sum())}/{n}, the negative source {int(rest_n.sum())}/{n}")
    last = np.zeros(400, bool); last[Rr[np.argsort(E)]] = True                                                   # rows with at least one event
    li = {r: E[Rr == r].max() for r in np.unique(Rr)}                                                          # the row's last release
    ur = np.array(sorted(li)); lr = np.array([li[r] for r in ur])
    vv_before = np.array([bool(AT[:li[r], r, g[r]].any()) for r in ur])
    say(f"   per row (the row's last release, {len(ur)} rows): final class V/N/tie {[int((C[ur] == c).sum()) for c in ('V', 'N', 'tie')]}; lost rows {frac(int(lost[ur].sum()), len(ur))};"
        f" rows without any event: lost {frac(int(lost[~last].sum()), int((~last).sum()))}, class V/N/tie {[int((C[~last] == c).sum()) for c in ('V', 'N', 'tie')]};"
        f" of all 127 lost rows, with an event {int((lost & last).sum())}; valued source reached before the last release {int(vv_before.sum())}/{len(ur)};"
        f" no whiff at all after the last release {int(np.array([not W[e + 1:, r].any() for r, e in zip(ur, lr)]).sum())}/{len(ur)}")
    return ur


def hold_start(o, e, r):
    """first step of the hold that ends at step e"""
    h = o["H"][:, r]; s = e - 1
    while s > 0 and h[s - 1] == h[e - 1]: s -= 1
    return s


def toward(o, s, r):
    """the flee side (90 = +y, 270 = -y) at step s points toward the valued source (World7: the valued source is at +y of the other iff plus_y == good)"""
    return bool((o["FLEE"][s, r] == 90.0) == (o["plus_y"][r] == o["good"][r]))


def neg_segments(o):
    """negative-hold segments: (row, start, end step or -1, how it ended). End step = first step not holding it; kind: 'evidence' if EV on the end step,
    'drive' if a timeout drive (TO or SUS) is on it, else 'other'."""
    H = o["H"]; neg = 1 - o["good"]; out = []
    for r in range(H.shape[1]):
        h = H[:, r]; t = 0
        while t < T:
            if h[t] != neg[r]: t += 1; continue
            s = t
            while t < T and h[t] == neg[r]: t += 1
            e = t if t < T else -1
            kind = "open" if e < 0 else "evidence" if o["EV"][e, r] else "drive" if (o["TO"][e, r] or o["SUS"][e - 1, r]) else "base timeout on the step before" if o["TO"][e - 1, r] else "other"
            out.append((r, s, e, kind))
    return out


def part_b(o, o10, say):
    say("\n== B. Agent8: negative holds, wall contacts, and P(V | wall contact) ==")
    seg = neg_segments(o); C = o["C"]; P = o["POS"]; cls = cls_of(o); cls10 = cls_of(o10); g = o["good"]
    kinds = {k: sum(1 for x in seg if x[3] == k) for k in ("evidence", "drive", "base timeout on the step before", "other", "open")}
    say(f"   negative-hold segments {len(seg)} (incl. any held at construction), ended by kind {kinds}")
    ended = [x for x in seg if x[3] == "evidence"]
    wc = np.array([bool(C[s:e, r].any()) for r, s, e, _ in ended]); tfc = np.array([int(np.argmax(C[s:e, r])) for r, s, e, _ in ended if C[s:e, r].any()])
    dur = np.array([e - s for r, s, e, _ in ended]); ncont = np.array([int(C[s:e, r].sum()) for r, s, e, _ in ended])
    dy = np.array([abs(P[e - 1, r, 1] - (P[s - 1, r, 1] if s > 0 else o["start"][r, 1])) for r, s, e, _ in ended])
    ymax = np.array([np.abs(P[s:e, r, 1] - (P[s - 1, r, 1] if s > 0 else o["start"][r, 1])).max() for r, s, e, _ in ended])
    say(f"   evidence-ended negative holds {len(ended)}: a wall contact during the hold before the release {frac(int(wc.sum()), len(ended))} (contacts per hold {q(ncont, '.0f')});"
        f" hold start -> first wall contact {q(tfc, '.0f')} steps; hold start -> evidence release {q(dur, '.0f')} steps (with a contact {q(dur[wc], '.0f')}, without {q(dur[~wc], '.0f')})")
    tw = np.array([toward(o, s, r) for r, s, e, _ in ended])
    say(f"   flee side at the hold's formation toward the valued source {int(tw.sum())}/{len(ended)}: with a wall contact before the release {int((tw & wc).sum())}, without {int((tw & ~wc).sum())};"
        f" away {int((~tw).sum())}: with a contact {int((~tw & wc).sum())}, without {int((~tw & ~wc).sum())}; hold start -> release, toward {q(dur[tw], '.0f')}, away {q(dur[~tw], '.0f')}")
    say(f"   crosswind displacement over the hold |y_end - y_start| {q(dy)} (with a contact {q(dy[wc])}, without {q(dy[~wc])}); largest crosswind excursion during the hold {q(ymax)}")
    op = [x for x in seg if x[3] == "open"]
    say(f"   negative holds still held at step 599: {len(op)}; wall contacts during them {q(np.array([int(C[s:, r].sum()) for r, s, _, _ in op]), '.0f')}")
    # where the evidence release happens relative to the plumes
    geo = [rel(o, e, r) for r, s, e, _ in ended]
    say(f"   at the evidence release: inside the valued whiff region {sum(x['val'][2] for x in geo)}/{len(ended)}, inside the negative one {sum(x['neg'][2] for x in geo)}/{len(ended)};"
        f" d_cross to the valued axis {q(np.abs([x['val'][1] for x in geo]))}, d_along {q(np.array([x['val'][0] for x in geo]))}")
    anyc = o["contacts"] > 0; V = cls == "V"; V10 = cls10 == "V"
    k1, n1, k0, n0 = int((V & anyc).sum()), int(anyc.sum()), int((V & ~anyc).sum()), int((~anyc).sum())
    import ph15
    _, lo1, hi1 = ph15.wilson(k1, n1); _, lo0, hi0 = ph15.wilson(k0, n0)
    say(f"   rows with >= 1 wall contact: Agent8 {n1}/400, Agent10 {int((o10['contacts'] > 0).sum())}/400")
    say(f"   Agent8 P(V | any wall contact) {k1}/{n1} = {k1 / n1:.3f} [{lo1:.3f}, {hi1:.3f}]; P(V | no wall contact) {k0}/{n0} = {k0 / n0:.3f} [{lo0:.3f}, {hi0:.3f}]")
    say(f"   paired on the same rows: in Agent8's no-contact rows Agent8 V {k0}/{n0}, Agent10 V {int((V10 & ~anyc).sum())}/{n0}; in Agent8's contact rows Agent8 V {k1}/{n1}, Agent10 V {int((V10 & anyc).sum())}/{n1}")
    out = V & ~V10
    say(f"   the 64 rows that leave V: Agent8 had a wall contact in {int((out & anyc).sum())}/{int(out.sum())}")
    fc = first_true(C); fv = first_true(o["H"] == g[None, :]); fva = first_true(o["AT2"][:, np.arange(400), g])
    m = V & (fv >= 0)
    say(f"   Agent8 V rows {int(V.sum())}: first valued hold after the first wall contact {int((m & (fc >= 0) & (fc < fv)).sum())}/{int(m.sum())};"
        f" first arrival at the valued source after the first wall contact {int((V & (fc >= 0) & (fc < fva)).sum())}/{int(V.sum())}")
    negc = neg_held(o) & C
    say(f"   Agent8 wall contacts {int(C.sum())} in total, while holding the negative odour {int(negc.sum())}, while holding the valued odour {int(((o['H'] == g[None, :]) & C).sum())}, holding nothing {int(((o['H'] < 0) & C).sum())}")
    return anyc


def part_c(o10, o8, say):
    say("\n== C. The 64 paired rows that move out of V (Agent8 V, Agent10 not V) ==")
    c10, c8 = cls_of(o10), cls_of(o8); rows = np.flatnonzero((c8 == "V") & (c10 != "V")); g = o10["good"]
    def first_diff(ks):
        eq = np.ones(o10["H"].shape, bool)
        for k in ks:
            e = o10[k] == o8[k]; eq &= e.reshape(e.shape[0], e.shape[1], -1).all(2)
        return first_true(~eq)
    fany = first_diff(("POS", "HEAD", "H", "S", "SG", "NAV", "SINCE", "TGT")); fd = first_diff(("POS", "HEAD", "H", "NAV", "SINCE", "TGT"))
    fdrive = first_true(o10["SUS"])
    dr = events(o10)["drives"]; m = on_hold(dr) & dr["ended"]
    fr = np.full(400, -1); fkind = np.full(400, -1)
    for e, r, hp in sorted(zip(dr["end"][m], dr["r"][m], dr["hp"][m])):
        if fr[r] < 0: fr[r], fkind[r] = e, int(hp == g[r])
    say(f"   rows {len(rows)} (Agent10 class N {int((c10[rows] == 'N').sum())}, tie {int((c10[rows] == 'tie').sum())});"
        f" first step differing in any recorded field (circuit s included) {q(fany[rows], '.0f')}, == the step after Agent10's first sustained drive step {int((fany[rows] == fdrive[rows] + 1).sum())}/{len(rows)};"
        f" first step differing in hold or trajectory (H, POS, HEAD, NAV, SINCE, TGT) == Agent10's first drive release (a drive-ended hold) {int((fd[rows] == fr[rows]).sum())}/{len(rows)};"
        f" that first release ends a negative hold {int((fkind[rows] == 0).sum())}, a valued hold {int((fkind[rows] == 1).sum())}")
    say(f"   first hold/trajectory differing step (= the release) quartiles {q(fd[rows], '.0f')}; state then: Agent10 holds nothing {int((o10['H'][fd[rows], rows] < 0).sum())}, Agent8 holds the negative odour"
        f" {int((o8['H'][fd[rows], rows] == 1 - g[rows]).sum())}, the valued {int((o8['H'][fd[rows], rows] == g[rows]).sum())}, nothing {int((o8['H'][fd[rows], rows] < 0).sum())}")
    geo = [rel(o10, t, r) for t, r in zip(fd[rows], rows)]
    say(f"   position then: inside the negative whiff region {sum(x['neg'][2] for x in geo)}, inside the valued {sum(x['val'][2] for x in geo)}, outside both {sum(not x['neg'][2] and not x['val'][2] for x in geo)};"
        f" distance to the nearest region {q(np.array([min(x['val'][3], x['neg'][3]) for x in geo]))}; d_along to the valued source {q(np.array([x['val'][0] for x in geo]))},"
        f" |d_cross| to the valued axis {q(np.abs([x['val'][1] for x in geo]))}")
    for lab, o in (("Agent10", o10), ("Agent8", o8)):
        ins, _ = inside_any(o); lost = arm_stats(o)[4]; W = o["W"]; AT = o["AT2"]; C = o["C"]
        re_ = np.array([bool(ins[t + 1:, r].any()) for t, r in zip(fd[rows], rows)]); wh = np.array([bool(W[t + 1:, r].any()) for t, r in zip(fd[rows], rows)])
        rv = np.array([bool(AT[t:, r, g[r]].any()) for t, r in zip(fd[rows], rows)]); rn = np.array([bool(AT[t:, r, 1 - g[r]].any()) for t, r in zip(fd[rows], rows)])
        wv = np.array([bool(W[t + 1:, r, g[r]].any()) for t, r in zip(fd[rows], rows)]); cc = np.array([bool(C[t:, r].any()) for t, r in zip(fd[rows], rows)])
        t60 = np.array([bool(W[t + 1:t + 61, r].any()) for t, r in zip(fd[rows], rows)])
        say(f"   [{lab}] after the first differing step: any whiff within 60 steps {int(t60.sum())}/{len(rows)}; any whiff until the end {int(wh.sum())}; valued whiff {int(wv.sum())};"
            f" re-entered a whiff region {int(re_.sum())}; reached the valued source {int(rv.sum())}, the negative source {int(rn.sum())}; wall contact {int(cc.sum())}; lost row {int(lost[rows].sum())};"
            f" class V/N/tie {[int((cls_of(o)[rows] == c).sum()) for c in ('V', 'N', 'tie')]}")
    return rows


def part_d(o10, o8, say):
    say("\n== D. Both arms: wall contacts, and where the agent is when nothing has been held for >= 60 steps ==")
    for lab, o in (("Agent10", o10), ("Agent8", o8)):
        H = o["H"]; run_ = np.zeros(H.shape, int); c = np.zeros(H.shape[1], int)
        for t in range(H.shape[0]): c = np.where(H[t] < 0, c + 1, 0); run_[t] = c
        m = run_ >= 60; ins, dist = inside_any(o)
        d = dist[m]; rowsm = m.any(0)
        say(f"   [{lab}] rows with >= 1 wall contact {int((o['contacts'] > 0).sum())}/400 (contacts per row {o['contacts'].mean():.3f});"
            f" (row, step) with nothing held for >= 60 steps {int(m.sum())} in {int(rowsm.sum())} rows; of those inside a whiff region {frac(int((d == 0).sum()), len(d))};"
            f" distance to the nearest region, outside {q(d[d > 0])}, p90 {np.percentile(d[d > 0], 90):.1f}; share at > 10 {(d > 10).mean():.3f}, > 20 {(d > 20).mean():.3f}")
        P = np.concatenate([o["start"][None], o["POS"][:-1]], 0); r = np.arange(400)
        da = np.minimum(P[:, :, 0] - o["src"][r, 0, 0][None], P[:, :, 0] - o["src"][r, 1, 0][None])[m]
        say(f"      on those (row, step): d_along to the sources {q(da)} (upwind of both {(da < 0).mean():.3f}, beyond the cones' far end > {LMAX:.0f} {(da > LMAX).mean():.3f})")


def main():
    print(f"== R3 diagnosis (measurement only; owner 2026-09-24, point 1). ph24c.py sha256 {sha(__file__)}; ph24.py {sha(ph24.__file__)}; ph24b.py {sha(ph24b.__file__)};"
          f" seeds {EVAL} reused (the R3 runs); World7 +1/-1, 400 x 600; Agent10 vs Agent8 ==")
    ph24.record = ph24b.record
    o = {"Agent10": run("T1", Agent10, VALS, EVAL), "Agent8": run("T1", Agent8, VALS, EVAL)}
    print("\n== reproduction of the recorded R3 counts (experiments/avoidance_check/ph24b_check.txt) ==")
    if not reproduce(o): print("== reproduction FAILED: nothing measured =="); sys.exit(1)
    part_a(o["Agent10"], print); part_b(o["Agent8"], o["Agent10"], print); part_c(o["Agent10"], o["Agent8"], print); part_d(o["Agent10"], o["Agent8"], print)
    print("\n== end (measurement only; no cause named beyond the counts; no change tested) ==")


if __name__ == "__main__":
    main()
