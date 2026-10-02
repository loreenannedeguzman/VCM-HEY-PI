# E50 Demo Day Report

## 1. Project Identity

- **Project title:** ME2 VCM - Final E50 Raspberry Pi Voice Command System  
  Source: `FINAL GITHUB README ORIGINAL.md`, project title/overview.
- **Course / Machine Exercise:** Machine Exercise 2 Voice Command Model (VCM).  
  Source: `FINAL GITHUB README ORIGINAL.md`, project overview.
- **Final experiment ID:** `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT`.  
  Source: `results/phase_bg_e50_bg_revised_vocab_original_preserve_e41_init_20260928/PHASE_BG_TRAINING_CONFIG.json`, key `experiment_id`.
- **Target hardware:** Raspberry Pi 5.  
  Source: `deployment/vcm_pi_package/README_PI_DEPLOYMENT.md`, package title and Pi setup sections.
- **System type:** Offline Raspberry Pi 5 voice-command system for fixed command labels and local actions.  
  Source: `deployment/vcm_pi_package/README_PI_DEPLOYMENT.md`, final model and command routing sections.
- **Project status:** Ready with documented limitations.  
  Source: `VCM_PROJECT_STATUS.md` / package status evidence and final E50 report evidence.
- **Closure / final audit date:** 2026-09-30 final package/evidence audit and Item 16 benchmark evidence.  
  Source: `pi_validation/e50_bn_close_item16_final_benchmark_20260930_105703/ITEM16_AGGREGATE_METRICS.json`; package review/status artifacts.

**One-sentence system description:** E50 is a local Raspberry Pi 5 VCM that uses E37 wake detection, E50 command CNN inference, E40 confidence/rejection, deterministic routing, local action execution, recorded response audio, and persistent return-to-listening behavior.

## 2. System Architecture

```text
Pi microphone
-> E37 wake detection
-> command capture
-> log-Mel preprocessing
-> E50 command CNN
-> E40 confidence/rejection policy
-> deterministic command router
-> local action
-> local response audio
-> return to listening
```

- **Wake model:** `E37_TARGETED_COLOR_VOLUME_FIX`
- **Command model:** `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT`
- **Command policy:** `E40_NON_LED_COMMAND_GUARDRAIL_THRESHOLDS`, deployed as `configs/e50_revised_vocab_e40_thresholds.json`

This is not an LLM, cloud ASR, online speech-recognition service, or arbitrary transcription system. It is a fixed-vocabulary local command classifier with deterministic local action routing.

Recovered E37 provenance note: the project-specific Raspberry Pi `Hey Pi` wake-recording evidence has been recovered and documented in `E37_HEY_PI_DATASET_EVIDENCE_RECOVERY_AUDIT_20261002.md`. The recovered manifest at `/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi/manifest.csv` documents 99 wake-stage recordings, including 50 `WAKE` / `hey pi` rows, 64 adaptation-designated rows, and 35 holdout-designated rows, all recorded as 4-second 16 kHz audio using `plughw:2,0`. This establishes the recording-set provenance, but not the exact final E37 training-row membership or full E37 training configuration.

Sources: `deployment/vcm_pi_package/README_PI_DEPLOYMENT.md`, final model, command routing, wake-gated demo, and touchscreen GUI sections; `pi_validation/e50_bn_close_item16_final_benchmark_20260930_105703/ITEM16_AGGREGATE_METRICS.json` identity fields.

## 3. Model

