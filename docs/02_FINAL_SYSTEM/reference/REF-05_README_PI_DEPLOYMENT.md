# VCM Raspberry Pi 5 Deployment Package

This folder is the offline deployment package for the ME2 Voice Command Model.
It is prepared for Raspberry Pi 5 live microphone validation and local
record-then-infer demos. GPIO/LED control should be enabled only after the
selected command route has passed held-out Pi microphone validation.

## Final Included Model

Default model:

- Wake model: `E37_TARGETED_COLOR_VOLUME_FIX`
- Command model: `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT`
- Purpose: final Phase BM baseline for defensible E50 demo preparation
- Input: 4-second mono WAV, standardized to 16 kHz
- Feature: log-Mel spectrogram, shape `398 x 40 x 1`
- Output: one of 19 revised raw command labels, using `LIGHT_DIM` instead of
  historical `COLOR`
- Wake threshold: `0.90`
- Command default confidence threshold: `0.90`
- Command guardrail policy: `configs/e50_revised_vocab_e40_thresholds.json`
- E50 weights SHA256:
  `bc8ac64ced4305ddf43bf4de377f3cc636a764eff339cd9f92af06340c50b8ff`
- E52 is rejected and must not be deployed as the final model.

Command routing:

- The command CNN predicts raw command labels such as `LIGHT_ON`, `LIGHT_OFF`,
  `LIGHT_DIM`, `NEXT`, `PAUSE`, `WEATHER`, and `TIMER`.
- `actions/raw_command_router.py` maps those raw labels to the assignment
  intent/action layer, for example `LIGHT_ON -> LIGHT_CONTROL` with
  `light_action=on`.
- The model does not transcribe speech and does not use ASR, cloud APIs, or an
  LLM. It is a fixed-vocabulary voice command classifier.
- GPIO remains off unless `--enable-gpio` is explicitly passed.

Measured evidence for the final E50 stack:

- E50 current95-compatible offline: `83/90 = 92.22%`.
- E50 Phase AV-compatible offline: `139/194 = 71.65%`.
- E50 Phase AV-compatible accepted-wrong: `8`.
- BI live wake-gated Raspberry Pi evidence: wake `36/36`, raw command
  recognition `24/35`, accepted-correct `15`, accepted-wrong `1`, UNKNOWN
  safe rejection `1/1`.
- BK targeted weak-command evidence recovered `CREATE_REMINDER`, but
  `TIME`, `BRIGHTNESS`, `TEMPERATURE`, `VOLUME_UP`, `VOLUME_DOWN`, and `CALL`
  are not final-demo-ready.

Guardrail policy:

- `configs/e50_revised_vocab_e40_thresholds.json`
- Purpose: deployment-compatible copy of the frozen E40 policy for the revised
  `LIGHT_DIM` E50 vocabulary.
- Important caveat: do not lower thresholds to recover weak commands.
  `TEMPERATURE` produced accepted-wrong live actions and is excluded from the
  final demo.

Older E33/E32/E31/E30/E28/E27/E26/E24 raw-command models and broad-intent
models may remain in the package as historical artifacts, but they are not the
final default and should not be presented as the Phase BM final model.

## Pi Setup From a Fresh Raspberry Pi OS Unit

1. Flash Raspberry Pi OS to the microSD card.
2. Boot the Raspberry Pi 5 and complete first-run setup.
3. Connect to Wi-Fi only for setup if needed. The project itself is prepared to
   run offline after dependencies and package files are installed.
