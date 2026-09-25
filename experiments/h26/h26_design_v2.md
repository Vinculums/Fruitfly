# H26 design v2 FINAL: adaptive presence, the presence prior separated from the presence window, on the adopted agent (Agent10), +1/0

Date 2026-09-24. Status: **v2 FINAL (confirmed by the owner 2026-09-24).** The owner answered the v1 DRAFT (doc d9452710c5166ba01, experiments/h26/h26_design_v1.md, sha256 18983aa2cefbbd61310a42d07eb30eb4d7df8e82288e9eaa6ca839073a073598) on 2026-09-24, verbatim '권고안대로 확정하고 H26 진행' (gloss 'confirm as recommended and proceed with H26'): every RECOMMENDED option of section 12 is confirmed (decision:h26-open). Signed before any code: the H26-scoped relaxation of section 3.4 (decision:classification-rule-relaxed-presence-prior-h26) and the M5(d) re-sign (decision:h26-m5d-bar-resigned), both in H14 format. v2 differs from v1 only in wording that asked for confirmation or signature (this status, section 12 replaced by the confirmation, the signed decisions cited); no bar, seed, arm, prediction or rule is changed. Opened for design by the owner on 2026-09-24 ('1. H17 종료, 등록된 순서대로 adaptive presence(제안) → H20 Stage B', gloss 'option 1: close H17; proceed in the registered order, adaptive presence (proposed), then H20 Stage B'; decision:h26-open-design), in the same message that closed H17 (decision:h17-closed). The item was queued as 'adaptive presence', proposed by the interpreting assistant and not decided, at the H24 Run 2 closure (decision:h24-run2-closed); it had no number, and decision:h26-open-design assigns **H26** (the highest number in use was H25). Concept: concept:h26-adaptive-presence. Templates: H24 Run 2 design v2 FINAL (doc d65589bd43383a57c, experiments/h24/h24_run2_design_v2.md; "H24 Run 2" below) and H17 Run 2 design v1 (doc dedd3d11f43f9156f). H24's and H24 Run 2's verdicts (NOT shown; decision:h24-closed, decision:h24-run2-closed) stand and are not re-judged; their seeds stay registered to them. H25's release stays adopted at +1/0 and ON HOLD at negative values (decision:h25-release-adopted-within-tested-conditions, decision:release-negative-scope-on-hold). Supplied values, learning off, G 2, the H21 gate on, C0.

Code citations are repo-relative path:line at HEAD 6a11f2e; sha256 prefixes: ph11.py e80f40bd, ph21.py 3a1d79d9, ph22.py 03ab8c47, ph23.py ae180492, ph24.py f344f178, ph25.py 5620a908, ph25b.py ad12a912. Measurement citations: "sweep" is experiments/h24/h24_run2_nsweep.md with its output experiments/h24/ph25b_nsweep.txt (sha256 51534047...ecc7; record:h24-run2-n-sweep-result); "R2 bench" is experiments/h24/ph25_bench.txt (record:h24-run2-bench-result); "H24 bench" is experiments/h24/ph23_bench.txt (record:h24-bench-result); "H17 table" is the any-odour silence table of record:h17-post-bench-diagnosis-result and record:h17-run2-post-bench-diagnosis-result.

## 0. What is new against H24 Run 2

| item | H24 Run 2 (design v2 FINAL) | H26 (this design) | why (section) |
|---|---|---|---|
| counter start | c_k = 0 at construction: an odour never sensed is present on steps 0 to N - 2 (the prior is tied to the window) | **c_k = N_hi - P at construction**: an odour never sensed is present on steps 0 to P - 2; after any whiff of it the window is N_hi | the sweep moved the prior and the window together; W1 and T3a read only the prior, T1 mostly the window (2.3) |
| window after a whiff | N 60 | **N_hi 300** | T1 at N 300 on the sweep: V/N/tie 383/15/2 = Agent10's, DP 0.0000, 387 rows bitwise Agent10 (2.4) |
| prior | 59 steps (N 60) | **59 steps (P 60)**, unchanged | W1 and T3a at a 59-step prior: dwell 22.733, R 1.005 (sweep), W1 measured twice (2.2) |
| agent | Agent11 = Release + Agent9, N 60 | **Agent14 = Release + Agent9 with the start value**; no second state variable | (3.2, 3.5) |
| relaxation | re-signed for H24 Run 2; lapsed with its closure | **new, H26 only**, H14 format (3.4) | the old one lapsed |
| bench | (a)-(f), (h) with the stop rule | inherited, plus identities against Agent11 at N 60 and N 300, **(m)** the at-risk rows measured before any bar is read, the post-whiff window exact in the Lost world at L + 300, **(h3)** a W1 stop rule | (4) |
| M5(d) | lost rows vs Agent6 <= +0.05, predicted 0 to +0.02 | the prediction corrected from two benches (+0.035, +0.0475); **re-signed against Agent10 (decision:h26-m5d-bar-resigned)** | (7, 12 point 4) |
| seeds | 9919/9929, 1815/1915, 20261041-43 | **new:** dev 9977/9987, eval 1985/2085, bench 20261071/20261072, bootstrap 20261073 | (9) |

Nothing else changes from H24 Run 2: the filter rule (v-p) given presence, the tasks, the arm structure, the criteria's statistics and general rules, the verdict's form.

## 1. Hypothesis

**H26: an agent whose value filter takes v_max over the odours present, where an odour is present while held or for N_hi = 300 steps after its last whiff, and, before it has ever been sensed in the run, only on the first P - 1 = 59 steps (a prior), does three things at +1/0 against the adopted agent Agent10.** (i) In the H21 choice task it keeps H23's result: P(V) at least 0.88 and within 0.05 of Agent10 [M2]. (ii) In the absent-odour world W1 it tracks the only odour present within the registered dwell gap of the unfiltered agent Agent6 [M5]. (iii) After the valued odour is lost from step 0 (T3a, H25's constructed loss) it opens the filter exactly at step 59 and recovers at least half of the ceiling-floor span [M7]. The base is Agent10 = Release + Agent8 (the H23 filter and the H25 release; learning off, G 2, gate on, C0). The window, its prior and the filter are the agent's own state under a signed H26-scoped relaxation (3.4). Implementation claims are checked on constructed states first (section 4).

## 2. The measured reason

### 2.1 The cost being removed

- The H23 filter (ph21.py:69: v_max over all odours in the read-out; :71 keep; :72 nav) steers only on a top-valued whiff unless a top-valued or negative odour is held. With the valued odour absent from the world, the neutral odour never steers (record:absent-odour-check-result: Agent8 never surges in W1, dwell median 8 against 25).
- On H24 Run 2's bench seeds (R2 bench (d)): W1 mean dwell within 3.0 of the source over 600 steps Agent10 11.902, Agent6 24.433 (Agent10g equal to Agent6 row for row); lost rows 33 and 14. At the H25 evaluation Agent10 12.133 against Agent6 25.435.

### 2.2 The fixed window and what it measured

