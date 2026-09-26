#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H12 Stage 1: the module bench. MB5 = ph8.MB4 with a per-compartment relaxation toward w0 (the parallel pair's own decay).

Usage: python ph36.py demo | bench     (stdout, LF line ends; redirected to experiments/h12/ph36_<mode>.txt)

Design: H12 design v2 FINAL, doc d27ec95924fe49be1, sha256 3d3aab80...95f1 (experiments/h12/h12_design_v2.md), opened by
decision:h12-open (owner, 2026-09-26, '권고안으로 확정하고 H12 진행', gloss 'confirm as recommended and proceed with H12': every
RECOMMENDED option of design v1 section 12). Stage 1 signs nothing and adopts nothing; no adopted file is edited: ph4.py, ph8.py and
ph11.py are imported unchanged and their sha256 is checked at run time against the prefixes the design cites (d009568c, ada2fc4b,
e80f40bd). MB5 subclasses ph8.MB4: step() calls MB4.step() unchanged and then applies one relaxation line to the compartments given a
finite time constant; with every tau None it IS MB4 (identities (I1), (I2)). The mechanism (m1) is MB5(parallel True, gated True,
tau (None, None, tau_ext, tau_ext)): the extinction pair relaxes, the acquisition pair does not.

Readings where the design is silent, chosen so that the identities stay exact (printed again in the bench output):
 (R1) The relaxation: after MB4.step (after the clip, ph8.py:96), for every compartment c with a finite tau_c,
      w[:, c, :] = w[:, c, :] + (w0 - w[:, c, :]) / tau_c, w0 = 1.0 (MB's default, ph4.py:20); on every step, silent steps included.
      It keeps w inside [0, 2], so no second clip is applied. A weight at w0 is left at w0 exactly.
 (R2) Arms (design 4.1), all gated True (the adopted gate): A0 parallel False, no tau (the adopted module); A1 parallel True, no tau
      (H11 full); P parallel True, tau (None, None, tau, tau); S1 parallel False, tau on every compartment; S2 parallel False, tau on
      compartment 1 only. Each module is built with rng default_rng(0) (ph8.mk's), which the module never draws from.
 (R3) (r): ph8.py is run as a subprocess (python3 ph8.py: H11's own main, its own seeds) and its stdout is compared line for line
      with experiments/h11/ph8_h11.txt. Any mismatch stops the bench.
 (R4) (I1), (I2) on H11's protocols: ph8.f1_battery, f2_sustained, f3_trace and f6_savings called with MB5 (tau None) factories and
      with ph8.mk's MB4 factories (parallel False and True, gated True); the returned values equal exactly. On every constructed
      schedule of design 4.1 (s), the A0 and A1 arms run in lockstep beside an ph8.MB4 twin with the same flags and w, tc, tr are
      compared bitwise at every read point (after acquisition, after extinction, at every D, after every re-pairing, on the control
      path at every D, and the naive pairing).
 (R5) (I2'): A1 against A0, the behavioural valence after EVERY step of the acquisition, extinction and re-pairing phases and at
      every read point. The two layouts sum the same quantities in a different order ((o0 - o1') + (o2 - o3) against
      (o0 - o1) + (o2 - o3')), so the design's 'exact' (2.2) holds in real arithmetic; a smoke check on the unregistered code seed 5
      (demo) found last-bit differences (1.4e-16). Read as: max |difference| <= 1e-12, the maximum printed.
 (R6) (I4): H15 Run 2's recorded source-occupancy streams are re-created by ph15.run_e1('intact', Run 2's evaluation seeds
      (1640, 1740), keep_src=True) (ph15.py:121-126; ph15's own replay check uses this call) and replayed as ph15.replay
      (ph15.py:129-135) into ph8.MB4(parallel False, gated True) and into P at tau_ext*; both end values equal the run's own end
      values o['val'][-1] bitwise, and the number of (step, row) carrying a code with no reinforcement is 0. Run 2's evaluation seeds
      are reused on purpose for this identity only and are not in the seed scan.
 (R7) Retention schedules (design 4.1 (s), 5.5): the punishment sign (compartment 0) on odour A's code MB.odour(20261151), the reward
      sign (compartment 1) on odour B's code MB.odour(20261152); acquisition = 10 forward pairings (ph8.trained), extinction = 20
      forward presentations without reinforcement (ph4.pairing(code, None), as ph8.f3_trace), then silent mb.step() calls; at each D
      in {0, 300, 1000, 3000, 5000, 10000} the valence is read (no step) and ONE forward re-pairing is applied to a deep copy (the
      silent run continues on the original). Control path: a deep copy taken after acquisition, silent steps, read at each D. Naive:
      a fresh module, one forward pairing. The baseline valence at w0 is exactly 0 (checked), so raw valences are used.
 (R8) SR's denominator: 'a, the acquisition-site valence at the end of extinction' is taken from the parallel layout without decay
      (A1) at the same K and sign. In P it is the same array bitwise (in the parallel layout compartments 0 and 1 are written only by
      external reinforcement; checked); in the single-site arms MB4.acq_valence contains the extinction trace (a = v_ext, 0/0), so
      A1's value is the acquisition site's own scale for every arm, as design 4.2 requires for 'A0 and A1 ... 0 exactly'.
      SR(D) = (|v(D)| - |v_ext|) / (|a| - |v_ext|); RET(D) = |v_ctrl(D)| / |v_ctrl trained|; REACQ(D) = |v_rep(D)| - |v(D)|; all per run.
 (R9) Statistics (design 4.2): per-run quantities; the median over the 200 runs; its 95 percent bootstrap interval (5000 resamples of
      runs, seed 20261153, percentiles 2.5 and 97.5); 'lower bound' is the interval's lower end. The module is deterministic given the
      codes (no noise), so the per-run minimum and maximum and, for P, the exact 1 - (1 - 1/tau)^D are printed beside.
 (R10) F6(D) in H11's form, on medians: |median v_rep(D) - median v_ext| / |median v_naive| (ph8.py:215-223); reported, no bar.
 (R11) Order: F1 and F2 (K 500) for every arm and tau are printed and tau_ext* is fixed by the registered rule (design 4.3) before any
      retention schedule runs; (s1) stops the bench there. SR and RET are registered at K 200 (B3, B4); K 500 is reported.
 (R12) Configurations run in parallel processes (fork); each builds its own module; the demo checks parallel == sequential.
 (R13) Seed scan (design section 9): the 18 numbers of section 9, digit-boundary, every file under the repository except .git and
      __pycache__, excluded by name: ph36.py, ph36b.py, ph36_*.txt, ph36b_*.txt, h12_*.md, master_plan.md, notes/*.md, viewer/*; and
      the (file, number) pair of decision:seed-scan-exclusion-ph31-eval (experiments/h20/ph31_eval.txt with Stage C Run 1's E1
      evaluation agent seed, read from ph30.py's seed constants, not written here). The demo's smoke seeds (5, and 3/4 for the I4
      instrument, as ph15's demo) are used deliberately for smoke checks only and are not part of the scan.
 (R14) B5 is read at tau_ext* (S1 and S2 at the same tau). (s2): B3 or B4 failing stops the item.
Nothing changes after the table.
"""
import sys, os, re, io, math, copy, hashlib, subprocess
import multiprocessing as mp
import numpy as np
import ph4, ph8, ph11
from ph4 import MB, pairing
from ph8 import MB4

sys.stdout.reconfigure(newline="\n")            # LF output, so the recorded sha256 equals the committed blob
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
DESIGN = "H12 v2 FINAL doc d27ec95924fe49be1 hash 3d3aab80cce766f4b3201c951970f4e118ddcd9506633e95a265d6a7941495f1"
DESIGN_FILE = os.path.join(REPO, "experiments", "h12", "h12_design_v2.md")
H11_TXT = os.path.join(REPO, "experiments", "h11", "ph8_h11.txt")
PREFIX = dict(ph4="d009568c", ph8="ada2fc4b", ph11="e80f40bd")                 # design v2 header
SEEDS = dict(A=20261151, B=20261152, boot=20261153)
RUN2_EVAL = (1640, 1740)                         # H15 Run 2's evaluation seeds: identity (I4) only; NOT in the seed scan
CODE = dict(pun=SEEDS["A"], rew=SEEDS["B"]); COMP = dict(pun=0, rew=1)       # reading R7 (design 5.5)
TAUS = (2000, 5000, 10000, 20000)
DS = (0, 300, 1000, 3000, 5000, 10000)
D_REG = 5000
KSET = dict(K500=dict(ph8.KW), K200=dict(ph11.MB))
R = ph8.R                                        # 200 runs (ph8.py:33)
NBOOT, QLO, QHI = 5000, 2.5, 97.5
NPROC = int(os.environ.get("PH36_PROCS", "4"))
ARMS = ("A0", "A1", "P", "S1", "S2")


def sha(p=__file__): return hashlib.sha256(open(p, "rb").read()).hexdigest()


# ------------------------------------------------------------------ the module (design 3.2, reading R1)
class MB5(MB4):
    """ph8.MB4 plus one relaxation line per compartment with a finite time constant. tau: length-C tuple, None = no decay."""

    def __init__(self, runs, tau=None, **kw):
        super().__init__(runs, **kw)
        self.w0 = float(kw.get("w0", 1.0))
        self.tau = tuple(tau) if tau is not None else (None,)*self.C
        assert len(self.tau) == self.C
        self.trace_code, self.trace = None, None                 # measurement only: valence after each step (reading R5)

    def step(self, code=None, reinf=None):
        MB4.step(self, code, reinf)
        for c, t in enumerate(self.tau):
            if t is not None:
                self.w[:, c, :] = self.w[:, c, :] + (self.w0 - self.w[:, c, :])/t
        if self.trace_code is not None: self.trace.append(self.valence(self.trace_code))


def arm_kw(arm, tau):
    """reading R2"""
    if arm == "A0": return dict(parallel=False, tau=None)
    if arm == "A1": return dict(parallel=True, tau=None)
    if arm == "P": return dict(parallel=True, tau=(None, None, tau, tau))
    if arm == "S1": return dict(parallel=False, tau=(tau, tau, tau, tau))
    if arm == "S2": return dict(parallel=False, tau=(None, tau, None, None))
    raise ValueError(arm)


def build(arm, tau, K, runs=R):
    return MB5(runs, gated=True, rng=np.random.default_rng(0), **arm_kw(arm, tau), **KSET[K])


def twin4(arm, K, runs=R):
    """the ph8.MB4 twin of A0 / A1 (reading R4)"""
    return MB4(runs, parallel=(arm == "A1"), gated=True, rng=np.random.default_rng(0), **KSET[K])


def configs():
    return [("A0", None), ("A1", None)] + [(a, t) for a in ("P", "S1", "S2") for t in TAUS]


def label(arm, tau): return arm if tau is None else f"{arm} tau {tau}"


# ------------------------------------------------------------------ (b): F1 and F2 at K 500 (ph8.py:112-155, unchanged)
def f12(job):
    arm, tau = job
    make = lambda: build(arm, tau, "K500")
    b = ph8.f1_battery(make)
    peak, final, ret, traj = ph8.f2_sustained(make)
    n = 0.95*R
    clauses = dict(acq=b["acq"] >= n, leak=b["leak"] <= 10, ext=b["ext"] <= 30, rev=b["rev"] >= n, timing=b["timing"] >= n)
    return dict(arm=arm, tau=tau, b=b, peak=peak, final=final, ret=ret, traj=traj, clauses=clauses,
                f1=all(clauses.values()), f2=ret >= 70.0)


def f12_line(r):
    b = r["b"]
    return (f"   {label(r['arm'], r['tau']):16s} F1 acq {b['acq']}/{R} (dA {b['dA']:+.3f})  leak {b['leak']:.1f}%  ext {b['ext']:.1f}%"
            f"  rev {b['rev']}/{R}  timing {b['timing']}/{R} -> {'pass' if r['f1'] else 'FAIL'}"
            f" | F2 peak {r['peak']:.3f} t400 {r['final']:.3f} retains {r['ret']:.1f}% -> {'pass' if r['f2'] else 'FAIL'}")


def tau_rule(rows):
    """design 4.3: the smallest tau at which P passes every clause of F1 and F2 at K 500"""
    for t in TAUS:
        r = [x for x in rows if x["arm"] == "P" and x["tau"] == t][0]
        if r["f1"] and r["f2"]: return t
    return None


# ------------------------------------------------------------------ (s): the retention schedules (reading R7)
def wsig(m): return hashlib.sha256(m.w.tobytes() + m.tc.tobytes() + m.tr.tobytes()).hexdigest()


def schedule(job):
    arm, tau, K, sign = job[:4]; cseed = job[4] if len(job) > 4 else CODE[sign]          # job[4]: the demo's smoke code seed
    twin = arm in ("A0", "A1"); trace = arm in ("A0", "A1")
    m = build(arm, tau, K); c = m.odour(cseed); comp = COMP[sign]
    t4 = twin4(arm, K) if twin else None
    ms = [m] + ([t4] if twin else [])
    same = []                                                              # (I1)/(I2) on the schedule, reading R4
    def chk(): same.append(bool(not twin or (np.array_equal(m.w, t4.w) and np.array_equal(m.tc, t4.tc) and np.array_equal(m.tr, t4.tr))))
    v0 = m.valence(c).copy()
    if trace: m.trace_code, m.trace = c, []
    for _ in range(10):
        for x in ms: pairing(x, c, comp, "forward")
    v_tr, a_tr = m.valence(c).copy(), m.acq_valence(c).copy(); chk()
    ctrl = copy.deepcopy(m); ctrl.trace_code = None
    ctrl4 = copy.deepcopy(t4) if twin else None
    for _ in range(20):
        for x in ms: pairing(x, c, None, "forward")
    v_ext, a_ext = m.valence(c).copy(), m.acq_valence(c).copy(); chk()
    sig_ext01 = hashlib.sha256(m.w[:, :2].tobytes()).hexdigest()
    tr_steps = [v.copy() for v in m.trace] if trace else []
    if trace: m.trace_code, m.trace = None, None
    vD, vrep, rep_tr, t_now = {}, {}, {}, 0
    for D in DS:
        for _ in range(D - t_now):
            for x in ms: x.step()
        t_now = D
        vD[D] = m.valence(c).copy(); chk()
        cp = copy.deepcopy(m); cp4 = copy.deepcopy(t4) if twin else None
        if trace: cp.trace_code, cp.trace = c, []
        pairing(cp, c, comp, "forward")
        if twin: pairing(cp4, c, comp, "forward"); same.append(bool(np.array_equal(cp.w, cp4.w) and np.array_equal(cp.tc, cp4.tc)))
        vrep[D] = cp.valence(c).copy(); rep_tr[D] = [v.copy() for v in cp.trace] if trace else []
    sig_end01 = hashlib.sha256(m.w[:, :2].tobytes()).hexdigest()
    # control path: acquisition, then silence
    cs = [ctrl] + ([ctrl4] if twin else [])
    vC, t_now = {}, 0
    for D in DS:
        for _ in range(D - t_now):
            for x in cs: x.step()
        t_now = D
        vC[D] = ctrl.valence(c).copy()
        if twin: same.append(bool(np.array_equal(ctrl.w, ctrl4.w) and np.array_equal(ctrl.tc, ctrl4.tc) and np.array_equal(ctrl.tr, ctrl4.tr)))
    # naive: one pairing on a fresh module
    n = build(arm, tau, K); vn0 = n.valence(c).copy(); pairing(n, c, comp, "forward"); v_naive = n.valence(c).copy()
    if twin:
        n4 = twin4(arm, K); pairing(n4, c, comp, "forward"); same.append(bool(np.array_equal(n.w, n4.w)))
    return dict(arm=arm, tau=tau, K=K, sign=sign, v0=v0, vn0=vn0, v_tr=v_tr, a_tr=a_tr, v_ext=v_ext, a_ext=a_ext, vD=vD, vrep=vrep,
                vC=vC, v_naive=v_naive, twin_same=all(same), n_checks=len(same), tr_steps=tr_steps, rep_tr=rep_tr,
                sig_ext01=sig_ext01, sig_end01=sig_end01)


# ------------------------------------------------------------------ statistics (reading R9)
_IDX = {}
def boot_median(x):
    x = np.asarray(x, float); n = len(x)
    if n not in _IDX: _IDX[n] = np.random.default_rng(SEEDS["boot"]).integers(0, n, (NBOOT, n))
    bs = np.median(x[_IDX[n]], 1); lo, hi = np.percentile(bs, [QLO, QHI])
    return float(np.median(x)), float(lo), float(hi)


def measures(s, a_scale):
    """per-run SR, RET, REACQ at every D; a_scale = A1's acquisition-site valence at the end of extinction (reading R8)"""
    ae, ve = np.abs(a_scale), np.abs(s["v_ext"])
    out = {}
    for D in DS:
        with np.errstate(divide="ignore", invalid="ignore"):
            SR = (np.abs(s["vD"][D]) - ve)/(ae - ve)
            RET = np.abs(s["vC"][D])/np.abs(s["vC"][0])
        REACQ = np.abs(s["vrep"][D]) - np.abs(s["vD"][D])
        F6 = abs(float(np.median(s["vrep"][D])) - float(np.median(s["v_ext"])))/abs(float(np.median(s["v_naive"])))
        out[D] = dict(SR=SR, RET=RET, REACQ=REACQ, F6=F6)
    return out


def fmt_iv(x, f="+.4f"):
    m, lo, hi = boot_median(x)
    return f"{m:{f}} [{lo:{f}}, {hi:{f}}] (runs min {np.min(x):{f}}, max {np.max(x):{f}})"


# ------------------------------------------------------------------ (I4) on H15 Run 2's recorded streams (reading R6)
def replay5(o, tau):
    import ph15
    n = len(o["good"]); m = MB5(n, parallel=True, gated=True, tau=(None, None, tau, tau), rng=np.random.default_rng(0), **ph11.MB)
    bad = 0
    for s in o["src"]:
        at = np.stack([(s == 0) | (s == 2), (s == 1) | (s == 2)], 1)
        code, rv = ph15.inputs(o["codes"], o["good"], at)
        bad += int((code.any(1) & (rv.sum(1) <= 0)).sum())
        m.step(code=code, reinf=rv)
    return ph15.valences(m, o["codes"], o["good"]), bad, m


def i4(tau, seeds=RUN2_EVAL, runs=None, steps=None):
    import ph15
    kw = {} if runs is None else dict(runs=runs, steps=steps)
    o = ph15.run_e1("intact", seeds, keep_src=True, **kw)
    r4 = ph15.replay(o, True)
    r5, bad, m = replay5(o, tau)
    pair_untouched = bool(np.all(m.w[:, 2:] == 1.0))
    ok = bool(np.array_equal(r4, o["val"][-1]) and np.array_equal(r5, o["val"][-1]) and bad == 0 and pair_untouched)
    return ok, dict(adopted=bool(np.array_equal(r4, o["val"][-1])), h12=bool(np.array_equal(r5, o["val"][-1])), bad=bad,
                    pair=pair_untouched, rows=len(o["good"]), steps=len(o["src"]))


# ------------------------------------------------------------------ seed scan (reading R13)
def seed_numbers():
    s = [SEEDS["A"], SEEDS["B"], SEEDS["boot"], 9911, 9921, 2129, 2243]
    derived = [9911 + 10000, 2129 + 10000, SEEDS["A"] + 10000, 9921 + 20000, 2243 + 20000, SEEDS["B"] + 20000]
    extra = [9911 + 20000, 2129 + 20000, SEEDS["A"] + 20000, SEEDS["A"] + 10000000, SEEDS["B"] + 20000000]
    return s + derived + extra


def pair_number():
    t = open(os.path.join(HERE, "ph30.py"), encoding="utf-8").read()
    return int(re.search(r"SEEDS = dict\(dev=.*?eval=\(\((\d+), (\d+)\)", t).group(2))       # Stage C Run 1's E1 evaluation agent seed


def seeds_unused():
    nums = seed_numbers(); pair_num = pair_number(); pair_file = os.path.join("experiments", "h20", "ph31_eval.txt")
    hits, nf = [], 0
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        rel = os.path.relpath(root, REPO).replace("\\", "/"); top = rel.split("/")[0]
        for f in files:
            if f in ("ph36.py", "ph36b.py", "master_plan.md") or (f.startswith(("ph36_", "ph36b_")) and f.endswith(".txt")) \
                    or (f.startswith("h12_") and f.endswith(".md")): continue
            if (os.path.basename(root) == "notes" and f.endswith(".md")) or top == "viewer": continue
            nf += 1; p = os.path.join(root, f); relp = os.path.relpath(p, REPO)
            ns = [x for x in nums if not (relp == pair_file and x == pair_num)]
            pat = re.compile(rb"(?<!\d)(" + "|".join(map(str, ns)).encode() + rb")(?!\d)")
            if pat.search(open(p, "rb").read()): hits.append(relp)
    return hits, nums, nf


# ------------------------------------------------------------------ header
def header(say=print):
    say(f"   ph36.py sha256 {sha()}; design {DESIGN}")
    say("   imported unchanged: " + "; ".join(f"{os.path.basename(m.__file__)} {sha(m.__file__)}" for m in (ph4, ph8, ph11)))
    pre = {k: sha(os.path.join(HERE, k + ".py"))[:8] == v for k, v in PREFIX.items()}
    dz = sha(DESIGN_FILE) == DESIGN.split("hash ")[1]
    say(f"   ph4.py, ph8.py, ph11.py sha256 prefixes equal to design v2's ({PREFIX}): {all(pre.values())}; experiments/h12/h12_design_v2.md sha256 equal to the design's hash: {dz}")
    say(f"   seeds: odour A {SEEDS['A']} (punishment sign), odour B {SEEDS['B']} (reward sign), bootstrap {SEEDS['boot']} ({NBOOT} resamples, 95 percent);"
        f" H11's own seeds (rng 0; codes 11, 12, 101) for the reproduction; H15 Run 2's evaluation seeds {RUN2_EVAL} for (I4) only (not in the scan);"
        f" the pair of decision:seed-scan-exclusion-ph31-eval excluded by reference; {R} runs; K sets {list(KSET)}; tau grid {TAUS}; D {DS}")
    return all(pre.values()) and dz


def readings(say=print):
    doc = __doc__; i = doc.index("Readings where"); j = doc.index("Nothing changes after the table.")
    for line in doc[i:j].rstrip().splitlines(): say("   " + line)


def pool(): return mp.get_context("fork").Pool(NPROC)


# ------------------------------------------------------------------ the bench (design section 4)
def bench(say=print):
    say(f"== H12 Stage 1, the module bench (design v2 FINAL section 4). design {DESIGN} ==")
    hok = header(say); readings(say)
    hits, nums, nf = seeds_unused()
    say(f"   seed scan (R13): {len(nums)} numbers, {nf} files scanned, files containing any: {hits if hits else 'none'}")
    if not hok or hits:
        say("   STOP: a hash check or the seed scan failed; nothing is run"); return
    # ---- (r) reproduction first
    say("\n== (r) H11 reproduced: python3 ph8.py (H11's main, its own seeds) against experiments/h11/ph8_h11.txt ==")
    out = subprocess.run([sys.executable, os.path.join(HERE, "ph8.py")], cwd=HERE, capture_output=True, text=True).stdout
    ref = open(H11_TXT, encoding="utf-8").read()
    ol, rl = out.rstrip("\n").split("\n"), ref.rstrip("\n").split("\n")
    diff = [i for i in range(max(len(ol), len(rl))) if i >= len(ol) or i >= len(rl) or ol[i] != rl[i]]
    r_ok = not diff
    say(f"   lines: reproduced {len(ol)}, recorded {len(rl)}; mismatching lines: {len(diff)} -> {'MATCH' if r_ok else 'MISMATCH'}")
    for line in ol: say("   | " + line)
    if not r_ok:
        for i in diff[:10]: say(f"   line {i + 1}: reproduced {ol[i] if i < len(ol) else '<none>'!r} recorded {rl[i] if i < len(rl) else '<none>'!r}")
        say("   STOP: (r) failed (an implementation error; fixed before anything is read)"); return
    # ---- (i) identities on H11's protocols (I1), (I2)
    say("\n== (i) identities on H11's protocols: MB5 (tau None) == ph8.MB4, F1, F2, F3, F6 returned values (reading R4) ==")
    with pool() as p: prot = p.map(protocols, [("MB5", False), ("MB4", False), ("MB5", True), ("MB4", True)])
    i1 = prot[0] == prot[1]; i2 = prot[2] == prot[3]
    say(f"   (I1) MB5(parallel False, tau None) == MB4(parallel False, gated True): {i1}")
    say(f"   (I2) MB5(parallel True, tau None) == MB4(parallel True, gated True) (H11 full): {i2}")
    # ---- (b) F1 and F2, the tau rule
    say("\n== (b) F1 and F2 at K 500 for every arm and tau (ph8.py:112-155 unchanged; bounds ph8.py:180-182) ==")
    with pool() as p: rows = p.map(f12, configs())
    for r in rows: say(f12_line(r))
    tstar = tau_rule(rows)
    fails = [(r["tau"], [k for k, v in r["clauses"].items() if not v]) for r in rows if r["arm"] == "P" and not r["f1"]]
    say(f"\n   tau rule (design 4.3): tau_ext* = the smallest tau in {TAUS} at which P passes every clause of F1 and F2 at K 500 -> "
        f"{tstar if tstar else 'NONE'}; P's failing clauses by tau: {fails if fails else 'none'}")
    if tstar is None:
        say("   STOP (s1): no candidate; H12 not shown at the module level; Stage 2 not run"); return
    say(f"   tau_ext* = {tstar}, fixed here, before any retention schedule has run (reading R11)")
    # ---- (s) retention schedules
    say("\n== (s) retention schedules, every arm and tau, both signs, K 500 and K 200 (reading R7) ==")
    jobs = [(a, t, K, sg) for K in KSET for sg in ("pun", "rew") for (a, t) in configs()]
    with pool() as p: res = p.map(schedule, jobs)
    S = {(r["arm"], r["tau"], r["K"], r["sign"]): r for r in res}
    base0 = all(np.all(r["v0"] == 0.0) and np.all(r["vn0"] == 0.0) for r in res)
    tw = all(S[(a, None, K, sg)]["twin_same"] for a in ("A0", "A1") for K in KSET for sg in ("pun", "rew"))
    ntw = sum(S[(a, None, K, sg)]["n_checks"] for a in ("A0", "A1") for K in KSET for sg in ("pun", "rew"))
    # (I2'): A1 vs A0 on every traced step and every read point
    mx = 0.0; nstep = 0
    for K in KSET:
        for sg in ("pun", "rew"):
            a0, a1 = S[("A0", None, K, sg)], S[("A1", None, K, sg)]
            for x, y in zip(a0["tr_steps"], a1["tr_steps"]): mx = max(mx, float(np.abs(x - y).max())); nstep += 1
            for D in DS:
                for x, y in zip(a0["rep_tr"][D], a1["rep_tr"][D]): mx = max(mx, float(np.abs(x - y).max())); nstep += 1
                mx = max(mx, float(np.abs(a0["vD"][D] - a1["vD"][D]).max()), float(np.abs(a0["vC"][D] - a1["vC"][D]).max()),
                         float(np.abs(a0["vrep"][D] - a1["vrep"][D]).max()))
            mx = max(mx, float(np.abs(a0["v_naive"] - a1["v_naive"]).max()))
    i2p = mx <= 1e-12
    # a_P == a_A1 (reading R8)
    ap = all(np.array_equal(S[("P", t, K, sg)]["a_ext"], S[("A1", None, K, sg)]["a_ext"]) and
             S[("P", t, K, sg)]["sig_ext01"] == S[("A1", None, K, sg)]["sig_ext01"] and S[("P", t, K, sg)]["sig_end01"] == S[("A1", None, K, sg)]["sig_end01"]
             for t in TAUS for K in KSET for sg in ("pun", "rew"))
    say(f"   baseline valence at w0 exactly 0 in every schedule and naive module: {base0}")
    say(f"   (I1), (I2) on the schedules: A0 and A1 == their ph8.MB4 twins, w, tc, tr bitwise at every read point: {tw} ({ntw} comparisons)")
    say(f"   (I2') A1 vs A0 behavioural valence on every traced step and read point ({nstep} traced steps x 200 runs, 2 K, 2 signs): max |difference| {mx:.3e} -> {i2p} (tolerance 1e-12, reading R5)")
    say(f"   P's acquisition pair == A1's bitwise (w[:, 0:2] after extinction and at D 10000; a at the end of extinction), every tau, K, sign: {ap}")
    # ---- (I4)
    say(f"\n== (I4) H15 Run 2's recorded streams (ph15.run_e1('intact', {RUN2_EVAL}, keep_src=True)) replayed into the adopted module and into P at tau_ext* {tstar} ==")
    i4ok, d4 = i4(tstar)
    say(f"   adopted replay == the run's end values bitwise: {d4['adopted']}; P replay == the run's end values bitwise: {d4['h12']}; "
        f"(step, row) with a code and no reinforcement: {d4['bad']}; P's extinction pair untouched (every weight 1.0): {d4['pair']}; "
        f"{d4['rows']} rows x {d4['steps']} steps -> (I4) {i4ok}")
    B1 = r_ok and i1 and i2 and tw and i2p and ap and base0 and i4ok
    # ---- tables
    say("\n== the retention measures: medians over 200 runs, 95 percent bootstrap interval of the median, per-run min and max (reading R9) ==")
    M = {}
    for (a, t, K, sg), s in S.items(): M[(a, t, K, sg)] = measures(s, S[("A1", None, K, sg)]["a_ext"])
    for K in KSET:
        for sg in ("pun", "rew"):
            a1 = S[("A1", None, K, sg)]
            say(f"\n   [{K}, {'punishment (compartment 0), odour A' if sg == 'pun' else 'reward (compartment 1), odour B'}] A1: trained {np.median(a1['v_tr']):+.4f},"
                f" extinguished {np.median(a1['v_ext']):+.4f}, acquisition site a {np.median(a1['a_ext']):+.4f}, naive one pairing {np.median(a1['v_naive']):+.4f}")
            for (a, t) in configs():
                s = S[(a, t, K, sg)]; m = M[(a, t, K, sg)]
                say(f"   {label(a, t):16s} trained {np.median(s['v_tr']):+.4f}  extinguished {np.median(s['v_ext']):+.4f}  control trained {np.median(s['vC'][0]):+.4f}")
                for D in DS:
                    ex = f"  exact 1-(1-1/tau)^D {1 - (1 - 1/t)**D:.4f}" if a == "P" else ""
                    say(f"      D {D:5d}: SR {fmt_iv(m[D]['SR'])}{ex}")
                    say(f"               RET {fmt_iv(m[D]['RET'])}  REACQ {np.median(m[D]['REACQ']):+.4f}  F6 {m[D]['F6']:.2f}x  v(D) {np.median(s['vD'][D]):+.4f}  v_rep {np.median(s['vrep'][D]):+.4f}")
    # ---- criteria
    say(f"\n== Stage 1 criteria (design 4.4) at tau_ext* = {tstar} ==")
    rP = [r for r in rows if r["arm"] == "P" and r["tau"] == tstar][0]
    B2 = rP["f1"] and rP["f2"]
    say(f"   B1 reproduction (r) and identities (i): (r) {r_ok}, (I1) {i1}, (I2) {i2}, schedules' twins {tw}, (I2') {i2p}, acquisition pair {ap}, baseline {base0}, (I4) {i4ok} -> {'PASS' if B1 else 'FAIL'}")
    say(f"   B2 P at tau_ext*: F1 {rP['f1']} (every clause), F2 {rP['f2']} -> {'PASS' if B2 else 'FAIL'}")
    b3, b4 = {}, {}
    for sg in ("pun", "rew"):
        m = M[("P", tstar, "K200", sg)][D_REG]
        sr = boot_median(m["SR"]); rt = boot_median(m["RET"])
        b3[sg] = sr[1] >= 0.20; b4[sg] = rt[1] >= 0.99
        say(f"   {'punishment' if sg == 'pun' else 'reward    '} K 200, D {D_REG}: SR {sr[0]:.4f} [{sr[1]:.4f}, {sr[2]:.4f}] (exact {1 - (1 - 1/tstar)**D_REG:.4f}; runs {np.min(m['SR']):.6f}..{np.max(m['SR']):.6f})"
            f" lower >= 0.20 -> {'PASS' if b3[sg] else 'FAIL'}; RET {rt[0]:.4f} [{rt[1]:.4f}, {rt[2]:.4f}] (runs {np.min(m['RET']):.4f}..{np.max(m['RET']):.4f}) lower >= 0.99 -> {'PASS' if b4[sg] else 'FAIL'}")
    B3, B4 = all(b3.values()), all(b4.values())
    say(f"   B3 (SR, both signs) -> {'PASS' if B3 else 'FAIL'}; B4 (RET, both signs) -> {'PASS' if B4 else 'FAIL'}")
    say(f"   B5 (reported, not a bar) at tau {tstar}, K 200, D {D_REG}:")
    for a in ("S1", "S2"):
        for sg in ("pun", "rew"):
            m = M[(a, tstar, "K200", sg)][D_REG]
            say(f"      {a} {'punishment' if sg == 'pun' else 'reward    '}: SR {np.median(m['SR']):+.4f}, RET {np.median(m['RET']):.4f}")
    s1p = [np.median(M[("S1", tstar, "K200", sg)][D_REG]["SR"]) <= 0 for sg in ("pun", "rew")]
    s2a = np.median(M[("S2", tstar, "K200", "pun")][D_REG]["SR"]) > 0 and not np.median(M[("S2", tstar, "K200", "rew")][D_REG]["SR"]) > 0
    s2r = np.median(M[("S2", tstar, "K200", "rew")][D_REG]["RET"]) < 1
    say(f"      as predicted: S1 SR <= 0 both signs {all(s1p)}; S2 SR > 0 for the aversive sign only {bool(s2a)}; S2 RET < 1 for the appetitive sign {bool(s2r)}")
    s2stop = not (B3 and B4)
    stage1 = B1 and B2 and B3 and B4
    say(f"\n   (s1) no candidate: not fired (tau_ext* {tstar}); (s2) B3 or B4 failing: {'FIRED' if s2stop else 'not fired'}")
    say(f"   STAGE 1: {'PASS (B1-B4)' if stage1 else 'NOT PASSED'}"
        f"{'' if stage1 else ' -> Stage 2 not run'}; tau_ext* = {tstar}")


def protocols(job):
    """(I1)/(I2) on H11's protocols (reading R4)"""
    kind, par = job
    make = (lambda: build("A1" if par else "A0", None, "K500")) if kind == "MB5" else (lambda: ph8.mk(par, True))
    b = ph8.f1_battery(make); f2 = ph8.f2_sustained(make); f3 = ph8.f3_trace(make); f6 = ph8.f6_savings(make)
    return repr((b, f2, f3, f6))


# ------------------------------------------------------------------ demo self-checks (smoke seeds only; no registered seed)
def demo(say=print):
    say(f"== H12 Stage 1 demo self-checks. design {DESIGN} ==")
    say("   smoke runs use the unregistered code seed 5 and ph15's own smoke seeds (3, 4); no registered seed is used and no number here is read for any criterion")
    hok = header(say)
    assert hok, "a hash check failed"; say("ok 1  ph4.py, ph8.py, ph11.py prefixes and the design file hash equal the record")
    hits, nums, nf = seeds_unused()
    assert not hits, f"seed scan: {hits}"; say(f"ok 2  seed scan clean: {len(nums)} numbers, {nf} files, no hit (R13)")
    kw = dict(ph8.KW); n = 40
    for par in (False, True):
        a = MB5(n, parallel=par, gated=True, rng=np.random.default_rng(0), **kw); b = MB4(n, parallel=par, gated=True, rng=np.random.default_rng(0), **kw)
        c = a.odour(5)
        for m in (a, b):
            for _ in range(6): pairing(m, c, 0, "forward")
            for _ in range(8): pairing(m, c, None, "forward")
            for _ in range(300): m.step()
            pairing(m, c, 1, "reverse")
        assert np.array_equal(a.w, b.w) and np.array_equal(a.tc, b.tc) and np.array_equal(a.tr, b.tr)
    say("ok 3  MB5 with the site inert (every tau None) == ph8.MB4 bitwise (w, tc, tr), parallel False and True, after pairing, extinction, silence, a reverse pairing")
    m = MB5(n, parallel=True, gated=True, tau=(None, None, 2000, 2000), rng=np.random.default_rng(0), **kw)
    m.w = np.random.default_rng(7).uniform(0.2, 1.8, m.w.shape); w_before = m.w.copy(); m.step()
    exp = w_before.copy(); exp[:, 2:] = w_before[:, 2:] + (1.0 - w_before[:, 2:])/2000
    assert np.array_equal(m.w, exp)
    say("ok 4  the relaxation line: one silent step moves compartments 2, 3 by exactly (w0 - w)/tau and leaves 0, 1 unchanged")
    for tau, D in ((2000, 300), (5000, 1000)):
        p = MB5(n, parallel=True, gated=True, tau=(None, None, tau, tau), rng=np.random.default_rng(0), **kw)
        q = MB5(n, parallel=True, gated=True, rng=np.random.default_rng(0), **kw)
        c = p.odour(5)
        for x in (p, q):
            for _ in range(10): pairing(x, c, 0, "forward")
            for _ in range(20): pairing(x, c, None, "forward")
        ve, ae = np.abs(p.valence(c)), np.abs(q.acq_valence(c))
        assert np.array_equal(p.acq_valence(c), q.acq_valence(c))
        for _ in range(D): p.step()
        sr = (np.abs(p.valence(c)) - ve)/(ae - ve)
        assert np.allclose(sr, 1 - (1 - 1/tau)**D, atol=1e-9, rtol=0), (sr.min(), sr.max(), 1 - (1 - 1/tau)**D)
    say("ok 5  P in silence recovers SR = 1 - (1 - 1/tau)^D (tau 2000 D 300, tau 5000 D 1000; 1e-9), and its acquisition site equals A1's bitwise")
    g = MB5(n, parallel=True, gated=True, tau=(None, None, 2000, 2000), rng=np.random.default_rng(0), **kw); c = g.odour(5)
    rv = np.zeros((n, 4)); rv[:, 0] = 1.0
    for _ in range(100): g.step(code=c, reinf=rv.copy())
    assert np.all(g.w[:, 2:] == 1.0)
    say("ok 6  under sustained reinforcement the gate writes nothing and the decaying pair stays exactly at w0 (F2's mechanism)")
    a0 = MB5(n, parallel=False, gated=True, rng=np.random.default_rng(0), **kw); a1 = MB5(n, parallel=True, gated=True, rng=np.random.default_rng(0), **kw)
    c = a0.odour(5); mx = 0.0; bit = True
    for x in (a0, a1): x.trace_code, x.trace = c, []
    for _ in range(10):
        pairing(a0, c, 0); pairing(a1, c, 0)
    for _ in range(20):
        pairing(a0, c, None); pairing(a1, c, None)
    for x, y in zip(a0.trace, a1.trace): mx = max(mx, float(np.abs(x - y).max())); bit &= np.array_equal(x, y)
    assert mx <= 1e-12
    say(f"ok 7  (I2') instrument: single-site and parallel layouts' valences on every step, max |difference| {mx:.3e} (bitwise equal: {bool(bit)}; reading R5)")
    # parallel == sequential (reading R12)
    job = ("P", 2000, "K200", "rew", 5)
    seq = schedule(job)
    with pool() as pl: par = pl.map(schedule, [job])[0]
    assert all(np.array_equal(seq["vD"][D], par["vD"][D]) and np.array_equal(seq["vC"][D], par["vC"][D]) and np.array_equal(seq["vrep"][D], par["vrep"][D]) for D in DS)
    say("ok 8  a schedule run in a worker process == the same schedule run sequentially, bitwise (reading R12; smoke code seed 5)")
    ok, d = i4(2000, seeds=(3, 4), runs=40, steps=1200)
    assert ok, d
    say(f"ok 9  (I4) instrument on ph15's smoke seeds (3, 4), 40 rows x 1200 steps: adopted and P replays == the run's end values bitwise, code-without-reinforcement steps {d['bad']}, pair untouched {d['pair']}")
    say("ok    all demo self-checks passed")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "demo"
    if mode == "demo": demo()
    elif mode == "bench": bench()
    else: sys.exit("usage: python ph36.py demo | bench")
