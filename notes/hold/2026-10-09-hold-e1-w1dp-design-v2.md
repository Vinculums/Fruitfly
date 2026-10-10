# Hold E1: W1Dp branch exposure, design v2 FINAL

Date: 2026-10-09. Status: **v2 FINAL, owner-confirmed for implementation and one screen**.
Authority: decision:hold-e1-w1dp-open.
Owner instruction, verbatim: '권고안으로 작업 진행' (proceed with the recommendations).
This confirms all five recommendations in the preceding response and v1 section 12.

## Confirmed execution package and pre-run readings

W1Dp only. B4 +1/0/0 and B5 +1/-1/0, each 400 x 600. Only actual H advances;
unchanged PassiveFly projects H/R at the same state. D draws independently
from B's exact pre-move plume probability, consuming every row-step uniform.
Keep the unchanged three-channel window 300, G 2, N2 and learning off.
X1-X4, all-command exposure and separate tied-burst attribution are unchanged.
This FINAL makes no benefit or probability forecast and adopts nothing.

Fresh seeds: the screen role in config/hold-e1-seeds.json. Base and derived
streams were checked before registration against the whole repository and
individual Vinc literal searches, and are disjoint from all prior stage-two
roles. Receipt: experiments/hold/hold_e1_seed_registration.json. No exclusions
were added. All B4/B5 lineage/bare/passive versions share this pair; no other
experimental seed role. H0 retains the explicitly spent smoke alias only.

The historical cross-class L2 field contract is frozen from B2.L2.names in
experiments/module/identity.json (81 common, 26 lineage-only, no Fly-only).
Require the exact sets at every act/bump and compare common state/RNG bytes;
never infer a new intersection after a mismatch. Same-class passivity includes
all Fly attributes except only hr/hold_projection. H0 compares Agent16 lineage
against the untouched ph33.run lineage, all output keysets/bytes except arm/
cls/kind label metadata, all same-lineage state fields and RNG/draw audits.
Keep the historical module_identity.l3_scores contract unchanged. Its h28
W1 summary calls ph32.w1sum and contains four trajectory fields. To fulfill
the specified complete W1 diagnostic check, add ph25.w1sum (ph25.py:93),
which calls ph22.summary on the original B source and includes hold/release,
navigation, cast, contacts and trajectory diagnostics. Compare every field
of both summaries; do not apply stage-two diagnostic exclusions.

Runtime is Python 3.13.12, NumPy 2.5.3, local single process and BLAS threads 1,
assertions enabled. Source-byte pins from v1 apply to the unchanged references.
After code review, config/hold-e1-execution-pins.json additionally freezes the
runner, tests, FINAL/config/seed receipt, R2 manifest, historical identity and
import closure before H0. Its own bytes are carried in every run provenance.
No measurement-dependent edit to these pins is permitted.

Use only H0 as a smoke world. Constructed unit fixtures may test boundaries,
D uniform consumption, wiring and claim guards; no smaller W1Dp pilot is
opened. Full invocation requires a complete H0 receipt matching all current
pins. Make the pair-keyed exclusive durable claim, independent of output
folder, before any fresh screen generator construction, including identities.
Preserve a complete=false identity receipt before work, first mismatch and
claim on failure. Both full B4/B5 gates precede aggregation from the same saved
outputs. No second simulation to regenerate counts, no automatic repeat or
extension. Root independently recomputes headlines from saved arrays before
result registration, then runs the unchanged R2 scan-only verifier.

If a true identity failure is found, preserve it and stop. A source correction
needs a documented pre-measurement review; a claimed fresh pair cannot be
silently rerun. Report every X flag; only all four passing opens a separately
authorized benefit-design proposal. Any negative screen retains the unchanged
thresholds and ends without automatic seed replacement or condition tuning.

## Preserved v1 specification

The text below preserves the reviewed proposal and source appendix. Its draft
status and pending authorization language are superseded by the confirmed
package above. No observed E1 result is added to this FINAL.

# Hold E1: W1Dp branch exposure, design v1 DRAFT

Date: 2026-10-09. Status: **design opened; reviewed proposal, not an execution FINAL**.
Authority: decision:hold-e1-w1dp-open-design. Owner instruction:
'**W1Dp의 분기 노출만 검사하는 E1 설계** 진행' (proceed with the W1Dp
E1 branch-exposure design). This opens design work. New measurement seeds,
implementation and simulation are reserved for the execution FINAL.

## 1. Question and exact contrast

Does the unchanged three-channel reference agent reach a read-out command
branch often enough in W1Dp to make a later, separately designed benefit trial
readable? The main condition is supplied values +1/0/0, learning off.

