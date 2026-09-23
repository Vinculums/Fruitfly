# H15 Run 2: experiment specification v3

Date 2026-09-20. **v3 = v2 (doc d8b1e00dd1609fadc) as amended below.** Every section not restated here stands as in v2: 1 question, 2 agent of record and frozen defects, 3 world (400 agents, 200 P-start and 200 R-start by assignment), 4 the two evaluations, 5 arms, 6 measures, 8 seeds. Sections 2.1, 4 (one sentence), 5 (two rows), 7 and the new 7.2, 7.3, 10 are restated in full and replace v2's. The owner recommended the learning-loop change; it is now part of the specification. No code exists.

## 2.1 The learning loop (replaces v2's 2.1)

**Rule.** Every agent's learning state is updated exactly once per world step, after the move, from that agent's own position: the odour code of the source it is within 3.0 of, and that source's reinforcement (compartment 1 for reward, 0 for punishment, magnitude 1), or zeros. **Merging.** If an agent were within 3.0 of both sources in one step, the two codes are combined by elementwise maximum and the two reinforcement vectors are summed, in ONE call. The geometry makes this impossible (sources at least 14 apart), so the rule exists for completeness and a counter reports how often it fired (expected 0). As in Run 1, odour sensed in a plume away from a source is not presented to the learning module. **Frozen learning** means the module is not called: weights and traces are both static.

**Run 1 is kept as the result of the loop it used.** Reproducing its +0.901 and -0.900 is not required.

**Self-checks, none of which looks at a task score.**
1. Independence of the learning state: agent i, given the same input stream, ends with identical weights and traces (to 1e-12) when run alone, inside a population of 50, and inside the same population in permuted order.
2. Decay in time: with no code and no reinforcement, both traces shrink by exactly 1 - 1/5 = 0.8 per world step (tau_code = tau_reinf = 5), so after 10 silent steps they are 0.107 of their value.
3. Exactly once: a call counter equals the number of world steps, in E1 and in each phase of E2; during a frozen test it stays at 0.
4. Independence of whole rows: run the full simulation twice on the same seeds; in the second run one agent is displaced at step 0 (moved onto a source). Every OTHER agent's trajectory, selection state and learning state must be bit-identical in the two runs. Run 1's loop is put through the same test once, for the record; it is expected to fail it, and that is not a requirement on Run 2.
5. Consistency: an agent standing at a source for n consecutive steps gets the same weight change from Run 1's loop and from this one.

## 4, amended sentence: the training dose

E2 training is **a fixed training of 30 CONSECUTIVE reinforced steps at each source**. It is not described as equivalent to any number of natural visits: a natural visit is 6-9 steps, and separated visits are not equivalent to one unbroken stay because the traces decay between them. Bench reference at the agent's learning parameters (ph15_gatebench.py): under the adopted gated rule the learned valence is +-0.500 after 5 consecutive steps and +-1.000 from 10 onward, so 30 steps is a saturating dose.

## 5, amended rows: the gate comparison

| arm | evaluation | question | role |
|---|---|---|---|
| gate replay | E1, offline | the causal effect of the gate on the weights: each agent's recorded input stream from the intact run is replayed into an ungated module with the same initial weights, so both rules receive IDENTICAL sensory and reinforcement input | auxiliary, main gate comparison |
| trained, ungated | E2 training only | the gate's effect at a known continuous exposure of 30 steps; weight level, no test phase | auxiliary |
| ungated learning, free-running | E1 | descriptive only: behaviour and inputs differ between arms, so any high-exposure subgroups are different groups; reported as conditional, never as the gate's causal effect | reported |

## 7. Criteria (replaces v2's 7)

### 7.0 Sampling unit, statistics and uncertainty

**Sampling unit.** One evaluation is 400 rows. Each row is one agent in ITS OWN independently drawn world: its own source positions, start, whiff sequence and noise. So there are 400 worlds with one agent each; nothing random is shared between rows. Sharing a seed across arms pairs row i across arms; it is not the reason rows are treated as independent. That reason is self-check 4 above, and if it fails no interval is computed. Fixed, not random, and shared by every row: all parameters, the distributions the worlds are drawn from, and the odour codes, which are fixed per row index by the odour's identifier and do NOT vary with the seed (rows 0-199 carry the code pairs used in every earlier run). The resampling unit is the row. Conclusions are about variation across worlds and agents drawn from these distributions at these fixed parameters, nothing wider.

