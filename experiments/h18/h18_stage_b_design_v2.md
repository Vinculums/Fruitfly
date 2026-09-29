# H18 Stage B design v2 FINAL: branch B-iii, what the `return` rule does when the wind cue returns: one cast restart per silence at the first cue-on step, on H16's single-source agent with the adopted ring, in the K5(b) world

Date 2026-09-29. Status: **v2 FINAL (confirmed by the owner 2026-09-29). Stage B opened by decision:h18-stage-b-open.**

The owner's words, verbatim: '권고안대로 확정, v2는 opus 에이전트로 쓰고 Stage B 진행' (gloss: 'confirmed as recommended; v2 written by the Opus agent, then proceed with Stage B').
- The confirmation was given **before the v1 draft arrived**, under the owner's standing instruction to follow the recommended options.
- It was applied **after** the Fable session's review (notes/reviews/2026-09-29-h18-stage-b-design-v1-review.md, sha256 3a99fc17). The review's five amendments are folded in at the sections they touch and marked [v2, amendment n]: (1) the rule at code level (3.2); (2) (I-c) wording (3.3); (3) `restart_rand`'s p and stream (3.2); (4) the per-agent statistic of M2 and M5 (7); (5) execution (9).
- Every point of section 12 is recorded as CONFIRMED (recommended), with its alternatives Not taken.

**v2 differs from v1 only in the status and confirmation text, section 12, the five amendment points, the HEAD, the master_plan.md line numbers (moved at 8c83827; the cited source files are unchanged) and section 9's registered files. NO bar, seed, arm, rule, candidate or stop rule changes.**

v1 DRAFT: experiments/h18/h18_stage_b_design_v1.md, sha256 43cf6da30ffd791e362c16ebc278a37dbceb31289528f41dbc117bd6c1eca16d (commit 8c83827), kept unchanged as history.

Opened for design by decision:h18-stage-b-iii-open-design, the owner's words verbatim 'B-iii 설계 열자, v1 초안은 opus 에이전트로' (gloss: 'open B-iii for design; the v1 draft by the Opus agent'). Branch B-iii is the one branch whose registered condition Stage A met (experiments/h18/h18_diagnosis.md section 10, sha256 fd2e31bb; design v2 section 3, experiments/h18/h18_design_v2.md, sha256 cbc2d97c). Template: H29 design v1 (experiments/h29/h29_design_v1.md, sha256 5078d814) for the section form; H18 design v2 for scope, execution and citation conventions; H10 design v2 section 8 for the order.

**Scope.** Outside the adopted scope. The adopted agent senses the wind on every step (decision:h16-close-limited-adoption, master_plan.md:49-53). **Nothing here changes the adopted agent.** Any adoption would EXTEND the adopted scope, by a separate decision of the owner's. It would adopt a **body rule for the cue-loss condition, not the ring**. Standing rule: open plane, no walls, for the cue-loss task (record:h16-k5b-confounded-by-walls).

**What B-iii does not do.** It does not repair the heading memory.
- Stage A found the cue-off error to be per-step noise summed within a block. The closed-loop residual has sd 2.58 degrees in every rotation bin, the bench gain is 1.0000, and there are no jumps (ph37_read.txt:358; diagnosis section 6).
- The second, zero-input ring step raises the drift sd by 1.4433 (F-v MET, ph37_read.txt:296).
- Branch B-v (one ring step per agent-step) was **not met as registered**, because it also needs F-i NOT MET and F-i read INCONCLUSIVE (diagnosis section 10).
- B-iii leaves the ring, its wiring and its noise as they are. It changes what the body does when the cue returns.

**On what Stage B does not rest.** B-iii's condition in Stage A rests on F3:
- ring_sep 97 of 161 unrecovered events began on a cue-off step (0.6025), one event above the registered 0.60.
- The recorded `ring` rows read 89 of 162 (0.5494), INCONCLUSIVE (ph37_read.txt:423, :432; diagnosis section 10).

**Stage B's test does not rest on that margin.** It is a direct paired comparison of the changed agent with the unchanged ring on new seeds, with its own bars (section 7).

Code citations are path:line at HEAD 8c83827. sha256 prefixes:

| file | prefix |
|---|---|
| src/ph12.py | e1035e09 |
| src/ph12b.py | ec6b1896 |
| src/ph9.py | 7699b4e6 |
| src/ph10.py | de93f177 |
| src/ph11.py | e80f40bd |
| src/ph16.py | 33d5fdb2 |
| src/ph23.py | ae180492 |
| src/ph35.py | e4a3ceda |
| src/ph37.py | 76190250 |