| Item | Final E50 value | Definition / evidence |
|---|---:|---|
| Model type | tiny VCM CNN command classifier | `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT_model_summary.txt`, model summary. |
| Final runtime vocabulary | 19 labels | `PHASE_BG_TRAINING_CONFIG.json`, key `labels`; deployment README final model section. |
| Sampling rate | 16,000 Hz | `PHASE_BG_TRAINING_CONFIG.json`, `preprocessing.sample_rate_hz`. |
| Input duration | 4.0 seconds | `PHASE_BG_TRAINING_CONFIG.json`, `preprocessing.target_duration_sec`. |
| Feature representation | log-Mel spectrogram | `PHASE_BG_TRAINING_CONFIG.json`, preprocessing keys; deployment README final model section. |
| Feature shape | 398 x 40; model input `(398, 40, 1)` | `PHASE_BG_TRAINING_CONFIG.json`, `expected_frames`, `mel_bins`, `feature_shape`; model summary input layer. |
| Parameter count | 66,483 | `PHASE_BG_TRAINING_CONFIG.json`, key `parameter_count`; model summary total params. |
| E50 weights | 251,734 bytes | `E50_FINAL_SHA256_MANIFEST_20260930.csv` / final SHA manifest entry for E50 weights. |
| E50 weights + normalization | 252,464 bytes | Derived from 251,734-byte weights + 730-byte normalization; final SHA manifest entries. |
| MACs | 85,774,144 Conv2D/Dense MACs per 4-second input | Final benchmark/metrics documentation MAC accounting. |
| Wake model | `E37_TARGETED_COLOR_VOLUME_FIX` | Deployment README final model section; Item 16 frozen stack. |
| Command model | `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT` | Training config; Item 16 aggregate metrics. |
| Threshold policy | `E40_NON_LED_COMMAND_GUARDRAIL_THRESHOLDS` | Deployment README; deployed config `configs/e50_revised_vocab_e40_thresholds.json`. |

The final vocabulary labels are: `PLAY_MUSIC`, `WEATHER`, `TIME`, `LIGHT_ON`, `LIGHT_OFF`, `LIGHT_DIM`, `BRIGHTNESS`, `TIMER`, `ALARM`, `TEMPERATURE`, `NEXT`, `PAUSE`, `STOP`, `VOLUME_UP`, `VOLUME_DOWN`, `CREATE_REMINDER`, `LIST_REMINDERS`, `CALL`, `MESSAGE`.

## 4. Efficiency

| Metric | Value | Meaning | Source |
|---|---:|---|---|
| Parameters | 66,483 | Final E50 command CNN parameters | `PHASE_BG_TRAINING_CONFIG.json`, `parameter_count`; model summary. |
| Weights | 251,734 bytes | Final E50 weights artifact size | Final SHA manifest entry for E50 weights. |
| Weights + normalization | 252,464 bytes | Weights plus 730-byte normalization artifact | Final SHA manifest entries. |
| MACs | 85,774,144 per 4-second input | Conv2D/Dense MAC estimate for command CNN | Final benchmark/metrics documentation. |
| Model load | 1.8566017879998071 s | E50 model load time during Item 15 saved-WAV inference benchmark | `outputs/e50_bn_close_item15_performance_20260930_102647_evidence.tar.gz`, `inference_benchmark/item15_e50_pi_inference_summary.json`. |
| CNN inference mean | 31.82 ms | Pi 5 saved-command-WAV CNN inference only | same summary JSON, `latency.mean_ms`. |
| CNN inference median/P50 | 31.39 ms | Pi 5 saved-command-WAV CNN inference only | same summary JSON, `latency.median_ms`. |
| CNN inference P95 | 34.40 ms | Pi 5 saved-command-WAV CNN inference only | same summary JSON, `latency.p95_ms`. |
| CNN inference max | 38.31 ms | Pi 5 saved-command-WAV CNN inference only | same summary JSON, `latency.max_ms`. |
| CNN-only RTF mean | 0.0080 | 31.822338 ms / 4,000 ms command input | Derived from Item 15 summary JSON and 4.0 s input duration in training config. |
| CNN-only RTF P95 | 0.0086 | 34.402333 ms / 4,000 ms command input | Derived from Item 15 summary JSON and 4.0 s input duration in training config. |

Important: latency and RTF values above are **CNN inference only**. They are not end-to-end latency, GUI latency, microphone-to-action latency, wake-to-action latency, or acoustic response-onset latency.

