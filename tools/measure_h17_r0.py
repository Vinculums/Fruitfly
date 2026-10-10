#!/usr/bin/env python3
"""Registered R0 passive measurement. Root runs spent H0 before one main claim.

No generator is created on import. Original controllers and worlds are untouched
on disk. The Passive logger shares its original BitGenerator; literal Fly and
Agent17 primitive logs are reconstructed only after all identity gates pass.
"""
import os
THREADS=('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS')
for _key in THREADS:os.environ[_key]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
for _key in ('PH30_PROCS','PH32_PROCS','PH33_PROCS'):os.environ[_key]='1'
import argparse
from contextlib import contextmanager
import gc
import hashlib
import importlib
import json
from pathlib import Path
import platform
import struct
import sys
import time
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from h17_r0_recording import (AP,ARMS,CONDITIONS,SAMPLE_FIELDS,Archive,GeneratorTap,MISSING,
    EvidenceError,canonical,digest,equal,require,walk,original_blob,n2_masks,readings)

ROOT=Path(__file__).resolve().parents[1]
DESIGN='experiments/h17/h17_r0_design_v2.md'
CONFIG='config/h17-r0-seeds.json'
REGISTRATION='experiments/h17/h17_r0_seed_registration.json'
OPENING='config/h17-r0-execution-opening.json'
PINS='config/h17-r0-execution-pins.json'
H0='experiments/h17/r0_smoke'
REGISTRY='experiments/h17/r0_registry'
REVIEW='notes/reviews/2026-10-09-h17-r0-execution-review.md'


def unique(pairs):
    out={}
    for key,value in pairs:require(key not in out,'duplicate JSON key');out[key]=value
    return out


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'),object_pairs_hook=unique,
                      parse_constant=lambda value: (_ for _ in ()).throw(EvidenceError('nonfinite JSON')))


def file_digest(path):
    hasher=hashlib.sha256()
    with Path(path).open('rb') as stream:
        while chunk:=stream.read(1<<20):hasher.update(chunk)
    return hasher.hexdigest().translate(AP)


def runtime_stamp():
    """Stable runtime closure, deliberately excluding clocks and process IDs."""
    libraries={name:dict(path=str(Path(importlib.import_module(name).__file__).resolve()),
        sha256_alpha=file_digest(importlib.import_module(name).__file__))
        for name in ('numpy._core._multiarray_umath','numpy.random._generator')}
    return dict(python=platform.python_version(),numpy=np.__version__,implementation=platform.python_implementation(),
        executable=str(Path(sys.executable).resolve()),executable_sha256_alpha=file_digest(sys.executable),
        numpy_path=str(Path(np.__file__).resolve()),numpy_init_sha256_alpha=file_digest(np.__file__),
        platform=platform.platform(),machine=platform.machine(),pointer_bits=struct.calcsize('P')*8,
        byteorder=sys.byteorder,threads={name:os.environ.get(name) for name in THREADS},processes=1,
        optimize=sys.flags.optimize,assertions_enabled=__debug__,native_libraries=libraries,
        numpy_config_sha256_alpha=digest(canonical(np.__config__.show(mode='dicts'))))


