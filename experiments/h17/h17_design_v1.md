# H17 design v1 DRAFT: cold-start and reacquisition search (a navigation hypothesis)

Date 2026-09-24. Status: **v1 DRAFT, for the owner's confirmation (section 12). No code.** Opened for design by the owner on 2026-09-24 ('일단 fruit fly 제안 추천에맞게 진행하고 laya는 추후 전달'; decision:h17-open-design), after H24 Run 2 was closed at its bench stop (decision:h24-run2-closed), in the registered order H24 Run 2 -> H17 -> H20 Stage B (decision:priority-h24run2-h17-stageb). Template: H24 Run 2 design v2 FINAL (doc d65589bd43383a57c) and H25 design v2 FINAL (doc dce297e76390fa854). Concept: concept:h17-cold-search. **This is a NAVIGATION hypothesis.** It adds a search mode to the target heading only; selection, the gate, the filter, the release, the flee and the ring are untouched, and the agent is bitwise the adopted agent on every row in which the mode never engages. Supplied values, learning off, G 2, the H21 gate on, C0. Code citations are repo-relative path:line at the commit this design was written on (eb78bb2); sha256 prefixes: ph9.py 7699b4e6, ph11.py e80f40bd, ph12.py e1035e09, ph12b.py ec6b1896, ph13.py 2d75fae8, ph16.py 33d5fdb2, ph19.py 00c6a3b3, ph21.py 3a1d79d9, ph24.py f344f178, ph22.py 03ab8c47.

## 1. Hypothesis

**H17: an agent that, after a registered silence of S steps with nothing held and no whiff of any odour, replaces the return cast's target with a crosswind cast of growing amplitude slanted slowly along the wind, finds a plume from an odour-free position outside it where the adopted agent does not, and leaves the adopted behaviour unchanged wherever a whiff arrives within S.** Concretely, at +1/0 and +1/-1 on Agent10 (the adopted agent, H23 filter + H25 release): (i) from constructed odour-free starts at the R3 stranded positions it senses a plume and reaches a source in a registered fraction of rows against the adopted agent's floor [bench (c)]; (ii) it does not engage during normal tracking in the H21 task [bench (d); T1]; (iii) in the +1/-1 stranded condition it recovers stranded rows without resting on the wall reflex [T3]. Implementation claims are checked on constructed states first (section 4).

## 2. The measured reason, and what the current navigation actually does

