#!/usr/bin/env python3
"""Module consolidation: the identity check of src/fly.py against the adopted class trees (design v2 FINAL section 6).

Usage: python module_identity.py S0 | A1 | A2 | A3 | A4 | A5 | A6 | A7 | A7r | B1 | B2 | B3
Writes (appends) experiments/module/identity.txt and updates experiments/module/identity.json; echoes to stdout (LF).

Design: notes/module/2026-09-29-module-consolidation-design-v2.md (v2 FINAL, decision:module-consolidation-open). No phN file is
edited: the reference arms are built by the existing hooks (ph35.make for Agent17, ph33.build for Agent16, ph30.build for the
Stage C harness); the candidate fly.Fly is injected at run time into the same harnesses (ph24.make, ph33.build, ph30.build).
Layers, zero tolerance, byte equality: L1 the harness's recorded fields; L2 a sha256 per attribute of the agent object (and of
up, sel, ring, mb) and of the generator state, after every act and every bump; L3 per-row scores by the existing functions.
Seeds are read from the phN constants and never printed (design section 8, [v2, amendment 4]); digests are written in a
digit-free alphabet (hex 0-9 mapped to g-p) so that no output can carry a seed number.
"""
import sys, os, json, time, hashlib, platform
sys.stdout.reconfigure(newline="\n")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import numpy as np
import ph35                                      # Agent17; hooks ph24.make (ph35 -> ph34b -> ph28 -> ph25b -> ph25 -> ph24)
import ph33                                      # Agent16 and its harness (imports ph32, ph30)
import ph31                                      # the Stage C Run 2 seed constant only
import ph24, ph25, ph28, ph30, ph32
import fly

OUT_DIR = os.environ.get("MODULE_OUT") or os.path.join(REPO, "experiments", "module")   # MODULE_OUT: a scratch folder for script checks only
TXT, JSN = os.path.join(OUT_DIR, "identity.txt"), os.path.join(OUT_DIR, "identity.json")
FIXES = []                                       # (old fly.py sha256, new fly.py sha256, cause): filled if a fix is made
DESIGN = "notes/module/2026-09-29-module-consolidation-design-v2.md"

#            kind, world, values
ROWS = {"A1": ("h29", "T1", (1.0, 0.0)), "A2": ("h29", "W1", (1.0, 0.0)), "A3": ("h29", "T3a", (1.0, 0.0)),
        "A4": ("h29", "T3b", (1.0, 0.0)), "A5": ("h29", "T1", (1.0, -1.0)), "A6": ("h29", "T1", (0.0, 0.0)),
        "A7": ("sim", "Agent17", None), "A7r": ("sim", "Agent14N2", None),
        "B1": ("h28", "T1", (1.0, 0.0, 0.0)), "B2": ("h28", "W1", (1.0, 0.0, 0.0)), "B3": ("h28", "T1", (1.0, -1.0, 0.0))}
ROLE = {"A1": "adopted scope", "A2": "adopted scope", "A3": "adopted scope", "A4": "adopted scope (t0 150)",
        "A5": "coverage: N2 negative branch", "A6": "coverage: two-odour top set", "A7": "coverage, no recorded reference",
        "A7r": "recorded reference", "B1": "adopted scope (T1D)", "B2": "adopted scope (W1D)", "B3": "coverage: N2 negative branch (T1D)"}
SEED_NAME = {"h29": "ph35.SEEDS['eval']", "h28": "ph33.SEEDS['eval']", "sim": "ph31.SEEDS['eval'][0]"}
L1A = ph28.BEHK + ("SUS", "Z", "AT2", "C")                                    # design section 6, L1 (two-channel harness)
L1B = ("POS", "HEAD", "S", "SG", "H", "NAV", "SINCE", "TGT", "SIL", "TO", "EV", "SUS", "Z", "W", "AT2", "C", "VAL")
SIM_DROP = ("n2S", "n2Z")                        # end-of-run counts of ReleaseN2's measurement-only n2S/n2Z (dropped, design 4.1)
SUB = ("up", "sel", "ring", "mb")
DIGITFREE = str.maketrans("0123456789", "ghijklmnop")


def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def df(hexs): return hexs.translate(DIGITFREE)


