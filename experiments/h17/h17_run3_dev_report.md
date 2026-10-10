# H17 Run3 GS250 DEV operation report

Date: 2026-10-10. DEV operation disposition: PASS. Frozen statistical disposition: PASS. The nine statistical clauses are reported unchanged for transparency; they are not an extra DEV efficacy gate or a reason for fitting, tuning or selection.

## Execution and validity

The owner separately opened DEV with "승인 한다 권고안 작업 진행" after the all-PASS BENCH. Exactly one reserved DEV pair was claimed durably before any DEV generator. The completed claim binds identity, metrics and raw evidence. There was no retry, reseed, replacement, extension or retuning. The registry contains one completed BENCH claim and one completed DEV claim; the registered EVAL pair remains unused.

Each of C0, T1, W1 and T3 retains 400 rows and 600 ticks for Fly, Passive, Agent17, GSOff and GS250. All twenty native validity gates passed. Independent verification checked 102473 saved arrays. ROOT independently rebuilt policy and endpoints, checked 510 arrays and recalculated all nine clauses without creating RNGs or drawing samples. Runner, verifier and ROOT agree on every clause and the statistical disposition.

One saved inference matrix has 5000 by 400 int64 indices. Seven paired endpoints reuse that matrix and linear quantiles at 0.025 and 0.975. The two proportion clauses use two-sided 95% Wilson intervals. The full 400-row denominators and 600-tick horizon are unchanged.

## Frozen statistical clauses

Paired estimates are GS250 minus Fly. E is any delivered whiff; V is valued-source dwell greater than other-source dwell, with ties failing; L is no delivered whiff in the last 200 ticks. D_other is nominal-other source dwell in steps per row. T1 intervention counts rows with any actual eligible intervention.

| Clause | Estimate | 95% interval | Frozen bound | Statistical status |
|---|---:|---|---|---|
| C0_absolute | 0.795 | [0.7527205845, 0.8316671618] | lower >= 0.5 | PASS |
| C0_E | 0.795 | [0.755, 0.8325] | lower >= 0.1 | PASS |
| T1_intervention | 0.01 | [0.003895483795, 0.02542656465] | upper <= 0.05 | PASS |
| T1_V | 0.0025 | [0, 0.0075] | lower >= -0.05 | PASS |
| T3_V | 0.0075 | [0, 0.0175] | lower >= -0.05 | PASS |
| T1_L | -0.005 | [-0.0125, 0] | upper <= 0.05 | PASS |
| W1_L | -0.0275 | [-0.045, -0.01] | upper <= 0.05 | PASS |
| T3_L | -0.015 | [-0.0275, -0.005] | upper <= 0.05 | PASS |
| W1_D_other | 0.7775 | [0.4925, 1.09] | lower >= -6 | PASS |

## Full-sample observations

| Condition | Arm | Rows | Any whiff | Any reach | Valued dwell majority | Lost last 200 | Ever engaged |
|---|---|---:|---:|---:|---:|---:|---:|
| C0 | Fly | 400 | 0 | 0 | 0 | 400 | 0 |
| C0 | GS250 | 400 | 318 | 266 | 134 | 82 | 400 |
| C0 | GSOff | 400 | 0 | 0 | 0 | 400 | 0 |
| C0 | Passive | 400 | 0 | 0 | 0 | 400 | 0 |
| C0 | Agent17 | 400 | 0 | 0 | 0 | 400 | 0 |
| T1 | Fly | 400 | 400 | 400 | 366 | 3 | 0 |
| T1 | GS250 | 400 | 400 | 400 | 367 | 1 | 4 |
| T1 | GSOff | 400 | 400 | 400 | 366 | 3 | 0 |
| T1 | Passive | 400 | 400 | 400 | 366 | 3 | 0 |
| T1 | Agent17 | 400 | 400 | 400 | 366 | 3 | 0 |
| W1 | Fly | 400 | 397 | 400 | 47 | 13 | 0 |
| W1 | GS250 | 400 | 400 | 400 | 29 | 2 | 55 |
| W1 | GSOff | 400 | 397 | 400 | 47 | 13 | 0 |
| W1 | Passive | 400 | 397 | 400 | 47 | 13 | 0 |
| W1 | Agent17 | 400 | 397 | 400 | 47 | 13 | 0 |
| T3 | Fly | 400 | 400 | 336 | 305 | 132 | 0 |
| T3 | GS250 | 400 | 400 | 338 | 308 | 126 | 13 |
| T3 | GSOff | 400 | 400 | 336 | 305 | 132 | 0 |
| T3 | Passive | 400 | 400 | 336 | 305 | 132 | 0 |
| T3 | Agent17 | 400 | 400 | 336 | 305 | 132 | 0 |

