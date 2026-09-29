# Review of H18 Stage B (branch B-iii) design v1 DRAFT (2026-09-29)

Reviewer: the Fable session. Draft: experiments/h18/h18_stage_b_design_v1.md, sha256 43cf6da30ffd791e362c16ebc278a37dbceb31289528f41dbc117bd6c1eca16d, by an Opus 5.5 agent on the owner's 'B-iii 설계 열자, v1 초안은 opus 에이전트로' (decision:h18-stage-b-iii-open-design). Nothing was run except sed, grep and sha256sum. The owner's confirmation ('권고안대로 확정, v2는 opus 에이전트로 쓰고 Stage B 진행') arrived before the draft did, under the standing instruction to follow the recommended options; this review was applied before v2 was written, and the amendments below are folded into v2 as part of that confirmation.

## Verified

- Code lines cited: ph11.py:59 (`p_wind=1.0`) and :86 (`wind_on` draws against p_wind) hold, so no cue return occurs in any adopted world; ph12.py:64 (`always` returns all True); ph12.py:79-80 (the docstring separating `clock` from `since`) and :91-94 (the wall rule restarting the clock without a whiff); ph12.py:115-116 (since and clock zeroed on a whiff, incremented otherwise); ph23.py:95-98 (the adopted cast is its own implementation on `since`, not ph12's Nav2). (I-a) is therefore by code on two independent grounds, as the draft says.
- The (1a) arithmetic: mean cos over 0 to 120 degrees = sin(120)/2.094 = 0.4135; over the full 0-170-0 loop = sin(170)/2.967 = 0.0585; drifts 24.8 per 100 steps against 9.9 per 283 steps. Correct. The rejection reason is the right one: in an open plane an agent pushed upwind past the source leaves the plume region for good.
- The swing arithmetic (5.3, 8.9, 8.8 units over the first three 30-step half-periods) is straight-path and labelled inferred.
- The Stage A numbers quoted (5.485/2.390/1.221/0.779 at cue-on steps 1/2/3/5; 0.7702 outside the odour; 97 of 161 and 89 of 162; residual sd 2.58; F-v 1.4433) match ph37_read.txt.
- Seeds 18101-18106 and 18201-18203: `git grep -nwE` 0 hits each (checked again here on the tracked files). The graph scan is PENDING (key), stated, not claimed.
- Wording: the draft says B-iii does not repair the memory, that Stage B's test does not rest on the F3 margin, that no counterfactual predicts d, and that the bench stop rule is the likely end. No 'structurally impossible', no 'for any', no figure carried between conditions.

## Amendments for v2 (small; no bar, seed, arm or rule changes)

1. **State the rule at code level (3.2).** `armed` is False at construction (an agent with no whiff yet cannot fire; consistent with Stage A's C3, events with no prior whiff excluded); the clock reset happens after ph12.py:116's increment on the same step, so the target of the firing step is computed with clock 0 (offset 0, side = cast_sign); `cast_sign` is not touched; `since` is not touched.
2. **(I-c) wording.** 'Equals `ring` bitwise before each agent's first firing' is right because the rule draws no random number and the ring's noise stays on the agent generator; after the first firing the two arms consume the same draws on different states. Say so, so a reader does not expect pairing of positions after the first firing.
3. **`restart_rand` (3.2).** State that p is one number, frozen on the bench and written into the development and evaluation runs' headers, and that its per-step draws come from SeedSequence(agent).spawn(1) child 0 so `ring`, `restart` and `exact_restart` keep identical agent-generator sequences.
4. **M2 and M5 statistic.** Name the per-agent quantity: late unrecovered is `absorbed`'s per-agent flag (no whiff in the last three blocks, ph12.py:164); the paired difference is the mean over the 200 agents of (flag_ring - flag_restart), bootstrap over agents.
5. **Execution (9).** Add H18 v2's amendment 1 verbatim: one arm per process, float32/int8 arrays to disk, readings in a separate pass; numpy 2.4.6; and that the bench's stop decision is printed and committed before any development seed is used.

## Not changed

The lever (1b) and its fixed parameter, the rejected candidates, the arms, the bars (M2 and M5 lower bound > 0, M3 > -1.0, M4 wording), the stop rules, the seeds, the scope statement. If the owner's confirmation stands with these amendments, v2 FINAL differs from v1 only in the status and confirmation text, section 12 and the five points above.
