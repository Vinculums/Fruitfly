#!/usr/bin/env python3
"""Fruits Fly regression harness (Phase 0.1).  Usage:  python3 regress.py [exp1 exp2 exp3r1 exp3r2 exp4]
Reruns Exp1 Run2, Exp2 Run1, Exp3 Run1, Exp3 Run2, Exp4 Run1 and checks every number recorded in the
Vinc run documents. Tolerances are those of record:phase0-success-criteria, stored before the first run.
Exit code 0 only if every check passes."""
import sys, json, time, math
import numpy as np
from ffcore import STM, stm_run, WTA, Net, trial, cwa

R = 200
CHECKS = []

def _add(exp, name, kind, rec, new, ok):
    CHECKS.append(dict(exp=exp, name=name, kind=kind, recorded=rec, new=new, ok=bool(ok)))

def exact(exp, name, rec, new, prec):      # criterion 1: printed precision
    _add(exp, name, "exact", rec, round(float(new), prec + 1), abs(rec - new) <= 0.5*10**-prec + 1e-12)
def same(exp, name, rec, new):             # criterion 2: qualitative outcome
    _add(exp, name, "same", rec, new, rec == new)
def frac(exp, name, rec, new):             # criterion 2: categorical fraction 0.00 / 1.00
    _add(exp, name, "frac", rec, round(float(new), 3), abs(rec - new) <= 0.02)
def count(exp, name, rec, new, n=R):       # criterion 3: stochastic count
    p = (rec + new) / (2.0*n); tol = max(4.0, 3.0*math.sqrt(2*n*p*(1-p)))
    _add(exp, name, "count", rec, int(new), abs(rec - new) <= tol)
def triple(exp, name, rec, new, n=R):
    for lab, a, b in zip(("correct", "wrong", "abstain"), rec, new): count(exp, f"{name} {lab}", a, b, n)
def cont(exp, name, rec, new):             # criterion 4: continuous under noise
    _add(exp, name, "cont", rec, round(float(new), 4), abs(rec - new) <= max(0.1*abs(rec), 0.01))

def targets(n=5): return np.random.default_rng(1000).integers(0, n, R)
def net(design, **kw): return Net(design, R, rng=np.random.default_rng(0), **kw)
def cell(design, netkw=None, **tk):
    netkw = netkw or {}
    return trial(net(design, **netkw), targets(netkw.get("n", 5)), **tk)
def idle(design, **kw):
    m = net(design, **kw)
    for _ in range(400): m.step(np.zeros((R, m.n)))
    return float(np.mean((m.memory() > 0.5).sum(1) == 0))
HARD = dict(d=0.05, cue=300)

# ------------------------------------------------------------------ Exp1 Run 2
def exp1():
    E = "exp1"
    mk = {"leak": lambda: STM("leak"), "linear": lambda: STM("linear", 0.03), "saturating": lambda: STM("sat", 0.10)}
    T1 = {"leak": (4.524, 0.0268, 0.0000, 42), "linear": (4.804, 0.6371, 0.0015, 111), "saturating": (4.853, 2.0164, 1.9993, 400)}
    for k, (pk, s100, s400, ret) in T1.items():
        h = stm_run(mk[k](), 1.0)
        exact(E, f"T1 {k} peak", pk, h.max(), 3); exact(E, f"T1 {k} s@100", s100, h[104], 4)
        exact(E, f"T1 {k} s@400", s400, h[404], 4); same(E, f"T1 {k} retention", ret, int((h[5:] > 0.5).sum()))
    amps = (0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.50, 1.00, 2.00)
    T2 = {"leak": (0,)*9, "linear": (0, 0, 0, 0, 0, 0, 0.001, 0.001, 0.003), "saturating": (0.001,)*4 + (1.999,)*5}
    for k, rec in T2.items():
        for a, r in zip(amps, rec): exact(E, f"T2 {k} amp {a}", r, stm_run(mk[k](), a)[404], 3)
    for sd, on, off in ((0.0, 200, 200), (0.02, 200, 200), (0.05, 200, 200), (0.10, 180, 172), (0.20, 118, 84)):
        count(E, f"T3 sd {sd} ON", on, sum(stm_run(mk["saturating"](), 1.0, noise=sd, seed=s)[404] > 1 for s in range(200)))
        count(E, f"T3 sd {sd} OFF", off, sum(stm_run(mk["saturating"](), 0.0, noise=sd, seed=s)[404] < 1 for s in range(200)))
    h = stm_run(mk["saturating"](), 1.0, reset_at=200)
    exact(E, "T4 s@199", 1.999, h[199], 3); exact(E, "T4 s@210", -2.097, h[210], 3); exact(E, "T4 s@400", 0.0006, h[404], 4)
    for a in (0.040, 0.050, 0.055, 0.060, 0.070):
        same(E, f"T5 alpha {a} decays (s@400 <= 0.0149)", True, bool(stm_run(STM("sat", a), 1.0)[404] <= 0.01495))
    exact(E, "T5 alpha 0.1 latch", 1.9993, stm_run(STM("sat", 0.1), 1.0)[404], 4)
    exact(E, "T5 alpha 0.2 latch", 4.0000, stm_run(STM("sat", 0.2), 1.0)[404], 4)

