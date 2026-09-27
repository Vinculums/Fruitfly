#!/usr/bin/env python3
"""H10 Stage A: a confidence gate on the H9 graded selector (design v2 FINAL, experiments/h10/h10_design_v2.md).

Usage (one job at a time, BLAS pinned to one thread, in the local session; no GitHub Actions):
  python src/h10.py demo                              > experiments/h10/h10_demo.txt
  python src/h10.py repro                             > experiments/h10/repro/stdout.log
  python src/h10.py calibration --out experiments/h10/calibration  > experiments/h10/calibration/stdout.log
  python src/h10.py freeze                            > experiments/h10/freeze.log
  python src/h10.py development --out experiments/h10/development  > experiments/h10/development/stdout.log
  python src/h10.py evaluation --out experiments/h10/evaluation    > experiments/h10/evaluation/stdout.log

What this file is, read against the design:
  R1  ph7.UP, ph7.ChanDiv (through ph7.Graded, J 1.2, c 0.5, every other default), ph7.Bistable and ph7.committed are
      imported and used unchanged; ph7.py and ph2.py are not edited (their sha256 is printed and checked).
  R2  The candidate (section 3) is class H10: a ph7.Graded instance stepped as ph7.Graded.step does (up.step, then c.step),
      plus the evidence traces e for the three tau_e, updated every step including silence. The nine (tau_e, theta)
      settings share one graded trajectory: the gate consumes no randomness and never touches the state (design 2.4), so
      computing the nine gates on one trajectory is exact. The forced-open arm (4) is that object's own raw identity and is
      compared bitwise, every step, with the separately constructed and separately stepped arm 2.
  R3  Arm 6, the simple mask, is a read-out on arm 2's graded state (q on s >= theta_m); it has no state of its own.
  R4  Every arm is built with its own generator from the condition's child 2, so every arm draws the identical internal
      noise (one standard_normal((rows, 5)) per step in both circuits). Inputs are one tape per condition, shared.
  R5  Input construction follows ph7.cue_phase, ph7.pulse and ph7.blank in the same order of floating operations, so the
      harness on ph7's own generators reproduces ph7's counts (section 8.1). Targets: 80 per identity, permuted by child 0.
  R6  A read point 'step k' is the output after k steps. Every primary rate uses all assigned rows.
  R7  Wilson 95% (z 1.959964) for single proportions; paired percentile bootstrap, 5000 row resamples, one index matrix
      default_rng(bootstrap).integers(0, 400, size=(5000, 400)) per stage, for differences.
  R8  Selection (8.2): first H10 setting passing every criterion, tau_e ascending then theta ascending; first arm-6 theta_m
      passing, ascending. No H10 setting passing -> NOT SHOWN, stop. A passing control never rescues H10.
  R9  The freeze (8.3) records this file's sha256; development and evaluation refuse to run if it has changed.
  R10 Disclosed fix before any registered seed: the first `repro` run printed no_reset_input False because the check
      searched the whole H10 class source and matched the word 'reset' in its docstring. The check now reads the code of
      H10.__init__, H10.step, H10.gates and run (the only places a reset could be passed). No model code changed; every
      count in that first run equals the recorded one.
"""
import argparse
import hashlib
import inspect
import json
import platform
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import ph7                                                     # noqa: E402  (unchanged)

sys.stdout.reconfigure(newline="\n")  # LF output, so the recorded sha256 equals the committed blob

DESIGN = ROOT / "experiments/h10/h10_design_v2.md"
FREEZE = ROOT / "experiments/h10/freeze.json"
N, J, C = 5, 1.2, 0.5
TAUS = (40, 80, 160)
THETAS = (0.004, 0.008, 0.016)
MASK_THETAS = (0.02, 0.05, 0.10)
SETTINGS = [(tau, th) for tau in TAUS for th in THETAS]           # the fixed selection order
U_WRONG = 0.04
BARS = dict(acquisition=0.90, retention=0.90, revision=0.85, distractor=0.90, idle=0.98, anti_trivial=-0.05,
            added_value=0.05)
Z = 1.959964
NBOOT, ROWS = 5000, 400
PERM = np.array([2, 4, 0, 3, 1])                                  # fixed channel permutation for the equivariance check
PERM_ROWS = 40
SCALES = (0.25, 0.5, 1.0, 2.0, 4.0)
HARD = dict(d=0.05, noise_sd=0.3, cue=300, blank=300)
EASY = dict(d=0.4, noise_sd=0.3, x0=1.0, cue=100)

SEEDS = {
    "calibration": dict(hard_0p25=45101, hard_0p5=45102, hard_1=45103, hard_2=45104, hard_4=45105, easy=45106,
                        revision=45107, distractor=45108, idle=45109, ambiguous=45110, bootstrap=45111),
    "development": dict(hard_0p25=45201, hard_0p5=45202, hard_1=45203, hard_2=45204, hard_4=45205, easy=45206,
                        revision=45207, distractor=45208, idle=45209, ambiguous=45210, bootstrap=45211),
    "evaluation": dict(hard_0p25=45301, hard_0p5=45302, hard_1=45303, hard_2=45304, hard_4=45305, easy=45306,
                       revision=45307, distractor=45308, idle=45309, ambiguous=45310, bootstrap=45311),
}
HARD_KEYS = dict(zip(SCALES, ("hard_0p25", "hard_0p5", "hard_1", "hard_2", "hard_4")))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def say(*a):
    print(*a, flush=True)


def note(*a):
    print(*a, file=sys.stderr, flush=True)


def sname(tau, th):
    return f"h10_tau{tau}_th{th}"


def mname(th):
    return f"mask_{th}"


