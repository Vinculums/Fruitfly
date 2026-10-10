"""Pinned GS250 measurement entry point. No generators are constructed on import."""
import os
THREADS=('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS')
for _key in THREADS:os.environ[_key]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
for _key in ('PH30_PROCS','PH32_PROCS','PH33_PROCS'):os.environ[_key]='1'
import argparse
import gc
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import h17_run3_recording as H
from h17_run3_recording import require,equal,digest,canonical,EvidenceError
import measure_h17_r0 as R

ROOT=Path(__file__).resolve().parents[1]
DESIGN='experiments/h17/h17_run3_design_v3.md'
SCHEMA='experiments/h17/h17_run3_evidence_schema.json'
KEYSETS='experiments/h17/h17_run3_array_keysets.json'
RUNTIME='experiments/h17/h17_run3_runtime.json'
CONFIG='config/h17-run3-seeds.json'
REGISTRATION='experiments/h17/h17_run3_seed_registration.json'
SPECIFICATION='config/h17-run3-specification-pins.json'
OPENING='config/h17-run3-execution-opening.json'
BASE_PINS='config/h17-run3-implementation-pins.json'
PINS='config/h17-run3-execution-pins.json'
H0='experiments/h17/run3/H0'
REGISTRY='experiments/h17/run3_registry'
AMENDMENT='experiments/h17/h17_run3_implementation_amendment_v1.md'
REVIEW='notes/reviews/2026-10-10-h17-run3-execution-review.md'
DATE='2026-10-10'
read=R.read
file_digest=R.file_digest
write_json=R.write_json
runtime_stamp=R.runtime_stamp


def schema_contract(root=ROOT):return read(Path(root)/SCHEMA)


def required_pin_files(root=ROOT):
    root=Path(root);opening=read(root/OPENING);spec=read(root/SPECIFICATION)
    paths=set(spec['files_sha256_alpha'])|set(opening['immutable_specification_files_sha256_alpha'])
    paths.update(opening['implementation_paths'])
    paths.update((OPENING,AMENDMENT,REVIEW,'experiments/h17/h17_run3_implementation_checks.json',
        'experiments/h17/h17_run3_execution_opening_checks.json','tools/recompute_h17_run3.py','tests/test_recompute_h17_run3.py'))
    paths.update(('tools/check_h17_run3_boundaries.py','experiments/h17/h17_run3_native_boundary_checks.json'))
    paths.update(p.relative_to(root).as_posix() for p in (root/'src').glob('*.py'))
    return sorted(paths)


def source_closure(pins):
    return digest(canonical({key:pins[key] for key in ('runtime','schema_sha256_alpha','keysets_sha256_alpha','specification_pins_sha256_alpha','files_sha256_alpha')}))


def registration_check(root,config):
    reg=read(root/REGISTRATION);numbers=[]
    for stage in ('bench','dev','eval'):
        pair=config[stage];require(len(pair)==2 and all(type(x) is int and x>=0 for x in pair),'registration/pair')
        w,a=pair;i=config['inference'][stage]
        roles=dict(world=w,agent=a,inference=i,world_balance=w+10000,c0_geometry=w+20000,cast=a+20000)
        equal(reg['stages'][stage],roles,'registration/derived roles/'+stage);numbers.extend(roles.values())
    require(len(set(numbers))==18 and reg['numbers']==numbers,'registration/all unique roles')
    local,graph=reg['local_scan'],reg['graph_scan']
    require(reg['complete'] is True and reg['config']==CONFIG and reg['distinct_role_count']==18 and reg['all_stage_roles_disjoint'] is True and reg['prior_roles_disjoint'] is True,'registration/contract')
    require(local['passed'] is True and local['hits']==[] and local['errors']==[] and local['exclusions']==['.git','__pycache__'],'registration/source scan')
    # Mixed FTS/vector pagination does not describe completeness of the literal
    # scan. The immutable receipt separately records the full canonical corpus.
    require(graph['passed'] is True and graph['all_canonical_read_verified'] is True and graph['canonical_documents']==258 and graph['literal_hits']==[],
            'registration/full canonical graph scan')
    require(all(item['verified'] is True and item['role_hits']==[] for item in graph['read_transport_fallbacks']),
            'registration/canonical transport reads')
    queries=graph['queries']
    require(len(queries)==18 and all(type(q['role_index']) is int and q['role_index']==j and q['executed'] is True and
        q['error'] is None and q['literal_hit'] is False and q['arms']=='fts+vector' and type(q['keyword_rows']) is int and
        q['keyword_rows']==0 and type(q['has_more']) is bool for j,q in enumerate(queries)),'registration/graph role queries')
    for key in ('fresh_generators_created','fresh_random_draws','claims_created'):require(reg[key]==0,'registration/'+key)
    for key in ('bootstrap_performed','simulation_performed','protected_seed_exceptions_added'):require(reg[key] is False,'registration/'+key)
    return reg


