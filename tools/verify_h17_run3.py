#!/usr/bin/env python3
"""Independent GS250 saved-evidence arithmetic. Imports only stdlib and NumPy.

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
THREADS=('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS')
for _name in THREADS:os.environ[_name]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import numpy as np


ROOT=Path(__file__).resolve().parents[1]
FINAL='experiments/h17/h17_run3_design_v3.md'
CONFIG='config/h17-run3-seeds.json'
REGISTRATION='experiments/h17/h17_run3_seed_registration.json'
SCHEMA='experiments/h17/h17_run3_evidence_schema.json'
KEYSETS='experiments/h17/h17_run3_array_keysets.json'
RUNTIME='experiments/h17/h17_run3_runtime.json'
SPEC='config/h17-run3-specification-pins.json'
BASEPINS='config/h17-run3-implementation-pins.json'
PINS='config/h17-run3-execution-pins.json'
OPENING='config/h17-run3-execution-opening.json'
REGISTRY='experiments/h17/run3_registry'
H0='experiments/h17/run3/H0'
AP=str.maketrans('0123456789abcdef','abcdefghijklmnop')
HEX=str.maketrans('abcdefghijklmnop','0123456789abcdef')
CONDITIONS=('C0','T1','W1','T3')
ARMS=('Fly','Passive','Agent17','GSOff','GS250')
Z=1.959963984540054
SAMPLE_FIELDS=tuple(('PRE_POS PRE_HEAD PRE_ROT H_pre H_post S_pre S_post SG_pre SG_post UP_pre UP_post Y '
 'SIL_pre SIL_base SIL_post SINCE_pre SINCE_post C_pre C_post PRES_pre PRES_post NAV TO EV '
 'base sustain negS negZ newz zreset withheld_N1_S withheld_N1_Z reset_drive EST TGT TURN cast_sign flee_side '
 'POS HEAD ROT C AT2 W_raw W_delivered source_uniforms probabilities wind_uniform wind_on turn_normal').split())
L1=('POS','HEAD','S','SG','H','NAV','SINCE','TGT','SIL','TO','EV','W','SUS','Z','AT2','C')
Z = 1.959963984540054


class VerificationError(RuntimeError):
    def __init__(self,field,index=None,phase=None,condition=None,arm=None):
        self.first_failure=dict(field=field,index=index,phase=phase,condition=condition,arm=arm)
        super().__init__(field)


def require(ok,field,index=None,phase=None):
    if not bool(ok):raise VerificationError(field,index,phase)


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
    out.update({k: world[k] for k in ('W0', 'SLOPE', 'LAM', 'LMAX', 'HIT_R', 'SPEED', 'ARENA')})
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

def observation(whiffs, reach, held, nav,marker=None):
    t, r, _ = whiffs.shape
    anyw = whiffs.any(2); anya = reach.any(2)
    q = np.zeros((t, r), np.int64); clock = np.zeros(r, np.int64)
    lastw = np.full((t, r), -1, np.int64); lastnav = np.full_like(lastw, -1)
    lw = np.full(r, -1, np.int64); ln = lw.copy()
    for i in range(t):
        clock = np.where(anyw[i], 0, clock + 1); q[i] = clock
        lw = np.where(anyw[i], i, lw); ln = np.where(nav[i], i, ln)
        lastw[i] = lw; lastnav[i] = ln
    mark = (q >= 250) & (held == -1) if marker is None else marker
    require(mark.dtype==np.dtype(bool) and mark.shape==(t,r),'reading/marker schema')
    m = first(mark); valid = m >= 0
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
        self.keys=tuple(keys);self.key_index=frozenset(self.keys)
        self.cache=OrderedDict();self.bytes=0;self.limit=limit
    def __iter__(self):return iter(self.keys)
    def __len__(self):return len(self.keys)
    def __getitem__(self,key):
        if key in self.cache:
            self.cache.move_to_end(key);return self.cache[key]
        require(key in self.key_index,'raw/unknown key')
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

def base_recurrence_check(sample, construction, c, label):
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
    return masks


def world_arithmetic_check(sample,construction,c,label):
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

def metric_reading(condition, sample, construction, masks,marker=None):
    w=sample['W_delivered']; at=sample['AT2']; h=sample['H_post']; nav=sample['NAV']
    t,r,_=w.shape
    obs=observation(w,at,h,nav,marker)
    valid=obs['marker_step']>=0
    lost=~w[-200:].any((0,2))
    reading=dict(primary=wilson(w.any((0,2)) if condition=='C0' else lost),
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
            primary=wilson(w.any((0,2)) if condition=='C0' else lost,select),
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

def pcg_state(state):
    require(type(state) is dict and set(state)=={'bit_generator','state','has_uint32','uinteger'},'PCG64/full native state fields')
    require(state['bit_generator']=='PCG64' and type(state['state']) is dict
        and set(state['state'])=={'state','inc'},'PCG64/engine and counter fields')
    require(all(type(state['state'][x]) is int and 0<=state['state'][x]<(1<<128) for x in ('state','inc'))
        and state['state']['inc']%2==1,'PCG64/native counters')
    require(type(state['has_uint32']) is int and state['has_uint32'] in (0,1)
        and type(state['uinteger']) is int and 0<=state['uinteger']<(1<<32),'PCG64/cached integer state')
    return state

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
        self.cache_bytes=0; self.cache_limit=32<<20;self.used=set()
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
        key=str(key);self.used.add(key)
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
        size=self.retained_size(result)
        if size<=self.cache_limit:
            while self.cache and (self.cache_bytes+size>self.cache_limit or len(self.cache)>=4096):
                _,(_,oldsize)=self.cache.popitem(last=False);self.cache_bytes-=oldsize
            self.cache[key]=(result,size);self.cache_bytes+=size
        return result

    def clear(self):
        self.cache.clear();self.cache_bytes=0

    @staticmethod
    def retained_size(value):
        seen=set()
        def size(x):
            if id(x) in seen:return 0
            seen.add(id(x))
            if isinstance(x,np.ndarray):return x.nbytes+sys.getsizeof(x)
            if isinstance(x,GeneratorState):return size(x.state)
            if isinstance(x,dict):return sys.getsizeof(x)+sum(size(k)+size(v) for k,v in x.items())
            if isinstance(x,(list,tuple,set)):return sys.getsizeof(x)+sum(size(v) for v in x)
            return sys.getsizeof(x)
        return size(value)

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
            return GeneratorState(pcg_state(state))
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

def draw_values(log, table):
    """Decode a complete primitive call; state equality is separately gated."""
    require(set(log)>={'generator','method','args','kwargs','result','before','after','step','phase'},'draw/log keyset')
    args=table.get(log['args']);kwargs=table.get(log['kwargs']);result=table.get(log['result'])
    require(isinstance(args,tuple) and isinstance(kwargs,dict) and isinstance(result,np.ndarray),'draw/call types')
    before=table.get(log['before']);after=table.get(log['after'])
    before=before.state if isinstance(before,GeneratorState) else before
    after=after.state if isinstance(after,GeneratorState) else after
    require(isinstance(before,dict) and isinstance(after,dict),'draw/state type')
    pcg_state(before);pcg_state(after)
    require(before.get('bit_generator')==after.get('bit_generator')=='PCG64','draw/bitgenerator')
    require(canonical_state(before)!=canonical_state(after),'draw/state unchanged')
    return args,kwargs,result,before,after

def canonical_state(value):
    """Insertion order intentionally retained for the historical repr hash."""
    return repr(value).encode('utf-8')

def call_shape(args, kwargs, method, shape, label):
    require(method in ('random','standard_normal'),'draw/method/'+label)
    require(len(args)==1 and not kwargs,'draw/exact original positional signature/'+label)
    size=args[0]
    actual=(size,) if isinstance(size,int) else tuple(size)
    require(actual==tuple(shape),'draw/size/'+label)

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
        act=by_phase.get((step,'base_act'),[])
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
    require(all(step==-1 or (0<=step<t and phase in ('sense','wind','twin','base_act')) for step,phase in by_phase),label+'/extra drawing phase')
    # Primitive calls on balance/code/cast/geometry roles may occur only in construction.
    for (step,phase),items in by_phase.items():
        if step>=0:require(all(g in worlds|{agent} for g,*_ in items),label+'/late construction draw')
    return {key:np.stack(value) for key,value in normals.items()}

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

def inherited_world_start(world_returns,c):
    """World4's retained source-index attribute, before World7's pose override."""
    x,ya,gap,unused_good,k,along,cross,unused_head=world_returns
    r=len(x);require(all(a.shape==(r,) for a in world_returns),'native world constructor row shapes')
    require(k.dtype==np.dtype('<i8') and np.isin(k,[0,1]).all(),'native World2 selected source')
    old_src=np.stack([np.stack([x,ya],1),np.stack([x,ya+gap],1)],1)
    half=c['W0']+c['SLOPE']*along
    old_y=np.clip(old_src[np.arange(r),k,1]+cross*half,0,c['ARENA'])
    # Match World4's separate source and pose translations before subtraction.
    return np.abs((old_y+60.)[:,None]-(old_src+60.)[:,:,1]).argmin(1)


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
    return inherited_world_start([entry[3] for entry in world],c)

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


def file_digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        while b:=f.read(1<<20):h.update(b)
    return h.hexdigest().translate(AP)


def scope(arm):return 'efficacy' if arm in ('Fly','GS250') else 'validity'


def prefix_of(condition,arm):return scope(arm)+'/'+condition+'/'+arm


def exact_keys(value,keys,label):
    require(isinstance(value,dict) and set(value)==set(keys),label+'/keys')


def value_same(a,b,label):
    if isinstance(a,np.ndarray) or isinstance(b,np.ndarray):same(a,b,label)
    elif isinstance(a,GeneratorState) or isinstance(b,GeneratorState):
        require(isinstance(a,GeneratorState) and isinstance(b,GeneratorState),label+'/generator type')
        require(canonical_state(a.state)==canonical_state(b.state),label+'/generator state')
    elif isinstance(a,dict) and isinstance(b,dict):
        exact_keys(a,b,label)
        for key in b:value_same(a[key],b[key],label+'/'+str(key))
    elif isinstance(a,(list,tuple)) and isinstance(b,type(a)):
        require(len(a)==len(b),label+'/length')
        for i,(x,y) in enumerate(zip(a,b)):value_same(x,y,label+'/'+str(i))
    elif a is MISSING or b is MISSING:require(a is b,label+'/missing')
    else:require(type(a) is type(b) and repr(a)==repr(b),label)


def source_schema(schema,key,descriptor,smoke):
    if key.startswith('blob/'):
        require(re.fullmatch('blob/[a-p]{64}',key) is not None,'schema/blob name')
        dtype=np.dtype(descriptor['dtype'])
        require(not dtype.hasobject and dtype.kind in schema['dtype_kinds'],'schema/blob dtype')
        return dict(dtype=dtype.str,shape=descriptor['shape'])
    rule=schema['arrays'].get(key);require(rule is not None,'schema/unregistered key/'+key)
    require(not smoke or not key.startswith('inference/'),'H0/inference array forbidden')
    dims=dict(T=600,R=40 if smoke else 400,E=3001,G=4801)
    return dict(dtype=rule['dtype'],shape=[dims.get(x,x) for x in rule['shape']])


def event_contract(record,t,label):
    expected=[dict(step=-1,phase='construction')]
    expected.extend(dict(step=i,phase=p) for i in range(t) for p in ('pre','base','pre_wrapper','wrapper','bump'))
    tree_same(record['events'],expected,label+'/events')


def native_header(metadata,condition,arm,label):
    tree_same(metadata,dict(world=condition,arm='Fly' if arm in ('Fly','Passive') else arm,
        G=2.,fixed=False,steps=600,draws_equal=True,rng_equal=True),label+'/independent native output header')


def gs_schedule(q_pre,delivered,held,cast_sign,base_tgt,base_turn,est,enabled=True):
    """Saved-input arithmetic only. No controller objects or noise generation."""
    q=np.where(delivered.any(-1),0,q_pre+1).astype(np.int64)
    eligible=(q>=250)&(held==-1);engaged=eligible&bool(enabled)
    u=np.where(engaged,q-250,-1).astype(np.int64)
    leg=np.zeros(q.shape,np.int64)
    # Integer boundaries avoid a floating inverse-triangle rounding convention.
    remaining=np.zeros(q.shape,np.int64);k=1
    while np.any(engaged&(leg==0)):
        bound=30*k*(k+1)//2;mask=engaged&(leg==0)&(u<bound)
        leg[mask]=k;remaining[mask]=bound-u[mask];k+=1
        require(k<=100,'gs/q out of registered horizon')
    sigma=np.where(engaged,cast_sign*np.where(leg%2==1,1,-1),0).astype(np.int8)
    alpha=np.where(engaged,np.where(u%300<150,1,-1),0).astype(np.int8)
    target=(180.0+sigma.astype(np.float64)*(90.0-alpha.astype(np.float64)*15.0))%360.0
    clip=np.clip(.6*((base_tgt-est+180)%360-180),-40,40)
    residual=base_turn-clip
    search_clip=np.clip(.6*((target-est+180)%360-180),-40,40)
    search=search_clip+residual
    return dict(q_pre=q_pre.copy(),q_post=q,u=u,leg=leg,remaining=remaining,eligible=eligible,
        engaged=engaged,sigma=sigma,alpha=alpha,BASE_TGT=base_tgt.copy(),BASE_TURN=base_turn.copy(),
        BASE_CLIP=clip,RESIDUAL=residual,SEARCH_TGT=np.where(engaged,target,base_tgt),
        SEARCH_CLIP=np.where(engaged,search_clip,clip),SEARCH_TURN=np.where(engaged,search,base_turn))


def gs_check(gs,sample,arm,label):
    t,r=sample['H_post'].shape;qpre=gs['q_pre']
    require(qpre.dtype==np.dtype('<i8') and qpre.shape==(t,r),label+'/q schema')
    same(qpre[0],np.zeros(r,np.int64),label+'/q initial')
    same(qpre[1:],gs['q_post'][:-1],label+'/q continuity')
    expected=gs_schedule(qpre,sample['W_delivered'],sample['H_post'],sample['cast_sign'],
        gs['BASE_TGT'],gs['BASE_TURN'],sample['EST'],arm=='GS250')
    expected['entry']=expected['engaged']&~np.concatenate([np.zeros((1,r),bool),expected['engaged'][:-1]])
    exact_keys(gs,expected,label+'/GS')
    for name,a in expected.items():same(gs[name],a,label+'/GS/'+name)
    same(sample['TGT'],expected['SEARCH_TGT'],label+'/executed target','wrapper')
    same(sample['TURN'],expected['SEARCH_TURN'],label+'/executed turn','wrapper')
    return expected


def endpoints(sample,construction,engaged,entry_mask=None):
    whiffs=sample['W_delivered'];at=sample['AT2'];r=whiffs.shape[1];rr=np.arange(r)
    dwell=at.sum(0,dtype=np.int64);good=construction['good'];dg=dwell[rr,good];do=dwell[rr,1-good]
    entry=engaged&~np.concatenate([np.zeros((1,r),bool),engaged[:-1]]) if entry_mask is None else entry_mask
    return dict(E=whiffs.any((0,2)),L=~whiffs[400:600].any((0,2)),V=dg>do,
        D_source=dwell,D_source_last200=at[400:600].sum(0,dtype=np.int64),D_good=dg,D_other=do,
        whiff_source=whiffs.any(0),reach_source=at.any(0),ever_engaged=engaged.any(0),
        first_entry_step=first(entry),entry_event_count=entry.sum(0,dtype=np.int64))


def anchor_check(anchor,sample,obs,gs,arm,label):
    r=sample['H_post'].shape[1];rr=np.arange(r)
    marker=first(gs['entry']) if arm=='GS250' else np.full(r,-1,np.int64) if arm=='GSOff' else obs['marker_step']
    valid=marker>=0;index=np.maximum(marker,0)
    exact_keys(anchor,set(SAMPLE_FIELDS)|{'anchor_valid','q_obs','last_whiff','last_nav'},label+'/anchor')
    same(anchor['anchor_valid'],valid,label+'/anchor validity')
    for name,a in sample.items():
        if name in ('TGT','TURN') and arm in ('GS250','GSOff'):a=gs['BASE_'+name]
        expected=a[index,rr].copy()
        expected[~valid]=-1 if arm=='GSOff' and expected.dtype.kind in 'iu' else 0
        same(anchor[name],expected,label+'/anchor/'+name)
    for name in ('q_obs','last_whiff','last_nav'):
        a=gs['q_post'] if name=='q_obs' and arm=='GS250' else obs[name]
        expected=a[index,rr].copy();expected[~valid]=-1
        same(anchor[name],expected,label+'/anchor/'+name)


def clause(interval,bar,direction,estimate):
    lo,hi=map(float,interval)
    require(math.isfinite(lo) and math.isfinite(hi) and lo<=hi,'clause/interval')
    status=('PASS' if lo>=bar else 'FAIL' if hi<bar else 'INCONCLUSIVE') if direction=='lower' else (
        'PASS' if hi<=bar else 'FAIL' if lo>bar else 'INCONCLUSIVE')
    return dict(estimate=float(estimate),interval=[lo,hi],bar=float(bar),direction=direction,status=status)


def paired_statistics(delta,indices):
    require(delta.dtype==np.dtype('<i8') and delta.shape==(400,),'inference/difference schema')
    require(indices.dtype==np.dtype('<i8') and indices.shape==(5000,400),'inference/indices schema')
    require(((indices>=0)&(indices<400)).all(),'inference/indices range')
    means=np.mean(delta[indices],axis=1,dtype=np.float64)
    interval=np.quantile(means,[.025,.975],method='linear')
    return means,interval


def all_clauses(endpoint_by_condition,indices):
    """Public root-recompute helper, sharing only saved row data and indices."""
    differences={};clauses={};statistics={}
    specs=(('C0','E',.10,'lower'),('T1','V',-.05,'lower'),('T3','V',-.05,'lower'),
           ('T1','L',.05,'upper'),('W1','L',.05,'upper'),('T3','L',.05,'upper'),
           ('W1','D_other',-6.,'lower'))
    for condition,field,bar,direction in specs:
        arms=endpoint_by_condition[condition]
        delta=arms['GS250'][field].astype(np.int64)-arms['Fly'][field].astype(np.int64)
        means,ci=paired_statistics(delta,indices);key=condition+'_'+field
        differences[key]=delta;statistics[key]=dict(replicate_mean=means,interval=ci)
        clauses[key]=clause(ci,bar,direction,delta.mean(dtype=np.float64))
    c0=wilson(endpoint_by_condition['C0']['GS250']['E'])
    t1=wilson(endpoint_by_condition['T1']['GS250']['ever_engaged'])
    clauses['C0_absolute']=clause(c0['interval'],.5,'lower',c0['estimate'])
    clauses['T1_intervention']=clause(t1['interval'],.05,'upper',t1['estimate'])
    verdict='PASS' if all(x['status']=='PASS' for x in clauses.values()) else (
        'NOT_SHOWN' if any(x['status']=='FAIL' for x in clauses.values()) else 'INCONCLUSIVE/NOT_SHOWN')
    return differences,statistics,clauses,verdict


def source_closure(pins):
    return digest(canonical({key:pins[key] for key in ('runtime','schema_sha256_alpha',
        'keysets_sha256_alpha','specification_pins_sha256_alpha','files_sha256_alpha')}))


def preflight(root=ROOT,smoke=False,stage='bench'):
    root=Path(root);schema=read(root/SCHEMA);keysets=read(root/KEYSETS);opening=read(root/OPENING)
    require(schema['complete'] is True and schema['version']=='h17-run3-evidence-v3','schema/frozen version')
    require(schema['execution_opened'] is False,'schema/specification scope')
    tree_same(schema['conditions'],list(CONDITIONS),'schema/conditions')
    tree_same(schema['sample_fields'],list(SAMPLE_FIELDS),'schema/sample fields')
    require(schema['expanded_keysets']['array_count']==len(keysets)==5580,'schema/main count')
    require(file_digest(root/KEYSETS)==schema['expanded_keysets']['sha256_alpha'],'schema/keysets bytes')
    infer={key for key in keysets if key.startswith('inference/')}
    require(infer==set(schema['mode_keysets']['H0']['inference_excluded_keys']) and len(infer)==24,'schema/H0 exact exclusion')
    require(schema['mode_keysets']['H0']['array_count']==len(keysets)-len(infer)==5556,'schema/H0 count')
    names=read(root/'experiments/module/identity.json')['A1']['L2']['names']
    for arm in ARMS:
        expected=sorted(names['common']+(names['ref_only'] if arm=='Agent17' else names['cand_only'])+
            (['q'] if arm in ('GS250','GSOff') else []))
        tree_same(schema['fieldsets'][arm],expected,'schema/original fieldsets/'+arm)
    require(opening['complete'] is True and opening['decision']=='decision:h17-run3-open'
        and opening['candidate']=='GS250' and opening['adoption']=='none','opening/authority')
    require(opening['authorized']['spent_input_H0'] is True and
        opening['authorized']['one_fresh_BENCH_after_H0_PASS'] is True,'opening/authorized sequence')
    require(opening['MAIN_rows']==400 and opening['H0_rows']==40 and opening['ticks']==600
        and opening['required_clauses']==9 and opening['registry']==REGISTRY,'opening/fixed contract')
    tree_same(opening['conditions'],list(CONDITIONS),'opening/conditions')
    check_source_files(root,opening['immutable_specification_files_sha256_alpha'])
    specification=read(root/SPEC)
    require(specification['complete'] is True and specification['candidate_confirmed'] is True
        and specification['q_contract_signed'] is True and specification['execution_opened'] is False
        and specification['implementation_complete'] is False and specification['H0_complete'] is False,
        'specification/authority and scope')
    check_source_files(root,specification['files_sha256_alpha'])
    path=root/(BASEPINS if smoke else PINS);pins=read(path)
    basekeys={'complete','decision','runtime','schema_sha256_alpha','keysets_sha256_alpha',
        'specification_pins_sha256_alpha','files_sha256_alpha','source_closure_sha256_alpha'}
    exact_keys(pins,basekeys if smoke else basekeys|{'base_pins_sha256_alpha','h0'},'pins')
    require(pins['complete'] is True and pins['decision']=='decision:h17-run3-open','pins/complete authority')
    require(pins['source_closure_sha256_alpha']==source_closure(pins),'pins/stable closure')
    for key,path0 in (('schema_sha256_alpha',SCHEMA),('keysets_sha256_alpha',KEYSETS),('specification_pins_sha256_alpha',SPEC)):
        require(pins[key]==file_digest(root/path0),'pins/'+key)
    actual=runtime_stamp();tree_same(pins['runtime'],actual,'runtime/actual vs pins')
    tree_same(read(root/RUNTIME)['runtime'],actual,'runtime/frozen specification')
    require(actual['python']=='3.13.12' and actual['numpy']=='2.5.3' and actual['optimize']==0
        and actual['assertions_enabled'] is True and actual['pointer_bits']==64 and actual['byteorder']=='little'
        and actual['processes']==1 and all(x=='1' for x in actual['threads'].values()),'runtime/platform contract')
    # Every newly introduced transitive Python source must be frozen too.
    required=set(specification['files_sha256_alpha'])|set(opening['immutable_specification_files_sha256_alpha'])|{
        OPENING,'src/h17_run3_arm.py','tools/h17_run3_recording.py','tools/measure_h17_run3.py',
        'tools/recompute_h17_run3.py','tests/test_recompute_h17_run3.py','experiments/h17/h17_run3_implementation_amendment_v1.md',
        'notes/reviews/2026-10-10-h17-run3-execution-review.md',
        'experiments/h17/h17_run3_implementation_checks.json','experiments/h17/h17_run3_execution_opening_checks.json',
        'tools/check_h17_run3_boundaries.py','experiments/h17/h17_run3_native_boundary_checks.json',
        'tools/h17_run3_archive_candidate.py','tests/test_h17_run3_archive_candidate.py',
        'experiments/h17/run3_H0_attempt1/sources/h17_run3_recording.py',
        'tools/verify_h17_run3.py','tests/test_h17_run3.py','tests/test_verify_h17_run3.py'}
    required|={p.relative_to(root).as_posix() for p in (root/'src').glob('*.py')}
    require(required<=set(pins['files_sha256_alpha']),'pins/complete transitive source inventory')
    require(not any(name.startswith(H0+'/') or name in (BASEPINS,PINS) for name in pins['files_sha256_alpha']),
        'pins/H0 cycle exclusion')
    check_source_files(root,pins['files_sha256_alpha'])
    config=read(root/CONFIG);reg=read(root/REGISTRATION);numbers=[]
    for mode in ('bench','dev','eval'):
        pair=config[mode];boot=config['inference'][mode]
        require(type(pair) is list and len(pair)==2 and all(type(x) is int and x>=0 for x in pair)
            and type(boot) is int and boot>=0,'registration/role types')
        w,a=pair;roles=dict(world=w,agent=a,inference=boot,world_balance=w+10000,c0_geometry=w+20000,cast=a+20000)
        tree_same(reg['stages'][mode],roles,'registration/roles/'+mode)
        numbers.extend(roles.values())
    require(len(numbers)==len(set(numbers))==18 and set(reg['numbers'])==set(numbers),'registration/disjoint roles')
    require(reg['complete'] is True and reg['local_scan']['passed'] is True
        and reg['local_scan']['hits']==[] and reg['local_scan']['errors']==[]
        and reg['graph_scan']['passed'] is True and reg['graph_scan']['literal_hits']==[]
        and reg['graph_scan']['all_canonical_read_verified'] is True,'registration/complete scan receipts')
    if not smoke:
        base=read(root/BASEPINS);require(pins['base_pins_sha256_alpha']==file_digest(root/BASEPINS),'pins/base bytes')
        for key in basekeys:tree_same(pins[key],base[key],'pins/MAIN stable base/'+key)
        h0=pins['h0'];exact_keys(h0,{'identity_sha256_alpha','metrics_sha256_alpha','raw_sha256_alpha',
            'verification_sha256_alpha','parent_recomputation_sha256_alpha','source_closure_sha256_alpha'},'pins/H0 receipts')
        require(h0['source_closure_sha256_alpha']==pins['source_closure_sha256_alpha'],'H0/matching stable closure')
        for name,key in (('identity.json','identity'),('metrics.json','metrics'),('raw.npz.ap','raw'),
            ('verification.json','verification'),('parent_recomputation.json','parent_recomputation')):
            require(file_digest(root/H0/name)==h0[key+'_sha256_alpha'],'H0/pinned '+name)
            if name.endswith('.json'):
                saved=read(root/H0/name);require(saved['complete'] is True and saved['smoke'] is True,'H0/complete '+name)
                if key!='metrics':require(saved['passed'] is True,'H0/pass '+name)
                if key=='parent_recomputation':
                    require(saved['source_closure_sha256_alpha']==pins['source_closure_sha256_alpha'],'H0/parent closure')
                else:
                    require(saved['provenance']['source_closure_sha256_alpha']==pins['source_closure_sha256_alpha'],'H0/base provenance')
                    require(saved['provenance']['execution_pins_sha256_alpha']==pins['base_pins_sha256_alpha'],'H0/base pin hash')
    schema=dict(schema,arrays=keysets)
    return pins,config,schema,file_digest(path)


def expected_provenance(root,pins,pin_hash):
    return dict(runtime=pins['runtime'],source_closure_sha256_alpha=pins['source_closure_sha256_alpha'],
        execution_pins_sha256_alpha=pin_hash,**{key:file_digest(Path(root)/path) for key,path in (
        ('design_sha256_alpha',FINAL),('seed_config_sha256_alpha',CONFIG),('seed_registration_sha256_alpha',REGISTRATION),
        ('schema_sha256_alpha',SCHEMA),('keysets_sha256_alpha',KEYSETS),('runtime_sha256_alpha',RUNTIME),
        ('specification_pins_sha256_alpha',SPEC),('opening_sha256_alpha',OPENING))})


def generator_checkpoints(arrays,record,prefix,table,condition,steps):
    labels=[dict(step=-1,phase='construction')]
    labels.extend(dict(step=t,phase=p) for t in range(steps) for p in
        ('before','sense','wind','twin','base_act','wrapper','move','bump'))
    tree_same(record['rng_labels'],labels,prefix+'/RNG labels')
    roles=[x['role'] for x in record['generator_instances']];states=arrays[prefix+'/rng_timeline']
    require(states.dtype==np.dtype('S64') and states.shape==(len(labels),len(roles)),prefix+'/RNG timeline')
    previous=[]
    for inst in record['generator_instances']:
        val=table.get(inst['initial']);require(isinstance(val,GeneratorState),prefix+'/initial generator')
        previous.append(val.state)
    calls={}
    for log in record['draw_log']:calls.setdefault((log['step'],log['phase']),[]).append(log)
    for i,label in enumerate(labels):
        for log in calls.get((label['step'],label['phase']),[]):
            g=log['generator'];_,_,_,before,after=draw_values(log,table)
            require(canonical_state(previous[g])==canonical_state(before),prefix+'/RNG call continuity',[label['step'],g],label['phase'])
            previous[g]=after
        for g in range(len(roles)):
            value=table.get(states[i,g]);require(isinstance(value,GeneratorState),prefix+'/RNG state type')
            require(canonical_state(value.state)==canonical_state(previous[g]),prefix+'/every stream phase',[label['step'],g],label['phase'])
        if condition=='W1' and label['phase'] in ('construction','twin','base_act','wrapper','move','bump'):
            require(canonical_state(previous[roles.index('world')])==canonical_state(previous[roles.index('twin')]),prefix+'/twin RNG coupling')
    return states


def initial_state_check(initial,construction,c,label,gs=False):
    r=len(construction['good'])
    scalars={'R':r,'G':c['G_STAR'],'N':200,'N_hi':200,'P':60,'up.n':c['UP_N'],
        'up.sig_n':c['UP_SIG']**c['UP_N'],'up.Rmax':c['UP_RMAX'],'up.k':c['UP_K'],'up.tau':c['UP_TAU'],
        'sel.R':r,'sel.n':2,'sel.w_i':c['C_WI'],'sel.g':c['C_G'],'sel.theta':c['C_THETA'],
        'sel.k':c['C_K'],'sel.tau':c['C_TAU'],'sel.tau_g':c['C_TAUG'],'sel.gsat':None,'sel.noise':c['C_NOISE'],
        'sel.pool_p':c['C_POOLP'],'sel.pool_c':c['C_POOLC'],'ring.R':r,'ring.n':c['RING_N'],
        'ring.p':c['RING_P'],'ring.sigma':c['RING_SIGMA'],'ring.c':c['RING_C'],'ring.Rmax':c['RING_RMAX'],
        'ring.tau':c['RING_TAU'],'ring.vgain':c['RING_VGAIN'],'ring.noise':c['RING_NOISE'],
        'ring.J':c['RING_J'],'ring.width':c['RING_WIDTH'],'mb.R':r,'mb.K':c['MB_K'],'mb.C':c['MB_C'],
        'mb.sparsity':c['MB_SPARSITY'],'mb.eta_d':c['MB_ETA_D'],'mb.eta_p':c['MB_ETA_P'],
        'mb.tau_code':c['MB_TAU_CODE'],'mb.tau_reinf':c['MB_TAU_REINF'],'mb.wmin':c['MB_WMIN'],
        'mb.wmax':c['MB_WMAX'],'mb.beta':c['MB_BETA'],'mb.parallel':False,'mb.gated':True}
    if 'nch' in initial:scalars['nch']=2
    for name,value in scalars.items():value_same(initial[name],value,label+'/initial '+name)
    for field,key in (('sel.s','S0'),('up.P','UP0'),('silence','SIL0'),('since','SINCE0'),
        ('c','C0'),('known','known'),('ring.s','ring0'),('codes','codes0'),('cast_sign','cast_sign'),('flee_side','flee_side')):
        same(initial[field],construction[key],label+'/construction '+key)
    same(initial['sel.S'][:,0],construction['SG0'],label+'/initial pool')
    for key in ('S0','SG0','UP0','SIL0','SINCE0','ring0'):require(not construction[key].any(),label+'/cold '+key)
    same(construction['C0'],np.full((r,2),140.),label+'/presence initial')
    same(initial['mb.w'],np.full((r,4,200),c['MB_W0']),label+'/initial weights')
    same(initial['mb.tc'],np.zeros((r,200)),label+'/initial code trace')
    same(initial['mb.tr'],np.zeros((r,4)),label+'/initial reinforcer trace')
    same(initial['present'],np.ones((r,2),bool),label+'/initial present')
    for field in ('last_turn','est','tgt'):same(initial[field],np.zeros(r),label+'/initial '+field)
    for field in ('nav_hit','due_timeout','due_evidence','sustain','zreset'):
        same(initial[field],np.zeros(r,bool),label+'/initial '+field)
    n=c['RING_N'];ii=np.arange(n)[:,None];jj=np.arange(n)[None,:]
    same(initial['ring.o'],((ii-jj+n//2)%n)-n//2,label+'/ring offsets')
    same(initial['ring.ang'],2*np.pi*np.arange(n)/n,label+'/ring angles')
    if 'abl' in initial:
        for field,value in dict(abl=set(),cast='return',rot_in='made',fix=True,filt=True,rule=True,scope='prior',release=True).items():
            value_same(initial[field],value,label+'/lineage native construction/'+field)
        for field in ('belief','prev'):same(initial[field],np.zeros(r),label+'/lineage initial '+field)
        for field in ('nav6','nav8','differs','differs8'):same(initial[field],np.zeros(r,bool),label+'/lineage initial '+field)
        same(initial['yp'],np.zeros((r,2)),label+'/lineage initial upstream diagnostic')
        for field in ('n2S','n2Z'):require(initial[field] is MISSING,label+'/lineage not-yet-created '+field)
    if gs:same(initial['q'],np.zeros(r,np.int64),label+'/initial q')


def snapshot_sample_check(timeline,sample,construction,gs,arm,arrays,prefix,c):
    """Full original call identity, not just a selection of convenient fields."""
    t,r=sample['H_post'].shape;initial=timeline.row(0)
    initial_state_check(initial,construction,c,prefix,arm in ('GS250','GSOff'))
    links={'S':'sel.s','SG':'sel.S','UP':'up.P','SIL':'silence','SINCE':'since','C':'c','PRES':'present'}
    rng=arrays[prefix+'/rng_timeline'];agent=4 if prefix.split('/')[1]=='W1' else 2
    base=sample.copy()
    if arm in ('GS250','GSOff'):base.update(TGT=gs['BASE_TGT'],TURN=gs['BASE_TURN'])
    rings=[]
    for i in range(t):
        pre,core,act,wrapped,bump=(1+5*i+j for j in range(5));before=timeline.row(pre)
        expected=dict(before)
        if i:
            for field in timeline.fields:value_same(before[field],timeline.get(bump-5,field),prefix+'/full tick continuity/'+field)
        for name,field in links.items():
            value=before[field][:,0] if name=='SG' else before[field]
            same(sample[name+'_pre'][i],value,prefix+'/sample '+name+'_pre')
            expected[field]=sample[name+'_post'][i,:,None] if name=='SG' else sample[name+'_post'][i]
        for name,field in (('EST','est'),('NAV','nav_hit'),('TO','due_timeout'),('EV','due_evidence'),
            ('sustain','sustain'),('zreset','zreset'),('TGT','tgt'),('TURN','last_turn')):
            expected[field]=base[name][i]
        expected['ring.s']=timeline.get(act,'ring.s');rings.append(expected['ring.s'])
        for field in ('rng','sel.rng','ring.rng','mb.rng'):
            value_same(before[field],timeline.table.get(rng[1+8*i,agent]),prefix+'/pre RNG '+field)
            expected[field]=timeline.table.get(rng[5+8*i,agent])
        if arm=='Agent17':
            # Full common-state identity plus these native lineage measurements.
            for field,name in (('n2S','withheld_N1_S'),('n2Z','withheld_N1_Z'),('yp','Y')):
                expected[field]=sample[name][i]
            h=sample['H_post'][i];wh=sample['W_delivered'][i];known=construction['known'];rr=np.arange(r)
            hit=(h>=0)&wh[rr,np.maximum(h,0)];vmax=known.max(1);top=(known>=0)&(known==vmax[:,None]);vh=known[rr,np.maximum(h,0)]
            expected['nav6']=hit|((h<0)&(wh&(known>=0)).any(1))
            expected['nav8']=np.where((h>=0)&((vh==vmax)|(vh<0)),hit,(wh&top).any(1))
            expected['differs']=sample['NAV'][i]!=expected['nav6'];expected['differs8']=sample['NAV'][i]!=expected['nav8']
            # Agent9's active path does not update these inherited fields.
            for field in ('prev','rot_in'):expected[field]=before[field]
        for field in timeline.fields:
            value_same(timeline.get(act,field),expected[field],prefix+'/complete original act/'+field)
            core_expected=before[field] if field in ('sustain','zreset','q','n2S','n2Z') else (
                sample['SIL_base'][i] if field=='silence' else expected[field])
            value_same(timeline.get(core,field),core_expected,prefix+'/core phase/'+field)
        after=dict(expected)
        if arm in ('GS250','GSOff'):
            after.update(q=gs['q_post'][i],tgt=sample['TGT'][i],last_turn=sample['TURN'][i])
            same(before['q'],gs['q_pre'][i],prefix+'/snapshot q_pre')
        for field in timeline.fields:
            value_same(timeline.get(wrapped,field),after[field],prefix+'/wrapper only q/commands/'+field)
            value_same(timeline.get(bump,field),after[field],prefix+'/original walls-off bump/'+field)
        for field in ('cast_sign','flee_side'):same(sample[field][i],before[field],prefix+'/sign '+field)
    return np.stack(rings)


def world_snapshot_check(arrays,record,prefix,table,sample,construction,condition,label,native_start):
    fields=record['world_fields'];events=record['events'];refs=arrays[prefix+'/world_timeline']
    initial={field:table.get(refs[0,j]) for j,field in enumerate(fields)}
    require(initial['walls'] is False and initial['t']==0,'world/initial walls/clock')
    dynamic={'pos','head','rot','t','bumped','rng','plume','raw'}
    for index,event in enumerate(events):
        state={field:table.get(refs[index,j]) for j,field in enumerate(fields)}
        for field in set(fields)-dynamic:value_same(state[field],initial[field],label+'/immutable world '+field)
        require(state['walls'] is False and state['p_d']==0 and state['p_wind']==1.
            and state['p_hit']==.3,label+'/world constants')
        if event['step']<0:
            same(state['pos'],construction['start'],label+'/world initial position')
            same(state['head'],construction['head0'],label+'/world initial heading')
            same(state['rot'],construction['rot0'],label+'/world initial rotation')
        else:
            i=event['step'];post=event['phase']=='bump'
            for field,pre,after in (('pos','PRE_POS','POS'),('head','PRE_HEAD','HEAD'),('rot','PRE_ROT','ROT')):
                same(state[field],sample[after if post else pre][i],label+'/world '+field,event['phase'])
            require(state['t']==i+int(post),label+'/world clock',[i],event['phase'])
            if event['phase'] in ('base','pre_wrapper','wrapper','bump'):
                same(state['plume'],sample['W_delivered'][i].any(1),label+'/world plume')
                if condition=='W1':same(state['raw'],sample['W_raw'][i],label+'/masked raw')
            checkpoint=1+8*i if event['phase']=='pre' else 8+8*i if post else 5+8*i
            value_same(state['rng'],table.get(arrays[prefix+'/rng_timeline'][checkpoint,0]),label+'/world RNG link')
        require(not state['bumped'].any(),label+'/no contacts')
        for field in ('src','good','cell','plus_y','start'):
            expected=native_start if field=='start' else construction[field]
            same(state[field],expected,label+'/source field '+field)
        if condition=='W1':
            same(state['pres'],1-construction['good'],label+'/masked present source identity')
            same(state['absent'],construction['good'],label+'/masked absent source identity')


def input_return_check(arrays,record,prefix,table,sample,gs,arm):
    for i in range(sample['H_post'].shape[0]):
        inp=table.get(arrays[prefix+'/input_timeline'][i]);ret=table.get(arrays[prefix+'/return_timeline'][i])
        baseret=table.get(arrays[prefix+'/base_return_timeline'][i])
        require(type(inp) is tuple and len(inp)==6 and type(ret) is tuple and len(ret)==2
            and type(baseret) is tuple and len(baseret)==2,prefix+'/native input/return types')
        for a,name in zip(inp[:3],('PRE_POS','PRE_HEAD','PRE_ROT')):same(a,sample[name][i],prefix+'/input '+name)
        require(type(inp[3]) is int and inp[3]==i,prefix+'/input clock')
        same(inp[4],sample['W_delivered'][i],prefix+'/input delivered');same(inp[5],sample['wind_on'][i],prefix+'/input wind')
        same(ret[0],sample['TURN'][i],prefix+'/executed return');same(ret[1],sample['H_post'][i],prefix+'/held return')
        same(baseret[0],gs['BASE_TURN'][i] if arm in ('GS250','GSOff') else sample['TURN'][i],prefix+'/base return turn')
        same(baseret[1],sample['H_post'][i],prefix+'/base return hold')


def transcript_order(record,condition,rows,steps,label,schema):
    roles=[x['role'] for x in record['generator_instances']]
    construction=['world']*8+['balance']
    if condition=='W1':construction+=['twin']*8+['twin_balance']
    construction+=['code0']*rows+['code1']*rows+['agent','cast']
    if condition=='C0':construction+=['geometry']*6
    actual=[]
    for log in record['draw_log']:
        exact_keys(log,schema['primitive_record_fields'],label+'/primitive')
        require(type(log['generator']) is int and 0<=log['generator']<len(roles),label+'/generator index')
        actual.append((log['step'],log['phase'],roles[log['generator']]))
    expected=[(-1,'construction',role) for role in construction]
    for i in range(steps):
        expected.extend([(i,'sense','world')]*2+[(i,'wind','world')])
        if condition=='W1':expected.extend([(i,'twin','twin')]*3)
        expected.extend([(i,'base_act','agent')]*4)
    require(actual==expected,label+'/exact global primitive order')
    for creation in record['generator_instances']:
        exact_keys(creation,schema['creation_record_fields'],label+'/creation descriptor')


def disabled_coupling(arrays,records,condition,schema):
    reference=records[condition]['Fly'];rp=prefix_of(condition,'Fly')
    for arm in ('Passive','Agent17','GSOff'):
        record=records[condition][arm];prefix=prefix_of(condition,arm)
        for groupname in ('output','sample','construction','twin'):
            left=group(arrays,rp+'/'+groupname+'/');right=group(arrays,prefix+'/'+groupname+'/')
            exact_keys(right,left,prefix+'/disabled '+groupname)
            for key in left:same(right[key],left[key],prefix+'/disabled '+groupname+'/'+key)
        tables=('world_timeline','rng_timeline','input_timeline','base_return_timeline','return_timeline')+(
            ('twin_input_timeline','twin_return_timeline') if condition=='W1' else ())
        for name in tables:
            same(arrays[prefix+'/'+name],arrays[rp+'/'+name],prefix+'/disabled '+name)
        fields=set(schema['fieldsets']['Fly'])
        if arm=='Agent17':fields&=set(record['state_fields'])
        full_snapshot_check(arrays[rp+'/attribute_hashes'],arrays[prefix+'/attribute_hashes'],
            reference,record,sorted(fields),prefix+'/disabled full original identity')
    # Efficacy coupling preserves common draws, not inputs/world trajectories.
    gp=prefix_of(condition,'GS250');candidate=records[condition]['GS250']
    same(arrays[gp+'/rng_timeline'],arrays[rp+'/rng_timeline'],gp+'/matched original generator phases')
    for key in group(arrays,rp+'/construction/'):
        same(arrays[gp+'/construction/'+key],arrays[rp+'/construction/'+key],gp+'/matched construction/'+key)
    for a,b in zip(candidate['generator_instances'],reference['generator_instances']):
        for key in ('index','role','seed_args','seed_kwargs','initial','state_type'):
            tree_same(a[key],b[key],gp+'/matched creation/'+key)
    for field in ('source_uniforms','wind_uniform','turn_normal'):
        same(arrays[gp+'/sample/'+field],arrays[rp+'/sample/'+field],gp+'/matched primitive returns/'+field)


def own_state_proof(proof,record,timeline,arrays,prefix,table,gs,sample,arm,schema):
    exact_keys(proof,schema['metadata_keysets']['base_act_proof'],prefix+'/base proof')
    p=proof['same_state'];exact_keys(p,schema['metadata_keysets']['same_state_proof'],prefix+'/same-state proof')
    if arm not in ('GS250','GSOff'):
        require(p['method']=='not_applicable_lineage' and p['first_failure'] is None,prefix+'/lineage proof mode')
        for key in set(p)-{'method','first_failure'}:require(p[key] is None,prefix+'/lineage unused proof')
        require(proof['plain_logger_H0'] is None,prefix+'/lineage unused plain proof');return
    require(p['method']=='unchanged_Fly_act_recorded_primitives' and p['first_failure'] is None,prefix+'/proof method')
    t=sample['H_post'].shape[0];fields=[x for x in timeline.fields if x!='q']
    for key in set(p)-{'method','first_failure'}:require(type(p[key]) is list and len(p[key])==t,prefix+'/complete proof '+key)
    agent=next(i for i,x in enumerate(record['generator_instances']) if x['role']=='agent')
    for i in range(t):
        before={field:timeline.get(1+5*i,field) for field in fields}
        expected={field:timeline.get(3+5*i,field) for field in fields}
        value_same(table.get(p['pre_state_refs'][i]),before,prefix+'/proof own pre state')
        require(p['input_refs'][i]==bytes(arrays[prefix+'/input_timeline'][i]).decode(),prefix+'/proof own input reference')
        actual_logs=[x for x in record['draw_log'] if x['step']==i and x['phase']=='base_act' and x['generator']==agent]
        require(len(actual_logs)==4,prefix+'/proof own exact primitive budget')
        require(type(p['primitive_refs'][i]) is list and len(p['primitive_refs'][i])==4,prefix+'/proof four primitives')
        for ref,log in zip(p['primitive_refs'][i],actual_logs):value_same(table.get(ref),log,prefix+'/proof own primitive')
        value_same(table.get(p['expected_state_refs'][i]),expected,prefix+'/proof independently checked full original result')
        value_same(table.get(p['expected_return_refs'][i]),(gs['BASE_TURN'][i],sample['H_post'][i]),prefix+'/proof base return')
        value_same(table.get(p['comparison_refs'][i]),dict(passed=True,fields=fields),prefix+'/proof complete field coverage')


def plain_logger_proof(proof,arrays,record,prefix,table,smoke,schema):
    p=proof['plain_logger_H0']
    if not smoke or prefix.split('/')[-1]!='GS250':
        require(p is None,prefix+'/plain proof mode');return
    exact_keys(p,schema['metadata_keysets']['plain_logger_H0_proof'],prefix+'/plain logger proof')
    require(p['candidate_class']=='GS250' and p['spent_pair_alias']=='h29/smoke'
        and p['first_failure'] is None,prefix+'/plain proof identity')
    # These references contain the literal uninstrumented candidate's complete
    # saved output/timelines, never an inferred claim that instrumentation passed.
    require(p['method']=='literal_GS250_vs_logged_GS250_full_run',prefix+'/plain proof method')
    outputs=table.get(p['native_outputs_ref']);expected=group(arrays,prefix+'/output/')
    exact_keys(outputs,set(expected)|set(record['output_metadata']),prefix+'/plain output keys')
    for name in expected:same(outputs[name],expected[name],prefix+'/plain output/'+name)
    for name,value in record['output_metadata'].items():value_same(outputs[name],value,prefix+'/plain metadata/'+name)
    state=table.get(p['state_refs']);world=table.get(p['world_refs']);rng=table.get(p['rng_refs'])
    exact_keys(state,{'timeline','fields','events','attribute_hashes'},prefix+'/plain states')
    exact_keys(world,{'timeline','fields','events'},prefix+'/plain worlds')
    exact_keys(rng,{'timeline','labels','instances'},prefix+'/plain generators')
    for actual,key,fields in ((state,'state_timeline','state_fields'),(world,'world_timeline','world_fields')):
        tree_same(actual['fields'],record[fields],prefix+'/plain '+fields)
        tree_same(actual['events'],record['events'],prefix+'/plain complete events')
        same(actual['timeline'],arrays[prefix+'/'+key],prefix+'/plain complete '+key)
    same(state['attribute_hashes'],arrays[prefix+'/attribute_hashes'],prefix+'/plain complete native hashes')
    tree_same(rng['labels'],record['rng_labels'],prefix+'/plain complete RNG labels')
    same(rng['timeline'],arrays[prefix+'/rng_timeline'],prefix+'/plain complete RNG states')
    # Literal and tapped objects have distinct handles, but their created streams,
    # seed arguments and initial bit-generator states must be identical.
    require(len(rng['instances'])==len(record['generator_instances']),prefix+'/plain stream inventory')
    for left,right in zip(rng['instances'],record['generator_instances']):
        exact_keys(left,right,prefix+'/plain creation fields')
        for field in set(right)-{'handle_type'}:value_same(left[field],right[field],prefix+'/plain creation/'+field)
        require(left['handle_type']=='Generator',prefix+'/literal Generator handle')
    same(table.get(p['input_refs']),arrays[prefix+'/input_timeline'],prefix+'/plain all inputs')
    returns=table.get(p['return_refs']);exact_keys(returns,{'actual','base'},prefix+'/plain returns')
    same(returns['actual'],arrays[prefix+'/return_timeline'],prefix+'/plain actual returns')
    same(returns['base'],arrays[prefix+'/base_return_timeline'],prefix+'/plain original returns')
    construction=table.get(p['construction_refs']);expected=group(arrays,prefix+'/construction/')
    value_same(construction,expected,prefix+'/plain construction')
    comparison=table.get(p['comparison_refs'])
    value_same(comparison,dict(passed=True,fields=record['state_fields'],world_fields=record['world_fields'],
        events=record['events'],rng_labels=record['rng_labels']),prefix+'/plain full comparison coverage')


def inference_check(arrays,metadata,table,seed,schema):
    exact_keys(metadata,schema['metadata_keysets']['inference_record'],'inference metadata')
    require(metadata['role']=='INFERENCE' and metadata['replicates']==5000
        and metadata['quantile_method']=='linear' and metadata['indices_key']=='inference/indices','inference/method')
    creation=metadata['creation'];exact_keys(creation,schema['creation_record_fields'],'inference creation')
    require(creation['role']=='inference' and creation['index']==0 and creation['state_type']=='PCG64'
        and creation['handle_type']=='Generator','inference/creation role')
    value_same(table.get(creation['seed_args']),(seed,),'inference/registered role')
    value_same(table.get(creation['seed_kwargs']),{},'inference/creation kwargs')
    require(creation['initial']==metadata['initial_state'],'inference/initial reference')
    refs=arrays['inference/call_refs'];require(refs.shape==(1,),'inference/exactly one primitive')
    call=table.get(refs[0]);value_same(call,metadata['primitive'],'inference/primitive reference')
    exact_keys(call,schema['primitive_record_fields'],'inference primitive fields')
    require(call['generator']==0 and call['method']=='integers' and call['step']==-1
        and call['phase']=='inference','inference/one declared call')
    args,kwargs,result,before,after=draw_values(call,table)
    require(args==(0,400) and kwargs.get('size')==(5000,400) and kwargs.get('endpoint') is False
        and kwargs.get('dtype')=='<i8' and set(kwargs)=={'size','dtype','endpoint'},'inference/exact call signature')
    initial=table.get(metadata['initial_state']);final=table.get(metadata['final_state'])
    require(isinstance(initial,GeneratorState) and isinstance(final,GeneratorState),'inference/typed PCG state')
    require(canonical_state(initial.state)==canonical_state(before) and canonical_state(final.state)==canonical_state(after),
        'inference/initial final call states')
    checkpoint=arrays['inference/checkpoints'];require(checkpoint.shape==(2,),'inference/two checkpoints')
    value_same(table.get(checkpoint[0]),initial,'inference/initial checkpoint')
    value_same(table.get(checkpoint[1]),final,'inference/final checkpoint')
    indices=arrays['inference/indices'];same(indices,result,'inference/raw integer return')
    require(indices.dtype==np.dtype('<i8') and indices.shape==(5000,400)
        and ((indices>=0)&(indices<400)).all(),'inference/index shape/range')
    require(metadata['indices_sha256_alpha']==array_descriptor(indices)['sha256_alpha'],'inference/indices hash')
    return indices


def claim_check(identity,directory,root,pins,config,schema,stage,smoke):
    if smoke:
        require(identity['claim'] is None,'H0/claim forbidden');return
    pair=config[stage];key=digest(canonical(pair));path=Path(root)/REGISTRY/(key+'.json')
    require(identity['claim']==path.relative_to(root).as_posix(),'claim/pair-only registry path')
    claim=read(path);exact_keys(claim,schema['metadata_keysets']['claim'],'claim')
    require(claim['format']=='h17-run3-claim-v3' and claim['complete'] is True
        and claim['pair_sha256_alpha']==key and claim['stage']==stage,'claim/completed registered pair')
    prov=identity['provenance']
    for field in set(prov)-{'runtime'}:require(claim[field]==prov[field],'claim/provenance '+field)
    require(claim['H0_sha256_alpha']==pins['h0']['verification_sha256_alpha'],'claim/matching H0')
    require(claim['output_path_sha256_alpha']==digest(str(Path(directory).resolve()).encode('utf-8')),'claim/output path')
    roles=read(Path(root)/REGISTRATION)['stages'][stage]
    expected={name:digest(canonical(value)) for name,value in roles.items()}
    tree_same(claim['role_digests'],expected,'claim/all registered roles')
    require(type(claim['result']) is str and re.fullmatch('[a-p]+',claim['result']) is not None,'claim/AP terminal result')
    terminal=json.loads(bytes.fromhex(claim['result'].translate(HEX)).decode('utf-8'),object_pairs_hook=unique)
    exact_keys(terminal,{'complete','status','identity_sha256_alpha','metrics_sha256_alpha','raw_sha256_alpha'},'claim/terminal fields')
    require(terminal['complete'] is True and terminal['identity_sha256_alpha']==file_digest(Path(directory)/'identity.json')
        and terminal['metrics_sha256_alpha']==file_digest(Path(directory)/'metrics.json')
        and terminal['raw_sha256_alpha']==identity['raw_arrays']['sha256_alpha'],'claim/terminal evidence')
    require(claim['rule']=='exclusive pair-only claim before any stage generator; failure consumes claim','claim/no reuse rule')
    require(terminal['status']==read(Path(directory)/'metrics.json')['verdict'],'claim/terminal verdict')
    if stage=='bench':require(claim['prerequisite_verification_sha256_alpha']==pins['h0']['verification_sha256_alpha'],'claim/bench prerequisite')
    else:
        previous='bench' if stage=='dev' else 'dev';prior=Path(root)/'experiments/h17/run3'/previous/'verification.json'
        gate=read(Path(root)/('config/h17-run3-'+stage+'-opening.json'))
        require(gate['complete'] is True and gate['opened'] is True and gate['stage']==stage
            and gate['source_closure_sha256_alpha']==pins['source_closure_sha256_alpha']
            and gate['prior_verification_sha256_alpha']==file_digest(prior)
            and type(gate['owner_instruction']) is str and bool(gate['owner_instruction'])
            and type(gate['decision']) is str and bool(gate['decision']),'stage/separate owner gate')
        require(claim['prerequisite_verification_sha256_alpha']==file_digest(prior),'claim/prior verification')
        receipt=read(prior);require(receipt['complete'] is True and receipt['passed'] is True,'stage/prior validity')
        if stage=='dev':require(receipt['verdict']=='PASS','DEV/bench all clauses PASS')


def observed_rows(sample,construction,marker):
    result=observation(sample['W_delivered'],sample['AT2'],sample['H_post'],sample['NAV'],marker)
    for source in (0,1):
        for span,start in (('full',0),('last200',400)):
            result['dwell_'+span+'_source'+str(source)]=sample['AT2'][start:,:,source].sum(0,dtype=np.int64)
    result['lost_last200']=~sample['W_delivered'][400:600].any((0,2))
    return result


def never_engaged_states(reference,candidate,rows,label):
    require(set(candidate.fields)-{'q'}==set(reference.fields),label+'/complete original fields')
    require(len(candidate.timeline)==len(reference.timeline),label+'/all original phases')
    for index in range(len(reference.timeline)):
        for field in reference.fields:
            a=reference.get(index,field);b=candidate.get(index,field)
            if isinstance(a,np.ndarray) and a.ndim and a.shape[0]==len(rows):
                same(b[rows],a[rows],label+'/original row-state/'+field)
            else:value_same(b,a,label+'/original global-state/'+field)


def reference_never_engaged(arrays,condition,engaged,schema,records,table):
    rows=~engaged.any(0);left=prefix_of(condition,'Fly');right=prefix_of(condition,'GS250')
    # Compare byte-per-row on EVERY recorded numerical field, respecting native row axes.
    for groupname in ('sample','output'):
        fields=group(arrays,left+'/'+groupname+'/')
        for name,a in fields.items():
            b=arrays[right+'/'+groupname+'/'+name];shape=schema['arrays'][left+'/'+groupname+'/'+name]['shape']
            if 'R' in shape:
                axis=shape.index('R');ix=[slice(None)]*a.ndim;ix[axis]=rows
                same(b[tuple(ix)],a[tuple(ix)],right+'/never-engaged '+groupname+'/'+name)
    never_engaged_states(snapshots(arrays,records['Fly'],left,table),
        snapshots(arrays,records['GS250'],right,table),rows,right+'/never-engaged')


def blob_closure(records,inference,arrays,table):
    """Only the transitive references of declared evidence may own blob members."""
    visited=set()
    def walk(value):
        if isinstance(value,(str,bytes,np.bytes_)):
            key=value if isinstance(value,str) else bytes(value).decode('ascii')
            if key in table.descriptors and key not in visited:
                visited.add(key);walk(table.get(key))
        elif isinstance(value,np.ndarray):
            if value.dtype==np.dtype('S64'):
                for item in value.flat:walk(item)
        elif isinstance(value,GeneratorState):walk(value.state)
        elif isinstance(value,dict):
            for item in value.values():walk(item)
        elif isinstance(value,(list,tuple,set)):
            for item in value:walk(item)
    walk(records);walk(inference)
    for key in arrays:
        if not key.startswith('blob/') and not key.endswith('/attribute_hashes'):
            a=arrays[key]
            if a.dtype==np.dtype('S64'):walk(a)
    # get() also traverses native array_ref tags inside typed dictionaries.
    require(table.used==set(table.descriptors),'blob/exact declared reference closure')


def verify(directory,root=ROOT,smoke=False,stage='bench'):
    directory=Path(directory).resolve();root=Path(root).resolve()
    pins,config,schema,pin_hash=preflight(root,smoke,stage);stage='H0' if smoke else stage
    identity_hash=file_digest(directory/'identity.json');metrics_hash=file_digest(directory/'metrics.json')
    identity=read(directory/'identity.json');metric=read(directory/'metrics.json')
    exact_keys(identity,schema['metadata_keysets']['identity_success'],'identity')
    exact_keys(metric,schema['metadata_keysets']['metrics_success'],'metrics')
    prov=expected_provenance(root,pins,pin_hash)
    for obj,kind in ((identity,'identity'),(metric,'metrics')):
        require(obj['format']=='h17-run3-'+kind+'-v3' and obj['stage']==stage
            and obj['date']=='2026-10-10' and obj['smoke'] is smoke and obj['complete'] is True
            and obj['rows']==(40 if smoke else 400) and obj['steps']==600 and obj['first_failure'] is None,
            kind+'/complete fixed sample')
        tree_same(obj['conditions'],list(CONDITIONS),kind+'/conditions')
        exact_keys(obj['provenance'],schema['metadata_keysets']['provenance'],kind+'/provenance')
        tree_same(obj['provenance'],prov,kind+'/immutable provenance')
    require(identity['passed'] is True,'identity/all gates passed')
    claim_check(identity,directory,root,pins,config,schema,stage,smoke)
    exact_keys(identity['records'],CONDITIONS,'records');exact_keys(metric['readings'],CONDITIONS,'readings')
    prefixes={prefix_of(c,a) for c in CONDITIONS for a in ARMS}
    exact_keys(identity['gates'],prefixes,'saved gates')
    descriptor=identity['raw_arrays'];exact_keys(descriptor,{'path','encoding','sha256_alpha','keys','arrays','blobs'},'raw manifest')
    rawkeys=set(descriptor['arrays']);nonblob={key for key in rawkeys if not key.startswith('blob/')}
    expected=set(schema['arrays'])-({key for key in schema['arrays'] if key.startswith('inference/')} if smoke else set())
    require(nonblob==expected,'raw/exact mode keyset')
    rawschema={key:source_schema(schema,key,value,smoke) for key,value in descriptor['arrays'].items()}
    arrays=load_arrays(directory,descriptor,rawschema);endpoint_map={};gates={};c=source_constants(root)
    original_pair=(5,6) if smoke else tuple(config[stage]);records=identity['records']
    lineage_names=read(root/'experiments/module/identity.json')['A1']['L2']['names']
    try:
        table=BlobTable(arrays,descriptor['blobs'])
        # Every validity check below finishes before any aggregate or inference statistic.
        for condition in CONDITIONS:
            exact_keys(records[condition],ARMS,'record arms/'+condition)
            exact_keys(metric['readings'][condition],ARMS,'reading arms/'+condition)
            for arm,record in records[condition].items():
                label=prefix_of(condition,arm)
                exact_keys(record,schema['metadata_keysets']['record'],label+'/record')
                tree_same(record['state_fields'],schema['fieldsets'][arm],label+'/fieldset')
                tree_same(record['world_fields'],schema['world_fieldsets'][condition],label+'/world fields')
                event_contract(record,600,label)
            disabled_coupling(arrays,records,condition,schema);endpoint_map[condition]={}
            for arm in ARMS:
                label=prefix_of(condition,arm);record=records[condition][arm]
                gate=identity['gates'][label]
                exact_keys(gate,{'complete','passed','rows','steps','identity'},label+'/saved gate fields')
                require(gate['complete'] is True and gate['passed'] is True and gate['rows']==(40 if smoke else 400)
                    and gate['steps']==600,label+'/saved completed gate')
                expected_gate=dict(passed=True,same_class=True,lineage=True,creation=True,generator_phases=True,
                    inputs_and_returns=True,full_original_outputs=True,sample=True,L1=list(L1),L2_names=lineage_names,
                    L3=True,GSOff=True,candidate_creation=True,candidate_draw_budget=True,candidate_same_state=True,never_engaged=True)
                tree_same(gate['identity'],expected_gate,label+'/complete identity clauses')
                sample=group(arrays,label+'/sample/');construction=group(arrays,label+'/construction/')
                output=group(arrays,label+'/output/');gs=group(arrays,label+'/gs/')
                native_header(record['output_metadata'],condition,arm,label)
                exact_keys(sample,SAMPLE_FIELDS,label+'/sample')
                require(all(np.isfinite(a).all() for a in sample.values() if a.dtype.kind=='f'),label+'/finite sample')
                exact_keys(record['construction_refs'],construction,label+'/construction references')
                for key,ref in record['construction_refs'].items():same(table.get(ref),construction[key],label+'/construction reference/'+key)
                require(record['observation_calls']=={'base':600,'circuit':600},label+'/exactly one original base/circuit')
                streams={'C0':7,'W1':8,'T1':6,'T3':6}[condition]
                require(record['independent_streams']==streams,label+'/created stream count')
                logged=arm in ('Passive','GS250')
                require(record['literal_generators'] is (not logged) and record['generator_handles']==streams*(2 if logged else 1),
                    label+'/literal and logger handles')
                require(all(x['handle_type']==('GeneratorTap' if logged else 'Generator') for x in record['generator_instances']),
                    label+'/native handle types')
                require(record['gs_mode']==('enabled' if arm=='GS250' else 'disabled' if arm=='GSOff' else 'reference')
                    and record['entry_semantics']==('actual' if arm in ('GS250','GSOff') else 'observational_shadow'),label+'/mode and entry semantics')
                effective=dict(record)
                if arm in ('GS250','Passive'):
                    require(record['draw_log_reference'] is None,label+'/own transcript required')
                    require(len(record['draw_log'])>0,label+'/direct transcript complete')
                else:
                    require(record['draw_log']==[] and record['draw_log_reference']==prefix_of(condition,'Passive'),label+'/disabled log proof reference')
                    effective['draw_log']=records[condition]['Passive']['draw_log']
                expected_log_proof=dict(source_arm='Passive',basis=['original shared BitGenerator direct primitive returns'],passed=True) if arm=='Passive' else dict(source_arm='GS250',basis=['own original shared BitGenerator primitive returns'],passed=True) if arm=='GS250' else dict(source_arm='Passive',basis=['complete disabled identity'],passed=True)
                tree_same(record['primitive_log_proof'],expected_log_proof,label+'/primitive transcript proof basis')
                transcript_order(effective,condition,len(construction['good']),600,label,schema)
                native_start=construction_draw_check(effective,table,construction,condition,original_pair,c,label)
                generator_checkpoints(arrays,effective,label,table,condition,600)
                normals=independent_draws(effective,table,sample,condition,label)
                timeline=snapshots(arrays,record,label,table)
                if arm in ('GS250','GSOff'):gs_check(gs,sample,arm,label)
                else:require(not gs,label+'/no GS instance diagnostics')
                base=sample.copy()
                if arm in ('GS250','GSOff'):base.update(TGT=gs['BASE_TGT'],TURN=gs['BASE_TURN'])
                masks=base_recurrence_check(base,construction,c,label)
                rings=snapshot_sample_check(timeline,sample,construction,gs,arm,arrays,label,c)
                base=dict(base,RING_post=rings)
                circuit_ring_check(base,construction,c,normals,label)
                world_arithmetic_check(sample,construction,c,label)
                world_snapshot_check(arrays,record,label,table,sample,construction,condition,label,native_start)
                construction_check(condition,construction,sample,c,len(construction['good']),label)
                input_return_check(arrays,record,label,table,sample,gs,arm)
                if condition=='W1':twin_check(arrays,record,label,table,sample)
                own_state_proof(record['base_act_proof'],effective,timeline,arrays,label,table,gs,sample,arm,schema)
                plain_logger_proof(record['base_act_proof'],arrays,record,label,table,smoke,schema)
                scores=original_output_check(output,sample,construction,label)
                expected_l3=dict(dwell=scores['dwell'],first=scores['first'],contacts=scores['contacts'],cls3=scores['choice'])
                if condition=='W1':expected_l3['w1sum']=w1_scores(output,construction['good'],c)
                stored_scores(arrays,record['L3'],expected_l3,label+'/L3')
                marker=gs['entry'] if arm in ('GS250','GSOff') else None
                obs=observed_rows(sample,construction,marker)
                storedobs=group(arrays,label+'/reading/');storedmasks=group(arrays,label+'/mask/')
                exact_keys(storedobs,obs,label+'/observations');exact_keys(storedmasks,masks,label+'/N2 masks')
                for key,a in obs.items():same(storedobs[key],a,label+'/observed '+key)
                for key,a in masks.items():same(storedmasks[key],a,label+'/N2 '+key)
                anchor_check(group(arrays,label+'/anchor/'),sample,obs,gs,arm,label)
                engaged=gs['engaged'] if arm in ('GS250','GSOff') else np.zeros(sample['H_post'].shape,bool)
                shadow=(obs['q_obs']>=250)&(sample['H_post']==-1)
                shadow_entry=shadow&~np.concatenate([np.zeros((1,shadow.shape[1]),bool),shadow[:-1]])
                end=endpoints(sample,construction,engaged,shadow_entry if arm not in ('GS250','GSOff') else None)
                storedend=group(arrays,label+'/endpoint/');exact_keys(storedend,end,label+'/endpoints')
                for key,a in end.items():same(storedend[key],a,label+'/endpoint '+key)
                if arm in ('Fly','GS250'):endpoint_map[condition][arm]=end
                if arm=='GS250':reference_never_engaged(arrays,condition,engaged,schema,records[condition],table)
                gates[label]=dict(complete=True,passed=True,rows=len(construction['good']),steps=600,
                    original_state_events=3001,generator_checkpoints=4801,streams=streams,primitive_calls=len(effective['draw_log']))
                del sample,construction,output,gs,base,rings,normals,timeline,obs,storedobs,storedmasks,storedend,masks
                table.clear();arrays.clear()
        # Check the inference primitive before invoking any statistical reduction.
        if smoke:
            require(identity['inference'] is None,'H0/no inference metadata');indices=None
        else:indices=inference_check(arrays,identity['inference'],table,config['inference'][stage],schema)
        blob_closure(records,identity['inference'],arrays,table)
        # Independent descriptive readings are now safe to compute.
        for condition in CONDITIONS:
            for arm in ARMS:
                label=prefix_of(condition,arm);sample=group(arrays,label+'/sample/');construction=group(arrays,label+'/construction/')
                masks=n2(sample,construction['known']);marker=arrays[label+'/gs/entry'] if arm in ('GS250','GSOff') else None
                _,reading=metric_reading(condition,sample,construction,masks,marker)
                tree_same(metric['readings'][condition][arm],reading,label+'/independent descriptive reading')
                table.clear();arrays.clear()
        if smoke:
            clauses={};verdict='VALIDITY_ONLY'
        else:
            differences,statistics,clauses,verdict=all_clauses(endpoint_map,indices)
            for key,delta in differences.items():
                same(arrays['inference/'+key+'/difference'],delta,'statistics/saved differences '+key)
                for name,a in statistics[key].items():same(arrays['inference/'+key+'/'+name],a,'statistics/'+key+'/'+name)
        tree_same(metric['clauses'],clauses,'metrics/nine independently recomputed clauses')
        require(metric['verdict']==verdict,'metrics/joint frozen verdict')
        _,_,_,posthash=preflight(root,smoke,stage if not smoke else 'bench')
        require(posthash==pin_hash,'post audit/immutable closure')
        require(file_digest(directory/'raw.npz.ap')==descriptor['sha256_alpha'],'post audit/raw bytes')
        require(file_digest(directory/'identity.json')==identity_hash and file_digest(directory/'metrics.json')==metrics_hash,
            'post audit/immutable JSON evidence')
        return dict(format='h17-run3-verification-v3',date='2026-10-10',stage=stage,complete=True,passed=True,
            smoke=smoke,provenance=prov,raw_sha256_alpha=descriptor['sha256_alpha'],checked_arrays=len(arrays),
            gates=gates,clauses=clauses,verdict=verdict,first_failure=None)
    except VerificationError as exc:
        if 'condition' in locals():exc.first_failure['condition']=condition
        if 'arm' in locals():exc.first_failure['arm']=arm
        raise
    finally:arrays.close()


def write_receipt(target,receipt,root=ROOT):
    payload=canonical(receipt)+b'\n'
    try:no_protected_tokens(payload,root)
    except VerificationError as exc:
        receipt=dict(receipt,complete=False,passed=False,verdict='INVALID',clauses={},
            first_failure=exc.first_failure,gates={'diagnostic_alpha':payload.hex().translate(AP)})
        payload=canonical(receipt)+b'\n';no_protected_tokens(payload,root)
    target=Path(target);temporary=target.with_suffix(target.suffix+'.tmp')
    with temporary.open('wb') as f:f.write(payload);f.flush();os.fsync(f.fileno())
    temporary.replace(target)
    return receipt


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path);parser.add_argument('--smoke',action='store_true')
    parser.add_argument('--stage',choices=('bench','dev','eval'),default='bench');parser.add_argument('--root',type=Path,default=ROOT)
    parser.add_argument('--receipt',type=Path)
    args=parser.parse_args(argv);directory=args.output.resolve();target=(args.receipt or directory/'verification.json').resolve()
    require(target.parent==directory and target.name.endswith('.json') and target.name not in ('identity.json','metrics.json'),
        'verification/receipt output restriction')
    stage='H0' if args.smoke else args.stage
    try:receipt=verify(directory,args.root,args.smoke,args.stage)
    except BaseException as exc:
        failure=exc.first_failure if isinstance(exc,VerificationError) else dict(field='verification '+type(exc).__name__,
            index=None,phase=None,condition=None,arm=None)
        receipt=dict(format='h17-run3-verification-v3',date='2026-10-10',stage=stage,complete=False,passed=False,
            smoke=args.smoke,provenance=None,raw_sha256_alpha=None,checked_arrays=0,gates={},clauses={},
            verdict='INVALID',first_failure=failure)
    receipt=write_receipt(target,receipt,args.root)
    print('GS250 independent saved-evidence '+('PASS' if receipt['passed'] else 'INVALID'),flush=True)
    return 0 if receipt['passed'] else 1


if __name__=='__main__':raise SystemExit(main())
