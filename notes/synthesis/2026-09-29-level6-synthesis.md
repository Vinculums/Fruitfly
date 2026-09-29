# Level 6 synthesis, 2026-09-29: the adopted agents against published fly behaviour

Written against design v2 FINAL (decision:level6-synthesis-open; criteria record:level6-synthesis-criteria stored
first). Not yet checked; not recorded until the reviewing session's three-part check.

Design: notes/synthesis/2026-09-29-level6-synthesis-design-v2.md (committed at 157cf47). Sources as read:
notes/synthesis/2026-09-29-level6-sources.md (S1-S13). Written by an Opus 5.5 agent in the local session; no code, no
run, no seed.

Citation convention. `master_plan.md:N` is a line of master_plan.md at commit 157cf47 (HEAD). Output files are cited
by repository path and line. Graph-only reports are cited by the local copies fetched to the session scratchpad
(graphdocs): `phase1_report.md` (graph doc d1bc7b5a05a8c84ef), `phase6_synthesis.md` (d1b7d628aa91fb211),
`phase7_1_report.md` (d44b3156fa127b325). Sources: **(i)** in the record, cited as recorded with the record line;
**(ii)** opened on 2026-09-29, Crossref record and PubMed abstract, entry S-number in the sources file.

Claim labels, on every claim: **[measured]** a number from a run output; **[read]** read from the record or the code as
the record states it, no number measured for it; **[source]** what a published source reports, abstract level;
**[inferred]** this document's own reasoning.

## The one finding worth keeping

Of the three places Phase 6 found the model departing from the fly, one has moved and two have not. Navigation moved:
the adopted agent now surges upwind on an odour whiff against a wind reference and casts after losing it, which is the
fly's behaviour in regular plumes [measured, B1, B2]. Holding a choice and extinction did not move: the adopted
selection circuit still revises only through the empty state [measured, L8], and the adopted learning module still
extinguishes by depressing the trained site, with no opposing trace kept and no spontaneous recovery [measured at module
level, B9, B15] [inferred].

The departure that remains in navigation is a second-order one. In plumes whose encounters are random in space and
time, walking flies turn stochastically with a direction biased by encounter timing, and the source's own summary says
this is not surge and cast (S2) [source]. The agent has only the surge-and-cast rule, and no measurement of turn
direction against encounter timing exists [read, B3].

Everything the agent matches here is matched within its tested conditions, mostly with the wind sensed on every step.
Where the fly's condition lies outside the adopted scope (loss of the wind cue), the agent's number is a recorded
limit, not a verdict [read, B4, L2].

## 1. What was compared

The comparison set is B1-B14 as registered (design v2 2.2), plus one row added at writing (B15) under the 2.2 rule.
The judging rules are design v2 2.1, applied as written:

- MATCH: a measured agent number in the fly finding's condition in kind, inside the named form's adopted scope, with
  the qualitative shape the source reports. Qualitative only.
- MISMATCH: as MATCH but a different shape; a mechanism mismatch is stated apart from the behavioural verdict.
- UNTESTED: the scope covers the condition but no agent measurement exists in it.
- OUTSIDE SCOPE: the adopted scope excludes the condition; the L-number (master_plan.md:2102-2126) is cited.
- PENDING: no source could be verified.
- A module-level number is labelled 'module level' and supports MATCH only for a circuit-property row. A lineage
  agent's number counts only with the decision that carries it. No verdict combines two rows.

The two adopted forms (master_plan.md:2132-2150): **Agent17**, the two-channel adopted agent (supplied +1/0, G 2, C0,
gate on, N2, learning off, World7 T1, W1, T3a, T3b at t0 150), and **Agent16**, the three-channel distractor form
(adds D at value 0, p_D 0.03; T1D and W1D) [read]. G 2 is carried in both scopes with no adopting decision; whether it
is adopted state is unsettled (master_plan.md:1992-1994, 2019) [read]. This synthesis treats it as neither adopted nor
not adopted.

## 2. The comparison (6.1)

Every verdict below holds within the tested conditions of the form named.

