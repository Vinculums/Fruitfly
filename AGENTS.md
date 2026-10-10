# Fruitfly project instructions

These instructions are self-contained for a fresh checkout. The owner's local
SuperClaude profile is not required. Read `master_plan.md`, then the latest
dated documents in `notes/handoffs/`, and the H17 Run3 v3 FINAL design and DEV
report before deciding what to change.

## Current scientific authority

H17 Run3 DEV is complete: operation PASS, all nine frozen statistical clauses
PASS, twenty validity gates PASS. Independent verification checked 102473 saved
arrays; ROOT recomputation checked 510 arrays without creating RNGs or drawing
samples. BENCH and historical H0 dispositions remain as recorded. Nothing was
adopted. EVAL has no claim and remains unopened behind its separate owner gate.

The owner authorized source publication, evidence transfer and cloud setup on
2026-10-10. This authorization does not open EVAL, authorize new simulations,
change frozen science or resolve Windows-to-Linux runtime comparability.
Cloud work may inspect code, verify archival bytes, run isolated synthetic pure
tests, and prepare an EVAL/runtime migration package for review.

Preserve the 112-file specification, 133-file MAIN implementation and six-file
DEV source closures, their exact bytes and pins. Preserve claims, historical
attempts and original H0/BENCH/DEV evidence. Do not regenerate missing evidence,
rerun spent stages, retry/reseed/replace/extend pairs, retune GS250, change
criteria or sample sizes, or edit the adopted Fly as part of migration.

## Standing project rules

- P1: check a known-answer expectation for saturation before registration. If
  its arm is at a ceiling or floor, record relative ratio/multiple criteria as
  SATURATED and unread, never MET or NOT MET.
- P2: state where every behavioural loop is anchored and whether a proposed
  change moves that anchor before registering a prediction. Retain saved
  anchors and raw arrays for independent arithmetic checks.
- P3: ROOT independently recomputes registered headline readings from saved
  arrays before final result registration, including when execution is delegated.
- P4: scientific simulations run in the authorized local session, never on
  GitHub Actions or hosted runners. Use one numeric process, assertions enabled,
  optimize zero, and all six numeric thread variables equal to `1`:
  `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`,
  `VECLIB_MAXIMUM_THREADS`, `NUMEXPR_NUM_THREADS`, `BLIS_NUM_THREADS`.
- P5: apply the original ph33/ph35 protected-token guard and authoritative R2
  exception manifest to new bytes. Do not add exceptions or excluded folders
  to make a migration check pass. Use the existing
  `tools/verify_h17_r0.py:no_protected_tokens` guard; do not print reserved seeds.

The Windows CPython/NumPy runtime stamp is immutable historical evidence. A
Linux Python installation is suitable for preparation only; do not bypass or
rewrite the exact runtime preflight. A proposed execution runtime requires a
separate comparability review, pins and owner decision before the EVAL opening.

## Source and evidence checks

Run `bash tools/setup_cloud.sh` for a standard-library preparation check.
Run `python3 tools/check_cloud_readiness.py --sources-only` without downloading
large evidence. Its explicit deferred-file list is not evidence acceptance.
Restore evidence using `config/cloud-evidence-manifest.json` and the migration
guide, then run `python3 tools/check_cloud_readiness.py --full` to check saved
bytes. Neither mode runs a simulation or verifies scientific arithmetic.
Never describe a planning check as scientific execution readiness.

Preserve other people's working-tree changes. Stage only the reviewed migration
set; check committed/remote bytes against source pins because line-ending
normalization can change hashes. Source publication is incomplete until the
actual remote commit and fresh checkout checks have been recorded.

## Canonical records

`master_plan.md` is the Git source of truth. Immediately after any master-plan
edit, synchronize and read back all thirteen Vinc canonical mirrors before any
further master-plan work. Do not invent a successful mirror update when access
is unavailable; report the incomplete synchronization.

Vinc team space: `01a0b944-ecb4-737b-b3e6-5cc99ff37654`. Read current conventions
before writes. Use English canonical titles and prose, preserving literal owner
quotes. Fetch existing node properties before replacing them: props are a full
replacement. Record actual source paths, a-p SHA-256 hashes and canonical doc
IDs. Require verified canonical reads and exact document/graph readback.
Desktop connectivity does not prove cloud access. Keep credentials in configured
secrets, never in Git or reports. If cloud writeback is unavailable, preserve
local receipts and report the missing verification.

When work exceeds fifty files or complexity exceeds the project's delegation
threshold, parallel agents may take separate explicit ownership. They must not
revert one another's edits. Final verification and scientific authority remain
with the reviewing ROOT session.

Current migration progress and restoration instructions: `notes/handoffs/2026-10-10-codex-cloud-migration.md`. Read its closing receipt when available before relying on cloud readiness.
