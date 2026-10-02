# ME2 VCM - Final E50 Raspberry Pi Voice Command System

## Project Purpose

This repository is the technical delivery package for the Machine Exercise 2 Voice Command Model (VCM). The goal was to build a small offline Raspberry Pi voice-command system that classifies fixed smart-device commands locally, routes accepted commands to deterministic actions, plays recorded local responses, and returns to listening without cloud ASR, an LLM, or remote inference.

## Final System Summary

The final delivery project is **E50**. The frozen stack is:

- Wake model: `E37_TARGETED_COLOR_VOLUME_FIX`
- Command model: `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT`
- E50 weights SHA256: `BC8AC64CED4305DDF43BF4DE377F3CC636A764EFF339CD9F92AF06340C50B8FF`
- Threshold policy: `E40_NON_LED_COMMAND_GUARDRAIL_THRESHOLDS`, deployed as `configs/e50_revised_vocab_e40_thresholds.json`
- Final runtime: Pi microphone -> E37 wake gate -> E50 command CNN -> E40 confidence policy -> deterministic router -> local action -> local response audio -> return to listening

The final user-facing Pi path is a touchscreen GUI launched locally on the Raspberry Pi 5. The technical flow is: open **VCM Offline**, press **START LISTENING**, say `Hey Pi`, speak a command, observe the local action/response, repeat without restarting, then press **STOP VCM**.

Recovered E37 wake-recording evidence is documented separately in `E37_HEY_PI_DATASET_EVIDENCE_RECOVERY_AUDIT_20261002.md`. The Raspberry Pi manifest at `/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi/manifest.csv` contains 99 project-specific wake-stage recordings, including 50 `WAKE` / `hey pi` rows, 64 adaptation-designated rows, and 35 holdout-designated rows, recorded as 4-second 16 kHz audio using `plughw:2,0`. This strengthens E37 recording provenance but does not reconstruct the exact final E37 training subset or training hyperparameters.

## Hardware And Software Environment

- Raspberry Pi 5
- Local Pi microphone, configured as `plughw:2,0`
- Local Pi HDMI audio output, configured as `plughw:CARD=vc4hdmi0,DEV=0`
- Local touchscreen/desktop GUI
- Python virtual environment on the Pi
- Offline runtime after setup; no cloud ASR, no LLM, no remote Python service, and no laptop microphone/audio during verified standalone operation

## Architecture

```text
Pi microphone
  -> E37 wake classifier
  -> command capture
  -> log-Mel preprocessing
  -> E50 CNN, 19-label command vocabulary
  -> E40 threshold / rejection policy
  -> deterministic raw-command router
  -> local action stub or local action
  -> recorded response WAV playback
  -> return to listening
```

## Dataset And Provenance

The final E50 command-recognition model was developed using selected material from the collectively produced VCM class Gold Dataset, rather than using the entire Gold Dataset unchanged. The final training set also includes a separately identified project-specific Pi adaptation branch.

Dataset A (`VCM_MASTER`) is a project-local Dataset2 / collective-family representation derived from selected collective dataset material; it is not claimed to be the entire Gold Dataset. It provides the primary speaker-separated corpus:

- 36,622 audio samples
- 16 classes
- 27,130 training samples
- 4,734 validation samples
- 4,758 test samples
- 395 speaker/group identities
- no speaker leakage across the evaluation splits

Dataset B (`VCM_BALANCED`) is a training-derived subset of VCM_MASTER and therefore inherits its collective-family provenance. It provides an additional balanced training corpus:

- 15,268 training samples
- 13,801 original samples
- 1,467 augmented samples
- derived exclusively from Dataset A training data

Dataset B augmentation was generated from the Dataset A training partition using the controlled augmentation procedures documented in the project, so it did not introduce validation/test source leakage. The final E50 training manifest contains 16,100 rows: 13,070 active-project rows, 2,800 selected VCM_BALANCED rows, and 230 separately identified E41 Pi adaptation rows. The first two components are collective-derived/project-local command-data branches; the E41 rows are project-specific deployment adaptation data and are not classified as Gold Dataset rows.

This GitHub package contains the final deployable model and required deployment artifacts. It does not claim to contain all training audio. Dataset provenance describes the data used for model development, while the package contents describe the artifacts needed to inspect and deploy the frozen E50 system.

The E37 `Hey Pi` wake-recording lineage is separate from the collective/class Gold Dataset lineage used for the E50 command model. The 99 recovered E37 wake-stage recordings should not be described as Gold Dataset rows and are not part of the 16,100-row E50 command-model training manifest.

User-voice provenance was audited separately in `05_RESULTS/E50_FINAL_BENCHMARK_AND_METRICS_20260930.md`. The package makes a conservative claim: known Phase AF user-recorded targeted recovery clips are not identified in the final E50/BG training manifest, but older Pi adaptation/recovery audio is part of the final training lineage and its speaker identity is not established from filenames alone. User speech was also used in physical Pi validation of the frozen system. Therefore the final package treats user speech as confirmed live validation evidence and does not claim an absolute guarantee of zero historical user voice in every training-lineage artifact.

