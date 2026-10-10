"""Corrupted saved evidence and exact passive-route definitions; no simulation."""
import importlib.util
from pathlib import Path
import unittest
from unittest import mock
import numpy as np

PATH=Path(__file__).resolve().parents[1]/'tools/verify_hold_e1.py'
SPEC=importlib.util.spec_from_file_location('independent_e1',PATH)
v=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(v)


class SavedE1Tests(unittest.TestCase):
    def test_byte_change_rejected_even_with_same_shape_and_dtype(self):
        original=np.array([0.,1.],dtype=np.float64)
        descriptor=v.array_descriptor(original)
        corrupt=original.copy();corrupt.view(np.uint8)[0]^=1
        with self.assertRaises(v.VerificationError):v.check_descriptor(corrupt,descriptor,'corrupted array')

    def test_shape_and_dtype_change_rejected(self):
        original=np.arange(4,dtype=np.int64)
        for corrupt in (original.reshape(2,2),original.astype(np.int32)):
            with self.assertRaises(v.VerificationError):v.check_descriptor(corrupt,v.array_descriptor(original),'changed schema')

    def test_burst_requires_two_previous_whiffs_in_inclusive_nine_steps(self):
        x=np.zeros((13,1,3),bool);x[[0,1,9,11,12],0,1]=True
        burst,bb,w2=v.burst_evidence(x,-1e9,9)
        self.assertTrue(burst[9,0,1])
        self.assertFalse(burst[11,0,1])
        self.assertTrue(burst[12,0,1])
        self.assertEqual(bb[11,0,1],9.)
        self.assertEqual(w2[11,0,1],9.)

    def test_lost_original_columns_excludes_D_and_uses_last_two_hundred(self):
        x=np.zeros((600,3,3),bool);x[:,0,2]=True;x[399,1,0]=True;x[400,2,1]=True
        np.testing.assert_array_equal(v.lost_original(x),[True,True,False])

    def test_targets_can_differ_without_pre_noise_command_difference(self):
        command=v.clip_command(np.array([270.,260.,100.,110.]),np.zeros(4),{'GAIN':.6,'MAXTURN':40.})
        np.testing.assert_array_equal(command,[-40.,-40.,40.,40.])

    def route_fixture(self):
        # Two rows: counter absence alone and neither-read alone must each fail
        # T1. Three-channel B/D presence and top status are already tied.
        h={'identity':np.array([[0,1]]),'nav':np.array([[False,False]]),
           'presence':np.ones((1,2,3),bool),'top':np.ones((1,2,3),bool),'clipped_turn':np.array([[0.,0.]])}
        r={k:value.copy() for k,value in h.items()};r['identity'][:]=2;r['nav'][:]=True;r['clipped_turn'][:]=1.
        state={'whiffs':np.array([[[False,True,False],[False,True,False]]]),
               'counter_post':np.array([[[300.,0.,300.],[299.,0.,300.]]]),
               'timeout':np.zeros((1,2),bool),'evidence':np.zeros((1,2),bool)}
        return h,r,state

    def test_T1_requires_both_counter_absence_and_neither_read(self):
        h,r,state=self.route_fixture();burst=np.zeros((1,2,3),bool);bb=np.zeros((1,2,3))
        routes=v.routes(h,r,state,np.zeros(2,int),{'N_HI':{3:300},'NEVER':-1e9},burst,bb)
        np.testing.assert_array_equal(routes['T1_noVcounter_both'],[[True,False]])
        np.testing.assert_array_equal(routes['T1_read_neither_V'],[[False,True]])
        self.assertFalse(routes['T1'].any())

    def test_never_timestamp_is_not_a_latest_burst_tie(self):
        h,r,state=self.route_fixture()
        result=v.routes(h,r,state,np.zeros(2,int),{'N_HI':{3:300},'NEVER':-1e9},np.zeros((1,2,3),bool),np.full((1,2,3),-1e9))
        self.assertFalse(result['T3'].any())
        np.testing.assert_array_equal(result['command_presence_equal'],result['command'])
        self.assertFalse(result['command_presence_difference'].any())

    def test_forged_first_step_is_rejected(self):
        mask=np.array([[False,True],[True,False],[True,True]])
        np.testing.assert_array_equal(v.first_true(mask),[1,0])
        with self.assertRaises(v.VerificationError):v.same(np.array([0,0]),v.first_true(mask),'forged first command')

    def test_empty_exposure_and_interpretation_thresholds(self):
        self.assertEqual(v.mask_metric(np.zeros((600,400),bool))['rows'],0)
        flags=dict(X1=True,X2=True,X3=False,X4=True)
        self.assertEqual(v.screen_reading(flags,0),'NOT REACHED IN THIS SAMPLE')
        self.assertEqual(v.screen_reading(flags,39),'REACHED, BELOW REGISTERED SCREEN')
        self.assertEqual(v.screen_reading(dict(flags,X3=True),40),'READABLE FOR A SEPARATE BENEFIT DESIGN')
        self.assertEqual(v.screen_reading(dict(flags,X2=False),40),'BLOCKED: POSITIVE CONTROL NOT REACHED')

    def test_evidence_helpers_do_not_construct_random_generators(self):
        with mock.patch.object(np.random,'default_rng',side_effect=AssertionError('fresh RNG forbidden')):
            v.source_constants(v.ROOT)
            v.burst_evidence(np.zeros((3,2,3),bool),-1e9,9)
            v.lost_original(np.zeros((600,2,3),bool))
            v.clip_command(np.array([180.]),np.zeros(1),{'GAIN':.6,'MAXTURN':40.})

    def audit_fixture(self):
        before=['a'*64]*11
        phase={'before':before.copy()};previous=before.copy()
        for kind,indices in (('sense',[0]),('wind',[0]),('D',[4]),('twin',[2]),('act',[5,6]),('bump',[])):
            now=previous.copy()
            for index in indices:now[index]=chr(ord('b')+len(phase))*64
            if kind=='twin':now[2]=now[0]
            phase[kind]=now;previous=now
        state={name:np.zeros((1,2)) for name in ('whiffs','wind_on','heading','rotation','turn','actual_hold')}
        state['actual_hold']=np.zeros((1,2),np.int64)
        record={'audit':{'creation':before.copy(),'construction':before.copy(),'final':phase['bump'].copy(),'phases':[phase],'balance':True},
                'rng_events':[phase['act'].copy(),phase['bump'].copy()],
                'input_digests':[v.digest(b''.join(v.snapshot_blob(state[k][0]) for k in ('whiffs','wind_on','heading','rotation')))],
                'return_digests':[v.digest(b''.join(v.snapshot_blob(state[k][0]) for k in ('turn','actual_hold')))]}
        l2={name:np.array([phase['act'][5],phase['bump'][5]]) for name in ('rng','sel.rng','ring.rng','mb.rng')}
        l2['sel.rng3']=np.array([phase['act'][6],phase['bump'][6]])
        return record,state,l2

    def test_unregistered_generator_draw_is_rejected(self):
        record,state,l2=self.audit_fixture()
        v.audit_check(record,state,l2,1,'constructed saved audit')
        record['audit']['phases'][0]['D'][7]='p'*64
        with self.assertRaises(v.VerificationError):v.audit_check(record,state,l2,1,'extra odour draw')

    def test_forged_input_digest_is_rejected(self):
        record,state,l2=self.audit_fixture();record['input_digests'][0]='p'*64
        with self.assertRaises(v.VerificationError):v.audit_check(record,state,l2,1,'changed input transcript')


if __name__=='__main__':unittest.main()
