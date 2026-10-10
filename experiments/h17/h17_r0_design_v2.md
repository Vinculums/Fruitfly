# H17 R0 passive current-baseline measurement: v2 FINAL

Date: 2026-10-09. Status: **measurement design FINAL; execution not opened**.
Owner instruction: "구체화 진행" (make the proposal concrete).
Decision: decision:h17-r0-design-final. Predecessor: decision:h17-run3-open-design.
This finalizes only the R0 proposal in h17_run3_design_v1.md. That historical
draft remains immutable; its candidate questions are not a FINAL efficacy design.

## 1. Question, authority and fixed reference

Describe failures to find or recover original-source odour on current
Fly(nch=2), supplied values, learning off. Preserve all adopted gain, gating,
filter, presence prior/window, N2, exact-kernel ring, return cast and motor
noise. No controller reads q_obs or a marker; no target intervention, search
state, N1 restoration, learning step, candidate selection, efficacy bar,
power forecast or new adoption is authorized. Historical H17 remains closed
NOT shown. Hold deferral and its measured outcomes remain unchanged.

This session reserves streams and specifies future artifacts, without creating
fresh generators or running trajectories. Implementation and measurement need
a separately recorded execution opening. The former H17 q relaxations remain
lapsed. A later controller reading q needs a new explicit relaxation.

## 2. Fixed sample and matched construction

Four conditions, each R=400 rows and T=600 sensing indices t=0..599.
The four World7 cells (good identity x physical side) contain exactly 100
rows each. Use one measurement pair from config/h17-r0-seeds.json, reset for
each condition and every identity arm. These are matched constructions across
conditions; do not describe the combined 1600 rows as independent samples.

| Condition | Values and start | Primary descriptive numerator / denominator |
|---|---|---|
| C0 | 0/0; position-only outer geometric stress below | Any delivered original-source whiff at t=0..299 / 400 |
| T1 | good +1, other 0; ordinary World7 start | No delivered original-source whiff at t=400..599 / 400 |
| W1 | good +1, other 0; ordinary start; mask good after both raw draws | No delivered original-source whiff at t=400..599 / 400 |
| T3 | good +1, other -1; ordinary start; N2 unchanged | No delivered original-source whiff at t=400..599 / 400 |

W1 also reports delivered non-valued-source whiff rows in that last window
(the complement of its primary), source-specific post-move dwell and reach
separately. Physical proximity to the masked source is never called a whiff.
C0 also reports all-row any-whiff at t=0..599 and reach at t=0..599.
Each condition reports both source whiffs/reach, held and navigation choices,
lost rows, contacts and source dwell without a net valence score.
Dwell_k is each row's mean AT2[:,row,k] over the specified window, then the
mean over all 400 rows; save each row's count. Report full and last-200 windows.
Binary measures use row numerators; step counts never become independent rows.

Construct existing World7(R, world_rng, W) unchanged: retain its inherited
eight main-W construction draws in order (source x, first-source y, legacy
gap, legacy good, legacy starting-source identity, along distance, cross
fraction, heading), even when later overwritten. Its W+10000 permutation
balances four cells; record cell, good, plus_y and both physical source poses.
Source separation is 10, ordinary start is 20 downwind of the pair midline.
Initial world head is inherited, rot=0, t=0, bumped=false. Background p_d=0.

Construct Fly with the main A stream and supplied known array. Preserve its
constructor flee-side draw, then assign the existing cast_draw(A,R), using
A+20000. Preserve all other initial agent/module state: empty hold, since
and silence zero, two counters 140, N=200, prior 60, presence true.
Fixed code streams are src/fly.py CODE_SEEDS, not new roles. No mb.step is called.

C0 uses a separate W+20000 generator AFTER ordinary world and agent
construction and cast assignment. For each cell in order 0,1,2,3, permute its
row indices and assign alternating outward signs +1,-1, exactly 50 each.
Then draw whole-R arrays da uniform[5,14], then dc uniform[26,31].
Choose source k=plus_y for outward +1, otherwise k=1-plus_y.
Override position only:
  pos.x = src[row,k].x + da
  pos.y = src[row,k].y + outward_sign * dc
Save sign, k, da, dc and the overridden start. Heading, rotation, flee/cast,
clocks, circuit, counters, ring and modules are untouched. Verify every cell
has both outer sides 50/50 and effective whiff probability zero for BOTH
plumes at the first sensing pose. This is constructed stress, not a
naturally produced negative-release state. Do not call ph26.construct:
its world-stream draw, heading redraw and historical clock overrides differ.

