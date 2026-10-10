# (d) The hold's benefit, stage two on the coverage conditions (A5, B3, A6): design v2 FINAL

Date 2026-10-09. Status: **v2 FINAL, owner-confirmed before implementation and runs**. decision:hold-stage2-coverage-open.

Owner instruction, verbatim: '다음 권고안에 따라 작업 이어서진행한다.' (proceed with the recommended next work). The recommendations refer to both v1 section-12 lists reviewed in the preceding progress response.

## Confirmed choices and implementation readings

All ten RECOMMENDED options in v1 section 12 are confirmed: A5 and B3, T1 only, ReadOutFly actual/instant, identities I1-I7 including I6, negative-source dwell R-H as primary with its lower interval bound strictly above 0, P(V) H-R lower bound at least -0.05, lost rows reported, span at least 1.0 on the bench, pass-probability stops at 0.5, A6 reported only, no draw tape. No materiality-bar selection is pending. Bench stops end that condition before development; no tuning, extensions or evaluation repeats.

Implementation corrections fixed before any run: I2 lists NINE nonlearning rows A1-A6 and B1-B3; the words 'all eleven' in v1 include the two excluded learning rows and are corrected. I4 compares available trajectory and score fields, with unrecorded TURN/EST captured by taps. For I5, each row's instantaneous identity and projected command are checked up to and including its first post-step state/field divergence, while its pre-step state and sensory inputs agree. A first command difference that occurs only after latent state divergence has no stage-one coupled projection identity and is reported as outside that check, not as a failed identity or an equality claim. I2 and I3/I6 remain the zero-tolerance code controls. A genuine identity failure stops before any bench and is diagnosed before a correction/re-run.

Seeds: config/hold-stage2-seeds.json is the exact registration for bench, dev, eval and bootstrap, selected after the full repository digit-boundary scan and individual graph searches including the balance, cast, D_OFF and A3_OFF derived streams. Scan receipt: experiments/hold/hold_seed_registration.json. Identity checks reuse the spent aliases. Seeds are named by those config keys in reports.

Runtime: local Python 3.13.12, numpy 2.5.3, one process and BLAS threads 1. Every stage persists per-row evidence and source/config/design hashes. The reviewing session recomputes headline statistics from stored arrays before graph result registration. One evaluation only, on surviving conditions; A6 bench and evaluation are reported even if both benefit conditions stop.

## Preserved v1 specification

The v1 text below preserves the original proposal and alternatives for provenance. Its future-tense approval statements and section-12 alternatives are superseded by the confirmed choices above. No measured result is added to this FINAL.

# (d) The hold's benefit, stage two on the coverage conditions (A5, B3, A6): design v1 DRAFT

Date 2026-10-07. Status: **v1 DRAFT for the owner's confirmation (section 12). A design, not a run: no code, no seed chosen or used, no bar fixed, nothing adopted.**
Authority: decision:hold-stage2-coverage-proposal-allowed, the owner's answer to the stage-one gates, verbatim '1. 열도록 한다. 2. 허용한다.'; this design rests on point 2 only
(gloss 'it is allowed': a stage-two benefit proposal on the coverage conditions may be proposed). Point 1 is not interpreted here. Basis: the stage-one report
`experiments/hold/hold_stage1_report.md` and its design `notes/hold/2026-10-07-hold-benefit-stage1-design-v1.md` rev 2, on HEAD 1ce9b22. Template:
`experiments/h29/h29_design_v1.md`. Labels: **measured** (a recorded output, cited by file:line or JSON field), **read** (a code line at HEAD 1ce9b22), **inferred**
(arithmetic or reasoning from those).

## 0. What is new

