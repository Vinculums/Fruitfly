"""Deterministic archive comparisons; no RNG, trajectory or source activation."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
import copy
import hashlib
import importlib.util
from pathlib import Path
import sys
import unittest
import zipfile
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from h17_run3_recording import Archive as LiveArchive
from h17_run3_archive_candidate import Archive as CandidateArchive

ARCHIVED=ROOT/'experiments/h17/run3_H0_attempt1/sources/h17_run3_recording.py'
ORIGINAL_SHA_ALPHA='ncpgianhliihpijoabglmmnjbcmmgoneemgkffhnellnnmfjggbalkkohiadckcl'
raw=ARCHIVED.read_bytes()
actual=hashlib.sha256(raw).hexdigest().translate(str.maketrans('0123456789abcdef','abcdefghijklmnop'))
if actual!=ORIGINAL_SHA_ALPHA:raise RuntimeError('archived original recorder hash mismatch')
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('_h17_run3_archived_original',ARCHIVED)
original=importlib.util.module_from_spec(spec);spec.loader.exec_module(original)
FrozenArchive=original.Archive


class Capture:
    """Capture the final ZIP in memory instead of emitting an AP run artifact."""
    def finish(self):
        self.zip.close();self.temp.seek(0)
        with zipfile.ZipFile(self.temp,'r') as archive:
            result=dict(order=archive.namelist(),npy={name:archive.read(name) for name in archive.namelist()},
                arrays=copy.deepcopy(self.arrays),blobs=copy.deepcopy(self.blobs))
        self.temp.close();self.closed=True
        return result


class FrozenCapture(Capture,FrozenArchive):pass
class CandidateCapture(Capture,CandidateArchive):pass
class ActivatedCapture(Capture,LiveArchive):pass


class ReachabilityContract(unittest.TestCase):
    def compare(self,fixture):
        frozen=FrozenCapture('unused.ap');candidate=CandidateCapture('unused.ap');activated=ActivatedCapture('unused.ap')
        metadata_f,expected=fixture(frozen);metadata_c,expected_c=fixture(candidate);metadata_a,expected_a=fixture(activated)
        self.assertEqual(metadata_f,metadata_c);self.assertEqual(metadata_f,metadata_a)
        self.assertEqual(expected,expected_c);self.assertEqual(expected,expected_a)
        left=frozen.seal(metadata_f);right=candidate.seal(metadata_c);live=activated.seal(metadata_a)
        self.assertEqual(left,right);self.assertEqual(left,live)
        self.assertEqual(set(right['blobs']),expected)
        self.assertEqual(right['order'],[key+'.npy' for key in right['arrays']])
        return right

    def test_nested_maps_shared_native_and_signed_zero(self):
        def fixture(a):
            data=a.put(np.array([-0.,1.],dtype=np.float64));unused=a.put(np.ones(3))
            scalar=a.put(np.asarray(-0.,dtype=np.float64));mapping=a.map_refs({'native':data,'scalar':scalar})
            outer=a.put({'nested':mapping,'again':mapping})
            a.array('ordinary/POS',np.array([[-0.,0.]],dtype=np.float64))
            return {'root':outer},{data,scalar,mapping,outer}
        result=self.compare(fixture)
        self.assertEqual(list(result['arrays'])[-1],'ordinary/POS')

    def test_native_s64_transitive_tables(self):
        def fixture(a):
            data=a.put(np.array([False,True]));leaf=a.put({'value':data})
            timeline=a.put(np.asarray([leaf,leaf],dtype='S64'));outer=a.put({'timeline':timeline})
            a.put(np.arange(3,dtype=np.int64));return {'root':outer},{data,leaf,timeline,outer}
        self.compare(fixture)

    def test_attribute_hash_arrays_never_create_reference_edges(self):
        def fixture(a):
            orphan=a.put(np.array([4.5]));hashes=a.put(np.asarray([orphan],dtype='S64'))
            a.non_reference_blobarrays.add(hashes);outer=a.put({'attribute_hashes':hashes})
            a.array('ordinary/attribute_hashes',np.asarray([orphan],dtype='S64'))
            return {'root':outer},{hashes,outer}
        self.compare(fixture)

    def test_all_declared_nonblob_reference_suffixes(self):
        def fixture(a):
            keep=[]
            for suffix in ('state_timeline','world_timeline','input_timeline','return_timeline','base_return_timeline','rng_timeline','call_refs','checkpoints'):
                key=a.put({'suffix':suffix});keep.append(key);a.array('ordinary/'+suffix,np.asarray([key,key],dtype='S64'))
            a.put('unreferenced');return {},set(keep)
        self.compare(fixture)

    def test_empty_roots_keep_only_nonblob_payloads(self):
        def fixture(a):
            a.put(np.arange(5));a.array('ordinary/numeric',np.array([1,2],dtype=np.int64));return {},set()
        self.compare(fixture)

    def test_native_self_reference_and_repeated_metadata_are_finite(self):
        def fixture(a):
            key=a.put(np.array([1.],dtype=np.float64));return {'many':[key]*40,'tuple':(key,key)},{key}
        self.compare(fixture)

    def test_long_nested_reference_chain(self):
        def fixture(a):
            key=a.put(np.array([-0.],dtype=np.float64));keep={key}
            for i in range(40):key=a.put({'previous':key,'label':str(i)});keep.add(key)
            return {'root':key},keep
        self.compare(fixture)

    def test_metadata_and_timeline_duplicate_roots(self):
        def fixture(a):
            native=a.put(np.zeros((2,2)));scalar=a.put(7);outer=a.put({'left':native,'right':scalar})
            a.array('ordinary/state_timeline',np.asarray([[outer,native],[scalar,outer]],dtype='S64'))
            a.put({'orphan':True});return {'root':outer},{native,scalar,outer}
        self.compare(fixture)


if __name__=='__main__':unittest.main()
