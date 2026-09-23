#!/usr/bin/env python3
"""Absent-odour check: the adopted agent (ph21.Agent8) when the odour it values is absent.

Usage: python ph22.py demo | dev | eval

Design v1 FINAL, confirmed by the owner (decision:absent-odour-check-open): doc ddab34a689d056e2e, hash 3ec1b989...3d43,
stored before this file existed. A check, not a hypothesis: descriptive readings R0-R5, pre-fixed outcome labels on
Agent8's reach (R1, R5), no PASS / FAIL, no fix tested. World: ph16.World7 with the absent source's column set to
False AFTER World7 draws it (the random stream is consumed exactly as in the H23 task; checked every step against an
unmasked World7 twin). Agents: ph21.Agent8 (filter on, G 2, gate on) and ph19.Agent6 (filter off), imported unchanged,
on the same seeds and draws. No adopted module is edited. Nothing changes after the table.
"""
import sys, os, re, hashlib
import numpy as np
import ph15, ph21
from ph16 import World7, cast_draw, R, T, DOWN
from ph19 import Agent6
from ph21 import Agent8, G_STAR
from ph9 import W0, SLOPE, LMAX

sys.stdout.reconfigure(newline="\n")            # LF output, so the recorded sha256 equals the committed blob
DESIGN = "v1 FINAL doc ddab34a689d056e2e hash 3ec1b989a776ced5289ab64689cbc59535de28c307f47cf038d43d863bef3d43"
PH21_SHA = "3a1d79d9a0d235f1bef7e435ec594cff4048180e27b28dcd892598c58413cfc1"   # the version H23 ran (doc ddcec8520fcd8e23c)
SEEDS = dict(dev=(9890, 9990), eval=(1775, 1875))
T5 = 1800
#            present odour (A = `good`, the higher read-out), read-out value of A (B is 0)
WORLDS = {"W1": ("B", 1.0), "W2": ("A", 1.0), "W3": ("B", 0.0), "W4": ("B", -1.0)}
ARMS = {"Agent8": Agent8, "Agent6": Agent6}


def sha(p=__file__): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def q3(x, f=".0f"): return f"{np.percentile(x, 25):{f}}/{np.median(x):{f}}/{np.percentile(x, 75):{f}}" if len(x) else "n/a"
def first_true(m): return np.where(m.any(0), m.argmax(0), -1)
def med(x): return float(np.median(x)) if len(x) else float("nan")


class Masked(World7):
    """World7 with one source silenced after the draw. `absent` (per row) is set by run() once `good` is known."""

    def sense(self):
        self.raw = super().sense()
        x = self.raw.copy(); x[np.arange(self.R), self.absent] = False
        self.plume = x.any(1)
        return x


def run(world, arm, seeds, runs=R, steps=T):
    present, va = WORLDS[world]; rows = np.arange(runs)
    w = Masked(runs, np.random.default_rng(seeds[0]), seeds[0]); g = w.good
    w.pres = g.copy() if present == "A" else 1 - g; w.absent = 1 - w.pres
    tw = World7(runs, np.random.default_rng(seeds[0]), seeds[0])            # the unmasked twin: R0 (iv)
    kv = np.zeros((runs, 2)); kv[rows, g] = va
    rng = np.random.default_rng(seeds[1])
    a = Agent8(runs, rng, G=G_STAR, known=kv, rule=True, filt=True) if arm == "Agent8" else Agent6(runs, rng, G=G_STAR, known=kv, rule=True)
    a.cast_sign = cast_draw(seeds[1], runs)
    o = dict(world=world, arm=arm, pres=w.pres, absent=w.absent, src=w.src[rows, w.pres].copy(), steps=steps, draws_equal=True,
             H=np.full((steps, runs), -1, np.int8), W=np.zeros((steps, runs, 2), bool), NAV=np.zeros((steps, runs), bool),
             TO=np.zeros((steps, runs), bool), EV=np.zeros((steps, runs), bool), SINCE=np.zeros((steps, runs), np.float32),
             POS=np.zeros((steps, runs, 2)), HEAD=np.zeros((steps, runs)), S=np.zeros((steps, runs, 2)),
             AT=np.zeros((steps, runs), bool), C=np.zeros((steps, runs), bool))
    for t in range(steps):
        tw.pos, tw.head = w.pos.copy(), w.head.copy()
        whiffs = w.sense(); tr = tw.sense()
        on = w.wind_on(); ton = tw.wind_on()
        o["draws_equal"] &= bool(np.array_equal(tr, w.raw) and np.array_equal(on, ton)
                                 and np.array_equal(whiffs[rows, w.pres], w.raw[rows, w.pres]) and not whiffs[rows, w.absent].any())
        turn, h = a.act(w, whiffs, on)
        w.move(turn); a.bump(w.bumped)
        o["H"][t] = h; o["W"][t] = whiffs; o["NAV"][t] = a.nav_hit; o["TO"][t] = a.due_timeout; o["EV"][t] = a.due_evidence
        o["SINCE"][t] = a.since; o["POS"][t] = w.pos; o["HEAD"][t] = w.head; o["S"][t] = a.sel.s
        o["AT"][t] = w.at_source()[rows, w.pres]; o["C"][t] = w.bumped
    o["rng_equal"] = w.rng.bit_generator.state == tw.rng.bit_generator.state
    return o