Only H advances. After each actual act, PassiveFly reconstructs the same
step's gated upstream output y and projects navigation twice: H reads the
actual post-circuit held identity; R reads argmax(y) if max(y) > 0.05, otherwise
no identity. Both projections use H's pre-step cast clock, heading estimate,
sensory input and actual gate/release/circuit updates. Only H's returned noisy
turn moves the world. R's command, silence and other projected fields never
write back. This is a passive, same-state exposure estimand, not two agents.

The primary command is the clipped turn **before** the common noise draw.
An identity, navigation flag or target mismatch alone is not command exposure.
No benefit/cost criterion, learned-value trial or adoption is registered here.

## 2. Evidence used, and what remains unknown

Measured: [D0 report](../../experiments/hold/hold_d0_report.md),
record:hold-d0-result. All six primary replay strata passed their gates, with
zero differing commands in the recorded sample. B1/B2 each had four simultaneous
B-D burst steps and twelve raw latest-burst-tie steps, but no qualifying
tied-single observation; f_id was undefined. Held-counter margins were sample
checks, not universal bounds.

Arithmetic on fixed B2 positions: W1Dp's expected tied-single opportunities
were 118.312857, its expected exposed-row upper bound 118.048201 and its
probability upper bound for 40 rows was 1.0. The last quantity is uninformative,
not a calibrated probability of success. W1N's smaller bound does not decide
W1Dp. D0 remains UNRESOLVED; the present opening comes from the owner.

The B-plume duty fraction, tie occupancy and conditional identity split in
W1Dp are unmeasured. No numerical exposure prediction is registered. Coverage
A5/B3's bench results are separate and supply no anchor for +1/0/0 here.

## 3. W1Dp world: the sole condition change

Keep World7 geometry, balanced source assignment, midline start, heading and
cast initialization, walls, motion and wind exactly as ph33's W1 harness.
Use ph22.Masked unchanged: both source columns are drawn normally, then the
valued source V (index good) is masked False; B is source index 1-good.
Channel D is index 2, value 0, with no separate source position.

At the sensing position **before movement**, compute for B:

```text
along = position_x - B_source_x
cross = abs(position_y - B_source_y)
in_cone = (along > 0) and (along < LMAX)
          and (cross < W0 + SLOPE * along)
near = distance(position, B_source) < 3.0
p_B = (in_cone or near) * world.p_hit * exp(-max(along, 0) / LAM)
D_whiff = rngD.uniform_for_this_row_and_step < p_B
```

This is World2.sense's existing law: p_hit 0.3, LAM 12.0, LMAX 25.0,
W0 1.5, SLOPE 0.25. Read constants from the unchanged sources. Preserve strict
boundary inequalities and the near-source test even behind the source.
The probability is in [0, 0.3]. Do not replace D by B's sampled whiff, or share
B's uniform: B and D are conditionally independent given the sensing position.
Their histories need not be independent unconditionally on a moving path.

One D uniform per row per step is consumed even when p_B is zero. Construction
and per-step order remain ph33.run's: masked world, unmasked twin, rngD
construction, values, agent/third-unit generators, cast initialization;
then sense, wind, D draw,
twin audit, act, record, move and bump. The raw V draw remains consumed.
The sole harness switch is D's comparison probability: original P_D for H0,
B's plume law for B4/B5. No density, geometry or horizon is tuned.

## 4. Agents, conditions, size and planned files

| Label | Condition | Purpose | Size |
|---|---|---|---|
| H0 | Original W1D +1/0/0, Agent16 actual-read | New harness reproduces ph33.run byte for byte | module_identity.size_of('h28', True), 40 x 200 |
| B4 | W1Dp +1/0/0 | Primary exposure screen | 400 x 600 |
| B5 | W1Dp +1/-1/0 | Positive-control flee branch only | 400 x 600 |

B4/B5 each compare the unchanged ph33.build('A16') lineage, bare fly.Fly
at nch=3 and unchanged hold_stage1_instrument.PassiveFly at nch=3. Actual-read
H is used in all three runs. There is no hold-not-read feedback arm.
The three-channel window remains 300, G 2 and learning off. B5 preserves
the registered N2 behavior at negative holds, including the known timeout
limitation; its values are coverage, not adopted scope.

Planned implementation: one new runner, tools/replay_hold_e1.py, modelled on
ph33.run and the scoped taps/injection in tools/replay_hold_stage1.py. It may
reuse hold_d0_metrics.plume_probability for the deterministic p_B calculation
after validating the law. No existing agent, world or phase file is edited.
Planned outputs: experiments/hold/hold_e1/identity.json, exposure.json,
hold_e1_report.md and a durable single-run claim. These are future paths.

