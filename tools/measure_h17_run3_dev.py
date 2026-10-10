"""Separately authorized DEV entry; preserves frozen Run 3 MAIN evidence grammar."""
import argparse
import gc
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import measure_h17_run3 as M
from h17_run3_recording import require,equal,digest,canonical,EvidenceError

H=M.H
ROOT=M.ROOT
OPENING='config/h17-run3-dev-opening.json'
PINS='config/h17-run3-dev-pins.json'
PRIOR='experiments/h17/run3/bench'
OUTPUT='experiments/h17/run3/dev'
DECISION='decision:h17-run3-dev-open'
FILES=('tools/measure_h17_run3_dev.py','tests/test_measure_h17_run3_dev.py',
       'tools/recompute_h17_run3_dev.py','tests/test_recompute_h17_run3_dev.py',
       'notes/reviews/2026-10-10-h17-run3-dev-execution-review.md',
       'experiments/h17/h17_run3_dev_implementation_checks.json')
ARTIFACTS={'identity':'identity.json','metrics':'metrics.json','raw':'raw.npz.ap',
           'verification':'verification.json','parent_recomputation':'parent_recomputation.json'}
CLAUSES={'C0_absolute','C0_E','T1_intervention','T1_V','T3_V','T1_L','W1_L','T3_L','W1_D_other'}


def stage_closure(pins):
    return digest(canonical({key:pins[key] for key in
        ('MAIN_pins_sha256_alpha','source_closure_sha256_alpha','files_sha256_alpha')}))


def prior_check(root,pins,main,provenance):
    """Verify byte-bound BENCH, full validity/efficacy and independent root links."""
    root=Path(root);hashes=pins['prior_artifacts_sha256_alpha']
    require(set(hashes)=={key+'_sha256_alpha' for key in ARTIFACTS},'DEV/prior exact artifacts')
    saved={}
    for key,name in ARTIFACTS.items():
        path=root/PRIOR/name
        require(M.file_digest(path)==hashes[key+'_sha256_alpha'],'DEV/prior hash/'+key)
        if key=='raw':continue
        obj=M.read(path);saved[key]=obj
        require(obj.get('complete') is True and obj.get('smoke') is False and obj.get('stage')=='bench'
                and obj.get('first_failure') is None,'DEV/prior complete scope/'+key)
        if key!='metrics':require(obj.get('passed') is True,'DEV/prior validity/'+key)
        if key!='verification':require(obj.get('rows')==400 and obj.get('steps')==600,'DEV/prior size/'+key)
        if key!='parent_recomputation':equal(obj.get('provenance'),provenance,'DEV/prior MAIN provenance/'+key)
        if key in ('identity','verification'):
            gates=obj.get('gates',{})
            require(set(gates)=={H.namespace(c,a) for c in H.CONDITIONS for a in H.ARMS}
                    and all(g.get('complete') is True and g.get('passed') is True and g.get('rows')==400
                            and g.get('steps')==600 for g in gates.values()),'DEV/prior twenty gates/'+key)
        if key in ('metrics','verification','parent_recomputation'):
            require(obj.get('verdict')=='PASS' and set(obj.get('clauses',{}))==CLAUSES
                    and all(c.get('status')=='PASS' for c in obj['clauses'].values()),'DEV/prior nine PASS/'+key)
    raw=hashes['raw_sha256_alpha'];verification=hashes['verification_sha256_alpha']
    require(saved['identity']['raw_arrays']['sha256_alpha']==raw
            and saved['verification']['raw_sha256_alpha']==raw,'DEV/prior raw links')
    parent=saved['parent_recomputation']
    require(parent.get('source_closure_sha256_alpha')==main['source_closure_sha256_alpha']
            and parent.get('verification_sha256_alpha')==verification and parent.get('raw_sha256_alpha')==raw
            and parent.get('rng_created') is False and type(parent.get('draws')) is int and parent['draws']==0,
            'DEV/prior independent root links')
    equal(saved['metrics']['clauses'],saved['verification']['clauses'],'DEV/prior independent clauses')
    # Root recomputation permits tiny arithmetic differences in an interval;
    # its frozen PASS receipt binds the same bytes and all nine decisions.
    for key in CLAUSES:
        a=saved['metrics']['clauses'][key];b=parent['clauses'][key]
        for field in ('status','bar','direction','estimate'):equal(a[field],b[field],'DEV/prior root clause/'+key+'/'+field)
    identity=saved['identity'];config=M.read(root/M.CONFIG);pair=config['bench']
    claimpath=root/M.REGISTRY/(digest(canonical(pair))+'.json')
    require(identity['claim']==claimpath.relative_to(root).as_posix(),'DEV/prior claim path')
    claim=M.read(claimpath);schema=M.read(root/M.SCHEMA)
    require(set(claim)==set(schema['metadata_keysets']['claim']),'DEV/prior claim grammar')
    require(claim['complete'] is True and claim['stage']=='bench' and claim['format']=='h17-run3-claim-v3'
            and claim['pair_sha256_alpha']==digest(canonical(pair)),'DEV/prior durable claim')
    for key in set(provenance)-{'runtime'}:equal(claim[key],provenance[key],'DEV/prior claim provenance/'+key)
    require(claim['H0_sha256_alpha']==main['h0']['verification_sha256_alpha']
            and claim['prerequisite_verification_sha256_alpha']==main['h0']['verification_sha256_alpha']
            and claim['output_path_sha256_alpha']==digest(str((root/PRIOR).resolve()).encode('utf-8')),
            'DEV/prior claim prerequisite')
    roles=M.read(root/M.REGISTRATION)['stages']['bench']
    equal(claim['role_digests'],{k:digest(canonical(v)) for k,v in roles.items()},'DEV/prior claim roles')
    result=canonical(dict(complete=True,status='PASS',identity_sha256_alpha=hashes['identity_sha256_alpha'],
        metrics_sha256_alpha=hashes['metrics_sha256_alpha'],raw_sha256_alpha=raw)).hex().translate(H.AP)
    require(claim['result']==result and claim['rule']=='exclusive pair-only claim before any stage generator; failure consumes claim',
            'DEV/prior terminal claim')


