#!/usr/bin/env python3
"""H14: repair the ring attractor's velocity integration.

Usage: python3 ph10.py [--quick] [demo|sweep|battery|agent|all]

The adopted ring (ph3.RingDiv) shifts its excitation kernel by a FIRST-ORDER approximation:

    W(o - delta) ~= W(o) - delta * W'(o)          exc = s @ W.T - delta * (s @ Wp.T)

That is accurate only while delta is small against the kernel width. Phase 3 calibrated one
gain at 0.225 deg/step, where delta is 0.01 wedges, and reported 0.997 to 0.999 across a tested
range of 0.056 to 0.45 deg/step. Phase 7.3 drives it at up to 40 deg/step, where delta is 17.8
wedges on a ring of 16. Measured there the gain is 0.13 at 5 deg/step and -0.06 at 20: not
merely inaccurate, sign reversed, and in the agent the ring is the worst of three heading
options rather than the best.

The repair keeps the mechanism and drops the approximation. The shift is still an asymmetric
connection kernel, which is what the fly's PEN neurons are taken to implement; it is simply
built at the offset it actually wants rather than linearised about zero:

    W_shift[i,j] = J * exp(-0.5 * ((wrap(o_ij - delta)) / width)^2)

Criteria: record:h14-success-criteria, stored before this file. I4 is why the state-rolling
version below is run as a comparison and is not eligible for adoption: it works, and it is a
numerical trick rather than a circuit.

ph3.py is NOT edited. The original is imported and used as the control, so Phase 3's recorded
numbers stay reproducible and what was adopted then stays on record.
"""
import sys
import numpy as np
from ph3 import RingDiv, cue, circdiff, nbumps

R = 200
QUICK = "--quick" in sys.argv
if QUICK: R = 40

KW = dict(J=0.5, c=2.0, p=2.0, sigma=0.3, Rmax=2.0, width=1.2)   # Phase 3's adopted design
VG_OLD = 10.0        # Phase 3's fitted gain, for the linearised shift
VG_NEW = 1.0         # kinematically exact for a true shift: delta wedges = v * n/360
HEAD = None          # set per ring size


