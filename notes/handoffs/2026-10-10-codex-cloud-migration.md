# Fruitfly cloud migration — 2026-10-10

Status: PREPARATION COMPLETE. Source and evidence publication, environment publication and functional fresh-task startup checks passed. See notes/handoffs/2026-10-10-codex-cloud-closing.md and .json. The owner authorized source publication, evidence transfer and cloud setup: "그럼 모두 해야지". This record does not open EVAL.

## Source and archive

Repository: https://github.com/Vinculums/Fruitfly
Branch: `codex/cloud-handoff-2026-10-10`.
Initial source commit: `8b0c9c94882b6d7aaa98fa41a0c87e581f7bed81`.
Evidence release: https://github.com/Vinculums/Fruitfly/releases/tag/fruitfly-evidence-2026-10-10 .

The initial commit publishes 211 added/updated small files and verifies 138 committed frozen sources byte for byte. The three maps retain 112 / 133 / 6 entries, 139 unique files. The one large frozen source evidence file h17_run3_native_boundary_checks.json is external. The branch supplies config/cloud-evidence-manifest.json and this guide. The published tool update is 78068b9c6eb902f57d8c9287f9c5d3fbc4afd3d7. The owner's original working branch/index were preserved.

Manifest: 13 originals, 10789289571 bytes; 16 gzip parts, 5949077102 bytes. All parts are below the release asset limit. Original hashes were freshly calculated during packing and all available frozen bindings matched. The manifest distinguishes matches to prior bindings from fresh transfer hashes. All sixteen parts and the original manifest are uploaded. All seventeen server-reported sizes and SHA256 digests match the transfer manifest; see 2026-10-10-codex-cloud-github-assets.json. Cloud reconstruction remains separately verified.

## Restore

Use the migration branch, not older main. In a clean cloud checkout:

```bash
git fetch origin codex/cloud-handoff-2026-10-10
git switch --detach origin/codex/cloud-handoff-2026-10-10
bash tools/setup_cloud.sh
python3 -B tools/restore_cloud_evidence.py --manifest config/cloud-evidence-manifest.json --root .
python3 -B tools/check_cloud_readiness.py --full
```

Restoration uses .git/cloud-evidence-cache, retaining existing scanner exclusions. It validates HTTPS, strict relative paths, every compressed part and final original size/SHA256(a-p). Exact originals are hash-verified and skipped; different existing files are never overwritten. Publication is exclusive and atomic after verification. Use --only with an exact relative artifact path to restore one file. --verify-only checks existing originals without downloading. --sources-only explicitly defers large archival bytes.

Pure tests: restore 22 PASS, source checker 10 PASS, safe Vinc reader 10 PASS; combined 42 PASS. Original P5 new-byte checks PASS. Local source check: plan_ready true, execution_ready false, no errors, thirteen explicit deferrals. No scientific arithmetic or runtime acceptance was rerun.

.gitattributes disables normalization for frozen/transferred bytes; verify actual committed/checkout hashes. .gitignore lists thirteen external artifact paths for Git bookkeeping, without adding scanner exclusions.

## Target environment

Setup task: https://chatgpt.com/local/01a1259f-1733-72dc-a3c6-f576207a1010
Name: Fruitfly H17 준비. UI privacy: Only me.
Initial checkout: /workspace/Fruitfly at older main 0ee20d9b8f7c4577c1f6cfcec45daba0700390bf.
Observed planning runtime: Linux / Python 3.12.14 / NumPy 2.3.5; assertions active and all six numeric thread variables 1 under the wrapper.

The environment was created before migration publication. Fetch and checkout the migration branch, run source checks and archival restoration, then publish the prepared environment snapshot and verify a fresh task startup. Saved/draft settings are not actual runtime or publication readiness.

Only the required api.github.com, mcp.vincs.io, vincs.io and release-assets.githubusercontent.com destinations were added to the existing restricted policy. Recheck enforced runtime observations and actual calls after applying settings.

## Vinc

Team space: 01a0b944-ecb4-737b-b3e6-5cc99ff37654.
Historical handoff d0d04637cd9ba7a6b; inventory d84950d0651c03934; DEV report d60929b82c419fa4b; DEV closing receipt decef2d816309d16e.

Desktop canonical reads were verified. The new stdlib check_vinc_cloud.py also read both fixed documents via the exact REST route: HTTP 200, verified true, canonical text equals checked-out local text. Run python3 -B tools/check_vinc_cloud.py in the target after the personal secret is available. The initial cloud task has no callable Vinc connector and did not verify these documents. Reachability alone does not supply authorization. Verify actual canonical text through an authorized connector or configured credential route. Store credentials only through environment secrets; never Git, reports, prompts or terminal output.

## Scientific boundary

DEV remains operation PASS and nine statistical clauses PASS; twenty validity gates, 102473 independent saved arrays, 510 ROOT arrays, no ROOT RNG/zero draws. Historical H0/BENCH/DEV are preserved. EVAL has zero claims and is unopened; nothing adopted.

Frozen Windows executable/library paths and hashes remain historical authority. Linux preparation establishes no runtime comparability. P4 retains scientific execution in the authorized local session and forbids hosted-runner simulation. A separate execution-location/runtime amendment, comparability review, pins and owner decision must precede any proposed cloud experiment. EVAL also requires its own concrete package and separate opening.

Next cloud work: prepare the isolated EVAL design and runtime migration proposal from saved evidence and verified source. Do not execute scientific runners, consume fresh pairs, tune GS250, change old pins, retry spent stages or assert adoption.

## Closing evidence

Closing receipts record all seventeen matching server assets, thirteen restored originals, 151 cloud byte checks, 42 passing pure tests, the published personal environment and a fresh-task PASS with GitHub HTTP 200 and actual enforced network observations. Cloud Vinc credentials are owner-managed by explicit owner instruction; no additional request or wait is required. Scientific execution and EVAL remain separately gated. Snapshot-ID/startup-source metadata not exposed to the fresh task is explicitly unverified.
