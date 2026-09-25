# H27 design v1 DRAFT: a third, irrelevant odour as a distractor, on the adopted agent (Agent14N2); does the hold keep navigation on the relevant plume?

Date 2026-09-25. Status: **v1 DRAFT, for the owner's confirmation (section 12). No code.** Opened for design by the owner on 2026-09-25, verbatim '1. shown으로 종결 및 n2는 범위 권고안으로 적용 2. 미입증안 해결책이 없나? 3,4 권고안으로 진행' (gloss: '1. close as shown, and apply N2 with the recommended scope; 2. is there no resolution for the not-shown ones?; 3 and 4: proceed with the recommended options'), point 4, the recommended option: the next item in the queue (decision:h27-open-design). The same message closed H20 Stage C Run 2 as shown (decision:h20-stage-c-run2-closed), adopted the value-gated release (decision:n2-release-adopted-within-tested-conditions), closed H20 as a whole (decision:h20-closed) and set the seed-scan exception (decision:seed-scan-exclusion-ph31-eval). The queue bullet this draws on reads 'A proper distractor condition (a third, irrelevant odour), which is what the hold's benefit needs; it changes the circuit's size and Phase 2's calibration' (master_plan.md, queue). It had no number; the highest in use is H26, so this design is **H27**. Concept: concept:h27-irrelevant-odour-distractor. Templates: H26 design v1 (doc d9452710c5166ba01, experiments/h26/h26_design_v1.md) for the form of a new hypothesis on the adopted agent; H20 Stage C Run 2 design v2 FINAL (doc d007990ab333e7194) for the claim labels and the self-review.

Code citations are repo-relative path:line at HEAD 8c50e9f; sha256 prefixes: ph2.py (Circuit, Upstream), ph11.py, ph14.py, ph16.py, ph19.py, ph21.py, ph23.py ae180492, ph24.py f344f178, ph28.py 64ce7d0c, ph30.py 98822834. Measurement citations: "H26 eval" is experiments/h26/h26_report.md (record:h26-result); "H19 out:N" is line N of experiments/h19/ph14_h19.txt; "Phase 2 report" is doc de3ea628db7e716f1 (H6, H7). Every claim is labelled **measured** (a recorded number), **read** (a cited code line) or **inferred** (arithmetic or reasoning on read or measured quantities). No code was written or run for this draft; the only things run were the seed scan (section 9) and checks on this file (sha256, a character check for dashes). Pass probabilities are hand arithmetic with normal approximations, stated where used.

## 0. What is new