# ------------------------------------------------------------------ Exp2 Run 1
def exp2():
    E = "exp2"
    act = lambda s: int((s > 0.1*s.max()).sum())
    T1 = {0.005: (49, 104.5), 0.010: (50, 82.2), 0.020: (50, 64.8), 0.050: (50, 44.9), 0.100: (50, 32.1), 0.300: (50, 17.0)}
    for d, (cor, tdec) in T1.items():
        x = np.ones(5); x[0] += d; c = 0; a = []; td = []
        for seed in range(50):
            m = WTA(seed=seed); first = None
            for t in range(600):
                s = m.step(x)
                if first is None and t > 5 and act(s) == 1: first = t
            c += int(s.argmax() == 0); a.append(act(s)); td.append(first if first is not None else 600)
        count(E, f"T1 d {d} correct of 50", cor, c, 50); frac(E, f"T1 d {d} mean active", 1.0, np.mean(a))
        cont(E, f"T1 d {d} decision time", tdec, np.mean(td))
        m = WTA(w_i=0.0, seed=0)
        for t in range(600): s = m.step(x)
        same(E, f"T1 d {d} control active", 5, act(s)); exact(E, f"T1 d {d} control ratio", 1 + d, s[0]/s[1], 3)
    wins = np.zeros(5, int); single = 0
    for seed in range(500):
        m = WTA(seed=seed)
        for t in range(600): s = m.step(np.ones(5))
        single += act(s) == 1; wins[s.argmax()] += 1
    same(E, "T2 single winner of 500", 500, int(single))
    for i, r in enumerate((101, 93, 111, 102, 93)): count(E, f"T2 wins channel {i}", r, wins[i], 500)
    T3 = {0.0: (1, 1, 1, 1, 1, 1), 0.5: (0, 0, 0, 1, 1, 1), 0.9: (0, 0, 0, 0, 0, 1), 1.2: (0, 0, 0, 0, 0, 1)}
    for we, rec in T3.items():
        for x1, r in zip((1.3, 1.5, 2.0, 3.0, 4.0, 6.0), rec):
            m = WTA(w_e=we, seed=0); x = np.ones(5); x[0] = 1.2
            for t in range(900):
                if t == 300: x[1] = x1
                s = m.step(x)
            same(E, f"T3 w_e {we} x1 {x1} switched", r, int(s.argmax() == 1))
    T4 = {0.0: (5, [2.397, 1.999, 2.0, 1.998, 2.0]), 0.1: (5, [1.553, 1.056, 1.056, 1.054, 1.056]),
          0.2: (5, [1.33, 0.667, 0.666, 0.666, 0.666]), 0.3: (5, [1.409, 0.412, 0.41, 0.413, 0.41]),
          0.5: (1, [2.397, 0, 0, 0, 0]), 0.7: (1, [2.397, 0, 0, 0, 0]), 1.0: (1, [2.397, 0, 0, 0, 0]), 2.0: (1, [2.397, 0, 0, 0, 0])}
    for wi, (na, rec) in T4.items():
        m = WTA(w_i=wi, seed=0); x = np.array([1.2, 1, 1, 1, 1.])
        for t in range(1500): s = m.step(x)
        same(E, f"T4 w_i {wi} active", na, act(s))
        for i, r in enumerate(rec): cont(E, f"T4 w_i {wi} s[{i}]", r, s[i])
    for we, rec in ((0.5, [0.001, 0.001, 0.002, 0.002, 0.001]), (0.9, [0.014, 0, 0, 0, 0]), (1.2, [5.0, 0, 0, 0, 0])):
        m = WTA(w_e=we, seed=0); x = np.array([1.2, 1, 1, 1, 1.])
        for t in range(900):
            if t == 300: x = np.zeros(5)
            s = m.step(x)
        for i, r in enumerate(rec): cont(E, f"T5 w_e {we} s[{i}]", r, s[i])

