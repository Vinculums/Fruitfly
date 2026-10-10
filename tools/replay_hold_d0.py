#!/usr/bin/env python3
"""D0 passive recount, six existing primary strata, no new world or seed.

All strata must pass stage-one passivity gates before summaries are written.
--smoke uses module_identity smoke aliases and sizes, for harness validation.
"""
import argparse
import json
import os
from pathlib import Path
import platform
import sys

import replay_hold_stage1 as stage1

ROOT = stage1.ROOT
BASE_MAKE_TAP = stage1.make_tap
DESIGN = 'notes/hold/2026-10-09-hold-branch-exposure-design-v2.md'


def make_d0_tap(m, instrumented, added):
    from hold_d0_metrics import plume_probability
    tap = BASE_MAKE_TAP(m, instrumented, added)
    tap.d0_samples = []
    tap.d0_initial = None
    attach, rec = tap.attach, tap.rec

    def attach_d0(agent):
        attach(agent)
        if not instrumented:
            return
        act = agent.act
        def observe(w, whiffs, wind_on):
            if tap.d0_initial is None:
                # The harness may install its registered initial hold AFTER
                # construction; capture immediately before the first act.
                tap.d0_initial = dict(h=agent.held().copy(), c=agent.c.copy())
            tap.current_whiffs = whiffs.copy()
            if agent.nch == 3:
                # Exactly the sensing positions, before World.move; good maps
                # source identities to V/B and differs between balanced rows.
                tap.current_probabilities = dict(B=plume_probability(w, 1-w.good),
                                                 N=plume_probability(w, w.good))
            result = act(w, whiffs, wind_on)
            return result
        agent.act = observe

    def rec_d0(agent, kind):
        rec(agent, kind)
        if not instrumented or kind != 'act':
            return
        p = agent.hold_projection
        sample = dict(h=agent.held().copy(), q=agent.hr.copy(), c=agent.c.copy(),
                      whiffs=tap.current_whiffs.copy(), timeout=agent.due_timeout.copy(),
                      evidence=agent.due_evidence.copy(),
                      top_H=p['H']['top'].copy(), top_R=p['R']['top'].copy(),
                      eligible_H=p['H']['eligible'].copy(), eligible_R=p['R']['eligible'].copy(),
                      nav_difference=p['H']['nav'] != p['R']['nav'],
                      command_difference=p['H']['clipped_turn'] != p['R']['clipped_turn'])
        if agent.nch == 3:
            sample.update(burst=agent.burst.copy(), bb=agent.bb.copy(),
                          probabilities={k: v.copy() for k, v in tap.current_probabilities.items()},
                          neutral=1-tap.agent_world_good)
        tap.d0_samples.append(sample)
    # Source mapping is captured through the same observed act, no agent field.
    original_attach = attach_d0
    def attach_world(agent):
        original_attach(agent)
        if instrumented:
            act = agent.act
            def world_mapping(w, whiffs, wind_on):
                if agent.nch == 3: tap.agent_world_good = w.good.copy()
                return act(w, whiffs, wind_on)
            agent.act = world_mapping
    tap.attach, tap.rec = attach_world, rec_d0
    return tap


def run_pair(m, passive, added, rid, smoke=False):
    original = stage1.make_tap
    seed_fn, size_fn = m.seeds_of, m.size_of
    captured = []
    def factory(*args):
        tap = make_d0_tap(*args); captured.append(tap); return tap
    try:
        stage1.make_tap = factory
        if smoke:
            m.seeds_of = lambda kind, ignored: seed_fn(kind, True)
            m.size_of = lambda kind, ignored: size_fn(kind, True)
        gate, evidence, condition = stage1.run_pair(m, passive, added, rid)
    finally:
        stage1.make_tap = original
        m.seeds_of, m.size_of = seed_fn, size_fn
    tap = captured[1]
    evidence.update(samples=tap.d0_samples, initial=tap.d0_initial)
    condition['seeds'] = 'module_identity.seeds_of(kind, smoke=True)' if smoke else condition['seeds']
    condition['sample'] = 'smoke harness validation' if smoke else 'registered D0 diagnosis'
    return gate, evidence, condition


