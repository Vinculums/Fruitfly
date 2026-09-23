# H24 design v3 FINAL: presence-scoped value filter, counter starting ON, N 60

Date 2026-09-23. Status: **v3 FINAL (confirmed by the owner 2026-09-23 as recommended: M7(b) reported, not a bar).** Supersedes H24 design v2 candidate FINAL (doc d5a2e259bfb6445b9, local experiments/h24/h24_design_v2.md, sha256 f84ddf998e9e975a2be41fc2f8e7d7d51abbd0a87697082e680a4ebcf5a6ee9f), which stays on record as history. The v2 status paragraph follows unchanged. Written on the owner's choices of 2026-09-23 (decision:h24-design-v2-choices) and the signed relaxation of the classification rule for H24 (decision:classification-rule-relaxed-presence-counter). Supersedes H24 design v1 DRAFT (doc d24c2efe28592c34d, local experiments/h24/h24_design_v1.md), which stays on record as history. Follows decision:filter-scope-explore-option-v. H23's verdict and adoption (decision:h23-closed, decision:h23-filter-adopted-within-tested-conditions) stand and are not re-judged. Supplied values, learning off, G 2, the H21 gate on, C0. Template: H23 design v2 (doc db6df2e0013ab96e7).

**Changes from v2.** The owner confirmed section 12 as recommended on 2026-09-23 ('음 추천안으로 해보자'), with one change to point 3: M7(b) (release within N + 40, relative to Agent6) is DEMOTED from a bar to a reported quantity. Reason: at the loss Agent9 and Agent6 are in different states (Agent9 mostly at the valued source, where the neutral whiff rate is exactly 0; section 5), and Agent9 is structurally 19 steps later (section 7, structural expectation), so a bar there would measure the start-state difference, not the rule. Edits, and only these: the status line; section 1 (iii); section 4 (f) and the bar-decision paragraph (decision:h24-t3-bars now fixes only bar_D for M7(c); S6 reported); the last line of section 5's tolerance arithmetic; section 6's T3 maintain role; section 7 M7(b) (reported: S per arm, the paired Agent9 - Agent6 difference and its interval printed, no bar; the S6 < 0.10 note kept as a readability note for the report), the joint pass probability and the verdict statement; section 8's pinned-baseline condition; the T3 line of section 10's 'what would make the predictions wrong'; section 12 (now the owner's confirmation). Section 13 is v2's self-review, kept verbatim as history. Nothing else changes.

**Changes from v1.** (1) One variant only, (v-p): a presence counter per odour that starts ON, N 60 (owner's point 1). (v-a) and (v-c) are recorded as rejected with the diagnosis numbers (section 3). (2) The classification rule is relaxed for H24 only, by a signed decision that names old, new and anchor and records the ON start as a prior (owner's point 2; section 3). (3) T3, a 'sensed then lost' world, is added: the only registered condition that exercises the window (owner's point 3; sections 5 to 7, M7). (4) T2's dwell bar is not fixed here. The design registers the criterion and the rule that derives its bar from Agent6's dwell in bench (d). The number is fixed by decision:h24-t2-dwell-bar after bench (d) and before the development run (owner's point 4; M5(b)). T3's two behavioural bars follow the same rule, from bench (f), in decision:h24-t3-bars. That second decision is this design's proposal and needs the owner's confirmation (section 12). (5) Two corrections to v1's wording. In W1 the agent is Agent8 on steps 0 to 58 (N - 1 = 59 steps), not 0 to 59. The T2 bar 'first surge within N + tolerance' stays a reported number, not a bar, because it fails by prediction (M5(e)). (6) The identities are restated for the counter (section 3). Bench (f) is added. The seeds are unchanged. T3 shares T1's seeds.

## 1. Hypothesis

**H24: with the value filter's v_max taken only over odours present in the agent's own state, where presence is a per-odour counter of steps since the odour was last sensed, window N 60, starting ON (section 3), the agent does three things.** (i) It keeps H23's result in the H21 choice task: P(V) within an allowed gap of the adopted filter (Agent8) and at least 0.88. (ii) In the absent-odour world W1 it tracks the only odour present, dwelling within an allowed gap of the unfiltered agent (Agent6). (iii) In the 'sensed then lost' world T3 it releases the neutral odour exactly N steps after the last valued whiff [M7(a)] and tracks it within the registered gap of Agent6 over steps 400 to 599 [M7(c)]. All three tasks are required for the verdict (T1, T2, T3; sections 5 to 7). Implementation claims are checked on constructed states first (section 4, M4).

## 2. The measured reason

Sources: record:absent-odour-check-result (report db7b4a7ca1c2ab7ea); record:h23-result (report d8b91235798da849f); record:selection-circuit-revision-via-empty-state; record:option-v-presence-diagnosis-result: ph21b.py (sha256 4f3b707ed5de68dca81631633b5589e6c8ad342dda5a786b0c6a43f7ae870b12, source doc d0a340a477986a52c), output experiments/h24/ph21b_diag.txt (sha256 17a0bf412a307d84e2be6b065f6f9446f4768321ff36040b485f2999a87f549a). All numbers below are dev-seed numbers from that diagnosis (H23 development seeds; absent-check development seeds for W1). The diagnosis ran no new rule, and it did not touch the evaluation seeds.

- The absent-odour check (seeds 1775/1875). In W1 Agent8 never surges. It reaches the source by casting past it (0.860). Its dwell median is 8 against Agent6's 25 (mean 12.36 against 24.31; paired lower in 330/400 rows). It ends upwind of the source.
- (2) In the H21 task, Agent8's first valued whiff comes at step 4/16/111 (quartiles; never in 3 rows). The fraction of rows with a valued whiff before step N is 0.718 at N 60 and at N 100. There are 127 neutral-first rows. Their first valued whiff comes 79/93/102 steps after the first hold (p90 195). Agent6 (maintain) has 135 neutral-first rows. While Agent6 holds the neutral odour, the steps since the last valued whiff are p50 324, and 0.883 of those row-steps have had no valued whiff yet.
- (4) 994 of the filter's 1298 actions (0.766) come before the row's first valued whiff. The first filter action comes before it in 99/99 of the rows the filter moved into V.
- (5) Exact identity bounds (no run of a new agent):
  - Start OFF: P(V) in [0.627, 0.820] for every window N from 10 to 600 and for both thresholds (1e-3, 1e-6).
  - Start ON ('prior + window N'): N 40 [0.882, 0.973]; **N 45 to 80 [0.915, 0.973]**; 150 [0.930, 0.970]; 600 = Agent8. At N 60 the rows split as follows: 376 bitwise Agent8 throughout (V 366), 193 bitwise Agent6 throughout, 192 both, 23 neither. The share of filter actions kept (proxy) is 0.814.
  - W1, start ON, N 60: bitwise Agent8 on steps 0 to 58. The first surge is the first B whiff at or after step 59: steps 112/128/154 (389 rows). The crude dwell proxy (not a simulation) is paired minus Agent6 mean -2.62, sd 5.86.
- (1) The non-held unit's s carries no presence signal (max 0.0046). Upstream P halves every step and never reaches 0 in a run.

**Reading (interpretation).** H23's gain in this task is made in the empty state at the start, before the valued odour has been sensed. The filter acts there because the valued odour is in the read-out, not because it has been sensed. A presence scope that starts OFF removes that act for every N. A scope that starts ON keeps it for the first N - 1 steps, and that is a prior, not evidence (section 3).

## 3. The change: variant (v-p), and the relaxation it needs

**Rejected variants (recorded, not run).** (v-a) takes presence as upstream P_k > theta. (v-c) is the presence counter starting OFF. Both are structurally blocked on T1. On the H23 dev seeds their exact identity bounds put P(V) in [0.627, 0.820] for every N from 10 to 600 and for theta 1e-3 and 1e-6 (filter 0.932, maintain 0.690). This is because 0.766 of the filter's actions, and its first action in 99/99 into-V rows, come before the row's first valued whiff, when no evidence of the valued odour exists under any definition. M2(a) and M2(b) would fail with near certainty (v1 section 7: P(k >= 365) < 1e-5 at the upper bound 0.82). The owner chose (v-p) (decision:h24-design-v2-choices, point 1: '(v-p) N 60 추천 — 시작 OFF는 T1이 구조적으로 막힘.').

**The rule (v-p).** Per row and per odour k in the read-out:
- Counter c_k, integer. c_k = 0 at construction: every odour in the read-out is presumed present at step 0 (the prior). Each step, before nav: c_k <- 0 if odour k whiffs this step, else c_k + 1. So with no whiff, c_k = t + 1 at step t, and the prior keeps k present on steps 0 to N - 2. After a whiff at step s, k is present on steps s to s + N - 1 and absent from s + N.
- present_k = (c_k < N) or (k is the odour held after this step's selection). N = 60.
- h = the held odour after selection; v_k the read-out.
- v_max = max of v_k over present k. top_k = present_k and v_k >= 0 and v_k = v_max.
- nav = hit, if h >= 0 and (v_h = v_max or v_h < 0).
- Otherwise nav = any whiff of an odour k with top_k.
- If no odour is present, then there is no whiff this step and nothing is held. v_max is undefined and the filter is inert: nav = False, which is also Agent6's line (H19 (a) as adopted).

Nothing else changes: gain, gate, circuit, releases, the silence timer on hit, flee, cast, ring. The rule draws no random numbers. A held odour counts as present (v1 section 3). Without that, a held valued odour after N silent steps would leave v_max = 0 and turn the neutral whiff into a surge while the valued odour is held. In practice a valued hold ends on the timeout within 41 silent steps (RESET_AFTER 40), before c reaches 60, so the held clause binds only in edge cases. Bench (b) and M3 check this; it is not assumed.

**The code (new file ph23.py; no adopted module edited).** Agent9(Agent8) takes a flag `scope` in {'off', 'prior'} and N (default 60). In __init__ it sets `self.c = np.zeros((runs, 2))` and the measurement fields `present`, `nav8`, `differs8`. act is ph21.Agent8.act (ph21.py sha256 3a1d79d9a0d235f1bef7e435ec594cff4048180e27b28dcd892598c58413cfc1, source doc ddcec8520fcd8e23c) copied verbatim, with lines 69 to 72 replaced by:

    v = self.chan_valence(); vh = v[rows, np.maximum(h, 0)]
    top8 = (v >= 0) & (v == v.max(1)[:, None])                                                   # Agent8's line 69, measurement only
    self.nav8 = np.where((h >= 0) & ((vh == v.max(1)) | (vh < 0)), hit, (whiffs & top8).any(1))  # Agent8's lines 71-72, measurement only
    if self.scope == "prior":                                                                    # H24: the presence scope
        self.c = np.where(whiffs, 0.0, self.c + 1.0)                                              # steps since last sensed; starts at 0 (the prior)
        held = np.zeros_like(whiffs); held[rows, np.maximum(h, 0)] = h >= 0
        self.present = (self.c < self.N) | held
    else:
        self.present = np.ones_like(whiffs)
    vmax = np.where(self.present, v, -np.inf).max(1)
    top = self.present & (v >= 0) & (v == vmax[:, None])
    self.nav6 = hit | ((h < 0) & (whiffs & (v >= 0)).any(1))                                    # Agent6's line, measurement only
    keep = (h >= 0) & ((vh == vmax) | (vh < 0))
    nav = np.where(keep, hit, (whiffs & top).any(1)) if self.filt else self.nav6
    self.differs = nav != self.nav6; self.differs8 = nav != self.nav8

With scope 'off', present is all True and vmax = v.max(1), so top and keep are Agent8's lines 69 and 71 exactly, and the counter is never read. scope 'off' is therefore Agent8 bitwise.

**Identities (by reading the code; checked in M3/M4).**
- scope 'off' == Agent8 bitwise.
- 0/0, +1/+1, +1/-1: every present non-negative odour is top (equal values), or the -1 odour never qualifies (v < 0). A held odour gives hit. With nothing held, nav is any whiff of a non-negative odour, and a whiff makes its odour present. So the agent == Agent6 bitwise, which is H19 (a).
- +1/0 with the valued odour held: it is present by the held clause and v_h = v_max, so nav = hit. == Agent8 == Agent6.
- **Presence identity:** on every step on which the valued odour is present, nav == nav8 (Agent8's expression on the same state). On every step on which it is not present, nav == nav6.
- **T1 (the H21 task):** the agent is bitwise Agent8 up to the step before its first `differs8` step (a filter action while the valued odour is not present). It is bitwise Agent6 up to the step before the first step on which the valued odour is present and Agent8's nav differs from Agent6's. Predicted from Part A (5), N 60: about 376/400 = 0.94 of rows bitwise Agent8 for all 600 steps, about 0.06 departing ('neither' 23, Agent6-only 1). The share of Agent8's filter actions kept is about 0.81 (proxy).
- **W1:** A is never sensed, so c_A = t + 1 and A is present on steps 0 to 58 only. The agent is bitwise Agent8 on steps 0 to 58. From step 59, nav == nav6 (Agent6's expression, v_max over B alone). Its first surge is the first B whiff at or after step 59.
- **T3:** the agent's T3 run == its own T1 run on steps 0 to t0 - 1, because the masking is inert before t0. After the row's last valued whiff L: nav == nav8 on steps L + 1 to L + 59. Since no valued whiff follows L, nav is then False on every one of those steps. nav == nav6 from step L + 60 on.

**The relaxation (signed; decision:classification-rule-relaxed-presence-counter, H14 format: old, new, anchor).**
- Old rule (owner, H20 Stage A close; H21 design section 3): 'The rule uses the agent's own value read-out and its own hold state; no source or axis position, no sensory history beyond what the circuit already holds.' decision:h22-open-design (a) carries it as: own value read-out and own hold/circuit state; no source or axis position; no privileged sensory history.
- New rule, H24 scope only: the same, plus ONE presence counter per odour (steps since that odour was last sensed) with one fixed window N = 60. The counter STARTS at zero: every odour in the read-out is presumed present at step 0. This start is a PRIOR, recorded as such, not evidence. No other sensory history.
- Anchor: (1) the agent's existing silence counter (RESET_AFTER 40, ph11), the same kind of quantity already in the adopted agent, now kept per odour; N 60 = 1.5 x RESET_AFTER. (2) The measured plateau of the dev-seed P(V) lower bound for the start-ON counter, reached at N 45 ([0.915, 0.973] for N 45 to 80). No fly finding is claimed.
- Scope: H24 only; any wider use is a new decision.
- Signed by the owner on 2026-09-23: '(v-p) 선택 시 N 60 + 분류 규칙 완화(및 prior) 서명 필요.'
- The prior reverses option (v)'s stated premise ('an odour never sensed cannot suppress the surge') for the first N - 1 steps of a run. This is stated, not hidden.

## 4. Mechanism bench (constructed states; before any task run)

Values +1/0 unless stated; G 2; gate on. Bench seeds 20261011 (whiffs, world) / 20261012 (agent). Wilson 95 percent. Paired bootstrap 5000 resamples, seed 20261013.
- **(a) Identities (implementation):**
  - (a1) scope 'off' == Agent8 (stub and World7, 400 x 600: H, s, S, nav, since, target, positions, headings).
  - (a2) 0/0, +1/+1, +1/-1 == Agent6 (stub, both channels p 0.30, 200 steps; World7 400 x 600).
  - (a3) +1/0 with the valued odour held (channel 0 alone p 0.30, 260 steps) == Agent8 == Agent6.
  - (a4) Presence identity on World7, 400 x 600: on every (row, step), nav == nav8 where the valued odour is present and == nav6 where it is not.
  - (a5) W1 (masked World7, 400 x 600): == Agent8 on steps 0 to 58 bitwise, and nav == nav6 on every step from 59.
- **(b) Counter dynamics, exact (stub, bench seeds, 400 rows):**
  - With no whiff at all, c = t + 1 and present on steps 0 to 58 exactly.
  - One whiff on channel 0 at step 0 and silence after: c = 0, 1, 2, ..., reset to 0 on the whiff step and +1 on every other step; present on steps 0 to 59 exactly, absent from step 60.
  - After a 20-step p 0.30 burst: absent from exactly 60 steps after the last whiff.
  - A valued hold never outlasts presence in these stubs: the held clause is never the only reason the valued odour is present on a step with c >= 60 (reported count; expected 0).
  - Bar: every row exact (tolerance 0; the counter is an integer). Statistic: fraction of rows exact, lower bound >= 0.95 (1.000 by construction).
- **(c) Task-like neutral-hold start (H23 bench (b) state: neutral axis 20 downwind, heading 180, neutral hold s 2.0, 800 rows, 600 steps). REPORTED, not a gate.** Statistic: fraction of neutral-held (row, step) with the valued odour present (filter on). Prediction: the first 59 steps (about 0.10 of neutral-held row-steps), plus the steps within 60 of a valued whiff. The valued odour is sensed in about 0.48 of rows by 600, and a valued whiff ends the neutral hold within about 12 to 27 steps. The trap duration (Agent6: p50 324 steps since a valued whiff, 0.883 never) is not bridged; this is stated in advance and is not a bar. Holding valued at 600 is reported against Agent8 (H23 bench (b): 0.271) and Agent6 (0.087).
- **(d) W1 on bench seeds (masked World7, 400 rows, 600 steps): the measurement that fixes M5(b)'s bar.** Arms Agent9, Agent8, Agent6.
  - Implementation bar: the first surge in each row is the first B whiff at or after step 59 (exact, every row; lower bound >= 0.95, 1.000 by construction).
  - Measured and reported: Agent6's mean dwell within 3.0 over 600 steps (D6_W1), which enters the bar rule (M5(b)); Agent9's and Agent8's dwell; the paired Agent9 - Agent6 difference and its sd. The last two are the measured prediction that replaces v1's proxy. They do not enter the bar.
- **(e) H23's implementation bars re-run:**
  - (a4') channel 1 held by construction, both channels p 0.30, 200 steps: on every step on which channel 0 is present, nav == channel 0's whiff (lower bound >= 0.95; 1.000 by construction).
  - (c') task start, nothing held: every nav True step on which the valued odour is present has a valued whiff (>= 0.95; 1.000).
- **(f) T3 construction and T3 bar measurement (bench seeds, 400 rows, 600 steps, t0 150).**
  - Construction check, every step of every arm:
    - For t < t0 the masked world's whiffs equal an unmasked World7 twin's, placed at the same position and heading, in both columns.
    - For t >= t0 the valued column is False and the neutral column equals the twin's.
    - The wind draws are equal, and the world generator's state is equal at the end (ph22's check, with the switch).
    - Each arm's T3 run == its World7 run on steps 0 to t0 - 1 bitwise.
  - Implementation bar (Agent9): M7(a)'s exactness in every eligible row (lower bound >= 0.95; 1.000 by construction).
  - Measured for the T3 bar rule (M7(c)), Agent6 only: D6 = the mean dwell within 3.0 of the neutral source over steps 400 to 599. Reported, Agent6: S6 = the fraction of eligible rows with a neutral surge within L + 1 to L + 100 (a readability note for M7(b), which is reported; no bar). Agent9's and Agent8's values are reported and do not enter the bar.
- **No-candidate rule:** if any identity (a1 to a5, the (f) construction) is False, or any implementation bar ((b), (d), (e), (f)) fails, the rule as specified does not do what section 3 says. The tasks are then NOT run, and the design returns to the owner. (c) is reported and does not stop the tasks. (d)'s and (f)'s measurements feed the bar decisions and do not stop the tasks.

**Bar decisions between bench and development run.** After M4 passes and before the development run, two decisions record the numbers the registered rules give: decision:h24-t2-dwell-bar (M5(b)) and decision:h24-t3-bars (M7(c) only; bar_D). Each states the bench value, the resulting bar and the pass probability recomputed at the bench's measured Agent9 - Agent6 difference. The rules are fixed by this design. Changing a rule after seeing the bench is a new signed relaxation under the standing rule (old, new, anchor), made before the development run. Task numbers are never used.

## 5. Tasks, stated in full (all three required)

**T1, the H21 choice task (= H20 Run 2 task, unchanged).**
- Geometry: two sources at the same downwind coordinate, SEP 10 apart crosswind, in a 160 x 160 translated arena (walls at least 68 from either source). A wall reflects the heading and triggers the bump reflex, which flips the flee side and the cast side.
- Plume: a whiff from source k with probability 0.30 exp(-d_along / 12) per step, inside the cone 0 < d_along < 25 and |d_cross| < 1.5 + 0.25 d_along, or within 3.0 of the source; independent per source per step. Speed 0.6; reached within 3.0.
- Start: on the midline, 20 downwind, heading uniform; each plume has p 0.057 at the start.
- Balance: 2 x 2 (valued odour A/B x valued side +y/-y), 100 rows per cell, permutation seeded with world seed + 10000. The initial cast side per row comes from agent seed + 20000, the same in every arm. 600 steps, no relocation.
- Agent constants as adopted:
  - upstream n 1.5, sigma 0.05, Rmax 1.8, k 0.8, tau 2;
  - circuit 2 units, theta 1, k 12, g 2, w_i 1, tau 10, pool tau 2, noise 0.01, S_MAX 5;
  - RESET_AFTER 40, MARGIN 0.2;
  - cast period 30, MAXOFF 170;
  - turn 0.6 x error clipped at 40, plus noise 6;
  - ring RingExact tau 1, sigma 0.5, n 16;
  - gain 1 + 2 max(v, 0); the H21 gate.
- Main measure: dwell_k = steps within 3.0 of source k; choice = the larger dwell; a tie = no choice. Every row is V, N or tie.

**T2, the absent-odour world W1 (as the absent-odour check, unchanged).** World7 with the valued source's column set to False after World7 draws it (ph22.Masked). The random stream is consumed as World7's, checked against an unmasked twin every step. Only B (value 0) is present; read-out A +1 / B 0. Start: World7's (20 downwind, 5 crosswind of B, inside its cone). 600 steps, 400 rows. Plus W3 (only B, read-out 0/0) as an identity world.

**T3, the 'sensed then lost' world (new).**
- World: World7 with both sources present on steps 0 to t0 - 1. From step t0 on, the valued source's whiffs are masked exactly as in ph22.Masked: the column is set to False after World7 draws it, and the random stream is unchanged. The switch is on the run loop's step index, not on World.t. Everything else is T1's: geometry, balance, start, values +1/0, 600 steps, 400 rows, T1's seeds. So each arm's T3 run equals its T1 run before t0 (M7(d)).
- **t0 = 150.** Justification:
  - (1) The prior must have expired before the loss. At t0 > 58 every row's valued presence at t0 rests on a sensed whiff, not on the ON start; from step 59 the prior plays no part.
  - (2) Most rows must have sensed the valued odour before t0. Agent8's first valued whiff falls at 4/16/111 (quartiles), and the neutral-first rows' first valued whiff comes a median 93 steps after a first hold near step 20. This puts about 0.91 to 0.94 of Agent8/Agent9 rows as having sensed it before 150. That figure is an estimate from quartiles, because the diagnosis printed no cut at 150; bench (f) and the development run print the exact count. For Agent6 (first valued whiff 4/12/34, never in 60 rows by 600; its neutral-first rows wait a median 322 steps after the first hold) the estimate is about 0.70 to 0.75.
  - (3) 450 steps remain after the loss, and T3's dwell third (steps 400 to 599) begins 250 steps after t0.
- Eligible rows, per arm: rows with at least one valued whiff on steps 0 to t0 - 1. L = the step of the row's last valued whiff (L <= t0 - 1). Rows that never sensed the valued odour before t0 are treated separately. For Agent9 these rows are W1-like after step 58: valued not present, Agent6's expression. Their readings are reported, not gated.
- Arms: Agent9 (main); Agent8 (the cost: it never releases, by code; at +1/0 its nav on a neutral-only whiff is always False, whatever it holds); Agent6 (reference).
- The neutral whiff rate at the agent's position after the loss (the tolerance arithmetic):
  - Inside the neutral cone at the start distance (d_along 20): p = 0.30 exp(-20/12) = 0.0567 per step, so the expected wait is 17.6 steps. P(no whiff in 40 steps) = (1 - 0.0567)^40 = 0.097. A tolerance of 40 gives 0.90 of in-cone rows a neutral whiff; at the neutral source (p about 0.30) the wait is about 3 steps.
  - At the valued source, the neutral whiff rate is exactly 0. The source is 10 crosswind of the neutral axis. That is outside the neutral 3.0 disc, and outside the neutral cone, whose half-width 1.5 + 0.25 d_along stays below 10 for every d_along < LMAX 25. The two cones overlap only for 14 < d_along < 25, where the half-width exceeds 5.
  - So for a row that loses the valued odour at the valued source, the time to its next neutral whiff is a search time, not a whiff wait. No rate arithmetic predicts it, and the absolute fraction within N + 40 has no numerical prediction. This is why M7(c) is registered relative to Agent6 with a bench-derived bar, and M7(b) is reported.

## 6. Arms

| task | arm | agent | values | role |
|---|---|---|---|---|
| T1 | scoped | Agent9, scope 'prior', N 60 | +1/0 | main |
| T1 | filter | Agent8 (adopted) | +1/0 | reference for the allowed gap (M2 b); separation identity |
| T1 | maintain | Agent6 | +1/0 | floor of H23's gain (M2 c); separation identity |
| T1 | pathway-off | Agent3 (G 0, gate off) | +1/0 | floor (M1 c) |
| T1 | known-answer | Agent5 | +1/0 | ceiling (M1 d) |
| T1 | neutral | Agent9 | 0/0 | identity with Agent6 (M3; M1 a, b) |
| T1 | priority-identity | Agent9 | +1/-1 | identity with Agent6 (M3; avoidance) |
| T2 | scoped | Agent9 | W1 +1/0 | main (M5) |
| T2 | filter | Agent8 | W1 +1/0 | the measured cost, reported |
| T2 | maintain | Agent6 | W1 +1/0 | reference for the allowed gap (M5 b, d) |
| T2 | identity | Agent9, Agent6 | W3 0/0 | bitwise identity (M3) |
| T3 | scoped | Agent9 | +1/0, loss at t0 150 | main (M7) |
| T3 | filter | Agent8 | +1/0, loss at t0 150 | the cost (never releases), reported; S = 0 by code (M3) |
| T3 | maintain | Agent6 | +1/0, loss at t0 150 | reference for the allowed gap (M7 c); M7 b reported |

## 7. Criteria

General rules:
- One statistic per criterion. Wilson intervals for proportions. Paired percentile bootstrap over rows, 5000 resamples, seed 20261013. 95 percent.
- One evaluation, no extension. A group under 50 rows is unreadable.
- Aggregation: PASS if every part passes, FAIL if any fails, else INCONCLUSIVE.

The pass-probability arithmetic is H23's:
- Normal approximation. For a paired DP, the per-row difference is in {-1, 0, +1}, with a = fraction into and b = fraction out of; sd = sqrt(a + b - DP^2), se = sd / 20. The bound clears bar B when the observed DP >= B + 1.96 se.
- Predictions are Part A's dev-seed bounds taken over as rates (section 10). Where the identity with Agent8 or Agent6 fixes most rows, a and b are the counts of the 'neither' rows.

- **M1 T1 validity (else UNREADABLE):** as H23. Ties <= 0.20 in neutral, pathway-off and known-answer. Neutral side balance within [0.35, 0.65]. Pathway-off P(V | chose) within [0.35, 0.65]. Known-answer P(V) lower bound >= 0.85. Pass > 0.99.
- **M2 T1 main (scoped arm).**
  - (a) P(V), lower bound >= 0.88 (k >= 365 of 400; H23's claim).
    - Prediction 0.91 to 0.97, centre 0.94.
    - At 0.91: mean 364, sd 5.72, P(z >= 0.09) = **0.46**. At 0.94: mean 376, sd 4.75, P(z >= -2.42) = **0.992**.
    - Alternative bar 0.85 (k >= 354): 0.97 at 0.91, > 0.999 at 0.94.
    - **Recommended: 0.88.** The hypothesis says the agent keeps H23's result, and 0.88 is the claim H23 registered and passed (0.953). A 0.85 bar would let H24 pass with a P(V) that H23's own M2(a) would have failed. The 0.46 is the price at the lower edge of an exact dev-seed bound. The filter arm itself rose from 0.932 (dev) to 0.953 (eval). The joint pass probability at the lower edge is set by M5(b) anyway (below), so 0.85 buys little there.
  - (b) Allowed gap to the adopted filter: paired DP = P(V) scoped - filter, lower bound >= -0.05.
    - Lower edge DP -0.017 (a 0, b 0.0175): se 0.0066; clears when DP >= -0.0371; P(z >= 3.0) = 0.999.
    - Centre -0.005 (a 0.010, b 0.015): se 0.0079; P > 0.999.
  - (c) DP = P(V) scoped - maintain, lower bound >= +0.05. Prediction +0.21 to +0.26, so P > 0.999.
- **M3 identities (printed in the run):** section 3's identities on the task seeds:
  - scope off == Agent8;
  - neutral and priority-identity == Agent6 (and the H21 chain re-run);
  - the presence identity on every (row, step) of the scoped arm, in T1, T2 and T3;
  - separation against filter and against maintain (counts of rows bitwise equal throughout; first departure);
  - W3 == Agent6 bitwise;
  - W1: == Agent8 on steps 0 to 58, nav == nav6 from 59;
  - T3: every arm == its T1 run on steps 0 to 149, and Agent8's nav on a neutral-only whiff is False on every (row, step).
- **M4 bench (section 4):** PASS iff (a), (b), (d)'s and (f)'s implementation bars, (e) and the (f) construction all pass; (c) reported. About 1 if the implementation is correct.
- **M5 T2 W1 (scoped arm; allowed gaps to Agent6).**
  - (a) Reach within 3.0 at least once by 600, lower bound >= 0.80 (the check's 'reach kept'). Prediction 0.94 to 0.99 (Agent8 reaches in about half the rows by step 58, dev; then Agent6's tracking), so P > 0.999.
  - **(b) Dwell: paired mean dwell difference scoped - Agent6 (steps within 3.0 over 600); bootstrap lower bound >= bar_T2.**
    - **Rule (fixed now):** bar_T2 = -0.20 x D6_W1, where D6_W1 is Agent6's mean W1 dwell in bench (d) (bench seeds, 400 rows, 600 steps), rounded to 0.1 step. The number is fixed by decision:h24-t2-dwell-bar after bench (d) and before the development run. The task's own numbers are never used.
    - Why a fraction of Agent6's dwell, not Agent6's median minus k x the paired sd:
      - (1) The rule reads only the reference arm. The paired sd includes the candidate, which would let Agent9's own variability set Agent9's bar.
      - (2) A fraction ties the gap to the size of the quantity measured.
      - (3) 0.20 of Agent6's dwell is about 0.4 of Agent8's measured deficit (Agent8's dwell is about 0.51 of Agent6's: 12.36 / 24.31 at eval, 12.82 / 24.66 at dev). The criterion therefore asks Agent9 to remove at least about 60 percent of the cost the design exists to remove.
      - (4) At the dev and check values (24.66, 24.31) the rule gives -4.9: v1's intent is kept, and only its source changes from a proxy-justified number to a bench measurement.
    - Illustrative pass probability at bar -4.9 with the proxy's sd 5.86 (se 0.29; the bound clears when the mean >= -4.33): at the proxy centre -2.6, > 0.999; at -4, 0.87; at -5, 0.01. Bench (d)'s measured Agent9 - Agent6 difference replaces the proxy as the prediction, and the bar decision restates the pass probability there.
  - (c) Wall contacts per row <= 0.10 (600 steps; 0.000 for both references in the check). P > 0.999.
  - (d) Lost rows (no whiff of B in the last third): DP scoped - Agent6, upper bound <= +0.05. Prediction 0 to +0.02. At +0.02 (a 0.03, b 0.01, se 0.0100), P = 0.85; at 0, P > 0.999.
  - (e) Implementation: the first surge is the first B whiff at or after step 59 in every row (exact). Reported beside it, not a bar: the fraction of rows whose first surge falls within N + 40 = step 99. The dev first-surge quartiles 112/128/154 predict under 0.25, because by step 59 Agent8's cast has carried the agent upwind of the plume. A bar there fails by prediction; v1 recorded the same.
  - Also reported: first-reach and first-surge steps; holding B; d_along at 600; Agent8's arm as the check's cost.
- **M6 T1 lost rows (allowed gap):** (a) no whiff of either plume in the last third: DP scoped - maintain, upper bound <= +0.05. (b) Wall contacts <= 0.10 per row. Prediction as H23 (-0.01 to +0.01; 0.00 to 0.02), so P > 0.999.
- **M7 T3 'sensed then lost' (t0 150).**
  - **(a) The window, exact (Agent9, eligible rows).**
    - nav is False on every step L + 1 to L + 59: no neutral surge while the valued odour is still present by its counter.
    - The first neutral surge after L is the first neutral whiff at or after L + 60.
    - The valued odour is not held on any step >= L + 60.
    - Bar: every eligible row exact; lower bound >= 0.95 (1.000 by construction). This is the counter's window seen directly.
  - **(b) Release within N + 40: REPORTED, not a bar (owner, 2026-09-23).** S = the fraction of eligible rows with a neutral surge on a step in L + 1 to L + 100, printed per arm (Wilson). Also printed: the paired difference S_Agent9 - S_Agent6 over rows eligible in both arms and its bootstrap interval. No bar; it does not enter M7's aggregate.
    - Why not a bar: at the loss Agent9 and Agent6 are in different states (Agent9 mostly at the valued source, where the neutral whiff rate is 0; section 5), and Agent9 is structurally 19 steps later (below). A bar would measure the start-state difference, not the rule.
    - Readability note for the report: if S6 < 0.10 (Agent6's S in bench (f)), the S comparison rests on a baseline pinned near zero and the report says so (standing rule, Phase 7.3 close).
    - Tolerance 40: section 5 arithmetic (0.90 of in-cone rows at d_along 20 whiff within 40 steps).
  - **(c) Tracking the neutral odour.** Paired mean dwell within 3.0 of the neutral source over steps 400 to 599, Agent9 - Agent6, all 400 rows; bootstrap lower bound >= bar_D.
    - Rule: bar_D = -0.20 x D6, where D6 is Agent6's mean in bench (f); fixed by decision:h24-t3-bars.
    - Unreadable if D6 < 1 step (pinned baseline).
  - (d) Identity: every arm's T3 run == its T1 run on steps 0 to 149 (bitwise). Agent9 == Agent8 up to Agent9's first differs8 step (separation, as T1).
  - Reported:
    - eligible counts per arm; L quartiles; the subset with L >= t0 - 60 (the valued odour present at t0, i.e. lost by the mask);
    - never-sensed rows' readings;
    - S for all three arms (S_Agent8 = 0 by code);
    - the first-neutral-surge delay after L;
    - d_along at 600; holding the neutral odour at 600.
  - Structural expectation (not a numerical prediction): on rows in the same state at L, Agent9's S <= Agent6's. Agent6 can surge on neutral from its release (by L + 41); Agent9 cannot before L + 60, so it is blind for 19 more steps.

**Joint pass probability** (parts independent; an order of magnitude). M1 0.99 x M2 x M3 about 1 x M4 about 1 x M5 x M6 > 0.99 x M7:
- At the lower edge: M2 0.46 x 0.999 x > 0.999, and M5 > 0.999 x 0.01 (M5(b) at -5 against -4.9) x > 0.999 x 0.85. That gives **about 0.004 x p(M7)**. With M2(a) at 0.85: about 0.008 x p(M7).
- At the centre: M2 0.992, M5 about 1, which gives **about 0.97 x p(M7)**.
- p(M7) = p(M7(a)) x p(M7(c)) (M7(b) is reported and does not enter). M7(a) about 1. M7(c) has no numerical prediction (section 5: the post-loss search time is not derivable). Its pass probability is stated in decision:h24-t3-bars from bench (f)'s Agent9 - Agent6 dwell difference.
- The lower edge is dominated by M5(b) at the proxy's lower edge. Bench (d) replaces that edge with a measurement.

**H24 verdict:** PASS iff M1 to M7 all PASS. The verdict statement: 'with v_max scoped to odours present by a per-odour counter (window 60, starting ON), the agent keeps H23's result in the H21 task within 0.05 of the adopted filter and at P(V) of at least 0.88; in the absent-odour world it tracks the only odour present within the registered dwell gap of the unfiltered agent; and after the valued odour is lost it releases the neutral odour exactly 60 steps after the last valued whiff [M7(a)] and tracks it within the registered gap of the unfiltered agent over steps 400 to 599 [M7(c)].' M7(b) is reported beside the verdict and is not part of it. A statement about supplied values +1/0, G 2, C0, these three worlds, learning off; the ON start a prior under decision:classification-rule-relaxed-presence-counter.

## 8. Unreadable conditions

- M1 failing.
- Ties above 0.20 in scoped, filter or maintain.
- A cell or eligible group under 50 rows.
- M3 failing: an implementation error, fixed before the evaluation.
- M4 not run or not passed: the tasks are not run.
- decision:h24-t2-dwell-bar or decision:h24-t3-bars not recorded before the development run: the tasks are not run.
- M7(c) with a pinned Agent6 baseline (D6 < 1 step): that part is UNREADABLE, and H24's aggregate is then INCONCLUSIVE at best. (S6 < 0.10 does not make anything unreadable: M7(b) is reported; the report notes the pinned baseline.)

## 9. Seeds, sizes, order

Sizes: T1 7 arms x 400 rows x 600 steps, plus M3 reruns; T2 W1 3 arms and W3 2 arms x 400 x 600; T3 3 arms x 400 x 600. Bench (a), (b), (d), (e), (f) 400 rows; (c) 800 rows.

**Seeds (unchanged from v1):** development world 9885, agent 9985; evaluation world 1785, agent 1885; bench 20261011 / 20261012; bootstrap 20261013. Derived: 19885 / 29985, 11785 / 21885, 20271011 / 20281012 (and 30261011 / 40261012 checked). T1, T2 and T3 share the development and evaluation seeds, as the absent-odour check shared its seeds across worlds. T3 needs no new stream: sharing T1's seeds is what makes M7(d) (T3 == T1 before t0) checkable. Bench (f) uses the bench seeds.

Check done 2026-09-23 for v2:
- (1) Every file under the repository, recursive, .git and __pycache__ excluded: 137 files, pattern (?<!\d)(n)(?!\d), for all fifteen numbers above. No file contains any of them. Excluded by name: ph23.py, ph23_*.txt, h24_*.md, master_plan.md, notes/*.md. Present and excluded at the check: master_plan.md, experiments/h24/h24_design_v1.md, notes/module_boundary_outlook.md.
- (2) vinc_search in the team space for the seed numbers: no keyword match (semantic neighbours only: seed lists of other designs).
- (3) Already registered and not reused: as v1 section 9 (unchanged).

**The code's self-check (ph23.py) repeats (1) before the first run**, excluding by name ph23.py, its outputs ph23_*.txt, the H24 documents h24_*.md, master_plan.md and notes/*.md. Known limit, as recorded in H23 section 9 and v1: this document's predecessor lists the absent-odour check's seeds, so ph22.py's own seed check fails on re-run; ph21.py's already fails on absent_odour_check_design_v1.md.

**Order:**
1. The owner confirms (section 12) -> FINAL.
2. ph23.py (Agent9; T3 world as a ph22.Masked subclass with the t0 switch; no adopted module edited).
3. Self-checks.
4. Bench (M4).
5. decision:h24-t2-dwell-bar and decision:h24-t3-bars (numbers from bench (d), (f) by the registered rules).
6. Development run (operation errors only).
7. One evaluation (T1, T2, T3).
8. Report.

Nothing changes after the table.

## 10. Predictions, with the arithmetic

- **T1:**
  - The dev exact bounds at N 60 are [0.915, 0.973], i.e. -0.017 to +0.041 around the filter's 0.932. The filter arm is predicted 0.93 to 0.97 on new seeds (H23: 0.953 at eval).
  - Scoped arm P(V) 0.91 to 0.97, centre 0.94. DP vs filter -0.017 to +0.02 (centre -0.005). DP vs maintain +0.21 to +0.26.
  - About 0.94 of rows are bitwise Agent8 throughout.
- **T2:**
  - Steps 0 to 58 as Agent8: casting; about half the rows pass within 3.0 of the source.
  - The first surge comes at the first B whiff at or after step 59 (dev 112/128/154), then Agent6's navigation rule.
  - Reach 0.94 to 0.99. Paired dwell difference -1 to -5, centre -2.6 (proxy; replaced by bench (d)'s measurement before the run). Lost-row difference 0 to +0.02. Wall contacts 0.
- **T3:**
  - (a) exact by construction.
  - Eligible fraction Agent9 about 0.91 to 0.94, Agent6 about 0.70 to 0.75 (estimates from quartiles).
  - S_Agent8 = 0 exactly (by code).
  - S_Agent9, S_Agent6 and the neutral dwells: measured, no numerical prediction (section 5: the valued source lies outside the neutral plume, so the wait after the loss is a search time).
  - Structurally S_Agent9 <= S_Agent6 on rows in the same state at L. Agent9 and Agent8 are identical before t0 in about 0.94 of rows, and Agent8 is at the valued source at t0 in most of them, so the Agent9 - Agent6 comparison is between different pre-loss states (Agent6 went to the neutral source in about 0.31 of rows).
- **Bench (c):** section 4.
- **What would make the predictions wrong:**
  - For T1, the 'neither' rows (23 of 400 dev) all going one way, or the eval seeds' first-valued-whiff timing differing from dev (0.718 of rows sensed the valued odour by step 60).
  - For T2, the dwell proxy (Agent6's dwell from the first-surge step, on Agent6's own trajectory) misstating where Agent9 is at that step; bench (d) measures this before the run.
  - For T3, the estimate of eligible rows (not read at 150). A post-loss search much slower for Agent9 than for Agent6 because of the 19 extra blind steps, during which Agent8-style casting carries it further upwind (W1: Agent8's cast passes upwind of the source by step 59). Or Agent6's baseline pinned near zero, which makes M7(c) unreadable (D6 < 1) or M7(b)'s reported comparison unreadable (S6 < 0.10).

## 11. What this design does not test

- Learning (H20 Stage B). With learned values all start at 0, so the rule is inert (equal values) until one value becomes positive. After that, a 0-valued odour is ignored for the first N - 1 steps of a trial (the prior) and for N steps after each whiff of the positive one. That is the H23 filter's behaviour, including its absent-odour cost, for those stretches. Any use there is a new decision (the relaxation is H24-scoped).
- +1/+0.5; other G; other geometries or starts; other t0; a loss that ends (the valued plume returning); the timeout; any circuit change.
- A window other than 60 (the T1 bounds do not move between N 45 and 80; T3 reads only N 60).
- Whether a fly keeps such a counter: no fly finding is cited or claimed.

## 12. The owner's confirmation (2026-09-23)

The owner confirmed this section as recommended by the orchestrating assistant: '음 추천안으로 해보자' (2026-09-23). Gloss, point by point:
1. **The rule (v-p) and N 60** (section 3), with the counter convention stated there: c = 0 at construction, updated before nav; present on steps 0 to 58 with no whiff; present on s to s + 59 after a whiff at s.
2. **The relaxation:** decision:classification-rule-relaxed-presence-counter as recorded (signed 2026-09-23; old / new / anchor; H24 scope; the ON start recorded as a prior).
3. **T3:** t0 150; eligibility as written (a valued whiff before t0; never-sensed rows reported apart); **M7(a) exact and M7(c) are the bars; M7(b) (release within N + 40, relative to Agent6) is DEMOTED to a reported quantity**, because Agent9 and Agent6 are in different states at the loss (Agent9 mostly at the valued source, where the neutral whiff rate is 0) and Agent9 is structurally 19 steps later, so a bar there would measure the start-state difference, not the rule. bar_D = -0.20 x D6 from bench (f), fixed in decision:h24-t3-bars.
4. **The T2 bar-derivation rule:** bar_T2 = -0.20 x D6_W1 (Agent6's mean W1 dwell in bench (d)), fixed by decision:h24-t2-dwell-bar after bench (d) and before the development run.
5. **T1 bar M2(a): 0.88.** The other bars stay as v1: M2(b) -0.05, M2(c) +0.05, M5(a) 0.80, M5(c) 0.10, M5(d) +0.05, M6 as H23.
6. **The seeds** (section 9, unchanged): development 9885/9985, evaluation 1785/1885, bench 20261011/20261012, bootstrap 20261013; T3 shares T1's.
7. **The order:** confirm -> ph23.py -> self-checks -> bench -> decision:h24-t2-dwell-bar and decision:h24-t3-bars -> dev -> one evaluation -> report.

## 13. Self-review (2026-09-23)

- Standalone: the rule, tasks, arms, criteria, seeds and order are stated in full; v1 is needed only as history.
- **Counter convention vs the brief.** The brief says both 'c_k = 0 at step 0' and 'W1 bitwise Agent8 for steps 0 to 59'. The convention chosen here (c = 0 at construction, updated before nav) is the one the diagnosis computed ('prior + window N': sensed at step -1). It gives present on steps 0 to 58 with no whiff, so Agent8 on 0 to 58 in W1. The alternative (c = 0 after step 0's update) would shift everything by one step and leave the diagnosis's exact bounds uncomputed for the rule actually run. Stated, not hidden.
- **T3's tolerance premise.** The brief asked for the tolerance from 'the neutral whiff rate at the agent's position'. At the valued source that rate is exactly 0 (geometry, section 5), so the wait after the loss is a search, not a whiff wait. The design therefore gives the in-cone arithmetic for the tolerance (40 steps: 0.90 at d_along 20) and registers M7(b), (c) relative to Agent6 with bench-derived bars, not with an absolute bar of computable pass probability. That is a proposal beyond the owner's four points (decision:h24-t3-bars), put to the owner in section 12.
- **T3 identity (iii) as briefed ('identity with Agent8 before t0, bitwise') does not hold in every row.** Agent9 departs from Agent8 before t0 in some of the about 24 of 400 rows that are not bitwise Agent8 in T1. What holds exactly is T3 == T1 before t0 for each arm, plus the separation identity. M7(d) is stated that way.
- **The brief's T2 bar 'first surge on B within N + tolerance'** fails by prediction (dev first-surge q1 112 > 99). It is kept as a reported number, as in v1; M5(e)'s exact form is the bar.
- The held clause: a valued hold formed after L from the valued odour's residual upstream signal would end on the timeout within 41 steps, before L + 60. It is checked (bench (b), M7(a)), not assumed.
- Part A's numbers are dev-seed numbers, taken over to the evaluation seeds as rates. The counterfactual 'actions kept' is an upper-bound proxy. The identity bounds are exact for the recorded rows.
- The joint pass probability at the lower edge is about 0.004 x p(M7), dominated by M5(b) at the proxy's lower edge. Bench (d) replaces that edge with a measurement, and the bar decision restates the probability. At the centre it is about 0.97 x p(M7); p(M7) is unknown until bench (f).
- The bar rules use only Agent6's bench values. The candidate's bench values are reported and do not enter any bar. A rule change after the bench is a new signed relaxation.
- Not tested: section 11.