## 5. Dataset / Training

| Item | Value | Evidence |
|---|---:|---|
| Dataset A | `VCM_MASTER` | Final dataset documentation. |
| Dataset A samples | 36,622 | `data/VCM Dataset2/VCM/VCM_MASTER/reports/FINAL_DATASET_DOCUMENTATION_A_B.txt`, executive summary and Dataset A size. |
| Dataset A classes | 16 | same documentation, Dataset A class inventory. |
| Dataset A train / validation / test | 27,130 / 4,734 / 4,758 | same documentation, executive summary and Dataset A size. |
| Dataset A speaker/group identities | 395 | same documentation, speaker independence section. |
| Dataset A speaker leakage | 0 train/val/test overlap | same documentation, speaker independence section. |
| Dataset B | `VCM_BALANCED` | same documentation, Dataset B section. |
| Dataset B training samples | 15,268 | same documentation, Dataset B final size. |
| Dataset B original / augmented | 13,801 / 1,467 | same documentation, Dataset B final size and augmentation sections. |
| Final E50/BG training manifest | 16,100 rows | E50 project status / requirements traceability and Phase BG training manifest evidence. |
| Active-project / Dataset2 / E41 adaptation rows | 13,070 / 2,800 / 230 | E50 project status / requirements traceability and Phase BG training manifest evidence. |

Provenance clarification: E50 was developed using selected material from the class collective Gold Dataset rather than using the entire collective dataset unchanged. The final E50 training manifest contains 16,100 rows: 13,070 active-project rows, 2,800 selected VCM_BALANCED rows, and 230 separately identified E41 Pi adaptation rows. The first two components are collective-derived/project-local command-data branches; the E41 rows are project-specific Pi deployment adaptation/calibration data and are not classified as Gold Dataset rows. The recovered E37 `Hey Pi` wake recordings are a separate project-specific Raspberry Pi wake-stage lineage; they are not Gold Dataset rows and are not part of the 16,100-row E50 command-model training manifest.
| Best epoch | 7 | `results/phase_bg_e50_bg_revised_vocab_original_preserve_e41_init_20260928/PHASE_BG_TRAINING_RESULTS.json`, `best_epoch`. |
| Internal validation loss | 1.3987702131271362 | same JSON, `best_internal_validation_loss`. |
| Internal validation accuracy | 0.6197039305768249 | same JSON, epoch 7 `val_accuracy`. |

Dataset source/licensing evidence is qualified, not blanket redistribution permission. The dataset source report documents Fluent Speech Commands, SLURP, Timers and Such, Multi-Sensor Voice Command DOI `10.48804/IEKKVZ` with CC-BY-4.0 and GDPR derivative download-tracking obligation, SET_TEMPERATURE project recordings/Piper TTS, and Google Speech Commands background-noise use. The correct public wording is to cite/follow upstream source terms and not to claim unrestricted redistribution unless separately established.

Training and internal validation values are not final Raspberry Pi performance metrics.

## 6. Raspberry Pi 5 Validation

Final physical benchmark population: **20 Pi 5 trials** = **19 valid command-label trials + 1 UNKNOWN/no-action trial**.

