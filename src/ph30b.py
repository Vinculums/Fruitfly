#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H20 Stage C post-bench diagnosis (measurement only; owner 2026-09-25, '2번 진단 먼저 진행', decision:h20-stage-c-post-bench-diagnosis).

Usage: python ph30b.py      (writes experiments/h20/ph30b_diag.txt, LF line ends)

ph30.py (sha256 checked below against the bench's), design v2 FINAL and the bench verdict (STOPPED by the registered (hR) stop rule,
record:h20-stage-c-bench-result) are untouched: Agent14N2, the harness `Sim`, the arms, G3, G3+, every bar, every rule and every
adopted module are imported as they are; no rule, bar, floor definition or arm is changed, no agent variant is added, nothing is swept.
Bench seeds only (ph30.BENCH['e1'] for the E1-C runs and ph30.BENCH['boot'] for the bootstrap, as ph30 sets it; not written out here,
so ph30's seed self-check stays valid); the development and evaluation seeds (ph30.SEEDS) are not used, and E2 is not run.

Reproduction first: the six bench arms (learned, H15 agent, positive-off, no-learning, known-answer, as composed (N1)) are re-run on the
bench E1 seeds through ph30's own constructor (ph30.e1_sim) and stepped by ph30's own Sim.step; this file only reads state between
steps (a recorder, below). From these runs ph30's own printing functions (ph30.e1_bench_arms, ph30.extras, ph30.crit) and the bench's
(h) and (hR) format strings must reproduce experiments/h20/ph30_bench.txt's (h), (hR) and 'printed beside' lines character for
character (G3 199/200, R-start punisher visits 10 and 64 of 200, the (hR) GM 16.000 [0.000, 19.667], G3+ 111/199). On any mismatch
nothing is measured.

The recorder (per step, after ph30.Sim.step): position after the move, the held odour h (a.held(); nothing changes the selection
circuit between act and the next act), the step's whiffs (captured by wrapping the world's own sense, which draws exactly as before),
the wall contact, the navigation event, the timeout flag (silence > RESET_AFTER before act, ph23.py:69 / ph14.py:66) and, for the
Agent14 arms, the evidence-release flag (ph23.py:70). The recorded dwell is checked against the harness's own (g, b) per block.

(A) The no-learning Agent14 arm's last-third punishing dwell in G3 (the (hR) quantity): distribution; the statistic as ph30 computes it
    (ph15.boot 'GM' = the group median, ph15.py:180, percentile bootstrap ph15.py:184) and as H15 Run 2 computed it (the same function
    at Run 2's 97.5 percent level and bootstrap seed, ph15.py:25, :268); the 0-dwell rows: position, holds, visits and wall contacts over
    the last third, classified by end state; the first-arrival and first-hold record; the same for H15 Run 2's agent without learning
    and beside it the learning arms.
(B) M4(c) as it would read on these runs: WIN / tie / loss on G3+ and on the subsets of G3 with no-learning dwell >= 1, 5, 10; the GM of
    the no-learning dwell in each; alternative floor arms; the paired dwell difference; and, as reference arithmetic, the pass
    probability each reading would have on a new draw of rows like the bench's (rows resampled from the bench G3, each resample judged by
    the registered 5000-resample interval; outer draws from a generator seeded by the sequence [bench bootstrap seed, 2]).
