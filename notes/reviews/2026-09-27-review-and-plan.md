# Fruitfly evidence review and next-work plan

Date: 2026-09-27 (Asia/Seoul). Reviewed baseline: `6870b4d7e50629b5362ab40454251ef94183bd83`.
Status: completed review; proposed follow-up plan, not a new hypothesis registration, closure, adoption or queue decision.
Request: review possible errors in the analysis and choice of work, then prepare the next work plan.
Scope: a focused audit of H12, the learning-input contract and the headline interpretations of H20/H21/H28/H29, using local source, recorded outputs and designs, plus current Vinc decisions and records in the Fruit Fly space. This is not an exhaustive re-audit or rerun of every earlier hypothesis.

The original scripts, designs, raw outputs and verdicts are preserved. This document is an additive correction to interpretations. It distinguishes code observations, existing measurements, a small new instrument check, and proposals. No new behavioural evaluation was run. Literature claims were not independently reviewed here; none of the conclusions below establishes that a fly implements this mechanism.

## 1. Main assessment

The project has evidence for supplied/learned values affecting behaviour within its registered worlds. It does not yet demonstrate a portable recognition-to-credit-assignment core. The H12 module result stands, and stopping Stage 2 was appropriate. The next action should be a bounded diagnosis followed by a controlled memory-to-behaviour test, rather than immediately moving the animal nearer the valued source and repeating Stage 2.

Three distinct questions have been mixed in the proposed continuation:

1. Does decay at the parallel site recover a value, with the same prior input history?
2. Does that recovered value change choice when both sources are accessible?
3. Can the embodied agent find the source again after a long absence?

The previous Stage 2 combines all three, with ongoing learning and renewed reinforcement. A failed readability check locates a task limitation but cannot decide the first two questions, or isolate which part of navigation causes the third.

## 2. Review findings, in priority order

### R1. The no-decay single-site and parallel modules are not generally equivalent

**Confirmed design assumption error, already visible in the recorded run; independently checked here.**

The H12 design section 2.2 says the two layouts have the same valence at every step, and section 5.2 labels H11 full an identity arm. The recorded Stage 2 output instead shows 350/400 trajectories departing, with a maximum value difference of about 0.204. The final summary printed by the same script still calls this a last-bit difference (`src/ph36b.py`, the bench and judgement print statements); that explanation is stale, even though the Vinc result record correctly explains the discrepancy.

`ph8.MB4.step` depends on compartment-specific reinforcement traces as well as the linear read-out. When reward and code coincide and reward then stops while code continues, potentiation driven by the past reward trace can cross zero. Opponent feedback then acts on different compartments in the two layouts. Linear equality of the read-out does not imply equality of the update rule across these input regimes.

**Instrument check:** `notes/reviews/h12_audit_probe.py` uses one deterministic module row, K=200, the already-used smoke code seed 5, and no behavioural seeds. Thirty simultaneous code/reward steps followed by sixty code-only steps produce maximum difference **0.2036079284**, first above 1e-12 at zero-based withdrawal step 5. Minimum values are **-0.0664196090** and **-0.2010007486**. Clearing eligibility traces at withdrawal, or setting potentiation to zero throughout the probe, removes the difference in this schedule. H11-style forward pairing agrees to **1.11e-16 at the sampled pairing boundaries**. These interventions are diagnostic controls, not proposed model changes or a proof covering all input schedules.

**Consequence:** H12 versus gate-only changes both layout and decay. It cannot attribute all differences to decay. A parallel/no-decay arm is a genuine mechanistic control in this regime, not an identity. The design's broader claims that positive extinction cannot cross zero and that parallel compartments are exclusively an extinction memory also need qualification to the tested update schedule: reinforcement traces can contribute potentiation as well as depression.

Sources: `src/ph8.py:67-99`; `experiments/h12/h12_design_v2.md:46-58`, `:157-165`; `experiments/h12/ph36b_bench.txt:192`, `:206`; Vinc `record:h12-stage2-bench-result`.

### R2. Masking navigation whiffs does not create an input-free retention interval

**Confirmed mismatch between the outline's interpretation and its detailed registration; not a code deviation from section 5.5.**

Section 5.1 says V is not met in P3. Section 5.5 explicitly registers a narrower operation: the mask removes whiffs, but standing near V still supplies V's code to the learning module without reinforcement. `src/ph36b.py:143-167` implements the latter. The bench reports **4,631 at-V steps in 267/400 H12 rows**, and **4,342 in 248/400 gate-only rows** during P3.

