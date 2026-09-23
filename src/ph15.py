#!/usr/bin/env python3
"""H15 Run 2: does a learned negative valence lead to avoidance, with long-horizon search kept?

Usage: python ph15.py demo | dev | eval

Implements the FINAL specification v4 and nothing else:
  vinc doc dc860b9c7c6f3aa6e, content hash
  7f23e6e5965b8ea911711f8332f5fcb6c8a7a2adcc87c0cd2118b7cc90ae854d
stored before this file existed (record:h15-run2-spec-v4-final, decision:h15-run2-open).
Section numbers in comments are that document's. `demo` runs self-checks 1-7, none of which looks
at a task score. `dev` uses development seeds to find operation errors; `eval` is run once.
An implementation error (code not doing what the text says) and a change to a criterion are
different things and are recorded separately.
"""
import sys
import numpy as np
from ph2 import Upstream
from ph8 import MB4
from ph9 import STEPS
from ph11 import MB
from ph14 import World5, Agent3

SPEC = "v4 doc dc860b9c7c6f3aa6e hash 7f23e6e5965b8ea911711f8332f5fcb6c8a7a2adcc87c0cd2118b7cc90ae854d"
R, BLOCKS, TRAIN, TEST_BLOCKS = 400, 9, 30, 3
Z, QLO, QHI, NBOOT, BOOT_SEED = 2.2414, 1.25, 98.75, 5000, 20260920      # 97.5 percent, both looks (7.0)
SEEDS = dict(dev=((9800, 9900), (9801, 9901)), eval=((1640, 1740), (1641, 1741)))
E1_ARMS = ["random", "oracle", "intact", "no-learning", "known", "ungated", "no-hold",
           "stage-removed", "xchan-removed", "exact-heading"]


