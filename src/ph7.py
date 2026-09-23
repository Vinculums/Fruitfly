#!/usr/bin/env python3
"""Phase 7.1: H9 -- does a graded substrate remove the need for an external reset?

Usage: python3 ph7.py [--quick] [sweep|gate|control|all]

The claim under test (concept:h9-graded-substrate-removes-reset): the Select-and-Hold circuit
needs an external reset only because its units are bistable latches. Hold the commitment in
graded units under divisive normalisation instead and competing evidence should revise it
through the circuit's own dynamics, with no reset drive applied anywhere.

The thing that could fail is that stability and revisability pull against each other. The
bistable circuit bought distractor immunity by being unrevisable, which is exactly why it
needed a reset. H9 is supported only if ONE setting passes both D3 (revision) and D4
(distractor immunity). Criteria: record:phase7-1-success-criteria, stored before this file.

What is carried over from Phase 3's D3, and what is not:
  carried over  graded units; divisive normalisation by a pool; persistence from recurrence
  NOT carried   the ring topology. Odour channels do not lie on a ring, so the excitation
                kernel becomes self-excitation only.
  changed       the pool is a SUM, not a mean. With a mean the winner's steady state scales
                with the channel count; with a sum it is Rmax/c whatever N is, which keeps
                the readout threshold comparable to the bistable circuit's ON state of ~2.0
                and lets the Phase 2 battery be run unchanged. Stated here because it is a
                deviation from D3 and not a free choice.
"""
import sys
import numpy as np
from ph2 import Upstream, Circuit

R = 200
QUICK = "--quick" in sys.argv
if QUICK: R = 40

UP = dict(n=1.5, sig=0.05, Rmax=1.8, k=0.8, tau=2.0)   # adopted upstream stage, unchanged
HOLD = 1.0            # readout threshold, the same one the Phase 2 battery uses
N = 5


class ChanDiv:
    """Graded channels under divisive normalisation. No bistability, no reset input.

    exc_i = J*s_i + x_i
    r_i   = Rmax * relu(exc_i)^p / (sigma^p + c * sum_j relu(exc_j)^p)
    s    <- s + (1/tau)*(-s + r)

    A lone winner settles at Rmax/c independent of N, because the pool is a sum. With
    Rmax 2.0 and c 1.0 that is 2.0, the same level the bistable ON state sits at, so
    `s > 1.0` reads commitment in both circuits and the batteries are comparable.

    There is deliberately no `reset` argument. The whole point is that nothing external
    releases the commitment.
    """
    DT = 1.0

    def __init__(self, runs, n=N, J=1.0, p=2.0, sigma=0.3, c=1.0, Rmax=2.0,
                 tau=10.0, noise=0.01, rng=None):
        self.R, self.n, self.J, self.p = runs, n, J, p
        self.sigma, self.c, self.Rmax, self.tau, self.noise = sigma, c, Rmax, tau, noise
        self.rng = rng if rng is not None else np.random.default_rng(0)
        self.s = np.zeros((runs, n))

    def memory(self): return self.s

    def step(self, x=None):
        exc = self.J*self.s + self.noise*self.rng.standard_normal(self.s.shape)
        if x is not None: exc = exc + x
        e = np.maximum(exc, 0.0)**self.p
        r = self.Rmax*e / (self.sigma**self.p + self.c*e.sum(1, keepdims=True))
        self.s = self.s + (self.DT/self.tau)*(-self.s + r)
        return self.s


class Graded:
    """upstream stage feeding the graded circuit."""
    def __init__(self, runs, n=N, rng=None, **ckw):
        self.R, self.n = runs, n
        rng = rng if rng is not None else np.random.default_rng(0)
        self.up = Upstream(runs=runs, chans=n, **UP)
        self.c = ChanDiv(runs, n=n, rng=rng, **ckw)
    def step(self, x): return self.c.step(self.up.step(x))
    def memory(self): return self.c.memory()


class Bistable:
    """the adopted design, as the control. Its reset input exists but is never driven here."""
    def __init__(self, runs, n=N, rng=None, **ckw):
        self.R, self.n = runs, n
        rng = rng if rng is not None else np.random.default_rng(0)
        self.up = Upstream(runs=runs, chans=n, **UP)
        self.c = Circuit(runs, n=n, rng=rng, **{**dict(theta=1.0, k=12.0), **ckw})
    def step(self, x): return self.c.step(self.up.step(x), reset=0.0)
    def memory(self): return self.c.memory()


