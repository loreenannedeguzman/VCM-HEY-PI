# Deployment Quickstart

This repository contains the frozen E50/E37/E40 VCM deployment package for compatible Raspberry Pi 5 hardware. The deployable GUI is `deployment/vcm_pi_package/scripts/vcm_touchscreen_gui.py`, verified in this package with SHA-256 `ff8b64759b1efb93d88cc30a7a8f8d1cea7b49924cb72b19bc643c4a746a2c42`.

The GUI is an operator-facing launch/display layer around the frozen runtime. It does not retrain models, change E50 predictions, change E40 thresholds, add command classes, replace the router, or change response assets.

## 1. Hardware and OS

- Raspberry Pi 5 or compatible Raspberry Pi environment.
- Pi OS with Python 3, ALSA recording/playback tools, and a working microphone/output device.
- Local runtime only; cloud inference is not required for VCM operation.

## 2. Clone or Download

Clone or download this repository onto the Pi, then enter the deployment package:

```bash
cd deployment/vcm_pi_package
```

## 3. Configure Audio

Inspect available ALSA devices:

```bash
arecord -l
aplay -l
```

The reference project used `plughw:2,0` for microphone input and `plughw:CARD=vc4hdmi0,DEV=0` for response audio output. If the target Pi uses different devices, create a local config file:

```bash
cp deployment_config.example.json deployment_config.local.json
```

Edit `deployment_config.local.json`, then launch with:

```bash
export VCM_DEPLOYMENT_CONFIG="$PWD/deployment_config.local.json"
```

Hardware device settings do not change the frozen E37/E50/E40 recognition stack.

## 4. Set Up Python

```bash
bash scripts/setup_vcm_pi.sh
```

If system packages are missing, install the Pi OS packages required for Python virtual environments, Tkinter, and ALSA tools using the target Pi's package manager.

## 5. Run Diagnostics

```bash
bash scripts/check_vcm_pi.sh
```

The diagnostic checks Python imports, model files, normalization files, E40 policy config, router/action files, response WAV assets, GUI identity, and available audio tools. It does not modify model artifacts.

## 6. Launch the GUI

```bash
bash scripts/run_vcm_touchscreen_gui.sh
```

The GUI starts the wake-gated runtime and displays the current state, last command, last action, response status, and offline status.

## 7. Launch Runtime Without GUI

```bash
bash scripts/run_vcm.sh
```

Runtime flow:

```text
microphone -> E37 wake -> command capture -> E50 -> E40 -> deterministic router -> local action -> response WAV -> return to listening
```

## 8. Physical Test

Say `hey pi`, then one of the supported final E50 commands. The final vocabulary has 19 command classes and uses `LIGHT_DIM`; `COLOR` is not a final E50 class.

Physical microphone/output behavior depends on the target Pi hardware and ALSA configuration. This package can be statically checked off-Pi, but physical deployment should be confirmed on the target Pi before claiming a successful hardware deployment.