```text
Collective/class Gold Dataset lineage
  |
  +-- Selected active-project command data
  |     -> 13,070 final E50 rows
  |
  +-- Dataset A: VCM_MASTER
  |     36,622 samples
  |     27,130 train / 4,734 validation / 4,758 test
  |     16 classes, 395 speaker/groups
  |     |
  |     +-- Dataset B: VCM_BALANCED
  |           15,268 training samples
  |           13,801 original / 1,467 augmented
  |           derived only from Dataset A training data
  |           -> 2,800 selected final E50 rows
  |
  +-- Separate project-specific E41 Pi adaptation/calibration
        -> 230 final E50 rows

Final E50 Training Manifest
  13,070 active_project_dataset
   2,800 dataset2_vcm_balanced
     230 e41_reconstructed_adaptation
  -----
  16,100 total

Separate Held-Out / Independent Evaluation
```

## Deployment From This Repository

A compatible Raspberry Pi 5 deployment starts from the package contents, not from the original development directory: clone or download this repository, copy `02_FINAL_SYSTEM/vcm_pi_package/` to the Pi, install the documented system and Python dependencies, configure the compatible Pi microphone/audio devices, then launch the provided runtime wrapper.

The operational offline chain is local to the Pi: microphone -> local E37 wake inference -> local E50 command inference -> local E40 rejection policy -> local deterministic routing/action -> local WAV response playback -> return to listening. No Internet, cloud service, remote Python process, laptop microphone, or laptop speaker is required for operational E50 inference.
## 19-Command Vocabulary

The final E50 system preserves all 19 callable labels:

`PLAY_MUSIC`, `WEATHER`, `TIME`, `LIGHT_ON`, `LIGHT_OFF`, `LIGHT_DIM`, `BRIGHTNESS`, `TIMER`, `ALARM`, `TEMPERATURE`, `NEXT`, `PAUSE`, `STOP`, `VOLUME_UP`, `VOLUME_DOWN`, `CREATE_REMINDER`, `LIST_REMINDERS`, `CALL`, `MESSAGE`.

Important distinction:

- Callable: 19/19 remain implemented and callable.
- Benchmarked: 19/19 were included in the Item 16 live Pi5 final benchmark.
- End-to-end success in Item 16: 10/19 valid command trials.
- Demo-ready: a 13-command subset is recommended for live demonstration.

The 13-command demo subset is **not** a runtime whitelist. `TEMPERATURE` remains callable and benchmarked, but it is not final-demo-safe because earlier evidence recorded accepted-wrong behavior.

## Final Validation Summary

Section 68 status at this package point:

- Verified: Items 1-14, 16, 17, 18, 19.
- Partially verified: Item 15, because actual Pi5 performance measurements exist and a later timing-only disposable instrumentation run measured additional live pipeline timings, but GUI launch-to-ready and acoustic playback onset were still not directly measured.
- Current item: Item 20, GitHub package preparation.
- Still separate follow-up deliverables: Item 21 command sheet reconciliation and Item 22 final demo script reconciliation.

Key Section 68 validations include response WAV verification, Pi playback, E50/E37/E40 loading, all-19 command callability, router verification, persistent runtime, GUI validation, duplicate-runtime protection, network-off standalone operation, UNKNOWN/safety sweep, multiple commands without restart, non-primary-speaker validation, final benchmark, requirements traceability, logs, and final hashes.

## Final Benchmark Summary

Benchmarks were selected according to the actual E50 architecture and deployment objective. Conventional classification metrics are used for the CNN command classifier; slot metrics are not applicable because E50 is not a slot-filling parser; full-command evaluation is adapted to end-to-end action success; rejection metrics are adapted to E40's multi-class confidence gate; speaker/fresh-audio tests assess generalization; and embedded efficiency metrics assess computational cost. Efficiency is evaluated together with model quality, not independently from it.

Item 16 is the final E50 live Pi benchmark record:

- 20 physical Pi5 benchmark trials: 19 command labels plus 1 UNKNOWN/no-action trial.
- Wake success: 19/20 overall; 18/19 valid commands.
- Raw live command classification: 13/19 = 68.42%.
- Acceptance / coverage: 10/19 = 52.63%.
- Accepted-action precision: 10/10 = 100%.
- Accepted-wrong actions: 0.
- End-to-end action success: 10/19 = 52.63%.
- UNKNOWN/no-action safety: 1/1 = 100%.
- Return-to-listening: 20/20 = 100%.

Model-efficiency headline:

- E50 parameter count: 66,483.
- E50 weights file: 251,734 bytes.
- Calculated Conv2D/Dense MACs per 4-second input: 85,774,144.
- Raspberry Pi 5 CNN inference latency: mean 31.82 ms, P95 34.40 ms.
- Timing-only disposable run: command preprocessing mean 5.225 ms, command CNN inference mean 30.493 ms, command confidence check mean 0.041 ms, capture-to-action mean 4069.968 ms, wake-to-action mean 8149.864 ms.
- Model load time: 1.86 s.

Generalization and limitations headline:

