#!/usr/bin/env python3
"""H20 Run 2 diagnosis (measurement only; owner's request 2026-09-23). ph18.py, design v1 and the
Run 2 verdict are untouched. ph18.run is called unchanged on the EVALUATION seeds, so every trajectory
is the one behind ph18_eval.txt (checked: V/N/tie of both arms equal the table). Adds only a log of the
two release flags per step. Names no cause: it decomposes the dwell-majority measure.

(1) paired flips, bias vs pathway-off, same rows (majority class and first hold)
(2) dwell steps at each source split by what was held on that step (valued / neutral / nothing)
(3) N rows of the dwell measure by hold history; releases per row by kind (timeout / evidence / direct)
(4) conversion of a valued first hold into a valued majority, split by whether pathway-off also held it first
"""
import hashlib
import numpy as np
import ph18
from ph16 import Agent4, World7, diagnostics
from ph9 import HIT_R

MADE = []
class Agent4L(Agent4):
    def __init__(self, *a, **k):
        super().__init__(*a, **k); self.T, self.E = [], []; MADE.append(self)
    def act(self, w, whiffs, wind_on):
        r = super().act(w, whiffs, wind_on); self.T.append(self.due_timeout.copy()); self.E.append(self.due_evidence.copy()); return r
class World7L(World7):
    def __init__(self, *a, **k): super().__init__(*a, **k); MADE.append(self)
ph18.Agent4, ph18.World7 = Agent4L, World7L

def sha(): return hashlib.sha256(open(__file__, "rb").read()).hexdigest()

def load(arm):
    MADE.clear(); o = ph18.run(arm, ph18.SEEDS["eval"]); w, a = MADE
    o["src"] = w.src; o["T"] = np.array(a.T); o["E"] = np.array(a.E)
    at = np.linalg.norm(o["POS"][:, :, None, :] - w.src[None], axis=3) < HIT_R          # steps x rows x 2
    assert np.array_equal(at.sum(0), o["dwell"]), "dwell recomputed from positions differs"
    o["AT"] = at; o["cls"] = np.select(list(ph18.majority(o)), [0, 1, 2]); o["d"] = diagnostics(o)
    return o

def releases(o):
    H = o["H"]; prev = np.vstack([np.full((1, H.shape[1]), -1, np.int8), H[:-1]]); committed = prev >= 0
    ended = committed & (H != prev)
    t = (o["T"] & committed); e = (o["E"] & ~o["T"] & committed); direct = ended & ~o["T"] & ~o["E"]
    return t.sum(0), e.sum(0), direct.sum(0), ended.sum(0)

def split(o, rows):
    good = o["good"]; n = len(good); r = np.arange(n); out = {}
    for name, k in (("valued", good), ("neutral", 1 - good)):
        at = o["AT"][:, r, k][:, rows]; H = o["H"][:, rows]; g, nn = good[rows], (1 - good)[rows]
        out[name] = tuple(int((at & (H == x[None, :])).sum()) for x in (g, nn)) + (int((at & (H < 0)).sum()),)
    return out

def hist(o, rows):
    d = o["d"]; ev, en, fv, fn = (d[k][rows] for k in ("ever_v", "ever_n", "fh_v", "fh_n"))
    return dict(none=int((~ev & ~en).sum()), neutral_only=int((en & ~ev).sum()), valued_only=int((ev & ~en).sum()),
                valued_then_neutral=int((ev & en & fv).sum()), neutral_then_valued=int((ev & en & fn).sum()))