def schema_contract():
    names=read(ROOT/'experiments/module/identity.json')['A1']['L2']['names']
    fieldsets={'Fly':sorted(names['common']+names['cand_only']),
               'Passive':sorted(names['common']+names['cand_only']),
               'Agent17':sorted(names['common']+names['ref_only'])}
    worldbase='R rng p_hit p_wind src good pos head arena walls t rot bumped start p_d cell side plus_y plume'.split()
    worldsets={c:sorted(worldbase+(['pres','absent','raw'] if c=='W1' else [])) for c in CONDITIONS}
    vectors={'PRE_POS':2,'S_pre':2,'S_post':2,'UP_pre':2,'UP_post':2,'Y':2,'C_pre':2,'C_post':2,
             'PRES_pre':2,'PRES_post':2,'POS':2,'AT2':2,'W_raw':2,'W_delivered':2,'source_uniforms':2,'probabilities':2}
    bools=set(('PRES_pre PRES_post NAV TO EV base sustain negS negZ newz zreset withheld_N1_S withheld_N1_Z C AT2 W_raw W_delivered wind_on').split())
    sample_schema={key:dict(dtype='|b1' if key in bools else '<i8' if key in ('H_pre','H_post') else '<f8',
                           shape=['T','R']+([vectors[key]] if key in vectors else [])) for key in SAMPLE_FIELDS}
    output={key:dict(dtype=dtype,shape=shape) for keys,dtype,shape in (
        ('H','|i1',['T','R']),('W P2','|b1',['T','R',2]),
        ('PA NAV TO EV SUS Z C AT2 PRES NAV6 NAV8 DIFF DIFF8','|b1',['T','R']),
        ('SIL SINCE','<f4',['T','R']),('C2','<f4',['T','R',2]),('TGT SG HEAD','<f8',['T','R']),
        ('S POS','<f8',['T','R',2]),('src','<f8',['R',2,2]),('start s0 dwell','<f8',['R',2]),
        ('good cell plus_y H0','<i8',['R']),('first','<i8',['R',2]),('cast contacts','<f8',['R'])) for key in keys.split()}
    output['AT2']=dict(dtype='|b1',shape=['T','R',2])
    construction={key:dict(dtype=dtype,shape=shape) for keys,dtype,shape in (
        ('src','<f8',['R',2,2]),('good cell plus_y','<i8',['R']),
        ('known ordinary_start start S0 UP0 C0','<f8',['R',2]),
        ('ordinary_head ordinary_rot cast_sign flee_side head0 rot0 SG0 SIL0 SINCE0','<f8',['R'])) for key in keys.split()}
    construction.update(ring0=dict(dtype='<f8',shape=['R',16]),codes0=dict(dtype='<f8',shape=['R',2,200]))
    obs={key:dict(dtype=dtype,shape=shape) for keys,dtype,shape in (
        ('q_obs last_whiff last_nav','<i8',['T','R']),('marker_mask','|b1',['T','R']),
        ('marker_step longest_silence first_whiff first_reach post_first_whiff post_first_reach available whiff_delay reach_delay','<i8',['R']),
        ('post_whiff_bits post_reach_bits first_whiff_bits first_reach_bits marker_reach_bits','|u1',['R']),
        ('whiff_event reach_event whiff_censored reach_censored lost_last200','|b1',['R'])) for key in keys.split()}
    for k in (100,200,300):
        for name in ('full','censored','whiff','reach'):obs[name+'_'+str(k)]=dict(dtype='|b1',shape=['R'])
        for source in (0,1):
            for name in ('whiff','reach'):obs[name+'_'+str(k)+'_source'+str(source)]=dict(dtype='|b1',shape=['R'])
    for source in (0,1):
        for span in ('full','last200'):obs['dwell_'+span+'_source'+str(source)]=dict(dtype='<i8',shape=['R'])
    masknames=('hit new negS negZ TO EV base sustain newz zreset withheld_N1_S withheld_N1_Z SIL_base SIL_post reset_drive units '
        'negative_to_unheld negative_zero_units negative_multiple_units negative_identity_change negative_end negative_same neither timeout_only evidence_only both').split()
    masks={key:dict(dtype='<f8' if key in ('SIL_base','SIL_post','reset_drive') else '<i8' if key=='units' else '|b1',shape=['T','R']) for key in masknames}
    w1={key:dict(dtype=dtype,shape=['R']) for keys,dtype in (
        ('reach lost nonav heldB_end','|b1'),
        ('first dwell whiffs fw nav contacts formed released end_to end_ev end_both end_none fh cone f5 ent5','<i8'),
        ('heldB nothing da_min da_end dc_end dmin','<f8')) for key in keys.split()}
    arrays={}
    for condition in CONDITIONS:
        for arm in ARMS:
            prefix=condition+'/'+arm
            for group,values in (('output',output),('sample',sample_schema),('construction',construction),('reading',obs),('mask',masks)):
                for key,value in values.items():arrays[prefix+'/'+group+'/'+key]=value.copy()
            if condition=='C0':
                for key in ('C0sign','C0k','C0da','C0dc'):
                    arrays[prefix+'/construction/'+key]=dict(dtype='<i8' if key=='C0k' else '<f8',shape=['R'])
            for name,width in (('state_timeline',len(fieldsets[arm])),('attribute_hashes',len(fieldsets[arm])),('world_timeline',len(worldsets[condition]))):
                arrays[prefix+'/'+name]=dict(dtype='|S64',shape=['E',width])
            arrays[prefix+'/rng_timeline']=dict(dtype='|S64',shape=['G',8 if condition=='W1' else 7 if condition=='C0' else 6])
            for name in ('input_timeline','return_timeline'):arrays[prefix+'/'+name]=dict(dtype='|S64',shape=['T'])
            if condition=='W1':
                for name in ('twin_input_timeline','twin_return_timeline'):arrays[prefix+'/'+name]=dict(dtype='|S64',shape=['T'])
                for name,dtype,shape in (('PRE_POS','<f8',['T','R',2]),('PRE_HEAD','<f8',['T','R']),
                    ('T','<i8',['T','R']),('RAW','|b1',['T','R',2]),('WIND','|b1',['T','R']),('WALLS','|b1',['T','R'])):
                    arrays[prefix+'/twin/'+name]=dict(dtype=dtype,shape=shape)
            arrays[prefix+'/anchor/anchor_valid']=dict(dtype='|b1',shape=['R'])
            for name in ('q_obs','last_whiff','last_nav'):arrays[prefix+'/anchor/'+name]=dict(dtype='<i8',shape=['R'])
            for key,value in sample_schema.items():arrays[prefix+'/anchor/'+key]=dict(dtype=value['dtype'],shape=value['shape'][1:])
            for key,value in {'dwell':dict(dtype='<f8',shape=['R',2]),'first':dict(dtype='<i8',shape=['R',2]),
                    'contacts':dict(dtype='<f8',shape=['R']),'cls3':dict(dtype='<i8',shape=['R'])}.items():arrays[prefix+'/L3/'+key]=value
            if condition=='W1':
                for key,value in w1.items():arrays[prefix+'/L3/w1sum/'+key]=value
                for k in range(100,601,100):arrays[prefix+'/L3/w1sum/cum/'+str(k)]=dict(dtype='|b1',shape=['R'])
    return dict(version='h17-r0-evidence-v2',conditions=list(CONDITIONS),arms=list(ARMS),main_rows=400,steps=600,
        smoke_rows=40,sample_fields=list(SAMPLE_FIELDS),sample_rule='bool masks; indices int64; geometry/clocks float64; original outputs retain native dtype',
        arrays=arrays,fieldsets=fieldsets,world_fieldsets=worldsets,dtype_kinds='biufUS',shape_dimensions=dict(T=600,R='40 smoke / 400 main',E=2401,G=4201),
        choices_semantics={
            'nav_sourceK':'NAV and delivered whiff source K concurrence; no reset-cause attribution',
            'held_nav_sourceK':'NAV and held source K concurrence; no reset-cause attribution'},
        raw_encoding='NPZ compressed; hex nibble a-p maps to 0-f',array_manifest=['dtype','shape','nbytes','sha256_alpha'],
        blob_template='blob/<AP content address>; ndarray native or uint8 canonical recursively typed JSON',
        blob_id='sha256(AP) of canonical descriptor followed by payload bytes',
        state_events=['construction','pre','base','act','bump'],rng_phases=['construction','before','sense','wind','twin','act','move','bump'],
        snapshot_exclusions=['act','bump'],missing_hash='sha256(AP) of byte M',
        lineage_fieldsets='experiments/module/identity.json A1.L2.names unchanged',
        primitive_log='Passive original BitGenerator handle; literal paired reconstruction after exact identity gates',
        primitive_log_boundary='outer source API invocation only; native nested dispatch delegates once without a transcript entry',
        raw_templates=['<condition>/<arm>/output/<original ndarray>','<condition>/<arm>/sample/<sample field>',
            '<condition>/<arm>/construction/<construction ndarray>','<condition>/<arm>/reading/<observation>',
            '<condition>/<arm>/mask/<N2 mask>','<condition>/<arm>/anchor/<field>',
            '<condition>/<arm>/state_timeline','<condition>/<arm>/attribute_hashes','<condition>/<arm>/world_timeline',
            '<condition>/<arm>/rng_timeline','<condition>/<arm>/input_timeline','<condition>/<arm>/return_timeline',
            'W1/<arm>/twin_input_timeline','W1/<arm>/twin_return_timeline',
            'W1/<arm>/twin/<PRE_POS,PRE_HEAD,T,RAW,WIND,WALLS>',
            '<condition>/<arm>/L3/<native score array>'])


