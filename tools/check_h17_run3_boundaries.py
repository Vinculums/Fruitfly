"""VALIDITY_ONLY native one-act fixtures, using immutable spent primitive returns.

No controller/world constructor, BitGenerator, random call or trajectory occurs.
Root executes this before freezing the Run3 base implementation closure.
"""
import os
for _key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[_key]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import argparse
from collections import OrderedDict
import copy
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
sys.path[:0]=[str(Path(__file__).resolve().parent),str(Path(__file__).resolve().parents[1]/'src')]
import numpy as np
import fly
import verify_h17_r0 as V
import h17_run3_recording as H
import measure_h17_run3 as M
from h17_run3_arm import GS250,GSOff

ROOT=Path(__file__).resolve().parents[1]
SPENT='experiments/h17/r0_smoke'
OUTPUT='experiments/h17/h17_run3_native_boundary_checks.json'


class SpentBlobs(V.BlobTable):
    """Same strict data-only grammar, checking each consumed blob lazily."""
    def __init__(self,arrays,descriptors):
        self.arrays=arrays;self.descriptors=descriptors;self.cache=OrderedDict();self.visiting=set();self.cache_bytes=0;self.cache_limit=32<<20;self.checked=set()

    def get(self,key):
        key=bytes(key).decode('ascii') if isinstance(key,(bytes,np.bytes_)) else str(key)
        if key not in self.checked:
            H.require(key in self.descriptors,'native fixture/unknown blob')
            a=self.arrays['blob/'+key];d=self.descriptors[key]
            H.require(not a.dtype.hasobject,'native fixture/object blob')
            H.require(H.digest(H.canonical(d)+a.tobytes())==key,'native fixture/blob content')
            if d['kind']=='ndarray':H.require(a.dtype.str==d['dtype'] and list(a.shape)==d['shape'],'native fixture/blob schema')
            else:H.require(d=={'kind':'typed_json'} and a.dtype==np.uint8 and a.ndim==1,'native fixture/typed schema')
            self.checked.add(key)
        return super().get(key)


def detached(values,cls,calls,q):
    a=object.__new__(cls);components={name:object.__new__(kind) for name,kind in (
        ('up',fly.Upstream),('sel',fly.Circuit),('ring',fly.Ring),('mb',fly.MB))}
    a.__dict__.update(components);replay=None
    for field,value in values.items():
        if isinstance(value,V.GeneratorState):
            if replay is None:replay=H.ReplayGenerator(value.state);replay.calls=copy.deepcopy(calls)
            else:H.equal(replay.bit_generator.state,value.state,'native fixture/shared generator aliases')
            copied=replay
        else:copied=copy.deepcopy(value)
        if '.' in field:
            component,name=field.split('.',1);setattr(components[component],name,copied)
        else:setattr(a,field,copied)
    if cls is not fly.Fly:a.q=np.full(a.R,q,np.int64)
    return a


def encoded_state(a):
    state={}
    for field,value in H.walk(a).items():
        if isinstance(value,H.ReplayGenerator):
            value=dict(recorded_generator_state=value.bit_generator.state,consumed=value.at)
        if isinstance(value,np.ndarray):value=dict(dtype=value.dtype.str,shape=list(value.shape),bytes_alpha=value.tobytes().hex().translate(H.AP))
        elif isinstance(value,np.generic):value=dict(dtype=value.dtype.str,bytes_alpha=value.tobytes().hex().translate(H.AP))
        state[field]=value
    return state


def full_same(a,b,label,exclude=()):
    aa,bb=H.walk(a),H.walk(b);H.require(set(aa)-set(exclude)==set(bb)-set(exclude),label+'/fieldsets')
    for field in set(aa)-set(exclude):
        left,right=aa[field],bb[field]
        if isinstance(left,H.ReplayGenerator):H.equal(left.bit_generator.state,right.bit_generator.state,label+'/'+field)
        else:H.equal(left,right,label+'/'+field)