| Metric | Result | Meaning | Source |
|---|---:|---|---|
| Wake Success | 19/20 = 95.0% overall; 18/19 = 94.74% valid-command trials | Wake-stage success metric, not command-recognition accuracy | `ITEM16_AGGREGATE_METRICS.json`, wake success fields. |
| Raw Command Classification | 13/19 = 68.42% | Correct raw command classification among 19 valid command trials; not overall system accuracy | `ITEM16_AGGREGATE_METRICS.json`, raw classification fields. |
| End-to-End Action Success | 10/19 = 52.63% | Correct raw label, accepted by threshold policy, correct local action, response playback true, and return to listening | `ITEM16_AGGREGATE_METRICS.json`, end-to-end fields; Item 16 benchmark definition. |
| Accepted-Action Precision | 10/10 = 100% | Of accepted/executed valid commands, every accepted command produced the correct corresponding action | `ITEM16_AGGREGATE_METRICS.json`, accepted correct/wrong and accepted precision fields. |
| Safe Rejection | 10/10 = 100% | Among non-executed trials, all were safely rejected without routed action | `ITEM16_AGGREGATE_METRICS.json`, safe rejection and non-executed fields. |
| UNKNOWN Safety | 1/1 = 100% | UNKNOWN/no-action trial produced no unintended action | `ITEM16_AGGREGATE_METRICS.json`, UNKNOWN safety fields. |
| Return to Listening | 20/20 = 100% | Runtime returned to listening after every benchmark trial | `ITEM16_AGGREGATE_METRICS.json`, return-to-listening fields. |

Metrics use their documented denominators and definitions; they should not be collapsed into a single overall accuracy.

## 7. Final Benchmark / Demo Day Metrics

| Requirement | Final status | Value / statement | Evidence |
|---|---|---|---|
| Keyword / wake metric | Established | Wake success 19/20 = 95.0%; 18/19 = 94.74% on valid commands | Item 16 aggregate metrics. |
| Intent / command accuracy equivalent | Established with E50 terminology | Raw command classification 13/19 = 68.42% | Item 16 aggregate metrics. |
| End-to-end action success | Established | 10/19 = 52.63% | Item 16 aggregate metrics and definition. |
| Accepted-action precision | Established | 10/10 = 100%; not overall accuracy | Item 16 aggregate metrics. |
| Safe rejection | Established | 10/10 = 100% among non-executed final benchmark trials | Item 16 aggregate metrics. |
| UNKNOWN safety | Established | 1/1 = 100% | Item 16 aggregate metrics. |
| False-accept rate | Qualified bounded metric established | Bounded command-window out-of-scope FAR 0/4 = 0.0%; broad environmental FAR NOT ESTABLISHED | Item 12 safety sweep result summary and result JSONs. |
| Latency P95 | Established | CNN inference P95 34.40 ms | Item 15 saved-WAV inference summary. |
| RTF | Qualified established | CNN-only mean RTF 0.0080; P95 0.0086. Qualified command-pipeline RTF from response playback-start audit: mean 0.016543; P95 0.018500. | CNN-only RTF derived from Item 15 CNN latency and 4.0 s command input duration; command-pipeline RTF from `~/e50_demoday_final_audit/E50_RESPONSE_LATENCY_MEASUREMENTS_V2.csv`. |
| Response latency | Qualified established | Pi local response playback-start latency: 5 accepted/executed trials; mean 66.172 ms; P50 64.837 ms; P95 73.999 ms; P99 73.999 ms; max 73.999 ms. Boundary: command WAV capture completion -> first observed local `aplay` response WAV process. | External passive audit files `~/e50_demoday_final_audit/E50_RESPONSE_LATENCY_MEASUREMENTS_V2.csv` and `E50_RESPONSE_LATENCY_EVENTS_V2.csv`; frozen runtime not modified. |
| Runtime | Established | Local/offline-after-setup Raspberry Pi runtime; persistent return-to-listening 20/20 | Deployment README; Item 11 offline verification; Item 16. |
| Comparable-size baseline | Qualified established | E51 fresh-init same-parameter baseline: 66,483 params; Phase BG offline current95-compatible 77/90 = 85.56%, phase_av-compatible 131/194 = 67.53% | E51 candidate report and training config. |
| Pi specifications | Established | Raspberry Pi 5 Model B Rev 1.1; ARM Cortex-A76; 4 cores; aarch64; Linux 6.18.50+rpt-rpi-2712; Python 3.13.5; 7.9 GiB RAM; CPU max 2400 MHz; CPU min 1500 MHz; arm_freq=2400; arm_boost=1; throttled=0x0; mic `plughw:2,0`; audio output `plughw:CARD=vc4hdmi0,DEV=0` | Item 15 prep and inference summary; read-only Pi spec audit `~/e50_demoday_final_audit/E50_PI_SPECS_READONLY_FINAL.txt`. |

