# Pi Deployment Readiness Report

## Current Status

The Raspberry Pi 5 deployment path is now partially validated on hardware. The
Pi boots, SSH works, the USB microphone records audio, TensorFlow imports, and
the deployment package can run local inference.

The project is closer to a full all-command live exam demo after switching the
Pi package from broad-intent output to raw-command output and then applying
successive Pi recovery passes. The current package default is the E33
raw-command model with an E33 per-label guardrail policy. It is still not final
exam-ready because E33 must be tested on a new live Pi validation pass after
being copied to the Raspberry Pi.

## Model Route

This remains a CNN voice-command classification project, not speech
transcription. The audio waveform is converted to a log-Mel spectrogram, then
the CNN predicts one fixed vocabulary command. No text transcript is produced.

The primary deployment candidate is now:

- `E33_PI_COLOR_LIGHTON_RESPONSIVENESS`

This model is an E32-based fine-tune that predicts raw command labels such as
`LIGHT_ON`, `LIGHT_OFF`, `NEXT`, and `PAUSE`, then routes them to the assignment
intent/action layer. It was promoted to package default because it recovered the
E32 fresh clean `COLOR` and `LIGHT_ON` responsiveness gaps while preserving
zero wrong accepted commands on saved guardrail evidence.

## Evidence Summary

General baseline:

- `E21_CNN_DENSE_NODROPOUT_1000PI_BESTVAL`
- official intent-balanced validation accuracy: `0.8267`
- official macro-F1: `0.8304`

Light-command problem discovered during microphone trials:

- real-microphone turn-on set with E21: `10/25` correct
- real-microphone turn-off set with E21: `4/25` correct
- combined real-microphone light result with E21: `14/50` correct
- accepted wrong predictions were too common for immediate LED control

Targeted adaptation:

- `E23_LIGHT_REALMIC_ADAPT_E21_REPLAY`
- trained from E21 using 30 real-microphone light examples plus 880 replay
  examples from the original data
- held-out real-microphone light evaluation: `16/20` correct
- at threshold `0.90`: `12/20` accepted, `12` correct accepted, `0` wrong accepted
- official validation accuracy after adaptation: `0.7933`
- official macro-F1 after adaptation: `0.7912`

Interpretation:

- E21 is still the strongest general validation baseline.
- E23 remains useful historical evidence because it reduced the real-microphone
  light-command risk.
- The official validation score dropped after targeted adaptation, so E23 should
  be described as a deployment candidate, not a final universal model.

Raw-command Raspberry Pi recovery:

- `E24_PI_RAW_COMMAND_RECOVERY_PROBE`
- trained from the Pi calibration adaptation split plus original-data replay
- Pi holdout examples: `95`
- raw-command accuracy: `86/95`, or `90.53%`
- at threshold `0.90`: `77/95` accepted, `76` accepted correct, `1` wrong
  accepted
- at threshold `0.95`: `69/95` accepted, `69` accepted correct, `0` wrong
  accepted

Interpretation:

- E24 is the safest current all-command deployment checkpoint.
- E24 is now the Pi package default because it supports action-level routing.
- The stricter threshold trades off coverage for safety, which is appropriate
  before enabling GPIO or other physical actions.

Optional E24 guardrail threshold policy:

- config: `configs/e24_pi_guardrail_thresholds.json`
- method: use per-predicted-label thresholds instead of one global threshold
- measured on saved E24 Pi holdout predictions: `80/95` accepted, `80`
  accepted correct, `0` wrong accepted
- example guardrails: keep `LIGHT_ON` at `0.95` to reject observed
  `LIGHT_OFF -> LIGHT_ON` false positives; keep `NEXT` at `0.90` to reject
  observed `STOP -> NEXT` false positives; use an `0.80` floor for lower-risk
  labels with no observed false positives

This is a candidate guardrail, not final proof. Because it was derived from the
existing holdout predictions, it needs fresh Pi microphone validation before it
can be used as final exam-readiness evidence.

Fresh Pi recovery checkpoint:

- `E27_PI_LIVE_NEXT_COLOR_RECOVERY_PROBE`
- trained from E26 with source replay, Pi adaptation replay, the preserved
  fresh Pi mini-set, and the latest E26 live failure clips
- original 95-clip Pi holdout raw-command accuracy: `85/95`, or `89.47%`
- E27 guardrail policy on original Pi holdout: `74/95` accepted, `74` accepted
  correct, `0` wrong accepted
- combined recovery set: `15/15` raw correct, `15/15` accepted correct, `0`
  wrong accepted

Interpretation:

- E27 directly fixes the copied live Pi failure examples for `NEXT` and
  `COLOR`.
