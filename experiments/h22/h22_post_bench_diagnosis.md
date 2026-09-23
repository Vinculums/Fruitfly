# H22 post-bench diagnosis: why bench (d) revises 0.210 of neutral holds instead of at least 0.50

Date 2026-09-23. Measurement only, at the owner's instruction (decision:h22-post-bench-diagnosis: '1. 1번 안 2. 기록 진행', option 1, bar and verdict kept). The bench verdict (record:h22-bench-result: M4 FAIL on (d), NO CANDIDATE, the task not run) is not re-judged. ph20.py (sha256 edec6d83...efbe, doc d714b91e1fbbc7ede), design v1 FINAL (doc dfd041adf77911e7c, hash 1ce2717e...7f83), Agent7's rule, every bar and every adopted module are unchanged. Code ph20b.py sha256 4b6c049797646b17fe86321053706963c1c64f6f51018f78a5a452f74ecd49d1 (source stored in its own document). Output ph20b_diag.txt sha256 12d1eee4511d64e74435b0feb007907ea4565804814b2c800abfb1995783c702 (written with LF line ends), appended below in full.

ph20b imports ph20 unchanged and builds bench (d)'s constructed state line for line as ph20.bench_d does: World7 on the bench seeds, 400 rows, the agent placed at the neutral source with World7's heading draw, fresh cast and silence counters, the neutral hold constructed (s 2.0 / 0, S 0), G 2, gate on; rule on (resample) and rule off on the same draws. It only records states around each sense/act call. Only the bench seeds are used; the development seeds 9870/9970 and the evaluation seeds 1755/1855 remain unused. **Identity check (printed in the run):** holding the valued odour at step 300 is 84/400 with the rule and 5/400 without, equal to ph20.bench_d re-run in the same process and to ph20_bench.txt; rows with a valued whiff by 300 (289 and 9), whiffs per row (1.84 and 0.09), first valued whiff median 186 and revision median 192 (rule on) also equal the bench's printout. The runs to 900 steps are the same runs continued. A diagnosis narrows where the failure lies; it names no cause beyond what was measured, and it tests no change.

## 1. Measured

1. **Revision against time, registered start** (holding the valued odour at step t, of 400; Wilson 95 percent at 300 and 600):

   | step | rule on | rule off | rule on, rows with >= 1 valued whiff by t | rule off, same |
   |---|---|---|---|---|
   | 100 | 0 (0.000) | 0 (0.000) | 0 | 0 |
   | 150 | 0 (0.000) | 0 (0.000) | 0 | 0 |
   | 200 | 52 (0.130) | 3 (0.007) | 160 | 8 |
   | 250 | 81 (0.203) | 5 (0.013) | 289 | 9 |
   | 300 | 84 (0.210) [0.173, 0.253] | 5 (0.013) [0.005, 0.029] | 289 | 9 |
   | 400 | 87 (0.217) | 34 (0.085) | 289 | 42 |
   | 500 | 119 (0.297) | 55 (0.138) | 299 | 81 |
   | 600 | 131 (0.328) [0.283, 0.375] | 76 (0.190) [0.155, 0.231] | 323 | 87 |
   | 750 | 146 (0.365) | 100 (0.250) | 325 | 120 |
   | 900 | 156 (0.390) | 123 (0.307) | 336 | 146 |

   Revised and later lost: 0 in both arms at every step (no valued hold ended). Revision rises with time but does not reach 0.60: at 600 the upper Wilson bound is 0.375, at 900 the point is 0.390. It rises in steps: 84 rows by 300 (all between steps 150 and 300), +3 by 400, +44 from 400 to 600, +25 from 600 to 900. Of the rows with at least one valued whiff, the fraction holding the valued odour is 0.291 at 300, 0.406 at 600, 0.464 at 900 with the rule, against 0.556, 0.874, 0.842 without it. The difference rule on minus rule off is +0.197 at 300, +0.138 at 600, +0.083 at 900.