def preflight(root=ROOT):
    root=Path(root)
    # This call is solely the unchanged common BASE/H0/MAIN closure check.
    # No frozen function or global is replaced to open a different stage.
    main,config,provenance=M.preflight(root,False,'bench')
    pins=M.read(root/PINS);gate=M.read(root/OPENING)
    require(set(pins)=={'format','date','complete','decision','stage','MAIN_pins_sha256_alpha',
        'source_closure_sha256_alpha','files_sha256_alpha','stage_closure_sha256_alpha','prior_artifacts_sha256_alpha'},
        'DEV/exact pins grammar')
    require(pins.get('format')=='h17-run3-dev-pins-v1' and pins.get('complete') is True
            and pins.get('decision')==DECISION and pins.get('stage')=='dev','DEV/pins contract')
    require(pins['MAIN_pins_sha256_alpha']==M.file_digest(root/M.PINS)
            and pins['source_closure_sha256_alpha']==main['source_closure_sha256_alpha'],'DEV/unchanged MAIN closure')
    require(set(pins['files_sha256_alpha'])==set(FILES),'DEV/exact new file inventory')
    require(not set(FILES)&set(main['files_sha256_alpha']),'DEV/new files only')
    for name,sha in pins['files_sha256_alpha'].items():
        path=(root/name).resolve()
        require(path.is_relative_to(root.resolve()) and path.is_file(),'DEV/stage path')
        require(M.file_digest(path)==sha,'DEV/stage source/'+name)
    require(pins['stage_closure_sha256_alpha']==stage_closure(pins),'DEV/stage closure')
    require(gate.get('complete') is True and gate.get('opened') is True and gate.get('stage')=='dev'
            and gate.get('decision')==DECISION and type(gate.get('owner_instruction')) is str
            and bool(gate['owner_instruction'].strip()),'DEV/owner opening')
    require(gate['source_closure_sha256_alpha']==main['source_closure_sha256_alpha']
            and gate['stage_pins_sha256_alpha']==M.file_digest(root/PINS)
            and gate['prior_verification_sha256_alpha']==pins['prior_artifacts_sha256_alpha']['verification_sha256_alpha'],
            'DEV/opening evidence links')
    prior_check(root,pins,main,provenance)
    control=dict(stage_pins_sha256_alpha=M.file_digest(root/PINS),opening_sha256_alpha=M.file_digest(root/OPENING),
        stage_closure_sha256_alpha=pins['stage_closure_sha256_alpha'],MAIN_pins_sha256_alpha=pins['MAIN_pins_sha256_alpha'],
        prior_verification_sha256_alpha=pins['prior_artifacts_sha256_alpha']['verification_sha256_alpha'])
    return main,config,provenance,control


