#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H24 Run 2: the presence-scoped value filter (H24's rule (v-p), N 60, starting ON) on the release agent.

Usage: python ph25.py demo | bench | dev | eval

Design v2 FINAL, confirmed by the owner (decision:h24-run2-open): doc d65589bd43383a57c, hash 0d819e73...8d7e, stored
before this file existed; the classification-rule relaxation re-signed for this run only
(decision:classification-rule-relaxed-presence-counter-run2). Composition only, nothing copied, no adopted module edited:
Agent11 = ph24.Release (the H25 release) + ph23.Agent9 (H24's counter). scope 'off' + release on IS Agent10 and release off
IS Agent9 (checked bitwise). Three run-time hooks, as ph24b did (the files are not edited): ph24.make and ph23.make also
build Agent11 / Agent9; ph24.record also stores the counter's measurement fields (P2, C2, PRES, NAV6, NAV8, DIFF, DIFF8);
the demo asserts the hook leaves every ph24.run field bitwise equal. Worlds as ph24: T1 World7; W1/W3 ph22.Masked; T3a the
constructed loss; T3b ph23.Lost (t0 150). BARS is filled after the bench by decision:h24-run2-t2-dwell-bar (the registered
order, not an amendment); dev and eval refuse to run while it is unset. Nothing changes after the table.
"""
import sys, os, re, math, hashlib
import numpy as np
import ph15, ph21, ph22, ph23, ph24
from ph16 import interval, crit, R, T
from ph18 import majority, describe_majority, agg
from ph19 import h21_diag
from ph21 import G_STAR, q3, first_true, hold600
from ph23 import Agent9, N_WIN, T0, presence_identity, first_surge_ok, pass_prob, eqmask, counter_exact, wv, wn
from ph24 import Release, Agent10, Agent10g, Agent8, Agent6, bitwise, traj, drive_summary, t3_dwell, ratio_boot, pass_prob_R, q3f

sys.stdout.reconfigure(newline="\n")            # LF output, so the recorded sha256 equals the committed blob
DESIGN = "v2 FINAL doc d65589bd43383a57c hash 0d819e73eb4296091452b869de910f349055e79e8576513bddcd655cccf28d7e"
SEEDS = dict(dev=(9919, 9929), eval=(1815, 1915))
BENCH = dict(rows=400, rows_c=800, p=0.30, steps_stub=200, steps_held=260, steps=600, seed_w=20261041, seed_a=20261042)
BS = (BENCH["seed_w"], BENCH["seed_a"])
ph15.BOOT_SEED = 20261043                       # design section 7 (set after the imports, which set their own); ph16 set 95 percent
# ---- bar constant: filled from bench (d) by decision:h24-run2-t2-dwell-bar (registered order) ----
BARS = dict(T2=None)                            # bar_T2 = -0.20 x D6_W1 (M5 b)
# ----
MODS = (ph21, ph22, ph23, ph24)


def sha(p=__file__): return hashlib.sha256(open(p, "rb").read()).hexdigest()


# ------------------------------------------------------------------ the agent (design section 3)
class Agent11(Release, Agent9): """H24 Run 2: the H25 release on H24's agent (Agent9, scope 'prior', N 60)"""


# ------------------------------------------------------------------ hooks (run time; ph24 and ph23 are not edited)
_make24, _record24, _make23 = ph24.make, ph24.record, ph23.make
_SCOPE = ["prior"]


def make(cls, runs, rng, G, known, gate=True, filt=True, release=True, scope=None):
    scope = scope or _SCOPE[0]
    if cls is Agent11: return Agent11(runs, rng, G=G, known=known, rule=gate, filt=filt, scope=scope, release=release)
    if cls is Agent9: return Agent9(runs, rng, G=G, known=known, rule=gate, filt=filt, scope=scope)
    return _make24(cls, runs, rng, G, known, gate, filt, release)


def make23(cls, runs, rng, G, known, gate, filt, scope="prior"):
    if cls in (Agent11, Agent10, Agent10g): return make(cls, runs, rng, G, known, gate, filt, scope=scope)
    return _make23(cls, runs, rng, G, known, gate, filt, scope)


def record(o, t, a, h, x, pa):
    """ph24.record, plus the counter's fields; every other field untouched"""
    _record24(o, t, a, h, x, pa)
    st, n = o["H"].shape; rows = np.arange(n)
    if "P2" not in o:
        o.update(P2=np.ones((st, n, 2), bool), C2=np.zeros((st, n, 2), np.float32), PRES=np.ones((st, n), bool), NAV6=np.zeros((st, n), bool),
                 NAV8=np.zeros((st, n), bool), DIFF=np.zeros((st, n), bool), DIFF8=np.zeros((st, n), bool))
    nine = isinstance(a, Agent9); g = o.get("good", np.zeros(n, int))
    o["NAV6"][t] = getattr(a, "nav6", a.nav_hit); o["NAV8"][t] = a.nav8 if nine else a.nav_hit; o["DIFF"][t] = getattr(a, "differs", False)
    if nine: o["P2"][t] = a.present; o["C2"][t] = a.c; o["DIFF8"][t] = a.differs8
    o["PRES"][t] = o["P2"][t][rows, g]


ph24.make, ph24.record, ph23.make = make, record, make23


def run(world, cls, vals, seeds, scope="prior", **kw):
    _SCOPE[0] = scope
    try: return ph24.run(world, cls, vals, seeds, **kw)
    finally: _SCOPE[0] = "prior"


def stub(cls, known, sched, scope="prior", **kw):
    kw.setdefault("seeds", BS); _SCOPE[0] = scope                 # ph24.stub's default seeds are H25's bench seeds
    try: return ph24.stub(cls, known, sched, **kw)
    finally: _SCOPE[0] = "prior"


# ------------------------------------------------------------------ measures
def sep10(o, ref): return ph23.separation(o, ref, "DIFF8")          # == ref up to the step before the first `differs8` step
def w1sum(o):
    r = np.arange(len(o["good"])); p = 1 - o["good"]
    return ph22.summary(dict(o, pres=p, AT=o["AT2"][:, r, p], src=o["src"][r, p]))
def lost_t1(o): return ~o["W"][-T//3:].any((0, 2))
def binom_ge(p, k=365, n=400): return float(sum(math.comb(n, j)*p**j*(1 - p)**(n - j) for j in range(k, n + 1)))
def cls3(o): return np.select(list(majority(o)), [0, 1, 2])


def construct_ok(o, held=True):
    r = np.arange(len(o["good"]))
    ok = o["draws_equal"] and o["rng_equal"] and np.array_equal(o["start"], o["src"][r, o["good"]])
    return bool(ok and (not held or ((o["s0"][r, o["good"]] == 2.0).all() and (o["H0"] == o["good"]).all())))


def m7a_t3a(o):
    """M7(a), T3a (origin -1): hold ends at step 47 with both units <= 1.0; valued not held on any step >= 47; no nav on steps 0-58
    (the valued column is masked, so every whiff there is neutral-only); first neutral surge = first neutral whiff at or after 59"""
    g = o["good"]; H = o["H"]; r = np.arange(len(g)); tt = np.arange(H.shape[0])[:, None]
    end = first_true(H != g[None, :]); e = (end == 47) & (o["S"][np.maximum(end, 0), r] <= 1.0).all(1)
    nh = ~((H == g[None, :]) & (tt >= 47)).any(0); nn = ~o["NAV"][:N_WIN - 1].any(0); fs, _, _ = first_surge_ok(o)
    return e & nh & nn & fs, dict(end47=e, notheld=nh, nonav=nn, surge=fs, end=end)


def t3_lost(o): return ph23.t3(dict(o, src2=o["src"]))


def t3a_steps(o):
    r = np.arange(len(o["good"])); ng = 1 - o["good"]
    return dict(surge=first_true(o["NAV"] & wn(o)), hold=first_true(o["H"] == ng[None, :]), arrive=first_true(o["AT2"][:, r, ng]), end=first_true(o["H"] != o["good"][None, :]))


def qq(x): return q3(x[x >= 0]) + f" (rows {int((x >= 0).sum())})"


# ------------------------------------------------------------------ the mechanism bench (design section 4)
def bench(say=print):
    p = BENCH["p"]; n = BENCH["rows"]; ids, bars, out = {}, {}, {}; kn = [1.0, 0.0]
    say(f"== H24 Run 2 mechanism bench (design v2 section 4). design {DESIGN}; {BENCH}; N {N_WIN}; t0 {T0}; bootstrap seed {ph15.BOOT_SEED} ==")
    header(say)
    both = [(BENCH["steps_stub"], p, p)]
    # (a) identities
    ids["a1 stub"] = bitwise(stub(Agent11, kn, both, scope="off"), stub(Agent10, kn, both))
    ids["a1 stub, channel 1 held"] = bitwise(stub(Agent11, kn, both, scope="off", hold=1), stub(Agent10, kn, both, hold=1))
    o11, o10, o10g = run("T1", Agent11, (1.0, 0.0), BS), run("T1", Agent10, (1.0, 0.0), BS), run("T1", Agent10g, (1.0, 0.0), BS)
    ids["a1 World7"] = bitwise(run("T1", Agent11, (1.0, 0.0), BS, scope="off"), o10)
    ids["a1' stub"] = bitwise(stub(Agent11, kn, both, release=False), stub(Agent9, kn, both))
    ids["a1' World7"] = bitwise(run("T1", Agent11, (1.0, 0.0), BS, release=False), run("T1", Agent9, (1.0, 0.0), BS))
    say(f"(a1) scope 'off' == Agent10 bitwise (H, s, S, nav, since, target, positions, headings, silence counter, timeout/evidence flags): stub both channels p {p}"
        f" {BENCH['steps_stub']} steps {ids['a1 stub']}; the same with channel 1 held {ids['a1 stub, channel 1 held']}; World7 {n} x {BENCH['steps']} {ids['a1 World7']}")
    k1, k2 = "a1' stub", "a1' World7"; say(f"(a1') release False == ph23.Agent9 bitwise: stub {ids[k1]}; World7 {ids[k2]}")
    for name, kv in (("0/0", (0.0, 0.0)), ("+1/+1", (1.0, 1.0)), ("+1/-1", (1.0, -1.0))):
        s_ok = bitwise(stub(Agent11, list(kv), both), stub(Agent10, list(kv), both)); a11 = run("T1", Agent11, kv, BS); w_ok = bitwise(a11, run("T1", Agent10, kv, BS))
        key = "a2' +1/-1 (reported identity)" if kv[1] < 0 else f"a2 {name}"; ids[key] = s_ok and w_ok
        say(f"({key.split()[0]}) Agent11 at {name} == Agent10 bitwise: stub {s_ok}; World7 {n} x {BENCH['steps']} {w_ok}; `differs8` (row, step) {int(a11['DIFF8'].sum())};"
            f" valued-present fraction {a11['PRES'].mean():.3f}{'  (a reported identity; a False would be an implementation error)' if kv[1] < 0 else ''}")
    hs = [(BENCH["steps_held"], p, 0.0)]; ids["a3"] = bitwise(stub(Agent11, kn, hs), stub(Agent10, kn, hs))
    say(f"(a3) +1/0, channel 0 alone p {p} {BENCH['steps_held']} steps (the valued odour held): == Agent10 bitwise {ids['a3']}")
    ids["a4 presence identity"] = presence_identity(o11); s_ok, s_cnt = sep10(o11, o10); ids["a4 separation vs Agent10"] = s_ok
    e10 = eqmask(o11, o10).all(0); fd = first_true(o11["DIFF8"])
    say(f"(a4) presence identity, World7 +1/0 {n} x {BENCH['steps']}: nav == nav8 where the valued odour is present and == nav6 where it is not, every (row, step): {ids['a4 presence identity']};"
        f" valued present on {o11['PRES'].mean():.3f} of (row, step); `differs8` (row, step) {int(o11['DIFF8'].sum())} in {int((fd >= 0).sum())} rows, first `differs8` step {q3(fd[fd >= 0])};"
        f" rows bitwise Agent10 throughout (positions, headings, circuit) {int(e10.sum())}; separation vs Agent10 (== up to the step before the first `differs8`) {s_ok} {s_cnt}")
    w11, w10, w6, w10g = (run("W1", c, (1.0, 0.0), BS) for c in (Agent11, Agent10, Agent6, Agent10g))
    ids["a5 W1 == Agent10 on 0-58"] = bitwise(w11, w10, n=N_WIN - 1); ids["a5 W1 nav == nav6 from 59"] = bool(np.array_equal(w11["NAV"][N_WIN - 1:], w11["NAV6"][N_WIN - 1:]))
    ids["a5 W1 presence 0-58 only, draws"] = bool(w11["PRES"][:N_WIN - 1].all() and not w11["PRES"][N_WIN - 1:].any() and all(o["draws_equal"] and o["rng_equal"] for o in (w11, w10, w6, w10g)))
    say(f"(a5) W1 (valued column masked) {n} x {BENCH['steps']}: Agent11 == Agent10 bitwise on steps 0-{N_WIN - 2} {ids['a5 W1 == Agent10 on 0-58']}; nav == nav6 on every step from {N_WIN - 1}"
        f" {ids['a5 W1 nav == nav6 from 59']}; valued present exactly on steps 0-{N_WIN - 2}, masked draws == the World7 twin, generator state equal {ids['a5 W1 presence 0-58 only, draws']}")
    # (b) counter dynamics, exact
    sch = {"no whiff": [(200, 0.0, 0.0)], "one whiff on channel 0 at step 0": [(1, 1.0, 0.0), (199, 0.0, 0.0)], "20-step p 0.30 burst on channel 0": [(20, p, 0.0), (180, 0.0, 0.0)]}
    okb = np.ones(n, bool); hot = 0; tb = np.arange(200)[:, None]; r_ = np.arange(n)
    for k, s in sch.items():
        o = stub(Agent11, kn, s); P, C, H = o["P2"], o["C2"], o["H"]
        ok, _ = counter_exact(dict(X=o["W"], C=C, P=P, H=H))
        held = np.zeros(P.shape, bool); held[np.arange(200)[:, None], r_[None, :], np.maximum(H, 0)] = H >= 0; ho = (held & (C >= N_WIN)).sum((0, 2)); hot += int(ho.sum())
        if k == "no whiff": pat = (C == tb[:, :, None] + 1).all((0, 2)) & (P == (tb <= N_WIN - 2)[:, :, None]).all((0, 2)); ptxt = "c == t + 1 and present exactly on steps 0-58, both channels"
        elif k.startswith("one"): pat = (C[:, :, 0] == tb).all(0) & (P[:, :, 0] == (tb <= N_WIN - 1)).all(0); ptxt = "c_0 == t and channel 0 present exactly on steps 0-59"
        else:
            x0 = o["W"][:, :, 0]; had = x0.any(0); Lr = np.where(had, 199 - np.argmax(x0[::-1], 0), -1)
            pat = (P[:, :, 0] == np.where(had[None, :], tb < Lr[None, :] + N_WIN, tb <= N_WIN - 2)).all(0)
            ptxt = f"channel 0 absent from exactly 60 steps after the last whiff (rows with a whiff {int(had.sum())}, last whiff step {q3(Lr[had])})"
        ex = ok & pat & (ho == 0); okb &= ex
        fh = first_true(H == 0); tt = np.arange(200)[:, None]; end = first_true((H != 0) & (tt > fh[None, :]) & (fh >= 0)[None, :])
        say(f"(b) {k}: rows exact {int(ex.sum())}/{n} (recursion and present == (c < 60) or held {int(ok.sum())}; {ptxt} {int(pat.sum())}; no held-only presence {int((ho == 0).sum())});"
            f" valued hold formed in {int((fh >= 0).sum())} rows, at step {qq(fh)}, ended at step {qq(end)}; held-only presence (row, step) {int(ho.sum())}")
    k_, pt, lo, hi = interval("P", okb); bars["b"] = lo
    say(f"(b) counter exact in every schedule: {k_}/{n} = {pt:.3f} [{lo:.3f}, {hi:.3f}] (bar lower bound >= 0.95) -> {'PASS' if lo >= 0.95 else 'FAIL'}; held clause the only reason for presence with c >= 60: {hot} (row, step), expected 0 (H24: 105,222)")
    # (c) task-like neutral-hold start, reported
    nc = BENCH["rows_c"]; cc = {k: ph23.run("T1", c, (1.0, 0.0), BS, filt=c is not Agent10g, runs=nc, start="variant", hold=True) for k, c in (("Agent11", Agent11), ("Agent10", Agent10), ("Agent10g", Agent10g))}
    c11 = cc["Agent11"]; hn = c11["H"] == (1 - c11["good"])[None, :]
    say(f"(c) task-like neutral-hold start (H23 bench (b) state: neutral source + (DOWN, 0), heading upwind, neutral hold s 2.0), {nc} rows x {BENCH['steps']} steps, REPORTED, not a gate:"
        f" Agent11 neutral-held (row, step) {int(hn.sum())}, fraction with the valued odour present {c11['PRES'][hn].mean() if hn.any() else float('nan'):.3f}; rows with a valued whiff by 600 {int(wv(c11).any(0).sum())}")
    for k, o in cc.items(): kk, pt_, l_, h_ = interval("P", hold600(o)); say(f"      {k}: holding the valued odour at step {BENCH['steps']} {kk}/{nc} = {pt_:.3f} [{l_:.3f}, {h_:.3f}]")
    for k in ("Agent10", "Agent10g"):
        _, dp, l_, h_ = interval("DP", hold600(c11).astype(float), hold600(cc[k]).astype(float)); say(f"      paired DP holding valued at 600, Agent11 - {k}: {dp:+.4f} [{l_:+.4f}, {h_:+.4f}]")
    # (d) W1: implementation bar and the measurement that fixes M5(b)'s bar
    ok_d, fs, fb = first_surge_ok(w11); k_, pt, lo_d, hi = interval("P", ok_d); bars["d"] = lo_d
    d11, d10, d6, d10g = (t3_dwell(o, 0, BENCH["steps"]) for o in (w11, w10, w6, w10g)); D6W1 = float(d6.mean()); bar_t2 = round(-0.20*D6W1, 1)
    pp, m, sd = pass_prob(d11 - d6, bar_t2); _, _, blo, bhi = interval("DP", d11, d6); _, m10, b10lo, b10hi = interval("DP", d11, d10)
    say(f"(d) W1, bench seeds, {n} x {BENCH['steps']}: first surge == first B whiff at or after step {N_WIN - 1} in {k_}/{n} = {pt:.3f} [{lo_d:.3f}, {hi:.3f}] (bar lower bound >= 0.95)"
        f" -> {'PASS' if lo_d >= 0.95 else 'FAIL'}; first-surge step {qq(fs)}")
    for name, o, d in (("Agent11", w11, d11), ("Agent10", w10, d10), ("Agent6", w6, d6), ("Agent10g", w10g, d10g)):
        s = w1sum(o); f1 = first_true(o["NAV"])
        say(f"      {name}: mean W1 dwell within 3.0 over {BENCH['steps']} steps {d.mean():.3f} (quartiles {q3f(d)}); reach {int(s['reach'].sum())}/{n}; lost rows {int(s['lost'].sum())};"
            f" wall contacts per row {s['contacts'].mean():.3f}; first surge step {qq(f1)}")
    say(f"   (d) measured: D6_W1 (Agent6's mean W1 dwell) = {D6W1:.4f}; Agent10g == Agent6 row for row {bool(np.array_equal(d10g, d6))}; rule bar_T2 = -0.20 x D6_W1 rounded to 0.1 = {bar_t2:+.1f};"
        f" paired Agent11 - Agent6 mean {m:+.4f} sd {sd:.4f} (bootstrap [{blo:+.4f}, {bhi:+.4f}]); paired Agent11 - Agent10 {m10:+.4f} [{b10lo:+.4f}, {b10hi:+.4f}];"
        f" M5(b) pass probability at the measured difference (design arithmetic) {pp:.4f}")
    out.update(D6_W1=D6W1, bar_T2=bar_t2, m_T2=m, sd_T2=sd, pp_T2=pp, d11=float(d11.mean()), d10=float(d10.mean()), d10g=float(d10g.mean()), m10=m10)
    # (e) H23's implementation bars re-run on Agent11
    ra = stub(Agent11, kn, both, hold=1); ok1 = ((ra["NAV"] == ra["W"][:, :, 0]) | ~ra["P2"][:, :, 0]).all(0); _, pt1, lo1, _ = interval("P", ok1)
    ok2 = ~(o11["NAV"] & o11["PRES"] & ~wv(o11)).any(0); _, pt2, lo2, _ = interval("P", ok2); bars["e a4'"] = lo1; bars["e c'"] = lo2
    say(f"(e) (a4') channel 1 held by construction, both channels p {p}, {BENCH['steps_stub']} steps: nav == channel 0's whiff on every step with channel 0 present in {int(ok1.sum())}/{n}"
        f" = {pt1:.3f}, lower bound {lo1:.3f} (>= 0.95); (c') task start: every nav step with the valued odour present has a valued whiff in {int(ok2.sum())}/{n} = {pt2:.3f}, lower bound {lo2:.3f} (>= 0.95)")
    # (f) T3 constructions and M7(a) with the released hold
    f = {k: run("T3a", c, (1.0, 0.0), BS) for k, c in (("Agent11", Agent11), ("Agent10", Agent10), ("Agent10g", Agent10g))}
    f["ceiling"] = run("T3a", None, (1.0, 0.0), BS, fixed="neutral")
    ids["f T3a construction, every arm"] = all(construct_ok(o, k != "ceiling") for k, o in f.items())
    ex, parts = m7a_t3a(f["Agent11"]); k_, pt, lo_f, hi = interval("P", ex); bars["f M7(a) T3a"] = lo_f
    say(f"(f) T3a (valued column masked from step 0, start at the valued source, s_valued 2.0 held), bench seeds {n} x {BENCH['steps']}: draws == the twin, generator state equal, start and hold,"
        f" every arm {ids['f T3a construction, every arm']}; Agent11 presence identity {presence_identity(f['Agent11'])}; Agent11 == Agent10 bitwise on steps 0-58 {bitwise(f['Agent11'], f['Agent10'], n=N_WIN - 1)}")
    say(f"(f) M7(a) T3a exact, Agent11, every row: {k_}/{n} = {pt:.3f} [{lo_f:.3f}, {hi:.3f}] (bar lower bound >= 0.95) -> {'PASS' if lo_f >= 0.95 else 'FAIL'}; parts: hold ends at step 47 with both units"
        f" <= 1.0 {int(parts['end47'].sum())}, valued not held from 47 {int(parts['notheld'].sum())}, no nav on 0-58 {int(parts['nonav'].sum())}, first neutral surge = first neutral whiff at or after 59"
        f" {int(parts['surge'].sum())}")
    for k in ("Agent11", "Agent10", "Agent10g"):
        st = t3a_steps(f[k]); say(f"      [T3a {k}] valued hold end step {qq(st['end'])}; first neutral surge {qq(st['surge'])}; first neutral hold {qq(st['hold'])}; first within 3.0 of the neutral source {qq(st['arrive'])}")
        drive_summary(f[k], f"T3a {k}", say)
    lw = {k: run("T3b", c, (1.0, 0.0), BS) for k, c in (("Agent11", Agent11), ("Agent10", Agent10), ("Agent10g", Agent10g))}
    t1r = {"Agent11": o11, "Agent10": o10, "Agent10g": o10g}
    ids["f Lost construction, every arm"] = all(o["draws_equal"] and o["rng_equal"] for o in lw.values()) and all(bitwise(lw[k], t1r[k], n=T0) for k in lw) \
        and not any(bitwise(lw[k], t1r[k], n=T0 + 60) for k in lw)
    dl = t3_lost(lw["Agent11"]); el = dl["elig"]; k_, pt, lo_l, hi = interval("P", dl["exact"][el]); bars["f M7(a) Lost"] = lo_l
    say(f"(f) Lost world (mask on from step {T0}): draws == the twin (both columns before t0), generator state equal, each arm == its World7 run on steps 0-{T0 - 1} and departs after:"
        f" {ids['f Lost construction, every arm']}; Agent11 presence identity {presence_identity(lw['Agent11'])}")
    say(f"(f) M7(a) Lost exact, Agent11, eligible rows (a valued whiff before t0, L = the last one): {k_}/{int(el.sum())} = {pt:.3f} [{lo_l:.3f}, {hi:.3f}] (bar lower bound >= 0.95)"
        f" -> {'PASS' if lo_l >= 0.95 else 'FAIL'}; parts (no nav on L+1..L+59, first neutral surge = first neutral whiff at or after L+60, valued not held from L+60):"
        f" {int(dl['a1'][el].sum())}/{int(dl['a2'][el].sum())}/{int(dl['a3'][el].sum())}; held-only valued presence (row, step) {ph23.held_only(dict(lw['Agent11'], CNT=lw['Agent11']['C2'][:, np.arange(n), lw['Agent11']['good']]))}")
    for k in lw:
        hold, end, rel = ph24.t3b_release(lw[k]); mm = hold & (end >= 0)
        say(f"      [Lost {k}] holding valued at t0 {int(hold.sum())}/{n}; ended {int(mm.sum())} (never {int((hold & (end < 0)).sum())}), relative to the origin {q3(rel[mm])};"
            f" neutral dwell 400-599 mean {t3_dwell(lw[k], 400, 600).mean():.3f}")
    Dc, D10, D11, D10g = (t3_dwell(f[k], 100, 600) for k in ("ceiling", "Agent10", "Agent11", "Agent10g"))
    _, spn, slo, shi = interval("DP", Dc, D10); sdr = float(np.std(Dc - D10)); Rb, Rlo, Rhi = ratio_boot(D11, D10, Dc); Rg, Rglo, Rghi = ratio_boot(D10g, D10, Dc)
    say(f"   (f) T3a measured (reported; the bar does not move): neutral dwell 100-599 Agent11 {D11.mean():.3f}, floor Agent10 {D10.mean():.3f}, ceiling {Dc.mean():.3f}, Agent10g {D10g.mean():.3f};"
        f" span {spn:.3f} [{slo:.3f}, {shi:.3f}]; per-row paired sd {sdr:.3f}; R Agent11 {Rb:.4f} [{Rlo:.4f}, {Rhi:.4f}], Agent10g {Rg:.4f} [{Rglo:.4f}, {Rghi:.4f}];"
        f" M7(b) pass probability at the bench R {pass_prob_R(Rb, sdr, spn):.4f}")
    out.update(R=Rb, span=spn)
    # (h) T1 on bench seeds, and the stop rule
    V11, V10, V10g = majority(o11)[0], majority(o10)[0], majority(o10g)[0]; c11, c10 = cls3(o11), cls3(o10)
    _, dp, dlo, dhi = interval("DP", V11.astype(float), V10.astype(float)); ppb, _, sdb = pass_prob(V11.astype(float) - V10.astype(float), -0.05)
    b = float(((c11 != 0) & (c10 == 0)).mean()); sd0 = math.sqrt(max(b - dp*dp, 0.0)) if dp < 0 else 0.0
    pp0 = 0.5*(1.0 + math.erf((dp + 0.05 - 1.959964*sd0/20)/(sd0/20)/math.sqrt(2.0))) if sd0 > 0 else float(dp >= -0.05)
    ppc, _, _ = pass_prob(V11.astype(float) - V10g.astype(float), 0.05)
    stop = ppb < 0.5; out.update(dp_T1=dp, dp_lo=dlo, dp_hi=dhi, pp_M2b=ppb, stop=stop)
    say(f"(h) T1 on bench seeds, World7 +1/0 {n} x {BENCH['steps']}, REPORTED: " + "; ".join(f"{k} V {int(majority(o)[0].sum())} N {int(majority(o)[1].sum())} tie {int(majority(o)[2].sum())}"
        f" P(V) {interval('P', majority(o)[0])[1]:.3f} [{interval('P', majority(o)[0])[2]:.3f}, {interval('P', majority(o)[0])[3]:.3f}]" for k, o in (("Agent11", o11), ("Agent10", o10), ("Agent10g", o10g))))
    say(f"   (h) paired DP P(V) Agent11 - Agent10 {dp:+.4f} [{dlo:+.4f}, {dhi:+.4f}] (bootstrap 5000, seed {ph15.BOOT_SEED}); into V {int(((c11 == 0) & (c10 != 0)).sum())}, out of V {int(b*n)};"
        f" rows bitwise Agent10 throughout {int(e10.sum())}, departing {int((~e10).sum())}; lost rows {int(lost_t1(o11).sum())} vs {int(lost_t1(o10).sum())}")
    say(f"   (h) pass probabilities at the bench values (design section 7 arithmetic): M2(a) P(k >= 365 of 400) at P(V) {V11.mean():.3f}: {binom_ge(V11.mean()):.4f};"
        f" M2(b) at DP {dp:+.4f} with the measured paired sd {sdb:.4f}: {ppb:.4f} (with the out-of-V-only sd sqrt(b - DP^2) = {sd0:.4f}: {pp0:.4f});"
        f" M2(c) vs Agent10g at DP {(V11.mean() - V10g.mean()):+.4f}: {ppc:.4f}")
    say(f"   (h) STOP RULE (design v2 section 12 point 5): M2(b) pass probability {ppb:.4f} {'< 0.5 -> STOP: the run returns to the owner after the bench record' if stop else '>= 0.5 -> continue'};"
        f" v1's form (point estimate below -0.05): {dp < -0.05}")
    idok = all(ids.values()); bok = all(v >= 0.95 for v in bars.values()); verdict = idok and bok
    say(f"== M4: identities {idok}; failed {[k for k, v in ids.items() if not v]}; implementation bars (lower bounds >= 0.95) {bok} " + str({k: round(v, 4) for k, v in bars.items()})
        + f" -> M4 {'PASS: the tasks may be run' if verdict else 'FAIL, NO CANDIDATE: the rule as specified does not do what section 3 says; the tasks are NOT run'};"
        f" (c), (h) reported; (h) stop rule {'STOP' if stop else 'continue'} ==")
    return verdict, out


# ------------------------------------------------------------------ self-checks
def seeds_unused():
    """design section 9: none of the H24 Run 2 seeds or derived generators appears in any other file under the repository (recursive, digit-boundary;
    excluded by name: this file, its outputs ph25_*.txt, the Run 2 documents h24_run2_*.md, master_plan.md, notes/*.md, viewer/*). The demo seeds 5/6
    are used deliberately and are NOT part of this check; no reproduction seed is used."""
    base = [*SEEDS["dev"], *SEEDS["eval"], BENCH["seed_w"], BENCH["seed_a"], ph15.BOOT_SEED]
    derived = [s + 10_000 for s in (SEEDS["dev"][0], SEEDS["eval"][0], BENCH["seed_w"])] + [s + 20_000 for s in (SEEDS["dev"][1], SEEDS["eval"][1], BENCH["seed_a"])]
    nums = base + derived + [30261041, 40261042]
    pat = re.compile(rb"(?<!\d)(" + "|".join(map(str, nums)).encode() + rb")(?!\d)"); hits = []; nf = 0
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        top = os.path.relpath(root, repo).replace("\\", "/").split("/")[0]
        for f in files:
            if f == "ph25.py" or (f.startswith("ph25_") and f.endswith(".txt")) or (f.startswith("h24_run2_") and f.endswith(".md")) or f == "master_plan.md": continue
            if (os.path.basename(root) == "notes" and f.endswith(".md")) or top == "viewer": continue
            nf += 1
            if pat.search(open(os.path.join(root, f), "rb").read()): hits.append(os.path.relpath(os.path.join(root, f), repo))
    return hits, nums, nf


def header(say=print):
    say(f"   ph25.py sha256 {sha()}; design {DESIGN}")
    say("   depends on: " + "; ".join(f"{os.path.basename(m.__file__)} {sha(m.__file__)}" for m in MODS))
    say(f"   seeds: dev {SEEDS['dev']}, eval {SEEDS['eval']}, bench {BS}, bootstrap {ph15.BOOT_SEED}; demo seeds (5, 6) used deliberately, NOT part of the seed scan; no reproduction seed used;"
        f" BARS {BARS}")


def demo():
    print(f"== H24 Run 2 self-checks (demo). design {DESIGN} ==")
    header()
    n, st = 40, 200; kw = dict(runs=n, steps=st); sd = (5, 6); sp = [(st, 0.30, 0.30)]; kn = [1.0, 0.0]
    for cls in (Agent10, Agent10g, Agent8, Agent6):
        ph24.record, ph24.make = _record24, _make24; a = ph24.run("T1", cls, (1.0, 0.0), sd, **kw); sa = ph24.stub(cls, kn, sp, rows=n, seeds=BS)
        ph24.record, ph24.make = record, make; b = ph24.run("T1", cls, (1.0, 0.0), sd, **kw); sb = ph24.stub(cls, kn, sp, rows=n, seeds=BS)
        assert all(np.array_equal(a[k], b[k]) for k in a if isinstance(a[k], np.ndarray)), f"a hook changed a ph24.run field ({cls.__name__})"
        assert all(np.array_equal(sa[k], sb[k]) for k in sa if isinstance(sa[k], np.ndarray)), f"a hook changed a ph24.stub field ({cls.__name__})"
    print("ok  the make and record hooks leave every field of ph24.run and ph24.stub bitwise equal for ph24's agents (World7 40 x 200 and stub; Agent10, Agent10g, Agent8, Agent6)")
    o10 = run("T1", Agent10, (1.0, 0.0), sd, **kw); o11 = run("T1", Agent11, (1.0, 0.0), sd, **kw)
    assert bitwise(run("T1", Agent11, (1.0, 0.0), sd, scope="off", **kw), o10) and bitwise(stub(Agent11, kn, sp, scope="off", rows=n), stub(Agent10, kn, sp, rows=n)), "scope off is not Agent10"
    assert bitwise(run("T1", Agent11, (1.0, 0.0), sd, release=False, **kw), run("T1", Agent9, (1.0, 0.0), sd, **kw)) \
        and bitwise(stub(Agent11, kn, sp, release=False, rows=n), stub(Agent9, kn, sp, rows=n)), "release off is not Agent9"
    a9 = run("T1", Agent9, (1.0, 0.0), sd, **kw); b9 = ph23.r9("T1", sd, **kw)
    assert all(np.array_equal(a9[k], b9[k]) for k in ("POS", "HEAD", "S", "H", "NAV", "W", "SINCE", "PRES", "NAV8", "NAV6", "DIFF8")), "Agent9 here is not ph23.run's"
    print("ok  Agent11 scope 'off' == Agent10 and release=False == Agent9, bitwise (World7 and stub, 40 x 200); Agent9 through ph24.run == ph23.run (counter fields included)")
    for kv in ((0.0, 0.0), (1.0, 1.0), (1.0, -1.0)):
        assert bitwise(run("T1", Agent11, kv, sd, **kw), run("T1", Agent10, kv, sd, **kw)), f"Agent11 at {kv} is not Agent10"
    ok, cnt = sep10(o11, o10); assert presence_identity(o11) and ok and o11["PRES"][:N_WIN - 1].all(), f"presence identity / separation {cnt}"
    print(f"ok  Agent11 == Agent10 at 0/0, +1/+1, +1/-1; at +1/0 the presence identity holds on every (row, step); separation vs Agent10 {cnt}")
    w11, w10 = run("W1", Agent11, (1.0, 0.0), sd, **kw), run("W1", Agent10, (1.0, 0.0), sd, **kw); fs, _, _ = first_surge_ok(w11)
    assert bitwise(w11, w10, n=N_WIN - 1) and np.array_equal(w11["NAV"][N_WIN - 1:], w11["NAV6"][N_WIN - 1:]) and w11["PRES"][:N_WIN - 1].all() and not w11["PRES"][N_WIN - 1:].any() and fs.all(), "W1"
    assert bitwise(run("W3", Agent11, (0.0, 0.0), sd, **kw), run("W3", Agent10, (0.0, 0.0), sd, **kw)), "W3"
    print("ok  W1: Agent11 == Agent10 on steps 0-58, nav == nav6 from 59, valued present on 0-58 only, first surge = first B whiff at or after 59 in every row; W3 Agent11 == Agent10")
    t3 = run("T3a", Agent11, (1.0, 0.0), sd, **kw); assert construct_ok(t3) and presence_identity(t3) and bitwise(t3, run("T3a", Agent10, (1.0, 0.0), sd, **kw), n=N_WIN - 1), "T3a"
    lb, l1 = run("T3b", Agent11, (1.0, 0.0), sd, **kw), o11; assert lb["draws_equal"] and lb["rng_equal"] and bitwise(lb, l1, n=T0) and not bitwise(lb, l1, n=st), "T3b"
    ex, parts = m7a_t3a(t3)
    print(f"ok  T3a construction (draws, start, hold), presence identity, == Agent10 on 0-58; T3b == T1 before t0 and departs after. Printed, not asserted (bench (f) measures it): M7(a) T3a exact"
          f" {int(ex.sum())}/{n} (end at 47 {int(parts['end47'].sum())}, not held from 47 {int(parts['notheld'].sum())}, no nav 0-58 {int(parts['nonav'].sum())}, surge {int(parts['surge'].sum())})")
    r = stub(Agent11, kn, [(1, 1.0, 0.0), (99, 0.0, 0.0)], rows=20); ok, ho = counter_exact(dict(X=r["W"], C=r["C2"], P=r["P2"], H=r["H"])); tb = np.arange(100)[:, None]
    assert ok.all() and (r["C2"][:, :, 0] == tb).all() and (r["C2"][:, :, 1] == tb + 1).all() and (r["P2"][:, :, 1] == (tb <= 58)).all(), "counter convention"
    print(f"ok  counter convention (c = 0 at construction, updated before nav; one whiff on channel 0 at step 0: c_0 = t, c_1 = t + 1; channel 1 present exactly on 0-58)."
          f" Printed, not asserted (bench (b)): channel 0 present exactly on 0-59 in {int((r['P2'][:, :, 0] == (tb <= 59)).all(0).sum())}/20; held-only presence {ho}")
    c = ph23.run("T1", Agent10, (1.0, 0.0), sd, runs=n, steps=st); assert all(np.array_equal(c[k], o10[k]) for k in ("POS", "HEAD", "S", "H", "NAV")), "ph23.run hook"
    v = ph23.run("T1", Agent11, (1.0, 0.0), sd, runs=n, steps=st, start="variant", hold=True); assert (v["H"][0] == 1 - v["good"]).all() and v["PRES"].any()
    print("ok  ph23.make hook: ph23.run with Agent10 == ph24.run (task start); ph23.run builds Agent11 for bench (c)'s variant start (neutral held at step 0)")
    hits, nums, nf = seeds_unused(); assert not hits, f"a seed of this run appears in {hits}"
    print(f"ok  seeds {nums} appear in no other file under the repository ({nf} files scanned; excluded by name ph25.py, ph25_*.txt, h24_run2_*.md, master_plan.md, notes/*.md, viewer/*)")
    print(f"    BARS {BARS} ({'unset: dev and eval refuse to run until decision:h24-run2-t2-dwell-bar is written in' if BARS['T2'] is None else 'set'})")


# ------------------------------------------------------------------ the tasks (design sections 5-8)
#            class, values, G, gate, filt, fixed
T1ARMS = {"scoped": (Agent11, (1.0, 0.0), G_STAR, True, True, None), "release-filter": (Agent10, (1.0, 0.0), G_STAR, True, True, None),
          "release-maintain": (Agent10g, (1.0, 0.0), G_STAR, True, False, None), "filter": (Agent8, (1.0, 0.0), G_STAR, True, True, None),
          "maintain": (Agent6, (1.0, 0.0), G_STAR, True, False, None), "pathway-off": (Agent8, (1.0, 0.0), 0.0, False, False, None),
          "known-answer": (None, (1.0, 0.0), 0.0, False, False, "valued"), "neutral": (Agent11, (0.0, 0.0), G_STAR, True, True, None),
          "neutral-ref": (Agent10, (0.0, 0.0), G_STAR, True, True, None),
          "priority": (Agent11, (1.0, -1.0), G_STAR, True, True, None), "priority-ref": (Agent10, (1.0, -1.0), G_STAR, True, True, None)}
T2ARMS = {"scoped": Agent11, "release-filter": Agent10, "maintain": Agent6, "release-maintain": Agent10g}
T3ARMS = {"scoped": Agent11, "floor": Agent10, "release-maintain": Agent10g, "ceiling": None}


def t1arm(name, seeds, **kw):
    cls, vals, G, gate, filt, fixed = T1ARMS[name]; return run("T1", cls, vals, seeds, G=G, gate=gate, filt=filt, fixed=fixed, **kw)


def t3arm(world, name, seeds):
    if name == "ceiling": return run(world, None, (1.0, 0.0), seeds, fixed="neutral" if world == "T3a" else "valued-then-neutral")
    return run(world, T3ARMS[name], (1.0, 0.0), seeds)


def main(mode):
    if None in BARS.values():
        print(f"== H24 Run 2 {mode}: REFUSED. BARS {BARS} is unset: decision:h24-run2-t2-dwell-bar must be recorded from the bench and written into this file first (design section 8) =="); sys.exit(2)
    seeds = SEEDS[mode]; rows = np.arange(R); ok = lambda z: "PASS" if z else "FAIL"
    print(f"== H24 Run 2, {mode.upper()}. design {DESIGN}; G {G_STAR}, gate on where G 2; N {N_WIN}; t0 {T0}; world seed {seeds[0]}, agent seed {seeds[1]}; {R} rows x {T} steps;"
          f" geometry C0; bootstrap seed {ph15.BOOT_SEED}; BARS {BARS}; {'operation check only' if mode == 'dev' else 'the one evaluation'} ==")
    header()
    hits, nums, nf = seeds_unused(); print(f"   seed self-check: every Run 2 seed and derived in no other file ({nf} scanned): {not hits}{'' if not hits else ' ' + str(hits)}")
    print("   rows share no state: one generator per world and one per agent population, fixed-size draws consumed in row order every step")
    t1 = {a: t1arm(a, seeds) for a in T1ARMS}; maj = {a: majority(t1[a]) for a in T1ARMS}
    print("\n== T1, the H21 choice task ==")
    for a in T1ARMS:
        o = t1[a]; describe_majority(a, o, *maj[a]); h21_diag(a, o)
        if a in ("scoped", "release-filter", "release-maintain", "filter", "maintain"): drive_summary(o, a, print)
        if isinstance(o, dict) and o["arm"] == "Agent11":
            fd = first_true(o["DIFF8"]); hn = o["H"] == (1 - o["good"])[None, :]
            print(f"      H24 diag: `differs8` rows {int((fd >= 0).sum())}/{R}, first `differs8` step {q3(fd[fd >= 0])}, (row, step) {int(o['DIFF8'].sum())}; valued present on {o['PRES'].mean():.3f}"
                  f" of (row, step), on {o['PRES'][hn].mean() if hn.any() else float('nan'):.3f} of neutral-held (row, step); presence identity {presence_identity(o)}")
    print("\n== T2, the absent-odour world W1 (valued column masked from step 0) and W3 (0/0) ==")
    t2 = {a: run("W1", c, (1.0, 0.0), seeds) for a, c in T2ARMS.items()}
    w3 = {a: run("W3", c, (0.0, 0.0), seeds) for a, c in (("scoped", Agent11), ("release-filter", Agent10))}
    s2 = {a: w1sum(o) for a, o in t2.items()}
    for a, o in t2.items():
        s = s2[a]; f1 = first_true(o["NAV"])
        print(f"   [W1 {a} {o['arm']}] dwell at the present source mean {s['dwell'].mean():.3f} (quartiles {q3f(s['dwell'].astype(float))}); reach {int(s['reach'].sum())}/{R}; lost rows {int(s['lost'].sum())};"
              f" wall contacts per row {s['contacts'].mean():.3f}; first surge step {qq(f1)}; holding B at {T} {int(s['heldB_end'].sum())}; draws == twin {o['draws_equal'] and o['rng_equal']}")
        drive_summary(o, f"W1 {a}", print)
    print("\n== T3a, the constructed loss (valued column masked from step 0, start at the valued source, valued hold s 2.0) ==")
    t3a = {a: t3arm("T3a", a, seeds) for a in T3ARMS}; D = {a: t3_dwell(t3a[a], 100, T) for a in t3a}
    for a, o in t3a.items():
        line = f"   [T3a {a} {o['arm']}] neutral dwell 100-599 mean {D[a].mean():.3f} (quartiles {q3f(D[a])}), rows > 0 {int((D[a] > 0).sum())}"
        if a != "ceiling":
            st = t3a_steps(o); line += (f"; valued hold end step {qq(st['end'])}; first neutral surge {qq(st['surge'])}; first neutral hold {qq(st['hold'])}; first within 3.0 of the neutral source"
                                        f" {qq(st['arrive'])}; holding neutral at {T} {int((o['H'][-1] == 1 - o['good']).sum())}")
        print(line)
        if a != "ceiling": drive_summary(o, f"T3a {a}", print)
    print("\n== T3b, the Lost world (mask on from t0 150; REPORTED) ==")
    t3b = {a: t3arm("T3b", a, seeds) for a in T3ARMS}; Db = {a: t3_dwell(t3b[a], 400, T) for a in t3b}
    for a, o in t3b.items():
        line = f"   [T3b {a} {o['arm']}] neutral dwell 400-599 mean {Db[a].mean():.3f} (quartiles {q3f(Db[a])})"
        if a != "ceiling":
            hold, end, rel = ph24.t3b_release(o); mm = hold & (end >= 0); d = t3_lost(o); e = d["elig"]
            line += (f"; eligible {int(e.sum())}/{R}; holding valued at t0 {int(hold.sum())}, ended {int(mm.sum())} at origin + {q3(rel[mm])}; first-neutral-surge delay after L"
                     f" {q3(d['delay'][e & (d['delay'] >= 0)])} (none {int((e & (d['delay'] < 0)).sum())})" + (f"; M7(a)-style exact {int(d['exact'][e].sum())}/{int(e.sum())}" if a == "scoped" else ""))
        print(line)
    judge(seeds, t1, maj, t2, s2, w3, t3a, D, t3b, Db)


def judge(seeds, t1, maj, t2, s2, w3, t3a, D, t3b, Db):
    rows = np.arange(R); ok = lambda z: "PASS" if z else "FAIL"
    print("\n== criteria (design v2 FINAL section 7; 95 percent, one evaluation, no extension; aggregation: PASS if every part passes, FAIL if any fails, else INCONCLUSIVE; the unrounded bound decides) ==")
    print(f"   bar read from BARS: bar_T2 {BARS['T2']} (decision:h24-run2-t2-dwell-bar)")
    m1 = []
    for a in ("neutral", "pathway-off", "known-answer"):
        z = maj[a][2]; m1.append(ok(z.mean() <= 0.20)); print(f"   M1(a) {a}: ties {z.sum()}/{R} = {z.mean():.3f}  at most 0.20 -> {m1[-1]}")
    o = t1["neutral"]; V, N, Z = maj["neutral"]; which = np.where(V, o["good"], np.where(N, 1 - o["good"], -1))
    m1.append(crit("M1(b) neutral, P(+y source majority | chose)", "P", (0.35, 0.65), False, (which == o["plus_y"])[~Z]))
    V, N, Z = maj["pathway-off"]; m1.append(crit("M1(c) floor: pathway-off, P(V | chose)", "P", (0.35, 0.65), False, V[~Z]))
    m1.append(crit("M1(d) ceiling: known-answer, P(V) over all rows", "P", 0.85, False, maj["known-answer"][0]))
    M1 = agg(m1); print(f"   M1 -> {M1}{'' if M1 == 'PASS' else '  (the run is UNREADABLE under section 8)'}")
    ties = {a: maj[a][2].mean() for a in ("scoped", "release-filter", "release-maintain")}
    print("   section 8: ties in the arms under test " + ", ".join(f"{a} {v:.3f}" for a, v in ties.items()) + " (unreadable above 0.20)")
    Vs, V10, V10g, V8, V6 = (maj[a][0] for a in ("scoped", "release-filter", "release-maintain", "filter", "maintain"))
    m2 = [crit("M2(a) scoped (Agent11), P(V) over all rows", "P", 0.88, False, Vs),
          crit("M2(b) DP = P(V) Agent11 - Agent10, same rows", "DP", -0.05, False, Vs.astype(float), V10.astype(float)),
          crit("M2(c) DP = P(V) Agent11 - Agent10g, same rows", "DP", 0.05, False, Vs.astype(float), V10g.astype(float))]
    M2 = agg(m2); print(f"   M2 -> {M2}")
    for lab, Vr in (("Agent6", V6), ("Agent8", V8)):
        _, dp, lo, hi = interval("DP", Vs.astype(float), Vr.astype(float)); print(f"      reported: DP Agent11 - {lab} {dp:+.4f} [{lo:+.4f}, {hi:+.4f}]")
    for a in ("scoped", "release-filter", "release-maintain", "filter", "maintain", "known-answer", "pathway-off"):
        k, pt, lo, hi = interval("P", maj[a][0]); print(f"      reported: {a} ({t1[a]['arm']}) V {maj[a][0].sum()} N {maj[a][1].sum()} tie {maj[a][2].sum()}; P(V) {k}/{R} = {pt:.3f} [{lo:.3f}, {hi:.3f}]")
    e10 = eqmask(t1["scoped"], t1["release-filter"]).all(0); cs, cr = cls3(t1["scoped"]), cls3(t1["release-filter"]); fd = first_true(t1["scoped"]["DIFF8"])
    print(f"      where the value goes (T1 identity counts): rows bitwise Agent10 throughout {int(e10.sum())}, departing {int((~e10).sum())} (first `differs8` step {q3(fd[fd >= 0])});"
          f" among departing rows: Agent11 V {int(Vs[~e10].sum())} vs Agent10 V {int(V10[~e10].sum())}; into V {int(((cs == 0) & (cr != 0)).sum())}, out of V {int(((cs != 0) & (cr == 0)).sum())};"
          f" V among rows bitwise Agent10 {int(Vs[e10].sum())}/{int(e10.sum())}; holding valued at {T}: Agent11 {int(hold600(t1['scoped']).sum())}, Agent10 {int(hold600(t1['release-filter']).sum())},"
          f" Agent10g {int(hold600(t1['release-maintain']).sum())}")
    # M3
    i = {}
    i["scope off == Agent10 (T1)"] = bitwise(t1arm("scoped", seeds, scope="off"), t1["release-filter"])
    i["release off == Agent9 (T1)"] = bitwise(t1arm("scoped", seeds, release=False), run("T1", Agent9, (1.0, 0.0), seeds))
    i["neutral 0/0 == Agent10"] = bitwise(t1["neutral"], t1["neutral-ref"])
    i["priority +1/-1 == Agent10 (reported identity)"] = bitwise(t1["priority"], t1["priority-ref"])
    i["presence identity T1, W1, T3a"] = presence_identity(t1["scoped"]) and presence_identity(t2["scoped"]) and presence_identity(t3a["scoped"])
    s_ok, s_cnt = sep10(t1["scoped"], t1["release-filter"]); i["separation vs Agent10 (T1)"] = s_ok
    i["W3 Agent11 == Agent10"] = bitwise(w3["scoped"], w3["release-filter"])
    w = t2["scoped"]; i["W1 == Agent10 on 0-58, nav == nav6 from 59"] = bitwise(w, t2["release-filter"], n=N_WIN - 1) and bool(np.array_equal(w["NAV"][N_WIN - 1:], w["NAV6"][N_WIN - 1:]))
    i["masked draws == World7 twin (W1, W3, T3a, T3b)"] = all(o["draws_equal"] and o["rng_equal"] for o in list(t2.values()) + list(w3.values()) + list(t3a.values()) + list(t3b.values()))
    i["T3a construction (draws, start, hold), every arm"] = all(construct_ok(o, a != "ceiling") for a, o in t3a.items())
    i["T3b == T1 on steps 0-149"] = all(bitwise(t3b[a], t1[b], n=T0) for a, b in (("scoped", "scoped"), ("floor", "release-filter"), ("release-maintain", "release-maintain")))
    M3 = ok(all(i.values()))
    print("   M3 identities: " + "; ".join(f"{k} {v}" for k, v in i.items()) + f" -> {M3}")
    print(f"      separation T1 Agent11 vs Agent10 (first `differs8`): {s_cnt}")
    # M4
    lines = []; v4, bo = bench(say=lines.append); M4 = ok(v4)
    for ln in lines:
        if ln.startswith("== M4") or ln.startswith("(b) counter exact") or ln.startswith("(f) M7(a)") or "(d) measured" in ln or "STOP RULE" in ln: print("      " + ln.strip())
    print(f"   M4 mechanism bench, re-run here with the bench seeds -> {M4}")
    # M5
    s9, s6 = s2["scoped"], s2["maintain"]
    m5 = [crit("M5(a) W1 Agent11, reach within 3.0 by 600", "P", 0.80, False, s9["reach"]),
          crit("M5(b) W1 dwell, Agent11 - Agent6, paired mean", "DP", BARS["T2"], False, s9["dwell"].astype(float), s6["dwell"].astype(float))]
    cm = s9["contacts"].mean(); m5.append(ok(cm <= 0.10)); print(f"   M5(c) W1 Agent11, wall contacts per row: mean {cm:.3f}  at most 0.10 -> {m5[-1]}")
    m5.append(crit("M5(d) W1 lost rows (no B whiff in the last third), Agent11 - Agent6", "DP", 0.05, True, s9["lost"].astype(float), s6["lost"].astype(float)))
    ex, fs, fb = first_surge_ok(w); m5.append(ok(ex.all())); print(f"   M5(e) W1 first surge == first B whiff at or after step {N_WIN - 1}: {int(ex.sum())}/{R} rows exact -> {m5[-1]}")
    M5 = agg(m5); pp, m, sd = pass_prob(s9["dwell"] - s6["dwell"], BARS["T2"])
    print(f"   M5 -> {M5}      reported: dwell mean Agent11 {s9['dwell'].mean():.3f} / Agent10 {s2['release-filter']['dwell'].mean():.3f} / Agent6 {s6['dwell'].mean():.3f} / Agent10g"
          f" {s2['release-maintain']['dwell'].mean():.3f}; paired Agent11 - Agent6 {m:+.3f} sd {sd:.3f}; Agent11 - Agent10 {(s9['dwell'] - s2['release-filter']['dwell']).mean():+.3f};"
          f" Agent10g == Agent6 row for row {bool(np.array_equal(s2['release-maintain']['dwell'], s6['dwell']))}; first surge {qq(fs)}")
    # M6
    ls, l10 = lost_t1(t1["scoped"]).astype(float), lost_t1(t1["release-filter"]).astype(float)
    m6 = [crit("M6(a) T1 no whiff of either plume in the last third, Agent11 - Agent10", "DP", 0.05, True, ls, l10)]
    cm = t1["scoped"]["contacts"].mean(); m6.append(ok(cm <= 0.10)); print(f"   M6(b) T1 Agent11, wall contacts per row: mean {cm:.3f}  at most 0.10 -> {m6[-1]}")
    M6 = agg(m6); print(f"   M6 -> {M6}")
    # M7
    ex7, parts = m7a_t3a(t3a["scoped"])
    m7 = [crit("M7(a) T3a Agent11, the window exact (end at 47 with both units <= 1.0, not held from 47, no nav on 0-58, first surge = first neutral whiff at or after 59)", "P", 0.95, False, ex7)]
    print(f"      M7(a) parts: end at 47 {int(parts['end47'].sum())}, not held from 47 {int(parts['notheld'].sum())}, no nav 0-58 {int(parts['nonav'].sum())}, surge {int(parts['surge'].sum())} of {R}")
    Ds, Df, Dc, Dg = D["scoped"], D["floor"], D["ceiling"], D["release-maintain"]
    _, spn, slo, shi = interval("DP", Dc, Df); readable = slo >= 5.0; Rp, Rlo, Rhi = ratio_boot(Ds, Df, Dc); Rg, Rglo, Rghi = ratio_boot(Dg, Df, Dc)
    print(f"   M7(b) readability: span D_ceiling - D_floor = {Dc.mean():.3f} - {Df.mean():.3f} = {spn:.3f} [{slo:.3f}, {shi:.3f}], lower bound >= 5.0 -> {'readable' if readable else 'UNREADABLE'}")
    m7b = ("PASS" if Rlo >= 0.5 else "FAIL" if Rhi < 0.5 else "INCONCLUSIVE") if readable else "UNREADABLE"
    print(f"   M7(b) R = (D_Agent11 - D_floor) / (D_ceiling - D_floor) = ({Ds.mean():.3f} - {Df.mean():.3f}) / {spn:.3f} = {Rp:.4f} [{Rlo:.4f}, {Rhi:.4f}] (bootstrap 5000, rows resampled together,"
          f" seed {ph15.BOOT_SEED}); at least 0.50 -> {m7b}; reported: Agent10g R {Rg:.4f} [{Rglo:.4f}, {Rghi:.4f}]")
    m7c = i["T3a construction (draws, start, hold), every arm"] and bitwise(t3a["scoped"], t3a["floor"], n=N_WIN - 1)
    print(f"   M7(c) T3a construction for every arm, and Agent11 == Agent10 bitwise on steps 0-58: {m7c} -> {ok(m7c)}")
    m7 += [m7b, ok(m7c)]; M7 = agg(m7); print(f"   M7 -> {M7}")
    # M8, +1/-1 reported
    print(f"   M8 T3b (REPORTED): neutral dwell 400-599 " + ", ".join(f"{a} {Db[a].mean():.3f}" for a in Db) + f"; span ceiling - floor {Db['ceiling'].mean() - Db['floor'].mean():.3f} (a ratio is not read)")
    for a in ("priority", "priority-ref"):
        k, pt, lo, hi = interval("P", maj[a][0])
        print(f"   +1/-1 (REPORTED, outside the verdict) [{a} {t1[a]['arm']}]: V {maj[a][0].sum()} N {maj[a][1].sum()} tie {maj[a][2].sum()}; P(V) {pt:.3f} [{lo:.3f}, {hi:.3f}]; lost rows"
              f" {int(lost_t1(t1[a]).sum())}; wall contacts per row {t1[a]['contacts'].mean():.3f}")
    print(f"      +1/-1 identity Agent11 == Agent10 bitwise: {i['priority +1/-1 == Agent10 (reported identity)']}")
    unread = M1 != "PASS" or max(ties.values()) > 0.20 or M3 != "PASS" or M4 != "PASS" or "UNREADABLE" in (M2, M5, M6, M7)
    verdict = all(x == "PASS" for x in (M1, M2, M3, M4, M5, M6, M7)); fail = any(x == "FAIL" for x in (M2, M5, M6, M7))
    lab = "PASS" if verdict else "UNREADABLE" if unread and not fail else "FAIL" if fail else "INCONCLUSIVE"
    print(f"\n== H24 Run 2 ==  M1 {M1}  M2 {M2}  M3 {M3}  M4 {M4}  M5 {M5}  M6 {M6}  M7 {M7}  (M8, +1/-1 reported) -> {lab}: "
          + ("with v_max scoped to odours present by a per-odour counter (window 60, starting ON) on the agent with the H25 release, the agent keeps H23's result in the H21 task within"
             " 0.05 of that agent and at P(V) of at least 0.88; in the absent-odour world it tracks the only odour present within the registered dwell gap of the unfiltered agent;"
             " and after the valued odour is lost it releases the valued hold, opens the filter exactly when the counter expires, and recovers at least half of the ceiling-floor span"
             if verdict else "UNREADABLE (section 8)" if lab == "UNREADABLE" else "NOT shown under the registered criteria"))


if __name__ == "__main__":
    mode = ([m for m in sys.argv[1:] if m in ("demo", "bench", "dev", "eval")] or ["demo"])[0]
    if mode == "demo": demo(); sys.exit(0)
    if mode == "bench":
        v, o = bench(); sys.exit(0 if v and not o["stop"] else 3 if v else 1)
    main(mode)