2. **What a valued whiff does to a neutral hold** (rule on, registered start, 900 steps; 800 valued whiffs arriving while the neutral odour was held, in 336 rows, each with a full 10-step window). Within 10 steps: the valued odour took the hold after 42 (0.052); the neutral hold was released to nothing held without the valued odour taking it after 612; the neutral hold survived all 10 steps after 146.

   | valued whiffs in the window (including this one) | 5-step window: flipped | 10-step window: flipped |
   |---|---|---|
   | 1 | 16/592 = 0.027 | 3/537 = 0.006 |
   | 2 | 16/174 = 0.092 | 22/203 = 0.108 |
   | 3+ | 10/34 = 0.294 | 17/60 = 0.283 |

   An isolated valued whiff (no other in the 9 steps before or after) flipped the hold 0 of 319 times; a non-isolated one 42 of 481. By the held unit's s at arrival: [0, 1.5) 36/95, [1.5, 1.8) 6/109, >= 1.8 0/596 (s median 2.17, 5th-95th percentile 1.20-3.11; valued unit s median 0.000; pool S median 2.84). The first valued whiff of a row flipped the hold within 10 steps in 1 of 336 rows (0 of 202 when it was the only valued whiff in its window). Flipped whiffs had 0.10 neutral whiffs in the preceding 20 steps and a median 49 steps since the last neutral whiff; unflipped ones 1.11 and 17. In the 612 releases without a flip the valued unit's peak s over the next 9 steps was median 0.00 (1.62 in flips) and the neutral unit fell to median 0.82.

   Rule off (239 events in 146 rows): flipped 90 (0.377); by whiffs in the 10-step window 1: 35/149 = 0.235, 2: 40/70 = 0.571, 3+: 15/20 = 0.750; isolated 0/46; held unit's s at arrival median 1.57, flips 62/89 below 1.5, 28/93 in [1.5, 1.8), 0/57 at >= 1.8; neutral whiffs in the preceding 20 steps 0.00 (flipped) and 0.02 (not); median 171 steps since the last neutral whiff.

3. **The route to revision (hold transitions).** Every first valued hold, in both arms and both starts, was entered from 'nothing held'; none directly from the neutral hold (rule on 156/156, rule off 123/123). Rule on: 495 stretches of 'nothing held' followed a neutral hold; 156 ended in the valued hold (duration quartiles 5/8/17 steps; 1.20 valued and 0.14 neutral whiffs in the stretch on average), 322 in the neutral hold again (9/16/38 steps; 0.02 valued and 2.12 neutral whiffs), 17 were still open at 900. Rule off: 149 stretches; 123 ended valued, 21 neutral again, 5 open. Per release the valued odour took the hold in 156/495 = 0.315 with the rule and 123/149 = 0.826 without.

4. **The loop, registered start** (first 600 steps; positions from the neutral source, d_along > 0 downwind). Rule on: maximum upwind excursion quartiles 30.2 / 32.4 / 37.8 (all 400 rows beyond 20 upwind); first return within 5.0 of the neutral source (after being beyond 10.0) in 400/400 rows at step 141 / 142 / 143; returns per row median 4 (0/1/2/3+ returns: 0/39/62/299); first entry into the valued cone (or within 3.0 of the valued source) in 391 rows at step 172 / 177 / 205; steps in the valued cone per row 13 / 26 / 50. First valued whiff (323 rows by 600) at step 177 / 201 / 214, at d_along 11.9 / 14.4 / 18.1, d_cross 5.5 / 6.6 / 7.6 from the neutral axis toward the valued one, 2.4 / 3.4 / 4.5 from the valued axis; the cast clock at that step equals the step number (177 / 201 / 214): no navigation hit since the start. Rule off: upwind excursion 32.5 / 33.1 / 33.5; first return at 148 / 152 / 155; returns median 3; first valued cone entry in 94 rows at 325 / 375 / 483; first valued whiff (87 rows) at step 330 / 411 / 488, d_along 6.2 / 8.1 / 9.8, 1.1 / 1.8 / 2.5 from the valued axis; cast clock 166 / 170 / 174.

5. **Where the first valued whiffs come from.** Rule on, 323 rows: within 3.0 of the valued source 5, plume core (|d_cross to the valued axis| < 3) 120, cone edge 198. At the median arrival position (d_along 14.4, |d_cross| 3.4; cone half-width 5.1 there) the per-step whiff probability from the world's cone formula (0.3 x exp(-d_along/12)) is 0.090. Rule off, 87 rows: source 2, core 74, edge 11; median position d_along 8.1, |d_cross| 1.8, probability 0.153.

6. **VARIANT start, not the bench** (a different constructed state, reported beside the registered start and not merged with it): the same 400 rows and seeds, but the agent on the neutral axis 20 downwind of the neutral source, heading upwind (180), neutral hold s 2.0 / 0, S 0, cast clock 0; 600 steps. Holding the valued odour: rule on 0 at 250, 3 (0.007) [0.003, 0.022] at 300, 4 at 400, 12 at 500, 33 (0.083) [0.059, 0.114] at 600 (34 ever revised, 1 lost); rule off 2 (0.005) [0.001, 0.018] at 300, 34 (0.085) [0.061, 0.116] at 600. Rows with a valued whiff by 600: 191 with the rule, 50 without. Rule on: 262 events, flipped within 10 steps 10 (isolated 0/155); 196 releases, 34 ended valued (0.173), 127 neutral again, 35 open; loop: upwind excursion 18.0 / 20.1 / 22.3, first return at step 31 / 32 / 33, 5 returns in every row, first valued cone entry at 254 / 446 / 475, first valued whiff at 448 / 473 / 533, at d_along 21.2 median and 5.2 from the valued axis (edge 165 of 191; probability 0.051). Rule off: 47 releases, 34 ended valued; first valued whiff at 468 / 519 / 533.