## 5. Identity and passivity gates before any exposure reading

H0 uses module_identity.seeds_of('h28', True), an explicitly reused smoke
alias. Compare the new runner's original-D mode with the untouched
ph33.run('W1', 'Agent16 D on', (1,0,0)). Check every recorded field including
HR, the Agent16 diagnostics and CONE, geometry/start metadata, draws_equal,
rng_equal, construction and all generator states. Class/arm labels are
metadata, not numerical identity fields. H0 must pass at zero tolerance.

B4 and B5 then each run the following comparisons on the registered full
screen pair. Preserve their outputs; release counts from those same outputs
only after **both conditions** finish all gates. Do not rerun a condition
as a second screen after examining its identity evidence.

| Comparison | Required evidence, zero tolerance |
|---|---|
| Agent16 lineage vs bare Fly | L1 = module_identity.L1B's 17 fields; L2 after every act/bump over the explicit historical common-state field map plus RNG states; L3 = module_identity.l3_scores('h28','W1',output,600) |
| Bare Fly vs PassiveFly | Same L1/L3; all base-state hashes with identical field sets, exactly 1200 act/bump events; identical act inputs/returns and generator states |
| H projection vs actual behavior | Identity, presence, navigation, cast clock, post-wrapper silence, target and pre-noise clipped turn match on every row-step |
| Observation wiring/sample | 400 complete rows, 600 complete steps, HR equals reconstructed instantaneous identity, all masks match their underlying arrays |
| Harness construction/draws | Masked/unmasked twin raw draws and wind equality; unchanged raw V consumption; explicit balance, cast, world, D, agent and third-unit states before/after their draw events |

For the cross-class L2 map, use the historical module identity contract;
list common, lineage-only and Fly-only attributes explicitly before the full
run. Do not silently drop a new mismatch or rely on an arbitrary attribute
count. For same-class passivity, only hr and hold_projection may be excluded,
as the existing MEASUREMENT_ATTRIBUTES declares; every base field is required.
Any further observer attribute must be external to the agent.

L3 checks dwell, contacts, first-source arrays, cls3, lost_t1 and the **complete**
W1 summary, including hold/release diagnostics. The stage-two I4 diagnostic
exclusion does not apply: E1's compared agents all advance actual H.
No tolerance, score exclusion or reference update may be added after a
mismatch. Stop at the first failing gate, preserve its receipt and diagnose
the implementation before a documented correction. Partial outputs never
open the count/report gate.

## 6. Observations and denominators

Primary denominator: all 400 B4 rows and all 600 steps, 240000 row-steps.
The corresponding B5 counts are labelled positive-control counts separately.
Conditional denominators are printed beside each conditional quantity;
empty denominators produce null/undefined, not zero.

Persist H/R projected identities, presence/top/eligible sets, navigation,
flee flag, target, clipped command, latent and post-wrapper silence. Save
per-row command counts, first command step (-1 if absent), first differing
expression, actual release-adjacent masks and wall-contact subsets. These
subsets are reports and never filter the primary denominator. Distinguish
raw burst timestamps from membership in an eligible ranked set.

Record simultaneous B-D bursts, raw latest-burst ties, one-member nonburst
whiffs, and each T1-T5 qualification from the preceding branch design on
the actual post-act/pre-move state. T1: V absent by counter in both projections
and read by neither. T2: B and D present/top in both. T3: their latest burst
timestamps equal and not NEVER. T4: exactly one member whiffs without bursting.
T5: one projection reads the non-whiffing tied member while the other reads
the whiffing member or nothing, producing different navigation. Define
f_id = count(T1&T2&T3&T4&T5) / count(T1&T2&T3&T4), null if the denominator
is zero. Report each condition,
their conjunction, the identity-split denominator and actual clipped-command
exposure within that conjunction. Also report command exposure outside it,
including presence-route exposure if observed; do not assert a universal
presence bound from D0's sample margins.

X3 uses **all differing clipped commands**, as previously registered, not
only qualifying tied-burst states. Passing X3 through another documented
branch does not establish the intended tied-burst explanation. A changed
target may produce equal clipped commands and is not counted as exposure.

For B4 H, lost_t1 is no whiff of either original source column during the
last 200 steps, exactly ph32.lost_t1. D is excluded even though co-emitted
from B's position. Persist the boolean lost mask, source/physical-side
mapping and contacts; label source index and physical +y separately.