- H24 Run 2's rule (ph23.py:83 c_k <- 0 on a whiff of k, else c_k + 1; :85 present_k = c_k < N or k held; :88-89 v_max and top over present odours; :91-92 keep and nav) with the H25 release (ph24.py:60-62; a silent hold ends 48 steps after its odour's last whiff, H25 (b4) 48/48/48) made the window exact: M7(a) 400/400 in T3a and 382/382 in the Lost world, held-only presence 0 (R2 bench (b), (f)).
- At N 60 it removed the W1 cost (dwell 22.733, paired vs Agent6 -1.700 sd 9.962 [-2.680, -0.730]; H24's bench on other seeds, Agent9 without the release, -1.71 sd 10.26) but cost the H21 task: P(V) 0.785 against Agent10 0.958, paired DP -0.1725 [-0.2125, -0.1350], out of V 70, into V 1 (R2 bench (h)); the stop rule fired.
- The sweep (N 60 to 450 and inf, bench seeds 20261041/42):

| N | T1 V/N/tie | T1 DP vs Agent10 | out of V | rows bitwise Agent10 | W1 dwell | W1 - Agent6 | W1 first surge | T3a R |
|---|---|---|---|---|---|---|---|---|
| 60 | 314/81/5 | -0.1725 | 70 | 270 | 22.733 | -1.700 | 114/124/157 | 1.005 |
| 90 | 314/81/5 | -0.1725 | 70 | 270 | 22.733 | -1.700 | 114/124/157 | 1.005 |
| 120 | 316/79/5 | -0.1675 | 67 | 276 | 24.805 | +0.373 | 122/140/257 | 1.005 |
| 150 | 318/77/5 | -0.1625 | 65 | 278 | 19.608 | -4.825 | 156/266/289 | 1.005 |
| 200 | 378/20/2 | -0.0125 | 5 | 372 | 17.775 | -6.658 | 265/272/439 | 0.771 |
| 300 | 383/15/2 | 0.0000 | 0 | 387 | 15.098 | -9.335 | 419/442/468 | 0.260 |
| 450 | 383/15/2 | 0.0000 | 0 | 392 | 14.585 | -9.848 | 455/468/535 | 0.259 |

  T1 clears from N 200; W1 holds only to N 120 (M5(b) pass probability 1.000 at 60-120, 0.034 at 150); no swept N meets both (sweep section 2).

### 2.3 What the sweep varied: two quantities at once (read from the code, checked by the sweep)

- **The counter starts at 0** (ph23.py:57). With no whiff of odour k, c_k = t + 1 at step t, so k is present on steps 0 to N - 2 by the start value alone: the **prior**. After a whiff at step s, k is present on s to s + N - 1: the **window**. One N sets both.
- **In W1 the valued column is False on every step** (ph22.py:37-42, the column masked after World7 draws it), so the valued odour is never sensed and never held: its presence is the prior and nothing else. **In T3a** the valued column is masked from step 0 and a valued hold is constructed (s 2.0; it ends at step 47, R2 bench (f) 400/400): presence is the prior plus the held clause on 0 to 46, which lies inside the prior. So in W1 and T3a, N acts only as the length of the prior.
- **At +1/0, nav depends on the valued odour's presence only** (read from ph23.py:83-92): with the valued odour present, v_max = +1 and nav is Agent8's expression; with it absent, v_max is the neutral value when the neutral odour is present (a neutral whiff makes it present on that step, :83; a held neutral odour is present by the held clause, :85), and a neutral whiff steers when nothing or the neutral odour is held (keep, :91; nav, :92). The neutral odour's own counter never changes nav. The R2 bench checked the resulting presence identity on every (row, step) of T1 (nav == nav8 where the valued odour is present, nav6 where not; (a4) True).
- **Checked by the sweep:** at every finite N the first surge in W1 was the first B whiff at or after step N - 1, and in T3a the first neutral whiff at or after N - 1, in 400/400 rows (sweep section 1). The W1 and T3a columns of the table are functions of the prior.
- **In T1 the valued odour is sensed early in most rows,** so N acts there mostly as the window. At N 60, 389 of 400 rows had a valued hold ended by the release, and in 388 the valued presence then expired, at step 78/97/102 (sweep section 3); expiry is L + 60 for the hold's last valued whiff L, so L = 18/37/42 and at least about three quarters of the rows had a valued whiff by step 42. (Inferred from the quartiles; not a per-row count.)
- **Consequence.** The sweep tested (prior, window) pairs on the diagonal only. The W1 and T3a targets constrain the prior (W1 passes at 59 to 119 steps; T3a R 1.005 to 149); the T1 target constrains the window (clear from 200, exact at 300). Nothing measured requires them to be equal. H26 separates them.

### 2.4 Where T1's cost sits

- Every out-of-V row is a `differs8` row at every N (sweep section 3): a step on which nav differs from Agent8's expression while the valued odour is absent. By the rule this is always a neutral whiff steering with nothing or the neutral odour held and the valued odour not present (ph23.py:85, :91-92), so **the valued odour is not held at any harmful departure**: in those rows the valued hold had already been released.
- First `differs8` step 204/354/373 at N 60 (130 rows), 270/280/419 at N 200 (28 rows, 5 out of V), 303/405/440 at N 300 (13 rows, none out of V). The sweep's reading (labelled there): the damage is in valued silences longer than about 150 steps while the neutral plume is sensed.
- **The scale of those silences is the agent's own loop.** H17 table (Agent10, T1 +1/0, longest any-odour silence per row): 154/160/171, p95 207, max 321 (Run 1 bench seeds); 155/160/170, p95 204, max 327 (Run 2 bench seeds); rows reaching 300: 3 and 2 of 400. The long silences are the return cast's loop after a whiff at a source (record:h17-post-bench-diagnosis-result (A)). A valued silence is at least as long as the any-odour silence around it.

### 2.5 The one population the separation cannot serve

A T1 row whose first valued whiff comes after step P - 2 is, until that whiff, in W1's informational state: nothing in the agent's sensory history distinguishes 'not yet sensed' from 'absent'. Any presence rule on the agent's own history faces this; the separated rule confines the trade-off to that stretch. What the record says about it:
- at least about three quarters of the T1 rows had a valued whiff by step 42 (2.3, inferred from the expiry quartiles);
- every T1 summary at N 60 equals N 90's (V/N/tie, DP, out/into V, the 130 `differs8` rows and their quartiles, the 270 rows bitwise Agent10); a departure on steps 59 to 88 before a first valued whiff would have occurred at N 60 and not at N 90, so no such departure changed any of these summaries (inference from equal summaries, not a row-level check);
- R2 bench (c), a constructed start on the neutral axis with a neutral hold, where the first valued whiff comes late (H23 bench (b): median step 469): holding the valued odour at 600 Agent11 (N 60) 0.096 against Agent10 0.066, paired +0.0300 [+0.0037, +0.0575]. It points the same way, but it is a constructed state and is **not** used as the prediction (the H17 lesson, section 13).
The size of this population on the task is not in the record. Bench (m) measures it before any bar is read.

## 3. The change

### 3.1 Candidates, evaluated from the measured numbers

Common facts used below: nav depends on the valued presence only (2.3); at a harmful departure the valued odour is not held (2.4); a silent valued hold ends 48 steps after the later of its last whiff and its formation (R2 bench (b): a whiff at step 0, hold formed at step 2, ended at 50; a burst, last whiff 16/18/19, ended 64/66/67); a hold forms only after the whiff that starts it, and every first valued hold is entered from 'nothing held' (H23 bench (b) 217/217; H22 156/156); a valued whiff never flips a held neutral odour directly (H22: 0/319 isolated, 0/596 at s >= 1.8). Every candidate below shares the separation identity: in a row where the valued odour is present on every step on which a neutral whiff arrives with nothing or the neutral odour held, nav == nav8 on every step and the row is bitwise Agent10.

| candidate | own state beyond Agent10 | W1 (valued never sensed) | T3a (valued lost from step 0) | T1 harmful rows | verdict |
|---|---|---|---|---|---|
| (a) window reloads to N_hi on a valued hit while a valued hold is kept, to N_lo otherwise | c_k plus one bit per odour (the window chosen at the last whiff); new relaxation | its start value: N_lo's prior | its start value | N_hi where each stretch's last valued whiff came while held; N_lo where it came with nothing or neutral held | rejected: never longer than (e) in T1, equal in W1/T3a, more state |
| (a') graded: the window grows with each valued whiff, shrinks in silence | c_k plus a real-valued window per odour; new relaxation | its start value | its start value | at most (e)'s once saturated; shrinking during silence works against T1, whose harmful stretches are silences | rejected |
| (b) filter on while a valued hold is held or N_b steps after its release | a per-odour steps-since-release counter or flag; new relaxation | never on (no valued hold): nav == nav6 from step 0, == Agent10g (dwell 24.433) | on 0 to 46 + N_b | the fixed-N counter with N = 48 + N_b (the release is at L + 48 in every silent stretch) | rejected: the empty state before the first valued hold is unfiltered (Agent10g's T1 0.627 against 0.958 is the lower edge); with a prior added it reduces to (e) at best |
| (c) release only after N silent steps during which the neutral odour was sensed at least M times | c_k plus a neutral-whiff count per silence; new relaxation | first surge delayed to the M-th B whiff after N - 1 | the same | M 1: identical to fixed N on nav (a departure is itself a neutral whiff); M > 1 delays W1 and T1 alike | rejected: no separation principle, no number |
| (d) the closure's proposal: per-odour patience tied to the expected inter-whiff gap | c_k plus a gap estimate per odour (real-valued); new relaxation | no gaps to estimate: its start value | its start value | in-plume gaps 3-26 steps set a window far below the 150-210-step loop silences | rejected: reduces to (e) where (e) works; needs a number the record lacks where it differs |
| **(e) CHOSEN: the prior separated from the window** (the counter starts at N_hi - P) | **none beyond H24 Run 2's counter** (only its start value changes); a new H26 relaxation (3.4) | **== Agent11 at N = P (60), bitwise** | **== Agent11 at N = P, bitwise** | **== Agent11 at N = N_hi (300) in every row whose first valued whiff comes by step P - 2** | chosen |
| (f) not a presence rule: shorten T1's valued silences by search | H17's q | n/a | n/a | n/a | out of scope: H17 closed (decision:h17-closed); q does not engage in valued silences spent in the neutral plume |

**(a) in detail.** In W1 and T3a the valued odour is never sensed, so no reload ever happens and the rule is its start value; with the prior at N_lo it is identical to (e) there. In T1 it is identical to (e) (with the same N_hi) in rows where every valued stretch ends with a whiff taken while the valued odour is held, and shorter (N_lo) where a stretch's last valued whiff arrives with nothing held (the first whiff of a stretch always does, and the hold forms 2 steps later) or with the neutral odour held (valued whiffs do not flip it). How often a harmful silence begins that way is not in the record, and it is not needed for the choice: (a) is never longer than (e) in T1, equal in W1, T3a and a loss after tracking (T3b, last whiff while held), and needs one more bit per odour. The graded variant (a') starts where (a) starts and, by shrinking in silence, shortens the window exactly in the stretches T1 needs long.

**(b) in detail.** At a harmful departure the valued odour is not held (2.4), and a silent valued hold ends 48 steps after its last whiff; so "held or N_b after the release" is a window of 48 + N_b from the last whiff in every row whose last valued whiff was taken while held, i.e. the fixed-N sweep again with N = 48 + N_b (T1 clear only from 48 + N_b >= 200). Its difference from a counter is where no valued hold exists: before the first valued hold, in every row, the filter is off and nav == nav6 (Agent10g's expression). The H23 gain sits exactly there (H23: Agent8 0.953, DP against Agent6 +0.240, the difference carried where the valued odour is not held; H21: 120 of 400 rows first hold the neutral odour). The lower edge is Agent10g on the R2 bench seeds, 0.627 against 0.958; no number places (b) inside [-0.33, 0]. With a prior added, (b) becomes (e) in W1/T3a and (e) or shorter in T1 (valued whiffs taken while the neutral odour is held never start a hold, so they never open (b)'s window, whereas (e)'s counter resets on them), with a hold-linked counter as new state.

**(c) in detail.** A harmful departure is a neutral whiff steering (2.4). With M = 1 the condition 'at least one neutral whiff in the silence' holds on every departure step, so nav equals the fixed-N counter's on every step: (c) with M 1 is the fixed N. With M > 1 the departure moves to the M-th neutral whiff of the silence, in W1 and in T1 alike; W1 already erodes when the first surge moves past the first B whiffs (first surge 114/124/157 at N 60, 156/266/289 at N 150, where M5(b) fails). The record carries no count of neutral whiffs in T1's harmful silences or before W1's first surge, and nothing says the two differ: both are 'valued silent, neutral sensed', the event W1 depends on.

**(d) in detail.** This is the idea the record itself carried ("per-odour patience tied to the expected inter-whiff gap", concept:h24-presence-scoped-value-filter; sweep section 4 (c)(1)). In W1 and T3a the valued odour has no gaps to estimate, so the rule is its start value: (e)'s prior. In T1 the harmful silences are the agent's loop (2.4: 150-210 steps, p95 204-207), not the plume's intermittency: inside a cone a whiff comes with probability 0.30 exp(-d_along / 12) per step (ph11.py:80-82), expected gaps of about 3 steps at the source, 18 at d_along 20 and 26 at 24.5. A window of a few expected gaps is far below 150; one long enough for T1 would be a multiplier of 8 to 60 on gaps that depend on where they were sampled. A running maximum of observed gaps would need a silence of that length before the first harmful one, which the record does not show. (d) needs a real-valued estimate per odour and a new relaxation, and gives (e) at best.

### 3.2 The chosen rule (e)

Per row and per odour k in the read-out, with **N_hi = 300** and **P = 60**:
- counter c_k, integer; **c_k = N_hi - P = 240 at construction**; each step, before nav, c_k <- 0 if odour k whiffs this step, else c_k + 1 (ph23.py:83, unchanged);
- present_k = (c_k < N_hi) or (k is the odour held after this step's selection) (ph23.py:84-85, with N = N_hi);
- v_max, top, keep, nav as ph23.py:88-92, unchanged; if nothing is present, no whiff occurs and nothing is held, nav = False (Agent6's line).
Hence: an odour never sensed is present on steps 0 to P - 2 = 58 (c = 240 + t + 1 < 300); after a whiff at step s it is present on s to s + 299 and absent from s + 300 unless it whiffs again or is held. Nothing else changes: gain, gate, circuit, the H25 release, the silence timer, flee, cast, ring. The rule draws no random numbers.

**What the rule does in each registered condition (read from the code; each checked at the bench):**
- **W1:** the valued odour is never sensed, so every step's valued presence equals Agent11's at N = P = 60 (c differs by the constant 240, the threshold by 240): **Agent14 == Agent11 (N 60) bitwise**; == Agent10 on steps 0 to 58 and nav == nav6 from 59. Sweep: dwell 22.733, first surge = first B whiff at or after 59 in 400/400.
- **T3a:** the same argument (valued column masked from step 0; the constructed hold ends at 47, inside the prior): **Agent14 == Agent11 (N 60) bitwise**; M7(a) exact at step 59; sweep R 1.005 [0.936, 1.077].
- **T1:** in every row whose first valued whiff comes at step <= 58, the valued presence equals Agent11's at N 300 on every step (both present up to that whiff by their priors; c = 0 at the whiff in both; identical after): **such a row is bitwise Agent11 (N 300)**, whose T1 on the sweep seeds is Agent10's outcome (383/15/2, DP 0.0000, 387 rows bitwise Agent10, the other 13 without an outcome change). A row whose first valued whiff comes later (or never) is Agent11 (N 300) up to step 58 and Agent11 (N 60) up to its first valued whiff plus 59; it can depart from Agent11 (N 300) only on a neutral whiff with nothing or the neutral odour held between step 59 and its first valued whiff. These are the at-risk rows (2.5), measured in bench (m).
- **The Lost world (T3b, t0 150), a loss after tracking:** the window after the last valued whiff L is 300: no nav on a neutral-only whiff on L + 1 to L + 299, first neutral surge = first neutral whiff at or after L + 300 (L <= 149, so <= 449 < 600). **H26 does not fix a loss after tracking:** there it is a fixed window of 300 (the sweep's T3a at N 300, R 0.260, indicates the price of a 300-step blind stretch). Stated as a limit; T3b is reported.
- **+1/-1 (T4):** Agent14 == Agent10 bitwise, whatever the counter's start value: the -1 odour is never top, the +1 odour is top whenever present, a held -1 odour gives keep through v_h < 0, and with the +1 odour absent a -1 whiff gives no top and nav False, Agent6's line (H24 Run 2 section 3's reading, independent of c; R2 bench (a2') 400/400 True at N 60). The known -0.160 cost of the release at negatives (record:release-negative-cost-limit) is Agent10's; the release stays on hold there.
- **0/0 and +1/+1:** == Agent10 bitwise (every present non-negative odour is top; a whiff makes its odour present).
- **Held-only presence** (the held clause the only reason for presence at c >= N_hi): 0 by construction, since a silent hold ends at L + 48 < L + 300, and in T3a at 47 < 59.

### 3.3 Identities (by reading the code; checked in M3/M4)

- scope 'off' == Agent10 bitwise (Agent9 scope 'off' == Agent8, ph23.py:86-87; the Release mixin on top).
- P = N_hi = N: Agent14 == Agent11 at N (the start value 0), in particular (P 60, N_hi 60) == ph25.Agent11.
- W1 and T3a: Agent14 (60, 300) == Agent11 (N 60) bitwise; T1 rows with the first valued whiff at <= 58: Agent14 == Agent11 (N 300) bitwise.
- 0/0, +1/+1, +1/-1 == Agent10 bitwise (+1/-1 a reported identity).
- Presence identity: nav == nav8 where the valued odour is present, nav6 where not, every (row, step).
- Separation: == Agent10 up to the step before the first `differs8` step; a row with no `differs8` step is bitwise Agent10 throughout.

### 3.4 The relaxation, SIGNED for H26 (decision:classification-rule-relaxed-presence-prior-h26; H14 format: old, new, anchor)

The H24-scoped decision:classification-rule-relaxed-presence-counter lapsed with decision:h24-closed and its re-sign decision:classification-rule-relaxed-presence-counter-run2 with decision:h24-run2-closed; both stay on record. H26 needed its own signature before any code; the owner signed it as written below on 2026-09-24 (decision:classification-rule-relaxed-presence-prior-h26, section 12 point 3):
- **Old** (owner, H20 Stage A close; H21 design section 3; decision:h22-open-design (a)): 'The rule uses the agent's own value read-out and its own hold state; no source or axis position, no sensory history beyond what the circuit already holds.'
- **New, H26 scope only:** the same, plus ONE presence counter per odour c_k (steps since odour k was last sensed) with one window N_hi = 300 (present_k = c_k < 300, or k held). The counter STARTS at N_hi - P = 240, so an odour never sensed in the run is presumed present on steps 0 to 58 (P = 60). **This start is a PRIOR, recorded as such, not evidence.** No second counter, no flag, no other sensory history: the start value is a constant of construction, and 'never sensed' is carried by the counter itself (c_k > t).
- **Anchor:** (1) the agent's silence counter (RESET_AFTER 40, ph11.py:39), the same kind of quantity kept per odour; (2) record:h24-run2-n-sweep-result: T1 at N 300 equals Agent10's outcome (383/15/2, DP 0.0000), W1 and T3a depend on the prior only (2.3) and pass at a 59-step prior (dwell 22.733, M5(b) 1.000; R 1.005); (3) P 60 = the signed N of both lapsed relaxations (1.5 x RESET_AFTER), inside H24's dev-seed plateau (N 45 to 80, record:option-v-presence-diagnosis-result), W1 at a 59-step prior measured on two bench seed sets (-1.71 and -1.70 against Agent6); (4) with the H25 release a silent valued hold ends at L + 48 < L + 300 (record:h25-bench-result (b4)), so the window outlasts the hold. No fly finding is claimed.
- The prior reverses option (v)'s stated premise ('an odour never sensed cannot suppress the surge') for the first 59 steps of a run, in W1, in T3a and in T1's rows without an early valued whiff. Stated, not hidden.
- **Scope:** H26 only (Agent14 = Release + Agent9 with the start value; this design's v2 FINAL); any wider use is a new decision.

### 3.5 The code (not written here)

A new file (proposed src/ph28.py). Agent14 = Release (ph24.py:47-62, unchanged) + ph23.Agent9 (unchanged), composed as H25 composed Agent10 and H24 Run 2 composed Agent11 (ph25.py:43): `class Agent14(Release, Agent9)`, whose constructor calls the base constructor with N = N_hi and then sets the counter to N_hi - P (ph23.py:57 sets it to 0). No adopted module is edited (ph21.py Agent8, ph24.py Release); ph23.py, ph25.py and ph25b.py are not edited. Whether ph25's run-time hooks (measurement fields; ph25.py:47-76) and ph25b's N wrapper (ph25b.py:18-35) are imported or re-declared is an implementation matter checked by identities (a1') and (a5)-(a7). The seed self-check repeats section 9's scan before the first run.

## 4. Mechanism bench (constructed states; before any task run)

Values +1/0 unless stated; G 2; gate on. Bench seeds 20261071 (world, whiffs) / 20261072 (agent); bootstrap 5000, seed 20261073. Wilson 95 percent. 400 rows x 600 steps unless stated.
- **(a) Identities (implementation):**
  - (a1) scope 'off' == Agent10 (stub both channels p 0.30 200 steps, the same with channel 1 held; World7).
  - (a1') (P 60, N_hi 60) == ph25.Agent11 bitwise (World7 T1, W1, T3a): the start value is the only change.
  - (a2) 0/0 and +1/+1 == Agent10 (stub, World7); (a2') +1/-1 == Agent10 (reported identity; a False is an implementation error).
  - (a3) +1/0 with the valued odour held (channel 0 alone p 0.30, 260 steps) == Agent10.
  - (a4) presence identity on World7 T1, every (row, step).
  - **(a5) W1: Agent14 == Agent11 (N 60) bitwise on every field and step;** == Agent10 on 0 to 58; nav == nav6 from 59.
  - **(a6) T3a: Agent14 == Agent11 (N 60) bitwise;** == Agent10 on 0 to 58.
  - **(a7) T1: every row whose first valued whiff comes at step <= 58 is bitwise Agent11 (N 300) throughout;** every row departing from Agent11 (N 300) is in bench (m)'s at-risk set.
  - (a8) separation against Agent10 as section 3.3.
- **(b) Counter dynamics, exact (stub, 400 rows, 400 steps):** no whiff: c = 240 + t + 1, present exactly on 0 to 58; one whiff on channel 0 at step 0: c_0 = t, channel 0 present exactly on 0 to 299, absent from 300 (the hold it forms ends at step 50); a 20-step p 0.30 burst: absent from exactly 300 steps after the last whiff; held-only presence 0 (row, step). Bar: every row exact in every schedule, lower bound >= 0.95 (1.000 by 3.2).
- **(c) Task-like neutral-hold start (H23 bench (b) state; 800 rows), REPORTED:** holding the valued odour at 600, Agent14, Agent11 (N 60), Agent10, Agent10g; first valued whiff step.
- **(d) W1:** implementation bar: first surge = first B whiff at or after step 59 in every row (lower bound >= 0.95). Measured: D6_W1 (Agent6's mean dwell; Agent10g printed beside it), which enters the M5(b) bar rule; Agent14's, Agent11 (N 60)'s and Agent10's dwell; paired Agent14 - Agent6 with its sd; lost rows per arm.
- **(e) H23's implementation bars re-run on Agent14:** (a4') channel 1 held, both channels p 0.30, 200 steps: on every step with channel 0 present, nav == channel 0's whiff; (c') task start, nothing held: every nav step with the valued odour present has a valued whiff. Lower bound >= 0.95 each.
- **(f) Constructed losses, exact windows:**
  - T3a construction (ph24.run 'T3a') for every arm; **M7(a) exact:** the valued hold ends at step 47 with both units <= 1.0; nav False on every step 0 to 58 on which only the neutral odour whiffs; the first neutral surge is the first neutral whiff at or after step 59; the valued odour not held on any step >= 47. Bar lower bound >= 0.95 (1.000 by 3.2).
  - Lost world (t0 150) construction; **the post-whiff window exact in every eligible row** (a valued whiff before t0; L the last one): no nav on a neutral-only whiff on L + 1 to L + 299; the first neutral surge is the first neutral whiff at or after L + 300; the valued odour not held on any step >= L + 60. Bar lower bound >= 0.95.
  - Measured and reported: T3a dwell 100 to 599 per arm, floor (Agent10), ceiling (Agent5 fixed to the neutral odour), the span and per-row paired sd, R and M7(b)'s pass probability at it.
- **(m) NEW: the at-risk rows, measured before (h) is read (Agent10 and Agent14, World7 T1).** Per row: the first valued whiff step (quartiles; rows with none by 58, by 118, by 598); the at-risk set = rows with no valued whiff by step 58 that receive a neutral whiff with nothing or the neutral odour held before their first valued whiff (or by 599), from Agent10's run; the rows in which Agent14 departs from Agent11 (N 300) (an exact check that they lie in the at-risk set, (a7)); their outcome in Agent14, Agent11 (N 300) and Agent10; k = Agent14's out-of-V rows minus Agent11 (N 300)'s. Printed with the M2 pass probabilities of section 7 at that k. No bar reads (m); it replaces the unknown of 2.5 with a count.
- **(h) T1 stop rule (inherited):** Agent14 vs Agent10, 400 x 600: P(V) each, paired DP with its bootstrap interval, into/out of V; Agent11 at N 300 and at N 60 reported. **M2(b)'s pass probability at the bench DP (section 7 arithmetic); below 0.5: STOP**, the run returns to the owner after the bench record.
- **(h3) W1 stop rule (new):** M5(b)'s pass probability at the bench's paired Agent14 - Agent6 difference with the bar bar_T2 = -0.20 x D6_W1 given by (d)'s reference value; **below 0.5: STOP**. By (a5) this reads Agent11 (N 60)'s W1 on new seeds.
- **No-candidate rule:** any identity False or any implementation bar ((b), (d), (e), (f)) failing: the rule does not do what section 3 says; tasks NOT run; back to the owner. (c) and (m) reported; (h) and (h3) stop rules.

**Bar decision between bench and development run:** decision:h26-t2-dwell-bar records bar_T2 = -0.20 x D6_W1 from (d) (rounded to 0.1) and the pass probability at the bench difference; the rule is fixed here. Task numbers are never used.

## 5. Tasks

- **T1, the H21 choice task (unchanged from H24 Run 2 / H25):** World7, two sources SEP 10 apart crosswind, 160 x 160 with reflecting walls, the cone plume (whiff probability 0.30 exp(-d_along / 12) inside 0 < d_along < 25, |d_cross| < 1.5 + 0.25 d_along, or within 3.0 of a source), start on the midline 20 downwind, heading uniform, 2 x 2 balance, initial cast side drawn per row (agent seed + 20000), 600 steps, 400 rows; +1/0; dwell majority V, N or tie.
- **T2 = W1, the absent-odour world:** ph22.Masked, the valued column False after World7 draws it; read-out A +1 / B 0; 600 steps; main measure dwell within 3.0 of B over 600 steps. W3 (only B, 0/0) as an identity world.
- **T3 = T3a, the constructed loss (H25's):** the valued column masked from step 0; the agent starts at the valued source with the valued hold constructed (s 2.0); World7's heading draw; 600 steps; main measure neutral dwell within 3.0 over steps 100 to 599.
- **T3b, the Lost world (t0 150): REPORTED** (H25's span about 3.9 is below the readability bound 5); here it is the one condition where the window after a whiff (300) is exercised, and is printed with the exact-window check.
- **T4, +1/-1 (World7): REPORTED** (the release is on hold at negative values; outside the verdict): the identity with Agent10 printed; P(V), lost rows, wall contacts per row.

## 6. Arms

| task | arm | agent | values | role |
|---|---|---|---|---|
| T1 | adaptive | Agent14 (Release + Agent9, P 60, N_hi 300) | +1/0 | main |
| T1 | base | Agent10 | +1/0 | allowed gap (M2 b); separation identity |
| T1 | release-maintain | Agent10g | +1/0 | floor of the filter's gain (M2 c) |
| T1 | fixed window | Agent11 at N 60 (H24 Run 2's) | +1/0 | reported |
| T1 | fixed window | Agent11 at N 300 | +1/0 | reported; identity (a7) reference |
| T1 | filter, maintain | Agent8, Agent6 | +1/0 | reported |
| T1 | pathway-off | Agent3 (G 0, gate off) | +1/0 | floor (M1 c) |
| T1 | known-answer | Agent5 | +1/0 | ceiling (M1 d) |
| T1 | neutral | Agent14 | 0/0 | identity with Agent10 (M3; M1 a, b) |
| T2 | adaptive | Agent14 | W1 +1/0 | main (M5) |
| T2 | base | Agent10 | W1 +1/0 | the cost removed, reported; M5(d) reference (re-signed, decision:h26-m5d-bar-resigned) |
| T2 | maintain | Agent6 (Agent10g beside it) | W1 +1/0 | reference for M5(b) and (d) |
| T2 | fixed window | Agent11 at N 60 | W1 +1/0 | identity (a5), reported |
| T2 | identity | Agent14, Agent10 | W3 0/0 | bitwise identity (M3) |
| T3a | adaptive | Agent14 | +1/0 | main (M7) |
| T3a | floor / ceiling | Agent10 / Agent5 fixed to the neutral odour | +1/0 | span |
| T3a | reported | Agent10g, Agent11 at N 60 | +1/0 | H25's R reference; identity (a6) |
| T3b | Agent14, Agent10, Agent10g, Agent11 at N 60 | | +1/0, loss at t0 150 | REPORTED |
| T4 | Agent14, Agent10 | | +1/-1 | REPORTED (identity printed) |

## 7. Criteria, with pass probabilities

General rules (as H24 Run 2): one statistic per criterion; Wilson intervals; paired percentile bootstrap over rows, 5000 resamples, seed 20261073; 95 percent; one evaluation, no extension; a group under 50 rows unreadable; aggregation PASS if every part passes, FAIL if any fails, else INCONCLUSIVE. Pass probabilities: a paired DP with discordant fraction b, sd = sqrt(b - DP^2), se = sd / 20, P = Phi((DP - bar) / se - 1.96) for a lower-bound bar, Phi((bar - DP) / se - 1.96) for an upper-bound bar; a mean difference with the bench's sd, se = sd / 20; R with se = sd / (20 x span); **counts by the exact binomial** (H17 Run 2's correction). Computed with a calculator (awk), no project code run.

- **M1 T1 validity (else UNREADABLE):** as H24 Run 2 (ties <= 0.20 in neutral, pathway-off, known-answer; neutral side balance [0.35, 0.65]; pathway-off P(V | chose) in [0.35, 0.65]; known-answer P(V) lower bound >= 0.85). Pass > 0.99 (H25: known-answer 0.943, pathway-off 194/202/4, balance 0.545).
- **M2 T1 main (adaptive arm):**
  - (a) P(V) lower bound >= 0.88 (k >= 365 of 400);
  - (b) paired DP Agent14 - Agent10, lower bound >= -0.05;
  - (c) paired DP Agent14 - Agent10g, lower bound >= +0.05 (Agent6 and Agent8 reported beside it).
  - **Prediction.** Agent14 = Agent11 (N 300) in every row with an early valued whiff (3.2), and Agent11 (N 300) matched Agent10's outcome on the sweep seeds (DP 0.0000, out of V 0). So DP = -k / 400 with k the net rows lost in the at-risk population (2.5, bench (m)); the record gives no centre for k, only that it is small on the sweep seeds' evidence (2.5). Range 0 to 10 (DP 0 to -0.025).
  - Pass probabilities (into V 0; b = k / 400; M2(a) exact binomial at P(V) 0.958 - k / 400, Agent10's 0.958 on the R2 bench):

| k | DP | M2(b) | M2(a) | 0.99 x M2(a) x M2(b) |
|---|---|---|---|---|
| 0-5 | 0 to -0.0125 | 1.000 | 1.000-0.998 | 0.99 |
| 8 | -0.0200 | 0.990 | 0.983 | 0.96 |
| 10 | -0.0250 | 0.893 | 0.955 | 0.84 |
| 12 | -0.0300 | 0.650 | 0.900 | 0.58 |
| 13 | -0.0325 | 0.506 | 0.860 | 0.43 |
| 15 | -0.0375 | 0.260 | 0.757 | 0.20 |
| 20 | -0.0500 | 0.025 | 0.420 | 0.01 |

  M2(b) passes with probability above 0.5 while k <= 13 (DP above about -0.033). M2(c): Agent10g 0.627 on the R2 bench, DP about +0.33: above 0.999.
- **M3 identities (printed in the run):** section 3.3 on the task seeds: scope off == Agent10; (60, 60) == Agent11; 0/0 == Agent10; +1/-1 == Agent10 (reported identity); presence identity on every (row, step) of the adaptive arm in T1, W1, T3a; separation against Agent10; W1 and T3a == Agent11 (N 60); T1 early-whiff rows == Agent11 (N 300); W3 == Agent10; T3a construction for every arm.
- **M4 bench (section 4):** PASS iff the identities, (b), (d), (e), (f) pass; about 1 if the implementation is correct.
- **M5 T2 W1 (adaptive arm):**
  - (a) reach within 3.0 at least once, lower bound >= 0.80 (k >= 336 of 400). Sweep 388/400: exact binomial pass above 0.9999.
  - (b) **paired mean dwell Agent14 - Agent6 over 600 steps, bootstrap lower bound >= bar_T2 = -0.20 x D6_W1 from bench (d)** (-4.9 at the R2 bench's D6 24.4325). By (a5) the prediction is Agent11 (N 60)'s: -1.70 (sd 9.96) and -1.71 (sd 10.26) on two bench seed sets. Pass probability at bar -4.9 and sd 9.96: at -1.7, 1.000; -2.7, 0.993; -3.2, 0.927; -3.7, 0.673; -4.2, 0.290.
  - (c) wall contacts per row <= 0.10: 0.000 on every W1 arm measured: about 1.
  - (d) **lost rows (no B whiff in the last third), RE-SIGNED for H26 (decision:h26-m5d-bar-resigned): DP Agent14 - Agent10, upper bound <= +0.05; the gap to Agent6 reported.** The inherited form was: DP Agent14 - Agent6, upper bound <= +0.05, with the prediction '0 to +0.02' (H24 v3, H24 Run 2). **That prediction is contradicted by both benches:** H24 bench Agent9 29 vs Agent6 10 (+0.0475); R2 bench Agent11 28 vs Agent6 14 (+0.035); the sweep's W1 lost rows are 28 to 34 at every N against Agent6's 14. Pass probability at +0.035: at most 0.37 (b = 0.035; 0.16 at b 0.095); at +0.0475: at most 0.04. **Re-signed by the owner (section 12 point 4) in H14 format to DP Agent14 - Agent10, upper bound <= +0.05, the gap to Agent6 reported:** at the benches' -0.0125 (28 vs 33) and -0.0175 (29 vs 36), pass 0.987 or above for a discordant fraction up to 0.09.
  - (e) implementation: first surge = first B whiff at or after step 59, every row (exact).
- **M6 T1 lost rows (allowed gap):** (a) no whiff of either plume in the last third: DP Agent14 - Agent10, upper bound <= +0.05; (b) wall contacts <= 0.10 per row. Sweep at N 300: lost rows 1 vs 1; H25: contacts 0.000 at +1/0. Pass above 0.99.
- **M7 T3a:**
  - (a) the window, exact (every row): the valued hold ends at step 47 with both units <= 1.0; nav False on every step 0 to 58 on which only the neutral odour whiffs; the first neutral surge is the first neutral whiff at or after step 59; the valued odour not held on any step >= 47. Lower bound >= 0.95 (1.000 by 3.2).
  - (b) R = (D_Agent14 - D_floor) / (D_ceiling - D_floor) over steps 100 to 599, floor Agent10, ceiling Agent5 fixed to the neutral odour; bootstrap lower bound >= 0.50; readable only if the span's lower bound >= 5.0. By (a6) the prediction is Agent11 (N 60)'s: R 1.005 [0.936, 1.077] (span 13.613 [12.650, 14.560], per-row sd 9.941). Pass probability at R 1.005, 0.957 (H25 eval Agent10g), 0.85 or 0.77: 1.000; at 0.70: 0.9998; at 0.60: 0.78.
  - (c) identity: every arm's construction; Agent14 == Agent11 (N 60) bitwise; == Agent10 on steps 0 to 58.
- **M8 T3b and T4:** REPORTED (T3b: the post-whiff window exact is a bench bar, (f); T4: the identity and Agent10's +1/-1 numbers).

**Joint pass probability** (parts independent; an order of magnitude). M1 0.99 x M2 x M3 about 1 x M4 about 1 x M5 (a, b, c about 1; (d) as re-signed 0.99) x M6 above 0.99 x M7 about 1. **At k 0 to 5 about 0.97; k 8 about 0.94; k 10 about 0.83; k 13 about 0.42.** With M5(d) as inherited, multiply by 0.04 to 0.37: at most about 0.36. The probability of reaching the evaluation is set by (h) (the same quantity as M2(b) on bench seeds) and (h3) (about 1 at the measured W1 difference).

**H26 verdict:** PASS iff M1 to M7 all PASS. Statement: 'with v_max scoped to odours present by a per-odour counter whose window is 300 steps after a whiff and whose prior, before the odour is first sensed, is 59 steps, the adopted agent keeps H23's result in the H21 task within 0.05 of Agent10 and at P(V) of at least 0.88; in the absent-odour world it tracks the only odour present within the registered dwell gap of the unfiltered agent; and after the valued odour is lost from step 0 it opens the filter exactly at step 59 and recovers at least half of the ceiling-floor span.' Supplied values +1/0, G 2, C0, these worlds, learning off; the prior under the signed H26 relaxation. Nothing about a loss after tracking (T3b reported) or negative values (T4 reported).

## 8. Unreadable conditions

M1 failing; ties above 0.20 in the adaptive, base or release-maintain arm; a cell under 50 rows; M3 failing (an implementation error, fixed before the evaluation); M4 not run or not passed (tasks not run); decision:h26-t2-dwell-bar not recorded before the development run (tasks not run); the relaxation not signed (no code); the M5(d) choice not recorded (no code); M7(b) with a span lower bound below 5.0 (that part UNREADABLE, the aggregate INCONCLUSIVE at best).

## 9. Seeds, sizes, order

Sizes: T1 10 arms (Agent11 twice), 400 x 600; T2 W1 5 arms and W3 2; T3a 5 arms; T3b 4 arms (reported); T4 2 arms (reported). Bench 400 rows, (b) 400 steps, (c) 800 rows.

**Seeds (new):** development world 9977, agent 9987; evaluation world 1985, agent 2085; bench 20261071 / 20261072; bootstrap 20261073. Derived: world + 10000 (cell permutation) 19977, 11985, 20271071; agent + 20000 (cast draw) 29987, 22085, 20281072; also checked 30261071 and 40261072 (the earlier designs' pattern). T1, T2, T3a, T3b and T4 share the development and evaluation seeds (as H25 and H24 Run 2).

Check done 2026-09-24 for this v1, before this file or any other file carried the numbers:
- (1) Every file under the repository, recursive, .git and __pycache__ excluded, **no exclusion by name: 189 files**, pattern (?<!\d)(n)(?!\d), for all fifteen numbers above. **No file contains any of them; no collision, nothing replaced.**
- (2) vinc_search in the team space, one query per number (15): no full-text match for any. The semantic arm timed out on the first two queries and reported the index rebuilding on the other thirteen (those results are full-text only); the few semantic neighbours it returned (decision:h20-stage-a-open, concept:doc.df06694876045671d) carry none of the numbers as text.
- (3) Registered and not reused: H17 Run 1 (9943/9953, 1945/2045, 20261051-53) and Run 2 (9961/9973, 1965/2065, 20261061-63), both kept registered by decision:h17-closed; H24 Run 2 (9919/9929, 1815/1915, 20261041-43); H25 (9896/9996, 1805/1905, 20261031-33); H24 (9885/9985, 1785/1885, 20261011-13); the absent-odour check (1775/1875); H23 (9880/9980, 1765/1865, 20261001-03); H22 (9870/9970, 1755/1855); every earlier registration (master_plan.md lists them, and the scan (1) covers it).

The code's self-check repeats (1) before the first run, excluding by name the H26 files that carry the seeds (ph28.py, ph28_*.txt, h26_*.md), master_plan.md, notes/*.md and viewer/*.

**Order:** the owner confirmed section 12 and signed the relaxation (3.4) and the M5(d) re-sign (2026-09-24) -> design v2 FINAL (this document) -> ph28.py (Agent14; no adopted module edited) -> self-checks -> bench (a)-(f), (m), (h), (h3) with the stop rules -> decision:h26-t2-dwell-bar -> development run (operation errors only) -> one evaluation (T1, T2, T3a; T3b and T4 reported) -> report. Nothing changes after the table. Then, in the project order: H20 Stage B.

## 10. Predictions, with the arithmetic

- **Bench:** identities True; (b), (d) first surge, (e), (f) M7(a) and the Lost-world window exact 400/400 (by 3.2); (m) at-risk rows a minority (at least about three quarters of rows with a valued whiff by step 42, 2.3); (h) DP 0 to -0.025; (h3) M5(b) pass probability about 1 (W1 == Agent11 (N 60), measured at -1.70 and -1.71).
- **T1:** Agent10 0.93 to 0.97 (H25 eval 0.960; R2 bench 0.958); Agent14 - Agent10 0 to -0.025 (k 0 to 10), no centre on record; Agent11 (N 300) equal to Agent10 in outcome; Agent11 (N 60) about -0.17 (R2 bench, sweep); Agent10g 0.55 to 0.65.
- **T2 W1:** Agent14 == Agent11 (N 60): dwell about 22 to 24 against Agent6 about 24 to 26 (paired about -1.7); Agent10 about 12; reach 0.96 to 0.98; lost rows about 28 to 30 against Agent6 10 to 14 and Agent10 33 to 36; contacts 0.
- **T3a:** Agent14 == Agent11 (N 60): M7(a) exact at 59; R 0.95 to 1.0 (R2 bench 1.005, H25 eval Agent10g 0.957); floor 0.8 to 0.9; ceiling about 14.
- **T3b (reported):** the filter opens at L + 300 (<= step 449): neutral dwell 400 to 599 between Agent10's (about 2.1) and Agent11 (N 60)'s (5.6 on the R2 bench), nearer Agent10's.
- **T4 (reported):** Agent14 == Agent10 bitwise; P(V) and lost rows Agent10's (-0.160 against Agent8 is the release's, on hold).
- **What would make them wrong:** (1) a larger at-risk population on the new seeds (k above 10), which (m) and (h) read before any task; (2) T1 valued silences over 300 steps spent in the neutral plume in more rows than the sweep's 13 `differs8` rows at N 300 (none out of V); (3) W1 on new seeds far from the two measurements (M5(b) falls below 0.5 at a difference of about -3.9); (4) the M5(d) lost-row gap, if kept against Agent6.

## 11. What this design does not test

Learning (H20 Stage B); negative values (on hold; T4 reported only); +1/+0.5; other G, geometries, starts or t0; **a loss after tracking** (the Lost world is reported: there H26 is a fixed 300-step window, and the sweep's T3a at N 300, R 0.260, indicates the price); candidates (a), (a'), (b), (c), (d) of 3.1 (rejected on record); a P or N_hi other than 60 and 300 (the alternatives listed in v1 section 12, not chosen); another RESET_AFTER or D; cold-start search (H17, closed; a recorded limit); a behaviour that shortens T1's valued silences; whether a fly keeps such a counter or prior (no fly finding is cited or claimed).

## 12. The owner's confirmation (2026-09-24)

The owner answered v1 section 12 on 2026-09-24, verbatim: '권고안대로 확정하고 H26 진행' (gloss: 'confirm as recommended and proceed with H26'). Every RECOMMENDED option is confirmed (decision:h26-open); v1's section 12, with the alternatives, stays in doc d9452710c5166ba01. Each point resolved:

1. **The candidate: CONFIRMED (e),** the prior separated from the window: one presence counter per odour as H24 Run 2's, its start value N_hi - P, no second state variable (3.1, 3.2). (a) the hold-conditioned reload and (a') its graded form, (b) the hold-tied window, (c) the neutral-conditioned release and (d) the closure's gap-scaled patience are rejected on record (3.1).
2. **The parameters: CONFIRMED P 60, N_hi 300** (the counter starts at 240; an odour never sensed is present on steps 0 to 58; the window after a whiff is 300). The alternatives (P 90, P 120, N_hi 200, N_hi 450) are not run.
3. **The relaxation: SIGNED as written in section 3.4**, H14 format, H26 only (decision:classification-rule-relaxed-presence-prior-h26). The owner's own words, adopted with the quote above: 'H26 한정 규칙 완화: 냄새별 존재 카운터 1개, 감지 후 창 300, 시작값 240(한 번도 감지되지 않은 냄새는 처음 59스텝만 존재로 간주, 증거가 아닌 사전값), 그 밖의 감각 이력 없음.' (gloss: 'H26-only rule relaxation: one presence counter per odour, window 300 after sensing, start value 240 (an odour never sensed is treated as present only for the first 59 steps, a prior, not evidence), no other sensory history.')
4. **The bars: CONFIRMED** M2 (a) 0.88, (b) -0.05, (c) +0.05 against Agent10g; M5 (a) 0.80, (b) bar_T2 = -0.20 x D6_W1 from bench (d), fixed after the bench by decision:h26-t2-dwell-bar (rounded to 0.1), (c) 0.10, (e) exact; M6 as H23; M7 (a) exact, (b) R >= 0.50 with the span bound 5.0. **M5(d) RE-SIGNED in H14 format, H26 only (decision:h26-m5d-bar-resigned):** old 'lost rows, DP scoped - Agent6, upper bound <= +0.05' (H24 v3 and H24 Run 2 M5(d)); new 'DP Agent14 - Agent10, upper bound <= +0.05; the gap to Agent6 reported'; anchor: H24 bench 29 / 36 / 10 and R2 bench 28 / 33 / 14 lost rows for the counter agent / the adopted agent / Agent6, and the sweep's 28 to 34 at every N (the inherited prediction '0 to +0.02' was never checked against them). What it guards: that the rule loses no more W1 rows than the adopted agent; what it gives up: a bar on the gap to the unfiltered agent, which the 59-step prior costs.
5. **The stop rules: CONFIRMED** (h) T1, stop if M2(b)'s pass probability at the bench DP is below 0.5; (h3) W1, stop if M5(b)'s pass probability at the bench difference is below 0.5; (m) printed before (h) is read.
6. **The seeds: CONFIRMED** development 9977/9987, evaluation 1985/2085, bench 20261071/20261072, bootstrap 20261073 (section 9).
7. **The order: CONFIRMED** H26 -> H20 Stage B (decision:h17-closed continuing decision:priority-h24run2-h17-stageb).

## 13. Self-review (2026-09-24)

- **Every claim about the adopted code cites a line or a measurement:** the filter ph21.py:69, :71-72; the counter, presence and filter scope ph23.py:57, :83-92; the release ph24.py:47-62; the mask ph22.py:37-42; the cone and whiff rate ph11.py:80-82; RESET_AFTER ph11.py:39; Agent11's composition ph25.py:43; the sweep's N wrapper ph25b.py:18-35. Measurements: the sweep, the R2 bench, the H24 bench, the H17 table, H25's (b4), H22's and H23's revision counts.
- **Measured vs read vs inferred.** Measured: every table number; the first-surge exactness at N - 1 at every N; the release at L + 48; the W1 lost rows. Read from the code: W1 and T3a depend on N only through the prior; nav depends on the valued presence only at +1/0; Agent14's identities with Agent11 at N 60 (W1, T3a) and N 300 (early-whiff T1 rows); the +1/-1 identity. Inferred: three quarters of T1 rows with a valued whiff by step 42 (from quartiles); no summary-changing departure on 59 to 88 (from equal N 60 / N 90 summaries); k small. Every read or inferred claim a bar rests on has a bench check: (a5)-(a7) for the identities, (b) and (f) for the windows, (m) for k.
- **The H24 lesson** (a bench clause presumed a release the circuit does not make: H24's held clause assumed the timeout ends a valued hold, record:silence-timeout-chain-result had shown it does not). Guard: no clause here rests on an unmeasured circuit event. The release is H25's measured L + 48 (and formation + 48 for a single whiff, R2 bench (b)); the window (300) and the prior (59) both outlast it, so the held clause is never the only reason for presence (held-only presence expected 0, bench (b)); every identity claimed between Agent14 and Agent11 or Agent10 is checked bitwise at the bench against the running agents, not presumed.
- **The H17 lesson** (a prediction anchored on the wrong population: H17 Run 2 predicted the task's stranded rows from (c1)'s constructed state and missed the whiff fraction, 18/84 against 0.5-0.7, because leg 1 pointed to the flee side in the task rows). Guard: every H26 prediction is anchored on the same worlds, starts and seeds' task construction as the task (the sweep's T1, W1 and T3a runs of Agent11, to which Agent14 is identical in W1, T3a and T1's early-whiff rows), not on a constructed state; the one population the identities do not cover (T1 rows without a valued whiff by step 58) is named in 2.5 and measured in (m) before (h) is read; the constructed-start result that points the same way (R2 bench (c)) is cited as such and not used.
- **An inherited prediction found wrong, stated:** M5(d)'s '0 to +0.02' (H24 v3, H24 Run 2) against the measured +0.0475 and +0.035; neither run reached a task, so it was never read. v1 section 12 point 4 asked the owner to re-sign or keep it, with the pass probability of each; the owner re-signed it against Agent10 (decision:h26-m5d-bar-resigned).
- **The candidate is small, and that is stated:** (e) changes one constant of construction and adds no state; the 'adaptivity' is that an odour's presence window depends on whether the odour has been sensed in the run. It does not address a loss after tracking (3.2, 11), which is the case a gap-scaled window (d) was proposed for; the record gives (d) no number there either.
- **The T1 risk is not hidden:** no centre for k; M2(b) holds above 0.5 only while k <= 13; the stop rule (h) reads it on bench seeds.
- The bar rules read reference arms only (D6_W1); the candidate's bench values are reported; a rule change after the bench is a new signed relaxation.
- Not tested: section 11.
