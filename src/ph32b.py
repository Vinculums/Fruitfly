#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H27 post-bench diagnosis (measurement only; owner 2026-09-26, '진단 먼저', gloss 'the diagnosis first'; decision:h27-post-bench-diagnosis).

Usage: python ph32b.py      (writes experiments/h27/ph32b_diag.txt, LF line ends)

ph32.py (sha256 checked below against the bench's), design v2 FINAL (doc d8c8949f2896cf1ec) and the bench verdict (STOPPED at the bench by
the registered stop rules (h), (hW), (hH), record:h27-bench-result) are untouched. Agent15, the harness `run`, the arms, the D generator,
p_D 0.03, every bar and every adopted module are imported as they are; no rule, parameter, bar or arm is changed, no agent variant is added,
nothing is swept. Bench seeds only: ph32.BS and ph32.BENCH['boot'], read from ph32 and not written in this file or in its output, so ph32's
seed self-check stays valid (ph32's scan excludes by name ph32.py, ph32_*.txt, h27_*.md, master_plan.md, notes/*.md, viewer/* and the
(file, number) pair of decision:seed-scan-exclusion-ph31-eval, experiments/h20/ph31_eval.txt; ph32b.py and ph32b_diag.txt are NOT
excluded by name, so the output text is checked against ph32.seed_numbers() before it is written). The development and evaluation seeds
(ph32.SEEDS) are not used.

