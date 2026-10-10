# Hold stage two: completed, both benefit conditions stopped at the bench

Date: 2026-10-09. Scope: supplied negative values, learning off, World7 T1,
400 rows x 600 steps, the registered N2 negative-hold timeout behavior retained.

**A5 and B3 both stopped before development.** The registered benefit measure,
negative-source dwell R minus H, had a negative bench interval in both conditions.
A5 stopped on h1; B3 stopped on h1 and its R-arm tie fraction exceeded the
readability ceiling. No A5/B3 development or evaluation trajectory was run.
The single evaluation was the registered A6 H/R report-only pair. No benefit
claim or scope adoption follows from this run.

## Authority, execution and independent verification

Design: [v2 FINAL](../../notes/hold/2026-10-09-hold-stage2-coverage-design-v2.md),
all ten recommended section-12 choices confirmed. Seed roles are registered in
`config/hold-stage2-seeds.json`; repository and graph registration evidence is
`experiments/hold/hold_seed_registration.json`. No seed digits are copied here.

The runtime was local Python 3.13.12, NumPy 2.5.3, one process, BLAS threads 1.
`src/fly.py` and the ph-chain files were unchanged. `ReadOutFly` overrides the
navigation read boundary in `_act`; gate, release, circuit and inherited N2
still read the actual hold. R keeps its own silence/reset history and embodied
trajectory. A common random stream does not force its sensory observations to
equal H after divergence.

The root session independently recomputed the stored-row bootstrap intervals,
Wilson intervals, pass probabilities, stop rules and source-side mapping.
[Independent verification receipt](hold_results_verification.json), generated
by `tools/verify_hold_results.py`, reports PASS for the bench, empty development
stage and A6-only evaluation. Physical +y statistics below come from this
receipt. Its construction-only World7 mapping consumes no new simulation input.

Every stage records source, FINAL, seed-config, seed-registration and correction
note hashes. Partial stages carry `complete=false` and cannot open a successor
gate. Evaluation was claimed once in the fixed global
`experiments/hold/hold_stage2_eval_registry/` before its draws; the claim is
independent of output path and is retained. All output writes pass the protected
ph33/ph35 seed-token scan, including benchmark and derived stream tokens.

## Identities and the reviewed gate correction

The completed full identity receipt is
[hold_stage2_corrected/hold_stage2_identity.json](hold_stage2_corrected/hold_stage2_identity.json):
29 gates PASS at 400 x 600. It covers all nine nonlearning rows A1-A6/B1-B3,
actual-read switch-off L1/L2/L3 equality, H's ph-chain identity, three-channel
instant-read identity, two-channel trajectory controls, stage-one projection
link, two-channel Agent16 at window 200, and 600-step generator-state audits.
The audit includes world, D, agent, third-unit, cast and construction generators.

An earlier full run stopped at I4/A2 and was preserved in
[hold_stage2/hold_stage2_identity.json](hold_stage2/hold_stage2_identity.json).
All ten trajectory fields matched, but its gate incorrectly required equality
of W1's actual-hold diagnostics inside a combined historical summary. That
contradicted I4's explicit allowance for H/SIL/TO/EV differences. The root
reviewed the exact ten-key exclusion before the corrected smoke and full rerun;
the core arm, criteria, conditions and seeds were unchanged. See the
[operational correction](../../notes/hold/2026-10-09-hold-stage2-i4-gate-correction.md).
No new trial seed was consumed by the failed identity run.

I4 now compares all remaining W1 trajectory/sensory scores at zero tolerance.
Its separately reported differing-row counts for the excluded diagnostics are:
heldB 132; nothing 132; formed 46; released 40; end_to 40; end_ev 0; end_both 0;
end_none 0; fh 78; heldB_end 7. I1/I2/I3/I6 retain their full comparisons.

I5's first-command projection is checked only while each row's pre-step state
remains coupled. At A5, 182 first-command rows were coupled and 149 were outside
that check after earlier recorded-field divergence; at B3 the counts were 150
and 205. All applicable projection checks passed. `first_divergence_any` means
the first **recorded-field** difference, not an exhaustive attribute comparison.

Seven focused boundary/censoring/I4 regression tests passed. The root's complete
22-test suite passed under the same runtime, with the managed Windows fixture
ACL adapter. The failed gate and all smoke receipts are retained.

## Bench: the registered primary measure failed in both conditions

All denominators are 400 rows. Dwell units are steps within 3.0 of the specified
source. Intervals are paired percentile bootstrap, 5000 resamples, 95 percent;
unrounded endpoints decide the gates. M2 is strictly greater than zero. M3's
lower-bound margin is -0.05. M4 is reported, with no role in the verdict.

| Condition | Negative dwell H / R / Free | M2 R-H [95% interval] | M3 P(V) H-R [95% interval] | M4 lost R-H [95% interval], reported |
|---|---|---|---|---|
| A5 +1/-1 | 2.7800 / 1.6275 / 4.7925 | -1.1525 [-1.6675, -0.6849375], FAIL | +0.2725 [+0.2275, +0.3175], PASS | +0.1825 [+0.1350, +0.2325] |
| B3 +1/-1/0, D on | 2.8650 / 1.4150 / 4.3225 | -1.4500 [-1.8825, -1.0349375], FAIL | +0.1200 [+0.0750, +0.1650], PASS | +0.1100 [+0.0575, +0.1625] |

The negative M2 sign means R spent less time at the negative source than H in
these bench samples, opposite to the registered benefit direction. The positive
choice difference and lower H lost-row rate are descriptive secondary findings.
They do not replace the failed primary criterion, reopen a stopped condition or
constitute an evaluation result.

