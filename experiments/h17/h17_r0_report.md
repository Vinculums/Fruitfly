# H17 R0: one passive current-Fly baseline measurement

Date: 2026-10-09. Status: COMPLETE; all validity gates passed. Descriptive measurement only.
Owner instruction: "다음 권고 사항 작업 진행". Execution decision: decision:h17-r0-open.
FINAL: experiments/h17/h17_r0_design_v2.md; canonical db4aadf3b4101cef9.

## Result and interpretation

The reserved pair was claimed once, and all C0/T1/W1/T3 measurements completed. The reviewing root independently recomputed the registered readings from saved arrays after the independent verifier passed. No search candidate, efficacy criterion, renewed state relaxation or adoption was opened.

| Condition | Registered primary measure | Observation marker | No marker | Any delivered whiff, full horizon | Reach, full horizon |
|---|---|---|---|---|---|
| C0 | 0/400; 0.00% [0.00, 0.95]; READABLE | 400/400; 100.00% [99.05, 100.00]; READABLE | 0/400; 0.00% [0.00, 0.95]; READABLE | 0/400; 0.00% [0.00, 0.95]; READABLE | 0/400; 0.00% [0.00, 0.95]; READABLE |
| T1 | 3/400; 0.75% [0.26, 2.18]; READABLE | 4/400; 1.00% [0.39, 2.54]; READABLE | 396/400; 99.00% [97.46, 99.61]; READABLE | 400/400; 100.00% [99.05, 100.00]; READABLE | 400/400; 100.00% [99.05, 100.00]; READABLE |
| T3 | 139/400; 34.75% [30.25, 39.54]; READABLE | 16/400; 4.00% [2.48, 6.40]; READABLE | 384/400; 96.00% [93.60, 97.52]; READABLE | 400/400; 100.00% [99.05, 100.00]; READABLE | 331/400; 82.75% [78.74, 86.14]; READABLE |
| W1 | 35/400; 8.75% [6.36, 11.93]; READABLE | 70/400; 17.50% [14.09, 21.53]; READABLE | 330/400; 82.50% [78.47, 85.91]; READABLE | 398/400; 99.50% [98.20, 99.86]; READABLE | 400/400; 100.00% [99.05, 100.00]; READABLE |

C0 primary is any delivered whiff in steps 0 through 299. T1, W1 and T3 primary is lost: no delivered whiff in steps 400 through 599. Reach is either source at distance strictly below 3 after movement. Wilson 95% intervals are descriptive row incidences, not efficacy tests.

Four conditions use matched constructions of 400 rows and 600 steps; they do not constitute independent groups of 1600 rows. The literal Fly, passive Fly and literal Agent17 arms are identity checks, not three independent samples. Walls are off, learning is off, and N2, presence/window and original controllers are unchanged. C0 is a constructed position-only, zero-initial-plume stress, not a naturally produced N2 release population.

## Strict post-marker windows

The marker is the first post-act q_obs >= 250 with h == -1. It is an observation, not an actual intervention. Windows contain only m+1 through m+K; step m reach is a separate baseline. Full windows require m+K <= 599. Late markers are censored, never counted as failures. A conditional denominator below 50 is UNREADABLE; a zero denominator is UNDEFINED.

