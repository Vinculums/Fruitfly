# Hold E1 W1Dp: exposure reached, below the registered screen

Date: 2026-10-09. Authority: decision:hold-e1-w1dp-open, owner-confirmed
v2 FINAL. One full pair-keyed invocation completed; its durable claim remains.
Status: **REACHED, BELOW REGISTERED SCREEN**. Nothing adopted. No benefit
trial opened, no seed replacement, extension, tuning or automatic repeat.

## Primary result and unchanged criteria

Both conditions have 400 complete rows and 600 steps, 240000 row-steps each.
Only actual H advances; R is a passive same-state projection. Exposure means
different clipped turn commands before the common noise draw.

| Criterion | Observed evidence | Result |
|---|---|---|
| X1 | H0 and both conditions' full identity/passivity/construction/draw/projection gates pass | PASS |
| X2 | B5 +1/-1/0: 397/400 exposed rows, 62042 differing command steps | PASS |
| X3 | B4 +1/0/0: 5/400 exposed rows (1.25%), 7 differing command steps; required at least 40 rows | FAIL |
| X4 | B4 actual H: 38/400 lost rows (9.5%); inclusive accepted range 20-380 | PASS |

B5 lost rows are 75/400 and reported only. Loss means no whiff of either
original source in the last 200 steps; D is excluded. Source index and physical
positive-y side are recorded separately; neither substitutes for the primary
measure. No confidence interval, bootstrap, power estimate, benefit/cost
contrast or causal interpretation of loss differences is registered here.

## Branch attribution and denominators

In B4 there are 222 simultaneous B-D burst steps and 14463 raw latest-burst
tie steps. The conjunction T1-T4 qualifies 170 row-steps. T1-T5 qualifies seven,
so f_id is 7/170 = 0.041176470588235294. This is a conditional identity/navigation
split on qualifying tied-single observations, not a probability of exposed rows.
All seven differing clipped commands occur on that tied-burst route; zero
commands differ outside it. Thus the intended branch is reached in this sample,
while the all-command row count remains below the unchanged X3 threshold.

In B5 there are 192 simultaneous bursts and 14086 raw tie steps, but zero
qualifying T1-T4 observations: f_id is null, not zero. All 62042 differing
commands are outside the tied-burst conjunction. This positive-control coverage
is reported separately from the adopted +1/0/0 question.

Plume observations use all 240000 row-steps in each condition. B4 has 27654
steps with nonzero B-plume probability, 4699 B whiffs and 4751 independent
D whiffs. B5 has 23087 such steps, 3986 B whiffs and 3985 D whiffs. These are
descriptions of the two actual H paths, not forecasts or a benefit contrast.

## Identity, provenance and independent verification

Canonical spent H0 reproduces the untouched ph33.run at zero tolerance:
55 output fields, 107 same-lineage state fields, 400 act/bump events, eleven
generator constructions and every pre/sense/wind/D/twin/act/bump checkpoint.
Full B4/B5 lineage-to-Fly and Fly-to-Passive comparisons pass L1, the frozen
historical cross-class field map, strict same-class state/RNG/input/return
checks, original historical scores and the added complete ph25/ph22 W1 summary.
Each full comparison has 1200 act/bump events. No diagnostic was excluded.

The original B-plume law is evaluated before movement; D uses its own uniform
at every row-step, including zero probability. Masked V raw draws and twin
world/wind audits are retained. Source/runtime/FINAL/config/registration pins
were checked before and after gates. Measurement uses 91 immutable files,
Python 3.13.12, NumPy 2.5.3, local single process and thread counts one.
The fresh screen pair and derived streams were scanned and registered before
implementation completion and before any screen generator construction.

Root validation: 31 existing/runner tests and 12 independent verifier tests
PASS (43 total). The separately authored saved-evidence verifier passes raw
file/per-array hashes, H0, full gates, state/projection/mask reconstruction,
generator roles/continuity, claim, complete W1 scores and X1-X4. Root also
recomputed exposed rows/steps, per-row first steps and counts, lost rows,
T1-T5, f_id and route command counts directly from saved NumPy arrays, importing
neither the runner nor the independent verifier's aggregation helpers.
Both computations agree. R2 scan-only verification passes: all 25 ph33 and
17 ph35 registered pairs accounted for, no errors or unused rows; no exception,
reference source or downstream source pin changed. Its receipt is preserved
in experiments/hold/hold_e1_execution_checks.json. Later-created summaries and
registration receipts are separately checked for protected tokens.

## Reproduction and disposition

Read-only verification: python tools/verify_hold_e1.py --output
experiments/hold/hold_e1. This reads the stored sample, not a new simulation.
The runner's global claim refuses another full invocation of the registered
pair even with a different output directory.

Evidence: identity.json, exposure.json, raw.npz.ap, verification.json and
root_recomputation.json in this directory. Raw NPZ bytes are losslessly encoded
with the a-p alphabet to prevent accidental protected seed-token matches;
dtype, shape and SHA-256 alphabet hashes accompany every array. Execution
manifest: config/hold-e1-execution-pins.json. Registration receipt:
experiments/hold/hold_e1_seed_registration.json. Pre-measurement review:
notes/hold/2026-10-09-hold-e1-execution-review.md.

E1 establishes finite-sample reachability in W1Dp, below the registered entry
screen for a separate benefit design. It neither establishes hold's behavioral
advantage nor proves a universal absence of exposure. D0 remains UNRESOLVED;
earlier coverage A5/B3 primary-criterion stops remain unchanged. Final owner
reading and any later project disposition remain pending.
