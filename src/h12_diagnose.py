#!/usr/bin/env python3
"""H12 Package D: diagnostic reuse of the spent Stage 2 bench pair only.

Run after the original ph36b bench has reproduced in its immutable checkout:
  python src/h12_diagnose.py --output experiments/h12/diagnosis \
      --reference-bench remote-output/ph36b_bench.txt

No development/evaluation seeds, parameter search, verdict, or Package E run occurs here.
"""
import argparse
import hashlib
import json
import os
import platform
import socket
import sys
from pathlib import Path

import numpy as np

import ph36b as b

SOURCE_SHA = "cfb9a26a45bfd5ef9e5d781d73a772e3129db24e633c66eeb89c2d61556f1cef"
DONORS = (("H12", "P"), ("gate only", "A0"), ("H11 full", "A1"))
MODES = ("A0", "A1", "P")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def module(mode, n, rng):
    if mode == "P":
        return b.MB5(n, parallel=True, gated=True, tau=(None, None, b.TAU, b.TAU), rng=rng, **b.ph11.MB)
    return b.MB4(n, parallel=(mode == "A1"), gated=True, rng=rng, **b.ph11.MB)


def external_bench(path):
    recorded = Path(b.REPO, "experiments/h12/ph36b_bench.txt").read_bytes()
    actual = Path(path).read_bytes()
    require(actual == recorded, "original bench stdout differs bytewise from committed ph36b_bench.txt")
    return {"recorded_sha256": hashlib.sha256(recorded).hexdigest(),
            "remote_sha256": hashlib.sha256(actual).hexdigest(), "byte_equal": True}


def nav_contributors(o, whiff=None):
    """Reconstruct Agent9/14's selected navigation branch and flee override."""
    rows = np.arange(b.R)
    g = o["good"]
    h = o["H"]
    x = o["W"] if whiff is None else whiff
    p = o["P2"]
    v = o["KV"]
    pv = p[:, rows, g]
    pn = p[:, rows, 1-g]
    vmax = np.maximum(np.where(pv, v, -np.inf), np.where(pn, b.C, -np.inf))
    vh = np.where(h == g[None, :], v, b.C)
    keep = (h >= 0) & ((vh == vmax) | (vh < 0))
    top_v = pv & (v >= 0) & (v == vmax)
    top_n = pn & (b.C >= 0) & (b.C == vmax)
    whiff_v = x[:, rows, g]
    whiff_n = x[:, rows, 1-g]
    v_support = whiff_v & ((keep & (h == g[None, :])) | (~keep & top_v))
    n_support = whiff_n & ((keep & (h == (1-g)[None, :])) | (~keep & top_n))
    require(np.array_equal(v_support | n_support, o["NAV"]),
            "reconstructed V/N whiff contributors do not account for every NAV event")
    flee = o["NAV"] & (h >= 0) & (vh < 0)
    return v_support & ~flee, n_support & ~flee, flee, v_support & n_support