| Condition | K | Full rows | Censored rows | Whiff | Reach |
|---|---|---|---|---|---|
| C0 | 100 | 400 | 0 | 0/400; 0.00% [0.00, 0.95]; READABLE | 0/400; 0.00% [0.00, 0.95]; READABLE |
| C0 | 200 | 400 | 0 | 0/400; 0.00% [0.00, 0.95]; READABLE | 0/400; 0.00% [0.00, 0.95]; READABLE |
| C0 | 300 | 400 | 0 | 0/400; 0.00% [0.00, 0.95]; READABLE | 0/400; 0.00% [0.00, 0.95]; READABLE |
| T1 | 100 | 0 | 4 | 0/0; UNDEFINED | 0/0; UNDEFINED |
| T1 | 200 | 0 | 4 | 0/0; UNDEFINED | 0/0; UNDEFINED |
| T1 | 300 | 0 | 4 | 0/0; UNDEFINED | 0/0; UNDEFINED |
| T3 | 100 | 16 | 0 | 0/16; 0.00% [0.00, 19.36]; UNREADABLE | 0/16; 0.00% [0.00, 19.36]; UNREADABLE |
| T3 | 200 | 16 | 0 | 5/16; 31.25% [14.16, 55.60]; UNREADABLE | 2/16; 12.50% [3.50, 36.02]; UNREADABLE |
| T3 | 300 | 5 | 11 | 4/5; 80.00% [37.55, 96.38]; UNREADABLE | 4/5; 80.00% [37.55, 96.38]; UNREADABLE |
| W1 | 100 | 63 | 7 | 3/63; 4.76% [1.63, 13.09]; READABLE | 44/63; 69.84% [57.64, 79.76]; READABLE |
| W1 | 200 | 56 | 14 | 29/56; 51.79% [39.01, 64.33]; READABLE | 51/56; 91.07% [80.74, 96.13]; READABLE |
| W1 | 300 | 54 | 16 | 35/54; 64.81% [51.48, 76.18]; READABLE | 52/54; 96.30% [87.46, 98.98]; READABLE |

| Condition | Any post-marker whiff to horizon | Any post-marker reach to horizon | Reach at marker baseline |
|---|---|---|---|
| C0 | 0/400; 0.00% [0.00, 0.95]; READABLE | 0/400; 0.00% [0.00, 0.95]; READABLE | 0/400; 0.00% [0.00, 0.95]; READABLE |
| T1 | 1/4; 25.00% [4.56, 69.94]; UNREADABLE | 1/4; 25.00% [4.56, 69.94]; UNREADABLE | 0/4; 0.00% [0.00, 48.99]; UNREADABLE |
| T3 | 9/16; 56.25% [33.18, 76.90]; UNREADABLE | 9/16; 56.25% [33.18, 76.90]; UNREADABLE | 0/16; 0.00% [0.00, 19.36]; UNREADABLE |
| W1 | 37/70; 52.86% [41.32, 64.10]; READABLE | 59/70; 84.29% [74.01, 90.99]; READABLE | 0/70; 0.00% [0.00, 5.20]; READABLE |

Horizon incidences have unequal remaining time and are not substitutes for strict fixed-length windows. Simultaneous source whiffs and reach retain both source bits; no argmax collapse is used.

## Source identity, W1 and geometry

Nominal good/other follows each row construction rather than a fixed source index. W1 nominal good delivery is zero; the retained raw source draw and copied pre-sense twin are verified. W1 other-source last-horizon whiff is the complement of its registered lost count. Dwell below is the mean row fraction within distance strictly below 3 after movement.