def seeds_of(kind, smoke):
    if smoke: return (5, 6)                      # the demo seeds (design section 6, S0)
    return {"h29": ph35.SEEDS["eval"], "h28": ph33.SEEDS["eval"], "sim": ph31.SEEDS["eval"][0]}[kind]


def size_of(kind, smoke):
    if smoke: return (40, 600) if kind == "sim" else (40, 200)   # the Stage C harness counts in blocks of 600 steps
    return (ph30.R, ph30.T1) if kind == "sim" else (400, 600)


# ------------------------------------------------------------------ L2: the per-step state hash
def blob(v):
    if isinstance(v, np.ndarray):
        a = np.ascontiguousarray(v); return b"A" + a.dtype.str.encode() + repr(a.shape).encode() + a.tobytes()
    if isinstance(v, np.random.Generator): return b"G" + repr(v.bit_generator.state).encode()
    if v is None or isinstance(v, (bool, int, float, str, tuple, list, set, np.generic)): return b"S" + type(v).__name__.encode() + repr(v).encode()
    return b"O" + type(v).__name__.encode()


def walk(a):
    out = {}
    for k, v in vars(a).items():
        if k in ("act", "bump"): continue        # the tap's own wrappers
        if k in SUB:
            for k2, v2 in vars(v).items(): out[k + "." + k2] = v2
        else: out[k] = v
    return out


class Tap:
    """wraps an agent instance's act and bump; after each call records a sha256 per attribute (or checks it against a twin)"""
    def __init__(self, capture=None):
        self.events, self.capture, self.snap = [], capture, None

    def attach(self, a):
        act0, bump0 = a.act, a.bump
        def act(*x, **k): r = act0(*x, **k); self.rec(a, "act"); return r
        def bump(*x, **k): r = bump0(*x, **k); self.rec(a, "bump"); return r
        a.act, a.bump = act, bump; self.agent = a

    def rec(self, a, kind):
        st = walk(a)
        if self.capture is not None and len(self.events) == self.capture:
            self.snap = {k: (np.copy(v) if isinstance(v, np.ndarray) else v) for k, v in st.items()}
        self.events.append((kind, {k: hashlib.sha256(blob(v)).digest() for k, v in st.items()}))


def compare_l2(tr, tc):
    """(ok, n_events, n_hashes, first mismatch, names) over the names common to both arms"""
    er, ec = tr.events, tc.events
    nr, nc = set(er[0][1]) if er else set(), set(ec[0][1]) if ec else set()
    common = sorted(nr & nc); first = None; nh = 0
    if len(er) != len(ec): first = ("event count", len(er), len(ec))
    for i, ((kr, dr), (kc, dc)) in enumerate(zip(er, ec)):
        if first is not None: break
        if kr != kc or set(dr) != nr or set(dc) != nc: first = (i, "event kind or attribute set", ""); break
        for k in common:
            nh += 1
            if dr[k] != dc[k]: first = (i, kr, k); break
    return first is None, min(len(er), len(ec)), nh, first, dict(common=common, ref_only=sorted(nr - nc), cand_only=sorted(nc - nr))


def chain(events, names):
    """one digest per event over the common names, and one chain digest per name (for identity.json)"""
    per = [df(hashlib.sha256(b"".join(d[k] for k in names)).hexdigest()) for _, d in events]
    byname = {}
    for k in names:
        h = hashlib.sha256()
        for _, d in events: h.update(d[k])
        byname[k] = df(h.hexdigest())
    return per, byname


# ------------------------------------------------------------------ hooks (run time; no file edited)
class CAND2:
    """marker: the candidate fly.Fly at nch 2 through ph24.make"""


TAP = [None]
_make_prev = ph24.make                           # ph35.make
_build33_prev = ph33.build
_build30_prev = ph30.build
SIMKIND = [None]
ph33.ARMS["module D on"] = ("CAND3", 3, True)    # run-time entry for the candidate's arm in ph33.run (the dict, not the file)


def make_hook(cls, runs, rng, G, known, gate=True, filt=True, release=True):
    if cls is CAND2:
        assert G == fly.G_STAR and gate and filt and release
        a = fly.Fly(runs, rng, known, nch=2)
    else: a = _make_prev(cls, runs, rng, G, known, gate, filt, release)
    TAP[0].attach(a); return a


