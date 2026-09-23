#!/usr/bin/env python3
"""Diagnosis of the unrecovered excess in the integrated agent. Measurement only.

Usage: python ph13b.py [demo]

The return rule alone left 0.0-0.5 percent of agents unrecovered late (H16 Run 2, one source).
Inside ph11's agent in the two-source world it left 7-19 percent. Those two runs differ in the
number of sources AND in sensing, selection and heading, so nothing is attributed yet. Here
every arm runs in the SAME two-source world, from the same initial states and seeds, and the
events between a whiff and the navigation rule are logged without touching the agent: act()
returns the selection state h, and hit = (h >= 0) and a whiff on channel h is the agent's own
formula, checked on every step against the agent's cast clock.

Core question (decision:two-source-check-judged): is odour actually met and ignored by
navigation because of the selection state? Plan and readings:
record:unrecovered-excess-diagnosis-plan, stored before this file. Nothing is fixed here.
"""
import sys
import numpy as np
from ph9 import STEPS, W0, SLOPE, LMAX, angdiff
from ph12 import Nav2, med
from ph13 import World4, Agent2, R, BLOCKS

T = BLOCKS*STEPS
SEEDS = [(1620, 1720), (9600, 9700)]
ARMS = [("bare", None), ("no-hold", ("learn", "hold")), ("no-norm", ("learn", "norm")),
        ("exact-heading", ("learn", "head")), ("full", ("learn",)), ("full+known", ())]


def trace(name, abl, seeds, runs=R, steps=T):
    w = World4(runs, np.random.default_rng(seeds[0])); rows = np.arange(runs); kv = None
    if abl is None:
        a = Nav2(runs, np.random.default_rng(seeds[1]), "return", "exact")
    else:
        if name == "full+known":
            kv = np.full((runs, 2), -1.0); kv[rows, w.good] = 1.0
        a = Agent2(runs, np.random.default_rng(seeds[1]), abl=abl, known=kv)
    b = lambda: np.zeros((steps, runs), bool)
    tr = dict(W=np.zeros((steps, runs, 2), bool), H=np.full((steps, runs), -1, np.int8),
              HP=np.full((steps, runs), -1, np.int8), HIT=b(), C=b(), E=b(), F=b(), INC=b(), AT=b())
    hp = np.full(runs, -1)
    for t in range(steps):
        whiffs = w.sense()
        inc = np.zeros(runs, bool)
        for k in (0, 1):
            da = w.pos[:, 0] - w.src[:, k, 0]; dc = np.abs(w.pos[:, 1] - w.src[:, k, 1])
            inc |= ((da > 0) & (da < LMAX) & (dc < W0 + SLOPE*da)) | (np.hypot(da, dc) < 3.0)
        if abl is None:
            hit = whiffs.any(1); turn = a.act(w, hit, w.wind_on()); h = np.full(runs, -1)
        else:
            turn, h = a.act(w, whiffs, w.wind_on())
            hit = np.where(h >= 0, whiffs[rows, np.maximum(h, 0)], False)
            assert ((a.since == 0) == hit).all(), "reconstructed hit disagrees with the agent's cast clock"
            tr["E"][t] = np.abs(angdiff(a.est, w.head)) > 45.0
            if kv is not None: tr["F"][t] = (h >= 0) & (kv[rows, np.maximum(h, 0)] < 0)
        w.move(turn); a.bump(w.bumped)
        tr["W"][t] = whiffs; tr["H"][t] = h; tr["HP"][t] = hp; tr["HIT"][t] = hit
        tr["C"][t] = w.bumped; tr["INC"][t] = inc; tr["AT"][t] = w.at_source().any(1)
        hp = h
    tr["end_d"] = np.linalg.norm(w.pos[:, None, :] - w.src, axis=2).min(1)
    return tr


def last_true(x):
    """step of the last True in each column of a (T, R) bool array, -1 if none"""
    return np.where(x.any(0), x.shape[0] - 1 - x[::-1].argmax(0), -1)


def summarise(name, tr):
    W, H, HP, HIT = tr["W"], tr["H"], tr["HP"], tr["HIT"]
    anyw = W.any(2); n = anyw.shape[1]; steps = anyw.shape[0]
    unrec = ~anyw[-3*STEPS:].any(0)
    dwell = tr["AT"][-3*STEPS:].sum(0)/3.0
    ign = anyw & ~HIT; none_held = ign & (H == -1); other = ign & (H >= 0)
    tot = max(int(anyw.sum()), 1)
    # re-encounters: a whiff after at least 40 whiff-free steps
    cs = np.cumsum(anyw, 0); quiet = np.zeros_like(anyw)
    quiet[41:] = (cs[40:-1] - cs[:-41]) == 0
    re = anyw & quiet
    ch = np.cumsum(HIT, 0); soon = np.zeros_like(anyw)
    soon[:-30] = (ch[30:] - ch[:-30] + HIT[:-30]) > 0
    print(f"\n   {name:14s} late unrecovered {unrec.mean()*100:5.1f}% ({int(unrec.sum())}/{n})"
          f"   last-third dwell median {med(dwell):5.1f}   whiffs per agent median {med(anyw.sum(0)):6.0f}"
          f"   heading error > 45 deg {tr['E'].mean()*100:5.2f}%   contacts/agent {tr['C'].sum(0).mean():5.1f}")
    print(f"      whiffs NOT handed to navigation: {ign.sum()/tot*100:5.1f}% of all whiffs"
          f"  (nothing held {none_held.sum()/tot*100:5.1f}%, the other odour held {other.sum()/tot*100:5.1f}%)")
    print(f"      re-encounters (whiff after >= 40 quiet steps): {int(re.sum()):6d};  a hit on that step"
          f" {HIT[re].mean()*100 if re.any() else float('nan'):5.1f}%;  a hit within 30 steps {soon[re].mean()*100 if re.any() else float('nan'):5.1f}%;"
          f"  nothing held just before {(HP[re] == -1).mean()*100 if re.any() else float('nan'):5.1f}%")
    lh, lw = last_true(HIT), last_true(anyw)
    after = np.arange(steps)[:, None] > lh[None, :]
    w_after = (anyw & after).sum(0); inc_after = (tr["INC"] & after).sum(0); c_after = (tr["C"] & after).sum(0)
    for label, m in (("late unrecovered", unrec), ("the rest", ~unrec)):
        if not m.any(): continue
        print(f"      {label:16s} n {int(m.sum()):3d}: last hit at step {med(lh[m]):6.0f}, last whiff at {med(lw[m]):6.0f};"
              f"  whiffs received after the last hit: median {med(w_after[m]):4.0f}, agents with any {float((w_after[m] > 0).mean())*100:5.1f}%;"
              f"  steps inside a cone after it {med(inc_after[m]):5.0f};  contacts after it {med(c_after[m]):4.0f};"
              f"  distance to nearest source at the end {med(tr['end_d'][m]):6.1f}")
    return dict(unrec=float(unrec.mean()), ignored=float(ign.sum()/tot), tr=tr, unrec_mask=unrec, lh=lh)