| Condition | Semantic source | Span | Whiff | Reach | Dwell mean | Dwell steps |
|---|---|---|---|---|---|---|
| C0 | nominal_good | full | 0/400; 0.00% [0.00, 0.95]; READABLE | 0/400; 0.00% [0.00, 0.95]; READABLE | 0.00000000 | 0 |
| C0 | nominal_good | last200 | 0/400; 0.00% [0.00, 0.95]; READABLE | 0/400; 0.00% [0.00, 0.95]; READABLE | 0.00000000 | 0 |
| C0 | nominal_other | full | 0/400; 0.00% [0.00, 0.95]; READABLE | 0/400; 0.00% [0.00, 0.95]; READABLE | 0.00000000 | 0 |
| C0 | nominal_other | last200 | 0/400; 0.00% [0.00, 0.95]; READABLE | 0/400; 0.00% [0.00, 0.95]; READABLE | 0.00000000 | 0 |
| T1 | nominal_good | full | 389/400; 97.25% [95.14, 98.46]; READABLE | 388/400; 97.00% [94.83, 98.28]; READABLE | 0.04077500 | 9786 |
| T1 | nominal_good | last200 | 373/400; 93.25% [90.36, 95.32]; READABLE | 361/400; 90.25% [86.95, 92.79]; READABLE | 0.04205000 | 3364 |
| T1 | nominal_other | full | 345/400; 86.25% [82.53, 89.28]; READABLE | 190/400; 47.50% [42.65, 52.39]; READABLE | 0.00840000 | 2016 |
| T1 | nominal_other | last200 | 64/400; 16.00% [12.73, 19.91]; READABLE | 24/400; 6.00% [4.06, 8.77]; READABLE | 0.00315000 | 252 |
| T3 | nominal_good | full | 317/400; 79.25% [75.01, 82.94]; READABLE | 304/400; 76.00% [71.58, 79.93]; READABLE | 0.02910833 | 6986 |
| T3 | nominal_good | last200 | 244/400; 61.00% [56.14, 65.65]; READABLE | 236/400; 59.00% [54.12, 63.71]; READABLE | 0.02426250 | 1941 |
| T3 | nominal_other | full | 345/400; 86.25% [82.53, 89.28]; READABLE | 98/400; 24.50% [20.54, 28.94]; READABLE | 0.00360833 | 866 |
| T3 | nominal_other | last200 | 38/400; 9.50% [7.00, 12.77]; READABLE | 5/400; 1.25% [0.54, 2.89]; READABLE | 0.00035000 | 28 |
| W1 | nominal_good | full | 0/400; 0.00% [0.00, 0.95]; READABLE | 338/400; 84.50% [80.63, 87.72]; READABLE | 0.01622917 | 3895 |
| W1 | nominal_good | last200 | 0/400; 0.00% [0.00, 0.95]; READABLE | 49/400; 12.25% [9.39, 15.83]; READABLE | 0.00686250 | 549 |
| W1 | nominal_other | full | 398/400; 99.50% [98.20, 99.86]; READABLE | 383/400; 95.75% [93.30, 97.33]; READABLE | 0.03985000 | 9564 |
| W1 | nominal_other | last200 | 365/400; 91.25% [88.07, 93.64]; READABLE | 348/400; 87.00% [83.35, 89.95]; READABLE | 0.04311250 | 3449 |

Fixed source identities 0 and 1, all four balanced construction cells, source-specific strict windows, selection/navigation concurrence and full original L1/L2/L3 outputs are retained in metrics.json and raw.npz.ap; parent_recomputation.json independently checks source/cell/dwell arithmetic. Navigation concurrence is not a causal attribution. Each construction cell has exactly 100 rows. All contact event and contact row counts are zero.

## T3 N2 transitions

Event counts count repeated steps; row counts count rows with at least one event. They must not be interchanged. Negative-to-unheld comprises zero or multiple post-circuit active units; identity changes are distinct. Timeout/evidence concurrence records coexistence, not cause.

| Observed mask | Events | Rows | Neither | Timeout only | Evidence only | Both |
|---|---|---|---|---|---|---|
| base | 7091 | 389 | 0 events / 0 rows | 7091 events / 389 rows | 0 events / 0 rows | 0 events / 0 rows |
| negative_end | 108 | 101 | 4 events / 4 rows | 3 events / 3 rows | 101 events / 98 rows | 0 events / 0 rows |
| negative_identity_change | 0 | 0 | 0 events / 0 rows | 0 events / 0 rows | 0 events / 0 rows | 0 events / 0 rows |
| negative_multiple_units | 0 | 0 | 0 events / 0 rows | 0 events / 0 rows | 0 events / 0 rows | 0 events / 0 rows |
| negative_same | 69258 | 248 | 67024 events / 248 rows | 1588 events / 165 rows | 645 events / 98 rows | 1 events / 1 rows |
| negative_to_unheld | 108 | 101 | 4 events / 4 rows | 3 events / 3 rows | 101 events / 98 rows | 0 events / 0 rows |
| negative_zero_units | 108 | 101 | 4 events / 4 rows | 3 events / 3 rows | 101 events / 98 rows | 0 events / 0 rows |
| sustain | 5505 | 293 | 0 events / 0 rows | 5505 events / 293 rows | 0 events / 0 rows | 0 events / 0 rows |
| withheld_N1_S | 1586 | 164 | 0 events / 0 rows | 1586 events / 164 rows | 0 events / 0 rows | 0 events / 0 rows |
| withheld_N1_Z | 258 | 249 | 258 events / 249 rows | 0 events / 0 rows | 0 events / 0 rows | 0 events / 0 rows |
| zreset | 872 | 308 | 872 events / 308 rows | 0 events / 0 rows | 0 events / 0 rows | 0 events / 0 rows |

