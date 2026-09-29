#!/usr/bin/env python3
"""H18 Stage B (branch B-iii): one restart of the cast clock per silence at the first cue-on step.

Usage (ONE process at a time; one arm per process):
    python src/ph38.py demo | arm <K5b|K5a> <arm> | calib | read
    arms: ring restart restart_rand exact exact_restart none integrate
This pass runs the BENCH only (bench seeds). Development and evaluation are not run by this file
until the bench decision is committed (design v2 amendment 5).

Registered by experiments/h18/h18_stage_b_design_v2.md (v2 FINAL, decision:h18-stage-b-open).
ph12b, ph12, ph10, ph11, ph9 and every adopted file are imported unchanged; the registered files'
sha256 prefixes are checked before anything runs.

Choices where the registered text needed a reading in code (fixed before any output existed):
  C1  the restart: where fire, the clock is set to -1 before Nav2.act, whose increment on a whiff-free
      step (ph12.py:116) makes the clock used for this step's target exactly 0; since is not touched.
      Equivalent to 'reset after the increment' (design 3.2 [v2, amendment 1]).
  C2  a cue return is a step with the cue on and the previous step's cue off; the previous cue state
      is True at construction (every agent is cued for t < 50, ph12b.py:44).
  C3  'whiff-free agent-step' (p for restart_rand, 3.2): an agent-step with no whiff (hit False).
      restart_rand draws one uniform per agent on every step from its own stream and fires where
      the step is whiff-free and the draw is below p; `armed` and the cue play no part in it.
  C4  every arm is built as Nav5; `ring`, `exact`, `none`, `integrate` with the rule off. Their
      comparison with ph12b.run2 is (I-d) and (I-e) at once.
  C5  in K5(b) every arm runs with wind 'blocks' (exact heading ignores the cue, ph12.py:104, so
      `exact` under 'blocks' is `exact` under 'always'); K5(a) is W-cone, walls 160 apart, 'always'.
  C6  (I-c): per agent, every recorded per-step field (est, head, pos, hit, clock, cue) equal on
      every step before the agent's first firing; agents that never fire are compared on all steps.
  C7  (b2) 'the clock value at each firing' is the clock the rule restarted: the clock of the
      previous step plus 1 (the value the step would have used without the restart).
  C8  (b4) the paired `integrate` agent: `restart` draws its ring noise from the agent generator
      (as recorded, ph12.py:84), `integrate` draws none, so their turn noise differ from step 0 and
      the pair diverges before any block ends. (b4) is printed as unreadable with that count, not
      computed on a different pairing.
  C9  M3/M4 'paired mean last-third score': the per-agent last-third mean (ph12.last), paired over
      the 200 agents; the bootstrap and the M2/M5 bootstrap share one index matrix from the bootstrap
      seed.
"""
import sys, os, io, json, time, hashlib, platform, contextlib, runpy, subprocess, inspect
sys.stdout.reconfigure(newline="\n")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
OUT = os.path.join(ROOT, "experiments", "h18"); ARR = os.path.join(OUT, "arrays_b"); LOGS = os.path.join(OUT, "logs_b")
DESIGN = os.path.join(OUT, "h18_stage_b_design_v2.md")
REGISTERED = dict(ph12="e1035e09", ph12b="ec6b1896", ph9="7699b4e6", ph10="de93f177", ph11="e80f40bd",
                  ph16="33d5fdb2", ph23="ae180492", ph35="e4a3ceda", ph37="76190250")

import ph12b, ph12, ph10, ph11, ph9, ph16
from ph9 import angdiff, STEPS
from ph12 import R, BLOCKS, LOST, last
from ph12b import World3, Nav3
from math import erf, sqrt

SEEDS = dict(bench=(18101, 18201, 18104))
STAGE = "bench"
W_SEED, A_SEED, B_SEED = SEEDS[STAGE]
T = BLOCKS*STEPS
ARMS = {"ring": ("ring", "off"), "restart": ("ring", "cue"), "restart_rand": ("ring", "rand"),
        "exact": ("exact", "off"), "exact_restart": ("exact", "cue"), "none": ("none", "off"),
        "integrate": ("integrate", "off")}
