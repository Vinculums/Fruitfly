"""Run 3 external evidence recorder; original R0 modules stay immutable."""
import copy
import gc
import json
import tempfile
import zipfile
from contextlib import contextmanager
from types import SimpleNamespace
import numpy as np
import h17_r0_recording as H
import measure_h17_r0 as R
from h17_r0_recording import (AP, CONDITIONS, SAMPLE_FIELDS, MISSING, EvidenceError,
    canonical, digest, equal, require, walk, original_blob, n2_masks, wilson, first,
    source_bits)

ARMS = ('Fly', 'Passive', 'Agent17', 'GSOff', 'GS250')


def namespace(condition, arm):
    return ('efficacy' if arm in ('Fly', 'GS250') else 'validity')+'/'+condition+'/'+arm


class Archive(H.Archive):
    def __init__(self, path, keysets=None, rows=400, smoke=False):
        super().__init__(path)
        self.keysets=keysets;self.rows=rows;self.smoke=smoke;self.tags={};self.non_reference_blobarrays=set()

    def array(self,key,value):
        if self.keysets is not None and not key.startswith('blob/'):
            expected=self.keysets.get(key)
            require(expected is not None and not (self.smoke and key.startswith('inference/')),'archive/unregistered key/'+key)
            dims={'T':600,'R':self.rows,'E':3001,'G':4801,'B':5000}
            a=np.asarray(value)
            require(a.dtype.str==expected['dtype'] and list(a.shape)==[dims.get(x,x) for x in expected['shape']],
                    'archive/frozen schema/'+key)
        super().array(key,value)

    def put(self,value):
        key=super().put(value)
        self.tags[key]=dict(type='array_ref',id=key) if isinstance(value,np.ndarray) else self.tag(value)
        return key

    def put_tag(self,tag):
        descriptor=dict(kind='typed_json');payload=canonical(tag);key=digest(canonical(descriptor)+payload)
        if key not in self.blobs:
            self.array('blob/'+key,np.frombuffer(payload,dtype=np.uint8));self.blobs[key]=descriptor
        self.tags[key]=tag
        return key

    def map_refs(self,refs):
        return self.put_tag(dict(type='dict',items=[[dict(type='str',value=k),self.tags[v]] for k,v in refs.items()]))

    def seal(self,metadata):
        """Drop only unreachable dedup blobs; retain every frozen nonblob key."""
        roots=set()
        def scan(value):
            if isinstance(value,str) and value in self.blobs:roots.add(value)
            elif isinstance(value,dict):
                for v in value.values():scan(v)
            elif isinstance(value,(tuple,list)):
                for v in value:scan(v)
        scan(metadata)
        self.zip.close();self.temp.seek(0)
        source=zipfile.ZipFile(self.temp,'r')
        for key in self.arrays:
            if key.startswith('blob/') or not key.endswith(('timeline','hashes','call_refs','checkpoints')):continue
            if key.endswith('hashes'):continue
            with source.open(key+'.npy') as stream:a=np.lib.format.read_array(stream,allow_pickle=False)
            for v in a.flat:scan(bytes(v).decode('ascii'))
        pending=list(roots);seen=set()
        while pending:
            key=pending.pop()
            if key in seen:continue
            seen.add(key);before=roots.copy();scan(self.tags[key])
            if self.blobs[key]['kind']=='ndarray' and self.blobs[key]['dtype']=='|S64' and key not in self.non_reference_blobarrays:
                with source.open('blob/'+key+'.npy') as stream:a=np.lib.format.read_array(stream,allow_pickle=False)
                for v in a.flat:scan(bytes(v).decode('ascii'))
            pending.extend(roots-before)
        target=tempfile.TemporaryFile('w+b')
        with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as dest:
            for key in list(self.arrays):
                if key.startswith('blob/') and key[5:] not in seen:
                    del self.arrays[key];self.blobs.pop(key[5:],None);continue
                with source.open(key+'.npy') as src,dest.open(key+'.npy','w',force_zip64=True) as dst:
                    while chunk:=src.read(1<<18):dst.write(chunk)
        source.close();self.temp.close();self.temp=target
        # finish() needs only a closeable ZIP object, which is already closed.
        self.zip=zipfile.ZipFile(target,'a');return self.finish()


class GeneratorTap(H.GeneratorTap):
    def call(self,name,*args,**kwargs):
        outer=self.depth==0
        before=copy.deepcopy(self.bit_generator.state) if outer else None
        result=super().call(name,*args,**kwargs)
        if outer:
            self.tracker.live.setdefault(self.index,[]).append((name,args,kwargs,result,before,copy.deepcopy(self.bit_generator.state)))
        return result