| item | the adopted agent (Agent14N2) as tested | H27 (this draft) | why (section) |
|---|---|---|---|
| odours | two channels: the valued odour V and the neutral odour B | **three channels**: V, B and a third odour D, value 0, never reinforced, arriving as background whiffs | the queue bullet; the hold's benefit (2.1) |
| agent | Agent14N2 = ReleaseN2 + Agent14 (ph30.py:139-140) | **Agent15**: Agent14N2 composed with N = 3 in a new file (src/ph32.py); no adopted file edited | ph11.py:112-116, ph23.py:57, :68, ph28.py:97 hard-code two channels (3.2) |
| evidence release | compares the held channel with `other = 1 - hi` (ph23.py:68) | compares it with the **strongest non-held channel**; identical at N 2 | at N 3, `1 - hi` is wrong (3.2); a composition rule for the owner to sign (3.4) |
| presence counter | one per odour, start 240, window 300 (ph28.py:97, ph23.py:83-85) | **the same rule for the third odour** | the H26 relaxation re-signed in form for Agent15 (3.4) |
| worlds | World7 T1, W1, T3a | T1, W1 and T3a **with the D background** (T1D, W1D, T3aD), each also without it | 4, 5 |
| arms | | adds a **hold-not-read arm** (the hold's benefit) and a release-off arm (reported) | 6 |
| seeds | | new (section 9) | |

## 1. Hypothesis

With a third, irrelevant odour D (value 0 in the agent's read-out, never reinforced, arriving as background whiffs at p_D per step anywhere in the arena), the adopted agent, composed with three channels (Agent15), (i) keeps its choice in the H21 task within an allowed gap of the same agent without D on the same rows; (ii) in the absent-odour world W1, where the valued odour never appears and B and D tie at the top value, keeps tracking B within an allowed gap of its distractor-free performance; and (iii) there, does so better than the same agent whose navigation and flee do not read the hold (the hold's benefit).

Stated narrowly: a statement about supplied values +1/0/0, G 2, C0, the adopted modules (gain, gate, filter with the presence counter, the N2 release), learning off, the D background at the registered rate. Not about learning (the value D would acquire; excluded, section 11).

## 2. The measured reason

### 2.1 The hold's benefit is open, and the record says why a distractor is what it needs

- **Open on record.** master_plan.md, architecture, selection and hold: 'Open: whether the hold earns its place. In H15 Run 2 the agent without it left 132 of 400 unrecovered against 21 of 400, with a rewarding dwell of 17.3 against 23.0; no distractor condition exists, so its distractor resistance is unverified' (**measured** numbers of H15 Run 2). H19 (a)'s known condition: late unrecovered full 16.0 percent, fix 4.5 percent, **no-hold 25.5 percent** (H19 out:15, :18, :21), while the rewarding dwell of fix vs no-hold was 23.7 vs 21.7, 'wins 57.5 percent, no' (H19 out:45) (**measured**; Agent3, World5, +1/-1, 5400 steps: not carried to this agent or world, section 13).
- **H19 (a)'s distractor condition N6 is unreadable.** Its background was the PUNISHED odour at p 0.03 (H19 out:25), which is a punisher everywhere: every arm at the floor, late unrecovered 91.5 / 94.5 / 100.0 percent (H19 out:46-49) (**measured**). The standing rule since: 'a distractor must be irrelevant: with two odour channels I made the background the punished odour' (master_plan.md, standing rules). A third channel is the only way to add an irrelevant odour without replacing one of the two task odours.
- **Every adopted readout pathway lists 'any distractor condition' as not validated:** the H21 gate (decision:h21-gate-adopted-within-tested-conditions), the H26 counter and Agent14 (decision:h26-adaptive-presence-adopted-within-tested-conditions), Stage B (decision:h20-stage-b-closed), N2 (decision:n2-release-adopted-within-tested-conditions); H19 (a) 'not covered: whiffs of B while A is held, and any condition with a distractor' (architecture).
- **The owner's boundary** (notes/module_boundary_outlook.md, doc d8dbff6b70830a8c5): the reusable core is recognition (normalisation, select-and-hold) and value memory, not the navigation. A distractor tests recognition directly.

### 2.2 A new reading from the code: at +1/0 the adopted agent's trajectory does not depend on the hold (read)

In Agent9.act (the base act of Agent14 and Agent14N2), navigation is `nav = where(keep, hit, (whiffs & top).any(1))` (ph23.py:92), with `top` the present odours at the top non-negative value (ph23.py:88-89), `keep` = something is held and its value is the present maximum or negative (ph23.py:91), `hit` the held odour's whiff (ph23.py:78). The flee reads the held value only when it is negative (ph23.py:77, :100). At values +1/0:
- while V is present, top = {V}; whether V, B or nothing is held, nav equals the V whiff (keep with V held gives V's whiff; any other case gives (whiffs & top) = V's whiff);
- while V is absent (not sensed for 300 steps after a whiff, or never sensed after step 58, ph23.py:83-85, ph28.py:97), top = {B}; with B held, keep gives B's whiff; with nothing or V held, (whiffs & top) gives B's whiff.
So at +1/0 in two-channel worlds nav is the whiff of the top present odour whatever the circuit holds, no flee occurs, and every other input to the turn (the cast clock ph23.py:95, 97-98; the wind estimate; the turn noise ph23.py:102) does not read the hold. **The hold has no behavioural role in the adopted agent at +1/0.** This agrees with what was accepted at H23 ('at +1/0 navigation is the known-answer arm's law and does not depend on the circuit', decision:h23-closed) and with H26's W1 identities (Agent10g == Agent6 row for row, H26 eval). It is the reason the hold's benefit cannot be measured on the present worlds.

With a third odour D at value 0, whenever V is absent top = {B, D} (a tie at the top value): with B held, keep holds and nav is B's whiff only; with D held, nav is D's whiff only; with nothing held, any B or D whiff steers. **The hold decides which of two equal-valued odours steers.** That is the condition a distractor creates and the one H27 registers.

### 2.3 What a third odour does to each adopted module (read)

| module | code | at N 3 |
|---|---|---|
| upstream stage (Heeger, Phase 2.1) | ph2.py:5-17; the cross-channel term is the MEAN over the other channels, divisor N - 1 (ph2.py:16) | the third channel is a column; with one other channel active its cross-suppression is half of what it is at N 2 (k P_j / 2 against k P_j): a circuit-input change, not a trajectory change at +1/0 (2.2) |
| selection circuit (ph2.Circuit) | n generic (ph2.py:24-30); the pool sums every unit (ph2.py:33-34); noise drawn with shape (R, n) from the agent's shared generator (ph2.py:40; the generator passed at ph11.py:113) | a third unit; its noise-level state enters the pool; with the shared generator every later draw of that generator (ring noise, turn noise ph23.py:102) shifts, so a separate generator for the third unit is recommended (3.3) |
| Phase 2's calibration | net drive at the uniform baseline 0.4945 at N 2, 0.3308 at N 3 (0.92 and 0.62 of x* 0.537); on the hard cue 24 wrong at N 2, 14 at N 3 (Phase 2 report, 2.2; **measured**, uniform input, not the agent's regime) | measured again in the agent's regime at bench (b) |
| odour codes | two codes, odour(101), odour(102) (ph11.py:116); drawn from their own seed (ph4.py:29-31) | a third code odour(103); no draw of the agent's generator; unused with supplied values |
| H19 (a) | superseded on nav by the filter lines (ph23.py:90-92; nav6 is measurement only) | in the filter-off arm (Agent15g) any non-negative whiff with nothing held steers (ph19.py:63), D included |
| H21 gate | ph23.py:64-66, generic over channels | V held: B and D gated (0 < 1); B held: D not gated (equal values); D held: B not gated |
| H23 filter, 'top-valued non-negative' | ph23.py:79, :88-92, generic | V present: top = {V}; V absent: top = {B, D} (2.2) |
| H26 presence counter | ph23.py:83-85; start 240 with shape (R, 2) (ph28.py:97) | a third counter c_D starting at 240: D is present on steps 0-58 by the prior, and 300 steps after any D whiff |
| H25 release with N2 | ph24.py:54-63; ph30.py:117-136, generic (reads held(), sel.s.any(1)) | a D hold (value 0, non-negative) is released as a B hold is, 48 steps after its last whiff |
| evidence release | `other = 1 - hi` (ph23.py:68; the same line ph16.py:79, ph19.py:52, ph21.py:58) | **wrong at N 3**: hi = 2 gives other = -1, the held channel itself (NumPy negative index), and hi = 0 never compares D; must be generalised (3.2) |
| read-out | chan_valence returns `known` of any width (ph14.py:52-53); the learned branch stacks two columns (ph14.py:55) | supplied values only; the learned branch is not used |
| worlds and harness | World2 two sources and two columns (ph11.py:64, :76-77); World7 (ph16.py:43-56); ph22.Masked; the run arrays (R, 2) (ph23.py:131, :140) | a new world class adds a D column; a new harness |

### 2.4 What the hold does against D, as far as the record goes

- **The circuit resists an amplitude distractor on a bench** (Phase 2 report 2.1, **measured**): with the upstream stage a held state survives a delay distractor of amplitude 1 to 10 in 1.00 of runs, because the stage cannot emit more than Rmax 1.8 and the winner suppresses by 2.0.
- **In the agent, holds are lost to the other odour's whiffs** (record:unrecovered-excess-diagnosis-result, **measured**): of 566 losses of the hold none came from the silence timeout and 94-95 percent followed a whiff of the other odour. H20 Run 2's diagnosis: holds end when the held unit has already decayed to the threshold (s median 1.06 the step before), and the other odour's response lowers the held unit through the pool (record:h20-run2-diagnosis; the mechanism part labelled an interpretation there).
- **A single unbiased whiff does not form a hold from rest** (0.756 of threshold; record:h20-post-bench-diagnosis-result, **measured**). D at value 0 gets no gain, so a D hold needs whiffs in quick succession (**inferred**: at p_D 0.03 a second D whiff within 5 steps has probability about 1 - 0.97^5 = 0.14).
- **The release ends a hold 48 steps after its odour's last whiff** (H25; record:h25-bench-result, **measured**). **Inferred risk, stated before any run:** after a B hold is released (the agent has left B's plume for 48 steps), nothing is held; with V absent every D whiff then steers (2.2) and resets the cast clock (ph23.py:95); the return cast's offset grows about 1.2 degrees per step (MAXOFF 170 over SAT 141.7 steps, ph12.py:29), so with D whiffs every 33 steps on average (p_D 0.03) the offset rarely passes about 40 degrees and the agent keeps moving upwind, away from a plume that lies downwind of its source. The distractor-free agent's return cast would instead swing back. So D is expected to cost W1 dwell and lost rows in the phases where nothing is held; the size is not on record. A release-off arm is reported to show this part (6).

