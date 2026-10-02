#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PACKAGE_ROOT" || exit 1

failures=0

check() {
  local name="$1"
  shift
  if "$@" >/tmp/vcm_check_stdout.$$ 2>/tmp/vcm_check_stderr.$$; then
    echo "PASS $name"
  else
    echo "FAIL $name"
    cat /tmp/vcm_check_stderr.$$ 2>/dev/null
    failures=$((failures + 1))
  fi
  rm -f /tmp/vcm_check_stdout.$$ /tmp/vcm_check_stderr.$$
}

check "OS available" uname -a
check "architecture available" uname -m
check "Python 3 available" python3 --version
check "NumPy import" python3 -c "import numpy; print(numpy.__version__)"
check "SciPy import" python3 -c "import scipy; print(scipy.__version__)"
check "TensorFlow import" python3 -c "import tensorflow as tf; print(tf.__version__)"
check "Tkinter import for GUI" python3 -c "import tkinter"

check "E50 weights" test -f models/cnn/E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT_weights.npz
check "E50 normalization" test -f models/cnn/E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT_normalization.npz
check "E37 weights" test -f models/cnn/E37_TARGETED_COLOR_VOLUME_FIX_weights.npz
check "E37 normalization" test -f models/cnn/E37_TARGETED_COLOR_VOLUME_FIX_normalization.npz
check "E40 policy config" test -f configs/e50_revised_vocab_e40_thresholds.json
check "raw router" test -f actions/raw_command_router.py
check "command actions" test -f actions/command_actions.py
check "response WAV directory" test -d responses_extra_loud_20260929
check "response WAV assets present" python3 - <<'PY'
from pathlib import Path
files = list(Path("responses_extra_loud_20260929").glob("*.wav"))
raise SystemExit(0 if len(files) >= 19 else 1)
PY
check "GUI script present" test -f scripts/vcm_touchscreen_gui.py
check "GUI SHA verified" python3 - <<'PY'
import hashlib
from pathlib import Path
target = "ff8b64759b1efb93d88cc30a7a8f8d1cea7b49924cb72b19bc643c4a746a2c42"
path = Path("scripts/vcm_touchscreen_gui.py")
actual = hashlib.sha256(path.read_bytes()).hexdigest()
print(actual)
raise SystemExit(0 if actual == target else 1)
PY
check "ALSA recording tool visible" bash -lc "command -v arecord"
check "ALSA playback tool visible" bash -lc "command -v aplay"

echo "Diagnostics complete: $failures failure(s)."
exit "$failures"
