# H17 post-bench diagnosis: where the (d) silences and the (h2) wall contacts come from

Date 2026-09-24. Measurement only, at the owner's instruction (decision:h17-post-bench-diagnosis: '3번 진단 먼저 진행해', gloss 'run the diagnosis, option 3, first'; the options offered were closure as no candidate, a Run 2 design, or this diagnosis). The bench verdict (record:h17-bench-result: B FAIL, NO CANDIDATE on part (d), tasks not run) is not re-judged, and nothing is adopted. ph26.py (sha256 1c9b6f5b6e3f0341e60c707cd577d748292ecdb720062ecada33336101e167cf, doc d911535d7e535751c), design v2 FINAL (doc d83a917ea4152b4a7, hash f94d6ace...7516), the Search rule, S 210, gamma 15, L0 30, U1 360, every bar and every adopted module are unchanged. Code src/ph26b.py sha256 6b45d87c94693a976fdcd0028b74ed37bba9041ef6c43c442c1f03a0b6d3e0ae (its source stored in its own document). Output experiments/h17/ph26b_diag.txt sha256 10429f5b2c69f13d9355792a2700a1b1ea8d87da31b75d9c4516b6806aeddf19 (LF line ends), appended below in full; every number in this report is taken from it.

Only the bench seeds are used (20261051 / 20261052, bootstrap 20261053, taken from ph26 and not written out in ph26b.py or its output, so ph26's seed self-check stays valid: re-run after the output was written, no H17 seed in any other file, 167 files scanned). The development seeds 9943/9953 and the evaluation seeds 1945/2045 remain unused. No rule was changed, no agent variant added and no S swept.

## 0. What was asked

(A) Where the any-odour silences of at least 210 steps in Agent10's normal T1 tracking come from (World7 +1/0, the 18 rows in which Agent12 engages). (B) Where Agent12's wall contacts at (h2) come from (World7 +1/-1, 0.247 per row), by search leg.

## 1. Reproduction check

- ph26.py's sha256 equals the bench's; ph26_bench.txt's sha256 equals the recorded ec9df782...ff6d.
- ph26.bench re-run in the same process: its 56 output lines equal ph26_bench.txt's 56 lines, line for line.
- The four runs measured here (ph26.run, World7 +1/0 and +1/-1, Agent12 and Agent10, bench seeds, 400 x 600) reproduce, character for character, the bench's (d) lines (Agent10's longest silence 154/160/171, p90 193, max 321, 18 rows reaching q >= 210; Agent12 engaged rows 18/400 = 0.045 [0.029, 0.070], 502 engaged (row, step)), its (h1) lines (Agent12 V 384 N 14 tie 2, Agent10 V 385 N 13 tie 2, DP -0.0025 [-0.0075, +0.0000]) and its (h2) lines (Agent12 V 308 N 40 tie 52, lost 106, contacts 0.247; Agent10 V 293 N 31 tie 76, lost 140, contacts 0.000; stranded rows 139 / 143; lost-row DP -0.0850 [-0.1150, -0.0575]; P(V) DP +0.0375 [+0.0150, +0.0600]).
- Row identity (bench (a2)) holds in both value pairs. Everything below was measured on reproducing runs.

## 2. Results (A): the (d) silences, World7 +1/0

**(A1) Longest any-odour silence per row (descriptive; no S is chosen from it).**

| | quartiles | p90 | p95 | p99 | max |
|---|---|---|---|---|---|
| Agent10 | 154/160/171 | 193 | 207 | 264 | 321 |
| Agent12 | 154/160/171 | 193 | 207 | 260 | 290 |

Rows with a longest silence of at least c (Agent10): 150: 392; 180: 56; 193: 41; 200: 28; **210: 18 (0.045)**; 220: 11; 230: 9; 240: 8; 250: 6; 260: 5; 280: 3; 300: 3; 350: 0. Histogram: 187 rows in [150, 160), 88 in [160, 170), 61 in [170, 180), then 15, 13, 10 per 10 steps to 210, 12 in [210, 250), 3 in [250, 300), 3 in [300, 350). Fraction of (row, step) with q >= 150/180/210/250/300/350: 0.03785/0.00732/0.00278/0.00107/0.00025/0. The two arms are equal in the 382 never-engaged rows. Reference arithmetic printed with the table: the Wilson upper bound of k rows of 400 is 0.0486 at k 11 and 0.0517 at k 12 (the (d) bar is an upper bound of at most 0.05).

**(A2) The 18 silences.** The rows whose Agent10 silence reaches q >= 210 are exactly Agent12's 18 engaged rows. Per row (positions are the position the step sensed at; d_along downwind positive; class as in (A4)):

| row | cell | silence steps (length) | last whiff | hold before | at start: class, d_along, `since` | at engagement: class, d_along | dwell before (valued/other) | Agent10 / Agent12 | Agent12 first whiff after engagement |
|---|---|---|---|---|---|---|---|---|---|
| 14 | 0 | 275-538 (264) | valued | none held; last valued hold ended by the H25 drive | (v), -1.3, 1 | (v), +19.0 | 13/7 | V / V | u 10, other |
| 31 | 1 | 282-599 (318, open) | valued | none held; valued hold ended by the drive | (v), -0.8, 1 | (v), +19.2 | 9/11 | N / N | u 51, other |
| 44 | 1 | 269-478 (210) | valued | valued held, ended by the drive 48 steps later | (v), -2.3, 1 | (v), +15.7 | 12/6 | V / V | u 1, other |
| 77 | 1 | 259-503 (245) | other | none held; other hold ended by the drive | (v), +21.3, 250 | (v), +15.1 | 9/10 | V / V | u 6, valued |
| 85 | 0 | 276-495 (220) | valued | none held; valued hold ended by the drive | (v), -1.8, 1 | (v), +18.7 | 4/12 | V / V | u 8, other |
| 106 | 1 | 278-496 (219) | valued | valued held, ended by the drive | (i), -3.0, 1 | (v), +14.5 | 16/5 | V / V | u 8, other |
| 135 | 2 | 40-269 (230) | valued | valued held, ended by the drive | (i), -3.0, 1 | (iii), +16.0 | 9/0 | V / V | u 70, valued |
| 184 | 1 | 119-334 (216) | valued | none held at the whiff (valued held at the start) | (i), -3.3, 1 | (v), +15.7 | 2/5 | **V / N** | u 16, other |
| 223 | 0 | 279-599 (321, open) | valued | none held; valued hold ended by the drive | (v), +4.1, 1 | (v), +24.6 | 15/5 | V / V | u 54, other |
| 233 | 3 | 284-501 (218) | valued | none held; valued hold ended by the drive | (v), +0.3, 1 | (v), +20.1 | 12/8 | V / V | u 2, other |
| 236 | 0 | 117-332 (216) | valued | valued held, ended by the drive | (v), -2.3, 1 | (v), +14.7 | 6/0 | V / V | u 21, other |
| 250 | 0 | 276-544 (269) | valued | valued held, ended by the drive | (v), -2.2, 1 | (v), +17.7 | 16/9 | V / V | u 4, other |
| 251 | 2 | 37-284 (248) | other | other held, ended by the drive | (v), +1.3, 38 | (ii), +29.3 | 0/5 | N / N | u 46, other |
| 289 | 1 | 21-243 (223) | valued | valued held, ended by the drive | (iii), +7.6, 1 | (ii), +25.7 | 0/0 | V / V | u 81, other |
| 334 | 1 | 277-491 (215) | valued | none held; valued hold ended by the drive | (iii), +2.2, 1 | (v), +22.6 | 22/8 | V / V | u 6, valued |
| 362 | 3 | 16-274 (259) | valued | valued held, ended by the drive | (v), +11.0, 1 | (ii), +28.9 | 0/0 | N / N | u 67, other |
| 385 | 2 | 125-343 (219) | valued | valued held, ended by the drive | (v), +0.3, 1 | (v), +19.2 | 12/9 | V / V | u 10, other |
| 399 | 0 | 281-599 (319, open) | valued | none held; valued hold ended by the drive | (v), +0.4, 1 | (v), +19.1 | 18/10 | V / V | u 12, other |

