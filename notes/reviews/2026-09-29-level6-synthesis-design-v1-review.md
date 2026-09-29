# Review of the Level 6 synthesis design v1 DRAFT (2026-09-29)

Reviewer: the reviewing session (Fable). Draft: notes/synthesis/2026-09-29-level6-synthesis-design-v1.md, sha256 1947889bb91e83f20e1a5fc2ebfcab0207cb8d5b738b0a0802debff353aa19be, 213 lines, by an Opus 5.5 agent on the owner's '그럼 다음 이어서 권고안으로 진행' (decision:level6-synthesis-open-design). This is a review, not a decision; the owner confirms by the draft's section 8.

## Verified

- **Numbers.** Every number in sections 1 to 4 that comes from the record was checked against the line it cites (master_plan.md at 112c1fe, experiments/h11/ph8_h11.txt, experiments/h14/ph10_adopt.txt, the graph-only Phase 7.1 report): 89 numbers scanned; the 31 not found near a master_plan line are literature numbers (years, volumes, page and millisecond values from the sources) or numbers cited to the experiment files, and those were opened and match (for example -0.727 -> -0.158 and 22 percent at ph8_h11.txt:15, 100.0 against 0.3 percent at :31-32, savings 0.0x at :42-45, gain 0.999-1.000 at ph10_adopt.txt:8, abstain 75 of 200 and 0 of 200 in the Phase 7.1 report). T3b +1.9525 is at master_plan.md:2119-2120 as cited.
- **Sources marked (ii).** Six of the eleven were resolved by DOI through Crossref in this review, and title, first author, journal, year and volume match the draft: Kim 2017 Science 356:849-853; Demir 2020 eLife 9; Felsenberg 2018 Cell 175:709-722; Das 2011 PNAS 108; Okubo 2020 Neuron 107:924-940; Alvarez-Salvado 2018 eLife 7. The other five (Seelig and Jayaraman 2015, Turner-Evans 2017, Green 2017, Aso 2014, van Breugel and Dickinson 2014) are resolved the same way when the synthesis is written (criterion C2).
- **Source rule.** The (ii) claims rest on PubMed abstracts and, for Demir 2020, its digest; the draft says so in every row and in section 8 point 2. Acceptable for a qualitative comparison as long as the label stays on the row.
- **Judging rules (2.1).** MATCH needs an agent number in the fly's condition in kind and inside the adopted scope; a module-level number can support MATCH only for a circuit-property row; mechanism mismatch is kept apart from the behavioural verdict; verdicts are never combined. This is stricter than Phase 6's comparison and consistent with the standing rules.
- **Wording.** No 'structurally impossible', no 'for any', no verdict upgraded; 'within the tested conditions' is kept; B10 and B13 are honestly PENDING.

## Amendments recommended for v2 (small)

1. **C2, source quality.** Add: every (ii) DOI is resolved by the checker through Crossref (or the publisher) at checking time, and the abstract text actually read is stored beside the synthesis (a short quote per source), so the claim can be re-read without the network.
2. **B4.** The fly finding cited is about the requirement for wind mechanoreception and the compass's use of wind, not about behaviour after a cue loss; keep the row OUTSIDE SCOPE (L2) as drafted, but state in the row that the fly side is 'no measured behaviour under cue loss found; the row reports the agent's limit only'.
3. **B12, the Kim 2017 (i) claim** (stochastic switching, jumps when a stimulus moves) was carried from Phase 6 and not re-verified in the abstract; mark it (i) as the draft does and add 'from the Phase 6 reading, not re-verified at abstract level'.
4. **Section 7, execution.** Name the checker's recount as the same three-part check used here (record numbers against lines, experiment-file citations opened, DOIs resolved), and that the synthesis is committed only after it.

## Not changed

The comparison set B1-B14, the circuit-link table, the reading rule of section 4, the criteria C1-C9, the 'candidates for the queue' section as proposals only, and G 2 carried as unsettled. If the owner confirms section 8 as recommended with amendments 1-4, v2 FINAL differs from v1 only in those points and the status and confirmation text.
