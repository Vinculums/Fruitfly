# Consolidation gate, 2026-09-29: design v1 DRAFT

**Status: v1 DRAFT, for the owner's confirmation (section 9). Not an owner decision.** Written by an Opus 5.5 agent at
the owner's request; the reviewing session (Claude) checks every number against the record before anything is recorded.
Every number below is quoted from `master_plan.md` at commit 2817eb6 with a line citation `master_plan.md:NNNN`, or
marked 'not in the record'. Nothing in this file is adopted, and no existing file is changed by it.

## 0. Status and scope

- Opened by **decision:consolidation-gate-open** (2026-09-29), the owner's words '정리 게이트 열자, 초안은 opus 에이전트로'
  (gloss: 'open the consolidation gate; the draft by an Opus agent'). The decision id is the reviewing session's; it is
  not yet in master_plan.md at 2817eb6 (not in the record there).
- Context: the queue confirmed at decision:h28-open-design now holds only (6) an H17 re-attempt, 'whose Run 3 would need
  new state' (master_plan.md:2439-2441, :2564-2565). H10 (master_plan.md:972-978) and H18 (master_plan.md:1079-1090) both
  closed on 2026-09-29 as NOT shown with nothing adopted. The last change to the adopted architecture was on 2026-09-26
  (H28 and H29 adoptions, master_plan.md:852-870); H12, H10 and H18 since then adopted nothing (master_plan.md:923-937,
  972-978, 1079-1090).
- **What a consolidation gate is here** (this draft's reading; the plan's own Phase 0 is the precedent, 'Consolidate (no
  new hypothesis)', master_plan.md:1106): no new hypothesis, no run, no change to the adopted architecture. It restates
  what is adopted (section 2), what is shown and not shown (section 3), what limits are recorded (section 4), which rules
  stand (section 5), how the work is run (section 6), what is open (section 7), and it PROPOSES next steps (section 8).
  Nothing here is decided until the owner confirms section 9.
- **Pending bookkeeping, not a decision.** The Vinc remote key expired (HTTP 401, 2026-09-29; master_plan.md:2441); the
  reviewing session reports it still rejected on the evening of 2026-09-29 (not in the record). Every H10 and H18 graph
  node and document put waits on it (master_plan.md:1883-1885, :1935-1936, :2441-2442); the H10 design re-put has been
  pending since the 2026-09-27 _PK refusals (master_plan.md:958-959). Meanwhile the git repository is the record
  (decision:master-plan-source-of-truth, master_plan.md:2369-2372). `main` was fast-forwarded to codex/h12-review-plan
  today: both are 2817eb6 (checked with `git rev-parse`), so the sentence '`main` is behind codex/h12-review-plan'
  (master_plan.md:2442) is now stale (flagged in section 9, point 8).

## 1. Where the project stands against its own plan

The plan names Levels 0 to 6 only as a snapshot of the start: 'Level 0 to 1 (connectome, circuits)', 'Level 2 to 3
(motifs, abstract architecture)', 'Level 4 (simulation)', 'Level 5 (agent)', 'Level 6 (behaviour comparison)'
(master_plan.md:1098-1102). It says later that 'the level framing ... is a snapshot of the start and is not tracked' and
that no level change is claimed (master_plan.md:1280-1282). The phase-to-level mapping below is the plan's own headings.

| Phase (level) | Plan's definition, short | Gate as written | Status as recorded |
|---|---|---|---|
| 0 Consolidate | regression harness, spec v0.1, protocol in graph (1107-1109) | 'every recorded result reproduces from one command' (1110) | complete, gate passed (8) |
| 1 Biological grounding (L0-1) | literature check; link each accepted hypothesis to a verified circuit or 'no anchor' (1113-1115) | H1, H2, H4, H5 each carry a sourced link or 'no anchor' (1116) | complete, gate passed, order kept (9) |
| 2 Select-and-Hold (L2-3) | H6 upstream stage; H7 commitment calibration (1119-1120) | wrong <= 5 of 200 over scale 0.25-4.0 and N 2-20, distractor amplitude >= 2 (1121) | complete, gate passed; H6 adopted; H7 closed as a recorded limit (10) |
| 3 Graded memory | H3 ring attractor (1124) | drift and update criteria stored beforehand (1125) | complete, gate passed; H3 adopted; velocity integration superseded at H14 (11-12) |
| 4 Learning | H8 reinforcement-gated plasticity (1128) | learning-curve criteria stored beforehand (1129) | complete, gate passed; H8 v2 adopted, amended at Phase 7.2 (13) |
| 5 Integrated agent (L5) | agent v1 in a 2D world; ablation of each module (1132-1133) | task performance above ablated versions (1134) | Run 1 gate NOT met, both headline claims later withdrawn (14); Run 2 complete, the circuit cleared, its reset had never fired (15); a gate verdict for Run 2 is not in the record |
| 6 Behaviour comparison, abstraction (L6) | 6.1 qualitative comparison with published fly behaviour; 6.2 abstraction ladder (1137-1138) | output: a synthesis document per motif (1139) | complete, gate passed; main result concept:discrete-vs-graded-bias (16-17) |
| 7 Acting on the Phase 6 synthesis | 7.1 H9, 7.2 H11, 7.3 H13 (1141-1144) | per sub-step | 7.1, 7.2, 7.3 complete; 7.3 gate passed (18-25) |
| after 7.3 | H14 promoted (1146), then H15 to H29, H12, H10, H18 as numbered hypotheses | each its own registered criteria | section 3; no Phase 8 exists and no closing gate for Phase 7 is in the record |

Reading (not a record): since Phase 7.3 all work has been inside the Level 5 agent (the plan says so of H20,
master_plan.md:1281-1282). Phase 1's anchor rule (1114) and Phase 6's comparison (1137) were run on the agent as it was
then; master_plan records no circuit link or 'no anchor' mark on the modules adopted after Phase 4 and no second
behaviour comparison (not in the record). Section 8 (c) proposes this.

## 2. The adopted architecture, restated in one place

Source: `## The architecture as currently adopted` (master_plan.md:1938-2155). Nothing is added. 'Within the tested
conditions' is kept wherever master_plan uses it.

### 2.1 The two forms (master_plan.md:1942-1960)

