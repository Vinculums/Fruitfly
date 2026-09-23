# Absent-odour check: report

Date 2026-09-23. Design v1 FINAL doc ddab34a689d056e2e (hash 3ec1b989...3d43; confirmed by the owner as written, decision:absent-odour-check-open). Code ph22.py sha256 03ab8c4706b19557af5d64edd83f812abba91b618439618b35837a49dd44ca1c (source doc d6a27b8b1f1b927ce, stored before the evaluation); it imports ph21.py unchanged (sha256 3a1d79d9...cfc1, the version H23 ran, checked at run time). One run, world seed 1775, agent seed 1875 (unused before; self-check True), 400 rows per world and arm, 600 steps, R5 400 rows x 1800 steps; output ph22_eval.txt sha256 bd2f6f563b8247178f3c9bc5ded8812e3367313857aae2a880a3ac22c886f842, appended in full below. Development run on 9890/9990 (output sha 7ec5ef67...17d9): no operation error. Nothing changed after the table. A check, not a hypothesis: descriptive readings with pre-fixed outcome labels on Agent8's reach, no PASS / FAIL, no fix tested.

## 1. Question

What does the adopted agent, Agent8 (ph21.py: ph19.Agent6 + the H23 value filter, G 2, the H21 gate on), do in a world that contains only an odour that is not top-valued in its read-out? By code (design section 1), with read-out +1 (A) / 0 (B) and only B's plume present, Agent8's navigation signal is False on every step: it never surges, and casts on the return-cast clock throughout. The check measures what casting alone does.

## 2. Construction and self-checks

- World: ph16.World7 unchanged, with the absent source's column set to False after World7 draws it (subclass `Masked` in ph22.py). Start: World7's own (midline, 20 downwind, heading drawn as World7; per-row initial cast side seed + 20000). Relative to the present source: 20 downwind, 5 crosswind, inside its cone.
- Worlds (A = World7 `good`): W1 only B present, read-out +1 / 0 (the cost case); W2 only A, +1 / 0 (control); W3 only B, 0 / 0 (identity); W4 only B, -1 / 0 (reported). Arms on the same seeds and draws: Agent8 (filter on) and ph19.Agent6 (filter off), G 2, gate on, learning off, values supplied.
- Self-checks, all True in demo, development and evaluation:
  - R0 (iv) masking consumes the random stream as World7 does: on every step of every run an unmasked World7 twin, placed at the masked world's position and heading, draws exactly the masked world's pre-mask whiffs and wind; the present column is unchanged and the absent column False; the world generator's state is equal at the end. In demo, against ph21.run itself (unmasked World7, Agent8 at +1/0, same seeds): positions, holds and whiffs are equal on every step before World7's first whiff of the absent source.
  - R0 (i) Agent8 in W1: nav 0 of 240 000 (row, step) at 600 steps and 0 of 720 000 at 1800.
  - R0 (ii) the absent odour is never sensed and never held in any run.
  - R0 (iii) bitwise (positions, headings, circuit states, holds, nav): Agent8 == Agent6 in W2, W3, W4; W4 == W3 for both agents; Agent6 in W1 == Agent6 in W3. The first 600 steps of the 1800-step runs equal the 600-step runs.
  - Seeds 9890/9990, 1775/1875 and derived 19890/29990, 11775/21875 appear in no other repository file (129 files at the evaluation).
- Implementation errors, fixed before any saved output: one, in a self-check. The demo's comparison against ph21.run first read World7's absent-odour whiffs from column 1 - `good` (the present odour in W1) instead of `good`. The assertion fired and the index was corrected to `good`; the construction itself was not changed. Cosmetic, left as run: the header's seed line prints the mode's seeds beside the derived numbers of both modes (the scan covers all eight). The file count was 130 at the development run and 129 at the evaluation because the development run's empty stderr capture was deleted in between.

## 3. Results per world and arm (600 steps, 400 rows each)

