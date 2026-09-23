# H25 report: silence-timeout release (a reset-control change)

Date 2026-09-23. Design v2 FINAL doc dce297e76390fa854 (confirmed by the owner, decision:h25-open, '추천안으로 확정'; hash 6fbb293b...e60b, equal to the local file's sha256). Code ph24.py sha256 f344f178e20380858f4d7400ef670223f90aa2927b3f7304772ae1d848bd1bef (source doc d0c87ae7a68d1a27f, stored before the development run; its code block checked byte-equal to the file). One evaluation, world seed 1805, agent seed 1905, 400 rows x 600 steps, G 2, gate on where G 2, geometry C0, t0 150, 95 percent intervals, bootstrap 5000 seed 20261033, no extension. Evaluation output ph24_eval.txt sha256 79adb6bb721369b13ed872aae85f2fe89c9ff605c3ad502819ce52ea6aca576b. Nothing was changed after the table.

**Status: H25 SHOWN under its registered criteria: M1, M2, M3, M4, M5, M7 all PASS; M6 and M8 reported, not part of the PASS condition.** The printout's summary label is the registered verdict sentence. What it says: the sustained drive ends a hold whose odour has been silent for more than RESET_AFTER steps, leaves the circuit empty and ends no recently whiffed hold; with it the gate agent (Agent10g) tracks the remaining neutral odour after the valued odour is lost, at R 0.957 [0.895, 1.025] of the ceiling-floor span; in the adopted agent (Agent10 = the fix on Agent8) the change is behaviour-inert at +1/0 (trajectories bitwise Agent8's in every row of every world). **The reported cost M6 is large: in the H21 choice task the gate agent with the fix stays at the valued source in 0.575 of rows against 0.730 without it, DP -0.155 [-0.200, -0.113].** A statement about supplied values +1/0, G 2, C0, this reset control and these worlds; not about learning, other values, other geometries, or the adopted agent letting go of a lost valued odour in behaviour (it does not, by construction). Closure is the owner's.

## 1. What was asked

H25 (design v2 section 1): when the silence timeout fires on a held odour, sustain the existing reset drive (10.0) until both selection units are at or below threshold (S), and zero the silence counter on the step a hold forms (Z). Then (i) a hold ends within RESET_AFTER + 1 + D steps of its odour's last whiff, leaving the nothing-held state, and no hold whose odour was whiffed within RESET_AFTER steps is ended (implementation, M4 bench); (ii) in the agent whose navigation reads the hold (Agent10g = Release + ph19.Agent6) the agent tracks the remaining neutral odour after the valued odour is lost, as a share of a ceiling-floor span (M7), while in the adopted agent (Agent10 = Release + ph21.Agent8) the change is behaviour-inert at +1/0 (M2, M3, M5). The owner confirmed design v1 section 12 as recommended (nine points; decision:h25-open); M6, the cost in the gate agent on the H21 task, is a reported quantity.

## 2. Implementation, self-checks, bench, development run

ph24.py defines a `Release` mixin whose act calls the adopted act unchanged and then rewrites only the silence counter: to RESET_AFTER + 1 on a step where the timeout drive was delivered, no evidence release fired, no whiff of the held odour arrived and a unit is still above 1.0 (so the base's own line delivers 10.0 again next step); to 0 on a hold's formation step. `Agent10 = Release + Agent8`, `Agent10g = Release + Agent6`. No adopted module was edited and no act was copied; Circuit.step is untouched. The on/off flag is named `release` (not `fix`): ph14.Agent3 already owns `self.fix`, its H19 (a) switch. Bench (e) needed ph14b's own agent (Agent3, fix=False) with the release flags exposed: `Agent3x` reads the timeout flag before act (the base's expression) and the evidence flag at the circuit call from the arguments Agent3 passes (the ph14b instance-spy method); it reproduces Agent3 bitwise with the release off (demo).

**Implementation errors: none at run time; every self-check passed on the first run.** Four corrections were made on reading the code before its first execution, none changing a number: Agent3 has no `tgt` (recorded as 0 for the bench (e) agent); event arrays typed so an empty list cannot break `bincount`; two garbled expressions in the (d) row count and the demo's (Z) check rewritten; the demo prints, and does not assert, the release timing (a bench measurement; the H24 lesson).

**Found in implementation, flagged, not an amendment:** design section 4 (e) names 'Agent4 at G 0 with zero values, which is Agent3' as the agent that reproduces ph14b 1a. It does not: Agent4 is Agent3 with H19 (a) on, while ph14b's chain ran Agent3 with fix=False. The bench ran both: the design's agent gives 8796 timeout / 540 evidence requests (not 8652 / 761); ph14b's own agent reproduces 8652 / 761 exactly (median 1 / 3 steps, released 0.2% / 100%). The (e) bar passes in both. The reproduction is a construction statement, not one of the identities (a1)-(a5) in the no-candidate rule, so it did not stop the tasks; it is reported. Also: the design's T1 arm table does not list a priority-identity arm, so none was run.

**Self-checks (demo, ph24_demo.txt sha256 f17bef7b...3564):** release=False equals Agent8 / Agent6 bitwise, every field and the counter (World7 and stub); identity (b) holds on 40 x 200 World7 rows; Agent10's trajectory equals Agent8's; a constructed valued hold gets its first drive at step 41 in every row and sustain occurs only on drive steps with a unit above 1.0; (Z) acts only on formation steps; the bench (e) agents with the release off reproduce ph14.Agent3 fix=False and ph16.Agent4 G 0; T3a and T3b constructions; the seed scan (15 numbers, 143 files, none found; the reproduction seeds 1725/1825, 1765/1865, 9600/9700 reused on purpose and excluded from the scan by design).

**Mechanism bench (M4), ph24_bench.txt sha256 eb54ea1f...09b5, record:h25-bench-result: PASS.**
- (a) identities all True: (a0) release off == base bitwise (stub, World7, both agents); (a1) identity (b) separation on every stub protocol of (b) and (c), World7, W1, T3a, T3b, both pairs (e.g. World7 Agent10g vs Agent6: 398 rows with a base firing on a hold, equal before it; 2 rows without one, equal throughout); (a2) Agent10 == Agent8 in trajectory in T1, W1, T3a, T3b; (a3) Agent10g == Agent6 in trajectory in W1; (a4) T3b draws equal the World7 twin, each arm's T3b run equals its World7 run on steps 0-149, T3a start and hold as specified; (a5) reproduction: H21 maintain on 1725/1825 300/96/4, H23 filter on 1765/1865 381/14/5, Agent10 381 row for row, separation True on both.
- (b) constructed holds then silence: 400/400 = 1.000 [0.990, 1.000] in b1 (valued, Agent10g), b2 (neutral, Agent10g), b3 (valued, Agent10). First drive at step 41 in every row; **D = 7 in every row (predicted 4)**; the hold ends at step 47 (predicted 44; bar <= 49); no unit above 1.0 afterwards; global unit peak 11.17. The bases keep the hold 400/400 through 1600 one-step firings. (b4) H21 bench (a) protocol: Agent10g keeps the valued hold on every phase-2 step in 0/400 (Agent6 400/400); release 48 steps after the last channel-0 whiff in every row; the neutral odour is then held (step quartiles 120/122/124 at p 0.30, 134/156/176 in 377 rows at p 0.057).
- (c) no false release: 400/400 = 1.000 [0.990, 1.000] for valued and neutral holds at p 0.30 and 0.057. Legitimate releases (drive after >= 41 silent steps) per row at p 0.057: 2.147 (valued) and 1.982 (neutral) against feed gaps >= 41 per row 3.013 / 3.050 (expected 3.083); at p 0.30 none. Holding the fed odour at step 599 at p 0.057: 374 and 332 of 400 (base 400).
- (d) silent gaps (World7, bench seeds; reported): see section 5.
- (e) ph14b protocol: circuit empty at the end of every uninterrupted drive on a held unit, 1899/1899 (design's agent) and 1932/1932 (ph14b's agent) = 1.000 [0.998, 1.000]; D 7/7/7; the base's one-step drive empties the circuit in 1/8804 and 7/8666.
- T3a on bench seeds (restated before the development run; the bar did not move): ceiling 13.938, floor 0.750, span 13.188 [12.250, 14.160], per-row paired sd 9.545; M7(b) pass probability at R 0.9 1.000, at R 0.6 0.659.

**Development run (seeds 9896/9996, ph24_dev.txt sha256 fbd3caf3...cfa9d, record:h25-dev-run):** no operation error, no amendment. (Its printout read every criterion PASS; R 0.962; M6 -0.128. That printout is not the verdict.) Evaluation seeds unused until the one evaluation.

## 3. Results, one evaluation (seeds 1805 / 1905)

**T1, the H21 choice task (dwell majority).**

| arm | agent | values | V | N | tie | P(V) [95%] | first hold valued / neutral | P(V \| first valued) | P(V \| first neutral) |
|---|---|---|---|---|---|---|---|---|---|
| filter-fix | Agent10 | +1/0 | 384 | 14 | 2 | 0.960 [0.936, 0.975] | 273 / 127 | 267/273 | 117/127 |
| filter | Agent8 | +1/0 | 384 | 14 | 2 | 0.960 (identical row for row) | 273 / 127 | 267/273 | 117/127 |
| maintain-fix | Agent10g | +1/0 | 230 | 164 | 6 | 0.575 | 272 / 128 | 193/272 = 0.710 | 37/128 |
| maintain | Agent6 | +1/0 | 292 | 105 | 3 | 0.730 | 272 / 128 | 264/272 = 0.971 | 28/128 |
| pathway-off | Agent8 G 0, gate off, filter off | +1/0 | 194 | 202 | 4 | 0.485 (floor: P(V \| chose) 0.490) | 201 / 196 | 152/201 | 39/196 |
| known-answer | Agent5 fixed valued | +1/0 | 377 | 21 | 2 | 0.943 [0.915, 0.961] | 400 / 0 | 377/400 | - |
| neutral | Agent10 | 0/0 | 184 | 209 | 7 | 0.460 (side balance 0.545) | 201 / 196 | | |