| Condition | Bench span Free-H | Ties H / R | Bench SD of paired dwell | M2 pass probability | M3 pass probability | Disposition |
|---|---|---|---|---|---|---|
| A5 | 2.0125, valid | 9/400 / 72/400 | 5.163743 | 6.64656e-11 | 1.0 | h1; stopped at the bench, NOT SHOWN |
| B3 | 1.4575, valid span | 46/400 / 98/400 | 4.428036 | 0.0 | 0.999999935 | h1 plus R ties 0.245 > 0.20; UNREADABLE |

The power calculation uses the frozen ph23 empirical SD convention, ddof=0,
and the registered normal approximation. Neither hS nor h2 fired. The bench
survivor list is empty.

| Condition/arm | P(V), all rows | Lost rows | Contacts/row | Negative whiffs/row | Mean leave latency | Censored leave rows |
|---|---|---|---|---|---|---|
| A5 H | 0.9300 | 34/400 | 0.3525 | 3.5950 | 15.8775 | 0 |
| A5 R | 0.6575 | 107/400 | 0.0000 | 2.5500 | 10.1200 | 0 |
| A5 Free | 0.9475 | 1/400 | 0.0000 | 4.4250 | 20.2900 | 1 |
| B3 H | 0.7525 | 128/400 | 24.9550 | 3.5050 | 18.5275 | 1 |
| B3 R | 0.6325 | 172/400 | 33.3950 | 2.2475 | 12.6175 | 1 |
| B3 Free | 0.9525 | 10/400 | 2.1875 | 4.2825 | 20.2475 | 1 |

Leave latency starts at the first negative whiff and ends at the first 30-step
continuous absence from that plume region; it is zero without a negative whiff
and censored at 600. These all-row means include the registered zero/censor
convention. The bench A6 H chance reference P(V) was 0.4725; Free supplied the
choice ceilings shown above. Wilson intervals and complete paired row arrays
are retained in the bench JSON.

Within each arm's own state, hold diagnostics are as follows. Actual versus
instant identity comparisons here are local within that arm; no same-input
step pairing is asserted after an H/R trajectory diverges.

| Condition/arm | Actual negative hold steps | Held negative, instant not | Instant negative, held not | Negative hold ends: evidence / timeout |
|---|---|---|---|---|
| A5 H | 40532 | 36556 | 5290 | 194 / 7 |
| A5 R | 59539 | 56593 | 4808 | 36 / 0 |
| B3 H | 4969 | 3087 | 5773 | 170 / 2 |
| B3 R | 3116 | 2211 | 4833 | 94 / 0 |

All H actual-negative and R read-negative flee checks were zero. R's actual
negative hold with target unequal to its flee side occurred on 56537 A5 and
2209 B3 row-steps, an intervention diagnostic. A5 and B3 had a recorded-field
divergence in all 400 rows; trajectory divergence occurred in 336 and 335 rows,
respectively. Per-row first-divergence steps are stored in the raw arrays.

## Development and the single evaluation

The development stage completed with an empty conditions/raw-arrays record.
The registered **dev world and dev agent seed roles were unused**, including
their balance, cast, D and third-unit derived streams: no development world or
agent was constructed. This stage records that both benefit conditions stayed
closed; it is not a development measurement.

The evaluation world and agent roles were used **only for A6 H/R at width two**.
Neither A5 nor B3 consumed an evaluation trajectory; no Free evaluation arm was
run. The evaluation's D and third-unit streams were not used. The bootstrap
role was used for bench statistics; A6 evaluation has no inferential criterion.
There was one evaluation invocation and its global claim remains.

A6 has supplied 0/0 and no negative source or valued-source hypothesis. The
uniform raw schema's negative-labelled keys at A6 refer only to the arbitrary
1-good source index; they are not an avoidance measure. No bar or benefit
verdict is assigned to A6.

| A6 pair | Recorded-field divergence rows | Trajectory divergence rows | Differing free-running clipped-command steps | Physical +y first H / R | Physical +y dwell majority H / R | Dwell ties H / R |
|---|---|---|---|---|---|---|
| Bench | 400/400 | 32/400 | 16798 / 240000 | 208/400 / 208/400 | 185/400 / 190/400 | 4/400 / 5/400 |
| Evaluation | 400/400 | 27/400 | 14056 / 240000 | 188/400 / 188/400 | 215/400 / 209/400 | 6/400 / 7/400 |

| A6 pair/arm | Mean dwell source index 0 | Mean dwell source index 1 | Source index 0 reached first |
|---|---|---|---|
| Bench H | 14.0075 | 14.0725 | 0.5400 |
| Bench R | 14.2075 | 13.8300 | 0.5400 |
| Evaluation H | 13.9825 | 14.3075 | 0.4500 |
| Evaluation R | 13.6425 | 14.4575 | 0.4500 |

The JSON field `side_balance` is **source index 0 first-arrival fraction**;
physical +y first-arrival and dwell-majority counts are supplied by the cited
independent verification receipt. All A6 rows reached a source. Its
differing-command counts are from independently evolving agents and
must not be compared directly with stage one's 64 local counterfactual command
steps on H's own state.

## Evidence and limits

Final measured receipts, each with complete per-row raw arrays and provenance:

- [Full corrected identities](hold_stage2_corrected/hold_stage2_identity.json)
- [Bench](hold_stage2_corrected/hold_stage2_bench.json)
- [Empty development stage](hold_stage2_corrected/hold_stage2_dev.json)
- [A6-only evaluation](hold_stage2_corrected/hold_stage2_eval.json)
- [Independent stored-row verification](hold_results_verification.json)

This closes the registered stage-two run at its bench stop rules. It establishes
no evaluated negative-source-dwell benefit in A5/B3, changes no adopted scope
and tunes no arm. Learning, different worlds, a repaired timeout chain and an
alternative primary criterion would each require a separate design and record.
