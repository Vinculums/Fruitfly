"""Intervention boundary and censoring checks on constructed local states."""
from pathlib import Path
import sys
import unittest
import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import fly
from hold_stage2_arm import ReadOutFly
from hold_stage2_harness import leave_latency, i4_scores, equal, M, I4_W1_HOLD_KEYS
import ph16


class ReadBoundary(unittest.TestCase):
    def test_initial_negative_read_flees_but_returns_actual_hold(self):
        world=ph16.Still(4)
        values=np.tile((1.,-1.),(4,1))
        x=np.tile((False,True),(4,1))
        a=ReadOutFly(4,np.random.default_rng(5),values)
        _,h=a.act(world,x,np.ones(4,bool))
        np.testing.assert_array_equal(h,np.full(4,-1))
        np.testing.assert_array_equal(a.hr,np.ones(4,int))
        np.testing.assert_array_equal(a.tgt,a.flee_side)

    def test_actual_switch_reproduces_fly_and_draws(self):
        world=ph16.Still(8)
        values=np.tile((1.,-1.),(8,1))
        a=ReadOutFly(8,np.random.default_rng(6),values,read='actual')
        b=fly.Fly(8,np.random.default_rng(6),values)
        inputs=np.random.default_rng(5).random((80,8,2))<0.12
        for x in inputs:
            ar=a.act(world,x,np.ones(8,bool));br=b.act(world,x,np.ones(8,bool))
            for av,bv in zip(ar,br):np.testing.assert_array_equal(av,bv)
            for key in ('since','silence','present','c','tgt','sustain','zreset'):
                np.testing.assert_array_equal(getattr(a,key),getattr(b,key))
            self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)

    def test_invalid_read_rejected(self):
        with self.assertRaises(ValueError):
            ReadOutFly(1,np.random.default_rng(5),np.zeros((1,2)),read='off')


class LeaveLatency(unittest.TestCase):
    def test_absent_hit_exit_and_censor(self):
        whiffs=np.zeros((60,3),bool);whiffs[4,1:]=True
        cone=np.ones((60,3),bool);cone[10:,1]=False
        latency,censored=leave_latency(whiffs,cone)
        np.testing.assert_array_equal(latency,[0,6,60])
        np.testing.assert_array_equal(censored,[False,False,True])

    def test_brief_exit_does_not_count(self):
        whiffs=np.zeros((80,1),bool);whiffs[3,0]=True
        cone=np.ones((80,1),bool);cone[5:34]=False;cone[40:]=False
        latency,censored=leave_latency(whiffs,cone)
        np.testing.assert_array_equal(latency,[37])
        self.assertFalse(censored[0])


class I4ScoreBoundary(unittest.TestCase):
    @staticmethod
    def fixture():
        steps,runs=60,4
        return dict(steps=steps,good=np.zeros(runs,int),src=np.zeros((runs,2,2)),
                 H=np.ones((steps,runs),int),NAV=np.zeros((steps,runs),bool),
                 W=np.zeros((steps,runs,2),bool),POS=np.zeros((steps,runs,2)),
                 AT2=np.zeros((steps,runs,2),bool),C=np.zeros((steps,runs),bool),
                 TO=np.zeros((steps,runs),bool),EV=np.zeros((steps,runs),bool),
                 SINCE=np.zeros((steps,runs)),dwell=np.zeros((runs,2)),
                 first=np.full((runs,2),-1),contacts=np.zeros(runs))

    def test_w1_hold_diagnostics_are_reported_separately_from_scores(self):
        out=self.fixture();steps,runs=out['H'].shape
        changed=dict(out,H=np.full((steps,runs),-1))
        self.assertFalse(equal(M.l3_scores('h29','W1',out,steps),M.l3_scores('h29','W1',changed,steps)))
        left,excluded=i4_scores('h29','W1',out,steps)
        right,other=i4_scores('h29','W1',changed,steps)
        self.assertTrue(equal(left,right))
        self.assertEqual(set(excluded),set(I4_W1_HOLD_KEYS))
        self.assertFalse(equal(excluded,other))

    def test_w1_trajectory_score_change_still_fails(self):
        out=self.fixture();steps=out['steps']
        changed=dict(out,C=out['C'].copy(),contacts=out['contacts'].copy())
        changed['C'][0,0]=True;changed['contacts'][0]=1.
        left,_=i4_scores('h29','W1',out,steps)
        right,_=i4_scores('h29','W1',changed,steps)
        self.assertFalse(equal(left,right))


if __name__=='__main__':unittest.main()
