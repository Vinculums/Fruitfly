# Fruitfly

Fruit fly circuit experiments (Phase 0.1 onward). The canonical record of each run lives in the Vinc graph (team space "Fruit Fly"); this repo holds the code and raw outputs so runs can be reproduced elsewhere.

## Run

```bash
pip install -r requirements.txt
cd src
python regress.py          # reruns Exp1-4 and checks every recorded number; exit 0 = all pass
python ph19.py             # any phase script runs standalone
```

- `src/ffcore.py` core models; `src/phN*.py` one script per phase (later phases import earlier ones, so run from `src/`).
- Recorded outputs (`phN_*.txt`) are no longer in the root; they live under `experiments/`, next to the design docs and reports for the same hypothesis.

## Layout

- `src/` all code, flat (scripts hash themselves and import each other by module name, so nothing in it moves).
- `experiments/<phase or hypothesis>/` recorded outputs (`*.txt`), design docs (`h*_design_*.md`, `h15_run2_spec_*.md`) and reports (`h*_report.md`).
- `master_plan.md` the plan (renamed from `master_plan_updated.md`); the git copy is the source of truth, the graph copy a mirror.
- `notes/` outlook notes (not decisions, nothing measured); canonical copies in the Vinc graph.
- `viewer/`: trajectory viewer (2D map + 3D scene) and the export script that reproduces the recorded runs; open via a local server or GitHub Pages.
- The canonical record, with sha256 provenance for every output file, is the Vinc graph (team space "Fruit Fly").

