#!/usr/bin/env python3
"""Ordered local stage-two trial; a claimed evaluation cannot be repeated.

Use --stage identity, bench, dev, eval in that order, or --stage all. --smoke
uses spent identity aliases at a smaller size and never opens a bench gate.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import sys

ROOT=Path(__file__).resolve().parents[1]
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','PH30_PROCS','PH33_PROCS','PH32_PROCS'):
    os.environ[name]='1'
sys.path.insert(0,str(ROOT/'src'))
import numpy as np
import hold_stage2_harness as h
import ph15,ph16,ph30
import verify_seed_scan_r2 as seed_verifier
from replay_hold_stage1 import PINS as REFERENCE_PINS

FINAL=ROOT/'notes/hold/2026-10-09-hold-stage2-coverage-design-v2.md'
CONFIG=ROOT/'config/hold-stage2-seeds.json'
SEED_RECEIPT=ROOT/'experiments/hold/hold_seed_registration.json'
I4_CORRECTION=ROOT/'notes/hold/2026-10-09-hold-stage2-i4-gate-correction.md'


def encode(value):
    if isinstance(value,np.ndarray): return value.tolist()
    if isinstance(value,np.generic): return value.item()
    raise TypeError(type(value).__name__)


def write(path,data):
    serialized=json.dumps(data,default=encode,indent=2,allow_nan=False)+'\n'
    legacy=[]
    for checker in (h.M.ph33,h.M.ph35):
        legacy.extend(checker.seed_numbers())
    if any(seed_verifier.count_number(serialized.encode('utf-8'),number) for number in legacy):
        raise RuntimeError('P5 output contains a registered legacy seed token; nothing written')
    temporary=path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(serialized,encoding='utf-8')
    temporary.replace(path)


def provenance(config=CONFIG):
    # Alphabet encoding prevents provenance hashes carrying registered seed
    # strings while retaining an invertible SHA256 representation.
    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest().translate(str.maketrans('0123456789abcdef','abcdefghijklmnop'))
    sources={str(Path(m.__file__).resolve().relative_to(ROOT)):digest(Path(m.__file__))
             for m in list(sys.modules.values()) if getattr(m,'__file__',None)
             and Path(m.__file__).resolve().is_relative_to(ROOT) and Path(m.__file__).suffix=='.py'}
    sources[str(Path(__file__).resolve().relative_to(ROOT))]=digest(Path(__file__))
    return dict(python=sys.version,numpy=np.__version__,platform=platform.platform(),
                final_sha256_alpha=digest(FINAL),seed_config_sha256_alpha=digest(config),
                seed_receipt_sha256_alpha=digest(SEED_RECEIPT),
                I4_correction_sha256_alpha=digest(I4_CORRECTION),
                sources_sha256_alpha=sources,hash_alphabet='abcdefghijklmnop maps to 0123456789abcdef',
                rows=400,steps=600,threads={k:os.environ.get(k) for k in
                ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','PH30_PROCS','PH33_PROCS','PH32_PROCS')})


def guard_previous(record,current):
    if record['provenance']!=current:
        raise RuntimeError('code/runtime provenance changed after the prior gate; reviewed new run required')
    if not record.get('complete',False):
        raise RuntimeError('prior stage interrupted before its durable completion gate')


def interval(a,b=None,kind='DP'):
    _,point,lo,hi=ph16.interval(kind,a,b)
    return dict(point=point,lower=lo,upper=hi)


def power(m,sd,n,bar,strict=False):
    if sd==0: return float(m>bar if strict else m>=bar)
    z=(m-bar)/(sd/math.sqrt(n))-1.959963984540054
    return 0.5*(1.+math.erf(z/math.sqrt(2.)))


def condition_result(measures,free,bootstrap_seed,bench=False):
    ph30.set_stats(1.959963984540054,2.5,97.5,bootstrap_seed)
    ph15.NBOOT=5000
    H,R=measures['H'],measures['R'];n=len(H['V'])
    m2=interval(R['D_neg'],H['D_neg'])
    m2['verdict']='PASS' if m2['lower']>0 else 'FAIL' if m2['upper']<=0 else 'INCONCLUSIVE'
    m3=interval(H['V'],R['V'])
    m3['verdict']='PASS' if m3['lower']>=-0.05 else 'FAIL' if m3['upper']<-0.05 else 'INCONCLUSIVE'
    m4=interval(R['lost'],H['lost']);m4['verdict']='REPORTED';m4['reference_line_lower_at_least']=0.05
    dwell=R['D_neg']-H['D_neg'];dp=H['V'].astype(float)-R['V'].astype(float)
    # Frozen ph23.pass_prob uses the empirical population SD (ddof=0).
    sd=float(np.std(dwell,ddof=0));b=float(np.mean(dp**2));p2=power(float(dwell.mean()),sd,n,0.,strict=True)
    p3=power(float(dp.mean()),math.sqrt(max(0.,b-float(dp.mean())**2)),n,-0.05)
    span=float(free['D_neg'].mean()-H['D_neg'].mean())
    ties={arm:float(x['tie'].mean()) for arm,x in measures.items()}
    m1=span>=1. and all(t<=0.20 for t in ties.values())
    stops=[]
    if span<1.:stops.append('hS')
    if p2<0.5:stops.append('h1')
    if p3<0.5:stops.append('h2')
    if not all(t<=0.20 for t in ties.values()):stops.append('M1/ties')
    return dict(M0='PASS',M1=dict(verdict='PASS' if m1 else 'UNREADABLE',span=span,ties=ties),
        M2=m2,M3=m3,M4=m4,bench_statistics=dict(m=float(dwell.mean()),s=sd,DP=float(dp.mean()),b=b,S=span,
        M2_pass_probability=p2,M3_pass_probability=p3),stop_rules=stops if bench else [],
        verdict='SHOWN' if m1 and m2['verdict']=='PASS' and m3['verdict']=='PASS' else 'UNREADABLE' if not m1 else 'NOT SHOWN',
        proportions={arm:dict(PV=interval(x['V'],kind='P'),lost=interval(x['lost'],kind='P'),tie=interval(x['tie'],kind='P')) for arm,x in measures.items()})


def read(path):return json.loads(path.read_text(encoding='utf-8'))


def run_stage(stage,args,prov):
    guard_provenance(prov,args.seeds)
    out=args.output;out.mkdir(parents=True,exist_ok=True)
    path=out/('hold_stage2_'+('smoke' if args.smoke else stage)+'.json')
    if path.exists():raise RuntimeError('output already exists; use a fresh reviewed output directory: '+str(path))
    if stage=='identity':
        try:
            result=h.identities(40 if args.smoke else 400,100 if args.smoke else 600)
        except h.IdentityFailure as error:
            write(path,dict(stage=stage,smoke=args.smoke,passed=False,complete=False,first=str(error),gates=error.gates,provenance=prov))
            raise
        guard_provenance(prov,args.seeds)
        result.update(stage=stage,smoke=args.smoke,provenance=prov,complete=True)
        write(path,result)
        print('identity PASS; '+str(path),flush=True)
        return
    identity=read(out/'hold_stage2_identity.json');guard_previous(identity,prov)
    if not identity['passed'] or identity.get('smoke'):raise RuntimeError('full identities must pass before bench')
    config=read(args.seeds)
    required=('bench','dev','eval','bootstrap')
    if any(k not in config for k in required):raise RuntimeError('missing registered seed role')
    seed_numbers=[*config['bench'],*config['dev'],*config['eval'],config['bootstrap']]
    if len(set(seed_numbers))!=7:raise RuntimeError('all registered seed roles must be distinct')
    if stage=='bench':conditions=['A5','B3']
    else:
        bench=read(out/'hold_stage2_bench.json');guard_previous(bench,prov)
        if bench['seed_config_sha256_alpha']!=hashlib.sha256(args.seeds.read_bytes()).hexdigest().translate(str.maketrans('0123456789abcdef','abcdefghijklmnop')):
            raise RuntimeError('registered seed config changed after bench')
        conditions=bench['survivors']
        if stage=='eval':
            dev=read(out/'hold_stage2_dev.json');guard_previous(dev,prov)
            if not dev['operation_checks_passed']:raise RuntimeError('development operation checks failed')
            # Exclusive durable claim precedes all evaluation draws. On crash
            # the trial needs review; removing this claim is not an operation.
            registry=ROOT/'experiments/hold/hold_stage2_eval_registry'
            registry.mkdir(parents=True,exist_ok=True)
            # Canonical evaluation-role digest is independent of output path,
            # config location, whitespace, and changes in the other seed roles.
            key=seed_verifier.digest_ap(json.dumps(config['eval'],separators=(',',':')).encode('ascii'))
            claim=dict(evaluation_role_sha256_alpha=key,provenance=prov,
                       output=str(out.resolve().relative_to(ROOT)),policy='One evaluation. No automatic rerun.')
            payload=json.dumps(claim,indent=2)+'\n'
            for checker in (h.M.ph33,h.M.ph35):
                if any(seed_verifier.count_number(payload.encode(),seed) for seed in checker.seed_numbers()):
                    raise RuntimeError('P5 claim collision; evaluation not claimed')
            with (registry/(key+'.claim')).open('x',encoding='utf-8') as f:
                f.write(payload)
    result=dict(stage=stage,provenance=prov,seed_roles='config/hold-stage2-seeds.json:'+stage,
                seed_config_sha256_alpha=hashlib.sha256(args.seeds.read_bytes()).hexdigest().translate(str.maketrans('0123456789abcdef','abcdefghijklmnop')),
                conditions={},raw_arrays={},operation_checks_passed=False,complete=False)
    write(path,result)
    # A6 is a paired report on bench/evaluation; no A6 development run.
    ids=conditions+(['A6'] if stage in ('bench','eval') else [])
    for rid in ids:
        print(stage+' '+rid+' H/R'+('/Free' if rid!='A6' else '')+' running',flush=True)
        outputs={};observers={};metrics={}
        for arm in ('H','R')+(() if rid=='A6' else ('Free',)):
            outputs[arm],observers[arm]=h.run(rid,arm,config[stage],state=False)
            metrics[arm]=h.measures(outputs[arm])
        if observers['H'].rngs!=observers['R'].rngs:
            result['failure']='hI generator state identity failed: '+rid
            write(path,result)
            raise RuntimeError('hI generator state identity failed: '+rid)
        if any(np.any(x['flee_violations']) for x in metrics.values()):
            result['failure']='flee implementation check failed: '+rid
            write(path,result)
            raise RuntimeError('flee implementation check failed: '+rid)
        fields=h.M.L1A if rid.startswith('A') else h.M.L1B
        metrics['first_divergence_any']=h.first_difference(outputs['H'],outputs['R'],fields+('C2','P2','VAL'))
        metrics['first_divergence_trajectory']=h.first_difference(outputs['H'],outputs['R'],h.TRAJECTORY)
        result['raw_arrays'][rid]=metrics
        if rid=='A6':
            result['conditions'][rid]=dict(verdict='REPORTED',command_exposure_steps=int((outputs['H']['CLIPPED']!=outputs['R']['CLIPPED']).sum()),
                first_divergence_any=metrics['first_divergence_any'],first_divergence_trajectory=metrics['first_divergence_trajectory'],
                side_balance={arm:float(np.mean(metrics[arm]['first_source']==0)) for arm in ('H','R')})
        else:
            # Evaluation validity retains the bench's fixed span; the Free
            # evaluation arm is reported as a contemporaneous reference too.
            cr=condition_result({a:metrics[a] for a in ('H','R')},metrics['Free'],config['bootstrap'],bench=stage=='bench')
            if stage!='bench':
                cr['M1']['span']=bench['conditions'][rid]['M1']['span']
                cr['M1']['verdict']='PASS' if cr['M1']['span']>=1 and all(t<=0.20 for t in cr['M1']['ties'].values()) else 'UNREADABLE'
                cr['verdict']='SHOWN' if cr['M1']['verdict']=='PASS' and cr['M2']['verdict']=='PASS' and cr['M3']['verdict']=='PASS' else 'UNREADABLE' if cr['M1']['verdict']!='PASS' else 'NOT SHOWN'
            result['conditions'][rid]=cr
            print(stage+' '+rid+': '+cr['verdict']+'; stops '+','.join(cr['stop_rules']),flush=True)
        # Free row arrays were retained above so the span is reproducible.
        write(path,result)
    if stage=='bench':result['survivors']=[rid for rid in conditions if not result['conditions'][rid]['stop_rules']]
    if stage in ('bench','eval') and 'A6' in result['raw_arrays']:
        floor=float(np.mean(result['raw_arrays']['A6']['H']['V']))
        for rid in conditions:
            result['conditions'][rid]['PV_floor_A6_H']=floor
            result['conditions'][rid]['PV_ceiling_Free']=float(np.mean(result['raw_arrays'][rid]['Free']['V']))
    guard_provenance(prov,args.seeds)
    result['operation_checks_passed']=True
    result['complete']=True
    write(path,result)
    print(stage+' complete; '+str(path),flush=True)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--stage',choices=('identity','bench','dev','eval','all'),required=True)
    parser.add_argument('--output',type=Path,default=ROOT/'experiments/hold/hold_stage2')
    parser.add_argument('--seeds',type=Path,default=ROOT/'config/hold-stage2-seeds.json')
    parser.add_argument('--smoke',action='store_true')
    args=parser.parse_args()
    if args.smoke and args.stage!='identity':parser.error('smoke only runs identities')
    if sys.flags.optimize:raise RuntimeError('assertions must remain enabled')
    seed_verifier.verify_sources(ROOT)
    seed_verifier.load_manifest(ROOT)
    for name,pin in REFERENCE_PINS.items():
        if seed_verifier.digest_ap((ROOT/'src'/(name+'.py')).read_bytes())!=pin:
            raise RuntimeError('reference source pin mismatch: '+name)
    if not FINAL.exists() or not args.seeds.exists():raise RuntimeError('FINAL and registered config required')
    prov=provenance(args.seeds)
    for stage in (('identity','bench','dev','eval') if args.stage=='all' else (args.stage,)):
        run_stage(stage,args,prov)


def guard_provenance(expected,config):
    if provenance(config)!=expected:
        raise RuntimeError('source, FINAL, config, or runtime changed during stage; no completion gate')


if __name__=='__main__':main()
