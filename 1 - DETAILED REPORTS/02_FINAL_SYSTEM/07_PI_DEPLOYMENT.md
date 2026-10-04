# Raspberry Pi Deployment

## Engineering Question

What actually runs on the Raspberry Pi, and how does the deployment package relate to the documentation?

The Raspberry Pi deployment package runs the frozen wake-gated E50 VCM core locally. It does not require cloud ASR, an LLM, a remote Python service, a laptop microphone, or a laptop speaker during standalone operation after setup. The deployment folder is the runnable artifact; the surrounding documentation explains and evidences it.

## Runtime Stack

```text
GUI / launcher
  -> pi_wake_voice_control_demo.py
  -> local microphone input
  -> E37 wake detector
  -> command capture
  -> preprocessing / log-Mel features
  -> E50 command CNN
  -> E40 threshold policy
  -> deterministic router
  -> local action layer
  -> local response WAV playback
  -> return to listening
```

## Hardware And Audio Path

| Item | Documented value |
|---|---|
| Target hardware | Raspberry Pi 5 |
| Wake/command input device context | `plughw:2,0` |
| Response audio output context | `plughw:CARD=vc4hdmi0,DEV=0` |
| Runtime mode | Offline/local after setup |
| GPIO | Off unless explicitly enabled |

The recovered E37 manifest also records `plughw:2,0` for all 99 project-specific wake-stage recordings. That is wake-recording provenance, not a rerun of the final physical benchmark.

## Frozen Runtime Components

| Component | Runtime artifact |
|---|---|
| Wake model | `models/cnn/E37_TARGETED_COLOR_VOLUME_FIX_weights.npz` and normalization |
| Command model | `models/cnn/E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT_weights.npz` and normalization |
| Threshold policy | `configs/e50_revised_vocab_e40_thresholds.json` |
| Preprocessing | `configs/preprocessing.json` and preprocessing Python modules |
| Wake-command runtime | `scripts/pi_wake_voice_control_demo.py` |
| GUI launcher | `scripts/run_vcm_touchscreen_gui.sh`, `scripts/vcm_touchscreen_gui.py` |
| Router/action layer | `actions/raw_command_router.py`, `actions/command_actions.py` |
| Response assets | `configs/demo_response_assets.json`, `responses_extra_loud_20260929/` |

## Launch Path

From the deployment package root:

```bash
cd "4b - DEPLOYMENT/vcm_pi_package"
bash scripts/run_vcm_touchscreen_gui.sh
```

The GUI starts the wake-gated runtime. A typical operator flow is: open VCM Offline, press START LISTENING, say `Hey Pi`, speak a supported command, observe the local action/response, and press STOP VCM when done.

## What The Deployment Package Does

The deployment package provides the actual runtime files: models, normalization artifacts, configuration, preprocessing modules, command router, action layer, response WAVs, scripts, and GUI launcher. The documentation does not replace these files. It explains their role, identity, and evidence boundaries.

## Evidence Output

Validation runs can save wake WAVs, command WAVs, and JSON result files into an evidence directory. The GUI reads recent result JSON for status display. This telemetry/display behavior is observational; it does not retrain or alter the frozen recognition/action core.

## Boundary

Do not infer from this deployment documentation that physical Pi revalidation was rerun after packaging. The package is deployable from the included runtime material, but the documented final physical benchmark remains the established 20-trial benchmark evidence.