# ------------------------------------------------------------------ Exp3 Run 1
def exp3r1():
    E = "exp3r1"
    for des, r in (("A", 1.00), ("B", 0.82), ("B2", 1.00)):
        (frac if r == 1.0 else lambda e, n, a, b: count(e, n, round(a*R), round(b*R)))(E, f"M0 idle {des}", r, idle(des))
    M1 = {"A": (0.02, 0.09, 0.45, 0.98, 1.00), "B": (0.23, 0.33, 0.54, 0.93, 1.00), "B2": (0.01, 0.02, 0.32, 0.98, 1.00)}
    for des, rec in M1.items():
        for d, r in zip((0.02, 0.05, 0.10, 0.20, 0.40), rec):
            count(E, f"M1 {des} d {d} correct", round(r*R), cwa(cell(des, d=d, cue=100))[0])
    M1b = {(100, 0.05): ((18, 5, 177), (66, 134, 0), (4, 0, 196)), (100, 0.10): ((89, 3, 108), (108, 92, 0), (64, 0, 136)),
           (300, 0.05): ((102, 98, 0), (66, 134, 0), (71, 0, 129)), (300, 0.10): ((171, 29, 0), (108, 92, 0), (193, 0, 7)),
           (1000, 0.05): ((102, 98, 0), (66, 134, 0), (171, 1, 28)), (1000, 0.10): ((171, 29, 0), (108, 92, 0), (200, 0, 0))}
    for (cue, d), recs in M1b.items():
        for des, rec in zip(("A", "B", "B2"), recs): triple(E, f"M1b cue {cue} d {d} {des}", rec, cwa(cell(des, d=d, cue=cue)))
    M2 = {"A": (1, 1, 1, 0, 0, 0, 0), "B": (1,)*7, "B2": (1, 1, 1, 1, 0, 0, 0)}
    for des, rec in M2.items():
        for a, r in zip((0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0), rec):
            frac(E, f"M2 {des} distractor {a}", float(r), cwa(cell(des, d=0.4, distractor=a))[0]/R)
    M3 = {("A", False): (1, 0, 0), ("B", False): (1, 0, 0), ("B2", False): (1, 0, 0),
          ("A", True): (1, 1, 1), ("B", True): (1, 0.89, 0.93), ("B2", True): (1, 1, 1)}
    for (des, rs), rec in M3.items():
        m = net(des); t0 = targets(); several = 0
        for i, r in enumerate(rec):
            out = trial(m, (t0 + i) % 5, d=0.4, reset=rs and i > 0)
            if i > 0: several += int((out == -2).sum())
            count(E, f"M3 {des} reset={rs} trial {i+1} correct", round(r*R), int((out == 1).sum()))
        if des == "A" and not rs: same(E, "M3 A no reset: several held in trials 2 and 3", 400, several)

