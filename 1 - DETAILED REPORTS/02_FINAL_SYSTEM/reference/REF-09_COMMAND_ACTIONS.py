from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from time import sleep
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STATE_PATH = PROJECT_ROOT / "results" / "tables" / "action_state.json"
DEFAULT_MUSIC_DIR = PROJECT_ROOT / "music"

NUMBER_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
}


@dataclass
class ActionRequest:
    intent: str
    confidence: float = 1.0
    accepted: bool = True
    phrase: str = ""
    slots: dict[str, Any] = field(default_factory=dict)
    threshold: float = 0.90


@dataclass
class ActionResult:
    intent: str
    status: str
    action: str
    message: str
    confidence: float
    accepted: bool
    slots: dict[str, Any] = field(default_factory=dict)
    hardware_applied: bool = False


def default_state() -> dict[str, Any]:
    return {
        "lights": {"power": "off", "brightness_percent": 100, "color": "white"},
        "thermostat": {
            "current_temperature_degrees": 27,
            "target_temperature_degrees": None,
            "fan": "off",
        },
        "timers": [],
        "alarms": [],
        "reminders": [],
        "media": {"status": "stopped", "volume": 50, "track_index": 0, "track": ""},
        "calls": [],
        "messages": [],
        "questions": [],
        "weather": {"temperature": 28, "condition": "Partly cloudy", "humidity": 72},
        "display": {"title": "VCM ASSISTANT", "lines": []},
        "alerts": [],
    }


def load_state(path: Path) -> dict[str, Any]:
    state = default_state()
    if not path.exists():
        return state
    with path.open("r", encoding="utf-8") as f:
        loaded = json.load(f)
    for key, value in loaded.items():
        if isinstance(value, dict) and isinstance(state.get(key), dict):
            state[key].update(value)
        else:
            state[key] = value
    if "temperature_degrees" in state["thermostat"]:
        state["thermostat"]["target_temperature_degrees"] = state["thermostat"].pop(
            "temperature_degrees"
        )
    return state


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
        f.write("\n")


def parse_slots(phrase: str) -> dict[str, Any]:
    text = phrase.lower().strip()
    slots: dict[str, Any] = {}

    if re.search(r"\b(turn|switch)\s+on\b|\blights?\s+on\b", text):
        slots["light_action"] = "on"
    elif re.search(r"\b(turn|switch)\s+off\b|\blights?\s+off\b", text):
        slots["light_action"] = "off"

    percent_match = re.search(r"\b(\d{1,3})\s*(percent|%)\b", text)
    if percent_match:
        slots["brightness_percent"] = max(0, min(100, int(percent_match.group(1))))
    elif "dim" in text:
        slots["brightness_percent"] = 50

    color_match = re.search(r"\b(red|green|blue|white|yellow|purple|pink|orange)\b", text)
    if color_match:
        slots["color"] = color_match.group(1)

    number_pattern = r"\d{1,3}|" + "|".join(NUMBER_WORDS)
    timer_match = re.search(rf"\b({number_pattern})\s*(second|seconds|minute|minutes|hour|hours)\b", text)
    if timer_match:
        raw_value = timer_match.group(1)
        value = int(raw_value) if raw_value.isdigit() else NUMBER_WORDS[raw_value]
        unit = timer_match.group(2)
        multiplier = 1 if unit.startswith("second") else 60 if unit.startswith("minute") else 3600
        slots["duration_seconds"] = value * multiplier

    alarm_match = re.search(rf"\b({number_pattern})(?::(\d{{2}}))?\s*(am|pm)\b", text)
    if alarm_match:
        raw_hour = alarm_match.group(1)
        hour = int(raw_hour) if raw_hour.isdigit() else NUMBER_WORDS[raw_hour]
        minute = int(alarm_match.group(2) or "0")
        meridiem = alarm_match.group(3)
        slots["alarm_time"] = f"{hour}:{minute:02d} {meridiem}"

    temp_match = re.search(r"\b(\d{2,3})\s*(degree|degrees)\b", text)
    if temp_match:
        slots["temperature_degrees"] = int(temp_match.group(1))

    if "pause" in text:
        slots["media_action"] = "pause"
    elif "stop" in text:
        slots["media_action"] = "stop"
    elif re.search(r"\b(next|skip)\b", text):
        slots["media_action"] = "next"
    elif re.search(r"\b(volume up|louder|raise volume|increase volume)\b", text):
        slots["media_action"] = "volume_up"
    elif re.search(r"\b(volume down|quieter|lower volume|decrease volume)\b", text):
        slots["media_action"] = "volume_down"
    elif re.search(r"\b(play music|start music|music)\b", text):
        slots["media_action"] = "play_music"
    elif re.search(r"\b(continue|resume)\b", text):
        slots["media_action"] = "resume"

    remind_match = re.search(r"\bremind me to\s+(.+)$", text)
    if remind_match:
        slots["reminder_text"] = remind_match.group(1).strip()
    elif "what are my reminders" in text or "list reminders" in text:
        slots["reminder_action"] = "list"

    call_match = re.search(r"\bcall\s+(.+)$", text)
    if call_match:
        slots["contact"] = call_match.group(1).strip()
        slots["communication_action"] = "call"

    message_match = re.search(r"\bmessage\s+(.+)$", text)
    if message_match:
        slots["contact"] = message_match.group(1).strip()
        slots["communication_action"] = "message"

    if text and text.endswith("?"):
        slots["query"] = text
    if "weather" in text:
        slots["question_type"] = "weather"
    elif re.search(r"\btime\b|\bclock\b", text):
        slots["question_type"] = "time"
    return slots