class RingExact:
    """Phase 3's D3 with the velocity shift built exactly instead of linearised.

    Everything else is identical to RingDiv: graded units, divisive normalisation by a pooled
    unit, persistence from recurrence. Only the kernel construction changes.
    """
    DT = 1.0

    def __init__(self, runs, n=16, J=1.0, width=1.2, p=2.0, sigma=0.3, c=1.0, Rmax=2.0,
                 tau=10.0, vgain=VG_NEW, noise=0.01, rng=None):
        self.R, self.n, self.p, self.sigma, self.c, self.Rmax = runs, n, p, sigma, c, Rmax
        self.tau, self.vgain, self.noise, self.J, self.width = tau, vgain, noise, J, width
        self.rng = rng if rng is not None else np.random.default_rng(0)
        self.s = np.zeros((runs, n))
        i = np.arange(n)[:, None]; j = np.arange(n)[None, :]
        self.o = ((i - j + n//2) % n) - n//2          # signed circular offset, (n, n)
        self.ang = 2*np.pi*np.arange(n)/n

    def pos(self):
        return np.degrees(np.angle((self.s*np.exp(1j*self.ang)).sum(1))) % 360.0

    def amp(self): return self.s.max(1)

    def step(self, x=None, v=0.0):
        s = self.s
        delta = np.asarray(self.vgain*v*self.n/360.0, dtype=float).reshape(-1, 1, 1)
        # the kernel at the offset it actually wants, wrapped onto the ring
        oo = ((self.o[None, :, :] - delta + self.n/2) % self.n) - self.n/2
        W = self.J*np.exp(-0.5*(oo/self.width)**2)
        exc = np.einsum('rij,rj->ri', W, s) + self.noise*self.rng.standard_normal(s.shape)
        if x is not None: exc = exc + x
        e = np.maximum(exc, 0.0)**self.p
        r = self.Rmax*e / (self.sigma**self.p + self.c*e.mean(1, keepdims=True))
        self.s = s + (self.DT/self.tau)*(-s + r)
        return self.s


class RingRoll(RingExact):
    """Comparison only, NOT eligible for adoption under criterion I4.

    Shifts the state array itself by linear interpolation between wedges and then applies the
    unshifted kernel. Identical outcome, a fraction of the cost, and not a circuit: no set of
    synaptic weights does this, so it answers a different question from the one the project asks.
    """

    def step(self, x=None, v=0.0):
        s = self.s
        delta = np.asarray(self.vgain*v*self.n/360.0, dtype=float)
        if delta.ndim == 0: delta = np.full(self.R, float(delta))
        k = np.floor(delta).astype(int); frac = (delta - k)[:, None]
        idx = (np.arange(self.n)[None, :] - k[:, None]) % self.n
        s0 = np.take_along_axis(s, idx, 1)
        s1 = np.take_along_axis(s, (idx - 1) % self.n, 1)
        sh = (1.0 - frac)*s0 + frac*s1
        W = self.J*np.exp(-0.5*(self.o/self.width)**2)
        exc = sh @ W.T + self.noise*self.rng.standard_normal(s.shape)
        if x is not None: exc = exc + x
        e = np.maximum(exc, 0.0)**self.p
        r = self.Rmax*e / (self.sigma**self.p + self.c*e.mean(1, keepdims=True))
        self.s = s + (self.DT/self.tau)*(-s + r)
        return self.s


def mk(kind, n=16, vgain=None, noise=0.01, seed=0, tau=10.0, **kw):
    """The velocity gain is not free. A kernel offset is a FORCE on the attractor, not a
    position command, so the bump's drift rate is the offset divided by the time constant.
    The gain that makes the bump track the command is therefore tau, which is exactly why
    Phase 3 fitted 10 for a tau of 10 and why that fit was never about the linearisation.
    """
    cls = {"old": RingDiv, "exact": RingExact, "roll": RingRoll}[kind]
    vg = vgain if vgain is not None else tau
    return cls(R, n=n, vgain=vg, noise=noise, tau=tau,
               rng=np.random.default_rng(seed), **{**KW, **kw})


def heads(n_runs):
    return np.random.default_rng(5).uniform(0, 360, n_runs)


def cued(r, deg, n=16, steps=200, amp=1.0):
    c = cue(R, n, deg, amp, width=KW["width"])
    for _ in range(steps): r.step(x=c)
    return r


# ---------------------------------------------------------------- I1, the velocity sweep
VELOCITIES = (0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 40.0)


def gain_at(kind, v, n=16, tau=10.0, steps=100):
    """Gain on UNWRAPPED cumulative displacement.

    Dividing a single circdiff folds anything past half a turn. At v=2 over 100 steps the
    command is 200 degrees, folds to -160, and reads as gain -0.8. That artifact is what the
    Phase 7.3 claim of a sign reversal rested on; see record:ring-attractor-out-of-velocity-range,
    which this run corrects. Accumulating per-step deltas cannot fold, because one step never
    moves the bump half a turn.
    """
    r = cued(mk(kind, n=n, tau=tau), heads(R), n=n)
    prev = r.pos(); total = np.zeros(R)
    for _ in range(steps):
        r.step(v=v)
        now = r.pos(); total += circdiff(now, prev); prev = now
    return float(np.median(total))/(v*steps)


def i1_sweep():
    print("\n== I1: velocity gain across the range a behaving agent uses ==")
    print("   Gain on unwrapped cumulative displacement. The velocity gain is set to tau for")
    print("   every design, which is the value that makes a kernel offset track the command.")
    cols = [("old", 10.0), ("exact", 10.0), ("exact", 5.0), ("exact", 2.0), ("exact", 1.0),
            ("roll", 2.0)]
    head = " ".join(f"{k[:5]}/t{int(t):<2d}".rjust(10) for k, t in cols)
    print(f"   {'v deg/step':>11} {head}")
    rows = {}
    for v in VELOCITIES:
        rows[v] = [gain_at(k, v, tau=t) for k, t in cols]
        print(f"   {v:11.2f} " + " ".join(f"{g:10.3f}" for g in rows[v]))
    ok = {}
    line = []
    for i, (k, t) in enumerate(cols):
        good = all(0.90 <= rows[v][i] <= 1.10 for v in VELOCITIES)
        ok[(k, t)] = good
        line.append(f"{'pass' if good else 'FAIL':>10}")
    print(f"   {'I1 verdict':>11} " + " ".join(line))
    print("   The old design does not reverse sign: it under-rotates progressively, reaching")
    print(f"   {rows[20.0][0]:.2f} at 20 deg/step and {rows[40.0][0]:.2f} at 40.")
    return ok, rows, cols


# ---------------------------------------------------------------- I2, Phase 3's own battery
def i2_battery(kind, n=16, tau=10.0):
    H = heads(R)
    r = cued(mk(kind, n=n, tau=tau), H, n=n)
    single = int((nbumps(r.s) == 1).sum()); a0 = r.amp().copy(); p0 = r.pos()
    err0 = float(np.median(np.abs(circdiff(p0, H))))
    for _ in range(1000): r.step()
    alive = int((r.amp() > 0.5*a0).sum())
    drift = float(np.median(np.abs(circdiff(r.pos(), p0))))
    before = float(np.median(np.abs(circdiff(r.pos(), H))))
    c = cue(R, n, H, 1.0, width=KW["width"])
    for _ in range(100): r.step(x=c)
    after = float(np.median(np.abs(circdiff(r.pos(), H))))
    ratio = before/max(after, 1e-9)
    q = mk(kind, n=n, seed=1, tau=tau)
    for _ in range(1000): q.step()
    quiet = int((q.amp() < 0.5).sum())
    ok = (single >= 0.95*R and alive >= 0.95*R and drift <= 1.0
          and ratio > 1.0 and quiet >= 0.95*R)
    return dict(single=single, alive=alive, drift=drift, cue_err=err0, ratio=ratio,
                quiet=quiet, ok=ok)


def i2_run(taus=(10.0, 5.0, 2.0, 1.0)):
    print("\n== I2: Phase 3's C1 to C5 battery, at Phase 3's own bounds ==")
    print("   Tracking fast needs a small offset, which needs a small tau. The question is")
    print("   what that costs the properties Phase 3 adopted the design for.")
    allok = {}
    for n in (8, 16, 32):
        print(f"   ring size {n}")
        b = i2_battery("old", n=n, tau=10.0)
        allok[("old", n, 10.0)] = b["ok"]
        print(f"     {'old   tau 10':14s} bump {b['single']:3d}/{R}  alive {b['alive']:3d}/{R}"
              f"  drift {b['drift']:5.2f} deg  cue x{b['ratio']:5.1f}"
              f"  quiet {b['quiet']:3d}/{R}  -> {'pass' if b['ok'] else 'FAIL'}")
        for tau in taus:
            b = i2_battery("exact", n=n, tau=tau)
            allok[("exact", n, tau)] = b["ok"]
            print(f"     {'exact tau ' + str(int(tau)):14s} bump {b['single']:3d}/{R}"
                  f"  alive {b['alive']:3d}/{R}  drift {b['drift']:5.2f} deg"
                  f"  cue x{b['ratio']:5.1f}  quiet {b['quiet']:3d}/{R}"
                  f"  -> {'pass' if b['ok'] else 'FAIL'}")
    return allok


def i2b_rescue():
    """ADDED after I2, and disclosed as added.

    At tau 1 the only Phase 3 criterion that fails is C5, no bump from rest: the ring ignites
    on noise. Sigma is the semi-saturation constant, which is the ignition threshold, and the
    Phase 6 ladder already found it load-bearing for exactly that property. So there is one
    principled thing to try before concluding the trade is unavoidable: raise sigma at tau 1
    and see whether quiet returns without losing the tracking that tau 1 bought.
    """
    print("\n== I2b: can a higher ignition threshold rescue tau 1? (ADDED after I2) ==")
    print(f"   {'sigma':>6} {'quiet n16':>10} {'drift':>7} {'bump':>7} {'alive':>7}"
          f" {'gain v1':>8} {'gain v40':>9}")
    out = []
    for sg in (0.3, 0.5, 0.8, 1.2, 2.0):
        H = heads(R)
        r = cued(mk("exact", n=16, tau=1.0, sigma=sg), H, n=16)
        single = int((nbumps(r.s) == 1).sum()); a0 = r.amp().copy(); p0 = r.pos()
        for _ in range(1000): r.step()
        alive = int((r.amp() > 0.5*a0).sum())
        drift = float(np.median(np.abs(circdiff(r.pos(), p0))))
        q = mk("exact", n=16, tau=1.0, sigma=sg, seed=1)
        for _ in range(1000): q.step()
        quiet = int((q.amp() < 0.5).sum())
        g1 = gain_sigma(1.0, sg); g40 = gain_sigma(40.0, sg)
        ok = (quiet >= 0.95*R and alive >= 0.95*R and single >= 0.95*R and drift <= 1.0
              and 0.90 <= g1 <= 1.10 and 0.90 <= g40 <= 1.10)
        out.append((sg, ok))
        print(f"   {sg:6.1f} {quiet:6d}/{R:<3d} {drift:7.2f} {single:5d}/{R:<3d}"
              f" {alive:5d}/{R:<3d} {g1:8.3f} {g40:9.3f}  {'pass' if ok else 'FAIL'}")
    hits = [s for s, ok in out if ok]
    print(f"   -> sigma values rescuing tau 1 on every criterion: {hits if hits else 'NONE'}")
    return hits


def gain_sigma(v, sigma, tau=1.0, n=16, steps=100):
    r = cued(mk("exact", n=n, tau=tau, sigma=sigma), heads(R), n=n)
    prev = r.pos(); total = np.zeros(R)
    for _ in range(steps):
        r.step(v=v)
        now = r.pos(); total += circdiff(now, prev); prev = now
    return float(np.median(total))/(v*steps)


# ---------------------------------------------------------------- I3, back in the agent
def i3_agent():
    """Phase 7.3's heading comparison, with the repaired ring swapped in. ph9 is not edited."""
    print("\n== I3: back in the Phase 7.3 agent ==")
    print("   The claim is NOT that the ring beats dead reckoning. Phase 7.3 showed heading")
    print("   memory carries little behaviour in that task. The claim is that it stops losing.")
    import ph9
    ph9.R = R

    cfg = {"kind": "exact", "tau": 2.0}

    class NavFixed(ph9.Nav):
        def __init__(self, runs, rng, **kw):
            super().__init__(runs, rng, **kw)
            if kw.get("head_mem") == "ring":
                self.ring = mk(cfg["kind"], n=16, noise=0.3, seed=0, tau=cfg["tau"])

    def go(head_mem, p_wind, kind="exact", tau=2.0):
        cfg["kind"], cfg["tau"] = kind, tau
        w = ph9.WindWorld(R, np.random.default_rng(0), p_hit=0.3, p_wind=p_wind)
        a = NavFixed(R, np.random.default_rng(1), rule="cast", head_mem=head_mem)
        return ph9.episode(w, a)

    print(f"   {'p_wind':>7} {'dead reckon':>12} {'old ring':>9} {'exact t10':>10}"
          f" {'exact t2':>9} {'roll t2':>8}   repaired vs dead reckoning")
    out = {}
    for pw in (1.0, 0.5, 0.2):
        base = go("integrate", pw)
        old = go("ring", pw, kind="old", tau=10.0)
        e10 = go("ring", pw, kind="exact", tau=10.0)
        e2 = go("ring", pw, kind="exact", tau=2.0)
        r2 = go("ring", pw, kind="roll", tau=2.0)
        mb, mo, m10, m2, mr = (float(np.median(x)) for x in (base, old, e10, e2, r2))
        # I3: the repaired ring must not LOSE to dead reckoning by the project's margin
        loses = ((mb - m2)/abs(mb) if mb else 0.0) >= 0.25 and float((base > e2).mean()) >= 0.60
        out[pw] = not loses
        print(f"   {pw:7.1f} {mb:12.1f} {mo:9.1f} {m10:10.1f} {m2:9.1f} {mr:8.1f}"
              f"   {'still loses' if loses else 'does not lose'}")
    return out


def demo():
    """self-check: the exact kernel really is a shift, and the linearised one really is not."""
    n, width, J = 16, 1.2, 0.5
    i = np.arange(n)[:, None]; j = np.arange(n)[None, :]
    o = ((i - j + n//2) % n) - n//2
    W = J*np.exp(-0.5*(o/width)**2)
    Wp = -(o/width**2)*W
    for d in (0.05, 1.0, 4.0):
        oo = ((o - d + n/2) % n) - n/2
        exact = J*np.exp(-0.5*(oo/width)**2)
        lin = W - d*Wp
        err = np.abs(exact - lin).max()/max(np.abs(exact).max(), 1e-12)
        print(f"ok  delta {d:4.2f} wedges: linearised kernel differs from the true shift by"
              f" {err*100:6.1f}% of peak")
    oo = ((o - 4.0 + n/2) % n) - n/2
    assert np.abs(J*np.exp(-0.5*(oo/width)**2) - (W - 4.0*Wp)).max() > 1.0, \
        "the linear approximation should be badly wrong at 4 wedges"
    # and a lone bump really does move the commanded amount under the exact kernel
    r = mk("exact"); c = cue(R, 16, np.zeros(R), 1.0, width=width)
    for _ in range(200): r.step(x=c)
    p0 = r.pos()
    for _ in range(100): r.step(v=20.0)
    got = float(np.median(circdiff(r.pos(), p0)))
    print(f"ok  exact ring at 20 deg/step: commanded 2000 deg, moved {got:.1f} deg"
          f" ({(got % 360):.1f} mod 360), gain {got/2000:.3f}")


if __name__ == "__main__":
    what = [a for a in sys.argv[1:] if a in ("demo", "sweep", "battery", "agent", "all")] or ["all"]
    if "demo" in what:
        demo(); sys.exit(0)
    print(f"== H14: repairing the ring's velocity integration. {R} runs per cell ==")
    print("== Criteria: record:h14-success-criteria, stored before this file existed ==")
    i1 = i1_sweep() if ("sweep" in what or "all" in what) else None
    i2 = i2_run() if ("battery" in what or "all" in what) else None
    i2b = i2b_rescue() if ("battery" in what or "all" in what) else None
    i3 = i3_agent() if ("agent" in what or "all" in what) else None
    if i1 and i2 and i3:
        ok1, _, _ = i1
        # the candidate for adoption: exact kernel, and the smallest tau that passes I2
        cands = [t for t in (10.0, 5.0, 2.0, 1.0)
                 if ok1.get(("exact", t)) and all(i2.get(("exact", n, t)) for n in (8, 16, 32))]
        print("\n== H14 verdict ==")
        print(f"   I1 passed by: {[f'{k}/tau{int(t)}' for (k, t), v in ok1.items() if v] or 'nothing'}")
        print(f"   settings passing I1 AND I2 at all three ring sizes: "
              f"{[f'exact/tau{int(t)}' for t in cands] or 'NONE'}")
        print(f"   I2b sigma rescue of tau 1: {i2b if i2b else 'NONE'}")
        print(f"   I3 (does not lose to dead reckoning): "
              f"{'pass' if all(i3.values()) else 'FAIL'}")
        ok = bool((cands or i2b) and all(i3.values()))
        print(f"   -> H14 {'SUPPORTED' if ok else 'not supported'}")
        print("   The roll variant is reported alongside and is not eligible under I4.")