def required_pin_files(root=ROOT):
    root=Path(root)
    paths={path.relative_to(root).as_posix() for path in (root/'src').glob('*.py')}
    paths.update((DESIGN,CONFIG,REGISTRATION,OPENING,REVIEW,
        'tools/measure_h17_r0.py','tools/h17_r0_recording.py','tools/verify_h17_r0.py',
        'tests/test_h17_r0.py','tests/test_verify_h17_r0.py','tools/replay_hold_stage1.py',
        'tools/verify_seed_scan_r2.py','config/seed-scan-exceptions-r2.json',
        'experiments/module/identity.json'))
    return sorted(paths)


def source_closure(pins):
    return digest(canonical({key:pins[key] for key in ('runtime','schema','files_sha256_alpha')}))


def preflight(root=ROOT,smoke=False):
    root=Path(root);pins=read(root/PINS)
    require(pins.get('complete') is True and pins.get('decision')=='decision:h17-r0-open','pins/opening')
    require(pins.get('schema')==schema_contract(),'pins/schema')
    require(pins.get('runtime')==runtime_stamp(),'pins/runtime')
    stamp=pins['runtime']
    require(stamp['python']=='3.13.12' and stamp['numpy']=='2.5.3' and stamp['pointer_bits']==64 and
            stamp['byteorder']=='little' and stamp['implementation']=='CPython' and stamp['optimize']==0 and
            stamp['assertions_enabled'] and all(x=='1' for x in stamp['threads'].values()),'runtime/registered')
    require(set(pins['files_sha256_alpha'])==set(required_pin_files(root)),'pins/complete source closure')
    require(pins.get('source_closure_sha256_alpha')==source_closure(pins),'pins/closure digest')
    for name,want in pins['files_sha256_alpha'].items():
        path=(root/name).resolve();require(path.is_relative_to(root.resolve()) and path.is_file(),'pins/path/'+name)
        require(digest(path.read_bytes())==want,'pins/source/'+name)
    opening=read(root/OPENING)
    require(opening.get('complete') is True and opening.get('execution_opened') is True and
        opening.get('decision')=='decision:h17-r0-open' and opening.get('design')==DESIGN and
        opening.get('seed_config')==CONFIG and opening.get('seed_registration')==REGISTRATION and
        opening.get('design_sha256_alpha')==digest((root/DESIGN).read_bytes()) and
        opening.get('seed_config_sha256_alpha')==digest((root/CONFIG).read_bytes()) and
        opening.get('seed_registration_sha256_alpha')==digest((root/REGISTRATION).read_bytes()) and
        opening.get('conditions')==list(CONDITIONS) and opening.get('rows')==400 and opening.get('steps')==600 and
        opening.get('main_claims_allowed')==1 and opening.get('candidate_selected') is False and
        opening.get('relaxation_signed') is False and opening.get('adoption')=='none','opening/contract')
    config=read(root/CONFIG);pair=config.get('measurement')
    require(isinstance(pair,list) and len(pair)==2 and all(type(n) is int and n>=0 for n in pair) and pair[0]!=pair[1],'config/pair')
    w,a=pair;nums=[w,a,w+10000,w+20000,a+20000];reg=read(root/REGISTRATION)
    local,graph=reg.get('local_scan',{}),reg.get('graph_scan',{})
    require(reg.get('complete') is True and reg.get('config')==CONFIG and reg.get('config_key')=='measurement' and
            reg.get('numbers')==nums and local.get('numbers')==nums,'registration/pair')
    require(local.get('passed') is True and local.get('hits')==[] and local.get('errors')==[] and
            local.get('prior_hold_roles_disjoint') is True and local.get('exclusions')==['.git','__pycache__'],'registration/local')
    queries=graph.get('queries',[])
    require(graph.get('passed') is True and [q.get('number') for q in queries]==nums and
        all(q.get('executed') is True and q.get('error') is None and q.get('literal_hit') is False and q.get('keyword_rows')==0 for q in queries),'registration/graph')
    require(reg.get('fresh_generators_created')==0 and reg.get('fresh_random_draws')==0 and reg.get('simulation_performed') is False and
            reg.get('protected_seed_exceptions_added') is False,'registration/no previous run')
    prov=dict(runtime=stamp,source_closure_sha256_alpha=source_closure(pins),
              design_sha256_alpha=digest((root/DESIGN).read_bytes()),config_sha256_alpha=digest((root/CONFIG).read_bytes()),
              registration_sha256_alpha=digest((root/REGISTRATION).read_bytes()),opening_sha256_alpha=digest((root/OPENING).read_bytes()))
    if not smoke:
        prov['execution_pins_sha256_alpha']=digest((root/PINS).read_bytes())
        h0=pins.get('h0',{})
        require(h0.get('source_closure_sha256_alpha')==source_closure(pins),'H0/current closure')
        for name,key in (('identity.json','identity'),('metrics.json','metrics'),('raw.npz.ap','raw'),('verification.json','verification')):
            path=root/H0/name;require(path.is_file() and file_digest(path)==h0.get(key+'_sha256_alpha'),'H0/'+name)
        for name in ('identity.json','metrics.json','verification.json'):
            h=read(root/H0/name);require(h.get('complete') is True and h.get('smoke') is True,'H0/complete/'+name)
            if name!='metrics.json':require(h.get('passed') is True,'H0/passed/'+name)
    return pins,tuple(pair),prov


