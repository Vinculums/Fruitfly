#!/usr/bin/env python3
"""H10 design check: arithmetic behind design v2's changes to the v1 DRAFT. The H10 candidate is not run.

Usage: python src/h10_design_check.py > experiments/h10/h10_design_check.txt

Nothing here uses a registered seed or runs the H10 gate or any arm on a noise stream. It prints:
  (1) Wilson 95% bounds at n = 400 for the proposed all-row bars: the largest wrong count whose upper bound is <= 0.025,
      the smallest correct count whose lower bound reaches 0.90 / 0.85 / 0.98, and the historical bistable hard-cue
      counts (experiments/h09/ph7_h9.txt: 121/4/75 of 200) doubled to n = 400;
  (2) the noise-free steady state of the adopted upstream stage (ph2.Upstream with ph7.UP, unchanged) for every v1 input,
      and v1's confidence ratio q = (largest - second) / sum on it. For a constant input the evidence trace e converges to
      this y, so this is the scale q takes once the trace has settled. It is an approximation: noise enters y
      nonlinearly;
  (3) an ideal observer that sums the raw hard-cue input over all 300 cue steps (no upstream stage, no clipping), with
      output gated on its own top-minus-second margin. Any mechanism reading the same input can do no better. This gives
      the best reachable coverage at a given all-row wrong rate. It is a Monte Carlo estimate on a generator used only
      here (DESIGN_ONLY_SEED), which is not a task seed and is listed in the design's seed scan;
  (4) the H9 graded circuit (ph7.ChanDiv, J 1.2, c 0.5, tau 10) with its internal noise set to 0, driven by the noise-free
      hard-cue and easy-cue upstream outputs of (2): its state and the same ratio q on the state, i.e. what v1's simple
      graded-state mask would read once the circuit has committed;
  (5) the effective sample size of the evidence trace e over the 300-step hard cue for each v1 tau_e,
      (sum w)^2 / sum w^2 with w_t = (1/tau_e)(1 - 1/tau_e)^(300 - t);
  (6) for candidate all-row wrong bars (Wilson upper bound <= U at n = 400) the largest passing count and the probability
      that a mechanism with a given true wrong rate passes at all five input scales (independent rows).
"""
import hashlib
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ph2 import Upstream                                        # noqa: E402  (adopted stage, unchanged)
import ph7                                                      # noqa: E402

sys.stdout.reconfigure(newline="\n")  # LF output, so the recorded sha256 equals the committed blob
N, Z = 5, 1.959964
DESIGN_ONLY_SEED = 91919
IDEAL_ROWS = 400_000


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def wilson(k, n):
    p = k / n
    centre = (p + Z * Z / (2 * n)) / (1 + Z * Z / n)
    half = Z * np.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / (1 + Z * Z / n)
    return centre - half, centre + half


def binom_cdf(k, n, p):
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k + 1))


def steady_y(x, steps=400):
    up = Upstream(runs=1, chans=N, **ph7.UP)
    for _ in range(steps):
        y = up.step(np.asarray(x, float)[None, :])
    return y[0]


def q_ratio(v):
    s = np.sort(v)[::-1]
    return (s[0] - s[1]) / (v.sum() + 1e-12), (s[0] - s[1]) / (s[0] + 1e-12)


