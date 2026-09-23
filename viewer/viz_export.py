# -*- coding: utf-8 -*-
"""Export per-step trajectories of recorded Fruits Fly runs (T1 = H23 eval, W1 = absent-odour eval, T3 = H24 bench (f)).

Read-only with respect to the repository: modules are imported unchanged, no bytecode is written, every output
goes next to this file. The run loop is ph23.run copied (it is the generalisation of ph21.run and ph22.run: same
construction order world -> values -> agent -> cast draw, same per-step order sense -> wind -> act -> move -> bump),
with logging added and the non-random bookkeeping dropped. It is checked bitwise against the modules' own run
functions (ph21.task, ph22.run, ph23.run) and the aggregate counts are asserted against the recorded outputs
before anything is exported.
"""
import sys, os, json, datetime
sys.dont_write_bytecode = True                     # do not write __pycache__ into the repository
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src')
sys.path.insert(0, SRC)
import numpy as np
import ph21, ph22, ph23
from ph16 import World7, cast_draw, R, T, DOWN, SEP
from ph17 import Agent5
from ph18 import majority
from ph19 import Agent6
from ph21 import Agent8, G_STAR
from ph23 import Agent9, Lost, T0, N_WIN
from ph9 import UPWIND, CAST_PERIOD, MAXOFF, HIT_R, SPEED, W0, SLOPE, LAM, LMAX
from ph11 import RESET_AFTER

OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.dirname(os.path.abspath(__file__))   # --out DIR: write elsewhere
SEEDS_T1, SEEDS_W1, SEEDS_T3 = ph21.SEEDS["eval"], ph22.SEEDS["eval"], ph23.BS
assert SEEDS_T1 == (1765, 1865) and SEEDS_W1 == (1775, 1875) and SEEDS_T3 == (20261011, 20261012)
KEYS = ("POS", "HEAD", "S", "H", "NAV")
log = []
def say(s=""): print(s); log.append(s)


def run(world, cls, vals, seeds, G=G_STAR, gate=True, filt=True, fixed=False, runs=R, steps=T, t0=T0):
    """ph23.run (start 'task', no hold) with per-step logging. world 'T1' World7, 'W1' ph22.Masked (valued source
    `good` silenced), 'T3' ph23.Lost (mask on from t0)."""
    masked = world != "T1"
    w = (Lost if world == "T3" else ph22.Masked if masked else World7)(runs, np.random.default_rng(seeds[0]), seeds[0])
    rows = np.arange(runs); g = w.good; neutral = 1 - g
    if masked: w.pres = neutral.copy(); w.absent = g.copy()
    tw = World7(runs, np.random.default_rng(seeds[0]), seeds[0]) if masked else None   # unmasked twin, own generator
    kv = np.zeros((runs, 2)); kv[rows, g] = vals[0]; kv[rows, neutral] = vals[1]
    rng = np.random.default_rng(seeds[1])
    a = Agent5(runs, rng, fixed=g.copy(), G=0.0, known=kv) if fixed else ph23.make(cls, runs, rng, G, kv, gate, filt)
    a.cast_sign = cast_draw(seeds[1], runs)
    o = dict(world=world, good=g.copy(), side=w.side.copy(), cell=w.cell.copy(), src2=w.src.copy(), start=w.pos.copy(), steps=steps,
             cast=a.cast_sign.copy(), draws_equal=True, first=np.full((runs, 2), -1), dwell=np.zeros((runs, 2)),
             H=np.full((steps, runs), -1, np.int8), W=np.zeros((steps, runs, 2), bool), NAV=np.zeros((steps, runs), bool),
             SINCE=np.zeros((steps, runs), np.float32), TGT=np.zeros((steps, runs)), POS=np.zeros((steps, runs, 2)),
             HEAD=np.zeros((steps, runs)), S=np.zeros((steps, runs, 2)), POOL=np.zeros((steps, runs)), AT2=np.zeros((steps, runs, 2), bool),
             TO=np.zeros((steps, runs), bool), EV=np.zeros((steps, runs), bool), C=np.zeros((steps, runs), bool))
    for t in range(steps):
        if world == "T3": w.on = t >= t0
        if masked: tw.pos, tw.head = w.pos.copy(), w.head.copy()
        whiffs = w.sense()
        if masked: tr = tw.sense()
        on = w.wind_on()
        if masked:
            mon = world != "T3" or t >= t0
            o["draws_equal"] &= bool(np.array_equal(tr, w.raw) and np.array_equal(on, tw.wind_on()) and np.array_equal(whiffs[rows, neutral], tr[rows, neutral])
                                     and np.array_equal(whiffs[rows, g], np.zeros(runs, bool) if mon else tr[rows, g]))
        turn, h = a.act(w, whiffs, on)
        w.move(turn); a.bump(w.bumped)
        at = w.at_source()
        o["first"] = np.where((o["first"] < 0) & at, t, o["first"]); o["dwell"] += at
        o["H"][t] = h; o["W"][t] = whiffs; o["NAV"][t] = a.nav_hit; o["SINCE"][t] = a.since; o["TGT"][t] = a.tgt
        o["POS"][t] = w.pos; o["HEAD"][t] = w.head; o["S"][t] = a.sel.s; o["POOL"][t] = a.sel.S[:, 0]; o["AT2"][t] = at
        o["TO"][t] = a.due_timeout; o["EV"][t] = a.due_evidence; o["C"][t] = w.bumped
    o["AT"] = o["AT2"][:, rows, neutral]; o["pres"] = neutral          # ph22.summary's keys (W1: present = neutral source)
    o["src"] = w.src[rows, neutral].copy()
    return o