def p5(data,root=ROOT):
    import verify_seed_scan_r2 as verifier
    sys.path.insert(0,str(Path(root)/'src'))
    for name in ('ph33','ph35'):
        checker=importlib.import_module(name)
        require(Path(checker.__file__).resolve()==(Path(root)/'src'/(name+'.py')).resolve(),'P5/checker source')
        require(not any(verifier.count_number(data,n) for n in checker.seed_numbers()),'P5/protected digits')


def write_json(path,obj,root=ROOT,exclusive=False):
    data=canonical(obj)+b'\n';p5(data,root);path=Path(path)
    if exclusive:
        with path.open('xb') as stream:stream.write(data);stream.flush();os.fsync(stream.fileno())
    else:
        temp=path.with_suffix(path.suffix+'.tmp')
        with temp.open('wb') as stream:stream.write(data);stream.flush();os.fsync(stream.fileno())
        temp.replace(path)
    return digest(data)


def claim_pair(pair,provenance,output,root=ROOT):
    """Pair-only exclusive claim, independent of output path and design label."""
    root=Path(root);key=digest(canonical(list(pair)));directory=root/REGISTRY;directory.mkdir(parents=True,exist_ok=True)
    path=directory/(key+'.json')
    obj=dict(complete=False,pair_sha256_alpha=key,provenance_sha256_alpha=digest(canonical(provenance)),
             source_closure_sha256_alpha=provenance['source_closure_sha256_alpha'],
             execution_pins_sha256_alpha=provenance['execution_pins_sha256_alpha'],
             output_path_sha256_alpha=digest(str(Path(output).resolve()).encode('utf-8')),
             decision='decision:h17-r0-open',design_sha256_alpha=provenance.get('design_sha256_alpha'),
             claim_rule='one registered pair, durable before first generator')
    try:write_json(path,obj,root,exclusive=True)
    except FileExistsError:raise EvidenceError('claim/registered pair already consumed') from None
    return path,obj


class Tracker:
    def __init__(self,store,condition,arm):
        self.store,self.condition,self.arm=store,condition,arm
        self.roles=['world','balance']
        if condition=='W1':self.roles+=['twin','twin_balance']
        self.roles+=['agent','code0','code1','cast']
        if condition=='C0':self.roles+=['geometry']
        self.instances=[];self.generators=[];self.draws=[];self.last_calls={};self.step=-1;self.phase='construction'
        self.labels=[];self.timeline=[];self.original=np.random.default_rng

    def factory(self,*args,**kwargs):
        index=len(self.instances);context=dict(condition=self.condition,arm=self.arm,step=self.step,phase=self.phase)
        require(index<len(self.roles),'rng/unregistered creation',phase=context)
        role=self.roles[index]
        try:
            original=self.original(*args,**kwargs)
            require(type(original) is np.random.Generator,'rng/literal factory type')
            handle=GeneratorTap(original,self,index) if self.arm=='Passive' else original
            self.instances.append(dict(index=index,role=role,seed_args=self.store.put(args),seed_kwargs=self.store.put(kwargs),
                initial=self.store.put(original),state_type=type(original.bit_generator).__name__,handle_type=type(handle).__name__))
            self.generators.append(handle);return handle
        except BaseException as exc:raise EvidenceError('rng/creation/'+role,None,context) from exc

    def checkpoint(self,phase):
        self.phase=phase;self.labels.append(dict(step=self.step,phase=phase))
        self.timeline.append([self.store.put(rng) for rng in self.generators])

    @contextmanager
    def intercept(self):
        previous=np.random.default_rng;np.random.default_rng=self.factory
        try:yield
        finally:np.random.default_rng=previous


def lineage_base_class(runtime):
    """Resolve the unchanged base through module_identity's exported harness."""
    return runtime.ph24.ph23.Agent9


class Tape:
    def __init__(self,store,condition=None,arm=None):
        self.store=store;self.events=[];self.states=[];self.hashes=[];self.worlds=[];self.inputs=[];self.returns=[]
        self.sil_base=None;self.y=None;self.base_calls=0;self.circuit_calls=0
        self.condition,self.arm=condition,arm

    def snap(self,a,w,phase,step):
        state=walk(a);world=vars(w)
        self.events.append(dict(step=step,phase=phase))
        context=dict(condition=self.condition,arm=self.arm,step=step,phase=phase)
        def capture(values,group,hashing=False):
            captured={}
            for key,value in values.items():
                try:captured[key]=digest(original_blob(value)) if hashing else self.store.put(value)
                except BaseException as exc:raise EvidenceError('snapshot/'+group+'/'+key,None,context) from exc
            return captured
        self.states.append(capture(state,'agent'))
        self.hashes.append(capture(state,'attribute_hash',True))
        self.worlds.append(capture(world,'world'))

    @contextmanager
    def base_tap(self,m,a,w,tracker):
        target,method=(lineage_base_class(m),'act') if isinstance(a,m.ph35.Agent17) else (m.fly.Fly,'_act')
        original=getattr(target,method);seltype=type(a.sel);circuit=seltype.step
        def call(instance,*args,**kwargs):
            result=original(instance,*args,**kwargs)
            if instance is a:
                self.base_calls+=1;self.sil_base=a.silence.copy();self.snap(a,w,'base',tracker.step)
            return result
        def selection(instance,y,*args,**kwargs):
            if instance is a.sel:self.circuit_calls+=1;self.y=y.copy()
            return circuit(instance,y,*args,**kwargs)
        setattr(target,method,call);seltype.step=selection
        try:yield
        finally:setattr(target,method,original);seltype.step=circuit

    def arrays(self):
        fields=sorted(set().union(*(x.keys() for x in self.states)))
        world_fields=sorted(set().union(*(x.keys() for x in self.worlds)))
        absent=self.store.put(MISSING);missing=digest(b'M')
        state=np.asarray([[row.get(k,absent) for k in fields] for row in self.states],dtype='S64')
        hashes=np.asarray([[row.get(k,missing) for k in fields] for row in self.hashes],dtype='S64')
        world=np.asarray([[row.get(k,absent) for k in world_fields] for row in self.worlds],dtype='S64')
        return fields,world_fields,state,hashes,world


