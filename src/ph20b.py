#!/usr/bin/env python3
"""H22 post-bench diagnosis (measurement only; owner 2026-09-23, decision:h22-post-bench-diagnosis).

ph20.py (sha256 checked below), design v1 FINAL and the bench verdict (M4 FAIL on (d), no candidate,
record:h22-bench-result) are untouched: Agent7's rule, every bar and every adopted module are imported
as they are. Bench seeds only (ph20.BENCH seed_w / seed_a; not written out here, so ph20's seed check stays valid); the
development and evaluation seeds are not used. This file builds the bench (d) constructed state line for line as ph20.bench_d does and
only records states around each World7.sense / Agent7.act call.

Identity first: with the registered 300-step protocol, holding the valued odour at step 300 must be
84/400 with the rule and 5/400 without, equal to ph20.bench_d re-run here; the extended runs are the same
runs continued (fixed-size draws per step, so their first 300 steps are the bench's steps).

(1) revision against time, registered start, to 900 steps, rule on and off
(2) what flips the neutral hold: every valued whiff arriving while the neutral odour is held; (2b) hold transitions
(3) the loop: upwind excursion, returns to the neutral source, first entry into the valued cone
(4) where the first valued whiffs come from (plume core vs cone edge) and the whiff probability there
(5) VARIANT start, NOT the bench: on the neutral axis DOWN (20) downwind of the neutral source, heading
    upwind, neutral hold constructed, cast clock 0 as after a fresh hit; 600 steps, rule on and off
(6) per arm: rows with no whiff of either plume in the last 100 steps at 300 and 600, wall contacts
Names no cause beyond what is measured; tests no change.
"""
import sys, hashlib
import numpy as np
import ph20
from ph16 import World7, cast_draw, interval, DOWN
from ph9 import UPWIND, W0, SLOPE, LMAX, LAM

sys.stdout.reconfigure(newline="\n")            # LF output on Windows, so the recorded sha256 survives git's eol=lf
PH20_SHA = "edec6d834860cc6c4c0ac361998fe09405344b2e494aef21a28b04ca7b6cefbe"
EXPECT = {True: 84, False: 5}                    # ph20_bench.txt, bench (d), step 300
CHECK = (100, 150, 200, 250, 300, 400, 500, 600, 750, 900)
NEAR, FAR, CORE, WIN = 5.0, 10.0, 3.0, 10       # return = within NEAR after having been beyond FAR; core = |d_cross| < CORE
P_HIT = 0.3                                      # World2's p_hit (ph11), the cone's whiff probability at d_along 0


def sha(): return hashlib.sha256(open(__file__, "rb").read()).hexdigest()
def q3(x): return f"{np.percentile(x, 25):.1f} / {np.median(x):.1f} / {np.percentile(x, 75):.1f}" if len(x) else "n/a"


def simulate(resample, steps, start):
    B = ph20.BENCH; sw, sa, n = B["seed_w"], B["seed_a"], B["rows"]
    w = World7(n, np.random.default_rng(sw), sw); r = np.arange(n); good = w.good; neutral = 1 - good
    kv = np.zeros((n, 2)); kv[r, good] = 1.0
    a = ph20.Agent7(n, np.random.default_rng(sa), G=ph20.G_STAR, known=kv, rule=True, resample=resample); a.cast_sign = cast_draw(sa, n)
    if start == "bench":
        w.pos = w.src[r, neutral].copy()                                        # as ph20.bench_d
    else:                                                                       # VARIANT, not the bench
        w.pos = w.src[r, neutral] + np.array([DOWN, 0.0]); w.head = np.full(n, UPWIND)
    a.sel.s[r, neutral] = 2.0
    o = dict(good=good, src=w.src.copy(), steps=steps, H=np.zeros((steps, n), np.int8), W=np.zeros((steps, n, 2), bool),
             P=np.zeros((steps, n, 2)), s0=np.zeros((steps, n, 2)), S0=np.zeros((steps, n)), C0=np.zeros((steps, n)), CT=np.zeros((steps, n)))
    c = np.zeros(n)
    for t in range(steps):
        o["P"][t] = w.pos; o["s0"][t] = a.sel.s; o["S0"][t] = a.sel.S[:, 0]; o["C0"][t] = a.since       # state when the step's whiffs arrive
        whiffs = w.sense(); turn, h = a.act(w, whiffs, w.wind_on())
        o["H"][t] = h; o["W"][t] = whiffs
        w.move(turn); a.bump(w.bumped); c = c + w.bumped; o["CT"][t] = c
    return o