Measurement citations:
- "Stage A" is experiments/h18/ph37_read.txt (sha256 5d4e7bd0), with ph37_summary.json (2e543c08) and h18_diagnosis.md (fd2e31bb).
- "K5 record" is experiments/h16/ph12b_h16r2.txt (48e4e73c).

Every claim is labelled **measured**, **read** or **inferred**. Nothing was run for this draft except grep, git grep, sha256sum and git log.

## 0. What is new

| item | recorded `ring` agent (H16 `return` + adopted ring) | Stage B changed agent | section |
|---|---|---|---|
| cast clock at a cue return | runs on (clock = steps since the last whiff, ph12.py:116) | **set to 0 once per silence, at the first cue-on step after the last whiff on which there is no whiff** | 3.1, 3.2 |
| ring, wiring, noise, cue | as adopted (ph12.py:84, :106-109; ph11.py:51-52) | unchanged | 0 |
| new state | none | two bits per agent: the previous step's cue state, and an 'armed' flag set on a whiff and cleared at the restart | 3.2 |
| random draws | the agent generator (turn noise, ring noise) | the same, no new draw (the rule is deterministic) | 3.3 |
| every-step-cue agent (K5(a), the adopted agent) | | identical by code (no cue return ever occurs) | 3.3 |

## 1. Hypothesis

**H18-B-iii: on the K5(b) task, the agent with one restart of its cast clock per silence at the first cue-on step leaves fewer agents unrecovered in the last third than the unchanged ring agent on the same worlds and noise (M2).** The agent is H16's `return` rule with the adopted ring. The restart comes at the first cue-on step after the last whiff (section 3.2). The test is paired: the changed agent draws the same noise as the unchanged one.

Two further conditions:
- The gain must exceed that of the same number of restarts at random whiff-free steps (M5).
- The last-third score must not fall (M3).

The same restart on an agent with perfect heading is reported (M4). If it raises that agent's score, the gain is named a body change, not a compensation for the memory.

Stated narrowly: the K5(b) world (open plane, cue off 50 of every 100 steps after step 50, ph12.py:63-65, ph12b.py:44), one source, no learning, 200 agents x 5400 steps, the adopted ring at noise 0.3.

## 2. The measured reason

### 2.1 What Stage A measured at and after a cue return (measured)

- **The heading estimate recovers within a few steps of the cue's return.** Median abs error on cue-on steps 1, 2, 3 and 5 after a cue-off block: 5.485, 2.390, 1.221 and 0.779 degrees (ring_sep, n about 10,700 per step). The p90 at step 3 is 2.929, and no step from 2 onward has any error over 20 degrees. The ring reads the same (5.503, 2.353, 1.198, 0.775). Source: ph37_read.txt:351, :377.
- **The agent is off the plume when the cue returns.** Of ring_sep's 161 unrecovered events, 0.7702 are outside the odour at the first cue-on step after the last whiff, and 0.9876 at the first cue return (ph37_read.txt:361). The ring reads 0.7654 and 1.0000 of 162 (ph37_read.txt:387).
- **The cue-off error displaces the agent in recovered and unrecovered events alike.** The median abs path error per cue-off block over the plume half-width is 2.9582 for unrecovered events and 2.1974 for recovered ones (381 and 6,069 block-event pairs). The mean abs P is 4.423 units, sd 5.529, over 10,796 blocks (ph37_read.txt:357). F-vi read INCONCLUSIVE.
- **Losses begin during cue loss somewhat more often than chance, on the instrument arm only.** 0.6025 of ring_sep's unrecovered events began on a cue-off step (97 of 161), against a measured cue-off share of 0.4955 (535,088 of 1,080,000 agent-steps). On the recorded ring it is 0.5494 (89 of 162). Source: ph37_read.txt:423, :432.
- **With perfect heading the same rule recovers almost every loss.**

  | arm | lost events | recovered | reacquisition median | late unrecovered (of 200) |
  |---|---|---|---|---|
  | integrate | 5,848 | 99.3 % | 153 | 0.5 % |
  | ring | 2,541 | 93.5 % | 161 | 64.5 % |

  Sources: K5 record:180, :184, :174, :178.
