# DECISIONS

Important engineering decisions for the ME2 VCM project.

## D001 - Final System Must Be Direct VCM, Not ASR Or LLM

### Date
2026-09-15

### Decision
Use a direct voice-command recognition pipeline:

`audio -> preprocessing -> log-Mel features -> tiny VCM -> command intent -> local action`

### Alternatives Considered
- ASR followed by text classification.
- ASR followed by an LLM.
- Cloud speech recognition.
- Assistant platforms such as Alexa or Google Assistant.

### Reason
The assignment explicitly says ASR models are undesirable for on-device computing because of footprint and requires standalone on-device operation with no LLM and no cloud models.

### Evidence
Assignment and VCM agent reference reviewed on 2026-09-15.

### Consequences
- The model must classify command intent directly from audio features.
- No final inference dependency may require internet access.
- Offline validation is required before final submission.

## D002 - Use Documentation-First Phased Workflow

### Date
2026-09-15

### Decision
Begin with requirements audit, project inventory, and documentation scaffold before dataset preprocessing or training.

### Alternatives Considered
- Immediately implement training code.
- Start with Raspberry Pi code.
- Start with model architecture experimentation.

### Reason
The project is examinable and requires an auditable engineering trail. Dataset assumptions must be checked before model work.

### Evidence
Initial project inventory found no dataset and no code.

### Consequences
- Phase 1 must inspect or locate the dataset.
- Experimental claims remain NOT YET MEASURED until run.

## D003 - Normalize Traceability Filename

### Date
2026-09-15

### Decision
Create `REQUIREMENTS_TRACEABILITY.md` without a space before `.md`.

### Alternatives Considered
- Create `REQUIREMENTS_TRACEABILITY .md` exactly as rendered in the PDF.

### Reason
The space appears to be formatting artifact or typo. A no-space filename is easier to reference and avoids confusion in scripts and documentation.

### Evidence
The VCM agent brief refers to requirements traceability multiple times with inconsistent spacing.

### Consequences
- All future references should use `REQUIREMENTS_TRACEABILITY.md`.

## D004 - Do Not Add New Augmentation Before Baseline

### Date
2026-09-15

### Decision
Proceed to the next task without adding new audio augmentation before the first baseline.

### Alternatives Considered
- Add more synthetic variants immediately.
- Apply random noise, gain, pitch, speed, or time-shift augmentation before the first model.
- Train first on the active dataset exactly as downloaded, then add augmentation only if measured results justify it.

### Reason
The active local dataset already includes substantial variation:
- fixed-phrase data: 20 classes, 50 speakers, 3 acoustic variations, 3,000 WAV files
- phrase-variant data: 20 classes, 30 speakers, 10 phrases per class, 3 acoustic variations, approximately 18,000 WAV files

Adding augmentation before a baseline would make it harder to understand whether model behavior comes from the dataset, architecture, preprocessing, or augmentation.

### Evidence
- `VCM Sources.pdf` lists Mark M's data sources and synthetic-generation approaches, including SLURP, Fluent Speech Commands, Google Speech Commands v2, eSpeak NG, and Chatterbox TTS with LibriSpeech/Common Voice references.
- Local support files report acoustic variation including clean, mild background noise, and quieter/farther microphone variants.
- Phase 1 local inventory verified 21,001 readable 16 kHz mono WAV files.

### Consequences
- The next task should be dataset metadata indexing and speaker-aware split creation.
- Any future augmentation must be train-only and recorded as a separate experiment.
- Validation/test data must not be augmented.
- UNKNOWN remains a separate requirement gap; it should not be confused with ordinary augmentation.

## D005 - Use 4-Second 40-Bin Log-Mel Features For First Baseline

### Date
2026-09-15

### Decision
Use deterministic 16 kHz mono audio loading with a 4.0-second fixed window and 40-bin log-Mel spectrograms for the first baseline.

Current feature shape:

`398 time frames x 40 Mel bins`

### Alternatives Considered
- 1-second or 2-second windows.
- Silence trimming before feature extraction.
- MFCCs instead of log-Mel.
- Librosa-based feature extraction.

### Reason
The active dataset duration range is 0.200 s to 3.880 s. A 4-second window avoids truncating normal dataset examples before the first baseline. Log-Mel also matches the intended technical direction in the VCM agent brief and is a common compact representation for command recognition.

The code uses NumPy/SciPy rather than librosa because NumPy and SciPy are available locally while librosa is not installed.

### Evidence
- `configs/preprocessing.json` records the preprocessing parameters.
- `python -m unittest discover -s tests -v` passed.
- `python preprocessing\inspect_preprocessing.py` produced `audio_shape=(64000,)` and `feature_shape=(398, 40)` for an indexed dataset WAV.

### Consequences
- All model training and evaluation should read features generated with the same configuration.
- Raspberry Pi inference must reproduce the same preprocessing.
- Shorter windows or silence trimming can be tested later as separate experiments if latency or model size becomes a problem.

## D006 - Use On-The-Fly Features For Smoke Baselines

### Date
2026-09-15

### Decision
Use on-the-fly log-Mel extraction for initial smoke baselines instead of bulk materializing all full `398 x 40` feature matrices.

### Alternatives Considered
- Precompute all log-Mel matrices before model training.
- Train directly from WAV files with a deep learning framework.
- Use pooled log-Mel statistics for fast sanity checks.

### Reason
The full included dataset has 21,000 WAV files. Storing every `398 x 40` float32 feature matrix would require roughly 1.3 GB before metadata or alternate feature variants. For Phase 3 smoke tests, on-the-fly extraction keeps storage small and verifies that the training code uses the exact same preprocessing configuration as Phase 2.

### Evidence
- `training/train_sklearn_baseline.py` successfully trained and saved smoke models using Phase 2 preprocessing.
- `python -m unittest discover -s tests -v` passed after adding the training scaffold.
- `E03_SMOKE_RAW_BALANCED` produced measured validation accuracy 0.245 and macro-F1 0.2446 on 600 train and 200 validation examples.

### Consequences
- Smoke baselines are reproducible and auditable without committing to a large feature cache.
- Final CNN training may still need a feature cache, dataset loader, or deep learning runtime.
- The sklearn smoke baseline is not the final assignment model.

## D007 - Sklearn Baseline Is A Pipeline Check, Not The Final VCM

### Date
2026-09-15

### Decision
Treat the sklearn baseline as a Phase 3 pipeline check, not as the final Raspberry Pi VCM model.

### Alternatives Considered
- Present the sklearn model as the final classifier.
- Wait to run any model experiment until PyTorch or TensorFlow is available.

### Reason
The available local Python environments currently include NumPy, SciPy, sklearn, and matplotlib, but not PyTorch or TensorFlow. A small sklearn baseline is useful for verifying dataset indexing, preprocessing, label encoding, artifact saving, and metric reporting. However, the assignment direction and exam notes expect a CNN-style command recognizer over log-Mel inputs.

### Evidence
- `E01_SMOKE`, `E02_SMOKE_FLAT`, and `E03_SMOKE_RAW_BALANCED` completed successfully.
- Best smoke result so far is only 0.245 validation accuracy and 0.2446 macro-F1.

### Consequences
- Next work should create or enable a CNN training path.
- The smoke baseline metrics should be reported honestly as early pipeline evidence only.

## D008 - Treat Sklearn MLP As Fallback Evidence Only

### Date
2026-09-15

### Decision
Run and log a nonlinear sklearn MLP smoke baseline only as fallback evidence while TensorFlow setup is blocked.

### Alternatives Considered
- Keep retrying TensorFlow package installation indefinitely.
- Call the sklearn MLP a CNN baseline.
- Stop without any measured progress.

### Reason
The local default Python environment has sklearn but no TensorFlow or PyTorch. A project-local virtual environment could not complete `ensurepip`, and pip package resolution for TensorFlow did not return promptly. The MLP baseline gives a measured nonlinear comparison without falsely claiming CNN training.

### Evidence
- `python -m unittest discover -s tests -v` passed 10 tests.
- `E04_SKLEARN_MLP_SMOKE` completed with validation accuracy 0.2600 and macro-F1 0.2319.
- The experiment output explicitly states that it is not the final CNN/TensorFlow model.

### Consequences
- The real CNN training task remains open.
- Do not use `E04_SKLEARN_MLP_SMOKE` as final model evidence.
- Continue looking for a TensorFlow-capable environment or a reliable installation path.

## D009 - Diagnose CNN Underperformance Before Adding More Data

### Date
2026-09-15

### Decision
Do not immediately add more command data after the first CNN smoke results. Diagnose the current CNN/training setup first.

### Alternatives Considered
- Add more synthetic/accent/noise command data now.
- Treat low validation accuracy as proof the dataset is insufficient.
- Proceed directly to Raspberry Pi trials with the current CNN.

### Reason
The first CNN smoke runs completed, but both training and validation accuracy are low. The best CNN smoke so far, `E06_CNN_SMOKE_NORM_20E`, reached only 0.2840 training accuracy and 0.1233 validation accuracy. Since the model is not fitting the small training subset strongly, the immediate issue may be architecture, training loop, preprocessing scale, label setup, or small-sample learning rather than dataset size.

### Evidence
- TensorFlow 2.20.0 installed and import verified.
- `E04_CNN_SMOKE`: validation accuracy 0.0967.
- `E05_CNN_SMOKE_NORM`: validation accuracy 0.0967.
- `E06_CNN_SMOKE_NORM_20E`: validation accuracy 0.1233.

### Consequences
- Next step should generate predictions/confusion diagnostics for CNN outputs.
- Data augmentation remains train-only and should wait until a measured weakness is identified.
- Raspberry Pi deployment should not use the current CNN as a final model.

## D010 - Use Fast BatchNorm For Next CNN Baseline

### Date
2026-09-15

### Decision
Use `configs/cnn_fast_batchnorm.json` for the next real CNN smoke/baseline.

### Alternatives Considered
- Remove BatchNorm entirely.
- Keep default BatchNorm momentum.
- Add more data immediately.

### Reason
The default BatchNorm CNN learned during training but failed inference on the same examples. The no-BatchNorm model did not learn well. Fast BatchNorm reached 0.8600 same-data accuracy and 0.8614 macro-F1 in `E11_CNN_OVERFIT_FASTBN`.

### Evidence
- `E09_CNN_OVERFIT_INTENT_BALANCED`: training accuracy 0.9600, same-data inference accuracy 0.1000.
- `E10_CNN_OVERFIT_INTENT_NOBN`: same-data inference accuracy 0.2200.
- `E11_CNN_OVERFIT_FASTBN`: same-data inference accuracy 0.8600, macro-F1 0.8614.

### Consequences
- The next proper CNN baseline should use fast BatchNorm.
- More data should still wait until after the corrected CNN baseline is measured.

## D011 - Continue Model Diagnosis After Corrected CNN Baseline

### Date
2026-09-15

### Decision
Do not move to data expansion or Raspberry Pi deployment yet. Continue diagnosing and improving the corrected CNN baseline.

### Alternatives Considered
- Add more synthetic/accent/noise data immediately.
- Deploy `E12_CNN_FASTBN_INTENT_SMOKE` to Raspberry Pi.
- Treat `E12` as final model evidence.

### Reason
`E12_CNN_FASTBN_INTENT_SMOKE` improved substantially over earlier CNN runs, but validation performance remains too low for final deployment and the model still over-predicts `THERMOSTAT`.

### Evidence
- `E12_CNN_FASTBN_INTENT_SMOKE`: validation accuracy 0.3533, macro-F1 0.3716.
- Intent-balanced diagnostics: 173 of 300 validation examples predicted as `THERMOSTAT`.

### Consequences
- Next work should inspect per-class confusion and improve architecture/training.
- Real microphone/laptop trials should wait until the model is less biased.

## D012 - Use Stronger No-Dropout Dense CNN As Current Best Smoke Baseline

### Date
2026-09-16

### Decision
Use `configs/cnn_fastbn_dense_nodropout.json` as the best CNN smoke/baseline configuration for continued development.

