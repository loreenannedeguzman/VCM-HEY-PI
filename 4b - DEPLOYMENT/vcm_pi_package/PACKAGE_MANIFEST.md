# Deployment Package Manifest

This manifest describes the files currently included in `4b - DEPLOYMENT/vcm_pi_package` for the runnable GitHub deployment package.

## Runtime Entry Points

| File | Purpose |
|---|---|
| `scripts/run_vcm_touchscreen_gui.sh` | Shell launcher for the touchscreen GUI. |
| `scripts/vcm_touchscreen_gui.py` | Tkinter GUI / runtime controller. |
| `scripts/pi_wake_voice_control_demo.py` | Wake-gated continuous runtime. |
| `scripts/pi_voice_control_demo.py` | Single-stage command runtime / utility. |
| `scripts/predict_wav_pi.py` | Saved-WAV prediction helper and reusable predictor. |

## Models, Normalization, And Labels

| File | Purpose |
|---|---|
| `models/cnn/E37_TARGETED_COLOR_VOLUME_FIX_weights.npz` | Final wake-gate model weights. |
| `models/cnn/E37_TARGETED_COLOR_VOLUME_FIX_normalization.npz` | E37 normalization values. |
| `results/tables/E37_TARGETED_COLOR_VOLUME_FIX_labels.json` | E37 output-index to label map. |
| `models/cnn/E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT_weights.npz` | Final E50 command model weights. |
| `models/cnn/E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT_normalization.npz` | E50 normalization values. |
| `results/tables/E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT_labels.json` | E50 output-index to label map. |

## Configuration

| File | Purpose |
|---|---|
| `configs/cnn_fastbn_dense_nodropout_raw19.json` | CNN architecture/input configuration. |
| `configs/preprocessing.json` | 16 kHz / 4 s log-Mel preprocessing configuration. |
| `configs/e50_revised_vocab_e40_thresholds.json` | Frozen E40-compatible confidence policy for E50. |
| `configs/demo_response_assets.json` | Label-to-response-WAV map. |

## Runtime Support Code

| Directory/File | Purpose |
|---|---|
| `preprocessing/` | WAV loading, resampling, peak normalization, log-Mel extraction. |
| `training/cnn_model.py` | CNN construction used by runtime model loading. |
| `training/baseline_features.py` | Preprocessing config loader used by runtime. |
| `actions/raw_command_router.py` | Deterministic raw-label to action/intent routing. |
| `actions/command_actions.py` | Local action execution/simulation. |

## Response Audio

The active response directory is:

```text
responses_extra_loud_20260929/
```

It contains mapped WAV responses for the 19 E50 command labels and `UNKNOWN` rejection behavior. The response map is `configs/demo_response_assets.json`.

## Setup / Documentation

| File | Purpose |
|---|---|
| `README_PI_DEPLOYMENT.md` | Current Pi setup and runtime instructions. |
| `requirements_pi.txt` | Pip-level Python dependencies: `numpy`, `scipy`, `tensorflow`. |
| `PI_MIC_VALIDATION_PROTOCOL.md` | Microphone validation notes. |
| `REPORT_PI_DEPLOYMENT_READINESS.md` | Historical readiness report; not the current quickstart. |
| `ACTION_LAYER_DESIGN.md` | Action-layer design note. |

## Optional Launcher

| File | Note |
|---|---|
| `vcm_touchscreen_gui.desktop` | Optional desktop launcher. Edit `Path=` and `Exec=` if the clone path differs. |

## Runtime Boundary

The package is intended to run from this repository without requiring:

- `ME2_VCM`
- `FINAL SUBMISSION VCM`
- `E53`
- Windows home-directory paths
- `/home/loreenanne`

The optional desktop file is the only artifact with a fixed path and should be adjusted locally if used.

## Validation Boundary

This manifest records package contents. It does not claim that a new physical Raspberry Pi benchmark was rerun after this packaging repair.