## 3. The change

### 3.1 The world: where the third odour comes from (choices, evaluated from the record)

- **(i) RECOMMENDED: a background odour D.** Each row and step, a D whiff with probability p_D anywhere, independent of position, drawn from its own generator (world seed + 30000), so World7's own draws are unchanged. D has no location, cannot be approached or avoided and carries no information: an irrelevant input on a non-target channel, the analogue of Phase 2's distractor. p_D: **0.03 recommended**, H19 (a)'s registered rate (H19 out:25), so the only change from N6 is the distractor's identity and value; about half the plume rate at the task start (0.3 exp(-20/12) = 0.057, ph11.py:80-84 with LAM 12, ph9.py:34) and a tenth of the rate within 3.0 of a source (0.30). Alternatives: 0.01 (weaker), 0.057 (equal to the start rate).
- **(ii) Rejected for H27: a third neutral source in World7.** It changes the geometry (a third cone; where it sits relative to the midline start changes arrival order and first holds; the link-check rule: a geometry is checked by a known-answer arm before it is registered, master_plan.md standing rules), turns the task into a three-option choice (H7's option-count limit, record:exp5-h7-option-count-limit) and needs a three-class dwell-majority measure. Kept as a later step.
- **(iii) Rejected: H19 (a)'s condition (a background of the punished odour).** It is a punisher everywhere and floored every arm (H19 out:46-49); the standing rule.

### 3.2 The agent: Agent15 (code not written here)

A new file src/ph32.py, importing the adopted modules unchanged. **No adopted file is edited.** Agent15 is Agent14N2 with:
- **(A) the constructor**: after the adopted constructor runs (so every construction draw of the agent's generator is unchanged), the upstream stage is rebuilt with chans 3 (replacing ph11.py:112), the circuit with n 3 (replacing ph11.py:113; see 3.3 for its noise), the codes with a third code odour(103) (ph11.py:116), and the presence counter as a (R, 3) array at 240 (replacing ph28.py:97).
- **(B) the act**: a class placed where Agent9.act sits in the method order (so ReleaseN2 wraps it unchanged, ph30.py:124), repeating Agent9.act's lines (ph23.py:60-104) with ONE line generalised: the evidence release compares the held channel with the strongest non-held channel, `due_evidence = committed & (max over j != hi of y_j - y_hi > MARGIN)`, in place of `other = 1 - hi` (ph23.py:68, :70). At N 2 the maximum over one other channel is that channel, so the line is identical (checked, identity (I1)). This is the N 3 meaning of an adopted rule, so it is put to the owner as a composition rule in H14 format (3.4), not changed silently.
- **Alternative, not recommended:** edit ph23.py:68 in place to the general form. It would be bitwise at N 2 but changes an adopted file whose sha256 is on record in every later record that imports it. A code change in an adopted module is the owner's decision; this design does not propose it.

### 3.3 The third unit's noise

- **RECOMMENDED: a separate generator (agent seed + 30000) for the third unit's noise**; the first two units draw from the agent's generator exactly as now (standard_normal((R, 2)) draws the same values in the same order). Then the agent's shared generator is consumed exactly as in Agent14N2, and by 2.2 **Agent15 without D has the trajectory of Agent14N2 on every row** (read; identity (I3)). The two model changes (the third unit in the pool, the mean divisor) remain and are measured on circuit fields, not hidden.
- Alternative: the shared generator with shape (R, 3). Every later draw shifts, so Agent15 without D and Agent14N2 differ by their random streams from step 0 and the size change can only be read as a paired DP.
- The upstream divisor (ph2.py:16) is **kept as adopted** (recommended). Alternative: k scaled to 1.6 so that one active other channel suppresses as at N 2: a parameter change of an adopted module, which reopens Phase 2's bench; not recommended.

### 3.4 What the owner signs before any code (H14 format)

1. **The evidence release at N channels, a composition rule, H27 only.** OLD: `due_evidence = committed & (y[other] - y[hi] > MARGIN)` with `other = 1 - hi` (ph23.py:68, :70; two channels). NEW: `due_evidence = committed & (max over j != hi of y_j - y[hi] > MARGIN)`. ANCHOR: identical at N 2 (identity (I1) on every field); the Phase 5 Run 2 release condition it generalises ('another channel exceeds the held one by MARGIN'). Scope: H27.
2. **The H26 relaxation re-signed in form for Agent15.** decision:classification-rule-relaxed-presence-prior-h26 (one presence counter per odour, window 300, start 240 as a prior, no other sensory history) stays in force for the adopted agent's counter; 'any wider use (another counter, another window, another agent) is a new decision' (decision:h26-adaptive-presence-adopted-within-tested-conditions). A third odour's counter on Agent15 is the same rule on another agent. OLD / NEW / ANCHOR identical to the H26 relaxation; scope H27. No other state is added: one unit, one code and one counter per odour, as for the two odours now.

No classification-rule relaxation beyond the re-sign in form is expected, and none is proposed.

## 4. Mechanism bench (constructed states and bench seeds; before any task seed)

Bench seeds 20261121 (world) / 20261122 (agent), bootstrap 20261123, 400 rows.
- **(a) Identities** (every field unless stated):
  - (I1) Agent15's code at N 2 (two channels, the generalised line) == Agent14N2 on every field in T1, W1, T3a and at 0/0 and +1/-1 (the generalisation is exact at N 2).
  - (I2) Agent15 with D on == Agent15 with D off, per row, on every field up to that row's first D whiff (D drawn from its own generator; the world's plume draws equal the D-free twin's, as ph22's masked twin check).
  - (I3) Agent15 with D off == Agent14N2 on the trajectory fields (POS, HEAD, NAV, SINCE, W for V and B, TURN, EST) in every row of T1, W1 and T3a (2.2 and 3.3); circuit fields (S, H, SG, SIL, TO, EV) reported, not claimed.
  - (I4) the hold-not-read arm with D off == Agent15 with D off on the trajectory fields in T1, W1, T3a (2.2: the hold has no behavioural role at +1/0 without D).
  - (I5) T1 with D: in every row in which V is present on every step, Agent15 with D on == with D off on the trajectory fields (2.2).
  - (I6) W1D and T3aD: nav False on steps 0-58; the first surge is the first B or D whiff at or after step 59, every row; no flee command in any arm at +1/0/0.
- **(b) The circuit at N 3 on constructed inputs** (the Agent15 stub, still world): (b1) a single whiff from rest on each channel, at values 0 and +1 (G 2): peak s and whether a hold forms, against N 2 (an unbiased whiff 0.756 of threshold, a biased one holds; record:h20-post-bench-diagnosis-result); (b2) a held unit at s 2.0 under D-only input at p 0.03 and p 0.30 for 200 steps: with V held (D gated) and with B held (D not gated, equal values), rows still holding at 200 (the H21 bench (a) form); (b3) the evidence release exact: with each channel held and constructed y, due_evidence fires exactly when the strongest other channel exceeds the held one by more than 0.2.
- **(c) Filter, gate, counter, release with three values** (constructed states, exact): top at (+1, 0, 0) with V present and absent; the gate's mask for each held channel; the three counters (start 240, reset on a whiff, present iff c < 300 or held); (S) and (Z) on a D hold (value 0: applied) at step 48 after its last whiff.
- **(d) The D stream**: whiff fraction per row and step within the Wilson interval of p_D; D independent of position (D fraction inside and outside the cones equal within the interval).
- **(m) printed first**: T1 rows in which V is ever absent (no V whiff by step 58, or a V silence over 300 steps), for Agent15 with D off; H26's count 20 at-risk rows (H26 eval) is the reference.
- **(h) T1D stop rule**: the pass probability of M2(b) at the bench DP (section 7 formula); STOP if below 0.5.
- **(hW) W1D stop rule**: the pass probabilities of M5(b) (with the bar fixed from the bench by the rule of section 7) and M5(d) at the bench values; STOP if either is below 0.5.
- **(hH) the hold's benefit stop rule**: the pass probability of M6 at the bench DP; STOP if below 0.5.
- **No-candidate rule**: (a) not all True, or (b3), (c), (d) failing, is an implementation error fixed before the bench continues; a stop rule firing ends the run before any development seed is used, the verdict is 'stopped at the bench', and nothing is tuned.

## 5. Tasks

- **T1D, the H21 choice task with the distractor**: World7 as registered (two sources SEP 10 apart crosswind, the start on the midline DOWN 20 downwind, 160 x 160 with reflecting walls, the cone plume, heading uniform, 2 x 2 balance by the seeded permutation, initial cast side drawn per row; ph16.py:24, :35-56), plus the D background (3.1); values V +1, B 0, D 0; 400 rows x 600 steps; dwell majority V, N or tie. **T1**, the same without D, for the reference and M1.
- **W1D, the absent-odour world with the distractor**: ph22.Masked (V's column silenced after World7 draws it), plus D; values +1/0/0; 600 steps; main measures dwell within 3.0 of B over 600 steps and lost rows (no B whiff in the last third, steps 400-599). **W1** without D for the reference.
- **T3aD, the constructed loss with the distractor**: V masked from step 0, the agent at V's source with a V hold constructed (s 2.0), plus D; 600 steps; neutral dwell over steps 100-599: **REPORTED** (with (I6) as its registered exactness).
- **T4, +1/-1/0 (World7, with and without D): REPORTED**, outside the verdict: the adopted agent (N2) at supplied +1/-1 in World7 has not been run (decision:n2-release-adopted-within-tested-conditions, limit (1)); printed are P(V), lost rows, wall contacts per row, flee violations, for Agent14N2 and Agent15 with D.
- **The H15 world (World6, learning on): EXCLUDED.** With learning on, the value D acquires depends on its code's overlap with the others (Stage B: residuals of +0.1 to +0.3 where codes share units, decision:h20-stage-b-closed), so D would stop being irrelevant; and value landing on whatever is held when reinforcement arrives (the outlook's 2.2) is a separate question, a learning stage after this one (section 11).

## 6. Arms

| task | arm | agent | values | role |
|---|---|---|---|---|
| T1D | adopted, D on | Agent15 | +1/0/0 | main (M2 a, b, c) |
| T1 | adopted, D off | Agent15 | +1/0/0 | paired reference (M2 b) |
| T1 | adopted, two channels | Agent14N2 | +1/0 | identity (I3) |
| T1D | filter off, D on | Agent15g (Agent15 with the filter off: gain, gate, N2 release) | +1/0/0 | floor of the filter under D (M2 c) |
| T1D | hold not read, D on | Agent15, nav, flee, counter and release reading the per-step argmax of y above 0.05 (ph14.py:62-63) in place of the hold | +1/0/0 | reported |
| T1 | pathway-off, known-answer, neutral | as H26's M1 arms (two channels, no D) | +1/0, 0/0 | M1 validity |
| T1D | pathway-off and neutral with D | three-channel versions | +1/0/0, 0/0/0 | reported |
| W1D | adopted, D on | Agent15 | +1/0/0 | main (M5) |
| W1 | adopted, D off | Agent15 | +1/0/0 | paired reference (M5 b, d) |
| W1 | two channels | Agent14N2 | +1/0 | identity (I3) |
| W1D | hold not read, D on | as above | +1/0/0 | the hold's benefit (M6) |
| W1 | hold not read, D off | as above | +1/0/0 | identity (I4) |
| W1D | release off, D on | Agent15 with the release off (the frozen defect in force) | +1/0/0 | reported (2.4) |
| W1D | filter off, D on | Agent15g | +1/0/0 | reported |
| T3aD, T3a | Agent15 D on / off, hold not read D on | | +1/0/0 | reported; (I6) |
| T4 | Agent14N2; Agent15 D on | | +1/-1(/0) | reported |

The hold-not-read arm keeps the circuit, gate and release running (their draws of the agent's generator are needed for (I4)) and removes what reads the hold: val, hit, keep, nav's held clause and the counter's held clause take the per-step argmax instead. It is named for what it removes: the hold's persistence as read by navigation and the flee; not 'no circuit'.

## 7. Criteria, with pass probabilities

General rules (as H26): one statistic per criterion; Wilson intervals for counts; paired percentile bootstrap over rows, 5000 resamples, seed 20261123; 95 percent; one evaluation, no extension; a group under 50 rows unreadable; a multi-part criterion PASS if every part passes, FAIL if any fails, else INCONCLUSIVE. Pass probabilities by the project's arithmetic: a paired DP with discordant fraction b, sd = sqrt(b - DP^2), se = sd / 20, P = Phi((DP - bar) / se - 1.96) for a lower-bound bar and Phi((bar - DP) / se - 1.96) for an upper-bound bar; a paired mean with sd s, se = s / 20; a count by the normal approximation with continuity correction. Hand arithmetic.

- **M1 T1 validity (else UNREADABLE):** H26's M1 on T1 without D (ties <= 0.20 in neutral, pathway-off, known-answer; neutral side balance in [0.35, 0.65]; pathway-off P(V | chose) in [0.35, 0.65]; known-answer lower bound >= 0.85). H26 eval: ties 7/5/2, balance 0.509, 0.539, 0.948 (measured). Pass above 0.99. The D-on floors are reported.
- **M2 T1D (the choice under the distractor):**
  - (a) **REPORTED against 0.88, not a gate (recommended, section 12 point 4).** Agent15 with D on, P(V). Reason: the adopted agent's own P(V) varies across seed sets (0.927 H26 eval, 0.922 Stage B eval, 0.953 Stage B bench; measured), which alone puts 0.88's pass probability at 0.79 to 1.00 with no distractor effect (400 rows, P(X >= 365): at 0.953, z = 3.95; at 0.925, z = 1.04, 0.85; at 0.922, z = 0.80, 0.79); a 5-row cost from 0.925 gives 0.54. The distractor's claim is paired, (b). Alternative: keep 0.88 as a gate (H26's bar).
  - (b) paired DP Agent15 D on - Agent15 D off, **lower bound >= -0.05** (H26's M2(b) form). Prediction (inferred): by (I5) only rows in which V is ever absent can differ; the record gives 20 at-risk rows at H26's evaluation (k 5 out of V there) and 16 rows with a V silence over 300 steps (Agent11 N 300 `differs8` rows, H26 eval); so k, the net rows D moves out of V, is 0 to about 10, no centre; D may also move rows into V (upwind drift from the start carries the agent toward both sources). Pass probability (into V 0, b = k / 400): k 0-5: 1.000; 8: 0.990; 10: 0.893; 12: 0.650; 13: 0.506; 15: 0.26 (the H26 design's table, same formula and bar; one line checked: k 10, sd 0.1561, se 0.0078, Phi(3.20 - 1.96) = 0.89).
  - (c) paired DP Agent15 D on - Agent15g D on, lower bound >= +0.05 (H26's M2(c) form). H26 eval: Agent14 - Agent10g +0.292 [+0.243, +0.340] (measured); with D the filter-off agent follows D whiffs whenever nothing is held (ph19.py:63), so the DP is expected at least as large (inferred). Pass above 0.999.
- **M3 identities:** (I1)-(I6) on the task seeds, printed in the run (an implementation error, fixed before the evaluation, if any fails).
- **M4 bench:** section 4 PASS (identities, (b3), (c), (d)); about 1 if the implementation is correct.
- **M5 W1D (tracking B under the distractor):**
  - (a) reach within 3.0 of B at least once, lower bound >= 0.80 (k >= 336 of 400; H26's M5(a)). W1 without D 385/400 (H26 eval); an agent that never surges reached 0.860 by casting past (record:absent-odour-check-result). Pass 0.89 (at 0.860: mean 344, sd 6.94, z = 1.22) to 1.00.
  - (b) paired mean dwell at B, Agent15 D on - Agent15 D off, over 600 steps, **lower bound >= bar_W = -0.20 x D_off**, D_off the bench's W1 mean dwell of Agent15 without D (the H26 rule, decision:h26-t2-dwell-bar's form), fixed from the bench by a recorded decision (decision:h27-w1d-dwell-bar) before the development run. At H26's W1 dwell 23.782 (measured) the bar would be about -4.8. Prediction: a cost, no centre (2.4). Pass probability at bar -4.8 and per-row sd 9.85 (H26 eval's paired sd; the D sd may be larger), se 0.49: difference -2.0: 1.00; -3.0: 0.99; -3.5: 0.75; -4.0: 0.37; -4.5: 0.07.
  - (c) wall contacts per row <= 0.10 (H26's M5(c); 0.000 in every W1 arm, H26 eval). Inferred risk: the upwind drift of 2.4 may bring agents to the upwind wall; the bench prints it.
  - (d) lost rows (no B whiff in steps 400-599), paired DP Agent15 D on - Agent15 D off, **upper bound <= +0.05** (H26's M5(d) form, against the same agent without D). W1 without D 35/400 lost (H26 eval). Pass probability at k_L extra lost rows (out of lost 0): 5: 1.00; 10: 0.89; 12: 0.65; 13: 0.50; 15: 0.26 (the M2(b) table mirrored).
- **M6 the hold's benefit (W1D):** paired DP of lost rows, hold-not-read D on - Agent15 D on, **lower bound >= +0.05**: the hold removes at least 5 points of lost rows under the distractor. Anchor, not carried: H19 (a)'s known condition, no-hold 25.5 percent against fix 4.5 percent late unrecovered (H19 out:18, :21; another world and agent). Prediction: positive (2.2: with B held D does not steer; without the hold D steers whenever it is the latest whiff), no centre. Pass probability (b = DP, one-directional): DP 0.075: 0.50; 0.08: 0.60; 0.10: 0.91 (sd 0.300, se 0.015, Phi(3.33 - 1.96)); 0.15: 1.00. Without D it is exactly 0 by (I4), so the benefit, if any, is the distractor's.
- **M7 T3aD, M8 T4: REPORTED** (T3aD: neutral dwell 100-599 for the D-on, D-off and hold-not-read arms; its exactness is in (I6)).

**Joint pass probability** (parts treated as independent; an order of magnitude). M1 0.99 x M2(b) (1.00 at k <= 5; 0.89 at 10) x M2(c) about 1 x M3, M4 about 1 x M5(a) 0.89 to 1.00 x M5(b) x M5(c) x M5(d) x M6. The record gives no centre for M5(b), M5(d) and M6; the stop rules read each at the bench before any task seed. If the bench puts each at 0.95: about 0.99 x 1 x 0.95 x 0.95^3 = 0.81; at 0.75 each: about 0.40; at the stop rules' edge (0.5 each): about 0.12. The probability of reaching the evaluation is the probability that (h), (hW) and (hH) all continue; by 2.4 (hW) is the likeliest to stop the run.

**H27 verdict:** PASS iff M1 to M6 all PASS. Statement: 'with a third, irrelevant odour arriving as background whiffs at p_D, the adopted agent composed with three channels keeps its choice in the H21 task within 0.05 of itself without the distractor; in the absent-odour world it keeps tracking the only relevant plume within the registered dwell and lost-row gaps of itself without the distractor, and loses at least 5 points fewer rows than the same agent whose navigation does not read the hold.' Supplied +1/0/0, G 2, C0, learning off, these worlds, this p_D.

## 8. Unreadable conditions

M1 failing; ties above 0.20 in the adopted arm with or without D; a cell or group under 50 rows; M3 failing (an implementation error, fixed before the evaluation); M4 not run or not passed (tasks not run); the evidence-release composition rule or the relaxation re-sign not signed before code (no code); decision:h27-w1d-dwell-bar not recorded before the development run (tasks not run).

## 9. Seeds, sizes, order

Sizes: T1 and T1D, 400 x 600, the arms of section 6 (about 10 runs); W1 and W1D about 7; T3a and T3aD 3; T4 2. Bench 400 rows.

**Seeds (new):** development world 9937, agent 9947; evaluation world 2083, agent 2173; bench 20261121 / 20261122; bootstrap 20261123. Derived: world + 10000 (the cell permutation, ph16.py:50) 19937, 12083, 20271121; world + 30000 (the new D generator) 39937, 32083, 20291121; agent + 20000 (the cast draw, ph16.py:40) 29947, 22173, 20281122; agent + 30000 (the new third-unit noise generator) 39947, 32173, 20291122. Also checked: world + 20000 29937, 22083, 20281121, and the earlier designs' pattern numbers 30261121, 40261122. T1, W1, T3a and T4 share the development and evaluation seeds (as H26).

Check done 2026-09-25 for this v1, before this file or any other file carried the numbers:
- (1) Every file under the repository, recursive, .git and __pycache__ excluded, no exclusion by name except the one pair excluded by decision:seed-scan-exclusion-ph31-eval (experiments/h20/ph31_eval.txt with Stage C Run 1's E1 evaluation agent seed; the number is not written here, by that decision): **224 files**, pattern (?<!\d)(n)(?!\d), for the 7 seeds, 12 derived numbers and 5 extra checks. **No file contains any of the final numbers.** Candidates dropped for file hits: 9991, 9993, 9994, 9997, 9998 (the Stage C designs, regress files, H26 and H23 outputs, ph30.py), 2075 (the H24 Run 2 N sweep), 9981 (the H17 bench), 9941 (the H17 designs, the H21 outputs).
- (2) vinc_search in the team space, one query per number (the 24 final numbers and the replaced candidates): no full-text match for any final number (the rows returned were semantic neighbours carrying none of the numbers; the semantic arm ran, 'fts+vector'). **Graph hits, replaced conservatively:** 2071 matched the props of record:h21-result (replaced); 2079 matched a sha256 substring in the title of concept:doc.d501080d7ed485c2a (replaced); final evaluation world 2083.
- (3) Checked against every registered seed (master_plan.md and each design's section 9, including Stage C Run 1 and Run 2, Stage B, H26, H17 Run 1 and Run 2, H24 Run 2, H25, H24 and earlier): no final number equals or derives to any of them. Registered numbers are cited here by reference, not written, so that earlier scripts' self-checks are not given new matches.

The code's self-check repeats (1) before the first run, excluding by name the H27 files that carry the seeds (ph32.py, ph32_*.txt, h27_*.md), master_plan.md, notes/*.md and viewer/*, and the pair of decision:seed-scan-exclusion-ph31-eval (listed by reference in the script header).

**Order:** the owner confirms section 12 and signs 3.4's two records -> design v2 FINAL -> src/ph32.py (Agent15; no adopted file edited) -> self-checks -> bench (a)-(d), (m), (h), (hW), (hH) with the stop rules -> decision:h27-w1d-dwell-bar -> development run (operation errors only) -> one evaluation -> report. Nothing changes after the table.

## 10. Predictions, with the arithmetic

- **Bench:** (I1)-(I6) True (read); (b1) the pattern of N 2 (unbiased single whiffs below threshold, biased ones holding), with peaks changed a little by the divisor (inferred); (b2) with V held and D gated, 400/400 hold at 200 steps (the gate zeroes D's input, as H21's bench (a) 400/400); with B held and D equal-valued, most rows hold at p 0.03 (Phase 2's bound; single D whiffs cannot displace a held unit), fewer at 0.30 (sustained other-odour input lowered held units in H20 Run 2), no centre; (m) about 15 to 20 rows with V ever absent in T1 (H26: 15 bench, 20 eval).
- **T1D:** Agent15 D off == Agent14N2 in trajectory (I3), P(V) about 0.92 to 0.95 (three measurements); D on - D off 0 to -0.025 (k 0 to 10), possibly positive; Agent15g D on below H26's Agent10g 0.635.
- **W1D:** D off == Agent14N2's W1 (dwell about 23 to 24, reach about 385/400, lost about 35); D on: a dwell and lost-row cost (2.4), no centre; hold-not-read D on worse than Agent15 D on (2.2), no centre; release-off D on better than Agent15 D on if 2.4's reading is right (reported, an interpretation until measured).
- **What would make them wrong:** (1) D costs more than the allowed gaps in W1D because the release exposes the cast clock to D after 48 silent steps (2.4): (hW) stops the run; (2) D holds forming more often than 2.4's arithmetic (then the hold can hurt as well as help, M6 small or negative): (hH) stops; (3) the divisor or the third unit changing circuit fields more than expected: reported only, since (I3) protects the trajectory; (4) at-risk rows more numerous on the new seeds than 20: (m), (h).

## 11. What H27 does not test

Learning with the distractor (the value D would acquire through shared code units, and whether value lands on the odour held when reinforcement arrives: the core's credit assignment, a later stage); a negative or positive D; a third source and three-option choice (H7's limit); D correlated with a plume; other p_D (section 12 alternatives); dense input (the outlook's caveat); a loss after tracking (T3b, the H26 limit); cold start (H17); heading-cue loss (H18; the wind is sensed every step); +1/-1 beyond T4's report; whether a fly resists such a distractor (no fly finding is cited).

## 12. What the owner confirms (each with a RECOMMENDED option)

1. **The hypothesis and its number.** RECOMMENDED: H27 as in section 1, on Agent15 (Agent14N2 with three channels). Alternative: the distractor on the two-channel agent by replacing B with D (rejected: it removes the neutral odour the choice task needs).
2. **The world.** RECOMMENDED: (i), a background odour D at **p_D 0.03**, from its own generator. Alternatives: p_D 0.01 or 0.057; (ii) a third source (rejected for H27, 3.1).
3. **The code and the two records to sign (3.2-3.4).** RECOMMENDED: a new file src/ph32.py, no adopted file edited; the third unit's noise from its own generator; the upstream divisor kept as adopted; SIGN (a) the evidence-release composition rule (strongest non-held channel; identical at N 2), H27 only, and (b) the H26 relaxation re-signed in form for Agent15's third counter, H27 only. Proposed text for the owner's own words: 'H27 한정: 증거 해제는 보유 채널을 보유하지 않은 채널 중 가장 강한 것과 비교한다(N 2에서는 기존과 동일). H26 완화(냄새별 존재 카운터 1개, 창 300, 시작값 240)를 Agent15의 세 번째 냄새 카운터에 형식만 재서명한다.' Alternatives: edit ph23.py:68 in place (not recommended: an adopted file); the shared generator (the size change then read as a paired DP only); k scaled to 1.6 (not recommended: reopens Phase 2's bench).
4. **The bars.** RECOMMENDED: M1 as H26 (T1 without D); M2(a) REPORTED against 0.88, (b) -0.05, (c) +0.05; M5 (a) 0.80, (b) bar_W = -0.20 x D_off from the bench (decision:h27-w1d-dwell-bar), (c) 0.10, (d) +0.05; M6 +0.05 on lost rows. Alternatives: M2(a) as a gate at 0.88 (pass 0.54 to 1.00 by 7); M6 on dwell instead of lost rows; M6 reported only (then the verdict speaks to distractor resistance, not the hold's benefit).
5. **The arms.** RECOMMENDED: section 6, with the hold-not-read arm as defined (circuit running, its hold not read) and the release-off arm reported. Alternative: the hold removed by skipping the circuit (rejected: its draws shift the agent's generator and (I4) is lost).
6. **The stop rules.** RECOMMENDED: (h), (hW), (hH) at pass probability 0.5, (m) printed first. Alternative: (hH) reported without a stop.
7. **The tasks.** RECOMMENDED: T1D and W1D registered; T3aD and T4 reported (T4 is the first run of N2 at supplied +1/-1 in World7, reported only); the H15 world excluded (5).
8. **The seeds.** RECOMMENDED: development 9937/9947, evaluation 2083/2173, bench 20261121/20261122, bootstrap 20261123, derived as section 9 (224 files scanned; two graph collisions replaced).
9. **The order.** RECOMMENDED: H27, then the queue as ranked in master_plan.md (the H26 T3b limit, H12, H10, H18, H17).

## 13. Self-review (2026-09-25)

- **Every code claim cites a line:** the circuit and upstream ph2.py:5-17, :24-42 (divisor :16, pool :33-34, noise :40); the agent's two-channel constructor ph11.py:112-116; chan_valence ph14.py:52-55; the hold ablation ph14.py:62-63; H19 (a) ph19.py:63; the gain ph23.py:62; the gate ph23.py:64-66; the evidence release ph23.py:68, :70 (and ph16.py:79, ph19.py:52, ph21.py:58); the filter and presence ph23.py:79-92; the cast ph23.py:95-100; turn noise ph23.py:102; the counter start ph28.py:97; the release ph24.py:54-63; N2 ph30.py:117-140; World7 ph16.py:35-56; the plume ph11.py:74-84, ph9.py:34; SAT ph12.py:29; the codes ph4.py:29-31.
- **Measured vs read vs inferred.** Measured: H26's T1, W1 and at-risk numbers; H19 (a)'s known and N6 lines; H15 Run 2's no-hold figures; Phase 2's distractor and N tables; the hold-loss diagnosis; the single-whiff threshold. Read: 2.2 (the hold has no behavioural role at +1/0), 2.3, the identities (I1)-(I6), the `1 - hi` defect at N 3. Inferred: every pass probability, the D-hold rate, the upwind-drift risk of 2.4, the T1D population bound. Every read claim a bar rests on is an identity at the bench ((I3), (I4), (I5)) before any task seed.
- **The H24 lesson** (a design assumption about circuit dynamics must cite a bench or a code line; a recorded defect is in force until fixed). Guard: no bar rests on a presumed circuit event; the release's 48 steps (H25 bench) and the frozen defect at negative holds (N2, Stage C bench (n)) are cited; 2.4's drift is labelled an inferred risk and read at (hW) before any task seed; the `1 - hi` line is named as wrong at N 3, not presumed harmless.
- **The H17 lesson** (a prediction anchored on the wrong population). Guard: T1D's prediction is bounded by the population the code allows to differ (rows with V ever absent, (I5)), counted at (m) before (h) is read; H19's 25.5 percent is an anchor only, not a prediction, because it comes from another agent and world.
- **The H26 lesson** (an inherited prediction never checked against the benches). Guard: no inherited number is used as a prediction for a D arm; M2(a)'s inherited 0.88 is shown to pass with 0.79 to 1.00 at zero effect on the adopted agent's own three measurements, and is recommended as reported.
- **The Stage C Run 1 lesson** (a readability estimate borrowed from another agent). Guard: every reference number for an Agent15 arm is Agent14's or Agent14N2's own (identical by (I3)); none is taken from Agent3 or H19's agents.
- **The task's own premise corrected:** 'with the third channel silent the agent is bitwise Agent14N2 on every field' is not true of the code (ph2.py:16 and :33-34 change the circuit fields, and a shared generator would shift every draw); what holds, with the third unit's noise on its own generator, is identity on the trajectory fields (I3), plus full identity of the generalised code at N 2 (I1).
- **The risk is stated, not hidden:** by 2.4 the likeliest outcome may be a stop at (hW); that would still answer whether the adopted core resists an irrelevant odour, and the release-off arm would say where the cost sits.
- **No code written or run**; the only things run were the seed scan and checks on this file.
- Not tested: section 11.