| Form | Agent | Built at (as master_plan cites) | Adopting decision | Tested scope, one line |
|---|---|---|---|---|
| two-channel, THE adopted agent | Agent17 = Agent14N2 built with N_hi 200 | src/ph35.py:104-105 through src/ph28.py:95-97; N17 = 200 at src/ph35.py:89 (1945-1947) | decision:h29-window-200-adopted-within-tested-conditions (862-870) | supplied +1/0, G 2, C0, gate on, N2, learning off, World7 T1, W1, T3a, T3b at t0 150 (1949-1951) |
| three-channel distractor form | Agent16 as composed in src/ph33.py | Act16 src/ph33.py:116-177; Agent16 src/ph33.py:180 (855, 1681-1682, 1955-1957) | decision:h28-burst-tie-adopted-within-tested-conditions (852-861) | supplied +1/0 with D at value 0, p_D 0.03, G 2, C0, gate on, N2, learning off, T1D and W1D; window 300 (1957-1959) |
| lineage reference | Agent14N2 = ReleaseN2 + Agent14 | src/ph30.py:117-140 (1962); cited as :117-136 at 2023 (see section 10) | decision:n2-release-adopted-within-tested-conditions (1961-1976) | the reference Agent17 was tested against (1953-1954) |

'A future design must say which form it composes' (master_plan.md:1943-1944). At two channels the H28 tie rule is inert
by code, so the three-channel form adds nothing to the two-channel form (master_plan.md:1959-1960).

### 2.2 Module by module (both forms unless stated)

| Module | What is adopted | Adopting decision | Tested scope, one line | Built at (as cited) |
|---|---|---|---|---|
| Upstream stage | Phase 2.1 Heeger stage, unchanged; also the amplifier and pulse-stretcher for a single whiff; 'whole stage removed' and 'cross-channel division term removed' are different controls (2000-2006) | Phase 2 (H6 adopted, 10); no decision id in the record | Phase 2 gate conditions (1121) | ph2.Upstream (2000); no line cited |
| Selection circuit (Select-and-Hold) | Phase 2 bistable circuit, unchanged; needs an external release (2007-2009) | Phase 2; no decision id in the record | Phase 2 gate; revision only via the empty state under sparse input (2026-2034) | Phase 2 circuit; no file or line cited in master_plan |
| H19 (a) | while nothing is held, a whiff of an odour whose valence is not negative is handed to navigation (2009-2011) | decision:h19a-adopt-and-run2-direction (72-80) | two-source 160x160 world, wind every step; not covered: whiffs of B while A is held, any distractor (2009-2011) | README lists ph14.py for H19(a); no line cited |
| Value gain G 2 | a gain (1 + G*max(v, 0)) on the stage output into the circuit and its evidence release; 'Tested in H20 Stage A, NOT adopted' (2043-2052), yet 'carried' by Agent14 (1969-1970) and named in every scope | no adopting decision in the record; G 2 fixed post hoc by decision:h20-stage-a-run-g2 (140-141) | G 2 appears in every adopted scope (1949, 1957, 2057) | ph16.py for H20 Stage A (README); no line cited |
| H21 gate | while a higher-valued odour is held, a lower-valued non-negative odour's response is zeroed into the circuit and the evidence release (2053-2056) | decision:h21-gate-adopted-within-tested-conditions (266-270); the H21 verdict is NOT shown | supplied value, +1/0, G 2, C0, dwell majority, learning off (2056-2057) | Agent6, ph19.py; the gate flag is the `rule` attribute, ph19.py:42 (612) |
| Release (N2) | H25's (S)+(Z) only while the held odour's own value is non-negative; off at a negative held value, where the frozen timeout defect stays in force (2016-2025) | decision:h25-release-adopted-within-tested-conditions (396-398), then decision:n2-release-adopted-within-tested-conditions superseding decision:release-negative-scope-on-hold (703-712) | (S)+(Z): +1/0, G 2, C0, T1/W1/T3a/T3b, learning off, gate on (2018-2019); off at negatives tested in World6 with learned values, H20 Stage C Run 2 (1965-1966) | Release mixin ph24.py (2017); ReleaseN2 src/ph30.py:117-140, the gate :128-132 (703-704, 1962-1963) |
| Heading ring | RingExact at tau 1.0, sigma 0.5, vgain = tau, n 16, wind at amplitude 6.0 (2067-2068) | decision:h14-adopt-tau1 (26-29) | wind sensed every step; 'equivalence was not tested' (2069-2071) | no file or line cited for RingExact; the second zero-input ring step at ph12.py:106-108 (985) |
| Ring input contract | fed the rotation made, not the commanded turn (2069) | decision:heading-input-rotation-made (54-57) | heading error over 45 degrees 4.30 -> 0.00 percent with the cue on every step (56-57) | no line cited |
| Navigation | surge-and-cast on a wind reference with the RETURN cast (triangle wave) (2107-2108) | decision:h16-close-limited-adoption (49-53) | little boundary influence, heading information every step, tracking a plume already entered and reacquiring after loss (2108-2110) | cast loop ph23.py:95-98, SAT 141.7 (1703); return rule ph12.py:126-128 (986) |
| H23 value filter | the upwind surge follows the top-valued non-negative odour in the agent's own read-out; a top-valued or negative held odour steers as before (2131-2136) | decision:h23-filter-adopted-within-tested-conditions (342-354) | supplied value, +1/0, G 2, C0, dwell majority, learning off, the H21 gate on (2136-2137) | Agent8, ph21.py (ph19.py line 63 replaced, 323); nav top present odour ph23.py:88-92 (1583) |
| Presence counter | present_k = (c_k < N_hi) or k held; start N_hi - 60 (a PRIOR: a never-sensed odour present on steps 0-58) (2142-2148) | decision:h26-adaptive-presence-adopted-within-tested-conditions (553-560); window 200 / start 140 for the two-channel form by decision:h29-window-200-adopted-within-tested-conditions (2152-2155) | two-channel: window 200, start 140 (1947-1948); three-channel: window 300, start 240 as tested (2154-2155) | counters ph23.py:83-85, start ph28.py:97 (2145); Agent14 src/ph28.py:92-97, constants :72 (1968-1969) |
| Three-channel additions | H27 composition rule (evidence release against the strongest non-held channel), three presence counters, the H28 burst-ranked value tie (1955-1957) | decision:h28-burst-tie-adopted-within-tested-conditions, re-signing the H28-scoped records for 'the adopted three-channel agent' (2189) | T1D and W1D at p_D 0.03 (1957-1959) | Act16 src/ph33.py:116-177; burst record :145-149, ranked top set :155-158, keep :161 (1681-1682) |
| Flee | a held negative odour drives the flee; negative avoidance overrides (1165-1167) | part of the adopted act; no separate decision in the record | 0 flee violations in every run where read (for example 160-161, 209, 1426) | the act reads `known` for the flee, ph23.py:77 (610, 1218) |
| Learning | H8 v2 with the extinction GATE; parallel site not adopted (2079) | decision:phase7-2-gate (21-22, 2079) | 'learning off' in every adopted agent scope; learned values reach behaviour through `known` within H20 Stage B's conditions and Stage C Run 2's (1988-1998) | acquisition ph4.py:58 (1764); extinction ph8.py:74-91, single-site :88-90 (1766-1767); read-out chan_valence ph14.py:52-55 (603) |
| Learning loop | every agent's learning state updated once per world step from its own position (2092-2095) | from H15 Run 2 (2092); no separate decision id in the record | H15 Run 2 world (2092-2095) | not cited |