def basics(o):
    n = len(o["good"]); r = np.arange(n); g = o["good"]
    hv = o["H"] == g[None, :]; wv = o["W"][:, r, g]
    return n, r, g, 1 - g, hv, wv


def revision(o, label):
    n, r, g, ng, hv, wv = basics(o); T = o["steps"]
    prev = np.vstack([np.full((1, n), -1, np.int8), o["H"][:-1]]); vend = (prev == g[None, :]) & (o["H"] != g[None, :])
    print(f"   {label}")
    print("      step | holding valued at t        | ever revised by t | >=1 valued whiff by t | revised, not holding at t | a valued hold ended by t | P(holding | >=1 valued whiff)")
    for t in CHECK:
        if t > T: continue
        hold = hv[t - 1]; ever = hv[:t].any(0); got = wv[:t].any(0); ended = vend[:t].any(0)
        k, p, lo, hi = interval("P", hold)
        ci = f" [{lo:.3f}, {hi:.3f}]" if t in (300, 600) else ""
        print(f"      {t:4d} | {k:3d}/{n} = {p:.3f}{ci:17s} | {int(ever.sum()):3d}               | {int(got.sum()):3d}                   | {int((ever & ~hold).sum()):3d}"
              f"                       | {int(ended.sum()):3d}                      | {hold[got].mean() if got.any() else float('nan'):.3f}")


