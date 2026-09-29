# Module consolidation: identity report

Date 2026-09-29. Design v2 FINAL, notes/module/2026-09-29-module-consolidation-design-v2.md, confirmed by the owner
2026-09-29 ('확정', gloss 'confirmed'): decision:module-consolidation-open; registered at 30dec50 (HEAD). Code and run by
an Opus 5.5 agent in the local session (P4). **This is a report of an engineering check with no hypothesis. It is not a
decision and adopts nothing;** the reviewing session recounts it (P3) and the owner decides what is recorded.

## 1. What was asked

Fold the adopted agents into one numpy-only file, src/fly.py (Agent17 at two channels, Agent16 at three, selected by
nch), and accept it only if it is the adopted class trees bitwise: rows S0, A1-A7, A7r, B1-B3 of design section 6, three
layers (L1 the harness's recorded fields, L2 a per-step hash of every agent attribute and the generator state after
every act and every bump, L3 the per-row scores), zero tolerance, seeds by named constant. No existing file changes.

## 2. Environment

| Item | Value |
|---|---|
| Python | 3.11.15 (main, Mar 24 2026, MSC v.1944 64 bit), through uv `--python 3.11.15` (a bare `--python 3.11` gave 3.11.9; the exact recorded version was available) |
| numpy | 2.4.6 (`uv run --no-project --with numpy==2.4.6`) |
| Platform | Windows-10-10.0.19045-SP0 |
| Threads | OPENBLAS, OMP, MKL 1; PH30_PROCS=1, PH33_PROCS=1 (PH32_PROCS=1 for the demos); one process at a time |
| Invocation | from the repository root, `python src/module_identity.py <row>`; S0 in one process, then each row in its own process |
| Files | src/fly.py sha256 3b360b2901678cbc313cca8874352fc706d80eb54f6dea5868ca11f419d1efc4 (350 lines); src/module_identity.py sha256 14558ac0f5b61a4a71972ccd1a4612385e2016cb6a75cee34c2fac57b103d6b5 (315 lines); both unchanged across all 22 recorded row headers |
| Outputs | experiments/module/identity.txt (22 row blocks, each with its own header: versions, thread pins, both sha256, the sha256 of every imported source file, fixes, the L2 attribute lists); experiments/module/identity.json (per row and layer, the L2 per-event digests and per-attribute chain digests in a digit-free alphabet) |

## 3. Identity per row and layer

Arms: reference = the adopted class tree built by the existing hooks (ph35.make for Agent17, ph33.build for Agent16,
ph30.build for the Stage C harness); candidate = fly.Fly injected at run time into the same harness (ph24.make,
ph33.build, ph30.build; no file edited). Byte equality everywhere (stricter than np.array_equal: -0.0 and 0.0 differ).

| Row | Role | Size | L1 fields equal (elements) | L2 events / hashes | L3 scores equal | Result | Time |
|---|---|---|---|---|---|---|---|
| A1 | T1 +1/0, adopted scope | 400 x 600 | 16/16 (4 800 000) | 1200 / 90 000 | 4/4 | IDENTICAL | 51.8 s |
| A2 | W1 +1/0 | 400 x 600 | 16/16 (4 800 000) | 1200 / 90 000 | 5/5 | IDENTICAL | 55.7 s |
| A3 | T3a +1/0 | 400 x 600 | 16/16 (4 800 000) | 1200 / 90 000 | 5/5 | IDENTICAL | 65.4 s |
| A4 | T3b at t0 150 +1/0 | 400 x 600 | 16/16 (4 800 000) | 1200 / 90 000 | 6/6 | IDENTICAL | 67.2 s |
| A5 | T1 +1/-1, coverage | 400 x 600 | 16/16 (4 800 000) | 1200 / 90 000 | 4/4 | IDENTICAL | 71.5 s |
| A6 | T1 0/0, coverage | 400 x 600 | 16/16 (4 800 000) | 1200 / 90 000 | 4/4 | IDENTICAL | 61.6 s |
| A7 | Agent17, Stage C E1-C learning on, coverage, no recorded reference | 400 x 5400 | 16/16 (1 769 040 000) | 10 800 / 810 000 | 38/38 | IDENTICAL | 724.7 s |
| A7r | Agent14N2, Stage C E1-C learning on, recorded reference | 400 x 5400 | 16/16 (1 769 040 000) | 10 800 / 810 000 | 38/38 | IDENTICAL | 674.1 s |
| B1 | Agent16 T1D +1/0/0 | 400 x 600 | 17/17 (5 520 000) | 1200 / 97 200 | 5/5 | IDENTICAL | 73.8 s |
| B2 | Agent16 W1D +1/0/0 | 400 x 600 | 17/17 (5 520 000) | 1200 / 97 200 | 6/6 | IDENTICAL | 63.9 s |
| B3 | Agent16 T1D +1/-1/0, coverage | 400 x 600 | 17/17 (5 520 000) | 1200 / 97 200 | 5/5 | IDENTICAL | 62.3 s |
| S0 | all eleven rows, demo seeds (5, 6) | 40 x 200 (A7, A7r 40 x 600) | all equal | all equal | all equal | IDENTICAL (11/11) | 45 s in all |

