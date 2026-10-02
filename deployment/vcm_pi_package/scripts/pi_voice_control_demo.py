from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT))
sys.path.insert(0, str(PACKAGE_ROOT / "scripts"))

from actions.command_actions import ActionRequest, execute_action  # noqa: E402
from actions.raw_command_router import RAW_COMMAND_ROUTES, route_raw_command  # noqa: E402
from predict_wav_pi import (  # noqa: E402
    DEFAULT_EXPERIMENT_ID,
    DEFAULT_THRESHOLD,
    DEFAULT_THRESHOLD_POLICY,
    predict_wav,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Record a Pi microphone command with arecord, classify it with the CNN, "
            "and optionally drive an LED for controlled validation."
        )
    )
    parser.add_argument("--duration-sec", type=float, default=4.0)
    parser.add_argument("--sample-rate", type=int, default=16000)
    parser.add_argument("--device", default="", help="Optional ALSA device, for example plughw:1,0.")
    parser.add_argument("--output-wav", default="pi_recordings/latest_command.wav")
    parser.add_argument("--experiment-id", default=DEFAULT_EXPERIMENT_ID)
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    parser.add_argument(
        "--threshold-policy",
        default=DEFAULT_THRESHOLD_POLICY,
        help=(
            "Optional JSON policy with per-label thresholds. When omitted, the "
            "global --threshold value is used."
        ),
    )
    parser.add_argument("--pin", type=int, default=17, help="BCM GPIO pin for LED.")
    parser.add_argument(
        "--phrase",
        default="",
        help="Optional phrase text for controlled slot parsing, for example 'turn on the light'.",
    )
    parser.add_argument(
        "--slot",
        action="append",
        default=[],
        help="Optional slot override such as light_action=on or brightness_percent=10.",
    )
    parser.add_argument(
        "--light-action",
        choices=["none", "on", "off", "toggle", "blink"],
        default="none",
        help=(
            "GPIO action to apply only when LIGHT_CONTROL is accepted. Keep this as "
            "'none' for microphone validation."
        ),
    )
    parser.add_argument(
        "--enable-gpio",
        action="store_true",
        help="Actually control GPIO. Without this flag the script is prediction-only.",
    )
    parser.add_argument(
        "--enable-local-audio",
        action="store_true",
        help="Allow PLAY_MUSIC/MEDIA_CONTROL handlers to play local WAV files with aplay.",
    )
    parser.add_argument("--music-dir", default="music", help="Folder of local WAV files.")
    return parser.parse_args()


def record_with_arecord(args: argparse.Namespace, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "arecord",
        "-D",
        args.device,
        "-r",
        str(args.sample_rate),
        "-c",
        "1",
        "-f",
        "S16_LE",
        "-d",
        str(int(round(args.duration_sec))),
        str(output_path),
    ]
    if not args.device:
        command = [item for idx, item in enumerate(command) if not (item == "-D" or idx > 0 and command[idx - 1] == "-D")]
    subprocess.run(command, check=True)


def main() -> None:
    args = parse_args()
    output_path = PACKAGE_ROOT / args.output_wav
    record_with_arecord(args, output_path)

    result = predict_wav(
        output_path,
        experiment_id=args.experiment_id,
        threshold=args.threshold,
        threshold_policy_path=args.threshold_policy,
        top_k=3,
    )
    slot_overrides = {}
    for raw_slot in args.slot:
        key, value = raw_slot.split("=", 1)
        slot_overrides[key] = value
    if args.light_action != "none":
        slot_overrides["light_action"] = args.light_action

    if result.predicted_intent in RAW_COMMAND_ROUTES:
        routed = route_raw_command(
            result.predicted_intent,
            confidence=result.confidence,
            accepted=result.accepted,
            threshold=result.threshold,
            slot_overrides=slot_overrides,
        )
        action_intent = routed.intent
        action_accepted = routed.accepted
        action_slots = routed.slots
    else:
        routed = None
        action_intent = result.predicted_intent
        action_accepted = result.accepted
        action_slots = slot_overrides

    action_result = execute_action(
        ActionRequest(
            intent=action_intent,
            confidence=result.confidence,
            accepted=action_accepted,
            phrase=args.phrase,
            slots=action_slots,
            threshold=result.threshold,
        ),
        state_path=PACKAGE_ROOT / "pi_recordings" / "action_state.json",
        enable_gpio=args.enable_gpio,
        gpio_pin=args.pin,
        enable_local_audio=args.enable_local_audio,
        music_dir=PACKAGE_ROOT / args.music_dir,
    )
    payload = asdict(result)
    if routed is not None:
        payload["raw_command_label"] = routed.command_label
        payload["routed_intent"] = routed.intent
        payload["routing_slots"] = routed.slots
        payload["routing_reason"] = routed.reason
    payload["action_result"] = asdict(action_result)
    payload["gpio_requested"] = args.enable_gpio

    print(json.dumps(payload, indent=2))
    if action_intent == "LIGHT_CONTROL" and action_result.status == "needs_slot":
        print(
            "Note: LIGHT_CONTROL needs a light_action slot such as on, off, "
            "toggle, or blink before GPIO can be applied."
        )


if __name__ == "__main__":
    main()
