# H24 Run 2 N sweep: the H21 choice-task cost against the absent-odour benefit as the presence window N grows

Date 2026-09-24. Measurement only, at the owner's instruction (decision:h24-run2-n-sweep: '우리 그 다음 테스트는 추천안대로', the recommended option 1). H24 Run 2 stays stopped at bench (h) (record:h24-run2-bench-result); no rule, bar or seed changes; no task run on registered seeds (dev 9919/9929 and eval 1815/1915 unused). Bench seeds 20261041/20261042, bootstrap 20261043 (5000), 400 rows x 600 steps per world. Code src/ph25b.py (sha256 ad12a9122c171dd32c3fceac946add9d0eb0380e885e0f0872dd97ccd59eeaf6, source doc df429960dec38ae4c), which imports src/ph25.py unchanged (sha256 5620a90819693379a53374ca3841e3bc3ddba860d8a8351da7aa1ed4dfe17d91) and adds one run-time wrapper on ph24.make that sets Agent11's N. Output experiments/h24/ph25b_nsweep.txt (sha256 515340477ad7a7a2be74a9b711dd2a7108415d9c8e0da814959dcb67cd78ecc7). This report names no cause beyond what was measured and tests no change.

## 1. Checks

- Reproduction at N 60 (asserted before the sweep): T1 V/N/tie 314/81/5, paired DP -0.1725 [-0.2125, -0.1350]; W1 dwell 22.733; T3a dwell 14.490, R 1.005. All equal the bench record.
- N inf: the arm is Agent10 itself; Agent11 with N = inf equals Agent10 bitwise in T1 (True).
- References: Agent10 T1 383/15/2; W1 dwell Agent6 24.4325, Agent10 11.902; bar_T2 by the design's rule -4.9; T3a floor 0.807, ceiling 14.420, span 13.613, per-row paired sd 9.941.
- At every finite N: W1 first surge = first B whiff at or after step N - 1 in 400/400; T3a first surge = first neutral whiff at or after N - 1 in 400/400; T3a valued hold ends at step 47 in 400/400; T3a construction True.
- ph25.seeds_unused() after the run: no hits (the output prints no seed digits for this reason).

## 2. The table

Targets: T1 DP lower bound >= -0.05 AND W1 dwell >= 0.8 x 24.4325 = 19.546 with M5(b) pass probability (bar -4.9) >= 0.5. Pass probabilities by design v2 section 7 arithmetic. "Seduced": fraction of 400 rows where a valued hold was ended by a timeout drive and the valued presence flag then went False (c >= N, not held) before the valued hold re-formed; in World7 the valued source is in the world throughout.

| N | T1 V/N/tie | T1 DP vs Agent10 [95%] | M2(b) pp | M2(a) pp | W1 dwell | W1 - Agent6 [95%] | M5(b) pp | T3a R [95%] | seduced |
|---|---|---|---|---|---|---|---|---|---|
| 60 | 314/81/5 | -0.1725 [-0.2125, -0.1350] | 0.0000 | 0.0000 | 22.733 | -1.700 [-2.680, -0.730] | 1.0000 | 1.005 [0.936, 1.077] | 0.970 |
| 90 | 314/81/5 | -0.1725 [-0.2125, -0.1350] | 0.0000 | 0.0000 | 22.733 | -1.700 [-2.680, -0.730] | 1.0000 | 1.005 [0.936, 1.077] | 0.970 |
| 120 | 316/79/5 | -0.1675 [-0.2075, -0.1325] | 0.0000 | 0.0000 | 24.805 | +0.373 [-0.818, +1.550] | 1.0000 | 1.005 [0.936, 1.077] | 0.968 |
| 150 | 318/77/5 | -0.1625 [-0.2000, -0.1275] | 0.0000 | 0.0000 | 19.608 | -4.825 [-5.985, -3.735] | 0.0337 | 1.005 [0.936, 1.077] | 0.973 |
| 200 | 378/20/2 | -0.0125 [-0.0250, -0.0025] | 1.0000 | 0.9971 | 17.775 | -6.658 [-7.720, -5.600] | 0.0000 | 0.771 [0.701, 0.845] | 0.273 |
| 300 | 383/15/2 | 0.0000 [0.0000, 0.0000] | 1.0000 | 1.0000 | 15.098 | -9.335 [-10.428, -8.252] | 0.0000 | 0.260 [0.227, 0.293] | 0.030 |
| 450 | 383/15/2 | 0.0000 [0.0000, 0.0000] | 1.0000 | 1.0000 | 14.585 | -9.848 [-11.038, -8.658] | 0.0000 | 0.259 [0.227, 0.293] | 0.015 |
| inf | 383/15/2 | 0.0000 | 1.0000 | 1.0000 | 11.902 | -12.530 [-13.823, -11.202] | 0.0000 | 0.000 | 0 |

