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

## Interpretation note (added 2026-09-27 after the owner's review; the verdict is unchanged)

The owner reviewed this result and asked for this note (decision:h12-closed). It adds a reading, not a new test: [`src/h12_expression_interpret.py`](../../src/h12_expression_interpret.py) runs no simulation and only reads the three preserved `rows.json` files; its full output is [`h12_expression_interpret.txt`](h12_expression_interpret.txt).

**The body does not read the transplanted memory.** Before every read-out step the harness writes the retained V value into `a.known` ([`src/h12_expression.py:164`](../../src/h12_expression.py)). When `known` is set, the agent takes its valence from `known` alone (`ph14.py:52-53`, `ph11.py:183-184`, `ph16.py:88`), so the transplanted module (`h12_expression.py:146`) and its codes are never read by the body. With memory frozen, the V valence the module itself would give the body is that same constant. The only route by which the module could change behaviour, learning during choice, was excluded by design. The data agree: the three no-decay arms have different eligibility traces after 0, 1,200 and 5,000 silent steps but the same V value, and they give the same dwell in all 400 rows of every stage. Each retention arm is therefore equivalent to a supplied-value arm whose per-row V is the retained value. The recorded "zero module calls during read-out" is a constant of the loop (no counter is incremented), not a measurement. The weight, trace and code immutability checks were actually performed.

**Choice follows the rank of V against N = +0.5, not its size.** Pooled over the D0_off, D1200_on and D5000_on arms of the three stages (3,600 rows), V dwell majority is 0.077 when V ≤ +0.5 (n 1,701) and 0.920 when V > +0.5 (n 1,899). Within each side it is flat: 0.064–0.083 in every bin below +0.5 and 0.903–0.929 in every bin above. These two levels match the supplied controls (V +0.45: 0.05–0.10; V +1.0: 0.92–0.93).

**The primary effect is predicted by two quantities that need no behavioural run.** The first is the fraction of rows whose value crosses +0.5 at D = 5,000. It follows from the checkpoint weights through `acq + par·(1 − 1/5000)^D`. The second is the supplied high-minus-low contrast.

| Stage | Rank crossing | × supplied high − low | Predicted | Observed |
|---|---:|---:|---:|---:|
| Calibration | 0.8375 | 0.8450 | 0.7077 | 0.7100 |
| Development | 0.8175 | 0.8700 | 0.7112 | 0.7050 |
| Evaluation | 0.8900 | 0.8300 | 0.7387 | 0.7350 |

**What Package E adds.** The new, measured fact is at the value level. Among A1 memories formed by behaving agents under the old P1/P2 schedule, 82–89% carry an extinction component in the parallel pair large enough that 5,000 silent decay steps lift V from below to above the +0.5 competitor. The behavioural read-out adds that the adopted agent converts that rank into choice when access is matched, which the readability controls already establish. Package E does **not** show that a memory drives behaviour from inside the agent. It also does not show recovery in a continuously moving, learning agent, and it gives no ground for adopting the parallel module.

**Smaller points.** Zero-contact ties, which design section 3 asks to report apart from equal positive dwell, are 0 in every arm of every stage. The no-decay V-majority is 69/400 in all three stages by coincidence: the rows differ, with 9–14 in common between stages against a chance expectation of 11.9, and the value distributions differ. The evaluation's equal-value strata (0.56 and 0.44) sit inside the gate and are not seen in calibration or development. Design section 2 names World7 for checkpoint generation; the harness uses the historical runner's `ph23.Lost` with the mask off before step 2,400, which the 22-field identity against `ph36b.run` covers.

## Erratum (2026-09-27; the verdict and the owner's closure are unchanged)

A review of the interpretation note (Codex handoff `notes/handoffs/2026-09-27-fable-h10.md`) found one registration mismatch and four wording faults. Everything above is kept as written; this section corrects it.

**1. Equal-value strata were computed by odour identity, not by side.** Design section 3 asks for the equal-value V-majority interval "in each of the two valued-side strata". The harness stratified on `baseline["good"]` (`src/h12_expression.py:333`). In World7 that field is the valued odour's identity (`good = cell // 2`); the physical side is `cell % 2` (`src/ph16.py:51`). The intervals recorded in every `summary.json`, and quoted in the Result section above, are therefore identity strata. [`src/h12_expression_erratum.py`](../../src/h12_expression_erratum.py) recomputes the clause on the physical side from the preserved rows only (no simulation). It rebuilds each stage's registered bootstrap draws and uses the harness's `side_interval` unchanged. It first reproduces the recorded identity-strata intervals and the primary interval exactly. Output: [`erratum/stdout.log`](erratum/stdout.log), [`erratum/result.json`](erratum/result.json). It was run in the local session with NumPy 2.4.6. An earlier identical submission to GitHub Actions (run 36302405993) was withdrawn on the owner's instruction, and its artifact is not used.

| Stage | Identity strata (as recorded) | Physical side: valued source at +y | Physical side: valued source at −y |
|---|---|---|---|
| Calibration | 101/200 [0.4368, 0.5742]; 96/200 [0.4100, 0.5502] | 101/200 [0.4337, 0.5729] | 96/200 [0.4099, 0.5490] |
| Development | 104/200 [0.4500, 0.5902]; 105/200 [0.4545, 0.5951] | 104/200 [0.4508, 0.5899] | 105/200 [0.4558, 0.5959] |
| Evaluation | 112/200 [0.4901, 0.6281]; 88/200 [0.3698, 0.5078] | 102/200 [0.4404, 0.5777] | 98/200 [0.4171, 0.5588] |

Every physical-side interval lies inside [0.35, 0.65]. With the other readability clauses as recorded, each stage stays readable under the registered side wording. The primary effect and every other number are unchanged. The evaluation's 0.56/0.44 split, which the interpretation note called a side bias, is an identity split. By physical side the split is 0.51/0.49.

**2. The supplied contrast is behaviour.** The note said the primary effect "is predicted by two quantities that need no behavioural run". That is wrong: the supplied high-minus-low contrast is itself measured behaviour from the same run. The product of rank crossing and supplied contrast is a post-hoc approximation that happens to lie within 0.007 of the observed effect. It is not an independent prediction registered in advance, and it is not an identity.

**3. The pooled rows are not 3,600 specimens.** The pooled table covers 1,200 memories (400 per stage), each observed under three retention conditions (D0_off, D1200_on, D5000_on). The three observations of one memory are not independent.

**4. Learning during choice is not the only conceivable route from the module to choice.** The note said learning during choice is "the only route by which the module could change behaviour". The specific, verified claim is narrower: in this harness `known` is set, so the body never reads the transplanted module. A frozen module could in principle be read directly with `known` absent; that would also change where N's value comes from, so it would be a different task. The overclaim also appears in the closure wording on record and in the master plan; both now point here.

**5. The module-call counter.** `readout_module_calls = 0` is a constant of the read-out loop, not instrumentation. The weight, trace and code immutability checks were actually executed. This restates the note's point, which stands.
