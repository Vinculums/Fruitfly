# (d) The hold's benefit, stage one: passive replay report (2026-10-07)

Status: measurement only, under `decision:hold-benefit-stage1-open` (read at revision five). Every passivity and
coupling gate passed in all nine strata. In the six primary strata (A1-A4 two-channel, B1-B2 three-channel) the read
identity differed from the actual hold in a large share of row-steps and no command differed in any row-step. In the
three coverage strata (A5, A6, B3) commands did differ. No benefit verdict; no stage two; no world, threshold, value or
window change; the owner chooses among the gates of the decision.

## What was run

- Code: PR #3 at 22d84b600afe5c545aa030860f285093851ddedd (`src/hold_stage1_instrument.py` sha256
  41e019b98fc48928f3e729411f6f02d1baae2e3741930394be6380619189ea6a; `tools/replay_hold_stage1.py` sha256
  cad8559cf1e0e3faaaeec9d4ec3890171e30423c1012513d5e18784a552215d6); reference `src/fly.py` sha256
  3b360b2901678cbc313cca8874352fc706d80eb54f6dea5868ca11f419d1efc4 and `src/module_identity.py` sha256
  14558ac0f5b61a4a71972ccd1a4612385e2016cb6a75cee34c2fac57b103d6b5, both byte-pinned by the runner and unchanged.
  Design: `notes/hold/2026-10-07-hold-benefit-stage1-design-v1.md` rev 2 (sha256
  d5cc2e62472c333f1a27f28537639e546f32d79b230f3997598a9fd01d18f1fd).
- Where and how: the owner's local session (Windows, uv, Python 3.13.12, numpy 2.5.3, OPENBLAS/OMP/MKL threads 1,
  PH30/PH32/PH33_PROCS 1, one process), run once by an Opus 5.5 agent, exit 0, wall time 397.5 s. The runner refused
  to start until the R2 verifier's source pins and manifest checked out, and refused to write a report whose bytes
  carried a ph33 or ph35 seed digit string. Output: `experiments/hold/hold_stage1_replay.json` (sha256
  4c43fde653e63048302cab5fe72d8d1a85911cfbf54584367fc09be0ab407d94, LF, 3 387 586 bytes). The reviewing session read
  the gates and counts from that file independently (`eval_hold.py`, a reader only); the numbers below are from it.
- Strata: the identity report's rows, exact worlds, values, windows, 400 rows x 600 steps, seeds by alias (A rows
  `ph35.SEEDS['eval']`, B rows `ph33.SEEDS['eval']`), reused on purpose for a diagnosis of those rows and read for no
  criterion. Learning off. A7/A7r and the three-channel learning path were not run (outside this stage).
- Intervention, per the decision: R reads `q = argmax(y)` when `max(y) > 0.05`, else nothing, from the same step's
  gated `y` after the gain (the H27/H28 R4 read-out); H reads the actual post-circuit hold. Only the read-out
  expressions (`val`, `hit`, `vh`, presence override, top/eligible, `keep`, `nav`, `since`, `silence`, `flee`, `tgt`,
  clipped turn, post-wrapper silence) are projected for both; the circuit, gate, evidence release, N2 wrapper and the
  returned hold stay actual; nothing R is written back. The passive subclass reconstructs `y` from the already updated
  upstream state without a second `step` and adds no random draw.

## Passivity and coupling gates (all nine strata)

| Gate | Result in every stratum |
|---|---|
| L1 recorded behaviour fields equal, instrumented vs uninstrumented `fly.Fly` | 16/16 (A rows), 17/17 (B rows) |
| L2 per-step attribute hashes equal | 1200 events, 91 200 hashes (A) / 97 200 (B); no attribute only on one side; only `hr` and `hold_projection` excluded |
| L3 scores equal | 4-6 of 4-6 per row, as the identity report |
| Construction draws and generator states equal | yes |
| Per-step inputs (whiffs, wind, heading, rotation) and returned (turn, hold) digests equal | yes |
| H projection equal to the actual identity, presence, nav, since, post-wrapper silence, target and clipped turn | yes, no first error |
| Complete sample (600 steps x 400 rows of masks) | yes |
| Recorded `HR` equals the instrument's `hr` where it differs from `H` (three-channel harness only) | yes (B1, B2, B3) |