Conditional recovery windows are descriptive diagnostics and do not replace full-sample clauses. A horizon is eligible only when m+K <= 599 and uses m+1 through m+K. Conditional n below 50 remains UNREADABLE; zero remains UNDEFINED. Complete diagnostics are retained in metrics.json.

## Frozen implementation and prerequisites

The separate DEV runner and ROOT wrapper passed 26 pure tests and independent code/package review. Actual runner, frozen independent verifier and ROOT stage-binding preflights passed before the DEV claim. The six-file DEV stage closure is unchanged. All 133 original implementation files, 112 immutable specification files and five completed BENCH artifacts retain their pinned bytes. DEV stage authority is a separate saved binding; frozen MAIN provenance and the original schema remain unchanged.

The original implementation passed 107 tests and nineteen native boundary fixtures. Corrected spent H0 is PASS and VALIDITY_ONLY, with no inference or fresh RNG. Its earlier INVALID attempt and former sources remain preserved. BENCH passed all nine clauses and twenty gates, independent verification of 105577 arrays and ROOT recomputation of 510 arrays. The runtime retains CPython 3.13.12, NumPy 2.5.3, assertions enabled, one experiment process and all six numerical thread settings equal to one.

## Evidence and provenance

Large identity and raw evidence stay local; this canonical report supplies their path and AP SHA references. The digest alphabet is a through p.

| Artifact | AP SHA | Canonical source_doc |
|---|---|---|
| experiments/h17/run3/dev/identity.json | nadboimbidhnpafllnjgbodddblmgmpoikikledfajfjmheiehfelcbhedfepjbb | local evidence; cited by this canonical report |
| experiments/h17/run3/dev/metrics.json | acedmkmohiclfakmgpelkjafblnlohdohbcpmehobahadmfggojllmmpgakghnch | d53377ead269da536 |
| experiments/h17/run3/dev/verification.json | oeeokmanhmdiopffkkgpmplciojanmbglgckdcmfcnmkkhngejgpadfeimohilnp | dab64524e906adc27 |
| experiments/h17/run3/dev/parent_recomputation.json | dknhibelknldbndplgdfjhbcdadcphbbkbfljbjecdfpmcakeoiigcediiiffkmc | d2a731eda75693af0 |
| experiments/h17/run3/dev/stage_binding.json | hjamionbfabljkkoegoknbfinonheefodcghgifbggpmbkppjpojolfdckheenpn | d6de740df9499cf20 |
| experiments/h17/run3/dev/raw.npz.ap | mohhcmpljbeljgficdhohdnfopkkgpfjoflpfcdbajndnabljjpgnemfahhnenfe | local evidence; cited by this canonical report |
| experiments/h17/run3_registry/gnhlhibmpgklhlkeblghphgkdjgjicpgdeobikdmecojfkkmhmlcpkimipnnplmc.json | hcpindpffjoaidfgfjncnfacggglnhhfdjbiecclgbegahmjilgfgddhllipalea | local evidence; cited by this canonical report |
| config/h17-run3-dev-pins.json | ldbdealfhdgogndfkjamnafmandbdeecjkcejjkcoadcjfomngoplhocajicljhl | d65980f43c28a90ee |
| config/h17-run3-dev-opening.json | fknddjaiamhpfnoomplfcikbboaccdfkkkcjcdmbmhoiahiboaplbmjdhpcddlan | d199f6b863d26a1e3 |
| experiments/h17/h17_run3_dev_opening_checks.json | ieejnkofpipoijabkpdjeabjlmhipghpinchhjgcdmekkmflpfgifggmjdhmmeol | d7e8de2321309350b |
| experiments/h17/h17_run3_bench_report.md | kdapndonkiccbfgpgcgcofjgdonkhaaichhbeipkclfgadomlggebjlfbbhjpafp | d174ae279839d2dba |
| config/h17-run3-execution-pins.json | kmlmecemionbinjlgfaiminbefhonppaphdffoncehhcnbcnnihllkioklbojjji | d26e41a82a3c983ee |
| experiments/h17/h17_run3_design_v3.md | oibjjpnikgaejokpgfpfoffoaiapnngnfjcknhfhmbojheoopgnamoimaajjjnmh | d528fa87b2f4f63d2 |

