#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H17 Run 2: the search engaged at S 250, the wall-contact bar re-anchored (a navigation hypothesis).

Usage: python ph27.py demo | bench | dev | eval

Design: H17 Run 2 design v2 FINAL, confirmed by the owner (decision:h17-run2-open, '권고안대로 확정하고 Run 2 진행', gloss 'confirm as
recommended and proceed with Run 2'): doc d73c77ebd99d50d86, hash d2374c5e...d5e9, stored before this file existed. The relaxation
re-signed in form for H17 and H17 Run 2 (decision:classification-rule-relaxed-any-odour-silence-counter-h17-run2: the same ONE counter q);
the T3 (c) bar re-signed for Run 2 (decision:h17-t3c-bar-resigned-run2).
ONE change from Run 1 (design section 3.1 (a)): the engagement threshold S 250 instead of 210; everything else of the Search rule is
ph26.py's code, imported unchanged (ph26.py is not edited; its sha256 is checked against Run 1's record). No adopted module is edited.
  Agent13 = Search13 + ph24.Agent10 (the main arm), Agent13g = Search13 + ph24.Agent10g (reported).
  Search13 is ph26.Search with S carried by the class (S = 250): around each call of ph26.Search.act it sets ph26's module constant
  S_ON to the instance's S and restores it afterwards, so the code executed is ph26's own rule (reading R14). Identity (a4) checks it:
  a Search13 agent with S 210 equals ph26.Agent12 bitwise on every field, the search fields included.
Run-time hooks (no file edited): ph24.make and ph26.make also build Agent13 / Agent13g (and the S 210 twin for (a4)); ph24.record and
ph26.record also store flee_side per step (FS, measurement only). The demo asserts the hooks leave every ph24.run / ph24.stub field of
ph24's agents and of ph26.Agent12 bitwise equal. Helpers reused by import: ph26 (the rule, cold-start runner, oracle, row identity,
engagement check, q recursion, pass probabilities, W1 summary), ph26b (whiff labels), ph24 (run, stub, bitwise, events), ph24c
(drive-ended negative holds), ph16 / ph15 (Wilson, bootstrap), ph18 (majority, aggregation), ph19 (H21 diagnostics). Nothing copied
from them except the task-and-criteria driver below, which follows ph26.main / judge with Agent13 and the re-signed T3 (c).

