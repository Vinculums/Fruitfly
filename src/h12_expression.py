#!/usr/bin/env python3
"""H12 Package E controlled expression, registered v2 design.

Usage: python src/h12_expression.py {smoke,calibration,development,evaluation} --output <directory>

Each stage runs on a GitHub-hosted Linux runner. Smoke reuses the spent (5, 6)
pair; the other stages use disjoint registered seeds and preserve raw row data.
"""
import argparse
import gc
import hashlib
import json
import os
import platform
import socket
import sys
from pathlib import Path

import numpy as np

import ph36b as b


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PH36B = "cfb9a26a45bfd5ef9e5d781d73a772e3129db24e633c66eeb89c2d61556f1cef"
SMOKE = (5, 6)
DESIGN = ROOT / "experiments/h12/h12_expression_design_v2.md"
MANIFEST = ROOT / "experiments/h12/h12_expression_manifest.json"
STAGES = {
    "calibration": ((20261281, 20261282), (21261281, 21261282), 20261283),
    "development": ((31011, 31012), (1031011, 1031012), 31013),
    "evaluation": ((71011, 71012), (1071011, 1071012), 71013),
}
NROWS = 400
NBOOT = 5000


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sources():
    require(sha(b.__file__) == EXPECTED_PH36B, "historical Stage 2 source changed")
    require(sha(b.ph36.__file__) == b.PH36_SHA, "historical module source changed")
    require(sha(b.ph36.DESIGN_FILE) == b.DESIGN.split("hash ")[1], "historical design changed")
    for name, digest in b.SHA_ON_RECORD.items():
        require(sha(Path(b.HERE, name + ".py")) == digest, name + " source changed")
    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        require(sha(__file__) == manifest["harness_sha256"], "registered harness changed")
        require(sha(DESIGN) == manifest["design_sha256"], "registered design changed")


def memory_checkpoints(seeds, runs):
    """Original H11-full P1/P2 loop, stopped after the update of step 2399."""
    steps = b.P2E
    rows = np.arange(runs)
    w = b.ph23.Lost(runs, np.random.default_rng(seeds[0]), seeds[0])
    good = w.good
    neutral = 1 - good
    w.pres, w.absent = neutral.copy(), good.copy()
    placeholder = np.zeros((runs, 2))
    placeholder[rows, good], placeholder[rows, neutral] = 1.0, b.C
    rng = np.random.default_rng(seeds[1])
    with b.ph28.pn(b.P_PRIOR, b.N17):
        a = b.ph24.make(b.Agent17, runs, rng, b.G_STAR, placeholder, True, True, True)
    require(type(a) is b.Agent17 and a.N_hi == b.N17, "Agent17 construction changed")
    a.mb = b.MB4(runs, parallel=True, gated=True, rng=a.mb.rng, **b.ph11.MB)
    b.ph29.train(a, good, "trained")
    code_v = a.codes[rows, good].copy()
    code_n = a.codes[rows, neutral].copy()
    a.known = placeholder.copy()
    a.known[rows, good] = a.mb.valence(code_v)
    a.cast_sign = b.cast_draw(seeds[1], runs)
    original = dict(arm="H11 full", good=good.copy(), cell=w.cell.copy(), steps=steps,
                    **b.ph24.blank(steps, runs), POS=np.zeros((steps, runs, 2)),
                    HEAD=np.zeros((steps, runs)), AT2=np.zeros((steps, runs, 2), bool),
                    C=np.zeros((steps, runs), bool), KV=np.zeros((steps, runs)))
    for t in range(steps):
        w.on = False
        pa = (a.sel.s > 1.0).any(1)
        whiff = w.sense()
        wind = w.wind_on()
        a.known = np.zeros((runs, 2))
        a.known[rows, neutral] = b.C
        a.known[rows, good] = a.mb.valence(code_v)
        original["KV"][t] = a.known[rows, good]
        turn, held = a.act(w, whiff, wind)
        b.ph24.record(original, t, a, held, whiff, pa)
        w.move(turn)
        a.bump(w.bumped)
        at = w.at_source()
        original["POS"][t], original["HEAD"][t] = w.pos, w.head
        original["AT2"][t], original["C"][t] = at, w.bumped
        at_v = at[rows, good]
        reward = np.zeros((runs, a.mb.C))
        if t < b.P1:
            reward[:, 1] = at_v
        a.mb.step(code=code_v * at_v[:, None], reinf=reward)
    checkpoint = dict(w=a.mb.w.copy(), tc=a.mb.tc.copy(), tr=a.mb.tr.copy(),
                      code_v=code_v, code_n=code_n,
                      value=a.mb.valence(code_v).copy(), good=good.copy())
    return checkpoint, original


