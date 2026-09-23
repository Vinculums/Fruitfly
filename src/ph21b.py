#!/usr/bin/env python3
"""Option-v presence diagnosis (measurement only; owner 2026-09-23, decision:filter-scope-explore-option-v).

Usage: python ph21b.py

Measures what 'evidence the agent already has' can mean for a presence-scoped v_max (H24, option v), on EXISTING
agents only: ph21.Agent8 (the adopted filter), ph19.Agent6 (maintain), ph2.Upstream. No new rule is run in any arm;
every presence rule below is applied offline to recorded trajectories (a counterfactual re-labelling, an upper-bound
proxy: under the new rule the trajectories would change after the first re-labelled step). ph21.py and ph22.py are
imported unchanged (sha256 checked). Seeds: the H23 development seeds (ph21.SEEDS['dev']) and the absent-check
development seeds (ph22.SEEDS['dev']); stub draws from ph21.BENCH / ph19.BENCH seeds. None is written out here, so
the earlier seed self-checks are not disturbed by this file or its output. Evaluation seeds are not touched.

(1) upstream decay: one whiff, a 20-step p 0.3 burst, a 20-step p 1 burst; the non-held unit's s while the other is
    held (H21 bench (a) protocol)
(2) H21 task, filter and maintain arms: first valued / neutral whiff; neutral-first rows; steps since the last valued
    whiff while the neutral odour is held
(3) W1 (absent world): the absent odour's upstream state; Agent8 / Agent6 reach and dwell as reference
(4) counterfactual re-labelling of the filter's `differs` steps per window N and per strict threshold theta
(5) EXACT identity bounds: per row, whether a scoped agent would be bitwise Agent6 or bitwise Agent8 over the whole run
    (start OFF: plain window, strict threshold; start ON: 'prior + window'); W1 under both
"""
import sys, hashlib
import numpy as np
import ph19, ph21, ph22
from ph2 import Upstream
from ph16 import Still, diagnostics, R, T
from ph19 import Agent6
from ph21 import Agent8, G_STAR, first_true

sys.stdout.reconfigure(newline="\n")            # LF output, so the recorded sha256 equals the committed blob
PH21_SHA = "3a1d79d9a0d235f1bef7e435ec594cff4048180e27b28dcd892598c58413cfc1"   # the version H23 ran
PH22_SHA = "03ab8c4706b19557af5d64edd83f812abba91b618439618b35837a49dd44ca1c"   # the version the absent-odour check ran
UP = dict(n=1.5, sig=0.05, Rmax=1.8, k=0.8)      # ph11.py line 112 (tau: ph2.Upstream's default 2.0); checked against the agent below
THETAS = (1e-3, 1e-6)
NS = (5, 10, 20, 40, 60, 100, 150, 200, 300, 600)
NEVER = 10**6


def sha(p=__file__): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def q(x, f=".0f"): return f"{np.percentile(x, 25):{f}}/{np.median(x):{f}}/{np.percentile(x, 75):{f}}" if len(x) else "n/a"
def pct(x, ps=(50, 75, 90, 95, 99)): return " ".join(f"p{p} {np.percentile(x, p):.0f}" for p in ps) if len(x) else "n/a"


def since_last(m):
    """m (steps, rows) bool -> steps since the last True at or before t (0 on a True step; NEVER before the first)"""
    out = np.empty(m.shape, np.int64); last = np.full(m.shape[1], -NEVER)
    for t in range(m.shape[0]):
        last = np.where(m[t], t, last); out[t] = np.where(last < 0, NEVER, t - last)
    return out


def offline_P(W):
    """the agent's upstream state P per step, recomputed from its recorded whiffs (P after the step's update)"""
    up = Upstream(runs=W.shape[1], chans=2, **UP); P = np.empty(W.shape)
    for t in range(W.shape[0]): up.step(W[t].astype(float)); P[t] = up.P
    return P


