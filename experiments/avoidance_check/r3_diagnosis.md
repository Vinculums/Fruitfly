# R3 diagnosis: where the release loses the valued outcome under +1/-1

Date 2026-09-24. Measurement only, at the owner's instruction (2026-09-24, '1 → 2(a) → 3·4·5', point 1). The avoidance check's readings (record:avoidance-check-result: R0 to R2 clean, R3 'avoidance changed') are not re-judged. ph24.py (sha256 f344f178...1bef), ph24b.py (sha256 bbabad15...eefc, doc d68d589ccad0beef9), the avoidance check design v1 FINAL (doc df00c6e0dbc5f6792, sha256 bc6b23d3...14c5) and every adopted module are unchanged. Code: src/ph24c.py, sha256 17adab85f64f75e64eb7a9febbefb417829a16ece4c391dc15e7721a21a76a45 (source stored in its own document, d4238c123b7873d90). Output: experiments/avoidance_check/ph24c_diag.txt, sha256 212e4c1818ab21027debfb3357264c6f9dc6070a825d59d0ab54fe22e11d655f (LF line ends).

ph24c imports ph24 and ph24b unchanged and re-runs R3's two arms exactly as ph24b does: ph24.run('T1', cls, (+1, -1), (1805, 1905)), World7, 400 rows x 600 steps, G 2, gate on, C0, with ph24b's record hook (the flee side per step; every other field bitwise equal, checked in ph24b). At +1/-1 Agent10 == Agent10g and Agent8 == Agent6 bitwise (R0), so Agent10 vs Agent8 is the only comparison. No new seed; the H25 evaluation seeds are reused for a reproduction, not for new evidence. **Reproduction (printed, asserted before any measurement):** Agent10 V/N/tie 306/27/67, lost rows 127, wall contacts per row 0.000; Agent8 370/16/14, 33, 0.307; negative holds formed / ended / ended by the drive 237/236/131 (Agent10) and 200/168/0 (Agent8). All MATCH. A diagnosis narrows where the difference lies; it names no cause beyond what was measured, and it tests no change.

Definitions. The whiff region of a source is ph11's: the cone 0 < d_along < 25 and |d_cross| < 1.5 + 0.25 d_along, or within 3.0 of the source (d_along = x - x_src, downwind > 0). 'Position at step t' is the position step t sensed at (after step t - 1's move). A lost row has no whiff of either plume on steps 400 to 599. 'Toward' / 'away': the flee side (90 = +y, 270 = -y) on the hold's first step points toward / away from the valued source (World7 puts the two sources 10 apart crosswind).

## 1. Measured

