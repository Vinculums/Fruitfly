# H17 Run 3 design v1 DRAFT: establish the current cold-search target first

Date: 2026-10-09. Status: **v1 DRAFT; design opened, execution not opened**.
Owner instruction: "해당 순서로 작업 진행" (proceed in the recommended order).
Design decision: decision:h17-run3-open-design.
Predecessor disposition: decision:hold-followup-deferred.
Historical H17 closure: decision:h17-closed, unchanged.

## 0. Recommendation and the present boundary

Complete the current hold review, defer further hold trials, and open this
H17 design in the registered order. The authorized deliverable is a reviewed
draft. No new seed, harness, controller state, trajectory or benchmark is
created or consumed by this drafting session.

**Recommendation: measurement-first scope on current Fly; withhold a Run 3
performance candidate until its current failure population and loop anchor
are established.** This is a substantive draft disposition, not a claim that
H17 is impossible or that a future run cannot succeed. The historical
opposite-flee first-leg idea is retained as a candidate question only.

The next concrete proposal is R0, a passive current-baseline cold-search
measurement. R0 needs its own FINAL specification, source closure, fresh
seed registration and execution opening. This draft does not authorize R0.
Candidate choice, efficacy bars and power predictions are deliberately not
registered from old Agent10/Agent13 measurements.

## 1. What the existing evidence establishes

| Historical work | Stored outcome | What is carried forward |
|---|---|---|
| Run 1, Agent12 with S 210 | Normal T1 tracking engaged 18/400 rows; the upper bound 0.070 exceeded 0.05; bench (d) FAIL / NO CANDIDATE | A silence threshold can intercept the return cast's normal loop |
| Run 2, Agent13 with S 250 | Bench (d) passed with four engaged rows; T3 lost-row difference -0.0650, interval [-0.0900, -0.0425]; (h2) reference pass probability 0.2287 below 0.5 caused STOP | Increasing S did not clear the registered recovery gate |
| Run 2 post-bench diagnosis | Whiff after engagement in 18/105 stranded rows; among early-engaged rows, first leg toward the pair whiffed in 13/19, away in 5/65; 17/18 whiff rows left lost | A directional association on the old release-produced population, not an intervention effect |
| Current consolidation record | Fly is identical to adopted Agent17 at two channels and Agent16 at three; N2 excludes negative holds from sustained timeout drive and formation reset | The old agent and its natural stranding population cannot be presumed to be the current baseline |

Run 1 and Run 2 remain closed as NOT shown under their registered criteria.
Neither reached its development/evaluation tasks and neither adopted search.
The former silence-counter relaxations lapsed at that closure.

Exact sources: experiments/h17/ph26_bench.txt, final B line and (d);
experiments/h17/ph27_bench.txt, (h2) and final B line;
experiments/h17/h17_run2_post_bench_diagnosis.md sections 2, 3, 5 and 6;
master_plan.md, H17 queued-candidate note and standing rules P1-P5.

## 2. Current baseline and the missing bridge

Reference is **Fly(nch=2), supplied values, learning off**, with the adopted
gain, gate, value filter, presence prior/window, N2 release, exact-kernel ring,
return cast and motor noise. This is the Agent17-equivalent form; no older
Agent10g switch or search state is assumed to exist. Three-channel search and
learning integration are outside this first proposal.

The following differences require explicit treatment:

- Old Agent10 used the global maximum over odour values. Current Fly uses
  presence-scoped ranking, with the two-channel counter starting at 140 and
  the window 200. Navigation and the position before an intervention can differ.
- Old H25 applied sustained timeout drive to negative holds. Current N2
  excludes negative holds from sustain (negS) and from the formation reset
  (negZ), src/fly.py:277-290 and src/ph30.py:117-136.
- This disables the old **N1 sustained-negative-timeout-to-empty route**.
  It does not imply that a negative hold can never end, that Gaussian-noise
  losses are impossible, or that cold starts have been solved. Evidence
  resets, ordinary circuit evolution and other endings must be distinguished.
- The current negative release rule is not turned back to N1 to manufacture
  a population for Run 3. An N1-only diagnostic would be historical mechanism
  context, not the adopted reference and not a Run 3 success condition.

**G0, satisfied by source reading in this drafting session:** acknowledge the
baseline change and preserve N2. **G1, still unmeasured:** identify a reachable,
readable failure on current Fly. Old release-produced rows are not G1 evidence.
No baseline R0 was executed in this session.

## 3. Clock and loop-anchor contract (P2)

The old rule was q <- 0 on any whiff, otherwise q + 1; after the complete
base act, engage when q >= S and h < 0; search phase u = q - S. Leg k spans
30 k steps; its crosswind sign alternates, and the along-wind slant reverses
periodically (src/ph26.py:72-101). Run 2 changed S to 250.

