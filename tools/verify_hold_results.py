"""Read stored rows and independently verify hold headlines; no simulation."""
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'tools'))
import verify_seed_scan_r2 as legacy
import ph33, ph35


def digest(p):
    return legacy.digest_ap(p.read_bytes())


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def same(actual, expected):
    assert np.allclose(actual, expected, rtol=1e-12, atol=1e-12), (actual, expected)


def paired(a, b, index):
    a, b = np.asarray(a, float), np.asarray(b, float)
    # Same registered estimator, independently written; no ph15.boot call.
    resampled = a[index].mean(1) - b[index].mean(1)
    lo, hi = np.percentile(resampled, (2.5, 97.5))
    return [float(a.mean()-b.mean()), float(lo), float(hi)]


def power(mean, sd, n, bar, strict=False):
    if sd == 0:
        return float(mean > bar if strict else mean >= bar)
    z = (mean-bar) * math.sqrt(n) / sd - 1.959963984540054
    return (1 + math.erf(z/math.sqrt(2))) / 2


def proportion(values):
    n=len(values)
    p=float(np.mean(values))
    z2=1.959963984540054**2
    denom=1+z2/n
    center=(p+z2/(2*n))/denom
    radius=math.sqrt(z2*(p*(1-p)/n+z2/(4*n*n)))/denom
    return [p,center-radius,center+radius]


def physical_mapping(world_seed, n):
    cell = np.empty(n, int)
    cell[np.random.default_rng(world_seed+10000).permutation(n)] = np.arange(n) % 4
    good = cell // 2
    plus_y = np.where(cell % 2 == 0, good, 1-good)
    return cell, good, plus_y