Stage one compared, on the reference agent's own state, the command it gives when navigation reads the actual hold (H) with the command it would give when navigation
reads the instantaneous read-out (R: `q = argmax(y)` when `max(y) > 0.05`, else nothing, from the same step's gated `y`). Only H advanced. Commands differed only in the
three coverage strata, all outside the adopted scope (supplied +1/0, learning off). Stage two proposes the first **free-running** comparison: two embodied agents, H and
R, each advancing on its own actions, in A5 and B3; A6 reported only (section 8). It is a new estimand (section 5), not an extension of the local measurement, and its
result says nothing about the adopted scope.

## 1. Hypothesis, per condition

- **A5 (two-channel form, World7 T1, supplied +1/-1, learning off).** Reading the actual hold, rather than the instantaneous read-out, lowers the time spent at the
  negative source on the same rows (paired dwell at the negative source, R - H, greater than 0), and costs no more than 0.05 of P(V) (paired DP H - R, lower bound at
  least -0.05). Mechanism (read, section 2.2-2.3): a held negative identity keeps the flee target after the whiff ends; R flees only while the negative channel is the
  argmax of the gated upstream output and above 0.05, about a dozen steps after its last whiff (inferred, 2.3). What it predicts, by direction only (inferred; no recorded
  number fixes a size or even a sign, 2.4): H leaves the punisher's plume for longer stretches and re-enters it less often; R ends each flee after at most about 7 units
  and resumes the cast near the plumes, so R may re-meet the negative plume more often (higher R dwell and more negative whiffs) but is less exposed to the stranding that
  ended Agent10's flees about 29 units off the plumes (fewer lost rows, fewer wall contacts in R). P(V) can move either way.
- **B3 (three-channel distractor form, T1D, supplied +1/-1/0, D on at p_D 0.03, learning off).** The same hypothesis and criteria, stated separately; no number is carried
  from A5 to B3 or back.
- **A6 (two-channel, T1, 0/0).** No hypothesis registered: reported only (section 8).

## 2. Basis: measured, read and inferred

### 2.1 Exposure in stage one (measured, `experiments/hold/hold_stage1_report.md` counts table; `experiments/hold/hold_stage1_replay.json` strata.*.command_exposure)

| Stratum | h != q | flee differs | command differs | rows exposed | per exposed row (quartiles) | first command step (quartiles) | rows with >= 100 command steps |
|---|---|---|---|---|---|---|---|
| A5 T1 +1/-1 | 86 379 | 43 504 | 43 352 (0.181 of 240 000) | 331/400 | 17/33/257 | 4/10/33 | 130 |
| B3 T1D +1/-1/0 | 110 096 | 10 473 | 10 319 (0.043) | 355/400 | 15/23/36 | 3/12/34 | 9 |
| A6 T1 0/0 | 61 002 | 0 | 64 (0.00027) | 33/400 | 1/2/3, max 4 | 29/34/37 | 0 |

Also measured (same JSON fields): first command difference at step 0 in 15 A5 rows and 23 B3 rows; every A6 command difference is release-adjacent (64 of 64); A5 commands
differ on all 146 wall row-steps, B3 on 3 of 9 351.

### 2.2 What H does while a negative identity is held (read, `src/fly.py` at 1ce9b22)

The flee target replaces surge and cast whenever the read value is negative (`tgt = where(val < 0, flee_side, tgt)`, fly.py:345; `val` from the read identity, :312). The
gate cannot act on a negative hold (`v >= 0 & v < vh`, :300, is false for every channel when `vh = -1`). The hold ends by the evidence release when another channel's
gated output exceeds the held one by 0.2 (:303, :218-222). The timeout fires at silence above 40 (:302) and delivers one reset step (:305-307), but the N2 wrapper
sustains it only at a non-negative previous hold (`negS`, :284; `sustain = base & ~negS`, :287), so the frozen timeout defect is in force: a silent negative hold is not
ended by silence (master_plan.md L9, record:silence- timeout-chain-result). A wall contact flips the flee side and the cast sign (:264-267; caller `a.bump(w.bumped)`,
ph33.py:251). So H flees until an evidence release, turning at walls, possibly to the run's end.

### 2.3 What R does (read, then inferred)

R flees iff `q` is the negative channel. After the negative channel's last whiff its upstream state halves every step (`P += (1/tau)(-P + u)`, tau 2.0, fly.py:38, :98);
`y = 1.8 P / (0.05^1.5 + P + 0.8 others)` (:101). With the other channel's P at 0, `y > 0.05` needs `P > 0.00032`: from one whiff (P 0.5) about 11 steps, from saturation
(P near 1) about 12 (inferred; fewer when the other channel's P is non-zero, and none while the valued channel's output, gained by 1 + 2 x 1 = 3 at :297, is larger). At
SPEED 0.6 per step (ph9.py:31) a flee of 12 steps covers at most about 7 units, against about 29 units crosswind for Agent10's flees of 48 to 54 steps (measured,
`experiments/avoidance_check/r3_diagnosis.md`:12-14); the sources sit 10 apart crosswind (ph16.py:24 SEP). R also flees **earlier** than H: before the circuit has formed
a hold (s above 1.0, fly.py:258, from s = 0 at one tenth per step, :129), R reads a whiffing negative channel while H reads nothing. At step 0 no hold can exist (s at
most 0.5 after one step, inferred), so the 15 A5 and 23 B3 rows with a first command difference at step 0 (2.1) are R-flees-H-does-not. In B3, H's negatively-held
row-steps are 6 084 at that condition and those seeds (measured, `experiments/h28/ph33_eval.txt`:47, the same rows as B3 by `experiments/module/module_report.md`:45), so
of the 10 473 flee-differing row-steps at least 4 389 are R-only (inferred: H-only cannot exceed 6 084). The comparison therefore branches in **both** directions; stage
one's reading point 3 names only one (section 13).

