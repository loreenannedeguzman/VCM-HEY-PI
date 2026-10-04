# Deployment Quickstart

This repository contains a runnable Raspberry Pi 5 deployment package for the final E50 VCM stack.

## What Runs

The runnable package is:

```text
4b - DEPLOYMENT/vcm_pi_package
```

Runtime stack:

```text
Microphone -> E37 wake detector -> command capture -> log-Mel preprocessing -> E50 command CNN -> E40 confidence guardrail -> deterministic router -> local action -> response WAV -> return to listening
```

Final runtime identities:

| Component | Value |
|---|---|
| Wake model | `E37_TARGETED_COLOR_VOLUME_FIX` |
| Command model | `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT` |
| Confidence policy | `configs/e50_revised_vocab_e40_thresholds.json` |
| GUI launcher | `scripts/run_vcm_touchscreen_gui.sh` |
| GUI file | `scripts/vcm_touchscreen_gui.py` |
| Response map | `configs/demo_response_assets.json` |

## Fresh Raspberry Pi 5 Setup

On the Pi:

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip python3-scipy python3-tk alsa-utils
```

Copy or clone the repository, then enter the package directory:

```bash
cd "VCM-HEY-PI/4b - DEPLOYMENT/vcm_pi_package"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements_pi.txt
```

If TensorFlow is not available for the Pi's Python version through ordinary pip, install the Raspberry Pi OS-compatible TensorFlow package for that OS/Python version, then rerun the import check.

## Sanity Checks

```bash
python -c "import numpy, scipy, tensorflow; print('imports ok')"
arecord -l
aplay -l
```

Record a short microphone test:

```bash
mkdir -p pi_recordings
arecord -D plughw:2,0 -r 16000 -c 1 -f S16_LE -d 4 pi_recordings/test.wav
```

Adjust `plughw:2,0` if `arecord -l` shows a different microphone device.

## Launch the GUI

```bash
export DEV=plughw:2,0
export RESPONSE_AUDIO_DEVICE=plughw:CARD=vc4hdmi0,DEV=0
bash scripts/run_vcm_touchscreen_gui.sh
```

The launcher changes into the package root before starting the GUI, so it does not require the package to live at a fixed absolute path.

## Optional Direct Runtime Command

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

## Required Runtime Metadata

The package includes the label maps required by `scripts/predict_wav_pi.py`:

```text
results/tables/E37_TARGETED_COLOR_VOLUME_FIX_labels.json
results/tables/E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT_labels.json
```

Without these files the CNN predictor cannot map output indices to labels.

## Desktop Launcher Note

`vcm_touchscreen_gui.desktop` is optional. If using it, edit its `Path=` and `Exec=` entries if the repository is not installed at the path shown in that desktop file. The shell launcher itself can be run directly from any clone path.

## Validation Boundary

This package was made deployable from the repository by restoring required runtime metadata and current deployment instructions. This does not rerun physical Raspberry Pi validation, retrain models, alter thresholds, or change benchmark results.

