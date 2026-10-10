#!/usr/bin/env python3
"""One claimed W1Dp exposure screen; --smoke runs spent original-D H0 only.

--output names a NEW directory. Full execution requires immutable execution
pins and a complete fresh-seed registration receipt. No generator using the
screen pair can be constructed before the canonical durable claim succeeds.
Raw arrays are a compressed NPZ encoded with digit-free a-p hexadecimal.
Decode the file using decode_arrays(); no pickled objects are stored.
"""
import argparse
from contextlib import contextmanager
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
FINAL = 'notes/hold/2026-10-09-hold-e1-w1dp-design-v2.md'
CONFIG = 'config/hold-e1-seeds.json'
RECEIPT = 'experiments/hold/hold_e1_seed_registration.json'
PINS = 'config/hold-e1-execution-pins.json'
THREADS = ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
           'PH30_PROCS', 'PH32_PROCS', 'PH33_PROCS')
for key in THREADS: os.environ[key] = '1'
import numpy as np

AP = str.maketrans('0123456789abcdef', 'abcdefghijklmnop')
HEX = str.maketrans('abcdefghijklmnop', '0123456789abcdef')
COMMON = tuple('G N N_hi P R bb burst c cast_sign codes due_evidence due_timeout est flee_side known last_turn mb.C mb.K mb.R mb.beta mb.eta_d mb.eta_p mb.gated mb.parallel mb.rng mb.sparsity mb.tau_code mb.tau_reinf mb.tc mb.tr mb.w mb.wmax mb.wmin nav_hit nch present ring.J ring.R ring.Rmax ring.ang ring.c ring.n ring.noise ring.o ring.p ring.rng ring.s ring.sigma ring.tau ring.vgain ring.width rng sel.R sel.S sel.g sel.gsat sel.k sel.n sel.noise sel.pool_c sel.pool_p sel.rng sel.rng3 sel.s sel.tau sel.tau_g sel.theta sel.w_i silence since sustain t16 tgt up.P up.Rmax up.k up.n up.sig_n up.tau w2 zreset'.split())
LINEAGE_ONLY = tuple('abl acts belief cast differs differs8 filt fix hold_read hr keep15 keep16 n2S n2Z nav15 nav6 nav8 prev release rot_in rule scope top15 topr val yp'.split())
MEASUREMENT = {'hr', 'hold_projection'}
M = None


def digest(data): return hashlib.sha256(data).hexdigest().translate(AP)
def read(path): return json.loads(Path(path).read_text(encoding='utf-8'))


def runtime_guard():
    if not __debug__ or sys.flags.optimize: raise RuntimeError('assertions must be enabled')
    if sys.version.split()[0] != '3.13.12' or np.__version__ != '2.5.3':
        raise RuntimeError('registered Python/NumPy runtime mismatch')
    if any(os.environ.get(key) != '1' for key in THREADS):
        raise RuntimeError('registered thread/process pins mismatch')


def required_pin_files(root):
    return {FINAL, CONFIG, RECEIPT, 'tools/replay_hold_e1.py', 'tests/test_hold_e1.py',
            'tools/replay_hold_stage1.py', 'tools/verify_seed_scan_r2.py',
            'config/seed-scan-exceptions-r2.json', 'experiments/module/identity.json'} | {
            p.relative_to(root).as_posix() for p in (root/'src').glob('*.py')}


def full_guard(root=ROOT):
    """Read-only preflight, deliberately called before runtime imports/claims."""
    runtime_guard()
    pins = read(root/PINS)
    if pins.get('complete') is not True: raise RuntimeError('execution pins incomplete')
    if pins.get('runtime') != dict(python='3.13.12', numpy='2.5.3', threads=1):
        raise RuntimeError('execution runtime declaration mismatch')
    files = pins.get('files_sha256_alpha', {})
    if not required_pin_files(root) <= files.keys(): raise RuntimeError('execution source pin closure incomplete')
    for name, expected in files.items():
        target = (root/name).resolve()
        if not target.is_relative_to(root.resolve()) or digest(target.read_bytes()) != expected:
            raise RuntimeError('execution source/registration pin mismatch: '+name)
    cfg, receipt = read(root/CONFIG), read(root/RECEIPT)
    pair = cfg.get('screen')
    if not isinstance(pair, list) or len(pair) != 2 or any(type(s) is not int or s < 0 for s in pair) or pair[0] == pair[1]:
        raise RuntimeError('invalid canonical screen pair')
    if receipt.get('complete') is not True or receipt.get('repository_scan', {}).get('passed') is not True or receipt.get('graph_scan', {}).get('passed') is not True:
        raise RuntimeError('seed registration scans incomplete')
    expected_numbers = [pair[0],pair[1],pair[0]+10_000,pair[0]+30_000,pair[1]+20_000,pair[1]+30_000]
    repo, graph = receipt['repository_scan'],receipt['graph_scan']
    queries = graph.get('queries',[])
    if (receipt.get('config') != CONFIG or receipt.get('role') != 'screen' or
        receipt.get('numbers') != expected_numbers or repo.get('numbers') != expected_numbers or
        repo.get('hits') != [] or repo.get('errors') != [] or repo.get('prior_stage2_roles_disjoint') is not True or
        [q.get('number') for q in queries] != expected_numbers or
        any(q.get('executed') is not True or q.get('literal_hit') is not False or q.get('error') is not None or q.get('keyword_rows') != 0 for q in queries) or
        receipt.get('runtime') != pins['runtime'] or receipt.get('simulation_performed') is not False):
        raise RuntimeError('seed base/derived scan receipt incomplete or mismatched')
    names = read(root/'experiments/module/identity.json')['B2']['L2']['names']
    if names != dict(common=list(COMMON), ref_only=list(LINEAGE_ONLY), cand_only=[]):
        raise RuntimeError('historical L2 contract changed')
    return pair, digest((root/PINS).read_bytes())


