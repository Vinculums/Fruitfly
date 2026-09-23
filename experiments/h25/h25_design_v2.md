# H25 design v2 FINAL: silence-timeout release (a reset-control change)

Date 2026-09-23. Status: **v2 FINAL (confirmed by the owner 2026-09-23 as recommended).** Supersedes v1 DRAFT (doc d3cb0794633a587ae). Opened for design by decision:h25-open-design (owner, 2026-09-23: '① H24 종결(no candidate) 진행, ② 다음을 타임아웃 수정(H25) 설계'). Follows decision:h24-closed (H24 NOT shown, no candidate at the bench: its held clause presumed a timeout release the circuit does not make) and decision:h19a-adopt-and-run2-direction (the timeout frozen as a known defect; 'a later fix allowed to be a reset-control change'). Template: H23 design v2 (doc db6df2e0013ab96e7). Supplied values, learning off, G 2, geometry C0. Code read for this design at commit 85fb6fd: src/ph2.py (sha256 9e0ef833...0a4e, source doc df546a54e73dc7e8c), src/ph11.py (e80f40bd...7a23, d145c92187ea02993), src/ph14.py and src/ph14b.py (c6b745c6...d0e0 and ef18eff8...312e, d0199028443dd6060), src/ph16.py (33d5fdb2...a2c2, d89d730faca4b965a), src/ph17.py (4b30ddf8...4f3b), src/ph19.py (00c6a3b3...4791, d583f45c494d675e6), src/ph21.py (3a1d79d9...cfc1, ddcec8520fcd8e23c), src/ph23.py (ae180492...b5ae, d0ea25b8bebac735d).

## 1. Hypothesis

**H25: when the silence timeout fires on a held odour, sustaining the existing reset drive until both selection units are below threshold, with the silence counter also zeroed when a hold forms (section 3), makes a hold end within RESET_AFTER + 1 + D steps of its odour's last whiff (D = the drive steps needed, 4 in the recorded bench), leaves the circuit in the nothing-held state, and ends no hold whose odour was whiffed within RESET_AFTER steps.** In the agent whose navigation reads the hold (the H21 gate agent, Agent6), this lets the agent track the remaining neutral odour after the valued odour is lost, within a registered share of a known-answer ceiling [T3, M7]. In the adopted full agent (Agent8) the change is behaviour-inert at +1/0 by code (section 3) [T1, T2, T3 identities, M2, M5].

Two statements, judged separately: (i) implementation, on constructed states and the recorded bench protocol before any task (section 4, M4); (ii) tasks (sections 5 to 7).

## 2. The measured reason

Sources: record:silence-timeout-chain-result and the H19 (a) report d9ca02b921ee74e59 (bench output experiments/h19/ph14b_defects.txt), Phase 7.1 report d44b3156fa127b325, record:h21-bench-result and the H21 report d4fd6c39f7f81e1ee, the H23 report d8b91235798da849f (outputs experiments/h21/ph19_eval.txt, experiments/h23/ph21_eval.txt), record:h24-bench-result (experiments/h24/ph23_bench.txt).