Names no cause beyond what is measured; tests no change.
"""
import sys, os, hashlib, math
import numpy as np
import ph30
import ph15
from ph30 import R, T1, BENCH, late, unrec, q3
from ph9 import STEPS, HIT_R
from ph11 import RESET_AFTER

PH30_SHA = "98822834043de5f31615e73cd4a83444adcef2f1d5e56478356d70ca905059bd"
BENCH_TXT_SHA = "3fec4dc50dd3af4456649cf8b10a494d04a5afe937f5bf1f65bc31f2a2367eec"
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
BENCH_TXT = os.path.join(REPO, "experiments", "h20", "ph30_bench.txt"); OUT = os.path.join(REPO, "experiments", "h20", "ph30b_diag.txt")
BENCH_ARMS = ("learned", "H15 agent", "positive-off", "no-learning", "known-answer", "as composed (N1)")
ARMS = BENCH_ARMS + ("H15 no-learning",)
LAST = slice(T1 - 3*STEPS, T1)                  # the last third: steps 3600-5399
NOUT = int(os.environ.get("PH30B_OUTER", "1000"))


def sha(p=__file__): return hashlib.sha256(open(p, "rb").read()).hexdigest()


_lines = []
def say(s=""): _lines.append(s); print(s, flush=True)


def qs(x, f=".2f"):
    x = np.asarray(x, float)
    if not len(x): return "n/a"
    return "/".join(f"{v:{f}}" for v in np.percentile(x, [0, 10, 25, 50, 75, 90, 100]))


# ------------------------------------------------------------------ the recorder (reads state only; ph30's Sim does every step)
def traced(name):
    seeds = BENCH["e1"]
    s = ph30.e1_sim(name, seeds)                 # ph30's own construction (world, agent, harness), no displacement
    w, a = s.w, s.a; n = a.R
    tr = dict(POS=np.zeros((T1, n, 2), np.float32), H=np.full((T1, n), -1, np.int8), W=np.zeros((T1, n, 2), bool),
              BUMP=np.zeros((T1, n), bool), NAV=np.zeros((T1, n), bool), TO=np.zeros((T1, n), bool), EV=np.zeros((T1, n), bool))
    box = {}; orig = w.sense
    def sense():
        x = orig(); box["w"] = x; return x
    w.sense = sense                               # the world's own sense, called once per step as before; its return is kept
    for t in range(T1):
        to = np.asarray(a.silence) > RESET_AFTER   # the timeout test of the coming act (ph23.py:69; ph14.py:66)
        s.step(t)
        tr["POS"][t] = w.pos; tr["H"][t] = a.held(); tr["W"][t] = box["w"]; tr["BUMP"][t] = w.bumped
        tr["NAV"][t] = a.nav_hit; tr["TO"][t] = to
        if hasattr(a, "due_evidence"): tr["EV"][t] = a.due_evidence
    o = s.finish()
    geo = dict(src=w.src.copy(), good=w.good.copy(), start=w.start.copy(), arena=float(w.arena))
    return name, o, tr, geo


def run_all():
    if ph30.NPROC <= 1: return [traced(a) for a in ARMS]
    import multiprocessing as mp
    with mp.get_context("fork").Pool(ph30.NPROC) as p: return p.map(traced, ARMS, chunksize=1)


# ------------------------------------------------------------------ reproduction
def reproduce(arms):
    say("\n== (0) reproduction (nothing is measured unless every check holds) ==")
    want = open(BENCH_TXT, encoding="utf-8").read().split("\n")
    L, A3, PO = arms["learned"], arms["H15 agent"], arms["positive-off"]
    ps = L["pstart"]; rs = ~ps; g3 = ps & (L["first_b"] >= 0)
    got = []
    head = f"(h) E1-C on bench seeds {BENCH['e1']}, {R} x {T1}; G3 (learned arm) {int(g3.sum())}/{int(ps.sum())}:"   # carries the seeds: compared, not printed
    ph30.e1_bench_arms(arms, g3, got.append)
    Vl, Va, Vp = (L["first_b"] >= 0)[rs], (A3["first_b"] >= 0)[rs], (PO["first_b"] >= 0)[rs]
    pa, dpa, ba = ph30.pp_pair(Vl, Va, -0.05, True); pb, dpb, bb = ph30.pp_pair(Vl, Vp, -0.05, True)
    _, l_a, h_a = ph15.boot("DP", Vl.astype(float), Va.astype(float))
    got.append(f"   (h) M2(a) R-start punisher visits learned {int(Vl.sum())} vs H15 agent {int(Va.sum())}: DP {dpa:+.4f} [{l_a:+.4f}, {h_a:+.4f}], discordant b {ba:.4f}"
               f" (learned only {int((Vl & ~Va).sum())}, H15 agent only {int((~Vl & Va).sum())}); pass probability {pa:.4f}")
    got.append(f"   reported: M2(b) learned vs positive-off {int(Vp.sum())}: DP {dpb:+.4f}, b {bb:.4f}, pass probability {pb:.4f}")
    nlb = late(arms["no-learning"]["b"])[g3]
    hr = ph30.crit("(hR) Agent14 no-learning, GM last-third punishing dwell in the bench G3 (reading R12)", "GM", 10, False, nlb, say=got.append)
    got.append(f"   (hR) STOP RULE: {'STOP: M4(c) would be unreadable' if hr != 'PASS' else 'PASS -> continue'}; G3+ (no-learning dwell > 0) {int((nlb > 0).sum())}/{int(g3.sum())}")
    for nm in BENCH_ARMS: ph30.extras(nm, arms[nm], g3, got.append)
    hit = [ln in want for ln in got]; head_ok = head in want
    say(f"   ph30.py sha256 equals the bench's ({PH30_SHA[:8]}...{PH30_SHA[-4:]}): True; ph30_bench.txt sha256 equals the recorded ({BENCH_TXT_SHA[:8]}...{BENCH_TXT_SHA[-4:]}): True")
    say(f"   the bench's (h) header line (G3 of the learned arm; it carries the bench seeds, so it is compared and not printed) present verbatim: {head_ok}")
    say(f"   lines recomputed here with ph30's own functions and format strings, present verbatim in ph30_bench.txt: {sum(hit)}/{len(hit)}")
    for ln, h in zip(got, hit): say(f"   {'==' if h else '!='} {ln.strip()}")
    checks = {"G3 199": int(g3.sum()) == 199, "G3+ 111": int((nlb > 0).sum()) == 111, "R-start P visits learned 10": int(Vl.sum()) == 10,
              "R-start P visits H15 agent 64": int(Va.sum()) == 64}
    pt, lo, hi = ph15.boot("GM", nlb)
    checks["GM 16.000 [0.000, 19.667]"] = (f"{pt:.3f}", f"{lo:.3f}", f"{hi:.3f}") == ("16.000", "0.000", "19.667")
    say("   named checks: " + "; ".join(f"{k} {v}" for k, v in checks.items()))
    ok = head_ok and all(hit) and all(checks.values())
    say(f"   reproduction holds: {ok}")
    return ok, g3


def dwell_check(o, tr, geo):
    """the recorded positions give the harness's own per-block dwell at both sources"""
    src, good = geo["src"], geo["good"]; r = np.arange(len(good))
    d = [np.linalg.norm(tr["POS"] - src[None, :, k, :].astype(np.float32), axis=2) for k in (0, 1)]
    at = np.stack([np.linalg.norm(tr["POS"].astype(float) - src[None, :, k, :], axis=2) < HIT_R for k in (0, 1)], 2)
    g = at[:, r, good]; b = at[:, r, 1 - good]
    ok = np.array_equal(g.reshape(9, STEPS, -1).sum(1), o["g"]) and np.array_equal(b.reshape(9, STEPS, -1).sum(1), o["b"])
    return ok, g, b


# ------------------------------------------------------------------ per-row records
def episodes(h):
    """segments of constant held odour: list of (odour, start, end) with end exclusive"""
    ch = np.flatnonzero(np.diff(h) != 0) + 1; st = np.r_[0, ch]; en = np.r_[ch, len(h)]
    return [(int(h[s]), int(s), int(e)) for s, e in zip(st, en) if h[s] >= 0]


def visits(atg, atb):
    """sequence of source visits ('R' / 'P'), each a maximal run of steps within HIT_R of one source"""
    lab = np.where(atg, 1, np.where(atb, 2, 0)); ch = np.flatnonzero(np.diff(lab) != 0) + 1
    st = np.r_[0, ch]; seq = [("R" if lab[s] == 1 else "P", int(s)) for s in st if lab[s] > 0]
    return seq


def compress(seq):
    if not seq: return "-"
    out = []; cur, k = seq[0][0], 0
    for c, _ in seq:
        if c == cur: k += 1
        else: out.append(f"{cur}{k}"); cur, k = c, 1
    out.append(f"{cur}{k}"); return " ".join(out)


