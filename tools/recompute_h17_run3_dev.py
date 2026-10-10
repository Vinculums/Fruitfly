"""DEV operation check from saved arrays; frozen ROOT arithmetic, no RNG draws."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import recompute_h17_run3 as R

ROOT = Path(__file__).resolve().parents[1]
GATE = 'config/h17-run3-dev-opening.json'
PINS = 'config/h17-run3-dev-pins.json'
MAIN = 'config/h17-run3-execution-pins.json'
FILES = {
    'tools/measure_h17_run3_dev.py', 'tests/test_measure_h17_run3_dev.py',
    'tools/recompute_h17_run3_dev.py', 'tests/test_recompute_h17_run3_dev.py',
    'notes/reviews/2026-10-10-h17-run3-dev-execution-review.md',
    'experiments/h17/h17_run3_dev_implementation_checks.json',
}


def file_digest(path):
    hasher = hashlib.sha256()
    with Path(path).open('rb') as source:
        while chunk := source.read(1 << 20):
            hasher.update(chunk)
    return hasher.hexdigest().translate(R.AP)


def check_files(root, files):
    for name, expected in files.items():
        path = (root / name).resolve()
        if not path.is_relative_to(root) or file_digest(path) != expected:
            raise ValueError('source bytes/' + name)


def check_saved_artifacts(initial):
    for path, expected in initial.items():
        if file_digest(path) != expected:
            raise ValueError('DEV saved artifact changed/' + Path(path).name)


def stage_bindings(root=ROOT):
    root = Path(root).resolve()
    gate, pins, main = (R.read(root / x) for x in (GATE, PINS, MAIN))
    if not (gate['complete'] is True and gate['opened'] is True and
            gate['stage'] == 'dev' and gate['decision'] == 'decision:h17-run3-dev-open' and
            isinstance(gate['owner_instruction'], str) and gate['owner_instruction'].strip()):
        raise ValueError('DEV owner gate')
    if not (pins['complete'] is True and pins['stage'] == 'dev' and
            pins['decision'] == gate['decision'] and
            gate['stage_pins_sha256_alpha'] == file_digest(root / PINS) and
            pins['MAIN_pins_sha256_alpha'] == file_digest(root / MAIN) and
            pins['source_closure_sha256_alpha'] == gate['source_closure_sha256_alpha'] ==
            main['source_closure_sha256_alpha']):
        raise ValueError('DEV stage pins/binding')
    if set(pins['files_sha256_alpha']) != FILES:
        raise ValueError('DEV stage source inventory')
    closure = {k: pins[k] for k in ('MAIN_pins_sha256_alpha',
                'source_closure_sha256_alpha', 'files_sha256_alpha')}
    if R.digest(R.canonical(closure)) != pins['stage_closure_sha256_alpha']:
        raise ValueError('DEV stage closure')
    base = {k: main[k] for k in ('runtime', 'schema_sha256_alpha',
            'keysets_sha256_alpha', 'specification_pins_sha256_alpha', 'files_sha256_alpha')}
    if R.digest(R.canonical(base)) != main['source_closure_sha256_alpha']:
        raise ValueError('MAIN source closure')
    check_files(root, main['files_sha256_alpha'])
    check_files(root, pins['files_sha256_alpha'])
    prior = root / 'experiments/h17/run3/bench'
    actual = {name + '_sha256_alpha': file_digest(prior / (name + ('.npz.ap' if name == 'raw' else '.json')))
              for name in ('identity', 'metrics', 'raw', 'verification', 'parent_recomputation')}
    if actual != pins['prior_artifacts_sha256_alpha'] or gate['prior_verification_sha256_alpha'] != actual['verification_sha256_alpha']:
        raise ValueError('BENCH prerequisite bytes')
    identity, metrics, verifier, parent = (R.read(prior / (x + '.json'))
                                         for x in ('identity', 'metrics', 'verification', 'parent_recomputation'))
    if not (identity['complete'] and identity['passed'] and metrics['complete'] and
            verifier['complete'] and verifier['passed'] and parent['complete'] and parent['passed']):
        raise ValueError('BENCH prerequisite validity')
    if any(x['stage'] != 'bench' or x['smoke'] is not False for x in (identity, metrics, verifier, parent)):
        raise ValueError('BENCH prerequisite mode')
    if any(x['verdict'] != 'PASS' or len(x['clauses']) != 9 or
           any(c['status'] != 'PASS' for c in x['clauses'].values()) for x in (metrics, verifier, parent)):
        raise ValueError('BENCH prerequisite all nine PASS')
    if (parent['verification_sha256_alpha'] != actual['verification_sha256_alpha'] or
            parent['raw_sha256_alpha'] != actual['raw_sha256_alpha'] or
            verifier['raw_sha256_alpha'] != actual['raw_sha256_alpha'] or
            identity['raw_arrays']['sha256_alpha'] != actual['raw_sha256_alpha'] or
            parent['rng_created'] is not False or parent['draws'] != 0 or
            parent['source_closure_sha256_alpha'] != main['source_closure_sha256_alpha']):
        raise ValueError('BENCH parent/evidence binding')
    for saved in (identity, metrics, parent):
        if saved['rows'] != 400 or saved['steps'] != 600:
            raise ValueError('BENCH fixed sample')
    for saved in (identity, verifier):
        if len(saved['gates']) != 20 or any(not (g['complete'] and g['passed'] and
                g['rows'] == 400 and g['steps'] == 600) for g in saved['gates'].values()):
            raise ValueError('BENCH twenty validity gates')
    return dict(format='h17-run3-dev-stage-binding-v3', stage='dev',
                source_closure_sha256_alpha=main['source_closure_sha256_alpha'],
                stage_closure_sha256_alpha=pins['stage_closure_sha256_alpha'],
                stage_pins_sha256_alpha=file_digest(root / PINS),
                opening_sha256_alpha=file_digest(root / GATE),
                MAIN_pins_sha256_alpha=file_digest(root / MAIN),
                prior_verification_sha256_alpha=actual['verification_sha256_alpha'])


def check_input(identity, verified, metrics):
    if not (identity['complete'] and identity['passed'] and verified['complete'] and
            verified['passed'] and metrics['complete']):
        raise ValueError('independent verification prerequisite')
    if any(x['stage'] != 'dev' or x['smoke'] is not False for x in (identity, verified, metrics)):
        raise ValueError('DEV stage binding')
    if any(R.canonical(x['provenance']) != R.canonical(identity['provenance']) for x in (verified, metrics)):
        raise ValueError('verification/provenance binding')
    if verified['raw_sha256_alpha'] != identity['raw_arrays']['sha256_alpha']:
        raise ValueError('verification/raw binding')
    for saved in (identity, metrics):
        if saved['rows'] != 400 or saved['steps'] != 600 or saved['conditions'] != list(R.CONDITIONS):
            raise ValueError('DEV fixed sample')
    if len(verified['gates']) != 20 or any(not (g['complete'] and g['passed'] and
            g['rows'] == 400 and g['steps'] == 600) for g in verified['gates'].values()):
        raise ValueError('DEV twenty validity gates')


def check_clauses(clauses, verdict, saved):
    if set(saved['clauses']) != set(clauses) or saved['verdict'] != verdict:
        raise ValueError('clause keyset/verdict')
    for name, value in clauses.items():
        other = saved['clauses'][name]
        for field in ('bar', 'direction', 'status', 'estimate'):
            if other[field] != value[field]:
                raise ValueError('clause/' + name + '/' + field)
        if not R.np.allclose(other['interval'], value['interval'], rtol=0, atol=2e-15):
            raise ValueError('clause/' + name + '/interval')


def recompute(directory, root=ROOT):
    root, directory = Path(root).resolve(), Path(directory).resolve()
    if directory != root / 'experiments/h17/run3/dev':
        raise ValueError('DEV canonical output')
    initial = {directory / name: file_digest(directory / name) for name in
               ('identity.json', 'metrics.json', 'verification.json', 'stage_binding.json', 'raw.npz.ap')}
    identity, verified, metrics = (R.read(directory / (x + '.json'))
                                 for x in ('identity', 'verification', 'metrics'))
    check_input(identity, verified, metrics)
    binding = stage_bindings(root)
    binding['claim_path'] = identity['claim']
    if R.read(directory / 'stage_binding.json') != binding:
        raise ValueError('DEV saved stage binding')
    prov = identity['provenance']
    if (prov['execution_pins_sha256_alpha'] != binding['MAIN_pins_sha256_alpha'] or
            prov['source_closure_sha256_alpha'] != binding['source_closure_sha256_alpha']):
        raise ValueError('DEV MAIN provenance')
    config = R.read(root / 'config/h17-run3-seeds.json')
    claim_path = root / 'experiments/h17/run3_registry' / (R.digest(R.canonical(config['dev'])) + '.json')
    if identity['claim'] != claim_path.relative_to(root).as_posix():
        raise ValueError('DEV registered pair claim')
    initial[claim_path] = file_digest(claim_path)
    claim = R.read(claim_path)
    terminal = json.loads(bytes.fromhex(claim['result'].translate(R.HEX)).decode('ascii'))
    if not (claim['complete'] is True and claim['stage'] == 'dev' and terminal['complete'] is True and
            claim['prerequisite_verification_sha256_alpha'] == binding['prior_verification_sha256_alpha'] and
            terminal['identity_sha256_alpha'] == file_digest(directory / 'identity.json') and
            terminal['metrics_sha256_alpha'] == file_digest(directory / 'metrics.json') and
            terminal['raw_sha256_alpha'] == identity['raw_arrays']['sha256_alpha'] and
            terminal['status'] == metrics['verdict']):
        raise ValueError('DEV terminal claim binding')
    raw = R.SavedArrays(directory, identity['raw_arrays'])
    try:
        if raw.raw_hash != initial[directory / 'raw.npz.ap']:
            raise ValueError('DEV initial raw binding')
        endpoints, summaries = {}, {}
        for condition in R.CONDITIONS:
            endpoints[condition], summaries[condition] = {}, {}
            for arm in R.ARMS:
                prefix = ('efficacy' if arm in ('Fly', 'GS250') else 'validity') + '/' + condition + '/' + arm
                whiffs = raw.get(prefix + '/sample/W_delivered')
                reach = raw.get(prefix + '/sample/AT2')
                good = raw.get(prefix + '/construction/good')
                engaged = R.np.zeros((600, 400), bool)
                entry_mask = None
                if arm in ('GS250', 'GSOff'):
                    fields = R.policy_arrays(whiffs, raw.get(prefix + '/sample/H_post'),
                        raw.get(prefix + '/sample/cast_sign'), raw.get(prefix + '/gs/BASE_TGT'),
                        raw.get(prefix + '/gs/BASE_TURN'), raw.get(prefix + '/sample/EST'), arm == 'GS250')
                    for name, expected in fields.items():
                        R.same(raw.get(prefix + '/gs/' + name), expected, prefix + '/policy/' + name)
                    R.same(raw.get(prefix + '/sample/TGT'), fields['SEARCH_TGT'], prefix + '/executed target')
                    R.same(raw.get(prefix + '/sample/TURN'), fields['SEARCH_TURN'], prefix + '/executed turn')
                    engaged = fields['engaged']
                else:
                    q = R.np.zeros(400, R.np.int64)
                    shadow = R.np.zeros((600, 400), bool)
                    held = raw.get(prefix + '/sample/H_post')
                    for tick in range(600):
                        q = R.np.where(whiffs[tick].any(axis=1), 0, q + 1)
                        shadow[tick] = (q >= 250) & (held[tick] == -1)
                    entry_mask = shadow & ~R.np.concatenate((R.np.zeros((1, 400), bool), shadow[:-1]), axis=0)
                endpoint = R.row_endpoints(whiffs, reach, good, engaged, entry_mask)
                for name, value in endpoint.items():
                    R.same(raw.get(prefix + '/endpoint/' + name), value, prefix + '/endpoint/' + name)
                endpoints[condition][arm] = endpoint
                summaries[condition][arm] = dict(rows=400, any_whiff=int(endpoint['E'].sum()),
                    lost_last200=int(endpoint['L'].sum()), valued_dwell_majority=int(endpoint['V'].sum()),
                    any_reach=int(endpoint['reach_source'].any(axis=1).sum()),
                    engaged_rows=int(endpoint['ever_engaged'].sum()), entry_events=int(endpoint['entry_event_count'].sum()))
        clauses, verdict = R.required_clauses(endpoints, raw.get('inference/indices'), raw)
        for saved in (metrics, verified):
            check_clauses(clauses, verdict, saved)
        if stage_bindings(root) != {k: v for k, v in binding.items() if k != 'claim_path'}:
            raise ValueError('DEV post audit stage binding')
        check_saved_artifacts(initial)
        return dict(format='h17-run3-dev-root-array-recomputation-v3', date='2026-10-10',
                    complete=True, passed=True, smoke=False, stage='dev', operation_verdict='PASS',
                    source_closure_sha256_alpha=binding['source_closure_sha256_alpha'],
                    stage_closure_sha256_alpha=binding['stage_closure_sha256_alpha'],
                    stage_pins_sha256_alpha=binding['stage_pins_sha256_alpha'],
                    opening_sha256_alpha=binding['opening_sha256_alpha'],
                    stage_binding_sha256_alpha=initial[directory / 'stage_binding.json'],
                    identity_sha256_alpha=initial[directory / 'identity.json'],
                    metrics_sha256_alpha=initial[directory / 'metrics.json'],
                    claim_sha256_alpha=initial[claim_path],
                    raw_sha256_alpha=raw.raw_hash, verification_sha256_alpha=initial[directory / 'verification.json'],
                    checked_arrays=len(raw.checked), rows=400, steps=600,
                    row_summaries=summaries, clauses=clauses, verdict=verdict,
                    rng_created=False, draws=0, first_failure=None)
    finally:
        raw.close()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args(argv)
    result = recompute(args.output)
    payload = R.canonical(result) + b'\n'
    from verify_h17_r0 import no_protected_tokens
    no_protected_tokens(payload, ROOT)
    with (args.output / 'parent_recomputation.json').open('xb') as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    print('Run3 DEV root operation PASS; fixed clauses ' + result['verdict'], flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