**Measured.**
- The timeout is delivered and does not release (ph14b 1a, neutral, seeds 9600/9700, 2400 steps): 8652 timeout requests, value 10.0 delivered in all, for 1 consecutive step (median); held unit 1.99 before, lowest 1.49 in the next 8 steps (threshold 1.0); global unit peak 6.99; released within 8 steps 0.2%. The evidence release, by contrast: 761 requests, 10.0 for a median of 3 consecutive steps, held unit to 0.54, released 100%. **Duration, not delivery.**
- The dose that releases (ph14b 1b: a committed circuit, reset A for D consecutive steps, then 30 steps free; median lowest s, released fraction of 100): A 10: D1 1.52 0%, D2 1.30 0%, D3 1.14 0%, **D4 0.06 100%**, D6 0.05 100%, D8 0.04 100%. A 20: D3 0.07 100%. A 40: D1 1.26 0%, **D2 0.09 100%**. The cliff is sharp (D3 1.14 not released, D4 0.06 released) and a released unit does not rebound in 30 free steps.
- The timeout fires thousands of times per arm and ends almost nothing (task, 400 rows x 600 steps): H21 maintain (Agent6) 4378 firings while held, 2 ended the hold, valued holds ended 0 (the gate: 'a valued hold is never lost', 0 of 280 valued-first rows); H23 filter (Agent8) 4176, 1 ended; H23 maintain 4304, 6 ended. Held unit's s the step before any hold ended, median 1.06 in every arm.
- In the H21 bench (a) the valued hold was kept on every one of 200 phase-2 steps in 400/400 rows; the timeout fired 1649 times in phase 2 and ended 0 holds (held unit's s dips to 1.48 and recovers).
- H24 bench (f): the design assumed 'a valued hold ends on the timeout within 41 silent steps'. It does not: M7(a) 65/370 = 0.176 [0.140, 0.218]; the valued odour still held at or after L + 60 in 305/370 eligible rows. H24 bench (b): a single valued whiff forms a valued hold in 400/400 stub rows and it persists to step 199 with no input.
- H24 bench, apart from the verdict (bench seeds): W1 mean dwell Agent9 24.125, Agent8 12.300, Agent6 25.835; T3 (Lost, t0 150) neutral dwell 400-599 Agent6 4.7425, Agent9 - Agent6 -1.70 (sd 5.11), Agent8 - Agent6 -2.22; Agent6's post-loss neutral surge S6 = 8/270 = 0.0296.

**Reading (Phase 7.1).** The reset is the price of abstention: the bistable units that abstain need an external drive to clear. A release must leave the circuit in the nothing-held state (both units below threshold), from which the input re-selects; it must not flip the hold.

**Why this lever.** The record locates the defect in the drive's duration (one step). The owner's direction and decision:h19a-adopt-and-run2-direction allow a reset-control change only.

## 3. The change: the reset control, boundaries stated

**The code as it stands (quoted).** The circuit takes the reset as an additive term in the pooled inhibition (ph2.py lines 32-42):

    def step(self, y, reset=0.0):
        q = self.pool_c * np.maximum(self.s, 0.0)**self.pool_p   # supralinear pool when p>1
        pool = q.sum(1, keepdims=True) + reset
        ...
        self.S += (self.DT/self.tau_g) * (-self.S + pool)
        u = (y + self.g*sigmoid(self.k*(self.s - self.theta)) + self.w_i*q - self.w_i*self.S
             + self.noise*self.rng.standard_normal(self.s.shape))
        self.s += (self.DT/self.tau) * (-self.s + np.clip(u, 0, self.S_MAX))

The request is made in each agent's act, copied from ph11.Agent.act (lines 174-178, 192) through ph14.Agent3.act (66-70, 86), ph16.Agent4.act (80-85, 93), ph19.Agent6.act (53-58, 66) to ph21.Agent8.act (lines 59-64, 76):

    self.due_timeout = self.silence > RESET_AFTER                       # RESET_AFTER 40 (ph11 line 39)
    self.due_evidence = committed & ((y[rows, other] - y[rows, hi]) > MARGIN)
    due = self.due_timeout | self.due_evidence
    rst = np.where(due, 10.0, 0.0)[:, None]
    self.silence = np.where(due, 0.0, self.silence)                     # zeroed on the firing step
    self.sel.step(y, reset=rst)
    h = self.held()
    ...
    self.silence = np.where(hit, 0.0, self.silence + 1.0)               # hit = a whiff of the held odour

So a firing delivers 10.0 once and zeroes the counter; the next firing is 41 steps later. Three facts from these lines matter:
- (F1) The counter runs whatever is held. With nothing held, hit is False and the timeout fires every 41 steps; the one-step drive then acts on sub-threshold units. That is unchanged by this design.
- (F2) **The counter is not reset when a hold forms.** A hold forms a few steps after the whiff that drives it (one valued whiff at G 2 forms the hold, H24 bench (b), 400/400; arithmetic on ph2 lines 13-17 and 41 puts the threshold crossing about two steps after the whiff; ph14b section 2: at G 0 a hold needs 2 consecutive whiffs, one whiff peaks at 0.76). On the formation step hit is usually False, so a new hold inherits the counter's value from the nothing-held stretch. With the timeout working, such a hold would end fewer than 41 steps after its own whiff. This is a code-line fact, not previously recorded; its size is measured in bench (d).
- (F3) **Agent8's navigation does not read the hold at +1/0** (ph21 lines 69-72): with the valued odour held, keep is True and nav = hit = a valued whiff; with the neutral odour held or nothing held, keep is False and nav = a whiff of the top-valued odour = a valued whiff. val (line 67) is never negative, so the flee line never acts. The turn is therefore a function of valued whiffs, the cast clock and the ring only; the circuit draws its noise every step with a fixed shape (ph2 line 40), so the random stream does not depend on the circuit's state. H24 design v3 section 6 already stated this for T3 ('by code'). Agent6's navigation does read the hold (ph19 line 63: nav = hit | (nothing held & any non-negative whiff)).

**Candidates evaluated.**
- (K4) Deliver the drive for 4 consecutive steps on every firing (ph14b: D4 at 10 releases 100%). Needs a drive-step count (the counter can carry it, 41 to 44), but it also lengthens every nothing-held firing (F1) from 1 to 4 steps, which changes the agent in every row every 41 steps while nothing is held: identity (b) would fail almost everywhere. And the margin is one step (D3 fails).
- (A40) A stronger drive, 40 for 2 steps (ph14b: D2 at 40 releases 100%; D1 does not). Same objection: it changes every nothing-held firing, and it still needs two steps.
- (S) **Sustain the existing drive (10.0) while any unit is above threshold after the drive step.** A nothing-held firing is then exactly today's one step (both units already below 1.0 after it), so F1 is untouched. A firing on a held unit continues until the circuit is empty; from ph14b's state that is D = 4 steps. The stopping rule itself guarantees the end state Phase 7.1 asks for (both units below threshold). A flip is not possible during the drive: after the first drive step the pool term is about 7 (ph14b 1a: global unit peak 6.99), so for the other unit u = y + g sigmoid + q - S is below zero for any y the agent produces (at most 1.8 x (1 + G) = 5.4); after the stop, S decays with tau_g 2 while the released unit is below threshold with no input, and ph14b D4 shows no rebound in 30 steps. **Chosen,** together with:
- (Z) **Zero the counter on the step a hold forms** (h >= 0 and h different from the hold before this step). This closes F2: the counter then counts steps since the held odour's last whiff or the hold's formation, so a hold whose odour was whiffed within RESET_AFTER steps is not timed out. Z adds no state and draws no random number.

**The change (new file ph24.py; no adopted module edited).** A mixin that wraps the adopted act without copying it:

    class Release:                                    # H25: the reset control
        def act(self, w, whiffs, wind_on):
            rows = np.arange(self.R); hp = self.held()
            turn, h = super().act(w, whiffs, wind_on)
            hit = (h >= 0) & whiffs[rows, np.maximum(h, 0)]
            new = (h >= 0) & (h != hp)
            sustain = self.due_timeout & ~self.due_evidence & (self.sel.s > 1.0).any(1) & ~hit
            self.silence = np.where(sustain, RESET_AFTER + 1.0, np.where(new, 0.0, self.silence))
            return turn, h

    class Agent10(Release, Agent8)     # the adopted full agent + H25
    class Agent10g(Release, Agent6)    # the H21 gate agent + H25

- sustain keeps the counter above RESET_AFTER, so the next step's own line (ph21 line 59 / ph19 line 53) fires the timeout again and delivers 10.0 again. It stops when both units are at or below 1.0 after a drive step, when a whiff of the held odour arrives (hit: the odour is back, the base line zeroes the counter), or when the evidence release fires (its path as before).
- Everything else is the adopted code: the constants (RESET_AFTER 40, MARGIN 0.2, amplitude 10.0, the circuit's), the gain, the gate, the filter, navigation, the ring. The wrapper reads only due_timeout and due_evidence, which Agent4 already exposes (ph16 lines 73, 80-81).
- The circuit's threshold test is ph11's held() (s > 1.0). 'Both units below threshold' is (s <= 1.0) on both units; held() also returns -1 when both units are above 1.0, and that state is sustained too.

**Identities (by reading the code; checked in M3, M4).**
- **(b) Identity where the timeout never fires on a hold.** The wrapper writes the counter only on sustain steps and formation steps. Before a row's first divergence, the fix's counter is at most the base's (Z only lowers it), so the fix fires on a hold only where the base also fires on a hold. Hence: **every recorded field except the counter's own value (positions, headings, s, S, held odour, nav, cast clock, target) equals the base agent's on every step before the row's first base timeout firing while a unit is above threshold; a row in which the base's timeout never fires on a hold is bitwise the base throughout.** The exception inside that class: a firing whose single step already empties the circuit (0.2% in ph14b 1a) is identical in both. Rows are independent: every random draw (world, wind, circuit noise, ring noise, turn noise) is made for all rows every step with a fixed shape.
- **The owner's gloss of (b), 'every history in which the held odour is whiffed at least every RESET_AFTER steps', is not the same class,** because of F2: the base can fire on a hold whose odour was whiffed 3 steps before formation and never since. On such a row the base delivers one step (a dip, no release) and the fix does not fire at all (Z). The held odour stays the same; s and S differ transiently. No reset-control change can be bitwise equal to the base there without reproducing the defect. Stated, not hidden; bench (d) counts these rows (section 12, point 3).
- **Agent10 == Agent8 in trajectory at +1/0, every row, every world** (F3): positions, headings, nav, cast clock, target equal; s, S, held odour and the counter differ after the first sustain event. Hence P(V), dwell, lost rows and contacts are equal row for row in T1, W1 and T3.
- **Agent10g == Agent6 in trajectory in W1, every row:** only the neutral odour is ever sensed, so a valued hold never forms (the unit receives no input; record:option-v-presence-diagnosis-result: a non-held unit's s stays near 0, max 0.0046) and ph19 line 63 gives nav = a neutral whiff whether the neutral odour or nothing is held.
- Values 0/0, +1/+1, +1/-1: the fix is not inert (Agent6 and Agent8 read the hold there). Only T1's neutral arm uses 0/0, for side balance.

**What the fix does to the gate's 'never lost (0/280)'.** With a working timeout a valued hold IS lost after 41 steps without a valued whiff (plus D). The gate still zeroes the neutral input while the valued odour is held (ph19 lines 48-50), so the neutral odour cannot end a valued hold that is being whiffed, and it cannot end it during the drive either. After the release nothing is held, the gate is off (hp < 0), and the input re-selects: a valued whiff forms a valued hold from one whiff at G 2, a neutral hold needs about 2 consecutive whiffs. In Agent8 the filter steers by value whatever is held (F3), so the lost hold changes nothing it does. In Agent6 the empty state hands any non-negative whiff to navigation (H19 (a)), so after a release the neutral plume can pull the agent: this is the cost measured in T1 (M6) and the behaviour wanted in T3 (M7).

## 4. Mechanism bench (before any task run)

Values +1/0 unless stated; G 2; gate on. Bench seeds 20261031 (whiffs, world) / 20261032 (agent). Stub = ph16.Still. Wilson 95 percent; paired bootstrap 5000 resamples, seed 20261033.
- **(a) Identities (implementation):**
  - (a1) Separation identity, Agent10 vs Agent8 and Agent10g vs Agent6: stub protocols of (b), (c) and World7 400 x 600. Every field of section 3's list equal up to the step before each row's first divergence step (first base firing on a hold that is not a one-step release); equal throughout on rows without one.
  - (a2) Agent10 == Agent8 in trajectory on every row: World7, W1 (ph22.Masked), T3a, T3b (section 5).
  - (a3) Agent10g == Agent6 in trajectory on every row in W1.
  - (a4) Constructions: T3b as H24 bench (f) (masked whiffs equal an unmasked World7 twin before t0, valued column False and neutral equal from t0, wind draws and generator state equal; each arm's T3b run == its World7 run on steps 0 to 149). T3a the same with the mask on from step 0 and the start placed at the valued source.
  - (a5) Reproduction on the recorded seeds (no criterion read): ph19 maintain (Agent6) on 1725/1825 gives V 300 / N 96 / tie 4; ph21 filter (Agent8) on 1765/1865 gives V 381 / N 14 / tie 5; Agent10 on 1765/1865 gives the same 381 row for row; (a1) holds for Agent10g vs Agent6 on 1725/1825 and Agent10 vs Agent8 on 1765/1865.
- **(b) Release on constructed states (stub, 400 rows, no input for 200 steps, counter 0 at construction):**
  - (b1) valued hold (s_0 = 2.0), Agent10g; (b2) neutral hold (s_1 = 2.0), Agent10g; (b3) valued hold, Agent10.
  - Statistic, per row exact: the hold ends at a step <= 49 (= RESET_AFTER + 9: the first drive at step 41, D <= 8, the longest duration ph14b measured), both units <= 1.0 at the end step, and no unit above 1.0 from then to step 199. Bar: lower bound >= 0.95. Predicted: 400/400, ending at step 44 (D 4).
  - Reported: D per row; S's peak; (b4) H21 bench (a)'s protocol with Agent10g (channel 0 p 0.30 for 60 steps, then channel 1 alone p 0.30 and 0.057 for 200): kept on every phase-2 step, predicted 0/400 (Agent6 recorded 400/400); step of the release after the last channel-0 whiff; step at which the neutral odour is held.
- **(c) No false release (stub, 400 rows, 600 steps):** a constructed hold (valued, then neutral, as (b)) with its own channel fed at p 0.30 and at p 0.057, the other channel silent, Agent10g. A false release = a hold ended by the timeout path whose first drive step comes RESET_AFTER steps or fewer after the held odour's last whiff or the hold's formation. Statistic: rows with no false release; bar lower bound >= 0.95; predicted 400/400 at both rates (by code: the drive starts only when the counter exceeds 40, and the counter counts from the last hit or formation).
  - Reported: legitimate releases (gap >= 41 in the feed) per row. Arithmetic: expected gaps of 41 or more per row = 600 x p x (1 - p)^41 = 8e-5 at p 0.30 and 3.1 at p 0.057 ((0.943)^41 = 0.090 of inter-whiff gaps). **At p 0.057 the registered timeout ends such holds by design; that is RESET_AFTER 40, not a false release** (section 12, point 6). A released valued hold re-forms on the next single whiff; a released neutral hold needs about 2 consecutive whiffs (p^2 = 0.003 per step at 0.057), so it mostly stays released.
- **(d) Realistic silent gaps (World7, bench seeds, 400 x 600, Agent6 and Agent8; reported, not a gate).** The recorded outputs hold no gap distribution (only totals), so it is measured here, before any development run: the distribution of the held odour's silent gaps while held; base firings on a hold, split into genuine (41 steps since the held odour's last hit or the hold's formation) and stale (F2); rows with no firing on a hold (the size of identity (b)'s class); what Agent10 / Agent10g do at each. Prediction: firings on a hold about 4000 to 4400 per arm (recorded 4378, 4176, 4304); the stale share has no recorded number. The uniform-counter arithmetic (a formation counter uniform on 0 to 40, no hit before it elapses) gives about 0.37 of holds formed from nothing at p 0.057 and about 0.06 at p 0.30 exposed to a stale firing without Z.
- **(e) The H19 silence-timeout bench protocol re-run (ph14b; seeds 9600/9700 as recorded, 2400 steps, neutral condition).** The agent is Agent4 at G 0 with zero values, which is Agent3 (recorded identity, ph16 identity_agent3), with and without Release. Construction: the base reproduces ph14b 1a (8652 timeout requests, median 1 step, 0.2% released; 761 evidence requests, median 3, 100%) and 1b (the circuit table; the circuit is untouched). With the fix: of timeout drives started on a held unit and not interrupted by a hit or the evidence release, the fraction that releases; bar lower bound >= 0.95; predicted 100%, median D 4.
- **No-candidate rule:** if any identity ((a1) to (a5)) is False, or any bar in (b), (c), (e) fails, the change as specified does not do what section 3 says; the tasks are NOT run and the design returns to the owner. (b4) and (d) are reported and do not stop the tasks.
- The bench also prints, on bench seeds, T3a's ceiling and floor dwells, the span and the per-row paired sd, and restates M7(b)'s pass probability from them (section 7). The bar is not changed by these numbers.

## 5. Tasks, stated in full

**T1, the H21 choice task (= H20 Run 2 task, unchanged).**
- Geometry: two sources at the same downwind coordinate, SEP 10 apart crosswind, in a 160 x 160 translated arena (walls at least 68 from either source); a wall reflects the heading and triggers the bump reflex (flee side and cast side flip).
- Plume: a whiff from source k with probability 0.30 exp(-d_along / 12) per step, inside the cone 0 < d_along < 25 and |d_cross| < 1.5 + 0.25 d_along, or within 3.0 of the source; independent per source per step. Speed 0.6; reached within 3.0.
- Start: on the midline, 20 downwind, heading uniform; each plume has p 0.057 at the start.
- Balance: 2 x 2 (valued odour A/B x valued side +y/-y), 100 rows per cell, permutation seeded with world seed + 10000; initial cast side per row from agent seed + 20000, the same in every arm. 600 steps, 400 rows, no relocation.
- Agent constants as adopted: upstream n 1.5, sigma 0.05, Rmax 1.8, k 0.8, tau 2; circuit 2 units, theta 1, k 12, g 2, w_i 1, tau 10, pool tau 2, noise 0.01, S_MAX 5; RESET_AFTER 40, MARGIN 0.2, reset amplitude 10; cast period 30, MAXOFF 170; turn 0.6 x error clipped at 40 plus noise 6; ring RingExact tau 1, sigma 0.5, n 16; gain 1 + 2 max(v, 0); the H21 gate; the H23 filter where stated.
- Main measure: dwell_k = steps within 3.0 of source k; choice = the larger dwell; a tie = no choice. Every row is V, N or tie.

**T2, the absent-odour world W1 (as the absent-odour check, unchanged).** World7 with the valued source's column set to False after World7 draws it (ph22.Masked); the random stream consumed as World7's, checked against an unmasked twin every step. Read-out A +1 / B 0; only B present. Start World7's. 600 steps, 400 rows.

**T3a, lost at the valued source (constructed; the bars).** ph22.Masked with the valued column masked from step 0 (the valued plume is gone). Start: placed at the valued source (w.pos = the valued source, World7's heading), valued hold constructed (s_valued 2.0), counter 0: the state H24's T3 found most rows in at the loss. Values +1/0. 600 steps, 400 rows, T1's seeds. Why constructed: in H24's T3 the arms were in different states at the loss (H24 design v3 section 12, point 3), so a behavioural bar there measured the pre-loss state. Here every arm starts in the same state, and the only neutral information is found by search: the valued source lies outside the neutral cone and 3.0 disc (H24 design v3 section 5), so the neutral whiff rate there is exactly 0.
- Measure: D = steps within 3.0 of the neutral source over steps 100 to 599 (the predicted release is at step 44; the window starts 56 steps later).

**T3b, 'sensed then lost' (H24's T3, reported).** ph23.Lost: World7 on steps 0 to 149, valued column masked from t0 150 (the run loop's step index). T1's seeds; each arm's T3b run == its T1 run before t0. Reported: neutral dwell 400 to 599; in rows holding the valued odour at t0, the step the valued hold ends relative to the counter's origin (the last valued hit or the hold's formation), predicted <= +49.

## 6. Arms

| task | arm | agent | values | role |
|---|---|---|---|---|
| T1 | filter-fix | Agent10 | +1/0 | regression of the adopted agent (M2) |
| T1 | filter | Agent8 | +1/0 | reference; identity (M2 a) |
| T1 | maintain-fix | Agent10g | +1/0 | the fix's cost in the gate agent (M6, reported) |
| T1 | maintain | Agent6 | +1/0 | reference for M6 |
| T1 | pathway-off | Agent8 G 0, gate off, filter off (= Agent3) | +1/0 | floor (M1 c) |
| T1 | known-answer | Agent5, held fixed to the valued odour | +1/0 | ceiling (M1 d) |
| T1 | neutral | Agent10 | 0/0 | side balance (M1 b) |
| T2 | filter-fix, filter | Agent10, Agent8 | W1 +1/0 | identity (M5 a) |
| T2 | maintain-fix, maintain | Agent10g, Agent6 | W1 +1/0 | identity (M5 b) |
| T3a | maintain-fix | Agent10g | +1/0 | main (M7) |
| T3a | ceiling | Agent5, held fixed to the neutral odour from step 0 | +1/0 | ceiling (M7 b) |
| T3a | maintain | Agent6 | +1/0 | floor (M7 b): never releases (record) |
| T3a | filter-fix, filter | Agent10, Agent8 | +1/0 | M7(a) for Agent10; trajectory identity; reported |
| T3b | maintain-fix, maintain, filter-fix, filter | as above | +1/0 | reported |
| T3b | ceiling | Agent5, held fixed to the valued odour before t0, to the neutral from t0 | +1/0 | reported |

Agent5's fixed path does not run the circuit (ph17 lines 55-66), so it skips the circuit's noise draw: the ceiling is paired with the other arms by row and world, not bitwise.

## 7. Criteria

General rules: one statistic per criterion; Wilson intervals for proportions; paired percentile bootstrap over rows, 5000 resamples, seed 20261033; 95 percent. One evaluation, no extension. A group under 50 rows is unreadable. Aggregation: PASS if every part passes, FAIL if any fails, else INCONCLUSIVE. Pass-probability arithmetic as H23's (normal approximation; for a proportion, the probability that the Wilson lower bound clears the bar at the predicted rate).

- **M1 T1 validity (else UNREADABLE):** as H23. Ties <= 0.20 in pathway-off and known-answer; neutral side balance within [0.35, 0.65]; pathway-off P(V | chose) within [0.35, 0.65]; known-answer P(V) lower bound >= 0.85. Pass probability > 0.99 (H23 design v2, section 7).
- **M2 T1 regression, adopted agent.**
  - (a) Agent10's trajectory == Agent8's on every row (POS, HEAD, NAV, SINCE, TGT). Identity; pass probability 1 if F3 holds (it is also M3).
  - (b) Agent10 P(V), Wilson lower bound >= 0.88 (H23's bar). At P 0.953 (H23 evaluation) the bound clears with probability > 0.999; at 0.93 (the lower edge of H24's filter prediction) about 0.93 (k >= 365 of 400 needed; mean 372, sd 5.1).
  - Reported: DP Agent10 - Agent8 (predicted 0 exactly); lost rows (no whiff of either plume in the last third) and wall contacts (predicted equal row for row); valued holds ended (predicted many: recorded firings on a hold 4176 per 400 rows in H23's filter arm, 1 ended).
- **M3 identities (implementation; a failure is fixed before the evaluation, section 8):** section 4 (a1), (a2), (a3) on the evaluation seeds, for every T1, T2, T3a, T3b arm pair they name; T3a / T3b constructions.
- **M4 mechanism bench:** section 4, re-run with the bench seeds at the evaluation.
- **M5 T2 regression (W1).**
  - (a) Agent10's dwell == Agent8's row for row; (b) Agent10g's dwell == Agent6's row for row. Identities (section 3); pass probability 1. Agent6's tracking cannot worsen; Agent8's absent-odour cost (bench seeds: 12.3 against Agent6's 25.8) is not removed by this change (only a presence scope touched it, H24).
- **M6 T1 cost in the gate agent (a REPORTED quantity, no bar; section 12, point 5; not part of the PASS condition):** DP = P(V) Agent10g - Agent6, same rows, with its interval; lost rows and contacts, paired. Prediction from H21's recorded conversion: P(V | first hold valued) 272/280 = 0.971 with the gate against 201/280 = 0.718 without it; P(V | first hold neutral) 28/120. If the fix keeps conversion near 0.9 (a valued first hold is whiffed often enough on the approach: gaps of 41 or more are 0.090 of inter-whiff gaps at the start's p 0.057 and about 0 at the source), P(V) = (280 x 0.9 + 28) / 400 = 0.70, DP about -0.05; if conversion falls to the ungated 0.718, P(V) = 0.57, DP -0.18. Range [-0.18, 0], centre -0.05, kept as the prediction. Not a bar because no measured rate narrows it (section 12, point 5).
- **M7 T3a, the behaviour under test.**
  - (a) Release, Agent10g and Agent10, every row: the valued hold ends at a step <= 49 with both units <= 1.0 at the end step. Statistic: rows exact; bar Wilson lower bound >= 0.95. The neutral input is gated while the valued odour is held and the valued input is 0, so the only exit is the timeout; predicted 400/400 at step 44; the bound clears with up to 11 misses in 400.
  - (b) Tracking: R = (mean D_Agent10g - mean D_floor) / (mean D_ceiling - mean D_floor), T3a window 100 to 599, bootstrap over rows (the three arms resampled together). Bar: lower bound >= 0.50 (the fix recovers at least half of the span between an agent that never releases and one that knows at once which odour to track).
  - Readability: the span D_ceiling - D_floor, paired bootstrap lower bound >= 5.0 steps; else M7(b) is UNREADABLE and H25 INCONCLUSIVE at best.
  - Prediction: after the release Agent10g navigates by the same rule as the ceiling on neutral whiffs (nothing held: any non-negative whiff, ph19 line 63; then a neutral hold: hit on the neutral odour), and before it the two differ only on neutral whiffs, whose rate at the valued source is 0. The lag is about 45 steps, before the window. Centre R 0.9, lower edge 0.6. This is reasoning from the code and the geometry, not a measured rate; the ceiling and the floor have no recorded T3a value.
  - Pass probability, se_R about (sd_d / sqrt(400)) sqrt(1 + R^2) / span, with sd_d = 10 steps (the scale of H24's recorded paired sds: 10.3 over 600 steps in W1, 5.1 over 200 in T3): span 10 -> centre > 0.99, lower edge 0.40; span 5 -> centre 0.85, lower edge 0.14. Bench prints the span and sd on bench seeds and restates these before the development run; the bar does not move.
- **M8 T3b (REPORTED):** neutral dwell 400 to 599 per arm; the paired Agent10g - Agent6 and Agent10g - ceiling differences; release timing in rows holding the valued odour at t0.

**Verdict.** H25 SHOWN under its registered criteria if M1 PASS and M2, M3, M4, M5, M7 PASS; UNREADABLE if M1 fails (or M7(b)'s span is unreadable, section 8); otherwise, by the aggregation rule over M2, M3, M4, M5, M7, NOT shown (a FAIL) or INCONCLUSIVE. M6 and M8 are reported quantities and are not part of the PASS condition. Joint pass probability: centre about 0.99 x (0.85 to 0.99) = 0.84 to 0.98; lower edge about 0.99 x 0.93 x (0.14 to 0.40) = 0.13 to 0.37, dominated by M7(b)'s unmeasured span.

## 8. Unreadable conditions

- M1 failing.
- M7(b)'s span below 5.0 steps (lower bound).
- A group under 50 rows.
- M3 failing: an implementation error, fixed before the evaluation.
- M4 not run or not passed: the tasks are not run.

## 9. Seeds, sizes, order

Sizes: T1 7 arms x 400 x 600; T2 4 arms; T3a 5 arms; T3b 5 arms; bench (b), (c) 400 rows, (d) 400 x 600, (e) as ph14b.

**Seeds:** development world 9896, agent 9996; evaluation world 1805, agent 1905; bench 20261031 / 20261032; bootstrap 20261033. Derived: 19896 / 29996, 11805 / 21905 (cell permutation, cast draw), 20271031 / 20281032, 30261031 / 40261032 (checked). T1, T2, T3a and T3b share the development and evaluation seeds.

Check done 2026-09-23: every file under the repository, recursive, .git and __pycache__ excluded (145 files), pattern: the number with no digit on either side, for all fifteen numbers above. No file contains any of them. Excluded by name: ph24.py, ph24_*.txt, h25_*.md, master_plan.md, notes/*.md (master_plan.md and notes/module_boundary_outlook.md checked separately: no match). Rejected while choosing: 9890, 9990, 1795 (in the absent-odour check, H20, H23, H24 documents), 9995 (in src/regress_result.json). vinc_search in the team space for the numbers: no keyword match. Re-used on purpose and read for no criterion: 9600/9700 (bench (e), the recorded H19 protocol), 1725/1825 and 1765/1865 (bench (a5), reproduction).

The code's self-check (ph24.py) repeats the scan before the first run, with the same exclusions.

**Order:** 1. the owner confirms (section 12) -> FINAL. 2. ph24.py (Release, Agent10, Agent10g, the T3a start; no adopted module edited). 3. Self-checks. 4. Bench (M4). 5. Development run (operation errors only). 6. One evaluation (T1, T2, T3a, T3b). 7. Report. No bar decision between bench and development run: every bar is fixed here. Nothing changes after the table.

## 10. Predictions, with the arithmetic

- **Bench:** (b) 400/400 end at step 44 (first drive at step 41, when the counter reads 41; D 4 from ph14b 1b); (b4) 0/400 kept; (c) no false release (code); at p 0.057 about 3.1 legitimate releases per row; (d) about 4000 to 4400 base firings on a hold per arm; (e) base reproduced exactly, fix median D 4, 100% released.
- **T1:** Agent10 = Agent8 row for row; Agent8 P(V) on new seeds 0.93 to 0.97 (H23 dev 0.932, evaluation 0.953). So H23's adopted result is unchanged by this change; on H23's seeds Agent10 gives 381/400 (bench (a5)). Circuit records change: valued holds ended goes from about 0 to many. Agent10g - Agent6 DP [-0.18, 0], centre -0.05 (M6).
- **T2:** identities; dwell as the recorded bench values' order (Agent8 12.3, Agent6 25.8 on bench seeds).
- **T3a:** M7(a) 400/400 at step 44 for Agent10g and Agent10; R centre 0.9, lower edge 0.6; Agent10 and Agent8 identical in trajectory and blind to the neutral odour (D near the floor).
- **The gate's 'never lost (0/280)':** no longer true in either fixed agent; valued holds end after 41 silent steps. In Agent10 this changes no behaviour; in Agent10g it is M6's cost and M7's benefit.
- **What would make the predictions wrong:** a held state at the drive's start far from ph14b's (D above 8); F3 wrong (then M2(a) fails at the bench, a no-candidate stop); the ceiling's search from the valued source slower or faster than expected (span, M7(b) readability); M6's conversion outside [0.718, 0.97].

## 11. What this design does not test

- Learning (H20 Stage B); other values; other G; other geometries or starts.
- Another RESET_AFTER, amplitude or the evidence release; the one-step drive while nothing is held (unchanged).
- The H24 presence counter on top of the fix (the (v-p) re-attempt): proposed by the interpreting assistant at the H24 closure, not decided. It is the route by which the fix could reach the full agent's behaviour, since Agent8 at +1/0 does not read the hold.
- Whether a fly's hold ends this way: no fly finding is cited or claimed.

## 12. Decisions the owner confirmed (2026-09-23)

The owner confirmed this section of v1 as recommended by the orchestrating assistant, in the owner's words: **'추천안으로 확정'** ('confirmed as recommended'). The nine points, as confirmed:

1. **The mechanism: (S) + (Z)** (section 3): (S) keep delivering the existing 10.0 reset drive while any unit is above 1.0 after the drive step, stopping early on a hit of the held odour or an evidence release; (Z) zero the silence counter on the step a hold forms. Chosen against (S) alone (identity class the same, but F2 leaves stale-counter releases of recently whiffed holds: arithmetic about 0.37 of holds formed from nothing at p 0.057), (K4) and (A40) (both change every nothing-held firing).
2. **Which agent carries the behaviour.** Agent10g (= Release + Agent6, the H21 gate agent + the fix) is the main behavioural arm (T3a); Agent10 (= Release + Agent8) is the identity and regression arm. In Agent8 the fix is behaviour-inert at +1/0 (F3; H24 design v3 already stated it for T3). The owner's premise that the fix will change the H21/H23 runs holds for the circuit records, not for Agent8's trajectories.
3. **Identity (b) as restated** (section 3): every recorded field except the counter's own value equals the base agent's on every step up to the row's first base timeout firing while a unit is above threshold; a row with no such firing is bitwise the base throughout. The gloss 'whiffed at least every RESET_AFTER steps' differs on stale-counter firings (F2), counted in bench (d).
4. **T3 as T3a (constructed loss at the valued source; the bars M7(a), (b)) plus T3b (H24's Lost world, t0 150; reported),** with the ceiling (Agent5 fixed to the neutral odour) and floor (Agent6); R = (D_Agent10g - D_floor) / (D_ceiling - D_floor), bar lower bound >= 0.50, readable only if the span's lower bound >= 5.0.
5. **M6 (Agent10g - Agent6 on T1, the cost in the gate agent) is a REPORTED quantity, not a bar;** its predicted range [-0.18, 0] (centre -0.05) is kept as the prediction. The alternative not taken was a bar DP >= -0.10 (pass probability at the centre -0.05 about 0.7 if 0.05 of rows move into V and 0.10 out, se 0.019; at the lower edge -0.18 about 0).
6. **At p 0.057 the timeout ends a fed hold when a gap reaches 41 (0.090 of gaps):** releases at gaps >= 41 are legitimate (the registered constant RESET_AFTER 40), not false releases; keeping such holds would need another RESET_AFTER (a constant, outside this change).
7. **Bench (d) (the silent-gap distribution) on bench seeds** replaces the 'dev-seed diagnosis first': the recorded outputs hold no gap distribution.
8. **The seeds** (section 9): development 9896/9996, evaluation 1805/1905, bench 20261031/20261032, bootstrap 20261033; and the reuse of 9600/9700, 1725/1825, 1765/1865 (the H19, H21 and H23 evaluation seeds) for reproduction and identity checks only.
9. **The order** (section 9).

**Changes from v1.** Status set to v2 FINAL; section 12 records the owner's confirmation with the quote and the nine points; M6 is stated as a reported quantity with no bar, its predicted range [-0.18, 0] kept as the prediction; the verdict sentence states the aggregation over M2, M3, M4, M5, M7 and that M6 and M8 are not part of the PASS condition. Nothing else changes: the mechanism, bench, tasks, arms, criteria M1-M5, M7, M8, bars, seeds and order are v1's.

## 13. Self-review (2026-09-23)

- **Every assumption about the circuit's dynamics is backed by a recorded bench or a code line** (H24 failed exactly there). Release needs D 4 at 10: ph14b 1b (recorded). No rebound after the stop: ph14b 1b D4 (lowest 0.06, released 100% 30 steps later). No flip during the drive: ph2 lines 34, 38, 39 with ph14b 1a's recorded pool peak 6.99 and the input bound 5.4; this is arithmetic on code, checked by bench (b). The sustain stopping point equals ph14b's D4 only from a similar state (held s about 2); bench (b) measures D in the agent. Agent8's hold-independent navigation: ph21 lines 67-72 (and H24 v3 section 6). The stale counter (F2): ph19 lines 53-66, ph21 lines 59-76; its size is not recorded, only estimated, and bench (d) measures it. The one number not from a bench or a code line is M7(b)'s prediction (centre 0.9, edge 0.6), stated as reasoning.
- **Are T3's bars readable?** M7(b) is relative to a ceiling and a floor run in the same evaluation, with a registered readability floor on their span, not to a pinned reference (H24's M7(c) against Agent6's 4.74 with S6 0.0296). The span has no recorded value; if it is under 5.0 the part is unreadable, which is foreseen here, not discovered. The ceiling is not bitwise paired (Agent5 skips the circuit's noise draw).
- **What the fix does to H23's adopted result:** nothing behavioural. Agent10's trajectories equal Agent8's (F3), so P(V) 381/400 = 0.953 is reproduced on H23's seeds and P(V) is equal on any seeds; the adoption within the tested conditions (decision:h23-filter-adopted-within-tested-conditions) stands. The H21 gate's recorded 'a valued hold is never lost (0 of 280)' does not survive the fix; the gate's protection against the neutral odour does.
- **Brief vs code, stated:** (i) the brief's regression tasks with Agent8 become identities, which are stronger than allowed gaps and cannot fail except by an implementation error; (ii) T3 with Agent10(Agent8) could not show tracking by code, so the main T3 arm is Agent10g; (iii) the gloss of identity (b) is narrower than it reads (F2); (iv) 'no false releases at p 0.057' cannot hold for gaps of 41 or more under RESET_AFTER 40 (point 6); (v) no gap distribution is in the recorded outputs (bench (d)).
- The joint pass probability at the lower edge (0.13 to 0.37) is dominated by M7(b)'s unknown span and sd; the bench restates it before the development run.
- Not tested: section 11.
