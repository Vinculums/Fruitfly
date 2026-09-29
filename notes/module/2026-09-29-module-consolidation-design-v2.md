# Module consolidation, design v2 FINAL

**Status: v2 FINAL (confirmed by the owner 2026-09-29, '확정'). Opened by decision:module-consolidation-open.**

Date 2026-09-29. Code cited at HEAD e4fe9a2 (branch codex/h12-review-plan; the source files are unchanged since 4b8a4c0,
where v1 read them). Written by an Opus 5.5 agent from static reading only: no code run, no file edited, nothing
recorded. master_plan line numbers are renumbered to e4fe9a2 (an entry of 15 lines was inserted after line 1175 and
one line near 2690; checked with grep).

**What differs from v1** (notes/module/2026-09-29-module-consolidation-design-v1.md, sha256
9ee44834b436395b097a31e7814c874fc681d55bd080d88850877bfefcb161d2): only the status and confirmation text, section 10
(every point CONFIRMED), and the four amendments of the review (notes/reviews/2026-09-29-module-consolidation-design-v1-review.md),
each marked [v2, amendment n], plus the renumbered master_plan lines. No acceptance row, field, layer, seed or constant
of v1 changes; amendment 2 ADDS one row (A7r) and relabels A7.

## 0. Status, scope, what this is and is not

- **Status: v2 FINAL.** The owner confirmed section 10 as recommended, 2026-09-29, verbatim '확정' (gloss:
  'confirmed'): decision:module-consolidation-open. Code is written against this version only.
- Opened for design by the owner, 2026-09-29, verbatim '권고안으로 진행, Q1~Q4 큐 등록하고 모듈 통합 열자' (gloss:
  'proceed as recommended; register Q1-Q4 in the queue and open the module consolidation'):
  decision:module-consolidation-open-design (master_plan.md:1166-1167, 2692-2696). It is item (b) of the consolidation
  gate's order (notes/consolidation/2026-09-29-consolidation-v2.md:357-371).
- **An engineering step with NO hypothesis.** No new behaviour, nothing adopted, nothing in the agent's behaviour
  changed. The only test is bitwise identity with the adopted agents: Agent17 (two-channel, src/ph35.py:104-105) and
  Agent16 (three-channel, src/ph33.py:180-194), as the outlook's addendum names them (notes/module_boundary_outlook.md:77-82).
- **Accepted only if it IS the adopted agent bitwise** on every field listed in section 6. A float difference of one ulp
  is a failure.
- **Not tested here: reuse outside the fly world.** The outlook's caveat stands (notes/module_boundary_outlook.md:64-66):
  a new body means a new input contract, benched before use. Nothing here is a claim about another body.
- The outlook's own condition 'Not now. No caller exists' (notes/module_boundary_outlook.md:70) is set aside by the
  owner's decision above. No caller is claimed; section 1 says what the module would make possible without promising it.

## 1. Purpose, from the record

| Item | Record |
|---|---|
| Why fold | the reusable part is the recognition-value core, not the navigation; the fly body is the first test bed (outlook:3, 5-13); 'fold the chain into one file at the adopted constants; acceptance = bitwise identity' (outlook:71) |
| Why now | consolidation gate (b): 'its only test is bitwise identity, so it can fail only by finding an inconsistency in the chain, which would be worth knowing before (d) or (a) composes the agent again' (consolidation-v2:369-371) |
| Two forms rule | 'a future design must say which form it composes' (master_plan.md:2184-2186). This module composes BOTH, selected by one constructor argument (section 4.3) |
| G 2 | carried in every adopted scope with no adopting decision; 'whether it is adopted state is the owner's, unsettled' (master_plan.md:2040-2046) |

What it would make possible later, promised for none of them: Q1-Q3 designs (master_plan.md:2705-2711) could compose
against one numpy-only file instead of a 25-file import chain with run-time hooks; a caller outside the fly world could
import it (subject to section 0's caveat); the end-to-end chain of outlook section 7 (reinforcement, credit, read-out,
behaviour in one body) could be read in one file. Section 3 shows that one part of that chain, the address of the
credit, is not what the outlook says it is.

## 2. The current chain, as read at 4b8a4c0 (unchanged at e4fe9a2)

