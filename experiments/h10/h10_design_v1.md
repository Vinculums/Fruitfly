# H10 design v1 DRAFT: abstention without losing evidence-driven revision

2026-09-27. Owner instruction: prepare the next test design and hand it to Fable. This authorizes design and handoff; the new equations, numeric bars and seeds below have not been ratified for evaluation. No H10 simulation has been run. Baseline: repository commit 98e0e4d; H12 closed, MB5 not adopted. H10 follows the confirmed queue, then H18 and H17.

## Question and evidence

Can a confidence stage reject insufficient evidence while a graded selector retains and revises identity without an external reset? Scope is a selection-module experiment. No claim about fly anatomy, autonomous navigation, learning, or architectural adoption follows from it.

Sources: concept:h10-abstention-and-revision-are-different-stages; src/ph7.py and experiments/h09/ph7_h9.txt; master_plan.md selection-and-hold section. H9's J=1.2, c=0.5, tau=10 candidate kept, revised and resisted a distractor in 200/200 historical easy-cue rows, but made 44/200 wrong choices on the hard cue. It already passed the historical zero-input idle criterion. Therefore H10 must address incorrect commitments under ambiguous evidence, not claim that H9 always commits on silence. Historical counts motivate this test; they are not new-seed baselines.

## Stage A: one explicit candidate family

Keep ph7.UP and ChanDiv unchanged. Use five channels, J=1.2, c=0.5, tau=10, and the remaining ChanDiv defaults. No reset drive, target label, phase flag, elapsed-trial clock or future sample may enter the candidate.

At each step compute the existing upstream output y and update the graded circuit once. In parallel update an evidence trace e, initially zero:

    e_next = (1 - 1/tau_e) * e + y/tau_e
    q = (largest(e_next) - second_largest(e_next)) / (sum(e_next) + 1e-12)
    gate = sum(e_next) > 1e-6 and q >= theta
    raw_identity = ph7.committed(graded_state)
    output = raw_identity if gate else -1

The gate only permits or suppresses the graded output; it never substitutes argmax(e), sets a winner, clears state or supplies a reset. e updates during silence too. Record cases where the evidence-trace leader and raw_identity disagree. This is an explicit output-gating implementation of the hypothesis, not a claim that an independent biological stage has been discovered.

Finite calibration family: tau_e in {40, 80, 160}, theta in {0.02, 0.05, 0.10}, exactly nine settings. The constants and family are proposals to be fixed before calibration. No adaptive expansion, repeated threshold fitting or new graded-circuit sweep after seeing results.

Arms on matched input tapes and noise streams:

1. Adopted bistable selector, external reset always zero: historical reference.
2. Fixed H9 graded selector without the confidence gate.
3. H10 candidate.
4. H10 with gate forced open: must match arm 2 on all states and outputs.
5. H10 with gate forced closed: negative control, must fail acquisition coverage.
6. Simple graded-state confidence mask: use the same formula for q but on the graded state instead of e; theta in {0.02, 0.05, 0.10}, selected on calibration only. This tests whether the new evidence trace buys more than a read-out threshold. Do not call H10 necessary if this simpler control performs equivalently.

## Inputs and outcome definitions

Reproduce ph7's exact update order and historical protocols first, including its fixed target/noise generators, without changing ph7.py. Then use a separate seed-explicit harness for new trials; no hard-coded ph7 helper seed may leak into calibration/development/evaluation. Materialize common upstream input tapes once per row and reuse them across arms. Separate and log target, input-noise, internal-noise and bootstrap generators. Every arm gets the same noise tape; extra gate state consumes no randomness.

All new conditions use 400 assigned rows. Targets are balanced over five identities; B is the next identity cyclically, fixed before execution. Raw input is retained exactly, including the historical helper's treatment of negative noisy samples.

- Hard cue: d=0.05, noise_sd=0.3, x0=1, 300 cue steps then 300 blank, following ph7.d1_d5. Repeat at x0={0.25,0.5,1,2,4} for the scale test.
- Easy acquisition and hold: d=0.4, 100 cue steps, then 300 blank.
- Revision: easy A cue, 50 blank, B alone at amplitude 2 for 100 steps, then 50 blank.
- Distractor: same prehistory and B amplitude but B lasts 20 steps, then 230 blank. Its difference from revision is duration, as in ph7.
- Idle: 400 zero-input steps from initial state.
- Ambiguous input diagnostic: the hard-cue noise and duration with d=0, followed by 300 blank. Report every identity and abstention; there is no privileged correct label. This is descriptive in v1, not a hidden extra gate.

