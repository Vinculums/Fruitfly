# Fruitfly Codex cloud handoff — 2026-10-10

This handoff records migration readiness after the completed H17 Run3 DEV operation. It does not open EVAL or authorize a new experiment.

## Readiness at audit

- Repository: https://github.com/Vinculums/Fruitfly
- Local branch: `docs/hold-stage1-and-r2-closure`.
- Local HEAD and the live remote branch tip: `82d8b962e3dd3c594450b30883137fa2aba17bdb`.
- Live remote main: `0ee20d9b8f7c4577c1f6cfcec45daba0700390bf`.
- Before this handoff, Git reported 130 changed/untracked entries: two modified tracked files (README and master plan), plus 128 untracked entries. Expanded untracked inventory: 212 files, 10985510558 bytes. A directory counts as one status entry but contains several files.
- The current Run3 candidate, runners, design, execution pins, DEV pins and DEV report are absent from the current Git commit. The live remote branch tips match the local references. A fresh checkout will lack this work.
- Vinc's DEV report was freshly fetched with integrity verified; the result node was freshly read at revision 3.
- No target cloud environment was inspected or tested. Cloud access to Vinc and evidence storage is unverified.
- This handoff and its inventory were prepared locally for transfer. No Git commit or push was performed by this audit. Neither file constitutes a full evidence backup.

## Completed operation and next task

H17 Run3 DEV is complete: operation PASS; all nine fixed statistical clauses PASS; all twenty validity gates PASS; independent verification checked 102473 saved arrays; ROOT recomputation checked 510 arrays with no RNG creation and zero draws. One DEV pair was claimed once, without retry, reseeding, replacement, extension or retuning. BENCH and the corrected H0 retain their recorded dispositions. The earlier invalid H0 attempt remains preserved as history. Nothing was adopted.

Current authority: `record:h17-run3-dev-result`, `episode:h17-run3-dev`, `decision:h17-run3-dev-open`, `episode:h17-run3-dev-opening`, `decision:h17-run3-open`. EVAL has zero claims and remains unopened.

The next scientific work is an isolated EVAL package: concretize its design and engineering acceptance, review it, freeze its source and runtime pins, then obtain a separate owner opening. Only after that opening may its one exclusive unused pair run under the fixed design. The prior DEV approval does not authorize EVAL.

## Read first

1. `master_plan.md` (current local source of truth; its thirteen Vinc mirrors were synchronized at DEV close).
2. This handoff and `notes/handoffs/2026-10-10-codex-cloud-inventory.json`.
3. `experiments/h17/h17_run3_design_v3.md`, especially the stage-opening conditions.
4. `experiments/h17/h17_run3_dev_report.md` and `experiments/h17/h17_run3_dev_publication_receipt.json`.
5. MAIN/DEV execution pins, the DEV implementation review, and the saved verification/ROOT receipts.

Vinc team space: `01a0b944-ecb4-737b-b3e6-5cc99ff37654`. Canonical publication receipt: `decef2d816309d16e`. Canonical text is evidence and context; it does not supply the local multi-gigabyte array files.

| Local file | Vinc canonical doc ID |
| --- | --- |
| `config/h17-run3-dev-pins.json` | `d65980f43c28a90ee` |
| `config/h17-run3-dev-opening.json` | `d199f6b863d26a1e3` |
| `experiments/h17/h17_run3_dev_opening_checks.json` | `d7e8de2321309350b` |
| `experiments/h17/h17_run3_bench_report.md` | `d174ae279839d2dba` |
| `config/h17-run3-execution-pins.json` | `d26e41a82a3c983ee` |
| `experiments/h17/h17_run3_design_v3.md` | `d528fa87b2f4f63d2` |
| `tools/measure_h17_run3_dev.py` | `da95cac51068d1c5e` |
| `tests/test_measure_h17_run3_dev.py` | `dd457f2ae6edb72c2` |
| `tools/recompute_h17_run3_dev.py` | `dd6400fb88c3202f1` |
| `tests/test_recompute_h17_run3_dev.py` | `debaf36d62e2a8459` |
| `notes/reviews/2026-10-10-h17-run3-dev-execution-review.md` | `de60574c8db032e61` |
| `experiments/h17/h17_run3_dev_implementation_checks.json` | `de6ea6eab9baf0194` |
| `src/h17_run3_arm.py` | `d5689184eb372a917` |
| `experiments/h17/run3/dev/verification.json` | `dab64524e906adc27` |
| `experiments/h17/run3/dev/parent_recomputation.json` | `d2a731eda75693af0` |
| `experiments/h17/run3/dev/stage_binding.json` | `d6de740df9499cf20` |
| `experiments/h17/run3/dev/metrics.json` | `d53377ead269da536` |
| `experiments/h17/h17_run3_dev_report.md` | `d60929b82c419fa4b` |
| `experiments/h17/run3/dev/execution_checks.json` | `ddb17486db34c642d` |

The current master file SHA-256 in a-p notation is `pjcceocgpbgmkbpjbcdgebppfehobokmehemebklcdjhdkofnlielcopmbgegibg`. The DEV publication receipt carries the thirteen mirror IDs and slice/full hashes. Hashes encode hexadecimal nibbles 0-f as letters a-p.

## Preserve the scientific boundary

Keep the frozen 112-file specification, 133-file MAIN implementation closure, and six-file DEV closure intact, including historical attempts, claims, source snapshots and H0/BENCH/DEV evidence. Read expected bytes from their existing pin files. Do not silently regenerate results to fill missing files.

