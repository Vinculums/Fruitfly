# H15 Run 2: experiment specification v2

Date 2026-09-20. Status: **v2, written after the owner's review of v1. No code exists.** When the owner confirms it, this text is the pre-registration: a change before the evaluation is a recorded amendment, a change after its table is a new run. v1 is kept as h15_run2_spec_v1.md (content hash 66d956bc...).

## 0. Changes from v1

1. The training dose is described correctly. Measured (ph15_visits.py, development seeds): one natural visit delivers a median of 6-9 steps within 3.0 of a source (p90 10-12); the 20-28 I quoted was dwell PER BLOCK, three to four visits. 30 reinforced steps is a fixed dose worth four to five natural visits, and more than three times the single 9-step visit a known-valence agent makes to the punisher. It is not 'one visit'.
2. Training order is assigned evenly, exactly half reward-then-punish and half punish-then-reward, crossed with nothing else. The learned value of both odours is recorded for every agent immediately before the test.
3. Relocation resets the learning module's transient state too: the odour-code trace `tc` and the reinforcement trace `tr` go to zero. Only the weights are kept.
4. E2's MAIN evaluation freezes learning during the test. An E2 with learning left on is an auxiliary condition, reported separately, with no criterion.
5. E2's control is a SHAM-trained group: the same 30 + 30 steps of odour-code presentation at each source in the same order, with zero reinforcement. Both groups are tested with learning frozen from identical test starts.
6. 'Decided by one agent' is replaced by an executable uncertainty rule (section 7.0), with a three-way outcome PASS / FAIL / INCONCLUSIVE.
7. 400 agents, start groups assigned evenly, 200 and 200. Groups defined by what happened in the run are reported with their count and their share of the parent group, and a small count is itself a result. Matched comparisons keep the same agent index across arms.
8. The ungated-learning arm stays, as an auxiliary mechanism comparison with a 'not discriminated in this run' outcome. Nothing it shows changes a main criterion afterwards.
9. 'Baseline at the floor' is defined per comparison. A zero baseline is not a problem in itself; dividing by it, or comparing two groups that are both at the floor, is. Each Q names its own uncomputable and unreadable cases.
10. New, found while reading the learning module for item 3, and needing the owner's confirmation: the learning harness (section 2.1).

## 1. Question

**Does a learned negative valence lead to actual avoidance, and is long-horizon search maintained while it does?**

Claimed at the weight level only: learning of a positive valence (a positive valence has no behavioural effect in this agent). Marked unverified, not tested here: the selection circuit's resistance to a distractor; heading memory under loss of the wind cue.

## 2. The agent of record and the known defects held fixed

ph14.Agent3 with H19 (a) on, imported, not copied: upstream stage ph2.Upstream (n 1.5, sig 0.05, Rmax 1.8, k 0.8); Select-and-Hold ph2.Circuit (n 2, theta 1, k 12, noise 0.01) with its two releases; RingExact as adopted (n 16, tau 1, sigma 0.5, vgain 1), wind cue 6.0 on every step, fed the rotation made; ph8.MB4 gated, parallel site off (K 200, C 4, sparsity 0.05, eta_d 0.10, eta_p 0.30, beta 0.15); return cast, crosswind flee from a held odour of negative valence, wall reflex.

Held fixed, NOT repaired: the silence timeout never releases the hold; a positive valence is behaviourally inert; a whiff of B is ignored while A is held; the ring leaks agents under cue loss (not exercised); a plume is found from an odour-free start about half the time.

### 2.1 The learning harness (a change from Run 1's harness; to be confirmed)

Run 1's loop called the learning module once per source, and only on steps when SOME agent stood at that source, for the whole population at once. An agent's traces therefore decayed when other agents arrived, not with time: the agents were not independent, and every interval in section 7 assumes they are. In Run 2 the module is called exactly once per world step for every agent, with the odour code and reinforcement of the source the agent is within 3.0 of, or zeros. Reinforcement and compartments are as in Run 1 (compartment 1 for reward, 0 for punishment, magnitude 1). Consequence stated openly: traces now decay in world time, so learned values need not reproduce Run 1's +0.901 and -0.900. A self-check will show that an agent standing at a source for n steps gets the same weight change from both harnesses.

## 3. World

ph13.World4, 160x160 translation of ph11's two-source world: sources 14-18 apart crosswind at one downwind coordinate; cones 25 long overlapping only in their last 0-3 units in about a third of worlds; nearest wall to any source 68; p_hit 0.3; start inside one cone, 5-18 downwind of its source. **400 agents.** Which source rewards is assigned AFTER the world is drawn so that exactly 200 agents start in the punishing plume (**P-start**) and 200 in the rewarding plume (**R-start**), the split chosen by a seeded permutation. Arms of an evaluation share world seed, agent seed and agent index, so agent i is the same world row and initial state in every arm.

