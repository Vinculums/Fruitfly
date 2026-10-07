# R2 step 3: owner-clone verification (Windows, 2026-10-07)

Run by the reviewing session in the owner's full working tree (Windows 10, cp949 console, Python 3.13 via uv, numpy present), on PR #2 at 9afb74a plus the one-line fix below. The tree holds the four owner-local files (the NPZ and the three remote-runs summary.json copies) that the cloud checkout lacks. Design: notes/recommendations/2026-10-07-r2-step2-design-v1.md (rev 3, 7ef2070). Decision: decision:seed-scan-exception-pairs-r2.

## One defect found, fixed, re-verified

At 9afb74a the command failed on Windows with every ph35 hit reported as "uncovered hit" and "registered rows no longer returned by original scan", while ph33 passed 25/25. Cause: ph35.seeds_unused() returns repository-relative paths with the OS separator (src/ph35.py builds them with os.path.relpath and does not normalise), ph33.seeds_unused() normalises to "/". The verifier compared the ph35 paths against the manifest's "/" paths unchanged. Fix (tools/verify_seed_scan_r2.py, one line): normalise the hit path with .replace("\\", "/") before the comparison; a no-op for ph33 and on POSIX. Nothing else changed. The verifier's own digest therefore changes; the cloud report's value belongs to 9afb74a, the value below to this commit.

## Result after the fix

Command: python tools/verify_seed_scan_r2.py  (exit 0)

```
{
  "command": "python tools/verify_seed_scan_r2.py",
  "verifier_sha256_ap": "emfhapidcjidpgaofpbkefkbbkhdihknflepbhakdhkfceganepjhpiaobhiccac",
  "manifest_sha256_ap": "gkkeiinehcdkdajmgdhpcagkffdhjojkglbljnmefphakmogknnljmloeaacligg",
  "source_pins": "PASS",
  "downstream_pins": "PASS",
  "measurement": "N/A",
  "behavior": "N/A",
  "checks": [
    {
      "checker": "ph33",
      "scanned_files": 500,
      "hit_files": 9,
      "hit_pairs": 25,
      "applied_rows": 25,
      "unused": [],
      "errors": []
    },
    {
      "checker": "ph35",
      "scanned_files": 500,
      "hit_files": 9,
      "hit_pairs": 17,
      "applied_rows": 17,
      "unused": [],
      "errors": []
    }
  ],
  "local_coverage": "present files checked"
}
```

- ph33: 500 files walked, 9 hit files, 25 hit pairs, 25 rows applied, 0 unused, 0 errors.
- ph35: 500 files walked, 9 hit files, 17 hit pairs, 17 rows applied, 0 unused, 0 errors.
- Local coverage: present files checked. All four owner-local rows were applied against the real bytes: their digests and counts, measured at ee415d0, still hold.
- Source pins and downstream pins (ph33's PH32_SHA; ph36b's full pin and ph38's prefix for ph35) PASS. src/ph32.py, src/ph33.py, src/ph35.py, src/ph36b.py, src/ph38.py are byte-identical to origin/main ec6d442.

## Tests on Windows

python -W ignore::ResourceWarning -m unittest discover -s tests -v: 11 tests, OK (after the fix). The suite did not catch the separator defect because its fixtures build paths the same way on both platforms; a case that feeds an OS-native ph35 path through the coverage step is worth adding.

## P5

notes/recommendations/seed_scan_pairs.py re-run on this tree after writing this report: both checkers still hit the same 9 files; config/, tools/, tests/, the cloud report and this report are not hits. No seed digit appears in the manifest, the verifier, the tests, the cloud report or this report; seeds are named by alias throughout.

## Legacy demos

Not run here. Per decision (B) the recorded ph33.py demo and ph35.py demo stop at their own seed-scan assertion at HEAD; that stop is the approved consequence, not a failure of this verification, and is not reported as a pass.

Verifier sha256 (a-p), this commit: emfhapidcjidpgaofpbkefkbbkhdihknflepbhakdhkfceganepjhpiaobhiccac
Manifest sha256 (a-p): gkkeiinehcdkdajmgdhpcagkffdhjojkglbljnmefphakmogknnljmloeaacligg
