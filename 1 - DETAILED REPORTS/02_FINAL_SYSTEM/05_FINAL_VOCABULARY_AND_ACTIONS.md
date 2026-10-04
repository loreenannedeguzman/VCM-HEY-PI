# Final Vocabulary And Actions

## Engineering Question

What can the final E50 system classify, and what happens when an accepted label reaches the action layer?

E50 predicts one of 19 final labels. If E40 accepts the prediction, the deterministic router maps that label to an intent and default slots, then the local action/response layer handles it. The model label, routed intent, local action, and response WAV are related but not identical concepts.

## Final E50 Vocabulary

`PLAY_MUSIC`, `WEATHER`, `TIME`, `LIGHT_ON`, `LIGHT_OFF`, `LIGHT_DIM`, `BRIGHTNESS`, `TIMER`, `ALARM`, `TEMPERATURE`, `NEXT`, `PAUSE`, `STOP`, `VOLUME_UP`, `VOLUME_DOWN`, `CREATE_REMINDER`, `LIST_REMINDERS`, `CALL`, `MESSAGE`.

`COLOR` is not a final E50 class. `LIGHT_DIM` is the final vocabulary label replacing the historical color/dimming ambiguity in the final E50 vocabulary.

## Label-To-Action Specification

| E50 label | Intended command type | Routed intent/action evidence | Response WAV evidence |
|---|---|---|---|
| `PLAY_MUSIC` | Music playback | `media_action=play_music` | `play_music_extra_loud.wav` |
| `WEATHER` | Weather question placeholder | `question_type=weather` | `weather_extra_loud.wav` |
| `TIME` | Time question placeholder | `question_type=time` | `time_extra_loud.wav` |
| `LIGHT_ON` | Light control | `light_action=on` | `light_on_extra_loud.wav` |
| `LIGHT_OFF` | Light control | `light_action=off` | `light_off_extra_loud.wav` |
| `LIGHT_DIM` | Light adjustment | `brightness_percent=50`, `light_adjust_action=dim` | `light_dim_extra_loud.wav` |
| `BRIGHTNESS` | Brightness adjustment | `brightness_percent=50` | `brightness_extra_loud.wav` |
| `TIMER` | Timer placeholder | `duration_seconds=300` | `timer_extra_loud.wav` |
| `ALARM` | Alarm placeholder | `alarm_time=6:00 am` | `alarm_extra_loud.wav` |
| `TEMPERATURE` | Thermostat placeholder | `temperature_degrees=22` | `temperature_extra_loud.wav` |
| `NEXT` | Media control | `media_action=next` | `next_extra_loud.wav` |
| `PAUSE` | Media control | `media_action=pause` | `pause_extra_loud.wav` |
| `STOP` | Media control | `media_action=stop` | `stop_extra_loud.wav` |
| `VOLUME_UP` | Media control | `media_action=volume_up` | `volume_up_extra_loud.wav` |
| `VOLUME_DOWN` | Media control | `media_action=volume_down` | `volume_down_extra_loud.wav` |
| `CREATE_REMINDER` | Reminder placeholder | `reminder_text=demo reminder` | `create_reminder_extra_loud.wav` |
| `LIST_REMINDERS` | Reminder placeholder | `reminder_action=list` | `list_reminders_extra_loud.wav` |
| `CALL` | Communication placeholder | `communication_action=call` | `call_extra_loud.wav` |
| `MESSAGE` | Communication placeholder | `communication_action=message` | `message_extra_loud.wav` |

The response files establish the configured playback assets, not necessarily a separate transcript claim for every WAV.

## Rejection And No-Action Labels

`UNKNOWN` and wake/no-action behavior are safety paths rather than final callable E50 command actions. If a prediction is below E40 threshold, unsupported, or `UNKNOWN`, no command action should be routed. The response map includes `rejected_extra_loud.wav` for rejection feedback.

## Callable Versus Demo-Ready

All 19 labels are part of the final E50 vocabulary, but callable is not the same as equally validated or equally demo-ready. The final physical benchmark used one valid-command trial per final label plus one UNKNOWN/no-action trial. That supports integrated deployment evidence, not statistically meaningful per-label accuracy. Historical demo notes distinguish commands that were demo-ready, previously supported but needing repeat verification, callable but not verified for demo, or unsafe/not demo-ready.

## Dataset Coverage Boundary

Dataset2/VCM_MASTER has 16 classes, while final E50 has 19 labels. Dataset2 directly supports several final labels but does not directly provide final coverage for `CREATE_REMINDER`, `LIST_REMINDERS`, `CALL`, or `MESSAGE`; `LIGHT_DIM`/`BRIGHTNESS` support is nuanced. Final E50 therefore combines active-project data, selected `VCM_BALANCED` rows, and E41 adaptation rows.

## GUI Boundary

The GUI displays status and starts/stops the runtime. It does not define the 19 labels, choose thresholds, route actions, or change the response map.
