#!/usr/bin/env python3
"""Independent R0 evidence arithmetic. Imports only stdlib and NumPy.

No controller, trajectory harness, or random generator is imported or run.
"""
import argparse
import ast
from collections import OrderedDict
from collections.abc import Mapping
import hashlib
import importlib
import io
import json
import math
import os
from pathlib import Path
import platform
import re
import sys
import struct
import tempfile
import zipfile
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
FINAL = 'experiments/h17/h17_r0_design_v2.md'
CONFIG = 'config/h17-r0-seeds.json'
REGISTRATION = 'experiments/h17/h17_r0_seed_registration.json'
PINS = 'config/h17-r0-execution-pins.json'
AP = str.maketrans('0123456789abcdef', 'abcdefghijklmnop')
HEX = str.maketrans('abcdefghijklmnop', '0123456789abcdef')
CONDITIONS = ('C0', 'T1', 'W1', 'T3')
ARMS = ('Fly', 'Passive', 'Agent17')
SAMPLE_FIELDS=tuple(('PRE_POS PRE_HEAD PRE_ROT H_pre H_post S_pre S_post SG_pre SG_post UP_pre UP_post Y '
 'SIL_pre SIL_base SIL_post SINCE_pre SINCE_post C_pre C_post PRES_pre PRES_post NAV TO EV '
 'base sustain negS negZ newz zreset withheld_N1_S withheld_N1_Z reset_drive EST TGT TURN cast_sign flee_side '
 'POS HEAD ROT C AT2 W_raw W_delivered source_uniforms probabilities wind_uniform wind_on turn_normal').split())
L1=('POS','HEAD','S','SG','H','NAV','SINCE','TGT','SIL','TO','EV','W','SUS','Z','AT2','C')
Z = 1.959963984540054


class VerificationError(RuntimeError):
    def __init__(self, field, index=None, phase=None):
        self.first_failure = dict(field=field, index=index, phase=phase)
        super().__init__(field)


def require(ok, field, index=None, phase=None):
    if not bool(ok):
        raise VerificationError(field, index, phase)


def digest(data):
    return hashlib.sha256(data).hexdigest().translate(AP)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True,
                      allow_nan=False).encode('utf-8')


def unique(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, 'duplicate JSON key')
        out[key] = value
    return out


def read(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique,
                      parse_constant=lambda _: (_ for _ in ()).throw(VerificationError('nonfinite JSON')))


def same(actual, expected, field, phase=None):
    a, b = np.asarray(actual), np.asarray(expected)
    require(a.shape == b.shape, field + '/shape', phase=phase)
    require(a.dtype == b.dtype, field + '/dtype', phase=phase)
    if a.tobytes(order='C') != b.tobytes(order='C'):
        # Bit comparisons also detect signed zero and differing NaN payloads.
        aa = np.frombuffer(a.tobytes(order='C'), np.uint8).reshape(a.shape + (a.dtype.itemsize,))
        bb = np.frombuffer(b.tobytes(order='C'), np.uint8).reshape(b.shape + (b.dtype.itemsize,))
        ix = np.argwhere(np.any(aa != bb, axis=-1))[0].tolist()
        raise VerificationError(field, ix, phase)


def tree_same(actual, expected, field):
    require(type(actual) is type(expected), field + '/type')
    if isinstance(expected, dict):
        require(set(actual) == set(expected), field + '/keys')
        for key in expected:
            tree_same(actual[key], expected[key], field + '/' + str(key))
    elif isinstance(expected, list):
        require(len(actual) == len(expected), field + '/length')
        for i, value in enumerate(expected):
            tree_same(actual[i], value, field + '/' + str(i))
    elif isinstance(expected, float):
        require(actual.hex() == expected.hex(), field)
    else:
        require(actual == expected, field)


def expression(node, env):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        return env[node.id]
    if isinstance(node, (ast.Tuple, ast.List)):
        value = [expression(x, env) for x in node.elts]
        return tuple(value) if isinstance(node, ast.Tuple) else value
    if isinstance(node, ast.Dict):
        return {expression(k, env): expression(v, env) for k, v in zip(node.keys, node.values)}
    if isinstance(node, ast.UnaryOp):
        value = expression(node.operand, env)
        if isinstance(node.op, ast.USub): return -value
        if isinstance(node.op, ast.UAdd): return value
    if isinstance(node, ast.BinOp):
        a, b = expression(node.left, env), expression(node.right, env)
        if isinstance(node.op, ast.Add): return a + b
        if isinstance(node.op, ast.Sub): return a - b
        if isinstance(node.op, ast.Mult): return a * b
        if isinstance(node.op, ast.Div): return a / b
        if isinstance(node.op, ast.Pow): return a ** b
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'dict' and not node.args:
        return {x.arg: expression(x.value, env) for x in node.keywords}
    raise ValueError('not a literal expression')


def constants(path):
    result = {}
    for statement in ast.parse(path.read_text(encoding='utf-8')).body:
        if not isinstance(statement, ast.Assign): continue
        for target in statement.targets:
            pairs = [(target, statement.value)]
            if isinstance(target, (ast.Tuple, ast.List)) and isinstance(statement.value, (ast.Tuple, ast.List)):
                pairs = list(zip(target.elts, statement.value.elts))
            for name, node in pairs:
                if not isinstance(name, ast.Name): continue
                try: result[name.id] = expression(node, result)
                except (ValueError, KeyError, TypeError): pass
    return result


def source_constants(root):
    out = constants(root / 'src/fly.py')
    world = constants(root / 'src/ph9.py')
    out.update({k: world[k] for k in ('W0', 'SLOPE', 'LAM', 'LMAX', 'HIT_R', 'SPEED')})
    geometry = constants(root / 'src/ph16.py')
    out.update({k: geometry[k] for k in ('SEP', 'DOWN')})
    return out


def first(mask):
    return np.where(mask.any(axis=0), mask.argmax(axis=0), -1).astype(np.int64)


def bitsets(mask, at):
    rows = np.arange(mask.shape[1])
    valid = at >= 0
    result = np.zeros(mask.shape[1], np.uint8)
    result[valid] = (mask[at[valid], rows[valid], 0].astype(np.uint8)
                     | (mask[at[valid], rows[valid], 1].astype(np.uint8) << 1))
    return result


def wilson(mask, selected=None, conditional=False):
    mask = np.asarray(mask, dtype=bool)
    selected = np.ones(mask.shape, bool) if selected is None else np.asarray(selected, dtype=bool)
    n = int(selected.sum()); k = int((mask & selected).sum())
    if not n:
        return dict(numerator=k, denominator=n, estimate=None, interval=None, status='UNDEFINED')
    p = k / n; den = 1 + Z * Z / n
    centre = (p + Z * Z / (2 * n)) / den
    half = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / den
    return dict(numerator=k, denominator=n, estimate=p, interval=[centre-half, centre+half],
                status='UNREADABLE' if conditional and n < 50 else 'READABLE')


def n2(sample, known, hold=1.0, margin=0.2):
    hp, h = sample['H_pre'], sample['H_post']
    t, r = hp.shape; rows = np.arange(r)[None, :]
    values = np.broadcast_to(known, (t, r, 2))
    pre = np.maximum(hp, 0); post = np.maximum(h, 0)
    negS = (hp >= 0) & (values[np.arange(t)[:,None], rows, pre] < 0)
    negZ = (h >= 0) & (values[np.arange(t)[:,None], rows, post] < 0)
    whiffs = sample['W_delivered']
    hit = (h >= 0) & whiffs[np.arange(t)[:,None], rows, post]
    y = sample['Y']; yy = np.arange(t)[:,None]
    TO = sample['SIL_pre'] > 40
    EV = (hp >= 0) & ((y[yy, rows, 1-pre] - y[yy, rows, pre]) > margin)
    due = TO | EV
    sil_base = np.where(hit, 0.0, np.where(due, 0.0, sample['SIL_pre']) + 1.0)
    units = (sample['S_post'] > hold).sum(axis=2)
    new = (h >= 0) & (h != hp)
    base = TO & ~EV & (units > 0) & ~hit
    sustain = base & ~negS; newz = new & ~negZ
    result = dict(hit=hit, new=new, negS=negS, negZ=negZ, TO=TO, EV=EV,
                  base=base, sustain=sustain, newz=newz,
                  zreset=newz & ~sustain & (sil_base > 0),
                  withheld_N1_S=base & negS, withheld_N1_Z=new & negZ,
                  SIL_base=sil_base,
                  SIL_post=np.where(sustain, 41.0, np.where(newz, 0.0, sil_base)),
                  reset_drive=np.where(due, 10.0, 0.0), units=units.astype(np.int64))
    empty = negS & (h == -1)
    change = negS & (h >= 0) & (h != hp)
    result.update(negative_to_unheld=empty, negative_zero_units=empty & (units == 0),
                  negative_multiple_units=empty & (units > 1),
                  negative_identity_change=change, negative_end=empty | change,
                  negative_same=negS & (h == hp),
                  neither=~TO & ~EV, timeout_only=TO & ~EV,
                  evidence_only=~TO & EV, both=TO & EV)
    return result


def observation(whiffs, reach, held, nav):
    t, r, _ = whiffs.shape
    anyw = whiffs.any(2); anya = reach.any(2)
    q = np.zeros((t, r), np.int64); clock = np.zeros(r, np.int64)
    lastw = np.full((t, r), -1, np.int64); lastnav = np.full_like(lastw, -1)
    lw = np.full(r, -1, np.int64); ln = lw.copy()
    for i in range(t):
        clock = np.where(anyw[i], 0, clock + 1); q[i] = clock
        lw = np.where(anyw[i], i, lw); ln = np.where(nav[i], i, ln)
        lastw[i] = lw; lastnav[i] = ln
    mark = (q >= 250) & (held == -1); m = first(mark); valid = m >= 0
    after = valid[None,:] & (np.arange(t)[:,None] > m[None,:])
    fw = first(anyw & after); fa = first(anya & after)
    result = dict(q_obs=q, marker_mask=mark, marker_step=m,
                  longest_silence=q.max(0), last_whiff=lastw, last_nav=lastnav,
                  first_whiff=first(anyw), first_reach=first(anya),
                  post_first_whiff=fw, post_first_reach=fa,
                  post_whiff_bits=bitsets(whiffs,fw), post_reach_bits=bitsets(reach,fa),
                  available=np.where(valid,t-1-m,-1).astype(np.int64),
                  whiff_delay=np.where(fw>=0,fw-m,-1).astype(np.int64),
                  reach_delay=np.where(fa>=0,fa-m,-1).astype(np.int64),
                  whiff_event=valid & (fw>=0), reach_event=valid & (fa>=0),
                  whiff_censored=valid & (fw<0), reach_censored=valid & (fa<0))
    result['first_whiff_bits'] = bitsets(whiffs,result['first_whiff'])
    result['first_reach_bits'] = bitsets(reach,result['first_reach'])
    result['marker_reach_bits'] = bitsets(reach,m)
    for k in (100,200,300):
        full = valid & (m+k <= t-1)
        window = after & (np.arange(t)[:,None] <= m[None,:]+k)
        result['full_'+str(k)] = full
        result['censored_'+str(k)] = valid & ~full
        result['whiff_'+str(k)] = (anyw & window).any(0) & full
        result['reach_'+str(k)] = (anya & window).any(0) & full
        for source in (0,1):
            result['whiff_'+str(k)+'_source'+str(source)] = (whiffs[:,:,source] & window).any(0) & full
            result['reach_'+str(k)+'_source'+str(source)] = (reach[:,:,source] & window).any(0) & full
    return result