7. **Silence and walls.** Rows with no whiff of either plume in the last 100 steps, registered start: rule on 12 at 300, 98 at 600, 233 at 900; rule off 361, 247, 160. Variant: rule on 5 at 300, 26 at 600; rule off 302, 119. Wall contacts 0 in every arm and start.

## 2. Reading

Interpretation, separated from the measurements above; it names no cause beyond what was measured and tests no change.

**The owner's question: (가) a window problem, (나) a mechanism ceiling, or both.** Both are present, and the window is not sufficient. On the registered start revision does climb with time (0.210 at 300, 0.328 at 600, 0.390 at 900), so part of the bench (d) shortfall is the 300-step window: the loop brings the agent past the valued cone about once per cast-clock period (first valued whiffs mostly between steps 160 and 250, the next wave between 400 and 600), and 300 steps contain one pass. But at the task's exposure (about 590 steps for a neutral-first row) revision is 0.328 [0.283, 0.375], below 0.50 and below the predicted 0.60-0.95, and each later pass converts fewer of the remaining rows (84 of 400 by 300; 44 of 313 from 400 to 600; 25 of 269 from 600 to 900). This contradicts the design section 2 premise as far as it was tested: the rule does produce sampling (336 of 400 rows receive a valued whiff by 900, against 146 without it); it is the conversion of that sampling into a valued hold that falls short.

**Where the conversion is lost.** No valued whiff installed the valued hold directly. A valued whiff either left the neutral hold standing (held unit's s at or above 1.8: 0 of 596 flips) or released it to 'nothing held' through the evidence release, after which the valued unit had to be driven over threshold by further valued whiffs before neutral whiffs re-took the hold. Single whiffs never completed that (isolated whiffs 0/319; one whiff in 10 steps 3/537). With the rule, 322 of 495 releases went back to the neutral hold, with about two neutral whiffs and almost no valued whiff in the stretch; without the rule 21 of 149 did. Mechanism interpretation, not a causal test: with the rule the agent reaches the valued plume on the return leg of its loop, at the cone edge (198 of 323 first whiffs; about 0.09 whiffs per step) and still within reach of the neutral plume (unflipped whiffs had a neutral whiff a median 17 steps before; the held unit's s was higher, median 2.17 against 1.57 without the rule). Without the rule the few rows that reach the valued plume do so late, in its core (74 of 87), long after the last neutral whiff, and convert at 0.826 per release. The rule raises how often the valued plume is sampled but lowers how often a sample converts; the net gain over the rule-off agent shrinks with time (+0.197 at 300, +0.138 at 600, +0.083 at 900).

**The start.** The registered start is not representative of a task-like start in the one direction measured here: from the neutral axis 20 downwind, heading upwind (the variant; not the bench), revision at 600 is 0.083 with the rule and 0.085 without, no difference between the arms, and the first valued whiff arrives at a median step 473, at the far downwind edge of the valued cone (d_along 21.2, probability 0.051). The previous unregistered reading (the loop starts upwind and widens to 170 degrees over about 142 steps; the agent climbs about 28 units upwind, returns near the source near step 150 and reaches the valued plume near step 190) is confirmed in its timing for the registered start (upwind excursion median 32.4, first return at step 142, first valued whiff median 201, at 14.4 downwind rather than 19). Its implication that a window matched to the task would carry revision toward the prediction is not confirmed.

**Lost rows grow with time under the rule:** rows with no whiff of either plume in the last 100 steps rise from 12 at 300 to 98 at 600 and 233 at 900, while the rule-off agent's fall from 361 to 160. This bears on M6(a) if a longer exposure were ever registered.

## 3. What a design v2 would have to change (options; the choice is the owner's)

If the failure is read as (가) the window: a bench (d) window matched to the task's exposure (about 590-600 steps) is a registration change, and on this measurement it would not pass the unchanged bar (0.328, upper bound 0.375, against 0.50); the prediction 0.60-0.95 would also have to be withdrawn as written. A window change alone does not yield a candidate. The bar is not lowered to the observed number.

If it is read as (나) the mechanism (the measurements put the larger part here): what fails is the step from 'released' to 'valued held'. Levers, each its own hypothesis with its own criteria and none tested here:
- navigation while nothing is held after a release: H19 (a) surges on any non-negative whiff, so a neutral whiff in that stretch drives the agent back up the neutral plume; for example a surge only on the higher-valued odour in that stretch;
- navigation of the resample loop itself, so that sampling reaches the valued plume's core rather than its edge, earlier and farther from the neutral plume (cast geometry or period); the variant shows that the loop's reach depends strongly on the start;
- selection: letting a valued whiff, or a short cluster, install the valued hold instead of leaving 'nothing held' to be re-taken by the neutral odour, for example the H21 gate extended to the stretch in which nothing is held; this is a selection change, outside H22 as a navigation hypothesis;
- closing H22 as NOT shown (no candidate), with this diagnosis on record.

