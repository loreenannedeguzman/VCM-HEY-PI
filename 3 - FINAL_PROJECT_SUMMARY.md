# E50 Voice Command Module

## 1. Project Identity

E50 is a fixed-vocabulary, wake-gated, offline voice-command module for Raspberry Pi 5. It is not a cloud assistant, LLM, arbitrary speech-to-text system, online ASR service, or unrestricted natural-language interface. The system listens locally for the wake phrase `Hey Pi`, classifies the following command audio into one of 19 fixed E50 labels, applies a confidence guardrail before action execution, routes accepted labels to deterministic local actions, plays local WAV responses, and returns to listening.

| Item | Value / source |
|---|---|
| Project title | ME2 VCM - Final E50 Raspberry Pi Voice Command System. Source: `FINAL GITHUB README ORIGINAL.md`, project title/overview. |
| Course / machine exercise | Machine Exercise 2 Voice Command Model (VCM). Source: `FINAL GITHUB README ORIGINAL.md`, project overview. |
| Final experiment ID | `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT`. Source: `results/phase_bg_e50_bg_revised_vocab_original_preserve_e41_init_20260928/PHASE_BG_TRAINING_CONFIG.json`, key `experiment_id`. |
| Target hardware | Raspberry Pi 5. Source: `4b - DEPLOYMENT/vcm_pi_package/README_PI_DEPLOYMENT.md`, package title and Pi setup sections. |
| System type | Offline Raspberry Pi 5 voice-command system for fixed command labels and local actions. Source: deployment README final model and command routing sections. |
| Project status | Ready with documented limitations. Source: `VCM_PROJECT_STATUS.md` / package status evidence and final E50 report evidence. |
| Closure / final audit date | 2026-09-30 final package/evidence audit and Item 16 benchmark evidence. Source: `pi_validation/e50_bn_close_item16_final_benchmark_20260930_105703/ITEM16_AGGREGATE_METRICS.json`; package review/status artifacts. |

One-sentence system description: E50 is a local Raspberry Pi 5 VCM that uses E37 wake detection, E50 command CNN inference, E40 confidence/rejection, deterministic routing, local action execution, recorded response audio, and persistent return-to-listening behavior.

## 2. What Was Built

The deployable system is the frozen E50 VCM stack:

