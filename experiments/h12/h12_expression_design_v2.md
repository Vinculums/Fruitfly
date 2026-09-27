# H12 Package E design v2 FINAL: expression of a retained value under matched access

Date: 2026-09-27. Status: **FINAL, confirmed by the owner on 2026-09-27 before the first Package E calibration** ("확정하고 테스트 진행"). This is a new controlled behavioral question after the H12 Stage 2 bench stopped as UNREADABLE. It does not revise the registered Stage 1 PASS, the Stage 2 STOPPED result, or adoption. Source evidence: `notes/reviews/2026-09-27-review-and-plan.md`, `notes/reviews/2026-09-27-remote-diagnosis.md`, `experiments/h12/diagnosis/{summary.json,retention-inspection.json}`, and the original `experiments/h12/h12_design_v2.md`.

## 1. Question and scope

From identical extinguished A1 (parallel, no-decay) memory checkpoints, does decay of compartments 2 and 3 **during a silent retention interval only** change subsequent choice when both odours can be reached and the initial navigation state is matched? The primary comparison is paired decay-on minus decay-off at D=5000. This tests expression of retained value in a reset body. It does not test autonomous return of a continuously moving agent, a general identity between single-site and parallel modules, or recognition-based assignment of learning credit.

The Package D diagnosis motivates the separation. Its same-input A0/A1 maximum value gap was 0.203608; the old Stage 2's supplied ceiling had no V whiff in 335/400 P4 rows; and nine old-bench checkpoints had a negative acquisition component. None of these measurements is an exclusion rule or a result for the new cohort.

## 2. Frozen construction

Use the unchanged import chain and parameter values from `src/ph36b.py` (`Agent17`, `World7`, `ph11.MB`, `G_STAR`, presence prior 59, window 200, competitor N=+0.5). Do not edit `ph36b.py` or any adopted source. Keep a separate E harness with its own source hash and an exact source manifest.

For each assigned row, generate a new A1 memory under the old Stage 2's P1/P2 schedule, with **new seeds**: construct the World7/Agent17 pair and replace the learning module by `ph8.MB4(parallel=True,gated=True)` before the unchanged neutral-first `ph29.train`; P1 is steps 0–599 with V source reward; P2 is 600–2399 without external reward. At every step, the read-out precedes action and V source-contact code arrives after movement, exactly as `ph36b.run`. Save every row's V and N code, four compartment weights and both eligibility traces **after step 2399**. This is the fixed checkpoint boundary before step 2400. Keep all 400 rows, including memories without a positive extinction gap or with a reversed acquisition sign. Verify the generator against `ph36b.run('H11 full', ..., steps=2400)` on the same seed pair for all fields that original runner records; compare bitwise where the original field has full precision. The checkpoint generator must not use read-out results to choose rows.

Clone each checkpoint twice. In one clone, apply `MB5` tau `(None,None,5000,5000)` for D silent calls with **zero code and zero external reinforcement**; in the other, apply A1 with no decay. Eligibility traces evolve under the same zero input in both. D=5000 is primary, chosen from the original Stage 1; D=0 is a complete identity control; D=1200 is a descriptive bridge to the prior Stage 2. At D=0, all weights, traces, codes, values and compartment outputs must agree. Acquisition weights must remain invariant in both clones. Check the analytic zero-input value `acq_0 + par_0*(1-1/5000)^D` for the decay arm. Report the full signed distribution and all sign/rank crossings, including changes in the wrong direction. The old nine negative rows are historical evidence, **not the expected count on these new seeds**.

For each retention arm, build a fresh, unchanged Agent17 body at the same balanced World7 C0 start, using the assigned **read-out** world/agent seed pair. Transfer the memory codes to the corresponding V/N odour labels and the cloned module state to the new body. This is an explicit reset intervention; the body's earlier position, selector state and tracking history are not carried over. Body construction, source identity, cast sign and random streams must agree by row between paired arms at t=0. Write the retained V value and supplied N=+0.5 into the existing `known` pathway before each `act`. Both plumes remain available for all 600 read-out steps. **Call no module `step` during read-out**, including decay; supply no reinforcement. Record module-call count zero and immutable weights/traces/codes. Assert complete D=0 trajectory equality on every recorded field before judging any effect.

Controls use the same reset body and World7 draws: fixed V=+1.0, fixed V=+0.45 and equal V=N=+0.5. They do not learn or decay during read-out. The first two show whether this 600-step task can express a high versus low supplied value; the equal-value arm checks side balance. A0 and the originally continuous P trajectory are outside this primary design. They may only be added in a later, separately frozen descriptive protocol.

## 3. Outcomes and gates registered before any E run

