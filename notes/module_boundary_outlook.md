# Module boundary outlook: the recognition–value core and the fly body

Date 2026-09-23. **Status: OUTLOOK. Not a decision, not a design, nothing measured here.** Written at the owner's request after two questions ("what is this agent, how does it behave" and "if we modularise it, is it one function") and the owner's correction that the reusable part is how the agent recognises a value when it arrives and how it remembers it, not the navigation. Every number below is quoted from the record; the node and document ids are the sources. Nothing in this note is adopted, and the master plan is not changed by it. Companion note on possible uses outside the project: personal graph, see the episode that records this note.

## 1. The boundary

```
[sensing -> evidence]  ->  [recognition core]  ->  [value memory]  ->  [readout]  ->  [body]
 per-channel events        commit / abstain        credit to what      what to act     surge-and-cast
                                                    is held             on              (fly world only)
```

The project has validated the three middle blocks inside one body, the fly world. The two end blocks are that body's. If the agent is ever reused elsewhere, the module is the middle; the fly body is the first test bed, not the product.

## 2. The core, block by block, with what the record says

### 2.1 Recognition: normalisation + select-and-hold

- Upstream normalisation (ph2.Upstream, Heeger form, exponent 1.5, sigma 0.05, Rmax 1.8, cross-channel k 0.8, tau 2): the amplifier and pulse-stretcher that brings one event into the circuit's input range (one whiff reaches 0.76 of threshold through the stage, 0.10 raw; H19 benches). The master plan carries a WARNING that "whole stage removed" and "cross-channel division removed" are two different controls.
- Select-and-hold (ph2.Circuit: 2 units, theta 1.0, k 12, self-excitation g 2, tau 10, pool tau 2, noise 0.01, S_MAX 5). A hold is one unit above 1.0; with no input it sits near 2.0 and is stable.
- Measured properties:
  - Resists a short distractor 200/200 and abstains 75/200 where a graded circuit abstains 0/200; the reset is the price of abstention (Phase 7.1 report d44b3156fa127b325).
  - Under sparse input a hold is never flipped directly; every revision is a release to nothing-held followed by re-selection from the empty state (record:selection-circuit-revision-via-empty-state; measured twice: H22 diagnosis 156/156 and 123/123, H23 bench (b) 217/217 and 71/71). Under dense valued-only input (p 0.30 for 200 steps) a neutral hold was revised to the valued odour in 400/400 rows (H21 mechanism bench (b), report d4fd6c39f7f81e1ee Appendix B; the route of that revision was not recorded). **The property depends on input statistics.**
  - Re-selection from the empty state is decided by arrival order, biased by the value gain (H20 post-bench diagnosis: 77 of 400 rows formed an unbiased hold before the biased channel's first whiff; record:h20-post-bench-diagnosis-result).
  - The silence timeout fires but rarely ends a hold (H21 evaluation, maintain arm: 4378 firings while held, 2 holds ended — report d4fd6c39f7f81e1ee Appendix A; the bench-level account of the defect is record:silence-timeout-chain-result). A recorded defect, frozen.

### 2.2 Attribution: how a value gets attached when reinforcement arrives

- Value does not arrive as a value. A reinforcement signal arrives and is credited to **what is held at that moment**: the held odour's sparse code (mushroom-body-like, K 500, 5 percent sparse, eta_d 0.10, eta_p 0.30, feedback beta 0.15; Phase 4 adopted design, b4_ph4_run.py.txt) meets the dopamine-like signal and only those synapses change. Recognition (2.1) therefore decides the address of learning.
- Learning update: one per agent per step, with the merging rule and self-checks fixed in the H15 Run 2 specification v4 (dc860b9c7c6f3aa6e); traces tc and tr with tau 5.

### 2.3 Memory: two layers

- Short: the hold itself (fixed point near 2.0 without input); the heading ring (RingExact, n 16, tau 1, sigma 0.5, fed the rotation made; drift 4.3 degrees over 1000 dark steps at noise sd 0.3, the bound restated at the H14 adoption); the cast clock and the silence counter.
- Long: the value weights. Measured: two-sided learning is clean (+0.901 / −0.900, H15 Run 1); the extinction gate removes sustained-exposure erasure (0.3 percent retained becomes 100 percent; Phase 7.2 report d620e2afd6d4b940a); no reacquisition savings (0.0x in every cell, a model with no decay; same report); a parallel storage site preserves a trace that is behaviourally inert (H11, not adopted).

### 2.4 Readout: where stored value touches recognition and action

Three adopted pathways, each within its tested conditions only:
- Gain G 2 on the circuit's input for non-negative values (first selection; H20, G fixed post hoc).
- Gate: while a higher-valued odour is held, a lower-valued non-negative odour's response is removed from the circuit input and the evidence release (decision:h21-gate-adopted-within-tested-conditions; a valued hold never lost, 0/280).
- Filter: the upwind surge follows the top-valued odour in the read-out (decision:h23-filter-adopted-within-tested-conditions; P(V) 0.953 against the known-answer 0.965). Its scope is open under H24 (option v, presence-scoped v_max) after the absent-odour check (record:absent-odour-check-result: reach kept 0.860, dwell 8 against 25, upwind drift).

## 3. Body-specific (not part of the core)

- The plume statistics: whiff probability 0.30 exp(−d_along/12) inside a cone, 0.057 per plume at the task start; events, not concentrations.
- Surge-and-cast with the return cast (CAST_PERIOD 30, MAXOFF 170, triangle wave saturating at 141.7 steps), adopted for low-boundary, cue-every-step tracking and reacquisition only (H16 limited adoption); cold start weak (52 percent), walls absorb it in small arenas.
- H19 (a): with nothing held, any non-negative whiff counts for navigation (now narrowed by the filter when values differ).
- The ring's input contract: fed the rotation made, not the rotation commanded (heading error over 45 degrees 4.30 → 0.00 percent).
- The flee: a held negative odour drives a crosswind flee target that overrides everything (0 violations in every run).

## 4. Interface sketch (not built)

```python
core = fly.Core(seed=1)                      # recognition circuit + value memory
rec  = core.perceive(evidence=[0.0, 0.8])    # what is held: 0 / 1 / nothing
core.reinforce(+1)                           # credited to what is held; extinction gate applies
v    = core.readout()                        # value per item -> what to act on
turn = flybody.step(rec, v, wind, rotation_made)   # the fly body; the replaceable part
```

`evidence` is today "whiff per channel per step". Anything that arrives as a stream of per-item events could stand in that slot; whether the core behaves the same is the question of section 5.

## 5. The caveat that bounds every reuse

The core's measured properties hold under the fly world's input statistics: sparse events, 0.057 to 0.30 per step per channel, mostly one channel at a time. Under dense input the same circuit revised a hold within 200 steps in 400/400 rows (route not recorded). So a new body means a new input contract, benched before use — exactly what the ring needed ("fed the rotation made"). The constants are adopted values that passed benches, not free parameters; exposing them as arguments re-opens those benches. What a module would expose: the values (or the learning switch), the seed, and one tick-to-time scale.

## 6. When and how a module would be built

- Not now. No caller exists; inside the project the phN import chain (ph21 → ph19 → ph16 → ph14 → ph2) is the reproducible artefact, and H24 and Stage B may still change the filter's scope.
- When a caller exists: fold the chain into one file at the adopted constants; **acceptance = bitwise identity** with ph21.Agent8 (positions, headings, circuit states) on the same seeds over 600 steps, the M3-style check every hypothesis has used; the header names the decisions implemented (gate, filter, and the H24 outcome), so the module can be dated against the record.

## 7. What the project still has to show about the core itself

The end-to-end chain "reinforcement arrives → credited to the held odour → later read out → the agent goes there" has not run in one body: learning was validated in H15, readout in H20–H23, separately. H20 Stage B is that chain. H24 stands in front of it because a filter that removes a zero-valued odour from navigation also removes the chance to attach a value to it (the two-source check already found natural exposure to both sources insufficient, 17.5 percent).

## Addendum 2026-09-29 (consolidation gate, decision:consolidation-gate-closed)

The acceptance target in section 5 ('bitwise identity with ph21.Agent8') predates the later adoptions. The adopted
agents are now Agent17 (two-channel, src/ph35.py:104-105) and Agent16 (three-channel distractor form, src/ph33.py:180);
a module built from this outlook would be accepted by bitwise identity with those, on the same seeds, over 600 steps.
The text above is unchanged.