- The recovery set is not independent final proof because it was used in
  recovery training.
- The next required proof is a new live Pi validation pass using unique output
  filenames and the refreshed package.

Raspberry Pi hardware validation now completed:

- Pi SSH access works as `loreenanne@RaspberryPi5Loreen.local`.
- Python 3.13.5 is available.
- TensorFlow 2.21.0 imports on the Pi.
- USB microphone records through ALSA device `plughw:2,0`.
- A 4-second recording produces expected `(64000,)` audio and `(398, 40)`
  log-Mel features.
- Pi prediction scripts run on-device.

Earlier live-loop all-command Pi microphone sweep:

- 15 labels, 5 trials per label, 75 trials total.
- Correct broad-intent predictions: 47/75.
- Accepted predictions at threshold 0.90: 58/75.
- Correct accepted predictions: 43/58.
- Wrong accepted predictions: 15/58.

Interpretation of the earlier sweep:

- Pi setup is no longer the main blocker.
- Full-command recognition reliability is the main blocker.
- Strong labels can be demonstrated as evidence, but the full command set should
  not be claimed as exam-ready yet.

## Why Pi Microphone Validation Comes Before GPIO

Laptop microphone results already showed that the recording device can strongly
change performance. The Raspberry Pi microphone may have a different gain,
noise profile, distance, and frequency response. Because of that, the correct
next validation is to record a small Pi-microphone held-out set and classify it
before allowing predictions to control the LED.

## Current Limitation

The earlier broad-intent model combined phrases like "turn on the light" and
"turn off the light" into the same `LIGHT_CONTROL` intent. The current E24
model improves this by predicting raw commands first:

- `LIGHT_ON` routes to `LIGHT_CONTROL` with `light_action=on`.
- `LIGHT_OFF` routes to `LIGHT_CONTROL` with `light_action=off`.
- `NEXT`, `PAUSE`, and `STOP` route separately to media-control actions.

Remaining limitation: the model is not at the 100/100 demo target yet. E27's
guardrail policy rejects 21/95 original holdout clips to preserve zero wrong
accepted commands. That is acceptable for a safe checkpoint, but the next target
is higher accepted-correct coverage on a fresh live Pi validation set without
wrong accepted actions.

## Action Layer Prepared

An action-controller scaffold is now included in the package. It maps accepted
CNN intents to local behaviors:

- `LIGHT_CONTROL`: LED on/off/toggle/blink when a slot/action is provided.
- `LIGHT_ADJUST`: simulated brightness/color state, with optional PWM LED
  brightness.
- `SET_TIMER` and `SET_ALARM`: local state entries.
- `REMINDER`: local reminder storage/listing.
- `PLAY_MUSIC` and `MEDIA_CONTROL`: local media state and optional local WAV playback.
- `THERMOSTAT`: simulated target temperature and fan state.
- `QUESTION`: local time/weather answer when recognized, otherwise offline-safe query log.
- `CALL_MESSAGE`: offline-safe call/message log only.

This lets the project demonstrate the action architecture now without claiming
that unsupported online services or phone integration are available.

The action handlers are pre-coded. Hardware-specific visibility still depends
on available peripherals: RGB LED, buzzer, fan/motor driver, LCD, and speaker.

## Recommendation

Do not proceed directly to broad GPIO/live action activation for every command.
The next best step is a fresh E27 live validation cycle:

1. Copy the refreshed E27 package to the Raspberry Pi.
2. Record unique-file live trials for `NEXT`, `COLOR`, `STOP`, `LIGHT_ON`, and
   `LIGHT_OFF`.
3. Confirm that the refreshed default model and guardrail policy produce no
   wrong accepted commands.
4. Measure inference latency, CPU, RAM, and temperature on the Pi.
5. Enable GPIO and visible action output only after the fresh live results are
   safe.

## Next Work When Hardware Arrives

1. Record the full raw-label Pi calibration set.
2. Include labels missing from the 15-label sweep, especially `STOP`,
   `VOLUME_DOWN`, `COLOR`, and reminder creation.
3. Build a raw-command/subcommand training target so merged intents can map to
   the correct action.
4. Add targeted augmentation/guardrails for remaining weak commands, especially
   `LIGHT_OFF`, `STOP`, `COLOR`, `ALARM`, and `CREATE_REMINDER`.
5. Fine-tune with replay and evaluate on held-out Pi recordings.
6. Measure inference latency, RAM, and CPU on the Raspberry Pi.
7. Run `pi_led_test.py` to verify wiring separately.
8. Connect CNN prediction to GPIO only after recognition and wiring are both
   validated.
