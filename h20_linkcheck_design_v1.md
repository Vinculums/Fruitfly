# Selection-to-navigation link check, design v1

Date 2026-09-20. Status: **DRAFT for the owner's confirmation. No code.** Follows decision:h20-stage-a-closed. A diagnostic check, not a hypothesis: it asks whether, in the adopted agent, the identity of the tracked odour controls movement at all. Value and learning are excluded. Nothing in the agent is changed; the two intervention conditions replace one internal signal by a constant.

## 1. Question

In the H20 task world, does the identity of the odour the agent tracks control where it goes? H20 Stage A found that the value gain changed which odour was selected first (277 against 200 of 400) while the first source reached was the same row for row with and without the gain. That mismatch is measured; its location in the chain from selection to movement is not. This check fixes the tracked odour by intervention and asks whether the movement then differs.

## 2. Conditions (arms), everything else identical

Same world seed, agent seed, per-row initial cast side (the H20 amendment), and sensory-input generation rule (World7 with its geometry parameters). Values are all zero and G = 0, so the agent is ph14.Agent3 exactly (checked bitwise in the self-checks).

| arm | what decides the tracked odour | nature |
|---|---|---|
| track-A | the held odour is odour A (channel 0) on every step, by intervention | diagnostic intervention |
| track-B | the held odour is odour B (channel 1) on every step, by intervention | diagnostic intervention |
| circuit | the adopted Select-and-Hold circuit, as in H20 (H19 (a) on) | the adopted agent |

The intervention replaces the circuit's output: the selection block is not run and `h` is the constant; the rest of act is unchanged, so the only odour-specific signal that reaches navigation is, as in the adopted agent, a whiff of the held odour (`hit`), which resets the cast clock and sets the target to upwind. The untracked odour's whiffs are ignored, exactly as whiffs of the other odour are ignored while one is held. **No information is added**: no source position, no axis, no direction. The fixed arms do not evaluate the circuit; they show what navigation can express when the tracked identity is given.

Because the 2 x 2 world places odour A at +y in half the rows and at -y in the other half, tracking by identity is balanced over side.

## 3. Geometries, pre-defined, all run, none chosen afterwards

All starts are on the midline inside BOTH cones (the agent must be able to sense both odours; a start outside the cones adds a search problem and is not this check). W0 1.5, SLOPE 0.25, LAM 12, LMAX 25 as everywhere.

| condition | separation s | start d downwind | whiff p per plume at the start | cone overlap width at the start | cones separate below (downwind) | distance to each source |
|---|---|---|---|---|---|---|
| C0 (reference, the H20 task) | 10 | 20 | 0.057 | 3.0 | 14 | 20.6 |
| C1 (less overlap at the start) | 10 | 16 | 0.079 | 1.0 | 14 | 16.8 |
| C2 (longer separated stretch) | 14 | 28 | 0.029 | 3.0 | 22 | 29.0 |

Overlap width = 2*(W0 + SLOPE*d) - s. C1 keeps the sources and shortens the overlapping stretch to 2 units of upwind travel; C2 keeps the overlap width and lengthens the separated stretch to 22 units. C0 is the reference; C1 and C2 are reported beside it; no condition is selected after the results, and no other condition is added afterwards.

## 4. Records, per row and per step, in the fixed arms

Whiffs on each channel; the hit handed to navigation (`nav_hit`); the cast clock (`since`); the movement target (`tgt`); the turn; position; heading. Derived per row: first source reached (which, and when); dwell at each source over 600 steps; steps spent inside each cone; the first step at which the target differs between track-A and track-B; the first step at which the position differs; the first step with a whiff on one channel only; the crosswind offset from the midline, signed toward the tracked source's side, at the first step the agent's downwind distance drops below the separation point (14 for s 10, 22 for s 14). In the circuit arm: the same, plus the hold sequence as in H20.

## 5. Readings, fixed before the run (diagnostic readings, not a hypothesis verdict)

Wilson 95 percent intervals; one run on the evaluation seeds after a development run for operation; a group under 50 rows is unreadable; ties above 20 percent make a statistic unreadable. Each reading has three outcomes.

- **L1 first reach.** Over rows where both fixed arms reached a source within 600 steps: P(each arm reached its tracked odour's source first) and P(the same source in both arms). 'Expressed in the first reach' if the first has lower bound >= 0.70; 'not expressed in the first reach' if the second has lower bound >= 0.70; otherwise 'partial', with counts. No-choice counts printed per arm.
- **L2 dwell over 600 steps.** Per fixed arm, over all rows: P(dwell at the tracked source > dwell at the other), ties (equal dwell, including 0 = 0) counted. 'Expressed in dwell' if lower bound >= 0.70; 'not expressed' if the interval lies within [0.40, 0.60]; otherwise 'partial'.
- **L3 divergence, reported.** Median first step at which the target differs between track-A and track-B; median first step at which the position differs; the fraction of rows that diverge before the first reach; the fraction in which the target first differs at the first single-channel whiff. These say where along the chain the tracked identity first changes anything.
- **L4 crosswind expression at separation, reported with the three-way reading.** Per fixed arm: P(the signed crosswind offset toward the tracked source is positive at the step the cones separate), over rows that reach that step before reaching a source. Same bars as L2.
- **L5 reference.** Circuit arm: first hold, first reach, their agreement, and P(first reach = the first hold's source), for comparison with the H20 evaluation.

The readings are taken per geometry. The design says nothing about combining them across geometries; each is a separate description.

## 6. What this check does not do

No value pathway, no learning, no crosswind term, no information about source positions, no new navigation rule, no change to the agent or the world classes beyond the intervention on `h`. It does not test the circuit and does not give a verdict on H20. A future navigation term, if any, is a separate design in which it is first classified as an estimate from sensory history or as a diagnostic ground-truth direction.

## 7. Seeds, sizes, self-checks

400 rows per arm per geometry (3 x 3 = 9 runs of 400 x 600). Development seeds world 9830, agent 9930; evaluation seeds world 1690, agent 1790 (checked unused). Self-checks: the circuit arm with G 0 and zero values reproduces ph14.Agent3 bitwise; in a fixed arm `h` equals the constant on every step and the hit equals that channel's whiffs; the two fixed arms have identical positions up to the first step at which their targets differ; the geometry table's numbers (start inside both cones, whiff p, overlap width, separation point, distance) are asserted per condition; the per-row cast draw is identical across arms.

## 8. Predictions, on record

C0: L1 'not expressed' or 'partial' (H20's row-for-row identity of the reach suggests the first reach is set by the cast phase within the overlap); L2 'expressed' more likely than not (after a wrong first reach the untracked odour's whiffs give no hits, the cast continues, and the tracked source can still be found within 600 steps); L3 divergence at the first single-channel whiff in most rows, before the first reach. C1: L1 shifts toward 'partial' or 'expressed' because the separated stretch starts sooner. C2: uncertain; the longer separated stretch helps, the lower whiff rate (0.029) hurts. I do not predict L4.