class World6(World5):
    """World4 with which source rewards assigned AFTER the draw (section 3): 'balanced' gives
    exactly half the rows a start in the punishing plume, 'all_p' all of them, None keeps the draw."""

    def __init__(self, runs, rng, seed, assign="balanced"):
        super().__init__(runs, rng)
        if assign is None: return
        p = np.ones(runs, bool)
        if assign == "balanced":
            p[:] = False; p[np.random.default_rng(seed + 10_000).permutation(runs)[:runs // 2]] = True
        self.good = np.where(p, 1 - self.start, self.start)


def make_agent(arm, runs, rng, w):
    rows = np.arange(runs); kv, abl = None, ()
    if arm == "known": kv = np.full((runs, 2), -1.0); kv[rows, w.good] = 1.0
    abl = {"no-learning": ("learn",), "no-hold": ("hold",), "stage-removed": ("norm",),
           "exact-heading": ("head",)}.get(arm, ())
    a = Agent3(runs, rng, fix=True, abl=abl, rule=arm if arm in ("random", "oracle") else "agent", known=kv)
    if arm == "xchan-removed": a.up = Upstream(n=1.5, sig=0.05, Rmax=1.8, k=0.0, runs=runs, chans=2)
    if arm == "ungated": a.mb = MB4(runs, parallel=False, gated=False, rng=rng, **MB)
    return a


def inputs(codes, good, at):
    """section 2: one code and one reinforcement vector per row from where the row stands"""
    rows = np.arange(len(good))
    code = np.maximum(codes[:, 0]*at[:, [0]], codes[:, 1]*at[:, [1]])
    rv = np.zeros((len(good), 4))
    for k in (0, 1): rv[rows, np.where(good == k, 1, 0)] += at[:, k]
    return code, rv


def learn_legacy(a, w):
    """Run 1's loop, verbatim in effect: per source, only when someone is there, whole population"""
    hit = w.at_source(); rows = np.arange(a.R)
    for k in (0, 1):
        arrived = hit[:, k]
        if not arrived.any(): continue
        rv = np.zeros((a.R, 4)); rv[rows, np.where(w.good == k, 1, 0)] = arrived*1.0
        a.mb.step(code=a.codes[:, k]*arrived[:, None], reinf=rv)


def valences(mb, codes, good):
    v = np.stack([mb.valence(codes[:, 0]), mb.valence(codes[:, 1])], 1); rows = np.arange(len(good))
    return np.stack([v[rows, good], v[rows, 1 - good]], 1)                  # (R, 2): rewarded, punished


def simulate(w, a, steps, learn, legacy=False, keep_src=False):
    n = a.R; nb = steps // STEPS; rows = np.arange(n)
    o = dict(g=np.zeros((nb, n)), b=np.zeros((nb, n)), first_g=np.full(n, -1), first_b=np.full(n, -1),
             last_g=np.full(n, -1), last_b=np.full(n, -1), plume_late=np.zeros(n, bool), contacts=np.zeros(n),
             nearwall=np.zeros(n), none_held=np.zeros(n), w_none=np.zeros(n), h_none=np.zeros(n),
             w_other=np.zeros(n), h_other=np.zeros(n), visits_g=np.zeros(n), visits_b=np.zeros(n),
             long_g=np.zeros(n), val=np.zeros((nb, n, 2)), calls=0, merged=0,
             good=w.good.copy(), pstart=w.start != w.good, codes=a.codes.copy())
    src = np.full((steps, n), -1, np.int8) if keep_src else None
    pg = np.zeros(n, bool); pb = np.zeros(n, bool); run_g = np.zeros(n)
    for t in range(steps):
        k = t // STEPS
        whiffs = w.sense(); plume = w.plume
        turn, h = a.act(w, whiffs, w.wind_on())
        w.move(turn); a.bump(w.bumped)
        at = w.at_source()
        if learn:
            if legacy: learn_legacy(a, w)
            else:
                code, rv = inputs(a.codes, w.good, at); a.mb.step(code=code, reinf=rv)
            o["calls"] += 1; o["merged"] += int((at.sum(1) == 2).sum())
        g = at[rows, w.good]; b = at[rows, 1 - w.good]
        o["g"][k] += g; o["b"][k] += b
        for key, x in (("g", g), ("b", b)):
            o["first_" + key] = np.where((o["first_" + key] < 0) & x, t, o["first_" + key])
            o["last_" + key] = np.where(x, t, o["last_" + key])
        o["visits_g"] += g & ~pg; o["visits_b"] += b & ~pb; pg, pb = g, b
        run_g = (run_g + 1)*g; o["long_g"] = np.maximum(o["long_g"], run_g)
        if t >= steps - 3*STEPS: o["plume_late"] |= plume
        o["contacts"] += w.bumped
        if t >= steps - 3*STEPS: o["nearwall"] += np.minimum(w.pos, w.arena - w.pos).min(1) < 1.0
        if a.rule == "agent":
            anyw = whiffs.any(1); held = np.where(h >= 0, whiffs[rows, np.maximum(h, 0)], False)
            none = h < 0; other = (h >= 0) & anyw & ~held
            o["none_held"] += none; o["w_none"] += none & anyw; o["h_none"] += none & anyw & a.nav_hit
            o["w_other"] += other; o["h_other"] += other & a.nav_hit
        if keep_src: src[t] = np.where(at[:, 0] & at[:, 1], 2, np.where(at[:, 0], 0, np.where(at[:, 1], 1, -1)))
        if (t + 1) % STEPS == 0 and a.rule == "agent": o["val"][k] = valences(a.mb, a.codes, w.good)
    o["src"] = src; o["steps"] = steps; o["w_end"] = a.mb.w.copy(); o["pos_end"] = w.pos.copy()
    return o


def run_e1(arm, seeds, runs=R, steps=BLOCKS*STEPS, assign="balanced", legacy=False, displace=None, keep_src=False):
    w = World6(runs, np.random.default_rng(seeds[0]), seeds[0], assign)
    a = make_agent(arm, runs, np.random.default_rng(seeds[1]), w)
    if displace is not None: w.pos[displace] = w.src[displace, 1 - w.good[displace]]
    learn = a.rule == "agent" and a.known is None and "learn" not in a.abl
    return simulate(w, a, steps, learn, legacy, keep_src)


def replay(o, gated):
    """7.2: a row's recorded input stream into a fresh module; identical input for both rules"""
    n = len(o["good"]); m = MB4(n, parallel=False, gated=gated, rng=np.random.default_rng(0), **MB)
    for s in o["src"]:
        at = np.stack([(s == 0) | (s == 2), (s == 1) | (s == 2)], 1)
        code, rv = inputs(o["codes"], o["good"], at); m.step(code=code, reinf=rv)
    return valences(m, o["codes"], o["good"])


GAP = 50    # record:h15-run2-dev-log, SPECIFICATION amendment: silent steps between the two trainings


def run_e2(group, seeds, runs=R, learn_on=False, test=True, gap=GAP):
    """section 4. group: 'trained' | 'sham' | 'ungated' (training only).
    gap=0 is the protocol as first registered ('no gap'). With no gap the first odour's code trace and
    the first reinforcement's trace are alive when the second training starts, and pre-test values came
    out bimodal by training order (+-1.9 second-trained, +-0.5 first-trained; the bench gives +-1.0)."""
    w = World6(runs, np.random.default_rng(seeds[0]), seeds[0], "all_p")
    a = make_agent("ungated" if group == "ungated" else "intact", runs, np.random.default_rng(seeds[1]), w)
    rows = np.arange(runs); rf = np.zeros(runs, bool)
    rf[np.random.default_rng(seeds[0] + 20_000).permutation(runs)[:runs // 2]] = True      # reward first
    calls = 0
    for phase in (0, 1):
        at_good = rf if phase == 0 else ~rf
        k = np.where(at_good, w.good, 1 - w.good); code = a.codes[rows, k]
        rv = np.zeros((runs, 4))
        if group != "sham": rv[rows, np.where(at_good, 1, 0)] = 1.0
        for _ in range(TRAIN): a.mb.step(code=code, reinf=rv); calls += 1
        if phase == 0:
            for _ in range(gap): a.mb.step()              # a silent world step: traces decay in time
    pre = valences(a.mb, a.codes, w.good)
    a.mb.tc[:] = 0.0; a.mb.tr[:] = 0.0          # relocation keeps the weights only; nothing else has run
    if not test: return dict(pre=pre, train_calls=calls, reward_first=rf)
    o = simulate(w, a, TEST_BLOCKS*STEPS, learn_on)
    o.update(pre=pre, train_calls=calls, reward_first=rf)
    return o


# ------------------------------------------------------------------ 7.0 statistics
_idx = {}
def _resample(n):
    if n not in _idx: _idx[n] = np.random.default_rng(BOOT_SEED).integers(0, n, (NBOOT, n))
    return _idx[n]

def wilson(k, n):
    p = k/n; d = 1 + Z*Z/n; c = (p + Z*Z/(2*n))/d; h = Z*np.sqrt(p*(1 - p)/n + Z*Z/(4*n*n))/d
    return p, c - h, c + h

def boot(kind, a, b=None):
    i = _resample(len(a))
    with np.errstate(divide="ignore", invalid="ignore"):
        f = {"GM": lambda x, y: np.median(x, -1), "DGM": lambda x, y: np.median(x, -1) - np.median(y, -1),
             "RGM": lambda x, y: np.median(x, -1)/np.median(y, -1), "DP": lambda x, y: x.mean(-1) - y.mean(-1)}[kind]
        pt = f(np.asarray(a, float), None if b is None else np.asarray(b, float))
        bs = f(np.asarray(a, float)[i], None if b is None else np.asarray(b, float)[i])
    lo, hi = np.nanpercentile(bs, [QLO, QHI])
    return float(pt), float(lo), float(hi)

def verdict(lo, hi, thr, most):
    if most: return "PASS" if hi <= thr else "FAIL" if lo > thr else "INCONCLUSIVE"
    return "PASS" if lo >= thr else "FAIL" if hi < thr else "INCONCLUSIVE"

def crit(label, kind, thr, most, a, b=None, n_min=50):
    n = len(a)
    if n < n_min:
        print(f"   {label}: n {n} < {n_min} -> UNREADABLE"); return "UNREADABLE"
    if kind == "P":
        k = int(np.sum(a)); pt, lo, hi = wilson(k, n); extra = f"k {k} "
    elif kind == "WIN":
        k = int(np.sum(a < b)); ties = float(np.mean(a == b)); pt, lo, hi = wilson(k, n); extra = f"k {k} ties {ties*100:.1f}% "
        if ties > 0.20:
            print(f"   {label}: WIN {extra}n {n} -> UNREADABLE (ties)"); return "UNREADABLE"
    else:
        pt, lo, hi = boot(kind, a, b); extra = ""
    out = verdict(lo, hi, thr, most)
    print(f"   {label}: {kind} {extra}n {n}  value {pt:.3f}  97.5% interval [{lo:.3f}, {hi:.3f}]"
          f"  {'at most' if most else 'at least'} {thr} -> {out}")
    return out


# ------------------------------------------------------------------ section 6 measures
def late(x): return x[-3:].mean(0)
def unrec(o): return ~o["plume_late"]

def measures(name, o, m, label):
    n = int(m.sum()); g, b = late(o["g"])[m], late(o["b"])[m]
    vg, vb = o["first_g"][m] >= 0, o["first_b"][m] >= 0
    eg, eb = vg & (o["first_g"][m] < 3*STEPS), vb & (o["first_b"][m] < 3*STEPS)
    stay = (o["last_b"] - o["first_b"])[m][vb]
    fmt = lambda v: " ".join(f"{x:5.1f}" for x in v)
    md = lambda x: float(np.median(x)) if len(x) else float("nan")
    print(f"   {name:13s} {label:8s} n {n:3d} | visited R {vg.mean()*100:5.1f}% P {vb.mean()*100:5.1f}% both {(vg & vb).mean()*100:5.1f}%"
          f" (first third {eg.mean()*100:5.1f}/{eb.mean()*100:5.1f}/{(eg & eb).mean()*100:5.1f}) | first visit step"
          f" {md(np.where(vg & vb, np.minimum(o['first_g'][m], o['first_b'][m]), np.maximum(o['first_g'][m], o['first_b'][m]))[vg | vb]):5.0f};"
          f" first punished step {md(o['first_b'][m][vb]):5.0f} (n {int(vb.sum())}), from it to the last step at the punisher {md(stay):5.0f}")
    print(f"      dwell last third R median {md(g):5.1f} mean {g.mean():5.1f}, P median {md(b):5.1f} mean {b.mean():5.1f}"
          f" | late unrecovered {int(unrec(o)[m].sum())}/{n} | contacts/agent {o['contacts'][m].mean():6.1f}"
          f" near wall {o['nearwall'][m].mean()/(3*STEPS)*100:5.2f}% | visits R {md(o['visits_g'][m][vg]):4.0f} P {md(o['visits_b'][m][vb]):4.0f},"
          f" steps per visit R {md((o['g'].sum(0)[m]/np.maximum(o['visits_g'][m], 1))[vg]):4.1f}"
          f" P {md((o['b'].sum(0)[m]/np.maximum(o['visits_b'][m], 1))[vb]):4.1f}; longest unbroken rewarded run {md(o['long_g'][m][vg]):4.0f}")
    print(f"      per block median dwell R {fmt(np.median(o['g'][:, m], 1))} | P {fmt(np.median(o['b'][:, m], 1))}")
    wn, wo = o["w_none"][m].sum(), o["w_other"][m].sum()
    print(f"      nothing held on {o['none_held'][m].mean()/o['steps']*100:5.1f}% of steps; whiffs handed to navigation:"
          f" nothing held {o['h_none'][m].sum()/max(wn, 1)*100:5.1f}% of {int(wn)}, other odour held {o['h_other'][m].sum()/max(wo, 1)*100:5.1f}% of {int(wo)}")
    v = o["val"][-1][m]
    print(f"      learned valence at the end: rewarded odour, receivers n {int(vg.sum())} ({vg.mean()*100:.0f}% of group) median {md(v[vg, 0]):+.3f},"
          f" all {md(v[:, 0]):+.3f} | punished odour, receivers n {int(vb.sum())} ({vb.mean()*100:.0f}%) median {md(v[vb, 1]):+.3f}, all {md(v[:, 1]):+.3f}"
          f" | reinforced steps R {md(o['g'].sum(0)[m][vg]):5.0f} P {md(o['b'].sum(0)[m][vb]):5.0f}")
    if vb.any(): print(f"      per block, receivers: punished odour {' '.join(f'{x:+.2f}' for x in np.median(o['val'][:, m][:, vb, 1], 1))}"
                       f" | rewarded odour {' '.join(f'{x:+.2f}' for x in (np.median(o['val'][:, m][:, vg, 0], 1) if vg.any() else []))}")


def e1(mode):
    seeds = SEEDS[mode][0]; res = {}
    print(f"\n==== E1 natural search. world seed {seeds[0]}, agent seed {seeds[1]}, {R} rows ====")
    for arm in E1_ARMS:
        o = res[arm] = run_e1(arm, seeds, keep_src=arm == "intact")
        allr = np.ones(R, bool); ps = o["pstart"]
        print()
        for m, lab in ((allr, "all"), (ps, "P-start"), (~ps, "R-start")):
            if arm in ("intact", "no-learning", "known") or lab != "R-start": measures(arm, o, m, lab)
        if o["calls"]: print(f"      learning calls {o['calls']} over {o['steps']} steps; two sources in reach on {o['merged']} row-steps")
    I, N, K, RW, OR = res["intact"], res["no-learning"], res["known"], res["random"], res["oracle"]
    ps = I["pstart"]; out = {}
    print("\n== Q1 validity (all rows, last third) ==")
    q1 = [crit("(a) rewarding dwell, oracle - random", "DGM", 10, False, late(OR["g"]), late(RW["g"]))]
    for arm in E1_ARMS[2:]:
        for key in ("g", "b"):
            q1.append(crit(f"(b) {arm} dwell at {'R' if key == 'g' else 'P'}", "GM", 594, True, late(res[arm][key])))
    q1.append(crit("(c) total dwell, intact - random", "DGM", 10, False, late(I["g"]) + late(I["b"]), late(RW["g"]) + late(RW["b"])))
    print("\n== Q2 search maintained while learning (late unrecovered) ==")
    q2 = [crit("(a) intact, all rows", "P", 0.100, True, unrec(I))]
    ref = crit("    reference: known valence, all rows", "P", 0.100, True, unrec(K))
    for m, lab in ((ps, "P-start"), (~ps, "R-start")):
        crit(f"    reported: intact {lab}", "P", 0.100, True, unrec(I)[m]); crit(f"    reported: known {lab}", "P", 0.100, True, unrec(K)[m])
        q2.append("UNREADABLE" if ref == "FAIL" else crit(f"(b) intact - known, {lab}", "DP", 0.10, True, unrec(I)[m], unrec(K)[m]))
    g3 = ps & (I["first_b"] >= 0)
    print(f"\n== Q3 a learned negative valence becomes avoidance. G3 = P-start rows punished at least once: {int(g3.sum())}/{int(ps.sum())}"
          f" ({g3.sum()/ps.sum()*100:.1f}%) ==")
    base = crit("    readability: no-learning punishing dwell in G3", "GM", 10, False, late(N["b"])[g3])
    q3 = [crit("(a) learned valence of the punished odour", "GM", -0.5, True, I["val"][-1][g3, 1])]
    if base == "PASS":
        q3 += [crit("(b) punishing dwell, intact", "GM", 1.0, True, late(I["b"])[g3]),
               crit("(c) intact below no-learning", "WIN", 0.60, False, late(I["b"])[g3], late(N["b"])[g3]),
               crit("(c) punishing dwell, intact / no-learning", "RGM", 0.75, True, late(I["b"])[g3], late(N["b"])[g3])]
    else: q3 += ["UNREADABLE"]*3; print("   (b), (c): UNREADABLE, the no-learning baseline does not PASS 'at least 10'")
    print("\n== Q4 search continues after avoidance (G3 rows, known valence as reference) ==")
    refa = crit("    readability: known arm avoids (P-start punishing dwell)", "GM", 1.0, True, late(K["b"])[ps])
    refb = crit("    readability: known arm rewarding dwell in G3", "GM", 10, False, late(K["g"])[g3])
    if refa != "PASS": q4 = ["UNREADABLE"]*2; print("   Q4: UNREADABLE, the reference does not avoid")
    else:
        q4 = [crit("(a) reach the rewarding source after the first punished step, intact - known", "DP", -0.10, False,
                   (I["last_g"] > I["first_b"])[g3], (K["first_g"] >= 0)[g3])]
        q4.append(crit("(b) rewarding dwell, intact / known", "RGM", 0.75, False, late(I["g"])[g3], late(K["g"])[g3])
                  if refb == "PASS" else "UNREADABLE")
    g5 = I["first_g"] >= 0
    print(f"\n== Q5 positive valence, weight level only. G5 = rows rewarded at least once: {int(g5.sum())}/{R} ==")
    q5 = crit("learned valence of the rewarded odour", "GM", 0.5, False, I["val"][-1][g5, 0])
    print("\n== 7.2 gate comparison, auxiliary ==")
    rg, ru = replay(I, True), replay(I, False)
    print(f"   replay instrument (self-check 7): gated replay reproduces the intact arm's end values: {np.allclose(rg, I['val'][-1], atol=1e-12)}")
    lg = I["long_g"]
    print(f"   longest unbroken rewarded run, G5: median {np.median(lg[g5]):.0f}, p90 {np.percentile(lg[g5], 90):.0f};"
          f" rows under 10: {int((g5 & (lg < 10)).sum())}, 10-24: {int((g5 & (lg >= 10) & (lg < 25)).sum())}, 25 or more: {int((g5 & (lg >= 25)).sum())}")
    _, lo, hi = boot("RGM", ru[g5, 0], rg[g5, 0]); crit("replay, ungated / gated, G5", "RGM", 0.80, True, ru[g5, 0], rg[g5, 0])
    print("   reading: " + ("the rule with the gate keeps more of the value at the exposures that occurred" if hi <= 0.80 else
                            "no difference at the exposures that occurred" if lo >= 0.95 and hi <= 1.05 else "not discriminated in this run")
          + ("" if (g5 & (lg >= 25)).sum() >= 50 else "; fewer than 50 rows reach 25 consecutive steps, so this speaks for short stays only"))
    for m, lab in ((g5 & (lg < 10), "under 10"), (g5 & (lg >= 10) & (lg < 25), "10-24"), (g5 & (lg >= 25), "25 or more")):
        crit(f"   stratum {lab}", "RGM", 0.80, True, ru[m, 0], rg[m, 0])
    U = res["ungated"]; gu = U["first_g"] >= 0
    print(f"   free-running ungated arm, descriptive: rewarded-odour value among its receivers (n {int(gu.sum())}) median"
          f" {np.median(U['val'][-1][gu, 0]):+.3f}; intact receivers (n {int(g5.sum())}) {np.median(I['val'][-1][g5, 0]):+.3f}")
    e1v = "YES" if all(x == "PASS" for x in q1 + q2 + q3 + q4) else "NO" if "FAIL" in q1 + q2 + q3 + q4 else "NOT DECIDED BY THIS RUN"
    print(f"\n==== E1 VERDICT (Q1-Q4, integrated behaviour): Q1 {sorted(set(q1))} Q2 {q2} Q3 {q3} Q4 {q4} -> {e1v} ====")
    print(f"     Q5 (weight level): {q5}")
    return res


def e2(mode):
    seeds = SEEDS[mode][1]
    print(f"\n==== E2 controlled experience. world seed {seeds[0]}, agent seed {seeds[1]}, {R} rows, every row a P-start row ====")
    T, S, UG = run_e2("trained", seeds), run_e2("sham", seeds), run_e2("ungated", seeds, test=False)
    allr = np.ones(R, bool)
    print(f"   training protocol AS AMENDED before the evaluation: {TRAIN} consecutive steps at one source, {GAP} silent steps,"
          f" {TRAIN} at the other. In E2 'last third' below means the whole {TEST_BLOCKS}-block test.")
    T0 = run_e2("trained", seeds, gap=0, test=False)
    for lab, o in (("amended (gap)", T), ("as first registered (no gap)", T0)):
        rf = o["reward_first"]
        print(f"   pre-test valence, {lab}: rewarded odour trained first {np.median(o['pre'][rf, 0]):+.3f} / trained second"
              f" {np.median(o['pre'][~rf, 0]):+.3f};  punished odour trained first {np.median(o['pre'][~rf, 1]):+.3f} / trained second"
              f" {np.median(o['pre'][rf, 1]):+.3f}")
    for name, o in (("trained", T), ("sham", S)):
        print(); measures(name, o, allr, "all")
        print(f"      training calls {o['train_calls']} (2 x {TRAIN}); test learning calls {o['calls']} (frozen); reward-first rows {int(o['reward_first'].sum())};"
              f" pre-test valence rewarded {np.median(o['pre'][:, 0]):+.3f} punished {np.median(o['pre'][:, 1]):+.3f}")
    print("\n== Q6 controlled experience (learning frozen) ==")
    mc = [crit("    manipulation check: trained, punished odour before the test", "GM", -0.5, True, T["pre"][:, 1]),
          crit("    manipulation check: sham >= -0.1", "GM", -0.1, False, S["pre"][:, 1]),
          crit("    manipulation check: sham <= +0.1", "GM", 0.1, True, S["pre"][:, 1])]
    tb, sb = T["b"].sum(0), S["b"].sum(0)
    if not all(x == "PASS" for x in mc): q6 = ["UNREADABLE"]*3; print("   Q6: UNREADABLE, the training did not install the memory")
    else:
        base = crit("    readability: sham punishing dwell over the test", "GM", 10, False, sb)
        q6 = [crit("(a) punishing dwell, trained / sham", "RGM", 0.5, True, tb, sb) if base == "PASS" else "UNREADABLE",
              crit("(b) trained below sham", "WIN", 0.60, False, tb, sb),
              crit("(c) reach the rewarding source, trained - sham", "DP", 0.25, False, T["first_g"] >= 0, S["first_g"] >= 0)]
    print("\n== 7.2 gate at 30 consecutive steps, weight level ==")
    for j, lab in ((0, "rewarded"), (1, "punished")):
        crit(f"   |value| of the {lab} odour, trained-ungated / trained-gated", "RGM", 0.85, True, np.abs(UG["pre"][:, j]), np.abs(T["pre"][:, j]))
    A = run_e2("trained", seeds, learn_on=True)
    print("\n   auxiliary, no criterion: the same test with learning ON"); measures("trained+learn", A, allr, "all")
    print("\n   the protocol AS FIRST REGISTERED (no gap), reported beside the amended one:")
    T0f, S0f = run_e2("trained", seeds, gap=0), run_e2("sham", seeds, gap=0)
    crit("   as registered: manipulation check, trained punished odour", "GM", -0.5, True, T0f["pre"][:, 1])
    crit("   as registered: (a) punishing dwell, trained / sham", "RGM", 0.5, True, T0f["b"].sum(0), S0f["b"].sum(0))
    crit("   as registered: (b) trained below sham", "WIN", 0.60, False, T0f["b"].sum(0), S0f["b"].sum(0))
    crit("   as registered: (c) reach the rewarding source, trained - sham", "DP", 0.25, False, T0f["first_g"] >= 0, S0f["first_g"] >= 0)
    e2v = "PASS" if all(x == "PASS" for x in q6) else "FAIL" if "FAIL" in q6 else "UNREADABLE" if "UNREADABLE" in q6 else "INCONCLUSIVE"
    print(f"\n==== E2 RESULT (Q6, a trained memory driving behaviour with nothing learned in the test): {q6} -> {e2v} ====")


def demo():
    rng = np.random.default_rng(1); n, T = 50, 300
    m = MB4(n, parallel=False, gated=True, rng=np.random.default_rng(0), **MB)
    codes = np.stack([m.odour(101), m.odour(102)], 1); good = rng.integers(0, 2, n)
    src = np.where(rng.random((T, n)) < 0.15, rng.integers(0, 2, (T, n)), -1)
    def final(rows_):
        mm = MB4(len(rows_), parallel=False, gated=True, rng=np.random.default_rng(0), **MB)
        for s in src[:, rows_]:
            c, rv = inputs(codes[rows_], good[rows_], np.stack([s == 0, s == 1], 1)); mm.step(code=c, reinf=rv)
        return mm.w, mm.tc, mm.tr
    full = final(np.arange(n)); perm = rng.permutation(n); pfull = final(perm)
    for i in (0, 7, 49):
        alone = final(np.array([i])); j = int(np.flatnonzero(perm == i)[0])
        assert all(np.allclose(x[0], y[i], atol=1e-12) and np.allclose(z[j], y[i], atol=1e-12) for x, y, z in zip(alone, full, pfull))
    print("ok 1  a row's learning state is the same alone, in a population of 50, and in permuted order")
    mm = MB4(3, parallel=False, gated=True, rng=np.random.default_rng(0), **MB)
    c, rv = inputs(codes[:3], good[:3], np.ones((3, 2), bool)*[True, False]); mm.step(code=c, reinf=rv)
    tc0, tr0 = mm.tc.copy(), mm.tr.copy()
    for _ in range(10): mm.step()
    assert np.allclose(mm.tc, tc0*0.8**10) and np.allclose(mm.tr, tr0*0.8**10) and abs(0.8**10 - 0.107) < 1e-3
    print("ok 2  with no input both traces shrink by exactly 0.8 per step, 0.107 after 10")
    o = run_e1("intact", (3, 4), runs=40, steps=1200); assert o["calls"] == 1200 and o["merged"] == 0
    t = run_e2("trained", (3, 4), runs=40); assert t["train_calls"] == 2*TRAIN and t["calls"] == 0
    print("ok 3  one learning call per world step in E1, 60 in training, none during a frozen test")
    same = lambda x, y: all(np.array_equal(np.delete(x[k], 0, -1) if x[k].ndim and x[k].shape[-1] == 40 else x[k][1:],
                                           np.delete(y[k], 0, -1) if y[k].ndim and y[k].shape[-1] == 40 else y[k][1:])
                            for k in ("g", "b", "first_g", "last_b", "none_held", "pos_end", "w_end"))
    for legacy in (False, True):
        a_, b_ = (run_e1("intact", (3, 4), runs=40, steps=1200, legacy=legacy, displace=d) for d in (None, 0))
        ok = same(a_, b_)
        print(f"{'ok 4 ' if not legacy else 'note '} displacing one row leaves every other row bit-identical: {ok}"
              f"  ({'this loop' if not legacy else 'RUN 1 LOOP, expected False, for the record'})")
        assert ok or legacy
    wa = World6(20, np.random.default_rng(5), 5); ag = [make_agent("intact", 20, np.random.default_rng(6), wa) for _ in (0, 1)]
    wa.pos = wa.src[np.arange(20), wa.good].copy()
    for _ in range(12):
        c, rv = inputs(ag[0].codes, wa.good, wa.at_source()); ag[0].mb.step(code=c, reinf=rv); learn_legacy(ag[1], wa)
    assert np.allclose(ag[0].mb.w, ag[1].mb.w)
    print("ok 5  for an unbroken stay Run 1's loop and this one give the same weights")
    from ph14 import run as run14
    ref = run14("fix", "neutral", (1630, 1730)); mine = run_e1("no-learning", (1630, 1730), runs=200, assign=None)
    assert np.array_equal(ref["G"].reshape(9, STEPS, 200).sum(1), mine["g"]) and np.array_equal(ref["B"].reshape(9, STEPS, 200).sum(1), mine["b"])
    print("ok 6  with learning off the harness reproduces the H19 verdict run's `fix` arm")
    o = run_e1("intact", (3, 4), runs=40, steps=1200, keep_src=True)
    assert np.allclose(replay(o, True), o["val"][-1], atol=1e-12)
    print("ok 7  replaying a recorded input stream into a gated module reproduces the intact arm's values")


if __name__ == "__main__":
    mode = ([m for m in sys.argv[1:] if m in ("demo", "dev", "eval")] or ["demo"])[0]
    print(f"== H15 Run 2, {mode.upper()}. specification {SPEC} ==")
    print("== one amendment recorded before the evaluation: record:h15-run2-dev-log (E2 training gap). Q3(c) not amended. ==")
    if mode == "demo": demo(); sys.exit(0)
    if "e2only" not in sys.argv: e1(mode)
    e2(mode)