**One statistic per criterion, fixed here.** P = a proportion. DP = a difference of proportions over matched rows. GM = a group median. DGM = a difference of two group medians. RGM = a ratio of two group medians. WIN = share of matched rows where arm A is strictly below arm B, ties counting as not wins. No criterion uses the median of per-row paired differences. If a criterion turns out unreadable, for ties or anything else, its statistic is NOT replaced by another afterwards.

**Intervals and outcomes.** P and WIN: Wilson 95 percent. DP, GM, DGM, RGM: percentile bootstrap over rows, 5000 resamples, generator seed 20260920, matched arms resampled together, 95 percent. 'At most t': PASS if the upper bound <= t, FAIL if the lower bound > t. 'At least t': PASS if the lower bound >= t, FAIL if the upper bound < t. Otherwise INCONCLUSIVE. WIN with more than 20 percent exact ties: UNREADABLE. A group under 50 rows: UNREADABLE. Every criterion prints k, n, the point value, the interval and the outcome.

### 7.1 The criteria

**Q1 validity.** E1, all 400 rows, last third. (a) DGM, rewarding dwell, oracle minus random walk, at least 10. (b) GM of dwell at either source for every agent arm, at most 594. (c) DGM, total dwell, intact minus random walk, at least 10. A random walk at 0 is fine: these are differences. Unreadable: never.

**Q2 search maintained while learning.** E1, intact; late unrecovered = no plume whiff in blocks 7-9. (a) P over all 400, at most 0.100. (b) DP, intact minus known valence, in P-start and in R-start separately, at most +0.10. Unreadable: (b) only, if the known arm's own P over all 400 FAILS 'at most 0.100' (the reference is broken).

**Q3 a learned negative valence becomes avoidance.** E1. G3 = P-start rows with at least one punished step in the intact arm; its count and share of 200 are printed and the same rows are used in every arm. (a) GM, learned valence of the punished odour at the end, at most -0.5. (b) GM, last-third punishing dwell, intact, at most 1.0. (c) WIN, intact below no-learning on last-third punishing dwell, at least 0.60; and RGM, intact over no-learning, at most 0.75. Unreadable: G3 under 50; (b) and (c) if the no-learning arm's GM in G3 does not PASS 'at least 10' (both arms at the floor would not show avoidance, and the RGM would divide by a floor); (c)'s WIN on ties.

**Q4 search continues after avoidance.** E1, G3 rows, known-valence arm as the reference on the same rows. (a) DP, share reaching the rewarding source after the first punished step, intact minus known, at least -0.10. (b) RGM, last-third rewarding dwell, intact over known, at least 0.75. Unreadable: G3 under 50; all of Q4 if the known arm's GM of last-third punishing dwell in P-start does not PASS 'at most 1.0' (the reference does not avoid); (b) if the known arm's GM of rewarding dwell does not PASS 'at least 10' (a ratio over a floor).

**Q5 positive valence, weight level only.** E1, G5 = rows with at least one rewarded step (count and share printed). GM, learned valence of the rewarded odour, at least +0.5. No behavioural claim. Unreadable: G5 under 50.

**Q6 controlled experience.** E2 main, all 400 rows, learning frozen, trained against sham on the same rows. Manipulation check: GM of the punished odour's valence before the test at most -0.5 in the trained group, and the sham group's GM between -0.1 and +0.1; otherwise Q6 is UNREADABLE and that is reported as a finding about the dose. (a) RGM, punishing dwell summed over the test, trained over sham, at most 0.5. (b) WIN, trained below sham, at least 0.60. (c) DP, share reaching the rewarding source, trained minus sham, at least +0.25. Unreadable: (a) if the sham group's GM does not PASS 'at least 10 steps'; (b) on ties.