# ---------------------------------------------------------------- the candidate (design section 3)
class H10:
    """ph7.Graded (J 1.2, c 0.5, unchanged) plus the evidence traces e and the gate. No reset, no label, no clock."""

    def __init__(self, runs, rng):
        self.g = ph7.Graded(runs, rng=rng, J=J, c=C)
        self.e = np.zeros((len(TAUS), runs, N))

    def step(self, x):
        y = self.g.up.step(x)                     # ph7.Graded.step is c.step(up.step(x)); split only to read y
        s = self.g.c.step(y)
        for k, tau in enumerate(TAUS):
            self.e[k] = (1 - 1 / tau) * self.e[k] + y / tau
        return s

    def gates(self):
        """bool (len(TAUS), len(THETAS), runs): (sum(e) > 1e-6) and (q >= theta); q = (1st - 2nd) / (sum + 1e-12)."""
        srt = np.sort(self.e, axis=2)
        tot = self.e.sum(2)
        q = (srt[:, :, -1] - srt[:, :, -2]) / (tot + 1e-12)
        th = np.asarray(THETAS)[None, :, None]
        return (tot[:, None, :] > 1e-6) & (q[:, None, :] >= th), q, tot

    def leaders(self, tot):
        lead = self.e.argmax(2)
        return np.where(tot > 0, lead, -1)


def state_q(s):
    srt = np.sort(s, axis=1)
    return (srt[:, -1] - srt[:, -2]) / (s.sum(1) + 1e-12)


def multi_active(s):
    return (s > ph7.HOLD).sum(1) > 1


class TapeRNG:
    """feeds a pre-drawn internal-noise tape, one (rows, 5) slice per standard_normal call (permutation check only)."""

    def __init__(self, tape):
        self.tape, self.t = tape, 0

    def standard_normal(self, shape):
        z = self.tape[self.t]
        self.t += 1
        if z.shape != tuple(shape):
            raise RuntimeError(f"tape shape {z.shape} != {shape}")
        return z


# ---------------------------------------------------------------- conditions and tapes (design section 5)
def cue_steps(rows, tgt, rng, steps, d, x0, noise_sd):
    """ph7.cue_phase's input, in its order of floating operations."""
    idx = np.arange(rows)
    out = []
    for _ in range(steps):
        x = np.full((rows, N), float(x0))
        x[idx, tgt] += d * x0
        x += noise_sd * x0 * rng.standard_normal((rows, N))
        out.append(x)
    return out


def blank_steps(rows, steps):
    return [np.zeros((rows, N)) for _ in range(steps)]


def pulse_steps(rows, chan, amp, steps):
    idx = np.arange(rows)
    out = []
    for _ in range(steps):
        x = np.zeros((rows, N))
        x[idx, chan] = amp
        out.append(x)
    return out


def build(kind, rows, tgt, in_rng, x0=1.0):
    """input tape (T, rows, 5) and read points for one condition."""
    if kind == "hard":
        tape = cue_steps(rows, tgt, in_rng, HARD["cue"], HARD["d"], x0, HARD["noise_sd"]) + blank_steps(rows, HARD["blank"])
        reads = dict(cue_end=300, final=600)
    elif kind == "easy":
        tape = cue_steps(rows, tgt, in_rng, EASY["cue"], EASY["d"], EASY["x0"], EASY["noise_sd"]) + blank_steps(rows, 300)
        reads = dict(acq=100, hold=400)
    elif kind in ("revision", "distractor"):
        steps, tail = (100, 50) if kind == "revision" else (20, 230)
        tape = (cue_steps(rows, tgt, in_rng, EASY["cue"], EASY["d"], EASY["x0"], EASY["noise_sd"]) + blank_steps(rows, 50)
                + pulse_steps(rows, (tgt + 1) % N, 2.0, steps) + blank_steps(rows, tail))
        reads = dict(pre=150, final=300 if kind == "revision" else 400)
    elif kind == "idle":
        tape = blank_steps(rows, 400)
        reads = dict(final=400)
    elif kind == "ambiguous":
        tape = cue_steps(rows, tgt, in_rng, 300, 0.0, 1.0, 0.3) + blank_steps(rows, 300)
        reads = dict(final=600)
    else:
        raise ValueError(kind)
    return np.asarray(tape), reads


