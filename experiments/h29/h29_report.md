# H29 report: the H26 T3b limit (a loss after tracking), the presence window after a whiff shortened to 200 steps

Date 2026-09-26. Design v2 FINAL doc d724287aa203d256d (confirmed by the owner 2026-09-26, decision:h29-open, '(i) 권고안대로 진행', gloss 'branch (i), proceed as recommended': branch (i) of the T3b diagnosis, every recommended option of design v1 section 12 except point 1, which the diagnosis resolved, plus a REPORTED cast-phase sensitivity condition; hash 552e2ee17df346a4e8eb9fd06525eabd51db2a8d88040d6e44d632700fa56aa7, equal to the local file's sha256). Signed before code: decision:classification-rule-relaxed-presence-prior-h29. Code src/ph35.py sha256 e4a3ceda25628e7026a64861ad51f84974f1e2a720794276df706d006a52b1b1 (source doc d7ed06b1bd4bb0e2c, content_hash equal), the same file for the demo, bench, development run and evaluation. One evaluation, world seed 2111, agent seed 2221, 400 rows x 600 steps, supplied +1/0, G 2, gate on, C0, learning off, t0 150; bootstrap seed 20261143, 95 percent.

**Status: H29 SHOWN under its registered criteria: M1, M2 (b, c), M3, M4, M6 and M8 (a, b) all PASS.** The printout's summary label is the registered verdict sentence: with the presence window after a whiff shortened from 300 to 200 steps and the 59-step prior unchanged, the adopted agent keeps its choice in the H21 task within 0.05 of itself with the 300-step window (DP -0.0075 [-0.0200, +0.0025]), is unchanged in the absent-odour world and after a loss from step 0 (identities), and after the valued odour is lost following tracking opens the filter exactly 200 steps after the last valued whiff (376/376) and dwells longer at the neutral source late in the run than the adopted agent on the same rows (+1.9525 [+1.4549, +2.4501]). It is a trade within the registered bars, not a separation of loss from tracking (design 2.5). Closure, and any adoption, are the owner's.

## 1. What was asked

H29 (design v2 section 1): the adopted agent Agent14N2 with its presence window after a whiff shortened from 300 to 200 steps, the 59-step prior unchanged (Agent17), (i) keeps its choice in the H21 task within an allowed gap of the adopted agent [M2(b)], and (ii) after the valued odour is lost following tracking (the Lost world T3b, mask from t0 150) opens the filter exactly 200 steps after the last valued whiff [M8(a)] and recovers more late neutral dwell than the adopted agent on the same rows [M8(b)]. In W1 and T3a it is the adopted agent by code (M3). By the construction of T3b no rule on the agent's own state can shorten the window after a loss without shortening it in the T1 silence the row shares with its twin (design 2.5; F1 of the diagnosis, 400/400), so what is tested is a trade. The owner's confirmation added a stated sensitivity (the diagnosis's F2 finding: the effect depends on where the window's opening falls in the cast loop) and a REPORTED condition, T3b at t0 100 and t0 200, with no bar.

## 2. Implementation, self-checks, bench, development run

src/ph35.py defines Agent17 as a subclass of Agent14N2 with no body, built by a run-time hook through Agent14's existing constructor arguments (ph28.py:95-97) with P 60 and N_hi 200, so the counter starts at 140. ph28.py, ph30.py and ph34b.py are imported unchanged and checked at run time against the sha256 on record (True in every output header); Agent14N2 is built through ph34b's hook, the construction the T3b diagnosis validated against H26's own lines. No adopted file is edited. Readings R1-R13 where the design is silent are in the file header and printed in every output (for example R3: the exposure set (x) from Agent14N2's T1 run, a valued counter in [200, 300) after a valued whiff, the valued odour not held and a neutral whiff; R4: M8(b) over all 400 rows, PASS iff the bootstrap lower bound > 0, FAIL iff the upper bound <= 0).

**Self-checks (demo, experiments/h29/ph35_demo.txt sha256 5699f256a838514238a68f34ba724e3982729a81eb3020e59077d2e93b849d7b):** 12/12 ok on the demo seeds: seed scan clean (18 numbers, 235 files); the imported files as on record; this file's hook leaves every recorded field unchanged for Agent10, Agent10g, Agent6, Agent11 and Agent14N2; construction (Agent17: P 60, N_hi 200, counter 140; Agent14N2: 60, 300, 240; Agent17's class body empty); identities (I1)-(I6) and the reported t0 construction; the counter convention; the pass-probability arithmetic reproduces design section 7 (M2(b) at k 5/8/10/12/13/15 = 1.000/0.990/0.893/0.650/0.506/0.260; the M8(b) table). Fixed before the recorded demo: none (one unrecorded trial run of the same code on the demo seeds, all ok).

