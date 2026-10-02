#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PACKAGE_ROOT"

VENV_DIR="${VCM_VENV_DIR:-.venv}"

python3 -m venv "$VENV_DIR"
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip
python -m pip install -r requirements_pi.txt

python - <<'PY'
import numpy
import scipy
print("NumPy", numpy.__version__)
print("SciPy", scipy.__version__)
try:
    import tensorflow as tf
    print("TensorFlow", tf.__version__)
except Exception as exc:
    print("TensorFlow import failed:", exc)
    raise
PY

bash scripts/check_vcm_pi.sh