**Import chain, one line (Agent17's file, left to right):** ph35 -> ph34b -> ph30 -> ph28 -> ph25 (and ph25b) -> ph24
-> ph23 -> ph22 -> ph21 -> ph19 -> ph18, ph17 -> ph16 -> ph15 -> ph14 -> ph13 -> ph12b -> ph12 -> ph11 -> ph10, ph9,
ph8 -> ph4, ph3, ph2 -> ffcore. Agent16's file adds ph33 -> ph32 -> ph30 (src/ph33.py:81-95, src/ph32.py:84-98).
ph17 and ph18 are imported for harness helpers only (Agent5, majority); no adopted class uses them.

### 2.1 Two-channel form: Agent17, method resolution order

MRO (asserted in src/ph35.py:385): Agent17, Agent14N2, ReleaseN2, Agent14, Release, Agent9, Agent8, Agent6, Agent4,
Agent3, Agent2, Agent (ph11).

| Class | Defined | What it adds | Live in the adopted path |
|---|---|---|---|
| Agent17 | src/ph35.py:104-105 | nothing (empty body); built with P 60, N_hi 200 by the hook src/ph35.py:111-115 | class only |
| Agent14N2 | src/ph30.py:139-140 | nothing (composition) | class only |
| ReleaseN2 | src/ph30.py:117-136 | (S)/(Z) only at non-negative held value; calls the base act via super(Release, self) (:124) | act :121-136 |
| Agent14 | src/ph28.py:92-97 | P, N_hi; counter start N_hi - P (:97) | __init__ |
| Release | src/ph24.py:47-63 | release flag, sustain, zreset | __init__ :50-52; its act is bypassed (ph30.py:124) |
| Agent9 | src/ph23.py:52-104 | presence counter c, present, scope, N | __init__ :55-58; **act :60-104 is THE base act** |
| Agent8 | src/ph21.py:42-84 | filt flag, H23 filter | __init__ :46-48; act overridden |
| Agent6 | src/ph19.py:37-74 | gate flag stored in `rule` (:42) | __init__; act overridden |
| Agent4 | src/ph16.py:64-101 | G, yp, tgt, due_* | __init__ :70-73; act overridden |
| Agent3 | src/ph14.py:45-97 | fix, nav_hit; chan_valence :52-55 | chan_valence live; act dead |
| Agent2 | src/ph13.py:47-99 | cast, rot_in, est; estimate fed w.rot :56-61 | estimate live; act dead |
| Agent (ph11) | src/ph11.py:106-206 | up, sel, ring, mb, codes, timers, flee_side, cast_sign | __init__ :110-128, bump :130-141, held :143-145; act, estimate dead |
| Upstream | src/ph2.py:5-17 | Heeger stage | step |
| Circuit | src/ph2.py:19-42 | bistable circuit; sigmoid ffcore.py:5-6 | step |
| RingExact | src/ph10.py:44-78 | ring; cue src/ph3.py:36-41 | step, pos |
| MB, MB4 | src/ph4.py:18-63, src/ph8.py:40-99 | learning module (single site, gated) | valence, step |

Worlds (not agent): World7 src/ph16.py:43-56 <- World5 src/ph14.py:30-42 <- World4 src/ph13.py:33-44 (move is
World3.move, src/ph12b.py:46-61) <- World2 src/ph11.py:56-103; W1 is ph22.Masked (src/ph22.py:37-44); T3b is ph23.Lost
(src/ph23.py:112-119). Harness: ph35.run -> ph28.run (src/ph28.py:136-137) -> ph25.run (src/ph25.py:79-82) ->
ph24.run (src/ph24.py:113-149); fields recorded by ph24.record (:100-104) and ph25.record (src/ph25.py:63-73).

### 2.2 Three-channel form: Agent16

MRO: Agent16, ReleaseN2, Agent14, Release, Act16, Act15, Agent9, ... Agent (checked in the ph33 demo,
src/ph33.py:645-646). ReleaseN2's base act resolves to Act16.act.

| Class or function | Defined | What it adds | Live |
|---|---|---|---|
| Agent16 | src/ph33.py:180-194 | after the two-channel constructor: stage chans 3, Circuit3 n 3, code odour(103), counter (R, 3) at N_hi - P, burst record | __init__ |
| Act16 | src/ph33.py:116-177 | burst record :142-151, ranked top set :155-158, keep :161, t16 :176 | **act, THE base act** |
| Act15 | src/ph32.py:152-203 | hold_read class attribute :156 | act overridden |
| Circuit3 | src/ph32.py:125-142 | units 3.. noise on rng3 (:138-139) | step |
| evidence_due | src/ph32.py:145-149 | H27 composition rule | called at ph33.py:128 |
| build | src/ph33.py:205-209 | rng3 = default_rng(seed_a + A3_OFF), N_hi 300 via ph32's N_HI | harness |
| run | src/ph33.py:226-255 | D whiff from its own generator (world seed + D_OFF), :233, :242 | harness |

### 2.3 Every constant, where it is fixed

Core (recognition, value memory, read-out). N = number of constants in the row.

| Group | Constants | Fixed at | N |
|---|---|---|---|
| Upstream | n 1.5, sig 0.05 (sig**n formed at run time), Rmax 1.8, k 0.8; tau 2.0 (default) | src/ph11.py:112; src/ph2.py:9-10 | 5 |
| Circuit | n 2, theta 1.0, k 12.0, noise 0.01 | src/ph11.py:113 | 4 |
| Circuit defaults | w_i 1.0, g 2.0, tau 10.0, tau_g 2.0, pool_p 1.0, pool_c 1.0, gsat None; DT 1.0, S_MAX 5.0 | src/ph2.py:23-25 | 9 |
| sigmoid | clip -60..60 | ffcore.py:6 | 1 |
| Hold and release | hold = one unit above 1.0 | src/ph11.py:144 | 1 |
| | RESET_AFTER 40, MARGIN 0.2 | src/ph11.py:39 | 2 |
| | reset drive 10.0 | src/ph23.py:72 | 1 |
| | (S) silence set to RESET_AFTER + 1.0 | src/ph24.py:62; src/ph30.py:135 | 1 |
| | N2 test 'held value < 0.0' | src/ph30.py:128-129 | 1 |
| Switches, all on | G 2.0 (G_STAR), gate, filter, scope 'prior', release | src/ph21.py:27; src/ph24.py:93; src/ph25.py:48 | 5 |
| Learning module | K 200, C 4, sparsity 0.05, eta_d 0.10, eta_p 0.30, beta 0.15 | src/ph11.py:53 | 6 |
| | tau_code 5.0, tau_reinf 5.0, w0 1.0, wmin 0.0, wmax 2.0 | src/ph4.py:19-20 | 5 |
| | parallel False, gated True | src/ph11.py:115 | 2 |
| | code seeds 101, 102 | src/ph11.py:116 | 2 |
| Presence | P 60; N_hi 300 | src/ph28.py:72 | 2 |
| | N_hi 200 (two-channel form) | src/ph35.py:89 | 1 |
| | counter start N_hi - P (140 or 240) | src/ph28.py:97 | 1 |
| Three-channel | chans 3 and circuit n 3; code seed 103 | src/ph33.py:187-189 | 2 |
| | WIN 9; NEVER -1.0e9 | src/ph33.py:105-106 | 2 |
| | rng3 offset A3_OFF 30_000; hold_read True | src/ph32.py:109; src/ph33.py:183, 207 | 2 |

Body, agent side (the heading ring and the controller):

| Group | Constants | Fixed at | N |
|---|---|---|---|
| Ring | n 16, noise 0.3 | src/ph11.py:114 | 2 |
| | J 0.5, c 2.0, p 2.0, sigma 0.5, Rmax 2.0, width 1.2, tau 1.0, vgain 1.0 | src/ph11.py:52 | 8 |
| | DT 1.0 | src/ph10.py:50 | 1 |
| Wind cue | WIND_CUE 6.0; cue width 1.2 | src/ph11.py:51; src/ph13.py:60 | 2 |
| Controller | UPWIND 180.0 | src/ph9.py:33 | 1 |
| | CAST_PERIOD 30, CAST_GROW 1.2, MAXOFF 170.0 | src/ph9.py:40 | 3 |
| | GAIN 0.6, MAXTURN 40.0, TURN_NOISE 6.0 | src/ph9.py:41 | 3 |
| | SAT = MAXOFF/CAST_GROW (formed at run time, not the literal 141.7) | src/ph12.py:29 | 1 |
| | flee sides {90.0, 270.0}; cast_sign starts +1 | src/ph11.py:127-128 | 2 |

World and harness (stay in the phN chain under the recommendation of section 4.1): ARENA 40, HIT_R 3.0, SPEED 0.6,
STEPS 600 (src/ph9.py:31); W0 1.5, SLOPE 0.25, LAM 12, LMAX 25 (src/ph9.py:34); p_hit 0.3, p_wind 1.0
(src/ph11.py:59); at-source radius 3.0 (src/ph11.py:81); arena 160, shift 60 (src/ph13.py:37); SEP 10, DOWN 20, R 400
(src/ph16.py:24); T0 150 (src/ph23.py:34); P_D 0.03, D_OFF 30_000 (src/ph32.py:103, 109); cast draw at agent seed +
20_000 (src/ph16.py:35-40); cell permutation at world seed + 10_000 (src/ph16.py:50). N = 21.

**Count: 55 core + 23 agent-side body + 21 world and harness = 99 constants.**

## 3. The boundary, function by function

Outlook blocks (outlook:5-13, 44-50): core = upstream stage, Select-and-Hold with H19 (a), G 2, H21 gate, N2 release,
value memory with the extinction gate, read-out (filter, presence counter, three-channel additions, flee); body = world,
whiff generation, surge-and-cast with the return cast, the ring and its input contract, the wind cue, the arena.

| Code (live act, src/ph23.py unless named) | Lines | Side |
|---|---|---|
| stage, G 2 gain, H21 gate | :62-67 | core |
| timeout and evidence due, reset, circuit step, held | :68-75 | core |
| estimate: two ring steps (rotation made, then cue) | :76 -> src/ph13.py:56-61 | body |
| val of the held odour (from `known`), hit | :77-78 | core |
| presence counter, v_max, top set, keep, nav | :79-94 | core (read-out) |
| silence counter update | :96 | core (release clock) |
| cast clock `since`, offset, target | :95, :97-99 | body |
| flee override of the target | :100 | mixed, see U4 |
| turn noise, last_turn | :101-103 | body |
| ReleaseN2 post-act | src/ph30.py:123-136 | core |
| bump | src/ph11.py:130-141 | mixed, see U5 |
| learning step | src/ph30.py:235-238 via src/ph15.py:55-61 | harness, see U7 |

**Unclear places in code (named, not resolved by this design):**

- **U1. One act, one generator.** Core and body are interleaved in one method and draw from one generator in the order
  circuit, ring, ring, turn (section 5.2). A split into a core object and a body object with their own generators, or
  with the calls reordered, changes every draw. The split can be documentary only.
- **U2. The nav signal.** H19 (a), the H23 filter and the presence scope are one expression (src/ph23.py:88-92) whose
  only consumer is the body's cast clock (:95). The outlook lists H19 (a) under recognition and the filter under
  read-out; in code they are one line.
- **U3. The silence counter** is the hold's release clock (core) but is updated in the body section from `hit` (:96)
  and then overwritten by ReleaseN2 after the act (src/ph30.py:135).
- **U4. The flee.** Outlook section 3 lists it as body; the brief lists it under read-out. In code the value of the held
  odour (core, :77) replaces the body's target (:100).
- **U5. bump** flips both flee_side (the flee's exit, U4) and cast_sign (body) on a wall contact (src/ph11.py:139-141).
- **U6. Values enter through the harness.** chan_valence returns `known` (src/ph14.py:53); every live act reads
  `self.known` directly for the flee (:77), so `known` must be an array. With learning on, the harness writes
  `a.known` from the module's read-out before each act (src/ph30.py:213; readout :178-179).
- **U7. The address of the credit is the position, not the hold.** The outlook says reinforcement 'is credited to what
  is held at that moment' (outlook:29). The code credits the code of the source the agent stands at, with the
  reinforcement by which source is `good` (src/ph15.py:55-61), called by the harness after the move (src/ph30.py:235-238).
  master_plan already reads it this way ('receives an odour code only at a source', master_plan.md:2322-2324). The
  module must carry the code's behaviour; the outlook's sentence is not implemented and is not made true here.
- **U8. The outlook's K 500** (outlook:29) is Phase 4's value; the agent's module is built with K 200 (src/ph11.py:53).
- **U9. `rule` has two meanings:** the ph11 arm name 'agent' | 'random' | 'oracle' (src/ph11.py:110) and, from Agent6
  on, the gate flag (src/ph19.py:42). ph30.agentish reads it by name (src/ph30.py:186).
- **U10. 'Inert by code' at two channels holds only at unequal values.** master_plan says the H28 tie rule is inert by
  code at two channels (master_plan.md:857, 1788, 2201-2202). By reading, Act16 at two channels with EQUAL non-negative
  values (0/0, +1/+1) has two odours in the top set, so the ranked set applies (src/ph33.py:156-158); before any burst
  it is empty and no non-held whiff steers, where Agent9 would steer. H28's identity (I1') tested +1/0 and +1/-1 only
  (experiments/h28/ph33_bench.txt:27), where the top set has at most one odour. This is a reading, not a measurement;
  it does not touch the adopted scope (+1/0), but it rules out building the two-channel form through Act16.
- **[v2, amendment 1] Where U7, U8 and U10 are recorded.** The review verified all three against the code
  (notes/reviews/2026-09-29-module-consolidation-design-v1-review.md, 'Verified against the code'). None changes a
  verdict, a scope or an adoption.

  | Reading | Recorded as | By | When |
  |---|---|---|---|
  | U7 (credit by position, src/ph15.py:55-61) | an addendum to notes/module_boundary_outlook.md, its existing text unchanged; and the header of src/fly.py | addendum: the reviewing session; header: the coding agent | addendum at registration of v2; header with the code |
  | U8 (K 200 in the agent, src/ph11.py:53; K 500 is the module-level constant, src/ph8.py:37) | same as U7 | same as U7 | same as U7 |
  | U10 (tie rule at two channels) | a wording correction in master_plan at the two 'inert by code' sentences (master_plan.md:857, 1788), to read 'inert at two channels for the tested value pairs (+1/0, +1/-1)' | the reviewing session, by the owner's confirmation | at registration of v2 |

  Two more sentences carry the same claim with the phrase broken across a line: the consolidated record's section 2.1
  close (master_plan.md:2060-2062) and the architecture's two-forms entry (master_plan.md:2201-2202). The confirmation
  names two sentences; whether these two are corrected in the same edit is for the reviewing session to state at
  registration.
- **U11. The harness writes agent state:** cast_sign after construction (src/ph24.py:126), a constructed hold in T3a
  (src/ph24.py:128), `known` under learning (U6). These attribute names are part of the de facto interface.

## 4. The module

### 4.1 Files and contents

CONFIRMED (section 10 point 1): **one file, src/fly.py**, numpy only (no phN import, no ffcore import), containing the agent only: core
and agent-side body in one class, both forms. Reason: U1 (one generator, one fixed call order within a tick) makes the
core/body split a single ordering contract that a file boundary would cut in two; the outlook asked for 'one file'
(outlook:71). Not folded: worlds, harness loops, recorders and measures. They are the test environment, already the
reproducible artefact, and folding them would add a second identity surface with no caller. Not taken (section 10 point 2):
also fold World7, Masked and Lost into the same file.

Dropped from the chain because the adopted path never executes it: every act before Agent9's (src/ph11.py:156-206,
src/ph13.py:63-99, src/ph14.py:57-97, src/ph16.py:75-101, src/ph19.py:44-74, src/ph21.py:50-84), Act15.act, Release.act
(bypassed, src/ph30.py:124), the commanded-rotation estimate (src/ph11.py:147-154), the abl, fix, cast and rot switches,
prev and belief, gsat. Measurement-only attributes are dropped (confirmed, section 10 point 6): nav6, nav8, differs,
differs8 (src/ph23.py:80-81, 90, 93), n2S, n2Z (src/ph30.py:134), yp, hr, val, top15, keep15, keep16, nav15, acts
(src/ph33.py:163-164). Kept although partly measurement, because the recorded behavioural fields read them: nav_hit, tgt,
est, due_timeout, due_evidence, sustain, zreset.