Thus P3 combines decay with further unreinforced learning and different exposure histories between arms. It is not the silent retention used by Stage 1. P3 is also 1,200 steps, whereas Stage 1's registered retention result is at 5,000. Under pure decay alone the fraction is **0.213391** at 1,200 versus **0.632157** at 5,000; neither predicts the complete embodied run, which has further input.

**Consequence:** retain the old verdict and outputs, and label that task as sensory masking with contact-driven learning. A new pure-retention experiment must assert zero code and zero external reinforcement on every retention step, while continuing the registered decay clock.

### R3. The current behaviour contrast does not isolate spontaneous memory recovery

**Confirmed identification limitation.**

The candidate and control follow different trajectories during extinction and retention, so they receive different training histories. P4 also restores reinforcement and continues plasticity. Comparing their final values (0.563 versus 0.317, medians) or final dwell therefore combines prior exposure, memory dynamics, physical state, new source contact and possible reacquisition. The supplied-trajectory replays establish the value read-out route; because they replay each learning arm's own values, they do not remove this confounding or independently validate recovery.

The ceiling/floor contrast additionally inherits different histories before P4: the floor falls to 0.45 at step 600, while the ceiling remains at 1.0. The ceiling's poor performance is strong evidence that the registered task cannot express the intended comparison; it is not a causal proof that position alone is the bottleneck.

**Consequence:** compare cloned memory checkpoints under controlled retention, then freeze memory and reinforcement during a common-start behavioural read-out. Keep natural return after loss as a separate question. The result would concern expression of stored value given access, not autonomous reacquisition of a lost plume.

Sources: `src/ph36b.py:106-169`; design sections 5.1 and 5.5; `experiments/h12/ph36b_bench.txt`.

### R4. The integrated learning address is supplied by source contact

**Correction to the assistant's earlier broad explanation and to the outlook if read as a statement of the integrated implementation.**

`src/ph15.py:55-61` builds code and reinforcement from the source the agent physically occupies. Its inputs are `codes, good, at`, not the held identity. `simulate` calls this after movement. H12 similarly uses `codeV * atV`. Consequently, learning-to-value-to-action has evidence, but recognition/hold-to-credit-assignment has not been established by these integrated results. It is possible to receive the source's code even when its navigation whiffs are masked.

This is a registered environmental teaching signal, not a newly discovered implementation bug. The error is treating the result as evidence that the agent independently decides which perceived object deserves credit. `notes/module_boundary_outlook.md` is explicitly an outlook and dated before Stage B/C; its attribution wording and its old statement that integration is still pending should not be quoted as current implementation status.

**Consequence:** a future reusable-core milestone needs a learning-input contract and a discriminating test with held identity different from contacted identity. Choosing to learn from a held item, a contact sensor, or another sensory history is a separate model decision. Do not silently replace the current input rule in H12.

### R5. Bench precision and signed recovery were over-interpretable

**Confirmed measurement limitation, largely disclosed in the original records.**

Stage 1's 200 rows produce the same values for the one-code schedules. Degenerate bootstrap intervals are numerical consistency, not evidence of reliability under 200 independent biological or environmental perturbations. SR at D=5000 follows the chosen decay equation. The substantive result is compatibility with the existing battery at the selected tau, not discovery of a recovery law.

The absolute-value SR metric can label a sign-inverted memory as recovered: the single-site S2 reward control has positive SR **0.3888** even though its delayed value is negative. The original record discloses this; it does not invalidate P's Stage 1 pass. RET **1.2279** is a ratio to the immediate post-training read-out, not a probability or literal percentage of stored synapses preserved.

**Consequence:** report signed value, sign preservation, acquisition and opposing components alongside recovery magnitude. For a new signed recovery score use the trained sign s and require a positive meaningful denominator: `s*(v_D-v_ext) / [s*(a-v_ext)]`, with `s*v_D > 0` reported explicitly. Do not retroactively replace the registered metric.

### R6. The next task should not be chosen to obtain a pass label

**Review judgement.**

H12 was explicitly selected by the owner to study memory, with no measured failure in earlier behaving runs calling for it. That is a legitimate capability-extension choice. It is not evidence that this extension has higher practical value than attribution, cold search or cue-loss robustness.