def bitwise(o, ref): return all(np.array_equal(o[k], ref[k]) for k in KEYS)
def first_true(m): return np.where(m.any(0), m.argmax(0), -1)
def check(label, got, want):
    ok = got == want; say(f"   {label}: got {got}, recorded {want} -> {'MATCH' if ok else 'MISMATCH'}"); return ok


# ------------------------------------------------------------------ runs
say(f"== viz_export reproduction check, {datetime.datetime.now().isoformat(timespec='seconds')} ==")
say(f"   src {SRC}; ph21 sha256 {ph23.sha(ph21.__file__)} (H23's {ph23.PH21_SHA}); ph22 sha256 {ph23.sha(ph22.__file__)} (check's {ph23.PH22_SHA})")
V10 = (1.0, 0.0)
T1 = {"filter": run("T1", Agent8, V10, SEEDS_T1, filt=True),
      "maintain": run("T1", Agent8, V10, SEEDS_T1, filt=False),                     # ph21's maintain arm: Agent8 filt=False
      "known-answer": run("T1", Agent8, V10, SEEDS_T1, G=0.0, gate=False, filt=False, fixed=True)}
W1 = {"Agent8": run("W1", Agent8, V10, SEEDS_W1, filt=True), "Agent6": run("W1", Agent6, V10, SEEDS_W1, filt=False)}
T3 = {"Agent8": run("T3", Agent8, V10, SEEDS_T3, filt=True), "Agent6": run("T3", Agent6, V10, SEEDS_T3, filt=False),
      "Agent9": run("T3", Agent9, V10, SEEDS_T3, filt=True)}

oks = []
say("\n-- bitwise against the modules' own run functions (positions, headings, circuit s, held, nav; 400 rows x 600 steps) --")
for arm in T1: oks.append(bitwise(T1[arm], ph21.task(arm, SEEDS_T1))); say(f"   T1 {arm} == ph21.task('{arm}', {SEEDS_T1}): {oks[-1]}")
m6 = run("T1", Agent6, V10, SEEDS_T1, filt=False); oks.append(bitwise(T1["maintain"], m6)); say(f"   T1 maintain (Agent8 filt=False) == ph19.Agent6: {oks[-1]}")
for arm in W1: oks.append(bitwise(W1[arm], ph22.run("W1", arm, SEEDS_W1))); say(f"   W1 {arm} == ph22.run('W1', '{arm}', {SEEDS_W1}): {oks[-1]}")
for arm, f in (("Agent8", ph23.r8), ("Agent6", ph23.r6), ("Agent9", ph23.r9)):
    oks.append(bitwise(T3[arm], f("T3", SEEDS_T3))); say(f"   T3 {arm} == ph23.{f.__name__}('T3', {SEEDS_T3}): {oks[-1]}")