- **Lost ring agents end far from the source.** The median distance at the end is 111.5 units for ring and 102.2 for ring_sep, against 19.8 on the integrator's path (the shadow arm); the design's standing rule is LMAX 25 (ph37_read.txt:362, :388, :414).

### 2.2 The rule, as code (read)

- `since` and `clock` are both zeroed on a whiff and incremented otherwise (ph12.py:115-116).
- The code states the separation explicitly: "`clock` drives the cast and `since` only measures silence. They differ in the wall rules, where a contact may restart the search without the agent having smelled anything" (ph12.py:79-80).
- The `wall` rule already restarts the clock without a whiff, while lost (ph12.py:91-94).
- The `return` offset is a triangle wave, MAXOFF (1 - abs((clock / SAT) mod 2 - 1)): 0 at clock 0, 170 at SAT = 141.7 and 0 again at 283.3 (ph12.py:29, :99-100; MAXOFF 170 and CAST_GROW 1.2, ph9.py:40).
- The side is +1 or -1 by (clock // CAST_PERIOD) mod 2, with CAST_PERIOD 30, times cast_sign (ph12.py:125; ph9.py:40).
- The target is UPWIND 180 on a whiff, else UPWIND + side x offset (ph12.py:126; ph9.py:33).
- The turn is clip(GAIN x angdiff(target, est), plus or minus MAXTURN) + TURN_NOISE x a normal draw, with GAIN 0.6, MAXTURN 40 and TURN_NOISE 6 (ph12.py:127-128; ph9.py:41).
- **Cue schedule:** on iff (t + phase) mod 100 >= 50, with a random phase in 0-99 per agent (ph12.py:55, :63-65), OR t < 50 for every agent (ph12b.py:44).
- A cue return is therefore a step t with the cue on at t and off at t - 1. After step 50 it comes every 100 steps per agent, after a 50-step cue-off block.

### 2.3 What a cue return means for the cast (read, inferred)

- At the first cue return after a last whiff at t_L, clock = since = t - t_L.
  - If t_L lay on a cue-off step, this is 1 to 50.
  - If t_L lay on a cue-on step, the next return comes after the whole following cue-off block, so 51 to 100.
  - Read, from ph12.py:65, :116.
- The cast loop's first clock steps after t_L were walked with the drifting estimate. The body was off its target by e on every step (ph12.py:127). The walked part of the loop is therefore not the loop the rule meant.
- The loop continues from its current phase with the now-correct estimate, from a position displaced by the summed error (2.1). **Inferred.**

## 3. The change

### 3.1 The candidates, evaluated from the numbers

| candidate | new state | what the numbers say | verdict |
|---|---|---|---|
| (1a) clock <- 0 at **every** cue return with no whiff | previous cue bit | see (1a) below: the loop would drift upwind about 7 x faster | **rejected** |
| **(1b) clock <- 0 once per silence: at the first cue-on step after the last whiff, if no whiff there** | previous cue bit, armed bit | see (1b) below | **chosen** |
| (2) k steps with target UPWIND at the cue return, then the cast resumes | a k-step counter | an upwind run moves the agent along the plume axis, not across it; a free parameter k with no record to fix it | **rejected** |
| (3) restart the cast with its side toward the displacement | the ring's snap at the cue return (own state) plus a record of the targets walked in the block | see (3) below | **rejected** |
| (4) hold the pre-dropout estimate for the block (`none`-like) | none | `none` is over 45 degrees on 66.15 percent of cue-off steps, median 0.0, late unrecovered 95.5 percent (K5 record:168, :173) | **rejected**: a known floor |
| (5) no change: close as a limit (B-close) | | the alternative of section 12 point 1 | alternative |

**(1a) in detail.** After a restart at a cue return the clock would run through the 50 cued steps and the 50 cue-off steps and be restarted again at about clock 100. The offset would never exceed 1.2 x 100 = 120 degrees (ph9.py:40).
- The mean of cos(offset) over offsets 0 to 120 is sin(120 deg) / 2.094 = 0.4135. The upwind drift is 0.6 x 100 x 0.4135 = **24.8 units per 100 steps**.
- The unchanged full loop's mean cos over 0 to 170 and back is sin(170 deg) / 2.967 = 0.0585, a drift of 0.6 x 283.3 x 0.0585 = **9.9 units per 283 steps** (3.5 per 100).
- So (1a) would move a lost agent upwind about 7 times faster, past the source and away from a plume that lies downwind of it.

Inferred (straight-path arithmetic from ph12.py:99-100, :126, ph9.py:31, :40; heading assumed to follow the target).

**(1b) in detail.** A restart **once per silence** leaves every later loop of that silence whole, with the full 0 to 170 to 0 period of 283.3 steps. What it changes is where the loop is anchored. The anchor becomes the first step at which the estimate is again the cued heading, within 5.5 degrees at the first cue-on step and 2.4 by the second (2.1). The loop is then walked from the position the agent actually occupies with the estimate the rule assumes.
- This is the post-whiff search the integrator recovers from in 99.3 percent of events, but started from the displaced position, not from the plume edge.
- Its crosswind reach within 90 steps: the zigzag swings about 5.3, 14.2 and 17.7 units in the first three 30-step half-periods (see below), so it reaches about 9 units either side of the anchor.
- The plume half-width is 2.75 to 6.0 units at along 5 to 18 (ph9.py:34), so the median displacement of 2.2 to 3.0 half-widths (2.1) is about 6 to 18 units. The restarted loop reaches the near part of that range within 90 steps. **Inferred.**
- **The record measures no counterfactual. Stage A did not run a restarted cast. Whether (1b) gains anything is what Stage B tests.**

The swing arithmetic: 0.6 x 30 x the mean sin of offsets 0 to 34.8, 36 to 70.8 and 72 to 106.8 degrees, which is 0.295, 0.790 and 0.985. The swings alternate sides, so the positions are about +5.3, -8.9 and +8.8 units.

**(3) in detail.** The agent does hold one own-state signal of its cue-off error: the jump of its own estimate when the cue snaps the bump back, about -e at the last cue-off step.
- Under a random-walk reading, e at the block's end correlates with the summed error at sqrt(3)/2 = 0.87 (inferred).
- But the world-frame crosswind displacement also depends on the targets walked during the block, which sweep through plus or minus 170 degrees.
- Stage A measured P perpendicular to the walking direction, not its world-frame projection, and not its correlation with the snap (not in the record).
- Using the snap would need a record of the displacement: a position-like record that H29's precedent excluded, row (e3) 'a position or source record' (experiments/h29/h29_design_v1.md section 3.1).
- Rejected: not grounded in any measured number, and it needs state of a kind the precedent excludes. The snap-displacement correlation is registered as a reported bench reading (4 (b4)) for any later design.

**Why (1b) is the one lever.** It is the smallest change the record points at: the estimate is good again within 2 to 3 steps of a cue return (2.1), and the rule already lets the clock be restarted without a whiff (ph12.py:79-80, :91-94). It adds no free parameter:
- **the reset value is 0**, the rule's own value after a whiff (ph12.py:116);
- **the firing step is the first cue-on step**. Waiting 2 or 3 steps for the estimate to settle (median 2.390, then 1.221) is not needed: at clock 0 the target is UPWIND with offset 0, and a 5.5-degree estimate error adds 0.6 x 5.5 = 3.3 degrees to one turn, against TURN_NOISE 6 on every turn (ph9.py:41) (inferred);
- **once per silence**, by (1a)'s arithmetic.

No grid; nothing is calibrated on task scores.

### 3.2 The changed agent (code not written here)

A new file, proposed src/ph38.py, defines `Nav5(ph12b.Nav3)`. ph12b.py, ph12.py and every adopted file are imported unchanged and their sha256 checked at run time. Per agent:
- `armed` <- True on a whiff (hit);
- `prev_on`: the previous step's cue state, True at construction (every agent is cued for t < 50, ph12b.py:44);
- at step t: fire = cue on at t AND not prev_on AND armed AND no whiff at t;
- where fire: clock is set so that the clock used for the target at t is 0; `armed` <- False. `since` is not touched;
- everything else is Nav2.act unchanged (ph12.py:114-130).

The rule draws no random number.

**[v2, amendment 1] The rule at code level.**
- `armed` is **False at construction**. An agent with no whiff yet cannot fire; this is consistent with Stage A's choice C3, which excluded events with no prior whiff.
- The clock reset happens **after** ph12.py:116's increment on the same step. So the target of the firing step is computed with clock 0: offset 0 by ph12.py:99-100, side = cast_sign by ph12.py:125 (clock // 30 = 0).
- `cast_sign` is not touched; `since` is not touched.

**Control arm `restart_rand`.** The same agent, but the restart fires on each whiff-free step with probability p instead of at cue returns. It draws from its own stream, so the turn noise stays paired. The probability is fixed as p = firings / whiff-free agent-steps of Nav5 on the bench seeds (calibration then freeze, H10 form), recorded before the development run.

**[v2, amendment 3]**
- p is **one number**, frozen on the bench and written into the headers of the development and evaluation runs.
- restart_rand's per-step draws come from numpy SeedSequence(agent seed).spawn(1) child 0, so `ring`, `restart` and `exact_restart` keep identical agent-generator sequences.

### 3.3 Identities, by the code

- **(I-a) The adopted agent is identical by code.** Two reasons:
  - `Nav5` is not in any adopted agent's class tree. The adopted cast is its own implementation (ph23.py:95-98, Agent9 and its descendants to Agent17, ph35.py:104), and no adopted file imports ph38.py (checked by git grep at run time).
  - In the adopted worlds the cue is on at every step. World7 (ph16.py:43) descends through World5 and World4 to ph11.World2, whose wind_on is rng.random(R) < p_wind with p_wind 1.0 (ph11.py:59, :86). So a cue return never occurs there.
- **(I-b) In K5(a)** (W-cone, walls 160 apart, cue every step), Nav5 equals the recorded-construction `ring` bitwise on every field. World3.wind_on is all True under 'always' (ph12.py:64; ph12b.py:44), so fire is never True.
- **(I-c) In K5(b)**, Nav5 equals `ring` bitwise on every step before each agent's first firing. **[v2, amendment 2]** This holds because the rule draws no random number and the ring's noise stays on the agent generator. After the first firing the two arms consume the same draws on different states, so positions are **not** paired after an agent's first firing.
- **(I-d)** `exact`, `none` and `integrate` are ph12b.run2 unchanged.
- **(I-e)** Nav5 with the rule switched off equals ph12b.Nav3 bitwise (run2 on the bench seeds).
- **(I-f) The firings are exactly the defined steps.** Each firing is a cue-return step. Per agent, the number of firings equals the number of cue-return steps that are the first return after a whiff and carry no whiff. Printed with the number of cue returns per agent.

## 4. Mechanism bench (bench seeds, before any development seed)

- (b1) The identities (I-a) to (I-f) on the bench seeds, K5(a) and K5(b).
- (b2) Firings per agent against cue returns per agent: the distribution, and the clock value at each firing (the phase restarted; not in the record).
- (b3) The calibration of p for `restart_rand`, printed and frozen.
- (b4) Reported: the correlation of the snap at each firing with the world-frame crosswind displacement of the preceding block relative to the paired `integrate` agent, up to their divergence (for any later design; no bar).
- **(h) Stop rules:**
  - M2's bench point estimate d_bench <= 0, or its pass probability at the bench's d and discordance below 0.5 (section 7): **STOP**, 'stopped at the bench'.
  - M5's bench point estimate <= 0: **STOP**.
  - Nothing is tuned after a stop.

## 5. Tasks

- **K5(b) (registered):** World3, open plane, wind 'blocks', `return`, 200 agents x 5400 steps, as recorded (ph12b.py:198-201) on new seeds.
- **K5(a) (identity task):** W-cone, walls 160 apart, cue every step (ph12b.py:189-191).
- **Boundary exposure,** reported as the H16 Run 2 opening rule asks (master_plan.md:2167-2171):
  - K5(b): contacts 0 by construction (ph12b.py:52-53). Reported: the distance from the source at the end and its maximum over the run, and the share farther than LMAX 25.
  - K5(a): contacts and near-wall dwell, as describe2 prints them.

## 6. Arms (K5(b); every arm also run in K5(a) for identities)

| arm | heading | rule | role |
|---|---|---|---|
| `ring` | RingExact as recorded (ph12.py:105-109) | `return` | the reference, paired |
| `restart` | the same ring | Nav5 (1b) | the change (M2, M3) |
| `restart_rand` | the same ring | restarts at random whiff-free steps at rate p | anti-trivial control (M5) |
| `exact` | true heading | `return` | ceiling (record 24.0, late unrecovered 0.5 percent, K5 record:163) |
| `exact_restart` | true heading, wind 'blocks' | Nav5 (1b) | body check (M4) |
| `none` | held cue | `return` | floor (record 0.0, 95.5 percent, K5 record:168) |
| `integrate` | commanded turn, snapped while cued | `return` | reference (record 24.0, 0.5 percent, K5 record:180) |

## 7. Criteria, with pass probabilities

**General rules:**
- One statistic per criterion.
- Paired percentile bootstrap over the 200 agents, 5000 resamples, 95 percent.
- One evaluation, no extension; a group under 50 unreadable.
- **Pass probabilities** are hand arithmetic: for a paired share difference d with discordant fraction b, se = sqrt(b - d^2) / sqrt(200) and P = Phi(d / se - 1.96). The discordance between `restart` and `ring` is not in the record; the bench measures it.

**The criteria:**
- **M0 readability:** exact minus none, last-third median, >= 10 (record 24.0 against 0.0, K5 record:163, :168). Pass about 1.
- **M1 identities and mechanism:** (I-a) to (I-f) all True. Pass about 1 if the code is right.
- **M2 (main):** paired difference in late-unrecovered share, `ring` minus `restart`, **95 percent lower bound > 0**. Pass probability:

| d | b 0.3 | b 0.5 |
|---|---|---|
| 0 | 0.025 | 0.025 |
| 0.05 | 0.25 | 0.17 |
| 0.10 | 0.75 | 0.52 |
| 0.15 | 0.98 | 0.87 |
| 0.20 | > 0.999 | 0.99 |

  One line checked: d 0.10, b 0.3 gives se = sqrt(0.29) / 14.14 = 0.0381, and Phi(2.63 - 1.96) = Phi(0.67) = 0.75.

  **Why the bar is > 0, not a set size:**
  - Every unrecovered event is touched: no whiff follows t_L, and a cue return comes within 100 steps (ph12.py:65), so the restart fires once in each of the 161 (read, measured).
  - So the share the change can touch is 161 of 161 and gives no bound below the ceiling.
  - The upper bound is the ceiling itself: the recorded ring's 64.5 percent (129 of 200) against exact's 0.5 percent, a possible reduction of up to 0.64.
  - The F-iii and F3 numbers do not fix how much of that a restart can recover. 0.7702 of events are outside the odour at the first cue-on step, and the displacement is the same order in recovered events (2.1).
  - A bar above 0 would be a guess about the effect, not a reading of it.
- **M3 no loss of score:** paired mean last-third score, `restart` minus `ring`, **95 percent lower bound > -1.0**. The recorded ring's last-third mean is 5.5, p75 11.0 (K5 record:174). The paired sd is not in the record; pass probability read at the bench.
- **M4 body check (reported, a wording rule):** paired mean last-third score, `exact_restart` minus `exact`.
  - If the lower bound is > 0, the restart raises a perfect-heading agent's score. The M2 statement then names the gain a body change that holds with or without the memory.
  - If the upper bound is < 0, the restart costs a perfect-heading agent. This is reported, with no effect on the verdict.
- **M5 anti-trivial:** paired difference in late-unrecovered share, `restart_rand` minus `restart`, **95 percent lower bound > 0**. Same pass-probability table.
- **[v2, amendment 4] The per-agent quantity of M2 and M5.** Late unrecovered is `absorbed`'s per-agent flag: no whiff in the last three blocks (ph12.py:164). The paired difference is the mean over the 200 agents of (flag of the first-named arm minus flag of `restart`), bootstrapped over agents: flag_ring - flag_restart for M2, flag_restart_rand - flag_restart for M5.
- **M6 exposure:** reported (section 5).

**Joint pass probability** (M0 x M1 x M2 x M3 x M5, independence assumed, order of magnitude):
- at d 0.10 and b 0.3: about 0.75 x 0.75 x 0.9, **about 0.5**;
- at d 0.05: **about 0.05**.

The probability of reaching the evaluation is that of passing the bench stop rules.

**Verdict:** SHOWN iff M0, M1, M2, M3 and M5 pass. The statement: 'with one restart of the cast clock per silence at the first cue-on step, the `return` agent with the adopted ring leaves fewer agents unrecovered in the last third under 50-step cue loss than the unchanged agent on the same worlds and noise, and more than restarts at random steps would; the ring is unchanged.' If M4's lower bound > 0, the statement adds: 'the restart also raises a perfect-heading agent's score; it is a body change'.

## 8. Unreadable conditions

- M0 failing.
- M1 failing (an implementation error, repaired and disclosed before the evaluation).
- A group under 50.
- p not frozen before the development run.
- The seeds of section 9 used before the owner confirms this design.

## 9. Seeds, sizes, order

**New registered integers:**

| stage | world | agent | bootstrap |
|---|---|---|---|
| bench | 18101 | 18201 | 18104 |
| development | 18102 | 18202 | 18105 |
| evaluation | 18103 | 18203 | 18106 |

- Streams: numpy SeedSequence(agent seed).spawn(1), child 0 the `restart_rand` draws.
- The `ring` noise stays on the agent generator, as recorded, so `ring`, `restart` and `exact_restart` draw the same numbers.
- K5(a) and K5(b) use the same pair within a stage.

**Scan done 2026-09-29, before this file carried the numbers.** `git grep -nwE '<n>'` over the tracked files at d789f95 (363 files), and again with `--untracked`. Each of 18101, 18102, 18103, 18104, 18105, 18106, 18201, 18202 and 18203 had **0 hits** in both. The graph (vinc) scan cannot run (remote key expired, master_plan.md:2395-2396): **PENDING**.

**Sizes:** 7 arms x 2 tasks x 200 x 5400 per stage.

**Order:** the owner confirms section 12 (done, 2026-09-29) -> v2 FINAL (this file) -> src/ph38.py (Nav5; ph12b, ph12 and the adopted files imported unchanged, sha256 checked) -> self-checks -> bench (b1)-(b4) with the stop rules (h) -> p frozen and recorded -> development run (operation errors only) -> one evaluation -> report.
- One arm per process, arrays to disk and a separate reading pass (H18 v2 amendment 1).
- The local Claude session, one job at a time, BLAS pinned to one thread, uv with numpy 2.4.6.
- No GitHub Actions. Nothing changes after a table.

**[v2, amendment 5] Execution.**
- One arm per process, with float32/int8 arrays to disk and the readings in a separate pass (H18 v2 amendment 1). numpy 2.4.6.
- The bench's stop decision is printed and committed before any development seed is used.

**[v2] Files and invocation (registered).**
- **Harness:** src/ph38.py.
- **Outputs:** experiments/h18/ph38_bench.txt, ph38_dev.txt and ph38_eval.txt, all LF. Each has a header in ph37.py's form: python, numpy, platform, the script's sha256, and the sha256 of every imported source, checked against the prefixes of this header (a mismatch stops).
- **Arrays:** per-arm arrays under experiments/h18/arrays_b/ (npz, float32/int8/int16). They are kept local and not committed; each is listed with its sha256 in the stage output.
- **Summary:** one json per stage (proposed ph38_bench_summary.json, ph38_dev_summary.json, ph38_eval_summary.json).
- **Report:** experiments/h18/h18_stage_b_report.md.
- **Invocation,** from the repository root in Git Bash, one process at a time:
  `export PYTHONHOME= PYTHONPATH= OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 && uv run --no-project --with numpy==2.4.6 --python 3.13 python src/ph38.py <stage> [<arm>]`

## 10. Predictions, with the arithmetic

- **M0, M1:** pass (read).
- **Firings (b2):** about one per whiff-free stretch that spans a cue return. Lost agents fire once per silence, tracking agents about once per 100 steps with a small clock (a short silence). **Inferred.**
- **M4:** the restart on `exact` changes the loop's anchor while the heading is exact. It is predicted near 0 (the integrator's recovery is already 99.3 percent, K5 record:184), inferred.
- **M2:** d is not predictable from the record (3.1: no counterfactual measured). Two readings:
  - Against a gain: each later cue-off block adds a displacement of the same order (2.1). The restart acts on only the first block after a whiff, and 94.0 percent of events already recover without it (ring_sep, diagnosis section 8).
  - For one: 0.7702 of unrecovered agents are off the odour at the first cue-on step, with a correct estimate 3 steps later, and their continuing loop is anchored where the estimate was wrong.
  - A central guess of d about 0.05 (range 0 to 0.15) is inferred and weak. At 0.05 the pass probability is about 0.2, so the bench stop rule is the likely end.