def instrumentation(arm):
    """Copy ph36b.run's draw/update order and add a compact fixed input tape."""
    n, steps, seeds = b.R, b.T, b.SEEDS["bench"]
    label, trn, learn, reinf, vals = b.ARMS[arm]
    require(learn and trn == "trained" and vals == "mirror", "instrument only original trained donors")
    w = b.ph23.Lost(n, np.random.default_rng(seeds[0]), seeds[0])
    g = w.good
    rows = np.arange(n)
    nu = 1 - g
    w.pres = nu.copy()
    w.absent = g.copy()
    tw = b.World7(n, np.random.default_rng(seeds[0]), seeds[0])
    kv = np.zeros((n, 2))
    kv[rows, g] = 1.0
    kv[rows, nu] = b.C
    rng = np.random.default_rng(seeds[1])
    with b.ph28.pn(b.P_PRIOR, b.N17):
        a = b.ph24.make(b.Agent17, n, rng, b.G_STAR, kv, True, True, True)
    require(type(a) is b.Agent17 and a.N_hi == b.N17, "agent constructor changed")
    if label == "P":
        a.mb = module("P", n, a.mb.rng)
    elif label == "A1":
        a.mb = module("A1", n, a.mb.rng)
    train = b.ph29.train(a, g, trn)
    code_v = a.codes[rows, g].copy()
    code_n = a.codes[rows, nu].copy()
    initial = dict(w=a.mb.w.copy(), tc=a.mb.tc.copy(), tr=a.mb.tr.copy())
    a.known = np.zeros((n, 2))
    a.known[rows, nu] = b.C
    a.known[rows, g] = a.mb.valence(code_v)
    a.cast_sign = b.cast_draw(seeds[1], n)
    o = dict(arm=arm, good=g, cell=w.cell, steps=steps, draws_equal=True, v_train=train, calls=0,
             **b.ph24.blank(steps, n), POS=np.zeros((steps, n, 2)), HEAD=np.zeros((steps, n)),
             AT2=np.zeros((steps, n, 2), bool), C=np.zeros((steps, n), bool),
             KV=np.zeros((steps, n)), VT={}, FU=np.full(n, -1), unreinf=np.zeros(n, int))
    tape = {"raw_whiff": np.zeros((steps, n, 2), bool),
            "masked_whiff": np.zeros((steps, n, 2), bool),
            "contact": o["AT2"],
            "code_present": np.zeros((steps, n), bool),
            "external_reward": np.zeros((steps, n), bool),
            "tc_pre_sum": np.zeros((steps, n), np.float32),
            "tr_pre": np.zeros((steps, n, 4), np.float32),
            "tc_post_sum": np.zeros((steps, n), np.float32),
            "tr_post": np.zeros((steps, n, 4), np.float32),
            "output_pre": np.zeros((steps, n, 4), np.float32),
            "output_post": np.zeros((steps, n, 4), np.float32),
            "held": o["H"], "presence": np.zeros((steps, n, 2), bool),
            "nav_hit": o["NAV"], "nav_to_v": np.zeros((steps, n), bool),
            "nav_to_n": np.zeros((steps, n), bool), "nav_flee": np.zeros((steps, n), bool),
            "nav_ambiguous_both": np.zeros((steps, n), bool),
            "filter_eligible_v": np.zeros((steps, n), bool),
            "distance_v": np.zeros((steps, n), np.float32),
            "valence_pre": o["KV"], "valence_post": np.zeros((steps, n))}
    checkpoint = None
    p3_end = None
    acquisition_value = None
    source_v = w.src[rows, g].copy()
    for t in range(steps):
        if t == b.P1:
            acquisition_value = a.mb.valence(code_v).copy()
        if t == b.P2E:
            checkpoint = dict(w=a.mb.w.copy(), tc=a.mb.tc.copy(), tr=a.mb.tr.copy(),
                              code=code_v.copy(), value=a.mb.valence(code_v).copy(),
                              outputs=a.mb.out(code_v).copy())
        if t == b.P3E:
            p3_end = dict(value=a.mb.valence(code_v).copy(), outputs=a.mb.out(code_v).copy(),
                          w=a.mb.w.copy(), tc=a.mb.tc.copy(), tr=a.mb.tr.copy())
        w.on = b.P2E <= t < b.P3E
        tw.pos, tw.head = w.pos.copy(), w.head.copy()
        pa = (a.sel.s > 1.0).any(1)
        x = w.sense()
        on = w.wind_on()
        raw = tw.sense()
        ton = tw.wind_on()
        o["draws_equal"] &= bool(np.array_equal(raw, w.raw) and np.array_equal(on, ton)
                                 and np.array_equal(x[rows, nu], raw[rows, nu])
                                 and np.array_equal(x[rows, g], np.zeros(n, bool) if w.on else raw[rows, g]))
        tape["raw_whiff"][t] = raw
        tape["masked_whiff"][t] = x
        a.known = np.zeros((n, 2))
        a.known[rows, nu] = b.C
        a.known[rows, g] = a.mb.valence(code_v)
        o["KV"][t] = a.known[rows, g]
        tape["output_pre"][t] = a.mb.out(code_v)
        tape["tc_pre_sum"][t] = a.mb.tc.sum(1)
        tape["tr_pre"][t] = a.mb.tr
        turn, h = a.act(w, x, on)
        b.ph24.record(o, t, a, h, x, pa)
        # Presence is the actual pre-action filter state; eligibility also requires value and rank.
        tape["presence"][t] = o["P2"][t]
        present_v = o["P2"][t, rows, g]
        present_n = o["P2"][t, rows, nu]
        tape["filter_eligible_v"][t] = present_v & (o["KV"][t] >= 0) & (~present_n | (o["KV"][t] >= b.C))
        # Compute after the loop from the recorded filter branch, including h == -1.
        w.move(turn)
        a.bump(w.bumped)
        at = w.at_source()
        o["POS"][t] = w.pos
        o["HEAD"][t] = w.head
        o["AT2"][t] = at
        o["C"][t] = w.bumped
        tape["distance_v"][t] = np.linalg.norm(w.pos - source_v, axis=1)
        at_v = at[rows, g]
        rv = np.zeros((n, a.mb.C))
        reinforced = reinf and (t < b.P1 or t >= b.P3E)
        if reinforced:
            rv[:, 1] = at_v
        nr = at_v & ~reinforced
        o["FU"] = np.where((o["FU"] < 0) & nr, t, o["FU"])
        o["unreinf"] += nr
        tape["code_present"][t] = at_v
        tape["external_reward"][t] = rv[:, 1] > 0
        a.mb.step(code=code_v * at_v[:, None], reinf=rv)
        o["calls"] += 1
        tape["tc_post_sum"][t] = a.mb.tc.sum(1)
        tape["tr_post"][t] = a.mb.tr
        tape["output_post"][t] = a.mb.out(code_v)
        tape["valence_post"][t] = a.mb.valence(code_v)
        if (t + 1) % b.BLK == 0:
            oo = a.mb.out(code_v)
            o["VT"][t] = dict(v=a.mb.valence(code_v), acq=oo[:, 0] - oo[:, 1],
                               par=oo[:, 2] - oo[:, 3], out1=oo[:, 1], out0=oo[:, 0])
    o["rng_equal"] = w.rng.bit_generator.state == tw.rng.bit_generator.state
    o["mb_calls_attr"] = o["calls"]
    tape["presence_counter"] = o["C2"]
    (tape["nav_to_v"][:], tape["nav_to_n"][:], tape["nav_flee"][:],
     tape["nav_ambiguous_both"][:]) = nav_contributors(o, tape["masked_whiff"])
    return o, tape, checkpoint, p3_end, acquisition_value, code_v, code_n, initial


