#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Avoidance check: the H25 release under supplied values +1/-1 (a check: readings, no verdict).

Usage: python ph24b.py      (self-checks, then the one run; output experiments/avoidance_check/ph24b_check.txt)

Design v1 FINAL (owner pre-approved, 2026-09-24): experiments/avoidance_check/avoidance_check_design_v1.md.
Measurement only. ph24 and every adopted module are imported unchanged. One hook: ph24.record is wrapped at run
time (the file is not edited) to store the flee side per step (FLEE); every other recorded field is untouched
(asserted in the self-checks). R0 identities, R1 priority check, R2 constructed negative hold then silence,
R3 the +1/-1 task arm. No new seed.
"""
import sys, os, hashlib
import numpy as np
import ph24, ph15
from ph24 import Agent10, Agent10g, Agent8, Agent6, run, stub, separation, bitwise, traj, events, on_hold, first_true, q3, header, BS, R, T, RESET_AFTER
from ph16 import Still, interval
from ph18 import majority
from ph21 import G_STAR

sys.stdout.reconfigure(newline="\n")
DESIGN = "experiments/avoidance_check/avoidance_check_design_v1.md"
EVAL = (1805, 1905)                 # H25 evaluation seeds, reused on purpose (R0, R3)
VALS = (1.0, -1.0)
def sha(p=__file__): return hashlib.sha256(open(p, "rb").read()).hexdigest()
PAIRS = (("Agent10", Agent10, "Agent8", Agent8), ("Agent10g", Agent10g, "Agent6", Agent6))

_record = ph24.record
def record(o, t, a, h, x, pa):                                    # the hook: ph24.record, plus the flee side
    _record(o, t, a, h, x, pa)
    if "FLEE" not in o: o["FLEE"] = np.zeros(o["H"].shape)
    o["FLEE"][t] = a.flee_side


def neg_held(o): return o["H"] == (1 - o["good"])[None, :] if "good" in o else o["H"] == 1
def viol(o): return int((neg_held(o) & (o["TGT"] != o["FLEE"])).sum())


def selfcheck():
    kw = dict(runs=40, steps=200)
    for _, cls, _, _ in PAIRS:
        ph24.record = _record; a = run("T1", cls, VALS, (5, 6), **kw)
        ph24.record = record; b = run("T1", cls, VALS, (5, 6), **kw)
        assert all(np.array_equal(a[k], b[k]) for k in a if isinstance(a[k], np.ndarray)), "the hook changed a recorded field"
    print("ok  the record hook leaves every field of ph24.run bitwise equal (World7 +1/-1, 40 x 200, seeds 5/6, both fix agents); FLEE recorded")


def R0():
    print("\n== R0 identities (reuse of the H25 evaluation seeds 1805/1905: a reproduction/identity check, not new evidence), World7 +1/-1, 400 x 600 ==")
    o = {k: run("T1", c, VALS, EVAL) for k, c in (("Agent10", Agent10), ("Agent8", Agent8), ("Agent10g", Agent10g), ("Agent6", Agent6))}
    oks = []
    for f, _, b, _ in PAIRS:
        ok, cnt = separation(o[f], o[b]); oks.append(ok); print(f"   {f} vs {b}: identity (b) class {ok} {cnt}")
    e86 = bitwise(o["Agent8"], o["Agent6"]); e10 = bitwise(o["Agent10"], o["Agent10g"])
    print(f"   Agent8 == Agent6 bitwise at +1/-1 (every field, counter included): {e86}; Agent10 == Agent10g bitwise: {e10}")
    lab = "identity holds" if all(oks) and e86 and e10 else "identity holds, cross-equality fails" if all(oks) else "identity broken"
    print(f"   R0 -> '{lab}' ({'clean' if lab == 'identity holds' else 'NOT clean'})")
    return lab == "identity holds", o


def R1():
    print("\n== R1 the H21 constructed-state priority check, release on (ph19.priority_check6 protocol: Still stub, 50 rows, generator 11, negative odour (channel 1) held s 2.0, both channels presented every step, G 2) ==")
    clean = True
    for steps in (20, 200):
        for f, fc, b, bc in PAIRS:
            out = {}
            for k, cls in ((f, fc), (b, bc)):
                a = cls(50, np.random.default_rng(11), G=G_STAR, known=np.tile([1.0, -1.0], (50, 1)), rule=True, **(dict(filt=True) if cls in (Agent10, Agent8) else {}))
                a.sel.s[:, 1] = 2.0; w = Still(50); tg, hh, fl = [], [], []
                for _ in range(steps):
                    _, h = a.act(w, np.ones((50, 2), bool), np.ones(50, bool)); tg.append(a.tgt.copy()); hh.append(h.copy()); fl.append(a.flee_side.copy())
                out[k] = (np.array(tg), np.array(hh), np.array(fl))
            (tf, hf, ff), (tb, hb, fb) = out[f], out[b]; neg = hf == 1
            flee_ok = bool((tf[neg] == ff[neg]).all()); same = bool(np.array_equal(tf, tb) and np.array_equal(hf, hb))
            lab = "priority kept, identical" if flee_ok and same else "priority kept, differs" if flee_ok else "priority violated"
            clean &= lab == "priority kept, identical"
            print(f"   {steps:3d} steps, {f} vs {b}: negative-held (row, step) {int(neg.sum())} (base {int((hb == 1).sum())}), flee target on every one {flee_ok};"
                  f" hold and target equal to the base on every step {same}; valued held {int((hf == 0).sum())}, nothing {int((hf < 0).sum())} -> '{lab}'")
    print(f"   R1 -> {'clean' if clean else 'NOT clean'}")
    return clean


def R2():
    print(f"\n== R2 constructed negative hold, then silence (ph24.stub, bench seeds {BS}, 400 rows, 200 steps, no input, channel 1 held s 2.0, +1/-1) ==")
    n = 400; r = np.arange(n); clean = True
    for f, fc, b, bc in PAIRS:
        o = stub(fc, [1.0, -1.0], [(200, 0.0, 0.0)], hold=1); ob = stub(bc, [1.0, -1.0], [(200, 0.0, 0.0)], hold=1)
        H, S = o["H"], o["S"]; end = first_true(H != 1); t = np.arange(200)[:, None]
        after = t >= np.where(end >= 0, end, 200)[None, :]; held = ~after
        above = np.array([bool((S[e:, i] > 1.0).any()) if e >= 0 else True for i, e in enumerate(end)])
        flee_held = ((o["TGT"] == o["FLEE"]) | ~held).all(0); flee_after = ~((H == 1) & after).any(0); coinc = (o["TGT"] == o["FLEE"]) & after
        rel = (end >= 0) & (end <= 49) & (S[np.maximum(end, 0), r] <= 1.0).all(1) & ~above & flee_held & flee_after
        ex47 = rel & (end == 47)
        k, pt, lo, hi = interval("P", ex47); k2, _, lo2, _ = interval("P", rel)
        lab = "released as valued holds" if lo >= 0.95 else "released, other step" if rel.all() else "not released"
        clean &= lab != "not released"
        dr = events(o)["drives"]; m = on_hold(dr); first = first_true(o["TO"])
        nxt = H[np.minimum(np.maximum(end, 0) + 1, 199), r]
        print(f"   {f}: exact at 47 {k}/{n} = {pt:.3f} [{lo:.3f}, {hi:.3f}]; released <= 49 with the circuit empty, no unit above 1.0 after, flee on every held step and the negative odour not held from the end step on {k2}/{n} [{lo2:.3f}];"
              f" after the end, steps whose cast target equals the flee side numerically {int(coinc.sum())} in {int(coinc.any(0).sum())} rows (since {q3(o['SINCE'][coinc])}; a coincidence of the cast formula, not the flee assignment);"
              f" end step {q3(end[end >= 0])} (never {int((end < 0).sum())}); first drive {q3(first[first >= 0])}; D {q3(dr['D'][m])}, max {dr['D'][m].max() if m.any() else 0};"
              f" after the release nothing held {int((H[-1] < 0).sum())}/{n} at step 199, held on the step after the end {np.bincount(nxt + 1, minlength=3).tolist()} (nothing/valued/negative);"
              f" base {b} holding the negative odour at 199 {int((ob['H'][-1] == 1).sum())}/{n} (flee target on every step {bool((ob['TGT'] == ob['FLEE']).all())}) -> '{lab}'")
    print(f"   R2 -> {'clean' if clean else 'NOT clean'}")
    return clean


def arm_stats(o):
    V, N, Z = majority(o); rr = np.arange(len(o["good"])); dn = o["AT2"][:, rr, 1 - o["good"]].sum(0).astype(float)
    lost = ~o["W"][-T//3:].any((0, 2)); return V, N, Z, dn, lost


def neg_events(o):
    """negative holds: formed, ended by the timeout drive / otherwise; the state after a drive-ended negative hold"""
    ev = events(o); dr = ev["drives"]; neg = 1 - o["good"]; m = on_hold(dr) & (dr["hp"] == neg[dr["r"]]) & dr["ended"]
    H = o["H"]; steps = H.shape[0]; renag, reval = 0, 0
    for e, r in zip(dr["end"][m], dr["r"][m]):
        seg = H[e:min(e + 60, steps), r]; renag += int((seg == neg[r]).any()); reval += int((seg == o["good"][r]).any())
    formed = int((ev["form"] & (H == neg[None, :])).sum()) + int((o["H0"] == neg).sum())
    prev = ev["prev"]; ended = (prev == neg[None, :]) & (H != prev)
    return dict(formed=formed, ended=int(ended.sum()), by_drive=int(m.sum()), next_nothing=int((H[dr["end"][m], dr["r"][m]] < 0).sum()),
                reheld_neg_60=renag, held_val_60=reval, flee_steps=int((neg_held(o) & (o["TGT"] == o["FLEE"])).sum()))


def R3(o):
    print("\n== R3 the +1/-1 task arm (World7, 1805/1905, 400 x 600; the runs of R0) ==")
    for k in o:
        V, N, Z, dn, lost = arm_stats(o[k]); kk, pt, lo, hi = interval("P", V)
        print(f"   [{k}] V {int(V.sum())} N {int(N.sum())} tie {int(Z.sum())}; P(V) {pt:.3f} [{lo:.3f}, {hi:.3f}]; dwell at the negative source mean {dn.mean():.3f} (quartiles {q3(dn)}, rows > 0 {int((dn > 0).sum())});"
              f" flee violations {viol(o[k])}; wall contacts per row {o[k]['contacts'].mean():.3f}; lost rows {int(lost.sum())}; negative holds {neg_events(o[k])}")
    labs = {}
    for f, _, b, _ in PAIRS:
        Vf, _, Zf, df, lf = arm_stats(o[f]); Vb, _, Zb, db, lb = arm_stats(o[b])
        _, dp, dlo, dhi = interval("DP", Vf.astype(float), Vb.astype(float)); _, dd, ddlo, ddhi = interval("DP", df, db)
        _, lp, llo, lhi = interval("DP", lf.astype(float), lb.astype(float)); _, cp, clo, chi = interval("DP", o[f]["contacts"], o[b]["contacts"])
        _, pf, wlo, _ = interval("P", Vf); pb = Vb.mean()
        vf, vb = viol(o[f]), viol(o[b]); c1, c2, c3 = vf == 0 and vb == 0, ddhi <= 2.0, dlo >= -0.05
        lit = wlo >= pb - 0.05
        lab = "unreadable" if Zf.mean() > 0.20 or Zb.mean() > 0.20 else "avoidance kept" if c1 and c2 and c3 else "avoidance changed"
        labs[f] = lab
        cls_f, cls_b = np.select([Vf, ~Vf & ~Zf], [0, 1], 2), np.select([Vb, ~Vb & ~Zb], [0, 1], 2)
        print(f"   {f} vs {b}: (i) flee violations {vf} / {vb} -> {c1}; (ii) paired dwell at the negative source {dd:+.3f} [{ddlo:+.3f}, {ddhi:+.3f}], upper bound <= +2.0 -> {c2};"
              f" (iii) paired DP P(V) {dp:+.4f} [{dlo:+.4f}, {dhi:+.4f}], lower bound >= -0.05 -> {c3} (literal reading: Wilson lower bound {wlo:.3f} >= {pb:.3f} - 0.05 -> {lit}"
              f"{'' if lit == c3 else ', DISAGREES with (iii)'}); into V {int(((cls_f == 0) & (cls_b != 0)).sum())}, out of V {int(((cls_f != 0) & (cls_b == 0)).sum())};"
              f" lost rows DP {lp:+.4f} [{llo:+.4f}, {lhi:+.4f}]; contacts DP {cp:+.4f} [{clo:+.4f}, {chi:+.4f}]; trajectory equal {traj(o[f], o[b])} -> '{lab}'")
    print(f"   R3 -> Agent10 vs Agent8 '{labs['Agent10']}' ({'clean' if labs['Agent10'] == 'avoidance kept' else 'NOT clean'}); Agent10g vs Agent6 '{labs['Agent10g']}' (reported)")
    return labs["Agent10"] == "avoidance kept"


def main():
    print(f"== Avoidance check (release under +1/-1). design {DESIGN} sha256 {sha(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', DESIGN))};"
          f" ph24b.py sha256 {sha()}; G {G_STAR}, gate on, C0; bootstrap seed {ph15.BOOT_SEED}; one run; no new seed ==")
    header()
    selfcheck(); ph24.record = record
    c0, o = R0(); c1 = R1(); c2 = R2(); c3 = R3(o)
    allc = c0 and c1 and c2 and c3
    print(f"\n== readings: R0 {'clean' if c0 else 'NOT clean'}, R1 {'clean' if c1 else 'NOT clean'}, R2 {'clean' if c2 else 'NOT clean'}, R3 {'clean' if c3 else 'NOT clean'} -> "
          + ("every reading clean (design section 3): the condition for decision:agent10-adopted is met" if allc else "NOT every reading clean: nothing adopted, the numbers go to the owner") + " ==")


if __name__ == "__main__":
    main()
