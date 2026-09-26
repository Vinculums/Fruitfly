# H12 remote diagnosis and execution record

Date: 2026-09-27 (Asia/Seoul).

The owner requested testing with GPT-6-sol without running the simulation on the owner's local CPU. GPT-6-sol authored the diagnostic harness and owns the test-result review. The parent agent reviewed the instrumentation and orchestrated the remote runner. File editing, Git operations and result retrieval used the Windows workspace; all new simulation execution in this request used GitHub-hosted Linux compute.

## Execution boundary

The current Codex terminal is local Windows. Changing the model does not change that terminal's execution host. This session instead submitted the tests to GitHub Actions, with `runs-on: ubuntu-24.04`, a 45-minute timeout, one numerical thread, read-only repository permissions and pinned action revisions. No new server or self-hosted runner was provisioned. Actions usage is associated with the repository's existing GitHub account.

The baseline checkout is pinned to `6870b4d7e50629b5362ab40454251ef94183bd83`. It is isolated from new review files because the historical seed scanner inspects repository files. The diagnostic script imports unchanged historical modules in the current checkout. Original scripts, design text, output files, main and the original research branch are preserved.

## Verified baseline reproduction

- Run: https://github.com/Vinculums/Fruitfly/actions/runs/36259440207
- Submission commit: `c8c3ca08d4805d5cc7c6e3a81b9739cff914e161`.
- Completed successfully; job duration 3 minutes 9 seconds.
- Python 3.11.15, NumPy 2.4.6, Ubuntu 24, Linux x86-64, 2 CPUs.
- Provenance asserts `RUNNER_ENVIRONMENT=github-hosted` and Linux; hostname `runnervmtr4k5`.
- The entire stdout of `python src/ph36b.py bench` matches the historical `experiments/h12/ph36b_bench.txt` byte for byte, including source checks, seed scan, all arm summaries and identity checks.
- The historical conclusion remains Stage 2 bench **UNREADABLE**. A successful reproducibility test does not turn that experimental result into a PASS.

## Package D

Submission: https://github.com/Vinculums/Fruitfly/actions/runs/36259858400, commit `7684de6bdbe4f365aad07ac9592717da7fc028b7`.

This first full diagnostic attempt reproduced the original bench again and passed instrumented identity and own-stream replay checks for all three donors. It then stopped in `retention_summary`: the sign array still had 400 entries while the valid-denominator mask selected 381 entries. The resulting broadcast error was in new reporting code. The exception prevented publication of a completed diagnostic report. The failed run and its manifest remain available; the corrected run is recorded below after artifact inspection.

### Completed run

- Successful run: https://github.com/Vinculums/Fruitfly/actions/runs/36260387653
- Tested commit: `ac69bb7dd132a44456824237fc1133e9c8c64c22`.
- Job duration: 6 minutes 25 seconds, including setup, full historical reproduction, diagnosis and artifact upload.
- Diagnostic SHA-256: `43bbde6c068baf2d16ce3812a9bb04a7a6f9fa2716ac19e18a948ad14b1c84ef` (also verified against the local file).
- All original-field identities, three own-donor replays, D=0 clone equality, zero-input retention, acquisition-weight invariance and historical headline/contact counts passed.
- The corrected summary helper checks mixed valid/invalid denominators and the empty-valid-set case before simulation.
- The collected summaries and runtime manifest are saved under `experiments/h12/diagnosis/`. The full event archive is retained in the run artifact and downloaded separately; it is not committed as a large binary.

### Results

The original bench remains UNREADABLE. P4 V-majority counts are H12 33/400, gate-only 10/400, parallel/no-decay 10/400, supplied ceiling 42/400 and floor 5/400. The ceiling-floor gap is only 0.0925 against the existing 0.30 readability bar.

The A0/A1 identity assumption is false beyond rounding error. On every one of the three fixed donor streams, single-site/no-decay versus parallel/no-decay reaches a maximum absolute value difference of 0.2036079284; the first difference above 1e-12 appears at step 606. Their closed-loop trajectories depart on 350/400 rows. An H12-versus-A0 contrast therefore changes both layout and decay.

Pure retention starts from the identical A1 memory checkpoint at step 2400, for all 400 rows:

| Zero-input retention duration | Median value, decay on | Median value, decay off | Above competitor +0.5 | Crossed upward from below +0.5 |
|---|---:|---:|---:|---:|
| 0 | 0.374417 | 0.374417 | 52/400 | 0/400 |
| 1200 | 0.507910 | 0.374417 | 208/400 | 156/400 |
| 5000 | 0.767818 | 0.374417 | 384/400 | 332/400 |