| Script (`src/`) | Hypothesis / phase | Folder |
|---|---|---|
| `ph2*.py`, `ph3*.py`, `ph4*.py` (`b4_*` baselines) | Phases 2-4 adopted designs | `experiments/phase2-4/` |
| `ph5*.py`, `ph5b*.py` | Phase 5 | `experiments/phase5/` |
| `ph6.py` | Phase 6 abstraction ladder | `experiments/phase6/` |
| `ph7.py` | H9 (Phase 7.1) | `experiments/h09/` |
| `ph8.py` | H11 (Phase 7.2) | `experiments/h11/` |
| `ph9.py` | H13 (Phase 7.3) | `experiments/h13/` |
| `ph10.py`, `ph10_adopt.py` | H14 | `experiments/h14/` |
| `ph11.py` | H15 Run 1 | `experiments/h15/` |
| `ph12.py`, `ph12b.py`, `ph12c.py` | H16 Runs 1-2 + input contract | `experiments/h16/` |
| `ph13.py`, `ph13b.py` | two-source check + unrecovered diagnosis (before H15 Run 2) | `experiments/h15/` |
| `ph14.py`, `ph14b.py` | H19(a) | `experiments/h19/` |
| `ph15.py`, `ph15_*.py` | H15 Run 2 | `experiments/h15/` |
| `ph16.py`, `ph16b.py`, `ph16c.py` | H20 Stage A | `experiments/h20/` |
| `ph17.py` | selection-to-navigation link check (H20) | `experiments/h20/` |
| `ph18.py`, `ph18b.py` | H20 Run 2 + diagnosis | `experiments/h20/` |
| `ph19.py` | H21 | `experiments/h21/` |
| `ph20.py`, `ph20b.py` | H22 (bench: no candidate) + post-bench diagnosis | `experiments/h22/` |
| `ph21.py` | H23 | `experiments/h23/` |
| `ph22.py` | absent-odour check (after H23) | `experiments/absent_odour_check/` |
| `ph21b.py` | option-v presence diagnosis (before H24) | `experiments/h24/` |
| (none yet) | H24, design v1 only, no code yet | `experiments/h24/` |
| `ph26.py`, `ph26b.py`, `ph27.py`, `ph27b.py` | H17 (design v2 FINAL; demo `ph26_demo.txt`, bench `ph26_bench.txt`: stopped at the bench, no candidate on part (d); tasks not run) + post-bench diagnosis (`ph26b_diag.txt`, measurement only); H17 Run 2 (`ph27.py`, design v1 DRAFT `h17_run2_design_v1.md`, v2 FINAL `h17_run2_design_v2.md`: engagement at q >= 250, T3 (c) re-signed; demo `ph27_demo.txt`, bench `ph27_bench.txt`: stopped at the bench by the (h2) stop rule; tasks not run) + Run 2 post-bench diagnosis (`ph27b.py`, `ph27b_diag.txt`, `h17_run2_post_bench_diagnosis.md`, measurement only). **H17 CLOSED as NOT shown** (decision:h17-closed, 2026-09-24): nothing adopted, tasks never run | `experiments/h17/` |
| `ph28.py` | H26 adaptive presence (design v1 DRAFT `h26_design_v1.md`, v2 FINAL `h26_design_v2.md`; demo `ph28_demo.txt`, bench `ph28_bench.txt` (M4 PASS, stop rules continue) on the file with the bar unset; demo `ph28_demo_bar.txt`, development run `ph28_dev.txt`, one evaluation `ph28_eval.txt` with the bar set; report `h26_report.md`: SHOWN under the registered criteria). **H26 CLOSED as SHOWN; presence counter and Agent14 ADOPTED within the tested conditions** (decision:h26-closed, decision:h26-adaptive-presence-adopted-within-tested-conditions, 2026-09-25) | `experiments/h26/` |
| `ph29.py` | H20 Stage B, the learning check (design v1 DRAFT `h20_stage_b_design_v1.md`, v2 FINAL `h20_stage_b_design_v2.md`; demo `ph29_demo.txt`, bench `ph29_bench.txt` (M4 PASS, stop rules continue), development run `ph29_dev.txt`, one evaluation `ph29_eval.txt` (SHOWN under the registered criteria), report `h20_stage_b_report.md`). **H20 Stage B CLOSED as SHOWN** (decision:h20-stage-b-closed, 2026-09-25): a learned positive value is used in behaviour within the tested conditions; nothing new adopted | `experiments/h20/` |
| `ph30.py`, `ph30b.py` | H20 Stage C, the integration check (Agent14 with learning on in the H15 Run 2 world; design v1 DRAFT `h20_stage_c_design_v1.md`, v2 FINAL `h20_stage_c_design_v2.md`; demo `ph30_demo.txt`, bench `ph30_bench.txt`; the first bench run and its demo kept as `ph30_bench_before_fix.txt`, `ph30_demo_before_fix.txt`). **STOPPED at the bench by the (hR) stop rule** (record:h20-stage-c-bench-result); tasks not run + post-bench diagnosis (`ph30b.py`, `ph30b_diag.txt`, report `h20_stage_c_post_bench_diagnosis.md`; measurement only, record:h20-stage-c-post-bench-diagnosis-result); Stage C Run 2 opened for design (decision:h20-stage-c-run2-open-design; design v1 DRAFT `h20_stage_c_run2_design_v1.md`) and on design v2 FINAL `h20_stage_c_run2_design_v2.md` (decision:h20-stage-c-run2-open: M4(c) readability re-signed to read on G3+, (hR) restated, new seeds) | `experiments/h20/` |
| `ph31.py` | H20 Stage C Run 2 (imports `ph30.py` and `ph30b.py` unchanged; M4(c) readability on G3+, (hR) restated, bench (r')); demo `ph31_demo.txt`, bench `ph31_bench.txt` (M9 PASS, record:h20-stage-c-run2-bench-result), development run `ph31_dev.txt`, evaluation `ph31_eval.txt`, report `h20_stage_c_run2_report.md`. **Evaluated once: SHOWN under its registered criteria, M1 to M9 all PASS** (record:h20-stage-c-run2-result). **H20 Stage C Run 2 CLOSED as SHOWN** (decision:h20-stage-c-run2-closed); the value-gated release (N2) ADOPTED, so the adopted agent is Agent14N2 in `ph30.py` (decision:n2-release-adopted-within-tested-conditions); **H20 CLOSED as a whole** (decision:h20-closed, 2026-09-25). A chance number match in `ph31_eval.txt` is excluded as a (file, number) pair by decision:seed-scan-exclusion-ph31-eval | `experiments/h20/` |
| `ph32.py`, `ph32b.py` | H27, a third irrelevant odour as a distractor (Agent15 = Agent14N2 with three channels; design v1 DRAFT `h27_design_v1.md`, v2 FINAL `h27_design_v2.md`; demo `ph32_demo.txt`, bench `ph32_bench.txt`: M4 PASS, STOPPED at the bench by the stop rules (h), (hW), (hH), record:h27-bench-result; tasks not run; `ph32b.py` the post-bench diagnosis, measurement only, `ph32b_diag.txt`, `h27_post_bench_diagnosis.md`, record:h27-post-bench-diagnosis-result). **H27 CLOSED as NOT shown** (decision:h27-closed, 2026-09-26): stopped at the bench, tasks never run, nothing adopted; the distractor condition recorded as a limit of the adopted agent (record:distractor-capture-limit) | `experiments/h27/` |
| `ph33.py` | H28, discounting a ubiquitous odour by its whiff statistics (a burst-ranked value tie; Agent16 = Agent15 + Act16, `ph32.py` imported unchanged; design v1 DRAFT `h28_design_v1.md`, v2 FINAL `h28_design_v2.md`; demo `ph33_demo.txt`, bench `ph33_bench.txt`: M4 PASS, (h) and (hW) continue, record:h28-bench-result; development run `ph33_dev.txt`, record:h28-dev-run; one evaluation `ph33_eval.txt`: SHOWN under its registered criteria, record:h28-result; report `h28_report.md`). **H28 CLOSED as SHOWN** (decision:h28-closed, 2026-09-26); the burst-ranked value tie **ADOPTED for the three-channel distractor form only** (decision:h28-burst-tie-adopted-within-tested-conditions; Agent16 as composed; inert at two channels by code); W1D still loses 222/400 rows (record:distractor-capture-limit-under-h28-tie) | `experiments/h28/` |
| `ph34b.py`, `ph35.py` | H29, the H26 T3b limit, a loss after tracking (design v1 DRAFT `h29_design_v1.md`; decision:h29-open-design). No own-state rule can separate a loss from a tracking silence (the Lost world equals its T1 twin until the next valued whiff). `ph34b.py`: the measurement-only T3b diagnosis (decision:t3b-diagnosis; `ph34b_diag.txt`, `t3b_diagnosis.md`): F1 MET, F2 NOT MET, F3 NOT MET, F4 INCONCLUSIVE, F5 MET (T3b gain +2.460), F6 INCONCLUSIVE. `ph35.py`: H29 opened on design v2 FINAL `h29_design_v2.md` (decision:h29-open), Agent17 = Agent14N2 with the post-whiff window 200 (no adopted file edited); demo `ph35_demo.txt`, bench `ph35_bench.txt`: M4 PASS, (h) and (hB) continue, record:h29-bench-result; development run `ph35_dev.txt`, record:h29-dev-run; one evaluation `ph35_eval.txt`: SHOWN under its registered criteria (M2(b) -0.0075, M8(b) +1.9525), T3b at t0 100 and 200 reported, record:h29-result; report `h29_report.md`. **H29 CLOSED as SHOWN** (decision:h29-closed, 2026-09-26); the window 200 (start 140, prior unchanged) **ADOPTED within the tested conditions**, superseding the H26 window: **Agent17 is the adopted two-channel agent** (decision:h29-window-200-adopted-within-tested-conditions); limit: the T3b gain's cast-phase dependence | `experiments/h29/` |
| (none; design only) | H12, the acquisition and extinction traces persist differently (queued at the Phase 7.2 close): **opened for design** (decision:h12-open-design, 2026-09-26); design v1 DRAFT `h12_design_v1.md` (doc dff68b78ea66ed47e), for the owner's confirmation of section 12; no code. Recommended: a Stage 1 module bench (the parallel site with a decaying extinction pair, `ph36.py` proposed) gating a Stage 2 behavioural test | `experiments/h12/` |