oks.append(all(o["draws_equal"] for o in (*W1.values(), *T3.values()))); say(f"   masked worlds: draws equal to the unmasked twin on every step: {oks[-1]}")

say("\n-- aggregate counts against the recorded outputs --")
cls = {}
for arm, want in (("filter", (381, 14, 5)), ("maintain", (285, 109, 6)), ("known-answer", (386, 13, 1))):
    V, N, Z = majority(T1[arm]); cls[arm] = np.select([V, N, Z], ["V", "N", "tie"], "?")
    oks.append(check(f"T1 {arm} V/N/tie (experiments/h23/ph21_eval.txt)", (int(V.sum()), int(N.sum()), int(Z.sum())), want))
S1 = {arm: ph22.summary(o) for arm, o in W1.items()}
for arm, want in (("Agent8", 344), ("Agent6", 395)):
    oks.append(check(f"W1 {arm} reach (experiments/absent_odour_check/ph22_eval.txt)", int(S1[arm]["reach"].sum()), want))
D3 = {arm: ph23.t3(o) for arm, o in T3.items()}
for arm, want in (("Agent9", 370), ("Agent8", 379), ("Agent6", 270)):
    oks.append(check(f"T3 {arm} eligible (experiments/h24/ph23_bench.txt)", int(D3[arm]["elig"].sum()), want))
