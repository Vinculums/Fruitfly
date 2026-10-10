# H17 Run 3 design v3 FINAL: GS250 q-only growing cast on current Fly

Date: 2026-10-10. Status: FINAL specification confirmed under the owner instruction.
Owner instruction: "위 권고안에 따라 작업 착수 진행한다."
The immediately preceding recommendation named GS250 confirmation and its q-only
old/new/anchor/scope contract, then FINAL/runtime/schema/fresh-role reservation,
before a separate implementation/H0/bench execution opening.
This instruction confirms those concrete candidate/state choices and authorizes
this FINAL/reservation phase. It is not a fresh generator or evaluation claim.
Independent final verification is required before this package is registered ready.
Predecessors v1 and reviewed v2 DRAFT remain immutable; v2 canonical d73d7de44ea288ca0.
Current bridge: record:h17-r0-current-baseline, report d38fa7b26f04fc52c.
Historical decision:h17-closed remains unchanged. Adoption: none.

## 1. Confirmation, authority and scope

ONE GS250 candidate is selected for Run 3, and ONE new q-only state contract is
signed for this scope by decision:classification-rule-relaxed-any-odour-silence-counter-h17-run3.
The original H17/Run2 q signatures stay lapsed. This is an engineering navigation
quantity, not a new biological claim or a change to the original classification
rule outside this experiment.

Current Fly(nch=2), N2, presence window200/start140/prior60, gain, selection,
filter, ring, supplied known values and learning-off state are unchanged.
Exactly one original Fly.act is called. The enabled wrapper changes q and,
on engaged rows only, target/last_turn/returned-turn. No source position,
privileged geometry, stored pose/history, new entry clock, per-odour q or N1
restoration is authorized.

The fixed question is C0 delivered-whiff success by step599 in all400 rows,
with every added-success and T1/W1/T3 regression clause required. It is not
natural-N2-stranding proof, biological validation or adoption. No efficacy
measurement or candidate-effect forecast is performed in this phase.

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

## 3. Exact confirmed controller

Constants for this ONE FINAL: S250; L0=30; gamma15 degrees;
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
selected by this confirmed design.

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

## 4. Renewed H14-form state contract: SIGNED FOR RUN 3 ONLY

| Field | Confirmed contract |
|---|---|
| Old | Current Fly's own ring/wind estimate, since, silence, hold, presence and cast/flee state; no source or axis position and no privileged history |
| New | One aggregate q since any delivered odour whiff, initialized0; navigation target may read q only when no unique hold; u=q-250 and leg/slant derived without new persistent policy state |
| Anchor | Current R0 arrays distinguish q from silence/presence and show400 C0 entries atq250; since is not generally q. This is an engineering navigation quantity, not a fly-memory claim |
| Scope | GS250 Run 3 and its spent implementation-validity fixtures only, two channels, supplied values, learning off, fixed C0/T1/W1/T3, walls off, wind available under original World7 law |
| Signature | Signed under the owner instruction quoted above: decision:classification-rule-relaxed-any-odour-silence-counter-h17-run3. Old H17/Run2 signatures remain lapsed |
| Forbidden additions | Per-odour last-whiff/sign memory, stored entry pose/heading, source coordinates/identity, episode u counter, new cast-side state, state clamping, N1 restoration |
| Alternative declined | Using since or silence alone would react to filter/held-specific history; an entry-reset u would require a second relaxation |

Recorded diagnostic q/u/engaged/leg/entry fields must not become additional
controller memory. No wider three-channel, learning, wall or navigation
scope is inferred. The owner accepted both the single GS250 candidate and this renewed q-only contract by accepting the concrete prior recommendation. This signature opens no execution.

## 5. Fixed sample, reference and controls

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

## 6. Registered criteria, denominators and interval rules

These bars are the accepted normative choices: majority cold-start success,
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

| Required clause | Statistic | Registered bar |
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
stage-specific inference role is reserved in this FINAL registration.
No bootstrap or inference RNG is executed in this FINAL/reservation session.

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
GS entry[t]=engaged[t] AND NOT engaged[t-1], with false at construction; GSOff is always false. Reference/Passive/Agent17 use external rising shadow-marker eligibility, labeled observational. Record first and all later events separately.

At actual entry save PRE_POS/PRE_HEAD/PRE_ROT, EST/ring/core state, q/u,
since/silence/presence, cast/flee signs, last-whiff/nav indices, exact source
uniforms/probabilities and source geometry for reviewer diagnostics only.
Complete key/dtype/shape/blob grammar is frozen in the normative schema/keyset annexes below; implementation pins must match before fresh generators.
No candidate reads the saved source/geometry/anchor metadata.

