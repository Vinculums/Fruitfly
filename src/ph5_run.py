#!/usr/bin/env python3
"""Phase 5 run: integrated agent and module ablations. Usage: python3 ph5_run.py"""
import numpy as np
from ph5 import World, Agent, episode

R, EPISODES = 200, 9
ABL = [("intact", ()), ("no normalisation", ("norm",)), ("no select-and-hold", ("hold",)),
       ("no heading memory", ("head",)), ("no learned valence", ("learn",)), ("all off", ("all",))]

def run(abl, p_odour, reset=True, seed_w=0, seed_a=1):
    w = World(R, np.random.default_rng(seed_w), p_odour=p_odour)
    a = Agent(R, np.random.default_rng(seed_a), abl=abl, reset=reset)
    return np.array([episode(w, a) for _ in range(EPISODES)])      # (EPISODES, R)

def table(p_odour, label):
    print(f"\n== {label} (odour present on {p_odour*100:.0f}% of steps), {R} agents,"
          f" {EPISODES} episodes of 400 steps ==")
    res = {}
    for name, abl in ABL:
        s = run(abl, p_odour); res[name] = s
        last = s[-3:].ravel(); first = s[:3].ravel()
        print(f"  {name:20s} median score {np.median(last):8.1f}"
              f"   first third {np.median(first):7.1f} -> last third {np.median(last):7.1f}")
    base = res["intact"][-3:].mean(0)
    print("  matched-pair comparison against the intact agent (same worlds, same seeds):")
    for name, _ in ABL[1:]:
        other = res[name][-3:].mean(0)
        win = float((base > other).mean())
        mi, mo = float(np.median(base)), float(np.median(other))
        gap = (mi - mo)/abs(mi) if mi else float("nan")
        verdict = "intact better" if (gap >= 0.25 and win >= 0.60) else (
                  "ablation better" if mo > mi else "no clear difference")
        print(f"    vs {name:20s} intact wins {win*100:5.1f}% of pairs,"
              f" median gap {gap*100:+7.1f}% of intact  -> {verdict}")
    return res

def valences():
    w = World(R, np.random.default_rng(0), p_odour=1.0)
    a = Agent(R, np.random.default_rng(1))
    print("\n== What the intact agent learns ==")
    for ep in range(EPISODES):
        sc = episode(w, a)
        v0 = a.mb.valence(a.codes[:, 0]); v1 = a.mb.valence(a.codes[:, 1])
        vg = np.where(w.good == 0, v0, v1); vb = np.where(w.good == 0, v1, v0)
        if ep in (0, 2, 5, 8):
            print(f"   episode {ep}: score {np.median(sc):6.1f}"
                  f"   valence of the rewarding odour {np.median(vg):+.3f},"
                  f" of the punishing odour {np.median(vb):+.3f}")

def reset_effect():
    print("\n== The reset signal, which no phase found a biological anchor for ==")
    for rs in (True, False):
        s = run((), 1.0, reset=rs)[-3:].ravel()
        t = run(("learn",), 1.0, reset=rs)[-3:].ravel()
        print(f"   reset {'on ' if rs else 'off'}: intact {np.median(s):7.1f},"
              f" no-learned-valence {np.median(t):7.1f}")

def gradient_source():
    print("\n== Where the steering gradient is read from ==")
    for gon, lab in ((False, "raw channel of the selected odour"), (True, "normalised channel")):
        w = World(R, np.random.default_rng(0), p_odour=1.0)
        a = Agent(R, np.random.default_rng(1), grad_on_norm=gon)
        s = np.array([episode(w, a) for _ in range(EPISODES)])[-3:].ravel()
        print(f"   {lab:35s} median score {np.median(s):7.1f}")

if __name__ == "__main__":
    a = table(1.0, "Continuous odour")
    b = table(0.3, "Intermittent odour")
    print("\n== A4, is the heading module specific to intermittency? ==")
    for cond, res, p in (("continuous", a, 1.0), ("intermittent", b, 0.3)):
        i = float(np.median(res["intact"][-3:])); h = float(np.median(res["no heading memory"][-3:]))
        print(f"   {cond:13s}: intact {i:7.1f}, no heading memory {h:7.1f}, deficit {i-h:+7.1f}")
    valences(); reset_effect(); gradient_source()
