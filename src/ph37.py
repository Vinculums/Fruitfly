#!/usr/bin/env python3
"""H18 Stage A: a measurement-only diagnosis of the K5(b) rows.

Usage (ONE process at a time; one arm per process):
    python src/ph37.py demo | r0 | arm <exact|none|ring|integrate|ring_sep|ring_made> | bench | read

Registered by experiments/h18/h18_design_v2.md (v2 FINAL, decision:h18-open). Nothing here changes
the ring, the rule or any adopted file: ph12b, ph12, ph10, ph11, ph9, ph3 and ph12c are imported
unchanged and their sha256 prefixes are checked against the design header before anything runs.
Seeds: ph12b's own K5(b) seeds, read from ph12b.SEEDS['eval'] + 2 (ph12b.py:198, :200); the
measurement streams are numpy SeedSequence(agent seed).spawn(3) children 0, 1, 2 (design section 9).
No new integer seed.

Choices where the registered text needed a reading in code (fixed before any output existed;
printed again in the output):
  C1  cue-off block: a maximal run of consecutive cue-off steps of one agent; k = 1.. within it.
  C2  r_t (7 (D)) on every cue-off step t >= 1: angdiff(est_t, est_(t-1)) - turn_(t-1), the signed
      change of est over one step (folded within that step only) minus the rotation fed at t
      (ph12.py:106 feeds last_turn). Sums are sums of such signed per-step terms (H14 rule,
      master_plan.md:2037-2039).
  C3  loss events whose since reaches 143 without any whiff before (t_L < 0) have no last whiff;
      they are counted and excluded from the event readings.
  C4  per-block autocorrelation: Pearson r of (e_k, e_(k+L)) within one block, for blocks with at
      least 3 pairs and non-zero variance on both sides; F2 reads the median over blocks.
  C5  'the bench gain' at a rotation v (F-i): the median over the 400 bench rings of
      angdiff(pos after, pos before) / v; min and max printed beside it.
  C6  F-ii ratio: the median over cue-off blocks of length >= 50 of amp(k 50) / amp(k 1); the
      ratio of the medians is printed beside it.
  C7  F-iii 'the first cue-on step after t_L': literally the first step t > t_L with the cue on;
      the first cue RETURN (cue on at t, off at t - 1) is printed beside it, reported only.
  C8  F-vi: the cue-off blocks inside an event's windows are the blocks overlapping
      [t_L - 50, t_L + 142]; the half-width is W0 + SLOPE * max(along, 0) at t_L's position;
      the median is over all (event, block) pairs of the group.
  C9  exposure 'distance at the end': the position after the last move (w.pos at the end).
"""
import sys, os, io, re, json, time, hashlib, platform, contextlib, runpy
sys.stdout.reconfigure(newline="\n")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
OUT = os.path.join(ROOT, "experiments", "h18"); ARR = os.path.join(OUT, "arrays"); LOGS = os.path.join(OUT, "logs")
RECORD = os.path.join(ROOT, "experiments", "h16", "ph12b_h16r2.txt")
DESIGN = os.path.join(OUT, "h18_design_v2.md")
REGISTERED = dict(ph12b="ec6b1896", ph12="e1035e09", ph10="de93f177", ph11="e80f40bd", ph9="7699b4e6",
                  ph3="0b43d6f3", ph12c="bacf065f")

import ph12b, ph12, ph10, ph11, ph9, ph3, ph12c
from ph9 import angdiff, SPEED, W0, SLOPE, STEPS
from ph12 import R, BLOCKS, LOST, World1
from ph12b import World3, Nav3
from ph12c import Nav4
from ph10 import RingExact
from ph11 import RING, WIND_CUE
from ph3 import cue

W_SEED, A_SEED = ph12b.SEEDS["eval"][0] + 2, ph12b.SEEDS["eval"][1] + 2
T = BLOCKS*STEPS
ARMS = {"exact": ("exact", "always"), "none": ("none", "blocks"), "ring": ("ring", "blocks"),
        "integrate": ("integrate", "blocks"), "ring_sep": ("ring", "blocks"), "ring_made": ("ring_made", "blocks")}
RECORDED = ("exact", "none", "ring", "integrate")


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def header(stage):
    print(f"== H18 Stage A, src/ph37.py, stage `{stage}` ==")
    print(f"python {platform.python_version()}  numpy {np.__version__}  platform {platform.platform()}")
    print(f"src/ph37.py sha256 {sha(os.path.abspath(__file__))}")
    print(f"design experiments/h18/h18_design_v2.md sha256 {sha(DESIGN)}")
    bad = []
    for name, m in sorted(sys.modules.items()):
        f = getattr(m, "__file__", None)
        if not f or os.path.dirname(os.path.abspath(f)) != HERE or name == "__main__": continue
        h = sha(f); reg = REGISTERED.get(name)
        tag = "" if reg is None else (f"  registered {reg}: {'ok' if h.startswith(reg) else 'MISMATCH'}")
        print(f"  imported src/{name}.py sha256 {h}{tag}")
        if reg and not h.startswith(reg): bad.append(name)
    for name in REGISTERED:
        if name not in sys.modules: bad.append(name + " (not imported)")
    if bad:
        print(f"STOP: imported source does not match the design header: {bad}"); sys.exit(2)
    print(f"seeds: world {W_SEED}, agent {A_SEED} (ph12b.SEEDS['eval'] + 2); streams SeedSequence({A_SEED}).spawn(3)")
    print(f"BLAS threads: OPENBLAS {os.environ.get('OPENBLAS_NUM_THREADS')} OMP {os.environ.get('OMP_NUM_THREADS')}"
          f" MKL {os.environ.get('MKL_NUM_THREADS')}")


def run_main(path, argv):
    """run a project script's __main__ unchanged; its prints go to the current stdout"""
    old = sys.argv; sys.argv = argv
    try:
        runpy.run_path(path, run_name="__main__")
        code = 0
    except SystemExit as ex:
        code = ex.code or 0
    finally:
        sys.argv = old
    return code


# ------------------------------------------------------------------ stage demo
def stage_demo():
    header("demo")
    for script in ("ph12b.py", "ph12c.py"):
        print(f"\n-- python src/{script} demo (its own asserts) --")
        code = run_main(os.path.join(HERE, script), [script, "demo"])
        print(f"   exit code {code}")
        if code != 0: print("STOP: demo failed"); sys.exit(1)
    # the harness's own asserts, on a short known answer: the shadow ring leaves `integrate` unchanged
    # and the harness equals run2 (checked in full on the task rows by stage arm)
    print("\n-- harness asserts --")
    k = np.random.SeedSequence(A_SEED).spawn(3)
    assert [c.spawn_key for c in k] == [(0,), (1,), (2,)]
    print("ok  SeedSequence children are spawn keys (0,), (1,), (2,) of the agent seed")
    print("ok  demo stage complete")


# ------------------------------------------------------------------ stage r0
def stage_r0():
    header("r0")
    out = os.path.join(OUT, "r0_ph12b_eval.txt")
    t0 = time.time()
    with open(out, "w", newline="\n") as f, contextlib.redirect_stdout(f):
        code = run_main(os.path.join(HERE, "ph12b.py"), ["ph12b.py", "eval"])
    print(f"R0: `python src/ph12b.py eval` run unchanged (runpy, stdout to experiments/h18/r0_ph12b_eval.txt,"
          f" LF); exit {code}; {time.time() - t0:.0f} s")
    print(f"   r0 output sha256 {sha(out)}; record experiments/h16/ph12b_h16r2.txt sha256 {sha(RECORD)}")
    r0_diff(out)