### 2.4 Recorded analogs (measured; each on its own seeds and arms; none carried as a prediction)

| Source | Arms, condition | P(V) | lost rows | contacts/row | dwell at negative source | other |
|---|---|---|---|---|---|---|
| ph24b_check.txt:26-30 (avoidance check R3) | Agent10 (H25 release ends negative holds) vs Agent8 (no release), +1/-1 | 0.765 vs 0.925 | 127 vs 33 | 0.000 vs 0.307 | 2.487 vs 2.855; paired -0.368 [-0.550, -0.202] | DP -0.160 [-0.195, -0.125]; lost DP +0.235 |
| h26 ph28_eval.txt:121 | Agent14 (release on at negatives), T4 +1/-1 | 0.772 | 123 | 0.000 | not printed | |
| h29 ph35_eval.txt:42 | Agent17, T4 +1/-1 = **A5's H arm** (module_report.md:39) | 0.917 | 42 | 0.365 | not printed | ties 14 |
| h28 ph33_eval.txt:46 | Agent14N2, T4 +1/-1 | 0.932 | 39 | 0.393 | 3.135 | negatively held 44 895 row-steps, 0 flee violations |
| h28 ph33_eval.txt:47 | Agent16 D on, T4 +1/-1/0 = **B3's H arm** | 0.740 | 125 | 23.378 | 3.172 | negatively held 6 084, 0 violations, ties 45 |
| h28 ph33_eval.txt:96; master_plan.md:740-741, :802 | M6, lost-row DP hold-not-read - reference (W1D) | | 222 vs 222 | | | +0.0000 in H28; 0.0000 in H27 |

Interpretation (labelled): the release-on/off pairs show that ending a negative hold about 50 steps after it formed strands the agent outside both plumes (0 of 131
drive-ended holds met a whiff again, r3_diagnosis.md:15-17). R ends the flee, not the hold, and about four times sooner, so that record does not predict R. The sign of
the primary measure is not anchored either: the arm that kept fleeing (Agent8) dwelt **more** at the negative source, because the wall reflex carried it back across both
plumes (r3_diagnosis.md:22-29, :48). The paired sd of dwell at the negative source, about 1.78 per row (inferred from the half-width 0.174 of the -0.368 interval: se
0.0888, times 20), is the only recorded scale, from another arm pair.

## 3. The arms

### 3.1 H: `fly.Fly`, unchanged

