"""Constructed boundary/corruption tests; the root runs these before spent H0."""
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile
import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import h17_r0_recording as recording
import measure_h17_r0 as runner


def fixture(steps=600,rows=2):
    z=np.zeros((steps,rows));pair=np.zeros((steps,rows,2));boolean=np.zeros((steps,rows),bool)
    return dict(H_pre=np.full((steps,rows),-1,np.int64),H_post=np.full((steps,rows),-1,np.int64),
        S_post=pair.copy(),SIL_pre=z.copy(),Y=pair.copy(),W_delivered=pair.astype(bool),
        AT2=pair.astype(bool),NAV=boolean.copy(),C=boolean.copy())


class ObservationTests(unittest.TestCase):
    def test_first_possible_marker_is_step_before_clock_value(self):
        s=fixture();o=recording.observations(s['W_delivered'],s['AT2'],s['H_post'],s['NAV'])
        np.testing.assert_array_equal(o['marker_step'],np.full(2,249))
        self.assertEqual(o['q_obs'][248,0],249);self.assertEqual(o['q_obs'][249,0],250)
        self.assertTrue(o['full_300'].all())

    def test_marker_reach_is_excluded_and_simultaneous_source_bits_survive(self):
        s=fixture();s['AT2'][249,0]=True;s['AT2'][250,1]=True
        s['W_delivered'][250,1]=True
        o=recording.observations(s['W_delivered'],s['AT2'],s['H_post'],s['NAV'])
        self.assertEqual(o['marker_reach_bits'][0],3);self.assertEqual(o['post_first_reach'][0],-1)
        self.assertFalse(o['reach_100'][0]);self.assertTrue(o['reach_censored'][0])
        self.assertEqual(o['post_reach_bits'][1],3);self.assertEqual(o['post_whiff_bits'][1],3)
        self.assertEqual(o['reach_delay'][1],1)

    def test_full_window_exact_boundary_and_right_censor(self):
        s=fixture();s['W_delivered'][49,0,0]=True;s['W_delivered'][50,1,0]=True
        s['AT2'][599,:,1]=True
        o=recording.observations(s['W_delivered'],s['AT2'],s['H_post'],s['NAV'])
        np.testing.assert_array_equal(o['marker_step'],np.array([299,300],np.int64))
        self.assertTrue(o['full_300'][0]);self.assertFalse(o['full_300'][1])
        self.assertTrue(o['reach_300'][0]);self.assertFalse(o['reach_300'][1])
        self.assertTrue(o['censored_300'][1]);self.assertEqual(o['available'][1],299)

    def test_no_marker_does_not_enter_conditional_denominator(self):
        s=fixture();s['W_delivered'][::200]=True
        o=recording.observations(s['W_delivered'],s['AT2'],s['H_post'],s['NAV'])
        self.assertTrue((o['marker_step']==-1).all())
        report=recording.wilson(o['reach_event'],o['marker_step']>=0,True)
        self.assertEqual(report['status'],'UNDEFINED');self.assertIsNone(report['estimate'])

    def test_delivered_only_clock_does_not_consult_raw_masked_column(self):
        s=fixture();raw=np.ones_like(s['W_delivered']);s['W_raw']=raw
        o=recording.observations(s['W_delivered'],s['AT2'],s['H_post'],s['NAV'])
        self.assertEqual(o['marker_step'][0],249)
        s['W_delivered'][200,0,1]=True
        o=recording.observations(s['W_delivered'],s['AT2'],s['H_post'],s['NAV'])
        self.assertEqual(o['marker_step'][0],450)


