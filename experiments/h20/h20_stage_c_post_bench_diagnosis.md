# H20 Stage C post-bench diagnosis: why the no-learning floor's punishing dwell reads 16.000 [0.000, 19.667], and how M4(c) would read on other floors

Date 2026-09-25. Measurement only, at the owner's instruction (decision:h20-stage-c-post-bench-diagnosis: '2번 진단 먼저 진행', gloss 'run the diagnosis, option 2, first'; the options offered were closing Stage C at the bench stop and returning H20, this diagnosis, or a Run 2 design). H20 Stage C's verdict (record:h20-stage-c-bench-result: stopped at the bench by the registered (hR) stop rule, no bar decision, tasks not run) is not re-judged, and nothing is adopted. ph30.py (sha256 98822834043de5f31615e73cd4a83444adcef2f1d5e56478356d70ca905059bd, source doc d3a2e1142563d7b38), design v2 FINAL (doc d27e6dfe2e2c16183, hash f1e19095...453a), Agent14N2, the harness, the arms, G3, G3+, every bar, every rule and every adopted module are unchanged and imported as they are. Code src/ph30b.py sha256 4e4122c8ba945467d61f3235b8d7eac3d28e788f851ae2b3629d1f476a12be59 (its source stored in its own document). Output experiments/h20/ph30b_diag.txt sha256 69c9867cdb80605014eec27fa264d9d65ad3fb2119b3074d7897cd8b492d4ae8 (LF line ends), appended below in full; every number in sections 1-3 is taken from it and cited as diag:N (its line N). H15 Run 2 numbers are cited from experiments/h15/ph15_run2.txt as run2:N; bench numbers from experiments/h20/ph30_bench.txt as bench:N.

Only the bench E1 seeds (20261091 / 20261092) and the bench bootstrap seed (20261093) are used, read from ph30 and not written out in ph30b.py or its output, so ph30's seed self-check stays valid: re-run after the output was written, no Stage C seed in any other file, 200 files scanned. The development seeds (9982/9984, 9986/9988), the evaluation seeds (2037/2115, 2043/2141) and the E2 bench seeds were not used; E2 was not run. No rule, bar, floor definition or arm was changed; no agent variant was added; nothing was swept.

**A correction to the question as put.** 'GM' in this project is the group median, not a geometric mean: H15 Run 2 specification v3 line 36 ('GM = a group median') and ph15.boot, ph15.py:180 (`"GM": lambda x, y: np.median(x, -1)`), with a percentile bootstrap at ph15.py:184. ph30 uses the same function. Zeros enter as values; they are neither excluded nor floored (diag:41).

## 0. What was asked

(A) Why the no-learning Agent14 arm's last-third punishing dwell (the (hR) quantity, over G3) reads 16.000 [0.000, 19.667]: the per-row distribution, which rows have 0 dwell and why (their end state over the last third, their first arrivals and holds, what the no-learning Agent14 does at 0/0 per the code), the same quantity in H15 Run 2's agent and in the learning arms, how the GM treats zeros and what H15 Run 2's computation of the same quantity gives. (B) Whether another floor definition would make M4(c) readable, measured on the same runs and not proposed as a rule: the WIN, tie and loss counts under the present floor, the WIN and floor GM on subsets of G3, other arms as the floor, and the paired dwell difference.

## 1. Reproduction check

- ph30.py sha256 equals the bench's; ph30_bench.txt sha256 equals the recorded 3fec4dc5...7eec (diag:7).
- The six bench arms (learned, H15 agent, positive-off, no-learning, known-answer, as composed (N1)) were re-run on the bench E1 seeds through ph30's own constructor (ph30.e1_sim) and stepped by ph30's own Sim.step; ph30b only reads state between steps. From these runs ph30's own printing functions and the bench's format strings reproduce the bench's (h) header line (compared, not printed, because it carries the seeds) and 22 further lines ((h) arm lines, M2(a), M2(b), (hR), the (hR) STOP line and the twelve 'printed beside' lines), all present verbatim in ph30_bench.txt, 22/22 (diag:8-31).
- Named checks all True: G3 199, G3+ 111, R-start punisher visits learned 10 and H15 agent 64 of 200, GM 16.000 [0.000, 19.667] (diag:32-33).
- The recorder check holds: every arm in the same world draw; the dwell recomputed from the recorded positions (HIT_R 3.0) equals the harness's per-block g and b in all seven arms (diag:34). Everything below was measured on reproducing runs. The seventh arm, H15 Run 2's agent without learning (Agent3, abl 'learn', ph30's 'H15 no-learning'), is new on these seeds; it was defined in ph30 but not run at the bench.

## 2. Results (A): the (hR) quantity

### (A1) The distribution and the statistic (diag:36-46)

The quantity is, per G3 row, the mean over blocks 7-9 of the steps within HIT_R 3.0 of the punisher per 600-step block (ph15.late, ph15.py:210).

| | value |
|---|---|
| G3 (P-start rows punished at least once in the learned arm, ph30 reading R11) | 199/200 (row 339 is the P-start row outside G3) |
| rows at exactly 0 | **88/199 (44.2 percent)** |
| rows above 0 (G3+) | 111 |
| quantiles min/p10/p25/median/p75/p90/max, G3 | 0.00/0.00/0.00/16.00/24.33/27.07/34.33 |
| the same, G3+ only | 2.67/16.00/20.33/24.00/26.17/29.00/34.33 |
| histogram | 0: 88; (0, 1): 0; [1, 5): 2; [5, 10): 2; [10, 15): 4; [15, 20): 18; [20, 25): 43; [25, 30): 35; >= 30: 7 |
| GM as ph30 computes it (95 percent, bench bootstrap seed) | 16.000 [0.000, 19.667], 'at least 10' INCONCLUSIVE |
| resamples (of 5000) with 100 or more zero rows of 199, whose median is then 0 | 263 (5.26 percent) |
| resample medians below 10 | 736 (14.72 percent) |
| arithmetic mean (reference, same resamples) | 12.690 [10.990, 14.332]; over G3+ 22.751 |
| the same data at H15 Run 2's computation (ph15.py:268, 97.5 percent, Run 2's bootstrap seed ph15.py:25) | 16.000 [0.000, 20.333], INCONCLUSIVE |
| H15 Run 2's agent without learning on these rows, Run 2's computation | 21.000 [19.000, 22.667], PASS |
| H15 Run 2 eval, Agent3 no-learning on its own seeds (run2:189) | 20.667 [18.333, 22.667], PASS |

The distribution is two-moded, not wide: 88 rows at 0 and 107 of the 111 others at 10 or more (diag:40). The median of 199 values is the 100th ordered value; with 88 zeros it is positive (16.000), but a resample whose zero count reaches 100 has a median of 0. That happens in 5.26 percent of the 5000 resamples, more than the 2.5 percent tail, so the lower percentile point is 0 (diag:42). Run 2's own computation at 97.5 percent gives the same point and a lower bound of 0 as well (diag:44-45). The dwell radius is the same code in both (ph30's Sim counts b from w.at_source, as ph15.py:94, :100; ph11.py:103, HIT_R 3.0 at ph9.py:31), so there is no definition mismatch (diag:46).

### (A2) Where the 0-dwell rows are over the last third (diag:48-163)

Classes, exclusive in this order (diag:49-50):

| class | rows |
|---|---|
| (i) at the reward source (a last-third step within HIT_R of R) | **88** |
| (ii) at the punisher but not counted (definition mismatch) | 0 |
| (iii) lost (no whiff of either odour in the last third) | 0 |
| (iv) at a wall | 0 |
| (v) other | 0 |

Every 0-dwell row is at the rewarding source in the last third. Against the G3+ rows, which are at the punisher (diag:57-74):

| last third (row medians, quartiles) | 0-dwell rows (88) | G3+ rows (111) | G3+ rows with dwell >= 20 (85) |
|---|---|---|---|
| median distance to P / to R | 26.6 / 19.6 | 20.1 / 26.9 | 20.2 / 26.9 |
| steps within HIT_R of R / of P (of 1800) | 62/71/79 / 0 | 0 / 61/72/78 | 0 / 68/74/81 |
| whiffs of R / of P | 27/30/35 / 0 | 0 / 24/28/31 | 0 / 25/29/32 |
| share of steps holding P / R / nothing | 0.000 / 0.200 / 0.800 | 0.190 / 0.000 / 0.804 | 0.202 / 0.000 / 0.798 |
| wall contacts (whole run, all rows) | 0 | 0 | 0 |
| late unrecovered | 0 | 0 | 0 |

The two groups are mirror images: one source each, the same dwell at it (about 71-74 of 1800 steps, about 24 per block), no whiff of the other odour, no wall contact, never lost. One 0-dwell row came within 6.0 of the punisher in the last third without entering HIT_R (diag:50). The per-row table (diag:75-163) lists every 0-dwell row.

