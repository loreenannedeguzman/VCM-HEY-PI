# VCM Raspberry Pi 5 Deployment Package

This folder is the runnable offline deployment package for the final E50 Voice Command Module on Raspberry Pi 5.

The package runs a fixed-vocabulary local command-recognition stack. It does not use cloud speech recognition, an LLM, online ASR, or arbitrary speech transcription.

## Runtime Stack

```text
Microphone
  -> E37 wake detector
  -> post-wake command capture
  -> 16 kHz / 4 s log-Mel preprocessing
  -> E50 command CNN
  -> E40 confidence / rejection policy
  -> deterministic command router
  -> local action
  -> local response WAV
  -> return to listening
```

## Final Included Models And Policy

| Component | Runtime artifact |
|---|---|
| Wake model | `models/cnn/E37_TARGETED_COLOR_VOLUME_FIX_weights.npz` |
| Wake normalization | `models/cnn/E37_TARGETED_COLOR_VOLUME_FIX_normalization.npz` |
| Wake labels | `results/tables/E37_TARGETED_COLOR_VOLUME_FIX_labels.json` |
| Command model | `models/cnn/E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT_weights.npz` |
| Command normalization | `models/cnn/E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT_normalization.npz` |
| Command labels | `results/tables/E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT_labels.json` |
| CNN config | `configs/cnn_fastbn_dense_nodropout_raw19.json` |
| E40 threshold policy | `configs/e50_revised_vocab_e40_thresholds.json` |
| Preprocessing config | `configs/preprocessing.json` |
| Response map | `configs/demo_response_assets.json` |

Important identities:

| Artifact | SHA-256 |
|---|---|
| E50 weights | `BC8AC64CED4305DDF43BF4DE377F3CC636A764EFF339CD9F92AF06340C50B8FF` |
| E37 weights | `687E82E2CEFA6D74CEF2C0A15D28F8F6142D47D4A67E57C68C091E83FC2CEBDE` |
| E40 config | `A0B2495328FD5A1E0E5885E727623BA6D9F823BE94CCCDFD0AEAD77254BBB3FD` |
| GUI | `FF8B64759B1EFB93D88CC30A7A8F8D1CEA7B49924CB72B19BC643C4A746A2C42` |

## Final Command Vocabulary

The final E50 command model has 19 labels:

```text
PLAY_MUSIC, WEATHER, TIME, LIGHT_ON, LIGHT_OFF, LIGHT_DIM, BRIGHTNESS, TIMER,
ALARM, TEMPERATURE, NEXT, PAUSE, STOP, VOLUME_UP, VOLUME_DOWN,
CREATE_REMINDER, LIST_REMINDERS, CALL, MESSAGE
```

`LIGHT_DIM` is the final E50 class. Historical `COLOR` is not a final E50 command class. `COLOR` still appears in the E37 wake-label map because E37 was trained as a wake-stage model with additional false-wake/targeted labels.

## Raspberry Pi Setup

From a fresh Raspberry Pi OS system:

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip python3-scipy python3-tk alsa-utils
```

Enter this deployment directory after cloning or copying the repository:

```bash
cd "VCM-HEY-PI/4b - DEPLOYMENT/vcm_pi_package"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements_pi.txt
```

If TensorFlow installation fails, use the Raspberry Pi OS-compatible TensorFlow package for the installed OS/Python version. Then verify imports:

```bash
python -c "import numpy, scipy, tensorflow; print('imports ok')"
```

## Audio Device Checks

List input and output devices:

```bash
arecord -l
aplay -l
```

Record a 4-second test WAV:

```bash
mkdir -p pi_recordings
arecord -D plughw:2,0 -r 16000 -c 1 -f S16_LE -d 4 pi_recordings/test.wav
```

If the microphone is not `plughw:2,0`, use the device shown by `arecord -l`.

## Run A Saved-WAV Prediction Smoke Test

```bash
python scripts/predict_wav_pi.py pi_recordings/test.wav
```

This checks that TensorFlow, preprocessing, model weights, normalization, labels, and threshold policy can load together. It is not a benchmark.

## Run The Touchscreen GUI

```bash
export DEV=plughw:2,0
export RESPONSE_AUDIO_DEVICE=plughw:CARD=vc4hdmi0,DEV=0
bash scripts/run_vcm_touchscreen_gui.sh
```

The GUI starts `scripts/pi_wake_voice_control_demo.py` in continuous mode. It displays wake/command status, last command, last action, and response playback status. The GUI is an interface and launcher; it does not replace E37, E50, E40, the router, or the response WAVs.

If the shell file is not executable after a zip download, run either:

```bash
bash scripts/run_vcm_touchscreen_gui.sh
```

or:

```bash
chmod +x scripts/run_vcm_touchscreen_gui.sh
./scripts/run_vcm_touchscreen_gui.sh
```

## Direct Wake-Gated Runtime Command

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
  --response-map configs/demo_response_assets.json \
  --enable-response-audio \
  --continuous
```

## Response Audio

The active response map is `configs/demo_response_assets.json`. It points to `responses_extra_loud_20260929/`. All mapped response WAVs are included in this package, including `rejected_extra_loud.wav` for `UNKNOWN` / rejection behavior.

## Desktop Launcher

The optional file `vcm_touchscreen_gui.desktop` can be copied to the Pi desktop. If the repository is not installed at the hardcoded path in that file, edit only the desktop launcher path:

```text
Path=...
Exec=.../scripts/run_vcm_touchscreen_gui.sh
```

Do not edit model, label, threshold, router, or response configuration just to use the desktop launcher.

## What This Package Does Not Do

- It does not retrain E37 or E50.
- It does not rerun benchmarks automatically.
- It does not require ME2_VCM or FINAL SUBMISSION VCM at runtime.
- It does not require E53.
- It does not use cloud inference, online ASR, or an LLM.
- It does not guarantee the professor's Pi audio device names match `plughw:2,0` or `plughw:CARD=vc4hdmi0,DEV=0`; those may need local adjustment.

## Validation Boundary

The package now contains the runtime metadata required by the predictor and current deployment instructions. Physical Raspberry Pi revalidation is still a separate action and was not rerun by this packaging repair.