def summarize(np, evidence, condition):
    from hold_d0_metrics import hold_records
    result = stage1.summarize(np, evidence, condition)
    samples = evidence['samples']
    arrays = {key: np.stack([s[key] for s in samples]) for key in samples[0] if key != 'probabilities'}
    steps, rows = arrays['h'].shape
    def metric(mask):
        return dict(row_steps=int(mask.sum()), denominator_row_steps=rows*steps,
                    rows=int(mask.any(0).sum()), per_row=mask.sum(0).tolist())
    result['set_sizes'] = {key: {str(n): metric(arrays[key].sum(2) == n) for n in range(arrays[key].shape[2]+1)}
                           for key in ('top_H', 'top_R', 'eligible_H', 'eligible_R')}
    records = hold_records(np, samples, evidence['initial'])
    window = 200 if arrays['c'].shape[2] == 2 else 300
    result['holds'] = dict(records=records, denominator_holds=len(records),
                         maximum_held_counter=max((r['maximum_held_counter'] for r in records), default=None),
                         window=window, at_or_above_window=sum(r['maximum_held_counter'] >= window for r in records),
                         evidence_survival_at_or_above_window=sum(
                             r['maximum_counter_surviving_evidence_reset'] is not None and
                             r['maximum_counter_surviving_evidence_reset'] >= window for r in records),
                         interpretation='reset requests and actual identity exit recorded separately; inherited and censored holds explicit')
    natural = [r for r in records if not r['inherited_at_start']]
    inherited = [r for r in records if r['inherited_at_start']]
    surviving_evidence = [r['maximum_counter_surviving_evidence_reset'] for r in records
                          if r['maximum_counter_surviving_evidence_reset'] is not None]
    result['section3_bound_checks'] = dict(
        natural_formation_holds=len(natural), inherited_construction_holds=len(inherited),
        natural_maximum_formation_counter=max((r['formation_counter'] for r in natural), default=None),
        inherited_maximum_initial_counter=max((r['formation_counter'] for r in inherited), default=None),
        natural_maximum_held_counter=max((r['maximum_held_counter'] for r in natural), default=None),
        inherited_maximum_held_counter=max((r['maximum_held_counter'] for r in inherited), default=None),
        maximum_counter_surviving_evidence_reset=max(surviving_evidence, default=None), window=window,
        held_counter_below_window='UNRESOLVED' if not records else 'PASS' if all(r['maximum_held_counter'] < window for r in records) else 'FAIL',
        evidence_survival_below_window='PASS' if all(c < window for c in surviving_evidence) else 'FAIL',
        evidence_survival_observed=bool(surviving_evidence),
        interpretation='bounds checked on these recorded states only; initial construction is not natural formation')
    if arrays['c'].shape[2] == 3:
        row_index = np.arange(rows)[None, :]
        t_index = np.arange(steps)[:, None]
        neutral = arrays['neutral']
        bburst = arrays['burst'][t_index, row_index, neutral]
        dburst = arrays['burst'][:, :, 2]
        tied = (arrays['bb'][t_index, row_index, neutral] == arrays['bb'][:, :, 2]) & (arrays['bb'][:, :, 2] > -1.0e9)
        bwhiff = arrays['whiffs'][t_index, row_index, neutral]
        dwhiff = arrays['whiffs'][:, :, 2]
        single = tied & (bwhiff != dwhiff) & ~(bburst | dburst)
        for projection in ('H', 'R'):
            eligible = arrays['eligible_'+projection]
            result['set_sizes']['two_member_ranked_'+projection] = metric(eligible.sum(2) == 2)
        # T1/T2 jointly across H and R; all-row raw tie counts are also retained.
        top_bd = np.zeros_like(arrays['top_H']); top_bd[t_index, row_index, neutral] = True; top_bd[:, :, 2] = True
        qualifying = single & (arrays['top_H'] == top_bd).all(2) & (arrays['top_R'] == top_bd).all(2)
        # In a two-member tied set, T5 is precisely the nav split.
        split = qualifying & arrays['nav_difference']
        result['burst_ties'] = dict(simultaneous_bursts=metric(bburst & dburst),
                                  latest_burst_tie=metric(tied), tied_single_nonburst=metric(single),
                                  T1_T4=metric(qualifying), T1_T5=metric(split),
                                  identity_split_denominator=int(qualifying.sum()),
                                  f_id=None if not qualifying.any() else float(split.sum()/qualifying.sum()),
                                  f_id_status='undefined: no qualifying natural tied-single row-step' if not qualifying.any() else 'measured on natural qualifying tie states')
    return result


