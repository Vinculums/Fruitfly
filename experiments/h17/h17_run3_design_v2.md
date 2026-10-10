# H17 Run 3 design v2 DRAFT: one q-only growing cast on current Fly

Date: 2026-10-10. Status: reviewed candidate-design proposal; NOT FINAL.
Owner instruction: "권고안에 따라 작업 이어 진행" (continue with the recommendation).
Predecessor: h17_run3_design_v1.md, kept immutable.
Current bridge: record:h17-r0-current-baseline; report source_doc d38fa7b26f04fc52c.
Historical H17 closure: decision:h17-closed, unchanged.

## 1. Deliverable and design authority

The owner authorized the next recommended candidate-design work after one valid R0.
This document proposes ONE concrete candidate, its renewed state contract and new
efficacy/regression criteria. It does not confirm the candidate, sign the relaxation,
freeze a FINAL, register seeds, implement a controller, generate fresh trajectories
or open a bench/development/evaluation. The current Fly and all R0 evidence remain
immutable. The only computations in this session read saved R0 arrays and perform
deterministic geometric/interval arithmetic.

Proposed candidate name: GS250, a q-only growing crosswind cast around current
Fly(nch=2). Current N2, presence window 200/start140/prior60, gain, selection,
filter, ring, learning-off setting and original base act remain unchanged.
The original Fly act is called exactly once; on eligible rows only, replace its
target and returned turn after the complete act, including N2.

The efficacy question is narrow: in the R0 position-only C0 stress, can this
controller find a delivered source whiff in a majority of rows by the fixed
600-step horizon while meeting registered comparison and regression clauses?
It is not a biological validation, natural-N2-stranding claim or an adoption.

## 2. Current evidence and actual loop anchor (P2)

R0 used one reserved pair, four matched conditions of 400 rows and 600 steps,
and passed twelve identity gates, independent verification, parent saved-array
arithmetic and final review. C0 had no whiff or reach in the full horizon.
Last-200 lost rows were T1 3/400, W1 35/400 and T3 139/400. Markers were
C0 400, T1 4, W1 70 and T3 16. T3 conditional recovery remains UNREADABLE.

The reviewing root read the AP archive, checked its byte hash and recomputed
entry summaries directly. Evidence: h17_run3_anchor_audit.json, canonical da13f38d62551dccd. C0 in every
row has first marker at index249, q_obs250 and post-act since250. At that same
instant silence is4, both presence counters390, presencefalse and no unique
hold. Neither silence nor presence nor since in other conditions replaces q.
T3 marker since spans260..270 while q is250.

C0 actual PRE_POS relative to the source-pair midpoint:
along x range9.845..28.184, median18.522;
cross y range-44.647..44.040.
Cast signs are198 positive and202 negative; flee sides are203 at90 degrees
and197 at270. No first-leg choice is made from these outcomes, outward
geometry, good identity or source position.

The policy switches targets after the complete base act and before this
tick's move. Its geometric path starts at actual PRE_POS/PRE_HEAD/PRE_ROT,
using the current post-act EST, core/ring state, q, cast/flee signs, presence
and last-whiff/nav indices. The baseline marker's post-move POS is NOT that
pre-intervention pose. In a future candidate run, save its own entry pose;
after the first divergence, reference poses cannot be substituted.

For every later active entry e, record its actual q_e, derived u_e, leg k_e,
remaining commands B_k-u_e and actual pose. If eligibility was delayed by a
hold, do not invent a pose at u0 or add displacement of legs never executed.
The candidate does not store or read pose/heading history; this anchor is
external evidence and the coordinate origin of the arithmetic.

An ideal command walk is saved only to audit signs, intervals and anchors.
It assumes instantaneous perfect heading, zero noise and cast sign+1:
u0..350 produces crosswind extrema about-34.773/+34.773, along minimum
about-23.294 and final along displacement about-7.920. These are commanded
geometry, NOT a simulated ring/motor/world path, success estimate, effect
prediction or power forecast. The final move at599 contributes to reach,
but a whiff after that move would be sensed at600 and is outside the run.

## 3. Exact proposed controller

Constants for this ONE DRAFT: S250; L0=30; gamma15 degrees;
slant half-period150, cycle300. UPWIND180, GAIN0.6, MAXTURN40 and speed0.6
are the current originals. The 150-step slant convention covers both
slants in a 300-command phase cycle. Guaranteed execution of both across that phase cycle requires uninterrupted
eligibility without a whiff reset; an observed K300 window does not guarantee
both commanded slants were executed. No parameter sweep is proposed.

New persistent controller state: q, int64, initialized0.
After exactly one original Fly.act returns turn_base,h:
q := 0 on any DELIVERED whiff this tick, otherwise q+1.
eligible := (q>=250) AND (h==-1).

