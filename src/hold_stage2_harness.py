"""Scoped injections into the unchanged ph35/ph33 local simulation harnesses."""
from contextlib import contextmanager
import hashlib
import importlib
from pathlib import Path
import sys
import numpy as np
import ph35, ph33, ph24, ph30, ph32, fly
from hold_stage1_instrument import PassiveFly
from hold_stage2_arm import ReadOutFly

ROOT = Path(__file__).resolve().parents[1]
EXTRA = {'hr', 'hold_projection', 'hold_read'}
TRAJECTORY = ('POS', 'HEAD', 'NAV', 'SINCE', 'TURN', 'EST', 'TGT', 'W', 'AT2', 'C')
I4_W1_HOLD_KEYS = ('heldB', 'nothing', 'formed', 'released', 'end_to',
                   'end_ev', 'end_both', 'end_none', 'fh', 'heldB_end')


def identity_runtime():
    old = ph24.make, ph33.build, ph30.build
    arms = dict(ph33.ARMS)
    try:
        return importlib.import_module('module_identity')
    finally:
        ph24.make, ph33.build, ph30.build = old
        ph33.ARMS.clear(); ph33.ARMS.update(arms)


M = identity_runtime()


def equal(a, b):
    return M.beq(a, b)


def generator_states(a, w):
    states = {'world': repr(w.rng.bit_generator.state)}
    for name, value in M.walk(a).items():
        if isinstance(value, np.random.Generator):
            states[name] = repr(value.bit_generator.state)
    # rngD is local to ph33.run; each unconditional random(runs) call is
    # intercepted below in the scoped default_rng hook, not inferred from D.
    return states


class Observer:
    def __init__(self, state=True, projection=False):
        self.state = state
        self.projection = projection
        self.events = []
        self.records = []
        self.rngs = []

    def attach(self, a):
        self.agent = a
        act0, bump0 = a.act, a.bump
        def record_state(kind):
            if self.state:
                state = {k: v for k, v in M.walk(a).items() if k not in EXTRA}
                self.events.append((kind, {k: hashlib.sha256(M.blob(v)).digest()
                                          for k, v in state.items()}))
        def act(w, x, on):
            ps = w.pos.copy()
            result = act0(w, x, on)
            h = result[1]; rows = np.arange(a.R)
            hr = getattr(a, 'hr', h)
            hh = h if getattr(a, 'hold_read', True) else hr
            val = np.where(hh >= 0, a.known[rows, np.maximum(hh, 0)], 0.)
            valh = np.where(h >= 0, a.known[rows, np.maximum(h, 0)], 0.)
            negative = 1 - w.good
            da = ps[:, 0] - w.src[rows, negative, 0]
            dc = np.abs(ps[:, 1] - w.src[rows, negative, 1])
            cone = ((da > 0) & (da < ph32.LMAX) & (dc < ph32.W0 + ph32.SLOPE*da))
            cone |= np.linalg.norm(ps - w.src[rows, negative], axis=1) < 3.
            v = a.chan_valence(); hit = (hh >= 0) & x[rows, np.maximum(hh, 0)]
            vh = v[rows, np.maximum(hh, 0)]
            nav6 = hit | ((hh < 0) & (x & (v >= 0)).any(1))
            top8 = (v >= 0) & (v == v.max(1)[:, None])
            nav8 = np.where((hh >= 0) & ((vh == v.max(1)) | (vh < 0)), hit, (x & top8).any(1))
            rec = dict(HR=hr.copy(), VAL=val, VALH=valh, FLEE=a.flee_side.copy(),
                       NEG_CONE=cone, C2=a.c.copy(), P2=a.present.copy(),
                       PRES=a.present[rows, w.good].copy(), NAV6=nav6, NAV8=nav8,
                       DIFF8=a.nav_hit != nav8, TURN=result[0].copy(), EST=a.est.copy(),
                       CLIPPED=np.clip(fly.GAIN*fly.angdiff(a.tgt, a.est), -fly.MAXTURN, fly.MAXTURN))
            if self.projection:
                rec['PROJECTED_HR'] = a.hr.copy()
                rec['PROJECTED_TURN'] = a.hold_projection['R']['clipped_turn'].copy()
            self.records.append(rec)
            self.rngs.append(generator_states(a, w))
            record_state('act')
            return result
        def bump(mask):
            result = bump0(mask); record_state('bump'); return result
        a.act, a.bump = act, bump
        return a