Smallest N meeting both targets: **none of the swept N.** T1's target is met from N 200 up; W1's (dwell and M5(b)) at N 60, 90 and 120 only; N 150 clears the dwell level (19.608) but not M5(b) (pass probability 0.034).

## 3. Diagnostics per N (T1)

| N | rows out of V / into V | first `differs8` rows, step q1/med/q3 | re-held valued after first `differs8` | seduced rows (of 389-394 with a drive-ended valued hold) | expiry step | after expiry: re-held valued / reached valued / V at 600 |
|---|---|---|---|---|---|---|
| 60 | 70 / 1 | 130, 204/354/373 | 10 | 388 | 78/97/102 | 345 / 367 / 314 |
| 90 | 70 / 1 | 130, 204/354/373 | 10 | 388 | 108/127/132 | 345 / 367 / 314 |
| 120 | 67 / 0 | 124, 208/356/376 | 3 | 387 | 155/159/238 | 346 / 367 / 316 |
| 150 | 65 / 0 | 122, 209/357/380 | 4 | 389 | 189/270/301 | 345 / 368 / 317 |
| 200 | 5 / 0 | 28, 270/280/419 | 8 | 109 | 239/392/480 | 94 / 83 / 100 |
| 300 | 0 / 0 | 13, 303/405/440 | 3 | 12 | 318/428/493 | 3 / 4 / 10 |
| 450 | 0 / 0 | 8, 455/468/519 | 1 | 6 | 462/480/552 | 2 / 3 / 4 |

Every out-of-V row is a `differs8` row at every N. Other measured facts: W1 first surge 114/124/157 at N 60 and 90, 122/140/257 at 120, 156/266/289 at 150, 265/272/439 at 200, 419/442/468 at 300; W1 reach 388 (60-120), 379 (150, 200), 369 (300), 359 (450), 336 (inf); T3a first neutral surge 176/186/212 through N 150, 213/235/243 at 200, 476/479/507 at 300 and 450.

## 4. Reading (labelled; not tested)

(a) **Does an N meet both targets?** Not on the swept grid. The nearest miss on each side: N 120 meets W1 (dwell 24.8, M5(b) 1.000) and T3a (R 1.005) but costs T1 -0.1675 [-0.2075, -0.1325]; N 200 meets T1 (DP -0.0125, lower bound -0.025, M2(a) 0.997) and T3a (R 0.771, M7(b) 1.000) but W1 dwell falls to 17.8 (paired -6.66 against the bar -4.9; M5(b) 0.000). N between 150 and 200 was not measured; at N 150 both sides already fail, so an N there would need the W1 curve to rise again, which the grid does not show from 120 onward (it did rise from 90 to 120, so non-monotone steps exist).

(b) **Shape.** The T1 cost is flat at about -0.17 from N 60 to 150 and collapses between 150 and 200 (to -0.0125), zero from 300: the damaging rows are the `differs8` rows, whose first departure stays at median step about 355 up to N 150, i.e. rows with valued silences longer than 150 steps while the neutral plume is sensed. The W1 benefit is full up to N 120 and erodes from 150 (the first surge moves past the agent's first B whiffs, median 124 at N 60), reaching Agent10's level only at inf. The two requirements sit on the same quantity (steps since the last valued whiff): T1 needs the window longer than about 150-200 steps of valued silence, W1 needs it shorter than about 120-150; on these seeds the ranges do not overlap. The "seduced" count as defined is broad (about 0.97 of rows up to N 150, mostly harmless: 345 of 388 re-hold the valued odour); the harmful subset is the `differs8` out-of-V rows (70, 67, 65, 5, 0, 0).

(c) **What follows.** No Run 3 registration is sketched, since no N meets both targets. The recommendation from these measurements is **closure of H24 Run 2 at the bench stop** (the (h) stop rule stands; no verdict beyond it), then H17 in the registered order (decision:priority-h24run2-h17-stageb). What the counter idea would need to be re-attempted, stated as open questions, not designs: (1) a presence definition tied to the plume's own intermittency (a per-odour expected inter-whiff gap rather than one fixed N), since a fixed N must be both below about 120 (W1) and above about 150-200 (T1); (2) or a behaviour that shortens valued silences in T1 (the rows that lose V spend 150+ steps without a valued whiff), which is the H17 search question. N 200 is the only swept point where T1 and T3a both clear; it would fail M5(b) as registered, and any bar change there is outside this sweep.