def plume(position, src, c, p_hit=0.3):
    along = position[:,:,None,0] - src[None,:,:,0]
    cross = np.abs(position[:,:,None,1] - src[None,:,:,1])
    inside = ((along>0) & (along<c['LMAX']) & (cross<c['W0']+c['SLOPE']*along))
    at = np.linalg.norm(position[:,:,None,:]-src[None,:,:,:],axis=3)<3.0
    return np.where(inside|at,p_hit*np.exp(-np.maximum(along,0.0)/c['LAM']),0.0)


def array_descriptor(a):
    return dict(dtype=a.dtype.str, shape=list(a.shape), nbytes=a.nbytes,
                sha256_alpha=digest(np.ascontiguousarray(a).tobytes()))


class LazyArrays(Mapping):
    """Bounded lazy arrays; the ZIP remains on disk, not in a decoded RAM copy."""
    def __init__(self,file,keys,limit=32<<20):
        self.file=file;self.archive=np.load(file,allow_pickle=False)
        self.keys=tuple(keys);self.cache=OrderedDict();self.bytes=0;self.limit=limit
    def __iter__(self):return iter(self.keys)
    def __len__(self):return len(self.keys)
    def __getitem__(self,key):
        if key in self.cache:
            self.cache.move_to_end(key);return self.cache[key]
        require(key in self.keys,'raw/unknown key')
        a=self.archive[key]
        if a.nbytes<=self.limit:
            while self.cache and self.bytes+a.nbytes>self.limit:
                _,old=self.cache.popitem(last=False);self.bytes-=old.nbytes
            self.cache[key]=a;self.bytes+=a.nbytes
        return a
    def clear(self):self.cache.clear();self.bytes=0
    def close(self):self.archive.close();self.file.close();self.clear()


def archive_headers(z,descriptor,schema):
    names=z.namelist()
    require(len(names)==len(set(names)),'raw/duplicate zip member')
    require(all(x.endswith('.npy') for x in names),'raw/non array member')
    require({x[:-4] for x in names}==set(descriptor['arrays']),'raw/keyset')
    for name in names:
        with z.open(name) as f:
            version=np.lib.format.read_magic(f)
            require(version in ((1,0),(2,0)),'raw/unsupported NPY version')
            if version==(1,0):shape,fortran,dtype=np.lib.format.read_array_header_1_0(f)
            else:shape,fortran,dtype=np.lib.format.read_array_header_2_0(f)
            require(not dtype.hasobject and dtype.kind in 'biufUS','raw/dtype whitelist/'+name)
            key=name[:-4];pinned=schema.get(key)
            require(pinned is not None and list(shape)==pinned['shape'] and dtype.str==pinned['dtype'],'raw/pinned schema/'+key)
    return names


def load_arrays(directory, descriptor, schema):
    path=(directory/descriptor['path']).resolve()
    require(path.parent==directory.resolve() and path.name=='raw.npz.ap','raw/path')
    require(descriptor.get('encoding')=='NPZ compressed; hex nibble a-p maps to 0-f','raw/encoding declaration')
    decoded=tempfile.TemporaryFile('w+b');hasher=hashlib.sha256()
    with path.open('rb') as source:
        while payload:=source.read(1<<20):
            require(len(payload)%2==0 and re.fullmatch(rb'[a-p]+',payload) is not None,'raw/AP encoding')
            hasher.update(payload);decoded.write(bytes.fromhex(payload.decode('ascii').translate(HEX)))
    require(hasher.hexdigest().translate(AP)==descriptor['sha256_alpha'],'raw/file hash')
    decoded.seek(0)
    with zipfile.ZipFile(decoded) as z:
        names=archive_headers(z,descriptor,schema)
    decoded.seek(0);arrays=LazyArrays(decoded,[x[:-4] for x in names])
    require(descriptor.get('keys')==sorted(arrays),'raw/ordered manifest keys')
    for key in arrays:
        a=arrays[key]
        tree_same(descriptor['arrays'][key],array_descriptor(a),'raw/descriptor/'+key)
    arrays.clear()
    return arrays


