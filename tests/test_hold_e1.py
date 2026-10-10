"""E1 law, durable guards and passive wiring; spent smoke aliases only."""
from pathlib import Path
import sys
import tempfile
from contextlib import contextmanager
import shutil
import uuid
import types
import unittest
from unittest import mock

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import replay_hold_e1 as e1
import numpy as np


@contextmanager
def scratch():
    # pathlib's ordinary inherited workspace ACL; Windows tempfile's restrictive
    # mode creates inaccessible child directories in this managed environment.
    base=Path(__file__).resolve().parent
    path=base/('.hold_e1_test_'+uuid.uuid4().hex.translate(e1.AP))
    path.mkdir()
    try:yield str(path)
    finally:
        resolved=path.resolve()
        if not resolved.is_relative_to(base):raise RuntimeError('scratch cleanup escaped tests')
        shutil.rmtree(resolved)


class E1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.passive, cls.verifier, plume = e1.initialize()
        cls.plume=staticmethod(plume)

    def test_strict_cone_and_near_boundaries(self):
        # Source origin; points isolate strict along/cross/cone/near rules.
        pos=np.array([[10.,0.],[25.,0.],[10.,4.],[0.,3.],[-2.,0.],[-3.,0.]])
        w=types.SimpleNamespace(R=len(pos),src=np.zeros((len(pos),2,2)),pos=pos,p_hit=.3)
        got=self.plume(w,np.zeros(len(pos),int))
        expected=np.array([.3*np.exp(-10/12),0.,0.,0.,.3,0.])
        np.testing.assert_array_equal(got,expected)

    def test_D_draw_consumes_all_rows_at_zero_probability(self):
        class Recorded:
            def __init__(self):self.calls=[]
            def random(self,size):self.calls.append(size);return np.array([.01,.25,.8])
        rng=Recorded(); whiff,uniform=e1.d_draw(rng,np.array([0.,.3,0.]),3)
        self.assertEqual(rng.calls,[3])
        np.testing.assert_array_equal(whiff,[False,True,False])
        np.testing.assert_array_equal(uniform,[.01,.25,.8])

    def test_claim_pair_independent_of_output(self):
        with scratch() as directory:
            root=Path(directory)
            # Spent identities only: this test constructs no generator.
            claim=e1.claim_screen((5,6),{},root/'first',root)
            self.assertTrue(claim.exists())
            for checker in (e1.M.ph33,e1.M.ph35):
                self.assertTrue(all(number>=1000 for number in checker.seed_numbers()))
                self.assertFalse(any(self.verifier.count_number(claim.read_bytes(),number) for number in checker.seed_numbers()))
            with self.assertRaises(FileExistsError): e1.claim_screen((5,6),{},root/'other',root)
            self.assertTrue(claim.exists())

    def test_incomplete_guard_precedes_any_generator(self):
        with scratch() as directory:
            root=Path(directory);(root/'config').mkdir()
            (root/e1.PINS).write_text('{"complete":false}')
            with mock.patch.object(e1.np.random,'default_rng',side_effect=AssertionError('generator forbidden')):
                with self.assertRaisesRegex(RuntimeError,'pins incomplete'):e1.full_guard(root)
            self.assertFalse((root/'experiments/hold/hold_e1_registry').exists())

    def test_post_claim_startup_failure_keeps_first_receipt(self):
        with scratch() as directory:
            root=Path(directory);claim=e1.claim_screen((5,6),{},root/'out',root)
            e1.failure_receipt(root/'out',dict(provenance={}),RuntimeError('synthetic startup failure'),None,claim)
            self.assertTrue(claim.exists())
            emergency=e1.read(claim.with_suffix('.failure.json'))
            self.assertFalse(emergency['complete'])
            text=bytes.fromhex(emergency['first_failure_utf8_hex_alpha'].translate(e1.HEX)).decode()
            self.assertEqual(text,'RuntimeError: synthetic startup failure')

    def test_source_mutation_rejected_before_generator(self):
        with scratch() as directory:
            root=Path(directory);(root/'config').mkdir();source=root/'one.py';source.write_text('old')
            pins=dict(complete=True,runtime=dict(python='3.13.12',numpy='2.5.3',threads=1),files_sha256_alpha={'one.py':e1.digest(source.read_bytes())})
            import json
            (root/e1.PINS).write_text(json.dumps(pins));source.write_text('changed')
            with mock.patch.object(e1,'required_pin_files',return_value={'one.py'}),mock.patch.object(e1.np.random,'default_rng',side_effect=AssertionError('generator forbidden')):
                with self.assertRaisesRegex(RuntimeError,'pin mismatch'):e1.full_guard(root)

    def test_lossless_digit_free_array_evidence(self):
        with scratch() as directory:
            path=Path(directory)/'raw.npz.ap'
            original={'float':np.array([[1.25,-2.5]]),'bool':np.array([True,False])}
            receipt=e1.save_arrays(path,original)
            self.assertTrue(set(path.read_text())<=set('abcdefghijklmnop'))
            self.assertEqual(receipt['sha256_alpha'],e1.digest(path.read_bytes()))
            with e1.decode_arrays(path) as restored:
                for key in original:np.testing.assert_array_equal(restored[key],original[key])

    def test_passive_projection_wiring_without_world_simulation(self):
        # A prescribed sensory schedule in an immobile world checks external
        # tap wiring. Both streams are the explicitly spent identity aliases.
        seeds=e1.M.seeds_of('h28',True)
        a=self.passive(4,np.random.default_rng(seeds[0]),np.tile([1.,0.,0.],(4,1)),nch=3,rng3=np.random.default_rng(seeds[1]))
        observer=e1.Observer([],[],passive=True);observer.attach(a)
        world=types.SimpleNamespace(pos=np.zeros((4,2)),head=np.zeros(4),rot=np.zeros(4))
        for t in range(20):
            x=np.zeros((4,3),bool);x[:,1]=t in (0,1,2,11);x[:,2]=t in (0,1,2)
            a.act(world,x,np.ones(4,bool));a.bump(np.zeros(4,bool))
        self.assertEqual(observer.projection_errors,[])
        self.assertEqual(len(observer.events),40)
        for sample in observer.samples:
            np.testing.assert_array_equal(sample['actual_hold'],sample['projections']['H']['identity'])
            np.testing.assert_array_equal(sample['instantaneous'],sample['projections']['R']['identity'])

    def test_h0_reference_phase_checkpoints(self):
        gate,records=e1.h0(self.passive,self.plume)
        self.assertTrue(gate['passed'],gate.get('first_mismatch'))
        audits=[record[3] for record in records]
        self.assertEqual(len(audits[0]['creation']),11)
        self.assertEqual(audits[0]['construction'],audits[1]['construction'])
        self.assertEqual(audits[0]['phases'],audits[1]['phases'])


if __name__=='__main__':unittest.main()
