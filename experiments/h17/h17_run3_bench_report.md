# H17 Run3 GS250 BENCH report

Date: 2026-10-10. Final disposition: PASS within the frozen Run3 v3 BENCH scope. All nine required clauses passed the runner, independent saved-evidence verification and ROOT saved-array recomputation.

## Execution and validity

Exactly one authorized fresh BENCH pair was claimed durably before reserved generators were created. The completed claim binds the identity, metrics and raw evidence. No retry, reseed, replacement, extension or retuning occurred after that claim.

Each of C0, T1, W1 and T3 uses 400 rows and 600 ticks for Fly, Passive, Agent17, GSOff and GS250. All twenty native validity gates passed. Independent verification checked 105577 saved arrays. ROOT independently rebuilt the policy and endpoints, checked 510 arrays, and recalculated all nine clauses without constructing RNGs or drawing samples.

One saved inference matrix has 5000 by 400 int64 indices. Seven paired endpoints reuse that matrix; their intervals use linear quantiles at 0.025 and 0.975. The two proportion clauses use two-sided 95% Wilson intervals. Primary denominators retain all 400 rows and the full 600 ticks.

## Required clauses

Paired estimates are GS250 minus Fly. E means any delivered whiff; V means valued-source dwell exceeds other-source dwell (ties fail); L means no delivered whiff in the last 200 ticks. D_other is dwell at the nominal-other source, in steps per row. T1 intervention counts rows with any actual eligible intervention.

| Clause | Estimate | 95% interval | Required bound | Status |
|---|---:|---|---|---|
| C0_absolute | 0.81 | [0.76867623, 0.84542615] | lower >= 0.5 | PASS |
| C0_E | 0.81 | [0.77, 0.8475] | lower >= 0.1 | PASS |
| T1_intervention | 0.01 | [0.0038954838, 0.025426565] | upper <= 0.05 | PASS |
| T1_V | 0.005 | [0, 0.0125] | lower >= -0.05 | PASS |
| T3_V | 0.0125 | [0.0025, 0.025] | lower >= -0.05 | PASS |
| T1_L | -0.01 | [-0.02, -0.0025] | upper <= 0.05 | PASS |
| W1_L | -0.0625 | [-0.0875, -0.04] | upper <= 0.05 | PASS |
| T3_L | -0.03 | [-0.0475, -0.015] | upper <= 0.05 | PASS |
| W1_D_other | 1.415 | [1.0475, 1.8000625] | lower >= -6 | PASS |

## Full-sample observations

| Condition | Arm | Rows | Any whiff | Any reach | Valued dwell majority | Lost last 200 | Ever engaged |
|---|---|---:|---:|---:|---:|---:|---:|
| C0 | Fly | 400 | 0 | 0 | 0 | 400 | 0 |
| C0 | GS250 | 400 | 324 | 270 | 139 | 76 | 400 |
| C0 | GSOff | 400 | 0 | 0 | 0 | 400 | 0 |
| C0 | Passive | 400 | 0 | 0 | 0 | 400 | 0 |
| C0 | Agent17 | 400 | 0 | 0 | 0 | 400 | 0 |
| T1 | Fly | 400 | 400 | 400 | 374 | 4 | 0 |
| T1 | GS250 | 400 | 400 | 400 | 376 | 0 | 4 |
| T1 | GSOff | 400 | 400 | 400 | 374 | 4 | 0 |
| T1 | Passive | 400 | 400 | 400 | 374 | 4 | 0 |
| T1 | Agent17 | 400 | 400 | 400 | 374 | 4 | 0 |
| W1 | Fly | 400 | 397 | 400 | 58 | 29 | 0 |
| W1 | GS250 | 400 | 400 | 400 | 34 | 4 | 79 |
| W1 | GSOff | 400 | 397 | 400 | 58 | 29 | 0 |
| W1 | Passive | 400 | 397 | 400 | 58 | 29 | 0 |
| W1 | Agent17 | 400 | 397 | 400 | 58 | 29 | 0 |
| T3 | Fly | 400 | 400 | 324 | 294 | 146 | 0 |
| T3 | GS250 | 400 | 400 | 329 | 299 | 134 | 21 |
| T3 | GSOff | 400 | 400 | 324 | 294 | 146 | 0 |
| T3 | Passive | 400 | 400 | 324 | 294 | 146 | 0 |
| T3 | Agent17 | 400 | 400 | 324 | 294 | 146 | 0 |

Conditional recovery windows are descriptive diagnostics and do not replace the full-sample clauses. A horizon is eligible only when m+K <= 599 and uses m+1 through m+K. Conditional n below 50 remains UNREADABLE; n zero remains UNDEFINED. Complete diagnostic readings are retained in metrics.json.

## Implementation and spent H0

The reviewed implementation passed 107 tests across six suites and nineteen source-valid native boundary fixtures. All 112 immutable specification files and the 133-file implementation closure retain their pinned bytes. The runtime uses CPython 3.13.12, NumPy 2.5.3, one process and six numerical thread settings of one, with assertions enabled.

The first spent H0 runner passed its twenty gates, but its independent verifier returned INVALID because inherited native world.start source indices were conflated with positions. That attempt and exact former sources remain in experiments/h17/run3_H0_attempt1. Before the fresh BENCH claim, the correction reconstructed native constructor indices and the archive worklist received byte-equivalent three-way tests. The corrected full spent H0 passed twenty runner gates, independent verification of 86082 arrays and ROOT recomputation of 488 arrays. H0 is VALIDITY_ONLY, with no inference or fresh RNG. MAIN pins bind all five corrected H0 artifacts and the same frozen implementation closure.

## Evidence and provenance