**What the no-learning Agent14 does at 0/0 (read from the code).** Agent14 = ph24.Release + ph23.Agent9, counter start 240 (ph28.py:92-97); the no-learning arm writes known = 0/0 and never calls the module (ph30.E1ARMS; ph30.kv_of 'zero').
- Gain (ph23.py:62): factor 1 + 2 max(0, 0) = 1; inert.
- Gate (ph23.py:64-66): removes an odour with 0 <= v < v_held; at equal values nothing is removed; inert. The gate does not keep the first hold.
- Filter (ph23.py:88-92): vmax over the present odours is 0; both odours are top when present; keep = held and v_h == vmax is true for any held odour, so while holding only the held odour's whiffs steer (nav = hit); with nothing held a whiff of either odour steers (the whiffed odour is present on that step because the counter is reset at ph23.py:83 before :88). This is the H23 filter's inert case at equal values.
- Counter (ph23.py:82-85; start 240 = N_hi 300 - P 60, ph28.py:72, :92-97): the same prior for both odours (present on steps 0-58 if never sensed, then 300 steps after each whiff). At 0/0 it enters only through vmax and top, which it cannot change here (read above).
- Flee (ph23.py:77, :100): val = known[h] = 0, never negative; no flee.
- Release (ph24.py:54-63; under (N2), ReleaseN2, no held value is negative, so it is the release as composed; bench (i7) no-learning pair True, bench:333): the timeout drive (silence > 40, ph23.py:69) is sustained while a unit is above 1.0 and no whiff of the held odour arrives, which ends a hold 48 steps after the held odour's last whiff; (Z) zeroes the silence counter when a hold forms.
- Evidence release (ph23.py:70): a hold is released when the other odour's upstream response exceeds the held odour's by MARGIN 0.2.
- Cast (ph23.py:95-99): with no navigation event the H16 return cast swings the target about upwind with an offset that rises to MAXOFF 170 and returns (SAT 141.7 steps), alternating side every CAST_PERIOD 30 steps.

Measured against this reading (diag:53-56, 65-68): in the 0-dwell rows the first hold is P in 86 and R in 2, lasts 48/51/56 steps (min 48) and ends by the timeout drive in 88/88, never by the evidence release; every later P hold (420) also ends by the timeout drive. Each row forms 19/21/22 holds over the run and holds nothing on 80 percent of last-third steps. The G3+ rows show the same hold pattern at P (2227 P holds ended by the timeout drive, 26 still held at the end).

### (A3) First arrivals and the 'never left a source it found' reading (diag:52, 55-56, 64, 67-68, 165-169)

| | 0-dwell rows (88) | G3+ rows (111) |
|---|---|---|
| first source reached | P 88 | P 111 |
| visit pattern | P then R, one switch, never back to P: 88 | P only 103; P then R 6; two or more switches 2 |
| last source visited | R 88 | P 104, R 7 |
| R whiffs sensed before the first R hold | 2/3/5 per row, 88/88 rows with at least one, all arriving with nothing held (with P held: 0 rows) | none in 103 rows; 8 rows with at least one |
| first R hold | 88 rows, step 739/1120/1864, after nothing held for 262/303/543 steps | 8 rows, step 3812/4454/4861 |
| position at the first R hold | along the wind -2.6/3.0/7.1 from the sources' line; crosswind 0.84/0.90/0.96 of the way from the P axis to the R axis | -0.2/3.4/6.5; 0.90/0.95/1.06 |
| last step at P | 489/800/1355 (27 in block 1, 44 in blocks 2-3, 17 in blocks 4-6; max 3545) | 5264/5324/5366 |

Every row starts at P. What separates the two groups is whether an R whiff was ever sensed: the 0-dwell rows sensed 2 to 5 R whiffs, each while nothing was held, and then formed an R hold near the R axis about 300 steps after the previous hold had ended; 103 of the G3+ rows never sensed an R whiff in 5400 steps. Once at R, no 0-dwell row returned to P (0/88); among the G3+ rows 2 went back to P after reaching R (diag:168). Of the 88, 27 had left P for good within the first block.

### (A4) The same quantity in the other arms, same rows (diag:171-194)

| arm (G3 rows) | at 0 | above 0 | median | GM [95 percent], 'at least 10' | mean [95 percent] |
|---|---|---|---|---|---|
| Agent14 no-learning (the registered floor) | 88 | 111 | 16.00 | 16.000 [0.000, 19.667] INCONCLUSIVE | 12.690 [10.990, 14.332] |
| H15 Run 2's agent without learning (Agent3) | 55 | 144 | 21.00 | 21.000 [19.667, 22.667] PASS | 16.735 [15.194, 18.256] |
| learned Agent14 (N2), the main arm | 199 | 0 | 0.00 | 0.000 [0.000, 0.000] | 0.000 |
| H15 Run 2's agent, learning on | 198 | 1 | 0.00 | 0.000 [0.000, 0.000] | 0.013 [0.000, 0.040] |
| positive-off | 199 | 0 | 0.00 | 0.000 [0.000, 0.000] | 0.000 |
| as composed (N1), reported | 198 | 1 | 0.00 | 0.000 [0.000, 0.000] | 0.023 [0.000, 0.070] |
| known-answer | 199 | 0 | 0.00 | 0.000 [0.000, 0.000] | 0.000 |

H15 Run 2's agent without learning has the same kind of 0-dwell rows, fewer of them: its 55 are all class (i), at R (diag:180-186). 54 of the 55 are also 0 in Agent14 no-learning; 34 rows are 0 in Agent14 only; 1 in Agent3 only (diag:193). Its holds differ: 2/2/3 hold episodes per row; the first P hold in its 0-dwell rows lasts 486/822/1326 steps and ends without the timeout flag in 53 (the evidence release and decay are not separated for Agent3, whose act does not expose the evidence flag); its G3+ rows hold P on 99.4 percent of steps and 101 of 144 keep the first P hold to the end (diag:183-190). It sensed R whiffs with P held in 53 of its 55 0-dwell rows and 41 of its 144 G3+ rows.

### (A5) The G3 and G3+ definitions (diag:196-198)

G3: P-start rows with at least one punished step in the learned arm, 199/200 (ph30.py reading R11); the same 199 rows are punished at least once in the no-learning arm. G3+: G3 rows whose no-learning last-third punishing dwell is above 0, 111 (ph30.py reading R11 and judge()). The 88 rows outside G3+ are, by definition, the 0-dwell rows of (A1)-(A3): all at the rewarding source.

## 3. Results (B): M4(c) under other floor definitions, measured

### (B1) The registered floor (diag:200-205)

| M4 part, as it would read (M4(b) and M4(c) are gated by the readability rule in ph30.judge; not a verdict) | value |
|---|---|
| WIN learned below no-learning on G3+ | n 111: wins 111, ties 0, losses 0; tie fraction 0.000; share 1.000 [0.967, 1.000], 'at least 0.60' PASS |
| the same WIN over all G3, as Run 2 read Q3(c) (reference) | n 199: wins 111, ties 88 (44.2 percent), losses 0 |
| RGM learned / no-learning over G3 | 0.000 [0.000, 0.000], 'at most 0.75' PASS |
| M4(a) GM learned punished value at the end, G3 | -0.886 [-0.892, -0.800], PASS |
| M4(b) GM learned last-third punishing dwell, G3 | 0.000 [0.000, 0.000], PASS (0 of 199 rows above 0) |

On G3+ the WIN has no ties. M4(c) is unreadable on these runs only through the readability rule, which reads the no-learning GM over all of G3, while the WIN is read on G3+. Over all of G3 the ties would be 44.2 percent (all at the floor, the rows of (A2)).

### (B2) Subsets of G3 by the no-learning dwell (diag:207-213)