def preflight(root=ROOT,smoke=False,stage='bench'):
    root=Path(root);pinpath=BASE_PINS if smoke else PINS;pins=read(root/pinpath)
    require(pins['complete'] is True and pins['decision']=='decision:h17-run3-open','pins/opening')
    equal(pins['runtime'],runtime_stamp(),'pins/current runtime')
    equal(pins['runtime'],read(root/RUNTIME)['runtime'],'pins/frozen runtime')
    for name,key in ((SCHEMA,'schema'),(KEYSETS,'keysets'),(SPECIFICATION,'specification_pins')):
        require(file_digest(root/name)==pins[key+'_sha256_alpha'],'pins/'+key)
    require(set(pins['files_sha256_alpha'])==set(required_pin_files(root)),'pins/complete closure')
    require(source_closure(pins)==pins['source_closure_sha256_alpha'],'pins/closure digest')
    for name,sha in pins['files_sha256_alpha'].items():
        path=(root/name).resolve();require(path.is_relative_to(root.resolve()) and path.is_file(),'pins/path/'+name)
        require(file_digest(path)==sha,'pins/source/'+name)
    opening=read(root/OPENING)
    require(opening['complete'] is True and opening['decision']=='decision:h17-run3-open' and opening['candidate']=='GS250' and opening['registry']==REGISTRY and opening['MAIN_rows']==400 and opening['H0_rows']==40 and opening['ticks']==600 and opening['required_clauses']==9,'opening/contract')
    require(opening['authorized']['spent_input_H0'] is True and opening['authorized']['one_fresh_BENCH_after_H0_PASS'] is True,'opening/authority')
    for name,sha in opening['immutable_specification_files_sha256_alpha'].items():require(file_digest(root/name)==sha,'opening/immutable/'+name)
    require(smoke or stage=='bench','opening/DEV EVAL not opened')
    config=read(root/CONFIG);registration_check(root,config)
    boundaries=read(root/'experiments/h17/h17_run3_native_boundary_checks.json')
    require(boundaries['complete'] is True and boundaries['passed'] is True and boundaries['fresh_generators_created']==0 and boundaries['fresh_random_draws']==0 and boundaries['simulation_performed'] is False,'native boundaries/validity closure')
    require(boundaries['program_sha256_alpha']==file_digest(root/'tools/check_h17_run3_boundaries.py') and boundaries['native_source_sha256_alpha']==file_digest(root/'src/fly.py'),'native boundaries/source closure')
    prov={key+'_sha256_alpha':file_digest(root/path) for key,path in (
        ('design',DESIGN),('seed_config',CONFIG),('seed_registration',REGISTRATION),('schema',SCHEMA),('keysets',KEYSETS),('runtime',RUNTIME),('specification_pins',SPECIFICATION),('opening',OPENING))}
    prov.update(execution_pins_sha256_alpha=file_digest(root/pinpath),source_closure_sha256_alpha=source_closure(pins),runtime=pins['runtime'])
    if not smoke:
        base=read(root/BASE_PINS);require(pins['base_pins_sha256_alpha']==file_digest(root/BASE_PINS) and source_closure(base)==source_closure(pins),'MAIN/base closure')
        h0_prerequisites(root,pins,prov)
    return pins,config,prov


def h0_prerequisites(root,pins,provenance):
    h0=pins['h0'];require(set(h0)=={'identity_sha256_alpha','metrics_sha256_alpha','raw_sha256_alpha','verification_sha256_alpha','parent_recomputation_sha256_alpha','source_closure_sha256_alpha'} and h0['source_closure_sha256_alpha']==source_closure(pins),'H0/exact closure')
    expected=dict(provenance,execution_pins_sha256_alpha=pins['base_pins_sha256_alpha'])
    for name,key in (('identity.json','identity'),('metrics.json','metrics'),('raw.npz.ap','raw'),('verification.json','verification'),('parent_recomputation.json','parent_recomputation')):
        require(file_digest(Path(root)/H0/name)==h0[key+'_sha256_alpha'],'H0/hash/'+name)
        if not name.endswith('.json'):continue
        receipt=read(Path(root)/H0/name)
        require(receipt.get('complete') is True and receipt.get('smoke') is True and receipt.get('stage')=='H0' and receipt.get('first_failure') is None,'H0/complete spent scope/'+name)
        if key!='verification':require(receipt.get('rows')==40 and receipt.get('steps')==600,'H0/size/'+name)
        if key!='metrics':require(receipt.get('passed') is True,'H0/passed/'+name)
        if key=='parent_recomputation':
            require(receipt.get('source_closure_sha256_alpha')==source_closure(pins) and receipt.get('verification_sha256_alpha')==h0['verification_sha256_alpha'] and receipt.get('raw_sha256_alpha')==h0['raw_sha256_alpha'],'H0/root evidence links')
        else:equal(receipt.get('provenance'),expected,'H0/current base provenance/'+name)
        if key in ('metrics','verification','parent_recomputation'):
            require(receipt.get('clauses')=={} and receipt.get('verdict')=='VALIDITY_ONLY','H0/no efficacy/'+name)
        if key in ('identity','verification'):
            gates=receipt.get('gates',{})
            require(set(gates)=={H.namespace(c,a) for c in H.CONDITIONS for a in H.ARMS} and all(g.get('complete') is True and g.get('passed') is True and g.get('rows')==40 and g.get('steps')==600 for g in gates.values()),'H0/all twenty gates')
        if key=='verification':require(receipt.get('raw_sha256_alpha')==h0['raw_sha256_alpha'],'H0/verifier raw binding')
        if key=='identity':
            require(receipt.get('claim') is None and receipt.get('inference') is None and receipt.get('raw_arrays',{}).get('sha256_alpha')==h0['raw_sha256_alpha'],'H0/claim inference raw')


