# H21 report: hold maintenance by value in the H20 choice task

Date 2026-09-23. Design v2 FINAL doc d7fd5abcc95169698 (confirmed by the owner as written, decision:h21-open; hash e83c9de2...965a, equal to the local file's sha256). Code ph19.py sha256 00c6a3b32f80fae9f58b6dbd23a8e03b1710be45fcf335238f289567fce34791. One evaluation, world seed 1725, agent seed 1825, 400 rows x 600 steps, G 2, geometry C0, 95 percent intervals, no extension. Evaluation output ph19_eval.txt sha256 a963580521918c922071f46a4f2469f755290136e8f277379612a0fb0c11942e. Nothing was changed after the table.

**Status: NOT shown under the registered criteria, on an INCONCLUSIVE main criterion; no criterion failed.** M1 PASS, M2 INCONCLUSIVE (parts (a) and (b) PASS, part (c) INCONCLUSIVE), M3 PASS, M4 PASS, M5 PASS, M6 PASS. The registered verdict sentence requires every criterion to PASS; the printout's summary label is 'NOT shown'. Under the standing rule an INCONCLUSIVE criterion is not a FAIL and is not rewritten as a pass; the design allows no extension. Closure is the owner's. A statement about a supplied value, this rule, C0 and the dwell-majority measure; not about learning, the first source reached, other G or other geometries.

## 1. What was asked

H21: a hold on an odour with a positive value is maintained against a non-negative odour of lower value (the lower-valued odour's response is gated out of the selection circuit and the evidence release while the higher-valued odour is held); with this rule, in the H20 choice task with the value supplied, the source the agent stays at follows the value. Two statements judged separately: the rule maintains the hold (M4, bench), and a maintained valued hold is expressed in the dwell majority (M1, M2, M3, M5, M6, task). Arms: maintain (G 2, rule on), rule-off (the Run 2 agent), rule-only (G 0, rule on), pathway-off (floor), neutral (identity), known-answer (ceiling), priority-identity (+1/-1, identity with the Run 2 agent). Bars: M2(a) P(V) lower bound >= 0.70 over all 400 rows; (b) >= 0.55 per cell; (c) DP against rule-off lower bound >= +0.15; M6(a) added lost rows upper bound <= +0.05; (b) wall contacts <= 0.10 per row.

## 2. Implementation, self-checks, bench, development run

ph19.py defines Agent6 = ph16.Agent4 with the gate inserted where y' is formed (gate_k = 0 iff h >= 0 and 0 <= v_k < v_h; y'' replaces y' as the circuit's input and in the evidence-release comparison). No adopted module edited. Self-checks (demo output sha 8a989e32...ceeb): Agent6 with the rule off is Agent4 bitwise, and with the rule on is Agent4 at 0/0, +1/+1 and +1/-1 while differing at +1/0; in a constructed state with the valued odour held and the neutral odour presented for 100 steps the hold is kept in 100 percent of rows with the rule (the neutral response entering the circuit is 0) and in 0 percent without it; with the neutral odour held and the valued presented, 100 percent are revised, bitwise as Agent4; the priority constructed state (300 negative-held steps, flee target on every one, equal to G 0's); known-answer h and hit; arms share the cast draw; rule-off and priority-identity arms equal Agent4's runs; neutral equals G 0; the seeds 9860/9960/1725/1825 appear in no other script or output on record.

**Mechanism bench (M4), output sha c11977e4...5fa3: PASS.** Phase 1 channel 0 (+1) alone at p 0.30 for 60 steps: 400/400 hold it. Phase 2 channel 1 (0) alone for 200 steps, channel 0 silent: with the rule the hold is kept on every step in 400/400 rows, 1.000 [0.990, 1.000], at p 0.30 and at 0.057, at G 2 and at G 0; the timeout fired 1649 times in phase 2 and ended 0 holds (the held unit's s dips to 1.48 and recovers, median 1.95). Without the rule 0/400 keep it at either G (the held unit's s falls to 0 once channel 1 drives the circuit). Asymmetry: neutral held first, then the valued odour alone: circuit states bitwise equal to Agent4's, 400/400 revised in both. Inertness at 0/0, +1/+1 and +1/-1: bitwise equal. Noted: with channel 0 driven at p 0.30 and G 2 the bench itself reaches the clip on 4.3 to 4.7 percent of (row, step); a bench condition, not a task arm (task clip 0.01 percent).

**Development run (seeds 9860/9960, output sha 61b52aae...78fd):** no operation error; M1 PASS on the development seeds; no amendment. (Its printout read every criterion PASS, maintain 299/400 = 0.748, DP against rule-off +0.188 [+0.150, +0.227]; that printout is not the verdict.) Evaluation seeds unused until the one evaluation.

## 3. Results, one evaluation (seeds 1725 / 1825)

| arm | values | G | rule | V | N | tie | first hold valued / neutral | dwell median valued / other | P(V) dwell majority |
|---|---|---|---|---|---|---|---|---|---|
| maintain | +1 / 0 | 2 | on | 300 | 96 | 4 | 280 / 120 | 21.0 / 3.5 | 0.750 [0.705, 0.790] |
| rule-off | +1 / 0 | 2 | off | 228 | 162 | 10 | 280 / 120 | 15.0 / 10.0 | 0.570 |
| rule-only | +1 / 0 | 0 | on | 241 | 154 | 5 | 207 / 193 | 17.5 / 8.0 | 0.603 [0.554, 0.649] |
| pathway-off | +1 / 0 | 0 | off | 204 | 186 | 10 | 207 / 193 | 14.0 / 12.0 | 0.510 [floor: P(V \| chose) 0.523] |
| neutral | 0 / 0 | 2 | on | 204 | 186 | 10 | 207 / 193 | 14.0 / 12.0 | 0.510 (bitwise pathway-off) |
| known-answer | +1 / 0 | 0 | fixed h | 380 | 19 | 1 | 400 / 0 | 25.0 / 0.0 | 0.950 [0.924, 0.967] |
| priority-identity | +1 / -1 | 2 | on | 363 | 22 | 15 | 285 / 115 | 22.0 / 0.0 | 0.908 (bitwise the Run 2 agent) |

Cells of the maintain arm (V of 100; odour A +y, A -y, B +y, B -y): 86 / 70 / 76 / 68. First-approach step median 31 in every +1/0 arm; no wall contact in any of them. Input range at G 2: y' max 5.34, y' > 1.8 on 2.9 to 3.9 percent of channel-steps, the clip on 0.00 to 0.01 percent of steps; no arm flagged. First-reach secondary: maintain and rule-off identical, 208 / 192 (0.520 [0.471, 0.569]); pathway-off 206 / 194; known-answer 217 / 183 (0.542).

## 4. Criteria

- **M1 task validity: PASS.** Ties 10 / 10 / 1 of 400 in neutral, pathway-off, known-answer. Side balance 204/390 = 0.523 [0.474, 0.572]. Floor 204/390 = 0.523 [0.474, 0.572]. Ceiling 380/400 = 0.950 [0.924, 0.967].
- **M2 main: INCONCLUSIVE.** (a) maintain P(V) 300/400 = 0.750 [0.705, 0.790] against 0.70: PASS (the unrounded lower bound 0.7053 clears the bar by 0.005; 298 rows were needed, 300 were observed). (b) cells 86, 70, 76, 68 of 100 with lower bounds 0.779, 0.604, 0.668, 0.583 against 0.55: PASS. (c) DP = P(V) maintain minus rule-off = +0.180 [+0.143, +0.218] against +0.15: INCONCLUSIVE (the interval contains the bar; the unrounded lower bound is below 0.15). Reported: DP against pathway-off +0.240 [+0.198, +0.283]; 0.789 of the ceiling; rule-only 241/400 = 0.603 [0.554, 0.649], DP rule-only minus pathway-off +0.093 [+0.065, +0.122]; N 96, tie 4.
- **M3 identities: PASS.** Neutral with the rule at G 2 equals G 0 bitwise and G 0 equals ph14.Agent3; priority-identity equals ph16.Agent4 at +1/-1; rule-off equals ph16.Agent4 at +1/0; known-answer h equals the valued odour and its hit its whiffs.
- **M4 mechanism bench: PASS** (section 2; re-run inside the evaluation with the bench seeds: lower bound 0.990 over 400 rows).
- **M5 avoidance: PASS.** The +1/-1 agent is the Run 2 agent by construction (M3 ii); constructed state 300 negative-held (row, step), flee target on every one, equal to G 0's.
- **M6 no added lost rows: PASS.** (a) no whiff of either plume in the last third, maintain minus rule-off -0.003 [-0.008, +0.000] against at most +0.05 (3 against 4 rows). (b) wall contacts 0.000 per row against at most 0.10. Reported: no navigation hit in the last third, maintain 7, rule-off 4, rule-only 5, pathway-off 2, known-answer 14, priority-identity 30.

**H21 under the registered criteria: NOT shown; M2 INCONCLUSIVE, no FAIL.** One evaluation, no extension.

## 5. Where the value goes now (measured; the reading names no cause beyond what was measured)

- **Before a hold the gate does nothing, and the first selection is identical:** 280 valued-first rows in maintain and in rule-off (the same rows; first-reach identical 208 / 192), first hold at step median 12 in both.
- **A valued hold, once formed, is never lost with the rule:** valued holds ended 0 in maintain against 204 in rule-off (over 400 rows). Neutral holds ended 72 against 94; the revision of a neutral first hold to the valued odour is the same in both arms, 53 of 120 = 0.442 (the neutral-hold phase is identical until the revision).
- **A maintained valued hold converts:** P(V | first hold valued) 272/280 = 0.971 in maintain against 201/280 = 0.718 in rule-off. P(V | first hold neutral) 28/120 = 0.233 against 27/120. Of the 100 non-V rows in maintain, 92 are neutral-first rows and 8 valued-first.
- **The design's arithmetic is realised:** 0.70 x 0.971 + 0.30 x 0.233 = 0.750. The remaining loss is the first selection and the revision rate, as section 7 of the design said; the prediction (0.70 to 0.80; revision 0.3 to 0.45; DP against rule-off +0.15 to +0.30; rule-only 0.55 to 0.65; M6 no added lost rows) is met on every quantity, and the paired bar was set at the prediction's lower edge.
- **Paired, same rows:** the rule moves 72 rows into V and 0 out; 328 keep their class. Dwell medians 21.0 / 3.5 against 15.0 / 10.0. Dwell at the neutral source falls from 4975 to 3338 steps (over 400 rows), and of it 845 steps (25 percent) are spent while holding the valued odour (rule-off 411, 8 percent): an agent tracking the valued odour passes within 3.0 of the neutral source.
- **Rule and gain together exceed the sum of their separate effects (point estimates, observed):** gain alone (rule-off minus pathway-off) +0.060 (24 rows); rule alone (rule-only minus pathway-off) +0.093 [+0.065, +0.122]; both +0.240 [+0.198, +0.283]. Mechanism interpretation, not measured as a cause: the gain supplies more valued first holds (280 against 207) and the rule keeps them; with G 0 the rule keeps the 207 it gets (valued holds ended 23 in rule-only against 111 in pathway-off) and cannot add first holds.
- **Timeout:** fired 4378 times while held in maintain and ended 2 holds; the recorded limit (record:silence-timeout-chain-result) again.

## 6. What is shown and what is not

- Shown (registered): the gate maintains a valued hold on constructed input (M4: 400/400, 0/400 without it); the task is valid for the measure (M1, ceiling 0.950); the rule changes nothing at equal values, with nothing held, or at +1/-1 (M3, bitwise); avoidance is untouched by construction (M5); the rule adds no lost rows and no wall contact (M6). M2's absolute parts passed: the maintain arm stays at the valued source in 300 of 400 rows (lower bound 0.705 against 0.70) and in at least 68 of 100 in every cell.
- NOT shown (registered): that the rule's paired improvement over the Run 2 agent reaches +0.15 at 95 percent; observed +0.180 with interval [+0.143, +0.218]. M2 is INCONCLUSIVE, so the whole-run verdict is not a PASS.
- Measured, not a criterion: with the rule a valued hold is never lost (0 of 280) and converts at 0.971; the first selection and the revision of neutral holds bound P(V) at about 0.75 in this task.
- Not tested: learning, the integrated environment, any G other than 2, any geometry other than C0, the timeout, the navigation rule with nothing held, and any navigation change.

## 7. Provenance

- Design v2 FINAL doc d7fd5abcc95169698 (hash e83c9de2...965a); v1 doc d6a72a8f28a483b25 (history); decision:h21-open-design, decision:h21-design-v2-choices, decision:h21-open.
- Code ph19.py sha 00c6a3b3...4791 (source doc stored in full). Demo output sha 8a989e32...ceeb. Bench output sha c11977e4...5fa3 (record:h21-bench-result). Development output sha 61b52aae...78fd (record:h21-dev-run).
- Evaluation: seeds 1725/1825 unused before; output ph19_eval.txt sha a9635805...942e, appended below in full. Result: record:h21-result. Closure is the owner's.

## Appendix A: ph19_eval.txt in full (sha256 a963580521918c922071f46a4f2469f755290136e8f277379612a0fb0c11942e)

== H21, EVAL. design v2 FINAL doc d7fd5abcc95169698 hash e83c9de2acba49d65893000f453ee384134ab33a3c916466010327736535965a; this file sha256 00c6a3b32f80fae9f58b6dbd23a8e03b1710be45fcf335238f289567fce34791; G 2.0; world seed 1725, agent seed 1825; 400 rows x 600 steps; geometry C0; the one evaluation ==

   [maintain] G 2.0  MAIN, dwell majority: V 300  N 96  tie 4  (of 400)
      cells: 0 odour A valued, +y: V 86 N 14 0 0 | 1 odour A valued, -y: V 70 N 30 0 0 | 2 odour B valued, +y: V 76 N 22 0 2 | 3 odour B valued, -y: V 68 N 30 0 2
      dwell median valued 21.0 other 3.5; both zero 0; majority source == first hold 361/400; P(V | first hold valued) 272/280; P(V | first hold neutral) 28/120
      H21 diag: dwell steps at valued (valued-held, neutral-held, nothing) (7629, 104, 92) | at neutral (845, 2149, 344); nothing held 0.047 of steps
      H21 diag: holds ended 72 (on the timeout flag 2, evidence 69, both 0, neither 1); held unit's s the step before, median 1.06; timeout firings while held 4378, of which ended the hold 2; valued holds ended 0, neutral holds ended 72
      H21 diag: revision, first hold neutral and later held valued 53/120 = 0.442; no whiff of either plume in the last third 3; no navigation hit in the last third 7; wall contacts per row 0.00
      H21 diag: paired against rule-off, same rows: into V 72, out of V 0, unchanged class 328/400; first hold valued here 280 against 280
      secondary, first reach and diagnostics:

   [maintain] G 2.0  V 208  N 192  no-choice 0  (of 400)
      cells: 0 odour A valued, +y: V 59 N 41 0 0 | 1 odour A valued, -y: V 45 N 55 0 0 | 2 odour B valued, +y: V 49 N 51 0 0 | 3 odour B valued, -y: V 55 N 45 0 0
      P(V | reached) 208/400 = 0.520 [0.471, 0.569]; first-approach step median V 31 N 31; dwell median valued 21.0 other 3.5; contacts/row 0.00; no whiff in the last third 3
      first hold: valued 280 neutral 120 none 0, step median 12; hold changes mean 0.13; agreement: first hold == source reached 288/400, held at reach == source reached 237/400 (nothing held at reach 57); P(V | first hold valued) 188/280; P(V | first hold neutral) 20/120
      whiffs/row: valued plume 9.2 neutral plume 5.1 both same step 0.04; no-choice rows' hold history: never 0 valued only 0 neutral only 0 both 0
      input range: y' max 5.34, y' > 1.8 on 3.53% of (row, step, channel), s >= 4.9 on 0.01% of (row, step), s max 4.94
      segments, N rows: neutral selected first and held at reach 65; valued held earlier, neutral held at reach 0; valued held at reach yet neutral reached first 90; nothing held at reach 37 | V rows: valued held at reach 172 (of which first hold was neutral 3), neutral held at reach 16, nothing held 20

   [rule-off] G 2.0  MAIN, dwell majority: V 228  N 162  tie 10  (of 400)
      cells: 0 odour A valued, +y: V 67 N 31 0 2 | 1 odour A valued, -y: V 53 N 45 0 2 | 2 odour B valued, +y: V 53 N 44 0 3 | 3 odour B valued, -y: V 55 N 42 0 3
      dwell median valued 15.0 other 10.0; both zero 0; majority source == first hold 291/400; P(V | first hold valued) 201/280; P(V | first hold neutral) 27/120
      H21 diag: dwell steps at valued (valued-held, neutral-held, nothing) (5786, 104, 317) | at neutral (411, 3307, 1257); nothing held 0.113 of steps
      H21 diag: holds ended 298 (on the timeout flag 3, evidence 285, both 0, neither 10); held unit's s the step before, median 1.06; timeout firings while held 4084, of which ended the hold 3; valued holds ended 204, neutral holds ended 94
      H21 diag: revision, first hold neutral and later held valued 53/120 = 0.442; no whiff of either plume in the last third 4; no navigation hit in the last third 4; wall contacts per row 0.00
      secondary, first reach and diagnostics:

   [rule-off] G 2.0  V 208  N 192  no-choice 0  (of 400)
      cells: 0 odour A valued, +y: V 59 N 41 0 0 | 1 odour A valued, -y: V 45 N 55 0 0 | 2 odour B valued, +y: V 49 N 51 0 0 | 3 odour B valued, -y: V 55 N 45 0 0
      P(V | reached) 208/400 = 0.520 [0.471, 0.569]; first-approach step median V 31 N 31; dwell median valued 15.0 other 10.0; contacts/row 0.00; no whiff in the last third 4
      first hold: valued 280 neutral 120 none 0, step median 12; hold changes mean 0.44; agreement: first hold == source reached 288/400, held at reach == source reached 232/400 (nothing held at reach 96); P(V | first hold valued) 188/280; P(V | first hold neutral) 20/120
      whiffs/row: valued plume 7.6 neutral plume 6.1 both same step 0.03; no-choice rows' hold history: never 0 valued only 0 neutral only 0 both 0
      input range: y' max 5.34, y' > 1.8 on 2.89% of (row, step, channel), s >= 4.9 on 0.00% of (row, step), s max 4.92
      segments, N rows: neutral selected first and held at reach 65; valued held earlier, neutral held at reach 2; valued held at reach yet neutral reached first 56; nothing held at reach 69 | V rows: valued held at reach 165 (of which first hold was neutral 3), neutral held at reach 16, nothing held 27

   [rule-only] G 0.0  MAIN, dwell majority: V 241  N 154  tie 5  (of 400)
      cells: 0 odour A valued, +y: V 68 N 32 0 0 | 1 odour A valued, -y: V 58 N 42 0 0 | 2 odour B valued, +y: V 61 N 36 0 3 | 3 odour B valued, -y: V 54 N 44 0 2
      dwell median valued 17.5 other 8.0; both zero 0; majority source == first hold 343/400; P(V | first hold valued) 198/207; P(V | first hold neutral) 43/193
      H21 diag: dwell steps at valued (valued-held, neutral-held, nothing) (5043, 121, 1417) | at neutral (133, 3183, 1143); nothing held 0.187 of steps
      H21 diag: holds ended 134 (on the timeout flag 18, evidence 98, both 0, neither 18); held unit's s the step before, median 1.06; timeout firings while held 3857, of which ended the hold 18; valued holds ended 23, neutral holds ended 111
      H21 diag: revision, first hold neutral and later held valued 71/193 = 0.368; no whiff of either plume in the last third 2; no navigation hit in the last third 5; wall contacts per row 0.00
      H21 diag: paired against rule-off, same rows: into V 46, out of V 33, unchanged class 317/400; first hold valued here 207 against 280
      secondary, first reach and diagnostics:

   [rule-only] G 0.0  V 206  N 194  no-choice 0  (of 400)
      cells: 0 odour A valued, +y: V 59 N 41 0 0 | 1 odour A valued, -y: V 44 N 56 0 0 | 2 odour B valued, +y: V 49 N 51 0 0 | 3 odour B valued, -y: V 54 N 46 0 0
      P(V | reached) 206/400 = 0.515 [0.466, 0.564]; first-approach step median V 31 N 31; dwell median valued 17.5 other 8.0; contacts/row 0.00; no whiff in the last third 2
      first hold: valued 207 neutral 193 none 0, step median 30; hold changes mean 0.20; agreement: first hold == source reached 339/400, held at reach == source reached 172/400 (nothing held at reach 195); P(V | first hold valued) 176/207; P(V | first hold neutral) 30/193
      whiffs/row: valued plume 8.3 neutral plume 5.7 both same step 0.04; no-choice rows' hold history: never 0 valued only 0 neutral only 0 both 0
      input range: y' max 1.78, y' > 1.8 on 0.00% of (row, step, channel), s >= 4.9 on 0.00% of (row, step), s max 3.65
      segments, N rows: neutral selected first and held at reach 80; valued held earlier, neutral held at reach 0; valued held at reach yet neutral reached first 16; nothing held at reach 98 | V rows: valued held at reach 92 (of which first hold was neutral 0), neutral held at reach 17, nothing held 97

   [pathway-off] G 0.0  MAIN, dwell majority: V 204  N 186  tie 10  (of 400)
      cells: 0 odour A valued, +y: V 58 N 40 0 2 | 1 odour A valued, -y: V 51 N 48 0 1 | 2 odour B valued, +y: V 48 N 48 0 4 | 3 odour B valued, -y: V 47 N 50 0 3
      dwell median valued 14.0 other 12.0; both zero 0; majority source == first hold 306/400; P(V | first hold valued) 161/207; P(V | first hold neutral) 43/193
      H21 diag: dwell steps at valued (valued-held, neutral-held, nothing) (4128, 121, 1544) | at neutral (87, 3751, 1529); nothing held 0.217 of steps
      H21 diag: holds ended 228 (on the timeout flag 19, evidence 188, both 0, neither 21); held unit's s the step before, median 1.06; timeout firings while held 3768, of which ended the hold 19; valued holds ended 111, neutral holds ended 117
      H21 diag: revision, first hold neutral and later held valued 71/193 = 0.368; no whiff of either plume in the last third 2; no navigation hit in the last third 2; wall contacts per row 0.00
      secondary, first reach and diagnostics:

   [pathway-off] G 0.0  V 206  N 194  no-choice 0  (of 400)
      cells: 0 odour A valued, +y: V 59 N 41 0 0 | 1 odour A valued, -y: V 44 N 56 0 0 | 2 odour B valued, +y: V 49 N 51 0 0 | 3 odour B valued, -y: V 54 N 46 0 0
      P(V | reached) 206/400 = 0.515 [0.466, 0.564]; first-approach step median V 31 N 31; dwell median valued 14.0 other 12.0; contacts/row 0.00; no whiff in the last third 2
      first hold: valued 207 neutral 193 none 0, step median 30; hold changes mean 0.35; agreement: first hold == source reached 339/400, held at reach == source reached 172/400 (nothing held at reach 199); P(V | first hold valued) 176/207; P(V | first hold neutral) 30/193
      whiffs/row: valued plume 7.2 neutral plume 6.4 both same step 0.03; no-choice rows' hold history: never 0 valued only 0 neutral only 0 both 0
      input range: y' max 1.78, y' > 1.8 on 0.00% of (row, step, channel), s >= 4.9 on 0.00% of (row, step), s max 3.64
      segments, N rows: neutral selected first and held at reach 80; valued held earlier, neutral held at reach 0; valued held at reach yet neutral reached first 12; nothing held at reach 102 | V rows: valued held at reach 92 (of which first hold was neutral 0), neutral held at reach 17, nothing held 97

   [neutral] G 2.0  MAIN, dwell majority: V 204  N 186  tie 10  (of 400)
      cells: 0 odour A valued, +y: V 58 N 40 0 2 | 1 odour A valued, -y: V 51 N 48 0 1 | 2 odour B valued, +y: V 48 N 48 0 4 | 3 odour B valued, -y: V 47 N 50 0 3
      dwell median valued 14.0 other 12.0; both zero 0; majority source == first hold 306/400; P(V | first hold valued) 161/207; P(V | first hold neutral) 43/193
      H21 diag: dwell steps at valued (valued-held, neutral-held, nothing) (4128, 121, 1544) | at neutral (87, 3751, 1529); nothing held 0.217 of steps
      H21 diag: holds ended 228 (on the timeout flag 19, evidence 188, both 0, neither 21); held unit's s the step before, median 1.06; timeout firings while held 3768, of which ended the hold 19; valued holds ended 111, neutral holds ended 117
      H21 diag: revision, first hold neutral and later held valued 71/193 = 0.368; no whiff of either plume in the last third 2; no navigation hit in the last third 2; wall contacts per row 0.00
      secondary, first reach and diagnostics:

   [neutral] G 2.0  V 206  N 194  no-choice 0  (of 400)
      cells: 0 odour A valued, +y: V 59 N 41 0 0 | 1 odour A valued, -y: V 44 N 56 0 0 | 2 odour B valued, +y: V 49 N 51 0 0 | 3 odour B valued, -y: V 54 N 46 0 0
      P(V | reached) 206/400 = 0.515 [0.466, 0.564]; first-approach step median V 31 N 31; dwell median valued 14.0 other 12.0; contacts/row 0.00; no whiff in the last third 2
      first hold: valued 207 neutral 193 none 0, step median 30; hold changes mean 0.35; agreement: first hold == source reached 339/400, held at reach == source reached 172/400 (nothing held at reach 199); P(V | first hold valued) 176/207; P(V | first hold neutral) 30/193
      whiffs/row: valued plume 7.2 neutral plume 6.4 both same step 0.03; no-choice rows' hold history: never 0 valued only 0 neutral only 0 both 0
      input range: y' max 1.78, y' > 1.8 on 0.00% of (row, step, channel), s >= 4.9 on 0.00% of (row, step), s max 3.64
      segments, N rows: neutral selected first and held at reach 80; valued held earlier, neutral held at reach 0; valued held at reach yet neutral reached first 12; nothing held at reach 102 | V rows: valued held at reach 92 (of which first hold was neutral 0), neutral held at reach 17, nothing held 97

   [known-answer] G 0.0 (held odour fixed to the valued odour)  MAIN, dwell majority: V 380  N 19  tie 1  (of 400)
      cells: 0 odour A valued, +y: V 91 N 9 0 0 | 1 odour A valued, -y: V 97 N 3 0 0 | 2 odour B valued, +y: V 97 N 3 0 0 | 3 odour B valued, -y: V 95 N 4 0 1
      dwell median valued 25.0 other 0.0; both zero 0; majority source == first hold 380/400; P(V | first hold valued) 380/400; P(V | first hold neutral) 0/0
      H21 diag: dwell steps at valued (valued-held, neutral-held, nothing) (9941, 0, 0) | at neutral (1794, 0, 0); nothing held 0.000 of steps
      H21 diag: holds ended 0 (on the timeout flag 0, evidence 0, both 0, neither 0); held unit's s the step before, median nan; timeout firings while held 0, of which ended the hold 0; valued holds ended 0, neutral holds ended 0
      H21 diag: revision, first hold neutral and later held valued 0/0; no whiff of either plume in the last third 2; no navigation hit in the last third 14; wall contacts per row 0.00
      secondary, first reach and diagnostics:

   [known-answer] G 0.0  V 217  N 183  no-choice 0  (of 400)
      cells: 0 odour A valued, +y: V 60 N 40 0 0 | 1 odour A valued, -y: V 47 N 53 0 0 | 2 odour B valued, +y: V 53 N 47 0 0 | 3 odour B valued, -y: V 57 N 43 0 0
      P(V | reached) 217/400 = 0.542 [0.494, 0.591]; first-approach step median V 31 N 30; dwell median valued 25.0 other 0.0; contacts/row 0.00; no whiff in the last third 2
      first hold: valued 400 neutral 0 none 0, step median 0; hold changes mean 0.00; agreement: first hold == source reached 217/400, held at reach == source reached 217/400 (nothing held at reach 0); P(V | first hold valued) 217/400; P(V | first hold neutral) 0/0
      whiffs/row: valued plume 10.8 neutral plume 4.3 both same step 0.03; no-choice rows' hold history: never 0 valued only 0 neutral only 0 both 0
      input range: y' max 1.78, y' > 1.8 on 0.00% of (row, step, channel), s >= 4.9 on 0.00% of (row, step), s max 0.00
      segments, N rows: neutral selected first and held at reach 0; valued held earlier, neutral held at reach 0; valued held at reach yet neutral reached first 183; nothing held at reach 0 | V rows: valued held at reach 217 (of which first hold was neutral 0), neutral held at reach 0, nothing held 0

   [priority-identity] G 2.0  MAIN, dwell majority: V 363  N 22  tie 15  (of 400)
      cells: 0 odour A valued, +y: V 94 N 3 0 3 | 1 odour A valued, -y: V 91 N 5 0 4 | 2 odour B valued, +y: V 89 N 6 0 5 | 3 odour B valued, -y: V 89 N 8 0 3
      dwell median valued 22.0 other 0.0; both zero 13; majority source == first hold 274/400; P(V | first hold valued) 268/285; P(V | first hold neutral) 95/115
      H21 diag: dwell steps at valued (valued-held, neutral-held, nothing) (7623, 331, 666) | at neutral (389, 334, 425); nothing held 0.131 of steps
      H21 diag: holds ended 372 (on the timeout flag 3, evidence 363, both 0, neither 6); held unit's s the step before, median 1.06; timeout firings while held 4017, of which ended the hold 3; valued holds ended 217, neutral holds ended 155
      H21 diag: revision, first hold neutral and later held valued 98/115 = 0.852; no whiff of either plume in the last third 23; no navigation hit in the last third 30; wall contacts per row 0.27
      secondary, first reach and diagnostics:

   [priority-identity] G 2.0  V 275  N 112  no-choice 13  (of 400)
      cells: 0 odour A valued, +y: V 70 N 27 0 3 | 1 odour A valued, -y: V 66 N 31 0 3 | 2 odour B valued, +y: V 70 N 26 0 4 | 3 odour B valued, -y: V 69 N 28 0 3
      P(V | reached) 275/387 = 0.711 [0.664, 0.754]; first-approach step median V 32 N 31; dwell median valued 22.0 other 0.0; contacts/row 0.27; no whiff in the last third 23
      first hold: valued 285 neutral 115 none 0, step median 12; hold changes mean 0.48; agreement: first hold == source reached 225/387, held at reach == source reached 219/387 (nothing held at reach 111); P(V | first hold valued) 199/285; P(V | first hold neutral) 76/115
      whiffs/row: valued plume 10.0 neutral plume 3.5 both same step 0.04; no-choice rows' hold history: never 0 valued only 0 neutral only 12 both 1
      input range: y' max 5.34, y' > 1.8 on 3.86% of (row, step, channel), s >= 4.9 on 0.01% of (row, step), s max 4.93
      segments, N rows: neutral selected first and held at reach 7; valued held earlier, neutral held at reach 0; valued held at reach yet neutral reached first 53; nothing held at reach 52 | V rows: valued held at reach 212 (of which first hold was neutral 38), neutral held at reach 4, nothing held 59

== criteria (design v2 section 7; 95 percent, one evaluation, no extension; aggregation: PASS if every part passes, FAIL if any fails, else INCONCLUSIVE) ==
   M1(a) neutral: ties 10/400 = 0.025  at most 0.20 -> PASS
   M1(a) pathway-off: ties 10/400 = 0.025  at most 0.20 -> PASS
   M1(a) known-answer: ties 1/400 = 0.003  at most 0.20 -> PASS
   M1(b) neutral, P(+y source majority | chose): P k 204 n 390  value 0.523  95% interval [0.474, 0.572]  within [0.35, 0.65] -> PASS
   M1(c) floor: pathway-off, P(V | chose): P k 204 n 390  value 0.523  95% interval [0.474, 0.572]  within [0.35, 0.65] -> PASS
   M1(d) ceiling: known-answer, P(V) over all rows: P k 380 n 400  value 0.950  95% interval [0.924, 0.967]  at least 0.85 -> PASS
   M1 -> PASS
   M2(a) maintain, P(V) over all rows: P k 300 n 400  value 0.750  95% interval [0.705, 0.790]  at least 0.7 -> PASS
   M2(b) maintain, cell 0 (odour A valued, +y), P(V): P k 86 n 100  value 0.860  95% interval [0.779, 0.915]  at least 0.55 -> PASS
   M2(b) maintain, cell 1 (odour A valued, -y), P(V): P k 70 n 100  value 0.700  95% interval [0.604, 0.781]  at least 0.55 -> PASS
   M2(b) maintain, cell 2 (odour B valued, +y), P(V): P k 76 n 100  value 0.760  95% interval [0.668, 0.833]  at least 0.55 -> PASS
   M2(b) maintain, cell 3 (odour B valued, -y), P(V): P k 68 n 100  value 0.680  95% interval [0.583, 0.763]  at least 0.55 -> PASS
   M2(c) DP = P(V) maintain - rule-off, same rows: DP n 400  value 0.180  95% interval [0.143, 0.218]  at least 0.15 -> INCONCLUSIVE
   M2 -> INCONCLUSIVE
      reported, no bar: DP maintain - pathway-off +0.240 [+0.198, +0.283]
      reported: maintain N 96 tie 4; P(V) maintain / known-answer = 0.750 / 0.950 = 0.789 of the ceiling
      reported: rule-only P(V) 241/400 = 0.603 [0.554, 0.649]; DP rule-only - pathway-off +0.093 [+0.065, +0.122]
      reported, secondary first reach, maintain: V 208 N 192 none 0; P(V first) 208/400 = 0.520 [0.471, 0.569]
      reported, secondary first reach, rule-off: V 208 N 192 none 0; P(V first) 208/400 = 0.520 [0.471, 0.569]
      reported, secondary first reach, pathway-off: V 206 N 194 none 0; P(V first) 206/400 = 0.515 [0.466, 0.564]
      reported, secondary first reach, known-answer: V 217 N 183 none 0; P(V first) 217/400 = 0.542 [0.494, 0.591]
   M3 identities: (i) neutral at G 2.0 with the rule == G 0 True, G 0 == ph14.Agent3 True; (ii) priority-identity == ph16.Agent4 at +1/-1 True; (iii) rule-off == ph16.Agent4 at +1/0 True; (iv) known-answer h = valued and hit = its whiffs True -> PASS
   M4 mechanism bench (a), re-run here with the bench seeds: kept lower bound 0.990 over 400 holding rows >= 0.95 -> PASS
   M5 avoidance: +1/-1 agent is the Run 2 agent by construction (M3 ii True); constructed state: negative odour held on 300 (row, step), target = flee side on every one, equal to G 0's on the 300 steps both hold it; the valued odour took the hold on 250 afterwards -> PASS
   M6(a) no whiff of either plume in the last third, maintain - rule-off: DP n 400  value -0.003  95% interval [-0.008, 0.000]  at most 0.05 -> PASS
   M6(b) maintain, wall contacts per row: mean 0.000  at most 0.10 -> PASS
   M6 -> PASS      reported: no whiff in the last third maintain 3 rule-off 4 rule-only 2 known-answer 2; no navigation hit in the last third maintain 7, rule-off 4, rule-only 5, pathway-off 2, neutral 2, known-answer 14, priority-identity 30; rule-only contacts per row 0.00

== H21 ==  M1 PASS  M2 INCONCLUSIVE  M3 PASS  M4 PASS  M5 PASS  M6 PASS  -> NOT shown under the registered criteria

## Appendix B: ph19_bench.txt in full (sha256 c11977e421b73d6fb24ce15e2dd318d14c20ac910256edf9cdaff332d1605fa3)

== H21 mechanism bench (design section 4). design v2 FINAL doc d7fd5abcc95169698 hash e83c9de2acba49d65893000f453ee384134ab33a3c916466010327736535965a; this file sha256 00c6a3b32f80fae9f58b6dbd23a8e03b1710be45fcf335238f289567fce34791; {'rows': 400, 'phase1': 60, 'phase2': 200, 'p_hold': 0.3, 'p_other': (0.3, 0.057), 'seed_w': 20260926, 'seed_a': 20260927} ==
(a) maintenance: phase 1 channel 0 (+1) alone, phase 2 channel 1 (0) alone, channel 0 silent; statistic = held channel 0 on EVERY phase-2 step, over the rows holding it at step 60
   G 2.0 rule on  p_other 0.300: holding channel 0 at step 60: 400/400 (nothing 0, channel 1 0); kept on every phase-2 step 400/400 = 1.000 [0.990, 1.000]; timeout firings in phase 2 1649, ended the hold 0; held unit's s in phase 2 median 1.95 min 1.48; y'' max 5.34, y'' > 1.8 10.77%, s >= 4.9 4.29%, s max 4.99
   G 2.0 rule on  p_other 0.057: holding channel 0 at step 60: 400/400 (nothing 0, channel 1 0); kept on every phase-2 step 400/400 = 1.000 [0.990, 1.000]; timeout firings in phase 2 1649, ended the hold 0; held unit's s in phase 2 median 1.95 min 1.48; y'' max 5.34, y'' > 1.8 11.10%, s >= 4.9 4.72%, s max 4.99
   G 2.0 rule off p_other 0.300: holding channel 0 at step 60: 400/400 (nothing 0, channel 1 0); kept on every phase-2 step 0/400 = 0.000 [0.000, 0.010]; timeout firings in phase 2 0, ended the hold 0; held unit's s in phase 2 median 0.00 min 0.00; y'' max 5.34, y'' > 1.8 10.77%, s >= 4.9 4.29%, s max 4.99
   G 2.0 rule off p_other 0.057: holding channel 0 at step 60: 400/400 (nothing 0, channel 1 0); kept on every phase-2 step 0/400 = 0.000 [0.000, 0.010]; timeout firings in phase 2 706, ended the hold 0; held unit's s in phase 2 median 0.00 min 0.00; y'' max 5.34, y'' > 1.8 11.10%, s >= 4.9 4.72%, s max 4.99
   G 0.0 rule on  p_other 0.300: holding channel 0 at step 60: 400/400 (nothing 0, channel 1 0); kept on every phase-2 step 400/400 = 1.000 [0.990, 1.000]; timeout firings in phase 2 1649, ended the hold 0; held unit's s in phase 2 median 1.95 min 1.48; y'' max 1.78, y'' > 1.8 0.00%, s >= 4.9 0.00%, s max 3.75
   G 0.0 rule on  p_other 0.057: holding channel 0 at step 60: 400/400 (nothing 0, channel 1 0); kept on every phase-2 step 400/400 = 1.000 [0.990, 1.000]; timeout firings in phase 2 1649, ended the hold 0; held unit's s in phase 2 median 1.95 min 1.48; y'' max 1.78, y'' > 1.8 0.00%, s >= 4.9 0.00%, s max 3.75
   G 0.0 rule off p_other 0.300: holding channel 0 at step 60: 400/400 (nothing 0, channel 1 0); kept on every phase-2 step 0/400 = 0.000 [0.000, 0.010]; timeout firings in phase 2 0, ended the hold 0; held unit's s in phase 2 median 0.00 min 0.00; y'' max 1.78, y'' > 1.8 0.00%, s >= 4.9 0.00%, s max 3.77
   G 0.0 rule off p_other 0.057: holding channel 0 at step 60: 400/400 (nothing 0, channel 1 0); kept on every phase-2 step 0/400 = 0.000 [0.000, 0.010]; timeout firings in phase 2 718, ended the hold 0; held unit's s in phase 2 median 0.00 min 0.00; y'' max 1.78, y'' > 1.8 0.00%, s >= 4.9 0.00%, s max 3.75
(b) asymmetry, identity: neutral (channel 1, value 0) held first, then channel 0 (+1) alone: circuit states bitwise equal to the Run 2 agent's True; rows holding channel 1 at step 60: 400; revised to channel 0 within phase 2: 400 (both agents)
(c) inertness, identity: values 0/0, both channels p 0.3, 200 steps: bitwise equal to the Run 2 agent's True
(c) inertness, identity: values +1/+1, both channels p 0.3, 200 steps: bitwise equal to the Run 2 agent's True
(c) inertness, identity: values +1/-1, both channels p 0.3, 200 steps: bitwise equal to the Run 2 agent's True
== M4: (a) at G 2.0 with the rule, p_other 0.3: lower bound 0.990 >= 0.95 over 400 holding rows -> PASS; (b) identity True; (c) identities [True, True, True] -> PASS: the task may be run ==
