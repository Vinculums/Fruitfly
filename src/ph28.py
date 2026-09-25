#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H26: adaptive presence, the presence prior separated from the presence window, on the adopted agent (Agent10), +1/0.

Usage: python ph28.py demo | bench | dev | eval

Design: H26 design v2 FINAL, confirmed by the owner (decision:h26-open, '권고안대로 확정하고 H26 진행', gloss 'confirm as
recommended and proceed with H26'): doc d54441658b54a6799, hash ac95c22d...9f54, stored before this file existed. The relaxation
signed for H26 only (decision:classification-rule-relaxed-presence-prior-h26); M5(d) re-signed against Agent10
(decision:h26-m5d-bar-resigned). Composition only, nothing copied, no adopted module edited (ph21.py, ph24.py), and ph23.py,
ph25.py, ph25b.py are imported unchanged:
  Agent14 = ph24.Release (the H25 release) + ph23.Agent9 (the H24 counter), whose constructor calls the base constructor with
  N = N_hi (300) and then sets the counter to N_hi - P (240; ph23.py:57 sets it to 0). Nothing else differs from ph25.Agent11.
Run-time hooks (no file edited): ph24.make and ph23.make also build Agent14 (scope from ph25's hook, P and N_hi from this module);
every other class goes through ph25b's make (Agent11's N from ph25b._N, ph25b's own N wrapper, imported), then ph25's make and
ph25's record (the counter's measurement fields P2, C2, PRES, NAV6, NAV8, DIFF, DIFF8). Worlds and runners are ph24's (T1 World7,
W1 / W3 ph22.Masked, T3a the constructed loss, T3b ph23.Lost, t0 150). BARS is filled after the bench by
decision:h26-t2-dwell-bar (the registered order, not an amendment); dev and eval refuse to run while it is unset.