### Alternatives Considered
- Keep only the smaller `configs/cnn_fast_batchnorm.json` model.
- Use the stronger dense model with dropout.
- Add more synthetic or accent data immediately.

### Reason
The dense model with dropout did not pass the tiny overfit sanity test cleanly, while the no-dropout dense model reached perfect same-data validation. On the separate intent-balanced smoke validation set, the no-dropout dense model substantially improved over the smaller fast-BatchNorm CNN.

### Evidence
- `E13_CNN_DENSE_OVERFIT`: same-data validation accuracy 0.5400, macro-F1 0.5311.
- `E14_CNN_DENSE_NODROPOUT_OVERFIT`: same-data validation accuracy 1.0000, macro-F1 1.0000.
- `E15_CNN_DENSE_NODROPOUT_INTENT_SMOKE`: validation accuracy 0.5533, macro-F1 0.5411.
- `E12_CNN_FASTBN_INTENT_SMOKE`: validation accuracy 0.3533, macro-F1 0.3716.

### Consequences
- The CNN training path is confirmed capable of learning the log-Mel inputs.
- `E15` was an intermediate best smoke baseline, later superseded by `E16`.
- The next improvement should focus on training stability, per-class confusion, and full training scale before deployment.
- Additional data is still deferred until a measured data weakness is identified.

## D013 - Track Best Validation Epoch During CNN Smoke Training

### Date
2026-09-16

### Decision
Add optional best-validation tracking to `training/train_cnn_keras.py` and use it for the current CNN smoke baseline.

### Alternatives Considered
- Save only the final epoch weights.
- Stop training manually when validation looks good.
- Immediately switch to a different architecture.

### Reason
The no-dropout dense CNN showed unstable late training behavior. Validation performance rose and fell across epochs, so saving only the final epoch can miss the best checkpoint.

### Evidence
- `E15_CNN_DENSE_NODROPOUT_INTENT_SMOKE`: final validation accuracy 0.5533, macro-F1 0.5411.
- `E16_CNN_DENSE_NODROPOUT_BESTVAL_SMOKE`: best validation epoch 50, validation accuracy 0.5600, macro-F1 0.5434.
- `E16` final epoch without best tracking would have matched the E15 final result, but the saved best checkpoint is slightly stronger.

### Consequences
- `E16` was the best smoke baseline at that point, later superseded by `E19`.
- Best-validation tracking should be used for future smoke or larger training runs.
- The next model tuning step should test lower learning rate and/or mild regularization, not data expansion yet.

## D014 - Reject Lower Learning Rate Alone For Current CNN Smoke

### Date
2026-09-16

### Decision
Do not replace `E16` with the lower-learning-rate `E17` run.

### Alternatives Considered
- Promote `E17` because it used a smoother 0.0003 learning rate.
- Continue with the original 0.001 learning rate plus best-validation tracking.
- Try a different regularization or data scale experiment next.

### Reason
The lower learning rate still allowed the model to memorize the 1,000-example training subset, but validation performance stayed much lower than `E16`. This means the lower learning rate alone did not improve generalization.

### Evidence
- `E16_CNN_DENSE_NODROPOUT_BESTVAL_SMOKE`: validation accuracy 0.5600, macro-F1 0.5434.
- `E17_CNN_DENSE_NODROPOUT_LR3E4_BESTVAL_SMOKE`: best epoch 56, validation accuracy 0.3533, macro-F1 0.3594.
- `E17` reached 1.0000 training accuracy for many late epochs, but validation remained weak.

### Consequences
- Keep `E16` as the best smoke baseline at that point. It was later superseded by `E19`.
- Future tuning should test mild regularization, different sampling scale, or full training with best-validation tracking instead of simply lowering learning rate.

## D015 - Prefer Larger Training Coverage Over Mild Dropout For Current CNN

### Date
2026-09-16

### Decision
Promote `E19_CNN_DENSE_NODROPOUT_300PI_BESTVAL` as the current best CNN smoke baseline.

### Alternatives Considered
- Use mild dropout with the same 100 examples per intent as E16.
- Keep E16 as the best baseline.
- Add new/generated data immediately.

### Reason
Mild dropout did not beat E16, but increasing the training subset from 100 to 300 examples per intent produced a large validation gain. This suggests the current dataset already has useful coverage and the model benefits from using more of it before creating new data.

### Evidence
- `E16_CNN_DENSE_NODROPOUT_BESTVAL_SMOKE`: 1,000 train examples, validation accuracy 0.5600, macro-F1 0.5434.
- `E18_CNN_DENSE_DROPOUT01_BESTVAL_SMOKE`: 1,000 train examples, validation accuracy 0.4967, macro-F1 0.4667.
- `E19_CNN_DENSE_NODROPOUT_300PI_BESTVAL`: 3,000 train examples, validation accuracy 0.7233, macro-F1 0.7198.

### Consequences
- Keep `configs/cnn_fastbn_dense_nodropout.json` as the best architecture/config for now.
- Use larger training subsets or full training before deciding whether to generate more data.
- `MEDIA_CONTROL` is now the clearest weak intent in diagnostics and should be inspected next.

## D016 - Continue Scaling Existing Dataset Before Adding New Data

### Date
2026-09-16

### Decision
Promote `E20_CNN_DENSE_NODROPOUT_600PI_BESTVAL` as the current best CNN smoke baseline and continue using the existing dataset before adding or generating new data.

### Alternatives Considered
- Add new synthetic/accent/noise data immediately.
- Stop at E19 and move directly to deployment.
- Use confidence thresholding alone to compensate for model errors.

### Reason
Increasing training coverage from 300 to 600 examples per intent improved validation again. This gives direct evidence that the existing dataset still contains useful signal that the CNN can learn.

### Evidence
- `E19_CNN_DENSE_NODROPOUT_300PI_BESTVAL`: 3,000 train examples, validation accuracy 0.7233, macro-F1 0.7198.
- `E20_CNN_DENSE_NODROPOUT_600PI_BESTVAL`: 6,000 train examples, validation accuracy 0.8133, macro-F1 0.8113.
- E20 confidence threshold 0.90: accepts 250/300 validation examples, accepted-command accuracy 0.8800.
- E20 confidence threshold 0.95: accepts 232/300 validation examples, accepted-command accuracy 0.9181.

### Consequences
- E20 is the current best CNN smoke baseline.
- The next modeling step should scale closer to the full training set or run a more robust validation sample.
- Confidence-threshold rejection should be included in the Raspberry Pi inference design.
- Additional dataset construction is still not justified until full existing-data scaling and real microphone trials reveal a specific gap.

## D017 - Promote E21 But Track MEDIA_CONTROL Precision Risk

### Date
2026-09-16

### Decision
Promote `E21_CNN_DENSE_NODROPOUT_1000PI_BESTVAL` as the current best CNN smoke baseline by macro-F1, while explicitly tracking `MEDIA_CONTROL` precision as a remaining risk.

### Alternatives Considered
- Keep `E20` because it had better `MEDIA_CONTROL` precision.
- Promote `E21` because it has the best overall macro-F1.
- Add new data immediately for media commands.

### Reason
E21 improves overall validation performance and macro-F1, and it improves `MEDIA_CONTROL` recall. However, it predicts `MEDIA_CONTROL` more often than E20, reducing precision for that class.

### Evidence
- `E20_CNN_DENSE_NODROPOUT_600PI_BESTVAL`: validation accuracy 0.8133, macro-F1 0.8113.
- `E21_CNN_DENSE_NODROPOUT_1000PI_BESTVAL`: validation accuracy 0.8267, macro-F1 0.8304.
- E21 `MEDIA_CONTROL`: precision 0.50, recall 0.70, F1 0.58.
- E21 confidence threshold 0.90: accepts 255/300 examples, accepted-command accuracy 0.8902.
- E21 confidence threshold 0.95: accepts 241/300 examples, accepted-command accuracy 0.9046.

### Consequences
- E21 is the current best overall smoke baseline.
- For real command execution, confidence-threshold rejection remains important.
- Laptop microphone trials can proceed with E21, but observed false media triggers should be logged carefully.
- New data is still deferred until live microphone trials reveal a specific weakness.

## D018 - Treat Phase C as Frozen Baseline and Define E43 as Targeted Recovery

### Date
2026-09-26

### Decision
Use Phase C as the frozen diagnostic baseline and define E43 as a targeted
recovery experiment, not broad retraining and not threshold tuning.

### Alternatives Considered
- Start training immediately after Phase C.
- Lower thresholds to make low-confidence correct commands pass.
- Treat `LIGHT_OFF` and `NEXT` static output as model failures.
- Use the Phase C validation recordings as recovery/training data.

### Reason
Phase C isolated failure layers. The most serious issue is a wrong accepted
command: `CREATE_REMINDER` was predicted and executed as `LIST_REMINDERS`.
Other failures belong to different layers: safe VCM misclassifications,
confidence/rejection misses, and response/output uncertainty. Mixing all of
these into one broad retraining step would hide causality.

### Evidence
- `outputs/pi_evidence_pullback_20260925_214022/PHASE_C_TRIAL_TABLE.csv`
- `outputs/pi_evidence_pullback_20260925_214022/PHASE_C_BASELINE_SUMMARY_20260925.md`
- `PHASE_C_ERROR_ANALYSIS_20260925.md`
- `PHASE_E43_EXPERIMENT_SPEC_20260925.md`

### Consequences
- Phase C remains the reproducible comparison baseline.
- E43 may add targeted recovery data, but recovery clips must not become final
  validation evidence.
- Architecture and preprocessing remain fixed for initial E43.
- Thresholds remain fixed during initial E43; any threshold change requires a
  separate calibration decision after score and false-accept analysis.
- `LIGHT_OFF` and `NEXT` require output/action-path repair or retest before
  being treated as command-model failures.

## D019 - Classify LIGHT_OFF Phase C Partial as Output Mapping Bug, Not Model Failure

### Date
2026-09-26

### Decision
Treat the Phase C `LIGHT_OFF` partial pass as an action-output mapping bug, not as an E43 command-model training target.

### Reason
The command model predicted `LIGHT_OFF` correctly, routing selected `light.off`, and direct playback of `pi_responses/light_off.wav` was clear. The action-layer response map did not include `light.off`, so no response audio was played during action execution.

### Evidence
- Phase C trial: `phase_c_light_off_20260925_001`
- Direct WAV playback: clear
- Action-layer retest after mapping fix: `action: light.off`, `hardware_applied: true`
- User heard: "switching the light off"

### Consequence
Do not include `LIGHT_OFF` as an E43 model-retraining target. Keep it in regression validation to verify the output-path fix remains working.

## D020 - Remove NEXT From E43 Model-Retraining Targets Unless Fresh Validation Regresses

### Date
2026-09-26

### Decision
Do not treat `NEXT` as an E43 command-model recovery target after the action-layer retest.

### Reason
Phase C retry already showed correct command classification and routing for `NEXT`. The follow-up action-layer retest returned `media.next`, `hardware_applied: true`, and clear playback.

### Evidence
- Phase C command-stage trial: `phase_c_next_20260925_002`
- Action-layer retest on 2026-09-26: clear playback and `hardware_applied: true`

### Consequence
Keep `NEXT` in regression validation. Only reopen it as a model target if fresh validation produces new command-classification or confidence failures.

## D021 - Finalize E43 Target List After Output/Action Repairs

### Date
2026-09-26

### Decision
Keep `LIGHT_OFF` and `NEXT` out of E43 command-model retraining. Treat both as regression-validation commands after their output/action-path evidence improved.

### Reason
Both commands had correct Phase C VCM/routing evidence. Follow-up work showed `LIGHT_OFF` needed a response-audio mapping repair, while `NEXT` passed action-layer retest with clear playback. These are not justified model-training targets unless future fresh validation shows new classification or confidence failures.

### Evidence
- `PHASE_E43_EXPERIMENT_SPEC_20260925.md`
- Decision `D019`
- Decision `D020`
- `LIGHT_OFF` action-layer retest: `hardware_applied: true`, response heard
- `NEXT` action-layer retest: `hardware_applied: true`, clear playback

