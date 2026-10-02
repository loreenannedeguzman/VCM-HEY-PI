from __future__ import annotations

import argparse
import json
import os
import queue
import signal
import subprocess
import sys
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import ttk


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Touchscreen start/stop controller for the offline VCM runtime."
    )
    parser.add_argument("--device", default=os.environ.get("DEV", "plughw:2,0"))
    parser.add_argument(
        "--response-audio-device",
        default=os.environ.get("RESPONSE_AUDIO_DEVICE", ""),
    )
    parser.add_argument(
        "--evidence-dir",
        default=os.environ.get("EVID", "pi_validation/e50_bn_close_touchscreen_gui_20260929"),
    )
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--enable-gpio", action="store_true")
    parser.add_argument(
        "--wait-for-wake",
        action=argparse.BooleanOptionalAction,
        default=os.environ.get("VCM_WAIT_FOR_WAKE", "1") not in {"0", "false", "False"},
        help="Keep recording wake windows until WAKE is accepted before opening a command window.",
    )
    parser.add_argument(
        "--max-wake-attempts",
        type=int,
        default=int(os.environ.get("VCM_MAX_WAKE_ATTEMPTS", "0")),
        help="Maximum wake attempts per cycle; 0 means unlimited.",
    )
    parser.add_argument(
        "--wake-retry-delay-sec",
        type=float,
        default=float(os.environ.get("VCM_WAKE_RETRY_DELAY_SEC", "0.2")),
    )
    parser.add_argument("--poll-ms", type=int, default=1000)
    return parser.parse_args()