On current Fly, since resets on filtered navigation, silence follows the
held odour and N2, and c includes the presence prior. None substitutes for
an any-odour q. A passive q_obs can describe whiff history without becoming
controller state; a controller that reads q requires a new signed relaxation.

The base return loop is anchored at its most recent nav event and walked
from the resulting pose. A proposed search loop would be anchored at the
pose and heading at its own registered engagement. Changing S, engagement
eligibility, first-leg side, phase or slant changes that walked anchor.
Record pose, true/estimated heading, cast sign, flee side, since, silence,
presence counters and the most recent any-whiff/nav indices at that event.

No old release-plus-S estimate, since == q identity, 13/19 directional rate,
T3 pass probability or scalar effect prediction is transplanted to current
Fly. The old diagnosis itself corrected since == q: only 70/105 old engaged
stranded rows satisfied it. P2 source: concept:standing-rule-loop-anchor;
experiments/h18/h18_stage_b_design_v2.md sections on a restarted loop's anchor.

## 4. R0 passive measurement proposal

Purpose: determine what current Fly fails to find or recover, and whether a
future search intervention has an eligible population. R0 measures only the
reference, with no target change or counterfactual trajectory. One execution,
local single process, thread counts one, all source/runtime/input/array
receipts saved. This is a proposal requiring a separate execution opening.

Proposed fixed sample: four conditions, 400 independent rows x 600 steps
each; World7 plume law and source separation unchanged, wind available on
every step, walls OFF in every R0 condition. Source identity and physical
side are balanced by the harness and recorded separately. Changing walls
from historical task runs is explicit; R0 is not a reproduction of their
effect sizes. No wall-on performance inference follows from R0.

| Condition | Construction and values | Primary descriptive measure |
|---|---|---|
| C0, geometric cold-start stress | Values 0/0, constructor hold empty; downwind along-source distance uniform [5,14], outward crosswind gap uniform [26,31] from an outer source axis, balanced outer side; verify probability zero for both plumes at step zero | Any original-source whiff within the first 300 steps, over all 400 rows |
| T1, ordinary tracking reference | Original World7 task start and supplied +1/0 | Rows with no original-source whiff in the last 200 steps, over all 400 |
| W1, absent valued source | Original World7 task start, +1/0, valued plume masked while retaining its raw draw, other plume present | Original-source whiff in the last 200 steps and non-valued-source dwell, reported separately over all 400 |
| T3, current negative-value reference | Original World7 task start, +1/-1, N2 unchanged | Lost rows: no original-source whiff in the last 200 steps, over all 400 |

C0 is a **constructed geometric stress condition**, derived from old release
geometry. It is not called a naturally produced current-N2 state. Move the
world position only as specified; leave constructor since/silence/presence,
ring, circuit and module state untouched. Do not import the old q=45 or
since=q initialization. Because current Fly constructs its flee side, C0's
outer side must use an independent construction stream, never be chosen to
agree with flee side or the candidate's direction.

C0 additionally reports any-whiff within 600, reach within 600 using distance
strictly less than 3 after the move, per-row first-whiff/source identity and physical
side. A whiff is sensed before movement; reach is measured after movement.
Natural conditions report selection, value choice, contacts (must be zero),
loss and dwell separately; a held identity is not substituted for a whiff.

Passive recording includes whiffs/raw uniforms, positions/headings,
held identity before/after act, presence, timeout/evidence requests,
sustain/zreset and circuit state. q_obs starts at zero and resets on any
original-source whiff. Record longest silence and the first q_obs >= 250
with h < 0 **as an observation marker**, not an actual engagement.
Report all rows, including those with no marker. Post-marker recovery is
conditional and never replaces C0's all-assigned-row statistic.

When a previously negative hold ends, label the observed transition, timeout/
evidence flags and N2 masks. A coincident flag is not a demonstrated cause.
Compute base/sustain/negS/negZ from the saved pre/post states and distinguish
the withheld N1 drive from an actual N2 action. Do not infer a drive-produced
stranding solely from a negative-to-empty transition.

## 5. R0 validity and stop rules

- Identity first: ordinary Fly and its passive instrument share complete
  construction, input/return arrays, all unmodified state and generator draws.
  Only declared private observation fields are excluded from same-class
  comparisons. Every generator checkpoint and draw ordering is retained.
- Reference lineage: keep full two-channel Fly/Agent17 identity through the
  measurement harness. No hold, release, presence or RNG field is discarded
  merely because it is diagnostic. Check the measurement sample and runtime
  against the immutable source/config/FINAL closure before and after recording.