The previous recommendation to ensure V can be met again was a useful task-design direction, but premature as a complete plan: it addresses accessibility while leaving R1-R4 unresolved. A limited diagnosis has higher immediate value. Do not search over starts, competitor values, retention durations or navigation windows until a task passes. Fix one diagnostic matrix, then make one separately registered behavioural design.

## 3. Conclusions from earlier work that still stand

| Work | Keep | Do not extend to |
|---|---|---|
| H21 | Recorded 75% versus 57%; registered main comparison inconclusive; scoped adoption was a separate decision | A retrospectively relabelled PASS |
| H20 Stage B | Saturating training read out into behaviour; 369/400 valued dwell majority, learned-supplied outcome difference zero | Graded value calibration, unsupervised credit assignment, novel code ensembles |
| H20 Stage C Run 2 | Learning-on reduction in R-start punisher visits, 8 vs 56 vs 91 of 200; scoped registered criteria | The G3+ win criterion holding on all G3: the all-G3 result remains unreadable with 112/85/2 wins/ties/losses |
| H28 | Improvement under its three-channel distractor setup | General distractor resistance: 222/400 W1D rows still lost; the hold's necessity remains unmeasured there |
| H29 | Tested window trade at 200 with original prior; T1 difference -0.0075 and T3b dwell gain +1.9525 | A rule distinguishing loss from silence, universal optimality of 200, or transfer to the three-channel model |
| H12 | Stage 1 PASS; Stage 2 STOPPED/UNREADABLE; no adoption | Behavioural recovery proved, or mechanism disproved by the unreadable task |

The recurring lesson is a gap between module tests, learning-input schedules and behavioural opportunity. Registration and stopping rules worked in H12. They do not substitute for checking whether a design's causal interpretation follows from its actual input contract.

## 4. Next-work plan v1

This is a concrete proposal prepared under the review request. Existing hypothesis verdicts and the registered downstream order (H10, H18, H17 after disposition of H12) are unchanged. The plan has two work packages; only the review's tiny module instrument has run.

### Package D: bounded H12 diagnosis, measurement only

**Question:** which discrepancies arise from input timing, exposure, retention dynamics, and accessibility? No adoption or new behaviour PASS label is possible from this package.

**Files to create in the next execution:** `src/h12_diagnose.py`, `experiments/h12/diagnosis/{manifest.json,events.npz,summary.json,report.md}`. Import the existing modules unchanged. Use the already-spent Stage 2 bench pair from `ph36b.SEEDS['bench']`, and the already-used instrument smoke code seed. Do not use development or evaluation seeds. Record every reused seed as diagnostic reuse.

1. **Reproduce the existing bench before interventions.** Record source SHA-256s, Python/NumPy/platform and the complete arm table. Match integer counts (ceiling 42, floor 5, H12 33, gate-only 10; H11 departures 350), RNG identities and P3 contact counts. Match continuous outputs to their published precision, with any extra-precision comparison tolerance declared before execution. Stop and diagnose discrepancies before interpreting interventions.
2. **Record the learning and navigation inputs separately.** For each row/step: raw and masked whiffs, source contact, module code-present flag, external reinforcement, tc/tr summaries, valence and compartment outputs, held identity, presence counters, actual navigation hit and source position distance. Capture P2 end before step 2400 and P3 end before step 3600 without changing the original random draws. Assert the instrumented original remains identical on existing recorded fields. Expose the zero-input versus masking distinction directly.
3. **Replay identical inputs across module variants.** Use each of the three donor streams (H12, gate-only, H11 full) as a fixed input tape and replay it into A0, A1 and P from the same training protocol. Do not give the replayed module control over its donor's path. Report where same-input differences begin, signed inversions, and how much the closed-loop contrast changes with donor history. Reproduce each donor with its own module first. This separates input-history effects from module-update effects without claiming a unique additive decomposition of the closed loop.
4. **Clone A1 checkpoints to isolate retention decay.** Use every A1 row at the fixed P2 boundary, with no filtering for extinction success. Clone weights, codes and eligibility traces. Continue one clone with tau 5000 on compartments 2/3 and one without decay. Feed zero code and zero reinforcement for D in {0, 1200, 5000}. Assert clone equality at D=0, acquisition-weight invariance and zero training input at every step. Report signed value change, sign, comparator crossing and finite denominators. Clearing traces and disabling potentiation remain separate labelled diagnostic controls, never silent repairs to the adopted rule.
5. **Quantify opportunity at P4.** From the original arms report how many rows receive no V whiff, receive V whiffs but no V-directed navigation event, navigate on V but never reach it, reach but fail dwell majority, and tie. Partition ties into no source contact versus equal positive dwell. Measure filter eligibility and actual nav events, rather than infer cause from a distance or a global mean. Classify loss of opportunity versus failure to use opportunity without post-hoc exclusion from the main denominator.