4. Open Terminal on the Pi.
5. Update system packages:

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip python3-scipy alsa-utils python3-gpiozero
```

6. Copy this `vcm_pi_package` folder to the Pi, for example:

```bash
scp -r vcm_pi_package pi@raspberrypi.local:/home/pi/
```

7. Create a virtual environment:

```bash
cd /home/pi/vcm_pi_package
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements_pi.txt
```

If TensorFlow installation fails on the Pi, use the Raspberry Pi OS-compatible
TensorFlow package available for that OS/Python version, then rerun the import
check below.

## Sanity Checks

Check Python imports:

```bash
source /home/pi/vcm_pi_package/.venv/bin/activate
python -c "import numpy, scipy, tensorflow; print('imports ok')"
```

Check microphone devices:

```bash
arecord -l
```

Record one 4-second test WAV:

```bash
mkdir -p pi_recordings
arecord -r 16000 -c 1 -f S16_LE -d 4 pi_recordings/test.wav
```

If the USB microphone appears as a non-default ALSA device, include `-D`, for
example:

```bash
arecord -D plughw:1,0 -r 16000 -c 1 -f S16_LE -d 4 pi_recordings/test.wav
```

Run prediction on a WAV:

```bash
python scripts/predict_wav_pi.py pi_recordings/test.wav
```

Run prediction with the default E33 guardrail threshold policy:

```bash
python scripts/predict_wav_pi.py pi_recordings/test.wav
```

Run record-and-predict in dry-run mode:

```bash
python scripts/pi_voice_control_demo.py --duration-sec 4
```

Run record-and-predict with the default E33 guardrail threshold policy:

```bash
python scripts/pi_voice_control_demo.py --duration-sec 4
```

Run record-and-predict with a specific ALSA device:

```bash
python scripts/pi_voice_control_demo.py --device plughw:1,0 --duration-sec 4
```

## LED Wiring Check

Recommended simple LED wiring:

- Raspberry Pi GPIO17, physical pin 11, to resistor
- Resistor to LED anode
- LED cathode to ground, for example physical pin 6
- Use a current-limiting resistor, commonly 220 ohm to 330 ohm

After wiring:

```bash
python scripts/pi_led_test.py --pin 17
```

## Controlled GPIO Demo

Use this only after the microphone validation looks acceptable. By default,
`pi_voice_control_demo.py` does not apply GPIO actions.

Example controlled blink when `LIGHT_ON` or `LIGHT_OFF` routes to
`LIGHT_CONTROL`:

```bash
python scripts/pi_voice_control_demo.py --threshold 0.95 --enable-gpio --light-action blink
```

Example controlled test for a known "turn on the light" recording session:

```bash
python scripts/pi_voice_control_demo.py --threshold 0.95 --enable-gpio --light-action on
```

This remains controlled because GPIO should be enabled only after the route
being demonstrated is behaving safely on held-out Pi recordings.

## Action Layer

The package includes `actions/command_actions.py`, a local action controller
that can execute or simulate all assignment intents.

Dry-run examples:

```bash
python actions/command_actions.py --intent QUESTION --phrase "what time is it?"
python actions/command_actions.py --intent QUESTION --phrase "what is the weather?"
python actions/command_actions.py --intent PLAY_MUSIC --phrase "play music"
python actions/command_actions.py --intent SET_TIMER --phrase "set a timer for 5 minutes"
python actions/command_actions.py --intent SET_TIMER --phrase "set a timer for five minutes"
python actions/command_actions.py --intent SET_ALARM --phrase "set an alarm for 6 am"
python actions/command_actions.py --intent THERMOSTAT --phrase "set temperature to 24 degrees"
python actions/command_actions.py --intent LIGHT_ADJUST --phrase "dim lights to 10 percent"
python actions/command_actions.py --intent REMINDER --phrase "remind me to check the rice"
python actions/command_actions.py --intent CALL_MESSAGE --phrase "call mom"
```

For live prediction, `pi_voice_control_demo.py` now calls the same action layer
after CNN inference. With the default E33 model, it first routes the raw command
label to the correct broad intent and slots:

```bash
python scripts/pi_voice_control_demo.py --threshold 0.95 --phrase "turn on the light"
```

Keep `--enable-gpio` off during microphone validation. Add it only after
prediction behavior is acceptable:

```bash
python scripts/pi_voice_control_demo.py --threshold 0.95 --phrase "turn on the light" --enable-gpio
```

## Wake-Gated Demo

The final demo should be wake-gated. The selected wake phrase is:

```text
hey pi
```

Record fresh wake and UNKNOWN/false-wake examples:

```bash
python scripts/record_pi_wake_set.py --device plughw:2,0 --duration-sec 4 --output-dir pi_validation/wake_validation_hey_pi
```

After a wake-aware model has been trained and copied into the package, run the
two-stage demo. The script can use one model for both stages, but the preferred
2026-09-23 architecture is separate:

```text
wake model -> command model -> raw-command router -> local action
```

This is useful because wake detection and command/action recognition have
different error priorities. The wake model should minimize false wake events;
the command model should preserve correct action routing after wake.

Two-checkpoint example:

```bash
python scripts/pi_wake_voice_control_demo.py \
  --device plughw:2,0 \
  --wake-duration-sec 4 \
  --command-duration-sec 4 \
  --wake-experiment-id E37_TARGETED_COLOR_VOLUME_FIX \
  --wake-threshold 0.90 \
  --wake-threshold-policy "" \
  --command-experiment-id E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT \
  --command-threshold-policy configs/e50_revised_vocab_e40_thresholds.json \
  --cnn-config configs/cnn_fastbn_dense_nodropout_raw19.json