Unique hold means exactly one circuit unit above HOLD. h==-1 also includes
multiple active units; do not replace it with an all-units-below-threshold test.
A delivered whiff resets q even if NAV is false or the value filter blocks it.
A masked W1 raw whiff never resets q. Negative holds retain the current N2 rule.

On eligible rows derive u=q-250; no second counter, episode timer or entry latch.
Let B_k=30*k*(k+1)/2; choose the first positive k such that u<B_k.
Thus leg k covers B_(k-1)<=u<B_k and lasts30*k commands.
sigma=cast_sign*(+1 for odd k, -1 for even k).
alpha=+1 when u mod300<150, otherwise-1.
target_search=(180+sigma*(90-alpha*15)) mod360.

| Phase u | Leg | Slant |
|---|---|---|
| 0..29 | 1 | upwind |
| 30..89 | 2 | upwind |
| 90..149 | 3 | upwind |
| 150..179 | 3 | downwind |
| 180..299 | 4 | downwind |
| 300..350 in this cold horizon | 5 | upwind |

At u0, cast_sign+1 gives target255 degrees, physically negative y;
cast_sign-1 gives105 degrees, physically positive y. Both have an upwind
component. This is independent of flee direction, source/outward sign,
good identity and every privileged world geometry field.

Hold interruptions do NOT pause or reset q/phase. For example, first eligibility
at q300 starts u50 in leg2 with40 commands remaining; it does not start leg1.
Any delivered whiff resets q and immediately exits search. Re-eligibility ages
from the subsequent silence. This minimal-state choice is deliberate; a fresh
episode phase on every entry would need a second signed variable and is not
selected by this proposal.

Freeze the operation order, including the returned-turn residual:
1. Call unchanged Fly.act once, including N2; retain its returned turn_base,h,
   current tgt_base and current EST. Compute q and eligibility from delivered input.
2. base_clip=clip(0.6*angdiff(tgt_base,EST),-40,+40).
   reused_residual=turn_base-base_clip.
3. search_turn=clip(0.6*angdiff(target_search,EST),-40,+40)+reused_residual.
   On inactive rows keep returned turn_base directly, bitwise.
4. On active rows only set tgt to target_search and last_turn to search_turn;
   return search_turn,h there. On inactive rows retain base target/last_turn.
5. Call original World3.move once, then original Fly.bump once, then record
   post-move reach/contacts. No learning step.

The residual is the rounded base-return residual, not a claim of bitwise
recovery of TURN_NOISE times the original standard-normal primitive.
Its subtraction/addition order is fixed. No additional RNG call, changed
noise draw order or final clipping of the noisy turn is allowed. The future
harness saves raw motor primitives and the base/residual/search commands.

Bump retains its original cast/flee-side change; q and derived phase are not
reset by a bump. The changed sign affects the next command. All efficacy
conditions have walls OFF, so contacts must be zero. Wall-on efficacy and
the old contact-based T3 criterion are outside this design.

## 4. Renewed H14-form state proposal: DRAFT, NOT SIGNED

| Field | Proposed contract |
|---|---|
| Old | Current Fly's own ring/wind estimate, since, silence, hold, presence and cast/flee state; no source or axis position and no privileged history |
| New | One aggregate q since any delivered odour whiff, initialized0; navigation target may read q only when no unique hold; u=q-250 and leg/slant derived without new persistent policy state |
| Anchor | Current R0 arrays distinguish q from silence/presence and show400 C0 entries atq250; since is not generally q. This is an engineering navigation quantity, not a fly-memory claim |
| Scope | Proposed GS250 only, two channels, supplied values, learning off, fixed C0/T1/W1/T3, walls off, wind available under original World7 law |
| Signature | NOT SIGNED by this design instruction; old H17/Run2 q signatures remain lapsed |
| Forbidden additions | Per-odour last-whiff/sign memory, stored entry pose/heading, source coordinates/identity, episode u counter, new cast-side state, state clamping, N1 restoration |
| Alternative declined | Using since or silence alone would react to filter/held-specific history; an entry-reset u would require a second relaxation |

Recorded diagnostic q/u/engaged/leg/entry fields must not become additional
controller memory. No wider three-channel, learning, wall or navigation
scope is inferred. Acceptance of this draft must name both the single
candidate and this renewed state contract before a FINAL can sign it.

## 5. Fixed proposed sample, reference and controls

For each future fresh bench, development and evaluation pair: C0/T1/W1/T3,
400 matched rows each, 600 sensing ticks0..599, four100-row World7 cells.
Use the R0 FINAL construction/plume/masking law unchanged, including
ordinary draws, role-separated balanced cells, C0 geometry draws and
cast assignment. C0 changes position only; no q45/since45 old release state.
Known values: C0 0/0, T1/W1 good+1 and other0, T3 good+1 and other-1.