Report correct, wrong, absent and multi-active raw states separately; raw multi-active maps to abstention under the historical read-out. Primary task rates use all 400 assigned rows. For hold/revision/distractor, success requires a correct A output at the named pre-challenge boundary and the required final output; never drop initial failures. Also report conditional rates with their denominators for historical comparison. Time-to-revision failures are censored, never removed from summaries.

Record transitions step by step: A-to-B with or without intervening empty output, gate closures, raw graded-state changes, and evidence-trace changes. No-reset does not imply a direct nonempty-to-nonempty revision. Distinguish those claims explicitly.

## Proposed decision criteria

Use two-sided 95% Wilson intervals for single proportions; paired percentile bootstrap, 5,000 shared row resamples, for between-arm differences. All gates intersect; no endpoint is selected after evaluation.

| Criterion | Proposed acceptance |
|---|---|
| Implementation | Historical protocol reproduction; forced-open identity; no reset; label-permutation equivariance with correspondingly permuted noise; finite states and complete rows |
| Easy acquisition | Correct A at cue end: lower bound >=0.90 |
| Hard-cue errors, every scale | Wrong proportion: upper bound <=0.025 |
| Anti-trivial abstention, every scale | Candidate correct minus bistable correct: paired lower bound >=-0.05; show raw correct/abstain counts |
| Retention | Correct acquisition followed by same correct identity after 300 blank, all-row lower bound >=0.90 |
| Revision | Correct A before challenge and correct B at final read, all-row lower bound >=0.85 |
| Distractor resistance | Correct A before challenge and correct A at final read, all-row lower bound >=0.90 |
| Idle | No exposed commitment at any of the 400 steps, lower bound >=0.98 |
| Added value of the gate | Ungated graded minus H10 hard-cue wrong rate at x0=1: paired lower bound >=0.05 |

The all-row bars differ from H9's conditional point-estimate bars and are new proposals, not retrospective changes to H9. Retain both sets of measurements. The simple graded-state mask is assessed on the same table. If it also passes, report that the separate evidence trace is not established as necessary; do not manufacture a superiority claim from nonsignificance.

## Selection, seeds and stop rules

Calibration chooses the first H10 setting passing all proposed gates in fixed lexicographic order (tau_e ascending, then theta ascending); choose the first simple-mask theta passing in ascending order. If none pass, stop as NOT SHOWN for this candidate family. Do not pick a best-looking failure. A passing control with no passing H10 candidate does not rescue H10.

After selection, freeze source, design, candidate and control configurations in a hash manifest. Development checks the frozen implementation and all gates on independent rows. Any scientific gate failure stops before evaluation. Implementation repairs must be disclosed, rehashed and verified without threshold changes. Evaluation runs once, only after development qualifies it; report null/inconclusive/failure without adding rows or changing the family.

Seed allocation is deliberately not filled with guessed numbers. Before v2 FINAL, Fable must list exact disjoint seeds for every condition and generator, including derived offsets, check repo and Vinc collisions, and publish the manifest. Previously used H9 seeds are for reproduction only. No evaluation seed is spent for debugging. Missing seeds or an incomplete manifest block execution, not design review.

## Stage B is conditional, not authorized by a module PASS

Before any body integration, inventory how Agent17 reads selector state, held identity, N2 release, presence, H19 navigation and the value gate. The candidate's actual output must drive the body; preserving a legacy held() path would bypass the intervention. Publish a composition record specifying which reset controller is replaced and re-sign the affected maintenance/release/distractor criteria. Keep the adopted agent untouched. Freeze body-level tasks, controls, bars and seeds in a separate design before executing them. Stage A alone cannot adopt H10.

## Fable deliverables

Review this draft and resolve any equation/protocol ambiguity before presenting v2 FINAL for owner confirmation of the new numeric choices. Implement only after that registration; run simulations on remote Linux as previously requested. Deliver raw row arrays, state trajectories, full stdout, source/design hashes, failure counts, registered verdict and interpretation. The planner should interpret those raw artifacts, not another model's summary. Preserve H12's closed status and do not start H18/H17 in parallel.
