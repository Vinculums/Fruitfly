# R2 scan-only implementation: cloud verification

Implements the owner's authorized standalone scan verifier on the existing draft PR branch. The contract is [step two design, rev three](https://github.com/Vinculums/Fruitfly/blob/7ef2070/notes/recommendations/2026-10-07-r2-step2-design-v1.md). Measurement and behavior acceptance are N/A. No experiment implementation or historical record is changed.

## Registration provenance

The manifest's `entries` are exactly equal, in order and every field, to [the owner's entries](https://github.com/Vinculums/Fruitfly/blob/ee415d09a5bac4f100077f371f647b2f1878550f/notes/recommendations/2026-10-07-r2-step3-owner-entries.json). The source is the JSON array at that commit, wrapped in `schema: r2-v1`, `decision: decision:seed-scan-exception-pairs-r2`, and `entries`. All four owner-local file digests are preserved verbatim; none was remeasured, inferred from another file, or substituted.

The approved entries comprise ph33: 25 rows / 29 occurrences; ph35: 17 rows / 17 occurrences; twelve distinct files, six shared paths. The cloud checkout lacks the three optional JSON copies and the optional NPZ. This is not owner-tree validation. Scratch optional-file fixtures test the contract, not the owner's missing bytes.

## Implementation and checks

`python tools/verify_seed_scan_r2.py` checks source pins before imports, reads and verifies the manifest integrity pin before parsing, and calls each unchanged `seeds_unused()` directly. It reports the original file count and hit-file count separately from covered rows. For each registered file, count and digest are computed from the same raw byte buffer. The ph35 hit-file result is expanded with its actual returned seed set and original pair exclusion; ph33 retains its original pair exclusions and checks that its reported hit numbers still match the byte buffer. No scanner function, source, constant, import guard, or traversal rule is replaced. No behavioral adapter or experiment execution is part of the command.

All digest encodings use the strict character-only a–p representation. The verifier pins its local source import closure and checks ph33's ph32 pin plus the existing ph36b full pin and ph38 prefix for ph35. The original source files, downstream sources and their pins remain byte-identical to the starting commit. The verifier's own digest is reported at execution rather than embedded in itself. Use this report with the committed verifier source.

Passed checks:

- Cloud R2 command: source pins, downstream pins, manifest integrity, schema and hit coverage pass. Per-checker results appear below.
- Focused positive/negative suite: `python -W ignore::ResourceWarning -m unittest discover -s tests -v` passes eleven tests, including multiple mutation cases. Suppression only hides the original scanners' unclosed-read resource warnings.
- Negative cases cover uncovered file/number pairs, checker and alias scope, other-checker resolution, extra occurrences, matching-digest count drift, same-count byte drift, seed removal, newline conversion, other seeds in an approved file, missing required files, optional absent/exact/drift lifecycle, malformed schema/digests/counts/paths, duplicate keys/rows, unsorted rows, missing/tampered manifest, manifest self-collisions, optimized execution, and original/downstream source and pin tampering.
- Original digit-boundary and raw binary behavior, legacy excluded pair semantics and checker return formats pass scratch regression tests.
- P5 checks the complete final bytes of the manifest, verifier, tests and this report against both original seed sets and byte digit boundaries. No new hits. No seed values are printed in this report.
- `cd src && python regress.py`: all 710 checks passed. This is the README regression command, not R2 measurement/behavior acceptance.
- Exact owner-entry equality, source preservation and `git diff --check` pass.

Legacy `ph33.py demo` and `ph35.py demo` stop at the original seed-scan assertion on approved hits. These are approved stops, not legacy demo passes. No recorded demo output was replaced.

Not run: owner-local four-file verification, downstream full experiments, paid or manually dispatched remote workflows. Measurement and behavior acceptance: N/A.

## Cloud scan results

| Checker | Scanned files | Hit files | Applied rows | Absent / unused rows | Errors |
|---|---:|---:|---:|---:|---:|
| ph33 | 428 | 6 | 22 | 3 | 0 |
| ph35 | 428 | 5 | 13 | 4 | 0 |

Local coverage: incomplete.

Verifier SHA (a–p): `npddnjepnigkelbgmjenooafgfanbpgnojoipfbnfenbadnigjagmmgjgldgfken`.

Manifest SHA (a–p): `gkkeiinehcdkdajmgdhpcagkffdhjojkglbljnmefphakmogknnljmloeaacligg`.

The absent rows are unused and never applied. A successful cloud exit does not establish coverage of absent files. Re-run the command in the owner's unchanged full working tree to check those bytes against the preserved registrations.

## Future registration and rollback

Do not automatically refresh a digest, count, source pin or manifest pin after drift. The owner must review changes against the decision; a new pair or broader scope needs separate authorization. For newly authorized registrations, measure each actual file's raw bytes and count in the environment that holds it; never infer a local copy's digest from another copy. Preserve exact paths and checker-specific aliases, sort rows by checker/path/alias, serialize UTF-8 without BOM, LF and one final newline, then verify schema and P5 over the whole manifest. Recompute the manifest's character-only SHA digest and update its verifier pin only as part of the reviewed pair. Re-run positive/negative tests, source preservation, P5 and cloud/owner-local checks with their coverage distinguished. Roll back manifest and corresponding verifier together to an approved commit. The command provides no runtime pin override.