def run_case(name,values,calls,world,q,held_mode='zero',whiff_mode='none',bumped=False):
    mutated=copy.deepcopy(values);r=mutated['R'];mutated['sel.s']=np.zeros((r,2));mutated['sel.S']=np.zeros((r,1));mutated['silence']=np.zeros(r);mutated['since']=np.zeros(r)
    if held_mode=='unique':mutated['sel.s'][:,0]=100.
    if held_mode=='multiple':mutated['sel.s'][:]=100.
    whiffs=np.zeros((r,2),bool)
    if whiff_mode=='negative_NAVfalse':mutated['known']=np.tile([1.,-1.],(r,1));whiffs[:,1]=True
    raw=np.ones_like(whiffs) if whiff_mode=='masked_raw' else whiffs.copy()
    wind=np.ones(r,bool)
    original=detached(mutated,fly.Fly,calls,q);candidate=detached(mutated,GS250,calls,q);off=detached(mutated,GSOff,calls,q)
    before=encoded_state(candidate);native=fly.Fly.act;capture={};count=0
    def observed(instance,*args,**kwargs):
        nonlocal count
        result=native(instance,*args,**kwargs)
        if instance is candidate:
            count+=1;capture['return']=tuple(x.copy() for x in result);capture['state']=copy.deepcopy(instance)
        return result
    fly.Fly.act=observed
    try:expected=original.act(world,whiffs,wind);actual=candidate.act(world,whiffs,wind);off_return=off.act(world,whiffs,wind)
    finally:fly.Fly.act=native
    H.require(count==1 and all(a.rng.at==4 for a in (original,candidate,off)),'native fixture/one act/four consumed')
    full_same(original,capture['state'],name+'/base',exclude=('q',));H.equal(capture['return'][0],expected[0],name+'/base return');H.equal(capture['return'][1],expected[1],name+'/base held')
    full_same(original,off,name+'/GSOff',exclude=('q',));H.equal(off_return[0],expected[0],name+'/GSOff return')
    h=actual[1];units=(candidate.sel.s>1.).sum(1)
    expected_units={'zero':0,'unique':1,'multiple':2}[held_mode]
    H.require((units==expected_units).all(),name+'/actual hold boundary')
    if whiff_mode=='negative_NAVfalse':H.require(not candidate.nav_hit.any() and whiffs.any(),name+'/delivered NAVfalse')
    if whiff_mode=='masked_raw':H.require(raw.any() and not whiffs.any(),name+'/raw masked delivered')
    from h17_run3_arm import schedule
    gs=schedule(np.full(r,q,np.int64),whiffs,h,candidate.cast_sign,capture['state'].tgt,candidate.est,expected[0])
    H.equal(candidate.q,gs['q_post'],name+'/q');H.equal(actual[0],gs['SEARCH_TURN'],name+'/turn');H.equal(candidate.tgt,gs['SEARCH_TGT'],name+'/target')
    full_same(original,candidate,name+'/wrapper field whitelist',exclude=('q','tgt','last_turn'))
    # Inherited body response is separately tested on an explicit synthetic mask.
    mask=np.full(r,bumped,bool);original.bump(mask);candidate.bump(mask);off.bump(mask)
    full_same(original,candidate,name+'/native bump',exclude=('q','tgt','last_turn'));full_same(original,off,name+'/GSOff native bump',exclude=('q',))
    H.require(all(a.rng.at==4 for a in (original,candidate,off)),name+'/bump zero primitives')
    proof=dict(before=before,base=encoded_state(capture['state']),original_after_bump=encoded_state(original),candidate_after_bump=encoded_state(candidate),off_after_bump=encoded_state(off),
        base_return=[dict(dtype=x.dtype.str,shape=list(x.shape),bytes_alpha=x.tobytes().hex().translate(H.AP)) for x in expected],
        actual_return=[dict(dtype=x.dtype.str,shape=list(x.shape),bytes_alpha=x.tobytes().hex().translate(H.AP)) for x in actual])
    return dict(name=name,passed=True,q_pre=q,q_post=int(candidate.q[0]),held_units=expected_units,engaged=bool(gs['engaged'][0]),u=int(gs['u'][0]),leg=int(gs['leg'][0]),remaining=int(gs['remaining'][0]),alpha=int(gs['alpha'][0]),
        original_calls=1,primitive_consumption=4,new_generators=0,new_random_draws=0,bump_mask=bumped,full_state_evidence_alpha=H.canonical(proof).hex().translate(H.AP))


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=ROOT/OUTPUT);args=parser.parse_args(argv)
    identity=M.read(ROOT/SPENT/'identity.json');H.require(identity['complete'] is True and identity['passed'] is True and identity['smoke'] is True,'native fixture/spent verified scope')
    raw=ROOT/SPENT/'raw.npz.ap';H.require(M.file_digest(raw)==identity['raw_arrays']['sha256_alpha'],'native fixture/spent raw hash')
    temporary=tempfile.TemporaryFile('w+b');hexmap=str.maketrans('abcdefghijklmnop','0123456789abcdef')
    with raw.open('rb') as source:
        while chunk:=source.read(1<<18):temporary.write(bytes.fromhex(chunk.decode('ascii').translate(hexmap)))
    temporary.seek(0);arrays=V.LazyArrays(temporary,identity['raw_arrays']['keys']);table=SpentBlobs(arrays,identity['raw_arrays']['blobs'])
    record=identity['records']['C0']['Passive'];timeline=V.SnapshotTimeline(arrays,record,'C0/Passive',table);values=timeline.row(1)
    logs=[x for x in record['draw_log'] if x['generator']==2 and x['step']==0 and x['phase']=='act'];H.require(len(logs)==4,'native fixture/spent four primitives')
    calls=[(log['method'],*V.draw_values(log,table)) for log in logs]
    world=SimpleNamespace(head=arrays['C0/Passive/sample/PRE_HEAD'][0].copy(),rot=arrays['C0/Passive/sample/PRE_ROT'][0].copy())
    cases=[]
    try:
        for name,q,held,whiff,bump in (
            ('q249_zero',248,'zero','none',False),('q250_zero',249,'zero','none',False),
            ('q250_unique',249,'unique','none',False),('q250_multiple',249,'multiple','none',False),
            ('any_delivered_NAVfalse',400,'unique','negative_NAVfalse',False),('W1_masked_RAW',249,'zero','masked_raw',False),
            ('delayed_q300_u50',299,'zero','none',False),('interruption_q300_held',299,'unique','none',False),
            ('resumption_q301_no_restart',300,'zero','none',False),('leg_end30',278,'zero','none',False),('leg_start30',279,'zero','none',False),
            ('leg_end90',338,'zero','none',False),('leg_start90',339,'zero','none',False),('leg_start180',429,'zero','none',False),('leg_start300',549,'zero','none',False),
            ('slant_before150',398,'zero','none',False),('slant_start150',399,'zero','none',False),('slant_before300',548,'zero','none',False),
            ('inherited_bump',249,'zero','none',True)):
            cases.append(run_case(name,values,calls,world,q,held,whiff,bump))
        result=dict(format='h17-run3-native-boundaries-v3',date=M.DATE,complete=True,passed=True,scope='SYNTHETIC VALIDITY_ONLY; no trajectory or efficacy rows',
            spent_pair_alias='h29/smoke',source_closure_sha256_alpha=identity['provenance']['source_closure_sha256_alpha'],
            spent_identity_sha256_alpha=M.file_digest(ROOT/SPENT/'identity.json'),spent_raw_sha256_alpha=M.file_digest(raw),
            native_source_sha256_alpha=M.file_digest(ROOT/'src/fly.py'),program_sha256_alpha=M.file_digest(Path(__file__)),original_fields=record['state_fields'],
            coverage=[x['name'] for x in cases],cases=cases,fresh_generators_created=0,fresh_random_draws=0,simulation_performed=False,first_failure=None)
        M.write_json(args.output,result);print('Native boundary validity PASS: '+str(len(cases))+' detached cases');return 0
    finally:arrays.close()


if __name__=='__main__':raise SystemExit(main())
