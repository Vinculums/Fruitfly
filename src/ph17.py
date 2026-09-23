#!/usr/bin/env python3
"""Selection-to-navigation link check (H20 follow-up). Measurement only, no hypothesis verdict.

Usage: python ph17.py demo | dev | eval

Does the identity of the tracked odour control movement in the adopted agent? Value and learning
are excluded (values 0, G 0: the agent is ph14.Agent3). Two intervention arms fix the held odour
to A or to B on every step (the selection block is not run; nothing else changes; no information
about sources is added); the third arm is the adopted circuit. Three pre-defined geometries.

Design v1, confirmed by the owner with two interpretation notes: doc d824732220256254b
(record:h20-linkcheck-design-v1, decision:h20-linkcheck-open). Readings L1-L5 are fixed there.
"""
import sys, hashlib
import numpy as np
from ph9 import UPWIND, CAST_PERIOD, MAXOFF, GAIN, MAXTURN, TURN_NOISE, STEPS, W0, SLOPE, LAM, LMAX, angdiff
from ph12 import SAT
from ph14 import World5, Agent3
from ph16 import Agent4, cast_draw, interval, med

DESIGN = "v1 doc d824732220256254b hash acd059a823ef7ccd09c4e68a6ad479bb422af4712252d015210d74bd575322ec"
R, T = 400, STEPS
SEEDS = dict(dev=(9830, 9930), eval=(1690, 1790))
GEOMS = {"C0": (10.0, 20.0), "C1": (10.0, 16.0), "C2": (12.0, 24.0)}       # separation s, start d downwind
# C2 was registered as (14, 28); the self-check found 28 > LMAX 25 (outside both cones) before any run.
# Replaced by the owner with (12, 24): overlap width 3.0 kept, cones separate below 18 (decision:h20-linkcheck-c2-amendment).
ARMS = {"track-A": 0, "track-B": 1, "circuit": None}

def sha(): return hashlib.sha256(open(__file__, "rb").read()).hexdigest()
def sep_point(s): return (s - 2*W0)/(2*SLOPE)                                # downwind distance where the cones separate


class World8(World5):
    """ph16.World7's placement with the geometry as parameters: two sources `s` apart crosswind at one
    downwind coordinate, the start on the midline `d` downwind; the 2 x 2 assignment puts odour A at +y
    in half the rows. `good` is kept only as the odour index the cell names; no value is used."""

    def __init__(self, runs, rng, seed, s, d):
        super().__init__(runs, rng)
        cell = np.empty(runs, int); cell[np.random.default_rng(seed + 10_000).permutation(runs)] = np.arange(runs) % 4
        self.cell, self.good, self.side, self.s, self.d = cell, cell // 2, np.where(cell % 2 == 0, 1.0, -1.0), s, d
        rows = np.arange(runs); x = self.src[:, 0, 0]; yc = self.src[:, 0, 1] + s/2
        self.src = np.zeros((runs, 2, 2)); self.src[:, :, 0] = x[:, None]
        self.src[rows, self.good, 1] = yc + self.side*s/2; self.src[rows, 1 - self.good, 1] = yc - self.side*s/2
        self.pos = np.stack([x + d, yc], 1); self.yc = yc


