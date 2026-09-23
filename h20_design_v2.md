# H20 design v2

Date 2026-09-20. Status: **DRAFT v2 for the owner's confirmation. No code.** Revises v1 (doc d1ade7c2ff6715415) on the owner's six review points. Pre-registration scope: **Stage A only** (supplied valence). Stages B and C are outlined in section 9 and are NOT part of this pre-registration.

Changes from v1, by the owner's point: (1) the gain's effect on the selection circuit's input range and saturation is recorded; the G bench is fully specified (input, initial state, noise, seeds), all candidates reported, a no-candidate rule, and a pre-set tolerance for the neutral case. (2) reaching a source and internal selection are separated: the main measure stays 'first source reached', and first hold, hold changes, hold-reach agreement and per-plume whiff counts are recorded as diagnostics. (3) A2's denominator is every assigned row; neutral choice and no-choice are reported beside it; the paired difference is over the same rows; the chooser-only preference is auxiliary; required success counts are computed here. (4) A1 reads whole intervals inside a pre-set tolerance; A3 becomes an implementation identity check. (5) A4 checks the flee command and behaviour against a G = 0 control with the same +1 / -1 values. (6) T-revise reports the pre-hold check, the revision event and the first reach separately, with a bounded wording.

## 1. Hypothesis (unchanged)

**H20: given the opportunity to approach both, the agent chooses the odour that carries a positive value over an odour that carries none.**

In the adopted agent a positive value has no behavioural effect: navigation approaches whatever Select-and-Hold holds, and only a negative value changes the target (the crosswind flee). H15 Run 2's free-running ungated arm, whose rewarded value had eroded to +0.05, behaved like the intact agent. What could show a positive value is a choice between two available odours.

## 2. The behavioural pathway: one change, odour selection

**Change.** After the upstream stage, the response y_k of odour k becomes y'_k = y_k * (1 + G * max(v_k, 0)), where v_k is the value the agent reads for odour k (Agent3.chan_valence: supplied in Stage A) and G is fixed on the bench. y' replaces y for BOTH consumers of the upstream output: the selection circuit's input and the evidence-release comparison (y'[other] - y'[held] > MARGIN). Nothing else changes: navigation, the return cast, H19 (a), the ring, the learning module, the flee. It is one line in act.

**Why this pathway.** Which odour is pursued is decided in one place, the selection circuit; the per-odour value read-out already exists; movement direction cannot express a choice (the agent does not know where the other source is); speed and dwell change how a chosen source is used, not which is chosen; a multiplicative factor on an existing signal is the smallest change.

**Priority of negative avoidance.** The gain applies to non-negative values only. If the held odour is negative the agent flees, whatever the other odour's value; H19 (a)'s rule (a whiff with nothing held is handed to navigation only if its odour is not negative) is unchanged. Negative avoidance is upstream of, and overrides, the positive bias. A4 checks this on the code path and in behaviour.

