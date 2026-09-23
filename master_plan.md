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

### H20 (decision:h20-priority-design-first; Stage A opened by decision:h20-stage-a-open, CLOSED by decision:h20-stage-a-closed; link check by decision:h20-linkcheck-open, complete; Run 2 opened by decision:h20-run2-open, evaluated, CLOSED by decision:h20-run2-closed)
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

## The architecture as currently adopted

Stated here so a later session does not have to reassemble it from decisions.

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
  condition exists, so its distractor resistance is unverified.
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
  **Note:** in the agent a POSITIVE valence has no behavioural effect. Two-sided learning can be
  read in the weights; only its negative side can show in behaviour. H20 Stage A tested one
  pathway for it: it reaches selection, not the source reached first.
- Navigation: surge-and-cast on a wind reference with the RETURN cast (triangle wave), adopted
  by decision:h16-close-limited-adoption. **Scope:** environments with little boundary influence
  and heading information on every step; tracking a plume already entered and reacquiring it
  after loss. **Not validated:** finding a plume from an odour-free start (about half, H17);
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

## Why this order
Phase 0 makes later comparison trustworthy. Phase 1 comes before further modelling because it can redirect Phases 2 to 4 and is the project's stated purpose. Phase 2 precedes 3 and 4 because both will reuse the Select-and-Hold circuit and inherit its defects. Phase 3 precedes 4 because heading memory needs no learning, while the integrated agent needs both. Phases 5 and 6 need everything before them.

## Awaiting the owner

- **H24 variant choice and confirmation of design v1** (doc d24c2efe28592c34d;
  record:option-v-presence-diagnosis-result): (v-a) strict, (v-c) presence counter starting OFF, or (v-p)
  counter starting ON (outside option (v) as worded), or (iv) instead; if (v-c) / (v-p), the draft
  classification-rule relaxation signed or refused and N (proposed 60); the bars and allowed gaps; both tasks
  required. Part A predicts (v-a) / (v-c) fail the H21-task bars and pass W1 by identity.

## Queued candidates, none started

The order does not change without a decision node. H21 is closed (decision:h21-closed); H22 is closed
(decision:h22-closed); H23 is closed as shown (decision:h23-closed). Next, in this order
(decision:next-absent-odour-check-then-stage-b): the absent-odour check is complete
(record:absent-odour-check-result: reach kept, the cost in dwell and drift); H24 (filter scope, option v) in
design (decision:filter-scope-explore-option-v); then H20 Stage B. H20's Stages B and C stay queued behind the check. H17, H18,
the silence timeout and the selection circuit's revision via the empty state stay as recorded limits.

- **H20 Stages B and C** (concept:h20-learned-positive-valence-in-behaviour): B, the same choice
  task with the value learned (its own criteria written at its design time; A4 does not transfer
  as it stands); C, the gain in the H15 Run 2 world with learning on, with Run 2's avoidance and
  long-horizon search values as the reference. Both depend on a task in which selection can be
  expressed in behaviour, which Stage A did not have and which the link check has now
  characterised, and on a hold that stays, which H21 tested (the gate adopted within its tested
  conditions only).
- **Silence timeout**, as a reset-control change or a circuit change
  (record:silence-timeout-chain-result); selection maintenance, release and distractor resistance
  re-verified either way.
- **H17** (concept:h17-cold-search) finding a plume from an odour-free start without walls.
- **H18** (concept:h18-ring-under-cue-loss) why the ring loses the plume under cue loss. The
  10 degree mean error is not taken as the cause; first the tail of large errors, how long an
  error persists, and the heading error just before a plume is lost.
- **A proper distractor condition** (a third, irrelevant odour), which is what the hold's benefit
  needs; it changes the circuit's size and Phase 2's calibration.
- **H12** the acquisition and extinction traces persist differently; this is what would make
  the parallel site earn its place.
- **H10** abstention and revision belong to different stages: a thresholded stage decides
  whether to commit at all, a graded stage decides what to and revises it.