def claim_pair(pair,stage,config,provenance,output,pins,root=ROOT):
    root=Path(root);key=digest(canonical(list(pair)));path=root/REGISTRY/(key+'.json')
    w,a=pair;roles=dict(world=w,agent=a,inference=config['inference'][stage],world_balance=w+10000,c0_geometry=w+20000,cast=a+20000)
    record={k:provenance[k] for k in ('design_sha256_alpha','seed_config_sha256_alpha','seed_registration_sha256_alpha','runtime_sha256_alpha','schema_sha256_alpha','keysets_sha256_alpha','specification_pins_sha256_alpha','execution_pins_sha256_alpha','source_closure_sha256_alpha','opening_sha256_alpha')}
    record.update(format='h17-run3-claim-v3',date=DATE,complete=False,pair_sha256_alpha=key,stage=stage,
        role_digests={k:digest(canonical(v)) for k,v in roles.items()},H0_sha256_alpha=pins['h0']['verification_sha256_alpha'],
        output_path_sha256_alpha=digest(str(Path(output).resolve()).encode('utf-8')),prerequisite_verification_sha256_alpha=pins['h0']['verification_sha256_alpha'],
        rule='exclusive pair-only claim before any stage generator; failure consumes claim',result=None)
    R.p5(canonical(record),root);path.parent.mkdir(parents=True,exist_ok=True)
    try:write_json(path,record,root,exclusive=True)
    except FileExistsError:raise EvidenceError('claim/registered pair consumed') from None
    except BaseException as exc:
        if path.exists():
            failure=dict(field='claim/exclusive durability failure',index=None,phase='claim',condition=None,arm=None)
            try:emergency_receipt(path,stage,provenance,failure,root)
            except BaseException:pass
        raise EvidenceError('claim/exclusive durability failure',phase='claim') from exc
    return path,record


def metadata(stage,smoke,rows,provenance):
    common=dict(date=DATE,stage=stage,complete=False,smoke=smoke,conditions=list(H.CONDITIONS),rows=rows,steps=600,provenance=provenance,first_failure=None)
    identity=dict(common,format='h17-run3-identity-v3',passed=False,claim=None,records={},gates={},raw_arrays=None,inference=None)
    metrics=dict(common,format='h17-run3-metrics-v3',readings={},clauses={},verdict='INVALID')
    return identity,metrics