def main():
    print(f"== H20 Run 2 diagnosis (measurement only). this file sha256 {sha()}; ph18.py sha256 {ph18.sha()}; design {ph18.DESIGN};"
          f" evaluation seeds {ph18.SEEDS['eval']}; {ph18.R} rows x {ph18.T} steps; arms bias (G 2) and pathway-off (G 0) re-run unchanged ==")
    B, P = load("bias"), load("pathway-off"); R = ph18.R; rows = np.arange(R)
    cnt = lambda o: tuple(int((o["cls"] == c).sum()) for c in range(3))
    assert cnt(B) == (214, 180, 6) and cnt(P) == (203, 190, 7), f"eval table not reproduced: {cnt(B)} {cnt(P)}"
    print(f"   identity: bias V/N/tie {cnt(B)} and pathway-off {cnt(P)} equal ph18_eval.txt; dwell recomputed from positions equals the run's dwell")
    L = ("V", "N", "tie")
    print("\n(1) paired majority class, same rows: rows = bias, cols = pathway-off")
    for i in range(3): print(f"   bias {L[i]:3s}: " + "  ".join(f"pathway-off {L[j]} {int(((B['cls'] == i) & (P['cls'] == j)).sum()):3d}" for j in range(3)))
    nv = int(((B["cls"] == 0) & (P["cls"] != 0)).sum()); vn = int(((B["cls"] != 0) & (P["cls"] == 0)).sum())
    print(f"   rows the gain moved INTO V {nv}, OUT of V {vn}, net {nv - vn}; unchanged class {int((B['cls'] == P['cls']).sum())}/{R}")
    FH = lambda o: np.where(o["d"]["fh_v"], 0, np.where(o["d"]["fh_n"], 1, 2)); fb, fp = FH(B), FH(P); F = ("valued", "neutral", "none")
    print("   paired first hold: rows = bias, cols = pathway-off")
    for i in range(3): print(f"   bias {F[i]:7s}: " + "  ".join(f"pathway-off {F[j]} {int(((fb == i) & (fp == j)).sum()):3d}" for j in range(3)))
    print(f"   first-hold step, paired: bias earlier in {int((B['d']['ft'] < P['d']['ft']).sum())} rows, same step {int((B['d']['ft'] == P['d']['ft']).sum())}, later {int((B['d']['ft'] > P['d']['ft']).sum())}")
    print("\n(2) dwell steps (within 3.0) at each source, summed over rows, split by the odour held on that step: valued-held / neutral-held / nothing-held")
    for name, o in (("bias", B), ("pathway-off", P)):
        for grp, sel in (("all rows", rows), ("V rows", rows[o["cls"] == 0]), ("N rows", rows[o["cls"] == 1])):
            s = split(o, sel); tot = {k: sum(v) for k, v in s.items()}
            print(f"   {name:12s} {grp:9s} n {len(sel):3d}: at valued {s['valued']} (total {tot['valued']}) | at neutral {s['neutral']} (total {tot['neutral']})")
        gap = (o["H"] < 0).mean(0)
        print(f"   {name:12s} steps with nothing held, fraction per row: mean {gap.mean():.3f}; V rows {gap[o['cls'] == 0].mean():.3f}; N rows {gap[o['cls'] == 1].mean():.3f}")
    print("\n(3) hold history of the rows of each majority class; releases per row by kind (a timeout or evidence release counted only while something was held)")
    for name, o in (("bias", B), ("pathway-off", P)):
        t, e, d, ended = releases(o)
        for grp, sel in (("V rows", rows[o["cls"] == 0]), ("N rows", rows[o["cls"] == 1]), ("tie", rows[o["cls"] == 2])):
            h = hist(o, sel)
            print(f"   {name:12s} {grp:6s} n {len(sel):3d}: hold history {h}; releases per row: timeout {t[sel].mean():.2f} evidence {e[sel].mean():.2f}"
                  f" direct switch {d[sel].mean():.2f}; holds ended {ended[sel].mean():.2f}")
        print(f"   {name:12s} totals: timeout {int(t.sum())} evidence {int(e.sum())} direct {int(d.sum())}; rows with any release {int(((t + e + d) > 0).sum())}/{R}")
    print("\n(4) conversion of a valued first hold into a valued majority (dwell measure), same rows in both arms")
    bv, pv = B["d"]["fh_v"], P["d"]["fh_v"]; V_B, V_P = B["cls"] == 0, P["cls"] == 0
    for label, m in (("bias: first hold valued, pathway-off ALSO first held valued", bv & pv), ("bias: first hold valued, pathway-off did NOT (gain-induced)", bv & ~pv),
                     ("bias: first hold neutral", B["d"]["fh_n"])):
        print(f"   {label}: n {int(m.sum())}; P(V) in bias {int((V_B & m).sum())}/{int(m.sum())} = {V_B[m].mean():.3f}; P(V) in pathway-off on the same rows {V_P[m].mean():.3f}")
    m = pv & ~bv; print(f"   pathway-off first held valued but bias did not: n {int(m.sum())}")
    m = pv; print(f"   pathway-off: first hold valued: n {int(m.sum())}; P(V) in pathway-off {V_P[m].mean():.3f}; in bias on the same rows {V_B[m].mean():.3f} (bias first hold valued there {int((bv & m).sum())})")
    late = rows[bv & pv]; print(f"   rows both arms first held valued: bias first-hold step median {np.median(B['d']['ft'][late]):.0f}, pathway-off {np.median(P['d']['ft'][late]):.0f}")

if __name__ == "__main__" and "--part2" not in __import__("sys").argv: main()


