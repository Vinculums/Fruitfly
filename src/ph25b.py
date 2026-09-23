#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H24 Run 2, N sweep (measurement only; decision:h24-run2-n-sweep): Agent11 with the presence window N in {60, 90, 120, 150, 200,
300, 450, inf} on ph25's bench seeds. inf = Agent10 (scope off). No rule, bar or seed change; no task seed touched.
ph25 is imported unchanged; the only addition is a run-time wrapper on ph24.make that sets Agent11's N (Agent9 reads self.N only in act).

Usage: python ph25b.py   (from src/; output LF; redirect to experiments/h24/ph25b_nsweep.txt)
Seed digits are not printed (the output would otherwise trip ph25.seeds_unused, which does not exclude this file's output by name).
"""
import sys, math
import numpy as np
import ph24, ph25
from ph25 import Agent11, Agent10, Agent6, BS, BENCH, run, majority, cls3, interval, pass_prob, binom_ge, lost_t1, w1sum, t3_dwell, ratio_boot, \
    pass_prob_R, t3a_steps, construct_ok, first_true, q3, qq, bitwise, eqmask, sha
from ph23 import first_surge_ok, wn

NS = [60, 90, 120, 150, 200, 300, 450, math.inf]
_N = [60]
_make = ph24.make                                             # ph25's hook


def make(cls, *a, **kw):
    x = _make(cls, *a, **kw)
    if cls is Agent11: x.N = _N[0]
    return x


ph24.make = make


def arm(world, N, **kw):
    if N == math.inf: return run(world, Agent10, (1.0, 0.0), BS, **kw)
    _N[0] = N
    try: return run(world, Agent11, (1.0, 0.0), BS, **kw)
    finally: _N[0] = 60


def seduced(o):
    """T1 rows where a valued hold was ended by a timeout drive and afterwards, before the valued hold re-formed, the valued presence
    flag went False (c >= N, not held) - the valued source is in the world throughout in World7. Returns rows, expiry step, re-acquisition."""
    g = o["good"]; n = len(g); H, P = o["H"], o["PRES"]; st = H.shape[0]; dr = ph24.events(o)["drives"]
    te = np.full(n, -1); rel = np.zeros(n, bool)
    for r, hp, ended, e in zip(dr["r"], dr["hp"], dr["ended"], dr["end"]):
        if hp != g[r] or not ended or te[r] >= 0: continue
        rel[r] = True; ref = np.flatnonzero(H[e + 1:, r] == g[r]); stop = e + 1 + (ref[0] if len(ref) else st - e - 1)
        x = np.flatnonzero(~P[e + 1:stop, r])
        if len(x): te[r] = e + 1 + x[0]
    s = te >= 0; rows = np.arange(n)
    after = lambda m: np.array([bool(m[te[r]:, r].any()) if s[r] else False for r in rows])
    return dict(rel=rel, s=s, te=te, rehold=after(H == g[None, :]), reach=after(o["AT2"][:, rows, g]), whiff=after(o["W"][:, rows, g]))


def diff8(o):
    g = o["good"]; rows = np.arange(len(g)); fd = first_true(o["DIFF8"]); tt = np.arange(o["H"].shape[0])[:, None]; late = tt > fd[None, :]
    return fd, ((o["H"] == g[None, :]) & late).any(0) & (fd >= 0), (o["AT2"][:, rows, g] & late).any(0) & (fd >= 0)


def fmt(N): return "inf" if N == math.inf else str(N)


def main():
    n = BENCH["rows"]
    print(f"== H24 Run 2 N sweep (ph25b.py, measurement only; decision:h24-run2-n-sweep). ph25's bench seeds and bootstrap seed (digits not printed); {n} rows x {BENCH['steps']} steps;"
          f" N {[fmt(N) for N in NS]} (inf = Agent10, scope off) ==")
    print(f"   ph25b.py sha256 {sha(__file__)}; ph25.py sha256 {sha(ph25.__file__)}; design {ph25.DESIGN}")
    # references
    o10, w10, w6 = run("T1", Agent10, (1.0, 0.0), BS), run("W1", Agent10, (1.0, 0.0), BS), run("W1", Agent6, (1.0, 0.0), BS)
    f10, fc = run("T3a", Agent10, (1.0, 0.0), BS), run("T3a", None, (1.0, 0.0), BS, fixed="neutral")
    V10 = majority(o10)[0]; c10 = cls3(o10); d10, d6 = t3_dwell(w10, 0, 600), t3_dwell(w6, 0, 600); D6 = float(d6.mean()); bar_t2 = round(-0.20*D6, 1)
    Dfl, Dc = t3_dwell(f10, 100, 600), t3_dwell(fc, 100, 600); _, spn, _, _ = interval("DP", Dc, Dfl); sdr = float(np.std(Dc - Dfl))
    target_w = 0.8*D6
    print(f"   references: T1 Agent10 V {int(V10.sum())} N {int(majority(o10)[1].sum())} tie {int(majority(o10)[2].sum())}; W1 dwell Agent6 {D6:.4f}, Agent10 {d10.mean():.3f};"
          f" bar_T2 by the design's rule {bar_t2:+.1f}; T3a floor Agent10 {Dfl.mean():.3f}, ceiling {Dc.mean():.3f}, span {spn:.3f}, per-row paired sd {sdr:.3f}")
    print(f"   targets (registered, owner's instruction): T1 DP lower bound >= -0.05 AND W1 dwell >= 0.8 x Agent6 = {target_w:.3f} with M5(b) pass probability (bar {bar_t2:+.1f}) >= 0.5")
    tab = []
    for N in NS:
        print(f"\n== N {fmt(N)} ==")
        o = arm("T1", N); V = majority(o)[0]; c = cls3(o); Vn, Nn, Zn = (int(m.sum()) for m in majority(o))
        _, dp, lo, hi = interval("DP", V.astype(float), V10.astype(float)); ppb, _, sdb = pass_prob(V.astype(float) - V10.astype(float), -0.05); ppa = binom_ge(V.mean())
        into, out = int(((c == 0) & (c10 != 0)).sum()), int(((c != 0) & (c10 == 0)).sum()); e10 = eqmask(o, o10).all(0)
        if N == 60:
            assert (Vn, Nn, Zn) == (314, 81, 5) and (round(dp, 4), round(lo, 4), round(hi, 4)) == (-0.1725, -0.2125, -0.135), "N 60 T1 does not reproduce the bench"
            print("   reproduction: T1 V/N/tie 314/81/5 and DP -0.1725 [-0.2125, -0.1350] as recorded (asserted)")
        if N == math.inf: print(f"   identity: this arm is Agent10 itself (the reference); Agent11 with N = inf == Agent10 bitwise (T1): "
                                f"{bitwise(ph25_inf(), o10)}")
        k, pv, plo, phi = interval("P", V)
        print(f"   T1: V {Vn} N {Nn} tie {Zn}; P(V) {pv:.3f} [{plo:.3f}, {phi:.3f}]; paired DP vs Agent10 {dp:+.4f} [{lo:+.4f}, {hi:+.4f}]; into V {into}, out of V {out};"
              f" lost rows {int(lost_t1(o).sum())} (Agent10 {int(lost_t1(o10).sum())}); rows bitwise Agent10 throughout {int(e10.sum())}")
        print(f"      pass probabilities (design section 7 arithmetic): M2(a) P(k >= 365 of 400) at P(V) {V.mean():.3f}: {ppa:.4f}; M2(b) at DP {dp:+.4f}, paired sd {sdb:.4f}: {ppb:.4f}")
        if N != math.inf:
            sd_ = seduced(o); fd, rh, ra = diff8(o); s = sd_["s"]
            print(f"      seduced path: rows with a valued hold ended by a timeout drive {int(sd_['rel'].sum())}; of those, valued presence expired (c >= {N}) before the valued hold re-formed"
                  f" {int(s.sum())} = {s.mean():.3f} of {n} rows; expiry step {q3(sd_['te'][s])}; after expiry: valued whiff again {int(sd_['whiff'].sum())}, valued re-held {int(sd_['rehold'].sum())},"
                  f" within 3.0 of the valued source again {int(sd_['reach'].sum())}; class at 600 among them V {int((c[s] == 0).sum())} N {int((c[s] == 1).sum())} tie {int((c[s] == 2).sum())}"
                  f" (Agent10 on the same rows V {int((c10[s] == 0).sum())})")
            print(f"      first `differs8`: rows {int((fd >= 0).sum())}, step {q3(fd[fd >= 0])}; after it, valued re-held {int(rh.sum())}, within 3.0 of the valued source {int(ra.sum())};"
                  f" out-of-V rows among `differs8` rows {int(((c != 0) & (c10 == 0) & (fd >= 0)).sum())}")
        # W1
        w = arm("W1", N); d = t3_dwell(w, 0, 600); ppw, mw, sdw = pass_prob(d - d6, bar_t2); _, _, wlo, whi = interval("DP", d, d6); sm = w1sum(w); f1 = first_true(w["NAV"])
        if N == 60:
            assert round(float(d.mean()), 3) == 22.733, "N 60 W1 does not reproduce the bench"; print("   reproduction: W1 dwell 22.733 as recorded (asserted)")
        fs_line = ""
        if N != math.inf: ok, _, _ = first_surge_ok(w, N - 1); fs_line = f"; first surge == first B whiff at or after step {N - 1} in {int(ok.sum())}/{n}"
        print(f"   W1: dwell {d.mean():.3f} (quartiles {ph24.q3f(d)}) vs Agent6 {D6:.3f}, Agent10 {d10.mean():.3f}; paired vs Agent6 {mw:+.4f} sd {sdw:.4f} [{wlo:+.4f}, {whi:+.4f}];"
              f" M5(b) pass probability at bar {bar_t2:+.1f}: {ppw:.4f}; reach {int(sm['reach'].sum())}/{n}; lost rows {int(sm['lost'].sum())}; first surge step {qq(f1)}{fs_line}")
        # T3a
        f = arm("T3a", N); D = t3_dwell(f, 100, 600); Rb, Rlo, Rhi = ratio_boot(D, Dfl, Dc); st = t3a_steps(f)
        if N == 60:
            assert round(float(D.mean()), 3) == 14.490 and round(Rb, 3) == 1.005, "N 60 T3a does not reproduce the bench"; print("   reproduction: T3a dwell 14.490, R 1.005 as recorded (asserted)")
        fs_line = ""
        if N != math.inf: ok, _, _ = first_surge_ok(f, N - 1); fs_line = f"; first surge == first neutral whiff at or after step {N - 1} in {int(ok.sum())}/{n}"
        print(f"   T3a: construction {construct_ok(f)}; neutral dwell 100-599 {D.mean():.3f} (floor {Dfl.mean():.3f}, ceiling {Dc.mean():.3f}); R {Rb:.4f} [{Rlo:.4f}, {Rhi:.4f}];"
              f" M7(b) pass probability {pass_prob_R(Rb, sdr, spn):.4f}; valued hold end step {qq(st['end'])}; first neutral surge {qq(st['surge'])}{fs_line}")
        tab.append((N, dp, lo, hi, ppb, ppa, float(d.mean()), ppw, Rb, Rlo, float(sd_["s"].mean()) if N != math.inf else 0.0))
    print("\n== table: N -> T1 DP [interval], M2(b) pass prob, M2(a) pass prob; W1 dwell, M5(b) pass prob; T3a R [lower]; seduced fraction ==")
    for N, dp, lo, hi, ppb, ppa, dw, ppw, Rb, Rlo, sf in tab:
        print(f"   N {fmt(N):>4}: T1 DP {dp:+.4f} [{lo:+.4f}, {hi:+.4f}] M2(b) {ppb:.4f} M2(a) {ppa:.4f} | W1 dwell {dw:6.3f} M5(b) {ppw:.4f} | T3a R {Rb:.4f} [{Rlo:.4f}] | seduced {sf:.3f}")
    ok = [N for N, dp, lo, hi, ppb, ppa, dw, ppw, *_ in tab if lo >= -0.05 and dw >= target_w and ppw >= 0.5]
    print(f"\n== smallest N meeting BOTH targets (T1 DP lower bound >= -0.05; W1 dwell >= {target_w:.3f} with M5(b) pass probability >= 0.5): "
          f"{fmt(ok[0]) if ok else 'NONE of the swept N'}; all meeting: {[fmt(N) for N in ok]} ==")


def ph25_inf():
    _N[0] = math.inf
    try: return run("T1", Agent11, (1.0, 0.0), BS)
    finally: _N[0] = 60


if __name__ == "__main__":
    main()