The bounded FAR definition used here is: false accepts / valid out-of-scope command-window safety prompts, where a false accept means the frozen E50 system accepted/executed a command. It does not claim a broad environmental false-accept rate over arbitrary background audio.

## 8. Comparable-Size Baseline

| Model | Parameters | Weight size | Initialization | Offline comparison evidence | Status |
|---|---:|---:|---|---|---|
| E51 comparable baseline | 66,483 | 251,009 bytes | Fresh initialization | current95-compatible 77/90 = 85.56%; phase_av-compatible 131/194 = 67.53%; combined revised test 2727/4230 = 64.47%; phase_av accepted precision 89.61% | Qualified offline same-architecture baseline |
| Final E50 | 66,483 | 251,734 bytes | Mapped E41 initialization | current95-compatible 83/90 = 92.22%; phase_av-compatible 139/194 = 71.65%; combined revised test 2724/4230 = 64.40%; phase_av accepted precision 91.92%; final Pi E2E 10/19 = 52.63% | Final selected system |

Source: `results/phase_bg_e51_bg_revised_vocab_original_preserve_fresh_init_20260928/PHASE_BG_E51_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_FRESH_INIT_CNN_CANDIDATE_20260928.md`; `results/phase_bg_e50_bg_revised_vocab_original_preserve_e41_init_20260928/PHASE_BG_E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT_CNN_CANDIDATE_20260928.md`; corresponding training config and model artifacts.

This comparison is qualified because E51 was not rerun as a second final physical Pi benchmark. It is a comparable-size offline baseline, not a second deployed runtime result.

## 9. Offline / Deployment

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

The GUI is the interface/launcher/display. Recognition, thresholding, routing, and action execution are runtime responsibilities.

## 10. Submission / Reproducibility

- **GitHub package:** `ME2_VCM_E50_GITHUB_PACKAGE_20260930`
- **Package status:** ready with documented limitations.
- **Deployment package:** `deployment/vcm_pi_package` with model artifacts, configs, runtime scripts, actions, responses, requirements, README, and launcher.
- **Dependency file:** `deployment/vcm_pi_package/requirements_pi.txt` lists `numpy`, `scipy`, `tensorflow`.
- **Documented setup:** Raspberry Pi OS setup, system packages, Python virtual environment, package copy, import checks, microphone checks, wake-gated runtime command, and touchscreen GUI command.
- **Reproduction wording:** The repository provides packaged deployment artifacts and launch commands. Reproduction requires the documented Raspberry Pi OS, Python/environment, dependency, audio-device, and hardware prerequisites. It should not be described as one-command reproduction on arbitrary computers.

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
| False-accept rate | Qualified established | Bounded command-window FAR 0/4 = 0.0%; broad environmental FAR not established. |
| Latency P95 | Established | CNN inference P95 34.40 ms; CNN-only. |
| RTF | Qualified established | CNN-only mean RTF 0.0080; P95 RTF 0.0086; qualified command-pipeline mean RTF 0.016543 and P95 RTF 0.018500. |
| Runtime | Established | Offline-after-setup local Pi runtime with deterministic routing and response audio. |
| GitHub package | Established | `ME2_VCM_E50_GITHUB_PACKAGE_20260930`. |
| Dataset citation/license | Qualified | Source/license report identifies upstream sources and terms; blanket redistribution not established. |
| Training logs + final checkpoint | Established | Training results/config/checkpoint evidence present. |
| Pi latency reproducibility | Qualified | Existing Item 15 saved-WAV inference benchmark documents CNN method; external passive V2 audit documents Pi local response playback-start latency without modifying frozen runtime. |
| Held-out unseen speakers | Qualified | Dataset speaker-independent splits established; formal statistical speaker-independent Pi benchmark not established. |
| Comparable-size baseline | Qualified established | E51 fresh-init same-parameter offline baseline exists; no second Pi benchmark for E51. |