Cells, filter-fix (V of 100): 96 / 95 / 98 / 95; maintain-fix 63 / 56 / 60 / 51; maintain 75 / 68 / 72 / 77. **Agent10 vs Agent8: positions, headings, nav, cast clock and target bitwise equal on every row (M2 a); DP +0.000; lost rows 2 vs 2 and contacts 0 vs 0, equal row for row.** Agent10g - Agent6 (M6, reported): DP -0.1550 [-0.2000, -0.1125]; into V 12, out of V 74; lost rows 7 vs 4, DP +0.0075 [-0.0050, +0.0200]; wall contacts 0 in every arm.

**T2, W1 (valued source silenced from step 0): identities.** Dwell at the present (neutral) source, mean: Agent10 12.133 = Agent8 12.133 row for row; Agent10g 25.435 = Agent6 25.435 row for row. Draws equal the twin in every arm.

**T3a, lost at the valued source (constructed).**

| arm | valued hold ended (step quartiles) | exact (<= 49, circuit empty) | neutral first held (step quartiles; rows) | first within 3.0 of the neutral source | dwell at the neutral source, 100-599, mean (quartiles) |
|---|---|---|---|---|---|
| Agent10g (maintain-fix) | 47 / 47 / 47 | 400/400 | 186 / 222 / 304; 309 | 198 / 240 / 310 | 13.300 (6 / 14 / 20) |
| floor: Agent6 | never (400) | 0/400 | never | 475 / 533 / 536 | 0.890 (0 / 0 / 0) |
| ceiling: Agent5 fixed neutral | - | - | fixed | | 13.857 (7 / 15 / 21) |
| Agent10 (filter-fix) | 47 / 47 / 47 | 400/400 | 185 / 196 / 247; 211 | 475 / 533 / 536 | 0.890 (= Agent8) |
| Agent8 (filter) | never (400) | 0/400 | never | 475 / 533 / 536 | 0.890 |

Span D_ceiling - D_floor 12.967 [12.070, 13.918]; **R = (13.300 - 0.890) / 12.967 = 0.9570 [0.8946, 1.0249].** Agent10 releases the hold exactly as Agent10g does, and its trajectory stays bitwise Agent8's: it releases and still does not follow the neutral odour (the filter steers on valued whiffs only; F3).

**T3b, sensed then lost (Lost, t0 150; reported).** Neutral dwell 400-599: Agent10g 6.830, Agent6 4.143, Agent10 1.972 = Agent8 1.972, ceiling (fixed valued then neutral from t0) 5.897; Agent10g - Agent6 +2.688 [+2.185, +3.185]; Agent10g - ceiling +0.933 [+0.267, +1.608]. Rows holding the valued odour at t0: Agent10g 80 (the fix had already let many valued holds go before t0), Agent6 272, Agent10 173, Agent8 317; in the fix arms every one of these holds ended, at 22/28/35 (Agent10g) and 16/22/29 (Agent10) steps after t0, 48 steps after the counter's origin in every row (80/80 and 173/173 <= +49); in the base arms none ended.

## 4. Criteria

- **M1 T1 validity: PASS.** Ties pathway-off 4/400, known-answer 2/400 (neutral 7/400, reported); side balance 214/393 = 0.545 [0.495, 0.593] within [0.35, 0.65]; floor 194/396 = 0.490 [0.441, 0.539] within [0.35, 0.65]; ceiling 377/400 = 0.943 [0.915, 0.961] >= 0.85.
- **M2 regression, adopted agent: PASS.** (a) Agent10's trajectory == Agent8's on every row: True. (b) Agent10 P(V) 384/400 = 0.960 [0.936, 0.975] >= 0.88.
- **M3 identities: PASS.** (a1) identity (b) separation, both pairs, in T1, W1, T3a, T3b (T1: every row has a base firing on a hold, first at step quartiles 58/78/80 and 55/78/81, all equal before it); (a2) Agent10 == Agent8 in trajectory in T1, W1, T3a, T3b; (a3) Agent10g == Agent6 in trajectory in W1; T2, T3a, T3b draws equal the twin; T3a start and hold; T3b == T1 on steps 0-149 in every arm, the ceiling included.
- **M4 mechanism bench: PASS** (section 2; re-run inside the evaluation with the bench seeds: identical lines).
- **M5 T2 regression: PASS.** Agent10 dwell == Agent8's row for row; Agent10g dwell == Agent6's row for row.
- **M6 (REPORTED, no bar):** DP = P(V) Agent10g - Agent6 -0.1550 [-0.2000, -0.1125]; predicted range [-0.18, 0], centre -0.05.
- **M7 T3a: PASS.** (a) Agent10g 400/400 = 1.000 [0.990, 1.000] >= 0.95; Agent10 400/400 [0.990, 1.000]. Readability: span lower bound 12.070 >= 5.0, readable. (b) R 0.9570 [0.8946, 1.0249] >= 0.50 (unrounded lower bound decides).
- **M8 T3b (REPORTED):** section 3.

**H25 under the registered criteria: SHOWN (M1 PASS; M2, M3, M4, M5, M7 PASS; M6 and M8 reported, not part of it).** Registered sentence, as printed: 'the sustained drive ends a hold whose odour is silent for more than RESET_AFTER steps, leaves the circuit empty and ends no recently whiffed hold, and with it the gate agent tracks the remaining neutral odour after the valued odour is lost, recovering at least half of the ceiling-floor span; in the adopted agent the change is behaviour-inert at +1/0'.

## 5. Where the release goes (measured; no cause named beyond what was measured)

- **Release steps per hold:** every timeout drive on a held unit lasted D = 7 steps (quartiles 7/7/7, max 7) in every arm, world, the stubs and the ph14b protocol; it starts after exactly 41 silent steps (quartiles 41/41/41, none stale) and ends the hold 48 steps after the held odour's last whiff or the hold's formation (T3b 80/80 and 173/173 rows; stub (b4) 48/48/48). Nothing-held firings stay one step (D > 1 among them: 0 in every arm), as section 3 (F1) requires.
- **Timeout firings against holds ended (T1):** Agent6 4323 firings on a hold, 0 holds ended (H21 recorded 4378 / 2); Agent8 4178, 0 (H23 filter recorded 4176 / 1, H23 maintain 4304 / 6). With the fix: Agent10g 1390 drives (9708 drive steps) on a hold, 1382 ended the hold, the circuit empty at each of those ends, 0 interrupted; Agent10 1468 drives (10248 steps), 1461 ended, 3 interrupted by a hit or the evidence release. Valued holds ended: Agent10 1312, Agent10g 944 (bases 0). (Z) lowered the counter 1432 (Agent10) and 1203 (Agent10g) times; the bases had 145 and 118 stale firings on a hold (a hold fired on fewer than 41 silent steps after its formation, F2).
- **Hold durations (T1):** with the fix quartiles 48/48/55 (Agent10) and 48/48/54 (Agent10g), 1736 and 1450 holds; the bases 306/568/590 and 381/578/591, 527 and 473 holds. Nothing held: Agent10 0.639 of steps, Agent10g 0.684, Agent8 0.075, Agent6 0.061. Held odour's silent gaps while held, >= 41: Agent6 0.335, Agent8 0.303 of gaps (bench seeds (d): 0.325 and 0.299; between two hits 0.289 and 0.260).
- **Agent10 vs Agent8 in T1:** by construction Agent8's navigation does not read the hold at +1/0; confirmed: trajectory fields equal on all 400 rows (M2 a), V class equal row for row, while the circuit records differ (1569 holds ended against 128; nothing held 0.639 against 0.075).
- **Agent10g vs Agent6 in T1 (M6):** the valued first hold no longer carries the row: P(V | first hold valued) 193/272 = 0.710 against 264/272 = 0.971; P(V | first hold neutral) 37/128 against 28/128; into V 12, out of V 74. Revision of a neutral first hold to valued 58/128 against 49/128. At the valued source Agent10g spent 3147 steps with nothing held (Agent6 108); at the neutral source 3109 with nothing held (Agent6 516). The empty state hands any non-negative whiff to navigation (ph19 line 63), so after a release the neutral plume pulls the agent; that is the cost the design named, at the low end of its range.
- **T3a:** release delay after the loss 47 steps in every row (both fixed agents); Agent10g first holds the neutral odour at step 222 (median, 309 rows) and first reaches the neutral source at 240; its neutral dwell 13.300 against the floor's 0.890 and the ceiling's 13.857; the ceiling-floor span 12.967; R 0.957.
- **T3b:** the fix raises Agent10g's late neutral dwell above Agent6's (+2.688) and above the ceiling's (+0.933; the ceiling holds the valued odour fixed until t0 and so starts its search later). Agent10's is Agent8's (1.972).

## 6. Predictions (design v2 section 10) against the observations

