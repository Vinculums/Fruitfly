"""R0 typed, content-addressed evidence and descriptive row arithmetic.

The measurement runner uses this module; the independent verifier does not.
No controller imports or generator construction occur on import.
"""
import hashlib
import json
import math
from pathlib import Path
import tempfile
import zipfile
import os
import numpy as np

AP=str.maketrans('0123456789abcdef','abcdefghijklmnop')
CONDITIONS=('C0','T1','W1','T3')
ARMS=('Fly','Passive','Agent17')
Z=1.959963984540054
SAMPLE_FIELDS=tuple(('PRE_POS PRE_HEAD PRE_ROT H_pre H_post S_pre S_post SG_pre SG_post UP_pre UP_post Y '
 'SIL_pre SIL_base SIL_post SINCE_pre SINCE_post C_pre C_post PRES_pre PRES_post NAV TO EV '
 'base sustain negS negZ newz zreset withheld_N1_S withheld_N1_Z reset_drive EST TGT TURN cast_sign flee_side '
 'POS HEAD ROT C AT2 W_raw W_delivered source_uniforms probabilities wind_uniform wind_on turn_normal').split())
MISSING=object()


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')


def digest(raw):return hashlib.sha256(raw).hexdigest().translate(AP)


def require(ok,field,index=None,phase=None):
    if not bool(ok):raise EvidenceError(field,index,phase)


class EvidenceError(RuntimeError):
    def __init__(self,field,index=None,phase=None):
        self.failure=dict(field=field,index=index,phase=phase)
        super().__init__(field)


def equal(a,b,label,phase=None):
    if isinstance(a,dict):
        require(isinstance(b,dict) and set(a)==set(b),label+'/keys',phase=phase)
        for key in a:equal(a[key],b[key],label+'/'+str(key),phase)
        return
    if isinstance(a,np.ndarray) or isinstance(b,np.ndarray):
        x,y=np.asarray(a),np.asarray(b)
        require(x.dtype==y.dtype and x.shape==y.shape,label+'/schema',phase=phase)
        if x.tobytes(order='C')!=y.tobytes(order='C'):
            xx=np.ascontiguousarray(x).view(np.uint8).reshape(x.shape+(x.dtype.itemsize,))
            yy=np.ascontiguousarray(y).view(np.uint8).reshape(y.shape+(y.dtype.itemsize,))
            index=np.argwhere((xx!=yy).any(-1))[0].tolist()
            raise EvidenceError(label,index,phase)
    else:require(type(a) is type(b) and repr(a)==repr(b),label,phase=phase)


