# H20 Run 2 report: the supplied-value choice test with the dwell-majority measure

Date 2026-09-21. Design v1 FINAL doc d3866101cd92f911d (confirmed by the owner as written, decision:h20-run2-open; hash of the draft it confirms b88f0769...b115). Code ph18.py sha256 26ad4defb7590e16e1030b0b6f8073d3258584baeec06ba66e233315da7c97c3. One evaluation, world seed 1695, agent seed 1795, 400 rows x 600 steps, G 2, geometry C0, 95 percent intervals, no extension. Evaluation output ph18_eval.txt sha256 321d8ff19092ffc6cdadd83cf8b48206a269e99b4248434242c816fdb6e15394. Nothing was changed after the table.

**Status: NOT shown under the registered criteria.** R1 PASS, R2 FAIL, R3 PASS, R4 PASS. Closure is the owner's. Stage A's verdict (NOT shown; decision:h20-stage-a-closed) stands and is not re-judged. A statement about a supplied value in this task and this measure; not about learning; not about the first source reached.

## 1. What was asked

H20 (unchanged from Stage A): given the opportunity to approach both, the agent chooses the odour that carries a positive value over an odour that carries none. Run 2 supplies the value (+1 / 0 / -1 per odour) and does not learn. Main measure, changed from Stage A: the source the agent stays at more over the 600 steps (dwell within 3.0; a tie is no choice). Geometry C0 kept (sources 10 apart, midline start 20 downwind). Known-answer arm (held odour fixed to the valued odour by intervention, G 0) as the measure's ceiling; pathway-off as its floor. The first source reached is reported as a secondary measure. Criteria R1-R4; a criterion PASSes if every part passes, FAILs if any part fails, INCONCLUSIVE otherwise.

## 2. Implementation, self-checks, development run

ph18.py uses ph16's world, agent and criteria code and ph17's Agent5 intervention with the held odour set per row to that row's valued odour. No adopted module was edited. Self-checks (demo output sha 64027deb...2174): G 0 reproduces Agent3; geometry and pre-hold; constructed-state priority; known-answer h is the valued odour on every step and the hit is its whiffs; majority classes; neutral at G 2 bitwise equal to G 0 on 40 rows x 200 steps.

Development run (seeds 9840/9940, output sha 80f90c21...bdab): no operation error. R1 PASS, R3 PASS, R4 PASS. R2 printed FAIL on those seeds (P(V) 209/400 = 0.522; DP 0.050); that printout is not the verdict. No amendment. Evaluation seeds unused until the one evaluation.

## 3. Results, one evaluation (seeds 1695 / 1795)

| arm | values | G | selection | V | N | tie | first hold valued / neutral / none | P(V) dwell majority |
|---|---|---|---|---|---|---|---|---|
| bias | +1 / 0 | 2 | circuit | 214 | 180 | 6 | 274 / 125 / 1 | 0.535 [0.486, 0.583] |
| neutral | 0 / 0 | 2 | circuit | 203 | 190 | 7 | 210 / 186 / 4 | 0.508 |
| pathway-off | +1 / 0 | 0 | circuit | 203 | 190 | 7 | 210 / 186 / 4 | 0.508 [floor: P(V \| chose) 0.517] |
| known-answer | +1 / 0 | 0 | held odour fixed to valued | 377 | 22 | 1 | 400 / 0 / 0 (step 0) | 0.943 [0.915, 0.961] |
| priority | +1 / -1 | 2 | circuit | 365 | 22 | 13 | 278 / 122 / 0 | 0.912 [0.881, 0.936] |
| priority-off | +1 / -1 | 0 | circuit | 369 | 15 | 16 | 228 / 171 / 1 | 0.922 |

Cells of the bias arm (V of 100; odour A +y, A -y, B +y, B -y): 55 / 48 / 57 / 54. Dwell median valued / other: bias 14.0 / 11.0; pathway-off 12.0 / 12.0; known-answer 26.0 / 0.0; priority 22.0 / 0.0. First-approach step median 31 in the four arms without a negative value. No wall contact in those four; 0.33-0.35 contacts per row in the priority arms. Input range at G 2: y' max 5.34, y' > 1.8 on 2.74 percent (bias) to 3.84 percent (priority) of channel-steps, the clip (s >= 4.9) on 0.00-0.01 percent of steps, s max 4.93-4.95. No arm flagged on the clip.