KEYS = ("POS", "HEAD", "S", "H", "NAV")
def same(o1, o2, n=None): return all(np.array_equal(o1[k][:n], o2[k][:n]) for k in KEYS)
def absent_ok(o): r = np.arange(len(o["pres"])); return bool(not o["W"][:, r, o["absent"]].any() and not (o["H"] == o["absent"][None, :]).any())


def wil(m):
    k, n = int(np.sum(m)), len(m); pt, lo, hi = ph15.wilson(k, n); return k, n, pt, lo, hi

def label(m):
    k, n, pt, lo, hi = wil(m)
    if n < 50: return "UNREADABLE", (k, n, pt, lo, hi)
    return ("reach lost" if hi <= 0.20 else "reach kept" if lo >= 0.80 else "reach reduced"), (k, n, pt, lo, hi)


def summary(o, upto=None):
    """per-row quantities over the first `upto` steps (default all); design section 4"""
    s = o["steps"] if upto is None else upto; r = np.arange(len(o["pres"])); p = o["pres"]
    AT, W, H, NAV, POS = o["AT"][:s], o["W"][:s, r, p], o["H"][:s], o["NAV"][:s], o["POS"][:s]
    da = POS[:, :, 0] - o["src"][None, :, 0]; dc = np.abs(POS[:, :, 1] - o["src"][None, :, 1]); dist = np.hypot(da, dc)
    near5 = dist < 5.0; ent5 = (near5 & ~np.vstack([np.zeros((1, len(r)), bool), near5[:-1]])).sum(0)
    heldB = H == p[None, :]; prev = np.vstack([np.full((1, len(r)), False), heldB[:-1]])
    formed = (heldB & ~prev).sum(0); ended = ~heldB & prev
    return dict(reach=AT.any(0), first=first_true(AT), dwell=AT.sum(0), whiffs=W.sum(0), fw=first_true(W), nav=NAV.sum(0),
                lost=~W[-s//3:].any(0), nonav=~NAV[-s//3:].any(0), contacts=o["C"][:s].sum(0),
                heldB=heldB.mean(0), nothing=(H < 0).mean(0), formed=formed, released=ended.sum(0),
                end_to=(ended & o["TO"][:s] & ~o["EV"][:s]).sum(0), end_ev=(ended & o["EV"][:s] & ~o["TO"][:s]).sum(0),
                end_both=(ended & o["TO"][:s] & o["EV"][:s]).sum(0), end_none=(ended & ~o["TO"][:s] & ~o["EV"][:s]).sum(0),
                fh=first_true(H >= 0), heldB_end=heldB[-1], cone=((da > 0) & (da < LMAX) & (dc < W0 + SLOPE*da)).sum(0),
                da_min=da.min(0), da_end=da[-1], dc_end=dc[-1], dmin=dist.min(0), f5=first_true(near5), ent5=ent5,
                since_max=float(o["SINCE"][:s].max()), cum={c: AT[:c].any(0) for c in range(100, s + 1, 100)})


def describe(o, upto=None):
    d = summary(o, upto); n = len(d["reach"]); s = o["steps"] if upto is None else upto
    lab, (k, _, pt, lo, hi) = label(d["reach"]); rr = d["reach"]
    print(f"\n   [{o['world']} {o['arm']}] {s} steps: reach (within 3.0 of the present source at least once) {k}/{n} = {pt:.3f} [{lo:.3f}, {hi:.3f}]"
          + (f" -> {lab}" if o["arm"] == "Agent8" and o["world"] == "W1" else "") + f"; first-reach step quartiles {q3(d['first'][rr])}")
    print(f"      dwell (steps within 3.0) q1/median/q3 {q3(d['dwell'], '.1f')} mean {d['dwell'].mean():.2f}; rows with no whiff of the present plume in the last third"
          f" {int(d['lost'].sum())}; no nav in the last third {int(d['nonav'].sum())}; wall contacts per row {d['contacts'].mean():.3f} (rows with any {int((d['contacts'] > 0).sum())});"
          f" nav (row, step) {int(d['nav'].sum())}; cast clock max {d['since_max']:.0f}")
    print(f"      present-plume whiffs per row {d['whiffs'].mean():.2f} (rows with any {int((d['fw'] >= 0).sum())}, first whiff step quartiles {q3(d['fw'][d['fw'] >= 0])});"
          f" steps in the present cone per row {d['cone'].mean():.1f}")
    print(f"      holds: fraction of (row, step) holding B/present {d['heldB'].mean():.3f}, nothing {d['nothing'].mean():.3f}; holds of the present odour formed"
          f" {int(d['formed'].sum())} (rows {int((d['formed'] > 0).sum())}), released {int(d['released'].sum())} (timeout flag {int(d['end_to'].sum())},"
          f" evidence {int(d['end_ev'].sum())}, both {int(d['end_both'].sum())}, neither {int(d['end_none'].sum())}); first hold step quartiles"
          f" {q3(d['fh'][d['fh'] >= 0])} (never {int((d['fh'] < 0).sum())}); holding the present odour at step {s} {int(d['heldB_end'].sum())}/{n}")
    print(f"      trajectory: most-upwind d_along (start 20) q1/median/q3 {q3(d['da_min'], '.1f')}, rows passing upwind of the source (d_along < 0) {int((d['da_min'] < 0).sum())};"
          f" final d_along {q3(d['da_end'], '.1f')}, final |crosswind| {q3(d['dc_end'], '.1f')}; minimum distance {q3(d['dmin'], '.1f')};"
          f" first step within 5.0 {q3(d['f5'][d['f5'] >= 0])} (rows {int((d['f5'] >= 0).sum())}), within 3.0 {q3(d['first'][rr])} (rows {int(rr.sum())});"
          f" entries into 5.0 per row mean {d['ent5'].mean():.2f} (0: {int((d['ent5'] == 0).sum())}, 1: {int((d['ent5'] == 1).sum())},"
          f" 2: {int((d['ent5'] == 2).sum())}, 3+: {int((d['ent5'] >= 3).sum())})")
    print("      cumulative reach at 100-step checkpoints: " + " ".join(f"{c}:{int(v.sum())}" for c, v in d["cum"].items()))
    return d


# ------------------------------------------------------------------ self-checks
def seeds_unused():
    """design section 7: none of the check's seeds or derived generators appears in any other file under the repository
    (recursive; excluded by name: this file, its outputs ph22_*.txt, the check's documents absent_odour_check_*.md, master_plan.md)"""
    nums = [*SEEDS["dev"], *SEEDS["eval"], SEEDS["dev"][0] + 10_000, SEEDS["dev"][1] + 20_000, SEEDS["eval"][0] + 10_000, SEEDS["eval"][1] + 20_000]
    pat = re.compile(rb"(?<!\d)(" + "|".join(map(str, nums)).encode() + rb")(?!\d)"); hits = []; n = 0
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for f in files:
            if f == "ph22.py" or (f.startswith("ph22_") and f.endswith(".txt")) or (f.startswith("absent_odour_check_") and f.endswith(".md")) or f == "master_plan.md": continue
            n += 1
            if pat.search(open(os.path.join(root, f), "rb").read()): hits.append(os.path.relpath(os.path.join(root, f), repo))
    return hits, nums, n


def identities(res, n=None):
    """R0 (i)-(iv) on a set of runs {(world, arm): o}"""
    i1 = int(res[("W1", "Agent8")]["NAV"].sum()) == 0
    i2 = all(absent_ok(o) for o in res.values())
    i3 = {f"{wd} Agent8 == Agent6": same(res[(wd, "Agent8")], res[(wd, "Agent6")]) for wd in ("W2", "W3", "W4")}
    i3.update({f"W4 == W3 {a}": same(res[("W4", a)], res[("W3", a)]) for a in ARMS})
    i3["Agent6 W1 == W3"] = same(res[("W1", "Agent6")], res[("W3", "Agent6")])
    i4 = all(o["draws_equal"] and o["rng_equal"] for o in res.values())
    return i1, i2, i3, i4


def demo():
    print(f"== absent-odour check, self-checks (demo). design {DESIGN}; this file sha256 {sha()}; ph21.py sha256 {sha(ph21.__file__)} ==")
    assert sha(ph21.__file__) == PH21_SHA, "ph21.py is not the version H23 ran"
    seeds, n, steps = (5, 6), 40, 300
    w = Masked(400, np.random.default_rng(0), 0); d = w.pos[:, None, :] - w.src
    assert np.allclose(d[:, :, 0], DOWN) and np.allclose(np.abs(d[:, :, 1]), 5.0) and 5.0 < W0 + SLOPE*DOWN
    res = {(wd, a): run(wd, a, seeds, n, steps) for wd in WORLDS for a in ARMS}
    i1, i2, i3, i4 = identities(res)
    assert i4, "masking changed the random stream or the present column"
    print(f"ok  R0 (iv) masking after the draw: on every step of all 8 runs ({n} rows x {steps} steps) World7's own draw on the same positions equals the masked world's"
          f" pre-mask draw, the wind draws are equal, the present column is unchanged, the absent column is False, and the world generator's state is equal at the end")
    # the same check against a free-running unmasked World7: until the first step World7 would have delivered an absent whiff, the trajectories are identical
    o7 = ph21.run((1.0, 0.0), seeds, G_STAR, True, True, runs=n, steps=steps)          # ph21's own task run (World7, Agent8), W1's values
    o1 = res[("W1", "Agent8")]; r = np.arange(n); fa = first_true(o7["W"][:, r, o7["good"]])          # W1's absent odour is A = `good`
    pre = np.arange(steps)[:, None] < np.where(fa < 0, steps, fa)[None, :]
    eq = (o1["POS"] == o7["POS"]).all(2) & (o1["H"] == o7["H"]) & (o1["W"] == o7["W"]).all(2)
    assert (eq | ~pre).all() and np.array_equal(o1["pres"], 1 - o7["good"]), "the masked world departs from World7 before an absent whiff"
    print(f"ok  against ph21.run (unmasked World7, Agent8 at +1/0, same seeds): positions, holds and whiffs equal on every step before World7's first whiff of the absent"
          f" source (step median {med(fa[fa >= 0]):.0f}, never in {int((fa < 0).sum())} of {n} rows)")
    assert i1, "Agent8 surged in W1"
    assert i2, "the absent odour was sensed or held"
    assert all(i3.values()), f"identities {i3}"
    print(f"ok  R0 (i) Agent8 in W1: nav (row, step) 0; (ii) the absent odour never sensed and never held in any run; (iii) {i3}")
    assert (res[("W1", "Agent8")]["H"] == res[("W1", "Agent8")]["pres"][None, :]).any(), "W1: the present odour was never held (the circuit should still receive it)"
    hits, nums, nf = seeds_unused(); assert not hits, f"a seed of this check appears in {hits}"
    print(f"ok  seeds {SEEDS} and derived {nums[4:]} appear in no other file under the repository ({nf} files scanned; excluded by name ph22.py, ph22_*.txt,"
          f" absent_odour_check_*.md, master_plan.md)")


def main(mode):
    seeds = SEEDS[mode]
    print(f"== absent-odour check, {mode.upper()}. design {DESIGN}; this file sha256 {sha()}; ph21.py sha256 {sha(ph21.__file__)}"
          f" (the version H23 ran: {sha(ph21.__file__) == PH21_SHA}); world seed {seeds[0]}, agent seed {seeds[1]}; {R} rows x {T} steps per world and arm,"
          f" R5 W1 {R} x {T5}; G {G_STAR}, gate on; {'operation check only' if mode == 'dev' else 'the one evaluation'} ==")
    hits, nums, nf = seeds_unused()
    print(f"   seed self-check: {SEEDS[mode]} and derived {nums[4:]} in no other file ({nf} scanned): {not hits}{'' if not hits else ' ' + str(hits)}")
    print("   worlds: " + "; ".join(f"{k} present {v[0]}, read-out A {v[1]:+.0f} / B 0" for k, v in WORLDS.items()) + " (A = World7 `good`)")
    res = {(wd, a): run(wd, a, seeds) for wd in WORLDS for a in ARMS}
    sm = {key: describe(o) for key, o in res.items()}
    i1, i2, i3, i4 = identities(res)
    print("\n== readings (design v1 FINAL section 5; Wilson 95 percent; no PASS / FAIL) ==")
    print(f"   R0 (i) Agent8 in W1, nav (row, step): {int(res[('W1', 'Agent8')]['NAV'].sum())} -> {i1}; (ii) absent odour never sensed, never held, all 8 runs: {i2};"
          f" (iii) {i3}; (iv) masked draws == World7's on every step, generator state equal, all 8 runs: {i4}")
    a8, a6 = sm[("W1", "Agent8")], sm[("W1", "Agent6")]
    lab, (k, n, pt, lo, hi) = label(a8["reach"]); k6, _, p6, l6, h6 = wil(a6["reach"])
    print(f"   R1 W1 {T} steps: Agent8 reach {k}/{n} = {pt:.3f} [{lo:.3f}, {hi:.3f}] -> {lab.upper()}; Agent6 reach {k6}/{n} = {p6:.3f} [{l6:.3f}, {h6:.3f}]"
          f" (predicted 0.94 to 1.00)")
    dw = a8["dwell"] - a6["dwell"]
    print(f"      dwell median Agent8 {med(a8['dwell']):.1f} / Agent6 {med(a6['dwell']):.1f}, mean {a8['dwell'].mean():.2f} / {a6['dwell'].mean():.2f}; paired rows Agent8 below"
          f" {int((dw < 0).sum())}, equal {int((dw == 0).sum())} (both 0: {int(((a8['dwell'] == 0) & (a6['dwell'] == 0)).sum())}), above {int((dw > 0).sum())};"
          f" first-reach median {med(a8['first'][a8['reach']]):.0f} / {med(a6['first'][a6['reach']]):.0f}; B held at step {T} {int(a8['heldB_end'].sum())} / {int(a6['heldB_end'].sum())};"
          f" lost rows {int(a8['lost'].sum())} / {int(a6['lost'].sum())}; wall contacts per row {a8['contacts'].mean():.3f} / {a6['contacts'].mean():.3f}")
    for wd, tag in (("W2", "R2 control"), ("W3", "R3 identity"), ("W4", "R4 reported")):
        e = f"Agent8 == Agent6 {i3[f'{wd} Agent8 == Agent6']}" + (f"; == Agent6 W1 {i3['Agent6 W1 == W3']}" if wd == "W3" else "") + \
            (f"; W4 == W3 Agent8 {i3['W4 == W3 Agent8']}, Agent6 {i3['W4 == W3 Agent6']}" if wd == "W4" else "")
        kk, nn, pp, ll, hh = wil(sm[(wd, "Agent8")]["reach"])
        print(f"   {tag}, {wd}: {e}; reach {kk}/{nn} = {pp:.3f} [{ll:.3f}, {hh:.3f}], dwell median {med(sm[(wd, 'Agent8')]['dwell']):.1f}")
    print(f"\n== R5 the horizon: W1, {T5} steps, both arms ==")
    r5 = {a: run("W1", a, seeds, steps=T5) for a in ARMS}
    pref = {a: same(r5[a], res[("W1", a)], T) for a in ARMS}
    print(f"   implementation check: the first {T} steps of the {T5}-step runs equal the {T}-step runs bitwise: {pref}; Agent8 nav (row, step) {int(r5['Agent8']['NAV'].sum())};"
          f" absent odour never sensed or held {all(absent_ok(o) for o in r5.values())}; masked draws == World7's {all(o['draws_equal'] and o['rng_equal'] for o in r5.values())}")
    s5 = {a: describe(r5[a]) for a in ARMS}
    for a in ARMS:
        lab5, (k, n, pt, lo, hi) = label(s5[a]["reach"]); o = r5[a]
        thirds = [o["AT"][i*T:(i + 1)*T].sum(0) for i in range(3)]
        print(f"   R5 {a}: reach by {T5} {k}/{n} = {pt:.3f} [{lo:.3f}, {hi:.3f}]" + (f" -> {lab5.upper()}" if a == "Agent8" else "")
              + f"; cumulative reach at 600/1200/1800 {int(s5[a]['cum'][600].sum())}/{int(s5[a]['cum'][1200].sum())}/{int(s5[a]['cum'][1800].sum())};"
              f" dwell per third (median; mean) " + ", ".join(f"{med(x):.1f}; {x.mean():.2f}" for x in thirds)
              + f"; d_along at {T5} q1/median/q3 {q3(s5[a]['da_end'], '.1f')}, rows upwind of the source at {T5} {int((s5[a]['da_end'] < 0).sum())};"
              f" wall contacts per row {s5[a]['contacts'].mean():.3f}")
    print("\n== end of table; nothing changes after it ==")


if __name__ == "__main__":
    mode = ([m for m in sys.argv[1:] if m in ("demo", "dev", "eval")] or ["demo"])[0]
    if mode == "demo": demo(); sys.exit(0)
    main(mode)