**What the code does now (Agent10 = Release + Agent8; ph24.py:66; the target is Agent8's, ph21.py:72-82).**
- nav = hit on the held odour, or, with nothing held, a whiff of a top-valued non-negative odour (ph21.py:72). `since` resets on nav only (ph21.py:75); `silence` resets on a hit of the held odour (ph21.py:76). A negative whiff, a filter-blocked whiff and any whiff while a non-top odour is held do not reset `since`.
- Target: nav -> UPWIND 180 (ph21.py:79; ph9.py:33); otherwise the return cast, side = cast_sign x (+1, -1) flipping every CAST_PERIOD 30 steps (ph21.py:77; ph9.py:40), offset off = MAXOFF (1 - |(since / SAT) mod 2 - 1|), a triangle wave 0 -> 170 -> 0 with period 2 SAT = 283.3 steps (ph21.py:78; SAT = MAXOFF / CAST_GROW = 141.7, ph12.py:29). A negative hold overrides with the flee side 90 / 270 (ph21.py:80). turn = clip(0.6 angdiff(target, estimate), +-40) + 6.0 N(0, 1) (ph21.py:81-82; ph9.py:41). Speed 0.6 per step (ph9.py:31). The wall reflex flips flee_side and cast_sign on a contact (ph11.py:130-141).
- The plume (ph11.py:74-84): a whiff only inside the cone 0 < d_along < 25, |d_cross| < 1.5 + 0.25 d_along, or within 3.0 of the source, with probability 0.3 exp(-d_along / 12). Crosswind extent 3.0 at the source, 15.5 at LMAX 25. Nothing upwind of a source (d_along < -3) or beyond d_along 25 is ever sensed. The wind is sensed every step (World2 p_wind 1.0, ph11.py:86), so the ring's cue-loss leak (H18) is not in play in these worlds.

**The path the return cast produces from an odour-free position (arithmetic, exact heading, no turn noise, integrating ph21.py:77-79; not run).** Along-wind velocity -0.6 cos(off); crosswind velocity -+0.6 sin(off) with the side flipping every 30 steps.
- Along-wind: upwind while off < 90, downwind while off > 90. Integral from off 0 to 90 (since 0 to 75.0): -0.6 sin 90 / 0.020944 = **-28.6** (upwind); from off 90 up to 170 and back to 90 (since 75.0 to 208.3): +0.6 x 2 (1 - sin 170) / 0.020944 = **+47.4**; since 208.3 to 283.3: -28.6. Net per cycle **-9.8** (the drift concept:h17-cold-search records as 'about 10 units upwind per cycle'). Position relative to the start of the silence: -28.6 at since 75, **+18.8 at 208**, -9.8 at 283, -38.4 at 358, +9.0 at 492, -19.6 at 567.
- Crosswind: the 30-step leg integrals 0.6 integral sin(off) are 5.5, 14.3, 17.7, 14.3, 6.3, 10.9, 17.0, 16.6, 9.9, 2.8 over since 0 to 300 with alternating sign: positions -5.5, +8.8, -8.9, +5.4, -0.9, +10.0, -7.0, +9.6, -0.3, +2.5. **The crosswind excursion stays within about +-10 of the start line and does not grow from cycle to cycle** (the side period 60 and the triangle period 283.3 are incommensurate; the pattern shifts, its amplitude does not).
- So the cast samples a strip about 20 wide crosswind and about 47 long along the wind, sliding about 10 upwind per cycle. The plume is at most 15.5 wide.

**Why it fails to re-enter, per recorded state.**
- **The stranded state after a release (R3; record:r3-negative-release-diagnosis-result; experiments/avoidance_check/r3_diagnosis.md section 1.1).** At the drive release the agent is outside both whiff regions in 131/131, 20.7/24.5/26.6 from the nearest (max 28.4), |d_cross| 26.1/29.0/30.9 to the nearer axis, d_along 4.9/11.1/13.8. From there no whiff arrives in the rest of the run in 131/131 (181 to 528 steps remain); 116/131 = 0.885 of these rows end lost. The strip's +-10 cannot bridge a crosswind gap of 26-31 minus the cone's half-width at d_along 5-14 (2.7 to 5.0), i.e. 21-28 units. The same shape in the 64 rows moving out of V (section 1.3: 19.8/24.6/26.7 from the nearest region, whiff to the end 1/64).
- **Where the adopted agent is when odour-free (R3 section 1.4).** Agent10, nothing held >= 60 steps, 101,207 (row, step): inside a whiff region 0.066; distance outside 8.8/18.5/26.6; d_along -12.2/0.3/25.0, upwind of both sources 0.496, beyond the cones' far end 0.250. Both halves of the along-wind loop above are visible: half the odour-free time upwind of the sources, a quarter beyond LMAX.
- **The absent-odour drift (record:absent-odour-check-result).** In W1 Agent8 never surges (the filter), casts throughout, reaches by casting past the source 344/400, and ends upwind of it (median -63.4 at 1800 steps, 111 rows at the wall): the net -9.8 per cycle, accumulated.
- **The cold-start clause (H16 Run 2, doc d74aba218d183d57e; experiments/h16/ph12b_h16r2.txt lines 54, 92, 135).** From a uniform odour-free start in the 40 x 40 frame (ph12.py:50-53) translated inside walls 160 apart, the return rule reached the source in **52.0 percent** (walls) and **49.5 percent** (no walls) over 5400 steps, against K3's 75; the random walk reached 52.5 (walls). K3 FAIL; the return rule was adopted for cue-every-step tracking and reacquisition only, cold search deferred to H17 (decision:h16-close-limited-adoption). Reading (not measured): starts within about 10 + the cone's half-width of an axis and within the loop's along range are found; the others are not.
- **The absorbing state the return cast replaced (H15 Run 1, doc df06694876045671d; Phase 7.3, doc dfcc4a911f3760870).** The saturating cast (off = min(170, 1.2 since)) holds the target at 10 / 350 degrees after 141.7 silent steps, i.e. nearly downwind for good; 92 percent of agents were absorbed at the downwind wall. Any search whose along-wind motion is one-way downwind reproduces it.
- **Short losses work.** H16 Run 2's long-loss reacquisitions (since > 142 at the whiff; ph12.py:143) have total silence median 153, **p90 204 (W-cone) and 208 (W-lost)** (ph12b_h16r2.txt lines 32, 62): the cast's own return pass, which ends at since 208.3 (the downwind-most point of the loop, above). That behaviour must stay untouched.
- **The wall confound (R3 section 1.2).** Agent8's recovery in +1/-1 rests partly on the reflex: P(V | wall contact) 86/106 = 0.811 vs 284/294 = 0.966 without; the whole 64-row P(V) gap sits in its 106 contact rows; all 123 contacts while holding the negative odour. A search must be judged without that crutch.

## 3. The change: a search mode on the target, and the relaxation it needs

**Candidates (evaluated from the code and the record; one chosen).**
- **(i) CHOSEN: a crosswind cast of growing amplitude, slanted along the wind, the slant reversing on a fixed clock.** It widens exactly what the return cast does not widen (the +-10 strip, section 2) and keeps an along-wind excursion in both directions (the loop is needed: half the odour-free time is upwind of the sources, a quarter beyond LMAX, R3 section 1.4). Fly grounding, RECALLED, not verified against the papers in this session: flies that lose an odour plume cast crosswind (van Breugel and Dickinson 2014, in flight) and odour offset increases turning and crosswind excursions (Alvarez-Salvado et al 2018, walking); both are cited by ph9.py:9-10. A growing amplitude is a design choice, not a claimed fly finding.
- (ii) rejected: a downwind drift with crosswind zigzag. At S the agent sits at the loop's downwind-most point (+18.8 from the loss point; about +43 from a release point, section 3 geometry), so a one-way downwind drift leaves the cones' far end and reproduces H15's downwind-wall absorbing state; its downwind leg is kept as the second half of (i)'s slant cycle.
- (iii) rejected: return to the last-whiff heading by dead reckoning. The heading at the last whiff is the surge target, upwind (ph21.py:79), which the cast already takes; returning to the last-whiff position needs a position integrator the agent does not have (the ring holds heading only), and the ring leaks under cue loss (concept:ring-leaks-under-cue-loss, H18).
- (iv) rejected: a Levy-like random search. It needs randomness beyond the agent's turn noise and has no fly grounding in the project's record.

**The rule (Search, on the target only).** Per row, with the agent's own state:
- q = steps since the last whiff of ANY odour: q <- 0 if any channel whiffs this step, else q + 1; q = 0 at construction. **New state (relaxation below).**
- engaged = search and q >= S and nothing held after this step's selection (h < 0). q >= S >= 1 implies no whiff this step, so nav is False and the adopted target on that step is the return cast (never the surge, never the flee: the flee needs a negative hold).
- Search clock u = q - S (0 on the first engaged step). Leg k = 1, 2, 3, ... lasts 30 k steps (CAST_PERIOD x k; boundaries at u = 30, 90, 180, 300, 450, 630). Side sigma_k = cast_sign x (+1 for odd k, -1 for even k); cast_sign is the agent's own, flipped by the wall reflex (ph11.py:141), so a contact reverses the current leg.
- Slant alpha = +1 (upwind) for (u mod 720) < 360, -1 (downwind) otherwise; gamma = 15 degrees.
- Search target = (UPWIND + sigma_k (90 - alpha gamma)) mod 360. With alpha +1: 180 +- 75 (crosswind with an upwind component); with alpha -1: 180 +- 105 (crosswind with a downwind component).
- On engaged steps tgt is the search target and the turn is recomputed from it with the SAME noise sample; on every other step the adopted turn is untouched. Mode off on the first whiff of any odour (q = 0); the return cast then resumes at its current `since` (never reset by the search). No random numbers are drawn; no selection, gate, filter, release, silence, flee or ring state is read or written except cast_sign (read).

**The geometry, in the world's units (exact heading, no noise).** Crosswind speed 0.6 cos 15 = 0.580, along-wind 0.6 sin 15 = 0.155 per step.
- Zigzag extremes relative to the engagement line: +17.4, -17.4, +34.8, -34.8, +52.2, -52.2 at u = 30, 90, 180, 300, 450, 630. The strip reaches +-34.8 by u = 300 (the return cast: +-10, never growing).
- Along-wind: 0.155 u upwind for u < 360 (55.9 units at 360), back to 0 at 720.
- Against the plume: the widest cone is 15.5; at the R3 positions the gap to bridge is 21-28 crosswind (section 2), inside the +-34.8 of legs 3 and 4.
- Detection per crossing at crosswind speed 0.58 (cone width w = 3 + 0.5 d_along, whiff probability 0.3 exp(-d / 12)): P(at least one whiff) = 0.88 at d_along 5, 0.85 at 10, 0.80 at 15, 0.73 at 20, 0.66 at 24.
- **Where the agent is at engagement.** For a loss while tracking (since = q from 0): the loop's downwind-most point, +18.8 from the loss point at since 208.3; the upwind slant then brings it back through the cone's along range. For an R3-type release (flee about 40-50 silent steps, then the cast from since about 45): the integral of -0.6 cos(off) from since 45 to 210 is about +43 units downwind of the release point, i.e. d_along about 48-57, beyond LMAX; the upwind slant reaches d_along 25 at u about 150-205 and d_along 0 at u about 310-370, the span in which legs 4 and 5 (amplitude +-34.8 to +52.2) sweep. Not measured; bench (c) records the engagement positions.
- **Walls (160 x 160, walls >= 68 from each source, ph16.py:259).** An R3-type agent is about 26-41 crosswind beyond a source, so >= about 27-42 from the side wall; legs 5-6 (+-52.2) can reach it. Contacts are counted and barred (T3 (c)); the open-plane bench has walls off (World3.move honours `walls`, ph12b.py:53; World4 sets it True, ph13.py:39).

**S = 210, and why.** The return cast's downwind return pass ends at since 208.3 (off back to 90, ph21.py:78 with SAT 141.7); H16 Run 2's long-loss reacquisitions have p90 204 and 208 (section 2). S 210 therefore lets the adopted cast finish its own reacquisition pass and engages at the loop's downwind-most point. With the H25 release a hold ends 48 steps after its odour's last whiff (H25 (b4): 48/48/48), so for Agent10-based arms nothing is held at q >= 49 and the 'nothing held' clause binds only if a hold persists (checked, bench (b)). The caller's proposal RESET_AFTER + SAT = 181.7 (about 180) is the alternative in section 12: it engages before the cast's return pass completes, in the stretch 180-208 where some of H16's long-loss reacquisitions happen (between 10 and 50 percent of them: only the median 153 and p90 204-208 are on record).

**The code (new file ph26.py; no adopted module edited).** `class Search` mixin wrapping act (the H25 Release pattern, ph24.py:47-63): calls super().act, updates q from this step's whiffs, and on engaged rows only replaces tgt and recomputes turn = clip(0.6 angdiff(tgt, est), +-40) + (the base's noise sample, recovered as turn - clip(0.6 angdiff(tgt_base, est), +-40)); last_turn and tgt updated on those rows only. `Agent12(Search, Agent10)` (the main arm), `Agent12g(Search, Agent10g)` (reported). Flag `search` (True | False); constants S 210, L0 = CAST_PERIOD, gamma 15, U1 360. Measurement fields: q, engaged, u, leg.