| prediction | observed | |
|---|---|---|
| bench (b) 400/400, ending at step 44 (D 4) | 400/400; ending at step 47 (D 7) | bar met; D and end step NOT met (7, not 4) |
| bench (b4) 0/400 kept (Agent6 400/400) | 0/400 (Agent6 400/400) | met |
| bench (c) no false release (by code) | 400/400 in all four conditions | met |
| bench (c) about 3.1 legitimate releases per row at p 0.057 | 2.147 (valued), 1.982 (neutral); feed gaps >= 41 3.01 / 3.05 | gaps met; releases fewer than gaps (not predicted separately) |
| bench (d) 4000-4400 base firings on a hold per arm | 4322 (Agent6), 4173 (Agent8) | met |
| bench (d) stale share: no recorded number; uniform arithmetic 0.37 of holds formed from nothing at p 0.057 exposed | stale firings 98 / 141 (2.3 / 3.4 percent of firings on a hold; 98 of 470 and 141 of 534 holds formed) | measured; lower than the arithmetic's exposure |
| bench (e) base reproduced exactly | ph14b's agent: exact; the design's agent (Agent4 G 0): not (8796 / 540) | met for ph14b's agent; the design named the wrong agent |
| bench (e) fix median D 4, 100% released | D 7/7/7; empty at the drive's end 100% | release met; D not met |
| T1 Agent10 = Agent8 row for row | trajectory bitwise equal, all rows | met |
| T1 Agent8 P(V) 0.93-0.97 on new seeds | 0.960 | met |
| T1 valued holds ended from about 0 to many | 0 -> 1312 (Agent10) | met |
| M6 DP in [-0.18, 0], centre -0.05 | -0.155 [-0.200, -0.113] | point in range, near its lower edge; interval extends past it |
| M6 conversion P(V \| first valued) within [0.718, 0.97] | 0.710 | NOT met: just below the lower edge (the design listed this as what would make the prediction wrong) |
| T2 identities; dwell order Agent8 12.3 < Agent6 25.8 | identities True; 12.133 < 25.435 | met |
| T3a M7(a) 400/400 at step 44 | 400/400 at step 47 | bar met; step not met |
| T3a R centre 0.9, lower edge 0.6 | 0.957 [0.895, 1.025] | met, above the centre |
| T3a Agent10 and Agent8 identical and blind to the neutral odour (D near the floor) | D 0.890 = the floor, identical | met |
| gate's 'never lost (0/280)' no longer true in either fixed agent | valued holds ended 1312 (Agent10), 944 (Agent10g) | met |
| T3b release <= +49 from the counter's origin | +48 in 80/80 and 173/173 | met |

## 7. What is shown and what is not

- **Shown (registered):** the reset control as specified ends every hold whose odour has been silent for more than RESET_AFTER steps (stub and task, D 7, the circuit empty at the end, no rebound), ends no hold earlier (no false release, 400/400 at p 0.30 and 0.057), and leaves nothing-held firings as they were; it is the base agent bitwise wherever the design says (release off; up to each row's first base firing on a hold; Agent10's trajectory everywhere; Agent10g in W1). In the gate agent, after a constructed loss at the valued source, it recovers R 0.957 [0.895, 1.025] of the span between an agent that never releases and one that tracks the neutral odour from the start.
- **Not shown:** that the adopted agent lets go of a lost valued odour in behaviour. **By construction Agent10's behaviour at +1/0 is Agent8's**: its circuit releases the hold (400/400 in T3a) but its navigation, steered by the value filter, keeps ignoring the neutral odour (T3a dwell 0.890 = the floor; T3b 1.972 = Agent8). For the adopted agent to track the remaining odour, the value filter must release as well: the H24 presence counter re-attempt (proposed by the interpreting assistant at the H24 closure) is the route, and it is **not decided**.
- **Measured, not a criterion:** the gate agent pays for the release in the choice task: P(V) 0.575 against 0.730 (M6), because its valued first hold now ends after 41 silent steps and the empty state hands the neutral plume to navigation. Whether that cost is acceptable, and in which agent the fix belongs, is not a question this design answers.
- **The design's D prediction was wrong (7, not 4):** ph14b 1b's committed state (s about 2 with 30 free steps) is not the agent's; the registered bound (<= 49 steps, D <= 8) held with one step to spare. The design's bench (e) agent was misnamed (section 2).
- **Not tested:** learning (H20 Stage B); other values, G, geometries or starts; another RESET_AFTER, amplitude or evidence release; the presence counter on top of the fix; a fly finding (none cited or claimed).

## 8. Provenance

- Design v2 FINAL doc dce297e76390fa854 (experiments/h25/h25_design_v2.md, sha256 6fbb293bfb14acbc941998ccc1b7934ec20d0b873131bf9c2ba90e925fcce60b); v1 DRAFT doc d3cb0794633a587ae (history); decision:h25-open-design, decision:h25-open.
- Code src/ph24.py sha256 f344f178e20380858f4d7400ef670223f90aa2927b3f7304772ae1d848bd1bef, source doc d0c87ae7a68d1a27f. Imported unchanged (sha256 in every output header): ph2 9e0ef833...0a4a, ph9 7699b4e6...9706, ph11 e80f40bd...7a23, ph13 2d75fae8...1f2d, ph14 c6b745c6...e0d0, ph14b ef18eff8...312e, ph15 cc939996...3fdc, ph16 33d5fdb2...a2c2, ph17 4b30ddf8...689f, ph18 26ad4def...97c3, ph19 00c6a3b3...4791, ph21 3a1d79d9...cfc1, ph22 03ab8c47...ca1c, ph23 ae180492...b5ae.
- Outputs (LF): ph24_demo.txt f17bef7bbb0e897adaafa946ce2d490d2bf753d64ea21ad5391b64f979683564; ph24_bench.txt eb54ea1fdefddac88c3e57a43fb09cfdc41ac575d483bec1c966f686df0009b5 (record:h25-bench-result); ph24_dev.txt fbd3caf3b5a990f17e6abca55da97e466c25e20e4a7dfff1cfc5389d908cfa9d (record:h25-dev-run); ph24_eval.txt 79adb6bb721369b13ed872aae85f2fe89c9ff605c3ad502819ce52ea6aca576b (record:h25-result).
- Seeds: development 9896/9996, evaluation 1805/1905 (now spent), bench 20261031/20261032, bootstrap 20261033; reused for reproduction and identity checks only: 9600/9700, 1725/1825, 1765/1865. Python 3.14.3, numpy 2.4.4.
- Closure is the owner's.

## Appendix A: ph24_eval.txt in full (sha256 79adb6bb721369b13ed872aae85f2fe89c9ff605c3ad502819ce52ea6aca576b)