def require_h0(pin_hash, root=ROOT):
    """A current-pin completed canonical H0 receipt is required BEFORE claim."""
    directory=root/'experiments/hold/hold_e1_smoke'
    prior=read(directory/'identity.json')
    p=prior.get('provenance',{})
    if (prior.get('complete') is not True or prior.get('passed') is not True or
        prior.get('gates',{}).get('H0',{}).get('passed') is not True or
        p.get('execution_pins_sha256_alpha') != pin_hash or p.get('python') != '3.13.12' or
        p.get('numpy') != '2.5.3' or p.get('threads') != {k:'1' for k in THREADS} or p.get('smoke') is not True):
        raise RuntimeError('complete current-pin canonical H0 receipt required before claim')
    raw=prior.get('raw_arrays',{})
    target=(directory/raw.get('path','')).resolve()
    if not target.is_relative_to(directory.resolve()) or not target.is_file() or digest(target.read_bytes()) != raw.get('sha256_alpha'):
        raise RuntimeError('prior H0 raw evidence hash mismatch')
    if not raw.get('arrays'):raise RuntimeError('prior H0 per-array evidence receipt incomplete')


def claim_screen(pair, provenance, output, root=ROOT):
    """Exclusive pair key independent of config formatting and output path."""
    key = digest(json.dumps(list(pair), separators=(',', ':')).encode('ascii'))
    registry = root/'experiments/hold/hold_e1_registry'
    registry.mkdir(parents=True, exist_ok=True)
    path = registry/(key+'.claim')
    payload=(json.dumps(dict(screen_pair_sha256_alpha=key,
              provenance_sha256_alpha=digest(json.dumps(provenance,sort_keys=True).encode()),
              execution_pins_sha256_alpha=provenance.get('execution_pins_sha256_alpha'),
              output_path_sha256_alpha=digest(str(Path(output).resolve()).encode()),complete=False,
              policy='One screen; failure retains claim; output path does not authorize another run.'),indent=2)+'\n').encode()
    # All variable numerical content is encoded before the exclusive write.
    # The only remaining digits are the fixed hash-label '256'; pinned legacy
    # registered seed tokens have at least four digits. Check before writing.
    if re.search(rb'\d{4,}',payload):raise RuntimeError('P5 claim contains numerical content; no claim written')
    with path.open('xb') as target:
        target.write(payload); target.flush(); os.fsync(target.fileno())
    return path


def initialize():
    global M
    sys.path.insert(0, str(ROOT/'tools'))
    import replay_hold_stage1 as stage1
    M, passive, _, verifier = stage1.load_runtime()
    sys.path.insert(0, str(ROOT/'src'))
    from hold_d0_metrics import plume_probability
    return passive, verifier, plume_probability


def encode(value):
    if isinstance(value, np.ndarray): return value.tolist()
    if isinstance(value, np.generic): return value.item()
    if isinstance(value, bytes): return value.hex().translate(AP)
    raise TypeError(type(value).__name__)


def protected(data, verifier):
    if any(verifier.count_number(data, number) for checker in (M.ph33, M.ph35) for number in checker.seed_numbers()):
        raise RuntimeError('P5 collision; no output written; representation review required')


def write_json(path, value, verifier):
    data = (json.dumps(value, default=encode, indent=2, allow_nan=False)+'\n').encode()
    protected(data, verifier)
    temporary = path.with_suffix(path.suffix+'.tmp')
    with temporary.open('wb') as target:
        target.write(data); target.flush(); os.fsync(target.fileno())
    temporary.replace(path)


def save_arrays(path, arrays):
    buffer = io.BytesIO(); np.savez_compressed(buffer, **arrays)
    payload = buffer.getvalue().hex().translate(AP).encode('ascii')
    temporary = path.with_suffix(path.suffix+'.tmp')
    with temporary.open('wb') as target:
        target.write(payload); target.flush(); os.fsync(target.fileno())
    temporary.replace(path)
    manifest={key:dict(dtype=value.dtype.str,shape=list(value.shape),sha256_alpha=digest(np.ascontiguousarray(value).tobytes()))
              for key,value in arrays.items()}
    return dict(path=path.name, sha256_alpha=digest(payload), encoding='NPZ compressed; hex nibble a-p maps to 0-f', keys=sorted(arrays),arrays=manifest)


