# H10 design v2 FINAL: abstention without losing evidence-driven revision

2026-09-27. **Status: FINAL, confirmed by the owner on 2026-09-27 (UTC), section 12 (decision:h10-open).** No bar, seed, arm, prediction or rule changed from the candidate put to the owner. At registration no H10 arm had been run and no seed in section 9 had been used.

This version is written from Codex's v1 DRAFT (commit a7e615a; Vinc doc de54a82b469cc43b4; `experiments/h10/h10_design_v1.md`, kept unchanged as history). The owner asked this session to read the handoff `notes/handoffs/2026-09-27-fable-h10.md` and continue from it ('codex/h12-review-plan의 a7e615a를 받고, notes/handoffs/2026-09-27-fable-h10.md부터 읽어 이어서 진행해 주세요.'). The only computation behind the changes is design arithmetic: [`src/h10_design_check.py`](../../src/h10_design_check.py), output [`h10_design_check.txt`](h10_design_check.txt). That script does not run the H10 gate, does not run any arm on a noise stream, and uses no seed from section 9.

## 1. Question and scope

Can a confidence stage withhold commitment on insufficient evidence while a graded selector keeps, and revises, its identity without an external reset? This is a selection-module experiment. No claim about fly anatomy, autonomous navigation, learning or adoption follows from it (concept:h10-abstention-and-revision-are-different-stages; `src/ph7.py`; `experiments/h09/ph7_h9.txt`).

The H9 graded selector (`ph7.ChanDiv`, J 1.2, c 0.5, tau 10) kept, revised and resisted a distractor in 200/200 historical easy-cue rows. It made 44/200 wrong choices on the hard cue at x0 1 and 44–61 at every input scale. The adopted bistable circuit, never reset, made 121/4/75 correct/wrong/abstain at x0 1 and 3–5 wrong at every scale. It could not revise (D3 0/200). H10 therefore targets wrong commitments under weak evidence. It does not claim that H9 commits on silence: H9 passed the zero-input idle test. The historical counts motivate the design. They are not new-seed baselines.

## 2. What the review changed, and why

**2.1 The confidence threshold was on the wrong scale.** v1 defines q = (largest − second)/sum over the five-channel evidence trace. The trace converges to the upstream output y for a constant input. Under the hard cue every channel carries the background input x0, so the sum is about five channels' worth. The noise-free steady state of the adopted upstream stage (`ph2.Upstream` with `ph7.UP`, unchanged) gives:

| Input | q = (1st − 2nd)/sum |
|---|---:|
| Hard cue, x0 0.25 / 0.5 / 1 / 2 / 4 | 0.0085 / 0.0083 / 0.0082 / 0.0082 / 0.0082 |
| Easy cue (d 0.4), x0 1 | 0.0573 |
| B alone at amplitude 2 (revision, distractor) | 1.0000 |
| Ambiguous (d 0), x0 1 | 0.0000 |

v1's grid was θ ∈ {0.02, 0.05, 0.10}. θ = 0.02 is 2.4 times the settled hard-cue q, so the gate would stay closed on most hard-cue rows and fail the anti-trivial abstention check. θ = 0.10 is above the easy-cue q, so the gate would block easy acquisition. The v1 family would therefore fail by the placement of its grid, not by anything the hypothesis says. **Changed [owner, 12.1]:** θ ∈ {0.004, 0.008, 0.016}, that is 0.5, 1 and 2 times the settled hard-cue q at x0 1. Each value is at most 0.28 times the easy-cue q. The q formula itself is kept. These are noise-free steady states: noise enters y nonlinearly, and calibration measures the actual distribution.

**2.2 Silence neither retains nor erodes the gate.** Once the upstream stage's own tail (tau 2) has passed, a blank input decays every component of e by the same factor. q is invariant under that decay, so a read after silence sees the gate as it stood at the end of the preceding input. Retention across a blank is therefore the graded circuit's property alone. Under the idle condition the upstream output is exactly 0, so e = 0 and the gate is closed by construction. The idle criterion thus tests only the graded circuit, which passed 200/200 historically. For the candidate it is an implementation identity, not evidence.

**2.3 The evidence trace and the graded output can disagree, and the gate does not resolve it.** The gate permits or withholds the graded identity. It never substitutes e's leader. After the distractor, for example, e's leader is B while the graded circuit correctly still holds A; the gate passes A. This division is the hypothesis: a thresholded stage decides *whether*, a graded stage decides *what*. The consequence is the main risk of the design. A wrong graded commitment made on a row whose evidence margin is high passes the gate.

