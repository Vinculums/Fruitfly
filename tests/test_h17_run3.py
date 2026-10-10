"""Pure synthetic contract fixtures: no world, trajectory, or RNG creation."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
import json
import copy
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'tools')]
from h17_run3_arm import GS250,GSOff,schedule
from fly import Fly,angdiff
import h17_run3_recording as H
import measure_h17_run3 as M


def scheduled(q,h=None,whiff=None,enabled=True):
    q=np.asarray(q,np.int64);r=len(q)
    return schedule(q,np.zeros((r,2),bool) if whiff is None else whiff,
        np.full(r,-1,np.int64) if h is None else np.asarray(h,np.int64),
        np.ones(r),np.zeros(r),np.zeros(r),np.zeros(r),enabled)


def synthetic_sample(steps=600,rows=4):
    sample={}
    schema=M.read(ROOT/'experiments/h17/h17_run3_array_keysets.json')
    prefix='efficacy/C0/Fly/sample/'
    for name in H.SAMPLE_FIELDS:
        d=schema[prefix+name];shape=[steps if x=='T' else rows if x=='R' else x for x in d['shape']]
        sample[name]=np.zeros(shape,dtype=d['dtype'])
    sample['H_pre'].fill(-1);sample['H_post'].fill(-1)
    return sample


class ScheduleContract(unittest.TestCase):
    def test_first_boundary(self):
        d=scheduled([248,249]);np.testing.assert_array_equal(d['engaged'],[False,True]);np.testing.assert_array_equal(d['u'],[-1,0])
        np.testing.assert_array_equal(d['leg'],[0,1]);np.testing.assert_array_equal(d['remaining'],[0,30])

    def test_leg_boundaries(self):
        d=scheduled([278,279,338,339]);np.testing.assert_array_equal(d['leg'],[1,2,2,3])
        np.testing.assert_array_equal(d['remaining'],[1,60,1,90])

    def test_phase_ages_through_hold(self):
        d=scheduled([299],[0]);self.assertFalse(d['engaged'][0]);self.assertEqual(d['q_post'][0],300)
        d=scheduled([299]);self.assertEqual(d['leg'][0],2);self.assertEqual(d['remaining'][0],40)

    def test_any_delivered_resets(self):
        d=scheduled([400,400],whiff=np.array([[False,True],[False,False]]));np.testing.assert_array_equal(d['q_post'],[0,401])

    def test_alpha_half_period(self):
        d=scheduled([398,399,548,549]);np.testing.assert_array_equal(d['alpha'],[1,-1,-1,1])

    def test_disabled_still_updates_q(self):
        d=scheduled([500],enabled=False);self.assertEqual(d['q_post'][0],501);self.assertTrue(d['eligible'][0]);self.assertFalse(d['engaged'][0]);self.assertEqual(d['u'][0],-1)

    def test_noise_residual_not_clipped(self):
        q=np.array([249],np.int64);base=np.array([45.]);turn=np.array([171.])
        d=schedule(q,np.zeros((1,2),bool),np.array([-1]),np.ones(1),base,np.zeros(1),turn)
        expected=turn-np.clip(.6*angdiff(base,np.zeros(1)),-40.,40.)
        H.equal(d['RESIDUAL'],expected,'residual');H.equal(d['SEARCH_TURN'],d['SEARCH_CLIP']+expected,'turn')
        self.assertGreater(d['SEARCH_TURN'][0],40.)

    def test_inactive_signed_zero_bytes(self):
        turn=np.array([-0.]);target=np.array([-0.])
        d=schedule(np.array([0]),np.zeros((1,2),bool),np.array([-1]),np.ones(1),target,np.zeros(1),turn)
        self.assertEqual(d['SEARCH_TURN'].tobytes(),turn.tobytes());self.assertEqual(d['SEARCH_TGT'].tobytes(),target.tobytes())

    def test_wrapper_calls_original_once_and_only_adds_q(self):
        a=object.__new__(GS250);a.q=np.array([249,0],np.int64);a.cast_sign=np.ones(2);a.tgt=np.zeros(2);a.est=np.zeros(2);a.last_turn=np.zeros(2)
        fields=set(vars(a));whiffs=np.zeros((2,2),bool)
        with patch.object(Fly,'act',return_value=(np.array([.3,-0.]),np.array([-1,-1]))) as native:
            turn,h=a.act(None,whiffs,np.zeros(2,bool))
        self.assertEqual(native.call_count,1);self.assertEqual(set(vars(a)),fields);self.assertEqual(turn[1].tobytes(),np.float64(-0.).tobytes())
        self.assertEqual(a.q.tolist(),[250,1])

    def test_off_returns_original_array_object(self):
        a=object.__new__(GSOff);a.q=np.array([600],np.int64);a.cast_sign=np.ones(1);a.tgt=np.zeros(1);a.est=np.zeros(1);a.last_turn=np.zeros(1)
        original=np.array([-0.])
        with patch.object(Fly,'act',return_value=(original,np.array([-1]))) as native:result=a.act(None,np.zeros((1,2),bool),np.zeros(1,bool))
        self.assertIs(result[0],original);self.assertEqual(native.call_count,1);self.assertEqual(a.q[0],601)


class SavedEvidenceContract(unittest.TestCase):
    def test_actual_registration_mixed_vector_pagination_is_not_literal_scan_incompleteness(self):
        config=M.read(ROOT/M.CONFIG);registered=M.read(ROOT/M.REGISTRATION)
        self.assertEqual(len(registered['graph_scan']['queries']),18)
        self.assertTrue(all(q['has_more'] is True for q in registered['graph_scan']['queries']))
        with patch.object(np.random,'default_rng') as factory,patch.object(np.random,'PCG64') as bitgenerator:
            M.registration_check(ROOT,config)
        factory.assert_not_called();bitgenerator.assert_not_called()

    def test_actual_registration_rejects_incomplete_canonical_scan_or_literal_query_failure(self):
        config=M.read(ROOT/M.CONFIG);registered=M.read(ROOT/M.REGISTRATION)
        mutations=(('graph','all_canonical_read_verified',False),('graph','canonical_documents',257),
            ('graph','literal_hits',[{'synthetic':'hit'}]),('query','executed',False),('query','keyword_rows',1),
            ('query','literal_hit',True),('query','error','synthetic error'),('query','arms','vector'),
            ('query','role_index',1),('fallback','verified',False),('fallback','role_hits',[0]))
        for target,key,value in mutations:
            changed=copy.deepcopy(registered);graph=changed['graph_scan']
            selected=graph if target=='graph' else graph['queries'][0] if target=='query' else graph['read_transport_fallbacks'][0]
            selected[key]=value
            with self.subTest(target=target,key=key),patch.object(M,'read',return_value=changed),patch.object(np.random,'default_rng') as factory:
                with self.assertRaises(H.EvidenceError):M.registration_check(ROOT,config)
            factory.assert_not_called()

    def test_reference_shadow_is_not_intervention(self):
        s=synthetic_sample();ends=H.endpoint(s,{'good':np.array([0,0,1,1])},None,'Fly')
        np.testing.assert_array_equal(ends['ever_engaged'],False);np.testing.assert_array_equal(ends['first_entry_step'],249);np.testing.assert_array_equal(ends['entry_event_count'],1)

    def test_c0_whiff_after_old_horizon_counts(self):
        s=synthetic_sample();s['W_delivered'][400,0,1]=True
        c=dict(known=np.zeros((4,2)),cell=np.arange(4));obs,masks,out=H.readings('C0',s,c)
        self.assertEqual(out['primary']['numerator'],1);self.assertEqual(out['cells']['0']['primary']['numerator'],1)

    def test_window_excludes_marker_includes_last_tick(self):
        w=np.zeros((600,1,2),bool);at=np.zeros_like(w);nav=np.zeros((600,1),bool);h=np.full((600,1),-1,np.int64);marker=np.zeros((600,1),bool);marker[399]=True
        w[399,0]=True;w[599,0]=True;o=H.observations(w,at,h,nav,marker)
        self.assertEqual(o['post_first_whiff'][0],599);self.assertTrue(o['full_200'][0]);self.assertEqual(o['post_whiff_bits'][0],3);self.assertFalse(o['full_300'][0])

    def test_exact_archive_key_dtype_and_shape(self):
        with tempfile.TemporaryDirectory() as directory:
            a=H.Archive(Path(directory)/'raw.npz.ap',{'x':{'dtype':'<i8','shape':[2]}})
            with self.assertRaises(H.EvidenceError):a.array('y',np.zeros(2,np.int64))
            with self.assertRaises(H.EvidenceError):a.array('x',np.zeros(2,np.int32))
            with self.assertRaises(H.EvidenceError):a.array('x',np.zeros(3,np.int64))
            a.array('x',np.zeros(2,np.int64));a.finish()

    def test_blob_closure_keeps_nested_timeline_and_drops_orphan(self):
        with tempfile.TemporaryDirectory() as directory:
            a=H.Archive(Path(directory)/'raw.npz.ap');needed=a.put(np.array([-0.]));orphan=a.put(np.ones(2));timeline=a.put(np.asarray([needed],dtype='S64'));root=a.put(dict(timeline=timeline));manifest=a.seal({'root':root})
            self.assertIn(needed,manifest['blobs']);self.assertNotIn(orphan,manifest['blobs']);self.assertIn(timeline,manifest['blobs'])

    def test_inference_dtype_normalization_is_narrow(self):
        kwargs=dict(size=(5000,400),dtype=np.int64,endpoint=False);result=H.inference_kwargs(kwargs)
        self.assertIs(kwargs['dtype'],np.int64);self.assertEqual(result['dtype'],'<i8')
        for dtype in (int,np.int32,'<i8'):
            with self.assertRaises(H.EvidenceError):H.inference_kwargs(dict(kwargs,dtype=dtype))

    def test_failure_metadata_exact_top_level_keys(self):
        identity,metrics=M.metadata('bench',False,400,{})
        schema=M.schema_contract()
        self.assertEqual(set(identity),set(schema['metadata_keysets']['identity_success']))
        self.assertEqual(set(metrics),set(schema['metadata_keysets']['metrics_success']))

    def test_failed_preflight_cannot_claim_or_create_generator(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);out=root/'experiments/h17/run3/bench'
            with patch.object(M,'ROOT',root),patch.object(M,'preflight',side_effect=H.EvidenceError('fixture/guard')) as guard,patch.object(M,'claim_pair') as claim,patch.object(np.random,'default_rng') as factory:
                with self.assertRaises(H.EvidenceError):M.main(['--stage','bench','--output',str(out)])
            guard.assert_called_once();claim.assert_not_called();factory.assert_not_called();self.assertFalse(out.exists())

    def test_namespace_save_matches_every_frozen_arm_key(self):
        keysets=M.read(ROOT/'experiments/h17/h17_run3_array_keysets.json');dimensions={'T':600,'R':4,'E':3001,'G':4801}
        for condition in H.CONDITIONS:
            for arm in H.ARMS:
                prefix=H.namespace(condition,arm)
                keys={k[len(prefix)+1:]:v for k,v in keysets.items() if k.startswith(prefix+'/')}
                def arrays(group):
                    return {k[len(group)+1:]:np.zeros([dimensions.get(x,x) for x in d['shape']],dtype=d['dtype']) for k,d in keys.items() if k.startswith(group+'/')}
                sample=arrays('sample');sample['H_pre'].fill(-1);sample['H_post'].fill(-1)
                construction=arrays('construction');construction['cell']=np.arange(4,dtype=np.int64)
                gs=arrays('gs') or None
                if gs is not None:gs['u'].fill(-1)
                tables={k:np.zeros([dimensions.get(x,x) for x in d['shape']],dtype=d['dtype']) for k,d in keys.items() if '/' not in k}
                score=arrays('L3');w1={k[6:]:v for k,v in score.items() if k.startswith('w1sum/')}
                score={k:v for k,v in score.items() if '/' not in k}
                if w1:
                    cum={k[4:]:v for k,v in w1.items() if k.startswith('cum/')};score['w1sum']={k:v for k,v in w1.items() if '/' not in k};score['w1sum']['cum']=cum
                run=dict(output=arrays('output'),sample=sample,construction=construction,twin=arrays('twin'),gs=gs,tables=tables,record={})
                with tempfile.TemporaryDirectory() as directory:
                    store=H.Archive(Path(directory)/'raw.npz.ap',keysets,rows=4,smoke=True)
                    H.save_run(store,condition,arm,run,score)
                    self.assertEqual(set(store.arrays),{prefix+'/'+k for k in keys},prefix);store.finish()

    def test_claim_path_independent_and_no_generator(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);pins={'h0':{'verification_sha256_alpha':'a'*64}}
            prov={k:'b'*64 for k in ('design_sha256_alpha','seed_config_sha256_alpha','seed_registration_sha256_alpha','runtime_sha256_alpha','schema_sha256_alpha','keysets_sha256_alpha','specification_pins_sha256_alpha','execution_pins_sha256_alpha','source_closure_sha256_alpha','opening_sha256_alpha')}
            # Synthetic aliases only; no generator is constructed.
            with patch.object(M.R,'p5',return_value=None):
                path,record=M.claim_pair([101,102],'bench',{'inference':{'bench':103}},prov,root/'one',pins,root)
                with self.assertRaises(H.EvidenceError):M.claim_pair([101,102],'bench',{'inference':{'bench':103}},prov,root/'two',pins,root)
            self.assertEqual(path.parent,root/M.REGISTRY);self.assertIsNone(record['result']);self.assertFalse(record['complete'])

    def test_claim_durability_fault_keeps_first_failure_sidecar(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);pins={'h0':{'verification_sha256_alpha':'a'*64}}
            prov={k:'b'*64 for k in ('design_sha256_alpha','seed_config_sha256_alpha','seed_registration_sha256_alpha','runtime_sha256_alpha','schema_sha256_alpha','keysets_sha256_alpha','specification_pins_sha256_alpha','execution_pins_sha256_alpha','source_closure_sha256_alpha','opening_sha256_alpha')}
            native=M.write_json
            def fault(path,value,root=M.ROOT,exclusive=False):
                answer=native(path,value,root,exclusive)
                if exclusive:raise OSError('synthetic durability fault')
                return answer
            with patch.object(M.R,'p5',return_value=None),patch.object(M,'write_json',side_effect=fault):
                with self.assertRaises(H.EvidenceError):M.claim_pair([201,202],'bench',{'inference':{'bench':203}},prov,root/'one',pins,root)
            records=list((root/M.REGISTRY).glob('*.failure.json'));self.assertEqual(len(records),1)
            receipt=M.read(records[0]);self.assertFalse(receipt['complete']);self.assertEqual(receipt['first_failure']['phase'],'claim')
            self.assertTrue(records[0].with_name(records[0].name.replace('.failure.json','.json')).is_file())

    def test_postclaim_output_fault_preserves_registry_receipt_before_rng(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);out=root/'experiments/h17/run3/bench';pins={'h0':{'verification_sha256_alpha':'a'*64}}
            config={'bench':[301,302],'inference':{'bench':303}}
            prov={k:'b'*64 for k in ('design_sha256_alpha','seed_config_sha256_alpha','seed_registration_sha256_alpha','runtime_sha256_alpha','schema_sha256_alpha','keysets_sha256_alpha','specification_pins_sha256_alpha','execution_pins_sha256_alpha','source_closure_sha256_alpha','opening_sha256_alpha')}
            nativewrite=M.write_json;nativeclaim=M.claim_pair
            def fault(path,value,root=M.ROOT,exclusive=False):
                if Path(path).parent==out:raise OSError('synthetic output fault')
                return nativewrite(path,value,root,exclusive)
            with patch.object(M,'ROOT',root),patch.object(M,'preflight',return_value=(pins,config,prov)),patch.object(M,'claim_pair',side_effect=lambda *args:nativeclaim(*args,root=root)),patch.object(M.R,'p5',return_value=None),patch.object(M,'write_json',side_effect=fault),patch.object(np.random,'default_rng') as factory:
                self.assertEqual(M.main(['--stage','bench','--output',str(out)]),1)
            factory.assert_not_called();sidecars=list((root/M.REGISTRY).glob('*.failure.json'));self.assertEqual(len(sidecars),1)
            self.assertEqual(M.read(sidecars[0])['first_failure']['field'],'execution exception')

    def test_h0_prerequisite_semantic_tampering_rejected_even_with_new_file_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);out=root/M.H0;out.mkdir(parents=True)
            pins=dict(runtime={},schema_sha256_alpha='a'*64,keysets_sha256_alpha='b'*64,specification_pins_sha256_alpha='c'*64,files_sha256_alpha={},base_pins_sha256_alpha='d'*64)
            closure=M.source_closure(pins);prov=dict(source_closure_sha256_alpha=closure,execution_pins_sha256_alpha='e'*64);base=dict(prov,execution_pins_sha256_alpha=pins['base_pins_sha256_alpha'])
            shared=dict(complete=True,smoke=True,stage='H0',rows=40,steps=600,first_failure=None)
            identity=dict(shared,passed=True,provenance=base,claim=None,inference=None,gates={H.namespace(c,a):dict(complete=True,passed=True,rows=40,steps=600) for c in H.CONDITIONS for a in H.ARMS})
            metrics=dict(shared,provenance=base,clauses={},verdict='VALIDITY_ONLY')
            verification=dict(format='h17-run3-verification-v3',date=M.DATE,stage='H0',complete=True,passed=True,smoke=True,provenance=base,raw_sha256_alpha=None,checked_arrays=5556,gates=identity['gates'],clauses={},verdict='VALIDITY_ONLY',first_failure=None)
            self.assertEqual(set(verification),set(M.schema_contract()['metadata_keysets']['verification_success']))
            (out/'raw.npz.ap').write_bytes(b'ap');rawsha=M.file_digest(out/'raw.npz.ap');identity['raw_arrays']=dict(sha256_alpha=rawsha);verification['raw_sha256_alpha']=rawsha
            objects={'identity':identity,'metrics':metrics,'verification':verification}
            def write(key):
                path=out/(key+'.json');path.write_bytes(H.canonical(objects[key])+b'\n');return M.file_digest(path)
            h0=dict(source_closure_sha256_alpha=closure,raw_sha256_alpha=rawsha)
            for key in objects:h0[key+'_sha256_alpha']=write(key)
            parent=dict(shared,passed=True,source_closure_sha256_alpha=closure,verification_sha256_alpha=h0['verification_sha256_alpha'],raw_sha256_alpha=rawsha,clauses={},verdict='VALIDITY_ONLY')
            objects['parent_recomputation']=parent;h0['parent_recomputation_sha256_alpha']=write('parent_recomputation');pins['h0']=h0
            M.h0_prerequisites(root,pins,prov)
            for key,field,value in (('identity','smoke',False),('metrics','stage','bench'),('verification','provenance',prov),('verification','raw_sha256_alpha','f'*64),('parent_recomputation','verification_sha256_alpha','f'*64),('parent_recomputation','source_closure_sha256_alpha','g'*64),('metrics','clauses',{'unexpected':1})):
                before=objects[key][field];objects[key][field]=value;h0[key+'_sha256_alpha']=write(key)
                with self.assertRaises(H.EvidenceError),patch.object(np.random,'default_rng') as factory:M.h0_prerequisites(root,pins,prov)
                factory.assert_not_called();objects[key][field]=before;h0[key+'_sha256_alpha']=write(key)


if __name__=='__main__':unittest.main()
