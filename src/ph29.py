#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H20 Stage B: a learned positive value in the adopted agent (Agent14), the H21 choice task.

Usage: python ph29.py demo | bench | dev | eval

Design: H20 Stage B design v2 FINAL, confirmed by the owner (decision:h20-stage-b-open, '권고안 적용', gloss 'apply the
recommended options'): doc d3f2ce9707790cd87, sha256 28c1010f...66ae, stored before this file existed. No relaxation, no new
state, no bar re-signed (design section 3.8). Composition only, nothing copied, no adopted module edited (ph4, ph8, ph11, ph14,
ph21, ph23, ph24, ph28 are imported unchanged; their sha256 is printed in every output header):
  the training (design 3.4) is the H15 E2 protocol (ph15.TRAIN 30 steps, ph15.GAP 50 silent steps, 30 steps; ph15.py:151-160)
  applied to the agent's own module a.mb with the agent's own codes a.codes, the NEUTRAL odour first and the valued odour second
  (reinforcement on compartment 1 for the trained group, none for the sham group); the read-out is the agent's own
  chan_valence() with known None (ph14.py:55), written into a.known (candidate A); tc and tr are cleared (ph15.py:160); the
  module is never called again. Everything else is ph28's harness (Agent14 = Release + Agent9, counter start 240, window 300).
Run-time hooks (no file edited): ph24.make and ph23.make are wrapped so that, while a training mode is set, the agent built by
the previous hook is trained and its read-out written into `known` right after construction and before the cast draw
(ph24.py:125-126, ph23.py:131-132); ph24's name Agent5 is replaced by a factory that builds ph17.Agent5 and applies the same
wrapper (ph24.run builds the fixed-hold agent directly, ph24.py:124); ph24.record is wrapped to check, at steps 0, 299 and
599, that the module is frozen (i6). With no training mode set, every hook returns the agent unchanged (checked in the demo).

Readings where the design is silent, chosen so that the identities stay exact (printed again in the bench output):
 (R1) The valued channel g of each row is taken from the +1/0 array the harness builds (ph24.py:122) for the arm; every trained
      or sham arm is run with vals (1, 0) and the wrapper asserts the pattern (exactly one 1 and one 0 per row). That array is
      the constructor's placeholder; the read-out replaces it (the constructor does not use `known`: identity (i2)).
 (R2) 'Bitwise on every field': Agent14 against Agent14, ph28's field list (ph24's identity fields + SIL, TO, EV, W, NAV6, NAV8,
      DIFF, DIFF8, PRES) plus P2 and C2; Agent14 against Agent10 (i4), ph24's identity fields + SIL, TO, EV (H26's a2); Agent8
      and Agent5 against themselves, every field of ph28's list that the run records.
 (R3) A row has an 'identical trajectory' when it is equal on POS, HEAD, H, NAV, SINCE, TGT and W over every step; (i3) is read
      on those rows: C2, P2, PRES, SIL, TO, EV, SUS and Z equal on every step.
 (R4) (i6): in the record hook, after the act of steps 0, steps/2 - 1 and steps - 1 (0, 299, 599 in a 600-step run), the live
      read-out stack(mb.valence(codes[:, 0]), mb.valence(codes[:, 1])) equals the read-out written at training exactly, mb.w
      equals the post-training weights and tc, tr are zero; every trained or sham arm of the run, in every world.
 (R5) (i7) and (g1): the masks are recomputed from the run's recorded state (H before the step's selection = the previous H, or
      H0; H after it; P2) with the learned values and with +1/0 in the same orientation, and compared on every (row, step):
      gate (ph23.py:66), top (ph23.py:88-89), keep (ph23.py:91), the H19 (a) mask v >= 0 (ph23.py:90) and the flee mask
      val < 0 (ph23.py:77).
 (R6) (g2): ph16b.single_whiff's measure (ph16b.py:84-90): a whiff on channel 1 at step 0 in every row and nothing after, 40
      steps, nothing held; peak = the maximum over steps of the median over rows of s of channel 1; 'holds' = channel 1 held on
      any step, per row; values (1.0, v_N) with v_N 0, 0.1, 0.2 (gains 1.0, 1.2, 1.4) and the bench's learned values.
 (R7) (h): the M2(a) pass probability at the bench DP (design section 7): b = the discordant fraction of the V indicator between
      the learned and the supplied arm, sd = sqrt(b - DP^2), se = sd / 20, P = Phi((DP + 0.05) / se - 1.96); sd 0: the point
      decides. STOP below 0.5.
 (R8) (i8): the supplied arm through this harness on 1985/2085 equals ph28.t1arm('adaptive') bitwise on every field (R2) and
      its V/N/tie and per-cell counts equal H26's recorded evaluation (371/28/1; cells 90/10/0, 95/5/0, 95/5/0, 91/8/1).
 (R9) The exactness claims of (t) (the no-candidate rule): v_V == 1.0 in every trained row; v_N > 0 in every trained row; both
      sham values exactly 0.0 in every row; compartments 0, 2, 3 unchanged (every weight 1.0) in both groups.
 (R10) ML is read per row on the seed's balance: trained v_V >= +0.5, 0 <= v_N <= +0.15, v_V > v_N; sham |v| <= 0.1 and v >= 0
      for both odours. (hL) STOP if more than 40 trained rows fail or any sham row fails.
 (R11) The learned Agent10g and pathway-off arms train their own modules on the same rows (the same read-out, deterministic);
      the known-answer arm is run at +1/0 and, for (i5), again with the learned read-out.
 (R12) dev and eval re-run the bench on the bench seeds for M4 (as ph28 did).
 (R13) Lost rows (M6(a)) = ph25.lost_t1 (no whiff of either plume in the last third).
Nothing changes after the table.
"""
import sys, os, re, math, hashlib
from contextlib import contextmanager
import numpy as np
import ph28                                              # hooks ph24.make / ph24.record / ph23.make (sets its own bootstrap seed)
import ph4, ph8, ph11, ph14, ph15, ph17, ph21, ph22, ph23, ph24, ph25, ph25b
from ph16 import World7, interval, crit, R, T, CELLS
from ph18 import majority, describe_majority, agg
from ph19 import h21_diag
from ph21 import G_STAR, q3, first_true, hold600
from ph23 import first_surge_ok, wv, wn
from ph24 import Agent10, Agent10g, Agent8, Agent6, bitwise, t3_dwell, ratio_boot, q3f
from ph25 import w1sum, lost_t1, binom_ge, cls3, construct_ok, qq
from ph28 import Agent14, ALLK, PR, pp_dp

sys.stdout.reconfigure(newline="\n")            # LF output, so the recorded sha256 equals the committed blob
DESIGN = "H20 Stage B v2 FINAL doc d3f2ce9707790cd87 hash 28c1010f29978b0389106e6b6a0d02a91ed3eb5b9c95be86557a723e30b966ae"
SEEDS = dict(dev=(9983, 9989), eval=(2005, 2107))
BENCH = dict(rows=400, rows_g3=800, p=0.30, steps_stub=200, steps_held=260, steps_g2=40, steps=600, seed_w=20261081, seed_a=20261082)
BS = (BENCH["seed_w"], BENCH["seed_a"])
REPRO = (1985, 2085)                             # H26's evaluation seeds, reused for (i8) only; NOT in the seed scan
H26_T1 = dict(V=371, N=28, tie=1, cells=((90, 10, 0), (95, 5, 0), (95, 5, 0), (91, 8, 1)))   # experiments/h26/ph28_eval.txt
ph15.BOOT_SEED = 20261083; ph15._idx.clear()     # design section 7 (after ph28's import set its own); the resample cache emptied
TRAIN, GAP = ph15.TRAIN, ph15.GAP                 # 30, 50 (ph15.py:24, :138)
MODS = (ph4, ph8, ph11, ph14, ph15, ph17, ph21, ph22, ph23, ph24, ph25, ph25b, ph28)
FULL = ALLK + ("P2", "C2")                        # reading R2
TRAJK = ("POS", "HEAD", "H", "NAV", "SINCE", "TGT", "W")                      # reading R3
CNTK = ("C2", "P2", "PRES", "SIL", "TO", "EV", "SUS", "Z")                    # reading R3
ML_BOUND = 40


def sha(p=__file__): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def Phi(x): return 0.5*(1.0 + math.erf(x/math.sqrt(2.0)))
def fx(x): return f"{x:.15g}"


# ------------------------------------------------------------------ the training and the read-out (design sections 3.3 A, 3.4)
def train(a, g, group, order="neutral-first"):
    """H15 E2 on the agent's own module: neutral code 30 steps, 50 silent steps, valued code 30 steps (reinforcement on compartment
    1 for 'trained', none for 'sham'); read-out by the agent's own chan_valence with known None; traces cleared. Returns (R, 2)."""
    rows = np.arange(a.R); cV, cN = a.codes[rows, g], a.codes[rows, 1 - g]
    z = np.zeros((a.R, a.mb.C)); rv = np.zeros((a.R, a.mb.C))
    if group == "trained": rv[:, 1] = 1.0                                   # reward is compartment 1 (ph15.py:60, :155)
    phases = [(cN, z), (cV, rv)] if order == "neutral-first" else [(cV, rv), (cN, z)]
    for i, (code, r) in enumerate(phases):
        for _ in range(TRAIN): a.mb.step(code=code, reinf=r)
        if i == 0:
            for _ in range(GAP): a.mb.step()                                # silent steps: traces decay (ph15.py:157-158)
    keep = a.known; a.known = None; v = a.chan_valence(); a.known = keep     # ph14.py:55, the live read-out
    a.mb.tc[:] = 0.0; a.mb.tr[:] = 0.0                                       # ph15.py:160
    return v