**Q7 integrity.** Regression 710/710; hashes of stored modules unchanged; self-checks 1-5 and the agent check (learning off reproduces the H19 verdict run's `fix` arm) pass.

### 7.2 The gate comparison, auxiliary, tied to the mechanism

What the gate prevents is the erosion of a learned value under CONTINUOUS reinforced exposure. Bench, agent's parameters: gated +-1.000 from 10 consecutive steps onward; ungated peaks at 0.935 at 10 steps, then 0.745 at 25, 0.511 at 50, 0.240 at 100, 0.053 at 200. The two rules do not differ at 10 consecutive steps or fewer and differ by a quarter from 25. A cumulative count says nothing about this, so none is used.
- **Replay (the comparison that isolates the gate).** Rows of G5. RGM of the end value, ungated replay over gated. Printed with it: the distribution of each row's LONGEST run of consecutive rewarded steps, and the same RGM within three strata of that longest run (under 10, 10-24, 25 or more), which are properties of the input stream and therefore identical for both rules. Readings: 'the gate protects the value at the exposures that occurred' if the upper bound is at most 0.80; 'no difference at the exposures that occurred' if the interval lies within 0.95-1.05; anything else 'not discriminated in this run'. If fewer than 50 rows have a longest run of 25 or more, the run does not contain the exposure at which the bench shows the gate to matter, and whatever is found is worded for short stays only. Never 'the gate has no effect'.
- **E2, 30 consecutive steps.** RGM of the absolute pre-test value, trained-ungated over trained-gated, each odour. The bench predicts about 0.70. 'Protects at 30 consecutive steps, as the bench predicts' if the upper bound is at most 0.85.
- The free-running ungated arm is descriptive. Nothing in 7.2 changes a main criterion afterwards.

### 7.3 Verdicts, and what happens when the run does not decide

**Two separate results, neither implying the other.**
- **E1 verdict (Q1-Q4): the integrated-behaviour question.** YES if Q1, Q2, Q3, Q4 all PASS. NO if any FAILS. Otherwise NOT DECIDED BY THIS RUN.
- **E2 result (Q6): does a trained memory drive behaviour when nothing is learned during the test.** PASS, FAIL, INCONCLUSIVE or UNREADABLE on its own. An E1 YES is not reported as establishing E2, nor the reverse.
- Q5 and 7.2 are stated beside them at the weight level.

**Procedure when not decided. It is not 'run again until it passes'.**
- A FAIL is final for this specification.
- UNREADABLE because a baseline is at the floor or a reference is broken cannot be cured by more rows; it needs a changed design with its own registration.
- INCONCLUSIVE, or UNREADABLE only because a group has under 50 rows, with no FAIL: the owner may authorise ONE extension. It is fixed now: the same code, hash-identical, the same specification, 800 rows, new seeds E1 1650/1750 and E2 1651/1751, analysed on its own (not pooled) with 97.5 percent intervals in place of 95, because the question is then being looked at a second time. Its outcome is final for this specification. A second INCONCLUSIVE is reported as 'this design does not decide it'; there is no third run.
- Whether to extend is decided from the printed outcomes alone, before anything else about the run is analysed further.

## 10. Predictions (additions to v2's 9)

Self-check 4 passes for Run 2's loop and fails for Run 1's. Q3(a): one natural first visit of about 8 steps puts the punished odour's value near -0.8 (bench: -0.5 at 5 steps, -1.0 at 10). Replay: most rows' longest run is under 25, so 'not discriminated' or 'no difference at the exposures that occurred'. E2 at 30 consecutive steps: ungated about 0.70 of gated.

## Appendix: ph15_gatebench.py

sha256 d1555ee3a40e86c62039fa32da19e7d161ad158afa892794bdb438f86a98f210, output ph15_gatebench.txt (numbers in 7.2; reward and punishment are mirror images).

```python
#!/usr/bin/env python3
"""Bench evidence for what the extinction gate prevents, at the agent's own learning parameters.

Phase 7.2's probe (ph8.f2_sustained): the odour code and its reinforcement together on EVERY step,
i.e. one unbroken stay at a source. Reported for the gated rule (adopted) and the ungated rule,
for reward (compartment 1) and punishment (compartment 0): the learned valence after n continuous
steps. This ties the gate comparison's readability in H15 Run 2 to CONTINUOUS exposure length,
not to a cumulative count. No task, no score.
"""
import numpy as np
import ph8
from ph8 import MB4, f2_sustained
from ph11 import MB

for comp, name in ((1, "reward"), (0, "punishment")):
    for gated in (True, False):
        make = lambda: MB4(ph8.R, parallel=False, gated=gated, rng=np.random.default_rng(0), **MB)
        peak, final, kept, traj = f2_sustained(make, comp=comp)
        print(f"{name:10s} {'gated  ' if gated else 'ungated'} peak |valence| {peak:5.3f}, after 400 steps {final:5.3f}"
              f" ({kept:5.1f}% of peak) | " + "  ".join(f"n={t}: {v:+.3f}" for t, v in traj))
```
