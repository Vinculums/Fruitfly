#!/usr/bin/env python3
"""H10 calibration: where the graded arm's wrong commitments sit on the evidence-trace margin q (measurement only).

Usage: python src/h10_margin_diag.py > experiments/h10/calibration/margin_diag.txt

Answers the registered open question (design 2.3, 10) on the calibration rows already recorded in
experiments/h10/calibration/trace.npz: on the five hard conditions, per tau_e, the q of e at the read for rows where the
ungated graded arm (arm 2) is correct vs wrong, how separable the two groups are by any threshold on q, e's leader on
them, and when the graded arm first commits. Reads the trace only: no simulation, no seed, no bar changed, nothing gated.
Encoding (src/h10.py): outputs are int8 identity 0..4, -1 abstain (run, ph7.committed); a read 'step k' is row k-1 of the
(T, rows) stream (at); q_at_reads is (tau 40/80/160, read cue_end 300 / final 600, rows), q = (1st - 2nd) / sum of e
(H10.gates); an H10 setting outputs the graded identity where q >= theta and sum(e) > 1e-6, else -1.
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(newline="\n")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import h10                                                      # noqa: E402  (unchanged; constants only)

CAL = HERE.parent / "experiments/h10/calibration"
QS = (0, 10, 25, 50, 75, 90, 100)
MAXW = 8                                                        # Wilson upper <= 0.04 of 400 <=> wrong <= 8
READS = ((1, 600, "final (step 600)"), (0, 300, "cue end (step 300)"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def cwa(o, t):
    return int((o == t).sum()), int(((o >= 0) & (o != t)).sum()), int((o == -1).sum())


def quant(v):
    return " ".join(f"{x:.5f}" for x in np.percentile(v, QS)) if len(v) else "(none)"


def auc(qw, qc):
    """P(q_wrong < q_correct), ties counted half."""
    if not len(qw) or not len(qc):
        return float("nan")
    s = np.sort(qc)
    right, left = np.searchsorted(s, qw, "right"), np.searchsorted(s, qw, "left")
    return float(((len(qc) - right) + 0.5 * (right - left)).sum() / (len(qw) * len(qc)))


def frontier(q, cor, wr):
    """exposed (correct, wrong) at every threshold q >= thr, thr over the distinct q of committed rows plus +inf."""
    thr = np.append(np.unique(q[cor | wr]), np.inf)
    c = np.array([(cor & (q >= t)).sum() for t in thr])
    w = np.array([(wr & (q >= t)).sum() for t in thr])
    return thr, c, w


def consistency(z, s):
    print("\n== 1. consistency with summary.json ==")
    ok = True
    ph = s["phase71_readings"]
    for x0 in h10.SCALES:
        key, x = h10.HARD_KEYS[x0], str(x0)
        t = z[f"{key}/targets"]
        grd = z[f"{key}/out/graded"].astype(int)
        g = cwa(grd[599], t)
        b = cwa(z[f"{key}/out/bistable"][599].astype(int), t)
        chk = [("graded wrong 600 vs phase71 d5", g[1], ph["graded"]["d5"][h10.SCALES.index(x0)]),
               ("bistable correct 600 vs criteria", b[0], s["criteria"][h10.sname(40, 0.004)]["hard"][x]["bistable_correct"])]
        if x0 == 1.0:
            chk.append(("graded c/w/a 600 vs phase71 d1", list(g), ph["graded"]["d1_cwa"]))
        for name, got, rec in chk:
            p = got == rec
            ok &= p
            print(f"  {key:9s} {name:33s} {got!s:16s} recorded {rec!s:16s} {'PASS' if p else 'FAIL'}")
        print(f"  {key:9s} graded c/w/a (no recorded field) 600 {g}  300 {cwa(grd[299], t)}")
        for k, tau in enumerate(h10.TAUS):
            for j, th in enumerate(h10.THETAS):
                n = h10.sname(tau, th)
                o = z[f"{key}/out/{n}"].astype(int)
                rec = s["criteria"][n]["hard"][x]
                got = [cwa(o[599], t), cwa(o[299], t)]
                want = [(rec["correct"], rec["wrong"], rec["abstain"]),
                        tuple(rec["cue_end_300"][f] for f in ("correct", "wrong", "abstain"))]
                gate = z[f"{key}/gate"][k, j]
                rebuilt = all(np.array_equal(o[r - 1], np.where(gate[r - 1], grd[r - 1], -1)) for r in (300, 600))
                qr = z[f"{key}/q_at_reads"][k]
                qgate = [int(((qr[i] >= th) != gate[r - 1]).sum()) for i, r in ((0, 300), (1, 600))]
                p = got == want and rebuilt
                ok &= p
                print(f"  {key:9s} {n:20s} 600 {got[0]!s:16s} 300 {got[1]!s:16s} gate*graded==out {rebuilt};"
                      f" rows where (q >= theta) != gate at 300/600: {qgate[0]}/{qgate[1]}  {'PASS' if p else 'FAIL'}")
    print(f"  consistency: {'PASS' if ok else 'FAIL'}")
    return ok


def groups(z, key, i, r, k):
    t = z[f"{key}/targets"].astype(int)
    grd = z[f"{key}/out/graded"]
    o = grd[r - 1].astype(int)
    anyc = grd >= 0
    return dict(t=t, o=o, q=z[f"{key}/q_at_reads"][k, i].astype(float), ld=z[f"{key}/lead"][k, r - 1].astype(int),
                first=np.where(anyc.any(0), anyc.argmax(0) + 1, -1),
                bc=int((z[f"{key}/out/bistable"][r - 1].astype(int) == t).sum()), cor=o == t, wr=(o >= 0) & (o != t))


def frac(a, n):
    return f"{a}/{n} ({a / max(n, 1):.3f})"


def block(label, g, per_condition):
    cor, wr, q = g["cor"], g["wr"], g["q"]
    print(f"  {label}: graded c/w/a {int(cor.sum())}/{int(wr.sum())}/{int((g['o'] == -1).sum())}")
    for nm, m in (("correct", cor), ("wrong", wr)):
        print(f"    2. q {nm:7s} quantiles {quant(q[m])}")
        print(f"       q {nm:7s} at/below theta  "
              + "  ".join(f"<= {th}: {frac(int((q[m] <= th).sum()), int(m.sum()))}" for th in h10.THETAS))
    print(f"    3. AUC P(q_wrong < q_correct), ties half: {auc(q[wr], q[cor]):.4f}")
    if per_condition:
        thr, c, w = frontier(q, cor, wr)
        ok = w <= MAXW
        bi = int(np.argmax(np.where(ok, c, -1)))
        bar = g["bc"] - 20
        at_bar = c >= bar
        print(f"       frontier over {len(thr)} thresholds: max correct with wrong <= {MAXW}: {c[bi]} (wrong {w[bi]})"
              f" at q >= {thr[bi]:.6f}")
        if at_bar.any():
            ai = int(np.nonzero(at_bar)[0].max())
            print(f"       anti-trivial point bar correct >= bistable {g['bc']} - 20 = {bar}: highest threshold"
                  f" q >= {thr[ai]:.6f} exposes correct {c[ai]}, wrong {w[ai]}")
        else:
            print(f"       anti-trivial point bar correct >= bistable {g['bc']} - 20 = {bar}: no threshold reaches it")
        both = ok & at_bar
        print(f"       any threshold with wrong <= {MAXW} and correct >= {bar} in these rows: "
              + (f"YES ({int(both.sum())} thresholds)" if both.any() else "NO"))
    for nm, m in (("correct", cor), ("wrong", wr)):
        n = int(m.sum())
        print(f"    4. {nm:7s} leader == graded identity {frac(int((g['ld'][m] == g['o'][m]).sum()), n)};"
              f"  leader == target {frac(int((g['ld'][m] == g['t'][m]).sum()), n)}")
    if per_condition:
        for nm, m in (("correct", cor), ("wrong", wr)):
            print(f"    5. first commit step, {nm:7s} quantiles {quant(g['first'][m])}")


def main():
    z = np.load(CAL / "trace.npz")
    s = json.loads((CAL / "summary.json").read_text(encoding="utf-8"))
    print("H10 post-calibration margin diagnosis (measurement only; calibration seeds already spent; no simulation)")
    print(f"script sha256 {sha(__file__)}")
    print(f"experiments/h10/calibration/trace.npz sha256 {sha(CAL / 'trace.npz')}")
    print(f"experiments/h10/calibration/summary.json sha256 {sha(CAL / 'summary.json')}")
    print(f"src/h10.py sha256 {sha(HERE / 'h10.py')}  numpy {np.__version__}")
    print("quantiles: min 10 25 50 75 90 max; q = e's margin at the read (float32 as saved); exposure = q >= threshold;"
          " 'first commit step' = first step with a graded output >= 0")
    if not consistency(z, s):
        print("STOP: recomputed counts differ from summary.json; nothing further is reported")
        return 1
    for i, r, rname in READS:
        for k, tau in enumerate(h10.TAUS):
            print(f"\n== read {rname}, tau_e {tau} ==")
            pool = []
            for x0 in h10.SCALES:
                g = groups(z, h10.HARD_KEYS[x0], i, r, k)
                pool.append(g)
                block(f"x0 {x0}", g, True)
            cat = {f: np.concatenate([g[f] for g in pool]) for f in ("t", "o", "q", "ld", "first", "cor", "wr")}
            cat["bc"] = sum(g["bc"] for g in pool)
            block("6. pooled over five x0, 2000 rows (per-condition bars not applied to the pool)", cat, False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