| # | Fly behaviour | Source's claim | Agent (form; number; citation) | Verdict |
|---|---|---|---|---|
| B1 | Upwind surge on odour contact, with a wind reference | (ii) S1: odour evokes an upwind run during odour (ON response); wind orientation needs antennal mechanoreceptors. (ii) S6: about 190 ms after a plume encounter flies speed up and turn upwind [source] | navigation module of Agent17, adopted by decision:h16-close-limited-adoption, measured in H16 Run 2: return rule last-third median 23.7, late unrecovered 0.0 percent (experiments/h16/ph12b_h16r2.txt:24), against the control 0.0, wins 97.5 percent (:133) [measured]; the surge on a whiff with the wind sensed is the rule itself [read] | **MATCH** within the tested conditions (heading information every step, little boundary influence, a plume already entered; master_plan.md:2298-2300) |
| B2 | Search after losing the odour, and reacquisition | (ii) S6: about 450 ms after losing the plume flies begin vertical and horizontal casts, holding a crosswind heading. (ii) S1: a local search at odour offset, driven by odour alone [source] | same module: 5834 loss events, 99.6 percent recovered, reacquisition median 153 steps (experiments/h16/ph12b_h16r2.txt:32) [measured]; H19 (a) (decision:h19a-adopt-and-run2-direction): late unrecovered 10.5 -> 0.0 percent (master_plan.md:75) [measured] | **MATCH** within the tested conditions, for a search triggered by odour loss. Form: the agent's crosswind triangle cast resembles the flying fly's crosswind casts more than the walking fly's local search [inferred]. Loss after tracking is shown at T3b t0 150 only (L5, master_plan.md:2112) |
| B3 | Navigation where encounters are random in space and time | (ii) S2: stochastic saccades whose direction is biased upwind by the timing of prior encounters; the digest says this is a strategy other than surge and cast [source] | no measurement of turn direction against encounter timing exists [read]; the H13 encounter-frequency variant did not beat the plain cast, 28.0 vs 29.0, wins 43.5 percent (experiments/h13/ph9_h13.txt:26) [measured], not adopted | **UNTESTED** (behavioural statistic). Mechanism MISMATCH, stated apart: the agent's turn rule is deterministic per whiff [read] |
| B4 | Behaviour when the wind cue is lost | (ii) S1: wind orientation needs antennal mechanoreceptors; (ii) S8: the compass is linked to wind direction and also takes visual cues; its use under unreliable cues is the authors' expectation. No measured behaviour under cue loss found; the row reports the agent's limit only [source] | L2: cue absent 50 steps at a time, 64.5 percent unrecovered against 0.5 for a perfect integrator (master_plan.md:1086-1087) [measured] | **OUTSIDE SCOPE** (L2, master_plan.md:2109; the adopted agent senses the wind every step, master_plan.md:1087-1088) |
| B5 | Heading memory in darkness | (ii) S3: the population relies on self-motion cues in darkness; with no visual or self-motion cue, orientation is kept by persistent activity. (i) darkness correlation 0.3 to 0.95 across animals (phase1_report.md:12) [source] | module level, RingExact n 16, tau 1 (decision:h14-adopt-tau1): bump 200/200, alive 200/200, drift 1.39 degrees over 1000 dark steps against the restated bound 4.3 (experiments/h14/ph10_adopt.txt:7, :14) [measured] | **MATCH, module level** (a circuit-property row: persistence with bounded drift). The behaving agent in the dark is B4 |
| B6 | Heading updated from self-motion | (ii) S9: neurons encoding heading and angular velocity update the compass when the fly turns in darkness. (ii) S10: shifting neurons are needed to track heading in the dark [source] | module level: velocity gain 0.999 to 1.000 at n 16 (experiments/h14/ph10_adopt.txt:8) [measured]; agent level with the cue on, fed the rotation made (decision:heading-input-rotation-made): heading error over 45 degrees 4.30 -> 0.00 percent (master_plan.md:56-57) [measured], not a darkness condition | **MATCH, module level** (circuit property: integration of turns) |
| B7 | Learned valence drives approach and avoidance | (ii) S7: MBON activation induces repulsion or attraction by cell type; valence in the MBON ensemble biases memory-based action selection [source] | negative, learned during behaviour: -0.892 from one visit of about 7 steps and leaving the punisher, H15 Run 2's agent (master_plan.md:99-101) [measured]; positive, learned and frozen: learned - sham +0.467 [+0.415, +0.522], Agent14 (master_plan.md:590) [measured]; learning on: punisher visits 8 vs 56 of 200 R-start rows, Agent14N2 (master_plan.md:687-688) [measured], carried by decision:n2-release-adopted-within-tested-conditions | **MATCH** within the tested conditions for Agent14N2 and Agent14 (saturating learned values only, L17, master_plan.md:2124). For Agent17 with learning on: no measurement [read] |
| B8 | Aversive conditioning: acquisition, reversal, timing sign | (i) Hige et al 2015; Handler et al 2019 (phase6_synthesis.md:101-102) | module level, with the gate: acquisition 200/200 (dA -0.727), reversal 200/200, timing 200/200 (experiments/h11/ph8_h11.txt:12) [measured], identical to the ungated baseline (:6) | **MATCH carried, module level** (Phase 6 MATCHED; the gate left it unchanged) |
| B9 | Extinction | (ii) S5: omission of punishment is remembered as a positive experience; the original aversive memory and a new appetitive extinction memory co-exist in the MBON network and combine in MBONs [source] | module level, adopted gated single site: behavioural value -0.727 -> -0.158, acquisition site 22 percent kept (experiments/h11/ph8_h11.txt:15, :32) [measured]; parallel site held unproven, not adopted (L11, master_plan.md:2118) [read]; extinction has never fired in a recorded behaving run (master_plan.md:2271-2272) [read] | **MISMATCH, module level** (carried). In the behaving agent **UNTESTED** |
| B10 | Re-learning after extinction (savings) | needs a source: searched again at writing (sources file, 'Found at writing'); S5 and S12 do not report reacquisition | module level: savings 0.0x in every H11 cell (experiments/h11/ph8_h11.txt:42-45); adopted arm A0 in H12 Stage 1, REACQ +0.0033, F6 0.03x (experiments/h12/ph36_bench.txt:140) [measured] | **PENDING** |
| B11 | Discounting a ubiquitous or irrelevant odour | (ii) S11: prior exposure to an odorant selectively reduces the response to it, through potentiated inhibition in the antennal lobe [source] | Agent16: background D at p_D 0.03, W1D 222/400 rows lost against 29 without D (master_plan.md:801-802; L4, master_plan.md:2111) [measured]; H27's agent 400/400 (master_plan.md:762-763) [measured]. No measurement of the agent's response to D as a function of prior exposure [read] | three-channel form: **UNTESTED** (see note 1); two-channel form: **OUTSIDE SCOPE** (no D; L3, master_plan.md:2110) |
| B12 | Persistence of a committed choice, and its revision | (ii) S4: an artificial bump is maintained with naturalistic dynamics; local excitation and global inhibition give a unique persistent representation. (i) locks onto one of two competitors, switches stochastically with low probability, jumps when a stimulus moves (phase6_synthesis.md:29-31), from the Phase 6 reading, not re-verified at abstract level [source] | L8: 0 of 319 isolated valued whiffs flipped a neutral hold; every revision went through the empty state (master_plan.md:2115) [measured]; the graded substrate that revises (200/200 vs 0/200, master_plan.md:18-20) was not adopted [read] | **MISMATCH** within the tested conditions, on revision (resting on the (i) claim). Persistence itself is consistent with S4 [inferred] |
| B13 | Declining to commit on weak evidence | (ii) found at writing, S13: in trained odour discriminations, lower contrast lengthens reaction times and lowers accuracy, as in drift-diffusion to a threshold; abstention is not reported [source] | module level: the adopted bistable circuit abstains on 75 of 200 hard-cue trials, the graded one on 0 (phase7_1_report.md:21, :103) [measured]; no reaction-time or abstention measurement in any behaving task [read] | **UNTESTED** (a behavioural row: the module-level number cannot support a verdict here) |
| B14 | Sparse odour coding | (i) Turner et al 2008; Lin et al 2014 (phase6_synthesis.md:103-104) | unchanged since Phase 6 [read] | **MATCH carried** (by construction, not re-judged) |
| B15 | Spontaneous recovery after extinction (**added at writing**) | (ii) found at writing, S12: extinguished reward memory in Drosophila recovers spontaneously, because the extinction memory is actively forgotten [source] | module level, adopted arm A0: spontaneous recovery SR +0.0000 at every silent interval up to D 10000, punishment and reward (experiments/h12/ph36_bench.txt:138-149, :322-333) [measured]; MB5, which does recover, is not adopted (master_plan.md:923-924) [read] | **MISMATCH, module level**. In the behaving agent **UNTESTED** |