| world | arm | reach (within 3.0 at least once) | dwell q1 / median / q3 (mean) | lost rows (no whiff, last third) | wall contacts / row | nav (row, step) | holding present / nothing (fraction of row-steps) | holding present at 600 |
|---|---|---|---|---|---|---|---|---|
| W1 | Agent8 | 344 = 0.860 [0.823, 0.891] | 6 / 8 / 16 (12.36) | 38 | 0.000 | 0 | 0.791 / 0.209 | 374 |
| W1 | Agent6 | 395 = 0.988 [0.971, 0.995] | 19 / 25 / 29.2 (24.31) | 16 | 0.000 | 4242 | 0.747 / 0.253 | 386 |
| W2 | Agent8 | 394 = 0.985 [0.968, 0.993] | 20 / 25 / 30 (24.91) | 13 | 0.000 | 4251 | 0.908 / 0.092 | 398 |
| W2 | Agent6 | identical to W2 Agent8 (bitwise) | | | | | | |
| W3 | Agent8 | 395 = 0.988 [0.971, 0.995] | 19 / 25 / 29.2 (24.31) | 16 | 0.000 | 4242 | 0.747 / 0.253 | 386 |
| W3 | Agent6 | identical to W3 Agent8 (bitwise); equal to Agent6 in W1 | | | | | | |
| W4 | Agent8 | identical to W3 (bitwise) | | | | | | |
| W4 | Agent6 | identical to W3 (bitwise) | | | | | | |

W1 at 1800 steps (R5):

| arm | reach by 1800 | cumulative reach 600 / 1200 / 1800 | dwell per 600-step third, median (mean) | lost rows (last 600) | wall contacts / row (rows) | d_along at 1800 q1 / median / q3 | holding present / nothing |
|---|---|---|---|---|---|---|---|
| Agent8 | 381 = 0.953 [0.927, 0.969] | 344 / 367 / 381 | 8 (12.36), 9 (11.07), 8 (7.39) | 130 | 0.675 (111) | -65.3 / -63.4 / -61.4 | 0.912 / 0.088 |
| Agent6 | 400 = 1.000 [0.990, 1.000] | 395 / 399 / 400 | 25 (24.31), 24 (24.06), 24 (23.68) | 0 | 0.000 (0) | -26.4 / -19.4 / -9.2 | 0.911 / 0.089 |

(d_along is the downwind distance from the present source; negative is upwind of it.)

## 4. Readings (as registered; Wilson 95 percent)

- **R0 code identities:** (i) True, (ii) True, (iii) all six True, (iv) True (section 2).
- **R1 the cost, W1, 600 steps.** Agent8 reach 344/400 = 0.860 [0.823, 0.891]: lower bound 0.823 >= 0.80 -> **'reach kept'**. Agent6 reach 395/400 = 0.988 [0.971, 0.995]. Reported beside it: dwell median 8 against 25 (mean 12.36 against 24.31); paired, Agent8's dwell is below Agent6's in 330 rows, equal in 6 (both 0 in 5) and above in 64; first-reach step median 43 against 44; holding B at step 600, 374 against 386; lost rows 38 against 16; no wall contact in either.
- **R2 control, W2:** Agent8 == Agent6 bitwise (the filter is inert when the only odour present is top-valued); reach 394/400 = 0.985 [0.968, 0.993], dwell median 25.
- **R3 identity, W3:** Agent8 == Agent6 bitwise, and equal to Agent6 in W1; reach 395/400 = 0.988 [0.971, 0.995], dwell median 25.
- **R4 reported, W4:** Agent8 == Agent6 bitwise and equal to W3 for both.
- **R5 the horizon, W1, 1800 steps.** Agent8 reach by 1800 381/400 = 0.953 [0.927, 0.969]: lower bound >= 0.80 -> **'reach kept'**. Agent6 400/400 = 1.000 [0.990, 1.000]. Cumulative reach, dwell per third, d_along and wall contacts are in the table above. Every Agent8 row ends upwind of the source (400/400); Agent6 rows do in 361/400.

## 5. How the adopted agent behaves when the odour it values is absent (W1, measured)