# ------------------------------------------------------------------ hooks (run time; no file edited)
_MODE = [None]      # None | 'learned' | 'sham' | 'learned->+1/0' | 'valued-first'
_make24, _make23, _record24 = ph24.make, ph23.make, ph24.record              # ph28's make, ph28's make23, ph25's record


def g_of(kv):
    """reading R1: the valued channel from the harness's +1/0 array"""
    g = (kv[:, 1] == 1.0).astype(int); rows = np.arange(len(g))
    assert (kv[rows, g] == 1.0).all() and (kv[rows, 1 - g] == 0.0).all(), "a trained arm must be run with vals (1, 0)"
    return g


def post(a, kv):
    m = _MODE[0]
    if m is None: return a
    g = g_of(kv); v = train(a, g, "sham" if m == "sham" else "trained", "valued-first" if m == "valued-first" else "neutral-first")
    a.known = kv if m == "learned->+1/0" else v
    a._ph29 = dict(w=a.mb.w.copy(), v=v.copy(), g=g.copy(), mode=m)
    READOUT[0] = dict(v=v.copy(), g=g.copy(), codes=a.codes.copy(), mode=m)
    return a


READOUT = [None]


def make(cls, runs, rng, G, known, gate=True, filt=True, release=True): return post(_make24(cls, runs, rng, G, known, gate, filt, release), known)
def make23(cls, runs, rng, G, known, gate, filt, scope="prior"): return post(_make23(cls, runs, rng, G, known, gate, filt, scope), known)
def agent5(runs, rng, **kw): return post(ph17.Agent5(runs, rng, **kw), kw["known"])