```

For final validation evidence, add a trial id and evidence folder. This saves
the wake WAV, command WAV, and JSON result together:

```bash
python scripts/pi_wake_voice_control_demo.py \
  --device plughw:2,0 \
  --wake-duration-sec 4 \
  --command-duration-sec 4 \
  --wake-experiment-id E37_TARGETED_COLOR_VOLUME_FIX \
  --wake-threshold 0.90 \
  --wake-threshold-policy "" \
  --command-experiment-id E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT \
  --command-threshold-policy configs/e50_revised_vocab_e40_thresholds.json \
  --cnn-config configs/cnn_fastbn_dense_nodropout_raw19.json \
  --evidence-dir pi_validation/wake_gated_live_20260923 \
  --trial-id wake_stop_001 \
  --expected-wake "hey pi" \
  --expected-command "stop"
```

Broad-category safety note:

E50 is the selected Phase BG offline command candidate, but it still requires
fresh Raspberry Pi end-to-end validation. Keep `--enable-gpio` off until the
selected stack has passed live wake-command-action tests. The E50 policy file is
a deployment-compatible copy of frozen E40 guardrails for the revised
`LIGHT_DIM` vocabulary; it is not a tuned threshold policy.

```bash
python scripts/pi_wake_voice_control_demo.py \
  --device plughw:2,0 \
  --wake-duration-sec 4 \
  --command-duration-sec 4 \
  --wake-experiment-id E37_TARGETED_COLOR_VOLUME_FIX \
  --wake-threshold 0.90 \
  --wake-threshold-policy "" \
  --command-experiment-id E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT \
  --command-threshold-policy configs/e50_revised_vocab_e40_thresholds.json \
  --cnn-config configs/cnn_fastbn_dense_nodropout_raw19.json \
  --evidence-dir pi_validation/e50_wake_gated_live_20260928 \
  --trial-id e50_wake_temperature_001 \
  --expected-wake "hey pi" \
  --expected-command "temperature"
```

Backward-compatible single-checkpoint example:

```bash
python scripts/pi_wake_voice_control_demo.py --device plughw:2,0 --wake-duration-sec 4 --command-duration-sec 4
```

Persistent five-cycle final demo example. Models are loaded once at startup,
then the program returns to listening after each command:

```bash
python scripts/pi_wake_voice_control_demo.py \
  --device plughw:2,0 \
  --wake-duration-sec 4 \
  --command-duration-sec 4 \
  --cycles 5 \
  --evidence-dir pi_validation/e50_bm_final_demo_20260928 \
  --trial-id e50_bm_demo \
  --expected-wake "hey pi" \
  --enable-response-audio