For GS250, m is each row's FIRST actual entry; for Fly/Passive/Agent17 it is the first shadow marker, never actual intervention; GSOff has no actual entry (m=-1). Strict row windows use
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


## 8. Frozen validity grammar and implementation requirements

Normative schema: experiments/h17/h17_run3_evidence_schema.json,
source_doc de7a0ecbae0d8640a, SHA(a-p) hfhgafgkdkiopcbjmaailjdlepnlcpggmbidhhknjfmeodfeicacblnmbalgbaib.
Exact expanded non-blob array keys/dtypes/shapes:
experiments/h17/h17_run3_array_keysets.json, source_doc dc1dee4488863d6ce,
SHA(a-p) ihjaclekfppfhlkjkgmkchbgnhfadbogifkjphhmkppahnanenebljcllpephpmk.
MAIN has5580 arrays, H0 has5556: H0 excludes precisely all24 inference/ keys.
The schema fixes JSON root/record/provenance keysets and recursive typed tags too.
No object/pickle/downcast/undeclared extra key or inferred wildcard is allowed.

Efficacy namespaces: efficacy/<condition>/Fly and /GS250.
Validity namespaces: validity/<condition>/Passive, /Agent17 and /GSOff.
These validity arms are matched controls, never extra efficacy rows.
All original native outputs, sample50, construction, N2, lineage L3 and full
recursive Fly/up/sel/ring/mb state remain saved at their exact original dtype.
GS fieldset has original76 plus q only. Immutable class-level search-off config
adds no instance history. Recorded u/eligible/engaged/entry/leg/sign/anchor fields
remain external recorder arrays. q is never excluded from its own state record.

Events: construction(-1), then each tick pre -> base -> pre_wrapper -> wrapper -> bump.
base is original Fly._act after its return, BEFORE N2.
pre_wrapper is COMPLETE original Fly.act, after N2, BEFORE q update/overwrite.
wrapper is after q/override, before move. bump follows original move and bump.
E=1+5*T=3001. base_return_timeline is the complete original returned tuple.
RNG checkpoints: construction, then before/sense/wind/twin/base_act/wrapper/move/bump;
G=1+8*T=4801. No stream state may change from base_act through wrapper/move/bump.
No extra source/agent draw or duplicate base act may be hidden by instrumentation.

GS q_pre/q_post/u/leg/remaining are int64[T,R]; eligible/engaged/entry bool[T,R];
sigma/alpha int8[T,R]; BASE_TGT/BASE_TURN/BASE_CLIP/RESIDUAL and SEARCH_TGT/
SEARCH_CLIP/SEARCH_TURN float64[T,R]. Inactive diagnostics use u=-1,
leg/remaining/sigma/alpha=0, SEARCH_* corresponding BASE_* (no NaN).
The inactive rule is keyed on engaged, not eligible. GSOff updates q by the
same delivered-whiff law but class-level off forces engaged/entry false,
ever_engaged false, first_entry_step=-1 and entry_event_count0.

anchor_valid means actual first entry for GS250; external shadow marker for
Fly/Passive/Agent17; actual-none for GSOff. GSOff anchor_valid is allfalse,
integer/index/clock anchors-1, boolfalse, float0. Anchor mapping keeps native sample timing: TGT/TURN are BASE_TGT/BASE_TURN; q uses q_post, original state snapshots use pre_wrapper, while POS/HEAD/ROT/C/AT2 remain post-move entry-step baseline. The executed command stays sample/TGT and sample/TURN. Its external marker can exist
separately and cannot create an actual entry anchor. All subsequent entries
are reconstructed from the complete per-tick saved state/entry mask.

Disabled identity: full original construction/inputs/returns/outputs/state/world/
generator phases and L1/L2/L3 must match literal Fly, including Agent17's exact
registered lineage mapping. Only GS q is excluded from original-state comparison;
q still follows its own saved exact law. Existing clock/N2/presence/ring fields
are not exemptions. Tap callables act/bump and external recorder are the only
other existing exclusions.

