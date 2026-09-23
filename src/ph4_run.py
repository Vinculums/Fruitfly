#!/usr/bin/env python3
"""Phase 4 run: H8 v2, compartment-local timing-signed plasticity. Usage: python3 ph4_run.py"""
import numpy as np
from ph4 import MB, pairing

R = 200
KW = dict(K=500, C=2, sparsity=0.05, eta_d=0.10, eta_p=0.30, beta=0.15)   # adopted
def mb(seed=0, **kw): return MB(R, rng=np.random.default_rng(seed), **{**KW, **kw})

def trained(m, code, comp=0, n=10, order="forward"):
    for _ in range(n): pairing(m, code, comp, order)
    return m

def l1_l2():
    m = mb(); A = m.odour(11); B = m.odour(12)
    v0 = m.valence(A).copy(); b0 = m.valence(B).copy()
    print(f"L2 code overlap between A and B: {(A*B).sum(1).mean():.2f} of {int(A.sum(1)[0])} active units")
    print("L1 acquisition, median change in learned valence of A:")
    sign5 = None
    for i in range(1, 11):
        pairing(m, A, 0, "forward")
        d = m.valence(A) - v0
        if i == 5: sign5 = int((d < 0).sum())
        if i in (1, 2, 3, 5, 10): print(f"    after {i:2d} pairings: {np.median(d):+.3f}")
    asym = float(np.median(m.valence(A) - v0))
    print(f"    correct sign at 5 pairings: {sign5}/{R}")
    spec = float(np.median(m.valence(B) - b0))
    print(f"L2 specificity: unpaired B moved {spec:+.4f}, which is {abs(spec/asym)*100:.1f}% of A's change")
    return asym

def l3():
    m = mb(); A = m.odour(11); v0 = m.valence(A).copy()
    trained(m, A); vt = (m.valence(A) - v0).copy()
    for _ in range(20): pairing(m, A, None, "forward")      # odour with no reinforcement
    ve = m.valence(A) - v0
    ok = int((np.abs(ve) <= 0.3*np.abs(vt)).sum())
    print(f"L3 extinction: trained {np.median(vt):+.3f} -> after 20 unreinforced {np.median(ve):+.3f}"
          f"  ({abs(np.median(ve)/np.median(vt))*100:.0f}% of trained), within bound in {ok}/{R}")

def l4():
    m = mb(); A = m.odour(11); v0 = m.valence(A).copy()
    trained(m, A)
    print(f"L4 reversal: after punishment training {np.median(m.valence(A)-v0):+.3f}")
    flip = np.zeros(R, bool); first = None
    for i in range(1, 11):
        pairing(m, A, 1, "forward")                          # now paired with reward
        d = m.valence(A) - v0
        flip |= d > 0
        if first is None and flip.all(): first = i
        if i in (1, 3, 5, 10): print(f"    after {i:2d} reward pairings: {np.median(d):+.3f}")
    print(f"    sign flipped within 10 pairings in {int(flip.sum())}/{R}"
          f"{'' if first is None else f', all runs by pairing {first}'}")

def l5():
    f = mb(); Af = f.odour(11); f0 = f.valence(Af).copy(); trained(f, Af, order="forward")
    df = f.valence(Af) - f0
    g = mb(); Ag = g.odour(11); g0 = g.valence(Ag).copy(); trained(g, Ag, order="reverse")
    dg = g.valence(Ag) - g0
    print(f"L5 timing: same reinforcement, forward pairing {np.median(df):+.3f},"
          f" reverse pairing {np.median(dg):+.3f}, opposite sign in {int(((df<0)&(dg>0)).sum())}/{R}")

def l6():
    # sense 1, the rule: does a compartment's weights change only when its own reinforcement
    # unit is active? Tested with the internal feedback switched off.
    m0 = MB(R, rng=np.random.default_rng(0), **{**KW, "beta": 0.0})
    A0 = m0.odour(11); w0 = m0.w[:, 1].copy(); trained(m0, A0)
    exact = bool(np.array_equal(m0.w[:, 1], w0))
    # sense 2, the training event: with the feedback on, does training one compartment leave the
    # other untouched?
    m = mb(); A = m.odour(11); w_other = m.w[:, 1].copy(); trained(m, A)
    same = bool(np.array_equal(m.w[:, 1], w_other))
    print(f"L6 locality of the rule (feedback off): compartment 1 unchanged, exactly: {exact}"
          f"  (max abs difference {np.abs(m0.w[:,1]-w0).max():.1e})")
    print(f"L6 locality of the training event (feedback on, adopted design): unchanged: {same}"
          f"  (max abs difference {np.abs(m.w[:,1]-w_other).max():.2f})")
    print("    The rule is compartment-local. The extinction feedback is itself a reinforcement")
    print("    signal into the other compartment, so the training event is not.")

def sparsity_sweep():
    print("\n== Reported, not gated: sparsity and specificity ==")
    for sp in (0.02, 0.05, 0.10, 0.25, 0.50):
        m = mb(sparsity=sp); A = m.odour(11); B = m.odour(12)
        v0 = m.valence(A).copy(); b0 = m.valence(B).copy()
        trained(m, A)
        dA = float(np.median(m.valence(A) - v0)); dB = float(np.median(m.valence(B) - b0))
        ov = float((A*B).sum(1).mean()); nact = int(A.sum(1)[0])
        print(f"   active {sp*100:5.1f}% ({nact:3d} units), overlap {ov:6.2f}:"
              f" A {dA:+.3f}, B {dB:+.3f}, leakage {abs(dB/dA)*100:5.1f}%")

def rejected():
    print("\n== Rejected design R1: no output-to-reinforcement feedback (beta 0) ==")
    m = MB(R, rng=np.random.default_rng(0), **{**KW, "beta": 0.0}); A = m.odour(11)
    v0 = m.valence(A).copy(); trained(m, A); vt = (m.valence(A) - v0).copy()
    for _ in range(20): pairing(m, A, None, "forward")
    ve = m.valence(A) - v0
    print(f"   trained {np.median(vt):+.3f} -> after 20 unreinforced {np.median(ve):+.3f}"
          f" ({abs(np.median(ve)/np.median(vt))*100:.0f}% of trained). No extinction: an unreinforced"
          f" odour drives nothing, so nothing changes.")
    print("\n== Rejected design R2: plasticity sign set by overlap, not by order ==")
    print("   In the first rule the potentiation term read the reinforcement trace whether or not")
    print("   reinforcement was still on. With feedback added, reinforcement became co-active with")
    print("   the odour, potentiation dominated, and punishment training drove the valence to the")
    print("   wrong saturation: measured -2.000 where -1.000 is full depression.")

if __name__ == "__main__":
    print("== Adopted design: K 500, 5% sparse, eta_d 0.10, eta_p 0.30, feedback beta 0.15 ==")
    l1_l2(); l3(); l4(); l5(); l6(); sparsity_sweep(); rejected()
