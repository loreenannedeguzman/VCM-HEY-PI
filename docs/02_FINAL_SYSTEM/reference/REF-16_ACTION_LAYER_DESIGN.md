# Voice Command Action Layer Design

## Purpose

The CNN predicts an intent. The action layer turns an accepted intent into a
local device behavior or a safe simulated behavior.

This is separate from the CNN because the CNN currently does not transcribe
speech and does not output slots such as `on`, `off`, `10 percent`, `5 minutes`,
or `mom`.

## Supported Intents

| Intent | Current action behavior | Hardware/online status |
|---|---|---|
| `PLAY_MUSIC` | records media state as playing; can play local WAV with `aplay` when enabled | local speaker optional |
| `QUESTION` | routes supported questions to local time or simulated weather; logs generic questions | online search disabled for offline deployment |
| `LIGHT_CONTROL` | on/off/toggle if slot is available | GPIO optional |
| `LIGHT_ADJUST` | updates brightness/color state; optional PWM LED brightness | GPIO optional |
| `SET_TIMER` | creates local timer entry | local state |
| `SET_ALARM` | creates local alarm entry | local state |
| `THERMOSTAT` | stores target temperature and simulated fan state | fan optional later |
| `MEDIA_CONTROL` | pause/stop/next/volume/play-music state changes; can play local WAV with `aplay` when enabled | local speaker optional |
| `REMINDER` | creates or lists local reminders | local state |
| `CALL_MESSAGE` | logs call/message request only | no phone service invoked |

## Slot Handling

The current project can conceptualize these actions now, but full autonomy
requires slot information. Examples:

- `turn on the light` needs `light_action=on`
- `turn off the light` needs `light_action=off`
- `dim lights to 10 percent` needs `brightness_percent=10`
- `set a timer for 5 minutes` needs `duration_seconds=300`
- `set an alarm for 6 am` needs `alarm_time=6:00 am`
- `set temperature to 24 degrees` needs `temperature_degrees=24`
- `call mom` needs `contact=mom`

For now, `actions/command_actions.py` can parse slots from an optional phrase
string. In the live CNN-only path, these slots must be supplied by a controlled
demo mode, separate phrase labels, or a future lightweight slot/action model.

## Recommended Demo Scope

For the first Raspberry Pi demo:

1. Validate `LIGHT_CONTROL` prediction from the Pi microphone.
2. Use a controlled light action such as `--slot light_action=on` or
   `--slot light_action=off`, or run a blink/toggle demo.
3. Keep search, calls, and messaging as logged stubs because the final system
   must operate locally and offline.

## What Is Already Pre-Coded

- Local time answer for `QUESTION`.
- Simulated weather answer for `QUESTION`.
- LED on/off/toggle/blink for `LIGHT_CONTROL`.
- LED brightness state for `LIGHT_ADJUST`.
- Timer and alarm storage.
- Simulated thermostat target and fan state.
- Media state, track index, next/pause/stop/volume, and optional local WAV playback.
- Reminder storage and listing.
- Simulated call/message screen state.

## What Still Needs Hardware To Become Visible

- RGB LED or separate LEDs for full color output.
- Buzzer for timer/alarm completion.
- Fan or motor driver for thermostat demonstration.
- OLED/LCD screen if display output should be visible outside console/state JSON.
- Speaker if local music playback should be audible.

## Demo Commands

```bash
python actions/command_actions.py --intent LIGHT_CONTROL --phrase "turn on the light"
python actions/command_actions.py --intent LIGHT_ADJUST --phrase "dim lights to 10 percent"
python actions/command_actions.py --intent SET_TIMER --phrase "set a timer for 5 minutes"
python actions/command_actions.py --intent SET_ALARM --phrase "set an alarm for 6 am"
python actions/command_actions.py --intent THERMOSTAT --phrase "set temperature to 24 degrees"
python actions/command_actions.py --intent MEDIA_CONTROL --phrase "pause"
python actions/command_actions.py --intent REMINDER --phrase "remind me to check the rice"
python actions/command_actions.py --intent CALL_MESSAGE --phrase "call mom"
```
