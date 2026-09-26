#!/usr/bin/env python3
"""H12 Package E draft implementation; smoke identities only until registration.

Usage: python src/h12_expression.py smoke --output <directory>

Smoke reuses the already-spent (5, 6) pair. It reports implementation checks,
not a behavioral effect, task readability, or an H12 verdict.
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


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PH36B = "cfb9a26a45bfd5ef9e5d781d73a772e3129db24e633c66eeb89c2d61556f1cef"
SMOKE = (5, 6)


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


def readout(checkpoint, retained, body_seeds, runs):
    """Reset body, transplant memory, keep it frozen for 600-step choice."""
    rows = np.arange(runs)
    w = b.World7(runs, np.random.default_rng(body_seeds[0]), body_seeds[0])
    good, neutral = w.good, 1 - w.good
    values = np.zeros((runs, 2))
    values[rows, good], values[rows, neutral] = retained[1], b.C
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
    o = dict(steps=600, good=good.copy(), cell=w.cell.copy(), **b.ph24.blank(600, runs),
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
                  harness_sha256=sha(__file__), design_sha256=sha(ROOT / "experiments/h12/h12_expression_design_v1.md"))
    (output / "smoke.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("mode", choices=("smoke",))
    cli.add_argument("--output", type=Path, required=True)
    args = cli.parse_args()
    smoke(args.output)
