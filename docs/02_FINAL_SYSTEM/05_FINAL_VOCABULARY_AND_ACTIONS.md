# 05 - Final Vocabulary And Actions

## Final Vocabulary

Final E50 has 19 callable command labels:

`PLAY_MUSIC`, `WEATHER`, `TIME`, `LIGHT_ON`, `LIGHT_OFF`, `LIGHT_DIM`, `BRIGHTNESS`, `TIMER`, `ALARM`, `TEMPERATURE`, `NEXT`, `PAUSE`, `STOP`, `VOLUME_UP`, `VOLUME_DOWN`, `CREATE_REMINDER`, `LIST_REMINDERS`, `CALL`, and `MESSAGE`.

`COLOR` is not a final E50 class. The final vocabulary uses `LIGHT_DIM`. [REF-01] [REF-02] [REF-11]

## Dataset2 Coverage Boundary

Dataset2/VCM_MASTER has 16 classes, not the final 19-label E50 vocabulary. Dataset2 directly supports several labels but does not directly provide final coverage for `CREATE_REMINDER`, `LIST_REMINDERS`, `CALL`, or `MESSAGE`, and its `LIGHT_DIM`/`BRIGHTNESS` support is nuanced. Final E50 therefore combines active-project data, bounded Dataset2 support, and separate E41 adaptation data. [REF-02]

## Label-To-Action Mapping

The E50 CNN predicts a raw command label. If E40 accepts the prediction, the deterministic router maps it to an intent and default slots. [REF-07] [REF-08]

| E50 label | Routed intent | Default route evidence | Response asset evidence |
|---|---|---|---|
| `PLAY_MUSIC` | `PLAY_MUSIC` | `media_action=play_music` | `play_music_extra_loud.wav` |
| `WEATHER` | `QUESTION` | `question_type=weather` | `weather_extra_loud.wav` |
| `TIME` | `QUESTION` | `question_type=time` | `time_extra_loud.wav` |
| `LIGHT_ON` | `LIGHT_CONTROL` | `light_action=on` | `light_on_extra_loud.wav` |
| `LIGHT_OFF` | `LIGHT_CONTROL` | `light_action=off` | `light_off_extra_loud.wav` |
| `LIGHT_DIM` | `LIGHT_ADJUST` | `brightness_percent=50`, `light_adjust_action=dim` | `light_dim_extra_loud.wav` |
| `BRIGHTNESS` | `LIGHT_ADJUST` | `brightness_percent=50` | `brightness_extra_loud.wav` |
| `TIMER` | `SET_TIMER` | `duration_seconds=300` | `timer_extra_loud.wav` |
| `ALARM` | `SET_ALARM` | `alarm_time=6:00 am` | `alarm_extra_loud.wav` |
| `TEMPERATURE` | `THERMOSTAT` | `temperature_degrees=22` | `temperature_extra_loud.wav` |
| `NEXT` | `MEDIA_CONTROL` | `media_action=next` | `next_extra_loud.wav` |
| `PAUSE` | `MEDIA_CONTROL` | `media_action=pause` | `pause_extra_loud.wav` |
| `STOP` | `MEDIA_CONTROL` | `media_action=stop` | `stop_extra_loud.wav` |
| `VOLUME_UP` | `MEDIA_CONTROL` | `media_action=volume_up` | `volume_up_extra_loud.wav` |
| `VOLUME_DOWN` | `MEDIA_CONTROL` | `media_action=volume_down` | `volume_down_extra_loud.wav` |
| `CREATE_REMINDER` | `REMINDER` | `reminder_text=demo reminder` | `create_reminder_extra_loud.wav` |
| `LIST_REMINDERS` | `REMINDER` | `reminder_action=list` | `list_reminders_extra_loud.wav` |
| `CALL` | `CALL_MESSAGE` | `communication_action=call` | `call_extra_loud.wav` |
| `MESSAGE` | `CALL_MESSAGE` | `communication_action=message` | `message_extra_loud.wav` |

Sources: route map [REF-08] and response map [REF-10].

## Rejection Behavior

`UNKNOWN` and `WAKE` are no-action safety labels in the router. Unsupported labels or below-threshold predictions do not become actions. The response map includes an `UNKNOWN` response asset pointing to `rejected_extra_loud.wav`. [REF-08] [REF-10]

## Callable Versus Demo-Ready

The final package preserves all 19 callable labels and benchmarked all 19 in Item 16. However, callable is not identical to demo-ready. The adjusted package README distinguishes the full callable vocabulary from the recommended live demo subset and preserves historical limitations for commands such as `TEMPERATURE`. [REF-03]

## GUI Boundary

The GUI is not part of label-to-action semantics. It displays status and starts/stops the runtime. Recognition, acceptance, routing, and action mapping remain in the frozen VCM core. [REF-05] [REF-06] [REF-15]