# ------------------------------------------------------------------ Exp3 Run 2
def exp3r2():
    E = "exp3r2"
    hard = lambda netkw=None, **tk: cwa(cell("B2", netkw, **{**HARD, **tk}))
    easy = lambda netkw=None, **tk: cwa(cell("B2", netkw, d=0.4, **tk))[0]/R
    for v, rec in ((0.5, (15, 0, 185)), (0.7, (9, 0, 191)), (0.85, (29, 0, 171)), (1.0, (71, 0, 129)), (1.15, (124, 5, 71)),
                   (1.3, (146, 24, 30)), (1.5, (136, 55, 9)), (2.0, (103, 97, 0))):
        triple(E, f"w_i {v} hard", rec, hard({"w_i": v}))
        frac(E, f"w_i {v} easy", 1.0, easy({"w_i": v})); frac(E, f"w_i {v} idle", 1.0, idle("B2", w_i=v))
    for v in (0.5, 1.0, 1.2): frac(E, f"g {v} easy (no ON state)", 0.0, easy({"g": v}))
    for v, rec in ((1.5, (41, 0, 159)), (2.0, (71, 0, 129)), (3.0, (111, 4, 85)), (4.0, (140, 13, 47))):
        triple(E, f"g {v} hard", rec, hard({"g": v}))
    for v, rec in ((0.5, (86, 114, 0)), (0.75, (118, 82, 0)), (1.25, (1, 0, 199)), (1.5, (0, 0, 200))):
        triple(E, f"theta {v} hard", rec, hard({"theta": v}))
    frac(E, "theta 2.0 easy", 0.0, easy({"theta": 2.0}))
    frac(E, "k 2 idle (empty state unstable)", 0.0, idle("B2", k=2.0))
    for v, rec in ((2.0, (103, 97, 0)), (4.0, (122, 78, 0)), (16.0, (1, 0, 199))): triple(E, f"k {v} hard", rec, hard({"k": v}))
    for v, rec in ((0.5, (0, 0, 200)), (0.75, (1, 0, 199)), (0.9, (28, 0, 172)), (1.25, (147, 24, 29)), (1.5, (147, 49, 4)), (2.0, (110, 90, 0))):
        triple(E, f"x0 {v} hard", rec, hard(x0=v))
    for v, rec in ((2, (154, 46, 0)), (3, (171, 26, 3)), (5, (71, 0, 129)), (10, (0, 0, 200)), (20, (0, 0, 200))):
        triple(E, f"N {v} hard", rec, hard({"n": v})); frac(E, f"N {v} easy", 1.0, easy({"n": v}))
    for v, rec in ((0.1, (200, 0, 0)), (0.6, (18, 9, 173)), (1.0, (39, 76, 85))): triple(E, f"cue noise {v} hard", rec, hard(noise_sd=v))
    count(E, "cue noise 1.0 easy correct", round(0.83*R), round(easy(noise_sd=1.0)*R))
    G = {0.7: (2, 9, 58, 112), 0.85: (8, 29, 78, "guess"), 1.0: (41, 71, 111, "guess"), 1.15: (108, 124, "guess", "guess"),
         1.3: ("guess",)*4, 1.5: ("guess",)*4}
    for wi, row in G.items():
        frac(E, f"grid w_i {wi} g 1.0 nohold (easy)", 0.0, easy({"w_i": wi, "g": 1.0}))
        for g, rec in zip((1.5, 2.0, 3.0, 4.0), row):
            c, w, a = hard({"w_i": wi, "g": g})
            if rec == "guess":   # recorded wrong > 5; boundary widened by the count floor of 4
                same(E, f"grid w_i {wi} g {g} guess (wrong >= 2)", True, w >= 2)
            else:
                count(E, f"grid w_i {wi} g {g} correct", rec, c); same(E, f"grid w_i {wi} g {g} wrong <= 9", True, w <= 9)