@contextmanager
def injection(factory, observer):
    old = ph24.make, ph33.build, np.random.default_rng
    arms = dict(ph33.ARMS)
    generated = []
    def generator(*args, **kwargs):
        rng = old[2](*args, **kwargs)
        generated.append(rng)
        return rng
    def make(cls, runs, rng, G, known, gate=True, filt=True, release=True):
        if cls is M.CAND2:
            if not (G == fly.G_STAR and gate and filt and release):
                raise RuntimeError('unsupported injection')
            return observer.attach(factory(runs, rng, known, nch=2))
        return observer.attach(old[0](cls, runs, rng, G, known, gate, filt, release))
    def build(kind, runs, seed_a, good, kv):
        if kind == 'HOLD_STAGE2':
            rng = np.random.default_rng(seed_a)
            rng3 = np.random.default_rng(seed_a + ph32.A3_OFF)
            return observer.attach(factory(runs, rng, kv, nch=3, rng3=rng3))
        return observer.attach(old[1](kind, runs, seed_a, good, kv))
    # Each per-step generator state includes every generator constructed by
    # the harness: D, world/twin, cast, agent, third unit, and odour generators.
    act_record = observer.rngs
    class States(list):
        def append(self, state):
            state['all_constructed'] = [repr(g.bit_generator.state) for g in generated]
            super().append(state)
    observer.rngs = States(act_record)
    ph24.make, ph33.build, np.random.default_rng = make, build, generator
    ph33.ARMS['stage2 injected'] = ('HOLD_STAGE2', 3, True)
    try:
        yield
    finally:
        ph24.make, ph33.build, np.random.default_rng = old
        ph33.ARMS.clear(); ph33.ARMS.update(arms)


def run(rid, arm, seeds, runs=400, steps=600, state=True, reference=None):
    kind, world, values = M.ROWS[rid]
    if arm == 'Free':
        values = tuple(max(v, 0.) for v in values)
    factory = {'H': PassiveFly, 'R': ReadOutFly, 'Free': fly.Fly,
               'actual': lambda *a, **k: ReadOutFly(*a, read='actual', **k),
               'Fly': fly.Fly}[arm]
    if reference == 'A16two':
        def factory(runs, rng, known, nch=2):
            return ph33.Agent16(runs, rng, nch=2, N_hi=200,
                               P=ph32.P_PRIOR, G=fly.G_STAR, known=known,
                               rule=True, filt=True, scope='prior', release=True,
                               hold_read=arm != 'R')
    observer = Observer(state=state, projection=arm == 'H' and reference is None)
    with injection(factory, observer):
        if kind == 'h29':
            cls = ph35.Agent17 if reference == 'chain' else M.CAND2
            out = ph35.run(world, cls, values, seeds, runs=runs, steps=steps)
        else:
            name = ('hold-not-read D on' if arm == 'R' else 'Agent16 D on') if reference == 'chain' else 'stage2 injected'
            out = ph33.run(world, name, values, seeds, runs=runs, steps=steps)
    for key in observer.records[0]:
        out[key] = np.stack([r[key] for r in observer.records])
    out['kv'] = observer.agent.known.copy()
    out['stage2_arm'] = arm
    return out, observer


def comparison(a, b, fields):
    result = {k: equal(a[k], b[k]) for k in fields}
    first = None
    for key in fields:
        if not result[key]:
            index = np.argwhere(a[key] != b[key])[0].tolist()
            first = dict(field=key, index=index)
            break
    return dict(passed=all(result.values()), fields=result, first=first)


def first_difference(a, b, fields):
    shape = a['H'].shape
    mask = np.zeros(shape, bool)
    for key in fields:
        delta = a[key] != b[key]
        mask |= delta.reshape(*shape, -1).any(2)
    return np.where(mask.any(0), mask.argmax(0), -1)