- If H9's hard-cue errors (0.22 at x0 1) were independent of e's margin, the exposed wrong rate would be about 0.22 times the coverage, and no setting could pass.
- If the errors fall in low-margin rows, the gate can approach the ideal-observer frontier (2.6).

Arithmetic cannot say which holds; calibration measures it. Disagreement between e's leader and the graded identity is recorded row by row in every arm. An agreement requirement (output only when e's leader equals the graded identity) was considered and not added [owner, 12.5]. It would make the evidence trace a second selector, which is not the division the hypothesis states.

**2.4 Read-out versus state.** The gate changes only the exposed output. The graded state, its internal noise and e are identical whether the gate is open or closed, so the forced-open arm must equal the ungated arm bitwise on state and output. Claims are therefore made separately on two levels:

- the raw graded state: revision with no reset, possibly through a moment with no channel above threshold;
- the exposed output: revision that may pass through an abstention while q crosses zero, as e's leader changes from A to B.

**2.5 The simple graded-state mask cannot abstain once the circuit has committed.** Driven noise-free by the upstream output, the H9 circuit commits to the hard-cue target by step 100. The same q computed on its state is then 0.12 at step 100 and 0.72 at step 300 (easy cue: 0.55–0.81). v1's mask grid, θ ≤ 0.10, therefore passes every committed state at the read points. The mask is predicted to equal the ungated arm there. It stays as the registered control that asks whether a read-out threshold on the state alone suffices, with this prediction stated in advance.

**2.6 How the error bar behaves at n = 400 [owner, 12.3].** An all-row wrong-rate upper bound ≤ 0.025 (Wilson) allows at most 3 wrong of 400; 4 gives 0.0254. Two consequences follow:

- The adopted bistable's historical wrong rate (8 per 400) would pass with probability 0.04.
- Across all five scales (independent rows), the probability of passing is 0.91 at a true wrong rate of 0.25%, 0.46 at 0.5% and 0.015 at 1%.

An upper bound ≤ 0.04 allows 8 wrong of 400; its five-scale pass probabilities are 1.00, 0.999 and 0.90 at those rates, and 0.07 at 2%.

An ideal observer summing the raw hard cue over all 300 steps bounds any mechanism reading the same input. Its best coverage is 0.77 at an all-row wrong rate of 0.0075, 0.70 at 0.004 and 0.62 at 0.002. The candidate's trace sees less of the cue than that observer: its effective window is 79, 152 and 235 of the 300 steps at τ_e 40, 80 and 160.

**2.7 The anti-trivial abstention bar is binding too.** The bistable's historical correct rate is 0.605 at x0 1. The bar asks for a paired lower bound ≥ −0.05, and between-arm discordance is likely 0.3–0.5 of rows. Under those conditions the candidate's correct rate must reach roughly the bistable's point estimate, 0.60–0.62. The ideal observer reaches 0.69 at a wrong rate of 0.004. The bar is kept as in v1.

**2.8 Seeds were left blank in v1.** They are filled in section 9, scanned against the repository and the graph.

**2.9 Protocol ambiguities resolved:** update order, read points, cue noise on the easy cue, balanced targets, the permutation check's tolerance, and the shared-noise construction (sections 3–6).

