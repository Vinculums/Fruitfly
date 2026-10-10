"""Pure DEV authorization/durability fixtures; no controller or RNG is loaded."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import measure_h17_run3_dev as D
M=D.M


def put(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(D.canonical(obj)+b'\n')


class Fixture:
    def __init__(self,root):
        self.root=root;self.native_read=M.read
        self.config=self.native_read(ROOT/M.CONFIG)
        self.roles=self.native_read(ROOT/M.REGISTRATION)['stages']['bench']
        self.prov=self.native_read(ROOT/D.PRIOR/'verification.json')['provenance']
        self.main=self.native_read(ROOT/M.PINS)
        self.main['files_sha256_alpha']={'immutable-original.py':D.digest(b'immutable')}
        self.main['source_closure_sha256_alpha']=self.prov['source_closure_sha256_alpha']
        put(root/M.PINS,self.main)
        put(root/M.SCHEMA,{'metadata_keysets':{'claim':self.native_read(ROOT/M.SCHEMA)['metadata_keysets']['claim']}})
        gates={D.H.namespace(c,a):dict(complete=True,passed=True,rows=400,steps=600) for c in D.H.CONDITIONS for a in D.H.ARMS}
        clauses=copy.deepcopy(self.native_read(ROOT/D.PRIOR/'metrics.json')['clauses'])
        identity,metrics=M.metadata('bench',False,400,self.prov)
        raw=root/D.PRIOR/'raw.npz.ap';raw.parent.mkdir(parents=True);raw.write_bytes(b'deterministic fixture archive')
        rawsha=M.file_digest(raw)
        identity.update(complete=True,passed=True,gates=gates,raw_arrays={'sha256_alpha':rawsha})
        metrics.update(complete=True,clauses=clauses,verdict='PASS')
        verification=dict(format='h17-run3-verification-v3',date=M.DATE,stage='bench',complete=True,passed=True,smoke=False,
            provenance=self.prov,raw_sha256_alpha=rawsha,checked_arrays=0,gates=gates,clauses=clauses,verdict='PASS',first_failure=None)
        self.claim=root/M.REGISTRY/(D.digest(D.canonical(self.config['bench']))+'.json')
        identity['claim']=self.claim.relative_to(root).as_posix()
        for name,obj in [('identity.json',identity),('metrics.json',metrics),('verification.json',verification)]:put(root/D.PRIOR/name,obj)
        parent=dict(complete=True,passed=True,smoke=False,stage='bench',rows=400,steps=600,first_failure=None,
            source_closure_sha256_alpha=self.main['source_closure_sha256_alpha'],raw_sha256_alpha=rawsha,
            verification_sha256_alpha=M.file_digest(root/D.PRIOR/'verification.json'),rng_created=False,draws=0,clauses=clauses,verdict='PASS')
        put(root/D.PRIOR/'parent_recomputation.json',parent)
        for name in D.FILES:
            path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(('fixture '+name).encode())
        self.pins=dict(format='h17-run3-dev-pins-v1',date=M.DATE,complete=True,decision=D.DECISION,stage='dev',
            MAIN_pins_sha256_alpha=M.file_digest(root/M.PINS),source_closure_sha256_alpha=self.main['source_closure_sha256_alpha'],
            files_sha256_alpha={name:M.file_digest(root/name) for name in D.FILES},stage_closure_sha256_alpha=None,
            prior_artifacts_sha256_alpha={key+'_sha256_alpha':M.file_digest(root/D.PRIOR/name) for key,name in D.ARTIFACTS.items()})
        self.gate=dict(complete=True,opened=True,stage='dev',decision=D.DECISION,owner_instruction='approved DEV fixture',
            source_closure_sha256_alpha=self.main['source_closure_sha256_alpha'],prior_verification_sha256_alpha=None,stage_pins_sha256_alpha=None)
        self.refresh()

    def read(self,path):
        path=Path(path)
        if path==self.root/M.CONFIG:return self.config
        if path==self.root/M.REGISTRATION:return {'stages':{'bench':self.roles}}
        return self.native_read(path)

    def refresh(self):
        hashes=self.pins['prior_artifacts_sha256_alpha']
        hashes.update({key+'_sha256_alpha':M.file_digest(self.root/D.PRIOR/name) for key,name in D.ARTIFACTS.items()})
        claim={k:v for k,v in self.prov.items() if k!='runtime'}
        claim.update(format='h17-run3-claim-v3',date=M.DATE,complete=True,stage='bench',
            pair_sha256_alpha=D.digest(D.canonical(self.config['bench'])),role_digests={k:D.digest(D.canonical(v)) for k,v in self.roles.items()},
            H0_sha256_alpha=self.main['h0']['verification_sha256_alpha'],
            output_path_sha256_alpha=D.digest(str((self.root/D.PRIOR).resolve()).encode()),
            prerequisite_verification_sha256_alpha=self.main['h0']['verification_sha256_alpha'],
            rule='exclusive pair-only claim before any stage generator; failure consumes claim',
            result=D.canonical(dict(complete=True,status='PASS',identity_sha256_alpha=hashes['identity_sha256_alpha'],
                metrics_sha256_alpha=hashes['metrics_sha256_alpha'],raw_sha256_alpha=hashes['raw_sha256_alpha'])).hex().translate(D.H.AP))
        put(self.claim,claim)
        self.pins['stage_closure_sha256_alpha']=D.stage_closure(self.pins);put(self.root/D.PINS,self.pins)
        self.gate['prior_verification_sha256_alpha']=hashes['verification_sha256_alpha']
        self.gate['stage_pins_sha256_alpha']=M.file_digest(self.root/D.PINS);put(self.root/D.OPENING,self.gate)

    def mutate_receipt(self,name,fn):
        path=self.root/D.PRIOR/name;obj=self.native_read(path);fn(obj);put(path,obj);self.refresh()

    def patches(self):
        return patch.object(M,'preflight',return_value=(self.main,self.config,self.prov)),patch.object(M,'read',side_effect=self.read)


class DevPreflight(unittest.TestCase):
    def test_actual_grammar_and_unchanged_common_check(self):
        with tempfile.TemporaryDirectory() as directory:
            f=Fixture(Path(directory));common,reader=f.patches()
            with common as guard,reader:
                main,config,prov,control=D.preflight(f.root)
                guard.assert_called_once_with(f.root,False,'bench')
                self.assertEqual(prov,f.prov);self.assertEqual(control['stage_pins_sha256_alpha'],M.file_digest(f.root/D.PINS))
                self.assertEqual(main,f.main);self.assertEqual(config,f.config)

    def test_gate_corruption_rejected(self):
        mutations=[('opened',False),('complete',False),('stage','eval'),('decision','unapproved'),
            ('owner_instruction',' '),('source_closure_sha256_alpha','wrong'),('prior_verification_sha256_alpha','wrong'),('stage_pins_sha256_alpha','wrong')]
        for key,value in mutations:
            with self.subTest(key=key),tempfile.TemporaryDirectory() as directory:
                f=Fixture(Path(directory));f.gate[key]=value;put(f.root/D.OPENING,f.gate)
                common,reader=f.patches()
                with common,reader,self.assertRaises(D.EvidenceError):D.preflight(f.root)

    def test_stage_source_mutation_or_incomplete_inventory(self):
        for mutation in ('bytes','inventory','closure','MAIN'):
            with self.subTest(mutation=mutation),tempfile.TemporaryDirectory() as directory:
                f=Fixture(Path(directory))
                if mutation=='bytes':(f.root/D.FILES[0]).write_bytes(b'changed')
                elif mutation=='inventory':f.pins['files_sha256_alpha'].pop(D.FILES[0])
                elif mutation=='closure':f.pins['stage_closure_sha256_alpha']='wrong'
                else:f.pins['MAIN_pins_sha256_alpha']='wrong'
                if mutation!='bytes':put(f.root/D.PINS,f.pins);f.gate['stage_pins_sha256_alpha']=M.file_digest(f.root/D.PINS);put(f.root/D.OPENING,f.gate)
                common,reader=f.patches()
                with common,reader,self.assertRaises(D.EvidenceError):D.preflight(f.root)

    def test_prior_raw_byte_mutation_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            f=Fixture(Path(directory));(f.root/D.PRIOR/'raw.npz.ap').write_bytes(b'changed')
            common,reader=f.patches()
            with common,reader,self.assertRaises(D.EvidenceError):D.preflight(f.root)

    def test_prior_semantic_failures_despite_matching_hashes(self):
        mutations=[('identity.json',lambda x:x.update(smoke=True)),
            ('identity.json',lambda x:x['gates'].pop(next(iter(x['gates'])))),
            ('identity.json',lambda x:x['provenance'].update(execution_pins_sha256_alpha='wrong')),
            ('metrics.json',lambda x:x.update(verdict='FAIL')),
            ('verification.json',lambda x:x['clauses']['C0_E'].update(status='FAIL')),
            ('parent_recomputation.json',lambda x:x.update(rng_created=True)),
            ('parent_recomputation.json',lambda x:x.update(draws=True)),
            ('parent_recomputation.json',lambda x:x.update(verification_sha256_alpha='wrong')),
            ('parent_recomputation.json',lambda x:x.update(raw_sha256_alpha='wrong'))]
        for name,fn in mutations:
            with self.subTest(name=name,fn=fn),tempfile.TemporaryDirectory() as directory:
                f=Fixture(Path(directory));f.mutate_receipt(name,fn);common,reader=f.patches()
                with common,reader,self.assertRaises(D.EvidenceError):D.preflight(f.root)

    def test_prior_claim_tampering_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            f=Fixture(Path(directory));claim=f.native_read(f.claim);claim['complete']=False;put(f.claim,claim)
            common,reader=f.patches()
            with common,reader,self.assertRaises(D.EvidenceError):D.preflight(f.root)


class DevDurability(unittest.TestCase):
    def test_preflight_rejection_precedes_claim_and_runtime(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);out=root/D.OUTPUT
            with patch.object(D,'ROOT',root),patch.object(D,'preflight',side_effect=D.EvidenceError('fixture/denied')),patch.object(D,'claim_pair') as claim,patch.object(D,'collect') as collect:
                with self.assertRaises(D.EvidenceError):D.main(['--output',str(out)])
            claim.assert_not_called();collect.assert_not_called();self.assertFalse(out.exists())

    def test_exclusive_pair_claim_duplicate_output_independent(self):
        with tempfile.TemporaryDirectory() as directory:
            f=Fixture(Path(directory));common,reader=f.patches()
            with common,reader,patch.object(M.R,'p5'):
                pins,config,prov,control=D.preflight(f.root)
                path,claim=D.claim_pair(config,prov,f.root/'first',pins,control,f.root)
                self.assertEqual(claim['prerequisite_verification_sha256_alpha'],f.gate['prior_verification_sha256_alpha'])
                self.assertEqual(claim['H0_sha256_alpha'],pins['h0']['verification_sha256_alpha'])
                with self.assertRaises(D.EvidenceError):D.claim_pair(config,prov,f.root/'second',pins,control,f.root)
                self.assertTrue(path.exists())

    def test_control_drift_denied_before_exclusive_create(self):
        with tempfile.TemporaryDirectory() as directory:
            f=Fixture(Path(directory));common,reader=f.patches()
            with common,reader:
                pins,config,prov,control=D.preflight(f.root)
                f.gate['owner_instruction']='changed after preflight';put(f.root/D.OPENING,f.gate)
                with patch.object(M,'write_json') as writer,self.assertRaises(D.EvidenceError):D.claim_pair(config,prov,f.root/'out',pins,control,f.root)
                writer.assert_not_called()

    def test_exclusive_fsync_failure_keeps_consumed_claim_and_sidecar(self):
        with tempfile.TemporaryDirectory() as directory:
            f=Fixture(Path(directory));common,reader=f.patches();native=M.write_json
            def fault(path,obj,root=M.ROOT,exclusive=False):
                result=native(path,obj,root,exclusive)
                if exclusive:raise OSError('fixture fsync fault')
                return result
            with common,reader,patch.object(M.R,'p5'):
                pins,config,prov,control=D.preflight(f.root)
                with patch.object(M,'write_json',side_effect=fault),self.assertRaises(D.EvidenceError):D.claim_pair(config,prov,f.root/'out',pins,control,f.root)
                sidecars=list((f.root/M.REGISTRY).glob('*.failure.json'));self.assertEqual(len(sidecars),1)
                self.assertEqual(f.native_read(sidecars[0])['first_failure']['phase'],'claim')

    def test_binding_failure_stops_runtime_and_preserves_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            f=Fixture(Path(directory));common,reader=f.patches();native=M.write_json
            def fault(path,obj,root=M.ROOT,exclusive=False):
                if Path(path).name=='stage_binding.json':raise OSError('fixture binding failure')
                return native(path,obj,root,exclusive)
            with common,reader,patch.object(D,'ROOT',f.root),patch.object(M.R,'p5'),patch.object(M,'write_json',side_effect=fault),patch.object(D,'collect') as collect:
                self.assertEqual(D.main(['--output',str(f.root/D.OUTPUT)]),1)
                collect.assert_not_called()
            sidecars=list((f.root/M.REGISTRY).glob('*.failure.json'));self.assertEqual(len(sidecars),1)
            self.assertFalse(f.native_read(sidecars[0])['complete'])

    def completed_statistical_verdict(self,verdict):
        with tempfile.TemporaryDirectory() as directory:
            f=Fixture(Path(directory));common,reader=f.patches();out=f.root/D.OUTPUT
            class Store:
                def seal(self,receipt):
                    (out/'raw.npz.ap').write_bytes(b'synthetic completed evidence');return {'sha256_alpha':M.file_digest(out/'raw.npz.ap')}
            def collect(path,receipt,metrics,config):
                binding=f.native_read(path/'stage_binding.json')
                self.assertEqual(binding['format'],'h17-run3-dev-stage-binding-v3')
                self.assertTrue((f.root/binding['claim_path']).is_file())
                metrics.update(verdict=verdict,clauses={'synthetic':{'status':'FAIL' if verdict=='NOT_SHOWN' else 'INCONCLUSIVE'}});return Store()
            with common,reader,patch.object(D,'ROOT',f.root),patch.object(M.R,'p5'),patch.object(D,'collect',side_effect=collect):
                self.assertEqual(D.main(['--output',str(out)]),0)
            self.assertEqual(f.native_read(out/'metrics.json')['verdict'],verdict)
            self.assertNotIn('operation_verdict',f.native_read(out/'metrics.json'))
            pairkey=D.digest(D.canonical(f.config['dev']));claim=f.native_read(f.root/M.REGISTRY/(pairkey+'.json'))
            self.assertTrue(claim['complete']);self.assertEqual(claim['result'],D.canonical(dict(complete=True,status=verdict,
                identity_sha256_alpha=M.file_digest(out/'identity.json'),metrics_sha256_alpha=M.file_digest(out/'metrics.json'),
                raw_sha256_alpha=M.file_digest(out/'raw.npz.ap'))).hex().translate(D.H.AP))

    def test_dev_statistical_failure_is_saved_without_operation_pass(self):
        self.completed_statistical_verdict('NOT_SHOWN')

    def test_dev_inconclusive_is_saved_without_operation_pass(self):
        self.completed_statistical_verdict('INCONCLUSIVE/NOT_SHOWN')

    def test_changed_consumed_claim_cannot_be_overwritten_as_terminal_success(self):
        for mutation in ('field','truncate','whitespace'):
            with self.subTest(mutation=mutation),tempfile.TemporaryDirectory() as directory:
                f=Fixture(Path(directory));common,reader=f.patches();out=f.root/D.OUTPUT
                class Store:
                    def seal(self,receipt):
                        (out/'raw.npz.ap').write_bytes(b'synthetic evidence');return {'sha256_alpha':M.file_digest(out/'raw.npz.ap')}
                def collect(path,receipt,metrics,config):
                    claim=f.root/receipt['claim']
                    if mutation=='field':
                        obj=f.native_read(claim);obj['complete']=True;put(claim,obj)
                    elif mutation=='truncate':claim.write_bytes(b'{')
                    else:claim.write_bytes(claim.read_bytes()+b' ')
                    metrics['verdict']='PASS';return Store()
                with common,reader,patch.object(D,'ROOT',f.root),patch.object(M.R,'p5'),patch.object(D,'collect',side_effect=collect) as runtime:
                    self.assertEqual(D.main(['--output',str(out)]),1);self.assertEqual(runtime.call_count,1)
                pairkey=D.digest(D.canonical(f.config['dev']));claimpath=f.root/M.REGISTRY/(pairkey+'.json')
                terminal=f.native_read(claimpath);self.assertFalse(terminal['complete'])
                sidecar=f.native_read(claimpath.with_suffix('.failure.json'))
                self.assertEqual(sidecar['first_failure']['field'],'claim/exclusive header changed')
                self.assertEqual(sidecar['first_failure']['phase'],'claim')
                self.assertFalse(f.native_read(out/'identity.json')['complete'])


if __name__=='__main__':unittest.main()
