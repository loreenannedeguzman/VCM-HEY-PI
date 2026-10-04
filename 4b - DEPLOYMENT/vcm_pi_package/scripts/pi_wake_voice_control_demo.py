from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT))
sys.path.insert(0, str(PACKAGE_ROOT / "scripts"))

from actions.command_actions import ActionRequest, execute_action  # noqa: E402
from actions.raw_command_router import RAW_COMMAND_ROUTES, route_raw_command  # noqa: E402
from predict_wav_pi import (  # noqa: E402
    DEFAULT_CNN_CONFIG,
    DEFAULT_EXPERIMENT_ID,
    DEFAULT_THRESHOLD,
    DEFAULT_THRESHOLD_POLICY,
    VcmPredictor,
    predict_wav,
)

DEFAULT_WAKE_EXPERIMENT_ID = "E37_TARGETED_COLOR_VOLUME_FIX"
DEFAULT_COMMAND_EXPERIMENT_ID = "E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT"
DEFAULT_WAKE_THRESHOLD = 0.90
DEFAULT_WAKE_THRESHOLD_POLICY = ""
DEFAULT_COMMAND_THRESHOLD_POLICY = "configs/e50_revised_vocab_e40_thresholds.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Two-stage Pi demo: require a WAKE prediction before command action routing."
    )
    parser.add_argument("--device", default="", help="Optional ALSA device, for example plughw:2,0.")
    parser.add_argument("--sample-rate", type=int, default=16000)
    parser.add_argument("--wake-duration-sec", type=float, default=4.0)
    parser.add_argument("--command-duration-sec", type=float, default=4.0)
    parser.add_argument("--wake-wav", default="pi_recordings/latest_wake.wav")
    parser.add_argument("--command-wav", default="pi_recordings/latest_command_after_wake.wav")
    parser.add_argument(
        "--evidence-dir",
        default="",
        help=(
            "Optional folder for timestamped validation evidence. When set, "
            "the wake WAV, command WAV, and result JSON are saved together."
        ),
    )
    parser.add_argument(
        "--trial-id",
        default="",
        help="Optional readable trial id used with --evidence-dir, for example wake_stop_001.",
    )
    parser.add_argument(
        "--expected-wake",
        default="",
        help="Optional note for the wake phrase that should be spoken in this trial.",
    )
    parser.add_argument(
        "--expected-command",
        default="",
        help="Optional note for the command phrase that should be spoken in this trial.",
    )
    parser.add_argument(
        "--experiment-id",
        default=DEFAULT_EXPERIMENT_ID,
        help=(
            "Backward-compatible default model for both stages. Use "
            "--wake-experiment-id and --command-experiment-id to split the stages."
        ),
    )
    parser.add_argument("--wake-experiment-id", default=DEFAULT_WAKE_EXPERIMENT_ID)
    parser.add_argument("--command-experiment-id", default=DEFAULT_COMMAND_EXPERIMENT_ID)
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    parser.add_argument("--wake-threshold", type=float, default=DEFAULT_WAKE_THRESHOLD)
    parser.add_argument("--command-threshold", type=float, default=None)
    parser.add_argument("--cnn-config", default=DEFAULT_CNN_CONFIG)
    parser.add_argument("--threshold-policy", default=DEFAULT_THRESHOLD_POLICY)
    parser.add_argument("--wake-threshold-policy", default=DEFAULT_WAKE_THRESHOLD_POLICY)
    parser.add_argument("--command-threshold-policy", default=DEFAULT_COMMAND_THRESHOLD_POLICY)
    parser.add_argument("--wake-label", default="WAKE")
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--pin", type=int, default=17)
    parser.add_argument("--enable-gpio", action="store_true")
    parser.add_argument("--enable-local-audio", action="store_true")
    parser.add_argument("--music-dir", default="music")
    parser.add_argument(
        "--cycles",
        type=int,
        default=1,
        help="Number of wake-command cycles to run before exiting. Use 0 with --continuous.",
    )
    parser.add_argument(
        "--continuous",
        action="store_true",
        help="Run persistent wake-command cycles until interrupted. Models are loaded once.",
    )
    parser.add_argument(
        "--wait-for-wake",
        action="store_true",
        help=(
            "Keep recording wake windows until the wake phrase is accepted. "
            "This prevents the command loop from advancing or ending just "
            "because the operator did not speak during one wake window."
        ),
    )
    parser.add_argument(
        "--max-wake-attempts",
        type=int,
        default=0,
        help="Maximum wake windows before rejecting. Use 0 for unlimited with --wait-for-wake.",
    )
    parser.add_argument(
        "--wake-retry-delay-sec",
        type=float,
        default=0.2,
        help="Short pause between rejected wake windows when --wait-for-wake is enabled.",
    )
    parser.add_argument("--response-map", default="configs/demo_response_assets.json")
    parser.add_argument(
        "--enable-response-audio",
        action="store_true",
        help="Play mapped local response WAVs with aplay after action execution.",
    )
    parser.add_argument(
        "--response-audio-device",
        default="",
        help="Optional ALSA device for response WAV playback, for example plughw:0,0.",
    )
    return parser.parse_args()