def source_hashes():
    files = ['src/fly.py', 'src/module_identity.py', 'src/hold_stage1_instrument.py',
             'src/hold_d0_metrics.py', 'tools/replay_hold_stage1.py', 'tools/replay_hold_d0.py',
             'src/ph11.py', 'src/ph9.py', 'src/ph16.py', 'src/ph22.py', 'src/ph33.py', 'src/ph35.py', DESIGN]
    return {name: stage1.digest((ROOT/name).read_bytes()) for name in files}


def write_gated_report(path, report, m, verifier):
    raw = (json.dumps(report, indent=2)+'\n').encode()
    if any(verifier.count_number(raw, number) for checker in (m.ph33, m.ph35) for number in checker.seed_numbers()):
        raise RuntimeError('report P5 collision; no report written; representation review required')
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as target: target.write(raw)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--smoke', action='store_true')
    args = parser.parse_args()
    if args.output.exists(): parser.error('output must be a new file')
    m, passive, added, verifier = stage1.load_runtime()
    gates, saved = {}, {}
    for rid in stage1.PRIMARY:
        print('Checking D0 passivity: '+rid, flush=True)
        gate, evidence, condition = run_pair(m, passive, added, rid, args.smoke)
        gates[rid] = gate
        if not gate['passed']:
            # Minimal error receipt; never aggregate or release failed-run data.
            receipt = dict(status='STOP: D0 passivity gate failed', stratum=rid, gate=gate,
                           provenance=dict(source_sha256_ap=source_hashes()))
            write_gated_report(args.output, receipt, m, verifier)
            print('D0 gate failed: '+rid+'; minimal error receipt written, no aggregates.')
            return 1
        saved[rid] = evidence, condition
    # All statistics/proxy arithmetic occur ONLY after all six gates pass.
    from hold_d0_metrics import exact_proxy
    probabilities = saved['B2'][0]['samples']
    pb = m.np.stack([s['probabilities']['B'] for s in probabilities])
    pn = m.np.stack([s['probabilities']['N'] for s in probabilities])
    report = dict(status='all six passivity gates passed; passive D0 diagnosis',
                  sample='smoke' if args.smoke else 'full', gates=gates,
                  strata={rid: summarize(m.np, *saved[rid]) for rid in stage1.PRIMARY},
                  proxies={candidate: exact_proxy(pb, pd) for candidate, pd in (('W1Dp', pb), ('W1N', pn))},
                  B2_probabilities=dict(B_per_step=pb.tolist(), N_per_step=pn.tolist(),
                                        in_B_plume_fraction=float((pb > 0).mean()),
                                        probability_mean=float(pb.mean()), sensing_position='before move'),
                  burst_formula_audit='draft agrees with actual w2: current whiff plus at least two whiffs in preceding nine ticks',
                  provenance=dict(source_sha256_ap=source_hashes(), python=sys.version.split()[0], numpy=m.np.__version__,
                                  platform=platform.platform(), design=DESIGN,
                                  thread_and_process_pins={key: os.environ[key] for key in
                                      ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
                                       'PH30_PROCS', 'PH32_PROCS', 'PH33_PROCS')}),
                  interpretation='frozen W1D position proxies; no new condition, no benefit verdict, no calibrated P(X3)')
    checks = [s['section3_bound_checks'] for s in report['strata'].values()]
    if any(c['held_counter_below_window'] == 'FAIL' or c['evidence_survival_below_window'] == 'FAIL' for c in checks):
        report['next_step_reading'] = 'FAIL: section3 bound violated; no E1; constructed-witness review required'
    elif any(c['held_counter_below_window'] == 'UNRESOLVED' for c in checks):
        report['next_step_reading'] = 'UNRESOLVED: insufficient hold observations; no E1'
    elif all(p['probability_at_least_40_rows_upper_bound'] < .5 for p in report['proxies'].values()):
        report['next_step_reading'] = 'proxy supports deferral: both conservative probability bounds below 0.5; no calibrated free-running prediction; no E1'
    else:
        report['next_step_reading'] = 'UNRESOLVED: conservative proxy bound does not establish failure for both candidates; no E1'
    write_gated_report(args.output, report, m, verifier)
    print('D0 passivity verified; report written. No benefit verdict.')
    return 0


if __name__ == '__main__':
    try: sys.exit(main())
    except (OSError, RuntimeError, ValueError) as exc:
        print('D0 stopped: '+str(exc), file=sys.stderr); sys.exit(1)