**Identities (by reading the rule; checked in section 4).**
- search False == Agent10 bitwise (the mixin returns super().act untouched); Agent12g search False == Agent10g.
- **Row identity:** in any row where q never reaches S with nothing held, Agent12 == Agent10 bitwise on every field (no draw, no state write on non-engaged steps). In particular every row in which a whiff of any odour arrives at least every S steps.
- **Chains:** 0/0, +1/+1, +1/-1 (search False) == Agent10; with search True, the never-engaged rows are bitwise Agent10 in each chain.
- **Stub (p per channel):** P(no whiff of either channel for 210 steps) = (1 - p)^420: at p 0.057 about e^-24.7, at 0.30 about e^-150; the mode is never engaged, so the stub is bitwise Agent10.
- **Not identical:** rows that engage, from the first engaged step on. This is the change being tested.

**The relaxation, to be SIGNED before any code (H14 format: old, new, anchor).**
- Old rule (the owner's standing rule for H17, carried by the opening brief; the classification rule of H21-H25 for selection-side mechanisms, decision:h22-open-design (a)): the mechanism uses the agent's own state only - wind direction (sensed), heading (ring), the cast clock `since`, the silence counter, the hold state; no source or axis position; no privileged history.
- New rule, **H17 scope only**: the same, plus ONE counter q = steps since the last whiff of any odour (q = 0 at construction; reset on any whiff), and the search clock u = q - S derived from it (no second variable). No position, no heading or position memory at the last whiff, no per-odour history.
- Anchor: (1) the same kind of quantity as the two existing timers, kept deliberately separate (ph11.py:118-126): `since` counts from the last nav event and so is blind to filter-blocked and negative whiffs (ph21.py:72, 75), `silence` counts from the last hit of the held odour (ph21.py:76); q is the whiff-driven counterpart of `since`. (2) The lapsed H24 counters were per odour (c_k); q is one number, the minimum over odours of c_k. (3) No fly finding is claimed for q.
- The no-new-state alternative (section 12 point 2): engage on since >= S and nothing held. It needs no signature but engages inside a plume whose whiffs do not steer (W1's B plume under the filter; a negative plume with nothing held), which the owner's constraint (d) excludes.
- Scope: H17 only; any wider use is a new decision.

## 4. Mechanism bench (constructed states; before any task run)

Bench seeds 20261051 (world, whiffs) / 20261052 (agent); bootstrap 5000, seed 20261053. Wilson 95 percent. 400 rows unless stated.
- **(a) Identities (implementation):** (a1) search False == Agent10 (stub both channels p 0.30, 200 steps; World7 +1/0, 400 x 600; all fields: H, s, S, nav, since, silence, target, positions, headings); Agent12g False == Agent10g. (a2) search True: every never-engaged row bitwise Agent10 (World7 +1/0 and +1/-1; W1; T3a); the stub bitwise Agent10 (never engaged). (a3) chains 0/0, +1/+1, +1/-1 as section 3.
- **(b) Engagement exact (stub world Still, 400 rows, 800 steps; schedules: one whiff at step 0 then silence; a 20-step p 0.30 burst then silence; silence from construction):** engaged exactly from the step with q = S (step 210 after construction with no whiff; S steps after the last whiff) to the step before the next whiff; off exactly on a whiff step; u, leg index and slant equal the formula (boundaries 30, 90, 180, 300, 450, 630; slant flips at 360, 720); the target equals the search target on every engaged step and the adopted target on every other; steps with q >= S and a hold: counted (expected 0 for Agent12, by H25 (b4)). Bar: every row exact; lower bound >= 0.95.
- **(c) Cold start (constructed odour-free starts; walls OFF as the primary reading, walls ON reported with contacts; values 0/0 so any whiff steers; nothing held):**
  - (c1) **R3 stranded state.** Two sources as World7; start at d_along uniform [5, 14], |d_cross| to the nearer axis uniform [26, 31] on the outer side of a random source (R3 section 1.1), heading uniform; since = q = 45 (the release state: about 40-50 silent steps of flee); engagement at step 165. Measured: (i) any whiff in steps 165-464 (300 steps after engagement); (ii) a source reached (within 3.0) by step 765 (600 after engagement); the engagement position (d_along, d_cross).
  - (c2) **Upwind of the sources (W1's drift).** d_along uniform [-60, -20], |d_cross| to the midline <= 10; since = q = S (already silent). Reported.
  - (c3) **H16's cold-start square.** Uniform in a 40 x 40 square placed on the source pair as H16's frame placed its source (x from x_src - 11 to x_src + 29, y within +-20 of the pair's midline), redrawn while inside either whiff region (ph12.py:50-53's rule); since = q = 0. Reached ever by 600 and 1800 steps. Reported (H16's 52.0 / 49.5 were a single source over 5400 steps).
  - Arms: floor Agent10 (the same construction); Agent12; **ceiling: an oracle given the direction to the nearest point of the nearest whiff region** (target = that bearing until the first whiff, then the adopted rule; a ceiling arm only, like known-answer).
  - **Bars (c1, walls off):** (i) whiff within 300 after engagement, lower bound >= 0.40; (ii) reach within 600 after engagement, lower bound >= 0.30; (iii) paired DP (i) Agent12 - Agent10, lower bound >= +0.30. Floor measured, not assumed (R3: 0/131 whiffs after stranding).
- **(d) No false engagement.** First the gap distribution: the longest any-odour silence per row and the fraction of (row, step) with q >= 150, 180, 210, 250 for Agent10 in T1 (World7 +1/0 and +1/-1, 400 x 600) and in the stub at p 0.057 and 0.30. Bar: T1 +1/0, fraction of rows with any engaged step, upper bound <= 0.05. (The H24 N sweep's 150-200-step silences were valued silences while the neutral plume was sensed, experiments/h24/h24_run2_nsweep.md section 4 (b); q resets on the neutral whiffs, so they are not q silences. Measured here, not assumed.)
- **(h1) T1 on bench seeds, the stop rule.** Agent12 vs Agent10, World7 +1/0, 400 x 600: P(V) each, paired DP, engaged rows, into / out of V; T1 (b)'s pass probability at the bench DP by section 7's arithmetic. **Stop rule: pass probability below 0.5 -> the run stops after the bench record and returns to the owner.**
- **(h2) T3 on bench seeds, the stop rule.** Agent12 vs Agent10, World7 +1/-1, 400 x 600 (ph24.run 'T1' at (+1, -1), bench seeds): lost-row DP, P(V) DP, contacts per row; T3 (a)'s pass probability at the bench DP. **Stop rule: below 0.5 -> stop and return to the owner.**
- **No-candidate rule:** any identity (a) False, (b) not exact, or a (c1) bar failing -> the search does not do what section 3 says; tasks NOT run; the design returns to the owner. (d) failing -> tasks not run (the mode would change normal tracking). (h1), (h2): the stop rules above. (c2), (c3), walls-on readings: reported.

## 5. Tasks, stated in full

- **T1, the H21 choice task (as H24 Run 2 / H25 T1, unchanged).** World7: two sources SEP 10 apart crosswind, 160 x 160 with reflecting walls >= 68 from either source, start on the midline 20 downwind, heading uniform, 2 x 2 balance, initial cast side from agent seed + 20000, 400 x 600, +1/0. Measure: dwell majority (V, N, tie).
- **T2, the absent-odour world W1 (unchanged; ph22.Masked).** The valued column False; only B (value 0) present; read-out +1/0; 400 x 600. Measure: dwell within 3.0 of B's source.
- **T3, the +1/-1 stranded condition (the avoidance check's R3 run, new seeds).** T1's world at supplied values +1/-1 (ph24.run 'T1', (+1, -1)). Measures: P(V) (dwell majority), lost rows (no whiff of either plume on steps 400-599), wall contacts per row; stranded rows (a drive-ended negative hold, as R3) and their post-release whiffs.
- **T4, the constructed loss T3a (H25's; reported).** Valued column False from step 0, start at the valued source with a valued hold constructed, 400 x 600. Measures: dwell within 3.0 of the neutral source (100-599) and distance to the valued source over time. Agent12's filter never lets the neutral odour steer (Agent10's line); the question is only whether search returns it to the source region instead of drifting. The filter's blindness to the neutral odour is H24's question, not H17's.

## 6. Arms

| task | arm | agent | values | role |
|---|---|---|---|---|
| T1 | search | Agent12 (Search + Agent10) | +1/0 | main (regression) |
| T1 | base | Agent10 | +1/0 | reference; row identity |
| T1 | search-gate | Agent12g, Agent10g | +1/0 | reported |
| T2 | search | Agent12 | W1 +1/0 | main (regression + reported gain) |
| T2 | base / reference | Agent10 (floor 11.9 bench, H24 Run 2), Agent6 (24.4) | W1 +1/0 | floor / reported reference |
| T3 | search | Agent12 | +1/-1 | main |
| T3 | base | Agent10 | +1/-1 | floor (R3: 0.765, 127 lost) |
| T3 | wall-reflex base | Agent8 | +1/-1 | reference (R3: 0.925, 33 lost, 0.307 contacts) |
| T3 | search-gate | Agent12g, Agent10g | +1/-1 | reported |
| T4 | search, base, ceiling | Agent12, Agent10, Agent5 fixed to the neutral odour | +1/0 | reported |

## 7. Criteria

General rules (as H24 Run 2): one statistic per criterion; Wilson intervals; paired percentile bootstrap over rows, 5000 resamples, seed 20261053; 95 percent; one evaluation; a group under 50 rows unreadable; aggregation PASS if every part passes, FAIL if any fails. Pass probabilities by the normal approximation: a proportion bar at n 400, P = Phi((p - theta) / se - 1.96), se = sqrt(p (1 - p) / 400); a paired DP with discordant fraction b, sd = sqrt(b - DP^2), se = sd / 20.

- **B bench (section 4):** PASS iff (a), (b), (c1)(i)-(iii) and (d) pass, and neither stop rule fires.
  - (c1)(i) bar 0.40: prediction 0.45-0.75, centre 0.60. P at p 0.60: 1.000; 0.50: 0.979; 0.45: 0.52; 0.42: 0.12.
  - (c1)(ii) bar 0.30: prediction 0.35-0.65, centre 0.50. P at 0.50: 1.000; 0.40: 0.983; 0.35: 0.56.
  - (c1)(iii) bar +0.30: floor predicted <= 0.05 (R3 0/131); at Agent12 0.45 (DP about 0.42, b about 0.48, se 0.028): 0.99.
  - (d) bar 0.05: prediction 0.0025-0.02 (Agent10's T1 lost rows 1/400 on H24 Run 2's bench seeds). P at 0.02: 0.99; 0.03: 0.65.
- **M1 T1 regression:** (a) rows bitwise Agent10 (never engaged): reported with the engaged-row count; (b) **paired DP P(V) Agent12 - Agent10, lower bound >= -0.05** (the project's allowed gap, as H24 Run 2 M2(b)). Pass probabilities (H24 Run 2 design v2 section 7): DP 0 or -0.01: 1.000; -0.02: 0.990; -0.03: 0.650; -0.04: 0.174. Prediction: DP in [-0.02, +0.01] (at most about 8 engaged rows) -> P >= 0.99. (c) lost rows DP upper bound <= +0.05; contacts <= 0.10 per row.
- **M2 T2 W1 regression:** (a) **paired dwell Agent12 - Agent10, lower bound >= -1.2** (0.10 x Agent10's 11.9); (b) reported: Agent12 - Agent6, reach, lost rows, contacts. Prediction: difference 0 to +2: in 600 steps the W1 agent's loop stays within d_along about -18 to +39 of B (start 20 downwind, section 2 arithmetic) and B's whiffs reset q, so the mode engages only in rows silent for 210 steps (W1 lost rows 14-38 in the record), whose dwell is near zero; P(M2(a)) > 0.95. The absent-odour dwell cost (Agent10 11.9 vs Agent6 24.4) is the filter's; H17 is not expected to remove it.
- **M3 T3 +1/-1 stranded (the claim):**
  - (a) **lost rows, paired DP Agent12 - Agent10, upper bound <= -0.05.** Arithmetic: R3 131 stranded rows, 116 lost; releases at step 72/87/419 (quartiles), so about 0.6-0.7 of them (about 80-92 rows) engage (release + about 165) with >= 200 steps left; with a whiff in 0.5-0.7 of those, and a whiff of either plume on 400-599 ending 'lost', about 30-60 fewer lost rows: **DP -0.075 to -0.15, centre -0.11.** P at -0.075 (b 0.085): 0.42; -0.10 (b 0.11): 0.885; -0.11: 0.95; -0.125 (b 0.135): 0.99.
  - (b) **P(V), paired DP Agent12 - Agent10, lower bound >= -0.02 (no harm).** Arithmetic: in 109/131 R3 releases the agent fled away from the valued source, so the nearer plume on the way back is the negative one; a negative whiff with nothing held can re-form a negative hold, flee again and strand again; V needs the valued plume beyond it. Of the 84 non-V stranded rows (N 24, tie 60), about 4-24 become V: **DP +0.01 to +0.06, centre +0.03.** P at +0.03 (b 0.05): 0.995; +0.01 (b 0.03): 0.88; 0: about 0.5.
  - (c) **wall contacts per row <= 0.10** (the honest target: recovery without the reflex; Agent8 0.307, Agent10 0.000 in R3). Arithmetic: only rows reaching legs 5-6 (+-52.2, u >= 300) without a whiff reach a side wall; predicted 0.02-0.12 per row; P about 1 at 0.05, about 0.5 at 0.10.
  - Reported: the P(V) gap to Agent8's 0.925 (predicted still 0.10-0.15); post-release whiffs in the stranded rows (0/131 for Agent10; predicted 0.5-0.7 of those with >= 200 steps left); re-formed negative holds after a search whiff; P(V | wall contact) per arm.
- **M4 T4 T3a (REPORTED):** neutral dwell 100-599 (Agent10 0.807 on H24 Run 2's bench seeds), time within 10 of the valued source, the engaged-step fraction. Prediction: small; q resets on the neutral whiffs, so the mode engages only away from both.
- **Identities in the run (printed):** search False == Agent10; never-engaged rows bitwise Agent10 in T1, T2, T3, T4; engagement exact on every row (q, u, leg, target).

**Joint pass probability** (independent parts, an order of magnitude): bench about 0.5-1 (set by (c1)(i)), M1 >= 0.99, M2 > 0.95, M3 (a) 0.42-0.99 x (b) 0.5-0.99 x (c) 0.5-1. At the centres about 0.7; at the low edges about 0.1. The (h1) and (h2) stop rules replace M1's and M3 (a)'s edges with bench-seed measurements before any task seed is spent.

**H17 verdict:** PASS iff B, M1, M2, M3 PASS. Statement: 'after S silent steps with nothing held, a crosswind cast of growing amplitude slanted along the wind lets the adopted agent find a plume from the stranded state outside it without the wall reflex, and changes nothing where a whiff arrives within S.' Supplied values, G 2, C0, these worlds, learning off, the wind sensed every step; q under the H17-scoped relaxation.

## 8. Unreadable conditions

The relaxation not signed (no code); B not run or not passed (tasks not run); a stop rule fired (tasks not run); ties above 0.20 in T1's base arm; fewer than 50 stranded rows in T3's base arm (the lost-row claim then UNREADABLE); M1 identities failing (an implementation error, fixed before the evaluation).

## 9. Seeds, sizes, order

Sizes: bench (a)-(d), (h1), (h2) 400 rows; (c) 400 per class and wall setting, 765 steps (c1), 600 (c2), 1800 (c3). T1 4 arms, T2 3, T3 5, T4 3; 400 x 600.

**Seeds (new):** development world 9943, agent 9953; evaluation world 1945, agent 2045; bench 20261051 / 20261052; bootstrap 20261053. Derived: world + 10000 (cell permutation) 19943, 11945, 20271051; agent + 20000 (cast draw) 29953, 22045, 20281052; also checked 30261051, 40261052. T1-T4 share the development and evaluation seeds.

Check done 2026-09-24 for v1:
- (1) Every file under the repository, recursive, .git and __pycache__ excluded: 165 files, pattern (?<!\d)(n)(?!\d) for all fifteen numbers above: no file contains any of them. A first candidate, dev world 9941, was found in experiments/h21/h21_report.md and experiments/h21/ph19_eval.txt and replaced by 9943 (agent 9951 by 9953). Excluded by name: ph26.py, ph26_*.txt, h17_*.md, master_plan.md, notes/*.md, viewer/*; present and excluded at the check: master_plan.md, notes/module_boundary_outlook.md and the six files under viewer/.
- (2) vinc_search in the team space for the seed numbers: no text match (semantic neighbours only).
- (3) Registered and not reused: H24 Run 2's (9919/9929, 1815/1915, 20261041-43, unused and registered to H24 Run 2), H25's (9896/9996, 1805/1905, 20261031-33), H24's, and every earlier registration.

**The code's self-check (ph26.py) repeats (1) before the first run.**

**Order:** the owner confirms (section 12) and signs the relaxation -> v2 FINAL -> ph26.py (Search mixin; Agent12 = Search + Agent10; no adopted module edited) -> self-checks -> bench (a)-(d), (h1), (h2) with the stop rules -> development run (operation errors only) -> one evaluation (T1-T4) -> report. Nothing changes after the table.

## 10. Predictions, with the arithmetic

- **Bench (c1):** Agent10 whiff after engagement <= 0.05 (R3: 0/131 to the run's end). Agent12 0.45-0.75 (the upwind slant crosses d_along 25 -> 0 at u about 150-370 while legs 4-5 sweep +-34.8 to +52.2; per-crossing detection 0.66-0.88); reach 0.35-0.65 (a whiff then steers at 0/0). Oracle about 1.0.
- **Bench (c2):** low within 300 steps (the first 360 search steps slant upwind, away from the plumes); by 600 steps higher (the downwind half). Reported only.
- **Bench (c3):** Agent10 below H16's 52 percent at 600 steps (H16's figure was over 5400); Agent12 above it; no bar.
- **Bench (d):** engaged rows in T1 +1/0 0.0025-0.02.
- **T1:** DP in [-0.02, +0.01]. **T2:** Agent12 - Agent10 0 to +2 dwell. **T3:** lost-row DP -0.075 to -0.15 (centre -0.11), P(V) DP +0.01 to +0.06 (centre +0.03), contacts 0.02-0.12 per row. **T4:** near Agent10.
- **What would make them wrong:** the engagement position differing from the exact-heading arithmetic (turn noise and the ring estimate); the negative plume re-capturing searched rows more often than assumed (T3 (b) toward 0); walls reached earlier than assumed (T3 (c)); longer any-odour silences in T1 than Agent10's lost-row count implies (bench (d)).

## 11. What this design does not test

Learning (H20 Stage B); heading-cue loss (H18; the wind is sensed every step here); another S, L0, gamma or U1; a search that remembers where it lost the plume (position); search while a hold is kept (Agent6 / Agent8 without the release keep holds indefinitely, record:silence-timeout-chain-result, so the mode would rarely engage for them; not an arm); whether flies grow their cast amplitude (no fly finding is claimed; the casting citations are recalled). **Note on the queued 'adaptive presence' item (master plan):** as designed the mode keys on silence of ANY odour, so it does not engage in H24 Run 2's harmful T1 rows, whose 150-200-step valued silences were spent while the neutral plume was sensed (h24_run2_nsweep.md section 4 (b)); H17 would shorten those silences only under the valued-silence variant of section 12 point 2(b).

## 12. What the owner confirms

1. **The mechanism:** (i) a crosswind cast of growing amplitude (legs 30 k steps), slanted 15 degrees along the wind, the slant reversing every 360 steps; (ii)-(iv) rejected as in section 3. Recommended.
2. **The new state and the relaxation (section 3):** (a) RECOMMENDED: sign the H17-scoped relaxation for ONE counter q = steps since the last whiff of any odour; or (b) a valued-silence variant (q resets only on whiffs of non-negative odours; lets the search pass through a negative plume and would also engage inside a neutral plume in T1; a new bench (d) risk); or (c) no new state: engage on `since` >= S and nothing held (engages inside non-steering plumes, contrary to constraint (d)).
3. **S:** 210 (recommended; the cast's return pass ends at 208.3, H16 p90 204-208) or 180 (RESET_AFTER + SAT; engages during some of the adopted reacquisitions).
4. **The bench:** parts (a)-(d), the (c1) bars 0.40 / 0.30 / +0.30, the oracle ceiling, open plane primary with walls reported; the stop rules (h1) on T1 and (h2) on T3's lost rows at pass probability 0.5.
5. **The tasks and bars:** T1 DP >= -0.05; T2 dwell vs Agent10 >= -1.2; T3 lost-row DP <= -0.05, P(V) DP >= -0.02, contacts <= 0.10 per row; T4 reported.
6. **The seeds** (section 9) and **the order** (H17 -> adaptive presence (queued, proposed) -> H20 Stage B).

## 13. Self-review (2026-09-24)

- **Every claim about the current navigation cites a line or a measurement** (the H24 lesson): targets ph21.py:72-82, the triangle ph21.py:78 with SAT ph12.py:29, the plume ph11.py:74-84, the reflex ph11.py:130-141, the walls ph12b.py:53 / ph13.py:39; the path arithmetic is labelled 'exact heading, no noise, not run', and its drift (-9.8 per cycle) matches the recorded 'about 10'.
- **An inconsistency found and stated, not smoothed:** the R3 diagnosis measured the stranded agents 24.6 (median) from the nearest region at e + 200; the arithmetic puts an R3-type agent about 43 downwind of its release point at engagement, which would place it farther. The along-wind position at e + 200 was not recorded. The arithmetic ignores turn noise and the flee's exact length; bench (c1) records the engagement positions before any bar is read.
- **The engagement rule differs from the brief's example in S** (210, not about 180), with the reason stated and 180 left as the owner's option.
- **The search cannot reach every odour-free state within 300 steps:** covering a 62 x 60 rectangle at 12-unit spacing needs at least 517 steps at speed 0.6 whatever the pattern; the bench bars only the R3 class (c1), the class carrying the measured consequence; (c2) and (c3) are reported.
- **The negative plume:** in +1/-1 the search can bring the agent back into the negative plume first (109/131 fled away from the valued source), and a re-formed negative hold flees and strands again. This is why T3 (b) is a no-harm bar and the Agent8 gap is reported, not barred.
- **The adaptive-presence queue text** says H17 'may shorten the very silences that set the T1 side of the curve'; with the recommended any-odour q it would not (section 11). Stated here for the owner.
- **Identity is by construction on never-engaged rows;** engaged rows differ on purpose. The noise sample is reused on engaged rows so that no extra draw shifts other rows' random streams (the generator is per agent object, one draw per step for all rows).
- **Walls:** the open-plane bench removes the reflex from the primary reading; the task keeps walls and bars contacts.
- Not tested: section 11.