**Input range and saturation, recorded (owner's point 1).** The upstream stage bounds y_k below Rmax = 1.8, and the circuit was verified on inputs in [0, 1.8]. With the gain, y'_k can reach 1.8 * (1 + G): 2.7 at G = 0.5, 3.6 at G = 1, 5.4 at G = 2. The circuit clips its drive at S_MAX = 5. This is not treated as an error; it is measured. For the bench and for every task arm the record includes: max y' entering the circuit; the fraction of (row, step) pairs with y' > 1.8 (outside the verified range); the fraction of (row, step) pairs with any circuit state s_k >= 4.9 (the clip reached); max s. These are reported beside the results, and any arm whose clip fraction exceeds 1 percent is flagged in the report.

## 3. The G bench (fixed before Stage A; no task, no score)

- **Circuit under test:** the H20 agent's own act, called with a stub world (heading 0, rotation 0, wind cue on every step, no movement), so the selection block that runs in the bench is the one that runs in the task. Navigation output ignored.
- **Input:** boolean whiffs, independent Bernoulli per channel per step, equal rates on both channels. Criterion condition p = 0.057 per step (the task's start rate, section 4). Reported second condition p = 0.30 (the on-axis rate). Channel 0 is the biased channel (value +1, channel 1 value 0, supplied).
- **Initial state:** freshly constructed agent: circuit s = 0, S = 0, upstream P = 0, silence 0, nothing held.
- **Noise:** the circuit's own noise, 0.01 per step, as adopted; nothing added.
- **Seeds:** whiff draws rng 20260921; agent rng 20260922; 400 rows; 200 steps (about 11 expected whiffs per channel at p = 0.057).
- **Candidates:** G in {0, 0.5, 1, 2}; every candidate is run at both rates and every result is reported.
- **Measures per candidate:** P(first hold is channel 0 | any hold); rows with any hold; the channel held at step 200; number of hold changes; the input-range records of section 2.
- **Selection rule:** G* = the smallest candidate at p = 0.057 with the Wilson 95 percent lower bound of P(first hold is channel 0 | any hold) >= 0.85 (400 rows: observed >= 354 of 400 when all rows hold) AND at least 200 rows with any hold.
- **Neutral tolerance:** at G = 0 the interval of P(first hold is channel 0 | any hold) must lie entirely within [0.35, 0.65] (with 400 holding rows: observed between 159 and 241). If it does not, the bench itself is unreadable and Stage A does not run.
- **No-candidate rule:** if no candidate meets the selection rule, Stage A is NOT run; the result is recorded and the design returns to the owner (pathway or bench conditions), not to a wider candidate set chosen after seeing the numbers.
- The bench script, its output and G* are stored with sha256 before the task's first development run.

## 4. The minimal choice task

**World.** Two sources at one downwind coordinate, 10 units apart crosswind, in the 160x160 translated arena (walls at least 68 from either source); cones, whiff probability, speed and hit radius as everywhere else. With 10 units between axes the two cones overlap from 14 units downwind onward. **Start:** on the midline between the two axes, 20 units downwind of the sources (inside both cones: half-width there 6.5 against 5 to each axis), heading uniform random. Each plume delivers a whiff with probability 0.3 * exp(-20/12) = 0.057 per step, equal for the two. Equal availability at the start is a statement about sensory opportunity, not about reaching either source; section 6 records both.

**Balance, crossed 2 x 2.** Which odour code (A or B) carries the positive value: half the rows each. On which side (+y or -y) the valued source sits: half each, crossed with the first. 400 rows, 100 per cell, assigned by seeded permutation. The main measure is computed per cell and pooled.

**Trial.** 600 steps, one persistent trial per row, no relocation. **Choice = the first source the agent comes within 3.0 of.** No-choice = neither within 600 steps. Dwell at each source over the trial is recorded and reported separately, never used as the main measure.

**Outcome classes, fixed.** Every row is exactly one of: reached the valued source first (V), reached the neutral source first (N), no choice (0). All three counts are printed for every arm and every cell. No row is dropped from any table.

## 5. Arms, Stage A (values supplied, learning off)

| arm | values valued / other | G | start state | what it answers |
|---|---|---|---|---|
| bias | +1 / 0 | G* | empty (T-empty) | main question: does a supplied positive value decide which source is reached first |
| bias-revise | +1 / 0 | G* | neutral pre-held (T-revise) | can the bias revise an existing selection |
| neutral | 0 / 0 | G* | empty | side preference and the task's chance level (identical to G = 0 by A3) |
| pathway-off | +1 / 0 | 0 | empty | the agent as it is now: the value is present but has no pathway |
| priority | +1 / -1 | G* | empty | the valued odour reached, the negative one fled, with the gain on |
| priority-off | +1 / -1 | 0 | empty | the same values without the gain: the reference for A4 |

Values are supplied as ph11's `known` array (+1 / 0 / -1 per odour); the learning module is not called. All arms share world seed, agent seed and row index; matched rows are the same world and the same agent noise stream. Six arms x 400 rows x 600 steps.

## 6. Measures

**Main (per arm, per cell):** counts V, N, 0; first-approach step.

**Diagnostics separating selection from reaching (owner's point 2), per row:** first hold (which odour, at which step); the full sequence of hold changes and their count; the odour held at the moment of the first reach; agreement flags: first hold == source reached first, held-at-reach == source reached; whiff counts from each plume over the trial and the count of steps with whiffs from both plumes; for no-choice rows, their hold history (never held / held valued / held neutral). One fixed diagnostic reading, reported and not a gate: P(reached valued first | first hold was the valued odour) and P(reached valued first | first hold was the neutral odour). If the bias arm fails A2, these say whether selection did not follow the value (first hold not valued) or selection did and navigation did not deliver it (first hold valued, reach neutral or none).

**Other:** dwell at each source; late unrecovered on plume whiffs; the selection state at trial start, verified per row (empty, or holding the neutral odour in T-revise); wall contacts; the input-range and saturation records of section 2.

## 7. Criteria, Stage A

Statistics as in the H15 Run 2 specification: one fixed statistic per criterion, no post-hoc swap; Wilson intervals for proportions; percentile bootstrap over rows for paired differences (5000 resamples, seed 20260923, matched rows resampled together); PASS / FAIL / INCONCLUSIVE by the interval against the bar; a group under 50 rows is unreadable. **One evaluation at 95 percent, no extension**: FAIL or INCONCLUSIVE returns to design, never to a rerun. Development seeds (world 9820, agent 9920) for operation errors only; evaluation seeds (world 1680, agent 1780), unused by any run on record. Sampling unit: the row.

**Denominators.** A2 and A4(c) use every assigned row (the arms are compared on the same 400 rows). A1 uses rows that reached a source, because it asks about symmetry between the two choices; the no-choice rate is capped separately.

- **A1 task validity, three parts, all required, else Stage A is UNREADABLE.**
  (a) No-choice at most 20 percent of rows in the neutral and pathway-off arms (observed).
  (b) Side balance: in the neutral arm, the interval of P(reached +y first | reached) lies entirely within [0.35, 0.65]. With 360 reaching rows this is an observed proportion between 0.400 and 0.600; with 400, between 0.398 and 0.603. The tolerance is 15 points because the 2 x 2 crossing removes any side or identity preference from A2 by construction; A1 only has to exclude an asymmetry large enough to make the cells unequal in difficulty.
  (c) Pathway-off equivalence: the interval of P(reached valued first | reached) lies entirely within [0.35, 0.65] (same tolerance, same reading). This is the statement that without the pathway the value is not expressed.

- **A2 the main criterion (bias arm, T-empty), three parts, all required.**
  (a) P(reached valued first) over all 400 rows: Wilson lower bound >= 0.70. Required: at least 298 of 400 rows (observed 0.745).
  (b) Per cell, P(reached valued first) over the cell's 100 rows: lower bound >= 0.55 in each of the four cells. Required: at least 65 of 100 in every cell (observed 0.650).
  (c) DP = P(V) in bias minus P(V) in pathway-off, over the same 400 rows, bootstrap lower bound >= +0.20.
  Reported beside it, not a gate: the counts N and 0; the chooser-only preference P(V | reached) with its interval.
  Level check (owner's point 3): v1's intent was 'the valued source at least three times as often as the neutral one'. Over all rows that intent depends on the no-choice rate: 0.75 at no-choice 0, 0.675 at the predicted no-choice of 10 percent, 0.60 at the 20 percent cap. The bars 0.70 pooled and 0.55 per cell keep the intent at the predicted no-choice rate; with v1's 0.75 / 0.60 on this denominator the requirement would be 317 of 400 and 70 of 100, which at 10 percent no-choice is 88 percent of the reaching rows, more than v1 meant. The bars above are what is registered; they are not relaxed after the numbers.

- **A3 the gain alone changes nothing: an implementation identity check, not an arm.** With all values 0 the factor is exactly 1.0 for every channel, so the check is exact: the neutral arm run with G = G* and with G = 0, same seeds, 400 rows x 600 steps, must give bitwise-identical positions, headings and circuit states at every step (np.array_equal). A second identity: with G = 0 and any values, the H20 agent reproduces ph14.Agent3 step for step. Both are asserted in the self-checks and their result is printed in the run.

- **A4 priority (owner's point 5), three parts, all required.**
  (a) Code path: in both priority arms, on every (row, step) where the held odour's value is negative, the navigation target equals the flee side. Violations are counted over all rows and steps and must be 0.
  (b) Behaviour: dwell at the negative source over the trial (steps within 3.0), priority minus priority-off, paired bootstrap of the mean difference: upper bound <= +1.0 step (the gain does not increase time at the punished source). Reported beside it: the fraction of rows ever within 3.0 of the negative source, and for those rows the steps from first entry to first exit beyond 6.0, both arms.
  (c) P(reached valued first) over all rows in the priority arm: lower bound >= 0.70 (298 of 400).
  Reported, no bar: DP between priority and priority-off. The +1 / -1 condition does not isolate the positive value's effect (avoidance already sends the G = 0 agent away from the negative source); A2 isolates it. A4 shows that the gain leaves avoidance intact and that the two do not conflict.

- **A5 T-revise (owner's point 6): reported with a fixed reading, not a gate for H20.**
  Pre-hold: 30 steps with the neutral odour presented to the upstream stage (x = 1 on its channel every step) while the agent does not move; then the trial. Verified per row before the trial: the rows holding the neutral odour are the T-revise group; rows that failed the pre-hold are counted, reported, and not in the group; the group is unreadable under 50 rows.
  Events recorded separately: (i) revision = the first step at which the held odour changes from neutral to valued, with the count and the median step, and which release fired (evidence: y'[other] - y'[held] > MARGIN, or the silence timeout > 40; both are recorded at the release step); (ii) the first source reached; (iii) the agreement between the two.
  Reading: P(revision within 600 steps | T-revise group) lower bound >= 0.50 -> 'the bias revised a held neutral selection under this condition'. Otherwise -> 'revision was rare within this condition and time (counts)'. No generalisation to 'the bias cannot revise a selection'. P(reached valued first | T-revise group) is reported beside it.

**Stage A verdict:** the pathway carries a supplied positive value into the choice of source if A1, A2, A3 and A4 all PASS. It is a statement about a supplied value, not about learning and not about the integrated environment.

## 8. Unreadable conditions

The bench not on record, or no candidate meeting the selection rule, or the neutral tolerance failed; no-choice above 20 percent in an arm under test; a cell under 50 rows; A1 failing; the T-revise group under 50 rows (A5 only); A3's identity failing (an implementation error, recorded as such, fixed before evaluation).

## 9. Stages B and C, outline only, not pre-registered

**B, learning check.** The same task; values come from the learning module after a fixed reward training on one odour (30 consecutive reinforced steps, traces allowed to decay for 50 steps) with the other odour presented for the same 30 steps without reinforcement; a sham group gets both presentations and no reinforcement; the learned value of each odour is checked before the test (rewarded at least +0.5, neutral within +-0.1); learning frozen during the test; order and initial selection state fixed as in A. Its criteria are written at its own design time: A2 with the sham group in place of pathway-off transfers; A4 does NOT transfer as it stands, because a neutral presentation does not produce a negative value, so B needs its own statement about avoidance (a punished training, or none, decided then).

**C, integration check.** The gain connected in the H15 Run 2 world with learning on; the Run 2 measures for negative-valence avoidance and long-horizon search kept, with the Run 2 values as the reference. Nothing about C is claimed from A or B.

## 10. Predictions, on record

Bench: G* = 1 (0.5 possible). A1 passes. A2 passes at the bars above. A3 passes (exact). A4 passes. Diagnostic reading: most V rows have the valued odour as the first hold; the N rows in the bias arm are mostly navigation not delivering a valued first hold, not selection choosing neutral. T-revise: revision uncertain; I expect 'rare within this condition' more than the 0.50 reading, because release needs the other odour's response to exceed the held one's by 0.2 and the held odour's response is refreshed on every whiff. Most likely to surprise: the no-choice rate at 20 units downwind and the clip fraction at G = 2 if G* lands there.

## 11. What is needed to implement A

A subclass of ph14.Agent3 with the gain (one line in act, guarded by max(v, 0), applied before the release comparison and the circuit input), a per-step record of the held odour, of y' max and of the circuit state; a world class placing the two sources 10 apart with the midline start and the 2 x 2 assignment; the T-revise pre-hold routine; the bench script; self-checks: G = 0 reproduces Agent3 step for step; all-zero values reproduce G = 0 step for step; the pre-hold leaves exactly one odour held; every start is inside both cones; the two plumes' whiff rates at the start are equal in expectation; the flee target assertion of A4(a).