### Consequence
E43 remains focused on the higher-value model evidence: `CREATE_REMINDER` / `LIST_REMINDERS`, `LIGHT_ON`, `COLOR`, and confidence/rejection behavior for `PLAY_MUSIC`, `BRIGHTNESS`, `PAUSE`, and `VOLUME_DOWN`.

## D022 - Use Explicit E43 Phrase-Based Recovery Collection

### Date
2026-09-27

### Decision
Collect E43 recovery audio with an explicit phrase plan instead of blindly using the older all-command calibration helper.

### Reason
The Phase C `CREATE_REMINDER` failure occurred on the phrase "create reminder". The older calibration helper prompts `CREATE_REMINDER` as "reminder drink water", which does not directly target the observed failure. E43 must match the evidence-driven failure mode.

### Evidence
- `phase_c_create_reminder_20260925_001`
- `PHASE_C_ERROR_ANALYSIS_20260925.md`
- `PHASE_E43_RECOVERY_DATA_COLLECTION_PLAN_20260927.md`

### Consequence
E43 recovery clips will be stored as `E43_TARGETED_RECOVERY_DATA_V1` under `pi_validation/e43_targeted_recovery_20260927_v1/` and treated as recovery/training data only. Fresh validation must be recorded later after training.

## D023 - Use Cautious E43 Training After Smoke Regression

### Date
2026-09-27

### Decision
Do not scale the first smoke configuration directly. Run a cautious candidate that preserves E41 normalization, starts from E41 weights, and uses a smaller targeted update.

### Reason
The smoke model completed successfully but increased wrong accepted predictions at threshold 0.90 from 4 to 7 and regressed several previously reliable labels. That makes promotion unsafe even though some target labels improved.

### Evidence
- `PHASE_E43_TRAINING_SMOKE_RESULT_20260927.md`
- `PHASE_E43_SMOKE_REGRESSION_ANALYSIS_20260927.md`
- `PHASE_E43_CAUTIOUS_TRAINING_SPEC_20260927.md`

### Consequence
`E43_TARGETED_COMMAND_RECOVERY_CAUTIOUS` is the next candidate. It remains a training experiment only until it passes comparison analysis and then fresh independent validation.

## D024 - Do Not Promote E43 Cautious Candidate

### Date
2026-09-27

### Decision
Do not promote `E43_TARGETED_COMMAND_RECOVERY_CAUTIOUS`.

### Reason
The cautious candidate reduced smoke wrong-accept regressions, but it remained below E41 current95 re-evaluation on accuracy and macro-F1. It also failed the E43 recovery `COLOR` set with 0/10 correct.

### Evidence
- `PHASE_E43_CAUTIOUS_TRAINING_RESULT_20260927.md`
- `results/tables/E43_CAUTIOUS_VS_E41_SMOKE_SUMMARY.csv`
- `results/tables/E43_CAUTIOUS_VS_E41_SMOKE_PER_LABEL.csv`
- `results/tables/E43_CAUTIOUS_VS_E41_SMOKE_WRONG_ACCEPTED.csv`

### Consequence
Keep E43 cautious as evidence only. Next work should analyze recovery prediction failures before another training run.

## D025 - Pause E43 Retraining Until Recovery Errors Are Inspected

### Date
2026-09-27

### Decision
Do not start another E43 training run immediately after the cautious model.

### Reason
The recovery-error analysis showed mixed failure modes. `COLOR` was 0/10 but safely rejected, while `CREATE_REMINDER`, `VOLUME_DOWN`, and several contrast/regression clips produced wrong accepted predictions. These require data/audio and class-separation inspection before selecting the next intervention.

### Evidence
- `PHASE_E43_CAUTIOUS_RECOVERY_ERROR_ANALYSIS_20260927.md`
- `results/tables/E43_CAUTIOUS_FRESH_RECOVERY_ERROR_SUMMARY.csv`
- `results/tables/E43_CAUTIOUS_FRESH_RECOVERY_ERRORS.csv`

### Consequence
Next work should inspect audio quality and prediction behavior for the failing recovery clips, especially `COLOR`, `CREATE_REMINDER`, and `VOLUME_DOWN`, before defining any E43 follow-up training or threshold change.

## D026 - Treat COLOR Failure As Phrase-Coverage Issue Before Retraining

### Date
2026-09-27

### Decision
Do not treat `COLOR` as a simple low-confidence threshold problem. Treat it as a phrase-coverage/class-separation problem until disproven.

### Reason
Audio QC showed the E43 `COLOR` clips were structurally valid and not grossly quiet or truncated. The original all-command calibration data used the phrase `color red`, while Phase C and E43 recovery used the shorter phrase `color`.

### Evidence
- `PHASE_E43_RECOVERY_AUDIO_DATA_INSPECTION_20260927.md`
- `results/tables/E43_RECOVERY_AUDIO_QC_BY_LABEL.csv`
- `data/calibration/pi_validation/all_commands_calibration_15x/manifest.csv`

### Consequence
The next data intervention should explicitly cover both `color` and `color red`, and should include contrast examples for classes that `COLOR` is confused with.

## D027 - Reject E44 Focused Color Recovery Candidate

### Date
2026-09-27

### Decision
Do not promote `E44_FOCUSED_COLOR_RECOVERY_CAUTIOUS`.

### Reason
The model degraded holdout accuracy and macro-F1 compared with E41 and still failed the intended `COLOR` recovery objective. Combined recovery `COLOR` performance was only 3/30 correct and produced 11 wrong accepted `COLOR` errors at threshold 0.90.

### Evidence
- `PHASE_E44_CANDIDATE_TRAINING_RESULT_20260927.md`
- `results/tables/E44_CANDIDATE_VS_E41_E43_HOLDOUT_SUMMARY.csv`
- `results/tables/E44_CANDIDATE_COMBINED_RECOVERY_ERROR_SUMMARY.csv`

### Consequence
Do not use E44 for live validation. The next work should investigate whether `COLOR` as a one-word raw command is too ambiguous for the current tiny VCM setup or whether command phrase design/data collection needs revision.

## D028 - Treat COLOR As Unresolved Command-Design Issue

### Date
2026-09-27

### Decision
Do not continue blind retraining for `COLOR`. Treat `COLOR` as unresolved until the command phrase design or dataset design is revised.

### Reason
Three model states failed the one-word `color` phrase on E44 clips:

- E41: 0/10
- E43 cautious: 0/10
- E44 cautious: 0/10

The phrase `color red` also remained weak. E44 achieved only 3/10 and introduced high-confidence wrong accepted `COLOR` errors.

### Evidence
- `PHASE_E44_COLOR_COMMAND_DESIGN_AUDIT_20260927.md`
- `results/tables/E44_COLOR_DESIGN_COLOR_ONLY_BY_MODEL_PHRASE.csv`

### Consequence
Requirements traceability should distinguish `LIGHT_ADJUST` category coverage from the unreliable raw `COLOR` label. `BRIGHTNESS` may provide partial `LIGHT_ADJUST` evidence, but `COLOR` is not verified.

## D029 - Keep E41 As Current Candidate After E43/E44 Rejection

### Date
2026-09-27

### Decision
Use `E41_FUNCTIONAL_NON_LED_RECOVERY` as the current evidence-supported
candidate for the next validation/benchmark planning step. Do not promote E43
or E44.

### Reason
E41 remains strongest on the same 95-example holdout:

- E41 current95 accuracy 0.9473684210526315, macro-F1 0.947900053163211,
  wrong accepted at threshold 0.90 = 2.
- E43 cautious accuracy 0.9157894736842105, macro-F1 0.9156831472620945,
  wrong accepted at threshold 0.90 = 2.
- E44 cautious accuracy 0.8947368421052632, macro-F1 0.896785670469881,
  wrong accepted at threshold 0.90 = 1.

E44 reduced one wrong accept but degraded accuracy/F1 and did not solve the
targeted `COLOR` recovery problem.

### Evidence
- `PHASE_R_REQUIREMENTS_MODEL_SELECTION_AUDIT_20260927.md`
- `results/tables/E44_CANDIDATE_VS_E41_E43_HOLDOUT_SUMMARY.csv`
- `results/tables/E41_FUNCTIONAL_NON_LED_RECOVERY_CURRENT95_REEVAL_metrics.json`

### Consequence
The project should proceed from E41 as the current candidate, while keeping
`COLOR`, `CREATE_REMINDER`, and several threshold-rejected commands marked
incomplete. E41 still needs current-candidate Pi benchmark and fresh validation
evidence before final claims.

## D030 - Do Not Use Threshold-Only Repair For Remaining Phase C Failures

### Date
2026-09-27

### Decision
Do not lower the global threshold or rely on threshold-only repair for the
remaining Phase C failures.

### Reason
The most serious Phase C failure was not a low-confidence rejection. It was
`CREATE_REMINDER` misclassified as `LIST_REMINDERS` at confidence
0.9953140020370483, accepted and routed to the wrong reminder action. Lowering
thresholds cannot fix that. Raising the `LIST_REMINDERS` threshold enough to
block that case would risk rejecting correct `LIST_REMINDERS` evidence.

E41 under the E40 threshold policy on the 95-example holdout had 80 accepted
predictions, 79 accepted correct, and 1 accepted wrong. The remaining correct
rejections need label-specific analysis, not a global threshold change.

### Evidence
- `PHASE_T_REMAINING_FAILURE_REPAIR_SELECTION_20260927.md`
- `results/tables/PHASE_T_E41_E40_POLICY_HOLDOUT_SUMMARY.csv`
- `results/tables/PHASE_T_PHASE_C_REMAINING_FAILURES.csv`

### Consequence
The next work should specify a targeted E45 repair, prioritizing reminder class
separation and `LIGHT_ON`, while keeping `COLOR` separate as a command-design
issue.

## D031 - E45 Must Be Targeted Manifest-First, Not Immediate Training

### Date
2026-09-27

### Decision
Define `E45_TARGETED_REMINDER_LIGHTON_CONFIDENCE_REPAIR` as a targeted repair
candidate, but do not start training until the derived E45 manifest is built and
readiness-checked.

### Reason
E43 and E44 showed that training without tight data control can damage holdout
behavior or fail the intended repair. E45 should change only the recovery data
composition first, while keeping E41 base weights, E41 normalization,
architecture, preprocessing, parser, router, and action logic fixed.

### Evidence
- `PHASE_T_REMAINING_FAILURE_REPAIR_SELECTION_20260927.md`
- `PHASE_U_E45_TARGETED_REPAIR_SPEC_20260927.md`

### Consequence
The next safe task is to construct and audit
`outputs/e45_targeted_repair_20260927/manifest_e45_targeted_recovery_for_training.csv`.
Training remains blocked until that audit passes.

## D032 - E45 Manifest Readiness Passed

### Date
2026-09-27

### Decision
The E45 derived manifest is ready for a separate training experiment.

### Reason
The manifest contains 125 targeted recovery rows, 125 unique WAV paths, zero
duplicates, zero missing files, and zero bad audio-format files. `COLOR` rows
were deliberately excluded because `COLOR` remains a command-design issue.

### Evidence
- `PHASE_V_E45_MANIFEST_READINESS_AUDIT_20260927.md`
- `outputs/e45_targeted_repair_20260927/manifest_e45_targeted_recovery_for_training.csv`
- `outputs/e45_targeted_repair_20260927/manifest_e45_targeted_recovery_readiness_summary.json`

### Consequence
E45 training may be run as the next separate experiment step using the fixed
specification. Recovery data remains training-only and must not become final
validation data.

## D033 - Do Not Promote E45 Targeted Repair

### Date
2026-09-27

### Decision
Do not promote `E45_TARGETED_REMINDER_LIGHTON_CONFIDENCE_REPAIR`.

### Reason
E45 did not outperform the current E41 candidate on the 95-example holdout and
it increased wrong accepted predictions under the same E40 threshold policy.
E45 holdout accuracy was 0.9368421052631579 and macro-F1 was
0.935805422647528, compared with E41 current95 accuracy
0.9473684210526315 and macro-F1 0.947900053163211. Under E40 policy, E45 had
3 accepted-wrong holdout predictions, while E41 had 1.

