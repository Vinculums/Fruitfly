# H26 report: adaptive presence (the presence prior separated from the presence window)

Date 2026-09-25. Design v2 FINAL doc d54441658b54a6799 (confirmed by the owner 2026-09-24, decision:h26-open, '권고안대로 확정하고 H26 진행', gloss 'confirm as recommended and proceed with H26'; hash ac95c22d51838604912aa5537580686b93b3fece76827721c03564973ee09f54, equal to the local file's sha256). Code src/ph28.py sha256 64ce7d0ce123f912aa675e86627d5b6b0ae3d89976b093666316e6b78441e7aa (source doc d4f81b6d946b6ccfb, content_hash equal; the demo and bench ran on 29c594e49a839e327e87290fd253a80034997ae2d2b88fff8b604d58776c9dd7, and only the bar constant BARS['T2'] changed between the two). One evaluation, world seed 1985, agent seed 2085, 400 rows x 600 steps, G 2, gate on where G 2, geometry C0, t0 150, 95 percent intervals, bootstrap 5000 seed 20261073, no extension. Evaluation output experiments/h26/ph28_eval.txt sha256 87ece381471bdbb6a4a5ec66551d82b06775d9e924b3976350dd8dfdbf2be922. Nothing was changed after the table.

**Status: H26 SHOWN under its registered criteria: M1, M2, M3, M4, M5, M6, M7 all PASS; M8 (T3b, T4) reported, not part of the PASS condition.** The printout's summary label is the registered verdict sentence: with v_max scoped to odours present by a per-odour counter whose window is 300 steps after a whiff and whose prior, before the odour is first sensed, is 59 steps, the adopted agent keeps H23's result in the H21 task within 0.05 of Agent10 and at P(V) of at least 0.88 (P(V) 0.927, DP -0.0075 [-0.020, +0.005]); in the absent-odour world it tracks the only odour present within the registered dwell gap of the unfiltered agent (paired dwell Agent14 - Agent6 -1.047 [-2.043, -0.075] against the bar -4.9); and after the valued odour is lost from step 0 it opens the filter exactly at step 59 (400/400) and recovers at least half of the ceiling-floor span (R 1.0376 [0.9642, 1.1186]). A statement about supplied values +1/0, G 2, C0, learning off, these worlds, and the 59-step prior under the signed H26-scoped relaxation (decision:classification-rule-relaxed-presence-prior-h26). **Not about a loss after tracking** (T3b: there the window is a fixed 300 steps) **or negative values** (T4 reported only). Closure is the owner's.

## 1. What was asked

H26 (design v2 section 1): an agent whose value filter takes v_max over the odours present, where an odour is present while held or for N_hi = 300 steps after its last whiff and, before it has ever been sensed in the run, only on the first P - 1 = 59 steps (a prior), does three things at +1/0 against the adopted agent Agent10 (= Release + Agent8): (i) in the H21 choice task it keeps H23's result, P(V) at least 0.88 and within 0.05 of Agent10 [M2]; (ii) in the absent-odour world W1 it tracks the only odour present within the registered dwell gap of the unfiltered agent Agent6 [M5]; (iii) after the valued odour is lost from step 0 (T3a) it opens the filter exactly at step 59 and recovers at least half of the ceiling-floor span [M7]. The agent is Agent14 = ph24.Release + ph23.Agent9 whose presence counter starts at N_hi - P = 240 instead of 0: the only change from H24 Run 2's Agent11, and no second state variable. The owner confirmed every recommended option of design v1 section 12 (candidate (e), P 60, N_hi 300, the relaxation signed in the owner's words, the bars with M5(d) re-signed against Agent10 (decision:h26-m5d-bar-resigned), stop rules (h) and (h3) with (m) printed first, the seeds, the order H26 -> H20 Stage B).

## 2. Implementation, self-checks, bench, bar decision, development run

ph28.py composes Agent14 from adopted and earlier modules without editing any of them (ph21.py, ph24.py adopted; ph23.py, ph25.py, ph25b.py imported unchanged, sha256 in every output header). Its constructor calls Agent9's with N = N_hi and sets the counter to N_hi - P. Readings R1-R11 where the design is silent are stated in the file header and printed in the bench output (e.g. R3, the at-risk set of (m); R4, what 'departs from Agent11 (N 300)' means; R8, the Lost-world window check).

**Self-checks (demo, experiments/h26/ph28_demo.txt sha256 df003ecfb6e214e43f030a2dd6e0834189186920be5bfc2fa2a5361d63c444ab, on 29c594e4...):** every check ok: the make hooks leave every field of ph24.run / ph24.stub bitwise equal for ph24's and ph25's agents; ph25b's N wrapper reproduces ph25.Agent11 at N 60; Agent14 scope 'off' == Agent10, (P 60, N_hi 60) == ph25.Agent11 and, release off, == ph23.Agent9; 0/0, +1/+1, +1/-1 == Agent10; presence identity and separation; early-whiff rows bitwise Agent11 (N 300); W1 and T3a == Agent11 (N 60); the counter convention; the pass-probability arithmetic reproduces design section 7; the seed scan (15 numbers, 181 files, no hit). **Implementation errors at run time: none recorded** (the demo header reads 'fixed before this recorded demo: none').

**Mechanism bench (M4), experiments/h26/ph28_bench.txt sha256 2f3012d1d35689216c1ca05819a5c5344ea6031f6d1731fb14f74a08367a81c1, record:h26-bench-result: PASS; both stop rules continue.**
- (a) identities all True, including (a1') (P 60, N_hi 60) == ph25.Agent11 on every field with the counter; (a5) W1 == Agent11 (N 60) on every field with the valued counter exactly Agent11's + 240; (a6) the same in T3a; (a7) 289/400 T1 rows with a valued whiff by step 58, all 289 bitwise Agent11 (N 300); 15 rows depart from Agent11 (N 300), all 15 in the at-risk set.
- (b) counter exact 400/400 = 1.000 [0.990, 1.000] in every schedule; held-only presence 0.
- (d) W1 first surge == the first B whiff at or after step 59 in 400/400; D6_W1 (Agent6) 24.7200; Agent14 22.942 == Agent11 (N 60); paired Agent14 - Agent6 -1.7775 (sd 10.3360).
- (e) 400/400 twice; (f) M7(a) T3a 400/400; the Lost-world post-whiff window exact at L + 300 in 385/385 eligible rows.
- (m) printed before (h): at-risk rows 15 (literal reading 109); out of V Agent14 1, Agent11 (N 300) 0, so k = 1; M2(b) at k 1.0000.
- (h) T1 on bench seeds: Agent14 382/18/0 = 0.955, Agent10 381/19/0 = 0.953; DP +0.0025 [-0.0050, +0.0100]; M2(b) pass probability 1.0000 -> continue. (h3) M5(b) pass probability at -1.7775 with bar_T2 -4.9: 1.0000 -> continue.

**Bar decision (decision:h26-t2-dwell-bar, recorded 2026-09-25 before ph28.py was touched and before any task seed was used):** bar_T2 = -0.20 x D6_W1 = -0.20 x 24.7200 = -4.944, rounded to 0.1 = **-4.9**, from the bench (d) line; the bench's own M5(b) reading (-1.7775) is reported there, not a verdict. The constant was then written into ph28.py as BARS['T2'] = -4.9, the one line that changed (29c594e4... -> 64ce7d0c...). The demo self-checks were re-run on the new file (experiments/h26/ph28_demo_bar.txt sha256 1ce83778bd8c46a099bca8acf5fdf6406a0385c8191a36a33c5f215a7a2c916f): every line equal to the recorded demo except the file's sha256 in the header and the BARS line ('BARS {'T2': -4.9} (set)'). The bench was not re-run as a step; dev and eval re-run it internally for M4 (reading R11), and both reproduce the bench's M4 lines exactly (8 of 8 printed lines).

**Development run (seeds 9977/9987, experiments/h26/ph28_dev.txt sha256 1608c56b94f7998f3cbcbfb0698c69d6411125746fc3ac5cc542ca3ec2fde208, record:h26-dev-run):** no operation error, no amendment ('amendments: none'). (Its printout read every criterion PASS: T1 Agent14 0.925 vs Agent10 0.938, DP -0.012; W1 -0.547 against -4.9; R 0.9867. That printout is not the verdict.) The evaluation seeds were unused until the one evaluation.

**Record-keeping, stated:** this run was resumed after the previous agent was cut off right after the bench; record:h26-bench-result was written at the resumption. The graph server was intermittently unreachable. record:h26-dev-run could be written only while the evaluation was already running (no amendment existed to record). The source doc's re-put with the new hash was first acknowledged by the server during the development run but did not persist (a read-back returned the old version); it was re-put and verified equal to the file after the evaluation had run. The code that ran is identified by the sha256 printed in each output header.

## 3. Results, one evaluation (seeds 1985 / 2085)

**T1, the H21 choice task (+1/0, dwell majority).**

| arm | agent | values | V | N | tie | P(V) [95%] | P(V \| first hold valued) | P(V \| first hold neutral) |
|---|---|---|---|---|---|---|---|---|
| adaptive (main) | Agent14 (P 60, N_hi 300) | +1/0 | 371 | 28 | 1 | 0.927 [0.898, 0.949] | 267/275 | 104/125 |
| base | Agent10 | +1/0 | 374 | 25 | 1 | 0.935 [0.906, 0.955] | 267/275 | 107/125 |
| fixed window N 300 | Agent11 | +1/0 | 374 | 26 | 0 | 0.935 [0.906, 0.955] | 267/275 | 107/125 |
| fixed window N 60 | Agent11 | +1/0 | 319 | 76 | 5 | 0.797 [0.755, 0.834] | 222/275 | 97/125 |
| filter | Agent8 | +1/0 | 374 | 25 | 1 | 0.935 [0.906, 0.955] | 267/275 | 107/125 |
| release-maintain | Agent10g | +1/0 | 254 | 139 | 7 | 0.635 [0.587, 0.681] | 223/278 | 31/122 |
| maintain | Agent6 | +1/0 | 296 | 101 | 3 | 0.740 [0.695, 0.781] | 269/278 | 27/122 |
| pathway-off | Agent8 G 0, gate off, filter off | +1/0 | 213 | 182 | 5 | 0.532 (floor: P(V \| chose) 0.539) | 170/206 | 43/192 |
| known-answer | Agent5 fixed valued | +1/0 | 379 | 19 | 2 | 0.948 [0.921, 0.965] | 379/400 | - |
| neutral | Agent14 (== Agent10 bitwise) | 0/0 | 210 | 183 | 7 | 0.525 (side balance 0.509) | 156/206 | 54/192 |

Paired: **Agent14 - Agent10 DP -0.0075 [-0.020, +0.005]** (into V 2, out of V 5); Agent14 - Agent11 (N 300) -0.0075 [-0.0200, +0.0050]; Agent14 - Agent8 -0.0075; Agent14 - Agent11 (N 60) +0.1300 [+0.0975, +0.1650]; Agent14 - Agent10g +0.292 [+0.243, +0.340]; Agent14 - Agent6 +0.1875 [+0.1450, +0.2300]. Where the value goes: 374 rows bitwise Agent10 throughout, 26 departing (first `differs8` step 104/112/148); 288/400 rows with a valued whiff by step 58, all bitwise Agent11 (N 300); at-risk rows 20, rows departing from Agent11 (N 300) 20, all in the at-risk set; out of V Agent14 5, Agent11 (N 300) 0, **k = 5**. Agent11 (N 300) `differs8` rows 16 (first 307/426/455); Agent11 (N 60) 122 (199/350/371). Lost rows (no whiff of either plume in the last third) 0 vs 0; wall contacts 0 in every arm.

**T2, W1 (the valued column masked from step 0).**

| arm | agent | dwell within 3.0 of the present source, mean (quartiles) | reach | lost rows | first surge (quartiles; rows) |
|---|---|---|---|---|---|
| adaptive | Agent14 | 23.782 (19.0 / 24.5 / 30.0) | 385/400 | 35 | 113 / 123 / 149; 383 |
| fixed window N 60 | Agent11 | 23.782 (identical row for row) | 385/400 | 35 | 113 / 123 / 149; 383 |
| maintain | Agent6 | 24.830 (20.0 / 25.0 / 30.0) | 396/400 | 16 | 4 / 12 / 110; 396 |
| release-maintain | Agent10g | 24.830 (== Agent6 row for row) | 396/400 | 16 | 4 / 12 / 110; 396 |
| base | Agent10 | 12.335 (6.0 / 9.0 / 18.2) | 338/400 | 45 | none |

Paired dwell Agent14 - Agent6 -1.047 [-2.043, -0.075] (sd 9.846; the reported line prints the same mean as -1.048); Agent14 - Agent10 +11.447. W3 (0/0): Agent14 == Agent10 bitwise. Masked draws equal the World7 twin in every arm.

**T3a, lost at the valued source from step 0 (constructed).**

| arm | valued hold ended | first neutral surge (rows) | first within 3.0 of the neutral source (rows) | neutral dwell 100-599, mean (quartiles) |
|---|---|---|---|---|
| Agent14 | 47 / 47 / 47 | 175 / 189 / 211 (318) | 197 / 239 / 306 (316) | 13.680 (6 / 15 / 21) |
| Agent11 (N 60), Agent10g | identical to Agent14 | | | 13.680 |
| floor: Agent10 | 47 / 47 / 47 | none | 470 / 511 / 534 (71) | 1.040 (0 / 0 / 0) |
| ceiling: Agent5 fixed neutral | - | - | | 13.223 (5 / 14 / 20) |

Span 12.183 [11.225, 13.150]; **R = (13.680 - 1.040) / 12.183 = 1.0376 [0.9642, 1.1186]**.

**T3b, the Lost world (t0 150; REPORTED).** Neutral dwell 400-599: Agent14 4.412, Agent10 2.312, Agent10g 7.048, Agent11 (N 60) 5.772. Agent14: 379 eligible rows, the post-whiff window exact at L + 300 in 379/379; first neutral surge 471/476/479 steps after the last valued whiff (none in 173 rows); valued holds at t0 (180) all ended at origin + 48.

**T4, +1/-1 (World7; REPORTED, outside the verdict).** Agent14 == Agent10 bitwise: V 309, N 33, tie 58, P(V) 0.772 [0.729, 0.811], lost rows 123, contacts 0.

## 4. Criteria (registered bars only)

| criterion | measured | bar | result |
|---|---|---|---|
| M1(a) ties: neutral / pathway-off / known-answer | 7/400, 5/400, 2/400 | <= 0.20 each | PASS |
| M1(b) neutral side balance P(+y \| chose) | 200/393 = 0.509 [0.460, 0.558] | within [0.35, 0.65] | PASS |
| M1(c) floor, pathway-off P(V \| chose) | 213/395 = 0.539 [0.490, 0.588] | within [0.35, 0.65] | PASS |
| M1(d) ceiling, known-answer P(V) | 379/400 = 0.948 [0.921, 0.965] | lower bound >= 0.85 | PASS |
| M2(a) Agent14 P(V) | 371/400 = 0.927 [0.898, 0.949] | lower bound >= 0.88 | PASS |
| M2(b) DP Agent14 - Agent10 | -0.0075 [-0.020, +0.005] | lower bound >= -0.05 | PASS |
| M2(c) DP Agent14 - Agent10g | +0.292 [+0.243, +0.340] | lower bound >= +0.05 | PASS |
| M3 identities (14 listed in the output) | all True | all True | PASS |
| M4 mechanism bench (re-run on bench seeds) | identities True; bar lower bounds 0.9905 x5, 0.9901 | identities; each >= 0.95 | PASS |
| M5(a) W1 reach within 3.0 | 385/400 = 0.963 [0.939, 0.977] | lower bound >= 0.80 | PASS |
| M5(b) W1 paired dwell Agent14 - Agent6 | -1.047 [-2.043, -0.075] | lower bound >= -4.9 (decision:h26-t2-dwell-bar) | PASS |
| M5(c) W1 wall contacts per row | 0.000 | <= 0.10 | PASS |
| M5(d) W1 lost rows DP Agent14 - Agent10 (re-signed) | -0.025 [-0.055, +0.005] | upper bound <= +0.05 | PASS |
| M5(e) W1 first surge = first B whiff at or after 59 | 400/400 | every row | PASS |
| M6(a) T1 lost rows DP Agent14 - Agent10 | 0.000 [0.000, 0.000] | upper bound <= +0.05 | PASS |
| M6(b) T1 wall contacts per row | 0.000 | <= 0.10 | PASS |
| M7(a) T3a window exact | 400/400 = 1.000 [0.990, 1.000] | lower bound >= 0.95 | PASS |
| M7(b) readability: span | 12.183 [11.225, 13.150] | lower bound >= 5.0 | readable |
| M7(b) R | 1.0376 [0.9642, 1.1186] | lower bound >= 0.50 | PASS |
| M7(c) T3a construction; == Agent11 (N 60); == Agent10 on 0-58 | True | True | PASS |
| M8 T3b, T4 | section 3 | reported | - |

Ties in the arms under test (section 8): adaptive 0.003, base 0.003, release-maintain 0.018 (unreadable above 0.20). **H26 under the registered criteria: SHOWN** (M1-M7 PASS). Reported beside M5(d), not a criterion: lost rows Agent14 35, Agent10 45, Agent6 16; DP Agent14 - Agent6 +0.0475 [+0.0200, +0.0775].

**Identities (M3, all True):** scope off == Agent10 (T1); (P 60, N_hi 60) == Agent11 (T1, with the counter); neutral 0/0 == Agent10; +1/-1 == Agent10 (reported identity); presence identity in T1, W1, T3a; separation vs Agent10 (T1: 374 never `differs8`, all equal throughout; 26 equal before their first `differs8`); W1 == Agent11 (N 60) on every field with the counter + 240, == Agent10 on 0-58, nav == nav6 from 59; T3a == Agent11 (N 60); T1 early-whiff rows == Agent11 (N 300); T1 departing rows in the at-risk set; W3 == Agent10; masked draws == the World7 twin (W1, W3, T3a, T3b); T3a construction in every arm; T3b == T1 on steps 0-149.

## 5. Predictions (design v2 section 10) against the observations

| prediction | observed | |
|---|---|---|
| bench identities True; (b), (d), (e), (f) exact | all True; 400/400, 400/400, 385/385 | met |
| bench (m) at-risk rows a minority | 15/400 | met |
| bench (h) DP 0 to -0.025 | +0.0025 | NOT met as stated (just above the range, the favourable side) |
| bench (h3) pass probability about 1 | 1.0000 | met |
| T1 Agent10 0.93-0.97 | 0.935 | met |
| T1 Agent14 - Agent10 0 to -0.025 (k 0 to 10) | -0.0075 (k 5) | met |
| T1 Agent11 (N 300) equal to Agent10 in outcome | V 374 both | met in V (N/tie 26/0 against Agent10's 25/1) |
| T1 Agent11 (N 60) about -0.17 | -0.1375 (0.797 vs 0.935) | NOT met (a smaller cost) |
| T1 Agent10g 0.55-0.65 | 0.635 | met |
| W1 Agent14 == Agent11 (N 60) | identical row for row | met |
| W1 dwell about 22-24 against Agent6 about 24-26, paired about -1.7 | 23.782 vs 24.830, paired -1.047 | dwell met; paired gap smaller than predicted |
| W1 Agent10 about 12 | 12.335 | met |
| W1 reach 0.96-0.98 | 0.963 | met |
| W1 lost rows about 28-30, Agent6 10-14, Agent10 33-36 | 35, 16, 45 | NOT met (all three higher) |
| W1 contacts 0 | 0.000 | met |
| T3a M7(a) exact at 59 | 400/400 | met |
| T3a R 0.95 to 1.0 | 1.0376 | NOT met (above the range) |
| T3a floor 0.8-0.9, ceiling about 14 | 1.040, 13.223 | floor NOT met (higher); ceiling about 0.8 below 14 |
| T3b between Agent10 (about 2.1) and Agent11 (N 60) (5.6), nearer Agent10's | 4.412 between 2.312 and 5.772, nearer Agent11 (N 60)'s (midpoint 4.042) | between met; 'nearer Agent10's' NOT met |
| T4 Agent14 == Agent10 bitwise | True | met |

## 6. What is shown and what is not

- **Shown (registered):** the prior separated from the window does what the design reads from the code, and the registered bars hold on the evaluation seeds. In W1 and T3a Agent14 is H24 Run 2's Agent11 at N 60 row for row (the valued odour is never sensed there, so only the 59-step prior acts); in T1 it is Agent11 at N 300 in every row with a valued whiff by step 58 (288/400), and it departs from it only in the at-risk rows the design named (20/20). The T1 cost the fixed N 60 window paid (0.797 against 0.935) is not paid (0.927, DP -0.0075 [-0.020, +0.005]); the W1 absent-odour cost of the adopted agent (12.335 against Agent6's 24.830) is removed to within -1.047 [-2.043, -0.075]; after a constructed loss the filter opens exactly at step 59 and R is 1.0376 [0.9642, 1.1186].
- **The T1 cost that remains, stated:** 5 rows leave V and 2 enter (net 3 of 400); all 5 lie in the at-risk rows (no valued whiff by step 58, then a neutral whiff with nothing or the neutral odour held before the first valued whiff). This is the population design 2.5 said no presence rule on the agent's own history can serve; it was measured, not removed.
- **Measured, not a criterion:** W1 lost rows against the unfiltered agent: DP Agent14 - Agent6 +0.0475 [+0.0200, +0.0775] (35 vs 16). Under the inherited form of M5(d) (DP against Agent6, upper bound <= +0.05), which the owner re-signed before any code (decision:h26-m5d-bar-resigned), this would not have passed (upper bound 0.0775). The registered M5(d) is the re-signed one, and it passes; the gap to Agent6 is the price of the 59-step prior and is reported, not judged. W1 first surge 113/123/149 against Agent6's 4/12/110: the prior delays the first neutral surge to the first B whiff at or after step 59 in every row (400/400).
- **Not shown:** a loss after tracking. In the Lost world the window after the last valued whiff is a fixed 300 steps (exact in 379/379), so the first neutral surge comes 471/476/479 steps after it and the late neutral dwell (4.412) stays below the fixed-60 agent's (5.772) and the release-maintain agent's (7.048). Negative values: T4 only reported (Agent14 == Agent10; the release stays on hold at negative values, decision:release-negative-scope-on-hold).
- **Predictions missed, stated (section 5):** the W1 lost-row counts (35, 16, 45 against 28-30, 10-14, 33-36), the T3a R and floor (above their ranges), the T1 cost of Agent11 (N 60) (-0.1375, not about -0.17), the bench (h) range (+0.0025, above 0) and T3b's 'nearer Agent10's'. None enters a bar.
- **Not tested:** learning (H20 Stage B); other P or N_hi (60 and 300 only); other values, G, geometries or starts; another RESET_AFTER; a behaviour that shortens T1's valued silences; the rejected candidates (a)-(d) of design 3.1; whether a fly keeps such a counter or prior (no fly finding is cited or claimed). The prior is a prior, recorded as such under the H26-only relaxation, not evidence.

## 7. Provenance

- Design v2 FINAL doc d54441658b54a6799 (experiments/h26/h26_design_v2.md, sha256 ac95c22d51838604912aa5537580686b93b3fece76827721c03564973ee09f54); v1 DRAFT doc d9452710c5166ba01 (experiments/h26/h26_design_v1.md, sha256 18983aa2cefbbd61310a42d07eb30eb4d7df8e82288e9eaa6ca839073a073598); decision:h26-open-design, decision:h26-open, decision:classification-rule-relaxed-presence-prior-h26, decision:h26-m5d-bar-resigned, decision:h26-t2-dwell-bar.
- Code src/ph28.py sha256 64ce7d0ce123f912aa675e86627d5b6b0ae3d89976b093666316e6b78441e7aa (dev and eval; source doc d4f81b6d946b6ccfb, content_hash equal); 29c594e49a839e327e87290fd253a80034997ae2d2b88fff8b604d58776c9dd7 (demo and bench; BARS unset; the same text with BARS['T2'] None). Imported unchanged (sha256 in every output header): ph15 cc939996...3fdc, ph21 3a1d79d9...cfc1, ph22 03ab8c47...ca1c, ph23 ae180492...b5ae, ph24 f344f178...1bef, ph25 5620a908...7d91, ph25b ad12a912...eaf6.
- Outputs (LF): ph28_demo.txt df003ecfb6e214e43f030a2dd6e0834189186920be5bfc2fa2a5361d63c444ab; ph28_bench.txt 2f3012d1d35689216c1ca05819a5c5344ea6031f6d1731fb14f74a08367a81c1 (record:h26-bench-result); ph28_demo_bar.txt 1ce83778bd8c46a099bca8acf5fdf6406a0385c8191a36a33c5f215a7a2c916f; ph28_dev.txt 1608c56b94f7998f3cbcbfb0698c69d6411125746fc3ac5cc542ca3ec2fde208 (record:h26-dev-run); ph28_eval.txt 87ece381471bdbb6a4a5ec66551d82b06775d9e924b3976350dd8dfdbf2be922 (record:h26-result). The outputs are committed beside this report and are not reproduced in it.
- Seeds: development 9977/9987, evaluation 1985/2085 (now spent), bench 20261071/20261072, bootstrap 20261073; seed self-check clean in every run (181 files). Python 3.11.15, numpy 2.4.6.
- Closure is the owner's.