Seeds: A rows ph35.SEEDS['eval'] (experiments/h29/h29_report.md:3); B rows ph33.SEEDS['eval']
(experiments/h28/h28_report.md:3); A7 and A7r ph31.SEEDS['eval'][0] (experiments/h20/h20_stage_c_run2_report.md:3).
Reused on purpose, read for no criterion; never printed. The harness's own construction checks (draws_equal,
rng_equal against the unmasked twin world) were True for both arms in every harness row.

- **L1 fields.** A rows: POS, HEAD, S, SG, H, NAV, SINCE, TGT, SIL, TO, EV, W, SUS, Z, AT2, C. B rows: the same plus
  VAL. A7/A7r: the harness's per-step trace (ph30.Sim with trace on: H, S, SG, SIL, SINCE, TURN, W, EST, NAV, TGT, TO,
  EV, C, POS, HEAD, MBW), compared step by step with the two arms in lockstep, nothing stored.
- **L2 attributes.** 75 attributes at two channels, 81 at three, hashed after every act and every bump. They are listed
  by name in every row header of identity.txt, including the generator state of 'rng' and of every sub-object's
  rng/rng3. Some attributes exist in one arm only and are listed there, not hashed. Reference-only attributes are the
  dropped measurement and configuration attributes (17 at two channels, 26 at three: abl, belief, cast, differs,
  differs8, filt, fix, n2S, n2Z, nav6, nav8, prev, release, rot_in, rule, scope, yp; at three channels also acts,
  hold_read, hr, keep15, keep16, nav15, top15, topr, val). The only candidate-only attribute is nch at two channels.
- **L3 scores.** dwell per source, first reach, contacts, dwell-majority class; W1 ph25.w1sum / ph32.w1sum; T3a
  ph24.t3_dwell over 100-599; T3b t3_dwell over 400-599 and ph28.lost300 at W 200; B rows ph32.lost_t1. For A7/A7r, every
  key of ph30.Sim.finish except n2S and n2Z (below).

## 4. Fixes made during the run

**None.** src/fly.py was not changed after it was first written; every row header records the same sha256 and 'fixes
during the run: none'. Before the recorded run, src/module_identity.py was debugged in two script-check runs into a
scratch folder (MODULE_OUT); nothing from them is in experiments/module/. The first check crashed in the Stage C row
because that harness counts in 600-step blocks. That was a script error, not a difference, and the smoke size of A7
and A7r was set to 40 x 600. The second check was all IDENTICAL.

**Negative control, scratch only.** A one-ulp change of TURN_NOISE in the candidate was caught by L2 at event 0,
attribute last_turn, 10 of 40 rows differing, and by L1 in POS and HEAD. A one-ulp change of MARGIN was not caught: the
threshold is never met that closely, so the change had no effect on any state. Module constants are not attributes, so
L2 sees a constant only through what it changes.

## 5. Deviations and judgments for the review

1. **A7r's test-only setting.** The candidate's N, N_hi and c were set to 300, 300 and 240 after construction. The design
   named N and c; N_hi had to be set too, because it is a hashed attribute that Agent14N2 carries at 300. This is still
   draw-neutral and adds no constructor argument.
2. **L3 at A7/A7r leaves out n2S and n2Z** of the end-of-run record. They are ph30.Sim's sums of ReleaseN2's
   measurement-only attributes n2S and n2Z, which the confirmed section 10 point 6 drops. The candidate has no such
   attribute, so the harness adds nothing (src/ph30.py:225). The release state they measure is compared in L1 (SUS, Z via
   sustain and zreset, SIL) and in L2.
