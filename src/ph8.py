#!/usr/bin/env python3
"""Phase 7.2: H11 -- extinction as a parallel opposing trace, gated by outcome omission.

Usage: python3 ph8.py [--quick] [demo|all]

H8 v2 extinguishes by depressing the SAME compartments that acquisition wrote, back toward
balance. Phase 5 Run 2 measured what that costs: under sustained pairing the valence peaks at
+-0.935 at t=10 and is ground to +-0.003 by t=400, so a memory survives only for a stimulus
the agent leaves. Phase 6.1 named the fly's alternative: traces of the original memory and of
the extinction memory co-exist, written in parallel at different sites, with extinction driven
by reward-coding dopaminergic neurons downstream of the avoidance-directing MBONs
(Felsenberg et al 2018, Cell).

The redesign has TWO separable ingredients, and the point of this file is to test them apart:

  parallel  the extinction signal writes to compartments 2 and 3, which acquisition never
            touches, instead of writing back onto 0 and 1.
  gated     the extinction signal fires only when no external reinforcement is arriving,
            because extinction is driven by the OMISSION of an expected outcome rather than
            by the expectation itself.

Predicted before running, per criteria F4: `gated` is what removes the sustained-exposure
erasure (F2), and `parallel` is what leaves the original association readable after behaviour
has extinguished (F3). The two-by-two is reported in full so the prediction can be wrong.

ph4.py is not edited. MB4 subclasses it, and MB4(parallel=False, gated=False) is asserted in
demo() to reproduce H8 v2 exactly, so the baseline cell of the two-by-two IS the adopted rule.
"""
import sys
import numpy as np
from ph4 import MB, pairing, reinf_vec

R = 200
QUICK = "--quick" in sys.argv
if QUICK: R = 40

KW = dict(K=500, C=4, sparsity=0.05, eta_d=0.10, eta_p=0.30, beta=0.15)   # C=4, else Phase 4's


class MB4(MB):
    """Four compartments. 0 and 1 are the acquisition pair, 2 and 3 the extinction pair.

    behavioural valence = (out0 - out1) + (out2 - out3)
    acquisition valence = (out0 - out1)          <- what F3 reads

    Compartment 0's reinforcement unit signals punishment, so pairing odour with punishment
    depresses w[0], out0 falls and the valence falls. Depressing compartment 3 raises the
    valence back, which is how an opposing trace cancels an aversive memory behaviourally
    without touching the memory itself.

    The extinction drive reads the BEHAVIOURAL valence, not the acquisition site's. That makes
    it self-limiting: once the opposing trace has cancelled the original, the drive is zero and
    extinction stops rather than overshooting into the opposite sign.
    """

    def __init__(self, runs, parallel=True, gated=True, **kw):
        super().__init__(runs, **kw)
        self.parallel, self.gated = parallel, gated

    def _out(self, code):
        return self.out(code)

    def valence(self, code):
        o = self.out(code)
        return (o[:, 0] - o[:, 1]) + (o[:, 2] - o[:, 3])

    def acq_valence(self, code):
        o = self.out(code)
        return o[:, 0] - o[:, 1]

    def step(self, code=None, reinf=None):
        code = np.zeros((self.R, self.K)) if code is None else code
        reinf = np.zeros((self.R, self.C)) if reinf is None else reinf
        if self.beta and code.any():
            o = self.out(code)
            drive = (o[:, 0] - o[:, 1]) + (o[:, 2] - o[:, 3])
            gate = 1.0
            if self.gated:
                # extinction is driven by the omission of the outcome, so it is silent while
                # an external reinforcement is actually arriving.
                gate = (reinf.sum(1, keepdims=True) <= 0.0).astype(float)
            pos = np.maximum(drive, 0.0)[:, None]      # appetitive -> oppose by depressing +
            neg = np.maximum(-drive, 0.0)[:, None]     # aversive   -> oppose by depressing -
            fb = np.zeros_like(reinf)
            if self.parallel:
                fb[:, 2:3] = pos
                fb[:, 3:4] = neg
            else:
                fb[:, 0:1] = pos                        # H8 v2: straight back onto the original
                fb[:, 1:2] = neg
            reinf = reinf + self.beta*fb*gate
        tc_now = np.minimum(self.tc + code, 1.0)
        tr_past = self.tr*(reinf <= 0.0)
        dw = (-self.eta_d*np.einsum('rc,rk->rck', reinf, tc_now)
              + self.eta_p*np.einsum('rc,rk->rck', tr_past, code))
        self.w = np.clip(self.w + dw, self.wmin, self.wmax)
        self.tc += (1.0/self.tau_code)*(-self.tc) + code
        self.tr += (1.0/self.tau_reinf)*(-self.tr) + reinf
        self.tc = np.minimum(self.tc, 1.0); self.tr = np.minimum(self.tr, 1.0)


