#!/usr/bin/env python3
"""Phase 5 Run 2: integrated agent, re-run against the stored gate after fixing the three
defects the Run 1 report named. Usage: python3 ph5b_run.py [--quick]

Order matters and is fixed by criteria B1 and B5: the task is calibrated against the all-off
control FIRST and frozen, and only then is the ablation table produced. Nothing below reads
the intact agent's score before the calibration is fixed.
"""
import sys
import numpy as np
from ph5 import World, episode
from ph5b import Agent2, learned

R, EPISODES = 200, 9
QUICK = "--quick" in sys.argv
if QUICK: R, EPISODES = 40, 3

ABL = [("intact", ()), ("no normalisation", ("norm",)), ("no select-and-hold", ("hold",)),
       ("no heading memory", ("head",)), ("no learned valence", ("learn",)), ("all off", ("all",))]
CAND_STEPS = (400, 800, 1600, 3200)
B1_MIN = 10.0        # a condition is only readable if some arm reaches this median |score|


def run(abl, p_odour, steps, seed_w=0, seed_a=1, **akw):
    w = World(R, np.random.default_rng(seed_w), p_odour=p_odour)
    a = Agent2(R, np.random.default_rng(seed_a), abl=abl, **akw)
    s = np.array([episode(w, a, steps=steps) for _ in range(EPISODES)])   # (EPISODES, R)
    return s, w, a


def last(s): return s[-3:].ravel() if EPISODES >= 3 else s.ravel()


# ---------------------------------------------------------------- B1: calibrate, then freeze
def calibrate(p_odour, label):
    """Episode length chosen against the ALL-OFF GRADIENT CLIMBER only (criteria B1).

    The probe is all modules off AND neutral_start off, i.e. the always-approach agent of
    Run 1. It has to be that one and not Run 2's all-off agent: under the neutral rule half
    the population descends the gradient, so its median is ~0 by construction and would say
    the task is at the floor when it is not. The probe is a fixed yardstick for the world,
    deliberately independent of the action rule being tested.
    """
    print(f"\n== B1 task calibration, {label} (odour on {p_odour*100:.0f}% of steps) ==")
    print("   probe: all modules off, always-approach (the Run 1 gradient climber).")
    print("   the intact agent is not run here.")
    chosen = None
    for steps in CAND_STEPS:
        s, _, _ = run(("all",), p_odour, steps, neutral_start=False)
        med = float(np.median(last(s)))
        ok = abs(med) >= B1_MIN
        print(f"   {steps:5d} steps: all-off median score {med:8.1f}"
              f"   {'discriminates' if ok else 'at the floor'}")
        if ok and chosen is None:
            chosen = steps
            break
    if chosen is None:
        print(f"   NO episode length up to {CAND_STEPS[-1]} makes this condition discriminate.")
        print("   Under B1 this condition is reported as uninformative and no verdict is read from it.")
    else:
        print(f"   FROZEN: {chosen} steps.")
    return chosen


# ---------------------------------------------------------------- the gate table (A1)
def table(p_odour, steps, label):
    print(f"\n== {label} (odour on {p_odour*100:.0f}% of steps), {R} agents,"
          f" {EPISODES} episodes of {steps} steps ==")
    res = {}
    for name, abl in ABL:
        s, w, a = run(abl, p_odour, steps); res[name] = s
        print(f"  {name:20s} median score {np.median(last(s)):8.1f}"
              f"   first third {np.median(s[:3].ravel()):7.1f} -> last third {np.median(last(s)):7.1f}")
    base = res["intact"][-3:].mean(0)
    print("  matched-pair comparison against the intact agent (same worlds, same seeds):")
    passed = 0
    for name, _ in ABL[1:-1]:                       # the four single-module ablations
        other = res[name][-3:].mean(0)
        win = float((base > other).mean())
        mi, mo = float(np.median(base)), float(np.median(other))
        gap = (mi - mo)/abs(mi) if mi else float("nan")
        ok = gap >= 0.25 and win >= 0.60
        passed += ok
        verdict = "intact better" if ok else ("ablation better" if mo > mi else "no clear difference")
        print(f"    vs {name:20s} intact wins {win*100:5.1f}% of pairs,"
              f" median gap {gap*100:+8.1f}% of intact  -> {verdict}")
    print(f"  A1: intact beats {passed} of 4 single-module ablations"
          f"  -> {'GATE MET' if passed == 4 else 'gate NOT met'}")
    ceil = float(steps)                    # +1 per step at the rewarding source
    at_ceiling = [n for n, _ in ABL if float(np.median(last(res[n]))) >= 0.99*ceil]
    if len(at_ceiling) > 1:
        print(f"  CEILING: {len(at_ceiling)} arms are at the task ceiling of {ceil:.0f}"
              f" ({', '.join(at_ceiling)}).")
        print("  A1 asks the intact agent to EXCEED each ablation by 25 percent. Two arms that")
        print("  both sit on the ceiling cannot differ, so for those pairs the gate is not")
        print("  failed on the architecture, it is unreadable on the task. B1 checked that this")
        print("  condition can discriminate; it did not check that it cannot saturate. Recorded")
        print("  as a task-design limit and NOT worked around, per B5.")
    return res