def assert_identity(ref, inst):
    for key in b.KEYS:
        require(np.array_equal(ref[key], inst[key]), f"instrumented original differs at {ref['arm']}:{key}")
    for key in ("good", "cell", "v_train", "FU", "unreinf"):
        require(np.array_equal(ref[key], inst[key]), f"instrumented original differs at {ref['arm']}:{key}")
    for key in ("draws_equal", "rng_equal", "calls"):
        require(ref[key] == inst[key], f"instrumented original differs at {ref['arm']}:{key}")
    for t in ref["VT"]:
        for key in ref["VT"][t]:
            require(np.array_equal(ref["VT"][t][key], inst["VT"][t][key]),
                    f"instrumented original differs at {ref['arm']}:VT:{t}:{key}")


def train_module(mode, code_v, code_n):
    n = len(code_v)
    m = module(mode, n, np.random.default_rng(b.SEEDS["bench"][1]))
    z = np.zeros((n, m.C))
    rv = z.copy()
    rv[:, 1] = 1.0
    for _ in range(b.ph29.TRAIN):
        m.step(code=code_n, reinf=z)
    for _ in range(b.ph29.GAP):
        m.step()
    for _ in range(b.ph29.TRAIN):
        m.step(code=code_v, reinf=rv)
    m.tc[:] = 0.0
    m.tr[:] = 0.0
    return m


def replay(tape, code_v, code_n, mode, own_initial=None):
    """Same donor code/contact/reward tape; module never controls the path."""
    n = len(code_v)
    m = train_module(mode, code_v, code_n)
    if own_initial is not None:
        for key in ("w", "tc", "tr"):
            require(np.array_equal(getattr(m, key), own_initial[key]),
                    f"own donor off-world training differs: {mode}:{key}")
    vals = np.zeros((b.T, n))
    value_pre = np.zeros((b.T, n))
    contact = tape["code_present"]
    reward = tape["external_reward"]
    for t in range(b.T):
        value_pre[t] = m.valence(code_v)
        rv = np.zeros((n, m.C))
        rv[:, 1] = reward[t]
        m.step(code=code_v * contact[t, :, None], reinf=rv)
        vals[t] = m.valence(code_v)
    return value_pre, vals


