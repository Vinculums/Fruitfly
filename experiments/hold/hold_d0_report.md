# Hold D0 passive recount

Date: 2026-10-09. Status: **completed; six passivity gates pass; candidate screening remains UNRESOLVED; no E1 opened and no benefit verdict.**

Registered design: [branch exposure design v2 FINAL](../../notes/hold/2026-10-09-hold-branch-exposure-design-v2.md). Scope clarification: [bound reading review](../../notes/hold/2026-10-09-hold-bound-reading-review.md), stored separately during the run without changing its measurements, criteria, sample or implementation. The observed counter margins below are empirical checks on these states. The draft's universal claim across every world and horizon is not established: circuit noise is Gaussian with unbounded support.

## Execution and validity

The owner-approved D0 was run once at full size, using existing primary strata A1–A4 and B1–B2, each 400 rows × 600 steps. Existing evaluation seeds were deliberately reused by alias: `ph35.SEEDS['eval']` and `ph33.SEEDS['eval']`. No new world, new seed, agent parameter, learning arm or counterfactual feedback was introduced.

The runner wraps the unchanged `hold_stage1_instrument.PassiveFly` externally and reuses stage one's pair runner. All six strata pass L1 recorded-field byte equality, L2 per-event state and generator hashes with no undeclared exclusions, L3 score equality, construction/draw coupling, identical inputs and returns, complete sample and actual-H projection equality. No statistics were aggregated before the final gate passed. P5 passed before the report JSON was written.

Runtime: Python 3.13.12 and NumPy 2.5.3, matching the original stage-one replay; BLAS/OpenMP/MKL threads and PH30/PH32/PH33 process settings all pinned to one. Four independent arithmetic/event-timing tests passed, including exhaustive enumeration of uncertain draws against the exact tie recurrence. A separate six-stratum smoke check passed before full execution.

Raw record: [hold_d0_replay.json](hold_d0_replay.json). Its SHA-256 in the runner's digit-free a–p alphabet is `oakjaokgcpnabplmiaidjkdchoiiekclnhfgibkalbpfilkdnaojiifjhijhkoeh`. The raw record contains every per-row summary, per-hold counter record, pre-move B2 plume probability and source/design hash used to derive this report. Python/platform/version and thread/process pins are also recorded there.

## Measured read-out and sets

**All six strata have zero differing clipped commands**, over 1 440 000 total row-steps. This reproduces stage one's adopted-scope observation and supplies no benefit comparison.

The following counts each use all 240 000 row-steps of their stratum. H and R have the same size counts. The complete per-row distributions and every size, including zero, are in the raw record.

| stratum | top size zero | top size one | top size two | eligible size zero | eligible size one | eligible size two |
|---|---:|---:|---:|---:|---:|---:|
| A1 | 1 279 | 238 721 | 0 | 1 279 | 238 721 | 0 |
| A2 | 29 174 | 210 826 | 0 | 29 174 | 210 826 | 0 |
| A3 | 96 492 | 143 508 | 0 | 96 492 | 143 508 | 0 |
| A4 | 27 692 | 212 308 | 0 | 27 692 | 212 308 | 0 |
| B1 | 14 | 224 513 | 15 473 | 1 900 | 238 100 | 0 |
| B2 | 271 | 97 968 | 141 761 | 32 354 | 207 646 | 0 |

B1 and B2 each have four simultaneous B–D burst steps on three rows and 12 raw latest-burst-tie row-steps on three rows. Neither has a tied-single nonburst row-step. Their shared-top qualifying T1–T4 denominator is zero, as is T1–T5. **The conditional identity-split fraction f_id is undefined, not zero.** A raw timestamp tie does not imply a two-member eligible ranked set: both three-channel strata have zero such eligible row-steps.

## Measured hold margins

A hold is a contiguous actual held identity. The record distinguishes its formation counter, maximum counter while it remains held, reset requests, consecutive reset requests, actual identity exit, first/last request-to-exit lag and right censoring. Timeout/evidence requests do not mean immediate release. Inherited harness construction is labelled separately from natural formation.

| stratum | naturally formed holds | inherited holds | maximum natural formation counter | maximum natural held counter | maximum inherited held counter | maximum counter surviving an evidence reset | presence window |
|---|---:|---:|---:|---:|---:|---:|---:|
| A1 | 1 723 | 0 | 9 | 56 | — | 42 | 200 |
| A2 | 936 | 0 | 11 | 58 | — | unobserved | 200 |
| A3 | 595 | 400 | 9 | 55 | 187 | unobserved | 200 |
| A4 | 1 175 | 0 | 9 | 56 | — | 25 | 200 |
| B1 | 2 126 | 0 | 10 | 57 | — | 53 | 300 |
| B2 | 1 495 | 0 | 10 | 57 | — | 54 | 300 |

A3's inherited counter begins at 140. Its observed maximum 187 stays 13 ticks below the two-channel presence window. Naturally formed holds stay at least 142 ticks below the two-channel window and 243 below the three-channel window. No held state or evidence-reset-surviving state reaches its presence window. Every registered observed-window check passes. These margins support the presence reading on the recorded sample, with the universal-theorem limitation stated above.

## Frozen-position arithmetic proxies

The audited burst formula agrees with `fly.py`: the current whiff plus at least two whiffs in the preceding nine ticks. The model uses the two latest preceding whiff ages, yielding 46 states per channel, with a joint distribution restricted to equal most-recent burst timestamps. A lone burst destroys a tie; simultaneous bursts reset its timestamp; never/never is excluded. This exactly carries the time-varying independent Bernoulli histories and their Poisson-binomial burst expectations; no stationary approximation or random draw is used.

B's probability is read from **the actual B2 sensing position before the move**, using the inherited plume law. W1Dp uses that same probability for an independent D draw; W1N uses the masked valued source's raw plume probability. B2's fraction with nonzero B plume probability is **0.0892125**. These are expectations conditional on W1D trajectories; candidate agents would follow other trajectories. Presence, held identity and clipped command are not predicted.

| conditional quantity | W1Dp | W1N |
|---|---:|---:|
| expected simultaneous B–D bursts | 151.879399 | 0.056070 |
| expected latest-burst-tie row-steps | 11 642.702296 | 5.973995 |
| expected tied-single nonburst row-steps | 118.312857 | 0.120615 |
| upper bound on expected exposed rows, before presence/identity requirements | 118.048201 | 0.120615 |
| conservative upper bound on probability of at least 40 exposed rows | 1.000000 | 0.003015 |

The row bound uses `sum(min(expected tied-single events per row, 1))`. Markov's inequality divides this bound by 40 and caps the result at one. It is deliberately an upper bound, not a fitted or calibrated P(X3). Actual command exposure requires the remaining presence and identity conditions as well. Because no natural qualifying tied-single state was observed, the proposed f_id anchor cannot be estimated from D0.

**The approved deferral rule is not established for both candidates.** W1N's frozen-position upper bound is below 0.5; W1Dp's bound is uninformative at one. D0 therefore records **UNRESOLVED**, without claiming W1Dp meets the threshold or predicting that it fails. No E1 harness or new condition is authorized by this result. A decision about a new condition requires an explicit follow-up design/owner opening. The separate approved stage-two coverage work remains independent of this unresolved candidate screen.
