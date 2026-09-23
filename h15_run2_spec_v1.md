# H15 Run 2: experiment specification v1

Date 2026-09-20. Status: **DRAFT for the owner's confirmation. No code exists and none is written until this is confirmed.** Direction set by decision:h19a-adopt-and-run2-direction (owner). When confirmed, this text becomes the pre-registration; after that, any change before the evaluation is a recorded amendment and any change after its table is a new run.

## 1. Question

**Does a learned negative valence lead to actual avoidance, and is long-horizon search maintained while it does?**

Claimed at most at the weight level: learning of a positive valence (in this agent a positive valence has no behavioural effect). Marked unverified and not tested here: the selection circuit's resistance to a distractor; heading memory under loss of the wind cue.

## 2. The agent of record, and the known defects held fixed

- Upstream normalisation ph2.Upstream (n 1.5, sig 0.05, Rmax 1.8, k 0.8), unchanged.
- Select-and-Hold ph2.Circuit (n 2, theta 1, k 12, noise 0.01) with Phase 5 Run 2's two releases, unchanged.
- Heading: RingExact as adopted in H14 (n 16, tau 1, sigma 0.5, vgain 1), wind cue amplitude 6.0 on EVERY step, fed the rotation made.
- Learning: ph8.MB4, gated, parallel site off (K 200, C 4, sparsity 0.05, eta_d 0.10, eta_p 0.30, beta 0.15). Reinforcement as in ph11.episode: on every step within 3.0 of a source the odour code of that source is paired with that source's reinforcement.
- Navigation: surge-and-cast with the return cast; crosswind flee from a held odour of negative valence; wall reflex; H19 (a): while nothing is held, a whiff of an odour whose valence is not negative is handed to navigation.
- Implementation: ph14.Agent3 with fix on, imported, not copied. A self-check must show that with learning off it reproduces the H19 verdict run's `fix` arm on that run's seeds.

Held fixed, NOT repaired in this run: the silence timeout never releases the hold; a positive valence is behaviourally inert; a whiff of B is ignored while A is held; the ring leaks agents under cue loss (not exercised, the wind is sensed every step); a plume is found from an odour-free start about half the time.

## 3. World

ph13.World4: ph11's two-source world drawn in its own frame and translated +60 inside walls 160 apart. Sources 14-18 apart crosswind at the same downwind coordinate; cones 25 long, overlapping only in their last 0-3 units in about a third of worlds; nearest wall to any source 68; p_hit 0.3; which source rewards is random; start inside one cone chosen at random, 5-18 downwind of its source. 200 agents.

Start groups, fixed here and used by every criterion that names one: **P-start** = the start cone is the punishing source's; **R-start** = the rewarding source's.

## 4. Two evaluations, never mixed

### E1. Natural-search evaluation

One continuous world, 9 blocks of 600 steps, learning on from step 0, no relocation, nothing delivered by the experimenter. It measures what the agent finds and experiences by itself and how it behaves afterwards. Known in advance from the two-source check: exposure is one-sided. P-start agents arrive at the punisher by themselves; R-start agents seldom meet it (6-17 percent). E1 therefore answers the core question in the P-start group, and reports the R-start group without expecting two-sided learning from it.

### E2. Controlled-experience evaluation

Never claimed as autonomous search. **What is controlled is the receipt of reinforcement**, not odour exposure and not arrival.

- Training: every agent is held at the punishing source for 30 steps and at the rewarding source for 30 steps (order random per agent, counterbalanced), receiving that source's reinforcement paired with its odour code on each of those steps, exactly as a step within 3.0 of the source does in E1. No navigation happens during training. 30 steps is about what one natural visit delivers (20-28 steps per block in the two-source check). An untrained control arm skips training.
- Relocation to the test start. KEPT: the learned weights, and only those. RESET: selection state (circuit units and global unit to zero, silence clock to zero), the upstream stage's filtered drive, the cast clock, the cast side and flee side (redrawn), position and heading (drawn from the P-start distribution). The ring is not reset; with the wind sensed every step it re-anchors within a few steps. Learning stays ON during the test, as it is in the world.
- Test: every agent starts as a P-start agent, 3 blocks of 600 steps.
- Because relocation puts every agent back inside a plume, **E2's unrecovered rate says nothing about search persistence and is not used for it.** E2 is read for value-driven behaviour only.

## 5. Arms and the question each answers