# ------------------------------------------------------------------ Exp4 Run 1
def exp4():
    E = "exp4"; D = ("B2", "G1", "G2", "G3")
    for des in D: frac(E, f"idle {des}", 1.0, idle(des))
    SC = {"B2": ((0, 0, 200), (0, 0, 200), (71, 0, 129), (112, 88, 0), (107, 68, 25)),
          "G1": ((0, 0, 200), (0, 0, 200), (75, 0, 125), (112, 88, 0), (108, 42, 50)),
          "G2": ((18, 0, 182), (65, 0, 135), (94, 1, 105), (106, 3, 91), (112, 5, 83))}
    SC["G3"] = SC["G2"]
    for des in D:
        for x0, rec in zip((0.25, 0.5, 1.0, 2.0, 4.0), SC[des]): triple(E, f"scale {des} x0 {x0}", rec, cwa(cell(des, x0=x0, scaled=True, **HARD)))
    NC = {"B2": ((154, 46, 0), (171, 26, 3), (71, 0, 129), (0, 0, 200), (0, 0, 200)),
          "G1": ((152, 48, 0), (170, 25, 5), (75, 0, 125), (0, 0, 200), (0, 0, 200)),
          "G2": ((146, 54, 0), (168, 30, 2), (94, 1, 105), (0, 0, 200), (0, 0, 200)),
          "G3": ((135, 65, 0), (131, 69, 0), (94, 1, 105), (0, 0, 200), (0, 0, 200))}
    for des in D:
        for n, rec in zip((2, 3, 5, 10, 20), NC[des]): triple(E, f"N {des} N {n}", rec, cwa(cell(des, {"n": n}, **HARD)))
        for n in (2, 5, 10, 20):
            r = 0.92 if (des, n) == ("G3", 20) else 1.0; v = cwa(cell(des, {"n": n}, d=0.4))[0]
            (count(E, f"easy {des} N {n} correct", round(r*R), v) if r < 1 else frac(E, f"easy {des} N {n}", 1.0, v/R))
    for des in D:
        m = net(des); t0 = targets()
        for i in range(3): frac(E, f"3 trials {des} trial {i+1}", 1.0, float((trial(m, (t0 + i) % 5, d=0.4, reset=i > 0) == 1).mean()))
    DS = {"B2": (1, 1, 0, 0, 0, 0), "G1": (1, 1, 0, 0, 0, 0), "G2": (0,)*6, "G3": (0,)*6}
    amps = (1, 2, 3, 4, 6, 10)
    for des in D:
        for a, r in zip(amps, DS[des]): frac(E, f"distractor {des} amp {a}", float(r), cwa(cell(des, d=0.4, distractor=a))[0]/R)
    G4 = {1.5: ((11, 0, 189), ((0, 0, 200), (11, 0, 189), (128, 8, 64)), (1, 1, 1, 1, 1, 0)),
          2.0: ((63, 0, 137), ((0, 0, 200), (63, 0, 137), (145, 46, 9)), (1, 1, 1, 1, 0, 0)),
          2.5: ((110, 4, 86), ((0, 0, 200), (110, 4, 86), (112, 88, 0)), (1, 1, 1, 0, 0, 0)),
          3.0: ((142, 18, 40), ((1, 0, 199), (142, 18, 40), (102, 98, 0)), (1, 1, 0, 0, 0, 0))}
    for C, (h, sc, ds) in G4.items():
        triple(E, f"G4 C {C} hard", h, cwa(cell("G4", {"C": C}, **HARD)))
        for x0, rec in zip((0.25, 1.0, 4.0), sc): triple(E, f"G4 C {C} scale x0 {x0}", rec, cwa(cell("G4", {"C": C}, x0=x0, scaled=True, **HARD)))
        for a, r in zip(amps, ds): frac(E, f"G4 C {C} distractor amp {a}", float(r), cwa(cell("G4", {"C": C}, d=0.4, distractor=a))[0]/R)

ALL = dict(exp1=exp1, exp2=exp2, exp3r1=exp3r1, exp3r2=exp3r2, exp4=exp4)
if __name__ == "__main__":
    which = [a for a in sys.argv[1:] if a in ALL] or list(ALL); verbose = "-v" in sys.argv
    t0 = time.time()
    for w in which:
        t = time.time(); ALL[w](); print(f"[{w}] done in {time.time()-t:.1f}s", flush=True)
    fails = [c for c in CHECKS if not c["ok"]]
    for c in (CHECKS if verbose else fails):
        print(f"{'ok  ' if c['ok'] else 'FAIL'} {c['exp']:7s} {c['kind']:5s} {c['name']}: recorded {c['recorded']} new {c['new']}")
    print("\nSummary")
    for w in which:
        cs = [c for c in CHECKS if c["exp"] == w]; print(f"  {w:7s} {sum(c['ok'] for c in cs):4d} / {len(cs):4d} pass")
    print(f"  total   {len(CHECKS)-len(fails):4d} / {len(CHECKS):4d} pass, {len(fails)} fail, {time.time()-t0:.0f}s")
    json.dump(CHECKS, open("regress_result.json", "w"), indent=1, default=str)
    sys.exit(1 if fails else 0)