### Evidence
- `PHASE_W_E45_TRAINING_RESULT_20260927.md`
- `results/tables/E45_CANDIDATE_VS_E41_E43_E44_HOLDOUT_SUMMARY.csv`
- `results/tables/E45_VS_E41_E40_POLICY_HOLDOUT_COMPARISON.csv`
- `results/tables/E45_E40_POLICY_HOLDOUT_WRONG_ACCEPTED.csv`
- `results/tables/E45_E40_POLICY_RECOVERY_WRONG_ACCEPTED.csv`

### Consequence
Keep E41 as the current evidence-supported candidate. Preserve E45 as a
documented targeted recovery experiment, but do not use it for fresh live
validation or final claims. Any next repair must start with E45 error analysis,
not another broad training run.

## D034 - Next Repair Must Target E45 Wrong-Accept Safety Regressions

### Date
2026-09-27

### Decision
Do not start another model-training run immediately. If another intervention is
attempted, it must be a tightly specified safety repair for the actual E45
wrong-accepted pairs.

### Reason
E45 did not simply leave the E41 wrong accept in place. It removed E41's
offline `COLOR -> WEATHER` wrong accept but introduced three new wrong
accepted pairs: `PAUSE -> CALL`, `STOP -> NEXT`, and
`CREATE_REMINDER -> ALARM`. Two of these changed E41 safe correct rejections
into unsafe accepted wrong predictions, and one changed an already-wrong but
safe rejection into an unsafe accept.

`COLOR` remains a separate command-design issue because E45 explicitly excluded
`COLOR` from the targeted recovery manifest.

### Evidence
- `PHASE_X_E45_WRONG_ACCEPT_REGRESSION_ANALYSIS_20260927.md`
- `results/tables/PHASE_X_E45_WRONG_ACCEPTED_VS_E41_ROWS.csv`
- `results/tables/PHASE_X_E41_WRONG_ACCEPTED_VS_E45_ROWS.csv`
- `results/tables/PHASE_X_E41_E45_WRONG_ACCEPT_CONFUSION_PAIRS.csv`

### Consequence
The next experiment, if any, should be specified around wrong-action safety and
confidence calibration, not broad recovery upweighting.

## D035 - Diagnose Calibration/Policy Before Any Further Retraining

### Date
2026-09-27

### Decision
Choose next-action recommendation B: confidence/rejection calibration or policy
analysis is justified without retraining. Do not execute the intervention yet.

### Reason
Phase Y showed that E45's unsafe accepts were caused at the classifier and
confidence-policy level. `PAUSE_015.wav` and `CREATE_REMINDER_014.wav` changed
from safe E41 correct rejections into wrong high-confidence E45 classifications.
`STOP_013.wav` kept the same wrong `NEXT` prediction but increased confidence
enough to cross the E40 policy threshold.

No router/action-layer mechanism explains the regressions, and lowering the
global threshold would move in the wrong safety direction.

### Evidence
- `PHASE_Y_E45_SAFETY_REGRESSION_DIAGNOSIS_20260927.md`
- `results/tables/PHASE_Y_E45_SAFETY_REGRESSION_THREE_SAMPLE_COMPARISON.csv`
- `results/tables/PHASE_Y_E45_ADDITIONAL_ACCEPTED_WRONG_REGRESSIONS.csv`
- `results/tables/PHASE_Y_E41_E45_REGRESSION_PAIR_OCCURRENCES.csv`

### Consequence
E41 remains frozen as the current evidence-supported candidate. The next phase,
if run, should analyze confidence/rejection policy around the identified
high-risk pairs before any retraining or data repair is attempted.

## D036 - Recommend Narrow Class-Specific Calibration Experiment, Not Production Change

### Date
2026-09-27

### Decision
Recommend option B: conduct a narrow class-specific threshold calibration
experiment. Do not execute it yet and do not change production thresholds.

### Reason
Phase Z showed that the current E40 `NEXT = 0.98` threshold provides useful
safety by rejecting E41 `STOP_013.wav` misclassified as `NEXT` at confidence
0.979959. Lowering `NEXT` below 0.98 would increase accepted-wrong predictions
in the existing holdout.

The same analysis found a narrow PAUSE calibration hypothesis: lowering
`PAUSE` from 0.99 to around 0.96 would recover one correct PAUSE holdout sample
without increasing accepted-wrong predictions in the current small holdout.
That is enough to justify a separate calibration experiment, but not enough to
edit the production policy directly.

### Evidence
- `PHASE_Z_E41_CONFIDENCE_REJECTION_POLICY_ANALYSIS_20260927.md`
- `results/tables/PHASE_Z_E41_RELEVANT_CLASS_POLICY_OUTCOMES.csv`
- `results/tables/PHASE_Z_E41_CLASS_SPECIFIC_THRESHOLD_WHATIF.csv`
- `results/tables/PHASE_Z_E41_STOP_NEXT_POLICY_ROWS.csv`

### Consequence
E41 remains frozen. E40 remains unchanged. Any next phase should specify a
narrow calibration experiment before changing thresholds.

## D037 - Require Fresh Independent PAUSE Calibration Before Any Threshold Change

### Date
2026-09-27

### Decision
Do not change the production PAUSE threshold. Treat `PAUSE = 0.96` as an
unvalidated hypothesis requiring a fresh independent calibration experiment.

### Reason
Phase AA audited the available PAUSE evidence and found no suitable independent
calibration set. The 95-example holdout produced the hypothesis, so it cannot
validate it. E43 PAUSE clips are recovery/training-linked evidence, Phase C has
only one PAUSE trial, and E44 has no PAUSE examples.

### Evidence
- `PHASE_AA_PAUSE_THRESHOLD_CALIBRATION_SPEC_20260927.md`
- `results/tables/PHASE_AA_PAUSE_DATA_SOURCE_AUDIT.csv`
- `PHASE_Z_E41_CONFIDENCE_REJECTION_POLICY_ANALYSIS_20260927.md`

### Consequence
E41 remains the frozen current candidate. E40 remains unchanged. `NEXT = 0.98`
must stay fixed. Any future PAUSE threshold experiment must use fresh
calibration data that is separate from recovery/training data and from final
fresh validation.

## 2026-09-27 - E46 Not Promoted

Decision: Do not promote E46_TARGETED_LIVE_FAILURE_RECOVERY.

Evidence: E46 decreased frozen 95-example holdout accuracy from E41's 90/95 to 87/95, introduced six E41-correct to E46-wrong regressions, and increased frozen E40 accepted-wrong cases from 1 to 2. E46 remains an experimental artifact only. E41 remains the current frozen candidate.

## 2026-09-27 - E46 Regression Diagnosis Confirms No Promotion

Decision: Continue to keep E41 frozen and do not promote E46.

Evidence: The post-experiment diagnosis confirmed E46 lowered holdout accuracy from 94.74% to 91.58%, lowered accepted-action precision from 98.75% to 97.30%, and introduced accepted-wrong STOP -> NEXT and VOLUME_DOWN -> VOLUME_UP cases under frozen E40. The observed regression pattern is mixed across target and contrast boundaries. No causal claim is made that Phase AF data alone caused the regressions.

## 2026-09-27 - Phase AG+ Shows E46 Regressions Are Mostly Classifier-Output Changes

Decision: Keep E41 frozen. Do not promote E46. Do not change E40 thresholds from Phase AG+ alone. Do not start E47 without a separate experimental question and authorization.

Evidence: Phase AG+ analyzed the artifact-defined nine correctness-flip samples. All six E41-correct -> E46-wrong regressions were top-1 prediction changes; none were purely same-label confidence/acceptance changes. Four of the six also changed the E40 acceptance/rejection outcome. The two E46 accepted-wrong cases had different mechanisms: STOP_013.wav retained the same wrong NEXT prediction but E46 confidence crossed the frozen NEXT 0.98 threshold, while VOLUME_DOWN_011.wav changed top-1 from VOLUME_DOWN to VOLUME_UP and crossed the frozen VOLUME_UP threshold.

Consequence: A future confidence-calibration investigation is justified only as a separate diagnostic because of STOP_013.wav. A future classifier experiment would need a separate design or ablation; Phase AG+ does not authorize immediate retraining.

## 2026-09-27 - Adopt Controlled Candidate Repair As The Next Project Standard

Decision: Change the engineering objective from "determine whether E41 is good enough" to "make the live Pi VCM work through controlled experiments." Continue working toward a demonstrably reliable VCM rather than accepting Phase AD performance as the endpoint.

Evidence: Phase AD showed live end-to-end performance gaps, while E45 and E46 showed that untargeted or insufficiently controlled model changes can improve some cases while creating regressions. The key unsafe outcome is wrong prediction -> accepted -> wrong action. Correct rejection of uncertain or wrong commands is acceptable behavior for an action-triggering VCM.

Promotion gate: any future candidate must demonstrate no unacceptable degradation on the frozen 95-example holdout, no increase in accepted-wrong actions, improvement in documented high-risk classes, no serious regression in previously strong classes, fresh Pi validation, and end-to-end action validation before replacing E41.

Consequence: The next intervention must be chosen from the AG+ mechanism evidence. The target is reliable accepted actions and safe rejection, not a higher holdout number by itself.

## 2026-09-27 - Phase AH Recommends Controlled Classifier Ablation, Not Immediate Training

Decision: Recommend the next experiment category as a controlled classifier ablation. Do not train E47 yet. Keep confidence calibration separate.

Evidence: Phase AH reconciled the authoritative E41/E46 artifact set and found no internal mismatch. The saved artifacts define six E41-correct -> E46-wrong regressions and three E41-wrong -> E46-correct improvements. Phase AD/AE show live classifier failures in CALL, COLOR, TEMPERATURE, NEXT, and LIGHT_OFF, while Phase AG/AG+ show that broad E46 recovery training produced mixed gains and regressions. STOP_013 is the clearest confidence/acceptance-policy case and should not be mixed into a classifier-only repair.

Consequence: The next phase, if authorized, should specify a narrow ablation question before training: for example, whether target-only data, target+contrast data, or one-pair repair can improve a documented failure without reproducing STOP/NEXT or VOLUME_DOWN/VOLUME_UP accepted-wrong regressions. E41 remains frozen.

## 2026-09-27 - Reject E47 Targeted Classifier Ablation

Decision: Do not promote E47_TARGETED_CLASSIFIER_ABLATION. Do not proceed to fresh live validation for E47. Keep E41 frozen.

Evidence: E47 tested a narrower repair than E46 but degraded frozen holdout performance from E41's 90/95 to 79/95. It produced 11 E41-correct -> E47-wrong regressions, 0 E41-wrong -> E47-correct corrections, and left all five E41 holdout errors unresolved. Under frozen E40, accepted-wrong outcomes increased from 1 to 3: PAUSE -> CALL, STOP -> NEXT, and LIST_REMINDERS -> CREATE_REMINDER. The STOP -> NEXT safety regression reappeared as accepted-wrong.

Consequence: The selected target/contrast fine-tuning recipe is not viable. E47 should remain an experimental artifact only. Any future work must avoid immediate model iteration and should first analyze why narrow fine-tuning is degrading stable classes.

## 2026-09-27 - Phase AJ Selects Controlled Architecture Experiment As Next Design Path

Decision: Do not train E48 yet. Select a controlled architecture experiment as the next evidence-supported experiment category to design and authorize separately. Keep E41 frozen and keep E45/E46/E47 rejected.

Evidence: Phase AJ found that E46 and E47 both preserved the same E41 feature representation and tiny CNN architecture while changing fine-tuning/data mixture, and both degraded frozen holdout performance and accepted-wrong safety behavior. The remaining live failures are primarily wrong top-1 classifications under fresh Pi conditions, while confidence/rejection remains safety-relevant for whether wrong predictions execute. The inspected E41 model is a deliberately tiny Conv2D CNN with global pooling and approximately 66k parameters, using a fixed 4-second 40-bin log-mel representation with no VAD/silence trimming observed.

