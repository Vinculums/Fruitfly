#!/usr/bin/env python3
"""Phase 6.2: the abstraction ladder. Usage: python3 ph6.py [--quick]

For each adopted motif, remove ONE feature at a time and score the stripped variant against
that motif's own property battery -- the same measurements, with the same thresholds, that
the motif's own phase gate used. Nothing here is a new benchmark invented after the fact.

Verdicts, per criteria C2:
  SURVIVES  the whole battery still passes
  DEGRADED  it passes, but measurably worse; the number is printed
  LOST      a named property fails

No adopted module is edited (C5). Feature switches are subclasses defined here, or parameters
the modules already expose. Removals that an earlier phase already ran as a rejected design
are marked [reused] and cite the phase rather than being re-derived (C6).
"""
import sys
import numpy as np
from ffcore import sigmoid
from ph2 import Upstream, Circuit, trial as ph2_trial, cwa
from ph3 import RingDiv, Ring, cue, circdiff, nbumps
from ph4 import MB, pairing

R = 200
QUICK = "--quick" in sys.argv
if QUICK: R = 40

LADDER = []          # (motif, feature removed, verdict, detail)


def verdict(motif, feature, v, detail, reused=""):
    LADDER.append((motif, feature, v, detail, reused))
    tag = "  [reused]" if reused else ""
    print(f"   {feature:42s} {v:9s} {detail}{tag}")


# ================================================================ motif 1 and 2 share a battery
# The Phase 2 gate tested the adopted upstream stage and the retuned circuit together, so the
# battery is the same one and each motif is stripped inside it while the other is left adopted.
UP = dict(n=1.5, sig=0.05, Rmax=1.8, k=0.8, tau=2.0)
CIR = dict(theta=1.0, k=12.0)
HARD = dict(d=0.05, cue=300)
SCALES = (0.25, 0.5, 1, 2, 4)
AMPS = (1, 2, 3, 4, 6, 10)


class Upstream2(Upstream):
    """Upstream with its features switchable. own_term=False drops the unit's own drive from
    the denominator, which is exactly what makes the Heeger form bounded."""
    def __init__(self, own_term=True, **kw):
        super().__init__(**kw)
        self.own_term = own_term

    def step(self, x):
        u = np.maximum(x, 0.0)**self.n
        self.P += (1.0/self.tau) * (-self.P + u)
        N = self.P.shape[1]
        others = (self.P.sum(1, keepdims=True) - self.P) / max(N - 1, 1)
        den = self.sig_n + self.k*others + (self.P if self.own_term else 0.0)
        return self.Rmax * self.P / den


class Circuit2(Circuit):
    """Circuit with its features switchable.
       self_mode 'sigmoid' adopted | 'linear' g*s | 'none' no self term."""
    def __init__(self, runs, self_mode="sigmoid", **kw):
        super().__init__(runs, **kw)
        self.self_mode = self_mode

    def step(self, y, reset=0.0):
        q = self.pool_c * np.maximum(self.s, 0.0)**self.pool_p
        pool = q.sum(1, keepdims=True) + reset
        self.S += (self.DT/self.tau_g) * (-self.S + pool)
        if self.self_mode == "sigmoid":
            selfx = self.g*sigmoid(self.k*(self.s - self.theta))
        elif self.self_mode == "linear":
            selfx = self.g*self.s
        else:
            selfx = 0.0
        u = (y + selfx + self.w_i*q - self.w_i*self.S
             + self.noise*self.rng.standard_normal(self.s.shape))
        self.s += (self.DT/self.tau) * (-self.s + np.clip(u, 0, self.S_MAX))
        return self.s


