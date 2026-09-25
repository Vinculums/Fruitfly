#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H20 Stage C Run 2: Agent14 with its learning module ON in the H15 Run 2 world, M4(c)'s readability read on G3+.

Usage: python ph31.py demo | bench | dev | eval

Design: H20 Stage C Run 2 design v2 FINAL, doc d007990ab333e7194, sha256 48fdd1f3...e4f2 (experiments/h20/
h20_stage_c_run2_design_v2.md), opened by decision:h20-stage-c-run2-open (the owner's standing instruction of 2026-09-25,
'다음도 권고안에 따라 작업 진행', gloss 'proceed with the next work too, according to the recommended option', applied to every
recommended option of design v1 section 12). Signed before this file existed: decision:h20-stage-c-m4c-readability-resigned-run2
(M4(c)'s readability: G3+ at least 50 rows and the no-learning GM over G3+ lower bound >= 10; Run 2 only; H14 format) and
decision:release-value-gated-stage-c-run2 ((N2) re-signed in form, Stage C Run 1 and Run 2).

Run 2 inherits every part of Run 1 (design v2 FINAL doc d27e6dfe2e2c16183; src/ph30.py) that its design does not change.
ph30 is imported UNCHANGED (its sha256 is checked at run time and the run stops on a mismatch), and through it ph4, ph8, ph9,
ph11, ph13, ph14, ph15, ph16, ph19, ph21, ph23, ph24, ph25, ph25b, ph28; ph30b is imported unchanged for its (B5) judge and its
end-state classes. No adopted module and no Run 1 file is edited. What this file adds: Run 2's seeds and seed self-check; the
bench (r) and (r'); the constructed states on Run 2's bench seeds; the restated (hR); the H15 no-learning arm at the bench; the
M4 judge with the re-signed readability and the four reported items of design 3.2; the recorder for the end-state classes.

Readings where the design is silent (printed again in every output header):
 (R1) (r) is ph30.reproduction, the function Run 1's bench ran, called first; (r') then calls ph30.bench as it is, whose own
      first part is (r) again; both are compared line for line (the H15 Run 2 output and Run 1's bench output respectively).
 (R2) (r'): the E1 bench rows of Run 1 are taken from ph30.bench's own run through a run-time hook on ph30.pool_run that keeps
      a copy of its results (restored afterwards; no ph30 code changes). During (r') the statistics are ph30's (95 percent,
      Run 1's bench bootstrap seed, read from ph30.BENCH); afterwards Run 2's (95 percent, 20261113).
 (R3) (r'): a line of ph30's bench output carrying one of Run 1's seed numbers (the pattern of ph30.seed_numbers(), as ph30b's
      leak check) is compared and not printed, so that ph30's seed self-check stays valid; this file names no Run 1 seed.
 (R4) (r'): (hR2) on Run 1's rows is drawn exactly as ph30b (B5): ph30b.judge_draw, mode '>0', outer generator seeded by the
      sequence [Run 1's bench bootstrap seed, 2], 1000 draws. The Agent3 argument of judge_draw is not read by mode '>0'; Run 1's
      bench has no H15 no-learning arm, so the floor's own dwell is passed there.
 (R5) The recorder (end-state classes, design 3.2 item (3)): a separate run of the same arm on the same seeds through ph30.e1_sim
      and ph30's Sim.step, reading state between steps only; the world's own sense is wrapped to keep its return (ph30b's way);
      over the last third it keeps whether any whiff of either odour arrived and the number of wall contacts. Classes by
      ph30b.classify with atR / atP = the harness's own steps within HIT_R of R / P over blocks 7-9, nearwall_L = the harness's
      own near-wall count (float64 positions; ph30b recomputed it from float32 recorded positions). The recorded run is checked
      equal to the unrecorded one on every end-of-run record.
 (R6) (hR2) at the Run 2 bench: ph30b.judge_draw mode '>0' (G3+ at least 50 by its n >= 50 test and the GM lower bound >= 10;
      the RGM over the drawn G3 with a finite upper bound <= 0.75; the WIN on the drawn G3+ with ties <= 0.20 and Wilson lower
      bound >= 0.60), outer generator [20261113, 2], 1000 draws; the fractions for the RGM part, the WIN part and M4(c) as a
      whole printed beside.
 (R7) (v), (g), (n) and (i9) are built on Run 2's bench E1 seeds (ph30.stub and ph30.build with the seeds passed; ph30.constructed
      binds Run 1's); (i5) on Stage B's 2005/2107 through ph30.i5_check.
 (R8) M9 in dev and eval is read from experiments/h20/ph31_bench.txt (its sha256, the ph31.py sha256 in its header and its M9
      line printed), not re-run: design section 9 sizes (r') as one re-run. (Run 1's reading R14 re-ran its bench; this run does not.)
 (R9) Design 3.2 item (3) lists every G3 row outside G3+ with its class and the learned arm's last-third punishing dwell; item (4)
      takes 'H15 Run 2's agent without learning' as ph30's arm 'H15 no-learning' (ph15.make_agent abl 'learn').
 (R10) The H15 no-learning arm at the bench is ph30's single E1 arm 'H15 no-learning', added to the bench's arm list; the H15
      no-learning end-state classes at the bench come from its recorded run (R5).
 (R11) Everything else as ph30's readings R1-R20 (ph30's header), with Run 2's seeds.
 (R12) At the end of every mode the output is checked for Run 1's seed numbers outside the masked (r') lines and the result
      printed (a step count or other number can equal one by chance).
 (R13) dev and eval: the recorded no-learning run (R5) is checked equal to the unrecorded arm on every end-of-run record and the
      result printed beside design 3.2 item (3); it reads no rule (M8 stays the identities of Run 1).
 (R14) M9 (R8) is PASS iff ph31_bench.txt has exactly one M9 line, it reads 'M9 PASS', and the ph31.py sha256 in its header equals
      this file's sha256 (the bench was run by the code that runs the tasks).

Completion note (2026-09-25). This file was written up to line 615 by an earlier session that was cut off by a rate limit before
any recorded run; it was then read in full against the design, ph30.py and ph30b.py by the resuming session. The resuming session
found every part of design sections 3-9 present (seed constants and scan, (r), (r'), the restated (hR), the H15 no-learning arm at
the bench, the re-signed M4 judge with the four reported items, dev and eval) and changed only: this completion note; readings R13
and R14 with their code (the recorder check printed in dev and eval; M9 requiring the bench to have been run by this same file);
the demo header's wording of the check 5 fix, which the earlier session recorded before the cut-off and which was not re-run
separately. No bar, seed, arm, rule or statistic was changed.
Nothing changes after the table.
"""
import sys, os, re, io, math, hashlib, contextlib
import multiprocessing as mp
import numpy as np
import ph30                                     # imported unchanged: sets Run 1's statistics; Run 2's are set below
import ph30b                                    # imported unchanged: judge_draw (B5), classify, CLS
import ph15
from ph9 import STEPS
from ph15 import World6, late, unrec
from ph16 import Still
from ph21 import G_STAR

sys.stdout.reconfigure(newline="\n")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
PH30_SHA = "98822834043de5f31615e73cd4a83444adcef2f1d5e56478356d70ca905059bd"
PH30B_SHA = "4e4122c8ba945467d61f3235b8d7eac3d28e788f851ae2b3629d1f476a12be59"
PH30_BENCH_SHA = "3fec4dc50dd3af4456649cf8b10a494d04a5afe937f5bf1f65bc31f2a2367eec"
DESIGN = "H20 Stage C Run 2 v2 FINAL doc d007990ab333e7194 hash 48fdd1f30952a376fce85fba355645635d08ef37db772b59fe24588f7ac2e4f2"
R, T1, T2 = ph30.R, ph30.T1, ph30.T2
SEEDS = dict(dev=((9955, 9959), (9967, 9975)), eval=((2057, 2159), (2061, 2163)))
BENCH = dict(e1=(20261111, 20261112), e2=(20261114, 20261115), boot=20261113)
NOUT = int(os.environ.get("PH31_OUTER", "1000"))
BENCH_OUT = os.path.join(REPO, "experiments", "h20", "ph31_bench.txt")
BENCH6 = ["learned", "H15 agent", "positive-off", "no-learning", "known-answer", "as composed (N1)"]
EXPECT_RP = dict(G3=199, G3p=111, GM=("24.000", "22.667", "24.667", "PASS"), WIN=(111, 0, 0), P=1.0, cls={"i": 88, "ii": 0, "iii": 0, "iv": 0, "v": 0})
RUN1_PAT = re.compile(r"(?<!\d)(" + "|".join(str(x) for x in ph30.seed_numbers()) + r")(?!\d)")


def sha(p=__file__): return hashlib.sha256(open(p, "rb").read()).hexdigest()


def stats2(): ph30.set_stats(ph30.Z95, ph30.QLO95, ph30.QHI95, BENCH["boot"])
def stats1(): ph30.set_stats(ph30.Z95, ph30.QLO95, ph30.QHI95, ph30.BENCH["boot"])


stats2()


# ------------------------------------------------------------------ output capture (reading R12)
class Tee:
    def __init__(self, s): self.s, self.buf = s, []
    def write(self, x): self.buf.append(x); return self.s.write(x)
    def flush(self): self.s.flush()
    def __getattr__(self, k): return getattr(self.s, k)


def leak_check():
    t = sys.stdout
    txt = "".join(t.buf) if isinstance(t, Tee) else ""
    hits = sorted(set(RUN1_PAT.findall(txt)))
    print(f"   leak check (reading R12): Run 1 seed numbers in this output outside the masked (r') lines: {hits if hits else 'none'}")


# ------------------------------------------------------------------ header, readings, seed scan
def header(say=print):
    ok30, ok30b = sha(ph30.__file__) == PH30_SHA, sha(ph30b.__file__) == PH30B_SHA
    say(f"   ph31.py sha256 {sha()}; design {DESIGN}")
    say(f"   ph30.py sha256 {sha(ph30.__file__)} (the Run 1 version {PH30_SHA[:8]}...{PH30_SHA[-4:]}: {ok30}); ph30b.py sha256 {sha(ph30b.__file__)}"
        f" (recorded {PH30B_SHA[:8]}...{PH30B_SHA[-4:]}: {ok30b})")
    say("   imported modules (through ph30): " + "; ".join(f"{os.path.basename(m.__file__)} {sha(m.__file__)}" for m in ph30.MODS))
    say(f"   seeds: E1-C dev {SEEDS['dev'][0]}, eval {SEEDS['eval'][0]}; E2-C dev {SEEDS['dev'][1]}, eval {SEEDS['eval'][1]}; bench E1 {BENCH['e1']}, E2 {BENCH['e2']};"
        f" bootstrap {BENCH['boot']} (95 percent, 5000); reproduction (r) on H15 Run 2's {ph30.REPRO} only (reused on purpose, read for no criterion, NOT in the seed scan);"
        " (r') on Run 1's bench seeds read from ph30 (not written out); (i5) on Stage B's (2005, 2107) only; demo seeds (3, 4), (5, 6), (7, 8) used deliberately")
    say("   decisions: decision:h20-stage-c-run2-open (seven points); decision:h20-stage-c-m4c-readability-resigned-run2 (M4(c) readability on G3+, G3+ >= 50, Run 2 only);"
        " decision:release-value-gated-stage-c-run2 ((N2) re-signed in form, Stage C Run 1 and Run 2; decision:release-negative-scope-on-hold stays in force outside Stage C);"
        " the adopted agent: decision:h26-adaptive-presence-adopted-within-tested-conditions")
    say(f"   rows share no state: one world generator and one agent generator per arm; arms in {ph30.NPROC} parallel processes (ph30 reading R18)")
    if not (ok30 and ok30b): say("== ph30.py or ph30b.py is not the recorded version: STOP, nothing is run =="); raise SystemExit(4)


def readings(say=print):
    say("   readings where the design is silent (file header R1-R12): R1 (r) = ph30.reproduction first, then (r') = ph30.bench as it is (its own (r) again); R2 Run 1's rows"
        " from ph30.bench through a hook on ph30.pool_run (restored), ph30's statistics during (r'), Run 2's after; R3 (r') lines carrying a Run 1 seed number compared, not"
        " printed; R4 (r') (hR2) = ph30b.judge_draw mode '>0', generator [Run 1's bench bootstrap seed, 2], 1000 draws; R5 recorder: a separate recorded run of the arm"
        " (whiffs of either odour and contacts over the last third), classes by ph30b.classify, the recorded run checked equal to the unrecorded one; R6 (hR2) at the Run 2"
        " bench = ph30b.judge_draw mode '>0', generator [20261113, 2], 1000 draws, RGM / WIN / M4(c) fractions beside; R7 (v), (g), (n), (i9) on Run 2's bench E1 seeds,"
        " (i5) on 2005/2107; R8 M9 in dev and eval read from ph31_bench.txt, not re-run; R9 item (3) every G3 row outside G3+, item (4) the arm 'H15 no-learning';"
        " R10 the H15 no-learning arm at the bench = ph30's single arm, its classes from its recorded run; R11 else ph30's R1-R20; R12 a leak check for Run 1 seed numbers")


def seed_numbers():
    base = [*SEEDS["dev"][0], *SEEDS["eval"][0], *SEEDS["dev"][1], *SEEDS["eval"][1], *BENCH["e1"], *BENCH["e2"], BENCH["boot"]]
    worlds = [SEEDS["dev"][0][0], SEEDS["dev"][1][0], SEEDS["eval"][0][0], SEEDS["eval"][1][0], BENCH["e1"][0], BENCH["e2"][0]]
    agents = [SEEDS["dev"][0][1], SEEDS["dev"][1][1], SEEDS["eval"][0][1], SEEDS["eval"][1][1], BENCH["e1"][1], BENCH["e2"][1]]
    return base + [s + 10_000 for s in worlds] + [s + 20_000 for s in worlds] + [s + 20_000 for s in agents] + [BENCH["e1"][0] + 10_000_000, BENCH["e1"][1] + 20_000_000]


def seeds_unused():
    """design section 9: none of Run 2's numbers appears in any other file under the repository (recursive, digit boundary; .git and
    __pycache__ excluded; excluded by name: ph31.py, ph31_*.txt, h20_stage_c_run2_*.md, master_plan.md, notes/*.md, viewer/*)"""
    nums = seed_numbers(); pat = re.compile(rb"(?<!\d)(" + "|".join(map(str, nums)).encode() + rb")(?!\d)"); hits = []; nf = 0
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        top = os.path.relpath(root, REPO).replace("\\", "/").split("/")[0]
        for f in files:
            if f == "ph31.py" or (f.startswith("ph31_") and f.endswith(".txt")) or (f.startswith("h20_stage_c_run2_") and f.endswith(".md")) or f == "master_plan.md": continue
            if (os.path.basename(root) == "notes" and f.endswith(".md")) or top == "viewer": continue
            nf += 1
            if pat.search(open(os.path.join(root, f), "rb").read()): hits.append(os.path.relpath(os.path.join(root, f), REPO))
    return hits, nums, nf


# ------------------------------------------------------------------ jobs: ph30's, plus the recorder (reading R5)
def recorded(name, seeds, runs=R, steps=T1):
    s = ph30.e1_sim(name, seeds, runs, steps); w = s.w; box = {}; orig = w.sense
    def sense():
        x = orig(); box["w"] = x; return x
    w.sense = sense
    L0 = steps - 3*STEPS; wl = np.zeros(runs, bool); bl = np.zeros(runs)
    for t in range(steps):
        s.step(t)
        if t >= L0: wl |= box["w"].any(1); bl += w.bumped
    return dict(o=s.finish(), whiff_L=wl, bumps_L=bl)


def job(spec):
    if spec[0] == "rec1":
        _, name, seeds, runs, steps = spec; return recorded(name, seeds, runs, steps)
    return ph30.job(spec)


def pool_run(specs):
    if ph30.NPROC <= 1: return [job(s) for s in specs]
    with mp.get_context("fork").Pool(ph30.NPROC) as p: return p.map(job, specs, chunksize=1)


def classes(rec, rows):
    """ph30b's end-state classes (A2) for the given rows (reading R5)"""
    o = rec["o"]; out = {}
    for r in rows:
        x = dict(atR=int(o["g"][-3:, r].sum()), atP=int(o["b"][-3:, r].sum()), whiff_any_L=bool(rec["whiff_L"][r]),
                 bumps_L=int(rec["bumps_L"][r]), nearwall_L=int(o["nearwall"][r]))
        out[int(r)] = ph30b.classify(x)
    return out


def class_counts(cl): return {c: sum(v == c for v in cl.values()) for c in ph30b.CLS}


# ------------------------------------------------------------------ the re-signed readability and (hR2) (decision:h20-stage-c-m4c-readability-resigned-run2)
def hr2(lb, nlb, xa, seed, nout=None):
    """fractions of outer draws (rows with replacement) in which the re-signed readability, the RGM part, the WIN part and M4(c)
    as a whole pass, each draw judged by ph30b.judge_draw mode '>0' (readings R4, R6)"""
    nout = nout or NOUT; rng = np.random.default_rng([seed, 2]); cnt = np.zeros(4, int); n = len(lb)
    for _ in range(nout):
        idx = rng.integers(0, n, n)
        rd, rg, wn = ph30b.judge_draw(lb[idx], nlb[idx], xa[idx], [">0"])[">0"]
        cnt += np.array([rd, rg, wn, rd and rg and wn], int)
    ph15._idx.clear()
    return cnt/nout


def win_counts(a, b):
    a, b = np.asarray(a), np.asarray(b); return int((a < b).sum()), int((a == b).sum()), int((a > b).sum())


def reported_items(L, NL, A3N, g3, rec, say=print):
    """design 3.2, reported beside M4, no bar: (1) the floor over all G3; (2) the all-G3 WIN; (3) the rows outside G3+; (4) the Agent3 floor"""
    lb, nl = late(L["b"])[g3], late(NL["b"])[g3]; G3 = np.flatnonzero(g3)
    say("   reported beside M4, no bar (design 3.2):")
    pt, lo, hi = ph15.boot("GM", nl)
    say(f"   (1) Run 1's reading: Agent14 no-learning GM last-third punishing dwell over ALL G3: n {len(nl)}, rows at 0 {int((nl == 0).sum())}; {pt:.3f} [{lo:.3f}, {hi:.3f}];"
        f" 'at least 10' would read {ph15.verdict(lo, hi, 10, False)}")
    k, t, l = win_counts(lb, nl); n = len(lb); p, wlo, whi = ph15.wilson(k, n); tf = t/n
    say(f"   (2) WIN learned below no-learning over ALL G3 (Run 2's Q3(c) form): n {n}; wins {k}, ties {t}, losses {l}; tie fraction {tf:.3f}; share {p:.3f} [{wlo:.3f}, {whi:.3f}]"
        f" -> {'UNREADABLE (ties > 0.20; the tie rule, not waived)' if tf > 0.20 else ph15.verdict(wlo, whi, 0.60, False)}")
    out = G3[nl == 0]; cl = classes(rec, out) if rec is not None else {}
    lo_ = late(L["b"])[out]
    say(f"   (3) G3 rows outside G3+ (no-learning last-third punishing dwell 0): {len(out)}; end-state classes (ph30b (A2)): "
        + "; ".join(f"{ph30b.CLS[c]} {v}" for c, v in class_counts(cl).items())
        + f"; learned arm's last-third punishing dwell in these rows: above 0 (a loss hidden from the G3+ WIN) {int((lo_ > 0).sum())}, max {lo_.max() if len(lo_) else 0:.3f}")
    for s0 in range(0, len(out), 10):
        say("       " + "; ".join(f"row {r} ({cl.get(int(r), '-')}) {late(L['b'])[r]:.3f}" for r in out[s0:s0 + 10]))
    if A3N is not None:
        a3 = late(A3N["b"])[g3]
        say(f"   (4) H15 Run 2's agent without learning as a floor (arm 'H15 no-learning'): rows at 0 {int((a3 == 0).sum())}/{len(a3)}")
        ph30.crit("       reported: H15 no-learning GM last-third punishing dwell over G3", "GM", 10, False, a3, say=say)
        ph30.crit("       reported: RGM learned / H15 no-learning over G3", "RGM", 0.75, True, lb, a3, say=say)
        m = a3 > 0; k3, t3, l3 = win_counts(lb[m], a3[m])
        say(f"       reported: WIN learned below H15 no-learning on its own dwell > 0 rows: n {int(m.sum())}; wins {k3}, ties {t3}, losses {l3}")
        ph30.crit("       reported: WIN learned below H15 no-learning on its own dwell > 0 rows", "WIN", 0.60, False, lb[m], a3[m], say=say)
    return cl


# ------------------------------------------------------------------ (r') Run 1's bench through ph30 as imported
def rprime(say=print):
    okf = sha(ph30.BENCH_TXT) == PH30_BENCH_SHA
    say(f"(r') Run 1's bench through ph30 as imported (reading R1-R4): ph30.py {sha(ph30.__file__) == PH30_SHA}; experiments/h20/ph30_bench.txt sha256 {sha(ph30.BENCH_TXT)}"
        f" (recorded {PH30_BENCH_SHA[:8]}...{PH30_BENCH_SHA[-4:]}: {okf})")
    if not okf: return False, {}
    stats1(); cap = []; orig = ph30.pool_run
    def hook(specs):
        r = orig(specs); cap.append((specs, r)); return r
    ph30.pool_run = hook; buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf): v1, o1 = ph30.bench()
    finally: ph30.pool_run = orig
    mine = buf.getvalue().split("\n"); ref = open(ph30.BENCH_TXT, encoding="utf-8").read().split("\n")
    eqn = sum(1 for a, b in zip(mine, ref) if a == b); same = mine == ref; masked = 0
    say(f"(r') ph30.bench re-run: {len(mine) - 1} lines against {len(ref) - 1} in ph30_bench.txt; equal line for line {eqn - 1 if mine[-1] == ref[-1] == '' else eqn}; identical {same};"
        f" ph30.bench's M9 as Run 1 (STOPPED by (hR)): {(not v1) and o1.get('stop_hr') is True and not o1.get('stop_h') and not o1.get('stop_hs')}")
    for i, (a, b) in enumerate(zip(mine, ref)):
        if i == len(mine) - 1 and a == "": break
        if RUN1_PAT.search(a) or RUN1_PAT.search(b):
            masked += 1; say(f"   (r') {i + 1:3d} {'==' if a == b else '!='} [a line carrying Run 1's bench seeds: compared, not printed]"); continue
        say(f"   (r') {i + 1:3d} {'==' if a == b else '!='} {a}")
        if a != b: say(f"   (r') {i + 1:3d} ref {b}")
    say(f"(r') lines carrying Run 1's seeds, compared and not printed: {masked}")
    # Run 1's E1 bench rows (the E1 + E2 bench call of ph30.bench)
    want = ph30.e1_specs(ph30.BENCH["e1"], arms=BENCH6) + ph30.e2_specs(ph30.BENCH["e2"])
    hit = [r for s, r in cap if s == want]
    if len(hit) != 1: say(f"(r') Run 1's bench call not found in the captured pool calls ({len(cap)} calls): implementation error"); stats2(); return False, {}
    s1 = ph30.e1_specs(ph30.BENCH["e1"], arms=BENCH6); arms, _, _ = ph30.collect(s1, hit[0][:len(s1)])
    rec = pool_run([("rec1", "no-learning", ph30.BENCH["e1"], R, T1)])[0]
    L, NL = arms["learned"], arms["no-learning"]; ps = L["pstart"]; g3 = ps & (L["first_b"] >= 0)
    lb, nlb = late(L["b"])[g3], late(NL["b"])[g3]; g3p = nlb > 0
    recsame = not ph30.end_equal(NL, rec["o"])
    say(f"(r') recorder: the recorded no-learning run == the bench's no-learning arm on every end-of-run record: {recsame}")
    ph15._idx.clear(); gp = ph15.boot("GM", nlb[g3p]); gv = ph15.verdict(gp[1], gp[2], 10, False); k, t, l = win_counts(lb[g3p], nlb[g3p])
    say(f"(r') the re-signed readability on Run 1's bench rows (ph30's statistics): G3 {int(g3.sum())}; G3+ {int(g3p.sum())}; Agent14 no-learning GM over G3+"
        f" {gp[0]:.3f} [{gp[1]:.3f}, {gp[2]:.3f}] 'at least 10' -> {gv}; WIN learned below no-learning on G3+ wins {k}, ties {t}, losses {l}")
    fr = hr2(lb, nlb, nlb, ph30.BENCH["boot"])
    say(f"(r') (hR2) on Run 1's rows, drawn as ph30b (B5) draws it ({NOUT} outer draws): readability PASS {fr[0]:.3f}; RGM part {fr[1]:.3f}; WIN part {fr[2]:.3f}; M4(c) whole {fr[3]:.3f}")
    cl = classes(rec, np.flatnonzero(g3)[~g3p]); cc = class_counts(cl)
    say(f"(r') end-state classes of the {int((~g3p).sum())} G3 rows outside G3+ (ph30b.classify via the recorder): " + "; ".join(f"({c}) {v}" for c, v in cc.items()))
    chk = {"every line identical": same, "G3 199": int(g3.sum()) == EXPECT_RP["G3"], "G3+ 111": int(g3p.sum()) == EXPECT_RP["G3p"],
           "GM 24.000 [22.667, 24.667] PASS": (f"{gp[0]:.3f}", f"{gp[1]:.3f}", f"{gp[2]:.3f}", gv) == EXPECT_RP["GM"], "WIN 111/0/0": (k, t, l) == EXPECT_RP["WIN"],
           "(hR2) 1.000": fr[0] == EXPECT_RP["P"], "classes (i) 88, others 0": cc == EXPECT_RP["cls"], "recorder == bench arm": recsame}
    ok = all(chk.values())
    say("(r') expected exactly (design section 4; diag:38, :49, :201, :210, :231): " + "; ".join(f"{k_} {v}" for k_, v in chk.items()) + f" -> (r') {ok}")
    stats2()
    return ok, dict(chk=chk)


# ------------------------------------------------------------------ constructed states on Run 2's bench seeds (reading R7)
def constructed(seeds=None, say=print):
    seeds = seeds or BENCH["e1"]; ids, exact = {}, {}
    w = World6(R, np.random.default_rng(seeds[0]), seeds[0], "balanced")
    ex, masks_ok, u = ph30.value_trajectories(w.good, say); exact.update(ex)
    say(f"   (v) exactness claims (ph30 reading R6): " + "; ".join(f"{k} {v}" for k, v in ex.items()))
    one = [(1, 0.0, 1.0), (40 - 1, 0.0, 0.0)]; g = {}
    for v in (0.0, 0.01, 0.025, 0.05, 0.1):
        o = ph30.stub("A14N2", (1.0, v), one, seeds=seeds); s1 = o["S"][:, :, 1]; peak = float(np.median(s1, 1).max()); held = int((o["H"] == 1).any(0).sum()); g[v] = (peak, held)
        say(f"(g) one punisher whiff at step 0 from rest, gain {1 + G_STAR*v:.2f} (v_P {v}): peak of the median s_1 {peak:.3f}; per-row peak quartiles {ph30.q3(s1.max(0), '.3f')};"
            f" rows holding the punisher odour on some step {held}/{R}")
    say(f"   (g) Stage B reproduced first: 0.756 at gain 1.0 {round(g[0.0][0], 3) == 0.756}; every row holding at gain 1.2 {g[0.1][1] == R}")
    sil = [(260, 0.0, 0.0)]; ev = [(100, 0.0, 0.0), (160, 0.30, 0.0)]
    for lab, sch in (("silent", sil), ("R whiffs p 0.30 from step 100", ev)):
        for kind in ("A14", "A14N2"):
            o = ph30.stub(kind, (1.0, -0.9), sch, hold=1, seeds=seeds); H = o["H"]; st = H.shape[0]
            end = np.where((H != 1).any(0), (H != 1).argmax(0), -1); r = np.arange(R)
            byev = (end >= 0) & o["EV"][np.maximum(end, 0), r]; byto = (end >= 0) & ~byev
            flee = o["FL"][H == 1].mean() if (H == 1).any() else float("nan")
            say(f"(n) {'(N1) as composed' if kind == 'A14' else '(N2)'}, negative hold (known (1.0, -0.9), channel 1 held s 2.0), {lab}: hold ended in {int((end >= 0).sum())}/{R} rows"
                f" (step {ph30.q3(end[end >= 0])}; at step 47: {int((end == 47).sum())}); ended with the evidence release flag {int(byev.sum())}, without it {int(byto.sum())};"
                f" still held at step {st - 1}: {int((H[-1] == 1).sum())}; timeout firings while held {int((o['TO'] & (H == 1)).sum())}; target == flee side on held steps {flee:.3f}")
    c9, txt = i9(seeds); ids["(i9) the flee reads the learned sign (mirror all rows, stale none)"] = c9; say(txt)
    ok5, txt = ph30.i5_check(); ids["(i5) the harness's Agent14 in World7 T1 == Stage B's supplied arm (2005/2107)"] = ok5; say(txt)
    return ids, exact


def i9(seeds=None):
    seeds = seeds or BENCH["e1"]; res = {}
    for lab in ("mirror", "stale"):
        class Wd: pass
        wd = Wd(); wd.good = np.zeros(R, int)
        a = ph30.build("A14N2", R, np.random.default_rng(seeds[1]), wd, None); a.known = np.zeros((R, 2)); a.sel.s[:, 1] = 2.0
        rv = np.zeros((R, 4)); rv[:, 0] = 1.0; a.mb.step(code=a.codes[:, 1], reinf=rv)
        if lab == "mirror": a.known = ph30.readout(a)
        _, h = a.act(Still(R), np.zeros((R, 2), bool), np.ones(R, bool)); res[lab] = (int(((a.tgt == a.flee_side) & (h == 1)).sum()), int((h == 1).sum()), ph30.readout(a)[:, 1])
    ok = res["mirror"][0] == R and res["stale"][0] == 0
    return ok, (f"(i9) constructed (ph30 reading R9, Run 2's bench agent seed): v_1 after one punished step {ph30.uniq(res['mirror'][2])}; with the mirror target == flee side in"
                f" {res['mirror'][0]}/{R} rows (channel 1 held {res['mirror'][1]}); with known left at 0/0 {res['stale'][0]}/{R} (held {res['stale'][1]}) -> {ok}")


# ------------------------------------------------------------------ the mechanism bench (design section 4)
def bench(say=print, seeds=None, steps=T1, full=True, nout=None):
    """full=False: a code-path run of everything after (r) and (r') (demo only)"""
    seeds = seeds or dict(e1=BENCH["e1"], e2=BENCH["e2"])
    say(f"== H20 Stage C Run 2 mechanism bench (design v2 FINAL section 4). design {DESIGN}; bench E1 {seeds['e1']}, E2 {seeds['e2']}; bootstrap seed {BENCH['boot']}, 95 percent;"
        f" (hR2) {nout or NOUT} outer draws ==")
    header(say); readings(say)
    out = dict(stop=False, nocand=False, repro=False, rprime=False)
    if full:
        hits, nums, nf = seeds_unused()
        say(f"   seed self-check (design section 9, before the first run): every Run 2 seed and derived number in no other file ({nf} scanned): {not hits}{'' if not hits else ' ' + str(hits)}")
        if hits: say("== a Run 2 seed appears in another file: STOP =="); return False, out
        hits30, _, nf30 = ph30.seeds_unused()
        say(f"   ph30's own seed self-check (Run 1's numbers; this file's outputs must not break it): {not hits30}{'' if not hits30 else ' ' + str(hits30)} ({nf30} scanned)")
        rep = ph30.reproduction(say); stats2(); out["repro"] = rep
        if not rep: say("== (r) NOT reproduced: no comparison is read; the bench stops here =="); return False, out
        say("== (r) holds: every line of experiments/h15/ph15_run2.txt reproduced; (r') next ==")
        rp, _ = rprime(say); out["rprime"] = rp
        if not rp: say("== (r') NOT reproduced: an implementation error; nothing else is read; the bench stops here (fixed and re-run) =="); return False, out
        say("== (r') holds: Run 1's bench reproduced line for line and the re-signed readability reads Run 1's rows exactly as expected; the Run 2 bench continues ==")
    else: out["repro"] = out["rprime"] = True
    ids, exact = constructed(seeds["e1"], say)
    arm_list = BENCH6 + ["H15 no-learning"]
    s1 = ph30.e1_specs(seeds["e1"], steps=steps, arms=arm_list); s2 = ph30.e2_specs(seeds["e2"], steps=min(T2, steps))
    sr = [("rec1", "no-learning", seeds["e1"], R, steps), ("rec1", "H15 no-learning", seeds["e1"], R, steps)]
    res = pool_run(s1 + s2 + sr); stats2()
    arms, disp, locks = ph30.collect(s1, res[:len(s1)]); e2a, e2d, e2l = ph30.collect(s2, res[len(s1):len(s1) + len(s2)]); recNL, recA3 = res[-2], res[-1]
    say(f"(i) identities on the E1 bench seeds {seeds['e1']}, {R} x {steps} (lockstep, ph30 reading R2):")
    ids.update(ph30.identities(arms, disp, locks + e2l, steps, e2=(e2a, e2d), say=say))
    rs_same = not ph30.end_equal(arms["no-learning"], recNL["o"]) and not ph30.end_equal(arms["H15 no-learning"], recA3["o"])
    say(f"   recorder (reading R5): the recorded no-learning and H15 no-learning runs == the unrecorded arms on every end-of-run record: {rs_same}")
    ids["recorder == unrecorded arm"] = rs_same
    L, A3, PO, NL, A3N = arms["learned"], arms["H15 agent"], arms["positive-off"], arms["no-learning"], arms["H15 no-learning"]
    ps = L["pstart"]; rs = ~ps; g3 = ps & (L["first_b"] >= 0)
    say(f"(h) E1-C on bench seeds {seeds['e1']}, {R} x {steps}; G3 (learned arm) {int(g3.sum())}/{int(ps.sum())}:")
    ph30.e1_bench_arms(arms, g3, say)
    o = A3N; vb = o["first_b"] >= 0
    say(f"   [H15 no-learning] R-start rows visiting P {int((vb & ~ps).sum())}/{int((~ps).sum())}; P-start late unrecovered {int(unrec(o)[ps].sum())}/{int(ps.sum())}, R-start"
        f" {int(unrec(o)[~ps].sum())}/{int((~ps).sum())}; all {int(unrec(o).sum())}/{R}; G3 reach after the first punished step {int((o['last_g'] > o['first_b'])[g3].sum())}/{int(g3.sum())};"
        f" last-third dwell median R {np.median(late(o['g'])):.1f} P {np.median(late(o['b'])):.1f}; first rewarded step {ph30.q3(o['first_g'][o['first_g'] >= 0])}; contacts/agent {o['contacts'].mean():.2f}")
    Vl, Va, Vp = (L["first_b"] >= 0)[rs], (A3["first_b"] >= 0)[rs], (PO["first_b"] >= 0)[rs]
    pa, dpa, ba = ph30.pp_pair(Vl, Va, -0.05, True); pb, dpb, bb = ph30.pp_pair(Vl, Vp, -0.05, True)
    _, l_a, h_a = ph15.boot("DP", Vl.astype(float), Va.astype(float))
    say(f"   (h) M2(a) R-start punisher visits learned {int(Vl.sum())} vs H15 agent {int(Va.sum())}: DP {dpa:+.4f} [{l_a:+.4f}, {h_a:+.4f}], discordant b {ba:.4f}"
        f" (learned only {int((Vl & ~Va).sum())}, H15 agent only {int((~Vl & Va).sum())}); pass probability {pa:.4f}")
    say(f"   reported: M2(b) learned vs positive-off {int(Vp.sum())}: DP {dpb:+.4f}, b {bb:.4f}, pass probability {pb:.4f}")
    stop_h = pa < 0.5
    say(f"   (h) STOP RULE: M2(a) pass probability {pa:.4f} {'< 0.5 -> STOP: the run returns to the owner after the bench record' if stop_h else '>= 0.5 -> continue'}")
    ul, ua = unrec(L)[ps], unrec(A3)[ps]; p3, dp3, b3 = ph30.pp_pair(ul, ua, 0.10, True)
    rl, ra = (L["last_g"] > L["first_b"])[g3], (A3["last_g"] > A3["first_b"])[g3]; p5, dp5, b5 = ph30.pp_pair(rl, ra, -0.10, False)
    say(f"   (hS) M3(b) P-start late unrecovered learned {int(ul.sum())} vs H15 agent {int(ua.sum())} of {int(ps.sum())}: DP {dp3:+.4f}, b {b3:.4f}, pass probability {p3:.4f};"
        f" M5(a) G3 reach after the first punished step learned {int(rl.sum())} vs H15 agent {int(ra.sum())} of {int(g3.sum())}: DP {dp5:+.4f}, b {b5:.4f}, pass probability {p5:.4f}")
    pr3, dpr3, _ = ph30.pp_pair(unrec(L)[rs], unrec(A3)[rs], 0.10, True)
    say(f"   reported: M3(b) R-start DP {dpr3:+.4f}, pass probability {pr3:.4f}; M3(a) learned late unrecovered {int(unrec(L).sum())}/{R}")
    stop_hs = p3 < 0.5 or p5 < 0.5
    say(f"   (hS) STOP RULE: {'STOP: the run returns to the owner after the bench record' if stop_hs else 'both >= 0.5 -> continue'}")
    # (hR), restated (decision:h20-stage-c-m4c-readability-resigned-run2)
    lb, nlb, a3b = late(L["b"])[g3], late(NL["b"])[g3], late(A3N["b"])[g3]; g3p = nlb > 0; n3p = int(g3p.sum())
    stop_hr1 = n3p < 50
    say(f"   (hR1) G3+ (G3 rows whose Agent14 no-learning last-third punishing dwell is above 0) {n3p}/{int(g3.sum())}; STOP if under 50: {'STOP' if stop_hr1 else 'continue'}")
    fr = hr2(lb, nlb, a3b, BENCH["boot"], nout)
    stop_hr2 = fr[0] < 0.5
    say(f"   (hR2) pass probability of the re-signed readability (G3+ at least 50 and the no-learning GM over G3+ lower bound >= 10), {nout or NOUT} outer draws of the bench G3 rows"
        f" (generator [{BENCH['boot']}, 2]; ph30b (B5), reading R6): {fr[0]:.4f} {'< 0.5 -> STOP' if stop_hr2 else '>= 0.5 -> continue'}")
    stop_hr = stop_hr1 or stop_hr2
    say(f"   (hR) STOP RULE: {'STOP: M4(c) would be unreadable' if stop_hr else 'continue'}")
    say("   printed beside (hR), no rule:")
    ph30.crit("   point reading: Agent14 no-learning GM last-third punishing dwell over the bench G3+", "GM", 10, False, nlb[g3p], say=say)
    say(f"   pass probabilities of the other M4(c) parts on the same draws: RGM part {fr[1]:.4f}; WIN part (ties <= 0.20, Wilson lower >= 0.60) {fr[2]:.4f}; M4(c) as a whole {fr[3]:.4f}")
    k, t, l = win_counts(lb[g3p], nlb[g3p])
    say(f"   WIN learned below no-learning on the bench G3+: wins {k}, ties {t}, losses {l}")
    reported_items(L, NL, A3N, g3, recNL, say)
    z3 = np.flatnonzero(g3)[a3b == 0]; c3 = class_counts(classes(recA3, z3))
    say(f"   the H15 no-learning arm at the bench (reading R10): GM over G3 printed in item (4); its zero rows {len(z3)}, classes: " + "; ".join(f"({c}) {v}" for c, v in c3.items())
        + f"; zero in both no-learning arms {int(((nlb == 0) & (a3b == 0)).sum())}")
    say("   printed beside (no rule): Stage C measures per arm")
    for nm in arm_list: ph30.extras(nm, arms[nm], g3, say)
    say(f"(E2 bench seeds {seeds['e2']}, ph30 reading R13, printed beside, no rule): pre-test medians trained rewarded {np.median(e2a['trained, learning on']['pre'][:, 0]):+.3f},"
        f" punished {np.median(e2a['trained, learning on']['pre'][:, 1]):+.3f}; sham {np.median(e2a['sham, frozen']['pre'][:, 0]):+.3f}/{np.median(e2a['sham, frozen']['pre'][:, 1]):+.3f};"
        + "; ".join(f" {nm}: reach R {int((o_['first_g'] >= 0).sum())}/{R}, P dwell median {np.median(o_['b'].sum(0)):.1f}" for nm, o_ in e2a.items()))
    idok = all(ids.values()); exok = all(exact.values()); nocand = not (idok and exok); stop = stop_h or stop_hs or stop_hr
    verdict = out["repro"] and out["rprime"] and idok and exok and not stop
    out.update(stop=stop, nocand=nocand, pa=pa, p3=p3, p5=p5, hr=fr, n3p=n3p, stop_h=stop_h, stop_hs=stop_hs, stop_hr=stop_hr)
    say(f"== M9: (r) {out['repro']}; (r') {out['rprime']}; identities {idok}; failed {[k_ for k_, v in ids.items() if not v]}; exactness claims of (v) {exok}; failed {[k_ for k_, v in exact.items() if not v]};"
        f" (h) {'STOP' if stop_h else 'continue'}; (hS) {'STOP' if stop_hs else 'continue'}; (hR) {'STOP' if stop_hr else 'continue'} -> M9 "
        + ("PASS: the tasks may be run" if verdict else ("FAIL, NO CANDIDATE: the design reading is wrong there; the tasks are NOT run" if nocand else
                                                        "STOPPED by a stop rule: the tasks are NOT run; the owner decides")) + " ==")
    return verdict, out


# ------------------------------------------------------------------ the tasks (design sections 5-8)
def main(mode_, runs=R, steps=T1, tsteps=T2, seeds=None, smoke=False):
    s1, s2 = seeds or SEEDS[mode_]
    print(f"== H20 Stage C Run 2, {mode_.upper()}{' (CODE-PATH SMOKE RUN on unregistered demo seeds; numbers not used)' if smoke else ''}. design {DESIGN}; Agent14 (P 60, N_hi 300), G {G_STAR},"
          f" gate, filter, release (N2); E1-C world {s1[0]} agent {s1[1]}, E2-C world {s2[0]} agent {s2[1]}; {runs} rows; E1-C {steps} steps, E2-C training {ph15.TRAIN}/{ph15.GAP}/{ph15.TRAIN}"
          f" then {tsteps} test steps; bootstrap {ph15.BOOT_SEED}, 95 percent; {'operation check only (not a verdict)' if mode_ == 'dev' else 'the one evaluation'} ==")
    header(); readings()
    if not smoke:
        hits, nums, nf = seeds_unused(); print(f"   seed self-check: every Run 2 seed and derived number in no other file ({nf} scanned): {not hits}{'' if not hits else ' ' + str(hits)}")
        if hits: print("== STOP: a seed of this run appears in another file =="); return
    print("   amendments: none")
    sp1 = ph30.e1_specs(s1, runs, steps); sp2 = ph30.e2_specs(s2, runs, tsteps); sr = [("rec1", "no-learning", s1, runs, steps)]
    res = pool_run(sp1 + sp2 + sr); stats2()
    arms, disp, locks = ph30.collect(sp1, res[:len(sp1)]); e2a, e2d, e2l = ph30.collect(sp2, res[len(sp1):len(sp1) + len(sp2)]); recNL = res[-1]
    L = arms["learned"]; ps = L["pstart"]; g3 = ps & (L["first_b"] >= 0)
    print(f"   recorder (reading R13): the recorded no-learning run == the unrecorded arm on every end-of-run record: {not ph30.end_equal(arms['no-learning'], recNL['o'])}")
    print(f"\n==== E1-C natural search. world seed {s1[0]}, agent seed {s1[1]}, {runs} rows, {steps} steps, learning on from step 0 ====")
    for nm in list(ph30.AGENT_ARMS) + ["random", "oracle"]: ph30.print_arm(nm, arms[nm], g3, groups=nm in ph30.AGENT_ARMS)
    print(f"\n==== E2-C controlled experience, learning ON in the test. world seed {s2[0]}, agent seed {s2[1]}, {runs} rows, every row a P-start row ====")
    allr = np.ones(runs, bool)
    for nm, o in e2a.items():
        rf = o["reward_first"]
        print(); ph15.measures(nm[:13], o, allr, "all")
        print(f"      [{nm}] training calls {o['train_calls']}; test learning calls {o['calls']}; reward-first rows {int(rf.sum())}; pre-test valence rewarded {np.median(o['pre'][:, 0]):+.3f}"
              f" (first {np.median(o['pre'][rf, 0]):+.3f} / second {np.median(o['pre'][~rf, 0]):+.3f}) punished {np.median(o['pre'][:, 1]):+.3f}"
              f" (first {np.median(o['pre'][~rf, 1]):+.3f} / second {np.median(o['pre'][rf, 1]):+.3f}); reach R {int((o['first_g'] >= 0).sum())}/{runs}; P dwell over the test median {np.median(o['b'].sum(0)):.1f}")
    judge(mode_, arms, disp, locks, e2a, e2d, e2l, g3, recNL, steps, smoke)


def judge(mode_, arms, disp, locks, e2a, e2d, e2l, g3, recNL, steps=T1, smoke=False):
    ok = lambda z: "PASS" if z else "FAIL"
    crit, agg = ph30.crit, ph30.agg
    L, A3, PO, NL, KA, A3N = arms["learned"], arms["H15 agent"], arms["positive-off"], arms["no-learning"], arms["known-answer"], arms["H15 no-learning"]
    ps = L["pstart"]; rs = ~ps; n = len(ps)
    print("\n== criteria (Run 2 design v2 FINAL section 7; 95 percent, one evaluation, no extension; a multi-part criterion PASS if every part passes, FAIL if any fails, else INCONCLUSIVE) ==")
    print("\n== M1 validity (all rows, last third) ==")
    m1 = [crit("(a) rewarding dwell, oracle - random", "DGM", 10, False, late(arms["oracle"]["g"]), late(arms["random"]["g"]))]
    for nm in ph30.AGENT_ARMS:
        for key in ("g", "b"): m1.append(crit(f"(b) {nm} dwell at {'R' if key == 'g' else 'P'}", "GM", 594, True, late(arms[nm][key])))
    m1.append(crit("(c) total dwell, learned - random", "DGM", 10, False, late(L["g"]) + late(L["b"]), late(arms["random"]["g"]) + late(arms["random"]["b"])))
    M1 = agg(m1); print(f"   M1 -> {M1}")
    print("\n== M2 the gain (E1-C, R-start rows): visited the punishing source at least once over the run ==")
    Vl, Va, Vp = ((o["first_b"] >= 0)[rs].astype(float) for o in (L, A3, PO))
    print(f"   R-start rows visiting P: learned {int(Vl.sum())}/{int(rs.sum())}, H15 agent {int(Va.sum())}, positive-off {int(Vp.sum())}, known-answer {int((KA['first_b'] >= 0)[rs].sum())},"
          f" no-learning {int((NL['first_b'] >= 0)[rs].sum())}, as composed (N1) {int((arms['as composed (N1)']['first_b'] >= 0)[rs].sum())}, H15 no-learning {int((A3N['first_b'] >= 0)[rs].sum())}")
    m2 = [crit("(a) DP learned Agent14 - H15 Run 2's agent", "DP", -0.05, True, Vl, Va), crit("(b) DP learned Agent14 - Agent14 positive-off", "DP", -0.05, True, Vl, Vp)]
    M2 = agg(m2); print(f"   M2 -> {M2}")
    print("\n== M3 search kept (late unrecovered: no plume whiff in blocks 7-9) ==")
    m3 = [crit("(a) learned, all rows", "P", 0.100, True, unrec(L))]
    for m, lab in ((ps, "P-start"), (rs, "R-start")):
        m3.append(crit(f"(b) DP learned - H15 agent, {lab}", "DP", 0.10, True, unrec(L)[m].astype(float), unrec(A3)[m].astype(float)))
        crit(f"    reported: DP learned - known-answer, {lab}", "DP", 0.10, True, unrec(L)[m].astype(float), unrec(KA)[m].astype(float))
    M3 = agg(m3); print(f"   M3 -> {M3}")
    print(f"\n== M4 avoidance kept, readability RE-SIGNED for Run 2 (decision:h20-stage-c-m4c-readability-resigned-run2). G3 = P-start rows punished at least once in the learned arm:"
          f" {int(g3.sum())}/{int(ps.sum())} ==")
    if g3.sum() < 50: m4 = ["UNREADABLE"]; print("   G3 under 50 -> UNREADABLE")
    else:
        nl = late(NL["b"]); g3p = g3 & (nl > 0)
        print(f"    G3+ = G3 rows whose no-learning last-third punishing dwell is above 0: {int(g3p.sum())} (the re-signed readability needs at least 50)")
        base = crit("    readability (re-signed): Agent14 no-learning punishing dwell in G3+", "GM", 10, False, nl[g3p])
        m4 = [crit("(a) learned value of the punished odour at the end", "GM", -0.5, True, L["val"][-1][g3, 1])]
        if base == "PASS":
            m4 += [crit("(b) punishing dwell, learned", "GM", 1.0, True, late(L["b"])[g3]),
                   agg([crit("(c) punishing dwell, learned / no-learning", "RGM", 0.75, True, late(L["b"])[g3], nl[g3]),
                        crit("(c) learned below no-learning, WIN on G3+", "WIN", 0.60, False, late(L["b"])[g3p], nl[g3p])])]
            print(f"   (c) -> {m4[-1]}")
        else: m4 += ["UNREADABLE"]*2; print("   (b), (c): UNREADABLE, the re-signed readability does not PASS (G3+ under 50 or the GM over G3+ not PASS 'at least 10')")
        k, t, l = win_counts(late(L["b"])[g3p], nl[g3p]); print(f"    WIN on G3+ counts: wins {k}, ties {t}, losses {l}")
        reported_items(L, NL, A3N, g3, recNL)
    M4 = agg(m4); print(f"   M4 -> {M4}")
    print("\n== M5 reach and dwell after avoidance (G3, H15 Run 2's agent as the reference) ==")
    if g3.sum() < 50: m5 = ["UNREADABLE"]
    else:
        m5 = [crit("(a) reach the rewarding source after the first punished step, learned - H15 agent", "DP", -0.10, False,
                   (L["last_g"] > L["first_b"])[g3].astype(float), (A3["last_g"] > A3["first_b"])[g3].astype(float))]
        rb = crit("    readability: H15 agent rewarding dwell in G3", "GM", 10, False, late(A3["g"])[g3])
        m5.append(crit("(b) rewarding dwell, learned / H15 agent", "RGM", 0.75, False, late(L["g"])[g3], late(A3["g"])[g3]) if rb == "PASS" else "UNREADABLE")
    M5 = agg(m5); print(f"   M5 -> {M5}")
    g5 = L["first_g"] >= 0
    print(f"\n== M6 the rewarded value, weight level. G5 = rows rewarded at least once in the learned arm: {int(g5.sum())}/{n} ==")
    M6 = crit("learned value of the rewarded odour at the end", "GM", 0.5, False, L["val"][-1][g5, 0]); print(f"   M6 -> {M6}")
    print("\n== M7 controlled experience with learning ON (E2-C, all rows) ==")
    T, S, A = e2a["trained, learning on"], e2a["sham, frozen"], e2a["H15 agent trained, learning on"]
    mc = [crit("    manipulation check: trained, punished odour before the test", "GM", -0.5, True, T["pre"][:, 1]),
          crit("    manipulation check: sham >= -0.1", "GM", -0.1, False, S["pre"][:, 1]), crit("    manipulation check: sham <= +0.1", "GM", 0.1, True, S["pre"][:, 1])]
    tb, sb = T["b"].sum(0), S["b"].sum(0)
    if not all(x == "PASS" for x in mc): m7 = ["UNREADABLE"]; print("   M7: UNREADABLE, the training did not install the memory")
    else:
        base = crit("    readability: sham punishing dwell over the test", "GM", 10, False, sb)
        m7 = [crit("(a) punishing dwell, trained learning on / sham frozen", "RGM", 0.5, True, tb, sb) if base == "PASS" else "UNREADABLE",
              crit("(b) trained below sham", "WIN", 0.60, False, tb, sb),
              crit("(c) reach the rewarding source, trained - sham", "DP", 0.25, False, (T["first_g"] >= 0).astype(float), (S["first_g"] >= 0).astype(float)),
              crit("(d) reach the rewarding source, Agent14 trained learning on - H15 agent trained learning on", "DP", -0.10, False,
                   (T["first_g"] >= 0).astype(float), (A["first_g"] >= 0).astype(float))]
    for nm in ("trained, frozen", "trained, learning on, as composed (N1)"):
        o = e2a[nm]; print(f"      reported: {nm}: reach R {int((o['first_g'] >= 0).sum())}/{n}, P dwell over the test median {np.median(o['b'].sum(0)):.1f};"
                           f" DP reach vs trained learning on {float((o['first_g'] >= 0).mean() - (T['first_g'] >= 0).mean()):+.4f}")
    M7 = agg(m7); print(f"   M7 -> {M7}")
    print("\n== M8 identities (task seeds) ==")
    ids = ph30.identities(arms, disp, locks + e2l, steps, e2=(e2a, e2d))
    c9, txt = i9(); ids["(i9) the flee reads the learned sign (constructed)"] = c9
    print(f"   {txt}")
    M8 = ok(all(ids.values())); print(f"   M8 -> {M8}; failed {[k_ for k_, v in ids.items() if not v]}")
    print("\n== M9 the mechanism bench, read from its recorded output (reading R8) ==")
    try:
        btxt = open(BENCH_OUT, encoding="utf-8").read(); bl = btxt.split("\n")
        m9l = [x for x in bl if x.startswith("== M9")]; hl = [x for x in bl if x.strip().startswith("ph31.py sha256")]
        print(f"   experiments/h20/ph31_bench.txt sha256 {sha(BENCH_OUT)}; its header: {hl[0].strip() if hl else 'n/a'}; this file sha256 {sha()}")
        print(f"   its M9 line: {m9l[-1] if m9l else 'n/a'}")
        bsha = re.search(r"ph31\.py sha256 ([0-9a-f]{64})", hl[0]).group(1) if hl else None
        print(f"   the bench was run by this same file (reading R14): {bsha == sha()}")
        M9 = ok(len(m9l) == 1 and "M9 PASS" in m9l[0] and bsha == sha())
    except OSError:
        print("   experiments/h20/ph31_bench.txt not found -> M9 FAIL (not run)"); M9 = "FAIL"
    print(f"   M9 -> {M9}")
    print("\n== M10 lost rows and walls (reported, no bar) ==")
    for nm in ph30.AGENT_ARMS:
        o = arms[nm]; reach = (o["last_g"] > o["first_b"])[g3]; wb = o["wall_between"][g3]
        print(f"   {nm}: contacts per agent {o['contacts'].mean():.2f}; near-wall dwell {o['nearwall'].mean()/(3*STEPS)*100:.2f}%; late unrecovered {int(unrec(o).sum())}/{n};"
              f" G3 reach after the first punished step {int(reach.sum())} (with an intervening wall contact {int((reach & wb).sum())})")
    Ms = dict(M1=M1, M2=M2, M3=M3, M4=M4, M5=M5, M6=M6, M7=M7, M8=M8, M9=M9)
    verdict = all(x == "PASS" for x in Ms.values()); fail = any(x == "FAIL" for x in (M2, M3, M4, M5, M6, M7))
    unread = any(x == "UNREADABLE" for x in Ms.values()) or M1 != "PASS" or M8 != "PASS" or M9 != "PASS"
    lab = "PASS" if verdict else "FAIL" if fail else "UNREADABLE" if unread else "INCONCLUSIVE"
    print(f"\n== H20 Stage C Run 2 ==  " + "  ".join(f"{k} {v}" for k, v in Ms.items()) + " (M10 reported) -> " + lab + ": "
          + ("SHOWN: with learning on during the run in the H15 Run 2 world, the adopted agent (Agent14, with the release applied at non-negative holds only; (N2), re-signed in form"
             " for Run 2) uses the positive value it learns at the rewarding source: fewer R-start rows visit the not-yet-learned punisher than with H15 Run 2's agent and than"
             " with its own positive values removed; and it keeps H15 Run 2's long-horizon search, its avoidance of the learned punisher (among the punished rows in which the"
             " no-learning agent ends at the punisher, it dwells there less) and its reach of the reward after avoidance, within Run 2's allowed gaps on the same rows; with a"
             " trained memory and learning on in the test it dwells less at the punisher and reaches the reward more than a sham, as H15 Run 2's agent does."
             if verdict else "NOT shown under the registered criteria" + (" (UNREADABLE, section 8)" if lab == "UNREADABLE" else "")))


# ------------------------------------------------------------------ self-checks
def demo():
    print(f"== H20 Stage C Run 2 self-checks (demo). design {DESIGN} ==")
    header()
    print("   code-path runs in checks 7 and 8 use unregistered demo seeds (3, 4), (5, 6), (7, 8) with 400 rows and 1800 E1 steps / 600 E2 test steps; their numbers are not used anywhere")
    print("   fixed before this recorded demo (recorded by the session that wrote this file before a rate-limit cut-off; not re-run separately): check 5 first used"
          " 39 positive rows of 199 as the 'G3+ under 50' case; resampled, 3 of 50 draws reached 50 or more positive rows (the check's own expectation was wrong,"
          " not the code); now 25 positive rows. After the cut-off: readings R13 and R14 added (see the file header); no bar, seed, arm, rule or statistic changed")
    # 1. imported versions
    assert sha(ph30.__file__) == PH30_SHA and sha(ph30b.__file__) == PH30B_SHA and sha(ph30.BENCH_TXT) == PH30_BENCH_SHA
    print("ok 1  ph30.py, ph30b.py and experiments/h20/ph30_bench.txt are the recorded versions (sha256)")
    # 2. statistics
    stats1(); s1 = ph15.BOOT_SEED; stats2()
    assert s1 == ph30.BENCH["boot"] and ph15.BOOT_SEED == BENCH["boot"] and abs(ph15.QHI - ph15.QLO - 95.0) < 1e-12 and ph15.Z == ph30.Z95
    print(f"ok 2  statistics switch between Run 1's (for (r')) and Run 2's ({ph15.BOOT_SEED}, 95 percent)")
    # 3. the recorder does not disturb a run and classifies
    n, st = 40, 1800
    for nm in ("no-learning", "H15 no-learning"):
        a = ph30.e1_sim(nm, (3, 4), n, st).run(); b = recorded(nm, (3, 4), n, st)
        assert not ph30.end_equal(a, b["o"]), nm
        cl = classes(b, np.arange(n)); assert set(cl.values()) <= set(ph30b.CLS)
    print(f"ok 3  the recorder leaves the run unchanged (every end-of-run record, no-learning and H15 no-learning, 40 x 1800) and classifies every row: {class_counts(cl)}")
    # 4. the re-signed readability on constructed dwell arrays
    rng = np.random.default_rng(7); base = np.r_[np.zeros(88), rng.uniform(16, 32, 111)]
    old = ph15.boot("GM", base); ph15._idx.clear(); new = ph15.boot("GM", base[base > 0])
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        r_old = ph30.crit("x", "GM", 10, False, base); r_new = ph30.crit("x", "GM", 10, False, base[base > 0])
        few = np.r_[np.zeros(160), rng.uniform(16, 32, 39)]; r_few = ph30.crit("x", "GM", 10, False, few[few > 0])
    assert r_old != "PASS" and r_new == "PASS" and r_few == "UNREADABLE", (r_old, r_new, r_few, old, new)
    print(f"ok 4  readability on a two-moded floor (88 zeros, 111 in [16, 32]): over all rows {r_old} {old[0]:.3f} [{old[1]:.3f}, {old[2]:.3f}], over the dwell > 0 rows {r_new};"
          f" 39 dwell > 0 rows: {r_few} (n < 50)")
    # 5. (hR2): passes on such rows, fails when G3+ is too small, fails when the positive rows sit under 10
    few2 = np.r_[np.zeros(174), rng.uniform(16, 32, 25)]
    lb = np.zeros(199); f1 = hr2(lb, base, base, 11, 50); f2 = hr2(lb, few2, few2, 11, 50); low = np.r_[np.zeros(88), rng.uniform(1, 8, 111)]; f3 = hr2(lb, low, low, 11, 50)
    assert f1[0] == 1.0 and f1[3] == 1.0 and f2[0] == 0.0 and f3[0] == 0.0, (f1, f2, f3)
    print(f"ok 5  (hR2) on constructed rows (50 draws): passing floor {f1[0]:.2f} (M4(c) whole {f1[3]:.2f}); 25 positive rows {f2[0]:.2f} (G3+ under 50 in every draw); positives in [1, 8] {f3[0]:.2f}")
    # 6. seeds; ph30's own scan stays valid; the (r') mask finds the seed-carrying lines of ph30_bench.txt
    hits, nums, nf = seeds_unused(); assert not hits, f"a Run 2 seed appears in {hits}"
    hits30, _, nf30 = ph30.seeds_unused(); assert not hits30, f"a Run 1 seed appears in {hits30}"
    src = open(__file__, encoding="utf-8").read(); assert not RUN1_PAT.search(src), "this file names a Run 1 seed"
    ref = open(ph30.BENCH_TXT, encoding="utf-8").read().split("\n"); nm_ = [i + 1 for i, x in enumerate(ref) if RUN1_PAT.search(x)]
    assert len(nm_) >= 4
    print(f"ok 6  seeds {nums} appear in no other file ({nf} scanned; excluded by name ph31.py, ph31_*.txt, h20_stage_c_run2_*.md, master_plan.md, notes/*.md, viewer/*);"
          f" ph30's own seed self-check still clean ({nf30} scanned); this file names no Run 1 seed; the (r') mask covers ph30_bench.txt lines {nm_}")
    # 7. code path of the bench after (r) and (r') (demo seeds, 1800 steps, 50 outer draws)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): v, o = bench(seeds=dict(e1=(3, 4), e2=(5, 6)), steps=1800, full=False, nout=50)
    lines = buf.getvalue().split("\n"); m9 = [x for x in lines if x.startswith("== M9")]
    assert len(m9) == 1 and any(x.startswith("   (hR2)") for x in lines) and any(x.startswith("   (3) G3 rows outside G3+") for x in lines), m9
    print(f"ok 7  bench code path after (r) and (r') runs end to end ({len(lines)} lines; demo seeds; numbers not used)")
    # 8. code path of dev / eval (demo seeds, 1800 E1 steps, 600 E2 test steps)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): main("dev", steps=1800, tsteps=600, seeds=((5, 6), (7, 8)), smoke=True)
    lines = buf.getvalue().split("\n"); fin = [x for x in lines if x.startswith("== H20 Stage C Run 2 ==")]
    assert len(fin) == 1 and any("readability (re-signed)" in x for x in lines), fin
    print(f"ok 8  dev / eval code path runs end to end ({len(lines)} lines; demo seeds; numbers not used)")
    stats2()


if __name__ == "__main__":
    m = ([x for x in sys.argv[1:] if x in ("demo", "bench", "dev", "eval")] or ["demo"])[0]
    sys.stdout = Tee(sys.stdout)
    if m == "demo": demo(); leak_check(); sys.exit(0)
    if m == "bench":
        v, o = bench(); leak_check(); sys.exit(0 if v else 2 if not (o["repro"] and o["rprime"]) else 1 if o["nocand"] else 3)
    main(m); leak_check()