Readings where the design is silent, chosen so that the identities stay exact (printed again in the bench output):
 (R1) Agent14's counter is Agent9's float array set to N_hi - P at construction (exact for these integers); P and N_hi are
      per instance, defaults 60 and 300. (P 60, N_hi 60) gives the start value 0, i.e. ph25.Agent11 (identity a1').
 (R2) 'Bitwise on every field' (a1', a5, a6, a7, M3): ph24's identity fields (POS, HEAD, S, SG, H, NAV, SINCE, TGT, SIL, TO, EV)
      plus W, NAV6, NAV8, DIFF, DIFF8 and PRES (the valued odour's presence). The counter's value C2 and the neutral odour's
      presence differ between Agent14 and Agent11 by construction (start 240 vs 0; window 300 vs 60) and do not enter nav at
      +1/0 (design 2.3); in W1 and T3a the valued column of C2 is checked to exceed Agent11 (N 60)'s by exactly 240 on every
      (row, step). In (a1') (P = N_hi = 60) C2 and P2 are included, both columns.
 (R3) The at-risk set of (m), from Agent10's T1 run: rows with no valued whiff on steps 0-58 and at least one step t with
      59 <= t < the first valued whiff (t <= 599 if none) on which a neutral whiff arrives while nothing or the neutral odour
      is held (H after that step's selection): the only steps on which Agent14 can depart from Agent11 (N 300) (design 3.2).
      The literal reading without the lower bound 59 (any such step before the first valued whiff) is printed beside it.
 (R4) A row 'departs from Agent11 (N 300)' when it is not equal on ph24's identity fields (POS, HEAD, S, SG, H, NAV, SINCE, TGT,
      SIL, TO, EV) plus W over all 600 steps: the behaviour and the circuit. PRES is left out here because a row without a valued
      whiff by step 58 differs in the valued presence flag itself (Agent14 absent from step 59, Agent11 (N 300) present to 298)
      whether or not nav ever differs; the early-whiff rows of (a7) are compared on all of R2's fields, PRES included.
 (R5) k = Agent14's out-of-V rows minus Agent11 (N 300)'s (out of V: not V in the arm, V in Agent10). The M2 pass
      probabilities printed at k (design section 7): M2(b) at DP = -k / 400 with b = k / 400 (into V 0), sd = sqrt(b - DP^2),
      se = sd / 20; M2(a) the exact binomial P(K >= 365 of 400) at P(V) = this bench's Agent10 P(V) - k / 400 (the design's
      table used 0.958, the R2 bench's Agent10). k <= 0 reads DP 0.
 (R6) (h) pass probability (design section 7): b = the discordant fraction of the V indicator between Agent14 and Agent10,
      sd = sqrt(b - DP^2) (equal to the paired sd, ddof 0, of the V differences), se = sd / 20,
      P = Phi((DP + 0.05) / se - 1.96); sd 0: the point decides. The bootstrap interval is printed beside it.
 (R7) (h3) pass probability: ph23.pass_prob (Phi((m - bar) / se - 1.96), m the mean paired W1 dwell Agent14 - Agent6, se = sd
      (ddof 0) / 20) with bar_T2 = round(-0.20 x D6_W1, 1) from this bench's (d).
 (R8) Lost world (t0 150), the post-whiff window exact, eligible rows (a valued whiff before t0, L the last one): (i) no nav on
      a neutral-only whiff (a neutral whiff and no valued whiff) on L + 1 to L + 299; (ii) the first neutral surge after L (nav
      on a neutral whiff) is the first neutral whiff at or after L + 300; (iii) the valued odour not held on any step >= L + 60.
      Construction: draws equal to the World7 twin, generator state equal, each arm == its World7 run on steps 0-149 and
      departing from it afterwards (checked over the whole run; ph25 checked within t0 + 60).
 (R9) The pathway-off arm is ph25's: Agent8 with G 0, gate off, filter off (the design's table names it 'Agent3 (G 0, gate
      off)', as H24 Run 2's did; ph25 ran it this way).
 (R10) Agent11 at N 300 is ph25.Agent11 built through ph25b's N wrapper (ph25b._N set to 300 for the call).
 (R11) dev and eval re-run the bench on the bench seeds for M4 (as ph25 did) and read BARS for M5(b).
Nothing changes after the table.
"""
import sys, os, re, math, hashlib
from contextlib import contextmanager
import numpy as np
import ph25                                              # hooks ph24.make / ph24.record / ph23.make (sets its own bootstrap seed)
import ph25b                                             # hooks ph24.make again (Agent11's N); nothing run at import
import ph15, ph21, ph22, ph23, ph24
from ph16 import interval, crit, R, T
from ph18 import majority, describe_majority, agg
from ph19 import h21_diag
from ph21 import G_STAR, q3, first_true, hold600
from ph23 import Agent9, T0, presence_identity, first_surge_ok, pass_prob, eqmask, wv, wn
from ph24 import Release, Agent10, Agent10g, Agent8, Agent6, bitwise, t3_dwell, ratio_boot, pass_prob_R, q3f, drive_summary
from ph25 import Agent11, w1sum, lost_t1, binom_ge, cls3, construct_ok, m7a_t3a, t3a_steps, qq, sep10, t3_lost

sys.stdout.reconfigure(newline="\n")            # LF output, so the recorded sha256 equals the committed blob
DESIGN = "H26 v2 FINAL doc d54441658b54a6799 hash ac95c22d51838604912aa5537580686b93b3fece76827721c03564973ee09f54"
P_PRIOR, N_HI = 60, 300
SEEDS = dict(dev=(9977, 9987), eval=(1985, 2085))
BENCH = dict(rows=400, rows_c=800, p=0.30, steps_stub=200, steps_held=260, steps_b=400, steps=600, seed_w=20261071, seed_a=20261072)
BS = (BENCH["seed_w"], BENCH["seed_a"])
ph15.BOOT_SEED = 20261073; ph15._idx.clear()     # design section 7 (after ph25's import set its own); the resample cache emptied
# ---- bar constant: filled from bench (d) by decision:h26-t2-dwell-bar (registered order) ----
BARS = dict(T2=-4.9)                            # bar_T2 = -0.20 x D6_W1 (M5 b)
# ----
MODS = (ph15, ph21, ph22, ph23, ph24, ph25, ph25b)
Z95 = 1.96
ALLK = ph24.FIELDS + ("SIL", "TO", "EV", "W", "NAV6", "NAV8", "DIFF", "DIFF8", "PRES")     # reading R2
BEHK = ph24.FIELDS + ("SIL", "TO", "EV", "W")                                               # reading R4
PR = P_PRIOR - 1                                 # 59: the first step on which a never-sensed odour is absent


def sha(p=__file__): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def Phi(x): return 0.5*(1.0 + math.erf(x/math.sqrt(2.0)))


# ------------------------------------------------------------------ the agent (design sections 3.2, 3.5)
class Agent14(Release, Agent9):
    """H26: the H25 release on H24's agent with the presence prior separated from the window (counter starts at N_hi - P)"""

    def __init__(self, runs, rng, P=P_PRIOR, N_hi=N_HI, **kw):
        super().__init__(runs, rng, N=N_hi, **kw); self.P, self.N_hi = P, N_hi
        self.c = np.full((runs, 2), float(N_hi - P))                                   # reading R1


# ------------------------------------------------------------------ hooks (run time; no file edited)
_make_prev, _make23_prev = ph24.make, ph23.make          # ph25b.make (-> ph25.make -> ph24's), ph25.make23
_PN = [(P_PRIOR, N_HI)]


def make(cls, runs, rng, G, known, gate=True, filt=True, release=True):
    if cls is Agent14:
        P, N = _PN[0]; return Agent14(runs, rng, P=P, N_hi=N, G=G, known=known, rule=gate, filt=filt, scope=ph25._SCOPE[0], release=release)
    return _make_prev(cls, runs, rng, G, known, gate, filt, release)


def make23(cls, runs, rng, G, known, gate, filt, scope="prior"):
    if cls is Agent14:
        keep = ph25._SCOPE[0]; ph25._SCOPE[0] = scope
        try: return make(cls, runs, rng, G, known, gate, filt)
        finally: ph25._SCOPE[0] = keep
    return _make23_prev(cls, runs, rng, G, known, gate, filt, scope)


ph24.make, ph23.make = make, make23


@contextmanager
def pn(P, N):
    keep = _PN[0]; _PN[0] = (P, N)
    try: yield
    finally: _PN[0] = keep


@contextmanager
def n11(N):
    keep = ph25b._N[0]; ph25b._N[0] = N
    try: yield
    finally: ph25b._N[0] = keep


def run(world, cls, vals, seeds, scope="prior", P=P_PRIOR, N_hi=N_HI, **kw):
    with pn(P, N_hi): return ph25.run(world, cls, vals, seeds, scope=scope, **kw)


def run11(world, N, vals, seeds, **kw):
    """ph25.Agent11 at window N (reading R10)"""
    with n11(N): return ph25.run(world, Agent11, vals, seeds, **kw)


def stub(cls, known, sched, scope="prior", P=P_PRIOR, N_hi=N_HI, N11=60, **kw):
    kw.setdefault("seeds", BS)
    with pn(P, N_hi), n11(N11): return ph25.stub(cls, known, sched, scope=scope, **kw)


# ------------------------------------------------------------------ measures
def roweq(o1, o2, ks=ALLK):
    """per row: equal on every field in ks over every step (reading R2)"""
    ok = np.ones(o1["H"].shape[1], bool)
    for k in ks:
        if k not in o1: continue
        e = o1[k] == o2[k]; ok &= e.reshape(e.shape[0], e.shape[1], -1).all((0, 2))
    return ok


def c2_offset(o14, o11, d=N_HI - P_PRIOR):
    """valued column of the counter: Agent14's == Agent11 (N 60)'s + 240 on every (row, step) (reading R2)"""
    r = np.arange(len(o14["good"])); return bool(np.array_equal(o14["C2"][:, r, o14["good"]], o11["C2"][:, r, o11["good"]] + d))


def counter_exact(o, c0=N_HI - P_PRIOR, N=N_HI):
    """bench (b): per row, c follows c <- 0 on a whiff else c + 1 from c0 exactly, and present == (c < N) or held"""
    X = o["W"]; steps, rows, _ = X.shape; c = np.full((rows, 2), float(c0)); ok = np.ones(rows, bool); ho = np.zeros(rows, int)
    for t in range(steps):
        c = np.where(X[t], 0.0, c + 1.0); held = np.zeros((rows, 2), bool); h = o["H"][t]; held[np.arange(rows), np.maximum(h, 0)] = h >= 0
        ok &= (o["C2"][t] == c).all(1) & (o["P2"][t] == ((c < N) | held)).all(1); ho += (held & (c >= N)).sum(1)
    return ok, ho


def first_valued(o): return first_true(wv(o))


def at_risk(o10, lo=PR):
    """reading R3, from Agent10's run: no valued whiff on 0..lo-1 and a neutral whiff with nothing or the neutral odour held on a step
    t with lo <= t < first valued whiff (t <= 599 if none). lo = 0 gives the literal reading (printed beside it)."""
    g = o10["good"]; H = o10["H"]; st = H.shape[0]; tt = np.arange(st)[:, None]; fv = first_valued(o10); fvx = np.where(fv < 0, st, fv)
    ok_state = (H < 0) | (H == (1 - g)[None, :]); ev = wn(o10) & ok_state & (tt >= lo) & (tt < fvx[None, :])
    return (fvx >= PR) & ev.any(0), fv


def lost300(o, t0=T0, W=N_HI):
    """reading R8: the post-whiff window exact in the Lost world, eligible rows"""
    g = o["good"]; st = o["steps"]; tt = np.arange(st)[:, None]; v, n = wv(o), wn(o)
    elig = v[:t0].any(0); L = np.where(elig, t0 - 1 - np.argmax(v[:t0][::-1], 0), -1)
    win = (tt > L) & (tt <= L + W - 1); after = tt >= L + W
    a1 = ~(o["NAV"] & n & ~v & win).any(0); anynav = (o["NAV"] & win).any(0)
    fs = first_true(o["NAV"] & n & (tt > L)); a2 = fs == first_true(n & after)
    a3 = ~((o["H"] == g[None, :]) & (tt >= L + 60)).any(0)
    return dict(elig=elig, L=L, exact=elig & a1 & a2 & a3, a1=a1, a2=a2, a3=a3, anynav=anynav, delay=np.where(fs >= 0, fs - L, -1))


def pp_dp(dp, b, bar=-0.05, most=False):
    """design section 7: paired DP with discordant fraction b, sd = sqrt(b - DP^2), se = sd / 20 (reading R5, R6)"""
    sd = math.sqrt(max(b - dp*dp, 0.0))
    if sd <= 0: return float(dp <= bar) if most else float(dp >= bar)
    se = sd/20.0; return Phi(((bar - dp) if most else (dp - bar))/se - Z95)


def pp_k(k, p10):
    """reading R5: M2(b) and M2(a) at k net rows out of V"""
    kk = max(k, 0); dp = -kk/400.0; return pp_dp(dp, kk/400.0), binom_ge(max(min(p10 - kk/400.0, 1.0), 0.0))


def fmtp(x): return f"{x:.4f}"


# ------------------------------------------------------------------ the mechanism bench (design section 4)
def readings(say):
    say("   readings where the design is silent (file header R1-R11): R1 Agent14 = Agent9's constructor with N = N_hi, counter set to N_hi - P (float, exact);"
        " R2 'bitwise on every field' = ph24's identity fields + SIL, TO, EV, W, NAV6, NAV8, DIFF, DIFF8, PRES; C2 and the neutral presence differ by construction and do"
        " not enter nav, the valued C2 checked to be Agent11 (N 60)'s + 240 in W1/T3a; (a1') includes C2 and P2; R3 at-risk set from Agent10's run: no valued whiff on 0-58"
        " and a neutral whiff with nothing or the neutral odour held on a step t, 59 <= t < first valued whiff (<= 599 if none), the literal reading (any step before the"
        " first valued whiff) printed beside it; R4 departing = not equal on ph24's identity fields + W over 600 steps (PRES left out); R5 k = out-of-V rows Agent14 minus Agent11 (N 300), M2(b) at"
        " DP = -k/400, b = k/400; M2(a) exact binomial at this bench's Agent10 P(V) - k/400; R6 (h): b = discordant fraction of V, sd = sqrt(b - DP^2), se = sd/20,"
        " Phi((DP + 0.05)/se - 1.96); R7 (h3): ph23.pass_prob at bar_T2 = round(-0.20 x D6_W1, 1); R8 Lost window: no nav on a neutral-only whiff on L+1..L+299,"
        " first neutral surge after L == first neutral whiff at or after L+300, valued not held from L+60; departure after t0 checked over the whole run; R9 pathway-off"
        " = Agent8 G 0 gate off filter off (ph25's); R10 Agent11 at N 300 via ph25b's N wrapper; R11 dev/eval re-run the bench for M4")


def bench(say=print):
    p = BENCH["p"]; n = BENCH["rows"]; st = BENCH["steps"]; ids, bars, out = {}, {}, {}; kn = [1.0, 0.0]; v10 = (1.0, 0.0)
    say(f"== H26 mechanism bench (design v2 FINAL section 4). design {DESIGN}; {BENCH}; P {P_PRIOR}, N_hi {N_HI} (counter start {N_HI - P_PRIOR}); t0 {T0};"
        f" bootstrap seed {ph15.BOOT_SEED} ==")
    header(say); readings(say)
    say("   rows share no state: one generator per world and one per agent population, fixed-size draws consumed in row order every step")
    both = [(BENCH["steps_stub"], p, p)]
    # ---- (a) identities
    ids["a1 stub"] = bitwise(stub(Agent14, kn, both, scope="off"), stub(Agent10, kn, both))
    ids["a1 stub, channel 1 held"] = bitwise(stub(Agent14, kn, both, scope="off", hold=1), stub(Agent10, kn, both, hold=1))
    o14, o10, o10g = run("T1", Agent14, v10, BS), run("T1", Agent10, v10, BS), run("T1", Agent10g, v10, BS)
    o60, o300 = run11("T1", 60, v10, BS), run11("T1", N_HI, v10, BS)
    ids["a1 World7"] = bitwise(run("T1", Agent14, v10, BS, scope="off"), o10)
    say(f"(a1) scope 'off' == Agent10 bitwise (H, s, S, nav, since, target, positions, headings, silence counter, timeout/evidence flags): stub both channels p {p}"
        f" {BENCH['steps_stub']} steps {ids['a1 stub']}; the same with channel 1 held {ids['a1 stub, channel 1 held']}; World7 {n} x {st} {ids['a1 World7']}")
    k1 = ALLK + ("P2", "C2")
    a1p = {"T1": bitwise(run("T1", Agent14, v10, BS, P=60, N_hi=60), o60, k1)}
    w60 = run11("W1", 60, v10, BS); f60 = run11("T3a", 60, v10, BS)
    a1p["W1"] = bitwise(run("W1", Agent14, v10, BS, P=60, N_hi=60), w60, k1); a1p["T3a"] = bitwise(run("T3a", Agent14, v10, BS, P=60, N_hi=60), f60, k1)
    a1p["stub"] = bitwise(stub(Agent14, kn, both, P=60, N_hi=60), stub(Agent11, kn, both, N11=60), k1)
    ids["a1' (P 60, N_hi 60) == ph25.Agent11"] = all(a1p.values())
    say(f"(a1') Agent14 with (P 60, N_hi 60) == ph25.Agent11 (N 60) bitwise on every field incl. the counter C2 and presence P2: " + "; ".join(f"{k} {v}" for k, v in a1p.items()))
    for name, kv in (("0/0", (0.0, 0.0)), ("+1/+1", (1.0, 1.0)), ("+1/-1", (1.0, -1.0))):
        s_ok = bitwise(stub(Agent14, list(kv), both), stub(Agent10, list(kv), both)); a14 = run("T1", Agent14, kv, BS); w_ok = bitwise(a14, run("T1", Agent10, kv, BS))
        key = "a2' +1/-1 (reported identity)" if kv[1] < 0 else f"a2 {name}"; ids[key] = s_ok and w_ok
        say(f"({key.split()[0]}) Agent14 at {name} == Agent10 bitwise: stub {s_ok}; World7 {n} x {st} {w_ok}; `differs8` (row, step) {int(a14['DIFF8'].sum())};"
            f" valued-present fraction {a14['PRES'].mean():.3f}{'  (a reported identity; a False would be an implementation error)' if kv[1] < 0 else ''}")
    hs = [(BENCH["steps_held"], p, 0.0)]; ids["a3"] = bitwise(stub(Agent14, kn, hs), stub(Agent10, kn, hs))
    say(f"(a3) +1/0, channel 0 alone p {p} {BENCH['steps_held']} steps (the valued odour held): == Agent10 bitwise {ids['a3']}")
    ids["a4 presence identity"] = presence_identity(o14); fd = first_true(o14["DIFF8"]); e10 = eqmask(o14, o10).all(0)
    say(f"(a4) presence identity, World7 +1/0 {n} x {st}: nav == nav8 where the valued odour is present and == nav6 where it is not, every (row, step): {ids['a4 presence identity']};"
        f" valued present on {o14['PRES'].mean():.3f} of (row, step); `differs8` (row, step) {int(o14['DIFF8'].sum())} in {int((fd >= 0).sum())} rows, first `differs8` step"
        f" {q3(fd[fd >= 0])}; rows bitwise Agent10 throughout (positions, headings, circuit) {int(e10.sum())}")
    w14, w10, w6, w10g = (run("W1", c, v10, BS) for c in (Agent14, Agent10, Agent6, Agent10g))
    ids["a5 W1 == Agent11 (N 60) every field"] = bitwise(w14, w60, ALLK) and c2_offset(w14, w60)
    ids["a5 W1 == Agent10 on 0-58"] = bitwise(w14, w10, n=PR); ids["a5 W1 nav == nav6 from 59"] = bool(np.array_equal(w14["NAV"][PR:], w14["NAV6"][PR:]))
    ids["a5 W1 presence 0-58 only, draws"] = bool(w14["PRES"][:PR].all() and not w14["PRES"][PR:].any() and all(o["draws_equal"] and o["rng_equal"] for o in (w14, w10, w6, w10g, w60)))
    say(f"(a5) W1 (valued column masked) {n} x {st}: Agent14 == Agent11 (N 60) bitwise on every field (reading R2) and valued counter = Agent11's + {N_HI - P_PRIOR}"
        f" {ids['a5 W1 == Agent11 (N 60) every field']}; == Agent10 on steps 0-{PR - 1} {ids['a5 W1 == Agent10 on 0-58']}; nav == nav6 from {PR} {ids['a5 W1 nav == nav6 from 59']};"
        f" valued present exactly on 0-{PR - 1}, masked draws == the World7 twin, generator state equal {ids['a5 W1 presence 0-58 only, draws']}")
    f14 = run("T3a", Agent14, v10, BS); f10 = run("T3a", Agent10, v10, BS)
    ids["a6 T3a == Agent11 (N 60) every field"] = bitwise(f14, f60, ALLK) and c2_offset(f14, f60); ids["a6 T3a == Agent10 on 0-58"] = bitwise(f14, f10, n=PR)
    say(f"(a6) T3a {n} x {st}: Agent14 == Agent11 (N 60) bitwise on every field and valued counter = Agent11's + {N_HI - P_PRIOR} {ids['a6 T3a == Agent11 (N 60) every field']};"
        f" == Agent10 on steps 0-{PR - 1} {ids['a6 T3a == Agent10 on 0-58']}")
    fv14 = first_valued(o14); early = (fv14 >= 0) & (fv14 <= PR - 1); eq300 = roweq(o14, o300); dep = ~roweq(o14, o300, BEHK); risk, fv10 = at_risk(o10); risk0, _ = at_risk(o10, lo=0)
    ids["a7 early-whiff rows == Agent11 (N 300)"] = bool(eq300[early].all()); ids["a7 departing rows in the at-risk set"] = bool((~dep | risk).all())
    say(f"(a7) T1: rows whose first valued whiff is at step <= {PR - 1}: {int(early.sum())}/{n}; of them bitwise Agent11 (N 300) throughout (reading R2) {int(eq300[early].sum())}"
        f" -> {ids['a7 early-whiff rows == Agent11 (N 300)']}; rows departing from Agent11 (N 300) {int(dep.sum())}, of them in the at-risk set (reading R3) {int((dep & risk).sum())}"
        f" -> {ids['a7 departing rows in the at-risk set']}")
    s_ok, s_cnt = sep10(o14, o10); ids["a8 separation vs Agent10"] = s_ok
    say(f"(a8) separation vs Agent10 (== up to the step before the first `differs8`; no `differs8` -> equal throughout): {s_ok} {s_cnt}")
    # ---- (b) counter dynamics, exact
    sb = BENCH["steps_b"]; tb = np.arange(sb)[:, None]; r_ = np.arange(n)
    sch = {"no whiff": [(sb, 0.0, 0.0)], "one whiff on channel 0 at step 0": [(1, 1.0, 0.0), (sb - 1, 0.0, 0.0)], "20-step p 0.30 burst on channel 0": [(20, p, 0.0), (sb - 20, 0.0, 0.0)]}
    okb = np.ones(n, bool); hot = 0
    for k, s in sch.items():
        o = stub(Agent14, kn, s); P2, C, H = o["P2"], o["C2"], o["H"]; ok, ho = counter_exact(o); hot += int(ho.sum())
        if k == "no whiff": pat = (C == (N_HI - P_PRIOR) + tb[:, :, None] + 1).all((0, 2)) & (P2 == (tb <= PR - 1)[:, :, None]).all((0, 2)); ptxt = f"c == {N_HI - P_PRIOR} + t + 1 and present exactly on steps 0-{PR - 1}, both channels"
        elif k.startswith("one"): pat = (C[:, :, 0] == tb).all(0) & (P2[:, :, 0] == (tb <= N_HI - 1)).all(0); ptxt = f"c_0 == t and channel 0 present exactly on steps 0-{N_HI - 1}, absent from {N_HI}"
        else:
            x0 = o["W"][:, :, 0]; had = x0.any(0); Lr = np.where(had, sb - 1 - np.argmax(x0[::-1], 0), -1)
            pat = (P2[:, :, 0] == np.where(had[None, :], tb < Lr[None, :] + N_HI, tb <= PR - 1)).all(0)
            ptxt = f"channel 0 absent from exactly {N_HI} steps after the last whiff (rows with a whiff {int(had.sum())}, last whiff step {q3(Lr[had])})"
        ex = ok & pat & (ho == 0); okb &= ex
        fh = first_true(H == 0); end = first_true((H != 0) & (tb > fh[None, :]) & (fh >= 0)[None, :])
        say(f"(b) {k}: rows exact {int(ex.sum())}/{n} (recursion from {N_HI - P_PRIOR} and present == (c < {N_HI}) or held {int(ok.sum())}; {ptxt} {int(pat.sum())}; no held-only presence"
            f" {int((ho == 0).sum())}); valued hold formed in {int((fh >= 0).sum())} rows, at step {qq(fh)}, ended at step {qq(end)}; held-only presence (row, step) {int(ho.sum())}")
    k_, pt, lo, hi = interval("P", okb); bars["b"] = lo
    say(f"(b) counter exact in every schedule ({n} rows x {sb} steps): {k_}/{n} = {pt:.3f} [{lo:.3f}, {hi:.3f}] (bar lower bound >= 0.95) -> {'PASS' if lo >= 0.95 else 'FAIL'};"
        f" held clause the only reason for presence with c >= {N_HI}: {hot} (row, step), expected 0")
    # ---- (c) task-like neutral-hold start, reported
    nc = BENCH["rows_c"]
    with n11(60): cc = {k: ph23.run("T1", c, v10, BS, filt=c is not Agent10g, runs=nc, start="variant", hold=True)
                        for k, c in (("Agent14", Agent14), ("Agent11 (N 60)", Agent11), ("Agent10", Agent10), ("Agent10g", Agent10g))}
    c14 = cc["Agent14"]; hn = c14["H"] == (1 - c14["good"])[None, :]
    say(f"(c) task-like neutral-hold start (H23 bench (b) state: neutral source + (DOWN, 0), heading upwind, neutral hold s 2.0), {nc} rows x {st} steps, REPORTED, not a gate:"
        f" Agent14 neutral-held (row, step) {int(hn.sum())}, fraction with the valued odour present {c14['PRES'][hn].mean() if hn.any() else float('nan'):.3f}")
    for k, o in cc.items():
        kk, pt_, l_, h_ = interval("P", hold600(o)); fvc = first_valued(o)
        say(f"      {k}: holding the valued odour at step {st} {kk}/{nc} = {pt_:.3f} [{l_:.3f}, {h_:.3f}]; first valued whiff step {qq(fvc)}")
    for k in ("Agent11 (N 60)", "Agent10", "Agent10g"):
        _, dp, l_, h_ = interval("DP", hold600(c14).astype(float), hold600(cc[k]).astype(float)); say(f"      paired DP holding valued at 600, Agent14 - {k}: {dp:+.4f} [{l_:+.4f}, {h_:+.4f}]")
    # ---- (d) W1: implementation bar and the measurement that fixes M5(b)'s bar
    ok_d, fs, fb = first_surge_ok(w14, PR); k_, pt, lo_d, hi = interval("P", ok_d); bars["d"] = lo_d
    d14, d60, d10, d6, d10g = (t3_dwell(o, 0, st) for o in (w14, w60, w10, w6, w10g)); D6W1 = float(d6.mean()); bar_t2 = round(-0.20*D6W1, 1)
    pp3, m, sd = pass_prob(d14 - d6, bar_t2); _, _, blo, bhi = interval("DP", d14, d6); _, m10, b10lo, b10hi = interval("DP", d14, d10)
    say(f"(d) W1, bench seeds, {n} x {st}: first surge == first B whiff at or after step {PR} in {k_}/{n} = {pt:.3f} [{lo_d:.3f}, {hi:.3f}] (bar lower bound >= 0.95)"
        f" -> {'PASS' if lo_d >= 0.95 else 'FAIL'}; first-surge step {qq(fs)}")
    for name, o, d in (("Agent14", w14, d14), ("Agent11 (N 60)", w60, d60), ("Agent10", w10, d10), ("Agent6", w6, d6), ("Agent10g", w10g, d10g)):
        s = w1sum(o); f1 = first_true(o["NAV"])
        say(f"      {name}: mean W1 dwell within 3.0 over {st} steps {d.mean():.3f} (quartiles {q3f(d)}); reach {int(s['reach'].sum())}/{n}; lost rows {int(s['lost'].sum())};"
            f" wall contacts per row {s['contacts'].mean():.3f}; first surge step {qq(f1)}")
    l14, l10, l6 = (w1sum(o)["lost"].astype(float) for o in (w14, w10, w6))
    _, dl10, dl10lo, dl10hi = interval("DP", l14, l10); _, dl6, dl6lo, dl6hi = interval("DP", l14, l6)
    say(f"   (d) measured: D6_W1 (Agent6's mean W1 dwell) = {D6W1:.4f}; Agent10g == Agent6 row for row {bool(np.array_equal(d10g, d6))}; rule bar_T2 = -0.20 x D6_W1 rounded to 0.1 = {bar_t2:+.1f};"
        f" paired Agent14 - Agent6 mean {m:+.4f} sd {sd:.4f} (bootstrap [{blo:+.4f}, {bhi:+.4f}]); paired Agent14 - Agent10 {m10:+.4f} [{b10lo:+.4f}, {b10hi:+.4f}];"
        f" W1 lost rows DP Agent14 - Agent10 {dl10:+.4f} [{dl10lo:+.4f}, {dl10hi:+.4f}] (M5(d) as re-signed, reported here), Agent14 - Agent6 {dl6:+.4f} [{dl6lo:+.4f}, {dl6hi:+.4f}]")
    out.update(D6_W1=D6W1, bar_T2=bar_t2, m_T2=m, sd_T2=sd, pp_T2=pp3, d14=float(d14.mean()), d10=float(d10.mean()), d10g=float(d10g.mean()), m10=m10)
    # ---- (e) H23's implementation bars re-run on Agent14
    ra = stub(Agent14, kn, both, hold=1); ok1 = ((ra["NAV"] == ra["W"][:, :, 0]) | ~ra["P2"][:, :, 0]).all(0); _, pt1, lo1, _ = interval("P", ok1)
    ok2 = ~(o14["NAV"] & o14["PRES"] & ~wv(o14)).any(0); _, pt2, lo2, _ = interval("P", ok2); bars["e a4'"] = lo1; bars["e c'"] = lo2
    say(f"(e) (a4') channel 1 held by construction, both channels p {p}, {BENCH['steps_stub']} steps: nav == channel 0's whiff on every step with channel 0 present in {int(ok1.sum())}/{n}"
        f" = {pt1:.3f}, lower bound {lo1:.3f} (>= 0.95); (c') task start: every nav step with the valued odour present has a valued whiff in {int(ok2.sum())}/{n} = {pt2:.3f},"
        f" lower bound {lo2:.3f} (>= 0.95)")
    # ---- (f) constructed losses
    f = {"Agent14": f14, "Agent11 (N 60)": f60, "Agent10": f10, "Agent10g": run("T3a", Agent10g, v10, BS), "ceiling": run("T3a", None, v10, BS, fixed="neutral")}
    ids["f T3a construction, every arm"] = all(construct_ok(o, k != "ceiling") for k, o in f.items())
    ex, parts = m7a_t3a(f14); k_, pt, lo_f, hi = interval("P", ex); bars["f M7(a) T3a"] = lo_f
    say(f"(f) T3a (valued column masked from step 0, start at the valued source, s_valued 2.0 held), bench seeds {n} x {st}: draws == the twin, generator state equal, start and hold,"
        f" every arm {ids['f T3a construction, every arm']}; Agent14 presence identity {presence_identity(f14)}")
    say(f"(f) M7(a) T3a exact, Agent14, every row: {k_}/{n} = {pt:.3f} [{lo_f:.3f}, {hi:.3f}] (bar lower bound >= 0.95) -> {'PASS' if lo_f >= 0.95 else 'FAIL'}; parts: hold ends at step 47 with"
        f" both units <= 1.0 {int(parts['end47'].sum())}, valued not held from 47 {int(parts['notheld'].sum())}, no nav on 0-{PR - 1} {int(parts['nonav'].sum())}, first neutral surge ="
        f" first neutral whiff at or after {PR} {int(parts['surge'].sum())}")
    for k in ("Agent14", "Agent11 (N 60)", "Agent10", "Agent10g"):
        s3 = t3a_steps(f[k]); say(f"      [T3a {k}] valued hold end step {qq(s3['end'])}; first neutral surge {qq(s3['surge'])}; first neutral hold {qq(s3['hold'])};"
                                  f" first within 3.0 of the neutral source {qq(s3['arrive'])}")
    lw = {"Agent14": run("T3b", Agent14, v10, BS), "Agent11 (N 60)": run11("T3b", 60, v10, BS), "Agent10": run("T3b", Agent10, v10, BS), "Agent10g": run("T3b", Agent10g, v10, BS)}
    t1r = {"Agent14": o14, "Agent11 (N 60)": o60, "Agent10": o10, "Agent10g": o10g}
    ids["f Lost construction, every arm"] = all(o["draws_equal"] and o["rng_equal"] for o in lw.values()) and all(bitwise(lw[k], t1r[k], n=T0) for k in lw) \
        and not any(bitwise(lw[k], t1r[k]) for k in lw)
    dl = lost300(lw["Agent14"]); el = dl["elig"]; k_, pt, lo_l, hi = interval("P", dl["exact"][el]); bars["f window Lost (L + 300)"] = lo_l
    say(f"(f) Lost world (mask on from step {T0}): draws == the twin (both columns before t0), generator state equal, each arm == its World7 run on steps 0-{T0 - 1} and departs after"
        f" (reading R8): {ids['f Lost construction, every arm']}; Agent14 presence identity {presence_identity(lw['Agent14'])}")
    say(f"(f) post-whiff window exact in the Lost world, Agent14, eligible rows (a valued whiff before t0, L = the last one; reading R8): {k_}/{int(el.sum())} = {pt:.3f} [{lo_l:.3f}, {hi:.3f}]"
        f" (bar lower bound >= 0.95) -> {'PASS' if lo_l >= 0.95 else 'FAIL'}; parts (no nav on a neutral-only whiff on L+1..L+{N_HI - 1}, first neutral surge after L = first neutral"
        f" whiff at or after L+{N_HI}, valued not held from L+60): {int(dl['a1'][el].sum())}/{int(dl['a2'][el].sum())}/{int(dl['a3'][el].sum())}; any nav on L+1..L+{N_HI - 1}"
        f" {int(dl['anynav'][el].sum())} rows; L {q3(dl['L'][el])}; first-neutral-surge delay after L {q3(dl['delay'][el & (dl['delay'] >= 0)])} (none {int((el & (dl['delay'] < 0)).sum())})")
    for k in lw:
        hold, end, rel = ph24.t3b_release(lw[k]); mm = hold & (end >= 0)
        say(f"      [Lost {k}] holding valued at t0 {int(hold.sum())}/{n}; ended {int(mm.sum())} (never {int((hold & (end < 0)).sum())}), relative to the origin {q3(rel[mm])};"
            f" neutral dwell 400-599 mean {t3_dwell(lw[k], 400, 600).mean():.3f}")
    Dc, D10, D14, D60, D10g = (t3_dwell(f[k], 100, 600) for k in ("ceiling", "Agent10", "Agent14", "Agent11 (N 60)", "Agent10g"))
    _, spn, slo, shi = interval("DP", Dc, D10); sdr = float(np.std(Dc - D10)); Rb, Rlo, Rhi = ratio_boot(D14, D10, Dc); Rg, Rglo, Rghi = ratio_boot(D10g, D10, Dc)
    say(f"   (f) T3a measured (reported; the bar does not move): neutral dwell 100-599 Agent14 {D14.mean():.3f}, Agent11 (N 60) {D60.mean():.3f}, floor Agent10 {D10.mean():.3f},"
        f" ceiling {Dc.mean():.3f}, Agent10g {D10g.mean():.3f}; span {spn:.3f} [{slo:.3f}, {shi:.3f}]; per-row paired sd {sdr:.3f}; R Agent14 {Rb:.4f} [{Rlo:.4f}, {Rhi:.4f}],"
        f" Agent10g {Rg:.4f} [{Rglo:.4f}, {Rghi:.4f}]; M7(b) pass probability at the bench R {pass_prob_R(Rb, sdr, spn):.4f}")
    out.update(R=Rb, span=spn)
    # ---- (m) the at-risk rows, printed before (h) is read
    c14_, c10_, c300_, c60_ = cls3(o14), cls3(o10), cls3(o300), cls3(o60); fv300 = first_valued(o300)
    say(f"(m) the at-risk rows, World7 T1 +1/0 {n} x {st} (printed before (h) is read; no bar reads (m)):")
    for name, fvx in (("Agent10", fv10), ("Agent14", fv14), ("Agent11 (N 300)", fv300)):
        nx = np.where(fvx < 0, 10**6, fvx)
        say(f"      [{name}] first valued whiff step {qq(fvx)} (never {int((fvx < 0).sum())}); rows with none by step {PR - 1} {int((nx > PR - 1).sum())}, by 118 {int((nx > 118).sum())},"
            f" by 598 {int((nx > 598).sum())}")
    say(f"      at-risk set (reading R3, from Agent10's run): {int(risk.sum())} rows (literal reading, any step before the first valued whiff: {int(risk0.sum())});"
        f" rows departing from Agent11 (N 300) {int(dep.sum())}, all in the at-risk set {bool((~dep | risk).all())} ((a7)); departing rows' first departure step"
        f" {q3(first_true(~(eqmask(o14, o300)))[dep]) if dep.any() else 'n/a'}")
    for lab, m_ in (("at-risk rows", risk), ("departing rows", dep)):
        say(f"      [{lab}, {int(m_.sum())}] outcome V/N/tie: Agent14 {int((c14_[m_] == 0).sum())}/{int((c14_[m_] == 1).sum())}/{int((c14_[m_] == 2).sum())};"
            f" Agent11 (N 300) {int((c300_[m_] == 0).sum())}/{int((c300_[m_] == 1).sum())}/{int((c300_[m_] == 2).sum())};"
            f" Agent10 {int((c10_[m_] == 0).sum())}/{int((c10_[m_] == 1).sum())}/{int((c10_[m_] == 2).sum())}")
    out14, out300 = int(((c14_ != 0) & (c10_ == 0)).sum()), int(((c300_ != 0) & (c10_ == 0)).sum()); kk = out14 - out300
    P10 = float((c10_ == 0).mean()); pb_k, pa_k = pp_k(kk, P10)
    say(f"      out of V (vs Agent10): Agent14 {out14}, Agent11 (N 300) {out300}; into V: Agent14 {int(((c14_ == 0) & (c10_ != 0)).sum())}, Agent11 (N 300) {int(((c300_ == 0) & (c10_ != 0)).sum())}")
    say(f"   (m) k = Agent14's out-of-V rows - Agent11 (N 300)'s = {out14} - {out300} = {kk}; M2 pass probabilities at k (design section 7, reading R5): M2(b) at DP {-max(kk, 0)/400:+.4f},"
        f" b {max(kk, 0)/400:.4f}: {pb_k:.4f}; M2(a) exact binomial at P(V) {P10:.3f} - {max(kk, 0)}/400: {pa_k:.4f}")
    out.update(k=kk, risk=int(risk.sum()), dep=int(dep.sum()))
    # ---- (h) T1 on bench seeds, and the stop rule
    V14, V10, V10g = (c14_ == 0), (c10_ == 0), (cls3(o10g) == 0)
    _, dp, dlo, dhi = interval("DP", V14.astype(float), V10.astype(float)); b = float((V14 != V10).mean()); ppb = pp_dp(dp, b)
    ppm, _, sdb = pass_prob(V14.astype(float) - V10.astype(float), -0.05); ppc = pp_dp(float(V14.mean() - V10g.mean()), float((V14 != V10g).mean()), bar=0.05)
    stop_h = ppb < 0.5; out.update(dp_T1=dp, dp_lo=dlo, dp_hi=dhi, pp_M2b=ppb, stop_h=stop_h)
    say(f"(h) T1 on bench seeds, World7 +1/0 {n} x {st}, REPORTED: " + "; ".join(f"{k} V {int(majority(o)[0].sum())} N {int(majority(o)[1].sum())} tie {int(majority(o)[2].sum())}"
        f" P(V) {interval('P', majority(o)[0])[1]:.3f} [{interval('P', majority(o)[0])[2]:.3f}, {interval('P', majority(o)[0])[3]:.3f}]"
        for k, o in (("Agent14", o14), ("Agent10", o10), ("Agent10g", o10g), ("Agent11 (N 300)", o300), ("Agent11 (N 60)", o60))))
    say(f"   (h) paired DP P(V) Agent14 - Agent10 {dp:+.4f} [{dlo:+.4f}, {dhi:+.4f}] (bootstrap 5000, seed {ph15.BOOT_SEED}); into V {int(((c14_ == 0) & (c10_ != 0)).sum())}, out of V {out14};"
        f" rows bitwise Agent10 throughout {int(e10.sum())}, departing {int((~e10).sum())}; lost rows {int(lost_t1(o14).sum())} vs {int(lost_t1(o10).sum())};"
        f" reported: Agent11 (N 300) - Agent10 {float((c300_ == 0).mean() - P10):+.4f}, Agent11 (N 60) - Agent10 {float((c60_ == 0).mean() - P10):+.4f}")
    say(f"   (h) pass probabilities at the bench values (design section 7 arithmetic, reading R6): M2(a) P(k >= 365 of 400) at P(V) {V14.mean():.3f}: {binom_ge(V14.mean()):.4f};"
        f" M2(b) at DP {dp:+.4f} with discordant fraction b {b:.4f}, sd sqrt(b - DP^2) {math.sqrt(max(b - dp*dp, 0.0)):.4f} (paired sd {sdb:.4f}): {ppb:.4f} (ph23.pass_prob {ppm:.4f});"
        f" M2(c) vs Agent10g at DP {(V14.mean() - V10g.mean()):+.4f}: {ppc:.4f}")
    say(f"   (h) STOP RULE (design v2 FINAL section 4, section 12 point 5): M2(b) pass probability {ppb:.4f} {'< 0.5 -> STOP: the run returns to the owner after the bench record' if stop_h else '>= 0.5 -> continue'}")
    # ---- (h3) W1 stop rule
    stop_h3 = pp3 < 0.5; out.update(stop_h3=stop_h3)
    say(f"   (h3) STOP RULE (design v2 FINAL section 4, section 12 point 5; reading R7): M5(b) pass probability at the bench's paired W1 dwell Agent14 - Agent6 {m:+.4f} (sd {sd:.4f})"
        f" with bar_T2 {bar_t2:+.1f} (-0.20 x D6_W1 {D6W1:.4f}): {pp3:.4f} {'< 0.5 -> STOP: the run returns to the owner after the bench record' if stop_h3 else '>= 0.5 -> continue'}")
    idok = all(ids.values()); bok = all(v >= 0.95 for v in bars.values()); verdict = idok and bok; stop = stop_h or stop_h3; out["stop"] = stop
    say(f"== M4: identities {idok}; failed {[k for k, v in ids.items() if not v]}; implementation bars (lower bounds >= 0.95) {bok} " + str({k: round(float(v), 4) for k, v in bars.items()})
        + f" -> M4 {'PASS: the tasks may be run' if verdict else 'FAIL, NO CANDIDATE: the rule as specified does not do what section 3 says; the tasks are NOT run'};"
        f" (c), (m) reported; (h) stop rule {'STOP' if stop_h else 'continue'}; (h3) stop rule {'STOP' if stop_h3 else 'continue'} ==")
    return verdict, out


# ------------------------------------------------------------------ self-checks
def seeds_unused():
    """design section 9: none of the fifteen numbers appears in any other file under the repository (recursive, digit-boundary; .git and
    __pycache__ excluded; excluded by name: this file, its outputs ph28_*.txt, the H26 documents h26_*.md, master_plan.md, notes/*.md,
    viewer/*). The demo seeds 5/6 are used deliberately and are NOT part of this check."""
    base = [*SEEDS["dev"], *SEEDS["eval"], BENCH["seed_w"], BENCH["seed_a"], ph15.BOOT_SEED]
    derived = [s + 10_000 for s in (SEEDS["dev"][0], SEEDS["eval"][0], BENCH["seed_w"])] + [s + 20_000 for s in (SEEDS["dev"][1], SEEDS["eval"][1], BENCH["seed_a"])]
    nums = base + derived + [BENCH["seed_w"] + 10_000_000, BENCH["seed_a"] + 20_000_000]
    pat = re.compile(rb"(?<!\d)(" + "|".join(map(str, nums)).encode() + rb")(?!\d)"); hits = []; nf = 0
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        top = os.path.relpath(root, repo).replace("\\", "/").split("/")[0]
        for f in files:
            if f == "ph28.py" or (f.startswith("ph28_") and f.endswith(".txt")) or (f.startswith("h26_") and f.endswith(".md")) or f == "master_plan.md": continue
            if (os.path.basename(root) == "notes" and f.endswith(".md")) or top == "viewer": continue
            nf += 1
            if pat.search(open(os.path.join(root, f), "rb").read()): hits.append(os.path.relpath(os.path.join(root, f), repo))
    return hits, nums, nf


def header(say=print):
    say(f"   ph28.py sha256 {sha()}; design {DESIGN}")
    say("   imported modules: " + "; ".join(f"{os.path.basename(m.__file__)} {sha(m.__file__)}" for m in MODS))
    say(f"   seeds: dev {SEEDS['dev']}, eval {SEEDS['eval']}, bench {BS}, bootstrap {ph15.BOOT_SEED}; demo seeds (5, 6) used deliberately, NOT part of the seed scan; no reproduction seed used;"
        f" BARS {BARS}")
    say("   decisions: decision:h26-open; decision:classification-rule-relaxed-presence-prior-h26; decision:h26-m5d-bar-resigned; bar: decision:h26-t2-dwell-bar")


def demo():
    print(f"== H26 self-checks (demo). design {DESIGN} ==")
    header()
    print("   fixed before this recorded demo: none (see the episode for the code-path test)")
    n, st = 40, 200; kw = dict(runs=n, steps=st); sd = (5, 6); sp = [(st, 0.30, 0.30)]; kn = [1.0, 0.0]; v10 = (1.0, 0.0)
    for cls in (Agent10, Agent10g, Agent8, Agent6, Agent11):
        ph24.make = _make_prev; a = ph25.run("T1", cls, v10, sd, **kw); sa = ph25.stub(cls, kn, sp, rows=n, seeds=BS)
        ph24.make = make; b = ph25.run("T1", cls, v10, sd, **kw); sb = ph25.stub(cls, kn, sp, rows=n, seeds=BS)
        assert all(np.array_equal(a[k], b[k]) for k in a if isinstance(a[k], np.ndarray)), f"the make hook changed a ph24.run field ({cls.__name__})"
        assert all(np.array_equal(sa[k], sb[k]) for k in sa if isinstance(sa[k], np.ndarray)), f"the make hook changed a ph24.stub field ({cls.__name__})"
    print("ok  this file's make hook leaves every field of ph24.run and ph24.stub bitwise equal for ph24's and ph25's agents (World7 40 x 200 and stub; Agent10, Agent10g, Agent8, Agent6, Agent11)")
    a = ph25.run("T1", Agent11, v10, sd, **kw); b = run11("T1", 60, v10, sd, **kw); c = run11("T1", 300, v10, sd, **kw)
    assert bitwise(a, b, ALLK + ("P2", "C2")), "Agent11 through the N wrapper at 60 is not ph25.run's"
    last = np.full((n, 2), -1)
    for t in range(st): last = np.where(c["W"][t], t, last); assert np.array_equal(c["C2"][t], np.where(last >= 0, t - last, t + 1)), "Agent11 N 300 counter"
    assert np.array_equal(c["P2"], (c["C2"] < 300) | (np.arange(2)[None, None, :] == c["H"][:, :, None])), "Agent11 N 300 presence"
    print("ok  ph25b's N wrapper: Agent11 at N 60 through it == ph25.run's Agent11 (every field, counter included); at N 300 the counter is steps since the last whiff and present == c < 300 or held")
    o10 = run("T1", Agent10, v10, sd, **kw); o14 = run("T1", Agent14, v10, sd, **kw); o300 = run11("T1", 300, v10, sd, **kw)
    assert bitwise(run("T1", Agent14, v10, sd, scope="off", **kw), o10) and bitwise(stub(Agent14, kn, sp, scope="off", rows=n), stub(Agent10, kn, sp, rows=n)), "scope off is not Agent10"
    assert bitwise(run("T1", Agent14, v10, sd, P=60, N_hi=60, **kw), ph25.run("T1", Agent11, v10, sd, **kw), ALLK + ("P2", "C2")), "(P 60, N_hi 60) is not Agent11"
    assert bitwise(run("T1", Agent14, v10, sd, release=False, P=60, N_hi=60, **kw), ph25.run("T1", Agent9, v10, sd, **kw), ALLK + ("P2", "C2")), "release off (60, 60) is not Agent9"
    print("ok  Agent14 scope 'off' == Agent10 (World7 and stub); (P 60, N_hi 60) == ph25.Agent11 and, with release off, == ph23.Agent9 (every field, the counter included)")
    for kv in ((0.0, 0.0), (1.0, 1.0), (1.0, -1.0)):
        assert bitwise(run("T1", Agent14, kv, sd, **kw), run("T1", Agent10, kv, sd, **kw)), f"Agent14 at {kv} is not Agent10"
    ok, cnt = sep10(o14, o10); assert presence_identity(o14) and ok and o14["PRES"][:PR].all(), f"presence identity / separation {cnt}"
    print(f"ok  Agent14 == Agent10 at 0/0, +1/+1, +1/-1; at +1/0 the presence identity holds on every (row, step); separation vs Agent10 {cnt}")
    fv = first_valued(o14); early = (fv >= 0) & (fv <= PR - 1); eq = roweq(o14, o300); dp_ = ~roweq(o14, o300, BEHK); risk, _ = at_risk(o10)
    assert eq[early].all() and (~dp_ | risk).all(), "(a7)"
    print(f"ok  T1 40 x 200: rows with a valued whiff by step 58 ({int(early.sum())}) are bitwise Agent11 (N 300) on every field; departing rows ({int(dp_.sum())}) lie in the at-risk set ({int(risk.sum())})")
    w14, w60, w10 = run("W1", Agent14, v10, sd, **kw), run11("W1", 60, v10, sd, **kw), run("W1", Agent10, v10, sd, **kw); fs, _, _ = first_surge_ok(w14, PR)
    assert bitwise(w14, w60, ALLK) and c2_offset(w14, w60) and bitwise(w14, w10, n=PR) and np.array_equal(w14["NAV"][PR:], w14["NAV6"][PR:]) and fs.all(), "W1"
    assert not bitwise(w14, w60, ALLK + ("C2",)), "the counter value must differ by construction"
    assert bitwise(run("W3", Agent14, (0.0, 0.0), sd, **kw), run("W3", Agent10, (0.0, 0.0), sd, **kw)), "W3"
    print("ok  W1: Agent14 == Agent11 (N 60) on every field of reading R2, its valued counter = Agent11's + 240 (and C2 itself differs, as constructed); == Agent10 on 0-58;"
          " nav == nav6 from 59; first surge = first B whiff at or after 59 in every row; W3 Agent14 == Agent10")
    t3 = run("T3a", Agent14, v10, sd, **kw); t60 = run11("T3a", 60, v10, sd, **kw)
    assert construct_ok(t3) and presence_identity(t3) and bitwise(t3, t60, ALLK) and c2_offset(t3, t60) and bitwise(t3, run("T3a", Agent10, v10, sd, **kw), n=PR), "T3a"
    ex, parts = m7a_t3a(t3)
    print(f"ok  T3a: construction, presence identity, == Agent11 (N 60) on every field, == Agent10 on 0-58. Printed, not asserted (bench (f)): M7(a) exact {int(ex.sum())}/{n}")
    lb = run("T3b", Agent14, v10, sd, runs=n); l1 = run("T1", Agent14, v10, sd, runs=n); assert lb["draws_equal"] and lb["rng_equal"] and bitwise(lb, l1, n=T0) and not bitwise(lb, l1), "T3b"
    d = lost300(lb); e = d["elig"]
    print(f"ok  Lost world 40 x 600: draws == twin, == T1 before t0 and departs after. Printed, not asserted (bench (f)): window exact at L + 300 {int(d['exact'][e].sum())}/{int(e.sum())}")
    r = stub(Agent14, kn, [(1, 1.0, 0.0), (399, 0.0, 0.0)], rows=20); ok, ho = counter_exact(r); tb = np.arange(400)[:, None]
    assert ok.all() and (ho == 0).all() and (r["C2"][:, :, 0] == tb).all() and (r["C2"][:, :, 1] == 240 + tb + 1).all() and (r["P2"][:, :, 1] == (tb <= 58)).all() \
        and (r["P2"][:, :, 0] == (tb <= 299)).all(), "counter convention"
    print("ok  counter convention (c = 240 at construction, updated before nav; one whiff on channel 0 at step 0: c_0 = t, c_1 = 240 + t + 1; channel 1 present exactly on 0-58,"
          " channel 0 exactly on 0-299); held-only presence 0")
    v = ph23.run("T1", Agent14, v10, sd, runs=n, steps=st, start="variant", hold=True); assert (v["H"][0] == 1 - v["good"]).all() and v["PRES"][:PR].all() and v["arm"] == "Agent14"
    print("ok  ph23.make hook: ph23.run builds Agent14 for bench (c)'s variant start (neutral held at step 0)")
    tab = {k: pp_k(k, 0.958) for k in (8, 10, 12, 13, 15, 20)}
    exp = {8: (0.990, 0.983), 10: (0.893, 0.955), 12: (0.650, 0.900), 13: (0.506, 0.860), 15: (0.260, 0.757), 20: (0.025, 0.420)}
    assert all(abs(tab[k][0] - exp[k][0]) < 0.003 and abs(tab[k][1] - exp[k][1]) < 0.003 for k in exp), tab
    pw = [pass_prob(np.array([x - 9.96, x + 9.96]*200), -4.9)[0] for x in (-2.7, -3.2, -3.7, -4.2)]
    assert all(abs(a_ - b_) < 0.003 for a_, b_ in zip(pw, (0.993, 0.927, 0.673, 0.290))), pw
    print("ok  pass-probability arithmetic reproduces the design's section 7 tables: M2(b)/M2(a) at k 8, 10, 12, 13, 15, 20 = " + ", ".join(f"{tab[k][0]:.3f}/{tab[k][1]:.3f}" for k in exp)
          + "; M5(b) at bar -4.9, sd 9.96, differences -2.7/-3.2/-3.7/-4.2 = " + "/".join(f"{x:.3f}" for x in pw))
    hits, nums, nf = seeds_unused(); assert not hits, f"a seed of this run appears in {hits}"
    print(f"ok  seeds {nums} appear in no other file under the repository ({nf} files scanned; excluded by name ph28.py, ph28_*.txt, h26_*.md, master_plan.md, notes/*.md, viewer/*)")
    print(f"    BARS {BARS} ({'unset: dev and eval refuse to run until decision:h26-t2-dwell-bar is written in' if BARS['T2'] is None else 'set'})")


# ------------------------------------------------------------------ the tasks (design sections 5-8)
#            class, values, G, gate, filt, fixed, Agent11 window
T1ARMS = {"adaptive": (Agent14, (1.0, 0.0), G_STAR, True, True, None, None), "base": (Agent10, (1.0, 0.0), G_STAR, True, True, None, None),
          "release-maintain": (Agent10g, (1.0, 0.0), G_STAR, True, False, None, None), "fixed N 60": (Agent11, (1.0, 0.0), G_STAR, True, True, None, 60),
          "fixed N 300": (Agent11, (1.0, 0.0), G_STAR, True, True, None, 300), "filter": (Agent8, (1.0, 0.0), G_STAR, True, True, None, None),
          "maintain": (Agent6, (1.0, 0.0), G_STAR, True, False, None, None), "pathway-off": (Agent8, (1.0, 0.0), 0.0, False, False, None, None),
          "known-answer": (None, (1.0, 0.0), 0.0, False, False, "valued", None), "neutral": (Agent14, (0.0, 0.0), G_STAR, True, True, None, None),
          "neutral-ref": (Agent10, (0.0, 0.0), G_STAR, True, True, None, None)}
T4ARMS = {"adaptive": Agent14, "base": Agent10}
T2ARMS = {"adaptive": Agent14, "base": Agent10, "maintain": Agent6, "release-maintain": Agent10g, "fixed N 60": Agent11}
T3ARMS = {"adaptive": Agent14, "floor": Agent10, "ceiling": None, "release-maintain": Agent10g, "fixed N 60": Agent11}
T3BARMS = {"adaptive": Agent14, "base": Agent10, "release-maintain": Agent10g, "fixed N 60": Agent11}


def t1arm(name, seeds, **kw):
    cls, vals, G, gate, filt, fixed, N = T1ARMS[name]
    with n11(N or 60): return run("T1", cls, vals, seeds, G=G, gate=gate, filt=filt, fixed=fixed, **kw)


def warm(world, cls, seeds, vals=(1.0, 0.0), **kw):
    if cls is None: return run(world, None, vals, seeds, fixed="neutral", **kw)
    with n11(60): return run(world, cls, vals, seeds, **kw)


def main(mode):
    if None in BARS.values():
        print(f"== H26 {mode}: REFUSED. BARS {BARS} is unset: decision:h26-t2-dwell-bar must be recorded from the bench and written into this file first (design section 8) =="); sys.exit(2)
    seeds = SEEDS[mode]
    print(f"== H26, {mode.upper()}. design {DESIGN}; G {G_STAR}, gate on where G 2; P {P_PRIOR}, N_hi {N_HI}; t0 {T0}; world seed {seeds[0]}, agent seed {seeds[1]}; {R} rows x {T} steps;"
          f" geometry C0; bootstrap seed {ph15.BOOT_SEED}; BARS {BARS}; {'operation check only (not a verdict)' if mode == 'dev' else 'the one evaluation'} ==")
    header()
    hits, nums, nf = seeds_unused(); print(f"   seed self-check: every H26 seed and derived in no other file ({nf} scanned): {not hits}{'' if not hits else ' ' + str(hits)}")
    print("   amendments: none")
    print("   rows share no state: one generator per world and one per agent population, fixed-size draws consumed in row order every step")
    t1 = {a: t1arm(a, seeds) for a in T1ARMS}; maj = {a: majority(t1[a]) for a in T1ARMS}
    print("\n== T1, the H21 choice task (+1/0) ==")
    for a in T1ARMS:
        o = t1[a]; describe_majority(a, o, *maj[a]); h21_diag(a, o)
        if a in ("adaptive", "base", "release-maintain", "fixed N 300"): drive_summary(o, a, print)
        if a in ("adaptive", "fixed N 60", "fixed N 300"):
            fd = first_true(o["DIFF8"]); hn = o["H"] == (1 - o["good"])[None, :]
            print(f"      H26 diag [{a}]: `differs8` rows {int((fd >= 0).sum())}/{R}, first `differs8` step {q3(fd[fd >= 0])}, (row, step) {int(o['DIFF8'].sum())}; valued present on"
                  f" {o['PRES'].mean():.3f} of (row, step), on {o['PRES'][hn].mean() if hn.any() else float('nan'):.3f} of neutral-held (row, step); presence identity {presence_identity(o)}")
    print("\n== T2, the absent-odour world W1 (valued column masked from step 0) and W3 (0/0) ==")
    t2 = {a: warm("W1", c, seeds) for a, c in T2ARMS.items()}
    w3 = {a: run("W3", c, (0.0, 0.0), seeds) for a, c in (("adaptive", Agent14), ("base", Agent10))}
    s2 = {a: w1sum(o) for a, o in t2.items()}
    for a, o in t2.items():
        s = s2[a]; f1 = first_true(o["NAV"])
        print(f"   [W1 {a} {o['arm']}] dwell at the present source mean {s['dwell'].mean():.3f} (quartiles {q3f(s['dwell'].astype(float))}); reach {int(s['reach'].sum())}/{R}; lost rows {int(s['lost'].sum())};"
              f" wall contacts per row {s['contacts'].mean():.3f}; first surge step {qq(f1)}; holding B at {T} {int(s['heldB_end'].sum())}; draws == twin {o['draws_equal'] and o['rng_equal']}")
    print("\n== T3a, the constructed loss (valued column masked from step 0, start at the valued source, valued hold s 2.0) ==")
    t3a = {a: warm("T3a", c, seeds) for a, c in T3ARMS.items()}; D = {a: t3_dwell(t3a[a], 100, T) for a in t3a}
    for a, o in t3a.items():
        line = f"   [T3a {a} {o['arm']}] neutral dwell 100-599 mean {D[a].mean():.3f} (quartiles {q3f(D[a])}), rows > 0 {int((D[a] > 0).sum())}"
        if a != "ceiling":
            s3 = t3a_steps(o); line += (f"; valued hold end step {qq(s3['end'])}; first neutral surge {qq(s3['surge'])}; first neutral hold {qq(s3['hold'])}; first within 3.0 of the neutral"
                                        f" source {qq(s3['arrive'])}; holding neutral at {T} {int((o['H'][-1] == 1 - o['good']).sum())}")
        print(line)
    print("\n== T3b, the Lost world (mask on from t0 150; REPORTED) ==")
    t3b = {a: warm("T3b", c, seeds) for a, c in T3BARMS.items()}; Db = {a: t3_dwell(t3b[a], 400, T) for a in t3b}
    for a, o in t3b.items():
        hold, end, rel = ph24.t3b_release(o); mm = hold & (end >= 0)
        d = lost300(o) if a == "adaptive" else t3_lost(o); e = d["elig"]
        print(f"   [T3b {a} {o['arm']}] neutral dwell 400-599 mean {Db[a].mean():.3f} (quartiles {q3f(Db[a])}); eligible {int(e.sum())}/{R}; holding valued at t0 {int(hold.sum())}, ended"
              f" {int(mm.sum())} at origin + {q3(rel[mm])}; first-neutral-surge delay after L {q3(d['delay'][e & (d['delay'] >= 0)])} (none {int((e & (d['delay'] < 0)).sum())})"
              + (f"; post-whiff window exact at L + {N_HI} {int(d['exact'][e].sum())}/{int(e.sum())}" if a == "adaptive" else f"; window-60 exact (ph25's check) {int(d['exact'][e].sum())}/{int(e.sum())}"))
    print("\n== T4, +1/-1 (World7; REPORTED) ==")
    t4 = {a: run("T1", c, (1.0, -1.0), seeds) for a, c in T4ARMS.items()}
    for a, o in t4.items():
        V, N, Z = majority(o); k, pt, lo, hi = interval("P", V)
        print(f"   [T4 {a} {o['arm']}] V {int(V.sum())} N {int(N.sum())} tie {int(Z.sum())}; P(V) {pt:.3f} [{lo:.3f}, {hi:.3f}]; lost rows {int(lost_t1(o).sum())}; wall contacts per row {o['contacts'].mean():.3f}")
    judge(seeds, t1, maj, t2, s2, w3, t3a, D, t3b, Db, t4)


def judge(seeds, t1, maj, t2, s2, w3, t3a, D, t3b, Db, t4):
    ok = lambda z: "PASS" if z else "FAIL"
    print("\n== criteria (design v2 FINAL section 7; 95 percent, one evaluation, no extension; aggregation: PASS if every part passes, FAIL if any fails, else INCONCLUSIVE; the unrounded bound decides) ==")
    print(f"   bar read from BARS: bar_T2 {BARS['T2']} (decision:h26-t2-dwell-bar); M5(d) as re-signed (decision:h26-m5d-bar-resigned)")
    m1 = []
    for a in ("neutral", "pathway-off", "known-answer"):
        z = maj[a][2]; m1.append(ok(z.mean() <= 0.20)); print(f"   M1(a) {a}: ties {z.sum()}/{R} = {z.mean():.3f}  at most 0.20 -> {m1[-1]}")
    o = t1["neutral"]; V, N, Z = maj["neutral"]; which = np.where(V, o["good"], np.where(N, 1 - o["good"], -1))
    m1.append(crit("M1(b) neutral, P(+y source majority | chose)", "P", (0.35, 0.65), False, (which == o["plus_y"])[~Z]))
    V, N, Z = maj["pathway-off"]; m1.append(crit("M1(c) floor: pathway-off, P(V | chose)", "P", (0.35, 0.65), False, V[~Z]))
    m1.append(crit("M1(d) ceiling: known-answer, P(V) over all rows", "P", 0.85, False, maj["known-answer"][0]))
    M1 = agg(m1); print(f"   M1 -> {M1}{'' if M1 == 'PASS' else '  (the run is UNREADABLE under section 8)'}")
    ties = {a: maj[a][2].mean() for a in ("adaptive", "base", "release-maintain")}
    print("   section 8: ties in the arms under test " + ", ".join(f"{a} {v:.3f}" for a, v in ties.items()) + " (unreadable above 0.20)")
    Va, V10, V10g, V8, V6 = (maj[a][0] for a in ("adaptive", "base", "release-maintain", "filter", "maintain"))
    m2 = [crit("M2(a) adaptive (Agent14), P(V) over all rows", "P", 0.88, False, Va),
          crit("M2(b) DP = P(V) Agent14 - Agent10, same rows", "DP", -0.05, False, Va.astype(float), V10.astype(float)),
          crit("M2(c) DP = P(V) Agent14 - Agent10g, same rows", "DP", 0.05, False, Va.astype(float), V10g.astype(float))]
    M2 = agg(m2); print(f"   M2 -> {M2}")
    for lab, Vr in (("Agent6", V6), ("Agent8", V8), ("Agent11 (N 300)", maj["fixed N 300"][0]), ("Agent11 (N 60)", maj["fixed N 60"][0])):
        _, dp, lo, hi = interval("DP", Va.astype(float), Vr.astype(float)); print(f"      reported: DP Agent14 - {lab} {dp:+.4f} [{lo:+.4f}, {hi:+.4f}]")
    for a in ("adaptive", "base", "release-maintain", "fixed N 60", "fixed N 300", "filter", "maintain", "known-answer", "pathway-off"):
        k, pt, lo, hi = interval("P", maj[a][0]); print(f"      reported: {a} ({t1[a]['arm']}) V {maj[a][0].sum()} N {maj[a][1].sum()} tie {maj[a][2].sum()}; P(V) {k}/{R} = {pt:.3f} [{lo:.3f}, {hi:.3f}]")
    ca, cb, c300 = cls3(t1["adaptive"]), cls3(t1["base"]), cls3(t1["fixed N 300"]); e10 = eqmask(t1["adaptive"], t1["base"]).all(0)
    risk, fv10 = at_risk(t1["base"]); eq300 = roweq(t1["adaptive"], t1["fixed N 300"]); dep = ~roweq(t1["adaptive"], t1["fixed N 300"], BEHK)
    out_a, out_3 = int(((ca != 0) & (cb == 0)).sum()), int(((c300 != 0) & (cb == 0)).sum())
    print(f"      where the value goes (T1 identity counts): rows bitwise Agent10 throughout {int(e10.sum())}, departing {int((~e10).sum())}; into V {int(((ca == 0) & (cb != 0)).sum())},"
          f" out of V {out_a}; at-risk rows (reading R3) {int(risk.sum())}; rows departing from Agent11 (N 300) {int(dep.sum())}; k = out-of-V Agent14 - Agent11 (N 300) = {out_a} - {out_3}"
          f" = {out_a - out_3}; holding valued at {T}: Agent14 {int(hold600(t1['adaptive']).sum())}, Agent10 {int(hold600(t1['base']).sum())}")
    # M3
    i = {}; a14 = t1["adaptive"]
    i["scope off == Agent10 (T1)"] = bitwise(t1arm("adaptive", seeds, scope="off"), t1["base"])
    i["(P 60, N_hi 60) == Agent11 (T1)"] = bitwise(run("T1", Agent14, (1.0, 0.0), seeds, P=60, N_hi=60), t1["fixed N 60"], ALLK + ("P2", "C2"))
    i["neutral 0/0 == Agent10"] = bitwise(t1["neutral"], t1["neutral-ref"])
    i["+1/-1 == Agent10 (reported identity)"] = bitwise(t4["adaptive"], t4["base"])
    i["presence identity T1, W1, T3a"] = presence_identity(a14) and presence_identity(t2["adaptive"]) and presence_identity(t3a["adaptive"])
    s_ok, s_cnt = sep10(a14, t1["base"]); i["separation vs Agent10 (T1)"] = s_ok
    w = t2["adaptive"]; i["W1 == Agent11 (N 60) every field, == Agent10 on 0-58, nav == nav6 from 59"] = bitwise(w, t2["fixed N 60"], ALLK) and c2_offset(w, t2["fixed N 60"]) \
        and bitwise(w, t2["base"], n=PR) and bool(np.array_equal(w["NAV"][PR:], w["NAV6"][PR:]))
    i["T3a == Agent11 (N 60) every field"] = bitwise(t3a["adaptive"], t3a["fixed N 60"], ALLK) and c2_offset(t3a["adaptive"], t3a["fixed N 60"])
    fv = first_valued(a14); early = (fv >= 0) & (fv <= PR - 1); i["T1 early-whiff rows == Agent11 (N 300)"] = bool(eq300[early].all())
    i["T1 departing rows in the at-risk set"] = bool((~dep | risk).all())
    i["W3 Agent14 == Agent10"] = bitwise(w3["adaptive"], w3["base"])
    i["masked draws == World7 twin (W1, W3, T3a, T3b)"] = all(o["draws_equal"] and o["rng_equal"] for o in list(t2.values()) + list(w3.values()) + list(t3a.values()) + list(t3b.values()))
    i["T3a construction (draws, start, hold), every arm"] = all(construct_ok(o, a != "ceiling") for a, o in t3a.items())
    i["T3b == T1 on steps 0-149"] = all(bitwise(t3b[a], t1[b], n=T0) for a, b in (("adaptive", "adaptive"), ("base", "base"), ("release-maintain", "release-maintain"), ("fixed N 60", "fixed N 60")))
    M3 = ok(all(i.values()))
    print("   M3 identities: " + "; ".join(f"{k} {v}" for k, v in i.items()) + f" -> {M3}")
    print(f"      separation T1 Agent14 vs Agent10 (first `differs8`): {s_cnt}; T1 early-whiff rows {int(early.sum())}/{R}")
    # M4
    lines = []; v4, bo = bench(say=lines.append); M4 = ok(v4)
    for ln in lines:
        if ln.startswith("== M4") or ln.startswith("(b) counter exact") or ln.startswith("(f) M7(a)") or ln.startswith("(f) post-whiff") or "(d) measured" in ln or "STOP RULE" in ln or "(m) k =" in ln:
            print("      " + ln.strip())
    print(f"   M4 mechanism bench, re-run here with the bench seeds -> {M4}")
    # M5
    s9, s6, s10 = s2["adaptive"], s2["maintain"], s2["base"]
    m5 = [crit("M5(a) W1 Agent14, reach within 3.0 by 600", "P", 0.80, False, s9["reach"]),
          crit("M5(b) W1 dwell, Agent14 - Agent6, paired mean", "DP", BARS["T2"], False, s9["dwell"].astype(float), s6["dwell"].astype(float))]
    cm = s9["contacts"].mean(); m5.append(ok(cm <= 0.10)); print(f"   M5(c) W1 Agent14, wall contacts per row: mean {cm:.3f}  at most 0.10 -> {m5[-1]}")
    m5.append(crit("M5(d) W1 lost rows (no B whiff in the last third), Agent14 - Agent10 (re-signed)", "DP", 0.05, True, s9["lost"].astype(float), s10["lost"].astype(float)))
    _, g6, g6lo, g6hi = interval("DP", s9["lost"].astype(float), s6["lost"].astype(float))
    print(f"      M5(d) reported beside it (not a criterion): lost rows Agent14 {int(s9['lost'].sum())}, Agent10 {int(s10['lost'].sum())}, Agent6 {int(s6['lost'].sum())}; the gap to Agent6,"
          f" DP Agent14 - Agent6 {g6:+.4f} [{g6lo:+.4f}, {g6hi:+.4f}]")
    ex, fs, fb = first_surge_ok(w, PR); m5.append(ok(ex.all())); print(f"   M5(e) W1 first surge == first B whiff at or after step {PR}: {int(ex.sum())}/{R} rows exact -> {m5[-1]}")
    M5 = agg(m5); pp, m, sd = pass_prob(s9["dwell"] - s6["dwell"], BARS["T2"])
    print(f"   M5 -> {M5}      reported: dwell mean Agent14 {s9['dwell'].mean():.3f} / Agent10 {s10['dwell'].mean():.3f} / Agent6 {s6['dwell'].mean():.3f} / Agent10g"
          f" {s2['release-maintain']['dwell'].mean():.3f} / Agent11 (N 60) {s2['fixed N 60']['dwell'].mean():.3f}; paired Agent14 - Agent6 {m:+.3f} sd {sd:.3f}; Agent14 - Agent10"
          f" {(s9['dwell'] - s10['dwell']).mean():+.3f}; Agent10g == Agent6 row for row {bool(np.array_equal(s2['release-maintain']['dwell'], s6['dwell']))}; first surge {qq(fs)}")
    # M6
    ls, l10 = lost_t1(a14).astype(float), lost_t1(t1["base"]).astype(float)
    m6 = [crit("M6(a) T1 no whiff of either plume in the last third, Agent14 - Agent10", "DP", 0.05, True, ls, l10)]
    cm = a14["contacts"].mean(); m6.append(ok(cm <= 0.10)); print(f"   M6(b) T1 Agent14, wall contacts per row: mean {cm:.3f}  at most 0.10 -> {m6[-1]}")
    M6 = agg(m6); print(f"   M6 -> {M6}")
    # M7
    ex7, parts = m7a_t3a(t3a["adaptive"])
    m7 = [crit("M7(a) T3a Agent14, the window exact (end at 47 with both units <= 1.0, not held from 47, no nav on 0-58, first surge = first neutral whiff at or after 59)", "P", 0.95, False, ex7)]
    print(f"      M7(a) parts: end at 47 {int(parts['end47'].sum())}, not held from 47 {int(parts['notheld'].sum())}, no nav 0-58 {int(parts['nonav'].sum())}, surge {int(parts['surge'].sum())} of {R}")
    Ds, Df, Dc, Dg = D["adaptive"], D["floor"], D["ceiling"], D["release-maintain"]
    _, spn, slo, shi = interval("DP", Dc, Df); readable = slo >= 5.0; Rp, Rlo, Rhi = ratio_boot(Ds, Df, Dc); Rg, Rglo, Rghi = ratio_boot(Dg, Df, Dc)
    print(f"   M7(b) readability: span D_ceiling - D_floor = {Dc.mean():.3f} - {Df.mean():.3f} = {spn:.3f} [{slo:.3f}, {shi:.3f}], lower bound >= 5.0 -> {'readable' if readable else 'UNREADABLE'}")
    m7b = ("PASS" if Rlo >= 0.5 else "FAIL" if Rhi < 0.5 else "INCONCLUSIVE") if readable else "UNREADABLE"
    print(f"   M7(b) R = (D_Agent14 - D_floor) / (D_ceiling - D_floor) = ({Ds.mean():.3f} - {Df.mean():.3f}) / {spn:.3f} = {Rp:.4f} [{Rlo:.4f}, {Rhi:.4f}] (bootstrap 5000, rows resampled together,"
          f" seed {ph15.BOOT_SEED}); at least 0.50 -> {m7b}; reported: Agent10g R {Rg:.4f} [{Rglo:.4f}, {Rghi:.4f}]")
    m7c = i["T3a construction (draws, start, hold), every arm"] and i["T3a == Agent11 (N 60) every field"] and bitwise(t3a["adaptive"], t3a["floor"], n=PR)
    print(f"   M7(c) T3a construction for every arm, Agent14 == Agent11 (N 60) bitwise, == Agent10 on steps 0-58: {m7c} -> {ok(m7c)}")
    m7 += [m7b, ok(m7c)]; M7 = agg(m7); print(f"   M7 -> {M7}")
    # M8, reported
    print(f"   M8 T3b (REPORTED): neutral dwell 400-599 " + ", ".join(f"{a} {Db[a].mean():.3f}" for a in Db))
    for a in ("adaptive", "base"):
        V, N, Z = majority(t4[a]); k, pt, lo, hi = interval("P", V)
        print(f"   M8 T4 +1/-1 (REPORTED, outside the verdict) [{a} {t4[a]['arm']}]: V {V.sum()} N {N.sum()} tie {Z.sum()}; P(V) {pt:.3f} [{lo:.3f}, {hi:.3f}]; lost rows {int(lost_t1(t4[a]).sum())};"
              f" wall contacts per row {t4[a]['contacts'].mean():.3f}")
    print(f"      +1/-1 identity Agent14 == Agent10 bitwise: {i['+1/-1 == Agent10 (reported identity)']}")
    unread = M1 != "PASS" or max(ties.values()) > 0.20 or M3 != "PASS" or M4 != "PASS" or "UNREADABLE" in (M2, M5, M6, M7)
    verdict = all(x == "PASS" for x in (M1, M2, M3, M4, M5, M6, M7)); fail = any(x == "FAIL" for x in (M2, M5, M6, M7))
    lab = "PASS" if verdict else "UNREADABLE" if unread and not fail else "FAIL" if fail else "INCONCLUSIVE"
    print(f"\n== H26 ==  M1 {M1}  M2 {M2}  M3 {M3}  M4 {M4}  M5 {M5}  M6 {M6}  M7 {M7}  (M8 T3b, T4 reported) -> {lab}: "
          + ("with v_max scoped to odours present by a per-odour counter whose window is 300 steps after a whiff and whose prior, before the odour is first sensed, is 59 steps,"
             " the adopted agent keeps H23's result in the H21 task within 0.05 of Agent10 and at P(V) of at least 0.88; in the absent-odour world it tracks the only odour present"
             " within the registered dwell gap of the unfiltered agent; and after the valued odour is lost from step 0 it opens the filter exactly at step 59 and recovers at least"
             " half of the ceiling-floor span" if verdict else "UNREADABLE (section 8)" if lab == "UNREADABLE" else "NOT shown under the registered criteria"))


if __name__ == "__main__":
    mode = ([m for m in sys.argv[1:] if m in ("demo", "bench", "dev", "eval")] or ["demo"])[0]
    if mode == "demo": demo(); sys.exit(0)
    if mode == "bench":
        v, o = bench(); sys.exit(0 if v and not o["stop"] else 3 if v else 1)
    main(mode)