Enabled GS uses its OWN direct original-BitGenerator primitive transcript.
Its complete pre_wrapper original state/return is proved against unchanged Fly
from the SAME candidate original pre-state, actual input and recorded primitives.
This is not a comparison to the free-running reference after divergence.
A data-only verifier reconstructs original operation order/N2 from saved data;
any controller replay used for implementation self-check is explicitly a
same-state validity replay with recorded primitive returns, never a second call
on the primary candidate or a new independent seed.
Before reserved streams, spent H0 must prove logger/plain passivity for the
enabled candidate too, from matched spent inputs, and per-call original-act
passivity at all declared mechanism boundaries.
Wrapper changes no original field except tgt/last_turn, plus declared q;
inactive returned turn/target/last_turn remain bitwise those of this base call.
Never-engaged complete rows remain identical to reference. Past-engaged rows
currently inactive are not required to equal free-running reference.

Reference and candidate use matched construction, generator primitive returns
and checkpoints. Their positions/probabilities/whiffs/inputs/core/outputs may
differ after divergence. W1 twin raw sensing/wind is compared at EACH ARM's
own actual pre-pose; masking preserves both source draws. Source calls stay
two random(R) then one wind random(R); original agent standard_normal calls
and creation budgets stay fixed, including zero-probability and certain wind.
Outer API calls only, unchanged handle/order/native nested-dispatch guard.

H0:40 rows,600 ticks, all fixed conditions/validity scopes, named public SPENT
h29 pair via module_identity.seeds_of('h29',True), original derived offsets.
No BENCH/DEV/EVAL role, inference generator, bootstrap or efficacy gate uses H0.
Deterministic synthetic fixtures cover q249/250, any delivered whiff including
NAVfalse, W1 masking, zero/unique/multiple holds, delayed q300/u50,
interruptions, leg30/90/180/300, slant150/300, residual order and bump semantics.
Constructed boundary state is VALIDITY_ONLY; it never enters efficacy denominators.

Runtime: experiments/h17/h17_run3_runtime.json, source_doc dcdcdc74a6f415241,
SHA(a-p) dhkhgbcnodhnjejeibigpagjoegnnjelndolgbjpghnocgjciojenioahpemiboh. Actual current stamp was read and equals R0:
CPython3.13.12, NumPy2.5.3, WindowsAMD64 little endian, assertions on,
optimize0, one local process, all six numerical thread settings1 before NumPy.
Executable/NumPy init/two native-library/config hashes are frozen in that file.
Any runtime drift stops before reserved generators.

## 9. Reserved roles, inference and durable claims

Config: config/h17-run3-seeds.json, source_doc db73cd95c357e7c63,
SHA(a-p) ppeengejcehflajckhoiefblfgoiibgacbgpkglepjmdjcicnjocgjfohdlamjlc.
Reservation: experiments/h17/h17_run3_seed_registration.json,
source_doc d47f07cd42242efa1, SHA(a-p) eebgnlmbfjnflojbfefbbdjefbbnjlajmbnllcobkaknebhfgfppogicfkgifcab.
For BENCH/DEV/EVAL separately reserve WORLD, AGENT and independent INFERENCE,
and expand BALANCE=WORLD+10000, GEOMETRY=WORLD+20000, CAST=AGENT+20000.
All18 values are distinct and absent from all pre-declaration repository bytes
and all258 canonical graph documents. Individual graph role searches also passed.
Complete local scan655 files, no hit/read error; graph oversized/transient reads
were resolved before declaration. Numeric values live only in config/registration.
Code streams remain src/fly.py CODE_SEEDS references. W1 twins/conditions/identity
arms reset matching roles intentionally; these are not extra independent samples.
Reservation creates no generator, draw, bootstrap, claim or execution permission.

For each MAIN stage use exactly Generator(PCG64(INFERENCE_stage)) and exactly
one integers(0,400,size=(5000,400),dtype=np.int64,endpoint=False).
Save the int64 matrix, initial/final generator state and original call evidence.
All seven paired endpoints across the four conditions use that SAME matrix:
delta int64[R], mean(delta[indices],axis=1,dtype=float64), then
np.quantile(replicate_mean,[0.025,0.975],method='linear').
Save differences,5000 means and interval arrays. No per-endpoint/per-condition
RNG/reseed. Independent verification reads indices/data and creates no RNG.

Use ONE registry experiments/h17/run3_registry/ across all stages.
Key is SHA(a-p) of canonical([WORLD,AGENT]), canonical JSON sorted/separator-fixed.
Stage/design/output/INFERENCE never enter that key. Claim immutable metadata
includes stage, all six role digests, FINAL/config/reservation/runtime/schema/
keysets/specification/execution/source/H0/opening hashes and prerequisite evidence.
Exclusively create and fsync claim before ANY stage generator, including identity,
construction and inference. Any failure preserves the consumed claim and first
failure/emergency receipt. Relabeling/reservation/output changes cannot repeat
the pair. No claim is created during this FINAL phase.