Two efficacy arms: literal current Fly reference and GS250. Keep matched
world/source uniforms and original draw budgets; divergent positions may
produce different probabilities/outcomes from the same uniforms. W1 masks
good delivery after retaining both raw draws. Identity/lineage arms are
validity evidence, not independent efficacy samples.

No privileged-geometry oracle is required. C0's whiff baseline is reported
absolutely and as a paired difference; never divide by its near-zero share.
If any later FINAL adds a known-answer arm, its ceiling/floor and saturation
must be measured and relative clauses handled as SATURATED under P1. Old
oracle rates are not ceilings for this current composition.

## 6. New proposed criteria, denominators and interval rules

These bars are normative DRAFT choices: majority cold-start success,
at least ten percentage points confirmed added success, and limited
regression harm. They are not candidate-rate estimates and do not lower or
rejudge either closed H17 run's criteria.

For each row and condition:
E=any delivered whiff at sensing indices0..599.
L=no delivered whiff at indices400..599.
D_k=count of post-move distance strictly below3 to source k at0..599.
V=(D_good>D_other); ties and both-zero are not valued dwell-majority.
W1 D_other is nominal-other identity, not a fixed source index.
Every required denominator is ALL400 assigned rows/pairs, not engaged rows.

| Required clause | Statistic | Proposed bar |
|---|---|---|
| C0 absolute primary | GS250 E share; Wilson two-sided95 | lower bound>=0.50 |
| C0 added-success clause, same endpoint | mean(E_GS250-E_Fly), paired interval | lower bound>=+0.10 |
| T1 limited intervention | any eligible tick rows /400; Wilson two-sided95 | upper bound<=0.05 |
| T1 and T3 valued behavior | mean(V_GS250-V_Fly), separately each condition | paired lower bound>=-0.05 |
| T1, W1 and T3 loss | mean(L_GS250-L_Fly), separately each condition | paired upper bound<=+0.05 |
| W1 non-valued-source dwell | mean(D_other_GS250-D_other_Fly), steps per row | paired lower bound>=-6 steps |

The absolute C0 clause requires a majority demonstrated by its interval,
not merely a point of50%. At n400 the Wilson lower reaches0.50 first at
220/400 (55% point); 219/400 does not pass. At a50% point its half-width is
about4.88 percentage points. This is interval arithmetic, not predicted
candidate success. The worst binary paired SE bound is0.05; a rough normal
half-width can reach9.80 points. A point inside a5-point harm margin can
therefore remain INCONCLUSIVE. No post-bench widening of margins is allowed.

Wilson uses z1.959963984540054. All paired intervals use ONE fixed method:
5000 row-paired percentile bootstrap replicates; sample400 row indices with
replacement per replicate; compute the mean row difference, then quantiles
0.025 and0.975 with linear interpolation. The SAME index matrix is used for
all four matched conditions and all paired endpoints within one stage.
World/agent/geometry streams never supply inference draws; one fresh,
stage-specific inference role will be reserved only in the later FINAL.
No bootstrap or inference RNG is executed in this draft session.

A lower-bound clause is PASS if lower>=bar, FAIL if upper<bar, otherwise
INCONCLUSIVE. An upper-bound clause is PASS if upper<=bar, FAIL if lower>bar,
otherwise INCONCLUSIVE. All required clauses must PASS for an overall
efficacy PASS; a valid FAIL means NOT SHOWN for this scope; any unresolved
INCONCLUSIVE without a FAIL means INCONCLUSIVE/NOT SHOWN, never PASS.
Identity/provenance/schema/phase failures produce INVALID before statistics.
All clauses form a joint requirement; no subset can be selected as success.

Report C0 reach, source-specific whiff/reach, full/last200 dwell, cell strata,
N2 events/row incidence/concurrence and total contacts separately. A whiff
can occur before reaching a source; reaching a masked source is not a whiff.
No contact-driven or timeout-driven cause is inferred from co-occurrence.

## 7. Entry diagnostics and conditional windows

For each arm save q, derived u (inactive sentinel-1), eligible, leg, alpha,
base target/turn/clipped-command/residual, search target/turn, original noise,
all original outputs, typed state, generator checkpoints and input/return arrays.
External entry[t]=eligible[t] AND NOT eligible[t-1], with false at construction.
Record first and all later entries separately.

At actual entry save PRE_POS/PRE_HEAD/PRE_ROT, EST/ring/core state, q/u,
since/silence/presence, cast/flee signs, last-whiff/nav indices, exact source
uniforms/probabilities and source geometry for reviewer diagnostics only.
Freeze complete key/dtype/shape/blob grammar before fresh generators.
No candidate reads the saved source/geometry/anchor metadata.

