# H12 Package D diagnosis

Measurement only; no adoption or new behavioural PASS label.

The immutable original bench reproduced bytewise. Each instrumented donor reproduced all original fields bitwise.

## Original P4 counts

- H12: V 33, N 251, tie 116 / 400
- gate only: V 10, N 276, tie 114 / 400
- H11 full: V 10, N 277, tie 113 / 400
- ceiling: V 42, N 231, tie 127 / 400
- floor: V 5, N 293, tie 102 / 400
- sham: V 13, N 366, tie 21 / 400
- ceiling (H12 module): V 42, N 231, tie 127 / 400
- supplied H12 trajectory: V 33, N 251, tie 116 / 400
- supplied gate-only trajectory: V 10, N 276, tie 114 / 400

## P4 opportunity

The ordered partition assigns a row to its first failure stage: no V whiff, V whiff without V-supported upwind navigation, V navigation without contact, or contact without V dwell majority. Contact or majority can occur despite an earlier failure category; the unconditional counts report those overlaps.

- H12: {'no_V_whiff': 332, 'V_whiff_no_V_nav': 11, 'V_nav_no_V_contact': 4, 'V_contact_no_majority': 20, 'V_majority': 33}; filter eligible 68; unconditional V majority 33; zero-contact ties 115; positive ties 1; flee rows 0; both-channel nav rows 0
- gate only: {'no_V_whiff': 327, 'V_whiff_no_V_nav': 58, 'V_nav_no_V_contact': 3, 'V_contact_no_majority': 2, 'V_majority': 10}; filter eligible 54; unconditional V majority 10; zero-contact ties 114; positive ties 0; flee rows 0; both-channel nav rows 0
- H11 full: {'no_V_whiff': 327, 'V_whiff_no_V_nav': 58, 'V_nav_no_V_contact': 3, 'V_contact_no_majority': 2, 'V_majority': 10}; filter eligible 54; unconditional V majority 10; zero-contact ties 113; positive ties 0; flee rows 0; both-channel nav rows 0
- ceiling: {'no_V_whiff': 335, 'V_whiff_no_V_nav': 0, 'V_nav_no_V_contact': 2, 'V_contact_no_majority': 21, 'V_majority': 42}; filter eligible 65; unconditional V majority 42; zero-contact ties 126; positive ties 1; flee rows 0; both-channel nav rows 0
- floor: {'no_V_whiff': 318, 'V_whiff_no_V_nav': 69, 'V_nav_no_V_contact': 7, 'V_contact_no_majority': 1, 'V_majority': 5}; filter eligible 55; unconditional V majority 5; zero-contact ties 102; positive ties 0; flee rows 0; both-channel nav rows 0
- sham: {'no_V_whiff': 274, 'V_whiff_no_V_nav': 103, 'V_nav_no_V_contact': 7, 'V_contact_no_majority': 4, 'V_majority': 12}; filter eligible 87; unconditional V majority 13; zero-contact ties 20; positive ties 1; flee rows 0; both-channel nav rows 0
- ceiling (H12 module): {'no_V_whiff': 335, 'V_whiff_no_V_nav': 0, 'V_nav_no_V_contact': 2, 'V_contact_no_majority': 21, 'V_majority': 42}; filter eligible 65; unconditional V majority 42; zero-contact ties 126; positive ties 1; flee rows 0; both-channel nav rows 0
- supplied H12 trajectory: {'no_V_whiff': 332, 'V_whiff_no_V_nav': 11, 'V_nav_no_V_contact': 4, 'V_contact_no_majority': 20, 'V_majority': 33}; filter eligible 68; unconditional V majority 33; zero-contact ties 115; positive ties 1; flee rows 0; both-channel nav rows 0
- supplied gate-only trajectory: {'no_V_whiff': 327, 'V_whiff_no_V_nav': 58, 'V_nav_no_V_contact': 3, 'V_contact_no_majority': 2, 'V_majority': 10}; filter eligible 54; unconditional V majority 10; zero-contact ties 114; positive ties 0; flee rows 0; both-channel nav rows 0

## Same-input donor replays

- H12: own module reproduced bitwise; A0_vs_A1 first >1e-12 at step 606, max |difference| 0.203608, sign-inverted row-steps 7198; A1_vs_P first >1e-12 at step 601, max |difference| 0.317448, sign-inverted row-steps 0; A0_vs_P first >1e-12 at step 601, max |difference| 0.328664, sign-inverted row-steps 7198
- gate only: own module reproduced bitwise; A0_vs_A1 first >1e-12 at step 606, max |difference| 0.203608, sign-inverted row-steps 7194; A1_vs_P first >1e-12 at step 601, max |difference| 0.317448, sign-inverted row-steps 0; A0_vs_P first >1e-12 at step 601, max |difference| 0.328664, sign-inverted row-steps 7194
- H11 full: own module reproduced bitwise; A0_vs_A1 first >1e-12 at step 606, max |difference| 0.203608, sign-inverted row-steps 7198; A1_vs_P first >1e-12 at step 601, max |difference| 0.317448, sign-inverted row-steps 0; A0_vs_P first >1e-12 at step 601, max |difference| 0.328664, sign-inverted row-steps 7198

## False A0/A1 identity in the closed loop

H11 full and gate-only depart on 350/400 rows; maximum V value gap 0.203608. The donor replays show same-input module differences separately from changed exposure histories.


## Pure retention from every A1 P2 checkpoint

- D=0: median signed value 0.374417; positive 391; negative 9; above competitor 52; crossed upward from below 0
- D=1200: median signed value 0.507910; positive 391; negative 9; above competitor 208; crossed upward from below 156
- D=5000: median signed value 0.767818; positive 391; negative 9; above competitor 384; crossed upward from below 332

## Input contract for proposed Package E

Learning code in this integrated harness comes from V source contact after movement. Masking whiffs does not remove that code. Pure retention uses zero code and zero external reinforcement while the module clock continues. Package E remains unregistered and unrun.

See summary.json and events.npz for row-level data, replay contrasts, and source provenance.