```

Use `--continuous` instead of `--cycles 5` only for an unattended live demo.

## Touchscreen GUI

The package includes a small native Tkinter GUI for the Raspberry Pi
touchscreen. The GUI is only a local START / STOP / STATUS controller. It does
not replace the microphone, wake model, command CNN, confidence policy, router,
or action layer.

Run it from the Pi package root:

```bash
cd ~/vcm_pi_package
source .venv/bin/activate
export DEV=plughw:2,0
export RESPONSE_AUDIO_DEVICE=plughw:CARD=vc4hdmi0,DEV=0
bash scripts/run_vcm_touchscreen_gui.sh
```

The GUI starts `scripts/pi_wake_voice_control_demo.py` in continuous mode,
prevents duplicate runtime starts, stops the child runtime cleanly, and reads
the latest result JSON from its evidence directory to display the last command,
action, and response status.

Optional desktop launcher:

```bash
cp vcm_touchscreen_gui.desktop ~/Desktop/
chmod +x ~/Desktop/vcm_touchscreen_gui.desktop
chmod +x scripts/run_vcm_touchscreen_gui.sh
```

If the Pi username or package path is not `/home/pi/vcm_pi_package`, edit only
the desktop file path. Do not edit model, threshold, label, or router settings
for the GUI.

## Human Response WAV Recording

Final demo response audio must be recorded human speech. Placeholder tones are
useful only for audio-path smoke testing and are not final command responses.

On the Raspberry Pi, record one human response per command:

```bash
cd ~/vcm_pi_package
source .venv/bin/activate
python scripts/record_human_command_responses.py \
  --device plughw:2,0 \
  --duration-sec 3 \
  --backup-existing \
  --overwrite
```

The recorder prompts for each command response, writes the WAVs into
`responses/`, backs up existing placeholder files, and creates
`PHASE_BN_HUMAN_RESPONSE_RECORDING_MANIFEST.csv`.

Then verify format and duration:

```bash
python scripts/verify_human_command_responses.py
```

This verification does not prove the content is human speech by itself. Before
final demo, play the responses through the actual Pi speaker path and confirm
they are audible, intelligible human voice responses.

## Phase BN Audio-First Final Validation

Phase BN preserves the complete 19-command vocabulary. The current 13-command
demo subset is not a runtime whitelist. `TIME`, `BRIGHTNESS`, `TEMPERATURE`,
`VOLUME_UP`, `VOLUME_DOWN`, and `CALL` remain callable/testable. `TEMPERATURE`
is callable but not demo-safe until remediated because accepted-wrong live
actions were observed.

Before running all-19 validation, diagnose response playback:

```bash
cd ~/vcm_pi_package
source .venv/bin/activate
bash scripts/run_phase_bn_audio_diagnostics.sh
```

If a specific ALSA output works, use it for response WAV playback:

```bash
export RESPONSE_AUDIO_DEVICE=plughw:X,Y
```

Then run the small smoke sequence:

```bash
export DEV=plughw:2,0
bash scripts/run_phase_bn_audio_smoke.sh
```

Only after audio smoke validation is usable, run the all-19 callable-command
validation:

```bash
export EVID=pi_validation/e50_bn_all19_validation_20260928
bash scripts/run_phase_bn_all19_prompted_validation.sh
```

These scripts do not train, tune thresholds, modify E37/E40/E50, or restrict
the runtime vocabulary.

Expected behavior:

- `hey pi` opens the command window.
- `hey siri`, `hey google`, `alexa`, `hello`, silence/noise, and random speech
  do not open the command window.
- Commands spoken before a valid wake do not execute.
- Ordinary commands used as false-wake probes keep their true labels; they are
  no-action in the wake stage because the gate opens only for accepted `WAKE`.
- After a valid wake, one accepted command routes to its local action.
- `UNKNOWN` and `WAKE` are no-action safety labels.

Action notes:

- LED on/off/brightness can be connected to GPIO.
- Time and weather questions are already pre-coded as local answers.
- Timers, alarms, thermostat, media, reminders, calls, messages, and display
  outputs are stored as local demo state unless a real service/device is later added.
- Local WAV files placed in `music/` can be played with `aplay` when
  `--enable-local-audio` is used.
- Search, calls, and messaging are intentionally not connected to online
  services because final inference/demo must run locally and offline.