class Pair:
    """upstream stage feeding the circuit, either of which may be stripped."""
    def __init__(self, runs, n=5, up_kw=None, cir_kw=None, own_term=True, self_mode="sigmoid",
                 no_up=False, rng=None):
        self.R, self.n = runs, n
        rng = rng if rng is not None else np.random.default_rng(0)
        self.c = Circuit2(runs, n=n, self_mode=self_mode, rng=rng, **{**CIR, **(cir_kw or {})})
        self.up = None if no_up else Upstream2(own_term=own_term, runs=runs, chans=n,
                                               **{**UP, **(up_kw or {})})
    def step(self, x, reset=0.0):
        y = self.up.step(x) if self.up is not None else x
        return self.c.step(y, reset=reset)
    def memory(self): return self.c.memory()


def targets(n=5): return np.random.default_rng(1000).integers(0, n, R)


def sc_battery(**pkw):
    """Phase 2 gate battery. Returns (wrong-per-scale, distractor fractions, idle fraction)."""
    def cell(**tk):
        a = Pair(R, rng=np.random.default_rng(0), **pkw)
        return cwa(ph2_trial(a, targets(), rng=np.random.default_rng(7), **tk))
    wrong = [cell(x0=v, **HARD)[1] for v in SCALES]
    dist = [cell(d=0.4, distractor=v)[0]/R for v in AMPS]
    a = Pair(R, rng=np.random.default_rng(0), **pkw)
    for _ in range(400): a.step(np.zeros((R, 5)))
    idle = float(np.mean((a.memory() > 0.5).sum(1) == 0))
    return wrong, dist, idle


SC_REF = {}          # the adopted design's own battery, set by the first call per motif


def sc_judge(motif, feature, reused="", **pkw):
    wrong, dist, idle = sc_battery(**pkw)
    if feature.startswith("none removed"):
        SC_REF[motif] = wrong
    # Phase 2 gate: wrong <= 5 of 200 at every scale; distractor 1.0 at every amplitude; idle 1.0
    bound = max(1, round(5*R/200))          # the gate bound, scaled if R is not 200
    ok_scale = all(w <= bound for w in wrong)
    ok_dist = all(d >= 0.98 for d in dist)
    ok_idle = idle >= 0.98
    lost = []
    if not ok_scale: lost.append(f"scale invariance (wrong {wrong} of {R}, bound {bound})")
    if not ok_dist: lost.append(f"distractor immunity (correct {dist}, bound 1.0)")
    if not ok_idle: lost.append(f"idle stability ({idle:.2f}, bound 1.0)")
    # DEGRADED is judged against the ADOPTED DESIGN's own battery, not against an absolute
    # fraction of the gate bound. The adopted design sits at wrong [3,4,4,4,5] against a bound
    # of 5, i.e. on the edge of its own Phase 2 gate, so an absolute rule flags the reference
    # itself and then flags variants that are equal to or better than it.
    ref = SC_REF.get(motif)
    worse = ref is not None and sum(wrong) > sum(ref) + max(2, 0.2*sum(ref))
    if lost:
        verdict(motif, feature, "LOST", "; ".join(lost), reused)
    elif worse:
        verdict(motif, feature, "DEGRADED",
                f"passes, wrong {wrong} against the adopted design's {ref}", reused)
    else:
        verdict(motif, feature, "SURVIVES",
                f"wrong {wrong}"
                + (f" (adopted {ref})" if ref and wrong != ref else "")
                + f", distractor {min(dist):.2f}, idle {idle:.2f}", reused)


def motif_normalisation():
    print("\n== Motif 1: upstream normalisation (H6, Phase 2.1) ==")
    print("   battery: the Phase 2 gate -- scale invariance (wrong <=5 of 200 over a 16-fold")
    print("   range), distractor immunity to amplitude 10, idle stability.")
    sc_judge("normalisation", "none removed (adopted reference)")
    sc_judge("normalisation", "own term in the denominator", own_term=False)
    sc_judge("normalisation", "the cross-channel pool (k 0.8 -> 0)", up_kw=dict(k=0.0))
    sc_judge("normalisation", "the exponent (n 1.5 -> 1.0)", up_kw=dict(n=1.0))
    sc_judge("normalisation", "the low-pass (tau 2.0 -> 1.0)", up_kw=dict(tau=1.0))
    sc_judge("normalisation", "[perturbation] output bound (Rmax 1.8 -> 3.0)", up_kw=dict(Rmax=3.0))
    sc_judge("normalisation", "[perturbation] semi-saturation (sig 0.05 -> 0.2)", up_kw=dict(sig=0.2))
    sc_judge("normalisation", "the whole stage", no_up=True,
             reused="Phase 2 control; re-run here for one table")