def stage_binding(provenance,control,claim,root=ROOT):
    return dict(format='h17-run3-dev-stage-binding-v3',stage='dev',
        source_closure_sha256_alpha=provenance['source_closure_sha256_alpha'],
        **control,claim_path=Path(claim).relative_to(Path(root)).as_posix())


def claim_pair(config,provenance,output,pins,control,root=ROOT):
    root=Path(root);pair=config['dev'];key=digest(canonical(pair));path=root/M.REGISTRY/(key+'.json')
    w,a=pair;roles=dict(world=w,agent=a,inference=config['inference']['dev'],world_balance=w+10000,c0_geometry=w+20000,cast=a+20000)
    record={k:v for k,v in provenance.items() if k!='runtime'}
    gate=M.read(root/OPENING)
    require(M.file_digest(root/OPENING)==control['opening_sha256_alpha']
            and M.file_digest(root/PINS)==control['stage_pins_sha256_alpha'],'DEV/preclaim control unchanged')
    record.update(format='h17-run3-claim-v3',date=M.DATE,complete=False,pair_sha256_alpha=key,stage='dev',
        role_digests={k:digest(canonical(v)) for k,v in roles.items()},H0_sha256_alpha=pins['h0']['verification_sha256_alpha'],
        output_path_sha256_alpha=digest(str(Path(output).resolve()).encode('utf-8')),
        prerequisite_verification_sha256_alpha=gate['prior_verification_sha256_alpha'],
        rule='exclusive pair-only claim before any stage generator; failure consumes claim',result=None)
    M.R.p5(canonical(record),root);path.parent.mkdir(parents=True,exist_ok=True)
    try:M.write_json(path,record,root,exclusive=True)
    except FileExistsError:raise EvidenceError('claim/registered pair consumed') from None
    except BaseException as exc:
        if path.exists():
            failure=dict(field='claim/exclusive durability failure',index=None,phase='claim',condition=None,arm=None)
            try:M.emergency_receipt(path,'dev',provenance,failure,root)
            except BaseException:pass
        raise EvidenceError('claim/exclusive durability failure',phase='claim') from exc
    return path,record