**Mechanism bench (M4), experiments/h29/ph35_bench.txt sha256 e217dd00e3d5ab19b65808184f6504ae377c37f0266a5980c092536db5aed0a0, record:h29-bench-result: PASS; both stop rules continue.**
- Printed first: (m) H26's at-risk rows in Agent14N2's T1 run 20 (literal 123). (x) the exposure set 16 rows, first exposure step 285/414/457, silence age there 209/227/253; the 16 departing rows are exactly the (x) rows and each departs at its first exposure step. (t) T3b, 380 eligible rows: the first neutral whiff at or after L + W comes at L + 173/182/208 for W 60 and 150 (none 83), 212/233/242 for W 200 (none 89), 448/474/479 for W 250 (none 179), 471/475/480 for W 300 (none 180); at L + 200, 332 of 380 agents are in the neutral cone's along range just outside its width; at L + 300, 375/380 = 0.987 are upwind of both sources.
- (a) identities all True ((I1) Agent17 built with N_hi 300 == Agent14N2 on every recorded field in T1, W1, T3a, T3b, +1/-1; (I2), (I3) W1 and T3a identical with the valued counter exactly 100 lower; (I4) 384/384 and 16/16; (I5) 400/400; (I6) 0/0, +1/+1, +1/-1; (I7) held-only presence 0). (b) counter exact 400/400 = 1.000 [0.990, 1.000]. (f) the window exact at L + 200, 380/380 = 1.000 [0.990, 1.000]; T3a M7(a) 400/400.
- (h) T1 DP P(V) Agent17 - Agent14N2 +0.0025 [+0.0000, +0.0075] (into V 1, out of V 0); M2(b) pass probability 1.0000 -> continue. (hB) T3b paired neutral dwell +2.1350 [+1.6649, +2.6201], sd 5.0097; M8(b) pass probability 1.0000 -> continue.

**Development run (seeds 9903/9913, experiments/h29/ph35_dev.txt sha256 a70342bfd85c1954952f28d10108efadb5a2a096f211e5ea8a6de53ac313bf0c, record:h29-dev-run):** no operation error, no amendment ('amendments: none'). (Its printout read every criterion PASS; that printout is not the verdict.) The evaluation seeds were unused until the one evaluation.

## 3. Results, one evaluation (seeds 2111 / 2221)

**T1, the H21 choice task (dwell majority).**

| arm | agent | values | V | N | tie | P(V) [95%] | lost rows |
|---|---|---|---|---|---|---|---|
| shorter window (main) | Agent17 (N_hi 200) | +1/0 | 371 | 28 | 1 | 0.927 [0.898, 0.949] | 4 |
| adopted | Agent14N2 (N_hi 300) | +1/0 | 374 | 26 | 0 | 0.935 [0.906, 0.955] | 4 |
| filter off | Agent10g | +1/0 | 232 | 166 | 2 | 0.580 [0.531, 0.627] | 6 |
| neutral (M1) | Agent17 (== Agent14N2) | 0/0 | 191 | 205 | 4 | side balance 0.460 | 5 |
| pathway-off (M1) | Agent8 G 0, gate off, filter off | +1/0 | 188 | 206 | 6 | P(V \| chose) 0.477 | 6 |
| known-answer (M1) | Agent5 fixed valued | +1/0 | 383 | 16 | 1 | 0.958 [0.933, 0.973] | 2 |

Where the value goes: Agent17 against Agent14N2, into V 1, out of V 4 (k = 3); the exposure set (x) holds 19 rows (first exposure step 282/395/426), and the 19 departing rows are exactly these, each departing at its first exposure step; H26's at-risk rows 24 (literal 109).

**T3b, the Lost world (mask from t0 150; registered).**

| arm | agent | neutral dwell 400-599, mean (quartiles) | eligible | first neutral surge after L | none before 600 | window exact |
|---|---|---|---|---|---|---|
| shorter window (main) | Agent17 | 6.730 (1 / 6 / 10) | 376 | 215 / 235 / 242 | 78 | at L + 200: 376/376 |
| adopted | Agent14N2 | 4.777 (0 / 4 / 9) | 376 | 472 / 476 / 480 | 172 | at L + 300: 376/376 |
| fixed window 60 | Agent11 (N 60) | 5.772 (1 / 6 / 9) | 376 | 172 / 178 / 208 | 76 | at L + 60: 376/376 |
| never opens | Agent10 | 2.240 (0 / 0 / 3) | 391 | none | 391 | |
| filter off | Agent10g | 6.790 (3 / 7 / 10) | 288 | 171 / 176 / 193 | 31 | |
| H25's ceiling | Agent5 valued then neutral | 5.683 (1 / 5 / 9) | 388 | | | |