def mk(parallel, gated, seed=0, **kw):
    return MB4(R, parallel=parallel, gated=gated, rng=np.random.default_rng(seed), **{**KW, **kw})


def trained(m, code, comp=0, n=10, order="forward"):
    for _ in range(n): pairing(m, code, comp, order)
    return m


# ---------------------------------------------------------------- F1, Phase 4's own battery
def f1_battery(make):
    m = make(); A = m.odour(11); B = m.odour(12)
    v0 = m.valence(A).copy(); b0 = m.valence(B).copy()
    for _ in range(5): pairing(m, A, 0, "forward")
    sign5 = int(((m.valence(A) - v0) < 0).sum())
    for _ in range(5): pairing(m, A, 0, "forward")
    dA = float(np.median(m.valence(A) - v0)); dB = float(np.median(m.valence(B) - b0))
    leak = abs(dB/dA)*100 if dA else float("inf")

    me = make(); Ae = me.odour(11); e0 = me.valence(Ae).copy()
    trained(me, Ae)
    vt = float(np.median(me.valence(Ae) - e0))
    for _ in range(20): pairing(me, Ae, None, "forward")
    ve = float(np.median(me.valence(Ae) - e0))
    ext = abs(ve/vt)*100 if vt else float("inf")

    mr = make(); Ar = mr.odour(11); r0 = mr.valence(Ar).copy()
    trained(mr, Ar)
    flip = np.zeros(R, bool)
    for _ in range(10):
        pairing(mr, Ar, 1, "forward")
        flip |= (mr.valence(Ar) - r0) > 0

    f = make(); Af = f.odour(11); f0 = f.valence(Af).copy(); trained(f, Af, order="forward")
    df = f.valence(Af) - f0
    g = make(); Ag = g.odour(11); g0 = g.valence(Ag).copy(); trained(g, Ag, order="reverse")
    dg = g.valence(Ag) - g0
    timing = int(((df < 0) & (dg > 0)).sum())
    return dict(acq=sign5, dA=dA, leak=leak, ext=ext, rev=int(flip.sum()), timing=timing)


# ---------------------------------------------------------------- F2, sustained exposure
def f2_sustained(make, comp=0, steps=400):
    """the Phase 5 Run 2 probe: code and reinforcement together on every step."""
    m = make(); code = m.odour(101)
    rv = np.zeros((R, m.C)); rv[:, comp] = 1.0
    traj, peak = [], 0.0
    for t in range(1, steps + 1):
        m.step(code=code, reinf=rv)
        v = float(np.median(m.valence(code)))
        peak = max(peak, abs(v))
        if t in (5, 10, 25, 50, 100, 200, 400): traj.append((t, v))
    final = abs(traj[-1][1])
    return peak, final, (final/peak*100 if peak else 0.0), traj


# ---------------------------------------------------------------- F3, does the trace survive
def f3_trace(make):
    m = make(); A = m.odour(11)
    v0 = m.valence(A).copy(); a0 = m.acq_valence(A).copy()
    trained(m, A)
    vt = float(np.median(m.valence(A) - v0))
    at = float(np.median(m.acq_valence(A) - a0))
    for _ in range(20): pairing(m, A, None, "forward")
    ve = float(np.median(m.valence(A) - v0))
    ae = float(np.median(m.acq_valence(A) - a0))
    behav_gone = abs(ve) <= 0.30*abs(vt) if vt else False
    trace_kept = abs(ae) >= 0.50*abs(at) if at else False
    return dict(vt=vt, ve=ve, at=at, ae=ae, behav_gone=behav_gone, trace_kept=trace_kept,
                kept_pct=(abs(ae)/abs(at)*100 if at else 0.0))