So the instrumented reference advanced exactly as the uninstrumented one, and the H projection reproduces what the
agent actually did; the R projection is a local counterfactual on H's state, step by step.

## Counts, over all 400 rows and 600 steps (denominator 240 000 row-steps)

"Command" is a different clipped turn before the common noise draw. "Latent silence" is a different next-step silence
counter with the same current command (amendment one: in a freely evolving R arm this would alter the circuit one step
later; here only H advances). Rows exposed are rows with at least one such row-step.

| Stratum | Condition | h != q | presence set differs | nav differs | flee differs | target differs | command differs (rows exposed) | latent silence differs (rows) | command, release-adjacent (of adjacent row-steps) | command, at a wall (of wall row-steps) |
|---|---|---|---|---|---|---|---|---|---|---|
| A1 primary | T1 +1/0 | 63 764 | 0 | 0 | 0 | 0 | 0 (0/400) | 2 839 (400) | 0 (22 420) | 0 (0) |
| A2 primary | W1 +1/0 | 48 675 | 0 | 0 | 0 | 0 | 0 (0/400) | 3 036 (396) | 0 (19 600) | 0 (0) |
| A3 primary | T3a +1/0 | 50 312 | 0 | 0 | 0 | 0 | 0 (0/400) | 1 905 (326) | 0 (21 003) | 0 (0) |
| A4 primary | T3b t0 150 +1/0 | 56 847 | 0 | 0 | 0 | 0 | 0 (0/400) | 2 851 (400) | 0 (20 634) | 0 (0) |
| B1 primary | T1D +1/0/0 | 110 782 | 0 | 0 | 0 | 0 | 0 (0/400) | 7 177 (400) | 0 (24 322) | 0 (1 566) |
| B2 primary | W1D +1/0/0 | 106 743 | 0 | 0 | 0 | 0 | 0 (0/400) | 7 136 (400) | 0 (20 454) | 0 (17 344) |
| A5 coverage | T1 +1/-1 | 86 379 | 9 555 | 1 393 | 43 504 | 43 469 | 43 352 (331/400) | 2 864 (400) | 5 027 (22 235) | 146 (146) |
| A6 coverage | T1 0/0 | 61 002 | 0 | 64 | 0 | 64 | 64 (33/400) | 3 873 (400) | 64 (20 717) | 0 (0) |
| B3 coverage | T1D +1/-1/0 | 110 096 | 0 | 1 423 | 10 473 | 10 465 | 10 319 (355/400) | 7 054 (400) | 2 838 (23 413) | 3 (9 351) |

Other read-out expressions in the primary strata: `val` differed in A1 52 407, A3 18 800, A4 17 723, B1 44 885 and in
no row-step of the two W1 rows (A2, B2), `vh` in 24 244 to 57 528, `keep` in 42 591
to 58 359 row-steps; `top` and `eligible` never differed (they depend on identity only through the presence set).
First differing expression after the identity itself, primary strata: `val`, `hit`, `vh` or the presence override;
never `nav`. Row-steps with no read-out difference at all: 176 236 (A1), 191 325 (A2), 189 688 (A3), 183 153 (A4),
129 218 (B1), 133 257 (B2) of 240 000.

Coverage strata, first command step per row: A5 from step 0 to 530 (331 rows, up to 574 differing steps in one row);
A6 from step 8 to 417 (33 rows, at most 4 per row); B3 from step 0 to 542 (355 rows, up to 166 per row). In A5 and B3
the first downstream difference is `val` (the negative held value), in A6 `hit` or the presence override.

Constructed witnesses: not run; every count above is a naturally reached snapshot.

## Reading, within the decision's gate table