def rowrec(o, tr, geo, g, b, rows):
    src, good, start = geo["src"], geo["good"], geo["start"]; A = geo["arena"]
    recs = {}
    for r in rows:
        P, Rr = 1 - good[r], good[r]
        pos = tr["POS"][:, r, :].astype(float)
        dP = np.linalg.norm(pos - src[r, P], axis=1); dR = np.linalg.norm(pos - src[r, Rr], axis=1)
        h = tr["H"][:, r]; W = tr["W"][:, r, :]
        ep = episodes(h)
        first = ep[0] if ep else None
        if first is not None:
            od, s0, e0 = first
            cause = "held to the end" if e0 >= T1 else ("evidence release" if tr["EV"][e0, r] else "timeout drive" if tr["TO"][e0, r] else "other")
            nxt = "-" if e0 >= T1 else ("none" if h[e0] < 0 else ("R" if h[e0] == Rr else "P"))
            fh = dict(odour="R" if od == Rr else "P", start=s0, dur=e0 - s0, cause=cause, next=nxt)
        else: fh = None
        endings = {"evidence": 0, "timeout": 0, "other": 0, "open": 0}
        pend = []
        for od, s0, e0 in ep:
            if od == P:
                if e0 >= T1: endings["open"] += 1
                elif tr["EV"][e0, r]: endings["evidence"] += 1
                elif tr["TO"][e0, r]: endings["timeout"] += 1
                else: endings["other"] += 1
        # the first change of hold from P to R (directly or through nothing held)
        p2r = None; lastod = None
        for od, s0, e0 in ep:
            if lastod == P and od == Rr: p2r = s0; break
            lastod = od
        hprev = np.r_[-1, h[:-1]]                                        # the hold when the step's whiff arrives (the previous act's)
        fR = next((s0 for od, s0, e0 in ep if od == Rr), None)           # the first step an R hold is formed
        lim = T1 if fR is None else fR
        rw = W[:lim, Rr]; exp_ = dict(total=int(rw.sum()), none=int((rw & (hprev[:lim] < 0)).sum()), heldP=int((rw & (hprev[:lim] == P)).sum()))
        if fR is not None:
            yP, yR = src[r, P, 1], src[r, Rr, 1]
            prevend = max([e0 for od, s0, e0 in ep if e0 <= fR] or [-1])
            atR = dict(step=fR, along=float(pos[fR, 0] - src[r, P, 0]), cross=float((pos[fR, 1] - yP)/(yR - yP)),
                       before="nothing" if hprev[fR] < 0 else ("P" if hprev[fR] == P else "R"), gap=(fR - prevend) if prevend >= 0 else -1)
        else: atR = None
        seq = visits(g[:, r], b[:, r])
        lastP = int(o["last_b"][r]); after = [s for c, s in seq if c == "R" and s > lastP]
        L_ = LAST
        nearwall = (np.minimum(pos[L_], A - pos[L_]).min(1) < 1.0).sum()
        recs[r] = dict(
            dP_med=float(np.median(dP[L_])), dR_med=float(np.median(dR[L_])), dP_min=float(dP[L_].min()), dR_min=float(dR[L_].min()),
            dP_end=float(dP[-1]), dR_end=float(dR[-1]), along_end=float(pos[-1, 0] - src[r, P, 0]),
            atR=int(g[L_, r].sum()), atP=int(b[L_, r].sum()), wP=int(W[L_, P].sum()), wR=int(W[L_, Rr].sum()),
            heldP=float((h[L_] == P).mean()), heldR=float((h[L_] == Rr).mean()), held0=float((h[L_] < 0).mean()),
            heldP_all=float((h == P).mean()), heldR_all=float((h == Rr).mean()),
            bumps_L=int(tr["BUMP"][L_, r].sum()), bumps=int(tr["BUMP"][:, r].sum()), nearwall_L=int(nearwall),
            first_hold=fh, expR=exp_, firstRhold=atR, nhold=len(ep), p2r=p2r, pend=endings, seq=seq, pattern=compress(seq),
            switches=sum(1 for i in range(1, len(seq)) if seq[i][0] != seq[i - 1][0]),
            first_src=(seq[0][0] if seq else "-"), first_step=(seq[0][1] if seq else -1),
            last_src=(seq[-1][0] if seq else "-"), lastP=lastP, firstR=int(o["first_g"][r]), R_after_lastP=(after[0] if after else -1),
            near6P=bool((dP[L_] < 2*HIT_R).any()), whiff_any_L=bool(W[L_].any()), plume_late=bool(o["plume_late"][r]),
            dwell_blocks_P=o["b"][:, r].astype(int).tolist(), dwell_blocks_R=o["g"][:, r].astype(int).tolist())
    return recs


def classify(rec):
    if rec["atR"] > 0: return "i"
    if rec["atP"] > 0: return "ii"
    if not rec["whiff_any_L"]: return "iii"
    if rec["bumps_L"] > 0 or rec["nearwall_L"] > 0: return "iv"
    return "v"


CLS = {"i": "(i) at the reward source (a last-third step within HIT_R of R)", "ii": "(ii) at the punisher source but not counted",
       "iii": "(iii) lost (no whiff of either odour in the last third)", "iv": "(iv) at a wall (a contact or a step within 1.0 of a wall in the last third)",
       "v": "(v) other"}


def med(x, f=".1f"):
    x = [v for v in x if v is not None]
    return f"{np.median(x):{f}}" if len(x) else "n/a"


