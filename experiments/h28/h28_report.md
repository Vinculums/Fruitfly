# H28 report: a burst-ranked value tie discounting a ubiquitous, never-reinforced odour

Date 2026-09-26. Design v2 FINAL doc da2c1c079a1766d3e (confirmed by the owner 2026-09-26, decision:h28-open, '권고안으로 진행하고 다음작업 설계 진행', gloss 'proceed with the recommended options, then proceed with the next work's design'; hash b12137f684fb44d80f5a780fccfd1dc0f63669b5530d2a3eaf834b8df0316b8c, equal to the local file's sha256). Signed before code: decision:classification-rule-relaxed-burst-record-h28, decision:evidence-release-composition-rule-h28, decision:classification-rule-relaxed-presence-prior-h28. Code src/ph33.py sha256 f2a29722a398c81b7f73014d29c799a08c289eca1cc7366acd65e50154e720b0 (source doc dd7262b0c91dbc66b, content_hash equal), the same file for the demo, bench, development run and evaluation. One evaluation, world seed 2093, agent seed 2197, 400 rows x 600 steps, supplied +1/0/0, G 2, gate on, C0, learning off, D at p_D 0.03 from its own generator; bootstrap seed 20261133, 95 percent.

**Status: H28 SHOWN under its registered criteria: M1, M2 (b, c), M3, M4 and M5(a') all PASS.** The printout's summary label is the registered verdict sentence: with a ubiquitous, never-reinforced odour arriving as background whiffs at p_D 0.03, the adopted agent whose value ties are ranked by the recency of each odour's last burst (three whiffs within 10 steps) keeps its choice in the H21 task within 0.05 of itself without the distractor (DP -0.0275 [-0.0450, -0.0125]), and in the absent-odour world loses at least 20 points fewer rows than the same agent without the ranking (lost-row DP -0.445 [-0.495, -0.397]; 222 against 400 lost). H27's W1D bars against D off, reported and not registered, all fail (as the design predicted, 2.4): the distractor still costs the absent-odour world a great deal (222 lost against 29 without D). Closure is the owner's.

## 1. What was asked

H28 (design v2 section 1): with H27's third odour D (value 0, never reinforced, whiffs at p_D 0.03 anywhere), the adopted agent composed with three channels and given a burst-ranked value tie (Agent16: when present non-negative odours tie at the top value, only the one that most recently delivered three whiffs within 10 steps may steer or keep; none if none has burst) (i) keeps its choice in the H21 task within an allowed gap of itself without D on the same rows [M2(b)], and (ii) in the absent-odour world W1 with D loses at least 20 points fewer rows than H27's Agent15 [M5(a')]. With D absent the rule never acts, so it is the adopted agent (checked, M3/M4).

## 2. Implementation, self-checks, bench, development run

src/ph33.py composes Agent16 = (ReleaseN2, Agent14, Act16), Act16(Act15), from src/ph32.py imported unchanged (sha256 d9f585d5...2743 checked at run time) and the adopted modules imported unchanged (sha256 in every output header); no adopted file and not ph32.py is edited. Act16.act repeats Act15.act with three changes only: the burst record updated with the presence counter, the ranked top set, and keep. Readings R1-R14 where the design is silent are in the file header and printed in every output (for example R2: the most recent whiff is read from the presence counter, so the stored state is exactly the signed pair, the second most recent whiff and the last burst; R8: the entry-point classes).

**Self-checks (demo, experiments/h28/ph33_demo.txt sha256 370839e0b0046c25652c7b34e0a2a4c31e9f250da0f1e3287e2438c9751f8c2f):** 8/8 ok: method order (ReleaseN2's base act is Act16.act); this harness equals ph32.run bitwise for H27's arms; parallel equals sequential; identities (I1')-(I6'); bench (b), (c) and H27's (b3), (c) on the demo seeds; entry-point classification exact; the pass-probability arithmetic reproduces design section 7 (M2(b) k 5/8/10/12/13/15 = 1.000/0.990/0.893/0.650/0.506/0.260; M5(a') L 250/280/300/320 = 1.000/0.992/0.637/0.025); seed scan clean (24 numbers, 224 files). Fixed before the recorded demo, noted in its header: one earlier trial run on the demo seeds printed the (I1') labels with the first letter cut; the label slice was corrected; no model, harness, bar or rule code changed.

**Mechanism bench (M4), experiments/h28/ph33_bench.txt sha256 45b0f2630598f92a0770f08bff51d044cfc8a46aff4f1017dcb5602213178671, record:h28-bench-result: PASS; both stop rules continue.**
- Printed first: (m) 125/400 T1 rows with V ever absent (H26's at-risk 24, literal 111; prior expiry 112); (w) 116/400 W1 rows with no B whiff on 0-58. (e) D-driven nav events: T1D Agent16 223 of 4480 (E2 136, E1 45, E1b 3, E3 39, E4 0) against Agent15's 1492 of 5087; W1D Agent16 2935 of 4496 (E2 1484, E1 296, E1b 6, E3 1149, E4 0) against Agent15's 6392 of 6643; in the 116 (w) rows 1647 of 1769 (E3 859). N1 (Agent15's law steers on a V or B whiff, Agent16 does not): T1D 24 (step, row) in 9 rows; W1D 369 in 118 rows.
- (a) identities all True; (b) the burst record equal to brute force on five schedules (D stream 180 bursts of 7104 whiffs = 0.0253 [0.0219, 0.0293], beside the design's 0.0282; plume-like p 0.30: 351/400 rows burst); (c) the ranked top set, keep and nav exact on 2560 constructed rows; H27's (b3), (c), (d) True on the new seeds.
- (h) T1D DP Agent16 D on - D off -0.0150 [-0.0300, -0.0025]; M2(b) pass probability 0.9987 -> continue. (hW) W1D lost 228 against 400 (Agent15 D on), DP -0.4300 [-0.4775, -0.3800]; M5(a') pass probability 1.0000 -> continue.

**Development run (seeds 9907/9917, experiments/h28/ph33_dev.txt sha256 e49edf3d3313e4db8ca3934bde08e2b7466f2072864f7a78dc08f52dec9a3c5f, record:h28-dev-run):** no operation error, no amendment ('amendments: none'). (Its printout read every criterion PASS; that printout is not the verdict.) The evaluation seeds were unused until the one evaluation.

## 3. Results, one evaluation (seeds 2093 / 2197)

**T1 / T1D, the H21 choice task (dwell majority).**

| arm | agent | values | V | N | tie | P(V) [95%] | lost rows |
|---|---|---|---|---|---|---|---|
| burst tie, D on (main) | Agent16 | +1/0/0 | 366 | 28 | 6 | 0.915 [0.884, 0.939] | 18 |
| burst tie, D off | Agent16 (== Agent15 D off, == Agent14N2 in outcome) | +1/0/0 | 377 | 22 | 1 | 0.943 [0.915, 0.961] | 0 |
| H27's agent, D on (floor) | Agent15 | +1/0/0 | 317 | 69 | 14 | 0.792 [0.750, 0.829] | 83 |
| adopted, two channels | Agent14N2 | +1/0 | 377 | 22 | 1 | 0.943 [0.915, 0.961] | 0 |
| filter off, D on | Agent15g | +1/0/0 | 187 | 177 | 36 | 0.468 [0.419, 0.516] | 400 |
| hold not read, D on | Agent16, hh = read argmax | +1/0/0 | 366 | 28 | 6 | 0.915 (== Agent16 D on) | 18 |
| neutral with D (reported) | Agent16 | 0/0/0 | 204 | 186 | 10 | 0.510 | 125 |
| neutral (M1) | Agent14N2 | 0/0 | 191 | 203 | 6 | side balance 0.467 | 4 |
| pathway-off (M1) | Agent8 G 0, gate off, filter off | +1/0 | 190 | 200 | 10 | P(V \| chose) 0.487 | 5 |
| known-answer (M1) | Agent5 fixed valued | +1/0 | 382 | 16 | 2 | 0.955 [0.930, 0.971] | 6 |

Where the value goes: Agent16 D on against D off, into V 0, out of V 11 (k = 11); T1 rows with V ever absent (Agent16 D off) 124; the rule acts in 117 T1D rows (first action step 59/59/60), and those rows are identical to Agent15 D on on every field before it (I6'). Paired: Agent16 D on - Agent15 D on +0.1225 [+0.0900, +0.1575] (M2(d), reported); Agent16 D on - Agent14N2 -0.0275 [-0.0450, -0.0125].

**W1 / W1D, the absent-odour world (valued column masked from step 0).**

| arm | agent | dwell within 3.0 of B, mean (quartiles) | reach | lost rows | wall contacts per row |
|---|---|---|---|---|---|
| burst tie, D on (main) | Agent16 | 13.957 (0 / 10 / 25) | 288/400 | 222 | 43.360 |
| H27's agent, D on (floor) | Agent15 | 4.537 (0 / 4 / 8) | 223/400 | 400 | 106.608 |
| burst tie, D off (ceiling) | Agent16 (== Agent15 D off == Agent14N2) | 23.657 (17 / 25 / 31) | 385/400 | 29 | 0.000 |
| hold not read, D on | Agent16, hh = read argmax | 13.957 (identical) | 288/400 | 222 | 43.360 |
| release off, D on | Agent16, release off | 13.957 (identical) | 288/400 | 222 | 43.360 |
| filter off, D on | Agent15g | 3.277 (0 / 0 / 7) | 182/400 | 400 | 117.080 |

Rows with no B whiff on steps 0-58 (the population design 2.4 names as out of reach of any statistic of the odours' own streams): 110; of them lost in Agent16 D on 89; lost rows of Agent16 D on outside them 133.

**T3a / T3aD (REPORTED).** Neutral dwell 100-599: Agent16 D on 0.220, Agent16 D off 13.193 (== Agent14N2), Agent15 D on 0.087, hold-not-read D on 0.220. The rule acts in 6 T3aD rows.

**T4, +1/-1 (World7; REPORTED, outside the verdict).** Agent14N2 +1/-1: V 373, N 20, tie 7, P(V) 0.932 [0.904, 0.953], flee violations 0. Agent16 D on +1/-1/0: V 296, N 59, tie 45, P(V) 0.740 [0.695, 0.781], lost rows 125, flee violations 0 of 6084; paired DP -0.1925 [-0.2350, -0.1500].

## 4. Criteria (registered bars only)

| criterion | measured | bar | result |
|---|---|---|---|
| M1(a) ties: neutral / pathway-off / known-answer | 6/400, 10/400, 2/400 | <= 0.20 each | PASS |
| M1(b) neutral side balance P(+y \| chose) | 184/394 = 0.467 [0.418, 0.516] | within [0.35, 0.65] | PASS |
| M1(c) floor, pathway-off P(V \| chose) | 190/390 = 0.487 [0.438, 0.537] | within [0.35, 0.65] | PASS |
| M1(d) ceiling, known-answer P(V) | 382/400 = 0.955 [0.930, 0.971] | lower bound >= 0.85 | PASS |
| M2(a) Agent16 D on P(V) | 366/400 = 0.915 [0.884, 0.939] | reported against 0.88 | reported (lower bound >= 0.88) |
| M2(b) DP P(V) Agent16 D on - Agent16 D off | -0.0275 [-0.0450, -0.0125] (printed -0.027 [-0.045, -0.012]) | lower bound >= -0.05 | PASS |
| M2(c) DP P(V) Agent16 D on - Agent15g D on | +0.448 [+0.397, +0.498] | lower bound >= +0.05 | PASS |
| M2(d) DP P(V) Agent16 D on - Agent15 D on | +0.1225 [+0.0900, +0.1575] | reported | reported |
| M3 identities (I1')-(I6') on the task seeds | all True | all True | PASS |
| M4 mechanism bench (re-run on the bench seeds) | PASS; its M4 line equal to ph33_bench.txt's | section 4 | PASS |
| M5(a') W1D lost-row DP Agent16 D on - Agent15 D on | -0.445 [-0.495, -0.397] (222 vs 400) | upper bound <= -0.20 | PASS |

Section 8: ties in Agent16 D on 0.015, D off 0.003 (unreadable above 0.20); no group under 50 rows. **H28 under the registered criteria: SHOWN** (M1, M2, M3, M4, M5(a') PASS).

**Identities (M3, all True):** (I1') Agent16's code at N 2 == Agent14N2 on every field in T1, W1, T3a at +1/0 and +1/-1; (I2') D on == D off on every field before each row's first D whiff (Agent16 and the hold-not-read arm, 400/400 in each world); (I3') Agent16 D off == Agent15 D off on every field and HR in T1, W1, T3a, == Agent14N2 on the trajectory fields in every row, the rule never acting without D; (I4') hold-not-read D off == Agent16 D off on the trajectory; (I5') the 276 T1 rows with V present on every step: D on == D off 276/276; (I6') Agent16 D on == Agent15 D on on every field before each row's first action (T1D 117 rows acting, W1D 315, T3aD 6; 400/400 each); no flee at +1/0/0; masked draws == the World7 twin; T3a construction.

## 5. Reported items (no bar in the verdict)

- **M2(a):** 0.915 [0.884, 0.939]; its lower bound is above 0.88 (reported, as H27 registered it).
- **H27's W1D bars against D off (design 2.4 predicted them to fail):** (a) reach 288/400 = 0.720 [0.674, 0.762] against 0.80, below; (b) paired dwell Agent16 D on - D off -9.700 [-10.880, -8.438] against bar_W -4.7 (bench D_off 23.3875), below; (c) wall contacts 43.360 per row against 0.10; (d) lost-row DP D on - D off +0.4825 [+0.4300, +0.5325] against +0.05, above. The rule recovers part of the W1D loss (222 against 400 lost; dwell 13.957 against 4.537), not the distractor-free level (29 lost, 23.657).
- **M6, the hold's benefit:** lost-row DP hold-not-read D on - Agent16 D on +0.0000 [+0.0000, +0.0000] (222 against 222). The hold-not-read arm equals Agent16 in outcome in T1D and W1D as well; the release-off arm loses the same 222 W1D rows. The hold's benefit under a distractor stays unmeasured, as in H27.
- **T3aD:** neutral dwell 0.220 against 13.193 without D; the rule leaves the constructed loss as H27 left it (0.087).
- **T4:** Agent16 at +1/-1/0 with D 0.740 against Agent14N2 0.932 at +1/-1 (DP -0.1925). At +1/-1/0 B is negative, so with V absent D is the lone top odour and the rule has no tie to act on.
- **Neutral with D (0/0/0):** ties 10, P(V | chose) 0.523, lost rows 125 (the rule acts in value ties; reported).

## 6. Predictions (design v2 section 10) against the observations

| prediction | observed | |
|---|---|---|
| bench identities (I1')-(I6') True | all True | met |
| bench (b) D burst fraction about 0.028 (+-0.004) | 0.0253 | met (low side) |
| bench (m) about 100-125, about 100 prior expiry | 125, 112 prior | met (top of the range) |
| bench (w) about 100 | 116 (eval 110) | NOT met as stated (higher) |
| T1D k about 4 to 8 | bench 6 net (7 out, 1 in); eval 11 (11 out, 0 in) | bench met; evaluation NOT met (above the range) |
| T1D DP about -0.01 to -0.02, P(V) about 0.90-0.91 | eval -0.0275, 0.915 | NOT met (a larger cost; P(V) just above the range because D off is 0.943) |
| W1D L about 110 to 245 | bench 228, eval 222 | met |
| W1D: the rows with no B whiff by step 58 captured as in H27 (about 97 lost) | eval 110 such rows, 89 of them lost; 133 lost rows outside them | NOT met in composition (fewer lost among them, more outside) |
| W1D reach, dwell, contacts between floor and ceiling | 288, 13.957, 43.360 between Agent15 and D off | met |
| H27's M5(d) fails (lost-row DP about +0.22 to +0.56) | +0.4825 | met |
| M6 near 0 | +0.0000 | met |

## 7. What is shown and what is not

- **Shown (registered):** ranking value ties by the recency of each odour's last burst removes most of the choice-task cost of a ubiquitous distractor and recovers a large part of the absent-odour world, without changing the adopted agent when D is absent. In T1D the cost against itself without D is 0.0275 of P(V) (11 rows out of V, none in), against H27's 0.1325; D-driven nav falls from 1492 to 223 events at the bench. In W1D 222 rows are lost against 400 for H27's agent; D-driven nav falls from 0.962 to 0.653 of nav events at the bench. Without D the rule never acts (I3', 0 (step, row)).
- **The distractor cost that remains, stated:** W1D still loses 222 rows against 29 without D, with 43.4 wall contacts per row. By path (bench (e), counts only), the residual W1D D-driven nav is mostly E2 (D read as held and in the ranked top set, 1484) and E3 (D the lone top odour, 1149), with E1 296 and E4 0. The design's floor argument (2.4) named the (w) rows; on the evaluation seeds 89 of the 110 (w) rows are lost and 133 lost rows lie outside them. This run attributes no path to those 133 rows (no diagnostic beyond the design's was run); no cause is established.
- **Not shown:** the hold's benefit under a distractor (M6 +0.0000; the hold-not-read arm takes the same path); a loss after tracking with D (T3aD 0.220 against 13.193); +1/-1/0 with D (T4 0.740 against 0.932; no tie arises there); the 110 W1D rows in which B is never sensed before the capture (inside record:distractor-capture-limit); other p_D; a continuous-background D; learning with a distractor; whether a fly ranks odours by bursts (no fly finding is cited).
- **Predictions missed, stated (section 6):** the evaluation's k (11 against 4-8) and DP (-0.0275 against -0.01 to -0.02), the bench's (w) (116 against about 100), and the composition of the W1D losses. None enters a bar.
- **Not tested:** section 11 of the design; the alternatives not taken at section 12 (the lone-odour burst gate (ii'), the held-last tie, a pair within 5 steps, p_D 0.01).

## 8. Provenance

- Design v2 FINAL doc da2c1c079a1766d3e (experiments/h28/h28_design_v2.md, sha256 b12137f684fb44d80f5a780fccfd1dc0f63669b5530d2a3eaf834b8df0316b8c); v1 DRAFT doc dc81dbd5005ca164c (sha256 135a28f2fddd09328f5f282055813e1756b8d5cbc91a7e160b3a274fa5936a51); decision:h28-open-design, decision:h28-open, decision:classification-rule-relaxed-burst-record-h28, decision:evidence-release-composition-rule-h28, decision:classification-rule-relaxed-presence-prior-h28.
- Code src/ph33.py sha256 f2a29722a398c81b7f73014d29c799a08c289eca1cc7366acd65e50154e720b0 (demo, bench, dev, eval; source doc dd7262b0c91dbc66b, content_hash equal). Imported unchanged: ph32.py d9f585d5...2743 and, through it, ph2, ph11, ph14, ph15, ph16, ph17, ph22, ph23 (ae180492), ph24 (f344f178), ph25, ph28 (64ce7d0c), ph30 (98822834), sha256 in every output header.
- Outputs (LF): ph33_demo.txt 370839e0b0046c25652c7b34e0a2a4c31e9f250da0f1e3287e2438c9751f8c2f; ph33_bench.txt 45b0f2630598f92a0770f08bff51d044cfc8a46aff4f1017dcb5602213178671 (record:h28-bench-result); ph33_dev.txt e49edf3d3313e4db8ca3934bde08e2b7466f2072864f7a78dc08f52dec9a3c5f (record:h28-dev-run); ph33_eval.txt 43e3a99920016f665f5c8343914ebc55eaf55fdd3c1f893787f5c45591ed3dbe (record:h28-result). The outputs are committed beside this report and are not reproduced in it.
- Seeds: development 9907/9917, evaluation 2093/2197 (now spent), bench 20261131/20261132, bootstrap 20261133; the seed self-check clean in every run (224 files), with the pair of decision:seed-scan-exclusion-ph31-eval excluded by reference. Python 3.11.15, numpy 2.4.6.
- Closure, and any adoption, are the owner's.
