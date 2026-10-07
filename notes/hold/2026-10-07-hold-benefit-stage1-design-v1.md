# (d) The hold's benefit — stage one design v1 DRAFT

Status: v1 DRAFT for owner review; design preparation and PR publication authorized, execution not authorized. This is a measurement-only design on `src/fly.py`; no experiment has been implemented or run. It neither establishes a hold benefit nor authorizes stage two, a world change, or a change to the adopted agent.

## Question and evidence

Before scoring benefit, distinguish three questions: can changing the identity read by navigation change a command at the same input and internal state; does a recorded experimental condition reach such a state; and can a comparison preserve its claimed input and random-draw controls? A difference in hold identity alone answers none of these. A difference in action is not evidence that the action is better.

Repository baseline: [merged source](https://github.com/Vinculums/Fruitfly/blob/0ee20d9/src/fly.py), especially `Fly.act`, `Fly._act`, `Fly.held`, `evidence_due`, and `Fly.estimate`. The [module identity report](https://github.com/Vinculums/Fruitfly/blob/0ee20d9/experiments/module/module_report.md), sections “Identity per row and layer” and “What the module does not claim”, records eleven real conditions plus one smoke row, with three-layer equality. It does not establish equality in every possible state or validate three-channel learning. Its historical adoption-status remarks are not treated as new decisions here.

The [H28 report](https://github.com/Vinculums/Fruitfly/blob/0ee20d9/experiments/h28/h28_report.md), “What is shown and what is not”, reports zero benefit for its hold-not-read comparison and the same W1D paths. That is evidence about those rows, not a proof that reading hold can never matter. Its M6 is not reused as a new stage-one success bar. H15's “no select-and-hold” control in `ph11.Agent.act` removes circuit use; it is a different intervention. H20's [Run Two report](https://github.com/Vinculums/Fruitfly/blob/0ee20d9/experiments/h20/h20_run2_report.md), “Where the failure appears”, separates first selection from the resulting trajectory and score. H20's known-answer control fixes identity by intervention; it is not the hold-not-read arm proposed here.

Operative decision texts read in the FruitFly space before drafting, with their read revisions:

- [decision:fly-reference-implementation](https://vincs.io/app/?space=01a0b944-ecb4-737b-b3e6-5cc99ff37654#view/trace/decision:fly-reference-implementation), revision five: item (b) closed; fly.py is the reference within eleven verified conditions plus the smoke check. Agent17 learning-on is included; three-channel learning and other conditions remain unverified. Existing experiment code is preserved; no behavior, performance or speed improvement is claimed. Q3 parallel work remains held.
- [decision:gain-g2-adopted-within-tested-conditions](https://vincs.io/app/?space=01a0b944-ecb4-737b-b3e6-5cc99ff37654#view/trace/decision:gain-g2-adopted-within-tested-conditions), revision four: G 2 is the baseline within Agent17/Agent16's recorded application conditions, without changing its value or code. It is neither an optimum nor generally superior. H20 Stage A remains NOT SHOWN and the G bench remains no-candidate; another G, world or learning condition needs separate verification. This housekeeping does not revise the recorded detailed Stage A criteria.
- [decision:seed-scan-exception-pairs-r2](https://vincs.io/app/?space=01a0b944-ecb4-737b-b3e6-5cc99ff37654#view/trace/decision:seed-scan-exception-pairs-r2), revision eleven: R2 closed at the recorded merge; the approved count/digest-bound exceptions are checked by the separate scan-only verifier. Legacy demo stops remain accepted. An edit to a registered file requires review rather than automatic re-signing.

Existing experiment sources, parameters, worlds, seed checkers, manifest and pins remain unchanged. These scope decisions do not authorize executing this new draft.

## Exact contrast: a read-out intervention, not circuit removal

Use the two-channel and three-channel forms separately. Reference H reads the actual post-circuit identity `h = held()`. Counterfactual R reads `q = argmax(y)` only when `max(y) > 0.05`, otherwise nothing. Here `y` is the same step's upstream output after the existing gain and gate. This is the historical H27/H28 read-out definition (`ph33.Act16.act`, `hr` and `hh`), including its threshold and lowest-index `argmax` tie convention, not a new fitted threshold. R does not remove the circuit or erase its state. It still depends indirectly on actual pre-step hold through the unchanged gate and evidence-release logic. This measures direct post-circuit read-out dependence, not the total causal contribution of hold.

For each local comparison, freeze one reference pre-step snapshot, observed whiffs, wind cue, world heading/rotation and random draws. Perform the common upstream, gate, release and circuit computation once. Derive H and R from that shared post-circuit state. Both projections use the same updated whiff counters and burst records; substitute only the read identity in the following read-out expressions:

| Expression | H | R |
|---|---|---|
| Value and whiff hit of the read identity | actual `h` | instantaneous `q` |
| Identity's presence override, `present = (c < N) or read_identity` | `h` override | `q` override |
| Top-valued eligible set; three-channel burst ranking | recomputed from H presence | recomputed from R presence with the same `bb` |
| `keep`, `nav`, flee condition | H identity and sets | R identity and sets |
| Next `since`, read-out `silence`, target, clipped and noisy turn | H expressions | R expressions, same starting clocks and turn draw |

The actual circuit identity returned to `Fly.act` remains `h` in both. The outer N2 wrapper reads actual previous/current circuit holds and actual-held whiff for its own `hit`, `new`, `negS`, `negZ`, `sustain` and `newz`; it may nevertheless see a different read-out silence counter. Record the post-wrapper silence separately. Do not replace all calls to `held()`, the gate identity, evidence release, circuit noise, or N2 identities with `q`. This boundary follows the historical distinction in `ph33.Act16.act`, which returns the actual circuit hold even for its hold-not-read arm.

No counterfactual state is written back to the running reference. In particular, do not call the stochastic `act` a second time on the live object to obtain an alternative. A future instrument must demonstrate that passive capture leaves the unchanged reference's state, outputs and generator states bitwise equal to an uninstrumented twin. The instrument itself and any executable counterfactual implementation require a later approval; this PR contains neither.

## Static branch audit, before reachability measurement

Read the code symbolically, distinguishing a locally admissible snapshot from one the experiment can reach. Enumerate held/nothing/ambiguous circuit states; unequal and tied non-negative values; negative values; presence just below/at the window; no burst, tied bursts and uniquely ranked bursts; whiffs absent, held-only, other-only and simultaneous; release due or not; target and turn saturation. Keep the existing thresholds and strict comparisons.

A candidate witness is not just `h != q`. It must carry enough state to calculate both projections consistently: circuit memory, upstream state and gated `y`, known values, pre/post whiff counters, burst history where applicable, clocks, cast sign, flee side, heading estimate, actual world heading/rotation, and the common noise draw. The audit reports the first differing expression and the final command. A constructed state may show a code branch without showing reachability.

Candidate routes to inspect, not experimental findings:

- **Same unique non-negative top value:** different identities can still yield the same `nav`. If the effective top set is a singleton, both routes often read that same whiff. Establish the equality conditions rather than counting every identity mismatch as exposure.
- **Tied top values:** if the effective eligible set contains the held channel and another channel, the held channel has no whiff, the other does, and H keeps the held channel while R reads the other, their `nav` can differ. At three channels the burst ranking must actually leave the relevant membership/tie; an unranked value tie alone is insufficient. Equal-value two-channel coverage is a distinct stratum, not an extension of the supplied-value adoption scope.
- **Presence override:** an old held channel can remain present despite its counter, while R overrides another channel or none. Determine whether this changes the maximum value, ranked membership and then navigation; record separately from a pure identity-read effect with identical eligible sets.
- **Negative-value route:** if actual hold is negative but R reads none or a non-negative channel, H's flee target can differ from R's surge/cast target. For example, silence with a surviving negative hold and `y` below the read-out threshold is a candidate local witness. Check the snapshot's circuit/release consistency before using it. Negative-value coverage is not a claim that every negative or learning condition is adopted or verified.
- **Hidden equality:** different `nav` or target may still produce equal clipped turns, or equal displacement after a world boundary response. Conversely, different silence with equal current commands can produce delayed differences. Report both current command equality and latent-state differences without calling the latter a measured action effect.

If the audit establishes no branch in a specified condition, state the restricted domain of that conclusion. If it finds none in all proposed existing conditions, stop before a benefit trial. Put two alternatives to the owner: commission a world-change design that exposes a documented branch, or defer (d). Do not change the world, a threshold, a value pair or a window to manufacture separation within this stage.

## Planned reachability sample and denominators

After approval of a final measurement design, use fixed, already recorded conditions, with no new trial budget or seed search. Proposed primary strata are the identity report's two-channel A1–A4 and three-channel B1–B2: T1/W1/T3a/T3b in the reference's tested two-channel setting, and T1D/W1D in its tested three-channel setting. Negative/tie coverage A5/A6/B3 is reported separately. Learning is off in these strata; A7/A7r and all three-channel learning are outside this first measurement. A later design that depends on an unverified path must first add the relevant identity evidence.

Use the exact world, masking, values, prior, windows, starting states, row count and horizon of the named historical condition; for T3b use the identity report's recorded onset, not the other onsets it did not test. Seeds are referenced only as each condition's `eval_w`/`eval_a` aliases resolving to `ph35.SEEDS['eval']` or `ph33.SEEDS['eval']`. Third-channel streams use that harness's named `D_OFF` and `A3_OFF` rules without copying digits. Reusing spent seeds supports a diagnosis of those rows, not a fresh confirmatory evaluation. No independent seed or number of reruns is selected here.

A stored trace can establish only quantities whose necessary state was actually retained. Module identity hashes cannot reconstruct missing gated inputs or alternate targets. Inventory recorded fields first. If the trace lacks any required state, mark that reading NOT MEASURABLE FROM ARCHIVE and request a separately authorized passive replay of the fixed condition; do not infer zero exposure from missing fields. This design-only task performs neither replay nor a new trial.

For every stratum, retain all assigned rows and all scheduled steps as the main denominator. Report counts of identity mismatch, different presence/top sets, different `nav`, different flee status, different target, different clipped turn, different final turn, and latent silence differences; then report conditional counts with their denominators alongside them. Include rows ever exposed, first eligible step, repeated events per row and the first differing expression. No eligibility filter removes a failed or never-exposed row from the main denominator. Separate constructed witnesses from naturally reached snapshots and identify release-adjacent/boundary events. Zero observed events means none in this fixed sample; it is not a universal impossibility result.

## What can be held equal

**Local coupled projection:** H and R share the exact reference snapshot and observations, known values, heading estimate and per-event noise. A copied world can optionally evaluate one-step movement for each command, then be discarded. Equality before the intervention and deterministic calculations can be checked exactly; current turn inequality must still be distinguished from displacement inequality. The reference world and agent advance only on H. These are local counterfactual measurements on H's state distribution, not a freely evolving R trajectory and not an unbiased estimate of long-run benefit.

**Fixed-input replay, if later authorized:** both projections can receive the same recorded observation tape even after commands differ. This isolates responses to an external tape; it is not two independently embodied agents navigating the same world, because the tape no longer follows R's position. State distributions and delayed effects must be labeled accordingly.

**Freely evolving trajectories, only in a later design:** arms can share world equations, source geometry, initial states and exogenous random variates. Once their actions change positions/headings, their plume exposure, wind-relative observations, wall contacts, actual rotations and later internal states can differ. Identical seeds do not make those endogenous observations identical. Never overwrite R's observations with H's and then report a natural trajectory comparison.

Audit random consumption by event and array shape, not just by the initial seed. `fly.py` draws circuit noise, a separate third-channel circuit stream when applicable, ring rotation noise, conditional ring cue noise when `wind_on.any()`, and turn noise; construction draws flee side. World sensing, masks and movement must be inspected in their actual inherited methods. A branch changing whether or how many draws occur breaks sequential coupling. If necessary, propose a separately reviewed exogenous draw-tape design indexed by step, row and draw role; do not retrofit the world or production agent in this PR. For the local comparison, calculate both read-outs from the same already-drawn buffer, so the read-out intervention adds no random draw.

## Stage-one interpretation and owner gates

| Finding | Permitted conclusion / next owner decision |
|---|---|
| Branch exists and is reached; passive reference and local input/draw equality verified | Action dependence is measurable in that named condition. Propose a separate stage-two design with preregistered benefit and cost measures; no benefit verdict yet. |
| Branch exists but no exposure in the fixed sample | No observed exposure; report denominators. Owner chooses a world-change design or deferral, not an adaptive search inside this measurement. |
| No branch within the audited conditions | Comparison is structurally uninformative there. Owner chooses world-change design or defer (d); do not change world here. |
| Missing archive state or failed passive-identity/coupling check | Measurement blocked or invalid; report the missing field/first mismatch, obtain a reviewed correction before execution. No zero-benefit claim. |
| Commands differ but controlled equivalence ends at trajectory divergence | Report only the local result; a later trajectory trial must allow endogenous observation divergence and define its own estimand. |

Stage two has no authorization, metric threshold, new seed registration or execution in this draft. The owner first decides the stage-one intervention boundary and sample, whether a passive replay is needed, and ultimately whether the evidence warrants benefit testing. The recorded research order is preserved; no parallel Q3 work is opened.

## Publication checks

Before commit: scan the final document bytes, including links and metadata, with the current original seed sets and digit-boundary rules; seeds remain aliases. Run the standalone R2 verifier with its manifest and pins unchanged and report cloud/local coverage separately. Inspect that only this design and `master_plan.md` differ from current main. These are documentation/integrity checks, not stage-one measurements or new experiments. A manifest count/digest conflict, if any, must be reported for owner review rather than remeasured or re-pinned.