def flips(o, label):
    n, r, g, ng, hv, wv = basics(o); H, T = o["H"], o["steps"]
    prev = np.vstack([ng[None, :].astype(np.int8), H[:-1]])                  # held before step 0: the constructed neutral hold
    ev = wv & (prev == ng[None, :])
    cw = np.vstack([np.zeros((1, n), int), np.cumsum(wv, 0)]); ch = np.vstack([np.zeros((1, n), int), np.cumsum(hv, 0)])
    cn = np.vstack([np.zeros((1, n), int), np.cumsum(H < 0, 0)])
    ts, rs = np.nonzero(ev); keep = ts <= T - WIN; ts, rs = ts[keep], rs[keep]
    n5 = cw[ts + 1, rs] - cw[np.maximum(ts - 4, 0), rs]; n10 = cw[ts + 1, rs] - cw[np.maximum(ts - 9, 0), rs]
    after = cw[np.minimum(ts + WIN, T), rs] - cw[ts + 1, rs]                 # further valued whiffs in the next 9 steps
    flip = (ch[ts + WIN, rs] - ch[ts, rs]) > 0; rel = ~flip & ((cn[ts + WIN, rs] - cn[ts, rs]) > 0)
    sh, sv, S = o["s0"][ts, rs, ng[rs]], o["s0"][ts, rs, g[rs]], o["S0"][ts, rs]
    print(f"   {label}: valued whiffs arriving while the neutral odour is held (events with a full {WIN}-step window): {len(ts)} in {len(set(rs))} rows;"
          f" flipped to the valued odour within {WIN} steps {int(flip.sum())} = {flip.mean() if len(ts) else float('nan'):.3f};"
          f" not flipped but the hold released (nothing held) at some step {int(rel.sum())}; neutral kept all {WIN} steps {int((~flip & ~rel).sum())}")
    if not len(ts): return
    print(f"      at arrival: held (neutral) unit s median {np.median(sh):.2f} [{np.percentile(sh, 5):.2f}, {np.percentile(sh, 95):.2f}], valued unit s median {np.median(sv):.3f},"
          f" pool S median {np.median(S):.2f}")
    for name, x in (("valued whiffs in the 5 steps up to and including it", n5), ("... in the 10 steps", n10)):
        cells = [(k, (x == k) if k < 3 else (x >= 3)) for k in (1, 2, 3)]
        print(f"      by {name}: " + "; ".join(f"{'3+' if k == 3 else k}: {int(flip[m].sum())}/{int(m.sum())} = {flip[m].mean() if m.any() else float('nan'):.3f}" for k, m in cells))
    wn = o["W"][:, r, ng]; cwn = np.vstack([np.zeros((1, n), int), np.cumsum(wn, 0)]); nn20 = cwn[ts + 1, rs] - cwn[np.maximum(ts - 19, 0), rs]
    last = np.full(n, -10**6); LN = np.zeros((T, n), int)
    for t in range(T): last = np.where(wn[t], t, last); LN[t] = last
    gap = ts - LN[ts, rs]; gap = np.where(gap > T, T + 1, gap)                  # T + 1: no neutral whiff yet
    print(f"      neutral whiffs in the 20 steps up to it: flipped mean {nn20[flip].mean() if flip.any() else float('nan'):.2f}, not flipped {nn20[~flip].mean():.2f};"
          f" steps since the last neutral whiff: flipped median {np.median(gap[flip]) if flip.any() else float('nan'):.0f}, not flipped median {np.median(gap[~flip]):.0f}")
    k = np.arange(1, WIN)[:, None]; sv_pk = o["s0"][ts[None, :] + k, rs[None, :], g[rs][None, :]].max(0); sh_lo = o["s0"][ts[None, :] + k, rs[None, :], ng[rs][None, :]].min(0)
    end = H[ts + WIN - 1, rs]; cat = lambda m: f"neutral {int((m & (end == ng[rs])).sum())}, nothing {int((m & (end < 0)).sum())}, valued {int((m & (end == g[rs])).sum())}"
    print(f"      released but not flipped ({int(rel.sum())}): hold at the 10th step {cat(rel)}; over the next 9 steps the valued unit's peak s median"
          f" {np.median(sv_pk[rel]) if rel.any() else float('nan'):.2f} (flipped {np.median(sv_pk[flip]) if flip.any() else float('nan'):.2f}), the neutral unit's lowest s median"
          f" {np.median(sh_lo[rel]) if rel.any() else float('nan'):.2f} (flipped {np.median(sh_lo[flip]) if flip.any() else float('nan'):.2f})")
    iso = (n10 == 1) & (after == 0)
    print(f"      isolated whiff (no other valued whiff in the 9 steps before or the 9 after): {int(flip[iso].sum())}/{int(iso.sum())} = {flip[iso].mean() if iso.any() else float('nan'):.3f};"
          f" not isolated {int(flip[~iso].sum())}/{int((~iso).sum())} = {flip[~iso].mean() if (~iso).any() else float('nan'):.3f}")
    bins = (0.0, 1.5, 1.8, 2.0, 2.2, 2.5, 5.1)
    print("      by the held unit's s at arrival: " + "; ".join(
        f"[{a:.1f}, {b:.1f}): {int(flip[(sh >= a) & (sh < b)].sum())}/{int(((sh >= a) & (sh < b)).sum())}" for a, b in zip(bins[:-1], bins[1:])))
    fv = np.where(wv.any(0), wv.argmax(0), -1); m = fv >= 0; rr = r[m]; tf = fv[m]
    held_n = prev[tf, rr] == ng[rr]; ok = tf <= T - WIN
    fl = (ch[np.minimum(tf + WIN, T), rr] - ch[tf, rr]) > 0; single = (cw[np.minimum(tf + WIN, T), rr] - cw[tf, rr]) == 1
    print(f"      first valued whiff per row: {int(m.sum())} rows (neutral held at it {int(held_n.sum())}); flipped within {WIN} steps {int(fl.sum())}, not {int((~fl).sum())}"
          f" (rows with a full window {int(ok.sum())}); when it was the only valued whiff in its {WIN}-step window: flipped {int((fl & single).sum())}/{int(single.sum())},"
          f" when more followed: {int((fl & ~single).sum())}/{int((~single).sum())}")


def transitions(o, label):
    """(2b) hold transitions (0 nothing, N neutral, V valued; before step 0 the constructed neutral hold) and every
    stretch of 'nothing held' that follows a neutral hold: how it ends, how long it lasts, which whiffs arrive in it"""
    n, r, g, ng, hv, wv = basics(o); H, T = o["H"], o["steps"]; wn = o["W"][:, r, ng]
    lab = np.vstack([np.ones((1, n), int), np.where(H == g[None, :], 2, np.where(H == ng[None, :], 1, 0))])
    L = ("0", "N", "V"); tr = {}
    out = []                                                                   # (outcome, duration, valued whiffs, neutral whiffs)
    first_rev = []                                                             # state before the first valued hold
    for j in range(n):
        x = lab[:, j]; ch = np.nonzero(x[1:] != x[:-1])[0] + 1               # indices in lab where the state changes
        for i in ch: tr[(x[i - 1], x[i])] = tr.get((x[i - 1], x[i]), 0) + 1
        v = np.nonzero(x == 2)[0]
        if len(v): first_rev.append(x[v[0] - 1])
        for i in ch:
            if x[i - 1] == 1 and x[i] == 0:
                nxt = ch[ch > i]; e = nxt[0] if len(nxt) else T + 1              # lab index of the next change (or past the end)
                out.append((x[e] if e <= T else -1, e - i, int(wv[i - 1:e - 1, j].sum()), int(wn[i - 1:e - 1, j].sum())))
    print(f"   {label}: transitions " + ", ".join(f"{L[a]}->{L[b]} {c}" for (a, b), c in sorted(tr.items())))
    fr = np.array(first_rev)
    print(f"      first valued hold per row ({len(fr)} rows): entered from nothing held {int((fr == 0).sum())}, directly from the neutral hold {int((fr == 1).sum())}")
    if not out: return
    oc, du, nv, nn = (np.array(z) for z in zip(*out))
    parts = []
    for name, k in (("valued", 2), ("neutral again", 1), ("still nothing at the end", -1)):
        m = oc == k
        parts.append(f"{name} {int(m.sum())} (duration quartiles {q3(du[m])}; valued whiffs in it mean {nv[m].mean() if m.any() else float('nan'):.2f},"
                     f" neutral whiffs mean {nn[m].mean() if m.any() else float('nan'):.2f})")
    print(f"      'nothing held' stretches after a neutral hold: {len(oc)}; ended by " + "; ".join(parts))