s6 = D3["Agent6"]["S"][D3["Agent6"]["elig"]]
oks.append(check("T3 Agent6 S (neutral surge within L+1..L+100 | eligible), k/n", f"{int(s6.sum())}/{len(s6)}", "8/270"))
ALL_OK = all(oks)
say(f"\n== reproduction {'OK: all checks match' if ALL_OK else 'FAILED: nothing exported'} ==")
open(os.path.join(OUT, "repro_check.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(log) + "\n")
if not ALL_OK: sys.exit(1)


# ------------------------------------------------------------------ per-row quantities
def rowinfo(o, r):
    g = int(o["good"][r]); n = 1 - g; H = o["H"][:, r]
    fh = int(np.argmax(H >= 0)) if (H >= 0).any() else -1
    held_n = np.flatnonzero(H == n); rev = [t for t in np.flatnonzero(H == g) if len(held_n) and held_n[0] < t]
    fvw, fnw = o["W"][:, r, g], o["W"][:, r, n]
    return dict(first_hold=None if fh < 0 else {"odour": "valued" if H[fh] == g else "neutral", "step": fh},
                first_valued_whiff_step=int(np.argmax(fvw)) if fvw.any() else None,
                first_neutral_whiff_step=int(np.argmax(fnw)) if fnw.any() else None,
                revision_step=int(rev[0]) if rev else None,
                dwell_valued=int(o["AT2"][:, r, g].sum()), dwell_neutral=int(o["AT2"][:, r, n].sum()))

def steps(o, r):
    g = int(o["good"][r]); n = 1 - g; out = []
    for t in range(o["steps"]):
        h = int(o["H"][t, r])
        out.append({"step": t, "x": round(float(o["POS"][t, r, 0]), 2), "y": round(float(o["POS"][t, r, 1]), 2),
                    "heading_deg": round(float(o["HEAD"][t, r]), 2), "held": "none" if h < 0 else "valued" if h == g else "neutral",
                    "whiff_valued": bool(o["W"][t, r, g]), "whiff_neutral": bool(o["W"][t, r, n]), "nav": bool(o["NAV"][t, r]),
                    "since": int(o["SINCE"][t, r]), "s_valued": round(float(o["S"][t, r, g]), 3), "s_neutral": round(float(o["S"][t, r, n]), 3),
                    "S": round(float(o["POOL"][t, r]), 3), "target_deg": round(float(o["TGT"][t, r]), 2),
                    "at_valued": bool(o["AT2"][t, r, g]), "at_neutral": bool(o["AT2"][t, r, n])})
    return out

def static(world, o, r, seeds):
    g = int(o["good"][r]); sv, sn = o["src2"][r, g], o["src2"][r, 1 - g]
    return {"world": world, "row": int(r), "seeds": {"world": seeds[0], "agent": seeds[1]},
            "valued_odour": "AB"[g], "valued_side": "+y" if o["side"][r] > 0 else "-y", "cast_sign_initial": int(o["cast"][r]),
            "valued_source": [round(float(sv[0]), 2), round(float(sv[1]), 2)], "neutral_source": [round(float(sn[0]), 2), round(float(sn[1]), 2)],
            "start": [round(float(o["start"][r, 0]), 2), round(float(o["start"][r, 1]), 2)]}

rows_out = []
def export(world, res, r, seeds, why, outcome):
    ref = next(iter(res.values())); assert all(np.array_equal(o["src2"], ref["src2"]) and np.array_equal(o["start"], ref["start"]) for o in res.values())
    d = static(world, ref, r, seeds); d["selection"] = why
    d["arms"] = {arm: {"outcome": outcome(arm, o, r), **rowinfo(o, r), "steps": steps(o, r)} for arm, o in res.items()}
    rows_out.append(d); say(f"   [{world} row {r}] {why['criterion']}: {why['values']}")


# ------------------------------------------------------------------ selection
say("\n-- selected rows --")
log_sel_start = len(log)
f, m, k = T1["filter"], T1["maintain"], T1["known-answer"]; n400 = np.arange(R); g1 = f["good"]
fh = {a: ph21.diagnostics(o)["fh"] for a, o in T1.items()}
dv = lambda o: o["dwell"][n400, o["good"]]; dn = lambda o: o["dwell"][n400, 1 - o["good"]]
t1_out = lambda arm, o, r: {"class": str(cls[arm][r]), "dwell_majority_rule": "V if dwell_valued > dwell_neutral, N if <, tie if ="}

def pick(mask, score):
    idx = np.flatnonzero(mask); return int(idx[np.argmax(score[idx])]) if len(idx) else None

# (a) first hold valued in maintain and filter, both V; the one with the largest filter valued dwell
ma = (fh["maintain"] == g1) & (fh["filter"] == g1) & (cls["maintain"] == "V") & (cls["filter"] == "V")
ra = pick(ma, dv(f) + dv(m))
# (b) first hold neutral in both; maintain N, filter V; clearest contrast = maintain neutral dwell + filter valued dwell
mb = (fh["maintain"] == 1 - g1) & (fh["filter"] == 1 - g1) & (cls["maintain"] == "N") & (cls["filter"] == "V")
rb = pick(mb, dn(m) + dv(f))
# (c) filter: steps at the valued source while holding neutral
dis = ((f["H"] == (1 - g1)[None, :]) & f["AT2"][:, n400, g1]).sum(0)
rc = pick(np.ones(R, bool), dis)
# (d) one of filter's N rows: largest neutral dwell
rd = pick(cls["filter"] == "N", dn(f).astype(float))
say(f"   T1 candidate counts: (a) {int(ma.sum())} rows, (b) {int(mb.sum())} rows, (d) filter N rows {int((cls['filter'] == 'N').sum())}")
for r, crit in ((ra, "(a) first hold valued in maintain and filter, both end V; max(filter+maintain valued dwell)"),
                (rb, "(b) first hold neutral in maintain and filter, maintain N (trapped), filter V (revised); max(maintain neutral dwell + filter valued dwell)"),
                (rc, "(c) dissociation: max over rows of filter steps at the valued source while holding neutral"),
                (rd, "(d) one of filter's N rows; max neutral dwell")):
    if r is None: say(f"   T1 {crit}: NO ROW"); continue
    vals = {a: dict(cls=str(cls[a][r]), first_hold=rowinfo(o, r)["first_hold"], dwell_v=int(dv(o)[r]), dwell_n=int(dn(o)[r])) for a, o in T1.items()}
    vals["filter_steps_at_valued_holding_neutral"] = int(dis[r])
    export("T1", T1, r, SEEDS_T1, {"criterion": crit, "values": vals}, t1_out)

# W1: the present source is the neutral one (valued source silenced)
a8, a6 = W1["Agent8"], W1["Agent6"]; s8, s6_ = S1["Agent8"], S1["Agent6"]
w1_out = lambda arm, o, r: {"reach": bool(S1[arm]["reach"][r]), "dwell": int(S1[arm]["dwell"][r]), "first_reach_step": int(S1[arm]["first"][r]),
                            "final_d_along": round(float(S1[arm]["da_end"][r]), 2), "note": "reach/dwell = within HIT_R of the present (neutral) source"}
me = s8["reach"] & (s6_["dwell"] >= 20) & (s8["dwell"] < s6_["dwell"])
re_ = pick(me, -s8["da_end"] - 0.5*s8["dwell"])            # far upwind at the end, low dwell
rf = pick(~s8["reach"], s6_["dwell"].astype(float))
say(f"   W1 candidate counts: (e) {int(me.sum())} rows; (f) Agent8 never reaches {int((~s8['reach']).sum())} rows")
for r, crit in ((re_, "(e) Agent8 reaches then passes through and ends far upwind (min final d_along - 0.5 dwell) while Agent6 dwell >= 20"),
                (rf, "(f) Agent8 never reaches the present source; max Agent6 dwell")):
    if r is None: say(f"   W1 {crit}: NO ROW"); continue
    vals = {a: dict(reach=bool(S1[a]["reach"][r]), dwell=int(S1[a]["dwell"][r]), final_d_along=round(float(S1[a]["da_end"][r]), 2),
                    most_upwind_d_along=round(float(S1[a]["da_min"][r]), 2)) for a in W1}
    export("W1", W1, r, SEEDS_W1, {"criterion": crit, "values": vals}, w1_out)

# T3 (Agent9 is reproduced above but not exported, to keep the file small)
t3e = {"Agent8": T3["Agent8"], "Agent6": T3["Agent6"]}; g3 = T3["Agent8"]["good"]
def t3_out(arm, o, r):
    d = D3[arm]; h = int(o["H"][-1, r])
    return {"eligible": bool(d["elig"][r]), "L": int(d["L"][r]), "held_at_600": "none" if h < 0 else "valued" if h == g3[r] else "neutral",
            "S_neutral_surge_L1_L100": bool(d["S"][r]), "dwell_neutral_400_599": int(d["dwell"][r]),
            "note": "eligible = a valued whiff on steps 0-149; L = last valued whiff before t0 150"}
after = np.arange(T)[:, None] >= T0
hold_end8 = ((T3["Agent8"]["H"] == g3[None, :]) | ~after).all(0)                   # holds valued on every step t0..599
a6n = (T3["Agent6"]["AT2"][:, n400, 1 - g3] & after).sum(0)                        # Agent6 steps at the neutral source after t0
rel6 = ((T3["Agent6"]["H"] != g3[None, :]) & after).any(0)
mg = D3["Agent8"]["elig"] & D3["Agent6"]["elig"] & hold_end8 & rel6 & (a6n > 0)
rg = pick(mg, a6n.astype(float))
mh = D3["Agent6"]["elig"] & (a6n == 0)
rh = pick(mh & D3["Agent8"]["elig"], -D3["Agent6"]["L"].astype(float)) if (mh & D3["Agent8"]["elig"]).any() else pick(mh, -D3["Agent6"]["L"].astype(float))
say(f"   T3 candidate counts: (g) {int(mg.sum())} rows; (h) Agent6 eligible and never at the neutral source after t0 {int(mh.sum())} rows"
    f" (of them also Agent8-eligible {int((mh & D3['Agent8']['elig']).sum())})")
for r, crit in ((rg, "(g) both eligible; Agent8 holds valued on every step 150-599; Agent6 releases and is at the neutral source after t0; max Agent6 neutral steps after t0"),
                (rh, "(h) Agent6 eligible and never within HIT_R of the neutral source after t0; earliest Agent6 L")):
    if r is None: say(f"   T3 {crit}: NO ROW"); continue
    vals = {a: dict(eligible=bool(D3[a]["elig"][r]), L=int(D3[a]["L"][r]), held_at_600=t3_out(a, T3[a], r)["held_at_600"],
                    steps_at_neutral_after_t0=int((T3[a]["AT2"][:, r, 1 - g3[r]] & after[:, 0]).sum())) for a in t3e}
    vals["Agent8_holds_valued_150_599"] = bool(hold_end8[r])
    export("T3", t3e, r, SEEDS_T3, {"criterion": crit, "values": vals}, t3_out)


# ------------------------------------------------------------------ write
x0 = "x0 = source x coordinate (both sources share it; World2 draws it in [8, 14], World4 adds 60, so x0 in [68, 74])"
world_static = dict(arena={"x": [0.0, 160.0], "y": [0.0, 160.0], "walls": "reflecting (ph12b World3.move)"},
                    LMAX=LMAX, cone="0 < d_along < 25 and |d_cross| < 1.5 + 0.25*d_along (d_along = x - x_src, d_cross = y - y_src)",
                    at_source_emits="also whiffs anywhere within 3.0 of a source, at the same p",
                    whiff_p="p = 0.30*exp(-max(d_along, 0)/12) per step per source, Bernoulli", HIT_R=HIT_R, SEP=SEP, DOWN=DOWN,
                    coordinate_convention=("wind blows toward +x (heading 0); upwind = heading 180 = -x (ph9: 'wind blows toward +x, i.e. heading 0."
                                           " Upwind, toward the source, is heading 180'). Headings in degrees, heading h moves by (cos h, sin h)*0.6,"
                                           " so 90 = +y. Both sources at x = x0, y = yc +/- 5; the agent starts at (x0 + 20, yc). " + x0),
                    speed=SPEED, UPWIND_deg=UPWIND, RESET_AFTER=RESET_AFTER, CAST_PERIOD=CAST_PERIOD, MAXOFF=MAXOFF, steps=T, rows_in_run=R)
worlds = {"T1": dict(world_static, description="ph16.World7: both sources emit (H23 eval task)", seeds=list(SEEDS_T1),
                     arms={"filter": "ph21.Agent8 filt=True, G 2, gate on", "maintain": "ph21.Agent8 filt=False, G 2, gate on (bitwise ph19.Agent6)",
                           "known-answer": "ph17.Agent5 held odour fixed to the valued odour, G 0"}),
          "W1": dict(world_static, description="ph22.Masked W1: the valued odour's column is set False after the draw; only the neutral source is sensed", seeds=list(SEEDS_W1),
                     arms={"Agent8": "ph21.Agent8 filt=True", "Agent6": "ph19.Agent6"}),
          "T3": dict(world_static, description="ph23.Lost: World7 until t0, then the valued column masked (sensed then lost)", t0=T0, seeds=list(SEEDS_T3),
                     arms={"Agent8": "ph21.Agent8 filt=True", "Agent6": "ph19.Agent6"}, N_WIN_agent9=N_WIN)}
meta = dict(generated=datetime.datetime.now().isoformat(timespec="seconds"), generator=os.path.abspath(__file__), src=SRC,
            values="valued odour value +1, neutral 0 (W1: valued absent)", odour_codes="A = channel 0, B = channel 1 (ph16 CELLS)",
            step_semantics="step t: whiffs sensed at the position before the move; x, y, heading_deg, at_* after the move of step t; held, nav, since, s, S, target after act",
            reproduction=[l.strip() for l in log[:log_sel_start]], reproduction_ok=ALL_OK)
path = os.path.join(OUT, "trajectories.json")
json.dump(dict(meta=meta, worlds=worlds, rows=rows_out), open(path, "w", encoding="utf-8"), separators=(",", ":"))
say(f"\nwrote {path} ({os.path.getsize(path)/1e6:.2f} MB, {len(rows_out)} rows, {sum(len(r['arms']) for r in rows_out)} arm trajectories)")
open(os.path.join(OUT, "repro_check.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(log) + "\n")
