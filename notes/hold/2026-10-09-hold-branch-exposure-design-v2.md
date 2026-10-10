# (d) The hold's benefit: a condition that exposes a read-out branch in the adopted scope, design v2 FINAL

Date 2026-10-09. Status: **v2 FINAL, owner-confirmed before implementation and runs**. decision:hold-branch-exposure-d0-open.

Owner instruction, verbatim: '다음 권고안에 따라 작업 이어서진행한다.' (proceed with the recommended next work). The recommendations refer to both v1 section-12 lists reviewed in the preceding progress response.

## Confirmed choices and implementation readings

All eight RECOMMENDED options in v1 section 12 are confirmed. D0 precedes any new condition. W1Dp is a design candidate only. E1 requires a later opening after D0 and is not opened here. No constructed witnesses now. The exposure screen remains 40 of 400, lost rows in [20, 380].

Implementation readings fixed before the run: the W1Dp/W1N expectations are conditional on the recorded B2 sensing positions, with no random draws. Burst/tie expectations may be computed by an exact finite-state recursion for the two most recent whiffs. They are proxies, not probabilities for a freely running new world. The draft supplies no calibrated mapping to P(X3): report observed identity split with its denominator, null if no eligible observation, and a conservative bound P(at least 40 exposed rows) <= expected tied-single opportunities / 40, capped at 1. Do not invent an exposure probability when the identity split or changed-state distribution is unmeasured. A bound failure in section 3 is reported and stops the branch conclusion; an unresolved proxy does not authorize E1.

Runtime: local Python 3.13.12, numpy 2.5.3, one process and BLAS threads 1. The existing passive instrument, fly.py, ph chain and seed pins stay byte-pinned. D0 uses the spent evaluation aliases only; no new experimental seed is consumed.

## Preserved v1 specification

The v1 text below preserves the original proposal and alternatives for provenance. Its future-tense approval statements and section-12 alternatives are superseded by the confirmed choices above. No measured result is added to this FINAL.

# (d) The hold's benefit: a condition that exposes a read-out branch in the adopted scope, design v1 DRAFT

Date 2026-10-07. Status: **v1 DRAFT, for the owner's confirmation (section 12). A design, not a run: no code, no seed used, no world changed, nothing adopted.** Opened by decision:hold-branch-exposure-design-open, the owner's point 1 of the answer to the stage-one gates, verbatim '1. 열도록 한다. 2. 허용한다.' (gloss: '1. Open it. 2. Allow it.'); point 2 is decision:hold-stage2-coverage-proposal-allowed, the separate stage-two proposal on the coverage conditions (notes/hold/2026-10-07-hold-stage2-coverage-design-v1.md, drafted separately). Stage one: experiments/hold/hold_stage1_report.md (record:hold-stage1-replay-result) on design notes/hold/2026-10-07-hold-benefit-stage1-design-v1.md rev 2. Template: experiments/h29/h29_design_v1.md.

**The agent is not changed.** Two-channel form: Agent17 (src/ph35.py:104-105); three-channel form: Agent16 (src/ph33.py:180-194); src/fly.py is the reference within its eleven identity rows plus smoke only (experiments/module/module_report.md section 3, decision:fly-reference-implementation). H and R are stage one's: H reads the actual post-circuit hold `h = held()` (src/fly.py:308); R reads `q = argmax(y)` if `max(y) > 0.05`, else nothing, from the same step's gated `y` (src/ph33.py:134, rebuilt passively at src/hold_stage1_instrument.py:27-34); only the read-out expressions are projected, nothing R is written back.

Citations: code as path:line at HEAD 1ce9b22 (src/fly.py sha256 3b360b29...1efc4, the byte-pinned reference). "Stage one" is the replay report and experiments/hold/hold_stage1_replay.json (sha256 4c43fde6...7d94). Every claim is labelled **measured** (a recorded number and its source), **read** (a cited code line) or **inferred** (arithmetic or reasoning on read or measured quantities). Nothing was run for this draft except read-only arithmetic on the recorded replay file and hand formulas (Bernoulli and upstream-decay arithmetic, normal approximations), stated where used. No seed digit appears in this file; seeds are named by alias.

## 0. What is new