def geometry(o):
    n, r, g, ng, hv, wv = basics(o); P = o["P"]; sn, sv = o["src"][r, ng], o["src"][r, g]
    da = P[..., 0] - sn[None, :, 0]                                           # > 0 downwind (wind toward +x)
    sgn = np.sign(sv[:, 1] - sn[:, 1]); dc = (P[..., 1] - sn[None, :, 1])*sgn[None, :]   # > 0 toward the valued source
    dcv = np.abs(P[..., 1] - sv[None, :, 1])                                  # the sources share x: d_along is the same for both
    incone = ((da > 0) & (da < LMAX) & (dcv < W0 + SLOPE*da)) | (np.hypot(da, dcv) < 3.0)
    return da, dc, dcv, incone


def loop(o, label, T=600):
    n, r, g, ng, hv, wv = basics(o); T = min(T, o["steps"]); da, dc, dcv, incone = geometry(o)
    da, dc, dcv, incone, wv = da[:T], dc[:T], dcv[:T], incone[:T], wv[:T]; dist = np.hypot(da, dc)
    far = np.zeros(n, bool); cnt = np.zeros(n, int); fr = np.full(n, -1)
    for t in range(T):
        far |= dist[t] > FAR; now = far & (dist[t] <= NEAR); cnt += now; fr = np.where((fr < 0) & now, t, fr); far &= ~now
    up = np.maximum(-da, 0).max(0); fc = np.where(incone.any(0), incone.argmax(0), -1); fv = np.where(wv.any(0), wv.argmax(0), -1)
    print(f"   {label} (first {T} steps; positions relative to the neutral source, d_along > 0 downwind, d_cross > 0 toward the valued source)")
    print(f"      max upwind excursion (quartiles) {q3(up)}; rows beyond 20 upwind {int((up > 20).sum())}")
    print(f"      first return within {NEAR} of the neutral source after being beyond {FAR}: rows {int((fr >= 0).sum())}/{n}, step quartiles {q3(fr[fr >= 0])};"
          f" returns per row quartiles {q3(cnt)}, rows with 0/1/2/3+ returns {int((cnt == 0).sum())}/{int((cnt == 1).sum())}/{int((cnt == 2).sum())}/{int((cnt >= 3).sum())}")
    print(f"      first entry into the valued cone (or within 3.0 of the valued source): rows {int((fc >= 0).sum())}, step quartiles {q3(fc[fc >= 0])};"
          f" steps in the valued cone per row quartiles {q3(incone.sum(0))}")
    m = fv >= 0; rr = r[m]; tf = fv[m]
    if not m.any(): print("      no valued whiff"); return
    a_, c_, v_, k_ = da[tf, rr], dc[tf, rr], dcv[tf, rr], o["C0"][tf, rr]
    print(f"      at the first valued whiff ({int(m.sum())} rows): step quartiles {q3(tf)}; d_along {q3(a_)}; d_cross from the neutral axis {q3(c_)};"
          f" |d_cross| to the valued axis {q3(v_)}; cast clock (steps since the last navigation hit) {q3(k_)}")
    src_at = np.hypot(a_, v_) < 3.0; core = ~src_at & (v_ < CORE); edge = ~src_at & ~core
    ma, mv = np.median(a_), np.median(v_); half = W0 + SLOPE*ma; pm = P_HIT*np.exp(-max(ma, 0.0)/LAM) if (0 < ma < LMAX and mv < half) else 0.0
    pr = P_HIT*np.exp(-np.maximum(a_, 0.0)/LAM)
    print(f"      where it came from: within 3.0 of the valued source {int(src_at.sum())}, plume core (|d_cross| < {CORE}) {int(core.sum())}, cone edge {int(edge.sum())};"
          f" at the median arrival position (d_along {ma:.1f}, |d_cross| {mv:.1f}; cone half-width there {half:.1f}) the per-step whiff probability is"
          f" {pm:.3f} (p_hit {P_HIT} x exp(-d_along/{LAM:.0f})); per-row value at arrival quartiles {q3(pr)}")


