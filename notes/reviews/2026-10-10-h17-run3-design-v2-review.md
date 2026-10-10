# H17 Run 3 v2 candidate-design review

Date: 2026-10-10. Verdict: CLEAR as a reviewed DRAFT only.
Owner instruction: "권고안에 따라 작업 이어 진행".
Design: experiments/h17/h17_run3_design_v2.md; canonical d73d7de44ea288ca0.
Design SHA256(a-p): nddceljahjnfddednpihcigbiooacjgloacoebmfcnabnnjjfoaepambjjgoknjf.
Anchor audit: experiments/h17/h17_run3_anchor_audit.json; canonical da13f38d62551dccd.
Anchor SHA256(a-p): jackbmmkbgpbikomfcagiomanioebhbpbddigbpoipcmgcnnabgngbonlfkibfhi.

## Scope and independent readings

The reviewing root read saved R0 AP arrays, validated their byte hash, and
recomputed marker/entry summaries and ideal command geometry without executing
Fly, creating RNGs or producing new trajectories. Current R0 closure remains
immutable: 96 files verified. C0 entry400/400 at t249/q250 is a constructed
position-only stress; T3's sixteen marker rows remain conditionally UNREADABLE.
The majority requirement, paired added-success clause and regression margins
are new normative DRAFT choices, not measured candidate effects or forecasts.

A delegated source/tick audit confirmed once-only complete Fly.act including N2,
then active target/last_turn override, rounded returned-turn residual reuse,
original move/bump, no extra RNG draw, q-only derived phase and no privileged
geometry/state reads. A separate denominator/state audit distinguished an
entry-reset u, which would require a second relaxation, from the selected
q-derived phase, which continues through holds. The latter is explicit.

## Adversarial review and applied corrections

The final read-only adversarial reviewer cleared the saved proposal after:
1. Qualifying guaranteed slant coverage: a phase cycle spans both slants,
   but execution of both is not guaranteed in an interrupted observed K300 window.
2. Freezing strict conditional windows to first-entry ROWS only. Later entries
   are repeated-event/distinct-row diagnostics, never independent sample additions.
3. Making the slant guarantee wording logically precise; an interruption does
   not imply both slants are impossible, only that coverage is not guaranteed.

Final clearance found no blocker in q-only phase/delayed entry, original
source/authority boundaries, current PRE_POS anchor, residual operation order,
motor/move/bump semantics, all400 efficacy/regression denominators, matched
bootstrap index sharing, Wilson threshold220/400, interval verdict inequalities,
stage stops or absence of candidate efficacy/power forecasts.

## What this review establishes

This clears a design proposal, not a controller or efficacy result. No unit test,
trajectory, RNG or bootstrap ran in this design session. Deterministic anchor/
geometry/Wilson arithmetic is separately saved. New-document protected-token
checks, original R2 source/manifest verification, historical evidence hashes
and canonical/master readbacks are recorded in the final design_checks receipt.

GS250 is proposed, not confirmed. Renewed q relaxation remains DRAFT unsigned;
old H17 signatures remain lapsed. FINAL, seed registration, implementation,
H0, bench/development/evaluation and adoption are unopened. Historical H17,
hold dispositions and Q1-Q4 order are unchanged.
