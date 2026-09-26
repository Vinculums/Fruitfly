# Fruits Fly master plan v0.1

RESTORED 2026-09-19 after the space was deleted and rebuilt. Text is the approved version, transcribed from the session record. See record:space-loss-2026-09-19.

Status: approved by the project owner on 2026-09-19. Execution mode: one phase at a time, report after each, the owner decides every gate.

Progress log
- Phase 0: complete, gate passed.
- Phase 1: complete, gate passed, phase order kept unchanged.
- Phase 2: complete, gate passed. H6 adopted; H7 closed as a recorded limit.
- Phase 3: complete, gate passed. H3 adopted. Its velocity integration was superseded at the
  H14 close (decision:h14-adopt-tau1); the Phase 3 design stays on record as what was adopted then.
- Phase 4: complete, gate passed. H8 v2 adopted, and amended at the Phase 7.2 close.
- Phase 5 Run 1: complete, gate NOT met. Both of its headline claims were later withdrawn.
- Phase 5 Run 2: complete. The Select-and-Hold circuit is cleared: its reset had never fired.
- Phase 6: complete, gate passed. Main result: the model takes the discrete or destructive
  version of a mechanism the fly implements gradedly or additively (concept:discrete-vs-graded-bias).
- Phase 7.1 (H9): complete. H9 rejected as stated; its mechanism claim accepted. A graded
  substrate revises with no reset (200/200) where the bistable circuit cannot (0/200), but it
  cannot abstain. The reset is the price of an abstention threshold. H10 queued.
- Phase 7.2 (H11): complete. The extinction gate is ADOPTED; the parallel opposing site is held
  unproven, since it changes no behaviour in any protocol tested. H12 queued.
- Phase 7.3 (H13): complete, gate passed. A clean double dissociation between the gradient rule
  and surge-and-cast. Two of its claims were later qualified: the ring is not sign-reversed
  (H14), and surge-and-cast's score was a first-pass score collected before absorption (H15).
- H14 (promoted out of the queue): complete. Not supported under its stored criteria. The owner
  restated the drift bound in fly-referenced terms and ADOPTED the exact-kernel ring at tau 1,
  sigma 0.5, for ring size 16 (decision:h14-adopt-tau1). H15 then found that this adoption had
  never been checked inside an agent (record:h14-adoption-untested-in-agent).
- H15 Run 1: complete, NOT supported. Every surge-and-cast arm scores exactly zero in the gated
  window, the known-valence probe included. Cause: 92 percent of agents are absorbed at the
  downwind wall within the first 600 steps (concept:surge-and-cast-absorbing-lost-state).
  Learning among agents that arrived is two-sided and clean (+0.901, -0.900). Reported as found;
  nothing changed after the table. The owner then opened H16 ahead of H15 Run 2
  (decision:h16-open) and set H15 Run 2's entry conditions (record:h15-run2-entry-conditions).
- H16 Run 1: complete, NOT supported as registered. A cast offset that returns toward upwind
  (`return`, a triangle wave) cuts late-unrecovered agents from 98 percent to 1 percent and holds
  a flat profile over 5400 steps, but in H15's 40x40 walled arena it only matches the random
  walk (9.7 against 10.0) and fails the floor clause. The wall-restart rule fails (81 percent).
  Report d80f00672a54d238b.
- H16 Run 2: complete, NOT supported under K1-K4 on one clause. Walls moved out of reach
  (160x160), every distribution relative to the source kept, rules frozen. `return` 23.7 against
  a random walk's 0.0, late unrecovered 0.0 percent, no wall contact by any agent, reacquisition
  153 steps median; the same seeds in the 40x40 arena give 10.3 with 524 contacts per agent.
  K3 fails on cold start only: from an odour-free start 52 percent find the plume. Ring
  connected: with the wind sensed every step it carries the rule unchanged (K5(a) pass); with
  the cue dropping out 50 steps at a time it leaks agents to a median of 0.0 while a perfect
  integrator keeps 24.0. Report d74aba218d183d57e.
- H16 CLOSED by the owner (decision:h16-close-limited-adoption). Both verdicts stand as not
  supported; K3 is not edited. By a separate decision the return rule is ADOPTED for a limited
  scope: low-boundary environments with heading information on every step, tracking a plume
  already entered and reacquiring it after loss. Cold search becomes H17; the ring under cue
  loss becomes H18.
- Heading input contract CHANGED by the owner (decision:heading-input-rotation-made): the ring
  is fed the rotation made, not the commanded turn. Verified: it follows every wall reflection,
  single-step rotations over 135 degrees included (7.5 -> 7.8 degrees), and heading error over
  45 degrees goes from 4.30 to 0.00 percent with the cue on every step.
- Two-source discriminability check (decision:h15-two-source-check-open): complete and JUDGED
  by the owner (decision:two-source-check-judged). M1 pass; M2 pass on equality (exactly 20 of
  200 agents unrecovered against a bar of 10 percent); M3(a) as first registered is a FAIL and
  stays one; the reading amended before the evaluation is a separate, narrower result. What is
  shown: from a start in the punishing plume, a KNOWN NEGATIVE valence drives avoidance and the
  move to the rewarding source (93.3 percent reach it). Not shown: any approach effect of a
  positive valence, and learning. Natural exposure to both sources is insufficient (17.5
  percent) and one-sided. The two-source world is kept. Report d536d4a14700d1e37.
- Unrecovered excess DIAGNOSED, measurement only (record:unrecovered-excess-diagnosis-result).
  Same world, initial states and seeds for every arm: bare return rule 0.5-1.5 percent late
  unrecovered, agent without Select-and-Hold 0-1, with exact heading 7.5-11, full agent 9.5-10.
  Every late-unrecovered agent received whiffs after its last hit (median 8-11) and none was
  handed to navigation. Of 566 losses of the hold none came from the silence timeout; 94-95
  percent followed a whiff of the other odour. Report d53188c5b3d6638ea.
- H19 option (a) (decision:h19-open-option-a): SUPPORTED on N1-N5, the distractor condition N6
  UNREADABLE (it was registered as reported, not as a gate). While nothing is held, a whiff of
  an odour whose valence is not negative resets the cast clock; nothing else changes. Late
  unrecovered 10.5 -> 0.0 percent with neutral valence (bare rule 0.5) and 16.0 -> 4.5 with
  known valence; the boundaries hold exactly; avoidance kept (97.2 percent of punishing-plume
  starters reach the reward); selection recovers too (losses never followed by a hold 7.3 -> 1.1
  percent; why is an interpretation, whiff spacing was not measured). Report d9ca02b921ee74e59.
  ADOPTED by the owner within the tested conditions, as a separate record
  (decision:h19a-adopt-and-run2-direction).
- Two defects tracked apart, measurement only. The silence timeout's reset is DELIVERED (10.0)
  but for one step, which dips the held unit from 1.99 to 1.49 and never releases; four
  consecutive steps at 10 or two at 40 would (record:silence-timeout-chain-result). FROZEN by
  the owner as a known defect for the integrated run. The upstream stage is also the amplifier
  and pulse-stretcher that brings a whiff into the circuit's range (one whiff: 0.76 of threshold
  with the stage, 0.10 raw). Two controls are kept under different names: 'whole stage removed'
  and 'cross-channel division term removed'; the second is bench-checked exact
  (record:cross-channel-control-bench-check).
- H15 Run 2 specification: written before any code and reviewed by the owner three times
  (v1 dc2456642089af3b9, v2 d8b1e00dd1609fadc, v3 d345d91f2132e4efc, kept as history). FINAL v4
  is one standalone document, doc dc860b9c7c6f3aa6e, hash 7f23e6e5...854d, cited by the code and
  the report. Run 2 opened by decision:h15-run2-open.