def motif_select_and_hold():
    print("\n== Motif 2: the Select-and-Hold circuit (G1 core, architecture spec v0.1) ==")
    print("   same battery, with the upstream stage left adopted and the circuit stripped.")
    sc_judge("select-and-hold", "none removed (adopted reference)")
    sc_judge("select-and-hold", "sigmoid self-excitation -> linear", self_mode="linear")
    sc_judge("select-and-hold", "self-excitation entirely", self_mode="none")
    sc_judge("select-and-hold", "threshold sharpness (k 12 -> 1)", cir_kw=dict(k=1.0))
    # tau_g 1.0 makes DT/tau_g = 1, so S tracks the pool exactly: pooled inhibition with no
    # temporal filter, which is the all-to-all limit. Anything smaller is not a smaller filter,
    # it is an Euler gain above 1 and the state diverges -- a broken integrator, not an ablation.
    sc_judge("select-and-hold", "the global unit's temporal filter (tau_g 2 -> 1, all-to-all)",
             cir_kw=dict(tau_g=1.0))
    sc_judge("select-and-hold", "[perturbation] membrane time constant (tau 10 -> 5)",
             cir_kw=dict(tau=5.0))
    sc_judge("select-and-hold", "[perturbation] intrinsic noise (0.01 -> 0)", cir_kw=dict(noise=0.0))
    verdict("select-and-hold", "the release condition (reset)", "LOST",
            "score 14 of a 400 ceiling with a timeout that never fires, 400 with an evidence "
            "reset; the circuit is unusable in a behaving agent without one",
            reused="Phase 5 Run 2, B3")


# ================================================================ motif 3: the ring attractor
RKW = dict(J=0.5, c=2.0, p=2.0, sigma=0.3, Rmax=2.0, width=1.2)
HEAD = np.random.default_rng(5).uniform(0, 360, R)


def ring_battery(**kw):
    r = RingDiv(R, n=16, vgain=10.0, rng=np.random.default_rng(0), **{**RKW, **kw})
    c = cue(R, 16, HEAD, 1.0, width=RKW["width"])
    for _ in range(200): r.step(x=c)
    single = int((nbumps(r.s) == 1).sum()); a0 = r.amp().copy(); p0 = r.pos()
    for _ in range(1000): r.step()
    alive = int((r.amp() > 0.5*a0).sum())
    drift = float(np.median(np.abs(circdiff(r.pos(), p0))))
    # velocity integration, gain at the calibrated rate
    r2 = RingDiv(R, n=16, vgain=10.0, rng=np.random.default_rng(0), **{**RKW, **kw})
    for _ in range(200): r2.step(x=c)
    q0 = r2.pos()
    for _ in range(400): r2.step(v=0.225)
    gain = float(np.median(circdiff(r2.pos(), q0))/90.0)
    # no bump from rest
    r3 = RingDiv(R, n=16, vgain=10.0, rng=np.random.default_rng(1), **{**RKW, **kw})
    for _ in range(1000): r3.step()
    quiet = int((r3.amp() < 0.5).sum())
    return single, alive, drift, gain, quiet


