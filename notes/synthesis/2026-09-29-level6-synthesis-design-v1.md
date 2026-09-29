# Level 6 synthesis, design v1 DRAFT: what will be compared with the fly, how a match is judged, what counts as a source

Date 2026-09-29. **Status: v1 DRAFT by an Opus 5.5 agent, for the owner's confirmation. Not an owner decision; nothing
here is registered until a v2 FINAL is confirmed.** Opened by decision:level6-synthesis-open-design (the owner's '그럼
다음 이어서 권고안으로 진행', gloss 'then continue with the next item as recommended'): item (c) of the consolidation
gate (notes/consolidation/2026-09-29-consolidation-v2.md section 8; order recorded at master_plan.md:1116-1117).

Citation convention. `master_plan.md:N` is a line of master_plan.md at commit 112c1fe. Graph-only documents are cited
by file name and line as fetched to the session scratchpad (`phase6_synthesis.md` = graph doc d1b7d628aa91fb211,
`phase1_report.md` = graph doc d1bc7b5a05a8c84ef, `phase7_1_report.md` = graph doc d44b3156fa127b325). Output files are cited by repository path and line. Sources are
marked **(i)** already in the record, cited as recorded, or **(ii)** verified now: the PubMed record (title, authors,
venue, abstract) was opened on 2026-09-29 through NCBI E-utilities and the claim below was read in that abstract. For
(ii) only the abstract was read (the publisher pages returned an error or 403); nothing is claimed from figures.

## 0. Status, scope, and what a Level 6 synthesis is here

- **What it is.** The written comparison Phase 6 defines (master_plan.md:1165-1168): 6.1 the adopted agents compared
  qualitatively with published fly behaviour; plus a circuit-link table in the Phase 1 form (phase1_report.md:6-40) for
  the modules adopted after Phase 4; plus 6.2 in reading form (section 4), with no ladder rerun.
- **What this file is.** The SPEC of that synthesis: the comparison set, the judging rules, the source rule and the
  success criteria, to be registered before the synthesis is written, as record:phase6-success-criteria was stored
  before the Phase 6 ladder was built (phase6_synthesis.md:4).
- **What it is not.** No run, no code, no seed, no adoption, no new hypothesis, no change to any verdict or to the
  adopted architecture. The synthesis may list candidates for the queue (section 5, C8); it decides nothing.
- **Which agent.** Both adopted forms (master_plan.md:2111-2129): Agent17, the two-channel adopted agent, and Agent16,
  the three-channel distractor form. Each row of section 2 names the form its agent number comes from. Where a number
  comes from a lineage agent (Agent14, Agent14N2, H15 Run 2's agent) that is said, with the adopting decision that
  carries it forward.

## 1. The baseline, and what has changed since Phase 6

### 1.1 What Phase 6 compared (2026-09-19)

Six behaviours, three matched and three not (phase6_synthesis.md:98-110; record:phase6-behaviour-comparison):

| # | Behaviour | Phase 6 verdict | Sources as recorded (i) |
|---|---|---|---|
| P1 | aversive conditioning: acquisition, reversal, timing-dependent sign | MATCHED, 200 of 200 | Hige et al 2015; Handler et al 2019 |
| P2 | sparse odour coding at about 5 percent of Kenyon cells | MATCHED, by construction | Turner et al 2008; Lin et al 2014 |
| P3 | heading memory persisting in darkness and drifting | MATCHED after the noise calibration | Seelig and Jayaraman 2015; Kim et al 2017 |
| P4 | extinction | MISMATCHED | Felsenberg et al 2018, Cell |
| P5 | plume navigation | MISMATCHED | Alvarez-Salvado et al 2018; van Breugel and Dickinson 2014; Demir et al 2020; Kadakia et al 2022 |
| P6 | releasing a committed choice | MISMATCHED | Kim et al 2017 |

The one bias (concept:discrete-vs-graded-bias; phase6_synthesis.md:11-19): the model takes the discrete or destructive
version of a mechanism the fly implements gradedly or additively. Three rows: holding a choice (latch vs graded
attractor), extinction (erasing vs parallel opposing trace), navigation (gradient climbing vs encounter timing against
a wind reference).

### 1.2 Modules adopted after Phase 4 that Phase 6 did not cover

From the consolidated record 2.2 (master_plan.md:1991-2009). One measured number each, with its line.

| # | Module | Adopting decision | One measured number | Cited at |
|---|---|---|---|---|
| M1 | Extinction GATE on H8 v2 (learning) | decision:phase7-2-gate | sustained pairing retains 100.0 percent against 0.3 without the gate | experiments/h11/ph8_h11.txt:31-32 |
| M1' | its later reading | (a reading, no decision) | with the gate on, extinction has never fired in any recorded behaving run | master_plan.md:2249-2251 |
| M2 | Heading ring, RingExact tau 1, sigma 0.5, n 16 | decision:h14-adopt-tau1 | drift 1.39 degrees over 1000 dark steps against the restated bound 4.3 | experiments/h14/ph10_adopt.txt:7, :14 |
| M3 | Ring input contract: the rotation made | decision:heading-input-rotation-made | heading error over 45 degrees 4.30 -> 0.00 percent, cue on every step | master_plan.md:56-57 |
| M4 | Return cast (surge-and-cast on a wind reference) | decision:h16-close-limited-adoption | 23.7 against a random walk's 0.0, late unrecovered 0.0 percent, 160x160 | master_plan.md:42-43 |
| M5 | H19 (a): a non-negative whiff reaches navigation while nothing is held | decision:h19a-adopt-and-run2-direction | late unrecovered 10.5 -> 0.0 percent with neutral valence | master_plan.md:75 |
| M6 | Value gain G 2 | **none in the record; adopted status unsettled** (master_plan.md:1971-1973, 1998) | first hold on the valued odour 277 of 400 against 200 without it | master_plan.md:2216-2217 |
| M7 | H21 gate | decision:h21-gate-adopted-within-tested-conditions (verdict NOT shown) | P(V) 0.750 against 0.570 without it | master_plan.md:2230 |
| M8 | Release: H25 (S)+(Z) at +1/0, then N2 (off at negative held values) | decision:h25-release-adopted-within-tested-conditions; decision:n2-release-adopted-within-tested-conditions | R-start rows visiting the not-yet-learned punisher 8 against 56 of 200 | master_plan.md:687-688 |
| M9 | H23 value filter | decision:h23-filter-adopted-within-tested-conditions | P(V) 381/400 = 0.953 | master_plan.md:338 |
| M10 | Presence counter with its 59-step PRIOR; window 200 for the two-channel form | decision:h26-adaptive-presence-adopted-within-tested-conditions; decision:h29-window-200-adopted-within-tested-conditions | W1 dwell 23.8 against Agent10's 12.3; T3b paired dwell +1.9525 against Agent14N2 | master_plan.md:2316; :2119-2120 |
| M11 | Three-channel additions: H27 composition rule, three counters, H28 burst-ranked tie | decision:h28-burst-tie-adopted-within-tested-conditions | W1D 222 against 400 rows lost (29 without D) | master_plan.md:801-802 |
| M12 | Flee: a held negative odour drives it and overrides | none separate; part of the adopted act (master_plan.md:2007) | 0 flee violations over 37,414 and 40,000 negative-held steps | master_plan.md:209 |
| M13 | Learning loop: one update per agent per world step | from H15 Run 2; no separate decision id (master_plan.md:2009) | a negative value of -0.89 from one natural visit of about 7 steps | master_plan.md:2265 |

The synthesis restates M6's status as 'unsettled' and does not treat it as adopted or as not adopted.

## 2. Registered comparison set (6.1)

### 2.1 Judging rules, written now

| Verdict | Rule |
|---|---|
| MATCH | a measured agent number exists in a condition that is the fly finding's condition in kind (the same stimulus event: odour onset, odour loss, cue absence, repeated unreinforced exposure, and so on), inside the adopted scope of the form named, and the agent's behaviour has the qualitative shape the source reports. Qualitative only: no magnitude, time constant or rate is compared. |
| MISMATCH | a measured agent number exists in that condition, inside the adopted scope, and its qualitative shape differs from the source's; or the behaviour the source reports is produced by the agent through a mechanism of a different kind, stated as a mechanism mismatch and kept apart from the behavioural verdict. |
| UNTESTED | the adopted scope covers the condition, but no agent measurement exists in it (for example, a supplied value where the fly finding concerns a learned one). |
| OUTSIDE SCOPE | the adopted scope excludes the condition; the recorded limit L-number (master_plan.md:2081-2105) is cited, and any agent number in that condition is reported as the limit's number, not as a verdict. |
| PENDING | no source could be verified: 'needs a source'. Not a verdict; the row is carried open. |

Additional rules: a number from a lineage agent counts only if the adopting decision that carries it to the named form
is cited; a module-level (bench) number is labelled 'module level' and can support MATCH only for a row whose fly
finding is itself about the circuit property, not about free behaviour; 'within the tested conditions' is kept on every
verdict; a verdict is never upgraded by combining two rows.

### 2.2 The comparison set

| # | Fly behaviour | Published finding and source | Agent's measured behaviour (form; number; line) | Expected reading, to be judged by 2.1 |
|---|---|---|---|---|
| B1 | Upwind surge on odour contact, with a wind reference | (ii) Alvarez-Salvado et al 2018, eLife 7:e37815, doi 10.7554/eLife.37815: odour evokes 'an upwind run during odor (ON response)'; wind orientation requires antennal mechanoreceptors. (ii) van Breugel and Dickinson 2014, Curr Biol 24:274-286, doi 10.1016/j.cub.2013.12.023: 190 +/- 75 ms after encountering a plume flies increase flight speed and turn upwind, using visual cues for wind direction | Agent17 lineage (M4): surge-and-cast against the gradient rule in the plume 29.0 vs 0.0, wins 81.5 percent (experiments/h13/ph9_h13.txt:25); return rule 23.7 vs random walk 0.0 (master_plan.md:42-43) | MATCH candidate, within 'heading information every step, low boundary influence' (master_plan.md:2277-2279) |
| B2 | Search after the odour is lost, and reacquisition | (ii) van Breugel and Dickinson 2014 (above): 450 +/- 165 ms after losing the plume flies begin vertical and horizontal casts, holding a crosswind heading. (ii) Alvarez-Salvado et al 2018: 'a local search at odor offset (OFF response)', 'search is driven solely by odor' | M4: late unrecovered 0.0 percent, reacquisition 153 steps median (master_plan.md:43); M5: 10.5 -> 0.0 percent (master_plan.md:75). Loss after tracking (T3b) at t0 150 only (L5, master_plan.md:2091) | MATCH candidate for the presence of a loss-triggered search; the agent's search is a crosswind triangle cast, the walking fly's is a local search: the synthesis states the form difference |
| B3 | Navigation in a plume whose encounters are random in space and time | (ii) Demir et al 2020, eLife 9:e57524, doi 10.7554/eLife.57524: turns are stochastic saccades 'whose direction was biased upwind by the timing of prior odor encounters'; the digest states this is a different strategy from surge and cast, which the flies use for regular streams | the agent's rule is a deterministic surge per whiff with a cast clock (M4, M5); the encounter-frequency variant did not beat the plain cast, 28.0 vs 29.0 (experiments/h13/ph9_h13.txt:26); no recorded measurement of turn direction against encounter timing | UNTESTED for the behavioural statistic; a mechanism MISMATCH stated apart (section 4, row 3) |
| B4 | Behaviour when the wind cue is lost | (ii) Alvarez-Salvado et al 2018: wind orientation needs antennal mechanoreceptors while search is odour-driven. (ii) Okubo et al 2020, Neuron 107:924-940, doi 10.1016/j.neuron.2020.06.022: the compass is linked to wind direction and also incorporates visual cues; that it 'should enable navigation' when no single cue is reliable is the authors' proposal, not a measured behaviour | L2: with the cue absent 50 steps at a time, 64.5 percent end unrecovered against 0.5 for a perfect integrator (master_plan.md:1086-1087) | OUTSIDE SCOPE (L2; the adopted agent senses the wind every step, master_plan.md:1087-1088) |
| B5 | Heading memory in darkness | (ii) Seelig and Jayaraman 2015, Nature 521:186-191, doi 10.1038/nature14446: the population relies 'on self-motion cues in darkness'; with visual and self-motion cues both absent the orientation is maintained through persistent activity. (i) the darkness correlation 0.3 to 0.95 across animals (phase1_report.md:12) | M2, module level: bump 200/200, drift 1.39 degrees over 1000 dark steps (experiments/h14/ph10_adopt.txt:7) | MATCH candidate at module level (persistence, bounded drift); in the behaving agent see B4 |
| B6 | Heading updated from self-motion | (ii) Turner-Evans et al 2017, eLife 6:e23496, doi 10.7554/eLife.23496: neurons conjunctively encoding heading and angular velocity update the heading representation when the fly turns in darkness. (ii) Green et al 2017, Nature 546:101-106, doi 10.1038/nature22343: shifting neurons are required to track heading in the dark | M2 gain 0.999 to 1.000 (experiments/h14/ph10_adopt.txt:8); M3: 4.30 -> 0.00 percent over 45 degrees, cue on (master_plan.md:56-57) | MATCH candidate at module level; M3 is agent level with the cue on, so it is not a darkness measurement |
| B7 | Learned valence drives approach and avoidance | (ii) Aso et al 2014, eLife 3:e04580, doi 10.7554/eLife.04580: optogenetic activation of MBONs can, by cell type, 'induce repulsion or attraction'; valence encoded by the MBON ensemble biases memory-based action selection | learned negative -0.892 from one visit and leaving the punisher (master_plan.md:99-101, H15 Run 2's agent); learned positive, frozen: learned - sham +0.467 (master_plan.md:590, Agent14); learning on: punisher visits 8 vs 56 of 200 (master_plan.md:687-688, Agent14N2). Saturating learned values only (L17, master_plan.md:2103) | MATCH candidate for both signs within those conditions; supplied-value results (for example 0.953, M9) count as UNTESTED for learning |
| B8 | Aversive conditioning: acquisition, reversal, timing sign | (i) Hige et al 2015; Handler et al 2019, as recorded (phase6_synthesis.md:101-102) | module with the gate: F1 acquisition 200/200, reversal 200/200, timing 200/200 (experiments/h11/ph8_h11.txt:12) | carried: Phase 6 MATCHED; the synthesis checks only that the gate left it unchanged |
| B9 | Extinction | (ii) Felsenberg et al 2018, Cell 175:709-722, doi 10.1016/j.cell.2018.08.021: omission of punishment is remembered as a positive experience; calcium traces for the original aversive memory and a new appetitive extinction memory co-exist in the MBON network; 'parallel competing memories' combine within MBONs | adopted single site: behavioural value -0.727 -> -0.158 with the acquisition site at 22 percent kept (experiments/h11/ph8_h11.txt:15, :32); parallel site held unproven (L11, master_plan.md:2097); extinction never fired in a behaving run (master_plan.md:2249-2251) | MISMATCH at module level carried; in the behaving agent UNTESTED (no measurement in which extinction fires) |
| B10 | Re-learning after extinction | needs a source (the Felsenberg abstract does not report reacquisition) | savings 0.0x in every cell (experiments/h11/ph8_h11.txt:42-45) | PENDING |
| B11 | Discounting a ubiquitous or irrelevant odour | (ii) Das et al 2011, PNAS 108:E646-E654, doi 10.1073/pnas.1106411108: 'prior odorant exposure results in a selective reduction of response to this odorant', arising from glomerulus-selective potentiation of inhibitory synapses in the antennal lobe | Agent16 (M11): background D at p_D 0.03, W1D 222/400 lost against 29 without D (master_plan.md:801-802; L4, master_plan.md:2090); H27's agent 400/400 (master_plan.md:762-763). The agent has no exposure-dependent change of response | three-channel form: MISMATCH only if the synthesis states that W1D is the fly's condition in kind (repeated unreinforced exposure); otherwise UNTESTED; two-channel form OUTSIDE SCOPE (no D, master_plan.md:2089) |
| B12 | Persistence of a committed choice, and its revision | (ii) Kim et al 2017, Science 356:849-853, doi 10.1126/science.aal4835: an artificial bump is maintained 'with naturalistic dynamics'; local excitation and global inhibition enforce a unique persistent representation. (i) locks onto one of two competing stimuli, switches stochastically with low probability, jumps when a stimulus moves, as recorded (phase6_synthesis.md:29-31); not in the abstract, not re-verified | L8: 0 of 319 isolated valued whiffs flipped a neutral hold; every revision via the empty state (master_plan.md:2094); H9 graded substrate revises 200/200 vs 0/200 but is not adopted (master_plan.md:18-20) | MISMATCH carried from P6 unless section 4 finds an adopted module that changed direct revision |
| B13 | Declining to commit on weak evidence | needs a source | bistable circuit abstains 75/200 (phase7_1_report.md:21); graded 0/200 (phase7_1_report.md:103) | PENDING |
| B14 | Sparse odour coding | (i) Turner et al 2008; Lin et al 2014 (phase6_synthesis.md:103-104) | unchanged since Phase 6 | carried: MATCHED by construction, not re-judged |

The writer may add a row only with a (ii) source opened at writing time and the same four columns; an added row is
marked 'added at writing' and cannot change a registered row's verdict.

## 3. Registered circuit-link table (Phase 1 form)

Each row says what the cited work reports and what it does not. 'No anchor' is written as in Phase 1
(phase1_report.md:35-36): no source found, not a weak anchor.

| Module | Candidate fly circuit | Reported by the source | Not reported by the source |
|---|---|---|---|
| M1 extinction gate | MB dopaminergic neurons signalling omission, (ii) Felsenberg et al 2018 | extinction needs specific dopaminergic neurons; omission of punishment acts as a positive experience | a gate that blocks extinction on reinforced steps; the gate's retention under sustained pairing. **No anchor for the gate itself** |
| M1' the later reading | none | | no source on whether fly extinction fires during continuous reinforced exposure; no anchor |
| M2 ring | ellipsoid body E-PG ring, (ii) Seelig and Jayaraman 2015; (ii) Kim et al 2017 | a persistent bump updated by self-motion; local excitation and global inhibition | the exact-kernel form, tau 1, n 16; the Phase 1 caveat on who carries the inhibition stands (phase1_report.md:33) |
| M2 wind coupling (amplitude 6.0) | wind input to the compass, (ii) Okubo et al 2020 | wind direction rotates the compass; wind is combined with visual and self-motion cues | an input amplitude; behaviour after the wind cue is lost |
| M3 rotation made | P-EN type shift neurons, (ii) Turner-Evans et al 2017; (ii) Green et al 2017 | angular velocity from turns updates the heading estimate | whether the signal is the rotation executed or the motor command: the abstracts do not say. Partial |
| M4 return cast | flight casting and walking OFF search, (ii) van Breugel and Dickinson 2014; (ii) Alvarez-Salvado et al 2018 | a search begun after odour loss (crosswind casts in flight; local search in walking) | a triangle wave returning upwind; the cast period; any circuit. Behavioural anchor only, no circuit anchor |
| M5 H19 (a) | ON response, (ii) Alvarez-Salvado et al 2018 | odour onset evokes an upwind run | the condition 'while nothing is held' and 'valence not negative'. Behavioural anchor, partial |
| M6 gain G 2 | none found | | no source searched to verification for a value-dependent gain on odour input; no anchor (not searched is stated as such) |
| M7 H21 gate | MBON ensemble, (ii) Aso et al 2014 | valence in the MBON ensemble biases memory-based action selection | zeroing a lower-valued odour's input while a higher-valued one is held; no anchor for the gate |
| M8 release (H25, N2) | none | | Phase 1's no anchor for a reset (phase1_report.md:35) carries to both release rules; no anchor |
| M9 H23 filter | MBON ensemble, (ii) Aso et al 2014 | valence biases action selection | a top-valued-only rule on the upwind surge. Partial |
| M10 presence counter and its prior | antennal lobe habituation, (ii) Das et al 2011, as a contrast | a response change after prior exposure to an odour | a presence window, a never-sensed odour counted present on steps 0-58; no anchor for the counter |
| M11 three-channel additions | none | | no source for a burst-ranked value tie or the H27 composition rule; no anchor |
| M12 flee | MBONs inducing repulsion, (ii) Aso et al 2014 | activation of some MBON types induces repulsion | an override of every other drive; crosswind flee geometry. Partial |
| M13 learning loop | none | | an implementation property (one update per step); no anchor expected; stated as not a biological claim |

## 4. The abstraction question revisited (6.2 in reading form)

Reading rule, registered: a Phase 6 mismatch is 'moved' only if an adopted module changed the behaviour the fly
comparison reads, and the adopting decision id is cited. A shown result with nothing adopted, a module-level result, or
an adoption that changes a different behaviour does not move it; the row then says 'not moved' and names what was
tested.

| Phase 6 row | Later work, from the record | Expected reading |
|---|---|---|
| 1. holding a choice: latch vs graded attractor | H9: graded substrate revises 200/200 vs 0/200 but cannot abstain, rejected as stated, nothing adopted (master_plan.md:18-20); H10: confidence gate STOPPED at calibration, NOT shown (master_plan.md:956-978); adopted H21 gate, N2 release and H23 filter change maintenance, release and steering, not direct revision (L8, master_plan.md:2094) | not moved; refined: the reset is the price of abstention (phase7_1_report.md:106-107) |
| 2. extinction: erasing vs parallel opposing trace | H11: extinction gate ADOPTED (decision:phase7-2-gate), removing sustained-pairing erasure (retains 100.0 vs 0.3 percent, experiments/h11/ph8_h11.txt:31-32); parallel site held unproven; H12 Package E +0.7350 [0.6925, 0.7775] in a controlled read-out only, MB5 NOT adopted (master_plan.md:920-921, 923-924) | moved for the sustained-exposure erasure (decision:phase7-2-gate); not moved for the parallel trace |
| 3. navigation: gradient climbing vs encounter timing | H13: double dissociation, surge-and-cast 29.0 vs gradient 0.0 in the plume, gradient 539.5 vs 7.0 in the smooth world (experiments/h13/ph9_h13.txt:69-70); return cast ADOPTED (decision:h16-close-limited-adoption) | moved to surge-and-cast on a wind reference, within its scope; B3 records that stochastic timing-biased turning is still not the agent's rule |

The synthesis may add an updated bias table (section 8, point 5) built only from these three readings.

## 5. Success criteria for the synthesis document, stored before it is written

To be stored as record:level6-synthesis-criteria at v2 FINAL, before the synthesis is started.

| # | Criterion | Met when |
|---|---|---|
| C1 | Coverage | every module M1-M13 of 1.2 has a row in section 3 of the synthesis, and every one whose behaviour a fly finding addresses is referenced by a row of section 2; B1-B14 all present |
| C2 | Source quality | every source names authors, year, venue; every (ii) source carries the DOI or URL actually opened and the claim read there; (i) sources cite the record line |
| C3 | Granularity | every circuit link states what is and is not reported, or says 'no anchor' |
| C4 | No verdict upgraded | MATCH only with a measured agent number in the fly's condition in kind, inside the named form's scope; 'within the tested conditions' kept; no recorded verdict (shown, not shown, stopped) restated in stronger words |
| C5 | Numbers | every agent number carries a line citation at 112c1fe and equals the cited line |
| C6 | Open list | an explicit list of every row read UNTESTED, OUTSIDE SCOPE (with its L-number) or PENDING |
| C7 | Section 4 | each Phase 6 mismatch read by the registered rule, with the decision id when 'moved' |
| C8 | Candidates for the queue | a separate section that proposes, ranks and justifies from a row, and decides nothing |
| C9 | Honesty limits | the section 6 limits repeated in the synthesis |

## 6. What the synthesis does not claim

- No fly-level fidelity. A MATCH says the agent shows a behaviour of the same qualitative kind in its own task; it does
  not say the agent behaves like a fly or that its module is the fly's circuit.
- Qualitative only. No timescale, rate, distance or probability is compared with fly data; the agent's numbers are its
  own tasks' numbers, not fly measurements.
- Literature, not primary data: abstracts for (ii), the record for (i); nothing checked against the connectome
  (the limit Phase 1 and Phase 6 recorded, phase1_report.md:70, phase6_synthesis.md:146-147).
- Scope: every verdict is within the tested conditions of the named form; the limits L1-L19 (master_plan.md:2087-2105)
  and the standing rule that a success inside a scope is not read as evidence outside it
  (master_plan.md:2011-2012) apply.
- No module is adopted, rejected or re-judged by a verdict of the synthesis.

## 7. Execution

| Item | Plan |
|---|---|
| Writer | an Opus agent, in the local session (no GitHub Actions), after v2 FINAL is confirmed |
| Checker | the reviewing session: recounts every cited number against its line; opens every (ii) source itself; checks C1-C9 |
| Output | notes/synthesis/2026-09-29-level6-synthesis.md, LF only |
| Graph | mirrored to the Fruit Fly space; result record:level6-synthesis-result; criteria record:level6-synthesis-criteria stored first |
| Runs | none; no seed used or registered |
| Commit | the owner's; nothing is committed by the writer |

## 8. What the owner confirms

| # | Point | Options | RECOMMENDED |
|---|---|---|---|
| 1 | The comparison set | (a) B1-B14 as in 2.2; (b) only the six Phase 6 rows plus B11; (c) (a) plus rows added at writing | (a); rows added at writing only under the 2.2 rule |
| 2 | The source rule | (a) (i) recorded or (ii) verified at writing with DOI/URL, abstracts allowed and labelled; (b) (ii) requires full text | (a); (b) would leave most (ii) rows PENDING since publisher pages refused access today |
| 3 | The judging rules | (a) 2.1 as written, mechanism mismatch kept apart from the behavioural verdict; (b) one combined verdict | (a) |
| 4 | The criteria | (a) C1-C9; (b) C1-C7 only | (a) |
| 5 | An updated bias table | (a) include, built only from section 4's readings; (b) leave Phase 6's table unchanged | (a) |
| 6 | 'Candidates for the queue' | (a) in, proposals only; (b) out | (a); B11 against the queued 'habituation to a ubiquitous odour' (master_plan.md:767-769) is the obvious case |
| 7 | The gain G 2 | (a) carry as 'unsettled' (M6); (b) the owner settles it first | (a); settling it is a separate decision |

## 9. Self-review: the three weakest points

1. **Abstracts only.** Every (ii) claim was read in a PubMed abstract; the digest sentence used in B3 (a different
   strategy from surge and cast) is the eLife plain-language summary, not the results. A full-text reading could
   narrow B1, B3 and B12. The (i) claim in B12 (stochastic switching, jumps) is not in the Kim et al abstract and was
   not re-verified.
2. **'The fly's condition in kind' is a judgement.** B2 (triangle cast vs local search), B7 (supplied vs learned) and
   B11 (background whiffs vs prior exposure) turn on it; the rule narrows it but the writer still decides, and the
   checker must be able to disagree on the stated reason.
3. **Module-level MATCHes.** B5, B6 and B8 would match on bench numbers while the behaving agent has no darkness or
   extinction condition in scope (L2; M1'); read together they could look like more agreement with the fly than the
   agent's behaviour shows. The synthesis must print the 'module level' label beside each.