## 7. Registered screen, carried unchanged

| Criterion | Exact rule |
|---|---|
| X1 | H0 plus all identity, passivity, draw/coupling and projection gates pass in B4 and B5 |
| X2 | At least one B5 row has a differing pre-noise clipped command |
| X3 | At least 40 of all 400 B4 rows have one or more differing clipped commands |
| X4 | B4 H lost rows are inclusively between 20 and 380 of 400 |

All four are required for **READABLE FOR A SEPARATE BENEFIT DESIGN**. This is
an exact finite-sample screen, not a hypothesis-test confidence bound. Report
raw counts/fractions without bootstrap or a new inferential bar. B5's loss
rate is reported and does not enter X4. X2 contains no ratio to B4, so no
ceiling/floor-relative known-answer clause is introduced (P1).

The legacy 40-row rationale used a best-case +0.05 paired lost-row contrast
scenario. It remains a design heuristic; passive exposure does not bound
free-running R's discordance after its own silence/circuit history diverges.
No power estimate, success probability or benefit claim is inferred here.

## 8. Outcome readings and stopping

| Outcome | Reading and disposition |
|---|---|
| H0/X1 fails or sample/provenance incomplete | BLOCKED/INVALID; no exposure verdict; preserve first mismatch |
| X1 passes, X2 fails | Positive control did not expose a command branch; BLOCKED for this screen. This alone does not prove an instrument bug. |
| X1/X2 pass, B4 exposure 0 | NOT REACHED IN THIS SAMPLE; below X3 |
| X1/X2 pass, B4 exposure 1-39 | REACHED, BELOW REGISTERED SCREEN; unreadable for the proposed benefit-design screen |
| X4 fails | UNREADABLE on loss-range criterion; no extension or density retuning |
| X1-X4 all pass | READABLE for a separate benefit design, in W1Dp only; route attribution reported independently |

Report all X flags even if several fail. Any follow-up benefit design would
need its own embodied arms, primary measure, seeds and owner opening.
No 1800-step extension, another layout, lower row threshold, seed search,
learning, constructed witness or repeat is triggered by a negative result.

## 9. Seeds, execution order and durable evidence

No new numerical seed is proposed or registered in this draft. At the FINAL,
choose one fresh screen world/agent pair and scan the whole repository and
graph for the base and derived balance, cast, D_OFF and A3_OFF streams, also
against the already registered stage-two seed roles. Write a distinct E1
config and scan receipt; do not edit the earlier seed registration. B4/B5 and
all three actual-H versions use this same pair. H0 uses only the spent smoke
alias. There are no bench, development, evaluation or bootstrap seed roles.

Before implementation: confirm section 12, issue v2 FINAL with scanned seed
registration and immutable source/runtime pins. Implement the new runner;
test the plume boundaries, independent D consumption, passive wiring and
durable gate. Use H0 smoke first. Claim the full E1 invocation exclusively
**before any fresh screen generator is constructed**, including identity
runs. The claim is keyed by canonical registered pair, independent of output
directory, and remains after a failure. B4/B5 full identities and passivity
then precede aggregation of the saved observations. One screen; no repeated
world simulation to obtain another exposure table.

Check source, FINAL/config/receipt hashes and runtime before and after each
gate; reject disabled assertions and incomplete prior receipts. Persist
per-row arrays/masks, bitwise comparison evidence, all RNG/construction
audits, the first failed gate and its field/step, and complete=false until
all required work finishes. Before result registration, the root session
independently recomputes exposed rows, command counts, lost rows, route
qualifications and X1-X4 from stored evidence (P3). Simulations are local,
Python 3.13.12/NumPy 2.5.3, one process and BLAS threads one (P4).

Run the R2 scan-only verifier and preserve its manifest/source/downstream
pins. Existing pair exclusion: experiments/h20/ph31_eval.txt,
decision:seed-scan-exclusion-ph31-eval. R2 exceptions remain exclusively the
registered pairs (decision:seed-scan-exception-pairs-r2); no new exclusion.
Protected ph33/ph35 seed tokens do not appear in notes or reports (P5),
including accidental output/hash matches. Use aliases and digit-free hashes;
a collision stops writing for representation review, never edits the sample.

## 10. Code references and behavioral-loop reading