Large identity and raw evidence stay local; the canonical copy of this report supplies their path and AP SHA references. Digest alphabet uses a through p.

| Artifact | AP SHA | Canonical source_doc |
|---|---|---|
| experiments/h17/run3/bench/identity.json | ccljdnpfnafgkhoopcblpccmmjjhjeikpbemgbgoobbjkclokjhpicnljabnigmb | local evidence; cited by this canonical report |
| experiments/h17/run3/bench/metrics.json | pepdomenkhgnbobikdohpoooihloimemlbjmmfmnlmolepnahdmpkfhibakiaeck | d944fe4d7898545d3 |
| experiments/h17/run3/bench/raw.npz.ap | fpcnbmlmdbmfcdjklmbjbgplpaiafdaaaajmedahgjmjebikgnpdianelimofdeg | local evidence; cited by this canonical report |
| experiments/h17/run3/bench/verification.json | pcfkknnbfcidefaicgnebcbljanhhdmanmpicepnkdjpdagkgcojcbcpadhhgjif | dc30750c9210e863f |
| experiments/h17/run3/bench/parent_recomputation.json | ihfkbnifclbdakpokmpaeofgndoecmpfdpoimnpifmnhilpakoapnjlebnehmiba | d97176ee4a5564e85 |
| config/h17-run3-implementation-pins.json | callhhomcelgdnkdjjiijcpnblhdofdpifgcapppclniedkbpamcegkippdmogko | ddfc554ab2f9cda0b |
| config/h17-run3-execution-pins.json | kmlmecemionbinjlgfaiminbefhonppaphdffoncehhcnbcnnihllkioklbojjji | d26e41a82a3c983ee |
| experiments/h17/h17_run3_design_v3.md | oibjjpnikgaejokpgfpfoffoaiapnngnfjcknhfhmbojheoopgnamoimaajjjnmh | d528fa87b2f4f63d2 |
| experiments/h17/h17_run3_implementation_checks.json | igkefhplpioecmgmmfdlgecllgpeoijkmgaacbkblmnjppiplinlafoabldhhlpl | d8dda08311218039c |
| notes/reviews/2026-10-10-h17-run3-execution-review.md | hcecbmbhpcmmgbeoojjhdelecmdfpkjilkkimlfnebojjkmggccemmcpedkichph | d1eb54bbc80ef554b |
| experiments/h17/run3/H0/verification.json | abcoiadjhbhkbkmbnkncgnjgdjnmamegcblabbpbhnacipdlppkelfkladnpabef | d7416abc425ce82f0 |
| experiments/h17/run3/H0/parent_recomputation.json | iocmpaidmkladgnmbgooedjoldnfpjfgobehligliffknocjalahpcolighbgbip | d8543ef69a89133ba |
| experiments/h17/run3_H0_attempt1/H0/verification.json | ialokkplnohaigjlkifgfjojabpgdagndenjfaiplhjelkjjacmicbpekpfcekef | d475af50c62749fec |

Implementation source closure AP SHA: lkjcbpplkaangopbillnjeibfheenahmjhlfcbhdgpcefngfgkbkgegbdgefcali.

Code citations (each refers to its actual canonical code document):

- src/h17_run3_arm.py; AP SHA kedhfjfpjnnkaigdldnkgjjikifimhjoegmbpmjninfifooidolfechelmacpfof; source_doc d5689184eb372a917.
- tools/h17_run3_recording.py; AP SHA ihcdgdkdeaacekdkeklbnfjkcojafnolbmmgmgmabhcmofeonnepimmcpgahecek; source_doc d6ab331647626ea85.
- tools/h17_run3_archive_candidate.py; AP SHA gfnemcogleknlidonafbijpclgijpiabggjhcppippmidpbabhoibihgeibhhjcb; source_doc df3c308389e413f45.
- tools/measure_h17_run3.py; AP SHA ooinaeikokkfhaocoolnalnpefadenkmifjggajkfjcedijibaoaejnilbdpcdoa; source_doc d691f73466e633a55.
- tools/verify_h17_run3.py; AP SHA hkkdlgndgbdlibbpikiikcihajiophpgckhiomgfkfffeikejehanjlidbfjboig; source_doc d7b2a2a78d3cf7804.
- tools/recompute_h17_run3.py; AP SHA haaalnghjmjceomomehhopkdjngmibnhjoepheonfngpbenfghebhplmmhblcgel; source_doc dfdfec29696ecb89b.
- tools/check_h17_run3_boundaries.py; AP SHA blfolcpkpaidoelkhgljhiocdlfkpfionklbhmafdngdgbcfifodnbfglkpellli; source_doc db6383e79ccce71b2.

## Interpretation and next gate

This PASS establishes the fixed engineering question under C0/T1/W1/T3 with supplied values, learning off, two channels and the original World7 wind law. C0 is the specified constructed stress condition. It is not a general fly-behavior forecast or a production adoption decision. Native Fly/N2 behavior, the historical H17 disposition, hold D0 UNRESOLVED, A5/B3 stops and E1 branch-screen limits retain their existing status.

DEV remains behind its separate owner gate. Under Run3 v3, DEV requires this saved all-PASS BENCH verification and its own exclusive pair; its required outcome is operation PASS with complete fixed-sample evidence and validity verification. EVAL requires a separate owner gate, DEV operation PASS and its own exclusive pair. Neither stage has been opened or executed here. No adoption, commit, push, merge or deployment is included.

The original R2 scanner passed the earlier 661-file inventory with exactly the existing 42 protected-token pairs and no unused or error rows. That full inventory receipt is historical; it is not represented as a rescan of the expanded final tree. New implementation/report bytes are checked with the unchanged original protected-token guard, with no new exception.