1. **Agent10's drive-ended negative holds (131, one per row, 131 rows).**
   - Timing: hold formed at step 18/35/365 (quartiles), drive start 66/81/413, release 72/87/419; hold length to the release 48/50/54 steps. Nothing held on the release step 131/131.
   - Flee direction: away from the valued source 109/131, toward it 22/131. At the release the agent is beyond the negative source (farther from the valued axis) in 109/131, all of them 'away'; beyond the valued source in 22/131, all of them 'toward' (these crossed the valued plume during the hold without an evidence release).
   - Position at the release: outside both whiff regions 131/131. Distance to the nearest region 20.7/24.5/26.6, max 28.4. |d_cross| to the nearer axis 26.1/29.0/30.9. d_along 4.9/11.1/13.8 (upwind of the sources in 10).
   - Next 60 steps (14 windows cut by the run's end): any whiff 0/131; re-entered a whiff region 0/131; reached a source 0/131; held at e + 60 nothing 117/117 (full windows); distance to the nearest region at e + 60 19.7/24.6/29.8.
   - Next 200 steps (34 cut): any whiff 0/131; re-entry 0/131; reached a source 0/131; held at e + 200 nothing 97/97; distance 21.9/24.6/30.2.
   - To the run's end: any whiff 0/131; re-entry 0/131; valued source reached 0/131, negative source 0/131.
   - Rows: final class V 47, N 24, tie 60 (the valued source had been reached before the release in 51 of the 131). **Lost 116/131 = 0.885**, against 11/269 = 0.041 in the rows without such a release. Of the 127 lost rows, 116 contain a drive-ended negative hold.

2. **Agent8's negative holds (200) and the wall.**
   - Ends: 167 by the evidence release, 1 on the step after a base timeout firing (a 3-step hold whose s was 1.21 and fell below 1.0), 32 still held at step 599 (wall contacts per hold 1/1/1, quartiles). The recorded 'ended 168' is 167 + 1.
   - Of the 167 evidence-ended holds, a wall contact during the hold before the release: **83/167 = 0.497**. Hold start → first contact 124/131/137 steps. Hold start → release 20/33/280: with a contact 265/280/296, without 15/20/23.
   - By flee direction: toward 96 (a contact before the release 14, none 82; release after 15/21/25 steps); away 71 (a contact 69, none 2; release after 267/283/296 steps).
   - Crosswind displacement over the hold, |y_end - y_start|: 8.0/10.8/13.2 (with a contact 7.8/10.6/12.9, without 8.4/11.2/13.5); largest crosswind excursion during the hold 11.2/19.6/79.1.
   - At the evidence release: inside the valued whiff region 91/167, inside the negative one 2/167; |d_cross| to the valued axis 2.1/3.4/4.3.
   - Every one of Agent8's 123 wall contacts happens while it holds the negative odour (0 while holding the valued odour, 0 holding nothing).
   - Rows with >= 1 wall contact: Agent8 106/400; Agent10 0/400.
   - **P(V | any wall contact) 86/106 = 0.811 [0.726, 0.874]; P(V | no wall contact) 284/294 = 0.966 [0.939, 0.981]** (Agent8, Wilson 95 percent).
   - Paired, same rows: in Agent8's 294 no-contact rows Agent8 V 284 and Agent10 V 284; in its 106 contact rows Agent8 V 86 and Agent10 V 22. All 64 rows that leave V had an Agent8 wall contact (64/64).
   - Agent8's V rows: the first valued hold comes after the first wall contact in 59/368; the first arrival at the valued source comes after it in 61/370.

3. **The 64 paired rows that move out of V** (Agent8 V; Agent10 N 10, tie 54).
   - The circuit s first differs at step 41/67/74 (the drive's delivery). Hold and trajectory (H, POS, HEAD, NAV, SINCE, TGT) first differ exactly at Agent10's first drive release in 64/64, at step 67/74/79. That release ends a negative hold in 63 and a valued hold in 1.
   - State then: Agent10 holds nothing 64/64; Agent8 holds the negative odour 63, the valued odour 1. Position outside both whiff regions 64/64; distance to the nearest region 19.8/24.6/26.7; |d_cross| to the valued axis 34.8/38.8/40.4.
   - Agent10 afterwards: a whiff within 60 steps 0/64, any whiff to the end 1/64, a valued whiff 0/64, re-entered a whiff region 1/64, reached the valued source 0/64 (the negative source 1/64), wall contact 0/64; lost row 64/64.
   - Agent8 afterwards: a whiff within 60 steps 0/64, any whiff to the end 64/64, a valued whiff 64/64, a wall contact 64/64, re-entered a whiff region 64/64, reached the valued source 64/64 (the negative source 9/64); lost row 1/64; V 64/64.

4. **Both arms: where the agent is when nothing has been held for >= 60 steps.**
   - Agent10: 101,207 (row, step) in 400 rows; inside a whiff region 0.066; distance to the nearest region, outside it, 8.8/18.5/26.6 (p90 33.2); farther than 10: 0.671, than 20: 0.422; d_along to the sources -12.2/0.3/25.0 (upwind of both 0.496; beyond the cones' far end 0.250).
   - Agent8: 15,465 (row, step) in 138 rows; inside 0.061; distance 5.0/8.3/12.7 (p90 20.8); farther than 10: 0.362, than 20: 0.104; d_along -9.6/-0.6/20.9 (upwind of both 0.511; beyond the far end 0.202).

## 2. Reading

Interpretation, separated from the measurements above. It names no cause beyond what was measured and tests no change.

**The owner's question, part 1: is the -0.160 the release stranding the agent outside the plumes?** On these rows, yes, as far as measured. The release does what H25 built it to do: it ends a negative hold 48 to 54 steps after it formed, with nothing held. By then the flee has carried the agent about 29 units crosswind, outside both whiff regions in 131 of 131 releases, 20 to 27 units from the nearest one. From there no whiff arrives in the rest of the run in 131 of 131 (181 to 528 steps remain), and 116 of these rows end lost. The whole P(V) difference sits in rows where the base agent meets a wall: on the 294 rows where Agent8 touches no wall, the two arms have the same V count (284 and 284); every one of the 64 rows that leaves V is a row where Agent8 hit a wall. What fails after the release is a search that starts from an odour-free position well outside the plumes. That is the limit recorded at the H16 close and queued as H17 (cold-start search; 52 percent reached the plume from an odour-free start in H16 Run 2, under a different start and arena). Here the same kind of search, from about 25 units off the plumes, finds a whiff in 0 of 131 cases. The release exposes this limit; the counts do not say the release is wrong for a hold that should end.

**The owner's question, part 2: is Agent8's 0.925 partly a wall-reflex artefact?** Partly, on these rows. When Agent8 flees away from the valued source (71 evidence-ended holds), it keeps the negative hold for about 130 steps until it reaches the arena wall (69 of 71), the bump reflex (ph11 Agent.bump) turns the flee side around, and the agent flees back across both plumes; the hold then ends by the evidence release, inside the valued whiff region in 91 of all 167 evidence releases. 61 of Agent8's 370 V rows reach the valued source only after a wall contact, and every wall contact happens while the negative odour is held. P(V) is 0.811 with a wall contact and 0.966 without. The wall reflex was added in ph11 to stop an agent pinning itself against a wall; it was not designed as a return path, and the arena's walls are a construction of the task. In the 61 V rows whose first valued arrival follows a wall contact, the base's recovery went through that reflex (each contact made while fleeing the negative odour), not through the circuit releasing the hold. What the base would do without walls is not measured here.

**What this means for the comparison.** The -0.160 compares a release that strands the agent with a base whose negative hold is carried back by the wall. Neither arm is measured finding the plume by search from far outside it: Agent10 does not in 131 of 131 releases, and Agent8 does not search while it holds the negative odour (it flees until the wall turns it; 32 negative holds were still held at step 599, with wall contacts 1/1/1 per hold, quartiles). The avoidance itself (flee on every negative-held step, lower dwell at the negative source) is kept, as R3 recorded.

**Not measured:** a run without walls (the base's stranding there); the same rows under another RESET_AFTER or another flee rule; whether a different search after the release would find the plume. Each would test a change and is outside this diagnosis.

## 3. Provenance

- Runs: ph24.run('T1', Agent10 | Agent8, (+1, -1), (1805, 1905)), 400 x 600, the runs of R0 and R3 in ph24b_check.txt, reproduced (the introduction).
- Code: src/ph24c.py sha256 17adab85...6a45; imports ph24 (f344f178...1bef), ph24b (bbabad15...eefc), ph9 constants.
- Output: experiments/avoidance_check/ph24c_diag.txt sha256 212e4c18...655f.
- Owner's instruction: 2026-09-24, '1 → 2(a) → 3·4·5' (point 1: the diagnosis; point 2(a): the scope decision that follows it).

## 4. Output (ph24c_diag.txt, in full)

The output file is stored verbatim in the repository (experiments/avoidance_check/ph24c_diag.txt, sha256 above); every number in section 1 is quoted from it.