class Archive:
    """Stream arrays into a private ZIP, then AP-encode in bounded chunks."""
    def __init__(self,path):
        self.path=Path(path);self.temp=tempfile.TemporaryFile('w+b')
        self.zip=zipfile.ZipFile(self.temp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6)
        self.arrays={};self.blobs={};self.closed=False

    def array(self,key,value):
        original=np.asarray(value);a=np.ascontiguousarray(original).reshape(original.shape)
        require(not a.dtype.hasobject and a.dtype.kind in 'biufUS',key+'/supported dtype')
        description=dict(dtype=a.dtype.str,shape=list(a.shape),nbytes=a.nbytes,sha256_alpha=digest(a.tobytes()))
        if key in self.arrays:
            require(self.arrays[key]==description,key+'/duplicate unequal array');return
        with self.zip.open(key+'.npy','w',force_zip64=True) as stream:
            np.lib.format.write_array(stream,a,allow_pickle=False)
        self.arrays[key]=description

    def tag(self,value):
        if value is MISSING:return dict(type='missing')
        if isinstance(value,np.ndarray):return dict(type='array_ref',id=self.put(value))
        if isinstance(value,np.random.Generator):return dict(type='generator',state=self.tag(value.bit_generator.state))
        if value is None:return dict(type='none')
        if isinstance(value,np.generic):
            return dict(type='numpy_scalar',dtype=value.dtype.str,value_hex_alpha=value.tobytes().hex().translate(AP))
        if type(value) in (bool,int,float,str):
            return dict(type=type(value).__name__,value=value.hex() if type(value) is float else value)
        if isinstance(value,(list,tuple,set)):
            items=[self.tag(x) for x in value]
            if isinstance(value,set):items.sort(key=canonical)
            return dict(type=type(value).__name__,items=items)
        if isinstance(value,dict):return dict(type='dict',items=[[self.tag(k),self.tag(v)] for k,v in value.items()])
        raise EvidenceError('unsupported snapshot type '+type(value).__name__)

    def put(self,value):
        if isinstance(value,np.ndarray):
            original=np.asarray(value);a=np.ascontiguousarray(original).reshape(original.shape)
            descriptor=dict(kind='ndarray',dtype=a.dtype.str,shape=list(a.shape));payload=a.tobytes()
        else:
            descriptor=dict(kind='typed_json');payload=canonical(self.tag(value));a=np.frombuffer(payload,dtype=np.uint8)
        key=digest(canonical(descriptor)+payload)
        if key not in self.blobs:
            self.array('blob/'+key,a);self.blobs[key]=descriptor
        return key

    def finish(self):
        if self.closed:return self.manifest
        self.zip.close();self.temp.seek(0);hasher=hashlib.sha256()
        temporary=self.path.with_suffix(self.path.suffix+'.tmp')
        try:
            with temporary.open('wb') as dest:
                while chunk:=self.temp.read(1<<18):
                    encoded=chunk.hex().translate(AP).encode('ascii');dest.write(encoded);hasher.update(encoded)
                dest.flush();os.fsync(dest.fileno())
            temporary.replace(self.path)
        finally:self.temp.close()
        self.closed=True
        self.manifest=dict(path=self.path.name,encoding='NPZ compressed; hex nibble a-p maps to 0-f',
                           sha256_alpha=hasher.hexdigest().translate(AP),keys=sorted(self.arrays),arrays=self.arrays,blobs=self.blobs)
        return self.manifest


class GeneratorTap(np.random.Generator):
    """One handle to the original BitGenerator; no new stream or extra draw."""
    def __init__(self,generator,tracker,index):
        super().__init__(generator.bit_generator)
        self.tracker,self.index=tracker,index

    def call(self,name,*args,**kwargs):
        tr=self.tracker;before=tr.store.put(self)
        result=getattr(super(),name)(*args,**kwargs)
        tr.draws.append(dict(generator=self.index,method=name,args=tr.store.put(args),kwargs=tr.store.put(kwargs),
                            result=tr.store.put(result),before=before,after=tr.store.put(self),step=tr.step,phase=tr.phase))
        tr.last_calls.setdefault(self.index,[]).append((name,result))
        return result

    def random(self,*a,**k):return self.call('random',*a,**k)
    def uniform(self,*a,**k):return self.call('uniform',*a,**k)
    def integers(self,*a,**k):return self.call('integers',*a,**k)
    def permutation(self,*a,**k):return self.call('permutation',*a,**k)
    def choice(self,*a,**k):return self.call('choice',*a,**k)
    def standard_normal(self,*a,**k):return self.call('standard_normal',*a,**k)


def walk(agent):
    state={}
    for key,value in vars(agent).items():
        if key in ('act','bump'):continue
        if key in ('up','sel','ring','mb'):
            for sub,item in vars(value).items():state[key+'.'+sub]=item
        else:state[key]=value
    return state


def original_blob(value):
    if value is MISSING:return b'M'
    if isinstance(value,np.ndarray):
        a=np.ascontiguousarray(value);return b'A'+a.dtype.str.encode()+repr(a.shape).encode()+a.tobytes()
    if isinstance(value,np.random.Generator):return b'G'+repr(value.bit_generator.state).encode()
    if value is None or isinstance(value,(bool,int,float,str,tuple,list,set,np.generic)):
        return b'S'+type(value).__name__.encode()+repr(value).encode()
    raise EvidenceError('unsupported original state hash type '+type(value).__name__)


def first(mask):return np.where(mask.any(0),mask.argmax(0),-1).astype(np.int64)