def decode_arrays(path):
    data = bytes.fromhex(Path(path).read_text(encoding='ascii').translate(HEX))
    return np.load(io.BytesIO(data), allow_pickle=False)


@contextmanager
def tracked_generators():
    original = np.random.default_rng
    created, creation = [], []
    def factory(*args, **kwargs):
        generator = original(*args, **kwargs)
        created.append(generator)
        creation.append(digest(M.blob(generator)))
        return generator
    np.random.default_rng = factory
    try: yield created, creation
    finally: np.random.default_rng = original


def states(generators): return [digest(M.blob(g)) for g in generators]


class Observer:
    """External snapshots only; no added agent fields or extra random draws."""
    def __init__(self, generators, creation, passive=False):
        self.generators, self.creation, self.passive = generators, creation, passive
        self.events, self.inputs, self.returns, self.rngs, self.samples = [], [], [], [], []
        self.projection_errors = []
    def attach(self, a):
        self.agent = a
        act, bump = a.act, a.bump
        def observed(w, x, on):
            previous = dict(held=a.held().copy(), since=a.since.copy(), silence=a.silence.copy(),
                            counter=a.c.copy(), upstream=a.up.P.copy(), position=w.pos.copy(),
                            heading=w.head.copy(), rotation=w.rot.copy())
            self.inputs.append(digest(b''.join(M.blob(z) for z in (x, on, w.head, w.rot))))
            result = act(w, x, on)
            self.returns.append(digest(b''.join(M.blob(z) for z in result)))
            h = result[1]; rows = np.arange(a.R); v = a.chan_valence()
            others = (a.up.P.sum(1, keepdims=True)-a.up.P)/2
            y = a.up.Rmax*a.up.P/(a.up.sig_n+a.up.P+a.up.k*others)
            y *= 1+a.G*np.maximum(v, 0)
            vh = v[rows, np.maximum(previous['held'], 0)]
            y *= ~((previous['held'] >= 0)[:, None] & (v >= 0) & (v < vh[:, None]))
            q = np.where(y.max(1) > .05, y.argmax(1), -1)
            sample = dict(**previous, whiffs=x.copy(), wind_on=on.copy(), actual_hold=h.copy(), instantaneous=q,
                          counter_post=a.c.copy(), upstream_post=a.up.P.copy(), circuit=a.sel.s.copy(),
                          circuit_pool=a.sel.S.copy(), known=v.copy(), est=a.est.copy(),
                          flee_side=a.flee_side.copy(), cast_sign=a.cast_sign.copy(),
                          silence_post=a.silence.copy(), since_post=a.since.copy(), nav=a.nav_hit.copy(),
                          tgt=a.tgt.copy(), turn=result[0].copy(), burst=a.burst.copy(),
                          bb=a.bb.copy(), w2=a.w2.copy(), timeout=a.due_timeout.copy(),
                          evidence=a.due_evidence.copy(), gated_y=y.copy())
            if self.passive:
                p = a.hold_projection
                sample['projections'] = {arm: {k: value.copy() for k, value in p[arm].items()} for arm in ('H', 'R')}
                sample['release'] = p['release'].copy()
                actual = dict(identity=h, presence=a.present, nav=a.nav_hit, since=a.since,
                              post_silence=a.silence, tgt=a.tgt,
                              clipped_turn=np.clip(M.fly.GAIN*M.fly.angdiff(a.tgt, a.est), -M.fly.MAXTURN, M.fly.MAXTURN))
                for key, value in actual.items():
                    if not M.beq(p['H'][key], value): self.projection_errors.append(dict(step=len(self.samples), field=key))
                if not M.beq(q, a.hr) or not M.beq(y, p['y']):
                    self.projection_errors.append(dict(step=len(self.samples), field='instantaneous/gated_y'))
            self.samples.append(sample); self.record(a, 'act')
            return result
        def observed_bump(mask):
            result = bump(mask); self.record(a, 'bump'); return result
        a.act, a.bump = observed, observed_bump
        return a
    def record(self, a, kind):
        state = M.walk(a)
        if self.passive:
            if not MEASUREMENT <= state.keys(): raise RuntimeError('missing passive observer attributes')
            state = {k: v for k, v in state.items() if k not in MEASUREMENT}
        self.events.append((kind, {key: hashlib.sha256(M.blob(value)).digest() for key, value in state.items()}))
        self.rngs.append(states(self.generators))


def d_draw(rng, probability, rows):
    """Unconditional independent uniform consumption, including p=0."""
    uniform = rng.random(rows)
    return uniform < probability, uniform