**2.10 The queued statement named different criteria [owner, 12.9].** When H10 was queued, concept:h10-abstention-and-revision-are-different-stages said it would be tested by "the same six criteria of record:phase7-1-success-criteria, unchanged". v1 and v2 gate instead on all-row interval versions of those criteria, plus an anti-trivial abstention check and an added-value check. The reason: Phase 7.1 read D2–D4 as fractions of committed runs and D1/D5 as point wrong counts. A gate that abstains can therefore pass them by abstaining, since uncommitted rows leave the D2–D4 denominators and cannot be wrong. The six historical criteria are still computed exactly as Phase 7.1 defined them (200-row cells from ph7's own generators in the reproduction, and the same conditional or point readings on every new stage) and reported beside the registered table. They are not a gate.

## 3. Stage A candidate: one explicit family

`ph7.UP` and `ph7.ChanDiv` are used unchanged: five channels, J 1.2, c 0.5, tau 10, internal noise 0.01, and every other default. No reset drive, target label, phase flag, elapsed-trial clock or future sample enters the candidate. Each step t does the following, in this order:

    y_t      = upstream.step(x_t)                                  # ph2.Upstream, ph7.UP
    s_t      = graded.step(y_t)                                    # ph7.ChanDiv, one internal-noise draw
    e_t      = (1 - 1/tau_e) * e_{t-1} + y_t / tau_e               # e_0 = 0; updated in silence too
    q_t      = (largest(e_t) - second(e_t)) / (sum(e_t) + 1e-12)
    gate_t   = (sum(e_t) > 1e-6) and (q_t >= theta)
    raw_t    = ph7.committed(s_t)                                  # -1 if none or more than one above 1.0
    output_t = raw_t if gate_t else -1

The gate consumes no randomness and never sets a winner, clears the state or supplies a reset. **Family:** τ_e ∈ {40, 80, 160} [owner, 12.2] × θ ∈ {0.004, 0.008, 0.016} [owner, 12.1], exactly nine settings. No expansion, no refit and no new graded-circuit sweep after results.

## 4. Arms, on shared input and noise tapes

1. **Adopted bistable** (`ph7.Bistable`, reset never driven): the historical reference.
2. **H9 graded, ungated** (`ph7.Graded`).
3. **H10 candidate**, the nine settings of section 3.
4. **H10, gate forced open**: must equal arm 2 bitwise on state and output (identity).
5. **H10, gate forced closed**: output always −1. A read-out-path control; it must fail acquisition.
6. **Simple graded-state mask**: output = raw if q on the graded state ≥ θ_m, with θ_m ∈ {0.02, 0.05, 0.10} as v1, selected on calibration only. Predicted in 2.5 to equal arm 2 at the read points. If this control passes as H10 does, the evidence trace is not established as necessary.

Every arm reads the same input tape. Arms 1–6 draw their internal noise from the same child stream (both circuits draw one `standard_normal((rows, 5))` per step), so the draws are identical. The upstream stage is deterministic.

## 5. Conditions and read points

All new conditions use 400 assigned rows. Targets are balanced, exactly 80 per identity, permuted by the condition's target stream. The second identity is B = (A + 1) mod 5, fixed before execution. The cue input follows `ph7.cue_phase` exactly:

    x = x0 on every channel;  x[A] += d * x0;  x += noise_sd * x0 * N(0, 1)

Negative samples are kept as drawn; the upstream stage clips them. Pulses and blanks carry no input noise, as in `ph7.pulse` and `ph7.blank`.

| Condition | Protocol (steps) | Read points |
|---|---|---|
| Hard cue, x0 ∈ {0.25, 0.5, 1, 2, 4} (five conditions) | cue d 0.05, noise_sd 0.3, 300; blank 300 | final at 600 (as `ph7.d1_d5`); cue end 300 reported |
| Easy acquisition and hold | cue d 0.4, noise_sd 0.3, x0 1, 100; blank 300 | acquisition at 100; hold at 400 |
| Revision | easy cue 100; blank 50; B alone amplitude 2 for 100; blank 50 | pre-challenge 150; final 300 |
| Distractor | easy cue 100; blank 50; B alone amplitude 2 for 20; blank 230 | pre-challenge 150; final 400 |
| Idle | zero input, 400 | every step |
| Ambiguous (descriptive) | cue d 0, noise_sd 0.3, x0 1, 300; blank 300 | final 600; identities and abstentions reported, no gate |

## 6. Outcomes

At each read point an output is **correct** (the named identity), **wrong** (another identity) or an **abstention** (−1). Raw multi-active states map to −1 through `committed`, as historically; they are also counted separately.

Every primary rate uses all 400 assigned rows. Hold, revision and distractor succeed only with a correct A at the pre-challenge read and the required identity at the final read; initial failures stay in the denominator. Conditional rates, with their denominators, are reported beside them for comparison with H9.

The following are logged step by step, per arm and row:

- A-to-B transitions, with and without an intervening abstention;
- gate closures and openings;
- raw graded-state changes;
- e's leader, and disagreement between e's leader and the raw identity.

Time to revision is censored for rows that never revise; those rows are never removed.

## 7. Registered criteria (all must pass; no endpoint is chosen after evaluation)

Single proportions use two-sided 95% Wilson intervals. Between-arm differences use a paired percentile bootstrap: 5,000 row resamples, one shared index matrix per stage.

| Criterion | Acceptance |
|---|---|
| Implementation | Historical reproduction (section 8); forced-open arm = arm 2 bitwise; forced-closed arm output always −1; no reset input anywhere; label-permutation equivariance: permuting channels of the input and internal-noise tapes permutes states and outputs (states within 1e-12, outputs exactly) on the first 40 rows of every condition; finite states; complete rows |
| Easy acquisition | Correct A at step 100: lower bound ≥ 0.90 |
| Hard-cue errors, every scale | All-row wrong rate at step 600: upper bound ≤ U, with **U = 0.04 (≤ 8 of 400)** [owner, 12.3] |
| Anti-trivial abstention, every scale | Candidate correct minus bistable correct at step 600: paired lower bound ≥ −0.05; raw correct/wrong/abstain counts shown |
| Retention | Correct at 100 and the same correct identity at 400: lower bound ≥ 0.90 |
| Revision | Correct A at 150 and correct B at 300: lower bound ≥ 0.85 |
| Distractor resistance | Correct A at 150 and correct A at 400: lower bound ≥ 0.90 |
| Idle | No exposed commitment at any of the 400 steps: lower bound ≥ 0.98 (an identity for arm 3; see 2.2) |
| Added value of the gate | Arm 2 wrong minus candidate wrong, hard cue x0 1: paired lower bound ≥ +0.05 |

These all-row bars are new proposals. They differ from H9's conditional point bars and do not revise H9, whose measurements are reported alongside. Arm 6 is judged on the same table. If it also passes, the report states that the separate evidence trace is not established as necessary; no superiority claim is made from non-significance.

## 8. Order, selection and stop rules

1. **Historical reproduction.** Run `python src/ph7.py all` unchanged; it must reproduce `experiments/h09/ph7_h9.txt` line for line. Then the new harness, driven by ph7's own generators, must reproduce ph7's D1–D6 counts for arms 1 and 2 (targets `default_rng(1000).integers(0, 5, 200)`, cue noise `default_rng(7)`, internal noise `default_rng(0)`, 200 rows). A mismatch is an implementation error: repair, disclose and rehash before any registered seed is used.
2. **Calibration** (seeds of section 9). Choose the first H10 setting passing every criterion, in fixed order: τ_e ascending, then θ ascending. Choose the first arm-6 θ_m passing, ascending. If no H10 setting passes, H10 stops **NOT SHOWN** for this family. No best-looking failure is picked, and a passing control does not rescue H10.
3. **Freeze.** Record the source, design, chosen settings and seed manifest with SHA-256 hashes.
4. **Development**, on its own seeds: every criterion again, as a check on the frozen implementation. A scientific gate failure stops before evaluation. An implementation repair is disclosed, rehashed and re-verified without changing any bar.
5. **One evaluation**, on its own seeds, only if development qualified it. The result is reported as it falls (pass, null, inconclusive or failure), with no added rows and no change to the family.

Every run happens in the local Claude session [owner, 12.7], one job at a time, with BLAS pinned to one thread. No GitHub Actions run is used.

## 9. Seeds and generators

Each condition in each stage has one registered integer. `numpy.random.SeedSequence(seed).spawn(3)` derives three child streams from it:

- child 0: the target permutation (80 per identity);
- child 1: the input-noise tape;
- child 2: the internal-noise tape shared by arms 1–6.

The idle condition uses only child 2. The bootstrap index matrix is `default_rng(bootstrap).integers(0, 400, size=(5000, 400))`, shared by every condition and contrast in the stage. No extra derived offset exists.

| Condition | Calibration | Development | Evaluation |
|---|---:|---:|---:|
| Hard cue x0 0.25 | 45101 | 45201 | 45301 |
| Hard cue x0 0.5 | 45102 | 45202 | 45302 |
| Hard cue x0 1 | 45103 | 45203 | 45303 |
| Hard cue x0 2 | 45104 | 45204 | 45304 |
| Hard cue x0 4 | 45105 | 45205 | 45305 |
| Easy acquisition and hold | 45106 | 45206 | 45306 |
| Revision | 45107 | 45207 | 45307 |
| Distractor | 45108 | 45208 | 45308 |
| Idle | 45109 | 45209 | 45309 |
| Ambiguous | 45110 | 45210 | 45310 |
| Bootstrap | 45111 | 45211 | 45311 |

Other seeds in use:

- **Historical reproduction only:** ph7's hard-coded 0, 7 and 1000.
- **Design arithmetic only:** 91919 (the ideal-observer Monte Carlo in `src/h10_design_check.py`); never a task seed.

**Scan, repeated before first use, 2026-09-27 (UTC) [owner, 12.6].** No number was replaced.

1. **Repository:** every file under the working tree (365 files; .git and __pycache__ excluded), pattern `(^|[^0-9])(n)([^0-9]|$)` for the 34 numbers. Standalone matches appear only in this design, `master_plan.md` and `README.md`, which carry H10's own registration, and in `src/h10_design_check.py` (91919). Elsewhere the target digits occur only inside longer digit runs, such as float digits (0.43550453058969907) and hashes, never as numbers.
2. **Graph node titles, one-liners and props:** `vinc_search` per number at limit 20. The control 71013 returns both nodes known to carry it in props (positions 1 and 4). The 34 numbers match only H10's own nodes: `concept:doc.d22b49532e5dd57bd`, `decision:h10-open-design` and `record:h10-design-check`.
3. **Graph document text:** the search's keyword arm does not index numeric tokens. Controls known to be in document text (71013, 20261081, 20261083) returned only semantic neighbours or word matches. A per-number search therefore cannot scan document text, and the earlier designs' "no full-text match" readings for numbers carried no information. The text half was done by reading instead. The 32 documents that have no repository counterpart were fetched in full, every fetch verified, and searched for the 34 numbers both standalone and inside longer digit runs, with no match. Those 32 are the Phase 0–7.3, H14–H16 and H19 reports; the H15 Run 1 and Run 2 reports and Run 2 specification v4; the H20 Stage A report, H20 design v1 and the H20 Run 2 diagnosis; the link-check report; the two-source check; the unrecovered-excess diagnosis; the ph12c result; Exp1–Exp4; the architecture spec; and the master plan addendum. The other 123 documents mirror repository files, which scan 1 covers; a mirrored text may differ from the committed file in small edits.

## 10. Predictions and risks

**Predicted with the section 12 recommendations:**

- The forced-open identity is exact.
- The forced-closed arm fails acquisition.
- Idle passes by construction.
- The simple mask equals arm 2 at the read points.
- Easy acquisition, hold, revision and distractor pass for every θ ≤ 0.016, as long as the graded circuit reproduces its historical 200/200. The settled easy-cue q is 0.057, and q after B alone is near 1.

**Not predicted:** whether the hard-cue wrong and anti-trivial bars pass together. That depends on how H9's wrong commitments relate to e's margin (2.3), which is the question the experiment asks. The ideal-observer frontier (2.6) is an upper bound, not a prediction. The largest risk is that the graded circuit commits early, on noise, on rows where the long-window evidence later becomes strong. The gate would then pass those errors. Disagreement counts will show it.

## 11. Stage B is conditional, not authorized by a module PASS

Unchanged from v1:

- Before any body integration, inventory how Agent17 reads the selector state, held identity, N2 release, presence, H19 navigation and the value gate.
- The candidate's actual output must drive the body; keeping a legacy `held()` path would bypass the intervention.
- A composition record states which reset controller is replaced and re-signs the affected maintenance, release and distractor criteria.
- The adopted agent is not touched.
- Body-level tasks, controls, bars and seeds are frozen in a separate design before they run.

Stage A alone cannot adopt H10.

## 12. The owner's confirmation

The owner confirmed this section on 2026-09-27 (UTC) with the words '권고안대로 확정하고 진행, 커밋 푸쉬' (gloss 'confirm as recommended and proceed; commit, push'); decision:h10-open. Every point was confirmed as recommended:

1. **θ grid: CONFIRMED** {0.004, 0.008, 0.016} (2.1). Not taken: v1's {0.02, 0.05, 0.10}.
2. **τ_e grid: CONFIRMED** {40, 80, 160}, as v1.
3. **Hard-cue wrong bar: CONFIRMED** U = 0.04, at most 8 of 400 (2.6). Not taken: v1's U = 0.025.
4. **The other bars: CONFIRMED** as v1: acquisition 0.90, retention 0.90, revision 0.85, distractor 0.90, idle 0.98, anti-trivial −0.05, added value +0.05.
5. **No agreement requirement: CONFIRMED** (2.3).
6. **Seeds: CONFIRMED** as section 9, with the graph scan repeated before first use (done; section 9).
7. **Execution: CONFIRMED** in the local Claude session, not GitHub Actions.
8. **Order and stop rules: CONFIRMED** as section 8.
9. **Gate: CONFIRMED** on the all-row interval table of section 7; the six Phase 7.1 criteria are reported as defined, not gating (2.10).

This file is design v2 FINAL. From here no bar, seed, arm, prediction or rule changes. The candidate text put to the owner (sha256 c64a5763d7b6f38d7a1703aa21d8ae1b1948bb9f3237b0003bde9e5b84a57f78) differs from this file only in the title, the status line, the U cell of section 7, the scan paragraph of section 9 and this section.