For each arm, m is each row's FIRST actual entry. Strict row windows use
m+1..m+K for K100/200/300, with each row entering at most once per K.
The full-window denominator is the number of first-entry rows with m+K<=599;
Wilson intervals and the fifty-row screen refer to that row denominator.
Later entries are separate repeated-event diagnostics, never independent rows
or additions to these denominators; report repeated-event counts and distinct
row incidence separately without a repeated-entry efficacy interval.
Exclude AT2[m]; report this move's reach as entry-step baseline because GS250
may already change that move.
Full window requires m+K<=599; late windows are censored, not failures.
No-entry rows remain in every required all-row endpoint. Conditional groups
below50 are UNREADABLE and zero denominators UNDEFINED. Candidate/reference
entry populations differ after divergence; do not treat them as matched
conditional samples or use a treatment-defined subgroup as efficacy evidence.
For a descriptive shared risk set, reference first-marker rows may be used,
explicitly labeled; the all400 primary still governs.

## 8. Future implementation/validity/stage gates

Before any implementation/performance use: reviewed FINAL, candidate confirmation,
renewed q signature, fresh-role registration with full repository/graph checks,
and a separate execution opening. No grant is inferred from historical openings.

Required future mechanism checks:
- search disabled: full Fly state/input/return/output and generator identity,
  two-channel Agent17 lineage, current runtime; only declared new observation fields
  excluded, not existing clocks/N2/presence/core attributes.
- Same original state/input call: pre-wrapper base act is bitwise Fly, all original
  RNG primitive calls/returns/order and typed N2/core/ring state retained.
- Inactive rows retain current base-call turn/target/state. Never-engaged whole rows
  remain full-trajectory identical. After past activity, current inactivity does
  not imply equality to the untouched reference trajectory.
- Deterministic boundary schedules for q249/250, any-whiff reset including NAVfalse,
  masked raw W1 input, unique versus multiple holds, delayed q300 entry at u50,
  interruptions without phase reset, leg30/90/180/300 and slant150/300 boundaries,
  residual formula/order and original bump behavior.
- All original state and raw arrays are saved; identities and complete sample/
  provenance/geometry/masking/no-extra-draw checks precede aggregates. Root recomputes
  results independently from saved arrays (P3).

Proposed later sequence: public spent-input H0 for implementation validity only;
one fresh mechanism/efficacy bench with the fixed criteria; if every required
clause PASS, one development pair for operation checks without fitting; then
one exclusively claimed evaluation pair. FAIL/INCONCLUSIVE/INVALID at the
bench stops the sequence and preserves evidence; no fresh replacement,
parameter search, added horizon or reduced margin. Development operation errors
stop evaluation. Final evaluation is claimed once; failure cannot be retried
under another directory/design label. This sequence itself needs the later
execution opening. No old h2 pass-probability gate is imported.

No candidate effect or pass probability is registered from R0 or the ideal
command walk. An eventual valid fresh candidate bench supplies the first
candidate effect anchor; any later forecast would state that source/loop anchor
and uncertainty. Bench evidence never licenses changing this rule or its bars.

## 9. Seed, source and historical preservation

No numeric seed is proposed, registered or consumed here. Future roles are
stage-specific WORLD, AGENT, BALANCE, GEOMETRY, CAST and INFERENCE aliases;
derived roles must be disjoint from all earlier R0/hold/historical roles.
Keep code-stream constants by reference. No reuse of the consumed R0 pair
as candidate bench/development/evaluation or as candidate-effect evidence.

Standing exclusions: experiments/h20/ph31_eval.txt with
decision:seed-scan-exclusion-ph31-eval; exact registered exception pairs with
decision:seed-scan-exception-pairs-r2. No new exception or folder exclusion.
P5: all new documents/evidence use digit-free a-p hash/byte encoding and
protected seed token checks. Current Fly/ph sources, R0 FINAL/registration,
one-claim registry, raw arrays and historical results remain unchanged.

All future simulation is local, single process, numerical thread limits one.
There is no hosted run, commit, merge, publication or adoption in this design.
Q1-Q4 keep their recorded order, Q3 parallel work stays held. Hold D0 UNRESOLVED,
A5/B3 bench stops and E1 below-screen outcome remain unchanged.

## 10. Concrete recommendation after this reviewed draft

Confirm this single GS250 design and the q-only old/new/anchor/scope contract,
then finalize the specification, source/runtime/evidence grammar, fresh-role
reservation and exclusive-claim rules. Only after that should a separately
opened implementation/H0/bench sequence begin. This draft has made the action
reviewable; it has not signed or executed it.

Source references: src/fly.py current act, hold, target/motor and bump;
src/ph12b.py original move; src/ph26.py Search for residual/leg syntax only;
R0 FINAL experiments/h17/h17_r0_design_v2.md canonical db4aadf3b4101cef9;
R0 report canonical d38fa7b26f04fc52c and execution checks canonical
d90dd04d247b78bc3; standing P1-P5 in master_plan.md.
