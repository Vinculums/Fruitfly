# Review of the module consolidation design v1 DRAFT (2026-09-29)

Reviewer: the reviewing session (Fable). Draft: notes/module/2026-09-29-module-consolidation-design-v1.md, sha256 9ee44834b436395b097a31e7814c874fc681d55bd080d88850877bfefcb161d2, 399 lines, by an Opus 5.5 agent on the owner's '권고안으로 진행, Q1~Q4 큐 등록하고 모듈 통합 열자' (decision:module-consolidation-open-design). Nothing was run except sed, grep and sha256sum. This is a review, not a decision; the owner confirms by the draft's section 10.

## Verified against the code (HEAD 4b8a4c0)

- **U7, where learning is credited.** src/ph15.py:55-61 `inputs(codes, good, at)`: the code and the reinforcement vector are both built from `at`, the source the row stands at, not from the held odour. The outlook note (notes/module_boundary_outlook.md:29, 'credited to what is held at that moment') does not describe the code; the consolidated record's learning-loop line ('updated once per world step from its own position') does. The outlook is an OUTLOOK, not a decision, so nothing adopted is affected; its wording is stale.
- **U8, the sparse code size.** The agent's learning module is built with K 200 (src/ph11.py:53, MB); K 500 is Phase 4's and Phase 7.2's module-level constant (src/ph8.py:37); ph8.py:242 already carries the K 200, C 2 variant. The outlook's 'K 500' is the module-level figure, not the agent's.
- **U10, the H28 tie rule at two channels.** src/ph33.py:154-157: `top` is every present channel at the top non-negative value; `ranked` applies when `nT >= 2`. At two channels with EQUAL non-negative values (0/0, +1/+1) both channels are `top`, so the rule acts. master_plan's 'at two channels the rule is inert by code' (lines 857, 1773) holds for the value pairs H28's identities tested (+1/0 and +1/-1) and for the adopted +1/0 scope, not for any pair. The wording is a candidate correction: 'inert at two channels for the tested value pairs (+1/0, +1/-1)'. The draft's choice to build the two-channel form under an explicit `nch == 2` branch rather than through Act16 follows.
- **Seed digits in notes.** src/ph35.py:234 skips a `.md` file only when its directory's basename is `notes`; a file under notes/module/ is scanned for ph35's own seed values. The draft cites seeds by constant name and report line and carries no digits; correct, and worth a standing note (below).
- The import chain and the class trees are as read (ph35 -> ph34b -> ph30 -> ph28 -> ... -> ph2; Agent16 through ph33 -> ph32 -> ph30); Agent9's step (ph23.py:60-104) wrapped by ReleaseN2 (ph30.py:121-136) for Agent17, Act16's (ph33.py:119-177) for Agent16.

## Amendments recommended for v2 (small)

1. **Record the three readings as bookkeeping for the owner, not as changes.** U7 and U8: an addendum line to the outlook note (its text unchanged), and the module header. U10: a wording correction in master_plan at lines 857 and 1773, by the owner's decision at v2, since it touches recorded text; no verdict, scope or adoption changes.
2. **A7 (learning on) needs a recorded reference or must be labelled coverage-only.** The draft runs Agent17 with learning on in the H20 Stage C Run 2 E1-C harness, which Agent17 never ran in; it reproduces no recorded number. Keep it, labelled 'coverage, no recorded reference', and add the recorded learning-on run that exists for the lineage (Agent14N2 in H20 Stage C Run 2, ph31 evaluation seeds) as the recorded reference row, comparing the module against Agent14N2's class tree there.
3. **The hash layer.** State that the per-step hash covers every attribute of the agent object and its generator state, listed by name in the output header, so a later reader can see what 'all agent state' was.
4. **Seed digits.** Add to section 8 that no design or report under notes/ or experiments/module/ may carry the digits of any registered seed of ph33 or ph35, because their seed scans read those folders; seeds are named by constant and report line, as the draft does. Propose it as a standing note for the owner (P5) in the same form as P1-P4.

## Not changed

One file src/fly.py, the interface, the forms switch by `nch`, the acceptance rows, the three comparison layers at zero tolerance, seeds reused by name, G 2 carried and flagged, the file names. If the owner confirms section 10 as recommended with amendments 1-4, v2 FINAL differs from v1 only in those points and the status and confirmation text.