### 4.2 Interface (outlook section 4 made concrete)

```python
import fly                                        # src/fly.py
a = fly.Fly(runs, rng, known, nch=2, rng3=None)   # nch 2: Agent17; nch 3: Agent16 (rng3 required)
turn, h = a.act(w, whiffs, wind_on)               # one tick; w supplies w.rot (rotation made) and w.head (for the cue)
a.bump(mask)                                      # after the world's move
a.mb.step(code=code, reinf=rv)                    # learning, called by the caller after the move (U7)
a.known = np.stack([a.mb.valence(a.codes[:, 0]), a.mb.valence(a.codes[:, 1])], 1)   # learned values, before act (U6)
```

| Outlook name (outlook:52-58) | Here | Why not a wrapper |
|---|---|---|
| perceive(evidence) -> held | the recognition section of act; a.held() | a separate call could be made out of order (U1) |
| reinforce(+1) | a.mb.step(code, reinf) | the unchanged harness ph30.Sim calls mb.step (src/ph30.py:238) |
| readout() | a.known / a.chan_valence(); the module's read-out as in src/ph30.py:178-179 | ph30.Sim writes a.known (src/ph30.py:213) |
| flybody.step(rec, v, wind, rotation_made) | the body section of act, reading w.rot and w.head | same act, same generator |
| the seed | rng (and rng3), Generators, as every harness passes them | cast_draw and rng3's offset belong to the harnesses |
| one tick scale | module constant: one tick = one world step (DT 1.0, src/ph2.py:23, src/ph10.py:50) | any other scale re-opens the benches |