If both: a v2 would need a mechanism change of the kind above and a window matched to the task, with new predictions and a bench on its own seeds before any task seed is used.

## 4. What this does not establish

No change was tested. It does not show that any lever in section 3 would reach 0.50 or 0.60; the absence of conversion is not evidence that a given term is needed. The variant is one constructed start, not the task's start (the task starts on the midline 20 downwind); it is reported as a second constructed state only. The 900-step figures are not an extrapolation to any limit. The task was not run, and no development or evaluation seed was used.

## 5. Provenance

decision:h22-post-bench-diagnosis (owner, 2026-09-23). ph20b.py sha 4b6c0497...49d1 (imports ph20 unchanged; ph20.py sha edec6d83...efbe checked at run time); design v1 FINAL doc dfd041adf77911e7c hash 1ce2717e...7f83; bench seeds only; output sha 12d1eee4...c702. Bench result: record:h22-bench-result. Result: record:h22-post-bench-diagnosis-result.

## Appendix: ph20b_diag.txt in full

== H22 post-bench diagnosis (measurement only). this file sha256 4b6c049797646b17fe86321053706963c1c64f6f51018f78a5a452f74ecd49d1; ph20.py sha256 edec6d834860cc6c4c0ac361998fe09405344b2e494aef21a28b04ca7b6cefbe; design v1 FINAL doc dfd041adf77911e7c hash 1ce2717e95d3444c79d8eeeec6b618d553edede71069b61ece7eb3cd13037f83; the bench seeds (ph20.BENCH seed_w / seed_a), 400 rows; no other seed used ==

(0) identity: the registered 300-step protocol (bench (d)) re-run
   rule on : holding the valued odour at step 300 here 84/400, ph20.bench_d 84/400, ph20_bench.txt 84/400 -> True; rows with >=1 valued whiff by 300 289, per row 1.84; first valued whiff median 186, revision median 192
   rule off: holding the valued odour at step 300 here 5/400, ph20.bench_d 5/400, ph20_bench.txt 5/400 -> True; rows with >=1 valued whiff by 300 9, per row 0.09; first valued whiff median 180, revision median 194

(1) revision against time, REGISTERED start (placed at the neutral source, World7 heading draw, neutral hold s 2.0 / 0, S 0), 900 steps
   rule on
      step | holding valued at t        | ever revised by t | >=1 valued whiff by t | revised, not holding at t | a valued hold ended by t | P(holding | >=1 valued whiff)
       100 |   0/400 = 0.000                  |   0               |   0                   |   0                       |   0                      | nan
       150 |   0/400 = 0.000                  |   0               |   0                   |   0                       |   0                      | nan
       200 |  52/400 = 0.130                  |  52               | 160                   |   0                       |   0                      | 0.325
       250 |  81/400 = 0.203                  |  81               | 289                   |   0                       |   0                      | 0.280
       300 |  84/400 = 0.210 [0.173, 0.253]   |  84               | 289                   |   0                       |   0                      | 0.291
       400 |  87/400 = 0.217                  |  87               | 289                   |   0                       |   0                      | 0.301
       500 | 119/400 = 0.297                  | 119               | 299                   |   0                       |   0                      | 0.398
       600 | 131/400 = 0.328 [0.283, 0.375]   | 131               | 323                   |   0                       |   0                      | 0.406
       750 | 146/400 = 0.365                  | 146               | 325                   |   0                       |   0                      | 0.449
       900 | 156/400 = 0.390                  | 156               | 336                   |   0                       |   0                      | 0.464
   rule off
      step | holding valued at t        | ever revised by t | >=1 valued whiff by t | revised, not holding at t | a valued hold ended by t | P(holding | >=1 valued whiff)
       100 |   0/400 = 0.000                  |   0               |   0                   |   0                       |   0                      | nan
       150 |   0/400 = 0.000                  |   0               |   0                   |   0                       |   0                      | nan
       200 |   3/400 = 0.007                  |   3               |   8                   |   0                       |   0                      | 0.375
       250 |   5/400 = 0.013                  |   5               |   9                   |   0                       |   0                      | 0.556
       300 |   5/400 = 0.013 [0.005, 0.029]   |   5               |   9                   |   0                       |   0                      | 0.556
       400 |  34/400 = 0.085                  |  34               |  42                   |   0                       |   0                      | 0.810
       500 |  55/400 = 0.138                  |  55               |  81                   |   0                       |   0                      | 0.679
       600 |  76/400 = 0.190 [0.155, 0.231]   |  76               |  87                   |   0                       |   0                      | 0.874
       750 | 100/400 = 0.250                  | 100               | 120                   |   0                       |   0                      | 0.833
       900 | 123/400 = 0.307                  | 123               | 146                   |   0                       |   0                      | 0.842