def record(o, t, a, h, x, pa):
    _record24(o, t, a, h, x, pa)
    d = getattr(a, "_ph29", None)
    if d is not None and t in (0, o["steps"]//2 - 1, o["steps"] - 1):                        # reading R4
        live = np.stack([a.mb.valence(a.codes[:, 0]), a.mb.valence(a.codes[:, 1])], 1)
        ok = bool(np.array_equal(live, d["v"]) and np.array_equal(a.mb.w, d["w"]) and not a.mb.tc.any() and not a.mb.tr.any())
        o.setdefault("FROZEN", []).append((t, ok))


ph24.make, ph23.make, ph24.Agent5, ph24.record = make, make23, agent5, record


@contextmanager
def mode(m):
    keep = _MODE[0]; _MODE[0] = m
    try: yield
    finally: _MODE[0] = keep


VALS = {"supplied": (None, (1.0, 0.0)), "learned": ("learned", (1.0, 0.0)), "sham": ("sham", (1.0, 0.0)), "learned->+1/0": ("learned->+1/0", (1.0, 0.0)),
        "zero": (None, (0.0, 0.0)), "valued-first": ("valued-first", (1.0, 0.0))}


def run(world, cls, val, seeds, **kw):
    m, vals = VALS[val]
    with mode(m): return ph28.run(world, cls, vals, seeds, **kw)


def stub(cls, val, sched, **kw):
    """val: a VALS key (trained groups: channel 0 valued) or a known pair (supplied)"""
    kw.setdefault("seeds", BS)
    if isinstance(val, str): m, known = VALS[val]
    else: m, known = None, val
    with mode(m): return ph28.stub(cls, list(known), sched, **kw)


def frozen_ok(o): return bool(o.get("FROZEN")) and all(ok for _, ok in o["FROZEN"])


def mk14(n, seed_a, kv):
    """an Agent14 as ph24.run builds it (ph28's make), no training"""
    with mode(None): return ph24.make(Agent14, n, np.random.default_rng(seed_a), G_STAR, kv, True, True, True)


# ------------------------------------------------------------------ measures
def stepeq(o1, o2, ks):
    """(steps, rows): equal on every field in ks at that step"""
    eq = np.ones(o1["H"].shape, bool)
    for k in ks:
        if k not in o1 or k not in o2: continue
        e = np.asarray(o1[k]) == np.asarray(o2[k]); eq &= e.reshape(e.shape[0], e.shape[1], -1).all(2)
    return eq


def roweq(o1, o2, ks): return stepeq(o1, o2, ks).all(0)


def overlap(codes): return (codes[:, 0]*codes[:, 1]).sum(1).astype(int)


def masks(o, v):
    """reading R5: the order-dependent masks recomputed from the recorded state with values v (R, 2)"""
    H = o["H"].astype(int); steps, n = H.shape; rows = np.arange(n)[None, :]
    HP = np.vstack([np.asarray(o["H0"], int)[None, :], H[:-1]]); P2 = o["P2"]; ge = v >= 0
    vhp = v[rows, np.maximum(HP, 0)]; gate = (HP >= 0)[:, :, None] & ge[None] & (v[None] < vhp[:, :, None])
    vmax = np.where(P2, v[None], -np.inf).max(2); top = P2 & ge[None] & (v[None] == vmax[:, :, None])
    vh = v[rows, np.maximum(H, 0)]; keep = (H >= 0) & ((vh == vmax) | (vh < 0)); flee = (H >= 0) & (vh < 0)
    return dict(gate=gate, top=top, keep=keep, h19=np.broadcast_to(ge[None], P2.shape), flee=flee)


def masks_equal(o, v, g):
    """per row: every mask with v equal to the mask with +1/0 in the same orientation, on every step"""
    n = len(g); r = np.arange(n); kv = np.zeros((n, 2)); kv[r, g] = 1.0
    a, b = masks(o, v), masks(o, kv); ok = np.ones(n, bool); per = {}
    for k in a:
        e = (a[k] == b[k]).reshape(a[k].shape[0], n, -1).all((0, 2)); per[k] = int(e.sum()); ok &= e
    return ok, per


def ml_check(vt, vs, g):
    """reading R10. vt, vs: (R, 2) trained and sham read-outs per channel. Returns per-row pass masks by clause."""
    r = np.arange(len(g)); vV, vN = vt[r, g], vt[r, 1 - g]; sV, sN = vs[r, g], vs[r, 1 - g]
    c = dict(vV=vV >= 0.5, vN=(vN >= 0.0) & (vN <= 0.15), order=vV > vN)
    t_ok = c["vV"] & c["vN"] & c["order"]; s_ok = (np.abs(sV) <= 0.1) & (sV >= 0) & (np.abs(sN) <= 0.1) & (sN >= 0)
    return t_ok, s_ok, c, vV, vN, sV, sN


def agent_state(a):
    """(i1): every array, number and flag of the agent and of its upstream stage, circuit, ring and module, and the generator state"""
    st = {}
    for pre, obj in (("", a), ("up.", a.up), ("sel.", a.sel), ("ring.", a.ring), ("mb.", a.mb)):
        for k, x in vars(obj).items():
            if isinstance(x, np.ndarray) or isinstance(x, (int, float, bool, str, np.number)) or x is None: st[pre + k] = x
    st["rng"] = a.rng.bit_generator.state
    return st


def state_diff(s1, s2):
    out = []
    for k in sorted(set(s1) | set(s2)):
        x, y = s1.get(k, "<absent>"), s2.get(k, "<absent>")
        same = np.array_equal(x, y) if isinstance(x, np.ndarray) or isinstance(y, np.ndarray) else x == y
        if not same: out.append(k)
    return out


def pp_m2a(Vl, Vs):
    """reading R7"""
    dp = float(Vl.mean() - Vs.mean()); b = float((Vl != Vs).mean()); return pp_dp(dp, b, bar=-0.05), dp, b


def uniq(x):
    u, c = np.unique(x, return_counts=True); return ", ".join(f"{fx(a)} x{b}" for a, b in zip(u, c))


def readings(say):
    say("   readings where the design is silent (file header R1-R13): R1 g from the harness's +1/0 array (asserted), the placeholder replaced by the read-out;"
        " R2 bitwise = ph28's fields + P2, C2 (Agent14 vs Agent14), ph24's fields + SIL, TO, EV (vs Agent10); R3 identical trajectory = POS, HEAD, H, NAV, SINCE,"
        " TGT, W equal on every step, (i3) on those rows: C2, P2, PRES, SIL, TO, EV, SUS, Z; R4 (i6) live read-out == written read-out, mb.w == post-training,"
        " tc = tr = 0 at steps 0, steps/2 - 1, steps - 1; R5 masks (gate, top, keep, H19 (a) v >= 0, flee val < 0) recomputed from the recorded state with the"
        " learned values and with +1/0; R6 (g2) ph16b.single_whiff's measure (median over rows, max over 40 steps), a channel-1 whiff at step 0; R7 (h) b = discordant"
        " fraction of V, sd = sqrt(b - DP^2), se = sd/20, Phi((DP + 0.05)/se - 1.96), STOP below 0.5; R8 (i8) == ph28.t1arm('adaptive') bitwise and == H26's recorded"
        " counts; R9 exactness: v_V == 1.0, v_N > 0 (trained), sham == 0.0, compartments 0, 2, 3 all 1.0; R10 ML per row, (hL) STOP above 40 trained failures or any"
        " sham failure; R11 learned Agent10g and pathway-off train their own modules (same read-out); known-answer at +1/0, again with the learned read-out for (i5);"
        " R12 dev/eval re-run the bench for M4; R13 lost rows = ph25.lost_t1")


# ------------------------------------------------------------------ the mechanism bench (design section 4)
def bench(say=print):
    n = BENCH["rows"]; st = BENCH["steps"]; p = BENCH["p"]; ids, exact, out = {}, {}, {}
    say(f"== H20 Stage B mechanism bench (design v2 FINAL section 4). design {DESIGN}; {BENCH}; TRAIN {TRAIN}, GAP {GAP}; bootstrap seed {ph15.BOOT_SEED} ==")
    header(say); readings(say)
    say("   construction order in every trained or sham arm: world, mask, twin, values (+1/0 placeholder), agent, TRAINING on a.mb + read-out into a.known, cast draw, position, hold")
    # ---- (t) the learned values, no task
    w = World7(n, np.random.default_rng(BS[0]), BS[0]); g = w.good; cell = w.cell; r = np.arange(n); kv = np.zeros((n, 2)); kv[r, g] = 1.0
    grp = {}
    for name, grp_, order in (("trained", "trained", "neutral-first"), ("sham", "sham", "neutral-first"), ("valued-first", "trained", "valued-first")):
        a = mk14(n, BS[1], kv.copy()); v = train(a, g, grp_, order); grp[name] = (a, v)
    at, vt = grp["trained"]; asm, vs = grp["sham"]; av, vr = grp["valued-first"]; u = overlap(at.codes)
    t_ok, s_ok, cl, vV, vN, sV, sN = ml_check(vt, vs, g)
    say(f"(t) training (H15 E2: neutral {TRAIN} steps, {GAP} silent, valued {TRAIN} steps; reward on compartment 1 in the trained group), bench world seed's balance, {n} rows:")
    say(f"      u (units shared by the two codes of a row): " + ", ".join(f"u={k}: {int((u == k).sum())}" for k in range(int(u.max()) + 1))
        + " (hypergeometric expectation about 237 / 131 / 29 / 4 for 0 / 1 / 2 / >= 3)")
    say(f"      per-cell counts of u: " + " | ".join(f"cell {c}: " + "/".join(str(int(((cell == c) & (u == k)).sum())) for k in range(int(u.max()) + 1)) for c in range(4)))
    say(f"      trained v_V: quartiles {fx(np.percentile(vV, 25))}/{fx(np.median(vV))}/{fx(np.percentile(vV, 75))}; by value: {uniq(vV)}")
    say(f"      trained v_N: quartiles {fx(np.percentile(vN, 25))}/{fx(np.median(vN))}/{fx(np.percentile(vN, 75))}; by value: {uniq(vN)}")
    say("      cross-table u x v_N (trained): " + " | ".join(f"u={k}: {uniq(vN[u == k])}" for k in range(int(u.max()) + 1) if (u == k).any()))
    say(f"      design 3.4 inferred: u=0 about +7.1e-6, u=1 about +0.1000064; measured u=0 {uniq(vN[u == 0]) if (u == 0).any() else 'n/a'}; u=1 {uniq(vN[u == 1]) if (u == 1).any() else 'n/a'}")
    say(f"      sham: v_V by value {uniq(sV)}; v_N by value {uniq(sN)}")
    w0 = {k: bool((a.mb.w[:, [0, 2, 3]] == 1.0).all()) for k, (a, _) in grp.items()}
    exact["v_V == 1.0 in every trained row"] = bool((vV == 1.0).all()); exact["v_N > 0 in every trained row"] = bool((vN > 0).all())
    exact["sham values exactly 0.0"] = bool((vs == 0.0).all()); exact["compartments 0, 2, 3 unchanged (trained, sham)"] = w0["trained"] and w0["sham"]
    say(f"      exactness claims (reading R9): " + "; ".join(f"{k} {v}" for k, v in exact.items()) + f"; rows with v_N < 0 (trained) {int((vN < 0).sum())}")
    nf = int((~t_ok).sum()); nsf = int((~s_ok).sum()); stop_hl = nf > ML_BOUND or nsf > 0
    say(f"   (t) ML (design section 7, reading R10): trained rows failing {nf}/{n} (v_V >= 0.5 fails {int((~cl['vV']).sum())}; 0 <= v_N <= 0.15 fails {int((~cl['vN']).sum())}"
        f" (v_N < 0 {int((vN < 0).sum())}, v_N > 0.15 {int((vN > 0.15).sum())}); v_V > v_N fails {int((~cl['order']).sum())}); by cell " + "/".join(str(int(((cell == c) & ~t_ok).sum())) for c in range(4))
        + f"; failing rows by u " + ", ".join(f"u={k}: {int(((u == k) & ~t_ok).sum())}" for k in range(int(u.max()) + 1)) + f"; sham rows failing {nsf}/{n}")
    say(f"   (hL) STOP RULE (design section 4): ML {'UNREADABLE' if stop_hl else 'readable'} ({nf} trained failures against the bound {ML_BOUND}; {nsf} sham failures)"
        f" -> {'STOP: the run returns to the owner after the bench record' if stop_hl else 'continue'}")
    rN = vr[r, 1 - g]; rV = vr[r, g]
    say(f"      printed beside, not used by any arm: valued FIRST: v_V by value {uniq(rV)}; v_N at u=0 {uniq(rN[u == 0]) if (u == 0).any() else 'n/a'} (negative in {int((rN[u == 0] < 0).sum())}/{int((u == 0).sum())} u=0 rows;"
        f" design 3.4 infers about -2.8e-6); v_N at u=1 {uniq(rN[u == 1]) if (u == 1).any() else 'n/a'}; rows with v_N < 0 {int((rN < 0).sum())}/{n}")
    out.update(u=u, vV=vV, vN=vN, ml_fail=nf, sham_fail=nsf, stop_hl=stop_hl)
    # ---- (i1)
    a0 = mk14(n, BS[1], np.zeros((n, 2))); s0 = agent_state(a0)
    a1 = mk14(n, BS[1], np.zeros((n, 2))); a1.known = train(a1, g, "trained"); d1 = state_diff(agent_state(a1), s0)
    a2 = mk14(n, BS[1], np.zeros((n, 2))); a2.known = train(a2, g, "sham"); d2 = state_diff(agent_state(a2), s0)
    ids["i1 trained agent differs from an untrained one only in known and mb.w"] = d1 == ["known", "mb.w"]; ids["i1 sham agent == untrained (placeholder 0/0)"] = d2 == []
    say(f"(i1) training leaves the agent untouched except mb.w (and the read-out in known): trained agent vs untrained, differing state {d1} -> {d1 == ['known', 'mb.w']};"
        f" sham vs untrained (placeholder zeros) {d2} -> {d2 == []}; {len(s0)} state entries compared incl. the generator state")
    # ---- (i2) (i4) stubs
    both = [(BENCH["steps_stub"], p, p)]; alone = [(BENCH["steps_held"], p, 0.0)]
    i2s = {"both p 0.30": bitwise(stub(Agent14, "learned->+1/0", both), stub(Agent14, (1.0, 0.0), both), FULL),
           "channel 0 alone": bitwise(stub(Agent14, "learned->+1/0", alone), stub(Agent14, (1.0, 0.0), alone), FULL),
           "channel 1 held": bitwise(stub(Agent14, "learned->+1/0", both, hold=1), stub(Agent14, (1.0, 0.0), both, hold=1), FULL)}
    T = {"learned": run("T1", Agent14, "learned", BS)}; rlT = READOUT[0]
    T.update({k: run("T1", Agent14, k, BS) for k in ("supplied", "sham", "learned->+1/0", "zero")})
    T["Agent10 0/0"] = run("T1", Agent10, "zero", BS)
    ids["i2 stub"] = all(i2s.values()); ids["i2 World7 T1"] = bitwise(T["learned->+1/0"], T["supplied"], FULL)
    say(f"(i2) the learned agent with known overwritten by +1/0 == the supplied Agent14 bitwise on every field: stub " + "; ".join(f"{k} {v}" for k, v in i2s.items())
        + f"; World7 T1 {n} x {st} {ids['i2 World7 T1']}")
    s_sh = stub(Agent14, "sham", both); ids["i4 stub"] = bitwise(s_sh, stub(Agent14, (0.0, 0.0), both), FULL) and bitwise(s_sh, stub(Agent10, (0.0, 0.0), both))
    ids["i4 World7 T1"] = bitwise(T["sham"], T["zero"], FULL) and bitwise(T["sham"], T["Agent10 0/0"])
    say(f"(i4) sham == Agent14 at 0/0 (every field) == Agent10 at 0/0 (ph24's fields): stub {ids['i4 stub']}; World7 T1 {ids['i4 World7 T1']}")
    L, S = T["learned"], T["supplied"]; tr_eq = roweq(L, S, TRAJK); ceq = roweq(L, S, CNTK)
    ids["i3 counter and release fields equal on trajectory-identical rows"] = bool((ceq | ~tr_eq).all())
    say(f"(i3) T1 learned vs supplied: rows with an identical trajectory (reading R3) {int(tr_eq.sum())}/{n}; of them counter and release fields equal on every step"
        f" {int((ceq & tr_eq).sum())} -> {ids['i3 counter and release fields equal on trajectory-identical rows']}")
    # ---- (i5)
    po_l = run("T1", Agent8, "learned", BS, G=0.0, gate=False, filt=False); po_s = run("T1", Agent8, "supplied", BS, G=0.0, gate=False, filt=False)
    ka_l = run("T1", None, "learned", BS, G=0.0, gate=False, filt=False, fixed="valued"); ka_s = run("T1", None, "supplied", BS, G=0.0, gate=False, filt=False, fixed="valued")
    ids["i5 pathway-off learned == +1/0"] = bitwise(po_l, po_s, FULL); ids["i5 known-answer learned == +1/0"] = bitwise(ka_l, ka_s, FULL)
    say(f"(i5) pathway-off (Agent8 G 0, gate off, filter off) with the learned values == with +1/0 bitwise: {ids['i5 pathway-off learned == +1/0']};"
        f" known-answer (Agent5 fixed valued, G 0) with the learned values == with +1/0: {ids['i5 known-answer learned == +1/0']}")
    # ---- (i6) (i7)
    Tg = {"Agent10g learned": run("T1", Agent10g, "learned", BS, filt=False)}
    fr = {"learned": L, "sham": T["sham"], "learned->+1/0": T["learned->+1/0"], "pathway-off learned": po_l, "known-answer learned": ka_l, **Tg}
    ids["i6 frozen (T1, every trained or sham arm)"] = all(frozen_ok(o) for o in fr.values())
    say(f"(i6) the module is frozen during the test (reading R4; steps 0, 299, 599): " + "; ".join(f"{k} {frozen_ok(o)}" for k, o in fr.items()))
    mk_ok, per = masks_equal(L, rlT["v"], L["good"]); ids["i7 masks equal +1/0 masks on every (row, step), learned T1"] = bool(mk_ok.all())
    say(f"(i7) T1 learned run: gate, top, keep, H19 (a), flee masks with the learned values == with +1/0 on every (row, step): rows equal per mask {per}; all rows {int(mk_ok.sum())}/{n}"
        f" -> {bool(mk_ok.all())}; the run's read-out equals (t)'s trained read-out {bool(np.array_equal(rlT['v'], vt))}")
    # ---- (i8)
    rs = run("T1", Agent14, "supplied", REPRO); r28 = ph28.t1arm("adaptive", REPRO); V_, N_, Z_ = majority(rs); c_ = rs["cell"]
    cells = tuple((int(V_[c_ == c].sum()), int(N_[c_ == c].sum()), int(Z_[c_ == c].sum())) for c in range(4))
    i8 = bitwise(rs, r28, FULL) and (int(V_.sum()), int(N_.sum()), int(Z_.sum())) == (H26_T1["V"], H26_T1["N"], H26_T1["tie"]) and cells == H26_T1["cells"]
    ids["i8 reproduction of the H26 T1 (1985/2085)"] = i8
    say(f"(i8) reproduction on H26's evaluation seeds {REPRO} (reading R8): this harness's supplied Agent14 == ph28.t1arm('adaptive') bitwise {bitwise(rs, r28, FULL)};"
        f" V/N/tie {int(V_.sum())}/{int(N_.sum())}/{int(Z_.sum())} (recorded {H26_T1['V']}/{H26_T1['N']}/{H26_T1['tie']}); cells {cells} (recorded {H26_T1['cells']})"
        f" -> {i8}")
    # ---- (g) constructed states
    rows_g = n; lstub = stub(Agent14, "learned", both); lv = READOUT[0]["v"]
    say(f"(g) the pathway at the learned magnitudes (stub, {rows_g} rows, channel 0 valued); the stub's learned read-out: v_0 by value {uniq(lv[:, 0])}; v_1 by value {uniq(lv[:, 1])}")
    g1 = {}
    for lab, val in (("v_N 7.1e-6", (1.0, 7.1e-6)), ("v_N 0.1", (1.0, 0.1)), ("v_N 0.2", (1.0, 0.2)), ("learned", "learned")):
        for sl, kw in (("both p 0.30", {}), ("channel 1 held", dict(hold=1))):
            o = lstub if (val == "learned" and not kw) else stub(Agent14, val, both, **kw)
            v = READOUT[0]["v"] if val == "learned" else np.tile(val, (rows_g, 1))
            ok, per = masks_equal(o, v, np.zeros(rows_g, int)); g1[f"{lab}, {sl}"] = bool(ok.all())
            say(f"      (g1) {lab}, {sl}: masks equal +1/0's on every (row, step) in {int(ok.sum())}/{rows_g} rows (per mask {per})")
    ids["g1 masks order-only (stub)"] = all(g1.values())
    say(f"   (g1) all constructed states: {ids['g1 masks order-only (stub)']}")
    one = [(1, 0.0, 1.0), (BENCH["steps_g2"] - 1, 0.0, 0.0)]
    for lab, val in (("gain 1.0 (v_N 0)", (1.0, 0.0)), ("gain 1.2 (v_N 0.1)", (1.0, 0.1)), ("gain 1.4 (v_N 0.2)", (1.0, 0.2)), ("learned values", "learned")):
        o = stub(Agent14, val, one); s1 = o["S"][:, :, 1]; peak = float(np.median(s1, 1).max()); held = (o["H"] == 1).any(0)
        pr = s1.max(0); extra = ""
        if val == "learned":
            uu = overlap(READOUT[0]["codes"]); extra = "; by u: " + ", ".join(f"u={k}: holds {int((held & (uu == k)).sum())}/{int((uu == k).sum())}, peak median {np.median(pr[uu == k]):.3f}" for k in range(int(uu.max()) + 1) if (uu == k).any())
        say(f"      (g2) one neutral whiff at step 0, nothing held, {lab}: peak of the median s (threshold 1.0) {peak:.3f}; per-row peak quartiles {q3f(pr, '.3f')};"
            f" rows holding the neutral odour on some step {int(held.sum())}/{rows_g}{extra}" + (f"; H20's 0.756 reproduced: {round(peak, 3) == 0.756}" if lab.startswith("gain 1.0") else ""))
    nc = BENCH["rows_g3"]; g3 = {}
    for lab, val in (("learned", "learned"), ("supplied", "supplied")):
        m, vals = VALS[val]
        with mode(m), ph28.n11(60): g3[lab] = ph23.run("T1", Agent14, vals, BS, runs=nc, start="variant", hold=True)
    for lab, o in g3.items():
        k_, pt_, l_, h_ = interval("P", hold600(o)); say(f"      (g3) task-like neutral-hold start (H23 bench (b)), {nc} rows x {st}, REPORTED: {lab} Agent14 holding the valued odour at step {st} {k_}/{nc} = {pt_:.3f} [{l_:.3f}, {h_:.3f}]")
    _, dp3, l3, h3 = interval("DP", hold600(g3["learned"]).astype(float), hold600(g3["supplied"]).astype(float))
    say(f"      (g3) paired DP learned - supplied {dp3:+.4f} [{l3:+.4f}, {h3:+.4f}]; rows with an identical trajectory {int(roweq(g3['learned'], g3['supplied'], ('POS', 'HEAD', 'H', 'NAV', 'SINCE', 'TGT', 'W')).sum())}/{nc}")
    # ---- (h) T1 on bench seeds, the stop rule
    arms = {"learned": L, "supplied": S, "sham": T["sham"], "Agent10g learned": Tg["Agent10g learned"], "pathway-off learned": po_l, "known-answer": ka_s, "Agent10": run("T1", Agent10, "supplied", BS)}
    mj = {k: majority(o) for k, o in arms.items()}
    say(f"(h) T1 on bench seeds, World7 {n} x {st}: " + "; ".join(f"{k} V {int(m_[0].sum())} N {int(m_[1].sum())} tie {int(m_[2].sum())} P(V) {interval('P', m_[0])[1]:.3f}"
        f" [{interval('P', m_[0])[2]:.3f}, {interval('P', m_[0])[3]:.3f}]" for k, m_ in mj.items()))
    Vl, Vs = mj["learned"][0], mj["supplied"][0]; cl_, cs_ = cls3(L), cls3(S)
    _, dp, dlo, dhi = interval("DP", Vl.astype(float), Vs.astype(float)); ppa, dpa, b = pp_m2a(Vl, Vs); stop_h = ppa < 0.5
    se = stepeq(L, S, TRAJK); fd = first_true(~se); dep = fd >= 0
    say(f"   (h) paired DP P(V) learned - supplied {dp:+.4f} [{dlo:+.4f}, {dhi:+.4f}] (bootstrap 5000, seed {ph15.BOOT_SEED}); into V {int((Vl & ~Vs).sum())}, out of V {int((~Vl & Vs).sum())};"
        f" outcome class changed {int((cl_ != cs_).sum())} rows; rows bitwise on every field {int(roweq(L, S, FULL).sum())}")
    say(f"   (h) rows with an identical trajectory (reading R3) by u: " + ", ".join(f"u={k}: {int((~dep & (u == k)).sum())}/{int((u == k).sum())}" for k in range(int(u.max()) + 1))
        + f"; departing rows {int(dep.sum())}, by u " + ", ".join(f"u={k}: {int((dep & (u == k)).sum())}" for k in range(int(u.max()) + 1))
        + f"; first departing step {q3(fd[dep]) if dep.any() else 'n/a'}; rows changing outcome by u " + ", ".join(f"u={k}: {int(((cl_ != cs_) & (u == k)).sum())}" for k in range(int(u.max()) + 1)))
    Vsh, Vg = mj["sham"][0], mj["Agent10g learned"][0]
    ppb = pp_dp(float(Vl.mean() - Vsh.mean()), float((Vl != Vsh).mean()), bar=0.20); ppd = pp_dp(float(Vl.mean() - Vg.mean()), float((Vl != Vg).mean()), bar=0.05)
    cellp = [interval("P", Vl[L["cell"] == c]) for c in range(4)]
    say(f"   (h) pass probabilities at the bench values (design section 7 arithmetic, reading R7): M2(a) at DP {dpa:+.4f}, discordant fraction b {b:.4f}, sd {math.sqrt(max(b - dpa*dpa, 0.0)):.4f}: {ppa:.4f};"
        f" M2(b) learned - sham at DP {float(Vl.mean() - Vsh.mean()):+.4f}: {ppb:.4f}; M2(d) learned - learned Agent10g at DP {float(Vl.mean() - Vg.mean()):+.4f}: {ppd:.4f};"
        f" cells learned P(V) " + ", ".join(f"{c[0]}/100 [{c[2]:.3f}, {c[3]:.3f}]" for c in cellp) + f"; the 0.88 line (reported, not a bar) P(k >= 365 of 400) at {Vl.mean():.3f}: {binom_ge(Vl.mean()):.4f}")
    say(f"   (h) STOP RULE (design section 4, section 12 point 5): M2(a) pass probability {ppa:.4f} {'< 0.5 -> STOP: the run returns to the owner after the bench record' if stop_h else '>= 0.5 -> continue'}")
    out.update(dp=dp, dlo=dlo, dhi=dhi, pp_a=ppa, stop_h=stop_h, P=dict((k, float(m_[0].mean())) for k, m_ in mj.items()))
    idok = all(ids.values()); exok = all(exact.values()); nocand = not (idok and exok); stop = stop_h or stop_hl
    verdict = idok and exok and not stop; out.update(stop=stop, nocand=nocand)
    say(f"== M4: identities {idok}; failed {[k for k, v in ids.items() if not v]}; exactness claims of (t) {exok}; failed {[k for k, v in exact.items() if not v]}; (h) {'STOP' if stop_h else 'continue'};"
        f" (hL) {'STOP' if stop_hl else 'continue'} -> M4 {'PASS: the tasks may be run' if verdict else ('FAIL, NO CANDIDATE: the design reading is wrong there; the tasks are NOT run' if nocand else 'STOPPED by a stop rule: the tasks are NOT run; the owner decides')}; (g2), (g3) reported ==")
    return verdict, out


# ------------------------------------------------------------------ self-checks
def seeds_unused():
    """design section 9: none of the fifteen numbers appears in any other file under the repository (recursive, digit-boundary; .git and
    __pycache__ excluded; excluded by name: this file, its outputs ph29_*.txt, the Stage B documents h20_stage_b_*.md, master_plan.md,
    notes/*.md, viewer/*). The demo seeds 5/6 and the reproduction seeds 1985/2085 are used deliberately and are NOT part of this check."""
    base = [*SEEDS["dev"], *SEEDS["eval"], BENCH["seed_w"], BENCH["seed_a"], ph15.BOOT_SEED]
    derived = [s + 10_000 for s in (SEEDS["dev"][0], SEEDS["eval"][0], BENCH["seed_w"])] + [s + 20_000 for s in (SEEDS["dev"][1], SEEDS["eval"][1], BENCH["seed_a"])]
    nums = base + derived + [BENCH["seed_w"] + 10_000_000, BENCH["seed_a"] + 20_000_000]
    pat = re.compile(rb"(?<!\d)(" + "|".join(map(str, nums)).encode() + rb")(?!\d)"); hits = []; nf = 0
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        top = os.path.relpath(root, repo).replace("\\", "/").split("/")[0]
        for f in files:
            if f == "ph29.py" or (f.startswith("ph29_") and f.endswith(".txt")) or (f.startswith("h20_stage_b_") and f.endswith(".md")) or f == "master_plan.md": continue
            if (os.path.basename(root) == "notes" and f.endswith(".md")) or top == "viewer": continue
            nf += 1
            if pat.search(open(os.path.join(root, f), "rb").read()): hits.append(os.path.relpath(os.path.join(root, f), repo))
    return hits, nums, nf


def header(say=print):
    say(f"   ph29.py sha256 {sha()}; design {DESIGN}")
    say("   imported modules: " + "; ".join(f"{os.path.basename(m.__file__)} {sha(m.__file__)}" for m in MODS))
    say(f"   seeds: dev {SEEDS['dev']}, eval {SEEDS['eval']}, bench {BS}, bootstrap {ph15.BOOT_SEED}; reproduction (i8) on H26's {REPRO} only; demo seeds (5, 6) used deliberately;"
        f" neither is part of the seed scan")
    say("   decisions: decision:h20-stage-b-open (no relaxation, no bar re-sign); the adopted agent: decision:h26-adaptive-presence-adopted-within-tested-conditions")


def demo():
    print(f"== H20 Stage B self-checks (demo). design {DESIGN} ==")
    header()
    print("   fixed before this recorded demo: none. One earlier run of this demo (the code-path test) passed every check; only the print precision of the value counts (7 -> 15 significant digits) changed after it")
    n, st = 40, 200; kw = dict(runs=n, steps=st); sd = (5, 6); sp = [(st, 0.30, 0.30)]; kn = [1.0, 0.0]; v10 = (1.0, 0.0)
    hooked = (ph24.make, ph23.make, ph24.Agent5, ph24.record)
    for cls, kk in ((Agent14, {}), (Agent10, {}), (Agent10g, dict(filt=False)), (Agent8, dict(G=0.0, gate=False, filt=False)), (Agent6, dict(filt=False)), (None, dict(G=0.0, fixed="valued"))):
        ph24.make, ph23.make, ph24.Agent5, ph24.record = _make24, _make23, ph17.Agent5, _record24
        a = ph28.run("T1", cls, v10, sd, **kw, **kk); sa = ph28.stub(cls, kn, sp, rows=n, seeds=BS) if cls is not None else None
        ph24.make, ph23.make, ph24.Agent5, ph24.record = hooked
        b = ph28.run("T1", cls, v10, sd, **kw, **kk); sb = ph28.stub(cls, kn, sp, rows=n, seeds=BS) if cls is not None else None
        assert all(np.array_equal(a[k], b[k]) for k in a if isinstance(a[k], np.ndarray)) and "FROZEN" not in b, f"a hook changed a run field ({cls})"
        assert sa is None or all(np.array_equal(sa[k], sb[k]) for k in sa if isinstance(sa[k], np.ndarray)), f"a hook changed a stub field ({cls})"
    ph24.make, ph23.make, ph24.Agent5, ph24.record = _make24, _make23, ph17.Agent5, _record24
    va = ph23.run("T1", Agent14, v10, sd, runs=n, steps=st, start="variant", hold=True); ph24.make, ph23.make, ph24.Agent5, ph24.record = hooked
    vb = ph23.run("T1", Agent14, v10, sd, runs=n, steps=st, start="variant", hold=True)
    assert all(np.array_equal(va[k], vb[k]) for k in va if isinstance(va[k], np.ndarray)), "the ph23.make hook changed a field"
    print("ok  with no training mode the hooks leave every field of ph28.run / ph28.stub / ph23.run bitwise equal (Agent14, Agent10, Agent10g, Agent8 G 0, Agent6, Agent5 fixed; World7 40 x 200, stub, variant start)")
    # the training reproduces H15 E2's arithmetic on a fresh module
    g = np.array([0, 1]*(n//2)); a = mk14(n, 6, np.zeros((n, 2))); v = train(a, g, "trained"); r = np.arange(n)
    m = ph8.MB4(n, parallel=False, gated=True, rng=np.random.default_rng(0), **ph11.MB); codes = np.stack([m.odour(101), m.odour(102)], 1)
    assert np.array_equal(codes, a.codes), "codes"
    z = np.zeros((n, 4)); rv = np.zeros((n, 4)); rv[:, 1] = 1.0
    for _ in range(30): m.step(code=codes[r, 1 - g], reinf=z)
    for _ in range(50): m.step()
    for _ in range(30): m.step(code=codes[r, g], reinf=rv)
    pre = ph15.valences(m, codes, g)
    assert np.array_equal(v[r, g], pre[:, 0]) and np.array_equal(v[r, 1 - g], pre[:, 1]) and np.array_equal(a.mb.w, m.w) and not a.mb.tc.any() and not a.mb.tr.any(), "training"
    print(f"ok  train() == a direct MB4 run of the protocol (30 neutral, 50 silent, 30 valued with reward on compartment 1) read by ph15.valences; traces cleared; v_V {uniq(v[r, g])}; v_N {uniq(v[r, 1 - g])}")
    o = run("T1", Agent14, "learned", sd, **kw); rd = READOUT[0]
    assert np.array_equal(rd["g"], o["good"]) and frozen_ok(o) and len(o["FROZEN"]) == 3, "hook g / frozen"
    s = run("T1", Agent14, "sham", sd, **kw); assert (READOUT[0]["v"] == 0.0).all() and bitwise(s, run("T1", Agent14, "zero", sd, **kw), FULL), "sham"
    assert bitwise(run("T1", Agent14, "learned->+1/0", sd, **kw), run("T1", Agent14, "supplied", sd, **kw), FULL), "(i2)"
    assert bitwise(run("T1", None, "learned", sd, G=0.0, fixed="valued", **kw), run("T1", None, "supplied", sd, G=0.0, fixed="valued", **kw), FULL), "(i5) known-answer"
    ok, _ = masks_equal(o, rd["v"], o["good"]); assert ok.all(), "(i7)"
    w1 = run("W1", Agent14, "learned", sd, **kw); t3 = run("T3a", Agent14, "learned", sd, **kw); assert frozen_ok(w1) and frozen_ok(t3) and construct_ok(t3), "W1 / T3a"
    print("ok  the hook trains on the run's own balance (g == World7.good), the module stays frozen at steps 0, 99, 199; sham == 0/0; learned->+1/0 == supplied; known-answer learned == +1/0;"
          " masks order-only; W1 and T3a trained runs frozen, T3a construction intact (40 x 200)")
    # the masks: a negative value does change them (the check can fail)
    kv = np.zeros((n, 2)); kv[r, o["good"]] = 1.0; vneg = kv.copy(); vneg[r, 1 - o["good"]] = -1e-6
    okn, _ = masks_equal(o, vneg, o["good"]); assert not okn.all(), "the mask check cannot fail"
    print(f"ok  the mask comparison detects a negative neutral value (-1e-6): rows differing {int((~okn).sum())}/{n}")
    # pass-probability arithmetic (design section 7 table)
    tab = {k: (pp_dp(-k/400, k/400), pp_dp(-k/400, (k + 10)/400), binom_ge(0.927 - k/400)) for k in (0, 2, 5, 8, 10, 12, 13, 15, 20)}
    exp = {0: (1.000, 1.000, 0.885), 2: (1.000, 0.999, 0.791), 5: (1.000, 0.973, 0.601), 8: (0.990, 0.811, 0.393), 10: (0.893, 0.614, 0.272), 12: (0.650, 0.405, 0.175),
           13: (0.506, 0.313, 0.137), 15: (0.260, 0.171, 0.079), 20: (0.025, 0.025, 0.015)}
    assert all(abs(tab[k][j] - exp[k][j]) < 0.003 for k in exp for j in range(3)), tab
    print("ok  pass-probability arithmetic reproduces the design's section 7 table (M2(a) into 0 / into 5 / the 0.88 line at 0.927): "
          + ", ".join(f"k {k}: {tab[k][0]:.3f}/{tab[k][1]:.3f}/{tab[k][2]:.3f}" for k in exp))
    hits, nums, nf = seeds_unused(); assert not hits, f"a seed of this run appears in {hits}"
    print(f"ok  seeds {nums} appear in no other file under the repository ({nf} files scanned; excluded by name ph29.py, ph29_*.txt, h20_stage_b_*.md, master_plan.md, notes/*.md, viewer/*)")


# ------------------------------------------------------------------ the tasks (design sections 5-8)
#            class, values, G, gate, filt, fixed
T1ARMS = {"learned": (Agent14, "learned", G_STAR, True, True, None), "supplied": (Agent14, "supplied", G_STAR, True, True, None),
          "sham": (Agent14, "sham", G_STAR, True, True, None), "release-maintain learned": (Agent10g, "learned", G_STAR, True, False, None),
          "pathway-off": (Agent8, "learned", 0.0, False, False, None), "known-answer": (None, "supplied", 0.0, False, False, "valued"),
          "base": (Agent10, "supplied", G_STAR, True, True, None)}


def t1arm(name, seeds, val=None):
    cls, v, G, gate, filt, fixed = T1ARMS[name]; return run("T1", cls, val or v, seeds, G=G, gate=gate, filt=filt, fixed=fixed)


def main(mode_):
    seeds = SEEDS[mode_]; ok = lambda z: "PASS" if z else "FAIL"
    print(f"== H20 Stage B, {mode_.upper()}. design {DESIGN}; G {G_STAR}, gate on where G 2; Agent14 (P 60, N_hi 300); world seed {seeds[0]}, agent seed {seeds[1]}; {R} rows x {T} steps;"
          f" geometry C0; training H15 E2 (neutral {TRAIN}, gap {GAP}, valued {TRAIN}); bootstrap seed {ph15.BOOT_SEED}; {'operation check only (not a verdict)' if mode_ == 'dev' else 'the one evaluation'} ==")
    header()
    hits, nums, nf = seeds_unused(); print(f"   seed self-check: every Stage B seed and derived in no other file ({nf} scanned): {not hits}{'' if not hits else ' ' + str(hits)}")
    print("   amendments: none")
    print("   rows share no state: one generator per world and one per agent population, fixed-size draws consumed in row order every step")
    print("   construction order in every trained or sham arm: world, mask, twin, values (+1/0 placeholder), agent, TRAINING on a.mb + read-out into a.known, cast draw, position, hold")
    # ---- the read-out and ML on this seed's balance
    t1 = {}; t1["learned"] = t1arm("learned", seeds); rl = READOUT[0]; t1["sham"] = t1arm("sham", seeds); rsh = READOUT[0]
    g = t1["learned"]["good"]; cell = t1["learned"]["cell"]; u = overlap(rl["codes"]); r = np.arange(R)
    t_ok, s_ok, cl, vV, vN, sV, sN = ml_check(rl["v"], rsh["v"], g); nfail = int((~t_ok).sum()); nsf = int((~s_ok).sum()); ml_read = nfail <= ML_BOUND and nsf == 0
    print("\n== the learned values (read-out after training; printed before the task) ==")
    print(f"   u by row: " + ", ".join(f"u={k}: {int((u == k).sum())}" for k in range(int(u.max()) + 1)) + "; per cell " + " | ".join(f"cell {c}: " + "/".join(str(int(((cell == c) & (u == k)).sum())) for k in range(int(u.max()) + 1)) for c in range(4)))
    print(f"   trained v_V by value {uniq(vV)}; v_N by value {uniq(vN)}; cross-table u x v_N " + " | ".join(f"u={k}: {uniq(vN[u == k])}" for k in range(int(u.max()) + 1) if (u == k).any()))
    print(f"   sham v_V by value {uniq(sV)}; v_N by value {uniq(sN)}")
    print(f"   ML (design section 7): trained rows failing {nfail}/{R} (v_V >= 0.5 fails {int((~cl['vV']).sum())}; 0 <= v_N <= 0.15 fails {int((~cl['vN']).sum())}; v_V > v_N fails {int((~cl['order']).sum())});"
          f" by cell " + "/".join(str(int(((cell == c) & ~t_ok).sum())) for c in range(4)) + f"; sham rows failing {nsf}/{R} -> {'readable' if ml_read else 'UNREADABLE'} (bound {ML_BOUND}); failing rows kept in every arm as assigned")
    for a in T1ARMS:
        if a not in t1: t1[a] = t1arm(a, seeds)
    maj = {a: majority(t1[a]) for a in T1ARMS}
    print("\n== T1, the H21 choice task ==")
    for a in T1ARMS:
        o = t1[a]; describe_majority(a, o, *maj[a]); h21_diag(a, o)
    # ---- T2 W1
    print("\n== T2, the absent-odour world W1 (valued column masked from step 0; REPORTED) ==")
    t2 = {"learned": run("W1", Agent14, "learned", seeds), "supplied": run("W1", Agent14, "supplied", seeds), "sham": run("W1", Agent14, "sham", seeds),
          "maintain": run("W1", Agent6, "supplied", seeds, filt=False)}
    s2 = {a: w1sum(o) for a, o in t2.items()}
    for a, o in t2.items():
        s = s2[a]; f1 = first_true(o["NAV"])
        print(f"   [W1 {a} {o['arm']}] dwell at the present source mean {s['dwell'].mean():.3f} (quartiles {q3f(s['dwell'].astype(float))}); reach {int(s['reach'].sum())}/{R}; lost rows {int(s['lost'].sum())};"
              f" wall contacts per row {s['contacts'].mean():.3f}; first surge step {qq(f1)}; draws == twin {o['draws_equal'] and o['rng_equal']}")
    # ---- T3a
    print("\n== T3a, the constructed loss (valued column masked from step 0, start at the valued source, valued hold s 2.0; REPORTED) ==")
    t3a = {"learned": run("T3a", Agent14, "learned", seeds), "supplied": run("T3a", Agent14, "supplied", seeds), "floor": run("T3a", Agent10, "supplied", seeds),
           "ceiling": run("T3a", None, "supplied", seeds, fixed="neutral")}
    D = {a: t3_dwell(o, 100, T) for a, o in t3a.items()}
    for a, o in t3a.items(): print(f"   [T3a {a} {o['arm']}] neutral dwell 100-599 mean {D[a].mean():.3f} (quartiles {q3f(D[a])}), rows > 0 {int((D[a] > 0).sum())}")
    judge(seeds, t1, maj, t2, s2, t3a, D, ml_read, t_ok, nfail, nsf, u, rl)


def judge(seeds, t1, maj, t2, s2, t3a, D, ml_read, t_ok, nfail, nsf, u, rl):
    ok = lambda z: "PASS" if z else "FAIL"
    print("\n== criteria (design v2 FINAL section 7; 95 percent, one evaluation, no extension; aggregation: PASS if every part passes, FAIL if any fails, else INCONCLUSIVE; the unrounded bound decides) ==")
    print(f"   ML the learned-value check: trained failing {nfail}/{R} (bound {ML_BOUND}), sham failing {nsf}/{R} -> {'readable' if ml_read else 'UNREADABLE'}")
    m1 = []
    for a in ("sham", "pathway-off", "known-answer"):
        z = maj[a][2]; m1.append(ok(z.mean() <= 0.20)); print(f"   M1(a) {a}: ties {z.sum()}/{R} = {z.mean():.3f}  at most 0.20 -> {m1[-1]}")
    o = t1["sham"]; V, N, Z = maj["sham"]; which = np.where(V, o["good"], np.where(N, 1 - o["good"], -1))
    m1.append(crit("M1(b) sham, P(+y source majority | chose)", "P", (0.35, 0.65), False, (which == o["plus_y"])[~Z]))
    V, N, Z = maj["pathway-off"]; m1.append(crit("M1(c) floor: pathway-off (learned values), P(V | chose)", "P", (0.35, 0.65), False, V[~Z]))
    m1.append(crit("M1(d) ceiling: known-answer, P(V) over all rows", "P", 0.85, False, maj["known-answer"][0]))
    M1 = agg(m1); print(f"   M1 -> {M1}{'' if M1 == 'PASS' else '  (the run is UNREADABLE under section 8)'}")
    ties = {a: maj[a][2].mean() for a in ("learned", "supplied", "sham")}
    print("   section 8: ties in the learned, supplied and sham arms " + ", ".join(f"{a} {v:.3f}" for a, v in ties.items()) + " (unreadable above 0.20)")
    Vl, Vs, Vsh, Vg = (maj[a][0] for a in ("learned", "supplied", "sham", "release-maintain learned")); cell = t1["learned"]["cell"]
    m2 = [crit("M2(a) DP = P(V) learned - supplied (Agent14), same rows", "DP", -0.05, False, Vl.astype(float), Vs.astype(float)),
          crit("M2(b) DP = P(V) learned - sham (Agent14), same rows", "DP", 0.20, False, Vl.astype(float), Vsh.astype(float))]
    m2c = [crit(f"M2(c) cell {c} ({CELLS[c]}), learned P(V)", "P", 0.70, False, Vl[cell == c]) for c in range(4)]; m2.append(agg(m2c)); print(f"   M2(c) -> {m2[-1]}")
    m2.append(crit("M2(d) DP = P(V) learned Agent14 - learned Agent10g, same rows", "DP", 0.05, False, Vl.astype(float), Vg.astype(float)))
    M2 = agg(m2); print(f"   M2 -> {M2}")
    k, pt, lo, hi = interval("P", Vl)
    print(f"      reported, not a bar (design section 12 point 4): learned P(V) {k}/{R} = {pt:.3f} [{lo:.3f}, {hi:.3f}] against the 0.88 line (lower bound >= 0.88 would read"
          f" {'above' if lo >= 0.88 else 'below'}); P(k >= 365 of 400) at {pt:.3f}: {binom_ge(pt):.4f}")
    kp, ptp, lop, hip = interval("P", Vl[t_ok]); print(f"      reported beside M2 (design section 7 ML): learned P(V) over the ML-passing rows {kp}/{int(t_ok.sum())} = {ptp:.3f} [{lop:.3f}, {hip:.3f}]")
    for a in ("learned", "supplied", "sham", "release-maintain learned", "pathway-off", "known-answer", "base"):
        k, pt, lo, hi = interval("P", maj[a][0]); print(f"      reported: {a} ({t1[a]['arm']}) V {maj[a][0].sum()} N {maj[a][1].sum()} tie {maj[a][2].sum()}; P(V) {k}/{R} = {pt:.3f} [{lo:.3f}, {hi:.3f}]")
    _, dpb, lob, hib = interval("DP", Vl.astype(float), maj["base"][0].astype(float)); print(f"      reported: DP learned - Agent10 (+1/0) {dpb:+.4f} [{lob:+.4f}, {hib:+.4f}]")
    L, S = t1["learned"], t1["supplied"]; cl_, cs_ = cls3(L), cls3(S); se = stepeq(L, S, TRAJK); fd = first_true(~se); dep = fd >= 0
    print(f"      where the value goes: into V {int((Vl & ~Vs).sum())}, out of V {int((~Vl & Vs).sum())}; outcome class changed {int((cl_ != cs_).sum())} rows, by u "
          + ", ".join(f"u={k}: {int(((cl_ != cs_) & (u == k)).sum())}/{int((u == k).sum())}" for k in range(int(u.max()) + 1))
          + f"; rows with an identical trajectory {int((~dep).sum())}, by u " + ", ".join(f"u={k}: {int((~dep & (u == k)).sum())}" for k in range(int(u.max()) + 1))
          + f"; first departing step {q3(fd[dep]) if dep.any() else 'n/a'}; ML-failing rows' outcomes learned V {int((Vl & ~t_ok).sum())}/{int((~t_ok).sum())}, supplied V {int((Vs & ~t_ok).sum())}")
    # M3
    i = {}; seeds_ = seeds
    i["(i2) learned with known := +1/0 == supplied (T1, every field)"] = bitwise(run("T1", Agent14, "learned->+1/0", seeds_), S, FULL)
    i["(i4) sham == Agent14 0/0 (every field) == Agent10 0/0 (T1)"] = bitwise(t1["sham"], run("T1", Agent14, "zero", seeds_), FULL) and bitwise(t1["sham"], run("T1", Agent10, "zero", seeds_))
    i["(i5) pathway-off learned == +1/0 (T1)"] = bitwise(t1["pathway-off"], run("T1", Agent8, "supplied", seeds_, G=0.0, gate=False, filt=False), FULL)
    kal = run("T1", None, "learned", seeds_, G=0.0, gate=False, filt=False, fixed="valued"); i["(i5) known-answer learned == +1/0 (T1)"] = bitwise(kal, t1["known-answer"], FULL)
    fr = [t1[a] for a in ("learned", "sham", "release-maintain learned", "pathway-off")] + [kal, t2["learned"], t2["sham"], t3a["learned"]]
    i["(i6) module frozen in every trained or sham arm (T1, W1, T3a)"] = all(frozen_ok(o) for o in fr)
    mk, per = masks_equal(L, rl["v"], L["good"]); i["(i7) masks with the learned values == +1/0's on every (row, step) (T1 learned)"] = bool(mk.all())
    M3 = ok(all(i.values()))
    print("   M3 identities: " + "; ".join(f"{k} {v}" for k, v in i.items()) + f" -> {M3}")
    print(f"      (i7) rows equal per mask {per}; read-out printed above; construction order printed in the header")
    chk = all(o["draws_equal"] and o["rng_equal"] for o in list(t2.values()) + list(t3a.values())) and all(construct_ok(o, a != "ceiling") for a, o in t3a.items())
    print(f"      reported checks (not M3): masked draws == World7 twin (W1, T3a) and T3a construction in every arm: {chk}")
    # M4
    lines = []; v4, bo = bench(say=lines.append); M4 = ok(v4)
    for ln in lines:
        if ln.startswith("== M4") or "STOP RULE" in ln or ln.startswith("(i") or "exactness claims" in ln or ln.startswith("   (t) ML"): print("      " + ln.strip())
    print(f"   M4 mechanism bench, re-run here with the bench seeds -> {M4}")
    # M6
    ls, l0 = lost_t1(L).astype(float), lost_t1(S).astype(float)
    m6 = [crit("M6(a) T1 no whiff of either plume in the last third, learned - supplied", "DP", 0.05, True, ls, l0)]
    cm = L["contacts"].mean(); m6.append(ok(cm <= 0.10)); print(f"   M6(b) T1 learned, wall contacts per row: mean {cm:.3f}  at most 0.10 -> {m6[-1]}")
    M6 = agg(m6); print(f"   M6 -> {M6}")
    # M5, M7 reported
    sl, ss, sh, s6 = s2["learned"], s2["supplied"], s2["sham"], s2["maintain"]
    _, d1, d1l, d1h = interval("DP", sl["dwell"].astype(float), ss["dwell"].astype(float)); _, d6, d6l, d6h = interval("DP", sl["dwell"].astype(float), s6["dwell"].astype(float))
    fsok, fs, _ = first_surge_ok(t2["learned"], PR)
    print(f"   M5 W1 (REPORTED, no bar): paired dwell learned - supplied {d1:+.3f} [{d1l:+.3f}, {d1h:+.3f}] (identical row for row {bool(np.array_equal(sl['dwell'], ss['dwell']))}); learned - Agent6"
          f" {d6:+.3f} [{d6l:+.3f}, {d6h:+.3f}]; reach learned {int(sl['reach'].sum())}, supplied {int(ss['reach'].sum())}, sham {int(sh['reach'].sum())}, Agent6 {int(s6['reach'].sum())};"
          f" lost rows {int(sl['lost'].sum())} / {int(ss['lost'].sum())} / {int(sh['lost'].sum())} / {int(s6['lost'].sum())}; first surge == first B whiff at or after {PR}, learned {int(fsok.sum())}/{R}")
    Dl, Ds, Df, Dc = D["learned"], D["supplied"], D["floor"], D["ceiling"]; _, spn, slo, shi = interval("DP", Dc, Df)
    Rl, Rll, Rlh = ratio_boot(Dl, Df, Dc); Rs, Rsl, Rsh = ratio_boot(Ds, Df, Dc)
    print(f"   M7 T3a (REPORTED, no bar): span {spn:.3f} [{slo:.3f}, {shi:.3f}]; R learned {Rl:.4f} [{Rll:.4f}, {Rlh:.4f}], R supplied {Rs:.4f} [{Rsl:.4f}, {Rsh:.4f}]; neutral dwell learned"
          f" {Dl.mean():.3f}, supplied {Ds.mean():.3f}, floor {Df.mean():.3f}, ceiling {Dc.mean():.3f}; identical row for row learned vs supplied {bool(np.array_equal(Dl, Ds))}")
    unread = (not ml_read) or M1 != "PASS" or max(ties.values()) > 0.20 or M3 != "PASS" or M4 != "PASS" or "UNREADABLE" in (M2, M6)
    verdict = ml_read and all(x == "PASS" for x in (M1, M2, M3, M4, M6)); fail = any(x == "FAIL" for x in (M2, M6))
    lab = "PASS" if verdict else "UNREADABLE" if unread and not fail else "FAIL" if fail else "INCONCLUSIVE"
    print(f"\n== H20 Stage B ==  ML {'readable' if ml_read else 'UNREADABLE'}  M1 {M1}  M2 {M2}  M3 {M3}  M4 {M4}  M6 {M6}  (M5 W1, M7 T3a reported) -> {lab}: "
          + ("SHOWN: a positive value learned by the agent's own learning module under a fixed reward training (the neutral odour presented equally often without"
             " reinforcement; learning frozen in the test) is carried by the adopted agent (Agent14) into the choice of source in the H21 task: within 0.05 of the"
             " supplied value on the same rows, at least 0.20 above a sham-trained agent, at least 0.70 in every cell, and with the filter's gain over the gate agent"
             if verdict else "UNREADABLE (section 8)" if lab == "UNREADABLE" else "NOT shown under the registered criteria"))


if __name__ == "__main__":
    m = ([x for x in sys.argv[1:] if x in ("demo", "bench", "dev", "eval")] or ["demo"])[0]
    if m == "demo": demo(); sys.exit(0)
    if m == "bench":
        v, o = bench(); sys.exit(0 if v else 1 if o["nocand"] else 3)
    main(m)
