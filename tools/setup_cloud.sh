#!/usr/bin/env bash
# Preparation only. No simulation, claim, numerical import or dependency install.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
unset PYTHONOPTIMIZE
python3 -c 'import sys; assert sys.version_info >= (3, 11), "Python 3.11 or newer required"; assert sys.flags.optimize == 0'
python3 tools/check_cloud_readiness.py --sources-only
printf '%s\n' 'Preparation check complete. EVAL remains unopened; execution_ready is false.'
printf '%s\n' 'Set all six numeric thread variables to 1 in persistent environment configuration for later sessions.'