class Agent5(Agent4):
    """fixed None: Agent4 (with G 0 and zero values, ph14.Agent3). fixed 0 or 1: the held odour is that
    channel on every step; the selection block is not run; everything after it is Agent4's code."""

    def __init__(self, runs, rng, fixed=None, **kw):
        super().__init__(runs, rng, **kw); self.fixed = fixed

    def act(self, w, whiffs, wind_on):
        if self.fixed is None: return super().act(w, whiffs, wind_on)
        rows = np.arange(self.R)
        self.yp = self.up.step(whiffs.astype(float))            # the stage runs; nothing downstream reads it
        h = np.full(self.R, self.fixed)
        est = self.est = self.estimate(w, wind_on)
        val = np.where(h >= 0, self.known[rows, np.maximum(h, 0)], 0.0)
        hit = np.where(h >= 0, whiffs[rows, np.maximum(h, 0)], False)
        nav = hit | ((h < 0) & (whiffs & (self.chan_valence() >= 0)).any(1))
        self.nav_hit = nav
        self.since = np.where(nav, 0.0, self.since + 1.0)
        self.silence = np.where(hit, 0.0, self.silence + 1.0)
        side = np.where((self.since // CAST_PERIOD) % 2 == 0, 1.0, -1.0)*self.cast_sign
        off = MAXOFF*(1.0 - np.abs((self.since/SAT) % 2.0 - 1.0))
        tgt = np.where(nav, UPWIND, (UPWIND + side*off) % 360.0)
        self.tgt = tgt = np.where(val < 0, self.flee_side, tgt)
        turn = np.clip(GAIN*angdiff(tgt, est), -MAXTURN, MAXTURN)
        turn = turn + TURN_NOISE*self.rng.standard_normal(self.R)
        self.last_turn = turn
        return turn, h


def run(arm, geom, seeds, runs=R, steps=T):
    s, d = GEOMS[geom]
    w = World8(runs, np.random.default_rng(seeds[0]), seeds[0], s, d); rows = np.arange(runs)
    a = Agent5(runs, np.random.default_rng(seeds[1]), fixed=ARMS[arm], G=0.0, known=np.zeros((runs, 2)))
    a.cast_sign = cast_draw(seeds[1], runs)
    o = dict(arm=arm, geom=geom, s=s, d=d, src=w.src.copy(), yc=w.yc.copy(), cast=a.cast_sign.copy(),
             first=np.full((runs, 2), -1), dwell=np.zeros((runs, 2)), contacts=np.zeros(runs),
             W=np.zeros((steps, runs, 2), bool), NAV=np.zeros((steps, runs), bool), SINCE=np.zeros((steps, runs), np.float32),
             TGT=np.zeros((steps, runs)), TURN=np.zeros((steps, runs)), POS=np.zeros((steps, runs, 2)),
             HEAD=np.zeros((steps, runs)), H=np.full((steps, runs), -1, np.int8))
    for t in range(steps):
        whiffs = w.sense()
        turn, h = a.act(w, whiffs, w.wind_on())
        o["W"][t] = whiffs; o["NAV"][t] = a.nav_hit; o["SINCE"][t] = a.since; o["TGT"][t] = a.tgt; o["TURN"][t] = turn; o["H"][t] = h
        w.move(turn); a.bump(w.bumped)
        at = w.at_source()
        o["first"] = np.where((o["first"] < 0) & at, t, o["first"]); o["dwell"] += at
        o["POS"][t] = w.pos; o["HEAD"][t] = w.head; o["contacts"] += w.bumped
    da = o["POS"][:, :, 0] - o["src"][None, :, 0, 0]
    o["cone"] = np.stack([((da > 0) & (da < LMAX) & (np.abs(o["POS"][:, :, 1] - o["src"][None, :, k, 1]) < W0 + SLOPE*da)).sum(0)
                          for k in (0, 1)], 1)                                     # steps inside each cone
    f = np.where(o["first"] < 0, 10**9, o["first"]); o["reached"] = (o["first"] >= 0).any(1)
    o["which"] = np.where(o["reached"], f.argmin(1), -1); o["rs"] = np.where(o["reached"], f.min(1), -1)
    return o


# ------------------------------------------------------------------ readings (design section 5)
def reading(lo, hi, expressed=0.70, band=(0.40, 0.60)):
    if lo >= expressed: return "expressed"
    if band[0] <= lo and hi <= band[1]: return "not expressed"
    return "partial"

def first_true(mask):
    """per column: first row index where mask is True, else -1"""
    return np.where(mask.any(0), mask.argmax(0), -1)


def describe(o):
    k = ARMS[o["arm"]]; n = len(o["reached"]); r = o["reached"]
    if k is None:
        held = o["H"] >= 0; ft = first_true(held); fh = np.where(ft >= 0, o["H"][np.maximum(ft, 0), np.arange(n)], -1)
        print(f"   [{o['arm']}] reached A first {int((o['which'] == 0).sum())} B first {int((o['which'] == 1).sum())} none {int((~r).sum())};"
              f" first hold A {int((fh == 0).sum())} B {int((fh == 1).sum())} none {int((fh < 0).sum())}, step median {med(ft[ft >= 0]):.0f};"
              f" first-approach step median {med(o['rs'][r]):.0f}; dwell median A {med(o['dwell'][:, 0]):.1f} B {med(o['dwell'][:, 1]):.1f};"
              f" cone steps mean A {o['cone'][:, 0].mean():.0f} B {o['cone'][:, 1].mean():.0f}; contacts/row {o['contacts'].mean():.2f}")
        return
    tr, ot = o["which"] == k, o["which"] == 1 - k
    print(f"   [{o['arm']}] reached the tracked source first {int(tr.sum())}, the other first {int(ot.sum())}, none {int((~r).sum())};"
          f" first-approach step median tracked {med(o['rs'][tr]):.0f} other {med(o['rs'][ot]):.0f};"
          f" dwell median tracked {med(o['dwell'][:, k]):.1f} other {med(o['dwell'][:, 1 - k]):.1f};"
          f" cone steps mean tracked {o['cone'][:, k].mean():.0f} other {o['cone'][:, 1 - k].mean():.0f};"
          f" hits handed/row {o['NAV'].sum(0).mean():.1f}; contacts/row {o['contacts'].mean():.2f}")


def judge(res, geom):
    A, B, C = res["track-A"], res["track-B"], res["circuit"]; n = R; rows = np.arange(n); s, d = GEOMS[geom]
    print(f"\n   -- readings, {geom} (s {s:.0f}, d {d:.0f}); diagnostic readings, not a hypothesis verdict --")
    both = A["reached"] & B["reached"]
    if both.sum() < 50: print(f"   L1: rows reached in both fixed arms {int(both.sum())} < 50 -> UNREADABLE")
    else:
        each = ((A["which"] == 0) & (B["which"] == 1))[both]; same = (A["which"] == B["which"])[both]
        k1, p1, lo1, hi1 = interval("P", each); k2, p2, lo2, hi2 = interval("P", same)
        out = "expressed in the first reach" if lo1 >= 0.70 else "not expressed in the first reach" if lo2 >= 0.70 else "partial"
        print(f"   L1 first reach, rows reached in both fixed arms {int(both.sum())}: each arm reached its tracked source first {k1} = {p1:.3f}"
              f" [{lo1:.3f}, {hi1:.3f}]; the same source in both arms {k2} = {p2:.3f} [{lo2:.3f}, {hi2:.3f}] -> {out}."
              f" (The first rate holds when the two arms track different odours; no-choice: track-A {int((~A['reached']).sum())}, track-B {int((~B['reached']).sum())})")
    for o in (A, B):
        k = ARMS[o["arm"]]; dt, do = o["dwell"][:, k], o["dwell"][:, 1 - k]; ties = float((dt == do).mean())
        if ties > 0.20: print(f"   L2 dwell, {o['arm']}: ties {ties*100:.1f}% > 20% -> UNREADABLE (ties, of which both zero {int(((dt == 0) & (do == 0)).sum())})"); continue
        kk, p, lo, hi = interval("P", dt > do)
        print(f"   L2 dwell over {T} steps, {o['arm']}: P(dwell at tracked > other) {kk}/{n} = {p:.3f} [{lo:.3f}, {hi:.3f}], ties {ties*100:.1f}%"
              f" -> {reading(lo, hi)} in dwell. (Dwell is a more lenient measure than the first reach: it accrues over the whole trial.)")
    tdiff = first_true(A["TGT"] != B["TGT"]); pdiff = first_true((A["POS"] != B["POS"]).any(2))
    single = first_true(A["W"][:, :, 0] != A["W"][:, :, 1])
    reach = np.where(both, np.minimum(A["rs"], B["rs"]), np.where(A["reached"], A["rs"], B["rs"]))
    before = (tdiff >= 0) & ((reach < 0) | (tdiff < reach))
    print(f"   L3 divergence: target first differs at step median {med(tdiff[tdiff >= 0]):.0f} ({int((tdiff >= 0).sum())} rows diverge);"
          f" position first differs at median {med(pdiff[pdiff >= 0]):.0f}; first single-channel whiff at median {med(single[single >= 0]):.0f};"
          f" diverge before the first reach {int(before.sum())}/{n}; target first differs exactly at the first single-channel whiff"
          f" {int(((tdiff >= 0) & (tdiff == single)).sum())}/{int((tdiff >= 0).sum())}")
    dsep = sep_point(s)
    for o in (A, B):
        k = ARMS[o["arm"]]; da = o["POS"][:, :, 0] - o["src"][None, :, 0, 0]
        tsep = first_true(da < dsep); ok = (tsep >= 0) & ((o["rs"] < 0) | (tsep < o["rs"]))
        if ok.sum() < 50: print(f"   L4 {o['arm']}: rows passing the separation point {dsep:.0f} before a reach {int(ok.sum())} < 50 -> UNREADABLE"); continue
        sign = np.sign(o["src"][rows, k, 1] - o["yc"]); off = (o["POS"][np.maximum(tsep, 0), rows, 1] - o["yc"])*sign
        kk, p, lo, hi = interval("P", (off > 0)[ok])
        print(f"   L4 crosswind at the separation point ({dsep:.0f} downwind), {o['arm']}: offset toward the tracked source positive in {kk}/{int(ok.sum())}"
              f" = {p:.3f} [{lo:.3f}, {hi:.3f}] -> {reading(lo, hi)}")
    held = C["H"] >= 0; ft = first_true(held); fh = np.where(ft >= 0, C["H"][np.maximum(ft, 0), rows], -1)
    m = C["reached"] & (fh >= 0)
    if m.sum() < 50: print(f"   L5 circuit: rows reached with a first hold {int(m.sum())} < 50 -> UNREADABLE")
    else:
        kk, p, lo, hi = interval("P", (C["which"] == fh)[m])
        print(f"   L5 circuit arm: first reach = the first hold's source {kk}/{int(m.sum())} = {p:.3f} [{lo:.3f}, {hi:.3f}]"
              f" (H20 evaluation, neutral arm: 0.532 of all rows reached the valued source, first hold == source reached 335/400)")


# ------------------------------------------------------------------ self-checks (design section 7)
def demo():
    seeds = (5, 6); n = 40
    ws = [World8(n, np.random.default_rng(seeds[0]), seeds[0], 10.0, 20.0) for _ in (0, 1)]
    ag = [Agent3(n, np.random.default_rng(seeds[1]), known=np.zeros((n, 2))), Agent5(n, np.random.default_rng(seeds[1]), fixed=None, G=0.0, known=np.zeros((n, 2)))]
    for a in ag: a.cast_sign = cast_draw(seeds[1], n)
    for _ in range(400):
        for w, a in zip(ws, ag):
            t, _ = a.act(w, w.sense(), w.wind_on()); w.move(t); a.bump(w.bumped)
    assert np.array_equal(ws[0].pos, ws[1].pos) and np.array_equal(ws[0].head, ws[1].head), "the circuit arm is not Agent3"
    for geom, (s, d) in GEOMS.items():
        w = World8(400, np.random.default_rng(0), 0, s, d); dd = w.pos[:, None, :] - w.src
        assert np.allclose(dd[:, :, 0], d) and np.allclose(np.abs(dd[:, :, 1]), s/2) and d < LMAX and s/2 < W0 + SLOPE*d, geom
        assert np.minimum(w.src, w.arena - w.src).min() >= 68 and np.bincount(w.cell).tolist() == [100]*4
        plus = w.src[:, 0, 1] > w.src[:, 1, 1]; assert plus.sum() == 200, "odour A is not at +y in half the rows"
        rate = sum(w.sense().astype(float) for _ in range(2000))/2000
        p = 0.3*np.exp(-d/LAM); width = 2*(W0 + SLOPE*d) - s; dist = float(np.hypot(d, s/2))
        assert abs(rate[:, 0].mean() - p) < 0.01 and abs(rate[:, 1].mean() - p) < 0.01
        print(f"ok  {geom}: start {d:.0f} downwind, {s/2:.0f} crosswind of each source, inside both cones; whiff p {rate[:, 0].mean():.4f}/{rate[:, 1].mean():.4f}"
              f" (table {p:.3f}); overlap width {width:.1f}; cones separate below {sep_point(s):.0f}; distance {dist:.1f}; walls >= 68; cells 100 each")
    o = {arm: run(arm, "C0", seeds, runs=n, steps=200) for arm in ("track-A", "track-B")}
    for arm, k in (("track-A", 0), ("track-B", 1)):
        assert (o[arm]["H"] == k).all() and np.array_equal(o[arm]["NAV"], o[arm]["W"][:, :, k]), f"{arm}: h not constant or hit != that channel's whiffs"
    assert np.array_equal(o["track-A"]["cast"], o["track-B"]["cast"]), "the cast draw differs between arms"
    tdiff = first_true(o["track-A"]["TGT"] != o["track-B"]["TGT"])
    for r in range(n):
        t = tdiff[r] if tdiff[r] >= 0 else 200
        assert np.array_equal(o["track-A"]["POS"][:t, r], o["track-B"]["POS"][:t, r]), "positions differ before the target does"  # POS[t] follows the move on TGT[t]
    print("ok  the circuit arm reproduces ph14.Agent3 bitwise (G 0, zero values, cast draw applied to both)")
    print(f"ok  fixed arms: h constant on every step, the hit equals that channel's whiffs, same cast draw, positions identical up to the step"
          f" the target first differs (median {med(tdiff[tdiff >= 0]):.0f}, {int((tdiff >= 0).sum())}/{n} rows diverge in 200 steps)")


def main(mode):
    seeds = SEEDS[mode]
    print(f"== Selection-to-navigation link check, {mode.upper()}. design {DESIGN}; this file sha256 {sha()}; world seed {seeds[0]},"
          f" agent seed {seeds[1]}; {R} rows x {T} steps; values 0, G 0; {'operation check only' if mode == 'dev' else 'the one run'} ==")
    for geom, (s, d) in GEOMS.items():
        print(f"\n== {geom}: sources {s:.0f} apart, start {d:.0f} downwind on the midline; whiff p {0.3*np.exp(-d/LAM):.3f} per plume at the start,"
              f" overlap width {2*(W0 + SLOPE*d) - s:.1f}, cones separate below {sep_point(s):.0f}, distance {np.hypot(d, s/2):.1f} ==")
        res = {arm: run(arm, geom, seeds) for arm in ARMS}
        for arm in ARMS: describe(res[arm])
        judge(res, geom)


if __name__ == "__main__":
    mode = ([m for m in sys.argv[1:] if m in ("demo", "dev", "eval")] or ["demo"])[0]
    if mode == "demo": demo(); sys.exit(0)
    main(mode)