class Tracker(R.Tracker):
    def __init__(self,store,condition,arm,logged=False):
        super().__init__(store,condition,arm);self.logged=logged;self.live={}

    def factory(self,*args,**kwargs):
        index=len(self.instances);require(index<len(self.roles),'rng/unregistered creation')
        original=self.original(*args,**kwargs)
        require(type(original) is np.random.Generator,'rng/literal factory type')
        handle=GeneratorTap(original,self,index) if self.logged else original
        self.instances.append(dict(index=index,role=self.roles[index],seed_args=self.store.put(args),seed_kwargs=self.store.put(kwargs),
            initial=self.store.put(original),state_type=type(original.bit_generator).__name__,handle_type=type(handle).__name__))
        self.generators.append(handle)
        return handle


class Tape(R.Tape):
    def __init__(self,store,condition,arm):
        super().__init__(store,condition,arm)
        self.base_returns=[];self.pre_wrapper_refs=[];self.gs_frames=[];self.last_original=None

    @contextmanager
    def base_tap(self,m,a,w,tracker):
        target=type(a) if isinstance(a,m.ph35.Agent17) else m.fly.Fly
        original=target.act;owned='act' in target.__dict__
        def complete(instance,*args,**kwargs):
            result=original(instance,*args,**kwargs)
            if instance is a:
                self.base_returns.append(self.store.put(result))
                self.last_base_return=result
                self.snap(a,w,'pre_wrapper',tracker.step)
                self.pre_wrapper_refs.append(self.states[-1].copy())
                self.last_original=walk(a).copy()
                tracker.checkpoint('base_act')
                if hasattr(a,'q'):
                    from h17_run3_arm import schedule
                    self.gs_frames.append(schedule(a.q,args[1],result[1],a.cast_sign,a.tgt,a.est,result[0],
                                                   enabled=type(a).SEARCH_ENABLED))
            return result
        with super().base_tap(m,a,w,tracker):
            target.act=complete
            try:yield
            finally:
                if owned:target.act=original
                else:delattr(target,'act')


class ReplayGenerator:
    """Recorded primitive returns only; no BitGenerator or random method call."""
    def __init__(self,state):
        self.bit_generator=SimpleNamespace(state=copy.deepcopy(state));self.calls=[];self.at=0

    def standard_normal(self,shape):
        require(self.at<len(self.calls),'same-state/extra primitive')
        name,args,kwargs,result,before,after=self.calls[self.at]
        require(name=='standard_normal' and not kwargs and args==(shape,),'same-state/primitive signature')
        equal(self.bit_generator.state,before,'same-state/primitive before')
        self.bit_generator.state=copy.deepcopy(after);self.at+=1
        return result.copy()


def clone_original(a):
    memo={}
    def clone(v):
        if id(v) in memo:return memo[id(v)]
        if isinstance(v,np.random.Generator):
            x=ReplayGenerator(v.bit_generator.state);memo[id(v)]=x;return x
        if isinstance(v,np.ndarray):
            x=v.copy();memo[id(v)]=x;return x
        if hasattr(v,'__dict__'):
            x=object.__new__(type(v));memo[id(v)]=x
            x.__dict__.update({k:clone(value) for k,value in vars(v).items()});return x
        return copy.deepcopy(v)
    from fly import Fly
    result=object.__new__(Fly)
    result.__dict__.update({k:clone(v) for k,v in vars(a).items() if k not in ('q','act','bump')})
    return result


def proof_shell():
    return dict(method='not_applicable_lineage',pre_state_refs=None,input_refs=None,primitive_refs=None,
                expected_state_refs=None,expected_return_refs=None,comparison_refs=None,first_failure=None)


def prove_base(clone,w,whiffs,wind,calls,actual,returned,store):
    clone.rng.calls=calls
    result=clone.act(w,whiffs,wind)
    require(clone.rng.at==4,'same-state/four original primitives')
    equal(result[0],returned[0],'same-state/base turn');equal(result[1],returned[1],'same-state/base hold')
    expected={};fields=sorted(k for k in actual if k!='q')
    for key in fields:
        value=walk(clone)[key];observed=actual[key]
        if isinstance(value,ReplayGenerator):
            equal(value.bit_generator.state,observed.bit_generator.state,'same-state/state/'+key)
            expected[key]=store.put(observed)
        else:
            equal(value,observed,'same-state/state/'+key);expected[key]=store.put(value)
    return store.map_refs(expected),store.put(result),store.put(dict(passed=True,fields=fields))