class VcmTouchscreenGui:
    def __init__(self, root: tk.Tk, args: argparse.Namespace) -> None:
        self.root = root
        self.args = args
        self.process: subprocess.Popen[str] | None = None
        self.last_result_path: Path | None = None
        self.output_queue: queue.Queue[str] = queue.Queue()
        self.instruction_hold_until = 0.0

        root.title("VCM")
        root.geometry("480x320")
        root.minsize(420, 280)

        self.state_var = tk.StringVar(value="WAKE ME UP")
        self.status_var = tk.StringVar(value='Say "hey pi"')
        self.last_command_var = tk.StringVar(value="--")
        self.last_action_var = tk.StringVar(value="--")
        self.response_var = tk.StringVar(value="--")
        self.system_var = tk.StringVar(value="OFFLINE")

        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.poll_runtime()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=18)
        frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        state = ttk.Label(frame, textvariable=self.state_var, font=("TkDefaultFont", 24, "bold"), wraplength=430)
        state.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 4))

        status = ttk.Label(frame, textvariable=self.status_var, font=("TkDefaultFont", 15), wraplength=430)
        status.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 14))

        self.start_button = ttk.Button(frame, text="START LISTENING", command=self.start_runtime)
        self.start_button.grid(row=2, column=0, sticky="ew", padx=(0, 8), pady=(0, 12))

        self.stop_button = ttk.Button(frame, text="STOP VCM", command=self.stop_runtime)
        self.stop_button.grid(row=2, column=1, sticky="ew", padx=(8, 0), pady=(0, 12))

        self._add_row(frame, 3, "Last command:", self.last_command_var)
        self._add_row(frame, 4, "Last action:", self.last_action_var)
        self._add_row(frame, 5, "Response:", self.response_var)
        self._add_row(frame, 6, "System:", self.system_var)

    def _add_row(self, frame: ttk.Frame, row: int, label: str, variable: tk.StringVar) -> None:
        ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", pady=2)
        ttk.Label(frame, textvariable=variable, wraplength=260).grid(
            row=row, column=1, sticky="w", pady=2
        )

    def runtime_command(self) -> list[str]:
        command = [
            self.args.python,
            "-u",
            str(PACKAGE_ROOT / "scripts" / "pi_wake_voice_control_demo.py"),
            "--device",
            self.args.device,
            "--wake-duration-sec",
            "4",
            "--command-duration-sec",
            "4",
            "--wake-experiment-id",
            "E37_TARGETED_COLOR_VOLUME_FIX",
            "--wake-threshold",
            "0.90",
            "--wake-threshold-policy",
            "",
            "--command-experiment-id",
            "E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT",
            "--command-threshold-policy",
            "configs/e50_revised_vocab_e40_thresholds.json",
            "--cnn-config",
            "configs/cnn_fastbn_dense_nodropout_raw19.json",
            "--response-map",
            "configs/demo_response_assets.json",
            "--enable-response-audio",
            "--continuous",
            "--evidence-dir",
            self.args.evidence_dir,
            "--trial-id",
            "touchscreen_gui_wake_wait",
            "--expected-wake",
            "hey pi",
        ]
        if self.args.wait_for_wake:
            command.extend(
                [
                    "--wait-for-wake",
                    "--max-wake-attempts",
                    str(self.args.max_wake_attempts),
                    "--wake-retry-delay-sec",
                    str(self.args.wake_retry_delay_sec),
                ]
            )
        if self.args.response_audio_device:
            command.extend(["--response-audio-device", self.args.response_audio_device])
        if self.args.enable_gpio:
            command.append("--enable-gpio")
        return command

    def start_runtime(self) -> None:
        if self.process and self.process.poll() is None:
            self.state_var.set("WAKE ME UP")
            self.status_var.set('Say "hey pi"')
            return

        evidence_dir = PACKAGE_ROOT / self.args.evidence_dir
        evidence_dir.mkdir(parents=True, exist_ok=True)
        self.last_result_path = None
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        self.process = subprocess.Popen(
            self.runtime_command(),
            cwd=str(PACKAGE_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            start_new_session=True,
            env=env,
        )
        threading.Thread(target=self.read_runtime_output, daemon=True).start()
        self.set_instruction("WAKE ME UP", 'Say "hey pi"')
        self.system_var.set("OFFLINE")

    def read_runtime_output(self) -> None:
        if not self.process or not self.process.stdout:
            return
        try:
            for line in self.process.stdout:
                self.output_queue.put(line.strip())
        except Exception:
            return

    def set_instruction(self, state: str, status: str, hold_sec: float = 0.0) -> None:
        self.state_var.set(state)
        self.status_var.set(status)
        if hold_sec > 0:
            self.instruction_hold_until = time.monotonic() + hold_sec
        else:
            self.instruction_hold_until = 0.0

    def instruction_held(self) -> bool:
        return time.monotonic() < self.instruction_hold_until

    def stop_runtime(self) -> None:
        if not self.process or self.process.poll() is not None:
            self.process = None
            self.state_var.set("STOPPED")
            self.status_var.set("Runtime is not running")
            return

        try:
            if os.name == "posix":
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            else:
                self.process.terminate()
            self.process.wait(timeout=5)
        except Exception:
            try:
                self.process.kill()
            except Exception:
                pass
        finally:
            self.process = None
            self.state_var.set("STOPPED")
            self.status_var.set("VCM stopped")

    def poll_runtime(self) -> None:
        if self.process and self.process.poll() is not None:
            self.process = None
            self.state_var.set("STOPPED")
            self.status_var.set("Runtime exited")

        self.refresh_runtime_output()
        self.refresh_latest_result()
        self.root.after(self.args.poll_ms, self.poll_runtime)

    def refresh_runtime_output(self) -> None:
        while True:
            try:
                line = self.output_queue.get_nowait()
            except queue.Empty:
                return
            if not line:
                continue
            if "Wake stage" in line:
                if not self.instruction_held():
                    self.set_instruction("WAKE ME UP", 'Say "hey pi"')
            elif "Wake accepted" in line or "Command stage" in line:
                self.set_instruction("SAY WHAT YOU NEED", "I am at your command.")
            elif "Returned to listening" in line:
                if not self.instruction_held():
                    self.set_instruction("WAKE ME UP", 'Say "hey pi"')
            elif "Wake not accepted" in line or "Wake rejected" in line or "Wake phrase was not accepted" in line:
                self.set_instruction("I AM NOT AWAKE", 'Say "hey pi" again.', hold_sec=2.0)

    def refresh_latest_result(self) -> None:
        evidence_dir = PACKAGE_ROOT / self.args.evidence_dir
        if not evidence_dir.exists():
            return
        result_files = sorted(
            evidence_dir.glob("*_result.json"),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
        if not result_files:
            return
        latest = result_files[0]
        if latest == self.last_result_path:
            return
        self.last_result_path = latest
        try:
            payload = json.loads(latest.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            self.status_var.set("ERROR reading latest result")
            return

        command_result = payload.get("command_result") or {}
        action_result = payload.get("action_result") or {}
        response_result = payload.get("response_result") or {}

        predicted = command_result.get("predicted_label") or command_result.get("predicted_intent")
        accepted = command_result.get("accepted")
        action = action_result.get("action") or payload.get("routed_intent")
        response_played = response_result.get("played")

        if payload.get("status") == "rejected":
            if command_result:
                if str(predicted or "").upper() == "UNKNOWN":
                    self.set_instruction("I CAN'T DO THAT", 'Say "hey pi" again.', hold_sec=2.0)
                else:
                    self.set_instruction("I DIDN'T UNDERSTAND", 'Say "hey pi" again.', hold_sec=2.0)
            else:
                self.set_instruction("I AM NOT AWAKE", 'Say "hey pi" again.', hold_sec=2.0)
        elif payload.get("status") == "executed":
            if not self.instruction_held():
                self.set_instruction("WAKE ME UP", 'Say "hey pi"')
        else:
            if not self.instruction_held():
                self.status_var.set(str(payload.get("status", "Latest result recorded")))

        self.last_command_var.set(str(predicted or "--"))
        self.last_action_var.set(str(action or "--"))
        if accepted is False:
            self.response_var.set("No action")
        elif response_played is True:
            self.response_var.set("Played successfully")
        elif response_played is False:
            self.response_var.set("Not played")
        else:
            self.response_var.set("--")

    def on_close(self) -> None:
        self.stop_runtime()
        self.root.destroy()


def main() -> None:
    args = parse_args()
    root = tk.Tk()
    VcmTouchscreenGui(root, args)
    root.mainloop()


if __name__ == "__main__":
    main()