| item | stage one (measured) | this design | section |
|---|---|---|---|
| question | does an existing condition reach a branch | which change of CONDITION (agent unchanged) makes a branch reachable often enough that a later benefit trial is not structurally uninformative | 1 |
| two-channel +1/0, learning off | no command branch in 960 000 row-steps (A1-A4) | **verdict: no condition that keeps +1/0, learning off and the module constants reaches a branch, within the stated bound; the branches need a value change (the coverage conditions, decision:hold-stage2-coverage-proposal-allowed)** | 3 |
| three-channel +1/0/0 | tied-burst branch in code, 0 in 480 000 row-steps (B1, B2) | candidate condition **W1Dp**: W1D with D co-emitted from B's source by the read plume law (the same D stream, one uniform per row and step); the branch stays rare by the burst rule's construction | 4 |
| next step | | **D0, a passive recount on the recorded strata (spent seeds, no new condition) of the quantities the arithmetic lacks, before any new world is built** | 6, 12 |
| benefit | none scored | **none registered**; only an exposure screen (section 8) that decides whether a benefit trial could be informative | 8 |

## 1. The question

Within the adopted scope the read identity differs from the hold often (h != q on 48 675 to 110 782 of 240 000 row-steps per primary stratum) and no command differs (**measured**, stage one table). A benefit trial there compares two arms that issue the same commands at every step, so its result is fixed at zero by construction, as H27 and H28 found (M6 +0.0000, the hold-not-read arm on the same W1D paths; master_plan.md:741, :802, :1786). The question: **which change of world geometry, odour layout, value assignment within the forms' tested values, presence or prior condition, or horizon makes the unchanged agent reach a documented command branch between H and R, how often, and is that often enough to read a benefit at all?** This design decides only the last point's instrument and threshold. It registers no benefit measure.

## 2. The command branches of the read-out, enumerated