Scope statements carried unchanged: 'a success inside that scope is not read as evidence for anything outside it'
(standing rule, master_plan.md:2222-2224).

## 3. Shown, not shown, and adopted: the ledger since Phase 7

Verdict wording is copied as recorded. Dates are the ones master_plan gives; entries before 2026-09-23 carry no date in
master_plan (not in the record; the git history starts 2026-09-23, commit 49e0bb6). Count class (last column): S =
shown-class (SHOWN / SUPPORTED / PASS / gate passed), N = evaluated or judged and not shown-class, B = stopped before
evaluation (bench, calibration, readability), M = mixed or split verdict, C = check or measurement only, no verdict.

| # | Item | Verdict as recorded | Adopted | Closing decision | Date | Lines | Class |
|---|---|---|---|---|---|---|---|
| 1 | H9 (Phase 7.1) | 'H9 rejected as stated; its mechanism claim accepted'; graded substrate revises 200/200 vs 0/200, cannot abstain | nothing; H10 queued | decision:phase7-1-gate (1836) | not in the record | 18-20 | N |
| 2 | H11 (Phase 7.2) | 'complete'; extinction gate ADOPTED; parallel site 'held unproven' | extinction gate | decision:phase7-2-gate | not in the record | 21-22 | M |
| 3 | H13 (Phase 7.3) | 'complete, gate passed'; two claims later qualified | none recorded; its saturating cast later superseded (2115-2116) | decision:phase7-3-gate-h14-promoted (1146) | not in the record | 23-25 | S |
| 4 | H14 | 'Not supported under its stored criteria' | exact-kernel ring tau 1, sigma 0.5, n 16 | decision:h14-adopt-tau1 | not in the record | 26-29 | N |
| 5 | H15 Run 1 | 'NOT supported'; 92 percent absorbed at the downwind wall | nothing | not in the record (H16 opened, decision:h16-open) | not in the record | 30-35 | N |
| 6 | H16 Run 1 | 'NOT supported as registered'; return 9.7 vs random walk 10.0 in 40x40 | nothing at Run 1 | decision:h16-close-limited-adoption | not in the record | 36-40 | N |
| 7 | H16 Run 2 | 'NOT supported under K1-K4 on one clause' (K3 cold start 52 percent) | return cast, limited scope, by a separate decision | decision:h16-close-limited-adoption | not in the record | 41-53 | N |
| 8 | two-source check | 'JUDGED': M1 pass, M2 pass on equality, M3(a) FAIL | nothing; world kept | decision:two-source-check-judged | not in the record | 58-65 | C |
| 9 | H19 (a) | 'SUPPORTED on N1-N5, the distractor condition N6 UNREADABLE' | H19 (a) within the tested conditions | decision:h19a-adopt-and-run2-direction | not in the record | 72-80 | S |
| 10 | H15 Run 2 | 'E1 ... NOT DECIDED BY THIS RUN. E2 ... PASS'; Q5 PASS | none recorded | decision:h15-run2-closed | not in the record | 93-109 | M |
| 11 | H20 Stage A | 'NOT SHOWN under the registered criteria'; A1 PASS, A2 FAIL, A3 PASS, A4 INCONCLUSIVE | nothing (gain 'NOT adopted', 2043) | decision:h20-stage-a-closed | not in the record | 140-175 | N |
| 12 | link check | 'complete, one run'; a check | nothing | record:h20-linkcheck-result | not in the record | 176-199 | C |
| 13 | H20 Run 2 | 'NOT SHOWN under the registered criteria'; R2 FAIL | nothing | decision:h20-run2-closed | 2026-09-23 | 200-232 | N |
| 14 | H21 | 'NOT shown under the registered criteria on an INCONCLUSIVE M2'; no criterion failed | the gate, within the tested conditions, separate record | decision:h21-closed | 2026-09-23 | 245-295 | N |
| 15 | H22 | bench 'NO CANDIDATE', task not run; 'CLOSED as NOT shown' | nothing | decision:h22-closed | 2026-09-23 | 296-329 | B |
| 16 | H23 | 'PASS under the registered criteria, M1-M6 all PASS'; 'CLOSED as SHOWN' | the value filter, within the tested conditions | decision:h23-closed | 2026-09-23 | 330-354 | S |
| 17 | absent-odour check | run once; 'reach kept' (0.860), cost in dwell (8 vs 25) | nothing; led to option (v) | decision:absent-odour-check-open (run) | 2026-09-23 | 355-365 | C |
| 18 | H24 | M4 FAIL, no candidate; 'CLOSED as NOT shown' | nothing; relaxation lapsed | decision:h24-closed | 2026-09-23 | 383-388 | B |
| 19 | H25 | 'SHOWN under the registered criteria'; 'CLOSED as SHOWN' | the release (S)+(Z) at +1/0; negatives ON HOLD | decision:h25-closed | 2026-09-24 | 389-398 | S |
| 20 | avoidance check | run once, 'a check, no verdict'; R3 'avoidance changed'; 'Not every reading clean' | nothing; negatives ON HOLD (decision:release-negative-scope-on-hold) | not a closure | 2026-09-24 | 399-411 | C |
| 21 | H24 Run 2 | 'STOPPED at the bench by its registered stop rule'; 'CLOSED as NOT shown' | nothing; relaxation lapsed | decision:h24-run2-closed | 2026-09-24 | 412-435 | B |
| 22 | H17 Run 1 | 'STOPPED at the bench: no candidate by the registered rule' ((d) 18/400) | nothing | decision:h17-closed | 2026-09-24 | 451-468 | B |
| 23 | H17 Run 2 | 'STOPPED at the bench by the registered (h2) stop rule'; H17 'CLOSED as NOT shown under its registered criteria' | nothing; relaxations lapsed | decision:h17-closed | 2026-09-24 | 490-521 | B |
| 24 | H26 | 'SHOWN under the registered criteria (M1-M7 PASS)'; 'CLOSED as SHOWN' | presence counter and Agent14, within the tested conditions | decision:h26-closed | 2026-09-25 | 546-560 | S |
| 25 | H20 Stage B | 'SHOWN under the registered criteria'; 'CLOSED as SHOWN' | nothing new (module and read-out already adopted) | decision:h20-stage-b-closed | 2026-09-25 | 586-605 | S |
| 26 | H20 Stage C Run 1 | 'STOPPED at the bench by the (hR) stop rule' | nothing | closed with H20 (1271) | 2026-09-25 | 628-652 | B |
| 27 | H20 Stage C Run 2 | 'SHOWN under its registered criteria', M1-M9 PASS; 'CLOSED as SHOWN'; H20 'CLOSED as a whole' | N2, within the tested conditions | decision:h20-stage-c-run2-closed, decision:h20-closed | 2026-09-25 | 685-724 | S |
| 28 | H27 | 'STOPPED at the bench by all three stop rules, NOT shown under its registered criteria' | nothing; the distractor condition a recorded limit | decision:h27-closed | 2026-09-26 | 732-769 | B |
| 29 | H28 | 'SHOWN under its registered criteria'; 'CLOSED as SHOWN' | burst-ranked value tie, three-channel form only | decision:h28-closed | 2026-09-26 | 792-804, 852-861 | S |
| 30 | T3b diagnosis | measurement only; F1 MET, F2 NOT MET, F3 NOT MET, F4 INCONCLUSIVE, F5 MET, F6 INCONCLUSIVE | nothing | decision:t3b-diagnosis (opening) | 2026-09-26 | 820-830 | C |
| 31 | H29 | 'SHOWN under its registered criteria'; 'CLOSED as SHOWN' | window 200, Agent17 the adopted two-channel agent | decision:h29-closed | 2026-09-26 | 838-851, 862-870 | S |
| 32 | H12 Stage 1 | 'PASS' (module bench) | nothing ('Stage 1 adopts nothing') | decision:h12-closed | 2026-09-26 | 891-898 | S |
| 33 | H12 Stage 2 | 'STOPPED at the bench, K0 UNREADABLE' | nothing | decision:h12-closed | 2026-09-26 | 899-911 | B |
| 34 | H12 Package E | 'SHOWN within its controlled conditions' (reset, matched-access, frozen-memory read-out) | nothing; MB5 NOT adopted (decision:h12-parallel-module-not-adopted) | decision:h12-closed | 2026-09-27 | 912-945 | S |
| 35 | H10 | 'STOPPED at calibration: NOT SHOWN for this family'; 'CLOSED as NOT shown' | nothing | decision:h10-closed | 2026-09-29 | 956-978 | B |
| 36 | H18 Stage A | stopped at I7, corrected (option (a)), then 'COMPLETE, measurement only'; only B-iii met, by one event | nothing | (Stage A has no verdict) | 2026-09-29 | 998-1036 | C |
| 37 | H18 Stage B (B-iii) | 'STOPPED at the bench by its registered stop rules'; H18 'CLOSED as NOT shown' | nothing; the leak a recorded limit | decision:h18-closed | 2026-09-29 | 1059-1090 | B |

