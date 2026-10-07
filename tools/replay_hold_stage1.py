#!/usr/bin/env python3
"""Owner-local passive replay, not executed as part of code delivery.

Usage: python tools/replay_hold_stage1.py --output /path/to/new-report.json
Runs the fixed strata sequentially. All strata must pass L1/L2/L3 before any
projection counts are released. No free-running R arm, learning, or seed override.
"""
import argparse
from contextlib import contextmanager
import hashlib
import importlib
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PINS = {
    'fly': 'dldgalcjabghimlmdbdmmkiihedfcpmhagniaolfepgnokfigimkbbpebjnbopme',
    'module_identity': 'beffikmapflgbkekhbjhcmmnbkegbcdifocabgmlgkhfmoodemcpkmfhlbadnglf',
}
PRIMARY = ('A1', 'A2', 'A3', 'A4', 'B1', 'B2')
COVERAGE = ('A5', 'A6', 'B3')
ORDER = ('identity', 'val', 'hit', 'vh', 'presence_override', 'presence', 'top',
         'eligible', 'keep', 'nav', 'since', 'silence', 'flee', 'tgt',
         'clipped_turn', 'post_silence')


def digest(data):
    return hashlib.sha256(data).hexdigest().translate(
        str.maketrans('0123456789abcdef', 'abcdefghijklmnop'))


def load_runtime():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('assertions must remain enabled')
    for name, pin in PINS.items():
        if digest((ROOT / 'src' / (name + '.py')).read_bytes()) != pin:
            raise RuntimeError('reference source pin mismatch: ' + name)
    # Before numpy imports; sequential execution, as in the identity report.
    for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
                'PH30_PROCS', 'PH33_PROCS', 'PH32_PROCS'):
        os.environ[key] = '1'
    sys.path.insert(0, str(ROOT / 'tools'))
    import verify_seed_scan_r2 as verifier
    verifier.verify_sources(ROOT)
    verifier.load_manifest(ROOT)
    sys.path.insert(0, str(ROOT / 'src'))
    # Same import order as module_identity, with its import-time hook mutations
    # immediately restored. Its main/one/row_harness functions are never called.
    import ph35, ph33, ph31, ph24, ph30
    old = (ph24.make, ph33.build, ph30.build)
    arms = dict(ph33.ARMS)
    try:
        identity = importlib.import_module('module_identity')
    finally:
        ph24.make, ph33.build, ph30.build = old
        ph33.ARMS.clear()
        ph33.ARMS.update(arms)
    from hold_stage1_instrument import PassiveFly, MEASUREMENT_ATTRIBUTES
    return identity, PassiveFly, MEASUREMENT_ATTRIBUTES, verifier


@contextmanager
def inject(identity, agent_type, tap):
    """Exact module_identity hook signatures, scoped and restored on any exit."""
    m = identity
    old = (m.ph24.make, m.ph33.build, m.ph30.build)
    arms = dict(m.ph33.ARMS)

    def attach(agent):
        tap.attach(agent)
        return agent

    def make(cls, runs, rng, G, known, gate=True, filt=True, release=True):
        if cls is not m.CAND2:
            return old[0](cls, runs, rng, G, known, gate, filt, release)
        if G != m.fly.G_STAR or not (gate and filt and release):
            raise RuntimeError('unsupported two-channel hook configuration')
        return attach(agent_type(runs, rng, known, nch=2))

    def build33(kind, runs, seed_a, g, kv):
        if kind != 'CAND3':
            return old[1](kind, runs, seed_a, g, kv)
        rng = m.np.random.default_rng(seed_a)
        rng3 = m.np.random.default_rng(seed_a + m.ph32.A3_OFF)
        return attach(agent_type(runs, rng, kv, nch=3, rng3=rng3))

    def build30(kind, runs, rng, w, vals):
        # Exact Stage C injection contract from module_identity. The fixed row
        # list below never selects learning rows or the historical A7r override.
        if kind != 'A14N2':
            raise RuntimeError('unsupported Stage C hook kind')
        kv = m.ph30.kv_of(vals, w.good)
        return attach(agent_type(runs, rng, kv, nch=2))

    m.ph24.make, m.ph33.build, m.ph30.build = make, build33, build30
    m.ph33.ARMS['module D on'] = ('CAND3', 3, True)
    try:
        yield
    finally:
        m.ph24.make, m.ph33.build, m.ph30.build = old
        m.ph33.ARMS.clear()
        m.ph33.ARMS.update(arms)