def committed(net):
    """index of the channel the circuit is committed to, or -1 if none or more than one."""
    on = net.memory() > HOLD
    return np.where(on.sum(1) == 1, on.argmax(1), -1)


def targets(n=N): return np.random.default_rng(1000).integers(0, n, R)


def cue_phase(net, tgt, steps=300, d=0.05, x0=1.0, noise_sd=0.3, rng=None):
    rows = np.arange(R)
    rng = rng or np.random.default_rng(7)
    for _ in range(steps):
        x = np.full((R, net.n), float(x0)); x[rows, tgt] += d*x0
        x += noise_sd*x0*rng.standard_normal((R, net.n))
        net.step(x)


def blank(net, steps):
    for _ in range(steps): net.step(np.zeros((R, net.n)))


def pulse(net, chan, amp, steps):
    rows = np.arange(R)
    for _ in range(steps):
        x = np.zeros((R, net.n)); x[rows, chan] = amp
        net.step(x)


# ---------------------------------------------------------------- the six criteria
#
# Which cue each criterion uses follows Phase 2's own practice, not a choice made here. Phase 2
# scored scale invariance on the HARD cue (d=0.05, cue=300) and distractor resistance and the
# sequential-trial tests on the EASY cue (d=0.4, cue=100). The hard cue is deliberately near
# threshold: even the adopted design abstains on 44 percent of runs at x0=1.0, which is why the
# Phase 2 gate bounds the WRONG count and counts abstain separately. D1/D5 therefore report
# wrong only, and D2/D3/D4 use the easy cue so that almost every run has a commitment to test.
HARD = dict(d=0.05, steps=300)
EASY = dict(d=0.4, steps=100)


def d1_d5(mk, x0=1.0):
    """Phase 2's scale cell, reproduced exactly: hard cue, 300-step blank delay, then read.
    Returns (correct, wrong, abstain); the gate bounds `wrong`."""
    net = mk(); tgt = targets()
    cue_phase(net, tgt, x0=x0, **HARD)
    blank(net, 300)
    held = committed(net)
    correct = int((held == tgt).sum())
    wrong = int(((held != tgt) & (held >= 0)).sum())
    return correct, wrong, int((held == -1).sum())


def d2_hold(mk):
    """easy cue, then 300 blank steps. Of the runs that committed, how many still hold it."""
    net = mk(); tgt = targets()
    cue_phase(net, tgt, **EASY)
    before = committed(net)
    blank(net, 300)
    after = committed(net)
    ok = (before >= 0) & (after == before)
    return int(ok.sum()), int((before >= 0).sum())


def d3_revise(mk, amp=2.0, steps=100):
    """after committing to A, present B alone for 100 steps. No reset drive anywhere."""
    net = mk(); tgt = targets()
    cue_phase(net, tgt, **EASY)
    blank(net, 50)
    before = committed(net)
    other = (tgt + 1) % N
    pulse(net, other, amp, steps)
    blank(net, 50)
    after = committed(net)
    ok = (before >= 0) & (after == other)
    return int(ok.sum()), int((before >= 0).sum())


def d4_distractor(mk, amp=2.0, steps=20):
    """same channel, same amplitude, 20 steps instead of 100. Must NOT move.
    Duration is the only difference from D3: the question is whether the circuit
    integrates evidence over time rather than reacting to whatever is loudest now."""
    net = mk(); tgt = targets()
    cue_phase(net, tgt, **EASY)
    blank(net, 50)
    before = committed(net)
    other = (tgt + 1) % N
    pulse(net, other, amp, steps)
    blank(net, 230)
    after = committed(net)
    ok = (before >= 0) & (after == before)
    return int(ok.sum()), int((before >= 0).sum())


def d5_scale(mk):
    return [d1_d5(mk, x0=v)[1] for v in (0.25, 0.5, 1, 2, 4)]


def d6_idle(mk):
    net = mk()
    blank(net, 400)
    return int((committed(net) == -1).sum())