Diagnoses run between items (measurement only, no verdict) are cited inside their rows and not counted:
unrecovered-excess (66-71), the two defects (81-88), H20 G bench diagnosis (124-139), H20 Run 2 (216-232), H22
(300-311), option-v (366-375), R3 (403-406), H24 Run 2 N sweep (423-428), H17 (458-468, 499-512), H20 Stage C (640-652),
H27 (744-757), H10 margin (972-978, 1862-1876).

**Counts, by this table's grouping** (37 rows; section 10 lists how grouping changes them):
- S (shown-class): 11 (H13, H19 (a), H23, H25, H26, H20 Stage B, H20 Stage C Run 2, H28, H29, H12 Stage 1, H12 Package E).
- N (evaluated or judged, not shown-class): 8 (H9, H14, H15 Run 1, H16 Run 1, H16 Run 2, H20 Stage A, H20 Run 2, H21).
- B (stopped before evaluation): 10 (H22, H24, H24 Run 2, H17 Run 1, H17 Run 2, H20 Stage C Run 1, H27, H12 Stage 2, H10,
  H18 Stage B).
- M (mixed or split): 2 (H11, H15 Run 2).
- C (checks and measurement-only stages): 6 (two-source check, link check, absent-odour check, avoidance check, T3b
  diagnosis, H18 Stage A).
- Total 11 + 8 + 10 + 2 + 6 = 37. Verdict-bearing rows (S + N + B + M) 31; of those, NOT shown or stopped (N + B) 18.
- **Adoption decisions since Phase 7: 11** (extinction gate; ring tau 1; return cast; H19 (a); H21 gate; H23 filter; H25
  release at +1/0; H26 counter and Agent14; N2; H28 tie for the three-channel form; H29 window 200), plus one owner
  contract change (decision:heading-input-rotation-made) not counted. Three of the 11 followed a verdict that was not
  shown-class (H14, H16, H21), each by a separate record, as the rule at master_plan.md:2222-2224 requires. Not adopted
  though shown-class: H13 (none recorded), H20 Stage B (nothing new), H12 Stage 1 and Package E (MB5 not adopted).

## 4. Recorded limits of the adopted agent

'Status' uses master_plan's own label. 'In scope?' answers whether the adopted scope already excludes the condition.