Constructor arguments are exactly runs, rng, known (shape (runs, nch)), nch, rng3. Everything in section 2.3's core and
agent-side tables is a module constant, including G 2.0, P 60 and the window by form, with gate, filter, scope,
release and hold_read fixed on: exposing any of them re-opens its bench (outlook:66). The attribute surface the
unchanged harnesses read is kept by name: R, G, sel (s, S), held(), chan_valence(), known, codes, mb, cast_sign,
flee_side, silence, since, c, present, nav_hit, tgt, est, due_timeout, due_evidence, sustain, zreset (src/ph24.py:100-104,
126-130; src/ph25.py:63-73; src/ph32.py:262-271; src/ph30.py:208-265).

### 4.3 The forms switch

`nch` selects the form. nch 2 is Agent17 exactly: Agent9's act (src/ph23.py:60-104) wrapped by ReleaseN2
(src/ph30.py:121-136), window 200, start 140, ph2.Circuit noise. nch 3 is Agent16 exactly: Act16's act
(src/ph33.py:119-177) wrapped by ReleaseN2, window 300, start 240, Circuit3 noise split, three codes. The three-channel
additions sit under explicit `if self.nch == 3` branches (stage and circuit construction, codes, counter width, burst
record, ranked top set, keep). The design does NOT rely on the tie rule being inert at two channels (U10). One addition
is shared by code: evidence_due (src/ph32.py:145-149) returns y[1 - hi] - y[hi] at two channels, the same element as
src/ph23.py:68-70, so sharing it is bitwise safe for any values; H28's (I1') agrees at +1/0 and +1/-1.