(2) what flips the neutral hold, registered start, 900 steps
   rule on: valued whiffs arriving while the neutral odour is held (events with a full 10-step window): 800 in 336 rows; flipped to the valued odour within 10 steps 42 = 0.052; not flipped but the hold released (nothing held) at some step 612; neutral kept all 10 steps 146
      at arrival: held (neutral) unit s median 2.17 [1.20, 3.11], valued unit s median 0.000, pool S median 2.84
      by valued whiffs in the 5 steps up to and including it: 1: 16/592 = 0.027; 2: 16/174 = 0.092; 3+: 10/34 = 0.294
      by ... in the 10 steps: 1: 3/537 = 0.006; 2: 22/203 = 0.108; 3+: 17/60 = 0.283
      neutral whiffs in the 20 steps up to it: flipped mean 0.10, not flipped 1.11; steps since the last neutral whiff: flipped median 49, not flipped median 17
      released but not flipped (612): hold at the 10th step neutral 4, nothing 608, valued 0; over the next 9 steps the valued unit's peak s median 0.00 (flipped 1.62), the neutral unit's lowest s median 0.82 (flipped 0.46)
      isolated whiff (no other valued whiff in the 9 steps before or the 9 after): 0/319 = 0.000; not isolated 42/481 = 0.087
      by the held unit's s at arrival: [0.0, 1.5): 36/95; [1.5, 1.8): 6/109; [1.8, 2.0): 0/97; [2.0, 2.2): 0/116; [2.2, 2.5): 0/161; [2.5, 5.1): 0/222
      first valued whiff per row: 336 rows (neutral held at it 336); flipped within 10 steps 1, not 335 (rows with a full window 336); when it was the only valued whiff in its 10-step window: flipped 0/202, when more followed: 1/134
   rule off: valued whiffs arriving while the neutral odour is held (events with a full 10-step window): 239 in 146 rows; flipped to the valued odour within 10 steps 90 = 0.377; not flipped but the hold released (nothing held) at some step 148; neutral kept all 10 steps 1
      at arrival: held (neutral) unit s median 1.57 [1.06, 1.99], valued unit s median 0.000, pool S median 2.16
      by valued whiffs in the 5 steps up to and including it: 1: 45/162 = 0.278; 2: 32/60 = 0.533; 3+: 13/17 = 0.765
      by ... in the 10 steps: 1: 35/149 = 0.235; 2: 40/70 = 0.571; 3+: 15/20 = 0.750
      neutral whiffs in the 20 steps up to it: flipped mean 0.00, not flipped 0.02; steps since the last neutral whiff: flipped median 171, not flipped median 171
      released but not flipped (148): hold at the 10th step neutral 0, nothing 148, valued 0; over the next 9 steps the valued unit's peak s median 0.05 (flipped 1.14), the neutral unit's lowest s median 0.68 (flipped 0.53)
      isolated whiff (no other valued whiff in the 9 steps before or the 9 after): 0/46 = 0.000; not isolated 90/193 = 0.466
      by the held unit's s at arrival: [0.0, 1.5): 62/89; [1.5, 1.8): 28/93; [1.8, 2.0): 0/50; [2.0, 2.2): 0/5; [2.2, 2.5): 0/2; [2.5, 5.1): 0/0
      first valued whiff per row: 146 rows (neutral held at it 146); flipped within 10 steps 33, not 113 (rows with a full window 146); when it was the only valued whiff in its 10-step window: flipped 0/46, when more followed: 33/100

(2b) hold transitions and the 'nothing held' route, registered start, 900 steps
   rule on: transitions 0->N 322, 0->V 156, N->0 495
      first valued hold per row (156 rows): entered from nothing held 156, directly from the neutral hold 0
      'nothing held' stretches after a neutral hold: 495; ended by valued 156 (duration quartiles 5.0 / 8.0 / 17.2; valued whiffs in it mean 1.20, neutral whiffs mean 0.14); neutral again 322 (duration quartiles 9.0 / 16.0 / 37.8; valued whiffs in it mean 0.02, neutral whiffs mean 2.12); still nothing at the end 17 (duration quartiles 65.0 / 128.0 / 159.0; valued whiffs in it mean 0.00, neutral whiffs mean 0.82)
   rule off: transitions 0->N 21, 0->V 123, N->0 149
      first valued hold per row (123 rows): entered from nothing held 123, directly from the neutral hold 0
      'nothing held' stretches after a neutral hold: 149; ended by valued 123 (duration quartiles 5.0 / 6.0 / 10.0; valued whiffs in it mean 1.13, neutral whiffs mean 0.02); neutral again 21 (duration quartiles 17.0 / 33.0 / 55.0; valued whiffs in it mean 0.05, neutral whiffs mean 2.38); still nothing at the end 5 (duration quartiles 42.0 / 221.0 / 260.0; valued whiffs in it mean 0.00, neutral whiffs mean 1.20)