def timelines(tr, mask, lh, k=4):
    """the order of events from the last hit onward, for a few late-unrecovered agents"""
    W, H = tr["W"], tr["H"]; anyw = W.any(2); steps = anyw.shape[0]
    for r in np.flatnonzero(mask)[:k]:
        t0 = int(lh[r]); ev = []
        rel = np.flatnonzero(H[t0 + 1:, r] == -1)
        if t0 >= 0 and len(rel): ev.append(f"hold released at +{int(rel[0]) + 1}")
        for t in np.flatnonzero(anyw[t0 + 1:, r])[:6] + t0 + 1:
            ev.append(f"whiff at +{t - t0} (h {int(H[t, r])}, odour {'AB'[int(W[t, r].argmax())]})")
        c = np.flatnonzero(tr["C"][t0 + 1:, r])
        if len(c): ev.append(f"first wall contact at +{int(c[0]) + 1} ({len(c)} in all)")
        print(f"      agent {r:3d}: last hit at step {t0}; " + "; ".join(ev) + f"; then nothing to step {steps - 1}")


def releases(tr):
    """every loss of the hold, over all agents: when it happens, what precedes it, what follows"""
    W, H, HP, HIT = tr["W"], tr["H"], tr["HP"], tr["HIT"]; steps, n = H.shape
    since_hit, other10, recommit, whiffs_between, never = [], [], [], [], 0
    for r in range(n):
        hits = np.flatnonzero(HIT[:, r])
        for t in np.flatnonzero((HP[:, r] >= 0) & (H[:, r] == -1)):
            prev = hits[hits < t]
            since_hit.append(t - prev[-1] if len(prev) else t)
            other10.append(bool(W[max(0, t - 10):t + 1, r, 1 - HP[t, r]].any()))
            nxt = np.flatnonzero(H[t:, r] >= 0)
            if len(nxt):
                recommit.append(int(nxt[0])); whiffs_between.append(int(W[t:t + nxt[0], r].any(1).sum()))
            else:
                never += 1; whiffs_between.append(int(W[t:, r].any(1).sum()))
    s = np.array(since_hit); k = len(s)
    print(f"      losses of the hold: {k} over {n} agents.  steps since the last hit: median {med(s):5.0f},"
          f" within 41-50 (the silence timeout) {float(((s >= 41) & (s <= 50)).mean())*100:5.1f}%,"
          f" over 100 {float((s > 100).mean())*100:5.1f}%;"
          f"  a whiff of the OTHER odour in the 10 steps before {np.mean(other10)*100:5.1f}%")
    print(f"      after a loss: never holds again {never/k*100:5.1f}%;  otherwise holds again after median"
          f" {med(recommit) if recommit else float('nan'):5.0f} steps;  whiffs received while nothing is held:"
          f" median {med(whiffs_between):4.0f}, 90th percentile {np.percentile(whiffs_between, 90):4.0f}")


def report():
    print(f"== unrecovered excess, same two-source world for every arm. {R} agents, {T} steps, neutral valence unless noted ==")
    for seeds in SEEDS:
        print(f"\n== world seed {seeds[0]}, agent seed {seeds[1]} ==")
        out = {}
        for name, abl in ARMS:
            out[name] = summarise(name, trace(name, abl, seeds))
            if name != "full": out[name].pop("tr")
        f = out["full"]
        print("\n   `full`, every loss of the hold:")
        releases(f["tr"])
        print("\n   order of events after the last hit, first late-unrecovered agents of `full`:")
        timelines(f["tr"], f["unrec_mask"], f["lh"])
        print("\n   ladder, late unrecovered: " + "  ".join(f"{k} {v['unrec']*100:.1f}%" for k, v in out.items()))


def demo():
    tr = trace("full", ("learn",), (1, 2), runs=30, steps=300)      # the per-step assertion runs inside
    x = np.zeros((5, 3), bool); x[1, 0] = x[3, 0] = x[4, 2] = True
    assert list(last_true(x)) == [3, -1, 4]
    assert tr["W"].shape == (300, 30, 2) and (tr["HIT"] <= tr["W"].any(2)).all(), "a hit without a whiff"
    print("ok  reconstructed hit agrees with the agent's cast clock on every step; a hit always has a whiff")


if __name__ == "__main__":
    if "demo" in sys.argv[1:]: demo(); sys.exit(0)
    report()