def safe_trial_id(raw_value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", raw_value.strip())
    return cleaned.strip("._-")


def make_evidence_paths(args: argparse.Namespace) -> tuple[Path, Path, Path | None, str, str]:
    recorded_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    if not args.evidence_dir:
        return (
            PACKAGE_ROOT / args.wake_wav,
            PACKAGE_ROOT / args.command_wav,
            None,
            "",
            recorded_at,
        )

    evidence_dir = PACKAGE_ROOT / args.evidence_dir
    evidence_dir.mkdir(parents=True, exist_ok=True)
    trial_id = safe_trial_id(args.trial_id) if args.trial_id else datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    wake_path = evidence_dir / f"{trial_id}_wake.wav"
    command_path = evidence_dir / f"{trial_id}_command.wav"
    result_path = evidence_dir / f"{trial_id}_result.json"
    return wake_path, command_path, result_path, trial_id, recorded_at


def record_with_arecord(device: str, sample_rate: int, duration_sec: float, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "arecord",
        "-D",
        device,
        "-r",
        str(sample_rate),
        "-c",
        "1",
        "-f",
        "S16_LE",
        "-d",
        str(int(round(duration_sec))),
        str(output_path),
    ]
    if not device:
        command = [item for idx, item in enumerate(command) if not (item == "-D" or idx > 0 and command[idx - 1] == "-D")]
    subprocess.run(command, check=True)


def rejected_payload(
    reason: str,
    wake_result: object,
    command_result: object | None = None,
    *,
    wake_experiment_id: str = "",
    command_experiment_id: str = "",
    evidence: dict[str, object] | None = None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "wake_required": True,
        "status": "rejected",
        "reason": reason,
        "wake_experiment_id": wake_experiment_id,
        "command_experiment_id": command_experiment_id,
        "wake_result": asdict(wake_result),
        "command_result": asdict(command_result) if command_result is not None else None,
        "action_result": None,
        "gpio_requested": False,
    }
    if evidence is not None:
        payload["evidence"] = evidence
    return payload


def emit_payload(payload: dict[str, object], result_path: Path | None) -> None:
    if result_path is not None:
        payload.setdefault("evidence", {})
        evidence = payload["evidence"]
        if isinstance(evidence, dict):
            evidence["result_json"] = str(result_path)
        result_path.parent.mkdir(parents=True, exist_ok=True)
        result_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


def load_response_map(path: str) -> dict[str, str]:
    if not path:
        return {}
    response_path = Path(path)
    if not response_path.is_absolute():
        response_path = PACKAGE_ROOT / response_path
    if not response_path.exists():
        return {}
    with response_path.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    responses = raw.get("responses", raw)
    if not isinstance(responses, dict):
        return {}
    return {str(key): str(value) for key, value in responses.items()}


def response_status(
    raw_label: str,
    response_map: dict[str, str],
    *,
    enabled: bool,
    audio_device: str = "",
) -> dict[str, object]:
    relative_path = response_map.get(raw_label, "")
    if not relative_path:
        return {
            "response_label": raw_label,
            "response_wav": "",
            "wav_exists": False,
            "wav_readable": False,
            "playback_requested": enabled,
            "played": False,
            "reason": "No response WAV mapping exists for this label.",
        }
    wav_path = Path(relative_path)
    if not wav_path.is_absolute():
        wav_path = PACKAGE_ROOT / wav_path
    exists = wav_path.exists()
    readable = exists and wav_path.is_file()
    played = False
    reason = ""
    stderr = ""
    if enabled and readable:
        command = ["aplay", str(wav_path)]
        if audio_device:
            command = ["aplay", "-D", audio_device, str(wav_path)]
        try:
            completed = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            played = completed.returncode == 0
            stderr = (completed.stderr or "").strip()
            if not played:
                reason = f"aplay exited with status {completed.returncode}."
        except (FileNotFoundError, OSError) as exc:
            reason = f"aplay unavailable: {exc}"
    elif enabled and not readable:
        reason = "Mapped response WAV is missing or unreadable."
    return {
        "response_label": raw_label,
        "response_wav": str(wav_path),
        "wav_exists": exists,
        "wav_readable": readable,
        "playback_requested": enabled,
        "playback_device": audio_device,
        "played": played,
        "reason": reason,
        "stderr": stderr,
    }


def run_cycle(
    args: argparse.Namespace,
    *,
    wake_predictor: VcmPredictor,
    command_predictor: VcmPredictor,
    response_map: dict[str, str],
) -> dict[str, object]:
    wake_path, command_path, result_path, trial_id, recorded_at = make_evidence_paths(args)
    wake_experiment_id = args.wake_experiment_id or args.experiment_id
    command_experiment_id = args.command_experiment_id or args.experiment_id
    evidence = {
        "trial_id": trial_id,
        "recorded_at_utc": recorded_at,
        "expected_wake": args.expected_wake,
        "expected_command": args.expected_command,
        "wake_wav": str(wake_path),
    }
    evidence = {key: value for key, value in evidence.items() if value}

    wake_attempt = 0
    wake_result = None
    while True:
        wake_attempt += 1
        if args.wait_for_wake:
            print(f"Wake stage attempt {wake_attempt}: listening for the wake phrase.")
        else:
            print("Wake stage: say the wake phrase.")
        record_with_arecord(args.device, args.sample_rate, args.wake_duration_sec, wake_path)
        wake_result = wake_predictor.predict(wake_path, top_k=args.top_k)

        wake_ok = wake_result.accepted and wake_result.predicted_intent == args.wake_label
        if wake_ok:
            evidence["wake_attempts"] = wake_attempt
            break

        if not args.wait_for_wake:
            payload = rejected_payload(
                "Wake phrase was not accepted; command window stayed closed.",
                wake_result,
                wake_experiment_id=wake_experiment_id,
                command_experiment_id=command_experiment_id,
                evidence=evidence,
            )
            payload["returned_to_listening"] = True
            emit_payload(payload, result_path)
            return payload

        print(
            "Wake not accepted "
            f"(predicted={wake_result.predicted_intent}, "
            f"confidence={wake_result.confidence:.6f}). Still listening."
        )
        if args.max_wake_attempts and wake_attempt >= args.max_wake_attempts:
            evidence["wake_attempts"] = wake_attempt
            payload = rejected_payload(
                "Wake phrase was not accepted within max wake attempts; command window stayed closed.",
                wake_result,
                wake_experiment_id=wake_experiment_id,
                command_experiment_id=command_experiment_id,
                evidence=evidence,
            )
            payload["returned_to_listening"] = True
            emit_payload(payload, result_path)
            return payload
        if args.wake_retry_delay_sec > 0:
            time.sleep(args.wake_retry_delay_sec)

    evidence["command_wav"] = str(command_path)
    print("Wake accepted. Command stage: say one supported command.")
    record_with_arecord(args.device, args.sample_rate, args.command_duration_sec, command_path)
    command_result = command_predictor.predict(command_path, top_k=args.top_k)

    if not command_result.accepted:
        payload = rejected_payload(
            "Command prediction was below threshold after wake; no action taken.",
            wake_result,
            command_result,
            wake_experiment_id=wake_experiment_id,
            command_experiment_id=command_experiment_id,
            evidence=evidence,
        )
        payload["returned_to_listening"] = True
        emit_payload(payload, result_path)
        return payload

    if command_result.predicted_intent in {args.wake_label, "UNKNOWN"}:
        payload = rejected_payload(
            "Post-wake audio was WAKE/UNKNOWN, so no command action was taken.",
            wake_result,
            command_result,
            wake_experiment_id=wake_experiment_id,
            command_experiment_id=command_experiment_id,
            evidence=evidence,
        )
        payload["returned_to_listening"] = True
        emit_payload(payload, result_path)
        return payload

    if command_result.predicted_intent in RAW_COMMAND_ROUTES:
        routed = route_raw_command(
            command_result.predicted_intent,
            confidence=command_result.confidence,
            accepted=command_result.accepted,
            threshold=command_result.threshold,
        )
        action_intent = routed.intent
        action_slots = routed.slots
        action_accepted = routed.accepted
    else:
        routed = None
        action_intent = command_result.predicted_intent
        action_slots = {}
        action_accepted = False

    action_result = execute_action(
        ActionRequest(
            intent=action_intent,
            confidence=command_result.confidence,
            accepted=action_accepted,
            slots=action_slots,
            threshold=command_result.threshold,
        ),
        state_path=PACKAGE_ROOT / "pi_recordings" / "action_state.json",
        enable_gpio=args.enable_gpio,
        gpio_pin=args.pin,
        enable_local_audio=args.enable_local_audio,
        music_dir=PACKAGE_ROOT / args.music_dir,
    )

    payload = {
        "wake_required": True,
        "status": "executed" if action_result.status == "executed" else action_result.status,
        "wake_experiment_id": wake_experiment_id,
        "command_experiment_id": command_experiment_id,
        "evidence": evidence,
        "wake_result": asdict(wake_result),
        "command_result": asdict(command_result),
        "raw_command_label": routed.command_label if routed is not None else command_result.predicted_intent,
        "routed_intent": routed.intent if routed is not None else action_intent,
        "routing_slots": routed.slots if routed is not None else action_slots,
        "routing_reason": routed.reason if routed is not None else "No raw-command route exists.",
        "action_result": asdict(action_result),
        "response_result": response_status(
            routed.command_label if routed is not None else command_result.predicted_intent,
            response_map,
            enabled=args.enable_response_audio,
            audio_device=args.response_audio_device,
        ),
        "gpio_requested": args.enable_gpio,
        "returned_to_listening": True,
    }
    emit_payload(payload, result_path)
    return payload


def main() -> None:
    args = parse_args()
    wake_experiment_id = args.wake_experiment_id or args.experiment_id
    command_experiment_id = args.command_experiment_id or args.experiment_id
    wake_threshold = args.wake_threshold if args.wake_threshold is not None else args.threshold
    command_threshold = args.command_threshold if args.command_threshold is not None else args.threshold
    wake_threshold_policy = (
        args.wake_threshold_policy
        if args.wake_threshold_policy is not None
        else args.threshold_policy
    )
    command_threshold_policy = (
        args.command_threshold_policy
        if args.command_threshold_policy is not None
        else args.threshold_policy
    )
    response_map = load_response_map(args.response_map)
    wake_predictor = VcmPredictor(
        experiment_id=wake_experiment_id,
        cnn_config_path=args.cnn_config,
        threshold=wake_threshold,
        threshold_policy_path=wake_threshold_policy,
    )
    command_predictor = VcmPredictor(
        experiment_id=command_experiment_id,
        cnn_config_path=args.cnn_config,
        threshold=command_threshold,
        threshold_policy_path=command_threshold_policy,
    )
    if args.continuous:
        cycle = 1
        while True:
            cycle_args = argparse.Namespace(**vars(args))
            if args.trial_id:
                cycle_args.trial_id = f"{args.trial_id}_{cycle:03d}"
            run_cycle(
                cycle_args,
                wake_predictor=wake_predictor,
                command_predictor=command_predictor,
                response_map=response_map,
            )
            cycle += 1
            print("Returned to listening. Press Ctrl+C to stop.")
    else:
        cycles = max(1, args.cycles)
        for cycle in range(1, cycles + 1):
            cycle_args = argparse.Namespace(**vars(args))
            if cycles > 1 and args.trial_id:
                cycle_args.trial_id = f"{args.trial_id}_{cycle:03d}"
            run_cycle(
                cycle_args,
                wake_predictor=wake_predictor,
                command_predictor=command_predictor,
                response_map=response_map,
            )
            if cycle < cycles:
                print("Returned to listening. Starting next cycle.")


if __name__ == "__main__":
    main()
