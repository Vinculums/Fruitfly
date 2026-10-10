#!/usr/bin/env python3
"""Independently verify saved E1 evidence without agents, worlds or random draws.

Only NumPy and the standard library are imported. The source constants are
read as data through AST, never executed. This tool writes its own verification
receipt; it does not alter the screen, its arrays, pins or claim.
"""
import argparse
import ast
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
FINAL='notes/hold/2026-10-09-hold-e1-w1dp-design-v2.md'
CONFIG='config/hold-e1-seeds.json'
REGISTRATION='experiments/hold/hold_e1_seed_registration.json'
EXECUTION='config/hold-e1-execution-pins.json'
ALPHABET=str.maketrans('0123456789abcdef','abcdefghijklmnop')
HEX=str.maketrans('abcdefghijklmnop','0123456789abcdef')
ORDER=('identity','val','hit','vh','presence_override','presence','top','eligible',
       'keep','nav','since','silence','flee','tgt','clipped_turn','post_silence')
L1=('POS','HEAD','S','SG','H','NAV','SINCE','TGT','SIL','TO','EV','SUS','Z','W','AT2','C','VAL')
THREADS=('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','PH30_PROCS','PH32_PROCS','PH33_PROCS')
STATE_KEYS=set('held since silence counter upstream position heading rotation whiffs wind_on actual_hold instantaneous counter_post upstream_post circuit circuit_pool known est flee_side cast_sign silence_post since_post nav tgt turn burst bb w2 timeout evidence gated_y'.split())
OUTPUT_KEYS=set('kv good cell plus_y src start s0 H0 SIL SINCE TGT TURN EST SG NAV TO EV SUS Z PRES NAV6 NAV8 DIFF8 C CONE H HR W S C2 P2 POS HEAD AT2 VAL TOP TOPR BURST BB BW2 KEEP15 KEEP NAV15 ACT dwell contacts'.split())
LABELS={'arm','cls','kind'}
COMMON=tuple('G N N_hi P R bb burst c cast_sign codes due_evidence due_timeout est flee_side known last_turn mb.C mb.K mb.R mb.beta mb.eta_d mb.eta_p mb.gated mb.parallel mb.rng mb.sparsity mb.tau_code mb.tau_reinf mb.tc mb.tr mb.w mb.wmax mb.wmin nav_hit nch present ring.J ring.R ring.Rmax ring.ang ring.c ring.n ring.noise ring.o ring.p ring.rng ring.s ring.sigma ring.tau ring.vgain ring.width rng sel.R sel.S sel.g sel.gsat sel.k sel.n sel.noise sel.pool_c sel.pool_p sel.rng sel.rng3 sel.s sel.tau sel.tau_g sel.theta sel.w_i silence since sustain t16 tgt up.P up.Rmax up.k up.n up.sig_n up.tau w2 zreset'.split())
LINEAGE_ONLY=tuple('abl acts belief cast differs differs8 filt fix hold_read hr keep15 keep16 n2S n2Z nav15 nav6 nav8 prev release rot_in rule scope top15 topr val yp'.split())


class VerificationError(RuntimeError):
    pass


def require(ok,label):
    if not bool(ok):raise VerificationError(label)


def digest(raw):return hashlib.sha256(raw).hexdigest().translate(ALPHABET)


def unique(pairs):
    result={}
    for key,value in pairs:
        require(key not in result,'duplicate JSON key')
        result[key]=value
    return result


def read(path):
    return json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=unique,
                      parse_constant=lambda x: (_ for _ in ()).throw(VerificationError('nonfinite JSON number')))


def same(a,b,label):
    a,b=np.asarray(a),np.asarray(b)
    require(a.dtype==b.dtype and a.shape==b.shape and np.ascontiguousarray(a).tobytes()==np.ascontiguousarray(b).tobytes(),label)


def numeric_same(a,b,label):
    # Integer indices/counters may have different recorded widths. Values
    # must still agree exactly; no tolerance is introduced.
    a,b=np.asarray(a),np.asarray(b)
    require(a.shape==b.shape and np.array_equal(a,b),label)


def safe_expression(node,environment):
    if isinstance(node,ast.Constant):return node.value
    if isinstance(node,ast.Name):return environment[node.id]
    if isinstance(node,(ast.Tuple,ast.List)):
        values=[safe_expression(x,environment) for x in node.elts]
        return tuple(values) if isinstance(node,ast.Tuple) else values
    if isinstance(node,ast.Dict):
        return {safe_expression(k,environment):safe_expression(v,environment) for k,v in zip(node.keys,node.values)}
    if isinstance(node,ast.UnaryOp) and isinstance(node.op,(ast.USub,ast.UAdd)):
        value=safe_expression(node.operand,environment)
        return -value if isinstance(node.op,ast.USub) else value
    if isinstance(node,ast.BinOp):
        left,right=safe_expression(node.left,environment),safe_expression(node.right,environment)
        functions={ast.Add:lambda:left+right,ast.Sub:lambda:left-right,ast.Mult:lambda:left*right,
                   ast.Div:lambda:left/right,ast.Pow:lambda:left**right}
        return functions[type(node.op)]()
    if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='dict' and not node.args:
        return {k.arg:safe_expression(k.value,environment) for k in node.keywords}
    if isinstance(node,ast.Subscript):return safe_expression(node.value,environment)[safe_expression(node.slice,environment)]
    raise ValueError('not a data-only constant expression')


def constants(path):
    result={}
    def bind(target,value):
        if isinstance(target,ast.Name):result[target.id]=value
        elif isinstance(target,(ast.Tuple,ast.List)):
            for child,item in zip(target.elts,value):bind(child,item)
    for statement in ast.parse(path.read_text(encoding='utf-8')).body:
        if isinstance(statement,ast.Assign):
            if (len(statement.targets)==1 and isinstance(statement.targets[0],(ast.Tuple,ast.List))
                and isinstance(statement.value,(ast.Tuple,ast.List))):
                for target,expression in zip(statement.targets[0].elts,statement.value.elts):
                    try:bind(target,safe_expression(expression,result))
                    except (KeyError,ValueError,TypeError):continue
                continue
            try:value=safe_expression(statement.value,result)
            except (KeyError,ValueError,TypeError):continue
            for target in statement.targets:bind(target,value)
    return result


