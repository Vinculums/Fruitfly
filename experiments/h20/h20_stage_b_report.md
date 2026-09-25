# H20 Stage B report: a learned positive value in the adopted agent (Agent14), the H21 choice task

Date 2026-09-25. Design v2 FINAL doc d3f2ce9707790cd87 (confirmed by the owner 2026-09-25, decision:h20-stage-b-open, '권고안 적용', gloss 'apply the recommended options'; sha256 28c1010f29978b0389106e6b6a0d02a91ed3eb5b9c95be86557a723e30b966ae, equal to the local file's sha256). Code src/ph29.py sha256 122c19250ea5d67d0dbd997fa20493c63c6c1101faff83d3cc6b3e907d4c799c (source doc dbcf264395e76d71a, content_hash equal; the demo, bench, development run and evaluation all ran on this version). One evaluation, world seed 2005, agent seed 2107, 400 rows x 600 steps, G 2, gate on where G 2, geometry C0, Agent14 (P 60, N_hi 300), training H15 E2 (neutral 30 steps, 50 silent steps, valued 30 reinforced steps), 95 percent intervals, bootstrap 5000 seed 20261083, no extension. Evaluation output experiments/h20/ph29_eval.txt sha256 a507a3decb43ba260c93c395bd06cd69a3a64abd3766b9973ac9bc8685c90c62. Nothing was changed after the table.

**Status: H20 Stage B SHOWN under its registered criteria: ML readable (30/400 trained rows failing against the bound 40, no sham row failing); M1, M2, M3, M4, M6 all PASS; M5 (W1) and M7 (T3a) reported, not part of the PASS condition.** The printout's summary label is the registered verdict sentence: a positive value learned by the agent's own learning module under a fixed reward training (the neutral odour presented equally often without reinforcement; learning frozen in the test) is carried by the adopted agent (Agent14) into the choice of source in the H21 task: within 0.05 of the supplied value on the same rows (DP learned - supplied 0.000 [0.000, 0.000]), at least 0.20 above a sham-trained agent (+0.467 [+0.415, +0.522]), at least 0.70 in every cell (lower bounds 0.838, 0.826, 0.888, 0.863), and with the filter's gain over the gate agent (+0.367 [+0.318, +0.417]). A statement about this training dose (saturating), this protocol and order (neutral first), this code set, G 2, C0, the dwell majority, learning frozen in the test. **Not about learning during behaviour (Stage C), negative values, a sub-saturating learned value, or other codes.** Closure is the owner's.

## 1. What was asked

H20 Stage B (design v2 section 1): when the positive value of one odour is LEARNED by the agent's own learning module (a fixed reward training, learning frozen during the test) instead of supplied, does the adopted agent Agent14 choose the source of that odour over a source whose odour was presented equally often without reinforcement, as it does with the supplied value? The value enters through a read-out written into `known` (candidate A), the array Agent14 already reads; no module is edited. The owner confirmed every recommended option of design v1 section 12 (the read-out into `known`; H15 E2 training with the neutral odour first in a fixed order; the check ML with a sign clause; bars M2(a) -0.05 vs supplied, (b) +0.20 vs sham, (c) cells 0.70, (d) +0.05 vs learned Agent10g, the 0.88 line reported only; stop rules (h) and (hL); T1 main, W1 and T3a reported, +1/-1 excluded; the seeds; no sub-saturating arm; then the Stage C design). No relaxation and no bar re-sign was registered (design section 3.8: no new state).

## 2. Implementation, self-checks, bench, development run

ph29.py composes the run from adopted and earlier modules without editing any of them (ph4, ph8, ph11, ph14, ph15, ph17, ph21, ph22, ph23, ph24, ph25, ph25b, ph28 imported unchanged; sha256 in every output header). The training function applies the H15 E2 protocol to the agent's own module a.mb with its own codes, reads the values with the agent's own chan_valence() with `known` None (ph14.py:55), writes them into `known` and clears the traces (ph15.py:160). Run-time hooks on ph24.make, ph23.make, the name Agent5 in ph24 and ph24.record apply the training right after construction and before the cast draw, and check at steps 0, 299 and 599 that the module is frozen. Readings R1-R13 where the design is silent are stated in the file header and printed in the bench output (e.g. R1, the valued channel taken from the harness's +1/0 array; R3, what an 'identical trajectory' is; R5, how the masks are recomputed; R9, the exactness claims of (t)).

**Self-checks (demo, experiments/h20/ph29_demo.txt sha256 abe5150668b8742dc209c7a5d01cf13db9a6027cf367bb9ecb8be19837f0e937):** every check ok: with no training mode the hooks leave every field of ph28.run, ph28.stub and ph23.run bitwise equal for Agent14, Agent10, Agent10g, Agent8, Agent6 and the fixed-hold Agent5; train() equals a direct MB4 run of the protocol read by ph15.valences; the hook trains on the run's own balance and the module stays frozen; sham == 0/0; learned with `known` := +1/0 == supplied; the known-answer arm with learned values == +1/0; the masks are order-only and the mask check detects a -1e-6 neutral value; the pass-probability arithmetic reproduces the design's section 7 table; the seed scan (15 numbers, 190 files, no hit). **Implementation errors: none.** Before the recorded demo, the demo was run once (code-path test) and a scratch script ran the bench and main code paths once on the unregistered demo seeds 5/6 (and 7/8 in place of the reproduction seeds) to catch crashes; those numbers are not used anywhere. The only change after them was the print precision of the value counts (7 to 15 significant digits), stated in the demo header.

**Mechanism bench (M4), experiments/h20/ph29_bench.txt sha256 6377148393e9845d2276aea6bee749c09022171d43c45252ed0b6309867d2137, record:h20-stage-b-bench-result: PASS; both stop rules continue.**
- (t) The learned values, as read from the code: v_V = 1.0 exactly in 400/400 trained rows; v_N > 0 in 400/400 (about +7.13e-6 in the 218 rows whose two codes share no unit, +0.1000064 in the 152 sharing one, +0.2000057 in the 29 sharing two, +0.3000050 in the one sharing three); sham exactly 0.0; compartments 0, 2, 3 unchanged. The units shared per row (u 218 / 152 / 29 / 1) are a fixed property of the code set (the same on the bench, development and evaluation seeds). ML: 30 trained rows fail (the u >= 2 rows, v_N > 0.15), 0 sham rows -> readable; (hL) continue. Printed beside, not used: trained in the opposite order (valued first) v_N = -2.76e-6 in all 218 u = 0 rows, as design 3.4 inferred.
- (i) Identities, all True: (i1) training changes only `mb.w` (and the read-out in `known`), 86 state entries including the generator state; (i2) learned with `known` := +1/0 == supplied Agent14 on every field (three stubs and World7 T1); (i3) counter and release fields equal in all 281 trajectory-identical rows; (i4) sham == Agent14 0/0 == Agent10 0/0; (i5) pathway-off and known-answer with the learned values == with +1/0; (i6) frozen in every trained or sham arm; (i7) gate, top, keep, H19 (a) and flee masks equal to +1/0's on every (row, step); (i8) the harness reproduces H26's T1 on 1985/2085 row for row (371/28/1 and the four cells).
- (g) (g1) masks order-only at v_N 7.1e-6, 0.1, 0.2 and the learned values (8 of 8 constructed states, 400/400 rows). (g2) one neutral whiff from rest: gain 1.0 peak 0.756 of threshold (H20's value reproduced), no row holds; **gain 1.2 peak 1.975 and gain 1.4 peak 1.992, every row holds**; with the learned values 182/400 rows hold (all u >= 1 rows, no u = 0 row). (g3) neutral-hold start, 800 rows: holding the valued odour at 600 88/800 learned and supplied, DP 0.0000.
- (h) T1 on bench seeds: learned 381/16/3 = supplied 381/16/3 (0.953); DP 0.0000 [0.0000, 0.0000]; no row changed its outcome although 119 rows (all u >= 1) departed in trajectory (first departure 10/21/220); M2(a) pass probability 1.0000 -> continue. Sham 0.468, learned Agent10g 0.568, pathway-off 0.470, known-answer 0.958, Agent10 0.960.

**Development run (seeds 9983/9989, experiments/h20/ph29_dev.txt sha256 a0a4d2b766656c9c60d33fea75c50ae59c0d5458f6a7d0db52ba209ed04bca10, record:h20-stage-b-dev-run):** no operation error, no amendment ('amendments: none'); the code unchanged. (Its printout read every criterion PASS: learned 368/31/1 == supplied, DP 0.000; learned - sham +0.405; cells 87/93/97/91; vs learned Agent10g +0.325. That printout is not the verdict.) The evaluation seeds were unused until the one evaluation. The dev and evaluation outputs each re-run the bench for M4 (reading R12); every bench line they print equals the bench output.

## 3. Results, one evaluation (seeds 2005 / 2107)

**The learned values on the evaluation balance (printed before the task).** u 218 / 152 / 29 / 1 (per cell 56/36/8/0, 56/36/7/1, 57/36/7/0, 49/44/7/0); trained v_V = 1 in 400/400; v_N as on the bench (7.13e-6, 0.1000064, 0.2000057, 0.3000050 by u); sham 0 in 400/400. ML: 30 trained rows failing (by cell 8/8/7/7), 0 sham -> readable; the failing rows are kept in every arm as assigned.

**T1, the H21 choice task (dwell majority).**

| arm | agent | values | V | N | tie | P(V) [95%] | P(V \| first hold valued) | P(V \| first hold neutral) |
|---|---|---|---|---|---|---|---|---|
| learned (main) | Agent14 | trained, read out, frozen | 369 | 30 | 1 | 0.922 [0.892, 0.945] | 234/239 | 135/161 |
| supplied | Agent14 | +1/0 | 369 | 30 | 1 | 0.922 [0.892, 0.945] | 251/256 | 118/144 |
| sham | Agent14 | sham-trained (0/0 exactly) | 182 | 214 | 4 | 0.455 [0.407, 0.504] | 128/180 | 53/218 |
| release-maintain, learned | Agent10g | trained | 222 | 174 | 4 | 0.555 [0.506, 0.603] | 171/230 | 51/170 |
| pathway-off | Agent8 G 0, gate off, filter off | trained | 179 | 213 | 8 | 0.448 (floor: P(V \| chose) 0.457) | 138/180 | 40/218 |
| known-answer | Agent5 fixed valued, G 0 | +1/0 | 383 | 15 | 2 | 0.958 [0.933, 0.973] | 383/400 | - |
| base | Agent10 | +1/0 | 377 | 21 | 2 | 0.943 [0.915, 0.961] | 250/255 | 127/145 |

Cells, learned: 91/100, 90/100, 95/100, 93/100 (supplied identical). Paired: **learned - supplied 0.000 [0.000, 0.000]** (into V 0, out of V 0; no row changed its outcome class); learned - sham +0.467 [+0.415, +0.522]; learned Agent14 - learned Agent10g +0.367 [+0.318, +0.417]; learned - Agent10 -0.0200 [-0.0375, -0.0050] (reported). Where the learned value differs from the supplied one: 283 rows keep an identical trajectory (u = 0: 218/218; u = 1: 55/152; u = 2: 10/29; u = 3: 0/1), 117 rows depart (all u >= 1; first departure 9/19/214), and none of them changes its majority. The learned arm forms its first hold on the neutral odour more often (161 rows against 144), consistent with bench (g2), and still ends at the valued source in the same rows. Over the 370 ML-passing rows the learned P(V) is 340/370 = 0.919 [0.887, 0.943]; the 30 failing rows end V in 29 (supplied 29). The 0.88 line (reported, not a bar): lower bound 0.892, P(k >= 365 of 400) at 0.922 = 0.8022. Lost rows (no whiff in the last third) 0 in the learned and supplied arms; wall contacts 0.

**T2, W1 (the valued column masked from step 0; REPORTED).**

| arm | agent | dwell within 3.0 of the present source, mean (quartiles) | reach | lost rows | first surge (quartiles; rows) |
|---|---|---|---|---|---|
| learned | Agent14 | 23.215 (17.0 / 25.0 / 31.0) | 387/400 | 31 | 115 / 139 / 153; 388 |
| supplied | Agent14 | 23.215 (identical row for row) | 387/400 | 31 | 115 / 139 / 153; 388 |
| sham | Agent14 (0/0) | 24.233 (19.0 / 25.0 / 29.0) | 395/400 | 30 | 4 / 13 / 110; 397 |
| maintain | Agent6 | 24.233 (== sham row for row) | 395/400 | 30 | 4 / 13 / 110; 397 |

Paired dwell learned - supplied 0.000; learned - Agent6 -1.018 [-2.070, +0.013]. First surge = the first B whiff at or after step 59 in 400/400 learned rows. Masked draws equal the World7 twin in every arm.

**T3a, lost at the valued source from step 0 (constructed; REPORTED).** Neutral dwell 100-599: learned 13.512 = supplied 13.512 (identical row for row), floor Agent10 0.708, ceiling Agent5 fixed neutral 13.680; span 12.973 [12.015, 13.902]; **R learned 0.9871 [0.9170, 1.0602]** (= supplied). Construction checked in every arm.

## 4. Criteria (registered bars only)

| criterion | measured | bar | result |
|---|---|---|---|
| ML learned-value check | trained failing 30/400; sham failing 0/400 | at most 40; none | readable |
| M1(a) ties: sham / pathway-off / known-answer | 4/400, 8/400, 2/400 | <= 0.20 each | PASS |
| M1(b) sham side balance P(+y \| chose) | 200/396 = 0.505 [0.456, 0.554] | within [0.35, 0.65] | PASS |
| M1(c) floor, pathway-off P(V \| chose) | 179/392 = 0.457 [0.408, 0.506] | within [0.35, 0.65] | PASS |
| M1(d) ceiling, known-answer P(V) | 383/400 = 0.958 [0.933, 0.973] | lower bound >= 0.85 | PASS |
| M2(a) DP learned - supplied | 0.000 [0.000, 0.000] | lower bound >= -0.05 | PASS |
| M2(b) DP learned - sham | +0.467 [+0.415, +0.522] | lower bound >= +0.20 | PASS |
| M2(c) cells, learned P(V) | 91, 90, 95, 93 of 100 (lower bounds 0.838, 0.826, 0.888, 0.863) | each lower bound >= 0.70 | PASS |
| M2(d) DP learned Agent14 - learned Agent10g | +0.367 [+0.318, +0.417] | lower bound >= +0.05 | PASS |
| M3 identities (i2), (i4), (i5) x2, (i6), (i7) on the evaluation seeds | all True | all True | PASS |
| M4 mechanism bench (re-run on bench seeds) | identities and exactness claims True; (h) 1.0000, (hL) 30/40 | identities; continue | PASS |
| M6(a) T1 lost rows DP learned - supplied | 0.000 [0.000, 0.000] | upper bound <= +0.05 | PASS |
| M6(b) T1 wall contacts per row | 0.000 | <= 0.10 | PASS |
| M5 W1, M7 T3a | section 3 | reported | - |
| 0.88 line (reported, not a bar) | 0.922 [0.892, 0.945]; P 0.8022 | - | - |

Ties in the learned, supplied and sham arms (section 8): 0.003, 0.003, 0.010. No cell under 50 rows. **H20 Stage B under the registered criteria: SHOWN** (ML readable; M1, M2, M3, M4, M6 PASS).

**Identities (M3, all True):** (i2) the learned agent with `known` overwritten by +1/0 == the supplied Agent14 on every field (T1); (i4) sham == Agent14 at 0/0 (every field) == Agent10 at 0/0; (i5) pathway-off with the learned values == with +1/0; known-answer with the learned values == with +1/0; (i6) the module frozen in every trained or sham arm (T1, W1, T3a); (i7) gate, top, keep, H19 (a) and flee masks with the learned values == with +1/0 on every (row, step) of the learned T1 run (400/400 rows each). Reported beside M3: masked draws == the World7 twin (W1, T3a) and the T3a construction in every arm: True.

## 5. Predictions (design v2 section 10) against the observations

| prediction | observed | |
|---|---|---|
| bench (t): v_V 1.0 in 400/400, v_N > 0, about +7.1e-6 at u 0, about +0.1000064 at u 1, sham 0; valued-first negative at u 0 | 1.0; > 0; 7.13e-6; 0.1000064; 0; -2.76e-6 | met |
| u counts about 237 / 131 / 29 / 4; ML failures about 33 | 218 / 152 / 29 / 1; 30 | counts differ (a fixed property of the code set); ML met |
| bench identities all True; (g1) 400/400; (g2) 0.756 at gain 1.0, not predicted at 1.2 and 1.4 | all True; 400/400; 0.756; every row holds at 1.2 and 1.4 | met (1.2 and 1.4 not predicted) |
| T1 learned - supplied 0 to -0.0125 (k 0 to 5) | 0.000 (k 0), bench and evaluation | met |
| most u = 0 rows identical in trajectory, departures mostly in u >= 1 rows | 218/218 u = 0 rows identical; all 117 departures u >= 1 | met |
| supplied Agent14 0.925 to 0.955 | 0.922 | NOT met (just below) |
| sham 0.50 to 0.55, side balance near 0.5 | 0.455; 0.505 | P(V) NOT met (below); balance met |
| pathway-off near 0.53 (P(V \| chose) 0.5 to 0.55) | 0.448 (0.457) | NOT met (below) |
| known-answer 0.94 to 0.95 | 0.958 | NOT met (just above) |
| learned Agent10g 0.60 to 0.65 | 0.555 | NOT met (below) |
| Agent10 0.93 to 0.96; lost rows 0 to 2; contacts 0 | 0.943; 0; 0 | met |
| W1 learned dwell within about 1 of supplied; first surge at the first B whiff at or after 59 in every row | identical row for row; 400/400 | met |
| T3a R within about 0.05 of supplied | identical (0.9871) | met |

None of the missed predictions enters a bar. The sham and pathway-off arms (both carrying no usable value) fell below 0.5 on the evaluation seeds (0.455, 0.448), with the side balance at 0.505; their bars (M1) are two-sided and passed.

## 6. What the run does not show

- **Learning during behaviour.** Learning was on only in an off-world training and frozen in the test; nothing is learned while the agent chooses. That is **Stage C** (integration: learning on in the H15 Run 2 world, reinforcement delivered at the sources, natural visits, both signs, with H15 Run 2's avoidance and long-horizon search values as the reference), which needs the release's negative scope decided first (decision:release-negative-scope-on-hold).
- **Negative learned values.** No punished training was registered; +1/-1 was excluded; the release stays ON HOLD at negative values.
- **A sub-saturating learned value.** At the registered (saturating) dose the valued value is exactly +1.0, the supplied number; the learned and supplied arms differ only by the neutral odour's small positive residual. The result is therefore close to an identity test of the chain training -> read-out -> `known` -> pathway, plus a measurement that the residual (a neutral gain up to x 1.6, which makes a single neutral whiff form a hold in every row whose codes share a unit) moved trajectories in 117 rows and no outcome. A dose-response is a separate question.
- **Other codes, the opposite training order** (on the bench, valued-first gives the neutral odour a negative value in 218/400 rows, which would put Agent14 in the +1/-1 regime), other G, geometries, starts, P or N_hi, a loss after tracking, any distractor condition, or whether a fly learns this way (no fly finding is cited).

## 7. Record-keeping, stated

The graph server acknowledged and persisted every write made before this report on the first attempt; each write was read back. The design v2 FINAL doc and the source doc were read back in full and equal the files byte for byte. record:h20-stage-b-bench-result was first written with a props key the graph does not use (subject_path); it was re-sent the same session with `code` and `source_doc` per decision:code-citation-convention. The code that ran is identified by the sha256 printed in each output header.

Closure, and any adoption, are the owner's. Next in the project order (design v3; decision:h20-stage-b-open point 9): the Stage C design.