def longest_false(m):
    best = np.zeros(m.shape[1], int); cur = np.zeros(m.shape[1], int)
    for t in range(m.shape[0]): cur = np.where(m[t], 0, cur + 1); best = np.maximum(best, cur)
    return best


# ------------------------------------------------------------------ (1) upstream decay
def part1():
    print("\n== (1) upstream decay (ph2.Upstream as the agent has it) ==")
    a = Agent8(4, np.random.default_rng(0), G=G_STAR, known=np.tile([1.0, 0.0], (4, 1)), rule=True, filt=True)
    same = (a.up.n, a.up.sig_n, a.up.Rmax, a.up.k, a.up.tau) == (UP["n"], UP["sig"]**UP["n"], UP["Rmax"], UP["k"], 2.0)
    print(f"   parameters equal to Agent8's upstream stage (n, sig^n, Rmax, k, tau 2.0): {same}; form: P += (1/tau)(-P + x^n), so with no input P halves exactly every step"
          f" (tau 2), and y = Rmax P / (sig^n + P + k P_other); sig^n = {UP['sig']**UP['n']:.5f}")
    assert same
    up = Upstream(runs=1, chans=2, **UP); rec = []
    for t in range(2000):
        y = up.step(np.array([[1.0 if t == 0 else 0.0, 0.0]])); rec.append((up.P[0, 0], y[0, 0]))
        if up.P[0, 0] == 0.0: break
    P = np.array([r[0] for r in rec]); Y = np.array([r[1] for r in rec])
    print("   one whiff on channel 0 at step 0, then silence; per step (P_0, y_0), steps 0-59:")
    for s in range(0, 60, 10): print("     " + "  ".join(f"{t}:({P[t]:.3g},{Y[t]:.3g})" for t in range(s, min(s + 10, len(P)))))
    for th in THETAS: print(f"   P_0 first below {th:g} at step {int(np.argmax(P < th))} (present on steps 0..{int(np.argmax(P < th)) - 1}, a window of {int(np.argmax(P < th))} steps incl. the whiff step)")
    print(f"   P_0 exactly 0 first at step {len(P) - 1 if P[-1] == 0 else 'not within 2000'} (float64 underflow: the halving reaches the smallest subnormal); y_0 below 0.01 (the circuit's noise sd) at step {int(np.argmax(Y < 0.01))},"
          f" below 0.001 at step {int(np.argmax(Y < 1e-3))}")
    u = np.random.default_rng(ph21.BENCH["seed_w"]).random((20, 400))
    for lab, burst in (("20-step p 0.3 burst", u < 0.3), ("20-step p 1 burst", np.ones((20, 400), bool))):
        up = Upstream(runs=400, chans=2, **UP); below = {th: np.full(400, -1) for th in THETAS}; z = np.full(400, -1)
        for t in range(20 + 2000):
            x = np.zeros((400, 2)); x[:, 0] = burst[t] if t < 20 else 0.0; up.step(x)
            if t >= 19:
                for th in THETAS: below[th] = np.where((below[th] < 0) & (up.P[:, 0] < th), t - 19, below[th])
                z = np.where((z < 0) & (up.P[:, 0] == 0.0), t - 19, z)
        rows = burst.any(0)
        print(f"   {lab} on channel 0 (400 rows, rows with a whiff {int(rows.sum())}), steps after the burst's last step until P_0 < theta: "
              + "; ".join(f"{th:g}: {q(below[th][rows])} (max {below[th][rows].max()})" for th in THETAS) + f"; exactly 0: {q(z[rows])}")
    print("   the non-held unit's s while the other odour is held (H21 bench (a) protocol: 60 steps channel 0 p 0.30 then 200 steps channel 0 silent,"
          " channel 1 at p_other; Agent6, G 2, gate on; ph19 bench draws):")
    for po in ph19.BENCH["p_other"]:
        r = ph19.bench_run(Agent6, G_STAR, True, [1.0, 0.0], [(ph19.BENCH["phase1"], ph19.BENCH["p_hold"], 0.0), (ph19.BENCH["phase2"], 0.0, po)])
        h = r["H"]; s1 = r["S"][:, :, 1]; s0 = r["S"][:, :, 0]; m = h == 0; m2 = m.copy(); m2[:ph19.BENCH["phase1"]] = False
        print(f"     p_other {po}: (row, step) holding channel 0: {int(m.sum())}; channel 1's s there median {np.median(s1[m]):.4f} p99 {np.percentile(s1[m], 99):.4f} max {s1[m].max():.4f};"
              f" in phase 2 only median {np.median(s1[m2]):.4f} max {s1[m2].max():.4f} (held unit's s median {np.median(s0[m]):.2f}); hold threshold 1.0"
              f" (channel 1, value 0 < 1, is gated to 0 while channel 0 is held, so p_other cannot matter)")
    print("   reverse (the task's trap state): 60 steps channel 1 (value 0) p 0.30, then 200 steps channel 1 silent and channel 0 (value 1) at p_other; the valued unit's s"
          " while the neutral odour is still held:")
    for po in ph19.BENCH["p_other"]:
        r = ph19.bench_run(Agent6, G_STAR, True, [1.0, 0.0], [(ph19.BENCH["phase1"], 0.0, ph19.BENCH["p_hold"]), (ph19.BENCH["phase2"], po, 0.0)])
        h = r["H"]; s0 = r["S"][:, :, 0]; p1 = ph19.BENCH["phase1"]; m2 = np.zeros_like(h, bool); m2[p1:] = h[p1:] == 1
        kept = (h[p1 - 1] == 1); left = np.where(kept, first_true(h[p1:] != 1), -1)
        print(f"     p_other {po}: rows holding channel 1 at step {p1} {int(kept.sum())}; phase-2 steps until that hold ends {q(left[kept & (left >= 0)])} (never {int((kept & (left < 0)).sum())});"
              f" valued unit's s while channel 1 still held in phase 2: median {np.median(s0[m2]) if m2.any() else float('nan'):.4f} max {s0[m2].max() if m2.any() else float('nan'):.4f}")
    return P