def i4_scores(kind, world, out, steps):
    """I4 trajectory scores; W1's historical summary also contains hold data.

    Those ten hold diagnostics are returned separately and are never an I4
    score gate. The full historical scores remain in the other identities.
    """
    scores=M.l3_scores(kind,world,out,steps)
    excluded={}
    if world=='W1':
        summary=scores['w1sum'].copy()
        excluded={key:summary.pop(key) for key in I4_W1_HOLD_KEYS}
        scores['w1sum']=summary
    return scores,excluded


def identities(runs=400, steps=600):
    gates = {}
    def check(name, gate):
        gates[name] = gate
        if not gate['passed']:
            raise IdentityFailure(name, gates)
    for rid in ('A1','A2','A3','A4','A5','A6','B1','B2','B3'):
        kind, world, _ = M.ROWS[rid]
        seeds = M.seeds_of(kind, False)
        base, tb = run(rid, 'Fly', seeds, runs, steps)
        actual, ta = run(rid, 'actual', seeds, runs, steps)
        fields = M.L1A if kind == 'h29' else M.L1B
        gate = comparison(base, actual, fields)
        l2 = M.compare_l2(tb, ta)
        gate['L2_equal'] = l2[0] and not l2[4]['ref_only'] and not l2[4]['cand_only']
        gate['L2_first'] = l2[3]
        scores = (M.l3_scores(kind, world, o, steps) for o in (base, actual))
        sr, sc = scores
        gate['L3_equal'] = equal(sr, sc)
        gate['passed'] &= gate['L2_equal'] and gate['L3_equal']
        check('I2/'+rid, gate)
        if rid in ('A1','A2','A5','A6','B3'):
            h, th = run(rid, 'H', seeds, runs, steps)
            r, tr = run(rid, 'R', seeds, runs, steps)
            check('I7/draws/'+rid, dict(passed=th.rngs == tr.rngs,
                                       steps_checked=len(th.rngs),
                                       roles=sorted(th.rngs[0])))
            if rid in ('A5','A6','B3'):
                chain, tc = run(rid, 'Fly', seeds, runs, steps, reference='chain')
                g = comparison(chain, h, fields)
                g['L2_equal'] = M.compare_l2(tc, th)[0]
                g['L3_equal'] = equal(M.l3_scores(kind,world,chain,steps), M.l3_scores(kind,world,h,steps))
                g['passed'] &= g['L2_equal'] and g['L3_equal']
                check('I1/I7/'+rid, g)
            if rid in ('A1','A2'):
                g = comparison(base,r,TRAJECTORY)
                sr,er=i4_scores(kind,world,base,steps)
                sc,ec=i4_scores(kind,world,r,steps)
                g['L3_equal'] = equal(sr,sc)
                g['L3_scores']={key:equal(sr[key],sc[key]) for key in sr}
                if world=='W1':
                    g['W1_trajectory_scores']={key:equal(sr['w1sum'][key],sc['w1sum'][key]) for key in sr['w1sum']}
                    g['W1_excluded_hold_diagnostics']={key:int(np.count_nonzero(er[key]!=ec[key])) for key in I4_W1_HOLD_KEYS}
                g['allowed_internal_differences'] = {k:int((base[k]!=r[k]).reshape(steps,runs,-1).any(2).sum())
                    for k in ('S','SG','H','SIL','TO','EV','SUS','Z')}
                g['passed'] &= g['L3_equal']
                check('I4/'+rid,g)
            # HR and the pre-noise command are projection outputs, not fields
            # defining divergence. Include all common recorded behavior fields.
            fd = first_difference(h,r,tuple(dict.fromkeys(fields+('C2','P2','VAL'))))
            before = np.arange(steps)[:,None] <= np.where(fd>=0,fd,steps)[None,:]
            hr_ok = bool(((r['HR']==h['PROJECTED_HR']) | ~before).all())
            command_fd = first_difference(h,r,('CLIPPED',))
            eligible = (command_fd>=0) & ((fd<0) | (command_fd<=fd))
            rows = np.flatnonzero(eligible)
            cmd_ok = equal(r['CLIPPED'][command_fd[rows],rows], h['PROJECTED_TURN'][command_fd[rows],rows])
            check('I5/'+rid,dict(passed=hr_ok and cmd_ok, hr_until_first_field=hr_ok,
                                command_while_coupled=cmd_ok, coupled_command_rows=int(eligible.sum()),
                                uncoupled_command_rows=int(((command_fd>=0)&~eligible).sum()),
                                first_field_per_row=fd.tolist(),first_command_per_row=command_fd.tolist()))
    for rid in ('B1','B2','B3'):
        seeds=M.seeds_of('h28',False)
        r,tr=run(rid,'R',seeds,runs,steps)
        chain,tc=run(rid,'R',seeds,runs,steps,reference='chain')
        check('I3/'+rid,comparison(chain,r,ph32.EVERY+('HR',)))
    seeds=M.seeds_of('h29',False)
    for arm in ('Fly','R'):
        x,tx=run('A5',arm,seeds,runs,steps)
        y,ty=run('A5',arm,seeds,runs,steps,reference='A16two')
        check('I6/'+arm,comparison(x,y,ph32.EVERY+('HR',) if arm=='R' else ph32.EVERY))
    return dict(passed=True, runs=runs, steps=steps,
                correction='Nine nonlearning identity rows; the draft eleven is a count error.', gates=gates)