| # | Limit | Record id / status | Defining number(s) | In scope? |
|---|---|---|---|---|
| L1 | Cold-start search | 'recorded limit', record:release-negative-cost-limit unchanged (1533, 2458) | from an odour-free start 52 percent find the plume (45-46); H17 search not adopted: (c1) 0.542 and 0.578 vs 0/400 (1525-1526), task whiff fraction after engagement 18/84 = 0.214 vs 0.5-0.7 predicted (1528) | excluded: navigation 'Not validated: finding a plume from an odour-free start' (2110) |
| L2 | Ring under cue loss | 'recorded limit of the adopted ring outside the adopted scope', record:ring-cue-loss-limit (1080-1082) | 64.5 percent unrecovered vs 0.5 for a perfect integrator; residual sd 2.58 degrees, gain 1.0000; F-v 1.4433; 2 to 3 plume half-widths per block; restart 200 of 200 (1083-1088); cue absent 50 steps at a time | excluded: the adopted agent senses the wind every step (1088-1089, 2078) |
| L3 | Distractor capture, H27's agent | 'LIMIT of the adopted agent', record:distractor-capture-limit (761-764, 1977-1982) | T1D P(V) 0.787 vs 0.920; W1D 400/400 lost vs 22 (763-764) | the two-channel form has no D; superseded in the three-channel form by L4 |
| L4 | Distractor capture under the H28 tie | record:distractor-capture-limit-under-h28-tie (860-861, 1984-1986) | T1D DP -0.0275; W1D 222/400 lost vs 29 without D; T3aD 0.220 vs 13.193 (857-859) | NOT excluded: W1D is inside the three-channel form's tested scope (1957-1959) |
| L5 | T3b cast-phase dependence | a stated limit of decision:h29-window-200-adopted-within-tested-conditions; no record id (867-869, 1950-1953) | F2 NOT MET, 0.990 upwind at L + 300 (825-826); t0 100 +0.70 [+0.26, +1.14], t0 150 +1.95 [+1.45, +2.45], t0 200 +3.82 [+3.34, +4.31] (867-868) | partly: scope names T3b at t0 150 only (1951); other geometries and cast parameters untested (1952) |
| L6 | Loss whose second pass falls after the row's end | stated limit (F3), no record id (869, 1952-1953) | F3 recovery within 200 steps 0.478 (826) | not excluded by the scope's wording |
| L7 | The window acts in T1 silences | 'a trade' (1953) | T1 DP -0.0075 [-0.0200, +0.0025] (1950) | inside scope, within the registered bar |
| L8 | Selection circuit revises only via the empty state | 'RECORDED LIMIT', record:selection-circuit-revision-via-empty-state (2026-2034) | 0 of 319 isolated valued whiffs flipped a neutral hold; 156/156, 123/123; H23 bench 217/217, 71/71; dense input p 0.30 revised 400/400 by a route not recorded (2028-2034) | not excluded: a property of the adopted circuit, stated for sparse input only |
| L9 | Silence timeout defect at negative held values | 'KNOWN DEFECT, frozen', record:silence-timeout-chain-result (81-84, 2012-2015); in force at negatives under N2 (2023-2025, 2461-2462) | reset delivered for one step, held unit 1.99 -> 1.49, never releases (82-83) | fixed within N2 at non-negative values; in force at negative held values |
| L10 | Release at negative values | record:release-negative-cost-limit (406-407, 2020-2021); on-hold decision SUPERSEDED by N2 (2022-2025) | at +1/-1 as composed: P(V) -0.160, lost rows +0.235 (2020-2021); 131/131 no whiff after a drive-ended negative hold (406) | the release is off at negatives; 'supplied +1/-1 in World7 not run with N2 (read, not measured)' (1966-1967) |
| L11 | Parallel extinction site | 'held unproven' (21-22, 936); MB5 NOT adopted (decision:h12-parallel-module-not-adopted) | Package E +0.7350 [0.6925, 0.7775] at the value level only; 'No behavioural benefit in a continuously moving, learning agent was shown' (920-921, 933-935) | not adopted |
| L12 | Hold's benefit | '**Open:**' (2035), not a limit record | H15 Run 2 without the hold 132 of 400 unrecovered vs 21 (2035-2036); M6 DP 0 in H27 (1608) and +0.0000 in H28 (802) | unmeasured under a distractor (2041-2042) |
| L13 | Walls inside the rule's loop | concept:h15-arena-occupancy-floor, 'Not validated' (2113-2114) | 40x40: return 9.7 vs random walk 10.0 (38); 10.3 with 524 contacts per agent (44) | excluded: 'little boundary influence' (2108) |
| L14 | First source reached in C0 | link check reading (190-199, 2124-2130) | fixed identity reaches its source first in 0.060 (C0) and 0.087 (C1), 0.743 in C2 (186-192) | adopted scopes use the dwell-majority measure |
| L15 | Initial cast side | 'Found in H20 Stage A' (2117-2119) | 94 percent to one side with cast_sign +1 (2118-2119) | the harness draws it per row; the agent is unchanged (2119) |
| L16 | H26 prior cost in W1 | 'Measured cost' (2150) | W1 lost rows vs the unfiltered agent +0.0475 (2150) | inside scope |
| L17 | Learned values | stated boundary (1996-1998) | learned valued value exactly +1.0 at the saturating dose (579, 604) | 'Sub-saturating learned values are not shown; negative learned values are shown only in World6 with learning on, under N2' (1997-1998) |
| L18 | H7, commitment calibration to option count | 'closed as a recorded limit' (10) | not in the record (master_plan gives no number) | not stated |
| L19 | Fixed per-row odour codes | standing rule (2277-2279) | results conditional on the fixed code set | a condition on every result |

## 5. Standing rules

### 5.1 The rules as written (master_plan.md:2157-2379), one line each

'Setter' is master_plan's wording: 'Set by the owner', 'Added' (setter not named), or 'Added by the assistant'.