Consequence: A future candidate should test architecture/capacity as the independent variable while keeping data, preprocessing, labels, E40 policy, thresholds, router/actions, holdout evaluation, and validation exclusions fixed. This does not prove architecture is the root cause and does not authorize training, promotion, threshold changes, or live validation.

## 2026-09-27 - Block E48 Training Until Architecture Is Fully Specified

Decision: Do not train E48_CONTROLLED_TEMPORAL_CNN_CAPACITY_PROBE from the Phase AJ design as written.

Evidence: Phase AK required using the E48 architecture specified in Phase AJ and stopping if AJ did not uniquely specify one architecture. Phase AJ selected the architecture-experiment category but left the concrete architecture open, describing examples such as temporal/asymmetric convolution capacity or one additional convolutional block. That is not a single executable controlled architecture.

Consequence: E48 is inconclusive because it was blocked before training. The next prerequisite is a precise architecture specification with exact layer sequence, kernel sizes, channels, stride, pooling, normalization, activation, temporal handling, final pooling, classifier head, parameter count, and model-size target. E41 remains frozen and no model or production changes were made.

## 2026-09-27 - Pre-Register E48 Temporal Context Architecture

Decision: Approve the E48 architecture specification for a future controlled training phase, but do not train or promote it in Phase AL.

Evidence: Phase AL selected one narrow architecture hypothesis supported by Phase AJ: add temporal context before global pooling while preserving E41's feature pipeline, existing three Conv2D blocks, classifier head, labels, E40 policy, and evaluation protocol. The exact change is one inserted SeparableConv2D block after pool3: 96 filters, 5x3 kernel, stride 1x1, same padding, relu, followed by BatchNorm momentum 0.1. This raises parameter count from 66,483 to 77,619, remaining TinyML/Pi-sized.

Consequence: E48 is fully specified and ready for a separately authorized controlled training run. The training run must use frozen controls and must stop if the recorded E41 training data cannot be reconstructed without substitution. E41 remains frozen and no production changes were made.

## Phase AM Decision - 2026-09-27
- Do not train E48 from the current local project state.
- Reason: Phase AM pre-training data-integrity gate failed. E41 recorded 240 adaptation clips and 120 Pi holdout examples, but the locally reconstructable standard manifests provide only 231 adaptation clips and 95 holdout examples, with unresolved WAV paths in the local extra recovery manifest.
- Decision status: **E48 INCONCLUSIVE — FURTHER EVIDENCE REQUIRED**.
- E41 remains frozen. E40 and all thresholds remain unchanged.
- A future E48 execution would first need the exact E41-authorized training/adaptation/holdout source restored and verified, not substituted.


## 2026-09-27 — Phase AN Dataset Readiness Decision

Decision: Do not authorize E48 controlled training yet.

Rationale: the intended E48 experiment depends on preserving E41 dataset identity as a controlled variable. Phase AN could not reconstruct the full exact E41-authorized 240-adaptation / 120-holdout dataset. The dedicated E41 recovery WAVs/manifests are missing locally, and replacing them with similar or later recordings would create a different experiment.

Status: E48 DATASET NOT READY — PROVENANCE GAP REMAINS.


## 2026-09-27 — Phase AO Recovery Decision

Decision: Do not authorize E48 training from the current local dataset state.

Rationale: Phase AO searched local project storage and available archives for the missing authoritative E41 recovery directory. The missing 50 adaptation and 25 holdout WAVs were not recovered. Same-filename files elsewhere are weak candidates only and cannot be substituted without redefining the experiment.

Status: E41 RECOVERY PARTIAL — REMAINING FILES NOT FOUND.


## 2026-09-27 — Phase AP Reconciliation Decision

Decision: Do not authorize E48 training from the current evidence state.

Rationale: Phase AP could not establish exact artifact-to-Pi WAV identity. Historical E41 references are consistent with the expected missing recovery set, but the current 75-file recovered Pi-side package and SHA256 evidence were unavailable locally, so byte-level identity cannot be proven.


## 2026-09-27 — Phase AP Reconciliation Decision Updated

Decision: Do not train E48 yet.

Rationale: The recovered 75-WAV E41 package substantially closes the provenance gap. The 25 holdout rows are exact artifact-to-dataset matches. The 50 adaptation rows are strongly consistent with E41 but lack a historical per-row training manifest/hash tying them byte-for-byte to the training process. A separate methodology decision is needed before treating this as sufficient for E48.

Recommended next phase: Phase AQ dataset-readiness/methodology decision.


## 2026-09-27 — Phase AQ Methodology Decision

Decision: A future E48 controlled architecture experiment may be authorized in a separate phase, but only as an architecture-only experiment using a frozen reconstructed E41-authorized dataset with an explicit provenance caveat.

Rationale: Phase AP established exact identity for the 25 recovered E41 recovery holdout WAVs and strong consistency for the 50 recovered E41 recovery adaptation WAVs. The adaptation rows still lack byte-identifying historical training hashes, so E48 cannot be described as a perfect replay of E41 training. However, the dataset boundary is now explicit and reproducible enough for a controlled next experiment against frozen E41.

Required boundary: use 240 adaptation clips for future E48 training (190 base + 50 recovered recovery adaptation), exclude all 120 holdout rows (95 current formal + 25 exact recovered original-holdout rows), keep E41/E40 frozen, and make architecture the sole independent variable.

Consequence: The next evidence-supported intervention category is architecture. Do not combine architecture with feature, data, threshold, router/action, or live-validation changes. Do not train until a separate execution phase authorizes it.


## 2026-09-27 — Phase AR E48 Architecture Specification Decision

Decision: Pre-register E48 as a single architecture-only temporal-context probe. Do not train yet.

Evidence: Inspection of actual E41 code/config confirms E41 is a 66,483-parameter `tiny_vcm_cnn` using `[398,40,1]` log-mel input, Conv2D filters 24/48/96, 3x3 kernels, BatchNorm momentum 0.1, MaxPool after each block, avg+max global pooling, Dense 64, and Dense 19 softmax. E45/E46/E47 showed that additional fine-tuning/data interventions can cause cross-class regressions and accepted-wrong safety regressions, while Phase AD/AE/AG+ show remaining problems are primarily top-1 classifier/class-separation failures.

Consequence: If E48 is executed in a later phase, the only architecture change is one SeparableConv2D temporal context block after `pool3`: 96 filters, 5x3 kernel, stride 1x1, same padding, relu, followed by BatchNorm momentum 0.1. E48 has 77,619 parameters. E40, thresholds, preprocessing, dataset boundary, labels, router/actions, and current95 evaluation remain frozen.


## 2026-09-27 — Phase AS E48 Offline Evaluation Decision

Decision: Do not promote E48 in Phase AS. Preserve E41 as frozen. E48 may be considered for a separately authorized fresh live-validation design after review.

Evidence: E48 improved frozen current95 raw accuracy from E41's 90/95 to 91/95 and reduced accepted-wrong outcomes under frozen E40 from 1 to 0. Accepted-action precision improved from 98.75% to 100%. However, E48 reduced accepted-correct coverage from 79 to 72 and introduced three E41-correct -> E48-wrong raw regressions: `LIGHT_OFF -> WEATHER`, `STOP -> NEXT`, and `TEMPERATURE -> NEXT`.

Consequence: E48 passes the narrow offline raw/safety gate but does not justify production promotion. Any next step must be an explicitly authorized review or fresh live-validation phase; do not change E40, thresholds, E41, router/actions, or production configuration.


## 2026-09-27 — Phase AT E48 Regression Diagnosis Decision

Decision: Do not promote or reject E48 yet. Do not run live validation yet. Recommend a separate E48 confidence/rejection calibration diagnostic using existing offline evidence only.

Evidence: Phase AT found that all seven changed current95 cases are top-1 classification changes. E48 corrected four E41 errors and introduced three raw regressions, but all E48 wrong predictions were rejected under frozen E40. E48's zero accepted-wrong result is encouraging, but accepted-correct coverage dropped from 79 to 72 because rejected-correct cases increased to 19.

Consequence: Before live validation or promotion, determine whether E48's reduced accepted-correct coverage is an unavoidable safety tradeoff or a calibratable confidence/rejection issue. Keep E41/E48/E40 frozen and do not change production thresholds during that diagnostic.


## 2026-09-27 — Phase AU E48 Calibration Decision

Decision: Do not change E40 or production thresholds. Do not promote E48 yet. Design a controlled E48-specific threshold calibration experiment using independent calibration evidence.

Evidence: AU what-if analysis showed global threshold lowering is unsafe because it newly accepts `STOP -> NEXT` even at global 0.95. Class-specific E48 policies can recover many rejected-correct cases on current95 without accepted-wrong, including one policy that reaches 90 accepted-correct and 0 accepted-wrong while keeping `NEXT` and `WEATHER` protected.

Consequence: The current95 what-if result is promising but holdout-derived. A separate calibration experiment is required before any threshold change or live validation decision.


## 2026-09-27 — Phase AV Calibration Dataset Decision

Decision: Define an independent E48 confidence calibration dataset before any E48-specific threshold policy is selected.

Evidence: Phase AU showed that threshold candidates discovered on current95 can recover E48 rejected-correct cases, but global lowering creates accepted-wrong risk and the class-specific candidates are holdout-derived. Independent calibration evidence is required before proposing any E48-specific acceptance policy.

Consequence: Phase AV specifies a 210-WAV calibration-only dataset with all 19 labels and extra coverage around `NEXT`, `WEATHER`, `STOP`, `LIGHT_OFF`, `TEMPERATURE`, and `COLOR`. Data collection and integrity verification must pass before threshold analysis. E41/E48/E40 and all production thresholds remain frozen.


## 2026-09-27 — Phase AV Collection Decision

Decision: Accept the Phase AV Raspberry Pi collection as completed calibration evidence, subject to the documented limitation that holdout SHA256 overlap was not available in the Pi-side verifier output.

Evidence: Pi-side verifier reported 210 WAV files, 210 manifest rows, exact class-count match, 0 missing files, 0 duplicate trial IDs, 0 duplicate paths, 0 bad audio, 0 bad format, 0 bad duration, valid labels, correct calibration metadata, frozen holdout path overlap 0, SHA256 manifest generated, and final `PASS True`.

Consequence: The next phase may be an explicitly authorized E48 calibration inference/threshold-policy analysis using this fixed Phase AV dataset. No production threshold change is authorized from collection alone.


## 2026-09-27 — Phase AX Availability Decision

Decision: Do not run or report E48 calibration inference until the Phase AV WAV files and manifest are physically available in the inference environment.

Evidence: The local project contains frozen E48 model artifacts but not `pi_validation/phase_av_e48_independent_calibration_20260927_v1`; local Phase AV WAV count is 0.

Consequence: Phase AX is blocked locally. The verified Phase AV dataset must be copied/pulled into the project before inference can be executed.


## 2026-09-27 — Phase AX Inference Decision

Decision: Do not change E40, thresholds, E48, or production configuration based on Phase AX. Preserve AX as independent calibration inference evidence only.

Evidence: Frozen E48 on the independent Phase AV calibration set produced 88/210 raw correct and, under frozen E40, 38 accepted-correct, 13 accepted-wrong, 50 rejected-correct, and 109 rejected-wrong. Accepted-action precision was 74.51%.

Consequence: The independent calibration evidence shows that E48 plus frozen E40 is not safe enough for production promotion. Any later threshold-policy analysis must be explicitly authorized and must account for the 13 accepted-wrong Phase AV cases. AX itself performed no threshold optimization.


## 2026-09-27 — Phase AY Diagnostic Decision

Decision: Do not proceed directly to threshold tuning, live validation, or another architecture tweak. The next evidence-supported research question should address clean dataset/generalization before any promotion decision.

Evidence: AY showed a large current95-to-AV generalization gap, broad per-class degradation, repeated confusion families, and high-confidence wrong predictions. E48 had 13 accepted-wrong cases on AV, including recurring action-risk pairs. Frozen E41 diagnostic inference had better raw accuracy on AV but far worse accepted-wrong behavior, so neither candidate is suitable for promotion from this evidence.