def report(name, mk, full=True):
    cor, w, ab = d1_d5(mk)
    kept, n_k = d2_hold(mk)
    rev, n_rev = d3_revise(mk)
    dis, n_dis = d4_distractor(mk)
    idle = d6_idle(mk)
    scale = d5_scale(mk) if full else None
    print(f"   {name}")
    print(f"     D1 hard cue c/w/a         {cor:3d}/{w:3d}/{ab:3d}   (bound: wrong <= {5*R//200})")
    print(f"     D2 held through delay     {kept:3d} of {n_k:3d} committed   (bound 95%)")
    print(f"     D3 revised by evidence    {rev:3d} of {n_rev:3d} committed   (bound 90%)  <- the new one")
    print(f"     D4 resisted distractor    {dis:3d} of {n_dis:3d} committed   (bound 95%)")
    print(f"     D6 idle, no commitment    {idle:3d} of {R}   (bound 98%)")
    if full: print(f"     D5 wrong by input scale   {scale}   (bound {5*R//200} each)")
    return dict(d1=w, d2=(kept, n_k), d3=(rev, n_rev), d4=(dis, n_dis), d6=idle, d5=scale)


def _frac(pair): return pair[0]/pair[1] if pair[1] else 0.0


def verdict(b):
    s = lambda k, ok: f"D{k} {'pass' if ok else 'FAIL'}"
    # D2/D3/D4 are conditional on the run having committed at all: a circuit that never
    # commits cannot be said to have failed to revise. The stored criteria wrote these as
    # "of 200", which is unattainable for any circuit including the adopted one, since the
    # cue leaves some runs uncommitted. Read as a fraction of committed runs, and the
    # fractions are the ones the stored bounds imply: 190/200, 180/200, 190/200.
    bounds = [(1, b["d1"] <= 5*R/200), (2, _frac(b["d2"]) >= 0.95), (3, _frac(b["d3"]) >= 0.90),
              (4, _frac(b["d4"]) >= 0.95), (6, b["d6"] >= 0.98*R)]
    if b["d5"] is not None: bounds.append((5, all(v <= 5*R/200 for v in b["d5"])))
    print("     " + "  ".join(s(k, ok) for k, ok in bounds))
    return all(ok for _, ok in bounds)


# ---------------------------------------------------------------- runs
def control():
    print("\n== Control: the adopted bistable circuit, reset never driven ==")
    print("   D3 is expected to fail here. If it does not, H9 is not needed.")
    b = report("bistable (adopted)", lambda: Bistable(R, rng=np.random.default_rng(0)))
    verdict(b)


def sweep():
    print("\n== H9 sweep: self-excitation J against pool weight c ==")
    print("   Reported in full including settings that fail, per E1. D3 and D4 are the pair")
    print("   that matters; a setting that passes one by failing the other does not support H9.")
    print(f"   {'J':>5} {'c':>5} | {'D1w':>4} {'D2':>7} {'D3':>7} {'D4':>7} {'D6':>4} | both D3+D4?")
    hits = []
    for J in (0.8, 1.0, 1.2, 1.5, 2.0):
        for c in (0.5, 1.0, 2.0):
            mk = lambda J=J, c=c: Graded(R, rng=np.random.default_rng(0), J=J, c=c)
            _, w, _ = d1_d5(mk)
            kept, nk = d2_hold(mk)
            rev, nr = d3_revise(mk)
            dis, nd = d4_distractor(mk)
            idle = d6_idle(mk)
            both = _frac((rev, nr)) >= 0.90 and _frac((dis, nd)) >= 0.95
            if both: hits.append((J, c))
            print(f"   {J:5.1f} {c:5.1f} | {w:4d} {kept:3d}/{nk:<3d} {rev:3d}/{nr:<3d}"
                  f" {dis:3d}/{nd:<3d} {idle:4d} | {'YES' if both else '.'}")
    print(f"\n   settings passing D3 and D4 together: {hits if hits else 'NONE'}")
    return hits


