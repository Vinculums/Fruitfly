# H23 report: value-filtered navigation in the H21 choice task

Date 2026-09-23. Design v2 FINAL doc db6df2e0013ab96e7 (confirmed by the owner, decision:h23-open; hash c19751f4...0087, equal to the local file's sha256). Code ph21.py sha256 3a1d79d9a0d235f1bef7e435ec594cff4048180e27b28dcd892598c58413cfc1 (source doc ddcec8520fcd8e23c, stored before the development run). One evaluation, world seed 1765, agent seed 1865, 400 rows x 600 steps, G 2, gate on where G 2, geometry C0, 95 percent intervals, no extension. Evaluation output ph21_eval.txt sha256 b7b35099a43e7993bf93c7f1c18ff7e8d40d1f7a42783d63ee6abbef86cec6d0. Nothing was changed after the table.

**Status: PASS under the registered criteria: M1, M2, M3, M4, M5, M6 all PASS.** The printout's summary label is the registered verdict sentence. Bench (b), reported beside the verdict and not part of it (design v2 section 4, owner's point 1): PASS. The pass was the expected outcome: the design put its joint pass probability at about 0.89 at the prediction's lower edge, because at +1/0 the filter arm's navigation law is the known-answer arm's by code (section 3 of the design; checked by M3 iii and bench a5). **The pass is a statement about value-driven navigation in the full agent, not about selection controlling navigation: the task does not show selection controlling navigation (at +1/0 it does not, by construction).** A statement about a supplied value, this rule, values +1/0, C0, the dwell-majority measure and the full agent with its circuit running; not about learning, other values, other G, other geometries, or a world in which the higher-valued odour is absent. Closure is the owner's.

## 1. What was asked

H23: the agent's upwind surge follows the highest-valued non-negative odour in its own value read-out. While it holds that odour, the held odour's whiffs drive the surge; otherwise (nothing held, or a lower-valued non-negative odour held) only whiffs of a top-valued non-negative odour drive it. With this rule, in the H21 task, the source the agent stays at follows the value in more rows than with the H21 maintain agent, near the known-answer ceiling, without adding lost rows. Two statements judged separately: (i) implementation, on constructed states (M4: identities a1, a2, a3, a5; bars a4 and c); (ii) task (M1, M2, M3, M5, M6). Registered as a reported property, not a gate: whether the hold comes to agree with navigation from the task-like neutral-hold start (bench b). Arms: filter (Agent8, rule on), maintain (the H21 maintain agent, Agent6), pathway-off (floor), known-answer (ceiling; the navigation law the filter arm shares), neutral (0/0, identity), priority-identity (+1/-1, identity). Bars: M2(a) filter P(V) lower bound >= 0.88; (b) >= 0.70 per cell; (c) DP against maintain lower bound >= +0.05; M6(a) added lost rows upper bound <= +0.05; (b) wall contacts <= 0.10 per row.

## 2. Implementation, self-checks, bench, development run