def arm_class(m,arm):
    if arm in ('GS250','GSOff'):
        from h17_run3_arm import GS250,GSOff
        return GS250 if arm=='GS250' else GSOff
    return m.fly.Fly


def endpoint(sample,construction,gs,arm):
    w=sample['W_delivered'];at=sample['AT2'];r=w.shape[1];rows=np.arange(r)
    dwell=at.sum(0,dtype=np.int64)
    if gs is not None:entry=gs['entry'];engaged=gs['engaged']
    else:
        obs=H.observations(w,at,sample['H_post'],sample['NAV']);eligible=obs['marker_mask']
        entry=eligible & ~np.concatenate([np.zeros((1,r),bool),eligible[:-1]],0);engaged=np.zeros_like(entry)
    return dict(E=w.any((0,2)),L=~w[-200:].any((0,2)),D_source=dwell,
        D_source_last200=at[-200:].sum(0,dtype=np.int64),D_good=dwell[rows,construction['good']],
        D_other=dwell[rows,1-construction['good']],V=dwell[rows,construction['good']]>dwell[rows,1-construction['good']],
        reach_source=at.any(0),whiff_source=w.any(0),ever_engaged=engaged.any(0),first_entry_step=first(entry),
        entry_event_count=entry.sum(0,dtype=np.int64))


