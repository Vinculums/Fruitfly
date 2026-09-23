# H20 Run 2 design v1: the supplied-value choice test with a measure calibrated by fixed-identity arms

Date 2026-09-21. Status: **DRAFT for the owner's confirmation. No code.** Follows decision:h20-run2-design-first (option (a)). A NEW pre-registration with its own criteria, seeds and record. Stage A's verdict (NOT shown under its registered criteria, decision:h20-stage-a-closed) stands and is not re-judged. Supplied value only; no learning; no navigation change; no crosswind term; Stages B and C not entered.

## 1. Hypothesis (unchanged from Stage A)

**H20: given the opportunity to approach both, the agent chooses the odour that carries a positive value over an odour that carries none.**

## 2. What changes from Stage A, and the measured reason for each change

The link check (report df9cf42bb99c43d39) fixed the tracked odour by intervention and measured what the adopted navigation can express in the H20 world:

| measure | with the identity fixed, C0 | C1 | C2 |
|---|---|---|---|
| first source reached = the tracked source (each arm) | 0.060 (same source in both arms 0.932) | 0.087 | 0.743 |
| the source the agent stays at more over 600 steps = the tracked source | 0.950 / 0.968 | 0.948 / 0.963 | 0.973 / 0.968 |

- **Main measure changed:** from 'the first source reached' to **'the source the agent stays at more over the trial'** (dwell majority). In the H20 geometry a perfect selection reaches its source first in about half the rows, so no selection mechanism could have met a first-reach bar there; the dwell majority expresses a fixed identity in 95 to 97 percent of rows in every geometry tested. The first reach is kept as a reported secondary measure with its own known-answer ceiling.
- **Geometry kept:** C0 (sources 10 apart, midline start 20 downwind), the Stage A task and the bench's start rate 0.057. The dwell majority is expressed there (0.950 / 0.968); changing the geometry is not needed for the measure and would cut the continuity with the bench and Stage A. C1 and C2 are not run.
- **Known-answer arm added:** the tracked identity fixed to the VALUED odour by intervention (the link check's method, per row), with G 0. It is the ceiling of the measure in this run: what the task can show when selection is perfect. Pathway-off remains the floor (value present, no pathway). Both are validity clauses (floor, ceiling, and the measure discriminating between them), as the standing rules require.
- **G = 2, pre-registered here** (carried from decision:h20-stage-a-run-g2 with its reason: the bench's highest first-hold accuracy at the task's start rate and highest biased end state; the bench's own rule found no candidate and that verdict is unchanged). G is fixed before this run and not adjusted after.
- **Initial cast side drawn per row** (decision:h20-amendment-initial-cast-side) is part of the task from the start.
- **T-revise dropped:** answered in Stage A (revision in 238/400, 'meets the bar that at least half revise'); not needed for the choice question. It can be kept as a reported arm if the owner wants it.
- **Aggregation rule stated for every multi-part criterion** (the Stage A report needed a correction on this): a criterion is PASS if every part passes, FAIL if any part fails, INCONCLUSIVE otherwise; R1's failure makes the run UNREADABLE.

## 3. The task

World and balance as Stage A: two sources 10 apart crosswind at one downwind coordinate in the 160x160 arena, start on the midline 20 downwind (inside both cones, whiff p 0.057 per plume), heading uniform, initial cast side drawn per row (agent seed + 20000, identical across arms), 2 x 2 balance over which odour carries the value and which side it sits on, 100 rows per cell, 400 rows, 600 steps, no relocation. Values supplied as +1 / 0 / -1 per odour; the learning module is not called.

**Main measure, fixed.** dwell_k = steps within 3.0 of source k over the 600 steps. Choice = the source with the larger dwell. Tie (equal dwell, including 0 = 0) = no choice. Every row is exactly one of V (valued source majority), N (neutral majority), 0 (tie). All three counts printed per arm and per cell. No row dropped.

**Secondary measures, reported:** the first source reached (V / N / 0 as in Stage A); first hold (odour, step); hold changes; the odour held at the first reach; the Stage A segment table; agreement between the majority source and the first hold; dwell values; no whiff in the last third; wall contacts; the input-range and saturation records of Stage A's section 2 (y' max, fraction y' > 1.8, clip fraction, flagged above 1 percent).

## 4. Arms (values supplied, learning off)

| arm | values valued / other | G | selection | role |
|---|---|---|---|---|
| bias | +1 / 0 | 2 | the adopted circuit | main: does the supplied value decide which source the agent stays at |
| neutral | 0 / 0 | 2 | the adopted circuit | side balance and chance (identical to G 0 by R3) |
| pathway-off | +1 / 0 | 0 | the adopted circuit | floor: the value is present, no pathway |
| known-answer | +1 / 0 | 0 | the held odour fixed to the valued odour on every step (intervention, per row) | ceiling: the measure with a perfect selection |
| priority | +1 / -1 | 2 | the adopted circuit | avoidance priority with the gain on |
| priority-off | +1 / -1 | 0 | the adopted circuit | reference for R4 |

All arms share the world seed, agent seed, row index and cast draw. The known-answer arm's intervention is the link check's: the selection block is not run and `h` is the row's valued odour; nothing else changes; no information about source positions is given.

## 5. Criteria

Statistics as Stage A: one fixed statistic per criterion; Wilson intervals for proportions; percentile bootstrap over rows for paired differences (5000 resamples, seed 20260924, matched rows resampled together); 95 percent; one evaluation, no extension; a group under 50 rows unreadable; the unrounded bound decides. Denominators: R2 and R4(c) use every assigned row; R1's symmetry clauses use rows that chose (the tie rate is capped separately). Aggregation: PASS if every part passes, FAIL if any part fails, INCONCLUSIVE otherwise.

- **R1 task validity (else the run is UNREADABLE).**
  (a) Ties at most 20 percent of rows in neutral, pathway-off and known-answer (observed).
  (b) Side balance: neutral P(+y source majority | chose) interval within [0.35, 0.65].
  (c) Floor: pathway-off P(V | chose) interval within [0.35, 0.65].
  (d) Ceiling: known-answer P(V) over all 400 rows, lower bound >= 0.85 (the link check gave 0.950 and 0.968 in C0 for the two fixed identities).
- **R2 main (bias arm).**
  (a) P(V) over all 400 rows: lower bound >= 0.70 (check example: at least 298 of 400).
  (b) Per cell P(V) over 100 rows: lower bound >= 0.55 in each cell (at least 65 of 100).
  (c) DP = P(V) bias minus pathway-off over the same rows: bootstrap lower bound >= +0.20.
  Reported beside it, no bar: P(V) bias as a fraction of P(V) known-answer (how much of the ceiling the pathway reaches); N and 0 counts; the first-reach secondary (V / N / 0) for bias, pathway-off and known-answer, with the known-answer arm's first-reach rate as that measure's ceiling.
- **R3 identity (implementation checks, printed in the run).** Neutral at G 2 and at G 0 bitwise identical (positions, headings, circuit states); G 0 reproduces ph14.Agent3; in the known-answer arm `h` equals the row's valued odour on every step and the hit equals that channel's whiffs.
- **R4 priority.** (a) Code path: the constructed-state self-check of Stage A (negative odour held, valued presented, G 2: flee target on every negative-held step, equal to G 0's); in the run, violations 0 over the negative-held (row, step) exposure printed for both priority arms, with 'no violation, no opportunity to verify operation' if the exposure is 0 (then (a) rests on the self-check). (b) Dwell at the negative source, priority minus priority-off, paired mean difference upper bound <= +1.0 step; reported: rows ever within 3.0 of it, first entry to exit beyond 6.0. (c) P(V) over all rows in the priority arm, lower bound >= 0.70. Reported, no bar: DP priority minus priority-off.

**Run 2 verdict:** the pathway carries a supplied positive value into the choice of source, measured as the source the agent stays at, if R1, R2, R3 and R4 all PASS. A statement about a supplied value in this task and this measure; not about learning; not about the first source reached.

## 6. Unreadable conditions

R1 failing (any part); ties above 20 percent in an arm under test; a cell under 50 rows; R3 failing (an implementation error, recorded as such and fixed before the evaluation).

## 7. Seeds, sizes, order

400 rows per arm, six arms, plus the R3 rerun. Development seeds world 9840, agent 9940; evaluation seeds world 1695, agent 1795 (checked unused). Order: minimal implementation (ph16's world, agent and criteria code; ph17's intervention with a per-row fixed odour) -> self-checks -> development run for operation errors -> one evaluation -> report. Any change before the evaluation is recorded as an amendment or an implementation error; nothing changes after the table.

## 8. Predictions, on record

R1 passes (ties are rare: 0.0 to 0.2 percent in the link check; the ceiling is at 0.95 to 0.97). R2: the bias arm's P(V) between 0.70 and 0.80 (Stage A: the first hold followed the value in 277 of 400 rows and the evidence release revised held neutral selections in 238 of 400; the bench's end state at G 2 was 67.5 percent biased over all rows); DP against pathway-off +0.20 to +0.30; pathway-off near 0.5. This is the most uncertain prediction: whether selection converts into the majority source often enough for the 0.70 bound. R4 passes; the first-reach secondary stays near chance in the bias arm, as in Stage A, with the known-answer first-reach rate near 0.5 to 0.55.

## 9. What this run does not test

Learning (B), the integrated environment (C), any G other than 2, any geometry other than C0, the first source reached as a main measure, and any navigation change.