(3)+(4) the loop and where the valued whiffs come from, registered start
   rule on (first 600 steps; positions relative to the neutral source, d_along > 0 downwind, d_cross > 0 toward the valued source)
      max upwind excursion (quartiles) 30.2 / 32.4 / 37.8; rows beyond 20 upwind 400
      first return within 5.0 of the neutral source after being beyond 10.0: rows 400/400, step quartiles 141.0 / 142.0 / 143.0; returns per row quartiles 2.0 / 4.0 / 4.0, rows with 0/1/2/3+ returns 0/39/62/299
      first entry into the valued cone (or within 3.0 of the valued source): rows 391, step quartiles 172.0 / 177.0 / 205.0; steps in the valued cone per row quartiles 13.0 / 26.0 / 50.0
      at the first valued whiff (323 rows): step quartiles 177.0 / 201.0 / 214.0; d_along 11.9 / 14.4 / 18.1; d_cross from the neutral axis 5.5 / 6.6 / 7.6; |d_cross| to the valued axis 2.4 / 3.4 / 4.5; cast clock (steps since the last navigation hit) 177.0 / 201.0 / 214.0
      where it came from: within 3.0 of the valued source 5, plume core (|d_cross| < 3.0) 120, cone edge 198; at the median arrival position (d_along 14.4, |d_cross| 3.4; cone half-width there 5.1) the per-step whiff probability is 0.090 (p_hit 0.3 x exp(-d_along/12)); per-row value at arrival quartiles 0.1 / 0.1 / 0.1
   rule off (first 600 steps; positions relative to the neutral source, d_along > 0 downwind, d_cross > 0 toward the valued source)
      max upwind excursion (quartiles) 32.5 / 33.1 / 33.5; rows beyond 20 upwind 400
      first return within 5.0 of the neutral source after being beyond 10.0: rows 400/400, step quartiles 148.0 / 152.0 / 155.0; returns per row quartiles 3.0 / 3.0 / 3.0, rows with 0/1/2/3+ returns 0/4/24/372
      first entry into the valued cone (or within 3.0 of the valued source): rows 94, step quartiles 325.2 / 375.0 / 483.0; steps in the valued cone per row quartiles 0.0 / 0.0 / 0.0
      at the first valued whiff (87 rows): step quartiles 329.5 / 411.0 / 488.0; d_along 6.2 / 8.1 / 9.8; d_cross from the neutral axis 7.6 / 8.3 / 9.4; |d_cross| to the valued axis 1.1 / 1.8 / 2.5; cast clock (steps since the last navigation hit) 166.0 / 170.0 / 174.0
      where it came from: within 3.0 of the valued source 2, plume core (|d_cross| < 3.0) 74, cone edge 11; at the median arrival position (d_along 8.1, |d_cross| 1.8; cone half-width there 3.5) the per-step whiff probability is 0.153 (p_hit 0.3 x exp(-d_along/12)); per-row value at arrival quartiles 0.1 / 0.2 / 0.2