def endings(o, name):
    """(5) every hold ending: the release flag on that step, the held unit's state s the step before, what is held next and when"""
    H, T, E, S, good = o["H"], o["T"], o["E"], o["S"], o["good"]; n = H.shape[1]; rows = np.arange(n)
    prev = np.vstack([np.full((1, n), -1, np.int8), H[:-1]]); committed = prev >= 0; ended = committed & (H != prev)
    s_prev = np.vstack([np.zeros((1, n)), S[:-1][np.arange(len(S) - 1)[:, None], rows[None, :], np.maximum(prev[:-1], 0)]])
    fired = committed & (T | E)
    for label, m in (("resets fired while held, hold SURVIVED", fired & ~ended), ("hold ENDED", ended)):
        k = int(m.sum()); kinds = {"timeout": int((m & T & ~E).sum()), "evidence": int((m & E & ~T).sum()), "both": int((m & T & E).sum()), "neither": int((m & ~T & ~E).sum())}
        sp = s_prev[m]; print(f"   {name:12s} {label}: {k} (row, step); flag {kinds}; held unit's s the step before: median {np.median(sp) if k else float('nan'):.2f},"
              f" share >= 4.5 {(sp >= 4.5).mean() if k else float('nan'):.2f}, share < 2.0 {(sp < 2.0).mean() if k else float('nan'):.2f}")
    was = np.where(ended, prev, -1); by_val = {"valued hold ended": ended & (prev == good[None, :]), "neutral hold ended": ended & (prev == (1 - good)[None, :])}
    for label, m in by_val.items():
        ts, rs = np.nonzero(m); nxt, wait = [], []
        for t, r in zip(ts, rs):
            later = H[t:, r]; j = np.nonzero(later >= 0)[0]
            nxt.append(-1 if len(j) == 0 else later[j[0]]); wait.append(-1 if len(j) == 0 else j[0])
        nxt, wait = np.array(nxt), np.array(wait); same = (nxt == was[ts, rs]); other = (nxt >= 0) & ~same
        print(f"   {name:12s} {label}: {len(ts)}; next hold: same odour {int(same.sum())}, other odour {int(other.sum())}, none {int((nxt < 0).sum())};"
              f" steps to the next hold: median {np.median(wait[wait >= 0]) if (wait >= 0).any() else float('nan'):.0f}; at the ending step the agent had reached the valued source"
              f" in {int((o['first'][rs, good[rs]] >= 0) & (o['first'][rs, good[rs]] <= ts)).sum() if False else int(((o['first'][rs, good[rs]] >= 0) & (o['first'][rs, good[rs]] <= ts)).sum())} and the neutral in"
              f" {int(((o['first'][rs, 1 - good[rs]] >= 0) & (o['first'][rs, 1 - good[rs]] <= ts)).sum())}")
    held_v = H == good[None, :]; held_n = H == (1 - good)[None, :]
    sv = S[np.arange(len(S))[:, None], rows[None, :], good[None, :]]; sn = S[np.arange(len(S))[:, None], rows[None, :], (1 - good)[None, :]]
    print(f"   {name:12s} held unit's s over held steps: valued hold median {np.median(sv[held_v]):.2f} (share >= 4.5 {(sv[held_v] >= 4.5).mean():.2f});"
          f" neutral hold median {np.median(sn[held_n]):.2f} (share >= 4.5 {(sn[held_n] >= 4.5).mean():.2f}); held steps valued {int(held_v.sum())} neutral {int(held_n.sum())}")


def main2():
    B, P = load("bias"), load("pathway-off")
    print("\n(5) hold endings and surviving resets (a reset is the one-step drive 10 into the circuit's pool; RESET_AFTER 40 steps of silence on the held odour, MARGIN 0.2)")
    for name, o in (("bias", B), ("pathway-off", P)): endings(o, name)
    print("\n   bias N rows that held the valued odour first and the neutral odour later (77 in section 3): the valued hold's ending")
    o = B; d = o["d"]; good = o["good"]; rows = np.arange(len(good)); m = (o["cls"] == 1) & d["ever_v"] & d["ever_n"] & d["fh_v"]
    H = o["H"]; prev = np.vstack([np.full((1, len(good)), -1, np.int8), H[:-1]]); ended_v = (prev == good[None, :]) & (H != prev)
    t_end = np.where(ended_v.any(0), ended_v.argmax(0), -1)[m]; r = rows[m]
    reached_v = (o["first"][r, good[r]] >= 0) & (o["first"][r, good[r]] <= t_end); reached_n = (o["first"][r, 1 - good[r]] >= 0) & (o["first"][r, 1 - good[r]] <= t_end)
    kind = np.where(o["T"][t_end, r], "timeout", np.where(o["E"][t_end, r], "evidence", "neither"))
    print(f"   n {int(m.sum())}; first valued hold ends at step median {np.median(t_end):.0f}; flag at that step: " + ", ".join(f"{k} {int((kind == k).sum())}" for k in ("timeout", "evidence", "neither"))
          + f"; by then the valued source had been reached in {int(reached_v.sum())} rows, the neutral in {int(reached_n.sum())}, neither in {int((~reached_v & ~reached_n).sum())}")
    dv = np.linalg.norm(o["POS"][t_end, r] - o["src"][r, good[r]], axis=1); dn = np.linalg.norm(o["POS"][t_end, r] - o["src"][r, 1 - good[r]], axis=1)
    print(f"   distance at that step: to the valued source median {np.median(dv):.1f}, to the neutral median {np.median(dn):.1f}; nearer the neutral in {int((dn < dv).sum())} rows")
    wv = o["W"][:, r, good[r]]; wn = o["W"][:, r, 1 - good[r]]; before = np.arange(len(H))[:, None] < t_end[None, :]
    print(f"   whiffs before that step, per row: valued plume mean {(wv & before).sum(0).mean():.1f}, neutral plume mean {(wn & before).sum(0).mean():.1f};"
          f" after it: valued {(wv & ~before).sum(0).mean():.1f}, neutral {(wn & ~before).sum(0).mean():.1f}")


if __name__ == "__main__" and "--part2" in __import__("sys").argv: main2()