```
== H25, EVAL. design v2 FINAL doc dce297e76390fa854 hash 6fbb293bfb14acbc941998ccc1b7934ec20d0b873131bf9c2ba90e925fcce60b; G 2.0, gate on where G 2; world seed 1805, agent seed 1905; 400 rows x 600 steps; geometry C0; t0 150; bootstrap seed 20261033; the one evaluation ==
   ph24.py sha256 f344f178e20380858f4d7400ef670223f90aa2927b3f7304772ae1d848bd1bef; design v2 FINAL doc dce297e76390fa854 hash 6fbb293bfb14acbc941998ccc1b7934ec20d0b873131bf9c2ba90e925fcce60b
   imported modules: ph2.py 9e0ef833d3f5957da341cfeb9edd77fe9adb11de5354c71162c7569e83e30a4a; ph9.py 7699b4e6fb47a1bee5f7e4e991a88aac8fa5af3a940297fbd4e441441f4d9706; ph11.py e80f40bd710aca43252f04329846ffa29943251d19e718450e9a7ff49e947a23; ph13.py 2d75fae8e8c31e1c6ddf6577782fafde3099f10fe8f50fe382f53d09e9ef1f2d; ph14.py c6b745c60f9992934a0ccbc5584ef354a03f53f08b37a1252a694feb350be0d0; ph14b.py ef18eff833ccf1600d39758d72a50bf670d7d2013d2137d4d16603f06d15312e; ph15.py cc9399965e5cbc30cb7f35e8ce296d8d43e4657cf644d1ec350931e594403fdc; ph16.py 33d5fdb25959fb7f9cbe465ca25a8973776b39f1e5170d645cb53bc8d906a2c2; ph17.py 4b30ddf8b1fc6dc510f23a28f09d6391003d95f0744344d237f50e3393a3689f; ph18.py 26ad4defb7590e16e1030b0b6f8073d3258584baeec06ba66e233315da7c97c3; ph19.py 00c6a3b32f80fae9f58b6dbd23a8e03b1710be45fcf335238f289567fce34791; ph21.py 3a1d79d9a0d235f1bef7e435ec594cff4048180e27b28dcd892598c58413cfc1; ph22.py 03ab8c4706b19557af5d64edd83f812abba91b618439618b35837a49dd44ca1c; ph23.py ae180492eece93739da4d1b5d83a13a2b42c5e952445a92ab75f95c6fb2eb5ae
   seeds: dev (9896, 9996), eval (1805, 1905), bench (20261031, 20261032), bootstrap 20261033; reproduction seeds {'h21': (1725, 1825), 'h23': (1765, 1865), 'h19': (9600, 9700)} reused on purpose, NOT part of the seed scan
   rows share no state: one generator per world and one per agent population, fixed-size draws consumed in row order every step

== T1, the H21 choice task ==

   [filter-fix] G 2.0  MAIN, dwell majority: V 384  N 14  tie 2  (of 400)
      cells: 0 odour A valued, +y: V 96 N 3 0 1 | 1 odour A valued, -y: V 95 N 5 0 0 | 2 odour B valued, +y: V 98 N 1 0 1 | 3 odour B valued, -y: V 95 N 5 0 0
      dwell median valued 25.0 other 0.0; both zero 0; majority source == first hold 277/400; P(V | first hold valued) 267/273; P(V | first hold neutral) 117/127
      H21 diag: dwell steps at valued (valued-held, neutral-held, nothing) (4784, 55, 5019) | at neutral (723, 749, 361); nothing held 0.639 of steps
      H21 diag: holds ended 1569 (on the timeout flag 1461, evidence 105, both 0, neither 3); held unit's s the step before, median 1.08; timeout firings while held 10248, of which ended the hold 1461; valued holds ended 1312, neutral holds ended 257
      H21 diag: revision, first hold neutral and later held valued 125/127 = 0.984; no whiff of either plume in the last third 2; no navigation hit in the last third 15; wall contacts per row 0.00
      [filter-fix] timeout drives started on a hold 1468 (drive steps delivered 10248), D quartiles 7/7/7, D max 7; ended the hold 1461; circuit empty at the drive's end 1461; interrupted by a hit or the evidence release 3; silent steps before the drive (quartiles) 41/41/41, stale (< 41) 0; nothing-held drives 2730 (D > 1 among them 0); counter lowered by (Z) 1432
      [filter-fix] holds 1736; duration quartiles 48/48/55 (ended within the run 1569); held odour's silent gaps while held 4625, quartiles 1/5/47, >= 41 1470 (0.3178)

   [filter] G 2.0  MAIN, dwell majority: V 384  N 14  tie 2  (of 400)
      cells: 0 odour A valued, +y: V 96 N 3 0 1 | 1 odour A valued, -y: V 95 N 5 0 0 | 2 odour B valued, +y: V 98 N 1 0 1 | 3 odour B valued, -y: V 95 N 5 0 0
      dwell median valued 25.0 other 0.0; both zero 0; majority source == first hold 277/400; P(V | first hold valued) 267/273; P(V | first hold neutral) 117/127
      H21 diag: dwell steps at valued (valued-held, neutral-held, nothing) (8621, 658, 579) | at neutral (782, 874, 177); nothing held 0.075 of steps
      H21 diag: holds ended 128 (on the timeout flag 0, evidence 127, both 0, neither 1); held unit's s the step before, median 1.06; timeout firings while held 4178, of which ended the hold 0; valued holds ended 0, neutral holds ended 128
      H21 diag: revision, first hold neutral and later held valued 123/127 = 0.969; no whiff of either plume in the last third 2; no navigation hit in the last third 15; wall contacts per row 0.00
      [filter] timeout drives started on a hold 4178 (drive steps delivered 4178), D quartiles 1/1/1, D max 1; ended the hold 0; circuit empty at the drive's end 0; interrupted by a hit or the evidence release 20; silent steps before the drive (quartiles) 41/82/123, stale (< 41) 145; nothing-held drives 236 (D > 1 among them 0); counter lowered by (Z) 0
      [filter] holds 527; duration quartiles 306/568/590 (ended within the run 128); held odour's silent gaps while held 4600, quartiles 1/4/111, >= 41 1393 (0.3028)

   [maintain-fix] G 2.0  MAIN, dwell majority: V 230  N 164  tie 6  (of 400)
      cells: 0 odour A valued, +y: V 63 N 37 0 0 | 1 odour A valued, -y: V 56 N 44 0 0 | 2 odour B valued, +y: V 60 N 37 0 3 | 3 odour B valued, -y: V 51 N 46 0 3
      dwell median valued 16.0 other 11.0; both zero 0; majority source == first hold 284/400; P(V | first hold valued) 193/272; P(V | first hold neutral) 37/128
      H21 diag: dwell steps at valued (valued-held, neutral-held, nothing) (3161, 119, 3147) | at neutral (741, 1346, 3109); nothing held 0.684 of steps
      H21 diag: holds ended 1401 (on the timeout flag 1382, evidence 19, both 0, neither 0); held unit's s the step before, median 1.07; timeout firings while held 9708, of which ended the hold 1382; valued holds ended 944, neutral holds ended 457
      H21 diag: revision, first hold neutral and later held valued 58/128 = 0.453; no whiff of either plume in the last third 7; no navigation hit in the last third 7; wall contacts per row 0.00
      [maintain-fix] timeout drives started on a hold 1390 (drive steps delivered 9708), D quartiles 7/7/7, D max 7; ended the hold 1382; circuit empty at the drive's end 1382; interrupted by a hit or the evidence release 0; silent steps before the drive (quartiles) 41/41/41, stale (< 41) 0; nothing-held drives 3086 (D > 1 among them 0); counter lowered by (Z) 1203
      [maintain-fix] holds 1450; duration quartiles 48/48/54 (ended within the run 1401); held odour's silent gaps while held 3504, quartiles 1/6/47, >= 41 1392 (0.3973)

   [maintain] G 2.0  MAIN, dwell majority: V 292  N 105  tie 3  (of 400)
      cells: 0 odour A valued, +y: V 75 N 23 0 2 | 1 odour A valued, -y: V 68 N 32 0 0 | 2 odour B valued, +y: V 72 N 27 0 1 | 3 odour B valued, -y: V 77 N 23 0 0
      dwell median valued 20.0 other 6.0; both zero 0; majority source == first hold 363/400; P(V | first hold valued) 264/272; P(V | first hold neutral) 28/128
      H21 diag: dwell steps at valued (valued-held, neutral-held, nothing) (7185, 123, 108) | at neutral (840, 2176, 516); nothing held 0.061 of steps
      H21 diag: holds ended 73 (on the timeout flag 0, evidence 70, both 0, neither 3); held unit's s the step before, median 1.06; timeout firings while held 4323, of which ended the hold 0; valued holds ended 0, neutral holds ended 73
      H21 diag: revision, first hold neutral and later held valued 49/128 = 0.383; no whiff of either plume in the last third 4; no navigation hit in the last third 12; wall contacts per row 0.00
      [maintain] timeout drives started on a hold 4323 (drive steps delivered 4323), D quartiles 1/1/1, D max 1; ended the hold 0; circuit empty at the drive's end 0; interrupted by a hit or the evidence release 16; silent steps before the drive (quartiles) 41/82/123, stale (< 41) 118; nothing-held drives 181 (D > 1 among them 0); counter lowered by (Z) 0
      [maintain] holds 473; duration quartiles 381/578/591 (ended within the run 73); held odour's silent gaps while held 4220, quartiles 1/5/143, >= 41 1412 (0.3346)

   [pathway-off] G 0.0  MAIN, dwell majority: V 194  N 202  tie 4  (of 400)
      cells: 0 odour A valued, +y: V 46 N 51 0 3 | 1 odour A valued, -y: V 44 N 55 0 1 | 2 odour B valued, +y: V 53 N 47 0 0 | 3 odour B valued, -y: V 51 N 49 0 0
      dwell median valued 12.0 other 13.0; both zero 0; majority source == first hold 308/397; P(V | first hold valued) 152/201; P(V | first hold neutral) 39/196
      H21 diag: dwell steps at valued (valued-held, neutral-held, nothing) (3494, 123, 1625) | at neutral (125, 3943, 1518); nothing held 0.231 of steps
      H21 diag: holds ended 239 (on the timeout flag 10, evidence 213, both 0, neither 16); held unit's s the step before, median 1.06; timeout firings while held 3714, of which ended the hold 10; valued holds ended 129, neutral holds ended 110
      H21 diag: revision, first hold neutral and later held valued 61/196 = 0.311; no whiff of either plume in the last third 9; no navigation hit in the last third 9; wall contacts per row 0.00

   [known-answer] G 0.0 (held odour fixed to the valued odour)  MAIN, dwell majority: V 377  N 21  tie 2  (of 400)
      cells: 0 odour A valued, +y: V 98 N 2 0 0 | 1 odour A valued, -y: V 92 N 8 0 0 | 2 odour B valued, +y: V 95 N 3 0 2 | 3 odour B valued, -y: V 92 N 8 0 0
      dwell median valued 25.0 other 0.0; both zero 0; majority source == first hold 377/400; P(V | first hold valued) 377/400; P(V | first hold neutral) 0/0
      H21 diag: dwell steps at valued (valued-held, neutral-held, nothing) (9778, 0, 0) | at neutral (1987, 0, 0); nothing held 0.000 of steps
      H21 diag: holds ended 0 (on the timeout flag 0, evidence 0, both 0, neither 0); held unit's s the step before, median nan; timeout firings while held 0, of which ended the hold 0; valued holds ended 0, neutral holds ended 0
      H21 diag: revision, first hold neutral and later held valued 0/0; no whiff of either plume in the last third 3; no navigation hit in the last third 12; wall contacts per row 0.00

   [neutral] G 2.0  MAIN, dwell majority: V 184  N 209  tie 7  (of 400)
      cells: 0 odour A valued, +y: V 51 N 48 0 1 | 1 odour A valued, -y: V 42 N 57 0 1 | 2 odour B valued, +y: V 50 N 48 0 2 | 3 odour B valued, -y: V 41 N 56 0 3
      dwell median valued 13.0 other 15.0; both zero 0; majority source == first hold 274/397; P(V | first hold valued) 130/201; P(V | first hold neutral) 51/196
      H21 diag: dwell steps at valued (valued-held, neutral-held, nothing) (1427, 119, 3901) | at neutral (106, 1480, 4269); nothing held 0.770 of steps
      H21 diag: holds ended 1065 (on the timeout flag 1026, evidence 39, both 0, neither 0); held unit's s the step before, median 1.06; timeout firings while held 7231, of which ended the hold 1026; valued holds ended 504, neutral holds ended 561
      H21 diag: revision, first hold neutral and later held valued 77/196 = 0.393; no whiff of either plume in the last third 7; no navigation hit in the last third 7; wall contacts per row 0.00
      [neutral] timeout drives started on a hold 1038 (drive steps delivered 7231), D quartiles 7/7/7, D max 7; ended the hold 1026; circuit empty at the drive's end 1026; interrupted by a hit or the evidence release 0; silent steps before the drive (quartiles) 41/41/41, stale (< 41) 0; nothing-held drives 3683 (D > 1 among them 0); counter lowered by (Z) 941
      [neutral] holds 1088; duration quartiles 48/48/53 (ended within the run 1065); held odour's silent gaps while held 2357, quartiles 1/9/47, >= 41 1038 (0.4404)

== T2, the absent-odour world W1 (valued source silenced from step 0) ==
   [W1 filter-fix] dwell at the neutral (present) source mean 12.133, quartiles 6.0/9.0/16.2; rows reaching it 348; draws == twin True
      [W1 filter-fix] timeout drives started on a hold 844 (drive steps delivered 5781), D quartiles 7/7/7, D max 7; ended the hold 806; circuit empty at the drive's end 806; interrupted by a hit or the evidence release 9; silent steps before the drive (quartiles) 41/41/41, stale (< 41) 0; nothing-held drives 3835 (D > 1 among them 0); counter lowered by (Z) 796
      [W1 filter-fix] holds 937; duration quartiles 48/54/69 (ended within the run 807); held odour's silent gaps while held 3182, quartiles 1/5/47, >= 41 850 (0.2671)
   [W1 filter] dwell at the neutral (present) source mean 12.133, quartiles 6.0/9.0/16.2; rows reaching it 348; draws == twin True
      [W1 filter] timeout drives started on a hold 3602 (drive steps delivered 3602), D quartiles 1/1/1, D max 1; ended the hold 6; circuit empty at the drive's end 6; interrupted by a hit or the evidence release 36; silent steps before the drive (quartiles) 41/82/164, stale (< 41) 136; nothing-held drives 964 (D > 1 among them 0); counter lowered by (Z) 0
      [W1 filter] holds 391; duration quartiles 471/550/578 (ended within the run 17); held odour's silent gaps while held 4403, quartiles 2/5/49, >= 41 1164 (0.2644)
   [W1 maintain-fix] dwell at the neutral (present) source mean 25.435, quartiles 20.0/25.0/31.0; rows reaching it 396; draws == twin True
      [W1 maintain-fix] timeout drives started on a hold 893 (drive steps delivered 6238), D quartiles 7/7/7, D max 7; ended the hold 890; circuit empty at the drive's end 890; interrupted by a hit or the evidence release 0; silent steps before the drive (quartiles) 41/41/41, stale (< 41) 0; nothing-held drives 3931 (D > 1 among them 0); counter lowered by (Z) 860
      [W1 maintain-fix] holds 976; duration quartiles 48/48/51 (ended within the run 890); held odour's silent gaps while held 2044, quartiles 1/10/48, >= 41 895 (0.4379)
   [W1 maintain] dwell at the neutral (present) source mean 25.435, quartiles 20.0/25.0/31.0; rows reaching it 396; draws == twin True
      [W1 maintain] timeout drives started on a hold 3567 (drive steps delivered 3567), D quartiles 1/1/1, D max 1; ended the hold 11; circuit empty at the drive's end 11; interrupted by a hit or the evidence release 8; silent steps before the drive (quartiles) 41/82/123, stale (< 41) 200; nothing-held drives 1230 (D > 1 among them 0); counter lowered by (Z) 0
      [W1 maintain] holds 418; duration quartiles 321/481/575 (ended within the run 26); held odour's silent gaps while held 3296, quartiles 1/4/147, >= 41 1119 (0.3395)

== T3a, lost at the valued source (constructed: valued column masked from step 0, start at the valued source, valued hold s 2.0) ==
   [T3a maintain-fix] dwell at the neutral source, steps 100-599: mean 13.300, quartiles 6.0/14.0/20.0, rows > 0 319; valued hold ended at step quartiles 47/47/47 (never 0), exact (<= 49, circuit empty) 400/400; neutral first held at step 186/222/304 (rows 309); first within 3.0 of the neutral source 198/240/310
      [T3a maintain-fix] timeout drives started on a hold 963 (drive steps delivered 6705), D quartiles 7/7/7, D max 7; ended the hold 951; circuit empty at the drive's end 951; interrupted by a hit or the evidence release 0; silent steps before the drive (quartiles) 41/41/41, stale (< 41) 0; nothing-held drives 4117 (D > 1 among them 0); counter lowered by (Z) 513
      [T3a maintain-fix] holds 994; duration quartiles 47/48/50 (ended within the run 951); held odour's silent gaps while held 1982, quartiles 1/16/47, >= 41 966 (0.4874)
   [T3a maintain] dwell at the neutral source, steps 100-599: mean 0.890, quartiles 0.0/0.0/0.0, rows > 0 62; valued hold ended at step quartiles n/a (never 400), exact (<= 49, circuit empty) 0/400; neutral first held at step n/a (rows 0); first within 3.0 of the neutral source 475/533/536
      [T3a maintain] timeout drives started on a hold 5600 (drive steps delivered 5600), D quartiles 1/1/1, D max 1; ended the hold 0; circuit empty at the drive's end 0; interrupted by a hit or the evidence release 0; silent steps before the drive (quartiles) 164/308/451, stale (< 41) 0; nothing-held drives 0 (D > 1 among them 0); counter lowered by (Z) 0
      [T3a maintain] holds 400; duration quartiles 600/600/600 (ended within the run 0); held odour's silent gaps while held 400, quartiles 600/600/600, >= 41 400 (1.0000)
   [T3a filter-fix] dwell at the neutral source, steps 100-599: mean 0.890, quartiles 0.0/0.0/0.0, rows > 0 62; valued hold ended at step quartiles 47/47/47 (never 0), exact (<= 49, circuit empty) 400/400; neutral first held at step 185/196/247 (rows 211); first within 3.0 of the neutral source 475/533/536
      [T3a filter-fix] timeout drives started on a hold 791 (drive steps delivered 5414), D quartiles 7/7/7, D max 7; ended the hold 753; circuit empty at the drive's end 753; interrupted by a hit or the evidence release 37; silent steps before the drive (quartiles) 41/41/41, stale (< 41) 0; nothing-held drives 4510 (D > 1 among them 0); counter lowered by (Z) 326
      [T3a filter-fix] holds 763; duration quartiles 47/47/48 (ended within the run 762); held odour's silent gaps while held 1093, quartiles 9/47/47, >= 41 791 (0.7237)
   [T3a filter] dwell at the neutral source, steps 100-599: mean 0.890, quartiles 0.0/0.0/0.0, rows > 0 62; valued hold ended at step quartiles n/a (never 400), exact (<= 49, circuit empty) 0/400; neutral first held at step n/a (rows 0); first within 3.0 of the neutral source 475/533/536
      [T3a filter] timeout drives started on a hold 5600 (drive steps delivered 5600), D quartiles 1/1/1, D max 1; ended the hold 0; circuit empty at the drive's end 0; interrupted by a hit or the evidence release 0; silent steps before the drive (quartiles) 164/308/451, stale (< 41) 0; nothing-held drives 0 (D > 1 among them 0); counter lowered by (Z) 0
      [T3a filter] holds 400; duration quartiles 600/600/600 (ended within the run 0); held odour's silent gaps while held 400, quartiles 600/600/600, >= 41 400 (1.0000)
   [T3a ceiling] dwell at the neutral source, steps 100-599: mean 13.857, quartiles 7.0/15.0/21.0, rows > 0 319

== T3b, sensed then lost (ph23.Lost, valued column masked from t0 150; reported) ==
   [T3b maintain-fix] dwell at the neutral source, steps 400-599: mean 6.830, quartiles 3.0/6.0/10.0; holding the valued odour at t0 80/400; its hold ended in 80 (never 0), step after t0 quartiles 22/28/35, relative to the counter's origin quartiles 48/48/48, <= +49 80/80
   [T3b maintain] dwell at the neutral source, steps 400-599: mean 4.143, quartiles 0.0/0.5/8.0; holding the valued odour at t0 272/400; its hold ended in 0 (never 272), step after t0 quartiles n/a, relative to the counter's origin quartiles n/a, <= +49 0/0
   [T3b filter-fix] dwell at the neutral source, steps 400-599: mean 1.972, quartiles 0.0/0.0/1.2; holding the valued odour at t0 173/400; its hold ended in 173 (never 0), step after t0 quartiles 16/22/29, relative to the counter's origin quartiles 48/48/48, <= +49 173/173
   [T3b filter] dwell at the neutral source, steps 400-599: mean 1.972, quartiles 0.0/0.0/1.2; holding the valued odour at t0 317/400; its hold ended in 0 (never 317), step after t0 quartiles n/a, relative to the counter's origin quartiles n/a, <= +49 0/0
   [T3b ceiling] dwell at the neutral source, steps 400-599: mean 5.897, quartiles 1.0/5.0/9.0

== criteria (design v2 FINAL section 7; 95 percent, one evaluation, no extension; aggregation: PASS if every part passes, FAIL if any fails, else INCONCLUSIVE) ==
   M1(a) pathway-off: ties 4/400 = 0.010  at most 0.20 -> PASS
   M1(a) known-answer: ties 2/400 = 0.005  at most 0.20 -> PASS
      reported: neutral ties 7/400
   M1(b) neutral, P(+y source majority | chose): P k 214 n 393  value 0.545  95% interval [0.495, 0.593]  within [0.35, 0.65] -> PASS
   M1(c) floor: pathway-off, P(V | chose): P k 194 n 396  value 0.490  95% interval [0.441, 0.539]  within [0.35, 0.65] -> PASS
   M1(d) ceiling: known-answer, P(V) over all rows: P k 377 n 400  value 0.943  95% interval [0.915, 0.961]  at least 0.85 -> PASS
   M1 -> PASS
   M2(a) Agent10 trajectory == Agent8's on every row (POS, HEAD, NAV, SINCE, TGT): True -> PASS
   M2(b) Agent10 (filter-fix), P(V) over all rows: P k 384 n 400  value 0.960  95% interval [0.936, 0.975]  at least 0.88 -> PASS
   M2 -> PASS
      reported: DP Agent10 - Agent8 +0.000 [+0.000, +0.000]; lost rows (no whiff of either plume in the last third) 2 vs 2, equal row for row True; wall contacts 0 vs 0, equal row for row True
      M3 (a1) T1 filter-fix vs filter: True {'rows_without_firing': 0, 'with_firing': 400, 'with_firing_equal_throughout': 0, 'first_firing_step': '58/78/80'}
      M3 (a1) T1 maintain-fix vs maintain: True {'rows_without_firing': 0, 'with_firing': 400, 'with_firing_equal_throughout': 0, 'first_firing_step': '55/78/81'}
      M3 (a1) W1 filter-fix vs filter: True {'rows_without_firing': 24, 'with_firing': 376, 'with_firing_equal_throughout': 0, 'first_firing_step': '76/82/177'}
      M3 (a1) W1 maintain-fix vs maintain: True {'rows_without_firing': 11, 'with_firing': 389, 'with_firing_equal_throughout': 0, 'first_firing_step': '78/84/205'}
      M3 (a1) T3a filter-fix vs filter: True {'rows_without_firing': 0, 'with_firing': 400, 'with_firing_equal_throughout': 0, 'first_firing_step': '41/41/41'}
      M3 (a1) T3a maintain-fix vs maintain: True {'rows_without_firing': 0, 'with_firing': 400, 'with_firing_equal_throughout': 0, 'first_firing_step': '41/41/41'}
      M3 (a1) T3b filter-fix vs filter: True {'rows_without_firing': 1, 'with_firing': 399, 'with_firing_equal_throughout': 0, 'first_firing_step': '58/78/80'}
      M3 (a1) T3b maintain-fix vs maintain: True {'rows_without_firing': 1, 'with_firing': 399, 'with_firing_equal_throughout': 0, 'first_firing_step': '55/78/81'}
   M3 identities: (a1) T1 filter-fix vs filter True; (a1) T1 maintain-fix vs maintain True; (a2) T1 Agent10 == Agent8 trajectory True; (a1) W1 filter-fix vs filter True; (a1) W1 maintain-fix vs maintain True; (a2) W1 Agent10 == Agent8 trajectory True; (a1) T3a filter-fix vs filter True; (a1) T3a maintain-fix vs maintain True; (a2) T3a Agent10 == Agent8 trajectory True; (a1) T3b filter-fix vs filter True; (a1) T3b maintain-fix vs maintain True; (a2) T3b Agent10 == Agent8 trajectory True; (a3) W1 Agent10g == Agent6 trajectory True; T2 draws True; T3a draws, start, hold True; T3b draws True; T3b == T1 before t0 True -> PASS
   M4 mechanism bench, re-run here with the bench seeds (section 4); its lines:
      (b1 valued hold, Agent10g) exact 400/400 = 1.000 [0.990, 1.000] -> PASS; end step quartiles 47/47/47 (never 0); first drive step quartiles 41/41/41; D per row quartiles 7/7/7, max 7; S peak median 11.17 max 11.17; base (Agent6) holding at step 199: 400/400, its timeout firings 1600
      (b2 neutral hold, Agent10g) exact 400/400 = 1.000 [0.990, 1.000] -> PASS; end step quartiles 47/47/47 (never 0); first drive step quartiles 41/41/41; D per row quartiles 7/7/7, max 7; S peak median 11.17 max 11.17; base (Agent6) holding at step 199: 400/400, its timeout firings 1600
      (b3 valued hold, Agent10) exact 400/400 = 1.000 [0.990, 1.000] -> PASS; end step quartiles 47/47/47 (never 0); first drive step quartiles 41/41/41; D per row quartiles 7/7/7, max 7; S peak median 11.17 max 11.17; base (Agent8) holding at step 199: 400/400, its timeout firings 1600
      (b4) H21 bench (a) protocol, Agent10g, channel 1 p 0.3: holding channel 0 at step 60 400/400; kept on every phase-2 step 0/400; release step after the last channel-0 whiff, quartiles 48/48/48; step the neutral odour is held, quartiles 120/122/124 (rows 400)
      (b4) H21 bench (a) protocol, Agent6, channel 1 p 0.3: holding channel 0 at step 60 400/400; kept on every phase-2 step 400/400; release step after the last channel-0 whiff, quartiles n/a; step the neutral odour is held, quartiles n/a (rows 0)
      (b4) H21 bench (a) protocol, Agent10g, channel 1 p 0.057: holding channel 0 at step 60 400/400; kept on every phase-2 step 0/400; release step after the last channel-0 whiff, quartiles 48/48/48; step the neutral odour is held, quartiles 134/156/176 (rows 377)
      (b4) H21 bench (a) protocol, Agent6, channel 1 p 0.057: holding channel 0 at step 60 400/400; kept on every phase-2 step 400/400; release step after the last channel-0 whiff, quartiles n/a; step the neutral odour is held, quartiles n/a (rows 0)
      (valued hold, p 0.3) rows with no false release 400/400 = 1.000 [0.990, 1.000] -> PASS; legitimate releases (drive after >= 41 silent steps) per row mean 0.000 (rows with any 0); feed gaps >= 41 per row mean 0.000 (expected 0.0001); holding the fed odour at step 599: fix 400, base 400; drive D quartiles n/a
      (valued hold, p 0.057) rows with no false release 400/400 = 1.000 [0.990, 1.000] -> PASS; legitimate releases (drive after >= 41 silent steps) per row mean 2.147 (rows with any 373); feed gaps >= 41 per row mean 3.013 (expected 3.0832); holding the fed odour at step 599: fix 374, base 400; drive D quartiles 6/7/7
      (neutral hold, p 0.3) rows with no false release 400/400 = 1.000 [0.990, 1.000] -> PASS; legitimate releases (drive after >= 41 silent steps) per row mean 0.000 (rows with any 0); feed gaps >= 41 per row mean 0.000 (expected 0.0001); holding the fed odour at step 599: fix 400, base 400; drive D quartiles n/a
      (neutral hold, p 0.057) rows with no false release 400/400 = 1.000 [0.990, 1.000] -> PASS; legitimate releases (drive after >= 41 silent steps) per row mean 1.982 (rows with any 368); feed gaps >= 41 per row mean 3.050 (expected 3.0832); holding the fed odour at step 599: fix 332, base 400; drive D quartiles 5/7/7
      base reproduces ph14b 1a (8652 timeout / 761 evidence requests): False  | fix bar: circuit empty at the end of an uninterrupted drive, lower bound 0.998 >= 0.95 -> PASS
      base reproduces ph14b 1a (8652 timeout / 761 evidence requests): True  | fix bar: circuit empty at the end of an uninterrupted drive, lower bound 0.998 >= 0.95 -> PASS
      == M4: identities (a0-a5) True; failed: []; bars (b) True (lower bounds [np.float64(0.9905), np.float64(0.9905), np.float64(0.9905)]), (c) True ([np.float64(0.9905), np.float64(0.9905), np.float64(0.9905), np.float64(0.9905)]), (e) True ([np.float64(0.998), np.float64(0.998)]); (e) base reproduces ph14b 1a: [('Agent4', False), ('Agent3', True)] (reported) -> M4 PASS: the tasks may be run ==
   M4 -> PASS
   M5(a) W1 Agent10 dwell == Agent8's row for row True; M5(b) W1 Agent10g dwell == Agent6's row for row True -> PASS   (means: Agent10 12.133, Agent8 12.133, Agent10g 25.435, Agent6 25.435)
   M6 (REPORTED, no bar; not part of the PASS condition): DP = P(V) Agent10g - Agent6 -0.1550 [-0.2000, -0.1125] (P(V) 0.575 vs 0.730; predicted [-0.18, 0], centre -0.05); into V 12, out of V 74; lost rows 7 vs 4, DP +0.0075 [-0.0050, +0.0200]; contacts per row 0.000 vs 0.000, DP +0.0000 [+0.0000, +0.0000]
   M7(a) T3a maintain-fix (Agent10g): valued hold ends at a step <= 49 with both units <= 1.0, rows exact: P k 400 n 400  value 1.000  95% interval [0.990, 1.000]  at least 0.95 -> PASS
   M7(a) T3a filter-fix (Agent10): valued hold ends at a step <= 49 with both units <= 1.0, rows exact: P k 400 n 400  value 1.000  95% interval [0.990, 1.000]  at least 0.95 -> PASS
   M7(b) readability: span D_ceiling - D_floor = 13.857 - 0.890 = 12.967 [12.070, 13.918], lower bound >= 5.0 -> readable
   M7(b) R = (D_Agent10g - D_floor) / (D_ceiling - D_floor) = (13.300 - 0.890) / 12.967 = 0.9570 [0.8946, 1.0249] (bootstrap 5000, rows resampled together, seed 20261033); at least 0.50 -> PASS
   M7 -> PASS
   M8 T3b (REPORTED): neutral dwell 400-599 Agent10g 6.830, Agent6 4.143, Agent10 1.972, Agent8 1.972, ceiling 5.897; Agent10g - Agent6 +2.688 [+2.185, +3.185]; Agent10g - ceiling +0.933 [+0.267, +1.608]

== H25 ==  M1 PASS  M2 PASS  M3 PASS  M4 PASS  M5 PASS  M7 PASS  (M6, M8 reported) -> H25 SHOWN under its registered criteria: the sustained drive ends a hold whose odour is silent for more than RESET_AFTER steps, leaves the circuit empty and ends no recently whiffed hold, and with it the gate agent tracks the remaining neutral odour after the valued odour is lost, recovering at least half of the ceiling-floor span; in the adopted agent the change is behaviour-inert at +1/0
```