3. **S0 at A7/A7r ran 40 x 600**, not 40 x 200 (the harness's block size).
4. **Run-time dictionary entry.** ph33.ARMS received the run-time entry 'module D on' so that ph33.run can build the
   candidate. The file is not edited.
5. **Digits in hashes.** identity.txt prints the standard-hex sha256 of every imported source file. Two of them contain
   digit runs equal to seeds of phases without a seed scan: the hash of src/ph19.py contains a digit run equal to a ph12b evaluation seed and
   the hash of src/ph14b.py one equal to a ph12 evaluation seed (neither written here). No registered or derived seed number of ph33 or ph35 appears
   in any new file; checked against every seed constant in src/ph*.py and its derived numbers. identity.json and
   module_report.md contain none; identity.json writes its digests digit-free.

## 6. The demos (design section 6)

ph35.py demo and ph33.py demo were re-run unchanged into a scratch folder. **Both stop at their own seed-scan assertion
at HEAD, for a reason that predates this work.** Nine files committed after H28 and H29 carry their seed digits:
experiments/h12/h12_design_v1.md and _v2.md, experiments/h12/diagnosis/summary.json,
experiments/h18/arrays_b/K5b_restart_rand.npz (ph35 only), experiments/h29/h29_design_v1.md and _v2.md (ph33 only), three
summary.json files under notes/reviews/remote-runs/, and notes/synthesis/2026-09-29-level6-synthesis-design-v1.md, -v2.md
and -synthesis.md (by demo). **None of the hits is in a file made by this work.** Every output line before the assertion
equals the recorded demo (experiments/h29/ph35_demo.txt, experiments/h28/ph33_demo.txt).

Re-run a second time, with the scan's hits written to stderr and the scan then passed at run time, both demos completed
(exit 0). Every line equals the recorded demo except the seed-scan line itself, which prints a different file count.
Hits in files made by this work: 0 for each demo. Mending the nine files, or recording an exclusion, is the owner's and
the reviewing session's.

## 7. Constants cross-check (design section 2.3: 99 expected)

| Group | In the design | In src/fly.py | Where the rest stay |
|---|---|---|---|
| Core | 55 | 54 as module constants or fixed code (Upstream 5, circuit 4 + 9 defaults with gsat None, clip 1, hold 1, RESET_AFTER and MARGIN 2, reset 10.0, (S) RESET_AFTER + 1.0, the N2 test < 0.0, G 2.0 with gate, filter, scope and release fixed on 5, learning module 15, presence 4, three-channel 5) | the rng3 offset A3_OFF (src/ph32.py:109) stays in the harness, as design 4.2 registers; the identity script uses it as src/ph33.py:207 does |
| Body, agent side | 23 | 23 (ring 11, cue 2, controller 8, flee sides and the cast-sign start 2) | none |
| World and harness | 21 | 0 | the phN chain, unchanged (design 4.1) |
| **Total** | **99** | **77** | **22 in the phN chain** |

Formed values are formed as the chain forms them: sig**n, SAT = MAXOFF/CAST_GROW, DT/tau, sigma**p.

## 8. What the module does not claim

- No behaviour change, no fidelity to a fly beyond the phN chain's, no performance or speed claim.
- No reuse outside the fly world: a new body means a new input contract, benched before use (outlook section 5).
- Identity where tested only: the eleven rows above. Other worlds, values, windows or learning conditions are identical
  by code reading, not by this check. The three-channel learning path is not tested. A7 has no recorded reference; A7r
  compares against Agent14N2's class tree in its recorded harness and seeds, not against the report's printed numbers.
- Nothing about G 2's adoption status (flagged in the module docstring as the owner's, unsettled), U7, U8 or U10 is
  settled here; the docstring states them as readings.

## 9. Not done

- No commit, no push, no vinc record; no existing file edited (git status: three untracked paths, experiments/module/,
  src/fly.py, src/module_identity.py; git diff --stat empty).
- The reviewing session's recount (P3) and the owner's decision on what is recorded.
- The demos' seed-scan failure at HEAD (section 6) is reported, not repaired.
- T3b at t0 100 and 200 and Stage C E2-C: not taken (design section 10 point 7).