Original implementation closure AP SHA: lkjcbpplkaangopbillnjeibfheenahmjhlfcbhdgpcefngfgkbkgegbdgefcali.
DEV stage closure AP SHA: fkpmaadhjpfmjidmpoabdfffhmcakbgondnffkmfehbciihehmggcbggcndpncnp.

Code and review citations use each file's actual canonical document:

- experiments/h17/h17_run3_dev_implementation_checks.json; AP SHA bnlnnomeblhaflaobfcdigfminogpceohkapoeehglgpolllienfdkephcpbggce; source_doc de6ea6eab9baf0194.
- notes/reviews/2026-10-10-h17-run3-dev-execution-review.md; AP SHA pdnijlfmdikidnncmkgdgiegdocenfiijgbipaokhbjgpkcdgboffpmkmoiellhh; source_doc de60574c8db032e61.
- tests/test_measure_h17_run3_dev.py; AP SHA gjgfdbbniifabnhhndpgmbkhnjmkjpjoeajhpglhamfbijdidnkbdenahbhbgbca; source_doc dd457f2ae6edb72c2.
- tests/test_recompute_h17_run3_dev.py; AP SHA cjpmbjaijdceenjiagdeemdjalnhbbohnjaagfcojaolllpiinddmbjbjmjfjcjk; source_doc debaf36d62e2a8459.
- tools/measure_h17_run3_dev.py; AP SHA npjojgmabdlimfaochnfgijbeidclnnmokbhopgebpefnolahcblflijkoefmmmo; source_doc da95cac51068d1c5e.
- tools/recompute_h17_run3_dev.py; AP SHA hoaohlpjmhfjmplbbffdflhcpmidnkcpokdgfcjoimlailmgiahpemngdapcpali; source_doc dd6400fb88c3202f1.
- src/h17_run3_arm.py; AP SHA kedhfjfpjnnkaigdldnkgjjikifimhjoegmbpmjninfifooidolfechelmacpfof; source_doc d5689184eb372a917.

## Interpretation and next gate

DEV operation PASS establishes complete fixed-sample execution, saved evidence and all validity/schema/runtime/source/draw/claim checks with independent verification and ROOT recomputation without error. Statistical readings above do not create another DEV gate or authorize a change to the frozen candidate. No fitting, parameter selection or retuning was performed.

The scope remains the constructed Run3 engineering conditions with supplied values, learning off, two channels, original World7 wind law and walls off. It does not establish a general fly-behavior forecast or authorize adoption. Native Fly/N2 behavior, historical H17 outcomes, hold D0 UNRESOLVED, A5/B3 stops, E1 branch-screen limits and the Q1-Q4 order retain their recorded status.

The next recommendation is a separately owner-opened EVAL using its own exclusive unused pair, the same fixed sample and frozen clauses/stop labels, followed by independent saved-evidence verification, ROOT recomputation and a report. EVAL has not been opened or run. No adoption is authorized.

The original R2 scanner passed the historical 661-file inventory with exactly the existing 42 protected-token pairs and no unused or error rows. This is not a rescan of the expanded final tree. New report and check bytes use the unchanged original protected-token guard with no new exception.