- Exact recomputation: q_obs, first-whiff indices, loss, reach, state masks and
  every reported denominator must be reproducible from saved arrays.
- Any identity, sample-completeness, provenance, byte/hash, side balance,
  probability-zero C0 start, masked-draw or walls-off failure stops aggregation.
  An incomplete receipt cannot open a downstream stage.
- Wilson 95 percent intervals describe all-row binary measures. A conditional
  group below 50 rows is marked UNREADABLE; a zero denominator is undefined,
  not zero. Save the raw numerators and denominators beside every interval.
- R0 has no efficacy PASS label, bootstrap power stop, or automatic candidate
  search. It stops after one measurement report. If a proposed target population
  is absent, keep that fact and withhold that proposal; do not replace seeds,
  lengthen the horizon, retune a threshold or create the old N1 population.
- Reviewing root recomputes registered readings directly from the saved evidence
  before any measurement result is registered (P3). Simulation remains local (P4).

## 6. Run 3 candidate choices after the bridge

| Option | Present reading | What would be needed |
|---|---|---|
| Growing cold-search cast on current Fly | Closest continuation of general cold start; proposed, no current effect anchor | R0 failure and entry-state description; exact target intervention; renewed q relaxation; fixed geometry and regression conditions |
| First leg opposite prior flee direction | Historical association only; no supported current release-stranding population | Reachable current population and explicit side convention, wall behavior and entry phase; no causal prediction from 13/19 versus 5/65 |
| Last-whiff value-sign memory | New state; old data separate old stranded/tracking groups, not current groups | H14-form state authorization and a scoped question; do not call negative-only return a general cold-start solution |
| Lower T3 bar or revise stop-rule structure | Not recommended on old numbers | A new justified behavioral question and criterion, without re-judging either closed run |
| Defer Run 3 performance execution | **Recommended pending the current-baseline bridge** | Preserve current Fly, retain draft, decide after a separately opened R0 |

No candidate is selected by this draft. S 250 is an R0 observation marker,
not a newly validated engagement rule. A future candidate's source, allowed
state, no-extra-draw/noise reuse, entry/exit behavior and wall response must
be explicit before implementation. Any new state or reading has a signed
old/new/anchor/scope relaxation; the historical q signatures are not revived
by naming this work Run 3.

## 7. Future efficacy criteria and known-answer control (P1)

Future performance design needs one primary absolute measure, fixed reference/
candidate arms, a justified effect threshold, interval/verdict rules,
regression clauses and one evaluation claim. These are NOT fixed here from
the obsolete release population; this draft is not execution-ready.

If C0 first-whiff recovery is selected later, its all-assigned-row numerator
and window remain distinct from conditional post-marker recovery and source
reach. If a supplied-position known-answer probe is added, it must be
identified as a controller with privileged geometry, not an adopted agent.
Measure its absolute ceiling and the baseline floor before registering a
relative ratio. Old Run 2's known-answer whiff rate 0.990 and reach 1.000
are historical saturation warnings; they are not current-ceiling measurements.
A saturated relative clause is SATURATED and not read, never a passing gate.

The old T3 lost-difference bar and its old pass-probability estimate do not
transfer to a changed baseline, wall setting or failure population. New
effect/power arithmetic follows the registered loop-anchor audit and a
valid current sample; it is not produced by this drafting session.

## 8. Seeds, source preservation and execution authority

No seed is selected, proposed numerically, registered or consumed here.
If R0 is opened later, its world, agent and independent construction streams
are role-separated, checked against every existing role and derived stream,
and scanned over the repository and graph before registration. Statistical
resampling roles are assigned only if the FINAL measurement actually needs
them. Reference historical seeds by harness constants, not digits (P5).

The incidental historical exclusion experiments/h20/ph31_eval.txt is carried
by decision:seed-scan-exclusion-ph31-eval. The exact R2 exception-pair manifest
and source/downstream pins stay unchanged; decision:seed-scan-exception-pairs-r2.
No new exception or blanket folder exclusion is proposed.

Implementation and simulation require R0 FINAL plus its execution decision;
Run 3 candidate execution is a separate later gate. There is no PR merge,
publication, automatic run, extension, or new adoption in this design step.

## 9. Reviewable decisions

1. Keep the completed hold measurements and record operational deferral: done
   under decision:hold-followup-deferred, authorized by the current owner quote.
2. Open H17 Run 3 for design only, with current two-channel Fly as the reference.
3. Recommend R0 passive cold-search measurement as the next separately scoped
   proposal; no candidate or effect prediction before the bridge.
4. Keep N2 and adopted presence/window/heading state; do not restore N1 to
   reproduce a no-longer-applicable consequence.
5. Leave current performance execution on hold. The next deliverable after
   draft review is R0 FINAL and a concrete seed/gate specification, if selected.