def make_tap(m, instrumented, added):
    class Tap(m.Tap):
        def __init__(self):
            super().__init__()
            self.masks = []
            self.release = []
            self.projection_ok = True
            self.first_projection_error = None
            self.input_digests = []
            self.return_digests = []

        def attach(self, agent):
            # Retain module_identity's act/bump event timing. Input and returned
            # command/hold hashes add explicit identical-input/return checks.
            act = agent.act
            def observed(w, whiffs, wind_on):
                self.input_digests.append(hashlib.sha256(b''.join(
                    m.blob(x) for x in (whiffs, wind_on, w.head, w.rot))).digest())
                result = act(w, whiffs, wind_on)
                self.return_digests.append(hashlib.sha256(b''.join(m.blob(x) for x in result)).digest())
                return result
            agent.act = observed
            super().attach(agent)

        def rec(self, agent, kind):
            state = m.walk(agent)
            extras = set(vars(agent)) & set(added)
            if (instrumented and extras != set(added)) or (not instrumented and extras):
                raise RuntimeError('unexpected instrumentation attributes')
            for key in added:
                state.pop(key, None)
            self.events.append((kind, {k: hashlib.sha256(m.blob(v)).digest() for k, v in state.items()}))
            if not instrumented or kind != 'act':
                return
            p = agent.hold_projection
            h, r = p['H'], p['R']
            actual = dict(identity=agent.held(), presence=agent.present, nav=agent.nav_hit,
                          since=agent.since, post_silence=agent.silence, tgt=agent.tgt,
                          clipped_turn=m.np.clip(m.fly.GAIN * m.fly.angdiff(agent.tgt, agent.est),
                                                -m.fly.MAXTURN, m.fly.MAXTURN))
            for key, value in actual.items():
                if not m.beq(h[key], value):
                    self.projection_ok = False
                    if self.first_projection_error is None:
                        self.first_projection_error = dict(step=len(self.masks), expression=key)
            masks = {}
            for key in ORDER:
                difference = h[key] != r[key]
                masks[key] = difference.reshape(agent.R, -1).any(1).copy()
            # Store boolean observations only, without reading aggregate counts.
            self.masks.append(masks)
            self.release.append(p['release'].copy())
    return Tap()


def run_pair(m, passive, added, rid):
    kind, world, vals = m.ROWS[rid]
    seeds = m.seeds_of(kind, False)
    runs, steps = m.size_of(kind, False)
    outputs, taps = [], []
    for agent_type, instrumented in ((m.fly.Fly, False), (passive, True)):
        tap = make_tap(m, instrumented, added)
        with inject(m, agent_type, tap):
            if kind == 'h29':
                out = m.ph35.run(world, m.CAND2, vals, seeds, runs=runs, steps=steps)
            else:
                out = m.ph33.run(world, 'module D on', vals, seeds, runs=runs, steps=steps)
        outputs.append(out)
        taps.append(tap)
    ref, cand = outputs
    tr, tc = taps
    fields = m.L1A if kind == 'h29' else m.L1B
    l1 = {key: m.beq(ref[key], cand[key]) for key in fields}
    l2, events, hashes, first, names = m.compare_l2(tr, tc)
    # Unlike the historical cross-class comparison, no base attribute may be
    # missing or silently omitted here. Only the two declared additions differ.
    l2 = l2 and not names['ref_only'] and not names['cand_only']
    l2 = l2 and events == steps * 2
    sr, sc = (m.l3_scores(kind, world, out, steps) for out in outputs)
    l3 = {key: m.beq(sr[key], sc[key]) for key in sr}
    construction = all(bool(out[key]) for out in outputs for key in ('draws_equal', 'rng_equal'))
    coupling = tr.input_digests == tc.input_digests and tr.return_digests == tc.return_digests
    complete = len(tc.masks) == steps and all(len(x['identity']) == runs for x in tc.masks)
    ok = all(l1.values()) and l2 and all(l3.values()) and construction and coupling and complete and tc.projection_ok
    gate = dict(passed=bool(ok), L1=l1, L2=dict(equal=bool(l2), events=events, hashes=hashes,
                first=first, names=names, excluded_measurement_attributes=sorted(added)), L3=l3,
                construction=construction, inputs_and_returns_equal=coupling,
                projection_matches_actual=tc.projection_ok, first_projection_error=tc.first_projection_error,
                complete_sample=complete)
    # HR is the newly recorded instantaneous read identity, not an L1 behavior
    # field. Confirm its record wiring separately when the harness records it.
    if 'HR' in cand:
        # Full hr values are carried by ph32.record, masks retain only inequality.
        recorded = cand['HR'] != cand['H']
        gate['hr_record_matches'] = m.np.array_equal(recorded, m.np.stack([x['identity'] for x in tc.masks]))
        gate['passed'] = gate['passed'] and bool(gate['hr_record_matches'])
    evidence = dict(masks=tc.masks, release=m.np.stack(tc.release), boundary=cand['C'].astype(bool))
    return gate, evidence, dict(group='primary' if rid in PRIMARY else 'coverage', world=world,
                               values=vals, rows=runs, steps=steps, seeds=m.SEED_NAME[kind])