## Appendix B: ph24_bench.txt in full (sha256 eb54ea1fdefddac88c3e57a43fb09cfdc41ac575d483bec1c966f686df0009b5)

```
== H25 mechanism bench (design v2 section 4). design v2 FINAL doc dce297e76390fa854 hash 6fbb293bfb14acbc941998ccc1b7934ec20d0b873131bf9c2ba90e925fcce60b; this file sha256 f344f178e20380858f4d7400ef670223f90aa2927b3f7304772ae1d848bd1bef; {'rows': 400, 'steps_b': 200, 'steps_c': 600, 'steps': 600, 'seed_w': 20261031, 'seed_a': 20261032}; bootstrap seed 20261033 ==
   ph24.py sha256 f344f178e20380858f4d7400ef670223f90aa2927b3f7304772ae1d848bd1bef; design v2 FINAL doc dce297e76390fa854 hash 6fbb293bfb14acbc941998ccc1b7934ec20d0b873131bf9c2ba90e925fcce60b
   imported modules: ph2.py 9e0ef833d3f5957da341cfeb9edd77fe9adb11de5354c71162c7569e83e30a4a; ph9.py 7699b4e6fb47a1bee5f7e4e991a88aac8fa5af3a940297fbd4e441441f4d9706; ph11.py e80f40bd710aca43252f04329846ffa29943251d19e718450e9a7ff49e947a23; ph13.py 2d75fae8e8c31e1c6ddf6577782fafde3099f10fe8f50fe382f53d09e9ef1f2d; ph14.py c6b745c60f9992934a0ccbc5584ef354a03f53f08b37a1252a694feb350be0d0; ph14b.py ef18eff833ccf1600d39758d72a50bf670d7d2013d2137d4d16603f06d15312e; ph15.py cc9399965e5cbc30cb7f35e8ce296d8d43e4657cf644d1ec350931e594403fdc; ph16.py 33d5fdb25959fb7f9cbe465ca25a8973776b39f1e5170d645cb53bc8d906a2c2; ph17.py 4b30ddf8b1fc6dc510f23a28f09d6391003d95f0744344d237f50e3393a3689f; ph18.py 26ad4defb7590e16e1030b0b6f8073d3258584baeec06ba66e233315da7c97c3; ph19.py 00c6a3b32f80fae9f58b6dbd23a8e03b1710be45fcf335238f289567fce34791; ph21.py 3a1d79d9a0d235f1bef7e435ec594cff4048180e27b28dcd892598c58413cfc1; ph22.py 03ab8c4706b19557af5d64edd83f812abba91b618439618b35837a49dd44ca1c; ph23.py ae180492eece93739da4d1b5d83a13a2b42c5e952445a92ab75f95c6fb2eb5ae
   seeds: dev (9896, 9996), eval (1805, 1905), bench (20261031, 20261032), bootstrap 20261033; reproduction seeds {'h21': (1725, 1825), 'h23': (1765, 1865), 'h19': (9600, 9700)} reused on purpose, NOT part of the seed scan
   rows share no state: one generator per world and one per agent population, fixed-size draws consumed in row order every step
(b) release on constructed states: stub, 400 rows, no input for 200 steps, s 2.0 on the held channel, counter 0; statistic per row: the hold ends at a step <= 49, both units <= 1.0 at the end step, no unit above 1.0 from then to step 199; bar lower bound >= 0.95
   (b1 valued hold, Agent10g) exact 400/400 = 1.000 [0.990, 1.000] -> PASS; end step quartiles 47/47/47 (never 0); first drive step quartiles 41/41/41; D per row quartiles 7/7/7, max 7; S peak median 11.17 max 11.17; base (Agent6) holding at step 199: 400/400, its timeout firings 1600
   (b2 neutral hold, Agent10g) exact 400/400 = 1.000 [0.990, 1.000] -> PASS; end step quartiles 47/47/47 (never 0); first drive step quartiles 41/41/41; D per row quartiles 7/7/7, max 7; S peak median 11.17 max 11.17; base (Agent6) holding at step 199: 400/400, its timeout firings 1600
   (b3 valued hold, Agent10) exact 400/400 = 1.000 [0.990, 1.000] -> PASS; end step quartiles 47/47/47 (never 0); first drive step quartiles 41/41/41; D per row quartiles 7/7/7, max 7; S peak median 11.17 max 11.17; base (Agent8) holding at step 199: 400/400, its timeout firings 1600
   (b4) H21 bench (a) protocol, Agent10g, channel 1 p 0.3: holding channel 0 at step 60 400/400; kept on every phase-2 step 0/400; release step after the last channel-0 whiff, quartiles 48/48/48; step the neutral odour is held, quartiles 120/122/124 (rows 400)
   (b4) H21 bench (a) protocol, Agent6, channel 1 p 0.3: holding channel 0 at step 60 400/400; kept on every phase-2 step 400/400; release step after the last channel-0 whiff, quartiles n/a; step the neutral odour is held, quartiles n/a (rows 0)
   (b4) H21 bench (a) protocol, Agent10g, channel 1 p 0.057: holding channel 0 at step 60 400/400; kept on every phase-2 step 0/400; release step after the last channel-0 whiff, quartiles 48/48/48; step the neutral odour is held, quartiles 134/156/176 (rows 377)
   (b4) H21 bench (a) protocol, Agent6, channel 1 p 0.057: holding channel 0 at step 60 400/400; kept on every phase-2 step 400/400; release step after the last channel-0 whiff, quartiles n/a; step the neutral odour is held, quartiles n/a (rows 0)
(c) no false release: stub, 400 rows, 600 steps, a constructed hold with its own channel fed, the other silent, Agent10g; false = a hold ended by a timeout drive that started <= 40 steps after the held odour's last whiff or the hold's formation; bar lower bound >= 0.95
   (valued hold, p 0.3) rows with no false release 400/400 = 1.000 [0.990, 1.000] -> PASS; legitimate releases (drive after >= 41 silent steps) per row mean 0.000 (rows with any 0); feed gaps >= 41 per row mean 0.000 (expected 0.0001); holding the fed odour at step 599: fix 400, base 400; drive D quartiles n/a
   (valued hold, p 0.057) rows with no false release 400/400 = 1.000 [0.990, 1.000] -> PASS; legitimate releases (drive after >= 41 silent steps) per row mean 2.147 (rows with any 373); feed gaps >= 41 per row mean 3.013 (expected 3.0832); holding the fed odour at step 599: fix 374, base 400; drive D quartiles 6/7/7
   (neutral hold, p 0.3) rows with no false release 400/400 = 1.000 [0.990, 1.000] -> PASS; legitimate releases (drive after >= 41 silent steps) per row mean 0.000 (rows with any 0); feed gaps >= 41 per row mean 0.000 (expected 0.0001); holding the fed odour at step 599: fix 400, base 400; drive D quartiles n/a
   (neutral hold, p 0.057) rows with no false release 400/400 = 1.000 [0.990, 1.000] -> PASS; legitimate releases (drive after >= 41 silent steps) per row mean 1.982 (rows with any 368); feed gaps >= 41 per row mean 3.050 (expected 3.0832); holding the fed odour at step 599: fix 332, base 400; drive D quartiles 5/7/7
(a0) release=False == the base agent bitwise (every field, counter included): release off == base, stub, Agent10 True; release off == base, World7, Agent10 True; release off == base, stub, Agent10g True; release off == base, World7, Agent10g True
(a1) identity (b), separation up to the first base timeout firing while a unit is above threshold:
      stub b1 valued hold, Agent10g: True {'rows_without_firing': 0, 'with_firing': 400, 'with_firing_equal_throughout': 0, 'first_firing_step': '41/41/41'}
      stub b2 neutral hold, Agent10g: True {'rows_without_firing': 0, 'with_firing': 400, 'with_firing_equal_throughout': 0, 'first_firing_step': '41/41/41'}
      stub b3 valued hold, Agent10: True {'rows_without_firing': 0, 'with_firing': 400, 'with_firing_equal_throughout': 0, 'first_firing_step': '41/41/41'}
      stub c00.3: True {'rows_without_firing': 400, 'with_firing': 0, 'with_firing_equal_throughout': 0, 'first_firing_step': 'n/a'}
      stub c00.057: True {'rows_without_firing': 4, 'with_firing': 396, 'with_firing_equal_throughout': 3, 'first_firing_step': '74/132/204'}
      stub c10.3: True {'rows_without_firing': 400, 'with_firing': 0, 'with_firing_equal_throughout': 0, 'first_firing_step': 'n/a'}
      stub c10.057: True {'rows_without_firing': 12, 'with_firing': 388, 'with_firing_equal_throughout': 1, 'first_firing_step': '67/112/213'}
      World7 Agent10 vs Agent8: True {'rows_without_firing': 0, 'with_firing': 400, 'with_firing_equal_throughout': 0, 'first_firing_step': '60/78/80'}
      World7 Agent10g vs Agent6: True {'rows_without_firing': 2, 'with_firing': 398, 'with_firing_equal_throughout': 0, 'first_firing_step': '60/78/80'}
(a2) Agent10 == Agent8 in trajectory (POS, HEAD, NAV, SINCE, TGT), every row: T1 True; W1 True; T3a True; T3b True | (a3) Agent10g == Agent6 in trajectory in W1: True
      (a1) W1 Agent10 vs base: True {'rows_without_firing': 25, 'with_firing': 375, 'with_firing_equal_throughout': 0, 'first_firing_step': '77/82/176'}
      (a1) W1 Agent10g vs base: True {'rows_without_firing': 13, 'with_firing': 387, 'with_firing_equal_throughout': 0, 'first_firing_step': '77/82/164'}
      (a1) T3a Agent10 vs base: True {'rows_without_firing': 0, 'with_firing': 400, 'with_firing_equal_throughout': 0, 'first_firing_step': '41/41/41'}
      (a1) T3a Agent10g vs base: True {'rows_without_firing': 0, 'with_firing': 400, 'with_firing_equal_throughout': 0, 'first_firing_step': '41/41/41'}
      (a1) T3b Agent10 vs base: True {'rows_without_firing': 1, 'with_firing': 399, 'with_firing_equal_throughout': 0, 'first_firing_step': '60/78/80'}
      (a1) T3b Agent10g vs base: True {'rows_without_firing': 2, 'with_firing': 398, 'with_firing_equal_throughout': 0, 'first_firing_step': '60/78/80'}
(a4) constructions: T3b draws == the World7 twin (both columns before t0, valued False and neutral equal from t0), wind and generator state equal True; each arm's T3b run == its World7 run on steps 0-149 (every field) and departs after True; T3a draws (valued False from step 0) True; T3a start at the valued source with s_valued 2.0 held True
(a5) reproduction on the recorded seeds (identity checks, not new evidence): H21 maintain (Agent6) on (1725, 1825) V/N/tie (300, 96, 4) (recorded 300/96/4) True; H23 filter (Agent8) on (1765, 1865) (381, 14, 5) (recorded 381/14/5) True; Agent10 (381, 14, 5), V row for row == Agent8 True; separation Agent10g vs Agent6 (True, {'rows_without_firing': 0, 'with_firing': 400, 'with_firing_equal_throughout': 0, 'first_firing_step': '50/77/80'}); Agent10 vs Agent8 (True, {'rows_without_firing': 0, 'with_firing': 400, 'with_firing_equal_throughout': 0, 'first_firing_step': '57/78/80'})
(d) realistic silent gaps, World7 task start, bench seeds, 400 x 600 (reported, not a gate)
   [Agent6] held odour's silent gaps while held: 4360 runs, quartiles 1/4/132, >= 41 1418 = 0.3252; between two hits only 3444, quartiles 1/3/147, >= 41 0.2886; base timeout firings on a hold 4322 (genuine, >= 41 silent steps since the last hit or formation, 4224; stale 98); ended the hold 2; rows with no firing on a hold 2/400; holds formed 470
      [Agent10g] timeout drives started on a hold 1394 (drive steps delivered 9743), D quartiles 7/7/7, D max 7; ended the hold 1390; circuit empty at the drive's end 1390; interrupted by a hit or the evidence release 0; silent steps before the drive (quartiles) 41/41/41, stale (< 41) 0; nothing-held drives 3055 (D > 1 among them 0); counter lowered by (Z) 1193
      [Agent10g] holds 1458; duration quartiles 48/48/57 (ended within the run 1410); held odour's silent gaps while held 3704, quartiles 1/5/47, >= 41 1395 (0.3766)
      identity (b) class on these rows: {'rows_without_firing': 2, 'with_firing': 398, 'with_firing_equal_throughout': 0, 'first_firing_step': '60/78/80'}
   [Agent8] held odour's silent gaps while held: 4702 runs, quartiles 1/4/103, >= 41 1407 = 0.2992; between two hits only 3665, quartiles 1/3/117, >= 41 0.2603; base timeout firings on a hold 4173 (genuine, >= 41 silent steps since the last hit or formation, 4032; stale 141); ended the hold 1; rows with no firing on a hold 0/400; holds formed 534
      [Agent10] timeout drives started on a hold 1465 (drive steps delivered 10216), D quartiles 7/7/7, D max 7; ended the hold 1456; circuit empty at the drive's end 1456; interrupted by a hit or the evidence release 4; silent steps before the drive (quartiles) 41/41/41, stale (< 41) 0; nothing-held drives 2713 (D > 1 among them 0); counter lowered by (Z) 1417
      [Agent10] holds 1742; duration quartiles 48/48/56 (ended within the run 1579); held odour's silent gaps while held 4736, quartiles 1/5/47, >= 41 1471 (0.3106)
      identity (b) class on these rows: {'rows_without_firing': 0, 'with_firing': 400, 'with_firing_equal_throughout': 0, 'first_firing_step': '60/78/80'}
(e) the H19 ph14b protocol re-run: World4, seeds (9600, 9700), 200 rows x 2400 steps, neutral; the circuit table 1b (circuit only, untouched) follows

== 1b. bench: a committed circuit, reset of amplitude A for D consecutive steps; lowest value of the held unit, released? ==
   A   10 | D1: low 1.52 released   0% | D2: low 1.30 released   0% | D3: low 1.14 released   0% | D4: low 0.06 released 100% | D6: low 0.05 released 100% | D8: low 0.04 released 100%
   A   20 | D1: low 1.38 released   0% | D2: low 1.16 released   0% | D3: low 0.07 released 100% | D4: low 0.06 released 100% | D6: low 0.05 released 100% | D8: low 0.04 released 100%
   A   40 | D1: low 1.26 released   0% | D2: low 0.09 released 100% | D3: low 0.06 released 100% | D4: low 0.06 released 100% | D6: low 0.05 released 100% | D8: low 0.04 released 100%
   [the design's agent: Agent4 at G 0, zero values (= Agent3 with H19 (a) ON)]
      base silence timeout  requests  8796 | value delivered [10.] | consecutive steps with a reset: median   1 | held unit before 1.99, lowest in the next 8 steps 1.49 | global unit peak  6.99 | released within 8 steps   0.2%
      base evidence release requests   540 | value delivered [10.] | consecutive steps with a reset: median   4 | held unit before 1.38, lowest in the next 8 steps 0.54 | global unit peak 11.05 | released within 8 steps 100.0%
      base drives started on a held unit 8835, not interrupted by a hit or the evidence release 8804: circuit empty at the drive's end 1/8804 = 0.000 [0.000, 0.001]; D quartiles 1/1/1, max 1; both units <= 1.0 on the 8 steps after 11/8804
      fix  silence timeout  requests 13281 | value delivered [10.] | consecutive steps with a reset: median   4 | held unit before 1.46, lowest in the next 8 steps 0.57 | global unit peak 11.16 | released within 8 steps 100.0%
      fix  evidence release requests     0 | value delivered [] | consecutive steps with a reset: median nan | held unit before  nan, lowest in the next 8 steps  nan | global unit peak   nan | released within 8 steps   nan%
      fix  drives started on a held unit 1904, not interrupted by a hit or the evidence release 1899: circuit empty at the drive's end 1899/1899 = 1.000 [0.998, 1.000]; D quartiles 7/7/7, max 7; both units <= 1.0 on the 8 steps after 1899/1899
      base reproduces ph14b 1a (8652 timeout / 761 evidence requests): False  | fix bar: circuit empty at the end of an uninterrupted drive, lower bound 0.998 >= 0.95 -> PASS
   [ph14b's own agent: ph14.Agent3 fix=False, learning off]
      base silence timeout  requests  8652 | value delivered [10.] | consecutive steps with a reset: median   1 | held unit before 1.99, lowest in the next 8 steps 1.49 | global unit peak  6.99 | released within 8 steps   0.2%
      base evidence release requests   761 | value delivered [10.] | consecutive steps with a reset: median   3 | held unit before 1.37, lowest in the next 8 steps 0.54 | global unit peak 11.05 | released within 8 steps 100.0%
      base drives started on a held unit 8691, not interrupted by a hit or the evidence release 8666: circuit empty at the drive's end 7/8666 = 0.001 [0.000, 0.002]; D quartiles 1/1/1, max 1; both units <= 1.0 on the 8 steps after 8/8666
      fix  silence timeout  requests 13810 | value delivered [10.] | consecutive steps with a reset: median   4 | held unit before 1.47, lowest in the next 8 steps 0.57 | global unit peak 11.17 | released within 8 steps  98.5%
      fix  evidence release requests   414 | value delivered [10.] | consecutive steps with a reset: median   4 | held unit before 1.43, lowest in the next 8 steps 0.56 | global unit peak 11.14 | released within 8 steps 100.0%
      fix  drives started on a held unit 2021, not interrupted by a hit or the evidence release 1932: circuit empty at the drive's end 1932/1932 = 1.000 [0.998, 1.000]; D quartiles 7/7/7, max 7; both units <= 1.0 on the 8 steps after 1889/1932
      base reproduces ph14b 1a (8652 timeout / 761 evidence requests): True  | fix bar: circuit empty at the end of an uninterrupted drive, lower bound 0.998 >= 0.95 -> PASS
   T3a on bench seeds: dwell at the neutral source, steps 100-599: ceiling (Agent5 fixed neutral) mean 13.938, floor (Agent6) mean 0.750; span 13.188 [12.250, 14.160]; per-row paired sd 9.545; M7(b) pass probability at R 0.9 1.000, at R 0.6 0.659 (the bar does not move)
== M4: identities (a0-a5) True; failed: []; bars (b) True (lower bounds [np.float64(0.9905), np.float64(0.9905), np.float64(0.9905)]), (c) True ([np.float64(0.9905), np.float64(0.9905), np.float64(0.9905), np.float64(0.9905)]), (e) True ([np.float64(0.998), np.float64(0.998)]); (e) base reproduces ph14b 1a: [('Agent4', False), ('Agent3', True)] (reported) -> M4 PASS: the tasks may be run ==
```