def run_world(values, seeds, kind, passive_type, plume, original_d=False, runs=400, steps=600):
    """ph33.run order preserved verbatim; only D comparison law changes."""
    m = M; ph = m.ph33
    with tracked_generators() as (generated, creation):
        w = m.ph22.Masked(runs, np.random.default_rng(seeds[0]), seeds[0]) if hasattr(m, 'ph22') else ph.ph22.Masked(runs, np.random.default_rng(seeds[0]), seeds[0])
        rows = np.arange(runs); g = w.good; neutral = 1-g
        w.pres, w.absent = neutral.copy(), g.copy()
        tw = ph.World7(runs, np.random.default_rng(seeds[0]), seeds[0])
        rngD = np.random.default_rng(seeds[0]+ph.D_OFF)
        kv = ph.ph32.kv_of(values, g, 3)
        observer = Observer(generated, creation, passive=kind == 'Passive')
        if kind == 'Lineage': a = ph.build('A16', runs, seeds[1], g, kv)
        else:
            rng = np.random.default_rng(seeds[1]); rng3 = np.random.default_rng(seeds[1]+ph.A3_OFF)
            factory = passive_type if kind == 'Passive' else m.fly.Fly
            a = factory(runs, rng, kv, nch=3, rng3=rng3)
        a.cast_sign = ph.cast_draw(seeds[1], runs)
        observer.attach(a)
        construction = states(generated)
        o = dict(world='W1', arm='Agent16 D on', cls=type(a).__name__, kind='A16', vals=tuple(values), kv=kv, d_on=True, nch=3,
                 good=g, cell=w.cell, plus_y=w.plus_y, src=w.src.copy(), steps=steps, start=w.pos.copy(), s0=a.sel.s.copy(),
                 H0=a.held(), draws_equal=True, rng_equal=True, viol=0, neg=0, **ph.blank16(steps, runs, 3))
        phases, d_uniform, p_records, raw_records = [], [], [], []
        for t in range(steps):
            tw.pos, tw.head = w.pos.copy(), w.head.copy()
            ps = w.pos.copy(); before = states(generated)
            base = w.sense(); after_sense = states(generated)
            on = w.wind_on(); after_wind = states(generated)
            probability = np.full(runs, ph.P_D) if original_d else plume(w, neutral)
            dw, uniform = d_draw(rngD, probability, runs); after_d = states(generated)
            tr = tw.sense()
            o['draws_equal'] &= bool(np.array_equal(tr, w.raw) and np.array_equal(on, tw.wind_on()) and
                                    np.array_equal(base[rows, neutral], tr[rows, neutral]) and not base[rows, g].any())
            after_twin = states(generated)
            x = np.concatenate([base, dw[:, None]], 1)
            turn, h = a.act(w, x, on)
            ph.record(o, t, a, h, x, turn, g); ph.record16(o, t, a)
            # Fly is outside Agent9's isinstance recording branch. Restore
            # precisely the historical counter/presence diagnostic wiring.
            if kind != 'Lineage':
                o['C2'][t] = a.c; o['P2'][t] = a.present; o['PRES'][t] = a.present[rows, g]
            o['W'][t, :, 2] = dw; o['CONE'][t] = ph.cone_of(w, ps)
            negm = o['VAL'][t] < 0; o['neg'] += int(negm.sum()); o['viol'] += int((negm & (a.tgt != a.flee_side)).sum())
            w.move(turn); a.bump(w.bumped)
            o['POS'][t] = w.pos; o['HEAD'][t] = w.head; o['AT2'][t] = w.at_source(); o['C'][t] = w.bumped
            phases.append(dict(before=before, sense=after_sense, wind=after_wind, D=after_d, twin=after_twin,
                               act=observer.rngs[-2], bump=observer.rngs[-1]))
            d_uniform.append(uniform); p_records.append(probability); raw_records.append(w.raw.copy())
        o['rng_equal'] = w.rng.bit_generator.state == tw.rng.bit_generator.state
        o['dwell'] = o['AT2'].sum(0).astype(float); o['contacts'] = o['C'].sum(0).astype(float)
        audit = dict(creation=creation, construction=construction, phases=phases, final=states(generated),
                     balance=np.array_equal(np.bincount(w.cell, minlength=4), np.full(4, runs//4)),
                     D_uniforms=np.stack(d_uniform), D_probabilities=np.stack(p_records), raw_whiffs=np.stack(raw_records))
    return o, observer, audit


@contextmanager
def reference_phases(generators):
    """Scoped read-only checkpoints around untouched ph33.run's world calls."""
    world,masked=M.ph33.World7,M.ph33.ph22.Masked
    original_masked,original_world,original_wind=masked.sense,world.sense,world.wind_on
    owned_sense,owned_wind='sense' in world.__dict__,'wind_on' in world.__dict__
    phases=[]
    def masked_sense(w):
        phases.append(dict(before=states(generators)))
        result=original_masked(w)
        phases[-1]['sense']=states(generators)
        return result
    def world_sense(w):
        if not isinstance(w,masked):phases[-1]['D']=states(generators)
        return original_world(w)
    def world_wind(w):
        result=original_wind(w)
        phases[-1]['wind' if isinstance(w,masked) else 'twin']=states(generators)
        return result
    masked.sense,world.sense,world.wind_on=masked_sense,world_sense,world_wind
    try:yield phases
    finally:
        masked.sense=original_masked
        if owned_sense:world.sense=original_world
        else:delattr(world,'sense')
        if owned_wind:world.wind_on=original_wind
        else:delattr(world,'wind_on')


def h0(passive, plume):
    seeds = M.seeds_of('h28', True); runs, steps = M.size_of('h28', True)
    with tracked_generators() as (generated, creation):
        observer = Observer(generated, creation)
        build = M.ph33.build
        def attached(*args, **kwargs): return observer.attach(build(*args, **kwargs))
        M.ph33.build = attached
        try:
            with reference_phases(generated) as phases:
                reference = M.ph33.run('W1', 'Agent16 D on', (1., 0., 0.), seeds, runs=runs, steps=steps)
        finally: M.ph33.build = build
        for t,phase in enumerate(phases):phase.update(act=observer.rngs[2*t],bump=observer.rngs[2*t+1])
        reference_audit = dict(creation=creation.copy(),construction=phases[0]['before'],phases=phases,final=states(generated))
    candidate, tap, audit = run_world((1., 0., 0.), seeds, 'Lineage', passive, plume, True, runs, steps)
    ignored = {'arm', 'cls', 'kind'}
    fields = {key: M.beq(reference[key], candidate.get(key)) for key in reference if key not in ignored}
    l2 = compare_states(observer, tap, lineage='same_lineage', steps=steps)
    generators = reference_audit == {k:audit[k] for k in reference_audit} and observer.rngs == tap.rngs
    passed = set(reference) == set(candidate) and all(fields.values()) and l2['passed'] and generators and reference['draws_equal'] and reference['rng_equal']
    gate = dict(passed=bool(passed), all_output_fields=fields, complete_output_keysets=set(reference)==set(candidate), L2=l2,
                all_generator_events_equal=generators, seeds='module_identity.seeds_of(h28, smoke=True)', rows=runs, steps=steps,
                ignored_label_metadata=sorted(ignored))
    gate['first_mismatch']=first_difference(reference,candidate,ignored=ignored) or l2['first'] or first_rng_difference(reference_audit,audit)
    return gate, [('H0/reference', reference, observer, reference_audit), ('H0/candidate', candidate, tap, audit)]


def compare_states(reference, candidate, lineage, steps):
    first = None; expected_ref = set(COMMON) | set(LINEAGE_ONLY) if lineage else set(COMMON)
    expected_cand = expected_ref if lineage == 'same_lineage' else set(COMMON)
    compared = sorted(expected_ref) if lineage == 'same_lineage' else COMMON
    if len(reference.events) != steps*2 or len(candidate.events) != steps*2:
        first = dict(field='event_count', step=None)
    for i, ((kr, r), (kc, c)) in enumerate(zip(reference.events, candidate.events)):
        if first is not None: break
        if kr != kc or set(r) != expected_ref or set(c) != expected_cand:
            first = dict(event=i, field='explicit_state_field_sets', ref_only=sorted(set(r)-expected_ref), ref_missing=sorted(expected_ref-set(r)),
                         cand_only=sorted(set(c)-expected_cand), cand_missing=sorted(expected_cand-set(c)))
            break
        for name in compared:
            if r[name] != c[name]: first = dict(event=i, field=name); break
    return dict(passed=first is None, first=first, events=min(len(reference.events), len(candidate.events)),
                names=dict(common=list(compared), ref_only=list(LINEAGE_ONLY) if lineage is True else [], cand_only=[]))


def first_difference(a,b,path='',ignored=frozenset()):
    if isinstance(a,dict) and isinstance(b,dict):
        if set(a)-ignored != set(b)-ignored:return dict(field=path,reason='keysets')
        for key in a:
            if key not in ignored:
                found=first_difference(a[key],b[key],path+'/'+str(key))
                if found:return found
        return None
    if M.beq(a,b):return None
    if isinstance(a,np.ndarray) and isinstance(b,np.ndarray):
        if a.shape != b.shape:return dict(field=path,reason='shape',reference_shape=list(a.shape),candidate_shape=list(b.shape))
        if a.dtype != b.dtype:return dict(field=path,reason='dtype',reference_dtype=a.dtype.str,candidate_dtype=b.dtype.str)
        where=np.argwhere(a!=b)
        return dict(field=path,reason='value',index=where[0].tolist() if len(where) else [],step=int(where[0,0]) if len(where) and where.shape[1] else None)
    return dict(field=path,reason='scalar_or_type')


def first_rng_difference(a,b):
    for key in ('creation','construction','phases','final'):
        if a.get(key)==b.get(key):continue
        if key=='phases':
            for step,(left,right) in enumerate(zip(a[key],b[key])):
                for checkpoint in ('before','sense','wind','D','twin','act','bump'):
                    if left.get(checkpoint)!=right.get(checkpoint):
                        l,r=left.get(checkpoint,[]),right.get(checkpoint,[])
                        idx=next((i for i,(x,y) in enumerate(zip(l,r)) if x!=y),None)
                        return dict(field='RNG',step=step,checkpoint=checkpoint,generator=idx)
        return dict(field='RNG',checkpoint=key,reason='state_or_count')
    return None


def pair_gate(ref, cand, steps, lineage=False):
    ro, rt, ra = ref; co, ct, ca = cand
    l1 = {key: M.beq(ro[key], co[key]) for key in M.L1B}
    l2 = compare_states(rt, ct, lineage, steps)
    rs, cs = M.l3_scores('h28', 'W1', ro, steps), M.l3_scores('h28', 'W1', co, steps)
    # module_identity's ph32 summary has only four navigation fields. FINAL
    # additionally carries the complete historical ph22/ph25 W1 diagnostics.
    rs['complete_w1_summary'], cs['complete_w1_summary'] = M.ph25.w1sum(ro), M.ph25.w1sum(co)
    l3 = {key: M.beq(rs[key], cs[key]) for key in rs}
    rng = rt.rngs == ct.rngs and ra['creation'] == ca['creation'] and ra['construction'] == ca['construction'] and ra['phases'] == ca['phases'] and ra['final'] == ca['final']
    inputs = rt.inputs == ct.inputs and rt.returns == ct.returns
    construction = all(o['draws_equal'] and o['rng_equal'] and a['balance'] for o, _, a in (ref, cand))
    complete = len(ct.samples) == steps and co['H'].shape == (steps, 400) and all(len(s['actual_hold']) == 400 for s in ct.samples)
    wiring = not ct.passive or np.array_equal(co['HR'], np.stack([s['instantaneous'] for s in ct.samples]))
    projection = not ct.projection_errors
    passed = all(l1.values()) and l2['passed'] and all(l3.values()) and rng and inputs and construction and complete and projection and wiring
    first=(first_difference({k:ro[k] for k in M.L1B},{k:co[k] for k in M.L1B}) or
           l2['first'] or first_difference(rs,cs,'L3') or first_rng_difference(ra,ca) or
           (ct.projection_errors[0] if ct.projection_errors else None))
    if not passed and first is None:
        for field,left,right in (('inputs',rt.inputs,ct.inputs),('returns',rt.returns,ct.returns)):
            if left!=right:
                first=dict(field=field,step=next((i for i,(x,y) in enumerate(zip(left,right)) if x!=y),None));break
        if first is None:first=dict(field='construction/sample/instantaneous_record_wiring',step=None)
    return dict(passed=bool(passed), L1=l1, L2=l2, L3=l3, all_rng_event_states_equal=rng,
                input_return_equal=inputs, construction_draws_balance=construction, complete_sample=complete,
                instantaneous_record_wiring=wiring,
                actual_projection_matches=projection, first_projection_error=ct.projection_errors[:1],
                first_mismatch=first)


def collect_raw(label, output, observer, audit, arrays):
    for key, value in output.items():
        if isinstance(value, np.ndarray): arrays[label+'/output/'+key] = value
    for key in observer.samples[0]:
        if key != 'projections': arrays[label+'/state/'+key] = np.stack([s[key] for s in observer.samples])
    if observer.passive:
        for arm in ('H', 'R'):
            for key in observer.samples[0]['projections'][arm]:
                arrays[label+'/projection/'+arm+'/'+key] = np.stack([s['projections'][arm][key] for s in observer.samples])
    for key in ('D_uniforms', 'D_probabilities', 'raw_whiffs'):
        if key in audit: arrays[label+'/draw/'+key] = audit[key]
    arrays[label+'/L2/event_kind'] = np.array([kind for kind, _ in observer.events])
    for key in observer.events[0][1]:
        arrays[label+'/L2/'+key] = np.array([event[key].hex().translate(AP) for _, event in observer.events])
    return dict(output_metadata={k:v for k,v in output.items() if not isinstance(v,np.ndarray)},
                audit={k:v for k,v in audit.items() if not isinstance(v,np.ndarray)},
                input_digests=observer.inputs, return_digests=observer.returns, rng_events=observer.rngs)


def projection_readings(label, output, observer, arrays):
    prefix = label+'/projection/'
    h = {k: arrays[prefix+'H/'+k] for k in observer.samples[0]['projections']['H']}
    r = {k: arrays[prefix+'R/'+k] for k in observer.samples[0]['projections']['R']}
    steps, rows = h['identity'].shape; index = np.arange(rows)[None, :]; time = np.arange(steps)[:, None]
    g = output['good'][None, :]; b = 1-g; x = arrays[label+'/state/whiffs']; c = arrays[label+'/state/counter_post']
    bb = arrays[label+'/state/bb']; burst = arrays[label+'/state/burst']
    bx, dx = x[time, index, b], x[:, :, 2]
    t1 = (c[time, index, g] >= M.fly.N_HI[3]) & (h['identity'] != g) & (r['identity'] != g)
    t2 = np.ones((steps, rows), bool)
    for p in (h, r):
        t2 &= p['presence'][time, index, b] & p['presence'][:, :, 2] & p['top'][time, index, b] & p['top'][:, :, 2]
    t3 = (bb[time, index, b] == bb[:, :, 2]) & (bb[:, :, 2] > M.fly.NEVER)
    t4 = (bx != dx) & ~burst[time, index, b] & ~burst[:, :, 2]
    whiffing = np.where(bx, b, 2); nonwhiffing = np.where(bx, 2, b)
    t5 = (((h['identity'] == nonwhiffing) & ((r['identity'] == whiffing) | (r['identity'] < 0))) |
          ((r['identity'] == nonwhiffing) & ((h['identity'] == whiffing) | (h['identity'] < 0)))) & (h['nav'] != r['nav'])
    route = t1 & t2 & t3 & t4 & t5; denominator = t1 & t2 & t3 & t4
    command = h['clipped_turn'] != r['clipped_turn']
    from replay_hold_stage1 import ORDER
    first = np.full((steps, rows), -1, int); first_downstream = first.copy()
    for n, key in enumerate(ORDER):
        different = (h[key] != r[key]).reshape(steps, rows, -1).any(2)
        arrays[label+'/mask/'+key] = different
        first[(first < 0) & different] = n
        if key != 'identity': first_downstream[(first_downstream < 0) & different] = n
    release = arrays[label+'/state/release']; adjacent = release.copy()
    adjacent[1:] |= release[:-1]; adjacent[:-1] |= release[1:]
    masks = dict(T1=t1,T1_noVcounter_both=c[time,index,g]>=M.fly.N_HI[3],
                 T1_read_neither_V=(h['identity']!=g)&(r['identity']!=g), T2=t2, T3=t3, T4=t4, T5=t5, T1_T4=denominator, T1_T5=route,
                 command=command, command_tied_route=command & route, command_outside_tied_route=command & ~route,
                 command_presence_difference=command & (h['presence'] != r['presence']).any(2),
                 command_presence_equal=command & (h['presence'] == r['presence']).all(2),
                 release_adjacent=adjacent, release_adjacent_command=command & adjacent,
                 boundary=output['C'], boundary_command=command & output['C'],
                 simultaneous_B_D_bursts=burst[time,index,b] & burst[:,:,2], raw_latest_burst_tie=t3,
                 raw_single_nonburst=t4)
    for key,value in masks.items(): arrays[label+'/route/'+key] = value
    lost = M.ph32.lost_t1(output)
    arrays[label+'/summary/lost'] = lost
    arrays[label+'/summary/command_counts_per_row'] = command.sum(0)
    arrays[label+'/summary/first_command_step'] = np.where(command.any(0), command.argmax(0), -1)
    arrays[label+'/summary/first_expression'] = first
    arrays[label+'/summary/first_downstream_expression'] = first_downstream
    def metric(mask): return dict(events=int(mask.sum()), rows=int(mask.any(0).sum()), denominator_row_steps=steps*rows, denominator_rows=rows)
    return dict(command_exposure=metric(command), lost_rows=int(lost.sum()),
                route={key:metric(value) for key,value in masks.items()},
                identity_split_denominator=int(denominator.sum()), f_id=None if not denominator.any() else float(route.sum()/denominator.sum()),
                first_expression_names=list(ORDER), lost_definition='no original-source whiff in last200 steps; D excluded')


def failure_receipt(output,receipt,error,verifier,claim):
    """Preserve the first post-claim failure even if runtime/output setup fails."""
    receipt.update(complete=False,passed=False,first_failure=type(error).__name__+': '+str(error))
    try:
        output.mkdir(parents=True,exist_ok=True)
        if verifier is not None:write_json(output/'identity.json',receipt,verifier)
        else:raise RuntimeError('runtime not ready for normal receipt')
        return
    except BaseException:
        # This emergency form has no digits and cannot collide with seed tokens.
        target=claim.with_suffix('.failure.json') if claim is not None else output.parent/'hold_e1_setup_failure.json'
        emergency=dict(complete=False,passed=False,failure_type=type(error).__name__,
                       first_failure_utf8_hex_alpha=(type(error).__name__+': '+str(error)).encode().hex().translate(AP),
                       encoding='UTF eight bytes as hex nibble a-p maps to zero-f',
                       execution_pins_sha256_alpha=receipt.get('provenance',{}).get('execution_pins_sha256_alpha'))
        payload=(json.dumps(emergency,indent=2)+'\n').encode()
        if re.search(rb'\d{4,}',payload):raise RuntimeError('emergency receipt contains numerical content')
        with target.open('xb') as dest:dest.write(payload);dest.flush();os.fsync(dest.fileno())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path); parser.add_argument('--smoke', action='store_true')
    args = parser.parse_args(); output = args.output.resolve()
    if output.exists(): raise RuntimeError('output directory must be new')
    runtime_guard()
    pair, pin_hash = full_guard()
    provenance = dict(python=sys.version.split()[0], numpy=np.__version__, platform=platform.platform(),
                      execution_pins_sha256_alpha=pin_hash, threads={k:os.environ[k] for k in THREADS}, smoke=args.smoke)
    claim=None
    if not args.smoke:
        require_h0(pin_hash)
        claim=claim_screen(pair, provenance, output)
    def guard():
        runtime_guard()
        if full_guard() != (pair,pin_hash): raise RuntimeError('execution provenance changed after prior gate')
    receipt = dict(complete=False, gates={}, provenance=provenance, raw_records={})
    arrays = {};verifier=None
    try:
        passive, verifier, plume = initialize()
        output.mkdir(parents=True)
        write_json(output/'identity.json', receipt, verifier)
        guard(); print('E1 H0 spent original-D known answer', flush=True)
        gate, runs = h0(passive, plume); guard(); receipt['gates']['H0'] = gate
        for label,o,t,a in runs: receipt['raw_records'][label] = collect_raw(label,o,t,a,arrays)
        if not gate['passed']: raise RuntimeError('H0 failed; no fresh generator constructed')
        write_json(output/'identity.json', receipt, verifier)
        if args.smoke:
            receipt.update(complete=True, passed=True, raw_arrays=save_arrays(output/'raw.npz.ap', arrays))
            write_json(output/'identity.json',receipt,verifier)
            print('H0 smoke passed; no fresh screen seed used.',flush=True); return 0
        saved = {}
        for condition,values in (('B4',(1.,0.,0.)),('B5',(1.,-1.,0.))):
            actual = []
            for kind in ('Lineage','Fly'):
                guard(); print('E1 '+condition+' '+kind+' identity/passivity',flush=True)
                result = run_world(values,pair,kind,passive,plume); guard(); actual.append(result)
                label=condition+'/'+kind
                receipt['raw_records'][label]=collect_raw(label,*result,arrays)
            gates=dict(lineage_to_fly=pair_gate(actual[0],actual[1],600,True))
            receipt['gates'][condition]=gates
            if not gates['lineage_to_fly']['passed']:raise RuntimeError(condition+' lineage identity gate failed')
            write_json(output/'identity.json',receipt,verifier)
            guard();print('E1 '+condition+' Passive passivity',flush=True)
            result=run_world(values,pair,'Passive',passive,plume);guard();actual.append(result)
            receipt['raw_records'][condition+'/Passive']=collect_raw(condition+'/Passive',*result,arrays)
            gates['fly_to_passive']=pair_gate(actual[1],actual[2],600)
            if not gates['fly_to_passive']['passed']:raise RuntimeError(condition+' passivity gate failed')
            saved[condition]=actual[2]; write_json(output/'identity.json',receipt,verifier)
        # No exposure aggregation is permitted until BOTH condition gates pass.
        guard()
        readings={condition:projection_readings(condition+'/Passive',result[0],result[1],arrays) for condition,result in saved.items()}
        x=dict(X1=True,X2=readings['B5']['command_exposure']['rows']>=1,
               X3=readings['B4']['command_exposure']['rows']>=40,X4=20<=readings['B4']['lost_rows']<=380)
        raw=save_arrays(output/'raw.npz.ap',arrays); guard()
        receipt.update(complete=True,passed=True,raw_arrays=raw)
        write_json(output/'identity.json',receipt,verifier)
        reached=readings['B4']['command_exposure']['rows']
        verdict=('READABLE FOR SEPARATE BENEFIT DESIGN' if all(x.values()) else
                 'BLOCKED: positive control did not expose a command branch' if not x['X2'] else
                 'UNREADABLE: loss-range criterion failed' if not x['X4'] else
                 'NOT REACHED IN THIS SAMPLE' if reached==0 else 'REACHED, BELOW REGISTERED SCREEN')
        exposure=dict(complete=True,provenance=provenance,readings=readings,screen=x,
                      raw_arrays=raw,verdict=verdict,
                      interpretation='same-state passive exposure; no free-running benefit or power finding')
        write_json(output/'exposure.json',exposure,verifier)
        print('E1 saved once; both identity gates passed; independent raw-evidence review remains.',flush=True)
        return 0
    except BaseException as error:
        if arrays:
            try:receipt['raw_arrays']=save_arrays(output/'partial_raw.npz.ap',arrays)
            except BaseException:pass
        failure_receipt(output,receipt,error,verifier,claim)
        raise


if __name__ == '__main__':
    try: sys.exit(main())
    except (RuntimeError,OSError,ValueError) as error:
        print('E1 stopped: '+str(error),file=sys.stderr);sys.exit(1)