# ---------------------------------------------------------------- B2: is the learning two-sided
def b2_learning(steps):
    print("\n== B2 learning symmetry: does the rewarding odour get learned now? ==")
    rules = [("Run 1 rule: approach by default", dict(neutral_start=False)),
             ("neutral, frozen sign per agent", dict(neutral_start=True, neutral_mode="frozen")),
             ("neutral, bout timer (Run 2)", dict(neutral_start=True, neutral_mode="flip"))]
    for tag, kw in rules:
        w = World(R, np.random.default_rng(0), p_odour=1.0)
        a = Agent2(R, np.random.default_rng(1), **kw)
        for _ in range(EPISODES):
            sc = episode(w, a, steps=steps)
        good, bad = learned(a, w)
        v0 = a.mb.valence(a.codes[:, 0]); v1 = a.mb.valence(a.codes[:, 1])
        vg = np.where(w.good == 0, v0, v1)
        touched = float((np.abs(vg) > 1e-9).mean())*100
        print(f"   {tag:34s} rewarding {good:+.3f}  punishing {bad:+.3f}"
              f"  score {np.median(sc):7.1f}  reinforced-by-reward {touched:5.1f}%"
              f"  -> B2 {'met' if abs(good) >= 0.05 else 'NOT met'}")
    print("   Note the shape of this: nearly every agent IS reinforced by the rewarding odour,")
    print("   yet the median learned valence stays at zero. The action rule is not the cause;")
    print("   the next block isolates what is.")


def b2_erasure():
    """Why the rewarding odour's valence will not hold: the Phase 4 extinction feedback.

    Run in isolation on the mushroom-body module, with no agent and no world, so the
    mechanism is separated from anything about the task.
    """
    from ph4 import MB
    print("\n== Why B2 fails: sustained pairing erases what it just taught (module in isolation) ==")
    print("   The Phase 4 rule carries an opponent feedback (beta 0.15, the MBON-to-DAN loop)")
    print("   that pulls an active memory back toward balance. Pairing in bursts and then")
    print("   leaving the odour is the case Phase 4 tested. Sitting inside the odour is not.")
    for label, comp in (("reward (compartment 1)", 1), ("punishment (compartment 0)", 0)):
        m = MB(50, K=200, C=2, sparsity=0.05, eta_d=0.10, eta_p=0.30, beta=0.15,
               rng=np.random.default_rng(0))
        code = m.odour(101)
        rv = np.zeros((50, 2)); rv[:, comp] = 1.0
        traj = []
        for t in range(1, 401):
            m.step(code=code, reinf=rv)          # code and reinforcement together, every step
            if t in (5, 10, 25, 50, 100, 200, 400): traj.append((t, float(np.median(m.valence(code)))))
        print(f"   {label:26s} " + "  ".join(f"t={t}:{v:+.3f}" for t, v in traj))
    print("   The valence rises, then is ground back to zero as the feedback depresses the")
    print("   opposing compartment too. A memory survives only for a stimulus the agent LEAVES.")
    print("   In Run 1 the punishing odour was left (so -0.296 stuck) and in Run 2 the rewarding")
    print("   odour is sat on (so it does not). That is a property of the Phase 4 rule meeting a")
    print("   behaving agent, not of the Phase 5 action rule.")


# ---------------------------------------------------------------- B3: circuit, reset, or readout
def b3_diagnosis(steps):
    print("\n== B3 Select-and-Hold diagnosis, continuous odour ==")
    print("   (i) no hold at all, (ii) hold with the Run 1 silence timeout, (iii) hold with an")
    print("   evidence reset that releases the commitment when the other channel leads by 0.2.")
    variants = [("(i)   no hold", dict(abl=("hold",))),
                ("(ii)  timeout reset only", dict(evidence_reset=False)),
                ("(iii) evidence reset", dict(evidence_reset=True, margin=0.2))]
    med = {}
    for name, kw in variants:
        abl = kw.pop("abl", ())
        s, _, _ = run(abl, 1.0, steps, **kw)
        med[name] = float(np.median(last(s)))
        print(f"   {name:28s} median score {med[name]:8.1f}")
    i, iii = med["(i)   no hold"], med["(iii) evidence reset"]
    if i <= 0:
        print(f"   (i) is at {i:.1f}, so the B3 ratio is undefined and NOTHING is concluded from")
        print("   it. Reported as undecidable rather than resolved by a division by zero.")
        return
    ratio = iii/i
    print(f"   (iii) reaches {ratio*100:.1f}% of (i).")
    if ratio >= 0.60:
        print("   B3: the fault was the MISSING RESET. With one, the circuit is not the problem.")
    else:
        print("   B3: the fault is NOT only the missing reset. It lies in the circuit itself or in")
        print("   the way the agent reads its output; the reset does not recover the no-hold score.")
    print("\n   margin sensitivity (reported, not gated):")
    for m in (0.05, 0.1, 0.2, 0.4, 0.8):
        s, _, _ = run((), 1.0, steps, evidence_reset=True, margin=m)
        print(f"      margin {m:4.2f}: median score {np.median(last(s)):8.1f}")


if __name__ == "__main__":
    print("== Phase 5 Run 2. Criteria: record:phase5-run2-success-criteria, stored before this run ==")
    steps_c = calibrate(1.0, "continuous")
    steps_i = calibrate(0.3, "intermittent")

    if steps_c: table(1.0, steps_c, "Continuous odour")
    if steps_i: table(0.3, steps_i, "Intermittent odour")
    else: print("\n== Intermittent odour: UNINFORMATIVE under B1, not read (same as Run 1) ==")

    if steps_c:
        b2_learning(steps_c)
        b2_erasure()
        b3_diagnosis(steps_c)
        print("\n== A4, is the heading module specific to intermittency? ==")
        if steps_i:
            print("   evaluated from the two tables above")
        else:
            print("   cannot be evaluated: the intermittent condition does not discriminate.")