def _apply_led(action: str, pin: int, brightness_percent: int | None = None) -> bool:
    try:
        from gpiozero import LED, PWMLED
    except ImportError as exc:
        raise RuntimeError("gpiozero is required for GPIO actions on Raspberry Pi.") from exc

    if brightness_percent is not None:
        led = PWMLED(pin)
        led.value = max(0.0, min(1.0, brightness_percent / 100.0))
        led.close()
        return True

    led = LED(pin)
    if action == "on":
        led.on()
    elif action == "off":
        led.off()
    elif action == "toggle":
        led.toggle()
    elif action == "blink":
        led.on()
        sleep(0.5)
        led.off()
    else:
        led.close()
        return False
    led.close()
    return True


def _available_tracks(music_dir: Path) -> list[Path]:
    if not music_dir.exists():
        return []
    return sorted(
        path for path in music_dir.iterdir() if path.suffix.lower() in {".wav", ".mp3"}
    )


def _try_play_audio(path: Path) -> bool:
    if not path.exists() or path.suffix.lower() != ".wav":
        return False
    try:
        subprocess.Popen(["aplay", str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (FileNotFoundError, OSError):
        return False
    return True


def _set_display(state: dict[str, Any], title: str, *lines: str) -> None:
    state["display"] = {"title": title, "lines": list(lines)}


def execute_action(
    request: ActionRequest,
    *,
    state_path: Path = DEFAULT_STATE_PATH,
    enable_gpio: bool = False,
    gpio_pin: int = 17,
    enable_local_audio: bool = False,
    music_dir: Path = DEFAULT_MUSIC_DIR,
) -> ActionResult:
    slots = {**parse_slots(request.phrase), **request.slots}
    state = load_state(state_path)

    if not request.accepted:
        return ActionResult(
            intent=request.intent,
            status="rejected",
            action="none",
            message="Prediction was below the confidence threshold; no action taken.",
            confidence=request.confidence,
            accepted=False,
            slots=slots,
        )

    intent = request.intent
    now = datetime.now().isoformat(timespec="seconds")
    hardware_applied = False

    if intent == "PLAY_MUSIC":
        state["media"]["status"] = "playing"
        tracks = _available_tracks(music_dir)
        if tracks:
            track_index = int(state["media"].get("track_index", 0)) % len(tracks)
            state["media"]["track"] = str(tracks[track_index])
            if enable_local_audio:
                hardware_applied = _try_play_audio(tracks[track_index])
        _set_display(state, "PLAYING", Path(state["media"].get("track", "local music")).name)
        action = "media.play_music"
        message = "Music playback requested. Local WAV playback is attempted only when enabled."

    elif intent == "MEDIA_CONTROL":
        media_action = slots.get("media_action", "pause")
        tracks = _available_tracks(music_dir)
        if media_action in {"pause", "stop"}:
            state["media"]["status"] = media_action
        elif media_action in {"play_music", "resume"}:
            state["media"]["status"] = "playing"
            if tracks:
                track_index = int(state["media"].get("track_index", 0)) % len(tracks)
                state["media"]["track"] = str(tracks[track_index])
                if enable_local_audio:
                    hardware_applied = _try_play_audio(tracks[track_index])
        elif media_action == "next":
            state["media"]["track_index"] = int(state["media"].get("track_index", 0)) + 1
            if tracks:
                track_index = int(state["media"]["track_index"]) % len(tracks)
                state["media"]["track"] = str(tracks[track_index])
                if enable_local_audio:
                    hardware_applied = _try_play_audio(tracks[track_index])
        elif media_action == "volume_up":
            state["media"]["volume"] = min(100, int(state["media"]["volume"]) + 10)
        elif media_action == "volume_down":
            state["media"]["volume"] = max(0, int(state["media"]["volume"]) - 10)
        _set_display(
            state,
            "MEDIA",
            f"status: {state['media']['status']}",
            f"volume: {state['media']['volume']}",
        )
        action = f"media.{media_action}"
        message = "Media command recorded in local demo state."

    elif intent == "QUESTION":
        question_type = slots.get("question_type", "generic")
        state["questions"].append(
            {"created_at": now, "query": slots.get("query", request.phrase), "type": question_type}
        )
        if question_type == "weather":
            weather = state["weather"]
            _set_display(
                state,
                "WEATHER",
                f"{weather['temperature']} C",
                str(weather["condition"]),
                f"humidity: {weather['humidity']}%",
            )
            action = "question.weather_local"
            message = (
                f"Local weather: {weather['temperature']} C, "
                f"{weather['condition']}, humidity {weather['humidity']}%."
            )
        elif question_type == "time":
            current_time = datetime.now().strftime("%I:%M %p").lstrip("0")
            _set_display(state, "TIME", current_time)
            action = "question.time_local"
            message = f"Local time: {current_time}."
        else:
            _set_display(state, "QUESTION", "offline log only")
            action = "question.offline_stub"
            message = "Question/search is logged only. Online search is not used in offline deployment."

    elif intent == "LIGHT_CONTROL":
        light_action = slots.get("light_action")
        if light_action not in {"on", "off", "toggle", "blink"}:
            return ActionResult(
                intent=intent,
                status="needs_slot",
                action="light.noop",
                message="LIGHT_CONTROL was detected, but on/off/toggle/blink was not provided.",
                confidence=request.confidence,
                accepted=True,
                slots=slots,
            )
        state["lights"]["power"] = "on" if light_action in {"on", "toggle", "blink"} else "off"
        if enable_gpio:
            hardware_applied = _apply_led(light_action, gpio_pin)
        _set_display(state, "LIGHT", f"power: {state['lights']['power']}")
        action = f"light.{light_action}"
        message = f"Light action prepared: {light_action}."

    elif intent == "LIGHT_ADJUST":
        brightness = int(slots.get("brightness_percent", state["lights"]["brightness_percent"]))
        state["lights"]["brightness_percent"] = max(0, min(100, brightness))
        if "color" in slots:
            state["lights"]["color"] = slots["color"]
        if enable_gpio:
            hardware_applied = _apply_led("brightness", gpio_pin, state["lights"]["brightness_percent"])
        _set_display(
            state,
            "LIGHT ADJUST",
            f"brightness: {state['lights']['brightness_percent']}%",
            f"color: {state['lights']['color']}",
        )
        action = "light.adjust"
        message = "Light brightness/color state updated."

    elif intent == "SET_TIMER":
        duration = int(slots.get("duration_seconds", 300))
        due_at = (datetime.now() + timedelta(seconds=duration)).isoformat(timespec="seconds")
        state["timers"].append({"created_at": now, "duration_seconds": duration, "due_at": due_at})
        _set_display(state, "TIMER", f"{duration} seconds", f"due: {due_at}")
        action = "timer.create"
        message = f"Timer created for {duration} seconds."

    elif intent == "SET_ALARM":
        alarm_time = slots.get("alarm_time", "unspecified")
        state["alarms"].append({"created_at": now, "alarm_time": alarm_time})
        _set_display(state, "ALARM", str(alarm_time))
        action = "alarm.create"
        message = f"Alarm request stored for {alarm_time}."

    elif intent == "THERMOSTAT":
        temperature = slots.get("temperature_degrees")
        if temperature is not None:
            state["thermostat"]["target_temperature_degrees"] = int(temperature)
        target = state["thermostat"]["target_temperature_degrees"]
        current = state["thermostat"]["current_temperature_degrees"]
        if target is not None:
            state["thermostat"]["fan"] = "on" if current > target else "off"
        _set_display(
            state,
            "THERMOSTAT",
            f"current: {current} C",
            f"target: {target} C",
            f"fan: {state['thermostat']['fan']}",
        )
        action = "thermostat.set_temperature"
        message = "Thermostat command stored as simulated local state."

    elif intent == "REMINDER":
        if slots.get("reminder_action") == "list":
            action = "reminder.list"
            message = json.dumps(state["reminders"])
            _set_display(state, "REMINDERS", *[item["text"] for item in state["reminders"][-3:]])
        else:
            reminder_text = slots.get("reminder_text", request.phrase or "unspecified reminder")
            state["reminders"].append({"created_at": now, "text": reminder_text})
            action = "reminder.create"
            message = f"Reminder stored: {reminder_text}"
            _set_display(state, "REMINDER", reminder_text)

    elif intent == "CALL_MESSAGE":
        communication_action = slots.get("communication_action", "call")
        contact = slots.get("contact", "unspecified contact")
        state["calls" if communication_action == "call" else "messages"].append(
            {"created_at": now, "contact": contact, "phrase": request.phrase}
        )
        _set_display(state, communication_action.upper(), contact, "simulated only")
        action = f"communication.{communication_action}_stub"
        message = "Call/message command logged only. No phone or messaging service is invoked offline."

    else:
        return ActionResult(
            intent=intent,
            status="unsupported",
            action="none",
            message=f"No action handler exists for intent: {intent}",
            confidence=request.confidence,
            accepted=True,
            slots=slots,
        )

    save_state(state_path, state)
    return ActionResult(
        intent=intent,
        status="executed",
        action=action,
        message=message,
        confidence=request.confidence,
        accepted=True,
        slots=slots,
        hardware_applied=hardware_applied,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a VCM action handler in dry-run mode.")
    parser.add_argument("--intent", required=True)
    parser.add_argument("--confidence", type=float, default=1.0)
    parser.add_argument("--accepted", action="store_true", default=True)
    parser.add_argument("--phrase", default="")
    parser.add_argument("--slot", action="append", default=[], help="key=value slot override")
    parser.add_argument("--state-path", default=str(DEFAULT_STATE_PATH))
    parser.add_argument("--enable-gpio", action="store_true")
    parser.add_argument("--gpio-pin", type=int, default=17)
    parser.add_argument("--enable-local-audio", action="store_true")
    parser.add_argument("--music-dir", default=str(DEFAULT_MUSIC_DIR))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    slots = {}
    for raw_slot in args.slot:
        key, value = raw_slot.split("=", 1)
        slots[key] = value
    result = execute_action(
        ActionRequest(
            intent=args.intent,
            confidence=args.confidence,
            accepted=args.accepted,
            phrase=args.phrase,
            slots=slots,
        ),
        state_path=Path(args.state_path),
        enable_gpio=args.enable_gpio,
        gpio_pin=args.gpio_pin,
        enable_local_audio=args.enable_local_audio,
        music_dir=Path(args.music_dir),
    )
    print(json.dumps(asdict(result), indent=2))


if __name__ == "__main__":
    main()