Reproduction first: ph32.bench() is re-run as it is (every arm through ph32's own run, identities, (b1)-(d), (m), (h), (hW), (hH)); every
line it prints must equal experiments/h27/ph32_bench.txt's line for line (sha256 checked), and the headline numbers are asserted by name
(T1D P(V) 0.787 / 0.920; DP -0.1325 [-0.1675, -0.1000]; W1D paired dwell -19.7825, lost rows 400 vs 22; (hH) DP +0.0000 and M6 0.0000;
(m) 122). On any mismatch nothing is measured. Everything below reads the recorded fields of those very runs (ph32.record: H the circuit's
hold after the step's selection, HR the per-step argmax read by the hold-not-read arm, NAV, SINCE, TO and EV (the timeout and evidence
flags of the step's act, computed on the hold the step began with), SUS, C2 and P2 (counters and presence after the step's update), W the
step's whiffs (V, B, D), POS after the move, C the wall contact of the move, CONE at the sensing position, TGT the target heading).

Readings used here (measurement definitions; no rule reads them):
 (D1) the read hold hh = H (HR in the hold-not-read arm); values +1 on V (world column `good`), 0 on B and D.
 (D2) nav decomposition, per (step, row), the act's own law rebuilt from the recorded fields (ph23.py:86-92 as in ph32.Act15.act):
      vmax over the present odours (P2), top = present & v >= 0 & v == vmax, keep = hh >= 0 & (v_hh == vmax or v_hh < 0);
      steering set = {hh} if keep (the held odour's whiff), else the whiffing odours in top. Checked equal to the recorded NAV on every
      (step, row). A nav event is 'D-driven' when its steering set is {D} alone ('held-hit D' when D is held, 'unheld D' otherwise).
 (D3) hold episodes: maximal runs of one held channel in H. End step e + 1 (first step not held): 'evidence' if EV there, else
      'timeout (release)' if TO there, else 'other'; a hold still on at step 599 ends 'row end'. For every end, the steps from the held
      odour's last whiff (at or before e) to e + 1 are printed.
 (D4) positions: the sensing position of step t is POS[t - 1] (the start at t 0). d_along = x - x_src (the two sources share x; upwind is
      -x, UPWIND 180); d_cross to the V axis and the B axis = |y - y_src|. 'Whiff region' = ph32.cone_of (either cone or within 3.0).
      Walls at x 0 (upwind), x 160 (downwind), y 0 and y 160 (crosswind); the wall of a contact is the nearest wall to POS after the move.
 (D5) end state at step 599 (exclusive, in this order): at V (within 3.0), at B (within 3.0), at a wall (within 1.0 of one), upwind of
      both (d_along < 0), in the along range (0 <= d_along <= 25), downwind beyond 25.
 (D6) upwind displacement of a step = x before the move - x after; a nav event's segment runs from its step to the next nav event (or the
      row's end); segment displacements are summed per row by the event's driver.
 (D7) (m)'s rows (reading R7 of ph32): V absent by its counter on some step of the Agent15 D-off run (c_V >= 300). ta = first such step.
      'prior' = no V whiff on steps 0-58; 'silence' = otherwise (300 steps after the last V whiff before ta).
Names no cause; tests no change.
"""
import sys, os, hashlib, re
import numpy as np
import ph32
from ph32 import first_true, N_HI, PR, T, cone_of
from ph23 import wn
from ph9 import UPWIND, angdiff, LMAX
import ph28

PH32_SHA = "d9f585d5599ea9a4f218e87bd884fa8246a826be0111f495cfbec299a9222743"
BENCH_TXT_SHA = "957214476919dbbfa30c6b7f294d6b8554aec01eef485810d8e1a427dd4722f9"
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "experiments", "h27", "ph32b_diag.txt")
ARENA = 160.0
LAB = ("none", "V", "B", "D")


def sha(p=__file__): return hashlib.sha256(open(p, "rb").read()).hexdigest()


_lines = []
def say(s=""): _lines.append(s); print(s, flush=True)


def q(x, f=".0f"):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if not len(x): return "n/a"
    return "/".join(f"{v:{f}}" for v in np.percentile(x, [0, 25, 50, 75, 100])) + f" (n {len(x)})"


def pct(k, n): return f"{k}/{n} = {k/n:.3f}" if n else f"{k}/0"


# ------------------------------------------------------------------ per-run derived arrays
def derive(o):
    st, n = o["H"].shape; r = np.arange(n); g = o["good"]; B = 1 - g
    hnr = o["arm"].startswith("hold-not-read")
    hh = (o["HR"] if hnr else o["H"]).astype(int)
    v = np.zeros((n, 3)); v[r, g] = 1.0                                        # +1/0/0 (D1)
    W = o["W"]; P = o["P2"]
    lab = lambda h: np.where(h < 0, 0, np.where(h == g[None, :], 1, np.where(h == B[None, :], 2, 3)))   # none/V/B/D
    vh = v[r[None, :], np.maximum(hh, 0)]
    vmax = np.where(P, v[None, :, :], -np.inf).max(2)
    top = P & (v[None, :, :] >= 0) & (v[None, :, :] == vmax[:, :, None])
    keep = (hh >= 0) & ((vh == vmax) | (vh < 0))
    heldw = np.take_along_axis(W, np.maximum(hh, 0)[:, :, None], 2)[:, :, 0] & (hh >= 0)
    unheld = W & top
    nav = np.where(keep, heldw, unheld.any(2))
    # steering set per odour column (world columns g, B, 2) -> V/B/D flags
    oh = np.zeros_like(W); np.put_along_axis(oh, np.maximum(hh, 0)[:, :, None], (hh >= 0)[:, :, None], 2)
    steer = np.where(keep[:, :, None], oh & heldw[:, :, None], unheld)
    sV = steer[:, r, g]; sB = steer[:, r, B]; sD = steer[:, :, 2]
    P0 = np.concatenate([o["start"][None], o["POS"][:-1]], 0)
    d = dict(st=st, n=n, r=r, g=g, B=B, hh=hh, hl=lab(hh), Hl=lab(o["H"].astype(int)), keep=keep, nav=nav, sV=sV, sB=sB, sD=sD, top=top,
             P=P, W=W, wV=W[:, r, g], wB=W[:, r, B], wD=W[:, :, 2], PV=P[:, r, g], PB=P[:, r, B], PD=P[:, :, 2], P0=P0,
             xs=o["src"][:, 0, 0], yV=o["src"][r, g, 1], yB=o["src"][r, B, 1])
    d["navok"] = bool(np.array_equal(nav, o["NAV"]))
    d["Donly"] = nav & sD & ~sV & ~sB
    d["kind"] = np.where(~nav, -1, np.where(keep, 0, np.where(hh < 0, 1, 2)))          # 0 held-hit, 1 nothing held, 2 non-top held
    return d


def episodes(o, d, H=None):
    """(D3) hold episodes of the circuit's hold H: list of (row, lab, start, end_step, reason, gap)"""
    H = o["H"].astype(int) if H is None else H; st, n = H.shape; out = []
    g, B = d["g"], d["B"]; W = o["W"]
    for i in range(n):
        h = H[:, i]; ch = np.flatnonzero(np.diff(h) != 0) + 1; starts = np.concatenate([[0], ch]); ends = np.concatenate([ch, [st]])
        for s, e1 in zip(starts, ends):
            k = h[s]
            if k < 0: continue
            lb = 1 if k == g[i] else 2 if k == B[i] else 3
            if e1 >= st: reason = "row end"
            elif o["EV"][e1, i]: reason = "evidence"
            elif o["TO"][e1, i]: reason = "timeout"
            else: reason = "other"
            wk = np.flatnonzero(W[:e1, i, k]); gap = e1 - wk[-1] if len(wk) else -1
            out.append((i, lb, s, e1, reason, gap))
    return out


def hold_lines(tag, o, d, rows=None):
    n = d["n"]; rows = np.ones(n, bool) if rows is None else rows; nr = int(rows.sum()); st = d["st"]
    Hl = d["Hl"][:, rows]
    fr = [float((Hl == k).mean()) for k in range(4)]
    fr59 = [float((Hl[PR:] == k).mean()) for k in range(4)]
    say(f"   [{tag}] held (circuit H) fraction of (step, row), rows {nr}: none {fr[0]:.3f}, V {fr[1]:.3f}, B {fr[2]:.3f}, D {fr[3]:.3f};"
        f" steps {PR}-{st - 1}: none {fr59[0]:.3f}, V {fr59[1]:.3f}, B {fr59[2]:.3f}, D {fr59[3]:.3f}"
        + f"; per row, fraction of steps with nothing held {q((Hl == 0).mean(0), '.2f')}")
    ep = [e for e in episodes(o, d) if rows[e[0]]]
    for lb in (1, 2, 3):
        E = [e for e in ep if e[1] == lb]
        if not E: say(f"      {LAB[lb]} holds: none"); continue
        L = np.array([e[3] - e[2] for e in E]); rs = {}
        for e in E: rs[e[4]] = rs.get(e[4], 0) + 1
        per = np.bincount([e[0] for e in E], minlength=n)[rows]
        gaps = {k: np.array([e[5] for e in E if e[4] == k]) for k in ("timeout", "evidence", "other")}
        say(f"      {LAB[lb]} holds: {len(E)} in {int((per > 0).sum())} rows (per row {q(per)}); length {q(L)}; end: timeout (release) {rs.get('timeout', 0)},"
            f" evidence {rs.get('evidence', 0)}, other (neither flag) {rs.get('other', 0)}, row end {rs.get('row end', 0)}; steps from the held odour's last whiff to the end:"
            f" timeout {q(gaps['timeout'])}, evidence {q(gaps['evidence'])}, other (neither flag) {q(gaps['other'])}")
    return ep


def nav_lines(tag, o, d, rows=None):
    n = d["n"]; rows = np.ones(n, bool) if rows is None else rows; nr = int(rows.sum())
    nav = d["nav"][:, rows]; kind = d["kind"][:, rows]; sV, sB, sD = d["sV"][:, rows], d["sB"][:, rows], d["sD"][:, rows]; hl = d["hl"][:, rows]
    tot = int(nav.sum())
    def cnt(m): return int((nav & m).sum())
    parts = []
    for kd, kn in ((0, "held-hit"), (1, "nothing held"), (2, "non-top odour held")):
        m = kind == kd
        sub = [(nm, cnt(m & a & ~b1 & ~b2)) for nm, a, b1, b2 in (("V", sV, sB, sD), ("B", sB, sV, sD), ("D", sD, sV, sB))]
        multi = cnt(m) - sum(c for _, c in sub)
        parts.append(f"{kn} {cnt(m)} (" + ", ".join(f"{nm} {c}" for nm, c in sub) + f", two or more {multi})")
    Donly = d["Donly"][:, rows]; nD = int(Donly.sum())
    say(f"   [{tag}] nav events, rows {nr}: {tot} ({tot/nr:.2f} per row): " + "; ".join(parts))
    fd = first_true(Donly);
    say(f"      D-driven (steering set {{D}} alone) {pct(nD, tot)} of nav events; rows with any {int((fd >= 0).sum())}/{nr}; first D-driven nav step {q(fd[fd >= 0])};"
        f" D-driven events with V present {int((Donly & d['PV'][:, rows]).sum())}, with V absent {int((Donly & ~d['PV'][:, rows]).sum())}")
    wD = d["wD"][:, rows]; since0 = o["SINCE"][:, rows] == 0
    say(f"      the cast clock `since` resets exactly on nav (SINCE == 0 iff NAV): {bool(np.array_equal(since0, o['NAV'][:, rows]))};"
        f" D-whiff steps {int(wD.sum())}, of them with nav (any driver; `since` reset) {pct(int((wD & nav).sum()), int(wD.sum()))}, with a D-driven nav"
        f" {pct(int((wD & Donly).sum()), int(wD.sum()))}")
    PV = d["PV"][:, rows]; parts = []; partsD = []
    for vp, vn in ((True, "V present"), (False, "V absent")):
        for k in range(4):
            m = wD & (PV == vp) & (hl == k)
            if m.sum(): parts.append(f"{vn}, held {LAB[k]}: {int((m & nav).sum())} ({int((m & Donly).sum())})/{int(m.sum())}")
    say("      D-whiff steps with nav (of them D-driven) / D-whiff steps, by state (read hold): " + ("; ".join(parts) if parts else "none"))
    wB = d["wB"][:, rows]; parts = []
    for k in range(4):
        m = wB & ~PV & (hl == k)
        if m.sum(): parts.append(f"held {LAB[k]}: {int((m & nav).sum())}/{int(m.sum())}")
    say("      B-whiff steps with V absent, steering (nav) / total, by read hold: " + ("; ".join(parts) if parts else "none")
        + f"; (step, row) with V present and D in the top set {int((d['top'][:, rows][:, :, 2] & PV).sum())}")
    return fd


def presence_lines(tag, d, rows=None):
    n = d["n"]; rows = np.ones(n, bool) if rows is None else rows
    PV, PB, PD = d["PV"][:, rows], d["PB"][:, rows], d["PD"][:, rows]; top = d["top"][:, rows]; r = d["r"][rows]; g = d["g"][rows]; B = d["B"][rows]
    tV, tB, tD = top[:, np.arange(len(r)), g], top[:, np.arange(len(r)), B], top[:, :, 2]
    none = d["hl"][:, rows] == 0
    say(f"   [{tag}] present by counter or hold, fraction of (step, row): V {PV.mean():.3f}, B {PB.mean():.3f}, D {PD.mean():.3f}; steps {PR}-599: V {PV[PR:].mean():.3f},"
        f" B {PB[PR:].mean():.3f}, D {PD[PR:].mean():.3f}; rows with V absent on some step {int((~PV).any(0).sum())}")
    say(f"      top set, all (step, row): {{V}} {(tV & ~tB & ~tD).mean():.3f}, {{B, D}} {(tB & tD & ~tV).mean():.3f}, {{B}} {(tB & ~tD & ~tV).mean():.3f},"
        f" {{D}} {(tD & ~tB & ~tV).mean():.3f}, D in top {tD.mean():.3f}; steps with nothing read as held {none.mean():.3f}, of them D in top {tD[none].mean() if none.any() else float('nan'):.3f},"
        f" V in top {tV[none].mean() if none.any() else float('nan'):.3f}")


def geo(o, d, t, i):
    p = d["P0"][t, i]; return p[0] - d["xs"][i], abs(p[1] - d["yV"][i]), abs(p[1] - d["yB"][i])


def end_state(o, d):
    """(D5) per row: 0 at V, 1 at B, 2 at a wall, 3 upwind of both, 4 along range, 5 downwind beyond 25"""
    p = o["POS"][-1]; r = d["r"]; src = o["src"]
    aV = np.linalg.norm(p - src[r, d["g"]], axis=1) < 3.0; aB = np.linalg.norm(p - src[r, d["B"]], axis=1) < 3.0
    wall = np.minimum(p, ARENA - p).min(1) < 1.0; da = p[:, 0] - d["xs"]
    return np.select([aV, aB, wall, da < 0, da <= LMAX], [0, 1, 2, 3, 4], 5)


ENDS = ("at V", "at B", "at a wall", "upwind of both", "in the along range", "downwind beyond 25")


def ends_str(e, rows):
    return ", ".join(f"{ENDS[k]} {int(((e == k) & rows).sum())}" for k in range(6))


def walls(o, rows):
    """(D4) contacts by the nearest wall of POS after the move"""
    C = o["C"][:, rows]; p = o["POS"][:, rows]
    dist = np.stack([p[:, :, 0], ARENA - p[:, :, 0], p[:, :, 1], ARENA - p[:, :, 1]], 2); w = dist.argmin(2)
    return [int((C & (w == k)).sum()) for k in range(4)], first_true(C)


def traj_lines(tag, on, off, don, doff, rows, lostdef=None):
    """(A4) rows given; first D event (hold formation or D-driven nav) in the D-on run"""
    n = don["n"]; idx = np.flatnonzero(rows); st = don["st"]
    fh = first_true(don["Hl"] == 3); fn = first_true(don["Donly"])
    fdh = np.where(fh < 0, 10**6, fh); fdn = np.where(fn < 0, 10**6, fn); fe = np.minimum(fdh, fdn); has = fe < 10**6
    div = first_true(~(on["POS"] == off["POS"]).all(2))
    say(f"   [{tag}] rows {len(idx)}: rows with a D event {int(has[rows].sum())} (first a D hold {int((has & (fdh < fdn))[rows].sum())}, first a D-driven nav"
        f" {int((has & (fdn < fdh))[rows].sum())}, same step {int((has & (fdn == fdh))[rows].sum())}); first D event step {q(fe[rows & has])}; first step at which D on and"
        f" D off positions differ {q(div[rows & (div >= 0)])} (rows never differing {int((rows & (div < 0)).sum())}); divergence at or after the first D event"
        f" {int((rows & has & (div >= 0) & (div >= fe)).sum())}")
    da, dV, dB, cone, up20, lv, wc = [], [], [], [], [], [], []
    fc = first_true(on["C"])
    for i in idx:
        if not has[i]: continue
        t = int(fe[i]); a, cv, cb = geo(on, don, t, i); da.append(a); dV.append(cv); dB.append(cb); cone.append(bool(on["CONE"][t, i]))
        t2 = min(t + 20, st - 1); up20.append(don["P0"][t, i, 0] - on["POS"][t2, i, 0])
        x = on["POS"][t:, i, 0] - don["xs"][i]; out = np.flatnonzero((x < 0) | (x > LMAX)); lv.append(out[0] if len(out) else np.nan)
        wc.append(fc[i] - t if fc[i] >= t else np.nan)
    da, dV, dB, cone = np.array(da), np.array(dV), np.array(dB), np.array(cone)
    if len(da):
        say(f"      at the first D event: d_along {q(da, '.1f')} (upwind of the sources' line, d_along < 0: {int((da < 0).sum())}/{len(da)}); d_cross to the V axis {q(dV, '.1f')}, to the B axis {q(dB, '.1f')}; inside a whiff region {int(cone.sum())}/{len(cone)};"
            f" upwind displacement over the next 20 steps {q(up20, '.1f')}; steps to leaving the along range 0-25 {q(lv)}; steps to the first wall contact {q(wc)}"
            f" (rows with a contact after it {int(np.isfinite(wc).sum())})")
    ep = episodes(on, don); byrow = {}
    for e in ep: byrow.setdefault(e[0], []).append(e)
    st_ = {"D held": 0, "nothing held": 0}; prev = {}
    for i in idx:
        if fn[i] < 0: continue
        t = int(fn[i]); h = don["Hl"][t, i]
        if h == 3: st_["D held"] += 1; continue
        st_["nothing held"] += 1; E = [e for e in byrow.get(i, []) if e[3] <= t]
        key = "no earlier hold" if not E else f"{LAB[E[-1][1]]} hold ended by {E[-1][4]}"
        prev[key] = prev.get(key, 0) + 1
    say(f"      at the first D-driven nav (rows {int((rows & (fn >= 0)).sum())}): " + ", ".join(f"{k} {v}" for k, v in st_.items())
        + "; with nothing held, the last hold before it: " + ", ".join(f"{k} {v}" for k, v in sorted(prev.items())))
    e_on, e_off = end_state(on, don), end_state(off, doff)
    say(f"      end state at 599, D on: {ends_str(e_on, rows)}")
    say(f"      end state at 599, D off: {ends_str(e_off, rows)}")
    (won, fcon), (woff, fcoff) = walls(on, rows), walls(off, rows)
    say(f"      wall contacts D on {sum(won)} (upwind x 0 {won[0]}, downwind x 160 {won[1]}, y 0 {won[2]}, y 160 {won[3]}), rows with any {int((fcon >= 0).sum())}, first contact step"
        f" {q(fcon[fcon >= 0])}; D off {sum(woff)}, rows with any {int((fcoff >= 0).sum())}")
    return fe, has


def segments(o, d):
    """(D6) per row, upwind displacement summed by the driver of the nav segment it falls in: cast before any nav, V, B, D, two or more"""
    st, n = d["st"], d["n"]; x0 = d["P0"][:, :, 0]; x1 = o["POS"][:, :, 0]; up = x0 - x1
    drv = np.full((st, n), -1)
    nav = d["nav"]; sV, sB, sD = d["sV"], d["sB"], d["sD"]
    cur = np.full(n, -1)
    for t in range(st):
        lbl = np.where(sV[t] & ~sB[t] & ~sD[t], 0, np.where(sB[t] & ~sV[t] & ~sD[t], 1, np.where(sD[t] & ~sV[t] & ~sB[t], 2, 3)))
        cur = np.where(nav[t], lbl, cur); drv[t] = cur
    tot = np.stack([np.where(drv == k, up, 0.0).sum(0) for k in (-1, 0, 1, 2, 3)], 1)
    step = np.stack([np.where(nav & (drv == k), up, np.nan) for k in (0, 1, 2)], 0)
    return drv, up, tot, step


def surge_lines(tag, o, d, rows=None):
    n = d["n"]; rows = np.ones(n, bool) if rows is None else rows
    drv, up, tot, step = segments(o, d)
    kind, nav = d["kind"], d["nav"]
    per = lambda m: (nav & m)[:, rows].sum(0)
    sB_, sD_ = d["sB"] & ~d["sV"] & ~d["sD"], d["sD"] & ~d["sV"] & ~d["sB"]
    say(f"   [{tag}] surges (nav True) per row, mean (rows with any): B hit with B held {per((kind == 0) & sB_).mean():.2f} ({int((per((kind == 0) & sB_) > 0).sum())});"
        f" D hit with D held {per((kind == 0) & sD_).mean():.2f} ({int((per((kind == 0) & sD_) > 0).sum())}); B whiff, nothing held {per((kind == 1) & sB_).mean():.2f}"
        f" ({int((per((kind == 1) & sB_) > 0).sum())}); D whiff, nothing held {per((kind == 1) & sD_).mean():.2f} ({int((per((kind == 1) & sD_) > 0).sum())});"
        f" non-top odour held {per(kind == 2).mean():.2f}; two or more odours steering {per((kind >= 0) & ~sB_ & ~sD_ & ~(d['sV'] & ~d['sB'] & ~d['sD'])).mean():.2f}")
    say(f"      upwind displacement on the surge step itself (max 0.6): B-driven {q(step[1][:, rows], '.2f')}, D-driven {q(step[2][:, rows], '.2f')}")
    T_ = tot[rows]
    say(f"      upwind displacement per row by the segment's driver (from a nav event to the next; D6), mean [quartiles]: before any nav (cast) {T_[:, 0].mean():.1f}"
        f" [{q(T_[:, 0], '.1f')}]; V-driven {T_[:, 1].mean():.1f}; B-driven {T_[:, 2].mean():.1f} [{q(T_[:, 2], '.1f')}]; D-driven {T_[:, 3].mean():.1f} [{q(T_[:, 3], '.1f')}];"
        f" two or more {T_[:, 4].mean():.1f}; total {T_.sum(1).mean():.1f}")
    segn = []
    for i in np.flatnonzero(rows):
        ev = np.flatnonzero(d["Donly"][:, i])
        if not len(ev): continue
        nx = np.flatnonzero(nav[:, i]); b = np.searchsorted(nx, ev, side="right"); ends = np.where(b < len(nx), nx[np.minimum(b, len(nx) - 1)], d["st"])
        fc = np.flatnonzero(o["C"][:, i]); fc = fc[0] if len(fc) else d["st"]
        for s, e in zip(ev, ends): segn.append((up[s:e, i].sum(), e - s, s < fc))
    if segn:
        a = np.array(segn, float); pre = a[:, 2] > 0
        say(f"      per D-driven segment ({len(a)}): upwind displacement {q(a[:, 0], '.1f')}, mean {a[:, 0].mean():.2f}; length in steps {q(a[:, 1])}; the"
            f" {int(pre.sum())} segments starting before the row's first wall contact: upwind displacement {q(a[pre, 0], '.1f')}, mean {a[pre, 0].mean():.2f},"
            f" per step {a[pre, 0].sum()/max(a[pre, 1].sum(), 1):.3f}")
    tg = np.abs(angdiff(o["TGT"], UPWIND))[PR:, rows]
    say(f"      target heading with a downwind component (|target - upwind| > 90), steps {PR}-599: {(tg > 90).mean():.3f}; target within 40 of upwind {(tg <= 40).mean():.3f};"
        f" `since` on nothing-held steps {PR}-599 quartiles {q(o['SINCE'][PR:, rows][d['hl'][PR:, rows] == 0])}")
    return drv, up, tot


def exit_lines(tag, o, d, drv, rows=None):
    """W1: the final upwind exit (last step with d_along >= -3, + 1) and the driver of the segment it falls in"""
    n = d["n"]; rows = np.ones(n, bool) if rows is None else rows; st = d["st"]
    x = o["POS"][:, :, 0] - d["xs"][None, :]; ok = x >= -3.0; last = np.where(ok.any(0), st - 1 - np.argmax(ok[::-1], 0), -1); ex = last + 1
    has = rows & (ex < st) & (x[-1] < -3.0)
    lb = np.array([drv[ex[i], i] if has[i] else -9 for i in range(n)])
    names = ("cast (no nav yet)", "V", "B", "D", "two or more")
    say(f"   [{tag}] final upwind exit (after it d_along < -3 to the end), rows {int(has.sum())}/{int(rows.sum())}; exit step {q(ex[has])}; driver of the segment at the exit: "
        + ", ".join(f"{nm} {int((lb == k).sum())}" for k, nm in zip((-1, 0, 1, 2, 3), names)))
    tp = first_true(x < -3.0); hp = rows & (tp >= 0)
    ret = np.array([hp[i] and bool((x[tp[i]:, i] >= 0).any()) for i in range(n)])
    up = d["P0"][:, :, 0] - o["POS"][:, :, 0]; aft = np.arange(st)[:, None] >= np.where(tp < 0, st, tp)[None, :]
    byd = [float(np.where(aft & (drv == k), up, 0.0)[:, hp].sum(0).mean()) if hp.any() else 0.0 for k in (-1, 0, 1, 2, 3)]
    say(f"      first upwind pass (d_along < -3): rows {int(hp.sum())}, step {q(tp[hp])}; of them back downwind of the sources' line (d_along >= 0) later {int(ret.sum())};"
        f" most upwind d_along {q(x[:, rows].min(0), '.1f')}; upwind displacement after the first pass, mean per row by segment driver: "
        + ", ".join(f"{nm} {v:.1f}" for nm, v in zip(names, byd)))
    lastB = np.array([np.flatnonzero(d["wB"][:, i])[-1] if d["wB"][:, i].any() else -1 for i in range(n)])
    m = has & (lastB >= 0)
    say(f"      last B whiff step {q(lastB[rows & (lastB >= 0)])} (rows with none {int((rows & (lastB < 0)).sum())}); exit minus last B whiff {q((ex - lastB)[m])}")
    return ex, has


# ------------------------------------------------------------------ (B) the (m) rows
def m_lines(on, off, don, doff):
    n = doff["n"]; g = doff["g"]; r = doff["r"]
    cV = off["C2"][:, r, g]; vab = (cV >= N_HI).any(0); ta = first_true(cV >= N_HI)
    fv = first_true(doff["wV"]); prior = vab & ((fv < 0) | (fv > PR - 1)); sil = vab & ~prior
    assert int(vab.sum()) == int(ph32.v_absent(off).sum())
    say(f"(B1) (m) rows, V absent by its counter on some step of the Agent15 D-off run (reading R7): {int(vab.sum())}/{n}; 'prior' (no V whiff on 0-{PR - 1}) {int(prior.sum())},"
        f" first absent step {q(ta[prior])}; 'silence' (300 steps after a V whiff) {int(sil.sum())}, first absent step {q(ta[sil])}")
    risk, _ = ph28.at_risk(off); risk0, _ = ph28.at_risk(off, lo=0)
    say(f"      H26's at-risk definition (ph28 reading R3: no V whiff on 0-{PR - 1} and a B whiff with nothing or B held on a step from {PR} to the first V whiff) applied to"
        f" this D-off run: {int(risk.sum())} rows (literal reading from step 0: {int(risk0.sum())}); of them in (m) {int((risk & vab).sum())}")
    fvq = fv[fv >= 0]
    say(f"      first V whiff step (D off) {q(fvq)}; rows with none by step {PR - 1} {int(((fv < 0) | (fv > PR - 1)).sum())}, by 118 {int(((fv < 0) | (fv > 118)).sum())},"
        f" never {int((fv < 0).sum())}")
    # state at ta and over the preceding window, D off (position/event-based, not causal)
    Hl = doff["Hl"]; st = doff["st"]; tt = np.arange(st)[:, None]
    heldB = np.zeros(n, bool); heldN = np.zeros(n, bool); da = np.full(n, np.nan); dv = np.full(n, np.nan); db = np.full(n, np.nan); wall = np.zeros(n, bool)
    Bwin = np.zeros(n, bool); Bhold = np.zeros(n, bool); atBw = np.zeros(n, bool); frB = np.full(n, np.nan); frN = np.full(n, np.nan)
    for i in np.flatnonzero(vab):
        t = int(ta[i]); lo = max(0, t - N_HI); p = doff["P0"][t, i]
        heldB[i] = Hl[t, i] == 2; heldN[i] = Hl[t, i] == 0
        da[i] = p[0] - doff["xs"][i]; dv[i] = np.linalg.norm(p - off["src"][i, g[i]]); db[i] = np.linalg.norm(p - off["src"][i, 1 - g[i]])
        wall[i] = min(p[0], ARENA - p[0], p[1], ARENA - p[1]) < 1.0
        Bwin[i] = doff["wB"][lo:t, i].any(); Bhold[i] = (Hl[lo:t, i] == 2).any(); atBw[i] = off["AT2"][lo:t, i, 1 - g[i]].any()
        frB[i] = (Hl[lo:t, i] == 2).mean(); frN[i] = (Hl[lo:t, i] == 0).mean()
    pos = np.select([wall, da < 0, da <= LMAX], [0, 1, 2], 3)
    for lab_, m in (("prior", prior), ("silence", sil)):
        say(f"      [{lab_}, {int(m.sum())}] at ta (D off): held B {int((m & heldB).sum())}, nothing held {int((m & heldN).sum())}; position at a wall {int((m & (pos == 0)).sum())},"
            f" upwind of both sources (d_along < 0) {int((m & (pos == 1)).sum())}, in the along range {int((m & (pos == 2)).sum())}, downwind beyond 25 {int((m & (pos == 3)).sum())};"
            f" d_along {q(da[m], '.1f')}; distance to V {q(dv[m], '.1f')}, to B {q(db[m], '.1f')}; in the window before ta: B whiffs in {int((m & Bwin).sum())} rows, a B hold in"
            f" {int((m & Bhold).sum())}, within 3.0 of B in {int((m & atBw).sum())}; held fraction B {np.nanmean(frB[m]) if m.any() else float('nan'):.3f},"
            f" nothing {np.nanmean(frN[m]) if m.any() else float('nan'):.3f}")
    sl = np.flatnonzero(sil)
    if len(sl):
        lvw = np.array([np.flatnonzero(doff["wV"][:ta[i], i])[-1] for i in sl])
        say(f"      [silence] last V whiff before ta {q(lvw)}; ta - last V whiff {q(ta[sl] - lvw)}")
    # D on, the same rows
    von = ph32.v_absent(on); con, coff = ph32.cls3(on), ph32.cls3(off)
    tao = first_true(on["C2"][:, r, g] >= N_HI)
    say(f"(B2) the same rows in the Agent15 D-on run: V ever absent there {int((von & vab).sum())}/{int(vab.sum())} (all rows {int(von.sum())}; absent in D on only {int((von & ~vab).sum())},"
        f" in D off only {int((~von & vab).sum())}); first absent step equal in D on and D off {int((vab & von & (tao == ta)).sum())}")
    after = tt >= np.where(ta < 0, st, ta)[None, :]
    fh = first_true((don["Hl"] == 3) & after); fn = first_true(don["Donly"] & after); nvw = first_true(don["wV"] & after)
    INF = 10**6; a_ = np.where(fh < 0, INF, fh); b_ = np.where(fn < 0, INF, fn); c_ = np.where(nvw < 0, INF, nvw)
    heldD = np.array([bool(don["Hl"][ta[i], i] == 3) if ta[i] >= 0 else False for i in range(n)])
    k1 = vab & (heldD | ((a_ < c_) & (a_ <= b_))); k2 = vab & ~k1 & (b_ < c_); k4 = vab & ~k1 & ~k2
    outv = (coff == 0) & (con != 0); intov = (con == 0) & (coff != 0)
    fe = np.minimum(a_, b_)
    say("      the first D event at or after ta and before the next V whiff, D-on run (event-based, exclusive, in this order; out-of-V rows in brackets): (i) a D hold"
        f" (held at ta {int((vab & heldD).sum())}, or forming first) {int(k1.sum())} [{int((k1 & outv).sum())}]; (ii) a D-driven nav {int(k2.sum())} [{int((k2 & outv).sum())}];"
        f" (v) neither before the next V whiff or the row's end {int(k4.sum())} [{int((k4 & outv).sum())}]")
    say(f"      steps from ta to that first D event {q((fe - ta)[(k1 | k2)])}; steps from ta to the next V whiff in D on {q((c_ - ta)[vab & (c_ < INF)])} (rows with none"
        f" {int((vab & (c_ >= INF)).sum())}); in D off {q((np.where(first_true(doff['wV'] & after) < 0, INF, first_true(doff['wV'] & after)) - ta)[vab & (first_true(doff['wV'] & after) >= 0)])}"
        f" (rows with none {int((vab & (first_true(doff['wV'] & after) < 0)).sum())})")
    Hon = don["Hl"]; hta = np.array([Hon[ta[i], i] if ta[i] >= 0 else -1 for i in range(n)])
    ep = episodes(on, don); endB = {}; endBoff = {}
    for (e_, dd, lst) in ((ep, don, endB), (episodes(off, doff), doff, endBoff)):
        for (i, lb, s0, e1, rs, gp) in e_:
            if vab[i] and lb == 2 and s0 <= ta[i] < e1: lst[i] = (rs, e1, gp)
    def tally(dct, m):
        out = {}
        for i, (rs, e1, gp) in dct.items():
            if m[i]: out[rs] = out.get(rs, 0) + 1
        return ", ".join(f"{k} {v}" for k, v in sorted(out.items())) or "none"
    bta = vab & (hta == 2)
    aftB = np.array([i in endB and (k2[i] or k1[i]) and fe[i] >= endB[i][1] for i in range(n)])
    say(f"      D on, held at ta: none {int((vab & (hta == 0)).sum())}, B {int(bta.sum())}, D {int((vab & (hta == 3)).sum())}; the B hold held at ta ends by (D on): {tally(endB, vab)};"
        f" in the out-of-V rows: {tally(endB, outv)}; (D off: {tally(endBoff, vab)}); rows whose first D event comes at or after that B hold's end {int(aftB.sum())}"
        f" (out of V {int((aftB & outv).sum())})")
    say("      table, rows (out of V): mechanism of the D-off absence x held at ta (D off) x the D-on event class:")
    for lab_, m in (("(iv) prior expiry", prior), ("silence after a V whiff", sil)):
        for hl_, hm in (("(iii) B held at ta", heldB), ("nothing held at ta", heldN)):
            mm = m & hm
            say(f"         {lab_}, {hl_}: {int(mm.sum())} ({int((mm & outv).sum())}): (i) {int((mm & k1).sum())} ({int((mm & k1 & outv).sum())}), (ii) {int((mm & k2).sum())}"
                f" ({int((mm & k2 & outv).sum())}), (v) {int((mm & k4).sum())} ({int((mm & k4 & outv).sum())})")
    say(f"      by mechanism of the D-off absence: prior {int(prior.sum())} (out of V {int((prior & outv).sum())}), silence {int(sil.sum())} (out of V {int((sil & outv).sum())});"
        f" out of V overall {int(outv.sum())} (all in (m): {bool((outv <= vab).all())}), into V {int(intov.sum())}")
    say(f"      outcome V/B/tie of the {int(vab.sum())} rows: D on {int((con[vab] == 0).sum())}/{int((con[vab] == 1).sum())}/{int((con[vab] == 2).sum())}, D off"
        f" {int((coff[vab] == 0).sum())}/{int((coff[vab] == 1).sum())}/{int((coff[vab] == 2).sum())}")
    return vab, outv, ta


# ------------------------------------------------------------------ (C) the W1D loss paths
def c_lines(res):
    arms = ("Agent15 D on", "hold-not-read D on", "release-off D on", "Agent15 D off", "Agent15g D on")
    ref = res[("W1", "Agent15 D on")]; out = {}
    for a in arms:
        o = res[("W1", a)]; d = derive(o) if a != "Agent15g D on" else None; n = o["H"].shape[1]; r = np.arange(n); g = o["good"]; B = 1 - g
        s = ph32.w1sum(o); wB = o["W"][:, r, B]; lastB = np.array([np.flatnonzero(wB[:, i])[-1] if wB[:, i].any() else -1 for i in range(n)])
        at = o["AT2"][:, r, B]; lastat = np.array([np.flatnonzero(at[:, i])[-1] if at[:, i].any() else -1 for i in range(n)]); firstat = first_true(at)
        e = end_state(o, d if d is not None else dict(r=r, g=g, B=B, xs=o["src"][:, 0, 0]))
        wl, fc = walls(o, np.ones(n, bool))
        out[a] = dict(lost=s["lost"], lastB=lastB, fc=fc, e=e, lastat=lastat)
        say(f"   [W1 {a}] lost rows {int(s['lost'].sum())}/{n}; last B whiff step {q(lastB[lastB >= 0])} (rows with none {int((lastB < 0).sum())}); reach within 3.0 of B"
            f" {int(s['reach'].sum())}/{n}, first arrival {q(firstat[firstat >= 0])}, last step within 3.0 {q(lastat[lastat >= 0])}; dwell within 3.0 {q(s['dwell'])} (mean"
            f" {s['dwell'].mean():.3f}); dwell of reaching rows {q(s['dwell'][s['reach']])}")
        say(f"      end state at 599: {ends_str(e, np.ones(n, bool))}; wall contacts {sum(wl)} ({sum(wl)/n:.3f} per row): upwind x 0 {wl[0]}, downwind x 160 {wl[1]}, y 0 {wl[2]},"
            f" y 160 {wl[3]}; rows with any {int((fc >= 0).sum())}, first contact step {q(fc[fc >= 0])}")
    for a in ("hold-not-read D on", "release-off D on", "Agent15 D off"):
        o = res[("W1", a)]; A, Bq = out["Agent15 D on"], out[a]
        same = (o["POS"] == ref["POS"]).all((0, 2)); div = first_true(~(o["POS"] == ref["POS"]).all(2))
        both = (A["lastB"] >= 0) & (Bq["lastB"] >= 0); dfc = (A["fc"] >= 0) & (Bq["fc"] >= 0)
        say(f"   [W1 Agent15 D on vs {a}] rows with identical positions on all 600 steps {int(same.sum())}/{len(same)}; first differing step {q(div[div >= 0])};"
            f" lost in both {int((A['lost'] & Bq['lost']).sum())}, Agent15 only {int((A['lost'] & ~Bq['lost']).sum())}, {a} only {int((~A['lost'] & Bq['lost']).sum())};"
            f" last B whiff step equal {int((both & (A['lastB'] == Bq['lastB'])).sum())}/{int(both.sum())}, difference ({a} - Agent15) {q((Bq['lastB'] - A['lastB'])[both])};"
            f" first wall contact step difference {q((Bq['fc'] - A['fc'])[dfc])} (rows with a contact in both {int(dfc.sum())}); same end state {int((A['e'] == Bq['e']).sum())}")
    o = res[("W1", "hold-not-read D on")]
    say(f"   [W1 hold-not-read D on] steps on which the read argmax HR differs from the circuit's hold H {float((o['HR'] != o['H']).mean()):.3f};"
        f" HR fraction none/V/B/D {', '.join(f'{x:.3f}' for x in (np.mean(o['HR'] < 0), np.mean(o['HR'] == o['good'][None, :]), np.mean(o['HR'] == 1 - o['good'][None, :]), np.mean(o['HR'] == 2)))}")
    return out


# ------------------------------------------------------------------ reproduction
def reproduce():
    rec = open(ph32.BENCH_TXT, "rb").read(); ok_sha = sha(ph32.__file__) == PH32_SHA and hashlib.sha256(rec).hexdigest() == BENCH_TXT_SHA
    if not ok_sha: say("== ph32.py or ph32_bench.txt is not the recorded version: STOP, nothing is measured =="); raise SystemExit(4)
    lines = []; v, bo, res = ph32.bench(say=lines.append)
    want = rec.decode("utf-8").split("\n")
    if want and want[-1] == "": want = want[:-1]
    eq = [ln == w for ln, w in zip(lines, want)]
    say(f"   ph32.py sha256 equals the bench's ({PH32_SHA[:8]}...{PH32_SHA[-4:]}): True; ph32_bench.txt sha256 equals the recorded ({BENCH_TXT_SHA[:8]}...{BENCH_TXT_SHA[-4:]}): True")
    say(f"   ph32.bench() re-run as it is: {len(lines)} lines printed, ph32_bench.txt {len(want)} lines; equal line for line {sum(eq)}/{len(want)} -> {len(lines) == len(want) and all(eq)}")
    s = {a: ph32.w1sum(res[("W1", a)]) for a in ("Agent15 D on", "Agent15 D off", "hold-not-read D on")}
    con, coff = ph32.cls3(res[("T1", "Agent15 D on")]), ph32.cls3(res[("T1", "Agent15 D off")])
    _, _, dlo, dhi = ph32.interval("DP", (con == 0).astype(float), (coff == 0).astype(float))
    checks = {"T1D P(V) D on 0.787": f"{(con == 0).mean():.3f}" == "0.787", "D off 0.920": f"{(coff == 0).mean():.3f}" == "0.920",
              "DP -0.1325 [-0.1675, -0.1000]": f"{bo['dp_T1']:+.4f} [{dlo:+.4f}, {dhi:+.4f}]" == "-0.1325 [-0.1675, -0.1000]",
              "W1D paired dwell -19.7825": f"{bo['m5b']:+.4f}" == "-19.7825", "lost 400 vs 22": (int(s["Agent15 D on"]["lost"].sum()), int(s["Agent15 D off"]["lost"].sum())) == (400, 22),
              "(hH) DP +0.0000, M6 0.0000": f"{bo['dp6']:+.4f} {bo['pp_M6']:.4f}" == "+0.0000 0.0000", "(m) 122": bo["m"] == 122,
              "stop rules (h), (hW), (hH) all STOP": bool(bo["stop_h"] and bo["stop_hw"] and bo["stop_hh"])}
    say("   headline numbers: " + "; ".join(f"{k} {v}" for k, v in checks.items()))
    nums = ph32.seed_numbers(); pat = re.compile(r"(?<!\d)(" + "|".join(map(str, nums)) + r")(?!\d)")
    for tag in ("(m)", "(h)", "   (h)", "      [W1", "   (hW)", "   (hH)"):
        for ln in lines:
            if ln.startswith(tag): say("   == " + pat.sub("<bench seed>", ln.strip()))
    if not (len(lines) == len(want) and all(eq) and all(checks.values())):
        say("== the bench does not reproduce: STOP, nothing is measured =="); raise SystemExit(5)
    return res


def main():
    say(f"== H27 post-bench diagnosis (measurement only; owner 2026-09-26, '진단 먼저', decision:h27-post-bench-diagnosis). ph32b.py sha256 {sha()}; ph32.py sha256 {sha(ph32.__file__)};"
        f" design {ph32.DESIGN}; reproduces experiments/h27/ph32_bench.txt sha256 {BENCH_TXT_SHA} (record:h27-bench-result) ==")
    say("   imported modules (as ph32 prints them): " + "; ".join(f"{os.path.basename(m.__file__)} {sha(m.__file__)}" for m in ph32.MODS) + f"; ph32.py {sha(ph32.__file__)}")
    say("   seeds: the bench seeds (ph32.BS) and the bench bootstrap seed (ph32.BENCH['boot']), read from ph32 and not written out here; the development and evaluation seeds"
        " (ph32.SEEDS) are not used; p_D as ph32 sets it (0.03), unchanged")
    say("   seed scan: ph32's scan excludes by name ph32.py, ph32_*.txt, h27_*.md, master_plan.md, notes/*.md, viewer/* and the (file, number) pair of"
        " decision:seed-scan-exclusion-ph31-eval (experiments/h20/ph31_eval.txt); ph32b.py and this output are not excluded, so this text is checked against ph32.seed_numbers()"
        " before it is written")
    say("\n== (0) reproduction (nothing is measured unless every check holds) ==")
    res = reproduce()
    t1on, t1off = res[("T1", "Agent15 D on")], res[("T1", "Agent15 D off")]; w1on, w1off = res[("W1", "Agent15 D on")], res[("W1", "Agent15 D off")]
    w1h, w1r = res[("W1", "hold-not-read D on")], res[("W1", "release-off D on")]
    D = {k: derive(o) for k, o in (("T1on", t1on), ("T1off", t1off), ("W1on", w1on), ("W1off", w1off), ("W1h", w1h), ("W1r", w1r))}
    say("   (D2) the nav law rebuilt from the recorded fields equals the recorded NAV on every (step, row): " + ", ".join(f"{k} {v['navok']}" for k, v in D.items()))
    assert all(v["navok"] for v in D.values())
    con, coff = ph32.cls3(t1on), ph32.cls3(t1off); outv = (coff == 0) & (con != 0); vab = ph32.v_absent(t1off); lost1 = ph32.lost_t1(t1on)

    say("\n== (A1) what is held, and how holds end (D3) ==")
    for tag, o, d in (("T1D Agent15 D on", t1on, D["T1on"]), ("T1 Agent15 D off", t1off, D["T1off"]), ("W1D Agent15 D on", w1on, D["W1on"]), ("W1 Agent15 D off", w1off, D["W1off"]),
                      ("W1D release-off D on", w1r, D["W1r"])):
        hold_lines(tag, o, d)
    hold_lines("T1D Agent15 D on, the 122 (m) rows", t1on, D["T1on"], vab); hold_lines("T1 Agent15 D off, the 122 (m) rows", t1off, D["T1off"], vab)

    say("\n== (A2) nav events by source (D2), and the cast clock on D whiffs ==")
    for tag, o, d in (("T1D Agent15 D on", t1on, D["T1on"]), ("T1 Agent15 D off", t1off, D["T1off"]), ("W1D Agent15 D on", w1on, D["W1on"]), ("W1 Agent15 D off", w1off, D["W1off"]),
                      ("W1D hold-not-read D on (read hold HR)", w1h, D["W1h"]), ("W1D release-off D on", w1r, D["W1r"])):
        nav_lines(tag, o, d)
    nav_lines("T1D Agent15 D on, the 122 (m) rows", t1on, D["T1on"], vab); nav_lines("T1D Agent15 D on, the 278 V-always-present rows", t1on, D["T1on"], ~vab)

    say("\n== (A3) presence by the counters and the filter's top set ==")
    for tag, d in (("T1D Agent15 D on", D["T1on"]), ("T1 Agent15 D off", D["T1off"]), ("W1D Agent15 D on", D["W1on"]), ("W1 Agent15 D off", D["W1off"])):
        presence_lines(tag, d)
    presence_lines("T1D Agent15 D on, the 122 (m) rows", D["T1on"], vab)

    say("\n== (A4) trajectory consequence (first D event = first D hold or first D-driven nav, D-on run; D4, D5) ==")
    traj_lines(f"T1D rows out of V (V in D off, not V in D on)", t1on, t1off, D["T1on"], D["T1off"], outv)
    traj_lines(f"T1D rows lost in D on (no whiff of either plume on {T - T//3}-599)", t1on, t1off, D["T1on"], D["T1off"], lost1)
    traj_lines("T1D the 122 (m) rows", t1on, t1off, D["T1on"], D["T1off"], vab)
    traj_lines("T1D the 278 V-always-present rows", t1on, t1off, D["T1on"], D["T1off"], ~vab)
    traj_lines("W1D all rows (every row lost)", w1on, w1off, D["W1on"], D["W1off"], np.ones(D["W1on"]["n"], bool))

    say("\n== (A5) W1D surge accounting (D6) ==")
    drv_on, _, _ = surge_lines("W1D Agent15 D on", w1on, D["W1on"]); drv_off, _, _ = surge_lines("W1 Agent15 D off", w1off, D["W1off"])
    surge_lines("W1D hold-not-read D on", w1h, D["W1h"]); surge_lines("W1D release-off D on", w1r, D["W1r"])
    exit_lines("W1D Agent15 D on", w1on, D["W1on"], drv_on); exit_lines("W1 Agent15 D off", w1off, D["W1off"], drv_off)
    surge_lines("T1D Agent15 D on, rows out of V", t1on, D["T1on"], outv); surge_lines("T1 Agent15 D off, the same rows", t1off, D["T1off"], outv)

    say("\n== (B) the (m) rows (D7) ==")
    m_lines(t1on, t1off, D["T1on"], D["T1off"])

    say("\n== (C) the W1D loss paths, four arms (and Agent15g beside) ==")
    c_lines(res)
    say("\n== end: measurement only; no rule, parameter, bar or arm changed; bench seeds only; H27's verdict (stopped at the bench) unchanged ==")
    text = "\n".join(_lines) + "\n"
    nums = ph32.seed_numbers(); pat = re.compile(r"(?<!\d)(" + "|".join(map(str, nums)) + r")(?!\d)")
    hits = sorted(set(pat.findall(text)) | set(pat.findall(open(__file__, encoding="utf-8").read())))
    if hits: print(f"== a registered seed number appears in the output or in ph32b.py: {hits}; output NOT written =="); raise SystemExit(6)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f: f.write(text)
    print(f"written {OUT} sha256 {sha(OUT)}")


if __name__ == "__main__":
    main()