def balanced_targets(ss_child, rows=ROWS):
    return np.random.default_rng(ss_child).permutation(np.repeat(np.arange(N), rows // N))


# ---------------------------------------------------------------- the engine
def stream_names():
    return (["bistable", "graded", "open", "closed"] + [sname(t, h) for t, h in SETTINGS]
            + [mname(h) for h in MASK_THETAS])


def run(tape, rng_factory, keep_rows=0):
    """step every arm over one tape. Returns output streams (T, rows) int8 per arm, gates, leaders, q at every step for
    the three tau_e, identity flags, and (if keep_rows) the first keep_rows rows' states for the equivariance check."""
    T, rows, _ = tape.shape
    bist = ph7.Bistable(rows, rng=rng_factory())
    grad = ph7.Graded(rows, rng=rng_factory(), J=J, c=C)
    cand = H10(rows, rng=rng_factory())
    names = stream_names()
    out = {n: np.empty((T, rows), np.int8) for n in names}
    gate = np.empty((len(TAUS), len(THETAS), T, rows), bool)
    lead = np.empty((len(TAUS), T, rows), np.int8)
    qe = np.empty((len(TAUS), T, rows), np.float32)
    multi = {"bistable": np.empty((T, rows), bool), "graded": np.empty((T, rows), bool)}
    ident_state, finite = True, True
    kept = {a: np.empty((T, keep_rows, N)) for a in ("bistable", "graded", "cand")} if keep_rows else None
    for t in range(T):
        x = tape[t]
        bist.step(x)
        grad.step(x)
        cand.step(x)
        sb, sg, sc = bist.memory(), grad.memory(), cand.g.memory()
        ident_state &= bool(np.array_equal(sc, sg))
        finite &= bool(np.isfinite(sb).all() and np.isfinite(sg).all() and np.isfinite(cand.e).all())
        rb, rg, rc = ph7.committed(bist), ph7.committed(grad), ph7.committed(cand.g)
        g, q, tot = cand.gates()
        out["bistable"][t], out["graded"][t], out["open"][t], out["closed"][t] = rb, rg, rc, -1
        for i, (tau, th) in enumerate(SETTINGS):
            k, j = TAUS.index(tau), THETAS.index(th)
            out[sname(tau, th)][t] = np.where(g[k, j], rc, -1)
        qs = state_q(sg)
        for th in MASK_THETAS:
            out[mname(th)][t] = np.where(qs >= th, rg, -1)
        gate[:, :, t] = g
        lead[:, t] = cand.leaders(tot)
        qe[:, t] = q
        multi["bistable"][t], multi["graded"][t] = multi_active(sb), multi_active(sg)
        if keep_rows:
            kept["bistable"][t], kept["graded"][t], kept["cand"][t] = sb[:keep_rows], sg[:keep_rows], sc[:keep_rows]
    return dict(out=out, gate=gate, lead=lead, q=qe, multi=multi, ident_state=ident_state, finite=finite, kept=kept)


def perm_check(tape, noise_tape, main):
    """design section 7, implementation: on the first PERM_ROWS rows, permuting the channels of the input and the
    internal-noise tapes permutes the states (within 1e-12) and the outputs (exactly). Also checks that the unpermuted
    PERM_ROWS-row run equals the main run's first rows bitwise (row independence and tape equivalence)."""
    r = PERM_ROWS
    x0, n0 = tape[:, :r], noise_tape[:, :r]
    plain = run(x0, lambda: TapeRNG(n0), keep_rows=r)
    permd = run(x0[:, :, PERM], lambda: TapeRNG(n0[:, :, PERM]), keep_rows=r)
    inv = np.argsort(PERM)
    res = dict(rows=r, perm=PERM.tolist())
    res["plain_equals_main_states"] = all(bool(np.array_equal(plain["kept"][a], main["kept"][a])) for a in plain["kept"])
    res["plain_equals_main_outputs"] = all(bool(np.array_equal(plain["out"][n], main["out"][n][:, :r]))
                                           for n in plain["out"])
    dev = {a: float(np.abs(permd["kept"][a] - plain["kept"][a][:, :, PERM]).max()) for a in plain["kept"]}
    res["max_state_deviation"] = dev
    ok_out = {}
    for n in plain["out"]:
        o = plain["out"][n].astype(int)
        mapped = np.where(o >= 0, inv[np.clip(o, 0, N - 1)], -1)
        ok_out[n] = bool(np.array_equal(permd["out"][n], mapped))
    res["outputs_permute_exactly"] = ok_out
    res["ok"] = (res["plain_equals_main_states"] and res["plain_equals_main_outputs"]
                 and all(v <= 1e-12 for v in dev.values()) and all(ok_out.values()))
    return res


# ---------------------------------------------------------------- statistics (design section 7)
def wilson(k, n):
    p = k / n
    centre = (p + Z * Z / (2 * n)) / (1 + Z * Z / n)
    half = Z * np.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / (1 + Z * Z / n)
    return float(centre - half), float(centre + half)


def boot(diff, draws):
    vals = np.asarray(diff, float)[draws].mean(1)
    return [float(np.percentile(vals, q)) for q in (2.5, 97.5)]


def at(res, name, k):
    return res["out"][name][k - 1].astype(int)


def evaluate(stage, name, draws):
    """the registered criteria for one output stream (an H10 setting or an arm-6 threshold)."""
    c = {}
    e, tgt = stage["easy"], stage["easy"]["tgt"]
    ok = at(e, name, 100) == tgt
    k = int(ok.sum())
    c["acquisition"] = dict(k=k, n=ROWS, ci=wilson(k, ROWS), bar=BARS["acquisition"])
    c["acquisition"]["pass"] = c["acquisition"]["ci"][0] >= BARS["acquisition"]
    ok = (at(e, name, 100) == tgt) & (at(e, name, 400) == tgt)
    k = int(ok.sum())
    c["retention"] = dict(k=k, n=ROWS, ci=wilson(k, ROWS), bar=BARS["retention"])
    c["retention"]["pass"] = c["retention"]["ci"][0] >= BARS["retention"]
    r, tgt_r = stage["revision"], stage["revision"]["tgt"]
    ok = (at(r, name, 150) == tgt_r) & (at(r, name, 300) == (tgt_r + 1) % N)
    k = int(ok.sum())
    c["revision"] = dict(k=k, n=ROWS, ci=wilson(k, ROWS), bar=BARS["revision"])
    c["revision"]["pass"] = c["revision"]["ci"][0] >= BARS["revision"]
    d, tgt_d = stage["distractor"], stage["distractor"]["tgt"]
    ok = (at(d, name, 150) == tgt_d) & (at(d, name, 400) == tgt_d)
    k = int(ok.sum())
    c["distractor"] = dict(k=k, n=ROWS, ci=wilson(k, ROWS), bar=BARS["distractor"])
    c["distractor"]["pass"] = c["distractor"]["ci"][0] >= BARS["distractor"]
    idle = stage["idle"]["out"][name]
    k = int((idle == -1).all(0).sum())
    c["idle"] = dict(k=k, n=ROWS, ci=wilson(k, ROWS), bar=BARS["idle"])
    c["idle"]["pass"] = c["idle"]["ci"][0] >= BARS["idle"]
    c["hard"] = {}
    for x0 in SCALES:
        h, tgt_h = stage[HARD_KEYS[x0]], stage[HARD_KEYS[x0]]["tgt"]
        o, ob = at(h, name, 600), at(h, "bistable", 600)
        wrong = (o >= 0) & (o != tgt_h)
        kw = int(wrong.sum())
        cor, corb = (o == tgt_h).astype(float), (ob == tgt_h).astype(float)
        cell = dict(correct=int((o == tgt_h).sum()), wrong=kw, abstain=int((o == -1).sum()),
                    wrong_ci=wilson(kw, ROWS), wrong_pass=wilson(kw, ROWS)[1] <= U_WRONG,
                    bistable_correct=int(corb.sum()), anti_trivial_point=float((cor - corb).mean()),
                    anti_trivial_ci=boot(cor - corb, draws))
        cell["anti_trivial_pass"] = cell["anti_trivial_ci"][0] >= BARS["anti_trivial"]
        o300 = at(h, name, 300)
        cell["cue_end_300"] = dict(correct=int((o300 == tgt_h).sum()), wrong=int(((o300 >= 0) & (o300 != tgt_h)).sum()),
                                   abstain=int((o300 == -1).sum()))
        c["hard"][str(x0)] = cell
    h, tgt_h = stage["hard_1"], stage["hard_1"]["tgt"]
    o, og = at(h, name, 600), at(h, "graded", 600)
    w, wg = ((o >= 0) & (o != tgt_h)).astype(float), ((og >= 0) & (og != tgt_h)).astype(float)
    c["added_value"] = dict(point=float((wg - w).mean()), ci=boot(wg - w, draws), bar=BARS["added_value"])
    c["added_value"]["pass"] = c["added_value"]["ci"][0] >= BARS["added_value"]
    c["hard_wrong_all_pass"] = all(v["wrong_pass"] for v in c["hard"].values())
    c["anti_trivial_all_pass"] = all(v["anti_trivial_pass"] for v in c["hard"].values())
    c["science_pass"] = bool(c["acquisition"]["pass"] and c["retention"]["pass"] and c["revision"]["pass"]
                             and c["distractor"]["pass"] and c["idle"]["pass"] and c["hard_wrong_all_pass"]
                             and c["anti_trivial_all_pass"] and c["added_value"]["pass"])
    return c


def conditional(stage, name):
    """Phase 7.1's six readings (record:phase7-1-success-criteria) on this stage's rows, reported, not gating."""
    e, t = stage["easy"], stage["easy"]["tgt"]
    b, a = at(e, name, 100), at(e, name, 400)
    d2 = (int(((b >= 0) & (a == b)).sum()), int((b >= 0).sum()))
    r, tr = stage["revision"], stage["revision"]["tgt"]
    b, a = at(r, name, 150), at(r, name, 300)
    d3 = (int(((b >= 0) & (a == (tr + 1) % N)).sum()), int((b >= 0).sum()))
    d, td = stage["distractor"], stage["distractor"]["tgt"]
    b, a = at(d, name, 150), at(d, name, 400)
    d4 = (int(((b >= 0) & (a == b)).sum()), int((b >= 0).sum()))
    h, th = stage["hard_1"], stage["hard_1"]["tgt"]
    o = at(h, name, 600)
    d1 = (int((o == th).sum()), int(((o >= 0) & (o != th)).sum()), int((o == -1).sum()))
    d5 = [int(((at(stage[HARD_KEYS[x0]], name, 600) >= 0)
               & (at(stage[HARD_KEYS[x0]], name, 600) != stage[HARD_KEYS[x0]]["tgt"])).sum()) for x0 in SCALES]
    d6 = int((stage["idle"]["out"][name][-1] == -1).sum())
    return dict(d1_cwa=d1, d2=d2, d3=d3, d4=d4, d6=d6, d5=d5)


def events(res, name, tgt=None):
    """step-by-step event counts for one stream (design section 6): output changes, A->B with and without an
    intervening abstention, and (revision) the time to revision, censored at the final read."""
    o = res["out"][name].astype(int)
    ch = int((o[1:] != o[:-1]).sum())
    out = dict(changes=ch)
    if tgt is not None:
        B = (tgt + 1) % N
        direct = ((o[:-1] == tgt) & (o[1:] == B)).sum(0)
        via = np.zeros(o.shape[1], int)
        last = np.full(o.shape[1], -2)
        for t in range(o.shape[0]):
            v = o[t]
            nz = v >= 0
            via += (nz & (v == B) & (last == tgt) & (o[t - 1] == -1) if t else 0)
            last = np.where(nz, v, last)
        out.update(a_to_b_direct=int(direct.sum()), a_to_b_via_abstention=int(via.sum()))
    return out


# ---------------------------------------------------------------- a stage
def run_stage(stage_name, seeds=None, historical=False):
    """run every condition of one stage. historical=True: ph7's own generators and 200 rows (section 8.1)."""
    rows = ph7.R if historical else ROWS
    stage = {}
    kinds = [(HARD_KEYS[x0], "hard", x0) for x0 in SCALES] + [("easy", "easy", 1.0), ("revision", "revision", 1.0),
                                                              ("distractor", "distractor", 1.0), ("idle", "idle", 1.0),
                                                              ("ambiguous", "ambiguous", 1.0)]
    for key, kind, x0 in kinds:
        note(f"  {stage_name}: {key}")
        if historical:
            tgt = ph7.targets() if kind != "idle" else None
            in_rng = np.random.default_rng(7)
            factory = lambda: np.random.default_rng(0)                                  # noqa: E731
            noise_src = lambda: np.random.default_rng(0)                                # noqa: E731
        else:
            ch = np.random.SeedSequence(seeds[key]).spawn(3)
            tgt = balanced_targets(ch[0]) if kind != "idle" else None
            in_rng = np.random.default_rng(ch[1])
            factory = lambda ch=ch: np.random.default_rng(ch[2])                        # noqa: E731
            noise_src = factory
        tape, reads = build(kind, rows, tgt if tgt is not None else np.zeros(rows, int), in_rng, x0)
        res = run(tape, factory, keep_rows=PERM_ROWS)
        src = noise_src()
        noise_tape = np.asarray([src.standard_normal((rows, N)) for _ in range(len(tape))])
        res["perm"] = perm_check(tape, noise_tape, res)
        res.update(tgt=tgt, reads=reads, kind=kind, x0=x0, rows=rows, T=len(tape))
        stage[key] = res
    return stage


def implementation(stage):
    ok = {}
    ok["open_equals_graded_state_bitwise"] = all(r["ident_state"] for r in stage.values())
    ok["open_equals_graded_output"] = all(bool(np.array_equal(r["out"]["open"], r["out"]["graded"])) for r in stage.values())
    ok["closed_always_abstains"] = all(bool((r["out"]["closed"] == -1).all()) for r in stage.values())
    src_b = inspect.getsource(ph7.Bistable.step)
    ok["no_reset_input"] = ("reset=0.0" in src_b and "reset" not in inspect.signature(ph7.ChanDiv.step).parameters
                            and not any("reset" in inspect.getsource(f) for f in (H10.__init__, H10.step, H10.gates, run)))
    ok["label_permutation_equivariance"] = all(r["perm"]["ok"] for r in stage.values())
    ok["finite_states"] = all(r["finite"] for r in stage.values())
    ok["complete_rows"] = all(all(v.shape == (r["T"], r["rows"]) for v in r["out"].values()) for r in stage.values())
    ok["all"] = all(ok.values())
    return ok


def fmt_ci(ci):
    return f"[{ci[0]:.4f}, {ci[1]:.4f}]"


def print_stage(stage, draws, label):
    say(f"\n== {label}: arms 1 and 2, raw counts (correct / wrong / abstain) ==")
    for key in [HARD_KEYS[x0] for x0 in SCALES] + ["ambiguous"]:
        r = stage[key]
        for arm in ("bistable", "graded"):
            o = at(r, arm, 600)
            multi = int(r["multi"][arm][599].sum())
            say(f"  {key:10s} {arm:9s} step 600: {int((o == r['tgt']).sum()):3d} / {int(((o >= 0) & (o != r['tgt'])).sum()):3d}"
                f" / {int((o == -1).sum()):3d}   multi-active {multi}")
    r = stage["ambiguous"]
    for arm in ["bistable", "graded"] + [sname(t, h) for t, h in SETTINGS]:
        o = at(r, arm, 600)
        say(f"  ambiguous {arm:18s} identities at 600: " + " ".join(f"{i}:{int((o == i).sum())}" for i in range(N))
            + f"  abstain {int((o == -1).sum())}")
    say(f"\n== {label}: implementation ==")
    imp = implementation(stage)
    for k, v in imp.items():
        say(f"  {k:36s} {v}")
    for key, r in stage.items():
        p = r["perm"]
        say(f"  perm {key:10s} ok {p['ok']}  max state deviation "
            + ", ".join(f"{a} {v:.2e}" for a, v in p["max_state_deviation"].items())
            + f"  plain==main {p['plain_equals_main_states'] and p['plain_equals_main_outputs']}")
    table = {}
    say(f"\n== {label}: registered criteria (all rows; Wilson 95%; paired bootstrap 5000) ==")
    for name in [sname(t, h) for t, h in SETTINGS] + [mname(h) for h in MASK_THETAS]:
        c = evaluate(stage, name, draws)
        table[name] = c
        say(f"  {name}")
        for k in ("acquisition", "retention", "revision", "distractor", "idle"):
            v = c[k]
            say(f"    {k:12s} {v['k']:3d}/400 {fmt_ci(v['ci'])} lower >= {v['bar']:.2f}: {'PASS' if v['pass'] else 'FAIL'}")
        for x0 in SCALES:
            v = c["hard"][str(x0)]
            say(f"    hard x0 {x0:<4} c/w/a {v['correct']:3d}/{v['wrong']:3d}/{v['abstain']:3d}"
                f"  wrong {fmt_ci(v['wrong_ci'])} upper <= {U_WRONG}: {'PASS' if v['wrong_pass'] else 'FAIL'}"
                f"  | vs bistable ({v['bistable_correct']}) {v['anti_trivial_point']:+.4f} {fmt_ci(v['anti_trivial_ci'])}"
                f" lower >= -0.05: {'PASS' if v['anti_trivial_pass'] else 'FAIL'}"
                f"  | at 300 {v['cue_end_300']['correct']}/{v['cue_end_300']['wrong']}/{v['cue_end_300']['abstain']}")
        v = c["added_value"]
        say(f"    added value (arm 2 wrong - this wrong, x0 1) {v['point']:+.4f} {fmt_ci(v['ci'])} lower >= +0.05:"
            f" {'PASS' if v['pass'] else 'FAIL'}")
        say(f"    -> every scientific criterion: {'PASS' if c['science_pass'] else 'not all pass'}")
    say(f"\n== {label}: Phase 7.1's six readings, as defined there (reported, not gating) ==")
    six = {}
    for name in ["bistable", "graded"] + [sname(t, h) for t, h in SETTINGS] + [mname(h) for h in MASK_THETAS]:
        s6 = conditional(stage, name)
        six[name] = s6
        say(f"  {name:20s} D1 c/w/a {s6['d1_cwa'][0]}/{s6['d1_cwa'][1]}/{s6['d1_cwa'][2]}  D2 {s6['d2'][0]}/{s6['d2'][1]}"
            f"  D3 {s6['d3'][0]}/{s6['d3'][1]}  D4 {s6['d4'][0]}/{s6['d4'][1]}  D6 {s6['d6']}  D5 {s6['d5']}")
    say(f"\n== {label}: logged events (sums over rows) ==")
    logs = {}
    for key, r in stage.items():
        tgt = r["tgt"] if key in ("revision", "distractor") else None
        row = {}
        for name in ["bistable", "graded"] + [sname(t, h) for t, h in SETTINGS]:
            row[name] = events(r, name, tgt)
        for k, tau in enumerate(TAUS):
            g = r["gate"][k]
            row[f"gate_tau{tau}"] = {str(th): dict(openings=int((g[j, 1:] & ~g[j, :-1]).sum()),
                                                   closings=int((~g[j, 1:] & g[j, :-1]).sum()))
                                     for j, th in enumerate(THETAS)}
            raw = r["out"]["open"]
            dis = (raw >= 0) & (r["lead"][k] >= 0) & (r["lead"][k] != raw)
            row[f"disagree_tau{tau}"] = dict(steps=int(dis.sum()), rows=int(dis.any(0).sum()))
        logs[key] = row
        say(f"  {key:10s} raw graded changes {row['graded']['changes']}; e-leader vs raw disagreement rows "
            + ", ".join(f"tau {tau} {row[f'disagree_tau{tau}']['rows']}" for tau in TAUS)
            + ("; A->B direct / via abstention: " + ", ".join(
                f"{n.replace('h10_', '')} {row[n]['a_to_b_direct']}/{row[n]['a_to_b_via_abstention']}"
                for n in ["graded"] + [sname(t, h) for t, h in SETTINGS]) if tgt is not None else ""))
    r = stage["revision"]
    b = (r["tgt"] + 1) % N
    for name in ["graded"] + [sname(t, h) for t, h in SETTINGS]:
        o = r["out"][name][150:300].astype(int)
        hit = (o == b[None, :])
        first = np.where(hit.any(0), hit.argmax(0) + 151, -1)
        rev = first[first > 0]
        say(f"  revision time to B ({name}): revised {len(rev)}/400, steps after challenge onset median "
            f"{(np.median(rev) - 150) if len(rev) else float('nan')}, censored {int((first < 0).sum())}")
    return imp, table, six, logs


def select(table):
    chosen = next((f"{sname(t, h)}" for t, h in SETTINGS if table[sname(t, h)]["science_pass"]), None)
    mask = next((mname(h) for h in MASK_THETAS if table[mname(h)]["science_pass"]), None)
    return chosen, mask


def save(stage, out_dir, summary):
    out_dir.mkdir(parents=True, exist_ok=True)
    arrays = {}
    for key, r in stage.items():
        for n, v in r["out"].items():
            arrays[f"{key}/out/{n}"] = v
        arrays[f"{key}/gate"] = r["gate"]
        arrays[f"{key}/lead"] = r["lead"]
        arrays[f"{key}/q_at_reads"] = np.stack([r["q"][:, k - 1] for k in r["reads"].values()], 1)
        if r["tgt"] is not None:
            arrays[f"{key}/targets"] = r["tgt"]
    np.savez_compressed(out_dir / "trace.npz", **arrays)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8", newline="\n")
    say(f"\nwrote {out_dir.relative_to(ROOT).as_posix()}/trace.npz sha256 {sha(out_dir / 'trace.npz')}")
    say(f"wrote {out_dir.relative_to(ROOT).as_posix()}/summary.json sha256 {sha(out_dir / 'summary.json')}")


def header(what):
    say(f"H10 Stage A ({what}); design {DESIGN.relative_to(ROOT).as_posix()} sha256 {sha(DESIGN)}")
    say(f"src/h10.py sha256 {sha(__file__)}")
    say(f"src/ph7.py sha256 {sha(HERE / 'ph7.py')}  src/ph2.py sha256 {sha(HERE / 'ph2.py')}")
    say(f"python {sys.version.split()[0]}  numpy {np.__version__}  platform {platform.platform()}")


# ---------------------------------------------------------------- section 8.1: the harness on ph7's own generators
PH7_RECORDED = {  # experiments/h09/ph7_h9.txt, the control block and the J 1.2 c 0.5 gate block
    "bistable": dict(d1_cwa=(121, 4, 75), d2=(200, 200), d3=(0, 200), d4=(200, 200), d6=200, d5=[3, 4, 4, 4, 5]),
    "graded": dict(d1_cwa=(156, 44, 0), d2=(200, 200), d3=(200, 200), d4=(200, 200), d6=200, d5=[61, 47, 44, 45, 45]),
}


def ph7_direct():
    """ph7's own functions, called unchanged, for arms 1 and 2."""
    mk = {"bistable": lambda: ph7.Bistable(ph7.R, rng=np.random.default_rng(0)),
          "graded": lambda: ph7.Graded(ph7.R, rng=np.random.default_rng(0), J=J, c=C)}
    out = {}
    for arm, f in mk.items():
        out[arm] = dict(d1_cwa=ph7.d1_d5(f), d2=ph7.d2_hold(f), d3=ph7.d3_revise(f), d4=ph7.d4_distractor(f),
                        d6=ph7.d6_idle(f), d5=ph7.d5_scale(f))
    return out


def norm6(d):
    return dict(d1_cwa=list(d["d1_cwa"]), d2=list(d["d2"]), d3=list(d["d3"]), d4=list(d["d4"]), d6=d["d6"], d5=list(d["d5"]))


def repro(quiet=False):
    direct = ph7_direct()
    stage = run_stage("repro", historical=True)
    harness = {arm: conditional(stage, arm) for arm in ("bistable", "graded")}
    ok = all(norm6(harness[a]) == norm6(direct[a]) == norm6(PH7_RECORDED[a]) for a in ("bistable", "graded"))
    return ok, direct, harness, stage


def cmd_repro(args):
    header("section 8.1 step 2: the harness on ph7's own generators, 200 rows")
    ok, direct, harness, stage = repro()
    say("\n== ph7's D1-D6 counts: recorded (ph7_h9.txt) / ph7 functions called now / this harness ==")
    for arm in ("bistable", "graded"):
        say(f"  {arm}")
        for k in ("d1_cwa", "d2", "d3", "d4", "d6", "d5"):
            say(f"    {k:6s} {PH7_RECORDED[arm][k]!s:22s} {direct[arm][k]!s:22s} {harness[arm][k]!s:22s}")
    say(f"  reproduced: {ok}")
    imp = implementation(stage)
    say("\n== implementation checks on the historical cells ==")
    for k, v in imp.items():
        say(f"  {k:36s} {v}")
    for key, r in stage.items():
        p = r["perm"]
        say(f"  perm {key:10s} ok {p['ok']}  max state deviation "
            + ", ".join(f"{a} {v:.2e}" for a, v in p["max_state_deviation"].items()))
    say("\n== the candidate and the mask on the same 200-row historical cells: Phase 7.1's six readings (reported) ==")
    for name in [sname(t, h) for t, h in SETTINGS] + [mname(h) for h in MASK_THETAS]:
        s6 = conditional(stage, name)
        say(f"  {name:20s} D1 c/w/a {s6['d1_cwa'][0]}/{s6['d1_cwa'][1]}/{s6['d1_cwa'][2]}  D2 {s6['d2'][0]}/{s6['d2'][1]}"
            f"  D3 {s6['d3'][0]}/{s6['d3'][1]}  D4 {s6['d4'][0]}/{s6['d4'][1]}  D6 {s6['d6']}  D5 {s6['d5']}")
    out = ROOT / "experiments/h10/repro"
    out.mkdir(parents=True, exist_ok=True)
    summ = dict(reproduced=ok, recorded=PH7_RECORDED, ph7_direct={a: norm6(v) for a, v in direct.items()},
                harness={a: norm6(v) for a, v in harness.items()}, implementation=imp,
                h10_py_sha256=sha(__file__), ph7_py_sha256=sha(HERE / "ph7.py"), ph2_py_sha256=sha(HERE / "ph2.py"))
    (out / "summary.json").write_text(json.dumps(summ, indent=2) + "\n", encoding="utf-8", newline="\n")
    say(f"\nwrote experiments/h10/repro/summary.json sha256 {sha(out / 'summary.json')}")
    return 0 if ok and imp["all"] else 3


# ---------------------------------------------------------------- the registered stages
def cmd_stage(args, which):
    header(which)
    frozen = None
    if which in ("development", "evaluation"):
        frozen = json.loads(FREEZE.read_text(encoding="utf-8"))
        if frozen["h10_py_sha256"] != sha(__file__) or frozen["design_sha256"] != sha(DESIGN):
            say("REFUSED: src/h10.py or the design differs from the frozen hash")
            return 4
        if which == "evaluation":
            dev = json.loads((ROOT / "experiments/h10/development/summary.json").read_text(encoding="utf-8"))
            if not dev.get("qualified"):
                say("REFUSED: development did not qualify the evaluation")
                return 4
        say(f"frozen: {frozen['chosen']}  arm 6: {frozen['mask_chosen']}  (freeze.json sha256 {sha(FREEZE)})")
    seeds = SEEDS[which]
    say(f"seeds {json.dumps(seeds)}")
    ok_r, _, _, _ = repro()
    say(f"historical reproduction (section 8.1, re-run now): {ok_r}")
    stage = run_stage(which, seeds=seeds)
    draws = np.random.default_rng(seeds["bootstrap"]).integers(0, ROWS, size=(NBOOT, ROWS))
    imp, table, six, logs = print_stage(stage, draws, which)
    summary = dict(stage=which, seeds=seeds, historical_reproduction=ok_r, implementation=imp, criteria=table,
                   phase71_readings=six, events=logs, h10_py_sha256=sha(__file__), design_sha256=sha(DESIGN),
                   ph7_py_sha256=sha(HERE / "ph7.py"), ph2_py_sha256=sha(HERE / "ph2.py"), numpy=np.__version__)
    impl_ok = ok_r and imp["all"]
    say(f"\n== {which}: verdict ==")
    if which == "calibration":
        chosen, mask = select(table)
        summary.update(chosen=chosen, mask_chosen=mask, implementation_pass=impl_ok)
        say(f"  implementation (every check): {'PASS' if impl_ok else 'FAIL'}")
        say(f"  first H10 setting passing every criterion (tau_e ascending, then theta): {chosen}")
        say(f"  first arm-6 theta_m passing every criterion: {mask}")
        if not impl_ok:
            say("  STOP: an implementation check failed; repair, disclose and rehash before any other seed is used")
        elif chosen is None:
            say("  STOP: no H10 setting passes; H10 is NOT SHOWN for this family (design 8.2)")
        else:
            say("  continue to the freeze")
    else:
        name, mask = frozen["chosen"], frozen["mask_chosen"]
        c = table[name]
        verdict = impl_ok and c["science_pass"]
        summary.update(chosen=name, mask_chosen=mask, implementation_pass=impl_ok, frozen_setting_pass=verdict)
        say(f"  implementation (every check): {'PASS' if impl_ok else 'FAIL'}")
        say(f"  frozen setting {name}: every registered criterion {'PASS' if verdict else 'NOT all pass'}")
        if mask is not None:
            say(f"  arm 6 at its calibrated {mask}: {'PASS' if table[mask]['science_pass'] else 'not all pass'}")
        else:
            say("  arm 6: no theta_m passed at calibration; its three thresholds are reported above")
        if which == "development":
            summary["qualified"] = verdict
            say(f"  development {'qualifies' if verdict else 'does NOT qualify'} the single evaluation")
        else:
            summary["h10_stage_a"] = "PASS" if verdict else "NOT SHOWN"
            say(f"  H10 Stage A under the registered criteria: {'PASS' if verdict else 'NOT SHOWN'}")
    save(stage, Path(args.out) if args.out else ROOT / f"experiments/h10/{which}", summary)
    return 0


def cmd_freeze(args):
    header("section 8.3 freeze")
    cal = ROOT / "experiments/h10/calibration/summary.json"
    s = json.loads(cal.read_text(encoding="utf-8"))
    if not s.get("implementation_pass") or s.get("chosen") is None:
        say("REFUSED: calibration selected nothing, or an implementation check failed")
        return 4
    fr = dict(chosen=s["chosen"], mask_chosen=s["mask_chosen"], h10_py_sha256=sha(__file__), design_sha256=sha(DESIGN),
              ph7_py_sha256=sha(HERE / "ph7.py"), ph2_py_sha256=sha(HERE / "ph2.py"),
              calibration_summary_sha256=sha(cal), calibration_trace_sha256=sha(cal.parent / "trace.npz"), seeds=SEEDS,
              bars=dict(BARS, hard_wrong_upper=U_WRONG), family=dict(tau_e=TAUS, theta=THETAS, mask_theta=MASK_THETAS))
    FREEZE.write_text(json.dumps(fr, indent=2) + "\n", encoding="utf-8", newline="\n")
    say(json.dumps(fr, indent=2))
    say(f"wrote experiments/h10/freeze.json sha256 {sha(FREEZE)}")
    return 0


# ---------------------------------------------------------------- self-checks (no registered seed)
def cmd_demo(args):
    header("demo: self-checks on ph7's historical generators only (no registered seed)")
    rows, T = 60, 200
    tgt = np.random.default_rng(1000).integers(0, N, rows)
    x = np.asarray(cue_steps(rows, tgt, np.random.default_rng(7), T, 0.4, 1.0, 0.3) + blank_steps(rows, 100))
    g, h = ph7.Graded(rows, rng=np.random.default_rng(0), J=J, c=C), H10(rows, rng=np.random.default_rng(0))
    ok = True
    for t in range(len(x)):
        g.step(x[t])
        h.step(x[t])
        ok &= bool(np.array_equal(g.memory(), h.g.memory()))
    say(f"ok  H10's graded state equals ph7.Graded bitwise over {len(x)} steps: {ok}")
    assert ok
    r1, r2 = np.random.default_rng(0), np.random.default_rng(0)
    a, b = ph7.Graded(rows, rng=r1, J=J, c=C), H10(rows, rng=r2)
    for t in range(50):
        a.step(x[t])
        b.step(x[t])
        b.gates()
    same = r1.bit_generator.state == r2.bit_generator.state
    say(f"ok  the gate consumes no randomness (generator states equal after 50 steps): {same}")
    assert same
    hh = H10(3, rng=np.random.default_rng(0))
    hh.e[:] = np.array([[1.0, 0.9, 0.8, 0.8, 0.8]])[None]
    g1, q1, _ = hh.gates()
    hh.e *= 0.37
    g2, q2, _ = hh.gates()
    say(f"ok  q is invariant under a common decay of e: {np.allclose(q1, q2, rtol=1e-12)} (q {q1[0, 0]:.6f})")
    assert np.allclose(q1, q2, rtol=1e-12)
    z = H10(4, rng=np.random.default_rng(0))
    for _ in range(100):
        z.step(np.zeros((4, N)))
    gz, _, tz = z.gates()
    say(f"ok  under zero input e stays 0 and every gate is closed: {bool((tz == 0).all() and not gz.any())}")
    assert (tz == 0).all() and not gz.any()
    ch = np.random.SeedSequence(99).spawn(3)
    tg = balanced_targets(ch[0])
    say(f"ok  balanced targets: counts {np.bincount(tg, minlength=N).tolist()} of {len(tg)}")
    assert (np.bincount(tg, minlength=N) == ROWS // N).all()
    ga, gb = np.random.default_rng(ch[2]), np.random.default_rng(ch[2])
    say(f"ok  two generators from one SeedSequence child draw identically: "
        f"{bool(np.array_equal(ga.standard_normal((3, 5)), gb.standard_normal((3, 5))))}")
    say(f"ok  ChanDiv.step has no reset parameter: {'reset' not in inspect.signature(ph7.ChanDiv.step).parameters};"
        f" Bistable.step drives reset=0.0: {'reset=0.0' in inspect.getsource(ph7.Bistable.step)}")
    tape, _ = build("revision", PERM_ROWS, np.random.default_rng(1000).integers(0, N, PERM_ROWS), np.random.default_rng(7))
    main = run(tape, lambda: np.random.default_rng(0), keep_rows=PERM_ROWS)
    src = np.random.default_rng(0)
    nt = np.asarray([src.standard_normal((PERM_ROWS, N)) for _ in range(len(tape))])
    p = perm_check(tape, nt, main)
    say(f"ok? label-permutation check on a historical revision tape: ok {p['ok']}; max state deviation "
        + ", ".join(f"{a} {v:.2e}" for a, v in p["max_state_deviation"].items())
        + f"; outputs exact {all(p['outputs_permute_exactly'].values())}; plain==main {p['plain_equals_main_states']}")
    h1 = H10(2, rng=np.random.default_rng(0))
    xs = np.array([[1.05, 1, 1, 1, 1], [1.4, 1, 1, 1, 1]])
    for _ in range(400):
        h1.step(xs)
    _, qq, _ = h1.gates()
    say(f"ok  noise-free settled q (tau_e 160): hard {qq[2, 0]:.5f}, easy {qq[2, 1]:.5f}"
        f" (design check: 0.0082, 0.0573)")
    return 0


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument("what", choices=["demo", "repro", "calibration", "freeze", "development", "evaluation"])
    cli.add_argument("--out")
    args = cli.parse_args()
    if args.what == "demo":
        return cmd_demo(args)
    if args.what == "repro":
        return cmd_repro(args)
    if args.what == "freeze":
        return cmd_freeze(args)
    return cmd_stage(args, args.what)


if __name__ == "__main__":
    sys.exit(main())