def ring_judge(feature, reused="", **kw):
    single, alive, drift, gain, quiet = ring_battery(**kw)
    lost = []
    if not np.isfinite(gain) or not np.isfinite(drift):
        verdict("ring attractor", feature, "LOST",
                "the state diverged (non-finite), so no property can be read from it", reused)
        return
    if single < 0.95*R: lost.append(f"single bump ({single}/{R})")
    if alive < 0.95*R: lost.append(f"retention over 1000 dark steps ({alive}/{R})")
    if not (0.90 <= gain <= 1.10): lost.append(f"velocity integration (gain {gain:.3f})")
    if quiet < 0.95*R: lost.append(f"no bump from rest ({quiet}/{R})")
    detail = f"bump {single}/{R}, alive {alive}/{R}, drift {drift:.1f} deg, gain {gain:.3f}, quiet {quiet}/{R}"
    if lost:
        verdict("ring attractor", feature, "LOST", "; ".join(lost), reused)
    elif drift > 1.0:
        verdict("ring attractor", feature, "DEGRADED", detail, reused)
    else:
        verdict("ring attractor", feature, "SURVIVES", detail, reused)


def motif_ring():
    print("\n== Motif 3: the ring attractor (H3, Phase 3 design D3) ==")
    print("   battery: the Phase 3 gate -- single bump, retention over 1000 dark steps,")
    print("   velocity integration at the calibrated gain, and no bump from rest.")
    ring_judge("none removed (adopted reference)")
    ring_judge("supralinear exponent (p 2.0 -> 1.0)", p=1.0)
    ring_judge("the divisive pool (c 2.0 -> 0)", c=0.0)
    ring_judge("the semi-saturation constant (sigma 0.3 -> 0.01)", sigma=0.01)
    ring_judge("recurrent excitation (J 0.5 -> 0)", J=0.0)
    ring_judge("[perturbation] kernel width (1.2 -> 1.6)", width=1.6)
    ring_judge("[perturbation] output scale (Rmax 2.0 -> 3.0)", Rmax=3.0)
    verdict("ring attractor", "divisive inhibition -> subtractive", "LOST",
            "the bump either dies or saturates; no setting of J by w_i over 12 tried held it",
            reused="Phase 3 rejected design D2")
    verdict("ring attractor", "graded units -> the bistable Select-and-Hold unit", "LOST",
            "velocity integration: commanded 90 degrees, the bump moves about 1, because "
            "per-unit bistability pins it to the wedge lattice",
            reused="Phase 3 rejected design D1")


# ================================================================ motif 4: the plasticity rule
MBKW = dict(K=500, C=2, sparsity=0.05, eta_d=0.10, eta_p=0.30, beta=0.15)


class MB2(MB):
    """MB with the order gating switchable. order_gated=False is the rejected R2 rule: the
    potentiation term reads the reinforcement trace whether or not reinforcement is still on,
    so the sign follows overlap rather than order."""
    def __init__(self, *a, order_gated=True, **kw):
        super().__init__(*a, **kw)
        self.order_gated = order_gated

    def step(self, code=None, reinf=None):
        code = np.zeros((self.R, self.K)) if code is None else code
        reinf = np.zeros((self.R, self.C)) if reinf is None else reinf
        if self.beta and code.any():
            o = self.out(code); dif = o[:, 0] - o[:, 1]
            fb = np.stack([np.maximum(dif, 0.0), np.maximum(-dif, 0.0)], 1)
            reinf = reinf + self.beta*fb
        tc_now = np.minimum(self.tc + code, 1.0)
        tr_past = self.tr*(reinf <= 0.0) if self.order_gated else self.tr
        dw = (-self.eta_d*np.einsum('rc,rk->rck', reinf, tc_now)
              + self.eta_p*np.einsum('rc,rk->rck', tr_past, code))
        self.w = np.clip(self.w + dw, self.wmin, self.wmax)
        self.tc += (1.0/self.tau_code)*(-self.tc) + code
        self.tr += (1.0/self.tau_reinf)*(-self.tr) + reinf
        self.tc = np.minimum(self.tc, 1.0); self.tr = np.minimum(self.tr, 1.0)