The primary outcome is V dwell majority (`dwell_V > dwell_N`) over all 400 assigned rows in the 600-step read-out. N majority and ties (`dwell_V = dwell_N`) partition the same denominator. Report zero-contact ties separately from equal positive dwell. No filtering by extinction, signed recovery denominator, valence, V whiff, V-directed navigation, contact or value rank is allowed in a primary proportion. Report such attributes as mediators or diagnostics by row. Missing or invalid rows stop the run as an implementation error; they are never silently removed.

Pair every arm by the row's seed-derived identity. For each binary difference, compute the point estimate and a two-sided 95% **paired percentile bootstrap** interval from 5,000 row-resamples with replacement, using the registered bootstrap seed for that run and one shared resample index matrix for all contrasts. Use the same resample scheme for each arm's proportion and tie fraction. The endpoint is an empirical percentile, with no continuity or post-hoc correction. The checks below are an intersection of prespecified gates; no single passing endpoint overrides a failed gate. Calibration may reveal a task flaw but cannot lower a gate after seeing data.

| Check | Proposed acceptance | Consequence |
|---|---|---|
| Identity and implementation | D=0 paired trajectories equal on every recorded field; matching initial state and draws; zero module calls during read-out; no changed acquisition weights; analytic retention check | Any failure is an implementation error; repair and rerun only that stage before interpretation |
| Task readability | 95% lower bound of paired supplied high-minus-low V-majority contrast ≥ +0.30; supplied high V-majority lower bound ≥ 0.70; 95% upper bound of ties ≤ 0.20 in both primary and supplied control arms; equal-value V-majority intervals within [0.35,0.65] in each of the two valued-side strata | Otherwise UNREADABLE for this task; no H12 behavioral inference |
| Primary effect | Given a readable task, lower 95% bound for paired `P(V majority|decay on,D=5000) - P(V majority|decay off,D=5000)` ≥ +0.10 | Supports a practically meaningful effect **of this retention intervention on this read-out**. If the upper bound < +0.10, below bar; otherwise inconclusive |
| Mechanism record | Signed valence, acquisition and parallel contributions, value/rank crossing and sign-inverted rows, with all denominators | Descriptive; cannot be replaced by absolute-value SR alone |

The +0.10 minimum was proposed in the 2026-09-27 review **before** the Package D behavioral read-out and is retained here, not selected to fit its +0.0575 old-bench difference. The owner confirmed the proposed effect and supplied-readability bars on 2026-09-27 before Package E calibration. These bars do not revise the original H12 design or its stopped result. Development checks implementation and provenance without tuning thresholds. Evaluation is run once on its held-out pair, even if its answer is null or inconclusive. No extra sample is added after seeing evaluation.

## 4. Proposed seed manifest and separation

Each stage has independent checkpoint, read-out and bootstrap generators. Read-out world/agent seeds are the checkpoint pair plus 1,000,000. `World7` also derives a cell permutation at world+10,000; `cast_draw` derives its sign at agent+20,000. The complete registered numbers, including those offsets, are:

| Stage | Checkpoint world/agent | Read-out world/agent | Bootstrap | Derived world +10,000 (checkpoint/read-out) | Derived cast agent +20,000 (checkpoint/read-out) |
|---|---|---:|---:|---|---|
| Calibration | 20261281 / 20261282 | 21261281 / 21261282 | 20261283 | 20271281 / 21271281 | 20281282 / 21281282 |
| Development | 31011 / 31012 | 1031011 / 1031012 | 31013 | 41011 / 1041011 | 51012 / 1051012 |
| Evaluation | 71011 / 71012 | 1071011 / 1071012 | 71013 | 81011 / 1081011 | 91012 / 1091012 |

These are the **registered Package E seeds**. An exact digit-boundary scan found none of its 27 listed numbers in repository text before this design was written. On 2026-09-27, individual Vinc searches for all 27 numbers returned no keyword/FTS hits in the Fruit Fly space; semantic results were unrelated and are not evidence of a collision. The old H12 development/evaluation pairs remain reserved to its stopped design. Use the already spent `(5,6)` smoke pair only for code-path checks, labelled smoke and never as calibration. Verify the final source and design SHA-256 at execution, print all generators and record Python/NumPy/runner provenance. Persist raw row-level arrays and full stdout, not just a verdict.

## 5. Confirmed decision and execution order

The owner chose this **new controlled expression test** after Package D and fixed the gates in section 3, preserving the old Stage 2 stop. Freeze this v2 FINAL design, its SHA-256, the harness hash and seed manifest; smoke-check the frozen harness on the spent smoke pair; run remote calibration; stop or continue under the fixed readability and implementation rules; perform development checks; and run one evaluation only if the earlier gates hold. Record the result in Vinc and Git without rewriting earlier outputs. Keep the H10, H18, H17 queue until H12 is disposed separately.