A command is the clipped turn before the common noise draw (src/fly.py:346). It is a function of `tgt` (:344-345) and the shared heading estimate (:310). `tgt` reads `nav` (:344), `since` (:340, itself from `nav`) and `val` (:345). So H and R can issue different commands only through `nav` or `val < 0` (**read**). `silence` (:341) reads `hit` and is latent (next step's release, :302); it is reported, not a command.

### 2.1 Two-channel form (src/fly.py:312-314, :324-328, :336-337)

- **Flee route.** `val` (:312) is the read identity's value; `tgt` is the flee side where `val < 0` (:345). Needs a negative value. Not at +1/0 (**read**). Reached at +1/-1: A5 43 504 flee differences (**measured**).
- **Tied-top route.** `top` (:328) holds every present non-negative channel at the maximum value; `keep` (:336) holds a read identity whose value equals `vmax`; `nav` (:337) is the read channel's whiff if kept, else any top whiff. With two channels at the same value, H keeping the non-whiffing member while R reads the other or nothing gives `nav` False against True. Needs equal values. Not at +1/0 (**read**). Reached at 0/0: A6 64 row-steps on 33 rows (**measured**).
- **Presence route.** `present = (c < N) | held` (:325-326), `held` set from the read identity. If H's override and R's override add different channels absent by counter, `vmax` and `top` can differ. At +1/0 it changes `nav` only when V (+1) is absent by counter and present in one projection only: that projection's top is {V}, `keep` on V gives `nav` = V's whiff (False, V unsensed for 200 steps), the other's top is {B}, `nav` = B's whiff (**read**, :327-328, :336-337).
- **Identity-independent otherwise.** With equal presence sets at +1/0: top is {V} if V present, else {B} if B present, else empty; every identity gives `nav` = the top channel's whiff, or False (**read**; the stage-one reading, point 1, which I reproduce and agree with).

### 2.2 Three-channel form (src/fly.py:315-322, :329-334)

The burst record is updated before ranking (:316-322: `burst = whiff & t - w2 <= 9`, `bb = t` where burst, then `w2`), so a burst completed on this step counts on this step (ph33 reading R3, **read**). `topr` (:330-332) is `top` if it holds one channel or none; if it holds two or more, the members whose `bb` equals the largest `bb` over `top`, and none if that largest is 'never'. `keep` (:333) is the read identity in `topr` (or a negative value); `nav` (:334) as at two channels with `topr`.

- **Flee and the vh < 0 clause of keep:** need a negative value; not at +1/0/0 (**read**). Reached at +1/-1/0: B3 10 319 command row-steps (**measured**).
- **Tied-burst route, the only value-preserving route at +1/0/0** (**read**, the exact state at step t, after :316-322):
  (T1) V absent by counter in both projections and read by neither (else the presence route); (T2) B and D present in both, so `top` = {B, D} (:328, both value 0); (T3) `bb_B == bb_D == max > NEVER` (:330-331): **their most recent bursts fell on the same step, and neither has burst since, including at t**; (T4) exactly one of B, D whiffs at t, and that whiff is not a burst (a burst would set its `bb` to t at :321 and leave it alone in `topr`); (T5) one projection reads the non-whiffing member and the other reads the whiffing member or nothing. Then one `nav` is False (kept, own whiff absent) and the other True. A single-member or empty `topr` makes `nav` identity-independent.
- **Presence route at three channels.** As at two channels, through :325-326; bounded in section 3.2.

### 2.3 Against the stage-one reading

I **agree** with points 1-4 of the report's 'Reading' section and with its counts. I would **amend** three statements (none changes a count or a permitted conclusion):

1. Point 1's bound counts only the timeout ('the hold times out at silence > 40 ... the gap at hold formation would have to exceed 160 steps'). `silence` is also zeroed by any release step (src/fly.py:306) and by a new hold (:290), and a timeout does not end the hold at once: N2 repeats the reset while the circuit holds (:286-290), and four consecutive reset steps release a hold where one does not (1.99 to 1.49, master_plan.md:81-84, **measured**, record:silence-timeout-chain-result); the release lands 48 steps after the last whiff (master_plan.md:648, **measured**). The gap needed is therefore about 200 - 48 = 152 steps, not 160, and the evidence-release reset must be bounded separately (section 3.1). The conclusion stands.
2. Point 1's 'within about a dozen steps' for R's route: from P = 1 the gated output falls below 0.05 after 12 steps for a zero-valued channel and 14 for V with the gain 3 (`P` halves per step at tau 2.0, src/fly.py:98; y = 1.8 g P / (0.05^1.5 + P + 0.8 others), :101; **inferred**). The conclusion stands.
3. Point 2's 'both burst-ranked (tied bursts)' should read 'their most recent bursts on the same step (`bb` equality at src/fly.py:331), with no later burst of either, and the one whiff at the exposure step not itself a burst (:320-321)'; and the statement holds given equal presence sets, which section 3.2 bounds. The report's gate text '(for the two-channel form this means a value or presence condition, not a world geometry ...)' would read 'a value condition; the presence route is reached only by a harness-written hold (section 5, R8)'.

## 3. The two-channel verdict, and the presence bound at three channels

### 3.1 Two-channel +1/0, learning off

Given section 2.1, a two-channel +1/0 branch needs the presence sets to differ with V present in one projection only. Two routes, each bounded from the constants and the record:

- **R's override.** R reads q only if y_q > 0.05 (src/ph33.py:134). That needs q sensed within the last 13 steps (V) or 11 (B) (**inferred**, 2.3 point 2), far below the window 200 (src/fly.py:56). R's override never adds a channel absent by counter.
- **H's override.** H holds h with `c_h >= 200`. `c_h` and `silence` both reset on a whiff of h (:313, :324, :341). Otherwise `silence` resets only at hold formation (:290) and at a release step (:306). (a) Formation needs input: below s = 1 the unit decays without y, because 2·sigmoid(12(s - 1)) < s there (:125-129). So `c_h` at formation is at most about 13 (**inferred**). (b) A timeout leads, under N2, to the release 48 steps after the last whiff (**measured**, above). (c) An evidence release cannot reset a V hold, because B is gated to 0 while V is held (:300) and so cannot exceed V's output (:222). It resets a B hold only on a V whiff, which makes V present by counter for 200 steps, so top = {V} in both projections and `nav` is identity-independent. Hence while h is held, `c_h <= ~13 + 48 = ~61` (**inferred**), against 200. **Measured check:** presence never differed in 960 000 row-steps (A1-A4). That includes T3a, where a V hold is constructed at step 0 on a counter of 140. It would cross the window at step 59, so every hold ended by step 58, inside the bound.
- **Verdict.** For Agent17 at +1/0, learning off and the module constants, in any world (any geometry, odour layout of the two channels, prior state reached by the agent itself, or horizon), H and R issue the same command at every step. The bound is the margin above (about 61 against 200, and 13 against 200 on R's side). The record checks it in four worlds; it rests on the circuit's measured release and has not been checked by constructed witnesses. **A two-channel +1/0 branch-exposing condition does not exist within this bound.** The only exception found is a hold written by the harness on a channel whose counter is already at 152 or more (section 5, R8), a constructed state rather than a condition. The two-channel branches need a value change: equal values (tied-top, A6) or a negative value (flee, A5). These are the coverage conditions of decision:hold-stage2-coverage-proposal-allowed. **Recommended accordingly (12, point 2).**

### 3.2 The presence route at three channels

At three channels the evidence release is against the strongest non-held channel (src/fly.py:218-222). With B held (vh 0) D is not gated (:300, `0 < 0` false), so a D whiff can zero a non-whiffing B hold's `silence` without a B whiff. Could D's whiffs then keep a B hold alive past `c_B >= 300`? From the upstream arithmetic, a single D whiff keeps y_D - y_B > 0.2 for about 9 consecutive steps while y_B ≈ 0 (y_D 1.76, 1.72, 1.65, 1.53, 1.33, 1.05, 0.74, 0.47, 0.27, then 0.15; **inferred**), and `evidence_due` is re-read every step from the held identity (:303). That is about nine consecutive reset steps, and four release a hold (**measured**, above). So the hold ends instead of surviving (**inferred**). A V hold gates B and D (:300) and is bounded as in 3.1. **Measured check:** presence never differed in 480 000 row-steps (B1, B2). The tied-burst route of 2.2 is therefore the only three-channel +1/0/0 branch the design can target. Where this inference could fail is listed in section 13.

## 4. Three-channel: conditions that make the tied-burst branch reachable

### 4.1 Why it is rare in W1D (inferred)

Define b(p) = p · P(at least 2 whiffs in the previous 9 steps | p) for a channel whiffing independently at p per step (the burst of src/fly.py:320). b(0.03) = 0.00084, matching D's 0.0282 per whiff (master_plan.md:1826, H28 design 2.3). b(0.0567), the plume at the task start (H28 design 2.3), = 0.0050. b(0.1) = 0.0225. b(0.27), near a source, = 0.201.

The route needs two things at once, with opposite rate demands. (T3) needs a **simultaneous** burst, which favours dense whiffs. The tie must then survive, and (T4) needs a single **non-burst** whiff before either channel bursts again, which favours sparse whiffs. After a burst, about 5 quiet steps of both channels are needed before a whiff can be a non-burst. That holds with probability (1-p)^10: 0.35 at p 0.1, 0.043 at p 0.27.

- In W1D, D is independent of position, so simultaneous bursts arrive at b_B(t) × 0.00084: 1.9e-5 per step at p_B 0.1. B delivered 8.9 whiffs per row over steps 59-599, 0.0165 per step, about 6.7 of them in a 24.75-step dwell near B (W1 without D, H28 design v1 2.3, **measured**; **a W1 figure without D, not a W1D one**), so B gives a few bursts per row. That predicts about 400 × 4 × 0.00084 ≈ 1.3 simultaneous B-D bursts in all of B2. Times an exposure chance of about 0.05-1 per tie and an identity split (T5) of a fraction, that is about 0-1 command row-steps (**inferred**). That is consistent with the measured 0.
- (T5) is not the bottleneck. In B2, h != q on 106 743 of 240 000 row-steps, and the read identity's whiff differs in 7 136 (**measured**). Carried to tie states, this is **a figure from another state distribution**, so I take f_id = 0.25-0.5 as an unmeasured range.

### 4.2 Candidates (relative to the adopted W1D at p_D 0.03, values +1/0/0 kept)

| candidate | layout (from the world code) | what changes vs W1D | inferred reach of (T3)-(T4) |
|---|---|---|---|
| **W1Dp (RECOMMENDED for design)** | W1 (ph22.Masked, V's column False, src/ph22.py:40-44); D's whiff = the same `rngD.random(runs)` draw (src/ph33.py:233, :242) compared with B's plume law at the sensing position instead of p_D: in B's cone or within 3.0 of B, and u < 0.3·exp(-d_along/12) (src/ph11.py:74-84) | D is no longer ubiquitous: a second zero-valued odour co-emitted from B's source, drawn independently; one uniform per row and step as in W1D; no new constant | simultaneous bursts wherever the agent is in B's plume, b(p)^2 = 5.1e-4 (p 0.1) to 0.040 (p 0.27) per step; surviving ties per joint burst 0.35 to 0.043; **about 1-50 command row-steps in 400 x 600, at most as many rows** (state exposure about 1e-4 to 6e-4 per in-plume step, times f_id, times an unmeasured in-plume fraction) |
| W1N (alternative) | W1, the third channel = the masked valued source's raw column (`raw` at src/ph22.py:41, value 0); no D stream | the distractor is replaced by a second zero-valued plume source 10 crosswind of B (src/ph16.py:24, :52-54) | ties only where the two cones overlap, d_along > 14 (half-width 1.5 + 0.25 d > 5, src/ph9.py:34), p 0.093 to 0.037, crossed early in the cast; **lower than W1Dp** |
| W1D at a longer horizon (alternative) | B2 unchanged, more steps | horizon only | rate unchanged (about 1.9e-5 joint bursts per in-plume step); about 3x the near-zero count at 1800 steps |
| W1D at a higher p_D | rejected (section 5, R5) | | |

**Prediction for W1Dp, anchored on the arithmetic above (inferred; no measured anchor in this world):** fewer than 40 exposed rows of 400 in 600 steps, most likely (central range 1-15 rows). The upper range of about 40 rows needs ties that survive the agent leaving the plume and re-entering within the 48 steps a hold outlives its last whiff. The uncertainty is at least a factor of 5 either way: B's in-plume time in W1Dp is unmeasured, f_id in tie states is unmeasured, and the tie-state occupancy in B1/B2 was not recorded by stage one (its runner counts eligible-set differences, not eligible-set size; replay JSON, metrics keys). **This is why D0 comes first (section 6).**

## 5. Candidates rejected on record

- **R1 the read-out threshold 0.05 or R's argmax rule:** they define R (H27 reading R4, src/ph33.py:134). Changing them changes the contrast, not the condition.
- **R2 a module constant** (WIN 9, N_hi 200/300, RESET_AFTER 40, P_PRIOR 60, MARGIN 0.2, UP_TAU 2.0; src/fly.py:38-59): exposing one re-opens its bench (src/fly.py:29). That is an agent change.
- **R3 values outside the tested pairs and triples** (for example +1/+0.5, 0.5/0): no identity row, no adoption, and a new top-set structure.
- **R4 any agent change** (removing the burst rank, writing R back, a free-running R arm as the measurement): excluded by the owner's framing and by stage one's boundary.
- **R5 W1D at a raised p_D:** a world parameter chosen for exposure (an adaptive choice). It leaves H28's tested p_D 0.03, where the capture limit L4 is measured (222/400 lost, master_plan.md:2244), and D's density changes the task the benefit would be read in.
- **R6 a three-source world** (D from a third source position): a new geometry with a free position parameter; W1Dp reaches the same layout class with none.
- **R7 learning on (A7, Agent17 in the H15 Run 2 world):** it would bring ties at 0 (never-reinforced odours) and learned negatives, but it is a coverage condition outside the adopted scope (learning off) and outside stage one; it belongs with the stage-two proposal or a decision of its own.
- **R8 a harness-written two-channel hold** (T3a's construction moved to a step at which V's counter is 152 or more, with the agent in B's cone): it would reach the presence route (H top {V}, R top {B}), but as a state the agent never reaches. It is a constructed witness (offered as 12, point 4), not a condition for a benefit trial.

## 6. Measurement plan

**D0, recount on the recorded strata (recommended first; no new condition).** The design is stage one's passive replay: `src/hold_stage1_instrument.py` unchanged, a new runner modelled on `tools/replay_hold_stage1.py` (code not written here), the same pins, gates (L1/L2/L3, construction, inputs and returns, H projection equals actual), strata A1-A4 and B1-B2 (fly.py is the reference there), seeds `ph35.SEEDS['eval']` and `ph33.SEEDS['eval']` by alias, reused on purpose for a diagnosis and read for no criterion. Added readings, all row-steps of all rows:

- (a) size of `top` and of each projection's `eligible` (one, two, none), and row-steps with a two-member ranked set;
- (b) simultaneous B-D burst steps and their count per row;
- (c) row-steps with exactly one tied member whiffing, not as a burst, and among them the identity split (T5);
- (d) per hold, the held channel's maximum counter and the release cause and lag (timeout, evidence, consecutive reset steps), which measures the margins of 3.1 and 3.2;
- (e) B's whiff probability by step from the recorded positions (src/ph11.py:74-84, arithmetic, no draw), and the **expected** simultaneous-burst and tie counts under W1Dp's and W1N's D rules on the B2 trajectories. These are exact Poisson-binomial expectations, no random draw, labelled as proxies on W1D's state distribution, not W1Dp's.

Output: a re-anchored version of 4.2's arithmetic for W1Dp and W1N, with f_id and the in-plume fraction measured in B2.

**E1, the passive replay on the chosen condition (only if the owner opens it after D0).** This needs a new harness file. It would be modelled on ph33.run (src/ph33.py:226-255), with the D rule as 4.2. The ph chain stays unchanged, as does `ph22.Masked`. The harness needs identity rows (section 7) before any count is released. Size: 400 rows x 600 steps (the adopted size; a longer horizon only if chosen at 12, point 3). New seeds are to be chosen at the FINAL, after the repository and graph scan. One run, no extension, no adaptive change of the condition after any count is seen.

## 7. Identity rows before fly.py is read as the reference

| row | arms | check | why |
|---|---|---|---|
| H0 harness known answer | new harness with the D rule set to W1D's `u < P_D` vs `ph33.run('W1', 'Agent16 D on', (1, 0, 0))` | every recorded field, HR, CONE, `draws_equal`, `rng_equal`, byte equal, at module_identity's smoke size and seeds (`seeds_of(..., smoke)`) | the new world differs from W1D only in D's rule |
| B4 (W1Dp +1/0/0) | `ph33.build('A16')` (Agent16, the ph-chain agent) vs `fly.Fly(nch=3)`, injected as module_identity does | L1 the B rows' 17 fields, L2 the 81 attribute hashes after every act and bump plus generator states, L3 dwell, first, contacts, `ph32.w1sum`, `ph32.lost_t1`; zero tolerance | fly.py is unverified outside its eleven rows (module_report.md section 8) |
| B5 (W1Dp +1/-1/0) | the same two arms | as B4 | the positive control's identity |
| the D stream | new harness | one uniform per row and step from `default_rng(world seed + D_OFF)` (src/ph32.py:109), as W1D | random consumption audited by event, as stage one required |

If W1N is chosen instead: its H0 is the W1 twin's raw column (`draws_equal` against `World7`, src/ph22.py:40-44), and B4/B5 as above with its layout. No identity row is needed for D0, which runs only on existing rows.

## 8. Readings, denominators and the exposure threshold

**Readings (E1, as stage one plus D0's (a)-(c)):** identity mismatch; presence, top and eligible differences; eligible size; nav; flee; target; clipped turn (the command); latent silence and post-wrapper silence; release-adjacent and wall subsets; first differing expression; first command step and command row-steps per row; and the H arm's lost rows (`ph32.lost_t1` as in L3). **Main denominator:** all 400 rows x all 600 steps, no eligibility filter. Conditional counts are given with their own denominators beside them. A zero means none in this sample.

**Exposure threshold, registered here (the condition is READABLE for a benefit design only if all hold):**

- (X1) every passivity and coupling gate of stage one passes in B4 and B5;
- (X2) **positive control:** B5 (+1/-1/0, the flee route) shows command differences on at least one row. Otherwise the instrument is blind in this harness;
- (X3) **rows exposed >= 40 of 400** (at least one command row-step);
- (X4) **not floored:** the H arm's lost rows in [20, 380] of 400. A condition that floors or saturates every arm is unreadable (standing rule).

**Why 40 (hand arithmetic, the project's paired-DP formula, ph33 reading R9: sd = sqrt(b - DP²), se = sd/20, P = Φ((DP - bar)/se - 1.96)).** The anchor is the bar the record used for the hold's benefit, a lost-row DP of +0.05 (H27/H28 M6, master_plan.md:1773). A benefit trial can be discordant at most on exposed rows. With an exposed fraction e and the best case DP = b = e, P ≤ Φ((e - 0.05)/(sqrt(e - e²)/20) - 1.96): 0.025 at e 0.05 (20 rows), 0.48 at e 0.075 (30 rows), **0.92 at e 0.10 (40 rows)**. Below about 30 exposed rows, even a maximal effect fails the record's bar more often than not. The count is a screen on the passive projection over H's states. It is **not** a prediction of discordance in a free-running trial, where R's own state distribution differs (stage one, amendment one).

**Probability that W1Dp clears (X3), inferred from 4.2:** low (central 1-15 rows; about 40 only at the top of a factor-5 range). Roughly 0.1 or less, unanchored. D0 replaces this with measured inputs before any harness is written.

## 9. Interpretation (what each outcome permits)

| outcome | permitted conclusion | what the owner may decide next |
|---|---|---|
| D0 gates fail | measurement invalid; first mismatch reported | a reviewed correction, no reading |
| D0: the bound margins of 3.1/3.2 measured (max held counter well below the window) | the two-channel verdict and the three-channel presence bound hold on the record, with measured margins | record them; no two-channel condition design |
| D0: a held counter at the window, or a hold surviving an evidence release past N | a bound of section 3 is wrong; report it | a constructed-witness check (12, point 4) before anything else |
| D0 re-anchored P(X3) for W1Dp or W1N >= 0.5 | a condition is worth building | open E1 on that candidate (identity rows first) |
| D0 re-anchored P(X3) < 0.5 for both | the adopted-scope branch exists but is rare by the burst rule's construction, in the reachable layouts | defer (d) within the adopted scope; the coverage route (stage two) stays the only informative one |
| E1 gates, H0, B4 or B5 fail | measurement blocked or invalid | reviewed correction |
| E1 (X2) fails | the instrument does not see the flee branch in this harness | blocked; no reading |
| E1 passes (X1)-(X4) | action dependence is measurable in that named condition, outside the adopted scope (a new D layout) | a separate benefit design with preregistered measures, free-running arms and its own seeds; no benefit verdict here |
| E1 1-39 rows exposed | branch reached, below the threshold: unreadable for a benefit trial | defer (d) for this route; no extension, no re-tuned condition |
| E1 (X4) fails | the condition floors the agent; unreadable | as above |

A different `nav` or target is not evidence that either action is better (stage one).

## 10. Seeds, sizes, order

- D0: `ph35.SEEDS['eval']` (A1-A4) and `ph33.SEEDS['eval']` (B1, B2), by alias, a diagnosis of rows already spent; 400 x 600 as recorded; about 400 s at stage one's speed (397.5 s for eighteen runs, **measured**).
- E1: new seeds, to be chosen at the FINAL after the repository and graph scan. World, agent and third-unit streams follow the harness's named rules (D_OFF, A3_OFF; src/ph32.py:109). Smoke and H0 on module_identity's smoke seeds by function name.
- P5: no digit of a registered ph33 or ph35 seed in any file under notes/. This file names seeds only by alias.
- Order: owner's section 12, then D0 (code, owner's local session, run once), then the owner's choice, then (only if chosen) E1 design v2 FINAL with seeds, H0, B4, B5, then the replay once.

## 11. What this design does not test or claim

No benefit or cost of the hold, in any condition. No free-running R trajectory and no fixed-input tape. No claim that W1Dp or W1N is inside the adopted scope: both change D's layout, so any later result there is scoped to that condition. No new value, window, threshold or constant. No learning stratum (R7). No check of the two-channel bound by constructed witnesses unless 12 point 4 is chosen. No claim of impossibility beyond the stated bounds: the two-channel verdict is bounded by the release (48 steps, measured) and the upstream decay (12-14 steps, inferred) against the window 200, for supplied +1/0 and learning off. Every reach figure in section 4 is an inferred rate, not a measurement. Nothing about the coverage stage two, which is the separate draft's.

## 12. What the owner confirms (each with a RECOMMENDED option)

1. **The branch reading (section 2) and the amendments to stage one's reading (2.3).** RECOMMENDED: confirm as readings, recorded with this design, the stage-one report unchanged. Reason: they sharpen the conditions without changing a count or a permitted conclusion. Alternative: amend the report's text (a new report revision, review needed).
2. **The two-channel form.** RECOMMENDED: **no two-channel condition design.** Record that within the bound of 3.1 no condition keeping +1/0, learning off and the constants reaches a command branch. The two-channel branches need a value change, handled by the stage-two proposal (decision:hold-stage2-coverage-proposal-allowed). Reason: both routes are bounded with margins of about 139 and 187 steps, and 960 000 row-steps agree. Alternative: keep the question open until the constructed witnesses of point 4.
3. **The three-channel candidate.** RECOMMENDED: **W1Dp** (D co-emitted from B's source by the read plume law, the same D stream), 400 x 600, designed but not built until D0. Reason: of the reachable layouts it alone puts both zero-valued channels at the same moderate rates wherever B is sensed, adds no constant, and keeps W1D's draw count. Alternatives: W1N (no D stream, lower reach); W1Dp at 1800 steps (about 3x the exposure, a horizon outside every tested scope); W1D at 1800 steps (near zero).
4. **Constructed witnesses.** RECOMMENDED: **not now.** D0's (d) measures the bound margins on natural states. Alternative: add to D0 a Still-stub witness for each route (src/ph16.py:59-61, as the ph33 bench (c) states), run on Agent16/Agent17 and fly.Fly side by side: the two-channel harness-written hold (R8) and the three-channel tie (T1)-(T5). This would show the branches at code level only, not reachability.
5. **The order: D0 before any new world.** RECOMMENDED: **yes.** Reason: section 4's prediction is unanchored. Stage one did not record tie-state occupancy, and D0 measures it plus f_id on spent rows at no new seed cost. Alternative: go straight to E1 on W1Dp (spends a harness, three identity rows and new seeds before the deciding numbers are known).
6. **The exposure threshold (section 8).** RECOMMENDED: (X1)-(X4) as registered, 40 exposed rows of 400, lost rows in [20, 380]. Reason: anchored on the record's +0.05 bar (0.92 best-case pass at 40 rows, 0.48 at 30). Alternatives: 30 rows (best case 0.48); a command row-step count instead of rows (not recommended, since rows are the unit a benefit trial reads).
7. **The reading if D0 predicts failure.** RECOMMENDED: defer (d) within the adopted scope with the record 'branch exists at three channels, exposure rare by the burst rule's construction in the reachable layouts; none at two channels within the bound'. The coverage route stays as the separately proposed stage two. Alternative: E1 on W1Dp anyway, as a measurement of the rare rate (spends new seeds for an expected unreadable outcome).
8. **Identity rows (section 7).** RECOMMENDED: H0, B4, B5 before any E1 count, zero tolerance, as module_identity. Alternative: none (fly.py is not the reference outside its rows).

## 13. Self-review (2026-10-07)

- **Every code claim cites a line:** read-out src/fly.py:312-337; burst record :315-322; presence :325-326; flee :345; turn :346; gate :299-300; release :302-306; N2 :277-291; circuit :118-130; upstream :96-101; constants :38-59; R src/ph33.py:134; D stream :233, :242; plume law src/ph11.py:74-84; mask src/ph22.py:40-44; layout src/ph16.py:24, :52-54; cone src/ph9.py:34.
- **Where my reading could be wrong, and how the review can check it:**
  (i) 3.1(a): formation needs input. This rests on the circuit's unstable point at s = 1 with noise 0.01. A noise-driven crossing would let a hold form late. D0 (d) reads the held counter at formation.
  (ii) 3.2: about nine consecutive evidence-reset steps after a D whiff. This assumes y_B ≈ 0 and ignores the cross-channel term and the circuit noise. Two to three steps would not release (fewer than four), and a B hold could then outlive the window. D0 (d) counts holds that survive an evidence release, and the 480 000 recorded agreeing row-steps are the present check.
  (iii) The release at 48 steps after the last whiff is carried from the H25/H26 measurement to Agent17 and Agent16 (**a figure from another agent, same release code by identity**). A3's zero presence differences bound it at 58 there.
  (iv) Section 4's rates treat B's whiffs as stationary Bernoulli at a fixed p. Plume encounters are position-correlated, which raises simultaneous bursts and shortens surviving ties by unknown amounts. D0 (e) replaces them with expectations over recorded positions.
  (v) f_id is taken from W1D's overall split; tie states may differ.
  (vi) The threshold anchors on +0.05; a later benefit design may choose another bar, and the screen would then be re-derived, not carried.
- **Lessons carried:** H24 (a circuit assumption must cite a bench or a line): the only circuit events used are the measured four-step release and the 48-step release. H17 and H28 (a prediction anchored on the wrong population): every reach figure is labelled with the condition it comes from, and D0 measures before E1. Standing rules: criteria before runs (the threshold is registered here, before D0 or E1); a known-answer arm (B5, and H0 for the harness); floor and ceiling (X4); measurement first (D0).
- **Not done:** no code, no run, no seed, no world, no graph write, no edit of an existing file. Not tested: section 11.