# ---------------------------------------------------------------- the two-by-two
def cell(parallel, gated, label):
    make = lambda: mk(parallel, gated)
    b = f1_battery(make)
    peak, final, ret, traj = f2_sustained(make)
    t3 = f3_trace(make)
    n = 0.95*R
    f1_ok = (b["acq"] >= n and b["leak"] <= 10 and b["ext"] <= 30
             and b["rev"] >= n and b["timing"] >= n)
    f2_ok = ret >= 70.0
    f3_ok = t3["behav_gone"] and t3["trace_kept"]
    print(f"\n   {label}")
    print(f"     F1 acq {b['acq']}/{R} (dA {b['dA']:+.3f})  leak {b['leak']:.1f}%  "
          f"ext {b['ext']:.0f}%  rev {b['rev']}/{R}  timing {b['timing']}/{R}"
          f"   -> {'pass' if f1_ok else 'FAIL'}")
    print(f"     F2 sustained: peak {peak:.3f} -> t400 {final:.3f}, retains {ret:.1f}%"
          f"   (bound 70%)   -> {'pass' if f2_ok else 'FAIL'}")
    print(f"        " + "  ".join(f"t={t}:{v:+.3f}" for t, v in traj))
    print(f"     F3 trace: behavioural {t3['vt']:+.3f} -> {t3['ve']:+.3f}"
          f" ({'extinguished' if t3['behav_gone'] else 'NOT extinguished'});"
          f" acquisition site {t3['at']:+.3f} -> {t3['ae']:+.3f}"
          f" ({t3['kept_pct']:.0f}% kept)   -> {'pass' if f3_ok else 'FAIL'}")
    return dict(label=label, f1=f1_ok, f2=f2_ok, f3=f3_ok, ret=ret, kept=t3["kept_pct"])


# ------------------------------------------------- F6, reported not gated, ADDED AFTER THE RUN
def f6_savings(make):
    """Is the surviving trace functional, or merely present in the weights?

    Added after the two-by-two, and disclosed as added. F3 reads the acquisition weights, which
    for the parallel design is close to true by construction: extinction writes elsewhere, so
    of course compartment 0 is untouched. The behavioural question is whether that preserved
    trace does any work. Reacquisition savings is the standard probe: after extinction, ONE
    re-pairing should restore an aversive valence that a naive animal would need many pairings
    to reach. This is also a real fly phenomenon, so it is a prediction and not just a check.
    """
    m = make(); A = m.odour(11); v0 = m.valence(A).copy()
    trained(m, A)
    vt = float(np.median(m.valence(A) - v0))
    for _ in range(20): pairing(m, A, None, "forward")
    ve = float(np.median(m.valence(A) - v0))
    pairing(m, A, 0, "forward")                       # ONE re-pairing
    vr = float(np.median(m.valence(A) - v0))

    naive = make(); B = naive.odour(11); n0 = naive.valence(B).copy()
    pairing(naive, B, 0, "forward")                   # ONE pairing, from scratch
    vn = float(np.median(naive.valence(B) - n0))
    recov = abs(vr - ve)
    return dict(vt=vt, ve=ve, vr=vr, vn=vn, recov=recov,
                savings=(recov/abs(vn) if vn else float("inf")),
                frac_of_trained=(abs(vr)/abs(vt)*100 if vt else 0.0))