Note 1 (B11). The registered rule reads MISMATCH only if W1D is the fly's condition in kind. Das et al measure the
response to an odour after prior exposure to it; W1D measures capture by D during exposure, not whether the response to
D declines with exposure. The two are not the same condition, so the row is UNTESTED [inferred]. No adopted module lowers
the response to an odour with its prior exposure; the presence counters track only steps since an odour was last
sensed, for the filter's top set (master_plan.md:2026) [read]. This is the case section 5 lists first.

Note 2 (B7). The learned-value numbers come from lineage agents. Agent17 differs from Agent14N2 only in the presence
window (master_plan.md:2135-2138) [read]; that it would give the same learning-on result is not measured and is not
claimed.

Note 3 (B15). The row was added under the design's 2.2 rule with a (ii) source opened at writing. It changes no
registered row. It bears on B9 and on H12's parallel design [inferred]: the fly's extinction memory is a separate memory
that decays, which is the property H12 Stage 1 gave MB5 at module level and which the adopted module lacks.

### What remains open

| Reading | Rows |
|---|---|
| UNTESTED | B3 (behavioural statistic), B9 in the behaving agent, B11 (three-channel form), B13, B15 in the behaving agent, B7 for Agent17 with learning on |
| OUTSIDE SCOPE | B4 (L2); B11 two-channel form (L3) |
| PENDING | B10 |