def verify_stage2(path, config):
    r = read(path)
    assert r['complete'] and r['operation_checks_passed']
    assert r['provenance']['seed_config_sha256_alpha'] == digest(ROOT/'config/hold-stage2-seeds.json')
    for p, wanted in r['provenance']['sources_sha256_alpha'].items():
        assert digest(ROOT/p) == wanted, p
    assert digest(ROOT/'notes/hold/2026-10-09-hold-stage2-coverage-design-v2.md') == r['provenance']['final_sha256_alpha']
    assert digest(ROOT/'experiments/hold/hold_seed_registration.json') == r['provenance']['seed_receipt_sha256_alpha']
    assert digest(ROOT/'notes/hold/2026-10-09-hold-stage2-i4-gate-correction.md') == r['provenance']['I4_correction_sha256_alpha']
    bench = r if r['stage']=='bench' else read(path.parent/'hold_stage2_bench.json')
    expected_ids = ['A5','B3'] if r['stage']=='bench' else bench['survivors']
    expected_ids = expected_ids + (['A6'] if r['stage'] in ('bench','eval') else [])
    assert set(r['conditions']) == set(r['raw_arrays']) == set(expected_ids)
    result = {'stage': r['stage'], 'input_sha256_ap': digest(path), 'conditions': {}}
    for rid, data in r['raw_arrays'].items():
        n = len(data['H']['V'])
        assert n == 400
        cell, good, plus_y = physical_mapping(config[r['stage']][0], n)
        summary = {'physical_balance': {}, 'mapping': {'cell': cell.tolist(), 'good': good.tolist(), 'plus_y': plus_y.tolist()}}
        for arm in ('H', 'R'):
            x = data[arm]
            d0, d1 = np.asarray(x['dwell_source_0']), np.asarray(x['dwell_source_1'])
            first = np.asarray(x['first_source'])
            plus_majority = np.where(plus_y == 0, d0, d1) > np.where(plus_y == 0, d1, d0)
            summary['physical_balance'][arm] = {'first_plus_y': int((first==plus_y).sum()),
                'first_source_absent': int((first<0).sum()), 'dwell_majority_plus_y': int(plus_majority.sum()),
                'ties': int((d0==d1).sum()), 'denominator': n,
                'source_index_zero_first_fraction': float((first==0).mean())}
            same(np.asarray(x['V'], bool), np.where(good==0,d0,d1)>np.where(good==0,d1,d0))
            same(x['D_neg'], np.where(good==0,d1,d0))
            assert not any(x['flee_violations'])
        if rid != 'A6':
            # Existing ph15 cache resets from exactly this seed at each condition.
            index = np.random.default_rng(config['bootstrap']).integers(0,n,(5000,n))
            H, R = data['H'], data['R']
            stats = r['conditions'][rid]
            for name, a, b in (('M2',R['D_neg'],H['D_neg']), ('M3',H['V'],R['V']), ('M4',R['lost'],H['lost'])):
                expected = paired(a,b,index)
                actual = stats[name]
                same([actual['point'],actual['lower'],actual['upper']], expected)
                summary[name] = expected
            delta = np.asarray(R['D_neg']) - np.asarray(H['D_neg'])
            dp = np.asarray(H['V'],float) - np.asarray(R['V'],float)
            m, s = float(delta.mean()), float(delta.std(ddof=0))
            difference, discordant = float(dp.mean()), float((dp*dp).mean())
            span = float(np.mean(data['Free']['D_neg'])-np.mean(H['D_neg']))
            p2, p3 = power(m,s,n,0,True), power(difference,math.sqrt(max(0,discordant-difference*difference)),n,-0.05)
            for key, expected in {'m':m,'s':s,'DP':difference,'b':discordant,'S':span,
                                  'M2_pass_probability':p2,'M3_pass_probability':p3}.items():
                same(stats['bench_statistics'][key],expected)
            summary.update(m=m,s=s,DP=difference,b=discordant,span=span,M2_pass_probability=p2,M3_pass_probability=p3,
                           stops=stats['stop_rules'],reported_verdict=stats['verdict'])
            m2 = summary['M2']
            m3 = summary['M3']
            m2_verdict = 'PASS' if m2[1]>0 else 'FAIL' if m2[2]<=0 else 'INCONCLUSIVE'
            m3_verdict = 'PASS' if m3[1]>=-0.05 else 'FAIL' if m3[2]<-0.05 else 'INCONCLUSIVE'
            assert stats['M2']['verdict'] == m2_verdict
            assert stats['M3']['verdict'] == m3_verdict
            validity_span = span if r['stage']=='bench' else bench['conditions'][rid]['M1']['span']
            same(stats['M1']['span'],validity_span)
            tie_rates = {a:float(np.mean(data[a]['tie'])) for a in ('H','R')}
            for a,v in tie_rates.items():
                same(stats['M1']['ties'][a],v)
            readable = validity_span>=1 and all(v<=0.20 for v in tie_rates.values())
            verdict = 'UNREADABLE' if not readable else 'SHOWN' if m2_verdict==m3_verdict=='PASS' else 'NOT SHOWN'
            assert stats['M0']=='PASS' and stats['M1']['verdict']==('PASS' if readable else 'UNREADABLE')
            assert stats['verdict']==verdict
            summary['independent_verdict'] = verdict
            summary['validity_span'] = validity_span
            for a in ('H','R'):
                for label,field in (('PV','V'),('lost','lost'),('tie','tie')):
                    reported=stats['proportions'][a][label]
                    same([reported['point'],reported['lower'],reported['upper']],proportion(data[a][field]))
            if r['stage'] in ('bench','eval'):
                same(stats['PV_floor_A6_H'],np.mean(r['raw_arrays']['A6']['H']['V']))
                same(stats['PV_ceiling_Free'],np.mean(data['Free']['V']))
            if r['stage']=='bench':
                stops = ([] if span>=1 else ['hS']) + ([] if p2>=0.5 else ['h1']) + ([] if p3>=0.5 else ['h2'])
                if any(np.mean(data[a]['tie'])>0.20 for a in ('H','R')):
                    stops.append('M1/ties')
                assert stops == stats['stop_rules']
            else:
                assert stats['stop_rules']==[]
        result['conditions'][rid] = summary
    if r['stage']=='bench':
        assert r['survivors']==[rid for rid in ('A5','B3') if not result['conditions'][rid]['stops']]
    result['checks_passed'] = True
    return result