- **M5:** if d > 0 comes from the restart's timing, restart_rand at the same rate gains less (inferred). If restart_rand gains as much, the timing is not the cause and M5 fails.
- **What would make them wrong:** the restart moving lost agents farther from the source (the arithmetic of (1a) at a smaller scale, from a loop anchored away from the plume). (b2) and the exposure reading print it first.

## 11. What Stage B does not test, and what it would not show even if SHOWN

- **The ring still leaks.** Stage A's description stands: per-step noise summed within a cue-off block, raised by the second ring step (F-v MET).
- A SHOWN B-iii is a body rule that copes with the leak. It does not repair it, and it is not an adoption of the ring.
- The adopted two-channel task (Agent17) is untested (identical by code, 3.3).
- Other dropout schedules (lengths other than 50, random rather than periodic), walls under cue loss, other reset values or firing steps, the rejected candidates (3.1), and cold search (H17) are untested.
- Whether a fly restarts its search when a directional cue returns is not claimed. No fly finding is cited.

## 12. What the owner confirmed (2026-09-29: every point CONFIRMED as recommended)

The owner, 2026-09-29, verbatim: '권고안대로 확정, v2는 opus 에이전트로 쓰고 Stage B 진행' (gloss: 'confirmed as recommended; v2 written by the Opus agent, then proceed with Stage B'), decision:h18-stage-b-open, given before the draft arrived under the standing instruction to follow the recommended options and applied after the review. Each point is v1's RECOMMENDED option, now CONFIRMED; its alternatives are Not taken. The review's amendments are marked [v2, amendment n] where they land.