def silence(o, label):
    n = len(o["good"]); W, CT, T = o["W"], o["CT"], o["steps"]
    parts = [f"t {t}: no whiff of either plume in the last 100 steps {int((~W[t - 100:t].any((0, 2))).sum())}, wall contacts {int(CT[t - 1].sum())}" for t in (300, 600, 900) if t <= T]
    print(f"   {label}: " + "; ".join(parts))


def main():
    assert ph20.sha() == PH20_SHA, f"ph20.py changed: {ph20.sha()}"
    B = ph20.BENCH
    print(f"== H22 post-bench diagnosis (measurement only). this file sha256 {sha()}; ph20.py sha256 {ph20.sha()}; design {ph20.DESIGN};"
          f" the bench seeds (ph20.BENCH seed_w / seed_a), {B['rows']} rows; no other seed used ==")
    print("\n(0) identity: the registered 300-step protocol (bench (d)) re-run")
    runs = {}
    for rs in (True, False):
        o = simulate(rs, 900, "bench"); runs[rs] = o; n, r, g, ng, hv, wv = basics(o)
        k = int(hv[299].sum()); kb = ph20.bench_d(rs, quiet=True)[2]
        w3 = wv[:300]; fv = np.where(w3.any(0), w3.argmax(0), -1); rv = np.where(hv[:300].any(0), hv[:300].argmax(0), -1)
        print(f"   rule {'on ' if rs else 'off'}: holding the valued odour at step 300 here {k}/{n}, ph20.bench_d {kb}/{n}, ph20_bench.txt {EXPECT[rs]}/{n} -> {k == kb == EXPECT[rs]};"
              f" rows with >=1 valued whiff by 300 {int(w3.any(0).sum())}, per row {w3.sum(0).mean():.2f}; first valued whiff median {np.median(fv[fv >= 0]) if (fv >= 0).any() else float('nan'):.0f},"
              f" revision median {np.median(rv[rv >= 0]) if (rv >= 0).any() else float('nan'):.0f}")
        assert k == kb == EXPECT[rs], "the bench is not reproduced"
    print("\n(1) revision against time, REGISTERED start (placed at the neutral source, World7 heading draw, neutral hold s 2.0 / 0, S 0), 900 steps")
    for rs in (True, False): revision(runs[rs], f"rule {'on' if rs else 'off'}")
    print("\n(2) what flips the neutral hold, registered start, 900 steps")
    for rs in (True, False): flips(runs[rs], f"rule {'on' if rs else 'off'}")
    print("\n(2b) hold transitions and the 'nothing held' route, registered start, 900 steps")
    for rs in (True, False): transitions(runs[rs], f"rule {'on' if rs else 'off'}")
    print("\n(3)+(4) the loop and where the valued whiffs come from, registered start")
    for rs in (True, False): loop(runs[rs], f"rule {'on' if rs else 'off'}")
    print("\n(5) VARIANT start, NOT the bench (a different constructed state): on the neutral axis 20 downwind of the neutral source, heading upwind (180),"
          " neutral hold s 2.0 / 0, S 0, cast clock 0; same seeds and rows; 600 steps")
    var = {rs: simulate(rs, 600, "variant") for rs in (True, False)}
    for rs in (True, False): revision(var[rs], f"VARIANT rule {'on' if rs else 'off'}")
    for rs in (True, False): flips(var[rs], f"VARIANT rule {'on' if rs else 'off'}")
    for rs in (True, False): transitions(var[rs], f"VARIANT rule {'on' if rs else 'off'}")
    for rs in (True, False): loop(var[rs], f"VARIANT rule {'on' if rs else 'off'}")
    print("\n(6) silence and walls")
    for rs in (True, False): silence(runs[rs], f"registered start, rule {'on ' if rs else 'off'}")
    for rs in (True, False): silence(var[rs], f"VARIANT start,    rule {'on ' if rs else 'off'}")


if __name__ == "__main__":
    main()