- **It never surges.** Its movement command is the return cast on every step (nav 0; the cast clock equals the step count, maximum 600 and 1800). No whiff and no circuit state reaches the movement command.
- **It does reach the source, early, by casting past it.** 344 of 400 rows come within 3.0 by step 600 (Agent6 395). Most reaches happen in the first 200 steps: cumulative reach is 180 at step 100 and 338 at step 200, then 339 to 344 between steps 300 and 600, and 381 by step 1800 (additions near steps 900, 1100 and 1400). The first approach within 5.0 comes at step 27 / 35 / 45 (quartiles; 399 of 400 rows), about as early as Agent6's (27 / 30 / 110); the first within 3.0 at 30 / 43 / 111. Minimum distance to the source 1.1 / 1.7 / 2.3 (Agent6 0.4 / 0.8 / 1.3).
- **It does not stay.** Dwell within 3.0 over 600 steps: median 8 steps (quartiles 6 / 16) against Agent6's 25 (19 / 29.2); lower than Agent6's in 330 of 400 paired rows. Over 1800 steps the dwell per 600-step third stays at a median of 8 to 9 (Agent6 24 to 25), and its mean falls from 12.36 to 7.39.
- **It passes upwind of the source and keeps drifting upwind.** Every row goes upwind of the source within 600 steps (most-upwind d_along -21.4 / -19.9 / -17.8; start +20). At step 600 the agent is 17.3 upwind (median) and 7.7 crosswind; at 1800 it is 63.4 upwind (-65.3 / -63.4 / -61.4) and 12.8 crosswind, with its most-upwind point at -68.2 (median). The source is at least 68 units from every wall: by 1800, 111 of 400 rows have touched the upwind wall (0.675 contacts per row); none had by 600. Agent6 overshoots too (most-upwind -32.7 by 600), but it surges back on the plume and ends about 20 upwind (median -19.4 at 1800).
- **It enters the source's neighbourhood repeatedly without holding position there.** Entries into the 5.0 disc: mean 3.31 per row by 600 (Agent6 4.33) and 7.06 by 1800 (Agent6 12.61). It spends more steps inside the present cone than Agent6 (111.8 against 34.3 per row by 600) and senses more present-plume whiffs (13.22 against 10.61): the whiffs arrive, and nothing turns it upwind on them.
- **Meanwhile the circuit holds the odour it ignores.** It holds B on 0.791 of (row, step) by 600 (0.912 by 1800) and nothing on the rest; A is never held (never sensed). 397 B-holds form in 376 rows (first hold step median 33; 24 rows never hold by 600); 23 are released (6 on the timeout flag, 17 with neither flag); 374 of 400 rows hold B at step 600 and 394 at step 1800. The hold does not reach movement: with B held, B's value 0 is below the read-out maximum 1, so the filter blocks B's whiffs from navigation.
- **Lost rows.** No whiff of the present plume in the last third: 38 rows at 600 (Agent6 16) and 130 in the last 600 of 1800 steps (Agent6 0).
- Mechanism interpretation, labelled, not measured: the return cast starts at offset 0 (heading upwind) and widens at 1.2 degrees per step, so from a start 20 downwind and 5 crosswind of the source the first cast leg runs nearly upwind. That leg would carry the agent past the source around steps 30 to 45, which matches the measured first approach. On this reading the high reach is a property of this start and of the cast's first leg, not a search the agent performs; a start further off the source's axis, or a return after drifting away, was not tested. The design's arithmetic (an average upwind drift of +0.035 per step, reaching the source's coordinate near step 570) described the average over a full cast cycle, not the first leg; measured, the net upwind displacement is about 37 units at 600 and 83 at 1800.

## 6. The Agent6 reference against its prediction

Predicted: reach 0.94 to 1.00 and dwell median near 25 (design section 5, from the code identity with the known-answer law; the H23 known-answer arm reached the valued source in at least 387/400, with valued dwell median 25.0). Measured in W1: 395/400 = 0.988 [0.971, 0.995] and dwell median 25.0, inside the predicted range; bitwise equal to Agent6 and Agent8 in W3 and W4. W2 (the mirror, A present): 394/400 = 0.985, dwell median 25.

## 7. What the check does not establish