NUM = re.compile(r"[-+]?\d+(?:\.\d+)?%?|nan")


def r0_diff(out):
    a = open(RECORD, encoding="utf-8").read().split("\n"); b = open(out, encoding="utf-8").read().split("\n")
    print(f"   lines: record {len(a)}, R0 {len(b)} (split on LF; a trailing empty string counts once)")
    diff = [(i + 1, x, y) for i, (x, y) in enumerate(zip(a, b)) if x != y]
    if len(a) != len(b): diff.append((min(len(a), len(b)) + 1, "<length>", "<length>"))
    intdiff = False
    for i, x, y in diff:
        nx, ny = NUM.findall(x), NUM.findall(y)
        skel = NUM.sub("#", x) == NUM.sub("#", y) and len(nx) == len(ny)
        ints = [(p, q) for p, q in zip(nx, ny) if "." not in p and "." not in q and p != q]
        kind = "float formatting only" if skel and not ints else "INTEGER OR TEXT DIFFERENCE"
        if kind != "float formatting only": intdiff = True
        print(f"   line {i} differs ({kind}):\n     record: {x}\n     R0    : {y}")
    if not diff: print("   R0 RESULT: identical, every line (MATCH)")
    elif intdiff: print("   R0 RESULT: an integer count or text differs -> STOP"); sys.exit(3)
    else: print(f"   R0 RESULT: {len(diff)} lines differ in float formatting only: disclosed, not repaired")


# ------------------------------------------------------------------ stage arm (the harness)
def harness(arm):
    """ph12b.run2 (ph12b.py:73-102), line for line, plus reads. No random draw is added to a recorded arm:
    ring_sep's ring and the shadow ring draw from their own SeedSequence children."""
    head, wind = ARMS[arm]
    kids = np.random.SeedSequence(A_SEED).spawn(3)
    w = World3(R, np.random.default_rng(W_SEED), "cone", False, wind)
    a = (Nav4 if head == "ring_made" else Nav3)(R, np.random.default_rng(A_SEED), "return", head)
    if arm == "ring_sep": a.ring.rng = np.random.default_rng(kids[0])
    sh = RingExact(R, n=16, noise=0.3, rng=np.random.default_rng(kids[1]), **RING) if arm == "integrate" else None
    f32 = lambda *s: np.zeros(s, np.float32)
    rec = dict(est=f32(T, R), head=f32(T, R), pos=f32(T, R, 2), turn=f32(T, R),
               hit=np.zeros((T, R), np.int8), won=np.zeros((T, R), np.int8), clock=np.zeros((T, R), np.int16))
    if a.ring is not None: rec["amp"] = f32(T, R)
    if sh is not None: rec["sh_est"] = f32(T, R); rec["sh_amp"] = f32(T, R)
    z = lambda: np.zeros((BLOCKS, R))
    o = dict(score=z(), whiff=z(), wall=z(), contact=z(), events=0, gaps=[], wallfree=[],
             err=np.zeros(2), err_off=np.zeros(2), abs_off=0.0, mismatch=np.zeros(3))
    touched = np.zeros(R, bool); nocue = 0; emax = 0.0
    for t in range(T):
        b = t // STEPS
        hit = w.sense(); won = w.wind_on()
        back = hit & (a.since > LOST)
        if back.any():
            o["gaps"].append(a.since[back].copy()); o["wallfree"].append(~touched[back])
        touched &= ~hit
        if sh is not None:                              # as ph12.py:106-108, on this arm's own last_turn; read only
            sh.step(v=a.last_turn)
            if won.any(): sh.step(x=cue(R, 16, w.head, WIND_CUE, width=1.2)*won[:, None])
            rec["sh_est"][t] = sh.pos(); rec["sh_amp"][t] = sh.amp()
        rec["head"][t] = w.head; rec["pos"][t] = w.pos; rec["hit"][t] = hit; rec["won"][t] = won
        nocue += int(not won.any())
        turn = a.act(w, hit, won)
        o["events"] += int((a.since == LOST + 1).sum())
        if head != "exact":
            e = np.abs(angdiff(a.est, w.head)); bad = e > 45.0
            o["err"] += (bad.sum(), R); o["err_off"] += (bad[~won].sum(), (~won).sum())
            o["abs_off"] += e[~won].sum(); emax = max(emax, float(e.max()))
        rec["est"][t] = a.est; rec["clock"][t] = a.clock; rec["turn"][t] = turn
        if a.ring is not None: rec["amp"][t] = a.ring.amp()
        w.move(turn); a.bump(w.bumped); touched |= w.bumped
        differ = np.abs(angdiff(w.rot, turn)) > 1e-6
        o["mismatch"] += (differ.sum(), (differ & w.bumped).sum(), R)
        o["score"][b] += w.at_source(); o["whiff"][b] += hit; o["contact"][b] += w.bumped
    o["lost_end"] = a.since > LOST
    o["gaps"] = np.concatenate(o["gaps"]) if o["gaps"] else np.zeros(0)
    o["wallfree"] = np.concatenate(o["wallfree"]) if o["wallfree"] else np.zeros(0, bool)
    return o, rec, w, nocue, emax


OKEYS = ("score", "whiff", "wall", "contact", "events", "gaps", "wallfree", "err", "err_off", "abs_off", "mismatch", "lost_end")


def stage_arm(arm):
    header(f"arm {arm}")
    head, wind = ARMS[arm]
    print(f"arm `{arm}`: head {head}, wind {wind}, open plane (walls False), `return`, {R} agents x {T} steps")
    t0 = time.time()
    o, rec, w, nocue, emax = harness(arm)
    th = time.time() - t0
    meta = dict(arm=arm, head=head, wind=wind, seconds_harness=round(th, 1), nocue_steps=nocue,
                cueoff_agent_steps=int(o["err_off"][1]), max_abs_e_in_run=emax,
                mismatch=[int(x) for x in o["mismatch"]], events=int(o["events"]))
    print(f"   harness {th:.0f} s; agent-steps with no cued agent {nocue}; cue-off agent-steps {int(o['err_off'][1])};"
          f" mismatch (differ, at contacts, n) {meta['mismatch']}; max abs e in run {emax:.6g}")
    if arm in RECORDED:
        t1 = time.time()
        o2 = ph12b.run2("return", head=head, walls=False, wind=wind, seeds=(W_SEED, A_SEED))
        eq = {k: bool(np.array_equal(np.asarray(o[k]), np.asarray(o2[k]))) for k in OKEYS}
        meta["bitwise_vs_run2"] = eq; meta["seconds_run2"] = round(time.time() - t1, 1)
        print(f"   run2 {meta['seconds_run2']:.0f} s; harness == ph12b.run2 bitwise per key: {eq}")
        print(f"   R1 arrays bitwise: {'ALL EQUAL' if all(eq.values()) else 'NOT EQUAL -> STOP'}")
        if not all(eq.values()): json.dump(meta, open(os.path.join(ARR, f"{arm}_meta.json"), "w"), indent=1); sys.exit(4)
    os.makedirs(ARR, exist_ok=True)
    path = os.path.join(ARR, f"{arm}.npz")
    np.savez_compressed(path, **rec, src=w.src, pos_end=w.pos,
                        **{f"o_{k}": np.asarray(o[k]) for k in OKEYS})
    meta["npz_sha256"] = sha(path); meta["npz_bytes"] = os.path.getsize(path)
    json.dump(meta, open(os.path.join(ARR, f"{arm}_meta.json"), "w", newline="\n"), indent=1)
    print(f"   wrote experiments/h18/arrays/{arm}.npz ({meta['npz_bytes']} bytes, sha256 {meta['npz_sha256']});"
          f" total {time.time() - t0:.0f} s")