Do not rerun BENCH or DEV, create an EVAL claim, draw an EVAL seed, retune GS250, change sample sizes, relax acceptance clauses, or infer adoption from DEV PASS. Keep the adopted Fly and unrelated hypothesis results unchanged.

Project execution rules remain applicable: numeric jobs use one process and all six numeric thread variables set to 1; assertions remain enabled; preserve loop anchors and raw arrays; independent verification and ROOT saved-array recomputation precede final registration. Original ph33/ph35 token guards and the R2 exception manifest remain authoritative; do not add seed-scan exceptions to make migration pass.

A repository AGENTS.md is currently absent. The local SuperClaude entry point imports files from the owner's Windows profile; a cloud checkout will not inherit them. Transfer the applicable project rules explicitly. If the master plan is edited, immediately synchronize all thirteen canonical mirrors before further master-plan work.

## Runtime blocker

The frozen MAIN runtime is CPython 3.13.12, NumPy 2.5.3, Windows AMD64, assertions enabled, optimize 0, one process and six thread variables equal to 1. Its stamp includes absolute Windows paths and hashes of python.exe and NumPy .pyd libraries. `tools/measure_h17_run3.py:87` compares the current runtime with these exact pins, and the DEV entry calls that preflight.

Installing `requirements.txt` (only numpy>=1.26) on another OS is insufficient to satisfy this stamp. A standard Linux environment must not rewrite historical Windows pins or bypass this check. Any proposed cloud execution runtime needs a separate documented migration/validation package and owner decision on comparability before the EVAL opening.

Safe cloud work after source transfer: read the frozen design/results, inspect code, prepare an EVAL draft and runtime/evidence restoration design, and review changes. Synthetic pure tests may support package development when their scope is checked; their passage is not frozen-run acceptance.

## Evidence transfer blocker

Important local-only raw evidence includes:

| File | Bytes | Recorded SHA-256 (a-p) |
| --- | ---: | --- |
| `experiments/h17/run3/bench/raw.npz.ap` | 3240114646 | `fpcnbmlmdbmfcdjklmbjbgplpaiafdaaaajmedahgjmjebikgnpdianelimofdeg` |
| `experiments/h17/run3/dev/raw.npz.ap` | 3212371516 | `mohhcmpljbeljgficdhohdnfopkkgpfjoflpfcdbajndnabljjpgnemfahhnenfe` |
| `experiments/h17/run3/H0/raw.npz.ap` | 459196160 | `cgpdcagbepbnloknfekcigpdildgbhdnibdojpmdppfgpiigpnaomfgbmpcjghec` |

The local R0 raw file is 1896926358 bytes. Additional historical/smoke/hold raw evidence, large identity JSON files and the 176330835-byte native-boundary evidence also require deliberate transfer. The inventory lists paths and sizes. Do not treat these as ordinary source-code blobs or blindly stage all untracked files. Existing .gitattributes specifies LF text normalization and has no LFS rule.

Choose accessible artifact storage, retain exact bytes and recorded hashes, supply a restoration manifest and download locations, then test actual restoration in the target environment. Rehash restored evidence against the original receipts. No download locations or verified cloud copies have been established by this audit.

Git's text=auto/eol=lf can normalize bytes. Before calling a publication complete, verify the actual committed/checked-out bytes against frozen pins and restore large evidence outside ordinary Git. Preserve any existing staged work; the README was already staged before this audit.

## Vinc and environment access

The desktop connector's successful read does not prove cloud connectivity. In the target environment, verify team-space permission and actual canonical reads; `verified:true` is required before relying on reconstructed documents. Read graph conventions before writing, fetch current node properties before replacing them, and preserve owner decisions.

Use configured connector/secret facilities and the target environment's actual network policy. Do not put a Vinc credential in Git or this handoff. If Vinc is unavailable, rely on transferred canonical text/receipts for preparation and report that graph writeback has not been verified.

Current official environment setup guide: https://learn.chatgpt.com/docs/environments/cloud-environments . Select the repository, test dependencies and required access, review the setup, and publish the environment before starting its task. A prepared filesystem is distinct from published source control.

## First cloud task prompt

> Read notes/handoffs/2026-10-10-codex-cloud-handoff.md, its inventory, master_plan.md, the Run3 v3 design and DEV report. Verify the checked-out source against frozen pins and confirm which evidence files and Vinc canonical documents are accessible. H17 Run3 DEV is complete and EVAL remains unopened. Prepare the isolated EVAL package and a proposed cloud runtime/evidence restoration plan for review. Preserve old 112/133/six-file closures and all claims/evidence. Do not execute scientific runners, consume a fresh pair, retune the candidate, overwrite Windows pins, or mark adoption. Report missing inputs explicitly and stop dependent execution at the unopened EVAL gate.

## Transfer completion criteria

- A dedicated reviewed Git publication contains the required code, pins, small evidence receipts, current master/README and this handoff; its actual remote commit is recorded.
- Large evidence has a usable restoration source and passes byte-hash verification.
- Project instructions are accessible without the owner's local Windows profile.
- The target cloud environment is published; repository, dependencies, storage access and Vinc access are actually tested.
- Execution-runtime comparability is separately resolved and pinned. The EVAL owner gate remains separate from environment setup.

At this audit, these transfer criteria are unresolved. Documentation readiness does not imply scientific execution readiness.