| subset | n | wins / ties / losses | tie fraction | WIN share [Wilson 95] | no-learning GM in the subset [95 percent] | smallest passing k; P(K >= k) at the bench share |
|---|---|---|---|---|---|---|
| G3 (all) | 199 | 111 / 88 / 0 | 0.442 | 0.558 [0.488, 0.625], UNREADABLE (ties) | 16.000 [0.000, 19.667] INCONCLUSIVE | 133; 0.0010 |
| dwell > 0 (G3+, registered for the WIN) | 111 | 111 / 0 / 0 | 0.000 | 1.000 [0.967, 1.000] PASS | 24.000 [22.667, 24.667] PASS | 77; 1.0000 |
| dwell >= 1 | 111 | 111 / 0 / 0 | 0.000 | 1.000 [0.967, 1.000] PASS | 24.000 [22.667, 24.667] PASS | 77; 1.0000 |
| dwell >= 5 | 109 | 109 / 0 / 0 | 0.000 | 1.000 [0.966, 1.000] PASS | 24.000 [22.667, 24.667] PASS | 76; 1.0000 |
| dwell >= 10 (the bar's number) | 107 | 107 / 0 / 0 | 0.000 | 1.000 [0.965, 1.000] PASS | 24.000 [22.667, 24.667] PASS | 75; 1.0000 |

### (B3) Other arms as the floor (diag:215-221)

| floor arm | rows at 0 | GM over G3 [95 percent] | lower bound >= 10 | WIN learned below it on its own dwell > 0 rows |
|---|---|---|---|---|
| Agent14 no-learning (registered) | 88/199 | 16.000 [0.000, 19.667] | no (INCONCLUSIVE) | n 111: 111 / 0 / 0, PASS |
| H15 Run 2's agent without learning | 55/199 | 21.000 [19.667, 22.667] | yes (PASS) | n 144: 144 / 0 / 0, share 1.000 [0.974, 1.000] PASS |
| positive-off (learning on, positive values removed) | 199/199 | 0.000 [0.000, 0.000] | no (FAIL) | n 0 |
| as composed (N1) | 198/199 | 0.000 [0.000, 0.000] | no (FAIL) | n 1, UNREADABLE (n < 50) |
| H15 Run 2's agent, learning on | 198/199 | 0.000 [0.000, 0.000] | no (FAIL) | n 1, UNREADABLE |

positive-off is punished in 199/199 G3 rows and learns the punisher's value (median -0.888 at the end); its last-third punishing dwell is 0 in every G3 row, so it is not a no-avoidance floor. (N1) left 122 G3 rows late unrecovered (diag:221).

### (B4) The paired difference, learned - no-learning (diag:223-226)

| group | mean difference [95 percent, paired bootstrap] | difference of group medians | per-row: below 0 / at 0 / above 0 |
|---|---|---|---|
| G3 (199) | -12.690 [-14.332, -10.990] | -16.000 [-19.667, +0.000] | 111 / 88 / 0 |
| G3+ (111) | -22.751 [-23.784, -21.652] | -24.000 [-24.667, -22.667] | 111 / 0 / 0 |
| beside: learned - H15 no-learning, G3 | -16.735 [-18.256, -15.194] | | 144 / 55 / 0 |

No G3 row dwells more at the punisher with learning than without it; the 88 ties are the rows where the no-learning arm is at the rewarding source.

### (B5) Reference arithmetic: the same readings on resampled bench rows (diag:228-236)

1000 draws of 199 G3 rows with replacement from the bench rows (each row carrying its learned, no-learning and H15 no-learning dwell together), each judged exactly as the reading would be (the registered 5000-resample percentile interval at 95 percent, ph15.boot; n >= 50; the tie rule; Wilson 95). These are properties of the bench rows resampled, not pass probabilities for a new world seed, which the bench rows only sample.

| reading | readability PASS | RGM part | WIN part | all three |
|---|---|---|---|---|
| present: readability on G3, WIN on G3+ | **0.178** | 1.000 | 1.000 | 0.178 |
| readability and WIN on no-learning dwell > 0 | 1.000 | 1.000 | 1.000 | 1.000 |
| on dwell >= 1 | 1.000 | 1.000 | 1.000 | 1.000 |
| on dwell >= 5 | 1.000 | 1.000 | 1.000 | 1.000 |
| on dwell >= 10 | 1.000 | 1.000 | 1.000 | 1.000 |
| H15 no-learning as the floor (present structure) | 0.999 | 1.000 | 1.000 | 0.999 |

## 4. Reading (interpretation, not measured)

- The (hR) interval does not come from a spread-out quantity. The no-learning arm ends the run at exactly one source in every G3 row: 88 at the rewarding source and 111 at the punisher, with about the same dwell (about 24 per block) wherever it is. With 44.2 percent of rows at 0 the group median sits a few rows above its breakpoint, and the bootstrap's lower point falls to 0. The same holds at Run 2's own computation. The design's section 7 readability estimate (about 0.9) was inferred from Agent3's Run 2 value; on these rows Agent3 reads 21.000 [19.667, 22.667], and the difference is in the agent.
- The code reading gives one visible difference between the two no-learning agents at 0/0: the H25 release ends every hold 48 steps after the held odour's last whiff, so Agent14 holds nothing on about 80 percent of steps and hands a whiff of either odour to navigation. Agent3 keeps its P hold for hundreds or thousands of steps. The measured pattern fits a picture in which, with nothing held, an excursion that enters R's cone captures the agent at R, and it then stays near R as it stayed near P. Why excursions from P reach R's cone in some rows and not in others (world geometry, cast side, the timing of the loop) was not measured and is not established. Neither is why no row returned from R to P.
- The 88 rows are not lost, not at walls and not a counting artefact: they are at the other source. In an avoidance comparison they are rows where the floor arm also does not dwell at the punisher, for a reason other than learning. H15 Run 2's Q3(c) ties (26.6 percent, run2:192) have the same shape with Agent3, and on these seeds Agent3's 0-dwell rows are also all at R.
- M4(c) is not unreadable because of ties: on G3+ the WIN is 111/0/0. It is unreadable because the readability rule is read on all of G3 while the WIN is read on G3+. On G3+, or on any of the subsets measured, the floor is 24.000 [22.667, 24.667].
- The effect size the WIN summarises is large on these rows (G3+ mean difference -22.751 [-23.784, -21.652]), and the learned arm's last-third punishing dwell is 0 in all 199 G3 rows. That is bench arithmetic on bench seeds. It shows or decides nothing about Stage C, whose tasks were not run.

## 5. What the owner can decide

Listed neutrally. Nothing is adopted, and H20 Stage C's verdict (stopped at the bench by the registered (hR) stop rule, no bar decision, tasks not run) stands whichever option is chosen.

- **Close Stage C at the bench stop and return H20 as a whole.** Stage C stays 'stopped at the bench; nothing shown or not shown about its hypothesis', with this measurement on record. H20 as a whole (Stage A and Run 2 not shown, Stage B shown, Stage C stopped) returns to the owner, as the design's order says.
- **A Stage C Run 2 design.** It would need its own registration, predictions and bench on new seeds before any task seed; the bench seeds' role is spent and these numbers cannot serve as the Run 2 bench. It would have to register at least one of the following, each with its reason stated in advance and, for a changed rule, re-signed in H14 format:
  - (i) **A re-signed M4(c) readability rule read on the group the WIN uses (G3+, no-learning dwell > 0) or on a subset with no-learning dwell >= 1, 5 or 10.** On the bench: n 111/111/109/107, floor GM 24.000 [22.667, 24.667] in each, WIN 111/0/0 (or all wins), tie fraction 0; resampled bench rows 1.000 for readability, the RGM part and the WIN part. The rule would have to say what it still guards: G3+ is chosen by the floor arm's own outcome, and the 88 rows it drops are the rows where the no-learning agent ends at the reward source.
  - (ii) **A different floor arm: H15 Run 2's agent without learning (Agent3), the arm Run 2 itself used.** On the bench: GM 21.000 [19.667, 22.667] PASS, 55 rows at 0, WIN on its 144 dwell > 0 rows 144/0/0; resampled bench rows 0.999. The contrast would then include the agent difference (gain, gate, filter, release, counter) as well as learning, and the rule would have to say so.
  - (iii) **Not usable as a floor on these numbers:** positive-off (199/199 G3 rows at 0; it learns and avoids the punisher), (N1) and H15 Run 2's agent with learning (198/199 at 0).
  - (iv) **The present rule unchanged on new seeds.** The resampled bench rows pass it 0.178 of the time (the zero share, 44.2 percent here, sits near the median's 50 percent breakpoint).
  - In every case: the tie rule as H15 Run 2 left it (a WIN unreadable above 20 percent exact ties; not waived by decision:h15-run2-closed); the stop rules (h), (hS) and a (hR) restated for whatever readability rule is registered; new development, evaluation and bench seeds, scanned.
  - For reference only, because the H15 Run 2 statistics are fixed ('one statistic per criterion ... not replaced afterwards', spec v3 line 36): the arithmetic mean of the no-learning dwell over G3 is 12.690 [10.990, 14.332] (diag:43). A change of statistic would be a change to the inherited criterion, not a floor definition.

## 6. What this does not establish

No change was tested. No alternative rule, floor, statistic or arm was run as a criterion. The classes, positions, hold records and visit patterns describe the runs and name no cause. The resampled pass fractions in (B5) are reference arithmetic on the bench rows, not pass probabilities for a new world seed. The tasks were not run, and no development or evaluation seed was used.

## 7. Provenance

decision:h20-stage-c-post-bench-diagnosis (owner, 2026-09-25). ph30b.py sha 4e4122c8...be59 imports ph30 (sha 98822834...59bd) unchanged, checked at run time. Design v2 FINAL doc d27e6dfe2e2c16183, hash f1e19095...453a. Bench output ph30_bench.txt (sha 3fec4dc5...7eec) reproduced (the (h), (hR) and 'printed beside' lines, 23 lines). Bench E1 seeds and the bench bootstrap seed only. Output ph30b_diag.txt sha 69c9867c...4ae8. Run twice; the second run differs from the first only in its header line (two code-line citations in the source comments were corrected between the runs). Bench result: record:h20-stage-c-bench-result. Result: record:h20-stage-c-post-bench-diagnosis-result. H15 Run 2 evaluation: experiments/h15/ph15_run2.txt (sha 5ce0132f...8b39).

## Appendix: ph30b_diag.txt in full

```
== H20 Stage C post-bench diagnosis (measurement only; owner 2026-09-25, '2번 진단 먼저 진행'). ph30b.py sha256 4e4122c8ba945467d61f3235b8d7eac3d28e788f851ae2b3629d1f476a12be59; ph30.py sha256 98822834043de5f31615e73cd4a83444adcef2f1d5e56478356d70ca905059bd; design H20 Stage C v2 FINAL doc d27e6dfe2e2c16183 hash f1e1909566310ecafaeb589491d946b9d9526a8f1a5dc9d4b6ee46d2ae27453a; reproduces experiments/h20/ph30_bench.txt sha256 3fec4dc50dd3af4456649cf8b10a494d04a5afe937f5bf1f65bc31f2a2367eec (record:h20-stage-c-bench-result) ==
   imported modules (as ph30 prints them): ph4.py d009568cda4dba358f1857268e21a105ad8eac10add665b40792c1c82238646a; ph8.py ada2fc4b38c9d0083d083667ae3fbeb615f544b45f80199ec5b2bc86e6d3b43e; ph9.py 7699b4e6fb47a1bee5f7e4e991a88aac8fa5af3a940297fbd4e441441f4d9706; ph11.py e80f40bd710aca43252f04329846ffa29943251d19e718450e9a7ff49e947a23; ph13.py 2d75fae8e8c31e1c6ddf6577782fafde3099f10fe8f50fe382f53d09e9ef1f2d; ph14.py c6b745c60f9992934a0ccbc5584ef354a03f53f08b37a1252a694feb350be0d0; ph15.py cc9399965e5cbc30cb7f35e8ce296d8d43e4657cf644d1ec350931e594403fdc; ph16.py 33d5fdb25959fb7f9cbe465ca25a8973776b39f1e5170d645cb53bc8d906a2c2; ph19.py 00c6a3b32f80fae9f58b6dbd23a8e03b1710be45fcf335238f289567fce34791; ph21.py 3a1d79d9a0d235f1bef7e435ec594cff4048180e27b28dcd892598c58413cfc1; ph23.py ae180492eece93739da4d1b5d83a13a2b42c5e952445a92ab75f95c6fb2eb5ae; ph24.py f344f178e20380858f4d7400ef670223f90aa2927b3f7304772ae1d848bd1bef; ph25.py 5620a90819693379a53374ca3841e3bc3ddba860d8a8351da7aa1ed4dfe17d91; ph25b.py ad12a9122c171dd32c3fceac946add9d0eb0380e885e0f0872dd97ccd59eeaf6; ph28.py 64ce7d0ce123f912aa675e86627d5b6b0ae3d89976b093666316e6b78441e7aa
   seeds: the bench E1 seeds (ph30.BENCH['e1']) and the bench bootstrap seed (ph30.BENCH['boot'], 95 percent, 5000 resamples), read from ph30 and not written out here; the development and evaluation seeds (ph30.SEEDS) and the E2 bench seeds are not used; no E2 run
   bootstrap as ph30 sets it: level 95.0 percent (percentiles 2.5/97.5); ph15.boot 'GM' is the group median (ph15.py:180; spec v3 line 36 'GM = a group median')

== (0) reproduction (nothing is measured unless every check holds) ==
   ph30.py sha256 equals the bench's (98822834...59bd): True; ph30_bench.txt sha256 equals the recorded (3fec4dc5...7eec): True
   the bench's (h) header line (G3 of the learned arm; it carries the bench seeds, so it is compared and not printed) present verbatim: True
   lines recomputed here with ph30's own functions and format strings, present verbatim in ph30_bench.txt: 22/22
   == [learned] R-start rows visiting P 10/200; P-start late unrecovered 19/200, R-start 0/200; all 19/400; G3 reach after the first punished step 192/199; last-third dwell median R 23.3 P 0.0; first rewarded step 19/50/276; contacts/agent 3.43
   == [H15 agent] R-start rows visiting P 64/200; P-start late unrecovered 21/200, R-start 1/200; all 22/400; G3 reach after the first punished step 192/199; last-third dwell median R 23.3 P 0.0; first rewarded step 19/50/276; contacts/agent 3.62
   == [positive-off] R-start rows visiting P 90/200; P-start late unrecovered 19/200, R-start 4/200; all 23/400; G3 reach after the first punished step 192/199; last-third dwell median R 23.3 P 0.0; first rewarded step 19/50/276; contacts/agent 3.91
   == [no-learning] R-start rows visiting P 90/200; P-start late unrecovered 0/200, R-start 0/200; all 0/400; G3 reach after the first punished step 96/199; last-third dwell median R 14.0 P 3.7; first rewarded step 14/110/775; contacts/agent 0.01
   == [known-answer] R-start rows visiting P 0/200; P-start late unrecovered 12/200, R-start 1/200; all 13/400; G3 reach after the first punished step 192/199; last-third dwell median R 23.0 P 0.0; first rewarded step 19/120/284; contacts/agent 2.30
   == [as composed (N1)] R-start rows visiting P 10/200; P-start late unrecovered 122/200, R-start 4/200; all 126/400; G3 reach after the first punished step 89/199; last-third dwell median R 21.0 P 0.0; first rewarded step 14/28/124; contacts/agent 25.21
   == (h) M2(a) R-start punisher visits learned 10 vs H15 agent 64: DP -0.2700 [-0.3350, -0.2099], discordant b 0.2800 (learned only 1, H15 agent only 55); pass probability 1.0000
   == reported: M2(b) learned vs positive-off 90: DP -0.4000, b 0.4000, pass probability 1.0000
   == (hR) Agent14 no-learning, GM last-third punishing dwell in the bench G3 (reading R12): GM n 199  value 16.000  95% interval [0.000, 19.667]  at least 10 -> INCONCLUSIVE
   == (hR) STOP RULE: STOP: M4(c) would be unreadable; G3+ (no-learning dwell > 0) 111/199
   == [learned] visited P: P-start 199/200, R-start 10/200 (first P visit step, R-start 1834/2258/4619); punisher holds formed at a positive residual: rows 41, events 137 (R-start rows 41); R-start first P visits with R absent (counter >= 300) 10 / 300+ steps since an R whiff 10 of 10
   == G3 (199 rows): reach after the first punished step 192; with a wall contact between it and the next rewarded step 106, without 86; not reached 7 (of them with a wall contact after the first punished step 7); contacts per agent 3.43 (P-start 6.84, R-start 0.03); near wall 0.35%; steps holding a negative odour per row 237.2; (N2) withheld (S) 2060, (Z) 274
   == [H15 agent] visited P: P-start 199/200, R-start 64/200 (first P visit step, R-start 1239/2208/3524); punisher holds formed at a positive residual: rows 8, events 8 (R-start rows 7); R-start first P visits with R absent (counter >= 300) n/a / 300+ steps since an R whiff 52 of 64
   == G3 (199 rows): reach after the first punished step 192; with a wall contact between it and the next rewarded step 105, without 87; not reached 7 (of them with a wall contact after the first punished step 7); contacts per agent 3.62 (P-start 6.88, R-start 0.36); near wall 0.38%; steps holding a negative odour per row 268.4
   == [positive-off] visited P: P-start 199/200, R-start 90/200 (first P visit step, R-start 773/1125/1863); punisher holds formed at a positive residual: rows 21, events 21 (R-start rows 21); R-start first P visits with R absent (counter >= 300) 53 / 300+ steps since an R whiff 53 of 90
   == G3 (199 rows): reach after the first punished step 192; with a wall contact between it and the next rewarded step 106, without 86; not reached 7 (of them with a wall contact after the first punished step 7); contacts per agent 3.91 (P-start 6.80, R-start 1.02); near wall 0.41%; steps holding a negative odour per row 294.8; (N2) withheld (S) 2561, (Z) 364
   == [no-learning] visited P: P-start 199/200, R-start 90/200 (first P visit step, R-start 773/1125/1863); punisher holds formed at a positive residual: rows 0, events 0 (R-start rows 0); R-start first P visits with R absent (counter >= 300) 53 / 300+ steps since an R whiff 53 of 90
   == G3 (199 rows): reach after the first punished step 96; with a wall contact between it and the next rewarded step 0, without 96; not reached 103 (of them with a wall contact after the first punished step 0); contacts per agent 0.01 (P-start 0.00, R-start 0.01); near wall 0.00%; steps holding a negative odour per row 0.0
   == [known-answer] visited P: P-start 141/200, R-start 0/200 (first P visit step, R-start n/a); punisher holds formed at a positive residual: rows 0, events 0 (R-start rows 0); R-start first P visits with R absent (counter >= 300) 0 / 300+ steps since an R whiff 0 of 0
   == G3 (199 rows): reach after the first punished step 192; with a wall contact between it and the next rewarded step 72, without 120; not reached 7 (of them with a wall contact after the first punished step 5); contacts per agent 2.30 (P-start 4.16, R-start 0.45); near wall 0.21%; steps holding a negative odour per row 262.0; (N2) withheld (S) 2245, (Z) 417
   == [as composed (N1)] visited P: P-start 199/200, R-start 10/200 (first P visit step, R-start 1834/2258/4619); punisher holds formed at a positive residual: rows 41, events 137 (R-start rows 41); R-start first P visits with R absent (counter >= 300) 10 / 300+ steps since an R whiff 10 of 10
   == G3 (199 rows): reach after the first punished step 89; with a wall contact between it and the next rewarded step 0, without 89; not reached 110 (of them with a wall contact after the first punished step 110); contacts per agent 25.21 (P-start 49.58, R-start 0.83); near wall 3.28%; steps holding a negative odour per row 26.4
   named checks: G3 199 True; G3+ 111 True; R-start P visits learned 10 True; R-start P visits H15 agent 64 True; GM 16.000 [0.000, 19.667] True
   reproduction holds: True
   recorder check: every arm in the same world draw True; the dwell recomputed from the recorded positions (HIT_R 3.0) equals the harness's per-block g and b: learned True, H15 agent True, positive-off True, no-learning True, known-answer True, as composed (N1) True, H15 no-learning True

== (A1) the (hR) quantity: Agent14 no-learning, last-third punishing dwell (mean steps within HIT_R of the punisher per 600-step block, blocks 7-9) over G3 ==
   G3 = P-start rows with a punished step in the learned arm (ph30 reading R11): 199/200; the P-start row outside G3: [339] (its learned-arm first punished step [-1], no-learning last-third P dwell [0.0])
   rows with dwell exactly 0: 88/199 (44.2 percent); above 0 (G3+): 111
   quantiles min/p10/p25/median/p75/p90/max, all G3: 0.00/0.00/0.00/16.00/24.33/27.07/34.33; G3+ only: 2.67/16.00/20.33/24.00/26.17/29.00/34.33
   histogram (bins at the readability bar 10 and in steps of 5): 0 88; (0, 1) 0; [1, 5) 2; [5, 10) 2; [10, 15) 4; [15, 20) 18; [20, 25) 43; [25, 30) 35; >= 30 7
   GM as ph30 computes it (ph15.boot 'GM', ph15.py:180-185: np.median of the 199 values, zeros included as values, neither excluded nor floored; 95 percent percentile bootstrap): 16.000 [0.000, 19.667] -> 'at least 10' INCONCLUSIVE
   the resamples: zero rows per resample 83/88/93 (min 67, max 114); resamples with 100 or more zero rows of 199 (median then 0) 263/5000 = 5.26 percent; resample medians equal to 0: 263/5000 = 5.26 percent; resample medians below 10: 736/5000 = 14.72 percent (the lower 2.5 percent point is 0 because more than 2.5 percent of the resample medians are 0)
   for reference, the arithmetic mean: 12.690 [10.990, 14.332] (same resamples); the mean over G3+ only: 22.751
   the same data under H15 Run 2's computation of the same quantity (ph15.py:268 crit('readability: no-learning punishing dwell in G3', 'GM', 10, False, late(N['b'])[g3]), the same function at Run 2's 97.5 percent level and Run 2's bootstrap seed, ph15.py:25): 16.000 [0.000, 20.333] -> INCONCLUSIVE; resamples with 100+ zero rows 264/5000
   side by side (reported, not a re-judgement): ph30 (95 percent, bench bootstrap seed) 16.000 [0.000, 19.667] INCONCLUSIVE | Run 2's computation 16.000 [0.000, 20.333] INCONCLUSIVE | H15 Run 2's own agent without learning on these rows at Run 2's computation 21.000 [19.000, 22.667] PASS; H15 Run 2 eval (Agent3 no-learning, its own seeds) 20.667 [18.333, 22.667]
   the dwell radius: ph30's Sim counts b = w.at_source() (ph30.py Sim.step, as ph15.py:94, :100), w.at_source is ph11.py:103 (distance < HIT_R, ph9.py:31 HIT_R 3.0) in both; the definitions are the same code; recomputed from the recorded positions above: equal

== (A2) where the 0-dwell rows are over the last third (steps 3600-5399), with the G3+ rows beside ==
   classes (exclusive, in this order): (i) at the reward source (a last-third step within HIT_R of R) 88; (ii) at the punisher source but not counted 0; (iii) lost (no whiff of either odour in the last third) 0; (iv) at a wall (a contact or a step within 1.0 of a wall in the last third) 0; (v) other 0
   overlaps: class (i) rows with no whiff in the last third 0, class (i) rows also near a wall 0; 0-dwell rows within 2 x HIT_R (6.0) of the punisher on some last-third step without being within HIT_R 1
   class i (n 88): last third: median distance to P 26.6 (row medians; quartiles 25.9/26.6/27.6), to R 19.6 (19.1/19.6/20.3); steps within HIT_R of R 62/71/79, of P 0/0/0; whiffs P 0/0/0, R 27/30/35; share of steps holding P 0.000, R 0.200, nothing 0.800; rows with a last-third wall contact 0, whole-run contacts 0; rows within 2 x HIT_R of P on some last-third step 1; late unrecovered (no plume whiff, blocks 7-9) 0
      first source reached: P 88, R 0, none 0; first arrival step 13/18/124; last source visited: P 0, R 88, none 0; source switches 1/1/1 (0: 0, 1: 88, 2+: 0); last step at P 489/800/1355; first step at R 776/1105/1684 (rows reaching R 88); an R arrival after the last P step 88
      first hold: odour P 86, R 2, never held 0; formed at step 11/19/258; duration 48/51/56 (min 48, max 72); ended by: evidence release 0, timeout drive 88, other 0, held to the end 0; next held: R 0, P 0, none 88, - 0
      every P hold over the run ended by: evidence release 0, timeout drive 420, other 0, still held at the end 0; hold episodes per row 19/21/22; a P -> R change of hold 86 (first at step 776/1127/1865); whole-run share of steps holding P 0.037, R 0.150
      R whiffs sensed before the first R hold (or over the run if none forms): per row 2/3/5 (rows with none 0); of them arriving with nothing held 2/3/5 (rows with at least one 88), with P held 0/0/0 (rows with at least one 0); rows forming an R hold 88
      at the first R hold: step 739/1120/1864; held before it: nothing 88, P 0; steps since the previous hold ended 262/303/543; position along the wind from the sources' line (+ downwind) -2.6/3.0/7.1; crosswind as a fraction from the P axis (0) to the R axis (1) 0.84/0.90/0.96
   all 0-dwell rows (n 88): last third: median distance to P 26.6 (row medians; quartiles 25.9/26.6/27.6), to R 19.6 (19.1/19.6/20.3); steps within HIT_R of R 62/71/79, of P 0/0/0; whiffs P 0/0/0, R 27/30/35; share of steps holding P 0.000, R 0.200, nothing 0.800; rows with a last-third wall contact 0, whole-run contacts 0; rows within 2 x HIT_R of P on some last-third step 1; late unrecovered (no plume whiff, blocks 7-9) 0
      first source reached: P 88, R 0, none 0; first arrival step 13/18/124; last source visited: P 0, R 88, none 0; source switches 1/1/1 (0: 0, 1: 88, 2+: 0); last step at P 489/800/1355; first step at R 776/1105/1684 (rows reaching R 88); an R arrival after the last P step 88
      first hold: odour P 86, R 2, never held 0; formed at step 11/19/258; duration 48/51/56 (min 48, max 72); ended by: evidence release 0, timeout drive 88, other 0, held to the end 0; next held: R 0, P 0, none 88, - 0
      every P hold over the run ended by: evidence release 0, timeout drive 420, other 0, still held at the end 0; hold episodes per row 19/21/22; a P -> R change of hold 86 (first at step 776/1127/1865); whole-run share of steps holding P 0.037, R 0.150
      R whiffs sensed before the first R hold (or over the run if none forms): per row 2/3/5 (rows with none 0); of them arriving with nothing held 2/3/5 (rows with at least one 88), with P held 0/0/0 (rows with at least one 0); rows forming an R hold 88
      at the first R hold: step 739/1120/1864; held before it: nothing 88, P 0; steps since the previous hold ended 262/303/543; position along the wind from the sources' line (+ downwind) -2.6/3.0/7.1; crosswind as a fraction from the P axis (0) to the R axis (1) 0.84/0.90/0.96
   G3+ rows (no-learning dwell > 0) (n 111): last third: median distance to P 20.1 (row medians; quartiles 19.5/20.1/21.0), to R 26.9 (25.8/26.9/27.9); steps within HIT_R of R 0/0/0, of P 61/72/78; whiffs P 24/28/31, R 0/0/0; share of steps holding P 0.190, R 0.000, nothing 0.804; rows with a last-third wall contact 0, whole-run contacts 0; rows within 2 x HIT_R of P on some last-third step 111; late unrecovered (no plume whiff, blocks 7-9) 0
      first source reached: P 111, R 0, none 0; first arrival step 12/19/120; last source visited: P 104, R 7, none 0; source switches 0/0/0 (0: 103, 1: 6, 2+: 2); last step at P 5264/5324/5366; first step at R 3606/4368/4534 (rows reaching R 8); an R arrival after the last P step 7
      first hold: odour P 111, R 0, never held 0; formed at step 11/18/145; duration 48/51/57 (min 48, max 71); ended by: evidence release 0, timeout drive 111, other 0, held to the end 0; next held: R 0, P 0, none 111, - 0
      every P hold over the run ended by: evidence release 0, timeout drive 2227, other 0, still held at the end 26; hold episodes per row 19/21/22; a P -> R change of hold 8 (first at step 3812/4454/4861); whole-run share of steps holding P 0.192, R 0.000
      R whiffs sensed before the first R hold (or over the run if none forms): per row 0/0/0 (rows with none 103); of them arriving with nothing held 0/0/0 (rows with at least one 8), with P held 0/0/0 (rows with at least one 0); rows forming an R hold 8
      at the first R hold: step 3812/4454/4861; held before it: nothing 8, P 0; steps since the previous hold ended 283/486/650; position along the wind from the sources' line (+ downwind) -0.2/3.4/6.5; crosswind as a fraction from the P axis (0) to the R axis (1) 0.90/0.95/1.06
   high-dwell rows (no-learning dwell >= 20) (n 85): last third: median distance to P 20.2 (row medians; quartiles 19.5/20.2/21.0), to R 26.9 (26.2/26.9/27.9); steps within HIT_R of R 0/0/0, of P 68/74/81; whiffs P 25/29/32, R 0/0/0; share of steps holding P 0.202, R 0.000, nothing 0.798; rows with a last-third wall contact 0, whole-run contacts 0; rows within 2 x HIT_R of P on some last-third step 85; late unrecovered (no plume whiff, blocks 7-9) 0
      first source reached: P 85, R 0, none 0; first arrival step 12/19/120; last source visited: P 85, R 0, none 0; source switches 0/0/0 (0: 84, 1: 0, 2+: 1); last step at P 5278/5325/5366; first step at R 1609/1609/1609 (rows reaching R 1); an R arrival after the last P step 0
      first hold: odour P 85, R 0, never held 0; formed at step 11/18/146; duration 48/52/58 (min 48, max 71); ended by: evidence release 0, timeout drive 85, other 0, held to the end 0; next held: R 0, P 0, none 85, - 0
      every P hold over the run ended by: evidence release 0, timeout drive 1757, other 0, still held at the end 21; hold episodes per row 19/21/22; a P -> R change of hold 1 (first at step 2047/2047/2047); whole-run share of steps holding P 0.199, R 0.000
      R whiffs sensed before the first R hold (or over the run if none forms): per row 0/0/0 (rows with none 84); of them arriving with nothing held 0/0/0 (rows with at least one 1), with P held 0/0/0 (rows with at least one 0); rows forming an R hold 1
      at the first R hold: step 2047/2047/2047; held before it: nothing 1, P 0; steps since the previous hold ended 626/626/626; position along the wind from the sources' line (+ downwind) 6.0/6.0/6.0; crosswind as a fraction from the P axis (0) to the R axis (1) 0.96/0.96/0.96
   per 0-dwell row: row | class | last-third steps at R / at P, whiffs R/P | median distance to R / P (last third) | first hold odour, formed, duration, ended by -> next | visit pattern (R/P runs) | last step at P, first step at R | contacts (last third / run)
       1 | i   |  62/0,  28/0 |  18.8 /  28.6 | P  284   48 timeout drive -> none | P17 R12 | 2995, 3197 | 0/0
       7 | i   |  59/0,  23/0 |  19.6 /  26.6 | P   19   48 timeout drive -> none | P10 R22 | 1514, 1837 | 0/0
      19 | i   |  61/0,  35/0 |  19.3 /  24.9 | P  327   67 timeout drive -> none | P5 R26 |  653,  850 | 0/0
      21 | i   |  77/0,  24/0 |  19.4 /  26.6 | P   31   48 timeout drive -> none | P3 R28 |  353,  553 | 0/0
      24 | i   |  65/0,  35/0 |  17.0 /  26.5 | P  279   48 timeout drive -> none | P5 R28 |  732, 1026 | 0/0
      31 | i   |  74/0,  41/0 |  19.4 /  26.8 | P   24   48 timeout drive -> none | P4 R29 |  479,  650 | 0/0
      37 | i   |  55/0,  31/0 |  19.0 /  25.2 | P    7   59 timeout drive -> none | P8 R24 | 1116, 1318 | 0/0
      43 | i   | 102/0,  38/0 |  19.9 /  25.2 | P   19   48 timeout drive -> none | P6 R26 |  797,  985 | 0/0
      44 | i   |  82/0,  26/0 |  21.4 /  25.7 | P  135   48 timeout drive -> none | P11 R23 | 1693, 1879 | 0/0
      47 | i   |  77/0,  30/0 |  18.3 /  25.7 | P   12   49 timeout drive -> none | P5 R28 |  641,  956 | 0/0
      54 | i   |  66/0,  24/0 |  20.5 /  29.4 | P   16   53 timeout drive -> none | P6 R25 |  794, 1149 | 0/0
      55 | i   |  65/0,  34/0 |  19.5 /  25.6 | P  302   48 timeout drive -> none | P8 R24 | 1069, 1224 | 0/0
      60 | i   |  55/0,  40/0 |  19.7 /  27.3 | P   10   62 timeout drive -> none | P7 R23 |  942, 1256 | 0/0
      61 | i   |  59/0,  22/0 |  21.6 /  26.7 | P  152   49 timeout drive -> none | P3 R28 |  465,  781 | 0/0
      62 | i   |  90/0,  29/0 |  20.1 /  26.6 | P   12   51 timeout drive -> none | P6 R29 |  834, 1146 | 0/0
      66 | i   |  59/0,  25/0 |  18.9 /  25.6 | P   15   50 timeout drive -> none | P5 R27 |  644,  793 | 0/0
      71 | i   |  67/0,  30/0 |  19.0 /  27.3 | P  341   61 timeout drive -> none | P5 R25 |  942, 1246 | 0/0
      72 | i   |  42/0,  16/0 |  17.6 /  27.3 | P  433   48 timeout drive -> none | P4 R27 |  583,  775 | 0/0
      77 | i   |  58/0,  33/0 |  19.1 /  26.4 | P   12   59 timeout drive -> none | P8 R26 | 1183, 1386 | 0/0
      78 | i   |  80/0,  33/0 |  20.3 /  24.4 | P    8   54 timeout drive -> none | P2 R32 |  166,  498 | 0/0
      79 | i   |  51/0,  28/0 |  19.1 /  26.5 | P  304   48 timeout drive -> none | P4 R29 |  456,  655 | 0/0
      81 | i   |  78/0,  35/0 |  20.2 /  27.0 | P    7   48 timeout drive -> none | P6 R26 |  611, 1087 | 0/0
      88 | i   |  97/0,  38/0 |  19.9 /  26.3 | P  300   48 timeout drive -> none | P21 R15 | 2993, 3151 | 0/0
      97 | i   |  70/0,  21/0 |  20.9 /  26.6 | P   18   54 timeout drive -> none | P5 R27 |  727,  918 | 0/0
      99 | i   |  68/0,  26/0 |  19.4 /  26.0 | P  311   52 timeout drive -> none | P14 R20 | 2117, 2423 | 0/0
     104 | i   |  66/0,  33/0 |  17.5 /  26.2 | P  306   51 timeout drive -> none | P17 R16 | 2942, 2977 | 0/0
     106 | i   |  78/0,  31/0 |  20.1 /  28.5 | P   10   61 timeout drive -> none | P14 R20 | 1901, 2105 | 0/0
     113 | i   |  80/0,  31/0 |  20.5 /  27.5 | P  302   51 timeout drive -> none | P7 R24 | 1080, 1258 | 0/0
     121 | i   |  90/0,  40/0 |  19.6 /  24.9 | P  138   48 timeout drive -> none | P3 R30 |  315,  585 | 0/0
     129 | i   |  77/0,  31/0 |  21.0 /  27.6 | P   24   48 timeout drive -> none | P3 R30 |  334,  644 | 0/0
     135 | i   |  55/0,  35/0 |  20.0 /  28.4 | P   18   49 timeout drive -> none | P2 R31 |  171,  479 | 0/0
     136 | i   |  94/0,  30/0 |  19.6 /  26.0 | P  254   49 timeout drive -> none | P21 R11 | 3545, 3702 | 0/0
     137 | i   |  42/0,  25/0 |  18.2 /  23.6 | P    7   59 timeout drive -> none | P4 R26 |  637,  944 | 0/0
     146 | i   |  60/0,  27/0 |  17.8 /  26.9 | R  300   48 timeout drive -> none | P1 R27 |   21,  280 | 0/0
     151 | i   |  36/0,  15/0 |  21.7 /  29.8 | P  300   48 timeout drive -> none | P13 R15 | 2288, 2483 | 0/0
     154 | i   |  64/0,  27/0 |  18.9 /  27.5 | P   24   49 timeout drive -> none | P8 R27 | 1125, 1318 | 0/0
     159 | i   | 100/0,  35/0 |  20.1 /  28.3 | P   18   48 timeout drive -> none | P15 R21 | 2358, 2557 | 0/0
     161 | i   |  89/0,  41/0 |  19.6 /  25.6 | P   11   55 timeout drive -> none | P2 R32 |  171,  371 | 0/0
     163 | i   |  88/0,  30/0 |  19.1 /  26.4 | P   19   55 timeout drive -> none | P19 R18 | 2563, 2867 | 0/0
     165 | i   |  50/0,  28/0 |  20.1 /  26.9 | P    7   66 timeout drive -> none | P6 R23 |  793, 1104 | 0/0
     173 | i   |  83/0,  22/0 |  20.3 /  27.5 | P   15   48 timeout drive -> none | P18 R14 | 2839, 3135 | 0/0
     178 | i   |  76/0,  42/0 |  19.2 /  27.1 | P    8   56 timeout drive -> none | P4 R25 |  492,  808 | 0/0
     179 | i   |  72/0,  29/0 |  19.8 /  28.0 | P   12   57 timeout drive -> none | P8 R24 | 1347, 1651 | 0/0
     185 | i   |  78/0,  19/0 |  19.7 /  27.3 | P  120   48 timeout drive -> none | P5 R28 |  670,  863 | 0/0
     190 | i   |  62/0,  31/0 |  21.4 /  27.5 | P    8   51 timeout drive -> none | P5 R30 |  498,  700 | 0/0
     192 | i   |  67/0,  38/0 |  19.3 /  26.5 | P   18   52 timeout drive -> none | P4 R26 |  575,  777 | 0/0
     194 | i   |  69/0,  17/0 |  20.5 /  27.6 | P  135   48 timeout drive -> none | P16 R16 | 2396, 2600 | 0/0
     197 | i   |  82/0,  36/0 |  20.3 /  25.0 | P   31   48 timeout drive -> none | P16 R19 | 2145, 2340 | 0/0
     199 | i   |  77/0,  31/0 |  19.3 /  26.2 | P  480   48 timeout drive -> none | P7 R25 |  942, 1185 | 0/0
     200 | i   |  73/0,  30/0 |  18.4 /  26.1 | P  335   48 timeout drive -> none | P9 R24 | 1379, 1684 | 0/0
     202 | i   |  70/0,  30/0 |  21.2 /  26.8 | P  312   58 timeout drive -> none | P8 R24 | 1260, 1452 | 0/0
     212 | i   |  74/0,  28/0 |  19.5 /  27.9 | P   13   52 timeout drive -> none | P3 R30 |  322,  630 | 0/0
     215 | i   |  57/0,  31/0 |  20.2 /  28.4 | P   10   60 timeout drive -> none | P6 R27 |  708, 1008 | 0/0
     220 | i   |  62/0,  22/0 |  20.7 /  28.8 | P   24   49 timeout drive -> none | P6 R25 |  801, 1106 | 0/0
     236 | i   |  80/0,  33/0 |  20.4 /  26.3 | P   34   48 timeout drive -> none | P3 R31 |  334,  531 | 0/0
     238 | i   |  53/0,  38/0 |  18.5 /  24.8 | P  138   48 timeout drive -> none | P5 R24 |  753, 1075 | 0/0
     239 | i   | 106/0,  38/0 |  18.0 /  24.1 | P    6   68 timeout drive -> none | P2 R29 |  178,  547 | 0/0
     248 | i   |  66/0,  30/0 |  19.6 /  28.3 | P  176   72 timeout drive -> none | P7 R24 | 1152, 1310 | 0/0
     249 | i   |  65/0,  35/0 |  19.8 /  26.3 | P   11   56 timeout drive -> none | P13 R21 | 1886, 2086 | 0/0
     251 | i   |  73/0,  26/0 |  19.6 /  27.6 | P  286   48 timeout drive -> none | P8 R26 | 1244, 1440 | 0/0
     261 | i   |  71/0,  32/0 |  19.2 /  26.3 | P  179   54 timeout drive -> none | P3 R29 |  343,  540 | 0/0
     263 | i   |  79/0,  39/0 |  20.2 /  27.4 | P   18   65 timeout drive -> none | P6 R28 |  536,  845 | 0/0
     266 | i   |  77/0,  25/0 |  20.9 /  27.6 | R  458   53 timeout drive -> none | P2 R32 |  266,  458 | 0/0
     271 | i   |  58/0,  25/0 |  19.5 /  26.5 | P    6   58 timeout drive -> none | P1 R29 |   15,  512 | 0/0
     283 | i   |  64/0,  28/0 |  20.6 /  26.2 | P   11   51 timeout drive -> none | P8 R23 | 1305, 1604 | 0/0
     286 | i   |  70/0,  26/0 |  21.0 /  29.2 | P   13   48 timeout drive -> none | P8 R25 | 1345, 1540 | 0/0
     290 | i   |  75/0,  30/0 |  19.0 /  25.9 | P   22   51 timeout drive -> none | P2 R30 |  180,  372 | 0/0
     305 | i   |  93/0,  37/0 |  20.6 /  27.9 | P   28   48 timeout drive -> none | P2 R33 |  191,  486 | 0/0
     307 | i   |  62/0,  38/0 |  18.6 /  25.4 | P    8   48 timeout drive -> none | P2 R29 |  153,  471 | 0/0
     312 | i   |  55/0,  25/0 |  20.0 /  26.6 | P   12   53 timeout drive -> none | P9 R21 | 1334, 1540 | 0/0
     315 | i   |  70/0,  32/0 |  20.8 /  26.7 | P    9   50 timeout drive -> none | P8 R27 | 1113, 1419 | 0/0
     316 | i   |  86/0,  27/0 |  20.0 /  26.1 | P   10   49 timeout drive -> none | P5 R29 |  706,  856 | 0/0
     317 | i   |  73/0,  28/0 |  19.5 /  26.0 | P   13   59 timeout drive -> none | P14 R22 | 1952, 2140 | 0/0
     318 | i   |  97/0,  22/0 |  19.7 /  23.8 | P   22   48 timeout drive -> none | P5 R29 |  842, 1041 | 0/0
     320 | i   |  77/0,  28/0 |  19.1 /  28.0 | P  302   53 timeout drive -> none | P8 R21 | 1323, 1685 | 0/0
     322 | i   |  80/0,  31/0 |  19.7 /  26.3 | P    8   63 timeout drive -> none | P6 R26 |  799, 1004 | 0/0
     326 | i   |  65/0,  22/0 |  21.3 /  27.8 | P   15   54 timeout drive -> none | P2 R31 |  175,  473 | 0/0
     333 | i   |  77/0,  32/0 |  16.7 /  24.7 | P   16   48 timeout drive -> none | P21 R12 | 3052, 3369 | 0/0
     349 | i   |  71/0,  34/0 |  17.9 /  24.6 | P   11   63 timeout drive -> none | P5 R25 |  734,  926 | 0/0
     357 | i   |  85/0,  38/0 |  18.8 /  25.2 | P    8   65 timeout drive -> none | P12 R20 | 1750, 1944 | 0/0
     358 | i   |  77/0,  33/0 |  20.9 /  28.7 | P   15   48 timeout drive -> none | P11 R21 | 1558, 1860 | 0/0
     360 | i   |  75/0,  31/0 |  18.9 /  25.6 | P  271   48 timeout drive -> none | P6 R27 |  752, 1052 | 0/0
     371 | i   |  80/0,  37/0 |  20.6 /  28.6 | P   11   53 timeout drive -> none | P4 R26 |  478,  776 | 0/0
     377 | i   |  71/0,  34/0 |  19.2 /  25.6 | P   20   54 timeout drive -> none | P7 R26 |  971, 1299 | 0/0
     379 | i   |  62/0,  39/0 |  18.3 /  25.4 | P   11   65 timeout drive -> none | P3 R33 |  355,  549 | 0/0
     386 | i   |  62/0,  30/0 |  20.4 /  28.1 | P  321   53 timeout drive -> none | P8 R25 | 1105, 1305 | 0/0
     394 | i   |  84/0,  29/0 |  19.5 /  28.7 | P  286   48 timeout drive -> none | P19 R14 | 2834, 3136 | 0/0
     399 | i   |  49/0,  32/0 |  19.8 /  27.4 | P   15   60 timeout drive -> none | P22 R11 | 3366, 3558 | 0/0

== (A3) first arrivals and the 'never left a source it found' reading (no-learning Agent14, G3) ==
   0-dwell (n 88): visit patterns: P only 0; P then R and never back to P (one switch) 88; two or more switches 0; last visited source R 88, P 0; first hold P and held to the end 0
   G3+ (n 111): visit patterns: P only 103; P then R and never back to P (one switch) 6; two or more switches 2; last visited source R 7, P 104; first hold P and held to the end 0
   source switches, 0-dwell rows 1/1/1 vs G3+ rows 0/0/0; rows back at the punisher after their first R arrival (last P step > first R step): 0-dwell 0, G3+ 2
   0-dwell rows: last step at the punisher 15/188/489/800/1355/2446/3545 (min/p10/p25/median/p75/p90/max); rows whose last P step falls in block 1 27, blocks 2-3 44, blocks 4-6 17

== (A4) the same quantity in the other arms on the same rows (G3 of the learned arm; last-third punishing dwell) ==
   arm | rows at 0 | G3+ by its own dwell | quantiles min/p10/p25/median/p75/p90/max | GM [95 percent] 'at least 10' | mean [95 percent]
   no-learning       |  88 | 111 | 0.00/0.00/0.00/16.00/24.33/27.07/34.33 | 16.000 [0.000, 19.667] INCONCLUSIVE | 12.690 [10.990, 14.332]
   H15 no-learning   |  55 | 144 | 0.00/0.00/0.00/21.00/25.33/28.40/34.33 | 21.000 [19.667, 22.667] PASS | 16.735 [15.194, 18.256]
   learned           | 199 |   0 | 0.00/0.00/0.00/0.00/0.00/0.00/0.00 | 0.000 [0.000, 0.000] FAIL | 0.000 [0.000, 0.000]
   H15 agent         | 198 |   1 | 0.00/0.00/0.00/0.00/0.00/0.00/2.67 | 0.000 [0.000, 0.000] FAIL | 0.013 [0.000, 0.040]
   positive-off      | 199 |   0 | 0.00/0.00/0.00/0.00/0.00/0.00/0.00 | 0.000 [0.000, 0.000] FAIL | 0.000 [0.000, 0.000]
   as composed (N1)  | 198 |   1 | 0.00/0.00/0.00/0.00/0.00/0.00/4.67 | 0.000 [0.000, 0.000] FAIL | 0.023 [0.000, 0.070]
   known-answer      | 199 |   0 | 0.00/0.00/0.00/0.00/0.00/0.00/0.00 | 0.000 [0.000, 0.000] FAIL | 0.000 [0.000, 0.000]
   H15 Run 2's agent without learning (Agent3, abl 'learn'), its 0-dwell rows (55), classes: i 55; ii 0; iii 0; iv 0; v 0
   H15 no-learning 0-dwell rows (n 55): last third: median distance to P 26.4 (row medians; quartiles 25.4/26.4/27.7), to R 19.9 (19.1/19.9/20.4); steps within HIT_R of R 61/69/78, of P 0/0/0; whiffs P 0/0/0, R 24/28/30; share of steps holding P 0.000, R 1.000, nothing 0.000; rows with a last-third wall contact 1, whole-run contacts 2; rows within 2 x HIT_R of P on some last-third step 3; late unrecovered (no plume whiff, blocks 7-9) 0
      first source reached: P 55, R 0, none 0; first arrival step 13/18/118; last source visited: P 0, R 55, none 0; source switches 1/1/1 (0: 0, 1: 55, 2+: 0); last step at P 732/1260/1919; first step at R 1056/1555/2160 (rows reaching R 55); an R arrival after the last P step 55
      first hold: odour P 53, R 2, never held 0; formed at step 11/18/135; duration 486/822/1326 (min 4, max 5100); ended by: timeout drive 0, no timeout flag (evidence release or decay; the evidence flag is not exposed by Agent3) 53, held to the end 2; next held: R 0, P 0, none 53, - 2
      every P hold over the run ended by: timeout flag set 2, no timeout flag (evidence release or decay, not separated for Agent3) 86, still held at the end 0; hold episodes per row 2/2/3; a P -> R change of hold 53 (first at step 1121/1635/2326); whole-run share of steps holding P 0.216, R 0.710
      R whiffs sensed before the first R hold (or over the run if none forms): per row 5/7/8 (rows with none 0); of them arriving with nothing held 3/4/6 (rows with at least one 55), with P held 1/2/3 (rows with at least one 53); rows forming an R hold 55
      at the first R hold: step 1110/1568/2238; held before it: nothing 55, P 0; steps since the previous hold ended 66/277/301; position along the wind from the sources' line (+ downwind) -4.3/-2.2/3.5; crosswind as a fraction from the P axis (0) to the R axis (1) 0.86/0.93/0.99
   H15 no-learning G3+ rows (n 144): last third: median distance to P 20.0 (row medians; quartiles 19.5/20.0/20.9), to R 26.7 (25.3/26.7/27.6); steps within HIT_R of R 0/0/0, of P 61/72/79; whiffs P 24/28/32, R 0/0/0; share of steps holding P 1.000, R 0.000, nothing 0.000; rows with a last-third wall contact 0, whole-run contacts 0; rows within 2 x HIT_R of P on some last-third step 144; late unrecovered (no plume whiff, blocks 7-9) 0
      first source reached: P 144, R 0, none 0; first arrival step 12/19/122; last source visited: P 137, R 7, none 0; source switches 0/0/0 (0: 136, 1: 7, 2+: 1); last step at P 5266/5324/5368; first step at R 4235/4763/5216 (rows reaching R 8); an R arrival after the last P step 7
      first hold: odour P 144, R 0, never held 0; formed at step 11/18/182; duration 3480/5315/5387 (min 1, max 5394); ended by: timeout drive 3, no timeout flag (evidence release or decay; the evidence flag is not exposed by Agent3) 40, held to the end 101; next held: R 0, P 0, none 43, - 101
      every P hold over the run ended by: timeout flag set 4, no timeout flag (evidence release or decay, not separated for Agent3) 105, still held at the end 134; hold episodes per row 1/1/2; a P -> R change of hold 7 (first at step 4535/4978/5218); whole-run share of steps holding P 0.994, R 0.000
      R whiffs sensed before the first R hold (or over the run if none forms): per row 0/0/1 (rows with none 103); of them arriving with nothing held 0/0/0 (rows with at least one 9), with P held 0/0/1 (rows with at least one 41); rows forming an R hold 7
      at the first R hold: step 4535/4978/5218; held before it: nothing 7, P 0; steps since the previous hold ended 137/177/260; position along the wind from the sources' line (+ downwind) -3.7/-1.3/4.5; crosswind as a fraction from the P axis (0) to the R axis (1) 0.91/0.92/0.96
   0 in both no-learning arms 54; 0 in Agent14 only 34; 0 in Agent3 only 1
   H15 no-learning histogram: 0 55; (0, 1) 0; [1, 5) 2; [5, 10) 0; [10, 15) 3; [15, 20) 28; [20, 25) 56; [25, 30) 45; >= 30 10

== (A5) the G3 / G3+ definitions on these runs ==
   G3: P-start rows with at least one punished step in the learned arm (ph30.py reading R11; bench line (h)): 199/200; the same rows are punished at least once in the no-learning arm: 199/199
   G3+: G3 rows whose no-learning last-third punishing dwell is above 0 (ph30.py reading R11, judge()): 111; the 88 rows outside G3+ are by definition the 0-dwell rows of (A1)-(A3)

== (B1) M4(c) as it would read on these runs with the registered floor (Agent14 no-learning; reported, the (hR) rule made it unreadable) ==
   WIN learned below no-learning on G3+: n 111; wins 111, ties 0, losses 0; tie fraction 0.000 (rule: unreadable above 0.20); win share 1.000, Wilson 95 [0.967, 1.000] 'at least 0.60' -> PASS
   (for reference) the same WIN over all G3 as Run 2 read Q3(c): n 199; wins 111, ties 88 (44.2 percent), losses 0
   RGM learned / no-learning over G3 (the second part of M4(c)): 0.000 [0.000, 0.000] 'at most 0.75' -> PASS
   M4(a) GM learned punished value at the end over G3: -0.886 [-0.892, -0.800] 'at most -0.5' -> PASS; M4(b) GM learned last-third punishing dwell over G3: 0.000 [0.000, 0.000] 'at most 1.0' -> PASS; learned dwell above 0 in 0/199 G3 rows
   (M4(b) and M4(c) are gated by the readability rule in ph30.judge; the values above are printed as they would read, not as a verdict)

== (B2) the WIN restricted to subsets of G3 by the no-learning dwell, and the no-learning GM in each (measured on the same runs; no rule proposed) ==
   subset | n | wins / ties / losses | tie fraction | win share [Wilson 95] 'at least 0.60' | no-learning GM in the subset [95 percent] 'at least 10' | smallest passing k, P(K >= k) at the bench share
   G3 (all)                     | 199 | 111 /  88 /   0 | 0.442 | 0.558 [0.488, 0.625] UNREADABLE (ties) | 16.000 [0.000, 19.667] INCONCLUSIVE | 133, 0.0010
   dwell > 0 (G3+, registered)  | 111 | 111 /   0 /   0 | 0.000 | 1.000 [0.967, 1.000] PASS | 24.000 [22.667, 24.667] PASS | 77, 1.0000
   dwell >= 1                   | 111 | 111 /   0 /   0 | 0.000 | 1.000 [0.967, 1.000] PASS | 24.000 [22.667, 24.667] PASS | 77, 1.0000
   dwell >= 5                   | 109 | 109 /   0 /   0 | 0.000 | 1.000 [0.966, 1.000] PASS | 24.000 [22.667, 24.667] PASS | 76, 1.0000
   dwell >= 10                  | 107 | 107 /   0 /   0 | 0.000 | 1.000 [0.965, 1.000] PASS | 24.000 [22.667, 24.667] PASS | 75, 1.0000

== (B3) other arms as the floor, measured (no rule proposed): GM of the arm's last-third punishing dwell over G3, and the WIN learned below it on that arm's own dwell > 0 rows ==
   floor no-learning      : rows at 0 88/199; GM 16.000 [0.000, 19.667], lower bound >= 10: False (INCONCLUSIVE); WIN on its dwell > 0 rows: n 111, wins 111, ties 0, losses 0, tie fraction 0.000, share 1.000 [0.967, 1.000] PASS
   floor H15 no-learning  : rows at 0 55/199; GM 21.000 [19.667, 22.667], lower bound >= 10: True (PASS); WIN on its dwell > 0 rows: n 144, wins 144, ties 0, losses 0, tie fraction 0.000, share 1.000 [0.974, 1.000] PASS
   floor positive-off     : rows at 0 199/199; GM 0.000 [0.000, 0.000], lower bound >= 10: False (FAIL); WIN on its dwell > 0 rows: n 0, wins 0, ties 0, losses 0
   floor as composed (N1) : rows at 0 198/199; GM 0.000 [0.000, 0.000], lower bound >= 10: False (FAIL); WIN on its dwell > 0 rows: n 1, wins 1, ties 0, losses 0, tie fraction 0.000, share 1.000 [0.207, 1.000] UNREADABLE (n < 50)
   floor H15 agent        : rows at 0 198/199; GM 0.000 [0.000, 0.000], lower bound >= 10: False (FAIL); WIN on its dwell > 0 rows: n 1, wins 1, ties 0, losses 0, tie fraction 0.000, share 1.000 [0.207, 1.000] UNREADABLE (n < 50)
   positive-off in G3 (learning on, positive values removed from the read-out): punished at least once 199/199; learned punished value at the end, median -0.888; last-third P dwell > 0 in 0 rows; (N1): 1 rows, late unrecovered in G3 122

== (B4) the paired difference in last-third punishing dwell, learned - no-learning (the quantity the WIN summarises) ==
   G3 (n 199): mean difference -12.690 [-14.332, -10.990] (95 percent, paired bootstrap); difference of group medians -16.000 [-19.667, +0.000]; per-row differences quantiles -34.33/-27.07/-24.33/-16.00/0.00/0.00/0.00; rows below 0 111, at 0 88, above 0 0
   G3+ (n 111): mean difference -22.751 [-23.784, -21.652] (95 percent, paired bootstrap); difference of group medians -24.000 [-24.667, -22.667]; per-row differences quantiles -34.33/-29.00/-26.17/-24.00/-20.33/-16.00/-2.67; rows below 0 111, at 0 0, above 0 0
   beside: learned - H15 no-learning over G3: mean difference -16.735 [-18.256, -15.194]; rows below 0 144, at 0 55, above 0 0

== (B5) reference arithmetic (not a rule): how often each reading would PASS on a new draw of 199 G3 rows like the bench's ==
   1000 outer draws of G3 rows with replacement (rows carry their learned, no-learning and H15 no-learning dwell together; generator seeded by the sequence [bench bootstrap seed, 2]); each draw judged exactly as the reading would be (the registered 5000-resample percentile interval at 95 percent, ph15.boot; n >= 50; the tie rule; Wilson 95)
   present: readability on G3, WIN on G3+            : readability PASS 0.178; RGM part PASS 1.000; WIN part PASS (ties <= 0.20, lower >= 0.60) 1.000; all three 0.178
   readability and WIN on dwell > 0                  : readability PASS 1.000; RGM part PASS 1.000; WIN part PASS (ties <= 0.20, lower >= 0.60) 1.000; all three 1.000
   readability and WIN on dwell >= 1                 : readability PASS 1.000; RGM part PASS 1.000; WIN part PASS (ties <= 0.20, lower >= 0.60) 1.000; all three 1.000
   readability and WIN on dwell >= 5                 : readability PASS 1.000; RGM part PASS 1.000; WIN part PASS (ties <= 0.20, lower >= 0.60) 1.000; all three 1.000
   readability and WIN on dwell >= 10                : readability PASS 1.000; RGM part PASS 1.000; WIN part PASS (ties <= 0.20, lower >= 0.60) 1.000; all three 1.000
   H15 no-learning as the floor (present structure)  : readability PASS 0.999; RGM part PASS 1.000; WIN part PASS (ties <= 0.20, lower >= 0.60) 1.000; all three 0.999
   (these are properties of the bench rows resampled; they are not pass probabilities for a new seed's world draw, which the bench rows only sample)

== end of diagnosis; H20 Stage C's verdict unchanged: stopped at the bench by the registered (hR) stop rule, no bar decision; nothing adopted; the owner decides ==
```