TASKS = {"K5b": dict(walls=False, wind="blocks"), "K5a": dict(walls=True, wind="always")}
OKEYS = ("score", "whiff", "wall", "contact", "events", "gaps", "wallfree", "err", "err_off", "abs_off", "mismatch", "lost_end")
PFILE = os.path.join(OUT, "ph38_p.json")


def sha(path): return hashlib.sha256(open(path, "rb").read()).hexdigest()


def header(stage):
    head = subprocess.run(["git", "log", "-1", "--format=%H"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8").stdout.strip()
    print(f"== H18 Stage B (B-iii), src/ph38.py, stage `{stage}`, seeds of stage `{STAGE}` ==")
    print(f"python {platform.python_version()}  numpy {np.__version__}  platform {platform.platform()}")
    print(f"HEAD {head}")
    print(f"src/ph38.py sha256 {sha(os.path.abspath(__file__))}")
    print(f"design experiments/h18/h18_stage_b_design_v2.md sha256 {sha(DESIGN)}")
    bad = []
    for name, reg in REGISTERED.items():
        h = sha(os.path.join(HERE, name + ".py")); ok = h.startswith(reg)
        print(f"  registered src/{name}.py sha256 {h}  prefix {reg}: {'ok' if ok else 'MISMATCH'}")
        if not ok: bad.append(name)
    for name, m in sorted(sys.modules.items()):
        f = getattr(m, "__file__", None)
        if f and os.path.dirname(os.path.abspath(f)) == HERE and name not in REGISTERED and name != "__main__":
            print(f"  imported src/{name}.py sha256 {sha(f)}")
    if bad: print(f"STOP: registered source does not match the design header: {bad}"); sys.exit(2)
    print(f"seeds: world {W_SEED}, agent {A_SEED}, bootstrap {B_SEED}; restart_rand stream SeedSequence({A_SEED}).spawn(1)[0]")
    print(f"BLAS threads: OPENBLAS {os.environ.get('OPENBLAS_NUM_THREADS')} OMP {os.environ.get('OMP_NUM_THREADS')} MKL {os.environ.get('MKL_NUM_THREADS')}")


class Nav5(Nav3):
    """Nav3 plus B-iii (design v2 3.2). mode: 'off' (== Nav3), 'cue' (the registered rule), 'rand' (restart_rand)."""

    def __init__(self, runs, rng, rule, head, mode="off", p=0.0, rrng=None):
        super().__init__(runs, rng, rule, head)
        self.mode, self.p, self.rrng = mode, p, rrng
        self.armed = np.zeros(runs, bool)             # False at construction ([v2, amendment 1])
        self.prev_on = np.ones(runs, bool)             # C2
        self.fired = np.zeros(runs, bool)

    def act(self, w, hit, wind_on):
        if self.mode == "off": return super().act(w, hit, wind_on)
        if self.mode == "cue":
            fire = wind_on & ~self.prev_on & self.armed & ~hit
        else:
            u = self.rrng.random(self.R); fire = ~hit & (u < self.p)
        self.clock = np.where(fire, -1.0, self.clock)  # C1: Nav2.act's increment makes it 0 for this step's target
        turn = super().act(w, hit, wind_on)
        self.armed = (self.armed | hit) & ~fire
        self.prev_on = wind_on.copy(); self.fired = fire
        return turn


def harness(task, arm, p=0.0):
    """ph12b.run2 (ph12b.py:73-102) line for line, with Nav5 in place of Nav3, plus reads."""
    head, mode = ARMS[arm]; kw = TASKS[task]
    rrng = np.random.default_rng(np.random.SeedSequence(A_SEED).spawn(1)[0]) if mode == "rand" else None
    w = World3(R, np.random.default_rng(W_SEED), "cone", kw["walls"], kw["wind"])
    a = Nav5(R, np.random.default_rng(A_SEED), "return", head, mode, p, rrng)
    f32 = lambda *s: np.zeros(s, np.float32)
    rec = dict(est=f32(T, R), head=f32(T, R), pos=f32(T, R, 2), turn=f32(T, R),
               hit=np.zeros((T, R), np.int8), won=np.zeros((T, R), np.int8), fired=np.zeros((T, R), np.int8),
               clock=np.zeros((T, R), np.int16))
    z = lambda: np.zeros((BLOCKS, R))
    o = dict(score=z(), whiff=z(), wall=z(), contact=z(), events=0, gaps=[], wallfree=[],
             err=np.zeros(2), err_off=np.zeros(2), abs_off=0.0, mismatch=np.zeros(3))
    touched = np.zeros(R, bool)
    for t in range(T):
        b = t // STEPS
        hit = w.sense(); won = w.wind_on()
        back = hit & (a.since > LOST)
        if back.any():
            o["gaps"].append(a.since[back].copy()); o["wallfree"].append(~touched[back])
        touched &= ~hit
        rec["head"][t] = w.head; rec["pos"][t] = w.pos; rec["hit"][t] = hit; rec["won"][t] = won
        turn = a.act(w, hit, won)
        o["events"] += int((a.since == LOST + 1).sum())
        if head != "exact":
            e = np.abs(angdiff(a.est, w.head)); bad = e > 45.0
            o["err"] += (bad.sum(), R); o["err_off"] += (bad[~won].sum(), (~won).sum())
            o["abs_off"] += e[~won].sum()
        rec["est"][t] = a.est; rec["clock"][t] = a.clock; rec["turn"][t] = turn; rec["fired"][t] = a.fired
        w.move(turn); a.bump(w.bumped); touched |= w.bumped
        differ = np.abs(angdiff(w.rot, turn)) > 1e-6
        o["mismatch"] += (differ.sum(), (differ & w.bumped).sum(), R)
        o["score"][b] += w.at_source(); o["whiff"][b] += hit; o["contact"][b] += w.bumped
        if kw["walls"]: o["wall"][b] += np.minimum(w.pos, w.arena - w.pos).min(1) < 1.0
    o["lost_end"] = a.since > LOST
    o["gaps"] = np.concatenate(o["gaps"]) if o["gaps"] else np.zeros(0)
    o["wallfree"] = np.concatenate(o["wallfree"]) if o["wallfree"] else np.zeros(0, bool)
    return o, rec, w


def stage_demo():
    header("demo")
    for script in ("ph12b.py", "ph12c.py"):
        print(f"\n-- python src/{script} demo (its own asserts) --")
        old = sys.argv; sys.argv = [script, "demo"]; code = 0
        try: runpy.run_path(os.path.join(HERE, script), run_name="__main__")
        except SystemExit as ex: code = ex.code or 0
        finally: sys.argv = old
        print(f"   exit code {code}")
        if code: print("STOP: demo failed"); sys.exit(1)
    print("\n-- harness asserts (short constructed schedules, 40 agents x 300 steps) --")
    # rule off == Nav3 step for step; rule on fires only at a cue return after a whiff
    for walls, wind in ((False, "blocks"), (True, "always")):
        w1 = World3(40, np.random.default_rng(3), "cone", walls, wind); w2 = World3(40, np.random.default_rng(3), "cone", walls, wind)
        n1 = Nav5(40, np.random.default_rng(4), "return", "ring", "off"); n2 = Nav3(40, np.random.default_rng(4), "return", "ring")
        for _ in range(300):
            h1, o1 = w1.sense(), w1.wind_on(); h2, o2 = w2.sense(), w2.wind_on()
            w1.move(n1.act(w1, h1, o1)); w2.move(n2.act(w2, h2, o2)); n1.bump(w1.bumped); n2.bump(w2.bumped)
        assert np.array_equal(w1.pos, w2.pos) and np.array_equal(n1.clock, n2.clock)
    print("ok  Nav5 with the rule off == Nav3 over 300 steps, open plane 'blocks' and walled 'always'")
    w = World3(40, np.random.default_rng(3), "cone", False, "blocks"); n = Nav5(40, np.random.default_rng(4), "return", "ring", "cue")
    prev = np.ones(40, bool); armed = np.zeros(40, bool); nf = 0
    for _ in range(300):
        h, on = w.sense(), w.wind_on(); pc = n.clock.copy()
        turn = n.act(w, h, on); ret = on & ~prev
        exp = ret & armed & ~h
        assert np.array_equal(n.fired, exp) and np.all(n.clock[n.fired] == 0.0)
        armed = (armed | h) & ~exp; prev = on.copy(); nf += int(n.fired.sum()); w.move(turn)
    print(f"ok  rule on fires exactly at cue returns after a whiff with no whiff there, clock 0 at each firing ({nf} firings)")
    w = World3(40, np.random.default_rng(3), "cone", True, "always"); n = Nav5(40, np.random.default_rng(4), "return", "ring", "cue")
    for _ in range(300):
        h, on = w.sense(), w.wind_on(); w.move(n.act(w, h, on)); n.bump(w.bumped); assert not n.fired.any()
    print("ok  with the cue on every step the rule never fires")
    print("ok  demo stage complete")


def stage_arm(task, arm):
    header(f"arm {task} {arm}")
    head, mode = ARMS[arm]; kw = TASKS[task]; p = 0.0
    if mode == "rand":
        P = json.load(open(PFILE)); p = P["p"]
        print(f"   restart_rand at the frozen p {p!r} (experiments/h18/ph38_p.json sha256 {sha(PFILE)})")
    print(f"task {task} ({kw}), arm `{arm}`: head {head}, rule {mode}, `return`, {R} agents x {T} steps")
    t0 = time.time(); o, rec, w = harness(task, arm, p); th = time.time() - t0
    meta = dict(task=task, arm=arm, head=head, mode=mode, p=p, seconds_harness=round(th, 1),
                firings=int(rec["fired"].sum()), whiff_free=int((rec["hit"] == 0).sum()))
    print(f"   harness {th:.0f} s; firings {meta['firings']}; whiff-free agent-steps {meta['whiff_free']}")
    if mode == "off":
        t1 = time.time()
        o2 = ph12b.run2("return", head=head, walls=kw["walls"], wind=kw["wind"], seeds=(W_SEED, A_SEED))
        eq = {k: bool(np.array_equal(np.asarray(o[k]), np.asarray(o2[k]))) for k in OKEYS}
        meta["bitwise_vs_run2"] = eq; meta["seconds_run2"] = round(time.time() - t1, 1)
        print(f"   ph12b.run2 {meta['seconds_run2']:.0f} s; Nav5 (rule off) == ph12b.run2 bitwise per key: {eq}")
    os.makedirs(ARR, exist_ok=True)
    path = os.path.join(ARR, f"{task}_{arm}.npz")
    np.savez_compressed(path, **rec, src=w.src, pos_end=w.pos, **{f"o_{k}": np.asarray(o[k]) for k in OKEYS})
    meta["npz_sha256"] = sha(path); meta["npz_bytes"] = os.path.getsize(path)
    json.dump(meta, open(os.path.join(ARR, f"{task}_{arm}_meta.json"), "w", newline="\n"), indent=1)
    print(f"   wrote experiments/h18/arrays_b/{task}_{arm}.npz ({meta['npz_bytes']} bytes, sha256 {meta['npz_sha256']}); {time.time() - t0:.0f} s")


def stage_calib():
    header("calib")
    m = json.load(open(os.path.join(ARR, "K5b_restart_meta.json")))
    p = m["firings"]/m["whiff_free"]
    json.dump(dict(p=p, firings=m["firings"], whiff_free=m["whiff_free"], from_npz_sha256=m["npz_sha256"], stage=STAGE),
              open(PFILE, "w", newline="\n"), indent=1)
    print(f"(b3) p = firings / whiff-free agent-steps of `restart` on the bench, K5(b) = {m['firings']} / {m['whiff_free']} = {p!r}")
    print(f"   FROZEN: written to experiments/h18/ph38_p.json (sha256 {sha(PFILE)}); dev and eval read it")


# ------------------------------------------------------------------ read
def Phi(x): return 0.5*(1.0 + erf(x/sqrt(2.0)))


def load(task, arm, keys=None):
    Z = np.load(os.path.join(ARR, f"{task}_{arm}.npz")); return {k: Z[k] for k in (keys or Z.files)}


def flag(Z): return (Z["o_whiff"][-3:].sum(0) == 0).astype(float)     # ph12.py:164, per agent


def lastmean(Z): return Z["o_score"][-3:].mean(0)                       # ph12.last, per agent


def boot(x, idx):
    m = x[idx].mean(1); return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def paired_share(fa, fb, idx, label, P):
    """mean over agents of (fa - fb), bootstrap over agents; discordance b; pass probability (design section 7)"""
    d = fa - fb; dm = float(d.mean()); lo, hi = boot(d, idx); b = float((fa != fb).mean())
    var = b - dm**2
    pp = (Phi(dm/(sqrt(var)/sqrt(len(d))) - 1.96) if var > 0 else (1.0 if dm > 0 else 0.0))
    P(f"   {label}: d = {dm:+.4f} [{lo:+.4f}, {hi:+.4f}]  (n {len(d)}; {int(fa.sum())} vs {int(fb.sum())} flagged);"
      f" discordance b {b:.4f}; pass probability Phi(d/se - 1.96) = {pp:.4f}")
    return dict(d=dm, lo=lo, hi=hi, b=b, pass_prob=pp, na=int(fa.sum()), nb=int(fb.sum()))


def stage_read():
    header("read (bench)")
    def P(s=""): print(s)
    print("\nChoices where the registered text needed a reading in code (fixed before any output existed):")
    for ln in __doc__.split("Choices where")[1].split("\n")[2:]:
        if ln.strip(): print("  " + ln.strip())
    print("\n== logs of the earlier stages, embedded verbatim ==")
    for f in sorted(os.listdir(LOGS)):
        if not f.endswith(".txt"): continue
        p = os.path.join(LOGS, f)
        print(f"\n---- experiments/h18/logs_b/{f} (sha256 {sha(p)}) ----")
        print(open(p, encoding="utf-8").read().rstrip("\n"))
    meta = {}
    for task in TASKS:
        for arm in ARMS: meta[(task, arm)] = json.load(open(os.path.join(ARR, f"{task}_{arm}_meta.json")))
    print("\n== array files (kept local, not committed) ==")
    for (task, arm), m in meta.items(): print(f"   experiments/h18/arrays_b/{task}_{arm}.npz  {m['npz_bytes']} bytes  sha256 {m['npz_sha256']}")
    Pz = json.load(open(PFILE))
    print(f"   experiments/h18/ph38_p.json sha256 {sha(PFILE)}: p {Pz['p']!r}")
    SUM = dict(stage=STAGE, p=Pz, arrays={f"{t}_{a}": m["npz_sha256"] for (t, a), m in meta.items()})
    # (b1) identities
    print("\n== (b1) identities ==")
    I = {}
    hits = subprocess.run(["git", "grep", "-n", "ph38", "--", "src/"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8").stdout
    hits = [h for h in hits.splitlines() if not h.startswith("src/ph38.py")]
    pw = inspect.signature(ph11.World2.__init__).parameters["p_wind"].default
    same = ph16.World7.wind_on is ph11.World2.wind_on
    I["I-a"] = dict(grep_hits=hits, p_wind_default=pw, world7_uses_world2_wind_on=same, ok=(not hits and pw == 1.0 and same))
    print(f"   (I-a) `git grep -n ph38 -- src/` outside src/ph38.py: {len(hits)} hits {hits};"
          f" ph11.World2 p_wind default {pw} (ph11.py:59) and wind_on = rng.random(R) < p_wind (ph11.py:86);"
          f" ph16.World7.wind_on is ph11.World2.wind_on: {same} -> {'PASS' if I['I-a']['ok'] else 'FAIL'}")
    FIELDS = ("est", "head", "pos", "hit", "won", "clock", "turn")
    ok_b = {}
    for x, y in (("restart", "ring"), ("exact_restart", "exact")):
        A, B = load("K5a", x), load("K5a", y)
        ok_b[f"{x} == {y}"] = bool(all(np.array_equal(A[k], B[k]) for k in FIELDS + tuple("o_" + k for k in OKEYS))) and int(A["fired"].sum()) == 0
    I["I-b"] = ok_b
    print(f"   (I-b) K5(a), cue every step, every per-step field and every run2 key bitwise, no firing: {ok_b}")
    ok_c = {}
    for x, y in (("restart", "ring"), ("exact_restart", "exact")):
        A, B = load("K5b", x), load("K5b", y)
        fired = A["fired"].astype(bool); first = np.where(fired.any(0), fired.argmax(0), T)
        good = 0
        for r in range(R):
            t1 = first[r]
            if all(np.array_equal(A[k][:t1, r], B[k][:t1, r]) for k in FIELDS): good += 1
        ok_c[f"{x} == {y}"] = (good, R, int((first < T).sum()), [float(v) for v in np.percentile(first[first < T], (10, 50, 90))] if (first < T).any() else None)
    I["I-c"] = {k: dict(agents_equal=v[0], of=v[1], agents_firing=v[2], first_firing_p10_50_90=v[3]) for k, v in ok_c.items()}
    for k, v in ok_c.items():
        print(f"   (I-c) K5(b) {k} bitwise on every step before the agent's first firing (C6): {v[0]} of {v[1]} agents;"
              f" agents that fire {v[2]}, first firing step p10/50/90 {v[3]}")
    I["I-d_I-e"] = {f"{t}_{a}": meta[(t, a)]["bitwise_vs_run2"] for t in TASKS for a in ARMS if ARMS[a][1] == "off"}
    for k, v in I["I-d_I-e"].items():
        print(f"   (I-d)/(I-e) {k}: Nav5 rule off == ph12b.run2, all {len(v)} keys bitwise: {all(v.values())}")
    # (I-f) and (b2)
    A = load("K5b", "restart")
    hit, won, fired, clock = A["hit"].astype(bool), A["won"].astype(bool), A["fired"].astype(bool), A["clock"].astype(float)
    prev = np.vstack([np.ones((1, R), bool), won[:-1]]); ret = won & ~prev
    on_ret = bool(np.all(ret[fired])); exp = np.zeros(R, int); armed = np.zeros(R, bool)
    for t in range(T):
        e = ret[t] & armed & ~hit[t]; exp += e; armed = (armed | hit[t]) & ~e
    got = fired.sum(0)
    I["I-f"] = dict(all_on_cue_returns=on_ret, counts_equal=bool(np.array_equal(got, exp)))
    print(f"   (I-f) every firing on a cue-return step: {on_ret}; per agent, firings == first cue returns after a whiff with no whiff there"
          f" (recounted from the arrays): {I['I-f']['counts_equal']}")
    ids_ok = (I["I-a"]["ok"] and all(ok_b.values()) and all(v[0] == v[1] for v in ok_c.values())
              and all(all(v.values()) for v in I["I-d_I-e"].values()) and on_ret and I["I-f"]["counts_equal"])
    print(f"   identities: {'ALL PASS' if ids_ok else 'FAILED'}")
    SUM["identities"] = I; SUM["identities_ok"] = ids_ok
    print("\n== (b2) firings against cue returns, K5(b) `restart` ==")
    nret = ret.sum(0)
    prevclock = np.vstack([np.zeros((1, R)), clock[:-1]]) + 1.0
    cf = prevclock[fired]
    since = np.zeros(R); sf = []
    for t in range(T):
        since = np.where(hit[t], 0.0, since + 1.0)
        if fired[t].any(): sf.append(since[fired[t]])
    sf = np.concatenate(sf) if sf else np.zeros(0)
    q = lambda x, ps=(10, 50, 90): [float(v) for v in np.percentile(x, ps)] if len(x) else None
    B2 = dict(firings=int(fired.sum()), cue_returns=int(nret.sum()), per_agent_firings_q=q(got, (0, 10, 50, 90, 100)),
              per_agent_returns_q=q(nret, (0, 50, 100)), share_of_returns=float(fired.sum()/nret.sum()),
              clock_restarted_q=q(cf, (10, 25, 50, 75, 90, 100)), share_clock_over_50=float((cf > 50).mean()),
              lost_at_firing=int((sf > LOST).sum()))
    SUM["b2"] = B2
    print(f"   firings {B2['firings']} of {B2['cue_returns']} cue returns ({B2['share_of_returns']:.4f}); per agent firings min/p10/50/90/max"
          f" {B2['per_agent_firings_q']}; cue returns per agent min/50/max {B2['per_agent_returns_q']}")
    print(f"   clock restarted (C7) p10/25/50/75/90/max {B2['clock_restarted_q']}; share over 50 {B2['share_clock_over_50']:.4f};"
          f" firings with the agent lost (since > {LOST}) {B2['lost_at_firing']} of {len(sf)}")
    print(f"\n== (b3) p, frozen ==\n   p {Pz['p']!r} = {Pz['firings']} / {Pz['whiff_free']} (experiments/h18/ph38_p.json);"
          f" restart_rand fired {meta[('K5b', 'restart_rand')]['firings']} times on K5(b)")
    print("\n== (b4) reported ==\n   UNREADABLE as registered (C8): `restart` and `integrate` draw different turn noise from step 0"
          " (the ring draws from the agent generator, ph12.py:84), so the pair has diverged before any cue-off block ends.")
    Zr = load("K5b", "restart", ("hit", "pos")); Zi = load("K5b", "integrate", ("hit", "pos"))
    div = np.array([int(np.argmax(Zr["hit"][:, r] != Zi["hit"][:, r])) if (Zr["hit"][:, r] != Zi["hit"][:, r]).any() else T for r in range(R)])
    dpos = np.linalg.norm(Zr["pos"][1].astype(float) - Zi["pos"][1].astype(float), axis=1)
    print(f"   first step with differing whiff outcome p10/50/90 {q(div)}; position difference already at step 1: median {np.median(dpos):.4f}, max {dpos.max():.4f} units")
    SUM["b4"] = dict(unreadable=True, whiff_divergence_q=q(div), pos_diff_step1_median=float(np.median(dpos)))
    del Zr, Zi
    # criteria
    print("\n== bench readings: M0, M2, M3, M4, M5 (point estimates on the bench seeds; no verdict) ==")
    idx = np.random.default_rng(B_SEED).integers(0, R, size=(5000, R))
    OK_ = ["o_" + k for k in OKEYS]; Z = {a: load("K5b", a, OK_) for a in ("ring", "restart", "restart_rand", "exact", "exact_restart", "none")}
    med = lambda z: float(np.median(lastmean(z)))
    m0 = med(Z["exact"]) - med(Z["none"])
    print(f"   M0 exact - none, last-third median: {med(Z['exact']):.1f} - {med(Z['none']):.1f} = {m0:.1f} (>= 10: {m0 >= 10})")
    for a in ("ring", "restart", "restart_rand", "exact", "exact_restart", "none"):
        print(f"      {a:13s} last-third median {med(Z[a]):5.1f}, mean {lastmean(Z[a]).mean():5.2f}; late unrecovered {int(flag(Z[a]).sum())} of {R}"
              f" ({flag(Z[a]).mean()*100:.1f}%)")
    Zint = load("K5b", "integrate", OK_)
    print(f"      {'integrate':13s} last-third median {med(Zint):5.1f}, mean {lastmean(Zint).mean():5.2f}; late unrecovered {int(flag(Zint).sum())} of {R}")
    M2 = paired_share(flag(Z["ring"]), flag(Z["restart"]), idx, "M2 late unrecovered, ring - restart", P)
    d3 = lastmean(Z["restart"]) - lastmean(Z["ring"]); lo3, hi3 = boot(d3, idx)
    print(f"   M3 last-third mean, restart - ring: {d3.mean():+.3f} [{lo3:+.3f}, {hi3:+.3f}] (bar: lower bound > -1.0: {lo3 > -1.0}); paired sd {d3.std():.3f}")
    d4 = lastmean(Z["exact_restart"]) - lastmean(Z["exact"]); lo4, hi4 = boot(d4, idx)
    w4 = "lower bound > 0: the restart raises a perfect-heading agent's score (a body change)" if lo4 > 0 else \
         ("upper bound < 0: the restart costs a perfect-heading agent" if hi4 < 0 else "interval contains 0")
    print(f"   M4 last-third mean, exact_restart - exact: {d4.mean():+.3f} [{lo4:+.3f}, {hi4:+.3f}]; {w4} (reported, a wording rule)")
    M5 = paired_share(flag(Z["restart_rand"]), flag(Z["restart"]), idx, "M5 late unrecovered, restart_rand - restart", P)
    SUM["M"] = dict(M0=m0, M2=M2, M3=dict(d=float(d3.mean()), lo=lo3, hi=hi3, sd=float(d3.std())),
                    M4=dict(d=float(d4.mean()), lo=lo4, hi=hi4, wording=w4), M5=M5)
    print("\n== exposure ==")
    for task in TASKS:
        for a in ("ring", "restart", "restart_rand", "exact", "exact_restart", "none", "integrate"):
            z = load(task, a, ("pos_end", "src", "pos", "o_contact")); de = np.linalg.norm(z["pos_end"] - z["src"], axis=1)
            dm = np.linalg.norm(z["pos"].astype(float) - z["src"][None], axis=2).max(0)
            c = z["o_contact"].sum(0)
            print(f"   {task} {a:13s} distance at the end p10/50/90/max {' / '.join(f'{v:.1f}' for v in np.percentile(de, (10, 50, 90, 100)))};"
                  f" max over the run median {np.median(dm):.1f}; farther than 25 at the end {(de > 25).mean()*100:.1f}%;"
                  f" contacts per agent mean {c.mean():.2f}")
    print("\n== stop rules (h), design v2 section 4 ==")
    reasons = []
    if M2["d"] <= 0: reasons.append(f"M2 bench point estimate {M2['d']:+.4f} <= 0")
    if M2["pass_prob"] < 0.5: reasons.append(f"M2 pass probability at the bench d and b {M2['pass_prob']:.4f} < 0.5")
    if M5["d"] <= 0: reasons.append(f"M5 bench point estimate {M5['d']:+.4f} <= 0")
    if not ids_ok: reasons.append("an identity failed (implementation error)")
    for r in reasons: print(f"   - {r}")
    decision = "STOP: stopped at the bench" if reasons else "CONTINUE to development"
    print(f"   {decision}")
    SUM["stop"] = dict(decision=decision, reasons=reasons)
    json.dump(SUM, open(os.path.join(OUT, "ph38_bench_summary.json"), "w", newline="\n"), indent=1, default=float)
    print("\n   wrote experiments/h18/ph38_bench_summary.json")


if __name__ == "__main__":
    args = sys.argv[1:]
    os.makedirs(ARR, exist_ok=True); os.makedirs(LOGS, exist_ok=True)
    st = args[0] if args else "demo"
    if st == "demo": stage_demo()
    elif st == "arm" and len(args) > 2 and args[1] in TASKS and args[2] in ARMS: stage_arm(args[1], args[2])
    elif st == "calib": stage_calib()
    elif st == "read": stage_read()
    else: print(__doc__); sys.exit(1)
