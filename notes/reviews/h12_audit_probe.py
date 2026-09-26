"""Read-only, deterministic H12 audit instruments; not a hypothesis evaluation.

Uses the already-used smoke code seed 5. No task, bench, development or evaluation
seeds are consumed. Imports frozen modules; writes only the requested JSON report.
Schedules are fixed here before execution: H11 forward pairing; 30 simultaneous
reward/code steps followed by 60 code-only steps, with two diagnostic interventions
(clear eligibility traces at withdrawal; remove potentiation throughout).
"""
from pathlib import Path
import hashlib
import json
import platform
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
import numpy as np
from ph4 import pairing
from ph8 import MB4


def models(eta_p=0.30):
    kw = dict(runs=1, K=200, C=4, sparsity=0.05, eta_d=0.10,
              eta_p=eta_p, beta=0.15, gated=True)
    return MB4(parallel=False, **kw), MB4(parallel=True, **kw)


def withdrawal(clear=False, eta_p=0.30):
    a, b = models(eta_p)
    code = a.odour(5)
    reward = np.array([[0.0, 1.0, 0.0, 0.0]])
    for _ in range(30):
        for m in (a, b):
            m.step(code=code, reinf=reward)
    trained = [float(m.valence(code)[0]) for m in (a, b)]
    if clear:
        for m in (a, b):
            m.tc.fill(0)
            m.tr.fill(0)
    values = []
    for t in range(60):
        for m in (a, b):
            m.step(code=code)
        values.append([float(m.valence(code)[0]) for m in (a, b)])
    v = np.asarray(values)
    delta = np.abs(v[:, 0] - v[:, 1])
    ii = np.flatnonzero(delta > 1e-12)
    return dict(trained=trained, clear_traces=clear, eta_p=eta_p,
                first_difference_over_1e_minus_12=None if not len(ii) else int(ii[0]),
                max_abs_difference=float(delta.max()),
                minimum_values=v.min(0).tolist(), values_after_each_code_only_step=values)


def forward():
    a, b = models()
    code = a.odour(5)
    for _ in range(10):
        for m in (a, b):
            pairing(m, code, 1)
    samples = []
    for _ in range(20):
        for m in (a, b):
            pairing(m, code, None)
        samples.append([float(m.valence(code)[0]) for m in (a, b)])
    v = np.asarray(samples)
    return dict(max_abs_difference_at_pair_boundaries=float(np.abs(v[:, 0]-v[:, 1]).max()),
                values_at_pair_boundaries=samples)


def main():
    hashes = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
              for p in ("src/ph4.py", "src/ph8.py", "src/ph15.py", "src/ph36.py", "src/ph36b.py")}
    result = dict(scope="deterministic instrument check only; no behavioural result or adoption",
                  baseline_ref="6870b4d7e50629b5362ab40454251ef94183bd83",
                  python=platform.python_version(), numpy=np.__version__, source_sha256=hashes,
                  probe_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  forward_pairing=forward(), simultaneous_withdrawal=withdrawal(),
                  clear_trace_intervention=withdrawal(clear=True),
                  zero_potentiation_intervention=withdrawal(eta_p=0),
                  pure_decay_fraction={str(d): 1-(1-1/5000)**d for d in (1200, 1800, 5000)})
    output = Path(__file__).with_name("h12_audit_probe_result.json")
    output.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8", newline="\n")
    for key in ("forward_pairing", "simultaneous_withdrawal", "clear_trace_intervention", "zero_potentiation_intervention"):
        print(key, {k: v for k, v in result[key].items() if not k.startswith("values_")})
    print("pure_decay_fraction", result["pure_decay_fraction"])
    print("saved", output)


if __name__ == "__main__":
    main()