def summarize(np, evidence, condition):
    rows, steps = condition['rows'], condition['steps']
    arrays = {key: np.stack([x[key] for x in evidence['masks']]) for key in ORDER}
    def metric(mask):
        per_row = mask.sum(0)
        first = np.where(mask.any(0), mask.argmax(0), -1)
        return dict(events=int(mask.sum()), denominator_row_steps=rows * steps,
                    rows_exposed=int(mask.any(0).sum()), denominator_rows=rows,
                    events_per_row=per_row.tolist(), first_step_per_row=first.tolist(),
                    repeated_events_per_row=np.maximum(per_row - 1, 0).tolist())
    # Exposure is a different local clipped command; report all internal
    # differences separately so identity mismatch is never called action benefit.
    command = arrays['clipped_turn']
    any_difference = np.logical_or.reduce(list(arrays.values()))
    first = np.full((steps, rows), -1, dtype=int)
    first_downstream = np.full_like(first, -1)
    for i, key in enumerate(ORDER):
        first[(first < 0) & arrays[key]] = i
        if key != 'identity':
            first_downstream[(first_downstream < 0) & arrays[key]] = i
    release = evidence['release']
    adjacent = release.copy()
    adjacent[1:] |= release[:-1]
    adjacent[:-1] |= release[1:]
    boundary = evidence['boundary']
    if boundary.shape != (steps, rows):
        raise RuntimeError('unexpected boundary trace shape')
    return dict(condition=condition, metrics={k: metric(a) for k, a in arrays.items()},
                command_exposure=metric(command), any_readout_difference=metric(any_difference),
                first_differing_expression={key: int((first == i).sum()) for i, key in enumerate(ORDER)},
                first_downstream_expression={key: int((first_downstream == i).sum()) for i, key in enumerate(ORDER)},
                first_expression_denominator_row_steps=rows * steps,
                no_expression_difference=int((first < 0).sum()),
                release_adjacent_command={**metric(command & adjacent),
                                          'condition_row_steps': int(adjacent.sum())},
                boundary_command={**metric(command & boundary),
                                  'condition_row_steps': int(boundary.sum())},
                constructed_witnesses='not run', interpretation='local projections on H states; no benefit verdict')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('output must be a new file')
    m, passive, added, verifier = load_runtime()
    gates, saved = {}, {}
    for rid in PRIMARY + COVERAGE:
        gate, evidence, condition = run_pair(m, passive, added, rid)
        gates[rid] = gate
        if not gate['passed']:
            print(json.dumps(dict(status='STOP: passivity or coupling gate failed', stratum=rid, gate=gate)))
            return 1
        saved[rid] = (evidence, condition)
    # No statistics are aggregated/released until every requested stratum passes.
    report = dict(status='passivity verified; local measurement only', gates=gates,
                  decision='decision:hold-benefit-stage1-open', decision_revision='five',
                  primary=list(PRIMARY), coverage=list(COVERAGE),
                  strata={rid: summarize(m.np, *saved[rid]) for rid in PRIMARY + COVERAGE},
                  source_sha256_ap={name: digest((ROOT / 'src' / (name + '.py')).read_bytes())
                                    for name in ('fly', 'module_identity', 'hold_stage1_instrument')},
                  runner_sha256_ap=digest(Path(__file__).read_bytes()),
                  python=sys.version.split()[0], numpy=m.np.__version__)
    raw = (json.dumps(report, indent=2) + '\n').encode()
    # Aggregate counts can accidentally spell seed digits; never silently write
    # such a report into the scanned record. Review its representation instead.
    if any(verifier.count_number(raw, number) for checker in (m.ph33, m.ph35)
           for number in checker.seed_numbers()):
        raise RuntimeError('report P5 collision; no report written; representation review required')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('xb') as target:
        target.write(raw)
    print('All passivity gates passed; local projection report written. No benefit verdict.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, RuntimeError, ValueError) as exc:
        print('Stage one stopped: ' + str(exc), file=sys.stderr)
        sys.exit(1)