All worlds and W1 twins have walls=false before the first tick. Use existing
move and bump, not replacement movement code. Strict source reach is Euclidean
distance <3 after movement. Source arrivals do not replace stochastic sensing.

## 3. Streams, draw order and one measurement claim

Reserved base aliases W/A and derived roles W+10000 balance, W+20000 C0
geometry, A+20000 cast are in h17_r0_seed_registration.json. All five actual
values passed a literal digit-boundary scan over every repository file
(excluding only .git and __pycache__) before writing the declaration, and
individual graph searches. Prior hold roles are disjoint. Numeric literals
belong only in config/registration; this prose references aliases.

Actual generator instances per ordinary arm: T1/T3 six (W, A, balance,
cast, code0, code1); C0 seven with geometry; W1 eight with twin W and twin
balance. Identical W/twin and identity-arm streams are intentional matches,
not additional independent seeds. No bootstrap stream or resampling is used.

For each tick, retain ordered checkpoints around the following:
1. W1 copies actual pre-move position, heading and t into its unmasked twin.
2. Actual sense draws source-0 R uniforms then source-1 R uniforms, including
   zero-probability rows; W1 masks good only after both draws and retains raw.
3. Actual World2.wind_on draws R uniforms even at p_wind=1; output all true.
4. W1 twin sense and wind retain the same two-column/wind draws. Compare
   raw sensing and wind exactly. Its pose is reset next tick; do not move twin.
5. Complete unchanged act; save return, all states and observation marker.
6. Existing move, then bump; save post-move pose, rot, contacts and both AT2.
The source sense law is original World2: strict cone 0<along<LMAX and
cross<W0+SLOPE*along, OR distance<3; original p_hit and exponential law.
Masked.plume describes delivered any-whiff. No draw-free wind wrapper.

Runtime target: CPython 3.13.12, NumPy 2.5.3, Windows x64 little endian,
local single process, threads=1 (OMP/OpenBLAS/MKL/NumExpr/BLIS/VECLIB limits
set before NumPy import). Save actual runtime, executable and library
configuration in preflight/claim; any drift stops before fresh generators.

Future artifacts: tools/measure_h17_r0.py, tools/verify_h17_r0.py,
tests/test_h17_r0.py, tests/test_verify_h17_r0.py,
config/h17-r0-execution-pins.json, experiments/h17/r0/ and
experiments/h17/r0_registry/. They do not exist merely by being named here.
After implementation, freeze code/dependency/runtime hashes, concrete array
keysets/dtypes and H0 receipt in execution-pins before opening any fresh stream.
H0 uses named public spent smoke inputs, never the reserved pair; no H0
population is evidence for the R0 question.

Claim the measurement pair exclusively in a durable registry before creating
any fresh generator, after FINAL/config/registration/pins/H0 are valid.
Registry key is the config pair digest; design id is immutable claim metadata,
not part of a key that can bypass a prior pair claim. Claim survives failures;
a changed output directory or design id cannot repeat it.
One claimed invocation runs the pre-fixed identity arms and four conditions,
then aggregates only if all validity gates pass. Identity comparison arms
are not additional efficacy arms. Any exception writes complete=false and
first failing field/index/phase; no automatic restart, extension, replacement
seed, threshold change or aggregation of partial conditions.

## 4. Observation phases, clocks and markers

Mandatory arrays use leading (T,R), with channel/coordinate axis 2 where
applicable. Stored floats retain original float64 (no downcast), bool masks
are bool, indices and q int64 with -1 for absent, source bitsets uint8.
Identity outputs retain their original dtype exactly. State snapshots retain
each attribute's original dtype/shape, including any scalar dtype.

PRE_* is before sensing/act. H_pre is the hold at act entry. H_post, S_post,
EST, NAV, SINCE_post and SIL_post are after COMPLETE act, before move/bump.
SIL_base is after Fly._act but before its N2 wrapper. POS/HEAD/ROT, contacts
and AT2 are after move/bump. Marker pose uses PRE_POS/HEAD/ROT.

q_obs[-1]=0; for each row q_obs[t]=0 if W_delivered[t].any(), else previous+1.
marker_mask=(q_obs>=250)&(H_post==-1); marker_step is first true index or -1.
The first possible continuously odour-free marker is t=249 (250th sensing).
q observes delivered original-source whiffs, never masked raw W1 whiffs.
Longest silence is max(q_obs), including initial and terminal odour-free runs.
No equality with since, silence or presence counter is imposed.

At marker save the pre-move pose/head/rot, act-final estimate, hold/unit state,
cast/flee sides, since, all three silence phases, counters/presence, most
recent any-whiff index and NAV index inclusive of current act (or -1).
Markers are observational and never called actual search engagement.
H_post=-1 means no UNIQUE above-threshold unit, not necessarily empty circuit.

