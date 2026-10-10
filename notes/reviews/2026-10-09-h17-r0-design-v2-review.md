# H17 R0 v2 FINAL design and seed reservation review

Date: 2026-10-09. Verdict: **PASS for design completeness; execution not opened**.
Owner instruction: "구체화 진행". Independent reviewer: hold_review (read only).
Reviewed: experiments/h17/h17_r0_design_v2.md, config/h17-r0-seeds.json,
experiments/h17/h17_r0_seed_registration.json and their cited source.

The current Fly two-channel/N2 reference remains unchanged. R0 is a passive
description of four matched condition constructions, not an efficacy or
adoption test. The predecessor Run3 draft and historical closures are preserved.

## Corrections completed before registration

- Fixed code streams are module-level src/fly.py CODE_SEEDS, not a Fly class
  attribute.
- The durable measurement registry key is only the pair digest. Design ID is
  immutable metadata; changing output path or design ID cannot bypass a claim.
- W1's primary is fixed to last-200 lost rows /400; its complementary
  non-valued whiff incidence and physical dwell remain separate readings.
- q starts at zero and the earliest continuous-no-whiff marker is t=249.
  Strict post-marker windows exclude marker-step AT2, reported separately.
- Negative-to-unheld is split into no unit above threshold and multiple units;
  identity switching is separately counted. Concurrent reset flags are not causes.
- N2 reconstruction uses pre-hold sign, any above-threshold post unit, and the
  intermediate SIL_base, retaining all three silence phases.
- C0 changes position only, with a separate independent geometry stream and
  50/50 outer sides within every World7 cell. It does not call old construct.
- World7 still consumes wind uniforms at probability one, and W1 preserves
  both original source draws before applying its mask.

## Independent review evidence

All 30 source/evidence appendix digests and both config/reservation digests
match actual bytes. Source reading confirmed complete constructor/draw/tick
order, original move/bump and strict distance<3 reach. Mandatory storage,
same-class full identity, frozen lineage projection and independent verifier
requirements are consistent. Conditional windows use full-followup eligibility
and distinguish censored rows, undefined zero denominators and UNREADABLE
small populations. First simultaneous events retain both source bits.

Execution schema, implementation dependency pins and public spent-input H0
must be fixed and reviewed after implementation but before reserved generators.
This is an explicit implementation gate, not a permission to weaken FINAL
after viewing measurement. No remaining concrete design inconsistency found.

Root additionally checked protected tokens, exact UTF8 owner quote, current
source/downstream pins, unchanged R2 manifest and all appendix digests.
Fresh seed local scan checked all 589 repository files before declaration:
no hits/errors; prior hold roles disjoint. Five individual graph seed queries
completed with both search arms and no keyword/literal hit. A later episode
search had an encoder-build mismatch; full-text and exact-node reads were
used for registration identity, with both new IDs absent before creation.
No complete semantic search claim is made for that later query.

Previous full R2 scan remains the baseline receipt in
experiments/hold/hold_followup_h17_design_checks.json. This turn checks newly
written/changed text for protected literals and revalidates unchanged pins
and manifest; it does not claim a repeated full R2 sweep.

Reviewers edited no files and ran no trajectories or RNG. Root wrote the
design/config/receipt and applied corrections. This PASS means a reviewable
measurement contract; it is not a measured R0 outcome, execution opening,
new counter relaxation, controller change or candidate selection.