def group_summary(lab, recs, rows, ev=True):
    rs_ = [recs[r] for r in rows]; n = len(rs_)
    if not n: say(f"   {lab}: n 0"); return
    fh = [x["first_hold"] for x in rs_]
    say(f"   {lab} (n {n}): last third: median distance to P {med([x['dP_med'] for x in rs_])} (row medians; quartiles {q3([x['dP_med'] for x in rs_], '.1f')}),"
        f" to R {med([x['dR_med'] for x in rs_])} ({q3([x['dR_med'] for x in rs_], '.1f')}); steps within HIT_R of R {q3([x['atR'] for x in rs_])}, of P {q3([x['atP'] for x in rs_])};"
        f" whiffs P {q3([x['wP'] for x in rs_])}, R {q3([x['wR'] for x in rs_])}; share of steps holding P {med([x['heldP'] for x in rs_], '.3f')}, R {med([x['heldR'] for x in rs_], '.3f')},"
        f" nothing {med([x['held0'] for x in rs_], '.3f')}; rows with a last-third wall contact {sum(x['bumps_L'] > 0 for x in rs_)}, whole-run contacts {sum(x['bumps'] for x in rs_)};"
        f" rows within 2 x HIT_R of P on some last-third step {sum(x['near6P'] for x in rs_)}; late unrecovered (no plume whiff, blocks 7-9) {sum(not x['plume_late'] for x in rs_)}")
    say(f"      first source reached: P {sum(x['first_src'] == 'P' for x in rs_)}, R {sum(x['first_src'] == 'R' for x in rs_)}, none {sum(x['first_src'] == '-' for x in rs_)};"
        f" first arrival step {q3([x['first_step'] for x in rs_ if x['first_step'] >= 0])}; last source visited: P {sum(x['last_src'] == 'P' for x in rs_)}, R {sum(x['last_src'] == 'R' for x in rs_)},"
        f" none {sum(x['last_src'] == '-' for x in rs_)}; source switches {q3([x['switches'] for x in rs_])} (0: {sum(x['switches'] == 0 for x in rs_)}, 1: {sum(x['switches'] == 1 for x in rs_)},"
        f" 2+: {sum(x['switches'] >= 2 for x in rs_)}); last step at P {q3([x['lastP'] for x in rs_ if x['lastP'] >= 0])}; first step at R {q3([x['firstR'] for x in rs_ if x['firstR'] >= 0])}"
        f" (rows reaching R {sum(x['firstR'] >= 0 for x in rs_)}); an R arrival after the last P step {sum(x['R_after_lastP'] >= 0 for x in rs_)}")
    fo = [x for x in fh if x is not None]
    say(f"      first hold: odour P {sum(x['odour'] == 'P' for x in fo)}, R {sum(x['odour'] == 'R' for x in fo)}, never held {n - len(fo)}; formed at step {q3([x['start'] for x in fo])};"
        f" duration {q3([x['dur'] for x in fo])} (min {min([x['dur'] for x in fo]) if fo else 0}, max {max([x['dur'] for x in fo]) if fo else 0}); ended by: "
        + ", ".join(f"{c if ev or c != 'other' else 'no timeout flag (evidence release or decay; the evidence flag is not exposed by Agent3)'} {sum(x['cause'] == c for x in fo)}"
                    for c in (("evidence release", "timeout drive", "other", "held to the end") if ev else ("timeout drive", "other", "held to the end")))
        + "; next held: " + ", ".join(f"{c} {sum(x['next'] == c for x in fo)}" for c in ("R", "P", "none", "-")))
    pe = {k: sum(x["pend"][k] for x in rs_) for k in ("evidence", "timeout", "other", "open")}
    say(f"      every P hold over the run ended by: " + (f"evidence release {pe['evidence']}, timeout drive {pe['timeout']}, other {pe['other']}" if ev else
        f"timeout flag set {pe['timeout']}, no timeout flag (evidence release or decay, not separated for Agent3) {pe['other'] + pe['evidence']}") + f", still held at the end {pe['open']};"
        f" hold episodes per row {q3([x['nhold'] for x in rs_])}; a P -> R change of hold {sum(x['p2r'] is not None for x in rs_)} (first at step {q3([x['p2r'] for x in rs_ if x['p2r'] is not None])});"
        f" whole-run share of steps holding P {med([x['heldP_all'] for x in rs_], '.3f')}, R {med([x['heldR_all'] for x in rs_], '.3f')}")
    ex = [x["expR"] for x in rs_]; fr = [x["firstRhold"] for x in rs_ if x["firstRhold"] is not None]
    say(f"      R whiffs sensed before the first R hold (or over the run if none forms): per row {q3([e['total'] for e in ex])} (rows with none {sum(e['total'] == 0 for e in ex)});"
        f" of them arriving with nothing held {q3([e['none'] for e in ex])} (rows with at least one {sum(e['none'] > 0 for e in ex)}), with P held {q3([e['heldP'] for e in ex])}"
        f" (rows with at least one {sum(e['heldP'] > 0 for e in ex)}); rows forming an R hold {len(fr)}")
    if fr:
        say(f"      at the first R hold: step {q3([f['step'] for f in fr])}; held before it: nothing {sum(f['before'] == 'nothing' for f in fr)}, P {sum(f['before'] == 'P' for f in fr)};"
            f" steps since the previous hold ended {q3([f['gap'] for f in fr if f['gap'] >= 0])}; position along the wind from the sources' line (+ downwind) {q3([f['along'] for f in fr], '.1f')};"
            f" crosswind as a fraction from the P axis (0) to the R axis (1) {q3([f['cross'] for f in fr], '.2f')}")


# ------------------------------------------------------------------ statistics
def boot_ci(x, stat):
    i = ph15._resample(len(x)); xs = np.asarray(x, float)
    pt = stat(xs); bs = stat(xs[i]); lo, hi = np.nanpercentile(bs, [ph15.QLO, ph15.QHI]); return float(pt), float(lo), float(hi), bs


def gm_line(lab, x):
    pt, lo, hi = ph15.boot("GM", x); rd = ph15.verdict(lo, hi, 10, False)
    return pt, lo, hi, rd


def win_counts(xl, xf):
    xl, xf = np.asarray(xl), np.asarray(xf); n = len(xl)
    k = int((xl < xf).sum()); t = int((xl == xf).sum()); l = int((xl > xf).sum())
    if n == 0: return n, k, t, l, float("nan"), float("nan"), float("nan"), "n 0"
    p, lo, hi = ph15.wilson(k, n); ties = t/n
    rd = "UNREADABLE (n < 50)" if n < 50 else "UNREADABLE (ties)" if ties > 0.20 else ph15.verdict(lo, hi, 0.60, False)
    return n, k, t, l, p, lo, hi, rd


def kmin_win(n):
    for k in range(n + 1):
        if ph30.wilson95(k, n)[0] >= 0.60: return k
    return None


def binom_ge(k, n, p): return 1.0 - ph30.binom_le(k - 1, n, p) if k > 0 else 1.0


def judge_draw(xl, xf, xa, modes):
    """one draw of G3 rows: {mode: (readability PASS, RGM PASS, WIN PASS)} (reference arithmetic). Every interval is ph15.boot's (the
    registered 5000-resample percentile interval); its resample cache is emptied first so that memory stays bounded (the indices are
    regenerated from the same seed, i.e. the same indices)."""
    def gm_lo(x):
        if len(x) < 50: return None
        ph15._idx.clear(); return ph15.boot("GM", x)[1]
    def rgm_ok(a, b):
        ph15._idx.clear(); hi = ph15.boot("RGM", a, b)[2]; return bool(np.isfinite(hi) and hi <= 0.75)
    def win_ok(a, b):
        n = len(a)
        if n < 50: return False
        k = int((a < b).sum()); ties = float((a == b).mean())
        return ties <= 0.20 and ph30.wilson95(k, n)[0] >= 0.60
    rg_nl, rg_a3 = rgm_ok(xl, xf), rgm_ok(xl, xa); out = {}
    for m in modes:
        f = xa if m == "H15 floor" else xf
        if m in ("present", "H15 floor"): rsub = np.ones(len(f), bool); wsub = f > 0
        elif m == ">0": rsub = wsub = f > 0
        else: rsub = wsub = f >= float(m)
        lo = gm_lo(f[rsub]); out[m] = (lo is not None and lo >= 10, rg_a3 if m == "H15 floor" else rg_nl, win_ok(xl[wsub], f[wsub]))
    return out