def source_constants(root):
    result=constants(root/'src/fly.py')
    plume=constants(root/'src/ph9.py')
    geometry=constants(root/'src/ph16.py')
    for key in ('W0','SLOPE','LAM','LMAX','HIT_R'):result[key]=plume[key]
    for key in ('SEP','DOWN'):result[key]=geometry[key]
    return result


def legacy_numbers(root):
    offsets=constants(root/'src/ph32.py')
    protected=set()
    for name in ('ph33','ph35'):
        values=constants(root/('src/'+name+'.py'))
        seeds,bench=values['SEEDS'],values['BENCH']
        worlds=[seeds['dev'][0],seeds['eval'][0],bench['seed_w']]
        agents=[seeds['dev'][1],seeds['eval'][1],bench['seed_a']]
        protected.update([*seeds['dev'],*seeds['eval'],bench['seed_w'],bench['seed_a'],bench['boot']])
        protected.update(x+10000 for x in worlds)
        protected.update(x+20000 for x in agents)
        protected.update(x+20000 for x in worlds)
        protected.update((bench['seed_w']+10000000,bench['seed_a']+20000000))
        if name=='ph33':
            protected.update(x+offsets['D_OFF'] for x in worlds)
            protected.update(x+offsets['A3_OFF'] for x in agents)
    return protected


def no_protected_tokens(raw,root):
    require(not any(re.search(rb'(?<!\d)'+str(n).encode()+rb'(?!\d)',raw) for n in legacy_numbers(root)),
            'P5 collision; representation review required, evidence remains unchanged')


def array_descriptor(a):
    return dict(dtype=a.dtype.str,shape=list(a.shape),sha256_alpha=digest(np.ascontiguousarray(a).tobytes()))


def check_descriptor(a,descriptor,label):
    require(descriptor==array_descriptor(a),'array shape/dtype/hash mismatch: '+label)


def snapshot_blob(value):
    if isinstance(value,np.ndarray):
        a=np.ascontiguousarray(value)
        return b'A'+a.dtype.str.encode()+repr(a.shape).encode()+a.tobytes()
    return b'S'+type(value).__name__.encode()+repr(value).encode()


def mask_metric(mask):
    require(mask.dtype==bool and mask.ndim==2,'metric must be boolean steps x rows')
    steps,rows=mask.shape
    return dict(events=int(mask.sum()),rows=int(mask.any(0).sum()),denominator_row_steps=steps*rows,denominator_rows=rows)


def first_true(mask):return np.where(mask.any(0),mask.argmax(0),-1)


def burst_evidence(whiffs,never,window):
    steps,rows,chans=whiffs.shape
    count=np.cumsum(whiffs,axis=0,dtype=np.int64)
    previous=np.concatenate([np.zeros((1,rows,chans),np.int64),count[:-1]])
    before_window=np.zeros_like(count)
    before_window[window+1:]=count[:-(window+1)]
    burst=whiffs & ((previous-before_window)>=2)
    time=np.arange(steps,dtype=float)[:,None,None]
    latest=np.maximum.accumulate(np.where(burst,time,never),axis=0)
    whiff_time=np.maximum.accumulate(np.where(whiffs,time,never),axis=0)
    prior_whiff=np.concatenate([np.full((1,rows,chans),never),whiff_time[:-1]])
    second=np.maximum.accumulate(np.where(whiffs,prior_whiff,never),axis=0)
    return burst,latest,second


def clip_command(target,estimate,c):
    difference=(target-estimate+180.)%360.-180.
    return np.clip(c['GAIN']*difference,-c['MAXTURN'],c['MAXTURN'])