# ------------------------------------------------------------------ (2) and (4): the H21 task on the H23 development seeds
def part2(o, name):
    n = len(o["good"]); r = np.arange(n); g = o["good"]
    wv = o["W"][:, r, g]; wn = o["W"][:, r, 1 - g]; fv = first_true(wv); fn = first_true(wn); d = diagnostics(o)
    L = since_last(wv); hn = o["H"] == (1 - g)[None, :]
    nf = d["fh_n"]
    print(f"\n   [{name}] first valued whiff step {q(fv[fv >= 0])} (never {int((fv < 0).sum())}); first neutral whiff {q(fn[fn >= 0])} (never {int((fn < 0).sum())});"
          f" rows whose first whiff is neutral only {int(((fn >= 0) & ((fv < 0) | (fn < fv))).sum())}, valued only {int(((fv >= 0) & ((fn < 0) | (fv < fn))).sum())},"
          f" both on the same step {int(((fv >= 0) & (fv == fn)).sum())}")
    print(f"      rows whose first valued whiff is within N steps of the start (step < N): " + ", ".join(f"N {N}: {int(((fv >= 0) & (fv < N)).sum())}/{n} = {((fv >= 0) & (fv < N)).mean():.3f}" for N in (10, 20, 40, 60, 100)))
    ft = d["ft"]; gap = np.full(n, -1)
    for i in np.where(nf)[0]:
        after = np.where(wv[ft[i]:, i])[0]; gap[i] = after[0] if len(after) else -1
    had = nf & (gap >= 0)
    print(f"      neutral-first rows (first hold neutral) {int(nf.sum())}: first hold step {q(ft[nf])}; first valued whiff at or after the first hold, gap {q(gap[had])} steps"
          f" (p90 {np.percentile(gap[had], 90) if had.any() else float('nan'):.0f}, never {int((nf & (gap < 0)).sum())}); valued whiff before the first hold in {int((nf & (fv >= 0) & (fv < ft)).sum())};"
          f" longest run without a valued whiff in steps 0-199 {q(longest_false(wv[:200])[nf])} (max {longest_false(wv[:200])[nf].max() if nf.any() else 0})")
    Lh = L[hn]; nev = Lh >= NEVER
    print(f"      (row, step) holding the neutral odour {int(hn.sum())} in {int(hn.any(0).sum())} rows: steps since the last valued whiff (0 = this step) {pct(Lh[~nev])}, max {Lh[~nev].max() if (~nev).any() else 0};"
          f" no valued whiff yet {int(nev.sum())} ({nev.mean():.3f}); fraction with the last valued whiff more than N-1 steps ago (incl. never): "
          + ", ".join(f"N {N} {(Lh > N - 1).mean():.3f}" for N in (10, 20, 40, 60, 100, 200)))
    return dict(wv=wv, L=L, fv=fv, fn=fn, d=d)