1. **Primary strata, two-channel +1/0 (A1-A4): no command branch was reached, and by code reading none is open while
   the presence sets agree.** With values +1/0 the top set is the valued channel whenever it is present, else the
   other channel if present, else empty; `nav` is then the whiff of that top channel whatever identity is read (held
   valued: `keep` and its own whiff; held zero-valued while the valued is present: not kept, the valued channel's
   whiff; nothing held or R reading nothing: the top channel's whiff). `since`, `tgt` and the turn follow `nav`, and a
   negative `val` cannot occur at +1/0. What remains is a different presence set through the read identity's
   override, by one of two routes: the actual hold on a channel whose counter has passed the window (200) while the
   hold survives (the hold times out at silence > 40 and both counters reset on the same whiff of the held channel,
   so the gap at hold formation would have to exceed 160 steps), or R reading a channel absent for 200 steps whose
   upstream output still exceeds 0.05 (the stage decays with tau 2.0, so from saturation the output falls below 0.05
   within about a dozen steps). The presence set never differed in 960 000 primary two-channel row-steps. This is a
   reading of `fly.py` lines 311-337 for the two-channel +1/0, learning-off form only; it says nothing about other
   values, learning, or the three-channel form, and it has not been checked by constructed witnesses.
2. **Primary strata, three-channel +1/0/0 (B1, B2): a branch exists in code but was not reached.** `nav` can differ
   only when the valued channel is absent, the two zero-valued channels are both present and both burst-ranked (tied
   bursts), exactly one of them whiffs, and H and R read different identities (one possibly nothing); with a single
   ranked channel or none, `nav` is identity-independent. In 480 000 row-steps of T1D and
   W1D this did not occur; latent silence differences did (7 177 and 7 136 row-steps). Zero here means none in this
   fixed sample, not impossibility.
3. **Coverage strata (A5, A6, B3), reported apart: the comparison can branch and does.** A5 and B3 branch through the
   negative-value route (H flees from a held negative channel while R, reading nothing or the valued channel, surges
   or casts), A6 through the tied-top route (equal values 0/0, 64 row-steps on 33 rows). These conditions are not in
   the adopted scope (supplied negative value; equal values) and this stage registers no benefit measure for them.
4. **What follows from amendment one:** in every stratum the R read-out changes the next-step silence counter in
   1 905 to 7 177 row-steps, so a freely evolving hold-not-read arm would reset its circuit at different steps even
   where the current commands agree. That is a latent-state difference, not a measured action effect, and it is why
   the historical H27/H28 R4 arm is not the same thing as this passive projection.

Permitted conclusions, per the decision: for A1-A4, "no branch within the audited conditions" (structurally
uninformative there, by the reading in point 1, which the owner may ask to have checked by constructed witnesses);
for B1, B2, "branch exists but no exposure in the fixed sample"; for A5, A6, B3, "branch exists and is reached,
passivity and coupling verified", in conditions outside the adopted scope. No zero-benefit claim is made; a different
`nav` or target in A5/A6/B3 is not evidence that either action is better.

## Not claimed, not done

No benefit or cost was scored. No free-running R trajectory, fixed-input replay, learning stratum, new seed, repeat,
world, threshold, value or window change. No change to `fly.py`, the ph chain, the seed checkers, the R2 manifest or
pins. The timing (397.5 s for eighteen 400 x 600 runs) is reported, not compared.

## The owner's choices (decision:hold-benefit-stage1-open, gates)

- For the adopted-scope conditions (A1-A4, B1, B2): commission a world-change or condition-change design that exposes a
  documented branch (for the two-channel form this means a value or presence condition, not a world geometry; for the
  three-channel form a condition in which the valued channel is absent while two tied zero-valued channels burst), or
  defer (d).
- Whether a stage-two benefit design may be proposed on the coverage conditions (negative supplied value; equal
  values), which lie outside the adopted scope and would need their own identity rows and preregistered measures.
- Whether constructed witnesses should be run to check the two-channel reading in point 1 before any of the above.
