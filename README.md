# E50 Voice Command Module Repository Package

This repository package contains the final E50 Voice Command Module deployment/testing package. It preserves the frozen E50/E37/E40 recognition and action stack, the supporting technical documentation, provenance records, final benchmark evidence, and a clearly separated independent E53/VCM2 experiment record.

The repository is intended for inspection and Raspberry Pi 5 deployment/testing of the frozen VCM. It is not a from-scratch retraining package.

## What Is Included

- Frozen E50 command-model documentation and final technical reports under `docs/`.
- Curated Raspberry Pi runtime package under `deployment/vcm_pi_package/`.
- Final E37 wake model and E50 command model artifacts under `deployment/vcm_pi_package/models/cnn/`.
- E40 confidence policy and runtime configs under `deployment/vcm_pi_package/configs/`.
- Deterministic action/router implementation under `deployment/vcm_pi_package/actions/`.
- Local response WAV assets under `deployment/vcm_pi_package/responses_extra_loud_20260929/`.
- Dataset inspection material under `dataset/`, including the final E50 Phase BG training manifest.
- Provenance and integrity evidence under `provenance/` and `manifests/`.
- E53/VCM2 documentation under `independent_experiment/E53/`, explicitly separated from E50.

## Frozen E50 Identity

| Component | Identity |
|---|---|
| E50 command model | `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT` |
| E37 wake model | `E37_TARGETED_COLOR_VOLUME_FIX` |
| E40 policy | `E40_NON_LED_COMMAND_GUARDRAIL_THRESHOLDS` |
| Final vocabulary | 19 labels, with `LIGHT_DIM` and not final `COLOR` |
| Wake threshold | `0.90` |
| Command default threshold | `0.90` |

The deployable GUI is `deployment/vcm_pi_package/scripts/vcm_touchscreen_gui.py`, verified with SHA-256 `ff8b64759b1efb93d88cc30a7a8f8d1cea7b49924cb72b19bc643c4a746a2c42`. The GUI launches and displays the frozen runtime. It does not change recognition, E40 thresholds, router/action semantics, command classes, model files, or benchmark definitions.

## Training Environment

The documented Phase BG run for the final E50 command model was a local Windows CPU-only TensorFlow run. The reviewed evidence records Python 3.13.6, TensorFlow 2.20.0, Keras 3.11.3, no TensorFlow GPU device detected, and TensorFlow CUDA build disabled. The repository does not claim A100 or external-cluster training for the final E50 model.

## Deployment Quickstart

Start with:

- `DEPLOYMENT_QUICKSTART.md`
- `deployment/vcm_pi_package/README_PI_DEPLOYMENT.md`
- `deployment/vcm_pi_package/deployment_config.example.json`

The primary GUI launcher is:

```bash
cd deployment/vcm_pi_package
bash scripts/run_vcm_touchscreen_gui.sh
```

The default reference audio devices are microphone input `plughw:2,0` and response audio output `plughw:CARD=vc4hdmi0,DEV=0`. Target Pi hardware can override these with `deployment_config.local.json` and the `VCM_DEPLOYMENT_CONFIG` environment variable without changing source code.

Diagnostic and setup helpers:

```bash
cd deployment/vcm_pi_package
bash scripts/setup_vcm_pi.sh
bash scripts/check_vcm_pi.sh
```

The underlying wake-gated runtime path uses `scripts/pi_wake_voice_control_demo.py`.

## Evidence Boundaries

- This package assembly did not retrain, rerun benchmarks, execute the runtime, access the Raspberry Pi, or alter source projects.
- E50 used selected collective-family/project-local command data and a separately identified 230-row E41 Pi adaptation branch; it is not claimed to be a full unchanged copy of the collective Gold Dataset.
- Recovered E37 Hey Pi recordings are documented as project-specific Raspberry Pi wake-recording evidence; the exact final E37 training rows remain not established.
- E53/VCM2 is retained only as an independent experiment and is not the deployed E50 system.
- Third-party dataset terms remain applicable. Raw third-party audio is not redistributed merely to make the repository appear self-contained.

## Repository Map

| Path | Purpose |
|---|---|
| `deployment/vcm_pi_package/` | Curated deployable Raspberry Pi package. |
| `dataset/` | Final E50 training manifest and dataset-provenance inspection docs. |
| `docs/01_REQUIREMENTS` | Requirements and traceability. |
| `docs/02_FINAL_SYSTEM` | Final E50 system architecture and identities. |
| `docs/03_ENGINEERING_HISTORY` | Curated development history. |
| `docs/04_VALIDATION` | Validation methodology and evidence boundaries. |
| `docs/05_RESULTS` | Canonical final metrics. |
| `docs/06_REPRODUCTION` | Deployment/reproduction guidance and limitations. |
| `docs/07_INTEGRITY` | Artifact identity, hashes, and provenance boundaries. |
| `docs/08_DEMO` | Operator procedure and command reference. |
| `provenance/` | Dataset, E37 recording, and documentation provenance audits. |
| `independent_experiment/E53/` | Independent E53/VCM2 documentation. |
| `manifests/` | Package assembly and integrity manifests. |

## Package Manifest

See `manifests/REPOSITORY_PACKAGE_MANIFEST_20261002.md`. That manifest intentionally excludes its own SHA256 from the checksum table to avoid a false self-referential hash.