ph21.py defines Agent8 = ph19.Agent6 with one line of act replaced under the flag `filt` (keep = h >= 0 and (v_h = v_max or v_h < 0); nav = hit where keep, otherwise a whiff of a top-valued non-negative odour); `nav6` (Agent6's expression) and `differs` are exposed for measurement and read by nothing. No file in src/ other than the new ph21.py was edited. **No implementation error: every self-check passed on the first run; no fix was made.**

**Self-checks (demo, output sha f576bcf4...052c):** the H21 chain (ph19.demo) passes; Agent8 with the filter off is Agent6 bitwise, and with the filter on is Agent6 at 0/0, +1/+1 and +1/-1 while differing at +1/0; in a constructed state with the neutral odour held, neutral whiffs every step give nav on 0 percent of held steps with the filter (100 percent without) and the silence timer is still reset by every hit; valued whiffs while the neutral odour is still held give nav on 100 percent with the filter (0 percent without); at run level the maintain, neutral and priority-identity arms equal Agent6's runs, the filter arm's nav equals the valued whiff on every (row, step) and its trajectory equals G 0 gate off, the separation from maintain holds up to the first `differs` step, and no `differs` step occurs while the valued odour is held. **The bench (b) and (d) start states are ph20b's exactly:** rebuilt in ph21 on the H22 bench seeds and compared with ph20b.simulate (rule off = Agent6), bitwise equal over 400 rows (H and whiffs), reproducing 34/400 holding valued at 600 on the variant start and 5/400 at 300 on the registered start, with Agent6 and with Agent8 filter off. Seed check: the H23 seeds, the bootstrap seed and the derived generators appear in no other file under the repository.

**Found in implementation, not an amendment:** design v2 section 9 lists the bench's derived generators as 30261001 / 40261002; seed + 10000 and seed + 20000 give 20271001 / 20281002. The code's seed check covers all four numbers (none found elsewhere); no seed, draw or run is affected. Flagged for the owner.

**Mechanism bench (M4), output sha 1b836023...3330, record:h23-bench-result: PASS.** (a1) filter off equals Agent6 bitwise on the stub (with and without a constructed neutral hold) and on World7, 400 rows x 600 steps. (a2) filter on at 0/0, +1/+1, +1/-1 equals Agent6 bitwise on the stub and on World7, `differs` 0. (a3) +1/0 with the valued odour held: bitwise Agent6. (a4) channel 1 (value 0) held by construction, both channels p 0.30: nav equals channel 0's whiff on every step in 400/400 rows, 1.000 [0.990, 1.000] against 0.95; channel 1 was held on 5641 (row, step), nav True on 1579 of them, each with a valued whiff. (a5) World7 task start: positions and headings of Agent8 at G 2 with the gate equal Agent8 at G 0 gate off and Agent8 with a neutral hold constructed at step 0; the circuit states differ (holding valued at 600: 396 / 329 / 391) while the trajectories do not. (c) task start, nothing held: every nav step carries a valued whiff in 400/400 rows, 1.000 [0.990, 1.000] against 0.95.

**Bench (b), the one measurement of whether the hold follows navigation (reported, not a gate): PASS against its registered bar.** Task-like neutral-hold start (the diagnosis's variant state: on the neutral axis 20 downwind of the neutral source, heading upwind, s 2.0 / 0, S 0, since 0), 800 rows x 600 steps, same rows and draws:

| | Agent8 (filter) | Agent6 (maintain) |
|---|---|---|
| holding the valued odour at step 600 | 217/800 = 0.271 [0.242, 0.303] | 70/800 = 0.087 [0.070, 0.109] |
| dwell majority V / N / tie | 18 / 782 / 0 | 8 / 791 / 1 |
| rows with a valued whiff by 600; first valued whiff step quartiles | 360; 448 / 469 / 534 | 91; 370 / 483 / 526 |
| first surge on a valued whiff | 360 rows, at the first valued whiff itself in 360 | 72 rows, at the first valued whiff itself in 2 |
| first surge on a neutral-only whiff | 0 rows | 800 rows, step quartiles 4 / 9 / 16 |
| first valued hold entered from nothing held / directly from the neutral hold | 217 / 0 | 71 / 0 |
| releases of the neutral hold (N -> nothing) and how they end | 409: valued 217 (5 / 8 / 18 steps), neutral again 127, still nothing at 600 65 | 91: valued 71, neutral 14, nothing 6 |
| holds ended by flag | 409 (evidence 382, timeout flag 0, neither 27) | 92 (evidence 91, neither 1) |
| P(holding at 600 given a valued whiff) | 0.603 | 0.769 |
| no whiff of either plume in the last 100 steps; wall contacts | 175; 0 | 257; 0 |

Paired: positions first differ in 800/800 rows at step quartiles 4 / 9 / 16, the same steps as Agent8's first `differs` step (Agent6's first surge on a whiff of the held neutral odour); holding valued at 600 in both 22, Agent8 only 195, Agent6 only 48. **DP = +0.1837 [+0.1475, +0.2200] (bootstrap 5000, seed 20261003), bar lower bound > 0: PASS.** Reading (measured, no cause beyond it): with the filter the hold follows navigation in part: 217 of the 360 rows that met a valued whiff hold it at 600; every revision passes through 'nothing held' (the evidence release after valued whiffs), none is a direct flip; 127 releases return to the neutral hold. From this start 600 steps leave too little time for the dwell majority (V 18 of 800): the first valued whiff arrives at step 469 median.

(d) placed at the neutral source with a neutral hold (ph20.bench_d's state), H23 bench seeds, reported: Agent8 holds the valued odour at 300 in 221/400 = 0.552, at 600 in 305/400 = 0.762 [0.718, 0.802]; Agent6 8/400 and 82/400 = 0.205.

**Development run (seeds 9880/9980, output sha 2cb2a062...f2f4, record:h23-dev-run):** no operation error; no amendment. (Its printout read every criterion PASS, filter 373/400 = 0.932, DP against maintain +0.243 [+0.200, +0.285]; that printout is not the verdict.) Evaluation seeds unused until the one evaluation.

## 3. Results, one evaluation (seeds 1765 / 1865)

| arm | values | G | gate | rule | V | N | tie | first hold valued / neutral | holding valued at 600 | P(V) dwell majority |
|---|---|---|---|---|---|---|---|---|---|---|
| filter | +1 / 0 | 2 | on | on | 381 | 14 | 5 | 274 / 126 | 396 | 0.953 [0.927, 0.969] |
| maintain | +1 / 0 | 2 | on | off | 285 | 109 | 6 | 270 / 130 | 321 | 0.713 |
| pathway-off | +1 / 0 | 0 | off | off | 182 | 210 | 8 | 196 / 204 | 173 | 0.455 [floor: P(V \| chose) 0.464] |
| known-answer | +1 / 0 | 0 | off | fixed h | 386 | 13 | 1 | 400 / 0 | 400 | 0.965 [0.942, 0.979] |
| neutral | 0 / 0 | 2 | on | on | 182 | 210 | 8 | 196 / 204 | 173 | 0.455 (bitwise pathway-off) |
| priority-identity | +1 / -1 | 2 | on | on | 363 | 17 | 20 | 274 / 126 | 351 | 0.908 (bitwise Agent6 = the Run 2 agent) |

Cells of the filter arm (V of 100; odour A +y, A -y, B +y, B -y): 96 / 95 / 94 / 96. Dwell medians valued / other: filter 25.0 / 0.0, maintain 20.0 / 7.0, known-answer 25.0 / 0.0. No wall contact in any +1/0 arm. Input range at G 2: y' max 5.34, the clip on 0.00 to 0.01 percent of steps; no arm flagged. First-reach secondary: filter 207 / 192 / 1 none (0.517), maintain 201 / 199 (0.502), pathway-off 199 / 201, known-answer 210 / 190 (0.525).

## 4. Criteria

- **M1 task validity: PASS.** Ties 8 / 8 / 1 of 400 in neutral, pathway-off, known-answer. Side balance 183/392 = 0.467 [0.418, 0.516]. Floor 182/392 = 0.464 [0.416, 0.514]. Ceiling 386/400 = 0.965 [0.942, 0.979]. Section 8: ties in the arms under test 0.013 (filter), 0.015 (maintain).
- **M2 main: PASS.** (a) filter P(V) 381/400 = 0.953 [0.927, 0.969] against 0.88: PASS. (b) cells 96, 95, 94, 96 of 100, lower bounds 0.902, 0.888, 0.875, 0.902 against 0.70: PASS. (c) DP = P(V) filter minus maintain = +0.240 [+0.200, +0.282] against +0.05: PASS (a PASS says 'at least +0.05', as the design states). Reported: DP against pathway-off +0.497 [+0.448, +0.547]; N 14, tie 5.
- **M3 identities: PASS.** (i) maintain (Agent8, filter off) equals ph19.Agent6; (ii) neutral and priority-identity with the filter equal Agent6, Agent6 at 0/0 equals G 0, G 0 equals ph14.Agent3, Agent6 at +1/-1 equals ph16.Agent4; (iii) the filter arm's nav equals the valued whiff on every (row, step), and its positions and headings equal Agent8 at G 0 gate off; (iv) filter against maintain bitwise equal up to each row's first `differs` step (190 rows differ, all equal before it; 210 rows never differ and are equal over all 600 steps); (v) known-answer h equals the valued odour and its hit its whiffs.
- **M4 mechanism bench: PASS** (section 2; re-run inside the evaluation with the bench seeds: (a4) 0.990, (c) 0.990; beside it, not a gate, (b) DP +0.1837 [+0.1475, +0.2200] -> PASS).
- **M5 avoidance: PASS.** The +1/-1 agent is Agent6 = the Run 2 agent by construction (M3 ii); constructed state 300 negative-held (row, step), flee target on every one, equal to G 0's.
- **M6 no added lost rows: PASS.** (a) no whiff of either plume in the last third, filter minus maintain -0.010 [-0.020, -0.003] against at most +0.05 (0 against 4 rows). (b) wall contacts 0.000 per row against at most 0.10. Reported: no navigation hit in the last third, filter 13, maintain 12, pathway-off 7, known-answer 15, neutral 7, priority-identity 32; cast clock max filter 600, maintain 506.

**H23 under the registered criteria: the rule steers only on a top-valued odour whatever is held, with the identities holding (M4); with it the agent stays at the valued source in more rows than the H21 maintain agent, at P(V) of at least 0.88, without adding lost rows (M1 to M6 all PASS; bench (b), whether the hold follows navigation from the task-like neutral-hold start, reported beside the verdict: PASS, not part of it).** A statement about a supplied value, this rule, values +1/0, C0, the dwell-majority measure and the full agent with its circuit running; not about selection controlling navigation (it does not, at +1/0), learning, other values, other G, other geometries, or a world in which the higher-valued odour is absent. One evaluation, no extension.

## 5. Where the value goes now (measured; the reading names no cause beyond what was measured)

- **Navigation equals the known-answer law, and P(V) matches it:** filter / known-answer = 0.953 / 0.965 = 0.987 (predicted 0.97 to 1.03). The filter arm's nav equals the valued whiff on every (row, step) and its trajectory is bitwise the G 0 gate-off rerun's (M3 iii). maintain / known-answer = 0.738.
- **The first selection is almost unchanged, and no longer decides the outcome:** first hold valued 274 (filter) against 270 (maintain), identical row for row in 388/400. P(V | first hold valued) 268/274 = 0.978 (maintain 263/270 = 0.974); **P(V | first hold neutral) 113/126 = 0.897 (maintain 22/130 = 0.169).**
- **Does the hold follow navigation? In the task, largely:** neutral-first rows later held the valued odour in 122/126 = 0.968 with the filter against 52/130 = 0.400 for maintain; holding the valued odour at step 600: filter 396/400, maintain 321/400, known-answer 400 (fixed), pathway-off 173; among maintain's 130 neutral-first rows, 126 hold the valued odour at 600 with the filter against 52 without. The hold lags where navigation goes: the filter arm spent 681 steps at the valued source while still holding the neutral odour (maintain 89) and 752 steps at the neutral source while holding the valued odour (maintain 797). From the task-like neutral-hold start (bench b) the hold follows in part (0.271 at 600 against 0.087).
- **Revision route:** holds ended in the filter arm 131 (evidence 126, timeout flag 1, neither 4): neutral holds ended 128, valued holds ended 3 (maintain 78: neutral 76, valued 2). On bench (b) every first valued hold was entered from 'nothing held' (217/217), none directly from the neutral hold, and 127 of 409 releases returned to the neutral hold. The route is not decomposed per transition in the task printout.
- **`differs` counts:** in the filter arm 190/400 rows have at least one step on which the filter's nav differs from Agent6's expression, first at step quartiles 1 / 5 / 11; 1206 (row, step) in all. M3 (iv): all 190 are bitwise equal to maintain before that step; the other 210 never differ and are equal to maintain over all 600 steps.
- **Paired flips against maintain, same rows:** into V 97, out of V 1, unchanged class 301, one row moved between N and tie. Into V among neutral-first rows 88, among valued-first rows 9.
- **Lost rows:** no whiff of either plume in the last third, filter 0, maintain 4, known-answer 2; no navigation hit in the last third, filter 13 (maintain 12, known-answer 15).
- **Timeout:** fired 4176 times while held in the filter arm and ended 1 hold (maintain 4304 and 6); the recorded limit (record:silence-timeout-chain-result) again.

## 6. Predictions (design v2 section 10) against the observations

| prediction | observed | |
|---|---|---|
| bench (a), (c) implementation parts True, 1.000 | all True; (a4) and (c) 400/400 = 1.000 | met |
| bench (b) Agent8 holding valued at 600: 0.083 to 0.33, centre 0.20 | 0.271 [0.242, 0.303] | met, above the centre |
| bench (b) Agent6: 0.085 (rate from the H22 seeds) | 0.087 [0.070, 0.109] | met |
| bench (b) DP: -0.002 to +0.24, centre +0.115 | +0.184 [+0.148, +0.220] | met, above the centre |
| bench (b) first valued whiff: 0.48 of rows by 600, median step 473 | 360/800 = 0.45; median 469 | met approximately |
| bench (b) conversion given a valued whiff: between 0.173 and 0.680 | 217/360 = 0.603 | met |
| bench (b) first surge on the valued odour at the first valued whiff in every row that has one | 360/360 | met |
| bench (b) revision route via 'nothing held' in nearly every row | 217/217 | met |
| bench (b) no whiff in the last 100 steps: not predicted numerically (H22 rule 26/400; Agent6 119/400 on the H22 seeds) | Agent8 175/800 = 0.219; Agent6 257/800 = 0.321 | not predicted; Agent8 well above the H22 rule's rate |
| bench (b) wall contacts 0 | 0 | met |
| bench (c) Agent6 first surge about half valued | valued only 188, neutral only 205, both 7 | met |
| bench (c) Agent8 first surge valued in every row that surges | valued only 384, both 13, neutral only 0 (3 no surge) | met |
| bench (c) first hold valued 0.685 to 0.70, within a few percent of Agent6 | Agent8 280/400 = 0.70; Agent6 265/400 = 0.66 | met for Agent8; Agent6 slightly below the range |
| bench (c) dwell P(V) Agent8 0.93 to 0.97, Agent6 0.72 to 0.78 | 0.945; 0.725 | met |
| bench (d) holding valued at 600: 0.33 to 0.71 | 305/400 = 0.762 [0.718, 0.802] | NOT met: above the upper edge |
| bench (d) first valued whiff 323 of 400 by 600, median step 201 | not printed | not measured |
| task filter P(V) 0.93 to 0.97, centre 0.95 | 0.953 | met |
| task maintain P(V) 0.72 to 0.78 | 285/400 = 0.713 | NOT met: 0.007 below the lower edge |
| task DP filter - maintain +0.15 to +0.25, centre +0.20 | +0.240 | met |
| P(V) filter / known-answer 0.97 to 1.03 | 0.987 | met |
| per-cell P(V) within about 0.05 of the arm | 0.94 to 0.96 against 0.953 | met |
| ties about 0.3 percent (filter) | 5/400 = 1.25 percent | above the prediction (no bar) |
| holding valued at 600, filter higher than maintain among neutral-first rows | 126 against 52 of 130 | met |
| M6: no whiff in the last third within +/-0.01 of maintain | -0.010 (0 against 4) | met, at the edge |
| M6: contacts 0.00 to 0.02 | 0.000 | met |
| no navigation hit in the last third near known-answer's and above maintain's | filter 13, known-answer 15, maintain 12 | met |
| M1 passes, ceiling 0.93 to 0.97 | PASS, 0.965 | met |
| M3 (iv): rows never differing from maintain a minority | 210/400 never differ | NOT met: a majority |
| the random-stream difference does not matter more than sampling (ratio within 0.94 to 1.06) | 0.987 | met |

## 7. What is shown and what is not

- Shown (registered): the rule steers only on a top-valued odour whatever is held (M4: a4 400/400, c 400/400) and is Agent6 bitwise wherever the design says (a1, a2, a3, M3 i, ii); at +1/0 the circuit does not steer (a5, M3 iii: trajectories bitwise equal at G 0 gate off and with a constructed neutral hold); the task is valid for the measure (M1, ceiling 0.965); the filter arm stays at the valued source in 381/400 rows (lower bound 0.927 against 0.88), in at least 94 of 100 in every cell, +0.240 [+0.200, +0.282] over the H21 maintain agent on the same rows; it adds no lost rows and no wall contact (M6); avoidance is untouched by construction (M5).
- **Not shown, verbatim from the design: 'the task therefore cannot show that selection controls navigation', and a pass is a statement about value-driven navigation in the full agent, not about selection.** At +1/0 in this task the selection circuit does nothing for navigation.
- Measured, not a criterion: bench (b), the one measurement of whether the hold follows navigation from the task-like neutral-hold start: 0.271 against 0.087 at 600 (DP +0.184 [+0.148, +0.220], PASS against its reported bar); every revision through 'nothing held'. In the task the hold follows navigation in most rows (neutral-first rows revised 0.968; valued held at 600 in 396/400), with lag. P(V) filter / known-answer 0.987.
- Not tested: learning; the integrated environment; values other than +1/0, in particular +1/+0.5; **a world where the higher-valued odour is absent** (the agent would never surge on the only odour present if it is not top-valued; the rule's cost, bounding any adoption); any G other than 2; any geometry other than C0; the rule without the gate as a separate arm (bitwise the same trajectories at +1/0, a5); the timeout; a change to the circuit (none made); avoidance with the rule acting on a negative odour; the first selection as a lever; a crosswind or position term.

## 8. Provenance

- Design v2 FINAL doc db6df2e0013ab96e7 (hash c19751f4...0087); v1 doc d77542ae99d003747 (history); decision:h23-open-design, decision:h23-open.
- Code ph21.py sha 3a1d79d9...cfc1 (source doc ddcec8520fcd8e23c, stored in full before the development run). Demo output sha f576bcf4...052c. Bench output sha 1b836023...3330 (record:h23-bench-result). Development output sha 2cb2a062...f2f4 (record:h23-dev-run).
- Evaluation: seeds 1765/1865 unused before; output ph21_eval.txt sha b7b35099...c6d0, appended below in full. Result: record:h23-result. Closure is the owner's.

## Appendix A: ph21_eval.txt in full (sha256 b7b35099a43e7993bf93c7f1c18ff7e8d40d1f7a42783d63ee6abbef86cec6d0)

== H23, EVAL. design v2 FINAL doc db6df2e0013ab96e7 hash c19751f427363da9456a681659e23bf19bdb5463bdff966af99d04783bb30087; this file sha256 3a1d79d9a0d235f1bef7e435ec594cff4048180e27b28dcd892598c58413cfc1; G 2.0, gate on where G 2; world seed 1765, agent seed 1865; 400 rows x 600 steps; geometry C0; bootstrap seed 20261003; the one evaluation ==
   rows share no state: one generator per world and one per agent population, fixed-size draws consumed in row order every step

   [filter] G 2.0  MAIN, dwell majority: V 381  N 14  tie 5  (of 400)
      cells: 0 odour A valued, +y: V 96 N 4 0 0 | 1 odour A valued, -y: V 95 N 4 0 1 | 2 odour B valued, +y: V 94 N 5 0 1 | 3 odour B valued, -y: V 96 N 1 0 3
      dwell median valued 25.0 other 0.0; both zero 1; majority source == first hold 280/400; P(V | first hold valued) 268/274; P(V | first hold neutral) 113/126
      H21 diag: dwell steps at valued (valued-held, neutral-held, nothing) (8664, 681, 571) | at neutral (752, 975, 179); nothing held 0.071 of steps
      H21 diag: holds ended 131 (on the timeout flag 1, evidence 126, both 0, neither 4); held unit's s the step before, median 1.06; timeout firings while held 4176, of which ended the hold 1; valued holds ended 3, neutral holds ended 128
      H21 diag: revision, first hold neutral and later held valued 122/126 = 0.968; no whiff of either plume in the last third 0; no navigation hit in the last third 13; wall contacts per row 0.00
      H23 diag: rows with a `differs` step 190/400, first `differs` step quartiles 1/5/11; `differs` (row, step) 1206; nav == valued whiff on every (row, step) True; holding the valued odour at step 600 396/400 (neutral 4, nothing 0); P(V | first hold valued) 268/274, P(V | first hold neutral) 113/126; cast clock max 600
      H23 diag: paired against maintain, same rows: into V 97, out of V 1, unchanged class 301/400; first hold identical row for row 388/400 (valued here 274 against 270); into V among neutral-first rows 88, among valued-first rows 9; holding valued at step 600 here 396 against 321 (among maintain's neutral-first rows 126 against 52 of 130)
      secondary, first reach and diagnostics:

   [filter] G 2.0  V 207  N 192  no-choice 1  (of 400)
      cells: 0 odour A valued, +y: V 48 N 52 0 0 | 1 odour A valued, -y: V 55 N 45 0 0 | 2 odour B valued, +y: V 56 N 44 0 0 | 3 odour B valued, -y: V 48 N 51 0 1
      P(V | reached) 207/399 = 0.519 [0.470, 0.567]; first-approach step median V 31 N 30; dwell median valued 25.0 other 0.0; contacts/row 0.00; no whiff in the last third 0
      first hold: valued 274 neutral 126 none 0, step median 12; hold changes mean 0.32; agreement: first hold == source reached 293/399, held at reach == source reached 270/399 (nothing held at reach 44); P(V | first hold valued) 187/274; P(V | first hold neutral) 20/126
      whiffs/row: valued plume 11.1 neutral plume 4.8 both same step 0.05; no-choice rows' hold history: never 0 valued only 1 neutral only 0 both 0
      input range: y' max 5.34, y' > 1.8 on 4.13% of (row, step, channel), s >= 4.9 on 0.01% of (row, step), s max 4.95
      segments, N rows: neutral selected first and held at reach 86; valued held earlier, neutral held at reach 1; valued held at reach yet neutral reached first 80; nothing held at reach 25 | V rows: valued held at reach 183 (of which first hold was neutral 0), neutral held at reach 5, nothing held 19

   [maintain] G 2.0  MAIN, dwell majority: V 285  N 109  tie 6  (of 400)
      cells: 0 odour A valued, +y: V 65 N 34 0 1 | 1 odour A valued, -y: V 77 N 22 0 1 | 2 odour B valued, +y: V 77 N 22 0 1 | 3 odour B valued, -y: V 66 N 31 0 3
      dwell median valued 20.0 other 7.0; both zero 0; majority source == first hold 368/400; P(V | first hold valued) 263/270; P(V | first hold neutral) 22/130
      H21 diag: dwell steps at valued (valued-held, neutral-held, nothing) (7168, 89, 82) | at neutral (797, 2282, 524); nothing held 0.061 of steps
      H21 diag: holds ended 78 (on the timeout flag 6, evidence 67, both 0, neither 5); held unit's s the step before, median 1.06; timeout firings while held 4304, of which ended the hold 6; valued holds ended 2, neutral holds ended 76
      H21 diag: revision, first hold neutral and later held valued 52/130 = 0.400; no whiff of either plume in the last third 4; no navigation hit in the last third 12; wall contacts per row 0.00
      H23 diag: rows with a `differs` step 0/400, first `differs` step quartiles n/a; `differs` (row, step) 0; nav == valued whiff on every (row, step) False; holding the valued odour at step 600 321/400 (neutral 75, nothing 4); P(V | first hold valued) 263/270, P(V | first hold neutral) 22/130; cast clock max 506
      secondary, first reach and diagnostics:

   [maintain] G 2.0  V 201  N 199  no-choice 0  (of 400)
      cells: 0 odour A valued, +y: V 46 N 54 0 0 | 1 odour A valued, -y: V 53 N 47 0 0 | 2 odour B valued, +y: V 56 N 44 0 0 | 3 odour B valued, -y: V 46 N 54 0 0
      P(V | reached) 201/400 = 0.502 [0.454, 0.551]; first-approach step median V 31 N 31; dwell median valued 20.0 other 7.0; contacts/row 0.00; no whiff in the last third 4
      first hold: valued 270 neutral 130 none 0, step median 12; hold changes mean 0.14; agreement: first hold == source reached 295/400, held at reach == source reached 243/400 (nothing held at reach 60); P(V | first hold valued) 183/270; P(V | first hold neutral) 18/130
      whiffs/row: valued plume 9.1 neutral plume 5.6 both same step 0.04; no-choice rows' hold history: never 0 valued only 0 neutral only 0 both 0
      input range: y' max 5.34, y' > 1.8 on 3.44% of (row, step, channel), s >= 4.9 on 0.00% of (row, step), s max 4.93
      segments, N rows: neutral selected first and held at reach 71; valued held earlier, neutral held at reach 0; valued held at reach yet neutral reached first 83; nothing held at reach 45 | V rows: valued held at reach 172 (of which first hold was neutral 1), neutral held at reach 14, nothing held 15

   [pathway-off] G 0.0  MAIN, dwell majority: V 182  N 210  tie 8  (of 400)
      cells: 0 odour A valued, +y: V 43 N 56 0 1 | 1 odour A valued, -y: V 52 N 46 0 2 | 2 odour B valued, +y: V 43 N 57 0 0 | 3 odour B valued, -y: V 44 N 51 0 5
      dwell median valued 12.0 other 13.0; both zero 0; majority source == first hold 311/400; P(V | first hold valued) 146/196; P(V | first hold neutral) 36/204
      H21 diag: dwell steps at valued (valued-held, neutral-held, nothing) (3856, 106, 1235) | at neutral (98, 4114, 1475); nothing held 0.200 of steps
      H21 diag: holds ended 246 (on the timeout flag 13, evidence 207, both 0, neither 26); held unit's s the step before, median 1.06; timeout firings while held 3846, of which ended the hold 13; valued holds ended 133, neutral holds ended 113
      H21 diag: revision, first hold neutral and later held valued 67/204 = 0.328; no whiff of either plume in the last third 7; no navigation hit in the last third 7; wall contacts per row 0.00
      H23 diag: rows with a `differs` step 0/400, first `differs` step quartiles n/a; `differs` (row, step) 0; nav == valued whiff on every (row, step) False; holding the valued odour at step 600 173/400 (neutral 199, nothing 28); P(V | first hold valued) 146/196, P(V | first hold neutral) 36/204; cast clock max 439
      secondary, first reach and diagnostics:

   [pathway-off] G 0.0  V 199  N 201  no-choice 0  (of 400)
      cells: 0 odour A valued, +y: V 46 N 54 0 0 | 1 odour A valued, -y: V 53 N 47 0 0 | 2 odour B valued, +y: V 54 N 46 0 0 | 3 odour B valued, -y: V 46 N 54 0 0
      P(V | reached) 199/400 = 0.497 [0.449, 0.546]; first-approach step median V 31 N 31; dwell median valued 12.0 other 13.0; contacts/row 0.00; no whiff in the last third 7
      first hold: valued 196 neutral 204 none 0, step median 28; hold changes mean 0.37; agreement: first hold == source reached 339/400, held at reach == source reached 180/400 (nothing held at reach 189); P(V | first hold valued) 167/196; P(V | first hold neutral) 32/204
      whiffs/row: valued plume 6.7 neutral plume 7.1 both same step 0.04; no-choice rows' hold history: never 0 valued only 0 neutral only 0 both 0
      input range: y' max 1.78, y' > 1.8 on 0.00% of (row, step, channel), s >= 4.9 on 0.00% of (row, step), s max 3.63
      segments, N rows: neutral selected first and held at reach 84; valued held earlier, neutral held at reach 1; valued held at reach yet neutral reached first 15; nothing held at reach 101 | V rows: valued held at reach 95 (of which first hold was neutral 1), neutral held at reach 16, nothing held 88

   [known-answer] G 0.0 (held odour fixed to the valued odour)  MAIN, dwell majority: V 386  N 13  tie 1  (of 400)
      cells: 0 odour A valued, +y: V 96 N 4 0 0 | 1 odour A valued, -y: V 98 N 2 0 0 | 2 odour B valued, +y: V 94 N 5 0 1 | 3 odour B valued, -y: V 98 N 2 0 0
      dwell median valued 25.0 other 0.0; both zero 0; majority source == first hold 386/400; P(V | first hold valued) 386/400; P(V | first hold neutral) 0/0
      H21 diag: dwell steps at valued (valued-held, neutral-held, nothing) (9997, 0, 0) | at neutral (1891, 0, 0); nothing held 0.000 of steps
      H21 diag: holds ended 0 (on the timeout flag 0, evidence 0, both 0, neither 0); held unit's s the step before, median nan; timeout firings while held 0, of which ended the hold 0; valued holds ended 0, neutral holds ended 0
      H21 diag: revision, first hold neutral and later held valued 0/0; no whiff of either plume in the last third 2; no navigation hit in the last third 15; wall contacts per row 0.00
      H23 diag: rows with a `differs` step 0/400, first `differs` step quartiles n/a; `differs` (row, step) 0; nav == valued whiff on every (row, step) True; holding the valued odour at step 600 400/400 (neutral 0, nothing 0); P(V | first hold valued) 386/400, P(V | first hold neutral) 0/0; cast clock max 600
      secondary, first reach and diagnostics:

   [known-answer] G 0.0  V 210  N 190  no-choice 0  (of 400)
      cells: 0 odour A valued, +y: V 51 N 49 0 0 | 1 odour A valued, -y: V 57 N 43 0 0 | 2 odour B valued, +y: V 57 N 43 0 0 | 3 odour B valued, -y: V 45 N 55 0 0
      P(V | reached) 210/400 = 0.525 [0.476, 0.573]; first-approach step median V 31 N 30; dwell median valued 25.0 other 0.0; contacts/row 0.00; no whiff in the last third 2
      first hold: valued 400 neutral 0 none 0, step median 0; hold changes mean 0.00; agreement: first hold == source reached 210/400, held at reach == source reached 210/400 (nothing held at reach 0); P(V | first hold valued) 210/400; P(V | first hold neutral) 0/0
      whiffs/row: valued plume 10.9 neutral plume 4.8 both same step 0.04; no-choice rows' hold history: never 0 valued only 0 neutral only 0 both 0
      input range: y' max 1.78, y' > 1.8 on 0.00% of (row, step, channel), s >= 4.9 on 0.00% of (row, step), s max 0.00
      segments, N rows: neutral selected first and held at reach 0; valued held earlier, neutral held at reach 0; valued held at reach yet neutral reached first 190; nothing held at reach 0 | V rows: valued held at reach 210 (of which first hold was neutral 0), neutral held at reach 0, nothing held 0

   [neutral] G 2.0  MAIN, dwell majority: V 182  N 210  tie 8  (of 400)
      cells: 0 odour A valued, +y: V 43 N 56 0 1 | 1 odour A valued, -y: V 52 N 46 0 2 | 2 odour B valued, +y: V 43 N 57 0 0 | 3 odour B valued, -y: V 44 N 51 0 5
      dwell median valued 12.0 other 13.0; both zero 0; majority source == first hold 311/400; P(V | first hold valued) 146/196; P(V | first hold neutral) 36/204
      H21 diag: dwell steps at valued (valued-held, neutral-held, nothing) (3856, 106, 1235) | at neutral (98, 4114, 1475); nothing held 0.200 of steps
      H21 diag: holds ended 246 (on the timeout flag 13, evidence 207, both 0, neither 26); held unit's s the step before, median 1.06; timeout firings while held 3846, of which ended the hold 13; valued holds ended 133, neutral holds ended 113
      H21 diag: revision, first hold neutral and later held valued 67/204 = 0.328; no whiff of either plume in the last third 7; no navigation hit in the last third 7; wall contacts per row 0.00
      H23 diag: rows with a `differs` step 0/400, first `differs` step quartiles n/a; `differs` (row, step) 0; nav == valued whiff on every (row, step) False; holding the valued odour at step 600 173/400 (neutral 199, nothing 28); P(V | first hold valued) 146/196, P(V | first hold neutral) 36/204; cast clock max 439
      secondary, first reach and diagnostics:

   [neutral] G 2.0  V 199  N 201  no-choice 0  (of 400)
      cells: 0 odour A valued, +y: V 46 N 54 0 0 | 1 odour A valued, -y: V 53 N 47 0 0 | 2 odour B valued, +y: V 54 N 46 0 0 | 3 odour B valued, -y: V 46 N 54 0 0
      P(V | reached) 199/400 = 0.497 [0.449, 0.546]; first-approach step median V 31 N 31; dwell median valued 12.0 other 13.0; contacts/row 0.00; no whiff in the last third 7
      first hold: valued 196 neutral 204 none 0, step median 28; hold changes mean 0.37; agreement: first hold == source reached 339/400, held at reach == source reached 180/400 (nothing held at reach 189); P(V | first hold valued) 167/196; P(V | first hold neutral) 32/204
      whiffs/row: valued plume 6.7 neutral plume 7.1 both same step 0.04; no-choice rows' hold history: never 0 valued only 0 neutral only 0 both 0
      input range: y' max 1.78, y' > 1.8 on 0.00% of (row, step, channel), s >= 4.9 on 0.00% of (row, step), s max 3.63
      segments, N rows: neutral selected first and held at reach 84; valued held earlier, neutral held at reach 1; valued held at reach yet neutral reached first 15; nothing held at reach 101 | V rows: valued held at reach 95 (of which first hold was neutral 1), neutral held at reach 16, nothing held 88

   [priority-identity] G 2.0  MAIN, dwell majority: V 363  N 17  tie 20  (of 400)
      cells: 0 odour A valued, +y: V 92 N 5 0 3 | 1 odour A valued, -y: V 89 N 7 0 4 | 2 odour B valued, +y: V 93 N 2 0 5 | 3 odour B valued, -y: V 89 N 3 0 8
      dwell median valued 22.0 other 0.0; both zero 14; majority source == first hold 269/400; P(V | first hold valued) 260/274; P(V | first hold neutral) 103/126
      H21 diag: dwell steps at valued (valued-held, neutral-held, nothing) (7444, 373, 669) | at neutral (349, 336, 513); nothing held 0.140 of steps
      H21 diag: holds ended 409 (on the timeout flag 1, evidence 405, both 0, neither 3); held unit's s the step before, median 1.06; timeout firings while held 3964, of which ended the hold 1; valued holds ended 233, neutral holds ended 176
      H21 diag: revision, first hold neutral and later held valued 107/126 = 0.849; no whiff of either plume in the last third 24; no navigation hit in the last third 32; wall contacts per row 0.32
      H23 diag: rows with a `differs` step 0/400, first `differs` step quartiles n/a; `differs` (row, step) 0; nav == valued whiff on every (row, step) False; holding the valued odour at step 600 351/400 (neutral 28, nothing 21); P(V | first hold valued) 260/274, P(V | first hold neutral) 103/126; cast clock max 600
      secondary, first reach and diagnostics:

   [priority-identity] G 2.0  V 273  N 113  no-choice 14  (of 400)
      cells: 0 odour A valued, +y: V 64 N 33 0 3 | 1 odour A valued, -y: V 67 N 30 0 3 | 2 odour B valued, +y: V 69 N 28 0 3 | 3 odour B valued, -y: V 73 N 22 0 5
      P(V | reached) 273/386 = 0.707 [0.660, 0.750]; first-approach step median V 32 N 31; dwell median valued 22.0 other 0.0; contacts/row 0.32; no whiff in the last third 24
      first hold: valued 274 neutral 126 none 0, step median 12; hold changes mean 0.56; agreement: first hold == source reached 220/386, held at reach == source reached 224/386 (nothing held at reach 108); P(V | first hold valued) 190/274; P(V | first hold neutral) 83/126
      whiffs/row: valued plume 10.2 neutral plume 3.9 both same step 0.04; no-choice rows' hold history: never 0 valued only 0 neutral only 11 both 3
      input range: y' max 5.34, y' > 1.8 on 3.87% of (row, step, channel), s >= 4.9 on 0.00% of (row, step), s max 4.91
      segments, N rows: neutral selected first and held at reach 8; valued held earlier, neutral held at reach 1; valued held at reach yet neutral reached first 50; nothing held at reach 54 | V rows: valued held at reach 215 (of which first hold was neutral 39), neutral held at reach 4, nothing held 54

== criteria (design v2 FINAL section 7; 95 percent, one evaluation, no extension; aggregation: PASS if every part passes, FAIL if any fails, else INCONCLUSIVE) ==
   M1(a) neutral: ties 8/400 = 0.020  at most 0.20 -> PASS
   M1(a) pathway-off: ties 8/400 = 0.020  at most 0.20 -> PASS
   M1(a) known-answer: ties 1/400 = 0.003  at most 0.20 -> PASS
   M1(b) neutral, P(+y source majority | chose): P k 183 n 392  value 0.467  95% interval [0.418, 0.516]  within [0.35, 0.65] -> PASS
   M1(c) floor: pathway-off, P(V | chose): P k 182 n 392  value 0.464  95% interval [0.416, 0.514]  within [0.35, 0.65] -> PASS
   M1(d) ceiling: known-answer, P(V) over all rows: P k 386 n 400  value 0.965  95% interval [0.942, 0.979]  at least 0.85 -> PASS
   M1 -> PASS
   section 8: ties in the arms under test, filter 0.013, maintain 0.015 (unreadable above 0.20)
   M2(a) filter, P(V) over all rows: P k 381 n 400  value 0.953  95% interval [0.927, 0.969]  at least 0.88 -> PASS
   M2(b) filter, cell 0 (odour A valued, +y), P(V): P k 96 n 100  value 0.960  95% interval [0.902, 0.984]  at least 0.7 -> PASS
   M2(b) filter, cell 1 (odour A valued, -y), P(V): P k 95 n 100  value 0.950  95% interval [0.888, 0.978]  at least 0.7 -> PASS
   M2(b) filter, cell 2 (odour B valued, +y), P(V): P k 94 n 100  value 0.940  95% interval [0.875, 0.972]  at least 0.7 -> PASS
   M2(b) filter, cell 3 (odour B valued, -y), P(V): P k 96 n 100  value 0.960  95% interval [0.902, 0.984]  at least 0.7 -> PASS
   M2(c) DP = P(V) filter - maintain, same rows: DP n 400  value 0.240  95% interval [0.200, 0.282]  at least 0.05 -> PASS
   M2 -> PASS
      reported, no bar: DP filter - pathway-off +0.497 [+0.448, +0.547]
      reported: filter N 14 tie 5; P(V) filter / known-answer = 0.953 / 0.965 = 0.987 (predicted 0.97 to 1.03; outside 0.94 to 1.06 would show the random-stream difference matters more than sampling); P(V) maintain / known-answer 0.738
      reported: filter P(V | first hold valued) 268/274, P(V | first hold neutral) 113/126; holding the valued odour at step 600 396/400
      reported: maintain P(V | first hold valued) 263/270, P(V | first hold neutral) 22/130; holding the valued odour at step 600 321/400
      reported: known-answer P(V | first hold valued) 386/400, P(V | first hold neutral) 0/0; holding the valued odour at step 600 400/400
      reported, secondary first reach, filter: V 207 N 192 none 1; P(V first) 207/400 = 0.517 [0.469, 0.566]
      reported, secondary first reach, maintain: V 201 N 199 none 0; P(V first) 201/400 = 0.502 [0.454, 0.551]
      reported, secondary first reach, pathway-off: V 199 N 201 none 0; P(V first) 199/400 = 0.497 [0.449, 0.546]
      reported, secondary first reach, known-answer: V 210 N 190 none 0; P(V first) 210/400 = 0.525 [0.476, 0.573]
   M3 identities: (i) maintain (Agent8, filter off) == ph19.Agent6 True; (ii) neutral with the filter == Agent6 True, Agent6 at 0/0 == G 0 True, G 0 == ph14.Agent3 True; priority-identity with the filter == Agent6 True, Agent6 at +1/-1 == ph16.Agent4 True; (iii) filter nav == valued whiff on every (row, step) True, filter positions and headings == Agent8 at G 0 gate off True; (iv) filter vs maintain bitwise equal up to the first `differs` step True {'never': 210, 'never_equal': 210, 'differ': 190, 'differ_pre_equal': 190, 'differ_equal_throughout': 0}; (v) known-answer h = valued and hit = its whiffs True -> PASS
   M4 mechanism bench, (a4), (b) and (c) re-run here with the bench seeds: (a4) lower bound 0.990 >= 0.95; (c) lower bound 0.990 >= 0.95 -> PASS; reported beside it, not a gate: (b) paired DP holding valued at 600 +0.1837 [+0.1475, +0.2200], bar lower bound > 0 -> PASS
   M5 avoidance: +1/-1 agent is Agent6 = the Run 2 agent by construction (M3 ii True); H21's constructed state: negative odour held on 300 (row, step), target = flee side on every one, equal to G 0's on the 300 steps both hold it; the valued odour took the hold on 250 afterwards -> PASS
   M6(a) no whiff of either plume in the last third, filter - maintain: DP n 400  value -0.010  95% interval [-0.020, -0.003]  at most 0.05 -> PASS
   M6(b) filter, wall contacts per row: mean 0.000  at most 0.10 -> PASS
   M6 -> PASS      reported: no whiff in the last third filter 0 maintain 4 known-answer 2; no navigation hit in the last third filter 13, maintain 12, pathway-off 7, known-answer 15, neutral 7, priority-identity 32; cast clock max filter 600 maintain 506; `differs` (row, step) filter 1206

== H23 ==  M1 PASS  M2 PASS  M3 PASS  M4 PASS  M5 PASS  M6 PASS  -> the rule steers only on a top-valued odour whatever is held, and with it the agent stays at the valued source in more rows than the H21 maintain agent, at P(V) of at least 0.88, without adding lost rows (value-driven navigation in the full agent; not selection controlling navigation); reported beside it, not part of it: bench (b) PASS

## Appendix B: ph21_bench.txt in full (sha256 1b836023eaceed95864bb402e3e324e1d727432d7beec7c4d8f6a184519b3330)

== H23 mechanism bench (design v2 section 4). design v2 FINAL doc db6df2e0013ab96e7 hash c19751f427363da9456a681659e23bf19bdb5463bdff966af99d04783bb30087; this file sha256 3a1d79d9a0d235f1bef7e435ec594cff4048180e27b28dcd892598c58413cfc1; {'rows': 400, 'rows_b': 800, 'p': 0.3, 'steps_stub': 200, 'steps_held': 260, 'steps': 600, 'seed_w': 20261001, 'seed_a': 20261002}; bootstrap seed 20261003 ==
   rows share no state: one generator per world and one per agent population, fixed-size draws consumed in row order every step
(a1) filt=False == Agent6 bitwise: stub +1/0 both channels p 0.3 200 steps (H, s, S, nav, since, target) True; the same with channel 1 held True; World7 task start 400 rows x 600 steps (positions, headings, circuit, H, nav) True
(a2) filt=True at 0/0 == Agent6 bitwise: stub True; World7 400 x 600 True; `differs` (row, step) 0
(a2) filt=True at +1/+1 == Agent6 bitwise: stub True; World7 400 x 600 True; `differs` (row, step) 0
(a2) filt=True at +1/-1 == Agent6 bitwise: stub True; World7 400 x 600 True; `differs` (row, step) 0
(a3) +1/0, channel 0 alone p 0.3 260 steps (the valued odour held): bitwise Agent6 True
   (a4) +1/0, channel 1 (value 0) held by construction (s 2.0), both channels p 0.3, 200 steps: nav == channel 0's whiff on every step in 400/400 = 1.000 [0.990, 1.000] (bar lower bound >= 0.95); channel 1 held on 5641 (row, step), nav True on 1579 of them, all with a channel-0 whiff True; Agent6 on the same draws: nav on channel-1-held steps from channel 1's whiff 1730
(a5) circuit independence at +1/0, World7 task start 400 x 600: positions and headings of Agent8 (G 2, gate on) == Agent8 at G 0 gate off True; == Agent8 with a neutral hold constructed at step 0 True; nav == valued whiff on every (row, step) in all three True; circuit states differ (G 2 vs G 0) True; holding valued at 600: 396 / 329 / 391
(b) task-like neutral-hold start (ph20b VARIANT state), 800 rows x 600 steps, Agent8 and Agent6 on the same rows and draws; REPORTED, not a gate
   [Agent8 (filter)] holding the valued odour at step 600: 217/800 = 0.271 [0.242, 0.303]; dwell majority V 18 N 782 tie 0; rows with a valued whiff 360, first valued whiff step quartiles 448/469/534; first surge on a valued whiff: rows 360, step quartiles 448/469/534, at the first valued whiff itself 360; first surge of any kind on a neutral-only whiff 0 rows, first surge step quartiles 448/469/534
      holds ended 409 (timeout flag 0, evidence 382, both 0, neither 27); no whiff of either plume in the last 100 steps 175; wall contacts 0; cast clock max 600; `differs` (row, step) 20781
   Agent8 (filter): holding valued against time
      step | holding valued at t        | ever revised by t | >=1 valued whiff by t | revised, not holding at t | a valued hold ended by t | P(holding | >=1 valued whiff)
       100 |   0/800 = 0.000                  |   0               |   0                   |   0                       |   0                      | nan
       150 |   0/800 = 0.000                  |   0               |   2                   |   0                       |   0                      | 0.000
       200 |   2/800 = 0.003                  |   2               |  16                   |   0                       |   0                      | 0.125
       250 |   4/800 = 0.005                  |   4               |  16                   |   0                       |   0                      | 0.250
       300 |  10/800 = 0.013 [0.007, 0.023]   |  10               |  50                   |   0                       |   0                      | 0.200
       400 |  24/800 = 0.030                  |  24               |  50                   |   0                       |   0                      | 0.480
       500 | 146/800 = 0.182                  | 146               | 210                   |   0                       |   0                      | 0.695
       600 | 217/800 = 0.271 [0.242, 0.303]   | 217               | 360                   |   0                       |   0                      | 0.603
   Agent8 (filter): revision route: transitions 0->N 127, 0->V 217, N->0 409
      first valued hold per row (217 rows): entered from nothing held 217, directly from the neutral hold 0
      'nothing held' stretches after a neutral hold: 409; ended by valued 217 (duration quartiles 5.0 / 8.0 / 18.0; valued whiffs in it mean 1.27, neutral whiffs mean 0.06); neutral again 127 (duration quartiles 9.0 / 18.0 / 24.5; valued whiffs in it mean 0.02, neutral whiffs mean 1.80); still nothing at the end 65 (duration quartiles 49.0 / 53.0 / 77.0; valued whiffs in it mean 0.00, neutral whiffs mean 0.18)
   [Agent6 (maintain)] holding the valued odour at step 600: 70/800 = 0.087 [0.070, 0.109]; dwell majority V 8 N 791 tie 1; rows with a valued whiff 91, first valued whiff step quartiles 370/483/526; first surge on a valued whiff: rows 72, step quartiles 384/500/532, at the first valued whiff itself 2; first surge of any kind on a neutral-only whiff 800 rows, first surge step quartiles 4/9/16
      holds ended 92 (timeout flag 0, evidence 91, both 0, neither 1); no whiff of either plume in the last 100 steps 257; wall contacts 0; cast clock max 394; `differs` (row, step) 0
   Agent6 (maintain): holding valued against time
      step | holding valued at t        | ever revised by t | >=1 valued whiff by t | revised, not holding at t | a valued hold ended by t | P(holding | >=1 valued whiff)
       100 |   0/800 = 0.000                  |   0               |   0                   |   0                       |   0                      | nan
       150 |   0/800 = 0.000                  |   0               |   0                   |   0                       |   0                      | nan
       200 |   0/800 = 0.000                  |   0               |   0                   |   0                       |   0                      | nan
       250 |   3/800 = 0.004                  |   3               |   8                   |   0                       |   0                      | 0.375
       300 |   4/800 = 0.005 [0.002, 0.013]   |   4               |   8                   |   0                       |   0                      | 0.500
       400 |  25/800 = 0.031                  |  25               |  37                   |   0                       |   0                      | 0.676
       500 |  33/800 = 0.041                  |  34               |  47                   |   1                       |   1                      | 0.702
       600 |  70/800 = 0.087 [0.070, 0.109]   |  71               |  91                   |   1                       |   1                      | 0.769
   Agent6 (maintain): revision route: transitions 0->N 15, 0->V 71, N->0 91, V->0 1
      first valued hold per row (71 rows): entered from nothing held 71, directly from the neutral hold 0
      'nothing held' stretches after a neutral hold: 91; ended by valued 71 (duration quartiles 5.0 / 7.0 / 14.0; valued whiffs in it mean 1.14, neutral whiffs mean 0.00); neutral again 14 (duration quartiles 11.0 / 21.5 / 44.0; valued whiffs in it mean 0.00, neutral whiffs mean 2.36); still nothing at the end 6 (duration quartiles 18.8 / 30.0 / 51.0; valued whiffs in it mean 0.00, neutral whiffs mean 0.67)
   Agent8 vs Agent6, same rows: positions first differ in 800/800 rows, step quartiles 4/9/16; Agent8's first `differs` step quartiles 4/9/16 (800 rows); holding valued at 600 both 22, Agent8 only 195, Agent6 only 48; dwell class into V 18, out of V 8
   (b) paired DP holding valued at 600, Agent8 - Agent6: +0.1837 [+0.1475, +0.2200] (bootstrap 5000, seed 20261003); bar lower bound > 0 -> PASS (REPORTED, not a gate; design v2 section 4)
(c) task start, nothing held, 400 rows x 600 steps, Agent8 and Agent6 on the same draws
   (c) Agent8: rows in which every nav step has a valued whiff 400/400 = 1.000 [0.990, 1.000] (bar lower bound >= 0.95)
      Agent8: first surge on valued only 384, neutral only 0, both 13, none 3; first hold valued 280 neutral 120 none 0, step median 13; dwell-majority P(V) 378/400 = 0.945 [0.918, 0.963] (preview, no bar); holding valued at 600 396
      Agent6: first surge on valued only 188, neutral only 205, both 7, none 0; first hold valued 265 neutral 135 none 0, step median 13; dwell-majority P(V) 290/400 = 0.725 [0.679, 0.766] (preview, no bar); holding valued at 600 323
      first hold identical row for row 377/400, and at the same step 337
(d) placed at the neutral source with a neutral hold (ph20.bench_d's state) on the H23 bench seeds, 400 rows x 600 steps (reported, no bar)
   (d) Agent8: holding the valued odour at 300 221/400 = 0.552 [0.504, 0.600]; at 600 305/400 = 0.762 [0.718, 0.802]; no whiff of either plume in the last 100 steps 69
   (d) Agent6: holding the valued odour at 300 8/400 = 0.020 [0.010, 0.039]; at 600 82/400 = 0.205 [0.168, 0.247]; no whiff of either plume in the last 100 steps 246
== M4: identities (a1, a2, a3, a5) True {'a1 stub': True, 'a1 stub, channel 1 held': True, 'a1 World7 +1/0': True, 'a2 0/0': True, 'a2 +1/+1': True, 'a2 +1/-1': True, 'a3': True, 'a5 G0 gate off': True, 'a5 neutral hold': True, 'a5 nav law': True}; (a4) lower bound 0.990 >= 0.95 -> PASS; (c) lower bound 0.990 >= 0.95 -> PASS -> M4 PASS: the task may be run; bench (b), reported beside it: PASS ==