L (the last valued whiff before t0) 36/39/120 in Agent17 and Agent14N2; the valued hold ended 48 steps after its origin in all 155 rows holding it at t0. Paired Agent17 - Agent14N2: +1.9525 [+1.4549, +2.4501], sd 5.0646, rows gaining 178, losing 72, equal 150.

**W1 and T3a (identity worlds; H26's M5 and M7 quantities reported).** W1: Agent17 == Agent14N2 on every compared field (dwell 23.543, reach 383/400, lost rows 31, contacts 0.000, first surge == first neutral whiff at or after 59 in 400/400); Agent6 24.267, paired Agent17 - Agent6 -0.725 [-1.650, +0.223]; lost rows Agent6 18. T3a: identical (neutral dwell 100-599 13.720), M7(a) exact 400/400, R 0.9857 [0.9203, 1.0564] (floor Agent10 0.757, ceiling 13.908, span 13.150 [12.202, 14.090], readable).

**T4, +1/-1 (World7; REPORTED).** Agent17 and Agent14N2 identical: V 367, N 19, tie 14, P(V) 0.917 [0.886, 0.941], lost rows 42, contacts 0.365 per row.

## 4. Criteria (registered bars only)

| criterion | measured | bar | result |
|---|---|---|---|
| M1(a) ties: neutral / pathway-off / known-answer | 4/400, 6/400, 1/400 | <= 0.20 each | PASS |
| M1(b) neutral side balance P(+y \| chose) | 182/396 = 0.460 [0.411, 0.509] | within [0.35, 0.65] | PASS |
| M1(c) floor, pathway-off P(V \| chose) | 188/394 = 0.477 [0.428, 0.526] | within [0.35, 0.65] | PASS |
| M1(d) ceiling, known-answer P(V) | 383/400 = 0.958 [0.933, 0.973] | lower bound >= 0.85 | PASS |
| M2(a) Agent17 P(V) | 371/400 = 0.927 [0.898, 0.949] | reported against 0.88 | reported (lower bound >= 0.88) |
| M2(b) DP P(V) Agent17 - Agent14N2 | -0.0075 [-0.0200, +0.0025] (printed -0.008 [-0.020, 0.003]) | lower bound >= -0.05 | PASS |
| M2(c) DP P(V) Agent17 - Agent10g | +0.348 [+0.297, +0.397] | lower bound >= +0.05 | PASS |
| M3 identities (I1)-(I7) on the task seeds | all True | all True | PASS |
| M4 mechanism bench (re-run on the bench seeds) | PASS; its M4 line equal to ph35_bench.txt's | section 4 | PASS |
| M6(a) lost-row DP Agent17 - Agent14N2 | +0.000 [+0.000, +0.000] (4 vs 4) | upper bound <= +0.05 | PASS |
| M6(b) T1 wall contacts per row, Agent17 | 0.000 | <= 0.10 | PASS |
| M8(a) T3b window exact at L + 200 | 376/376 = 1.000 [0.990, 1.000] | lower bound >= 0.95 | PASS |
| M8(b) paired T3b dwell 400-599 Agent17 - Agent14N2 | +1.9525 [+1.4549, +2.4501] | lower bound > 0 | PASS |

Section 8: ties in Agent17 0.003, Agent14N2 0.000 (unreadable above 0.20); eligible T3b rows 376, no group under 50. **H29 under the registered criteria: SHOWN** (M1, M2, M3, M4, M6, M8 PASS).

**Identities (M3, all True):** (I1) Agent17 built with N_hi 300 == Agent14N2 on every recorded field in T1 and T3b; (I2) W1 and (I3) T3a == Agent14N2 on ph28.ALLK with the valued counter exactly 100 lower; (I4) T1: the departing rows are exactly the 19 exposure rows, each departing at its first exposure step; (I5) T3b == T1 on steps 0-149 and Agent17 == Agent14N2 before the first neutral whiff at or after L + 200 (400/400; 270 rows depart exactly there); (I6) 0/0, +1/-1, +1/+1; (I7) held-only presence 0; masked draws == the World7 twin; T3a construction; imported files as on record.

## 5. Reported items (no bar in the verdict)

- **M2(a):** 0.927 [0.898, 0.949]; its lower bound is above 0.88.
- **R_b and H25's R:** R_b = (D_17 - D_14N2) / (D_60 - D_14N2) = 1.9623 [1.3952, 3.4268] (D_60 5.772): the window of 200 recovered about twice the fixed-60 agent's advantage over the adopted agent. H25's R (floor Agent10 2.240, ceiling Agent5 valued then neutral 5.683, span 3.442 [2.870, 3.995], below the readability bound 5): Agent17 1.3043 [1.1058, 1.5468], Agent14N2 0.7371 [0.5893, 0.9028].
- **The phase-sensitivity condition (T3b at t0 100 and t0 200; design v2 section 5; no bar, no stop rule, outside the verdict):**

| t0 | eligible | L | t0 - L | L as at t0 150 | Agent17 dwell | Agent14N2 dwell | paired Agent17 - Agent14N2 | first surge after L: Agent17 (none) | Agent14N2 (none) |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 291 | 13/35/38 | 62/65/87 | 221 | 8.140 | 7.440 | +0.7000 [+0.2625, +1.1425] (gain 117, lose 82) | 235/242/280 (9) | 456/474/479 (25) |
| 150 (registered) | 376 | 36/39/120 | | | 6.730 | 4.777 | +1.9525 [+1.4549, +2.4501] (178, 72) | 215/235/242 (78) | 472/476/480 (172) |
| 200 | 376 | 118/133/189 | 11/67/82 | 207 | 5.553 | 1.735 | +3.8175 [+3.3400, +4.3050] (235, 21) | 213/232/239 (101) | 467/472/476 (322) |

  The window exact at L + 200 (Agent17) and at L + 300 (Agent14N2) in every eligible row at both t0, and (I5) True at both. What it shows, as a description and not a criterion: the paired interval lies above 0 at all three losses, and the size of the gain changes by a factor of about five between t0 100 and t0 200. In both agents the first neutral surge keeps its delay after L (Agent17 about L + 213 to 280, Agent14N2 about L + 456 to 480, the second downwind pass), so what t0 changes is where L falls in the run: at t0 100 L is 13/35/38 and the adopted agent's second-pass surge (about L + 470, near step 505) still falls inside the measurement window 400-599 (Agent14N2 dwell 7.440, none 25 of 291); at t0 200 L is 118/133/189 and that surge falls after step 599 for most rows (none 322 of 376, dwell 1.735), while Agent17's first-pass surge still comes at about L + 232. This is the cast-loop timing the stated sensitivity names, read on the same geometry and loop; it is not a test of the sensitivity at other geometries or cast parameters, and the t0 100 and 150 populations overlap by construction (221 of the 291 eligible rows at t0 100 have the same L as at t0 150, and those rows are the same trajectories).
- **W1 and T3a:** the adopted agent's own numbers by identity (section 3); paired W1 dwell Agent17 - Agent6 -0.725 [-1.650, +0.223]; W1 lost rows 31 against Agent6's 18 (the price of the 59-step prior, unchanged from the adopted agent).
- **T4:** identical to Agent14N2 at +1/-1 (0.917).

## 6. Predictions (design v2 section 10, unchanged from v1) against the observations

| prediction | observed | |
|---|---|---|
| bench identities True; (b), (f) exact | all True; 400/400, 380/380 | met |
| bench (m) about 15-25 rows | bench 20, eval 24 | met |
| bench (x) about 15-30 rows | bench 16, eval 19 | met |
| (t) a first neutral whiff at or after L + 200 and before L + 300 in a substantial share | window 200: 291 of 380 rows at 212/233/242 | met |
| T1 k about 5, range 0 to 10 | bench -1 (into 1, out 0); eval 3 (into 1, out 4) | bench NOT met as stated (below the range, on the favourable side); eval met |
| T1 DP about -0.0125, range 0 to -0.025 | bench +0.0025; eval -0.0075 | bench NOT met as stated (above 0); eval met |
| T3b gain m about +0.9, range +0.5 to +1.3 | bench +2.1350; eval +1.9525 | NOT met (above the range) |
| T3b gain bounded above by about Agent11 (N 60)'s advantage | eval advantage 0.995, gain 1.953 (R_b 1.96) | NOT met (the bound does not hold) |
| rows with no neutral surge before 600 fall from about 173 toward 81 | eval 172 -> 78 (Agent11 (N 60) 76) | met |
| Agent17's T3b dwell about 5.1-5.7 at the H26 evaluation's scale | eval 6.730 | NOT met (higher) |
| W1, T3a, T4 identical to Agent14N2 | identical | met |

The T3b misses were already visible in the T3b diagnosis on H26's bench seeds (gain +2.460, R_b 1.35; record:t3b-diagnosis-result); design v2 recorded them beside the unchanged predictions and they entered no bar.

## 7. What is shown and what is not

- **Shown (registered):** shortening the presence window after a whiff from 300 to 200 steps, with the prior unchanged, leaves the choice task within the allowed gap of the adopted agent (DP -0.0075 [-0.0200, +0.0025], 4 rows out and 1 into V, all of them among the 19 rows where the code lets the two agents differ) and, after a loss following tracking at t0 150, opens the filter exactly at L + 200 and raises late neutral dwell by 1.95 steps per row on the same rows. W1, T3a and +1/-1 are unchanged by code and by measurement.
- **What it is:** a trade, not a separation. The shorter window acts identically in the T1 silences that share their history with a loss (design 2.5; the diagnosis's F1 400/400); in T1 it steered on a neutral whiff in 19 of 400 rows here (16 at the bench, 29 on the development seeds).
- **The stated sensitivity, not resolved by this run:** the gain rests on the window opening inside the first downwind pass of the cast loop (the bench's (t): window 250 behaves like 300). The reported t0 condition shows the gain positive at three losses on the same loop and geometry, with its size set largely by where L falls relative to the measurement window; other geometries, cast parameters and windows between 200 and 250 are untested.
- **Not shown:** a rule that separates a loss from a tracking silence (excluded on the agent's own state by construction; a position record is outside the classification rule); windows other than 200; the burst- and count-conditioned windows (rejected in design 3.1); three channels and the distractor D (H28's condition; H28's closure is pending and untouched); learning; negative values beyond T4's report; cold start (H17); heading-cue loss (H18); whether a fly keeps such a window (no fly finding is cited).
- **Predictions missed, stated (section 6):** the T3b gain (1.95 against 0.5-1.3), the Agent11 bound, Agent17's dwell level, and the bench's T1 k and DP (outside the range on the favourable side). None enters a bar.
- **Not tested:** section 11 of the design; the alternatives not taken at section 12 (N_hi 250, M8(b) at a share, (hB) without a stop).

## 8. Provenance

- Design v2 FINAL doc d724287aa203d256d (experiments/h29/h29_design_v2.md, sha256 552e2ee17df346a4e8eb9fd06525eabd51db2a8d88040d6e44d632700fa56aa7); v1 DRAFT doc dd00688c21f09b13e (sha256 5078d814f51896067409125b59a8384a4dbe47f9a419ed7a48f6472de2a31260); the T3b diagnosis doc d8a7e386faf08075d (record:t3b-diagnosis-result); decision:h29-open-design, decision:t3b-diagnosis, decision:h29-open, decision:classification-rule-relaxed-presence-prior-h29.
- Code src/ph35.py sha256 e4a3ceda25628e7026a64861ad51f84974f1e2a720794276df706d006a52b1b1 (demo, bench, dev, eval; source doc d7ed06b1bd4bb0e2c, content_hash equal). Imported unchanged: ph28.py 64ce7d0c...e7aa, ph30.py 98822834...59bd, ph34b.py 1de70167...bf25 (checked at run time) and, through them, ph11, ph12, ph15, ph16, ph21, ph22, ph23, ph24, ph25, ph25b, sha256 in every output header.
- Outputs (LF): ph35_demo.txt 5699f256a838514238a68f34ba724e3982729a81eb3020e59077d2e93b849d7b; ph35_bench.txt e217dd00e3d5ab19b65808184f6504ae377c37f0266a5980c092536db5aed0a0 (record:h29-bench-result); ph35_dev.txt a70342bfd85c1954952f28d10108efadb5a2a096f211e5ea8a6de53ac313bf0c (record:h29-dev-run); ph35_eval.txt 1577b42c9982c53d717ba6a5b5061d17cb50fdaf26112115d1be00fd829c6e2e (record:h29-result). The outputs are committed beside this report and are not reproduced in it.
- Seeds: development 9903/9913, evaluation 2111/2221 (now spent), bench 20261141/20261142, bootstrap 20261143; the seed self-check clean in every run (235 files), with the pair of decision:seed-scan-exclusion-ph31-eval excluded by reference. Python 3.11.15, numpy 2.4.6.
- Closure, and any adoption, are the owner's.
