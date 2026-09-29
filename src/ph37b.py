#!/usr/bin/env python3
"""H18 Stage A: ring_sep against ring aggregates (design v2 section 8), read from the stored per-agent arrays.

Usage: python src/ph37b.py  > experiments/h18/ph37_sep_aggregates.txt

Read-only. It loads the per-agent arrays that src/ph37.py wrote for `ring` and `ring_sep`
(experiments/h18/arrays/<arm>.npz, keys o_*) and prints them with ph12b.describe2 and ph9.compare,
unchanged. The readings pass of ph37.py did not print these aggregates, which section 8 registers as
printed beside ring's. The logic is the scratchpad script that first produced this output, moved into
the repository unchanged, with the header ph37.py uses.
"""
import sys, os, hashlib, platform
sys.stdout.reconfigure(newline="\n")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
REGISTERED = dict(ph12b="ec6b1896", ph12="e1035e09", ph10="de93f177", ph11="e80f40bd", ph9="7699b4e6",
                  ph3="0b43d6f3", ph12c="bacf065f")
import ph12b
from ph9 import compare
from ph12 import last, absorbed, med


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


print(f"== ring_sep vs ring aggregates (design v2 section 8), from the stored per-agent arrays; python {platform.python_version()} numpy {np.__version__} ==")
print(f"   platform {platform.platform()}; src/ph37b.py sha256 {sha(os.path.abspath(__file__))}")
bad = []
for name, m in sorted(sys.modules.items()):
    f = getattr(m, "__file__", None)
    if not f or os.path.dirname(os.path.abspath(f)) != HERE or name == "__main__": continue
    h = sha(f); reg = REGISTERED.get(name)
    tag = "" if reg is None else f"  registered {reg}: {'ok' if h.startswith(reg) else 'MISMATCH'}"
    print(f"   imported src/{name}.py sha256 {h}{tag}")
    if reg and not h.startswith(reg): bad.append(name)
if bad: print(f"STOP: imported source does not match the design header: {bad}"); sys.exit(2)
print(f"   BLAS threads: OPENBLAS {os.environ.get('OPENBLAS_NUM_THREADS')} OMP {os.environ.get('OMP_NUM_THREADS')} MKL {os.environ.get('MKL_NUM_THREADS')}")
K = ("score","whiff","wall","contact","events","gaps","wallfree","err","err_off","abs_off","mismatch","lost_end")
O = {}
for a in ("ring", "ring_sep"):
    p = os.path.join(ROOT, "experiments", "h18", "arrays", f"{a}.npz")
    print(f"   experiments/h18/arrays/{a}.npz sha256 {sha(p)}")
    Z = np.load(p); O[a] = {k: (Z['o_'+k] if Z['o_'+k].ndim else Z['o_'+k].item()) for k in K}
for a in ("ring", "ring_sep"): ph12b.describe2(a, O[a], 0.0, False)
for a in ("ring", "ring_sep"):
    print(f"   {a}: last-third median {med(last(O[a])):.1f}, late unrecovered {absorbed(O[a])*100:.1f}% of 200, lost at end {O[a]['lost_end'].mean()*100:.1f}%")
compare(last(O["ring_sep"]), last(O["ring"]), "ring_sep vs ring, last third (reported)")