# ------------------------------------------------------------------ stage bench
def form(n, heads, noise, rng):
    g = RingExact(n, n=16, noise=noise, rng=rng, **RING)
    for _ in range(50):                                  # wired as ph12.py:106-108, every ring cued
        g.step(v=0.0); g.step(x=cue(n, 16, heads, WIND_CUE, width=1.2))
    return g


def stage_bench():
    header("bench")
    print("H14 standing rule (master_plan.md:2037-2039): an angular gain is measured on per-step displacement"
          " accumulated without folding. Every change of pos below is angdiff over ONE step; sums are sums of those.")
    B = {}
    n = 400; heads = 360.0*np.arange(n)/n
    print(f"\n(b0) noise 0, {n} rings, bump formed by the cue at 6.0 for 50 agent-steps at headings 0..359.1"
          " (spread over the wedge grid); cue off; one rotation v; then v = 0 for 49 agent-steps."
          " noise 0: the generator's draws are multiplied by zero (ph10.py:73).")
    print("   v      zero step  gain median  [min, max]        drift after 49 steps median |.| [max |.|]   amp end / amp formed")
    B["b0"] = {}
    for zero in (True, False):
        for v in (5, 10, 20, 30, 40, 50, 60, -5, -10, -20, -30, -40, -50, -60, 0):
            g = form(n, heads, 0.0, None); a0 = g.amp().copy(); p0 = g.pos()
            g.step(v=float(v))
            if zero: g.step(x=np.zeros((n, 16)))
            p1 = g.pos(); d = angdiff(p1, p0); cum = d.copy(); p = p1
            for _ in range(49):
                g.step(v=0.0)
                if zero: g.step(x=np.zeros((n, 16)))
                q = g.pos(); cum += angdiff(q, p); p = q
            drift = cum - v; ar = g.amp()/a0
            gain = d/v if v else np.full(n, np.nan)
            key = f"{'two' if zero else 'one'}_{v}"
            B["b0"][key] = dict(gain_median=float(np.median(gain)) if v else None,
                                gain_min=float(gain.min()) if v else None, gain_max=float(gain.max()) if v else None,
                                drift_med_abs=float(np.median(np.abs(drift))), drift_max_abs=float(np.abs(drift).max()),
                                amp_ratio_median=float(np.median(ar)))
            gs = f"{np.median(gain):8.4f}  [{gain.min():7.4f}, {gain.max():7.4f}]" if v else "     n/a  (v = 0)          "
            print(f"   {v:4d}   {'two' if zero else 'one':9s}  {gs}   {np.median(np.abs(drift)):9.4f} [{np.abs(drift).max():8.4f}]"
                  f"                     {np.median(ar):.4f}")
    # replay of recorded rotation sequences
    Z = np.load(os.path.join(ARR, "integrate.npz"))
    won, turn, hd = Z["won"], Z["turn"].astype(float), Z["head"].astype(float)
    t0s = []
    for r in range(R):
        off = np.concatenate([[0], (won[:, r] == 0).astype(int), [0]]); dd = np.diff(off)
        s, e = np.where(dd == 1)[0], np.where(dd == -1)[0]
        full = [a for a, b in zip(s, e) if b - a == 50 and a >= 1]
        t0s.append(full[0] if full else -1)
    t0s = np.array(t0s); ok = t0s >= 1
    rows = np.where(ok)[0]; m = len(rows); ts = t0s[ok]
    g = form(m, hd[ts - 1, rows], 0.0, None)
    p = g.pos(); cum = angdiff(p, hd[ts - 1, rows])
    for k in range(50):
        v = turn[ts + k - 1, rows]
        g.step(v=v); g.step(x=np.zeros((m, 16)))
        q = g.pos(); cum += angdiff(q, p) - v; p = q
    B["replay"] = dict(n=int(m), med_abs=float(np.median(np.abs(cum))), p90_abs=float(np.percentile(np.abs(cum), 90)),
                       max_abs=float(np.abs(cum).max()), mean_signed=float(cum.mean()))
    print(f"\n   replay at noise 0: the first full 50-step cue-off block of each agent of the `integrate` arm"
          f" ({m} of {R} agents have one), formed at the heading of its last cued step, fed that block's recorded"
          f" turns with the zero step; end-of-block error (unfolded: initial offset + sum of per-step changes - sum of v):"
          f" median |.| {B['replay']['med_abs']:.4f}, p90 {B['replay']['p90_abs']:.4f}, max {B['replay']['max_abs']:.4f},"
          f" mean signed {B['replay']['mean_signed']:+.4f} degrees")
    # (b1)
    kid = np.random.SeedSequence(A_SEED).spawn(3)[2]
    print(f"\n(b1) noise 0.3, {n} rings, stream child 2 (a fresh generator from it for each variant, so both see"
          " the same formation draws); bump formed as (b0); then 50 cue-off agent-steps at v = 0")
    B["b1"] = {}
    for two in (True, False):
        g = form(n, heads, 0.3, np.random.default_rng(kid))
        p = g.pos(); cum = np.zeros(n); per = []; amps = {}; jumps = 0
        for k in range(1, 51):
            g.step(v=0.0)
            if two: g.step(x=np.zeros((n, 16)))
            q = g.pos(); d = angdiff(q, p); per.append(d); cum += d; p = q; jumps += int((np.abs(d) > 30).sum())
            if k in (1, 10, 25, 50): amps[k] = float(np.median(g.amp()))
        per = np.concatenate(per)
        key = "two" if two else "one"
        B["b1"][key] = dict(step_sd=float(per.std()), sd50=float(cum.std()), amp=amps, jumps=jumps)
        print(f"   {key} step(s) per agent-step: per-step sd of the change of pos {per.std():.4f}, sd of pos at step 50"
              f" (unfolded) {cum.std():.4f}, median amp at steps 1/10/25/50 {amps[1]:.4f}/{amps[10]:.4f}/{amps[25]:.4f}/"
              f"{amps[50]:.4f}, single-step jumps over 30 degrees {jumps} of {per.size}")
    B["b1"]["ratio_sd50"] = B["b1"]["two"]["sd50"]/B["b1"]["one"]["sd50"]
    print(f"   F-v quantity: sd of pos at step 50, two steps / one step = {B['b1']['ratio_sd50']:.4f}")
    json.dump(B, open(os.path.join(ARR, "bench.json"), "w", newline="\n"), indent=1)
    print("   wrote experiments/h18/arrays/bench.json")