## 10. Stage gates, verdict and execution boundary

This phase completes candidate confirmation, signed q contract, reviewed FINAL,
exact runtime/evidence grammar, baseline specification closure and role reservation.
A separate execution opening is NEXT. No historical opening grants this execution.
Implementation runner/verifier/test hashes and a new matching H0 are not yet present
and are not represented as completed execution pins.

Future named artifacts: src/h17_run3_arm.py; tools/measure_h17_run3.py;
tools/verify_h17_run3.py; tests/test_h17_run3.py; tests/test_verify_h17_run3.py;
config/h17-run3-execution-opening.json; config/h17-run3-execution-pins.json;
experiments/h17/run3/H0, bench, dev, eval and run3_registry.
They are future requirements, not a claim these files or tests already exist.
The implementation/verifier are isolated from the adopted Fly/ph sources.
Freeze stable base implementation/source/config/runtime/schema pins BEFORE H0, excluding H0 result hashes from that base closure. After H0 verification, main execution pins add its completed receipt hashes before the first reserved generator. This avoids a pin/H0 self-reference cycle. These execution
pins are separate from this phase's completed specification pins.

After a separate implementation/H0/bench opening:
1. Implement and review; run meaningful mechanism/passivity/evidence/claim tests.
2. Pass new SPENT H0 on the exact final implementation closure, validity only.
3. Claim and run one fresh BENCH. Independently verify all evidence, then read all
   nine fixed clauses. Every clause must PASS to recommend the next stage.
   FAIL => NOT SHOWN for this scope; unresolved INCONCLUSIVE => INCONCLUSIVE/
   NOT SHOWN; validity fault => INVALID. Each stops. No retune/reseed/extension/
   horizon or margin change, no automatic replacement after output failure.
4. DEV requires the owner gate, saved BENCH all-PASS verification and its own
   exclusive fresh pair. Operation PASS means complete fixed sample/evidence,
   all validity/schema/runtime/source/draw/claim gates and independent/root
   recomputation pass, no error. No fit, tuning or efficacy selection from DEV.
   Its fixed clauses are reported for transparency but are not an extra efficacy
   gate or a reason to alter parameters. Operation failure stops EVAL.
5. EVAL requires the owner gate, DEV operation PASS and one exclusive pair.
   Apply the SAME complete fixed clauses and stop labels. Claim once.
   No retry or retrospective reinterpretation.

Each stage is reported before the next owner gate; the standing one-phase order
remains in force. The fixed conditional-window diagnostics never replace the
all400 efficacy denominator. A later claim/adoption remains the owner's decision.
No power/pass-probability forecast is inferred from R0 or ideal command geometry.

## 11. Source closure, history and package verification

This FINAL plus config/reservation/runtime/schema/keysets and unchanged original
R0 source/evidence anchors are frozen in config/h17-run3-specification-pins.json.
It is specification/baseline closure only, NOT a completed implementation/H0
execution pin set. Its actual hash and canonical source are attached in final
checks/decision; avoid a FINAL/pins self-reference cycle.
All96 R0 fixed files must remain byte-identical; reviewed v2 and anchor evidence
remain immutable. R0 pair already consumed once, never rerun as candidate bench.
Source references src/fly.py, ph11 World2, ph12b move, ph16 World7/cast_draw,
ph22 Masked, ph24 tick order, module_identity and existing recorder/verifier
retain their pinned original hashes.

Standing exclusions: experiments/h20/ph31_eval.txt with
decision:seed-scan-exclusion-ph31-eval; exact exception pairs with
decision:seed-scan-exception-pairs-r2. No new exception or folder exclusion.
P5 applies to all new design/review/evidence; hashes and raw bytes use a-p.
Original ph33/ph35 checkers and exact R2 manifest stay fixed.
Simulations only local/single-process/thread1 under P4; none in this phase.
No commit/push/merge/adoption. Q1-Q4 order and Q3 hold remain unchanged.
H17 historical NOT shown, hold D0 UNRESOLVED, A5/B3 bench stops and E1 below-screen
remain unchanged; this FINAL does not edit prior results or original criteria.

## 12. Concrete next action

Prepare the separate implementation/H0/bench execution opening on this verified
FINAL package. After that opening, implement the one fixed GS250 and independent
saved-evidence verifier, close reviewed execution pins, pass spent H0, then
consume only the BENCH pair once. DEV/EVAL remain held at their owner gates.