(5) VARIANT start, NOT the bench (a different constructed state): on the neutral axis 20 downwind of the neutral source, heading upwind (180), neutral hold s 2.0 / 0, S 0, cast clock 0; same seeds and rows; 600 steps
   VARIANT rule on
      step | holding valued at t        | ever revised by t | >=1 valued whiff by t | revised, not holding at t | a valued hold ended by t | P(holding | >=1 valued whiff)
       100 |   0/400 = 0.000                  |   0               |   0                   |   0                       |   0                      | nan
       150 |   0/400 = 0.000                  |   0               |   2                   |   0                       |   0                      | 0.000
       200 |   0/400 = 0.000                  |   0               |   9                   |   0                       |   0                      | 0.000
       250 |   0/400 = 0.000                  |   0               |   9                   |   0                       |   0                      | 0.000
       300 |   3/400 = 0.007 [0.003, 0.022]   |   3               |  29                   |   0                       |   0                      | 0.103
       400 |   4/400 = 0.010                  |   4               |  29                   |   0                       |   0                      | 0.138
       500 |  12/400 = 0.030                  |  12               | 109                   |   0                       |   0                      | 0.110
       600 |  33/400 = 0.083 [0.059, 0.114]   |  34               | 191                   |   1                       |   1                      | 0.173
   VARIANT rule off
      step | holding valued at t        | ever revised by t | >=1 valued whiff by t | revised, not holding at t | a valued hold ended by t | P(holding | >=1 valued whiff)
       100 |   0/400 = 0.000                  |   0               |   0                   |   0                       |   0                      | nan
       150 |   0/400 = 0.000                  |   0               |   0                   |   0                       |   0                      | nan
       200 |   0/400 = 0.000                  |   0               |   0                   |   0                       |   0                      | nan
       250 |   2/400 = 0.005                  |   2               |   4                   |   0                       |   0                      | 0.500
       300 |   2/400 = 0.005 [0.001, 0.018]   |   2               |   4                   |   0                       |   0                      | 0.500
       400 |   4/400 = 0.010                  |   4               |  12                   |   0                       |   0                      | 0.333
       500 |   9/400 = 0.022                  |   9               |  16                   |   0                       |   0                      | 0.562
       600 |  34/400 = 0.085 [0.061, 0.116]   |  34               |  50                   |   0                       |   0                      | 0.680
   VARIANT rule on: valued whiffs arriving while the neutral odour is held (events with a full 10-step window): 262 in 191 rows; flipped to the valued odour within 10 steps 10 = 0.038; not flipped but the hold released (nothing held) at some step 206; neutral kept all 10 steps 46
      at arrival: held (neutral) unit s median 2.07 [1.29, 3.11], valued unit s median 0.000, pool S median 2.62
      by valued whiffs in the 5 steps up to and including it: 1: 7/221 = 0.032; 2: 3/39 = 0.077; 3+: 0/2 = 0.000
      by ... in the 10 steps: 1: 5/211 = 0.024; 2: 2/44 = 0.045; 3+: 3/7 = 0.429
      neutral whiffs in the 20 steps up to it: flipped mean 0.40, not flipped 0.89; steps since the last neutral whiff: flipped median 58, not flipped median 19
      released but not flipped (206): hold at the 10th step neutral 2, nothing 204, valued 0; over the next 9 steps the valued unit's peak s median 0.00 (flipped 1.21), the neutral unit's lowest s median 0.77 (flipped 0.55)
      isolated whiff (no other valued whiff in the 9 steps before or the 9 after): 0/155 = 0.000; not isolated 10/107 = 0.093
      by the held unit's s at arrival: [0.0, 1.5): 6/26; [1.5, 1.8): 4/45; [1.8, 2.0): 0/53; [2.0, 2.2): 0/24; [2.2, 2.5): 0/33; [2.5, 5.1): 0/81
      first valued whiff per row: 191 rows (neutral held at it 191); flipped within 10 steps 4, not 187 (rows with a full window 191); when it was the only valued whiff in its 10-step window: flipped 0/145, when more followed: 4/46
   VARIANT rule off: valued whiffs arriving while the neutral odour is held (events with a full 10-step window): 73 in 48 rows; flipped to the valued odour within 10 steps 15 = 0.205; not flipped but the hold released (nothing held) at some step 56; neutral kept all 10 steps 2
      at arrival: held (neutral) unit s median 1.69 [1.15, 1.99], valued unit s median 0.000, pool S median 2.26
      by valued whiffs in the 5 steps up to and including it: 1: 6/51 = 0.118; 2: 9/21 = 0.429; 3+: 0/1 = 0.000
      by ... in the 10 steps: 1: 4/48 = 0.083; 2: 9/22 = 0.409; 3+: 2/3 = 0.667
      neutral whiffs in the 20 steps up to it: flipped mean 0.00, not flipped 0.07; steps since the last neutral whiff: flipped median 175, not flipped median 173
      released but not flipped (56): hold at the 10th step neutral 0, nothing 56, valued 0; over the next 9 steps the valued unit's peak s median 0.03 (flipped 1.18), the neutral unit's lowest s median 0.69 (flipped 0.52)
      isolated whiff (no other valued whiff in the 9 steps before or the 9 after): 0/20 = 0.000; not isolated 15/53 = 0.283
      by the held unit's s at arrival: [0.0, 1.5): 12/21; [1.5, 1.8): 3/30; [1.8, 2.0): 0/20; [2.0, 2.2): 0/0; [2.2, 2.5): 0/1; [2.5, 5.1): 0/1
      first valued whiff per row: 50 rows (neutral held at it 50); flipped within 10 steps 4, not 46 (rows with a full window 48); when it was the only valued whiff in its 10-step window: flipped 0/21, when more followed: 4/29
   VARIANT rule on: transitions 0->N 127, 0->V 34, N->0 196, V->0 1
      first valued hold per row (34 rows): entered from nothing held 34, directly from the neutral hold 0
      'nothing held' stretches after a neutral hold: 196; ended by valued 34 (duration quartiles 5.0 / 8.0 / 43.5; valued whiffs in it mean 1.32, neutral whiffs mean 0.26); neutral again 127 (duration quartiles 12.5 / 21.0 / 73.5; valued whiffs in it mean 0.01, neutral whiffs mean 2.07); still nothing at the end 35 (duration quartiles 50.0 / 55.0 / 78.5; valued whiffs in it mean 0.03, neutral whiffs mean 0.66)
   VARIANT rule off: transitions 0->N 11, 0->V 34, N->0 47
      first valued hold per row (34 rows): entered from nothing held 34, directly from the neutral hold 0
      'nothing held' stretches after a neutral hold: 47; ended by valued 34 (duration quartiles 5.0 / 7.0 / 15.0; valued whiffs in it mean 1.06, neutral whiffs mean 0.09); neutral again 11 (duration quartiles 12.0 / 20.0 / 39.0; valued whiffs in it mean 0.00, neutral whiffs mean 2.00); still nothing at the end 2 (duration quartiles 120.2 / 168.5 / 216.8; valued whiffs in it mean 0.00, neutral whiffs mean 2.00)
   VARIANT rule on (first 600 steps; positions relative to the neutral source, d_along > 0 downwind, d_cross > 0 toward the valued source)
      max upwind excursion (quartiles) 18.0 / 20.1 / 22.3; rows beyond 20 upwind 212
      first return within 5.0 of the neutral source after being beyond 10.0: rows 400/400, step quartiles 31.0 / 32.0 / 33.0; returns per row quartiles 5.0 / 5.0 / 5.0, rows with 0/1/2/3+ returns 0/0/0/400
      first entry into the valued cone (or within 3.0 of the valued source): rows 362, step quartiles 254.0 / 446.0 / 474.8; steps in the valued cone per row quartiles 5.0 / 12.0 / 21.0
      at the first valued whiff (191 rows): step quartiles 447.5 / 473.0 / 532.5; d_along 17.3 / 21.2 / 23.6; d_cross from the neutral axis 3.7 / 4.8 / 6.1; |d_cross| to the valued axis 3.9 / 5.2 / 6.3; cast clock (steps since the last navigation hit) 447.5 / 473.0 / 532.5
      where it came from: within 3.0 of the valued source 2, plume core (|d_cross| < 3.0) 24, cone edge 165; at the median arrival position (d_along 21.2, |d_cross| 5.2; cone half-width there 6.8) the per-step whiff probability is 0.051 (p_hit 0.3 x exp(-d_along/12)); per-row value at arrival quartiles 0.0 / 0.1 / 0.1
   VARIANT rule off (first 600 steps; positions relative to the neutral source, d_along > 0 downwind, d_cross > 0 toward the valued source)
      max upwind excursion (quartiles) 32.2 / 32.9 / 33.4; rows beyond 20 upwind 400
      first return within 5.0 of the neutral source after being beyond 10.0: rows 400/400, step quartiles 26.0 / 26.0 / 27.0; returns per row quartiles 4.0 / 4.0 / 4.0, rows with 0/1/2/3+ returns 0/0/1/399
      first entry into the valued cone (or within 3.0 of the valued source): rows 57, step quartiles 366.0 / 509.0 / 521.0; steps in the valued cone per row quartiles 0.0 / 0.0 / 0.0
      at the first valued whiff (50 rows): step quartiles 467.8 / 519.0 / 532.5; d_along 6.5 / 9.6 / 13.4; d_cross from the neutral axis 7.5 / 8.1 / 10.1; |d_cross| to the valued axis 0.8 / 2.2 / 2.7; cast clock (steps since the last navigation hit) 165.0 / 172.0 / 180.8
      where it came from: within 3.0 of the valued source 3, plume core (|d_cross| < 3.0) 40, cone edge 7; at the median arrival position (d_along 9.6, |d_cross| 2.2; cone half-width there 3.9) the per-step whiff probability is 0.135 (p_hit 0.3 x exp(-d_along/12)); per-row value at arrival quartiles 0.1 / 0.1 / 0.2

(6) silence and walls
   registered start, rule on : t 300: no whiff of either plume in the last 100 steps 12, wall contacts 0; t 600: no whiff of either plume in the last 100 steps 98, wall contacts 0; t 900: no whiff of either plume in the last 100 steps 233, wall contacts 0
   registered start, rule off: t 300: no whiff of either plume in the last 100 steps 361, wall contacts 0; t 600: no whiff of either plume in the last 100 steps 247, wall contacts 0; t 900: no whiff of either plume in the last 100 steps 160, wall contacts 0
   VARIANT start,    rule on : t 300: no whiff of either plume in the last 100 steps 5, wall contacts 0; t 600: no whiff of either plume in the last 100 steps 26, wall contacts 0
   VARIANT start,    rule off: t 300: no whiff of either plume in the last 100 steps 302, wall contacts 0; t 600: no whiff of either plume in the last 100 steps 119, wall contacts 0