## 4. Two evaluations, never mixed

**E1, natural search.** One continuous world, 9 blocks of 600 steps, learning on from step 0, no relocation, nothing delivered by the experimenter. Exposure is known to be one-sided (R-start agents meet the punisher in 6-17 percent of cases), so E1 answers the core question in the P-start group and reports R-start without expecting two-sided learning from it.

**E2, controlled experience.** Never claimed as autonomous search. What is controlled is the RECEIPT OF REINFORCEMENT.
- Training: each agent is held at one source for 30 steps and then at the other for 30, order assigned evenly (200 reward-first, 200 punish-first, seeded permutation, independent of start group). On each of those steps the learning module receives that source's odour code; the TRAINED group also receives that source's reinforcement, the SHAM group receives none. No navigation during training.
- Recorded before the test, for every agent in both groups: learned valence of the rewarded and of the punished odour.
- Relocation. KEPT: the learned weights only. RESET to their initial values: the learning traces `tc` and `tr`; selection state (circuit units, global unit, silence clock); the upstream stage's filtered drive; cast clock; cast side and flee side (redrawn from the agent's generator); position and heading (every agent is placed as a P-start agent, the same placement in both groups). The ring is not reset; with the wind sensed every step it re-anchors within a few steps.
- Test, MAIN: 3 blocks of 600 steps with learning FROZEN (the module is not called). Auxiliary: the same test with learning on, trained group only, reported separately with no criterion.
- E2's unrecovered rate is reported and is NOT used as evidence about search persistence, because relocation puts every agent back in a plume.

## 5. Arms and the question each answers

| arm | evaluation | question | role |
|---|---|---|---|
| intact | E1 | the core question | gated |
| no learning (valence fixed at zero) | E1 | behaviour with no learned value; baseline for avoidance | gated baseline |
| known valence | E1 | what value-driven behaviour reaches in this world; a reference, not an ablation | reference |
| trained / sham | E2 main | does value installed by a fixed reinforcement dose drive behaviour, with nothing learned during the test | gated / gated baseline |
| trained, learning on | E2 auxiliary | what continued learning adds | reported |
| ungated learning | E1 | mechanism comparison: does the extinction gate protect a learned value under the exposure that actually occurs | auxiliary |
| selection circuit removed | E1 | what the hold contributes in this world; distractor resistance stays unverified | reported |
| whole stage removed | E1 | the integrated result with the upstream stage absent under existing settings; not a test of normalisation | reported, claim limited |
| cross-channel division term removed | E1 | contribution of the interaction between channels, with gain, own-channel saturation and temporal filter kept | reported |
| exact heading | E1 | no difference expected with the wind sensed every step; not evidence about heading memory | reported |
| random walk, oracle | E1 | floor and ceiling per source | probes |

## 6. Measures, for all agents, P-start and R-start, always with counts

Never a net score. Visits to each source and to both (whole run, first third); step of first visit and of first punished step; steps from the first punished step to the last step ever spent at the punisher; dwell at each source per block and in the last third; visits and steps per visit; late unrecovered on plume whiffs; wall contacts and near-wall dwell; whiffs handed to navigation by selection state; steps with nothing held. Learning: learned valence of each odour at the end and per block, over agents that received that reinforcement (count and share of their parent group) and over all agents; reinforced steps received per source.

## 7. Criteria

### 7.0 How uncertainty is handled (applies to every criterion)

- A proportion k/n against a threshold uses the Wilson 95 percent interval [L, U]. 'At most t': PASS if U <= t, FAIL if L > t. 'At least t': PASS if L >= t, FAIL if U < t. Anything else is INCONCLUSIVE.
- A median, a difference of medians or proportions, or a ratio of medians uses a percentile bootstrap over agents: 5000 resamples, generator seed 20260920, resampling agent indices so that matched arms stay matched; 95 percent interval; the same three-way rule.
- A matched-pair win rate is wins over all pairs, ties counting as not wins, with its Wilson interval against 0.60; the share of exactly tied pairs is printed, and above 20 percent the comparison is UNREADABLE.
- Every criterion prints k, n, the point value, the interval and the outcome. A group smaller than 50 is UNREADABLE. INCONCLUSIVE and UNREADABLE never pass a gate and are never reported as failures; only a new run with new seeds can resolve them.

### 7.1 The criteria

**Q1 validity.** E1, all 400 agents, last third. (a) median rewarding dwell, oracle minus random walk: interval's lower bound at least 10. (b) no agent arm at the ceiling: upper bound of median dwell at either source below 594. (c) median total dwell, intact minus random walk: lower bound at least 10. These are differences, so a random walk at 0 is fine. Unreadable: never.