def project(identity,state,c,counter,bb,release,sustain,newz):
    steps,rows=identity.shape
    t=np.arange(steps)[:,None];r=np.arange(rows)[None,:];index=np.maximum(identity,0)
    values=state['known'];x=state['whiffs']
    value=np.where(identity>=0,values[t,r,index],0.)
    hit=np.where(identity>=0,x[t,r,index],False)
    vh=values[t,r,index]
    override=np.zeros_like(x);override[t,r,index]=identity>=0
    present=(counter<c['N_HI'][3])|override
    maximum=np.where(present,values,-np.inf).max(2)
    top=present&(values>=0)&(values==maximum[:,:,None])
    most=np.where(top,bb,-np.inf).max(2)
    ranked=top&(bb==most[:,:,None])&(most>c['NEVER'])[:,:,None]
    eligible=np.where((top.sum(2)>=2)[:,:,None],ranked,top)
    keep=(identity>=0)&(eligible[t,r,index]|(vh<0))
    nav=np.where(keep,hit,(x&eligible).any(2))
    since=np.where(nav,0.,state['since']+1.)
    before_silence=np.where(release,0.,state['silence'])
    silence=np.where(hit,0.,before_silence+1.)
    side=np.where((since//c['CAST_PERIOD'])%2==0,1.,-1.)*state['cast_sign']
    offset=c['MAXOFF']*(1.-np.abs((since/c['SAT'])%2.-1.))
    target=np.where(nav,c['UPWIND'],(c['UPWIND']+side*offset)%360.)
    target=np.where(value<0,state['flee_side'],target)
    post=np.where(sustain,c['RESET_AFTER']+1.,np.where(newz,0.,silence))
    return dict(identity=identity,val=value,hit=hit,vh=vh,presence_override=override,
                presence=present,top=top,eligible=eligible,keep=keep,nav=nav,since=since,
                silence=silence,flee=value<0,tgt=target,clipped_turn=clip_command(target,state['est'],c),post_silence=post)


def routes(h,r,state,good,c,burst,bb):
    steps,rows=h['identity'].shape
    time=np.arange(steps)[:,None];row=np.arange(rows)[None,:];v=good[None,:];b=1-v
    x=state['whiffs'];bx=x[time,row,b];dx=x[:,:,2]
    counter_both=state['counter_post'][time,row,v]>=c['N_HI'][3]
    read_neither=(h['identity']!=v)&(r['identity']!=v)
    t1=counter_both&read_neither
    t2=np.ones((steps,rows),bool)
    for p in (h,r):
        t2 &= p['presence'][time,row,b]&p['presence'][:,:,2]&p['top'][time,row,b]&p['top'][:,:,2]
    t3=(bb[time,row,b]==bb[:,:,2])&(bb[:,:,2]>c['NEVER'])
    t4=(bx!=dx)&~burst[time,row,b]&~burst[:,:,2]
    whiffing=np.where(bx,b,2);nonwhiffing=np.where(bx,2,b)
    split=((h['identity']==nonwhiffing)&((r['identity']==whiffing)|(r['identity']<0)))
    split |= ((r['identity']==nonwhiffing)&((h['identity']==whiffing)|(h['identity']<0)))
    t5=split&(h['nav']!=r['nav'])
    conjunction=t1&t2&t3&t4&t5;denominator=t1&t2&t3&t4
    command=h['clipped_turn']!=r['clipped_turn']
    presence=(h['presence']!=r['presence']).any(2)
    release=state['timeout']|state['evidence']
    adjacent=release.copy();adjacent[1:] |= release[:-1];adjacent[:-1] |= release[1:]
    return dict(T1=t1,T2=t2,T3=t3,T4=t4,T5=t5,T1_T4=denominator,T1_T5=conjunction,
        T1_noVcounter_both=counter_both,T1_read_neither_V=read_neither,command=command,
        command_tied_route=command&conjunction,command_outside_tied_route=command&~conjunction,
        command_presence_difference=command&presence,command_presence_equal=command&~presence,
        release_adjacent=adjacent,release_adjacent_command=command&adjacent,
        simultaneous_B_D_bursts=burst[time,row,b]&burst[:,:,2],raw_latest_burst_tie=t3,raw_single_nonburst=t4)


def lost_original(whiffs):
    require(whiffs.ndim==3 and whiffs.shape[2]==3,'three-channel lost input')
    return ~whiffs[-200:,:,:2].any((0,2))


def screen_reading(flags,rows):
    require(set(flags)=={'X1','X2','X3','X4'},'screen flag keyset')
    if not flags['X1']:return 'BLOCKED/INVALID'
    if not flags['X2']:return 'BLOCKED: POSITIVE CONTROL NOT REACHED'
    if not flags['X4']:return 'UNREADABLE: LOSS RANGE'
    if not flags['X3']:
        return 'NOT REACHED IN THIS SAMPLE' if rows==0 else 'REACHED, BELOW REGISTERED SCREEN'
    return 'READABLE FOR A SEPARATE BENEFIT DESIGN'


def w1_scores(output):
    """Complete ph22-style W1 summary, independently written, no exclusions."""
    steps,rows=output['H'].shape;r=np.arange(rows);b=1-output['good']
    at=output['AT2'][:,r,b];w=output['W'][:,r,b];h=output['H'];nav=output['NAV'];pos=output['POS']
    source=output['src'][r,b]
    along=pos[:,:,0]-source[None,:,0];cross=np.abs(pos[:,:,1]-source[None,:,1]);distance=np.hypot(along,cross)
    nearby=distance<5.;entries=(nearby&~np.vstack([np.zeros((1,rows),bool),nearby[:-1]])).sum(0)
    held=h==b[None,:];before=np.vstack([np.zeros((1,rows),bool),held[:-1]])
    ended=~held&before;to,ev=output['TO'],output['EV']
    dv=output['dwell'][r,output['good']];dn=output['dwell'][r,b]
    full=dict(reach=at.any(0),first=first_true(at),dwell=at.sum(0),whiffs=w.sum(0),fw=first_true(w),nav=nav.sum(0),
        lost=~w[-steps//3:].any(0),nonav=~nav[-steps//3:].any(0),contacts=output['C'].sum(0),
        heldB=held.mean(0),nothing=(h<0).mean(0),formed=(held&~before).sum(0),released=ended.sum(0),
        end_to=(ended&to&~ev).sum(0),end_ev=(ended&ev&~to).sum(0),end_both=(ended&to&ev).sum(0),
        end_none=(ended&~to&~ev).sum(0),fh=first_true(h>=0),heldB_end=held[-1],
        cone=((along>0)&(along<25.)&(cross<1.5+.25*along)).sum(0),da_min=along.min(0),da_end=along[-1],
        dc_end=cross[-1],dmin=distance.min(0),f5=first_true(nearby),ent5=entries,
        since_max=float(output['SINCE'].max()),cum={str(k):at[:k].any(0) for k in range(100,steps+1,100)})
    return dict(dwell=output['dwell'],contacts=output['contacts'],first=np.where(output['AT2'].any(0),output['AT2'].argmax(0),-1),
        cls3=np.where(dv>dn,0,np.where(dn>dv,1,2)),lost_t1=lost_original(output['W']),
        w1sum=dict(reach=at.any(0),dwell=at.sum(0).astype(float),lost=~w[400:].any(0),contacts=output['C'].sum(0).astype(float)),
        complete_w1_summary=full)


def compare_tree(left,right,label):
    if isinstance(left,dict):
        require(isinstance(right,dict) and left.keys()==right.keys(),label+' keyset')
        for key in left:compare_tree(left[key],right[key],label+'/'+str(key))
    else:same(left,right,label)


def mapping(output,c,rows):
    good,cell,plus=output['good'],output['cell'],output['plus_y'];src=output['src']
    require(good.shape==cell.shape==plus.shape==(rows,) and src.shape==(rows,2,2),'source mapping shapes')
    require(np.isin(cell,[0,1,2,3]).all(),'cell bounds')
    numeric_same(np.bincount(cell,minlength=4),np.full(4,rows//4),'balanced cells')
    numeric_same(good,cell//2,'cell/good mapping')
    numeric_same(plus,np.where(cell%2==0,good,1-good),'cell/physical +y mapping')
    numeric_same(plus,src[:,:,1].argmax(1),'physical +y source order')
    same(src[:,0,0],src[:,1,0],'two source x coordinates')
    # Compare differences to SEP with exact numerical equality; both source
    # coordinates were formed by equal additions/subtractions of SEP/2.
    numeric_same(np.abs(src[:,0,1]-src[:,1,1]),np.full(rows,c['SEP']),'source separation')
    expected_start=np.stack([src[:,0,0]+c['DOWN'],(src[:,0,1]+src[:,1,1])/2],1)
    same(output['start'],expected_start,'midline start')


def group(arrays,prefix):
    return {key[len(prefix):]:value for key,value in arrays.items() if key.startswith(prefix)}


def numeric_snapshot(output,state,c,rows,steps,label):
    require(set(output)==OUTPUT_KEYS,label+' output keyset')
    require(STATE_KEYS<=state.keys(),label+' state keyset')
    require(set(state)<=STATE_KEYS|{'release'},label+' extra state key')
    mapping(output,c,rows)
    require(state['whiffs'].dtype==bool and state['whiffs'].shape==(steps,rows,3),label+' complete whiffs')
    for key,value in state.items():
        require(value.shape[:2]==(steps,rows),label+' state shape: '+key)
        require(value.dtype.kind in 'biuf',label+' state numeric dtype: '+key)
        if value.dtype.kind=='f':require(np.isfinite(value).all(),label+' nonfinite state: '+key)
    x=state['whiffs'];known=state['known']
    values=np.zeros((rows,3));v=output['good'];r=np.arange(rows)
    values[r,v]=1.;values[r,1-v]=-1. if label.startswith('B5/') else 0.
    same(output['kv'],values,label+' supplied values')
    same(known,np.broadcast_to(values,(steps,rows,3)),label+' constant known values')
    same(output['W'],x,label+' recorded whiffs')
    numeric_same(output['H0'],np.full(rows,-1),label+' no inherited hold')
    same(output['s0'],np.zeros((rows,3)),label+' zero initial circuit')
    initial=dict(held=output['H0'],since=np.zeros(rows),silence=np.zeros(rows),
                 counter=np.full((rows,3),float(c['N_HI'][3]-c['P_PRIOR'])),
                 upstream=np.zeros((rows,3)),position=output['start'],rotation=np.zeros(rows))
    post=dict(held='actual_hold',since='since_post',silence='silence_post',counter='counter_post',upstream='upstream_post')
    for key,value in initial.items():
        numeric_same(state[key][0],value,label+' initial '+key)
        if key in post:same(state[key][1:],state[post[key]][:-1],label+' temporal continuity '+key)
    same(state['position'][1:],output['POS'][:-1],label+' pre-move position timing')
    same(state['heading'][1:],output['HEAD'][:-1],label+' pre-move heading timing')
    rotation=(output['HEAD'][:-1]-state['heading'][:-1]+180.)%360.-180.
    same(state['rotation'][1:],rotation,label+' rotation made input')
    expected_up=state['upstream']+(1./c['UP_TAU'])*(-state['upstream']+np.maximum(x.astype(float),0.)**c['UP_N'])
    same(state['upstream_post'],expected_up,label+' deterministic upstream update')
    others=(expected_up.sum(2,keepdims=True)-expected_up)/2
    y=c['UP_RMAX']*expected_up/(c['UP_SIG']**c['UP_N']+expected_up+c['UP_K']*others)
    y=y*(1.+c['G_STAR']*np.maximum(known,0.))
    t=np.arange(steps)[:,None];ri=np.arange(rows)[None,:];hp=state['held'];index=np.maximum(hp,0)
    vh=known[t,ri,index]
    y=y*~((hp>=0)[:,:,None]&(known>=0)&(known<vh[:,:,None]))
    same(state['gated_y'],y,label+' reconstructed gated upstream y')
    q=np.where(y.max(2)>.05,y.argmax(2),-1)
    numeric_same(state['instantaneous'],q,label+' instantaneous identity')
    held=state['circuit']>c['HOLD']
    actual=np.where(held.sum(2)==1,held.argmax(2),-1)
    numeric_same(state['actual_hold'],actual,label+' actual circuit read')
    other=y.copy();other[t,ri,index]=-np.inf;competitor=other.argmax(2)
    evidence=(hp>=0)&((y[t,ri,competitor]-y[t,ri,index])>c['MARGIN'])
    timeout=state['silence']>c['RESET_AFTER'];release=timeout|evidence
    same(state['timeout'],timeout,label+' timeout')
    same(state['evidence'],evidence,label+' evidence release')
    if 'release' in state:same(state['release'],release,label+' release mask')
    counter=np.where(x,0.,state['counter']+1.)
    same(state['counter_post'],counter,label+' counter update')
    numeric_same(output['C2'],counter.astype(output['C2'].dtype),label+' counter output wiring')
    burst,bb,w2=burst_evidence(x,c['NEVER'],c['WIN'])
    for key,value in (('burst',burst),('bb',bb),('w2',w2)):
        same(state[key],value,label+' independent burst history '+key)
    same(state['wind_on'],np.ones((steps,rows),bool),label+' always-on wind')
    require(np.isin(state['cast_sign'],[-1.,1.]).all(),label+' cast signs')
    require(np.isin(state['flee_side'],c['FLEE_SIDES']).all(),label+' flee sides')
    same(state['cast_sign'][1:],state['cast_sign'][:-1]*np.where(output['C'][:-1],-1.,1.),label+' wall/cast timing')
    same(state['flee_side'][1:],np.where(output['C'][:-1],(state['flee_side'][:-1]+180.)%360.,state['flee_side'][:-1]),label+' wall/flee timing')
    hit=(actual>=0)&x[t,ri,np.maximum(actual,0)]
    neg_previous=(hp>=0)&(known[t,ri,index]<0.)
    neg_actual=(actual>=0)&(known[t,ri,np.maximum(actual,0)]<0.)
    sustain=timeout&~evidence&(state['circuit']>1.).any(2)&~hit&~neg_previous
    newz=(actual>=0)&(actual!=hp)&~neg_actual
    h=project(actual,state,c,counter,bb,release,sustain,newz)
    projected_r=project(q,state,c,counter,bb,release,sustain,newz)
    zreset=newz&~sustain&(h['silence']>0)
    for key,field in (('H','actual_hold'),('HR','instantaneous'),('S','circuit'),('SG','circuit_pool'),
                      ('NAV','nav'),('SINCE','since_post'),('SIL','silence_post'),('TGT','tgt'),('EST','est'),('TURN','turn')):
        expected=state[field][:,:,0] if key=='SG' else state[field]
        if key=='HR' and label.endswith('/Fly'):expected=state['actual_hold']
        numeric_same(output[key],expected,label+' state/output wiring '+key)
    for key,field in (('nav','nav'),('since_post','since'),('silence_post','post_silence'),('tgt','tgt')):
        same(state[key],h[field],label+' actual projection '+key)
    same(output['SUS'],sustain,label+' N2 sustain')
    same(output['Z'],zreset,label+' N2 zreset')
    same(output['P2'],h['presence'],label+' actual presence')
    same(output['PRES'],h['presence'][t,ri,v[None,:]],label+' valued presence')
    same(output['VAL'],h['val'],label+' actual value output')
    numeric_same(output['dwell'],output['AT2'].sum(0).astype(float),label+' dwell rows')
    numeric_same(output['contacts'],output['C'].sum(0).astype(float),label+' contact rows')
    expected_at=np.linalg.norm(output['POS'][:,:,None,:]-output['src'][None,:,:,:],axis=3)<c['HIT_R']
    same(output['AT2'],expected_at,label+' source arrival wiring')
    return h,projected_r


def plume_draw(output,state,draw,c,label,original=False):
    require(set(draw)=={'D_uniforms','D_probabilities','raw_whiffs'},label+' draw keyset')
    steps,rows=state['actual_hold'].shape;t=np.arange(steps)[:,None];r=np.arange(rows)[None,:];b=1-output['good'][None,:]
    source=output['src'][np.arange(rows),1-output['good']]
    along=state['position'][:,:,0]-source[None,:,0];cross=np.abs(state['position'][:,:,1]-source[None,:,1])
    cone=(along>0)&(along<c['LMAX'])&(cross<c['W0']+c['SLOPE']*along)
    near=np.linalg.norm(state['position']-source[None,:,:],axis=2)<3.
    probability=np.full((steps,rows),.03) if original else (cone|near)*.3*np.exp(-np.maximum(along,0.)/c['LAM'])
    same(draw['D_probabilities'],probability,label+' exact pre-move D probability')
    u=draw['D_uniforms']
    require(u.shape==(steps,rows) and u.dtype==np.float64 and np.isfinite(u).all() and ((u>=0)&(u<1)).all(),label+' complete uniform draws')
    same(state['whiffs'][:,:,2],u<probability,label+' independent D threshold')
    raw=draw['raw_whiffs'];require(raw.shape==(steps,rows,2) and raw.dtype==bool,label+' raw source draws')
    same(state['whiffs'][t,r,b],raw[t,r,b],label+' unmasked B input')
    same(state['whiffs'][t,r,output['good'][None,:]],np.zeros((steps,rows),bool),label+' V masked after raw draw')


def physical_scores(output):
    rows=len(output['good']);plus=output['plus_y'];index=np.arange(rows)
    at=output['AT2'];first=np.where(at.any(0),at.argmax(0),10**9)
    reached=at.any((0,2));which=np.where(reached,first.argmin(1),-1)
    dwell=output['dwell'];higher=dwell[index,plus]>dwell[index,1-plus]
    return dict(first_plus_y=int((which==plus).sum()),first_source_absent=int((which<0).sum()),
                dwell_majority_plus_y=int(higher.sum()),dwell_ties=int((dwell[:,0]==dwell[:,1]).sum()),
                source_index_zero_first=int((which==0).sum()),denominator_rows=rows)


def preflight(root):
    pins=read(root/EXECUTION)
    runtime=dict(python='3.13.12',numpy='2.5.3',threads=1)
    require(pins.get('complete') is True and pins.get('runtime')==runtime,'execution manifest incomplete/runtime mismatch')
    required={FINAL,CONFIG,REGISTRATION,'tools/replay_hold_e1.py','tests/test_hold_e1.py',
              'tools/replay_hold_stage1.py','tools/verify_seed_scan_r2.py',
              'config/seed-scan-exceptions-r2.json','experiments/module/identity.json'}
    required|={p.relative_to(root).as_posix() for p in (root/'src').glob('*.py')}
    files=pins.get('files_sha256_alpha',{})
    require(required<=files.keys(),'measurement source pin closure incomplete')
    for name,expected in files.items():
        path=(root/name).resolve()
        require(path.is_relative_to(root.resolve()) and path.is_file(),'pin path outside repository or absent')
        require(digest(path.read_bytes())==expected,'measurement source/registration digest mismatch: '+name)
    config=read(root/CONFIG);registration=read(root/REGISTRATION);pair=config.get('screen')
    require(isinstance(pair,list) and len(pair)==2 and all(type(x) is int and x>=0 for x in pair) and pair[0]!=pair[1],'canonical pair malformed')
    numbers=[pair[0],pair[1],pair[0]+10000,pair[0]+30000,pair[1]+20000,pair[1]+30000]
    repo=registration.get('repository_scan',{});graph=registration.get('graph_scan',{});queries=graph.get('queries',[])
    require(registration.get('complete') is True and repo.get('passed') is True and graph.get('passed') is True,'registration scans incomplete')
    require(registration.get('config')==CONFIG and registration.get('role')=='screen' and registration.get('numbers')==numbers and
            repo.get('numbers')==numbers and repo.get('hits')==[] and repo.get('errors')==[] and repo.get('prior_stage2_roles_disjoint') is True and
            [q.get('number') for q in queries]==numbers and
            all(q.get('executed') is True and q.get('literal_hit') is False and q.get('error') is None and q.get('keyword_rows')==0 for q in queries) and
            registration.get('runtime')==runtime and registration.get('simulation_performed') is False,'base/derived seed registration receipt mismatch')
    historical=read(root/'experiments/module/identity.json')['B2']['L2']['names']
    require(historical==dict(common=list(COMMON),ref_only=list(LINEAGE_ONLY),cand_only=[]),'historical explicit L2 contract mismatch')
    return pair,digest((root/EXECUTION).read_bytes())


def provenance_check(provenance,pin_hash,smoke):
    require(provenance.get('python')=='3.13.12' and provenance.get('numpy')=='2.5.3' and
            provenance.get('execution_pins_sha256_alpha')==pin_hash and provenance.get('smoke') is smoke and
            provenance.get('threads')=={k:'1' for k in THREADS} and isinstance(provenance.get('platform'),str),'saved runtime/provenance mismatch')


def load_evidence(directory,identity):
    descriptor=identity.get('raw_arrays',{});path=(directory/descriptor.get('path','')).resolve()
    require(path.is_relative_to(directory.resolve()) and path.name=='raw.npz.ap' and path.is_file(),'raw evidence path invalid')
    payload=path.read_bytes()
    require(digest(payload)==descriptor.get('sha256_alpha'),'whole raw evidence digest mismatch')
    require(re.fullmatch(rb'[a-p]+',payload) is not None and len(payload)%2==0,'raw evidence encoding malformed')
    require(descriptor.get('encoding')=='NPZ compressed; hex nibble a-p maps to 0-f','raw evidence encoding declaration')
    with np.load(io.BytesIO(bytes.fromhex(payload.decode('ascii').translate(HEX))),allow_pickle=False) as archive:
        require(len(archive.files)==len(set(archive.files)),'duplicate archive key')
        arrays={key:archive[key] for key in archive.files}
    require(descriptor.get('keys')==sorted(arrays) and set(descriptor.get('arrays',{}))==set(arrays),'raw key manifest mismatch')
    for key,value in arrays.items():
        require(value.dtype.kind!='O','pickled/object evidence forbidden')
        check_descriptor(value,descriptor['arrays'][key],key)
    return arrays


def check_hashes(values,n,label):
    require(isinstance(values,list) and len(values)==n and all(isinstance(x,str) and re.fullmatch('[a-p]{64}',x) for x in values),label+' hash count/encoding')


def audit_check(record,state,l2,steps,label):
    audit=record['audit']
    for key in ('creation','construction','final'):check_hashes(audit.get(key),11,label+' '+key)
    if 'balance' in audit:require(audit['balance'] is True,label+' construction balance')
    phases=audit.get('phases',[])
    require(len(phases)==steps,label+' complete RNG phases')
    previous=audit['construction']
    changes={'sense':{0},'wind':{0},'D':{4},'twin':{2},'act':{5,6},'bump':set()}
    events=record.get('rng_events',[])
    require(len(events)==steps*2,label+' complete RNG events')
    inputs=record.get('input_digests',[]);returns=record.get('return_digests',[])
    check_hashes(inputs,steps,label+' inputs');check_hashes(returns,steps,label+' returns')
    for t,phase in enumerate(phases):
        require(set(phase)=={'before',*changes},label+' RNG checkpoint keyset')
        check_hashes(phase['before'],11,label+' before')
        require(phase['before']==previous,label+' inter-step generator continuity')
        for key,allowed in changes.items():
            now=phase[key];check_hashes(now,11,label+' '+key)
            changed={i for i in range(11) if now[i]!=previous[i]}
            require(changed==allowed,label+' unexpected draw roles at '+key)
            previous=now
            if key in ('twin','act','bump'):require(now[0]==now[2],label+' untouched world/twin draw equality')
        require(events[2*t]==phase['act'] and events[2*t+1]==phase['bump'],label+' RNG event/phase wiring')
        expected_input=digest(b''.join(snapshot_blob(state[k][t]) for k in ('whiffs','wind_on','heading','rotation')))
        expected_return=digest(b''.join(snapshot_blob(state[k][t]) for k in ('turn','actual_hold')))
        require(inputs[t]==expected_input and returns[t]==expected_return,label+' raw input/return digest wiring')
        for event in (2*t,2*t+1):
            for name in ('rng','sel.rng','ring.rng','mb.rng'):
                require(l2[name][event]==events[event][5],label+' agent generator state wiring '+name)
            require(l2['sel.rng3'][event]==events[event][6],label+' third generator state wiring')
    require(audit['final']==previous,label+' final RNG continuation')
    return {k:audit[k] for k in ('creation','construction','phases','final')}


def l2_check(l2,steps,lineage,label):
    fields=set(COMMON)|(set(LINEAGE_ONLY) if lineage else set())
    require(set(l2)==fields|{'event_kind'},label+' explicit L2 field set')
    same(l2['event_kind'],np.array(['act','bump']*steps),label+' every act and bump')
    for key in fields:
        require(l2[key].shape==(steps*2,) and l2[key].dtype.kind=='U' and all(re.fullmatch('[a-p]{64}',str(x)) for x in l2[key]),label+' L2 hash column '+key)


def gate_l2(gate,a,b,steps,lineage=False,same_lineage=False):
    names=sorted(set(COMMON)|set(LINEAGE_ONLY)) if same_lineage else list(COMMON)
    expected=dict(passed=True,first=None,events=steps*2,
                  names=dict(common=names,ref_only=list(LINEAGE_ONLY) if lineage else [],cand_only=[]))
    require(gate==expected,'saved L2 gate contract/count/value mismatch')
    for name in names:same(a[name],b[name],'zero-tolerance L2 '+name)


def base_evidence(arrays,records,label,c,rows,steps):
    require(label in records,'raw record absent: '+label)
    record=records[label];require(set(record)=={'output_metadata','audit','input_digests','return_digests','rng_events'},label+' raw record keyset')
    output=group(arrays,label+'/output/');state=group(arrays,label+'/state/');l2=group(arrays,label+'/L2/')
    metadata=record['output_metadata']
    require(metadata.get('steps')==steps and metadata.get('draws_equal') is True and metadata.get('rng_equal') is True,label+' output sampling/draw identity')
    require(metadata.get('world')=='W1',label+' original masked world')
    h,r=numeric_snapshot(output,state,c,rows,steps,label)
    # These hashes are recorded independently of observer snapshots. Rebuild
    # every available dynamic state column at both events, including the wall
    # update, so an equally corrupted pair cannot pass by hash equality alone.
    dynamic={'bb':'bb','burst':'burst','c':'counter_post','est':'est','known':'known',
             'last_turn':'turn','nav_hit':'nav','present':None,'sel.s':'circuit','sel.S':'circuit_pool',
             'silence':'silence_post','since':'since_post','tgt':'tgt','up.P':'upstream_post',
             'w2':'w2','due_timeout':'timeout','due_evidence':'evidence','cast_sign':'cast_sign','flee_side':'flee_side'}
    for field,source in dynamic.items():
        values=h['presence'] if source is None else state[source]
        for t in range(steps):
            for event in (0,1):
                value=values[t]
                if event==1 and field=='cast_sign':value=value*np.where(output['C'][t],-1.,1.)
                if event==1 and field=='flee_side':value=np.where(output['C'][t],(value+180.)%360.,value)
                require(l2[field][2*t+event]==digest(snapshot_blob(value)),label+' dynamic L2 snapshot '+field)
    for t in range(steps):
        require(l2['t16'][2*t]==l2['t16'][2*t+1]==digest(snapshot_blob(t+1)),label+' L2 burst clock')
    passive=label.endswith('/Passive')
    require(set(state)==STATE_KEYS|({'release'} if passive else set()),label+' exact observer state fields')
    l2_check(l2,steps,label.startswith('H0/') or label.endswith('/Lineage'),label)
    audit=audit_check(record,state,l2,steps,label)
    draw=group(arrays,label+'/draw/')
    if label!='H0/reference':plume_draw(output,state,draw,c,label,original=label.startswith('H0/'))
    else:require(not draw,label+' reference has no reconstructed D draws')
    return dict(output=output,state=state,l2=l2,metadata=metadata,audit=audit,h=h,r=r,record=record)


def h0_check(identity,arrays,c):
    records=identity['raw_records'];a=base_evidence(arrays,records,'H0/reference',c,40,200);b=base_evidence(arrays,records,'H0/candidate',c,40,200)
    require(set(a['metadata'])==set(b['metadata']),'H0 complete metadata keysets')
    for key in a['output']:same(a['output'][key],b['output'][key],'H0 complete output '+key)
    for key in set(a['metadata'])-LABELS:require(a['metadata'][key]==b['metadata'][key],'H0 metadata '+key)
    require(a['audit']==b['audit'] and a['record']['rng_events']==b['record']['rng_events'],'H0 generator identity every phase')
    require(a['record']['input_digests']==b['record']['input_digests'] and a['record']['return_digests']==b['record']['return_digests'],'H0 agent input/return identity')
    gate=identity['gates']['H0']
    gate_l2(gate['L2'],a['l2'],b['l2'],200,same_lineage=True)
    all_fields=set(a['output'])|set(a['metadata'])-LABELS
    require(gate.get('all_output_fields')=={k:True for k in all_fields} and gate.get('complete_output_keysets') is True and
            gate.get('all_generator_events_equal') is True and gate.get('passed') is True and gate.get('first_mismatch') is None and
            gate.get('rows')==40 and gate.get('steps')==200 and gate.get('ignored_label_metadata')==sorted(LABELS) and
            gate.get('seeds')=='module_identity.seeds_of(h28, smoke=True)','H0 saved gate mismatch')
    return dict(passed=True,rows=40,steps=200,all_output_fields=len(all_fields),L2_fields=len(COMMON)+len(LINEAGE_ONLY),RNG_generators=11,RNG_checkpoints=200*7)


def pair_check(gate,a,b,lineage):
    for key in L1:same(a['output'][key],b['output'][key],'zero-tolerance L1 '+key)
    gate_l2(gate['L2'],a['l2'],b['l2'],600,lineage=lineage)
    sa,sb=w1_scores(a['output']),w1_scores(b['output']);compare_tree(sa,sb,'complete L3')
    require(gate.get('L1')=={k:True for k in L1} and gate.get('L3')=={k:True for k in sa},'saved L1/L3 gate keyset/value mismatch')
    require(a['audit']==b['audit'] and a['record']['rng_events']==b['record']['rng_events'],'pair generator equality')
    for key in ('input_digests','return_digests'):require(a['record'][key]==b['record'][key],'pair '+key+' equality')
    for key in ('passed','all_rng_event_states_equal','input_return_equal','construction_draws_balance','complete_sample','instantaneous_record_wiring','actual_projection_matches'):
        require(gate.get(key) is True,'saved identity gate '+key)
    require(gate.get('first_projection_error')==[] and gate.get('first_mismatch') is None,'saved first-mismatch receipt')


def exposed_reading(arrays,label,evidence,stored):
    h,r=evidence['h'],evidence['r'];state=evidence['state'];output=evidence['output'];steps,rows=h['identity'].shape
    for arm,expected in (('H',h),('R',r)):
        raw=group(arrays,label+'/projection/'+arm+'/')
        require(set(raw)==set(ORDER),'projection field set')
        for field in ORDER:same(raw[field],expected[field],'independent '+arm+' projection '+field)
    masks={field:(h[field]!=r[field]).reshape(steps,rows,-1).any(2) for field in ORDER}
    recorded=group(arrays,label+'/mask/');require(set(recorded)==set(ORDER),'projection mask field set')
    first=np.full((steps,rows),-1,int);downstream=first.copy()
    for index,field in enumerate(ORDER):
        same(recorded[field],masks[field],'derived projection mask '+field)
        first[(first<0)&masks[field]]=index
        if index>0:downstream[(downstream<0)&masks[field]]=index
    route=routes(h,r,state,output['good'],evidence['constants'],state['burst'],state['bb'])
    route.update(boundary=output['C'],boundary_command=route['command']&output['C'])
    saved_route=group(arrays,label+'/route/');require(set(saved_route)==set(route),'route mask keyset')
    for key,value in route.items():same(saved_route[key],value,'independent route '+key)
    lost=lost_original(output['W']);command=route['command'];counts=command.sum(0);first_command=first_true(command)
    summary=group(arrays,label+'/summary/')
    expected=dict(lost=lost,command_counts_per_row=counts,first_command_step=first_command,first_expression=first,first_downstream_expression=downstream)
    require(set(summary)==set(expected),'per-row summary keyset')
    for key,value in expected.items():same(summary[key],value,'independent row summary '+key)
    denominator=int(route['T1_T4'].sum());numerator=int(route['T1_T5'].sum())
    reading=dict(command_exposure=mask_metric(command),lost_rows=int(lost.sum()),route={k:mask_metric(v) for k,v in route.items()},
                 identity_split_denominator=denominator,f_id=None if denominator==0 else float(numerator/denominator),
                 first_expression_names=list(ORDER),lost_definition='no original-source whiff in last200 steps; D excluded')
    require(stored==reading,'saved exposure aggregation mismatch')
    return dict(**reading,command_counts_per_row=counts.tolist(),first_command_step=first_command.tolist(),lost_per_row=lost.tolist(),
                route_counts_per_row={k:v.sum(0).tolist() for k,v in route.items()},route_first_steps={k:first_true(v).tolist() for k,v in route.items()},
                expression_counts_per_row={k:v.sum(0).tolist() for k,v in masks.items()},
                physical_plus_y=physical_scores(output),
                target_difference=mask_metric(masks['tgt']),nav_difference=mask_metric(masks['nav']),
                target_diff_command_equal=mask_metric(masks['tgt']&~command),
                command_definition='exact wrapped angle gain and clamp before motor noise; target/nav differences are reported separately')


def verify(directory,root=ROOT,smoke=False):
    require(__debug__ and not sys.flags.optimize,'verification requires assertions enabled')
    require(sys.version.split()[0]=='3.13.12' and np.__version__=='2.5.3','independent numerical runtime mismatch')
    pair,pin_hash=preflight(root);identity=read(directory/'identity.json')
    require(identity.get('complete') is True and identity.get('passed') is True,'identity receipt incomplete or failed')
    provenance_check(identity['provenance'],pin_hash,smoke)
    arrays=load_evidence(directory,identity);c=source_constants(root)
    labels={'H0/reference','H0/candidate'}|({f'{condition}/{kind}' for condition in ('B4','B5') for kind in ('Lineage','Fly','Passive')} if not smoke else set())
    require(set(identity.get('raw_records',{}))==labels,'complete raw record label set')
    require(set(identity.get('gates',{}))==({'H0'} if smoke else {'H0','B4','B5'}),'identity gate set')
    require({key.split('/')[0]+'/'+key.split('/')[1] for key in arrays}==labels,'archive label set')
    for label in labels:
        categories={key[len(label)+1:].split('/')[0] for key in arrays if key.startswith(label+'/')}
        expected={'output','state','L2'}|({'draw'} if label!='H0/reference' else set())|({'projection','mask','route','summary'} if label.endswith('/Passive') else set())
        require(categories==expected,'raw evidence category closure '+label)
    result=dict(complete=True,passed=True,read_only_evidence=True,simulation_performed=False,fresh_random_draws=False,
                execution_pins_sha256_alpha=pin_hash,verifier_sha256_alpha=digest(Path(__file__).read_bytes()),
                evidence_sha256_alpha={name:digest((directory/name).read_bytes()) for name in ('identity.json','raw.npz.ap')},
                H0=h0_check(identity,arrays,c))
    if smoke:return result
    canonical=root/'experiments/hold/hold_e1_smoke'
    prior=read(canonical/'identity.json');require(prior.get('complete') is True and prior.get('passed') is True,'prior canonical H0 incomplete')
    provenance_check(prior['provenance'],pin_hash,True);prior_arrays=load_evidence(canonical,prior)
    result['prior_canonical_H0']=h0_check(prior,prior_arrays,c)
    result['canonical_H0_sha256_alpha']=digest((canonical/'identity.json').read_bytes())
    pair_key=digest(json.dumps(pair,separators=(',',':')).encode('ascii'));claim_path=root/'experiments/hold/hold_e1_registry'/(pair_key+'.claim');claim=read(claim_path)
    require(claim.get('screen_pair_sha256_alpha')==pair_key and claim.get('provenance_sha256_alpha')==digest(json.dumps(identity['provenance'],sort_keys=True).encode()) and
            claim.get('execution_pins_sha256_alpha')==pin_hash and claim.get('output_path_sha256_alpha')==digest(str(directory.resolve()).encode()) and claim.get('complete') is False,'durable global screen claim mismatch')
    result['claim_sha256_alpha']=digest(claim_path.read_bytes())
    exposure=read(directory/'exposure.json');require(exposure.get('complete') is True,'exposure incomplete')
    require(exposure.get('provenance')==identity['provenance'] and exposure.get('raw_arrays')==identity['raw_arrays'],'exposure/identity provenance mismatch')
    require(set(exposure.get('readings',{}))=={'B4','B5'},'exposure condition set')
    readings={}
    for condition in ('B4','B5'):
        all_evidence={kind:base_evidence(arrays,identity['raw_records'],condition+'/'+kind,c,400,600) for kind in ('Lineage','Fly','Passive')}
        gates=identity['gates'][condition];require(set(gates)=={'lineage_to_fly','fly_to_passive'},condition+' pair gate set')
        pair_check(gates['lineage_to_fly'],all_evidence['Lineage'],all_evidence['Fly'],True)
        pair_check(gates['fly_to_passive'],all_evidence['Fly'],all_evidence['Passive'],False)
        passive=all_evidence['Passive'];passive['constants']=c
        readings[condition]=exposed_reading(arrays,condition+'/Passive',passive,exposure['readings'][condition])
    flags=dict(X1=True,X2=readings['B5']['command_exposure']['rows']>=1,X3=readings['B4']['command_exposure']['rows']>=40,X4=20<=readings['B4']['lost_rows']<=380)
    require(exposure.get('screen')==flags,'registered screen thresholds mismatch')
    reached=readings['B4']['command_exposure']['rows']
    verdict=('READABLE FOR SEPARATE BENEFIT DESIGN' if all(flags.values()) else
             'BLOCKED: positive control did not expose a command branch' if not flags['X2'] else
             'UNREADABLE: loss-range criterion failed' if not flags['X4'] else
             'NOT REACHED IN THIS SAMPLE' if reached==0 else 'REACHED, BELOW REGISTERED SCREEN')
    require(exposure.get('verdict')==verdict and exposure.get('interpretation')=='same-state passive exposure; no free-running benefit or power finding','screen interpretation mismatch')
    result.update(readings=readings,screen=flags,verdict=verdict,interpretation=exposure['interpretation'])
    result['evidence_sha256_alpha']['exposure.json']=digest((directory/'exposure.json').read_bytes())
    require(preflight(root)==(pair,pin_hash),'measurement provenance changed during verification')
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path,help='existing saved evidence directory')
    parser.add_argument('--smoke',action='store_true',help='verify saved spent H0 only')
    parser.add_argument('--receipt',type=Path,help='independent receipt path; default existing output/verification.json')
    args=parser.parse_args();directory=args.output.resolve()
    result=verify(directory,smoke=args.smoke)
    target=args.receipt or directory/'verification.json';target=target.resolve()
    require(target.is_relative_to((ROOT/'experiments/hold').resolve()) and
            (target.name=='verification.json' or target.name.endswith('_verification.json')),
            'independent receipt must be a verification JSON under experiments/hold')
    payload=(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n').encode('utf-8')
    no_protected_tokens(payload,ROOT)
    temporary=target.with_name(target.name+'.tmp')
    with temporary.open('xb') as stream:stream.write(payload)
    temporary.replace(target)
    print('Independent saved E1 evidence PASS; '+('H0 only' if args.smoke else result['verdict']))
    return 0


if __name__=='__main__':
    try:sys.exit(main())
    except (VerificationError,OSError,ValueError,KeyError,TypeError) as error:
        print('E1 independent evidence verification FAIL: '+str(error),file=sys.stderr)
        sys.exit(1)