def recurrence_check(sample, construction, c, label):
    """Rebuild deterministic controller arithmetic, not a trajectory."""
    whiffs = sample['W_delivered']; t, r, _ = whiffs.shape
    rows = np.arange(r)[None,:]; times = np.arange(t)[:,None]
    known = construction['known']; h = sample['H_post']; hp = sample['H_pre']
    same(sample['H_pre'][1:], sample['H_post'][:-1], label+'/hold continuity','pre')
    for name,initial in (('S',construction['S0']), ('SG',construction['SG0']),
                         ('UP',construction['UP0']), ('SIL',construction['SIL0']),
                         ('SINCE',construction['SINCE0']), ('C',construction['C0'])):
        post = sample[name+'_post']; pre = sample[name+'_pre']
        same(pre[0], initial,label+'/'+name+'/initial','construction')
        same(pre[1:],post[:-1],label+'/'+name+'/continuity','pre')
    for phase in ('pre','post'):
        active = sample['S_'+phase]>c['HOLD']
        expected = np.where(active.sum(2)==1,active.argmax(2),-1).astype(np.int64)
        same(sample['H_'+phase],expected,label+'/H_'+phase,phase)
    # Match the original in-place upstream update operation order.
    up=sample['UP_pre'].copy()
    u=np.maximum(whiffs.astype(float),0.0)**c['UP_N']
    up += (1.0/c['UP_TAU'])*(-up+u)
    same(sample['UP_post'],up,label+'/UP_post','base')
    others=(up.sum(2,keepdims=True)-up)/1
    y=c['UP_RMAX']*up/(c['UP_SIG']**c['UP_N']+up+c['UP_K']*others)
    y=y*(1.0+c['G_STAR']*np.maximum(known,0.0))
    vh=known[np.arange(r)[None,:],np.maximum(hp,0)]
    y=y*~((hp>=0)[:,:,None] & (known[None,:,:]>=0.0) & (known[None,:,:]<vh[:,:,None]))
    same(sample['Y'],y,label+'/Y','base')
    masks=n2(sample,known,c['HOLD'],c['MARGIN'])
    for key in ('TO','EV','SIL_base','SIL_post','base','sustain','negS','negZ','newz',
                'zreset','withheld_N1_S','withheld_N1_Z','reset_drive'):
        same(sample[key],masks[key],label+'/'+key,'act')
    count=np.where(whiffs,0.0,sample['C_pre']+1.0)
    same(sample['C_post'],count,label+'/C_post','base')
    override=np.zeros_like(whiffs)
    override[times,rows,np.maximum(h,0)]=h>=0
    presence=(count<200)|override
    same(sample['PRES_post'],presence,label+'/PRES_post','base')
    vmax=np.where(presence,known[None,:,:],-np.inf).max(2)
    top=presence & (known[None,:,:]>=0) & (known[None,:,:]==vmax[:,:,None])
    vh=known[rows,np.maximum(h,0)]
    keep=(h>=0)&((vh==vmax)|(vh<0))
    nav=np.where(keep,masks['hit'],(whiffs&top).any(2))
    same(sample['NAV'],nav,label+'/NAV','act')
    since=np.where(nav,0.0,sample['SINCE_pre']+1.0)
    same(sample['SINCE_post'],since,label+'/SINCE_post','act')
    side=np.where((since//c['CAST_PERIOD'])%2==0,1.0,-1.0)*sample['cast_sign']
    off=c['MAXOFF']*(1.0-np.abs((since/c['SAT'])%2.0-1.0))
    target=np.where(nav,c['UPWIND'],(c['UPWIND']+side*off)%360.0)
    val=np.where(h>=0,known[rows,np.maximum(h,0)],0.0)
    target=np.where(val<0,sample['flee_side'],target)
    same(sample['TGT'],target,label+'/TGT','act')
    angular=(target-sample['EST']+180.0)%360.0-180.0
    motor=np.clip(c['GAIN']*angular,-c['MAXTURN'],c['MAXTURN'])
    if 'turn_normal' in sample:
        same(sample['TURN'],motor+c['TURN_NOISE']*sample['turn_normal'],label+'/TURN','act')
    # Existing walls-off move arithmetic. Unit distance is a strict source test.
    head=(sample['PRE_HEAD']+sample['TURN'])%360.0
    angle=np.radians(head)
    pos=sample['PRE_POS']+c['SPEED']*np.stack([np.cos(angle),np.sin(angle)],2)
    same(sample['HEAD'],head,label+'/HEAD','move')
    same(sample['POS'],pos,label+'/POS','move')
    rot=(head-sample['PRE_HEAD']+180.0)%360.0-180.0
    same(sample['ROT'],rot,label+'/ROT','move')
    same(sample['AT2'],np.linalg.norm(pos[:,:,None,:]-construction['src'][None,:,:,:],axis=3)<c['HIT_R'],label+'/AT2','move')
    require(not sample['C'].any(),label+'/contacts','move')
    expected_p=plume(sample['PRE_POS'],construction['src'],c)
    same(sample['probabilities'],expected_p,label+'/probabilities','sense')
    uniform=sample['source_uniforms']
    require(np.isfinite(uniform).all() and ((uniform>=0)&(uniform<1)).all(),label+'/source uniforms','sense')
    same(sample['W_raw'],uniform<expected_p,label+'/raw whiffs','sense')
    wind=sample['wind_uniform']
    require(np.isfinite(wind).all() and ((wind>=0)&(wind<1)).all(),label+'/wind uniforms','wind')
    same(sample['wind_on'],wind<1.0,label+'/wind','wind')
    return masks


def circuit_ring_check(sample, construction, c, normals, label):
    """One-step evidence equations using logged noise values, never new draws."""
    t,r=sample['H_post'].shape
    require(set(normals)=={'circuit','rotation','cue','turn'},label+'/noise roles')
    same(sample['turn_normal'],normals['turn'],label+'/turn normal','act')
    initial=construction['ring0']; ring_previous=initial.copy()
    n=c['RING_N']; idx=np.arange(n)[:,None]; jdx=np.arange(n)[None,:]
    o=((idx-jdx+n//2)%n)-n//2
    ang=2*np.pi*np.arange(n)/n
    for i in range(t):
        s=sample['S_pre'][i].copy(); pool=sample['SG_pre'][i].reshape(r,1).copy()
        q=c['C_POOLC']*np.maximum(s,0.0)**c['C_POOLP']
        pool_input=q.sum(1,keepdims=True)+sample['reset_drive'][i,:,None]
        pool+=(c['C_DT']/c['C_TAUG'])*(-pool+pool_input)
        sig=1.0/(1.0+np.exp(-np.clip(c['C_K']*(s-c['C_THETA']),-c['SIG_CLIP'],c['SIG_CLIP'])))
        u=(sample['Y'][i]+c['C_G']*sig+c['C_WI']*q-c['C_WI']*pool+c['C_NOISE']*normals['circuit'][i])
        s+=(c['C_DT']/c['C_TAU'])*(-s+np.clip(u,0,c['C_SMAX']))
        same(sample['S_post'][i],s,label+'/circuit S','base')
        same(sample['SG_post'][i].reshape(r,1),pool,label+'/circuit pool','base')
        def ringstep(previous,rotation,noise,cue=None):
            delta=np.asarray(c['RING_VGAIN']*rotation*n/360.0,dtype=float).reshape(-1,1,1)
            oo=((o[None,:,:]-delta+n/2)%n)-n/2
            weight=c['RING_J']*np.exp(-0.5*(oo/c['RING_WIDTH'])**2)
            exc=np.einsum('rij,rj->ri',weight,previous)+c['RING_NOISE']*noise
            if cue is not None:exc=exc+cue
            e=np.maximum(exc,0.0)**c['RING_P']
            result=c['RING_RMAX']*e/(c['RING_SIGMA']**c['RING_P']+c['RING_C']*e.mean(1,keepdims=True))
            return previous+(c['RING_DT']/c['RING_TAU'])*(-previous+result)
        ring=ringstep(ring_previous,sample['PRE_ROT'][i],normals['rotation'][i])
        center=(sample['PRE_HEAD'][i]/360.0*n).reshape(-1,1)
        distance=np.abs(np.arange(n)[None,:]-center);distance=np.minimum(distance,n-distance)
        cue=c['WIND_CUE']*np.exp(-0.5*(distance/c['CUE_WIDTH'])**2)*sample['wind_on'][i,:,None]
        ring=ringstep(ring,0.0,normals['cue'][i],cue)
        if 'RING_post' in sample:same(sample['RING_post'][i],ring,label+'/ring','act')
        estimate=np.degrees(np.angle((ring*np.exp(1j*ang)).sum(1)))%360.0
        same(sample['EST'][i],estimate,label+'/estimate','act')
        ring_previous=ring
    return ring_previous


def metric_reading(condition, sample, construction, masks):
    w=sample['W_delivered']; at=sample['AT2']; h=sample['H_post']; nav=sample['NAV']
    t,r,_=w.shape
    obs=observation(w,at,h,nav)
    valid=obs['marker_step']>=0
    lost=~w[-200:].any((0,2))
    reading=dict(primary=wilson(w[:300].any((0,2)) if condition=='C0' else lost),
                 any_whiff_600=wilson(w.any((0,2))), reach_600=wilson(at.any((0,2))),
                 lost_last200=wilson(lost), markers=wilson(valid), no_marker=wilson(~valid),
                 horizon_whiff=wilson(obs['whiff_event'],valid,True),
                 horizon_reach=wilson(obs['reach_event'],valid,True),
                 marker_baseline_reach=wilson(obs['marker_reach_bits']!=0,valid,True),
                 windows={}, sources={}, transitions={}, cells={})
    for k in (100,200,300):
        selected=obs['full_'+str(k)]
        reading['windows'][str(k)]=dict(full=int(selected.sum()),censored=int(obs['censored_'+str(k)].sum()),
            whiff=wilson(obs['whiff_'+str(k)],selected,True),reach=wilson(obs['reach_'+str(k)],selected,True),
            sources={str(s):dict(whiff=wilson(obs['whiff_'+str(k)+'_source'+str(s)],selected,True),
                                reach=wilson(obs['reach_'+str(k)+'_source'+str(s)],selected,True)) for s in (0,1)})
    for source in (0,1):
        reading['sources'][str(source)]={}
        for window,lo in (('full',0),('last200',t-200)):
            count=at[lo:,:,source].sum(0,dtype=np.int64)
            obs['dwell_'+window+'_source'+str(source)]=count
            reading['sources'][str(source)][window]=dict(whiff=wilson(w[lo:,:,source].any(0)),
                reach=wilson(at[lo:,:,source].any(0)), dwell_mean=float((count/(t-lo)).mean()),
                dwell_count=int(count.sum()),row_denominator=r,step_denominator=t-lo)
    for key in ('negative_to_unheld','negative_zero_units','negative_multiple_units','negative_identity_change',
                'negative_end','negative_same','base','sustain','zreset','withheld_N1_S','withheld_N1_Z'):
        mask=masks[key]
        item=dict(events=int(mask.sum()), incidence=wilson(mask.any(0)), concurrence={})
        for name in ('neither','timeout_only','evidence_only','both'):
            concurrent=mask&masks[name]
            item['concurrence'][name]=dict(events=int(concurrent.sum()),rows=int(concurrent.any(0).sum()))
        reading['transitions'][key]=item
    for cell in range(4):
        select=construction['cell']==cell
        reading['cells'][str(cell)]=dict(rows=int(select.sum()),
            primary=wilson(w[:300].any((0,2)) if condition=='C0' else lost,select),
            lost_last200=wilson(lost,select),markers=wilson(valid,select))
    reading['contacts']=dict(events=int(sample['C'].sum()),rows=int(sample['C'].any(0).sum()))
    choices={'unheld':h<0,'nav':nav}
    for source in (0,1):
        choices['held_source'+str(source)]=h==source
        choices['nav_source'+str(source)]=nav&w[:,:,source]
        choices['held_nav_source'+str(source)]=nav&(h==source)
    reading['choices']={name:dict(events=int(mask.sum()),rows=int(mask.any(0).sum())) for name,mask in choices.items()}
    known=construction['known']; values=known[np.arange(r)[None,:],np.maximum(h,0)]
    reading['transitions']['negative_identity_change']['new_value_sign']={name:dict(events=int((masks['negative_identity_change']&selected).sum()),
        rows=int((masks['negative_identity_change']&selected).any(0).sum()))
        for name,selected in (('positive',values>0),('zero',values==0),('negative',values<0))}
    reading['transitions']['negative_identity_change']['new_identity']={str(source):dict(
        events=int((masks['negative_identity_change']&(h==source)).sum()),
        rows=int((masks['negative_identity_change']&(h==source)).any(0).sum())) for source in (0,1)}
    obs['lost_last200']=lost
    return obs,reading


def preflight(root):
    pins=read(root/PINS)
    require(pins.get('complete') is True,'pins/incomplete')
    files=pins.get('files_sha256_alpha',{})
    closure=digest(canonical({key:pins[key] for key in ('runtime','schema','files_sha256_alpha')}))
    require(pins.get('source_closure_sha256_alpha')==closure,'pins/source closure digest')
    required={FINAL,CONFIG,REGISTRATION,'config/h17-r0-execution-opening.json',
              'notes/reviews/2026-10-09-h17-r0-execution-review.md',
              'tools/h17_r0_recording.py','tools/replay_hold_stage1.py',
              'tools/verify_seed_scan_r2.py','config/seed-scan-exceptions-r2.json',
              'tools/measure_h17_r0.py','tools/verify_h17_r0.py',
              'tests/test_h17_r0.py','tests/test_verify_h17_r0.py',
              'experiments/module/identity.json'}
    required|={p.relative_to(root).as_posix() for p in (root/'src').glob('*.py')}
    require(required==set(files),'pins/source closure')
    schema=pins['schema'];history=read(root/'experiments/module/identity.json')['A1']['L2']['names']
    require(schema['version']=='h17-r0-evidence-v2' and schema['conditions']==list(CONDITIONS)
            and schema['arms']==list(ARMS) and schema['sample_fields']==list(SAMPLE_FIELDS)
            and schema['main_rows']==400 and schema['smoke_rows']==40 and schema['steps']==600
            and schema['dtype_kinds']=='biufUS' and schema['snapshot_exclusions']==['act','bump'], 'pins/schema')
    fieldsets={'Fly':sorted(history['common']+history['cand_only']),
               'Passive':sorted(history['common']+history['cand_only']),
               'Agent17':sorted(history['common']+history['ref_only'])}
    tree_same(schema['fieldsets'],fieldsets,'pins/lineage fieldsets')
    runtime=pins['runtime']
    tree_same(runtime,runtime_stamp(),'actual runtime vs pins')
    require(runtime.get('python')=='3.13.12' and runtime.get('numpy')=='2.5.3' and runtime.get('implementation')=='CPython'
            and runtime.get('pointer_bits')==64 and runtime.get('byteorder')=='little' and runtime.get('processes')==1
            and runtime.get('optimize')==0 and runtime.get('assertions_enabled') is True
            and set(runtime['threads'])=={'OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'}
            and all(x=='1' for x in runtime['threads'].values())
            and str(runtime.get('platform','')).lower().startswith('windows'), 'pins/runtime')
    for pathkey,hashkey in (('executable','executable_sha256_alpha'),('numpy_path','numpy_init_sha256_alpha')):
        require(digest(Path(runtime[pathkey]).read_bytes())==runtime[hashkey],'pins/runtime binary/'+pathkey)
    require(set(runtime['native_libraries'])=={'numpy._core._multiarray_umath','numpy.random._generator'},'pins/native library keyset')
    for name,entry in runtime['native_libraries'].items():
        require(digest(Path(entry['path']).read_bytes())==entry['sha256_alpha'],'pins/native binary/'+name)
    check_source_files(root,files)
    config=read(root/CONFIG); reg=read(root/REGISTRATION); pair=config.get('measurement')
    require(isinstance(pair,list) and len(pair)==2 and all(type(x) is int and x>=0 for x in pair) and pair[0]!=pair[1],'config/pair')
    w,a=pair; numbers=[w,a,w+10000,w+20000,a+20000]
    scan=reg.get('local_scan',{}); graph=reg.get('graph_scan',{})
    require(reg.get('complete') is True and reg.get('config')==CONFIG and reg.get('config_key')=='measurement'
            and reg.get('numbers')==numbers and scan.get('numbers')==numbers,'registration/numbers')
    require(scan.get('passed') is True and scan.get('hits')==[] and scan.get('errors')==[]
            and scan.get('prior_hold_roles_disjoint') is True and scan.get('exclusions')==['.git','__pycache__'], 'registration/repository')
    queries=graph.get('queries',[])
    require(graph.get('passed') is True and [q.get('number') for q in queries]==numbers and
            all(q.get('executed') is True and q.get('error') is None and q.get('literal_hit') is False and q.get('keyword_rows')==0 for q in queries), 'registration/graph')
    require(reg.get('fresh_generators_created')==0 and reg.get('fresh_random_draws')==0 and reg.get('simulation_performed') is False,'registration/no prior run')
    opening=read(root/'config/h17-r0-execution-opening.json')
    require(opening.get('complete') is True and opening.get('execution_opened') is True and
            opening.get('decision')=='decision:h17-r0-open' and opening.get('design')==FINAL and
            opening.get('design_sha256_alpha')==digest((root/FINAL).read_bytes()) and
            opening.get('seed_config_sha256_alpha')==digest((root/CONFIG).read_bytes()) and
            opening.get('seed_registration_sha256_alpha')==digest((root/REGISTRATION).read_bytes()) and
            opening.get('conditions')==list(CONDITIONS) and opening.get('rows')==400 and opening.get('steps')==600 and
            opening.get('main_claims_allowed')==1,'opening/contract')
    return pins,pair,digest((root/PINS).read_bytes())


def check_source_files(root,files):
    for name,expected in files.items():
        path=(root/name).resolve()
        require(path.is_relative_to(root.resolve()) and path.is_file(),'pins/path')
        require(digest(path.read_bytes())==expected,'pins/source/'+name)


def runtime_stamp():
    """Actual verifier process, not an assertion copied from saved metadata."""
    libraries={name:dict(path=str(Path(importlib.import_module(name).__file__).resolve()),
        sha256_alpha=digest(Path(importlib.import_module(name).__file__).read_bytes()))
        for name in ('numpy._core._multiarray_umath','numpy.random._generator')}
    threads=('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS')
    return dict(python=platform.python_version(),numpy=np.__version__,implementation=platform.python_implementation(),
        executable=str(Path(sys.executable).resolve()),executable_sha256_alpha=digest(Path(sys.executable).read_bytes()),
        numpy_path=str(Path(np.__file__).resolve()),numpy_init_sha256_alpha=digest(Path(np.__file__).read_bytes()),
        platform=platform.platform(),machine=platform.machine(),pointer_bits=struct.calcsize('P')*8,
        byteorder=sys.byteorder,threads={key:os.environ.get(key) for key in threads},processes=1,
        optimize=sys.flags.optimize,assertions_enabled=__debug__,native_libraries=libraries,
        numpy_config_sha256_alpha=digest(canonical(np.__config__.show(mode='dicts'))))


def group(arrays,prefix):
    return {key[len(prefix):]:arrays[key] for key in arrays if key.startswith(prefix)}


def full_snapshot_check(left,right,record_left,record_right,fields,label):
    require(record_left['events']==record_right['events'],label+'/event sequence')
    for name in fields:
        i=record_left['state_fields'].index(name); j=record_right['state_fields'].index(name)
        same(left[:,i],right[:,j],label+'/'+name)


def physical_scores(output,good):
    rows=np.arange(len(good)); at=output['AT2']; w=output['W']
    dwell=at.sum(0).astype(float)
    dv,dn=dwell[rows,good],dwell[rows,1-good]
    valued=dv>dn;neutral=dn>dv
    return dict(dwell=dwell,contacts=output['C'].sum(0).astype(float),
                first=np.where(at.any(0),at.argmax(0),-1),
                lost=~w[-200:].any((0,2)),
                choice=np.select([valued,neutral,~(valued|neutral)],[0,1,2]))


class GeneratorState:
    def __init__(self,state): self.state=state


class Missing:
    pass


MISSING=Missing()


def historical_blob(value):
    if isinstance(value,np.ndarray):
        a=np.ascontiguousarray(value)
        return b'A'+a.dtype.str.encode()+repr(a.shape).encode()+a.tobytes()
    if isinstance(value,GeneratorState): return b'G'+repr(value.state).encode()
    if value is MISSING: return b'M'
    require(value is None or isinstance(value,(bool,int,float,str,tuple,list,set,np.generic)), 'identity/unsupported attribute')
    return b'S'+type(value).__name__.encode()+repr(value).encode()


class BlobTable:
    """Decode pinned native arrays and recursively tagged values, never pickle."""
    def __init__(self, arrays, descriptors):
        self.arrays=arrays; self.descriptors=descriptors; self.cache=OrderedDict(); self.visiting=set()
        self.cache_bytes=0; self.cache_limit=32<<20
        require({x[5:] for x in arrays if x.startswith('blob/')}==set(descriptors),'blob/table keyset')
        for key,descriptor in descriptors.items():
            require(re.fullmatch('[a-p]{64}',key) is not None,'blob/id')
            a=arrays['blob/'+key]
            if descriptor.get('kind')=='ndarray':
                require(set(descriptor)=={'kind','dtype','shape'},'blob/array descriptor')
                require(a.dtype.str==descriptor['dtype'] and list(a.shape)==descriptor['shape'],'blob/array schema')
            else:
                require(descriptor=={'kind':'typed_json'} and a.dtype==np.uint8 and a.ndim==1,'blob/typed descriptor')
            require(digest(canonical(descriptor)+a.tobytes())==key,'blob/content address')

    def get(self,key):
        if isinstance(key,(bytes,np.bytes_)): key=bytes(key).decode('ascii')
        key=str(key)
        if key in self.cache:
            self.cache.move_to_end(key);return self.cache[key][0]
        require(key in self.descriptors and key not in self.visiting,'blob/reference or cycle')
        self.visiting.add(key)
        a=self.arrays['blob/'+key]
        if self.descriptors[key]['kind']=='ndarray': result=a
        else:
            raw=a.tobytes(); tag=json.loads(raw.decode('utf-8'),object_pairs_hook=unique)
            require(canonical(tag)==raw,'blob/noncanonical JSON')
            result=self.tag(tag)
        self.visiting.remove(key)
        size=a.nbytes
        if size<=self.cache_limit:
            while self.cache and (self.cache_bytes+size>self.cache_limit or len(self.cache)>=4096):
                _,(_,oldsize)=self.cache.popitem(last=False);self.cache_bytes-=oldsize
            self.cache[key]=(result,size);self.cache_bytes+=size
        return result

    def clear(self):
        self.cache.clear();self.cache_bytes=0

    def tag(self,tag):
        require(isinstance(tag,dict) and 'type' in tag,'blob/tag')
        kind=tag['type']
        if kind in ('none','missing'):
            require(set(tag)=={'type'},'blob/null schema')
            return None if kind=='none' else MISSING
        if kind in ('bool','int','float','str'):
            require(set(tag)=={'type','value'},'blob/scalar schema')
            value=tag['value']
            if kind=='float':
                require(isinstance(value,str),'blob/float encoding')
                result=float.fromhex(value)
                require(math.isfinite(result) and result.hex()==value,'blob/float canonical')
                return result
            require(type(value)=={'bool':bool,'int':int,'str':str}[kind],'blob/scalar type')
            return value
        if kind=='numpy_scalar':
            require(set(tag)=={'type','dtype','value_hex_alpha'},'blob/numpy scalar schema')
            dtype=np.dtype(tag['dtype']); ap=tag['value_hex_alpha']
            require(not dtype.hasobject and dtype.kind in 'biufUS' and re.fullmatch('[a-p]+',ap) is not None and len(ap)==2*dtype.itemsize,'blob/numpy scalar encoding')
            return np.frombuffer(bytes.fromhex(ap.translate(HEX)),dtype=dtype)[0]
        if kind=='array_ref':
            require(set(tag)=={'type','id'},'blob/array reference schema')
            value=self.get(tag['id']); require(isinstance(value,np.ndarray),'blob/array reference type')
            return value
        if kind in ('list','tuple','set'):
            require(set(tag)=={'type','items'} and isinstance(tag['items'],list),'blob/container schema')
            values=[self.tag(x) for x in tag['items']]
            if kind=='set':
                require(tag['items']==sorted(tag['items'],key=canonical),'blob/set canonical')
                require(len(set(values))==len(values),'blob/set duplicate')
                return set(values)
            return tuple(values) if kind=='tuple' else values
        if kind=='dict':
            require(set(tag)=={'type','items'} and isinstance(tag['items'],list),'blob/dict schema')
            result={}
            for pair in tag['items']:
                require(isinstance(pair,list) and len(pair)==2,'blob/dict pair')
                key,value=self.tag(pair[0]),self.tag(pair[1]);require(key not in result,'blob/dict duplicate')
                result[key]=value
            return result
        if kind=='generator':
            require(set(tag)=={'type','state'},'blob/generator schema')
            state=self.tag(tag['state']);require(isinstance(state,dict),'blob/generator state type')
            return GeneratorState(state)
        raise VerificationError('blob/unknown type')


class SnapshotTimeline:
    def __init__(self,arrays,record,prefix,table):
        self.events=record['events'];self.fields=record['state_fields'];self.table=table;self.prefix=prefix
        fields=self.fields;events=self.events
        require(len(fields)==len(set(fields)) and fields==sorted(fields),'snapshot/fields')
        self.timeline=arrays[prefix+'/state_timeline'];self.hashes=arrays[prefix+'/attribute_hashes']
        require(self.timeline.dtype==np.dtype('S64') and self.timeline.shape==(len(events),len(fields)),'snapshot/timeline schema')
        require(self.hashes.dtype==np.dtype('S64') and self.hashes.shape==self.timeline.shape,'snapshot/hash schema')
    def get(self,i,field):
        j=self.fields.index(field);value=self.table.get(self.timeline[i,j])
        require(bytes(self.hashes[i,j]).decode()==digest(historical_blob(value)),self.prefix+'/'+field+'/snapshot hash',[i,j],self.events[i]['phase'])
        return value
    def row(self,i):return {field:self.get(i,field) for field in self.fields}
    def validate(self):
        for i in range(len(self.events)):
            for field in self.fields:self.get(i,field)


def snapshots(arrays,record,prefix,table):
    result=SnapshotTimeline(arrays,record,prefix,table);result.validate();return result


def source_schema(schema,key,descriptor,smoke):
    """Dynamic content IDs are allowed only within the pinned blob grammar."""
    if key.startswith('blob/'):
        require(re.fullmatch('blob/[a-p]{64}',key) is not None,'schema/blob name')
        require(np.dtype(descriptor['dtype']).kind in schema['dtype_kinds'],'schema/blob dtype')
        return dict(dtype=descriptor['dtype'],shape=descriptor['shape'])
    # Fixed keys use a sample-size template. Concrete shapes are checked
    # against the pinned template before any payload is loaded.
    template=schema['arrays'].get(key)
    require(template is not None,'schema/unregistered key/'+key)
    dims={'T':600,'R':40 if smoke else 400,'E':2401,'G':4201}
    shape=[dims.get(x,x) for x in template['shape']]
    return dict(dtype=template['dtype'],shape=shape)


def draw_values(log, table):
    """Decode a complete primitive call; state equality is separately gated."""
    require(set(log)>={'generator','method','args','kwargs','result','before','after','step','phase'},'draw/log keyset')
    args=table.get(log['args']);kwargs=table.get(log['kwargs']);result=table.get(log['result'])
    require(isinstance(args,tuple) and isinstance(kwargs,dict) and isinstance(result,np.ndarray),'draw/call types')
    before=table.get(log['before']);after=table.get(log['after'])
    before=before.state if isinstance(before,GeneratorState) else before
    after=after.state if isinstance(after,GeneratorState) else after
    require(isinstance(before,dict) and isinstance(after,dict),'draw/state type')
    require(before.get('bit_generator')==after.get('bit_generator')=='PCG64','draw/bitgenerator')
    require(canonical_state(before)!=canonical_state(after),'draw/state unchanged')
    return args,kwargs,result,before,after


def canonical_state(value):
    """Insertion order intentionally retained for the historical repr hash."""
    return repr(value).encode('utf-8')


def call_shape(args, kwargs, method, shape, label):
    require(method in ('random','standard_normal'),'draw/method/'+label)
    require(not kwargs or set(kwargs)<={'size','dtype','out'},'draw/unexpected kwargs/'+label)
    size=args[0] if args else kwargs.get('size')
    actual=(size,) if isinstance(size,int) else tuple(size)
    require(actual==tuple(shape),'draw/size/'+label)
    require(kwargs.get('out') is None,'draw/out mutation/'+label)


def independent_draws(record, table, sample, condition, label):
    """Validate transcript continuity and rebuild delivered source/noise inputs."""
    logs=record['draw_log'];instances=record['generator_instances'];t,r=sample['H_post'].shape
    expected_count={'C0':7,'T1':6,'W1':8,'T3':6}[condition]
    require(len(instances)==expected_count,label+'/generator count')
    roles=[x['role'] for x in instances]
    require(len(set(roles))==expected_count,label+'/generator roles')
    worlds={i for i,role in enumerate(roles) if role in ('world','twin')}
    agent=next((i for i,role in enumerate(roles) if role=='agent'),None)
    require(agent is not None and len(worlds)==(2 if condition=='W1' else 1),label+'/primary roles')
    world=roles.index('world')
    twin=next((i for i in worlds if i!=world),None)
    previous={};by_phase={};normals={k:[] for k in ('circuit','rotation','cue','turn')}
    for i,instance in enumerate(instances):
        state=table.get(instance['initial']);state=state.state if isinstance(state,GeneratorState) else state
        require(isinstance(state,dict),label+'/creation state');previous[i]=state
    for log in logs:
        g=log['generator'];require(type(g) is int and 0<=g<expected_count,label+'/draw generator')
        args,kwargs,result,before,after=draw_values(log,table)
        require(canonical_state(previous[g])==canonical_state(before),label+'/draw state continuity',phase=str(log['phase']))
        previous[g]=after
        require(np.isfinite(result).all() if result.dtype.kind=='f' else True,label+'/draw finite')
        by_phase.setdefault((log['step'],log['phase']),[]).append((g,log,args,kwargs,result))
    for step in range(t):
        sense=by_phase.get((step,'sense'),[]);wind=by_phase.get((step,'wind'),[])
        require(len(sense)==2 and [x[0] for x in sense]==[world,world],label+'/sense call order',[step], 'sense')
        require(len(wind)==1 and wind[0][0]==world,label+'/wind call order',[step],'wind')
        for channel,item in enumerate(sense):
            _,log,args,kw,result=item;call_shape(args,kw,log['method'],(r,),label+'/sense')
            require(log['method']=='random',label+'/sense method')
            same(result,sample['source_uniforms'][step,:,channel],label+'/source uniform',[step])
        _,log,args,kw,result=wind[0];call_shape(args,kw,log['method'],(r,),label+'/wind')
        require(log['method']=='random',label+'/wind method')
        same(result,sample['wind_uniform'][step],label+'/wind uniform','wind')
        act=by_phase.get((step,'act'),[]) + by_phase.get((step,'base'),[])
        require(len(act)==4 and all(x[0]==agent for x in act),label+'/act draw count',[step],'act')
        for name,shape,item in zip(('circuit','rotation','cue','turn'),((r,2),(r,16),(r,16),(r,)),act):
            _,log,args,kw,result=item;call_shape(args,kw,log['method'],shape,label+'/'+name)
            require(log['method']=='standard_normal' and result.shape==shape,label+'/normal method/shape')
            normals[name].append(result)
        if condition=='W1':
            twinlog=by_phase.get((step,'twin'),[])
            require(len(twinlog)==3 and all(x[0]==twin for x in twinlog),label+'/twin calls',[step],'twin')
            for j,item in enumerate(twinlog):
                _,log,args,kw,result=item;call_shape(args,kw,log['method'],(r,),label+'/twin')
                require(log['method']=='random',label+'/twin method')
                reference=sample['source_uniforms'][step,:,j] if j<2 else sample['wind_uniform'][step]
                same(result,reference,label+'/twin draw','twin')
    require(all(step==-1 or (0<=step<t and phase in ('sense','wind','twin','act','base')) for step,phase in by_phase),label+'/extra drawing phase')
    # Primitive calls on balance/code/cast/geometry roles may occur only in construction.
    for (step,phase),items in by_phase.items():
        if step>=0:require(all(g in worlds|{agent} for g,*_ in items),label+'/late construction draw')
    return {key:np.stack(value) for key,value in normals.items()}


def event_contract(record,t,label):
    expected=[dict(step=-1,phase='construction')]
    expected.extend(dict(step=i,phase=phase) for i in range(t) for phase in ('pre','base','act','bump'))
    tree_same(record['events'],expected,label+'/events')


def snapshot_sample_check(timeline,sample,construction,label):
    """Link every numerical phase to the full typed snapshot evidence."""
    t,r=sample['H_post'].shape
    link={'S':'sel.s','SG':'sel.S','UP':'up.P','SIL':'silence','SINCE':'since','C':'c','PRES':'present'}
    for i in range(t):
        pre,base,act,bump=(1+4*i+j for j in range(4))
        for name,attribute in link.items():
            for phase,index in (('pre',pre),('post',act)):
                value=timeline.get(index,attribute)
                if name=='SG':value=np.asarray(value)[:,0]
                same(sample[name+'_'+phase][i],value,label+'/'+name+'_'+phase+'/snapshot',phase)
        same(sample['SIL_base'][i],timeline.get(base,'silence'),label+'/SIL_base snapshot','base')
        for name,attribute in (('EST','est'),('NAV','nav_hit'),('TO','due_timeout'),('EV','due_evidence'),
                               ('sustain','sustain'),('zreset','zreset'),('TGT','tgt'),('TURN','last_turn')):
            same(sample[name][i],timeline.get(act,attribute),label+'/'+name+'/snapshot','act')
        for name in ('cast_sign','flee_side'):
            same(sample[name][i],timeline.get(pre,name),label+'/'+name+'/snapshot','pre')
            same(timeline.get(bump,name),timeline.get(act,name),label+'/'+name+'/no contacts','bump')
        same(timeline.get(act,'known'),construction['known'],label+'/fixed known','act')
        for field in ('mb.w','mb.tc','mb.tr'):
            require(timeline.timeline[0,timeline.fields.index(field)]==timeline.timeline[act,timeline.fields.index(field)],label+'/no learning/'+field,[i],'act')
    initial=timeline.row(0)
    for key,field in (('S0','sel.s'),('SG0','sel.S'),('UP0','up.P'),('SIL0','silence'),('SINCE0','since'),('C0','c'),('ring0','ring.s')):
        value=initial[field]
        expected=value[:,0] if key=='SG0' else value
        same(construction[key],expected,label+'/stored construction/'+key,'construction')
    require(initial['N']==initial['N_hi']==200 and initial['P']==60,label+'/presence parameters')
    for key in ('S0','SG0','UP0','SIL0','SINCE0','ring0'):
        require(not construction[key].any(),label+'/cold constructor/'+key)
    same(construction['C0'],np.full((r,2),140.0),label+'/constructor counters')
    require(initial['present'].all(),label+'/constructor presence')
    same(initial['known'],construction['known'],label+'/constructor known')
    same(construction['codes0'],initial['codes'],label+'/stored construction/codes0','construction')
    return construction


def construction_check(condition,construction,sample,c,rows,label):
    require(construction['src'].shape==(rows,2,2),label+'/source shape')
    cell,good,plus=construction['cell'],construction['good'],construction['plus_y']
    same(good,(cell//2).astype(good.dtype),label+'/good balance')
    same(plus,np.where(cell%2==0,good,1-good).astype(plus.dtype),label+'/physical identity')
    require(np.array_equal(np.bincount(cell,minlength=4),np.full(4,rows//4)),label+'/four cell balance')
    src=construction['src'];rr=np.arange(rows)
    same(src[:,0,0],src[:,1,0],label+'/source along equality')
    same(src[rr,plus,1]-src[rr,1-plus,1],np.full(rows,c['SEP']),label+'/source separation')
    ordinary=np.stack([src[:,0,0]+c['DOWN'],src[:,:,1].mean(1)],1)
    same(construction['ordinary_start'],ordinary,label+'/ordinary start')
    same(sample['PRE_POS'][0],construction['start'],label+'/start wiring','pre')
    same(sample['PRE_HEAD'][0],construction['head0'],label+'/heading wiring','pre')
    same(sample['PRE_ROT'][0],construction['rot0'],label+'/rotation wiring','pre')
    require(not construction['rot0'].any(),label+'/initial rotation')
    same(construction['head0'],construction['ordinary_head'],label+'/untouched heading')
    same(construction['rot0'],construction['ordinary_rot'],label+'/untouched rotation')
    known=np.zeros((rows,2))
    if condition!='C0':known[rr,good]=1.0
    if condition=='T3':known[rr,1-good]=-1.0
    same(construction['known'],known,label+'/supplied values')
    if condition=='C0':
        sign=construction['C0sign'];k=construction['C0k'];da=construction['C0da'];dc=construction['C0dc']
        require(np.isin(sign,[-1.,1.]).all(),label+'/C0 side')
        for category in range(4):
            require(int(((cell==category)&(sign==1)).sum())==rows//8 and int(((cell==category)&(sign==-1)).sum())==rows//8,label+'/C0 side cell balance')
        same(k,np.where(sign>0,plus,1-plus).astype(k.dtype),label+'/C0 outer source')
        require(((da>=5)&(da<14)&(dc>=26)&(dc<31)).all(),label+'/C0 geometry bounds')
        start=np.stack([src[rr,k,0]+da,src[rr,k,1]+sign*dc],1)
        same(construction['start'],start,label+'/C0 geometry')
        require(not sample['probabilities'][0].any(),label+'/C0 zero probability','sense')
    else:same(construction['start'],construction['ordinary_start'],label+'/ordinary actual start')
    expected=sample['W_raw'].copy()
    if condition=='W1':expected[:,rr,good]=False
    same(sample['W_delivered'],expected,label+'/delivered mask','sense')
    same(sample['PRE_POS'][1:],sample['POS'][:-1],label+'/position continuity','pre')
    same(sample['PRE_HEAD'][1:],sample['HEAD'][:-1],label+'/heading continuity','pre')
    same(sample['PRE_ROT'][1:],sample['ROT'][:-1],label+'/rotation continuity','pre')


def construction_draw_check(record,table,construction,condition,pair,c,label):
    r=len(construction['good']);instances=record['generator_instances'];roles=[x['role'] for x in instances]
    expected_roles=['world','balance','agent','code0','code1','cast']
    if condition=='C0':expected_roles+=['geometry']
    if condition=='W1':expected_roles=['world','balance','twin','twin_balance','agent','code0','code1','cast']
    require(roles==expected_roles,label+'/generator role order')
    w,a=pair;expected_seeds=dict(world=w,balance=w+10000,agent=a,code0=c['CODE_SEEDS'][0],
        code1=c['CODE_SEEDS'][1],cast=a+20000,geometry=w+20000,twin=w,twin_balance=w+10000)
    for index,instance in enumerate(instances):
        require(instance['index']==index and instance['state_type']=='PCG64',label+'/generator descriptor')
        tree_same(table.get(instance['seed_args']), (expected_seeds[instance['role']],),label+'/seed role')
        tree_same(table.get(instance['seed_kwargs']), {},label+'/seed kwargs')
    construct={role:[] for role in roles}
    for log in record['draw_log']:
        if log['step']==-1:
            require(log['phase']=='construction',label+'/construction phase')
            construct[roles[log['generator']]].append((log,*draw_values(log,table)[:3]))
    world=construct['world']
    signatures=[('uniform',(8.0,14.0,r)),('uniform',(8.0,14.0,r)),('uniform',(14.0,18.0,r)),
                ('integers',(0,2,r)),('integers',(0,2,r)),('uniform',(5.0,18.0,r)),
                ('uniform',(-1,1,r)),('uniform',(0,360,r))]
    require(len(world)==8,label+'/eight world construction calls')
    for entry,(method,args) in zip(world,signatures):
        log,actual,kwargs,value=entry
        require(log['method']==method and actual==args and not kwargs and value.shape==(r,),label+'/world construction signature')
    balance=construct['balance'];require(len(balance)==1,label+'/balance call count')
    log,args,kwargs,permutation=balance[0]
    require(log['method']=='permutation' and args==(r,) and not kwargs and np.array_equal(np.sort(permutation),np.arange(r)),label+'/balance permutation')
    cell=np.empty(r,np.int64);cell[permutation]=np.arange(r)%4
    same(construction['cell'],cell.astype(construction['cell'].dtype),label+'/balance assignment')
    good=cell//2;side=np.where(cell%2==0,1.0,-1.0)
    # World4 translates the inherited source frame by 60. World7 overwrites
    # the gap/identity/start while preserving all eight construction calls.
    x=world[0][3]+60.0;yc=world[1][3]+60.0+c['SEP']/2
    src=np.zeros((r,2,2));rr=np.arange(r);src[:,:,0]=x[:,None]
    src[rr,good,1]=yc+side*c['SEP']/2;src[rr,1-good,1]=yc-side*c['SEP']/2
    same(construction['src'],src,label+'/world source draws')
    same(construction['ordinary_head'],world[7][3],label+'/world heading draw')
    for role,options,field in (('agent',[90.0,270.0],'flee_side'),('cast',[1.0,-1.0],'cast_sign')):
        require(len(construct[role])==1,label+'/'+role+'/construction count')
        log,args,kwargs,result=construct[role][0]
        require(log['method']=='choice' and len(args)==2 and args[0]==options and args[1]==r and not kwargs,label+'/'+role+'/choice signature')
        same(construction[field],result,label+'/'+role+'/choice result')
    codes=np.zeros((r,2,c['MB_K']))
    for channel,role in enumerate(('code0','code1')):
        require(len(construct[role])==r,label+'/fixed code choice count')
        for row,(log,args,kwargs,result) in enumerate(construct[role]):
            require(log['method']=='choice' and args==(c['MB_K'],10) and kwargs=={'replace':False}
                    and result.shape==(10,) and len(set(result.tolist()))==10 and ((result>=0)&(result<c['MB_K'])).all(),label+'/fixed code draw')
            codes[row,channel,result]=1.0
    same(construction['codes0'],codes,label+'/fixed codes state binding')
    if condition=='C0':
        geom=construct['geometry'];require(len(geom)==6,label+'/geometry call count')
        sign=np.empty(r,float)
        for category in range(4):
            log,args,kwargs,perm=geom[category]
            group_rows=np.where(cell==category)[0]
            require(log['method']=='permutation' and len(args)==1 and not kwargs,label+'/geometry permutation')
            same(np.asarray(args[0]),group_rows,label+'/geometry input rows')
            same(np.sort(perm),group_rows,label+'/geometry output rows')
            sign[perm]=np.where(np.arange(len(perm))%2==0,1.0,-1.0)
        same(construction['C0sign'],sign,label+'/geometry side draw')
        for entry,args_expected,field in ((geom[4],(5.,14.,r),'C0da'),(geom[5],(26.,31.,r),'C0dc')):
            log,args,kwargs,result=entry
            require(log['method']=='uniform' and args==args_expected and not kwargs,label+'/geometry bounds/order')
            same(construction[field],result,label+'/'+field+'/geometry draw')
    if condition=='W1':
        require(len(construct['twin'])==8 and len(construct['twin_balance'])==1,label+'/twin construction draw count')
        for left,right in zip(world,construct['twin']):
            require(left[0]['method']==right[0]['method'] and left[1:3]==right[1:3],label+'/twin construction methods')
            same(left[3],right[3],label+'/twin construction result')
        same(balance[0][3],construct['twin_balance'][0][3],label+'/twin balance result')


def generator_checkpoints(arrays,record,prefix,table,condition,steps):
    labels=[dict(step=-1,phase='construction')]
    labels.extend(dict(step=t,phase=p) for t in range(steps) for p in ('before','sense','wind','twin','act','move','bump'))
    tree_same(record['rng_labels'],labels,prefix+'/RNG labels')
    roles=[x['role'] for x in record['generator_instances']]
    states=arrays[prefix+'/rng_timeline']
    require(states.dtype==np.dtype('S64') and states.shape==(len(labels),len(roles)),prefix+'/RNG timeline schema')
    initial=[table.get(x['initial']) for x in record['generator_instances']]
    previous=[x.state if isinstance(x,GeneratorState) else x for x in initial]
    logs_by_phase={}
    for log in record['draw_log']:logs_by_phase.setdefault((log['step'],log['phase']),[]).append(log)
    index=0
    for label in labels:
        step,phase=label['step'],label['phase']
        calls=logs_by_phase.get((step,phase),[])
        for log in calls:
            g=log['generator'];_,_,_,before,after=draw_values(log,table)
            require(canonical_state(previous[g])==canonical_state(before),prefix+'/RNG checkpoint call continuity',[step,g],phase)
            previous[g]=after
        for g in range(len(roles)):
            value=table.get(states[index,g]);state=value.state if isinstance(value,GeneratorState) else value
            require(canonical_state(state)==canonical_state(previous[g]),prefix+'/RNG checkpoint state',[step,g],phase)
        if condition=='W1' and phase in ('construction','twin','act','move','bump'):
            require(canonical_state(previous[roles.index('world')])==canonical_state(previous[roles.index('twin')]),prefix+'/world twin RNG',[step],phase)
        index+=1
    return states


def world_snapshot_check(arrays,record,prefix,table,sample,construction,condition,label):
    fields=record['world_fields'];events=record['events'];timeline=arrays[prefix+'/world_timeline']
    require(fields==sorted(set(fields)) and timeline.shape==(len(events),len(fields)) and timeline.dtype==np.dtype('S64'),label+'/world timeline')
    def value(i,name):return table.get(timeline[i,fields.index(name)])
    for i,event in enumerate(events):
        state={field:value(i,field) for field in fields}
        require(state.get('walls') is False and state.get('p_d')==0 and state.get('p_wind')==1.0 and state.get('p_hit')==0.3,label+'/world constants',[event['step']],event['phase'])
        same(state['src'],construction['src'],label+'/fixed sources',event['phase'])
        same(state['good'],construction['good'],label+'/fixed good',event['phase'])
        if event['step']<0:
            same(state['pos'],construction['start'],label+'/world construction position','construction')
            same(state['head'],construction['head0'],label+'/world construction heading','construction')
            require(state['t']==0 and not state['bumped'].any(),label+'/world initial','construction')
        else:
            t=event['step'];post=event['phase']=='bump'
            for field,prekey,postkey in (('pos','PRE_POS','POS'),('head','PRE_HEAD','HEAD'),('rot','PRE_ROT','ROT')):
                same(state[field],sample[postkey if post else prekey][t],label+'/world/'+field,event['phase'])
            require(state['t']==t+int(post),label+'/world clock',[t],event['phase'])
            require(not state['bumped'].any(),label+'/world no contacts',[t],event['phase'])
            if condition=='W1' and event['phase'] in ('base','act','bump'):
                same(state['raw'],sample['W_raw'][t],label+'/masked raw',event['phase'])
                same(state['plume'],sample['W_delivered'][t].any(1),label+'/masked plume',event['phase'])


def original_output_check(output,sample,construction,label):
    direct={'H':'H_post','W':'W_delivered','NAV':'NAV','TO':'TO','EV':'EV','SUS':'sustain','Z':'zreset',
            'SIL':'SIL_post','SINCE':'SINCE_post','TGT':'TGT','S':'S_post','SG':'SG_post',
            'POS':'POS','HEAD':'HEAD','AT2':'AT2','C':'C','C2':'C_post','P2':'PRES_post'}
    for key,source in direct.items():
        require(key in output,label+'/original output missing/'+key)
        # Legacy outputs deliberately use int8 H and float32 clocks/counters.
        same(output[key],sample[source].astype(output[key].dtype),label+'/original output/'+key)
    same(output['PA'],(sample['S_pre']>1.).any(2),label+'/original pre-active')
    h=sample['H_post'];w=sample['W_delivered'];known=construction['known'];rr=np.arange(len(known))[None,:];tt=np.arange(len(h))[:,None]
    hit=(h>=0)&w[tt,rr,np.maximum(h,0)]
    nav6=hit|((h<0)&(w&(known[None,:,:]>=0)).any(2))
    vmax=known.max(1);top=(known>=0)&(known==vmax[:,None]);vh=known[rr,np.maximum(h,0)]
    nav8=np.where((h>=0)&((vh==vmax[None,:])|(vh<0)),hit,(w&top[None,:,:]).any(2))
    for name,value in (('NAV6',nav6),('NAV8',nav8),('DIFF',sample['NAV']!=nav6),('DIFF8',sample['NAV']!=nav8)):
        same(output[name],value,label+'/original diagnostic/'+name)
    same(output['PRES'],sample['PRES_post'][:,np.arange(len(known)),construction['good']],label+'/original valued presence')
    for key in ('src','good','cell','plus_y','start'):
        same(output[key],construction[key],label+'/original construction/'+key)
    same(output['cast'],construction['cast_sign'],label+'/original cast')
    same(output['s0'],construction['S0'],label+'/original initial circuit')
    same(output['H0'],np.full(len(construction['good']),-1,dtype=output['H0'].dtype),label+'/original initial hold')
    scores=physical_scores(output,construction['good'])
    for key in ('dwell','contacts','first'):
        same(output[key],scores[key].astype(output[key].dtype),label+'/original score/'+key)
    return scores


def w1_scores(output,good,c):
    """Complete ph25.w1sum/ph22.summary arithmetic from original arrays."""
    steps,rows=output['H'].shape;rr=np.arange(rows);p=1-good
    at=output['AT2'][:,rr,p];w=output['W'][:,rr,p];h=output['H'];nav=output['NAV'];pos=output['POS'];src=output['src'][rr,p]
    da=pos[:,:,0]-src[None,:,0];dc=np.abs(pos[:,:,1]-src[None,:,1]);dist=np.hypot(da,dc)
    near=dist<5.;ent=(near&~np.vstack([np.zeros((1,rows),bool),near[:-1]])).sum(0)
    held=h==p[None,:];prev=np.vstack([np.full((1,rows),False),held[:-1]]);ended=~held&prev
    return dict(reach=at.any(0),first=first(at),dwell=at.sum(0),whiffs=w.sum(0),fw=first(w),nav=nav.sum(0),
        lost=~w[-steps//3:].any(0),nonav=~nav[-steps//3:].any(0),contacts=output['C'].sum(0),
        heldB=held.mean(0),nothing=(h<0).mean(0),formed=(held&~prev).sum(0),released=ended.sum(0),
        end_to=(ended&output['TO']&~output['EV']).sum(0),end_ev=(ended&output['EV']&~output['TO']).sum(0),
        end_both=(ended&output['TO']&output['EV']).sum(0),end_none=(ended&~output['TO']&~output['EV']).sum(0),
        fh=first(h>=0),heldB_end=held[-1],cone=((da>0)&(da<c['LMAX'])&(dc<c['W0']+c['SLOPE']*da)).sum(0),
        da_min=da.min(0),da_end=da[-1],dc_end=dc[-1],dmin=dist.min(0),f5=first(near),ent5=ent,
        since_max=float(output['SINCE'].max()),cum={str(k):at[:k].any(0) for k in range(100,steps+1,100)})


def scores_same(a,b,label):
    require(set(a)==set(b),label+'/keys')
    for key in a:
        if isinstance(a[key],dict):scores_same(a[key],b[key],label+'/'+key)
        elif isinstance(a[key],np.ndarray):same(a[key],b[key],label+'/'+key)
        else:tree_same(a[key],b[key],label+'/'+key)


def coupling_gate(arrays,records,condition,names,schema):
    """Prove primitive-log projection before reading projected draw results."""
    literal=records['Fly'];passive=records['Passive'];lineage=records['Agent17']
    for arm,record in records.items():
        expected_keys={'output_metadata','state_fields','world_fields','events','rng_labels','generator_instances','draw_log',
            'independent_streams','generator_handles','literal_generators','construction_refs','observation_calls','primitive_log_proof','L3'}
        if arm!='Passive':expected_keys.add('draw_log_reference')
        require(set(record)==expected_keys,condition+'/'+arm+'/record keyset')
        require(record['state_fields']==schema['fieldsets'][arm] and
                record['world_fields']==schema['world_fieldsets'][condition],condition+'/'+arm+'/frozen fields')
        event_contract(record,600,condition+'/'+arm)
    for table in ('state_timeline','attribute_hashes','world_timeline','rng_timeline','input_timeline','return_timeline'):
        same(arrays[condition+'/Fly/'+table],arrays[condition+'/Passive/'+table],condition+'/sameclass/'+table)
    for arm in ('Fly','Agent17'):
        record=records[arm]
        tree_same(record['rng_labels'],passive['rng_labels'],condition+'/'+arm+'/RNG labels')
        for table in ('world_timeline','rng_timeline','input_timeline','return_timeline'):
            same(arrays[condition+'/'+arm+'/'+table],arrays[condition+'/Passive/'+table],condition+'/'+arm+'/paired/'+table)
        require(len(record['generator_instances'])==len(passive['generator_instances']),condition+'/creation count')
        for a,b in zip(record['generator_instances'],passive['generator_instances']):
            for field in ('index','role','seed_args','seed_kwargs','initial','state_type'):
                tree_same(a[field],b[field],condition+'/'+arm+'/creation/'+field)
        for groupname in ('sample','construction','output')+ (('twin',) if condition=='W1' else ()):
            prefix=condition+'/'+arm+'/'+groupname+'/'
            keys=[key[len(prefix):] for key in arrays if key.startswith(prefix)]
            other=condition+'/Passive/'+groupname+'/'
            require(set(keys)=={key[len(other):] for key in arrays if key.startswith(other)},condition+'/'+groupname+'/paired keyset')
            for key in keys:same(arrays[prefix+key],arrays[other+key],condition+'/'+arm+'/paired/'+groupname+'/'+key)
        metadata=dict(record['output_metadata']);other=dict(passive['output_metadata'])
        metadata.pop('arm',None);other.pop('arm',None)
        tree_same(metadata,other,condition+'/'+arm+'/original metadata')
    refset=set(lineage['state_fields']);candset=set(literal['state_fields'])
    tree_same(dict(common=sorted(refset&candset),ref_only=sorted(refset-candset),cand_only=sorted(candset-refset)),names,condition+'/lineage fields')
    a=arrays[condition+'/Agent17/attribute_hashes'];b=arrays[condition+'/Fly/attribute_hashes']
    for field in names['common']:
        same(a[:,lineage['state_fields'].index(field)],b[:,literal['state_fields'].index(field)],condition+'/lineage/'+field)
    proof=dict(source_arm='Passive',basis=['creation','every phase generator state','full inputs/returns','sample fields',
        'original output arrays','sameclass snapshots','frozen lineage common snapshots'],passed=True)
    for arm in ('Fly','Agent17'):
        tree_same(records[arm]['primitive_log_proof'],proof,condition+'/'+arm+'/primitive proof')
        require(records[arm]['draw_log_reference']==condition+'/Passive' and records[arm]['draw_log']==[],condition+'/'+arm+'/paired log reference')
    tree_same(passive['primitive_log_proof'],dict(source_arm='Passive',basis=['original shared BitGenerator direct primitive returns'],passed=True),condition+'/direct log proof')


def input_return_check(arrays,record,prefix,table,sample,timeline):
    t=sample['H_post'].shape[0]
    for kind,size in (('input',6),('return',2)):
        values=arrays[prefix+'/'+kind+'_timeline']
        require(values.dtype==np.dtype('S64') and values.shape==(t,),prefix+'/'+kind+'/timeline')
        for i,ref in enumerate(values):
            value=table.get(ref);require(isinstance(value,tuple) and len(value)==size,prefix+'/'+kind+'/tuple')
            if kind=='input':
                for item,key in zip(value[:3],('PRE_POS','PRE_HEAD','PRE_ROT')):same(item,sample[key][i],prefix+'/input/'+key,'pre')
                require(type(value[3]) is int and value[3]==i,prefix+'/input/world clock',[i],'pre')
                same(value[4],sample['W_delivered'][i],prefix+'/input/whiffs','sense')
                same(value[5],sample['wind_on'][i],prefix+'/input/wind','wind')
            else:
                same(value[0],sample['TURN'][i],prefix+'/return/turn','act')
                same(value[1],sample['H_post'][i],prefix+'/return/hold','act')
    rng=arrays[prefix+'/rng_timeline'];roles=[x['role'] for x in record['generator_instances']]
    agent=roles.index('agent')
    for i in range(t):
        # All aliased agent RNG attributes must name the same actual state.
        for phase,event,checkpoint in (('pre',1+4*i,1+7*i),('base',2+4*i,5+7*i),('act',3+4*i,5+7*i),('bump',4+4*i,7+7*i)):
            for field in ('rng','sel.rng','ring.rng','mb.rng'):
                value=timeline.get(event,field);observed=table.get(rng[checkpoint,agent])
                require(isinstance(value,GeneratorState) and isinstance(observed,GeneratorState)
                        and canonical_state(value.state)==canonical_state(observed.state),prefix+'/'+field+'/phase',[i],phase)


def stored_scores(arrays,tree,expected,prefix):
    require(isinstance(tree,dict) and set(tree)==set(expected),prefix+'/score keys')
    for key,value in expected.items():
        path=prefix+'/'+str(key)
        actual=tree[key]
        if isinstance(value,np.ndarray):
            tree_same(actual,{'array':path},path+'/reference')
            same(arrays[path],value,path)
        elif isinstance(value,dict):stored_scores(arrays,actual,value,path)
        else:tree_same(actual,value,path)


def runtime_provenance(identity,pins,pin_hash,root,smoke,directory,pair):
    prov=identity['provenance'];expected=dict(runtime=pins['runtime'],source_closure_sha256_alpha=pins['source_closure_sha256_alpha'],
        design_sha256_alpha=digest((root/FINAL).read_bytes()),config_sha256_alpha=digest((root/CONFIG).read_bytes()),
        registration_sha256_alpha=digest((root/REGISTRATION).read_bytes()),
        opening_sha256_alpha=digest((root/'config/h17-r0-execution-opening.json').read_bytes()))
    if not smoke:expected['execution_pins_sha256_alpha']=pin_hash
    tree_same(prov,expected,'provenance')
    if smoke:
        require('claim' not in identity,'H0/claim forbidden')
        return
    h0=pins.get('h0',{})
    require(h0.get('source_closure_sha256_alpha')==pins['source_closure_sha256_alpha'],'H0/source closure')
    for name,key in (('identity.json','identity'),('metrics.json','metrics'),('raw.npz.ap','raw'),('verification.json','verification')):
        path=root/'experiments/h17/r0_smoke'/name
        require(digest(path.read_bytes())==h0.get(key+'_sha256_alpha'),'H0/hash/'+name)
        if name.endswith('.json'):
            saved=read(path)
            require(saved.get('complete') is True and saved.get('smoke') is True,'H0/complete/'+name)
            if key!='metrics':require(saved.get('passed') is True,'H0/passed/'+name)
    key=digest(canonical(list(pair)))
    claim_path=root/'experiments/h17/r0_registry'/(key+'.json')
    require(identity.get('claim')==claim_path.relative_to(root).as_posix(),'claim/canonical pair path')
    claim=read(claim_path)
    expected_claim=dict(complete=True,pair_sha256_alpha=key,provenance_sha256_alpha=digest(canonical(prov)),
        source_closure_sha256_alpha=pins['source_closure_sha256_alpha'],execution_pins_sha256_alpha=pin_hash,
        design_sha256_alpha=prov['design_sha256_alpha'],
        output_path_sha256_alpha=digest(str(directory.resolve()).encode('utf-8')),decision='decision:h17-r0-open',
        claim_rule='one registered pair, durable before first generator',identity_sha256_alpha=digest((directory/'identity.json').read_bytes()),
        raw_sha256_alpha=identity['raw_arrays']['sha256_alpha'])
    tree_same(claim,expected_claim,'claim')


def twin_check(arrays,record,prefix,table,sample):
    twin=group(arrays,prefix+'/twin/')
    require(set(twin)=={'PRE_POS','PRE_HEAD','T','RAW','WIND','WALLS'},prefix+'/twin/keyset')
    same(twin['PRE_POS'],sample['PRE_POS'],prefix+'/twin position','twin')
    same(twin['PRE_HEAD'],sample['PRE_HEAD'],prefix+'/twin heading','twin')
    same(twin['T'],np.broadcast_to(np.arange(600,dtype=np.int64)[:,None],sample['H_post'].shape),prefix+'/twin clock','twin')
    same(twin['RAW'],sample['W_raw'],prefix+'/twin raw','twin')
    same(twin['WIND'],sample['wind_on'],prefix+'/twin wind','twin')
    require(not twin['WALLS'].any(),prefix+'/twin walls','twin')
    for step in range(600):
        inputs=table.get(arrays[prefix+'/twin_input_timeline'][step])
        returns=table.get(arrays[prefix+'/twin_return_timeline'][step])
        require(isinstance(inputs,tuple) and len(inputs)==3 and isinstance(returns,tuple) and len(returns)==2,prefix+'/twin typed I/O')
        same(inputs[0],twin['PRE_POS'][step],prefix+'/twin typed position','twin')
        same(inputs[1],twin['PRE_HEAD'][step],prefix+'/twin typed heading','twin')
        require(inputs[2]==step,prefix+'/twin typed clock',[step],'twin')
        same(returns[0],twin['RAW'][step],prefix+'/twin typed raw','twin')
        same(returns[1],twin['WIND'][step],prefix+'/twin typed wind','twin')


def verify(directory,root=ROOT,smoke=False):
    directory=Path(directory).resolve();root=Path(root).resolve()
    require(directory.is_relative_to((root/'experiments/h17').resolve()),'output/path')
    pins,pair,pin_hash=preflight(root)
    identity=read(directory/'identity.json');metric=read(directory/'metrics.json')
    expected_identity_keys={'complete','passed','smoke','conditions','records','gates','provenance','rows','steps','raw_arrays','metrics_sha256_alpha','first_failure'}
    if not smoke:expected_identity_keys.add('claim')
    require(set(identity)==expected_identity_keys,'identity/keyset')
    require(set(metric)=={'complete','smoke','source_closure_sha256_alpha','readings'},'metrics/keyset')
    require(identity.get('complete') is True and identity.get('passed') is True and identity.get('first_failure') is None,'identity/incomplete')
    require(identity.get('smoke') is smoke and identity.get('conditions')==list(CONDITIONS)
            and identity.get('steps')==600 and identity.get('rows')==(40 if smoke else 400),'identity/sample')
    require(metric.get('complete') is True and metric.get('smoke') is smoke and
            metric.get('source_closure_sha256_alpha')==pins['source_closure_sha256_alpha'],'metrics/incomplete')
    require(identity['metrics_sha256_alpha']==digest((directory/'metrics.json').read_bytes()),'metrics/hash')
    runtime_provenance(identity,pins,pin_hash,root,smoke,directory,pair)
    records=identity['records'];require(set(records)==set(CONDITIONS) and set(metric['readings'])==set(CONDITIONS),'condition keyset')
    descriptor=identity['raw_arrays'];schema=pins['schema']
    require(set(descriptor)=={'path','encoding','sha256_alpha','keys','arrays','blobs'},'raw/manifest keyset')
    nonblob={key for key in descriptor['arrays'] if not key.startswith('blob/')}
    require(nonblob==set(schema['arrays']),'raw/full pinned keyset')
    pinned_arrays={key:source_schema(schema,key,value,smoke) for key,value in descriptor['arrays'].items()}
    arrays=load_arrays(directory,descriptor,pinned_arrays)
    try:
        table=BlobTable(arrays,descriptor['blobs']);names=read(root/'experiments/module/identity.json')['A1']['L2']['names']
        require(set(identity['gates'])=={c+'/'+a for c in CONDITIONS for a in ARMS},'identity/gate keyset')
        # This pass precedes all projected primitive logs and all readings.
        for condition in CONDITIONS:
            require(set(records[condition])==set(ARMS) and set(metric['readings'][condition])==set(ARMS),'arm keyset')
            coupling_gate(arrays,records[condition],condition,names,schema)
            for arm in ARMS:
                gate=identity['gates'][condition+'/'+arm]
                expected_identity=dict(passed=True,same_class=True,lineage=True,creation=True,generator_phases=True,
                    inputs_and_returns=True,full_original_outputs=True,sample=True,L1=list(L1),L2_names=names,L3=True)
                tree_same(gate,dict(passed=True,complete=True,rows=40 if smoke else 400,steps=600,identity=expected_identity),'saved gate/'+condition+'/'+arm)
        constants_=source_constants(root); readings={};proofs={}
        # The named public spent H0 pair is a data-only constant, no RNG call.
        used_pair=(5,6) if smoke else pair
        baseline_construction=None
        for condition in CONDITIONS:
            readings[condition]={};proofs[condition]={};previous_scores=None
            for arm in ARMS:
                prefix=condition+'/'+arm;record=records[condition][arm]
                sample=group(arrays,prefix+'/sample/');construction=group(arrays,prefix+'/construction/');output=group(arrays,prefix+'/output/')
                require(set(sample)==set(SAMPLE_FIELDS),prefix+'/sample fieldset')
                require(all(np.isfinite(x).all() for x in sample.values() if x.dtype.kind=='f'),prefix+'/finite sample')
                for key,reference in record['construction_refs'].items():
                    require(key in construction,prefix+'/construction ref key')
                    same(construction[key],table.get(reference),prefix+'/construction ref/'+key)
                require(set(record['construction_refs'])==set(construction),prefix+'/construction ref keyset')
                timeline=snapshots(arrays,record,prefix,table)
                snapshot_sample_check(timeline,sample,construction,prefix)
                require(record['observation_calls']==dict(base=600,circuit=600),prefix+'/one base/circuit call')
                instance_count={'C0':7,'W1':8,'T1':6,'T3':6}[condition]
                require(record['independent_streams']==instance_count and record['generator_handles']==instance_count*(2 if arm=='Passive' else 1)
                        and record['literal_generators'] is (arm!='Passive'),prefix+'/generator handles')
                for instance in record['generator_instances']:
                    require(instance['handle_type']==('GeneratorTap' if arm=='Passive' else 'Generator'),prefix+'/handle type')
                effective=dict(record)
                if arm!='Passive':effective['draw_log']=records[condition]['Passive']['draw_log']
                construction_draw_check(effective,table,construction,condition,used_pair,constants_,prefix)
                generator_checkpoints(arrays,effective,prefix,table,condition,600)
                normals=independent_draws(effective,table,sample,condition,prefix)
                input_return_check(arrays,record,prefix,table,sample,timeline)
                world_snapshot_check(arrays,record,prefix,table,sample,construction,condition,prefix)
                if condition=='W1':twin_check(arrays,record,prefix,table,sample)
                construction_check(condition,construction,sample,constants_,40 if smoke else 400,prefix)
                masks=recurrence_check(sample,construction,constants_,prefix)
                final_ring=circuit_ring_check(sample,construction,constants_,normals,prefix)
                same(timeline.get(2400,'ring.s'),final_ring,prefix+'/final ring snapshot','bump')
                if arm=='Agent17':
                    for i in range(600):
                        for field,key in (('n2S','withheld_N1_S'),('n2Z','withheld_N1_Z'),('yp','Y')):
                            same(timeline.get(3+4*i,field),masks[key][i] if key in masks else sample[key][i],prefix+'/'+field+'/lineage','act')
                scores=original_output_check(output,sample,construction,prefix)
                l3=dict(dwell=scores['dwell'],first=scores['first'],contacts=scores['contacts'],cls3=scores['choice'])
                if condition=='W1':l3['w1sum']=w1_scores(output,construction['good'],constants_)
                stored_scores(arrays,record['L3'],l3,prefix+'/L3')
                if previous_scores is not None:scores_same(previous_scores,l3,prefix+'/independent L3 identity')
                previous_scores=l3
                obs,reading=metric_reading(condition,sample,construction,masks)
                stored_obs=group(arrays,prefix+'/reading/');stored_masks=group(arrays,prefix+'/mask/')
                require(set(stored_obs)==set(obs) and set(stored_masks)==set(masks),prefix+'/reading/mask keyset')
                for key,value in obs.items():same(stored_obs[key],value,prefix+'/reading/'+key)
                for key,value in masks.items():same(stored_masks[key],value,prefix+'/mask/'+key)
                anchors=group(arrays,prefix+'/anchor/');valid=obs['marker_step']>=0
                require(set(anchors)==set(SAMPLE_FIELDS)|{'anchor_valid','q_obs','last_whiff','last_nav'},prefix+'/anchor keyset')
                same(anchors['anchor_valid'],valid,prefix+'/anchor validity')
                rr=np.arange(len(valid));ix=np.maximum(obs['marker_step'],0)
                for key,value in sample.items():
                    expected=value[ix,rr].copy();expected[~valid]=0
                    same(anchors[key],expected,prefix+'/anchor/'+key)
                for key in ('q_obs','last_whiff','last_nav'):
                    expected=obs[key][ix,rr].copy();expected[~valid]=-1
                    same(anchors[key],expected,prefix+'/anchor/'+key)
                tree_same(metric['readings'][condition][arm],reading,prefix+'/metrics')
                readings[condition][arm]=reading
                proofs[condition][arm]=dict(passed=True,full_snapshot_events=2401,generator_checkpoints=4201,
                    streams=instance_count,primitive_calls=len(effective['draw_log']))
                # Keep only matched initial construction arrays across conditions.
                if baseline_construction is None:baseline_construction={k:construction[k].copy() for k in ('src','good','cell','plus_y','ordinary_start','ordinary_head','ordinary_rot','cast_sign','flee_side','S0','SG0','UP0','SIL0','SINCE0','C0','ring0','codes0')}
                else:
                    for key,value in baseline_construction.items():same(construction[key],value,prefix+'/matched construction/'+key)
                del sample,construction,output,timeline,normals,masks,obs,stored_obs,stored_masks,anchors
                table.clear();arrays.clear()
        # Recheck immutable closure and bytes after the full read.
        _,postpair,postpin=preflight(root);require(postpair==pair and postpin==pin_hash,'post verification/source closure')
        require(identity['metrics_sha256_alpha']==digest((directory/'metrics.json').read_bytes()),'post verification/metrics bytes')
        return dict(complete=True,passed=True,smoke=smoke,source_closure_sha256_alpha=pins['source_closure_sha256_alpha'],
            execution_pins_sha256_alpha=pin_hash,identity_sha256_alpha=digest((directory/'identity.json').read_bytes()),
            metrics_sha256_alpha=identity['metrics_sha256_alpha'],raw_sha256_alpha=descriptor['sha256_alpha'],
            verifier_sha256_alpha=digest((root/'tools/verify_h17_r0.py').read_bytes()),first_failure=None,gates=proofs,readings=readings)
    finally:arrays.close()


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path);parser.add_argument('--smoke',action='store_true')
    parser.add_argument('--receipt',type=Path)
    args=parser.parse_args(argv);directory=args.output.resolve();target=(args.receipt or directory/'verification.json').resolve()
    require(target.parent==directory and target.name.endswith('.json') and target.name not in ('identity.json','metrics.json'),'verification/receipt path')
    try:receipt=verify(directory,ROOT,args.smoke);status=0
    except BaseException as exc:
        receipt=dict(complete=False,passed=False,smoke=args.smoke,first_failure=exc.first_failure if isinstance(exc,VerificationError)
            else dict(field='verification exception',index=None,phase=None),exception_type=type(exc).__name__,
            error_utf8_alpha=str(exc).encode('utf-8').hex().translate(AP))
        status=1
    payload=canonical(receipt)+b'\n'
    try:no_protected_tokens(payload,ROOT)
    except VerificationError as exc:
        receipt=dict(complete=False,passed=False,smoke=args.smoke,first_failure=exc.first_failure,
            details_utf8_alpha=payload.hex().translate(AP))
        payload=canonical(receipt)+b'\n';no_protected_tokens(payload,ROOT);status=1
    temporary=target.with_suffix(target.suffix+'.tmp')
    temporary.write_bytes(payload);temporary.replace(target)
    print('R0 independent verification '+('PASS' if status==0 else 'FAIL'),flush=True)
    return status


def no_protected_tokens(payload,root):
    protected=set();offsets=constants(root/'src/ph32.py')
    for name in ('ph33','ph35'):
        source=constants(root/('src/'+name+'.py'));seeds=source['SEEDS'];bench=source['BENCH']
        worlds=[seeds['dev'][0],seeds['eval'][0],bench['seed_w']]
        agents=[seeds['dev'][1],seeds['eval'][1],bench['seed_a']]
        protected.update([*seeds['dev'],*seeds['eval'],bench['seed_w'],bench['seed_a'],bench['boot']])
        protected.update(x+10000 for x in worlds);protected.update(x+20000 for x in agents)
        protected.update(x+20000 for x in worlds)
        protected.update((bench['seed_w']+10000000,bench['seed_a']+20000000))
        if name=='ph33':
            protected.update(x+offsets['D_OFF'] for x in worlds);protected.update(x+offsets['A3_OFF'] for x in agents)
    require(not any(re.search(rb'(?<!\d)'+str(n).encode()+rb'(?!\d)',payload) for n in protected),'P5/protected token')


if __name__=='__main__':raise SystemExit(main())