def verify_d0(path):
    r=read(path)
    assert r['sample']=='full'
    assert all(x['passed'] for x in r['gates'].values())
    for p, wanted in r['provenance']['source_sha256_ap'].items():
        assert digest(ROOT/p)==wanted, p
    rows={}
    for rid, s in r['strata'].items():
        for name,m in s['metrics'].items():
            assert sum(m['events_per_row'])==m['events']
            assert sum(x>0 for x in m['events_per_row'])==m['rows_exposed']
        records=s['holds']['records']
        assert max(x['maximum_held_counter'] for x in records)==s['holds']['maximum_held_counter']
        assert sum(x['maximum_held_counter']>=s['holds']['window'] for x in records)==s['holds']['at_or_above_window']
        rows[rid]={'command_events':s['metrics']['clipped_turn']['events'],
                   'command_rows':s['metrics']['clipped_turn']['rows_exposed'],
                   'maximum_held_counter':s['holds']['maximum_held_counter'],
                   'window':s['holds']['window'],'hold_count':len(records),
                   'bound_checks':s['section3_bound_checks']}
        if 'burst_ties' in s:
            for name,m in s['burst_ties'].items():
                if isinstance(m,dict) and 'per_row' in m:
                    assert sum(m['per_row'])==m['row_steps']
                    assert sum(x>0 for x in m['per_row'])==m['rows']
            rows[rid]['burst_ties']={name:m['row_steps'] for name,m in s['burst_ties'].items() if isinstance(m,dict)}
            rows[rid]['f_id']=s['burst_ties']['f_id']
    proxy={}
    for candidate,p in r['proxies'].items():
        for name in ('simultaneous_bursts','latest_burst_tie_row_steps','tied_single_nonburst_row_steps'):
            same(sum(p[name]['expected_per_row']),p[name]['expected_total'])
        expected_upper=sum(min(x,1) for x in p['tied_single_nonburst_row_steps']['expected_per_row'])
        same(expected_upper,p['expected_exposed_rows_upper_bound'])
        same(min(expected_upper/40,1),p['probability_at_least_40_rows_upper_bound'])
        proxy[candidate]={'expected_tied_single_events':p['tied_single_nonburst_row_steps']['expected_total'],
                          'expected_exposed_rows_upper':expected_upper,'probability_40_rows_upper':min(expected_upper/40,1)}
    return {'input_sha256_ap':digest(path),'checks_passed':True,'strata':rows,'proxies':proxy,
            'next_step_reading':r['next_step_reading'],'scope':'fixed sample and frozen-path proxies; no universal horizon theorem'}


def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('independent verification requires assertions enabled')
    receipt={'date':'2026-10-09','reviewer':'root session, independently written estimator; no simulation',
             'verifier_sha256_ap':digest(Path(__file__)), 'stage2':{}}
    d0=ROOT/'experiments/hold/hold_d0_replay.json'
    if d0.exists():
        receipt['D0']=verify_d0(d0)
    config=read(ROOT/'config/hold-stage2-seeds.json')
    for stage in ('bench','dev','eval'):
        p=ROOT/f'experiments/hold/hold_stage2_corrected/hold_stage2_{stage}.json'
        if p.exists() and read(p).get('complete'):
            receipt['stage2'][stage]=verify_stage2(p,config)
    receipt['reporting_correction']="Stage-two side_balance in A6 is source-index-zero first-arrival, not physical +y. This receipt reconstructs the registered balanced World7 mapping and prints physical +y metrics. first_divergence_any denotes first recorded-field divergence."
    raw=(json.dumps(receipt,indent=2)+'\n').encode()
    if any(legacy.count_number(raw,n) for c in (ph33,ph35) for n in c.seed_numbers()):
        raise RuntimeError('P5 collision; representation review required')
    target=ROOT/'experiments/hold/hold_results_verification.json'
    target.write_bytes(raw)
    print(json.dumps({k:v for k,v in receipt.items() if k in ('D0','stage2')},indent=2))


if __name__=='__main__':
    main()