def part4(o8, m8, o6):
    print("\n== (4) counterfactual re-labelling of the filter's actions (filter arm, H23 dev seeds). An UPPER-BOUND PROXY, not a simulation:"
          " under a presence rule the trajectory would follow Agent6's after the first re-labelled step, and later steps would differ ==")
    D = o8["DIFF"]; nav = o8["NAV"]; wv = m8["wv"]; L = m8["L"]
    nav6 = np.where(D, ~nav, nav); withheld = D & nav6 & ~nav; added = D & nav & ~nav6
    print(f"   filter actions = `differs` (row, step) {int(D.sum())} in {int(D.any(0).sum())} rows: surge withheld (Agent6 would surge, a neutral whiff) {int(withheld.sum())},"
          f" surge added (a valued whiff while the neutral odour is held and no neutral whiff) {int(added.sum())}; every added step has a valued whiff this step"
          f" {bool(wv[added].all())} (so it is kept under any presence rule)")
    P = offline_P(o8["W"]); r = np.arange(len(o8["good"])); Pv = P[:, r, o8["good"]]
    before = D & (L >= NEVER)
    print(f"   of them before the row's first valued whiff (no evidence of the valued odour yet: lost under ANY presence rule, window or threshold): {int(before.sum())}"
          f" = {before.sum() / D.sum():.3f} of the filter's actions, in {int(before.any(0).sum())} rows")
    first_diff = first_true(D); rows_d = first_diff >= 0
    fd_lost = {N: rows_d & (L[np.maximum(first_diff, 0), r] > N - 1) for N in NS}
    Vf, Vm = ph21.majority(o8)[0], ph21.majority(o6)[0]; into = Vf & ~Vm
    print("   window rule (v-c proxy: present = a valued whiff in the last N steps incl. this one): lost (row, step) and fraction; rows whose FIRST filter action is lost"
          " (from there the row would follow Agent6 until the valued odour is present); the same among the rows the filter moved into V (paired against maintain, "
          f"{int(into.sum())} rows):")
    for N in NS:
        lost = D & (L > N - 1); fr = lost.sum() / D.sum()
        print(f"     N {N:>3}: lost {int(lost.sum())} = {fr:.3f} (kept {1 - fr:.3f}); first action lost in {int(fd_lost[N].sum())}/{int(rows_d.sum())} rows; among into-V rows {int((fd_lost[N] & into).sum())}/{int(into.sum())}")
    for N in range(1, 601):
        if 1 - (D & (L > N - 1)).sum() / D.sum() >= 0.95: best = N; break
    else: best = None
    print(f"   smallest N (1..600) keeping >= 0.95 of the filter's actions: {best if best else 'none (the pre-first-valued-whiff share alone exceeds 0.05)'}")
    for th in THETAS:
        lost = D & ~(Pv > th); fdl = rows_d & ~(Pv[np.maximum(first_diff, 0), r] > th)
        print(f"   strict rule (v-a proxy: present = P_valued > {th:g}, P recomputed offline from the recorded whiffs): lost {int(lost.sum())} = {lost.sum() / D.sum():.3f};"
              f" first action lost in {int(fdl.sum())}/{int(rows_d.sum())} rows, among into-V rows {int((fdl & into).sum())}/{int(into.sum())}")
    ok = np.array_equal(D & ~(Pv > 0.0), before)
    print(f"   check: P_valued > 0 exactly on every step after the row's first valued whiff (float64, 600 steps < underflow) {ok}: with theta -> 0 the strict rule's"
          f" window is the whole run after the first valued whiff")


