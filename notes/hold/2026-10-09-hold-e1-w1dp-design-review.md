# Hold E1 W1Dp: design review

Date: 2026-10-09. Scope: design v1 DRAFT, not execution approval.
Reviewed document: notes/hold/2026-10-09-hold-e1-w1dp-design-v1.md.
Review performed by /root/hold_review; corrections applied and checked by root.

The read-only review found no mathematical or scope blocker. It checked the
exact B-plume law, strict cone boundaries, the near-source exception behind
the source, and the independent D draw at every sensing step, including
zero-probability steps. Actual H alone advances; passive R projections do
not affect motion or agent state.

The draft preserves H0's complete known answer, the B4/B5 identity and
passivity gates, and the complete historical W1 L3 summary. The stage-two
I4 exclusions do not apply. X1-X4 retain their original thresholds and
denominators. X3 counts all differing clipped commands; tied-burst route
attribution is reported separately. Original-source-only loss excludes D.

The review requested four concrete corrections, all included in the final
draft bytes:

1. State rngD construction explicitly between the unmasked twin and values/
   agent construction, as in ph33.run.
2. Define f_id as count(T1&T2&T3&T4&T5) / count(T1&T2&T3&T4), with null for
   an empty denominator.
3. Anchor cast_draw at src/ph16.py:35, PassiveFly.act at
   src/hold_stage1_instrument.py:18, and the pair gate at
   tools/replay_hold_stage1.py:162.
4. Include the promised source-byte provenance appendix. Root checked all
   twelve recorded hashes against the current files.

The cited D0 figures agree with the saved report. D0 remains UNRESOLVED;
the existing coverage stop decisions remain unchanged. No outcome for E1
is inferred. A fresh pair belongs to the future execution FINAL, with a
durable pair-keyed claim before any fresh generator construction and no
automatic repeat. The present owner instruction opens design work only.

Root validation: source appendix matches; R2 reference and downstream source
pins and manifest pin pass; protected-number scan of both new notes passes;
diff whitespace check passes. These are document/provenance checks. No new
seed was selected, runner implemented, or simulation performed for this work.

Verdict: v1 DRAFT is ready for the execution-FINAL gate. This is not a benefit
finding or approval to run. Registration receipts and current file hashes are
stored in experiments/hold/hold_e1_design_checks.json.