def build33_hook(kind, runs, seed_a, g, kv):
    if kind == "CAND3":
        rng = np.random.default_rng(seed_a); rng3 = np.random.default_rng(seed_a + ph32.A3_OFF)   # as src/ph33.py:207
        a = fly.Fly(runs, rng, kv, nch=3, rng3=rng3)
    else: a = _build33_prev(kind, runs, seed_a, g, kv)
    TAP[0].attach(a); return a


def build30_hook(kind, runs, rng, w, vals):
    assert kind == "A14N2"                       # the 'learned' arm of ph30.E1ARMS
    kv = ph30.kv_of(vals, w.good); mode = SIMKIND[0]
    if mode == "ref Agent17":
        a = ph35.Agent17(runs, rng, P=ph28.P_PRIOR, N_hi=ph35.N17, G=ph30.G_STAR, known=kv, rule=True, filt=True, scope="prior", release=True)
    elif mode == "ref Agent14N2": a = _build30_prev(kind, runs, rng, w, vals)
    else:
        a = fly.Fly(runs, rng, kv, nch=2)
        if mode == "cand at 300":                # A7r: test-only setting of the window (design v2 section 6, amendment 2)
            a.N = a.N_hi = ph28.N_HI; a.c = np.full((runs, 2), float(ph28.N_HI - ph28.P_PRIOR))
    TAP[0].attach(a); return a


ph24.make, ph33.build, ph30.build = make_hook, build33_hook, build30_hook


# ------------------------------------------------------------------ equality (bytes, strictest)
def beq(x, y):
    if isinstance(x, dict) or isinstance(y, dict):
        return isinstance(x, dict) and isinstance(y, dict) and set(x) == set(y) and all(beq(x[k], y[k]) for k in x)
    if isinstance(x, np.ndarray) or isinstance(y, np.ndarray) or isinstance(x, np.generic):
        a, b = np.asarray(x), np.asarray(y)
        return a.dtype == b.dtype and a.shape == b.shape and np.ascontiguousarray(a).tobytes() == np.ascontiguousarray(b).tobytes()
    return type(x) == type(y) and repr(x) == repr(y)


def l3_scores(kind, world, o, steps):
    if kind == "h29":
        s = dict(dwell=o["dwell"], first=o["first"], contacts=o["contacts"], cls3=ph25.cls3(o))
        if world == "W1": s["w1sum"] = ph25.w1sum(o)
        if world == "T3a": s["t3_dwell_100"] = ph24.t3_dwell(o, 100, steps)
        if world == "T3b": s["t3_dwell_400"] = ph24.t3_dwell(o, 400, steps); s["lost300_W200"] = ph28.lost300(o, W=ph35.N17)
        return s
    s = dict(dwell=o["dwell"], contacts=o["contacts"], first=np.where(o["AT2"].any(0), o["AT2"].argmax(0), -1), cls3=ph32.cls3(o),
             lost_t1=ph32.lost_t1(o))
    if world == "W1": s["w1sum"] = ph32.w1sum(o)
    return s


# ------------------------------------------------------------------ one row
def run_harness(kind, world, vals, seeds, runs, steps, cand, capture=None):
    TAP[0] = Tap(capture)
    if kind == "h29": o = ph35.run(world, CAND2 if cand else ph35.Agent17, vals, seeds, runs=runs, steps=steps)
    else: o = ph33.run(world, "module D on" if cand else "Agent16 D on", vals, seeds, runs=runs, steps=steps)
    return o, TAP[0]


def row_harness(rid, kind, world, vals, seeds, runs, steps):
    o_r, t_r = run_harness(kind, world, vals, seeds, runs, steps, False)
    o_c, t_c = run_harness(kind, world, vals, seeds, runs, steps, True)
    fields = L1A if kind == "h29" else L1B
    l1 = {k: beq(o_r[k], o_c[k]) for k in fields}
    ok2, nev, nh, first, names = compare_l2(t_r, t_c)
    loc = None
    if not ok2 and isinstance(first[0], int): loc = locate_harness(kind, world, vals, seeds, runs, steps, first)
    sr, sc = l3_scores(kind, world, o_r, steps), l3_scores(kind, world, o_c, steps)
    l3 = {k: beq(sr[k], sc[k]) for k in sr}
    elems = sum(int(np.asarray(o_r[k]).size) for k in fields)
    extra = dict(construction=dict(ref=dict(draws_equal=o_r["draws_equal"], rng_equal=o_r["rng_equal"]),
                                   cand=dict(draws_equal=o_c["draws_equal"], rng_equal=o_c["rng_equal"])))
    return l1, elems, (ok2, nev, nh, first, names, loc), l3, (t_r, t_c), extra