## 3. Circuit links for the modules adopted after Phase 4 (Phase 1 form)

Each row says what the source reports of the module's property and what it does not; 'no anchor' means no source was
found, not a weak anchor (phase1_report.md:35-36).

| Module (adopting decision) | Candidate fly circuit and source | Reported | Not reported |
|---|---|---|---|
| M1 extinction gate (decision:phase7-2-gate) | MB dopaminergic neurons signalling omission; (ii) S5 | extinction needs specific dopaminergic neurons; omission acts as a positive experience; an opposing memory is formed and kept [source] | a gate that blocks extinction on reinforced steps. **No anchor** for the gate itself |
| M1' the later reading, extinction never fires in behaving runs (master_plan.md:2271-2272) | none | | whether fly extinction fires during reinforced exposure. **No anchor** |
| M2 heading ring, RingExact tau 1, n 16 (decision:h14-adopt-tau1) | E-PG ring in the ellipsoid body; (ii) S3, (ii) S4 | a persistent bump updated by self-motion; local excitation and global inhibition [source] | the exact-kernel form, its time constant, ring size; who carries the inhibition is argued (phase1_report.md:33) [read]. Anchored, partial |
| M2 wind coupling, amplitude 6.0 | wind input to the compass; (ii) S8 | wind direction rotates the compass, combined with visual and self-motion cues [source] | an input amplitude; behaviour after wind loss. Anchored, partial |
| M3 fed the rotation made (decision:heading-input-rotation-made) | shift neurons; (ii) S9, (ii) S10 | angular velocity of turns rotates the heading estimate [source] | whether the signal is the executed rotation or the motor command: the abstracts do not say. Anchored, partial |
| M4 return cast (decision:h16-close-limited-adoption) | casting in flight, (ii) S6; OFF search in walking, (ii) S1 | a search that starts after odour loss; crosswind casts in flight [source] | a triangle wave returning upwind, a cast period, any neural circuit. Behavioural anchor only; **no circuit anchor** |
| M5 H19 (a) (decision:h19a-adopt-and-run2-direction) | ON response; (ii) S1 | odour onset evokes an upwind run [source] | the conditions 'nothing held' and 'valence not negative'. Behavioural anchor, partial |
| M6 gain G 2 (no adopting decision; unsettled) | none | | a value-dependent gain on odour input: not searched to verification. **No anchor** |
| M7 H21 gate (decision:h21-gate-adopted-within-tested-conditions) | MBON ensemble; (ii) S7 | valence biases memory-based action selection [source] | zeroing a lower-valued odour while a higher-valued one is held. **No anchor** for the gate |
| M8 release, H25 (S)+(Z), then N2 (decision:h25-release-adopted-within-tested-conditions; decision:n2-release-adopted-within-tested-conditions) | none | | a signal that ends a held state; Phase 1 found none (phase1_report.md:35) [read]. **No anchor** |
| M9 H23 filter (decision:h23-filter-adopted-within-tested-conditions) | MBON ensemble; (ii) S7 | valence biases action selection [source] | a top-valued-only rule on the upwind surge. Partial |
| M10 presence counter and its 59-step prior; window 200 (decision:h26-adaptive-presence-adopted-within-tested-conditions; decision:h29-window-200-adopted-within-tested-conditions) | antennal lobe habituation as a contrast; (ii) S11 | a per-odour response change after prior exposure [source] | a presence window; a never-sensed odour counted present on steps 0-58. **No anchor** for the counter |
| M11 three-channel additions (decision:h28-burst-tie-adopted-within-tested-conditions) | none | | a burst-ranked value tie, the H27 composition rule. **No anchor** |
| M12 flee (no separate decision; master_plan.md:2028) | MBONs inducing repulsion; (ii) S7 | activation of some MBON types induces repulsion [source] | an override of every other drive; a crosswind flee geometry. Partial |
| M13 learning loop (from H15 Run 2; master_plan.md:2030) | none | | an implementation property; stated as no biological claim. **No anchor** |