Summary: silence start step 118/272/278 (min 16, max 284); q reaches 210 at 326/481/487; length 218/226/263 (15 end with a whiff, 3 open at the run end). Last whiff before the silence valued 16, other 2. At the last whiff a hold was held in 9 rows (each ended by the H25 timeout drive), nothing in 9 (each row's previous hold had ended by the drive). **At the silence start:** d_along -2.3/-0.2/2.0 (min -3.3, max 21.3), |d_cross| to the nearer axis 1.0/1.9/2.4, inside a whiff region 13/18, distance to the nearest region at most 0.5, nearest wall 67.2/69.6/71.3; the cast's `since` equals 1 in 16/18 (the last whiff was a navigation event). **At the engagement step:** d_along 15.8/19.0/22.0 (min 14.5, max 29.3), none upwind of the sources, 3 beyond LMAX 25, d_cross to the valued axis -3.2/-2.7/-1.5, inside a whiff region 14/18, distance to the nearest region at most 4.3; `since` 210 at the quartiles. No silence has a wall contact; nearest approach to a wall 38.6/41.2/43.9.

**(A3) Agent12 in the same rows.** Engagement at exactly the step Agent10's q reaches 210 in 18/18. A whiff follows engagement in 18/18 (first odour valued 3, other 15), at u 6/11/50; none stays engaged to the run end. Outcomes Agent10 -> Agent12: V->V 14, V->N 1, N->N 3. **The one differing row is row 184** (cell 1, odour A valued, -y): Agent10 V (dwell valued/other 16/5), Agent12 N (dwell 2/22); engaged at step 328, first whiff after it at 344, of the other odour. It is the only row of 400 whose outcome differs.

**(A4) Position-based classification** (design section 2 categories; per silence step, in this order: (iv) within 1.0 of a wall; (v) inside a whiff region, no whiff drawn; (i) upwind of both sources, d_along < 0; (ii) d_along >= 25; (iii) 0 <= d_along < 25 outside both cones; (vi) = no class holds at least half of a silence's steps):

| | (i) upwind | (ii) beyond LMAX | (iii) crosswind outside | (iv) wall | (v) inside, no whiff | (vi) mixed |
|---|---|---|---|---|---|---|
| majority over the silence | 16 | 0 | 0 | 0 | 0 | 2 |
| at the silence start | 3 | 0 | 2 | 0 | 13 | 0 |
| at the engagement step | 0 | 3 | 1 | 0 | 14 | 0 |

Pooled silence steps 4429: (i) 0.608, (ii) 0.036, (iii) 0.199, (iv) 0, (v) 0.157. The longest run of consecutive in-region steps without a whiff per silence is 22/28/34 (max 52). Reference arithmetic (not measured), a stay inside the cone at fixed d_along: expected longest dry spell in 600 steps 15.7 at d_along 0, 34.9 at 10, 49.8 at 15, 69.9 at 20, 90.5 at 24; P(a dry spell of at least 210 within 600 steps) 2.2e-07 at 15, 1.1e-04 at 20, 2.8e-03 at 24.

**(A5) Timing against the dwell.** 16/18 silences start after the agent had been at a source (valued dwell before > 0 in 15, other in 14), 1/1/2 steps after its last step at a source (max 120); 2 never reached one before. Outcomes: reached before, Agent10 V/N/tie 14/2/0, Agent12 13/3/0; never reached, 1/1/0 in both. For comparison, the 374 never-engaged rows whose longest silence is 150-209 start that silence inside a whiff region in 208, upwind in 144, and had reached a source before it in 371.

## 3. Results (B): the (h2) wall contacts, World7 +1/-1

**(B1)** Agent12 99 contacts = 0.247 per row in 39 rows (2 per contacting row at the quartiles; max 18, row 139); Agent10 0.

**(B2) Every contact** (listed in the appendix) is on an engaged step:

| by leg | leg 1-2 | leg 3 | leg 4 | legs 5-6 (u >= 300) |
|---|---|---|---|---|
| contacts (rows) | 0 | 44 (39) | 55 (37) | 0 |

u at the contact 172/185/194 (min 150, max 254); slant upwind (+1) 99, downwind 0. By wall: side wall on the negative source's side 68 (in 34 rows), side wall on the valued source's side 3 (2 rows), upwind wall 27 (4 rows), one corner (upwind and valued side); row 139 alone has 18 contacts, on the upwind and valued-side walls. d_along at the contact -68.3/14.7/21.0; |d_cross| to the valued axis 70.1/79.3/81.5. **All 99 contacts are in Agent10-stranded rows**, after the row's drive-ended negative hold. **No whiff of either odour follows any contact** (0/99). The 39 contacting rows end V 2, N 12, tie 25, **lost 39/39**. At the first engaged step these rows were at d_along 43.4/48.8/53.5, |d_cross| to the nearer axis 39.4/40.7/41.9 and 28.6/30.5/32.5 (min 26.4) from the nearer side wall; the 117 engaged rows without a contact were 12.2/21.8/34.7 from the nearer axis and 42.3/55.0/61.2 (min 32.6) from the nearer side wall. First contact at step 404/411/418, first engagement 232/238/246; no contact precedes engagement.

**(B3) The (h2) effect decomposed.**
- Agent10 stranded rows 139; Agent12 143 (the 139 plus 4). Of the 139, 131 engage in Agent12, 130 after the same first release as Agent10 (engagement 160/162/162 steps after it); 8 do not engage.
- Of the 131 engaged stranded rows: a whiff after engagement 37 (first odour valued 12, negative 25), none 94. First valued (12): V/N/tie 9/3/0, lost 0. First negative (25): 4/16/5, lost 6; a negative hold re-formed in 15, stranded again in 14. No whiff (94): 30/18/46, lost 94; these include all 39 contacting rows.
- Agent10's stranded rows: Agent10 V 38 N 30 tie 71, lost 133; Agent12 V 51 N 37 tie 51, lost 102.
- Paired transitions (400 rows): into V 19, out of V 4 (net +15 = DP +0.0375); into lost 3, out of lost 37 (net -34 = DP -0.0850). In the 139 stranded rows: into V 13, out of V 0, out of lost 31, into lost 0. In the other 261: into V 6, out of V 4, out of lost 6, into lost 3. **In the 39 contact rows: no transition in either direction.** All 19 into-V, 4 out-of-V, 37 out-of-lost and 3 into-lost transitions are in the 117 engaged rows without a contact; never-engaged rows have none.

**(B4) P(V | contact), Agent12 (Wilson 95 percent):** 2/39 = 0.051 [0.014, 0.169] against 306/361 = 0.848 [0.807, 0.881] without a contact; P(lost | contact) 39/39 = 1.000 [0.910, 1.000] against 67/361 = 0.186 [0.149, 0.229]. Paired on the same rows: in Agent12's contact rows Agent10 also has V 2/39 and lost 39/39; in the no-contact rows V 306 vs 291, lost 67 vs 101. Among the 156 engaged rows: P(V | contact) 0.051 vs 62/117 = 0.530 [0.440, 0.618]. Among Agent10's stranded rows: 0.051 vs 49/100 = 0.490 [0.394, 0.587].

## 4. Reading (interpretation, not measured)

- (A) The 18 long silences are not silences far from the plumes. By position they are the return cast's own loop after a whiff at or next to a source: 16 of 18 begin after the agent had been at a source (most within 1-2 steps of it), 16 with the cast just reset (`since` 1), spend most of their steps upwind of both sources (majority class (i) in 16), and reach q 210 back inside a whiff region in 14 (the valued cone in 13) at d_along 14.5-24.6, where a whiff is rare per step. The engaged rows are tracking rows (15 of 18 V), not lost rows. The design's (d) prediction (0.0025-0.02) was anchored on Agent10's lost-row count; section 10 listed 'longer any-odour silences in T1 than Agent10's lost-row count implies' as what would make it wrong, and this is the pattern measured. S 210 sits at about p95 of the longest-silence distribution (207). Which of these features, if any, would be causal is not established here.
- (A3) In these rows the search almost always ends within one or two legs on a whiff, mostly of the other odour (15 of 18), and changes the outcome in one row (184).
- (B) The contacts are not the legs 5-6 contacts the design predicted: they occur in legs 3 and 4 on the upwind slant, only in rows stranded by a negative release that were already 28.6/30.5/32.5 (min 26.4) from the nearer side wall at engagement, and no whiff follows any of them. Those rows are lost in both arms and contribute no transition; the measured (h2) gains sit in engaged rows without a contact. So in this measurement the (h2) effect does not rest on the wall reflex, but the contacts would count against T3 (c)'s 0.10 per row bar (0.247 here). The negative plume re-captures some searched rows (15 re-formed negative holds, 14 stranded again), as design section 13 anticipated.

## 5. What the owner can decide

Listed neutrally; nothing is adopted and the H17 verdict (stopped at the bench, no candidate) stands either way.
- **Close H17 as no candidate** (the registered verdict), with this diagnosis and the (c1) result on record, and keep cold search as a recorded limit.
- **A Run 2 design.** It would be a new design with its own registration, predictions and a bench on new seeds before any task seed (numbers measured on these bench seeds cannot serve as a Run 2 bench). It would have to register, for example: (i) the engagement rule, either a different S chosen with its reason stated in advance, or a condition that separates the measured tracking-loop silences (at or next to a source, then upwind, then back through the cone) from stranded states, and in either case what it does to (c1); (ii) the (d) bar, either kept or re-signed with a rationale anchored to the measured silence distribution rather than to the lost-row count (for reference, at n 400 the Wilson upper bound stays at or below 0.05 up to 11 rows); (iii) the T3 contact bar risk: the measured contacts are in legs 3-4 of stranded rows that were 28.6/30.5/32.5 (min 26.4) from the nearer side wall at engagement, so either the bar with its reason or a mechanism constraint on the crosswind excursion near walls would have to be registered before its bench; (iv) the T3 (a) margin (the bench's lost-row DP -0.0850 [-0.1150, -0.0575] against the registered upper bound -0.05; its pass probability is in the bench record) and the negative-plume re-capture (14 of 131 engaged stranded rows stranded again).

## 6. What this does not establish

No change was tested and no alternative S, gamma, leg schedule or bar was run. The classification is by position only; it names no cause. The dry-spell and Wilson figures are reference arithmetic, not measurements. The task was not run; no development or evaluation seed was used.

## 7. Provenance

decision:h17-post-bench-diagnosis (owner, 2026-09-24). ph26b.py sha 6b45d87c...e0ae (imports ph26 unchanged; ph26.py sha 1c9b6f5b...67cf checked at run time); design v2 FINAL doc d83a917ea4152b4a7 hash f94d6ace...7516; bench output ph26_bench.txt sha ec9df782...ff6d reproduced line for line; bench seeds only; output ph26b_diag.txt sha 10429f5b...df19. Bench result: record:h17-bench-result. Result: record:h17-post-bench-diagnosis-result.

## Appendix: ph26b_diag.txt in full

```
== H17 post-bench diagnosis (measurement only; owner 2026-09-24, '3번 진단 먼저 진행해'). ph26b.py sha256 6b45d87c94693a976fdcd0028b74ed37bba9041ef6c43c442c1f03a0b6d3e0ae; ph26.py sha256 1c9b6f5b6e3f0341e60c707cd577d748292ecdb720062ecada33336101e167cf; design v2 FINAL doc d83a917ea4152b4a7 hash f94d6ace552816313e366c810267353e585d516c33621913aec0f3a1c9c87516; reproduces experiments/h17/ph26_bench.txt sha256 ec9df782aa429492462849c9577e853bade96eefd18917626ee9a08e9643ff6d (record:h17-bench-result) ==
   imported modules (unchanged): ph9.py 7699b4e6fb47a1bee5f7e4e991a88aac8fa5af3a940297fbd4e441441f4d9706; ph11.py e80f40bd710aca43252f04329846ffa29943251d19e718450e9a7ff49e947a23; ph12b.py ec6b1896f60ef2e250d092e0f9f9f4105c06b38f6998de90700ca371213e0faa; ph13.py 2d75fae8e8c31e1c6ddf6577782fafde3099f10fe8f50fe382f53d09e9ef1f2d; ph15.py cc9399965e5cbc30cb7f35e8ce296d8d43e4657cf644d1ec350931e594403fdc; ph16.py 33d5fdb25959fb7f9cbe465ca25a8973776b39f1e5170d645cb53bc8d906a2c2; ph18.py 26ad4defb7590e16e1030b0b6f8073d3258584baeec06ba66e233315da7c97c3; ph19.py 00c6a3b32f80fae9f58b6dbd23a8e03b1710be45fcf335238f289567fce34791; ph21.py 3a1d79d9a0d235f1bef7e435ec594cff4048180e27b28dcd892598c58413cfc1; ph22.py 03ab8c4706b19557af5d64edd83f812abba91b618439618b35837a49dd44ca1c; ph24.py f344f178e20380858f4d7400ef670223f90aa2927b3f7304772ae1d848bd1bef; ph24b.py bbabad15ecb17078c09a7886d8375b38c9cd71de8e4cd2352062b3134040eefc; ph24c.py 17adab85f64f75e64eb7a9febbefb417829a16ece4c391dc15e7721a21a76a45
   bench seeds only (ph26.BS, bootstrap seed as ph26 sets it; not written out here); dev and eval seeds untouched. Nothing is changed or adopted; the H17 verdict (stopped at the bench, no candidate on part (d)) is not re-judged; S, gamma, L0, U1 and every bar as registered; no sweep
   S 210; walls 160 apart (World7); 'at a wall' = within 1.0 of a wall; LMAX 25; whiff probability 0.3 exp(-d_along / 12) inside a region

== (0) reproduction (nothing is measured unless every check holds) ==
   ph26.py sha256 equals the bench's (1c9b6f5b...67cf): True; ph26_bench.txt sha256 equals the recorded (ec9df782...ff6d): True
   ph26.bench re-run in this process (56 lines) equals ph26_bench.txt (56 lines) line for line: True
   the four runs measured below (ph26.run, World7 +1/0 and +1/-1, Agent12 and Agent10, bench seeds, 400 x 600): the bench's (d) gap lines (+1/0, +1/-1), (d) engaged-row lines (+1/0, +1/-1), (h1) two lines and (h2) three lines recomputed from them are each present verbatim in ph26_bench.txt: [True, True, True, True, True, True, True, True, True] -> True
      [World7 +1/0 Agent10] longest any-odour silence per row: quartiles 154/160/171, p90 193, max 321; rows reaching q >= 210 18; fraction of (row, step) with q >= 150/180/210/250: 0.03785/0.00732/0.00278/0.00107
      [World7 +1/-1 Agent10] longest any-odour silence per row: quartiles 157/174/543, p90 573, max 595; rows reaching q >= 210 156; fraction of (row, step) with q >= 150/180/210/250: 0.23980/0.19892/0.17699/0.15366
      [World7 +1/0 Agent12] rows with any engaged step 18/400 = 0.045 [0.029, 0.070]; engaged (row, step) 502; first engaged step 326/481/487 -> bar upper bound <= 0.05: FAIL (pass probability at the point, section 7: 0.0698)
      [World7 +1/-1 Agent12] rows with any engaged step 156/400 = 0.390 [0.343, 0.439]; engaged (row, step) 33993; first engaged step 234/245/330 (reported)
      (h1) T1 on bench seeds, World7 +1/0 400 x 600: Agent12 V 384 N 14 tie 2 P(V) 0.960 [0.936, 0.975]; Agent10 V 385 N 13 tie 2 P(V) 0.963 [0.939, 0.977]
      (h1) paired DP P(V) Agent12 - Agent10 -0.0025 [-0.0075, +0.0000] (bootstrap 5000, seed <ph26's bootstrap seed>); engaged rows 18; into V 0, out of V 1; V among engaged rows Agent12 14 vs Agent10 15; lost rows 1 vs 3; contacts per row 0.000 vs 0.000
      (h2) T3 on bench seeds, World7 +1/-1 400 x 600: Agent12 V 308 N 40 tie 52, lost rows 106, contacts per row 0.247; Agent10 V 293 N 31 tie 76, lost rows 140, contacts per row 0.000
      (h2) stranded rows (a drive-ended negative hold, as R3): Agent10 139 (releases 139), Agent12 143; Agent12 engaged rows 156, engaged (row, step) 33993; lost among Agent10's stranded rows: Agent10 133, Agent12 102
      (h2) lost-row paired DP Agent12 - Agent10 -0.0850 [-0.1150, -0.0575]; P(V) paired DP +0.0375 [+0.0150, +0.0600]; contacts per row 0.247
   never-engaged rows bitwise Agent10 and engaged rows equal before their first engaged step, both value pairs (bench (a2)): True

== (A) the bench (d) silences: World7 +1/0, 400 x 600, Agent10 (Agent12 alongside); q = steps since the last whiff of either odour (ph26.qrec) ==

(A1) longest any-odour silence per row (descriptive; no S is chosen from it)
   [Agent10] quartiles 154/160/171, p90 193, p95 207, p99 264, max 321; mean 166.8
   [Agent10] rows with a silence >= c:  120: 397 (0.9925); 150: 392 (0.9800); 180: 56 (0.1400); 193: 41 (0.1025); 200: 28 (0.0700); 210: 18 (0.0450); 220: 11 (0.0275); 230: 9 (0.0225); 240: 8 (0.0200); 250: 6 (0.0150); 260: 5 (0.0125); 280: 3 (0.0075); 300: 3 (0.0075); 350: 0 (0.0000); 400: 0 (0.0000); 500: 0 (0.0000)
   [Agent10] fraction of (row, step) with q >= c:  150: 0.03785; 180: 0.00732; 210: 0.00278; 250: 0.00107; 300: 0.00025; 350: 0.00000
   [Agent12] quartiles 154/160/171, p90 193, p95 207, p99 260, max 290; mean 166.3
   [Agent12] rows with a silence >= c:  120: 397 (0.9925); 150: 392 (0.9800); 180: 56 (0.1400); 193: 41 (0.1025); 200: 28 (0.0700); 210: 18 (0.0450); 220: 9 (0.0225); 230: 7 (0.0175); 240: 6 (0.0150); 250: 6 (0.0150); 260: 5 (0.0125); 280: 1 (0.0025); 300: 0 (0.0000); 350: 0 (0.0000); 400: 0 (0.0000); 500: 0 (0.0000)
   [Agent12] fraction of (row, step) with q >= c:  150: 0.03748; 180: 0.00689; 210: 0.00209; 250: 0.00054; 300: 0.00000; 350: 0.00000
   reference arithmetic (not measured): the Wilson 95 percent upper bound of k rows of 400 (the (d) bar is an upper bound <= 0.05): 6: 0.0323; 7: 0.0357; 8: 0.0390; 9: 0.0422; 10: 0.0454; 11: 0.0486; 12: 0.0517; 13: 0.0548; 14: 0.0579; 15: 0.0609; 16: 0.0640; 17: 0.0670; 18: 0.0700; 19: 0.0730; 20: 0.0760
   the two arms' longest silences are equal in the 382 never-engaged rows: True; differing rows 15 (all engaged rows)
   [Agent10] histogram of the longest silence per row: [0, 100) 0; [100, 120) 3; [120, 140) 2; [140, 150) 3; [150, 160) 187; [160, 170) 88; [170, 180) 61; [180, 190) 15; [190, 200) 13; [200, 210) 10; [210, 250) 12; [250, 300) 3; [300, 350) 3; [350, 601) 0

(A2) the rows whose Agent10 silence reaches q >= 210: 18 rows [14, 31, 44, 77, 85, 106, 135, 184, 223, 233, 236, 250, 251, 289, 334, 362, 385, 399]; Agent12's engaged rows [14, 31, 44, 77, 85, 106, 135, 184, 223, 233, 236, 250, 251, 289, 334, 362, 385, 399]; the same set: True
   row 14: cell 0 (odour A valued, +y); silence steps 275-538 (start = the step after the last whiff at 274; ends with a whiff at 539); length 264; the row's longest 264; q reaches 210 at step 484
      last whiff (step 274): valued; nothing held at the last whiff; the last hold before it: valued, steps 115-166, ended by H25 timeout drive; held at the silence start: nothing; held at step 484: nothing
      at the silence start: d_along -1.3; d_cross valued axis +2.6, other axis -12.6 (outward +); inside valued/other region 1/0; distance to the nearest region 0.0; nearest wall 69.3; class (v); cast `since` 1
      at step 484 (Agent12's engagement step): d_along +19.0; d_cross valued axis -3.3, other axis -6.7 (outward +); inside valued/other region 1/0; distance to the nearest region 0.0; nearest wall 70.4; class (v); cast `since` 210
      over the silence (Agent10): steps by class (i) 150, (ii) 0, (iii) 77, (iv) 0, (v) 37 -> majority (i); longest run inside a whiff region 35; nearest approach to a wall 39.7, contacts 0
      dwell before the silence valued/other 13/7 (last step at a source 274); after it 4/0; outcome Agent10 V, Agent12 V; Agent12 engaged at step 484, first whiff after it step 494 (other), u 10, leg 1
   row 31: cell 1 (odour A valued, -y); silence steps 282-599 (start = the step after the last whiff at 281; ends at the run end, 600); length 318; the row's longest 318; q reaches 210 at step 491
      last whiff (step 281): valued; nothing held at the last whiff; the last hold before it: valued, steps 126-173, ended by H25 timeout drive; held at the silence start: nothing; held at step 491: nothing
      at the silence start: d_along -0.8; d_cross valued axis +2.0, other axis -12.0 (outward +); inside valued/other region 1/0; distance to the nearest region 0.0; nearest wall 66.1; class (v); cast `since` 1
      at step 491 (Agent12's engagement step): d_along +19.2; d_cross valued axis -1.8, other axis -8.2 (outward +); inside valued/other region 1/0; distance to the nearest region 0.0; nearest wall 69.9; class (v); cast `since` 210
      over the silence (Agent10): steps by class (i) 201, (ii) 0, (iii) 86, (iv) 0, (v) 31 -> majority (i); longest run inside a whiff region 29; nearest approach to a wall 39.7, contacts 0
      dwell before the silence valued/other 9/11 (last step at a source 281); after it 1/0; outcome Agent10 N, Agent12 N; Agent12 engaged at step 491, first whiff after it step 542 (other), u 51, leg 2
   row 44: cell 1 (odour A valued, -y); silence steps 269-478 (start = the step after the last whiff at 268; ends with a whiff at 479); length 210; the row's longest 210; q reaches 210 at step 478
      last whiff (step 268): valued; held valued at the last whiff (formed 266), ended at step 316 by H25 timeout drive (48 steps after the last whiff); held at the silence start: valued; held at step 478: nothing
      at the silence start: d_along -2.3; d_cross valued axis +0.7, other axis -10.7 (outward +); inside valued/other region 1/0; distance to the nearest region 0.0; nearest wall 66.0; class (v); cast `since` 1
      at step 478 (Agent12's engagement step): d_along +15.7; d_cross valued axis -6.3, other axis -3.7 (outward +); inside valued/other region 0/1; distance to the nearest region 0.0; nearest wall 76.0; class (v); cast `since` 210
      over the silence (Agent10): steps by class (i) 149, (ii) 0, (iii) 29, (iv) 0, (v) 32 -> majority (i); longest run inside a whiff region 20; nearest approach to a wall 35.8, contacts 0
      dwell before the silence valued/other 12/6 (last step at a source 268); after it 17/0; outcome Agent10 V, Agent12 V; Agent12 engaged at step 478, first whiff after it step 479 (other), u 1, leg 1
   row 77: cell 1 (odour A valued, -y); silence steps 259-503 (start = the step after the last whiff at 258; ends with a whiff at 504); length 245; the row's longest 245; q reaches 210 at step 468
      last whiff (step 258): other; nothing held at the last whiff; the last hold before it: other, steps 139-210, ended by H25 timeout drive; held at the silence start: nothing; held at step 468: nothing
      at the silence start: d_along +21.3; d_cross valued axis -11.0, other axis +1.0 (outward +); inside valued/other region 0/1; distance to the nearest region 0.0; nearest wall 67.2; class (v); cast `since` 250
      at step 468 (Agent12's engagement step): d_along +15.1; d_cross valued axis -3.4, other axis -6.6 (outward +); inside valued/other region 1/0; distance to the nearest region 0.0; nearest wall 73.5; class (v); cast `since` 459
      over the silence (Agent10): steps by class (i) 141, (ii) 0, (iii) 33, (iv) 0, (v) 71 -> majority (i); longest run inside a whiff region 52; nearest approach to a wall 44.1, contacts 0
      dwell before the silence valued/other 9/10 (last step at a source 139); after it 5/0; outcome Agent10 V, Agent12 V; Agent12 engaged at step 468, first whiff after it step 474 (valued), u 6, leg 1
   row 85: cell 0 (odour A valued, +y); silence steps 276-495 (start = the step after the last whiff at 275; ends with a whiff at 496); length 220; the row's longest 220; q reaches 210 at step 485
      last whiff (step 275): valued; nothing held at the last whiff; the last hold before it: valued, steps 126-173, ended by H25 timeout drive; held at the silence start: nothing; held at step 485: nothing
      at the silence start: d_along -1.8; d_cross valued axis +2.1, other axis -12.1 (outward +); inside valued/other region 1/0; distance to the nearest region 0.0; nearest wall 70.3; class (v); cast `since` 1
      at step 485 (Agent12's engagement step): d_along +18.7; d_cross valued axis -2.8, other axis -7.2 (outward +); inside valued/other region 1/0; distance to the nearest region 0.0; nearest wall 69.3; class (v); cast `since` 210
      over the silence (Agent10): steps by class (i) 150, (ii) 0, (iii) 44, (iv) 0, (v) 26 -> majority (i); longest run inside a whiff region 25; nearest approach to a wall 42.4, contacts 0
      dwell before the silence valued/other 4/12 (last step at a source 275); after it 9/0; outcome Agent10 V, Agent12 V; Agent12 engaged at step 485, first whiff after it step 493 (other), u 8, leg 1
   row 106: cell 1 (odour A valued, -y); silence steps 278-496 (start = the step after the last whiff at 277; ends with a whiff at 497); length 219; the row's longest 219; q reaches 210 at step 487
      last whiff (step 277): valued; held valued at the last whiff (formed 276), ended at step 325 by H25 timeout drive (48 steps after the last whiff); held at the silence start: valued; held at step 487: nothing
      at the silence start: d_along -3.0; d_cross valued axis +1.7, other axis -11.7 (outward +); inside valued/other region 0/0; distance to the nearest region 0.4; nearest wall 66.9; class (i); cast `since` 1
      at step 487 (Agent12's engagement step): d_along +14.5; d_cross valued axis -2.8, other axis -7.2 (outward +); inside valued/other region 1/0; distance to the nearest region 0.0; nearest wall 71.4; class (v); cast `since` 210
      over the silence (Agent10): steps by class (i) 157, (ii) 0, (iii) 39, (iv) 0, (v) 23 -> majority (i); longest run inside a whiff region 23; nearest approach to a wall 38.3, contacts 0
      dwell before the silence valued/other 16/5 (last step at a source 276); after it 10/0; outcome Agent10 V, Agent12 V; Agent12 engaged at step 487, first whiff after it step 495 (other), u 8, leg 1
   row 135: cell 2 (odour B valued, +y); silence steps 40-269 (start = the step after the last whiff at 39; ends with a whiff at 270); length 230; the row's longest 230; q reaches 210 at step 249
      last whiff (step 39): valued; held valued at the last whiff (formed 6), ended at step 87 by H25 timeout drive (48 steps after the last whiff); held at the silence start: valued; held at step 249: nothing
      at the silence start: d_along -3.0; d_cross valued axis -0.6, other axis -9.4 (outward +); inside valued/other region 0/0; distance to the nearest region 0.0; nearest wall 66.6; class (i); cast `since` 1
      at step 249 (Agent12's engagement step): d_along +16.0; d_cross valued axis +5.7, other axis -15.7 (outward +); inside valued/other region 0/0; distance to the nearest region 0.2; nearest wall 74.3; class (iii); cast `since` 210
      over the silence (Agent10): steps by class (i) 152, (ii) 0, (iii) 16, (iv) 0, (v) 62 -> majority (i); longest run inside a whiff region 37; nearest approach to a wall 36.1, contacts 0
      dwell before the silence valued/other 9/0 (last step at a source 38); after it 24/0; outcome Agent10 V, Agent12 V; Agent12 engaged at step 249, first whiff after it step 319 (valued), u 70, leg 2
   row 184: cell 1 (odour A valued, -y); silence steps 119-334 (start = the step after the last whiff at 118; ends with a whiff at 335); length 216; the row's longest 216; q reaches 210 at step 328
      last whiff (step 118): valued; nothing held at the last whiff; the last hold before it: valued, steps 5-52, ended by H25 timeout drive; held at the silence start: valued; held at step 328: nothing
      at the silence start: d_along -3.3; d_cross valued axis +0.8, other axis -10.8 (outward +); inside valued/other region 0/0; distance to the nearest region 0.4; nearest wall 67.3; class (i); cast `since` 1
      at step 328 (Agent12's engagement step): d_along +15.7; d_cross valued axis -3.2, other axis -6.8 (outward +); inside valued/other region 1/0; distance to the nearest region 0.0; nearest wall 71.3; class (v); cast `since` 210
      over the silence (Agent10): steps by class (i) 158, (ii) 0, (iii) 37, (iv) 0, (v) 21 -> majority (i); longest run inside a whiff region 21; nearest approach to a wall 37.8, contacts 0
      dwell before the silence valued/other 2/5 (last step at a source 117); after it 14/0; outcome Agent10 V, Agent12 N DIFFERS; Agent12 engaged at step 328, first whiff after it step 344 (other), u 16, leg 1
   row 223: cell 0 (odour A valued, +y); silence steps 279-599 (start = the step after the last whiff at 278; ends at the run end, 600); length 321; the row's longest 321; q reaches 210 at step 488
      last whiff (step 278): valued; nothing held at the last whiff; the last hold before it: valued, steps 112-160, ended by H25 timeout drive; held at the silence start: nothing; held at step 488: nothing
      at the silence start: d_along +4.1; d_cross valued axis +1.9, other axis -11.9 (outward +); inside valued/other region 1/0; distance to the nearest region 0.0; nearest wall 72.5; class (v); cast `since` 1
      at step 488 (Agent12's engagement step): d_along +24.6; d_cross valued axis -1.9, other axis -8.1 (outward +); inside valued/other region 1/0; distance to the nearest region 0.0; nearest wall 67.0; class (v); cast `since` 210
      over the silence (Agent10): steps by class (i) 182, (ii) 0, (iii) 101, (iv) 0, (v) 38 -> majority (i); longest run inside a whiff region 34; nearest approach to a wall 41.8, contacts 0
      dwell before the silence valued/other 15/5 (last step at a source 275); after it 2/0; outcome Agent10 V, Agent12 V; Agent12 engaged at step 488, first whiff after it step 542 (other), u 54, leg 2
   row 233: cell 3 (odour B valued, -y); silence steps 284-501 (start = the step after the last whiff at 283; ends with a whiff at 502); length 218; the row's longest 218; q reaches 210 at step 493
      last whiff (step 283): valued; nothing held at the last whiff; the last hold before it: valued, steps 122-170, ended by H25 timeout drive; held at the silence start: nothing; held at step 493: nothing
      at the silence start: d_along +0.3; d_cross valued axis +2.1, other axis -12.1 (outward +); inside valued/other region 1/0; distance to the nearest region 0.0; nearest wall 68.0; class (v); cast `since` 1
      at step 493 (Agent12's engagement step): d_along +20.1; d_cross valued axis -2.8, other axis -7.2 (outward +); inside valued/other region 1/0; distance to the nearest region 0.0; nearest wall 68.1; class (v); cast `since` 210
      over the silence (Agent10): steps by class (i) 142, (ii) 0, (iii) 43, (iv) 0, (v) 33 -> majority (i); longest run inside a whiff region 24; nearest approach to a wall 43.4, contacts 0
      dwell before the silence valued/other 12/8 (last step at a source 283); after it 15/0; outcome Agent10 V, Agent12 V; Agent12 engaged at step 493, first whiff after it step 495 (other), u 2, leg 1
   row 236: cell 0 (odour A valued, +y); silence steps 117-332 (start = the step after the last whiff at 116; ends with a whiff at 333); length 216; the row's longest 216; q reaches 210 at step 326
      last whiff (step 116): valued; held valued at the last whiff (formed 116), ended at step 164 by H25 timeout drive (48 steps after the last whiff); held at the silence start: valued; held at step 326: nothing
      at the silence start: d_along -2.3; d_cross valued axis +0.7, other axis -10.7 (outward +); inside valued/other region 1/0; distance to the nearest region 0.0; nearest wall 71.0; class (v); cast `since` 1
      at step 326 (Agent12's engagement step): d_along +14.7; d_cross valued axis -1.0, other axis -9.0 (outward +); inside valued/other region 1/0; distance to the nearest region 0.0; nearest wall 72.0; class (v); cast `since` 210
      over the silence (Agent10): steps by class (i) 156, (ii) 0, (iii) 41, (iv) 0, (v) 19 -> majority (i); longest run inside a whiff region 17; nearest approach to a wall 40.9, contacts 0
      dwell before the silence valued/other 6/0 (last step at a source 116); after it 16/0; outcome Agent10 V, Agent12 V; Agent12 engaged at step 326, first whiff after it step 347 (other), u 21, leg 1
   row 250: cell 0 (odour A valued, +y); silence steps 276-544 (start = the step after the last whiff at 275; ends with a whiff at 545); length 269; the row's longest 269; q reaches 210 at step 485
      last whiff (step 275): valued; held valued at the last whiff (formed 273), ended at step 323 by H25 timeout drive (48 steps after the last whiff); held at the silence start: valued; held at step 485: nothing
      at the silence start: d_along -2.2; d_cross valued axis +1.2, other axis -11.2 (outward +); inside valued/other region 1/0; distance to the nearest region 0.0; nearest wall 71.6; class (v); cast `since` 1
      at step 485 (Agent12's engagement step): d_along +17.7; d_cross valued axis -3.0, other axis -7.0 (outward +); inside valued/other region 1/0; distance to the nearest region 0.0; nearest wall 68.5; class (v); cast `since` 210
      over the silence (Agent10): steps by class (i) 153, (ii) 0, (iii) 82, (iv) 0, (v) 34 -> majority (i); longest run inside a whiff region 33; nearest approach to a wall 41.6, contacts 0
      dwell before the silence valued/other 16/9 (last step at a source 275); after it 1/0; outcome Agent10 V, Agent12 V; Agent12 engaged at step 485, first whiff after it step 489 (other), u 4, leg 1
   row 251: cell 2 (odour B valued, +y); silence steps 37-284 (start = the step after the last whiff at 36; ends with a whiff at 285); length 248; the row's longest 248; q reaches 210 at step 246
      last whiff (step 36): other; held other at the last whiff (formed 26), ended at step 84 by H25 timeout drive (48 steps after the last whiff); held at the silence start: other; held at step 246: nothing
      at the silence start: d_along +1.3; d_cross valued axis -8.6, other axis -1.4 (outward +); inside valued/other region 0/1; distance to the nearest region 0.0; nearest wall 71.4; class (v); cast `since` 38
      at step 246 (Agent12's engagement step): d_along +29.3; d_cross valued axis -1.8, other axis -8.2 (outward +); inside valued/other region 0/0; distance to the nearest region 4.3; nearest wall 60.7; class (ii); cast `since` 247
      over the silence (Agent10): steps by class (i) 71, (ii) 96, (iii) 2, (iv) 0, (v) 79 -> majority (vi); longest run inside a whiff region 29; nearest approach to a wall 49.6, contacts 0
      dwell before the silence valued/other 0/5 (last step at a source 36); after it 7/3; outcome Agent10 N, Agent12 N; Agent12 engaged at step 246, first whiff after it step 292 (other), u 46, leg 2
   row 289: cell 1 (odour A valued, -y); silence steps 21-243 (start = the step after the last whiff at 20; ends with a whiff at 244); length 223; the row's longest 223; q reaches 210 at step 230
      last whiff (step 20): valued; held valued at the last whiff (formed 11), ended at step 68 by H25 timeout drive (48 steps after the last whiff); held at the silence start: valued; held at step 230: nothing
      at the silence start: d_along +7.6; d_cross valued axis -3.6, other axis -6.4 (outward +); inside valued/other region 0/0; distance to the nearest region 0.2; nearest wall 72.9; class (iii); cast `since` 1
      at step 230 (Agent12's engagement step): d_along +25.7; d_cross valued axis +2.9, other axis -12.9 (outward +); inside valued/other region 0/0; distance to the nearest region 0.7; nearest wall 64.0; class (ii); cast `since` 210
      over the silence (Agent10): steps by class (i) 127, (ii) 17, (iii) 32, (iv) 0, (v) 47 -> majority (i); longest run inside a whiff region 35; nearest approach to a wall 47.6, contacts 0
      dwell before the silence valued/other 0/0 (last step at a source -1); after it 19/0; outcome Agent10 V, Agent12 V; Agent12 engaged at step 230, first whiff after it step 311 (other), u 81, leg 2
   row 334: cell 1 (odour A valued, -y); silence steps 277-491 (start = the step after the last whiff at 276; ends with a whiff at 492); length 215; the row's longest 215; q reaches 210 at step 486
      last whiff (step 276): valued; nothing held at the last whiff; the last hold before it: valued, steps 119-168, ended by H25 timeout drive; held at the silence start: nothing; held at step 486: nothing
      at the silence start: d_along +2.2; d_cross valued axis +2.7, other axis -12.7 (outward +); inside valued/other region 0/0; distance to the nearest region 0.5; nearest wall 68.2; class (iii); cast `since` 1
      at step 486 (Agent12's engagement step): d_along +22.6; d_cross valued axis -2.6, other axis -7.4 (outward +); inside valued/other region 1/0; distance to the nearest region 0.0; nearest wall 65.1; class (v); cast `since` 210
      over the silence (Agent10): steps by class (i) 139, (ii) 0, (iii) 54, (iv) 0, (v) 22 -> majority (i); longest run inside a whiff region 22; nearest approach to a wall 45.1, contacts 0
      dwell before the silence valued/other 22/8 (last step at a source 275); after it 0/0; outcome Agent10 V, Agent12 V; Agent12 engaged at step 486, first whiff after it step 492 (valued), u 6, leg 1
   row 362: cell 3 (odour B valued, -y); silence steps 16-274 (start = the step after the last whiff at 15; ends with a whiff at 275); length 259; the row's longest 259; q reaches 210 at step 225
      last whiff (step 15): valued; held valued at the last whiff (formed 9), ended at step 63 by H25 timeout drive (48 steps after the last whiff); held at the silence start: valued; held at step 225: nothing
      at the silence start: d_along +11.0; d_cross valued axis -4.1, other axis -5.9 (outward +); inside valued/other region 1/0; distance to the nearest region 0.0; nearest wall 73.2; class (v); cast `since` 1
      at step 225 (Agent12's engagement step): d_along +28.9; d_cross valued axis -12.7, other axis +2.7 (outward +); inside valued/other region 0/0; distance to the nearest region 3.9; nearest wall 58.5; class (ii); cast `since` 210
      over the silence (Agent10): steps by class (i) 114, (ii) 48, (iii) 34, (iv) 0, (v) 63 -> majority (vi); longest run inside a whiff region 33; nearest approach to a wall 53.4, contacts 0
      dwell before the silence valued/other 0/0 (last step at a source -1); after it 0/1; outcome Agent10 N, Agent12 N; Agent12 engaged at step 225, first whiff after it step 292 (other), u 67, leg 2
   row 385: cell 2 (odour B valued, +y); silence steps 125-343 (start = the step after the last whiff at 124; ends with a whiff at 344); length 219; the row's longest 219; q reaches 210 at step 334
      last whiff (step 124): valued; held valued at the last whiff (formed 123), ended at step 172 by H25 timeout drive (48 steps after the last whiff); held at the silence start: valued; held at step 334: nothing
      at the silence start: d_along +0.3; d_cross valued axis +2.1, other axis -12.1 (outward +); inside valued/other region 1/0; distance to the nearest region 0.0; nearest wall 69.8; class (v); cast `since` 1
      at step 334 (Agent12's engagement step): d_along +19.2; d_cross valued axis -1.4, other axis -8.6 (outward +); inside valued/other region 1/0; distance to the nearest region 0.0; nearest wall 71.3; class (v); cast `since` 210
      over the silence (Agent10): steps by class (i) 145, (ii) 0, (iii) 47, (iv) 0, (v) 27 -> majority (i); longest run inside a whiff region 22; nearest approach to a wall 39.6, contacts 0
      dwell before the silence valued/other 12/9 (last step at a source 124); after it 16/0; outcome Agent10 V, Agent12 V; Agent12 engaged at step 334, first whiff after it step 344 (other), u 10, leg 1
   row 399: cell 0 (odour A valued, +y); silence steps 281-599 (start = the step after the last whiff at 280; ends at the run end, 600); length 319; the row's longest 319; q reaches 210 at step 490
      last whiff (step 280): valued; nothing held at the last whiff; the last hold before it: valued, steps 121-171, ended by H25 timeout drive; held at the silence start: nothing; held at step 490: nothing
      at the silence start: d_along +0.4; d_cross valued axis +2.4, other axis -12.4 (outward +); inside valued/other region 1/0; distance to the nearest region 0.0; nearest wall 69.9; class (v); cast `since` 1
      at step 490 (Agent12's engagement step): d_along +19.1; d_cross valued axis -1.5, other axis -8.5 (outward +); inside valued/other region 1/0; distance to the nearest region 0.0; nearest wall 71.5; class (v); cast `since` 210
      over the silence (Agent10): steps by class (i) 206, (ii) 0, (iii) 83, (iv) 0, (v) 30 -> majority (i); longest run inside a whiff region 28; nearest approach to a wall 38.2, contacts 0
      dwell before the silence valued/other 18/10 (last step at a source 280); after it 1/0; outcome Agent10 V, Agent12 V; Agent12 engaged at step 490, first whiff after it step 502 (other), u 12, leg 1

(A2) summary over the 18 silences (Agent10)
   silence start step 118/272/278 (min 16, max 284); step q reaches 210 326/481/487; silence length 218/226/263 (ended by a whiff 15, open at the run end 3)
   last whiff before the silence: valued 16, other (neutral) 2, both 0, from construction 0
   the hold at the last whiff: H25 timeout drive 9; nothing held at the last whiff 9; held at the silence start: nothing 8, valued 9, other 1
   at the silence start: d_along -2.3/-0.2/2.0 (min -3.3, max 21.3); upwind of both (d_along < 0) 9; beyond LMAX (d_along >= 25) 0; d_cross valued axis (outward +) -0.3/1.5/2.1, other axis -12.1/-11.5/-9.7; |d_cross| to the nearer axis 1.0/1.9/2.4; inside a whiff region 13; distance to the nearest region 0.0/0.0/0.0 (max 0.5); nearest wall 67.2/69.6/71.3 (within 1.0: 0)
   at the engagement step: d_along 15.8/19.0/22.0 (min 14.5, max 29.3); upwind of both (d_along < 0) 0; beyond LMAX (d_along >= 25) 3; d_cross valued axis (outward +) -3.2/-2.7/-1.5, other axis -8.5/-7.3/-6.8; |d_cross| to the nearer axis 1.8/2.8/3.2; inside a whiff region 14; distance to the nearest region 0.0/0.0/0.0 (max 4.3); nearest wall 67.2/70.1/71.4 (within 1.0: 0)
   cast `since` at the silence start equal to 1 (the last whiff was a navigation event, which resets it) 16/18
   cast `since` at the silence start 1/1/1 (min 1, max 250); at the engagement step 210/210/210
   rows with a wall contact during the silence 0; nearest approach to a wall during the silence 38.6/41.2/43.9

(A3) Agent12 in the same rows: engagement step 326/481/487; equal to the step Agent10's q reaches 210 in 18/18; a whiff after engagement 18/18 (first odour valued 3, other 15, both 0); u at that whiff 6/11/50; engaged to the run end 0
   outcome Agent10 -> Agent12 in these rows: V->V 14; V->N 1; N->N 3; Agent10 V 15, Agent12 V 14
   differing row 184: cell 1 (odour A valued, -y); Agent10 V (dwell valued/other 16/5), Agent12 N (dwell 2/22); engaged at 328, first whiff after it 344 (other); dwell before the silence 2/5
   rows whose outcome differs between the arms, all 400: [184] (never-engaged rows are bitwise equal, so any difference is in an engaged row)

(A4) position-based classification of the 18 silences (design section 2 categories; position only, no cause):
   majority class over the silence's steps (a class holding at least half of them; else (vi)): (i) upwind of both sources 16; (ii) beyond LMAX 25 downwind 0; (iii) crosswind outside both cones (0 <= d_along < 25) 0; (iv) at a wall (within 1.0) 0; (v) inside a whiff region, no whiff drawn 0; (vi) other: no class holds at least half the steps 2
   class at the silence start: (i) upwind of both sources 3; (ii) beyond LMAX 25 downwind 0; (iii) crosswind outside both cones (0 <= d_along < 25) 2; (iv) at a wall (within 1.0) 0; (v) inside a whiff region, no whiff drawn 13; (vi) other: no class holds at least half the steps 0
   class at the engagement step: (i) upwind of both sources 0; (ii) beyond LMAX 25 downwind 3; (iii) crosswind outside both cones (0 <= d_along < 25) 1; (iv) at a wall (within 1.0) 0; (v) inside a whiff region, no whiff drawn 14; (vi) other: no class holds at least half the steps 0
   pooled silence steps 4429: (i) 2693 (0.608); (ii) 161 (0.036); (iii) 880 (0.199); (iv) 0 (0.000); (v) 695 (0.157)
   longest run of consecutive steps inside a whiff region without a whiff, per silence: 22/28/34 (max 52)
   reference arithmetic (not measured): a stay inside the cone at fixed d_along, whiff probability p = 0.3 exp(-d_along / 12) per step:
      d_along  0.0: p 0.3000; P(210 steps without a whiff) = (1 - p)^210 = 2.96e-33; expected longest dry spell in 600 steps 15.7; P(a dry spell >= 210 within 600 steps) 0.00e+00
      d_along  5.0: p 0.1978; P(210 steps without a whiff) = (1 - p)^210 = 7.99e-21; expected longest dry spell in 600 steps 23.8; P(a dry spell >= 210 within 600 steps) 0.00e+00
      d_along 10.0: p 0.1304; P(210 steps without a whiff) = (1 - p)^210 = 1.82e-13; expected longest dry spell in 600 steps 34.9; P(a dry spell >= 210 within 600 steps) 9.40e-12
      d_along 15.0: p 0.0860; P(210 steps without a whiff) = (1 - p)^210 = 6.36e-09; expected longest dry spell in 600 steps 49.8; P(a dry spell >= 210 within 600 steps) 2.20e-07
      d_along 20.0: p 0.0567; P(210 steps without a whiff) = (1 - p)^210 = 4.79e-06; expected longest dry spell in 600 steps 69.9; P(a dry spell >= 210 within 600 steps) 1.11e-04
      d_along 24.0: p 0.0406; P(210 steps without a whiff) = (1 - p)^210 = 1.66e-04; expected longest dry spell in 600 steps 90.5; P(a dry spell >= 210 within 600 steps) 2.79e-03

(A5) timing against the dwell: silences starting after the agent had reached a source 16/18 (valued dwell before > 0: 15, other dwell before > 0: 14); never reached a source before the silence 2
   steps from the last step at a source to the silence start 1/1/2 (min 1, max 120); dwell before the silence valued 4/10/14, other 5/6/9; dwell after the silence start valued 1/8/16, other 0/0/0
   reached a source before the silence (16): dwell-majority outcome Agent10 V/N/tie [14, 2, 0], Agent12 [13, 3, 0]
   never reached one (2): dwell-majority outcome Agent10 V/N/tie [1, 1, 0], Agent12 [1, 1, 0]
   for comparison, the 374 rows whose longest silence is 150-209 (never engaged): start step 126/194/334; class at the start (i) 144, (ii) 0, (iii) 22, (iv) 0, (v) 208; reached a source before it 371

== (B) the bench (h2) wall contacts: World7 +1/-1, 400 x 600, Agent12 vs Agent10 ==

(B1) contacts
   [Agent12] contacts 99 = 0.247 per row; rows with any contact 39; contacts per contacting row 2.0/2.0/2.0 (max 18)
   [Agent10] contacts 0 = 0.000 per row; rows with any contact 0; contacts per contacting row n/a (max 0)

(B2) every Agent12 contact (99); the contact is registered by the move after step t's act, so engaged/u/leg/slant/hold are step t's; position = after the move (reflected); wall by that position; stranded = the row has a drive-ended negative hold (ph24c.released) in that arm
   row   0 step 426: engaged 1, u 174, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +13.5, y - y_source valued/negative -81.6/-71.6; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row   0 step 440: engaged 1, u 188, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +10.8, y - y_source valued/negative -81.6/-71.6; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row   1 step 432: engaged 1, u 175, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +12.2, y - y_source valued/negative -83.7/-73.7; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row   1 step 444: engaged 1, u 187, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +9.2, y - y_source valued/negative -83.4/-73.4; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row   3 step 416: engaged 1, u 174, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +21.7, y - y_source valued/negative -81.5/-71.5; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row   3 step 429: engaged 1, u 187, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +18.5, y - y_source valued/negative -81.6/-71.6; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row  37 step 409: engaged 1, u 172, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +25.1, y - y_source valued/negative -80.9/-70.9; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row  37 step 427: engaged 1, u 190, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +21.2, y - y_source valued/negative -80.6/-70.6; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row  43 step 412: engaged 1, u 167, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +14.3, y - y_source valued/negative -79.0/-69.0; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row  43 step 440: engaged 1, u 195, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +8.5, y - y_source valued/negative -79.3/-69.3; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row  50 step 406: engaged 1, u 169, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +23.9, y - y_source valued/negative -81.9/-71.9; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row  50 step 431: engaged 1, u 194, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +18.8, y - y_source valued/negative -82.2/-72.2; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row  66 step 410: engaged 1, u 172, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +18.3, y - y_source valued/negative -80.6/-70.6; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row  66 step 428: engaged 1, u 190, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +14.7, y - y_source valued/negative -80.2/-70.2; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row  85 step 410: engaged 1, u 166, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +19.7, y - y_source valued/negative -78.5/-68.5; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row  85 step 440: engaged 1, u 196, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +12.8, y - y_source valued/negative -78.3/-68.3; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 102 step 413: engaged 1, u 179, leg 3, slant +1; held nothing; wall side, negative source's side (y = 160); d_along +24.3, y - y_source valued/negative +86.5/+76.5; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 102 step 417: engaged 1, u 183, leg 4, slant +1; held nothing; wall side, negative source's side (y = 160); d_along +22.5, y - y_source valued/negative +86.5/+76.5; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 111 step 413: engaged 1, u 169, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +16.5, y - y_source valued/negative -80.1/-70.1; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 111 step 437: engaged 1, u 193, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +11.3, y - y_source valued/negative -80.4/-70.4; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 124 step 420: engaged 1, u 171, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +15.5, y - y_source valued/negative -78.9/-68.9; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 124 step 440: engaged 1, u 191, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +11.4, y - y_source valued/negative -79.1/-69.1; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 129 step 404: engaged 1, u 173, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +24.1, y - y_source valued/negative -78.5/-68.5; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 129 step 420: engaged 1, u 189, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +20.6, y - y_source valued/negative -78.1/-68.1; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 131 step 417: engaged 1, u 172, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +17.2, y - y_source valued/negative -79.5/-69.5; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 131 step 434: engaged 1, u 189, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +13.1, y - y_source valued/negative -79.5/-69.5; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 139 step 513: engaged 1, u 178, leg 3, slant +1; held nothing; wall upwind (x = 0); side, valued source's side (y = 0); d_along -72.4, y - y_source valued/negative -71.7/-81.7; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 139 step 514: engaged 1, u 179, leg 3, slant +1; held nothing; wall upwind (x = 0); d_along -72.4, y - y_source valued/negative -71.1/-81.1; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 139 step 517: engaged 1, u 182, leg 4, slant +1; held nothing; wall upwind (x = 0); d_along -72.3, y - y_source valued/negative -69.3/-79.3; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 139 step 524: engaged 1, u 189, leg 4, slant +1; held nothing; wall side, valued source's side (y = 0); d_along -71.2, y - y_source valued/negative -71.3/-81.3; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 139 step 535: engaged 1, u 200, leg 4, slant +1; held nothing; wall upwind (x = 0); d_along -72.4, y - y_source valued/negative -64.9/-74.9; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 139 step 536: engaged 1, u 201, leg 4, slant +1; held nothing; wall upwind (x = 0); d_along -72.3, y - y_source valued/negative -64.4/-74.4; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 139 step 543: engaged 1, u 208, leg 4, slant +1; held nothing; wall upwind (x = 0); d_along -72.4, y - y_source valued/negative -60.2/-70.2; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 139 step 544: engaged 1, u 209, leg 4, slant +1; held nothing; wall upwind (x = 0); d_along -72.2, y - y_source valued/negative -59.7/-69.7; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 139 step 547: engaged 1, u 212, leg 4, slant +1; held nothing; wall upwind (x = 0); d_along -72.4, y - y_source valued/negative -57.9/-67.9; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 139 step 548: engaged 1, u 213, leg 4, slant +1; held nothing; wall upwind (x = 0); d_along -72.3, y - y_source valued/negative -57.4/-67.4; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 139 step 551: engaged 1, u 216, leg 4, slant +1; held nothing; wall upwind (x = 0); d_along -72.4, y - y_source valued/negative -55.6/-65.6; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 139 step 552: engaged 1, u 217, leg 4, slant +1; held nothing; wall upwind (x = 0); d_along -72.2, y - y_source valued/negative -55.1/-65.1; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 139 step 556: engaged 1, u 221, leg 4, slant +1; held nothing; wall upwind (x = 0); d_along -72.3, y - y_source valued/negative -52.8/-62.8; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 139 step 578: engaged 1, u 243, leg 4, slant +1; held nothing; wall upwind (x = 0); d_along -72.4, y - y_source valued/negative -64.6/-74.6; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 139 step 579: engaged 1, u 244, leg 4, slant +1; held nothing; wall upwind (x = 0); d_along -72.3, y - y_source valued/negative -65.2/-75.2; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 139 step 585: engaged 1, u 250, leg 4, slant +1; held nothing; wall upwind (x = 0); d_along -72.3, y - y_source valued/negative -68.7/-78.7; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 139 step 586: engaged 1, u 251, leg 4, slant +1; held nothing; wall upwind (x = 0); d_along -72.4, y - y_source valued/negative -69.2/-79.2; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 139 step 589: engaged 1, u 254, leg 4, slant +1; held nothing; wall upwind (x = 0); d_along -72.4, y - y_source valued/negative -71.0/-81.0; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 145 step 394: engaged 1, u 169, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +31.2, y - y_source valued/negative -81.6/-71.6; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 145 step 418: engaged 1, u 193, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +25.9, y - y_source valued/negative -81.2/-71.2; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 152 step 420: engaged 1, u 168, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +18.1, y - y_source valued/negative -79.5/-69.5; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 152 step 446: engaged 1, u 194, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +12.7, y - y_source valued/negative -79.6/-69.6; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 158 step 403: engaged 1, u 170, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +25.2, y - y_source valued/negative -80.8/-70.8; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 158 step 424: engaged 1, u 191, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +20.8, y - y_source valued/negative -80.7/-70.7; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 182 step 575: engaged 1, u 150, leg 3, slant +1; held nothing; wall upwind (x = 0); d_along -71.3, y - y_source valued/negative -14.9/-4.9; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 V lost (Agent10 V lost)
   row 182 step 593: engaged 1, u 168, leg 3, slant +1; held nothing; wall upwind (x = 0); d_along -71.4, y - y_source valued/negative -24.0/-14.0; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 V lost (Agent10 V lost)
   row 197 step 404: engaged 1, u 170, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +21.6, y - y_source valued/negative -79.3/-69.3; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 197 step 425: engaged 1, u 191, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +17.6, y - y_source valued/negative -79.4/-69.4; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 203 step 559: engaged 1, u 171, leg 3, slant +1; held nothing; wall upwind (x = 0); d_along -68.3, y - y_source valued/negative +12.0/+2.0; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 203 step 570: engaged 1, u 182, leg 4, slant +1; held nothing; wall upwind (x = 0); d_along -68.3, y - y_source valued/negative +15.1/+5.1; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 203 step 585: engaged 1, u 197, leg 4, slant +1; held nothing; wall upwind (x = 0); d_along -68.3, y - y_source valued/negative +22.9/+12.9; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 203 step 586: engaged 1, u 198, leg 4, slant +1; held nothing; wall upwind (x = 0); d_along -68.1, y - y_source valued/negative +23.4/+13.4; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 203 step 589: engaged 1, u 201, leg 4, slant +1; held nothing; wall upwind (x = 0); d_along -68.3, y - y_source valued/negative +25.2/+15.2; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 205 step 424: engaged 1, u 176, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +9.7, y - y_source valued/negative -82.8/-72.8; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 205 step 433: engaged 1, u 185, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +6.7, y - y_source valued/negative -82.8/-72.8; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 206 step 409: engaged 1, u 177, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +20.6, y - y_source valued/negative -82.0/-72.0; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 206 step 417: engaged 1, u 185, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +18.3, y - y_source valued/negative -82.0/-72.0; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 214 step 592: engaged 1, u 167, leg 3, slant +1; held nothing; wall upwind (x = 0); d_along -72.3, y - y_source valued/negative -6.7/+3.3; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 V lost (Agent10 V lost)
   row 214 step 593: engaged 1, u 168, leg 3, slant +1; held nothing; wall upwind (x = 0); d_along -72.1, y - y_source valued/negative -6.2/+3.8; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 V lost (Agent10 V lost)
   row 214 step 597: engaged 1, u 172, leg 3, slant +1; held nothing; wall upwind (x = 0); d_along -72.3, y - y_source valued/negative -3.9/+6.1; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 V lost (Agent10 V lost)
   row 214 step 598: engaged 1, u 173, leg 3, slant +1; held nothing; wall upwind (x = 0); d_along -72.0, y - y_source valued/negative -3.4/+6.6; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 V lost (Agent10 V lost)
   row 232 step 415: engaged 1, u 176, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +16.7, y - y_source valued/negative -82.0/-72.0; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 232 step 425: engaged 1, u 186, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +14.0, y - y_source valued/negative -82.2/-72.2; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 238 step 414: engaged 1, u 169, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +12.7, y - y_source valued/negative -80.5/-70.5; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 238 step 437: engaged 1, u 192, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +7.9, y - y_source valued/negative -80.3/-70.3; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 250 step 404: engaged 1, u 166, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +23.4, y - y_source valued/negative -78.3/-68.3; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 250 step 434: engaged 1, u 196, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +17.8, y - y_source valued/negative -78.1/-68.1; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 251 step 409: engaged 1, u 171, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +21.1, y - y_source valued/negative -81.4/-71.4; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 251 step 429: engaged 1, u 191, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +16.1, y - y_source valued/negative -81.7/-71.7; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 258 step 392: engaged 1, u 178, leg 3, slant +1; held nothing; wall side, valued source's side (y = 0); d_along +28.6, y - y_source valued/negative -70.8/-80.8; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 258 step 400: engaged 1, u 186, leg 4, slant +1; held nothing; wall side, valued source's side (y = 0); d_along +26.0, y - y_source valued/negative -70.8/-80.8; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 259 step 405: engaged 1, u 169, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +20.0, y - y_source valued/negative -78.7/-68.7; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 259 step 429: engaged 1, u 193, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +14.8, y - y_source valued/negative -78.5/-68.5; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 285 step 402: engaged 1, u 171, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +30.3, y - y_source valued/negative -82.3/-72.3; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 285 step 422: engaged 1, u 191, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +26.4, y - y_source valued/negative -82.5/-72.5; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 322 step 395: engaged 1, u 165, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +27.6, y - y_source valued/negative -78.9/-68.9; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 322 step 426: engaged 1, u 196, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +21.5, y - y_source valued/negative -78.7/-68.7; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 331 step 414: engaged 1, u 175, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +15.8, y - y_source valued/negative -82.3/-72.3; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 331 step 425: engaged 1, u 186, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +12.6, y - y_source valued/negative -82.3/-72.3; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 332 step 406: engaged 1, u 176, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +23.6, y - y_source valued/negative -81.3/-71.3; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 332 step 416: engaged 1, u 186, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +20.8, y - y_source valued/negative -81.7/-71.7; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 340 step 413: engaged 1, u 173, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +19.3, y - y_source valued/negative -81.4/-71.4; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 340 step 428: engaged 1, u 188, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +16.0, y - y_source valued/negative -81.3/-71.3; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 367 step 399: engaged 1, u 170, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +25.6, y - y_source valued/negative -79.3/-69.3; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 367 step 421: engaged 1, u 192, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +20.9, y - y_source valued/negative -79.1/-69.1; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 368 step 398: engaged 1, u 167, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +27.7, y - y_source valued/negative -77.8/-67.8; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 368 step 426: engaged 1, u 195, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +21.4, y - y_source valued/negative -78.0/-68.0; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 370 step 411: engaged 1, u 174, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +17.7, y - y_source valued/negative -80.3/-70.3; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 370 step 425: engaged 1, u 188, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +14.3, y - y_source valued/negative -80.7/-70.7; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 386 step 429: engaged 1, u 178, leg 3, slant +1; held nothing; wall side, negative source's side (y = 160); d_along +10.9, y - y_source valued/negative +85.5/+75.5; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 386 step 435: engaged 1, u 184, leg 4, slant +1; held nothing; wall side, negative source's side (y = 160); d_along +8.8, y - y_source valued/negative +86.0/+76.0; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 N lost (Agent10 N lost)
   row 396 step 397: engaged 1, u 168, leg 3, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +30.4, y - y_source valued/negative -80.4/-70.4; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)
   row 396 step 423: engaged 1, u 194, leg 4, slant +1; held nothing; wall side, negative source's side (y = 0); d_along +24.7, y - y_source valued/negative -80.4/-70.4; stranded row Agent10/Agent12 1/1 (after an Agent12 release 1); next whiff none; outcome Agent12 tie lost (Agent10 tie lost)

(B2) summary over 99 contacts in 39 rows
   engaged at the contact 99/99; not engaged 0 (held then: nothing 0, valued 0, negative 0)
   by leg (engaged contacts): leg 3 44; leg 4 55; legs 5-6 0; u >= 300 0 = 0.000 of engaged contacts, 0.000 of all contacts; u at the contact 172/185/194 (min 150, max 254)
   by slant (engaged): upwind (+1) 99, downwind (-1) 0
   by wall: side, negative source's side (y = 0) 64; side, negative source's side (y = 160) 4; side, valued source's side (y = 0) 3; upwind (x = 0) 27; upwind (x = 0); side, valued source's side (y = 0) 1
   by wall, rows: side, negative source's side (y = 0) 32; side, negative source's side (y = 160) 2; side, valued source's side (y = 0) 2; upwind (x = 0) 4; upwind (x = 0); side, valued source's side (y = 0) 1; contacts per row by row: 0: 2, 1: 2, 3: 2, 37: 2, 43: 2, 50: 2, 66: 2, 85: 2, 102: 2, 111: 2, 124: 2, 129: 2, 131: 2, 139: 18, 145: 2, 152: 2, 158: 2, 182: 2, 197: 2, 203: 5, 205: 2, 206: 2, 214: 4, 232: 2, 238: 2, 250: 2, 251: 2, 258: 2, 259: 2, 285: 2, 322: 2, 331: 2, 332: 2, 340: 2, 367: 2, 368: 2, 370: 2, 386: 2, 396: 2
   d_along at the contact -68.3/14.7/21.0 (upwind of the sources 29); |d_cross| to the valued axis 70.1/79.3/81.5
   contacts in Agent10-stranded rows 99/99; in Agent12-stranded rows 99/99 (after an Agent12 release in the row 99)
   a whiff of either odour after the contact in the row 0/99 (first valued 0, negative 0, both 0); steps to it n/a
      leg 3: contacts 44 in 39 rows, followed by a whiff 0; contacts in rows ending V 6, in lost rows 44
      leg 4: contacts 55 in 37 rows, followed by a whiff 0; contacts in rows ending V 0, in lost rows 55
   contacting rows 39: Agent12 V 2 (0.051), N 12, tie 25; lost 39 (1.000); engaged rows 39; Agent10-stranded 39; Agent12-stranded 39
   first contact step in the contacting rows 404/411/418; first engaged step 232/238/246; first contact before the first engaged step 0
   at the first engaged step, contacting rows (39): d_along 43.4/48.8/53.5; |d_cross| to the nearer axis 39.4/40.7/41.9; distance to the nearer side wall 28.6/30.5/32.5 (min 26.4); distance to the upwind wall 115.3/119.8/124.6 (min 24.6); Agent10-stranded 39
   at the first engaged step, engaged rows without a contact (117): d_along 26.6/45.3/54.3; |d_cross| to the nearer axis 12.2/21.8/34.7; distance to the nearer side wall 42.3/55.0/61.2 (min 32.6); distance to the upwind wall 97.2/116.1/124.1 (min 27.0); Agent10-stranded 92

(B3) the (h2) effect decomposed
   Agent10 stranded rows (a drive-ended negative hold) 139; Agent12 stranded rows 143 (both 139, Agent12 only 4, Agent10 only 0)
   of Agent10's stranded rows: engaged in Agent12 131; the first release precedes the first engaged step (the same release in both arms, rows identical before engagement) 130; first engaged step - first release 160/162/162; not engaged 8 (their last-third whiff: lost in Agent10 2)
   engaged stranded rows 131: a whiff after the first engaged step 37 (first odour valued 12, negative 25, both 0, none 94); a negative hold re-formed after engagement 16; stranded again (a drive-ended negative hold after engagement) 14; a valued hold formed after engagement 17; the valued source reached after engagement 17
      first whiff valued (12): Agent12 V/N/tie [9, 3, 0], lost 0; re-formed negative hold 1, stranded again 0; rows with a contact 0
      first whiff negative (25): Agent12 V/N/tie [4, 16, 5], lost 6; re-formed negative hold 15, stranded again 14; rows with a contact 0
      no whiff (94): Agent12 V/N/tie [30, 18, 46], lost 94; re-formed negative hold 0, stranded again 0; rows with a contact 39
   Agent10's stranded rows, outcome in Agent10: V 38 N 30 tie 71; lost 133
   Agent10's stranded rows, outcome in Agent12: V 51 N 37 tie 51; lost 102
   Agent12 engaged rows not stranded in Agent10: 25 (Agent10 outcome V/N/tie [19, 1, 5], lost 7; Agent12 V/N/tie [21, 3, 1], lost 4; held nothing at any step before engagement 0)
   paired outcome table, all 400 rows (rows Agent10, columns Agent12):
      Agent10 V  : -> V 289  -> N   3  -> tie   1
      Agent10 N  : -> V   5  -> N  26  -> tie   0
      Agent10 tie: -> V  14  -> N  11  -> tie  51
   into V 19, out of V 4 (net +15 = P(V) DP +0.0375); into lost 3, out of lost 37 (net -34 = lost DP -0.0850)
      Agent10-stranded rows (139): into V 13, out of V 0; into lost 0, out of lost 31
      other rows (261): into V 6, out of V 4; into lost 3, out of lost 6
      Agent12 contact rows (39): into V 0, out of V 0; into lost 0, out of lost 0
      Agent12 no-contact rows (361): into V 19, out of V 4; into lost 3, out of lost 37
      engaged, no contact (117): into V 19, out of V 4; into lost 3, out of lost 37
      never engaged (244): into V 0, out of V 0; into lost 0, out of lost 0

(B4) P(V | wall contact) and P(lost | wall contact), Agent12's contact rows (Wilson 95 percent)
   Agent12 P(V | contact) 2/39 = 0.051 [0.014, 0.169]; P(V | no contact) 306/361 = 0.848 [0.807, 0.881]
   Agent12 P(lost | contact) 39/39 = 1.000 [0.910, 1.000]; P(lost | no contact) 67/361 = 0.186 [0.149, 0.229]
   paired on the same rows: in Agent12's contact rows Agent12 V 2/39, Agent10 V 2/39; lost Agent12 39, Agent10 39; in the no-contact rows Agent12 V 306/361, Agent10 V 291/361; lost Agent12 67, Agent10 101
   engaged rows only (156): P(V | contact) 2/39 = 0.051 [0.014, 0.169], P(V | no contact) 62/117 = 0.530 [0.440, 0.618]; P(lost | contact) 39/39 = 1.000 [0.910, 1.000], P(lost | no contact) 65/117 = 0.556 [0.465, 0.642]
   Agent10-stranded rows (139): P(V | Agent12 contact) 2/39 = 0.051 [0.014, 0.169], without 49/100 = 0.490 [0.394, 0.587]; P(lost | contact) 39/39 = 1.000 [0.910, 1.000], without 63/100 = 0.630 [0.532, 0.718]

== end (measurement only; positions and counts, no cause named; no change tested; bench seeds only) ==
```
