#!/usr/bin/env python3
"""H20 diagnosis after the G bench. Measurement only: ph16.py, design v3 and the bench verdict are
untouched; this file defines its own variant agent and never runs the task.

Two questions from the owner.
(1) Where does the value gain enter? Agent4.act uses y' = y*(1 + G*max(v, 0)) in TWO places: as
    the selection circuit's input and in the evidence-release comparison. Variants apply the gain
    in one place only ('circuit', 'release'); 'both' must reproduce the registered bench exactly.
(2) Sensory history before the first hold, on the registered bench input: whiffs per channel
    before the first hold, the order of the first whiff and the first hold, whether both channels'
    responses were present at the first hold. Tests the arrival-order interpretation recorded
    with the bench result against a circuit-process alternative.
"""
import hashlib
import numpy as np
import ph15
from ph9 import UPWIND, CAST_PERIOD, MAXOFF, GAIN, MAXTURN, TURN_NOISE, angdiff
from ph11 import RESET_AFTER, MARGIN
from ph12 import SAT
from ph16 import Agent4, Still, BENCH, bench, med

P0 = BENCH["rates"][0]
CANDS = (0.0, 0.5, 1.0, 2.0)


class Agent4b(Agent4):
    """Agent4 with the registered gain applied in one place only. where='both' IS Agent4 (checked)."""

    def __init__(self, runs, rng, where="both", **kw):
        super().__init__(runs, rng, **kw); self.where = where; self.y0 = np.zeros((runs, 2))

    def act(self, w, whiffs, wind_on):
        rows = np.arange(self.R)
        self.y0 = y0 = self.up.step(whiffs.astype(float)); g = 1.0 + self.G*np.maximum(self.chan_valence(), 0.0)
        yc = y0*g if self.where in ("both", "circuit") else y0      # what the circuit integrates
        yr = y0*g if self.where in ("both", "release") else y0      # what the evidence release compares
        self.yp = yc
        hp = self.held(); committed = hp >= 0; hi = np.maximum(hp, 0); other = 1 - hi
        self.due_timeout = self.silence > RESET_AFTER
        self.due_evidence = committed & ((yr[rows, other] - yr[rows, hi]) > MARGIN)
        due = self.due_timeout | self.due_evidence
        rst = np.where(due, 10.0, 0.0)[:, None]
        self.silence = np.where(due, 0.0, self.silence)
        self.sel.step(yc, reset=rst)
        h = self.held()
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


def history(G, where, p=P0):
    """the registered bench input (same seeds), with the sensory history before the first hold"""
    n, steps = BENCH["rows"], BENCH["steps"]; rw = np.random.default_rng(BENCH["seed_w"])
    a = Agent4b(n, np.random.default_rng(BENCH["seed_a"]), where, G=G, known=np.tile([1.0, 0.0], (n, 1)))
    w = Still(n); on = np.ones(n, bool)
    fw = np.full((n, 2), -1); cnt = np.zeros((n, 2), int); first = np.full(n, -1); ft = np.full(n, -1)
    overlap = np.zeros(n, bool); rel = np.zeros(2, int); again = np.zeros(2, int); prev = np.full(n, -1)
    for t in range(steps):
        whiffs = rw.random((n, 2)) < p
        _, h = a.act(w, whiffs, on)
        fw = np.where((fw < 0) & whiffs, t, fw)
        nohold = first < 0; cnt[nohold] += whiffs[nohold]            # whiffs up to and including the first hold's step
        new = nohold & (h >= 0)
        first = np.where(new, h, first); ft = np.where(new, t, ft)
        overlap |= new & (a.y0.min(1) > 0.05)                         # the other channel's response present too
        rel += [int((a.due_evidence & ~a.due_timeout).sum()), int(a.due_timeout.sum())]   # releases fired, by kind
        again += [int(((prev == 1) & (h == 0)).sum()), int(((prev == 0) & (h == 1)).sum())]  # direct hold switches
        prev = np.where(h >= 0, h, np.where(prev >= 0, prev, -1))
    return dict(fw=fw, cnt=cnt, first=first, ft=ft, overlap=overlap, end=h, rel=rel, again=again)