def savings_run():
    print("\n== F6 reacquisition savings (reported, not gated; ADDED after the two-by-two) ==")
    print("   After extinction, ONE re-pairing. A preserved trace should snap back; a trace")
    print("   that was erased has to be relearned from scratch like a naive animal.")
    print(f"   {'cell':34s} {'trained':>8} {'extinct':>8} {'+1 pair':>8} {'naive+1':>8}"
          f" {'savings':>8} {'% of trained':>13}")
    for par, gat, lab in ((False, False, "H8 v2 baseline"), (False, True, "gated only"),
                          (True, False, "parallel only"), (True, True, "H11 full")):
        s = f6_savings(lambda p=par, g=gat: mk(p, g))
        print(f"   {lab:34s} {s['vt']:+8.3f} {s['ve']:+8.3f} {s['vr']:+8.3f} {s['vn']:+8.3f}"
              f" {s['savings']:7.1f}x {s['frac_of_trained']:12.0f}%")


def demo():
    """self-check: MB4(parallel=False, gated=False) must BE H8 v2, and the gate must fire."""
    kw2 = dict(K=200, C=2, sparsity=0.05, eta_d=0.10, eta_p=0.30, beta=0.15)
    a = MB(30, rng=np.random.default_rng(0), **kw2)
    b = MB4(30, parallel=False, gated=False, rng=np.random.default_rng(0),
            **{**kw2, "C": 4})
    code = a.odour(11)
    for _ in range(6): pairing(a, code, 0, "forward")
    for _ in range(6): pairing(b, code, 0, "forward")
    va, vb = np.median(a.valence(code)), np.median(b.valence(code))
    assert abs(va - vb) < 1e-9, f"MB4(False,False) is not H8 v2: {va} vs {vb}"
    assert np.allclose(a.w[:, :2], b.w[:, :2]), "acquisition weights diverged"
    assert np.allclose(b.w[:, 2:], 1.0), "extinction compartments moved when parallel=False"

    # the gate: with external reinforcement present, a gated rule must not write extinction
    g = MB4(30, parallel=True, gated=True, rng=np.random.default_rng(0), **{**kw2, "C": 4})
    u = MB4(30, parallel=True, gated=False, rng=np.random.default_rng(0), **{**kw2, "C": 4})
    c2 = g.odour(11)
    rv = np.zeros((30, 4)); rv[:, 0] = 1.0
    for _ in range(50):
        g.step(code=c2, reinf=rv.copy()); u.step(code=c2, reinf=rv.copy())
    assert np.allclose(g.w[:, 2:], 1.0), "gated rule wrote extinction while reinforced"
    assert not np.allclose(u.w[:, 2:], 1.0), "ungated rule failed to write extinction"
    print(f"ok  MB4(parallel=False, gated=False) reproduces H8 v2 exactly ({va:+.6f})")
    print("ok  the gate silences extinction while external reinforcement is arriving")
    print("ok  without the gate, extinction writes during reinforcement (the H8 v2 failure mode)")


if __name__ == "__main__":
    if "demo" in sys.argv[1:]:
        demo(); sys.exit(0)
    print(f"== Phase 7.2, H11. {R} runs per cell, K={KW['K']} ==")
    print("== Criteria: record:phase7-2-success-criteria, stored before this file existed ==")
    print("== Prediction on record: `gated` gives F2, `parallel` gives F3 ==")
    rows = [cell(False, False, "H8 v2 baseline      (parallel=no,  gated=no )"),
            cell(False, True,  "gated only          (parallel=no,  gated=yes)"),
            cell(True,  False, "parallel only       (parallel=yes, gated=no )"),
            cell(True,  True,  "H11 full            (parallel=yes, gated=yes)")]
    print("\n== Two-by-two summary ==")
    print(f"   {'cell':38s} {'F1':>5} {'F2':>5} {'F3':>5}   F2 retains   F3 keeps")
    for r in rows:
        print(f"   {r['label']:38s} {'pass' if r['f1'] else 'FAIL':>5}"
              f" {'pass' if r['f2'] else 'FAIL':>5} {'pass' if r['f3'] else 'FAIL':>5}"
              f"   {r['ret']:8.1f}%   {r['kept']:7.0f}%")
    full = rows[-1]
    print(f"\n   H11 {'SUPPORTED' if (full['f1'] and full['f2'] and full['f3']) else 'not supported'}"
          f" on all three criteria.")
    savings_run()