def same_original(seeds, runs, observed):
    ref = b.run("H11 full", seeds, runs=runs, steps=b.P2E)
    require(np.array_equal(ref["good"], observed["good"]) and
            np.array_equal(ref["cell"], observed["cell"]), "checkpoint row identity differs")
    for key in b.KEYS:
        require(np.array_equal(ref[key], observed[key]), "checkpoint loop differs: " + key)
    return len(b.KEYS)


def retain(checkpoint, duration, decay):
    n = len(checkpoint["good"])
    rng = np.random.default_rng(0)  # MB constructor makes no draw; copied state is authoritative.
    mb = (b.MB5(n, parallel=True, gated=True, tau=(None, None, b.TAU, b.TAU),
                rng=rng, **b.ph11.MB) if decay else
          b.MB4(n, parallel=True, gated=True, rng=rng, **b.ph11.MB))
    for key in ("w", "tc", "tr"):
        getattr(mb, key)[:] = checkpoint[key]
    acq = mb.w[:, :2].copy()
    for _ in range(duration):
        mb.step(code=None, reinf=None)
    require(np.array_equal(acq, mb.w[:, :2]), "acquisition weights changed during silence")
    return mb, mb.valence(checkpoint["code_v"])


def readout(checkpoint, retained, body_seeds, runs, supplied_v=None):
    """Reset body, transplant memory, keep it frozen for 600-step choice."""
    rows = np.arange(runs)
    w = b.World7(runs, np.random.default_rng(body_seeds[0]), body_seeds[0])
    good, neutral = w.good, 1 - w.good
    values = np.zeros((runs, 2))
    values[rows, good] = retained[1] if supplied_v is None else supplied_v
    values[rows, neutral] = b.C
    rng = np.random.default_rng(body_seeds[1])
    with b.ph28.pn(b.P_PRIOR, b.N17):
        a = b.ph24.make(b.Agent17, runs, rng, b.G_STAR, values, True, True, True)
    a.mb = retained[0]
    # The reset body's odor labels are mapped to the valued and neutral memory codes.
    a.codes[rows, good] = checkpoint["code_v"]
    a.codes[rows, neutral] = checkpoint["code_n"]
    a.known = values.copy()
    a.cast_sign = b.cast_draw(body_seeds[1], runs)
    require(np.array_equal(a.mb.valence(a.codes[rows, good]), retained[1]),
            "memory transfer changed V read-out")
    frozen = (a.mb.w.copy(), a.mb.tc.copy(), a.mb.tr.copy(), a.codes.copy())
    o = dict(steps=600, good=good.copy(), cell=w.cell.copy(),
             start_pos=w.pos.copy(), start_head=w.head.copy(), **b.ph24.blank(600, runs),
             POS=np.zeros((600, runs, 2)), HEAD=np.zeros((600, runs)),
             AT2=np.zeros((600, runs, 2), bool), C=np.zeros((600, runs), bool),
             KV=np.zeros((600, runs)), calls=0)
    for t in range(600):
        pa = (a.sel.s > 1.0).any(1)
        whiff = w.sense()
        wind = w.wind_on()
        a.known = values.copy()
        o["KV"][t] = a.known[rows, good]
        turn, held = a.act(w, whiff, wind)
        b.ph24.record(o, t, a, held, whiff, pa)
        w.move(turn)
        a.bump(w.bumped)
        o["POS"][t], o["HEAD"][t] = w.pos, w.head
        o["AT2"][t], o["C"][t] = w.at_source(), w.bumped
    require(o["calls"] == 0 and all(np.array_equal(getattr(a.mb, key), old)
            for key, old in zip(("w", "tc", "tr"), frozen[:3])) and
            np.array_equal(a.codes, frozen[3]), "read-out modified the frozen memory")
    return o


