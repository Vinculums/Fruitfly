# H12 Package E: controlled expression of retained value

Date: 2026-09-27. The owner confirmed [design v2 FINAL](h12_expression_design_v2.md) and its fixed gates before the first Package E calibration. The [manifest](h12_expression_manifest.json) fixes disjoint calibration, development and evaluation seeds, 400 rows per stage, 5,000 paired bootstrap resamples, and SHA-256 hashes for the design and harness. All simulation and bootstrap computations ran on GitHub-hosted Linux (Python 3.11.15, NumPy 2.4.6); the local machine only inspected downloaded outputs. The original H12 Stage 1 PASS and Stage 2 STOPPED/UNREADABLE records are unchanged.

## Result

The **held-out evaluation** met all registered task-readability checks and the primary effect bar. In the reset, matched-access, frozen-memory 600-step read-out, V dwell majority occurred in 69/400 rows without silent decay and 363/400 with 5,000 silent decay calls. The paired difference was **+0.7350**, with a two-sided 95% paired percentile bootstrap interval **[+0.6925, +0.7775]**. Its lower bound exceeds the prespecified +0.10 minimum. This supports an effect of the retention intervention on choice **in this controlled read-out**.

| Stage | V-majority off / on at D=5000 | Paired difference, 95% CI | Task readability | Remote run |
|---|---:|---:|---|---|
| Calibration | 69/400 / 353/400 | +0.7100 [0.6625, 0.7550] | Pass | [36283991401](https://github.com/Vinculums/Fruitfly/actions/runs/36283991401) |
| Development | 69/400 / 351/400 | +0.7050 [0.6575, 0.7500] | Pass | [36284289530](https://github.com/Vinculums/Fruitfly/actions/runs/36284289530) |
| Evaluation, once | 69/400 / 363/400 | +0.7350 [0.6925, 0.7775] | Pass | [36284507506](https://github.com/Vinculums/Fruitfly/actions/runs/36284507506) |

In evaluation, the supplied V=+1.0 versus V=+0.45 contrast was +0.8300 [0.7925, 0.8675], above its +0.30 lower-bound bar. The supplied-high V-majority lower bound was 0.9025, above 0.70. The largest tie upper bound across all registered arms was 0.0200, below 0.20. With equal supplied values, valued-side-stratified V-majority intervals were [0.4901, 0.6281] and [0.3698, 0.5078], both inside [0.35, 0.65]. The two clones agreed at D=0 on all 24 recorded read-out fields; the checkpoint construction agreed with the historical runner on 22 fields; acquisition weights stayed fixed during silence; no memory-module step occurred during choice. The earlier [frozen-v2 smoke result](expression_smoke/frozen_v2_run_36283936113/h12-expression-smoke/smoke.json) independently exercised these identities on spent seeds.

No rows were filtered. In calibration/development/evaluation respectively, negative acquisition components numbered 8/11/4 and rows whose V value **worsened** under decay numbered 7/8/4. In evaluation, 385 values improved, four worsened and eleven were unchanged; 356/400 crossed from below to above the fixed N=+0.5 competitor rank. These exceptions remain in all 400-row denominators and can be inspected by row.

## Raw evidence and provenance

Each stage has an unmodified [summary](expression_calibration/calibration/summary.json), [400-row record](expression_calibration/calibration/rows.json), [checkpoint archive](expression_calibration/calibration/checkpoint.npz), and [stdout](expression_calibration/calibration/stdout.log), with equivalent files under [development](expression_development/development/rows.json) and [evaluation](expression_evaluation/evaluation/rows.json). The full per-arm trajectory archives are in the local stage directories and in the downloadable GitHub Actions artifacts (90-day retention). They were omitted from Git because the nine trajectory archives total about 49 MB per stage. The row-level outputs, checkpoints, stdout, design, source and seed manifest are committed. Evaluation source SHA-256: `8469de8001791a32904c8aed81d107574ceebaff2b7248b0614a9271818b4c04`; design SHA-256: `db1132b28a461ffb351b2902b821e6ae7bc535bacc67d7911c7ff9733495621b`. Both match the manifest and all three stage summaries.

## Interpretation boundary

The test deliberately transfers an A1 memory into a fresh Agent17/World7 body, presents both odours from a balanced start, supplies the retained V value through the existing `known` pathway, and freezes memory while the body chooses. It isolates whether the retained value **can be expressed as a choice** when access is matched. It does **not** show that the continuously moving Stage 2 agent rediscovers V after spending P3 at N, that the effect survives ongoing learning during choice, or that the parallel module should be adopted. The prior Stage 2 result remains stopped. Package E is **SHOWN within its tested conditions**; H12 closure and adoption remain separate product decisions. A further continuous-world test would require a new question and registration rather than treating this controlled result as a repair of Stage 2.