def collect(out,receipt,metrics,config):
    """Frozen MAIN loop, called only after a successful durable DEV claim."""
    from replay_hold_stage1 import load_runtime
    m,unused,unusedattrs,unusedverifier=load_runtime()
    keysets=M.read(ROOT/M.KEYSETS);store=H.Archive(out/'raw.npz.ap',keysets,400,False)
    names=M.read(ROOT/'experiments/module/identity.json')['A1']['L2']['names'];allends={}
    try:
        for condition in H.CONDITIONS:
            runs={};receipt['records'][condition]={};metrics['readings'][condition]={};allends[condition]={}
            for arm in ('Passive','Fly','Agent17','GSOff','GS250'):
                runs[arm]=H.run_arm(m,condition,arm,config['dev'],400,600,store,runs.get('Passive'))
            gate,scores=H.compare_disabled(m,condition,runs,names)
            H.never_engaged_states(runs['GS250'],runs['Fly'],store,condition)
            for arm in H.ARMS:
                reading,ends=H.save_run(store,condition,arm,runs[arm],scores[arm]);allends[condition][arm]=ends
                metrics['readings'][condition][arm]=reading;receipt['records'][condition][arm]=runs[arm]['record']
                receipt['gates'][H.namespace(condition,arm)]=dict(complete=True,passed=True,rows=400,steps=600,identity=gate)
            del runs,scores;gc.collect();M.write_json(out/'identity.json',receipt)
        require(len(receipt['gates'])==20 and all(x['passed'] for x in receipt['gates'].values()),'all twenty validity gates')
        receipt['inference'],metrics['clauses'],metrics['verdict']=H.inference(allends,config['inference']['dev'],store)
        require({k for k in store.arrays if not k.startswith('blob/')}==set(keysets),'archive/exact frozen keyset')
        return store
    except BaseException as exc:
        # The caller persists failure and preserves the consumed claim.
        try:receipt['raw_arrays']=store.finish()
        except BaseException:receipt['raw_arrays']=None
        if isinstance(exc,EvidenceError):
            if exc.failure.get('condition') is None:exc.failure['condition']=locals().get('condition')
            if exc.failure.get('arm') is None:exc.failure['arm']=locals().get('arm')
        raise


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args(argv);out=args.output.resolve()
    require(out==(ROOT/OUTPUT).resolve(),'output/canonical DEV path');require(not out.exists(),'output/already exists')
    pins,config,prov,control=preflight(ROOT)
    receipt,metrics=M.metadata('dev',False,400,prov);store=None
    claim,claimdata=claim_pair(config,prov,out,pins,control,ROOT)
    try:
        claim_header_sha256_alpha=M.file_digest(claim)
        equal(M.read(claim),claimdata,'claim/initial durable header',phase='claim')
        out.mkdir(parents=True);receipt['claim']=claim.relative_to(ROOT).as_posix();M.write_json(out/'identity.json',receipt)
        binding=stage_binding(prov,control,claim,ROOT)
        M.write_json(out/'stage_binding.json',binding,ROOT,exclusive=True)
        store=collect(out,receipt,metrics,config)
        postpins,postconfig,postprov,postcontrol=preflight(ROOT)
        equal(postprov,prov,'postrun/immutable MAIN closure');equal(postconfig,config,'postrun/registered roles')
        equal(postcontrol,control,'postrun/DEV operation closure')
        equal(M.read(out/'stage_binding.json'),stage_binding(postprov,postcontrol,claim,ROOT),'postrun/DEV saved binding')
        receipt['raw_arrays']=store.seal(receipt);store=None
        metrics['complete']=True;receipt.update(complete=True,passed=True)
        M.write_json(out/'metrics.json',metrics);M.write_json(out/'identity.json',receipt)
        require(M.file_digest(claim)==claim_header_sha256_alpha,'claim/exclusive header changed',phase='claim')
        equal(M.read(claim),claimdata,'claim/exclusive header changed',phase='claim')
        claimdata['complete']=True
        claimdata['result']=canonical(dict(complete=True,status=metrics['verdict'],identity_sha256_alpha=M.file_digest(out/'identity.json'),
            metrics_sha256_alpha=M.file_digest(out/'metrics.json'),raw_sha256_alpha=M.file_digest(out/'raw.npz.ap'))).hex().translate(H.AP)
        M.write_json(claim,claimdata)
        print('Run3 dev complete: '+metrics['verdict'],flush=True);return 0
    except BaseException as exc:
        failure=dict(field='execution exception',index=None,phase=None,condition=None,arm=None)
        if isinstance(exc,EvidenceError):failure.update(exc.failure)
        receipt.update(complete=False,passed=False,claim=claim.relative_to(ROOT).as_posix(),first_failure=failure)
        metrics.update(complete=False,first_failure=failure,readings={},clauses={},verdict='INVALID')
        if store is not None:
            try:receipt['raw_arrays']=store.finish()
            except BaseException:receipt['raw_arrays']=None
        output_failure=None
        try:
            out.mkdir(parents=True,exist_ok=True);M.write_json(out/'identity.json',receipt);M.write_json(out/'metrics.json',metrics)
        except BaseException as fault:output_failure=fault
        finally:
            try:M.emergency_receipt(claim,'dev',prov,failure,ROOT)
            except BaseException as fault:
                if output_failure is not None:raise fault from output_failure
            claimdata['complete']=False
            claimdata['result']=canonical(dict(complete=False,status='INVALID',first_failure=failure)).hex().translate(H.AP)
            try:M.write_json(claim,claimdata)
            except BaseException:
                if not claim.with_suffix('.failure.json').is_file():raise
        print('Run3 dev INVALID: '+failure['field'],flush=True);return 1


if __name__=='__main__':raise SystemExit(main())