**Exit:** a diagnosis report with every row accounted for, a reconciliation of the false identity, and the frozen input contract for Package E. If the original cannot be reproduced, the next task is provenance/runtime repair. If the issue is purely a contract ambiguity, correct it in an additive erratum before a new experiment. There is no parameter search or implicit continuation to evaluation.

### Package E: controlled expression of recovered memory, proposed new experiment

**Primary question:** from an identical extinguished parallel-memory checkpoint, does retention-only decay change subsequent choice when sensory opportunity and initial navigation state are held fixed?

This is narrower than the stopped H12 Stage 2. Turning decay on only after the checkpoint is an explicit causal intervention, not a replacement for H12's continuously decaying integrated agent. That full agent is a separately reported comparison, and autonomous return is deferred.

**Protocol to register after Package D and before any new task run:**

- Generate A1 memory checkpoints at the same fixed boundary using a specified training/input protocol, not selected because their values cross +0.5. Freeze this checkpoint generator in the new design. Use all rows; count those not extinguished and those with invalid recovery denominators.
- Clone each checkpoint into decay-on and decay-off retention arms. Retention input is exactly zero, tau=5000 where enabled. **D=5000 is primary** because it is Stage 1's registered endpoint; D=0 is the equality control; D=1200 is a reported bridge to the old stage. Do not select D after looking at choice results.
- At read-out construct new Agent17 bodies and the unchanged balanced World7 C0 start, with matched row identities, cast draws and random streams across arms. Keep the cloned memory values; reset non-memory navigation state identically by the existing constructor. This reset is a declared laboratory intervention. It does not establish natural recovery of a continuously moving agent.
- Present both plumes for 600 steps. Supply N=+0.5 as before. **Freeze all module weights and traces, including decay, throughout this read-out; no reinforcement or learning update occurs.** Read each retained V value into the existing value pathway. Test D=0 equality on every recorded field before any effect is judged.
- Controls: matched decay-off memory; fixed V=+1 and V=+0.45 with the same body reset; equal-value side-balance control; D=0 clone identity. Keep the original A0 and the continuously decaying P trajectory as separately labelled descriptive comparisons only if their construction is fixed beforehand. They are not substitutes for the matched checkpoint control.
- Main outcome: V dwell majority over all assigned rows in the 600-step read-out. Report N majority, zero-contact ties and equal-positive ties separately. Primary contrast is paired `P(V | decay-on, D=5000) - P(V | decay-off, D=5000)` over all rows. Do not restrict it to rows that crossed the competitor or happened to reach V. Value/rank crossing is a mediator, reported by row.

**Proposed bars, fixed in the final registration rather than fitted to a favourable bench result:**

| Check | Proposed reading | Stop/action |
|---|---|---|
| Implementation | D=0 clones identical; read-out module calls zero; no hidden input in retention; same random draws | Any violation is an implementation error; repair before an experimental result |
| Task readability | 95% lower bound of paired supplied high-minus-low contrast >= 0.30; high arm P(V) lower bound >= 0.70; tie upper bounds <= 0.20 in main/control arms; equal-value side balance interval inside [0.35, 0.65] | If missed, UNREADABLE for this task; no tuning to obtain a label |
| Effect of interest | Paired 95% lower bound >= +0.10 in the primary contrast | Lower >= +0.10: supported for this intervention; upper < +0.10: below the proposed bar; otherwise inconclusive |
| Mechanism description | Signed recovered value, sign preservation, rank crossing, unchanged acquisition pair | Report separately; no positive recovery claim based on absolute magnitude after sign inversion |

The +0.10 bar is a proposed practically meaningful minimum (40 of 400 net choices), not a value inferred from the failed bench's +0.0575 and not an approved criterion. Retain it or replace it with an explicit rationale **before calibration**. The stricter interval-based readability rules above are also proposed changes, not a reinterpretation of the old point-estimate rules.