- It does not re-judge H23 or the adoption, and it tests no fix.
- Reach is the only statistic with an outcome label. 'Reach kept' says Agent8 comes within 3.0 of the present source at least once, not that it stays or dwells there. The cost measured here is in dwell (about a third of Agent6's), in position (upwind of the source, toward the wall, at long horizons) and in lost rows, and none of these carries a pre-fixed outcome.
- The reach depends on this start (on the source's axis within 5 crosswind, 20 downwind, heading as World7). Not tested: other starts, other geometries, other G, and a two-source world in which the top-valued plume exists but does not reach the agent (the same state for the agent).
- Values are supplied (+1 / 0). Not tested: two positive unequal values (+1 / +0.5) and learned values. Learning is off.
- The timeout, the circuit and the cast are unchanged; no statement is made about them.
- The mechanism reading in section 5 (the first cast leg carries the agent past the source) interprets measured timings; it is not a measurement of the mechanism.

## 8. Candidate fixes, restated from design section 6, not chosen

Each is costed against the owner's classification rule (H20 Stage A close; decision:h22-open-design (a), decision:h23-open-design: the agent uses only its own value read-out and hold state, no source or axis position, no privileged sensory history):

- (i) 'Top-valued among the odours sensed within the last N steps': adds a sensory-history term (which odours were smelled recently), which the rule as it stands excludes. It would also need a new N and its own test.
- (ii) 'Surge on any non-negative odour when no top-valued odour has been sensed for N steps': the same sensory-history term, and a new N.
- (iii) An absolute rule (surge on v >= 0) with the relative filter applied only when a top-valued whiff was sensed recently: the same term. By construction, whenever the window has expired it brings back the neutral-odour surges the filter removed in H23.
- (iv) Accept the cost and limit the adoption's scope to worlds where the top-valued odour is present: no change to the agent. The cost measured here (dwell median 8 against 25, the agent ending upwind of the source, 130 lost rows by 1800) then stands for any world or stretch of time in which the top-valued odour's plume does not reach the agent. With learned values (H20 Stage B, where ties are measure-zero) that is any time the single top-valued odour is not being sensed.

The filter's scope is the owner's decision.

## 9. Provenance

- Design v1 FINAL doc ddab34a689d056e2e (hash 3ec1b989...3d43; local experiments/absent_odour_check/absent_odour_check_design_v1.md); decision:absent-odour-check-open; decision:next-absent-odour-check-then-stage-b; decision:h23-filter-adopted-within-tested-conditions.
- Code ph22.py sha 03ab8c47...ca1c (source doc d6a27b8b1f1b927ce), importing ph21.py sha 3a1d79d9...cfc1 (doc ddcec8520fcd8e23c), ph19.Agent6 and ph16.World7 unchanged; no file in src/ edited.
- Demo output ph22_demo.txt sha 65706b01...b3e8; development output ph22_dev.txt sha 7ec5ef67...17d9 (9890/9990, no operation error).
- Evaluation: seeds 1775/1875; output ph22_eval.txt sha bd2f6f56...f842, below in full. Result record:absent-odour-check-result; episode:2026-09-23-absent-odour-check-run.

## Appendix: ph22_eval.txt in full (sha256 bd2f6f563b8247178f3c9bc5ded8812e3367313857aae2a880a3ac22c886f842)

== absent-odour check, EVAL. design v1 FINAL doc ddab34a689d056e2e hash 3ec1b989a776ced5289ab64689cbc59535de28c307f47cf038d43d863bef3d43; this file sha256 03ab8c4706b19557af5d64edd83f812abba91b618439618b35837a49dd44ca1c; ph21.py sha256 3a1d79d9a0d235f1bef7e435ec594cff4048180e27b28dcd892598c58413cfc1 (the version H23 ran: True); world seed 1775, agent seed 1875; 400 rows x 600 steps per world and arm, R5 W1 400 x 1800; G 2.0, gate on; the one evaluation ==
   seed self-check: (1775, 1875) and derived [19890, 29990, 11775, 21875] in no other file (129 scanned): True
   worlds: W1 present B, read-out A +1 / B 0; W2 present A, read-out A +1 / B 0; W3 present B, read-out A +0 / B 0; W4 present B, read-out A -1 / B 0 (A = World7 `good`)

   [W1 Agent8] 600 steps: reach (within 3.0 of the present source at least once) 344/400 = 0.860 [0.823, 0.891] -> reach kept; first-reach step quartiles 30/43/111
      dwell (steps within 3.0) q1/median/q3 6.0/8.0/16.0 mean 12.36; rows with no whiff of the present plume in the last third 38; no nav in the last third 400; wall contacts per row 0.000 (rows with any 0); nav (row, step) 0; cast clock max 600
      present-plume whiffs per row 13.22 (rows with any 399, first whiff step quartiles 4/12/76); steps in the present cone per row 111.8
      holds: fraction of (row, step) holding B/present 0.791, nothing 0.209; holds of the present odour formed 397 (rows 376), released 23 (timeout flag 6, evidence 0, both 0, neither 17); first hold step quartiles 18/33/121 (never 24); holding the present odour at step 600 374/400
      trajectory: most-upwind d_along (start 20) q1/median/q3 -21.4/-19.9/-17.8, rows passing upwind of the source (d_along < 0) 400; final d_along -19.4/-17.3/-15.1, final |crosswind| 2.7/7.7/12.9; minimum distance 1.1/1.7/2.3; first step within 5.0 27/35/45 (rows 399), within 3.0 30/43/111 (rows 344); entries into 5.0 per row mean 3.31 (0: 1, 1: 70, 2: 70, 3+: 259)
      cumulative reach at 100-step checkpoints: 100:180 200:338 300:339 400:340 500:340 600:344

   [W1 Agent6] 600 steps: reach (within 3.0 of the present source at least once) 395/400 = 0.988 [0.971, 0.995]; first-reach step quartiles 31/44/116
      dwell (steps within 3.0) q1/median/q3 19.0/25.0/29.2 mean 24.31; rows with no whiff of the present plume in the last third 16; no nav in the last third 16; wall contacts per row 0.000 (rows with any 0); nav (row, step) 4242; cast clock max 600
      present-plume whiffs per row 10.61 (rows with any 399, first whiff step quartiles 4/12/76); steps in the present cone per row 34.3
      holds: fraction of (row, step) holding B/present 0.747, nothing 0.253; holds of the present odour formed 422 (rows 388), released 36 (timeout flag 10, evidence 0, both 0, neither 26); first hold step quartiles 19/38/138 (never 12); holding the present odour at step 600 386/400
      trajectory: most-upwind d_along (start 20) q1/median/q3 -33.3/-32.7/-32.1, rows passing upwind of the source (d_along < 0) 400; final d_along -25.3/-13.9/-4.8, final |crosswind| 1.3/2.8/5.3; minimum distance 0.4/0.8/1.3; first step within 5.0 27/30/110 (rows 400), within 3.0 31/44/116 (rows 395); entries into 5.0 per row mean 4.33 (0: 0, 1: 2, 2: 6, 3+: 392)
      cumulative reach at 100-step checkpoints: 100:199 200:379 300:388 400:391 500:395 600:395

   [W2 Agent8] 600 steps: reach (within 3.0 of the present source at least once) 394/400 = 0.985 [0.968, 0.993]; first-reach step quartiles 31/48/115
      dwell (steps within 3.0) q1/median/q3 20.0/25.0/30.0 mean 24.91; rows with no whiff of the present plume in the last third 13; no nav in the last third 13; wall contacts per row 0.000 (rows with any 0); nav (row, step) 4251; cast clock max 600
      present-plume whiffs per row 10.63 (rows with any 398, first whiff step quartiles 4/14/112); steps in the present cone per row 35.0
      holds: fraction of (row, step) holding B/present 0.908, nothing 0.092; holds of the present odour formed 398 (rows 398), released 0 (timeout flag 0, evidence 0, both 0, neither 0); first hold step quartiles 6/16/114 (never 2); holding the present odour at step 600 398/400
      trajectory: most-upwind d_along (start 20) q1/median/q3 -33.4/-32.9/-32.3, rows passing upwind of the source (d_along < 0) 400; final d_along -25.8/-13.7/-4.2, final |crosswind| 1.4/2.8/5.2; minimum distance 0.4/0.8/1.3; first step within 5.0 27/36/108 (rows 399), within 3.0 31/48/115 (rows 394); entries into 5.0 per row mean 4.37 (0: 1, 1: 3, 2: 8, 3+: 388)
      cumulative reach at 100-step checkpoints: 100:198 200:380 300:387 400:388 500:391 600:394

   [W2 Agent6] 600 steps: reach (within 3.0 of the present source at least once) 394/400 = 0.985 [0.968, 0.993]; first-reach step quartiles 31/48/115
      dwell (steps within 3.0) q1/median/q3 20.0/25.0/30.0 mean 24.91; rows with no whiff of the present plume in the last third 13; no nav in the last third 13; wall contacts per row 0.000 (rows with any 0); nav (row, step) 4251; cast clock max 600
      present-plume whiffs per row 10.63 (rows with any 398, first whiff step quartiles 4/14/112); steps in the present cone per row 35.0
      holds: fraction of (row, step) holding B/present 0.908, nothing 0.092; holds of the present odour formed 398 (rows 398), released 0 (timeout flag 0, evidence 0, both 0, neither 0); first hold step quartiles 6/16/114 (never 2); holding the present odour at step 600 398/400
      trajectory: most-upwind d_along (start 20) q1/median/q3 -33.4/-32.9/-32.3, rows passing upwind of the source (d_along < 0) 400; final d_along -25.8/-13.7/-4.2, final |crosswind| 1.4/2.8/5.2; minimum distance 0.4/0.8/1.3; first step within 5.0 27/36/108 (rows 399), within 3.0 31/48/115 (rows 394); entries into 5.0 per row mean 4.37 (0: 1, 1: 3, 2: 8, 3+: 388)
      cumulative reach at 100-step checkpoints: 100:198 200:380 300:387 400:388 500:391 600:394

   [W3 Agent8] 600 steps: reach (within 3.0 of the present source at least once) 395/400 = 0.988 [0.971, 0.995]; first-reach step quartiles 31/44/116
      dwell (steps within 3.0) q1/median/q3 19.0/25.0/29.2 mean 24.31; rows with no whiff of the present plume in the last third 16; no nav in the last third 16; wall contacts per row 0.000 (rows with any 0); nav (row, step) 4242; cast clock max 600
      present-plume whiffs per row 10.61 (rows with any 399, first whiff step quartiles 4/12/76); steps in the present cone per row 34.3
      holds: fraction of (row, step) holding B/present 0.747, nothing 0.253; holds of the present odour formed 422 (rows 388), released 36 (timeout flag 10, evidence 0, both 0, neither 26); first hold step quartiles 19/38/138 (never 12); holding the present odour at step 600 386/400
      trajectory: most-upwind d_along (start 20) q1/median/q3 -33.3/-32.7/-32.1, rows passing upwind of the source (d_along < 0) 400; final d_along -25.3/-13.9/-4.8, final |crosswind| 1.3/2.8/5.3; minimum distance 0.4/0.8/1.3; first step within 5.0 27/30/110 (rows 400), within 3.0 31/44/116 (rows 395); entries into 5.0 per row mean 4.33 (0: 0, 1: 2, 2: 6, 3+: 392)
      cumulative reach at 100-step checkpoints: 100:199 200:379 300:388 400:391 500:395 600:395

   [W3 Agent6] 600 steps: reach (within 3.0 of the present source at least once) 395/400 = 0.988 [0.971, 0.995]; first-reach step quartiles 31/44/116
      dwell (steps within 3.0) q1/median/q3 19.0/25.0/29.2 mean 24.31; rows with no whiff of the present plume in the last third 16; no nav in the last third 16; wall contacts per row 0.000 (rows with any 0); nav (row, step) 4242; cast clock max 600
      present-plume whiffs per row 10.61 (rows with any 399, first whiff step quartiles 4/12/76); steps in the present cone per row 34.3
      holds: fraction of (row, step) holding B/present 0.747, nothing 0.253; holds of the present odour formed 422 (rows 388), released 36 (timeout flag 10, evidence 0, both 0, neither 26); first hold step quartiles 19/38/138 (never 12); holding the present odour at step 600 386/400
      trajectory: most-upwind d_along (start 20) q1/median/q3 -33.3/-32.7/-32.1, rows passing upwind of the source (d_along < 0) 400; final d_along -25.3/-13.9/-4.8, final |crosswind| 1.3/2.8/5.3; minimum distance 0.4/0.8/1.3; first step within 5.0 27/30/110 (rows 400), within 3.0 31/44/116 (rows 395); entries into 5.0 per row mean 4.33 (0: 0, 1: 2, 2: 6, 3+: 392)
      cumulative reach at 100-step checkpoints: 100:199 200:379 300:388 400:391 500:395 600:395

   [W4 Agent8] 600 steps: reach (within 3.0 of the present source at least once) 395/400 = 0.988 [0.971, 0.995]; first-reach step quartiles 31/44/116
      dwell (steps within 3.0) q1/median/q3 19.0/25.0/29.2 mean 24.31; rows with no whiff of the present plume in the last third 16; no nav in the last third 16; wall contacts per row 0.000 (rows with any 0); nav (row, step) 4242; cast clock max 600
      present-plume whiffs per row 10.61 (rows with any 399, first whiff step quartiles 4/12/76); steps in the present cone per row 34.3
      holds: fraction of (row, step) holding B/present 0.747, nothing 0.253; holds of the present odour formed 422 (rows 388), released 36 (timeout flag 10, evidence 0, both 0, neither 26); first hold step quartiles 19/38/138 (never 12); holding the present odour at step 600 386/400
      trajectory: most-upwind d_along (start 20) q1/median/q3 -33.3/-32.7/-32.1, rows passing upwind of the source (d_along < 0) 400; final d_along -25.3/-13.9/-4.8, final |crosswind| 1.3/2.8/5.3; minimum distance 0.4/0.8/1.3; first step within 5.0 27/30/110 (rows 400), within 3.0 31/44/116 (rows 395); entries into 5.0 per row mean 4.33 (0: 0, 1: 2, 2: 6, 3+: 392)
      cumulative reach at 100-step checkpoints: 100:199 200:379 300:388 400:391 500:395 600:395

   [W4 Agent6] 600 steps: reach (within 3.0 of the present source at least once) 395/400 = 0.988 [0.971, 0.995]; first-reach step quartiles 31/44/116
      dwell (steps within 3.0) q1/median/q3 19.0/25.0/29.2 mean 24.31; rows with no whiff of the present plume in the last third 16; no nav in the last third 16; wall contacts per row 0.000 (rows with any 0); nav (row, step) 4242; cast clock max 600
      present-plume whiffs per row 10.61 (rows with any 399, first whiff step quartiles 4/12/76); steps in the present cone per row 34.3
      holds: fraction of (row, step) holding B/present 0.747, nothing 0.253; holds of the present odour formed 422 (rows 388), released 36 (timeout flag 10, evidence 0, both 0, neither 26); first hold step quartiles 19/38/138 (never 12); holding the present odour at step 600 386/400
      trajectory: most-upwind d_along (start 20) q1/median/q3 -33.3/-32.7/-32.1, rows passing upwind of the source (d_along < 0) 400; final d_along -25.3/-13.9/-4.8, final |crosswind| 1.3/2.8/5.3; minimum distance 0.4/0.8/1.3; first step within 5.0 27/30/110 (rows 400), within 3.0 31/44/116 (rows 395); entries into 5.0 per row mean 4.33 (0: 0, 1: 2, 2: 6, 3+: 392)
      cumulative reach at 100-step checkpoints: 100:199 200:379 300:388 400:391 500:395 600:395

== readings (design v1 FINAL section 5; Wilson 95 percent; no PASS / FAIL) ==
   R0 (i) Agent8 in W1, nav (row, step): 0 -> True; (ii) absent odour never sensed, never held, all 8 runs: True; (iii) {'W2 Agent8 == Agent6': True, 'W3 Agent8 == Agent6': True, 'W4 Agent8 == Agent6': True, 'W4 == W3 Agent8': True, 'W4 == W3 Agent6': True, 'Agent6 W1 == W3': True}; (iv) masked draws == World7's on every step, generator state equal, all 8 runs: True
   R1 W1 600 steps: Agent8 reach 344/400 = 0.860 [0.823, 0.891] -> REACH KEPT; Agent6 reach 395/400 = 0.988 [0.971, 0.995] (predicted 0.94 to 1.00)
      dwell median Agent8 8.0 / Agent6 25.0, mean 12.36 / 24.31; paired rows Agent8 below 330, equal 6 (both 0: 5), above 64; first-reach median 43 / 44; B held at step 600 374 / 386; lost rows 38 / 16; wall contacts per row 0.000 / 0.000
   R2 control, W2: Agent8 == Agent6 True; reach 394/400 = 0.985 [0.968, 0.993], dwell median 25.0
   R3 identity, W3: Agent8 == Agent6 True; == Agent6 W1 True; reach 395/400 = 0.988 [0.971, 0.995], dwell median 25.0
   R4 reported, W4: Agent8 == Agent6 True; W4 == W3 Agent8 True, Agent6 True; reach 395/400 = 0.988 [0.971, 0.995], dwell median 25.0

== R5 the horizon: W1, 1800 steps, both arms ==
   implementation check: the first 600 steps of the 1800-step runs equal the 600-step runs bitwise: {'Agent8': True, 'Agent6': True}; Agent8 nav (row, step) 0; absent odour never sensed or held True; masked draws == World7's True

   [W1 Agent8] 1800 steps: reach (within 3.0 of the present source at least once) 381/400 = 0.953 [0.927, 0.969] -> reach kept; first-reach step quartiles 30/108/112
      dwell (steps within 3.0) q1/median/q3 15.0/26.0/42.2 mean 30.82; rows with no whiff of the present plume in the last third 130; no nav in the last third 400; wall contacts per row 0.675 (rows with any 111); nav (row, step) 0; cast clock max 1800
      present-plume whiffs per row 26.84 (rows with any 400, first whiff step quartiles 4/12/108); steps in the present cone per row 193.2
      holds: fraction of (row, step) holding B/present 0.912, nothing 0.088; holds of the present odour formed 418 (rows 395), released 24 (timeout flag 6, evidence 0, both 0, neither 18); first hold step quartiles 18/34/121 (never 5); holding the present odour at step 1800 394/400
      trajectory: most-upwind d_along (start 20) q1/median/q3 -69.8/-68.2/-65.6, rows passing upwind of the source (d_along < 0) 400; final d_along -65.3/-63.4/-61.4, final |crosswind| 6.6/12.8/17.7; minimum distance 0.3/0.8/1.4; first step within 5.0 27/36/45 (rows 400), within 3.0 30/108/112 (rows 381); entries into 5.0 per row mean 7.06 (0: 0, 1: 4, 2: 23, 3+: 373)
      cumulative reach at 100-step checkpoints: 100:180 200:338 300:339 400:340 500:340 600:344 700:344 800:345 900:349 1000:349 1100:364 1200:367 1300:367 1400:379 1500:379 1600:379 1700:381 1800:381

   [W1 Agent6] 1800 steps: reach (within 3.0 of the present source at least once) 400/400 = 1.000 [0.990, 1.000]; first-reach step quartiles 31/108/117
      dwell (steps within 3.0) q1/median/q3 63.0/72.0/80.0 mean 72.05; rows with no whiff of the present plume in the last third 0; no nav in the last third 0; wall contacts per row 0.000 (rows with any 0); nav (row, step) 12106; cast clock max 1047
      present-plume whiffs per row 30.27 (rows with any 400, first whiff step quartiles 4/12/108); steps in the present cone per row 87.6
      holds: fraction of (row, step) holding B/present 0.911, nothing 0.089; holds of the present odour formed 437 (rows 400), released 37 (timeout flag 11, evidence 0, both 0, neither 26); first hold step quartiles 20/38/193 (never 0); holding the present odour at step 1800 400/400
      trajectory: most-upwind d_along (start 20) q1/median/q3 -34.1/-33.6/-33.2, rows passing upwind of the source (d_along < 0) 400; final d_along -26.4/-19.4/-9.2, final |crosswind| 1.5/3.1/5.6; minimum distance 0.2/0.3/0.5; first step within 5.0 27/30/110 (rows 400), within 3.0 31/108/117 (rows 400); entries into 5.0 per row mean 12.61 (0: 0, 1: 0, 2: 0, 3+: 400)
      cumulative reach at 100-step checkpoints: 100:199 200:379 300:388 400:391 500:395 600:395 700:397 800:397 900:398 1000:399 1100:399 1200:399 1300:400 1400:400 1500:400 1600:400 1700:400 1800:400
   R5 Agent8: reach by 1800 381/400 = 0.953 [0.927, 0.969] -> REACH KEPT; cumulative reach at 600/1200/1800 344/367/381; dwell per third (median; mean) 8.0; 12.36, 9.0; 11.07, 8.0; 7.39; d_along at 1800 q1/median/q3 -65.3/-63.4/-61.4, rows upwind of the source at 1800 400; wall contacts per row 0.675
   R5 Agent6: reach by 1800 400/400 = 1.000 [0.990, 1.000]; cumulative reach at 600/1200/1800 395/399/400; dwell per third (median; mean) 25.0; 24.31, 24.0; 24.06, 24.0; 23.68; d_along at 1800 q1/median/q3 -26.4/-19.4/-9.2, rows upwind of the source at 1800 361; wall contacts per row 0.000

== end of table; nothing changes after it ==