def plume(pos,src,p_hit):
    from ph9 import W0,SLOPE,LMAX
    from ph11 import LAM
    along=pos[:,None,0]-src[:,:,0];cross=np.abs(pos[:,None,1]-src[:,:,1])
    cone=(along>0)&(along<LMAX)&(cross<W0+SLOPE*along)
    near=np.linalg.norm(pos[:,None,:]-src,axis=2)<3.
    return np.where(cone|near,p_hit*np.exp(-np.maximum(along,0.)/LAM),0.)


def output_record(m,o,t,a,h,x,pa):
    """Original recorder plus Fly's mathematically identical lineage diagnostics."""
    m.ph24.record(o,t,a,h,x,pa)
    if not isinstance(a,lineage_base_class(m)):
        rows=np.arange(a.R);v=a.known;vh=v[rows,np.maximum(h,0)];hit=(h>=0)&x[rows,np.maximum(h,0)]
        nav6=hit|((h<0)&(x&(v>=0)).any(1));vmax=v.max(1);top=(v>=0)&(v==vmax[:,None])
        nav8=np.where((h>=0)&((vh==vmax)|(vh<0)),hit,(x&top).any(1))
        o['NAV6'][t]=nav6;o['NAV8'][t]=nav8;o['DIFF'][t]=a.nav_hit!=nav6;o['DIFF8'][t]=a.nav_hit!=nav8
        o['P2'][t]=a.present;o['C2'][t]=a.c;o['PRES'][t]=a.present[rows,o['good']]