def opportunity(o, tape=None):
    n, rows, g = b.R, np.arange(b.R), o["good"]
    sl = slice(b.P3E, b.P4E)
    whiff_arr = tape["masked_whiff"] if tape is not None else o["W"]
    whiff = whiff_arr[sl, rows, g].any(0)
    presence = o["P2"]
    eligible_arr = (presence[:, rows, g] & (o["KV"] >= 0) &
                    (~presence[:, rows, 1-g] | (o["KV"] >= b.C)))
    eligible = eligible_arr[sl].any(0)
    if tape is not None:
        nav_arr, n_arr, flee_arr, ambig_arr = (tape[k] for k in
            ("nav_to_v", "nav_to_n", "nav_flee", "nav_ambiguous_both"))
    else:
        nav_arr, n_arr, flee_arr, ambig_arr = nav_contributors(o)
    nav = nav_arr[sl].any(0)
    contact = o["AT2"][sl, rows, g].any(0)
    dv = o["AT2"][sl, rows, g].sum(0)
    dn = o["AT2"][sl, rows, 1-g].sum(0)
    # Ordered, exhaustive categories over all assigned rows.
    cats = np.select((~whiff, whiff & ~nav, whiff & nav & ~contact,
                      whiff & nav & contact & (dv <= dn)), (0, 1, 2, 3), default=4).astype(np.int8)
    require(np.all(np.bincount(cats, minlength=5).sum() == n), "opportunity partition incomplete")
    return dict(partition={k: int((cats == i).sum()) for i, k in enumerate((
        "no_V_whiff", "V_whiff_no_V_nav", "V_nav_no_V_contact",
        "V_contact_no_majority", "V_majority"))},
        whiff=int(whiff.sum()), filter_eligible=int(eligible.sum()),
        actual_V_supported_upwind_nav=int(nav.sum()),
        actual_N_supported_upwind_nav=int(n_arr[sl].any(0).sum()),
        flee_nav_rows=int(flee_arr[sl].any(0).sum()),
        ambiguous_both_supported_rows=int(ambig_arr[sl].any(0).sum()),
        contact=int(contact.sum()), V_majority_unconditional=int((dv > dn).sum()),
        tie_zero=int(((dv == dn) & (dv == 0)).sum()),
        tie_positive=int(((dv == dn) & (dv > 0)).sum()),
        N_majority=int((dn > dv).sum()),
        mean_min_distance_v=(float(tape["distance_v"][sl].min(0).mean()) if tape is not None else None),
        no_whiff_but_contact=int((~whiff & contact).sum()),
        no_V_nav_but_contact=int((~nav & contact).sum()))


def pure_retention(checkpoint):
    """A1 boundary clones. All 400 rows; zero code and external reinforcement."""
    code = checkpoint["code"]
    n = len(code)
    base = checkpoint["value"]
    out = {}
    for mode in ("decay_off", "decay_on"):
        m = module("P" if mode == "decay_on" else "A1", n,
                   np.random.default_rng(b.SEEDS["bench"][1]))
        for key in ("w", "tc", "tr"):
            getattr(m, key)[:] = checkpoint[key]
        require(np.array_equal(m.valence(code), base), "D=0 clone inequality")
        acq = m.w[:, :2].copy()
        values = {0: m.valence(code).copy()}
        outputs = {0: m.out(code).copy()}
        # None inputs are the module's exact zero-input path. Assert all external inputs by construction.
        for d in range(1, 5001):
            m.step(code=None, reinf=None)
            if d in (1200, 5000):
                require(np.array_equal(m.w[:, :2], acq), "acquisition weights moved during pure retention")
                values[d] = m.valence(code).copy()
                outputs[d] = m.out(code).copy()
        out[mode] = dict(values=values, outputs=outputs,
                         acquisition_invariant=bool(np.array_equal(m.w[:, :2], acq)))
    require(np.array_equal(out["decay_off"]["values"][0], out["decay_on"]["values"][0]),
            "D=0 modes differ")
    return out