withheld_N1_S and withheld_N1_Z are gates withheld by current N2, not executed N1 interventions. Negative hold endings alone do not demonstrate sustained-timeout-produced stranding. Per-sign, identity and full registered field readings remain in saved arrays and verification receipts.

## Validity and provenance

- Frozen closure: 96 source files; 3096 fixed non-blob array keys plus the pinned typed-blob grammar. Python/NumPy/native runtime and all six thread limits are pinned; one local process.
- Runner/helper and independent verifier suites: 39 tests passed. Adversarial reviews were cleared before the main draw.
- Final spent-input H0: all 12 identity gates, independent verifier and reviewing-root arithmetic passed. Two failed instrumentation H0 attempts and the successful pre-index H0 are preserved; H0 rates are not the main anchor.
- Main: all 12 condition/arm gates passed, including full construction, original typed state/input/return/output arrays, generator phase checkpoints, original primitive returns and frozen lineage. Primitive projection is explicitly contingent on complete identity.
- Independent verifier: saved-array, original equations, provenance, archive grammar and registered reading checks passed without executing trajectories. Reviewing root separately recomputed primary, clocks, markers, windows, cells, N2 masks, source whiff/reach/dwell and W1 complement from the same arrays.
- Pre-main R2: both original checkers scanned 621 files, using exactly the registered exception pairs, with no unused exception or error. Post-main evidence receives a protected-token delta check and AP archive alphabet/hash checks. Historical source/FINAL/registration/measurement closures remain immutable.

| Evidence | SHA256 (a-p encoding) |
|---|---|
| config/h17-r0-execution-pins.json | dcoacgfhhbjnacpfgohmaelnfdbckjoegliincphdmhkldlodbdjenhhlgggadkh |
| experiments/h17/h17_r0_pre_draw_checks.json | cdfndanbnaiaehpfgkbjfeoebilihefnamaeokibaofcjonkidagcdoicefpabci |
| experiments/h17/h17_r0_r2_pre_main.json | alnbndcokbjknnmknbkpeooimamblhpehgbdmhgkjncbcbafohnggedoplpoepfo |
| experiments/h17/r0/identity.json | ojkekmagcnglcbfceaighkjnnigkdnkbpnpjhcfelcmnpbomdgnkokgcefokokkg |
| experiments/h17/r0/metrics.json | mmdgdhkpiophlkhddebbgfojkopjahcfeomcnimobacnbchajcibodanikochjel |
| experiments/h17/r0/verification.json | fnfkpbdicfmkjegnbogodpbfjlkefldckhcgbdclmaodgchlnniohlacedphdbjc |
| experiments/h17/r0/parent_recomputation.json | hflbddioikfncoclcnbgcdhaaklhegmheancdmbkhfpfiohikhnbnalaokihaagp |
| experiments/h17/r0/raw.npz.ap | bdjliepfoneecapofbnelegdajohjcfekcckfofdmnkoophdcgooinfccggfdopc |

Source closure: ipnbbdcgnhimipkghbaefggdkdidknipflgdijhihabegkmnfjbbilgceglgpbgd.
Canonical execution review: d22a8acd2b108796a. Canonical pin index: d98d4328ae709a589, with four exact-readback pin parts. Execution opening: d539fa523228ae7f7. Final execution_checks.json records the report/graph/master readbacks and post-main checks.

## Next recommendation

Use this current baseline and its readable C0 marker/entry population to refine one Run 3 cold-search candidate design. Define its exact first-leg convention and its own walked anchor from stored marker pose, heading, cast/flee signs and presence/ring state. Keep N2 and the adopted presence/window. Any any-odour clock read by a controller requires a renewed explicit state relaxation.

Keep T1/W1/T3 as regression contexts. Do not extrapolate a current candidate effect or power from old Agent10/Agent13 rates, restore N1 to manufacture a population, increase horizons, select fresh pairs after seeing results or count conditional groups below the registered readability screen as evidence. Candidate selection, efficacy criteria, source/state changes and execution remain unopened. Q1-Q4 retain their recorded queue order; Q3 parallel work stays held. Historical H17 NOT shown and hold D0 UNRESOLVED / A5-B3 bench stops / E1 below-screen dispositions are unchanged.
