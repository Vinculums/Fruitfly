# H21 design v1: hold maintenance by value in the H20 choice task

Date 2026-09-23. Status: **DRAFT for the owner's confirmation. No code.** Follows decision:h21-open-design (owner, 2026-09-23: 'hold 유지 규칙을 별도 가설로 설계하자') and decision:h20-run2-closed. A NEW hypothesis with its own criteria, seeds and record. H20 Run 2 stays closed as NOT shown; H20 is neither shown nor rejected; its Stages B and C stay queued. Supplied value only; no learning; no navigation change; no change to the timeout; G 2 carried from Run 2 and not adjusted.

## 1. Hypothesis

**H21: a hold on an odour that carries a positive value is maintained against a non-negative odour of lower value. While such an odour is held, a lower-valued non-negative odour neither displaces it in the selection circuit nor releases it; a higher-valued odour still can. With this rule, in the H20 choice task with the value supplied, the source the agent stays at follows the value.**

Two statements are bundled and are judged separately: (i) the rule maintains the hold (mechanism bench, section 4); (ii) a maintained valued hold is expressed in the dwell majority (task, sections 5 to 7).

## 2. The measured reason for this hypothesis (record:h20-run2-diagnosis, doc d73ddadcfb33103cd)

- The gain wins the first selection: 64 more rows hold the valued odour first, all one way, and the hold forms earlier in 271 of 400 rows.
- Those 64 holds convert into a valued majority at 21/64 = 0.328; the 210 rows both arms selected convert at 165/210 = 0.786 in both arms. The whole drop of the conversion rate lies in the added rows.
- Dwell at the neutral source is accumulated while holding the neutral odour (63 percent) or nothing (29 percent); 7 percent while holding the valued odour. A valued hold that stays is delivered by navigation (known-answer arm: 0.943).
- Holds end when the held unit's state has already decayed to the threshold (median 1.06 the step before; the fixed point of a hold with no input is near 2.0). 296 of 315 endings coincide with the evidence flag, 5 with the timeout flag (3998 firings). In the 77 N rows that lost a valued first hold, the agent was nearer the neutral source in 75 when it ended; valued whiffs were 1.7 per row afterwards against 9.1 neutral.
- Code reading, to be verified on the bench (section 4), not yet measured as a cause: in ph2.Circuit the held unit's drive is y_h + g*sigmoid(k(s_h - theta)) + s_h - S, with S the pool of both units. With no input the hold sits at s = 2*sigmoid(12(s - 1)), near 2.0, and is stable. When the OTHER channel's response y_o enters, s_o rises, S rises with it, and s_h falls toward 2 - s_o; past s_o = 1 the hold is lost. The release drive (10 into the pool for one step) lowers s_h by about 0.2 and is recovered within a few steps. **So what ends a valued hold is the neutral odour's response entering the circuit while the valued response is zero; the release flags are a coincidence of the same condition, not the mechanism.** A rule that only blocks the evidence flag would therefore not maintain the hold; the rule below removes the competing drive itself.

## 3. The change: one rule, two computational effects, boundaries stated

**Rule.** Let h be the odour held at the start of the step (the same hp the evidence-release comparison already uses) and v_k the value the agent reads for odour k (Agent3.chan_valence; the supplied `known` array in this run). Define

  gate_k = 0 if (h >= 0 and 0 <= v_k < v_h), else 1;   y''_k = y'_k * gate_k,

where y'_k = y_k * (1 + G*max(v_k, 0)) is the Run 2 response with the gain. y'' replaces y' in BOTH places y' is used: as the selection circuit's input and in the evidence-release comparison (y''[other] - y''[held] > MARGIN). Nothing else changes: navigation (hit = whiffs of the held odour; nothing held -> any non-negative whiff), the return cast, H19 (a), the ring, the learning module (not called), the flee, the timeout (silence > RESET_AFTER), the upstream stage, the gain G.

**Effects.** (1) While a higher-valued odour is held, a lower-valued non-negative odour's response does not enter the selection circuit, so it cannot lower the held unit through the pool. (2) It cannot trigger the evidence release. These are two effects of one gate; the bench measures the first, the identity checks the second.