class N2Tests(unittest.TestCase):
    def test_prior_negative_to_unheld_retains_base_clock(self):
        s=fixture(1,2);s['H_pre'][0]=[1,1];s['SIL_pre'][0]=[41.,41.]
        s['S_post'][0,1]=[2.,2.]
        m=recording.n2_masks(s,np.array([[1.,-1.],[1.,-1.]]))
        self.assertTrue(m['negative_zero_units'][0,0]);self.assertTrue(m['negative_multiple_units'][0,1])
        self.assertTrue(m['withheld_N1_S'][0,1]);self.assertFalse(m['sustain'].any())
        np.testing.assert_array_equal(m['SIL_post'],np.ones((1,2)))

    def test_new_negative_hold_does_not_zero_and_negative_pre_blocks_sustain(self):
        s=fixture(1,2);s['H_pre'][0]=[-1,1];s['H_post'][0]=[1,0]
        s['SIL_pre'][0]=[7.,41.];s['S_post'][0,0,1]=2.;s['S_post'][0,1,0]=2.
        m=recording.n2_masks(s,np.array([[1.,-1.],[1.,-1.]]))
        self.assertTrue(m['withheld_N1_Z'][0,0]);self.assertEqual(m['SIL_post'][0,0],8.)
        self.assertTrue(m['negative_identity_change'][0,1]);self.assertFalse(m['sustain'][0,1])
        self.assertEqual(m['SIL_post'][0,1],0.)

    def test_timeout_and_evidence_are_independent_strict_flags(self):
        s=fixture(1,2);s['H_pre'][0]=[0,0];s['SIL_pre'][0]=[40.,41.]
        s['Y'][0,0]=[0.,.2];s['Y'][0,1]=[0.,.3]
        m=recording.n2_masks(s,np.zeros((2,2)))
        self.assertTrue(m['neither'][0,0]);self.assertTrue(m['both'][0,1])
        self.assertFalse(m['base'][0,1]);self.assertEqual(m['reset_drive'][0,1],10.)

    def test_unheld_index_never_reads_negative_last_column(self):
        s=fixture(1,2);m=recording.n2_masks(s,np.array([[0.,-1.],[0.,-1.]]))
        self.assertFalse(m['negS'].any());self.assertFalse(m['negZ'].any())


class EvidenceTests(unittest.TestCase):
    def test_typed_scalar_shape_and_constant_dedup(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'raw.npz.ap';a=recording.Archive(path)
            value=np.asarray(-0.,dtype=np.float64);key=a.put(value)
            self.assertEqual(key,a.put(value.copy()));self.assertEqual(len(a.blobs),1)
            a.array('scalar',value);manifest=a.finish()
            self.assertEqual(manifest['arrays']['scalar']['shape'],[])
            reverse=str.maketrans('abcdefghijklmnop','0123456789abcdef')
            with np.load(io.BytesIO(bytes.fromhex(path.read_text().translate(reverse))),allow_pickle=False) as archive:
                self.assertEqual(archive['scalar'].shape,());self.assertTrue(np.signbit(archive['scalar']))

    def test_equal_detects_signed_zero_and_dtype_corruption(self):
        with self.assertRaises(recording.EvidenceError):recording.equal(np.array([0.]),np.array([-0.]),'signed zero')
        with self.assertRaises(recording.EvidenceError):recording.equal(np.array([1],np.int64),np.array([1],np.int32),'dtype')

    def test_blob_generator_state_tag_retains_dictionary_insertion_order(self):
        with tempfile.TemporaryDirectory() as directory:
            a=recording.Archive(Path(directory)/'raw.npz.ap')
            tag=a.tag({'b':2,'a':1})
            self.assertEqual([entry[0]['value'] for entry in tag['items']],['b','a']);a.finish()

    def test_schema_closure_has_no_h0_cycle_and_complete_templates(self):
        pins=dict(runtime={'test':True},schema={'test':True},files_sha256_alpha={'source':'hash'})
        old=runner.source_closure(pins);pins['h0']={'identity_sha256_alpha':'different'}
        self.assertEqual(old,runner.source_closure(pins))
        schema=runner.schema_contract()
        for condition in runner.CONDITIONS:
            for arm in runner.ARMS:
                prefix=condition+'/'+arm
                self.assertIn(prefix+'/sample/SIL_base',schema['arrays'])
                self.assertIn(prefix+'/output/C2',schema['arrays'])
                self.assertIn(prefix+'/attribute_hashes',schema['arrays'])
        self.assertEqual(schema['arrays']['W1/Agent17/L3/w1sum/cum/600']['shape'],['R'])

    def test_pair_claim_survives_different_output_path(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);prov=dict(source_closure_sha256_alpha='closed',execution_pins_sha256_alpha='pinned')
            # A constructed pair tests filesystem exclusion; no generator is made.
            with patch.object(runner,'p5',lambda *args:None):
                path,obj=runner.claim_pair((1,2),prov,root/'first',root)
                self.assertFalse(obj['complete']);self.assertTrue(path.is_file())
                with self.assertRaises(recording.EvidenceError):runner.claim_pair((1,2),prov,root/'second',root)
                self.assertTrue(path.is_file())


if __name__=='__main__':unittest.main()
