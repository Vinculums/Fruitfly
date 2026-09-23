# H24 Run 2 design v1 DRAFT: the presence-scoped value filter on the release agent (Agent10), +1/0

Date 2026-09-24. Status: **v1 DRAFT, for the owner's confirmation (section 12). No code.** Opened for design by the owner on 2026-09-24 ('1 → 2(a) → 3·4·5', point 3; decision:h24-run2-open-design). Template: H24 design v3 FINAL (doc dafaa132a0267d56b, local experiments/h24/h24_design_v3.md). H24's verdict (decision:h24-closed: NOT shown, no candidate at the bench) stands and is not re-judged; H24's seeds stay registered to H24 and are not reused. H25's verdict and adoption (decision:h25-closed; decision:h25-release-adopted-within-tested-conditions, scoped by decision:release-negative-scope-on-hold: adopted at +1/0, on hold at negative values) stand. Supplied values, learning off, G 2, the H21 gate on, C0.

**What is new against H24 v3.** (1) The base agent is Agent10 (the H25 release + Agent8), not Agent8. (2) The main scope is +1/0; the +1/-1 arm is REPORTED, not part of the verdict (the release's negative-value adoption is on hold). (3) The behavioural T3 is H25's constructed loss (T3a); H24's Lost world (t0 150) is REPORTED (its span is too small to read, section 5). (4) The classification-rule relaxation must be re-signed: the H24 one lapsed with decision:h24-closed (section 3). (5) New seeds (section 9). The rule (v-p) is unchanged.

## 1. Hypothesis

**H24 Run 2: with the value filter's v_max taken only over odours present in the agent's own state (a per-odour counter of steps since last sensed, window N 60, starting ON; H24's rule (v-p), unchanged), on the agent that has the H25 release, the agent does three things at +1/0.** (i) It keeps H23's result in the H21 choice task: P(V) at least 0.88 and within an allowed gap of Agent10 [M2]. (ii) In the absent-odour world W1 it tracks the only odour present within an allowed gap of the unfiltered agent [M5]. (iii) After the valued odour is lost (T3a, H25's construction) it releases the valued hold, opens the filter exactly when the counter expires [M7(a)], and tracks the remaining neutral odour, recovering at least half of the ceiling-floor span [M7(b)]. Implementation claims are checked on constructed states first (section 4, M4).

## 2. The measured reason

- **H24's bench failed on one clause** (record:h24-bench-result; experiments/h24/ph23_bench.txt): every identity True, bars (b), (d), (e) pass, but (f) M7(a) 65/370 = 0.176 [0.140, 0.218] against 0.95. Parts: no nav on L+1..L+59 370/370; first neutral surge = first neutral whiff at or after L+60 122/370; valued not held from L+60 65/370. Cause read from the runs and the code: design v3 section 3 assumed 'a valued hold ends on the timeout within 41 silent steps'; it did not (timeout resets fired, the held unit recovered; 147,415 held-only row-steps in T3). The held clause (present_k includes 'k held') then kept the valued odour present past L+60.
- **H25 made that assumption true** (record:h25-result; experiments/h25/ph24_bench.txt): a valued hold constructed at step 0 with no input ends at step 47 in 400/400 rows ((b1), (b3); first drive at step 41, D 7), with both units at or below 1.0 and no unit above 1.0 afterwards; in H21 bench (a)'s protocol the valued hold ends 48 steps after its last whiff in 400/400 ((b4): 48/48/48). No false release in 400/400 ((c)). In the adopted agent (Agent10) the release is behaviour-inert at +1/0 (trajectory bitwise Agent8 in every row of T1, W1, T3a, T3b): the filter keeps the neutral odour from surging whatever is held. In the gate agent (Agent10g) the release is behaviourally live: T3a R 0.957 [0.895, 1.025]; T1 cost M6 -0.155 [-0.200, -0.113].
- **So the two pieces now fit.** H24's counter needs a valued hold that ends before the window; H25's release ends it at origin + 48, which is before origin + 60.
- **The absent-odour cost is still open.** In W1 Agent10's dwell equals Agent8's (12.133 at the H25 evaluation) against Agent6's 25.435 (Agent10g equal to Agent6 row for row). H24's bench (d) measured the counter there: Agent9 24.125 vs Agent6 25.835 (bench seeds 20261011/12), paired -1.71, sd 10.26.

## 3. The change: (v-p) on Agent10, and the relaxation it needs

**The rule (v-p), unchanged from H24 v3 section 3.** Per row and per odour k in the read-out:
- Counter c_k, integer. c_k = 0 at construction (the prior: every odour in the read-out presumed present at step 0). Each step, before nav: c_k <- 0 if odour k whiffs this step, else c_k + 1. With no whiff c_k = t + 1 at step t, so k is present on steps 0 to 58 by the prior; after a whiff at step s, present on s to s + 59, absent from s + 60.
- present_k = (c_k < N) or (k is the odour held after this step's selection). N = 60.
- v_max = max of v_k over present k; top_k = present_k and v_k >= 0 and v_k = v_max.
- nav = hit if h >= 0 and (v_h = v_max or v_h < 0); otherwise nav = any whiff of an odour k with top_k.
- If no odour is present, no whiff occurs this step and nothing is held; the filter is inert: nav = False (Agent6's line).
Nothing else changes: gain, gate, circuit, the H25 release (S)+(Z), the silence timer, flee, cast, ring. The rule draws no random numbers.

**The code (new file ph25.py; no adopted module edited).** Agent11 = Release (ph24.py, unchanged) + ph23.Agent9 (scope 'prior', N 60; unchanged). Nothing is copied: the class is `class Agent11(Release, Agent9)`, the same composition H25 used for Agent10 = Release + Agent8. Flags: `scope` ('off' | 'prior') and `release` (True | False).

**Why the held clause no longer binds (the arithmetic H24 v3 got wrong).** A valued hold whose last valued whiff is at L:
- the silence counter is 0 after step L; the first timeout drive fires at L + 42 (41 silent steps); the drive is sustained for D = 7 steps (H25 (b), D 7/7/7, max 7); the hold ends at L + 48 (H25 (b4): 48/48/48). A hold constructed at step 0 has its origin at -1 and ends at step 47 (H25 (b1), (b3)).
- The counter keeps the valued odour present by c < 60 through L + 59. On L + 48 to L + 59 the valued odour is present by the counter, not by the held clause, so the held clause is never the only reason for presence at c >= 60.
- After the release nothing is held or the neutral odour is; from L + 60 the valued odour is absent and the counter alone governs.
- Re-formation of a valued hold from the residual upstream signal is negligible: the upstream response halves per step without input (ph21b diagnosis (1); record:option-v-presence-diagnosis-result), so 48 steps after the last whiff it is of order 2^-48 of its peak and cannot drive the valued unit over threshold. Checked, not assumed (bench (b), (f)).
- The exceptions: a drive interrupted by the evidence release also ends the hold (earlier, not later); a valued whiff after L makes a new L. Neither keeps the valued odour held at L + 60 without a whiff.
Hence **M7(a) exact is expected at 1.000** in every eligible row (by construction of the code, as H24 v3 claimed and H24's bench refuted for the base without the release).

**Identities (by reading the code; checked in M3/M4).**
- scope 'off' == Agent10 bitwise (Agent9 scope 'off' == Agent8; the Release mixin on top).
- release False == ph23.Agent9 bitwise (H24's agent).
- 0/0 and +1/+1 == Agent10 bitwise: every present non-negative odour is top (equal values), a whiff makes its odour present, a held odour gives hit; so nav is Agent6's expression in every state, and at these values Agent8 == Agent6 (H23), so Agent11 == Release + Agent6 == Release + Agent8 = Agent10.
- **+1/-1 == Agent10 bitwise: a REPORTED identity (checked and printed; outside the verdict).** Reading the rule: the -1 odour never qualifies (v < 0 is never top), and the +1 odour is top whenever present (v_max = +1 when it is present). A +1 whiff makes it present that step; a held +1 is present by the held clause; a held -1 gives nav = hit through v_h < 0 (and the flee target). With the +1 odour absent and a -1 whiff, v_max = -1 and no odour is top: nav False, which is Agent6's line (a -1 whiff has v < 0). So in every state nav equals Agent6's expression, which at +1/-1 equals Agent8's (H23 identity). **The counter cannot change anything at +1/-1.** The known -0.160 cost of the release at negatives (record:avoidance-check-result; record:r3-negative-release-diagnosis-result) is therefore Agent10's, not the counter's, and Agent11 inherits it exactly.
- +1/0, valued held: present by the held clause and v_h = v_max, so nav = hit (== Agent10 == Agent8 == Agent6).
- **Presence identity:** on every step on which the valued odour is present, nav == nav8 (Agent8's expression on the same state); on every step on which it is not, nav == nav6.
- **T1 separation:** Agent11 == Agent10 bitwise up to the step before its first `differs8` step (a nav that differs from Agent8's expression while the valued odour is not present).
- **W1:** the valued odour is never sensed, so Agent11 == Agent10 (== Agent8 in trajectory, H25) on steps 0 to 58, and nav == nav6 from step 59.
- **T3a (constructed loss, H25):** the valued column is masked from step 0 and the valued hold s 2.0 is constructed; the counter's origin is the prior (-1). The valued hold ends at step 47; the valued odour is present by the prior through step 58; nav == nav8 on 0 to 58 (no neutral surge), nav == nav6 from 59. Agent10g surges on a neutral whiff from step 47; Agent11 from step 59: 12 steps later.

**The relaxation, to be RE-SIGNED for H24 Run 2 (H14 format: old, new, anchor).** decision:classification-rule-relaxed-presence-counter was H24-scoped and lapsed with decision:h24-closed; it stays on record. Run 2 needs its own signature before any code:
- Old rule (owner, H20 Stage A close; H21 design section 3): 'The rule uses the agent's own value read-out and its own hold state; no source or axis position, no sensory history beyond what the circuit already holds.' decision:h22-open-design (a) carries it as: own value read-out and own hold/circuit state; no source or axis position; no privileged sensory history.
- New rule, **H24 Run 2 scope only**: the same, plus ONE presence counter per odour (steps since that odour was last sensed) with one fixed window N = 60. The counter STARTS at zero: every odour in the read-out is presumed present at step 0. **This start is a PRIOR, recorded as such, not evidence.** No other sensory history.
- Anchor: (1) the agent's existing silence counter (RESET_AFTER 40, ph11), the same kind of quantity, kept per odour; N 60 = 1.5 x RESET_AFTER. (2) H24's measured dev-seed plateau of the P(V) lower bound for the start-ON counter (N 45 to 80, [0.915, 0.973]; record:option-v-presence-diagnosis-result). (3) New for Run 2: with the H25 release a valued hold ends at origin + 48 < origin + 60 (H25 (b), (b4)), so the window now outlasts the hold, which is what H24 v3 assumed and H24's bench refuted. No fly finding is claimed.
- Scope: H24 Run 2 only; any wider use is a new decision.
- The prior reverses option (v)'s stated premise ('an odour never sensed cannot suppress the surge') for the first N - 1 steps of a run. Stated, not hidden.
- Signature: **pending** (section 12, point 2). Without it the design stays a draft.

## 4. Mechanism bench (constructed states; before any task run)

Values +1/0 unless stated; G 2; gate on. Bench seeds 20261041 (world, whiffs) / 20261042 (agent). Wilson 95 percent. Paired bootstrap 5000, seed 20261043.
- **(a) Identities (implementation):**
  - (a1) scope 'off' == Agent10 (stub and World7, 400 x 600: H, s, S, nav, since, target, positions, headings, the silence counter).
  - (a1') release False == ph23.Agent9 (stub and World7).
  - (a2) 0/0 and +1/+1 == Agent10 (stub, both channels p 0.30, 200 steps; World7 400 x 600).
  - (a2') +1/-1 == Agent10 (same protocol). Printed as a reported identity; a False here is an implementation error and stops the tasks like any identity.
  - (a3) +1/0 with the valued odour held (channel 0 alone p 0.30, 260 steps) == Agent10.
  - (a4) Presence identity on World7, 400 x 600, every (row, step).
  - (a5) W1 (masked World7, 400 x 600): == Agent10 on steps 0 to 58 bitwise; nav == nav6 from 59.
- **(b) Counter dynamics, exact (stub, 400 rows, 200 steps):**
  - no whiff: c = t + 1; present exactly on 0 to 58;
  - one whiff on channel 0 at step 0, silence after: c_0 = t; the valued hold it forms ends at step 48; **channel 0 present exactly on 0 to 59, absent from 60** (H24's bench: 0/400, because the hold persisted);
  - a 20-step p 0.30 burst on channel 0: absent from exactly 60 steps after the last whiff (H24: 0/399);
  - held-only presence (the held clause the only reason for presence with c >= 60): **0 (row, step)** (H24: 105,222).
  - Bar: every row exact in every schedule; lower bound >= 0.95 (1.000 by the arithmetic of section 3).
- **(c) Task-like neutral-hold start (H23 bench (b) state; 800 rows, 600 steps). REPORTED.** Fraction of neutral-held (row, step) with the valued odour present; holding valued at 600 against Agent10 and Agent10g.
- **(d) W1 on bench seeds (400 x 600): the measurement that fixes M5(b)'s bar.** Implementation bar: the first surge is the first B whiff at or after step 59 in every row (lower bound >= 0.95). Measured: D6_W1 = Agent6's mean W1 dwell (Agent10g equals it row for row, H25 M5(b); both printed); Agent11's and Agent10's dwell; the paired Agent11 - Agent6 difference and sd (reported; they do not enter the bar).
- **(e) H23's implementation bars re-run on Agent11:** (a4') channel 1 held, both channels p 0.30, 200 steps: on every step with channel 0 present, nav == channel 0's whiff; (c') task start, nothing held: every nav step with the valued odour present has a valued whiff. Lower bound >= 0.95 each.
- **(f) T3 constructions and M7(a) with the released hold (bench seeds, 400 x 600).**
  - T3a construction (H25's, ph24.run 'T3a'): valued column False from step 0 in every step, neutral column == the unmasked twin's, wind and generator state equal; start at the valued source; s_valued 2.0 held at step 0.
  - Lost world construction (H24's, t0 150): as H24 bench (f).
  - **Implementation bar, M7(a) exact, in both worlds** (T3a: every row, origin -1; Lost: every eligible row, L = the last valued whiff before t0): nav False on every step origin + 1 to origin + 59 (T3a: 0 to 58) on which only the neutral odour whiffs; the first neutral surge after the origin is the first neutral whiff at or after origin + 60 (T3a: 59); the valued odour is not held on any step >= origin + 60; and (T3a) the valued hold ends at step 47 with both units <= 1.0. Lower bound >= 0.95 in each world (1.000 by section 3).
  - Measured and reported: T3a dwell at the neutral source 100 to 599 for Agent11, the floor (Agent10), the ceiling (Agent5 fixed to the neutral odour) and Agent10g; the span and its interval; the per-row paired sd; M7(b)'s pass probability restated at the bench's R. They do not change the bar.
- **(h) T1 on bench seeds, REPORTED (new; proposed, section 12 point 5):** Agent11 vs Agent10 in World7 +1/0, 400 x 600: P(V) each, paired DP, into/out of V, and the M2 pass probabilities recomputed at the bench's DP. **Proposed stop rule:** if the bench-seed paired DP point estimate is below -0.05, the design returns to the owner before the development run (M2(b) would be predicted to fail; section 7). No task seed is touched.
- **No-candidate rule:** if any identity (a1 to a5, the (f) constructions) is False or any implementation bar ((b), (d), (e), (f) M7(a)) fails, the rule as specified does not do what section 3 says; the tasks are NOT run and the design returns to the owner. (c) and (h) are reported ((h) with the proposed stop rule).

**Bar decision between bench and development run.** After M4 passes and before the development run, decision:h24-run2-t2-dwell-bar records bar_T2 = -0.20 x D6_W1 from bench (d) (rounded to 0.1) and the pass probability at the bench's measured Agent11 - Agent6 difference. M7(b)'s bar (R >= 0.50) is fixed here and does not move. Task numbers are never used.

## 5. Tasks, stated in full

**T1, the H21 choice task (= H24 v3 / H25 T1, unchanged).** Two sources SEP 10 apart crosswind at one downwind coordinate in a 160 x 160 arena with reflecting walls (walls at least 68 from either source; the bump reflex flips the flee side and the cast side). Plume: whiff probability 0.30 exp(-d_along / 12) inside the cone 0 < d_along < 25, |d_cross| < 1.5 + 0.25 d_along, or within 3.0 of the source. Start on the midline 20 downwind, heading uniform; 2 x 2 balance, 100 rows per cell; initial cast side from agent seed + 20000; 600 steps, 400 rows. Agent constants as adopted (H24 v3 section 5). Main measure: dwell majority; V, N or tie.

**T2, the absent-odour world W1 (unchanged).** ph22.Masked: the valued source's column False after World7 draws it; only B (value 0) present; read-out A +1 / B 0. W3 (only B, read-out 0/0) as an identity world.

**T3, the constructed loss T3a (H25's; behavioural T3).** ph22.Masked with the valued column False from step 0; the agent starts at the valued source with the valued hold constructed (s_valued 2.0); World7's heading draw; 600 steps, 400 rows, T1's seeds (ph24.run 'T3a'). Main measure: dwell within 3.0 of the neutral source over steps 100 to 599. H25's evaluation measured the span on it: ceiling 13.857, floor (Agent6 = Agent10) 0.890, span 12.967 [12.070, 13.918]; Agent10g 13.300, R 0.957 [0.895, 1.025].

**T3b, the Lost world (H24's T3, t0 150): REPORTED.** H25's T3b (the same world) measured ceiling 5.897 and floor (Agent10 = Agent8) 1.972: span about 3.9, below the readability bound 5, so a ratio there would be unreadable. It is run and printed (dwell 400 to 599 per arm; eligible rows; M7(a) exactness is bench (f)'s bar, not a task criterion), and does not enter the verdict.

## 6. Arms

| task | arm | agent | values | role |
|---|---|---|---|---|
| T1 | scoped | Agent11 (Release + Agent9, scope 'prior', N 60) | +1/0 | main |
| T1 | release-filter | Agent10 (adopted base) | +1/0 | reference for the allowed gap (M2 b); separation identity |
| T1 | release-maintain | Agent10g | +1/0 | floor of the filter's gain on this base (M2 c) |
| T1 | filter, maintain | Agent8, Agent6 | +1/0 | reported (H23 / H21 references; Agent10 == Agent8 in trajectory) |
| T1 | pathway-off | Agent3 (G 0, gate off) | +1/0 | floor (M1 c) |
| T1 | known-answer | Agent5 | +1/0 | ceiling (M1 d) |
| T1 | neutral | Agent11 | 0/0 | identity with Agent10 (M3; M1 a, b) |
| T1 | priority | Agent11 and Agent10 | +1/-1 | REPORTED: the identity (a2') printed; P(V), lost rows, wall contacts per row printed; outside the verdict |
| T2 | scoped | Agent11 | W1 +1/0 | main (M5) |
| T2 | release-filter | Agent10 | W1 +1/0 | the cost being removed, reported |
| T2 | maintain | Agent6 (and Agent10g, equal to it in H25) | W1 +1/0 | reference for the allowed gap (M5 b, d) |
| T2 | identity | Agent11, Agent10 | W3 0/0 | bitwise identity (M3) |
| T3a | scoped | Agent11 | +1/0, constructed loss | main (M7) |
| T3a | floor | Agent10 | +1/0 | floor (the filter never lets it surge on the neutral odour) |
| T3a | ceiling | Agent5 fixed to the neutral odour | +1/0 | ceiling |
| T3a | release-maintain | Agent10g | +1/0 | reported (H25's R 0.957 reference) |
| T3b | all of the above | | +1/0, loss at t0 150 | REPORTED |

## 7. Criteria

General rules (as H24 v3): one statistic per criterion; Wilson intervals; paired percentile bootstrap over rows, 5000 resamples, seed 20261043; 95 percent; one evaluation, no extension; a group under 50 rows unreadable; aggregation PASS if every part passes, FAIL if any fails, else INCONCLUSIVE. Pass-probability arithmetic H23's (normal approximation; for a paired DP with only out-of-V rows, sd = sqrt(b - DP^2), se = sd / 20).

- **M1 T1 validity (else UNREADABLE):** as H24 v3 (ties <= 0.20 in neutral, pathway-off, known-answer; neutral side balance [0.35, 0.65]; pathway-off P(V | chose) within [0.35, 0.65]; known-answer P(V) lower bound >= 0.85). Pass > 0.99 (H25: known-answer 0.943, pathway-off 194/202/4, balance 0.545).
- **M2 T1 main (scoped arm).**
  - (a) P(V), lower bound >= 0.88 (k >= 365 of 400).
  - (b) Allowed gap: paired DP = P(V) Agent11 - Agent10, lower bound >= -0.05.
  - (c) Paired DP = P(V) Agent11 - Agent10g, lower bound >= +0.05. Reported beside it: DP vs Agent6 and vs Agent8.
  - **Prediction, and why it is uncertain.** Agent10 scored 0.960 at the H25 evaluation (384/14/2). Agent11 departs from Agent10 only where the valued odour is absent by its counter while a neutral whiff arrives with nothing or the neutral odour held. With the release that now happens after every valued hold that goes silent: the hold ends at L + 48 and from L + 60 a neutral whiff surges. That is the gate agent's cost channel (Agent10g - Agent6 -0.155 [-0.200, -0.113] at H25; P(V | first hold valued) 0.710 vs 0.971), opened 12 steps later. Nothing on record locates Agent11 within [-0.155, 0]: the gate agent's cost is the lower edge (a 12-step delay that changes nothing), 0 the upper (the delay removes all of it). Nothing measured says how many of Agent10g's lost rows had their decisive neutral whiff in L + 48 to L + 59.
  - Pass probabilities at the edges. M2(a) at P(V) 0.96 (d = 0): 1.000; 0.94: 0.992; 0.93: 0.929; 0.92: 0.741; 0.91: 0.465; 0.90: 0.227; 0.805 (d = -0.155): 0.000. M2(b) (b = -DP, a = 0): at DP 0 or -0.01: 1.000; -0.02: 0.990; -0.025: 0.893; -0.03: 0.650; -0.035: 0.372; -0.04: 0.174; -0.05: 0.025; -0.155: 0.000. M2(b) passes with probability above 0.5 only if the true DP is above about -0.032. M2(c) (Agent10g 0.575): above 0.99 for any Agent11 P(V) above about 0.70.
  - This is the design's main risk, and it is stated before any code. Bench (h) measures the DP on bench seeds and, under the proposed stop rule, returns the design to the owner if it is below -0.05.
- **M3 identities (printed in the run):** section 3's identities on the task seeds: scope off == Agent10; release off == Agent9; neutral (0/0) == Agent10; priority (+1/-1) == Agent10 (printed; reported identity); the presence identity on every (row, step) of the scoped arm in T1, T2, T3a; separation against Agent10; W3 == Agent10; W1 == Agent10 on 0 to 58 and nav == nav6 from 59; T3a construction (draws, start, hold) for every arm.
- **M4 bench (section 4):** PASS iff (a), (b), (d)'s, (e)'s and (f)'s implementation bars and the (f) constructions pass; (c) and (h) reported. About 1 if the implementation is correct (section 3's arithmetic).
- **M5 T2 W1 (scoped arm; allowed gaps to Agent6).** As H24 v3:
  - (a) reach within 3.0 at least once, lower bound >= 0.80;
  - **(b) dwell: paired mean Agent11 - Agent6 (600 steps), bootstrap lower bound >= bar_T2, with bar_T2 = -0.20 x D6_W1 from bench (d)**, fixed by decision:h24-run2-t2-dwell-bar after the bench;
  - (c) wall contacts per row <= 0.10;
  - (d) lost rows (no B whiff in the last third): DP Agent11 - Agent6, upper bound <= +0.05;
  - (e) implementation: first surge = first B whiff at or after step 59, every row (exact).
  - Prediction: the release does not change W1 behaviour for the gate agent (H25: Agent10g == Agent6 in trajectory in W1), and Agent11 has Agent6's expression from step 59, so Agent11 is expected to track Agent9's W1 behaviour. H24 bench (d) on its bench seeds: Agent9 24.125 vs Agent6 25.835, paired -1.71, sd 10.26 (se 0.51); the rule's bar there was -5.2; the lower bound at the measured difference is about -2.72, so P(M5(b)) about 1.000 at that difference. At a difference of -4.0 with the same sd: about 0.65. (a), (c), (d): above 0.99 at H24's and H25's W1 numbers (reach 0.94 to 0.99; contacts 0.000; lost rows equal).
- **M6 T1 lost rows (allowed gap):** (a) no whiff of either plume in the last third, DP Agent11 - Agent10, upper bound <= +0.05; (b) wall contacts <= 0.10 per row. Prediction: Agent10's 0.000 contacts at +1/0 (H25 M2); lost rows as Agent10 to +0.02.
- **M7 T3a (the constructed loss).**
  - **(a) The window, exact (Agent11, every row):** the valued hold ends at step 47 with both units <= 1.0; nav False on every step 0 to 58 on which only the neutral odour whiffs; the first neutral surge is the first neutral whiff at or after step 59; the valued odour is not held on any step >= 47. Lower bound >= 0.95 (1.000 by section 3).
  - **(b) Tracking: R = (D_Agent11 - D_floor) / (D_ceiling - D_floor) over steps 100 to 599, floor Agent10, ceiling Agent5 fixed to the neutral odour; bootstrap lower bound >= 0.50 (rows resampled together).** Readable only if the span's lower bound >= 5.0 (H25 eval span 12.967 [12.070, 13.918]); else UNREADABLE.
  - Prediction: Agent11 behaves as Agent10g at the loss except that it cannot surge on the neutral odour on steps 47 to 58. At the H25 evaluation Agent10g's first neutral hold came at step 186/222/304 and its first arrival within 3.0 of the neutral source at 198/240/310: the neutral odour is almost never met before step 59 (the valued source lies outside the neutral whiff region). So R near Agent10g's 0.957; **range 0.85 to 0.96, centre about 0.95.** Pass probability (ph24.pass_prob_R with H25's bench per-row sd 9.545 and span 13.19): at R 0.85 to 0.96 above 0.999; at 0.70, 0.995; at 0.60, 0.66.
  - (c) Identity: every arm's T3a run satisfies the construction; Agent11 == Agent10 on steps 0 to 58 bitwise (the valued odour present by the prior on every one of them, so nav == nav8, Agent10's expression).
  - Reported: Agent10g's R beside Agent11's; the valued hold's end step; the first neutral hold and first neutral arrival steps; holding the neutral odour at 600.
- **M8 T3b (REPORTED):** neutral dwell 400 to 599 per arm, eligible counts, the span (expected about 3.9, below 5: a ratio is not read).
- **Reported, +1/-1 (outside the verdict):** the identity (a2') on the task seeds; Agent11's and Agent10's P(V), lost rows, wall contacts per row. Expected: equal to Agent10's R3 numbers on the same kind of task, the -0.160 cost being Agent10's (section 3).

**Joint pass probability** (parts independent; an order of magnitude). M1 0.99 x M2 x M3 about 1 x M4 about 1 x M5 about 1 x M6 > 0.99 x M7 (about 1 x above 0.999). **The joint is set by M2:** at d = 0 about 0.99; at d = -0.02 about 0.97; at d = -0.03 about 0.6; at d = -0.155 about 0. The record gives no centre for d (M2 above); bench (h) replaces this edge with a measurement.

**H24 Run 2 verdict:** PASS iff M1 to M7 all PASS. Statement: 'with v_max scoped to odours present by a per-odour counter (window 60, starting ON) on the agent with the H25 release, the agent keeps H23's result in the H21 task within 0.05 of that agent and at P(V) of at least 0.88; in the absent-odour world it tracks the only odour present within the registered dwell gap of the unfiltered agent; and after the valued odour is lost it releases the valued hold, opens the filter exactly when the counter expires, and recovers at least half of the ceiling-floor span.' A statement about supplied values +1/0, G 2, C0, these worlds, learning off; the ON start a prior under the re-signed relaxation. Nothing about negative values (the +1/-1 arm is reported).

## 8. Unreadable conditions

M1 failing; ties above 0.20 in scoped, release-filter or release-maintain; a cell under 50 rows; M3 failing (an implementation error, fixed before the evaluation); M4 not run or not passed (tasks not run); decision:h24-run2-t2-dwell-bar not recorded before the development run (tasks not run); the relaxation not re-signed (no code); M7(b) with a span lower bound below 5.0 (that part UNREADABLE, the aggregate INCONCLUSIVE at best).

## 9. Seeds, sizes, order

Sizes: T1 9 arms plus the +1/-1 pair, 400 x 600; T2 W1 4 arms and W3 2 arms; T3a 4 arms; T3b 4 arms (reported). Bench (a), (b), (d), (e), (f), (h) 400 rows; (c) 800.

**Seeds (new):** development world 9919, agent 9929; evaluation world 1815, agent 1915; bench 20261041 / 20261042; bootstrap 20261043. Derived: world + 10000 (cell permutation) 19919, 11815, 20271041; agent + 20000 (cast draw) 29929, 21915, 20281042; and 30261041 / 40261042 checked. T1, T2, T3a and T3b share the development and evaluation seeds (as H25).

Check done 2026-09-24 for v1:
- (1) Every file under the repository, recursive, .git and __pycache__ excluded: 157 files, pattern (?<!\d)(n)(?!\d), for all fifteen numbers above. No file contains any of them. Excluded by name: ph25.py, ph25_*.txt, h24_run2_*.md, master_plan.md, notes/*.md, viewer/* (the viewer's exported JSON carries seeds of other runs by construction). Present and excluded at the check: master_plan.md, notes/module_boundary_outlook.md, and the six files under viewer/.
- (2) vinc_search in the team space for the seed numbers: no text-chunk match; one node hit on a props token (record:h19a-result), whose files in the repository contain none of the numbers per (1).
- (3) Already registered and not reused: H24's (9885/9985, 1785/1885, 20261011-13), H25's (9896/9996, 1805/1905, 20261031-33), and every earlier registration.

**The code's self-check (ph25.py) repeats (1) before the first run** with the same exclusions.

**Order:** the owner confirms (section 12) and re-signs the relaxation -> FINAL -> ph25.py (Agent11 = Release + Agent9; no adopted module edited) -> self-checks -> bench (M4, with (h) and its stop rule) -> decision:h24-run2-t2-dwell-bar -> development run (operation errors only) -> one evaluation (T1, T2, T3a; T3b and +1/-1 reported) -> report. Nothing changes after the table.

## 10. Predictions, with the arithmetic

- **T1:** Agent10 0.93 to 0.97 (H25 eval 0.960; H23 0.953). Agent11 - Agent10 in [-0.155, 0], no centre on record (section 7 M2). Agent10g 0.55 to 0.75 (H25 0.575). About 0.94 of rows were bitwise Agent8 under H24's counter on the base without release (H24 dev bound); with the release more rows can depart (every silent valued hold now ends), so fewer rows are expected bitwise Agent10; how many is not on record.
- **T2 W1:** Agent11 as Agent9 in H24's bench (d) (dwell about 24 against Agent6 about 25 to 26; Agent10 about 12); reach 0.94 to 0.99; contacts 0.
- **T3a:** M7(a) exact; R 0.85 to 0.96 (centre 0.95); floor 0.8 to 1.0 (H25 0.890 eval, 0.750 bench); ceiling about 13.9.
- **T3b (reported):** span about 3.9, unreadable as a ratio; Agent11 between Agent10 (about 2.0) and Agent10g (about 6.8).
- **+1/-1 (reported):** Agent11 == Agent10 bitwise; P(V) and lost rows Agent10's.
- **What would make the predictions wrong:** for T1, the gate agent's cost channel carrying over in full (d near -0.155) or the 12-step window removing more than expected; for T3a, Agent11's 12 blind steps coinciding with neutral whiffs in more rows than Agent10g's first-neutral timing suggests; for W1, the release changing Agent11's post-59 behaviour (the gate agent's identity in W1 says it should not).

## 11. What this design does not test

Learning (H20 Stage B); negative values (on hold, decision:release-negative-scope-on-hold; the +1/-1 arm is reported only); +1/+0.5; other G, other geometries, starts or t0; a window other than 60; another RESET_AFTER or D; the wall reflex (the R3 diagnosis found it carries the base's +1/-1 outcome in part: record:r3-negative-release-diagnosis-result; at +1/0 the release agents touch no wall, H25 M2 contacts 0); cold-start search (H17); whether a fly keeps such a counter (no fly finding is cited or claimed).

## 12. What the owner confirms

1. **The base and scope:** Agent11 = Release + Agent9 on Agent10's lineage, +1/0 main; +1/-1 reported (identity printed, outside the verdict).
2. **The relaxation, re-signed for H24 Run 2** (section 3: old / new / anchor; scope H24 Run 2 only; the ON start recorded as a prior). Proposed text for the signature: 'H24 Run 2 한정: 냄새별 presence counter 1개(N 60, 시작 ON = prior) 허용, 분류 규칙 완화 재서명.' (to be given in the owner's own words).
3. **T3:** T3a (H25's constructed loss) as the behavioural T3; floor Agent10, ceiling Agent5 fixed to the neutral odour; R >= 0.50, readable if the span's lower bound >= 5; M7(a) exact; T3b (Lost, t0 150) reported (span about 3.9).
4. **The T2 bar rule:** bar_T2 = -0.20 x D6_W1 from bench (d), fixed by decision:h24-run2-t2-dwell-bar before the development run; the other bars as H24 v3 (M2(a) 0.88, M2(b) -0.05, M2(c) +0.05 now against Agent10g, M5(a) 0.80, M5(c) 0.10, M5(d) +0.05, M6 as H23).
5. **Bench (h) and its stop rule (the design's main risk):** T1 on bench seeds, reported; if the paired DP Agent11 - Agent10 point estimate is below -0.05 the design returns to the owner before the development run. Alternative: no (h), accepting that the joint pass probability is set by an unmeasured d in [-0.155, 0].
6. **The seeds** (section 9): development 9919/9929, evaluation 1815/1915, bench 20261041/20261042, bootstrap 20261043.
7. **The order** (section 9).

## 13. Self-review (2026-09-24)

- Standalone: rule, identities, bench, tasks, arms, criteria, seeds and order are stated; H24 v3 is needed only as history.
- **The brief's 'release at L + 47 < L + 60' and '13-step delay'.** H25 measures the end of a hold at step 47 when it is constructed at step 0 (origin -1, (b1)/(b3)) and at 48 steps after the last whiff in the H21 bench protocol ((b4): 48/48/48). The counter's origin is the same step as the whiff (c = 0 on the whiff step), so the release comes at L + 48 and the window closes at L + 60: 12 steps apart, not 13. In T3a the release is at step 47 and the prior's window closes after step 58: also 12 steps. Stated with H25's numbers, not the brief's.
- **The +1/-1 claim is read from the rule, not assumed:** the -1 odour never qualifies and the +1 odour is top whenever present, so the counter cannot change nav in any state; (a2') checks it.
- **T1 is the weak point, and it is not hidden.** The release that makes M7(a) exact is the same release that costs the gate agent -0.155 in T1; the counter re-opens that channel 12 steps after a silent valued hold ends. No recorded number places Agent11's T1 cost; section 7 gives the pass probability at both edges and section 12 point 5 proposes a bench-seed measurement with a stop rule. The owner may prefer to accept the risk.
- **The T3a floor is Agent10, not Agent6.** Both scored 0.890 at the H25 evaluation (Agent10 bitwise Agent8 in trajectory), so the span is H25's; Agent10 is the arm Agent11 is built on, which makes the ratio read the counter's contribution on this base.
- **T3b demoted to reported:** its H25 span (5.897 - 1.972, about 3.9) is below the readability bound; a bar there would be unreadable by prediction.
- M2(c) is registered against Agent10g (the same base without the filter) rather than Agent6; Agent6 is reported. This follows H24 v3's logic (the floor of the filter's gain on the agent's own base).
- The bar rules use only reference arms' bench values; the candidate's bench values are reported. A rule change after the bench is a new signed relaxation.
- Not tested: section 11.