## 5. Windows, denominators and uncertainty

For K=100,200,300 define strict post-marker stored indices m+1..m+K,
for BOTH W_delivered and post-move AT2. Exclude marker-step AT2[m] from
these windows; report it separately as marker-step baseline reach.
A full window needs m>=0 and m+K<=599. Late markers are right-censored,
never K-step failures. Numerator is any relevant event in the full window,
denominator its full-window rows. Report full-window and censored counts.

For every marker row save first strictly post-marker whiff/reach index or
-1, delay, available time 599-m and event/censor status. Simultaneous first
whiffs/reach retain two-bit source identities, never argmax. Report observed
event through the remaining horizon / all marker rows separately, explicitly
as unequal-followup horizon incidence. Report marker and no-marker counts
over 400. C0 unconditional first-300/full-600 measures remain primary.

All binary row estimates save numerator, denominator and Wilson 95% interval:
z=1.959963984540054; centre=(p+z*z/(2*n))/(1+z*z/n);
half=z*sqrt(p*(1-p)/n+z*z/(4*n*n))/(1+z*z/n).
Conditional n<50 is UNREADABLE; n=0 yields null estimate/interval, never zero.
Report fixed-cell counts too; Wilson is descriptive for this balanced sample,
not a forecast or independent-trial efficacy test. No interval for event
counts treating repeated events as rows, or for late markers as full-window
failures. No condition contrast is registered as a causal effect.

## 6. Negative transitions and exact N2 reconstruction

Use supplied known values unchanged. hp=H_pre; h=H_post;
negS=(hp>=0)&(known[hp]<0); negZ=(h>=0)&(known[h]<0),
with safe indexing that cannot map -1 to a real channel.
Negative-to-unheld: negS & h==-1; separate count(S_post>1)==0
from count>1 (multiple active units). Negative identity change:
negS & h>=0 & h!=hp. Negative end is their union, negative_same is negS&h==hp.
Report row incidence and repeated-event counts separately, new identity/value
sign, and concurrent TO/EV strata neither/timeout_only/evidence_only/both.
These flags describe concurrence, not a proved cause.

TO=(SIL_pre>40); EV is the existing strict gated other-minus-held Y margin
>0.2 with committed pre-hold. Reset drive=10 if TO|EV, else 0.
Recompute SIL_base from SIL_pre reset to zero when due, then zero for
post-held delivered whiff or increment by one otherwise. With:
hit=(h>=0)&W_delivered[h]
new=(h>=0)&(h!=hp)
base=TO & ~EV & any(S_post>1) & ~hit
sustain=base & ~negS
newz=new & ~negZ
zreset=newz & ~sustain & (SIL_base>0)
withheld_N1_S=base & negS
withheld_N1_Z=new & negZ
SIL_post=41 if sustain else 0 if newz else SIL_base.
Save all masks and reconstruct from saved inputs/states. base uses any
above-threshold unit, not h>=0; negS uses PRE hold; zreset uses SIL_base.
N2 withholds sustained timeout and negative formation reset; ordinary
negative timeout reset requests remain active. Negative holds may still
end by ordinary evolution/evidence/noise. Do not label every ending an
N1-produced stranding.

## 7. Durable evidence and full identity gates

Before fresh streams, the implementation review fixes the keysets, supported
dtype whitelist and recursive attribute serialization in execution-pins.
The mandatory fieldset below cannot be reduced; additive bookkeeping must
be declared before measurement. No object dtype, pickle, truncation or
quantization. Store NPZ evidence encoded wholly with a-p characters, and an
array manifest with each key, shape, dtype, byte size and data SHA-256 (a-p).
Use a-p alphabet for all hashes; numeric seeds remain only registration/config.

| Group | Mandatory saved fields |
|---|---|
| Construction | src, good, cell, plus_y, known, ordinary and actual start/head/rot; C0 sign/k/da/dc; complete initial agent/up/sel/ring/mb attributes |
| World inputs | PRE_POS/HEAD/ROT, source uniforms and effective probabilities, W_raw/W_delivered, wind uniform/output; W1 twin input/raw/wind/checkpoints |
| Act | H_pre/post, S_pre/post, pool state, upstream pre/post, gated Y, SIL_pre/base/post, SINCE_pre/post, counters C_pre/post, presence pre/post, NAV/TO/EV, N2 masks, reset drive |
| Movement | EST/TGT/TURN, cast_sign/flee_side, POS/HEAD/ROT, bumped/contacts, AT2 both sources |
| Readings | q_obs, marker and anchors, longest silence, first whiff/reach with bitsets, all row loss/dwell/transition/window/event/censor arrays |
| Identity | Complete original output keysets/bytes; construction and act/bump attribute digests, exact inputs/returns, generator creation/draw log and state checkpoints |

