# H18 Stage A amendment: the I7 known-answer expectation for `none` on F1, corrected before any ring reading

Date 2026-09-29. Decision: decision:h18-i7-expectation-corrected. The owner chose option (a) of experiments/h18/h18_diagnosis.md section 6 (AskUserQuestion, 2026-09-29: '(a) 기대값 오기로 기록하고 판독 진행', gloss 'record the expectation as mis-stated and proceed with the readings'). Registered before the readings pass runs; the stopped state is committed at 5ab9eea (record:h18-stage-a-i7-stop).

## What was wrong, and whose error it is

Design v2 section 7, identity I7 (from the reviewer's amendment 5, notes/reviews/2026-09-29-h18-design-v1-review.md), expected the `none` arm to read F1 MET. F1 reads MET only if the unrecovered share is at least 0.70 AND at least 2 x the recovered share. On `none` every event window of either kind holds a cue-off step with an error over 45 degrees (unrecovered 1.0000 of n 193, recovered 1.0000 of n 244; ph37_diag.txt line 329), so the relative clause cannot be met by construction. The expectation was mis-stated by the reviewer (the Fable session). The harness, the arrays, the (A) reading (which reproduces the K5 record's 66.15 percent and 79.7 degrees) and F1's definition are not at fault.

## What changes

- I7's expectation for `none` on F1 is restated as: the absolute clause (unrecovered share >= 0.70) MET; the relative clause reported and marked SATURATED (both shares 1.0000), not read. `integrate` unchanged: e identically 0, every e-reading UNREADABLE as already printed.
- src/ph37.py: only the I7 check's expected value for `none` on F1 changes, so that the run proceeds past I7; the change is disclosed in the output header with the new script sha256 and the old one (284fede4cffed8a8f97192e45a68a6a3cdef285104eaabf8c73f8d372a5fc815). The readings pass then reads the stored arrays (sha256 as listed in ph37_diag.txt lines 299-305) unchanged.

## What does not change

No threshold, no definition of any reading (A)-(E) or F row, no candidate, no arm, no seed, no array. F1's definition stays as registered for the ring arms; its relative clause is read there as written. The stopped output ph37_diag.txt (sha256 ce5e1bc0...) stays on record; the readings pass writes its own output file beside it rather than overwriting it.