1. **Whether to open Stage B on (1b).** **CONFIRMED** (recommended): yes, bench first, with the stop rules of 4 (h). The predicted pass probability is low (section 10), and the bench reads d and the discordance before any development seed. Not taken:
   - (a) B-close now: H18 is closed as a recorded limit of the ring outside the adopted scope, with Stage A's description;
   - (b) (1a) every-return restart (not recommended, 3.1 arithmetic);
   - (c) candidate (2) with a registered k (not recommended: no record fixes k).
2. **The lever and its parameter.** **CONFIRMED** (recommended): clock <- 0 at the first cue-on step after the last whiff with no whiff there, once per silence; since untouched; no grid. Not taken:
   - firing at cue-on step 3 (estimate median 1.221 there, 2.1);
   - an every-return restart.
3. **The code.** **CONFIRMED** (recommended): new file src/ph38.py with Nav5(ph12b.Nav3), no adopted file edited, the identities of 3.3. Not taken: none. [v2, amendments 1-3] The rule at code level (3.2), the (I-c) wording (3.3), and restart_rand's p and stream (3.2).
4. **Tasks and arms.** **CONFIRMED** (recommended): sections 5 and 6. Not taken: drop `exact_restart` (loses the body check).
5. **The bars.** **CONFIRMED** (recommended): M2 and M5 lower bound > 0; M3 lower bound > -1.0; M4 as a wording rule. [v2, amendment 4] The per-agent flag of M2 and M5 is named in section 7. Not taken:
   - M2 at a set size, e.g. lower bound >= 0.05 (pass about 0.2 at d 0.10, b 0.3);
   - M3 dropped.