def smoke(output):
    sources()
    require(os.environ.get("RUNNER_ENVIRONMENT") == "github-hosted" and
            platform.system() == "Linux", "smoke must run on a GitHub-hosted Linux runner")
    n = 40
    checkpoint, observed = memory_checkpoints(SMOKE, n)
    fields_checked = same_original(SMOKE, n, observed)
    off0, v_off0 = retain(checkpoint, 0, False)
    on0, v_on0 = retain(checkpoint, 0, True)
    require(np.array_equal(v_off0, v_on0), "D=0 values differ")
    require(all(np.array_equal(getattr(off0, key), getattr(on0, key))
                for key in ("w", "tc", "tr")), "D=0 clone states differ")
    body_seeds = SMOKE  # Reused smoke pair; no candidate E seed is spent.
    first = readout(checkpoint, (off0, v_off0), body_seeds, n)
    second = readout(checkpoint, (on0, v_on0), body_seeds, n)
    identity_fields = ("good", "cell", *b.KEYS)
    for key in identity_fields:
        require(np.array_equal(first[key], second[key]), "D=0 read-out differs: " + key)
    # Exercise the proposed retention endpoint as an implementation path only.
    on5000, value5000 = retain(checkpoint, 5000, True)
    acquisition = b.MB4(n, parallel=True, gated=True,
                        rng=np.random.default_rng(0), **b.ph11.MB)
    acquisition.w[:], acquisition.tc[:], acquisition.tr[:] = (checkpoint[k] for k in ("w", "tc", "tr"))
    acq = acquisition.out(checkpoint["code_v"])[:, 0] - acquisition.out(checkpoint["code_v"])[:, 1]
    par = acquisition.out(checkpoint["code_v"])[:, 2] - acquisition.out(checkpoint["code_v"])[:, 3]
    expected = acq + par * (1.0 - 1.0 / b.TAU)**5000
    require(np.max(np.abs(value5000 - expected)) < 1e-10, "retention analytic identity failed")
    third = readout(checkpoint, (on5000, value5000), body_seeds, n)
    require(third["calls"] == 0, "read-out called the module")
    output.mkdir(parents=True, exist_ok=True)
    result = dict(status="SMOKE_ONLY_NO_BEHAVIORAL_VERDICT", rows=n, checkpoint_seed_pair=SMOKE,
                  readout_seed_pair=body_seeds, original_field_identity_count=fields_checked,
                  D0_readout_identity_count=len(identity_fields), D0_clone_identity=True,
                  D5000_analytic_max_abs_error=float(np.max(np.abs(value5000 - expected))),
                  readout_module_calls=0, model="gpt-6-sol", platform=platform.platform(),
                  hostname=socket.gethostname(), runner_environment=os.environ["RUNNER_ENVIRONMENT"],
                  python=sys.version, numpy=np.__version__, historical_ph36b_sha256=sha(b.__file__),
                  harness_sha256=sha(__file__), design_sha256=sha(DESIGN))
    (output / "smoke.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


def row_readout(o):
    n = len(o["good"])
    rows = np.arange(n)
    v = o["AT2"][:, rows, o["good"]].sum(0)
    neutral = o["AT2"][:, rows, 1 - o["good"]].sum(0)
    return dict(dwell_v=v, dwell_n=neutral, v_majority=v > neutral,
                n_majority=neutral > v, tie=v == neutral,
                zero_contact=(v == 0) & (neutral == 0))


def interval(x, draws):
    values = np.asarray(x, float)[draws].mean(1)
    return [float(np.percentile(values, q)) for q in (2.5, 97.5)]


def side_interval(x, side, draws):
    chosen = side[draws]
    denom = chosen.sum(1)
    require(bool(np.all(denom)), "bootstrap draw has empty valued-side stratum")
    samples = (x[draws] * chosen).sum(1) / denom
    return [float(np.percentile(samples, q)) for q in (2.5, 97.5)]


def components(mb, code_v):
    out = mb.out(code_v)
    return out[:, 0] - out[:, 1], out[:, 2] - out[:, 3]


def run_stage(stage, output):
    sources()
    require(os.environ.get("RUNNER_ENVIRONMENT") == "github-hosted" and
            platform.system() == "Linux", "registered run requires GitHub-hosted Linux")
    require(MANIFEST.exists(), "registered hash manifest missing")
    checkpoint_seeds, body_seeds, bootstrap_seed = STAGES[stage]
    output.mkdir(parents=True, exist_ok=True)
    checkpoint, observed = memory_checkpoints(checkpoint_seeds, NROWS)
    fields_checked = same_original(checkpoint_seeds, NROWS, observed)
    np.savez_compressed(output / "checkpoint.npz", **checkpoint,
                        original_good=observed["good"], original_cell=observed["cell"],
                        original_at2=observed["AT2"], original_kv=observed["KV"])
    checkpoint_cell = observed["cell"].copy()
    del observed
    gc.collect()

    # Reuse a single 400-row index matrix for every registered interval.
    draws = np.random.default_rng(bootstrap_seed).integers(0, NROWS, size=(NBOOT, NROWS))
    off0, val_off0 = retain(checkpoint, 0, False)
    on0, val_on0 = retain(checkpoint, 0, True)
    require(np.array_equal(val_off0, val_on0) and all(
        np.array_equal(getattr(off0, key), getattr(on0, key))
        for key in ("w", "tc", "tr")), "D0 module clone identity failed")

    arms = {}
    metrics = {}
    retention = {}
    baseline = None
    for delay in (0, 1200, 5000):
        for state in ("off", "on"):
            mb, value = ((off0, val_off0) if delay == 0 and state == "off" else
                         (on0, val_on0) if delay == 0 else
                         retain(checkpoint, delay, state == "on"))
            key = f"D{delay}_{state}"
            acq, par = components(mb, checkpoint["code_v"])
            retention[key] = dict(value=value, acq=acq, par=par,
                                  weights=mb.w.copy(), tc=mb.tc.copy(), tr=mb.tr.copy())
            if state == "on" and delay:
                expected = retention["D0_off"]["acq"] + retention["D0_off"]["par"] * (1 - 1 / b.TAU) ** delay
                require(float(np.max(np.abs(value - expected))) < 1e-10,
                        f"D{delay} analytic value identity failed")
            o = readout(checkpoint, (mb, value), body_seeds, NROWS)
            if baseline is None:
                baseline = o
            else:
                for field in ("good", "cell", "start_pos", "start_head"):
                    require(np.array_equal(o[field], baseline[field]),
                            f"{key} initial body/world field differs: {field}")
            if delay == 0 and state == "on":
                for field in ("good", "cell", *b.KEYS):
                    require(np.array_equal(o[field], baseline[field]),
                            "D0 read-out field differs: " + field)
            metrics[key] = row_readout(o)
            np.savez_compressed(output / f"trajectory_{key}.npz",
                                good=o["good"], cell=o["cell"], at2=o["AT2"],
                                p2=o["P2"], kv=o["KV"], pos=o["POS"], head=o["HEAD"])
            arms[key] = dict(v_majority=float(metrics[key]["v_majority"].mean()),
                             n_majority=float(metrics[key]["n_majority"].mean()),
                             ties=float(metrics[key]["tie"].mean()))
            print(f"{stage} {key}: {arms[key]}", flush=True)

    for key, supplied in (("supplied_high", 1.0), ("supplied_low", 0.45),
                          ("supplied_equal", 0.5)):
        o = readout(checkpoint, (off0, val_off0), body_seeds, NROWS, supplied_v=supplied)
        for field in ("good", "cell", "start_pos", "start_head"):
            require(np.array_equal(o[field], baseline[field]),
                    f"{key} initial body/world field differs: {field}")
        metrics[key] = row_readout(o)
        np.savez_compressed(output / f"trajectory_{key}.npz",
                            good=o["good"], cell=o["cell"], at2=o["AT2"],
                            p2=o["P2"], kv=o["KV"], pos=o["POS"], head=o["HEAD"])
        arms[key] = dict(v_majority=float(metrics[key]["v_majority"].mean()),
                         n_majority=float(metrics[key]["n_majority"].mean()),
                         ties=float(metrics[key]["tie"].mean()))
        print(f"{stage} {key}: {arms[key]}", flush=True)

    for key, data in metrics.items():
        require(bool(np.all(data["v_majority"].astype(int) +
                            data["n_majority"].astype(int) + data["tie"].astype(int) == 1)),
                f"{key} outcome partition invalid")
        require(bool(np.all(data["dwell_v"] <= 600) and np.all(data["dwell_n"] <= 600)),
                f"{key} dwell invalid")
    require(all(bool(np.isfinite(values[field]).all())
                for values in retention.values() for field in ("value", "acq", "par")),
            "retention has missing or non-finite values")
    side = baseline["good"]
    require(bool(np.any(side == 0)) and bool(np.any(side == 1)), "valued side not balanced")
    primary_diff = metrics["D5000_on"]["v_majority"].astype(float) - metrics["D5000_off"]["v_majority"]
    supplied_diff = metrics["supplied_high"]["v_majority"].astype(float) - metrics["supplied_low"]["v_majority"]
    primary_ci = interval(primary_diff, draws)
    supplied_ci = interval(supplied_diff, draws)
    high_ci = interval(metrics["supplied_high"]["v_majority"], draws)
    tie_ci = {key: interval(data["tie"], draws) for key, data in metrics.items()}
    equal_side_ci = {str(i): side_interval(metrics["supplied_equal"]["v_majority"], side == i, draws)
                     for i in (0, 1)}
    readable = (supplied_ci[0] >= 0.30 and high_ci[0] >= 0.70 and
                all(ci[1] <= 0.20 for ci in tie_ci.values()) and
                all(ci[0] >= 0.35 and ci[1] <= 0.65 for ci in equal_side_ci.values()))
    verdict = ("UNREADABLE" if not readable else
               "EFFECT_ABOVE_BAR" if primary_ci[0] >= 0.10 else
               "BELOW_BAR" if primary_ci[1] < 0.10 else "INCONCLUSIVE")

    r0, r12, r50 = (retention[f"D{d}_on"] for d in (0, 1200, 5000))
    rank0, rank12, rank50 = (r["value"] > b.C for r in (r0, r12, r50))
    value_change = r50["value"] - retention["D5000_off"]["value"]
    rows = []
    for i in range(NROWS):
        record = dict(row=i, checkpoint_good=int(checkpoint["good"][i]),
                      readout_good=int(side[i]), checkpoint_cell=int(checkpoint_cell[i]),
                      readout_cell=int(baseline["cell"][i]),
                      negative_acquisition=bool(r0["acq"][i] < 0),
                      acquisition=float(r0["acq"][i]), parallel=float(r0["par"][i]),
                      rank_cross_1200=bool(rank0[i] != rank12[i]),
                      rank_cross_5000=bool(rank0[i] != rank50[i]))
        for key, values in retention.items():
            record[key] = dict(value=float(values["value"][i]),
                               acquisition=float(values["acq"][i]),
                               parallel=float(values["par"][i]))
        for key, data in metrics.items():
            record[key + "_choice"] = dict(dwell_v=int(data["dwell_v"][i]),
                                            dwell_n=int(data["dwell_n"][i]),
                                            v_majority=bool(data["v_majority"][i]),
                                            n_majority=bool(data["n_majority"][i]),
                                            tie=bool(data["tie"][i]),
                                            zero_contact=bool(data["zero_contact"][i]))
        rows.append(record)
    (output / "rows.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    summary = dict(stage=stage, status=verdict, task_readable=readable, rows=NROWS,
                   checkpoint_seed_pair=checkpoint_seeds, readout_seed_pair=body_seeds,
                   bootstrap_seed=bootstrap_seed, bootstrap_resamples=NBOOT,
                   checkpoint_field_identity_count=fields_checked,
                   D0_readout_identity_count=len(("good", "cell", *b.KEYS)),
                   readout_module_calls=0, arms=arms,
                   primary_effect=dict(point=float(primary_diff.mean()), ci95=primary_ci),
                   supplied_high_minus_low=dict(point=float(supplied_diff.mean()), ci95=supplied_ci),
                   supplied_high_v_majority_ci95=high_ci,
                   tie_ci95=tie_ci, equal_side_v_majority_ci95=equal_side_ci,
                   valued_side_counts={str(i): int((side == i).sum()) for i in (0, 1)},
                   negative_acquisition_count=int((r0["acq"] < 0).sum()),
                   rank_crossing_1200_count=int((rank0 != rank12).sum()),
                   rank_crossing_5000_count=int((rank0 != rank50).sum()),
                   rank_crossing_5000_above_to_below=int((rank0 & ~rank50).sum()),
                   rank_crossing_5000_below_to_above=int((~rank0 & rank50).sum()),
                   value_change_positive_count=int((value_change > 0).sum()),
                   value_change_negative_count=int((value_change < 0).sum()),
                   value_change_zero_count=int((value_change == 0).sum()),
                   model="gpt-6-sol", platform=platform.platform(),
                   hostname=socket.gethostname(), runner_environment=os.environ["RUNNER_ENVIRONMENT"],
                   python=sys.version, numpy=np.__version__,
                   historical_ph36b_sha256=sha(b.__file__), harness_sha256=sha(__file__),
                   design_sha256=sha(DESIGN), manifest_sha256=sha(MANIFEST))
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("mode", choices=("smoke", *STAGES))
    cli.add_argument("--output", type=Path, required=True)
    args = cli.parse_args()
    if args.mode == "smoke":
        smoke(args.output)
    else:
        run_stage(args.mode, args.output)