Both forms, built through the existing harnesses as `src/module_identity.py` does (ph35's hook for the two-channel form, `ph33.build` for the three-channel form). Run as
`src/hold_stage1_instrument.PassiveFly` (passivity verified in all nine strata, stage-one gates table) so that `hr` and the local R projection on H's own state are
recorded beside H.

### 3.2 R: a subclass in a new file, `fly.py` not edited

Proposed `src/hold_stage2_arm.py`, class `ReadOutFly(fly.Fly)` with one constructor argument `read` in {'actual', 'instant'}. It overrides `_act` only, repeating
fly.py:293-350 term for term, and computes `hr` exactly as ph33.py:134 (`where(y.max(1) > 0.05, y.argmax(1), -1)`) from the gated `y` after :300 and after `sel.step`
(:307), with `hh = h if read == 'actual' else hr`. `hh` replaces `h` in the read-out expressions only: `val` (:312), `hit` (:313), `vh` (:314), the presence override
(:325-326), `keep` (:333 or :336) and through them `nav`, `since`, `silence`, `tgt` and the clipped turn (:334-346). Kept actual: the gain, gate and evidence release on
`hp` (:297-303), the reset and circuit (:304-308), the heading (:310), the counters and burst record (:316-324), the turn noise (:347). `act` (:277-291) is inherited
unchanged, so N2 reads the actual previous and current hold and the actual held channel's whiff. `_act` returns the actual `h`. No random draw is added. This is the same
boundary as ph33.Act16 with `hold_read=False` (ph33.py:134-135, :150, :161) and stage one's projection (hold_stage1_instrument.py:50-82).

**Amendment one, stated as part of the R arm:** R's `silence` counts R's read-identity whiffs (:341); on the next step it sets `due_timeout` (:302) and so the reset
(:305-307), and N2 may then overwrite it (:290). R's circuit therefore follows its own reset times one step later even while its commands equal H's; stage one counted 1
905 to 7 177 such latent differences per stratum. As in H27/H28's hold-not-read arm (ph32.py:172-174, ph33.py:168), this coupling belongs to R by definition: the trial
compares an agent whose navigation reads the hold with one whose navigation reads the instantaneous output, each with its own downstream circuit history. It is not "the
same circuit, read differently".

### 3.3 Recorded fields

As `ph32.record` (EVERY + HR, ph32.py:262-271): `H` = the actual circuit hold returned by `act` (as the hold-not-read arm records it), `HR` = R's read identity, `VAL` =
the value of the read identity (ph32.py:269-270); plus `VALH` (value of the actual hold) and `FLEE` (flee side per step, the ph24b.py:28-32 hook pattern).

### 3.4 Reference arms for floors and ceilings

- **Free** (no avoidance): `fly.Fly` on the same seeds with the negative channel's supplied value set to 0 (A5: +1/0, which is A1's condition; B3: +1/0/0, B1's). Its
  dwell at the formerly negative source is the no-flee floor of C1's span; its P(V) is C2's ceiling.
- **Chance floor for P(V):** A6's H arm (0/0) on the same seeds, side balance by construction near 0.5.

## 4. Identities, before any measure is read

All at zero tolerance, run before the bench and printed first. Seeds: `ph35.SEEDS['eval']` and `ph33.SEEDS['eval']` by alias, as stage one, for these diagnosis-type
checks only (spent seeds; no criterion reads them).

- **(I1) H arm.** fly.Fly in A5, A6, B3 is already IDENTICAL to the ph-chain agents on L1/L2/L3 (module_report.md:39, :40, :45); re-checked through (I7).
- **(I2) Switch-off, the bitwise known answer.** `ReadOutFly(read='actual')` == fly.Fly on L1, L2 and L3 in all eleven identity rows (A1-A6, B1-B3; A7/A7r excluded,
  learning). This tests the repeated `_act` itself.
- **(I3) Three channels.** `ReadOutFly(read='instant', nch 3)` injected through `ph33.build` == ph33's 'hold-not-read D on' (ph33.py:198-209) on every field (EVERY + HR):
  (a) at T1D and W1D +1/0/0, whose outputs are recorded (ph33_eval.txt:20, :33); (b) at T1 +1/-1/0 against a fresh run of ph33's unchanged code. No hold-not-read output
  exists at +1/-1/0: ph33's evaluation ran that condition with Agent14N2 and Agent16 D on only (ph33.py:688, ph33_eval.txt:45-47); (b) is a code identity, not a recorded
  one.
- **(I4) Two channels, known answer at +1/0.** `ReadOutFly(read='instant', nch 2)` == fly.Fly at T1 and W1 +1/0 (A1, A2) on the trajectory and score fields (POS, HEAD,
  NAV, SINCE, TURN, EST, TGT, W, AT2, C; L3 scores) on every row and step. **Not** required equal on S, SG, H, SIL, TO, EV, SUS, Z: by amendment one these may differ, and
  their differing row-steps are counted and printed. Reason for the trajectory equality (inferred): at +1/0 the command depends on the read identity only through the
  presence override (stage-one reading point 1, fly.py:325-337), the presence set never differed in 960 000 row-steps (measured), and R overrides only a channel whiffed
  within about a dozen steps (2.3), whose counter is far below the window 200. Every-field equality is not a known answer here; the brief's wording should be corrected.
- **(I5) Link to stage one.** Per row, on every step up to and including the R arm's first differing field against the PassiveFly H run, R's `HR` equals the projection's
  `hr`, and on the first command-differing step R's clipped turn equals `hold_projection['R']['clipped_turn']` (hold_stage1_instrument.py:46, :78).
- **(I6) Cross-implementation, two channels (recommended).** `ph33.Agent16(nch=2, N_hi 200)` with `hold_read=True` == fly.Fly, and with `hold_read=False` ==
  `ReadOutFly(read='instant')`, at A5 on every field. Valid at +1/-1 only: the tie rule is inert there because the top set holds at most the valued channel (read,
  fly.py:26-27 U10; ph33.py:154-158); it acts at 0/0, so not at A6.
- **(I7) Harness.** The new runner reproduces the H numbers of A5, A6, B3 (module identity digests; ph35_eval.txt:42, ph33_eval.txt:47), and the world, D, agent and
  third-unit generator states are equal between the H and R arms after every step (section 5).

**Failure:** any identity failing stops the design before any measure: no bench, the first mismatch reported, a reviewed correction before anything is re-run (stage-one
gate table, last-but-one row). A failure of (I4) may be a real branch rather than a bug; (I2) and (I5) decide which before anything else.

## 5. The estimand, and the random draws

**Estimand.** Two freely evolving embodied agents per row, H and R, sharing the world equations, the source geometry and start (World7, ph16.py:43-55), the initial agent
state, and the exogenous variates by role. Once their commands differ, their positions, plume exposure, whiffs, wall contacts, rotations and later internal states diverge
endogenously; common variates do not make observations equal (a whiff is `(in region) & (u < p(pos))`, ph11.py:80-83: the same `u` at a different position). The estimand
is the per-row paired difference, over all 400 rows, of end-of-run and trajectory measures. No "same input" claim is made after a row's first divergence; R's observations
are never overwritten with H's.

**Draw audit (read).**

| Role | Generator | Line | Shape per step | State- or action-dependent? |
|---|---|---|---|---|
| whiff uniforms, per channel | world | ph11.py:83 | (R) x 2 | no (drawn for every row; background off, p_d 0, ph14.py World5) |
| wind | world | ph11.py:86 | (R) | no; p_wind 1.0, always on |
| D stream (B3) | rngD | ph33.py:233, :242 | (R) | no (drawn whatever p_D) |
| circuit noise | agent [+ rng3] | fly.py:123-128 | (R, 2) [+ (R, 1)] | no |
| ring, rotation step | agent | fly.py:209 via :271 | (R, 16) | no |
| ring, cue step | agent | fly.py:272-273 | (R, 16) | only on `wind_on.any()`, which is true every step at p_wind 1.0 and equal in both arms (same draws) |
| turn noise | agent | fly.py:347 | (R) | no |
| flee side | agent | fly.py:241 | (R), construction only | no |
| cast sign | own generator | ph16.py:35-40, ph33.py:235 | construction only | no |
| movement, walls | none | ph12b.py:46-62 | | no draw |

Learning is off, so `mb.step` is never called; the odour codes use their own generators (fly.py:146-152). Every shape is fixed and none is conditioned on state or action,
so both arms consume identical streams and row i receives the same variate at each (step, role): common random numbers by construction. **Recommended: no draw-tape;**
(I7)'s per-step generator-state equality is the check, and a tape is designed only if it fails.

## 6. Measures (per arm, per row, denominators all 400 rows)

- **D_neg**, dwell at the negative source: steps within 3.0 of it (`AT2[:, r, 1 - good]`, ph33.py:254, :738; HIT_R ph9.py:31; ph24b.py:109). A5: channel 1 - good; B3: the
  same plume channel (D has no source).
- **V**, dwell majority (ph18.majority through `cls3`, ph32.py:379), ties counted.
- **lost**, no whiff of either plume on steps 400-599 (`lost_t1`, ph32.py:378; D excluded).
- **contacts** per row (ph33.py:254).
- **Flee checks:** H, actual negative held and `TGT != FLEE` (ph24b.py:35-36), must be 0; R, `VAL < 0` and `TGT != FLEE` (ph33.py:250), must be 0. Both are implementation
  checks. Reported: R's row-steps with the actual hold negative and no flee (the intervention's own exposure).