## 12. Demo-Ready Facts

- Final runtime vocabulary: **19 labels**.
- All 19 final command labels are callable.
- The final physical benchmark contains **19 valid command-label trials**, one per label, plus **1 UNKNOWN/no-action trial**.
- A 13-command demo-ready subset was identified for demonstration; it is **not** a runtime whitelist.
- Runtime chain: **E37 wake -> E50 command CNN -> E40 policy -> deterministic router -> local action -> local response -> return to listening**.
- Final Pi benchmark highlights:
  - Raw command classification: **13/19 = 68.42%**.
  - End-to-end action success: **10/19 = 52.63%**.
  - Accepted-action precision: **10/10 = 100%**.
  - Safe rejection: **10/10 = 100%**.
  - Wake success: **19/20 = 95.0%**.
  - Return to listening: **20/20 = 100%**.
  - UNKNOWN safety: **1/1 = 100%**.
  - Bounded command-window false-accept rate: **0/4 = 0.0%**, qualified.
  - CNN inference P95: **34.40 ms**, CNN-only.
  - CNN-only P95 RTF: **0.0086**.
  - Response playback-start latency: **mean 66.172 ms; P95 73.999 ms**, qualified.
  - Qualified command-pipeline P95 RTF: **0.018500**.

## 13. Items Not Established

Do not fill these with estimates:

- Author/team information: **NOT ESTABLISHED IN PROJECT EVIDENCE**.
- A100 cluster information for final E50 training: **NOT ESTABLISHED IN PROJECT EVIDENCE**.
- GUI launch-to-ready latency: **NOT MEASURED**.
- Acoustic speaker-onset latency: **NOT MEASURED**. Pi local response playback-start latency is now measured as qualified external evidence: mean **66.172 ms**, P50 **64.837 ms**, P95/P99/max **73.999 ms** over 5 accepted/executed trials.
- Full end-to-end wake-to-action latency: **NOT MEASURED**.
- Full wake-to-response or acoustic end-to-end RTF: **NOT ESTABLISHED**. Qualified command-pipeline RTF to response playback start is established: mean **0.016543**, P95 **0.018500**.
- Broad environmental false-accept rate over arbitrary background/no-wake audio: **NOT ESTABLISHED**.
- Final ECE/calibration metric: **NOT MEASURED**.
- Formal noise/reverberation robustness benchmark: **NOT MEASURED**.
- Formal phrasing-variation benchmark: **NOT MEASURED**.
- Formal statistical speaker-independent final Pi benchmark: **NOT MEASURED**.
- Unrestricted dataset redistribution rights: **NOT ESTABLISHED AS A BLANKET CLAIM**.

Post-closure GUI telemetry is excluded from this report as evaluation evidence. It is not a benchmark, validation result, accuracy metric, or evidence of improved E50 performance.

## 14. Revision Integrity Confirmation

- New experiments performed for this revision: **NONE**.
- Existing benchmark values preserved: **YES**.
- Model weights changed: **NO**.
- E37 changed: **NO**.
- E40 changed: **NO**.
- Thresholds changed: **NO**.
- Dataset changed: **NO**.
- Training manifest changed: **NO**.
- Router/actions changed: **NO**.
- Response audio changed: **NO**.
- Runtime changed: **NO**.
- GUI changed: **NO**.
- GitHub package contents changed by this revision: **NO**.
- E53 accessed: **NO**.
- VCM executed: **NO**.
- Training executed: **NO**.
- Benchmark executed: **NO**.
- Documentation files created/updated by this revision: `FINAL_REQUIREMENTS_GAP_ANALYSIS.md`, `E50_FINAL_DEMODAY_METRICS.md`, `E50 DEMODAY REPORT.md`.