These recommendations do not silently open R0 or a candidate bench. The
current instruction authorized this draft and disposition only.

## 10. Source appendix and audit

Primary canonical links: current Fly source_doc dd1fc3d20ef84ad9d;
Run 2 design source_doc d73c77ebd99d50d86; Run 2 diagnosis report_doc
dd1ba5b405811ef4a; diagnosis source_doc d9e169fcd01da251b;
historical search source_doc d911535d7e535751c (ph26) and ddfbebac743e3c469 (ph27).
Graph records: record:module-identity-result,
record:h17-run2-post-bench-diagnosis-result, concept:standing-rule-loop-anchor.
The local source snapshot hashes below use the digit-free a-p SHA alphabet.
Historical measured inputs are immutable; source code is read, never executed
as a trajectory generator during drafting.

| Local source or saved evidence | SHA-256 (a-p) |
|---|---|
| src/fly.py | dldgalcjabghimlmdbdmmkiihedfcpmhagniaolfepgnokfigimkbbpebjnbopme |
| src/ph21.py | dkbnhjnjkancdfpblophoedfomfjemppeaeibiaochlcinmnijcfjimfiebdmpmb |
| src/ph23.py | kobiaejcoomojdhdjnkenblfnidkbdkclecmfojfceefkjcklhfpjfmgplcolfko |
| src/ph24.py | pdeepbhiocadiaifipenheaaopghaccdpjakkcjchldphdaehhckobnieilnblop |
| src/ph26.py | bmjlgpflgodpadebogamhahmnfhhnheicjcomnlhcaagcomknkddddgbabobghmp |
| src/ph27.py | nbcpkgfbheojgiimjjmnkilaamhehmbpgjnfeaoanicoihnlgkfcioinfbimbedk |
| src/ph30.py | jiiccideaednofpdbgbfohdmnekideeeknmopcpbnfofgehidfgnhamkjafafjln |
| src/ph33.py | pckcjhcckdjimiblhphdabencjmhjjkaimcijomkbmmhdggkmngfofabfeohcala |
| src/ph35.py | oekdmonkcfgciohacgkgeigbknfbpiejhepbockhcahjechgnphagnaagkfclblb |
| src/ph9.py | hgjjleogplehkbloofphoeojjbkiikkmipkfkpdkjeacjhplneoeebeebpenjhag |
| src/ph11.py | oiapealnhbakmkedcfcpaedcjiegppkcjjedcfbnbjohbiefaojkhppejojehkcd |
| src/ph12.py | obadfoajimdlicijjiljjlafpijlhodlilmkbfpdacfddokchpmmebdjlkndkbmh |
| src/ph12b.py | omglbijgpgaopcocfanajcoapjpjpebafmagldipgjjinojahaamkdhbcbdoapkk |
| src/ph16.py | ddnfpnlcfjfjplhpjmloegfmkcfkijhdhhgldjpbofbhangefmlfdlminjagkcmc |
| src/module_identity.py | beffikmapflgbkekhbjhcmmnbkegbcdifocabgmlgkhfmoodemcpkmfhlbadnglf |
| experiments/module/identity.json | diogkenmdgfnejioblllfllplmiakpoegjjgbnnjbkompnpmelhdbilmpddfjlci |
| experiments/h17/ph26_bench.txt | omjnphickkecjejcegciejmjfhhoifdlknojgoopnbijbhgcgoojkaiojgedppgn |
| experiments/h17/ph27_bench.txt | hbhgchikmlppchjfgfoockhlmikiimifhndmjlhiahdccapoikienfpoaimgjlhb |
| experiments/h17/ph26b_diag.txt | baecjpflcmgjpbdnjdffhjckchaakblbokinihnkdblhfnjmefbglgiagkonnpbj |
| experiments/h17/ph27b_diag.txt | hkcoooofdomlmgnnahhledgpjmnfccamalamlilfjbniipiiihcfjnnefppneebo |
| experiments/h17/h17_post_bench_diagnosis.md | fcbcgolodkgcodofoabiakeiklcdmminaimfghibnfjalaknnokjhlbkneemonhf |
| experiments/h17/h17_run2_post_bench_diagnosis.md | mlicenmegdfhdfaenkdkbbjofokamdpohencodcelcghhkkajgcglenebplhfooa |
| experiments/h17/h17_run2_design_v2.md | ncdhemfodajbbiemggjkpfpioajkfgbljnhkmpgiaoglbaplmcbbhfapnanhnfoj |
| experiments/h18/h18_stage_b_design_v2.md | glaakfagpfglmhfmofhgmodhkcddeidfigakddkkmjggkedhgghkchldnlmkedab |