class IdentityFailure(RuntimeError):
    def __init__(self,name,gates):
        super().__init__('identity failed: '+name)
        self.gates=gates


def leave_latency(negative_whiffs, cone, consecutive=30):
    steps,runs=negative_whiffs.shape
    out=np.zeros(runs,int)
    censored=np.zeros(runs,bool)
    for row in range(runs):
        hit=np.flatnonzero(negative_whiffs[:,row])
        if not len(hit): continue
        start=int(hit[0]); out[row]=steps; censored[row]=True
        for t in range(start,steps-consecutive+1):
            if not cone[t:t+consecutive,row].any():
                out[row]=t-start; censored[row]=False; break
    return out,censored


def measures(o):
    steps,runs=o['H'].shape; rows=np.arange(runs); neg=1-o['good']
    whiffs=o['W'][:,rows,neg]
    latency,censored=leave_latency(whiffs,o['NEG_CONE'])
    cls=ph32.cls3(o)
    actual_negative=o['VALH']<0
    read_negative=o['VAL']<0
    instant_negative=(o['HR']>=0)&(o['kv'][rows[None,:],np.maximum(o['HR'],0)]<0)
    previous=np.vstack([o['H0'][None,:],o['H'][:-1]])
    prior_negative=(previous>=0)&(o['kv'][rows[None,:],np.maximum(previous,0)]<0)
    ended=prior_negative&(o['H']!=previous)
    return dict(D_neg=o['dwell'][rows,neg],V=cls==0,tie=cls==2,lost=~o['W'][-200:,:,:2].any((0,2)),
        contacts=o['contacts'],L_leave=latency,L_leave_censored=censored,negative_whiffs=whiffs.sum(0),
        actual_negative_steps=actual_negative.sum(0),held_negative_instant_not=(actual_negative&~instant_negative).sum(0),
        instant_negative_held_not=(instant_negative&~actual_negative).sum(0),
        negative_ends_evidence=(ended&o['EV']).sum(0),negative_ends_timeout=(ended&o['TO']).sum(0),
        flee_violations=(read_negative&(o['TGT']!=o['FLEE'])).sum(0),
        actual_negative_no_flee=(actual_negative&(o['TGT']!=o['FLEE'])).sum(0),
        dwell_source_0=o['dwell'][:,0],dwell_source_1=o['dwell'][:,1],
        first_source_0=np.where(o['AT2'][:,:,0].any(0),o['AT2'][:,:,0].argmax(0),-1),
        first_source_1=np.where(o['AT2'][:,:,1].any(0),o['AT2'][:,:,1].argmax(0),-1),
        first_source=np.where(o['AT2'].any((0,2)),np.where(o['AT2'].any(0),o['AT2'].argmax(0),10**9).argmin(1),-1))