Reading of the table [inferred]. The adopted body (M2-M5) has behavioural or circuit anchors, partial in every row. The
adopted readout and control (M6-M11) has none beyond the general statement that MBON valence biases action selection:
the gate, the filter, the release, the presence counter and the tie rule are the agent's own engineering. That is the
same place Phase 1 left the reset (phase1_report.md:35), now five modules wide.

## 4. The abstraction question revisited (6.2 in reading form)

Rule, as registered: a Phase 6 mismatch is 'moved' only if an adopted module changed the behaviour the fly comparison
reads, with the decision id.

**Holding a choice: not moved.** The fly comparison reads revision of a committed choice by competing evidence (B12).
H9's graded substrate revises 200/200 against 0/200 but cannot abstain and was not adopted (master_plan.md:18-20)
[measured]; H10's confidence gate stopped at calibration, NOT shown (master_plan.md:956-966) [read]; the adopted gate,
release and filter change maintenance, release and steering, and revision still goes through the empty state (L8,
master_plan.md:2115) [measured]. What changed is the reading: the reset is the price of an abstention threshold
(phase7_1_report.md:106-107) [read].

**Extinction: not moved.** The fly comparison reads an opposing trace kept alongside the original (B9). The adopted
gate (decision:phase7-2-gate) removed a different defect: erasure under sustained reinforced pairing, retention 100.0
against 0.3 percent (experiments/h11/ph8_h11.txt:31-32) [measured]. With the gate alone the acquisition site still
keeps 22 percent after extinction, the erasing form (:32) [measured]. The parallel site was tested twice and not
adopted; Package E +0.7350 [0.6925, 0.7775] was shown in a controlled read-out only (master_plan.md:920-921, 923-924)
[measured, read]. B15 adds that the adopted module shows no spontaneous recovery (SR +0.0000,
experiments/h12/ph36_bench.txt:149) [measured]. The design expected 'moved for the sustained-exposure erasure'; under the
rule that defect is not what the fly comparison reads, so it is recorded as a related repair, not a move [inferred].

**Navigation: moved (decision:h16-close-limited-adoption), within the adopted scope.** Gradient climbing was replaced
by surge-and-cast on a wind reference. H13's double dissociation: in the plume surge-and-cast 29.0 against gradient
0.0; in the smooth world gradient 539.5 against 7.0 (experiments/h13/ph9_h13.txt:69-70) [measured]; the return cast is
adopted (B1, B2). Not moved: encounter-timing-biased stochastic turning in random plumes (B3) [read].

### The bias table, updated from these three readings only

| | the model at Phase 6 | the adopted model now | the fly |
|---|---|---|---|
| holding a choice | bistable latch, needs an external reset | unchanged; a release (N2) added, revision via the empty state only; the reset read as the price of abstention | graded attractor; competition revises it (Phase 6 reading, (i)) |
| extinction | depresses the trace, erases | unchanged form; a gate stops erasure under sustained reinforcement; no spontaneous recovery | an opposing trace kept in parallel (S5), itself forgotten, so the original recovers (S12) |
| navigation | climbs a spatial gradient | surge-and-cast on a wind reference with a return cast, in scope | surge and cast in regular plumes (S1, S6); timing-biased stochastic turns in random ones (S2) |

The bias Phase 6 stated, discrete or destructive where the fly is graded or additive, still describes two of the three
rows [inferred]. Navigation left it by adopting the fly's own regular-plume strategy.

## 5. Candidates for the queue (proposals only; nothing is decided here)

Each follows from a row. Order, opening and scope are the owner's.