- H15 Run 2: complete and CLOSED by the owner (decision:h15-run2-closed). **E1 (Q1-Q4,
  integrated behaviour): NOT DECIDED BY THIS RUN. E2 (Q6, a trained memory driving behaviour
  with nothing learned in the test): PASS.** Q5 (weight level): PASS. The tie rule is not
  waived, the run is not re-judged, and a rerun to obtain a pass label is not prioritised.
  Every E1 criterion passed except Q3(c)'s matched-pair win rate, UNREADABLE under the
  registered tie limit: 146 of 199 pairs improved and 53 were tied, which is not absence of
  evidence. Recorded separately as OBSERVED in the tested conditions: learning of a negative
  valence (-0.892 from one visit of about 7 steps) and leaving the punisher; E1's criteria on
  long-horizon search, avoidance and reaching the rewarding source passed (94.5 percent reach it,
  dwell 0.944 of a known-valence agent's median, late unrecovered 21/400); in E2, with learning
  frozen, the trained group dwelt less at the punisher and reached the reward more than the
  sham-trained group. The necessity of every component module is NOT shown. One specification
  amendment before the evaluation (a 50-step silent gap between the two E2 trainings); no
  implementation error found; nothing changed after the table. Report d8093197d7aa59faa
  (corrected on four points after the owner's review, record:h15-run2-report-corrections),
  source d5784b642378b2f65 (sha256 cc939996...3fdc). Moving on to the next research is an
  operational decision, separate from E1's statistical verdict.
- H20 set as the next priority by the owner, design before code
  (decision:h20-priority-design-first). The design was written for Stage A only (a SUPPLIED
  positive value, learning off), reviewed by the owner twice (v1 d1ade7c2ff6715415, v2
  d0e1226b1ae7e0f64, kept as history) and confirmed with four clarifications. FINAL v3 is one
  standalone document, doc dd947882bd962eebe, hash e563bd60...f0a3, stored before any code.
  H20 Stage A OPENED (decision:h20-stage-a-open). Hypothesis narrowed to: given the
  opportunity to approach both, the agent chooses the odour carrying a positive value over one
  carrying none. Pathway: one multiplicative gain (1 + G*max(v, 0)) on the upstream output
  entering Select-and-Hold and its evidence release; negative avoidance unchanged and overriding.
  Task: two sources 10 apart crosswind, midline start 20 downwind (equal whiff opportunity), 2x2
  balance over odour identity and side, 400 rows, choice = first source reached; six arms
  (bias, bias-revise, neutral, pathway-off, priority, priority-off). G fixed on a registered bench
  before the task. Criteria A1-A5 over all assigned rows, 95 percent, one evaluation, no
  extension. Order: implementation -> self-checks -> bench -> G* recorded -> dev -> evaluation.
- H20 G bench: NO ELIGIBLE CANDIDATE (record:h20-g-bench-result); the rule and the verdict stand.
  Implementation ph16.py (bench version sha 6eaad986...ec71, doc d906c4461b7feb3d4); every
  self-check passed. At the task's start rate p 0.057 the neutral case was within tolerance
  (0.506 [0.457, 0.555]) and the first-hold accuracy was 0.730 / 0.772 / 0.802 at G 0.5 / 1 / 2
  (lower bounds 0.684 / 0.729 / 0.761) against the registered lower bound 0.85. Per the rule the
  task was not run. The owner kept the bar and the verdict and asked for a diagnosis first.
  Diagnosis (record:h20-post-bench-diagnosis-result, ph16b.py sha b0a918b1...dad1, doc
  d501080d7ed485c2a): the gain enters in TWO places (the circuit input and the evidence release);
  the circuit input alone reproduces the registered first-hold counts exactly; the release
  pathway adds 2-4 points to the biased end state later. A single biased whiff holds at G >= 0.5
  (peak 1.996 against threshold 1.0), an unbiased one never (0.756). On the observed input, for
  the tested G, 77 of 400 rows form an unbiased hold before the biased channel's first whiff,
  which bounds the first-hold accuracy at 0.8075 for those G on that input (the ceiling is
  limited to the tested G and the observed input by the owner; 321 of 323 is a diagnostic
  conditional figure). Classified as a design error in the bench criterion. End state over all
  400 rows at G 1: biased 58.5 percent, nothing 34.8 percent.
- **H20 Stage A EVALUATED ONCE with G 2 (fixed post hoc by a separate execution decision of the
  owner, decision:h20-stage-a-run-g2, explicitly not a bench pass) and CLOSED by the owner
  (decision:h20-stage-a-closed): NOT SHOWN under the registered criteria. A1 PASS, A2 FAIL, A3
  PASS, A4 INCONCLUSIVE.** Report db2f39472a3eed143 (corrected after the owner's review,
  record:h20-stage-a-report-corrections), result record:h20-stage-a-result, source ph16.py sha
  33d5fdb2...a2c2 (doc d89d730faca4b965a), evaluation output sha 7e51446e...0a45, seeds
  1680/1780 unused before. Before the evaluation: development run 1
  (record:h20-dev-run-g2-a1b-failure) had no operation error but failed A1(b) on the development
  seeds because the adopted agent starts every row with the same initial cast side (cast_sign
  +1), which from the midline sends every first cast swing to -y (-y reached first in 94 percent
  of rows in every arm; flipping the sign reverses it to 0.963, drawing it per row balances it
  to 0.495; ph16c.py sha 0096a727...d28, doc d97e6ccaee4515549). AMENDED by the owner before the
  evaluation (decision:h20-amendment-initial-cast-side): the initial cast side is drawn per row
  in the task harness, the same draw in every arm; agents, bench, pathway, G and criteria
  unchanged; development run 2 then passed A1 with no operation error
  (record:h20-dev-run-g2-amended). Evaluation: A1 PASS (no-choice 0/400; P(+y first) 0.482
  [0.434, 0.531]; pathway-off P(V | reached) 0.532 [0.484, 0.581]). A2 FAIL: bias P(V) over all
  rows 213/400 = 0.532 [0.484, 0.581] against 0.70; cells 49 / 56 / 53 / 55 inconclusive; DP
  against pathway-off 0.000 [-0.008, 0.007] against +0.20. A3 PASS (bitwise). A4 INCONCLUSIVE
  (the printout's 'FAIL' is a labelling error: the rule names no aggregate when no part fails):
  (a) the flee target on every one of 34,330 negative-held (row, step) in priority and 36,892 in
  priority-off, 0 violations; (b) dwell at the negative source +0.507 [+0.230, +0.822] against
  at most +1.0, PASS; (c) priority P(V) 278/400 = 0.695 [0.648, 0.738] against 0.70,
  INCONCLUSIVE. The registered avoidance-maintenance criteria passed with the gain on; measured
  beside them, dwell at the punisher did increase (+0.507 step) and reaching the valued source
  first fell by 3.8 points. A5 reported: revision of a held neutral selection in 238/400 = 0.595
  [0.546, 0.642], 'meets the bar that at least half revise', by the evidence release (270 of 335
  releases; timeout 0). DIAGNOSIS by segment (names no cause by itself): the first hold follows
  the value (277 against 200 of 400, step median 13 against 30; a diagnostic, not a criterion);
  maintenance and revision change little (4 of 187 N rows switched); the first source reached is
  the same row for row in the bias and pathway-off arms; 43 N rows held the valued odour at the
  moment they reached the neutral source and 70 held nothing; the reach happens at about step 31
  whatever is held. The owner's statement of the core finding: the value gain changed the
  internal selection but not the first source reached; before learning, the problem appears in
  the part that links selection to action. No implementation error found; nothing changed after
  the table. Stages B and C are not entered.
- **Selection-to-navigation LINK CHECK (decision:h20-linkcheck-open, design v1 doc
  d824732220256254b confirmed with two interpretation notes; geometry C2 amended before any run,
  decision:h20-linkcheck-c2-amendment): complete, one run.** Value and learning excluded; the
  tracked odour fixed to A or to B by intervention against the adopted circuit; geometries C0
  (s 10, d 20, the H20 task), C1 (s 10, d 16), C2 (s 12, d 24; registered as s 14, d 28, which
  the self-check found beyond the cone length LMAX 25, record:h20-linkcheck-c2-design-error).
  ph17.py sha 4b30ddf8...689f (doc d075802dcb8974c59); one self-check off-by-one corrected
  before any run; dev run clean (record:h20-linkcheck-dev-run); evaluation on 1690/1790, output
  sha 39016345...d546; report df9cf42bb99c43d39; result record:h20-linkcheck-result. MEASURED:
  the tracked identity reaches the movement command at the first single-channel whiff in 400/400
  rows in every geometry (step median 6 to 8) and the positions diverge from then; by the point
  where the cones separate the crosswind position is at chance with respect to the tracked source
  (0.49 to 0.53, all geometries); in C0 and C1 the first source reached is the same whatever is
  tracked (0.932 and 0.910 of rows) and each fixed arm reaches its tracked source first in only
  0.060 and 0.087 ('not expressed in the first reach'); in C2, with the separated stretch
  lengthened from 14 to 18 units, each arm reaches its tracked source first in 0.743 [0.697,
  0.783] ('partial'); over 600 steps the agent stays at the tracked source in 0.95 to 0.97 of
  rows in every geometry ('expressed in dwell'; dwell is the more lenient measure). Reading for
  H20's task, not a re-judgement: on C0 a fixed and perfect selection reaches its source first in
  about half the rows (200 and 221 of 400), so A2's first-reach bar of 0.70 was above what the
  adopted navigation can express in that geometry for any selection mechanism; the Stage A
  verdict stands. Whether a crosswind term would be needed for the first reach in C0 is not
  tested and not claimed. The owner chose option (a) (decision:h20-run2-design-first) and opened Run 2
  (decision:h20-run2-open) on design v1 FINAL (doc d3866101cd92f911d).
- **H20 Run 2 EVALUATED ONCE (decision:h20-run2-open, design v1 FINAL doc d3866101cd92f911d, hash
  of the confirmed draft b88f0769...b115): NOT SHOWN under the registered criteria. R1 PASS, R2
  FAIL, R3 PASS, R4 PASS.** Report dd71f30d466badf4b, result record:h20-run2-result, source
  ph18.py sha 26ad4def...97c3, evaluation output sha 321d8ff1...5394, seeds 1695/1795 unused
  before. Self-checks passed; development run (9840/9940, record:h20-run2-dev-run) found no
  operation error and no amendment. Evaluation: R1 PASS (ties 7/7/1 of 400; floor P(V|chose)
  0.517; ceiling known-answer P(V) 377/400 = 0.943 [0.915, 0.961]). R2 FAIL: bias P(V) 214/400
  = 0.535 [0.486, 0.583] against 0.70; cells 55/48/57/54 inconclusive; DP against pathway-off
  0.028 [-0.002, 0.055] against +0.20; 0.568 of the ceiling. R3 PASS (bitwise; known-answer h
  fixed per row). R4 PASS: 0 flee violations over 37,414 and 40,000 negative-held steps; dwell
  at the punisher +0.368 [+0.107, +0.640]; priority P(V) 0.912; reported DP vs priority-off
  -0.010. DIAGNOSIS (names no cause): the measure expresses a perfect selection (dwell median
  26 vs 0); the gain still moves the first hold (274 vs 210, step 13 vs 30); it does not move
  the majority source (dwell median 14 vs 11). First-reach secondary near chance even in the
  known-answer arm (0.560). No implementation error; nothing changed after the table. Closure
  is the owner's. Stages B and C are not entered.
- **H20 Run 2 DIAGNOSED (measurement only) and CLOSED as NOT shown by the owner (2026-09-23,
  decision:h20-run2-closed).** Diagnosis at the owner's request (decision:h20-run2-diagnosis-run;
  ph18b.py sha 55b27b71...b433, doc d3bc88d13a259d129; output sha a33cf070...a342; report doc
  d73ddadcfb33103cd; record:h20-run2-diagnosis), on the evaluation trajectories re-run unchanged
  (V/N/tie identical to the table). The gain moves 24 rows into V and 13 out (net 11). It wins 64
  extra first selections, all toward the valued odour and earlier in 271 rows, but those convert
  into a valued majority at 0.328 while the 210 rows G 0 also selected convert at 0.786 in both
  arms. Dwell at the neutral source is accumulated while holding the neutral odour (63 percent) or
  nothing (29 percent), 7 percent while holding the valued odour. Holds end when the held unit has
  already decayed to the threshold (s median 1.06 the step before; the no-input fixed point is near
  2.0): 296 of 315 endings on the evidence flag, the timeout ended 5 of 3998 firings (the Phase 5
  Run 2 limit, now measured in the task). In the 77 N rows that lost a valued first hold the agent
  was nearer the neutral source in 75 when it ended; valued whiffs 1.7 per row afterwards against
  9.1 neutral. Reading, labelled a mechanism interpretation: the gain multiplies a response that is
  zero when the valued odour is absent; the neutral response then lowers the held unit through the
  circuit's pool; the release flags coincide with that condition and are not what ends the hold.
  H20 is neither shown nor rejected (two runs NOT shown); Stages B and C stay queued.
- **H21 OPENED FOR DESIGN by the owner (2026-09-23, decision:h21-open-design): hold maintenance by
  value, a separate hypothesis.** Design v1 DRAFT doc d6a72a8f28a483b25 (hash 6727beee...ca5a),
  for the owner's review, no code. Rule: while a higher-valued odour is held, a lower-valued
  non-negative odour's response is gated out of the selection circuit and the evidence release
  (two effects of one gate); equal values, nothing held and negative odours are never gated, so
  the agent is the Run 2 agent in those cases by construction. Mechanism bench before the task
  (a held valued odour must survive 200 steps of neutral-only input, lower bound 0.95; asymmetry
  and inertness as identities; no-candidate rule). Task as Run 2 (C0, dwell majority, 400 x 600),
  seven arms (maintain, rule-off = the Run 2 agent, rule-only at G 0, pathway-off, neutral,
  known-answer, priority-identity), criteria M1-M5, bars 0.70 / 0.55 per cell / DP +0.15 against
  rule-off proposed for the owner. Prediction on record: maintain 0.70 to 0.80 (arithmetic 0.76),
  rule-only 0.55 to 0.65.
- **H21 design v1 reviewed (five fixes), v2 confirmed FINAL by the owner (decision:h21-design-v2-choices,
  decision:h21-open; doc d7fd5abcc95169698, hash e83c9de2...965a), implemented, benched and EVALUATED
  ONCE: NOT shown under the registered criteria on an INCONCLUSIVE M2, no criterion failed. M1 PASS,
  M2 INCONCLUSIVE ((a) and (b) PASS, (c) INCONCLUSIVE), M3 PASS, M4 PASS, M5 PASS, M6 PASS.** Report
  d4fd6c39f7f81e1ee, result record:h21-result, source ph19.py sha 00c6a3b3...4791 (doc
  d583f45c494d675e6), evaluation output sha a9635805...942e, seeds 1725/1825 unused before (v1 had
  proposed 1720, which the two-source check had used; found in the self-review and replaced).
  Self-checks passed (Agent6 with the gate off is Agent4 bitwise; with it on it is Agent4 at 0/0,
  +1/+1 and +1/-1). Mechanism bench (record:h21-bench-result): with the gate a valued hold survives
  200 steps of neutral-only input in 400/400 rows at G 2 and at G 0 (bar 0.95 passed), 0/400 without
  it; the timeout fired 1649 times and ended none. Development run (record:h21-dev-run) clean, no
  amendment. Evaluation: maintain P(V) 300/400 = 0.750 [0.705, 0.790] against 0.70 (PASS; 298
  needed); cells 86/70/76/68 (PASS); DP against rule-off +0.180 [+0.143, +0.218] against +0.15
  (INCONCLUSIVE; the bar sat at the lower edge of the registered prediction range); DP against
  pathway-off +0.240 [+0.198, +0.283]; rule-only (G 0 + gate) 0.603; known-answer 0.950; no added
  lost rows (3 against 4), no wall contact. MEASURED: the first selection is identical with and
  without the gate (280 valued-first rows in both); with the gate a valued hold is never lost (0 of
  280 against 204) and converts into the majority source at 0.971 (against 0.718); the neutral-first
  rows are revised at 0.442 in both arms and make up 92 of the 100 non-V rows; the design's arithmetic
  (0.70 x 0.971 + 0.30 x 0.233 = 0.750) is realised. No implementation error; nothing changed after
  the table. Closure is the owner's.
- **H21 CLOSED by the owner (2026-09-23, decision:h21-closed): NOT shown under the registered
  criteria on an INCONCLUSIVE M2 (part (c), DP +0.180 [+0.143, +0.218] against +0.15); no criterion
  failed; not re-judged, no extension, nothing rewritten as a pass.** The gate is ADOPTED within the
  tested conditions only, as a separate record (decision:h21-gate-adopted-within-tested-conditions):
  supplied value, values +1/0, G 2, C0, the dwell-majority measure, learning off. Measured, recorded
  apart from the verdict: a valued hold is never lost with the gate (0 of 280 against 204) and
  converts at 0.971 (against 0.718); the first selection (280 valued-first) and the revision of
  neutral-first holds (53 of 120) are identical with and without it; paired, 72 rows into V and 0 out;
  the remaining loss is the front end, not maintenance. Recorded as an OBSERVATION, not a rule: the
  M2(c) bar sat at the lower edge of the registered prediction; at 400 paired rows (sd about 0.384,
  half-width about 0.038) the bound clears 0.15 only from an observed DP of about 0.188, so under a
  true DP of 0.18 the pass probability was roughly 0.35 to 0.5. **H22 OPENED FOR DESIGN by the owner
  (decision:h22-open-design): the front end of the H21 task, not the gate** (120 of 400 rows first
  hold the zero-valued odour, 53 revised; ceiling the known-answer arm's 0.950), with the owner's
  constraints (own value read-out and hold state only; avoidance untouched; no navigation change
  unless the hypothesis is about navigation and says so; a flagged subclass, identity with the H21
  maintain agent; bench first; seeds checked; the H21 task unchanged) and, for this design only, the
  pass probability of every bar at its registered prediction. Diagnosis from the record, no code
  run: with a neutral hold navigation surges only on neutral whiffs, which carries the agent up the
  neutral axis, where the valued cone never reaches inside LMAX; a neutral-first row is revised only
  if a valued whiff arrives before the overlap is left (arithmetic about 0.45 to 0.6 against 0.442
  measured; a mechanism interpretation); the known-answer arm, whose navigation ignores neutral
  whiffs, reaches 0.950. Design v1 DRAFT doc dfd041adf77911e7c (hash 97c4669c...2fd6, local
  experiments/h22/h22_design_v1.md), no code: the value-gated surge, a navigation hypothesis
  separated from selection (while a non-negative odour valued below the highest value in the
  agent's read-out is held, its whiffs do not reset the cast clock); six arms against the H21
  maintain agent; a bench with the agent placed at the neutral source; bars M2(a) 0.75, cells 0.55,
  DP +0.05 with pass probabilities 0.99, 0.95 and 0.89 at the prediction's lower edge; seeds
  9870/9970 and 1755/1855 checked unused. The first-selection lever was not chosen (bounded near
  0.83 by the arrival-order arithmetic and still carried up the neutral plume by H19 (a)).
- **H22 OPENED on design v1 FINAL (owner, 2026-09-23, decision:h22-open; hash 1ce2717e...7f83).
  Mechanism bench (M4): NO CANDIDATE, the task NOT run** (record:h22-bench-result; ph20.py sha
  edec6d83...efbe, doc d714b91e1fbbc7ede): (a) surge withheld 400/400 PASS, (b) and (c) identities
  True, (d) placed at the neutral source 84/400 = 0.210 [0.173, 0.253] against the bar 0.50
  (prediction 0.60 to 0.95), 5/400 without the rule; development and evaluation seeds unused; the bar
  not lowered. The owner chose a measurement-only post-bench diagnosis and the record
  (decision:h22-post-bench-diagnosis, '1. 1번 안 2. 기록 진행'). Diagnosis (ph20b.py sha
  4b6c0497...49d1, output 12d1eee4...c702, report d124565e8d93abf16,
  record:h22-post-bench-diagnosis-result): bench (d) reproduced exactly; on the registered start
  revision reaches 0.328 [0.283, 0.375] at 600 steps and 0.390 at 900 (rule off 0.190, 0.307), not
  0.60; no valued whiff installs the valued hold directly (isolated whiffs 0 of 319; every revision
  passes through 'nothing held'), and with the rule 322 of 495 releases return to the neutral hold
  (0.315 convert, against 0.826 without); on a variant start on the neutral axis 20 downwind (not the
  bench) 0.083 with the rule and 0.085 without at 600. Reading: window and mechanism both, the window
  alone insufficient; the rule produces sampling, not conversion. Verdict and bar unchanged; design
  v2 or closure is the owner's.
- **H22 CLOSED as NOT shown by the owner (2026-09-23, decision:h22-closed; '1. not shown 2. 가치 -
  필터 허용 3. 진행').** No candidate at the mechanism bench, so the task was not run and no task
  criterion was evaluated; not re-judged, the bar not lowered; seeds 9870/9970 and 1755/1855 never
  used and kept registered to H22. Nothing adopted. Structural reading (interpretation): the first
  selection and every revision are decided from the empty state (H19 (a) plus arrival order), which
  nothing biases toward the value except G; the gate protects a valued hold, nothing protects the
  empty state. Bench outputs normalised to LF (hashes re-recorded in record:h22-bench-result).
  **H23 OPENED FOR DESIGN (decision:h23-open-design): value-filtered navigation, allowed by the owner
  knowingly** (the navigation hit may depend on an odour's value in the agent's own read-out). Design
  v1 DRAFT doc d77542ae99d003747 (hash a225386a...7454, local experiments/h23/h23_design_v1.md), no
  code: while a top-valued odour is held, surge on its whiffs; otherwise only a top-valued
  non-negative odour's whiffs steer (Agent8 = Agent6 with ph19.py line 63 replaced; bitwise Agent6
  at 0/0, +1/+1, +1/-1 and with the valued odour held). At +1/0 navigation is the known-answer arm's
  law and no longer depends on the circuit, so the task cannot show selection controlling
  navigation. Bench on the diagnosis's task-like neutral-hold start at 600 steps; task bars M2(a)
  0.88, cells 0.70, DP +0.05 (pass 0.93, 0.99, 0.98 at the lower edge); bench (b) passes with
  probability 0.02 at its own lower edge, put to the owner. Seeds 9880/9980, 1765/1865, bench
  20261001/20261002, bootstrap 20261003 checked unused.
- **H23 OPENED on design v2 FINAL (decision:h23-open; owner 2026-09-23, '1과 5 그대로 확정 한다',
  then '1~5 전부 확정': all five points as recommended, bench (b) reported, not a gate).** Doc
  db6df2e0013ab96e7 (hash c19751f4...0087). ph21.py (sha 3a1d79d9...cfc1, source doc
  ddcec8520fcd8e23c): Agent8 = ph19.Agent6 + the value filter on nav. Self-checks pass first time;
  bench M4 PASS (identities True, (a4) and (c) 400/400); bench (b), reported: from the task-like
  neutral-hold start 217/800 = 0.271 hold the valued odour at 600 against 70/800 = 0.087, DP +0.184
  [+0.148, +0.220], every revision through 'nothing held' (record:h23-bench-result). Development run
  9880/9980: no operation error (record:h23-dev-run). One evaluation 1765/1865: **PASS under the
  registered criteria, M1-M6 all PASS**: filter P(V) 381/400 = 0.953 [0.927, 0.969], cells 94 to
  96, DP against the H21 maintain agent +0.240 [+0.200, +0.282], P(V) filter / known-answer 0.987,
  no added lost rows (record:h23-result; report d8b91235798da849f). Value-driven navigation in the
  full agent; the task does not show selection controlling navigation. Closure is the owner's.
- **H23 CLOSED as SHOWN by the owner (2026-09-23, decision:h23-closed; '1. shown + 진행 2. 추천안 진행
  3. 정리필수').** M1-M6 all PASS under the registered criteria; not re-judged. The value filter is
  ADOPTED within the tested conditions only, as a separate record
  (decision:h23-filter-adopted-within-tested-conditions): supplied value, +1/0, G 2, C0, dwell
  majority, learning off, the H21 gate on; not validated where the higher-valued odour is absent (the
  rule's known cost), at +1/+0.5, with learned values, other G or geometries. Bookkeeping, mandatory by
  the owner's point 3: the selection circuit's revision-via-the-empty-state limit recorded
  (record:selection-circuit-revision-via-empty-state); the design v2 section 9 seed arithmetic slip
  corrected in decision:h23-closed (the design left as cited); the code-citation convention set
  (decision:code-citation-convention; subject_path removed from four records). Next, by the owner's
  point 2 (decision:next-absent-odour-check-then-stage-b): the absent-odour check, design v1 DRAFT doc
  ddab34a689d056e2e (local experiments/absent_odour_check/absent_odour_check_design_v1.md), no code;
  then H20 Stage B.
- **Absent-odour check OPENED on design v1 FINAL and run once (decision:absent-odour-check-open; owner
  2026-09-23, '의견 그대로 확정하고 진행').** Doc ddab34a689d056e2e finalised in place (hash 3ec1b989...3d43).
  ph22.py (sha 03ab8c47...ca1c, source doc d6a27b8b1f1b927ce): World7 with the absent source masked after
  the draw; ph21.Agent8 against ph19.Agent6, unchanged. Self-checks pass (one self-check indexing error
  fixed in demo); development run 9890/9990 without operation error; one evaluation 1775/1875: R0
  identities all True; in W1 Agent8 never surges and reaches the source by casting past it, 344/400 =
  0.860 [0.823, 0.891] 'reach kept' (R5, 1800 steps: 381/400 'reach kept'), but dwells a third as long
  (median 8 against Agent6's 25), ends upwind of the source (median 63 upwind at 1800, 111 rows at the
  wall) and loses the plume in more rows (130 against 0 over the last 600 of 1800); Agent6 0.988 within
  its prediction (record:absent-odour-check-result; report db7b4a7ca1c2ab7ea). The filter's scope is the
  owner's decision, before H20 Stage B.
- **Filter scope: option (v) explored (owner 2026-09-23, '(v) 안으로 가보자'; decision:filter-scope-explore-option-v;
  a design decision, not an adoption).** Measurement-only diagnosis ph21b.py (sha 4f3b707e...0b12, source doc
  d0a340a477986a52c; output experiments/h24/ph21b_diag.txt sha 17a0bf41...549a; dev seeds only; no new rule
  run; record:option-v-presence-diagnosis-result): 0.766 of the H23 filter's actions, and its first action in
  99/99 rows it moved into V, precede the row's first valued whiff; any presence scope that starts OFF (strict
  P > theta, or a window N of any length) bounds P(V) in [0.627, 0.820] (filter 0.932, maintain 0.690) and is
  bitwise Agent6 in W1; a presence counter that starts ON keeps [0.915, 0.973] at N 45-80 (outside option (v)
  as worded; = the check's candidate (ii)). H24 design v1 DRAFT doc d24c2efe28592c34d (local
  experiments/h24/h24_design_v1.md; concept:h24-presence-scoped-value-filter): variants (v-a) / (v-c) / (v-p),
  two tasks (the H21 task and W1), a draft classification-rule relaxation for (v-c) / (v-p); no code.
- **H24 design v2, candidate FINAL (2026-09-23; decision:h24-design-v2-choices).** The owner chose (v-p), a
  presence counter per odour that starts ON, N 60; start OFF is structurally blocked on T1. The owner signed
  the H24-scoped relaxation of the classification rule, with the ON start recorded as a prior
  (decision:classification-rule-relaxed-presence-counter). T3, a 'sensed then lost' world, is added: the
  valued plume is masked from t0 150. The T2 dwell bar is to be fixed after bench (d) by a registered rule
  (decision:h24-t2-dwell-bar). Doc d5a2e259bfb6445b9 (local experiments/h24/h24_design_v2.md, sha
  f84ddf99...ee9f). No code. Awaiting the owner's confirmation.
- **H24 opened, benched and CLOSED as NOT shown (2026-09-23; decision:h24-open, record:h24-bench-result,
  decision:h24-closed).** Opened on design v3 FINAL (doc dafaa132a0267d56b); ph23.py (sha ae180492...b5ae,
  source doc d0ea25b8bebac735d). M4 FAIL at (f) M7(a), 65/370 = 0.176 [0.140, 0.218] against 0.95: the held
  clause presumed a timeout release the circuit does not make. No task run, nothing adopted, the H24-scoped
  relaxation lapsed. H25 (the silence-timeout fix) opened for design (decision:h25-open-design); design v1
  DRAFT doc d3cb0794633a587ae (experiments/h25/h25_design_v1.md), no code. Awaiting the owner's review.
- **H25 opened on design v2 FINAL, benched, developed and evaluated once (2026-09-23; decision:h25-open, owner
  '추천안으로 확정'; record:h25-bench-result, record:h25-dev-run, record:h25-result).** Design v2 FINAL doc
  dce297e76390fa854 (experiments/h25/h25_design_v2.md, sha 6fbb293b...e60b). ph24.py (sha f344f178...1bef, source doc
  d0c87ae7a68d1a27f): Release mixin (S)+(Z) on the adopted act; Agent10 = Release + Agent8, Agent10g = Release + Agent6.
  Bench M4 PASS; one evaluation 1805/1905: SHOWN under the registered criteria (M1-M5, M7 PASS); T3a R 0.957
  [0.895, 1.025]; Agent10 bitwise Agent8 in trajectory; M6 (reported) Agent10g - Agent6 P(V) -0.155 [-0.200, -0.113].
  Report doc d2a35d5a59aace929 (experiments/h25/h25_report.md). Awaiting the owner's closure.
- **H25 CLOSED as SHOWN; the release adopted within the tested conditions (2026-09-24; decision:h25-closed,
  decision:h25-release-adopted-within-tested-conditions).** Adopted at +1/0, G 2, C0, the worlds tested, learning off,
  gate on; negative values excluded pending the avoidance check.
- **Avoidance check run once (2026-09-24; design v1 FINAL doc df00c6e0dbc5f6792; src/ph24b.py sha bbabad15...eefc,
  source doc d68d589ccad0beef9; record:avoidance-check-result).** R0 'identity holds', R1 'priority kept, identical',
  R2 'released as valued holds', R3 'avoidance changed' (flee violations 0, dwell at the negative source lower, but
  P(V) 0.765 vs 0.925, paired DP -0.160 [-0.195, -0.125]; lost rows 127 vs 33). Not every reading clean.
- **The owner's decisions of 2026-09-24 ('1 → 2(a) → 3·4·5').** (1) R3 diagnosis, measurement only
  (record:r3-negative-release-diagnosis-result; src/ph24c.py sha 17adab85...6a45, source doc d4238c123b7873d90;
  report doc d56ab9eef4549b009, experiments/avoidance_check/r3_diagnosis.md): every drive-ended negative hold ends
  outside both plumes and no whiff follows (131/131); the whole P(V) gap sits in the base's wall-contact rows.
  (2a) The release stays adopted at +1/0 only; at negative values its adoption is ON HOLD
  (decision:release-negative-scope-on-hold); the cost recorded as a limit pointing to H17
  (record:release-negative-cost-limit). (3) H24 Run 2 opened for design (decision:h24-run2-open-design): design v1
  DRAFT doc d507838fdb2c85d0b (experiments/h24/h24_run2_design_v1.md), no code; the relaxation to be re-signed.
  (4) Viewer export extended with T3a, T1r and N1 rows, reproduction-checked (viewer/repro_check.txt).
- **H24 Run 2 opened and STOPPED at the bench by its registered stop rule (2026-09-24).** The owner confirmed design
  v1 section 12 ('(a) 규칙 완화 재서명, (b) 벤치 시드 T1 측정 (h) + 중단 규칙 채택 여부, (c) T3 = 구성 손실(T3a)로 등록
  H24 Run 2 → H17 → Stage B'): decision:h24-run2-open on design v2 FINAL (doc d65589bd43383a57c,
  experiments/h24/h24_run2_design_v2.md, sha 0d819e73...8d7e); the relaxation re-signed for Run 2 only
  (decision:classification-rule-relaxed-presence-counter-run2); the project order H24 Run 2 → H17 → H20 Stage B
  (decision:priority-h24run2-h17-stageb). src/ph25.py (Agent11 = Release + Agent9; sha 5620a908...7d91, source doc
  dce688892e4db423c). Bench (record:h24-run2-bench-result): every identity and implementation bar PASS (M7(a) exact
  400/400 in T3a, 382/382 in the Lost world; counter exact 400/400, held-only presence 0; W1 dwell Agent11 22.7 vs
  Agent10 11.9 vs Agent6 24.4), but bench (h) T1: P(V) Agent11 0.785 vs Agent10 0.958, paired DP -0.1725
  [-0.2125, -0.1350], M2(b) pass probability 0.0000 < 0.5: STOP. No bar decision, no development run, no evaluation;
  seeds 9919/9929 and 1815/1915 unused.
- **H24 Run 2 N sweep, measurement only (2026-09-24).** The owner chose the recommended option ('우리 그 다음 테스트는
  추천안대로'; decision:h24-run2-n-sweep). src/ph25b.py (sha ad12a912...eaf6, source doc df429960dec38ae4c; ph25.py
  unchanged), bench seeds only, N 60 to 450 and inf (record:h24-run2-n-sweep-result; report doc d06b9ef9d8775e587,
  experiments/h24/h24_run2_nsweep.md): no swept N meets both targets. T1 DP vs Agent10 about -0.17 for N 60-150,
  -0.0125 [-0.025, -0.0025] at 200, 0 from 300; W1 dwell with M5(b) passing only at N 60/90/120 (22.7/22.7/24.8),
  19.6 at 150 (M5(b) 0.034), 17.8 at 200. Recommendation on record: close Run 2 at the bench stop, then H17.
- **H24 Run 2 CLOSED as NOT shown (2026-09-24; decision:h24-run2-closed).** The owner accepted the recommendation
  ('일단 fruit fly 제안 추천에맞게 진행하고 laya는 추후 전달'). Stopped at bench (h) by the registered stop rule (Agent11 -
  Agent10 paired DP -0.1725 [-0.2125, -0.1350] on bench seeds; M2(b) pass probability 0.000); no candidate; T1/T2/T3
  never run; seeds dev 9919/9929 and eval 1815/1915 unused and registered to H24 Run 2. The N sweep is the measured
  reason (no fixed N meets both targets; record:h24-run2-n-sweep-result). Nothing adopted; the Run 2 relaxation
  (decision:classification-rule-relaxed-presence-counter-run2) lapses. Adaptive presence queued after H17, proposed,
  not decided.
- **H17 opened for design; design v1 DRAFT (2026-09-24; decision:h17-open-design).** Same owner message. Doc
  de696df4b5963d1c1 (experiments/h17/h17_design_v1.md, sha 8180e889...bc15f; concept:h17-cold-search), no code. A
  navigation hypothesis: Agent12 = Search + Agent10; after S 210 silent steps with nothing held and no whiff of any
  odour, a crosswind cast of growing amplitude (legs 30 k steps) slanted 15 degrees along the wind, the slant
  reversing every 360 steps. One new counter q (steps since the last whiff of any odour) needs a signed H17-scoped
  relaxation (H14 format). Bench (a)-(d) with (c1) bars 0.40 / 0.30 / +0.30 and stop rules (h1) / (h2); tasks T1-T4
  with bars T1 DP >= -0.05, T2 dwell vs Agent10 >= -1.2, T3 lost-row DP <= -0.05, P(V) DP >= -0.02 and contacts
  <= 0.10 per row, T4 reported. Seeds dev 9943/9953, eval 1945/2045, bench 20261051/20261052, bootstrap 20261053
  checked unused. Awaiting the owner's confirmation of section 12.
- **H17 opened on design v2 FINAL (2026-09-24; decision:h17-open).** The owner answered section 12 with '그래 그방향으로
  진행' ('yes, proceed in that direction'): every recommended option. The relaxation signed for H17 only
  (decision:classification-rule-relaxed-any-odour-silence-counter-h17: ONE counter q, steps since the last whiff of
  any odour). Design v2 FINAL doc d83a917ea4152b4a7 (experiments/h17/h17_design_v2.md, sha f94d6ace...7516); v1
  kept as history. src/ph26.py (sha 1c9b6f5b...67cf, source doc d911535d7e535751c): Agent12 = Search + Agent10, no
  adopted module edited; demo self-checks all pass (two failed self-checks fixed first, neither in the rule).
- **H17 STOPPED at the bench: no candidate by the registered rule (2026-09-24; record:h17-bench-result).** (a)
  identities all True; (b) engagement exact 400/400; (c1) bars PASS: from the R3 stranded state Agent12 senses a
  whiff within 300 steps of engagement in 0.542 [0.494, 0.591] (Agent10 0/400), reaches a source within 600 in
  0.698 [0.651, 0.740], paired DP +0.5425 [+0.4925, +0.5925]. (d) FAILS: in T1 +1/0 18/400 rows engage, 0.045
  [0.029, 0.070], upper bound above 0.05 (predicted 0.0025-0.02). Stop rules did not fire ((h1) 1.0000, T1 DP
  -0.0025; (h2) 0.6324, lost-row DP -0.0850). Tasks NOT run; dev 9943/9953 and eval 1945/2045 unused. The owner
  decides.
- **H17 post-bench diagnosis, measurement only (2026-09-24; decision:h17-post-bench-diagnosis,
  record:h17-post-bench-diagnosis-result).** The owner chose option 3 ('3번 진단 먼저 진행해', 'run the diagnosis, option
  3, first'). src/ph26b.py (sha 6b45d87c...e0ae, source doc d6bd7048dbe6be461) imports ph26 unchanged; bench seeds
  only; the bench re-run equals ph26_bench.txt line for line. (A) The 18 T1 silences of >= 210 steps are tracking rows
  (Agent10 V 15/18): 16 begin after the agent had been at a source, 16 with `since` 1, most steps upwind of both
  sources (majority class in 16/18), and 14 are back inside a whiff region (d_along 14.5-24.6) when q reaches 210; S
  210 sits at about p95 of Agent10's longest silence (207). Only row 184 changes outcome (V to N). (B) All 99 (h2)
  contacts are engaged, in legs 3-4 on the upwind slant (none in legs 5-6), in 39 Agent10-stranded rows, lost in both
  arms, no whiff after any contact; the contact rows carry no paired transition (all 19 into V and 37 out of lost are
  in engaged rows without a contact). Report doc d6f5ab6a423f8ba16 (experiments/h17/h17_post_bench_diagnosis.md).
  Nothing adopted; the H17 verdict unchanged. The owner decides between closure and a Run 2 design.
- **H17 Run 2 opened for design; design v1 DRAFT (2026-09-24; decision:h17-run2-open-design).** The owner chose
  option 2: '2번 Run 2 설계 v1 초안 진행' ('option 2, proceed with the Run 2 design v1 draft'). Run 1's verdict unchanged
  (stopped at the bench, no candidate, nothing adopted; its seeds stay registered to Run 1). Doc dedd3d11f43f9156f
  (experiments/h17/h17_run2_design_v1.md, sha 27bbd399...94dc), no code. Recommended: engagement at q >= 250 (q
  unchanged; 6/400 T1 rows reach 250 against 18 at 210 on Run 1's bench seeds); own-state separators rejected (`since`
  equals q in the tracking-loop silences, measured 16/18, and in the stranded state, read from ph21.py:71-75 and
  checked exactly at the bench); leg rule kept, T3 (c) re-signed (H14 format) to 'out-of-lost rows whose first
  post-engagement whiff follows a wall contact <= 0.10', contacts reported; (d) kept at 0.05 (pass 0.98 binomial,
  0.91 predictive); the q relaxation re-signed in form for Run 2; bench adds (b') and a W1 bench-seed reading (h3)
  with a proposed stop rule. Binding risk stated: T3 (a) pass probability about 0.5-0.6; joint about 0.32 if W1
  holds. Seeds dev 9961/9973, eval 1965/2065, bench 20261061/20261062, bootstrap 20261063 (181 files scanned, one
  collision replaced). Awaiting the owner's confirmation of section 12.
- **H17 Run 2 opened on design v2 FINAL (2026-09-24; decision:h17-run2-open).** The owner answered section 12 with
  '권고안대로 확정하고 Run 2 진행' ('confirm as recommended and proceed with Run 2'): every recommended option. Recorded
  before any code: the q relaxation re-signed in form for H17 and H17 Run 2
  (decision:classification-rule-relaxed-any-odour-silence-counter-h17-run2) and T3 (c) re-signed in H14 format
  (decision:h17-t3c-bar-resigned-run2: among rows leaving lost, the fraction whose first whiff after engagement follows
  a wall contact, point <= 0.10). Design v2 FINAL doc d73c77ebd99d50d86 (experiments/h17/h17_run2_design_v2.md, sha
  d2374c5e...d5e9; wording only changed from v1). src/ph27.py (sha d12fa651...143a, source doc ddfbebac743e3c469):
  Agent13 = ph26's Search rule at S 250 on Agent10, ph26.py imported unchanged; demo self-checks all pass on the first
  run.
- **H17 Run 2 STOPPED at the bench by the registered (h2) stop rule (2026-09-24; record:h17-run2-bench-result).** Every
  no-candidate part passes: identities (incl. (a4), Agent13's code at S 210 == ph26.Agent12 bitwise), (b) and (b')
  400/400, (c1) whiff within 300 steps of engagement 0.578 [0.529, 0.625], reach within 600 0.635 [0.587, 0.681], DP
  +0.5775 [+0.5300, +0.6225], (d) 4/400 = 0.010 [0.004, 0.025]. But on T3 (+1/-1) the lost-row DP is -0.0650 [-0.0900,
  -0.0425] (26 rows out of lost, 0 into; predicted -0.079 to -0.085), so T3 (a)'s pass probability is 0.2287 < 0.5:
  STOP. (h1) 1.0000 (T1 DP 0), (h2c) 1.0000 (0/26 contact-mediated; contacts 0.000 per row), (h3) 1.0000 (W1 dwell DP
  +1.750 [+1.173, +2.343]). Also: `since` - q is 0 in 376/400 (b'2) rows and 70/105 engaged stranded task rows, so the
  design's section 2 (E) reading holds only in part (printed notice; not a mechanism failure). Tasks NOT run; dev
  9961/9973 and eval 1965/2065 unused; nothing tuned. The owner decides.
- **H17 Run 2 post-bench diagnosis, measurement only (2026-09-24; decision:h17-run2-post-bench-diagnosis,
  record:h17-run2-post-bench-diagnosis-result).** The owner chose option 2 ('2번 진단 먼저 진행', 'run the diagnosis,
  option 2, first'). src/ph27b.py (sha a6232c09...79ac, source doc d9e169fcd01da251b) imports ph27 and ph26 unchanged;
  bench seeds only; the bench re-run equals ph27_bench.txt line for line and the (h2) headline reproduces. (A) Of 134
  stranded rows 105 engage (the other 29 are released at step 414 or later); 18 whiff after engagement, 87 do not. The
  87 sit about 29 outward of the negative source's axis at engagement (81/87), and the pair is first crossed at the
  end of leg 4 (u about 292), upwind of both sources in 63/64. In the 84 rows engaged by step 399, leg 1 (and so leg 3)
  is on the flee side in 65, and those whiff 5/65 against 13/19 with leg 1 toward the pair ((c1): 184/194 vs 47/206).
  The factor that missed the prediction is the whiff fraction after engagement: 18/84 = 0.214 against 0.5-0.7 (a whiff
  then leaves lost in 17/18). (B) `since` - q > 0 in 35/105 task rows and 24/400 constructed rows, all by one
  mechanism: the last negative whiff came with nothing held, 1-6 steps before the negative hold formed, so it was not
  nav (ph21.py:69, :72), and no hit followed while held. Design section 2 (E) holds in 70/105. Report doc
  dd1ba5b405811ef4a (experiments/h17/h17_run2_post_bench_diagnosis.md). Nothing adopted; the Run 2 verdict unchanged.
  The owner decides: close H17, or a Run 3 design.
- **H17 CLOSED as NOT shown under its registered criteria (2026-09-24; decision:h17-closed).** The owner chose option 1:
  '1. H17 종료, 등록된 순서대로 adaptive presence(제안) → H20 Stage B' ('option 1: close H17; proceed in the registered
  order, adaptive presence (proposed), then H20 Stage B'). Run 1 stopped at its bench on part (d) (18/400, upper bound
  0.070 against 0.05), Run 2 by its (h2) stop rule (T3 lost-row DP -0.0650 [-0.0900, -0.0425], pass probability
  0.2287); T1-T4 never run; dev/eval seeds of both runs unused and kept registered; nothing adopted; the H17 relaxations
  and the Run 2 T3 (c) re-sign lapse. The measured facts are recorded apart from the verdict (the search finds a plume
  from the constructed stranded state, (c1) 0.542 and 0.578 against 0/400; the task-level whiff fraction after
  engagement 18/84 = 0.214 against 0.5-0.7 is the factor that missed). Cold-start search stays a recorded limit; the
  release at negative values stays ON HOLD.
- **H26 (adaptive presence) opened for design; design v1 DRAFT (2026-09-24; decision:h26-open-design).** Same owner
  message; the number H26 assigned by that decision. Doc d9452710c5166ba01 (experiments/h26/h26_design_v1.md, sha
  18983aa2...3598; concept:h26-adaptive-presence), no code. Recommended: the presence prior separated from the window
  (one counter per odour starting at 240, so an odour never sensed is present on steps 0-58, window 300 after any
  whiff; Agent14 = Release + Agent9 with the start value; no second state variable; a new H26-scoped relaxation to
  sign). Candidates (a)-(d) rejected on record. Bench (m) measures T1's rows without an early valued whiff before the
  (h) T1 and (h3) W1 stop rules are read; M5(d) re-sign against Agent10 recommended (the inherited prediction contradicted
  by two benches). Seeds dev 9977/9987, eval 1985/2085, bench 20261071/20261072, bootstrap 20261073 (189 files scanned,
  no collision). Awaiting the owner's confirmation of section 12.
- **H26 opened on design v2 FINAL (2026-09-24; decision:h26-open, owner '권고안대로 확정하고 H26 진행', 'confirm as
  recommended and proceed with H26').** Every recommended option of v1 section 12 confirmed; signed before any code: the
  H26-only relaxation (decision:classification-rule-relaxed-presence-prior-h26: one presence counter per odour, window
  300, start 240 as a prior) and the M5(d) re-sign against Agent10 (decision:h26-m5d-bar-resigned). Design v2 FINAL doc
  d54441658b54a6799 (experiments/h26/h26_design_v2.md, sha ac95c22d...9f54).
- **H26 bench: M4 PASS, both stop rules continue (2026-09-24; record:h26-bench-result).** src/ph28.py (sha
  29c594e4...6dd7, BARS unset; source doc d4f81b6d946b6ccfb): Agent14 = Release + Agent9 with the counter starting at
  240. Every identity True; counter exact 400/400; W1 first surge at or after 59 400/400; T3a window 400/400; Lost-world
  window at L + 300 385/385. (m) printed first: at-risk rows 15, k = 1. (h) T1 DP Agent14 - Agent10 +0.0025 [-0.0050,
  +0.0100], M2(b) pass probability 1.0000; (h3) W1 paired dwell -1.7775 at bar -4.9, pass probability 1.0000. The run
  was resumed after the previous agent was cut off right after the bench; the bench record was written at resumption.
- **H26 M5(b) bar fixed from the bench (2026-09-25; decision:h26-t2-dwell-bar).** bar_T2 = -0.20 x D6_W1 = -0.20 x
  24.7200 = -4.9, by the registered rule, before any task seed was used; written into ph28.py as BARS['T2'] (sha now
  64ce7d0c...e7aa, the only line changed; demo re-run, ph28_demo_bar.txt). Development run 9977/9987: no operation
  error, no amendment (record:h26-dev-run).
- **H26 evaluated once (2026-09-25; 1985/2085; record:h26-result; report doc d8163e16317b251eb,
  experiments/h26/h26_report.md): SHOWN under the registered criteria (M1-M7 PASS).** T1 Agent14 P(V) 0.927 [0.898,
  0.949], DP vs Agent10 -0.0075 [-0.020, +0.005] (5 rows out of V, all in the 20 at-risk rows; k 5); W1 paired dwell vs
  Agent6 -1.047 [-2.043, -0.075] against -4.9; W1 lost rows vs Agent10 -0.025 [-0.055, +0.005] (vs Agent6 +0.0475
  [+0.0200, +0.0775], reported); T3a window exact 400/400, R 1.0376 [0.9642, 1.1186]. Not shown: a loss after tracking
  (T3b, a fixed 300-step window: 4.412 against Agent11 (N 60) 5.772) and negative values (T4 reported, == Agent10).
  Nothing adopted; awaiting the owner's closure.
- **H26 CLOSED as SHOWN; the presence counter and Agent14 adopted within the tested conditions (2026-09-25;
  decision:h26-closed, decision:h26-adaptive-presence-adopted-within-tested-conditions).** The owner answered '1.
  shown으로 종료하고 채택, H20 Stage B 진행' ('option 1: close as shown and adopt; proceed to H20 Stage B'). Not re-judged;
  one evaluation. Adopted: the presence counter starting at N_hi - P = 240 (P 60, N_hi 300) on the H23 filter; the adopted
  agent is now Agent14 = Release + Agent9 (src/ph28.py:92-97), within supplied +1/0, G 2, C0, gate on, release on,
  learning off, T1 / W1 / T3a. Limits: a loss after tracking not shown (T3b 4.412); negative values excluded (the
  release's negative scope stays ON HOLD); W1 lost rows vs Agent6 +0.0475 reported. The H26 relaxation stays in force
  for the adopted counter; the M5(d) re-sign applies to H26 only.
- **H20 Stage B opened for design; design v1 DRAFT (2026-09-25; decision:h20-stage-b-open-design).** Same owner message.
  Doc da31fd8fe14fd6444 (experiments/h20/h20_stage_b_design_v1.md, sha 0ca7f6c1...9248), no code. The learning check:
  the value learned by the agent's own module (H15 E2 protocol off-world: neutral odour 30 steps, 50 silent steps,
  valued odour 30 reinforced steps; sham without reinforcement), read out into `known` (the array Agent14 reads; no
  module edited), frozen in the test; T1 main, W1 and T3a reported, +1/-1 excluded. Read from the code: the learned
  valued value is exactly +1.0; the neutral odour keeps a small positive residual (about +7e-6, or about +0.1 where the
  two codes share a unit); presented in the opposite order it would be slightly NEGATIVE and flip Agent14 into the
  +1/-1 regime, so the order is fixed (neutral first) and the check has a sign clause (0 <= neutral <= +0.15).
  Recommended bars: learned - supplied >= -0.05, learned - sham >= +0.20, cells >= 0.70, vs learned Agent10g >= +0.05
  (0.88 reported); stop rules (h) and (hL). Seeds dev 9983/9989, eval 2005/2107, bench 20261081/20261082, bootstrap
  20261083 (198 files scanned; four collisions replaced). Awaiting the owner's confirmation of section 12.
- **H20 Stage B OPENED on design v2 FINAL (2026-09-25; decision:h20-stage-b-open).** The owner answered '권고안 적용'
  ('apply the recommended options'): every recommended option of design v1 section 12 confirmed. Design v2 FINAL doc
  d3f2ce9707790cd87 (experiments/h20/h20_stage_b_design_v2.md, sha 28c1010f...66ae): v1 with section 12 resolved; no
  bar, seed, arm, prediction or rule changed. No relaxation and no bar re-sign (no new state).
- **H20 Stage B code, demo and bench (2026-09-25; record:h20-stage-b-bench-result).** src/ph29.py (sha 122c1925...799c,
  source doc dbcf264395e76d71a): the H15 E2 training on the agent's own module, neutral first, the read-out written
  into `known`, frozen; no adopted module edited. Demo every check ok (ph29_demo.txt). Bench on 20261081/20261082 (M4
  PASS): the learned valued value is exactly +1.0 in 400/400 rows, the neutral residual positive in 400/400 (7.13e-6
  where the codes share no unit, 0.1000064 where they share one); sham exactly 0; ML 30/400 failing (the rows sharing
  two or three units) against the bound 40; every identity True, including learned with `known` := +1/0 == supplied
  and the reproduction of H26's T1; a single neutral whiff holds at gain 1.2 and 1.4 in every row; T1 learned ==
  supplied in outcome (381/16/3), DP 0.0000, (h) pass probability 1.0000, (hL) continue.
- **H20 Stage B development run (2026-09-25; 9983/9989; record:h20-stage-b-dev-run):** no operation error, no
  amendment.
- **H20 Stage B evaluated once (2026-09-25; 2005/2107; record:h20-stage-b-result; report doc d66ad8dea08c92116,
  experiments/h20/h20_stage_b_report.md): SHOWN under the registered criteria** (ML readable, M1, M2, M3, M4, M6 PASS;
  W1 and T3a reported). T1 learned Agent14 369/30/1 = supplied 369/30/1, P(V) 0.922 [0.892, 0.945]; DP learned -
  supplied 0.000 [0.000, 0.000] (no row changed its outcome; 117 rows, all with shared code units, changed trajectory);
  learned - sham +0.467 [+0.415, +0.522]; cells 91/90/95/93 (lower bounds >= 0.826); learned Agent14 - learned Agent10g
  +0.367 [+0.318, +0.417]. W1 and T3a: learned == supplied row for row. A statement about a saturating off-world
  training, neutral first, learning frozen in the test; not about learning during behaviour (Stage C), negative or
  sub-saturating learned values. Nothing adopted; awaiting the owner's closure.
- **H20 Stage B CLOSED as SHOWN (2026-09-25; decision:h20-stage-b-closed).** The owner answered 'Stage B를 shown으로
  종료. 채택할 새 메커니즘은 없고(학습 모듈과 read-out 경로는 이미 채택된 것) "학습된 양의 가치가 시험 조건 안에서 행동에
  쓰인다"는 결과를 기록으로 확정. 다음은 등록된 순서대로 H20 Stage C 설계: 학습을 켠 채 H15 Run 2 세계에서 통합 검사.'
  ('Close Stage B as shown. There is no new mechanism to adopt (the learning module and the read-out path are already
  adopted); fix on record the result that "a learned positive value is used in behaviour within the tested
  conditions". Next, in the registered order, the H20 Stage C design: the integration check with learning on, in the
  H15 Run 2 world.'). Not re-judged. The result fixed on record: a learned positive value is used in behaviour within
  the tested conditions (H15 E2 training off-world, neutral first, saturating dose, read out into `known` and frozen;
  World7 T1; Agent14; G 2; C0; gate and release on; the H26 counter). Nothing new adopted: the learning module
  (decision:phase7-2-gate, with H15 Run 2's loop) and the read-out path (chan_valence, ph14.py:52-55, and the `known`
  array Agent14 reads) were already adopted. Measured apart from the verdict: the learned valued value is exactly +1.0,
  so learned == supplied in outcome on every row (117 rows differ in trajectory, none in outcome).
- **H20 Stage C opened for design; design v1 DRAFT (2026-09-25; decision:h20-stage-c-open-design).** Same owner
  message. Doc dc7e62aeab81c347b (experiments/h20/h20_stage_c_design_v1.md, sha b89e9ff9...72a9), no code. The
  integration check: Agent14 with learning ON in the H15 Run 2 world (World6; E1 5400 steps; E2 training 30 / gap 50 /
  30, learning on in the test), H15 Run 2's agent reproduced first on its own seeds and used as the paired reference.
  Read from the code: the adopted act reads `known` directly for the flee (ph23.py:77) and fails with `known` None, so
  the module's read-out is written into `known` before every act by the harness (no module edited, no new state); ph15's
  harness cannot drive Agent14 (the `rule` attribute is the gate flag, ph19.py:42). The gain: fewer R-start rows
  visiting the not-yet-learned punisher (Run 2: 52/200 with learning and without, 3/200 known) against H15 Run 2's
  agent and against Agent14 with its learned positive values removed; Run 2's Q1-Q6 kept (Q3(c)'s WIN registered on
  the rows where the baseline is above the floor, the tie rule kept). The punisher's negative value under the release
  is put to the owner: recommended (N2), the release applied only at non-negative held values (a scoped composition
  rule to be signed in H14 format before code), with Agent14 as composed reported; inferred: as composed, about half
  of the P-start rows would be stranded (R3's 0/131). Stop rules (h), (hS), (hR). Seeds E1 dev 9982/9984, eval
  2037/2115; E2 dev 9986/9988, eval 2043/2141; bench 20261091/20261092, 20261094/20261095; bootstrap 20261093 (206
  files scanned; eight file and three graph collisions replaced). Awaiting the owner's confirmation of section 12.
- **H20 Stage C OPENED on design v2 FINAL (2026-09-25; decision:h20-stage-c-open).** The owner answered
  '권고안대로 확정하고 Stage C 진행' ('confirm as recommended and proceed with Stage C'): every recommended option of
  design v1 section 12 confirmed. First, in H14 format and for Stage C only, the release rule at negative holds was
  signed (decision:release-value-gated-stage-c: the H25 release (S)+(Z) is not applied while the held odour's own value
  is negative; decision:release-negative-scope-on-hold stays in force outside Stage C; nothing adopted). Design v2
  FINAL doc d27e6dfe2e2c16183 (experiments/h20/h20_stage_c_design_v2.md, sha f1e19095...453a): v1 with section 12
  resolved; no bar, seed, arm, prediction or rule changed.
- **H20 Stage C code, demo and bench: STOPPED at the bench by the (hR) stop rule (2026-09-25;
  record:h20-stage-c-bench-result).** src/ph30.py (sha 98822834...59bd, source doc d3a2e1142563d7b38): a harness that is
  ph15.simulate step for step plus the per-step mirror of the module's read-out into `known`, and the (N2) subclass; no
  adopted module edited. Demo 10/10 ok. Bench on 20261091/20261092 and 20261094/20261095: (r) H15 Run 2 reproduced
  line for line (266/266 lines of ph15_run2.txt); every identity True; (v) exactness True. (h) R-start rows visiting the
  punisher: learned Agent14 10/200, H15 Run 2's agent 64/200, positive-off 90/200 (DP -0.270, pass probability 1.0000),
  continue; (hS) 1.0000 and 1.0000, continue (P-start late unrecovered 19 vs 21; reach after punishment 192 vs 192 of
  199). **(hR): Agent14 no-learning's GM last-third punishing dwell in G3 16.000 [0.000, 19.667] does not PASS 'at
  least 10' -> STOP; the tasks were not run; no development or evaluation seed was used.** Printed beside: Agent14 as
  composed (N1) left 122/200 P-start rows unrecovered (the stranding inferred in design 3.6). The first bench run had
  printed 'no candidate' on an identity whose only unequal field was a harness measure (hold_pos) reading the clipped
  read-out; fixed, recorded, re-run: every other line identical, (hR) STOP in both. Awaiting the owner.
- **H20 Stage C post-bench diagnosis, measurement only (2026-09-25; decision:h20-stage-c-post-bench-diagnosis,
  owner '2번 진단 먼저 진행', 'run the diagnosis, option 2, first'; record:h20-stage-c-post-bench-diagnosis-result).**
  src/ph30b.py (sha 4e4122c8...be59, source doc df098689fe0f428d4) imports ph30 unchanged; bench E1 seeds and the bench
  bootstrap seed only. The bench's (h), (hR) and printed-beside lines reproduce verbatim (23/23). 'GM' is the group
  median (spec v3 line 36, ph15.py:180). The no-learning Agent14 floor ends every G3 row at one source: 88 at the reward
  source (last-third punishing dwell 0; none lost, none at a wall, no definition mismatch) and 111 at the punisher
  (median 24); with 44.2 percent of rows at 0, 5.26 percent of bootstrap resamples have median 0, hence 16.000 [0.000,
  19.667] (Run 2's computation: [0.000, 20.333]). The 0-dwell rows are those that sensed R whiffs with nothing held after
  the H25 release ended their P holds (48 steps after the last whiff); none returned to P. M4(c)'s WIN on G3+ is 111/0/0
  (no ties); the floor GM on G3+ (and on no-learning dwell >= 1, 5, 10) is 24.000 [22.667, 24.667]; H15 Run 2's agent
  without learning reads 21.000 [19.667, 22.667] (55 rows at 0, also at R). Report doc ded5da7a47fb9e759
  (experiments/h20/h20_stage_c_post_bench_diagnosis.md); output experiments/h20/ph30b_diag.txt (sha 69c9867c...4ae8).
  Stage C's verdict unchanged; nothing adopted. Awaiting the owner.
- **H20 Stage C Run 2 opened for design; design v1 DRAFT (2026-09-25; decision:h20-stage-c-run2-open-design).** The
  owner answered '다음도 권고안에 따라 작업 진행' ('proceed with the next work too, according to the recommended option'):
  the Run 2 design, the recommended option. Stage C Run 1's verdict unchanged (stopped at the bench by (hR), no bar
  decision); nothing adopted; Run 1's development and evaluation seeds unused and kept registered to Run 1. Doc
  dfad8d4ed6b1d7675 (experiments/h20/h20_stage_c_run2_design_v1.md, sha b091d7f0...71b6), no code. Recommended: M4(c)'s
  readability re-signed in H14 format (Run 2 only) to read on G3+, the rows the WIN is already read on (G3+ at least 50,
  floor GM lower bound >= 10; on the bench 111 rows, 24.000 [22.667, 24.667], resampled bench rows 1.000 against 0.178
  for the present rule); what it gives up stated (G3+ is chosen by the floor's own outcome; the 88 rows it drops ended at
  the reward source; losses there are invisible to the WIN) and reported beside (the floor over all G3, the all-G3 WIN
  with its ties, the dropped rows' end state, H15 Run 2's agent without learning as a floor); the tie rule untouched;
  (hR) restated as a pass probability on the bench rows with a G3+ >= 50 guard; (N2) re-signed in form for Run 2; a new
  ph31.py importing ph30 unchanged. Predictions from Agent14's own bench numbers: M4 about 0.98-0.99, joint about 0.83 to
  0.94 (M3(a) binding). Seeds E1 dev 9955/9959, eval 2057/2159; E2 dev 9967/9975, eval 2061/2163; bench
  20261111/20261112, 20261114/20261115; bootstrap 20261113 (216 files scanned; one file and three graph collisions
  replaced). Awaiting the owner's confirmation of section 12.
- **H20 Stage C Run 2 OPENED on design v2 FINAL (2026-09-25; decision:h20-stage-c-run2-open).** The owner's standing
  instruction '다음도 권고안에 따라 작업 진행' ('proceed with the next work too, according to the recommended option'),
  given before the Run 2 design was written, applied to every recommended option of design v1 section 12. Before any
  code, in H14 format: M4(c)'s readability re-signed for Run 2 only to read on G3+ with G3+ >= 50
  (decision:h20-stage-c-m4c-readability-resigned-run2, the proposed Korean wording of design 3.3 adopted as the owner's
  words) and (N2) re-signed in form for Stage C Run 1 and Run 2 (decision:release-value-gated-stage-c-run2). Design v2
  FINAL doc d007990ab333e7194 (experiments/h20/h20_stage_c_run2_design_v2.md, sha 48fdd1f3...e4f2): v1 with section 12
  resolved; no bar, seed, arm, prediction or rule changed.
- **H20 Stage C Run 2 code, demo, bench (M9 PASS) and development run (2026-09-25;
  record:h20-stage-c-run2-bench-result, record:h20-stage-c-run2-dev-run).** src/ph31.py (sha 77440037...ec80, source
  doc d4c5f81249ef02a9e) imports ph30 and ph30b unchanged. It was written by a session cut off by a rate limit before any
  run; the resuming session read it against the design, added readings R13 and R14 and a completion note, and changed no
  bar, seed, arm or rule. Demo 8/8 ok. Bench: (r) H15 Run 2 reproduced 266/266; (r') Run 1's bench reproduced 370/370
  through ph30 as imported, and the re-signed readability read Run 1's rows exactly as expected (G3+ 111, 24.000
  [22.667, 24.667], WIN 111/0/0, (hR2) 1.000); identities and (v) exactness True; (h) R-start punisher visits 18 vs 65
  of 200, pass probability 1.0000; (hS) 1.0000 and 1.0000; (hR1) G3+ 107 of 200; (hR2) 1.0000; no stop. Development
  run clean, no amendment.
- **H20 Stage C Run 2 evaluated once: SHOWN under its registered criteria (2026-09-25; record:h20-stage-c-run2-result;
  report doc de5963e5a73875a97, experiments/h20/h20_stage_c_run2_report.md).** M1 to M9 all PASS. With learning on in
  the H15 Run 2 world, Agent14 (N2) sent 8 of 200 R-start rows to the not-yet-learned punisher, against 56 for H15 Run
  2's agent (DP -0.240 [-0.300, -0.180]) and 91 with its positive values removed (DP -0.415); late unrecovered 18/400;
  M4 read with the re-signed readability (G3+ 112, floor GM 23.333 [22.667, 24.500]; WIN 112/0/0); reach after
  punishment 188 vs 189 of 199; E2 reach trained 373 vs sham 142 of 400. Reported beside, no bar: the floor over all G3
  18.667 [0.000, 20.667] (Run 1's rule would have read M4 (b), (c) unreadable); the all-G3 WIN 112/85/2, unreadable by
  the tie rule; the 87 rows outside G3+ all ended at the reward source, with the learned arm above 0 in 2 of them (the
  losses hidden from the G3+ WIN); H15 Run 2's agent without learning 22.000 [21.000, 22.667] with 40 rows at 0. A count
  in the evaluation output equals one of Run 1's seed numbers by chance (reported; no seed used). Nothing adopted.
  Awaiting the owner: Stage C's closure and H20 as a whole.
- **The owner's decisions of 2026-09-25: '1. shown으로 종결 및 n2는 범위 권고안으로 적용 2. 미입증안 해결책이 없나? 3,4
  권고안으로 진행'** (gloss: '1. close as shown, and apply N2 with the recommended scope; 2. is there no resolution for the
  not-shown ones?; 3 and 4: proceed with the recommended options').
  (1) **H20 Stage C Run 2 CLOSED as SHOWN** (decision:h20-stage-c-run2-closed): one evaluation, M1-M9 PASS; not re-judged;
  reported apart from the verdict: the all-G3 floor 18.667 [0.000, 20.667], the all-G3 WIN 112/85/2 unreadable, 2 losses
  hidden from the G3+ WIN (rows 136, 230), the Agent3 floor 22.000, three missed predictions, the resumed run.
  **The value-gated release (N2) ADOPTED** (decision:n2-release-adopted-within-tested-conditions): the adopted agent is now
  Agent14N2 = ReleaseN2 + Agent14 (src/ph30.py:117-140); at non-negative held values N2 is the H25 release by code
  (ph30.py:128-132) and by the Stage C bench identity (ph30_bench.txt line 326), so every H25/H26 adoption condition carries
  over; with a negative value held the release is off by rule (tested in World6 with learned values, Stage C Run 2 M3-M5);
  decision:release-negative-scope-on-hold is SUPERSEDED (the hold lifted by switching the release off at negatives, not by
  adopting it there). Limits: supplied +1/-1 in World7 not run with N2 (that the R3 stranding cannot arise is read from the
  code, not measured); T3b and cold start unchanged. Rejected on record: Stage C only; the release at negatives ((N1)).
  (2) **H20 CLOSED as a whole** (decision:h20-closed): Stage A NOT shown, Stage A Run 2 NOT shown, Stage B SHOWN, Stage C
  Run 1 stopped at the bench, Stage C Run 2 SHOWN. The resolution of the not-shown stages, the interpreting assistant's
  recommendation applied under point 2's question and the '3,4 권고안으로 진행' pattern: Stage A's question was answered under
  the registered criteria of H23 (0.953, DP vs maintain +0.240), H26 (Agent14 0.927 against the filter-off Agent10g 0.635,
  +0.292) and Stage B (+0.367 vs learned Agent10g); the link check found Stage A's first-reach measure inexpressible in C0;
  the dwell-majority re-run with the adopted pathway is H26's evaluation; so no Stage A re-run, and **Stage A's verdicts are
  NOT re-judged**. Conclusion: a positive value, supplied or learned, controls which source the adopted agent stays at
  within the tested conditions, and with learning on in the H15 Run 2 world it keeps Run 2's search, avoidance and reach
  while reducing punisher visits.
  (3) **Seed-scan exception** (decision:seed-scan-exclusion-ph31-eval): the number 2115 (Stage C Run 1's E1 evaluation
  agent seed) in experiments/h20/ph31_eval.txt line 175 is a whiff count; the (file, number) pair is excluded from every
  future seed scan; the output, ph30.py and ph31.py are not edited; ph30's self-check now lists ph31_eval.txt and ph31's
  demo check 6 would fail on re-run (known).
  (4) **H27 OPENED FOR DESIGN** (decision:h27-open-design): the queued distractor condition, a third irrelevant odour;
  design v1 DRAFT doc d1b2bdacd81997da7 (experiments/h27/h27_design_v1.md, sha256 483c38f4...2584), no code. Awaiting the
  owner's confirmation of section 12.
- **H27 OPENED on design v2 FINAL (2026-09-25; decision:h27-open).** The owner answered the v1 DRAFT '권고안으로 이어서
  진행' ('continue with the recommended options'): every recommended option of section 12 confirmed (nine points).
  Signed first, in H14 format, H27 only: decision:evidence-release-composition-rule-h27 (the evidence release compares
  the held channel with the strongest non-held channel; identical at N 2; a composition rule in the new file, ph23.py not
  edited) and decision:classification-rule-relaxed-presence-prior-h27 (the H26 relaxation re-signed in form for one
  counter per odour including D). Design v2 FINAL doc d8c8949f2896cf1ec (experiments/h27/h27_design_v2.md, sha
  88fdfdf7...7ddb): v1 with section 12 resolved; no bar, seed, arm, prediction or rule changed.
- **H27 code, demo and bench: STOPPED at the bench by all three stop rules (2026-09-26; record:h27-bench-result).**
  src/ph32.py (sha d9f585d5...2743, source doc d5a2b6526d40efbef): Agent15 = ReleaseN2 + Agent14 + Act15 (Agent9's act
  with the evidence line replaced), the stage, circuit (third unit's noise on its own generator), codes and counter
  rebuilt for three channels after the adopted constructor; no adopted file edited. Demo 8/8 ok (one fix of the demo's
  own table check, recorded in its header: the design's M5(b) illustration has a hand-arithmetic slip at -3.0, 0.99
  against the formula's 0.955). Bench on 20261121/20261122: M4 PASS (every identity (I1)-(I6) True; (b3), (c), (d)
  exact). **(h) T1D: P(V) D on 0.787 vs D off 0.920 (== Agent14N2), DP -0.1325 [-0.1675, -0.1000], M2(b) pass
  probability 0.0000 -> STOP. (hW) W1D: dwell 4.968 vs 24.750, paired -19.7825 against the rule bar -5.0; lost rows
  400/400 vs 22; wall contacts 105.6 per row; M5(b) and M5(d) 0.0000 -> STOP. (hH) the hold-not-read arm also lost
  400/400, DP +0.0000, M6 0.0000 -> STOP.** The release-off arm lost 400/400 too. The tasks were not run; no development
  or evaluation seed was used; decision:h27-w1d-dwell-bar not recorded (the bench did not pass its stop rules); nothing
  tuned. Awaiting the owner.
- **H27 post-bench diagnosis, measurement only (2026-09-26; decision:h27-post-bench-diagnosis, owner '진단 먼저',
  'the diagnosis first'; record:h27-post-bench-diagnosis-result).** src/ph32b.py (sha 4c8adf5e...9f10, source doc
  de72961845e8a258b) imports ph32 unchanged; bench seeds only. ph32.bench() re-run reproduces ph32_bench.txt line for
  line (60/60). With V absent by its counter, D (present on 0.989 of steps) is in the filter's top set with B, or alone,
  and its whiffs steer whenever nothing or D is held: D-driven nav is 0.956 of W1D nav events and 1348 events in T1D,
  none while V is present (D never in the top set then; the 278 V-always-present T1 rows identical with and without D).
  Each nav resets `since`, so the cast target stays within 40 degrees of upwind on 0.630 of steps (0.243 without D) and
  the agent runs to the upwind wall (W1D 303/400 at the wall at step 599). In W1 the initial cast takes every row upwind
  of B at steps 42-52 with and without D; 383 rows come back downwind without D, 83 with it. The 122 (m) rows are 103
  prior expiry (no V whiff by step 58) and 19 silences of 300 steps; H26's narrower at-risk definition gives 21 here; the
  53 out-of-V rows are all prior expiry, 52 with a D-driven nav first. M6 is unreadable because the hold-not-read and
  release-off arms lose all 400 rows on the same path (326/400 and 331/400 rows identical in position to Agent15).
  Report doc ddec6582aa2fcaa83 (experiments/h27/h27_post_bench_diagnosis.md); output experiments/h27/ph32b_diag.txt
  (sha ec3abdec...d0ae). H27's verdict unchanged; nothing adopted. Awaiting the owner.
- **H27 CLOSED at the bench stop (2026-09-26; decision:h27-closed; owner '위 권고안으로 진행', gloss 'proceed with the
  recommended option above', read by the interpreting assistant as option 1, the recommended position).** STOPPED at the
  bench by all three stop rules, NOT shown under its registered criteria; not re-judged; M4 PASS; tasks not run; dev
  9937/9947 and eval 2083/2173 unused and kept registered to H27. The distractor condition is recorded as a LIMIT of the
  adopted agent (record:distractor-capture-limit): a ubiquitous unreinforced odour at p_D 0.03 costs the choice task 0.13
  of P(V) (0.787 vs 0.920) and defeats tracking of a neutral plume entirely (W1D 400/400 lost vs 22); while V is present
  nothing changes; the hold's benefit under a distractor stays unmeasured. Structural reading (interpretation): the
  filter's top rule ranks by value alone, so a never-reinforced odour that whiffs everywhere ties the neutral odour and
  steers whenever V is absent. Nothing adopted; the H27-scoped relaxation and composition rule lapse (the composition
  rule stays available for a future N = 3 design by a new decision). Queued as PROPOSED by the interpreting assistant,
  not decided (its own addition, stated as such): a recognition-core mechanism for a ubiquitous odour (working name
  'habituation to a ubiquitous odour'), needing new per-odour state and a signed relaxation.
- **H28 OPENED FOR DESIGN (2026-09-26; decision:h28-open-design).** The queued proposal ranked first against the
  registered queue and numbered H28 (concept:h28-ubiquitous-odour-discount). Design v1 DRAFT doc dc81dbd5005ca164c
  (experiments/h28/h28_design_v1.md, sha 135a28f2...6a51), no code. By arithmetic from the record, habituation in its
  usual sense is rejected (the plume's in-cone whiff rate 0.037-0.30 exceeds D's 0.030; over a whole run D is the denser
  odour, 0.030 vs 0.0165-0.0171, but a long trace rises too late for a capture that begins at step 59), and the W1D rows
  in which B is never sensed before the capture (97/400) are out of reach of any value-free, position-free statistic.
  Recommended: a burst-ranked value tie (Agent16 = Agent15 + a new act in src/ph33.py): when present non-negative odours
  tie at the top value, only the most recently burst one (three whiffs within 10 steps) steers or keeps, none if none has
  burst; inert without D by code. T1D M2(b) >= -0.05 (predicted 4-8 rows out of V); W1D registered as the recovery over
  H27's agent, lost-row DP <= -0.20 (predicted 110-245 lost); H27's W1D bars reported; M6 reported; stop rules (h), (hW);
  three records to sign; joint about 0.97 at the predictions. Seeds dev 9907/9917, eval 2093/2197, bench
  20261131/20261132, bootstrap 20261133 (232 files scanned, one file and one graph collision replaced). Awaiting the
  owner's confirmation of section 12.
- **H28 OPENED on design v2 FINAL (2026-09-26; decision:h28-open; owner '권고안으로 진행하고 다음작업 설계 진행', gloss
  'proceed with the recommended options, then proceed with the next work's design').** Every recommended option of
  section 12 confirmed (ten points). Signed before code, H14 format, H28 only:
  decision:classification-rule-relaxed-burst-record-h28 (per odour the step of its second most recent whiff and of its
  last burst, read only to rank odours tied at the top value), decision:evidence-release-composition-rule-h28 and
  decision:classification-rule-relaxed-presence-prior-h28 (the two H27 records re-signed in form). vinc_decide on the
  H28 concept: only decisions_on_same_subject on the H20 concept (reported, not resolved). Design v2 FINAL doc
  da2c1c079a1766d3e (experiments/h28/h28_design_v2.md, sha b12137f6...6b8c); no bar, seed, arm, prediction or rule
  changed from v1.
- **H28 code, demo, bench, development run and one evaluation: SHOWN under its registered criteria (2026-09-26;
  record:h28-bench-result, record:h28-dev-run, record:h28-result; report doc d29986a75ef4e9711).** src/ph33.py (sha
  f2a29722...20b0, source doc dd7262b0c91dbc66b) composes Agent16 = Agent15 + Act16 from ph32.py imported unchanged; no
  adopted file edited. Demo 8/8 ok (one cosmetic label fix before the recorded demo, noted in its header). Bench
  (ph33_bench.txt sha 45b0f263...8671): M4 PASS; (m) 125, (w) 116; (h) T1D DP -0.0150 [-0.0300, -0.0025], M2(b) pass
  probability 0.9987; (hW) W1D lost 228 vs 400, M5(a') pass probability 1.0000; both continue. Development run
  9907/9917 (ph33_dev.txt sha e49edf3d...3c5f): no operation error, no amendment. One evaluation 2093/2197
  (ph33_eval.txt sha 43e3a999...3dbe): M1 PASS; M2(b) DP Agent16 D on - D off -0.0275 [-0.0450, -0.0125] PASS; M2(c)
  +0.448 [+0.397, +0.498] PASS; M3 identities PASS; M4 PASS; M5(a') W1D lost-row DP Agent16 - Agent15 (D on) -0.445
  [-0.495, -0.397] PASS (222 vs 400 lost). Reported: M2(a) 0.915; M2(d) +0.1225; H27's W1D bars against D off all fail
  (222 vs 29 lost, dwell 13.957 vs 23.657, 43.4 contacts per row); M6 +0.0000 (the hold's benefit stays unmeasured);
  T3aD 0.220 vs 13.193; T4 at +1/-1/0 0.740 vs 0.932. Predictions missed: k 11 (4-8 predicted), (w) 116 (about 100),
  the W1D loss composition (89 of 110 (w) rows lost, 133 lost outside them). Closure is the owner's.
- **H29 OPENED FOR DESIGN (2026-09-26; decision:h29-open-design; the second half of the owner's '권고안으로 진행하고
  다음작업 설계 진행', gloss 'then proceed with the next work's design').** The next queued item, the H26 T3b limit (a loss
  after tracking), numbered H29 (concept:h29-loss-after-tracking). Design v1 DRAFT doc dd00688c21f09b13e
  (experiments/h29/h29_design_v1.md, sha 5078d814...1260), no code, written on Agent14N2 (two channels, no D; it holds
  whether or not H28's rule is adopted). Central finding: the Lost world equals its T1 twin in every draw until the twin's
  next valued whiff, so no rule on the agent's own state can shorten the post-whiff window after a loss without
  shortening it in tracking; the only lever is the window's length. Candidates rejected on record: a burst-conditioned
  reload, a window shrinking with neutral whiffs, the hold-end window (H26's rejection stands), cast-phase keys at 2 SAT
  (about 284, a 16-step sliver) and SAT (about 142, T1 like N 150). The design's candidate if a run is chosen: Agent17 =
  Agent14N2 with the window 200 and the 59-step prior unchanged (identical in W1, T3a, +1/-1 by code; T1 at N 200 on the
  sweep DP -0.0125; predicted T3b gain about +0.9, range +0.5 to +1.3); M2(b) >= -0.05, M8(b) paired T3b dwell lower
  bound > 0; stop rules (h), (hB); joint about 0.93 at the predictions. Recommended at section 12 point 1: a
  measurement-only T3b diagnosis on H26's spent bench seeds before any run, then the run or closing T3b as a limit.
  Seeds, if run: dev 9903/9913, eval 2111/2221, bench 20261141/20261142, bootstrap 20261143 (240 files scanned, no
  collision). H28's closure and adoption remain awaiting the owner. Awaiting the owner's confirmation of section 12.
- **T3b DIAGNOSIS (2026-09-26; decision:t3b-diagnosis; measurement only; the owner's '그래 그럼 권고안으로 진행', gloss
  'yes, then proceed with the recommended option', accepting H29 design section 12 point 1).** Six falsification criteria
  F1-F6 registered in the decision before any code. src/ph34b.py (sha 1de70167...bf25; source doc d51314011b2b7f5e2) on
  H26's spent bench seeds (evaluation seeds for the reproduction only): H26's T3b and T1 lines reproduced, all MATCH
  (4.412, none 173/379). Readings: F1 twin identity 400/400 MET; F2 0.990 of rows upwind at L + 300 (the window opens
  between cast passes) NOT MET; F3 recovery within 200 steps of L + 300 0.478 NOT MET; F4 twins' next valued whiff
  within 200 0.917, median 153, INCONCLUSIVE; F5 Agent17 (window 200) T1 DP +0.0000 MET, T3b gain +2.460 [+1.883,
  +3.055]; F6 no own-state separation at 0.80/0.20 (neutral counter 0.652 vs 0.169) INCONCLUSIVE. (t) profile: window
  200 catches the first downwind pass (dwell 6.460), 250 misses it (4.115). Output experiments/h29/ph34b_diag.txt (sha
  6a4219b3...cc07); report experiments/h29/t3b_diagnosis.md (doc d8a7e386faf08075d); record:t3b-diagnosis-result. The
  readings point to branches (i) and (ii), not (iii). Nothing adopted; H29 not opened; H28 untouched. Awaiting the owner.
- **H29 OPENED (2026-09-26; decision:h29-open; the owner's '(i) 권고안대로 진행', gloss 'branch (i), proceed as
  recommended').** Branch (i) of the T3b diagnosis: every recommended option of design v1 section 12 except point 1, which
  the diagnosis resolved, plus one addition the interpreting assistant recommended and the owner accepted with the same
  words: the F2 finding recorded as a stated sensitivity and a REPORTED phase-sensitivity condition (T3b at t0 100 and
  t0 200, no bar). Signed before code: decision:classification-rule-relaxed-presence-prior-h29 (the H26 presence
  relaxation re-signed with window 200, start 140, H29 only). Design v2 FINAL doc d724287aa203d256d
  (experiments/h29/h29_design_v2.md, sha 552e2ee1...6aa7); no registered bar, seed, arm, prediction or rule changed.
- **H29 code, demo, bench, development run and one evaluation: SHOWN under its registered criteria (2026-09-26;
  record:h29-bench-result, record:h29-dev-run, record:h29-result; report doc d92ffd006bdbcdc28).** src/ph35.py (sha
  e4a3ceda...b1b1, source doc d7ed06b1bd4bb0e2c): Agent17 = Agent14N2 built with N_hi 200 through the existing
  constructor argument (a body-less subclass); ph28.py, ph30.py, ph34b.py imported unchanged and checked at run time; no
  adopted file edited. Demo 12/12 ok, nothing fixed. Bench (ph35_bench.txt sha e217dd00...d0a0): M4 PASS; (m) 20, (x) 16;
  (h) T1 DP +0.0025 [+0.0000, +0.0075], M2(b) pass probability 1.0000; (hB) T3b gain +2.1350 [+1.6649, +2.6201], M8(b)
  pass probability 1.0000; both continue. Development run 9903/9913 (ph35_dev.txt sha a70342bf...bf0c): no operation
  error, no amendment. One evaluation 2111/2221 (ph35_eval.txt sha 1577b42c...6e2e): M1 PASS; M2(b) DP Agent17 -
  Agent14N2 -0.0075 [-0.0200, +0.0025] PASS; M2(c) +0.348 PASS; M3 identities PASS (the 19 departing T1 rows are
  exactly the exposure set); M4 PASS; M6 PASS; M8(a) window exact at L + 200 376/376 PASS; M8(b) paired T3b dwell
  +1.9525 [+1.4549, +2.4501] PASS (6.730 vs 4.777). Reported: R_b 1.96; T3b at t0 100 +0.7000 [+0.2625, +1.1425], at t0
  200 +3.8175 [+3.3400, +4.3050] (the first-surge delays after L unchanged; t0 moves L relative to the measurement
  window). Predictions missed: the T3b gain (1.95 vs 0.5-1.3) and the Agent11 bound, Agent17's dwell level, the bench's
  T1 k and DP (favourable side). A trade, not a separation. Closure is the owner's; H28's closure untouched.
- **H28 CLOSED as SHOWN and the burst-ranked value tie ADOPTED for the three-channel distractor form (2026-09-26;
  decision:h28-closed, decision:h28-burst-tie-adopted-within-tested-conditions; the owner's '권고안으로 바로 진행', gloss
  'proceed right away with the recommended options').** Not re-judged. Adopted within the tested conditions only: Act16
  (src/ph33.py:116-177) in Agent16 as composed, supplied +1/0, D at value 0 and p_D 0.03, G 2, C0, gate on, N2, learning
  off, T1D and W1D; the H27 composition rule, the three-counter presence relaxation and the H28 burst-record relaxation
  become adopted state for the three-channel form only (in form). At two channels the rule is inert by code, so the
  two-channel adopted agent is unchanged. Limits: W1D 222/400 rows still lost (29 without D); T3aD 0.220 vs 13.193; M6
  (the hold's benefit under a distractor) unmeasured; other p_D, a non-zero-valued D, learning, the H15 world untested.
  The distractor limit under the adopted rule: record:distractor-capture-limit-under-h28-tie (T1D DP -0.0275, W1D
  222/400); record:distractor-capture-limit unchanged. Rejected on record: no adoption; adoption as the universal rule.
- **H29 CLOSED as SHOWN and the window 200 ADOPTED; the adopted two-channel agent is now Agent17 (2026-09-26;
  decision:h29-closed, decision:h29-window-200-adopted-within-tested-conditions; the same answer).** Not re-judged.
  Agent17 = Agent14N2 built with N_hi 200, counter start 140, the 59-step prior unchanged (src/ph35.py:104-105 through
  src/ph28.py:95-97); it supersedes the H26 window (300, start 240), whose relaxation stays on record as superseded; the
  H29 relaxation (decision:classification-rule-relaxed-presence-prior-h29) is the adopted state. Scope: +1/0, G 2, C0,
  gate on, N2, learning off, World7 T1, W1, T3a, T3b at t0 150. Limits: the T3b gain's cast-phase dependence (F2 NOT MET;
  t0 100 +0.70 [+0.26, +1.14], t0 150 +1.95 [+1.45, +2.45], t0 200 +3.82 [+3.34, +4.31]; other geometries and cast
  parameters untested); a loss whose second pass falls after the row's end is not recovered (F3); the three-channel form
  keeps its tested window 300. Rejected on record: keep 300; adopt 200 universally including the three-channel form.
- **H12 OPENED FOR DESIGN (2026-09-26; decision:h12-open-design; the same answer, 'then the next queued item').** The
  item queued at the Phase 7.2 close (concept:h12-differential-persistence, reused). Design v1 DRAFT doc
  dff68b78ea66ed47e (experiments/h12/h12_design_v1.md, sha 75428f1a...e79e), no code. From the code: the adopted module
  already writes extinction on the opposite valence's acquisition compartment, so no per-compartment decay gives
  sign-symmetric recovery with retained acquisition, while the parallel pair with one decay constant can; in every
  recorded behaving run extinction never fires (every coded step is reinforced), so the change is inert there and a
  behavioural test needs a world change and a positive competitor; decay alone gives recovery, not reacquisition by
  re-pairing. Recommended (c): a Stage 1 module bench (H11 reproduced bitwise; tau_ext the smallest of 2000, 5000,
  10000, 20000 keeping the Phase 4 battery, predicted 5000; SR >= 0.20 and RET >= 0.99 at D 5000 for both signs; stop
  rules) gating a Stage 2 behavioural test outlined with bars unmeasured. Seeds: Stage 1 codes 20261151/20261152,
  bootstrap 20261153; Stage 2 bench 20261151/20261152, dev 9911/9921, eval 2129/2243 (251 files scanned; one
  candidate replaced). Awaiting the owner's confirmation of section 12. Recorded by a session that resumed after a
  rate-limit cut-off (the cut-off session had written nothing).
- **H12 OPENED on design v2 FINAL (2026-09-26; decision:h12-open; the owner's '권고안으로 확정하고 H12 진행', gloss
  'confirm as recommended and proceed with H12': every recommended option of v1 section 12).** Design v2 FINAL doc
  d27ec95924fe49be1 (experiments/h12/h12_design_v2.md, sha 3d3aab80...95f1, content_hash equal): v1 with section 12
  replaced by the confirmation and Stage 2's registration completed from the confirmed outline before any run (section
  5.5: the world exactly, the learning input, the mirror, the arms' construction, the measures, K0, bar_B, (hS), K1, K2,
  the seeds' use). The one construction the outline left open: V is pre-acquired off-world by Stage B's training
  (ph29.train), because with the competitor at +0.5 from step 0 a naive learning arm is the outline's own sham.
- **H12 Stage 1 (module bench): PASS (2026-09-26; record:h12-bench-result).** src/ph36.py (MB5 = ph8.MB4 plus one
  relaxation line per decaying compartment; sha b83bd9e9...ca71, doc d75b858c9487ed11e); ph36_demo.txt (nine checks ok),
  ph36_bench.txt (sha 7071e2d8...b865). H11 reproduced line for line (45/45); (I1), (I2) exact; (I2') within 1.7e-16;
  (I4) on H15 Run 2's recorded streams bitwise. F1 at K 500: P at tau 2000 fails the extinction clause (37.1 percent),
  5000 passes (28.4 percent; predicted 28.7) -> tau_ext* = 5000; F2 100.0 percent. The module is deterministic (every run
  equal): SR at K 200, D 5000 = 0.6322 for both signs (= 1 - (1 - 1/5000)^5000), RET 1.2279 for both signs; B1-B4 PASS.
  B5: S1 SR -0.0984 (forgetting, no recovery); S2 recovers the aversive sign and inverts the appetitive one (v -0.4358).
  F6 at D 5000 4.15x, all recovery (REACQ -0.0338). Stage 1 adopts nothing.
- **H12 Stage 2: composition signed, then STOPPED at the bench, K0 UNREADABLE (2026-09-26;
  decision:h12-stage2-composition; record:h12-stage2-bench-result).** src/ph36b.py (sha cfb9a26a...1cef, doc
  dd4b2e56d1a576518): Agent17 with learning on in W7X, the H12 module (tau 5000) against the adopted one; every identity
  holds ((I5) 400/400, K2(c), the supplied trajectories, the draws). On the bench seeds the P4 ceiling (V +1) reaches
  P(V) 0.1050 against the floor's 0.0125, span +0.0925 < 0.30, and P4 ties are 0.255-0.318 (> 0.20): after P3 the agent
  stays at N and seldom meets V's plume even at V = +1, so the read-out cannot express the recovery the module shows
  (V 0.563 in the H12 arm against 0.317 in the gate-only arm at step 4199). By the registered rule Stage 2 is unreadable
  as designed (redesigned, not retuned); no bar was fixed (decision:h12-k1-bar not written), (hS) not computed, no
  development or evaluation seed run, nothing adopted. Also recorded: the single-site and parallel layouts are not
  equivalent in Stage 2's input regime (reward and code together, then code alone: the reward trace's potentiation can
  drive V below 0, where the single-site feedback masks it and the parallel one does not), a missed prediction of design
  2.2 (exact only for H11's forward-pairing protocols). Awaiting the owner: close H12 (shown at the module level only)
  or redesign Stage 2.

## Why a plan now

Four hypotheses were run in one day by picking the next most interesting candidate after each result. That produced a usable architecture (N units with thresholded saturating self-excitation plus one global inhibitory unit) but left three structural gaps: no hypothesis is tied to a real fly circuit, there is no behavioural benchmark, and success criteria were written after seeing results. From here the order is fixed in advance and changed only by a recorded decision.

## Where the project stood at the start, against Level 0 to 6

- Level 0 to 1 (connectome, circuits): empty. The biology and circuit layers held type definitions only.
- Level 2 to 3 (motifs, abstract architecture): H1, H2, H4, H5 done on abstract motifs.
- Level 4 (simulation): four experiment scripts, not yet one harness.
- Level 5 (agent): one task (cued delayed choice), no body, no environment.
- Level 6 (behaviour comparison): nothing.

## Phases, in order

### Phase 0. Consolidate (no new hypothesis)
- 0.1 One regression harness that reruns Exp1 to Exp4 and checks the recorded numbers.
- 0.2 Architecture spec v0.1 for the Select-and-Hold circuit with global unit.
- 0.3 Working protocol recorded in the graph.
- Gate: every recorded result reproduces from one command.

### Phase 1. Biological grounding (Level 0 to 1)
- 1.1 Literature check, with sources, of the circuits the abstract results resemble: antennal lobe local neurons (input normalisation), mushroom body Kenyon cells with the APL neuron, ellipsoid body heading circuit, dopamine-gated plasticity at mushroom body output synapses.
- 1.2 Fill the biology and circuit layers and link each accepted hypothesis to a verified circuit, or mark it as having no anchor.
- 1.3 Record mismatches as open questions.
- Gate: H1, H2, H4, H5 each carry at least one sourced circuit link or an explicit "no anchor".

### Phase 2. Close the open problems of Select-and-Hold
- 2.1 H6: normalisation belongs in a separate upstream stage (or is gated by input presence).
- 2.2 H7: what calibrates commitment to option count.
- Gate: wrong choices 5 of 200 or fewer across input scale 0.25 to 4.0 and N 2 to 20, with distractor resistance of amplitude 2 or more. If a sub-step fails twice, record it as a limit and move on.

### Phase 3. Graded memory
- 3.1 Adopt H3 (ring attractor): bump holds a continuous value without input, updates by velocity input, corrects to a landmark cue.
- Gate: drift and update accuracy meet criteria stored beforehand.

### Phase 4. Learning
- 4.1 H8: a reinforcement signal gating plasticity between a sparse code and an output unit gives association, extinction and reversal.
- Gate: learning curve criteria stored beforehand.

### Phase 5. Integrated agent (Level 5)
- 5.1 Agent v1: normalisation stage, selection and hold, heading memory, learned valence, action. A simple 2D world.
- 5.2 Ablation of each module.
- Gate: task performance above ablated versions, stored beforehand.

### Phase 6. Behaviour comparison and the abstraction question (Level 6)
- 6.1 Compare with published fly behaviour qualitatively.
- 6.2 Abstraction ladder: for each accepted motif, remove one feature at a time and record which computational property survives.
- Output: a synthesis document stating, per motif, the minimum structure that must be preserved.

### Phase 7. Acting on the Phase 6 synthesis (opened by decision:phase6-gate-pass-phase7-open)
- 7.1 H9: replace the bistable Select-and-Hold unit with a graded substrate; does the reset become unnecessary?
- 7.2 H11: rebuild extinction as a parallel opposing trace; does the sustained-exposure erasure disappear?
- 7.3 H13: give the world a wind reference and score navigation on encounter timing.

### H14, promoted (decision:phase7-3-gate-h14-promoted)
- Repair the ring's velocity integration so it holds at behavioural angular velocities. Closed by decision:h14-adopt-tau1.

### H15 (decision:h15-open; Run 2 by decision:h15-run2-open, closed by decision:h15-run2-closed)
- Rerun the integrated agent on the wind world with every adopted change in place. Run 1 not supported.
- Run 2's core question, set by the owner: does a LEARNED NEGATIVE valence lead to actual avoidance, with long-horizon search maintained while it does? Positive-valence learning is claimed at the weight level only; the selection circuit's distractor resistance and heading memory under cue loss are marked unverified.
- Run 2 was run on the final specification v4 (doc dc860b9c7c6f3aa6e): two evaluations never mixed, E1 natural search and E2 controlled experience; 400 rows, start groups assigned 200/200; one fixed statistic per criterion; 97.5 percent intervals at the first evaluation and at the one permitted extension; PASS / FAIL / INCONCLUSIVE / UNREADABLE; E1 and E2 reported as separate results.
- Run 2 closed: E1 NOT DECIDED BY THIS RUN, E2 PASS, with what was observed recorded separately (progress log).
- Interpretation limit: Run 2 ran with the wind sensed on every step, and success under that condition is not evidence that heading memory is needed or valid. Results are conditional on the fixed set of per-row odour codes.

### H16 (decision:h16-open, decision:h16-run2-open, closed by decision:h16-close-limited-adoption)
- Navigation alone, single source, long persistent horizon. Criteria record:h16-success-criteria (K1-K6). Run 1 and Run 2 both not supported; the return rule adopted for a limited scope by a separate decision.

### H19 (decision:h19-open-option-a, adopted by decision:h19a-adopt-and-run2-direction)
- Option (a) only: while nothing is held, a sensed whiff resets the cast clock, within the owner's three boundaries. Criteria record:h19-success-criteria (N1-N6). Supported on N1-N5, N6 unreadable; adopted within the tested conditions.

### H20 (decision:h20-priority-design-first; Stage A opened by decision:h20-stage-a-open, CLOSED by decision:h20-stage-a-closed; link check by decision:h20-linkcheck-open, complete; Run 2 opened by decision:h20-run2-open, evaluated, CLOSED by decision:h20-run2-closed; Stage B opened for design by decision:h20-stage-b-open-design, opened by decision:h20-stage-b-open, evaluated once, CLOSED as SHOWN by decision:h20-stage-b-closed; Stage C opened for design by decision:h20-stage-c-open-design, opened by decision:h20-stage-c-open with the Stage C-only release rule decision:release-value-gated-stage-c, STOPPED at the bench by its (hR) stop rule; post-bench diagnosis by decision:h20-stage-c-post-bench-diagnosis; Stage C Run 2 opened for design by decision:h20-stage-c-run2-open-design, opened by decision:h20-stage-c-run2-open with the M4(c) readability re-signed for Run 2 (decision:h20-stage-c-m4c-readability-resigned-run2) and (N2) re-signed in form (decision:release-value-gated-stage-c-run2), evaluated once, SHOWN under its registered criteria, CLOSED as SHOWN by decision:h20-stage-c-run2-closed with N2 adopted by decision:n2-release-adopted-within-tested-conditions; H20 as a whole CLOSED by decision:h20-closed)
- Does a positive value change which odour the agent pursues? Three separated checks: A, a
  supplied value (pre-registered, design v3 FINAL doc dd947882bd962eebe); B, a learned value
  (outline only); C, integration in the H15 Run 2 world (outline only). Nothing about B or C is
  claimed from A. Criteria A1-A5 in the design; A1-A4 gate Stage A, A5 (T-revise) is reported.
- Boundaries fixed by the owner: the pathway is one named change (a gain on the selection
  input), negative avoidance overrides it and is verified in a constructed state, the main
  measure is the first source reached over every assigned row with no-choice pre-defined, the
  crossing over identity and side separates preferences without removing them, an empty
  condition is not a pass, and a low revision rate is reported as an interval reading, never as
  'cannot'.
- Course of Stage A: bench with no eligible candidate (rule and verdict kept) -> diagnosis ->
  G 2 fixed post hoc by a separate execution decision -> dev run exposed the agent's fixed
  initial cast side (A1(b) FAIL on dev) -> amendment: initial cast side drawn per row -> one
  evaluation: NOT shown (A2 FAIL; A4 INCONCLUSIVE); the value moves selection, the first source
  reached does not follow it. CLOSED. Report db2f39472a3eed143.
- Link check (owner's next step, value and learning excluded): complete. The tracked identity
  controls where the agent ends up (dwell 0.95 to 0.97 in every geometry) and the first source
  reached only when the separated stretch is long enough (C2 0.743, partial; C0 and C1 0.060 and
  0.087, not expressed). In the H20 geometry the first reach is decided before the identity has
  moved the agent crosswind. Report df9cf42bb99c43d39. Stages B and C not entered.
- Run 2 (owner chose option (a); new pre-registration, not a re-judgement of Stage A; design v1
  FINAL doc d3866101cd92f911d): dwell-majority measure calibrated by a known-answer arm; C0 kept;
  G 2 pre-registered. One evaluation (seeds 1695/1795): NOT shown under the registered criteria
  (R1 PASS, R2 FAIL P(V) 0.535 DP 0.028, R3 PASS, R4 PASS). The measure's ceiling is 0.94; the
  pathway reaches 0.57 of it. Selection still follows the value (first hold 274 vs 210). Report
  dd71f30d466badf4b, source ph18.py sha 26ad4def...97c3. Diagnosed on the evaluation trajectories
  (record:h20-run2-diagnosis) and CLOSED as not shown by the owner (decision:h20-run2-closed); the
  diagnosis led to H21. Stages B and C not entered.
- Stage B (the learning check) OPENED FOR DESIGN on 2026-09-25 (decision:h20-stage-b-open-design), after H21, H23, H25
  and H26 made the supplied value control the dwell majority (H26: Agent14 0.927). Design v1 DRAFT doc
  da31fd8fe14fd6444 (experiments/h20/h20_stage_b_design_v1.md), no code: Agent14 unchanged; the value learned off-world
  by the H15 E2 protocol (neutral first, valued 30 reinforced steps; sham without reinforcement), read out into
  `known`, frozen in the test; learned vs supplied vs sham on the same rows in the H21 task; a learned-value check with a
  sign clause; W1 and T3a reported; +1/-1 excluded. Stage C (integration, learning on in the H15 Run 2 world) not
  entered.
- Stage B OPENED on design v2 FINAL (decision:h20-stage-b-open, owner 2026-09-25, '권고안 적용'; doc d3f2ce9707790cd87,
  experiments/h20/h20_stage_b_design_v2.md). src/ph29.py (source doc dbcf264395e76d71a); bench M4 PASS, (h) and (hL)
  continue (record:h20-stage-b-bench-result); development run clean (record:h20-stage-b-dev-run). **Evaluated once
  (2005/2107; record:h20-stage-b-result; report doc d66ad8dea08c92116): SHOWN under the registered criteria.** The
  learned value (valued exactly +1.0; neutral a small positive residual; sham exactly 0) is carried into the choice as
  the supplied value is: learned - supplied 0.000 [0.000, 0.000], learned - sham +0.467 [+0.415, +0.522], every cell
  >= 0.826 at the lower bound, learned Agent14 - learned Agent10g +0.367. Close to an identity test at the saturating
  dose; the neutral residual (gain up to x 1.6, a single neutral whiff then holds) moved 117 trajectories and no
  outcome. Missed predictions (sham 0.455, pathway-off 0.448, learned Agent10g 0.555, supplied 0.922, known-answer
  0.958) enter no bar. Not shown: learning during behaviour (Stage C), negative learned values, a sub-saturating dose,
  other codes. Nothing adopted; closure is the owner's. Stage C not entered.
- **Stage B CLOSED as SHOWN (2026-09-25, decision:h20-stage-b-closed).** Not re-judged. The result fixed on record, in
  the owner's words: **a learned positive value is used in behaviour within the tested conditions** (the H15 E2
  training off-world, neutral first, a saturating dose, the value read out into `known` and frozen; World7 T1 at
  +1/0-equivalent values; Agent14; G 2; C0; gate on; release on; the H26 counter). Nothing new adopted: the learning
  module and the read-out path were already adopted. Not shown: sub-saturating doses, learning on during the task,
  negative values, W1 and T3a beyond the reported identities.
- Stage C (the integration check) OPENED FOR DESIGN on 2026-09-25 (decision:h20-stage-c-open-design). Design v1 DRAFT
  doc dc7e62aeab81c347b (experiments/h20/h20_stage_c_design_v1.md), no code: Agent14 with learning ON in the H15 Run 2
  world (E1 natural search 5400 steps; E2 with learning on in the test), the module's read-out written into `known`
  before every act (the adopted flee reads `known`, ph23.py:77); H15 Run 2's agent reproduced first and used as the
  paired reference; the gain measured as fewer R-start rows visiting the not-yet-learned punisher; Run 2's search,
  avoidance, reach and E2 criteria kept with Run 2's allowed gaps; the release at negative holds put to the owner
  ((N2) recommended, a scoped rule to be signed before code). Awaiting the owner's confirmation of section 12.
- Stage C OPENED on design v2 FINAL (decision:h20-stage-c-open, owner 2026-09-25, '권고안대로 확정하고 Stage C 진행'; doc
  d27e6dfe2e2c16183, experiments/h20/h20_stage_c_design_v2.md), after the (N2) release rule was signed for Stage C only
  (decision:release-value-gated-stage-c). src/ph30.py (source doc d3a2e1142563d7b38). **Bench (record:h20-stage-c-bench-result):
  STOPPED by the (hR) stop rule** (Agent14 no-learning's GM last-third punishing dwell in G3 16.000 [0.000, 19.667], not
  PASS 'at least 10': M4(c)'s baseline would not be readable). Everything else on the bench held: H15 Run 2 reproduced line
  for line; every identity True (the mirror, pathway-off == H15 Run 2's agent, positive-off inert in Agent3, (N2) == as
  composed before any negative hold, row independence); (v) exact; (h) M2(a) at DP -0.270 (R-start punisher visits 10
  vs 64 of 200) and (hS) at 1.0000. The tasks were not run; nothing is shown or not shown about Stage C's hypothesis;
  nothing adopted. Reported beside: the release as composed at negative holds (N1) left 122/200 P-start rows unrecovered
  (against 19 under (N2)). The owner decides (Stage C, and H20 as a whole).
- Stage C post-bench diagnosis (decision:h20-stage-c-post-bench-diagnosis, owner 2026-09-25, '2번 진단 먼저 진행';
  record:h20-stage-c-post-bench-diagnosis-result; report doc ded5da7a47fb9e759; src/ph30b.py, measurement only, bench
  seeds). The (hR) interval reaches 0 because the no-learning floor is two-moded, not spread: in 88 of 199 G3 rows it ends
  the run at the reward source (0 punishing dwell), in 111 at the punisher (median 24), and the group median of a
  resample falls to 0 whenever 100 or more zero rows are drawn (5.26 percent of resamples). The 0-dwell rows sensed R
  whiffs with nothing held after the H25 release had ended their P holds, and never returned to P; H15 Run 2's agent
  without learning shows 55 such rows on the same seeds and reads 21.000 [19.667, 22.667]. On G3+ the M4(c) WIN is
  111/0/0 and the floor GM 24.000 [22.667, 24.667]. Verdict unchanged; the owner decides: close Stage C and return H20,
  or a Run 2 design that registers a re-signed M4(c) readability rule or floor (report section 5).
- Stage C Run 2 OPENED FOR DESIGN (decision:h20-stage-c-run2-open-design, owner 2026-09-25, '다음도 권고안에 따라 작업
  진행'). Design v1 DRAFT doc dfad8d4ed6b1d7675 (experiments/h20/h20_stage_c_run2_design_v1.md), no code. Run 2 changes
  one rule and inherits everything else from Run 1 (the hypothesis, the mirror, (N2), the arms, E1-C/E2-C, every other
  bar, (h), (hS)): M4(c)'s readability is read on G3+, the rows its WIN is already read on (G3+ at least 50, the floor's
  group median lower bound >= 10), re-signed in H14 format for Run 2 only, with H15 Run 2's agent without learning, the
  floor over all G3, the all-G3 WIN with its ties and the dropped rows' end state reported beside; the tie rule is not
  touched; (hR) becomes a pass probability on the bench rows with a G3+ count guard; (N2) is re-signed in form. Named
  lesson: Run 1's readability estimate (about 0.9) came from Agent3's value while the floor was Agent14. New seeds.
  Section 12 confirmed by the owner's standing instruction (below).
- Stage C Run 2 OPENED on design v2 FINAL (decision:h20-stage-c-run2-open; doc d007990ab333e7194) after the M4(c)
  readability re-sign (decision:h20-stage-c-m4c-readability-resigned-run2) and the (N2) re-sign in form
  (decision:release-value-gated-stage-c-run2). src/ph31.py (source doc d4c5f81249ef02a9e), ph30 and ph30b imported
  unchanged. Bench M9 PASS (record:h20-stage-c-run2-bench-result): (r) and (r') reproduced exactly; (h), (hS), (hR)
  continue (G3+ 107 of 200, (hR2) 1.0000). Development run clean (record:h20-stage-c-run2-dev-run). **Evaluated once,
  SHOWN under the registered criteria (record:h20-stage-c-run2-result; report doc de5963e5a73875a97): M1 to M9 all
  PASS.** The gain: R-start rows visiting the not-yet-learned punisher 8 (learned Agent14) vs 56 (H15 Run 2's agent) vs
  91 (positive-off) of 200; search, avoidance (read on G3+, 112 rows), reach and the E2 result kept. What M4(c) gives up
  is reported: on all G3 the WIN is unreadable by the tie rule (112/85/2), and the 87 rows outside G3+ (all at the
  reward source) hold 2 losses the G3+ WIN does not see. Nothing adopted. Closing Stage C, and H20 as a whole (Stages
  A, Run 2, B, C), is the owner's decision.
- **Stage C Run 2 CLOSED as SHOWN; N2 ADOPTED; H20 CLOSED as a whole (2026-09-25; decision:h20-stage-c-run2-closed,
  decision:n2-release-adopted-within-tested-conditions, decision:h20-closed; owner '1. shown으로 종결 및 n2는 범위
  권고안으로 적용 2. 미입증안 해결책이 없나? 3,4 권고안으로 진행').** Not re-judged. The stages:

  | stage | design (doc) | verdict | key numbers | closure |
  |---|---|---|---|---|
  | A (supplied value, first source reached) | dd947882bd962eebe | NOT shown (A2 FAIL, A4 INCONCLUSIVE) | P(V) 0.532, DP vs pathway-off 0.000 | decision:h20-stage-a-closed |
  | link check (value excluded) | d824732220256254b | a check | C0 first reach follows a fixed identity in 0.060; dwell 0.95-0.97 | record:h20-linkcheck-result |
  | A Run 2 (supplied value, dwell majority) | d3866101cd92f911d | NOT shown (R2 FAIL) | P(V) 0.535, DP 0.028; ceiling 0.943 | decision:h20-run2-closed |
  | B (learned value, frozen) | d3f2ce9707790cd87 | SHOWN | learned = supplied, P(V) 0.922; vs learned Agent10g +0.367 | decision:h20-stage-b-closed |
  | C Run 1 (learning on, H15 Run 2 world) | d27e6dfe2e2c16183 | STOPPED at the bench ((hR)) | floor GM over G3 16.000 [0.000, 19.667]; tasks not run | closed with H20 |
  | C Run 2 | d007990ab333e7194 | SHOWN (M1-M9 PASS) | R-start punisher visits 8 vs 56 vs 91 of 200; late unrecovered 18/400 | decision:h20-stage-c-run2-closed |

  The not-shown stages are resolved without re-judging them (the interpreting assistant's recommendation, applied under
  the owner's point 2 and the '3,4 권고안으로 진행' pattern): the Stage A question was answered under the registered
  criteria of H23, H26 and Stage B; the first-reach measure was found inexpressible in C0 by the link check; the
  dwell-majority re-run with the adopted pathway is H26's evaluation; no Stage A re-run. **H20's conclusion: a positive
  value, supplied or learned, controls which source the adopted agent stays at within the tested conditions, and with
  learning on in the H15 Run 2 world it keeps Run 2's search, avoidance and reach while reducing punisher visits.** Not
  shown: sub-saturating learned values, the first source reached, any distractor condition. The level framing ('Where the
  project stood at the start') is a snapshot of the start and is not tracked; H20 sits within the Level 5 agent of Phase 5
  and no level change is claimed.

### H21 (decision:h21-open-design, decision:h21-design-v2-choices, decision:h21-open; evaluated once, CLOSED by decision:h21-closed)
- Hold maintenance by value: while an odour with a positive value is held, a lower-valued
  non-negative odour's response is gated out of the selection circuit and the evidence release
  (Agent6 = Agent4 plus the gate; equal values, nothing held and negative odours never gated, so the
  agent is the Run 2 agent in those cases, checked bitwise). Design v2 FINAL doc d7fd5abcc95169698,
  written after the Run 2 diagnosis showed that a valued hold is lost through the circuit's own
  competition when the valued odour is absent, not through the release flags.
- Mechanism bench before the task (M4): a held valued odour survives 200 steps of neutral-only
  input in 400/400 rows with the gate, 0/400 without; asymmetry and inertness are identities.
- Task as Run 2 (C0, dwell majority, seven arms, seeds 1725/1825). One evaluation: NOT shown on an
  INCONCLUSIVE M2, no FAIL. maintain 0.750 [0.705, 0.790]; DP against the Run 2 agent +0.180
  [+0.143, +0.218] against +0.15; the gate never loses a valued hold (0 of 280) and the remaining
  loss is the first selection (120 of 400 rows first hold the neutral odour, 53 revised). Report
  d4fd6c39f7f81e1ee.
- CLOSED by the owner (decision:h21-closed): NOT shown under the registered criteria, M2
  INCONCLUSIVE on part (c), no criterion failed; not re-judged, no extension. The gate ADOPTED within
  the tested conditions only by a separate decision (decision:h21-gate-adopted-within-tested-conditions):
  supplied value, +1/0, G 2, C0, dwell majority, learning off. What follows is H22
  (decision:h22-open-design).

### H22 (decision:h22-open-design, decision:h22-open; bench NO CANDIDATE; post-bench diagnosis by decision:h22-post-bench-diagnosis; CLOSED by decision:h22-closed: NOT shown, nothing adopted)
- Value-gated surge (leave and resample): while a non-negative odour valued below the highest value
  in the agent's read-out is held, its whiffs do not reset the cast clock (Agent7 = the H21 maintain
  agent ph19.Agent6 plus this rule; equal values, nothing held and a negative held odour inert,
  checked bitwise). A navigation hypothesis separated from selection, aimed at the H21 front end (120
  of 400 rows first hold the zero-valued odour, 53 revised). Design v1 FINAL doc dfd041adf77911e7c
  (hash 1ce2717e...7f83).
- Mechanism bench before the task (M4): (a) and the identities pass; (d), the agent placed at the
  neutral source with a neutral hold, 84/400 = 0.210 [0.173, 0.253] hold the valued odour at step
  300 against 0.50 (5/400 without the rule). NO CANDIDATE: the task not run, seeds 9870/9970 and
  1755/1855 unused, the bar not lowered (record:h22-bench-result; ph20.py doc d714b91e1fbbc7ede).
- Post-bench diagnosis, measurement only (record:h22-post-bench-diagnosis-result, report
  d124565e8d93abf16): revision on the registered start 0.328 at 600 steps and 0.390 at 900; a valued
  whiff at most releases the neutral hold, and with the rule 322 of 495 releases return to it; a
  variant start on the neutral axis (not the bench) gives 0.083 with and 0.085 without the rule at
  600. Window and mechanism both; the window alone insufficient.
- CLOSED by the owner (decision:h22-closed): NOT shown under the registered criteria (no candidate
  at the bench; the task not run); not re-judged; seeds 9870/9970 and 1755/1855 unused and kept
  registered to H22. Nothing adopted. What follows is H23 (decision:h23-open-design).

### H23 (decision:h23-open-design, decision:h23-open; evaluated once; CLOSED as shown by decision:h23-closed; the filter adopted within the tested conditions by decision:h23-filter-adopted-within-tested-conditions)
- Value-filtered navigation: the upwind surge follows the top-valued non-negative odour in the
  agent's own read-out; while a top-valued (or a negative) odour is held its whiffs steer as before,
  otherwise only a top-valued odour's whiffs steer (Agent8 = the H21 maintain agent ph19.Agent6 with
  one line of act replaced; bitwise Agent6 at 0/0, +1/+1, +1/-1 and with the valued odour held). At
  +1/0 navigation is the known-answer arm's law and does not depend on the circuit (accepted by the
  owner in advance). Design v2 FINAL doc db6df2e0013ab96e7 (hash c19751f4...0087; v1
  d77542ae99d003747 history).
- Mechanism bench before the task (M4): identities and the implementation bars pass (400/400).
  Bench (b), reported, not a gate: from the task-like neutral-hold start the hold follows navigation
  in part, 0.271 against 0.087 at 600 steps (DP +0.184 [+0.148, +0.220]), every revision through
  'nothing held' (record:h23-bench-result; ph21.py doc ddcec8520fcd8e23c).
- Task as H21 (C0, dwell majority, six arms, seeds 1765/1865). One evaluation: PASS, M1-M6 all
  PASS. filter 0.953 [0.927, 0.969]; DP against maintain +0.240 [+0.200, +0.282]; filter /
  known-answer 0.987; P(V | first hold neutral) 0.897 against 0.169; neutral-first rows revised
  0.968 against 0.400; no added lost rows. Not shown: selection controlling navigation (at +1/0 it
  does not, by construction). Untested: a world where the higher-valued odour is absent (the rule's
  cost), +1/+0.5, learning, other G and geometries. Report d8b91235798da849f (record:h23-result).
- CLOSED by the owner (decision:h23-closed): SHOWN under the registered criteria, M1-M6 all PASS; a
  statement about a supplied value, this rule, +1/0, C0, the dwell-majority measure and the full agent
  with its circuit running, not about selection controlling navigation. The filter ADOPTED within the
  tested conditions only (decision:h23-filter-adopted-within-tested-conditions): supplied value, +1/0,
  G 2, C0, dwell majority, learning off, the H21 gate on. Its known cost, a world where the
  higher-valued odour is absent, is to be measured by the absent-odour check before H20 Stage B
  (decision:next-absent-odour-check-then-stage-b). Correction recorded in decision:h23-closed, not in
  the design (which the code and the outputs cite by hash): design v2 section 9 lists the bench's
  derived seeds as 30261001 / 40261002; seed + 10000 / + 20000 give 20271001 / 20281002; ph21.py's
  self-check tested all four and none appears in any other file; no run affected.

### Absent-odour check (decision:next-absent-odour-check-then-stage-b; opened by decision:absent-odour-check-open; run once)
- A check, not a hypothesis: the adopted agent (Agent8, the H23 filter) in World7 with one plume silenced
  after the draw, against Agent6 on the same seeds and draws; W1 the cost case (only the 0-valued odour,
  read-out +1/0), W2 control, W3 0/0 and W4 -1/0 identities. Design v1 FINAL doc ddab34a689d056e2e.
- One run (1775/1875): every identity True. In W1 Agent8 never surges; it reaches the source by casting
  past it (0.860, 'reach kept'; 0.953 by 1800), dwells a third as long (median 8 against 25), passes
  upwind and keeps drifting (63 upwind at 1800, 111 rows at the wall), and loses the plume in more rows.
  Meanwhile the circuit holds the present odour without following it. Agent6 0.988 as predicted. The
  reach reflects this start; other starts, +1/+0.5 and learned values untested. Report
  db7b4a7ca1c2ab7ea (record:absent-odour-check-result). Candidate fixes (i)-(iv) listed, none chosen by the
  check. Outcome: reach kept (0.860; 0.953 by 1800), the cost in dwell, drift and lost rows; the owner then
  chose to explore option (v), presence-scoped v_max (decision:filter-scope-explore-option-v), as H24.

### H24 (decision:filter-scope-explore-option-v; v2 choices decision:h24-design-v2-choices; decision:h24-open; bench NO CANDIDATE; CLOSED by decision:h24-closed: NOT shown, nothing adopted)
- Presence-scoped value filter (concept:h24-presence-scoped-value-filter). Diagnosis first
  (record:option-v-presence-diagnosis-result). v1 DRAFT doc d24c2efe28592c34d and v2 candidate FINAL doc
  d5a2e259bfb6445b9 are kept as history. Opened on design v3 FINAL (doc dafaa132a0267d56b,
  experiments/h24/h24_design_v3.md, sha 9a217a98...b06c; decision:h24-open): (v-p), Agent9(Agent8) in ph23.py
  (sha ae180492...b5ae, source doc d0ea25b8bebac735d), a per-odour counter, present = c < 60 or held, v_max over
  present odours; the classification rule relaxed for H24 only (decision:classification-rule-relaxed-presence-counter).
- **CLOSED as NOT shown (owner 2026-09-23, decision:h24-closed): no candidate at the mechanism bench**
  (record:h24-bench-result). M4 FAILED part (f) M7(a): 65/370 = 0.176 [0.140, 0.218] against 0.95. Under the
  no-candidate rule T1/T2/T3 were not run and no task criterion was evaluated; the bars of M5(b) and M7(c) were
  never fixed (decision:h24-t2-dwell-bar and decision:h24-t3-bars not created); seeds 9885/9985 and 1785/1885
  never used, registered to H24, not to be reused.
- **The design error:** design v3 section 3 assumed a valued hold ends on the timeout within 41 silent steps
  (RESET_AFTER 40), contrary to record:silence-timeout-chain-result and H21 bench (a). With the 'held counts as
  present' clause the valued odour stayed present past L + 60 in 305/370 eligible rows, and the filter never
  released.
- Measured apart from the verdict (bench seeds): the counter alone exact (no nav on L+1..L+59 in 370/370; bench
  (b) 400/400); identities a1-a5 and the (f) construction True; (d), (e) 400/400. **In W1 the presence counter
  removes the absent-odour cost:** mean dwell Agent9 24.125, Agent8 12.300, Agent6 25.835; paired Agent9 - Agent6
  -1.71 [-2.73, -0.64] (a bench-level measurement, not a task result). T3's Agent6 reference was pinned (S6
  0.0296, D6 4.74). Two implementation errors fixed before the saved bench (a demo assertion turned into a print;
  a q3 helper call); neither changes a number.
- Nothing adopted. The H24-scoped relaxation lapsed with the closure; it stays on record, and any reuse is a new
  decision.
- **H24 Run 2** (decision:h24-run2-open-design, decision:h24-run2-open; relaxation re-signed by
  decision:classification-rule-relaxed-presence-counter-run2): (v-p) on the release agent, Agent11 = Release + Agent9
  (src/ph25.py). **STOPPED at the bench by the registered stop rule of bench (h)** (record:h24-run2-bench-result):
  M4's identities and implementation bars all pass, the released hold makes the window exact, but on the bench seeds
  Agent11 loses the H21 task against Agent10 (P(V) 0.785 vs 0.958, DP -0.1725 [-0.2125, -0.1350]; M2(b) pass
  probability 0.0000). Tasks not run. CLOSED as NOT shown by the owner (decision:h24-run2-closed, 2026-09-24): the
  N sweep the measured reason (record:h24-run2-n-sweep-result), nothing adopted, the Run 2 relaxation lapsed.

### H25 (decision:h25-open-design, decision:h25-open; evaluated once; CLOSED as SHOWN by decision:h25-closed; the release adopted at +1/0 by decision:h25-release-adopted-within-tested-conditions, at negative values ON HOLD by decision:release-negative-scope-on-hold)
- Silence-timeout release (concept:h25-silence-timeout-release), a reset-control change: (S) keep delivering the
  existing 10.0 reset drive while a unit is above 1.0 after the drive step, stopping on a hit or an evidence release;
  (Z) zero the silence counter when a hold forms. v1 DRAFT doc d3cb0794633a587ae kept as history; design v2 FINAL doc
  dce297e76390fa854 (experiments/h25/h25_design_v2.md, sha 6fbb293b...e60b). ph24.py (sha f344f178...1bef, source
  doc d0c87ae7a68d1a27f); no adopted module edited.
- Bench (record:h25-bench-result): M4 PASS; constructed holds released 400/400 at step 47 (D 7, predicted 4); no
  false release 400/400; the ph14b protocol's uninterrupted drives empty the circuit 100%. The design's bench (e)
  agent was misnamed (Agent4 G 0 does not reproduce ph14b 1a; ph14b's Agent3 does). Development run 9896/9996 clean
  (record:h25-dev-run).
- **Evaluated once (1805/1905; record:h25-result; report doc d2a35d5a59aace929): SHOWN under the registered
  criteria** (M1, M2, M3, M4, M5, M7 PASS; M6, M8 reported). T3a: Agent10g R 0.957 [0.895, 1.025] of the
  ceiling-floor span (12.967 [12.070, 13.918]). Agent10's trajectory is Agent8's everywhere (T1 P(V) 0.960 both);
  its circuit releases, its navigation stays blind to the neutral odour by construction. M6: Agent10g - Agent6 P(V)
  -0.155 [-0.200, -0.113] (0.575 vs 0.730). Nothing adopted; closure and any adoption are the owner's.
- **CLOSED as SHOWN (decision:h25-closed, 2026-09-24).** The release (S)+(Z) adopted within the tested conditions
  only (decision:h25-release-adopted-within-tested-conditions): +1/0, G 2, C0, T1/W1/T3a/T3b, learning off, gate on.
  At negative values the adoption is ON HOLD, not rejected (decision:release-negative-scope-on-hold, owner
  2026-09-24, '1 → 2(a) → 3·4·5'), on the avoidance check below.
- **The on-hold decision SUPERSEDED (2026-09-25, decision:n2-release-adopted-within-tested-conditions):** the value-gated
  form (N2), (S) and (Z) only at non-negative held values, is the adopted release rule; identical to (S)+(Z) at
  non-negative values; off at negative held values. The release at negatives as composed ((N1)) stays not adopted.

### Avoidance check (the H25 release under +1/-1; design v1 FINAL doc df00c6e0dbc5f6792; run once; a check, no verdict)
- src/ph24b.py (sha bbabad15...eefc, source doc d68d589ccad0beef9); output experiments/avoidance_check/ph24b_check.txt;
  record:avoidance-check-result. Seeds 1805/1905 reused on purpose; no new seed.
- R0 'identity holds' (identity (b) in both pairs; Agent8 == Agent6 and Agent10 == Agent10g bitwise at +1/-1).
  R1 'priority kept, identical'. R2 'released as valued holds' (a negative hold ends at step 47 in 400/400).
  R3 'avoidance changed': flee violations 0/0; paired dwell at the negative source -0.368 [-0.550, -0.202]; P(V)
  Agent10 0.765 vs Agent8 0.925, paired DP -0.160 [-0.195, -0.125] against >= -0.05; lost rows 127 vs 33, DP
  +0.235 [+0.193, +0.278]; wall contacts per row 0.000 vs 0.307. Not every reading clean: Agent10 not adopted at
  negatives.
- **R3 diagnosis (measurement only; record:r3-negative-release-diagnosis-result; report doc d56ab9eef4549b009).**
  All 131 drive-ended negative holds end outside both whiff regions (20.7/24.5/26.6 from the nearest) and no whiff
  follows in the rest of the run (131/131); 116 of these rows end lost. On the 294 rows where Agent8 touches no
  wall both arms end V in 284; all 64 rows that leave V are Agent8 wall-contact rows; Agent8 P(V | wall contact)
  0.811 [0.726, 0.874] vs 0.966 [0.939, 0.981] without. Reading (interpretation): the release strands the agent
  outside the plumes, where search does not find them again (the H17 limit); the base's recovery in those rows goes
  through the wall reflex. Not measured: a run without walls.

### H17 (decision:h17-open-design, decision:h17-open; bench NO CANDIDATE on part (d); STOPPED; post-bench diagnosis by decision:h17-post-bench-diagnosis; Run 2 opened for design by decision:h17-run2-open-design and opened by decision:h17-run2-open; Run 2 STOPPED at the bench by its (h2) stop rule; Run 2 post-bench diagnosis by decision:h17-run2-post-bench-diagnosis; CLOSED by decision:h17-closed: NOT shown, nothing adopted)
- Cold-start and reacquisition search (concept:h17-cold-search), a navigation change on the target only: after S 210
  steps with nothing held and no whiff of any odour, a crosswind cast of growing amplitude (legs 30 k steps) slanted
  15 degrees along the wind, the slant reversing every 360 steps. One counter q under the H17-scoped relaxation
  (decision:classification-rule-relaxed-any-odour-silence-counter-h17). v1 DRAFT doc de696df4b5963d1c1 kept as
  history; design v2 FINAL doc d83a917ea4152b4a7 (experiments/h17/h17_design_v2.md, sha f94d6ace...7516). ph26.py
  (sha 1c9b6f5b...67cf, source doc d911535d7e535751c); no adopted module edited.
- Bench (record:h17-bench-result; experiments/h17/ph26_bench.txt sha ec9df782...ff6d): (a) identities all True
  (never-engaged rows bitwise Agent10 in T1, +1/-1, W1, T3a and the chains); (b) engagement exact 400/400; (c1) the
  R3 stranded state, walls off: whiff within 300 steps of engagement 0.542 [0.494, 0.591] vs Agent10 0/400, reach
  within 600 0.698 [0.651, 0.740], paired DP +0.5425 [+0.4925, +0.5925] (all three bars PASS; oracle 0.983 / 1.000);
  engagement positions d_along 50.0/52.2/54.5 beyond LMAX in 400/400. (c2) upwind starts: 0/400 for both arms
  (reported). (c3) the H16 square: reached by 600 steps Agent12 0.907 vs Agent10 0.688 (reported). (d) FAIL: T1 +1/0
  rows with any engaged step 18/400 = 0.045 [0.029, 0.070]; Agent10's own any-odour silences reach 210 steps in 18
  rows (p90 193, max 321). (h1) T1 DP -0.0025, pass probability 1.0000; (h2) lost-row DP -0.0850 [-0.1150, -0.0575],
  pass probability 0.6324, contacts 0.247 per row (reported). Neither stop rule fired.
- **STOPPED at the bench by the no-candidate rule** ('(d) failing -> tasks not run'). T1-T4 not run; seeds dev
  9943/9953 and eval 1945/2045 unused. Nothing adopted, nothing tuned. The owner decides.
- **Post-bench diagnosis (measurement only; decision:h17-post-bench-diagnosis; record:h17-post-bench-diagnosis-result;
  report doc d6f5ab6a423f8ba16, experiments/h17/h17_post_bench_diagnosis.md; ph26b.py sha 6b45d87c...e0ae, output
  ph26b_diag.txt sha 10429f5b...df19).** Bench seeds only, the bench reproduced line for line. (A) Agent10's longest
  any-odour silence per row in T1 +1/0: 154/160/171, p95 207, max 321; rows >= 210: 18, >= 250: 6, >= 300: 3. The 18
  are the return cast's loop after a whiff at or next to a source: 16/18 start after the agent had been at a source
  (13 inside a whiff region at the start, `since` 1 in 16), the majority of steps upwind of both sources in 16, and
  14 are inside a whiff region again at the engagement step (d_along 15.8/19.0/22.0); no wall; Agent10 V 15/18.
  Agent12 whiffs within u 6/11/50 in all 18 (first the other odour in 15); only row 184 changes outcome (V to N).
  (B) The 99 contacts (0.247 per row) are all engaged, legs 3 (44) and 4 (55), upwind slant, u 150-254, 68 on the
  negative source's side wall and 27 on the upwind wall, all in 39 Agent10-stranded rows that were 28.6/30.5/32.5
  from the nearer side wall at engagement; no whiff follows any contact; the 39 rows are lost in both arms (P(V |
  contact) 2/39 = 0.051 [0.014, 0.169] vs 306/361 = 0.848 without) and carry no paired transition: the (h2) effect
  (into V 19, out of V 4; out of lost 37, into lost 3) sits in the 117 engaged rows without a contact. Of 131 engaged
  stranded rows, 37 whiff after engagement (valued first 12, negative 25), 14 strand again. Reading only, no cause
  established. Nothing adopted; the verdict stands; the owner decides between closure and a Run 2 design.
- **Run 2, design only (decision:h17-run2-open-design, owner 2026-09-24: '2번 Run 2 설계 v1 초안 진행'; design v1 DRAFT
  doc dedd3d11f43f9156f, experiments/h17/h17_run2_design_v1.md, sha 27bbd399...94dc; no code).** Run 1's verdict
  unchanged. The one mechanism change recommended is the engagement threshold: q >= 250 instead of 210, everything
  else of the Search rule unchanged. Reason: the (d) silences are the return cast's own loop and the measured
  longest-silence table gives 6/400 T1 rows at 250 (Wilson upper bound 0.032); the stranded rows engage 40 steps later
  but, by the cast's exact-heading arithmetic, about 10 units further upwind, so T3 (a) is predicted at DP -0.079 to
  -0.085 (pass probability about 0.5-0.6, the binding part). No own-state variable separates the two silences
  (`since` equals q in both; the stranded case read from the code and checked exactly at the bench (b')). T3 (c)
  re-signed to guard recovery through the wall rather than the contact count (the 99 Run 1 contacts carry no
  transition); leg cap and flee-side first leg rejected. (d) kept at 0.05. The q relaxation re-signed in form for Run
  2. New seeds dev 9961/9973, eval 1965/2065, bench 20261061/20261062, bootstrap 20261063. Confirmed by the owner
  (next bullet).
- **Run 2 opened and STOPPED at the bench (decision:h17-run2-open, owner 2026-09-24: '권고안대로 확정하고 Run 2 진행';
  record:h17-run2-bench-result).** Design v2 FINAL doc d73c77ebd99d50d86 (experiments/h17/h17_run2_design_v2.md, sha
  d2374c5e...d5e9); relaxation re-signed in form (decision:classification-rule-relaxed-any-odour-silence-counter-h17-run2);
  T3 (c) re-signed (decision:h17-t3c-bar-resigned-run2). src/ph27.py (sha d12fa651...143a, source doc
  ddfbebac743e3c469), Agent13 = ph26's Search at S 250 on Agent10; outputs experiments/h17/ph27_demo.txt (sha
  53966af1...7a06) and ph27_bench.txt (sha 7176278a...9b71). Bench (seeds 20261061/20261062): identities all True
  (never-engaged rows bitwise Agent10 in T1, +1/-1, W1, T3a and the chains; (a4) Agent13 at S 210 == ph26.Agent12);
  (b) and (b') 400/400; (c1) 0.578 [0.529, 0.625] / 0.635 [0.587, 0.681] / DP +0.5775 [+0.5300, +0.6225], engagement
  d_along 39.0/41.6/44.3 (predicted about 40-44); (d) 4/400 = 0.010 [0.004, 0.025] (predicted 6, range 3-11), the
  engaged rows exactly those whose Agent10 silence reaches 250. (h1) T1 DP 0, pass probability 1.0000. **(h2) T3 lost-row
  DP -0.0650 [-0.0900, -0.0425], pass probability 0.2287 < 0.5: STOP** (predicted -0.079 to -0.085; the design had
  named T3 (a) its binding part, about 0.38 to clear both the stop rule and the evaluation). P(V) DP +0.0300 [+0.0150,
  +0.0475]; contacts 0.000 per row (predicted 0.15-0.30); re-signed T3 (c) 0/26, (h2c) 1.0000. (h3) W1 dwell Agent13 -
  Agent10 +1.750 [+1.173, +2.343], pass probability 1.0000 (lost rows 102 vs 34, reported). `since` - q at engagement
  0 in 376/400 (b'2) rows and 70/105 engaged stranded task rows (max 186): the design's reading that the two are equal
  in the stranded state holds only in part; printed as a notice, not a mechanism failure. Tasks NOT run; dev 9961/9973
  and eval 1965/2065 unused; nothing adopted, nothing tuned. The owner decides.
- **Run 2 post-bench diagnosis (measurement only; decision:h17-run2-post-bench-diagnosis;
  record:h17-run2-post-bench-diagnosis-result; report doc dd1ba5b405811ef4a,
  experiments/h17/h17_run2_post_bench_diagnosis.md; ph27b.py sha a6232c09...79ac, output ph27b_diag.txt sha
  7a2eeee5...441e).** Bench seeds only; the bench was reproduced line for line. Of Agent10's 134 stranded rows, 105
  engage 196-202 steps after the release. The 29 that do not were released at step 414 or later, so the run ends
  before q reaches 250. 18 rows whiff after engagement (u 150/159/180, legs 3-4) and 17 of them leave lost. The 87
  without a whiff start about 29 outward of the negative source (d_along 36.5; beyond LMAX in 73). Their first
  crossing of the pair comes at the end of leg 4 (u 289/292/295), at d_along -14.6, upwind of both sources in 63/64.
  At step 599, 70 of them are upwind of both. No wall is involved. In the 84 rows engaged by step 399, leg 1 is on
  the flee side (away from the pair) in 65; leg 1 toward the pair whiffs 13/19, away 5/65. In (c1), leg 1 toward
  whiffs 184/194 and away 47/206. The slant also runs further upwind than the design's arithmetic: leg 3 covers
  d_along 22 -> 5, against about 28 -> 14. The chain against the prediction: engaged by step 399 is 84/119 (0.706,
  predicted 0.6-0.7); a whiff follows in 18/84 (0.214, predicted 0.5-0.7); the row leaves lost in 17/18. `since` - q
  > 0 in 35/105 (and 24/400 constructed rows), all because the last negative whiff came with nothing held, 1-6 steps
  before the hold formed (ph21.py:69, :72). Section 2 (E) holds in 70/105. The last whiffed odour is negative in
  105/105 stranded rows and in none of the T1 silences (16 on these seeds, 18 in Run 1). That is the design's (b4)
  quantity, which is new state. Reading only; no cause established. Nothing adopted; the verdict stands. The owner
  decides between closing H17 and a Run 3 design, whose options and what each would register are listed in the
  report.
- **CLOSED as NOT shown under its registered criteria (owner 2026-09-24, decision:h17-closed:** '1. H17 종료, 등록된 순서대로
  adaptive presence(제안) → H20 Stage B', gloss 'option 1: close H17; proceed in the registered order, adaptive presence
  (proposed), then H20 Stage B'). Run 1 stopped at the bench by the no-candidate rule on part (d) (18/400 engaged rows,
  upper bound 0.070 against 0.05); Run 2 stopped at the bench by the (h2) stop rule (T3 lost-row DP -0.0650 [-0.0900,
  -0.0425] against M3 (a) <= -0.05, pass probability 0.2287). T1-T4 never run in either run; seeds unused and kept
  registered to H17 (Run 1 dev 9943/9953, eval 1945/2045; Run 2 dev 9961/9973, eval 1965/2065); not re-judged. Nothing
  adopted; the Run 1 and Run 2 relaxations and the Run 2 T3 (c) re-sign lapse. Measured apart from the verdict: the
  search finds a plume from the constructed stranded state in both benches ((c1) 0.542 / 0.698 / +0.5425 and 0.578 /
  0.635 / +0.5775 against Agent10 0/400); H16's square 0.907 vs 0.688; at S 250 (d) 4/400, contacts 0, W1 dwell +1.75;
  the task-level whiff fraction after engagement 18/84 = 0.214 against the predicted 0.5-0.7 is the factor that missed;
  leg 1 toward the pair 13/19 vs 5/65 (task) and 184/194 vs 47/206 ((c1)); 29 late-released rows unreachable by any leg
  rule; `since` - q separates nothing (35/105 vs 4/16); the last whiffed odour's value sign separates (105/105 vs 0/16)
  but is new state. Reading (interpretation): the search works from the stranded state; at the task the first leg's
  side and the upwind slant carry most stranded rows upwind of both sources before they cross the pair. Cold-start
  search stays a recorded limit (record:release-negative-cost-limit unchanged); the release at negative values stays
  ON HOLD (decision:release-negative-scope-on-hold).

### H26 (decision:h26-open-design, decision:h26-open; evaluated once; CLOSED as SHOWN by decision:h26-closed; ADOPTED within the tested conditions by decision:h26-adaptive-presence-adopted-within-tested-conditions)
- Adaptive presence (concept:h26-adaptive-presence), the item queued as proposed (not decided) at the H24 Run 2
  closure; the number H26 assigned by decision:h26-open-design (the highest in use was H25). The problem: the H23 filter
  is blind to the neutral odour when the valued odour is absent (W1 dwell Agent10 11.9 vs Agent6 24.4), and no fixed
  presence window N meets both the H21 task (clear from N 200) and W1 (only to N 120) (record:h24-run2-n-sweep-result).
- Design v1 DRAFT doc d9452710c5166ba01 (experiments/h26/h26_design_v1.md, sha 18983aa2...3598), no code. Reading
  from the code, checked by the sweep: the sweep moved two quantities together, since the counter starts at 0; W1 and
  T3a (valued odour never sensed) depend on N only through the prior, T1 mostly through the window after a whiff.
  Recommended candidate (e): the prior separated from the window, one counter per odour as H24 Run 2's starting at
  N_hi - P = 240 (an odour never sensed present on steps 0-58), window N_hi 300 after any whiff; Agent14 = Release +
  Agent9 with the start value; no second state variable; a new H26-scoped relaxation to sign (H14 format). Predicted:
  W1 and T3a bitwise Agent11 at N 60 (dwell 22.7, R 1.005); T1 bitwise Agent11 at N 300 (Agent10's outcome on the
  sweep) in every row with a valued whiff by step 58, the rest measured at bench (m). Rejected on record: (a) the
  hold-conditioned reload and its graded form, (b) the hold-tied window, (c) the neutral-conditioned release, (d) the
  closure's gap-scaled patience. Bench with (m), (h) T1 and (h3) W1 stop rules at 0.5; M5(d) (W1 lost rows vs Agent6)
  predicted to fail as inherited (+0.035 and +0.0475 on two benches), re-sign against Agent10 recommended. Joint pass
  probability about 0.97 at 0-5 extra lost rows, 0.83 at 10, 0.42 at 13. Not addressed: a loss after tracking (there
  the window is a fixed 300). Seeds dev 9977/9987, eval 1985/2085, bench 20261071/20261072, bootstrap 20261073 (189
  files scanned, no collision).
- Opened on design v2 FINAL (decision:h26-open, owner 2026-09-24, '권고안대로 확정하고 H26 진행'; doc d54441658b54a6799,
  experiments/h26/h26_design_v2.md, sha ac95c22d...9f54): candidate (e), P 60, N_hi 300; the H26-only relaxation signed
  (decision:classification-rule-relaxed-presence-prior-h26); M5(d) re-signed against Agent10
  (decision:h26-m5d-bar-resigned). src/ph28.py (source doc d4f81b6d946b6ccfb): Agent14 = Release + Agent9 with the
  counter starting at 240; no adopted module edited.
- Bench (record:h26-bench-result, ph28_bench.txt on ph28.py 29c594e4...6dd7): M4 PASS; (m) at-risk rows 15, k 1; (h)
  DP +0.0025, pass probability 1.0000; (h3) 1.0000. M5(b) bar fixed at -4.9 = -0.20 x 24.7200
  (decision:h26-t2-dwell-bar) and written into ph28.py (64ce7d0c...e7aa). Development run 9977/9987 clean
  (record:h26-dev-run).
- **Evaluated once (1985/2085; record:h26-result; report doc d8163e16317b251eb): SHOWN under the registered criteria**
  (M1-M7 PASS; T3b, T4 reported). T1: Agent14 0.927 vs Agent10 0.935, DP -0.0075 [-0.020, +0.005]; 288/400 rows with an
  early valued whiff bitwise Agent11 (N 300); 5 rows out of V, all at-risk. W1: Agent14 == Agent11 (N 60), dwell 23.782
  vs Agent6 24.830, paired -1.047 [-2.043, -0.075] (bar -4.9); lost rows 35 vs Agent10 45 (M5(d) -0.025 [-0.055,
  +0.005]) and vs Agent6 16 (+0.0475 [+0.0200, +0.0775], reported). T3a: window exact 400/400, R 1.0376 [0.9642,
  1.1186]. Not shown: a loss after tracking (T3b 4.412, the post-whiff window a fixed 300) and negative values (T4 ==
  Agent10). Missed predictions stated in the report (W1 lost-row counts, T3a R and floor, Agent11 (N 60)'s T1 cost).
- **CLOSED as SHOWN (2026-09-25, decision:h26-closed; owner '1. shown으로 종료하고 채택, H20 Stage B 진행').** Not
  re-judged. **ADOPTED within the tested conditions** (decision:h26-adaptive-presence-adopted-within-tested-conditions):
  the presence counter starting at 240 (P 60, N_hi 300); Agent14 = Release + Agent9 (src/ph28.py:92-97) is the adopted
  agent at supplied +1/0, G 2, C0, gate on, release on, learning off, in T1, W1 and T3a. Limits: a loss after tracking
  not shown (T3b); negative values excluded (decision:release-negative-scope-on-hold unchanged); learned values not
  validated (H20 Stage B). The H26 relaxation stays in force for the adopted counter; the M5(d) re-sign applies to H26
  only.

### H27 (decision:h27-open-design, decision:h27-open; STOPPED at the bench by its stop rules (h), (hW), (hH); post-bench diagnosis by decision:h27-post-bench-diagnosis; CLOSED by decision:h27-closed: NOT shown, nothing adopted, the distractor condition a recorded limit)
- A proper distractor condition, the queued item 'a third, irrelevant odour, which is what the hold's benefit needs'
  (concept:h27-irrelevant-odour-distractor); the number H27 assigned by decision:h27-open-design (the highest in use was
  H26). Chosen over the H26 T3b limit, H12, H10, H18 and H17 (ranked with reasons in that decision).
- Read from the code for the design: at +1/0 the adopted agent's trajectory does not depend on the hold (ph23.py:88-92:
  nav is the whiff of the top present odour whatever is held), so the hold's benefit cannot be measured in the present
  worlds; with a third odour D at the neutral odour's value, whenever the valued odour is absent the hold decides which of
  B and D steers.
- Design v1 DRAFT doc d1b2bdacd81997da7 (experiments/h27/h27_design_v1.md, sha256 483c38f4...2584): Agent15 = Agent14N2
  composed with three channels in a new file (src/ph32.py), no adopted file edited (two channels are hard-coded at
  ph11.py:112-113, :116, ph14.py:55, ph23.py:57, :68, ph28.py:97; the evidence release's `other = 1 - hi` is wrong at N 3
  and is generalised to the strongest non-held channel, a composition rule to sign; the H26 relaxation re-signed in form
  for the third counter); D a background odour at p_D 0.03, value 0, from its own generator (a third source and H19 (a)'s
  punished background rejected); T1D and W1D registered, T3aD and T4 reported, the H15 world excluded; arms with and
  without D, a hold-not-read arm and a release-off arm; criteria M1 as H26, M2(b) DP D on - D off >= -0.05, M2(c) vs the
  filter-off agent >= +0.05 (M2(a) 0.88 reported), M5 W1D reach 0.80, dwell bar -0.20 x the bench D-off dwell, contacts
  0.10, lost rows DP <= +0.05, M6 the hold's benefit (lost rows DP hold-not-read - Agent15 >= +0.05); stop rules (h),
  (hW), (hH); joint 0.81 / 0.40 / 0.12 if the bench puts the unknown parts at 0.95 / 0.75 / 0.5 (no centre on record; the
  release's 48-step end of a hold may expose the cast clock to D, a stated risk). Seeds dev 9937/9947, eval 2083/2173,
  bench 20261121/20261122, bootstrap 20261123.
- Opened on design v2 FINAL (decision:h27-open, owner 2026-09-25, '권고안으로 이어서 진행'; doc d8c8949f2896cf1ec,
  experiments/h27/h27_design_v2.md, sha 88fdfdf7...7ddb); signed before code: decision:evidence-release-composition-rule-h27,
  decision:classification-rule-relaxed-presence-prior-h27. src/ph32.py (sha d9f585d5...2743, source doc
  d5a2b6526d40efbef); no adopted file edited.
- **Bench (record:h27-bench-result, ph32_bench.txt sha 95721447...22f9): M4 PASS, every stop rule fired.** Identities
  (I1)-(I6) True (Agent15's code at N 2 == Agent14N2 on every field; D on == D off before the first D whiff; Agent15 D off
  == Agent14N2 on the trajectory in every row; the hold-not-read arm without D == Agent15; (I6) read as the exact
  navigation law). T1D P(V) 0.787 vs 0.920, DP -0.1325 (53 rows out of V, all among the 122 with V absent by its counter
  at some step); W1D dwell 4.968 vs 24.750, every row lost, 105.6 wall contacts per row (the upwind drift the design named
  as its first risk, 2.4); the hold-not-read and release-off arms lost every row as well, so M6's DP is 0. Predictions
  missed: T1D (0 to -0.025 predicted), (m) (15-20 predicted, 122 measured), (b2). **STOPPED at the bench; tasks not run;
  seeds dev 9937/9947 and eval 2083/2173 unused and registered to H27.** The mechanism is not diagnosed. Awaiting the
  owner.
- **Post-bench diagnosis (decision:h27-post-bench-diagnosis, owner 2026-09-26 '진단 먼저'; record:h27-post-bench-diagnosis-result;
  src/ph32b.py, report doc ddec6582aa2fcaa83, experiments/h27/h27_post_bench_diagnosis.md), measurement only, bench seeds.**
  The bench reproduces line for line. Measured capture path: when V is absent by its counter, D joins B in the filter's
  top set at value 0 (or is top alone) and its whiffs become nav events whenever nothing or D is held (W1D 0.956 of nav
  events D-driven; none while V is present); every nav resets the cast clock, the target stays near upwind (0.630 of
  steps within 40 degrees, against 0.243 without D) and the agent ends at the upwind wall. B holds, which would block D,
  are rare under D and end mostly by the evidence release (162 of 236 in W1D). The release-off arm loses the same rows
  (D holds then last to the row's end and D-held hits steer), so the release's 48-step end is one entry, not a
  necessary one. In W1 the initial cast, not D, takes every row upwind of B; D prevents the return. (m): 103 prior
  expiry, 19 silences; H26's at-risk definition gives 21; all 53 out-of-V rows are prior expiry. M6 is unreadable
  because the hold-not-read arm takes the same path (326/400 rows identical in position). What the owner can decide
  (listed in the report, nothing adopted): close H27 with the distractor condition recorded as a limit of the adopted
  agent; or a Run 2 design registering one of: a top-set rule for a never-reinforced odour (new state or a value-sign
  question; B and D carry the same value here; a signed relaxation), a lower p_D as a different condition, the release
  (an adopted module; release-off measured as not preventing the loss), or what resets the cast clock (the H19 (a)
  boundary). Verdict unchanged.
- **CLOSED (2026-09-26, decision:h27-closed; owner '위 권고안으로 진행', read as option 1).** STOPPED at the bench by all
  three stop rules, NOT shown under its registered criteria; M4 PASS; tasks not run; dev 9937/9947 and eval 2083/2173
  unused and kept registered to H27; not re-judged. Measured facts recorded apart from the verdict (T1D DP -0.1325; W1D
  dwell -19.78, lost 400/400 vs 22, 105.6 contacts per row; M6 unreadable; (m) 122 vs the predicted 15-20, the
  prediction anchored on H26's narrower definition; the capture path of the diagnosis). The distractor condition is a
  LIMIT of the adopted agent (record:distractor-capture-limit); the hold's benefit under a distractor stays unmeasured.
  Nothing adopted; decision:classification-rule-relaxed-presence-prior-h27 and decision:evidence-release-composition-rule-h27
  lapse and stay on record (the composition rule available to a future N = 3 design by a new decision). Queued as
  PROPOSED, not decided: a recognition-core mechanism for a ubiquitous odour, designed as H28 (below).

### H28 (decision:h28-open-design, decision:h28-open; evaluated once; CLOSED as SHOWN by decision:h28-closed; the burst-ranked value tie ADOPTED for the three-channel distractor form by decision:h28-burst-tie-adopted-within-tested-conditions)
- Discounting a ubiquitous, never-reinforced odour by its whiff statistics rather than its value
  (concept:h28-ubiquitous-odour-discount), the proposal queued at the H27 closure; the number H28 assigned by
  decision:h28-open-design (the highest in use was H27). Ranked first over the H26 T3b limit, H12, H10, H18 and H17 (reasons
  in that decision): it addresses a measured failure of the recognition core the owner named as reusable.
- Checked against the record before design (design v1 section 2.3, arithmetic on ph11.py:82 and the H27 numbers):
  habituation in its usual sense (discount the odour sensed more) has the wrong sign at the whiff scale (the plume's
  in-cone rate 0.0374 at the cone's end to 0.30 at the source exceeds D's 0.030) and the wrong timing over long windows
  (over a run D is denser, 0.030 against B 0.0165 and V 0.0171, but a trace long enough for T1's 150-200-step tracking
  silences reaches only about 0.0096 by step 115, while the capture begins at step 59). What separates D from a plume is
  clustering: three whiffs within 10 steps occur on 0.0282 of D whiffs and on 0.29-0.53 of passes near a source. The 97
  W1D rows in which B is never sensed before step 59 cannot be reached by any value-free, position-free statistic (D is
  then the only present odour, not a tie).
- Design v1 DRAFT doc dc81dbd5005ca164c (experiments/h28/h28_design_v1.md, sha256 135a28f2...6a51): Agent16 = Agent15
  (Agent14N2 with three channels, src/ph32.py unchanged) with a burst-ranked value tie in a new file src/ph33.py, no adopted
  file edited: when two or more present non-negative odours tie at the top value (ph23.py:88-92 as composed at
  ph32.py:187-191), only the most recently burst one stays in the top set and in keep; none if none has burst. New state
  per odour: the step of its second most recent whiff and of its last burst; a relaxation to sign in H14 format, plus the
  H27 composition rule and presence relaxation re-signed in form. With D absent no tie occurs at +1/0, so it is the adopted
  agent on every field by code. Candidates rejected on record: a rate trace above a threshold, the same gating presence, an
  upstream adaptation in ph2.Upstream (nav never reads the stage's output; it would reopen Phase 2), a surge-yield trace
  (too slow), a coincidence gate on every whiff, a rate-ranked tie; alternatives listed: a burst gate on a lone odour
  (changes the adopted agent without D), a held-last tie. T1D registered (M2(b) >= -0.05; predicted 4-8 rows out of V);
  W1D registered as the recovery over H27's agent (lost-row DP <= -0.20; predicted 110-245 lost of 400); H27's W1D bars
  against D off reported (predicted to fail); M6 reported; stop rules (h), (hW); joint about 0.97 at the predictions,
  0.50 at k 13. Seeds dev 9907/9917, eval 2093/2197, bench 20261131/20261132, bootstrap 20261133.
- Opened on design v2 FINAL (decision:h28-open, owner 2026-09-26, '권고안으로 진행하고 다음작업 설계 진행'; doc
  da2c1c079a1766d3e, experiments/h28/h28_design_v2.md, sha b12137f6...6b8c); signed before code:
  decision:classification-rule-relaxed-burst-record-h28, decision:evidence-release-composition-rule-h28,
  decision:classification-rule-relaxed-presence-prior-h28. src/ph33.py (sha f2a29722...20b0, source doc
  dd7262b0c91dbc66b); no adopted file and not ph32.py edited.
- **Bench (record:h28-bench-result, ph33_bench.txt sha 45b0f263...8671): M4 PASS, both stop rules continue.**
  Identities (I1')-(I6') True (Agent16's code at N 2 == Agent14N2 on every field; Agent16 D off == Agent15 D off on
  every field, the rule never acting without D; Agent16 D on == Agent15 D on before each row's first action); the burst
  record exact against brute force; the ranked top set, keep and nav exact on 2560 constructed rows. D-driven nav T1D 223
  vs Agent15's 1492, W1D 2935 of 4496 vs 6392 of 6643 (E3, D the lone top odour, 1149). (h) 0.9987, (hW) 1.0000.
- **Evaluation (record:h28-result, ph33_eval.txt sha 43e3a999...3dbe; report doc d29986a75ef4e9711): SHOWN.** T1D P(V)
  0.915 vs 0.943 without D, DP -0.0275 [-0.0450, -0.0125] (H27's agent 0.792); W1D 222 vs 400 lost, DP -0.445
  [-0.495, -0.397]; M1, M3, M4 PASS. Reported: H27's W1D bars against D off fail (222 vs 29 lost); M6 +0.0000; T3aD
  0.220 vs 13.193; T4 +1/-1/0 0.740 vs 0.932 (no tie arises there). The residual W1D loss is not attributed to a path by
  this run. Closure, and any adoption, are the owner's.
- **CLOSED as SHOWN (2026-09-26, decision:h28-closed; owner '권고안으로 바로 진행', gloss 'proceed right away with the
  recommended options').** Not re-judged. **ADOPTED within the tested conditions for the THREE-CHANNEL distractor form
  only** (decision:h28-burst-tie-adopted-within-tested-conditions): Act16 (src/ph33.py:116-177; the burst record :145-149,
  the ranked top set :155-158, keep :161) in Agent16 as composed (src/ph33.py:180), supplied +1/0, D at value 0 and p_D
  0.03, G 2, C0, gate on, N2, learning off, T1D and W1D. The H27 composition rule (decision:evidence-release-composition-rule-h28),
  the three-counter presence relaxation (decision:classification-rule-relaxed-presence-prior-h28) and the burst-record
  relaxation (decision:classification-rule-relaxed-burst-record-h28) are adopted state for the three-channel form, in form,
  scope 'the adopted three-channel agent'. At two channels the rule is inert by code (I1'), so the two-channel adopted agent
  is unchanged and does not carry them. Limits: W1D 222/400 lost (29 without D); T3aD 0.220 vs 13.193; M6 unmeasured;
  other p_D, a non-zero-valued D, learning with D, the H15 world. record:distractor-capture-limit-under-h28-tie records
  the limit under the adopted rule (T1D DP -0.0275, W1D 222/400); record:distractor-capture-limit is unchanged (H27's
  agent). Rejected on record: no adoption; adoption as the universal rule.

### H29 (decision:h29-open-design; the T3b diagnosis by decision:t3b-diagnosis; opened by decision:h29-open; evaluated once; CLOSED as SHOWN by decision:h29-closed; the window 200 ADOPTED within the tested conditions by decision:h29-window-200-adopted-within-tested-conditions, the adopted two-channel agent now Agent17)
- The H26 T3b limit, a loss after tracking (concept:h29-loss-after-tracking): after the adopted agent has tracked the
  valued odour and the odour disappears (the Lost world, t0 150), its presence counter keeps it present for a fixed 300
  steps after the last whiff, so the filter is blind to the neutral odour until L + 300 (exact 379/379; T3b neutral dwell
  4.412 against 5.772 at window 60, 7.048 unfiltered; first neutral surge 471/476/479 steps after L, none before 600 in
  173/379 rows). Numbered H29 by decision:h29-open-design (the highest in use was H28). Written on Agent14N2; with D absent
  Agent16 == Agent14N2 by code (record:h28-bench-result (I1'), (I3')), so it holds whether or not H28 is adopted.
- Checked against the record before design (design v1 section 2.5): the Lost world is World7 until t0 and equals its T1
  twin in every draw but the masked valued column after it (ph23.py:112-119, ph24.py:133-141; checked True at H26's bench
  and evaluation), so until the twin's next valued whiff any rule on the agent's own state acts identically in both. No
  own-state rule can shorten the window after a loss without shortening it in the T1 silence the row shares; the only
  lever is the window's length. The cast loop (ph23.py:95-98, SAT 141.7) brings the agent back through the plumes at
  about L + 170-245 and from about L + 470; the N sweep's T3a surges 213/235/243 at N 200 against 476/479/507 at N 300.
- Design v1 DRAFT doc dd00688c21f09b13e (experiments/h29/h29_design_v1.md, sha 5078d814...1260), no code. Candidates
  rejected on record: (a1) a burst-conditioned reload (cannot separate; below 200 it pays T1's cost), (a2) a window
  shrinking with neutral whiffs, (b) the hold-end window (H26's rejection stands), (d1) since > 2 SAT (a 16-step sliver),
  (d2) since > SAT (T1 like N 150); (c) closing the limit is the alternative. Candidate if run: (e1) Agent17 = Agent14N2
  with window 200, start 140, prior 59 unchanged, no new state; the H26 relaxation re-signed with window 200 (H29 only).
  Registered if run: T1 M2(b) DP vs Agent14N2 >= -0.05 (sweep N 200: -0.0125, pass 1.0000), M2(c), M6; T3b M8(a) window
  exact at L + 200 and M8(b) paired dwell vs Agent14N2 lower bound > 0 (predicted +0.9, range +0.5 to +1.3, T3a analog);
  W1 and T3a identities; stop rules (h), (hB). RECOMMENDED first (section 12 point 1): a measurement-only T3b diagnosis on
  H26's spent bench seeds, reading stated in advance. Seeds if run: dev 9903/9913, eval 2111/2221, bench
  20261141/20261142, bootstrap 20261143.
- T3b diagnosis done (decision:t3b-diagnosis, measurement only; src/ph34b.py; report experiments/h29/t3b_diagnosis.md,
  doc d8a7e386faf08075d; record:t3b-diagnosis-result). H26's T3b and T1 lines reproduced (all MATCH). On H26's bench
  seeds the twin identity holds (F1 MET, 400/400), but the blind window's end finds 0.990 of the agents upwind of both
  sources, between two downwind passes of the cast loop (F2 NOT MET), and only 0.478 surge on the neutral odour within
  200 steps of the window opening (F3 NOT MET). The twins return to the valued plume at a median of 153 steps (F4
  INCONCLUSIVE); no own-state quantity separates losses from long T1 silences at 0.80/0.20 (F6 INCONCLUSIVE). Agent17
  (window 200) measured directly: T1 DP +0.0000 (F5 MET), T3b gain +2.460 [+1.883, +3.055], above the design's +0.5 to
  +1.3; window 250 gains nothing (4.115 vs 4.000), so the result rests on the window's alignment with the cast loop.
  Branches (i) open H29 on design v1 and (ii) a different design are both triggered; (iii) close as a limit is not.
- Opened on design v2 FINAL (decision:h29-open, owner 2026-09-26, '(i) 권고안대로 진행', gloss 'branch (i), proceed as
  recommended'; doc d724287aa203d256d, experiments/h29/h29_design_v2.md, sha 552e2ee1...6aa7): every recommended option
  of v1 section 12 except point 1 (resolved by the diagnosis); the F2 finding recorded as a stated sensitivity (section
  11) and T3b at t0 100 and t0 200 added as a REPORTED condition (no bar). Signed before code:
  decision:classification-rule-relaxed-presence-prior-h29. src/ph35.py (sha e4a3ceda...b1b1, source doc
  d7ed06b1bd4bb0e2c); no adopted file edited.
- **Bench (record:h29-bench-result, ph35_bench.txt sha e217dd00...d0a0): M4 PASS, both stop rules continue.** Identities
  (I1)-(I7) True (Agent17 built with N_hi 300 == Agent14N2 on every field; W1, T3a identical; the 16 departing T1 rows
  are exactly the exposure set; T3b identical before the first neutral whiff at or after L + 200); counter exact 400/400;
  window exact at L + 200 380/380. (h) 1.0000 (DP +0.0025); (hB) 1.0000 (gain +2.1350, sd 5.0097).
- **Evaluation (record:h29-result, ph35_eval.txt sha 1577b42c...6e2e; report doc d92ffd006bdbcdc28): SHOWN.** T1 P(V)
  0.927 vs 0.935, DP -0.0075 [-0.0200, +0.0025] (4 out of V, 1 into, all in the 19 exposure rows); T3b neutral dwell
  6.730 vs 4.777, paired +1.9525 [+1.4549, +2.4501], window exact 376/376, rows never steering on the neutral odour by
  600 172 -> 78; M1, M3, M4, M6 PASS; W1, T3a, T4 identical. Reported: R_b 1.96 (the window-60 agent 5.772); the
  phase-sensitivity condition, t0 100 +0.70 [+0.26, +1.14] and t0 200 +3.82 [+3.34, +4.31]: positive at all three
  losses, its size set largely by where L falls relative to the measurement window 400-599 (the stated sensitivity to
  other geometries and cast parameters stays untested). A trade within the registered bars, not a separation of loss
  from tracking. Closure, and any adoption, are the owner's.
- **CLOSED as SHOWN (2026-09-26, decision:h29-closed; owner '권고안으로 바로 진행', gloss 'proceed right away with the
  recommended options').** Not re-judged; the diagnosis's six readings cited. **ADOPTED within the tested conditions**
  (decision:h29-window-200-adopted-within-tested-conditions): the presence window after a whiff 200 with start 140, the
  59-step prior unchanged; the adopted two-channel agent becomes Agent17 = Agent14N2 built with N_hi 200 (src/ph35.py:104-105,
  through src/ph28.py:95-97; N17 at src/ph35.py:89). It SUPERSEDES the H26 window (300, start 240) for the two-channel
  agent: decision:classification-rule-relaxed-presence-prior-h26 stays on record as superseded and
  decision:classification-rule-relaxed-presence-prior-h29 is the adopted state (scope widened from H29 only to the adopted
  two-channel agent within the tested conditions). Scope: +1/0, G 2, C0, gate on, N2, learning off, World7 T1, W1, T3a,
  T3b at t0 150. Limits: the T3b gain depends on the loss's cast phase (F2 NOT MET; t0 100 +0.70 [+0.26, +1.14], t0 150
  +1.95 [+1.45, +2.45], t0 200 +3.82 [+3.34, +4.31]; other geometries and cast parameters untested); a loss whose second
  pass falls after the row's end is not recovered (F3); the window also acts in T1 silences (a trade); the three-channel
  form keeps its tested window 300 until a run tests it at 200. Rejected on record: keep 300; adopt 200 universally
  including the three-channel form.

### H12 (queued at the Phase 7.2 close, decision:phase7-2-gate; opened for design by decision:h12-open-design; opened by decision:h12-open; Stage 1 PASS; Stage 2 STOPPED at the bench, K0 unreadable)
- The acquisition and extinction traces persist differently (concept:h12-differential-persistence, the node queued at
  the Phase 7.2 close, reused; the number assigned there). Opened for design by decision:h12-open-design (2026-09-26,
  the owner's '권고안으로 바로 진행' after the H28 and H29 closures), the next item in the order confirmed at
  decision:h28-open point 10 and decision:h29-open point 9. No measured failure calls for it (the queue's own ranking);
  the reasons are the confirmed order, the module boundary outlook's memory core, and Stage C's values changing during
  behaviour.
- Checked against the code before design (design v1 sections 1, 2.2, 2.3): the acquisition trace is the depression of
  the reinforced compartment's weights on the odour's code units (ph4.py:58; compartment 0 punishment, 1 reward); the
  extinction trace is written by the opponent feedback driven by the behavioural valence, gated off on any step with
  external reinforcement (ph8.py:74-91); in the adopted layout it lands on the opposite valence's acquisition compartment
  (ph8.py:88-90), in the parallel layout on compartments 2 and 3 (ph8.py:85-87), which the adopted agent already allocates
  and sums (ph11.py:53, :115; ph8.py:63-65). So no per-compartment decay in the single-site layout gives sign-symmetric
  spontaneous recovery with retained acquisition, while one decay constant on the parallel pair does. In every recorded
  behaving run extinction never fires (the module gets an odour code only at a source and every source reinforces,
  ph15.py:55-61), so the H12 module is identical to the adopted one there; the adopted read-out expresses value by sign
  and rank, so a behavioural test needs a world change (reward withdrawn) and a positive competitor; decay alone gives
  recovery, not reacquisition by re-pairing (acquisition weights at the floor).
- Design v1 DRAFT doc dff68b78ea66ed47e (experiments/h12/h12_design_v1.md, sha256 75428f1a...e79e), no code.
  Recommended (c), both in order: Stage 1, a module bench on MB5(ph8.MB4) in a new src/ph36.py (ph4.py, ph8.py untouched):
  H11's two-by-two and F6 reproduced bitwise; identities; tau_ext* the smallest of {2000, 5000, 10000, 20000} keeping F1
  and F2 (predicted 5000, a 1.3-point margin on F1's extinction clause); B3 SR lower bound >= 0.20 and B4 RET >= 0.99 at
  D 5000 for both signs; single-site arms reported; stop rules (s1), (s2). Stage 2 outlined (World7 T1 geometry with
  learning on, reward withdrawn at t0 600, V masked 2400-3599, reinstated 3600-4199, a supplied competitor c +0.5;
  arms H12 module, gate only, H11 full, supplied ceiling and floor, sham; K0 readability first; K1 bar = 0.5 x (ceiling
  minus floor) after the bench; pass probabilities unmeasured). No classification-rule relaxation; a composition record to
  sign before any Stage 2 code; adoption of the parallel site only by a separate decision after both stages. Seeds:
  Stage 1 codes 20261151/20261152, bootstrap 20261153; Stage 2 bench 20261151/20261152, dev 9911/9921, eval
  2129/2243. Confirmed by the owner 2026-09-26 (decision:h12-open, '권고안으로 확정하고 H12 진행').
- Opened on design v2 FINAL doc d27ec95924fe49be1 (experiments/h12/h12_design_v2.md, sha 3d3aab80...95f1): section 12
  confirmed point by point; Stage 2 registered in section 5.5 before any run (V pre-acquired off-world by Stage B's
  training, since a naive learning arm with the competitor at +0.5 would be the sham).
- Stage 1, src/ph36.py (MB5): PASS (record:h12-bench-result). H11 reproduced line for line; tau_ext* = 5000 (tau 2000
  fails F1's extinction clause, 37.1 percent; 5000 gives 28.4); SR 0.6322 and RET 1.2279 at K 200, D 5000 for both signs
  (deterministic, exact); (I4) the H12 module equals the adopted one bitwise on H15 Run 2's streams; S1 no recovery, S2
  one-sign recovery with appetitive inversion. Close to true by construction, as the design said; the non-trivial part is
  that a tau keeps the Phase 4 battery.
- Stage 2, src/ph36b.py on the signed composition (decision:h12-stage2-composition): STOPPED at the bench, K0
  UNREADABLE (record:h12-stage2-bench-result): ceiling 0.1050 against floor 0.0125 in P4 (span +0.0925 < 0.30), P4 ties
  0.255-0.318. The value recovers in the H12 arm (0.563 against 0.317 at 4199) but W7X's P4 cannot show it in behaviour:
  after P3 at N the agent seldom meets V's plume. No bar fixed, no task seed run, nothing adopted. The single-site and
  parallel layouts separate in this input regime (a missed prediction of design 2.2). The parallel site stays held
  unproven (decision:phase7-2-gate). Closure or a Stage 2 redesign is the owner's.

## The architecture as currently adopted

Stated here so a later session does not have to reassemble it from decisions.

- **TWO FORMS, since 2026-09-26 (decision:h28-burst-tie-adopted-within-tested-conditions,
  decision:h29-window-200-adopted-within-tested-conditions).** The adopted architecture has a two-channel form and a
  three-channel distractor form; a future design must say which form it composes.
  **The two-channel form, the adopted agent: Agent17 = Agent14N2 built with N_hi 200** (src/ph35.py:104-105, a body-less
  subclass built through Agent14's constructor argument, src/ph28.py:95-97; N17 = 200 at src/ph35.py:89): everything
  stated below for Agent14N2 holds for it, with the presence window after a whiff 200 and the counter start 140 (the
  59-step prior unchanged) in place of 300 and 240. It supersedes the H26 window for this form (the H26 relaxation stays
  on record as superseded; the H29 relaxation is the adopted state). **Scope:** supplied +1/0, G 2, C0, gate on, N2
  release, learning off, World7 T1, W1, T3a, and T3b at t0 150 (T3b paired dwell +1.9525 [+1.4549, +2.4501] against
  Agent14N2; T1 DP -0.0075 [-0.0200, +0.0025]; W1, T3a identical). Limits: the T3b gain's cast-phase dependence (t0 100
  +0.70, t0 200 +3.82; other geometries and cast parameters untested); a loss whose second pass falls after the row's end
  is not recovered; the shorter window also acts in T1 silences (a trade). Agent14N2 (window 300) is the reference it
  was tested against.
  **The three-channel distractor form: Agent16 as composed in src/ph33.py** (Agent14N2's modules with three channels, the
  H27 composition rule, three presence counters at window 300 and start 240, and the H28 burst-ranked value tie, Act16,
  src/ph33.py:116-177). **Scope:** supplied +1/0 with a background distractor D at value 0, p_D 0.03, G 2, C0, gate on,
  N2, learning off, T1D and W1D (T1D DP -0.0275 against itself without D; W1D 222/400 lost against 400 for H27's agent
  and 29 without D). It keeps the window 300 (200 untested at three channels). At two channels its tie rule is inert by
  code, so it adds nothing to the two-channel form.
- **Before 2026-09-26 (kept for the lineage): the adopted agent, as composed (decision:n2-release-adopted-within-tested-conditions, 2026-09-25): Agent14N2 =
  ReleaseN2 + Agent14** (src/ph30.py:117-140; ReleaseN2 applies the H25 release (S) and (Z) only while the held odour's
  own value is non-negative, :128-132). At non-negative values it is Agent14 by code and by the Stage C bench identity
  (ph30_bench.txt line 326), so everything below that is stated for Agent14 holds for it unchanged; with a negative value
  held the release is off by rule (tested in World6 with learned values and learning on, H20 Stage C Run 2), which
  supersedes decision:release-negative-scope-on-hold. Limits: supplied +1/-1 in World7 not run with N2 (read, not
  measured); T3b; cold start. Before it, from decision:h26-adaptive-presence-adopted-within-tested-conditions:
  Agent14 = ph24.Release + ph23.Agent9 with the presence counter starting at N_hi - P = 240 (src/ph28.py:92-97;
  constants P 60, N_hi 300 at :72). It carries every module below: the upstream stage, the selection circuit with the
  H20 gain (G 2) and the H21 gate, the H25 release, the ring, the learning module (constructed, not called with a
  supplied value), and navigation with H19 (a) and the H23 filter scoped by presence. **Scope:** supplied values +1/0,
  G 2, C0, gate on, release on, learning off, the worlds tested by H26 (World7 T1, W1, T3a). It replaces Agent10 (=
  Release + Agent8) as the adopted agent within that scope; Agent10 stays the reference it was tested against. A loss
  after tracking (T3b) is not shown; negative values are excluded; learned values beyond H20 Stage B's tested
  conditions are not validated (below). The H26-scoped relaxation of the classification rule (one presence counter per odour, window 300, start 240
  as a prior) stayed in force for this counter until it was superseded for the two-channel form on 2026-09-26 (above).
- **RECORDED LIMIT, a ubiquitous distractor (record:distractor-capture-limit; decision:h27-closed, 2026-09-26):** with a
  third odour D (value 0, never reinforced, background whiffs at p_D 0.03) the adopted agent composed with three channels
  loses 0.13 of P(V) in the choice task (0.787 vs 0.920) and every row in the absent-odour world (400/400 vs 22): with the
  valued odour absent, D ties the neutral odour at value 0 in the filter's top set and steers whenever nothing or D is
  held; while V is present nothing changes. The hold's benefit under a distractor is unmeasured. A remedy, the
  burst-ranked value tie (H28, Agent16, three channels), was evaluated once and SHOWN under its registered criteria
  (record:h28-result): T1D cost 0.0275 of P(V) against itself without D, W1D 222 vs 400 lost. **ADOPTED for the
  three-channel distractor form only (decision:h28-burst-tie-adopted-within-tested-conditions, 2026-09-26);** under it
  the limit is T1D DP -0.0275 and W1D 222/400 lost against 29 without D
  (record:distractor-capture-limit-under-h28-tie); the hold's benefit under a distractor stays unmeasured. The two-channel
  adopted agent is unchanged by it.
- **Learned values reach behaviour through the adopted read-out, with no new module (decision:h20-stage-b-closed,
  2026-09-25):** a positive value learned by the agent's own learning module (H15 E2 training off-world, neutral
  first, saturating dose), read out by the module's own function into the `known` array Agent14 already reads, is used
  in behaviour within Stage B's tested conditions (World7 T1, G 2, C0, gate and release on, learning frozen in the test);
  nothing was adopted for it and the adopted agent's scope above is not widened. Learning ON during behaviour was
  evaluated once in H20 Stage C Run 2 and SHOWN under its registered criteria within its tested conditions (World6, the
  H15 Run 2 tasks, the per-step mirror, the release gated at negative holds by the Stage C-only rule (N2); M4(c) read on
  G3+; record:h20-stage-c-run2-result), and CLOSED as SHOWN (decision:h20-stage-c-run2-closed); its release rule (N2) is
  now adopted (above); H20 is closed as a whole (decision:h20-closed). Stage C Run 1 stopped at its bench
  (record:h20-stage-c-bench-result). Sub-saturating learned values are not shown; negative learned values are shown only
  in World6 with learning on, under N2.

- Upstream normalisation: Phase 2.1's Heeger stage, unchanged (ph2.Upstream).
  **WARNING for ablation:** it is also the amplifier and pulse-stretcher that brings a single
  whiff into the circuit's input range. Two controls, never to be confused: 'whole stage
  removed' shows only the integrated result when the stage is absent; 'cross-channel division
  term removed' (k = 0) keeps gain, own-channel saturation and the temporal filter and isolates
  the interaction between channels. Neither is 'no normalisation'. In H15 Run 2 the second
  reported the same values as the intact agent: two odours are almost never present together there.
- Selection and hold: the Phase 2 bistable circuit, unchanged, with the understanding from
  Phase 5 Run 2 and 7.1 that it needs an external release and that a graded substrate would not.
  With **H19 (a), ADOPTED within the tested conditions** (two-source 160x160 world, wind every
  step): while nothing is held, a whiff of an odour whose valence is not negative is handed to
  navigation. Not covered: whiffs of B while A is held, and any condition with a distractor.
  **KNOWN DEFECT, frozen:** the 40-step silence timeout fires, its reset is delivered, and it
  never releases the hold; one step of reset is integrated away. 'Recovery does not depend on
  the timeout' holds for the tested conditions only. A later fix may be a reset-control change
  or a circuit change; either way maintenance, release and distractor resistance are re-verified.
  **H25 release, ADOPTED AT +1/0 ONLY (decision:h25-release-adopted-within-tested-conditions); at NEGATIVE values
  ON HOLD (decision:release-negative-scope-on-hold):** the Release mixin of ph24.py ((S) the timeout's 10.0 drive is
  sustained while a unit is above 1.0; (Z) the silence counter is zeroed when a hold forms) ends a hold 48 steps
  after its odour's last whiff. Within its scope (+1/0, G 2, C0, T1/W1/T3a/T3b, learning off, gate on) it fixes the
  defect above; in the adopted agent (Agent10 = Release + Agent8) it is behaviour-inert at +1/0. At +1/-1 it keeps
  avoidance but costs P(V) -0.160 and lost rows +0.235 (record:release-negative-cost-limit); outside the scope the
  defect stays in force. **SUPERSEDED at negative values (decision:n2-release-adopted-within-tested-conditions,
  2026-09-25):** the adopted release is now the value-gated form (N2, src/ph30.py:117-136): at non-negative held values
  it is (S)+(Z) exactly; at a negative held value it is off, so the frozen defect is in force there (a silent negative
  hold is not ended by silence; Stage C bench (n)). The on-hold release at negatives ((N1)) is not adopted.
  **RECORDED LIMIT (record:selection-circuit-revision-via-empty-state; owner's bookkeeping decision
  2026-09-23):** under sparse task input the circuit never flips a hold from one odour to the other
  directly; every observed revision is a release to nothing held (evidence release or timeout)
  followed by re-selection from the empty state (H22 diagnosis: 0 of 319 isolated valued whiffs and 0
  of 596 at held s >= 1.8 flipped a neutral hold, 156/156 and 123/123 revisions via nothing held;
  H23 bench (b): 217/217 and 71/71). Interpretation: which odour a re-selection takes is decided in
  the empty state by arrival order and by H19 (a) / the value filter, so a mechanism that must change
  a hold acts through the empty state. Stated for sparse input only: with dense valued-only input
  (H21 bench (b), p 0.30) a neutral hold was revised in 400/400 rows, by a route not recorded.
  **Open:** whether the hold earns its place. In H15 Run 2 the agent without it left 132 of 400
  unrecovered against 21 of 400, with a rewarding dwell of 17.3 against 23.0; no distractor
  condition exists, so its distractor resistance is unverified. H27 added one (a third odour D, value 0, background whiffs
  at p_D 0.03) and STOPPED at its bench (record:h27-bench-result): with D the adopted agent composed with three channels
  lost every W1 row and 0.13 of T1 P(V), and the arm whose navigation does not read the hold lost the same, so the
  question stays open. H27 was closed with the distractor condition recorded as a limit (decision:h27-closed,
  record:distractor-capture-limit). H28's evaluation (record:h28-result) reported M6 +0.0000 again: with the burst-ranked
  tie the hold-not-read arm loses the same 222 W1D rows, so the question stays open.
  **Tested in H20 Stage A, NOT adopted:** a gain (1 + G*max(v, 0)) on the upstream output
  entering the circuit and its evidence release, for odours with a positive value. Measured: a
  single whiff of the gained channel holds at G >= 0.5 (an ungained single whiff reaches 0.756 of
  threshold); the first hold is carried by the circuit-input entry alone; in the moving agent at
  G 2 the gain moved the first hold to the valued odour in 277 of 400 rows against 200 without
  it, 17 steps earlier, and revised a held neutral selection in 238 of 400 through the evidence
  release; the registered avoidance-maintenance criteria passed with it (no flee-command
  violation; dwell at the punisher +0.507 step, within the allowed +1; reaching the valued source
  first fell by 3.8 points). It did NOT change which source was reached first. Input range at
  G 2: y' up to 5.34, the clip reached on at most 0.01 percent of steps in the task.
  **H21 gate, ADOPTED WITHIN THE TESTED CONDITIONS ONLY (decision:h21-gate-adopted-within-tested-conditions;
  the H21 verdict is NOT shown, decision:h21-closed):** a gate that zeroes a lower-valued non-negative
  odour's response into the circuit and the evidence release while a higher-valued odour is held
  (Agent6; the Run 2 agent at equal values, with nothing held and at +1/-1, bitwise). **Scope:**
  supplied value, values +1/0, G 2, geometry C0, the dwell-majority measure, learning off. **Not
  validated:** learning, the integrated environment, other G, other geometries, other values, the
  first source reached, the timeout, any distractor condition. Measured: a
  valued hold is never lost with it (0 of 280 in the task, 400/400 on the bench) and converts into
  the majority source at 0.971; P(V) 0.750 against 0.570 without it on the same rows; the first
  selection is unchanged (the gate acts only once a hold exists); no lost rows added. Its limit is
  upstream of it: 120 of 400 rows first hold the neutral odour and 53 are revised.
  **Measured in the link check:** in the adopted agent the circuit's first hold forms near the
  reach (step 29 to 34 against a first approach at 31 to 38) and agrees with the source reached
  in 0.87 to 0.89 by position.
- Heading memory: RingExact at tau 1.0, sigma 0.5, vgain equal to tau, n=16, other parameters
  Phase 3's (decision:h14-adopt-tau1), wind coupled in at amplitude 6.0, FED THE ROTATION MADE
  (decision:heading-input-rotation-made). With the wind sensed every step its reported values
  are similar to exact heading's (H16 Run 2, H15 Run 2); equivalence was not tested, and that
  condition does not test whether heading memory is needed.
  **WARNING:** as a MEMORY it is not good enough to navigate on. With the cue absent 50 steps at
  a time it leaks agents to a median score of 0.0 where a perfect integrator keeps 24.0
  (concept:ring-leaks-under-cue-loss). The cause is not known; H18.
- Learning: H8 v2 with the extinction GATE, per decision:phase7-2-gate. Parallel site not adopted.
  **Read at the H12 design (2026-09-26, design v1 doc dff68b78ea66ed47e; no run):** the module receives an odour code
  only at a source and every source reinforces (ph15.py:55-61), so with the gate on extinction has never fired in any
  recorded behaving run; the adopted layout writes extinction on the opposite valence's acquisition compartment
  (ph8.py:88-90); no weight decays at any site. H12 tested the parallel site with a decaying extinction pair (MB5,
  src/ph36.py; tau_ext* 5000): Stage 1 PASS at the module level (record:h12-bench-result; inert on H15 Run 2's streams
  by (I4)), Stage 2 STOPPED at its bench, unreadable (record:h12-stage2-bench-result); nothing is adopted, the module
  above is unchanged, and the parallel site stays held unproven. Measured in H12 Stage 2: the single-site and parallel
  layouts are not equivalent when reward and code arrive together and then the code alone (the reward trace's
  potentiation can drive V below 0, where the single-site feedback masks it); design 2.2's identity holds for H11's
  forward-pairing protocols only.
  **Learning loop, from H15 Run 2:** every agent's learning state is updated exactly once per
  world step from its own position. Run 1's loop advanced the module only when some agent stood
  at a source, which coupled the agents (displacing one agent changed the others; shown by
  self-check 4). Run 1's numbers are kept as the result of that loop.
  **Measured in Run 2:** a negative value of -0.89 from one natural visit of about 7 steps. On
  the short repeated-visit input generated by the adopted agent, the gate contributed to keeping
  the memory (replay without the gate: 0.049 of the gated value), and the difference in the
  reward memory did not appear in the current behavioural structure; a similar bench number for
  200 continuous steps does not establish a shared mechanism. Two odours trained back to back
  interfere through the traces (+-2.0 second-trained, +-0.5 first-trained) unless the traces are
  allowed to decay in between.
  **Note (H15 Run 2's agent; for the adopted agent see 'Learned values reach behaviour' above, H20 Stage B):** in the
  agent a POSITIVE valence has no behavioural effect. Two-sided learning can be
  read in the weights; only its negative side can show in behaviour. H20 Stage A tested one
  pathway for it: it reaches selection, not the source reached first.
- Navigation: surge-and-cast on a wind reference with the RETURN cast (triangle wave), adopted
  by decision:h16-close-limited-adoption. **Scope:** environments with little boundary influence
  and heading information on every step; tracking a plume already entered and reacquiring it
  after loss. **Not validated:** finding a plume from an odour-free start (about half, H17; now with a measured
  consequence: after the release ends a negative hold 20-27 units outside the plumes no whiff follows in 131/131,
  record:release-negative-cost-limit; H17's search, closed NOT shown by decision:h17-closed, was not adopted, so the
  limit stays);
  navigation under loss of the heading cue; any arena whose walls are inside the rule's loop
  (in 40x40 it equals a random walk, concept:h15-arena-occupancy-floor). The saturating cast of
  Phase 7.3 is superseded: it leaves 94 to 98 percent of agents unrecovered over 5400 steps.
  **Found in H20 Stage A:** the adopted agent starts every row with the same initial cast side
  (cast_sign +1); in a symmetric two-source start this alone decided which source was reached
  (94 percent to one side); the H20 task harness draws it per row, the agent is unchanged.
  **Measured in the link check (value excluded, the tracked odour fixed by intervention):** the
  rule expresses the tracked odour's identity. The movement command differs from the first
  whiff that arrives on one channel only, in every row; over 600 steps the agent stays at the
  tracked source in 0.95 to 0.97 of rows in three geometries. What it does NOT do in the H20
  geometry is express the identity in the FIRST source reached: with two plumes overlapping at
  the start, the crosswind position at the point where the cones separate is at chance (0.49 to
  0.53) and the first reach is the same source whatever is tracked (0.93); with the separated
  stretch lengthened from 14 to 18 units the first reach follows the identity in 0.74. A
  first-reach measure in a two-source task therefore needs a geometry checked by a known-answer
  arm (the identity fixed) before it is registered. Whether a crosswind term is needed is not
  tested; such a term would change what the agent knows.
  **H23 value filter, ADOPTED WITHIN THE TESTED CONDITIONS ONLY
  (decision:h23-filter-adopted-within-tested-conditions; the H23 verdict is shown, decision:h23-closed):**
  the upwind surge follows the top-valued non-negative odour in the agent's own read-out; while a
  top-valued or a negative odour is held its whiffs steer as before, otherwise only a top-valued
  odour's whiffs steer (Agent8, ph21.py; bitwise Agent6 at 0/0, +1/+1, +1/-1 and with the valued
  odour held). **Scope:** supplied value, values +1/0, G 2, geometry C0, the dwell-majority measure,
  learning off, the H21 gate on. **Not validated:** a world where the higher-valued odour is absent
  (the agent would never surge on the odour present; the absent-odour check measures it), +1/+0.5,
  learned values, other G, other geometries, the timeout. Accepted consequence: with unequal values
  navigation is value-driven and selection does not steer; selection keeps equal-value arbitration,
  the flee, and the hold state the H21 gate protects.
  **H26 presence scope, ADOPTED WITHIN THE TESTED CONDITIONS ONLY
  (decision:h26-adaptive-presence-adopted-within-tested-conditions; the H26 verdict is shown, decision:h26-closed):**
  v_max of the H23 filter is taken over the odours present, present_k = (c_k < 300) or k held, with one counter c_k per
  odour (steps since last sensed, ph23.py:83-85) starting at 240 (ph28.py:97): an odour never sensed is present on steps
  0-58 (a PRIOR, not evidence), and for 300 steps after any whiff. In W1 it removes the filter's absent-odour cost
  (dwell 23.8 against Agent6 24.8 and Agent10 12.3); in T1 it keeps H23's result (0.927, DP vs Agent10 -0.0075); after a
  constructed loss from step 0 it opens at step 59 (R 1.04). **Scope:** as the adopted agent above. **Not validated:** a
  loss after tracking (T3b: a fixed 300-step blind window, 4.412 against 5.772 at N 60); negative values; learned values;
  other P or N_hi. Measured cost: W1 lost rows against the unfiltered agent +0.0475 (the price of the 59-step prior);
  T1 rows without a valued whiff by step 58 (20 of 400) carry the residual (k 5).
  **Window SUPERSEDED for the two-channel form (decision:h29-window-200-adopted-within-tested-conditions, 2026-09-26):**
  present_k = (c_k < 200) or k held, the counter starting at 140 (the prior P 60 unchanged: a never-sensed odour is present
  on steps 0-58), Agent17; the H26 relaxation stays on record as superseded there. The three-channel distractor form
  keeps window 300 and start 240 as tested.

## Standing rules
- One hypothesis active at a time. Adoption and every gate pass are decided by the project owner, not by the assistant.
- Success criteria are stored in the graph before the run.
- A new idea that appears mid-phase is recorded as a candidate and queued; it does not change the order without a decision node.
- Failed runs and rejected designs stay on record.
- Each phase ends with a short phase report document and an episode.
- Added in Phase 0 and in force from the Phase 0 gate: every script that produces a recorded number is stored in the graph in full, with its sha256, in the same session.
- Added at the Phase 5 close: a gate criterion that reads a score must state both a floor and a
  ceiling. Phase 5's B1 required the task to discriminate and forgot to forbid saturation, which
  made three of four A1 comparisons unreadable.
- Added at the Phase 6 close: an ablation must be checked for being a broken instrument before
  its verdict is read. Two of Phase 6's rows were first scored on a divergent integrator and on
  a threshold that flagged the reference design itself; one of them flipped a conclusion.
- Added at the Phase 7.2 close: a criterion that stands in for a behavioural claim must be
  behavioural. Phase 7.2's F3 read weights, passed, and was still the wrong test; the probe that
  asked the question behaviourally failed in every cell.
- Added at the Phase 7.3 close: a criterion that compares against a baseline must check the
  baseline is not pinned at zero. G4's percentage gap was 100 percent by construction in both
  conditions because the rule it compared against scored exactly 0.0 in each.
- Added at the H14 close: an angular gain must be measured on per-step displacement accumulated
  without folding. A single circdiff folds past half a turn and reads a correct rotation as a
  reversal. This one produced a false finding that stood on the record for a phase.
- Added at the H14 close: when a stored bound is relaxed, the change is a signed decision naming
  the old bound, the new bound, and the already-accepted measurement the new bound is anchored
  to. The stored criteria are never edited; the hypothesis keeps its verdict under them.
  One such relaxation of the classification rule exists, scoped to H24 only: a per-odour presence counter,
  N 60, starting ON as a prior (decision:classification-rule-relaxed-presence-counter) (lapsed with H24's closure; the decision stays on record). A second,
  scoped to H17 only: ONE counter q, steps since the last whiff of any odour
  (decision:classification-rule-relaxed-any-odour-silence-counter-h17), re-signed in form for H17 and H17 Run 2
  (decision:classification-rule-relaxed-any-odour-silence-counter-h17-run2); both lapsed with H17's closure
  (decision:h17-closed) and stay on record, as does the lapsed H24 Run 2 re-sign
  (decision:classification-rule-relaxed-presence-counter-run2). A new one, scoped to H26 only (one presence counter per
  odour, window 300, starting at 240 as a prior), was signed by the owner on 2026-09-24
  (decision:classification-rule-relaxed-presence-prior-h26); H26 was closed as shown and its counter adopted within the tested conditions (decision:h26-closed, decision:h26-adaptive-presence-adopted-within-tested-conditions, 2026-09-25), so this relaxation STAYS IN FORCE for the adopted agent's counter (Agent14), as part of the adopted state; any wider use (another counter, window or agent) is a new decision. The classification rule itself is unchanged elsewhere. A composition rule, not a relaxation, was signed in the same H14 format for H20 Stage C only (decision:release-value-gated-stage-c: the H25 release not applied while the held odour's own value is negative); it adopts nothing, and decision:release-negative-scope-on-hold stays in force outside Stage C. For H20 Stage C Run 2 that rule was re-signed in form, content unchanged, scope Stage C Run 1 and Run 2 (decision:release-value-gated-stage-c-run2), and one bar was re-signed in H14 format for Run 2 only: M4(c)'s readability read on G3+ with G3+ at least 50 (decision:h20-stage-c-m4c-readability-resigned-run2); the stored Run 1 criteria are not edited. On 2026-09-25 Stage C Run 2 was closed as shown (decision:h20-stage-c-run2-closed) and the (N2) rule was ADOPTED as the adopted agent's release rule (decision:n2-release-adopted-within-tested-conditions), which supersedes decision:release-negative-scope-on-hold; the Run 2-only M4(c) re-sign lapsed with the closure. For H27 two records were signed in the same format on 2026-09-25, H27 only: an evidence-release composition rule at N channels (decision:evidence-release-composition-rule-h27) and an in-form re-sign of the H26 relaxation for a third counter (decision:classification-rule-relaxed-presence-prior-h27); H27 stopped at its bench (record:h27-bench-result), and both stay on record, scoped to H27. H27 was closed on 2026-09-26 (decision:h27-closed): both lapse with the closure and stay on record; the composition rule stays available as a recorded composition for any future N = 3 design, by a new decision (a re-sign in form). For H28 three records were signed on 2026-09-26, H28 only (decision:h28-open): a new H28-scoped relaxation (per odour the step of its second most recent whiff and of its last burst, read only to rank odours tied at the top value; decision:classification-rule-relaxed-burst-record-h28) and the two H27 records re-signed in form (decision:evidence-release-composition-rule-h28, decision:classification-rule-relaxed-presence-prior-h28); H28 was evaluated once and SHOWN (record:h28-result); the three stay scoped to H28 until the owner's closure decides otherwise. For H29 one record was signed on 2026-09-26, H29 only (decision:h29-open): the H26 presence relaxation re-signed in H14 format with the window 200 and the start 140, the prior unchanged (decision:classification-rule-relaxed-presence-prior-h29); the adopted counter (300, start 240) is unchanged; H29 was evaluated once and SHOWN (record:h29-result); the record stays scoped to H29 until the owner's closure decides otherwise. On 2026-09-26 the owner closed both as SHOWN and adopted them within their tested conditions ('권고안으로 바로 진행', gloss 'proceed right away with the recommended options'): for the TWO-CHANNEL form the H26 relaxation (window 300, start 240) is SUPERSEDED by the H29 relaxation (window 200, start 140, the prior unchanged; decision:h29-window-200-adopted-within-tested-conditions), which is now the adopted state for Agent17 and stays in force as such (the H26 record stays on record as superseded); for the THREE-CHANNEL distractor form the H28 burst-record relaxation, the H27 three-counter presence relaxation and the H27 composition rule (as re-signed for H28) are adopted state, re-signed in form by decision:h28-burst-tie-adopted-within-tested-conditions with scope 'the adopted three-channel agent'; the two-channel form does not carry them. Any wider use of any of these (another window, another N, another agent) is a new decision. H12 (opened by decision:h12-open) proposed no relaxation of the classification rule (its change is inside the learning module); its Stage 2 composition was signed in H14 format as a composition record, H12 Stage 2 only (decision:h12-stage2-composition), and lapses with H12's closure unless the owner decides otherwise.
- Added after H15 Run 1: task validity has THREE clauses, not two. The probes must discriminate,
  no arm may saturate, and the intact agent (or a known-answer probe) must itself clear the
  floor in the window where the gate is read. H15's probes spanned 0.3 to 600 and every agent
  arm sat at exactly zero.
- Added after H15 Run 1: nothing is adopted for agent use until it has been run inside an agent
  at the agent's own noise. The H14 adoption check ran on a bench at noise 0.01 and its in-agent
  comparison used a different setting from the one adopted.
- Added after H15 Run 1: a behaving system is scored over a horizon long enough to expose
  absorbing states, with a location measure reported beside the score. One fresh episode per arm
  hid the fact that the navigation rule loses 92 percent of its agents for good.
- Added after H15 Run 1: a population median over a learned quantity is stated over the agents
  that had the experience, with their count, so that "did not learn" and "was never there"
  cannot be confused.
- Set by the owner at the H16 opening: development seeds and evaluation seeds are separate.
  Development runs exist to find operation errors. The evaluation is run once, and any change
  after its table is a new Run with its own record.
- Added after H16 Run 1: a score that counts presence in a region must be read against a random
  walk's occupancy of that region in that arena, and a scheme that cancels (+1 and -1) must be
  checked for hiding that floor. In a 40x40 arena a random walk sits at the source 10 steps in
  600; H15's cancelling score showed it as 0.3.
- Added after H16 Run 1: a test of heading memory under cue loss must run where unobserved
  heading changes do not dominate (record:h16-k5b-confounded-by-walls).
- Set by the owner at the H16 Run 2 opening: a rerun in a changed environment leaves the earlier
  verdict standing and states the scope of its own. The environment is pre-registered as
  geometry relative to the source (wall distances, plume extent, start distribution), not as a
  size, together with what was kept from the earlier run. Boundary exposure (contacts, near-wall
  dwell) is reported beside the score. Results are worded as "unrecovered within the observation
  time", not as the removal of an absorbing state.
- Added after H16 Run 2: a memory test is read only after a known-answer arm reproduces the
  no-loss arm. The perfect integrator reaching the source in 85.5 percent of agents exposed a
  cold start in my dropout schedule; after the fix it matched exact heading to the digit.
- Set by the owner at the H16 close: a hypothesis verdict and an adoption are separate records.
  An adoption states its scope and what it does NOT validate, and a success inside that scope
  is not read as evidence for anything outside it.
- Added at the H16 close: a figure measured in one starting state is not carried to another.
  I wrote that a second source would be found "half the time" from the cold-start figure; it was
  93 percent for agents driven off the first source and under 20 percent for agents with no
  reason to leave (record:correction-second-source-search-rate-unmeasured).
- Added at the H16 close: a draft decision is not the owner's until the owner says so. When a
  text arrives marked for review or for forwarding, the assistant asks before recording it.
- Added after the two-source check, wording corrected by the owner's review: in a design that
  yields many exactly tied pairs, a win-rate bar over all agents does not measure the effect it
  was meant to measure. A valence of +1 changes nothing in the agent and 42 percent of pairs
  were exact ties. The tie share is a result of the run, not a bound shown beforehand, so the
  bar is not called unreachable (record:correction-m3-wording-and-scope).
- Set by the owner after the two-source check: when a criterion is amended before the
  evaluation, the original verdict stands and the amended reading is reported as a separate
  result with the narrower question it answers stated.
- Set by the owner after the two-source check: a difference between two runs that differ in
  more than one way is not attributed to anything until the arms are compared in the same
  world, initial states and seeds, with the events in between logged. A diagnosis is not used
  to claim that a fix works; the fix is its own hypothesis with its own criteria.
- Set by the owner after the two-source check: an entry criterion must not lean on a value
  sitting on its threshold. Give the unrounded value, the counts and the per-group results, and
  fix in advance the group the criterion applies to.
- Set by the owner at the H19 opening: a fix is tested as the smallest change with its
  boundaries stated, against the existing system and a control without the component, on new
  seeds, with numbers registered for the allowed gap to the reference and the improvement
  required. A calibrated control is defined by an independent input and response test, never
  tuned to the task score, and is reported separately from the original ablation.
- Added after H19: a condition that floors every arm on development seeds is declared
  unreadable and is NOT retuned until an arm clears the floor; redesigning it is a separate
  step. And a distractor must be irrelevant: with two odour channels I made the background the
  punished odour, which is a punisher everywhere.
- Set by the owner at the H19 adoption: an explanation of WHY a result came out is labelled a
  mechanism interpretation unless the mechanism itself was measured. Observed differences are
  reported as they are, and a measure that happens to look favourable is never picked afterwards
  to stand in for a registered criterion. A control is named for what it removes; one that keeps
  part of a computation is not called its absence.
- Set by the owner at the H19 adoption: for an integrated run the specification is fixed before
  any code, as ONE standalone document whose version and hash the code and the report cite;
  earlier drafts are kept as history.
- Set by the owner in the Run 2 specification reviews: a quantity quoted to justify a design
  choice is checked for what it measures (I justified a 30-step training with 'one visit
  delivers 20-28 steps'; that was dwell per block, a visit delivers 6-9). Each criterion fixes
  ONE statistic, never replaced afterwards, even when ties make it unreadable. Uncertainty is
  handled by a stated interval rule with PASS / FAIL / INCONCLUSIVE, the same level at the first
  evaluation and at the one permitted extension, with no claim of simultaneous coverage over
  several criteria; FAIL is final; an extension is fixed in advance, run once, and is not
  'repeat until it passes'. 'Baseline at the floor' is defined per comparison: a zero baseline
  is fine, a ratio over it or two floored groups are not. An auxiliary arm without enough of
  the relevant exposure reads 'not discriminated in this run', never 'no effect', and never
  changes a main criterion afterwards.
- Set by the owner in the Run 2 specification reviews: the sampling unit and the grounds for
  independence are stated. A check that one row does not interfere with another shows absence of
  interference in the code; independence of the sample rests on how random numbers are generated
  and on the code confirmation that no state is shared, recorded beside it. What is fixed across
  runs is said to be fixed: the per-row odour codes do not vary with the seed, so results are
  conditional on that set and new seeds do not test generalisation to new codes.
- Set by the owner at the Run 2 opening: an implementation error (the code does not do what the
  specification says) and a change to a hypothesis or criterion are recorded separately.
- Added after H15 Run 2: a protocol sentence about timing is checked against the traces of the
  module it drives before it is registered ('no gap' between two trainings let the first trace
  act on the second). And before a matched-pair win rate is registered, say where ties can come
  from: arms identical by construction, or both arms reaching the same floor.
- Set by the owner at the H15 Run 2 close: a registered rule is not waived for one result and an
  undecided verdict is not rewritten as a pass; what was observed is recorded separately and
  called what it is. An outcome made unreadable by a registered limit is distinguished from
  absence of evidence (146 of 199 pairs improved, 53 tied). A rerun whose only purpose is a pass
  label is not prioritised. Deciding to move on to the next research is an operational decision,
  separate from a statistical verdict. In reports: a group is not described by a claim its own
  tied pairs contradict; similar reported values are not tested equivalence; an outcome is
  labelled exactly as the registered rule gives it, after checking the unrounded value; and a
  similar number on a bench does not establish a shared mechanism.
- Set by the owner in the H20 design reviews: a behavioural hypothesis about value is narrowed
  to a controlled choice task before it is run, with the behavioural pathway named and justified,
  the checks for a supplied value, a learned value and integration kept separate, and only the
  first pre-registered. A proportion compared across arms uses every assigned row as its
  denominator, with the other outcome classes reported beside it and the required success counts
  computed before the run; an interval that contains the chance value is not evidence of
  symmetry, which is read as the whole interval inside a pre-set tolerance; a condition whose
  formula is identical by construction is an implementation identity check, not an arm; a
  parameter fixed on a bench has its input, initial state, noise, seeds and every candidate on
  record, with a rule for no candidate passing; a balanced design separates preferences without
  removing them, so cells are reported; a rule that was never exercised in a run reads 'no
  violation, no opportunity to verify', and is verified in a constructed state instead; an
  interval reading has three outcomes, never a one-sided conclusion from a missed bar; and a
  diagnostic that narrows where a failure lies does not by itself name its cause.
- Set by the owner after the H20 G bench: a bench that finds no eligible candidate keeps its bar
  and its verdict; the bar is not lowered to the numbers and the pathway is not changed until
  a diagnosis has separated what the change actually does (every place the changed signal
  enters) from what the input allows (the history before the measured event). 'One line' is not
  one computational effect. An end-state proportion is read over every row, the unselected
  included. A bench bar's relation to task success is not known until the task is run, in either
  direction. A ceiling found on one input for tested parameter values is stated for those values
  and that input, not 'for any'. A parameter may then be fixed post hoc by a SEPARATE execution
  decision that says it is not a bench pass, with the reason and the fact of post-hoc choice on
  record, and nothing adjusted after the table. Added by the assistant from the same diagnosis:
  a bench bar for a mechanism is checked against the ceiling the registered input allows that
  mechanism BEFORE it is registered (here the arrival order of sparse whiffs bounded the first
  hold at 0.81 under a bar of 0.85).
- Added at the H20 Stage A evaluation: a symmetric choice task registers the adopted agent's
  initial state as part of the task, and a validity check on development seeds reads it before
  the evaluation. The agent's fixed initial cast side alone decided the first source reached
  (94 percent to one side); the crossing hid it in the pooled count and showed it in the cells.
  And a selection measure and a reach measure are two measures: an agent can select one odour
  and reach the other; the row-for-row identity of the reach between the arm with the pathway
  and the arm without it is the reading, and the segments (first selection, maintenance and
  revision, navigation) locate the failure without naming its cause.
- Set by the owner at the H20 Stage A close: a multi-part criterion whose rule names no
  aggregate is INCONCLUSIVE when no part fails and one is inconclusive, never FAIL; a printout's
  pass/not-pass summary is not the registered label. 'Avoidance intact' is not what a
  maintenance criterion shows; the report says which registered criteria passed and states the
  measured changes beside them (dwell did increase, reaching the valued source fell). A measured
  mismatch between selection and behaviour does not establish which part of the rule is
  responsible; the account is verified by intervening on the link (fixing the tracked identity)
  before any rule is changed. A geometry comparison uses a few pre-defined conditions with the
  present one as the reference, states each condition's initial sensory accessibility and source
  distance, keeps every start able to sense both odours, and never picks a favourable layout
  after the results. A navigation term that uses the source's or the axis's position changes
  what the agent knows, not only what it does; before any such term, it is classified as an
  estimate from sensory history or as a diagnostic ground-truth direction, and the absence of a
  term is not by itself evidence that it is needed.
- Added at the link check: a pre-registered geometry is checked against every hard bound of the
  world (the cone length LMAX, the half-width at the start) before registration, not only against
  the exponential whiff rate; C2 as registered lay beyond the cone length and the self-check
  caught it before any run. And a behavioural measure registered for a task (here the first
  source reached) is calibrated by a known-answer arm in which the quantity the hypothesis is
  about (here the tracked identity) is fixed by intervention: in the H20 geometry a perfect
  selection reaches its source first in about half the rows, so the bar the task carried could
  not have been met by any selection mechanism. A diagnostic reading with three outcomes is
  read on the unrounded bound (C2's 0.697 against 0.70 is 'partial', not 'expressed').
- Added by the assistant at the H20 Run 2 diagnosis: a release flag that coincides with a hold
  ending is not shown to be what ends it; the circuit's own dynamics are read and measured first
  (the timeout ended 5 of 3998 firings; a hold at its fixed point survives a one-step reset), and a
  rule meant to maintain a hold acts on what actually ends it, not on the flag. And a first hold's
  conversion into behaviour is compared on the SAME rows across arms before a mechanism is blamed:
  the rows both arms selected converted identically, and the whole loss lay in the rows the gain
  added.
- Added at the H21 design review and evaluation: a seed proposed in a design is checked against the
  whole record (every script and output, and the graph) before the draft goes to the owner, not
  after (v1 proposed 1720, used by the two-source check). And when a paired bar is placed at the
  lower edge of the registered prediction range, the design states the interval half-width expected
  at n (here about 0.04), so that a point estimate inside the range leaving the bar inside the
  interval is foreseen, not discovered.
- Housekeeping convention, set by the owner's bookkeeping decision of 2026-09-23
  (decision:code-citation-convention): records cite code by `code` (repo-relative path + sha256) and
  `source_doc` (the stored source's doc id); props.subject_path is not used.
- Housekeeping convention, set by the owner on 2026-09-23 under '의견 그대로' (decision:master-plan-source-of-truth,
  reversible): the git-tracked master_plan.md is the master plan's source of truth; graph doc
  d1867092e4263d16c is a mirror re-put from it after every edit; no pre-edit byte comparison with the
  store; the store's content_hash after each put must equal the file's sha256.
- Set by the owner on 2026-09-25 (point 3 of '1. shown으로 종결 및 n2는 범위 권고안으로 적용 2. 미입증안 해결책이 없나? 3,4
  권고안으로 진행', the recommended option; decision:seed-scan-exclusion-ph31-eval): an incidental seed match in a recorded
  output is excluded as a (file, number) PAIR, never by excluding the file, and the output is not edited. In force: the
  pair (experiments/h20/ph31_eval.txt, 2115), a whiff count at line 175 equal to Stage C Run 1's E1 evaluation agent seed.
  Every future design's section 9 and every future script header with a seed scan lists it by reference (file name plus
  decision id) without writing the number; ph30.py and ph31.py are not edited, so ph30's self-check lists ph31_eval.txt and
  ph31's demo check 6 would fail on re-run, both known.

## A standing caution about bench gates

Six times now something has passed its own gate and then failed in a behaving agent, in a way
the bench could not have seen.

- Phase 5 Run 2: the Select-and-Hold reset fired zero times in 400 steps.
- Phase 7.2: the parallel extinction site preserved a trace nothing could act on.
- Phase 7.3 and H14: the ring attractor under-rotated badly at the angular velocities an agent
  actually uses; the bench had only ever driven it to 0.45 degrees per step.
- H14 and H15: the ring adopted to fix that was itself checked only at bench noise, and loses
  the heading for most agents at the agent's noise.
- Phase 7.3 and H15: surge-and-cast passed on one fresh episode per arm and absorbs 92 percent
  of its agents at the downwind wall over a persistent horizon.
- Phase 2, Phase 5 Run 2 and the two-source check: Select-and-Hold passed its gates on sustained
  input, and its repaired reset was seen to fire; fed single-step whiffs in a behaving agent it
  drops a tenth of them, its timeout releases nothing, and the agent without it loses no one.

A phase gate establishes that a mechanism has a property on a bench. It does not establish that
the property is reachable, or usable, or in range, or stable over time, in the agent the project
is building. Writing the caution did not prevent the later instances; the rules added after
H15 Run 1 are the attempt to make it operational. H16 is the first time the stored criteria
stopped one of these before adoption, and the diagnosis after the two-source check is the first
time one was caught before an integrated run rather than after it. The same holds for the
experiment's own machinery: Run 1's learning loop coupled its agents for a whole phase before a
score-free check showed it. H20 adds two cases: a bench bar set above what its input allowed
stopped a task that had not been shown to need that bar; and the gain that moved selection on
the bench and in the agent did not move the source reached first, because in that geometry the
first reach cannot express any selection, which a known-answer arm for the measure would have
shown before the task was registered. The link check is that arm, run afterwards.

Observations from H22, recorded as observations (the owner has made no rule of them): the bench's
constructed state did not match the task's state (the agent placed at the neutral source gave 0.328
at 600 steps; on the task-like start, the neutral axis 20 downwind with a neutral hold, the rule's
effect was 0.083 against 0.085 without it); the bench window (300 steps) did not match the task
horizon (600); and the bench prediction (0.60 to 0.95) was borrowed from the known-answer arm, whose
navigation law differed from the rule's, instead of being computed from measured rates (release ->
re-take, cone-edge whiff density, loop period). The H23 design applies all three
(decision:h23-open-design).

H24 adds a lesson (decision:h24-closed): a design assumption about circuit dynamics must cite a recorded bench
or a code line, and a recorded defect must be treated as in force until a decision fixes it (H24's design
presumed the silence timeout ends a valued hold; record:silence-timeout-chain-result had recorded that it does not).

The avoidance check adds one (record:r3-negative-release-diagnosis-result): a base result may rest on an artefact
(here the wall reflex carrying the base's negative hold back across the plumes), so a fix that removes the artefact
can look like a regression.

H27 adds two (decision:h27-closed): a prediction anchored on a narrower definition than the one registered is not a
prediction for the registered quantity (the (m) count was predicted at 15-20 from H26's at-risk set and measured at 122
under H27's own definition, 21 under H26's); and a stated risk that names one entry point is not a bound (the release's
48-step end was named; the diagnosis found several entries, and the release-off arm lost the same rows). H28's design
guards both (its section 13).

## Why this order
Phase 0 makes later comparison trustworthy. Phase 1 comes before further modelling because it can redirect Phases 2 to 4 and is the project's stated purpose. Phase 2 precedes 3 and 4 because both will reuse the Select-and-Hold circuit and inherit its defects. Phase 3 precedes 4 because heading memory needs no learning, while the integrated agent needs both. Phases 5 and 6 need everything before them.

## Awaiting the owner

- **H12: close, or redesign Stage 2** (decision:h12-open; record:h12-bench-result; record:h12-stage2-bench-result;
  concept:h12-differential-persistence). Stage 1 PASSED at the module level (tau_ext* 5000; SR 0.6322 and RET 1.2279 for
  both signs at D 5000; the Phase 4 battery kept). Stage 2 STOPPED at its bench, UNREADABLE as designed: in W7X's P4 the
  supplied ceiling (V +1) reaches P(V) 0.1050 against the floor's 0.0125 (span +0.0925 < 0.30) and ties are 0.255-0.318
  (> 0.20), because an agent that spent P3 at N seldom meets V's plume again. By the registered rule a redesign, not a
  retune. Options for the owner: (a) close H12 as shown at the module level only, the parallel site staying held unproven
  (no behavioural claim); (b) open a Stage 2 redesign (a world in which the agent meets V again after the retention
  interval, for example a reinstatement from V's plume or a start near both sources, with its own readability check
  first); (c) defer H12 and take H10 (the confirmed order: H10, H18, H17). Nothing adopted; no task seed was used.

## Queued candidates, none started

The order does not change without a decision node. H21 is closed (decision:h21-closed); H22 is closed
(decision:h22-closed); H23 is closed as shown (decision:h23-closed). Next, in this order
(decision:next-absent-odour-check-then-stage-b): the absent-odour check is complete
(record:absent-odour-check-result: reach kept, the cost in dwell and drift); H24 (filter scope, option v) closed
as NOT shown (decision:h24-closed); H25, the silence-timeout fix, closed as shown (decision:h25-closed), the release
adopted at +1/0 and on hold at negative values (decision:release-negative-scope-on-hold). The order from here is
fixed by the owner (decision:priority-h24run2-h17-stageb): H24 Run 2, the (v-p) presence-counter re-attempt on
Agent10 (decision:h24-run2-open; stopped at the bench by its stop rule, record:h24-run2-bench-result), is closed as
NOT shown (decision:h24-run2-closed; nothing adopted, the Run 2 relaxation lapsed); H17 opened on design v2 FINAL
(decision:h17-open; doc d83a917ea4152b4a7) and STOPPED at the bench, no candidate on part (d)
(record:h17-bench-result); H17 Run 2 opened on design v2 FINAL (decision:h17-run2-open; doc d73c77ebd99d50d86) and
STOPPED at the bench by its (h2) stop rule (record:h17-run2-bench-result); H17 is CLOSED as NOT shown
(decision:h17-closed, 2026-09-24; nothing adopted, the relaxations lapsed, cold-start search a recorded limit); adaptive
presence, numbered H26, was opened on design v2 FINAL (decision:h26-open) and evaluated once: SHOWN under its
registered criteria (record:h26-result; report doc d8163e16317b251eb), and CLOSED as SHOWN with its counter and Agent14 adopted within the tested conditions (decision:h26-closed, decision:h26-adaptive-presence-adopted-within-tested-conditions, 2026-09-25); H20 Stage B was opened on design v2 FINAL (decision:h20-stage-b-open; doc d3f2ce9707790cd87), evaluated once and CLOSED as SHOWN (record:h20-stage-b-result; report doc d66ad8dea08c92116; decision:h20-stage-b-closed, 2026-09-25; nothing new adopted); H20 Stage C (integration, learning on in the H15 Run 2 world) was opened on design v2 FINAL (decision:h20-stage-c-open; doc d27e6dfe2e2c16183) and STOPPED at the bench by its (hR) stop rule (record:h20-stage-c-bench-result); after the post-bench diagnosis the owner opened Stage C Run 2 for design (decision:h20-stage-c-run2-open-design) and, by the standing instruction to follow the recommended options, on design v2 FINAL (decision:h20-stage-c-run2-open; doc d007990ab333e7194); Stage C Run 2 was evaluated once and SHOWN under its registered criteria (record:h20-stage-c-run2-result; report doc de5963e5a73875a97), and CLOSED as SHOWN with N2 adopted and H20 closed as a whole (decision:h20-stage-c-run2-closed, decision:n2-release-adopted-within-tested-conditions, decision:h20-closed, 2026-09-25). H27, the distractor condition, was opened on design v2 FINAL (decision:h27-open; doc d8c8949f2896cf1ec), STOPPED at its bench by all three stop rules (record:h27-bench-result) and CLOSED as NOT shown with the distractor condition a recorded limit (decision:h27-closed, record:distractor-capture-limit, 2026-09-26). **H28, the recognition-core discount of a ubiquitous odour (queued as proposed at the H27 closure), was opened on design v2 FINAL (decision:h28-open; doc da2c1c079a1766d3e), evaluated once and SHOWN under its registered criteria (record:h28-result; report doc d29986a75ef4e9711), and CLOSED as SHOWN with the burst-ranked value tie adopted for the three-channel distractor form only (decision:h28-closed, decision:h28-burst-tie-adopted-within-tested-conditions, 2026-09-26).** **H29, the H26 T3b limit (a loss after tracking), was opened for design (decision:h29-open-design), measured first by the T3b diagnosis (decision:t3b-diagnosis; record:t3b-diagnosis-result), opened on design v2 FINAL (decision:h29-open; doc d724287aa203d256d), evaluated once and SHOWN under its registered criteria (record:h29-result; report doc d92ffd006bdbcdc28), and CLOSED as SHOWN with the window 200 adopted, the adopted two-channel agent now Agent17 (decision:h29-closed, decision:h29-window-200-adopted-within-tested-conditions, 2026-09-26).** **H12, the differential persistence of the acquisition and extinction traces, was opened on design v2 FINAL (decision:h12-open; doc d27ec95924fe49be1): Stage 1 PASS at the module level (record:h12-bench-result; tau_ext* 5000), Stage 2 STOPPED at its bench, K0 unreadable (record:h12-stage2-bench-result); closure or a Stage 2 redesign awaits the owner.** The rest, ranked in decision:h28-open-design: (4) H10; (5) H18; (6) an H17 re-attempt. H17, H18, the T3b cast-phase dependence and the
selection circuit's revision via the empty state stay as recorded limits; the silence timeout defect is fixed
within the release's scope (non-negative held values) and stays in force at negative held values under N2.

- **H17** (concept:h17-cold-search) finding a plume from an odour-free start without walls. Moved up: it now
  carries a measured consequence (the release at negative values strands the agent outside the plumes, no whiff
  afterwards in 131/131; record:release-negative-cost-limit). Opened on design v2 FINAL (decision:h17-open; doc
  d83a917ea4152b4a7, experiments/h17/h17_design_v2.md); src/ph26.py; STOPPED at the bench, no candidate on part
  (d) (record:h17-bench-result): the search finds the plume from the stranded state ((c1) all PASS) but engages in
  18/400 T1 rows (upper bound 0.070 > 0.05). Tasks not run. Run 2 opened for design (decision:h17-run2-open-design;
  design v1 DRAFT doc dedd3d11f43f9156f, experiments/h17/h17_run2_design_v1.md: engagement at q >= 250, T3 (c)
  re-anchored, new seeds); opened on design v2 FINAL (decision:h17-run2-open; doc d73c77ebd99d50d86; src/ph27.py) and
  STOPPED at the bench by the (h2) stop rule (record:h17-run2-bench-result: T3 lost-row DP -0.0650, pass probability
  0.2287; every no-candidate part PASS, (d) 4/400); tasks not run. **CLOSED as NOT shown (decision:h17-closed,
  2026-09-24):** nothing adopted, the relaxations lapsed, seeds kept registered; cold-start search stays a recorded
  limit (record:release-negative-cost-limit unchanged).
- **H26, adaptive presence** (concept:h26-adaptive-presence; proposed by the interpreting assistant in the H24 Run 2
  closure, not decided; opened for design by decision:h26-open-design, the number assigned there). A fixed N cannot
  satisfy both T1 and W1 (record:h24-run2-n-sweep-result). Opened on design v2 FINAL (decision:h26-open; doc
  d54441658b54a6799): the presence prior separated from the window (Agent14, counter start 240, window 300); src/ph28.py;
  bench M4 PASS (record:h26-bench-result); **evaluated once, SHOWN under the registered criteria** (record:h26-result;
  report doc d8163e16317b251eb). **DONE: CLOSED as SHOWN and adopted within the tested conditions (decision:h26-closed,
  decision:h26-adaptive-presence-adopted-within-tested-conditions, 2026-09-25).**
- **H20 Stages B and C** (concept:h20-learned-positive-valence-in-behaviour). **Stage B DONE: CLOSED as SHOWN**
  (decision:h20-stage-b-closed, 2026-09-25; design v2 FINAL doc d3f2ce9707790cd87; src/ph29.py;
  record:h20-stage-b-result; report doc d66ad8dea08c92116; nothing new adopted). **Stage C OPENED on design v2 FINAL**
  (decision:h20-stage-c-open, 2026-09-25; doc d27e6dfe2e2c16183; the Stage C-only release rule
  decision:release-value-gated-stage-c; src/ph30.py) and **STOPPED at the bench by its (hR) stop rule**
  (record:h20-stage-c-bench-result; tasks not run); post-bench diagnosis done (record:h20-stage-c-post-bench-diagnosis-result);
  **Stage C Run 2 opened on design v2 FINAL** (decision:h20-stage-c-run2-open; doc d007990ab333e7194: M4(c)'s
  readability re-signed to read on G3+, new seeds; src/ph31.py), bench M9 PASS, **evaluated once: SHOWN under its
  registered criteria** (record:h20-stage-c-run2-result; report doc de5963e5a73875a97). **DONE: Stage C Run 2 CLOSED as
  SHOWN, N2 ADOPTED, H20 CLOSED as a whole** (decision:h20-stage-c-run2-closed,
  decision:n2-release-adopted-within-tested-conditions, decision:h20-closed, 2026-09-25). As first queued: B, the same choice
  task with the value learned (its own criteria written at its design time; A4 does not transfer
  as it stands); C, the gain in the H15 Run 2 world with learning on, with Run 2's avoidance and
  long-horizon search values as the reference. Both depend on a task in which selection can be
  expressed in behaviour, which Stage A did not have and which the link check has now
  characterised, and on a hold that stays, which H21 tested (the gate adopted within its tested
  conditions only).
- **Silence timeout**, H25, closed as shown (decision:h25-closed); the release adopted at +1/0, on hold at negative
  values (decision:release-negative-scope-on-hold) (record:silence-timeout-chain-result).
- **H24 Run 2** (decision:h24-run2-open): the presence-scoped value filter on Agent10 at +1/0; design v2 FINAL;
  stopped at bench (h) (record:h24-run2-bench-result); N sweep done: no N in 60-450 meets both the T1 and the W1
  target (T1 clears from N 200, W1 only up to N 120; record:h24-run2-n-sweep-result). CLOSED as NOT shown
  (decision:h24-run2-closed): nothing adopted, the Run 2 relaxation lapsed.
- **A proper distractor condition** (a third, irrelevant odour), which is what the hold's benefit
  needs; it changes the circuit's size and Phase 2's calibration. **H27: opened on design v2 FINAL (decision:h27-open),
  STOPPED at the bench by (h), (hW), (hH) (record:h27-bench-result); DONE: CLOSED as NOT shown (decision:h27-closed,
  2026-09-26)**, the distractor condition recorded as a limit of the adopted agent (record:distractor-capture-limit;
  concept:h27-irrelevant-odour-distractor; design v1 DRAFT doc d1b2bdacd81997da7, v2 FINAL doc d8c8949f2896cf1ec); the
  hold's benefit under a distractor stays unmeasured.
- **H28, discounting a ubiquitous odour by its whiff statistics** (concept:h28-ubiquitous-odour-discount; queued as
  proposed by the interpreting assistant at the H27 closure, not decided; opened for design by decision:h28-open-design,
  the number assigned there; design v1 DRAFT doc dc81dbd5005ca164c), ranked first: it addresses a measured failure of the
  recognition core the owner named (T1D DP -0.1325, W1D every row lost); habituation in its usual sense is rejected by
  arithmetic and a burst-ranked value tie is recommended; the W1D rows in which B is never sensed before the capture stay
  in the recorded limit. **Opened on design v2 FINAL (decision:h28-open); evaluated once, SHOWN under its registered
  criteria (record:h28-result). DONE: CLOSED as SHOWN, the tie ADOPTED for the three-channel distractor form only
  (decision:h28-closed, decision:h28-burst-tie-adopted-within-tested-conditions, 2026-09-26).**
- **The H26 T3b limit** (a loss after tracking: the post-whiff window a fixed 300 steps, 4.412 against 5.772), ranked
  second: a measured limit of an adopted module, narrow; a fix is another counter rule with the trade-off of
  record:h24-run2-n-sweep-result. **Opened for design as H29 (decision:h29-open-design, 2026-09-26; design v1 DRAFT doc
  dd00688c21f09b13e):** by T3b's construction no own-state rule separates a loss from a tracking silence; the lever is the
  window's length (Agent17, window 200). The T3b diagnosis is done (decision:t3b-diagnosis): F2 NOT MET, F5 MET, T3b
  gain +2.460 at window 200. **Opened on design v2 FINAL (decision:h29-open); evaluated once, SHOWN under its
  registered criteria (record:h29-result). DONE: CLOSED as SHOWN, the window 200 ADOPTED, Agent17 the adopted
  two-channel agent (decision:h29-closed, decision:h29-window-200-adopted-within-tested-conditions, 2026-09-26).**
- **H12** the acquisition and extinction traces persist differently; this is what would make
  the parallel site earn its place. Ranked third: the memory half of the core, but no measured failure calls for it.
  **Opened on design v2 FINAL (decision:h12-open, 2026-09-26; doc d27ec95924fe49be1, experiments/h12/h12_design_v2.md):**
  Stage 1 PASS at the module level (record:h12-bench-result; tau_ext* 5000; SR 0.6322, RET 1.2279 for both signs);
  Stage 2 (decision:h12-stage2-composition) STOPPED at its bench, K0 unreadable (record:h12-stage2-bench-result; ceiling
  minus floor +0.0925 < 0.30). Awaiting the owner: close at the module level or redesign Stage 2.
- **H10** abstention and revision belong to different stages: a thresholded stage decides
  whether to commit at all, a graded stage decides what to and revises it. Ranked fourth: a rebuild of the selection
  circuit that would reopen every adopted bench; revision via the empty state works in the adopted agent.
- **H18** (concept:h18-ring-under-cue-loss) why the ring loses the plume under cue loss. The
  10 degree mean error is not taken as the cause; first the tail of large errors, how long an
  error persists, and the heading error just before a plume is lost. Ranked fifth: outside the adopted scope, where the
  wind is sensed every step (64.5 percent unrecovered under 50-step cue loss, concept:ring-leaks-under-cue-loss).
- **An H17 re-attempt** (cold start), ranked sixth: closed twice at the bench (decision:h17-closed); the consequence that
  moved it up (the release stranding negative holds) no longer arises by code under N2; a Run 3 would need new state.