- **L_leave** (reported): from the arm's first negative whiff in the row, steps until the first step from which the agent stays outside the negative whiff region
  (ph11.py:78-82 geometry for that source, ph32.py:274-280 `cone_of`) for 30 consecutive steps; censored at 600; 0 for a row with no negative whiff. **Negative whiffs per
  row** (reported).
- **Hold diagnostics** (reported, per arm on its own state; step-by-step pairing across arms is not defined after divergence, as ph33's N1, ph33.py:52-55): fraction of
  row-steps with a negative actual hold; row-steps with the negative identity read by the hold rule but not by R, and the reverse (R arm: actual vs `HR`; H arm: actual vs
  the passive `hr`); negative holds ended by evidence and by a timeout-reset step; first divergence step per row (any field; trajectory).
- **Statistics:** Wilson 95 percent for proportions; paired percentile bootstrap over rows, 5000 resamples, 95 percent, through `ph16.interval` (ph16.py:169-171,
  ph15.boot) with a new bootstrap seed set by `ph30.set_stats` as ph33.py:104 and ph35.py:88 do. One statistic per criterion, never replaced; PASS/FAIL/INCONCLUSIVE by
  the interval rule.

## 7. Criteria, bars and pass probabilities (A5 and B3 separately, same structure)

- **M0 identities** (I1)-(I7): PASS required; otherwise stop (section 4).
- **M1 validity** (else UNREADABLE): ties at most 0.20 in H and in R (A5's H had 14/400, B3's 45/400, measured above); C1's span S = mean D_neg(Free) - mean D_neg(H) at
  least 1.0 step per row on the bench (inferred scale: recorded negative dwells are 2.5 to 3.2; if the punisher is barely visited without avoidance, no avoidance benefit
  can be read). P(V) printed between its floor (A6 H) and ceiling (Free).
- **M2 = C1, the benefit:** paired D_neg R - H, **lower bound > 0** PASS, upper bound <= 0 FAIL, else INCONCLUSIVE (the strict bar of H29's M8(b)). No anchor for m (2.4);
  s anchored only at about 1.78 (inferred, another arm pair). Pass probability Phi(m / (s / 20) - 1.96):

| m | s 1.8 | s 3.0 | s 4.0 |
|---|---|---|---|
| +0.1 | 0.20 | 0.10 | 0.07 |
| +0.2 | 0.60 | 0.27 | 0.17 |
| +0.3 | 0.92 | 0.52 | 0.32 |
| +0.4 | 0.99 | 0.76 | 0.52 |
| +0.6 | 1.00 | 0.98 | 0.85 |

  (checked: m 0.3, s 1.8: se 0.09, 3.33 - 1.96 = 1.37, Phi 0.92.)
- **M3 = C2, the cost bound:** paired DP P(V) H - R, **lower bound >= -0.05** (the project's M2(b) margin). Pass probability Phi((DP + 0.05) / se - 1.96), sd = sqrt(b -
  DP^2), se = sd / 20 (ph28.pp_dp, ph28.py:196-200): DP 0 with b 0.05 / 0.10 / 0.16: 0.99 / 0.89 / 0.71; DP -0.02, b 0.10: 0.48; DP -0.03, b 0.10: 0.25; DP +0.03, b 0.10:
  1.00.
- **M4 = C3, lost rows (H27/H28's M6, sign hold-not-read minus reference):** paired lost-row DP R - H, **REPORTED** with H27's line 'lower bound >= +0.05'
  (h27_design_v1.md:161) printed. Its pass probability would be 0.03 at DP +0.05, b 0.10, and 0.76 at DP +0.10, b 0.15 (same arithmetic); registering it would add a
  second benefit test (section 12 point 6).
- **Reported:** contacts, L_leave, negative whiffs, hold diagnostics, flee checks (a nonzero check is an implementation error).
- **Joint** (parts as independent, an order of magnitude): at m 0.3, s 1.8 and DP 0, b 0.10: 0.92 x 0.89, about 0.82; at m 0.2, s 3.0: about 0.24. With no anchor for m,
  these are scenarios, not predictions.
- **Verdict per condition:** 'the hold's benefit SHOWN in A5 (B3)' iff M0, M1, M2 and M3 PASS. M2 FAIL or INCONCLUSIVE: NOT SHOWN. M3 FAIL: a cost of reading the hold on
  choice, stated as such. Scope: supplied +1/-1 (+1/-1/0 with D), N2 release off at negative holds (the frozen timeout defect in force), G 2, C0, learning off, World7 T1,
  400 x 600.
- **Bench-first rule.** The bench (bench seeds, 400 x 600, arms H, R, Free; the A6 pair) measures m, s, DP, b, S. Stop rules: (hI) any identity fails; (hS) S below 1.0;
  (h1) M2's pass probability at the bench m and s below 0.5; (h2) M3's at the bench DP and b below 0.5. A stop ends the condition before any development seed: 'stopped at
  the bench', nothing tuned. Where the owner prefers a materiality bar for M2 to 0: bar_D = +0.10 x S rounded to 0.1, fixed by a bar decision from the bench before the
  development run (the H26 M5(b) pattern, decision:h26-t2-dwell-bar).

## 8. A6 (0/0): reported only (recommended)

Exposure is 64 row-steps of 240 000 (0.027 percent) on 33 rows, at most 4 per row, all release-adjacent, first at steps 29 to 40 (measured, 2.1). With no valued source
P(V) is chance by construction, and no avoidance exists to read. A paired binary difference over 400 rows could reach at most about 33/400 = 0.08 if divergence stayed in
the exposed rows (inferred; not bounded in a free run, where amendment one can move later exposure). Proposed: run the H/R pair at A6 on the bench and evaluation seeds,
print exposure, first divergence, side balance, first source reached and dwell at each source, no bar, no verdict. A world that exposes the tied-top route more often is a
world change and belongs to the stage-one gate 'commission a world-change design', not here.

## 9. Worlds, sizes, seeds

World7 T1 (two sources 10 apart crosswind, start on the midline 20 downwind, ph16.py:24, :43-55), 400 rows x 600 steps (ph16.py:24); values exactly (1.0, -1.0) for A5,
(1.0, -1.0, 0.0) with D on at p_D 0.03 for B3 (ph32's P_D; third-channel streams by the named D_OFF and A3_OFF rules, ph32.py:109), (0.0, 0.0) for A6; G 2, C0, gate on,
N2, learning off, as fly.py composes them. **W1/W1D at these values are not registered:** at +1/-1 W1 masks the valued source and leaves only the negative plume, a pure
avoidance world worth considering, but no fly.py identity row exists there (module rows A2, B2 are +1/0 and +1/0/0), so it would first need its own identity row (section
12 point 5). **Seeds:** bench, development, evaluation and bootstrap seeds are all new, to be chosen at the FINAL after a repository and graph scan; none is written here
(P5: no digits of a registered ph33 or ph35 seed in notes/). Identity rows reuse `ph35.SEEDS['eval']` and `ph33.SEEDS['eval']` by alias, for diagnosis-type checks only.

## 10. Order of work (each gate the owner's)

Owner confirms section 12 -> design v2 FINAL with seeds chosen after the scan -> code (the subclass file and a runner; no existing file edited) -> identities (I1)-(I7) ->
bench with the stop rules, the A6 pair printed -> any bar fixed by its registered rule, as a decision -> development run (operation errors only) -> one evaluation ->
report. Nothing changes after the table; a change is a new run with its own record.

## 11. What this proposal does not claim or test

- Nothing about the adopted scope (+1/0, +1/0/0): stage one found no command branch there in the fixed sample, and (I4) is a known-answer check, not a measurement of
  benefit.
- Nothing adopted, extended or re-scoped if a benefit is shown. A benefit in A5/B3 is a statement about supplied negative values with the N2 release off at negative holds
  and the frozen timeout defect in force, learning off, World7 T1, these rows; not about learned values, other worlds, walls removed, or the total causal contribution of
  the circuit (R keeps the circuit, gate and release; design rev 2, "Exact contrast").
- No fixed-input replay, no threshold other than 0.05, no learning stratum, no world change.

**Rejected on record:** (a) fixed-input replay as the main trial: the tape does not follow R's position, so it is not two embodied agents (design rev 2, "What can be held
equal"); (b) a fitted or changed 0.05 read-out threshold: H27/H28's R4 is the defined R; (c) running on +1/0: no branch in A1-A4, none reached in B1-B2; (d) an R arm
whose silence or circuit is forced to H's: overwrites R's own state, not a natural trajectory; (e) substituting `q` in the gate, evidence release or N2: removes the
circuit's role, a different intervention (H15's no-select-and-hold); (f) a draw-tape now (section 5); (g) adopting anything from this design.

## 12. What the owner confirms (each with a RECOMMENDED option)

1. **Whether to run stage two at all.** RECOMMENDED: yes, A5 and B3 as designed, bench first; reason: commands differ in 0.181 (A5) and 0.043 (B3) of row-steps on 83 and
   89 percent of rows, the only conditions where (d) is readable on recorded worlds. Alternative: defer (d).
2. **The R arm.** RECOMMENDED: `ReadOutFly` in a new file (3.2), amendment one's coupling kept as part of R. Alternative: ph33's Agent16 with `hold_read=False` at both
   widths (no fly.py lineage at two channels; window 300 unless N_hi passed).
3. **Identities.** RECOMMENDED: (I1)-(I7), with (I4) on trajectory and score fields only and (I3)(b) as a code identity. Alternative: drop (I6).
4. **Primary criterion.** RECOMMENDED: M2 (dwell at the negative source, R - H, lower bound > 0) with M3 as a cost bound. Alternatives: P(V) DP H - R as primary; lost
   rows (M4) as primary, H27/H28's M6 sign.
5. **Worlds.** RECOMMENDED: T1 only, as recorded. Alternative: add W1 at +1/-1 (negative plume only) after a new module identity row for fly.py there.
6. **Bars.** RECOMMENDED: M2 strict at 0; M3 at -0.05; M4 reported; S at least 1.0. Alternatives: M2 at bar_D = +0.10 x S by a bench-fixed decision; M4 registered at
   +0.05 (then two benefit tests per condition).
7. **Stop rules.** RECOMMENDED: (hI), (hS), (h1), (h2) at pass probability 0.5. Alternative: (h2) reported without a stop.
8. **A6.** RECOMMENDED: reported only (section 8). Alternatives: excluded with that reason; a world-change design.
9. **Draws.** RECOMMENDED: no draw-tape; per-step generator-state equality in (I7). Alternative: a reviewed tape design.
10. **Seeds.** RECOMMENDED: all new at the FINAL after the scan; identity rows on the eval aliases. Alternative: none.

## 13. Self-review (2026-10-07)

- **Points where the brief or stage one may be wrong.** (i) Stage one's reading point 3 says A5 and B3 branch with H fleeing while R surges or casts; R also flees where H
  does not (2.3: step-0 rows; at least 4 389 B3 row-steps), so the branch is two-sided. (ii) A two-channel 'R == H bitwise on every field at +1/0' known answer
  contradicts amendment one; (I4) uses trajectory and score fields, and the bitwise known answer is the switch-off (I2). (iii) No recorded hold-not-read arm exists at
  +1/-1/0; (I3)(b) is against a fresh ph33 run.
- **Arithmetic to check.** The dozen-step decay (2.3) assumes the other channel's P at 0 and P halving exactly (fly.py:98 at tau 2); the 7-unit flee assumes straight
  motion at 0.6 per step. The 4 389 bound assumes ph33's `neg` counts H's actual negative-held row-steps (ph33.py:250, VAL from `h` when `hold_read` is True,
  ph32.py:269). The sd 1.78 comes from the avoidance check's interval of a different pair. Pass probabilities: Phi with se = s / 20 or sqrt(b - DP^2) / 20. Recompute from
  the cited lines.
- **Readings to check.** The draw audit (section 5) rests on World2.sense/wind_on, World3.move and fly.py's draws; (I7) checks it. (I4)'s trajectory equality is inferred;
  (I2) and (I5) separate a bug from a branch if it fails.
- **Not carried:** no A5 number is used for B3; the ph35/ph33 T4 lines are the H arms on spent seeds, used for scale and identity only; the avoidance-check rows are other
  agents.
- **Seeds:** no seed digit is written; the file bytes are to be scanned against the ph33/ph35 seed sets before commit.