def emergency_receipt(claim,stage,provenance,failure,root=ROOT):
    identity,_=metadata(stage,False,400,provenance)
    identity.update(claim=Path(claim).relative_to(Path(root)).as_posix(),first_failure=failure)
    return write_json(Path(claim).with_suffix('.failure.json'),identity,root)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--smoke',action='store_true');parser.add_argument('--stage',choices=('bench','dev','eval'))
    args=parser.parse_args(argv);require(args.smoke != bool(args.stage),'CLI/smoke or stage exactly one')
    stage='H0' if args.smoke else args.stage;out=args.output.resolve();rows=40 if args.smoke else 400
    require(out==(ROOT/(H0 if args.smoke else 'experiments/h17/run3/'+stage)).resolve(),'output/canonical stage path')
    require(not out.exists(),'output/already exists')
    pins,config,prov=preflight(ROOT,args.smoke,args.stage or 'bench')
    receipt,metrics=metadata(stage,args.smoke,rows,prov);store=None;claim=None;claimdata=None;condition=None;arm=None
    if not args.smoke:claim,claimdata=claim_pair(config[stage],stage,config,prov,out,pins)
    try:
        out.mkdir(parents=True);receipt['claim']=None if claim is None else claim.relative_to(ROOT).as_posix();write_json(out/'identity.json',receipt)
        from replay_hold_stage1 import load_runtime
        m,unused,unusedattrs,unusedverifier=load_runtime();pair=m.seeds_of('h29',True) if args.smoke else config[stage]
        keysets=read(ROOT/KEYSETS);store=H.Archive(out/'raw.npz.ap',keysets,rows,args.smoke)
        names=read(ROOT/'experiments/module/identity.json')['A1']['L2']['names'];allends={}
        for condition in H.CONDITIONS:
            runs={};receipt['records'][condition]={};metrics['readings'][condition]={};allends[condition]={}
            # Direct Passive transcript exists before disabled GSOff same-state replay.
            for arm in ('Passive','Fly','Agent17','GSOff','GS250'):
                runs[arm]=H.run_arm(m,condition,arm,pair,rows,600,store,runs.get('Passive'))
            gate,scores=H.compare_disabled(m,condition,runs,names)
            H.never_engaged_states(runs['GS250'],runs['Fly'],store,condition)
            if args.smoke:
                plain=H.run_arm(m,condition,'GS250',pair,rows,600,store,plain=True)
                runs['GS250']['record']['base_act_proof']['plain_logger_H0']=H.plain_proof(runs['GS250'],plain,store);del plain
            for arm in H.ARMS:
                reading,ends=H.save_run(store,condition,arm,runs[arm],scores[arm]);allends[condition][arm]=ends
                metrics['readings'][condition][arm]=reading;receipt['records'][condition][arm]=runs[arm]['record']
                receipt['gates'][H.namespace(condition,arm)]=dict(complete=True,passed=True,rows=rows,steps=600,identity=gate)
            del runs,scores;gc.collect();write_json(out/'identity.json',receipt)
        require(len(receipt['gates'])==20 and all(x['passed'] for x in receipt['gates'].values()),'all twenty validity gates')
        if args.smoke:metrics['verdict']='VALIDITY_ONLY'
        else:receipt['inference'],metrics['clauses'],metrics['verdict']=H.inference(allends,config['inference'][stage],store)
        _,_,post=preflight(ROOT,args.smoke,args.stage or 'bench');equal(post,prov,'postrun/immutable closure')
        expected={k for k in keysets if not (args.smoke and k.startswith('inference/'))}
        require({k for k in store.arrays if not k.startswith('blob/')}==expected,'archive/exact frozen keyset')
        receipt['raw_arrays']=store.seal(receipt);store=None
        metrics['complete']=True;receipt.update(complete=True,passed=True)
        write_json(out/'metrics.json',metrics);write_json(out/'identity.json',receipt)
        if claim is not None:
            claimdata['complete']=True;claimdata['result']=canonical(dict(complete=True,status=metrics['verdict'],identity_sha256_alpha=file_digest(out/'identity.json'),metrics_sha256_alpha=file_digest(out/'metrics.json'),raw_sha256_alpha=file_digest(out/'raw.npz.ap'))).hex().translate(H.AP)
            write_json(claim,claimdata)
        print('Run3 '+stage+' complete: '+metrics['verdict'],flush=True);return 0
    except BaseException as exc:
        failure=dict(field='execution exception',index=None,phase=None,condition=condition,arm=arm)
        if isinstance(exc,EvidenceError):failure.update(exc.failure)
        receipt.update(complete=False,passed=False,first_failure=failure);metrics.update(complete=False,first_failure=failure,readings={},clauses={},verdict='INVALID')
        if store is not None:
            try:receipt['raw_arrays']=store.finish()
            except BaseException:receipt['raw_arrays']=None
        output_failure=None
        try:
            if not out.exists():out.mkdir(parents=True,exist_ok=True)
            write_json(out/'identity.json',receipt);write_json(out/'metrics.json',metrics)
        except BaseException as failure_exc:output_failure=failure_exc
        finally:
            if claim is not None:
                # Registry sidecar preserves the first failure independently of
                # output-directory and terminal-claim write failures.
                try:emergency_receipt(claim,stage,prov,failure,ROOT)
                except BaseException as sidecar_exc:
                    if output_failure is not None:raise sidecar_exc from output_failure
                claimdata['result']=canonical(dict(complete=False,status='INVALID',first_failure=failure)).hex().translate(H.AP)
                try:write_json(claim,claimdata)
                except BaseException:
                    # The consumed exclusive header and sidecar are retained.
                    if not claim.with_suffix('.failure.json').is_file():raise
            elif output_failure is not None:raise output_failure
        print('Run3 INVALID: '+failure['field'],flush=True);return 1


if __name__=='__main__':raise SystemExit(main())