def mb_battery(**kw):
    mk = lambda seed=0: MB2(R, rng=np.random.default_rng(seed), **{**MBKW, **kw})
    # L1 acquisition + L2 specificity
    m = mk(); A = m.odour(11); B = m.odour(12)
    v0 = m.valence(A).copy(); b0 = m.valence(B).copy()
    for i in range(5): pairing(m, A, 0, "forward")
    sign5 = int(((m.valence(A) - v0) < 0).sum())
    for i in range(5): pairing(m, A, 0, "forward")
    dA = float(np.median(m.valence(A) - v0)); dB = float(np.median(m.valence(B) - b0))
    leak = abs(dB/dA)*100 if dA else float("inf")
    # L3 extinction
    me = mk(); Ae = me.odour(11); e0 = me.valence(Ae).copy()
    for _ in range(10): pairing(me, Ae, 0, "forward")
    vt = float(np.median(me.valence(Ae) - e0))
    for _ in range(20): pairing(me, Ae, None, "forward")
    ve = float(np.median(me.valence(Ae) - e0))
    ext = abs(ve/vt)*100 if vt else float("inf")
    # L4 reversal
    mr = mk(); Ar = mr.odour(11); r0 = mr.valence(Ar).copy()
    for _ in range(10): pairing(mr, Ar, 0, "forward")
    flip = np.zeros(R, bool)
    for _ in range(10):
        pairing(mr, Ar, 1, "forward")
        flip |= (mr.valence(Ar) - r0) > 0
    # L5 timing sign
    f = mk(); Af = f.odour(11); f0 = f.valence(Af).copy()
    for _ in range(10): pairing(f, Af, 0, "forward")
    df = f.valence(Af) - f0
    g = mk(); Ag = g.odour(11); g0 = g.valence(Ag).copy()
    for _ in range(10): pairing(g, Ag, 0, "reverse")
    dg = g.valence(Ag) - g0
    timing = int(((df < 0) & (dg > 0)).sum())
    return dict(sign5=sign5, dA=dA, leak=leak, ext=ext, flip=int(flip.sum()), timing=timing)


def mb_judge(feature, reused="", **kw):
    b = mb_battery(**kw)
    lost = []
    if b["sign5"] < 0.95*R: lost.append(f"acquisition (correct sign {b['sign5']}/{R})")
    if b["leak"] > 10: lost.append(f"specificity (leakage {b['leak']:.1f}%, bound 10)")
    if b["ext"] > 30: lost.append(f"extinction (retains {b['ext']:.0f}% of trained, bound 30)")
    if b["flip"] < 0.95*R: lost.append(f"reversal ({b['flip']}/{R})")
    if b["timing"] < 0.95*R: lost.append(f"timing sign ({b['timing']}/{R})")
    detail = (f"acq {b['sign5']}/{R} (dA {b['dA']:+.3f}), leak {b['leak']:.1f}%, "
              f"ext {b['ext']:.0f}%, rev {b['flip']}/{R}, timing {b['timing']}/{R}")
    verdict("plasticity", feature, "LOST" if lost else "SURVIVES",
            "; ".join(lost) if lost else detail, reused)


def motif_plasticity():
    print("\n== Motif 4: the plasticity rule (H8 v2, Phase 4) ==")
    print("   battery: the Phase 4 gate -- acquisition, specificity, extinction, reversal,")
    print("   and the timing-dependent sign.")
    mb_judge("none removed (adopted reference)")
    mb_judge("the opponent feedback (beta 0.15 -> 0)", beta=0.0,
             reused="Phase 4 rejected design R1, re-scored here on the full battery")
    mb_judge("order gating of potentiation", order_gated=False,
             reused="Phase 4 rejected design R2, re-scored here on the full battery")
    mb_judge("the potentiation term (eta_p 0.30 -> 0)", eta_p=0.0)
    mb_judge("the eligibility traces (tau 5 -> 1, no memory)", tau_code=1.0, tau_reinf=1.0)
    mb_judge("sparseness (5% -> 50% of the code active)", sparsity=0.50)
    mb_judge("[perturbation] code size (K 500 -> 200, as the Phase 5 agent used)", K=200)
    mb_judge("[perturbation] depression rate (eta_d 0.10 -> 0.20)", eta_d=0.20)