Consequence: A clean, speaker-diverse, phrase-diverse retraining experiment is justified to design in a future phase. Confidence calibration may be analyzed later, but cannot be the sole repair path because the dominant issue includes wrong top-1 classification and high-confidence wrong predictions.


## 2026-09-27 — Phase AZ Dataset Integration Decision

Decision: The posted `VCM_MASTER`/`VCM_BALANCED` resource may be used only after review in a new controlled training-data intervention; do not train during AZ and do not silently merge it into E41/E48.

Evidence: AZ inspected the local downloaded resource at `C:\Users\Loreen Anne\Downloads\VCM\VCM`. `VCM_MASTER` has 36,622 rows/audio files with train/val/test 27,130/4,734/4,758 and 395 speakers/groups. `VCM_BALANCED` has 15,268 WAV train rows, 298 speakers/groups, and is derived from Dataset A train only. Embedded reports document zero speaker leakage, and AZ found 0 byte-identical SHA256 overlaps between Dataset B audio and 21,757 scoped current-project audio files.

Constraint: The resource has 16 classes, not the current 19 executable labels. `COLOR`, `CREATE_REMINDER`, `LIST_REMINDERS`, `CALL`, and `MESSAGE` are missing, and `BRIGHTNESS` is only partially represented by `LIGHT_DIM`.

Consequence: A future smallest defensible experiment should be pre-registered as a data intervention, likely using `VCM_BALANCED` for covered labels plus original/project training data for missing labels, while preserving Dataset A val/test, current95, Phase AV, and Phase AD evidence as non-training evaluation evidence. No requirement is upgraded from AZ alone.


## 2026-09-27 — Phase AZ-R Actual Dataset 2 Integration Decision

Decision: Dataset 2 is usable after controlled filtering (`B_USABLE_AFTER_CONTROLLED_FILTERING`), but do not train or merge yet.

Evidence: AZ-R verified the actual local files at `data/VCM Dataset2/VCM` against `data/VCM Dataset2 Specifications.pdf`. Dataset A matched the specification exactly for total, train/validation/test counts, class count, speaker count, and missing/corrupt audio. Dataset B matched the specification exactly for 15,268 training files, 13,801 originals, 1,467 augmented rows, and all documented class counts.

Leakage/provenance evidence: Actual manifest checks showed zero train/validation/test speaker intersections, zero Dataset B speaker overlap with Dataset A validation/test, and Dataset B source rows all tracing to Dataset A train. Byte-level checks found zero Dataset2 B overlap with the active project dataset and zero overlap with protected evaluation/live audio checked in AZ-R.

Constraint: Dataset 2 is a 16-class dataset. It lacks `COLOR`, `CREATE_REMINDER`, `LIST_REMINDERS`, `CALL`, and `MESSAGE`; `LIGHT_DIM` supports brightness/dimming utterances but not color. Source-family overlap with the original project dataset cannot be fully excluded from current active metadata because the active index lacks upstream public-dataset original IDs.

Consequence: The next defensible step, if approved, is a pre-registered data-intervention experiment using Dataset2 B for covered labels plus existing/project data for missing labels, while keeping Dataset A val/test, current95, Phase AV, Phase AD, and other final validation evidence out of training.


## 2026-09-28 — Phase BA Hybrid Dataset Training Decision

Decision: Do not promote `E49_BA_HYBRID_DATASET_E41_ARCH` to production or Raspberry Pi deployment from offline evidence.

Evidence: BA used the E41 architecture, frozen E41 initialization, frozen E40 thresholds, the established E41 preprocessing pipeline, and a frozen 11,830-row hybrid training manifest with 0 protected path overlap and 0 protected SHA256 overlap. Phase AV raw accuracy improved to 148/210 = 70.48%, compared with E41's 103/210 and E48's 88/210. Phase AV accepted-action precision improved to 80.95%, compared with E41's 57.14% and E48's 74.51%.

Safety/regression evidence: BA still produced 24 accepted-wrong Phase AV actions, worse than E48's 13 accepted-wrong cases. BA also regressed current95 raw accuracy to 78/95 = 82.11%, compared with E41's 90/95 and E48's 91/95. High-confidence wrong predictions remained present, including 24 wrong Phase AV predictions at confidence >= 0.90.

Consequence: BA demonstrates that the Dataset2 training-data intervention improves independent raw generalization, but it is not safe enough for promotion under frozen E40 and the current action system. Stop after BA. Do not tune thresholds, retrain, deploy to Pi, collect more data, or start a follow-on experiment without explicit authorization.


## 2026-09-28 — Phase BB Diagnostic Decision

Decision: Do not proceed directly to E50, threshold tuning, architecture change, or Pi deployment. If another model experiment is later authorized, the next evidence-supported intervention should be controlled class-preservation/rebalancing with original-data preservation or weighted sampling.

Evidence: BB showed E49's current95 regression was mainly in Dataset2-supported/partial labels, not in the five Dataset2-uncovered labels. Current95 raw-correct deltas were -10 for supported/partial labels and -2 for uncovered labels. Phase AV improved strongly in both groups: +29 for supported/partial labels and +16 for uncovered labels.

Safety evidence: E49 repaired all tracked AY confusion families relative to E48, but still produced 24 accepted-wrong Phase AV actions. Seventeen of those 24 were new accepted-wrong outcomes relative to E41. High-confidence wrong predictions improved versus E41 but worsened versus E48.

Consequence: The strongest interpretation is a real generalization gain with decision-boundary movement/possible forgetting and new unsafe accepted-wrong regions. The next step should preserve the Dataset2 generalization benefit while protecting original-domain boundaries. Phase AV must remain evaluation-only.


## 2026-09-28 — Phase BC Command-Vocabulary Revision Decision

Decision: Adopt `COLOR -> LIGHT_DIM` as a documented future command-vocabulary design revision, with implementation pending.

Evidence: The assignment requires the category `Dim / color lights` and gives `Dim lights to X percent` as its example. The assignment does not prescribe literal classifier labels. Dataset2 directly provides `LIGHT_DIM` and defines it as dimming / reducing brightness of lights. Dataset2 has no `COLOR` class. E49 had only 10 `COLOR` training examples and Phase BB showed `COLOR` remained unsafe.

Implementation caveat: Current router/action code does not yet include a `LIGHT_DIM` raw route. Current `BRIGHTNESS` and proposed `LIGHT_DIM` both map conceptually to brightness adjustment, so the future experiment must define whether they are distinct or should be consolidated before training.

Consequence: Historical E41/E48/E49 results remain unchanged. The next training experiment, if authorized, must treat this as a pre-training vocabulary/specification change and must not silently compare revised-vocabulary results as label-identical to E49.


## 2026-09-28 — Phase BF Functional Audit Decision

Decision: Do not claim the current frozen VCM is demo-ready from BF, and do not start another model-training experiment based on BF alone.

Evidence: BF verified that the packaged Pi predictor defaults to `E33_PI_COLOR_LIGHTON_RESPONSIVENESS`, while project history preserves `E37` + `E41` + `E40` as the main live-evidence stack and E49 as a rejected offline candidate. The current environment is not the Raspberry Pi runtime and lacks `arecord`, `aplay`, microphone, and speaker access, so fresh spoken end-to-end trials could not be run. The inspected wake-gated runner performs a single wake-command-action attempt and exits, and no per-command response WAV bank exists in the packaged music path.

Consequence: The next work should not be blind retraining. If the project wants BF evidence, run the audit on the actual Raspberry Pi with an explicitly selected frozen stack, or first authorize a separate implementation phase for persistent listening and response-WAV playback. Historical benchmark/live evidence remains unchanged, and no requirement is upgraded from BF alone.


## 2026-09-28 — Phase BG Initial Experiment Direction Decision

Decision: Start BG with a data-composition / original-preservation experiment under the revised `LIGHT_DIM` vocabulary, not with threshold tuning or an architecture change.

Evidence: BB showed E49's Dataset2 hybrid training substantially improved independent Phase AV raw accuracy, but also displaced current95 decision boundaries. BC established that future vocabulary can legitimately replace `COLOR` with `LIGHT_DIM`, and Dataset2 directly supports `LIGHT_DIM`. E48's architecture change did not solve independent generalization, so architecture is not the first BG variable.

Consequence: The first BG candidate should retain E41 architecture/preprocessing, exclude protected evaluation data, use Dataset2 train only for supported labels, preserve original training examples more strongly than E49, and evaluate historical data only on compatible labels without relabeling historical `COLOR`.


## 2026-09-28 — Phase BG Final Offline Classifier Decision

Decision: Select `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT` as the best BG offline command-classifier candidate for final review, but do not claim final Pi/demo verification yet.

Evidence: E50 restored much of E49's current95-compatible regression while retaining most of the independent Phase AV-compatible generalization gain. E50 reached 83/90 = 92.22% on current95-compatible rows and 139/194 = 71.65% on Phase AV-compatible rows, with 8 accepted-wrong Phase AV-compatible cases and 91.92% accepted-action precision under frozen E40. E51 had the same Phase AV accepted-wrong count and better broad Dataset2/combined safety, but regressed current95-compatible performance to 77/90 and Phase AV-compatible performance to 131/194.

Integrity: BG used the revised `LIGHT_DIM` vocabulary and did not relabel historical `COLOR` evaluation rows. Protected contamination checks found 0 path overlaps and 0 SHA256 overlaps. No threshold tuning, architecture change, preprocessing change, router/action change, wake-model change, protected-data training, Pi deployment, or live validation occurred.

Consequence: Stop model sweeps unless later Pi/demo evidence identifies a classifier-specific blocker. The next defensible phase is deployment/demo integration: package E50, wire the revised `LIGHT_DIM` runtime path, verify local action/response behavior, and run fresh Raspberry Pi end-to-end validation.


## 2026-09-28 — Phase BH Package Integration Decision

Decision: Use the packaged `E37_TARGETED_COLOR_VOLUME_FIX` wake model plus `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT` command model as the next validation stack.

Evidence: E50 was selected offline in BG, while BF showed the package still defaulted to E33 and lacked the revised `LIGHT_DIM` runtime path. BH copied E37/E50 artifacts into the Pi package, added a frozen E40-compatible E50 policy, added `LIGHT_DIM` routing, and verified local package inference and routing.

Constraint: BH did not run the Raspberry Pi microphone path, did not execute GPIO, did not add response WAVs, and did not prove final demo readiness.

Consequence: The next legitimate step is a controlled Pi-side validation phase using the now-packaged E37+E50 stack. Do not train another model unless Pi evidence shows classifier-specific failures after ruling out capture, routing, action, and package issues.


## 2026-09-28 — Phase BI Live Validation Decision

Decision: Do not claim final all-command demo readiness from BI, but preserve E37+E50 as a materially improved live-validation stack with strong wake behavior and several confirmed end-to-end command passes.

Evidence: BI produced 36/36 wake successes, tested all 19 revised command labels, achieved 15 accepted-correct command actions, 1 accepted-wrong action, 93.75% accepted-action precision, and 1/1 UNKNOWN safe rejection. End-to-end passes were observed for 12 command labels. The accepted-wrong failure was `TEMPERATURE -> WEATHER` at confidence 0.9973, causing a weather action instead of thermostat action.

Integration evidence: `LIGHT_DIM` initially failed due to missing Pi route, then passed after the user patched the Pi router. This shows the revised command can work but also confirms packaging/runtime route consistency matters.

Consequence: The next phase should not blindly train. It should decide between focused remediation of weak commands/integration gaps and a defensible demo plan. Persistent listening and response WAV evidence remain separate implementation gaps.


## 2026-09-28 — Phase BJ Diagnosis-First Targeted Remediation Decision

Decision: Perform targeted weak-command diagnosis before any final all-command demo claim, and do not start another general CNN sweep.

Evidence: BI showed 36/36 wake success, all 19 revised labels tested, 12 labels with at least one end-to-end pass, and 1/1 UNKNOWN safe rejection. However, seven labels lacked an end-to-end pass: `TIME`, `BRIGHTNESS`, `TEMPERATURE`, `VOLUME_UP`, `VOLUME_DOWN`, `CREATE_REMINDER`, and `CALL`. The most important safety failure was `TEMPERATURE -> WEATHER` at confidence `0.997283935546875`, which executed the wrong local action.