**Q2 search maintained while learning.** E1, intact, late unrecovered = no plume whiff in blocks 7-9. (a) all 400 agents: at most 10.0 percent. (b) P-start and R-start separately: the matched difference intact minus known-valence is at most +10 points. Per-group absolute rates are printed with their intervals. Unreadable: (b) only, if the known-valence arm's own all-agent rate FAILS 'at most 10 percent', because then the reference is broken.

**Q3 a learned negative valence becomes avoidance.** E1. Group G3 = P-start agents with at least one punished step in the intact arm; its count and share of the 200 are printed, and the same indices are used in every arm. (a) learned valence of the punished odour at the end, median at most -0.5. (b) last-third punishing dwell, intact, median at most 1.0. (c) matched pairs on last-third punishing dwell, intact below no-learning: win rate at least 0.60, and (no-learning median minus intact median) at least 25 percent of the no-learning median. Unreadable: G3 under 50; for (b) and (c), if the no-learning arm's median in G3 does not PASS 'at least 10', because then both arms are at the floor and absence of dwell would not show avoidance, and (c)'s ratio would divide by a floor; ties above 20 percent.

**Q4 search continues after avoidance.** E1, G3 indices, known-valence arm as reference on the same indices. (a) share that reach the rewarding source after their first punished step, intact minus known: at least -10 points. (b) last-third rewarding dwell, ratio of medians intact over known: at least 0.75. Unreadable: G3 under 50; all of Q4 if the known arm's last-third punishing dwell in P-start does not PASS 'at most 1.0' (the reference does not avoid); (b) if the known arm's median rewarding dwell does not PASS 'at least 10' (a ratio over a floor).

**Q5 positive valence, weight level only.** E1, group G5 = agents with at least one rewarded step (count and share printed). Learned valence of the rewarded odour, median at least +0.5. No behavioural claim. Unreadable: G5 under 50.
Auxiliary, ungated against gated, everything else identical. Printed for both arms: per agent, total steps within 3.0 of the rewarding source, longest unbroken stay, reinforced steps received; learned value at the end of each stay and at the start of the next, so that change DURING a stay and change AFTER leaving are separate; the number of agents at each exposure level. Read only if at least 50 agents in each arm received at least 100 rewarded steps; otherwise 'not discriminated in this run'. When readable: 'the gate protects the value' if the ratio of medians ungated over gated has its upper bound at most 0.5; 'no difference seen' if the interval lies within 0.8 to 1.25; anything else 'not discriminated in this run'. Never 'no effect'. Its outcome changes no main criterion.

**Q6 controlled experience.** E2 main, all 400 agents, learning frozen, trained against sham on the same indices. Manipulation check first: before the test the trained group's punished-odour valence has a median at most -0.5 and the sham group's absolute median is at most 0.1; if not, Q6 is UNREADABLE and that is reported as a finding about the dose. (a) punishing dwell summed over the test, ratio of medians trained over sham: at most 0.5. (b) matched pairs trained below sham: win rate at least 0.60. (c) share reaching the rewarding source, trained minus sham: at least +25 points. Unreadable: (a) if the sham median does not PASS 'at least 10 steps' (a ratio over a floor, and two groups at the floor); ties above 20 percent. Worded as 'after a fixed dose of both reinforcements, behaviour followed value with nothing learned during the test', never as search.

**Q7 integrity.** Regression 710/710; hashes of every stored module unchanged; the self-checks of section 2.1 and of the agent (with learning off it reproduces the H19 verdict run's `fix` arm) pass.

**Verdict.** The core question is answered YES if Q1, Q2, Q3 and Q4 all PASS. Any FAIL among them: NO, not supported. No FAIL but some INCONCLUSIVE or UNREADABLE: NOT DECIDED BY THIS RUN. Q5, Q6 and every reported arm are stated beside the verdict with their own readings. Observed differences are reported as they are; no measure is chosen afterwards to stand in for a registered criterion. A YES is valid for this world with the wind sensed every step and says nothing about the items marked unverified.

## 8. Seeds and procedure

Development, to find operation errors only: E1 9800/9900, E2 9801/9901, at 400 agents. Evaluation, never used: E1 1640/1740, E2 1641/1741. The evaluation is run once. Every script is stored in full with its sha256 in the same session.

## 9. Predictions

Q1, Q2 PASS (the known arm left 4.5 percent unrecovered under H19 (a); with 400 agents the interval should clear 10). Q3 PASS: a first visit delivers about 8 punished steps, enough to drive the value well below -0.5. Q4 PASS, close to the known arm's 97 percent. Q5 about +0.9. Gate comparison: most likely 'not discriminated', because agents receive about 200 rewarded steps in short stays of 6-9. Q6: manipulation check passes, (a)-(c) PASS. Most likely to surprise: how long agents stay at the punisher after the first punished step, since the hold outlasts its timeout and the flee acts only while the punished odour is held; and whether values differ from Run 1's under the corrected harness.