def locate_harness(kind, world, vals, seeds, runs, steps, first):
    ev, _, name = first
    _, tr = run_harness(kind, world, vals, seeds, runs, steps, False, capture=ev)
    _, tc = run_harness(kind, world, vals, seeds, runs, steps, True, capture=ev)
    return where(tr.snap.get(name), tc.snap.get(name))


def where(x, y):
    if isinstance(x, np.ndarray) and isinstance(y, np.ndarray) and x.shape == y.shape and x.ndim >= 1:
        d = (x != y).reshape(x.shape[0], -1).any(1) if x.shape[0] else np.zeros(0, bool)
        rows = np.flatnonzero(d)
        return dict(rows_differing=int(len(rows)), first_row=int(rows[0]) if len(rows) else None)
    return dict(ref=repr(x)[:200], cand=repr(y)[:200])


def row_sim(rid, seeds, runs, steps):
    """A7 / A7r: ph30.e1_sim's 'learned' arm (learning on, mirror 'v'), the two arms stepped in lockstep"""
    ref, cand = ("ref Agent14N2", "cand at 300") if rid == "A7r" else ("ref Agent17", "cand")
    SIMKIND[0] = ref; TAP[0] = Tap(); s_r = ph30.e1_sim("learned", seeds, runs=runs, steps=steps, trace=True); t_r = TAP[0]
    SIMKIND[0] = cand; TAP[0] = Tap(); s_c = ph30.e1_sim("learned", seeds, runs=runs, steps=steps, trace=True); t_c = TAP[0]
    l1 = {}; elems = 0; first = None; nh = 0; nev = 0; names = None
    for t in range(steps):
        a, b = s_r.step(t), s_c.step(t)
        if names is None: names = sorted(a)
        for k in a:
            e = beq(a[k], b.get(k)); l1[k] = l1.get(k, True) and e; elems += int(np.asarray(a[k]).size)
        ok, n, h, f, nm = compare_l2(t_r, t_c); nh += h; nev += n
        if not ok and first is None: first = (f, t)
        t_r.events.clear(); t_c.events.clear()
        if first is not None or not all(l1.values()): break
    o_r, o_c = s_r.finish(), s_c.finish()
    keys = [k for k in o_r if k not in SIM_DROP]
    l3 = {k: beq(o_r[k], o_c[k]) for k in keys}
    ok2 = first is None
    return l1, elems, (ok2, nev, nh, first, nm, None), l3, None, dict(steps_run=t + 1, sim_dropped=list(SIM_DROP), sim_names=names)


# ------------------------------------------------------------------ output
def header(rid, smoke, names):
    mods = sorted({m.__name__: os.path.abspath(m.__file__) for m in list(sys.modules.values())
                   if getattr(m, "__file__", None) and os.path.abspath(m.__file__).startswith(HERE)}.items())
    L = [f"== module identity, row {rid}{' (S0 smoke)' if smoke else ''}: {ROLE.get(rid, '')}. design {DESIGN} ==",
         f"   python {sys.version.split()[0]} ({sys.version}); numpy {np.__version__}; platform {platform.platform()}",
         "   threads: " + ", ".join(f"{k}={os.environ.get(k, '')}" for k in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "PH30_PROCS", "PH33_PROCS")),
         f"   module_identity.py sha256 {sha(os.path.abspath(__file__))}; fly.py sha256 {sha(os.path.join(HERE, 'fly.py'))}",
         "   imported source files (sha256): " + "; ".join(f"{n}.py {sha(p)}" for n, p in mods if n != "__main__"),
         "   fixes during the run: " + ("; ".join(f"fly.py {a} -> {b}: {c}" for a, b, c in FIXES) if FIXES else "none")]
    if names:
        L.append(f"   L2 attributes hashed (common to both arms, {len(names['common'])}): " + ", ".join(names["common"]))
        L.append(f"   L2 reference-only attributes, not hashed ({len(names['ref_only'])}): " + ", ".join(names["ref_only"]))
        L.append(f"   L2 candidate-only attributes, not hashed ({len(names['cand_only'])}): " + ", ".join(names["cand_only"]))
        L.append("   L2 generator state: 'rng' and every sub-object's 'rng'/'rng3' hashed as bit_generator.state")
    return L