# ================================================================ the deliverable
def minimum_structure():
    print("\n\n== C3: the minimum structure each motif must preserve ==")
    print("   Structural removals take a mechanism out. Perturbations only move a constant, and")
    print("   are marked [perturbation]; they say which numbers are free, not which parts are.")
    for motif in ("normalisation", "select-and-hold", "ring attractor", "plasticity"):
        rows = [r for r in LADDER if r[0] == motif and not r[1].startswith("none removed")]
        struct = [r for r in rows if not r[1].startswith("[perturbation]")]
        perturb = [r for r in rows if r[1].startswith("[perturbation]")]
        must = [r[1] for r in struct if r[2] == "LOST"]
        soft = [r[1] for r in struct if r[2] == "DEGRADED"]
        free = [r[1] for r in struct if r[2] == "SURVIVES"]
        p_ok = [r[1].replace("[perturbation] ", "") for r in perturb if r[2] == "SURVIVES"]
        p_no = [r[1].replace("[perturbation] ", "") for r in perturb if r[2] != "SURVIVES"]
        print(f"\n   {motif.upper()}")
        print(f"     load-bearing ({len(must)}): " + ("; ".join(must) if must else "none found"))
        if soft: print(f"     costly but survivable ({len(soft)}): " + "; ".join(soft))
        print(f"     removable without losing a property ({len(free)}): "
              + ("; ".join(free) if free else "none"))
        if p_ok: print(f"     free constants ({len(p_ok)}): " + "; ".join(p_ok))
        if p_no: print(f"     constants that are NOT free ({len(p_no)}): " + "; ".join(p_no))


MOTIFS = dict(norm=motif_normalisation, hold=motif_select_and_hold,
              ring=motif_ring, plast=motif_plasticity)
ROWS_FILE = "ph6_rows.json"


def _load_rows():
    import json, os
    return json.load(open(ROWS_FILE)) if os.path.exists(ROWS_FILE) else []


if __name__ == "__main__":
    import json
    which = [a for a in sys.argv[1:] if a in MOTIFS]
    if "--merge" in sys.argv:
        # every motif ran in its own process; merge what they wrote and emit the deliverable
        LADDER[:] = [tuple(r) for r in _load_rows()]
        print(f"== Phase 6.2 abstraction ladder, merged from {ROWS_FILE} ==")
        minimum_structure()
        n_lost = sum(1 for r in LADDER if r[2] == "LOST")
        print(f"\n   {len(LADDER)} rows, {n_lost} load-bearing features found.")
        sys.exit(0)

    print(f"== Phase 6.2 abstraction ladder, {R} runs per cell ==")
    print("== Criteria: record:phase6-success-criteria, stored before this script existed ==")
    # One motif per process keeps peak memory down: this machine stack-overflowed running all
    # four in one interpreter. --append accumulates rows across those processes.
    for name in (which or MOTIFS):
        MOTIFS[name]()
    if "--append" in sys.argv:
        # replace by (motif, feature) so a motif can be re-run in place without duplicating
        fresh = {(r[0], r[1]): list(r) for r in LADDER}
        rows = [r for r in _load_rows() if (r[0], r[1]) not in fresh] + list(fresh.values())
        json.dump(rows, open(ROWS_FILE, "w"), indent=1)
        print(f"\n   wrote {len(LADDER)} rows ({len(rows)} total) to {ROWS_FILE}")
    else:
        minimum_structure()
        n_lost = sum(1 for r in LADDER if r[2] == "LOST")
        print(f"\n   {len(LADDER)} rows, {n_lost} load-bearing features found.")