**Sampling and decision discipline:** provisionally 400 matched rows, balanced by valued odour identity and source side; paired bootstrap 5000 replicates at 95%; one primary contrast. This is conditional on the specified odour-code ensemble. A separate held-out code ensemble is needed before claiming transfer. As a planning approximation, if the true improvement is 0.20 and discordance 0.50, SE is sqrt((0.50-0.20^2)/400)=0.0339 and the chance of clearing a +0.10 lower-bound bar is about 0.84; at improvement 0.15 with the same discordance it is about 0.30. These are assumed scenarios, not measured power. Do not silently enlarge n after seeing an evaluation.

Before code: choose and record non-overlapping calibration, development, evaluation and bootstrap seeds, including derived offsets; scan both repository and Vinc for use. Do not assign seed numbers in this draft as if that scan were done. The old unused evaluation pair is reserved to the stopped design, not silently repurposed. Record a checksum of the final design and seed manifest. Calibration can stop the proposed design; it cannot lower its effect bar. Verify runtime and identity instrumentation on development data. Run the evaluation once, then report all outcomes including missing/invalid rows. Missing rows are never silently dropped.

**Possible conclusions:**

- Readable with a positive registered effect: memory decay affects choice under controlled access; no assertion about natural plume search or held-item credit assignment.
- Readable but below the bar or inconclusive: a mechanistic module property is insufficient for the proposed behavioural effect at this scale; preserve that result.
- Unreadable: diagnose the read-out task before another memory mechanism is introduced. Do not use the new test to overwrite the old STOPPED result.

### Downstream work and boundaries

After disposition of H12, the existing queue remains H10, H18, H17 unless separately changed. Alongside that decision, define the product-level milestone: a reusable core requires an explicit learning-address contract and a held-versus-contacted disagreement test (R4), then robustness to new input statistics and code ensembles. This is a proposed acceptance requirement, not a newly adopted architecture or automatic reprioritisation.

H28's three-channel agent retains its 300-step window. Do not combine its burst rule, Agent17's 200-step window, H12 decay and learning-on into a universal agent without testing their composition. Avoid refactoring the frozen experimental import chain until a specific consumer and equivalence target exist.

## 5. Reproducibility and hand-off

The PC initially had clean `main` at eb78bb2 and the complete working branch at 6870b4d. This review uses a separate `codex/h12-review-plan` branch from 6870b4d; the original main and working branch were not advanced. Existing source/output bytes are unchanged.

The local instrument ran with `D:\Tools\Python\python.exe -E notes/reviews/h12_audit_probe.py`, Python 3.12.9 and NumPy 2.4.6. Its JSON includes source and probe SHA-256s and complete small traces. The H12 full scripts use `multiprocessing.get_context('fork')`, unavailable in native Windows; the tiny module instrument does not call it. A source checkout is not yet a validated Windows reproduction environment. Use a recorded Linux runtime for Package D, or separately verify a portable execution path against the existing outputs before using it. No global Python settings were changed.

Known misleading historical strings should be addressed in a dated erratum and in future reporting code. Do not edit old raw outputs, self-hashing scripts or old design text to make the record look correct retroactively. The registered behaviour stop, source hashes and adoption scopes are part of the evidence.

## 6. Evidence index

- Vinc: `concept:h12-differential-persistence`, `record:h12-bench-result`, `record:h12-stage2-bench-result`, `decision:h12-open`, `decision:h12-stage2-composition`. At review time no H12 closure or adoption was recorded.
- H12 final design: `experiments/h12/h12_design_v2.md`, Vinc doc `d27ec95924fe49be1`.
- H12 module and Stage 2: `src/ph36.py` (Vinc doc `d75b858c9487ed11e`), `src/ph36b.py` (Vinc doc `dd4b2e56d1a576518`).
- H12 outputs: `experiments/h12/ph36_bench.txt`, `ph36b_bench.txt`, `ph36_demo.txt`, `ph36b_demo.txt`.
- Earlier scope: `experiments/h20/h20_stage_b_report.md`, `h20_stage_c_run2_report.md`; `experiments/h21/h21_report.md`; `experiments/h28/h28_report.md`; `experiments/h29/h29_report.md`; `notes/module_boundary_outlook.md`; current working-branch `master_plan.md`.
- New instrument: `notes/reviews/h12_audit_probe.py`, `notes/reviews/h12_audit_probe_result.json` (measurement only, no new agent run).