def retention_summary(r, acquisition_value):
    off, on = r["decay_off"], r["decay_on"]
    ext = on["values"][0]
    trained_sign = np.sign(acquisition_value)
    denominator = trained_sign * (acquisition_value - ext)
    valid = (trained_sign != 0) & (denominator > 1e-12)
    signed = {}
    for d in (0, 1200, 5000):
        v = on["values"][d]
        ctl = off["values"][d]
        signed[str(d)] = dict(median_value=float(np.median(v)),
                             median_delta_from_checkpoint=float(np.median(v-ext)),
                             positive=int((v > 0).sum()), negative=int((v < 0).sum()),
                             zero=int((v == 0).sum()),
                             above_competitor=int((v > b.C).sum()),
                             crossing_from_below=int(((ext < b.C) & (v >= b.C)).sum()),
                             decay_off_median=float(np.median(ctl)),
                             changed_from_off=int((v != ctl).sum()),
                             valid_signed_recovery_denominator=int(valid.sum()),
                             invalid_signed_recovery_denominator=int((~valid).sum()),
                             sign_preserved=int(((trained_sign*v) > 0).sum()),
                             median_signed_recovery=(float(np.median(
                                 (trained_sign*(v[valid]-ext[valid]))/denominator[valid]))
                                 if valid.any() else None))
    return signed