| Line | Setter, when | Rule, one line |
|---|---|---|
| 2158 | not stated | one hypothesis at a time; adoption and every gate decided by the owner |
| 2159 | not stated | success criteria stored in the graph before the run |
| 2160 | not stated | a mid-phase idea is queued; order changes only by a decision node |
| 2161 | not stated | failed runs and rejected designs stay on record |
| 2162 | not stated | each phase ends with a phase report document and an episode |
| 2163 | Added, Phase 0 | every script producing a recorded number stored in the graph in full, with sha256, same session |
| 2164 | Added, Phase 5 close | a score-reading gate states a floor and a ceiling |
| 2167 | Added, Phase 6 close | an ablation is checked for being a broken instrument first |
| 2170 | Added, Phase 7.2 close | a criterion standing in for a behavioural claim must be behavioural |
| 2173 | Added, Phase 7.3 close | a baseline comparison checks the baseline is not pinned at zero |
| 2176 | Added, H14 close | angular gain measured on per-step displacement accumulated without folding |
| 2179 | Added, H14 close | a relaxed bound is a signed decision naming old bound, new bound, anchor; stored criteria never edited (with the registry of scoped relaxations, 2181-2190) |
| 2191 | Added, after H15 Run 1 | task validity has three clauses (discriminate, no saturation, the intact agent clears the floor) |
| 2195 | Added, after H15 Run 1 | nothing adopted for agent use until run inside an agent at the agent's noise |
| 2198 | Added, after H15 Run 1 | score a behaving system over a horizon that exposes absorbing states, with a location measure |
| 2201 | Added, after H15 Run 1 | a median over a learned quantity is stated over agents that had the experience, with the count |
| 2204 | owner, H16 opening | development and evaluation seeds separate; one evaluation; a change after the table is a new Run |
| 2207 | Added, after H16 Run 1 | a presence score is read against a random walk's occupancy; cancelling schemes checked |
| 2211 | Added, after H16 Run 1 | heading memory under cue loss tested where unobserved heading changes do not dominate |
| 2213 | owner, H16 Run 2 opening | a rerun in a changed environment leaves the earlier verdict; geometry pre-registered relative to the source |
| 2219 | Added, after H16 Run 2 | a memory test is read only after a known-answer arm reproduces the no-loss arm |
| 2222 | owner, H16 close | verdict and adoption are separate records; an adoption states its scope and what it does not validate |
| 2225 | Added, H16 close | a figure measured in one starting state is not carried to another |
| 2229 | Added, H16 close | a draft decision is not the owner's until the owner says so |
| 2231 | Added, after the two-source check (wording by owner's review) | with many exact ties a win-rate bar does not measure the effect; ties are a result |
| 2236 | owner, after the two-source check | an amended criterion leaves the original verdict; the amended reading is separate |
| 2239 | owner, after the two-source check | a difference between runs differing in several ways is not attributed until matched; a diagnosis does not show a fix works |
| 2243 | owner, after the two-source check | an entry criterion does not lean on a value on its threshold; unrounded values and groups fixed in advance |
| 2246 | owner, H19 opening | a fix is the smallest change with boundaries, against the system and a control, on new seeds, with registered numbers |
| 2251 | Added, after H19 | a condition flooring every arm on dev seeds is unreadable and not retuned; a distractor must be irrelevant |
| 2255 | owner, H19 adoption | a WHY is labelled a mechanism interpretation unless measured; no favourable measure picked afterwards; controls named for what they remove |
| 2260 | owner, H19 adoption | an integrated run's specification is one standalone document fixed before code, cited by hash |
| 2263 | owner, Run 2 spec reviews | a justifying quantity is checked for what it measures; one statistic per criterion; PASS / FAIL / INCONCLUSIVE interval rule; FAIL final |
| 2274 | owner, Run 2 spec reviews | sampling unit and independence grounds stated; fixed codes mean results are conditional |
| 2280 | owner, Run 2 opening | an implementation error and a change to a hypothesis or criterion are recorded separately |
| 2282 | Added, after H15 Run 2 | a timing sentence is checked against the module's traces; say where ties can come from |
| 2286 | owner, H15 Run 2 close | a registered rule is not waived; an undecided verdict is not rewritten as a pass; labels exactly as the rule gives |
| 2295 | owner, H20 design reviews | a value hypothesis is narrowed to a controlled task; all-row denominators; symmetry needs a tolerance; three outcomes |
| 2309 | owner, after the H20 G bench (last sentence added by the assistant) | a no-candidate bench keeps bar and verdict; diagnosis before change; post-hoc parameter only by a separate execution decision; bench bar checked against the input's ceiling |
| 2322 | Added, H20 Stage A evaluation | a symmetric task registers the agent's initial state; selection and reach are two measures |
| 2330 | owner, H20 Stage A close | a multi-part criterion with no aggregate and no FAIL is INCONCLUSIVE; a printout summary is not the label; geometry rules |
| 2344 | Added, link check | a geometry is checked against every hard bound of the world; a reach measure calibrated by a known-answer arm |
| 2353 | Added by the assistant, H20 Run 2 diagnosis | a release flag coinciding with a hold's end is not shown to end it; conversion compared on the same rows |
| 2360 | Added, H21 review and evaluation | a proposed seed is checked against the whole record before the draft; a bar at the prediction's edge states the half-width |
| 2366 | owner, 2026-09-23 (decision:code-citation-convention) | records cite code by path + sha256 and source_doc |
| 2369 | owner, 2026-09-23 (decision:master-plan-source-of-truth) | the git master_plan.md is the source of truth; the graph doc a mirror re-put after every edit |
| 2373 | owner, 2026-09-25 (decision:seed-scan-exclusion-ph31-eval) | an incidental seed match is excluded as a (file, number) pair; the output is not edited |

### 5.2 The standing caution about bench gates (master_plan.md:2381-2432)

- The caution itself: 'Six times now' a mechanism passed its gate and failed in a behaving agent (2383-2396); 'A phase
  gate establishes that a mechanism has a property on a bench' (2398-2399). H20 adds two cases (2405-2409).
- H22 observations, 'the owner has made no rule of them' (2411-2418): bench state vs task state, bench window vs task
  horizon, a borrowed prediction.
- H24 lesson (decision:h24-closed): a dynamics assumption cites a bench or code line; a recorded defect is in force until
  fixed (2420-2422).
- Avoidance check lesson: a base result may rest on an artefact (2424-2426).
- H27 lessons (decision:h27-closed): a prediction anchored on a narrower definition; a named entry point is not a bound
  (2428-2432).

### 5.3 Flags (no rule is changed here)

1. **Graph-dependent rules are not being met.** 2159 (criteria in the graph before the run), 2163 (scripts in the graph
   the same session) and 2369 (mirror re-put after every edit) cannot be met while the key is rejected; practice since
   2026-09-27 has been to push the registration to git before any registered seed is used (master_plan.md:961-963).
   Proposed reading for the owner: git registration stands in until the key works, and the pending puts are listed
   (section 6.2). Not a rule change.
2. **2179 has become a registry.** The H14 relaxation rule carries, inside one bullet, the history of every scoped
   relaxation and composition record (2181-2190, about 3,500 words). Later practice refined it: records are 're-signed in
   form' per run (for example 483-485, 2185-2186), lapse at closure unless adopted (1635-1636), and become 'adopted state'
   with a scope (2189). Flag: the registry could move to its own section; the rule's text would not change.
3. **Known-answer cluster.** 2219 (known-answer arm before reading a memory test), 2344 (known-answer calibration of a
   measure) and the H18 I7 lesson (proposal P1 below) cover one idea at three levels.
4. **Seed cluster.** 2204, 2360, 2373 and the H10 finding that the graph's keyword search does not index numbers
   (960-961) overlap; the scan method is recorded only inside the H10 entry and design section 9 (1853-1854).
5. **Mechanism-interpretation cluster.** 2239 (a diagnosis does not show a fix works), 2255 (WHY is labelled), 2295 end (a
   diagnostic does not name its cause) and 2353 overlap.
6. **2162 (phase report and episode).** Since Phase 7 each hypothesis has a report document; whether episodes are still
   written is not in the record.
7. **The caution's count.** 'Six times now' (2383) predates H20's two added cases (2405-2409) and later bench-stops; the
   count may be stale.
8. **Execution practice not codified.** Local execution (the owner's '우리는 actoon에서 하면 안되고 여기 ㅇ에ㅣ전트
   실행해야함', gloss 'we must not do it on Actions; run it here in the agent', 943-945) and delegation to an Opus agent
   with independent recount (1018-1019, 1060-1063) are practice, recorded in progress entries, not in Standing rules.

### 5.4 Proposed additions (PROPOSALS for the owner, not rules)

- **P1 (from H18 I7, master_plan.md:1004-1016).** DRAFT: 'A known-answer expectation is checked for saturation before it
  is registered: where the known-answer arm sits at a ceiling or a floor, a relative clause of the criterion (a ratio or
  multiple between two shares) is recorded as SATURATED and not read, never as MET or NOT MET.'
- **P2 (from H18 Stage B, master_plan.md:1074-1077).** DRAFT: 'A design's arithmetic about a behavioural loop (a cast
  loop, a return path) states where the loop is anchored and checks whether the proposed change moves that anchor, before
  any prediction for the change is registered.'
- **P3 (codifies practice, master_plan.md:1018-1019, 1060-1063, 1864).** DRAFT: 'When a run is executed by a delegated
  agent, the reviewing session recomputes the registered headline readings from the stored outputs or arrays before the
  result is recorded.'
- **P4 (codifies the owner's instruction, master_plan.md:943-945).** DRAFT: 'Simulations run in the local session, never
  on GitHub Actions or other hosted runners; runs made on hosted runners before 2026-09-27 keep their records.'

## 6. Process ledger

### 6.1 How work has been run recently (as recorded)

| Practice | Where recorded |
|---|---|
| Spec before code, one standalone document cited by hash | rule 2260; every entry from H21 on, for example 245-247 |
| v1 DRAFT -> review -> v2 FINAL, section 12 answered by the owner; 'wording only' or no bar changed between versions | 481-488, 668-675, 783-791, 990-997 |
| Owner's standing instruction to follow the recommended options | 668-670 ('다음도 권고안에 따라 작업 진행'); 1037-1041 |
| Bench before task, with registered stop rules and pass probabilities | for example 490-498, 732-743, 1059-1078 |
| Diagnosis (measurement only) before closure or redesign | rule 2309; 458-468, 499-512, 640-652, 744-757, 972-978 |
| Development run for operation errors, then one evaluation | rule 2204; for example 838-851 |
| Execution by an Opus 5.5 agent, the reviewing session evaluates and recounts | 996-997; 1019-1021; 1060-1063; 1864 |
| Local execution, never GitHub Actions | 943-945; Package E ran on hosted runners before that instruction (912-913) |
| numpy pin | numpy 2.4.6 registered for H18 (995, 1000) |
| BLAS pin | not in the record (master_plan does not mention it) |
| Arrays kept local and hashed | H18 Stage A 136 MB (1011-1012); Stage B 275 MB (1078) |
| LF outputs so hashes match | 318 (H22 bench outputs normalised to LF); 928 |

### 6.2 Known debts

| Debt | Status | Where |
|---|---|---|
| H10 design v2 FINAL graph re-put | pending since the 2026-09-27 _PK refusals | 958-959 |
| H10 graph nodes and document puts (design v2 FINAL, src/h10.py, src/h10_perm_diag.py, src/h10_margin_diag.py, margin_diag.txt, the mirror) | pending on the key | 1883-1885 |
| H18 graph nodes and document puts (both designs, Stage A and Stage B outputs, the reports, the amendment) | pending on the key | 1935-1936 |
| H18 Stage B seeds 18101-18106, 18201-18203: graph scan | PENDING (repository scan 0 hits) | 1057-1058 |
| H18 Stage A instruments: graph scan | 'pending on the key' | 1901 |
| master_plan mirror re-put (decision:master-plan-source-of-truth) | not possible while the key is rejected | 2369-2372, 2441 |
| record:run-file-hash-discrepancy | named in the brief; not in the record at 2817eb6 (no match in any file of the repository) | not in the record |
| H10 label-permutation tolerance | failed check, not repaired: 1.059e-12 against 1e-12 in 1 of 40 rows, outputs exact | 966-968, 1860-1861, 1881-1882 |
| ph31 demo check 6 would fail on re-run; ph30's self-check lists ph31_eval.txt | known, not edited | 2376-2379 |
| Stale sentence '`main` is behind codex/h12-review-plan' | stale since today's fast-forward | 2442 |
| Stale acceptance target in the outlook note (bitwise identity 'with ph21.Agent8') | the adopted agent is now Agent17 / Agent16 | notes/module_boundary_outlook.md section 6 |

## 7. What remains open (not ranked)

- **The queue:** only (6) an H17 re-attempt; 'the consequence that moved it up (the release stranding negative holds) no
  longer arises by code under N2; a Run 3 would need new state' (2564-2565).
- **The outlook note's module idea** (notes/module_boundary_outlook.md, 2026-09-23): 'OUTLOOK. Not a decision' (its
  status line); 'Not now. No caller exists' (its section 6). Still an outlook.
- **The hold's benefit** under a distractor, 'Open' (2035-2042); M6 unmeasured in H27 and H28.
- **Untested conditions master_plan names:**
  - cue-loss schedules other than 50 steps at a time: the limit is stated for that schedule only (1083, 2072-2073); others
    not in the record;
  - walls under cue loss: excluded by rule 2211 (record:h16-k5b-confounded-by-walls);
  - T3b in other geometries and cast parameters (1740, 1751, 1952);
  - the three-channel form at window 200 (1959);
  - D: other p_D, a non-zero-valued D, learning with D, the H15 world (859);
  - learning in the adopted two-channel task: every adopted scope says 'learning off' (1949, 1957); learning on was shown
    only in World6 with Agent14 (N2) in H20 Stage C Run 2 (1991-1996); sub-saturating learned values not shown (1997);
  - supplied +1/-1 in World7 with N2: read from the code, not measured (1966-1967);
  - +1/+0.5, other G, other geometries, other P or N_hi (1340, 1361, 2138, 2149-2150);
  - the first source reached, and whether a crosswind term is needed (2129-2130);
  - the H12 module driving choice itself (learning on during choice, or a frozen module read directly): 'would need a new
    question and registration' (1829-1831);
  - H10's agreement gate: 'what an agreement gate would expose was not computed' (1877);
  - new odour codes: results conditional on the fixed per-row codes (2277-2279).
- **Plan-level items:** no circuit link or 'no anchor' mark on the post-Phase-4 adoptions, and no behaviour comparison
  of the current agent (section 1; not in the record).

## 8. Candidate directions, for the owner (PROPOSALS, not decisions)

| | (a) H17 Run 3 | (b) Module consolidation | (c) Level 6 synthesis of the current agent | (d) The hold's benefit |
|---|---|---|---|---|
| Question | Can a search rule find a plume from an odour-free or stranded start without costing tracking? | Can the adopted import chain be folded into one module that is bitwise the adopted agent? (engineering, no hypothesis) | Per Phase 6.1 and 1.2: how does Agent17 (and Agent16) compare qualitatively with published fly behaviour, and which post-Phase-4 modules have a circuit anchor or 'no anchor'? | Does Select-and-Hold change behaviour in the adopted agent, in a world where the hold can matter? |
| Motivation in the record | cold start a recorded limit (1533); (c1) finds a plume from the stranded state 0.542 / 0.578 vs 0/400 (1525-1526); both runs stopped at the bench, tasks never run (1521-1523) | two forms, 'a future design must say which form it composes' (1943-1944); outlook section 6 acceptance test is bitwise identity | Phase 6 is the plan's Level 6 step (1136-1139); Phase 1 'is the project's stated purpose' (2435); 11 adoptions since Phase 7 with no anchor mark (section 3) | 'Open: whether the hold earns its place' (2035); at +1/0 the trajectory does not depend on the hold (1583-1585); M6 0 in H27 (1608), +0.0000 in H28 (802) |
| New state needed | yes: 'the last whiffed odour's value sign separates (105/105 vs 0/16) but is new state' (1530-1531); a signed relaxation in H14 format (2179) | none; acceptance = bitwise identity on the same seeds (outlook section 6, target updated to Agent17 and Agent16) | none; a document, literature with sources | a world or measure where the hold matters; likely a new design, no module change stated |
| Cost | full cycle: design v1 DRAFT, review, v2 FINAL, relaxation signed, bench with stop rules, dev, one evaluation at 400 rows, new seeds | one new file plus an identity check over the adopted worlds (T1, W1, T3a, T3b; T1D, W1D); no seed beyond reproduction | no run for 6.1 and the anchors; 6.2 (the ladder) would need runs per motif, so 6.2 is left out of this candidate | full cycle, as (a); the H27 and H28 benches show the hold-not-read arm takes the same path (1608, 1621-1622), so the design must first find a world where it does not |
| Not worth doing if | the stranding motivation is gone under N2 by code (2564-2565) and the owner judges cold start outside the needed scope (2108-2110) | no caller exists (outlook section 6: 'Not now. No caller exists'); the phN chain is itself the reproducible artefact | the owner treats the level framing as untracked (1280-1282) and wants only mechanisms | no world can be built where the hold-not-read arm diverges; the question then stays open as recorded |
| Recommended rank | 4 | 2 | 1 | 3 |

**Recommended order: (c), then (b), then (d), then (a).**
1. (c) first: it costs no run, returns the project to the plan's stated purpose (Phase 1, 2435; Phase 6, 1136-1139),
   and its anchor table would show which open item matters biologically before any new hypothesis is chosen.
2. (b) second, as an engineering step with no hypothesis: its only test is bitwise identity, so it can fail only by
   finding an inconsistency in the chain, which would be worth knowing before (d) or (a) composes the agent again. If the
   owner keeps the outlook's 'no caller' condition, (b) is skipped.
3. (d) third: the one architectural question master_plan marks 'Open' on the adopted agent (2035), unmeasured twice.
4. (a) last: it needs new state and a relaxation, and the consequence that moved it up no longer arises by code under N2
   (2564-2565); that last fact is read from the code, not measured (1966-1967).

## 9. What the owner confirms

1. **Accept sections 2 to 4 as the consolidated record.** RECOMMENDED: accept after the reviewing session's number
   check, and write them into master_plan.md as a new section 'Consolidated record, 2026-09-29' placed before `## The
   architecture as currently adopted`, replacing nothing; mirror to the graph once the key works. Alternatives: (b)
   accept section 2 only; (c) keep this file as a note under notes/consolidation without writing into master_plan.
2. **P1 (known-answer saturation).** RECOMMENDED: adopt as a standing rule. Alternative: record it as an observation in
   the standing caution only.
3. **P2 (loop anchor in design arithmetic).** RECOMMENDED: adopt. Alternative: an observation under the standing caution,
   beside the H22 observations (2411-2418).
4. **P3 (independent recount of delegated runs).** RECOMMENDED: adopt, since it is already practice. Alternative: leave
   as practice.
5. **P4 (local execution).** RECOMMENDED: adopt, since the owner already gave the instruction (943-945). Alternative:
   leave it in the H12 erratum entry.
6. **The order of section 8.** RECOMMENDED: (c) -> (b) -> (d) -> (a). Alternatives: (b) first as pure bookkeeping; (a)
   first to use the only queued item; stop after this gate with nothing opened.
7. **Whether `main` stays in step with the working branch at each gate.** RECOMMENDED: yes, fast-forward `main` at every
   closure or adoption commit, as done today. Alternatives: only at consolidation gates; leave `main` behind.
8. **Bookkeeping corrections in the same edit as point 1** (each listed, no verdict touched): the stale '`main` is
   behind' sentence (2442); the ReleaseN2 line range, 117-140 (703, 1962) against 117-136 (2023), to be checked against
   src/ph30.py; the outlook note's acceptance target (Agent8 -> Agent17 and Agent16), as an addendum to the note, not an
   edit of its text. RECOMMENDED: make them. Alternative: list them as open bookkeeping only.
9. **The ledger's counting convention (section 3).** RECOMMENDED: keep the S / N / B / M / C classes with verdict
   wording copied verbatim. Alternative: count per hypothesis (H12, H17, H18, H20 one row each).

## 10. Self-review: the three weakest points

1. **The value gain G 2 is ambiguous in the record.** master_plan says the gain was 'Tested in H20 Stage A, NOT adopted'
   (2043) and names no adopting decision, yet Agent14 'carries ... the selection circuit with the H20 gain (G 2)' (1970)
   and every adopted scope reads 'G 2' (1949, 1957, 2057). Section 2.2 lists it as carried in scope with no adopting
   decision in the record. A reader could instead treat it as adopted with each agent. The owner or the reviewing session
   should say which reading master_plan intends.
2. **The counts depend on grouping.** H12 is three rows (Stage 1 S, Stage 2 B, Package E S), H17 two, H20 five plus the
   link check; H18 Stage A is counted as a check, H13's 'gate passed' as shown-class, H9's 'rejected as stated, mechanism
   accepted' as N, H11 and H15 Run 2 as mixed. Counted per hypothesis instead, the totals change (for example H12 would
   be one closure with no adoption). The reviewing session should recount every class from the table's last column.
3. **Citations for where modules are built are thin in master_plan.** No line is cited for the upstream stage, the
   circuit, RingExact or H19 (a); ReleaseN2 is cited as src/ph30.py:117-140 (1962) and :117-136 (2023); dates before
   2026-09-23 are not in master_plan. Section 4 also mixes items master_plan labels 'recorded limit' (L1, L2, L3, L4, L8,
   L18) with stated limits of an adoption (L5, L6, L7), a known defect (L9), 'Not validated' boundaries (L13) and an
   'Open' question (L12); the Status column keeps master_plan's label, but the choice of which boundaries to include is
   this draft's.