| Reference | Role |
|---|---|
| src/ph11.py:74; src/ph9.py:34 | Plume law and its strict geometric boundaries |
| src/ph16.py:43; src/ph16.py:35 | World7 balance/start and per-row cast initialization |
| src/ph22.py:37 | Mask after consuming raw source draws |
| src/ph33.py:226; src/ph32.py:109 | Actual harness order and named D/third-unit stream offsets |
| src/fly.py:293; src/fly.py:315; src/fly.py:346 | Actual-H updates, burst/presence ranking and pre-noise command |
| src/hold_stage1_instrument.py:18 | Passive act and same-state H/R projections |
| tools/replay_hold_stage1.py:107; tools/replay_hold_stage1.py:162 | External taps and strict passivity gates |
| src/module_identity.py:179; src/ph32.py:378 | Complete historical score contract and lost-row definition |
| src/hold_d0_metrics.py:5 | Deterministic pre-move source probability |

These paths refer to the pinned local bytes from the completed D0/coverage
session. A source-hash appendix is recorded with the reviewed draft.

P2: cast phase is anchored to the agent's since counter, reset by actual H
navigation. Co-emitting D changes encounters, presence, bursts, gating and
therefore the cast/reset anchor and later positions despite unchanged agent
equations. This is why the frozen B2 probability proxy cannot forecast a
W1Dp loop or an exposure rate. No stationary-cycle or horizon-scaling
prediction is registered.

## 11. Design review requirements

Review before FINAL: exact near/cone probability, pre-move timing, independent
B/D consumption including zero probability, H0's complete known answer,
same-class vs cross-class L2 scope, complete W1 L3, pre-noise clipping,
T1-T5 vs all-command X3, original-source-only lost rows, fresh seed ownership,
and no free-running interpretation. Preserve the review and its corrections
separately. No simulation was used to write this draft.

## 12. Execution recommendations for owner review

The design opening is already authorized. The following is the concrete
execution package proposed for its later FINAL:

1. **Recommended:** W1Dp only, 400 x 600, +1/0/0 main and +1/-1/0 control,
   original constants and the independent B-plume D law. No other candidate.
2. **Recommended:** passive H/R projection on H's path, unchanged PassiveFly;
   one new runner, zero-tolerance H0/B4/B5 gates and full W1 scores.
3. **Recommended:** carry X1-X4 unchanged; report route attribution and null
   conditional denominators; no benefit or power criterion.
4. **Recommended:** one fresh screen pair, scanned at FINAL, shared across
   full controls; no exploratory trial, extension or second screen.
5. **Recommended:** count only after all gates, root independent stored-row
   recomputation, report and owner reading before any further design.

This draft finishes the requested design work. Confirming it as an execution
FINAL and choosing its new seeds is the next gate; no such confirmation is
asserted by the present document.

## Appendix: source byte provenance

SHA-256 uses the digit-free a-p alphabet, mapping to hexadecimal 0-f.
These are the source bytes read for this draft, not a future runner hash.

| Source | SHA-256 (a-p) |
|---|---|
| src/fly.py | dldgalcjabghimlmdbdmmkiihedfcpmhagniaolfepgnokfigimkbbpebjnbopme |
| src/ph11.py | oiapealnhbakmkedcfcpaedcjiegppkcjjedcfbnbjohbiefaojkhppejojehkcd |
| src/ph9.py | hgjjleogplehkbloofphoeojjbkiikkmipkfkpdkjeacjhplneoeebeebpenjhag |
| src/ph16.py | ddnfpnlcfjfjplhpjmloegfmkcfkijhdhhgldjpbofbhangefmlfdlminjagkcmc |
| src/ph22.py | adklimehaglbjffhkpfngeonnidpibckllkjblgbiedjgbildfidhkejnneemkbm |
| src/ph32.py | njpfifnffjjokjkepcbioihlniiepkicegkicgloabbbpejfmplomcjjkjccched |
| src/ph33.py | pckcjhcckdjimiblhphdabencjmhjjkaimcijomkbmmhdggkmngfofabfeohcala |
| src/module_identity.py | beffikmapflgbkekhbjhcmmnbkegbcdifocabgmlgkhfmoodemcpkmfhlbadnglf |
| src/hold_stage1_instrument.py | eboabjljipmeijcipdohcjebbpgpacnblkkocodhebjdadjelogdiagbjbijokgk |
| src/hold_d0_metrics.py | dnemlgalhbclcdckmkabaoodgnegphhggcfjjlnbellgcfehkecgiaegbnceeijf |
| tools/replay_hold_stage1.py | mkniffjmpboaodpkkkoomjneomdijabhbodaecdmbabcfbdnfobihiekffccbfng |
| tools/verify_seed_scan_r2.py | emfhapidcjidpgaofpbkefkbbkhdihknflepbhakdhkfceganepjhpiaobhiccac |