def main():
    print("H10 design check (arithmetic only; no candidate circuit run; no registered seed used)")
    print(f"script sha256 {sha(__file__)}")
    print(f"ph2.py sha256 {sha(Path(__file__).parent / 'ph2.py')}  ph7.py sha256 {sha(Path(__file__).parent / 'ph7.py')}")
    print(f"numpy {np.__version__}")

    print("\n(1) Wilson 95% bounds at n = 400")
    n = 400
    k_max = max(k for k in range(n + 1) if wilson(k, n)[1] <= 0.025)
    print(f"  largest wrong count with upper bound <= 0.025: {k_max} (upper {wilson(k_max, n)[1]:.4f});"
          f" {k_max + 1} gives {wilson(k_max + 1, n)[1]:.4f}")
    for bar in (0.90, 0.85, 0.98):
        k = min(k for k in range(n + 1) if wilson(k, n)[0] >= bar)
        print(f"  smallest correct count with lower bound >= {bar:.2f}: {k} of 400 ({k / n:.4f})")
    c, w, a = 121, 4, 75
    print(f"  historical bistable hard cue (ph7_h9.txt) c/w/a {c}/{w}/{a} of 200 -> at 400 rows expected"
          f" {2 * c}/{2 * w}/{2 * a}; wrong {2 * w}/400 upper bound {wilson(2 * w, n)[1]:.4f}")
    lam = 2 * w
    p_pass = sum(math.exp(-lam) * lam ** k / math.factorial(k) for k in range(k_max + 1))
    print(f"  Poisson probability that a mechanism with the bistable's wrong rate shows <= {k_max} wrong of 400: {p_pass:.4f}")

    print("\n(2) noise-free steady state of the adopted upstream stage and v1's q")
    print("  input                                   y (target first, then the other four)          q=(1st-2nd)/sum  (1st-2nd)/1st")
    cases = []
    for x0 in (0.25, 0.5, 1.0, 2.0, 4.0):
        cases.append((f"hard cue x0 {x0}", [x0 * (1 + 0.05)] + [x0] * 4))
    cases += [("easy cue x0 1 (d 0.4)", [1.4, 1, 1, 1, 1]),
              ("B alone, amplitude 2 (revision/distractor)", [2, 0, 0, 0, 0]),
              ("ambiguous d 0, x0 1", [1, 1, 1, 1, 1])]
    for name, x in cases:
        y = steady_y(x)
        q, rel = q_ratio(y)
        print(f"  {name:40s} {np.array2string(y, precision=4, floatmode='fixed'):48s} {q:.5f}          {rel:.5f}")
    print("  v1 theta grid: 0.02, 0.05, 0.10")

    print("\n(3) ideal observer on the raw hard cue (x0 1, d 0.05, noise_sd 0.3, 300 steps, 5 channels)")
    rng = np.random.default_rng(DESIGN_ONLY_SEED)
    steps, d, sd = 300, 0.05, 0.3
    # The sum of 300 iid N(mu, sd) samples is N(300 mu, sd sqrt(300)); drawing the sums directly is exact.
    sums = rng.normal(steps * 1.0, sd * np.sqrt(steps), size=(IDEAL_ROWS, N))
    sums[:, 0] += steps * d
    order = np.sort(sums, axis=1)
    margin = order[:, -1] - order[:, -2]
    correct = sums.argmax(1) == 0
    print(f"  rows {IDEAL_ROWS}; ungated accuracy {correct.mean():.4f}")
    idx = np.argsort(-margin)
    cum_wrong = np.cumsum(~correct[idx]) / IDEAL_ROWS
    cum_cover = np.arange(1, IDEAL_ROWS + 1) / IDEAL_ROWS
    for w_rate in (0.0075, 0.004, 0.002):
        ok = np.flatnonzero(cum_wrong <= w_rate)
        top = ok[-1] if len(ok) else -1
        cover = cum_cover[top] if top >= 0 else 0.0
        corr = cover - cum_wrong[top] if top >= 0 else 0.0
        print(f"  all-row wrong rate <= {w_rate:.4f}: best coverage {cover:.4f}, all-row correct {corr:.4f}")
    for cover in (0.50, 0.60, 0.65, 0.70):
        top = int(cover * IDEAL_ROWS) - 1
        print(f"  coverage {cover:.2f}: all-row wrong {cum_wrong[top]:.4f}, all-row correct {cover - cum_wrong[top]:.4f}")

    print("\n(4) H9 graded circuit, internal noise 0, driven by the noise-free upstream output of (2)")
    for name, x in (("hard cue x0 1", [1.05, 1, 1, 1, 1]), ("easy cue x0 1", [1.4, 1, 1, 1, 1])):
        y = steady_y(x)
        net = ph7.ChanDiv(1, n=N, J=1.2, c=0.5, tau=10.0, noise=0.0)
        for step in range(1, 301):
            net.step(y[None, :])
            if step in (50, 100, 300):
                s = net.s[0]
                print(f"  {name}, after {step:3d} steps: s {np.array2string(s, precision=4, floatmode='fixed')}"
                      f"  committed {int(ph7.committed(net)[0])}  q on state {q_ratio(s)[0]:.4f}")

    print("\n(5) effective sample size of the evidence trace over the 300-step hard cue")
    t = np.arange(1, 301)
    for tau_e in (40, 80, 160):
        w = (1 / tau_e) * (1 - 1 / tau_e) ** (300 - t)
        print(f"  tau_e {tau_e:3d}: weight on the cue {w.sum():.3f}, effective steps {w.sum() ** 2 / (w ** 2).sum():.1f} of 300")

    print("\n(6) all-row wrong bars at n = 400: largest passing count, and pass probability at all five scales")
    rates = (0.0025, 0.005, 0.01, 0.02)
    print("  bar U    k_max   " + "   ".join(f"true {r:.4f}" for r in rates))
    for u in (0.025, 0.04, 0.05):
        k_max = max(k for k in range(n + 1) if wilson(k, n)[1] <= u)
        cells = [f"{binom_cdf(k_max, n, r) ** 5:11.4f}" for r in rates]
        print(f"  {u:.3f}   {k_max:5d}   " + "   ".join(cells))


if __name__ == "__main__":
    main()
