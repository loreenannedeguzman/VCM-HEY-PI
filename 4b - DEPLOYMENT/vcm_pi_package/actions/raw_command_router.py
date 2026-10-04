from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RoutedCommand:
    command_label: str
    intent: str
    accepted: bool
    confidence: float
    threshold: float
    slots: dict[str, str] = field(default_factory=dict)
    reason: str = ""


RAW_COMMAND_ROUTES: dict[str, tuple[str, dict[str, str]]] = {
    "PLAY_MUSIC": ("PLAY_MUSIC", {"media_action": "play_music"}),
    "WEATHER": ("QUESTION", {"question_type": "weather"}),
    "TIME": ("QUESTION", {"question_type": "time"}),
    "LIGHT_ON": ("LIGHT_CONTROL", {"light_action": "on"}),
    "LIGHT_OFF": ("LIGHT_CONTROL", {"light_action": "off"}),
    "PAUSE": ("MEDIA_CONTROL", {"media_action": "pause"}),
    "STOP": ("MEDIA_CONTROL", {"media_action": "stop"}),
    "NEXT": ("MEDIA_CONTROL", {"media_action": "next"}),
    "VOLUME_UP": ("MEDIA_CONTROL", {"media_action": "volume_up"}),
    "VOLUME_DOWN": ("MEDIA_CONTROL", {"media_action": "volume_down"}),
    "CALL": ("CALL_MESSAGE", {"communication_action": "call"}),
    "MESSAGE": ("CALL_MESSAGE", {"communication_action": "message"}),
    "LIST_REMINDERS": ("REMINDER", {"reminder_action": "list"}),
    "CREATE_REMINDER": ("REMINDER", {"reminder_text": "demo reminder"}),
    "TIMER": ("SET_TIMER", {"duration_seconds": "300"}),
    "ALARM": ("SET_ALARM", {"alarm_time": "6:00 am"}),
    "TEMPERATURE": ("THERMOSTAT", {"temperature_degrees": "22"}),
    "LIGHT_DIM": ("LIGHT_ADJUST", {"brightness_percent": "50", "light_adjust_action": "dim"}),
    "BRIGHTNESS": ("LIGHT_ADJUST", {"brightness_percent": "50"}),
}

NO_ACTION_RAW_LABELS = {"UNKNOWN", "WAKE"}


def route_raw_command(
    command_label: str,
    *,
    confidence: float,
    accepted: bool,
    threshold: float,
    slot_overrides: dict[str, str] | None = None,
) -> RoutedCommand:
    if command_label in NO_ACTION_RAW_LABELS:
        return RoutedCommand(
            command_label=command_label,
            intent=command_label,
            accepted=False,
            confidence=confidence,
            threshold=threshold,
            reason=f"{command_label} is a no-action safety label.",
        )

    if command_label not in RAW_COMMAND_ROUTES:
        return RoutedCommand(
            command_label=command_label,
            intent=command_label,
            accepted=False,
            confidence=confidence,
            threshold=threshold,
            reason=f"No raw-command route exists for {command_label}.",
        )

    intent, default_slots = RAW_COMMAND_ROUTES[command_label]
    slots = {**default_slots, **(slot_overrides or {})}
    return RoutedCommand(
        command_label=command_label,
        intent=intent,
        accepted=accepted,
        confidence=confidence,
        threshold=threshold,
        slots=slots,
        reason="accepted" if accepted else "Prediction was below the command confidence threshold.",
    )