| # | Proposal | From | Why | What it would need |
|---|---|---|---|---|
| Q1 | A per-odour exposure-dependent reduction of response in the recognition core (the queued 'habituation to a ubiquitous odour', master_plan.md:767-769) | B11, M10, M11 | the fly's discounting (S11) is exposure-dependent; the agent's is not measured, and L4 leaves 222/400 W1D rows lost | new per-odour state and a signed relaxation (master_plan.md:768-769); a measurement of response against prior exposure first, to make B11 readable |
| Q2 | A behavioural extinction condition: reward withdrawn and a positive competitor (master_plan.md:1821-1823) | B9, B15, M1' | extinction has never fired in a behaving run, so B9 and B15 are module level only | a world change; the adopted module unchanged as the reference arm |
| Q3 | A turn-direction statistic against encounter timing, measured on the adopted agent in a random-encounter plume | B3 | reading only; would make B3 readable before any navigation change | a measurement, no rule change; the H13 frequency variant (experiments/h13/ph9_h13.txt:26) is not this |
| Q4 | A literature item: reacquisition after extinction (savings) in Drosophila | B10 | B10 stays PENDING | a source opened and read; no run |

## 6. What this synthesis does not claim

- No fly-level fidelity. A MATCH says the agent shows a behaviour of the same qualitative kind in its own task; it does
  not say the agent behaves like a fly or that a module is the fly's circuit.
- Qualitative only. No time, rate, distance or probability is compared with fly data; the agent's numbers are its own
  tasks' numbers, not fly measurements. The 190 ms and 450 ms of S6 are quoted as the source's, not compared.
- Literature, not primary data: abstracts for (ii), the record for (i); the Demir point in B3 rests on the eLife
  digest; nothing was checked against the connectome (phase1_report.md:70; phase6_synthesis.md:146-147).
- Scope: every verdict is within the tested conditions of the named form; L1-L19 (master_plan.md:2108-2126) and the
  standing rule that a success inside a scope is not read as evidence outside it (master_plan.md:2032-2033) apply.
- Module-level MATCHes (B5, B6, B8) are about circuit properties; they are not evidence about the behaving agent, whose
  darkness condition is outside scope (B4) and whose extinction never fires (B9).
- No module is adopted, rejected or re-judged by this document; G 2 stays unsettled.

## 7. Criteria (record:level6-synthesis-criteria), answered

| # | Criterion | Answer | Evidence |
|---|---|---|---|
| C1 | Coverage | met | M1-M13 each have a row in section 3 (M1' and the M2 wind coupling as sub-rows); modules a fly finding addresses appear in section 2 (M1: B9, B15; M2: B5; M3: B6; M4: B1, B2; M5: B2; M9, M12: B7 via S7; M10, M11: B11); M6, M7, M8, M13 have no fly finding in 2.2 and say so in section 3; B1-B14 all present, B15 added |
| C2 | Source quality | met, pending the checker | every source names authors, year, venue; S1-S13 each give the DOI, the Crossref and PubMed URLs opened on 2026-09-29 and a verbatim quote (sources file); (i) sources cite the record line; the checker resolves every DOI again (amendment 1) |
| C3 | Granularity | met | every section 3 row has a 'Reported' and a 'Not reported' cell or 'no anchor' |
| C4 | No verdict upgraded | met | each MATCH has a measured agent number in the condition and scope named; module-level rows labelled; 'within the tested conditions' on every verdict; B11 read UNTESTED rather than MISMATCH (note 1); no recorded verdict restated |
| C5 | Numbers | met, pending the checker | every agent number carries a line citation at 157cf47 or a path:line, rechecked at writing |
| C6 | Open list | met | section 2, 'What remains open' |
| C7 | Section 4 | met | the three readings with the rule; decision:h16-close-limited-adoption for the one row moved; the departure from the design's expected reading for extinction stated |
| C8 | Candidates for the queue | met | section 5, Q1-Q4, proposals only |
| C9 | Honesty limits | met | section 6 |

## 8. Corrections and limits of this document

- Quotes in the sources file are kept under 15 words each, shorter than the 40 allowed, with a paraphrase for the rest.
- B10's second search found a spontaneous-recovery source (S12), not a reacquisition source. It was used for an added
  row (B15) and B10 stays PENDING.
- B13's source (S13) reports evidence accumulation to a threshold, not abstention. It moves B13 from PENDING to
  UNTESTED, because the only agent number is module level and the row is behavioural.
- The extinction reading of section 4 departs from the design's expected reading, by the registered rule; stated there.
- The comparison is between the adopted agents' own tasks and abstract-level statements; several rows (B2, B7, B11)
  turn on 'the fly's condition in kind', a judgement the checker may dispute on the stated reasons.