Interpretation: The remaining problems are mixed. Some are classifier/policy weaknesses, especially `TEMPERATURE`; some may be phrase/capture-sensitive safe rejections; some are demo-integration gaps such as persistent listening and response feedback. A broad retrain would not address all of these and would risk consuming time without targeting the observed failures.

Consequence: The next evidence-supported action is targeted Pi repeat/phrase validation for the weak labels under the frozen E37+E50+E40-compatible policy. If time is limited, a defensible demo subset can be prepared around commands that passed, but it must be labeled as a subset and cannot be represented as all-command completion. Do not train, lower thresholds, or use BI recordings as training material without a later explicitly scoped phase.


## 2026-09-28 — Phase BK Targeted Weak-Command Repeat Decision

Decision: Prepare a defensible final demo subset rather than running another general CNN sweep. Exclude `TEMPERATURE` from live demo unless a later targeted remediation phase is authorized and validated.

Evidence: BK used the correct frozen E37 wake + E50 command stack and produced 22 weak-command repeat trials. `CREATE_REMINDER` recovered with accepted end-to-end passes for `remind me` and `set reminder`. `TEMPERATURE` produced one accepted correct action, but also two accepted-wrong actions: `set thermostat -> STOP` and `temperature -> WEATHER`. `TIME`, `BRIGHTNESS`, `VOLUME_UP`, `VOLUME_DOWN`, and `CALL` still lacked accepted end-to-end passes.

Interpretation: BK confirms that the remaining problem is not solved by a simple demo phrase choice for all weak commands. `CREATE_REMINDER` can be added to the supported demo subset, but `TEMPERATURE` is actively unsafe and the other weak labels remain incomplete under frozen thresholds.

Consequence: A final demo can be defensible only if it is scoped to commands with live evidence and explicitly documents unsupported/unsafe commands. Threshold tuning is not justified because accepted-wrong actions are already present at high confidence. Any future model work should be targeted remediation, not another broad optimization sweep.


## 2026-09-28 — Phase BL Targeted Remediation Decision

Decision: Reject `E52_BL_TARGETED_WEAK_E50_FINETUNE` and retain E50 as the defensible fallback for final demo preparation.

Evidence: E52 was the only BL training candidate. It kept E50 architecture/preprocessing, used the existing legitimate BG/E50 manifest, started from E50 weights, and applied weak-label sample weights for `TIME`, `BRIGHTNESS`, `TEMPERATURE`, `VOLUME_UP`, `VOLUME_DOWN`, and `CALL`. E52 improved Phase AV-compatible raw accuracy from 139/194 to 150/194, but accepted-wrong actions increased from 8 to 13. BI live replay also worsened from 1 observed E50 accepted-wrong action to 3 E52 replay accepted-wrong actions. BK weak-command replay did not improve accepted-correct performance.

Interpretation: E52 is useful research evidence that weak-label emphasis can move raw boundaries, but it is not safe for action execution. The project objective is a defensible on-device VCM demo, not raw accuracy at the cost of more wrong actions.

Consequence: Do not deploy or promote E52. Prepare a final demo around the 13 labels with live end-to-end evidence, and document `TIME`, `BRIGHTNESS`, `TEMPERATURE`, `VOLUME_UP`, `VOLUME_DOWN`, and `CALL` as limitations unless a future targeted data collection/remediation phase is explicitly authorized.


## 2026-09-28 — Phase BM Final Integration Decision

Decision: Freeze E37+E50 as the final recognition stack and proceed to physical Pi validation with a 13-command demo subset.

Evidence: BM verified the packaged E50 SHA256, label order, final vocabulary, router/action mappings, response WAV inventory, and offline replay behavior using BI/BK WAV evidence. The package runtime now defaults to E50, supports persistent `--cycles`/`--continuous` operation, and includes local response WAV assets.

Interpretation: The system is sufficiently hardened offline for final physical validation, but BM does not itself prove speaker playback, Pi persistent-loop stability, GPIO/PWM, or Pi latency. Those require Pi execution.

Consequence: The next legitimate step is physical Raspberry Pi validation using the BM handoff. Do not run another CNN sweep, train E53, tune thresholds, or deploy E52. Continue excluding the six unsupported/unsafe labels from the final live demo unless new evidence is produced.


## 2026-09-28 — Phase BM Physical Pi Validation Decision

Decision: Treat the final Pi validation as partial demo validation, not full audio end-to-end completion.

Evidence: The copied archive `outputs/e50_bm_final_demo_20260928_evidence.tar.gz` has SHA256 `4695a6d0fb282624499a42d8102ff4bf578022c5a0e15a8368b8ef7fd97079ec`. Parsing its 14 result JSON files showed 13/14 wake successes, 11/13 correct command recognitions across selected demo commands, 9/13 accepted automatic action executions, 14/14 returns to listening, and 1/1 UNKNOWN safe rejection. Response WAV assets existed and were readable for all executed commands, but physical playback failed because `aplay` exited with status 1.

Interpretation: The Pi run supports the E37+E50 wake-recognition-router-action loop for 9 selected demo commands, but it does not verify audible response playback. The playback failure is an audio-output integration issue, not a classifier failure.

Consequence: Do not train or tune thresholds to address the response WAV issue. The next legitimate implementation task is Pi audio-output diagnosis, followed by a small response-playback rerun. Final demo claims must disclose that this run had 0/13 full audio end-to-end successes due to playback failure.


## 2026-09-28 — Phase BM Command Callability Decision

Decision: Preserve the complete 19-command VCM as callable/testable while separately limiting the deliberate final demo to commands with sufficient safety evidence.

Evidence: BM command-status artifacts show all 19 labels remain present in the model vocabulary/label map and have router/action paths. The six unresolved labels are not removed; they are not currently demo-ready. `TEMPERATURE` is callable and implemented but unsafe/not demo-ready because accepted-wrong live actions were observed.

Interpretation: `CALLABLE`, `IMPLEMENTED`, `VERIFIED`, and `DEMO_READY` are separate states. A final demo subset is not a runtime command whitelist.

Consequence: Do not add code that rejects commands merely because they are outside the current demo subset. Keep all 19 commands available for testing and future remediation. Use `PHASE_BM_19_COMMAND_IMPLEMENTATION_CALLABILITY.csv` for complete callability and `PHASE_BM_CURRENT_DEMO_READY_COMMANDS.csv` for the deliberate demo subset.


## 2026-09-28 — Phase BN Offline Runtime Hardening Decision

Decision: Continue with E37+E50 and harden only the runtime/audio validation layer before physical Pi testing.

Evidence: E50 SHA256 matched the frozen expected hash, all 19 final labels remain present, all 19 commands route to executable local action handlers, and response WAV coverage now exists for all 19 commands plus UNKNOWN. The previous Pi failure was response playback (`aplay exited with status 1`), so BN added explicit response-audio device selection and stderr capture without changing the ML stack.

Interpretation: The next blocker is Pi audio output and physical validation, not classifier optimization. Runtime hardening that improves evidence quality and playback-device selection is legitimate; training, threshold tuning, or model replacement is not.

Consequence: Deploy `outputs/e50_bn_runtime_update_20260928.tar.gz`, run the Phase BN audio diagnostics first, then proceed to smoke/all-19 validation only after the audio path is understood. Do not run E53, deploy E52, tune thresholds, or create a demo whitelist.

## 2026-09-28 - Phase BN Prompted Repeated-Cycle Audio Decision

Decision: Treat response audio as verified for a small prompted repeated-cycle smoke set and proceed to all-19 prompted validation, while preserving the distinction between repeated single-cycle evidence and a same-process continuous-loop proof.

Evidence: `outputs/e50_bn_prompted_multicycle_20260928_evidence.tar.gz` has SHA256 `10011b1364b73820a62853e784a7896bd649a10e9bada96656274674ec6be4f4`. Four prompted trials (`ALARM`, `TIMER`, `PAUSE`, `LIST_REMINDERS`) all accepted wake, accepted command, executed the intended action, reported `response_result.played=true` on `plughw:CARD=vc4hdmi1,DEV=0`, returned to listening, and were heard by the operator.

Interpretation: The audio-output blocker from BM is resolved for these selected response tones. Remaining recognition variability should be measured through all-19 validation, not addressed by training or threshold tuning in BN.

Consequence: Run all-19 prompted validation next. Keep all 19 commands callable and testable. Report weak commands as callable/not verified or unsafe/not demo-ready, not as unavailable. Do not add a runtime demo whitelist.

## 2026-09-28 - Phase BN All-19 Validation Decision

Decision: Treat the all-19 prompted Pi validation as a complete callability/testability audit snapshot, not as permission to broaden the final demo without considering prior safety evidence.

Evidence: `outputs/e50_bn_all19_validation_20260928_evidence.tar.gz` has SHA256 `18b7bda8aff4dc9de12568e20626069547f51c03397deffe222ab6fad7115e98`. The run covered all 19 commands plus one UNKNOWN phrase. It produced 10/19 end-to-end audio passes, 0 accepted-wrong command actions, 19/20 wake acceptances, 20/20 returns to listening, and a safe UNKNOWN rejection.

Interpretation: The all-19 vocabulary remains callable/testable. The latest misses were safe failures, not wrong executed actions. However, a command passing once in this run does not erase prior accepted-wrong evidence; `TEMPERATURE` remains unsafe/not demo-ready.

Consequence: Prepare final BN synthesis and demo documentation from accumulated evidence. If more Pi testing is done, it should be targeted repeats of latest safe misses or chosen final-demo commands, not model training, threshold tuning, or another CNN sweep.

## 2026-09-29 - Preserve E50 and Stage Final Deployment Without Further CNN Work

Decision: keep E50 as the frozen final command CNN candidate and continue final deployment staging rather than starting another CNN experiment.

Rationale: the final deployment guide explicitly closes model development unless integration testing proves the frozen CNN is itself a blocking failure. Current blockers are deployment/integration evidence boundaries: touchscreen control, continuous runtime proof, final disconnected Pi demonstration, and performance measurement.

Implementation decision: add a small Tkinter touchscreen controller as a wrapper around the existing E37+E50 runtime. The GUI starts/stops the runtime and displays status from evidence JSON; it does not contain recognition, threshold, router, or action logic.

Promotion/deployment boundary: this is not a claim of complete standalone deployment. Physical touchscreen validation and disconnected offline demo remain required before final standalone status can be claimed.

## 2026-09-29 - Do Not Treat Tone Responses as Final Demo Responses

Decision: classify the existing short response WAVs as placeholder audio-path smoke assets, not final recorded human responses.

Rationale: the final deployment guide requires specific recorded human responses for each command. The current files are too short to be credible human command responses and must not be used as evidence of final recorded-response compliance.

Next decision boundary: after physical recording and playback verification, update response status from BLOCKED to verified or failed based on actual evidence.


## 2026-09-29 - Phase BN-CLOSE Verification Decision

Decision: Do not declare final deployment verified until the remaining Pi-only physical tests are actually run. BN-CLOSE may prepare scripts, audit tables, handoff commands, and a final verification report, but touchscreen, standalone/offline/no-laptop operation, same-process persistence, final human recorded responses, non-primary-speaker validation, and Pi performance measurements remain pending unless backed by physical evidence.

Evidence: Existing BN evidence supports all-19 callability/testing, 10/19 latest all-19 end-to-end audio passes, 0 latest accepted-wrong actions, UNKNOWN safe rejection, GUI implementation in package, and response/audio-path smoke evidence. It does not support claiming physical touchscreen operation, disconnected standalone operation, or final human response compliance.

Consequence: Keep E37/E50/E40 frozen. Run only physical verification and evidence collection next. Do not train, tune thresholds, add a demo whitelist, remove hard commands, or create a final deployment archive until physical BN-CLOSE evidence is complete.

## 2026-09-29 - Phase BN-CLOSE Round1 Audio-Device Decision