| arm | evaluation | question | status |
|---|---|---|---|
| intact | E1, E2 | the core question | gated |
| no learning (neutral valence) | E1 | what behaviour looks like with no learned value; the baseline for avoidance | gated baseline |
| known valence | E1 | reference: what value-driven behaviour can reach in this world; not an ablation | reference |
| untrained | E2 | what the controlled experience adds at the start of the test | gated baseline |
| ungated learning (MB4 gated off) | E1 | under sustained exposure at a source, does the extinction gate protect the learned value? weight level | reported, fixed reading |
| selection circuit removed | E1 | what the hold contributes in this world; distractor resistance stays unverified | reported |
| whole stage removed | E1 | the integrated result when the upstream stage is absent under the existing settings; NOT a test of normalisation | reported, claim limited |
| cross-channel division term removed (k = 0) | E1 | the contribution of the interaction between channels with gain, own-channel saturation and temporal filter kept; bench-verified (record:cross-channel-control-bench-check) | reported |
| exact heading | E1 | with the wind sensed every step no difference is expected; whatever is found is NOT evidence about heading memory | reported |
| random walk, oracle | E1 | floor and ceiling per source | probes |

## 6. Measures, reported for all agents, P-start and R-start, with counts

Never a net score. Visit rate of each source and of both, over the run and in the first third; step of the first visit and of the first punishment; steps from the first punishment to leaving the punisher for good; dwell at the rewarding and at the punishing source per block and in the last third; late unrecovered counted on plume whiffs; wall contacts and near-wall dwell; share of whiffs handed to navigation by selection state; share of steps with nothing held. Learning: learned valence of each odour at the end, over agents that received that reinforcement (with their count) AND over all agents; reinforced steps received per source.

## 7. Criteria, each tied to a named group

Every rate is given with its count and unrounded value. A criterion met or missed by one agent is reported as 'at the bar' and is not used alone to pass a gate.

- **Q1 validity (E1, all agents, last third, per source).** Oracle rewarding dwell minus random walk's at least 10; no agent arm at 99 percent of 600 at either source; intact total dwell median at least the random walk's + 10.
- **Q2 search maintained while learning (E1, intact).** Late unrecovered at most 10.0 percent in ALL agents, in P-start and in R-start, each separately. Reference, reported beside it: the known-valence arm in the same world and seeds.
- **Q3 a learned negative valence becomes avoidance (E1, P-start agents that received punishment; unreadable if fewer than 50).** (a) learned valence of the punished odour, median at most -0.5. (b) punishing dwell in the last third: intact median at most 1.0, read only if the no-learning arm's median in the same group is at least 10. (c) matched pairs on last-third punishing dwell: intact below no-learning in at least 60 percent of pairs, with a gap of at least 25 percent of the no-learning median.
- **Q4 search continues after avoidance (E1, same group as Q3).** Share reaching the rewarding source within 10 points of the known-valence arm's in the same group; last-third rewarding dwell median at least 75 percent of the known arm's.
- **Q5 positive valence, weight level only (E1, agents that received reward, with count).** Learned valence of the rewarded odour, median at least +0.5. Gate reading, reported: among agents with at least 1000 reinforced steps at the rewarding source, 'the gate protects the learned value' if the ungated arm's median learned valence is below half of the gated arm's.
- **Q6 controlled experience (E2, all agents, first test block).** Punishing dwell: trained median at most half of untrained's, read only if untrained's median is at least 5. Share reaching the rewarding source within the test: trained at least untrained's. Worded as 'after both reinforcements were delivered, behaviour followed value', never as search.
- **Q7 no regression.** 710/710; no stored module edited.

Verdict: the core question is answered YES if Q1-Q4 pass. Q5, Q6 and the reported arms are stated beside it with their own readings. A pass is valid for this world, with the wind sensed every step, and says nothing about the items marked unverified in section 1.

## 8. Unreadable conditions, fixed in advance

A group smaller than 50 agents; a baseline below the floor stated in its criterion; the known-valence reference itself failing to avoid (last-third punishing dwell median above 1.0 in P-start) makes Q3 and Q4 unreadable rather than failed; every arm at the floor in a comparison; any criterion decided by a single agent.

## 9. Seeds and procedure

Development, to find operation errors only: E1 9800/9900, E2 9801/9901. Evaluation, never used before: E1 1640/1740, E2 1641/1741; all arms of an evaluation share its seeds. The evaluation is run once. Observed differences are reported as they are; no measure is chosen afterwards to stand in for a registered criterion. Every script is stored in full with its sha256 in the same session.

## 10. Predictions

Q1, Q2 pass (known-valence arm left 4.5 percent unrecovered under H19 (a)). Q3: P-start agents are punished on arrival, learn within one visit and leave; pass. Q4: close to the known arm's 97 percent. Q5: +0.9 among the rewarded, as in Run 1; the ungated arm's value is eroded at the rewarding source, where agents sit for thousands of steps. Q6: trained agents avoid from the first block; pass. Most likely to surprise: the time between the first punishment and leaving, because the hold outlasts its timeout and the flee acts only while the punished odour is held.