def part5(o8, o6, w1):
    """EXACT, not a proxy. Nav is the only thing the scoped rule changes and it consumes no random numbers, so a scoped agent is bitwise
    Agent6 up to the first step where, on Agent6's own trajectory, the valued odour is present and Agent8's nav (at +1/0: the valued whiff)
    differs from Agent6's; and bitwise Agent8 up to the first step where, on Agent8's trajectory, a filter action falls outside presence.
    (Presence includes the held odour: a held valued odour counts as evidence, so the valued-held branch is Agent8's = Agent6's.)"""
    print("\n== (5) EXACT identity bounds for a presence-scoped agent (no run of it): per row, is it bitwise Agent6 or bitwise Agent8 for all 600 steps? ==")
    r = np.arange(len(o8["good"])); g = o8["good"]
    wv6, wv8 = o6["W"][:, r, g], o8["W"][:, r, g]; L6, L8 = since_last(wv6), since_last(wv8)
    P6, P8 = offline_P(o6["W"])[:, r, g], offline_P(o8["W"])[:, r, g]
    V6, V8 = ph21.majority(o6)[0], ph21.majority(o8)[0]
    tt = np.arange(L6.shape[0])[:, None] + 1; M6, M8 = np.minimum(L6, tt), np.minimum(L8, tt)      # prior: a virtual valued whiff at step -1
    rules = ([(f"window N {N}", L6 <= N - 1, L8 <= N - 1) for N in (10, 20, 40, 60, 100, 200, 600)] + [(f"P_valued > {th:g}", P6 > th, P8 > th) for th in THETAS]
             + [(f"prior+window N {N}", M6 <= N - 1, M8 <= N - 1) for N in (10, 20, 40, 60, 100, 150, 200, 300, 600)])
    print("   'prior+window N': the trace starts ON (each odour in the repertoire presumed present at step 0, as if sensed at step -1) and decays with window N;"
          " the plain window and the strict threshold start OFF (nothing sensed yet)")
    for lab, pv6, pv8 in rules:
        dev6 = pv6 & (wv6 != o6["NAV"]); dev8 = ~pv8 & o8["DIFF"]
        eq6, eq8 = ~dev6.any(0), ~dev8.any(0); both = eq6 & eq8
        assert np.array_equal(V6[both], V8[both])
        known = eq6 | eq8; kv = int(V6[eq6].sum() + V8[eq8 & ~eq6].sum()); unk = int((~known).sum())
        f6 = first_true(dev6)
        if lab.startswith("prior"): kept = 1 - (o8["DIFF"] & ~pv8).sum() / o8["DIFF"].sum(); lab = f"{lab} (filter actions kept {kept:.3f})"
        print(f"   {lab:>16}: rows bitwise Agent6 throughout {int(eq6.sum())} (V {int(V6[eq6].sum())}), bitwise Agent8 throughout {int(eq8.sum())} (V {int(V8[eq8].sum())}),"
              f" both {int(both.sum())}, neither {unk}; P(V) of the scoped agent bounded in [{kv / 400:.3f}, {(kv + unk) / 400:.3f}] (maintain {V6.mean():.3f}, filter {V8.mean():.3f});"
              f" among maintain's non-V rows ({int((~V6).sum())}) those that ever leave Agent6's trajectory {int((~V6 & ~eq6).sum())}, first departure step {q(f6[~V6 & ~eq6])}")
    D = o8["DIFF"]; scan = []
    for N in range(1, 601):
        pv6, pv8 = M6 <= N - 1, M8 <= N - 1; eq6, eq8 = ~(pv6 & (wv6 != o6["NAV"])).any(0), ~(~pv8 & D).any(0)
        kv = int(V6[eq6].sum() + V8[eq8 & ~eq6].sum()); scan.append((N, 1 - (D & ~pv8).sum() / D.sum(), kv / 400, (kv + int((~(eq6 | eq8)).sum())) / 400))
    f95 = next((z for z in scan if z[1] >= 0.95), None); f88 = next((z for z in scan if z[2] >= 0.88), None); f90 = next((z for z in scan if z[2] >= 0.90), None)
    print(f"   prior+window scan N 1..600: smallest N keeping >= 0.95 of the filter's actions {f95[0] if f95 else 'none'} (kept {f95[1]:.3f}, P(V) bounds [{f95[2]:.3f}, {f95[3]:.3f}]);"
          f" smallest N with the P(V) lower bound >= 0.88: {f88[0] if f88 else 'none'} (kept {f88[1]:.3f}, bounds [{f88[2]:.3f}, {f88[3]:.3f}]);"
          f" >= 0.90: {f90[0] if f90 else 'none'} (kept {f90[1]:.3f}, bounds [{f90[2]:.3f}, {f90[3]:.3f}])")
    print("   scan excerpt (N: kept, lower, upper): " + "  ".join(f"{z[0]}: {z[1]:.3f} [{z[2]:.3f}, {z[3]:.3f}]" for z in scan if z[0] in (25, 30, 35, 40, 45, 50, 55, 60, 80, 120, 250, 400, 500)))
    w6, w8 = w1["Agent6"], w1["Agent8"]; rr = np.arange(len(w6["pres"])); wv = w6["W"][:, rr, w6["absent"]]
    print(f"   W1 (absent-check dev seeds): the absent odour is never present on Agent6's trajectory ({int(wv.sum())} whiffs), so a scoped agent that starts OFF is bitwise"
          f" Agent6 in all {wv.shape[1]} rows over 600 steps under every window and threshold (the valued-present condition never holds)")
    wb8, wb6 = w8["W"][:, rr, w8["pres"]], w6["W"][:, rr, w6["pres"]]; t = np.arange(w6["steps"])[:, None]
    for N in (10, 20, 40, 60, 100):
        d6 = (t <= N - 2) & w6["NAV"]; eq6 = ~d6.any(0)                       # prior+window: A present only on steps 0..N-2, where Agent6's surges would be withheld
        ft = first_true(wb8 & (t >= N - 1))                                    # on Agent8's trajectory (identical up to step N-2): first B whiff once the prior has lapsed
        s8 = ph22.summary(w8, upto=N - 1)
        print(f"   W1 prior+window N {N}: bitwise Agent6 throughout in {int(eq6.sum())}/400 rows (Agent6 surges before step {N - 1} in the rest); bitwise Agent8 on steps 0..{N - 2}"
              f" in every row, where Agent8 had reached the source in {int(s8['reach'].sum())} rows; first B whiff at or after step {N - 1} (tracking can start): {q(ft[ft >= 0])}"
              f" (rows {int((ft >= 0).sum())}; exact: the scoped agent is Agent8 until that whiff and surges on it); Agent6's own first-reach median {np.median(ph22.summary(w6)['first'][ph22.summary(w6)['reach']]):.0f}")
        d8 = w8["AT"][:N - 1].sum(0); d6 = np.array([w6["AT"][max(f, 0):, i].sum() if f >= 0 else 0 for i, f in enumerate(ft)]); prox = d8 + d6; full6 = w6["AT"].sum(0); dd = prox - full6
        print(f"      crude dwell proxy (NOT a simulation): Agent8's dwell on steps 0..{N - 2} + Agent6's own dwell from the first-surge step to 600: {q(prox, '.1f')} (mean {prox.mean():.2f});"
              f" minus Agent6's full dwell per row: mean {dd.mean():+.2f} sd {dd.std():.2f} (Agent6 dwell {q(full6, '.1f')}, mean {full6.mean():.2f})")