# ------------------------------------------------------------------ main
def main():
    ok30, okt = sha(ph30.__file__) == PH30_SHA, sha(BENCH_TXT) == BENCH_TXT_SHA
    say(f"== H20 Stage C post-bench diagnosis (measurement only; owner 2026-09-25, '2번 진단 먼저 진행'). ph30b.py sha256 {sha()}; ph30.py sha256 {sha(ph30.__file__)};"
        f" design {ph30.DESIGN}; reproduces experiments/h20/ph30_bench.txt sha256 {sha(BENCH_TXT)} (record:h20-stage-c-bench-result) ==")
    say("   imported modules (as ph30 prints them): " + "; ".join(f"{os.path.basename(m.__file__)} {sha(m.__file__)}" for m in ph30.MODS))
    say("   seeds: the bench E1 seeds (ph30.BENCH['e1']) and the bench bootstrap seed (ph30.BENCH['boot'], 95 percent, 5000 resamples), read from ph30 and not written out here;"
        " the development and evaluation seeds (ph30.SEEDS) and the E2 bench seeds are not used; no E2 run")
    say(f"   bootstrap as ph30 sets it: level {ph15.QHI - ph15.QLO:.1f} percent (percentiles {ph15.QLO}/{ph15.QHI}); ph15.boot 'GM' is the group median (ph15.py:180; spec v3 line 36 'GM = a group median')")
    if not (ok30 and okt):
        say(f"== ph30.py sha256 matches: {ok30}; ph30_bench.txt sha256 matches: {okt}: STOP, nothing is run =="); return False
    res = run_all()
    arms = {nm: o for nm, o, _, _ in res}; trs = {nm: t for nm, _, t, _ in res}; geos = {nm: g for nm, _, _, g in res}
    ok, g3 = reproduce(arms)
    if not ok:
        say("== (0) NOT reproduced: nothing is measured =="); return False
    same_world = all(np.array_equal(geos[nm]["src"], geos["no-learning"]["src"]) and np.array_equal(geos[nm]["good"], geos["no-learning"]["good"]) for nm in ARMS)
    GB = {}
    for nm in ARMS:
        okd, g, b = dwell_check(arms[nm], trs[nm], geos[nm]); GB[nm] = (okd, g, b)
    say(f"   recorder check: every arm in the same world draw {same_world}; the dwell recomputed from the recorded positions (HIT_R {HIT_R}) equals the harness's per-block g and b: "
        + ", ".join(f"{nm} {GB[nm][0]}" for nm in ARMS))
    if not (same_world and all(v[0] for v in GB.values())):
        say("== recorder check failed: nothing is measured =="); return False
    L, NL, A3N, A3 = arms["learned"], arms["no-learning"], arms["H15 no-learning"], arms["H15 agent"]
    ps = L["pstart"]; rows = np.arange(R); G3 = rows[g3]
    nlb = late(NL["b"])[g3]; zero = G3[nlb == 0]; posr = G3[nlb > 0]

    # ---------------------------------------------------------------- (A1)
    say("\n== (A1) the (hR) quantity: Agent14 no-learning, last-third punishing dwell (mean steps within HIT_R of the punisher per 600-step block, blocks 7-9) over G3 ==")
    say(f"   G3 = P-start rows with a punished step in the learned arm (ph30 reading R11): {len(G3)}/{int(ps.sum())}; the P-start row outside G3: {rows[ps & ~g3].tolist()}"
        f" (its learned-arm first punished step {L['first_b'][ps & ~g3].tolist()}, no-learning last-third P dwell {late(NL['b'])[ps & ~g3].round(3).tolist()})")
    say(f"   rows with dwell exactly 0: {int((nlb == 0).sum())}/{len(nlb)} ({(nlb == 0).mean()*100:.1f} percent); above 0 (G3+): {int((nlb > 0).sum())}")
    say(f"   quantiles min/p10/p25/median/p75/p90/max, all G3: {qs(nlb)}; G3+ only: {qs(nlb[nlb > 0])}")
    edges = [(0, 0, "0"), (0, 1, "(0, 1)"), (1, 5, "[1, 5)"), (5, 10, "[5, 10)"), (10, 15, "[10, 15)"), (15, 20, "[15, 20)"), (20, 25, "[20, 25)"), (25, 30, "[25, 30)"), (30, 1e9, ">= 30")]
    def hist(x): return "; ".join(f"{lab} {int(((x == 0) if hi == 0 else ((x > lo) & (x < hi)) if lo == 0 else ((x >= lo) & (x < hi))).sum())}" for lo, hi, lab in edges)
    say(f"   histogram (bins at the readability bar 10 and in steps of 5): {hist(nlb)}")
    pt, lo, hi, rd = gm_line("", nlb)
    say(f"   GM as ph30 computes it (ph15.boot 'GM', ph15.py:180-185: np.median of the 199 values, zeros included as values, neither excluded nor floored; 95 percent percentile"
        f" bootstrap): {pt:.3f} [{lo:.3f}, {hi:.3f}] -> 'at least 10' {rd}")
    ph15._idx.clear(); i = ph15._resample(len(nlb)); zc = (nlb[i] == 0).sum(1); mb = np.median(nlb[i], 1)
    say(f"   the resamples: zero rows per resample {q3(zc)} (min {zc.min()}, max {zc.max()}); resamples with 100 or more zero rows of 199 (median then 0) {int((zc >= 100).sum())}/5000"
        f" = {(zc >= 100).mean()*100:.2f} percent; resample medians equal to 0: {int((mb == 0).sum())}/5000 = {(mb == 0).mean()*100:.2f} percent; resample medians below 10: {int((mb < 10).sum())}/5000"
        f" = {(mb < 10).mean()*100:.2f} percent (the lower 2.5 percent point is 0 because more than 2.5 percent of the resample medians are 0)")
    mpt, mlo, mhi, _ = boot_ci(nlb, lambda x: x.mean(-1))
    say(f"   for reference, the arithmetic mean: {mpt:.3f} [{mlo:.3f}, {mhi:.3f}] (same resamples); the mean over G3+ only: {nlb[nlb > 0].mean():.3f}")
    with ph30.run2_stats():
        p2, l2, h2 = ph15.boot("GM", nlb); r2 = ph15.verdict(l2, h2, 10, False)
        ph15._idx.clear(); i2 = ph15._resample(len(nlb)); z2 = (nlb[i2] == 0).sum(1)
        a3b = late(A3N["b"])[g3]; p3_, l3_, h3_ = ph15.boot("GM", a3b); r3_ = ph15.verdict(l3_, h3_, 10, False)
        lev = ph15.QHI - ph15.QLO
    say(f"   the same data under H15 Run 2's computation of the same quantity (ph15.py:268 crit('readability: no-learning punishing dwell in G3', 'GM', 10, False, late(N['b'])[g3]),"
        f" the same function at Run 2's {lev:.1f} percent level and Run 2's bootstrap seed, ph15.py:25): {p2:.3f} [{l2:.3f}, {h2:.3f}] -> {r2}; resamples with 100+ zero rows {int((z2 >= 100).sum())}/5000")
    say(f"   side by side (reported, not a re-judgement): ph30 (95 percent, bench bootstrap seed) {pt:.3f} [{lo:.3f}, {hi:.3f}] {rd} | Run 2's computation {p2:.3f} [{l2:.3f}, {h2:.3f}] {r2}"
        f" | H15 Run 2's own agent without learning on these rows at Run 2's computation {p3_:.3f} [{l3_:.3f}, {h3_:.3f}] {r3_}; H15 Run 2 eval (Agent3 no-learning, its own seeds) 20.667 [18.333, 22.667]")
    say("   the dwell radius: ph30's Sim counts b = w.at_source() (ph30.py Sim.step, as ph15.py:94, :100), w.at_source is ph11.py:103 (distance < HIT_R, ph9.py:31 HIT_R 3.0) in both;"
        " the definitions are the same code; recomputed from the recorded positions above: equal")

    # ---------------------------------------------------------------- (A2)
    say("\n== (A2) where the 0-dwell rows are over the last third (steps 3600-5399), with the G3+ rows beside ==")
    recs = rowrec(NL, trs["no-learning"], geos["no-learning"], GB["no-learning"][1], GB["no-learning"][2], G3)
    cls = {r: classify(recs[r]) for r in zero}
    say("   classes (exclusive, in this order): " + "; ".join(f"{CLS[c]} {sum(v == c for v in cls.values())}" for c in CLS))
    ov = dict(R_and_nowhiff=sum(recs[r]["atR"] > 0 and not recs[r]["whiff_any_L"] for r in zero), R_and_wall=sum(recs[r]["atR"] > 0 and (recs[r]["bumps_L"] > 0 or recs[r]["nearwall_L"] > 0) for r in zero),
              near6P=sum(recs[r]["near6P"] for r in zero))
    say(f"   overlaps: class (i) rows with no whiff in the last third {ov['R_and_nowhiff']}, class (i) rows also near a wall {ov['R_and_wall']};"
        f" 0-dwell rows within 2 x HIT_R (6.0) of the punisher on some last-third step without being within HIT_R {ov['near6P']}")
    for c in CLS:
        rr = [r for r in zero if cls[r] == c]
        if rr: group_summary(f"class {c}", recs, rr)
    group_summary("all 0-dwell rows", recs, list(zero))
    group_summary("G3+ rows (no-learning dwell > 0)", recs, list(posr))
    hi20 = G3[nlb >= 20]; group_summary("high-dwell rows (no-learning dwell >= 20)", recs, list(hi20))
    say("   per 0-dwell row: row | class | last-third steps at R / at P, whiffs R/P | median distance to R / P (last third) | first hold odour, formed, duration, ended by -> next |"
        " visit pattern (R/P runs) | last step at P, first step at R | contacts (last third / run)")
    for r in zero:
        x = recs[r]; f = x["first_hold"] or dict(odour="-", start=-1, dur=0, cause="-", next="-")
        say(f"     {r:3d} | {cls[r]:3s} | {x['atR']:3d}/{x['atP']:d}, {x['wR']:3d}/{x['wP']:d} | {x['dR_med']:5.1f} / {x['dP_med']:5.1f} | {f['odour']} {f['start']:4d} {f['dur']:4d} {f['cause']} -> {f['next']} |"
            f" {x['pattern']} | {x['lastP']:4d}, {x['firstR']:4d} | {x['bumps_L']}/{x['bumps']}")

    # ---------------------------------------------------------------- (A3)
    say("\n== (A3) first arrivals and the 'never left a source it found' reading (no-learning Agent14, G3) ==")
    for lab, rr in (("0-dwell", zero), ("G3+", posr)):
        xs = [recs[r] for r in rr]
        onlyP = sum(x["pattern"].startswith("P") and "R" not in x["pattern"] for x in xs)
        P_then_R = sum(x["pattern"].startswith("P") and x["switches"] == 1 and x["last_src"] == "R" for x in xs)
        back = sum(x["switches"] >= 2 for x in xs)
        endR = sum(x["last_src"] == "R" for x in xs); endP = sum(x["last_src"] == "P" for x in xs)
        say(f"   {lab} (n {len(xs)}): visit patterns: P only {onlyP}; P then R and never back to P (one switch) {P_then_R}; two or more switches {back}; last visited source R {endR}, P {endP};"
            f" first hold P and held to the end {sum(1 for x in xs if x['first_hold'] and x['first_hold']['odour'] == 'P' and x['first_hold']['cause'] == 'held to the end')}")
    s0 = [recs[r]["switches"] for r in zero]; s1 = [recs[r]["switches"] for r in posr]
    say(f"   source switches, 0-dwell rows {q3(s0)} vs G3+ rows {q3(s1)}; rows back at the punisher after their first R arrival (last P step > first R step):"
        f" 0-dwell {sum(1 for r in zero if recs[r]['lastP'] > recs[r]['firstR'] >= 0)}, G3+ {sum(1 for r in posr if recs[r]['lastP'] > recs[r]['firstR'] >= 0)}")
    lp0 = [recs[r]["lastP"] for r in zero]
    say(f"   0-dwell rows: last step at the punisher {qs(lp0, '.0f')} (min/p10/p25/median/p75/p90/max); rows whose last P step falls in block 1 {sum(v < 600 for v in lp0)}, blocks 2-3 {sum(600 <= v < 1800 for v in lp0)},"
        f" blocks 4-6 {sum(1800 <= v < 3600 for v in lp0)}")

    # ---------------------------------------------------------------- (A4)
    say("\n== (A4) the same quantity in the other arms on the same rows (G3 of the learned arm; last-third punishing dwell) ==")
    say("   arm | rows at 0 | G3+ by its own dwell | quantiles min/p10/p25/median/p75/p90/max | GM [95 percent] 'at least 10' | mean [95 percent]")
    for nm in ("no-learning", "H15 no-learning", "learned", "H15 agent", "positive-off", "as composed (N1)", "known-answer"):
        x = late(arms[nm]["b"])[g3]; p_, l_, h_, r_ = gm_line("", x); ph15._idx.clear(); m_, ml, mh, _ = boot_ci(x, lambda y: y.mean(-1))
        say(f"   {nm:17s} | {int((x == 0).sum()):3d} | {int((x > 0).sum()):3d} | {qs(x)} | {p_:.3f} [{l_:.3f}, {h_:.3f}] {r_} | {m_:.3f} [{ml:.3f}, {mh:.3f}]")
    rA = rowrec(A3N, trs["H15 no-learning"], geos["H15 no-learning"], GB["H15 no-learning"][1], GB["H15 no-learning"][2], G3)
    a3b = late(A3N["b"])[g3]; z3 = G3[a3b == 0]; c3 = {r: classify(rA[r]) for r in z3}
    say(f"   H15 Run 2's agent without learning (Agent3, abl 'learn'), its 0-dwell rows ({len(z3)}), classes: " + "; ".join(f"{c} {sum(v == c for v in c3.values())}" for c in CLS))
    group_summary("H15 no-learning 0-dwell rows", rA, list(z3), ev=False)
    group_summary("H15 no-learning G3+ rows", rA, list(G3[a3b > 0]), ev=False)
    both0 = int(((nlb == 0) & (a3b == 0)).sum())
    say(f"   0 in both no-learning arms {both0}; 0 in Agent14 only {int(((nlb == 0) & (a3b > 0)).sum())}; 0 in Agent3 only {int(((nlb > 0) & (a3b == 0)).sum())}")
    say(f"   H15 no-learning histogram: {hist(a3b)}")

    # ---------------------------------------------------------------- (A5)
    say("\n== (A5) the G3 / G3+ definitions on these runs ==")
    say(f"   G3: P-start rows with at least one punished step in the learned arm (ph30.py reading R11; bench line (h)): {len(G3)}/{int(ps.sum())};"
        f" the same rows are punished at least once in the no-learning arm: {int((NL['first_b'][g3] >= 0).sum())}/{len(G3)}")
    say(f"   G3+: G3 rows whose no-learning last-third punishing dwell is above 0 (ph30.py reading R11, judge()): {len(posr)}; the {len(zero)} rows outside G3+ are by definition the 0-dwell rows of (A1)-(A3)")

    # ---------------------------------------------------------------- (B1)
    say("\n== (B1) M4(c) as it would read on these runs with the registered floor (Agent14 no-learning; reported, the (hR) rule made it unreadable) ==")
    lb = late(L["b"])[g3]
    n, k, t, l_, p_, lo_, hi_, rd_ = win_counts(lb[nlb > 0], nlb[nlb > 0])
    say(f"   WIN learned below no-learning on G3+: n {n}; wins {k}, ties {t}, losses {l_}; tie fraction {t/n:.3f} (rule: unreadable above 0.20); win share {p_:.3f}, Wilson 95 [{lo_:.3f}, {hi_:.3f}]"
        f" 'at least 0.60' -> {rd_}")
    n0, k0, t0, l0, *_ = win_counts(lb, nlb)
    say(f"   (for reference) the same WIN over all G3 as Run 2 read Q3(c): n {n0}; wins {k0}, ties {t0} ({t0/n0*100:.1f} percent), losses {l0}")
    ph15._idx.clear(); rp, rl, rh = ph15.boot("RGM", lb, nlb)
    say(f"   RGM learned / no-learning over G3 (the second part of M4(c)): {rp:.3f} [{rl:.3f}, {rh:.3f}] 'at most 0.75' -> {ph15.verdict(rl, rh, 0.75, True)}")
    ph15._idx.clear(); ap, al, ah = ph15.boot("GM", L["val"][-1][g3, 1]); ph15._idx.clear(); bp, bl, bh = ph15.boot("GM", lb)
    say(f"   M4(a) GM learned punished value at the end over G3: {ap:.3f} [{al:.3f}, {ah:.3f}] 'at most -0.5' -> {ph15.verdict(al, ah, -0.5, True)};"
        f" M4(b) GM learned last-third punishing dwell over G3: {bp:.3f} [{bl:.3f}, {bh:.3f}] 'at most 1.0' -> {ph15.verdict(bl, bh, 1.0, True)}; learned dwell above 0 in {int((lb > 0).sum())}/{len(lb)} G3 rows")
    say("   (M4(b) and M4(c) are gated by the readability rule in ph30.judge; the values above are printed as they would read, not as a verdict)")

    # ---------------------------------------------------------------- (B2)
    say("\n== (B2) the WIN restricted to subsets of G3 by the no-learning dwell, and the no-learning GM in each (measured on the same runs; no rule proposed) ==")
    say("   subset | n | wins / ties / losses | tie fraction | win share [Wilson 95] 'at least 0.60' | no-learning GM in the subset [95 percent] 'at least 10' | smallest passing k, P(K >= k) at the bench share")
    subsets = [("G3 (all)", np.ones(len(nlb), bool)), ("dwell > 0 (G3+, registered)", nlb > 0), ("dwell >= 1", nlb >= 1), ("dwell >= 5", nlb >= 5), ("dwell >= 10", nlb >= 10)]
    for lab, m in subsets:
        n, k, t, l_, p_, lo_, hi_, rd_ = win_counts(lb[m], nlb[m]); ph15._idx.clear(); gp, gl, gh = ph15.boot("GM", nlb[m]); gr = ph15.verdict(gl, gh, 10, False)
        km = kmin_win(n); pk = binom_ge(km, n, k/n) if km is not None else float("nan")
        say(f"   {lab:28s} | {n:3d} | {k:3d} / {t:3d} / {l_:3d} | {t/n:.3f} | {p_:.3f} [{lo_:.3f}, {hi_:.3f}] {rd_} | {gp:.3f} [{gl:.3f}, {gh:.3f}] {gr} | {km}, {pk:.4f}")

    # ---------------------------------------------------------------- (B3)
    say("\n== (B3) other arms as the floor, measured (no rule proposed): GM of the arm's last-third punishing dwell over G3, and the WIN learned below it on that arm's own dwell > 0 rows ==")
    for nm in ("no-learning", "H15 no-learning", "positive-off", "as composed (N1)", "H15 agent"):
        f = late(arms[nm]["b"])[g3]; ph15._idx.clear(); gp, gl, gh = ph15.boot("GM", f); gr = ph15.verdict(gl, gh, 10, False)
        n, k, t, l_, p_, lo_, hi_, rd_ = win_counts(lb[f > 0], f[f > 0])
        say(f"   floor {nm:17s}: rows at 0 {int((f == 0).sum())}/{len(f)}; GM {gp:.3f} [{gl:.3f}, {gh:.3f}], lower bound >= 10: {gl >= 10} ({gr});"
            f" WIN on its dwell > 0 rows: n {n}, wins {k}, ties {t}, losses {l_}" + (f", tie fraction {t/n:.3f}, share {p_:.3f} [{lo_:.3f}, {hi_:.3f}] {rd_}" if n else ""))
    po = arms["positive-off"]; pn = arms["as composed (N1)"]
    say(f"   positive-off in G3 (learning on, positive values removed from the read-out): punished at least once {int((po['first_b'][g3] >= 0).sum())}/{len(G3)};"
        f" learned punished value at the end, median {np.median(po['val'][-1][g3, 1]):+.3f}; last-third P dwell > 0 in {int((late(po['b'])[g3] > 0).sum())} rows;"
        f" (N1): {int((late(pn['b'])[g3] > 0).sum())} rows, late unrecovered in G3 {int(unrec(pn)[g3].sum())}")

    # ---------------------------------------------------------------- (B4)
    say("\n== (B4) the paired difference in last-third punishing dwell, learned - no-learning (the quantity the WIN summarises) ==")
    for lab, m in (("G3", np.ones(len(nlb), bool)), ("G3+", nlb > 0)):
        d = lb[m] - nlb[m]; ph15._idx.clear(); dp, dl, dh = ph15.boot("DP", lb[m], nlb[m]); ph15._idx.clear(); gp, gl, gh = ph15.boot("DGM", lb[m], nlb[m])
        say(f"   {lab} (n {int(m.sum())}): mean difference {dp:+.3f} [{dl:+.3f}, {dh:+.3f}] (95 percent, paired bootstrap); difference of group medians {gp:+.3f} [{gl:+.3f}, {gh:+.3f}];"
            f" per-row differences quantiles {qs(d)}; rows below 0 {int((d < 0).sum())}, at 0 {int((d == 0).sum())}, above 0 {int((d > 0).sum())}")
    d3 = lb - a3b; ph15._idx.clear(); dp, dl, dh = ph15.boot("DP", lb, a3b)
    say(f"   beside: learned - H15 no-learning over G3: mean difference {dp:+.3f} [{dl:+.3f}, {dh:+.3f}]; rows below 0 {int((d3 < 0).sum())}, at 0 {int((d3 == 0).sum())}, above 0 {int((d3 > 0).sum())}")

    # ---------------------------------------------------------------- (B5) reference arithmetic
    say(f"\n== (B5) reference arithmetic (not a rule): how often each reading would PASS on a new draw of {len(G3)} G3 rows like the bench's ==")
    say(f"   {NOUT} outer draws of G3 rows with replacement (rows carry their learned, no-learning and H15 no-learning dwell together; generator seeded by the sequence"
        f" [bench bootstrap seed, 2]); each draw judged exactly as the reading would be (the registered 5000-resample percentile interval at 95 percent, ph15.boot; n >= 50; the tie rule; Wilson 95)")
    modes = [("present: readability on G3, WIN on G3+", "present"), ("readability and WIN on dwell > 0", ">0"), ("readability and WIN on dwell >= 1", "1"),
             ("readability and WIN on dwell >= 5", "5"), ("readability and WIN on dwell >= 10", "10"), ("H15 no-learning as the floor (present structure)", "H15 floor")]
    rng = np.random.default_rng([BENCH["boot"], 2]); cnt = {m: np.zeros(4, int) for _, m in modes}
    for j in range(NOUT):
        idx = rng.integers(0, len(G3), len(G3)); xl, xf, xa = lb[idx], nlb[idx], a3b[idx]
        jd = judge_draw(xl, xf, xa, [m for _, m in modes])
        for m, (rd_, rg_, wn_) in jd.items(): cnt[m] += np.array([rd_, rg_, wn_, rd_ and rg_ and wn_], int)
    ph15._idx.clear()
    for lab, m in modes:
        c = cnt[m]/NOUT
        say(f"   {lab:50s}: readability PASS {c[0]:.3f}; RGM part PASS {c[1]:.3f}; WIN part PASS (ties <= 0.20, lower >= 0.60) {c[2]:.3f}; all three {c[3]:.3f}")
    say("   (these are properties of the bench rows resampled; they are not pass probabilities for a new seed's world draw, which the bench rows only sample)")
    say("\n== end of diagnosis; H20 Stage C's verdict unchanged: stopped at the bench by the registered (hR) stop rule, no bar decision; nothing adopted; the owner decides ==")
    return True


if __name__ == "__main__":
    ok = main()
    import re
    pat = re.compile(r"(?<!\d)(" + "|".join(str(x) for x in ph30.seed_numbers()) + r")(?!\d)")      # ph30.seeds_unused's pattern
    leak = sorted(set(pat.findall("\n".join(_lines)) + pat.findall(open(__file__, encoding="utf-8").read())))
    if leak: print(f"A STAGE C SEED NUMBER IN THE OUTPUT OR THE SOURCE {leak}: the output is NOT written"); sys.exit(2)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh: fh.write("\n".join(_lines) + "\n")
    print(f"written {OUT} sha256 {sha(OUT)}")
    sys.exit(0 if ok else 1)