def single_whiff(G, chan):
    """from rest, ONE whiff on `chan` then silence: peak of that channel's circuit state"""
    a = Agent4b(50, np.random.default_rng(3), "both", G=G, known=np.tile([1.0, 0.0], (50, 1)))
    w = Still(50); on = np.ones(50, bool); x = np.zeros((50, 2), bool); x[:, chan] = True; peak = 0.0
    for t in range(40):
        a.act(w, x if t == 0 else np.zeros((50, 2), bool), on); peak = max(peak, float(np.median(a.sel.s[:, chan])))
    return peak


def main():
    print(f"== H20 diagnosis after the G bench (measurement only). this file sha256 {hashlib.sha256(open(__file__, 'rb').read()).hexdigest()};"
          f" bench conditions {BENCH}; criterion rate p {P0} ==")
    print("\n(1) where the gain enters: bench variants with the gain in one place only")
    for G in CANDS:
        ref = bench(G, P0)["first"]
        for where in ("both", "circuit", "release"):
            r = history(G, where); held = r["first"] >= 0; nh = int(held.sum()); k = int((r["first"] == 0).sum())
            pt, lo, hi = ph15.wilson(k, nh)
            same = " (= registered bench)" if np.array_equal(r["first"], ref) else " (DIFFERS from the registered bench)" if where == "both" else ""
            e = r["end"]
            print(f"   G {G:3.1f} {where:8s}: first hold biased {k}/{nh} = {pt:.3f} [{lo:.3f}, {hi:.3f}]{same};"
                  f" end state over 400: biased {int((e == 0).sum())/4:.1f}% unbiased {int((e == 1).sum())/4:.1f}% none {int((e < 0).sum())/4:.1f}%;"
                  f" releases fired: evidence {r['rel'][0]} timeout {r['rel'][1]}; direct switches to biased {r['again'][0]}, to unbiased {r['again'][1]}")
    print("\n(1b) one whiff from rest: peak circuit state of that channel (threshold 1.0)")
    for G in CANDS:
        print(f"   G {G:3.1f}: biased channel {single_whiff(G, 0):.3f}  unbiased channel {single_whiff(G, 1):.3f}")
    print("\n(2) sensory history before the first hold, registered pathway (both), p 0.057")
    for G in CANDS:
        r = history(G, "both"); f, fw, cnt, ft = r["first"], r["fw"], r["cnt"], r["ft"]; held = f >= 0
        fwb, fwu = fw[:, 0], fw[:, 1]
        first_b = (fwb >= 0) & ((fwu < 0) | (fwb < fwu)); first_u = (fwu >= 0) & ((fwb < 0) | (fwu < fwb)); tie = (fwb >= 0) & (fwb == fwu)
        hb = f == 0; hu = f == 1
        pb = lambda m: f"{int((hb & m).sum())}/{int((held & m).sum())}"
        print(f"   G {G:3.1f}: first whiff on the biased channel {int(first_b.sum())}, unbiased {int(first_u.sum())}, same step {int(tie.sum())};"
              f" P(first hold biased | first whiff biased) {pb(first_b)}; P(first hold biased | first whiff unbiased) {pb(first_u)};"
              f" (| same step) {pb(tie)}")
        for name, m in (("hold = biased", hb), ("hold = unbiased", hu)):
            if not m.any(): print(f"      {name}: none"); continue
            cb, cu = cnt[m, 0], cnt[m, 1]
            print(f"      {name} ({int(m.sum())} rows): whiffs before the hold, biased median {med(cb):.0f} (mean {cb.mean():.2f}),"
                  f" unbiased median {med(cu):.0f} (mean {cu.mean():.2f}); rows with 0 whiffs of the OTHER channel before the hold"
                  f" {int(((cu if name == 'hold = biased' else cb) == 0).sum())}; held on its first own whiff {int(((cb if name == 'hold = biased' else cu) == 1).sum())};"
                  f" other response present at the hold {int(r['overlap'][m].sum())}; steps from the first whiff of any channel to the hold median"
                  f" {med(ft[m] - np.where(fw[m] < 0, 10**9, fw[m]).min(1)):.0f}")
    print("\n   reading key: arrival order limits the gain if the unbiased holds form with 0 biased whiffs before them;"
          " a circuit process limits it if they form after a biased whiff was already received")


if __name__ == "__main__":
    main()