## 5. What must not change

### 5.1 Constants and composition

Every constant of section 2.3, and each formed the way the code forms it (sig**n, SAT = MAXOFF/CAST_GROW, DT/tau, the
sigma**p of the ring): a literal written in place of a formed value can differ in the last bit. The G 2 composition,
(1 + G*max(v, 0)) on the stage output before the gate (src/ph23.py:62), is carried as it is; the module header states
that its adoption status is the owner's and unsettled (master_plan.md:2040-2046).

### 5.2 Random-draw order (bitwise identity depends on it)

| Generator | Draw | Where | When |
|---|---|---|---|
| agent rng | flee_side choice([90, 270], runs) | src/ph11.py:127 | construction; the only construction draw (Circuit, RingExact, MB4 store rng and draw nothing) |
| agent rng | circuit noise standard_normal((R, 2)) | src/ph2.py:40; src/ph32.py:138 | every act, first |
| rng3 | third unit standard_normal((R, 1)) | src/ph32.py:139 | every act, right after, nch 3 only |
| agent rng | ring noise (R, 16), velocity step | src/ph10.py:73 via src/ph13.py:58 | every act, second |
| agent rng | ring noise (R, 16), cue step | src/ph13.py:59-60 | every act if any row senses wind (always at p_wind 1.0); all rows draw |
| agent rng | turn noise standard_normal(R) | src/ph23.py:102; src/ph33.py:174 | every act, last |
| own rngs | codes: default_rng(101), (102), (103), one choice per row in a Python loop | src/ph4.py:29-36 | construction; must stay a per-row loop |
| harness | cast_draw (agent seed + 20_000), world, twin, D generator | src/ph16.py:35-40; src/ph24.py:118-123; src/ph33.py:233 | outside the module |

## 6. Acceptance test (M3-style identity)

**Arms.** Reference = the adopted class trees built by the existing hooks (Agent17 through src/ph35.py:111-115; Agent16
through src/ph33.py:205-209). Candidate = fly.Fly injected at run time into the same harnesses by the project's own
hook pattern (ph24.make for the two-channel harness, as src/ph28.py:100-119 and src/ph35.py:108-118 do; ph33.build for
the three-channel one). No existing file is edited; the harness, the world and every non-agent draw are the reference's
by construction. The checks reuse the form of ph24.bitwise (src/ph24.py:166-170), ph34b.every (src/ph34b.py:128-129),
ph32.every (src/ph32.py:365) and ph35's (I1) (src/ph35.py:388-391).

**Worlds, values, seeds.** 400 rows. Seeds are reused on purpose, read for no criterion: identity checks may reuse spent
seeds. They are named here by constant and report line, not written out, because this note sits in notes/module/, which
the ph33 and ph35 seed scans do read (their exclusion is basename 'notes', src/ph35.py:234, src/ph33.py:359).