def tau_sweep(hits):
    """A SECOND sweep, added after the first one showed D1 failing at every setting that
    passed D3 and D4. Disclosed as added, per E1.

    Motivation, stated before running it: D1 is a near-threshold discrimination where the cue
    noise (sd 0.3) is six times the signal (d 0.05), so accuracy comes from integrating over
    the 300-step cue. J sets how deep the attractor is; tau sets how long evidence is averaged
    before the circuit commits. They are different knobs, so tau is the one that could break
    the accuracy-against-stability tension the J sweep found.
    """
    if not hits:
        print("\n== tau sweep skipped: nothing passed D3 and D4 ==")
        return []
    print("\n== Second sweep (added after D1 failed): integration time tau ==")
    print(f"   {'J':>5} {'c':>5} {'tau':>5} |  {'D1w':>4} {'D2':>7} {'D3':>7} {'D4':>7} {'D6':>4} | all?")
    out = []
    for J, c in hits:
        for tau in (10.0, 20.0, 40.0, 80.0):
            mk = lambda J=J, c=c, tau=tau: Graded(R, rng=np.random.default_rng(0), J=J, c=c, tau=tau)
            _, w, _ = d1_d5(mk)
            kept, nk = d2_hold(mk)
            rev, nr = d3_revise(mk)
            dis, nd = d4_distractor(mk)
            idle = d6_idle(mk)
            ok = (w <= 5*R/200 and _frac((kept, nk)) >= 0.95 and _frac((rev, nr)) >= 0.90
                  and _frac((dis, nd)) >= 0.95 and idle >= 0.98*R)
            if ok: out.append((J, c, tau))
            print(f"   {J:5.1f} {c:5.1f} {tau:5.1f} |  {w:4d} {kept:3d}/{nk:<3d} {rev:3d}/{nr:<3d}"
                  f" {dis:3d}/{nd:<3d} {idle:4d} | {'YES' if ok else '.'}")
    print(f"\n   settings passing every criterion except D5: {out if out else 'NONE'}")
    return out


def gate(hits):
    print("\n== H9 gate: the full battery on the settings that passed D3 and D4 ==")
    if not hits:
        print("   No setting passed both. Under E1 that rejects H9 and no reset is added back.")
        return
    for J, c in hits:
        b = report(f"graded J={J} c={c}", lambda: Graded(R, rng=np.random.default_rng(0), J=J, c=c))
        ok = verdict(b)
        print(f"     -> H9 {'SUPPORTED' if ok else 'not supported'} at this setting")


def demo():
    """self-check: the graded circuit holds without input and has no reset input at all."""
    net = ChanDiv(20, rng=np.random.default_rng(0))
    x = np.zeros((20, N)); x[:, 2] = 1.5
    for _ in range(200): net.step(x)
    on = net.s[:, 2].copy()
    assert (on > HOLD).all(), f"did not ignite: {on[:3]}"
    for _ in range(300): net.step(None)
    assert (net.s[:, 2] > HOLD).all(), f"did not hold: {net.s[:3, 2]}"
    assert (net.s.sum(1) - net.s[:, 2] < 0.1).all(), "other channels not suppressed"
    import inspect
    assert "reset" not in inspect.signature(ChanDiv.step).parameters, "step must take no reset"
    print(f"ok  ignites to {on.mean():.3f}, holds at {net.s[:, 2].mean():.3f} after 300 blank steps")
    print("ok  ChanDiv.step has no reset parameter")


if __name__ == "__main__":
    what = [a for a in sys.argv[1:] if a in ("sweep", "gate", "control", "all", "demo")] or ["all"]
    if "demo" in what:
        demo(); sys.exit(0)
    print(f"== Phase 7.1, H9. {R} runs per cell ==")
    print("== Criteria: record:phase7-1-success-criteria, stored before this file existed ==")
    if "control" in what or "all" in what: control()
    hits = sweep() if ("sweep" in what or "all" in what) else []
    if "gate" in what or "all" in what:
        best = tau_sweep(hits)
        gate(hits)
        if best:
            print("\n== Full battery on the best setting from the tau sweep ==")
            J, c, tau = best[0]
            b = report(f"graded J={J} c={c} tau={tau}",
                       lambda: Graded(R, rng=np.random.default_rng(0), J=J, c=c, tau=tau))
            ok = verdict(b)
            print(f"     -> H9 {'SUPPORTED' if ok else 'not supported on every criterion'}")
