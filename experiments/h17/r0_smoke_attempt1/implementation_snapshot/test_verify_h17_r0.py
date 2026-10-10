"""Constructed saved-state verifier tests; no trajectories or random draws."""
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import numpy as np

PATH=Path(__file__).resolve().parents[1]/'tools/verify_h17_r0.py'
SPEC=importlib.util.spec_from_file_location('verify_h17_r0_under_test',PATH)
V=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(V)


class VerifyTests(unittest.TestCase):
    def test_cold_marker_is_sensing_index_249(self):
        w=np.zeros((600,2,2),bool);at=w.copy();h=np.full((600,2),-1,np.int64)
        nav=np.zeros((600,2),bool)
        x=V.observation(w,at,h,nav)
        np.testing.assert_array_equal(x['marker_step'],[249,249])
        self.assertEqual(x['q_obs'][249,0],250)
        self.assertEqual(x['longest_silence'][0],600)

    def test_delivered_whiff_restarts_clock_and_no_marker(self):
        w=np.zeros((600,2,2),bool);w[240,0,0]=True;w[480,0,1]=True
        h=np.full((600,2),-1,np.int64);h[:,1]=0
        x=V.observation(w,np.zeros_like(w),h,np.zeros((600,2),bool))
        np.testing.assert_array_equal(x['marker_step'],[-1,-1])
        self.assertEqual(x['q_obs'][240,0],0)
        self.assertEqual(x['longest_silence'][0],240)

    def test_windows_exclude_marker_include_endpoint_censor_late(self):
        w=np.zeros((600,2,2),bool);at=np.zeros_like(w);h=np.zeros((600,2),np.int64)
        h[249,0]=-1;h[500,1]=-1
        at[249,0]=True;at[349,0,0]=True;w[350,0,0]=True
        x=V.observation(w,at,h,np.zeros((600,2),bool))
        np.testing.assert_array_equal(x['full_100'],[True,False])
        np.testing.assert_array_equal(x['censored_100'],[False,True])
        np.testing.assert_array_equal(x['reach_100'],[True,False])
        self.assertFalse(x['whiff_100'][0])
        self.assertEqual(x['marker_reach_bits'][0],3)
        self.assertEqual(x['available'][1],99)

    def test_simultaneous_first_events_keep_both_bits(self):
        w=np.zeros((600,1,2),bool);w[250,0]=True
        at=np.zeros_like(w);at[251,0]=True
        x=V.observation(w,at,np.full((600,1),-1,np.int64),np.zeros((600,1),bool))
        self.assertEqual(x['first_whiff_bits'][0],3)
        self.assertEqual(x['post_whiff_bits'][0],3)
        self.assertEqual(x['post_reach_bits'][0],3)
        self.assertEqual(x['whiff_delay'][0],1)

    def test_n2_negative_multiactive_not_unique_hold(self):
        sample=dict(H_pre=np.array([[1,0]],np.int64),H_post=np.array([[-1,1]],np.int64),
            W_delivered=np.zeros((1,2,2),bool),Y=np.zeros((1,2,2)),
            SIL_pre=np.array([[41.,41.]]),S_post=np.array([[[1.1,1.2],[0.9,1.3]]]))
        x=V.n2(sample,np.array([[1.,-1.],[1.,-1.]]))
        self.assertTrue(x['base'][0,0]);self.assertFalse(x['sustain'][0,0])
        self.assertTrue(x['negative_multiple_units'][0,0])
        self.assertFalse(x['negative_zero_units'][0,0])
        self.assertTrue(x['withheld_N1_S'][0,0]);self.assertEqual(x['SIL_post'][0,0],1.)
        # Sustain keys off PRE positive hold even when POST new hold is negative.
        self.assertTrue(x['sustain'][0,1]);self.assertTrue(x['negZ'][0,1])
        self.assertEqual(x['SIL_post'][0,1],41.)

    def test_zreset_reads_base_not_post_clock(self):
        sample=dict(H_pre=np.array([[-1]],np.int64),H_post=np.array([[0]],np.int64),
            W_delivered=np.zeros((1,1,2),bool),Y=np.zeros((1,1,2)),
            SIL_pre=np.array([[4.]]),S_post=np.array([[[1.1,0.2]]]))
        x=V.n2(sample,np.array([[1.,0.]]))
        self.assertTrue(x['zreset'][0,0]);self.assertEqual(x['SIL_base'][0,0],5.)
        self.assertEqual(x['SIL_post'][0,0],0.)

    def test_zero_conditional_is_undefined_not_zero(self):
        result=V.wilson(np.array([False]),np.array([False]),True)
        self.assertIsNone(result['estimate']);self.assertIsNone(result['interval'])
        self.assertEqual(result['status'],'UNDEFINED')
        self.assertEqual(V.wilson(np.array([True]),conditional=True)['status'],'UNREADABLE')

    def test_bitexact_float_and_first_failure_index(self):
        with self.assertRaises(V.VerificationError) as raised:
            V.same(np.array([0.,-0.]),np.array([0.,0.]),'state','act')
        self.assertEqual(raised.exception.first_failure,dict(field='state',index=[1],phase='act'))

    def test_typed_blob_roundtrip_and_tampering(self):
        a=np.array([-0.,1.],np.float64)
        desc=dict(kind='ndarray',dtype=a.dtype.str,shape=list(a.shape))
        key=V.digest(V.canonical(desc)+a.tobytes())
        table=V.BlobTable({'blob/'+key:a},{key:desc})
        V.same(table.get(key),a,'roundtrip')
        with self.assertRaises(V.VerificationError):
            V.BlobTable({'blob/'+key:np.array([0.,1.])},{key:desc})

    def test_typed_json_rejects_unknown_and_wrong_scalar_type(self):
        table=V.BlobTable({}, {})
        with self.assertRaises(V.VerificationError):table.tag({'type':'int','value':True})
        with self.assertRaises(V.VerificationError):table.tag({'type':'pickle','value':'x'})
        with self.assertRaises(V.VerificationError):table.tag({'type':'numpy_scalar','dtype':'O','value_hex_alpha':'aa'})

    def test_duplicate_json_and_nonfinite_rejected(self):
        with self.assertRaises(V.VerificationError):
            json.loads('{"x":1,"x":2}',object_pairs_hook=V.unique)

    def test_data_only_constants_never_evaluate_call(self):
        import ast
        with self.assertRaises(ValueError):V.expression(ast.parse('run_trajectory()').body[0].value,{})

    def test_stored_constructor_corruption_is_rejected_without_overwrite(self):
        r=1
        initial={'sel.s':np.zeros((r,2)),'sel.S':np.zeros((r,1)), 'up.P':np.zeros((r,2)),
            'silence':np.zeros(r),'since':np.zeros(r),'c':np.full((r,2),140.),'ring.s':np.zeros((r,16)),
            'N':200,'N_hi':200,'P':60,'present':np.ones((r,2),bool),'known':np.zeros((r,2)),
            'codes':np.zeros((r,2,200))}
        class Timeline:
            def row(self,index):return initial
        construction=dict(S0=initial['sel.s'].copy(),SG0=initial['sel.S'][:,0].copy(),UP0=initial['up.P'].copy(),
            SIL0=initial['silence'].copy(),SINCE0=initial['since'].copy(),C0=initial['c'].copy(),
            ring0=initial['ring.s'].copy(),codes0=initial['codes'].copy(),known=initial['known'].copy())
        construction['codes0'][0,0,0]=1.
        with self.assertRaises(V.VerificationError) as raised:
            V.snapshot_sample_check(Timeline(),{'H_post':np.empty((0,r),np.int64)},construction,'fixture')
        self.assertEqual(raised.exception.first_failure['field'],'fixture/stored construction/codes0')
        self.assertEqual(construction['codes0'][0,0,0],1.)

    def test_phase_contract_rejects_pre_after_base(self):
        record={'events':[{'step':-1,'phase':'construction'}, {'step':0,'phase':'base'},
                          {'step':0,'phase':'pre'}, {'step':0,'phase':'act'}, {'step':0,'phase':'bump'}]}
        with self.assertRaises(V.VerificationError):V.event_contract(record,1,'fixture')

    def test_l3_is_dwell_majority_not_first_arrival(self):
        at=np.zeros((600,1,2),bool);at[0,0,0]=True;at[2:5,0,1]=True
        o={'AT2':at,'W':np.zeros_like(at),'H':np.full((600,1),-1,np.int8),'C':np.zeros((600,1),bool)}
        score=V.physical_scores(o,np.array([0],np.int64))
        self.assertEqual(score['choice'][0],1)
        self.assertEqual(score['first'][0,0],0)

    def test_native_array_schema_rejects_unpinned_and_dimension_drift(self):
        schema={'dtype_kinds':'biufUS','arrays':{'T1/Fly/state_timeline':{'dtype':'|S64','shape':['E',2]}}}
        result=V.source_schema(schema,'T1/Fly/state_timeline',{},False)
        self.assertEqual(result,{'dtype':'|S64','shape':[2401,2]})
        with self.assertRaises(V.VerificationError):V.source_schema(schema,'T1/Fly/unregistered',{},False)
        with self.assertRaises(V.VerificationError):V.source_schema(schema,'blob/'+'a'*64,{'dtype':'O','shape':[1]},False)

    def test_claim_design_pair_and_output_provenance_are_checked(self):
        root=V.ROOT;directory=root/'experiments/h17/test_claim_fixture';pair=(5,6)
        saved=V.digest(b'saved');closure='a'*64;pin='b'*64
        runtime={'fixture':'saved runtime'}
        prov=dict(runtime=runtime,source_closure_sha256_alpha=closure,design_sha256_alpha=saved,
                  config_sha256_alpha=saved,registration_sha256_alpha=saved,opening_sha256_alpha=saved,
                  execution_pins_sha256_alpha=pin)
        key=V.digest(V.canonical(list(pair)))
        claimpath=root/'experiments/h17/r0_registry'/(key+'.json')
        identity={'provenance':prov,'claim':claimpath.relative_to(root).as_posix(),'raw_arrays':{'sha256_alpha':saved}}
        pins={'runtime':runtime,'source_closure_sha256_alpha':closure,'h0':dict(source_closure_sha256_alpha=closure,
            identity_sha256_alpha=saved,metrics_sha256_alpha=saved,raw_sha256_alpha=saved,verification_sha256_alpha=saved)}
        claim=dict(complete=True,pair_sha256_alpha=key,provenance_sha256_alpha=V.digest(V.canonical(prov)),
            source_closure_sha256_alpha=closure,execution_pins_sha256_alpha=pin,design_sha256_alpha=saved,
            output_path_sha256_alpha=V.digest(str(directory.resolve()).encode('utf-8')),decision='decision:h17-r0-open',
            claim_rule='one registered pair, durable before first generator',identity_sha256_alpha=saved,raw_sha256_alpha=saved)
        def reader(path):
            if path.parent.name=='r0_smoke':return {'complete':True,'passed':True,'smoke':True}
            return claim
        with patch.object(Path,'read_bytes',return_value=b'saved'),patch.object(V,'read',side_effect=reader):
            V.runtime_provenance(identity,pins,pin,root,False,directory,pair)
            for field in ('pair_sha256_alpha','design_sha256_alpha','output_path_sha256_alpha','source_closure_sha256_alpha'):
                original=claim[field];claim[field]='p'*64
                with self.assertRaises(V.VerificationError):V.runtime_provenance(identity,pins,pin,root,False,directory,pair)
                claim[field]=original

    def test_changed_source_bytes_are_rejected(self):
        with patch.object(Path,'is_file',return_value=True),patch.object(Path,'read_bytes',return_value=b'changed'):
            with self.assertRaises(V.VerificationError) as raised:
                V.check_source_files(V.ROOT,{'src/fly.py':V.digest(b'original')})
        self.assertEqual(raised.exception.first_failure['field'],'pins/source/src/fly.py')

    def test_archive_object_and_unknown_keys_rejected_before_payload(self):
        def archive(value,key='x'):
            result=io.BytesIO()
            with zipfile.ZipFile(result,'w') as z:
                data=io.BytesIO();np.lib.format.write_array(data,value,allow_pickle=True)
                z.writestr(key+'.npy',data.getvalue())
            result.seek(0);return zipfile.ZipFile(result)
        with archive(np.array([{}],dtype=object)) as z:
            with self.assertRaises(V.VerificationError):
                V.archive_headers(z,{'arrays':{'x':{}}},{'x':{'dtype':'|O','shape':[1]}})
        with archive(np.array([1],np.int64),'unexpected') as z:
            with self.assertRaises(V.VerificationError):
                V.archive_headers(z,{'arrays':{'x':{}}},{'x':{'dtype':'<i8','shape':[1]}})

    def test_terminal_marker_retains_zero_followup_and_censoring(self):
        w=np.zeros((600,1,2),bool);h=np.zeros((600,1),np.int64);h[599]=-1
        x=V.observation(w,np.zeros_like(w),h,np.zeros((600,1),bool))
        self.assertEqual(x['marker_step'][0],599);self.assertEqual(x['available'][0],0)
        self.assertTrue(x['whiff_censored'][0]);self.assertFalse(x['whiff_event'][0])
        self.assertFalse(x['full_100'][0]);self.assertTrue(x['censored_100'][0])


if __name__=='__main__':unittest.main()
