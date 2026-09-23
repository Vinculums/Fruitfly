#!/usr/bin/env python3
"""Phase 2 run: H6 (upstream normalisation) and H7 (option-count calibration).
Usage: python3 ph2_run.py            reproduces every table in the Phase 2 report."""
import numpy as np
from ph2 import Agent, trial, cwa

R = 200
UP = dict(n=1.5, sig=0.05, Rmax=1.8, k=0.8)     # adopted upstream stage
C  = dict(theta=1.0, k=12.0)                    # circuit retuned for the normalised input
HARD = dict(d=0.05, cue=300)

def targets(n=5): return np.random.default_rng(1000).integers(0, n, R)
def agent(n=5, up=UP, ckw=None): return Agent(R, n=n, up=up, rng=np.random.default_rng(0), **(ckw or C))
def cell(n=5, up=UP, ckw=None, **tk):
    return cwa(trial(agent(n, up, ckw), targets(n), rng=np.random.default_rng(7), **tk))
def idle(n=5, up=UP, ckw=None):
    a = agent(n, up, ckw)
    for _ in range(400): a.step(np.zeros((R, n)))
    return float(np.mean((a.memory() > 0.5).sum(1) == 0))

def gate():
    print("== Adopted design U1: upstream normalisation + retuned Select-and-Hold ==")
    print("idle (no input, 400 steps, fraction empty):", idle())
    print("scale, hard cue, correct/wrong/abstain, x0 0.25 0.5 1 2 4:")
    print("  ", [cell(x0=v, **HARD) for v in (0.25, 0.5, 1, 2, 4)])
    print("scale, easy cue, fraction correct:")
    print("  ", [cell(x0=v, d=0.4)[0]/R for v in (0.25, 0.5, 1, 2, 4)])
    print("option count, hard cue, N 2 3 5 10 20:")
    print("  ", [cell(n=v, **HARD) for v in (2, 3, 5, 10, 20)])
    print("option count, easy cue, fraction correct:")
    print("  ", [cell(n=v, d=0.4)[0]/R for v in (2, 3, 5, 10, 20)])
    print("distractor in the delay, easy cue, amplitude 1 2 3 4 6 10:")
    print("  ", [cell(d=0.4, distractor=v)[0]/R for v in (1, 2, 3, 4, 6, 10)])
    a = agent(); t0 = targets(); rng = np.random.default_rng(7)
    print("three sequential trials with reset:",
          [round(float((trial(a, (t0+i) % 5, d=0.4, reset=i > 0, rng=rng) == 1).mean()), 3) for i in range(3)])

def control():
    print("\n== Control: same circuit, no upstream stage (this is G1/B2 retuned) ==")
    print("scale, hard cue:", [cell(up=None, x0=v, **HARD) for v in (0.25, 0.5, 1, 2, 4)])
    print("distractor:     ", [cell(up=None, d=0.4, distractor=v)[0]/R for v in (1, 2, 3, 4, 6, 10)])

def threshold_sweep():
    print("\n== Retuning the decision threshold for the normalised input (hard cue) ==")
    for th in (1.0, 1.05, 1.1, 1.15, 1.2):
        print("  theta", th, [cell(ckw=dict(theta=th, k=ks), **HARD) for ks in (8, 12, 16)])

def h7_attempt_1():
    print("\n== H7 attempt 1, REJECTED: saturating global inhibitory unit ==")
    for Smax in (2.5, 3.0, 4.0):
        for kap in (0.5, 1.0, 2.0):
            ck = dict(C, gsat=(Smax, kap))
            print(f"  Smax {Smax} kappa {kap} N:", [cell(n=v, ckw=ck, **HARD) for v in (2, 3, 5, 10, 20)])

def h7_attempt_2():
    print("\n== H7 attempt 2, REJECTED: supralinear pooling, pool = c*sum(s^p) ==")
    for p, c in ((1.5, 1.0), (1.5, 2.0), (2.0, 1.0), (2.0, 2.0)):
        ck = dict(C, pool_p=p, pool_c=c)
        print(f"  p {p} c {c} N:", [cell(n=v, ckw=ck, **HARD) for v in (2, 3, 5, 10, 20)])
    print("  raising theta on the N-flat settings collapses every N at once:")
    for th in (1.2, 1.35):
        ck = dict(theta=th, k=16.0, pool_p=2.0, pool_c=2.0)
        print(f"    theta {th} N:", [cell(n=v, ckw=ck, **HARD) for v in (2, 5, 20)])

def h7_diagnosis():
    print("\n== Why option count fails: net drive at baseline against the ignition drive x* = 0.537 ==")
    from ph2 import Agent as A2
    for N in (2, 3, 5, 10, 20):
        a = A2(1, n=N, up=UP, noise=0.0, rng=np.random.default_rng(0), **C)
        for _ in range(600): a.step(np.ones((1, N)))
        s = a.memory()[0]; y = a.up.step(np.ones((1, N)))[0]
        net = y[0] - 1.0*(s.sum() - s[0])
        print(f"  N {N:3d}  baseline state {s[0]:.4f}  net drive {net:.4f}  = {net/0.537:.2f} x*")

if __name__ == "__main__":
    gate(); control(); threshold_sweep(); h7_attempt_1(); h7_attempt_2(); h7_diagnosis()
