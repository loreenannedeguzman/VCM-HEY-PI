# 07 - Raspberry Pi Deployment

## What Actually Runs On The Raspberry Pi

The final Raspberry Pi deployment runs a local wake-gated VCM stack: E37 wake inference, E50 command inference, E40 confidence policy, deterministic raw-command routing, local action handling, local response WAV playback, and return-to-listening behavior. It runs offline after setup and does not require cloud ASR, an LLM, remote Python service, laptop microphone, or laptop speaker during verified standalone operation. [REF-03] [REF-05]

## Hardware And Environment

The target hardware is Raspberry Pi 5. The adjusted package README records local Pi microphone configuration `plughw:2,0` and local Pi HDMI audio output `plughw:CARD=vc4hdmi0,DEV=0` for final package context. [REF-03] [REF-05] [REF-15]

The recovered E37 wake-recording manifest also records `plughw:2,0` as the input device for all 99 project-specific wake-stage recordings in `/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi/manifest.csv`. This is recording provenance evidence, not a rerun of the final deployment benchmark. [REF-17]

## Frozen Runtime Components

| Component | Runtime artifact / evidence |
|---|---|
| Wake model | `models/cnn/E37_TARGETED_COLOR_VOLUME_FIX_weights.npz` and normalization. [REF-13] |
| Command model | `models/cnn/E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT_weights.npz` and normalization. [REF-13] |
| Command threshold policy | `configs/e50_revised_vocab_e40_thresholds.json`. [REF-07] |
| Preprocessing | `configs/preprocessing.json`; 16 kHz mono 4-second log-Mel setup. [REF-06] |
| Wake-command runtime | `scripts/pi_wake_voice_control_demo.py`. [REF-06] |
| GUI launcher | `scripts/run_vcm_touchscreen_gui.sh` and `scripts/vcm_touchscreen_gui.py`. [REF-06] [REF-15] |
| Router/action layer | `actions/raw_command_router.py`, `actions/command_actions.py`. [REF-08] [REF-09] |
| Response audio map | `configs/demo_response_assets.json`. [REF-10] |

## Launch Mechanism

The final GUI launch path starts from the package root, activates the Python environment, sets microphone and response-audio devices, and runs the touchscreen GUI launcher. [REF-05] [REF-15]

```bash
cd ~/vcm_pi_package
source .venv/bin/activate
export DEV=plughw:2,0
export RESPONSE_AUDIO_DEVICE=plughw:CARD=vc4hdmi0,DEV=0
bash scripts/run_vcm_touchscreen_gui.sh
```

Some older documentation examples mention other HDMI device names. Use the configured device that matches the actual Pi audio output evidence for the deployment being demonstrated. [REF-03] [REF-05] [REF-15]

## Runtime Flow

```text
Open VCM Offline / run GUI launcher
  -> press START LISTENING
  -> GUI starts wake-gated runtime
  -> say "Hey Pi"
  -> E37 accepts wake
  -> speak command
  -> E50 predicts label
  -> E40 accepts or rejects
  -> accepted label routes to local action
  -> response WAV plays
  -> runtime returns to listening
  -> press STOP VCM when done
```

## GPIO State

GPIO remains off unless explicitly enabled. The technical package documentation should describe local actions and response audio rather than implying live physical GPIO control unless separately demonstrated. [REF-05]

## Evidence Output

The deployment README explains that validation runs can save wake WAVs, command WAVs, and JSON result files into an evidence directory. The GUI reads the latest result JSON for status display. [REF-05]

Separate from the final benchmark evidence, the recovered E37 audit identifies the original `Hey Pi` wake-recording resource and manifest on the Raspberry Pi. Those 99 wake-stage recordings are not copied into this documentation package and should not be treated as the final 20-trial Pi benchmark population. [REF-17]

## Deployment Boundary

This deployment section distinguishes the frozen VCM core from the post-freeze enhanced DUi/GUI. The GUI launches and displays the runtime; it does not alter the model, thresholds, vocabulary, router, or response assets. [REF-05] [REF-06] [REF-15]