The signed recovery fraction is defined for 381 rows and undefined for 19 under the declared denominator rule. Its valid-row median is 0.213391 at 1200 and 0.632157 at 5000. Nine values remain negative at all three reported durations; there is no universal positive-memory recovery claim. Counts and behavioral denominators retain all 400 rows.

**Additional correction from the negative rows:** a read-only inspection of the existing arrays ran remotely at https://github.com/Vinculums/Fruitfly/actions/runs/36261176952. All nine negative rows had P1 value +1 but a negative acquisition component by the P2 boundary. Seven have a positive parallel component at that boundary, so decaying it makes their total value more negative. Two improve but remain negative. The acquisition weights are invariant during the new zero-input retention test; they were not invariant during the preceding embodied learning phase. These are different claims. Parallel topology alone does not guarantee preservation of a positive acquisition memory.

The stored values agree with `acq_P2 + par_P2 * (1 - 1/5000)^D` to maximum absolute error 3.431e-14 across the tested durations. The same nine row IDs are negative at all three checkpoints. Detailed values and invalid-denominator cases are retained in `experiments/h12/diagnosis/retention-inspection.json`. No new trajectory, parameter sweep or seed was generated for this inspection.

The original P4 task strongly limits sensory opportunity: H12 has no V whiff in 332/400 rows, and even the supplied ceiling has no V whiff in 335/400 rows. In H12 the ordered partition is 332 no-whiff, 11 whiff-without-V-supported-navigation, 4 navigation-without-contact, 20 contact-without-majority and 33 V-majority. Its 116 ties include 115 rows with zero contact at either source. These are descriptive path-dependent measurements; they do not establish a unique causal explanation for each failure.

### Measurement conventions

The presence state is computed inside `Agent9.act` before the navigation decision. Navigation attribution reconstructs the actual keep/top branch; a valued whiff may support navigation even when the valued odour is not held. Negative-held flee overrides and simultaneous support from both channels are reported separately. The reconstructed V-or-N contributors must account for every recorded navigation hit. This attribution describes the program's branch, not a counterfactual biological cause.

The ordered opportunity categories partition all 400 assigned rows; they do not define a filtered success rate. Unconditional V-majority and zero-contact versus positive-dwell ties are reported separately. Rounded float32 trace/output diagnostics are descriptive; original-field and replay-value identity checks use the original precision.

Package D reuses the spent bench input pair only. Development and evaluation remain unused. Package E remains a proposed, unregistered intervention and is not executed by this workflow.

### Interpretation limits

Same-input replay estimates differences between the modules conditional on each donor's fixed source-contact and reward sequence. A different donor supplies a different history. These comparisons do not uniquely decompose the original closed-loop effect into additive contributions.

Pure retention starts from each A1 checkpoint before step 2400 and changes only decay during a zero-input interval. Every assigned row is included, regardless of extinction success. A change in the retained memory does not establish behavioral expression or autonomous return. The original P3 remains a different intervention because source-contact learning continues while navigation whiffs are masked.

The next behavioral test therefore needs matched initial memories, equal sensory opportunity, frozen memory during choice and predeclared readability/effect criteria. Moving the agent closer and repeating the old continuously learning comparison would leave the causal ambiguity unresolved.

## Next work after Package D

Package D is complete at the measurement level. This dated report is an additive H12 evidence erratum: A0/A1 are not general identities, and the acquisition component can change sign during the embodied input schedule. Carry both corrections into any next registration while preserving the original results and source hashes.

Prepare Package E as a separately registered test of whether retention-only decay changes choice. Use the same A1 checkpoints in both arms; D=0 for identity, D=5000 as primary and D=1200 as the bridge; fresh matched navigation states with both sources accessible; frozen weights/traces and no reinforcement throughout read-out. Report all 400 rows, including the nine inverted memories and nineteen undefined recovery fractions. Keep the previously proposed readability and effect criteria explicitly proposed until registration; do not select a criterion from these results. Scan and register new calibration/development/evaluation seeds before running them.

The learning-address contract remains separate: the harness supplies V source-contact code after movement, rather than demonstrating learning credit assigned through the held identity. Neither the recovery measurement nor a future controlled-choice effect would by itself establish a portable recognition-to-learning core.