def source_bits(mask,indices):
    result=np.zeros(mask.shape[1],np.uint8)
    for row,at in enumerate(indices):
        if at>=0:result[row]=int(mask[at,row,0])|int(mask[at,row,1])<<1
    return result


def wilson(mask,selected=None,conditional=False):
    selected=np.ones(np.shape(mask),bool) if selected is None else selected
    n=int(np.count_nonzero(selected));k=int(np.count_nonzero(mask&selected))
    if n==0:return dict(numerator=k,denominator=n,estimate=None,interval=None,status='UNDEFINED')
    p=k/n;den=1+Z*Z/n;centre=(p+Z*Z/(2*n))/den
    width=Z*math.sqrt(p*(1-p)/n+Z*Z/(4*n*n))/den
    return dict(numerator=k,denominator=n,estimate=p,interval=[centre-width,centre+width],
                status='UNREADABLE' if conditional and n<50 else 'READABLE')


def observations(w,at,h,nav):
    steps,rows,_=w.shape;anyw=w.any(2);anya=at.any(2)
    q=np.empty((steps,rows),np.int64);clock=np.zeros(rows,np.int64)
    lastw=np.full_like(q,-1);lastnav=np.full_like(q,-1)
    for t in range(steps):
        clock=np.where(anyw[t],0,clock+1);q[t]=clock
        if t>0:lastw[t]=lastw[t-1];lastnav[t]=lastnav[t-1]
        lastw[t,anyw[t]]=t;lastnav[t,nav[t]]=t
    marker=(q>=250)&(h==-1);m=first(marker);valid=m>=0
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


def n2_masks(sample,known):
    hp,h=sample['H_pre'],sample['H_post'];t,r=hp.shape;ti=np.arange(t)[:,None];ri=np.arange(r)[None,:]
    pre=np.maximum(hp,0);post=np.maximum(h,0)
    negS=(hp>=0)&(known[ri,pre]<0);negZ=(h>=0)&(known[ri,post]<0)
    hit=(h>=0)&sample['W_delivered'][ti,ri,post];new=(h>=0)&(h!=hp)
    TO=sample['SIL_pre']>40;Y=sample['Y']
    EV=(hp>=0)&((Y[ti,ri,1-pre]-Y[ti,ri,pre])>.2)
    sil=np.where(hit,0.,np.where(TO|EV,0.,sample['SIL_pre'])+1.)
    units=(sample['S_post']>1.).sum(2,dtype=np.int64)
    base=TO&~EV&(units>0)&~hit;sustain=base&~negS;newz=new&~negZ
    empty=negS&(h==-1);change=negS&(h>=0)&(h!=hp)
    return dict(hit=hit,new=new,negS=negS,negZ=negZ,TO=TO,EV=EV,base=base,sustain=sustain,newz=newz,
                zreset=newz&~sustain&(sil>0),withheld_N1_S=base&negS,withheld_N1_Z=new&negZ,SIL_base=sil,
                SIL_post=np.where(sustain,41.,np.where(newz,0.,sil)),reset_drive=np.where(TO|EV,10.,0.),units=units,
                negative_to_unheld=empty,negative_zero_units=empty&(units==0),negative_multiple_units=empty&(units>1),
                negative_identity_change=change,negative_end=empty|change,negative_same=negS&(h==hp),
                neither=~TO&~EV,timeout_only=TO&~EV,evidence_only=~TO&EV,both=TO&EV)


def readings(condition,sample,construction):
    w,at,h,nav=(sample[x] for x in ('W_delivered','AT2','H_post','NAV'));t,r,_=w.shape
    obs=observations(w,at,h,nav);masks=n2_masks(sample,construction['known']);valid=obs['marker_step']>=0;lost=~w[-200:].any((0,2))
    out=dict(primary=wilson(w[:300].any((0,2)) if condition=='C0' else lost),any_whiff_600=wilson(w.any((0,2))),
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
        out['cells'][str(cell)]=dict(rows=int(selected.sum()),primary=wilson(w[:300].any((0,2)) if condition=='C0' else lost,selected),
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
