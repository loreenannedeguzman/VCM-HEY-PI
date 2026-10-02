#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PACKAGE_ROOT"

CONFIG_FILE="${VCM_DEPLOYMENT_CONFIG:-$PACKAGE_ROOT/deployment_config.example.json}"

read_json_field() {
  local field="$1"
  python - "$CONFIG_FILE" "$field" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
field = sys.argv[2]
if not path.exists():
    raise SystemExit(0)
try:
    data = json.loads(path.read_text(encoding="utf-8"))
except Exception:
    raise SystemExit(0)
value = data
for part in field.split("."):
    if not isinstance(value, dict) or part not in value:
        raise SystemExit(0)
    value = value[part]
if value is not None:
    print(value)
PY
}

DEV="${DEV:-$(read_json_field audio.input_device)}"
DEV="${DEV:-plughw:2,0}"
RESPONSE_AUDIO_DEVICE="${RESPONSE_AUDIO_DEVICE:-$(read_json_field audio.output_device)}"
RESPONSE_AUDIO_DEVICE="${RESPONSE_AUDIO_DEVICE:-plughw:CARD=vc4hdmi0,DEV=0}"
EVID="${EVID:-pi_validation/e50_runtime_manual_test}"

args=(
  --device "$DEV"
  --evidence-dir "$EVID"
  --wait-for-wake
  --response-audio-device "$RESPONSE_AUDIO_DEVICE"
)

python "$PACKAGE_ROOT/scripts/pi_wake_voice_control_demo.py" "${args[@]}"