def bench_arm(o):
    dv, dn = b.dwell(o)
    return {"blocks": [{"V": int((dv[i] > dn[i]).sum()), "N": int((dn[i] > dv[i]).sum()),
                        "tie": int((dv[i] == dn[i]).sum()),
                        "mean_dwell_V": float(dv[i].mean()), "mean_dwell_N": float(dn[i].mean())}
                       for i in range(b.NB)],
            "draws_equal": bool(o["draws_equal"]), "rng_equal": bool(o["rng_equal"]),
            "calls": int(o["calls"]),
            "P3_contact_steps_V": int(o["AT2"][b.P2E:b.P3E, np.arange(b.R), o["good"]].sum()),
            "P3_contact_rows_V": int(o["AT2"][b.P2E:b.P3E, np.arange(b.R), o["good"]].any(0).sum())}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--reference-bench", required=True, type=Path)
    args = p.parse_args()
    require(digest(b.__file__) == SOURCE_SHA, "ph36b.py source hash changed")
    for name, expected in b.SHA_ON_RECORD.items():
        require(digest(Path(b.HERE, name + ".py")) == expected, f"{name}.py source hash changed")
    require(digest(b.ph36.__file__) == b.PH36_SHA, "ph36.py source hash changed")
    require(digest(b.ph36.DESIGN_FILE) == b.DESIGN.split("hash ")[1], "design source hash changed")
    bench = external_bench(args.reference_bench)
    args.output.mkdir(parents=True, exist_ok=True)
    manifest = dict(hostname=socket.gethostname(), platform=platform.platform(),
                    python=sys.version, numpy=np.__version__, seeds={"world": b.SEEDS["bench"][0],
                    "agent": b.SEEDS["bench"][1], "bootstrap": b.BOOT,
                    "smoke_world": 5, "smoke_agent": 6}, seed_status="diagnostic reuse only",
                    source_sha256={p.name: digest(p) for p in Path(b.HERE).glob("ph*.py")},
                    diagnostic_sha256=digest(__file__), original_bench=bench,
                    extra_precision_tolerance=0.0, field_identity="bitwise array equality",
                    scope="Package D measurement; no behavioural verdict or adoption")
    (args.output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    summary = {"original_bench": bench, "arms": {}, "donor_replays": {}, "opportunity": {},
               "retention": {}, "checks": {}}
    saved = {}
    checkpoint_a1 = None
    gate_ref = None
    for arm, own_mode in DONORS:
        print(f"diagnosing donor {arm}", flush=True)
        ref = b.run(arm, b.SEEDS["bench"])
        inst, tape, checkpoint, p3_end, acquisition_value, code_v, code_n, initial = instrumentation(arm)
        assert_identity(ref, inst)
        require(ref["draws_equal"] and ref["rng_equal"], f"RNG identity failed: {arm}")
        summary["checks"][f"{arm}_instrumented_identity"] = True
        summary["arms"][arm] = bench_arm(ref)
        summary["opportunity"][arm] = opportunity(ref, tape)
        if arm == "gate only":
            gate_ref = ref
        if arm == "H11 full":
            require(gate_ref is not None, "gate-only reference missing")
            departures = b.first_dep(ref, gate_ref)
            max_value_gap = float(np.max(np.abs(ref["KV"]-gate_ref["KV"])))
            require(int((departures >= 0).sum()) == 350, "H11/A0 departure count differs")
            summary["false_identity"] = dict(departing_rows=int((departures >= 0).sum()),
                                             first_departure_step_by_row=departures.tolist(),
                                             max_abs_closed_loop_value_gap=max_value_gap)
            del gate_ref
            gate_ref = None
        replay_vals = {}
        for mode in MODES:
            print(f"  replay {mode}", flush=True)
            pre, post = replay(tape, code_v, code_n, mode, initial if mode == own_mode else None)
            if mode == own_mode:
                require(np.array_equal(pre, ref["KV"]), f"own replay pre-value differs: {arm}")
                require(np.array_equal(post, tape["valence_post"]), f"own replay post-value differs: {arm}")
            replay_vals[mode] = pre
            saved[f"{arm.replace(' ', '_')}_replay_{mode}_pre_value"] = pre
            saved[f"{arm.replace(' ', '_')}_replay_{mode}_post_value"] = post
        summary["donor_replays"][arm] = {
            "own_reproduced": True,
            "pairwise": {f"{x}_vs_{y}": {"first_step_above_1e_12":
                int(np.flatnonzero(np.any(np.abs(replay_vals[x]-replay_vals[y]) > 1e-12, axis=1))[0])
                if np.any(np.abs(replay_vals[x]-replay_vals[y]) > 1e-12) else -1,
                "max_abs_value_difference": float(np.max(np.abs(replay_vals[x]-replay_vals[y]))),
                "sign_inversion_row_steps": int(np.sum(replay_vals[x]*replay_vals[y] < 0))}
                for x, y in (("A0", "A1"), ("A1", "P"), ("A0", "P"))}}
        prefix = arm.replace(" ", "_")
        for key, arr in tape.items():
            if key != "contact":
                saved[f"{prefix}_{key}"] = arr.copy()
        saved[f"{prefix}_contact"] = tape["contact"].copy()
        saved[f"{prefix}_code_V"] = code_v
        saved[f"{prefix}_code_N"] = code_n
        saved[f"{prefix}_good"] = ref["good"].copy()
        saved[f"{prefix}_P2_boundary_weights"] = checkpoint["w"]
        saved[f"{prefix}_P2_boundary_tc"] = checkpoint["tc"]
        saved[f"{prefix}_P2_boundary_tr"] = checkpoint["tr"]
        saved[f"{prefix}_P3_boundary_value"] = p3_end["value"]
        saved[f"{prefix}_P3_boundary_outputs"] = p3_end["outputs"]
        saved[f"{prefix}_P3_boundary_weights"] = p3_end["w"]
        saved[f"{prefix}_P3_boundary_tc"] = p3_end["tc"]
        saved[f"{prefix}_P3_boundary_tr"] = p3_end["tr"]
        saved[f"{prefix}_P1_boundary_acquisition_value"] = acquisition_value
        if arm == "H11 full":
            checkpoint_a1 = checkpoint
            acquisition_a1 = acquisition_value
        del ref, inst, tape, replay_vals
    require(checkpoint_a1 is not None, "A1 checkpoint missing")
    ret = pure_retention(checkpoint_a1)
    summary["retention"] = retention_summary(ret, acquisition_a1)
    summary["checks"]["D0_clones_equal"] = True
    summary["checks"]["zero_code_and_external_reward_retention"] = True
    summary["checks"]["acquisition_weights_invariant"] = all(x["acquisition_invariant"] for x in ret.values())
    for mode, entry in ret.items():
        for d, v in entry["values"].items():
            saved[f"retention_{mode}_D{d}_value"] = v
            saved[f"retention_{mode}_D{d}_outputs"] = entry["outputs"][d]
    for arm in b.ARMS:
        if arm in summary["arms"]:
            continue
        print(f"tabulating original arm {arm}", flush=True)
        traj = (saved["H12_replay_P_pre_value"] if arm == "supplied H12 trajectory" else
                saved["gate_only_replay_A0_pre_value"] if arm == "supplied gate-only trajectory" else None)
        ref = b.run(arm, b.SEEDS["bench"], traj=traj)
        summary["arms"][arm] = bench_arm(ref)
        summary["opportunity"][arm] = opportunity(ref)
        del ref
    require(summary["arms"]["ceiling"]["blocks"][-1]["V"] == 42, "ceiling count differs")
    require(summary["arms"]["floor"]["blocks"][-1]["V"] == 5, "floor count differs")
    require(summary["arms"]["H12"]["blocks"][-1]["V"] == 33, "H12 count differs")
    require(summary["arms"]["gate only"]["blocks"][-1]["V"] == 10, "gate count differs")
    require(summary["arms"]["H12"]["P3_contact_steps_V"] == 4631, "H12 P3 contacts differ")
    require(summary["arms"]["gate only"]["P3_contact_steps_V"] == 4342, "gate P3 contacts differ")
    require(summary["arms"]["H12"]["P3_contact_rows_V"] == 267, "H12 P3 contact rows differ")
    require(summary["arms"]["gate only"]["P3_contact_rows_V"] == 248, "gate P3 contact rows differ")
    summary["checks"]["headline_counts_and_P3_contacts"] = True
    np.savez_compressed(args.output / "events.npz", **saved)
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    lines = ["# H12 Package D diagnosis", "", "Measurement only; no adoption or new behavioural PASS label.", "",
             "The immutable original bench reproduced bytewise. Each instrumented donor reproduced all original fields bitwise.",
             "", "## Original P4 counts", ""]
    for arm in b.ARMS:
        x = summary["arms"][arm]["blocks"][-1]
        lines.append(f"- {arm}: V {x['V']}, N {x['N']}, tie {x['tie']} / 400")
    lines.extend(["", "## P4 opportunity", "",
                  "The ordered partition assigns a row to its first failure stage: no V whiff, "
                  "V whiff without V-supported upwind navigation, V navigation without contact, "
                  "or contact without V dwell majority. Contact or majority can occur despite an earlier "
                  "failure category; the unconditional counts report those overlaps.", ""])
    for arm, x in summary["opportunity"].items():
        lines.append(f"- {arm}: {x['partition']}; filter eligible {x['filter_eligible']}; "
                     f"unconditional V majority {x['V_majority_unconditional']}; "
                     f"zero-contact ties {x['tie_zero']}; positive ties {x['tie_positive']}; "
                     f"flee rows {x['flee_nav_rows']}; both-channel nav rows {x['ambiguous_both_supported_rows']}")
    lines.extend(["", "## Same-input donor replays", ""])
    for arm, x in summary["donor_replays"].items():
        lines.append(f"- {arm}: own module reproduced bitwise; " + "; ".join(
            f"{pair} first >1e-12 at step {v['first_step_above_1e_12']}, "
            f"max |difference| {v['max_abs_value_difference']:.6f}, "
            f"sign-inverted row-steps {v['sign_inversion_row_steps']}"
            for pair, v in x["pairwise"].items()))
    lines.extend(["", "## False A0/A1 identity in the closed loop", "",
                  f"H11 full and gate-only depart on {summary['false_identity']['departing_rows']}/400 rows; "
                  f"maximum V value gap {summary['false_identity']['max_abs_closed_loop_value_gap']:.6f}. "
                  "The donor replays show same-input module differences separately from changed exposure histories.", ""])
    lines.extend(["", "## Pure retention from every A1 P2 checkpoint", ""])
    for d, x in summary["retention"].items():
        lines.append(f"- D={d}: median signed value {x['median_value']:.6f}; positive {x['positive']}; "
                     f"negative {x['negative']}; above competitor {x['above_competitor']}; "
                     f"crossed upward from below {x['crossing_from_below']}")
    lines.extend(["", "## Input contract for proposed Package E", "",
                  "Learning code in this integrated harness comes from V source contact after movement. "
                  "Masking whiffs does not remove that code. Pure retention uses zero code and zero external reinforcement "
                  "while the module clock continues. Package E remains unregistered and unrun.", "",
                  "See summary.json and events.npz for row-level data, replay contrasts, and source provenance.", ""])
    (args.output / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print("Package D complete", flush=True)


if __name__ == "__main__":
    main()
