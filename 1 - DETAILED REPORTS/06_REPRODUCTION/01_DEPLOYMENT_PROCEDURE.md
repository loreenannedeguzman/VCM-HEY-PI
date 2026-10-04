# Deployment Procedure

## Frozen Core Launch Concept

The frozen core is launched from the Raspberry Pi package root using the documented runner:

```bash
cd ~/vcm_pi_package
bash scripts/run_vcm_touchscreen_gui.sh
```

The runner represents the frozen E37/E50/E40 command path. The post-freeze DUi/GUI is an interface layer around this core and must not be described as a retrained E50 model.

## Expected Runtime Flow

1. The microphone listens for the E37 wake phrase.
2. A successful wake opens the command window.
3. The system captures the command WAV.
4. Log-Mel preprocessing feeds the E50 CNN.
5. E40 applies the confidence/rejection policy.
6. Accepted labels route to deterministic local actions.
7. Local response audio is played.
8. The system returns to listening.

## Devices

| Device role | Documented value |
|---|---|
| Wake/command microphone | plughw:2,0 |
| Local response audio | plughw:CARD=vc4hdmi0,DEV=0 |

## What This Document Does Not Do

This document does not execute the runtime, test the Pi, alter devices, install dependencies, regenerate models, or run benchmarks.