**What the rule does NOT do.** With equal values (0/0, +1/+1) gate = 1 everywhere: the agent IS the Run 2 agent (M3). With nothing held gate = 1. A negative odour (v_k < 0) is never gated: the adopted avoidance path is untouched, so at values +1/-1 the agent IS the Run 2 agent (M3). A held odour of value 0 is still displaced by a valued odour (v_k = 1 > 0, gate 1): revision toward the higher value is kept. The timeout still fires and still resets; its firings and the holds it ends are reported (Run 2: 5 of 3998).

**Classification (owner's rule at the Stage A close).** The rule uses the agent's own value read-out and its own hold state; no source or axis position, no sensory history beyond what the circuit already holds. It changes what the agent does with what it knows, not what it knows.

**Alternative the owner may prefer (not the default):** gate negative odours too (gate_k = 0 whenever h >= 0 and v_k < v_h). Then an agent holding a valued odour would never switch to the punished odour and never flee it; the +1/-1 arms would become a test with Run 2's R4 (a, b, c) criteria instead of an identity check. The default keeps avoidance upstream of the positive bias, as Stage A registered.

## 4. Mechanism bench (before any task run; constructed input; no task, no score)

- **Circuit under test:** the H21 agent's own act with the G bench's stub world (Still: heading 0, rotation 0, wind cue on, no movement), so the selection block that runs on the bench is the one that runs in the task; navigation output ignored. 400 rows; freshly constructed agent; the circuit's own noise 0.01; G 2; values supplied.
- **(a) Maintenance.** Values +1 (channel 0) / 0 (channel 1). Phase 1: channel 0 alone, Bernoulli p 0.30 per step, 60 steps; rows holding channel 0 at step 60 are the denominator (their count and the rows not holding printed). Phase 2: channel 1 alone, p 0.30, 200 steps; channel 0 silent. Statistic: the fraction of denominator rows that hold channel 0 on EVERY step of phase 2 (a single lost step counts as lost). Wilson 95 percent. Reported beside it: the same at p 0.057; the number of timeout firings in phase 2 and the holds they ended; the held unit's s over phase 2 (median, min); the input-range records (y'' max, fraction y'' > 1.8, clip fraction, s max).
  **Bar:** with the rule, lower bound >= 0.95 (the input allows 1.0: the gated response is zero, and only the circuit's noise and the timeout resets act on the hold). **Reference, reported and not a bar:** the same protocol without the rule (the Run 2 agent), expected to lose most holds by the reading in section 2.
- **(b) Asymmetry, identity.** Values +1 / 0. Phase 1: channel 1 (value 0) alone, p 0.30, 60 steps. Phase 2: channel 0 (+1) alone, p 0.30, 200 steps. With the rule, the circuit states (s, S) are bitwise equal to the Run 2 agent's on the same draws (gate 1 because v_0 > v_h). Printed: the fraction of rows revised to channel 0 within phase 2 (both agents; the same number).
- **(c) Inertness, identity.** Values 0/0 and +1/+1, both channels p 0.30, 200 steps: circuit states bitwise equal to the Run 2 agent's. Values +1/-1, both channels p 0.30, 200 steps: bitwise equal to the Run 2 agent's (negative never gated).
- **Seeds:** whiff draws rng 20260926, agent rng 20260927, the same streams for every condition. **Stored** with the bench script and its sha256 before the task's first development run.
- **No-candidate rule:** if (a) fails its bar, the rule as specified does not maintain the hold; the task is NOT run and the design returns to the owner. The bar is not lowered to the number.

## 5. The task (as H20 Run 2, unchanged)

World, balance, start, cast side per row, 400 rows x 600 steps, no relocation, geometry C0, as design d3866101cd92f911d section 3. Values supplied +1 / 0 / -1; the learning module not called.

**Main measure, fixed:** the dwell majority (dwell_k = steps within 3.0 of source k; V / N / tie; a tie is no choice; every row exactly one class; all three counts per arm and per cell; no row dropped).

**Secondary and diagnostics, reported:** the first source reached (V / N / 0); first hold (odour, step); hold changes; the odour held at the first reach; the segment table; agreement of the majority with the first hold; dwell medians; no whiff in the last third; wall contacts; the input-range records. **Added from the diagnosis:** dwell at each source split by the odour held on that step (valued / neutral / nothing); steps with nothing held per row; hold endings by the flag on that step and by the held unit's s the step before; timeout firings and the holds they ended; rows that first held the neutral odour and were later revised to the valued odour (the revision rate the prediction uses); paired flips against rule-off on the same rows.

## 6. Arms (values supplied, learning off; all arms share world seed, agent seed, row index and cast draw)

| arm | values valued / other | G | rule | selection | role |
|---|---|---|---|---|---|
| maintain | +1 / 0 | 2 | on | circuit | main: does a maintained valued hold decide which source the agent stays at |
| rule-off | +1 / 0 | 2 | off | circuit | the Run 2 bias agent on these seeds: the rule's reference (M2 c) |
| rule-only | +1 / 0 | 0 | on | circuit | maintenance without the selection gain: which pathway carries the value |
| pathway-off | +1 / 0 | 0 | off | circuit | floor: the value present, no pathway (Agent3) |
| neutral | 0 / 0 | 2 | on | circuit | identity with G 0 (M3): the rule and the gain change nothing when every value is zero |
| known-answer | +1 / 0 | 0 | off | held odour fixed to the valued odour (ph17 intervention, per row) | ceiling of the measure on these seeds |
| priority-identity | +1 / -1 | 2 | on | circuit | identity with the Run 2 agent at +1 / -1 (M3): avoidance untouched by construction |

The known-answer arm is kept because floor and ceiling are validity clauses for the measure on the seeds actually run; it costs one arm.

## 7. Criteria

Statistics as Run 2: one fixed statistic per criterion; Wilson intervals for proportions; percentile bootstrap over rows for paired differences (5000 resamples, seed 20260928, matched rows resampled together); 95 percent; one evaluation, no extension; a group under 50 rows unreadable; the unrounded bound decides. Denominators: M2 uses every assigned row; M1's symmetry clauses use rows that chose (the tie rate capped separately). Aggregation: a criterion is PASS if every part passes, FAIL if any part fails, INCONCLUSIVE otherwise. Sampling unit the row; rows share no state (one generator per world and one per agent population, consumed in row order every step). The per-row odour codes do not vary with the seed; results are conditional on that set.

- **M1 task validity (else the run is UNREADABLE).** (a) Ties at most 20 percent of rows in neutral, pathway-off and known-answer (observed). (b) Side balance: neutral P(+y source majority | chose) interval within [0.35, 0.65]. (c) Floor: pathway-off P(V | chose) interval within [0.35, 0.65]. (d) Ceiling: known-answer P(V) over all 400 rows, lower bound >= 0.85.
- **M2 main (maintain arm).** (a) P(V) over all 400 rows: lower bound >= 0.70 (check example: at least 298 of 400). (b) Per cell P(V) over 100 rows: lower bound >= 0.55 in each cell (at least 65 of 100). (c) DP = P(V) maintain minus rule-off over the same rows: bootstrap lower bound >= +0.15. Reported beside it, no bar: DP maintain minus pathway-off (the gain and the rule together); P(V) maintain as a fraction of P(V) known-answer; rule-only P(V) with its interval and its DP against pathway-off; N and tie counts; the first-reach secondary for maintain, rule-off, pathway-off and known-answer.
- **M3 identities (printed in the run).** (i) neutral at G 2 with the rule bitwise equal to G 0 (positions, headings, circuit states) and G 0 equal to ph14.Agent3; (ii) priority-identity bitwise equal to the Run 2 agent (ph16.Agent4, G 2) at +1 / -1 on the same seeds; (iii) rule-off bitwise equal to ph16.Agent4 at +1 / 0; (iv) known-answer h equals the row's valued odour on every step and the hit equals that channel's whiffs.
- **M4 mechanism bench (section 4), run and passed before the task**; its output cited by sha256 in the report.
- **M5 avoidance.** By construction (negative never gated) the +1 / -1 agent is the Run 2 agent, verified in M3 (ii); Run 2's constructed-state check (negative held, valued presented, G 2: flee target on every negative-held step, equal to G 0's) is re-run and printed. If the owner chooses the alternative in section 3, M5 becomes Run 2's R4 (a, b, c) in full, with the priority-off reference arm added.

**H21 verdict:** the rule maintains a valued hold (M4) and a maintained valued hold decides which source the agent stays at (M1, M2, M3, M5 all PASS). A statement about a supplied value, this rule, C0 and the dwell-majority measure; not about learning, the first source reached, other G or other geometries.

## 8. Unreadable conditions

M1 failing (any part); ties above 20 percent in an arm under test; a cell under 50 rows; M3 failing (an implementation error, recorded as such and fixed before the evaluation); M4 not run or not passed (the task is not run).

## 9. Seeds, sizes, order

400 rows per arm, seven arms, plus the M3 reruns. Development seeds world 9860, agent 9960; evaluation seeds world 1720, agent 1820; both to be checked unused against every seed on record before the first run. Order: design confirmed -> minimal implementation (Agent6 = Agent4 plus the gate; no adopted module edited) -> identity self-checks -> mechanism bench (M4) -> development run for operation errors only -> one evaluation -> report. Any change before the evaluation is recorded as an amendment or an implementation error; nothing changes after the table.

## 10. Predictions, on record (arithmetic from Run 2's evaluation; the whiff supply will differ once holds are maintained, so these are ranges)

- M4 (a): with the rule >= 0.98 of holding rows keep the hold through 200 steps of neutral-only input at p 0.30; without the rule, under 0.30 keep it.
- Rows whose first hold is the valued odour: about 0.685 (Run 2: 274/400); a maintained valued hold is expressed at about 0.94 (known-answer). Rows whose first hold is the neutral odour and are later revised to the valued odour: Run 2 gave 48 of 125 = 0.38; with the rule the revised hold is then kept. Arithmetic: 0.685 x 0.94 + 0.315 x 0.38 x 0.94 = 0.76. **Prediction: maintain P(V) 0.70 to 0.80; DP against rule-off +0.15 to +0.30; DP against pathway-off +0.20 to +0.30.** This is the most uncertain prediction and it sits near the bar; the bar is not moved to it.
- rule-only (G 0 + rule): first hold at chance (0.50), kept when valued; neutral-first rows revised at Run 2's G 0 rate (61 of 186 = 0.33): 0.50 x 0.94 + 0.50 x 0.33 x 0.94 = 0.62. **Prediction 0.55 to 0.65.** If rule-only lands near maintain, maintenance carries more of the value than the selection gain does; if it lands near pathway-off, the gain is needed for the first selection. Reported, not a criterion.
- M1 passes (ties rare; ceiling 0.93 to 0.97). M3 identities hold by construction. Timeout firings comparable to Run 2 (about 10 per row), ending under 1 percent of holds.

## 11. What this design does not test

Learning (H20 Stage B), the integrated environment (Stage C), any G other than 2, any geometry other than C0, the first source reached as a main measure, the timeout (a recorded limit, record:silence-timeout-chain-result), the navigation rule when nothing is held (the 29 percent of neutral dwell accumulated with nothing held is reduced only indirectly, by fewer gaps), and any navigation change.

## 12. Open choices for the owner before v2

1. Negative odours: never gated (default, avoidance untouched, +1/-1 arm an identity check) or gated too (alternative, full R4 test).
2. Bars: 0.70 over all rows, 0.55 per cell, +0.15 against rule-off. The arithmetic in section 10 puts the prediction at 0.76 and +0.22; the bars are Run 2's for continuity, with the paired bar set on the rule's own reference.
3. The known-answer arm on these seeds: kept (recommended) or replaced by Run 2's 0.943 as the registered ceiling.
4. Seeds 9860/9960 and 1720/1820.