def check_offline_P(seeds, n=40, steps=200):
    """the offline recomputation equals the agent's own upstream state on a live run (Agent8, World7, task start)"""
    from ph16 import World7, cast_draw
    w = World7(n, np.random.default_rng(seeds[0]), seeds[0]); rows = np.arange(n); kv = np.zeros((n, 2)); kv[rows, w.good] = 1.0
    a = Agent8(n, np.random.default_rng(seeds[1]), G=G_STAR, known=kv, rule=True, filt=True); a.cast_sign = cast_draw(seeds[1], n)
    Ws, Ps = [], []
    for _ in range(steps):
        x = w.sense(); t, _ = a.act(w, x, w.wind_on()); w.move(t); a.bump(w.bumped); Ws.append(x); Ps.append(a.up.P.copy())
    return np.array_equal(offline_P(np.array(Ws)), np.array(Ps))


def main():
    assert sha(ph21.__file__) == PH21_SHA and sha(ph22.__file__) == PH22_SHA, "ph21.py or ph22.py is not the version that ran"
    print(f"== option-v presence diagnosis (measurement only). this file sha256 {sha()}; ph21.py {sha(ph21.__file__)} (the version H23 ran: True);"
          f" ph22.py {sha(ph22.__file__)} (the version the absent-odour check ran: True); {R} rows x {T} steps; seeds: ph21.SEEDS['dev'] (H23 development),"
          f" ph22.SEEDS['dev'] (absent-check development), stub draws ph21.BENCH / ph19.BENCH; no new rule run ==")
    part1()
    dev = ph21.SEEDS["dev"]
    print(f"\n   offline upstream recomputation equals Agent8's own P on a live run (40 rows x 200 steps, H23 dev seeds): {check_offline_P(dev)}")
    print("\n== (2) H21 task (World7, +1/0, G 2, gate on), H23 development seeds ==")
    o8 = ph21.task("filter", dev); o6 = ph21.task("maintain", dev)
    assert ph21.same(o6, ph21.task("maintain", dev, cls=Agent6))
    Vf, Vm = ph21.majority(o8)[0], ph21.majority(o6)[0]
    print(f"   dwell-majority P(V): filter {Vf.mean():.3f}, maintain {Vm.mean():.3f} (paired into V {int((Vf & ~Vm).sum())}, out of V {int((~Vf & Vm).sum())}); maintain arm == Agent6 bitwise True")
    m8 = part2(o8, "filter (Agent8)"); part2(o6, "maintain (Agent6)")
    print("\n== (3) W1, absent-odour world (only B present, read-out +1 / 0), absent-check development seeds ==")
    w1 = {arm: ph22.run("W1", arm, ph22.SEEDS["dev"]) for arm in ("Agent8", "Agent6")}
    for arm, o in w1.items():
        s = ph22.summary(o); rr = s["reach"]; rows = np.arange(len(o["pres"]))
        PA = offline_P(o["W"])[:, rows, o["absent"]]
        print(f"   [{arm}] reach {int(rr.sum())}/{len(rr)} = {rr.mean():.3f}; first reach {q(s['first'][rr])}; dwell {q(s['dwell'], '.1f')} (mean {s['dwell'].mean():.2f});"
              f" lost rows {int(s['lost'].sum())}; nav (row, step) {int(s['nav'].sum())}; absent odour A: whiffs {int(o['W'][:, rows, o['absent']].sum())}, upstream P_A max {PA.max()!r}")
    print("   reading (code, not a run): A is never sensed, so P_A is exactly 0 and a window trace of A stays 0 on every step: under a presence rule that starts OFF A is never"
          " present, v_max is taken over B alone, and the scoped agent in W1 is Agent6's navigation from step 0 (0 steps of ignoring B, not N)."
          " The N-step cost arises only after A HAS been sensed and then is lost (not in W1), or with a trace that starts ON (section 5).")
    part4(o8, m8, o6)
    part5(o8, o6, w1)


if __name__ == "__main__":
    main()