| Id | Form | World | Values | Steps | Seeds (world, agent) | Role |
|---|---|---|---|---|---|---|
| S0 | both | every row below | as below | 200, 40 rows | demo seeds (5, 6) | smoke, first |
| A1-A4 | Agent17 | T1, W1, T3a, T3b at t0 150 | +1/0, learning off | 600 | ph35.SEEDS['eval'] (experiments/h29/h29_report.md:3, :126) | the adopted scope |
| A5 | Agent17 | T1 | +1/-1 | 600 | same | coverage: N2's negative branch |
| A6 | Agent17 | T1 | 0/0 | 600 | same | coverage: two-odour top set |
| A7 | Agent17 | World6, E1-C, per-step mirror of the module's read-out, learning ON | learned | 5400 | ph31.SEEDS['eval'][0] (experiments/h20/h20_stage_c_run2_report.md:3, :121) | **coverage, no recorded reference** [v2, amendment 2] |
| A7r | Agent14N2 (lineage) | World6, E1-C, ph30.e1_sim's 'learned' arm (src/ph30.py:162, 303-308), learning ON, mirror 'v' | learned | 5400 | ph31.SEEDS['eval'][0] (experiments/h20/h20_stage_c_run2_report.md:3, :121) | recorded reference [v2, amendment 2] |
| B1-B2 | Agent16 | T1D, W1D (D on, p_D 0.03) | +1/0/0 | 600 | ph33.SEEDS['eval'] (experiments/h28/h28_report.md:3, :118) | the adopted scope |
| B3 | Agent16 | T1D | +1/-1/0 | 600 | same | coverage: N2's negative branch |

A7 names the one recorded run with learning on in a behaving agent: H20 Stage C Run 2, E1-C (report :3), whose learned
arm was Agent14N2 (src/ph30.py:162). Agent17 was never run with learning on, so A7 compares Agent17's class tree with the
candidate in that harness (src/ph30.py:190-274, 303-308); it reproduces no recorded number and is labelled coverage.

**[v2, amendment 2] A7r, the recorded reference.** The module against Agent14N2's class tree (built by ph30.build kind
'A14N2', src/ph30.py:153-155) in the harness and on the evaluation seeds of the recorded learning-on run, H20 Stage C
Run 2 E1-C (ph31.SEEDS['eval'][0]; experiments/h20/h20_stage_c_run2_report.md:3, :121). The candidate is injected by a
run-time hook on ph30.build, as section 6's other rows inject theirs; ph30.py and ph31.py are not edited. Agent14N2 is
the two-channel form at window 300 and counter start 240 (src/ph28.py:72, 97), while the module's two-channel window is
the constant 200. The identity script therefore sets the candidate's window attribute N to 300 and its counter c to 240
right after construction, as the harnesses already set cast_sign (src/ph24.py:126); construction draws only flee_side
(section 5.2), so the setting is draw-neutral. It is test-only: the constructor gains no argument and section 10
point 4 stands. A7r is the one row with a recorded run behind its reference; like every row it is compared on L1, L2
and L3, not on the report's printed numbers. E2-C (report :3) is left
out: its training protocol is harness code outside the module. The three-channel form has no learning-on run and the
learning inputs handle two channels only (src/ph15.py:58-60): not tested.

**Fields, two layers, zero tolerance, every row at every step.**

| Layer | What | How |
|---|---|---|
| L1 recorded | positions, headings (POS, HEAD), circuit state (S, SG), hold (H), nav (NAV), cast clock (SINCE), target (TGT), release clock and state (SIL, TO, EV, SUS, Z), whiffs (W), at-source (AT2), contacts (C); nch 3 also VAL | the harness's own arrays, np.array_equal per field (ph28.BEHK plus SUS, Z, AT2, C; src/ph28.py:83) |
| L2 full precision | after every act and every bump: **every attribute of the agent object** (its instance dictionary, and recursively those of up, sel, ring and mb), arrays and scalars alike, plus the generator state (rng and, at nch 3, rng3 bit_generator.state) [v2, amendment 3]. Expected to include P, s, S, ring s, w, tc, tr, codes, known, c, present, since, silence, last_turn, est, tgt, cast_sign, flee_side, sustain, zreset; nch 3: bb, w2, burst, t16 | sha256 of each attribute's bytes (float64 arrays as stored) per step, digest lists compared; **the attribute names hashed are listed, per arm, in the header of identity.txt**; a name present in one arm and not the other is reported as such, not hashed; on a mismatch the first (step, attribute, row) is printed |
| L3 per-row scores | dwell per source and first reach (src/ph24.py:147-148); dwell-majority class (ph25.cls3); W1 summary (ph25.w1sum); T3a/T3b dwell (ph24.t3_dwell); T3b window reading (ph28.lost300 at W 200); T1D/W1D lost rows (ph25.lost_t1); A7 and A7r: the end-of-run record of ph30.Sim.finish (src/ph30.py:268-270) | computed from both arms' outputs with the existing functions, compared exactly |

L2 exists because L1 records SIL and SINCE as float32 (src/ph24.py:110) and the counter as float32 (src/ph25.py:68), so
L1 alone cannot see a difference below float32 resolution.

**Demos.** After the identity run, ph35.py demo and ph33.py demo are re-run unchanged. They must pass as recorded
(experiments/h29/ph35_demo.txt, experiments/h28/ph33_demo.txt); their seed scans (src/ph35.py:368, ph33 demo) then also
check that no new file carries one of their seed numbers.

**Stop rule.** Any difference in any layer stops the run. The cause is fixed in src/fly.py, disclosed in the report,
the file rehashed and every row of the table rerun from S0. Nothing is tuned; no field, row, world or tolerance is
dropped to make a row pass.

