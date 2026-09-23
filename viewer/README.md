# Whiff and Hold — trajectory viewer

Per-step trajectories of recorded runs, drawn as a 2D map and as a 3D scene of stylised flies.

- Path colour = the odour the selection circuit holds (valued / neutral / none); surge steps are drawn thick (dots in 3D).
- Plume cones are shaded by whiff probability (0.30·e^(−d/12)); a silenced source is drawn dashed.
- Arms are shown side by side (and together in the 3D scene) on identical worlds: same seeds, same noise, only the rule differs.
- The strip under each map shows the held odour, whiffs, and the two circuit unit states s.

## Open

`fetch` is blocked on `file://`, so double-clicking `index.html` does not load the data. Serve the folder instead:

```bash
cd viewer
python -m http.server
# then open http://localhost:8000/
```

Or via GitHub Pages at `https://vinculums.github.io/Fruitfly/viewer/` once Pages is enabled on `main` / root.

A published artifact copy of the page is private to the owner.

## Regenerate

```bash
python viewer/viz_export.py            # ~1 minute; writes viewer/trajectories.json and viewer/repro_check.txt
python viewer/viz_export.py --out DIR  # write elsewhere
```

The script imports `src/` unchanged (no bytecode written), reruns the recorded runs, checks them bitwise against the modules' own run functions and against the recorded counts, and refuses to export unless every check matches (`repro_check.txt` is the log). Schema: `SCHEMA.md`.

## What the data is

A bitwise reproduction of:

| World | Recorded output | Seeds (world/agent) | Arms |
|---|---|---|---|
| T1 (both sources emit) | `experiments/h23/ph21_eval.txt` | 1765 / 1865 | filter, maintain, known-answer |
| W1 (valued source absent) | `experiments/absent_odour_check/ph22_eval.txt` | 1775 / 1875 | Agent8, Agent6 |
| T3 (valued odour lost at t0 150) | `experiments/h24/ph23_bench.txt` | 20261011 / 20261012 (bench) | Agent8, Agent6 (Agent9 reproduced, not exported) |

Eight rows, each chosen by a criterion (`rows[].selection`):

| World / row | Criterion |
|---|---|
| T1 198 | (a) first hold valued in maintain and filter, both end V; max(filter + maintain valued dwell) |
| T1 318 | (b) first hold neutral in maintain and filter, maintain N (trapped), filter V (revised); max(maintain neutral dwell + filter valued dwell) |
| T1 5 | (c) dissociation: max over rows of filter steps at the valued source while holding neutral |
| T1 135 | (d) one of filter's N rows; max neutral dwell |
| W1 123 | (e) Agent8 reaches then passes through and ends far upwind (min final d_along − 0.5 dwell) while Agent6 dwell ≥ 20 |
| W1 225 | (f) Agent8 never reaches the present source; max Agent6 dwell |
| T3 244 | (g) both eligible; Agent8 holds valued on every step 150–599; Agent6 releases and is at the neutral source after t0; max Agent6 neutral steps after t0 |
| T3 177 | (h) Agent6 eligible and never within HIT_R of the neutral source after t0; earliest Agent6 L |