def construct(m,condition,arm,pair,rows,tracker):
    seed_w,seed_a=pair;r=np.arange(rows)
    w=(m.ph24.ph22.Masked if condition=='W1' else m.ph24.World7)(rows,np.random.default_rng(seed_w),seed_w)
    if condition=='W1':w.pres=1-w.good;w.absent=w.good.copy()
    tw=m.ph24.World7(rows,np.random.default_rng(seed_w),seed_w) if condition=='W1' else None
    known=np.zeros((rows,2));known[r,w.good]=0. if condition=='C0' else 1.
    known[r,1-w.good]=-1. if condition=='T3' else 0.
    rng=np.random.default_rng(seed_a)
    a=m.ph35.Agent17(rows,rng,P=60,N_hi=200,G=2.,known=known,rule=True,filt=True,scope='prior',release=True) if arm=='Agent17' else arm_class(m,arm)(rows,rng,known,nch=2)
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
        require(not R.plume(w.pos,w.src,w.p_hit).any(),'construction/C0 zero effective plume')
    w.walls=False
    if tw is not None:tw.walls=False
    construction.update(start=w.pos.copy(),head0=w.head.copy(),rot0=w.rot.copy())
    require(len(tracker.generators)==len(tracker.roles),'rng/complete creation')
    require(all(np.count_nonzero(w.cell==cell)==rows//4 for cell in range(4)),'construction/cells')
    require(not a.sel.s.any() and not a.silence.any() and not a.since.any() and (a.c==140.).all() and a.present.all(),'construction/controller defaults')
    return w,tw,a,construction

def run_arm(m,condition,arm,pair,rows,steps,store,primitive_source=None,plain=False):
    print('Run3 '+condition+' '+arm+': validity and saved evidence',flush=True)
    logged=arm in ('Passive','GS250') and not plain
    tracker=Tracker(store,condition,arm,logged=logged);tape=Tape(store,condition,arm)
    proof=proof_shell();primitive_frames=[];live_frames=[]
    if arm in ('GS250','GSOff') and not plain:
        proof={key:[] for key in ('pre_state_refs','input_refs','primitive_refs','expected_state_refs','expected_return_refs','comparison_refs')}
        proof.update(method='unchanged_Fly_act_recorded_primitives',first_failure=None)
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
            tracker.step=t;tracker.last_calls={};tracker.live={};tracker.checkpoint('before');tape.snap(a,w,'pre',t)
            for name,value in dict(PRE_POS=w.pos,PRE_HEAD=w.head,PRE_ROT=w.rot,H_pre=a.held(),S_pre=a.sel.s,
                SG_pre=a.sel.S[:,0],UP_pre=a.up.P,SIL_pre=a.silence,SINCE_pre=a.since,C_pre=a.c,PRES_pre=a.present).items():put(name,t,value)
            if tw is not None:tw.pos,tw.head,tw.t=w.pos.copy(),w.head.copy(),w.t
            probability=R.plume(w.pos,w.src,w.p_hit);pa=(a.sel.s>1.).any(1)
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
            tracker.phase='base_act';before_base=tape.base_calls;before_sel=tape.circuit_calls
            clone=clone_original(a) if arm in ('GS250','GSOff') and not plain else None
            pre_refs={k:v for k,v in tape.states[-1].items() if k!='q'}
            turn,h=a.act(w,x,on)
            require(tape.base_calls==before_base+1 and tape.circuit_calls==before_sel+1,'act/exactly one original base/circuit',phase=t)
            tape.returns.append(store.put((turn,h)));tape.snap(a,w,'wrapper',t);tracker.checkpoint('wrapper')
            agent_index=tracker.roles.index('agent')
            normal_logs=[x for x in tracker.draws if x['step']==t and x['generator']==agent_index]
            calls=tracker.live.get(agent_index,[]) if logged else (primitive_source['live_frames'][t] if primitive_source else [])
            primitive_frames.append(normal_logs);live_frames.append(calls)
            if clone is not None:
                if not logged:normal_logs=primitive_source['primitive_frames'][t]
                expected,returned,comparison=prove_base(clone,w,x,on,calls,tape.last_original,tape.last_base_return,store)
                proof['pre_state_refs'].append(store.map_refs(pre_refs))
                proof['input_refs'].append(tape.inputs[-1])
                proof['primitive_refs'].append([store.put(log) for log in normal_logs])
                proof['expected_state_refs'].append(expected);proof['expected_return_refs'].append(returned)
                proof['comparison_refs'].append(comparison)
            R.output_record(m,o,t,a,h,x,pa)
            fields=dict(H_post=h,S_post=a.sel.s,SG_post=a.sel.S[:,0],UP_post=a.up.P,Y=tape.y,SIL_base=tape.sil_base,
                SIL_post=a.silence,SINCE_post=a.since,C_post=a.c,PRES_post=a.present,NAV=a.nav_hit,TO=a.due_timeout,EV=a.due_evidence,
                EST=a.est,TGT=a.tgt,TURN=turn,cast_sign=a.cast_sign,flee_side=a.flee_side,W_raw=raw_copy,W_delivered=x,
                probabilities=probability,wind_on=on)
            for name,value in fields.items():put(name,t,value)
            tracker.phase='move';w.move(turn);tracker.checkpoint('move')
            tracker.phase='bump';a.bump(w.bumped);tape.snap(a,w,'bump',t);tracker.checkpoint('bump')
            o['POS'][t]=w.pos;o['HEAD'][t]=w.head;o['AT2'][t]=w.at_source();o['C'][t]=w.bumped
            for name,value in dict(POS=w.pos,HEAD=w.head,ROT=w.rot,C=w.bumped,AT2=o['AT2'][t]).items():put(name,t,value)
            if logged:
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
        n2s=np.asarray([dictrow.get('n2S') for event,dictrow in zip(tape.events,tape.states) if event['phase']=='wrapper'],dtype='S64')
        # Lineage masks are retained in the typed snapshots; verifier decodes them.
        require(len(n2s)==steps,'N2/full lineage withheld snapshots')
    fields,world_fields,state,hashes,world=tape.arrays()
    record=dict(output_metadata={k:v for k,v in o.items() if not isinstance(v,np.ndarray)},state_fields=fields,world_fields=world_fields,
        events=tape.events,rng_labels=tracker.labels,generator_instances=tracker.instances,draw_log=tracker.draws,
        independent_streams=len(tracker.instances),generator_handles=len(tracker.instances)*(2 if logged else 1),
        literal_generators=not logged,construction_refs={k:store.put(v) for k,v in construction.items()},
        observation_calls=dict(base=tape.base_calls,circuit=tape.circuit_calls),
        primitive_log_proof=None,draw_log_reference=None,base_act_proof=dict(same_state=proof,plain_logger_H0=None),
        gs_mode='enabled' if arm=='GS250' else 'disabled' if arm=='GSOff' else 'reference',
        entry_semantics='actual' if arm in ('GS250','GSOff') else 'observational_shadow')
    tables=dict(state_timeline=state,attribute_hashes=hashes,world_timeline=world,
        rng_timeline=np.asarray(tracker.timeline,dtype='S64'),input_timeline=np.asarray(tape.inputs,dtype='S64'),return_timeline=np.asarray(tape.returns,dtype='S64'),base_return_timeline=np.asarray(tape.base_returns,dtype='S64'))
    if condition=='W1':tables.update(twin_input_timeline=np.asarray(twin_inputs,dtype='S64'),twin_return_timeline=np.asarray(twin_returns,dtype='S64'))
    gs={key:np.stack([frame[key] for frame in tape.gs_frames]) for key in tape.gs_frames[0]} if tape.gs_frames else None
    if gs is not None:
        gs['entry']=gs['engaged'] & ~np.concatenate([np.zeros((1,rows),bool),gs['engaged'][:-1]],0)
    del tape,tracker;gc.collect()
    return dict(output=o,sample=sample,construction=construction,record=record,tables=tables,twin=twin,gs=gs,primitive_frames=primitive_frames,live_frames=live_frames)


def observations(w,at,h,nav,actual_marker=None):
    steps,rows,_=w.shape;anyw=w.any(2);anya=at.any(2)
    q=np.empty((steps,rows),np.int64);clock=np.zeros(rows,np.int64)
    lastw=np.full_like(q,-1);lastnav=np.full_like(q,-1)
    for t in range(steps):
        clock=np.where(anyw[t],0,clock+1);q[t]=clock
        if t>0:lastw[t]=lastw[t-1];lastnav[t]=lastnav[t-1]
        lastw[t,anyw[t]]=t;lastnav[t,nav[t]]=t
    marker=(q>=250)&(h==-1) if actual_marker is None else actual_marker;m=first(marker);valid=m>=0
    later=(np.arange(steps)[:,None]>m)&valid[None,:]
    fw=first(anyw&later);fa=first(anya&later)
    result=dict(q_obs=q,marker_mask=marker,marker_step=m,longest_silence=q.max(0),last_whiff=lastw,last_nav=lastnav,
                first_whiff=first(anyw),first_reach=first(anya),post_first_whiff=fw,post_first_reach=fa,
                post_whiff_bits=source_bits(w,fw),post_reach_bits=source_bits(at,fa),available=np.where(valid,steps-1-m,-1).astype(np.int64),
                whiff_delay=np.where(fw>=0,fw-m,-1).astype(np.int64),reach_delay=np.where(fa>=0,fa-m,-1).astype(np.int64),
                whiff_event=valid&(fw>=0),reach_event=valid&(fa>=0),whiff_censored=valid&(fw<0),reach_censored=valid&(fa<0))
    result.update(first_whiff_bits=source_bits(w,result['first_whiff']),first_reach_bits=source_bits(at,result['first_reach']),marker_reach_bits=source_bits(at,m))
    for k in (100,200,300):
        full=valid&(m+k<=steps-1);window=later&(np.arange(steps)[:,None]<=m+k)
        result['full_'+str(k)]=full;result['censored_'+str(k)]=valid&~full
        for name,events in (('whiff',w),('reach',at)):
            result[name+'_'+str(k)]=(events.any(2)&window).any(0)&full
            for source in (0,1):result[name+'_'+str(k)+'_source'+str(source)]=(events[:,:,source]&window).any(0)&full
    return result

def readings(condition,sample,construction,actual_marker=None):
    w,at,h,nav=(sample[x] for x in ('W_delivered','AT2','H_post','NAV'));t,r,_=w.shape
    obs=observations(w,at,h,nav,actual_marker);masks=n2_masks(sample,construction['known']);valid=obs['marker_step']>=0;lost=~w[-200:].any((0,2))
    out=dict(primary=wilson(w.any((0,2)) if condition=='C0' else lost),any_whiff_600=wilson(w.any((0,2))),
             reach_600=wilson(at.any((0,2))),lost_last200=wilson(lost),markers=wilson(valid),no_marker=wilson(~valid),
             horizon_whiff=wilson(obs['whiff_event'],valid,True),horizon_reach=wilson(obs['reach_event'],valid,True),
             marker_baseline_reach=wilson(obs['marker_reach_bits']!=0,valid,True),windows={},sources={},transitions={},cells={})
    for k in (100,200,300):
        full=obs['full_'+str(k)]
        out['windows'][str(k)]=dict(full=int(full.sum()),censored=int(obs['censored_'+str(k)].sum()),
            whiff=wilson(obs['whiff_'+str(k)],full,True),reach=wilson(obs['reach_'+str(k)],full,True),
            sources={str(s):dict(whiff=wilson(obs['whiff_'+str(k)+'_source'+str(s)],full,True),
                                reach=wilson(obs['reach_'+str(k)+'_source'+str(s)],full,True)) for s in (0,1)})
    for source in (0,1):
        out['sources'][str(source)]={}
        for name,lo in (('full',0),('last200',t-200)):
            count=at[lo:,:,source].sum(0,dtype=np.int64);obs['dwell_'+name+'_source'+str(source)]=count
            out['sources'][str(source)][name]=dict(whiff=wilson(w[lo:,:,source].any(0)),reach=wilson(at[lo:,:,source].any(0)),
                 dwell_mean=float((count/(t-lo)).mean()),dwell_count=int(count.sum()),row_denominator=r,step_denominator=t-lo)
    for name in ('negative_to_unheld','negative_zero_units','negative_multiple_units','negative_identity_change','negative_end','negative_same','base','sustain','zreset','withheld_N1_S','withheld_N1_Z'):
        mask=masks[name];out['transitions'][name]=dict(events=int(mask.sum()),incidence=wilson(mask.any(0)),concurrence={})
        for flag in ('neither','timeout_only','evidence_only','both'):
            both=mask&masks[flag];out['transitions'][name]['concurrence'][flag]=dict(events=int(both.sum()),rows=int(both.any(0).sum()))
    for cell in range(4):
        selected=construction['cell']==cell
        out['cells'][str(cell)]=dict(rows=int(selected.sum()),primary=wilson(w.any((0,2)) if condition=='C0' else lost,selected),
                                    markers=wilson(valid,selected),lost_last200=wilson(lost,selected))
    out['contacts']=dict(events=int(sample['C'].sum()),rows=int(sample['C'].any(0).sum()))
    choices={'unheld':h<0,'nav':nav}
    # NAV/source-whiff and NAV/held-source masks record concurrence only;
    # neither identifies which signal caused a reset.
    for source in (0,1):
        choices['held_source'+str(source)]=h==source
        choices['nav_source'+str(source)]=nav&w[:,:,source]
        choices['held_nav_source'+str(source)]=(h==source)&nav
    out['choices']={k:dict(events=int(x.sum()),rows=int(x.any(0).sum())) for k,x in choices.items()}
    value=np.where(h>=0,construction['known'][np.arange(r)[None,:],np.maximum(h,0)],0.)
    out['transitions']['negative_identity_change']['new_value_sign']={}
    out['transitions']['negative_identity_change']['new_identity']={str(source):
        dict(events=int((masks['negative_identity_change']&(h==source)).sum()),
             rows=int((masks['negative_identity_change']&(h==source)).any(0).sum())) for source in (0,1)}
    for sign,criterion in (('positive',value>0),('zero',value==0),('negative',value<0)):
        mask=masks['negative_identity_change']&criterion
        out['transitions']['negative_identity_change']['new_value_sign'][sign]=dict(events=int(mask.sum()),rows=int(mask.any(0).sum()))
    obs['lost_last200']=lost
    return obs,masks,out


def compare_disabled(m,condition,runs,names):
    base,passive,lineage=(runs[k] for k in ('Fly','Passive','Agent17'))
    gate,scores=R.compare_runs(m,condition,base,passive,lineage,names)
    off=runs['GSOff']
    for group in ('construction','twin'):
        equal(off[group],base[group],condition+'/GSOff/'+group)
    for key,value in base['output'].items():
        if key!='arm':equal(off['output'][key],value,condition+'/GSOff/output/'+key)
    for key,value in base['sample'].items():
        if key not in ('source_uniforms','wind_uniform','turn_normal'):
            equal(off['sample'][key],value,condition+'/GSOff/sample/'+key)
    for key,value in base['tables'].items():
        if key in ('state_timeline','attribute_hashes'):
            indices=[off['record']['state_fields'].index(k) for k in base['record']['state_fields']]
            equal(off['tables'][key][:,indices],value,condition+'/GSOff/'+key)
        else:equal(off['tables'][key],value,condition+'/GSOff/'+key)
    for name in ('source_uniforms','wind_uniform','turn_normal'):off['sample'][name]=passive['sample'][name].copy()
    for arm in ('Fly','Agent17','GSOff'):
        runs[arm]['record']['draw_log_reference']=namespace(condition,'Passive')
        runs[arm]['record']['primitive_log_proof']=dict(source_arm='Passive',basis=['complete disabled identity'],passed=True)
    scores={k:s for k,s in zip(('Fly','Passive','Agent17'),scores)}
    scores['GSOff']=m.l3_scores('h29','W1' if condition=='W1' else 'T1',off['output'],600)
    equal(scores['GSOff'],scores['Fly'],condition+'/GSOff/L3')
    candidate=runs['GS250']
    equal(candidate['construction'],base['construction'],condition+'/GS250/construction')
    equal(candidate['record']['rng_labels'],base['record']['rng_labels'],condition+'/GS250/rng labels')
    equal(candidate['tables']['rng_timeline'],base['tables']['rng_timeline'],condition+'/GS250/common draw budget')
    for ci,bi in zip(candidate['record']['generator_instances'],base['record']['generator_instances']):
        for key in ('index','role','seed_args','seed_kwargs','initial','state_type'):
            equal(ci[key],bi[key],condition+'/GS250/creation/'+key)
    for name in ('source_uniforms','wind_uniform','turn_normal'):
        equal(candidate['sample'][name],passive['sample'][name],condition+'/GS250/exogenous/'+name)
    # Complete original outputs are exact on rows with no wrapper engagement.
    unengaged=~candidate['gs']['engaged'].any(0);rows=len(unengaged)
    for key,value in base['output'].items():
        other=candidate['output'][key]
        if isinstance(value,np.ndarray):
            if value.ndim>1 and value.shape[0]==600 and value.shape[1]==rows:
                equal(other[:,unengaged],value[:,unengaged],condition+'/GS250/never-engaged/'+key)
            elif value.ndim and value.shape[0]==rows:
                equal(other[unengaged],value[unengaged],condition+'/GS250/never-engaged/'+key)
    scores['GS250']=m.l3_scores('h29','W1' if condition=='W1' else 'T1',candidate['output'],600)
    candidate['record']['primitive_log_proof']=dict(source_arm='GS250',basis=['own original shared BitGenerator primitive returns'],passed=True)
    gate.update(GSOff=True,candidate_creation=True,candidate_draw_budget=True,candidate_same_state=True,never_engaged=True)
    return gate,scores


def never_engaged_states(candidate,base,store,condition):
    selected=~candidate['gs']['engaged'].any(0);rows=len(selected)
    fields=base['record']['state_fields'];other=candidate['record']['state_fields']
    require(sorted(fields+['q'])==other,condition+'/GS250/q-only fieldset')
    if not selected.any():return
    for j,field in enumerate(fields):
        cj=other.index(field)
        for tick,(left,right) in enumerate(zip(candidate['tables']['state_timeline'][:,cj],base['tables']['state_timeline'][:,j])):
            a,b=bytes(left).decode(),bytes(right).decode()
            if a==b:continue
            da,db=store.blobs[a],store.blobs[b]
            equal(da,db,condition+'/never-engaged/schema/'+field,phase=tick)
            if da['kind']=='ndarray' and da['shape'] and da['shape'][0]==rows:
                def value(key):
                    with store.zip.open('blob/'+key+'.npy','r') as stream:return np.lib.format.read_array(stream,allow_pickle=False)
                equal(value(a)[selected],value(b)[selected],condition+'/never-engaged/state/'+field,phase=tick)
            else:equal(store.tags[a],store.tags[b],condition+'/never-engaged/global/'+field,phase=tick)


def plain_proof(logged,plain,store):
    for group in ('output','construction','twin','gs','tables'):
        equal(plain[group],logged[group],'H0/plain logger/'+group)
    for key,value in plain['sample'].items():equal(value,logged['sample'][key],'H0/plain logger/sample/'+key)
    rec=plain['record'];tables=plain['tables']
    store.non_reference_blobarrays.add(store.put(tables['attribute_hashes']))
    comparison=dict(passed=True,fields=rec['state_fields'],world_fields=rec['world_fields'],events=rec['events'],rng_labels=rec['rng_labels'])
    return dict(method='literal_GS250_vs_logged_GS250_full_run',candidate_class='GS250',spent_pair_alias='h29/smoke',
        native_outputs_ref=store.put(plain['output']),state_refs=store.put(dict(fields=rec['state_fields'],events=rec['events'],timeline=tables['state_timeline'],attribute_hashes=tables['attribute_hashes'])),
        world_refs=store.put(dict(fields=rec['world_fields'],events=rec['events'],timeline=tables['world_timeline'])),
        input_refs=store.put(tables['input_timeline']),return_refs=store.put(dict(actual=tables['return_timeline'],base=tables['base_return_timeline'])),
        rng_refs=store.put(dict(labels=rec['rng_labels'],timeline=tables['rng_timeline'],instances=rec['generator_instances'])),
        construction_refs=store.put(plain['construction']),comparison_refs=store.put(comparison),first_failure=None)


def save_run(store,condition,arm,run,score):
    prefix=namespace(condition,arm);sample=run['sample'];require(set(sample)==set(SAMPLE_FIELDS),prefix+'/sample keyset')
    for group in ('output','sample','construction','twin','gs'):
        for key,value in (run[group] or {}).items():
            if isinstance(value,np.ndarray):store.array(prefix+'/'+group+'/'+key,value)
    for key,value in run['tables'].items():store.array(prefix+'/'+key,value)
    actual=run['gs']['entry'] if run['gs'] is not None else None
    obs,masks,metrics=readings(condition,sample,run['construction'],actual)
    for key,value in obs.items():store.array(prefix+'/reading/'+key,value)
    for key,value in masks.items():store.array(prefix+'/mask/'+key,value)
    ends=endpoint(sample,run['construction'],run['gs'],arm)
    for key,value in ends.items():store.array(prefix+'/endpoint/'+key,value)
    marker=obs['marker_step'];valid=marker>=0;rr=np.arange(len(marker));ix=np.maximum(marker,0)
    store.array(prefix+'/anchor/anchor_valid',valid)
    for name in ('q_obs','last_whiff','last_nav'):
        value=obs[name][ix,rr].copy();value[~valid]=-1;store.array(prefix+'/anchor/'+name,value)
    for name,value in sample.items():
        if name in ('TGT','TURN') and run['gs'] is not None:value=run['gs']['BASE_'+name]
        anchor=value[ix,rr].copy();anchor[~valid]=-1 if arm=='GSOff' and anchor.dtype.kind in 'iu' else 0
        store.array(prefix+'/anchor/'+name,anchor)
    run['record']['L3']=R.save_tree_arrays(store,prefix+'/L3',score)
    return metrics,ends


def inference_kwargs(kwargs):
    require(set(kwargs)=={'size','dtype','endpoint'} and kwargs['dtype'] is np.int64,'inference/explicit dtype')
    return dict(size=kwargs['size'],dtype='<i8',endpoint=kwargs['endpoint'])


def clause(estimate,interval,bar,direction):
    lo,hi=interval
    status=('PASS' if lo>=bar else 'FAIL' if hi<bar else 'INCONCLUSIVE') if direction=='lower' else ('PASS' if hi<=bar else 'FAIL' if lo>bar else 'INCONCLUSIVE')
    return dict(estimate=float(estimate),interval=[float(lo),float(hi)],bar=bar,direction=direction,status=status)


def inference(ends,seed,store):
    rng=np.random.Generator(np.random.PCG64(seed));before=store.put(rng)
    creation=dict(index=0,role='inference',seed_args=store.put((seed,)),seed_kwargs=store.put({}),initial=before,state_type='PCG64',handle_type='Generator')
    kwargs=dict(size=(5000,400),dtype=np.int64,endpoint=False)
    indices=rng.integers(0,400,**kwargs);after=store.put(rng)
    log=dict(generator=0,method='integers',args=store.put((0,400)),kwargs=store.put(inference_kwargs(kwargs)),result=store.put(indices),before=before,after=after,step=-1,phase='inference')
    primitive=store.put(log);store.array('inference/indices',indices);store.array('inference/checkpoints',np.asarray([before,after],dtype='S64'));store.array('inference/call_refs',np.asarray([primitive],dtype='S64'))
    clauses={}
    for name,condition,field,bar,direction in (
        ('C0_E','C0','E',.10,'lower'),('T1_V','T1','V',-.05,'lower'),('T3_V','T3','V',-.05,'lower'),
        ('T1_L','T1','L',.05,'upper'),('W1_L','W1','L',.05,'upper'),('T3_L','T3','L',.05,'upper'),('W1_D_other','W1','D_other',-6.,'lower')):
        delta=ends[condition]['GS250'][field].astype(np.int64)-ends[condition]['Fly'][field].astype(np.int64)
        replicate=np.mean(delta[indices],axis=1,dtype=np.float64);interval=np.quantile(replicate,[.025,.975],method='linear')
        for key,value in (('difference',delta),('replicate_mean',replicate),('interval',interval)):store.array('inference/'+name+'/'+key,value)
        clauses[name]=clause(delta.mean(),interval,bar,direction)
    for name,mask,bar,direction in (('C0_absolute',ends['C0']['GS250']['E'],.5,'lower'),('T1_intervention',ends['T1']['GS250']['ever_engaged'],.05,'upper')):
        ci=wilson(mask);clauses[name]=clause(ci['estimate'],ci['interval'],bar,direction)
    verdict='PASS' if all(x['status']=='PASS' for x in clauses.values()) else 'NOT_SHOWN' if any(x['status']=='FAIL' for x in clauses.values()) else 'INCONCLUSIVE/NOT_SHOWN'
    record=dict(role='INFERENCE',creation=creation,initial_state=before,final_state=after,primitive=log,
        indices_key='inference/indices',indices_sha256_alpha=digest(indices.tobytes()),replicates=5000,quantile_method='linear')
    return record,clauses,verdict
