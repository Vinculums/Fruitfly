"""Root arithmetic from saved Run3 arrays; no trajectory or inference draws.

Endpoint and interval code is independent of the runner and verifier. The sole
verifier utility used at publication is the unchanged protected-token guard.
"""
import os
for _name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
              'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[_name] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys
import tempfile
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
AP = str.maketrans('0123456789abcdef', 'abcdefghijklmnop')
HEX = str.maketrans('abcdefghijklmnop', '0123456789abcdef')
CONDITIONS = ('C0', 'T1', 'W1', 'T3')
ARMS = ('Fly', 'GS250', 'Passive', 'Agent17', 'GSOff')


def digest(data):
    return hashlib.sha256(data).hexdigest().translate(AP)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False).encode('ascii')


def read(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('duplicate JSON key')
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding='utf-8'),
                      object_pairs_hook=unique,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite JSON')))


def same(actual, expected, field):
    actual, expected = np.asarray(actual), np.asarray(expected)
    if (actual.dtype != expected.dtype or actual.shape != expected.shape or
            actual.tobytes() != expected.tobytes()):
        raise ValueError(field)


class SavedArrays:
    def __init__(self, directory, descriptor):
        self.descriptor = descriptor
        if descriptor['path'] != 'raw.npz.ap':
            raise ValueError('raw/path')
        self.decoded = tempfile.TemporaryFile('w+b')
        hasher = hashlib.sha256()
        with (directory / descriptor['path']).open('rb') as source:
            while payload := source.read(1 << 20):
                if len(payload) % 2 or re.fullmatch(rb'[a-p]+', payload) is None:
                    raise ValueError('raw/AP encoding')
                hasher.update(payload)
                self.decoded.write(bytes.fromhex(payload.decode('ascii').translate(HEX)))
        self.raw_hash = hasher.hexdigest().translate(AP)
        if self.raw_hash != descriptor['sha256_alpha']:
            raise ValueError('raw/hash')
        self.decoded.seek(0)
        self.arrays = np.load(self.decoded, allow_pickle=False)
        if (len(self.arrays.files) != len(set(self.arrays.files)) or
                sorted(self.arrays.files) != descriptor['keys']):
            raise ValueError('raw/keyset')
        self.checked = set()

    def get(self, key):
        value = self.arrays[key]
        description = self.descriptor['arrays'][key]
        actual = dict(dtype=value.dtype.str, shape=list(value.shape),
                      nbytes=value.nbytes, sha256_alpha=digest(value.tobytes()))
        if actual != description or value.dtype.hasobject:
            raise ValueError('raw/array hash/' + key)
        self.checked.add(key)
        return value

    def close(self):
        self.arrays.close()
        self.decoded.close()


def first(mask):
    return np.where(mask.any(axis=0), mask.argmax(axis=0), -1).astype(np.int64)


def row_endpoints(whiffs, reach, good, engaged, entry_mask=None):
    if whiffs.dtype != np.bool_ or reach.dtype != np.bool_:
        raise ValueError('endpoint/native bool')
    if whiffs.shape != reach.shape or whiffs.shape[0] != 600:
        raise ValueError('endpoint/fixed horizon')
    rows = whiffs.shape[1]
    dwell = reach.sum(axis=0, dtype=np.int64)
    dg = dwell[np.arange(rows), good]
    other = dwell[np.arange(rows), 1 - good]
    previous = np.concatenate((np.zeros((1, rows), dtype=bool), engaged[:-1]), axis=0)
    entries = engaged & ~previous if entry_mask is None else entry_mask
    return dict(E=whiffs.any(axis=(0, 2)), L=~whiffs[400:600].any(axis=(0, 2)),
                V=dg > other, D_source=dwell,
                D_source_last200=reach[400:600].sum(axis=0, dtype=np.int64),
                D_good=dg, D_other=other, whiff_source=whiffs.any(axis=0),
                reach_source=reach.any(axis=0), ever_engaged=engaged.any(axis=0),
                first_entry_step=first(entries),
                entry_event_count=entries.sum(axis=0, dtype=np.int64))