Bare Fly must be recorded explicitly: ph25.record's Agent9 isinstance branch
does not provide its actual two-channel counter/presence. Counter/presence
arrays must compare exactly with Fly's attributes. Record intermediate
SIL_base without calling _act twice or adding any draw/state mutation.

Three pre-fixed arms per condition: ordinary Fly, passive-instrumented Fly,
unchanged adopted Agent17. L1: ordinary/passive complete output keysets and
bytes, inputs and returns; lineage fields equal module_identity.L1A
(ph28.BEHK + SUS,Z,AT2,C), plus original output schema saved in pins.
L2: same-class complete recursive Fly/up/sel/ring/mb state at construction,
after act and bump, all generator checkpoints, zero tolerance. Only act/bump
tap callables and externally held recorder state are excluded. Lineage L2
uses exactly module_identity.compare_l2's declared mapping/exclusion rules
and fieldset; cannot invent exclusions after observing a mismatch. Preserve
both classes' full snapshots, including lineage diagnostic n2S/n2Z even if
their explicitly registered identity projection differs. L3: recompute
registered descriptive measures for all arms, plus existing applicable
lineage scores from the stored required arrays; no rerun for score calculation.
Any field unable to match needs correction/review before consuming the pair,
not a retrospective identity exemption.

All gates must pass before aggregate: full 4x400x600 sample/keyset/dtypes/
hashes, ordinary/passive L1/L2/L3, Fly/Agent17 lineage L1/L2/L3, no extra
draws and every generator checkpoint, balance/C0 independence/zero initial
probabilities/untouched state, original W1 raw/twin draws and mask, wind
draws, walls off/no contacts, fixed known/no learning, phase contracts and
all exact formulas. Identity gates are evidence validity, not performance.

## 8. Independent verifier, report and next decision

Future verifier reads only saved arrays/manifests, constants and hashes;
it never runs the runner, Fly, ph harness or RNG. It recomputes every
registered metric, all denominators/censoring and N2/state masks, reports
first failure field/index/phase and checks complete source/config/runtime
closure. Save FINAL/config/registration/implementation/verifier hashes,
fixed schema, every file/array digest, all gates, raw numerators/denominators
and complete status. Root independently recomputes the readings before
registering any result (P3). Tests exercise meaningful recording passivity,
window boundaries, simultaneous-source identities, censoring, N2 negative/
multi-unit branches, durable claim and malformed evidence rejection.

R0 stops after one verified measurement report. There is no efficacy PASS,
candidate/adoption or automatic follow-up. A missing/unreadable population
is retained, not manufactured by N1, extra seeds or a longer horizon.
Any future performance design first names its current failure population
and walked loop anchor (P2); old Agent10/13 rates/power are not forecasts.
A later known-answer relative clause at its ceiling/floor is SATURATED,
not PASS/FAIL (P1).

Next reviewable action is a separate R0 execution opening: implement the
named runner/verifier, pin and review them, pass spent-input H0, then claim
and measure once under this FINAL. Candidate execution remains a later
decision after reading the current baseline.

## 9. Source closure and reservation evidence

Canonical current Fly source: dd1fc3d20ef84ad9d.
Predecessor DRAFT: dac20b7f7a9bbc737.
Historical Run2 design: d73c77ebd99d50d86; diagnosis: dd1ba5b405811ef4a.
Construction anchors: ph11 World2; ph13 World4; ph14 World5; ph16 World7/
cast_draw; ph22 Masked; ph24 tick order; module_identity lineage gates.
Source/evidence snapshot below is immutable for this FINAL. Future code
closure must include every transitive Python dependency, configs and runtime,
validated before/after measurement; digest drift stops.

Reservation config SHA (a-p): iejnjbleicghhinmedadflphnnpibopmflpapajejgedijjeigaooblhdajnhmed.
Reservation receipt SHA (a-p): pleafleiefdijfpbghcliihcofebdemeeeicldggpgbmnokandimckjgbkajibji.
No new R2 exception: source/downstream pins and exact exception-pair manifest
stay fixed. Historical ph31_eval exclusion remains separately registered.