**Outputs.** experiments/module/identity.txt (LF; header with the sha256 of src/fly.py, the identity script and every
imported phN file, the numpy and Python versions, the thread pins; one line per row and layer), experiments/module/
identity.json (per row, per field: equal or not; the L2 digest lists), experiments/module/module_report.md. None of the
three writes a seed number (the script reads them from the phN constants).

## 7. What the module does not claim

- No fidelity to a fly beyond what the phN chain already has; no behaviour change; no performance or speed claim.
- No reuse validated: section 0's input-contract caveat applies to any other body (outlook:64-66).
- Identity where tested only: the rows of section 6. 'A figure measured in one starting state is not carried to another'
  (master_plan.md:2467): other worlds, values, window lengths or learning conditions are identical by code reading, not
  by this test.
- Nothing about G 2's adoption status, the tie rule's scope (U10), the credit's address (U7) or K (U8) is settled here.
- No relaxation of any stored bound is made, so no H14-format signed decision is needed (master_plan.md:2421-2423).
  P1 and P2 (master_plan.md:2623-2629) do not apply: no known-answer arm, no loop arithmetic.

## 8. Order and execution

| Step | Who | What |
|---|---|---|
| 1 | Opus 5.5 agent | v1 DRAFT (done, committed at e4fe9a2) |
| 2 | reviewing session (Fable) | review with four amendments (done, notes/reviews/2026-09-29-module-consolidation-design-v1-review.md) |
| 3 | owner | confirmed section 10 as recommended, '확정', 2026-09-29: decision:module-consolidation-open (a draft is not the owner's until the owner says so, master_plan.md:2471) |
| 3a | reviewing session | at registration: the U7/U8 outlook addendum and the U10 wording correction of [v2, amendment 1]; P5 below proposed to the owner |
| 4 | Opus agent | writes src/fly.py and src/module_identity.py; edits no existing file |
| 5 | local session (P4, master_plan.md:2632) | the identity run, one process, invocation below; S0, then every row of section 6 |
| 6 | reviewing session (P3, master_plan.md:2630) | recounts from identity.json and the stored arrays; re-runs S0 and one full row independently; checks the hashes |
| 7 | owner | decides what is recorded; nothing is recorded as adopted |

**Registered files.** Code: src/fly.py (the module), src/module_identity.py (the identity script). Outputs:
experiments/module/identity.txt, experiments/module/identity.json, experiments/module/module_report.md. No other file
is created or edited by steps 4-5.

**Registered invocation** (PowerShell, from the repository root; one process; the pool sizes pinned to 1 because the
H20 and H28 pools use fork, src/ph30.py:100, src/ph33.py:108, 261-263):

```
$env:PYTHONHOME=$null; $env:PYTHONPATH=$null
$env:OPENBLAS_NUM_THREADS="1"; $env:OMP_NUM_THREADS="1"; $env:MKL_NUM_THREADS="1"
$env:PH30_PROCS="1"; $env:PH33_PROCS="1"
uv run --with numpy==2.4.6 --python 3.11 python src/module_identity.py > experiments/module/identity.txt
```

numpy 2.4.6 and Python 3.11 are those of both recorded evaluations (experiments/h29/h29_report.md:126,
experiments/h28/h28_report.md:118). The identity compares two arms inside one process, so it does not depend on the
interpreter; the header prints both versions. The script calls sys.stdout.reconfigure(newline="\n") so the output is LF.

**[v2, amendment 4] Seed digits in notes/ and experiments/module/.** No design, review or report under notes/ (at any
depth) or under experiments/module/, and no output of src/module_identity.py, carries the digits of a registered seed
of ph33 or ph35, or of any number their seed scans derive from one (src/ph35.py:218-223, src/ph33.py:342-347): those
scans skip a .md file only when its folder's basename is 'notes' (src/ph35.py:234, src/ph33.py:359), so they read
notes/module/ and experiments/module/. Seeds are named by constant and report line, as this design does; a
master_plan or file line number equal to such a number is cited by a range whose ends differ from it. Proposed to the
owner as a standing note in the P1-P4 form (master_plan.md:2623-2632):

- P5 (proposed, not the owner's until confirmed): a design, review or report outside the files a hypothesis's own seed
  scan excludes by name names every registered seed by its constant and a report line, never by its digits, and is
  checked against every registered and derived seed number before it is committed. (From the module consolidation
  design, notes/module/2026-09-29-module-consolidation-design-v1.md section 6.)

## 9. Risks for bitwise identity, from the code

| Risk | Reading | Guard |
|---|---|---|
| Draw order | four agent draws per act in a fixed order, the cue step drawing for every row (section 5.2) | keep the order and the shapes; L2 compares rng states every step |
| Circuit3 at nch 3 | draws (R, 2) from rng then (R, 1) from rng3 and concatenates (src/ph32.py:138-139); one (R, 3) draw differs | copy verbatim |
| Float summation order | the circuit input is y + g*sigmoid + w_i*q - w_i*S + noise*z in that order (src/ph2.py:39-40); the stage's others = (sum - P)/max(N - 1, 1) (src/ph2.py:16); einsum subscripts in the ring (src/ph10.py:73) and in MB.out (src/ph4.py:39) | same expressions, same einsum strings; no matmul rewrite |
| Formed constants | SAT (src/ph12.py:29), sig**n (src/ph2.py:10), sigma**p (src/ph10.py:76) | form them as the code does |
| In-place updates | Upstream P += (src/ph2.py:14), Circuit S and s += (src/ph2.py:38, 41), MB tc and tr += (src/ph4.py:61-62); the harness writes sel.s in T3a (src/ph24.py:128) | keep in-place semantics and the sel.s name; L2 copies before hashing |
| Aliased arrays at construction | due_evidence and due_timeout one array (src/ph16.py:73); top15 = topr, keep15 = keep16 = nav15 = acts (src/ph33.py:193-194) | harmless because each is reassigned in act; the module does not write them in place |
| Second ring step | two ring steps per tick: velocity from w.rot, then the cue at velocity 0 (src/ph13.py:58-60); the recorded drift doubling (master_plan.md:2318) comes from it | keep both steps; w.rot starts at zero (src/ph13.py:41) |
| Presence and burst update order | cp, c, w1, burst, bb, w2, then present (src/ph33.py:143-151) | copy verbatim |
| Learning loop order | mirror before act, act, move, bump, at_source, mb.step, all rows vectorised, once per world step (src/ph30.py:211-238; master_plan.md:2334-2337) | A7 and A7r run the unchanged harness; mb.step is the module's own |
| Codes per row | a Python loop of choice(K, nact, replace=False) per row (src/ph4.py:34-35) | keep the loop |
| Harness attribute reads | isinstance(a, Agent9) guards the counter fields in ph25.record and ph32.record (src/ph25.py:69-71, src/ph32.py:268) | those fields are left out of L1 and covered by L2 (c, present) |
| Seed scans | new files in notes/module and experiments/module are read by the phN seed scans (src/ph35.py:229-238) | no seed number written; the demos re-run as the check |

## 10. What the owner confirmed

Confirmed by the owner 2026-09-29, verbatim '확정' (gloss: 'confirmed'), every point as recommended, with the review's
amendments 1-4: decision:module-consolidation-open.

1. **One file or two.** CONFIRMED (recommended): one file, src/fly.py (reason U1). Not taken: src/flycore.py and
   src/flybody.py sharing one generator.
2. **What the file holds.** CONFIRMED (recommended): the agent only, both forms. Not taken: also World7, Masked and Lost.
3. **Interface.** CONFIRMED (recommended): Fly(runs, rng, known, nch=2, rng3=None), act, bump, held, chan_valence, and
   the attribute surface of section 4.2, with no perceive/reinforce/readout wrappers (the outlook's names mapped in the
   table). Not taken: wrappers.
4. **Constants.** CONFIRMED (recommended): every constant of section 2.3's core and agent-side tables a module constant,
   G 2.0 and the window by form included; no argument beyond the five (A7r's test-only setting, section 6, adds none).
   Not taken: constants as arguments.
5. **Forms switch.** CONFIRMED (recommended): nch, with the three-channel additions under explicit nch == 3 branches
   (U10), and evidence_due shared. Not taken: the two-channel form through Act16.
6. **Measurement-only attributes.** CONFIRMED (recommended): dropped (section 4.1). Not taken: carried.
7. **Rows.** CONFIRMED (recommended): S0, A1-A7, B1-B3 of section 6, with A7 labelled coverage and A7r added
   [v2, amendment 2]. Not taken: T3b at t0 100 and 200; E2-C of Stage C Run 2.
8. **Fields and tolerance.** CONFIRMED (recommended): L1, L2 and L3, zero tolerance, every row, every step; L2 over every
   attribute, names listed in the output header [v2, amendment 3]. Not taken: any tolerance.
9. **Seeds.** CONFIRMED (recommended): the recorded evaluation seeds reused on purpose, named by constant and report
   line, never written into a new file (section 8, [v2, amendment 4]); the demo seeds (5, 6) for S0. Not taken: new seeds.
10. **G 2.** CONFIRMED (recommended): carried as a module constant; the header flags its adoption status as the owner's,
    unsettled. Not taken: G as an argument.
11. **File names.** CONFIRMED (recommended): src/fly.py; src/module_identity.py; experiments/module/identity.txt,
    experiments/module/identity.json, experiments/module/module_report.md (registered in section 8). Not taken: other
    names.
12. **Readings U7, U8, U10.** CONFIRMED (recommended), as amended [v2, amendment 1]: U7 and U8 in an addendum to the
    outlook (its text unchanged) and in the module header; U10 as the wording correction of section 3 in master_plan,
    by the reviewing session at registration. Not taken: leaving the record's wording unchanged.

## 11. Self-review: the three weakest points

1. **L2 matches state by attribute name.** State held only in a local variable (hp, the gated y, v_max) is not hashed;
   it is covered only through its outputs (H, NAV, TGT, the turn through POS and HEAD). A transcription error whose
   effect is masked in every tested row would pass. The coverage rows A5, A6, B3 were chosen by reading, not by a
   measured branch coverage.
2. **A7 is an identity in a harness Agent17 never ran in.** It exercises the learning path but reproduces no recorded
   number, and the three-channel form's learning path is not tested at all. [v2, amendment 2] A7 is now labelled
   coverage and A7r supplies a recorded reference, at the cost of a test-only setting of the candidate's window.
3. **Three readings stand unmeasured and contradict the record's wording:** U10 (inert by code), U7 (the credit's
   address) and U8 (K). The design avoids depending on them; [v2, amendment 1] the review verified all three against
   the cited lines, and they are recorded as section 3's amendment table says. The seed values are cited by constant and
   report line rather than written out ([v2, amendment 4]).
