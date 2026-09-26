# H27 post-bench diagnosis: how the background odour D takes over navigation, where the 122 (m) rows come from, and why M6 cannot be read

Date 2026-09-26. Measurement only. The owner asked for it (decision:h27-post-bench-diagnosis). After the H27 bench stop the owner was offered three options: (1) close H27 at the bench stop, (2) run a measurement-only diagnosis first, (3) write a Run 2 design. The owner answered on 2026-09-26, verbatim '진단 먼저' (gloss: 'the diagnosis first'). This diagnosis does not re-judge H27's verdict and adopts nothing. The verdict stands as recorded in record:h27-bench-result: stopped at the bench by the registered stop rules (h), (hW), (hH); tasks not run.

Nothing that H27 registered was changed:
- src/ph32.py (sha256 d9f585d5599ea9a4f218e87bd884fa8246a826be0111f495cfbec299a9222743, source doc d5a2b6526d40efbef);
- design v2 FINAL (doc d8c8949f2896cf1ec);
- Agent15, the harness, the arms and the D generator, with p_D fixed at 0.03;
- every bar, every rule and every adopted module. All are imported as they are.

Code: src/ph32b.py, sha256 4c8adf5e4c4e6612aaa2631476805fc18f0c2dee78a05c16b19d48ab80b89f10. Its source is stored in its own document, doc de72961845e8a258b, whose content_hash equals the file's sha256.

Output: experiments/h27/ph32b_diag.txt, sha256 ec3abdec0912a55791eef53192b41b9cf5843beb5117cfc261a7cfeee9d8d0ae, LF line ends. It is appended below in full. Every measured number in sections 1 to 4 comes from it and is cited as diag:N (its line N). Numbers quoted from other records carry the record's id.