| Source / saved evidence | SHA-256 (a-p) |
|---|---|
| src/fly.py | dldgalcjabghimlmdbdmmkiihedfcpmhagniaolfepgnokfigimkbbpebjnbopme |
| src/ph21.py | dkbnhjnjkancdfpblophoedfomfjemppeaeibiaochlcinmnijcfjimfiebdmpmb |
| src/ph23.py | kobiaejcoomojdhdjnkenblfnidkbdkclecmfojfceefkjcklhfpjfmgplcolfko |
| src/ph24.py | pdeepbhiocadiaifipenheaaopghaccdpjakkcjchldphdaehhckobnieilnblop |
| src/ph26.py | bmjlgpflgodpadebogamhahmnfhhnheicjcomnlhcaagcomknkddddgbabobghmp |
| src/ph27.py | nbcpkgfbheojgiimjjmnkilaamhehmbpgjnfeaoanicoihnlgkfcioinfbimbedk |
| src/ph30.py | jiiccideaednofpdbgbfohdmnekideeeknmopcpbnfofgehidfgnhamkjafafjln |
| src/ph33.py | pckcjhcckdjimiblhphdabencjmhjjkaimcijomkbmmhdggkmngfofabfeohcala |
| src/ph35.py | oekdmonkcfgciohacgkgeigbknfbpiejhepbockhcahjechgnphagnaagkfclblb |
| src/ph9.py | hgjjleogplehkbloofphoeojjbkiikkmipkfkpdkjeacjhplneoeebeebpenjhag |
| src/ph11.py | oiapealnhbakmkedcfcpaedcjiegppkcjjedcfbnbjohbiefaojkhppejojehkcd |
| src/ph12.py | obadfoajimdlicijjiljjlafpijlhodlilmkbfpdacfddokchpmmebdjlkndkbmh |
| src/ph12b.py | omglbijgpgaopcocfanajcoapjpjpebafmagldipgjjinojahaamkdhbcbdoapkk |
| src/ph16.py | ddnfpnlcfjfjplhpjmloegfmkcfkijhdhhgldjpbofbhangefmlfdlminjagkcmc |
| src/module_identity.py | beffikmapflgbkekhbjhcmmnbkegbcdifocabgmlgkhfmoodemcpkmfhlbadnglf |
| experiments/module/identity.json | diogkenmdgfnejioblllfllplmiakpoegjjgbnnjbkompnpmelhdbilmpddfjlci |
| experiments/h17/ph26_bench.txt | omjnphickkecjejcegciejmjfhhoifdlknojgoopnbijbhgcgoojkaiojgedppgn |
| experiments/h17/ph27_bench.txt | hbhgchikmlppchjfgfoockhlmikiimifhndmjlhiahdccapoikienfpoaimgjlhb |
| experiments/h17/ph26b_diag.txt | baecjpflcmgjpbdnjdffhjckchaakblbokinihnkdblhfnjmefbglgiagkonnpbj |
| experiments/h17/ph27b_diag.txt | hkcoooofdomlmgnnahhledgpjmnfccamalamlilfjbniipiiihcfjnnefppneebo |
| experiments/h17/h17_post_bench_diagnosis.md | fcbcgolodkgcodofoabiakeiklcdmminaimfghibnfjalaknnokjhlbkneemonhf |
| experiments/h17/h17_run2_post_bench_diagnosis.md | mlicenmegdfhdfaenkdkbbjofokamdpohencodcelcghhkkajgcglenebplhfooa |
| experiments/h17/h17_run2_design_v2.md | ncdhemfodajbbiemggjkpfpioajkfgbljnhkmpgiaoglbaplmcbbhfapnanhnfoj |
| experiments/h18/h18_stage_b_design_v2.md | glaakfagpfglmhfmofhgmodhkcddeidfigakddkkmjggkedhgghkchldnlmkedab |
| experiments/hold/hold_d0_report.md | ikcbmaenbhpkndpkdhpkpnbfpjdgfpehephlfnknonikgfgpdjkdhelbckmpbnno |
| experiments/hold/hold_stage2_report.md | lfmmdhodaimcjkhahodijcnlimbolkhbnmbgmlmkklhbkpdojmappapolpgkomoa |
| experiments/hold/hold_e1/hold_e1_report.md | cfbjgjcngldlidnjkkcdonalifejgoonmiihhfbmfiimhoklhnheaohcphnpplbd |
| src/ph13.py | cnhfpkoioimdbobmgnnpgfhhhicpkpnodajjpbapoipfapodicpfdnajojopbpcn |
| src/ph14.py | mglhefmgapjjjcjdekammlmffieopdfekadpfdpaildhkbcfckgjepoldfaloana |
| src/ph22.py | adklimehaglbjffhkpfngeonnidpibckllkjblgbiedjgbildfidhkejnneemkbm |