- E50 current95-compatible controlled result: 83/90 = 92.22%.
- E50 Phase AV-compatible independent/fresh-audio result: 139/194 = 71.65%.
- The independent evaluation exposed a measurable generalization gap relative to controlled holdout.
- Training dynamics: the retained E50 training history shows validation deterioration after the selected epoch-7 checkpoint, consistent with classical overfitting during continued training. Epoch 7 had training loss `0.3458`, training accuracy `0.8801`, validation loss `1.3988`, and validation accuracy `0.6197`; epoch 11 had training loss `0.1946`, training accuracy `0.9322`, validation loss `2.1883`, and validation accuracy `0.6018`. The deployed checkpoint was selected at the best internal validation-loss point; later overfit checkpoints were not deployed.
- Non-primary-speaker validation was performed, with mixed recognition results.
- Production-GUI launch-to-ready timing, acoustic playback onset, noise/reverb robustness, and ECE were not systematically measured.

Detailed benchmark and metric definitions are in `05_RESULTS/E50_FINAL_BENCHMARK_AND_METRICS_20260930.md`.

These metrics must not be collapsed into one accuracy number. Raw classification, acceptance, accepted-action precision, safety, computational efficiency, and end-to-end action success measure different things.
## Known Limitations

- End-to-end command success in the final live benchmark was 10/19, not 19/19.
- Some callable commands are not final-demo-safe or not strongly verified enough for technical demonstration.
- `TEMPERATURE` is callable and passed in Item 16, but remains not demo-safe due historical accepted-wrong evidence.
- Training-dynamics limitation: E50's retained training history shows classical overfitting after the selected epoch-7 checkpoint. Epoch 7 was the best internal validation-loss point (`val_loss=1.3988`, `val_accuracy=0.6197`) and was selected for deployment; by epoch 11, validation loss had deteriorated to `2.1883`. Later overfit epochs were not deployed. This finding is documented alongside, but does not solely explain, the independent/live generalization gap.
- Model limitations and failure attribution: individual deployment failures are not attributed automatically to overfitting. Independent/live performance is also affected by data coverage, class confusion, speaker/acoustic/domain variation, and the confidence-based rejection policy. A correct but below-threshold prediction is a safe rejection; a high-confidence wrong label is classifier confusion; a correct accepted label with a downstream problem is a router/action/output issue only where directly evidenced.
- Item 15 performance is partially verified: E50 load time, saved-WAV inference latency, resource behavior, and a repeated runtime sequence were measured. A later timing-only disposable instrumentation run measured additional wake, preprocessing, CNN, confidence-check, router/action, response-invocation, capture-to-action, and wake-to-action timings without modifying the production runtime. GUI launch-to-ready and acoustic playback onset remain unmeasured.
- Non-primary-speaker validation demonstrated real operation, but with mixed command correctness; the softer non-primary voice and operator timing/instruction issues were preserved in evidence.

## Engineering History Overview

The engineering path progressed from requirements and dataset construction through baseline CNN experiments, Pi/deployment mismatch diagnosis, controlled recovery/adaptation attempts, E46/E47/E48/E49 analysis, revised vocabulary selection, E50 freeze, runtime/GUI integration, safety validation, offline validation, duplicate-runtime validation, non-primary-speaker validation, performance measurement, final benchmark recording, and final artifact integrity verification.

Intermediate experiments are summarized in `03_ENGINEERING_HISTORY/ENGINEERING_HISTORY_SUMMARY.md`; raw logs are included for auditability.

## Reproduction And Inspection Path

Start here:

1. `02_FINAL_SYSTEM/vcm_pi_package/README_PI_DEPLOYMENT.md` for Pi deployment context.
2. `06_REPRODUCTION/INSTALL.md` for dependency setup.
3. `06_REPRODUCTION/RUN.md` for the final local GUI/runtime path.
4. `06_REPRODUCTION/COMMAND_REFERENCE.md` for command distinctions.
5. `04_VALIDATION/FINAL_BENCHMARK.md` for final benchmark results.
6. `07_INTEGRITY/E50_ITEM19_FINAL_HASH_REPORT_20260930.md` for final hashes.

## Evidence And Integrity

The package includes final validation summaries plus selected evidence archives under `04_VALIDATION/evidence/`. The integrity record is:

- `07_INTEGRITY/E50_FINAL_SHA256_MANIFEST_20260930.csv`
- CSV SHA256: `D3E20250541CA3F58027F885215EB784727ABBC601C23425A6090FD6A9A0F4F0`
- `07_INTEGRITY/E50_FINAL_SHA256_MANIFEST_20260930.txt`
- TXT SHA256: `F29FB2B2BB75FEC683367F2406173DFCE2526B47D45B0AA9C0CADEE6CB8B1482`

Item 19 verified 224 manifest rows, 224 existing/verified artifacts, zero missing artifacts, zero hash mismatches, and 19,275,672 bytes.

## Independent E53 Experiment

`09_INDEPENDENT_EXPERIMENT/E53_INDEPENDENT_EXPERIMENT.md` documents E53 as a separate experimental track. E53 is not part of the final E50 implementation, final E50 benchmark, or Section 68 completion evidence. No E53 implementation, model, dataset, configuration, or result is used to satisfy E50 requirements.