Readings where the design is silent, chosen so that never-engaged rows stay bitwise Agent10 (printed again in the bench output):
 (R1) Step counting as ph26 R1 at S 250: q is updated at the top of each act; silence from construction -> first engaged step index 249;
      one whiff at step index 0 -> first engaged step index 250; (c1) q = since = 45 at construction -> engagement at step index 204
      (the 205th step); window (i) indices 204-503, window (ii) indices 204-803; the (c1) run is 805 steps.
 (R2) (c2) since = q = S = 250 at construction, read literally: the first step is already engaged, with u = 1.
 (R3)-(R7) as ph26.py R3-R7 (oracle; constructions from the world generator; (b) whiffs on channel 0, (d) stubs 600 steps both
      channels; pass probability b = discordant fraction, sd = sqrt(b - DP^2), se = sd / 20; reach = within 3.0 after the move).
 (R8) (b'): (b'1) is (b)'s one-whiff schedule at +1/0 (800 steps); (b'2) values +1/-1, channel 1 (the negative odour) at p 0.30 for
      20 steps, then silence to 800 steps. A row is exact iff the rule holds on every step (ph26.engagement_exact at S 250: q recursion,
      engaged = q >= S and nothing held, u, leg, slant, target, the same noise sample), it is not engaged on any step with q 210-249,
      and its first engaged step is exactly 250 steps after its last whiff. The bar reads that indicator. The constructed state (a
      negative hold forms; target = flee_side on every held step; the hold ends by the drive; nothing held afterwards) is checked and
      printed per row beside it; `since` - q on the first engaged step is printed with its count.
 (R9) T3 (c) as re-signed: a row leaves lost if Agent10 is lost and Agent13 is not (lost = no whiff of either plume on steps 400-599).
      For such a row, fe = Agent13's first engaged step and tw = its first step after fe with a whiff of either odour; the row is
      contact-mediated iff Agent13 registered a wall contact on the move after any step in [fe, tw - 1] (the contact is registered by
      the move after a step's act, so it precedes the whiff sensed at tw). The statistic is the fraction of contact-mediated rows among
      the rows that leave lost; PASS iff the point estimate <= 0.10; UNREADABLE if fewer than 20 rows leave lost.
 (R10) (h2c) pass probability: the exact binomial P(K <= floor(0.10 n)) with K ~ Binomial(n, f), n = the bench's count of rows that
      leave lost and f = the bench's contact-mediated fraction (design section 7: 'with about 35 out-of-lost rows'); f = 0 gives 1;
      n < 20 gives 0 (the part could not be read).
 (R11) (h3) pass probability: M2 (a)'s bar (paired dwell Agent13 - Agent10, lower bound >= -1.2) at the bench: DP = mean paired
      difference, sd = the paired differences' standard deviation (ddof 0), se = sd / 20, P = Phi((DP + 1.2) / se - 1.96); sd 0: the
      point decides. The bootstrap interval is printed beside it.
 (R12) 'sigma_1 pointed to the flee_side side' (h2, reported): at the row's first engaged step, the sign of sin(leg 1's search target)
      (target 255 for cast_sign +1, i.e. toward -y; 105 for -1) equals the sign of sin(flee_side) (90 -> +y, 270 -> -y).
 (R13) (d)'s pass probability (reported beside the bar): the exact binomial P(K <= 11 of 400) at p = the bench's engaged-row fraction.
 (R14) S per instance, as stated above; ph26.engagement_exact and ph26.cold are called with ph26.S_ON set to 250 for the call (their
      only S-dependent quantities: the engagement rule check and (c2)'s q0).
Nothing changes after the table.
"""
import sys, os, re, math, hashlib
from contextlib import contextmanager
import numpy as np
import ph26                                            # hooks ph24; sets its own bootstrap seed (reset below)
import ph26b                                           # measurement helpers only (whiff labels); nothing run at import
import ph9, ph11, ph12b, ph13, ph15, ph16, ph18, ph19, ph21, ph22, ph24, ph24b, ph24c
from ph16 import interval, crit, R, T
from ph18 import majority, describe_majority, agg
from ph19 import h21_diag
from ph21 import G_STAR, q3, first_true
from ph24 import Agent10, Agent10g, Agent8, Agent6, bitwise, t3_dwell, q3f, events
from ph24c import released
from ph26 import (Search, AgentO, Agent12, leg_of, slant_of, search_target, row_identity, qrec, lost, cls3, Phi, pp_dp, pp_prop,
                  rel_pos, region_near, inside, fmt_ci, w1sum)
from ph9 import LMAX

sys.stdout.reconfigure(newline="\n")
DESIGN = "H17 Run 2 v2 FINAL doc d73c77ebd99d50d86 hash d2374c5e3091184c669af5f8e09a561b9d7acf680e6b10fbc211750fd0d7d5e9"
PH26_SHA = "1c9b6f5b6e3f0341e60c707cd577d748292ecdb720062ecada33336101e167cf"     # record:h17-bench-result
S_RUN2 = 250
SEEDS = dict(dev=(9961, 9973), eval=(1965, 2065))
BENCH = dict(rows=400, steps=600, steps_b=800, steps_stub=200, steps_c1=805, steps_c2=600, steps_c3=1800, q_c1=45, seed_w=20261061, seed_a=20261062)
BS = (BENCH["seed_w"], BENCH["seed_a"])
ph15.BOOT_SEED = 20261063; ph15._idx.clear()        # design section 7 (after ph26's import set its own); the resample cache emptied
MODS = (ph9, ph11, ph12b, ph13, ph15, ph16, ph18, ph19, ph21, ph22, ph24, ph24b, ph24c, ph26, ph26b)
E_C1 = S_RUN2 - BENCH["q_c1"] - 1                     # 204 (reading R1)
Z95 = 1.959964


def sha(p=__file__): return hashlib.sha256(open(p, "rb").read()).hexdigest()


@contextmanager
def s_on(S):
    keep = ph26.S_ON; ph26.S_ON = S
    try: yield
    finally: ph26.S_ON = keep


# ------------------------------------------------------------------ the agent (design section 3.5)
class Search13(Search):
    """ph26.Search with S carried by the class; the executed rule is ph26.Search.act (reading R14)"""
    S = S_RUN2

    def act(self, w, whiffs, wind_on):
        with s_on(self.S): return super().act(w, whiffs, wind_on)


class Agent13(Search13, Agent10): """H17 Run 2: the search at S 250 on the adopted agent (Agent10 = Release + Agent8)"""
class Agent13g(Search13, Agent10g): """H17 Run 2: the search at S 250 on Agent10g (reported)"""
class Agent13at210(Agent13):
    """identity (a4) only: Agent13's code with S 210, to equal ph26.Agent12 bitwise"""
    S = 210


# ------------------------------------------------------------------ hooks (run time; no file edited)
_make26, _record26 = ph26.make, ph26.record


def make(cls, runs, rng, G, known, gate=True, filt=True, release=True):
    if isinstance(cls, type) and issubclass(cls, Agent13): kw = dict(rule=gate, filt=filt, release=release, search=ph26._SEARCH[0])
    elif cls is Agent13g: kw = dict(rule=gate, release=release, search=ph26._SEARCH[0])
    else: return _make26(cls, runs, rng, G, known, gate, filt, release)
    return cls(runs, rng, G=G, known=known, **kw)


def record(o, t, a, h, x, pa):
    """ph26.record (itself ph24.record plus the search fields), plus flee_side per step (FS); every other field untouched"""
    _record26(o, t, a, h, x, pa)
    if "FS" not in o: o["FS"] = np.zeros(o["H"].shape)
    o["FS"][t] = a.flee_side


ph24.make, ph24.record, ph26.make, ph26.record = make, record, make, record


def run(world, cls, vals, seeds, search=True, **kw): return ph26.run(world, cls, vals, seeds, search=search, **kw)
def stub(cls, known, sched, search=True, **kw): kw.setdefault("seeds", BS); return ph26.stub(cls, known, sched, search=search, **kw)
def cold(klass, cls, walls, seeds=BS, runs=BENCH["rows"], steps=None):
    with s_on(S_RUN2): return ph26.cold(klass, cls, walls, seeds=seeds, runs=runs, steps=steps or BENCH[f"steps_{klass}"])
def engagement_exact(o, q0=0.0, S=S_RUN2):
    with s_on(S): return ph26.engagement_exact(o, q0)


SFIELDS = ph24.FIELDS + ("SIL", "TO", "EV", "W", "Q", "ENG", "U", "LEG", "CS", "TGTB", "NZB", "NZ", "POS", "HEAD", "C", "AT2")


# ------------------------------------------------------------------ measures
def binom_cdf(k, n, p):
    if k < 0: return 0.0
    if p <= 0: return 1.0
    if p >= 1: return 1.0 if k >= n else 0.0
    return float(min(1.0, sum(math.comb(n, i)*p**i*(1 - p)**(n - i) for i in range(0, min(k, n) + 1))))


def pp_d(k, n=400): return binom_cdf(11, n, k/n)                          # reading R13


def m3c(o13, o10):
    """reading R9: rows that leave lost; contact-mediated among them; counts of rows with no engagement / no whiff after it (expected 0)"""
    l13, l10 = lost(o13), lost(o10); out = l10 & ~l13; fe = first_true(o13["ENG"]); med = np.zeros(len(out), bool); noeng = nowh = 0
    steps = o13["H"].shape[0]
    for r in np.flatnonzero(out):
        f = int(fe[r])
        if f < 0: noeng += 1; continue
        w = np.flatnonzero(o13["W"][f + 1:, r].any(1)); tw = f + 1 + int(w[0]) if len(w) else steps
        if not len(w): nowh += 1
        med[r] = bool(o13["C"][f:tw, r].any())
    return out, med, noeng, nowh


def pp_m3c(n, k):                                                           # reading R10
    if n < 20: return 0.0
    return binom_cdf(n//10, n, k/n)


def pp_cont(d, bar, most=False):                                            # reading R11
    dp = float(np.mean(d)); sd = float(np.std(d)); n = len(d)
    if sd <= 0: return (float(dp <= bar) if most else float(dp >= bar)), dp, sd
    se = sd/math.sqrt(n); return Phi(((bar - dp) if most else (dp - bar))/se - Z95), dp, sd


def contacts_by_leg(o):
    C, E, L = o["C"], o["ENG"], o["LEG"]; out = {"not engaged": int((C & ~E).sum())}
    for k in sorted(set(L[C & E].tolist())): out[f"leg {k}"] = int((C & E & (L == k)).sum())
    return out


def flee_side_match(o, r, f):
    """reading R12: leg 1's crosswind direction at the first engaged step points to the flee_side side"""
    tgt = search_target(np.array([0.0]), np.array([o["CS"][f, r]]))[0]
    return bool(np.sign(np.sin(np.radians(tgt))) == np.sign(np.sin(np.radians(o["FS"][f, r]))))


def neg_after(o13, rows, fe):
    """per row (after its first engaged step): the first whiff's odour, a negative hold re-formed, stranded again (a drive-ended negative hold)"""
    g = o13["good"]; neg = 1 - g; ev = events(o13); form = ev["form"]; E, Rr, _ = released(o13); fo, reneg, restr = [], [], []
    for r in rows:
        f = int(fe[r]); w = np.flatnonzero(o13["W"][f:, r].any(1)); fo.append(ph26b.whiff_lab(o13, f + int(w[0]), r) if len(w) else "none")
        reneg.append(bool((form[f + 1:, r] & (o13["H"][f + 1:, r] == neg[r])).any())); restr.append(any((x == r) and (e > f) for e, x in zip(E, Rr)))
    return fo, np.array(reneg, bool), np.array(restr, bool)


# ------------------------------------------------------------------ the mechanism bench (design section 4)
def readings(say):
    say("   readings where the design is silent (file header R1-R14): R1 q updated at the top of each act (silence from construction: first engaged step index 249;"
        " one whiff at index 0: index 250; (c1) q = since = 45: engagement at step index 204, window (i) indices 204-503, window (ii) 204-803, run 805 steps);"
        " R2 (c2) q = since = 250 at construction (first step engaged, u = 1); R3-R7 as ph26.py; R8 (b') row exact = the rule on every step + not engaged at q 210-249"
        " + first engaged step exactly 250 after the last whiff, the constructed state printed beside it; R9 T3 (c): rows leaving lost, contact-mediated iff an Agent13"
        " contact on the moves of steps [first engaged step, first whiff after it - 1], point <= 0.10, unreadable under 20 rows; R10 (h2c) pass probability exact binomial"
        " P(K <= floor(0.10 n)) at the bench's n and fraction; R11 (h3) pass probability Phi((DP + 1.2) / (sd / 20) - 1.96), sd of the paired dwell differences;"
        " R12 sigma_1 vs flee_side by the sign of sin(leg 1 target) and sin(flee_side); R13 (d) pass probability exact binomial P(K <= 11 of 400);"
        " R14 S per instance (ph26.S_ON set around ph26.Search.act), checked by (a4)")


def bench(say=print):
    n = BENCH["rows"]; p = 0.30; kn = [1.0, 0.0]; ids = {}; bars = {}; out = {}
    say(f"== H17 Run 2 mechanism bench (design section 4). design {DESIGN}; {BENCH}; S {S_RUN2}, L0 {ph26.L0}, gamma {ph26.GAMMA}, U1 {ph26.U1}; bootstrap seed {ph15.BOOT_SEED} ==")
    header(say); readings(say)
    both = [(BENCH["steps_stub"], p, p)]
    # (a1)
    ids["a1 stub Agent13 off == Agent10"] = bitwise(stub(Agent13, kn, both, search=False), stub(Agent10, kn, both))
    ids["a1 stub Agent13g off == Agent10g"] = bitwise(stub(Agent13g, kn, both, search=False), stub(Agent10g, kn, both))
    T1 = {(k, v): run("T1", c, v, BS) for v in ((1.0, 0.0), (1.0, -1.0)) for k, c in (("Agent13", Agent13), ("Agent10", Agent10))}
    ids["a1 World7 Agent13 off == Agent10"] = bitwise(run("T1", Agent13, (1.0, 0.0), BS, search=False), T1[("Agent10", (1.0, 0.0))])
    ids["a1 World7 Agent13g off == Agent10g"] = bitwise(run("T1", Agent13g, (1.0, 0.0), BS, search=False), run("T1", Agent10g, (1.0, 0.0), BS))
    say(f"(a1) search False == the base bitwise (H, s, S, nav, since, silence, target, positions, headings, timeout/evidence flags): stub both channels p {p} {BENCH['steps_stub']} steps:"
        f" Agent13 == Agent10 {ids['a1 stub Agent13 off == Agent10']}, Agent13g == Agent10g {ids['a1 stub Agent13g off == Agent10g']}; World7 +1/0 {n} x {BENCH['steps']}:"
        f" Agent13 == Agent10 {ids['a1 World7 Agent13 off == Agent10']}, Agent13g == Agent10g {ids['a1 World7 Agent13g off == Agent10g']}")
    # (a2)
    sp = stub(Agent13, kn, both); ids["a2 stub == Agent10 (never engaged)"] = bitwise(sp, stub(Agent10, kn, both)) and not sp["ENG"].any()
    say(f"(a2) search True, stub both channels p {p}: == Agent10 bitwise and never engaged {ids['a2 stub == Agent10 (never engaged)']} (engaged (row, step) {int(sp['ENG'].sum())})")
    for v in ((1.0, 0.0), (1.0, -1.0)):
        ok, cnt = row_identity(T1[("Agent13", v)], T1[("Agent10", v)]); ids[f"a2 World7 {v}"] = ok
        say(f"(a2) World7 {v[0]:+.0f}/{v[1]:+.0f} {n} x {BENCH['steps']}: never-engaged rows bitwise Agent10, engaged rows equal before their first engaged step: {ok} {cnt}")
    WT = {}
    for wd in ("W1", "T3a"):
        WT[wd] = (run(wd, Agent13, (1.0, 0.0), BS), run(wd, Agent10, (1.0, 0.0), BS)); ok, cnt = row_identity(*WT[wd]); ids[f"a2 {wd}"] = ok
        say(f"(a2) {wd} {n} x {BENCH['steps']}: {ok} {cnt}; masked draws == the World7 twin {WT[wd][0]['draws_equal'] and WT[wd][0]['rng_equal']}")
    # (a3)
    for v in ((0.0, 0.0), (1.0, 1.0), (1.0, -1.0)):
        b10 = T1[("Agent10", v)] if v == (1.0, -1.0) else run("T1", Agent10, v, BS); off = bitwise(run("T1", Agent13, v, BS, search=False), b10)
        on_ = T1[("Agent13", v)] if v == (1.0, -1.0) else run("T1", Agent13, v, BS); ok, cnt = row_identity(on_, b10)
        s_off = bitwise(stub(Agent13, list(v), both, search=False), stub(Agent10, list(v), both)); s_on_ = bitwise(stub(Agent13, list(v), both), stub(Agent10, list(v), both))
        ids[f"a3 {v}"] = off and ok and s_off and s_on_
        say(f"(a3) chain {v[0]:+.0f}/{v[1]:+.0f}: search False == Agent10 World7 {off}, stub {s_off}; search True stub == Agent10 {s_on_}; World7 never-engaged rows bitwise {ok} {cnt}")
    # (a4)
    for v in ((1.0, 0.0), (1.0, -1.0)):
        a, b = run("T1", Agent13at210, v, BS), run("T1", Agent12, v, BS); eq = bitwise(a, b, SFIELDS); ids[f"a4 {v}"] = eq
        say(f"(a4) World7 {v[0]:+.0f}/{v[1]:+.0f} {n} x {BENCH['steps']}: Agent13's code at S 210 == ph26.Agent12 bitwise on every field incl. q, engaged, u, leg, cast sign, base target"
            f" and noise samples: {eq} (engaged rows {int(a['ENG'].any(0).sum())} vs {int(b['ENG'].any(0).sum())})")
    # (b)
    sch = {"one whiff at step 0 then silence": [(1, 1.0, 0.0), (BENCH["steps_b"] - 1, 0.0, 0.0)], "a 20-step p 0.30 burst then silence": [(20, p, 0.0), (BENCH["steps_b"] - 20, 0.0, 0.0)],
           "silence from construction": [(BENCH["steps_b"], 0.0, 0.0)]}
    okb = np.ones(n, bool); hq = 0; SO = {}
    for k, s in sch.items():
        o = stub(Agent13, kn, s); SO[k] = o; ex, held_q = engagement_exact(o); okb &= ex; hq += held_q
        fe = first_true(o["ENG"]); anyw = o["W"].any(2); lastw = np.where(anyw.any(0), o["H"].shape[0] - 1 - np.argmax(anyw[::-1], 0), -1)
        rel = np.where(lastw >= 0, fe - lastw, fe); fh = first_true(o["H"] >= 0)
        hold_end = np.where(fh >= 0, first_true((o["H"] < 0) & (np.arange(o["H"].shape[0])[:, None] > fh[None, :])), -1)
        ul = o["U"][o["ENG"]]; bl = [int(u) for u in (30, 90, 180, 300, 450) if (ul == u).any()]
        say(f"(b) {k}: rows exact {int(ex.sum())}/{n}; first engaged step index {q3(fe[fe >= 0])} (never {int((fe < 0).sum())}); first engaged step - last whiff step {q3(rel[fe >= 0])}"
            f" (rows with a whiff {int((lastw >= 0).sum())}); engaged until the run's end in {int(o['ENG'][-1].sum())} rows; hold formed {int((fh >= 0).sum())} rows, ended at step"
            f" {q3(hold_end[hold_end >= 0])}; q >= S with a hold (row, step) {held_q}; u max {int(ul.max()) if len(ul) else -1}, leg boundaries crossed {bl}; legs seen {sorted(set(o['LEG'][o['ENG']].tolist()))};"
            f" slant -1 steps {int((o['ENG'] & (slant_of(np.maximum(o['U'], 0)) < 0)).sum())}")
    k_, pt, lo, hi = interval("P", okb); bars["b"] = lo
    say(f"(b) engagement exact in every schedule (q recursion, engaged = q >= S and nothing held, u, leg, slant, the target = the search target on engaged steps and the base's"
        f" target on every other, the same noise sample): {fmt_ci(k_, n, pt, lo, hi)} (bar lower bound >= 0.95) -> {'PASS' if lo >= 0.95 else 'FAIL'}; q >= S with a hold, all schedules: {hq} (expected 0)")
    # (b')
    bp = np.ones(n, bool); sq = {}
    for lab, o, kv in (("b'1 tracking-loop silence (+1/0, one valued whiff at step 0, then silence)", SO["one whiff at step 0 then silence"], kn),
                       ("b'2 R3 stranded state (+1/-1, 20 steps p 0.30 on the negative channel, then silence)", stub(Agent13, [1.0, -1.0], [(20, 0.0, p), (BENCH["steps_b"] - 20, 0.0, 0.0)]), [1.0, -1.0])):
        ex, held_q = engagement_exact(o); fe = first_true(o["ENG"]); anyw = o["W"].any(2); st = o["H"].shape[0]
        lastw = np.where(anyw.any(0), st - 1 - np.argmax(anyw[::-1], 0), -1); Q = o["Q"]
        mid = ((Q >= 210) & (Q < S_RUN2) & o["ENG"]).any(0); timing = (fe >= 0) & np.where(lastw >= 0, fe - lastw == S_RUN2, fe == S_RUN2 - 1)
        rowok = ex & ~mid & timing; bp &= rowok; r_ = np.arange(n); fes = np.maximum(fe, 0)
        dsq = (o["SINCE"][fes, r_] - Q[fes, r_])[fe >= 0]; sq[lab[:3]] = dsq
        ch = 1 if kv[1] < 0 else 0; held = o["H"] == ch; formed = held.any(0)
        fl = np.where(held, o["TGT"] == o["FS"], True).all(0); hend = np.where(formed, first_true(~held & (np.arange(st)[:, None] > first_true(held)[None, :])), -1)
        hits = held & o["W"][:, :, ch]; lasthit = np.where(hits.any(0), st - 1 - np.argmax(hits[::-1], 0), -1)
        dr = events(o)["drives"]; bydrive = np.zeros(n, bool)
        m = (dr["hp"] == ch) & dr["ended"]; bydrive[dr["r"][m]] = True
        after = np.array([bool((o["H"][hend[r]:, r] < 0).all()) if hend[r] >= 0 else False for r in range(n)])
        say(f"(b') {lab}: rows exact {int(rowok.sum())}/{n} (rule on every step {int(ex.sum())}, engaged at some q 210-249 {int(mid.sum())}, first engaged step - last whiff step == 250"
            f" (index 249 in a row without a whiff) {int(timing.sum())}; rows without a whiff {int((lastw < 0).sum())}); first engaged step index {q3(fe[fe >= 0])} (never {int((fe < 0).sum())}); q >= S with a hold {held_q}")
        say(f"      constructed state: hold of the {'negative' if ch == 1 else 'valued'} odour formed {int(formed.sum())}/{n}"
            + (f"; target == flee_side on every held step {int((fl & formed).sum())}/{n}" if ch == 1 else "") + f"; the hold ended {int((hend >= 0).sum())}, by the timeout drive {int(bydrive.sum())}; steps from the last hit of the held odour"
            f" to the hold's end {q3((hend - lasthit)[(hend >= 0) & (lasthit >= 0)])}; nothing held from the end to step {st - 1} {int(after.sum())}; first engaged step - hold end"
            f" {q3((fe - hend)[(fe >= 0) & (hend >= 0)])}")
        say(f"      `since` - q on the first engaged step: {q3(dsq)} (min {int(dsq.min()) if len(dsq) else 0}, max {int(dsq.max()) if len(dsq) else 0}); equal to 0 in {int((dsq == 0).sum())}/{len(dsq)} rows")
    k_, pt, lo, hi = interval("P", bp); bars["b'"] = lo; sq0 = bool(len(sq["b'2"]) == n and (sq["b'2"] == 0).all())
    say(f"(b') engaged / not engaged exact as the rule says, both constructed states: {fmt_ci(k_, n, pt, lo, hi)} (bar lower bound >= 0.95) -> {'PASS' if lo >= 0.95 else 'FAIL'}")
    say(f"(b') `since` - q identity in (b'2) (expected 0 in every row by ph21.py:71-75, design section 2 (E)): {sq0}" + ("" if sq0 else
        " -> NOTICE FOR THE OWNER: the rejection of design section 3.1 (b) rests on a wrong reading; the bench continues (not a mechanism failure)"))
    out["b2_since_q0"] = sq0
    # (c)
    say(f"(c) cold start, values 0/0, nothing held, {n} rows per class and wall setting; arms floor Agent10, Agent13, ceiling oracle (reading R3); walls OFF is the primary reading")
    C = {}
    for klass in ("c1", "c2", "c3"):
        for walls in (False, True):
            for k, c in (("Agent10", Agent10), ("Agent13", Agent13), ("oracle", AgentO)): C[(klass, walls, k)] = cold(klass, c, walls)
    ids["c constructions equal across arms and wall settings"] = all(np.array_equal(C[(kl, wl, k)]["start"], C[(kl, False, "Agent10")]["start"])
                                                                   for kl in ("c1", "c2", "c3") for wl in (False, True) for k in ("Agent10", "Agent13", "oracle"))
    o0 = C[("c1", False, "Agent10")]; ins0 = inside(o0["start"], o0["src"]); m = o0["meta"]
    geo_ok = bool(not ins0.any() and (m["da"] >= 5).all() and (m["da"] <= 14).all() and (m["dc"] >= 26).all() and (m["dc"] <= 31).all())
    ids["c1 start outside both regions, d_along [5, 14], |d_cross| [26, 31] outer side"] = geo_ok
    c3in = bool(inside(C[("c3", False, "Agent10")]["start"], C[("c3", False, "Agent10")]["src"]).any()); ids["c3 start outside both regions"] = not c3in
    say(f"   constructions identical across arms and wall settings {ids['c constructions equal across arms and wall settings']}; (c1) start outside both whiff regions, d_along in [5, 14],"
        f" |d_cross| in [26, 31] on the outer side: {geo_ok} (d_along {q3f(m['da'])}, |d_cross| {q3f(m['dc'])}, source index 0/1 {np.bincount(m['k'], minlength=2).tolist()});"
        f" (c3) starts outside both regions {not c3in}")
    e = E_C1; W1_, W2_ = slice(e, e + 300), slice(e, e + 600); res = {}
    for walls in (False, True):
        lab = "walls OFF (primary)" if not walls else "walls ON (reported)"
        o10, o13, oo = (C[("c1", walls, k)] for k in ("Agent10", "Agent13", "oracle"))
        wi = {k: o["W"][W1_].any((0, 2)) for k, o in (("Agent10", o10), ("Agent13", o13), ("oracle", oo))}
        re_ = {k: o["AT2"][W2_].any((0, 2)) for k, o in (("Agent10", o10), ("Agent13", o13), ("oracle", oo))}
        pre = {k: o["W"][:e].any((0, 2)) for k, o in (("Agent10", o10), ("Agent13", o13), ("oracle", oo))}
        eng = o13["ENG"][e]; fe = first_true(o13["ENG"]); ex, _ = engagement_exact(o13, q0=BENCH["q_c1"])
        say(f"   (c1) R3 stranded state, {lab}, {BENCH['steps_c1']} steps; Agent13 engaged at step index {e} in {int(eng.sum())}/{n} rows (first engaged step {q3(fe[fe >= 0])},"
            f" never {int((fe < 0).sum())}); engagement exact (q0 45) {int(ex.sum())}/{n}; any whiff before the engagement step: Agent10 {int(pre['Agent10'].sum())}, Agent13 {int(pre['Agent13'].sum())}, oracle {int(pre['oracle'].sum())}")
        for k in ("Agent10", "Agent13", "oracle"):
            o = C[("c1", walls, k)]; k1, p1, l1, h1 = interval("P", wi[k]); k2, p2, l2, h2 = interval("P", re_[k]); fw = first_true(o["W"].any(2)); fa = first_true(o["AT2"].any(2))
            say(f"      [{k}] (i) any whiff in the 300 steps from the engagement step {fmt_ci(k1, n, p1, l1, h1)}; (ii) a source reached in the 600 steps from it {fmt_ci(k2, n, p2, l2, h2)};"
                f" first whiff step {q3(fw[fw >= 0])} (rows {int((fw >= 0).sum())}); first reach step {q3(fa[fa >= 0])} (rows {int((fa >= 0).sum())}); ever reached by {BENCH['steps_c1']}"
                f" {int((fa >= 0).sum())}; wall contacts per row {o['contacts'].mean():.3f}; engaged (row, step) {int(o['ENG'].sum())}")
            res[(walls, k)] = (wi[k], re_[k], l1, l2)
        _, dp, dlo, dhi = interval("DP", wi["Agent13"].astype(float), wi["Agent10"].astype(float))
        _, dpr, drlo, drhi = interval("DP", re_["Agent13"].astype(float), re_["Agent10"].astype(float))
        say(f"      paired DP (i) Agent13 - Agent10 {dp:+.4f} [{dlo:+.4f}, {dhi:+.4f}]; paired DP (ii) {dpr:+.4f} [{drlo:+.4f}, {drhi:+.4f}] (bootstrap 5000, seed {ph15.BOOT_SEED})")
        fw13 = first_true(o13["W"].any(2)); uw = (fw13 - e)[(fw13 >= e)]
        say(f"      Agent13 first whiff after engagement, u = step - {e}: {q3(uw)} (rows {len(uw)}); cumulative fraction by u 130/167/190/299/599: "
            + "/".join(f"{(uw <= u).sum()/n:.3f}" for u in (130, 167, 190, 299, 599)))
        rr = np.flatnonzero(eng)
        if len(rr):
            ep = np.array([rel_pos(o13, e, r) for r in rr]); insd = inside(o13["POS"][e - 1, rr], o13["src"][rr]); _, dist, _ = region_near(o13["POS"][e - 1, rr], o13["src"][rr])
            say(f"      engagement position (Agent13, the position step {e} sensed at, relative to the start's source): d_along {q3f(ep[:, 0])} (min {ep[:, 0].min():.1f}, max {ep[:, 0].max():.1f};"
                f" beyond LMAX 25 {int((ep[:, 0] > LMAX).sum())}, upwind of the source {int((ep[:, 0] < 0).sum())}), d_cross outward {q3f(ep[:, 1])} (min {ep[:, 1].min():.1f}, max {ep[:, 1].max():.1f});"
                f" inside a whiff region {int(insd.sum())}; distance to the nearest region {q3f(dist)}; start d_along {q3f(m['da'][rr])}, |d_cross| {q3f(m['dc'][rr])}")
        if not walls:
            bars["c1 (i) whiff within 300, Agent13 (>= 0.40)"] = res[(False, "Agent13")][2]; bars["c1 (ii) reach within 600, Agent13 (>= 0.30)"] = res[(False, "Agent13")][3]
            bars["c1 (iii) paired DP (i) Agent13 - Agent10 (>= +0.30)"] = dlo; out.update(c1_i=float(wi["Agent13"].mean()), c1_ii=float(re_["Agent13"].mean()), c1_dp=dp, c1_dplo=dlo)
            say(f"   (c1) BARS, walls off: (i) lower bound {res[(False, 'Agent13')][2]:.4f} >= 0.40 -> {'PASS' if res[(False, 'Agent13')][2] >= 0.40 else 'FAIL'};"
                f" (ii) lower bound {res[(False, 'Agent13')][3]:.4f} >= 0.30 -> {'PASS' if res[(False, 'Agent13')][3] >= 0.30 else 'FAIL'};"
                f" (iii) lower bound {dlo:+.4f} >= +0.30 -> {'PASS' if dlo >= 0.30 else 'FAIL'}; floor (Agent10) (i) {wi['Agent10'].mean():.3f}; ceiling (oracle) (i) {wi['oracle'].mean():.3f}, (ii) {re_['oracle'].mean():.3f}")
    for klass, wins in (("c2", (300, 600)), ("c3", (600, 1800))):
        for walls in (False, True):
            parts = []
            for k in ("Agent10", "Agent13", "oracle"):
                o = C[(klass, walls, k)]; wv = [int(o["W"][:t].any((0, 2)).sum()) for t in wins]; rv = [int(o["AT2"][:t].any((0, 2)).sum()) for t in wins]
                parts.append(f"{k}: whiff by {wins[0]}/{wins[1]} {wv[0]}/{wv[1]}, reached by {wins[0]}/{wins[1]} {rv[0]}/{rv[1]} (= {rv[0]/n:.3f}/{rv[1]/n:.3f}), contacts per row {o['contacts'].mean():.3f},"
                             f" engaged rows {int(o['ENG'].any(0).sum())}")
            say(f"   ({klass}) {'upwind of the sources' if klass == 'c2' else 'the H16 cold-start square'}, {'walls OFF' if not walls else 'walls ON'}, {BENCH['steps_' + klass]} steps, REPORTED: " + "; ".join(parts))
    o2 = C[("c2", False, "Agent13")]
    say(f"   (c2) reading R2 check: Agent13 engaged on step index 0 in {int(o2['ENG'][0].sum())}/{n} rows with u {sorted(set(o2['U'][0][o2['ENG'][0]].astype(int).tolist()))}")
    # (d)
    say(f"(d) no false engagement: any-odour silence (q from the recorded whiffs) for Agent10, and Agent13's engaged rows")
    for lab, o in (("World7 +1/0 Agent10", T1[("Agent10", (1.0, 0.0))]), ("World7 +1/-1 Agent10", T1[("Agent10", (1.0, -1.0))]),
                   ("stub p 0.057 Agent10", stub(Agent10, kn, [(BENCH["steps"], 0.057, 0.057)])), ("stub p 0.30 Agent10", stub(Agent10, kn, [(BENCH["steps"], 0.30, 0.30)]))):
        Q = qrec(o["W"]); mx = Q.max(0)
        say(f"   [{lab}] longest any-odour silence per row: quartiles {q3(mx)}, p90 {np.percentile(mx, 90):.0f}, p95 {np.percentile(mx, 95):.0f}, max {mx.max():.0f}; rows reaching q >= 150/180/210/250/300: "
            + "/".join(str(int((mx >= c).sum())) for c in (150, 180, 210, 250, 300)) + "; fraction of (row, step) with q >= 150/180/210/250/300: " + "/".join(f"{(Q >= c).mean():.5f}" for c in (150, 180, 210, 250, 300)))
    for lab, v in (("+1/0", (1.0, 0.0)), ("+1/-1", (1.0, -1.0))):
        o = T1[("Agent13", v)]; er = o["ENG"].any(0); k_, pt, lo, hi = interval("P", er)
        mx10 = qrec(T1[("Agent10", v)]["W"]).max(0); same = bool(np.array_equal(er, mx10 >= S_RUN2))
        say(f"   [World7 {lab} Agent13] rows with any engaged step {fmt_ci(k_, n, pt, lo, hi)}; engaged (row, step) {int(o['ENG'].sum())}; first engaged step {q3(first_true(o['ENG'])[er])};"
            f" the engaged rows are exactly the rows whose Agent10 silence reaches 250: {same}"
            + (f" -> bar upper bound <= 0.05: {'PASS' if hi <= 0.05 else 'FAIL'} (pass probability, exact binomial P(K <= 11 of 400) at p {pt:.4f}, reading R13: {pp_d(k_):.4f})" if v == (1.0, 0.0) else " (reported)"))
        if v == (1.0, 0.0): bars["d engaged rows T1 +1/0 (upper <= 0.05)"] = hi; out.update(d_hi=hi, d_k=k_, d_pp=pp_d(k_))
    for pp_ in (0.057, 0.30):
        o = stub(Agent13, kn, [(BENCH["steps"], pp_, pp_)]); say(f"   [stub p {pp_} Agent13] engaged (row, step) {int(o['ENG'].sum())}; == Agent10 bitwise {bitwise(o, stub(Agent10, kn, [(BENCH['steps'], pp_, pp_)]))}")
    # (h1)
    o13, o10 = T1[("Agent13", (1.0, 0.0))], T1[("Agent10", (1.0, 0.0))]; V13, V10 = majority(o13)[0], majority(o10)[0]; c13, c10 = cls3(o13), cls3(o10)
    P1, dp1, b1, sd1, P1m = pp_dp(V13, V10, -0.05, False); _, _, blo, bhi = interval("DP", V13.astype(float), V10.astype(float)); stop1 = P1 < 0.5
    e_ = o13["ENG"].any(0); l13, l10 = lost(o13), lost(o10)
    say(f"(h1) T1 on bench seeds, World7 +1/0 {n} x {BENCH['steps']}: " + "; ".join(f"{k} V {int(majority(o)[0].sum())} N {int(majority(o)[1].sum())} tie {int(majority(o)[2].sum())} P(V) "
        f"{interval('P', majority(o)[0])[1]:.3f} [{interval('P', majority(o)[0])[2]:.3f}, {interval('P', majority(o)[0])[3]:.3f}]" for k, o in (("Agent13", o13), ("Agent10", o10))))
    say(f"   (h1) paired DP P(V) Agent13 - Agent10 {dp1:+.4f} [{blo:+.4f}, {bhi:+.4f}] (bootstrap 5000, seed {ph15.BOOT_SEED}); engaged rows {int(e_.sum())}; into V {int(((c13 == 0) & (c10 != 0)).sum())},"
        f" out of V {int(((c13 != 0) & (c10 == 0)).sum())}; V among engaged rows Agent13 {int(V13[e_].sum())} vs Agent10 {int(V10[e_].sum())}; lost rows {int(l13.sum())} vs {int(l10.sum())};"
        f" contacts per row {o13['contacts'].mean():.3f} vs {o10['contacts'].mean():.3f}")
    say(f"   (h1) M1 (b)'s pass probability (lower bound >= -0.05) at the bench DP {dp1:+.4f}, discordant b {b1:.4f}, sd sqrt(b - DP^2) {sd1:.4f}: {P1:.4f} (with the measured paired sd: {P1m:.4f})")
    say(f"   (h1) STOP RULE (design section 4): pass probability {P1:.4f} {'< 0.5 -> STOP: the run returns to the owner after the bench record' if stop1 else '>= 0.5 -> continue'}")
    # (h2)
    o13, o10 = T1[("Agent13", (1.0, -1.0))], T1[("Agent10", (1.0, -1.0))]; V13, V10 = majority(o13)[0], majority(o10)[0]; l13, l10 = lost(o13), lost(o10)
    P2, dp2, b2, sd2, P2m = pp_dp(l13, l10, -0.05, True); _, _, llo, lhi = interval("DP", l13.astype(float), l10.astype(float)); stop2 = P2 < 0.5
    Pb, dpv, bv, sdv, Pbm = pp_dp(V13, V10, -0.02, False); _, _, vlo, vhi = interval("DP", V13.astype(float), V10.astype(float))
    cm = o13["contacts"].mean(); e_ = o13["ENG"].any(0); c13, c10 = cls3(o13), cls3(o10)
    _, r10, _ = released(o10); _, r13, _ = released(o13); s10, s13 = np.unique(r10), np.unique(r13)
    say(f"(h2) T3 on bench seeds, World7 +1/-1 {n} x {BENCH['steps']}: " + "; ".join(f"{k} V {int(majority(o)[0].sum())} N {int(majority(o)[1].sum())} tie {int(majority(o)[2].sum())},"
        f" lost rows {int(lost(o).sum())}, contacts per row {o['contacts'].mean():.3f}" for k, o in (("Agent13", o13), ("Agent10", o10))))
    say(f"   (h2) stranded rows (a drive-ended negative hold, as R3): Agent10 {len(s10)} (releases {len(r10)}), Agent13 {len(s13)}; Agent13 engaged rows {int(e_.sum())}, engaged (row, step) {int(o13['ENG'].sum())};"
        f" lost among Agent10's stranded rows: Agent10 {int(l10[s10].sum())}, Agent13 {int(l13[s10].sum())}")
    say(f"   (h2) lost-row paired DP Agent13 - Agent10 {dp2:+.4f} [{llo:+.4f}, {lhi:+.4f}]; P(V) paired DP {dpv:+.4f} [{vlo:+.4f}, {vhi:+.4f}]; contacts per row {cm:.3f};"
        f" into V {int(((c13 == 0) & (c10 != 0)).sum())}, out of V {int(((c13 != 0) & (c10 == 0)).sum())}; out of lost {int((l10 & ~l13).sum())}, into lost {int((l13 & ~l10).sum())}")
    say(f"   (h2) M3 (a)'s pass probability (upper bound <= -0.05) at the bench DP {dp2:+.4f}, discordant b {b2:.4f}, sd {sd2:.4f}: {P2:.4f} (measured paired sd: {P2m:.4f});"
        f" reported: M3 (b) (lower bound >= -0.02) at {dpv:+.4f}, b {bv:.4f}: {Pb:.4f} (measured sd: {Pbm:.4f})")
    say(f"   (h2) STOP RULE (design section 4): pass probability {P2:.4f} {'< 0.5 -> STOP: the run returns to the owner after the bench record' if stop2 else '>= 0.5 -> continue'}")
    # (h2) added, reported
    fe = first_true(o13["ENG"]); cr = o13["contacts"] > 0; crow = np.flatnonzero(cr)
    say(f"   (h2) added, reported: contacts {int(o13['C'].sum())} in {int(cr.sum())} rows; by leg {contacts_by_leg(o13)}; P(V | contact) {fmt_ci(*interval('P', V13[cr])[:1], int(cr.sum()), *interval('P', V13[cr])[1:]) if cr.any() else 'n/a'};"
        f" contact rows lost {int(l13[cr].sum())}, Agent10-stranded {int(np.isin(crow, s10).sum())}")
    out_, med, noeng, nowh = m3c(o13, o10); nout, kmed = int(out_.sum()), int(med.sum()); P2c = pp_m3c(nout, kmed); stop2c = P2c < 0.5
    anyc = int((out_ & cr).sum())
    say(f"   (h2) M3 (c) re-signed (reading R9): rows leaving lost {nout} (readable if >= 20: {nout >= 20}); contact-mediated (a contact before the first whiff after the first engaged step)"
        f" {kmed} -> fraction {kmed/nout if nout else float('nan'):.4f} (bar point <= 0.10); rows leaving lost with no engaged step {noeng}, with no whiff after it {nowh} (expected 0);"
        f" rows leaving lost with any contact in the row {anyc} (reported)")
    say(f"   (h2c) STOP RULE (design section 4): M3 (c)'s pass probability (reading R10, exact binomial P(K <= {nout//10} of {nout}) at {kmed/nout if nout else 0:.4f}) {P2c:.4f}"
        f" {'< 0.5 -> STOP: the run returns to the owner after the bench record' if stop2c else '>= 0.5 -> continue'}")
    se_ = np.array([r for r in s10 if fe[r] >= 0], int)
    dsq = np.array([o13["SINCE"][fe[r], r] - o13["Q"][fe[r], r] for r in se_]) if len(se_) else np.array([])
    say(f"   (h2) `since` - q at the first engaged step in Agent10-stranded rows engaged in Agent13 ({len(se_)}): {q3(dsq)} (min {int(dsq.min()) if len(dsq) else 0}, max {int(dsq.max()) if len(dsq) else 0});"
        f" equal to 0 in {int((dsq == 0).sum())}/{len(dsq)}; first engaged step - first release {q3(np.array([fe[r] - min(ee for ee, x in zip(released(o10)[0], r10) if x == r) for r in se_]))}")
    fm = [flee_side_match(o13, r, int(fe[r])) for r in crow if fe[r] >= 0]; fs_all = [flee_side_match(o13, r, int(fe[r])) for r in se_]
    say(f"   (h2) sigma_1 pointed to the flee_side side (reading R12): contact rows {sum(fm)}/{len(fm)}; engaged Agent10-stranded rows {sum(fs_all)}/{len(fs_all)}")
    if len(se_):
        fo, reneg, restr = neg_after(o13, se_, fe)
        say(f"   (h2) engaged stranded rows {len(se_)}: first whiff after the first engaged step valued {fo.count('valued')}, negative {fo.count('other')}, both {fo.count('both')}, none {fo.count('none')};"
            f" a negative hold re-formed after engagement {int(reneg.sum())}; stranded again {int(restr.sum())}; Agent13 V {int(V13[se_].sum())}, lost {int(l13[se_].sum())} (Agent10 V {int(V10[se_].sum())}, lost {int(l10[se_].sum())})")
    out.update(h1_dp=dp1, h1_pp=P1, h2_dp=dp2, h2_pp=P2, h2_pv=dpv, h2c_pp=P2c, h2c_n=nout, h2c_k=kmed, stop1=stop1, stop2=stop2, stop2c=stop2c)
    # (h3)
    o13w, o10w = WT["W1"]; s13, s10w = w1sum(o13w), w1sum(o10w); d = s13["dwell"].astype(float) - s10w["dwell"].astype(float)
    P3, dp3, sd3 = pp_cont(d, -1.2, False); _, _, wlo, whi = interval("DP", s13["dwell"].astype(float), s10w["dwell"].astype(float)); stop3 = P3 < 0.5; ew = o13w["ENG"].any(0)
    say(f"(h3) W1 on bench seeds (ph22.Masked, +1/0, {n} x {BENCH['steps']}): engaged rows {int(ew.sum())} (first engaged step {q3(first_true(o13w['ENG'])[ew])}); dwell at the present source mean"
        f" Agent13 {s13['dwell'].mean():.3f}, Agent10 {s10w['dwell'].mean():.3f}; paired dwell Agent13 - Agent10 {dp3:+.3f} [{wlo:+.3f}, {whi:+.3f}] (bootstrap), sd {sd3:.3f}; rows differing"
        f" {int((d != 0).sum())} (all engaged: {bool(((d != 0) <= ew).all())}); reach {int(s13['reach'].sum())}/{int(s10w['reach'].sum())}; lost rows {int(s13['lost'].sum())}/{int(s10w['lost'].sum())}")
    say(f"   (h3) STOP RULE (design section 4): M2 (a)'s pass probability (lower bound >= -1.2; reading R11) {P3:.4f} {'< 0.5 -> STOP: the run returns to the owner after the bench record' if stop3 else '>= 0.5 -> continue'}")
    out.update(h3_dp=dp3, h3_sd=sd3, h3_pp=P3, stop3=stop3)
    # verdict
    idok = all(ids.values()); cb = {k: v for k, v in bars.items() if k.startswith("c1")}
    cok = cb["c1 (i) whiff within 300, Agent13 (>= 0.40)"] >= 0.40 and cb["c1 (ii) reach within 600, Agent13 (>= 0.30)"] >= 0.30 and cb["c1 (iii) paired DP (i) Agent13 - Agent10 (>= +0.30)"] >= 0.30
    bok, bpok, dok = bars["b"] >= 0.95, bars["b'"] >= 0.95, bars["d engaged rows T1 +1/0 (upper <= 0.05)"] <= 0.05
    cand = idok and bok and bpok and cok and dok; stops = {"h1": (stop1, P1), "h2": (stop2, P2), "h2c": (stop2c, P2c), "h3": (stop3, P3)}; anystop = any(s for s, _ in stops.values())
    B = cand and not anystop; out.update(ids=idok, b=bok, bp=bpok, c1=cok, d=dok, cand=cand, B=B)
    bpl = bars["b'"]
    say(f"== B: (a) identities {idok} (failed {[k for k, v in ids.items() if not v]}); (b) exact {bok} (lower bound {bars['b']:.4f}); (b') exact {bpok} (lower bound {bpl:.4f});"
        f" (c1) bars {cok} " + str({k: round(float(v), 4) for k, v in cb.items()}) + f"; (d) {dok} (upper bound {bars['d engaged rows T1 +1/0 (upper <= 0.05)']:.4f}); stop rules "
        + ", ".join(f"({k}) {'STOP' if s else 'continue'} ({pv:.4f})" for k, (s, pv) in stops.items())
        + f" -> B {'PASS: the tasks may be run' if B else ('FAIL, NO CANDIDATE: the search as specified does not do what section 3 says (or (d) fails); the tasks are NOT run' if not cand else 'NOT passed: a registered stop rule fired; the tasks are NOT run and the run returns to the owner')} ==")
    return B, out


# ------------------------------------------------------------------ self-checks
def seeds_unused():
    """design section 9: none of the fifteen numbers appears in any other file under the repository (recursive, digit-boundary; .git and
    __pycache__ excluded; excluded by name: this file, its outputs ph27_*.txt, the Run 2 documents h17_run2_*.md, master_plan.md,
    notes/*.md, viewer/*). The demo seeds 5/6 are used deliberately and are NOT part of this check."""
    base = [*SEEDS["dev"], *SEEDS["eval"], BENCH["seed_w"], BENCH["seed_a"], ph15.BOOT_SEED]
    derived = [s + 10_000 for s in (SEEDS["dev"][0], SEEDS["eval"][0], BENCH["seed_w"])] + [s + 20_000 for s in (SEEDS["dev"][1], SEEDS["eval"][1], BENCH["seed_a"])]
    nums = base + derived + [BENCH["seed_w"] + 10_000_000, BENCH["seed_a"] + 20_000_000]
    pat = re.compile(rb"(?<!\d)(" + "|".join(map(str, nums)).encode() + rb")(?!\d)"); hits = []; nf = 0
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        top = os.path.relpath(root, repo).replace("\\", "/").split("/")[0]
        for f in files:
            if f == "ph27.py" or (f.startswith("ph27_") and f.endswith(".txt")) or (f.startswith("h17_run2_") and f.endswith(".md")) or f == "master_plan.md": continue
            if (os.path.basename(root) == "notes" and f.endswith(".md")) or top == "viewer": continue
            nf += 1
            if pat.search(open(os.path.join(root, f), "rb").read()): hits.append(os.path.relpath(os.path.join(root, f), repo))
    return hits, nums, nf


def header(say=print):
    say(f"   ph27.py sha256 {sha()}; ph26.py sha256 {sha(ph26.__file__)} (Run 1's recorded {PH26_SHA[:8]}...{PH26_SHA[-4:]}: {sha(ph26.__file__) == PH26_SHA}); design {DESIGN}")
    say("   imported modules: " + "; ".join(f"{os.path.basename(m.__file__)} {sha(m.__file__)}" for m in MODS))
    say(f"   seeds: dev {SEEDS['dev']}, eval {SEEDS['eval']}, bench {BS}, bootstrap {ph15.BOOT_SEED}; demo seeds (5, 6) used deliberately, NOT part of the seed scan; no reproduction seed used")
    say("   decisions: decision:h17-run2-open; decision:classification-rule-relaxed-any-odour-silence-counter-h17-run2; decision:h17-t3c-bar-resigned-run2")


def demo():
    print(f"== H17 Run 2 self-checks (demo). design {DESIGN} ==")
    header()
    print("   fixed before this recorded demo: none (see the episode for the code-path test)")
    assert sha(ph26.__file__) == PH26_SHA, "ph26.py differs from Run 1's recorded file"
    print(f"ok  ph26.py is Run 1's file, unchanged (sha256 {PH26_SHA})")
    n, st = 40, 200; kw = dict(runs=n, steps=st); sd = (5, 6); sp = [(st, 0.30, 0.30)]; kn = [1.0, 0.0]
    for cls in (Agent10, Agent10g, Agent8, Agent6, Agent12):
        ph24.record, ph24.make = _record26, _make26; a = ph24.run("T1", cls, (1.0, 0.0), sd, **kw); sa = ph24.stub(cls, kn, sp, rows=n, seeds=sd)
        ph24.record, ph24.make = record, make; b = ph24.run("T1", cls, (1.0, 0.0), sd, **kw); sb = ph24.stub(cls, kn, sp, rows=n, seeds=sd)
        assert all(np.array_equal(a[k], b[k]) for k in a if isinstance(a[k], np.ndarray)), f"a hook changed a ph24.run field ({cls.__name__})"
        assert all(np.array_equal(sa[k], sb[k]) for k in sa if isinstance(sa[k], np.ndarray)), f"a hook changed a ph24.stub field ({cls.__name__})"
    print("ok  the ph27 make and record hooks leave every field of ph24.run and ph24.stub bitwise equal to ph26's hooks alone (World7 40 x 200 and stub; Agent10, Agent10g, Agent8, Agent6, ph26.Agent12)")
    for cls, base in ((Agent13, Agent10), (Agent13g, Agent10g)):
        assert bitwise(run("T1", cls, (1.0, 0.0), sd, search=False, **kw), run("T1", base, (1.0, 0.0), sd, **kw)), f"{cls.__name__} search off is not {base.__name__}"
        assert bitwise(stub(cls, kn, sp, search=False, rows=n, seeds=sd), stub(base, kn, sp, rows=n, seeds=sd)), f"{cls.__name__} search off (stub) is not {base.__name__}"
        assert bitwise(stub(cls, kn, sp, rows=n, seeds=sd), stub(base, kn, sp, rows=n, seeds=sd)), f"{cls.__name__} stub (never engaged) is not {base.__name__}"
    print("ok  search=False: Agent13 == Agent10 and Agent13g == Agent10g bitwise (World7 and stub, 40 x 200); search True in the stub at p 0.30 == the base (never engaged)")
    sil = [(400, 0.0, 0.0)]
    a, b = stub(Agent13at210, kn, sil, rows=n, seeds=sd), stub(Agent12, kn, sil, rows=n, seeds=sd); assert bitwise(a, b, SFIELDS) and (first_true(a["ENG"]) == 209).all(), "(a4) stub"
    a, b = run("T1", Agent13at210, (1.0, -1.0), sd, runs=n, steps=400), run("T1", Agent12, (1.0, -1.0), sd, runs=n, steps=400); assert bitwise(a, b, SFIELDS), "(a4) World7"
    print(f"ok  (a4) Agent13's code at S 210 == ph26.Agent12 bitwise on every field incl. the search fields (stub silence 40 x 400, first engaged index 209; World7 +1/-1 40 x 400,"
          f" engaged rows {int(a['ENG'].any(0).sum())})")
    assert ph26.S_ON == 210, "ph26's module constant restored"
    print("ok  ph26.S_ON is 210 after every call (restored by Search13.act and the s_on helper)")
    for lab, sched, first in (("silence from construction", [(400, 0.0, 0.0)], 249), ("one whiff at step 0", [(1, 1.0, 0.0), (399, 0.0, 0.0)], 250)):
        o = stub(Agent13, kn, sched, rows=n, seeds=sd); ex, hq = engagement_exact(o); fe = first_true(o["ENG"])
        assert ex.all() and hq == 0 and (fe == first).all() and o["ENG"][first:].all(), f"engagement ({lab}): exact {int(ex.sum())}, held {hq}, first {set(fe.tolist())}"
        ex210, _ = engagement_exact(o, S=210); assert not ex210.any(), "the check at S 210 must reject an S 250 record"
        print(f"ok  stub {lab}, 40 rows x 400: engagement exact at S 250 in every row; first engaged step index {first}; engaged to the end; q >= S with a hold 0; the same check at S 210 rejects every row")
    o = stub(Agent13, [1.0, -1.0], [(20, 0.0, 0.30), (380, 0.0, 0.0)], rows=n, seeds=sd); ex, hq = engagement_exact(o); fe = first_true(o["ENG"]); held = o["H"] == 1
    anyw = o["W"].any(2); wh = anyw.any(0); lastw = np.where(wh, 399 - np.argmax(anyw[::-1], 0), -1); r_ = np.arange(n)
    assert ex.all() and (held.any(0) == wh).all() and np.where(held, o["TGT"] == o["FS"], True).all() and np.where(wh, fe - lastw == 250, fe == 249).all(), "(b'2) construction / engagement"
    print(f"ok  (b'2) schedule 40 x 400: a negative hold forms in every row with a whiff ({int(wh.sum())}), target == flee_side on every held step, engagement exact and 250 steps after the last whiff."
          f" Printed, not asserted (the bench measures it): `since` - q on the first engaged step {q3(o['SINCE'][fe, r_] - o['Q'][fe, r_])}")
    o = run("T1", Agent13, (1.0, 0.0), sd, runs=n, steps=400); ok, cnt = row_identity(o, run("T1", Agent10, (1.0, 0.0), sd, runs=n, steps=400)); ex, hq = engagement_exact(o)
    assert ok and ex.all(), f"World7 row identity {cnt}"
    print(f"ok  World7 +1/0 40 x 400: never-engaged rows bitwise Agent10, engaged rows equal before their first engaged step {cnt}; engagement exact in every row (q >= S with a hold: {hq})")
    c = {k: cold("c1", cl, False, seeds=sd, runs=n, steps=320) for k, cl in (("Agent10", Agent10), ("Agent13", Agent13), ("oracle", AgentO))}
    assert all(np.array_equal(c[k]["start"], c["Agent10"]["start"]) for k in c) and not inside(c["Agent10"]["start"], c["Agent10"]["src"]).any()
    pre = c["Agent13"]["W"][:E_C1].any((0, 2)); fe = first_true(c["Agent13"]["ENG"]); ex, _ = engagement_exact(c["Agent13"], q0=BENCH["q_c1"])
    assert E_C1 == 204 and ex.all() and (fe[~pre] == 204).all(), f"(c1) engagement at step index 204 in rows without an earlier whiff {set(fe[~pre].tolist())}"
    ok, cnt = row_identity(c["Agent13"], c["Agent10"]); assert ok, f"(c1) Agent13 vs Agent10 before engagement {cnt}"
    print(f"ok  (c1) construction 40 rows: identical start in every arm, outside both whiff regions; Agent13 engaged at step index 204 in every row without an earlier whiff"
          f" ({int((~pre).sum())} rows), engagement exact, equal to Agent10 before it {cnt}")
    o2 = cold("c2", Agent13, False, seeds=sd, runs=n, steps=5); assert o2["ENG"][0].all() and (o2["U"][0] == 1).all(), "(c2) reading R2"
    print("ok  (c2) q = since = 250 at construction: engaged on step index 0 with u = 1 in every row (reading R2)")
    cn = cold("c1", Agent13, False, seeds=sd, runs=n, steps=50); assert not cn["C"].any()
    print("ok  walls off: no contact is ever registered (40 x 50)")
    for wd in ("W1", "T3a"):
        o = run(wd, Agent13, (1.0, 0.0), sd, **kw); ok, cnt = row_identity(o, run(wd, Agent10, (1.0, 0.0), sd, **kw)); assert ok and o["draws_equal"] and o["rng_equal"], wd
    print("ok  W1 and T3a (40 x 200): row identity vs Agent10 and the masked draws == the World7 twin")
    # the re-signed T3 (c) statistic on a constructed record (reading R9)
    st_, nn = 600, 6; W = np.zeros((st_, nn, 2), bool); E = np.zeros((st_, nn), bool); Cc = np.zeros((st_, nn), bool)
    W[450, 0, 0] = True; E[300:450, 0] = True; Cc[320, 0] = True              # row 0: contact after engagement, before the whiff -> mediated
    W[450, 1, 1] = True; E[300:450, 1] = True; Cc[460, 1] = True              # row 1: contact after the whiff -> not mediated
    W[450, 2, 0] = True; E[300:450, 2] = True; Cc[200, 2] = True              # row 2: contact before engagement -> not mediated
    W[450, 3, 0] = True; E[300:450, 3] = True; Cc[449, 3] = True              # row 3: contact on the move after the last pre-whiff step -> mediated
    W[450, 4, 0] = True                                                       # row 4: never engaged (not leaving lost in a real run)
    o13 = dict(W=W, ENG=E, C=Cc, H=np.full((st_, nn), -1)); o10 = dict(W=np.zeros((st_, nn, 2), bool), H=np.full((st_, nn), -1))
    out_, med, noeng, nowh = m3c(o13, o10)
    assert out_[:5].all() and not out_[5] and med.tolist() == [True, False, False, True, False, False] and noeng == 1 and nowh == 0, (med, noeng, nowh)
    print("ok  T3 (c) statistic (reading R9) on a constructed record: a contact between the first engaged step and the first whiff after it counts (incl. the move after the"
          " last step before the whiff); a contact after the whiff or before engagement does not; a row without engagement is counted apart")
    p_d = pp_d(6); p_c = (pp_m3c(35, 0), pp_m3c(35, round(0.05*35)), binom_cdf(3, 35, 0.05), binom_cdf(3, 35, 0.094))
    assert abs(p_d - 0.981) < 0.002 and abs(p_c[2] - 0.90) < 0.01 and abs(p_c[3] - 0.58) < 0.015 and p_c[0] == 1.0, (p_d, p_c)
    print(f"ok  exact binomial pass probabilities reproduce the design's arithmetic: (d) P(K <= 11 of 400) at 6/400 = {p_d:.3f} (design 0.981); T3 (c) with 35 rows leaving lost:"
          f" f 0 -> {p_c[0]:.3f}, f 0.05 -> {p_c[2]:.3f} (design 0.90), f 0.094 -> {p_c[3]:.3f} (design 0.58)")
    hits, nums, nf = seeds_unused(); assert not hits, f"a seed of this run appears in {hits}"
    print(f"ok  seeds {nums} appear in no other file under the repository ({nf} files scanned; excluded by name ph27.py, ph27_*.txt, h17_run2_*.md, master_plan.md, notes/*.md, viewer/*)")


# ------------------------------------------------------------------ the tasks (design sections 5-8)
T1ARMS = {"search": Agent13, "base": Agent10, "search-gate": Agent13g, "base-gate": Agent10g}
T2ARMS = {"search": Agent13, "base": Agent10, "reference": Agent6}
T3ARMS = {"search": Agent13, "base": Agent10, "wall-reflex base": Agent8, "search-gate": Agent13g, "base-gate": Agent10g}
T4ARMS = {"search": Agent13, "base": Agent10, "ceiling": None}


def main(mode):
    seeds = SEEDS[mode]; rows = np.arange(R)
    print(f"== H17 Run 2, {mode.upper()}. design {DESIGN}; G {G_STAR}, gate on; S {S_RUN2}; world seed {seeds[0]}, agent seed {seeds[1]}; {R} rows x {T} steps; geometry C0;"
          f" bootstrap seed {ph15.BOOT_SEED}; {'operation check only (not a verdict)' if mode == 'dev' else 'the one evaluation'} ==")
    header()
    hits, nums, nf = seeds_unused(); print(f"   seed self-check: every H17 Run 2 seed and derived in no other file ({nf} scanned): {not hits}{'' if not hits else ' ' + str(hits)}")
    print("   amendments: none")
    print("   rows share no state: one generator per world and one per agent population, fixed-size draws consumed in row order every step")
    print("\n== B, the mechanism bench, re-run first with the bench seeds (section 4; the tasks run only if B passes) ==")
    lines = []; B, bo = bench(say=lines.append)
    for ln in lines:
        if ln.startswith("== B") or ln.startswith("(b) engagement exact") or ln.startswith("(b') engaged") or "(c1) BARS" in ln or "bar upper bound" in ln or "STOP RULE" in ln or "pass probability" in ln:
            print("   " + ln.strip())
    if not B:
        print("\n== B did not pass: the tasks are NOT run (design section 4 / 8). =="); return
    t1 = {a: run("T1", c, (1.0, 0.0), seeds) for a, c in T1ARMS.items()}; maj = {a: majority(t1[a]) for a in t1}
    print("\n== T1, the H21 choice task (+1/0) ==")
    for a, o in t1.items():
        describe_majority(a, o, *maj[a]); h21_diag(a, o)
        if "ENG" in o and o["SRCH"]: er = o["ENG"].any(0); print(f"      [{a}] engaged rows {int(er.sum())}/{R}, engaged (row, step) {int(o['ENG'].sum())}, first engaged step {q3(first_true(o['ENG'])[er])}")
    print("\n== T2, the absent-odour world W1 (valued column masked from step 0) ==")
    t2 = {a: run("W1", c, (1.0, 0.0), seeds) for a, c in T2ARMS.items()}; s2 = {a: w1sum(o) for a, o in t2.items()}
    for a, o in t2.items():
        s = s2[a]; print(f"   [W1 {a} {o['arm']}] dwell at the present source mean {s['dwell'].mean():.3f} (quartiles {q3f(s['dwell'].astype(float))}); reach {int(s['reach'].sum())}/{R};"
                         f" lost rows {int(s['lost'].sum())}; wall contacts per row {s['contacts'].mean():.3f}; engaged rows {int(o['ENG'].any(0).sum())}; draws == twin {o['draws_equal'] and o['rng_equal']}")
    print("\n== T3, the +1/-1 stranded condition (World7 at +1/-1) ==")
    t3 = {a: run("T1", c, (1.0, -1.0), seeds) for a, c in T3ARMS.items()}; m3 = {a: majority(o) for a, o in t3.items()}; L3 = {a: lost(o) for a, o in t3.items()}
    st = {a: released(o) for a, o in t3.items()}
    for a, o in t3.items():
        V, N, Z = m3[a]; E, Rr, _ = st[a]; sr = np.unique(Rr); wc = o["contacts"] > 0
        after = np.array([bool(o["W"][e + 1:, r].any()) for e, r in zip(E, Rr)], bool); left = T - 1 - E
        pvw = f"{V[wc].mean():.3f} ({int(V[wc].sum())}/{int(wc.sum())})" if wc.any() else "n/a"
        print(f"   [T3 {a} {o['arm']}] V {int(V.sum())} N {int(N.sum())} tie {int(Z.sum())}; lost rows {int(L3[a].sum())}; wall contacts per row {o['contacts'].mean():.3f} (rows with any {int(wc.sum())});"
              f" P(V | wall contact) {pvw}; stranded rows {len(sr)} (drive-ended negative holds {len(E)}); any whiff after the release {int(after.sum())}/{len(E)}, among releases with >= 200 steps left"
              f" {int(after[left >= 200].sum())}/{int((left >= 200).sum())}; engaged rows {int(o['ENG'].any(0).sum())}")
    o13 = t3["search"]; fe = first_true(o13["ENG"]); s10 = np.unique(st["base"][1]); se_ = np.array([r for r in s10 if fe[r] >= 0], int)
    print(f"      [T3 search] contacts by leg {contacts_by_leg(o13)}; lost among the base's stranded rows: search {int(L3['search'][s10].sum())}, base {int(L3['base'][s10].sum())}")
    if len(se_):
        fo, reneg, restr = neg_after(o13, se_, fe); dsq = np.array([o13["SINCE"][fe[r], r] - o13["Q"][fe[r], r] for r in se_])
        print(f"      [T3 search] engaged stranded rows {len(se_)}: first whiff after engagement valued {fo.count('valued')}, negative {fo.count('other')}, both {fo.count('both')}, none {fo.count('none')};"
              f" negative hold re-formed {int(reneg.sum())}; stranded again {int(restr.sum())}; `since` - q at the first engaged step {q3(dsq)} (0 in {int((dsq == 0).sum())})")
    print("\n== T4, the constructed loss T3a (reported) ==")
    t4 = {a: (run("T3a", c, (1.0, 0.0), seeds) if c is not None else run("T3a", None, (1.0, 0.0), seeds, fixed="neutral")) for a, c in T4ARMS.items()}
    D4 = {a: t3_dwell(o, 100, T) for a, o in t4.items()}
    for a, o in t4.items():
        g = o["good"]; dv = np.linalg.norm(o["POS"] - o["src"][rows, g][None], axis=2)
        print(f"   [T4 {a} {o['arm']}] neutral dwell 100-599 mean {D4[a].mean():.3f} (quartiles {q3f(D4[a])}); steps within 10 of the valued source per row {(dv < 10).sum(0).mean():.1f};"
              f" distance to the valued source median at steps 100/300/599 {np.median(dv[100]):.1f}/{np.median(dv[300]):.1f}/{np.median(dv[599]):.1f};"
              f" engaged-step fraction {o['ENG'].mean():.4f}")
    judge(seeds, B, t1, maj, t2, s2, t3, m3, L3, st, t4, D4)


def judge(seeds, B, t1, maj, t2, s2, t3, m3, L3, st, t4, D4):
    ok = lambda z: "PASS" if z else "FAIL"
    print("\n== criteria (design v2 FINAL section 7; 95 percent, one evaluation, no extension; aggregation: PASS if every part passes, FAIL if any fails, else INCONCLUSIVE; the unrounded bound decides) ==")
    Bv = "PASS" if B else "FAIL"; print(f"   B bench -> {Bv}")
    i = {}
    i["T1 search False == Agent10"] = bitwise(run("T1", Agent13, (1.0, 0.0), seeds, search=False), t1["base"])
    i["T1 Agent13g search False == Agent10g"] = bitwise(run("T1", Agent13g, (1.0, 0.0), seeds, search=False), t1["base-gate"])
    cnts = {}
    for lab, a, b in (("T1", t1["search"], t1["base"]), ("T1 gate", t1["search-gate"], t1["base-gate"]), ("T2", t2["search"], t2["base"]), ("T3", t3["search"], t3["base"]),
                      ("T3 gate", t3["search-gate"], t3["base-gate"]), ("T4", t4["search"], t4["base"])):
        ok_, cnt = row_identity(a, b); i[f"{lab} never-engaged rows bitwise the base"] = ok_; cnts[lab] = cnt
        ex, hq = engagement_exact(a); i[f"{lab} engagement exact every row"] = bool(ex.all()); cnts[lab]["q>=S with a hold"] = hq
    idok = all(i.values())
    print("   identities in the run: " + "; ".join(f"{k} {v}" for k, v in i.items()) + f" -> {'all True' if idok else 'FAILED (UNREADABLE, section 8)'}")
    for k, v in cnts.items(): print(f"      {k}: {v}")
    # M1
    V13, V10 = maj["search"][0], maj["base"][0]; ties = maj["base"][2].mean(); e1 = t1["search"]["ENG"].any(0)
    print(f"   M1(a) rows bitwise Agent10 (never engaged) {cnts['T1']['never_equal']}/{R}; engaged rows {int(e1.sum())} (reported); base ties {maj['base'][2].sum()}/{R} = {ties:.3f} (unreadable above 0.20)")
    m1 = [crit("M1(b) T1 paired DP P(V) Agent13 - Agent10", "DP", -0.05, False, V13.astype(float), V10.astype(float)),
          crit("M1(c) T1 lost rows (no whiff of either plume on 400-599), Agent13 - Agent10", "DP", 0.05, True, lost(t1["search"]).astype(float), lost(t1["base"]).astype(float))]
    cm = t1["search"]["contacts"].mean(); m1.append(ok(cm <= 0.10)); print(f"   M1(c) T1 Agent13 wall contacts per row: mean {cm:.3f}  at most 0.10 -> {m1[-1]}")
    M1 = agg(m1); c13, c10 = cls3(t1["search"]), cls3(t1["base"])
    print(f"   M1 -> {M1}      reported: into V {int(((c13 == 0) & (c10 != 0)).sum())}, out of V {int(((c13 != 0) & (c10 == 0)).sum())}; P(V) Agent13 {V13.mean():.3f}, Agent10 {V10.mean():.3f},"
          f" Agent13g {maj['search-gate'][0].mean():.3f}, Agent10g {maj['base-gate'][0].mean():.3f}; lost rows {int(lost(t1['search']).sum())} vs {int(lost(t1['base']).sum())}")
    # M2
    d13, d10, d6 = (s2[a]["dwell"].astype(float) for a in ("search", "base", "reference"))
    M2 = crit("M2(a) T2 W1 paired dwell Agent13 - Agent10", "DP", -1.2, False, d13, d10)
    _, a6, a6l, a6h = interval("DP", d13, d6)
    print(f"   M2 -> {M2}      M2(b) reported: dwell Agent13 {d13.mean():.3f}, Agent10 {d10.mean():.3f}, Agent6 {d6.mean():.3f}; Agent13 - Agent6 {a6:+.3f} [{a6l:+.3f}, {a6h:+.3f}];"
          f" reach {int(s2['search']['reach'].sum())}/{int(s2['base']['reach'].sum())}/{int(s2['reference']['reach'].sum())}; lost rows {int(s2['search']['lost'].sum())}/{int(s2['base']['lost'].sum())}/"
          f"{int(s2['reference']['lost'].sum())}; contacts per row {s2['search']['contacts'].mean():.3f}/{s2['base']['contacts'].mean():.3f}/{s2['reference']['contacts'].mean():.3f} (Agent13/Agent10/Agent6);"
          f" engaged rows {int(t2['search']['ENG'].any(0).sum())}")
    # M3
    nstr = len(np.unique(st["base"][1])); readable = nstr >= 50
    print(f"   M3 readability: stranded rows in the base arm {nstr} (at least 50 -> {'readable' if readable else 'UNREADABLE'})")
    m3a = crit("M3(a) T3 lost rows, paired DP Agent13 - Agent10", "DP", -0.05, True, L3["search"].astype(float), L3["base"].astype(float)) if readable else "UNREADABLE"
    if not readable: print("   M3(a) -> UNREADABLE (fewer than 50 stranded rows in the base arm)")
    m3b = crit("M3(b) T3 P(V), paired DP Agent13 - Agent10", "DP", -0.02, False, m3["search"][0].astype(float), m3["base"][0].astype(float))
    out_, med, noeng, nowh = m3c(t3["search"], t3["base"]); nout, kmed = int(out_.sum()), int(med.sum())
    m3c_ = "UNREADABLE" if nout < 20 else ok(kmed/nout <= 0.10)
    print(f"   M3(c) T3 (re-signed, decision:h17-t3c-bar-resigned-run2; reading R9): rows leaving lost {nout}; contact-mediated {kmed}; fraction {kmed/nout if nout else float('nan'):.4f}"
          f" at most 0.10 (point) -> {m3c_}{' (fewer than 20 rows leave lost)' if nout < 20 else ''}; rows leaving lost without an engaged step {noeng}, without a whiff after it {nowh}")
    wc = t3["search"]["contacts"] > 0; V3 = m3["search"][0]
    print(f"   M3(c) reported beside it: contacts per row {t3['search']['contacts'].mean():.3f} (rows with any {int(wc.sum())}); by leg {contacts_by_leg(t3['search'])};"
          f" P(V | contact) {fmt_ci(int(V3[wc].sum()), int(wc.sum()), *interval('P', V3[wc])[1:]) if wc.any() else 'n/a'}; rows leaving lost with any contact in the row {int((out_ & wc).sum())}")
    M3 = agg([m3a, m3b, m3c_])
    _, g8, g8l, g8h = interval("DP", m3["search"][0].astype(float), m3["wall-reflex base"][0].astype(float))
    print(f"   M3 -> {M3}      reported: P(V) Agent13 {m3['search'][0].mean():.3f}, Agent10 {m3['base'][0].mean():.3f}, Agent8 {m3['wall-reflex base'][0].mean():.3f}, Agent13g {m3['search-gate'][0].mean():.3f},"
          f" Agent10g {m3['base-gate'][0].mean():.3f}; gap Agent13 - Agent8 {g8:+.3f} [{g8l:+.3f}, {g8h:+.3f}]; lost rows " + "/".join(str(int(L3[a].sum())) for a in L3) + f" ({'/'.join(L3)})")
    # M4
    _, x1, x1l, x1h = interval("DP", D4["search"], D4["base"])
    print(f"   M4 T4 (REPORTED): neutral dwell 100-599 Agent13 {D4['search'].mean():.3f}, Agent10 {D4['base'].mean():.3f}, ceiling {D4['ceiling'].mean():.3f}; Agent13 - Agent10 {x1:+.3f} [{x1l:+.3f}, {x1h:+.3f}];"
          f" engaged-step fraction Agent13 {t4['search']['ENG'].mean():.4f}")
    unread = (not idok) or ties > 0.20 or m3a == "UNREADABLE"
    parts = (Bv, M1, M2, M3); verdict = all(x == "PASS" for x in parts)
    lab = "PASS" if verdict else "UNREADABLE" if unread else "FAIL" if any(x == "FAIL" for x in parts) else "INCONCLUSIVE"
    print(f"\n== H17 Run 2 ==  B {Bv}  M1 {M1}  M2 {M2}  M3 {M3}  (M4 reported) -> {lab}"
          + (": after 250 silent steps with nothing held, a crosswind cast of growing amplitude slanted along the wind lets the adopted agent find a plume from the stranded state outside it,"
             " recovers stranded rows without that recovery passing through the wall reflex, and changes nothing where a whiff arrives within 250 steps (supplied values, G 2, C0, these worlds,"
             " learning off, the wind sensed every step; q under the H17 relaxation, re-signed in form for Run 2)" if verdict else " under the registered criteria")
          + (" [development run: operation check only, not a verdict]" if seeds == SEEDS["dev"] else ""))


if __name__ == "__main__":
    mode = ([m for m in sys.argv[1:] if m in ("demo", "bench", "dev", "eval")] or ["demo"])[0]
    if mode == "demo": demo(); sys.exit(0)
    if mode == "bench":
        B, o = bench(); sys.exit(0 if B else 3 if o["cand"] else 1)
    main(mode)
