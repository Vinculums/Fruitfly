"""Deterministic saved-input and corrupted-evidence tests. No trajectory/RNG."""
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import numpy as np

PATH=Path(__file__).resolve().parents[1]/'tools/verify_h17_run3.py'
SPEC=importlib.util.spec_from_file_location('verify_run3_under_test',PATH)
V=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(V)


class VerifyRun3Tests(unittest.TestCase):
    def setUp(self):
        self.no_rng=patch.object(np.random,'default_rng',side_effect=AssertionError('verifier constructed RNG'))
        self.no_rng.start();self.addCleanup(self.no_rng.stop)

    def schedule(self,pre,held=None,whiffs=None,enabled=True):
        pre=np.asarray(pre,np.int64);shape=pre.shape
        held=np.full(shape,-1,np.int64) if held is None else np.asarray(held,np.int64)
        whiffs=np.zeros(shape+(2,),bool) if whiffs is None else whiffs
        return V.gs_schedule(pre,whiffs,held,np.ones(shape),np.full(shape,180.),np.full(shape,3.),np.full(shape,180.),enabled)

    def test_integer_q_leg_and_slant_boundaries(self):
        x=self.schedule([248,249,278,279,338,339,398,399,428,429,548,549])
        np.testing.assert_array_equal(x['u'],[-1,0,29,30,89,90,149,150,179,180,299,300])
        np.testing.assert_array_equal(x['leg'],[0,1,1,2,2,3,3,3,3,4,4,5])
        np.testing.assert_array_equal(x['alpha'],[0,1,1,1,1,1,1,-1,-1,-1,-1,1])
        self.assertEqual(x['SEARCH_TGT'][1],255.)
        self.assertEqual(x['SEARCH_TGT'][7],285.)
        self.assertEqual(x['remaining'][3],60)

    def test_delayed_hold_entry_and_multiple_units_unheld(self):
        x=self.schedule([299,299,299],held=[-1,0,-1])
        np.testing.assert_array_equal(x['leg'],[2,0,2])
        np.testing.assert_array_equal(x['remaining'],[40,0,40])
        # A multiple-unit hold is represented by -1, exactly like zero units.
        self.assertTrue(x['engaged'][2]);self.assertFalse(x['engaged'][1])

    def test_any_delivered_resets_regardless_nav_or_valence(self):
        whiffs=np.zeros((3,2),bool);whiffs[0,0]=True;whiffs[1,1]=True
        x=self.schedule([500,500,500],whiffs=whiffs)
        np.testing.assert_array_equal(x['q_post'],[0,0,501])
        np.testing.assert_array_equal(x['engaged'],[False,False,True])
        # Masked RAW is deliberately absent from the policy input signature.
        self.assertTrue(self.schedule([500],whiffs=np.zeros((1,2),bool))['engaged'][0])

    def test_hold_interruption_keeps_q_phase(self):
        q=np.array([249,250,251],np.int64)
        x=self.schedule(q,held=[-1,0,-1])
        np.testing.assert_array_equal(x['q_post'],[250,251,252])
        np.testing.assert_array_equal(x['u'],[0,-1,2])

    def test_gsoff_updates_q_but_has_no_actual_entry(self):
        x=self.schedule([300,500],enabled=False)
        self.assertTrue(x['eligible'].all());self.assertFalse(x['engaged'].any())
        np.testing.assert_array_equal(x['q_post'],[301,501])
        np.testing.assert_array_equal(x['u'],[-1,-1])
        V.same(x['SEARCH_TURN'],x['BASE_TURN'],'off command')

    def test_inactive_signed_zero_and_active_no_final_clamp(self):
        x=V.gs_schedule(np.array([0,249],np.int64),np.zeros((2,2),bool),np.array([-1,-1],np.int64),
            np.ones(2),np.full(2,180.),np.array([-0.,60.]),np.full(2,180.))
        self.assertTrue(np.signbit(x['SEARCH_TURN'][0]))
        self.assertEqual(x['SEARCH_TURN'][1],100.)
        self.assertEqual(x['RESIDUAL'][1],60.)

    def test_observation_actual_entries_and_gsoff_none(self):
        w=np.zeros((600,1,2),bool);h=np.full((600,1),-1,np.int64);nav=np.zeros((600,1),bool)
        marker=np.zeros((600,1),bool);marker[300,0]=True
        obs=V.observation(w,w.copy(),h,nav,marker)
        self.assertEqual(obs['marker_step'][0],300)
        self.assertEqual(obs['q_obs'][249,0],250)
        self.assertFalse(obs['full_300'][0])
        self.assertEqual(V.observation(w,w,h,nav,np.zeros_like(marker))['marker_step'][0],-1)

    def test_strict_post_entry_window_excludes_marker_move(self):
        w=np.zeros((600,1,2),bool);at=w.copy();at[249,0]=True;w[350,0,0]=True
        h=np.full((600,1),-1,np.int64);nav=np.zeros((600,1),bool)
        obs=V.observation(w,at,h,nav)
        self.assertEqual(obs['marker_reach_bits'][0],3)
        self.assertFalse(obs['reach_100'][0]);self.assertFalse(obs['whiff_100'][0])
        self.assertTrue(obs['whiff_200'][0])

    def test_endpoints_keep_physical_and_good_identity_separate(self):
        w=np.zeros((600,2,2),bool);w[0,0,1]=True;at=w.copy();at[:3,0,0]=True;at[:4,0,1]=True
        sample=dict(W_delivered=w,AT2=at)
        x=V.endpoints(sample,{'good':np.array([1,0],np.int64)},np.zeros((600,2),bool))
        np.testing.assert_array_equal(x['V'],[True,False])
        np.testing.assert_array_equal(x['L'],[True,True])
        self.assertEqual(x['D_good'][0],4);self.assertEqual(x['D_other'][0],3)

    def test_reference_shadow_entry_is_never_actual_intervention(self):
        sample=dict(W_delivered=np.zeros((600,1,2),bool),AT2=np.zeros((600,1,2),bool))
        shadow=np.zeros((600,1),bool);shadow[249]=True
        x=V.endpoints(sample,{'good':np.zeros(1,np.int64)},np.zeros((600,1),bool),shadow)
        self.assertFalse(x['ever_engaged'][0]);self.assertEqual(x['first_entry_step'][0],249)
        self.assertEqual(x['entry_event_count'][0],1)

    def test_c0_late_whiff_counts_in_full_primary_and_cell(self):
        sample=dict(W_delivered=np.zeros((600,4,2),bool),AT2=np.zeros((600,4,2),bool),
            H_post=np.full((600,4),-1,np.int64),NAV=np.zeros((600,4),bool),C=np.zeros((600,4),bool))
        sample['W_delivered'][400,2,0]=True
        names=('negative_to_unheld negative_zero_units negative_multiple_units negative_identity_change '
            'negative_end negative_same base sustain zreset withheld_N1_S withheld_N1_Z neither timeout_only evidence_only both').split()
        masks={name:np.zeros((600,4),bool) for name in names}
        _,reading=V.metric_reading('C0',sample,dict(cell=np.arange(4),known=np.zeros((4,2))),masks)
        self.assertEqual(reading['primary']['numerator'],1)
        self.assertEqual(reading['cells']['2']['primary']['numerator'],1)
        self.assertEqual(reading['cells']['1']['primary']['numerator'],0)

    def test_bootstrap_uses_saved_matrix_and_rejects_index_corruption(self):
        idx=np.tile(np.arange(400,dtype=np.int64),(5000,1));delta=np.arange(400,dtype=np.int64)%3-1
        means,ci=V.paired_statistics(delta,idx)
        np.testing.assert_array_equal(means,np.full(5000,delta.mean()))
        np.testing.assert_array_equal(ci,[delta.mean(),delta.mean()])
        idx[0,0]=400
        with self.assertRaises(V.VerificationError):V.paired_statistics(delta,idx)

    def test_joint_clauses_do_not_substitute_positive_secondary(self):
        idx=np.tile(np.arange(400,dtype=np.int64),(5000,1));data={}
        for c in V.CONDITIONS:
            data[c]={}
            for arm in ('Fly','GS250'):
                data[c][arm]=dict(E=np.zeros(400,bool),L=np.zeros(400,bool),V=np.ones(400,bool),
                    D_other=np.zeros(400,np.int64),ever_engaged=np.zeros(400,bool))
        _,_,clauses,verdict=V.all_clauses(data,idx)
        self.assertEqual(len(clauses),9);self.assertEqual(verdict,'NOT_SHOWN')
        self.assertEqual(clauses['C0_absolute']['status'],'FAIL')
        self.assertEqual(clauses['T1_V']['status'],'PASS')

    def test_wilson_boundaries_and_equality_bars(self):
        mask=np.arange(400)<220
        self.assertGreaterEqual(V.wilson(mask)['interval'][0],.5)
        self.assertLess(V.wilson(np.arange(400)<219)['interval'][0],.5)
        self.assertEqual(V.clause([-.05,0],-.05,'lower',0)['status'],'PASS')
        self.assertEqual(V.clause([0,.05],.05,'upper',0)['status'],'PASS')

    def test_keysets_h0_exact_exclusion_and_q_fieldsets(self):
        root=PATH.parents[1];schema=V.read(root/V.SCHEMA);arrays=V.read(root/V.KEYSETS);schema=dict(schema,arrays=arrays)
        self.assertEqual(len(arrays),5580)
        self.assertEqual(len([k for k in arrays if not k.startswith('inference/')]),5556)
        self.assertEqual(V.source_schema(schema,'efficacy/C0/GS250/state_timeline',{},True),
            {'dtype':'|S64','shape':[3001,77]})
        self.assertEqual(V.source_schema(schema,'efficacy/C0/GS250/rng_timeline',{},False)['shape'],[4801,7])
        with self.assertRaises(V.VerificationError):V.source_schema(schema,'inference/indices',{},True)
        with self.assertRaises(V.VerificationError):V.source_schema(schema,'not_registered',{},False)

    def test_native_shape_object_and_extra_zip_key_rejected(self):
        buf=io.BytesIO()
        with zipfile.ZipFile(buf,'w') as z:
            with z.open('value.npy','w') as f:np.lib.format.write_array(f,np.array(3.,np.float64),allow_pickle=False)
        buf.seek(0)
        desc={'arrays':{'value':{}}}
        with zipfile.ZipFile(buf) as z:
            self.assertEqual(V.archive_headers(z,desc,{'value':{'dtype':'<f8','shape':[]}}),['value.npy'])
            with self.assertRaises(V.VerificationError):V.archive_headers(z,desc,{'value':{'dtype':'<f8','shape':[1]}})
            with self.assertRaises(V.VerificationError):V.archive_headers(z,{'arrays':{}},{})

    def test_typed_blobs_bitwise_hash_and_class_whitelist(self):
        a=np.array([-0.,1.]);descriptor={'kind':'ndarray','dtype':a.dtype.str,'shape':list(a.shape)}
        key=V.digest(V.canonical(descriptor)+a.tobytes())
        table=V.BlobTable({'blob/'+key:a},{key:descriptor});V.same(table.get(key),a,'native bytes')
        with self.assertRaises(V.VerificationError):V.BlobTable({'blob/'+key:np.array([0.,1.])},{key:descriptor})
        with self.assertRaises(V.VerificationError):table.tag({'type':'type','value':'numpy.int64'})
        with self.assertRaises(V.VerificationError):table.tag({'type':'int','value':True})
        with self.assertRaises(V.VerificationError):table.tag({'type':'numpy_scalar','dtype':'O','value_hex_alpha':'aa'})

    def test_failure_keyset_matches_schema(self):
        schema=V.read(PATH.parents[1]/V.SCHEMA)
        e=V.VerificationError('bad',index=[1],phase='wrapper')
        self.assertEqual(set(e.first_failure),set(schema['metadata_keysets']['first_failure']))
        self.assertNotIn('passed',schema['metadata_keysets']['metrics_success'])

    def test_unreferenced_blob_rejected_before_aggregation(self):
        payloads={};descriptors={};ids=[]
        for value in (1.,2.):
            a=np.array([value]);d=dict(kind='ndarray',dtype=a.dtype.str,shape=list(a.shape))
            key=V.digest(V.canonical(d)+a.tobytes());ids.append(key)
            payloads['blob/'+key]=a;descriptors[key]=d
        payloads['fixture/state_timeline']=np.array([[ids[0]]],dtype='S64')
        with self.assertRaises(V.VerificationError):V.blob_closure({},None,payloads,V.BlobTable(payloads,descriptors))
        del payloads['blob/'+ids[1]];del descriptors[ids[1]]
        V.blob_closure({},None,payloads,V.BlobTable(payloads,descriptors))

    def test_event_order_mutation_rejected(self):
        record={'events':[{'step':-1,'phase':'construction'}]+[
            {'step':0,'phase':p} for p in ('pre','base','pre_wrapper','wrapper','bump')]}
        V.event_contract(record,1,'fixture');record['events'][2]['phase']='pre_wrapper'
        with self.assertRaises(V.VerificationError):V.event_contract(record,1,'fixture')

    def test_native_header_binds_arm_world_and_original_constants(self):
        for arm in V.ARMS:
            metadata=dict(world='C0',arm='Fly' if arm in ('Fly','Passive') else arm,G=2.,fixed=False,
                steps=600,draws_equal=True,rng_equal=True)
            V.native_header(metadata,'C0',arm,'fixture')
            for key,value in (('world','T1'),('arm','other'),('G',3.),('fixed',True),('steps',599),('draws_equal',False)):
                corrupted=dict(metadata);corrupted[key]=value
                with self.assertRaises(V.VerificationError):V.native_header(corrupted,'C0',arm,'fixture')

    def test_never_engaged_checks_full_native_row_and_global_states(self):
        class Timeline:
            timeline=[None,None]
            def __init__(self,fields,data):self.fields=fields;self.data=data
            def get(self,index,field):return self.data[field]
        left=Timeline(['weights','constant'],dict(weights=np.zeros((2,4,3)),constant=4))
        right=Timeline(['weights','constant','q'],dict(weights=np.zeros((2,4,3)),constant=4))
        rows=np.array([True,False]);right.data['weights'][1]=9
        V.never_engaged_states(left,right,rows,'fixture')
        right.data['weights'][0,0,0]=1
        with self.assertRaises(V.VerificationError):V.never_engaged_states(left,right,rows,'fixture')
        right.data['weights'][0]=0;right.data['constant']=5
        with self.assertRaises(V.VerificationError):V.never_engaged_states(left,right,rows,'fixture')

    def test_no_executable_expression_evaluation(self):
        import ast
        with self.assertRaises(ValueError):V.expression(ast.parse('np.random.default_rng()').body[0].value,{})

    def test_inference_exact_native_signature_and_saved_return(self):
        schema=V.read(PATH.parents[1]/V.SCHEMA)
        indices=np.tile(np.arange(400,dtype=np.int64),(5000,1))
        before={'bit_generator':'PCG64','state':{'state':1,'inc':3},'has_uint32':0,'uinteger':0}
        after={'bit_generator':'PCG64','state':{'state':2,'inc':3},'has_uint32':0,'uinteger':0}
        values={'seed':(5,),'empty':{},'args':(0,400),
            'kwargs':dict(size=(5000,400),dtype='<i8',endpoint=False),'result':indices,
            'before':V.GeneratorState(before),'after':V.GeneratorState(after)}
        class Table:
            def get(self,key):return values[key.decode() if isinstance(key,bytes) else key]
        call=dict(generator=0,method='integers',args='args',kwargs='kwargs',result='result',
            before='before',after='after',step=-1,phase='inference');values['call']=call
        creation=dict(index=0,role='inference',seed_args='seed',seed_kwargs='empty',initial='before',state_type='PCG64',handle_type='Generator')
        metadata=dict(role='INFERENCE',replicates=5000,quantile_method='linear',indices_key='inference/indices',
            creation=creation,initial_state='before',final_state='after',primitive=call,
            indices_sha256_alpha=V.array_descriptor(indices)['sha256_alpha'])
        arrays={'inference/call_refs':np.array(['call'],dtype='S64'),
            'inference/checkpoints':np.array(['before','after'],dtype='S64'),'inference/indices':indices}
        V.inference_check(arrays,metadata,Table(),5,schema)
        for name,value in (('dtype','<i4'),('endpoint',True),('size',(5000,399))):
            original=values['kwargs'][name];values['kwargs'][name]=value
            with self.assertRaises(V.VerificationError):V.inference_check(arrays,metadata,Table(),5,schema)
            values['kwargs'][name]=original
        values['result']=indices.copy();values['result'][0,0]=1
        with self.assertRaises(V.VerificationError):V.inference_check(arrays,metadata,Table(),5,schema)

    def test_same_state_own_transcript_and_complete_field_proof(self):
        schema=V.read(PATH.parents[1]/V.SCHEMA);prefix='efficacy/C0/GS250'
        logs=[dict(generator=0,step=0,phase='base_act',slot=i) for i in range(4)]
        values={'pre':{'x':np.array([0.])},'post':{'x':np.array([1.])},
            'ret':(np.array([3.]),np.array([-1],np.int64)),'comparison':dict(passed=True,fields=['x'])}
        values.update({str(i):log for i,log in enumerate(logs)})
        class Table:
            def get(self,key):return values[key]
        class Timeline:
            fields=['q','x']
            def get(self,row,field):return np.array([0. if row==1 else 1.])
        proof=dict(same_state=dict(method='unchanged_Fly_act_recorded_primitives',pre_state_refs=['pre'],
            input_refs=['input'],primitive_refs=[['0','1','2','3']],expected_state_refs=['post'],
            expected_return_refs=['ret'],comparison_refs=['comparison'],first_failure=None),plain_logger_H0=None)
        record=dict(generator_instances=[dict(role='agent')],draw_log=logs)
        arrays={prefix+'/input_timeline':np.array(['input'],dtype='S64')}
        gs={'BASE_TURN':np.array([[3.]])};sample={'H_post':np.array([[-1]],np.int64)}
        def verify():V.own_state_proof(proof,record,Timeline(),arrays,prefix,Table(),gs,sample,'GS250',schema)
        verify()
        values['post']['x'][0]=2.
        with self.assertRaises(V.VerificationError):verify()
        values['post']['x'][0]=1.;values['comparison']['fields']=[]
        with self.assertRaises(V.VerificationError):verify()
        values['comparison']['fields']=['x'];record['draw_log']=logs[:-1]
        with self.assertRaises(V.VerificationError):verify()
        record['draw_log']=logs;proof['same_state']['input_refs']=['other_arm_input']
        with self.assertRaises(V.VerificationError):verify()

    def test_plain_logger_full_typed_recipe_detects_return_and_hash_change(self):
        schema=V.read(PATH.parents[1]/V.SCHEMA);prefix='efficacy/C0/GS250'
        state=np.array([['s']],dtype='S64');world=np.array([['w']],dtype='S64');rng=np.array([['r']],dtype='S64')
        inputs=np.array(['i'],dtype='S64');returns=np.array(['t'],dtype='S64');base=np.array(['b'],dtype='S64')
        hashes=np.array([['h']],dtype='S64');out=np.array([1.]);events=[dict(step=-1,phase='construction')]
        instance=dict(index=0,role='agent',seed_args='seed',seed_kwargs='empty',initial='initial',state_type='PCG64',handle_type='GeneratorTap')
        record=dict(output_metadata={'world':'C0'},state_fields=['q'],world_fields=['t'],events=events,
            rng_labels=events,generator_instances=[instance])
        literal=dict(instance,handle_type='Generator')
        values=dict(outputs={'X':out,'world':'C0'},state=dict(fields=['q'],events=events,timeline=state,attribute_hashes=hashes),
            world=dict(fields=['t'],events=events,timeline=world),rng=dict(labels=events,timeline=rng,instances=[literal]),
            inputs=inputs,returns=dict(actual=returns,base=base),construction={'good':np.array([0],np.int64)},
            comparison=dict(passed=True,fields=['q'],world_fields=['t'],events=events,rng_labels=events))
        class Table:
            def get(self,key):return values[key]
        arrays={prefix+'/'+k:v for k,v in dict(state_timeline=state,attribute_hashes=hashes,world_timeline=world,
            rng_timeline=rng,input_timeline=inputs,return_timeline=returns,base_return_timeline=base).items()}
        arrays[prefix+'/output/X']=out;arrays[prefix+'/construction/good']=values['construction']['good']
        proof=dict(plain_logger_H0=dict(method='literal_GS250_vs_logged_GS250_full_run',candidate_class='GS250',
            spent_pair_alias='h29/smoke',native_outputs_ref='outputs',state_refs='state',world_refs='world',input_refs='inputs',
            return_refs='returns',rng_refs='rng',construction_refs='construction',comparison_refs='comparison',first_failure=None))
        def verify():V.plain_logger_proof(proof,arrays,record,prefix,Table(),True,schema)
        verify();values['returns']['base']=np.array(['other'],dtype='S64')
        with self.assertRaises(V.VerificationError):verify()
        values['returns']['base']=base;values['state']['attribute_hashes']=np.array([['other']],dtype='S64')
        with self.assertRaises(V.VerificationError):verify()


if __name__=='__main__':unittest.main()