**Seeds.** Only the bench seeds were used: world 20261121, agent 20261122, bootstrap 20261123.
- ph32b.py reads them from ph32 and does not write them. Neither ph32b.py nor its output contains them, and the output text is checked before it is written.
- After the output was written, ph32's seed scan was re-run: no H27 seed or derived number appears in any other file, 218 files scanned.
- The scan excludes the following by name: ph32.py, ph32_*.txt, h27_*.md (this report among them), master_plan.md, notes/*.md, viewer/*.
- It also excludes one (file, number) pair set by decision:seed-scan-exclusion-ph31-eval: experiments/h20/ph31_eval.txt.
- The development seeds (9937/9947) and the evaluation seeds (2083/2173) were not used. They remain registered to H27.

No rule, parameter, bar or arm was changed. No agent variant was added. Nothing was swept.

## 0. What was asked

The diagnosis was put with three questions.

**(A) By which path a D whiff takes over navigation.** The candidates were: the filter's top rule, where D at value 0 ties with the neutral odour B; the fraction of steps with nothing held; and the moment the agent leaves, going upwind. The questions under (A):
1. What is held, and how holds end.
2. nav events by source, and what the cast clock `since` does on D whiffs.
3. Presence by the counters, and the top set.
4. The trajectory consequence.
5. The W1D surge accounting. This includes the design's stated risk (section 2.4): once the release ends a hold, D whiffs steer and reset the cast clock.

**(B) Where the 122 (m) rows come from.**

**(C) Why the hold's benefit (M6) cannot be read**, given that both arms lose every W1D row.

## 1. Reproduction check (diag:6-24)

- ph32.py's sha256 equals the bench's, and ph32_bench.txt's sha256 equals the recorded 95721447...22f9 (diag:7).
- **ph32.bench() was re-run as it is, through ph32's own run, identities, benches and stop rules. It printed 60 lines, and all 60 equal ph32_bench.txt line for line** (diag:8).
- The headline numbers were asserted by name, and each holds (diag:9):
  - T1D P(V) 0.787 with D and 0.920 without;
  - DP -0.1325 [-0.1675, -0.1000];
  - W1D paired dwell -19.7825;
  - lost rows 400 with D against 22 without;
  - (hH) DP +0.0000 and M6 0.0000;
  - (m) 122;
  - all three stop rules STOP.
- The (m), (h), (hW) and (hH) lines are printed again with the seed numbers redacted (diag:10-24).
- The nav law was rebuilt from the recorded fields (reading D2). It equals the recorded NAV on every (step, row) of the six runs analysed (diag:25).

Everything below was measured on these reproducing runs.

Measurement definitions (ph32b.py header, D1-D7):
- The read hold is the circuit's hold H. In the hold-not-read arm it is the per-step argmax HR.
- A nav event is **D-driven** when its steering set is D alone. The steering set is the held odour's whiff under `keep`, and otherwise the whiffing odours in the top set.
- Hold ends are classified by the flags of the step on which the hold ends:
  - 'evidence': the evidence flag EV is set;
  - 'timeout (release)': the timeout flag TO is set. This is the H25/N2 release, ending a hold 48 steps after the held odour's last whiff;
  - 'other': neither flag is set;
  - 'row end': the hold is still on at step 599.
- d_along is the along-wind distance from the sources' line, measured at the sensing position; upwind is -x. The upwind wall is at x 0.
- End states at step 599 are classified by position.

## 2. (A) The capture path

### (A1) What is held and how holds end (diag:27-55)

| run | nothing held (steps 59-599) | V | B | D | D holds (rows) | how D holds end: timeout / evidence / other / row end | steps from the last D whiff to a timeout end |
|---|---|---|---|---|---|---|---|
| T1D Agent15 D on | 0.563 | 0.174 | 0.011 | 0.252 | 842 (356) | 331 / 375 / 22 / 114 | 48/48/48/50/56 |
| T1 Agent15 D off | 0.688 | 0.276 | 0.036 | 0 | none | | |
| W1D Agent15 D on | 0.549 | 0 | 0.017 | 0.434 | 1035 (392) | 798 / 15 / 24 / 198 | 48/48/48/48/57 |
| W1 Agent15 D off | 0.798 | 0 | 0.202 | 0 | none | | |
| W1D release-off D on | 0.262 | 0 | 0.025 | 0.713 | 453 (389) | 10 / 30 / 27 / 386 | (length 1/235/390/494/592) |

Quantiles are min/p25/median/p75/max.

**How B holds end** (diag:30, 34, 38, 42):

| run | B holds | timeout | evidence | other |
|---|---|---|---|---|
| W1 D off | 998 | 915 | 0 | 0 |
| W1D D on | 236 | 55 | 162 | 19 |
| T1 D off | 247 | 163 | 80 | 0 |
| T1D D on | 156 | 25 | 119 | 12 |

- In the task, D holds form in 392 of 400 W1D rows, and 1035 D holds form in total. With the release on, 798 of the 1035 end by the timeout, 48 steps (median) after D's last whiff.
- The bench measured this 48-step end on constructed states only. Here it holds in the task as well.
- With the release off, D holds last 390 steps (median), and 386 of the 453 are still on at step 599 (diag:47).
- V holds end by the timeout in every run, at 48 steps (median) after the last V whiff (diag:29, 33).

### (A2) nav events by source, and the cast clock (diag:57-97)

| run | nav events (per row) | D-driven | share D-driven | D-driven with V present / absent | first D-driven nav step |
|---|---|---|---|---|---|
| T1D Agent15 D on | 4899 (12.25) | 1348 (held-hit D 585, nothing held D 763) | 0.275 | 0 / 1348 | 59/77/92/118/591 (96 rows) |
| T1D, the 278 V-always-present rows | 3223 | 0 | 0.000 | 0 / 0 | none |
| T1 Agent15 D off | 4266 (10.66) | 0 | 0 | | |
| W1D Agent15 D on | 6677 (16.69) | 6381 (held-hit D 2922, nothing held D 3459) | 0.956 | 0 / 6381 | 59/72/88/112/294 (400 rows) |
| W1 Agent15 D off | 3565 (8.91), all B | 0 | 0 | | |
| W1D hold-not-read D on | 6712, all 'held-hit' by the read argmax | 6468 | 0.964 | 0 / 6468 | 59/69/82/105/294 |
| W1D release-off D on | 6664 (held-hit D 4695, nothing held D 1632) | 6327 | 0.949 | 0 / 6327 | 59/72/88/120/330 |

**What `since` does on D whiffs.** By the code (ph23.py:95; ph32.py:194 in Act15), `since` resets on nav and on nothing else.
- Measured: SINCE == 0 exactly on the steps with nav, in every run (diag:60, 65, 70, 75, 80, 85, 90, 95).
- A D whiff therefore resets the cast clock exactly when it is part of a nav event.
- Share of D-whiff steps with a D-driven nav: 0.188 in T1D (diag:60) and 0.888 in W1D (diag:70).
- By state, W1D (diag:71):
  - V absent and nothing held: every D whiff steers (3469/3469, of them 3459 D-driven);
  - V absent and D held: every D whiff steers (2922/2922);
  - V absent and B held: 2 of 88 steer, and those 2 were not D-driven;
  - V present: none of the D whiffs steers (0 of 511 + 149 + 48).
- T1D has the same pattern (diag:61): V absent, nothing held 764/764; V absent, D held 585/585; V absent, B held 0/30. With V present, the D-whiff steps that carry nav are V-driven (0 of them D-driven).

**B whiffs with V absent** (diag:72): with B held they steer (79/79); with nothing held they steer (217/217); with D held they do not (0/1).

### (A3) Presence and the top set (diag:99-109)

| run | V present (59-599) | B present | D present | top {V} | top {B, D} | top {D} | D in top (all steps) | (step, row) with V present and D in top |
|---|---|---|---|---|---|---|---|---|
| T1D D on | 0.787 | 0.471 | 0.989 | 0.808 | 0.105 | 0.084 | 0.190 | 0 |
| W1D D on | 0.000 | 0.413 | 0.989 | 0.098 | 0.366 | 0.526 | 0.892 | 0 |
| W1 D off | 0.000 | 0.928 | 0.000 | 0.098 | 0 | 0 | 0 | 0 |

- **D is never in the top set while V is present** (0 (step, row) in every run; diag:62, 72, 97). **No D-driven nav occurs while V is present** (0 in every run). D is present by its counter on 0.989 of steps.
- Where V is absent, D is in the top set as follows:
  - with B present, as the tie {B, D};
  - with B absent by its counter, alone. In W1D this is 0.526 of all (step, row).
- In W1D, D is in the top set on 0.862 of the steps with nothing held (diag:105).

**The capture path, as measured.** It runs through nav in the periods when V is absent, in two ways:
- D whiffs with nothing held (the filter's top rule: D is tied at value 0 with B, or is top alone);
- D whiffs while D is held (`keep` on a D hold).

Each such nav resets `since`. Holds enter the path in two ways, neither of which steers by itself:
- a D hold makes D's whiffs the only steering input and blocks B's whiffs;
- B holds, which would block D, are rare under D (B held on 0.017 of W1D steps 59-599, against 0.202 without D). They end mostly by the evidence release (162 of 236), where D is the strongest non-held channel.

While V is present nothing goes through nav: in T1D, the 278 rows with V present on every step have no D-driven nav and the same trajectory with and without D (diag:93-94, 130-134).

### (A4) Trajectory consequence (diag:111-141)

The first D event is the first D hold or the first D-driven nav in the D-on run.

| rows | n | first D event step | first step where D on and D off positions differ | d_along at the first D event (upwind of the sources' line) | inside a whiff region then | upwind displacement over the next 20 steps (max 12) | steps to the first wall contact |
|---|---|---|---|---|---|---|---|
| T1D out of V (V without D, not V with D) | 53 | 9/65/79/91/108 | 59/72/83/93/110 | -8.9 median (48/53) | 5/53 | 11.6/11.9/12.1 (quartiles) | 119/130/168 |
| T1D lost with D | 90 | 9/73/87/101/446 | 59/77/92/107/591 | -9.7 (80/90) | 6/90 | 11.3/11.8/12.1 | 116/127/174 |
| T1D the 122 (m) rows | 122 | 9/77/96/201/548 | 59/77/92/118/591 (96 rows; 26 never differ) | -8.8 (106/120) | 8/120 | -0.7/11.6/12.0 | 116/127/187 |
| T1D the 278 V-always-present rows | 278 | first D event is a D hold in 240 | never (278 identical) | | | | none |
| W1D all rows | 400 | 8/63/80/105/294 | 59/72/88/112/294 | -6.9 (303/400) | 93/400 | 11.2/11.8/12.1 | 116/134/172 |

**At the first D-driven nav, what is held** (diag:114, 138):
- T1D out-of-V rows: nothing is held in 52 of 53. The last hold before it was a B hold ended by the evidence release in 30, a B hold ended by the timeout in 10, and in 6 rows there had been no earlier hold.
- W1D: nothing is held in 363 of 400 and D in 37. For the 363, the last earlier hold was a B hold ended by evidence in 133 and by the timeout in 45; in 144 rows there had been no earlier hold.

**End state at step 599:**

| rows | at V | at B | at a wall | upwind of both | in the along range |
|---|---|---|---|---|---|
| T1D out of V, D on | 0 | 0 | 42 | 11 | 0 |
| the same rows, D off | 5 | 0 | 0 | 42 | 6 |
| W1D, D on | 0 | 0 | 303 | 97 | 0 |
| W1, D off | 0 | 22 | 0 | 332 | 46 |

The out-of-V rows are V by dwell majority without D. At step 599 they are mostly upwind of both sources without D (42), not at V (5).

**Where the wall contacts are.** They are at the upwind wall x 0 almost entirely: 42057 of 42258 in W1D, with 0 at the downwind wall (diag:141); 5626 of 5662 in the T1D out-of-V rows (diag:117). There are no wall contacts without D.

### (A5) W1D surge accounting (diag:143-177)

**Surges per row** (diag:144, 149):

| surges per row | W1D, D on | W1, D off |
|---|---|---|
| D whiffs, nothing held | 8.65 (all 400 rows) | 0 |
| D hits, D held | 7.30 (375 rows) | 0 |
| B whiffs, nothing held | 0.52 | 6.52 |
| B hits, B held | 0.20 | 2.39 |

**Upwind displacement per row, by the driver of the nav segment** (diag:146, 151). A segment runs from a nav event to the next one.

| driver | W1D, D on | W1, D off |
|---|---|---|
| cast before any nav | 23.6 | 11.4 |
| B-driven | 5.1 | 20.7 |
| D-driven | 59.6 | 0 |
| total | 88.3 | 32.1 |

- **Per D-driven segment that starts before the row's first wall contact** (2055 segments): 11.61 upwind units on average, 0.353 per step (diag:147).
- On the surge step itself, a D-driven surge moves a median 0.20 upwind (max 0.6).
- Counted over all D-driven segments, the median displacement is 0.4, because most of them start at the wall.

**The cast target** on steps 59-599 (diag:148, 152):

| | W1D, D on | W1, D off |
|---|---|---|
| target within 40 degrees of upwind | 0.630 | 0.243 |
| target with a downwind component | 0.115 | 0.499 |
| `since` on nothing-held steps, quartiles | 12/36/68 | 66/100/136 |

**Leaving B's cone** (diag:163-168):
- **In every row the agent first passes more than 3 upwind of the sources' line on steps 42-52 (median 45), with and without D.** The trajectories are identical until then: D on and D off first differ at step 59 or later (diag:136). nav cannot occur before step 59 in W1.
- Afterwards the agent comes back downwind of the sources' line in 383 of 400 rows without D, but in 83 of 400 with D.
- The furthest upwind d_along reached: median -70.9 with D, -32.6 without.
- Upwind displacement after the first pass, by driver:
  - with D: D-driven 59.6, B-driven 5.1, cast 0.7;
  - without D: B-driven 20.7, cast -11.5, meaning the cast carried the agent back downwind.

The design's stated risk (2.4) was that surges on D whiffs carry the agent upwind out of B's cone. As measured, the initial cast carries the agent out of the cone upwind, in both runs. D-driven segments then make up most of the further upwind travel (59.6 of 88.3 units per row) that takes it to the wall.

Arm comparison in W1D (diag:153-162):
- The hold-not-read arm (D-driven 60.2 per row, 0.351 per step before the wall) and the release-off arm (60.6, 0.356) show the same accounting.
- In T1D's 53 out-of-V rows it is also the same: D-driven 61.3 per row, 0.323 per step before the wall; the target is within 40 degrees of upwind 0.636 with D against 0.237 for the same rows without D (diag:169-177).

## 3. (B) The 122 (m) rows (diag:179-196)

The (m) population is defined on the **D-off** run (ph32 reading R7): V absent by its counter on some step. D plays no part in why V is absent in these rows.

**Why V is absent, D off.** Of the 122 rows:
- **103 are prior expiry**: no V whiff on steps 0-58, so V is absent at step 59.
- **19 are a 300-step V silence after a whiff**: absent at 300/318/338/490/578; the last V whiff was at 0-278 (diag:180, 185).

**The design's 15-20 prediction** was anchored on H26's at-risk set. That set is narrower (ph28 reading R3: no V whiff by step 58, plus a B whiff with nothing or B held before the first V whiff).
- Applied to this D-off run, the H26 definition gives **21 rows**, all inside the 122 (diag:181).
- The literal reading, from step 0, gives 103.
- In the record, H26's bench had 15 at-risk rows and 111 rows with no V whiff by step 58 (record:h26-bench-result). Here there are 103 rows with no V whiff by step 58, 31 by step 118, and 14 that never get one (diag:182).

**State at the first absent step ta, D off** (diag:183-184):
- **prior (103)**:
  - B held at ta in 96, nothing held in 7;
  - all 103 upwind of both sources, d_along -7.2/-6.8/-6.0;
  - before step 59: B whiffs in 101 rows, a B hold in 96, within 3.0 of B in 96.
- **silence (19)**:
  - B held in 7, nothing held in 12;
  - 18 upwind of both sources.

**The same rows with D.**
- V is absent in the same 122 rows, first at the same step (diag:186).
- What is held at ta with D (diag:189): nothing in 66, B in 55, D in 1.
- Without D, all 103 B holds held at ta end by the timeout. With D, the B holds held at ta end by the evidence release in 32 and by the timeout in 22.

**Classification.** Position- and event-based, not causal: the mechanism of the D-off absence, times what is held at ta without D, times the first D event at or after ta before the next V whiff with D (diag:187, 190-194). Counts are rows; out-of-V rows are in parentheses.

| D-off absence | held at ta (D off) | rows (out of V) | (i) a D hold first | (ii) a D-driven nav first | (v) neither before the next V whiff or the end |
|---|---|---|---|---|---|
| (iv) prior expiry | (iii) B held | 96 (49) | 1 (1) | 70 (48) | 25 (0) |
| (iv) prior expiry | nothing held | 7 (4) | 0 | 6 (4) | 1 (0) |
| silence after a V whiff | (iii) B held | 7 (0) | 0 | 7 (0) | 0 |
| silence after a V whiff | nothing held | 12 (0) | 1 (0) | 10 (0) | 1 (0) |
| total | | 122 (53) | 2 (1) | 93 (52) | 27 (0) |

- **All 53 out-of-V rows are prior-expiry rows. 52 of them have a D-driven nav first, and 1 has a D hold first.** Among them, 49 held B at ta without D.
- No row moved into V (diag:195).
- The first D event came 13/27/39 steps (quartiles) after ta (diag:188).
- The next V whiff after ta:
  - with D, 94 rows get none;
  - without D, it comes 54/56/59 steps after ta, and 26 rows get none.
- Outcomes of the 122 rows, V/B/tie: with D 42/76/4, without D 95/26/1 (diag:196).

## 4. (C) The W1D loss paths (diag:198-212)

| arm | lost rows | last B whiff step (rows with none) | reach within 3.0 of B | last step within 3.0 of B | dwell of reaching rows | end state at 599: wall / upwind of both / at B / along range | wall contacts per row (upwind wall share) | first contact step |
|---|---|---|---|---|---|---|---|---|
| Agent15 D on | 400 | 28/36/103 (97) | 221 | 36/39/118 | 7/8/10 | 303 / 97 / 0 / 0 | 105.645 (42057/42258) | 193/225/265 |
| hold-not-read D on | 400 | 28/36/44 (97) | 221 | 36/39/114 | 7/8/9 | 302 / 98 / 0 / 0 | 107.218 (42673/42887) | 190/218/257 |
| release-off D on | 400 | 29/36/114 (97) | 224 | 36/40/123 | 7/8/11 | 302 / 98 / 0 / 0 | 103.265 (41102/41306) | 193/227/281 |
| Agent15 D off | 22 | 462/506/580 (1) | 392 | 465/508/582 | 20/26/31 | 0 / 332 / 22 / 46 | 0 | none |
| Agent15g D on (beside) | 400 | 11/35/38 (115) | 189 | 36/38/39 | 6/7/9 | 304 / 96 / 0 / 0 | 115.743 | 169/181/216 |

**Paired against Agent15 D on** (diag:209-211):

| arm | rows with the same position on all 600 steps | first differing step | lost in both / one arm only | last B whiff step equal | same end state |
|---|---|---|---|---|---|
| hold-not-read | 326/400 | 60/69/78/132/274 (the other 74) | 400 / 0 | 290/303 | 385 |
| release-off | 331/400 | | 400 / 0 | 271/303 | 391 |
| Agent15 D off | 0/400 | 59/72/88/112/294 | 22 / 378 (Agent15 D on only) | 4/303 | |

For hold-not-read, the first wall contact step differs by 0/0/0 (quartiles) over 399 rows.

**Measured: the loss is one common path in all three D-on arms, not two different paths.**
- In the three D-on arms the reaching rows touch B around step 30. That is the initial pass, since the first arrival is at 29/30/31.
- These rows dwell about 8 steps and never return: the last step within 3.0 of B is at median 39.
- Every row loses B before step 300 (the last B whiff is at step 292 at the latest).

In the hold-not-read arm the read argmax differs from the circuit's hold on 0.438 of steps (diag:212). On whiff steps it is the whiffed odour, so its nav events are all 'held-hit' and 0.964 of them are D-driven (diag:78-79).

## 5. Reading (interpretation, not measured)

- The measured sequence is consistent with this picture:
  - When V is absent by its counter, D, present on about 99 percent of steps because it whiffs everywhere, joins B in the filter's top set at value 0, or is top alone.
  - Whenever nothing is held, or D is held, its whiffs become nav events.
  - Each nav event resets the cast clock. The cast target then stays within 40 degrees of upwind on most steps, so the agent keeps moving upwind until it reaches the upwind wall.
  - Without D the same agent's clock grows, its return cast swings back downwind, and it finds the plume again.
  - Nothing in these runs isolates a cause, since no variant was run.
- The design's stated risk named the release's 48-step end of a hold as the entry point. The measurements fit that only in part:
  - With the release on, most D holds and many B holds do end at 48 steps, and nothing is then held.
  - With the release off, D holds persist (median 390 steps) and D-held hits steer as much. The release-off arm loses the same 400 rows, on the same path, with 331/400 rows identical in position.
  - B holds, which would block D, are mostly ended by the evidence release with D as the strongest other channel. They are not ended by the 48-step release.
  - So in these runs the release's end is one of several ways into the captured state, not a necessary one.
- In W1D, D does not carry the agent out of B's cone. The initial cast does that at steps 42-52 in every row, with and without D, before navigation can act. What differs is the return: 383 rows return downwind without D and 83 with it.
- In T1D, D can act only after V is absent. All 53 out-of-V rows are rows where the agent had passed the sources early (B first, B held) and was about 7 units upwind of them when V's prior ran out at step 59. Without D, the next V whiff in the (m) rows came 54/56/59 steps (quartiles) after ta.
- The design's prediction of 15-20 at-risk rows was anchored on H26's narrower definition, which gives 21 here, not on the (m) definition it registered.
- M6 cannot be read because the two arms it compares take the same path. The hold-not-read arm's argmax names the whiffed odour on every whiff step, so D whiffs steer it as they steer Agent15. B holds, the only holds that would shield navigation from D in W1D, are rare and short-lived under D in both arms. In this condition the hold has no occasion to differ between the arms. Whether the hold would help in a condition where the adopted arm does not lose every row is not measured.
- These are bench seeds only. The numbers describe the bench runs and are not estimates for the registered development or evaluation seeds.

## 6. What the owner can decide

Listed neutrally. Nothing is adopted. H27's verdict (stopped at the bench by (h), (hW), (hH); tasks not run) stands whichever is chosen.

- **Close H27 at the bench stop**, with the distractor condition recorded as a limit of the adopted agent (Agent14N2 composed with three channels): with a value-0 background odour at p_D 0.03 and the valued odour absent by its counter, the adopted navigation follows the background odour's whiffs. The measured counts it would rest on:
  - W1D: D-driven nav is 0.956 of nav events; every row is lost; the agent sits at the upwind wall at step 599 in 303 of 400 rows.
  - T1D: 53 rows move out of V, all in the prior-expiry population.
  - While V is present: 0 D-driven nav events and identical trajectories in the 278 V-always-present rows.
  - The hold's benefit (M6) remains unmeasured.
- **A Run 2 design.** It would need its own registration, predictions and bench on new seeds. The bench seeds' role is spent. The development and evaluation seeds 9937/9947 and 2083/2173 remain registered to H27 and unused. It would have to register at least one of the following, each with its reason stated in advance:
  - (a) **A rule change in the filter's top set for an odour that has never been reinforced.** At supplied +1/0/0 with learning off, B and D carry the same value and neither is reinforced. So a rule that keeps D out of the top set must say what separates D from B, for example a record of reinforcement or of location, which is new state. Otherwise it is a value-sign question. It needs a signed relaxation of the classification rule in H14 format. It would rest on:
    - D whiffs steer whenever V is absent and nothing or D is held (W1D 3469/3469 and 2922/2922; T1D 764/764 and 585/585);
    - D is never top while V is present.
  - (b) **A lower p_D, as a different condition.** For example 0.01, the design's alternative. It is not a repair of this one. Measured here:
    - about 18 D whiffs per row (7187 over 400 rows);
    - 16 D-driven surges per row in W1D;
    - 11.6 upwind units per D-driven segment before the wall.
    No other rate was run, so the size of the effect at another rate is not measured.
  - (c) **The release's 48-step end as the entry point.** This is an adopted module (H25, N2; decision:n2-release-adopted-within-tested-conditions); a change reopens it. Measured: the release-off arm loses the same 400 rows, D holds then last to the end of the row, and D-held hits steer (11.74 per row). Changing the release alone therefore did not prevent the loss on these runs.
  - (d) **The H19 (a) reset boundaries: what resets the cast clock.** `since` resets on every nav event, so D-driven nav resets it. This is an adopted navigation boundary. It rests on:
    - the target within 40 degrees of upwind 0.630 with D against 0.243 without;
    - the target downwind 0.115 against 0.499;
    - the median `since` on nothing-held steps 36 against 100.
  - For M6 in particular: any design that means to read the hold's benefit needs a condition in which the adopted arm does not lose every row. Here the two arms are identical in position in 326 of 400 rows.

## 7. What this does not establish

- No change was tested. No alternative rule, rate, release, reset or arm was run.
- The classes, positions, hold records and displacement sums describe the runs and name no cause.
- The tasks were not run, and no development or evaluation seed was used.
- Nothing here re-opens the bench verdict.

## 8. Provenance

- Decision: decision:h27-post-bench-diagnosis (owner, 2026-09-26, '진단 먼저').
- Code: ph32b.py, sha 4c8adf5e...9f10. It imports ph32 (sha d9f585d5...2743) unchanged, checked at run time, together with the modules ph32 imports.
- Design: v2 FINAL, doc d8c8949f2896cf1ec, hash 88fdfdf7...7ddb.
- Reproduced: ph32_bench.txt (sha 95721447...22f9), all 60 lines.
- Seeds: the bench seeds only.
- Output: ph32b_diag.txt (sha ec3abdec...d0ae). Run twice from scratch; the two outputs are byte-identical.
- Bench result: record:h27-bench-result. This result: record:h27-post-bench-diagnosis-result. H26 reference: record:h26-bench-result.

## Appendix: ph32b_diag.txt in full

```
== H27 post-bench diagnosis (measurement only; owner 2026-09-26, '진단 먼저', decision:h27-post-bench-diagnosis). ph32b.py sha256 4c8adf5e4c4e6612aaa2631476805fc18f0c2dee78a05c16b19d48ab80b89f10; ph32.py sha256 d9f585d5599ea9a4f218e87bd884fa8246a826be0111f495cfbec299a9222743; design H27 v2 FINAL doc d8c8949f2896cf1ec hash 88fdfdf7a68c4a8d254bd505ac8aaea0f1e2a2697b68fc105701fda9940c7ddb; reproduces experiments/h27/ph32_bench.txt sha256 957214476919dbbfa30c6b7f294d6b8554aec01eef485810d8e1a427dd4722f9 (record:h27-bench-result) ==
   imported modules (as ph32 prints them): ph2.py 9e0ef833d3f5957da341cfeb9edd77fe9adb11de5354c71162c7569e83e30a4a; ph11.py e80f40bd710aca43252f04329846ffa29943251d19e718450e9a7ff49e947a23; ph14.py c6b745c60f9992934a0ccbc5584ef354a03f53f08b37a1252a694feb350be0d0; ph15.py cc9399965e5cbc30cb7f35e8ce296d8d43e4657cf644d1ec350931e594403fdc; ph16.py 33d5fdb25959fb7f9cbe465ca25a8973776b39f1e5170d645cb53bc8d906a2c2; ph17.py 4b30ddf8b1fc6dc510f23a28f09d6391003d95f0744344d237f50e3393a3689f; ph22.py 03ab8c4706b19557af5d64edd83f812abba91b618439618b35837a49dd44ca1c; ph23.py ae180492eece93739da4d1b5d83a13a2b42c5e952445a92ab75f95c6fb2eb5ae; ph24.py f344f178e20380858f4d7400ef670223f90aa2927b3f7304772ae1d848bd1bef; ph25.py 5620a90819693379a53374ca3841e3bc3ddba860d8a8351da7aa1ed4dfe17d91; ph28.py 64ce7d0ce123f912aa675e86627d5b6b0ae3d89976b093666316e6b78441e7aa; ph30.py 98822834043de5f31615e73cd4a83444adcef2f1d5e56478356d70ca905059bd; ph32.py d9f585d5599ea9a4f218e87bd884fa8246a826be0111f495cfbec299a9222743
   seeds: the bench seeds (ph32.BS) and the bench bootstrap seed (ph32.BENCH['boot']), read from ph32 and not written out here; the development and evaluation seeds (ph32.SEEDS) are not used; p_D as ph32 sets it (0.03), unchanged
   seed scan: ph32's scan excludes by name ph32.py, ph32_*.txt, h27_*.md, master_plan.md, notes/*.md, viewer/* and the (file, number) pair of decision:seed-scan-exclusion-ph31-eval (experiments/h20/ph31_eval.txt); ph32b.py and this output are not excluded, so this text is checked against ph32.seed_numbers() before it is written

== (0) reproduction (nothing is measured unless every check holds) ==
   ph32.py sha256 equals the bench's (d9f585d5...2743): True; ph32_bench.txt sha256 equals the recorded (95721447...22f9): True
   ph32.bench() re-run as it is: 60 lines printed, ph32_bench.txt 60 lines; equal line for line 60/60 -> True
   headline numbers: T1D P(V) D on 0.787 True; D off 0.920 True; DP -0.1325 [-0.1675, -0.1000] True; W1D paired dwell -19.7825 True; lost 400 vs 22 True; (hH) DP +0.0000, M6 0.0000 True; (m) 122 True; stop rules (h), (hW), (hH) all STOP True
   == (m) T1 rows with V ever absent (no V whiff by step 58, or a V silence of 300 steps; Agent15 D off, reading R7): 122/400 (H26 eval's at-risk count 20 is the reference); of them no V whiff by 58: 103; first V whiff step 4/12/30 (rows 386)
   == (h) T1 on bench seeds, +1/0/0 400 x 600: Agent15 D on V 315 N 79 tie 6 P(V) 0.787 [0.745, 0.825]; Agent15 D off V 368 N 29 tie 3 P(V) 0.920 [0.889, 0.943]; Agent14N2 V 368 N 29 tie 3 P(V) 0.920 [0.889, 0.943]; Agent15g D on V 188 N 182 tie 30 P(V) 0.470 [0.422, 0.519]
   == (h) paired DP P(V) Agent15 D on - D off -0.1325 [-0.1675, -0.1000] (bootstrap 5000, seed <bench seed>); discordant b 0.1325, sd sqrt(b - DP^2) 0.3390; M2(b) pass probability 0.0000; M2(c) vs Agent15g at DP +0.3175 (b 0.3375): 1.0000; M2(a) reported, P(K >= 365 of 400) at P(V) 0.787: 0.0000; lost rows (no whiff of either plume in the last third) D on 90, D off 5
   == (h) STOP RULE (design section 4): M2(b) pass probability 0.0000 < 0.5 -> STOP
   == [W1 Agent15 D on] mean dwell within 3.0 of B over 600 steps 4.968 (quartiles 0/5/8); reach 221/400; lost rows 400; wall contacts per row 105.645
   == [W1 Agent15 D off] mean dwell within 3.0 of B over 600 steps 24.750 (quartiles 19/25/31); reach 392/400; lost rows 22; wall contacts per row 0.000
   == [W1 Agent14N2] mean dwell within 3.0 of B over 600 steps 24.750 (quartiles 19/25/31); reach 392/400; lost rows 22; wall contacts per row 0.000
   == [W1 hold-not-read D on] mean dwell within 3.0 of B over 600 steps 4.723 (quartiles 0/5/8); reach 221/400; lost rows 400; wall contacts per row 107.218
   == [W1 hold-not-read D off] mean dwell within 3.0 of B over 600 steps 24.750 (quartiles 19/25/31); reach 392/400; lost rows 22; wall contacts per row 0.000
   == [W1 release-off D on] mean dwell within 3.0 of B over 600 steps 5.263 (quartiles 0/5/9); reach 224/400; lost rows 400; wall contacts per row 103.265
   == [W1 Agent15g D on] mean dwell within 3.0 of B over 600 steps 3.493 (quartiles 0/0/7); reach 189/400; lost rows 400; wall contacts per row 115.743
   == (hW) measured: D_off (Agent15's mean W1 dwell without D) = 24.7500; rule bar_W = -0.20 x D_off rounded to 0.1 = -5.0 (reading R12); paired dwell D on - D off -19.7825 sd 10.1430 (bootstrap [-20.7626, -18.8275]); M5(b) pass probability 0.0000; lost rows DP D on - D off +0.9450 [+0.9225, +0.9675] (b 0.9450); M5(d) pass probability 0.0000; M5(a) reach 221/400 = 0.552 [0.504, 0.600]; M5(c) contacts per row 105.645
   == (hW) STOP RULE (design section 4): M5(b) 0.0000, M5(d) 0.0000 -> < 0.5 -> STOP
   == (hH) the hold's benefit: lost rows DP hold-not-read D on - Agent15 D on +0.0000 [+0.0000, +0.0000] (b 0.0000); M6 pass probability 0.0000; without D (hold-not-read D off - Agent15 D off) +0.0000
   == (hH) STOP RULE (design section 4): M6 pass probability 0.0000 < 0.5 -> STOP
   (D2) the nav law rebuilt from the recorded fields equals the recorded NAV on every (step, row): T1on True, T1off True, W1on True, W1off True, W1h True, W1r True

== (A1) what is held, and how holds end (D3) ==
   [T1D Agent15 D on] held (circuit H) fraction of (step, row), rows 400: none 0.540, V 0.212, B 0.020, D 0.228; steps 59-599: none 0.563, V 0.174, B 0.011, D 0.252; per row, fraction of steps with nothing held 0.16/0.47/0.55/0.62/0.92 (n 400)
      V holds: 951 in 324 rows (per row 0/2/3/3/5 (n 400)); length 2/48/49/60/94 (n 951); end: timeout (release) 878, evidence 0, other (neither flag) 1, row end 72; steps from the held odour's last whiff to the end: timeout 48/48/48/50/55 (n 878), evidence n/a, other (neither flag) 8/8/8/8/8 (n 1)
      B holds: 156 in 138 rows (per row 0/0/0/1/4 (n 400)); length 1/16/29/48/76 (n 156); end: timeout (release) 25, evidence 119, other (neither flag) 12, row end 0; steps from the held odour's last whiff to the end: timeout 48/48/48/51/55 (n 25), evidence 3/10/21/33/52 (n 119), other (neither flag) 1/13/16/18/21 (n 12)
      D holds: 842 in 356 rows (per row 0/1/2/3/5 (n 400)); length 1/40/52/82/394 (n 842); end: timeout (release) 331, evidence 375, other (neither flag) 22, row end 114; steps from the held odour's last whiff to the end: timeout 48/48/48/50/56 (n 331), evidence 1/11/19/31/53 (n 375), other (neither flag) 1/1/4/8/44 (n 22)
   [T1 Agent15 D off] held (circuit H) fraction of (step, row), rows 400: none 0.648, V 0.304, B 0.048, D 0.000; steps 59-599: none 0.688, V 0.276, B 0.036, D 0.000; per row, fraction of steps with nothing held 0.56/0.62/0.64/0.66/0.92 (n 400)
      V holds: 1435 in 386 rows (per row 0/3/4/4/5 (n 400)); length 1/48/48/54/94 (n 1435); end: timeout (release) 1295, evidence 0, other (neither flag) 0, row end 140; steps from the held odour's last whiff to the end: timeout 48/48/48/50/52 (n 1295), evidence n/a, other (neither flag) n/a
      B holds: 247 in 194 rows (per row 0/0/0/1/4 (n 400)); length 1/30/48/59/121 (n 247); end: timeout (release) 163, evidence 80, other (neither flag) 0, row end 4; steps from the held odour's last whiff to the end: timeout 48/48/48/50/56 (n 163), evidence 4/16/20/25/42 (n 80), other (neither flag) n/a
      D holds: none
   [W1D Agent15 D on] held (circuit H) fraction of (step, row), rows 400: none 0.566, V 0.000, B 0.036, D 0.398; steps 59-599: none 0.549, V 0.000, B 0.017, D 0.434; per row, fraction of steps with nothing held 0.14/0.44/0.56/0.70/1.00 (n 400)
      V holds: none
      B holds: 236 in 202 rows (per row 0/0/1/1/2 (n 400)); length 1/20/39/50/80 (n 236); end: timeout (release) 55, evidence 162, other (neither flag) 19, row end 0; steps from the held odour's last whiff to the end: timeout 48/48/48/51/56 (n 55), evidence 1/14/25/38/51 (n 162), other (neither flag) 3/16/16/18/21 (n 19)
      D holds: 1035 in 392 rows (per row 0/2/2/3/6 (n 400)); length 1/48/76/118/412 (n 1035); end: timeout (release) 798, evidence 15, other (neither flag) 24, row end 198; steps from the held odour's last whiff to the end: timeout 48/48/48/48/57 (n 798), evidence 3/6/8/14/20 (n 15), other (neither flag) 1/1/1/1/14 (n 24)
   [W1 Agent15 D off] held (circuit H) fraction of (step, row), rows 400: none 0.787, V 0.000, B 0.213, D 0.000; steps 59-599: none 0.798, V 0.000, B 0.202, D 0.000; per row, fraction of steps with nothing held 0.57/0.72/0.80/0.84/1.00 (n 400)
      V holds: none
      B holds: 998 in 392 rows (per row 0/2/3/3/5 (n 400)); length 2/48/48/57/86 (n 998); end: timeout (release) 915, evidence 0, other (neither flag) 0, row end 83; steps from the held odour's last whiff to the end: timeout 48/48/49/52/58 (n 915), evidence n/a, other (neither flag) n/a
      D holds: none
   [W1D release-off D on] held (circuit H) fraction of (step, row), rows 400: none 0.308, V 0.000, B 0.043, D 0.649; steps 59-599: none 0.262, V 0.000, B 0.025, D 0.713; per row, fraction of steps with nothing held 0.01/0.13/0.24/0.43/1.00 (n 400)
      V holds: none
      B holds: 235 in 194 rows (per row 0/0/0/1/3 (n 400)); length 1/18/37/63/190 (n 235); end: timeout (release) 6, evidence 205, other (neither flag) 24, row end 0; steps from the held odour's last whiff to the end: timeout 2/3/5/6/8 (n 6), evidence 1/17/31/51/171 (n 205), other (neither flag) 3/14/16/18/21 (n 24)
      D holds: 453 in 389 rows (per row 0/1/1/1/3 (n 400)); length 1/235/390/494/592 (n 453); end: timeout (release) 10, evidence 30, other (neither flag) 27, row end 386; steps from the held odour's last whiff to the end: timeout 3/4/6/8/14 (n 10), evidence 2/8/15/68/167 (n 30), other (neither flag) 3/6/9/12/17 (n 27)
   [T1D Agent15 D on, the 122 (m) rows] held (circuit H) fraction of (step, row), rows 122: none 0.546, V 0.064, B 0.055, D 0.335; steps 59-599: none 0.546, V 0.058, B 0.024, D 0.371; per row, fraction of steps with nothing held 0.16/0.46/0.54/0.65/0.92 (n 122)
      V holds: 95 in 46 rows (per row 0/0/0/2/4 (n 122)); length 4/48/48/52/84 (n 95); end: timeout (release) 87, evidence 0, other (neither flag) 0, row end 8; steps from the held odour's last whiff to the end: timeout 48/48/48/50/55 (n 87), evidence n/a, other (neither flag) n/a
      B holds: 111 in 95 rows (per row 0/1/1/1/4 (n 122)); length 1/20/37/52/76 (n 111); end: timeout (release) 25, evidence 74, other (neither flag) 12, row end 0; steps from the held odour's last whiff to the end: timeout 48/48/48/51/55 (n 25), evidence 3/13/24/37/48 (n 74), other (neither flag) 1/13/16/18/21 (n 12)
      D holds: 295 in 116 rows (per row 0/2/2/3/5 (n 122)); length 1/48/68/98/394 (n 295); end: timeout (release) 185, evidence 51, other (neither flag) 4, row end 55; steps from the held odour's last whiff to the end: timeout 48/48/48/48/56 (n 185), evidence 1/8/17/24/50 (n 51), other (neither flag) 1/1/1/1/1 (n 4)
   [T1 Agent15 D off, the 122 (m) rows] held (circuit H) fraction of (step, row), rows 122: none 0.661, V 0.214, B 0.125, D 0.000; steps 59-599: none 0.688, V 0.225, B 0.087, D 0.000; per row, fraction of steps with nothing held 0.58/0.62/0.64/0.68/0.92 (n 122)
      V holds: 336 in 108 rows (per row 0/2/3/4/4 (n 122)); length 2/48/48/52/84 (n 336); end: timeout (release) 286, evidence 0, other (neither flag) 0, row end 50; steps from the held odour's last whiff to the end: timeout 48/48/48/50/51 (n 286), evidence n/a, other (neither flag) n/a
      B holds: 161 in 114 rows (per row 0/1/1/1/4 (n 122)); length 5/48/54/65/121 (n 161); end: timeout (release) 156, evidence 3, other (neither flag) 0, row end 2; steps from the held odour's last whiff to the end: timeout 48/48/48/50/56 (n 156), evidence 7/12/16/16/17 (n 3), other (neither flag) n/a
      D holds: none

== (A2) nav events by source (D2), and the cast clock on D whiffs ==
   [T1D Agent15 D on] nav events, rows 400: 4899 (12.25 per row): held-hit 2256 (V 1669, B 2, D 585, two or more 0); nothing held 1960 (V 1184, B 12, D 763, two or more 1); non-top odour held 683 (V 683, B 0, D 0, two or more 0)
      D-driven (steering set {D} alone) 1348/4899 = 0.275 of nav events; rows with any 96/400; first D-driven nav step 59/77/92/118/591 (n 96); D-driven events with V present 0, with V absent 1348
      the cast clock `since` resets exactly on nav (SINCE == 0 iff NAV): True; D-whiff steps 7187, of them with nav (any driver; `since` reset) 1474/7187 = 0.205, with a D-driven nav 1348/7187 = 0.188
      D-whiff steps with nav (of them D-driven) / D-whiff steps, by state (read hold): V present, held none: 35 (0)/3029; V present, held V: 70 (0)/1562; V present, held B: 1 (0)/113; V present, held D: 19 (0)/1104; V absent, held none: 764 (763)/764; V absent, held B: 0 (0)/30; V absent, held D: 585 (585)/585
      B-whiff steps with V absent, steering (nav) / total, by read hold: held none: 13/13; held B: 2/2; (step, row) with V present and D in the top set 0
   [T1 Agent15 D off] nav events, rows 400: 4266 (10.66 per row): held-hit 2279 (V 2231, B 48, D 0, two or more 0); nothing held 1867 (V 1743, B 124, D 0, two or more 0); non-top odour held 120 (V 120, B 0, D 0, two or more 0)
      D-driven (steering set {D} alone) 0/4266 = 0.000 of nav events; rows with any 0/400; first D-driven nav step n/a; D-driven events with V present 0, with V absent 0
      the cast clock `since` resets exactly on nav (SINCE == 0 iff NAV): True; D-whiff steps 0, of them with nav (any driver; `since` reset) 0/0, with a D-driven nav 0/0
      D-whiff steps with nav (of them D-driven) / D-whiff steps, by state (read hold): none
      B-whiff steps with V absent, steering (nav) / total, by read hold: held none: 124/124; held B: 48/48; (step, row) with V present and D in the top set 0
   [W1D Agent15 D on] nav events, rows 400: 6677 (16.69 per row): held-hit 3001 (V 0, B 79, D 2922, two or more 0); nothing held 3676 (V 0, B 207, D 3459, two or more 10); non-top odour held 0 (V 0, B 0, D 0, two or more 0)
      D-driven (steering set {D} alone) 6381/6677 = 0.956 of nav events; rows with any 400/400; first D-driven nav step 59/72/88/112/294 (n 400); D-driven events with V present 0, with V absent 6381
      the cast clock `since` resets exactly on nav (SINCE == 0 iff NAV): True; D-whiff steps 7187, of them with nav (any driver; `since` reset) 6393/7187 = 0.890, with a D-driven nav 6381/7187 = 0.888
      D-whiff steps with nav (of them D-driven) / D-whiff steps, by state (read hold): V present, held none: 0 (0)/511; V present, held B: 0 (0)/149; V present, held D: 0 (0)/48; V absent, held none: 3469 (3459)/3469; V absent, held B: 2 (0)/88; V absent, held D: 2922 (2922)/2922
      B-whiff steps with V absent, steering (nav) / total, by read hold: held none: 217/217; held B: 79/79; held D: 0/1; (step, row) with V present and D in the top set 0
   [W1 Agent15 D off] nav events, rows 400: 3565 (8.91 per row): held-hit 956 (V 0, B 956, D 0, two or more 0); nothing held 2609 (V 0, B 2609, D 0, two or more 0); non-top odour held 0 (V 0, B 0, D 0, two or more 0)
      D-driven (steering set {D} alone) 0/3565 = 0.000 of nav events; rows with any 0/400; first D-driven nav step n/a; D-driven events with V present 0, with V absent 0
      the cast clock `since` resets exactly on nav (SINCE == 0 iff NAV): True; D-whiff steps 0, of them with nav (any driver; `since` reset) 0/0, with a D-driven nav 0/0
      D-whiff steps with nav (of them D-driven) / D-whiff steps, by state (read hold): none
      B-whiff steps with V absent, steering (nav) / total, by read hold: held none: 2609/2609; held B: 956/956; (step, row) with V present and D in the top set 0
   [W1D hold-not-read D on (read hold HR)] nav events, rows 400: 6712 (16.78 per row): held-hit 6712 (V 0, B 244, D 6468, two or more 0); nothing held 0 (V 0, B 0, D 0, two or more 0); non-top odour held 0 (V 0, B 0, D 0, two or more 0)
      D-driven (steering set {D} alone) 6468/6712 = 0.964 of nav events; rows with any 400/400; first D-driven nav step 59/69/82/105/294 (n 400); D-driven events with V present 0, with V absent 6468
      the cast clock `since` resets exactly on nav (SINCE == 0 iff NAV): True; D-whiff steps 7187, of them with nav (any driver; `since` reset) 6479/7187 = 0.901, with a D-driven nav 6468/7187 = 0.900
      D-whiff steps with nav (of them D-driven) / D-whiff steps, by state (read hold): V present, held B: 0 (0)/39; V present, held D: 0 (0)/669; V absent, held B: 11 (0)/11; V absent, held D: 6468 (6468)/6468
      B-whiff steps with V absent, steering (nav) / total, by read hold: held B: 244/244; (step, row) with V present and D in the top set 0
   [W1D release-off D on] nav events, rows 400: 6664 (16.66 per row): held-hit 4799 (V 0, B 104, D 4695, two or more 0); nothing held 1865 (V 0, B 224, D 1632, two or more 9); non-top odour held 0 (V 0, B 0, D 0, two or more 0)
      D-driven (steering set {D} alone) 6327/6664 = 0.949 of nav events; rows with any 400/400; first D-driven nav step 59/72/88/120/330 (n 400); D-driven events with V present 0, with V absent 6327
      the cast clock `since` resets exactly on nav (SINCE == 0 iff NAV): True; D-whiff steps 7187, of them with nav (any driver; `since` reset) 6341/7187 = 0.882, with a D-driven nav 6327/7187 = 0.880
      D-whiff steps with nav (of them D-driven) / D-whiff steps, by state (read hold): V present, held none: 0 (0)/516; V present, held B: 0 (0)/147; V present, held D: 0 (0)/45; V absent, held none: 1641 (1632)/1641; V absent, held B: 5 (0)/143; V absent, held D: 4695 (4695)/4695
      B-whiff steps with V absent, steering (nav) / total, by read hold: held none: 233/233; held B: 104/104; held D: 1/35; (step, row) with V present and D in the top set 0
   [T1D Agent15 D on, the 122 (m) rows] nav events, rows 122: 1676 (13.74 per row): held-hit 706 (V 119, B 2, D 585, two or more 0); nothing held 903 (V 127, B 12, D 763, two or more 1); non-top odour held 67 (V 67, B 0, D 0, two or more 0)
      D-driven (steering set {D} alone) 1348/1676 = 0.804 of nav events; rows with any 96/122; first D-driven nav step 59/77/92/118/591 (n 96); D-driven events with V present 0, with V absent 1348
      the cast clock `since` resets exactly on nav (SINCE == 0 iff NAV): True; D-whiff steps 2201, of them with nav (any driver; `since` reset) 1359/2201 = 0.617, with a D-driven nav 1348/2201 = 0.612
      D-whiff steps with nav (of them D-driven) / D-whiff steps, by state (read hold): V present, held none: 4 (0)/424; V present, held V: 5 (0)/146; V present, held B: 0 (0)/88; V present, held D: 1 (0)/164; V absent, held none: 764 (763)/764; V absent, held B: 0 (0)/30; V absent, held D: 585 (585)/585
      B-whiff steps with V absent, steering (nav) / total, by read hold: held none: 13/13; held B: 2/2; (step, row) with V present and D in the top set 0
   [T1D Agent15 D on, the 278 V-always-present rows] nav events, rows 278: 3223 (11.59 per row): held-hit 1550 (V 1550, B 0, D 0, two or more 0); nothing held 1057 (V 1057, B 0, D 0, two or more 0); non-top odour held 616 (V 616, B 0, D 0, two or more 0)
      D-driven (steering set {D} alone) 0/3223 = 0.000 of nav events; rows with any 0/278; first D-driven nav step n/a; D-driven events with V present 0, with V absent 0
      the cast clock `since` resets exactly on nav (SINCE == 0 iff NAV): True; D-whiff steps 4986, of them with nav (any driver; `since` reset) 115/4986 = 0.023, with a D-driven nav 0/4986 = 0.000
      D-whiff steps with nav (of them D-driven) / D-whiff steps, by state (read hold): V present, held none: 31 (0)/2605; V present, held V: 65 (0)/1416; V present, held B: 1 (0)/25; V present, held D: 18 (0)/940
      B-whiff steps with V absent, steering (nav) / total, by read hold: none; (step, row) with V present and D in the top set 0

== (A3) presence by the counters and the filter's top set ==
   [T1D Agent15 D on] present by counter or hold, fraction of (step, row): V 0.808, B 0.523, D 0.990; steps 59-599: V 0.787, B 0.471, D 0.989; rows with V absent on some step 122
      top set, all (step, row): {V} 0.808, {B, D} 0.105, {B} 0.002, {D} 0.084, D in top 0.190; steps with nothing read as held 0.540, of them D in top 0.192, V in top 0.806
   [T1 Agent15 D off] present by counter or hold, fraction of (step, row): V 0.926, B 0.542, D 0.098; steps 59-599: V 0.918, B 0.492, D 0.000; rows with V absent on some step 122
      top set, all (step, row): {V} 0.926, {B, D} 0.000, {B} 0.072, {D} 0.000, D in top 0.000; steps with nothing read as held 0.648, of them D in top 0.000, V in top 0.915
   [W1D Agent15 D on] present by counter or hold, fraction of (step, row): V 0.098, B 0.471, D 0.990; steps 59-599: V 0.000, B 0.413, D 0.989; rows with V absent on some step 400
      top set, all (step, row): {V} 0.098, {B, D} 0.366, {B} 0.007, {D} 0.526, D in top 0.892; steps with nothing read as held 0.566, of them D in top 0.862, V in top 0.126
   [W1 Agent15 D off] present by counter or hold, fraction of (step, row): V 0.098, B 0.935, D 0.098; steps 59-599: V 0.000, B 0.928, D 0.000; rows with V absent on some step 400
      top set, all (step, row): {V} 0.098, {B, D} 0.000, {B} 0.837, {D} 0.000, D in top 0.000; steps with nothing read as held 0.787, of them D in top 0.000, V in top 0.086
   [T1D Agent15 D on, the 122 (m) rows] present by counter or hold, fraction of (step, row): V 0.370, B 0.608, D 0.988; steps 59-599: V 0.301, B 0.566, D 0.987; rows with V absent on some step 122
      top set, all (step, row): {V} 0.370, {B, D} 0.345, {B} 0.008, {D} 0.277, D in top 0.622; steps with nothing read as held 0.546, of them D in top 0.624, V in top 0.370

== (A4) trajectory consequence (first D event = first D hold or first D-driven nav, D-on run; D4, D5) ==
   [T1D rows out of V (V in D off, not V in D on)] rows 53: rows with a D event 53 (first a D hold 6, first a D-driven nav 47, same step 0); first D event step 9/65/79/91/108 (n 53); first step at which D on and D off positions differ 59/72/83/93/110 (n 53) (rows never differing 0); divergence at or after the first D event 53
      at the first D event: d_along -10.9/-8.9/-8.2/-6.2/14.7 (n 53) (upwind of the sources' line, d_along < 0: 48/53); d_cross to the V axis 0.4/4.4/6.7/10.3/14.3 (n 53), to the B axis 0.0/1.5/3.5/7.5/15.4 (n 53); inside a whiff region 5/53; upwind displacement over the next 20 steps 2.5/11.6/11.9/12.1/12.4 (n 53); steps to leaving the along range 0-25 0/0/0/0/27 (n 53); steps to the first wall contact 108/119/130/168/448 (n 53) (rows with a contact after it 53)
      at the first D-driven nav (rows 53): D held 1, nothing held 52; with nothing held, the last hold before it: B hold ended by evidence 30, B hold ended by other 4, B hold ended by timeout 10, D hold ended by evidence 2, no earlier hold 6
      end state at 599, D on: at V 0, at B 0, at a wall 42, upwind of both 11, in the along range 0, downwind beyond 25 0
      end state at 599, D off: at V 5, at B 0, at a wall 0, upwind of both 42, in the along range 6, downwind beyond 25 0
      wall contacts D on 5662 (upwind x 0 5626, downwind x 160 0, y 0 22, y 160 14), rows with any 53, first contact step 179/195/203/250/535 (n 53); D off 0, rows with any 0
   [T1D rows lost in D on (no whiff of either plume on 400-599)] rows 90: rows with a D event 90 (first a D hold 16, first a D-driven nav 74, same step 0); first D event step 9/73/87/101/446 (n 90); first step at which D on and D off positions differ 59/77/92/107/591 (n 89) (rows never differing 1); divergence at or after the first D event 89
      at the first D event: d_along -39.6/-9.7/-7.9/-5.1/39.2 (n 90) (upwind of the sources' line, d_along < 0: 80/90); d_cross to the V axis 0.2/3.9/6.6/10.4/14.3 (n 90), to the B axis 0.0/1.5/3.7/7.5/17.9 (n 90); inside a whiff region 6/90; upwind displacement over the next 20 steps -11.9/11.3/11.8/12.1/12.4 (n 90); steps to leaving the along range 0-25 0/0/0/0/105 (n 90); steps to the first wall contact 52/116/127/174/448 (n 86) (rows with a contact after it 86)
      at the first D-driven nav (rows 89): D held 1, nothing held 88; with nothing held, the last hold before it: B hold ended by evidence 45, B hold ended by other 6, B hold ended by timeout 15, D hold ended by evidence 5, D hold ended by other 1, D hold ended by timeout 4, V hold ended by timeout 1, no earlier hold 11
      end state at 599, D on: at V 0, at B 0, at a wall 69, upwind of both 21, in the along range 0, downwind beyond 25 0
      end state at 599, D off: at V 6, at B 0, at a wall 0, upwind of both 72, in the along range 12, downwind beyond 25 0
      wall contacts D on 8816 (upwind x 0 8765, downwind x 160 0, y 0 27, y 160 24), rows with any 86, first contact step 172/198/223/266/535 (n 86); D off 0, rows with any 0
   [T1D the 122 (m) rows] rows 122: rows with a D event 120 (first a D hold 43, first a D-driven nav 77, same step 0); first D event step 9/77/96/201/548 (n 120); first step at which D on and D off positions differ 59/77/92/118/591 (n 96) (rows never differing 26); divergence at or after the first D event 96
      at the first D event: d_along -39.6/-17.5/-8.8/-5.8/39.2 (n 120) (upwind of the sources' line, d_along < 0: 106/120); d_cross to the V axis 0.2/3.4/5.8/9.4/14.3 (n 120), to the B axis 0.0/2.3/4.6/10.7/19.3 (n 120); inside a whiff region 8/120; upwind displacement over the next 20 steps -11.9/-0.7/11.6/12.0/12.4 (n 120); steps to leaving the along range 0-25 0/0/0/0/105 (n 120); steps to the first wall contact 52/116/127/187/448 (n 89) (rows with a contact after it 89)
      at the first D-driven nav (rows 96): D held 1, nothing held 95; with nothing held, the last hold before it: B hold ended by evidence 47, B hold ended by other 6, B hold ended by timeout 18, D hold ended by evidence 7, D hold ended by other 1, D hold ended by timeout 4, V hold ended by timeout 1, no earlier hold 11
      end state at 599, D on: at V 0, at B 0, at a wall 72, upwind of both 46, in the along range 4, downwind beyond 25 0
      end state at 599, D off: at V 7, at B 0, at a wall 0, upwind of both 99, in the along range 16, downwind beyond 25 0
      wall contacts D on 8828 (upwind x 0 8777, downwind x 160 0, y 0 27, y 160 24), rows with any 89, first contact step 172/198/226/303/591 (n 89); D off 0, rows with any 0
   [T1D the 278 V-always-present rows] rows 278: rows with a D event 240 (first a D hold 240, first a D-driven nav 0, same step 0); first D event step 8/119/192/338/582 (n 240); first step at which D on and D off positions differ n/a (rows never differing 278); divergence at or after the first D event 0
      at the first D event: d_along -33.6/-30.4/-23.2/-12.2/16.6 (n 240) (upwind of the sources' line, d_along < 0: 226/240); d_cross to the V axis 0.0/1.6/3.3/5.4/13.1 (n 240), to the B axis 0.2/5.3/8.5/11.7/17.8 (n 240); inside a whiff region 15/240; upwind displacement over the next 20 steps -12.0/-9.7/-6.0/-3.1/12.5 (n 240); steps to leaving the along range 0-25 0/0/0/0/98 (n 240); steps to the first wall contact n/a (rows with a contact after it 0)
      at the first D-driven nav (rows 0): D held 0, nothing held 0; with nothing held, the last hold before it: 
      end state at 599, D on: at V 19, at B 2, at a wall 0, upwind of both 235, in the along range 22, downwind beyond 25 0
      end state at 599, D off: at V 19, at B 2, at a wall 0, upwind of both 235, in the along range 22, downwind beyond 25 0
      wall contacts D on 0 (upwind x 0 0, downwind x 160 0, y 0 0, y 160 0), rows with any 0, first contact step n/a; D off 0, rows with any 0
   [W1D all rows (every row lost)] rows 400: rows with a D event 400 (first a D hold 77, first a D-driven nav 323, same step 0); first D event step 8/63/80/105/294 (n 400); first step at which D on and D off positions differ 59/72/88/112/294 (n 400) (rows never differing 0); divergence at or after the first D event 400
      at the first D event: d_along -32.7/-9.1/-6.9/-0.8/39.2 (n 400) (upwind of the sources' line, d_along < 0: 303/400); d_cross to the V axis 0.0/2.8/5.6/9.6/16.8 (n 400), to the B axis 0.0/2.1/4.6/8.0/16.7 (n 400); inside a whiff region 93/400; upwind displacement over the next 20 steps 2.2/11.2/11.8/12.1/12.5 (n 400); steps to leaving the along range 0-25 0/0/0/0/38 (n 400); steps to the first wall contact 63/116/134/172/475 (n 399) (rows with a contact after it 399)
      at the first D-driven nav (rows 400): D held 37, nothing held 363; with nothing held, the last hold before it: B hold ended by evidence 133, B hold ended by other 15, B hold ended by timeout 45, D hold ended by evidence 7, D hold ended by timeout 19, no earlier hold 144
      end state at 599, D on: at V 0, at B 0, at a wall 303, upwind of both 97, in the along range 0, downwind beyond 25 0
      end state at 599, D off: at V 0, at B 22, at a wall 0, upwind of both 332, in the along range 46, downwind beyond 25 0
      wall contacts D on 42258 (upwind x 0 42057, downwind x 160 0, y 0 122, y 160 79), rows with any 399, first contact step 164/193/225/265/585 (n 399); D off 0, rows with any 0

== (A5) W1D surge accounting (D6) ==
   [W1D Agent15 D on] surges (nav True) per row, mean (rows with any): B hit with B held 0.20 (21); D hit with D held 7.30 (375); B whiff, nothing held 0.52 (79); D whiff, nothing held 8.65 (400); non-top odour held 0.00; two or more odours steering 0.03
      upwind displacement on the surge step itself (max 0.6): B-driven -0.46/0.55/0.60/0.60/0.60 (n 286), D-driven -0.59/-0.09/0.20/0.55/0.60 (n 6381)
      upwind displacement per row by the segment's driver (from a nav event to the next; D6), mean [quartiles]: before any nav (cast) 23.6 [-19.2/21.3/27.0/28.9/31.0 (n 400)]; V-driven 0.0; B-driven 5.1 [-0.1/0.0/0.0/0.0/55.4 (n 400)]; D-driven 59.6 [4.0/58.3/61.7/64.4/109.3 (n 400)]; two or more 0.1; total 88.3
      per D-driven segment (6381): upwind displacement -50.6/-0.1/0.4/5.4/31.9 (n 6381), mean 3.73; length in steps 1/9/22/43/272 (n 6381); the 2055 segments starting before the row's first wall contact: upwind displacement -46.6/4.1/9.9/18.5/31.9 (n 2055), mean 11.61, per step 0.353
      target heading with a downwind component (|target - upwind| > 90), steps 59-599: 0.115; target within 40 of upwind 0.630; `since` on nothing-held steps 59-599 quartiles 0/12/36/68/271 (n 118866)
   [W1 Agent15 D off] surges (nav True) per row, mean (rows with any): B hit with B held 2.39 (256); D hit with D held 0.00 (0); B whiff, nothing held 6.52 (394); D whiff, nothing held 0.00 (0); non-top odour held 0.00; two or more odours steering 0.00
      upwind displacement on the surge step itself (max 0.6): B-driven -0.56/-0.10/0.58/0.60/0.60 (n 3565), D-driven n/a
      upwind displacement per row by the segment's driver (from a nav event to the next; D6), mean [quartiles]: before any nav (cast) 11.4 [-5.0/1.7/15.5/20.0/40.4 (n 400)]; V-driven 0.0; B-driven 20.7 [-19.8/8.5/19.9/33.2/57.5 (n 400)]; D-driven 0.0 [0.0/0.0/0.0/0.0/0.0 (n 400)]; two or more 0.0; total 32.1
      target heading with a downwind component (|target - upwind| > 90), steps 59-599: 0.499; target within 40 of upwind 0.243; `since` on nothing-held steps 59-599 quartiles 0/66/100/136/600 (n 172584)
   [W1D hold-not-read D on] surges (nav True) per row, mean (rows with any): B hit with B held 0.61 (67); D hit with D held 16.17 (400); B whiff, nothing held 0.00 (0); D whiff, nothing held 0.00 (0); non-top odour held 0.00; two or more odours steering 0.00
      upwind displacement on the surge step itself (max 0.6): B-driven -0.46/0.33/0.59/0.60/0.60 (n 244), D-driven -0.60/-0.09/0.21/0.55/0.60 (n 6468)
      upwind displacement per row by the segment's driver (from a nav event to the next; D6), mean [quartiles]: before any nav (cast) 24.6 [-19.2/22.6/27.7/29.1/31.0 (n 400)]; V-driven 0.0; B-driven 3.6 [0.0/0.0/0.0/0.0/55.4 (n 400)]; D-driven 60.2 [15.0/58.8/61.7/64.4/109.3 (n 400)]; two or more 0.0; total 88.3
      per D-driven segment (6468): upwind displacement -50.6/-0.1/0.4/5.4/31.9 (n 6468), mean 3.72; length in steps 1/9/22/43/272 (n 6468); the 2066 segments starting before the row's first wall contact: upwind displacement -46.6/4.1/9.9/18.5/31.9 (n 2066), mean 11.65, per step 0.351
      target heading with a downwind component (|target - upwind| > 90), steps 59-599: 0.109; target within 40 of upwind 0.635; `since` on nothing-held steps 59-599 quartiles 11/20/34/61/271 (n 153698)
   [W1D release-off D on] surges (nav True) per row, mean (rows with any): B hit with B held 0.26 (29); D hit with D held 11.74 (383); B whiff, nothing held 0.56 (82); D whiff, nothing held 4.08 (353); non-top odour held 0.00; two or more odours steering 0.02
      upwind displacement on the surge step itself (max 0.6): B-driven -0.46/0.56/0.60/0.60/0.60 (n 328), D-driven -0.59/-0.10/0.20/0.56/0.60 (n 6327)
      upwind displacement per row by the segment's driver (from a nav event to the next; D6), mean [quartiles]: before any nav (cast) 22.4 [-19.2/20.2/26.8/28.9/31.0 (n 400)]; V-driven 0.0; B-driven 5.2 [0.0/0.0/0.0/0.0/55.1 (n 400)]; D-driven 60.6 [15.0/58.5/61.8/64.7/109.3 (n 400)]; two or more 0.1; total 88.3
      per D-driven segment (6327): upwind displacement -50.6/-0.1/0.4/5.8/31.9 (n 6327), mean 3.83; length in steps 1/9/22/43/272 (n 6327); the 2095 segments starting before the row's first wall contact: upwind displacement -46.6/4.1/9.9/18.5/31.9 (n 2095), mean 11.61, per step 0.356
      target heading with a downwind component (|target - upwind| > 90), steps 59-599: 0.121; target within 40 of upwind 0.626; `since` on nothing-held steps 59-599 quartiles 0/11/30/67/251 (n 56664)
   [W1D Agent15 D on] final upwind exit (after it d_along < -3 to the end), rows 400/400; exit step 42/44/46/114/293 (n 400); driver of the segment at the exit: cast (no nav yet) 268, V 0, B 73, D 57, two or more 2
      first upwind pass (d_along < -3): rows 400, step 42/44/45/46/52 (n 400); of them back downwind of the sources' line (d_along >= 0) later 83; most upwind d_along -74.0/-72.5/-70.9/-69.2/-64.1 (n 400); upwind displacement after the first pass, mean per row by segment driver: cast (no nav yet) 0.7, V 0.0, B 5.1, D 59.6, two or more 0.1
      last B whiff step 0/28/36/103/292 (n 303) (rows with none 97); exit minus last B whiff 0/4/11/40/254 (n 303)
   [W1 Agent15 D off] final upwind exit (after it d_along < -3 to the end), rows 323/400; exit step 448/486/541/583/599 (n 323); driver of the segment at the exit: cast (no nav yet) 6, V 0, B 317, D 0, two or more 0
      first upwind pass (d_along < -3): rows 400, step 42/44/45/46/52 (n 400); of them back downwind of the sources' line (d_along >= 0) later 383; most upwind d_along -39.5/-33.2/-32.6/-31.9/-11.7 (n 400); upwind displacement after the first pass, mean per row by segment driver: cast (no nav yet) -11.5, V 0.0, B 20.7, D 0.0, two or more 0.0
      last B whiff step 27/462/506/580/599 (n 399) (rows with none 1); exit minus last B whiff 0/1/3/5/549 (n 322)
   [T1D Agent15 D on, rows out of V] surges (nav True) per row, mean (rows with any): B hit with B held 0.04 (1); D hit with D held 7.13 (51); B whiff, nothing held 0.06 (2); D whiff, nothing held 9.30 (53); non-top odour held 0.00; two or more odours steering 0.02
      upwind displacement on the surge step itself (max 0.6): B-driven -0.15/-0.01/0.56/0.60/0.60 (n 5), D-driven -0.59/-0.14/0.16/0.55/0.60 (n 871)
      upwind displacement per row by the segment's driver (from a nav event to the next; D6), mean [quartiles]: before any nav (cast) 27.7 [21.3/26.6/28.3/29.2/30.9 (n 53)]; V-driven 0.0; B-driven 0.4 [-0.1/0.0/0.0/0.0/23.1 (n 53)]; D-driven 61.3 [25.4/60.3/61.8/64.0/69.4 (n 53)]; two or more 0.0; total 89.4
      per D-driven segment (871): upwind displacement -47.8/-0.1/0.3/5.4/30.7 (n 871), mean 3.73; length in steps 1/9/22/42/200 (n 871); the 264 segments starting before the row's first wall contact: upwind displacement -23.8/4.8/11.6/18.6/30.7 (n 264), mean 12.07, per step 0.323
      target heading with a downwind component (|target - upwind| > 90), steps 59-599: 0.109; target within 40 of upwind 0.636; `since` on nothing-held steps 59-599 quartiles 0/11/35/67/199 (n 15397)
   [T1 Agent15 D off, the same rows] surges (nav True) per row, mean (rows with any): B hit with B held 0.00 (0); D hit with D held 0.00 (0); B whiff, nothing held 0.04 (1); D whiff, nothing held 0.00 (0); non-top odour held 0.00; two or more odours steering 0.00
      upwind displacement on the surge step itself (max 0.6): B-driven -0.06/0.08/0.23/0.37/0.52 (n 2), D-driven n/a
      upwind displacement per row by the segment's driver (from a nav event to the next; D6), mean [quartiles]: before any nav (cast) 19.5 [15.1/18.8/19.7/20.7/22.0 (n 53)]; V-driven 11.1; B-driven -0.1 [-6.6/0.0/0.0/0.0/0.0 (n 53)]; D-driven 0.0 [0.0/0.0/0.0/0.0/0.0 (n 53)]; two or more 0.0; total 30.5
      target heading with a downwind component (|target - upwind| > 90), steps 59-599: 0.499; target within 40 of upwind 0.237; `since` on nothing-held steps 59-599 quartiles 0/76/100/127/451 (n 18969)

== (B) the (m) rows (D7) ==
(B1) (m) rows, V absent by its counter on some step of the Agent15 D-off run (reading R7): 122/400; 'prior' (no V whiff on 0-58) 103, first absent step 59/59/59/59/59 (n 103); 'silence' (300 steps after a V whiff) 19, first absent step 300/318/338/490/578 (n 19)
      H26's at-risk definition (ph28 reading R3: no V whiff on 0-58 and a B whiff with nothing or B held on a step from 59 to the first V whiff) applied to this D-off run: 21 rows (literal reading from step 0: 103); of them in (m) 21
      first V whiff step (D off) 0/4/12/30/576 (n 386); rows with none by step 58 103, by 118 31, never 14
      [prior, 103] at ta (D off): held B 96, nothing held 7; position at a wall 0, upwind of both sources (d_along < 0) 103, in the along range 0, downwind beyond 25 0; d_along -8.1/-7.2/-6.8/-6.0/-4.0 (n 103); distance to V 4.6/6.7/7.7/8.1/16.9 (n 103), to B 7.4/13.5/14.8/15.6/17.0 (n 103); in the window before ta: B whiffs in 101 rows, a B hold in 96, within 3.0 of B in 96; held fraction B 0.555, nothing 0.445
      [silence, 19] at ta (D off): held B 7, nothing held 12; position at a wall 0, upwind of both sources (d_along < 0) 18, in the along range 1, downwind beyond 25 0; d_along -24.4/-18.8/-17.0/-8.4/0.8 (n 19); distance to V 5.4/11.3/18.3/19.5/24.7 (n 19), to B 0.3/8.8/17.3/21.4/25.9 (n 19); in the window before ta: B whiffs in 16 rows, a B hold in 15, within 3.0 of B in 5; held fraction B 0.210, nothing 0.639
      [silence] last V whiff before ta 0/18/38/190/278 (n 19); ta - last V whiff 300/300/300/300/300 (n 19)
(B2) the same rows in the Agent15 D-on run: V ever absent there 122/122 (all rows 122; absent in D on only 0, in D off only 0); first absent step equal in D on and D off 122
      the first D event at or after ta and before the next V whiff, D-on run (event-based, exclusive, in this order; out-of-V rows in brackets): (i) a D hold (held at ta 1, or forming first) 2 [1]; (ii) a D-driven nav 93 [52]; (v) neither before the next V whiff or the row's end 27 [0]
      steps from ta to that first D event 0/13/27/39/183 (n 95); steps from ta to the next V whiff in D on 51/53/54/58/154 (n 28) (rows with none 94); in D off 48/54/56/59/517 (n 96) (rows with none 26)
      D on, held at ta: none 66, B 55, D 1; the B hold held at ta ends by (D on): evidence 32, other 1, timeout 22; in the out-of-V rows: evidence 16, timeout 10; (D off: timeout 103); rows whose first D event comes at or after that B hold's end 42 (out of V 26)
      table, rows (out of V): mechanism of the D-off absence x held at ta (D off) x the D-on event class:
         (iv) prior expiry, (iii) B held at ta: 96 (49): (i) 1 (1), (ii) 70 (48), (v) 25 (0)
         (iv) prior expiry, nothing held at ta: 7 (4): (i) 0 (0), (ii) 6 (4), (v) 1 (0)
         silence after a V whiff, (iii) B held at ta: 7 (0): (i) 0 (0), (ii) 7 (0), (v) 0 (0)
         silence after a V whiff, nothing held at ta: 12 (0): (i) 1 (0), (ii) 10 (0), (v) 1 (0)
      by mechanism of the D-off absence: prior 103 (out of V 53), silence 19 (out of V 0); out of V overall 53 (all in (m): True), into V 0
      outcome V/B/tie of the 122 rows: D on 42/76/4, D off 95/26/1

== (C) the W1D loss paths, four arms (and Agent15g beside) ==
   [W1 Agent15 D on] lost rows 400/400; last B whiff step 0/28/36/103/292 (n 303) (rows with none 97); reach within 3.0 of B 221/400, first arrival 29/30/31/35/262 (n 221), last step within 3.0 33/36/39/118/292 (n 221); dwell within 3.0 0/0/5/8/22 (n 400) (mean 4.968); dwell of reaching rows 1/7/8/10/22 (n 221)
      end state at 599: at V 0, at B 0, at a wall 303, upwind of both 97, in the along range 0, downwind beyond 25 0; wall contacts 42258 (105.645 per row): upwind x 0 42057, downwind x 160 0, y 0 122, y 160 79; rows with any 399, first contact step 164/193/225/265/585 (n 399)
   [W1 hold-not-read D on] lost rows 400/400; last B whiff step 0/28/36/44/292 (n 303) (rows with none 97); reach within 3.0 of B 221/400, first arrival 29/30/31/35/262 (n 221), last step within 3.0 33/36/39/114/292 (n 221); dwell within 3.0 0/0/5/8/20 (n 400) (mean 4.723); dwell of reaching rows 1/7/8/9/20 (n 221)
      end state at 599: at V 0, at B 0, at a wall 302, upwind of both 98, in the along range 0, downwind beyond 25 0; wall contacts 42887 (107.218 per row): upwind x 0 42673, downwind x 160 0, y 0 127, y 160 87; rows with any 399, first contact step 164/190/218/257/529 (n 399)
   [W1 release-off D on] lost rows 400/400; last B whiff step 0/29/36/114/292 (n 303) (rows with none 97); reach within 3.0 of B 224/400, first arrival 29/30/31/41/262 (n 224), last step within 3.0 33/36/40/123/292 (n 224); dwell within 3.0 0/0/5/9/22 (n 400) (mean 5.263); dwell of reaching rows 1/7/8/11/22 (n 224)
      end state at 599: at V 0, at B 0, at a wall 302, upwind of both 98, in the along range 0, downwind beyond 25 0; wall contacts 41306 (103.265 per row): upwind x 0 41102, downwind x 160 0, y 0 121, y 160 83; rows with any 398, first contact step 164/193/227/281/585 (n 398)
   [W1 Agent15 D off] lost rows 22/400; last B whiff step 27/462/506/580/599 (n 399) (rows with none 1); reach within 3.0 of B 392/400, first arrival 29/30/108/112/561 (n 392), last step within 3.0 33/465/508/582/599 (n 392); dwell within 3.0 0/19/25/31/60 (n 400) (mean 24.750); dwell of reaching rows 4/20/26/31/60 (n 392)
      end state at 599: at V 0, at B 22, at a wall 0, upwind of both 332, in the along range 46, downwind beyond 25 0; wall contacts 0 (0.000 per row): upwind x 0 0, downwind x 160 0, y 0 0, y 160 0; rows with any 0, first contact step n/a
   [W1 Agent15g D on] lost rows 400/400; last B whiff step 0/11/35/38/312 (n 285) (rows with none 115); reach within 3.0 of B 189/400, first arrival 29/30/31/32/219 (n 189), last step within 3.0 33/36/38/39/314 (n 189); dwell within 3.0 0/0/0/7/19 (n 400) (mean 3.493); dwell of reaching rows 1/6/7/9/19 (n 189)
      end state at 599: at V 0, at B 0, at a wall 304, upwind of both 96, in the along range 0, downwind beyond 25 0; wall contacts 46297 (115.743 per row): upwind x 0 46045, downwind x 160 0, y 0 148, y 160 104; rows with any 400, first contact step 153/169/181/216/502 (n 400)
   [W1 Agent15 D on vs hold-not-read D on] rows with identical positions on all 600 steps 326/400; first differing step 60/69/78/132/274 (n 74); lost in both 400, Agent15 only 0, hold-not-read D on only 0; last B whiff step equal 290/303, difference (hold-not-read D on - Agent15) -225/0/0/0/0 (n 303); first wall contact step difference -406/0/0/0/41 (n 399) (rows with a contact in both 399); same end state 385
   [W1 Agent15 D on vs release-off D on] rows with identical positions on all 600 steps 331/400; first differing step 60/101/115/176/360 (n 69); lost in both 400, Agent15 only 0, release-off D on only 0; last B whiff step equal 271/303, difference (release-off D on - Agent15) -123/0/0/0/248 (n 303); first wall contact step difference -71/0/0/0/184 (n 398) (rows with a contact in both 398); same end state 391
   [W1 Agent15 D on vs Agent15 D off] rows with identical positions on all 600 steps 0/400; first differing step 59/72/88/112/294 (n 400); lost in both 22, Agent15 only 378, Agent15 D off only 0; last B whiff step equal 4/303, difference (Agent15 D off - Agent15) -153/412/448/514/593 (n 303); first wall contact step difference n/a (rows with a contact in both 0); same end state 80
   [W1 hold-not-read D on] steps on which the read argmax HR differs from the circuit's hold H 0.438; HR fraction none/V/B/D 0.692, 0.000, 0.031, 0.277

== end: measurement only; no rule, parameter, bar or arm changed; bench seeds only; H27's verdict (stopped at the bench) unchanged ==
```