6. **The stop rules.** **CONFIRMED** (recommended): 4 (h). Not taken: the bench reported only.
7. **The seeds.** **CONFIRMED** (recommended): section 9 (0 hits each; the graph scan PENDING). Not taken: other numbers, scanned then.
8. **Execution.** **CONFIRMED** (recommended): section 9's order and environment. Not taken: none. [v2, amendment 5] One arm per process, arrays to disk, a separate reading pass, numpy 2.4.6; the bench stop decision is committed before any development seed; files and invocation are registered in section 9.
9. **Scope.** **CONFIRMED** (recommended): as the header states; any adoption is a separate decision that extends scope, and adopts a body rule for the cue-loss condition, not the ring. Not taken: none.

## 13. Self-review (2026-09-29)

- **Weakest: the lever's gain is not grounded in a measured counterfactual.** Stage A never ran a restarted cast. The case for (1b) rests on the fast recovery of the estimate and on the rule's own post-whiff search, which recovers 99.3 percent with perfect heading. It does not rest on a number that predicts d. The pass probability may be low, and the bench stop rule is expected to decide.
- **Weakest: the control's rate is matched on average, not per agent.** p is one number calibrated on the bench. restart_rand fires the same number of restarts in expectation, not the same number per agent or per silence.
- **Weakest: the pass-probability table is conditional.** The discordance b and the paired sds are not in the record. The table spans b 0.3 to 0.5 by assumption; the bench measures them.
- The (1a) and swing arithmetic assumes the heading follows the target on a straight path. The turn clip (40 degrees per step) and the noise make the real loop smoother (inferred).
- The cast-phase sensitivity found in H29's T3b diagnosis (a window 50 steps longer missed the whole first pass) suggests that the outcome may depend on the phase the restart imposes. Only one reset value is tested (section 11).
- B-iii was met in Stage A on one event (97 of 161) and not on the recorded arm. The header states it; Stage B's test does not use that number.