def policy_arrays(delivered, held, cast_sign, base_tgt, base_turn, est, enabled):
    ticks, rows = held.shape
    qpre = np.empty((ticks, rows), np.int64)
    qpost = np.empty_like(qpre)
    q = np.zeros(rows, np.int64)
    for tick in range(ticks):
        qpre[tick] = q
        q = np.where(delivered[tick].any(axis=1), 0, q + 1)
        qpost[tick] = q
    eligible = (qpost >= 250) & (held == -1)
    engaged = eligible & enabled
    u = np.where(engaged, qpost - 250, -1).astype(np.int64)
    leg = np.zeros_like(u)
    boundary, k = 0, 0
    pending = engaged.copy()
    while pending.any():
        k += 1
        boundary += 30 * k
        ending = pending & (u < boundary)
        leg[ending] = k
        pending[ending] = False
    remaining = np.where(engaged, 30 * leg * (leg + 1) // 2 - u, 0).astype(np.int64)
    sigma = np.where(engaged, cast_sign * np.where(leg % 2 == 1, 1, -1), 0).astype(np.int8)
    alpha = np.where(engaged, np.where(u % 300 < 150, 1, -1), 0).astype(np.int8)
    original_diff = (base_tgt - est + 180.0) % 360.0 - 180.0
    base_clip = np.clip(0.6 * original_diff, -40.0, 40.0)
    residual = base_turn - base_clip
    search_tgt = (180.0 + sigma * (90.0 - alpha * 15.0)) % 360.0
    search_diff = (search_tgt - est + 180.0) % 360.0 - 180.0
    search_clip = np.clip(0.6 * search_diff, -40.0, 40.0)
    search_turn = search_clip + residual
    entry = engaged & ~np.concatenate((np.zeros((1, rows), bool), engaged[:-1]), axis=0)
    return dict(q_pre=qpre, q_post=qpost, eligible=eligible, engaged=engaged,
                u=u, leg=leg, remaining=remaining, sigma=sigma, alpha=alpha,
                BASE_TGT=base_tgt, BASE_TURN=base_turn, BASE_CLIP=base_clip,
                RESIDUAL=residual, SEARCH_TGT=np.where(engaged, search_tgt, base_tgt),
                SEARCH_CLIP=np.where(engaged, search_clip, base_clip),
                SEARCH_TURN=np.where(engaged, search_turn, base_turn), entry=entry)


def wilson_interval(values):
    n = len(values)
    p = int(np.count_nonzero(values)) / n
    z = 1.959963984540054
    denominator = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denominator
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
    return p, (center - half, center + half)


def judge(estimate, interval, bar, direction):
    lo, hi = map(float, interval)
    if direction == 'lower':
        status = 'PASS' if lo >= bar else 'FAIL' if hi < bar else 'INCONCLUSIVE'
    else:
        status = 'PASS' if hi <= bar else 'FAIL' if lo > bar else 'INCONCLUSIVE'
    return dict(estimate=float(estimate), interval=[lo, hi], bar=float(bar),
                direction=direction, status=status)


def required_clauses(endpoints, indices, raw=None):
    if indices.dtype != np.dtype('<i8') or indices.shape != (5000, 400):
        raise ValueError('inference/fixed indices')
    if not ((indices >= 0) & (indices < 400)).all():
        raise ValueError('inference/index range')
    clauses = {}
    for condition, name, bar, direction in (
            ('C0', 'E', .10, 'lower'), ('T1', 'V', -.05, 'lower'),
            ('T3', 'V', -.05, 'lower'), ('T1', 'L', .05, 'upper'),
            ('W1', 'L', .05, 'upper'), ('T3', 'L', .05, 'upper'),
            ('W1', 'D_other', -6., 'lower')):
        arms = endpoints[condition]
        delta = arms['GS250'][name].astype(np.int64) - arms['Fly'][name].astype(np.int64)
        means = np.mean(delta[indices], axis=1, dtype=np.float64)
        interval = np.quantile(means, [.025, .975], method='linear')
        key = condition + '_' + name
        if raw is not None:
            for field, expected in (('difference', delta), ('replicate_mean', means), ('interval', interval)):
                same(raw.get('inference/' + key + '/' + field), expected, key + '/' + field)
        clauses[key] = judge(np.mean(delta, dtype=np.float64), interval, bar, direction)
    for key, values, bar, direction in (
            ('C0_absolute', endpoints['C0']['GS250']['E'], .5, 'lower'),
            ('T1_intervention', endpoints['T1']['GS250']['ever_engaged'], .05, 'upper')):
        estimate, interval = wilson_interval(values)
        clauses[key] = judge(estimate, interval, bar, direction)
    statuses = [x['status'] for x in clauses.values()]
    verdict = ('PASS' if all(x == 'PASS' for x in statuses) else
               'NOT_SHOWN' if 'FAIL' in statuses else 'INCONCLUSIVE/NOT_SHOWN')
    return clauses, verdict


def recompute(directory, smoke=False):
    identity = read(directory / 'identity.json')
    verified = read(directory / 'verification.json')
    metrics = read(directory / 'metrics.json')
    if not (identity['complete'] and identity['passed'] and verified['complete'] and
            verified['passed'] and metrics['complete']):
        raise ValueError('independent verification prerequisite')
    if any(saved['smoke'] is not smoke for saved in (identity, verified, metrics)):
        raise ValueError('H0/MAIN mode')
    if (identity['stage'] != verified['stage'] or identity['stage'] != metrics['stage'] or
            identity['stage'] not in (('H0',) if smoke else ('bench',))):
        raise ValueError('verification/stage binding')
    if any(canonical(saved['provenance']) != canonical(identity['provenance'])
           for saved in (verified, metrics)):
        raise ValueError('verification/provenance binding')
    if verified['raw_sha256_alpha'] != identity['raw_arrays']['sha256_alpha']:
        raise ValueError('verification/raw binding')
    pins_path = ROOT / 'config' / ('h17-run3-implementation-pins.json' if smoke else 'h17-run3-execution-pins.json')
    pins = read(pins_path)
    if (digest(pins_path.read_bytes()) != identity['provenance']['execution_pins_sha256_alpha'] or
            pins['source_closure_sha256_alpha'] != identity['provenance']['source_closure_sha256_alpha']):
        raise ValueError('current pins/binding')
    rows = 40 if smoke else 400
    if any(saved['rows'] != rows or saved['steps'] != 600 or
           saved['conditions'] != list(CONDITIONS) for saved in (identity, metrics)):
        raise ValueError('fixed sample')
    raw = SavedArrays(directory, identity['raw_arrays'])
    try:
        endpoints, summaries = {}, {}
        for condition in CONDITIONS:
            endpoints[condition], summaries[condition] = {}, {}
            for arm in ARMS:
                prefix = ('efficacy' if arm in ('Fly', 'GS250') else 'validity') + '/' + condition + '/' + arm
                whiffs = raw.get(prefix + '/sample/W_delivered')
                reach = raw.get(prefix + '/sample/AT2')
                good = raw.get(prefix + '/construction/good')
                engaged = np.zeros((600, rows), bool)
                entry_mask = None
                if arm in ('GS250', 'GSOff'):
                    fields = policy_arrays(whiffs, raw.get(prefix + '/sample/H_post'),
                        raw.get(prefix + '/sample/cast_sign'), raw.get(prefix + '/gs/BASE_TGT'),
                        raw.get(prefix + '/gs/BASE_TURN'), raw.get(prefix + '/sample/EST'), arm == 'GS250')
                    for name, expected in fields.items():
                        same(raw.get(prefix + '/gs/' + name), expected, prefix + '/policy/' + name)
                    same(raw.get(prefix + '/sample/TGT'), fields['SEARCH_TGT'], prefix + '/executed target')
                    same(raw.get(prefix + '/sample/TURN'), fields['SEARCH_TURN'], prefix + '/executed turn')
                    engaged = fields['engaged']
                else:
                    q = np.zeros(rows, np.int64)
                    shadow = np.zeros((600, rows), bool)
                    held = raw.get(prefix + '/sample/H_post')
                    for tick in range(600):
                        q = np.where(whiffs[tick].any(axis=1), 0, q + 1)
                        shadow[tick] = (q >= 250) & (held[tick] == -1)
                    entry_mask = shadow & ~np.concatenate((np.zeros((1, rows), bool), shadow[:-1]), axis=0)
                endpoint = row_endpoints(whiffs, reach, good, engaged, entry_mask)
                for name, value in endpoint.items():
                    same(raw.get(prefix + '/endpoint/' + name), value, prefix + '/endpoint/' + name)
                endpoints[condition][arm] = endpoint
                summaries[condition][arm] = dict(rows=rows,
                    any_whiff=int(endpoint['E'].sum()), lost_last200=int(endpoint['L'].sum()),
                    valued_dwell_majority=int(endpoint['V'].sum()),
                    any_reach=int(endpoint['reach_source'].any(axis=1).sum()),
                    engaged_rows=int(endpoint['ever_engaged'].sum()),
                    entry_events=int(endpoint['entry_event_count'].sum()))
        if smoke:
            if metrics['clauses'] or verified['clauses'] or metrics['verdict'] != 'VALIDITY_ONLY':
                raise ValueError('H0/statistics forbidden')
            if any(x.startswith('inference/') for x in raw.arrays.files):
                raise ValueError('H0/inference forbidden')
            clauses, verdict = {}, 'VALIDITY_ONLY'
        else:
            clauses, verdict = required_clauses(endpoints, raw.get('inference/indices'), raw)
            for saved in (metrics, verified):
                if set(saved['clauses']) != set(clauses) or saved['verdict'] != verdict:
                    raise ValueError('clause keyset/verdict')
                for name, value in clauses.items():
                    other = saved['clauses'][name]
                    for field in ('bar', 'direction', 'status'):
                        if other[field] != value[field]:
                            raise ValueError('clause/' + name + '/' + field)
                    if not np.allclose(other['interval'], value['interval'], rtol=0, atol=2e-15):
                        raise ValueError('clause/' + name + '/interval')
                    if other['estimate'] != value['estimate']:
                        raise ValueError('clause/' + name + '/estimate')
        return dict(format='h17-run3-root-array-recomputation-v3', date='2026-10-10',
                    complete=True, passed=True, smoke=smoke, stage=identity['stage'],
                    source_closure_sha256_alpha=identity['provenance']['source_closure_sha256_alpha'],
                    raw_sha256_alpha=raw.raw_hash,
                    verification_sha256_alpha=digest((directory / 'verification.json').read_bytes()),
                    checked_arrays=len(raw.checked), rows=rows, steps=600,
                    row_summaries=summaries, clauses=clauses, verdict=verdict,
                    rng_created=False, draws=0, first_failure=None)
    finally:
        raw.close()


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--smoke', action='store_true')
    args = parser.parse_args(argv)
    result = recompute(args.output.resolve(), args.smoke)
    payload = canonical(result) + b'\n'
    from verify_h17_r0 import no_protected_tokens
    no_protected_tokens(payload, ROOT)
    target = args.output / 'parent_recomputation.json'
    with target.open('xb') as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    print('Run3 root saved-array recomputation PASS; ' + result['verdict'], flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