Decision: Use `plughw:CARD=vc4hdmi0,DEV=0` rather than `plughw:CARD=vc4hdmi1,DEV=0` for subsequent BN-CLOSE runtime response playback.

Evidence: Round1 same-process 5-cycle runtime passed wake/classification/action/return-to-listening for all five cycles, but each response playback failed on `hdmi1` with ALSA error 524. Direct recheck showed both `hdmi0` and `default` played `responses/timer.wav`, and the operator heard the timer response twice.

Consequence: This is a response playback device-selection issue. Do not train, tune thresholds, or modify E37/E50/E40. Rerun response/persistent tests with `RESPONSE_AUDIO_DEVICE=plughw:CARD=vc4hdmi0,DEV=0`.

## 2026-09-29 - Phase BN-CLOSE Round2 hdmi0 Playback Decision

Decision: Treat `plughw:CARD=vc4hdmi0,DEV=0` as the current working BN-CLOSE response playback device for the Pi.

Evidence: The pasted Round2 Pi transcript for `OUT=pi_validation/e50_bn_close_20260929_round2` shows a same-process 5-cycle loop with 5/5 wake accepts, 5/5 command accepts/executions, 5/5 `response_result.played=true`, and 5/5 returns to listening. Commands were `PLAY_MUSIC`, `TIMER`, `ALARM`, `PAUSE`, and `LIST_REMINDERS`. The operator reported hearing all available response playback first, and then correct answers to all command cycles.

Consequence: The Round1 response failure is resolved for the tested loop when using hdmi0. Preserve the Round2 Pi evidence directory as a tarball before making final claims from source WAV/JSON/CSV files. Remaining BN-CLOSE work is physical evidence collection, not model training or threshold tuning.

## 2026-09-29 - Phase BN-CLOSE Response Volume Boost Decision

Decision: Preserve the original response WAV files and use new boosted response filenames for deployment playback.

Evidence: All 20 response assets, including UNKNOWN/rejection feedback, were peak-normalized from original peak 8191 to boosted peak 32767 and written under `responses_boosted/` with `_boosted.wav` filenames. Originals were copied to `responses_original_pre_boost_20260929/`. The active `configs/demo_response_assets.json` response map now points to the boosted filenames. `PHASE_BN_CLOSE_RESPONSE_BOOST_MANIFEST_20260929.csv` records source paths, backup paths, boosted paths, gain factors, peaks, and SHA256 values.

Consequence: Runtime response playback should use the louder assets after deploying the boosted-response package. This change is limited to response audio assets and the response map; it does not change E37/E50/E40, thresholds, preprocessing, routing, actions, GPIO behavior, or command callability. If the boosted files sound distorted on the Pi, revert the response map to `responses/*.wav` or restore from `responses_original_pre_boost_20260929/`.

## 2026-09-29 - Phase BN-CLOSE Extra-Loud Pi Response Decision

Decision: Use the Pi-generated `responses_extra_loud_20260929/*_extra_loud.wav` files as the active deployment response set.

Evidence: The initial Windows-side boosted package was not acceptable on the Pi. The working Pi response WAVs were then boosted on-device into `responses_extra_loud_20260929/`; all 19 command labels plus UNKNOWN were verified to map to existing extra-loud files; archive `outputs/e50_bn_close_extra_loud_responses_20260929.tar.gz` was preserved with SHA256 `9ce3be48ee05738305a189a15eb0e1de4c126767084138266f11cdb32d1f1128`; the operator reported the extra-loud responses were perfect.

Consequence: Treat `responses_boosted/` and `outputs/e50_bn_close_boosted_responses_20260929.tar.gz` as rejected/obsolete for deployment playback. Continue using the extra-loud Pi-generated response map unless later physical playback evidence shows a problem.

## 2026-09-29 - Phase BN-CLOSE Wait-for-Wake Interaction Decision

Decision: Add an explicit wait-for-wake runtime mode for the final demo interaction.

Evidence: The fixed-cycle persistent loop returns to a new 4-second wake window immediately after a response. If the operator pauses, that wake window can expire before the next `hey pi`, causing a rejection or consuming a cycle. This is an interaction timing problem, not a classifier or threshold problem.

Consequence: Use `--wait-for-wake` for kiosk-style demo operation. The runtime will keep recording wake windows until `WAKE` is accepted, then open the command window. This preserves the frozen E37/E50/E40 stack and changes only the wake-listening control flow.

## 2026-09-29 - Phase BN-CLOSE Touchscreen GUI Validation Decision

Decision: Validate the touchscreen GUI as a controller for the wake-wait runtime, not as a separate recognition path.

Evidence: Wake-wait mode is physically verified, and the GUI is a Tkinter wrapper around `pi_wake_voice_control_demo.py`. The correct validation is therefore whether touchscreen START launches the wake-wait runtime, touchscreen STOP terminates it, status updates reflect evidence JSON, and responses play through the accepted HDMI0/extra-loud response path.

Consequence: The GUI now launches the frozen E37+E50 runtime with `--wait-for-wake` by default. Physical GUI validation must be collected from the Pi touchscreen and archived separately. No model, threshold, router, action, GPIO, or command-vocabulary changes are authorized.

## 2026-09-29 - Phase BN-CLOSE Touchscreen GUI Status Wording Decision

Decision: Treat command rejection and wake-gate rejection as safe return-to-listening states in the GUI display.

Evidence: During physical GUI validation, a rejected command left the touchscreen showing `COMMAND REJECTED`, which made the system appear stopped even when the intended wake-wait behavior is to continue listening for the next wake phrase.

Consequence: The GUI should display `TELL ME WHAT YOU NEED` only after wake acceptance and should display `STILL LISTENING` after a wake miss or safely rejected command. This is a display/readability decision only and does not change recognition, thresholds, routing, actions, or safety behavior.

## 2026-09-30 - Section 68 Post-Audit Validation Decision

Decision: Promote Section 68 Items 10, 11, 12, and 14 to VERIFIED based on the controlled Pi evidence collected after the read-only hard-stop audit; keep Item 15 at PARTIALLY VERIFIED.

Evidence:

- Item 10 duplicate runtime archive SHA256 `712b36c7d8b54af7dc551f65a43199a4c5d909d04daa428aa589e28d8ba9bfe8`.
- Item 11 network-off standalone archive SHA256 `215f33cbe05a40b5fdb285fe77e1d91a122d3fa494fd5593c5684fa1b59d561a`.
- Item 12 safety sweep archive SHA256 `1523324c4a60ac4c2545a7220ecb38f125b4c9729a8ae75225332a6ca639ce89`.
- Item 14 non-primary-speaker archive SHA256 `360603516a3e7d4ea5747a5e7f08988c3655c1d17fee72a77edcc9446c73f5e3`.
- Item 15 performance archive SHA256 `7300b975256ddd2278ed9253aa2c4e8d439b4beca221cf23ef875fa929e93f91`.

Interpretation:

- Duplicate runtime, standalone offline operation, safety handling, and non-primary-speaker Pi operation now have direct physical evidence.
- Pi performance has direct measurements for model load, saved-WAV inference latency, CPU, RAM, temperature, and loop/resource observations, but not the full fine-grained live timing breakdown originally requested.

Consequence:

- Proceed next to Item 16 final benchmark designation.
- Do not reopen CNN optimization, training, threshold tuning, router semantics, response mapping, GUI behavior, or command-vocabulary decisions.
- Treat Item 15 as partially measured unless the project owner explicitly authorizes additional instrumentation.

## 2026-09-30 - Section 68 Item 16 Benchmark Designation Decision

Decision: designate the all-19 physical Pi validation as the primary final E50 live benchmark population, with later Section 68 Items 10-15 evidence used as supporting integration context.

Evidence: Item 16 evidence archive `outputs/e50_bn_close_item16_final_benchmark_20260930_105703_evidence.tar.gz`, SHA256 `b6a2d9e66f42a1d6b4eb118f9e02505361072582e29b50add9761b1d359b5da1`.

Interpretation: the final benchmark is not a demo-subset benchmark and not an offline classifier-only benchmark. It records all 19 command labels plus one UNKNOWN/no-action trial, separates wake, raw classification, acceptance, accepted-correct, accepted-wrong, safe rejection, end-to-end action success, UNKNOWN safety, and return-to-listening metrics.

Consequence: Item 16 is VERIFIED. Proceed next only to Item 19 final frozen hash manifest. Do not train, tune thresholds, alter router/GUI/runtime/response assets, or broaden the demo set from this benchmark.

## 2026-09-30 - Final Evidence Audit Decision

Decision: use conservative provenance language for user-voice claims and mark the final professor package READY WITH DOCUMENTED LIMITATIONS, not "perfect" or "fully complete."

Evidence:

- The final E50/BG training manifest has 16,100 rows: 13,070 active-project training rows, 2,800 Dataset2 training rows, and 230 E41 reconstructed adaptation rows.
- The final training manifest has 0 matches for `PHASE_AF`, `targeted_live`, or `recovery_training`.
- Phase AF did collect 105 targeted recovery recordings during development.
- Final BG/E50 contamination checks reported 0 protected path overlaps and 0 protected SHA256 overlaps.
- Older Pi adaptation/recovery rows are present in training, and their speaker identity cannot be established from filenames alone.
- User speech was used in live physical Pi validation of the frozen system.

Interpretation:

- Do not claim "100% guaranteed no user voice anywhere in the final training lineage."
- It is supported to say that the identified Phase AF targeted recovery clips are not present in the final E50/BG training manifest.
- It is confirmed that user speech was part of live Pi validation evidence.
- It is indeterminate whether every older Pi adaptation/recovery row is non-user speech.

Consequence:

- Final user-voice provenance classification is INDETERMINATE for absolute exclusion and SUPPORTED for Phase AF non-inclusion in final E50/BG training.
- Preserve documented limitations rather than closing them cosmetically.
- Do not modify E50, E37, E40, thresholds, router, runtime, GUI behavior, response assets, microphone/audio configuration, command vocabulary, or E53.
- This decision was logged in the main project only; the GitHub package was not touched by the logging pass.

## 2026-09-30 - Preserve Frozen E50 Despite Post-Checkpoint Overfitting Evidence

Decision: do not reopen E50 training based on the newly documented post-checkpoint overfitting pattern.

Evidence:

- The retained E50 training history records epoch 7 as the best internal validation-loss point.
- Epoch 7 was the selected E50 checkpoint under the Phase BG internal-validation-loss selection rule.
- Continued training after epoch 7 shows classical training/validation divergence: training loss continues downward and training accuracy continues upward, while validation loss worsens and validation accuracy does not meaningfully improve.
- The later overfit checkpoints were not deployed.

Reasoning:

1. The obvious checkpoint-selection remedy was already applied: the final checkpoint corresponds to the best internal validation-loss point.
2. The observed overfitting occurs after the selected checkpoint, not as evidence that a later checkpoint was deployed.
3. Existing alternative experiments did not establish a safely superior replacement for the final frozen E50 stack.
4. Reopening training immediately before final delivery would create a new uncontrolled experimental branch and risk tuning against evaluation evidence.
5. No evidence currently justifies reopening the frozen final model within the remaining project scope.

Consequence: preserve frozen E50 and document the training-dynamics limitation honestly. Do not claim retraining could never improve E50; the narrower decision is that no controlled evidence currently justifies replacing the frozen delivery model.

## 2026-09-30 - Do Not Use Overfitting As A Catch-All Failure Explanation

Decision: the project will attribute E50 failures to the most specific evidence-supported failure layer available.

Reasoning: post-epoch-7 overfitting is a demonstrated training-dynamics limitation, but the final E50 checkpoint was selected at epoch 7 and later overfit epochs were not deployed. Individual command failures can arise from classifier confusion, limited data coverage, live-domain shift, speaker/acoustic variation, E40 confidence rejection, or downstream router/action/output behavior. These categories are not interchangeable.

Consequence: command failures should not be attributed to overfitting unless direct evidence supports that attribution. Safe rejections should be documented as confidence/guardrail behavior; high-confidence wrong labels as classifier confusion; correct accepted labels with downstream problems as router/action/output issues where evidenced.