```text
Raspberry Pi microphone
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

The deployment package is in `4b - DEPLOYMENT/vcm_pi_package/`. It contains runtime scripts, E37 and E50 model artifacts, E40 threshold configuration, preprocessing/action/router code, GUI launcher, and local response WAV assets. The GUI is an operator interface and launcher around the frozen VCM core; it does not replace E37, E50, E40, the router, or the response assets.

Recognition, thresholding, routing, and action execution are runtime responsibilities. The GUI is the interface/launcher/display.

## 3. Frozen Technical Identity

| Component | Final value / evidence |
|---|---|
| Final command model | `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT` |
| Wake model | `E37_TARGETED_COLOR_VOLUME_FIX` |
| Confidence policy | `E40_NON_LED_COMMAND_GUARDRAIL_THRESHOLDS`, deployed as `configs/e50_revised_vocab_e40_thresholds.json` |
| Final vocabulary | 19 labels; `LIGHT_DIM` is included, final `COLOR` is not |
| Input audio | 16 kHz, 4.0 s command window |
| Feature representation | log-Mel spectrogram / matrix, 398 x 40, model input `(398, 40, 1)` |
| E50 parameters | 66,483 |
| E50 weights | 251,734 bytes |
| E50 normalization | 730 bytes |
| E50 weights + normalization | 252,464 bytes |
| E50 MACs | 85,774,144 Conv2D/Dense MACs per 4-second input |
| E50 weights SHA-256 | `BC8AC64CED4305DDF43BF4DE377F3CC636A764EFF339CD9F92AF06340C50B8FF` |
| E37 weights SHA-256 | `687E82E2CEFA6D74CEF2C0A15D28F8F6142D47D4A67E57C68C091E83FC2CEBDE` |
| E40 config SHA-256 | `A0B2495328FD5A1E0E5885E727623BA6D9F823BE94CCCDFD0AEAD77254BBB3FD` |
| Wake threshold | 0.90 |
| Command default threshold | 0.90 |

Model/evidence sources include `PHASE_BG_TRAINING_CONFIG.json`, `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT_model_summary.txt`, final SHA manifest entries, deployment README final model sections, and Item 16 frozen-stack evidence.

The final vocabulary labels are: `PLAY_MUSIC`, `WEATHER`, `TIME`, `LIGHT_ON`, `LIGHT_OFF`, `LIGHT_DIM`, `BRIGHTNESS`, `TIMER`, `ALARM`, `TEMPERATURE`, `NEXT`, `PAUSE`, `STOP`, `VOLUME_UP`, `VOLUME_DOWN`, `CREATE_REMINDER`, `LIST_REMINDERS`, `CALL`, `MESSAGE`.

## 4. E37 Wake-Gate Provenance

Recovered E37 provenance note: the project-specific Raspberry Pi `Hey Pi` wake-recording evidence has been recovered and documented in `E37_HEY_PI_DATASET_EVIDENCE_RECOVERY_AUDIT_20261002.md`. The recovered manifest at `/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi/manifest.csv` documents 99 wake-stage recordings, including 50 `WAKE` / `hey pi` rows, 64 adaptation-designated rows, and 35 holdout-designated rows, all recorded as 4-second 16 kHz audio using `plughw:2,0`.

The 99 recovered E37 `Hey Pi` wake recordings are a separate Raspberry Pi wake-stage lineage. They support E37 wake-gate provenance and establish the recording-set evidence, but they are not part of the 16,100-row E50 command-model training manifest and do not establish the exact final E37 training-row membership or full E37 training configuration.

## 5. Dataset And Training

The final E50 command model used a manifest-driven training set rather than an uncontrolled folder crawl. E50 was developed using selected material from the class collective Gold Dataset rather than using the entire collective dataset unchanged. The first two final training components are collective-derived/project-local command-data branches; the E41 rows are project-specific Pi deployment adaptation/calibration data and are not classified as Gold Dataset rows. The recovered E37 `Hey Pi` wake recordings are a separate project-specific Raspberry Pi wake-stage lineage; they are not Gold Dataset rows and are not part of the 16,100-row E50 command-model training manifest.

| Item | Value | Evidence / note |
|---|---:|---|
| Dataset A | `VCM_MASTER` | Final dataset documentation. |
| Dataset A samples | 36,622 | `data/VCM Dataset2/VCM/VCM_MASTER/reports/FINAL_DATASET_DOCUMENTATION_A_B.txt`, executive summary and Dataset A size. |
| Dataset A classes | 16 | Same documentation, Dataset A class inventory. |
| Dataset A train / validation / test | 27,130 / 4,734 / 4,758 | Same documentation, executive summary and Dataset A size. |
| Dataset A speaker/group identities | 395 | Same documentation, speaker independence section. |
| Dataset A speaker leakage | 0 train/val/test overlap | Same documentation, speaker independence section. |
| Dataset B | `VCM_BALANCED` | Same documentation, Dataset B section. |
| Dataset B training samples | 15,268 | Same documentation, Dataset B final size. |
| Dataset B original / augmented | 13,801 / 1,467 | Same documentation, Dataset B final size and augmentation sections. |
| Final E50/BG training manifest | 16,100 rows | E50 project status / requirements traceability and Phase BG training manifest evidence. |
| Active-project / Dataset2 / E41 adaptation rows | 13,070 / 2,800 / 230 | E50 project status / requirements traceability and Phase BG training manifest evidence. |
| Best epoch | 7 | `results/phase_bg_e50_bg_revised_vocab_original_preserve_e41_init_20260928/PHASE_BG_TRAINING_RESULTS.json`, `best_epoch`. |
| Internal validation loss | 1.3987702131271362 | Same JSON, `best_internal_validation_loss`. |
| Internal validation accuracy | 0.6197039305768249 | Same JSON, epoch 7 `val_accuracy`. |

Dataset source/licensing evidence is qualified, not blanket redistribution permission. The dataset source report documents Fluent Speech Commands, SLURP, Timers and Such, Multi-Sensor Voice Command DOI `10.48804/IEKKVZ` with CC-BY-4.0 and GDPR derivative download-tracking obligation, SET_TEMPERATURE project recordings/Piper TTS, and Google Speech Commands background-noise use. The correct public wording is to cite/follow upstream source terms and not to claim unrestricted redistribution unless separately established.

Training and internal validation values are not final Raspberry Pi performance metrics.

## 6. Raspberry Pi 5 Validation And Final Benchmark

Final physical benchmark population: 20 Pi 5 trials = 19 valid command-label trials plus 1 UNKNOWN/no-action trial.

| Metric | Result | Meaning / boundary | Source |
|---|---:|---|---|
| Wake success, overall | 19/20 = 95.0% | Wake-stage success across all benchmark trials; not command-recognition accuracy. | `ITEM16_AGGREGATE_METRICS.json`, wake success fields. |
| Wake success, valid commands | 18/19 = 94.74% | Wake-stage success on valid command trials. | Item 16 aggregate metrics. |
| Raw command classification | 13/19 = 68.42% | Correct raw command classification among 19 valid command trials; not overall system accuracy. | Item 16 aggregate metrics. |
| E40 acceptance / end-to-end action success | 10/19 = 52.63% | Correct raw label, accepted by threshold policy, correct local action, response playback true, and return to listening. | Item 16 aggregate metrics and benchmark definition. |
| Accepted-correct | 10 | Accepted valid commands that executed the correct action. | Item 16 aggregate metrics. |
| Accepted-wrong | 0 | Accepted valid commands that executed a wrong action. | Item 16 aggregate metrics. |
| Accepted-action precision | 10/10 = 100% | Of accepted/executed valid commands, every accepted command produced the correct corresponding action; not overall accuracy. | Item 16 aggregate metrics. |
| Safe rejection | 10/10 = 100% | Among non-executed final benchmark trials, all were safely rejected without routed action. | Item 16 aggregate metrics. |
| UNKNOWN safety | 1/1 = 100% | UNKNOWN/no-action trial produced no unintended action. | Item 16 aggregate metrics. |
| Return to listening | 20/20 = 100% | Runtime returned to listening after every benchmark trial. | Item 16 aggregate metrics. |
| Bounded command-window false-accept rate | 0/4 = 0.0%, qualified | False accepts / valid out-of-scope command-window safety prompts; not broad environmental FAR. | Item 12 safety sweep result summary and result JSONs. |

Metrics use their documented denominators and definitions; they should not be collapsed into a single overall accuracy. The engineering conclusion is not that the command classifier is near-perfect. Raw command classification was moderate at 13/19, and end-to-end action success was 10/19. The stronger result is that accepted commands were action-correct in the tested population: there were zero accepted-wrong actions, safe rejection worked for all non-executed cases, UNKNOWN safety was preserved, and the runtime returned to listening after every trial.

## 7. Efficiency, Latency, RTF, And Pi Specifications

| Metric | Value | Meaning / source |
|---|---:|---|
| Parameters | 66,483 | Final E50 command CNN parameters; `PHASE_BG_TRAINING_CONFIG.json`, `parameter_count`; model summary. |
| Weights | 251,734 bytes | Final E50 weights artifact size; final SHA manifest entry. |
| Weights + normalization | 252,464 bytes | Weights plus 730-byte normalization artifact; final SHA manifest entries. |
| MACs | 85,774,144 per 4-second input | Conv2D/Dense MAC estimate for command CNN; final benchmark/metrics documentation. |
| Model load | 1.8566017879998071 s | E50 model load time during Item 15 saved-WAV inference benchmark; `outputs/e50_bn_close_item15_performance_20260930_102647_evidence.tar.gz`, `inference_benchmark/item15_e50_pi_inference_summary.json`. |
| CNN inference mean | 31.82 ms | Pi 5 saved-command-WAV CNN inference only; Item 15 summary JSON, `latency.mean_ms`. |
| CNN inference median/P50 | 31.39 ms | Pi 5 saved-command-WAV CNN inference only; same summary JSON, `latency.median_ms`. |
| CNN inference P95 | 34.40 ms | Pi 5 saved-command-WAV CNN inference only; same summary JSON, `latency.p95_ms`. |
| CNN inference max | 38.31 ms | Pi 5 saved-command-WAV CNN inference only; same summary JSON, `latency.max_ms`. |
| CNN-only RTF mean | 0.0080 | 31.822338 ms / 4,000 ms command input; derived from Item 15 CNN latency and 4.0 s input duration. |
| CNN-only RTF P95 | 0.0086 | 34.402333 ms / 4,000 ms command input; derived from Item 15 CNN latency and 4.0 s input duration. |
| Qualified command-pipeline RTF mean / P95 | 0.016543 / 0.018500 | Qualified command-pipeline RTF from response playback-start audit; `~/e50_demoday_final_audit/E50_RESPONSE_LATENCY_MEASUREMENTS_V2.csv`. |
| Response playback-start latency | mean 66.172 ms; P50 64.837 ms; P95 73.999 ms; P99 73.999 ms; max 73.999 ms over 5 accepted/executed trials | Boundary: command WAV capture completion -> first observed local `aplay` response WAV process. External passive audit files `~/e50_demoday_final_audit/E50_RESPONSE_LATENCY_MEASUREMENTS_V2.csv` and `E50_RESPONSE_LATENCY_EVENTS_V2.csv`; frozen runtime not modified. |
| Pi specifications | Raspberry Pi 5 Model B Rev 1.1; ARM Cortex-A76; 4 cores; aarch64; Linux 6.18.50+rpt-rpi-2712; Python 3.13.5; 7.9 GiB RAM; CPU max 2400 MHz; CPU min 1500 MHz; `arm_freq=2400`; `arm_boost=1`; `throttled=0x0`; mic `plughw:2,0`; audio output `plughw:CARD=vc4hdmi0,DEV=0` | Item 15 prep and inference summary; read-only Pi spec audit `~/e50_demoday_final_audit/E50_PI_SPECS_READONLY_FINAL.txt`. |

Important: CNN latency and CNN-only RTF values are CNN inference only. They are not end-to-end latency, GUI latency, microphone-to-action latency, wake-to-action latency, or acoustic response-onset latency.

## 8. Comparable-Size Baseline

| Model | Parameters | Weight size | Initialization | Offline comparison evidence | Status |
|---|---:|---:|---|---|---|
| E51 comparable baseline | 66,483 | 251,009 bytes | Fresh initialization | current95-compatible 77/90 = 85.56%; phase_av-compatible 131/194 = 67.53%; combined revised test 2727/4230 = 64.47%; phase_av accepted precision 89.61% | Qualified offline same-architecture baseline |
| Final E50 | 66,483 | 251,734 bytes | Mapped E41 initialization | current95-compatible 83/90 = 92.22%; phase_av-compatible 139/194 = 71.65%; combined revised test 2724/4230 = 64.40%; phase_av accepted precision 91.92%; final Pi E2E 10/19 = 52.63% | Final selected system |

Sources: `results/phase_bg_e51_bg_revised_vocab_original_preserve_fresh_init_20260928/PHASE_BG_E51_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_FRESH_INIT_CNN_CANDIDATE_20260928.md`; `results/phase_bg_e50_bg_revised_vocab_original_preserve_e41_init_20260928/PHASE_BG_E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT_CNN_CANDIDATE_20260928.md`; corresponding training config and model artifacts.

This comparison is qualified because E51 was not rerun as a second final physical Pi benchmark. It is a comparable-size offline baseline, not a second deployed runtime result.

## 9. Offline Deployment And Demo Flow

Established deployment facts:

- Raspberry Pi 5 deployment.
- Local microphone input.
- Local model inference.
- Local threshold policy.
- Deterministic local routing.
- Local action execution.
- Local response audio.
- Touchscreen GUI.
- Persistent listening / return-to-listening.
- Offline operation after setup.
- No cloud/remote inference, online ASR, or LLM is used during verified operation.

Source: deployment README final model, command routing, wake-gated demo, and touchscreen GUI sections; Item 11 offline-operation verification.

Operator demo flow:

```text
Open VCM Offline
-> START LISTENING
-> say "Hey Pi"
-> wait for wake acceptance
-> speak command
-> observe local action/response
-> system returns to listening
-> repeat without restart
-> STOP VCM
```

On the Raspberry Pi deployment target, use the packaged runtime directory:

```bash
cd "4b - DEPLOYMENT/vcm_pi_package"
bash scripts/run_vcm_touchscreen_gui.sh
```

The core runtime path uses `scripts/pi_wake_voice_control_demo.py`, E37 wake detection, E50 command inference, E40 thresholds, deterministic routing, and local response WAV playback. See `4a - DEPLOYMENT_QUICKSTART.md` and `4b - DEPLOYMENT/vcm_pi_package/README_PI_DEPLOYMENT.md` for current operational details. Detailed reproduction notes are in `1 - DETAILED REPORTS/06_REPRODUCTION/01_DEPLOYMENT_PROCEDURE.md`.

## 10. Submission And Reproducibility

- Repository package: `GITHUB_PACKAGE_FINAL_20261002`.
- Historical package label preserved in source notes: `ME2_VCM_E50_GITHUB_PACKAGE_20260930`.
- Package status: ready with documented limitations.
- Deployment package: `4b - DEPLOYMENT/vcm_pi_package` with model artifacts, configs, runtime scripts, actions, responses, requirements, README, and launcher.
- Dependency file: `4b - DEPLOYMENT/vcm_pi_package/requirements_pi.txt` lists `numpy`, `scipy`, `tensorflow`.
- Documented setup: Raspberry Pi OS setup, system packages, Python virtual environment, package copy, import checks, microphone checks, wake-gated runtime command, and touchscreen GUI command.
- Reproduction wording: the repository provides packaged deployment artifacts and launch commands. Reproduction requires the documented Raspberry Pi OS, Python/environment, dependency, audio-device, and hardware prerequisites. It should not be described as one-command reproduction on arbitrary computers.

Example GUI launch from deployment README:

```bash
cd ~/vcm_pi_package
source .venv/bin/activate
export DEV=plughw:2,0
export RESPONSE_AUDIO_DEVICE=plughw:CARD=vc4hdmi0,DEV=0
bash scripts/run_vcm_touchscreen_gui.sh
```

## 11. Reviewer Checklist

| Reviewer item | Status | Evidence / qualification |
|---|---|---|
| Model | Established | E50 command CNN, E37 wake model, E40 policy identified. |
| Dataset | Established with qualified licensing/citation | Dataset A/B documented; cite/follow upstream source terms; do not claim unrestricted redistribution. |
| Training | Established | E50 training config, training results, final checkpoint and internal validation evidence exist. |
| Raspberry Pi validation | Established | Item 16 final physical Pi benchmark, 20 trials. |
| Keyword/wake metric | Established | Wake success 19/20 = 95.0%. |
| Command classification | Established | Raw command classification 13/19 = 68.42%. |
| End-to-end action success | Established | 10/19 = 52.63%. |
| Accepted-action precision | Established | 10/10 = 100%; not overall accuracy. |
| False-accept rate | Qualified established | Bounded command-window FAR 0/4 = 0.0%; broad environmental FAR not established. |
| Latency P95 | Established | CNN inference P95 34.40 ms; CNN-only. |
| RTF | Qualified established | CNN-only mean RTF 0.0080; P95 RTF 0.0086; qualified command-pipeline mean RTF 0.016543 and P95 RTF 0.018500. |
| Runtime | Established | Offline-after-setup local Pi runtime with deterministic routing and response audio. |
| GitHub package | Established | `GITHUB_PACKAGE_FINAL_20261002`; historical package label `ME2_VCM_E50_GITHUB_PACKAGE_20260930` appears in source notes. |
| Dataset citation/license | Qualified | Source/license report identifies upstream sources and terms; blanket redistribution not established. |
| Training logs + final checkpoint | Established | Training results/config/checkpoint evidence present. |
| Pi latency reproducibility | Qualified | Existing Item 15 saved-WAV inference benchmark documents CNN method; external passive V2 audit documents Pi local response playback-start latency without modifying frozen runtime. |
| Held-out unseen speakers | Qualified | Dataset speaker-independent splits established; formal statistical speaker-independent Pi benchmark not established. |
| Comparable-size baseline | Qualified established | E51 fresh-init same-parameter offline baseline exists; no second Pi benchmark for E51. |

## 12. Demo-Ready Facts

- Final runtime vocabulary: 19 labels.
- All 19 final command labels are callable.
- The final physical benchmark contains 19 valid command-label trials, one per label, plus 1 UNKNOWN/no-action trial.
- A 13-command demo-ready subset was identified for demonstration; it is not a runtime whitelist.
- Runtime chain: E37 wake -> E50 command CNN -> E40 policy -> deterministic router -> local action -> local response -> return to listening.
- Final Pi benchmark highlights: raw command classification 13/19 = 68.42%; end-to-end action success 10/19 = 52.63%; accepted-action precision 10/10 = 100%; safe rejection 10/10 = 100%; wake success 19/20 = 95.0%; return to listening 20/20 = 100%; UNKNOWN safety 1/1 = 100%; bounded command-window false-accept rate 0/4 = 0.0%, qualified; CNN inference P95 34.40 ms, CNN-only; CNN-only P95 RTF 0.0086; response playback-start latency mean 66.172 ms and P95 73.999 ms, qualified; qualified command-pipeline P95 RTF 0.018500.

## 13. Main Limitations And Items Not Established

Do not fill these with estimates:

- Author/team information: not established in project evidence.
- A100-based final E50 training: not applicable. The final E50 command model was trained locally on the project laptop; the reviewed Phase BG/E50 records support local Windows CPU-only TensorFlow training, not A100 or external-cluster training.
- GUI launch-to-ready latency: not measured as a core VCM benchmark metric. The GUI is documented as a post-freeze presentation/control layer, but no formal launch-to-ready timing benchmark was established.
- Acoustic speaker-onset latency: not measured. Pi local response playback-start latency is measured only as qualified external evidence: mean 66.172 ms, P50 64.837 ms, P95/P99/max 73.999 ms over 5 accepted/executed trials.
- Full end-to-end wake-to-action latency: not measured.
- Full wake-to-response or acoustic end-to-end RTF: not established. Qualified command-pipeline RTF to response playback start is established: mean 0.016543, P95 0.018500.
- Broad environmental false-accept rate over arbitrary background/no-wake audio: not established.
- Final ECE/calibration metric: not measured.
- Formal noise/reverberation robustness benchmark: not measured.
- Formal phrasing-variation benchmark: not measured.
- Formal statistical speaker-independent final Pi benchmark: not measured.
- Per-intent physical-Pi metrics are limited because the final benchmark used one trial per valid label.
- Unrestricted dataset redistribution rights: not established as a blanket claim.
- Exact final E37 training-row membership is not established by the recovered wake-recording evidence.

Post-closure GUI passive telemetry is documented as an operator-facing observability enhancement, not as evaluation evidence. It improves runtime display/status visibility around wake, command, routing, action, response, and return-to-listening behavior, but it is not a benchmark, validation result, latency measurement, accuracy metric, or evidence of improved E50 model performance.

## 14. First Reading Path

| If you want to inspect... | Read |
|---|---|
| Overall architecture | `1 - DETAILED REPORTS/02_FINAL_SYSTEM/01_SYSTEM_ARCHITECTURE.md` |
| Wake gate | `1 - DETAILED REPORTS/02_FINAL_SYSTEM/02_WAKE_GATE_E37.md` |
| Final command model | `1 - DETAILED REPORTS/02_FINAL_SYSTEM/03_COMMAND_MODEL_E50.md` |
| Confidence/rejection policy | `1 - DETAILED REPORTS/02_FINAL_SYSTEM/04_CONFIDENCE_POLICY_E40.md` |
| Vocabulary/actions | `1 - DETAILED REPORTS/02_FINAL_SYSTEM/05_FINAL_VOCABULARY_AND_ACTIONS.md` |
| Dataset/training | `1 - DETAILED REPORTS/02_FINAL_SYSTEM/06_DATASET_AND_TRAINING.md` |
| Pi deployment | `1 - DETAILED REPORTS/02_FINAL_SYSTEM/07_PI_DEPLOYMENT.md` |
| Final benchmark numbers | `1 - DETAILED REPORTS/05_RESULTS/01_FINAL_BENCHMARK_RESULTS.md` |
| Latency/RTF/FAR | `1 - DETAILED REPORTS/05_RESULTS/02_LATENCY_RTF_AND_FAR.md` |
| Engineering history | `1 - DETAILED REPORTS/03_ENGINEERING_HISTORY/01_DEVELOPMENT_TIMELINE.md` |
| Reproduction/deployment | `1 - DETAILED REPORTS/06_REPRODUCTION/01_DEPLOYMENT_PROCEDURE.md` |
| Integrity/hashes | `1 - DETAILED REPORTS/07_INTEGRITY/01_FROZEN_ARTIFACT_IDENTITY.md` |
| Independent E53 experiment | `5 - INDEPENDENT EXPERIMENT - E53/02_E53_E50_SEPARATION.md` |

## 15. E53 Boundary

E53/VCM2 is retained only as an independent experiment. It is not the deployed E50 VCM, not the final E50 command model, not part of the E50 benchmark, and not part of the final Raspberry Pi action pipeline.

## 16. Revision Integrity Confirmation

- New experiments performed for this documentation revision: none.
- Existing benchmark values preserved: yes.
- Model weights changed: no.
- E37 changed: no.
- E40 changed: no.
- Thresholds changed: no.
- Dataset changed: no.
- Training manifest changed: no.
- Router/actions changed: no.
- Response audio changed: no.
- Runtime changed: no.
- GUI changed: no.
- E53 accessed for this edit: no.
- VCM executed for this edit: no.
- Training executed for this edit: no.
- Benchmark executed for this edit: no.
- Documentation files updated by this packaging repair: `README.md`, `4a - DEPLOYMENT_QUICKSTART.md`, and current deployment documentation under `4b - DEPLOYMENT/vcm_pi_package/`.


