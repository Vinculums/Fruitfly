# H17 R0 execution review

Date: 2026-10-09. Decision: `decision:h17-r0-open`.

The owner opened the next recommended sequence with “다음 권고 사항 작업 진행”. The opening in `config/h17-r0-execution-opening.json` authorizes implementation and review, public spent-input H0, one durably claimed measurement, and independent recomputation. The immutable measurement contract remains `experiments/h17/h17_r0_design_v2.md`. This review authorizes no candidate, controller relaxation, efficacy threshold, adoption, or follow-up simulation.

## Reviewed implementation

`tools/measure_h17_r0.py` runs C0, T1, W1 and T3, with literal Fly, Passive and literal Agent17 in each condition. Main has 400 rows and 600 steps; public H0 has 40 rows and 600 steps. Conditions and arms use matched constructions. All twelve identity gates must complete before numeric summaries are published.

Literal Fly and Agent17 retain ordinary NumPy Generator handles. Passive alone uses a Generator subclass that calls the original primitive once on the same original BitGenerator and records its arguments, return and before/after states. This creates a second handle, not an additional stream or draw. Literal-arm primitive transcripts are projected from Passive only after exact creation, every RNG checkpoint, full input/return, world state, sample, original output and same-class/lineage state gates. The transcript explicitly records this proof basis. Constructor code, balance, cast and cold geometry streams are retained and named. Temporary log results are cleared each tick.

Class-level base-act and circuit taps call their original methods once and are restored. They capture the base clock and actual gated circuit input without adding controller attributes. Complete Fly/upstream/circuit/ring/learning-module state is recorded at construction, pre-act, base-act, complete-act and bump. The historical A1/A2/A5/A6 lineage fieldsets are fixed; only existing act/bump callables are excluded. Learning is not run. W1 additionally stores the twin's copied position, heading, clock, raw whiffs, wind and walls, along with typed input/return records and generator checkpoints.

`tools/h17_r0_recording.py` preserves native dtype and shape, including scalar arrays and signed zero. It streams a compressed NPZ to disk and encodes bytes with the a-p alphabet. Typed content-addressed blobs contain recursive state without object arrays or pickle. The pinned schema fixes every nonblob array key, dtype and shape template, agent/world fieldsets, event order and recursive blob grammar before fresh streams exist. Original output arrays keep their original dtype. All historical L1 outputs, full source dwell/first/contact/cls3 L3 arrays and the full W1 summary are compared.

`tools/verify_h17_r0.py` imports only standard-library modules and NumPy. It never imports or runs controllers or constructs generators. Source constants are read as data through AST. It independently validates archive hashes and schema, typed state hashes, all twelve coupling gates, construction/draw order, generator continuity, source sensing, upstream/circuit/ring/command equations, original/L3 outputs, N2 masks, markers, strict post-marker windows, anchors, censoring and summary arithmetic. The decoded archive remains on disk; array and blob caches are bounded. Saved construction arrays are compared with initial snapshots and independent construction arithmetic, never overwritten to make them match.

The schema and report define `nav_sourceK` as NAV and delivered-whiff-K concurrence, and `held_nav_sourceK` as NAV and held-K concurrence. Neither count attributes a navigation reset to a source. N2 timeout/evidence concurrence also does not establish a cause.

## Root checks and read-only review

Root ran 34 constructed tests in one local process with six thread settings equal to one: fourteen runner/recording tests and twenty independent-verifier tests. All passed. The tests cover first possible marker at sensing index 249, delivered-only clocks, simultaneous source bits, strict exclusion of marker-step reach, exact window endpoints, late and terminal censoring, no-marker/zero-denominator handling, N2 negative/multiple-unit and base-clock boundaries, signed zero/dtype/scalar preservation, malformed blobs/JSON/archive keys, changed source bytes, phase ordering, saved construction corruption and pair-only claim provenance/reuse prevention.

Root also verified syntax, original R2 source/downstream pins and exact exception manifest, and absence of protected legacy tokens in the new implementation files. The independent verifier's P5 guard rejected every one of the forty-two tokens returned by the two original checkers and accepted a safe AP payload.

The read-only reviewer found no remaining mathematical blocker after correction of scalar-shape storage, bounded draw retention, full historical L3/W1 coverage, saved-construction comparison, registry path, emergency failure preservation and actual executing runtime checks. Clearance remains conditional on spent H0 proving all four conditions and three arms under this exact frozen closure. H0 and the main measurement have not been run at the writing of this pinned review.

## Execution gate and failure rules

Pins include the review, all source files, measurement/recording/verifier/test code, FINAL, opening, registration, seed configuration, historical lineage fixture, R2 checker and unchanged exception manifest. Runtime pins include Python/NumPy versions, executable and native binary hashes, NumPy configuration, byte order, optimization/assertions and all six thread settings. Stable source closure excludes H0 hashes and the pin file itself to avoid a cycle. After independent H0 verification, only H0 evidence hashes are added; the main additionally records the full final pin-file hash.

Before any reserved generator, the runner exclusively creates a pair-only claim in `experiments/h17/r0_registry`. The claim does not depend on an output label and survives failure. Failure receipts retain the first field/index/phase and AP-encoded diagnostic text, with a registry sidecar if the output directory is unwritable. Numeric JSON uses ordinary descriptive counts guarded before writing by strict P5; a coincidental protected token is an actual stop, with raw AP evidence retained. No failed main is automatically retried.

Root will run public H0 and its independent verifier first, preserve the base pins, add verified H0 hashes, perform the original full R2 scan plus final delta checks, and confirm that the registered main claim remains absent. Only then may the one main run begin. Root will independently recalculate saved arrays before recording a result. Identity PASS describes measurement validity; it is not an efficacy or adoption verdict. Existing closures and source behavior remain unchanged.
