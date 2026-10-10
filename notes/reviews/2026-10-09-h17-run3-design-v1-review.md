# H17 Run 3 draft review and hold disposition check

Date: 2026-10-09. Status: COMPLETE; v1 DRAFT review clear.
Scope: existing evidence and source reading only. No simulation, trajectory,
fresh random draw, controller implementation or seed registration.

## Findings and decisions

The owner authorized the recommended sequence with "해당 순서로 작업 진행":
operational hold follow-up deferral, then H17 Run 3 draft. The separate hold
disposition retains D0 UNRESOLVED, coverage's bench stops and E1's reached/
below-screen verdict. Nothing is adopted and no additional hold run is opened.

The current Fly/N2 baseline changes the relevance of the historical H17
failure. src/fly.py:277-290 withholds negative sustain and formation reset;
ordinary timeout requests, evidence resets and circuit evolution still exist.
The old N1 sustained-negative-release stranding route is not assumed to
persist, and absence of that route is not absence of all losses.

The stored Run 1/2 bench and diagnosis values were checked against their TXT
sources. First-leg toward/away differences are an association in the old
population, not a tested intervention. The draft therefore proposes passive
R0 on current Fly before choosing a performance candidate, with fresh seed
and execution gates left unopened.

## Review correction and validation

A first draft used "distance at most 3" for reach. The reviewer identified
World7's strict distance < HIT_R convention (src/ph11.py:102-103). It was
corrected to "strictly less than 3 after the move" before canonical design
registration. This is a draft-reading correction, not an execution error.
No draft condition, completed experiment or historical bar was changed.

Root independently confirmed the exact owner quote in both UTF-8 files using
Unicode escapes and ASCII JSON output. Garbled PowerShell display was not a
file defect. Protected seed-token checks pass on the disposition and draft;
reference source/downstream pins and the R2 manifest are unchanged.

## Final read-only review

An independent reviewer found no remaining source, mathematical or scope
blocker after the strict reach correction. The review covers current N2
qualification, historical/current separation, independent C0 construction,
constructor-counter preservation, raw masked-draw order, full identity,
all-assigned versus conditional denominators, undefined zero denominators,
readability limits, P1-P5, loop anchors and no revival of lapsed relaxations.

The review performed no simulation, edits or random draws. The two source
audits likewise used saved evidence and read-only code inspection. Canonical
document hashes, master mirrors, graph read-backs and final seed-scan results
are recorded in experiments/hold/hold_followup_h17_design_checks.json.

## Disposition

Reviewed H17 Run 3 v1 remains DRAFT, execution not opened. No candidate is
selected. The next recommendation is a separately finalized passive R0
measurement specification and its own registration/execution decision.
Historical H17 remains closed; the new design does not re-judge it.
