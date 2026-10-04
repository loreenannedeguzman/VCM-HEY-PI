#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

DEV="${DEV:-plughw:2,0}"
EVID="${EVID:-pi_validation/e50_bn_close_touchscreen_gui_20260929}"
RESPONSE_AUDIO_DEVICE="${RESPONSE_AUDIO_DEVICE:-plughw:CARD=vc4hdmi0,DEV=0}"
VCM_WAIT_FOR_WAKE="${VCM_WAIT_FOR_WAKE:-1}"
VCM_MAX_WAKE_ATTEMPTS="${VCM_MAX_WAKE_ATTEMPTS:-0}"
VCM_WAKE_RETRY_DELAY_SEC="${VCM_WAKE_RETRY_DELAY_SEC:-0.2}"

args=(
  --device "$DEV"
  --evidence-dir "$EVID"
  --max-wake-attempts "$VCM_MAX_WAKE_ATTEMPTS"
  --wake-retry-delay-sec "$VCM_WAKE_RETRY_DELAY_SEC"
)

if [[ "$VCM_WAIT_FOR_WAKE" != "0" ]]; then
  args+=(--wait-for-wake)
else
  args+=(--no-wait-for-wake)
fi

if [[ -n "$RESPONSE_AUDIO_DEVICE" ]]; then
  args+=(--response-audio-device "$RESPONSE_AUDIO_DEVICE")
fi

python scripts/vcm_touchscreen_gui.py "${args[@]}"