def construct(m,condition,arm,pair,rows,tracker):
    seed_w,seed_a=pair;r=np.arange(rows)
    w=(m.ph24.ph22.Masked if condition=='W1' else m.ph24.World7)(rows,np.random.default_rng(seed_w),seed_w)
    if condition=='W1':w.pres=1-w.good;w.absent=w.good.copy()
    tw=m.ph24.World7(rows,np.random.default_rng(seed_w),seed_w) if condition=='W1' else None
    known=np.zeros((rows,2));known[r,w.good]=0. if condition=='C0' else 1.
    known[r,1-w.good]=-1. if condition=='T3' else 0.
    rng=np.random.default_rng(seed_a)
    a=m.ph35.Agent17(rows,rng,P=60,N_hi=200,G=2.,known=known,rule=True,filt=True,scope='prior',release=True) if arm=='Agent17' else m.fly.Fly(rows,rng,known,nch=2)
    a.cast_sign=m.ph24.cast_draw(seed_a,rows)
    construction={k:np.copy(v) for k,v in dict(src=w.src,good=w.good,cell=w.cell,plus_y=w.plus_y,known=known,
        ordinary_start=w.pos,ordinary_head=w.head,ordinary_rot=w.rot,cast_sign=a.cast_sign,flee_side=a.flee_side,
        S0=a.sel.s,SG0=a.sel.S[:,0],UP0=a.up.P,SIL0=a.silence,SINCE0=a.since,C0=a.c,ring0=a.ring.s,codes0=a.codes).items()}
    if condition=='C0':
        geom=np.random.default_rng(seed_w+20000);outward=np.empty(rows,float)
        for cell in range(4):
            ix=np.flatnonzero(w.cell==cell);require(len(ix)%2==0,'construction/C0 even cell')
            order=geom.permutation(ix);outward[order]=np.where(np.arange(len(ix))%2==0,1.,-1.)
        da=geom.uniform(5.,14.,rows);dc=geom.uniform(26.,31.,rows)
        k=np.where(outward>0,w.plus_y,1-w.plus_y)
        w.pos=np.stack([w.src[r,k,0]+da,w.src[r,k,1]+outward*dc],1)
        construction.update(C0sign=outward,C0k=k,C0da=da,C0dc=dc)
        require(not plume(w.pos,w.src,w.p_hit).any(),'construction/C0 zero effective plume')
    w.walls=False
    if tw is not None:tw.walls=False
    construction.update(start=w.pos.copy(),head0=w.head.copy(),rot0=w.rot.copy())
    require(len(tracker.generators)==len(tracker.roles),'rng/complete creation')
    require(all(np.count_nonzero(w.cell==cell)==rows//4 for cell in range(4)),'construction/cells')
    require(not a.sel.s.any() and not a.silence.any() and not a.since.any() and (a.c==140.).all() and a.present.all(),'construction/controller defaults')
    return w,tw,a,construction


def run_arm(m,condition,arm,pair,rows,steps,store):
    print('R0 '+condition+' '+arm+': construction and original trajectory',flush=True)
    tracker=Tracker(store,condition,arm);tape=Tape(store,condition,arm)
    with tracker.intercept():w,tw,a,construction=construct(m,condition,arm,pair,rows,tracker)
    tracker.checkpoint('construction');tape.snap(a,w,'construction',-1)
    o=dict(world=condition,arm=type(a).__name__,good=w.good.copy(),cell=w.cell.copy(),plus_y=w.plus_y.copy(),src=w.src.copy(),G=a.G,
        fixed=False,steps=steps,cast=a.cast_sign.copy(),start=w.pos.copy(),s0=a.sel.s.copy(),H0=a.held(),draws_equal=True,rng_equal=True,
        POS=np.zeros((steps,rows,2)),HEAD=np.zeros((steps,rows)),AT2=np.zeros((steps,rows,2),bool),C=np.zeros((steps,rows),bool),**m.ph24.blank(steps,rows))
    sample={};rr=np.arange(rows);twin_inputs=[];twin_returns=[]
    twin={name:np.empty(shape,dtype=dtype) for name,dtype,shape in (
        ('PRE_POS',np.float64,(steps,rows,2)),('PRE_HEAD',np.float64,(steps,rows)),('T',np.int64,(steps,rows)),
        ('RAW',bool,(steps,rows,2)),('WIND',bool,(steps,rows)),('WALLS',bool,(steps,rows)))} if tw is not None else {}
    def put(name,t,value):
        v=np.asarray(value)
        if name not in sample:
            dtype=bool if v.dtype.kind=='b' else np.int64 if name in ('H_pre','H_post') else np.float64
            sample[name]=np.empty((steps,)+v.shape,dtype=dtype)
        sample[name][t]=v
    with tape.base_tap(m,a,w,tracker):
        for t in range(steps):
            tracker.step=t;tracker.last_calls={};tracker.checkpoint('before');tape.snap(a,w,'pre',t)
            for name,value in dict(PRE_POS=w.pos,PRE_HEAD=w.head,PRE_ROT=w.rot,H_pre=a.held(),S_pre=a.sel.s,
                SG_pre=a.sel.S[:,0],UP_pre=a.up.P,SIL_pre=a.silence,SINCE_pre=a.since,C_pre=a.c,PRES_pre=a.present).items():put(name,t,value)
            if tw is not None:tw.pos,tw.head,tw.t=w.pos.copy(),w.head.copy(),w.t
            probability=plume(w.pos,w.src,w.p_hit);pa=(a.sel.s>1.).any(1)
            tracker.phase='sense';x=w.sense();tracker.checkpoint('sense')
            tracker.phase='wind';on=w.wind_on();tracker.checkpoint('wind')
            if tw is not None:
                twin_inputs.append(store.put((tw.pos.copy(),tw.head.copy(),tw.t)))
                twin['PRE_POS'][t]=tw.pos;twin['PRE_HEAD'][t]=tw.head;twin['T'][t]=tw.t;twin['WALLS'][t]=tw.walls
                tracker.phase='twin';raw=tw.sense();wind=tw.wind_on()
                equal(raw,w.raw,'W1/twin raw',phase=t);equal(wind,on,'W1/twin wind',phase=t)
                equal(w.rng.bit_generator.state,tw.rng.bit_generator.state,'W1/twin RNG',phase=t)
                equal(x[rr,1-w.good],raw[rr,1-w.good],'W1/delivered other',phase=t)
                require(not x[rr,w.good].any(),'W1/masked delivered',phase=t)
                raw_copy=raw.copy()
                twin_returns.append(store.put((raw,wind)))
                twin['RAW'][t]=raw;twin['WIND'][t]=wind
            else:raw_copy=x.copy()
            tracker.checkpoint('twin')
            tape.inputs.append(store.put((w.pos.copy(),w.head.copy(),w.rot.copy(),w.t,x,on)))
            tracker.phase='act';before_base=tape.base_calls;before_sel=tape.circuit_calls
            turn,h=a.act(w,x,on)
            require(tape.base_calls==before_base+1 and tape.circuit_calls==before_sel+1,'act/exactly one original base/circuit',phase=t)
            tape.returns.append(store.put((turn,h)));tape.snap(a,w,'act',t);tracker.checkpoint('act')
            output_record(m,o,t,a,h,x,pa)
            fields=dict(H_post=h,S_post=a.sel.s,SG_post=a.sel.S[:,0],UP_post=a.up.P,Y=tape.y,SIL_base=tape.sil_base,
                SIL_post=a.silence,SINCE_post=a.since,C_post=a.c,PRES_post=a.present,NAV=a.nav_hit,TO=a.due_timeout,EV=a.due_evidence,
                EST=a.est,TGT=a.tgt,TURN=turn,cast_sign=a.cast_sign,flee_side=a.flee_side,W_raw=raw_copy,W_delivered=x,
                probabilities=probability,wind_on=on)
            for name,value in fields.items():put(name,t,value)
            tracker.phase='move';w.move(turn);tracker.checkpoint('move')
            tracker.phase='bump';a.bump(w.bumped);tape.snap(a,w,'bump',t);tracker.checkpoint('bump')
            o['POS'][t]=w.pos;o['HEAD'][t]=w.head;o['AT2'][t]=w.at_source();o['C'][t]=w.bumped
            for name,value in dict(POS=w.pos,HEAD=w.head,ROT=w.rot,C=w.bumped,AT2=o['AT2'][t]).items():put(name,t,value)
            if arm=='Passive':
                world_calls=tracker.last_calls[tracker.roles.index('world')]
                agent_calls=tracker.last_calls[tracker.roles.index('agent')]
                require([x[0] for x in world_calls]==['random']*3,'rng/world original calls',phase=t)
                require([x[0] for x in agent_calls]==['standard_normal']*4,'rng/agent original calls',phase=t)
                put('source_uniforms',t,np.stack([world_calls[0][1],world_calls[1][1]],1))
                put('wind_uniform',t,world_calls[2][1]);put('turn_normal',t,agent_calls[-1][1])
    o['dwell']=o['AT2'].sum(0).astype(float);o['contacts']=o['C'].sum(0).astype(float)
    o['first']=np.where(o['AT2'].any(0),o['AT2'].argmax(0),-1)
    masks=n2_masks(sample,construction['known'])
    for name in ('base','sustain','negS','negZ','newz','zreset','withheld_N1_S','withheld_N1_Z','reset_drive'):
        sample[name]=masks[name].copy()
    equal(sample['SIL_base'],masks['SIL_base'],'N2/observed base clock')
    equal(sample['SIL_post'],masks['SIL_post'],'N2/observed final clock')
    equal(o['SUS'],sample['sustain'],'N2/actual sustain');equal(o['Z'],sample['zreset'],'N2/actual reset')
    if arm=='Agent17':
        n2s=np.asarray([dictrow.get('n2S') for event,dictrow in zip(tape.events,tape.states) if event['phase']=='act'],dtype='S64')
        # Lineage masks are retained in the typed snapshots; verifier decodes them.
        require(len(n2s)==steps,'N2/full lineage withheld snapshots')
    fields,world_fields,state,hashes,world=tape.arrays()
    record=dict(output_metadata={k:v for k,v in o.items() if not isinstance(v,np.ndarray)},state_fields=fields,world_fields=world_fields,
        events=tape.events,rng_labels=tracker.labels,generator_instances=tracker.instances,draw_log=tracker.draws,
        independent_streams=len(tracker.instances),generator_handles=len(tracker.instances)*(2 if arm=='Passive' else 1),
        literal_generators=arm!='Passive',construction_refs={k:store.put(v) for k,v in construction.items()},
        observation_calls=dict(base=tape.base_calls,circuit=tape.circuit_calls),
        primitive_log_proof=None)
    tables=dict(state_timeline=state,attribute_hashes=hashes,world_timeline=world,
        rng_timeline=np.asarray(tracker.timeline,dtype='S64'),input_timeline=np.asarray(tape.inputs,dtype='S64'),return_timeline=np.asarray(tape.returns,dtype='S64'))
    if condition=='W1':tables.update(twin_input_timeline=np.asarray(twin_inputs,dtype='S64'),twin_return_timeline=np.asarray(twin_returns,dtype='S64'))
    del tape,tracker;gc.collect()
    return dict(output=o,sample=sample,construction=construction,record=record,tables=tables,twin=twin)


def compare_runs(m,condition,reference,passive,lineage,names):
    equal(reference['output'],passive['output'],condition+'/sameclass/full original output')
    equal(reference['construction'],passive['construction'],condition+'/sameclass/construction')
    equal(reference['twin'],passive['twin'],condition+'/sameclass/twin')
    for table in reference['tables']:
        equal(reference['tables'][table],passive['tables'][table],condition+'/sameclass/'+table)
    equal(reference['record']['state_fields'],passive['record']['state_fields'],condition+'/sameclass/fieldset')
    equal(reference['record']['world_fields'],passive['record']['world_fields'],condition+'/sameclass/worldfieldset')
    for run in (reference,lineage):
        equal(run['record']['rng_labels'],passive['record']['rng_labels'],condition+'/RNG phase labels')
        equal(run['tables']['rng_timeline'],passive['tables']['rng_timeline'],condition+'/all generators all phases')
        for key in ('input_timeline','return_timeline','world_timeline')+ (('twin_input_timeline','twin_return_timeline') if condition=='W1' else ()):
            equal(run['tables'][key],passive['tables'][key],condition+'/coupling/'+key)
        ri=run['record']['generator_instances'];pi=passive['record']['generator_instances']
        require(len(ri)==len(pi),condition+'/generator creation count')
        for i,(r,p) in enumerate(zip(ri,pi)):
            for field in ('index','role','seed_args','seed_kwargs','initial','state_type'):equal(r[field],p[field],condition+'/creation/'+field,phase=i)
        for key,value in run['sample'].items():equal(value,passive['sample'][key],condition+'/sample/'+key)
        equal(run['construction'],passive['construction'],condition+'/construction all arms')
        equal(run['twin'],passive['twin'],condition+'/twin all arms')
    rfields=set(lineage['record']['state_fields']);cfields=set(reference['record']['state_fields'])
    measured=dict(common=sorted(rfields&cfields),ref_only=sorted(rfields-cfields),cand_only=sorted(cfields-rfields))
    equal(measured,names,condition+'/frozen lineage fieldsets')
    for name in names['common']:
        ri=lineage['record']['state_fields'].index(name);ci=reference['record']['state_fields'].index(name)
        # Construction, pre, base, act and bump all included, strengthening historical act/bump gate.
        equal(lineage['tables']['attribute_hashes'][:,ri],reference['tables']['attribute_hashes'][:,ci],condition+'/lineage/'+name)
    for field in m.L1A:equal(lineage['output'][field],reference['output'][field],condition+'/lineage/L1/'+field)
    # All additional original arrays, including measurement fields, are preserved and checked too.
    require(set(lineage['output'])==set(reference['output']),condition+'/lineage original output keyset')
    for field in reference['output']:
        if field!='arm':equal(lineage['output'][field],reference['output'][field],condition+'/lineage/full output/'+field)
    scoreworld='W1' if condition=='W1' else 'T1'
    scores=[m.l3_scores('h29',scoreworld,run['output'],600) for run in (reference,passive,lineage)]
    for i in (1,2):equal(scores[0],scores[i],condition+'/L3/'+str(i))
    proof=dict(source_arm='Passive',basis=['creation','every phase generator state','full inputs/returns','sample fields','original output arrays','sameclass snapshots','frozen lineage common snapshots'],passed=True)
    for run in (reference,lineage):
        for name in ('source_uniforms','wind_uniform','turn_normal'):run['sample'][name]=passive['sample'][name].copy()
        run['record']['primitive_log_proof']=proof.copy()
        run['record']['draw_log_reference']=condition+'/Passive'
    passive['record']['primitive_log_proof']=dict(source_arm='Passive',basis=['original shared BitGenerator direct primitive returns'],passed=True)
    return dict(passed=True,same_class=True,lineage=True,creation=True,generator_phases=True,inputs_and_returns=True,
        full_original_outputs=True,sample=True,L1=list(m.L1A),L2_names=names,L3=True),scores


def save_tree_arrays(store,prefix,tree):
    if isinstance(tree,dict):return {str(k):save_tree_arrays(store,prefix+'/'+str(k),v) for k,v in tree.items()}
    if isinstance(tree,np.ndarray):store.array(prefix,tree);return dict(array=prefix)
    return tree.item() if isinstance(tree,np.generic) else tree


def save_run(store,condition,arm,run,score):
    prefix=condition+'/'+arm;sample=run['sample'];require(set(sample)==set(SAMPLE_FIELDS),prefix+'/mandatory sample keyset')
    for group in ('output','sample','construction','twin'):
        for key,value in run[group].items():
            if isinstance(value,np.ndarray):store.array(prefix+'/'+group+'/'+key,value)
    for key,value in run['tables'].items():store.array(prefix+'/'+key,value)
    obs,masks,metrics=readings(condition,sample,run['construction'])
    for key,value in obs.items():store.array(prefix+'/reading/'+key,value)
    for key,value in masks.items():store.array(prefix+'/mask/'+key,value)
    marker=obs['marker_step'];valid=marker>=0;r=np.arange(len(marker));ix=np.maximum(marker,0)
    store.array(prefix+'/anchor/anchor_valid',valid)
    for name in ('q_obs','last_whiff','last_nav'):
        value=obs[name][ix,r].copy();value[~valid]=-1;store.array(prefix+'/anchor/'+name,value)
    for name,value in sample.items():
        anchor=value[ix,r].copy();anchor[~valid]=0;store.array(prefix+'/anchor/'+name,anchor)
    run['record']['L3']=save_tree_arrays(store,prefix+'/L3',score)
    return metrics


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path);parser.add_argument('--smoke',action='store_true')
    args=parser.parse_args(argv);out=args.output.resolve()
    require(out.is_relative_to((ROOT/'experiments/h17').resolve()),'output/workspace h17 directory')
    require(not out.exists(),'output/already exists');out.mkdir(parents=True)
    receipt=dict(complete=False,passed=False,smoke=args.smoke,conditions=list(CONDITIONS),records={},gates={})
    store=None;claim=None;claimdata=None
    try:
        pins,pair,provenance=preflight(ROOT,args.smoke);receipt['provenance']=provenance
        if args.smoke:require(out==(ROOT/H0).resolve(),'H0/canonical directory')
        else:claim,claimdata=claim_pair(pair,provenance,out);receipt['claim']=claim.relative_to(ROOT).as_posix()
        write_json(out/'identity.json',receipt)
        from replay_hold_stage1 import load_runtime
        m,unused,unusedattrs,verifier=load_runtime()
        # Imports above create no streams. H0 alone resolves the existing public aliases.
        if args.smoke:pair=m.seeds_of('h29',True)
        rows,steps=(40 if args.smoke else 400),600
        receipt.update(rows=rows,steps=steps)
        names=read(ROOT/'experiments/module/identity.json')['A1']['L2']['names']
        store=Archive(out/'raw.npz.ap');metric=dict(complete=False,smoke=args.smoke,source_closure_sha256_alpha=source_closure(pins),readings={})
        for condition in CONDITIONS:
            print('R0 '+condition+': literal Fly, Passive, literal Agent17',flush=True)
            runs=[run_arm(m,condition,arm,pair,rows,steps,store) for arm in ARMS]
            gate,scores=compare_runs(m,condition,*runs,names)
            receipt['records'][condition]={};metric['readings'][condition]={}
            for arm,run,score in zip(ARMS,runs,scores):
                metric['readings'][condition][arm]=save_run(store,condition,arm,run,score)
                receipt['records'][condition][arm]=run['record']
                receipt['gates'][condition+'/'+arm]=dict(passed=True,complete=True,rows=rows,steps=steps,identity=gate)
            del runs,scores;gc.collect()
            write_json(out/'identity.json',receipt)
        postpins,postpair,postprovenance=preflight(ROOT,args.smoke)
        equal(postprovenance,provenance,'postrun/full immutable provenance')
        require(len(receipt['gates'])==12 and all(x['passed'] for x in receipt['gates'].values()),'all twelve gates')
        receipt['raw_arrays']=store.finish();store=None
        # Numeric summaries are first published only after the twelve identity gates.
        metric['complete']=True;receipt['metrics_sha256_alpha']=write_json(out/'metrics.json',metric)
        receipt.update(complete=True,passed=True,first_failure=None)
        write_json(out/'identity.json',receipt)
        if claim is not None:
            claimdata['complete']=True;claimdata['identity_sha256_alpha']=file_digest(out/'identity.json')
            claimdata['raw_sha256_alpha']=receipt['raw_arrays']['sha256_alpha'];write_json(claim,claimdata)
        print('R0 identity PASS: all twelve registered arms complete',flush=True)
        return 0
    except BaseException as exc:
        receipt['complete']=False;receipt['passed']=False
        receipt['first_failure']=exc.failure if isinstance(exc,EvidenceError) else dict(field='execution exception',index=None,phase=None)
        receipt['exception_type']=type(exc).__name__
        # Error text is kept in AP bytes; incidental digit runs cannot enter legacy scans.
        receipt['error_utf8_alpha']=str(exc).encode('utf-8').hex().translate(AP)
        if exc.__cause__ is not None:
            receipt['cause_type']=type(exc.__cause__).__name__
            receipt['cause_utf8_alpha']=str(exc.__cause__).encode('utf-8').hex().translate(AP)
        if store is not None:
            try:receipt['raw_arrays']=store.finish()
            except BaseException:receipt['raw_archive_complete']=False
        try:write_json(out/'identity.json',receipt)
        except BaseException:
            diagnostic=dict(first_failure=receipt['first_failure'],exception_type=receipt['exception_type'],
                            error_utf8_alpha=receipt['error_utf8_alpha'])
            if 'cause_type' in receipt:
                diagnostic.update(cause_type=receipt['cause_type'],cause_utf8_alpha=receipt['cause_utf8_alpha'])
            emergency=dict(complete=False,passed=False,smoke=args.smoke,diagnostic_alpha=canonical(diagnostic).hex().translate(AP))
            try:write_json(out/'failure.json',emergency)
            except BaseException:
                require(claim is not None,'failure/no durable claim fallback')
                write_json(claim.with_suffix('.failure.json'),emergency)
        print('R0 FAIL: '+receipt['first_failure']['field'],flush=True)
        return 1


if __name__=='__main__':raise SystemExit(main())
