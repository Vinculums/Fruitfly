#!/usr/bin/env python3
"""Phase 3 run: ring attractor (H3), graded memory. Usage: python3 ph3_run.py"""
import numpy as np
from ph3 import Ring, RingDiv, cue, circdiff, nbumps

R = 200
KW = dict(J=0.5, c=2.0, p=2.0, sigma=0.3, Rmax=2.0, width=1.2)   # adopted design D3
VGAIN = 10.0                                                      # calibrated once, at 0.225 deg/step
HEAD = np.random.default_rng(5).uniform(0, 360, R)

def mk(n=16, vgain=VGAIN, seed=0, **kw): return RingDiv(R, n=n, vgain=vgain, rng=np.random.default_rng(seed), **{**KW, **kw})
def cued(r, deg, steps=200, amp=1.0, n=16):
    c = cue(R, n, deg, amp, width=KW["width"])
    for _ in range(steps): r.step(x=c)
    return r

def c1_c2(n=16, label="N=16"):
    r = cued(mk(n=n), HEAD, n=n)
    nb = nbumps(r.s); a0 = r.amp().copy(); p0 = r.pos()
    e0 = np.abs(circdiff(p0, HEAD))
    for _ in range(1000): r.step()
    d = np.abs(circdiff(r.pos(), p0))
    print(f"[{label}] C1 single bump {int((nb==1).sum())}/{R}   cue error median {np.median(e0):.1f} deg")
    print(f"[{label}] C2 alive after 1000 dark steps {int((r.amp()>0.5*a0).sum())}/{R}"
          f"   drift median {np.median(d):.1f} p90 {np.percentile(d,90):.1f} max {d.max():.1f} deg")
    return d

def c3(n=16, label="N=16"):
    print(f"[{label}] C3 velocity integration, one gain calibrated at 0.225 deg/step:")
    for v in (0.05625, 0.1125, 0.225, 0.45):
        r = cued(mk(n=n), HEAD, n=n); p0 = r.pos()
        for _ in range(400): r.step(v=v)
        got = circdiff(r.pos(), p0); cmd = v*400
        err = np.abs(got - cmd)
        print(f"   v {v:7.5f} deg/step, commanded {cmd:6.1f} deg: gain {np.median(got)/cmd:.3f}"
              f"  median abs error {np.median(err):.1f} deg")

def c4(n=16, label="N=16"):
    r = cued(mk(n=n), HEAD, n=n)
    for _ in range(1000): r.step()
    before = np.abs(circdiff(r.pos(), HEAD))
    c = cue(R, n, HEAD, 1.0, width=KW["width"])
    for _ in range(100): r.step(x=c)
    after = np.abs(circdiff(r.pos(), HEAD))
    print(f"[{label}] C4 cue correction: error before {np.median(before):.1f} deg,"
          f" after {np.median(after):.1f} deg, ratio {np.median(before)/max(np.median(after),1e-9):.1f}x")

def c5(n=16, label="N=16"):
    r = mk(n=n, seed=1)
    for _ in range(1000): r.step()
    print(f"[{label}] C5 no bump from rest: {int((r.amp()<0.5).sum())}/{R}  mean peak {r.amp().mean():.3f}")

def ring_sizes():
    print("\n== Reported, not gated: ring size ==")
    for n in (8, 16, 32):
        c1_c2(n=n, label=f"N={n}"); c3(n=n, label=f"N={n}"); c4(n=n, label=f"N={n}"); c5(n=n, label=f"N={n}")

def stress():
    print("\n== Reported, not gated: how weak are the gated numbers? ==")
    print("   Drift over 1000 dark steps against internal noise:")
    for nz in (0.01, 0.05, 0.1, 0.3, 1.0):
        r = cued(mk(noise=nz), HEAD); p0 = r.pos(); a0 = r.amp().copy()
        for _ in range(1000): r.step()
        d = np.abs(circdiff(r.pos(), p0))
        print(f"      noise sd {nz:4.2f}: alive {int((r.amp()>0.5*a0).sum())}/{R}"
              f"  drift median {np.median(d):5.1f} p90 {np.percentile(d,90):6.1f} deg")
    print("   Landmark recapture: bump held at one heading, landmark then shown 90 deg away")
    for nz in (0.01, 0.1):
        for amp in (0.3, 0.5, 1.0, 2.0):
            r = cued(mk(noise=nz), HEAD)
            tgt2 = (HEAD + 90.0) % 360.0
            c = cue(R, 16, tgt2, amp, width=KW["width"])
            for _ in range(200): r.step(x=c)
            e = np.abs(circdiff(r.pos(), tgt2))
            print(f"      noise {nz:4.2f} cue amplitude {amp:4.2f}: captured (within 15 deg)"
                  f" {int((e<15).sum())}/{R}, median error {np.median(e):5.1f} deg")

def rejected_designs():
    print("\n== Rejected design D1: the Select-and-Hold bistable unit placed on a ring ==")
    for J, g in ((1.0, 2.0), (1.5, 2.0), (2.0, 2.0)):
        gains = []
        for vg in (1.0, 2.0, 4.0, 8.0):
            r = Ring(R, n=16, J=J, g=g, w_i=1.0, width=1.2, theta=0.5, vgain=vg,
                     rng=np.random.default_rng(0))
            c = cue(R, 16, HEAD, 1.0)
            for _ in range(200): r.step(x=c)
            p0 = r.pos()
            for _ in range(400): r.step(v=0.225)
            gains.append(round(float(np.median(circdiff(r.pos(), p0)))/90, 3))
        print(f"   J {J} g {g}: velocity gain at vgain 1,2,4,8 = {gains}  (bump pinned to wedges)")
    print("\n== Rejected design D2: graded unit, subtractive global inhibition ==")
    for J in (1.2, 1.5, 2.0, 2.5):
        for wi in (0.6, 1.0, 1.4):
            r = Ring(R, n=16, J=J, g=0.0, w_i=wi, width=1.2, theta=0.5, rng=np.random.default_rng(0))
            c = cue(R, 16, HEAD, 1.0)
            for _ in range(200): r.step(x=c)
            a0 = r.amp().mean()
            for _ in range(1000): r.step()
            print(f"   J {J} w_i {wi}: peak at cue offset {a0:.2f} -> after 1000 dark steps {r.amp().mean():.2f}")

if __name__ == "__main__":
    print("== Adopted design D3: divisive global inhibition, graded units, 16 wedges ==")
    c1_c2(); c3(); c4(); c5()
    ring_sizes(); stress(); rejected_designs()