Secondary, first reach (V / N / none): bias 213 / 187 / 0, P(V) 0.532 [0.484, 0.581]; pathway-off 210 / 190 / 0, 0.525 [0.476, 0.573]; known-answer 224 / 176 / 0, 0.560 [0.511, 0.608] (that measure's ceiling with a perfect selection).

## 4. Criteria

- **R1 task validity: PASS.** (a) ties 7 / 7 / 1 of 400 in neutral, pathway-off and known-answer, all at most 0.20. (b) neutral P(+y source majority | chose) 202/393 = 0.514 [0.465, 0.563], inside [0.35, 0.65]. (c) floor: pathway-off P(V | chose) 203/393 = 0.517 [0.467, 0.566], inside [0.35, 0.65]. (d) ceiling: known-answer P(V) 377/400 = 0.943 [0.915, 0.961], lower bound >= 0.85.
- **R2 main: FAIL.** (a) bias P(V) 214/400 = 0.535 [0.486, 0.583] against 0.70: FAIL. (b) cells 55, 48, 57, 54 of 100, intervals [0.452, 0.644], [0.385, 0.577], [0.472, 0.663], [0.443, 0.634] against 0.55: all INCONCLUSIVE. (c) DP = P(V) bias minus pathway-off 0.028 [-0.002, 0.055] against +0.20: FAIL. Reported: N 180, tie 6; P(V) bias / known-answer = 0.535 / 0.943 = 0.568 of the ceiling.
- **R3 identity: PASS.** Neutral at G 2 and at G 0: positions, headings and circuit states bitwise equal; G 0 reproduces ph14.Agent3; in the known-answer arm h equals the row's valued odour on every step and the hit equals that channel's whiffs.
- **R4 priority: PASS.** (a)(i) constructed state: negative odour held on 300 (row, step), target the flee side on every one, equal to G 0's on all 300; the valued odour took the hold on 250 afterwards: PASS. (a)(ii) in the run: negative odour held in 198 rows over 37,414 (row, step) in priority and 218 rows over 40,000 in priority-off; violations 0 in both: PASS. (b) dwell at the negative source, priority minus priority-off, mean +0.368 [+0.107, +0.640] against at most +1.0: PASS (rows ever within 3.0 of it 110 against 95; first entry to exit beyond 6.0 median 14 against 14 steps; none stayed). (c) priority P(V) 365/400 = 0.912 [0.881, 0.936] against 0.70: PASS. Reported without a bar: DP = P(V) priority minus priority-off -0.010 [-0.030, +0.010].

**Run 2 under the registered criteria: NOT shown.** R1 PASS, R2 FAIL, R3 PASS, R4 PASS. The whole-run reading follows R2's FAIL.

## 5. Where the failure appears (measured; it names no cause by itself)

The measure can express a perfect selection: the known-answer arm stays at the valued source in 377 of 400 rows (dwell median 26 against 0), matching the link check's 0.95-0.97 in C0. The floor sits at chance (pathway-off 203 of 400; P(V | chose) 0.517). R1 is therefore not the reason R2 fails.

The gain moves the first hold. In the bias arm the first hold is the valued odour in 274 of 400 rows against 210 in pathway-off, and it forms earlier (step median 13 against 30). That is the same diagnostic observation as in Stage A (277 against 200). It is not a registered criterion.

The gain does not move the majority source. Bias P(V) 214/400 against pathway-off 203/400, DP 0.028 with an interval that includes zero. Dwell medians 14 against 11, against 26 against 0 when the identity is fixed from step 0. Of the 180 N rows in the bias arm, 72 selected the neutral odour first and held it at the first reach; 48 were holding the valued odour at the moment they reached the other source; 66 held nothing at the reach. P(V | first hold valued) is 186/274 on the majority measure.

The first-reach secondary stays near chance in every arm, including the known-answer arm (0.560 [0.511, 0.608]), as the link check and the design's prediction required for C0.

R4(c) passes because the negative source is avoided, not because the gain adds a positive choice on top of that avoidance. Priority-off (G 0, values +1 / -1) already has P(V) 369/400 = 0.922; the reported DP of the gain in that pair is -0.010. The registered avoidance-maintenance clauses (a, b) passed with 0 flee violations and a dwell increase at the punisher inside the allowed +1 step.

## 6. What is shown and what is not

- Shown (registered): the task is valid for this measure (R1: ties rare, side balanced, floor at chance, ceiling at 0.94); the gain changes nothing when every value is zero (R3, exact); the registered avoidance-maintenance criteria passed with the gain on (R4 a, b) and P(V) in the priority arm met 0.70 (R4 c).
- Shown (diagnostic, not a criterion): a supplied positive value, through the gain, changes which odour the moving agent selects first (274 against 210 of 400). A perfect selection, imposed from step 0, is expressed in the majority source (0.943). The first source reached is not expressed even then (0.560).
- NOT shown: that a supplied positive value changes which source the agent stays at more (R2 FAIL, P(V) 0.535, DP 0.028, 0.568 of the ceiling).
- Not tested: learning (B), the integrated environment (C), any G other than 2, any geometry other than C0, and any navigation change.

## 7. Provenance

- Design v1 FINAL doc d3866101cd92f911d (draft hash b88f0769...b115; stored content hash 1c285b0a...a98c). Opened by decision:h20-run2-open. Stage A closed as not shown (decision:h20-stage-a-closed); link check report df9cf42bb99c43d39.
- Self-checks: ph18.py sha 26ad4def...97c3, demo output sha 64027deb...2174.
- Development run: seeds 9840/9940, output ph18_dev.txt sha 80f90c21...bdab; no operation error; no amendment.
- Evaluation: the same ph18.py, seeds 1695/1795 unused before this run, output ph18_eval.txt sha 321d8ff1...5394.
- Result: record:h20-run2-result. Closure is the owner's.
