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
- `phN_*.txt` in the root are the recorded outputs of those runs; `h*_design_*.md` / `h*_report.md` are design docs and reports; `master_plan_updated.md` is the plan.
