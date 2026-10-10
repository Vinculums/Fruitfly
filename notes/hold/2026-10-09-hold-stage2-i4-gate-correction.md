# Stage-two I4 gate correction, reviewed before any bench

Date: 2026-10-09. Operational gate correction, reviewed by the root session.

The first full identity run stopped at I4/A2. Its receipt is preserved at
`experiments/hold/hold_stage2/hold_stage2_identity.json`: passed false, complete
false. All ten trajectory fields were byte-identical; I2/A2 and the per-step
generator audit passed. No bench, development, or evaluation seed was used.

The failed check required equality of `module_identity.l3_scores`'s entire W1
summary. `ph25.w1sum` calls `ph22.summary`; that summary combines trajectory
scores with actual-hold/release diagnostics. Requiring those diagnostics to
match contradicts the registered I4 allowance for H/SIL/TO/EV differences.

The corrected I4 compares dwell, first, contacts and cls3 unchanged, and every
W1 summary key except this exact list: heldB, nothing, formed, released, end_to,
end_ev, end_both, end_none, fh, heldB_end. Excluded keys and their differing-row
counts are reported separately. Every remaining W1 key uses zero tolerance.
I1, I2, I3 and I6 keep their full historical score/field comparisons. The core
ReadOutFly intervention, seeds, conditions, criteria and stop rules are unchanged.

A constructed W1 fixture tests that differing hold diagnostics do not fail I4
while its trajectory scores match. A score mismatch still fails equality. A
fresh smoke run precedes the full identity rerun in
`experiments/hold/hold_stage2_corrected`; the failed receipt is retained.
