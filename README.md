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
- `master_plan.md` the plan (renamed from `master_plan_updated.md`).
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
| (none yet) | H22, design only, no code yet | `experiments/h22/` |
