# Review of the consolidation gate v1 DRAFT (2026-09-29)

Reviewer: the reviewing Claude session. Draft: notes/consolidation/2026-09-29-consolidation-v1.md, sha256 26dc2b9d2a87357e5798d51021e4cd3f62e8b781f058dbadd492ee9e7a264dd2, 417 lines, by an Opus 5.5 agent on the owner's '정리 게이트 열자, 초안은 opus 에이전트로' (decision:consolidation-gate-open). Nothing was run for this review except sed, grep and sha256sum. This is a review, not a decision; the owner confirms by the draft's section 9.

## Verified

- **The G 2 ambiguity (the draft's weak point 1) is real.** master_plan.md:2043 says the gain was 'Tested in H20 Stage A, NOT adopted'. master_plan.md:140-141 records that H20 Stage A was evaluated once with G 2 'fixed post hoc by a separate execution decision of the owner, decision:h20-stage-a-run-g2, explicitly not a bench pass'. Every later adopted scope carries 'G 2' (for example master_plan.md:602, :1212), and no decision in master_plan adopts the gain. The draft does not resolve this and should not: it is the owner's question. Recommended wording for section 9: the owner states whether G 2 is adopted state (and by which decision) or a composition carried by every later design.
- **Grouping-dependent counts (weak point 2).** The draft's own table recount matches its totals; the classification choices are stated. Keep the table and the counts, and add one sentence that the totals change if counted one row per hypothesis.
- **Module build sites (weak point 3).** master_plan cites build lines only for later modules; the draft keeps the plan's labels and does not invent lines. Correct.
- **Stale bookkeeping.** master_plan's 'main is behind codex/h12-review-plan' is out of date: main was fast-forwarded to 2817eb6 today. The outlook note's acceptance target (ph21.Agent8) predates Agent17 and Agent16. Both are rightly listed under section 9 point 8.

## Correction

- **record:run-file-hash-discrepancy is graph-only, not absent.** It is a Vinc graph record (the four `*_run.py` files whose recorded sha256 does not match the document bodies, although the bodies reproduce every recorded number), written before the repository existed as a clone. The draft's section 6 line 323 should read 'graph-only record (not in the repository); readable once the Vinc key works' instead of 'not in the record'.

## On the proposals

- P1 (known-answer saturation) and P2 (a loop's anchor) are the two lessons of today's H18 work and are worded narrowly enough to be checkable. Recommended: adopt both.
- P3 (recompute headline readings when execution is delegated) and P4 (local execution only) write down current practice and an owner instruction (memory of 2026-09-27: 'actions에서 하면 안되고 여기 에이전트 실행해야함'). Recommended: adopt both.
- Section 8's order (c) Level 6 synthesis, (b) module consolidation, (d) the hold's benefit, (a) H17 Run 3 is argued from the record. One note for the owner: (c) and (b) have no hypothesis and no run of the kind the gates were built for, so each still needs its own spec before work starts.