def one(rid, smoke, say):
    kind, world, vals = ROWS[rid]; seeds = seeds_of(kind, smoke); runs, steps = size_of(kind, smoke)
    t0 = time.time()
    if kind == "sim": l1, elems, l2, l3, taps, extra = row_sim(rid, seeds, runs, steps)
    else: l1, elems, l2, l3, taps, extra = row_harness(rid, kind, world, vals, seeds, runs, steps)
    ok2, nev, nh, first, names, loc = l2; dt = time.time() - t0
    ok = all(l1.values()) and ok2 and all(l3.values()) and all(v for d in extra.get("construction", {}).values() for v in d.values())
    L = header(rid, smoke, names)
    what = f"world {world}, values {vals}" if kind != "sim" else f"World6 E1-C 'learned' arm, reference {'Agent17' if rid == 'A7' else 'Agent14N2'}"
    L.append(f"   row: {what}; seeds {'the demo seeds (5, 6)' if smoke else SEED_NAME[kind]}; {runs} rows x {steps} steps")
    if "construction" in extra: L.append(f"   harness construction checks (draws_equal, rng_equal): {extra['construction']}")
    if kind == "sim": L.append(f"   steps run in lockstep {extra['steps_run']}; L3 excludes {extra['sim_dropped']} (measurement of dropped attributes, design 4.1)")
    L.append(f"   L1 recorded fields: {sum(l1.values())}/{len(l1)} equal ({elems} elements compared): " + ", ".join(f"{k} {v}" for k, v in l1.items()))
    L.append(f"   L2 state hashes: {'EQUAL' if ok2 else 'DIFFER'}; events compared {nev} (acts and bumps); hashes compared {nh}"
             + ("" if ok2 else f"; first mismatch {first}; located {loc}"))
    L.append(f"   L3 per-row scores: {sum(l3.values())}/{len(l3)} equal: " + ", ".join(f"{k} {v}" for k, v in l3.items()))
    L.append(f"   RESULT {rid}{' S0' if smoke else ''}: {'IDENTICAL' if ok else 'DIFFERENT'}; run time {dt:.1f} s")
    for x in L: say(x)
    rec = dict(role=ROLE[rid], smoke=smoke, seeds=("demo" if smoke else SEED_NAME[kind]), runs=runs, steps=steps, identical=ok,
               L1=l1, L1_elements=elems, L2=dict(equal=ok2, events=nev, hashes=nh, first=repr(first), located=loc, names=names),
               L3=l3, seconds=round(dt, 1), fly_sha=df(sha(os.path.join(HERE, "fly.py"))), script_sha=df(sha(os.path.abspath(__file__))))
    if taps is not None:
        per_r, by_r = chain(taps[0].events, names["common"]); per_c, by_c = chain(taps[1].events, names["common"])
        rec["L2"]["digests_ref"], rec["L2"]["digests_cand"], rec["L2"]["by_name_ref"], rec["L2"]["by_name_cand"] = per_r, per_c, by_r, by_c
    return ok, rec


def main(arg):
    os.makedirs(OUT_DIR, exist_ok=True)
    rows = list(ROWS) if arg == "S0" else [arg]; smoke = arg == "S0"
    fh = open(TXT, "a", encoding="utf-8", newline="\n")
    def say(s): print(s); fh.write(s + "\n"); fh.flush()
    data = json.load(open(JSN, encoding="utf-8")) if os.path.exists(JSN) else {}
    all_ok = True
    for rid in rows:
        ok, rec = one(rid, smoke, say); all_ok &= ok
        data[("S0/" if smoke else "") + rid] = rec
        with open(JSN, "w", encoding="utf-8", newline="\n") as f: json.dump(data, f, indent=1, sort_keys=True)
        if not ok: say(f"STOP: row {rid} differs (design section 6 stop rule)"); break
    fh.close()
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