# ------------------------------------------------------------------ stage read
def q(x, ps=(50, 90, 99, 99.9)):
    x = np.asarray(x, float)
    return [float(np.percentile(x, p)) for p in ps] if x.size else [float("nan")]*len(ps)


def pearson(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    if x.size < 3 or x.std() == 0 or y.std() == 0: return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def spearman(x, y):
    rk = lambda v: np.argsort(np.argsort(v)).astype(float)
    return pearson(rk(np.asarray(x)), rk(np.asarray(y)))


def blocks_of(won):
    """C1: per agent, the cue-off blocks (start, end exclusive)"""
    out = []
    for r in range(won.shape[1]):
        off = np.concatenate([[0], (won[:, r] == 0).astype(np.int8), [0]]); dd = np.diff(off)
        for s, e in zip(np.where(dd == 1)[0], np.where(dd == -1)[0]): out.append((r, int(s), int(e)))
    return out


def events_of(hit):
    """loss events: since reaches LOST + 1 = 143 (ph12b.py:89; since as ph12.py:115); t_L = t - 143"""
    since = np.zeros(hit.shape[1]); ev = []
    for t in range(hit.shape[0]):
        since = np.where(hit[t] == 1, 0.0, since + 1.0)
        for r in np.where(since == LOST + 1)[0]: ev.append((int(r), t - (LOST + 1)))
    return ev


class Arm:
    def __init__(self, name, est_key="est", amp_key="amp", src_arm=None):
        Z = np.load(os.path.join(ARR, f"{src_arm or name}.npz"))
        self.name = name
        self.est = Z[est_key].astype(float); self.head = Z["head"].astype(float)
        self.won = Z["won"]; self.hit = Z["hit"]; self.turn = Z["turn"].astype(float)
        self.clock = Z["clock"]; self.pos = Z["pos"]; self.src = Z["src"]; self.pos_end = Z["pos_end"]
        self.amp = Z[amp_key].astype(float) if amp_key in Z.files else None
        self.e = angdiff(self.est, self.head)
        self.off = self.won == 0
        self.blocks = blocks_of(self.won)
        self.K = np.zeros(self.won.shape, np.int16)
        for r, s, e in self.blocks: self.K[s:e, r] = np.arange(1, e - s + 1)
        self.ev = events_of(self.hit)


def in_odour(pos, src):
    class S: pass
    s = S(); s.pos = np.asarray(pos, float); s.src = np.asarray(src, float)
    return World1.in_odour(s)                             # ph12.py:58-61, unchanged


def readings(A, P):
    """(A)-(E) for one arm; P prints. Returns the numbers."""
    S = {}; e, ae, off, won = A.e, np.abs(A.e), A.off, A.won
    aoff = ae[off]; noff = aoff.size
    # (A)
    thr = (10, 20, 30, 45, 90, 135)
    S["A_share"] = {t: float((aoff > t).mean()) for t in thr}; S["A_count"] = {t: int((aoff > t).sum()) for t in thr}
    S["A_q"] = q(aoff) + [float(aoff.max())]
    P(f"   (A) tail, cue-off agent-steps n {noff}: share over " + ", ".join(
        f"{t}: {S['A_share'][t]*100:.3f}% ({S['A_count'][t]})" for t in thr))
    P(f"       |e| quantiles 50/90/99/99.9/max {' / '.join(f'{x:.3f}' for x in S['A_q'])} deg; mean {aoff.mean():.3f}")
    pa_max = np.array([ae[off[:, r], r].max() if off[:, r].any() else 0 for r in range(R)])
    pa_20 = np.array([(ae[off[:, r], r] > 20).mean() if off[:, r].any() else 0 for r in range(R)])
    S["A_agents_any"] = {t: int((pa_max > t).sum()) for t in (45, 90, 135)}
    P(f"       per agent (n {R}): with any cue-off step over 45/90/135: {S['A_agents_any'][45]}/{S['A_agents_any'][90]}/"
      f"{S['A_agents_any'][135]}; per-agent max |e| p10/50/90/max {' / '.join(f'{x:.2f}' for x in q(pa_max, (10, 50, 90, 100)))};"
      f" per-agent share over 20 p10/50/90/max {' / '.join(f'{x*100:.2f}%' for x in q(pa_20, (10, 50, 90, 100)))}")
    byk = []
    for k in range(1, 51):
        m = A.K == k; v = ae[m]; byk.append((k, int(v.size), float((v > 45).mean()) if v.size else float("nan"),
                                             float(np.median(v)) if v.size else float("nan"), float(v.mean()) if v.size else float("nan")))
    S["A_byk"] = byk
    for i in range(0, 50, 10):
        P("       by k (k: n, share>45, median, mean)  " + "  ".join(f"{k}: {n}, {s*100:.2f}%, {md:.2f}, {mn:.2f}" for k, n, s, md, mn in byk[i:i + 10]))
    # (B)
    for t0 in (20, 45):
        L = []
        for r in range(R):
            m = np.concatenate([[0], (off[:, r] & (ae[:, r] > t0)).astype(np.int8), [0]]); dd = np.diff(m)
            L += list(np.where(dd == -1)[0] - np.where(dd == 1)[0])
        L = np.array(L)
        S[f"B_runs_{t0}"] = dict(n=int(L.size), q=q(L, (50, 90, 99)) if L.size else None, max=int(L.max()) if L.size else 0)
        P(f"   (B) runs of consecutive cue-off steps with |e| > {t0}: n {L.size}" +
          (f", length p50/p90/p99 {' / '.join(f'{x:.1f}' for x in q(L, (50, 90, 99)))}, max {L.max()}" if L.size else ""))
    ac = {}
    for lag in (1, 5, 10, 25):
        vals = []
        for r, s, en in A.blocks:
            if en - s - lag >= 3:
                c = pearson(e[s:en - lag, r], e[s + lag:en, r])
                if c == c: vals.append(c)
        ac[lag] = (float(np.median(vals)) if vals else float("nan"), len(vals))
    S["B_ac"] = ac
    P("       autocorrelation of signed e within cue-off blocks (C4), median over blocks [blocks used]: " +
      ", ".join(f"lag {l}: {ac[l][0]:.3f} [{ac[l][1]}]" for l in (1, 5, 10, 25)))
    bm = np.array([e[s:en, r].mean() for r, s, en in A.blocks])
    S["B_blockmean"] = (float(bm.mean()), float(bm.std()), int(bm.size))
    P(f"       per-block mean signed e: mean {bm.mean():+.3f}, sd across blocks {bm.std():.3f} (blocks {bm.size})")
    nxt = {}
    by_agent = {}
    for r, s, en in A.blocks: by_agent.setdefault(r, []).append((s, en))
    on = {j: [] for j in range(1, 11)}; carry = ([], []); on50 = []
    for r, bl in by_agent.items():
        for i, (s, en) in enumerate(bl):
            nstart = bl[i + 1][0] if i + 1 < len(bl) else T
            for j in range(1, 11):
                t = en + j - 1
                if t < nstart and t < T: on[j].append(ae[t, r])
            if i + 1 < len(bl): carry[0].append(e[en - 1, r]); carry[1].append(e[bl[i + 1][0], r])
            if en + 49 < nstart and en + 49 < T: on50.append(ae[en + 49, r])
    S["B_on"] = {j: (float(np.median(on[j])), float(np.percentile(on[j], 90)), float((np.array(on[j]) > 20).mean()), len(on[j])) for j in on}
    P("       |e| on cue-on step j after a cue-off block (j: median, p90, share>20, n)  " +
      "  ".join(f"{j}: {S['B_on'][j][0]:.3f}, {S['B_on'][j][1]:.3f}, {S['B_on'][j][2]*100:.2f}%, {S['B_on'][j][3]}" for j in range(1, 11)))
    S["B_carry"] = (pearson(*carry), len(carry[0])); S["B_on50"] = (float(np.median(on50)), float(np.percentile(on50, 90)), len(on50))
    P(f"       carry-over: correlation of e at a block's last cue-off step with e at the next block's first cue-off step"
      f" {S['B_carry'][0]:.3f} (pairs {S['B_carry'][1]}); |e| at cue-on step 50 median {S['B_on50'][0]:.3f}, p90 {S['B_on50'][1]:.3f} (n {S['B_on50'][2]})")
    # (C)
    Pblk = {}
    Pby = {}
    for r, s, en in A.blocks:
        Pblk[(r, s, en)] = SPEED*np.sin(np.radians(e[s:en, r])).sum(); Pby.setdefault(r, []).append((s, en, Pblk[(r, s, en)]))
    hits = {r: np.where(A.hit[:, r] == 1)[0] for r in range(R)}
    nolast = sum(1 for r, tl in A.ev if tl < 0)
    E = []
    for r, tl in A.ev:
        if tl < 0: continue
        hr = hits[r]; rec = bool((hr > tl).any())
        pre = [t for t in range(max(0, tl - 50), tl + 1) if off[t, r]]
        post = list(range(tl + 1, min(T, tl + 143)))
        w_pre = ae[pre, r] if pre else np.zeros(0); w_post = ae[post, r]
        allw = np.concatenate([w_pre, w_post])
        ton = next((t for t in range(tl + 1, T) if won[t, r] == 1), None)
        tret = next((t for t in range(tl + 1, T) if won[t, r] == 1 and won[t - 1, r] == 0), None)
        along = A.pos[tl, r, 0] - A.src[r, 0]; hw = W0 + SLOPE*max(float(along), 0.0)
        ratios = [abs(pv)/hw for (s, en, pv) in Pby.get(r, []) if s <= tl + 142 and en - 1 >= tl - 50]
        E.append(dict(r=r, tl=tl, rec=rec, e_tl=float(e[tl, r]), pre_med=float(np.median(w_pre)) if w_pre.size else float("nan"),
                      pre_max=float(w_pre.max()) if w_pre.size else float("nan"), post_med=float(np.median(w_post)),
                      post_max=float(w_post.max()), any45=bool((allw > 45).any()), off_tl=bool(off[tl, r]),
                      clock_tl=int(A.clock[tl, r]), ton=ton, tret=tret,
                      out_on=(None if ton is None else not bool(in_odour(A.pos[ton, r][None], A.src[r][None])[0])),
                      out_ret=(None if tret is None else not bool(in_odour(A.pos[tret, r][None], A.src[r][None])[0])),
                      ratios=ratios))
    U = [x for x in E if not x["rec"]]; Rc = [x for x in E if x["rec"]]
    S["C_n"] = dict(events=len(A.ev), no_prior_whiff=nolast, unrecovered=len(U), recovered=len(Rc))
    P(f"   (C) loss events {len(A.ev)} (since reaches 143); without a prior whiff (C3, excluded) {nolast};"
      f" unrecovered {len(U)}, recovered {len(Rc)}")
    for nm, G in (("unrecovered", U), ("recovered", Rc)):
        if not G: continue
        f = lambda k: np.array([x[k] for x in G], float)
        S[f"C_{nm}"] = dict(e_tl_abs_med=float(np.median(np.abs(f("e_tl")))), pre_med=float(np.nanmedian(f("pre_med"))),
                            pre_max_med=float(np.nanmedian(f("pre_max"))), post_med=float(np.median(f("post_med"))),
                            post_max_med=float(np.median(f("post_max"))), any45=float(f("any45").mean()),
                            off_tl=float(f("off_tl").mean()), clock_tl_max=int(f("clock_tl").max()))
        c = S[f"C_{nm}"]
        P(f"       {nm} (n {len(G)}): |e| at t_L median {c['e_tl_abs_med']:.3f}; pre-loss window |e| median of medians"
          f" {c['pre_med']:.3f}, median of maxima {c['pre_max_med']:.3f}; post-whiff window median of medians {c['post_med']:.3f},"
          f" median of maxima {c['post_max_med']:.3f}; share with any |e| > 45 in either window {c['any45']:.4f};"
          f" share with t_L on a cue-off step {c['off_tl']:.4f}; cast clock at t_L max {c['clock_tl_max']} (0 by ph12.py:116)")
    au = [(x["r"]) for x in E]
    # agent level
    late = A.hit[-3*STEPS:].sum(0) == 0
    S["C_agents"] = dict(unrecovered=int(late.sum()), recovered=int((~late).sum()))
    P(f"       agent level: late unrecovered agents {int(late.sum())}, recovered {int((~late).sum())} (ph12.py:164)")
    pooled = lambda G: np.array([v for x in G for v in x["ratios"]])
    pu, prc = pooled(U), pooled(Rc)
    S["C_P"] = dict(unrec_med=float(np.median(pu)) if pu.size else float("nan"), unrec_n=int(pu.size),
                    rec_med=float(np.median(prc)) if prc.size else float("nan"), rec_n=int(prc.size))
    allP = np.array(list(Pblk.values()))
    S["C_Pall"] = (float(np.abs(allP).mean()), float(allP.std()), int(allP.size))
    P(f"       path error P = SPEED x sum sin(e) per cue-off block: all blocks mean |P| {np.abs(allP).mean():.3f}, sd {allP.std():.3f}"
      f" (n {allP.size}); |P| / half-width at t_L (C8): unrecovered median {S['C_P']['unrec_med']:.4f} (pairs {pu.size}),"
      f" recovered median {S['C_P']['rec_med']:.4f} (pairs {prc.size})")
    # (D)
    tt, rr = np.where(off); keep = tt >= 1; tt, rr = tt[keep], rr[keep]
    v = A.turn[tt - 1, rr]; rres = angdiff(A.est[tt, rr], A.est[tt - 1, rr]) - v
    bins = [(0, 10), (10, 20), (20, 30), (30, 40), (40, 1e9)]
    S["D_bins"] = []
    for lo, hi in bins:
        m = (np.abs(v) >= lo) & (np.abs(v) < hi)
        S["D_bins"].append((lo, hi, int(m.sum()), float(rres[m].mean()) if m.any() else float("nan"), float(rres[m].std()) if m.any() else float("nan")))
    slope = float(np.cov(rres, v)[0, 1]/v.var(ddof=1))
    jumps = int((np.abs(rres) > 30).sum()); S["D_slope"] = slope; S["D_jumps_per1e5"] = jumps/rres.size*1e5
    P(f"   (D) step residual r_t (C2) on {rres.size} cue-off steps: by |v| bin (n, mean, sd) " +
      "; ".join(f"{lo}-{'' if hi > 1e8 else hi}: {n}, {mn:+.4f}, {sd:.4f}" for lo, hi, n, mn, sd in S["D_bins"]) +
      f"; OLS slope of r on v {slope:+.5f}; jumps |r| > 30: {jumps} ({S['D_jumps_per1e5']:.2f} per 100,000)")
    endE, sumV = [], []
    for r, s, en in A.blocks:
        ts = np.arange(max(s, 1), en)
        if ts.size == 0: continue
        endE.append(e[en - 1, r]); sumV.append(A.turn[ts - 1, r].sum())
    S["D_corr_end_sumv"] = pearson(endE, sumV)
    P(f"       correlation of end-of-block signed e with the block's summed signed rotation {S['D_corr_end_sumv']:+.4f} (blocks {len(endE)})")
    if A.amp is not None:
        amk = [float(np.median(A.amp[A.K == k])) for k in (1, 10, 25, 50)]
        rat = []
        for r, s, en in A.blocks:
            if en - s >= 50: rat.append(A.amp[s + 49, r]/A.amp[s, r])
        m50 = A.K == 50
        S["D_amp_k"] = amk; S["D_amp_ratio"] = float(np.median(rat)); S["D_amp_ratio_of_medians"] = amk[3]/amk[0]
        S["D_rho50"] = spearman(ae[m50], A.amp[m50]); S["D_amp_n"] = len(rat)
        P(f"       amp by cue-off step k 1/10/25/50 (median) {' / '.join(f'{x:.4f}' for x in amk)}; per-block amp(50)/amp(1)"
          f" median (C6) {S['D_amp_ratio']:.4f} (blocks {len(rat)}), ratio of medians {S['D_amp_ratio_of_medians']:.4f};"
          f" Spearman rho |e| vs amp at k 50 {S['D_rho50']:+.4f} (n {int(m50.sum())})")
    # F-iii quantities
    s2 = S["B_on"][2][0]; S["F3iii"] = dict(step2_med=s2)
    if U:
        lit = [x["out_on"] for x in U if x["out_on"] is not None]; ret = [x["out_ret"] for x in U if x["out_ret"] is not None]
        S["F3iii"].update(share_lit=float(np.mean(lit)) if lit else float("nan"), n_lit=len(lit),
                          share_ret=float(np.mean(ret)) if ret else float("nan"), n_ret=len(ret))
        P(f"       F-iii: unrecovered events outside the odour at the first cue-on step after t_L (C7, literal)"
          f" {S['F3iii']['share_lit']:.4f} (n {len(lit)}); at the first cue RETURN after t_L (reported) {S['F3iii']['share_ret']:.4f} (n {len(ret)})")
    # (E)
    dend = np.linalg.norm(A.pos_end - A.src, axis=1); dmax = np.linalg.norm(A.pos - A.src[None], axis=2).max(0)
    S["E"] = dict(end_q=q(dend, (10, 50, 90, 100)), max_q=q(dmax, (10, 50, 90, 100)), beyond25=float((dend > 25).mean()))
    P(f"   (E) exposure: wall contacts 0 by construction (ph12b.py:52-53); distance from source at the end (C9)"
      f" p10/50/90/max {' / '.join(f'{x:.1f}' for x in S['E']['end_q'])}; max over the run p10/50/90/max"
      f" {' / '.join(f'{x:.1f}' for x in S['E']['max_q'])}; farther than LMAX 25 at the end {S['E']['beyond25']*100:.1f}% of {R}")
    S["_U"] = U; S["_Rc"] = Rc
    return S


def band(met, notmet):
    return "MET" if met else ("NOT MET" if notmet else "INCONCLUSIVE")


def ftable(S, B, mism, cue_share, P, label):
    F = {}
    nu, nr = S["C_n"]["unrecovered"], S["C_n"]["recovered"]
    unread = nu < 50 or nr < 50
    su = S["C_unrecovered"]["any45"] if "C_unrecovered" in S else float("nan"); sr = S["C_recovered"]["any45"] if "C_recovered" in S else float("nan")
    F["F1"] = ("UNREADABLE" if unread else band(su >= 0.70 and su >= 2*sr, su <= 0.30 or su <= 1.2*sr), f"unrecovered {su:.4f} (n {nu}), recovered {sr:.4f} (n {nr})")
    ac10 = S["B_ac"][10][0]; s3 = S["B_on"][3][0]
    F["F2"] = ("UNREADABLE" if ac10 != ac10 else band(ac10 >= 0.6 and s3 <= 5, ac10 <= 0.2), f"lag-10 median {ac10:.4f} (blocks {S['B_ac'][10][1]}), cue-on step 3 median |e| {s3:.4f}")
    sh = S["C_unrecovered"]["off_tl"] if "C_unrecovered" in S else float("nan")
    F["F3"] = ("UNREADABLE" if nu < 50 else band(sh >= 0.60, sh <= 0.45), f"t_L cue-off share {sh:.4f} (n {nu}); measured cue-off share of all agent-steps {cue_share:.4f}")
    g = {int(k.split("_")[1]): d for k, d in B["b0"].items() if k.startswith("two_") and d["gain_median"] is not None}
    g45 = [d["gain_median"] for v, d in g.items() if abs(v) <= 45]; g60 = [d["gain_median"] for v, d in g.items() if abs(v) <= 60]
    sl, co = S["D_slope"], S["D_corr_end_sumv"]
    F["Fi"] = (band(any(x < 0.90 or x > 1.10 for x in g45) or abs(sl) >= 0.05 or abs(co) >= 0.3,
                    all(0.97 <= x <= 1.03 for x in g60) and abs(sl) <= 0.02 and abs(co) <= 0.1),
               f"bench gains (median, zero step) {min(g60):.4f} to {max(g60):.4f} for |v| <= 60; closed-loop slope {sl:+.5f}; end-of-block correlation {co:+.4f}")
    if "D_amp_ratio" in S:
        ra, j, rho = S["D_amp_ratio"], S["D_jumps_per1e5"], S["D_rho50"]
        F["Fii"] = (band(ra <= 0.5 or j >= 10 or rho <= -0.4, ra >= 0.8 and j <= 1 and abs(rho) <= 0.2),
                    f"amp ratio {ra:.4f}; jumps {j:.2f} per 100,000; rho {rho:+.4f}")
    else: F["Fii"] = ("UNREADABLE", "no amplitude (no ring)")
    s2 = S["F3iii"]["step2_med"]; shl = S["F3iii"].get("share_lit", float("nan"))
    F["Fiii"] = ("UNREADABLE" if nu < 50 else band(s2 <= 5 and shl >= 0.60, s2 > 15 or shl <= 0.40), f"cue-on step 2 median |e| {s2:.4f}; share outside the odour {shl:.4f} (n {S['F3iii'].get('n_lit', 0)})")
    F["Fiv"] = (band(mism > 0, mism == 0), f"mismatch count {mism}")
    rv = B["b1"]["ratio_sd50"]
    F["Fv"] = (band(rv >= 1.3, rv <= 1.1), f"bench (b1) sd ratio two/one {rv:.4f}")
    pu, prc = S["C_P"]["unrec_med"], S["C_P"]["rec_med"]
    F["Fvi"] = ("UNREADABLE" if unread else band(F["F1"][0] == "NOT MET" and pu >= 0.5 and pu >= 1.5*prc, pu <= 0.25 or pu <= 1.1*prc),
                f"median |P| / half-width unrecovered {pu:.4f}, recovered {prc:.4f}")
    for k in ("F1", "F2", "F3", "Fi", "Fii", "Fiii", "Fiv", "Fv", "Fvi"):
        P(f"   {label:9s} {k:5s} {F[k][0]:12s} {F[k][1]}")
    return F


def pairing(Asep, Aint, P):
    """amendment 6: pairing ends at divergence. Per agent: t_div (hit outcome; position > 1.0), e at t_div,
    whether t_div precedes t_L of ring_sep's first loss event."""
    first_tl = {}
    for r, tl in Asep.ev:
        if tl >= 0 and r not in first_tl: first_tl[r] = tl
    out = {}
    for kind in ("hit", "pos"):
        td, ed, prec = [], [], []
        for r in range(R):
            if kind == "hit": d = np.where(Asep.hit[:, r] != Aint.hit[:, r])[0]
            else: d = np.where(np.linalg.norm(Asep.pos[:, r].astype(float) - Aint.pos[:, r].astype(float), axis=1) > 1.0)[0]
            t = int(d[0]) if d.size else None
            td.append(t if t is not None else T); ed.append(abs(Asep.e[t, r]) if t is not None else np.nan)
            if r in first_tl and t is not None: prec.append(t < first_tl[r])
        td = np.array(td); nd = int((td < T).sum())
        out[kind] = dict(diverged=nd, tdiv_q=q(td[td < T], (10, 50, 90)), e_q=q(np.array(ed)[td < T], (50, 90)),
                         precedes=int(np.sum(prec)), with_loss=len(prec))
        o = out[kind]
        P(f"   pairing (ring_sep vs integrate), divergence by {'whiff outcome' if kind == 'hit' else 'position > 1.0'}:"
          f" diverged agents {nd} of {R}; t_div p10/50/90 {' / '.join(f'{x:.0f}' for x in o['tdiv_q'])};"
          f" |e| at t_div p50/p90 {' / '.join(f'{x:.3f}' for x in o['e_q'])};"
          f" t_div before ring_sep's first loss t_L in {o['precedes']} of {o['with_loss']} agents with a loss event")
    return out


def stage_read():
    header("read")
    lines = []
    def P(s=""): print(s); lines.append(s)
    print("\nChoices where the registered text needed a reading in code (fixed before any output existed):")
    for ln in __doc__.split("Choices where")[1].split("\n")[2:]:
        if ln.strip(): print("  " + ln.strip())
    print("\n== logs of the earlier stages, embedded verbatim ==")
    for f in ("demo", "r0", "arm_exact", "arm_none", "arm_ring", "arm_integrate", "arm_ring_sep", "arm_ring_made", "bench"):
        p = os.path.join(LOGS, f + ".txt")
        print(f"\n---- experiments/h18/logs/{f}.txt (sha256 {sha(p)}) ----")
        print(open(p, encoding="utf-8").read().rstrip("\n"))
    meta = {a: json.load(open(os.path.join(ARR, f"{a}_meta.json"))) for a in ARMS}
    B = json.load(open(os.path.join(ARR, "bench.json")))
    SUM = dict(meta=meta, bench=B)
    print("\n== array files (kept local, not committed) ==")
    for a in ARMS: print(f"   experiments/h18/arrays/{a}.npz  {meta[a]['npz_bytes']} bytes  sha256 {meta[a]['npz_sha256']}")
    print(f"   experiments/h18/arrays/bench.json  sha256 {sha(os.path.join(ARR, 'bench.json'))}")
    # R1: ph12b's own print code on the loaded dicts
    print("\n== R1: K5 record lines 162-189 regenerated by ph12b.stage_b's own print code from the harness arrays ==")
    O = {}
    for a in RECORDED:
        Z = np.load(os.path.join(ARR, f"{a}.npz"))
        O[a] = {k: (Z[f"o_{k}"] if Z[f"o_{k}"].ndim else Z[f"o_{k}"].item()) for k in OKEYS}
    headmap = {"none": "none", "ring": "ring", "integrate": "integrate"}
    def fake(rule, head="exact", start="cone", walls=True, wind="always", seeds=(0, 1), **kw):
        return O[head] if (not walls and wind == "blocks") else O["exact"]
    real = ph12b.run2; ph12b.run2 = fake
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        ph12b.stage_b("eval", {"W-cone": {"return": O["exact"]}, "O-cone": {"return": O["exact"]}})
    ph12b.run2 = real
    got = buf.getvalue().split("\n"); i0 = next(i for i, x in enumerate(got) if x.startswith("   (b) OPEN PLANE"))
    got = got[i0:]
    while got and got[-1] == "": got.pop()
    rec = open(RECORD, encoding="utf-8").read().split("\n")[161:189]
    r1 = got == rec
    print(f"   regenerated {len(got)} lines, record lines 162-189 {len(rec)}: {'CHARACTER FOR CHARACTER EQUAL' if r1 else 'DIFFERENT'}")
    if not r1:
        for k, (x, y) in enumerate(zip(rec, got)):
            if x != y: print(f"   line {162 + k}:\n     record : {x}\n     harness: {y}")
        print("STOP: R1 failed"); sys.exit(5)
    bw = {a: all(meta[a]["bitwise_vs_run2"].values()) for a in RECORDED}
    print(f"   per-agent arrays equal ph12b.run2 bitwise: {bw}")
    SUM["R1"] = dict(lines_equal=r1, bitwise=bw)
    # identities
    print("\n== identities ==")
    I = {}
    I["I1"] = {a: meta[a]["mismatch"][0] for a in ("ring", "integrate")}
    print(f"   I1 mismatch count (handed != made): ring {I['I1']['ring']}, integrate {I['I1']['integrate']} -> {'PASS' if not any(I['I1'].values()) else 'FAIL'}")
    I["I2"] = bool(np.array_equal(O["integrate"]["score"], O["exact"]["score"]))
    print(f"   I2 integrate == exact on every per-agent score: {I['I2']}")
    I["I3"] = bool(all(meta["integrate"]["bitwise_vs_run2"].values()))
    print(f"   I3 integrate with the shadow attached == ph12b.run2 integrate, every key bitwise: {I['I3']}")
    Zr, Zm = np.load(os.path.join(ARR, "ring.npz")), np.load(os.path.join(ARR, "ring_made.npz"))
    dest = float(np.abs(angdiff(Zr["est"].astype(float), Zm["est"].astype(float))).max())
    dsc = float(np.abs(Zr["o_score"] - Zm["o_score"]).max())
    I["I4"] = dict(max_est_diff=dest, max_score_diff=dsc, lost_end_equal=bool(np.array_equal(Zr["o_lost_end"], Zm["o_lost_end"])))
    print(f"   I4 ring_made vs ring (reported): max |est difference| {dest:.6g} deg (float32 arrays), max per-agent block-score"
          f" difference {dsc:.6g}, lost_end equal {I['I4']['lost_end_equal']}")
    del Zr, Zm
    nco = meta["ring"]["cueoff_agent_steps"]; cue_share = nco/(T*R)
    I["I5"] = dict(nocue={a: meta[a]["nocue_steps"] for a in ARMS if ARMS[a][1] == "blocks"}, cueoff=nco, share=cue_share,
                   cueoff_all_equal=len({meta[a]["cueoff_agent_steps"] for a in ARMS if ARMS[a][1] == "blocks"}) == 1)
    print(f"   I5 steps with no cued agent {I['I5']['nocue']}; cue-off agent-steps {nco} of {T*R} -> measured cue-off share"
          f" {cue_share:.6f} (same in every dropout arm: {I['I5']['cueoff_all_equal']})")
    inst = O["integrate"]["err_off"][0]/O["integrate"]["err_off"][1]
    I["I6"] = float(inst)
    print(f"   I6 instrument check: integrate over 45 deg on {inst*100:.2f}% of cue-off steps < 1: {inst < 0.01}")
    SUM["identities"] = I
    if any(I["I1"].values()) or not I["I2"] or not I["I3"] or inst >= 0.01:
        print("STOP: an identity failed"); sys.exit(6)
    # I7 known answers, before any ring reading
    print("\n== I7 known-answer readings (before any ring, ring_sep or shadow reading) ==")
    An = Arm("none")
    print(f"   `none`: in-run err_off share {O['none']['err_off'][0]/O['none']['err_off'][1]*100:.2f}% and mean"
          f" {O['none']['abs_off']/O['none']['err_off'][1]:.1f} deg (K5 record:173: 66.15%, 79.7)")
    st = {"on": True}
    def PA(s):                                            # `none` is read on (A) only (and F1 below)
        if s.startswith("   (B)"): st["on"] = False
        if st["on"]: P(s)
    Sn = readings(An, PA)
    Fn = ftable(Sn, B, meta["ring"]["mismatch"][0], cue_share, lambda s: None, "none")
    print(f"   `none` F1: {Fn['F1'][0]}  ({Fn['F1'][1]}); expected MET")
    del An
    Ai = Arm("integrate", amp_key="__none__")
    emax = meta["integrate"]["max_abs_e_in_run"]
    print(f"   `integrate`: max |e| over every agent-step in the run (float64) {emax!r}; from the stored arrays {np.abs(Ai.e).max()!r}")
    Si = readings(Ai, lambda s: None)
    Fi_ = ftable(Si, B, meta["integrate"]["mismatch"][0], cue_share, lambda s: None, "integrate")
    readable = {k: v for k, v in Fi_.items() if v[0] != "UNREADABLE" and k in ("F1", "F2", "F3", "Fii", "Fiii", "Fvi")}
    print(f"   `integrate` F rows on which e can be read: " + "; ".join(f"{k} {v[0]} ({v[1]})" for k, v in Fi_.items() if k in ("F1", "F2", "F3", "Fii", "Fiii", "Fvi")))
    SUM["I7"] = dict(none_F1=Fn["F1"], none_A_share45=Sn["A_share"][45], integrate_emax=emax,
                     integrate_rows={k: v for k, v in Fi_.items()})
    surprise = []
    if Fn["F1"][0] != "MET": surprise.append(f"`none` F1 reads {Fn['F1'][0]} ({Fn['F1'][1]}), expected MET")
    if emax != 0.0: surprise.append(f"`integrate` max |e| {emax!r}, expected identically 0")
    for k, v in readable.items():
        if v[0] != "NOT MET": surprise.append(f"`integrate` {k} reads {v[0]}, expected NOT MET")
    json.dump(clean(SUM), open(os.path.join(OUT, "ph37_summary.json"), "w", newline="\n"), indent=1)
    if surprise:
        print("\nSTOP at I7 (design section 7: 'a surprise in either is an implementation error, repaired and disclosed"
              " before any `ring`, `ring_sep` or `shadow` reading is taken'):")
        for s in surprise: print(f"   - {s}")
        print("   No ring, ring_sep or shadow reading has been computed. experiments/h18/ph37_summary.json holds the numbers so far.")
        sys.exit(7)
    print("   I7: no surprise")
    ring_readings(SUM, B, meta, cue_share, P)


def ring_readings(SUM, B, meta, cue_share, P):
    print("\n== readings (A)-(E) ==")
    S = {}
    for nm, kw in (("ring_sep", {}), ("ring", {}), ("shadow", dict(est_key="sh_est", amp_key="sh_amp", src_arm="integrate"))):
        print(f"\n-- {nm} --")
        A = Arm(nm, **kw); S[nm] = readings(A, P)
        if nm == "ring_sep": Asep = A
        else: del A
    print("\n-- pairing (amendment 6: the only paired quantities; everything after t_div is read per arm) --")
    Aint = Arm("integrate", amp_key="__none__")
    PAIR = pairing(Asep, Aint, P); del Aint, Asep
    print("\n== registered falsification readings (ring_sep reads the F rows; ring and shadow beside) ==")
    F = {}
    for nm in ("ring_sep", "ring", "shadow"):
        F[nm] = ftable(S[nm], B, meta["ring"]["mismatch"][0], cue_share, print, nm)
    f = {k: v[0] for k, v in F["ring_sep"].items()}
    print("\n== branch table read from the ring_sep F rows only (design section 3) ==")
    br = {"B-i": f["Fi"] == "MET", "B-ii": f["Fii"] == "MET", "B-iii": f["Fiii"] == "MET" and f["F3"] == "MET",
          "B-v": f["Fv"] == "MET" and f["Fi"] == "NOT MET" and f["Fii"] == "NOT MET",
          "B-vi": f["Fvi"] == "MET" and f["F1"] == "NOT MET"}
    br["B-close"] = not any(v == "MET" for k, v in f.items() if k in ("Fi", "Fii", "Fiii", "Fv", "Fvi"))
    for k, v in br.items(): print(f"   {k:8s} condition {'met' if v else 'not met'}")
    for nm in S:
        S[nm].pop("_U", None); S[nm].pop("_Rc", None)
    SUM.update(readings=S, pairing=PAIR, F=F, branches=br)
    json.dump(clean(SUM), open(os.path.join(OUT, "ph37_summary.json"), "w", newline="\n"), indent=1)
    print("\n   wrote experiments/h18/ph37_summary.json")


def clean(x):
    if isinstance(x, dict): return {str(k): clean(v) for k, v in x.items() if not str(k).startswith("_")}
    if isinstance(x, (list, tuple)): return [clean(v) for v in x]
    if isinstance(x, (np.integer,)): return int(x)
    if isinstance(x, (np.floating,)): return float(x)
    if isinstance(x, np.bool_): return bool(x)
    if isinstance(x, float) and x != x: return None
    return x


if __name__ == "__main__":
    args = sys.argv[1:]
    os.makedirs(ARR, exist_ok=True); os.makedirs(LOGS, exist_ok=True)
    stage = args[0] if args else "demo"
    if stage == "demo": stage_demo()
    elif stage == "r0": stage_r0()
    elif stage == "arm" and len(args) > 1 and args[1] in ARMS: stage_arm(args[1])
    elif stage == "bench": stage_bench()
    elif stage == "read": stage_read()
    else: print(__doc__); sys.exit(1)
