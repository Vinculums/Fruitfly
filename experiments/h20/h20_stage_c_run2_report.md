# H20 Stage C Run 2 report: the adopted agent with learning on in the H15 Run 2 world, M4(c)'s readability read on G3+

Date 2026-09-25. Design v2 FINAL doc d007990ab333e7194 (experiments/h20/h20_stage_c_run2_design_v2.md, sha256 48fdd1f30952a376fce85fba355645635d08ef37db772b59fe24588f7ac2e4f2, equal to the Vinc content_hash and to the hash cited in decision:h20-stage-c-run2-open), opened by the owner's standing instruction of 2026-09-25, verbatim '다음도 권고안에 따라 작업 진행' (gloss: 'proceed with the next work too, according to the recommended option'), applied to every recommended option of the v1 DRAFT's section 12 (decision:h20-stage-c-run2-open). Signed before any Run 2 code: decision:h20-stage-c-m4c-readability-resigned-run2 (M4(c)'s readability on G3+, Run 2 only, H14 format) and decision:release-value-gated-stage-c-run2 ((N2) re-signed in form). Code src/ph31.py sha256 7744003736c9b3bb43ea34b79e8724bad41c92c963f3afaca6a743670870ec80 (source doc d4c5f81249ef02a9e, content_hash equal; the demo, bench, development run and evaluation all ran on this version), importing src/ph30.py (98822834...59bd) and src/ph30b.py (4e4122c8...be59) unchanged, both checked at run time. One evaluation: E1-C world 2057, agent 2159; E2-C world 2061, agent 2163; 400 rows; E1-C 5400 steps with learning on from step 0; E2-C training 30 / gap 50 / 30 then 1800 test steps with learning on; bootstrap 5000 resamples, seed 20261113, 95 percent. Output experiments/h20/ph31_eval.txt (375 lines, sha256 419dd660f0966b9bc531df0de5f3e19957c3bf8e5679e5ee9199cb70110d0635).

**Status: H20 Stage C Run 2 SHOWN under its registered criteria: M1 to M9 all PASS (M10 reported).** The printout's summary line is the registered verdict sentence, with M4(c) worded as design 3.2 requires: with learning on during the run in the H15 Run 2 world, the adopted agent (Agent14, with the release applied at non-negative holds only; (N2), re-signed in form for Run 2) uses the positive value it learns at the rewarding source: fewer R-start rows visit the not-yet-learned punisher than with H15 Run 2's agent and than with its own positive values removed; and it keeps H15 Run 2's long-horizon search, its avoidance of the learned punisher (among the punished rows in which the no-learning agent ends at the punisher, it dwells there less) and its reach of the reward after avoidance, within Run 2's allowed gaps on the same rows; with a trained memory and learning on in the test it dwells less at the punisher and reaches the reward more than a sham, as H15 Run 2's agent does. **Nothing is adopted by this report; closing Stage C, and H20 as a whole (Stages A, Run 2, B, C), is the owner's decision.**

## 1. What was asked

Run 1's question, unchanged (Run 1 design section 1): with its learning module ON during the run, does the adopted agent Agent14 (with (N2)) use the positive value it learns at the rewarding source to keep choosing that source over the not-yet-learned punisher (M2, the gain), while keeping H15 Run 2's long-horizon search (M3), avoidance of the learned punisher (M4), reach and dwell after avoidance (M5), the rewarded value (M6) and the controlled-experience result with learning on in the test (M7)? Stage C Run 1 stopped at its bench by the (hR) stop rule (record:h20-stage-c-bench-result): the no-learning floor's group median over all G3 had a lower bound of 0 because the floor is two-moded (post-bench diagnosis, record:h20-stage-c-post-bench-diagnosis-result). Run 2 changes only M4(c)'s readability (read on G3+, the rows the WIN is already read on, with G3+ at least 50) and the stop rule that reads it at the bench, and uses new seeds. Run 1's verdict is not re-judged; H15 Run 2's Q3(c) is not re-judged.

## 2. Implementation, self-checks, bench, development run

- **Code.** src/ph31.py was written up to its end by an earlier session that was cut off by a rate limit before any recorded run. The resuming session read it in full against the design, ph30.py and ph30b.py and found every part of design sections 3 to 9 present; it added readings R13 (the recorder's equality with the unrecorded no-learning arm printed in dev and eval) and R14 (M9 PASS requires the bench output's ph31.py sha256 to equal the running file's) and a completion note in the header; no bar, seed, arm, rule or statistic was changed. Readings R1 to R14 are in the file header and printed in every output.
- **Demo** (experiments/h20/ph31_demo.txt, sha256 6efc2ddf3fb2775d92f521c59d2b383fcb606868ab4af8c797fecbca5e88e555): 8/8 ok (the recorded versions of ph30, ph30b and ph30_bench.txt; the statistics switch; the recorder leaves a run unchanged; the re-signed readability on a constructed two-moded floor; (hR2) on constructed rows; the seed scans; the bench and dev/eval code paths end to end on unregistered demo seeds 400 rows x 1800 steps, numbers not used). One demo-stage fix recorded in its header by the earlier session (check 5's 'G3+ under 50' case used 39 positive rows, which resampling carries to 50 or more in some draws; now 25), not re-run separately.
- **Bench** (experiments/h20/ph31_bench.txt, 782 lines, sha256 fdd80164a53fd41d5cfcbee4c64dd430337febd87e7286d6f09bc5116e310277; record:h20-stage-c-run2-bench-result). Seed self-check before the first run: the 33 Run 2 seed and derived numbers in no other file, True; ph30's own scan clean, True.

| part | measured | bar | result |
|---|---|---|---|
| (r) H15 Run 2 reproduced (1640/1740, 1641/1741, reproduction only) | 266 / 266 lines identical; arrays field for field equal | every line | PASS |
| (r') Run 1's bench through ph30 as imported | 370 / 370 lines identical (5 lines carrying Run 1's seeds compared, not printed); G3 199, G3+ 111, floor GM over G3+ 24.000 [22.667, 24.667] PASS, WIN 111/0/0, (hR2) 1.000, the 88 rows outside G3+ all class (i) | exact expected values (design section 4) | PASS (no harness fix needed) |
| (i) identities (i1), (i3)-(i9), recorder | all True | all True | PASS |
| (v) exactness claims | True | True | PASS |
| (h) M2(a) pass probability | learned 18 vs H15 Run 2's agent 65 of 200 R-start rows, DP -0.2350 [-0.2950, -0.1800]: 1.0000 | >= 0.5 | continue |
| (hS) M3(b) P-start / M5(a) | 13 vs 13 of 200 (DP 0.000): 1.0000; 191 vs 191 of 200 (DP 0): 1.0000 | >= 0.5 each | continue |
| (hR1) bench G3+ count | 107 of 200 | >= 50 | continue |
| (hR2) pass probability of the re-signed readability | 1.0000 (1000 outer draws, generator [20261113, 2]; RGM part 1.0000, WIN part 1.0000, M4(c) whole 1.0000) | >= 0.5 | continue |
| M9 | (r), (r'), identities, exactness True; no stop | | **PASS** |

- **Development run** (experiments/h20/ph31_dev.txt, sha256 f367b1a2b04d428ae846f5c47ef029eced1975621c00e528710fc1f6fe1325f5; record:h20-stage-c-run2-dev-run): ran end to end on 9955/9959 and 9967/9975 with no operation error; **no amendment**. The record was written at 19:19 UTC as the evaluation was launched, before the evaluation produced any output.

## 3. Results, one evaluation (E1-C 2057/2159, E2-C 2061/2163)

| measure (ph31_eval.txt) | learned Agent14 (N2) | H15 Run 2's agent | positive-off | no-learning | known-answer | as composed (N1) | H15 no-learning |
|---|---|---|---|---|---|---|---|
| R-start rows visiting P (of 200) | 8 | 56 | 91 | 91 | 1 | 8 | 56 |
| late unrecovered (of 400) | 18 | 21 | 21 | 1 | 21 | 128 | 1 |
| G3 reach after the first punished step (of 199) | 188 | 189 | 188 | 91 | 190 | 88 | 55 |
| contacts per agent | 3.02 | 3.33 | 3.54 | 0.04 | 3.50 | 23.80 | 0.04 |
| last-third dwell GM at R / at P | 23.000 / 0.000 | 22.667 / 0.000 | 23.000 / 0.000 | 11.500 / 4.333 | 23.000 / 0.000 | 20.333 / 0.000 | 9.833 / 8.167 |

E2-C (all 400 rows P-start): pre-test values trained +1.000 / -1.000, sham 0.000 / 0.000; reach R trained learning on 373/400, H15 agent trained learning on 373/400, trained frozen 373/400, (N1) 183/400, sham frozen 142/400; P dwell over the test, median 8.0, 8.0, 8.0, 6.0, 66.0.

**Identities on the task seeds (M8), all True:** (i1) Agent3 + mirror, (i4) Agent3 + min(v, 0) mirror and (i3) Agent8 pathway-off equal to Agent3 live on every (step, row) and every end-of-run record; (i6) Agent14 (N2) at 0/0 == Agent10 at 0/0; (i7) the no-learning pair (N2) == (N1); (i7) learned (N2) == (N1) on every row before its first negative hold (196 rows never hold a negative odour, all equal throughout; 204 do; 0 depart before it); (i8) row independence in the seven E1-C and three E2-C learning-on arms, learning calls 5400 / 1800 / 0, training 60 in every E2 arm, identical training; the mirror equals a fresh read-out on every step (0 mismatches); H19 (a) boundary and flee violations 0/0 in every agent arm; (i9) 400/400 with the mirror, 0/400 with `known` left at 0/0.

## 4. Criteria (registered bars only)

| criterion | measured (95 percent) | bar | result |
|---|---|---|---|
| M1 (a) oracle - random rewarding dwell | DGM 600.000 [600.000, 600.000] | >= 10 | PASS |
| M1 (b) every agent arm, dwell at R and at P | largest GM 23.333 | <= 594 | PASS (16 parts) |
| M1 (c) learned - random total dwell | DGM 23.000 [22.333, 23.667] | >= 10 | PASS |
| **M1** | | | **PASS** |
| M2 (a) DP learned - H15 Run 2's agent, R-start visits | -0.240 [-0.300, -0.180] (8 vs 56 of 200) | upper <= -0.05 | PASS |
| M2 (b) DP learned - positive-off | -0.415 [-0.485, -0.345] (8 vs 91) | upper <= -0.05 | PASS |
| **M2** | | | **PASS** |
| M3 (a) learned late unrecovered | 18/400, 0.045 [0.029, 0.070] | <= 0.10 | PASS |
| M3 (b) DP learned - H15 agent, P-start | 0.000 [-0.015, 0.015] | <= +0.10 | PASS |
| M3 (b) DP learned - H15 agent, R-start | -0.015 [-0.035, 0.000] | <= +0.10 | PASS |
| **M3** | | | **PASS** |
| M4 G3 (P-start rows punished in the learned arm) | 199/200 | >= 50 | readable |
| M4 readability (re-signed): G3+ count | 112 | >= 50 | met |
| M4 readability (re-signed): floor GM over G3+ | 23.333 [22.667, 24.500] | lower >= 10 | PASS |
| M4 (a) learned punished value at the end, G3 | -0.889 [-0.894, -0.800] | <= -0.5 | PASS |
| M4 (b) learned last-third punishing dwell, G3 | 0.000 [0.000, 0.000] | <= 1.0 | PASS |
| M4 (c) RGM learned / no-learning, G3 | 0.000 [0.000, 0.000] | <= 0.75 | PASS |
| M4 (c) WIN learned below no-learning, G3+ | 112 / 112, ties 0.0 percent, 1.000 [0.967, 1.000] | >= 0.60, ties <= 0.20 | PASS |
| **M4** | | | **PASS** |
| M5 (a) DP reach after the first punished step, learned - H15 agent | -0.005 [-0.015, 0.000] | >= -0.10 | PASS |
| M5 readability: H15 agent rewarding dwell, G3 | 22.667 [21.667, 23.000] | >= 10 | PASS |
| M5 (b) RGM rewarding dwell learned / H15 agent | 1.000 [0.970, 1.031] | >= 0.75 | PASS |
| **M5** | | | **PASS** |
| **M6** learned rewarded value at the end, G5 389/400 | 1.000 [1.000, 1.000] | >= 0.5 | **PASS** |
| M7 manipulation check (trained punished value; sham within +/- 0.1) | -1.000 [-1.000, -0.900]; 0.000 [0.000, 0.000] | <= -0.5; +/- 0.1 | PASS |
| M7 readability: sham punishing dwell | 66.000 [63.000, 70.000] | >= 10 | PASS |
| M7 (a) RGM trained learning on / sham | 0.121 [0.100, 0.127] | <= 0.5 | PASS |
| M7 (b) WIN trained below sham | 391/400, ties 0.8 percent, 0.978 [0.958, 0.988] | >= 0.60 | PASS |
| M7 (c) DP reach trained - sham | +0.578 [+0.525, +0.630] | >= +0.25 | PASS |
| M7 (d) DP reach Agent14 - H15 agent, both trained learning on | 0.000 [0.000, 0.000] | >= -0.10 | PASS |
| **M7** | | | **PASS** |
| **M8** identities on the task seeds | all True | all True | **PASS** |
| **M9** bench (read from ph31_bench.txt, run by this same file) | M9 PASS | | **PASS** |
| M10 lost rows and walls | reported (section 3 table) | no bar | reported |

**Reported beside M4, no bar (design 3.2), stated so that nothing the re-sign gives up is hidden:**
1. **The floor over all G3 (Run 1's reading):** n 199, 87 rows at 0; 18.667 [0.000, 20.667]; 'at least 10' would read INCONCLUSIVE, as on Run 1's bench. Under Run 1's rule M4 (b) and (c) would have been UNREADABLE on these seeds; under the re-signed rule they are read.
2. **The WIN over all G3 (Run 2's Q3(c) form):** 112 wins, 85 ties, 2 losses; tie fraction 0.427; share 0.563 [0.493, 0.630]; UNREADABLE by the tie rule (ties above 0.20), which is not waived.
3. **The 87 G3 rows outside G3+:** end states all class (i), at the reward source (classes (ii) at the punisher uncounted, (iii) lost, (iv) at a wall, (v) other: 0 each). **In 2 of them the learned arm's last-third punishing dwell is above 0 (row 136: 8.000; row 230: 0.667); these are the losses hidden from the G3+ WIN**, the two losses of item 2. They are read by M4 (b) (group median 0.000 over G3) and the RGM (0.000), both PASS.
4. **H15 Run 2's agent without learning as a floor (option (ii)):** 40/199 G3 rows at 0; GM 22.000 [21.000, 22.667] (would PASS 'at least 10'); RGM learned / it 0.000 [0.000, 0.000]; WIN on its 159 dwell > 0 rows 159/0/0, 1.000 [0.976, 1.000].

## 5. Predictions (design v2 section 10) against the observations

| prediction | observed | met |
|---|---|---|
| (r) every line of run2; (r') every Run 1 bench line, G3+ 111, 24.000 [22.667, 24.667], (hR2) 1.000 | 266/266; 370/370; exactly as expected | yes |
| M2 learned about 10 (5 to 20) R-start punisher visits | 8 (bench 18) | yes |
| M2 H15 Run 2's agent about 40 to 64 | 56 (bench 65, just above) | yes (bench: no) |
| M2 positive-off about 70 to 90 | 91 (bench 89) | **no, just above** |
| M3 learned late unrecovered about 19/400 (10 to 28), nearly all P-start; P-start DP about -0.01 | 18/400 (17 P-start); DP 0.000 | yes |
| M4 G3 about 199; floor zero rows about 88 (60 to 115), nearly all at the reward source | 199; 87, all at the reward source | yes |
| M4 G3+ about 111 (85 to 140); floor GM over G3+ about 24 [22.5, 25] | 112; 23.333 [22.667, 24.500] | yes |
| M4 WIN on G3+ all or nearly all wins, ties 0 to a few; learned dwell 0 in nearly every G3 row; RGM 0.000 | 112/0/0; 2 of 199 rows above 0; 0.000 | yes |
| M4 floor over all G3 between 0 and 20, lower bound may reach 0 | 18.667 [0.000, 20.667] | yes |
| M4 Agent3 floor about 55 zero rows, GM about 21 | 40 zero rows (bench 54); GM 22.000 | **zero rows no** (fewer); GM yes |
| M5 reach after the first punished step about 192 of 199 in both arms; rewarding dwell medians about 23 | 188 and 189 of 199; RGM 1.000, H15 agent GM 22.667 | approximately (4 rows fewer) |
| M7 manipulation check +1 / -1 and 0 / 0; reach trained about 375/400, equal to the H15 agent; sham reach about 138/400, sham P dwell about 67 | +1.000 / -1.000, 0 / 0; 373 = 373; 142; 66.0 | yes |
| M9 reaching the evaluation about 0.99; joint pass about 0.83 to 0.94 | reached; all parts PASS | consistent |

Missed: positive-off's R-start punisher visits (91, the range's top was 90), the H15 no-learning floor's zero-row count (40 against about 55) and, on the bench, the H15 agent's 65 (range top 64). None of these enters a bar.

## 6. What the run does not show

- **M4(c) is read on G3+, a set chosen by the floor arm's own outcome** (design 3.2). The WIN speaks only for the 112 punished rows in which the no-learning agent ends at the punisher; it does not see the 87 rows in which the floor ended at the reward source, where the learned arm can only tie or lose. Two such losses exist here (rows 136, 230). Over all G3 the WIN is UNREADABLE by the tie rule (ties 0.427). The direction of any bias from the selection (G3+ enriched for world draws in which the reward plume is hard to reach from the punisher, diagnosis (A3)) is not measured.
- **Why some no-learning rows end at the reward source** (world geometry, cast side, loop timing) was not measured.
- The floor over all punished rows, H15 Run 2's agent without learning as the M4(c) floor, a mean or any other statistic in place of the group median: reported or not tested, not criteria.
- **The release at negative values as adopted** is not tested: only (N2), a Stage C-only rule (decision:release-value-gated-stage-c, re-signed in form for Run 2), with (N1) reported. (N1) as composed again strands P-start rows (128/400 late unrecovered, 88 of 199 G3 rows reach the reward after punishment, 23.80 contacts per agent); decision:release-negative-scope-on-hold stays in force outside Stage C.
- Everything Run 1 did not test (Run 1 design section 11): other worlds, other learning rules, other arm sizes, other schedules; E2-C only with the training protocol of H15 Run 2.
- The (N2) frozen defect at a silent negative hold (bench (n): held to the end in 400/400 without evidence) is unchanged and was not a criterion.

## 7. Record-keeping, stated

- **Seeds used:** E1-C evaluation 2057/2159 and E2-C 2061/2163 once; development 9955/9959, 9967/9975 once; bench 20261111/20261112, 20261114/20261115, bootstrap 20261113; H15 Run 2's 1640/1740, 1641/1741 for (r) only; Run 1's bench seeds read from ph30 for (r') only (not written out). Stage C Run 1's development and evaluation seeds stay unused and registered to Run 1.
- **A chance number in the evaluation output.** The evaluation's leak check (reading R12) reports that the number 2115, one of Run 1's registered evaluation seeds, appears once in ph31_eval.txt, as a count ('whiffs handed to navigation: nothing held 65.4% of 2115', line 175, ph15's own measures print). No seed was used; the output is not edited (nothing changes after the table). Consequence: ph30's seed self-check (ph30.seeds_unused), which does not exclude ph31 outputs, now lists experiments/h20/ph31_eval.txt, and ph31's demo check 6, which asserts that check, would now fail if re-run. The demo, bench and development outputs report no such number.
- **Nothing was tuned, swept or re-judged; no bar was adjusted; no post-hoc measure enters the verdict.** No adopted module and no Run 1 file was edited.
- Records: record:h20-stage-c-run2-bench-result, record:h20-stage-c-run2-dev-run, record:h20-stage-c-run2-result. Source doc d4c5f81249ef02a9e. Design v2 FINAL doc d007990ab333e7194.
- **Closure is the owner's.** After Stage C Run 2, H20 as a whole (Stages A, Run 2, B, C) returns to the owner (design section 9, decision:h20-stage-c-run2-open point 7).
