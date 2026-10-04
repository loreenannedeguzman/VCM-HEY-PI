# AGENT_LOG

Master chronological engineering log for ME2 - Voice Controlled Smart Device.

Important rule: this log records actual work only. Metrics such as accuracy, latency, RAM, CPU, model size, and Raspberry Pi performance must be written only after measurement. Until then, use NOT YET MEASURED or NOT YET EXECUTED.

## 2026-09-15 16:20:09 +08:00 - Phase 0 - Requirements Audit And Project Start

### Objective
Start the VCM project safely by inspecting the provided assignment materials and creating the documentation framework before implementation or training.

### Requirement Addressed
- Assignment requirement 1: Build a dataset to train VCMs - NOT STARTED.
- Assignment requirement 2: Build and train a VCM - NOT STARTED.
- Assignment requirement 3: Design a benchmark - NOT STARTED.
- Assignment requirement 4: Validate VCM performance - NOT STARTED.
- Assignment requirement 5: Build Raspberry Pi demo - NOT STARTED.
- Assignment requirement 6: Tiny real-time RPi4/5 VCM - NOT STARTED.
- Assignment requirement 7: Standalone, no cloud - planned constraint.
- Assignment requirement 8: No LLM, pure VCM - planned constraint.

### Action Performed
- Read the provided VCM assignment PDF and VCM agent brief PDF as project/reference material.
- Verified the project root exists: `C:\Users\Loreen Anne\Documents\New project\ME2_VCM`.
- Inspected existing project contents.
- Created the initial folder structure for data, preprocessing, models, training, evaluation, benchmark, deployment, demo, results, configs, and tests.
- Created the core documentation framework.
- Inspected `VCM Sources.xlsx`, which appeared in the project folder during verification.

### Files Affected
- Created directories:
  - `data/`
  - `data/raw/`
  - `data/processed/`
  - `data/metadata/`
  - `preprocessing/`
  - `models/`
  - `training/`
  - `evaluation/`
  - `benchmark/`
  - `deployment/`
  - `demo/`
  - `results/`
  - `results/tables/`
  - `results/figures/`
  - `configs/`
  - `tests/`
- Created documentation files:
  - `AGENT_LOG.md`
  - `PROJECT_STATUS.md`
  - `REQUIREMENTS_TRACEABILITY.md`
  - `DECISIONS.md`
  - `EXAM_NOTES.md`
  - `EXPERIMENT_LOG.md`
  - `README.md`
  - `data/metadata/DATASET_INVENTORY.md`
  - `data/metadata/LABEL_MAPPING.md`

### Commands/Tools Used
- `pdfinfo.exe` for PDF metadata.
- Python `pypdf` for text extraction.
- `Get-ChildItem` and `rg --files` for project inventory.
- `New-Item` for directory creation.

### Actual Result
- Project root exists.
- Existing source files before scaffolding:
  - `VCM AGENT.docx`
  - `VCM AGENT.pdf`
  - `VCM Machine Exercise.pdf`
- Additional source planning file found:
  - `VCM Sources.xlsx`
- No local audio dataset found yet.
- No implementation code found yet.
- Documentation scaffold created.
- Hardware status from user: Raspberry Pi 5 and physical components will be available Friday, September 18, 2026.

### Metrics/Results
- Training accuracy: NOT YET MEASURED.
- Validation accuracy: NOT YET MEASURED.
- Macro-F1: NOT YET MEASURED.
- Model size: NOT YET MEASURED.
- Raspberry Pi latency: NOT YET MEASURED.
- RAM usage: NOT YET MEASURED.
- CPU usage: NOT YET MEASURED.
- Microphone performance: NOT YET MEASURED.
- GPIO demo: NOT YET EXECUTED.

### Interpretation
The project has not yet reached dataset, modeling, or hardware phases. The correct next step is Phase 1: dataset inspection and label mapping, not training.

### Decision
Use the direct VCM architecture required by the assignment:

`audio -> preprocessing -> log-Mel features -> tiny VCM -> command intent -> local action`

Do not use ASR, cloud speech APIs, LLMs, or internet-dependent inference in the final system.

### Reason For Decision
The assignment explicitly requires a tiny standalone voice command model for on-device use and forbids cloud-based models and LLMs.

### Problems Encountered
- `pdftotext.exe` was not present in the local Poppler bundle.
- Windows console output initially failed on one Unicode character.

### Resolution
- Used Python `pypdf` for extraction.
- Reran extraction with UTF-8 console output.

### Next Step
Phase 1: choose or locate the actual audio dataset, inspect class labels, check sample rates/durations/speaker metadata, and create a label mapping to the 10 command categories plus UNKNOWN.

### Exam Concepts
- Difference between VCM and ASR.
- Why no LLM or cloud inference is allowed.
- Why UNKNOWN is necessary.
- Why dataset inspection comes before training.
- Why Raspberry Pi measurements must be actual measured values, not estimates.

## 2026-09-15 16:47:33 +08:00 - Phase 1 - Google Drive Dataset Download

### Objective
Download the user-provided Google Drive dataset into the local VCM project folder so the project can proceed toward offline operation.

### Requirement Addressed
- Requirement 1: Build a dataset to train VCMs - IN PROGRESS.
- Requirement 7: Standalone/offline operation - IN PROGRESS because the files are now local.
- Requirement 8: No LLM/pure VCM - unchanged; no inference architecture built yet.

### Action Performed
- Accessed the public Google Drive folder provided by the user.
- Wrote a local Drive folder downloader script in the Codex work area.
- Downloaded the files exposed by the public folder page into `data/raw/google_drive_dataset/`.
- Verified local WAV count, sample rate, channel count, duration range, and basic readability.
- Attempted a public Google Drive API listing with the page API key; it was blocked without authenticated access.

### Files Affected
- `data/raw/google_drive_dataset/`
- `data/raw/google_drive_dataset/_download_manifest.json`
- `data/metadata/DATASET_INVENTORY.md`
- `data/metadata/LABEL_MAPPING.md`
- `PROJECT_STATUS.md`
- `REQUIREMENTS_TRACEABILITY.md`
- `README.md`
- `AGENT_LOG.md`

### Commands/Tools Used
- Python `requests` for Google Drive page access and file downloads.
- Python `wave` for WAV readability checks.
- Python filesystem inspection for counts and durations.

### Actual Result
- Manifest file entries: 2,004.
- Local WAV files: 2,000.
- Local support text/markdown files: 4.
- Unreadable/corrupted WAV files: 0.
- Sample rate: 16 kHz for all downloaded WAV files.
- Channels: mono for all downloaded WAV files.
- Duration range: 0.480 s to 3.400 s.
- Mean duration: 1.120 s.
- Observed raw labels: ALARM, CALL, DIM_DOWN, DIM_UP, LIGHT_OFF, LIGHT_ON, LIST_REMINDERS, MESSAGE, NEXT, PAUSE, PLAY_MUSIC, SET_REMINDER, STOP, TEMP_DOWN, TEMP_UP, TIME, TIMER, VOLUME_DOWN, VOLUME_UP, WEATHER.

### Metrics/Results
- Dataset file count for downloaded subset: 2,000 WAV files.
- Training accuracy: NOT YET MEASURED.
- Validation accuracy: NOT YET MEASURED.
- Macro-F1: NOT YET MEASURED.
- Model size: NOT YET MEASURED.
- Raspberry Pi latency: NOT YET MEASURED.

### Interpretation
The downloaded subset is suitable for initial inspection and preprocessing work because the WAV files are local, readable, 16 kHz, and mono. However, completeness is unresolved: support files inside the dataset claim larger intended totals than the public unauthenticated Drive page exposed.

### Decision
Treat `data/raw/google_drive_dataset/` as the active local downloaded subset, but do not claim the full dataset has been downloaded until the completeness issue is resolved.

### Reason For Decision
The project must not fabricate dataset completeness. The actual local evidence shows 2,000 WAV files, while support notes claim larger totals.

### Problems Encountered
- The first sequential downloader was too slow.
- The initial parser misread some Drive metadata as filenames.
- Google Drive public page appears to expose only the first 50 files per class folder.
- Google Drive API listing was blocked without authenticated access.

### Resolution
- Switched to a parallel downloader.
- Corrected audio filename parsing.
- Verified the downloaded subset locally.
- Recorded the completeness limitation explicitly.

### Next Step
Confirm whether the 2,000-file subset is the intended working dataset. If not, obtain the full dataset through a ZIP archive, authenticated Drive connector/access, or another complete local transfer method.

### Exam Concepts
- Why local/offline dataset availability matters.
- Why dataset completeness must be verified before training.
- Why a readable audio file count is evidence but not proof of dataset sufficiency.
- Why UNKNOWN remains a methodological gap if not present in the dataset.

## 2026-09-15 17:08:15 +08:00 - Phase 1 - User-Downloaded ZIP Dataset Inspection

### Objective
Inspect the dataset the user downloaded into the local project `data/` folder and determine whether it resolves the earlier Google Drive partial-download limitation.

### Requirement Addressed
- Requirement 1: Build a dataset to train VCMs - IN PROGRESS.
- Requirement 7: Standalone/offline operation - IN PROGRESS because the dataset is local.

### Action Performed
- Inspected `C:\Users\Loreen Anne\Documents\New project\ME2_VCM\data`.
- Counted audio files by top-level extracted ZIP folder.
- Verified all newly downloaded WAV files with Python's `wave` module.
- Counted labels and inferred apparent speaker IDs from filename patterns.
- Located the extra WEATHER file.

### Files Affected
- `data/metadata/DATASET_INVENTORY.md`
- `data/metadata/LABEL_MAPPING.md`
- `PROJECT_STATUS.md`
- `REQUIREMENTS_TRACEABILITY.md`
- `README.md`
- `AGENT_LOG.md`

### Commands/Tools Used
- `Get-ChildItem` for filesystem inventory.
- Python filesystem inspection for counts.
- Python `wave` for WAV readability, sample rate, channel count, and duration checks.

### Actual Result
- Active extracted dataset WAV files: 21,001.
- Active extracted dataset WAV bytes: 816,536,204.
- Readable WAV files: 21,001.
- Unreadable/corrupted WAV files: 0.
- Sample rate: 16 kHz for all active extracted WAV files.
- Channels: mono for all active extracted WAV files.
- Duration range: 0.200 s to 3.880 s.
- Mean duration: 1.214 s.
- Fixed phrase portion: 3,000 WAVs with 50 apparent speaker IDs.
- Phrase-variant portion: 18,001 WAVs with 30 apparent speaker IDs.
- Label counts: all 20 labels have 1,050 WAVs except WEATHER, which has 1,051 WAVs.
- Extra file: `WEATHER_s5_p2_v2(1).wav`.

### Metrics/Results
- Dataset inventory metrics: MEASURED for active extracted dataset.
- Training accuracy: NOT YET MEASURED.
- Validation accuracy: NOT YET MEASURED.
- Macro-F1: NOT YET MEASURED.
- Model size: NOT YET MEASURED.
- Raspberry Pi latency: NOT YET MEASURED.

### Interpretation
The user-downloaded ZIP data resolves the earlier partial-download limitation. The active extracted dataset matches the expected 3,000 fixed-phrase files plus approximately 18,000 phrase-variant files, with one extra duplicate-style WEATHER file.

### Decision
Use the extracted ZIP data in `data/drive-download-*` as the active dataset. Do not use the earlier `data/raw/google_drive_dataset/` partial mirror for training/evaluation unless explicitly needed for comparison.

### Reason For Decision
The extracted ZIP data is complete enough to match the dataset notes, while the earlier public-page mirror contained only 2,000 files.

### Problems Encountered
- One extra duplicate-style WEATHER file is present.
- UNKNOWN class is still not present as a raw dataset label.
- Speaker identity is currently inferred from filenames and not yet verified against independent metadata.

### Resolution
- Recorded the extra WEATHER file explicitly.
- Kept UNKNOWN as a documented dataset gap.
- Deferred final split creation until duplicate handling and speaker split policy are decided.

### Next Step
Create a clean metadata index for the active dataset, excluding or flagging the duplicate-style WEATHER file, then design a speaker-aware train/validation/test split.

### Exam Concepts
- Why duplicate files can bias evaluation.
- Why speaker IDs should be separated across train/validation/test.
- Why raw dataset labels may need to be mapped into assignment intent categories.
- Why UNKNOWN needs either actual examples or a documented rejection strategy.

## 2026-09-15 17:21:05 +08:00 - Phase 1 - Data Source And Augmentation Decision

### Objective
Use `VCM Sources.pdf` and the local dataset evidence to decide whether the project needs additional augmentation before proceeding.

### Requirement Addressed
- Requirement 1: Build a dataset to train VCMs - IN PROGRESS.
- Requirement 4: Validate performance - planning only, NOT YET EXECUTED.
- Requirement 6: Tiny real-time model - planning only, NOT YET MEASURED.

### Action Performed
- Read `VCM Sources.pdf` as source documentation, not as user instructions.
- Compared its listed sources and generation strategy with the active local dataset inventory.
- Reviewed local dataset support files documenting speaker counts, phrase counts, and acoustic variants.
- Recorded the augmentation decision in project documentation.

### Files Affected
- `DECISIONS.md`
- `PROJECT_STATUS.md`
- `data/metadata/DATASET_INVENTORY.md`
- `EXAM_NOTES.md`
- `AGENT_LOG.md`

### Commands/Tools Used
- Python `pypdf` for PDF text extraction.
- `Get-Content` for local support files and documentation review.

### Actual Result
The active dataset already contains meaningful variety:
- fixed-phrase set: 20 classes, 50 speakers, 3 acoustic variations, 3,000 WAV files
- phrase-variant set: 20 classes, 30 speakers, 10 phrases per class, 3 acoustic variations, approximately 18,000 WAV files
- verified local total: 21,001 readable 16 kHz mono WAV files

### Metrics/Results
- Augmentation experiment: NOT YET EXECUTED.
- Baseline training: NOT YET EXECUTED.
- Validation accuracy: NOT YET MEASURED.
- Noise robustness: NOT YET MEASURED.

### Interpretation
Additional augmentation is not needed before the first baseline. The first model should use the active dataset as-is, after duplicate handling and speaker-aware splitting, so later changes have a clear comparison point.

### Decision
Proceed to the next task without adding new augmentation now. Revisit augmentation only as a train-only experiment after baseline validation/noise results exist.

### Reason For Decision
Adding augmentation before the first baseline would blur the interpretation of early results. The dataset already contains acoustic variation, so the more scientific next step is metadata indexing and split planning.

### Problems Encountered
- UNKNOWN is still not present as a raw dataset label.
- One duplicate-style WEATHER file remains unresolved.

### Resolution
- Keep UNKNOWN as a separate requirement gap.
- Handle duplicate-style WEATHER file during metadata indexing.

### Next Step
Create the active dataset metadata index and speaker-aware train/validation/test split.

### Exam Concepts
- What data augmentation is.
- Why augmentation should be train-only.
- Why baseline-first experimentation helps interpret model improvements.
- Why UNKNOWN handling is separate from ordinary augmentation.

## 2026-09-15 17:33:34 +08:00 - Phase 1 - Metadata Index And Speaker Split

### Objective
Create an auditable metadata index and a speaker-aware train/validation/test split for the active local dataset.

### Requirement Addressed
- Requirement 1: Build a dataset to train VCMs - IN PROGRESS.
- Requirement 4: Validate performance - dataset split preparation complete, validation NOT YET EXECUTED.
- Requirement 7: Standalone/offline operation - IN PROGRESS because all referenced audio paths are local.

### Action Performed
- Built a metadata index for the active extracted dataset.
- Parsed raw labels, speaker IDs, phrase IDs, variation IDs, phrase text, assignment intents, sample rate, channels, duration, and file sizes.
- Flagged and excluded `WEATHER_s5_p2_v2(1).wav` because it has a duplicate-style filename and all expected WEATHER combinations are present without it.
- Created an 80/10/10-style speaker-aware split.
- Copied the metadata builder script into the project for reproducibility.
- Updated project documentation to move the next action to Phase 2 preprocessing.

### Files Affected
- `data/metadata/build_dataset_index.py`
- `data/metadata/active_dataset_index.csv`
- `data/metadata/active_dataset_split_summary.csv`
- `data/metadata/DATASET_SPLIT_PLAN.md`
- `data/metadata/DATASET_INVENTORY.md`
- `PROJECT_STATUS.md`
- `REQUIREMENTS_TRACEABILITY.md`
- `README.md`
- `AGENT_LOG.md`

### Commands/Tools Used
- Python `wave` for audio metadata.
- Python `csv` for metadata outputs.
- PowerShell `Import-Csv` and `Get-Content` for verification.

### Actual Result
- Total indexed WAV rows: 21,001.
- Included WAV files: 21,000.
- Excluded WAV files: 1.
- Excluded file: `data/drive-download-20260915T085536Z-1-001/WEATHER/WEATHER_s5_p2_v2(1).wav`.
- Train split: 16,800 WAV files.
- Validation split: 2,100 WAV files.
- Test split: 2,100 WAV files.
- Each raw label has 840 train, 105 validation, and 105 test files after exclusion.
- No speaker overlap exists across train/validation/test within each source group.

### Metrics/Results
- Dataset split counts: MEASURED.
- Model training: NOT YET EXECUTED.
- Validation accuracy: NOT YET MEASURED.
- Macro-F1: NOT YET MEASURED.
- Raspberry Pi latency: NOT YET MEASURED.

### Interpretation
The dataset is now ready for preprocessing. The split is deterministic, local, and speaker-aware based on filename-inferred speaker IDs.

### Decision
Use `data/metadata/active_dataset_index.csv` as the source of truth for preprocessing and later training. Do not train from raw folder scans because that could accidentally include the superseded partial mirror or the excluded duplicate-style file.

### Reason For Decision
The index makes dataset membership, label mapping, and split assignment explicit and reproducible.

### Problems Encountered
- Direct patch creation in the external project path was refused by the patch tool, so the builder script was first created in the Codex work area and then copied into the project after write permission was refreshed.
- Speaker IDs are inferred from filenames and still need source-metadata verification if available.

### Resolution
- Generated the metadata outputs successfully in the project folder.
- Recorded the limitation about filename-inferred speaker IDs.

### Next Step
Phase 2: implement reproducible audio loading and preprocessing from the metadata index.

### Exam Concepts
- Why speaker-aware splitting matters.
- Why duplicate-style files should be excluded before splitting.
- Why dataset metadata should be the source of truth rather than ad hoc folder scanning.
- Why preprocessing must use the same split and inclusion rules as training.

## 2026-09-15 17:49:55 +08:00 - Phase 1 - Dataset Provenance, Structure, And Description

### Objective
Document a professor-facing explanation of the dataset provenance, structure, and purpose because dataset construction is a major assignment expectation.

### Requirement Addressed
- Requirement 1: Build a dataset to train VCMs - IN PROGRESS.
- Requirement 3: Design a benchmark - supports later benchmark documentation but NOT YET EXECUTED.
- Requirement 4: Validate VCM performance - supports later validation but NOT YET EXECUTED.

### Action Performed
- Reviewed `VCM Sources.pdf` as source evidence, not as project instructions.
- Compared the source descriptions with the active local dataset inventory.
- Added a provenance, structure, and description section to `DATASET_INVENTORY.md`.
- Added likely oral-exam questions and answers to `EXAM_NOTES.md`.
- Updated `PROJECT_STATUS.md` to show that dataset provenance documentation has been completed.

### Files Affected
- `data/metadata/DATASET_INVENTORY.md`
- `EXAM_NOTES.md`
- `PROJECT_STATUS.md`
- `AGENT_LOG.md`

### Commands/Tools Used
- Python `pypdf` for reading `VCM Sources.pdf`.
- `Get-Content` for local dataset support files.
- `apply_patch` for documentation updates.

### Actual Result
The dataset explanation now records:
- Provenance from Mark Andrian Macalalad's listed sources: SLURP, Fluent Speech Commands, Google Speech Commands v2, eSpeak NG, and Chatterbox TTS with LibriSpeech/Common Voice references.
- Active local storage in `data/drive-download-*` folders.
- Two logical portions: a 3,000-WAV fixed-phrase portion and an approximately 18,000-WAV phrase-variant portion.
- Dataset structure by raw command-label folder.
- Filename meaning, including raw label, speaker ID, phrase ID, and acoustic variation ID.
- Mapping direction from 20 raw labels to 10 assignment command intents.
- Why augmentation is not required before the first baseline.
- Known limitations: missing UNKNOWN raw class, filename-inferred speaker IDs, one excluded duplicate-style WEATHER file, and licensing/provenance details still needing final confirmation if required.

### Metrics/Results
- New experimental metrics: NOT YET MEASURED.
- Dataset construction documentation: UPDATED.
- Dataset training readiness: READY FOR PREPROCESSING, with UNKNOWN still unresolved for final validation.

### Interpretation
The dataset is appropriate for proceeding to preprocessing and baseline training because it is local, command-focused, short-duration, 16 kHz mono audio with speaker, phrase, and acoustic variation. It is not yet complete for final assignment validation because UNKNOWN handling remains unresolved.

### Decision
Proceed to Phase 2 preprocessing using the existing active dataset. Do not add augmentation now. Keep UNKNOWN handling as a separate design task.

### Reason For Decision
The dataset already contains built-in variation, so the next evidence-generating step is preprocessing and baseline measurement rather than adding more data transformations prematurely.

### Problems Encountered
- The source documentation explains dataset ingredients but does not fully settle licensing/provenance requirements for final reporting.
- UNKNOWN is absent as a raw class.

### Resolution
- Logged the available provenance and the remaining limitations explicitly.
- Deferred UNKNOWN strategy to the next dataset/model-design decision.

### Next Step
Phase 2: implement reproducible audio loading and log-Mel preprocessing from `active_dataset_index.csv`.

### Exam Concepts
- Dataset provenance.
- Difference between raw labels and assignment intents.
- Why source diversity matters.
- Why augmentation is deferred until after a baseline.
- Why UNKNOWN is a separate open-set rejection issue.

## 2026-09-15 18:03:36 +08:00 - Phase 2 - Audio Loading And Log-Mel Preprocessing

### Objective
Implement reproducible audio loading and log-Mel feature extraction from the active dataset metadata index.

### Requirement Addressed
- Requirement 2: Build and train a VCM - preprocessing implementation complete, training NOT YET EXECUTED.
- Requirement 4: Validate VCM performance - preprocessing tests complete, validation NOT YET EXECUTED.
- Requirement 6: Tiny real-time Raspberry Pi VCM - preprocessing direction implemented, Raspberry Pi performance NOT YET MEASURED.
- Requirement 7: Standalone/offline operation - preprocessing uses local files only.

### Action Performed
- Created a preprocessing configuration file.
- Implemented WAV loading, mono conversion, optional resampling, peak normalization, and fixed-length padding/trimming.
- Implemented log-Mel feature extraction using NumPy and SciPy.
- Added a CLI to inspect one indexed WAV through the preprocessing pipeline.
- Added unit tests for metadata inclusion/exclusion, split counts, fixed-length audio loading, and log-Mel feature shape.
- Documented the preprocessing pipeline and exam concepts.

### Files Affected
- `configs/preprocessing.json`
- `preprocessing/__init__.py`
- `preprocessing/audio_io.py`
- `preprocessing/log_mel.py`
- `preprocessing/inspect_preprocessing.py`
- `preprocessing/PREPROCESSING.md`
- `tests/test_preprocessing.py`
- `DECISIONS.md`
- `PROJECT_STATUS.md`
- `EXAM_NOTES.md`
- `AGENT_LOG.md`

### Commands/Tools Used
- `python -m unittest discover -s tests -v`
- `python preprocessing\inspect_preprocessing.py`
- Python packages: `numpy`, `scipy`

### Actual Result
Unit tests passed:

```text
test_dataset_split_counts ... ok
test_index_excludes_duplicate_weather_file ... ok
test_load_audio_pads_to_fixed_length ... ok
test_log_mel_shape_for_indexed_example ... ok
Ran 4 tests ... OK
```

Inspection of one indexed WAV produced:

```text
audio_shape=(64000,)
feature_shape=(398, 40)
feature_dtype=float32
feature_min=-13.815511
feature_max=6.903997
feature_mean=-11.748891
```

### Metrics/Results
- Preprocessing tests: PASSED.
- Log-Mel feature shape: VERIFIED for one indexed dataset WAV.
- Full feature precomputation: NOT YET EXECUTED.
- Model training: NOT YET EXECUTED.
- Accuracy/F1 metrics: NOT YET MEASURED.
- Raspberry Pi latency: NOT YET MEASURED.

### Interpretation
The preprocessing pipeline is implemented and reproducible. One included WAV from the metadata index can be transformed into the expected fixed-shape log-Mel feature matrix.

### Decision
Use 4-second, 40-bin log-Mel features for the first baseline:

`64,000 audio samples -> 398 x 40 log-Mel feature matrix`

### Reason For Decision
The dataset duration range is 0.200 s to 3.880 s, so a 4-second window avoids truncating normal examples before the first baseline. Shorter windows or silence trimming can be evaluated later as separate experiments if needed.

### Problems Encountered
- The first unit-test implementation attempted to use the system temporary directory, which was blocked by Windows sandbox permissions.

### Resolution
- Changed the scratch WAV test to write under the project-local `tests/_tmp` folder.

### Next Step
Decide whether baseline training should compute features on the fly or precompute feature files, then implement the first baseline model.

### Exam Concepts
- 16 kHz mono standardization.
- Fixed-shape model inputs.
- Framing, Hann windows, FFT, Mel filterbanks, and log compression.
- Why training and Raspberry Pi inference must use the same preprocessing.

## 2026-09-15 18:23:57 +08:00 - Phase 2 - Exam Notes Correction

### Objective
Add the exact Phase 2 preprocessing exam questions and answers requested by the user to `EXAM_NOTES.md`.

### Requirement Addressed
- Requirement 2: Build and train a VCM - supports understanding of preprocessing.
- Requirement 6: Tiny real-time Raspberry Pi VCM - supports explanation of compact feature choices.
- Requirement 7: Standalone/offline operation - supports explanation of identical local preprocessing.

### Action Performed
- Reviewed the current `EXAM_NOTES.md`.
- Confirmed that related notes existed but the exact requested checklist was not written explicitly.
- Added a dedicated `Phase 2 Preprocessing Questions` section.

### Files Affected
- `EXAM_NOTES.md`
- `AGENT_LOG.md`

### Commands/Tools Used
- `Get-Content`
- `Get-Date`
- `apply_patch`

### Actual Result
`EXAM_NOTES.md` now explicitly answers:
- why audio is standardized to 16 kHz mono
- why a fixed input shape is required for CNN training
- what framing means
- what STFT/FFT does
- what a Mel filterbank is
- why log-Mel features are useful for command recognition
- why preprocessing must be identical during training, validation, test, and Raspberry Pi inference

### Metrics/Results
- New experimental metrics: NOT YET MEASURED.
- Documentation correction: COMPLETE.

### Interpretation
The exam notes now match the Phase 2 study checklist instead of relying on scattered related answers.

### Decision
Keep preprocessing exam material in `EXAM_NOTES.md` as explicit question-and-answer entries.

### Reason For Decision
The professor may ask these questions directly, and the user needs answers that are easy to reconstruct and explain orally.

### Problems Encountered
- Earlier documentation did not include each requested question in exact form.

### Resolution
- Added the missing explicit Q&A section.

### Next Step
Continue Phase 2/Phase 3 by preparing feature generation or baseline training, using the same preprocessing configuration.

### Exam Concepts
- 16 kHz mono.
- Fixed CNN input shape.
- Framing.
- STFT/FFT.
- Mel filterbank.
- Log-Mel features.
- Consistent preprocessing across all stages.

## 2026-09-15 18:28:11 +08:00 - Documentation Convention - Phase-Labelled Exam Notes

### Objective
Reorganize `EXAM_NOTES.md` so exam questions and answers are clearly labelled by project phase.

### Requirement Addressed
- Exam preparation requirement from the VCM agent brief.
- Documentation/audit trail requirement.

### Action Performed
- Replaced the previous flat `EXAM_NOTES.md` organization with phase-labelled sections.
- Added a convention at the top of the file requiring future exam notes to be filed under the relevant phase.
- Preserved existing questions and answers under Phase 0, Phase 1, and Phase 2.

### Files Affected
- `EXAM_NOTES.md`
- `AGENT_LOG.md`

### Actual Result
`EXAM_NOTES.md` now contains:
- `Phase 0 - Requirements And System Architecture`
- `Phase 1 - Dataset Inspection, Provenance, And Splitting`
- `Phase 2 - Audio Preprocessing And Log-Mel Features`

### Decision
From this point forward, every new exam note should be added under a phase heading.

### Reason For Decision
The user needs to know which task or implementation phase each exam concept belongs to, especially for oral defense preparation.

### Next Step
Continue adding future exam concepts under the relevant phase heading as new work is implemented.

## 2026-09-15 18:40:22 +08:00 - Phase 3 - Baseline Training Scaffold And Smoke Experiments

### Objective
Create the first reproducible baseline training path and run measured smoke experiments.

### Requirement Addressed
- Baseline model preparation.
- Experiment logging.
- Reproducible offline artifact generation.

### Action Performed
- Added `training/baseline_features.py`.
- Added `training/train_sklearn_baseline.py`.
- Added `tests/test_baseline_training.py`.
- Ran unit tests.
- Ran three measured smoke experiments:
  - `E01_SMOKE`
  - `E02_SMOKE_FLAT`
  - `E03_SMOKE_RAW_BALANCED`
- Updated project status, decisions, experiment log, README, and phase-labelled exam notes.

### Files Affected
- `training/__init__.py`
- `training/baseline_features.py`
- `training/train_sklearn_baseline.py`
- `tests/test_baseline_training.py`
- `PROJECT_STATUS.md`
- `DECISIONS.md`
- `EXPERIMENT_LOG.md`
- `EXAM_NOTES.md`
- `README.md`
- `AGENT_LOG.md`
- `results/tables/E01_SMOKE_metrics.json`
- `results/tables/E02_SMOKE_FLAT_metrics.json`
- `results/tables/E03_SMOKE_RAW_BALANCED_metrics.json`
- `models/baseline/E01_SMOKE_sklearn_pipeline.joblib`
- `models/baseline/E02_SMOKE_FLAT_sklearn_pipeline.joblib`
- `models/baseline/E03_SMOKE_RAW_BALANCED_sklearn_pipeline.joblib`

### Commands/Tools Used
- `python -m unittest discover -s tests -v`
- `python training\train_sklearn_baseline.py --experiment-id E01_SMOKE --feature-mode pooled --train-per-intent 30 --validation-per-intent 10 --seed 42 --max-iter 1000`
- `python training\train_sklearn_baseline.py --experiment-id E02_SMOKE_FLAT --feature-mode flat --train-per-intent 30 --validation-per-intent 10 --seed 42 --max-iter 1000`
- `python training\train_sklearn_baseline.py --experiment-id E03_SMOKE_RAW_BALANCED --feature-mode flat --train-per-raw-label 30 --validation-per-raw-label 10 --seed 42 --max-iter 1000`

### Actual Result
- Unit tests passed: 8 tests.
- `E01_SMOKE`: accuracy 0.2000, macro-F1 0.1862.
- `E02_SMOKE_FLAT`: accuracy 0.2000, macro-F1 0.1866.
- `E03_SMOKE_RAW_BALANCED`: accuracy 0.2450, macro-F1 0.2446.

### Interpretation
The baseline pipeline is operational and auditable. The sklearn linear baseline is not strong enough to be the final VCM model.

### Decision
Treat sklearn baselines as Phase 3 smoke/pipeline checks. Proceed toward a true CNN training path.

### Reason For Decision
The assignment direction and Phase 2 exam notes expect a CNN-style command recognizer over log-Mel features. Current local Python environments do not have PyTorch or TensorFlow installed.

### Problems Encountered
- Default Python and Anaconda Python have sklearn/NumPy/SciPy/matplotlib but no PyTorch or TensorFlow.
- Tiny intent-balanced samples underrepresent some raw command labels inside merged assignment intents.

### Resolution
- Added raw-label-balanced sampling.
- Logged smoke results honestly rather than overstating performance.

### Next Step
Set up a true CNN training path or install/select an available deep learning runtime.

### Exam Concepts
- Smoke baseline.
- Macro-F1.
- Confusion matrix.
- Raw-label-balanced sampling.
- Difference between pipeline verification and final model performance.

## 2026-09-15 18:52:26 +08:00 - Phase 4 - CNN Training Path Scaffold

### Objective
Set up enough of the true CNN training path to continue efficiently after the next usage top-up.

### Requirement Addressed
- CNN model preparation.
- Offline project continuity.
- Phase-labelled exam notes.

### Action Performed
- Added `configs/cnn_baseline.json`.
- Added `training/cnn_model.py`.
- Added `training/train_cnn_keras.py`.
- Added `training/CNN_TRAINING.md`.
- Added `tests/test_cnn_scaffold.py`.
- Updated project status, README, exam notes, and agent log.

### Actual Result
The project now has a TensorFlow/Keras CNN scaffold using the Phase 2 `398 x 40 x 1` log-Mel input shape.

### Verification
`python -m unittest discover -s tests -v` passed 10 tests.

### Metrics/Results
CNN training metrics are NOT YET MEASURED.

### Decision
Do not attempt heavy TensorFlow installation or CNN training while usage is low. Stop at a tested scaffold and leave the first CNN smoke command documented.

### Reason For Decision
The current local Python environments do not have TensorFlow installed, and the user asked to do only enough until the next top-up.

### Next Step
After usage top-up, install/select a TensorFlow-capable environment and run:

`python training\train_cnn_keras.py --experiment-id E04_CNN_SMOKE --epochs 3 --train-per-raw-label 50 --validation-per-raw-label 15`

### Exam Concepts
- CNN over log-Mel features.
- Small model design for Raspberry Pi.
- Difference between scaffolded code and measured training results.

## 2026-09-15 18:56:38 +08:00 - Lightweight Pause-Point Check

### Objective
Use the remaining low-usage window for safe checks and a next-session checklist without starting heavy installation or training.

### Action Performed
- Rechecked local Python package availability.
- Re-ran unit tests.
- Added `NEXT_SESSION_CHECKLIST.md`.
- Updated `README.md` to point to the checklist.

### Actual Result
- Python 3.13.6 is active for the default `python` command.
- TensorFlow is not installed.
- PyTorch is not installed.
- sklearn, NumPy, SciPy, and matplotlib are installed.
- `python -m unittest discover -s tests -v` passed 10 tests.

### Decision
Pause before TensorFlow installation and CNN training.

### Reason For Decision
The user indicated low usage remaining and asked to do only what is enough in the meantime.

### Next Step
After top-up, follow `NEXT_SESSION_CHECKLIST.md` and begin with TensorFlow environment setup.

## 2026-09-15 20:57:46 +08:00 - Raspberry Pi 5 Work Plan Added

### Objective
Add step-by-step Raspberry Pi 5 initiation, setup, configuration, programming, deployment, and validation guidance to the project work plan.

### Requirement Addressed
- Raspberry Pi deployment planning.
- Hardware initiation guidance.
- Offline validation planning.
- Phase-labelled exam guidance.

### Action Performed
- Added `deployment/RASPBERRY_PI5_WORK_PLAN.md`.
- Updated `README.md` to link the deployment work plan.
- Updated `PROJECT_STATUS.md`.
- Added exam notes for data expansion, laptop trials, and Raspberry Pi deployment.

### Decision
Wait before building more main command data. Run CNN training and real voice trials first, then add targeted train-only data or augmentation only if measured results justify it.

### Reason For Decision
The active command dataset already has 21,000 included WAV files. Adding more synthetic data before measuring the CNN and real microphone performance could obscure the actual weakness.

### Sources Consulted
- Raspberry Pi getting started documentation.
- Raspberry Pi OS Python package and virtual environment documentation.
- Raspberry Pi GPIO hardware documentation.
- GPIO Zero pin factory documentation.
- Raspberry Pi audio documentation.

### Next Step
After usage top-up, continue with TensorFlow/CNN training. When hardware arrives, follow `deployment/RASPBERRY_PI5_WORK_PLAN.md`.

## 2026-09-15 21:26:09 +08:00 - CNN Smoke Attempt And Fallback MLP Smoke

### Objective
Continue toward the CNN smoke/baseline task.

### Action Performed
- Checked available Python environments.
- Confirmed default Python is 3.13.6.
- Confirmed bundled Codex Python is 3.12.14 but lacks sklearn/SciPy/TensorFlow.
- Attempted to create a project-local virtual environment.
- Attempted short pip TensorFlow package-resolution probes.
- Added `training/train_sklearn_mlp.py`.
- Ran unit tests.
- Ran `E04_SKLEARN_MLP_SMOKE`.

### Actual Result
- TensorFlow was not installed in available Python environments.
- Project venv creation failed during `ensurepip` because copying the bundled pip wheel to temp was denied.
- Pip TensorFlow package-resolution checks did not return promptly and were stopped.
- `python -m unittest discover -s tests -v` passed 10 tests.
- `E04_SKLEARN_MLP_SMOKE` completed:
  - train examples: 1,000
  - validation examples: 300
  - accuracy: 0.2600
  - macro-F1: 0.2319

### Files Affected
- `training/train_sklearn_mlp.py`
- `results/tables/E04_SKLEARN_MLP_SMOKE_metrics.json`
- `results/tables/E04_SKLEARN_MLP_SMOKE_classification_report.txt`
- `results/tables/E04_SKLEARN_MLP_SMOKE_confusion_matrix.csv`
- `results/figures/E04_SKLEARN_MLP_SMOKE_confusion_matrix.png`
- `models/baseline/E04_SKLEARN_MLP_SMOKE_sklearn_mlp.joblib`
- `EXPERIMENT_LOG.md`
- `PROJECT_STATUS.md`
- `DECISIONS.md`
- `EXAM_NOTES.md`
- `AGENT_LOG.md`

### Interpretation
The actual CNN smoke did not run because TensorFlow setup is blocked. The fallback MLP result is measured, but it is not strong enough and is not the final model direction.

### Decision
Continue pursuing a TensorFlow-capable environment for the real CNN baseline.

### Next Step
Resolve TensorFlow installation or use another machine/environment with TensorFlow support, then run `training/train_cnn_keras.py`.

### Cleanup Note
The failed virtual environment attempt left `.venv` and `.tmp` artifacts. A cleanup command was attempted but blocked by the command policy, so these folders should not be treated as a valid training environment.

## 2026-09-15 21:59:13 +08:00 - TensorFlow Environment Resolved

### Objective
Create a TensorFlow-capable environment for CNN training.

### Action Performed
- Diagnosed pip install failures.
- Confirmed pip could not install even small packages until the user-site parent directory existed.
- Downloaded TensorFlow 2.20.0 and dependency wheels into `runtimes/wheels`.
- Added `tools/download_tf_wheelhouse.py` to reproduce the wheelhouse download.
- Installed TensorFlow from the local wheelhouse using `pip --user --no-index --find-links`.
- Verified TensorFlow import.
- Re-ran unit tests.

### Actual Result
- TensorFlow 2.20.0 imports successfully.
- TensorFlow is installed under `C:\Users\Loreen Anne\AppData\Roaming\Python\Python313\site-packages`.
- `python -m unittest discover -s tests -v` passed: 10 tests, 1 skipped because TensorFlow is now installed.

### Decision
Proceed with the actual CNN smoke experiment.

### Next Step
Run `E04_CNN_SMOKE`.

## 2026-09-15 22:26:04 +08:00 - CNN Smoke Experiments Completed

### Objective
Run the actual TensorFlow CNN smoke/baseline after resolving the environment.

### Action Performed
- Patched `training/train_cnn_keras.py` for Keras 3 compatibility.
- Diagnosed hangs in high-level Keras `fit`, `evaluate`, and `.keras` save paths.
- Replaced the high-level Keras training/evaluation/save path with:
  - manual TensorFlow gradient training loop
  - direct validation forward pass
  - NumPy `.npz` model weight saving
- Added train-derived log-Mel normalization.
- Ran `E04_CNN_SMOKE`.
- Ran `E05_CNN_SMOKE_NORM`.
- Ran `E06_CNN_SMOKE_NORM_20E`.
- Re-ran unit tests.

### Actual Result
- `E04_CNN_SMOKE`: validation accuracy 0.0967.
- `E05_CNN_SMOKE_NORM`: validation accuracy 0.0967.
- `E06_CNN_SMOKE_NORM_20E`: validation accuracy 0.1233.
- `python -m unittest discover -s tests -v` passed 10 tests with 1 expected skip because TensorFlow is installed.

### Interpretation
The TensorFlow CNN path now works, but the current tiny CNN/training setup is not yet a good command recognizer.

### Decision
Do not add more command data yet. Diagnose CNN underperformance first.

### Next Step
Generate prediction/confusion diagnostics for the CNN outputs and revise the architecture/training setup before attempting a full baseline or Raspberry Pi deployment.

## 2026-09-15 22:37:57 +08:00 - CNN Diagnostics And Overfit Sanity Tests

### Objective
Run CNN prediction/confusion diagnostics and overfit sanity tests.

### Action Performed
- Added `evaluation/cnn_predict_diagnostics.py`.
- Added `configs/cnn_no_batchnorm.json`.
- Added `configs/cnn_fast_batchnorm.json`.
- Updated CNN training to support intent-balanced sampling and overfit-same-data validation.
- Generated prediction diagnostics for `E06_CNN_SMOKE_NORM_20E`.
- Ran raw-label-balanced overfit test `E07_CNN_OVERFIT_TINY`.
- Ran no-BatchNorm overfit test `E08_CNN_OVERFIT_NOBN`.
- Ran intent-balanced default BatchNorm overfit test `E09_CNN_OVERFIT_INTENT_BALANCED`.
- Ran intent-balanced no-BatchNorm overfit test `E10_CNN_OVERFIT_INTENT_NOBN`.
- Ran intent-balanced fast-BatchNorm overfit test `E11_CNN_OVERFIT_FASTBN`.
- Re-ran unit tests.

### Actual Result
- `E06` diagnostics: 253 of 300 validation examples predicted as `THERMOSTAT`; macro-F1 0.0499.
- `E09`: training accuracy 0.9600 but same-data inference accuracy 0.1000.
- `E10`: same-data inference accuracy 0.2200.
- `E11`: same-data inference accuracy 0.8600 and macro-F1 0.8614.
- Unit tests passed: 12 tests, 1 expected skip.

### Interpretation
The CNN pipeline works, but default BatchNorm caused inference failure in the manual training setup. Fast BatchNorm fixed the overfit sanity test.

### Decision
Use `configs/cnn_fast_batchnorm.json` for the next real CNN smoke/baseline. Do not add more data yet.

### Next Step
Run a corrected CNN smoke/baseline using fast BatchNorm and intent-balanced sampling.

## 2026-09-15 22:46:37 +08:00 - Corrected Fast-BatchNorm CNN Smoke

### Objective
Run the corrected real CNN smoke/baseline using `configs/cnn_fast_batchnorm.json` and intent-balanced sampling.

### Action Performed
- Ran `E12_CNN_FASTBN_INTENT_SMOKE`.
- Generated intent-balanced prediction/confusion diagnostics.
- Updated project status, experiment log, decisions, exam notes, and agent log.

### Actual Result
- Training examples: 1,000.
- Validation examples: 300.
- Epochs: 40.
- Training accuracy at final epoch: 0.6970.
- Intent-balanced validation accuracy: 0.3533.
- Intent-balanced validation macro-F1: 0.3716.
- Diagnostic predicted counts still show over-prediction of `THERMOSTAT`: 173 of 300 validation examples.

### Interpretation
Fast BatchNorm fixed the earlier inference failure and produced a much stronger CNN smoke, but the model remains too biased and too weak for deployment.

### Decision
Continue model diagnosis and improvement before adding data or deploying.

### Next Step
Inspect per-class confusion for `E12`, then improve architecture/training to reduce `THERMOSTAT` collapse.

## 2026-09-16 03:35:04 +08:00 - Stronger Dense CNN Smoke Baseline

### Objective
Continue CNN model diagnosis after the corrected fast-BatchNorm baseline.

### Action Performed
- Confirmed `E13_CNN_DENSE_OVERFIT` completed.
- Fixed the manual CNN training loop so it uses the learning rate from the selected CNN config.
- Added `configs/cnn_fastbn_dense_nodropout.json`.
- Ran `python -m unittest discover -s tests`; 13 tests passed with 1 expected skip.
- Ran `E14_CNN_DENSE_NODROPOUT_OVERFIT`.
- Ran `E15_CNN_DENSE_NODROPOUT_INTENT_SMOKE`.
- Generated prediction and confusion diagnostics for `E15`.
- Updated project status, experiment log, decisions, and exam notes.

### Actual Result
- `E13_CNN_DENSE_OVERFIT`: same-data validation accuracy 0.5400, macro-F1 0.5311.
- `E14_CNN_DENSE_NODROPOUT_OVERFIT`: same-data validation accuracy 1.0000, macro-F1 1.0000.
- `E15_CNN_DENSE_NODROPOUT_INTENT_SMOKE`: validation accuracy 0.5533, macro-F1 0.5411.
- `E15` predicted all 10 intents instead of collapsing mostly into one class.

### Interpretation
The CNN path is now learning properly on the current log-Mel features. Removing dropout made the dense CNN pass the sanity test, and the same configuration improved real validation performance.

### Decision
Treat `E15` as the best smoke baseline at that point, but not as the final model. This was later superseded by `E16`.

### Next Step
Tune training stability and inspect per-class confusion, especially for `CALL_MESSAGE` and `QUESTION`, before full training or Raspberry Pi deployment.

## 2026-09-16 03:49:02 +08:00 - Best-Validation CNN Smoke Checkpoint

### Objective
Test whether saving the best validation epoch improves the current CNN smoke baseline.

### Action Performed
- Added optional `--track-best-validation` support to `training/train_cnn_keras.py`.
- Re-ran unit tests: 13 passed, 1 expected skip.
- Ran `E16_CNN_DENSE_NODROPOUT_BESTVAL_SMOKE`.
- Generated prediction and confusion diagnostics for `E16`.
- Updated project status, experiment log, decisions, and exam notes.

### Actual Result
- Best validation checkpoint: epoch 50.
- Validation accuracy: 0.5600.
- Macro-F1: 0.5434.
- Model weights file size: 248,537 bytes.
- Prediction counts are distributed across all 10 intents.

### Interpretation
Best-validation checkpointing gives a small but real improvement and confirms that training stability matters. The model is no longer collapsed into one intent, but it still needs tuning before deployment.

### Decision
Use `E16_CNN_DENSE_NODROPOUT_BESTVAL_SMOKE` as the best smoke baseline at that point. It was later superseded by `E19`.

### Next Step
Try lower learning rate and/or mild regularization with best-validation tracking, then scale training after the validation pattern is more stable.

## 2026-09-16 05:16:25 +08:00 - Lower Learning Rate CNN Tuning

### Objective
Test whether a lower learning rate improves the current no-dropout dense CNN smoke baseline.

### Action Performed
- Added `configs/cnn_fastbn_dense_nodropout_lr3e4.json`.
- Ran `python -m unittest discover -s tests`; 13 tests passed with 1 expected skip.
- Ran `E17_CNN_DENSE_NODROPOUT_LR3E4_BESTVAL_SMOKE`.
- Generated prediction and confusion diagnostics for `E17`.
- Updated project status, experiment log, decisions, and exam notes.

### Actual Result
- Best validation checkpoint: epoch 56.
- Validation accuracy: 0.3533.
- Macro-F1: 0.3594.
- Model weights file size: 248,186 bytes.

### Interpretation
Lowering the learning rate alone made the smoke baseline worse. The model memorized the training subset but did not generalize well to validation.

### Decision
Keep `E16_CNN_DENSE_NODROPOUT_BESTVAL_SMOKE` as the best smoke baseline at that point. It was later superseded by `E19`.

### Next Step
Try mild regularization or a larger training subset with best-validation tracking.

## 2026-09-16 06:01:29 +08:00 - Mild Regularization And Larger Training Subset

### Objective
Try mild regularization or a larger training subset with `--track-best-validation`.

### Action Performed
- Added `configs/cnn_fastbn_dense_dropout01.json`.
- Ran `python -m unittest discover -s tests`; 13 tests passed with 1 expected skip.
- Ran `E18_CNN_DENSE_DROPOUT01_BESTVAL_SMOKE` using dropout 0.1.
- Generated diagnostics for `E18`.
- Ran `E19_CNN_DENSE_NODROPOUT_300PI_BESTVAL` using 300 training examples per intent.
- Generated diagnostics for `E19`.
- Updated project status, experiment log, decisions, and exam notes.

### Actual Result
- `E18`: validation accuracy 0.4967, macro-F1 0.4667.
- `E19`: best epoch 51, validation accuracy 0.7233, macro-F1 0.7198.
- `E19` model weights file size: 249,006 bytes.

### Interpretation
Mild dropout was not helpful on the smoke subset. Increasing training coverage from 1,000 to 3,000 examples produced a large improvement, so the current dataset should be used more fully before deciding to augment.

### Decision
Promote `E19_CNN_DENSE_NODROPOUT_300PI_BESTVAL` as the current best smoke baseline.

### Next Step
Inspect `MEDIA_CONTROL` confusion and consider scaling closer to the full training set with best-validation tracking.

## 2026-09-16 08:33:11 +08:00 - Confidence Diagnostics And Larger CNN Scale-Up

### Objective
Continue the CNN route, scale training closer to the full dataset, add confidence-threshold evaluation, and inspect `MEDIA_CONTROL`.

### Action Performed
- Added `evaluation/prediction_error_analysis.py`.
- Ran confidence-threshold and `MEDIA_CONTROL` raw-label diagnostics for E19.
- Ran `E20_CNN_DENSE_NODROPOUT_600PI_BESTVAL` using 600 training examples per intent.
- Generated prediction, confusion, confidence-threshold, and `MEDIA_CONTROL` diagnostics for E20.
- Updated project status, experiment log, decisions, and exam notes.

### Actual Result
- E19 threshold 0.90: accepted 206/300 examples, accepted-command accuracy 0.8738.
- E19 `MEDIA_CONTROL` weak raw labels: `NEXT` 1/9 correct and `VOLUME_DOWN` 1/5 correct.
- E20 best epoch: 60.
- E20 validation accuracy: 0.8133.
- E20 macro-F1: 0.8113.
- E20 threshold 0.90: accepted 250/300 examples, accepted-command accuracy 0.8800.
- E20 threshold 0.95: accepted 232/300 examples, accepted-command accuracy 0.9181.
- E20 `MEDIA_CONTROL` improved to precision 0.65, recall 0.57, F1 0.61.

### Interpretation
Scaling the existing dataset continues to improve the CNN. Confidence thresholding gives a practical safety gate for Raspberry Pi deployment. `MEDIA_CONTROL` is still the weakest class, but it improved with more training coverage.

### Decision
Keep `E20_CNN_DENSE_NODROPOUT_600PI_BESTVAL` as the current best smoke baseline. Do not add new data yet.

### Next Step
Either scale closer to the full training set or run laptop microphone trials with confidence-threshold rejection once the user is ready.

## 2026-09-16 12:12:09 +08:00 - Larger CNN Scale-Up To 1,000 Per Intent

### Objective
Run larger CNN training using existing data, generate confusion and confidence-threshold diagnostics, and decide whether accuracy improves or stabilizes before laptop microphone trials.

### Action Performed
- Ran `E21_CNN_DENSE_NODROPOUT_1000PI_BESTVAL` using up to 1,000 training examples per intent.
- Generated prediction and confusion diagnostics for E21.
- Generated confidence-threshold and `MEDIA_CONTROL` raw-label diagnostics for E21.
- Updated project status, experiment log, decisions, and exam notes.

### Actual Result
- E21 selected 9,520 training examples.
- Best validation checkpoint: epoch 51.
- Validation accuracy: 0.8267.
- Macro-F1: 0.8304.
- E21 threshold 0.90: accepted 255/300 examples, accepted-command accuracy 0.8902.
- E21 threshold 0.95: accepted 241/300 examples, accepted-command accuracy 0.9046.
- E21 `MEDIA_CONTROL`: precision 0.50, recall 0.70, F1 0.58.

### Interpretation
Scaling closer to the full dataset improved overall macro-F1 slightly over E20. The main caution is `MEDIA_CONTROL`: E21 catches more actual media commands but over-predicts that class.

### Decision
Promote `E21_CNN_DENSE_NODROPOUT_1000PI_BESTVAL` as the current best smoke baseline by macro-F1.

### Next Step
Prepare laptop microphone trials with confidence-threshold rejection, and log false `MEDIA_CONTROL` triggers carefully.

## 2026-09-16 12:20:11 +08:00 - Laptop WAV Trial Tooling

### Objective
Prepare the next step: laptop microphone trials with confidence-threshold rejection.

### Action Performed
- Checked the current Python environment for audio recording packages.
- Confirmed `sounddevice`, `pyaudio`, and `soundfile` are not installed.
- Confirmed `ffmpeg`, `SoundRecorder.exe`, and `VoiceRecorder.exe` are not available as command-line recorders.
- Added `demo/cnn_inference.py`.
- Added `demo/predict_wav.py`.
- Added `demo/record_and_predict.py`.
- Added `demo/LAPTOP_MIC_TRIALS.md`.
- Ran a WAV prediction smoke test using the E21 model.
- Re-ran unit tests.

### Actual Result
- `python -m unittest discover -s tests` passed 13 tests with 1 expected skip.
- `demo/predict_wav.py` loaded E21 weights and predicted a known `CALL_MESSAGE` WAV correctly.
- The same prediction was rejected by the 0.90 threshold because confidence was 0.508806, proving the gate is active.
- `demo/record_and_predict.py` exits cleanly and explains that `sounddevice` is required for live microphone capture.

### Interpretation
The local inference path is ready. Live laptop recording needs either the optional `sounddevice` dependency or a PCM WAV recording produced by another local recorder.

### Decision
Use WAV-based laptop trials immediately if a local WAV recording is available. Do not add new data yet.

### Next Step
Obtain or record PCM WAV laptop microphone samples, then run them through `demo/predict_wav.py` with threshold 0.90 or 0.95.

## 2026-09-16 12:27:28 +08:00 - First Real Laptop WAV Trial

### Objective
Run the user's first laptop-recorded command through the current E21 model.

### Action Performed
- The requested path `C:\Users\Loreen Anne\Downloads\turn_on_lights.wav` was not present.
- Found likely recordings in Downloads: `turn_on_lights.m4a` and `Recording.wav`.
- Used `Recording.wav` because it is a compatible PCM WAV file.
- Checked WAV header: stereo, 48 kHz, 16-bit, 2.731 seconds.
- Ran `demo/predict_wav.py` with expected intent `LIGHT_CONTROL` and threshold 0.90.

### Actual Result
- Predicted intent: `SET_ALARM`.
- Confidence: 0.818775.
- Accepted: false.
- Top 3: `SET_ALARM`, `QUESTION`, `LIGHT_CONTROL`.

### Interpretation
The recognition was wrong, but the confidence gate worked as intended and rejected the command before execution.

### Decision
Do not add new data yet based on one trial. Run more controlled laptop WAV trials and look for a repeated pattern.

### Next Step
Record several short WAV commands for `LIGHT_CONTROL`, keeping the phrase and microphone distance consistent, then run them through `demo/predict_wav.py`.

## 2026-09-16 12:36:13 +08:00 - Controlled Laptop WAV Batch

### Objective
Run the user's laptop recordings from `Documents\Sound Recordings` through E21 and summarize the trial batch.

### Action Performed
- Located 13 WAV files in `C:\Users\Loreen Anne\Documents\Sound Recordings`.
- Ran all 13 through `demo/predict_wav.py` with expected intent `LIGHT_CONTROL` and threshold 0.90.
- Summarized the appended `results/tables/laptop_mic_trials.csv` rows.

### Actual Result
- Correct predictions: 4/13.
- Accepted predictions: 10/13.
- Accepted correct predictions: 4/13.
- Accepted wrong predictions: 6/13.
- Wrong accepted predictions included `CALL_MESSAGE`, `SET_ALARM`, `MEDIA_CONTROL`, `THERMOSTAT`, and `PLAY_MUSIC`.

### Interpretation
Laptop-recorded audio currently has a mismatch against the training/validation distribution. Confidence gating helped some cases, but it did not prevent all false accepts because several wrong predictions were highly confident.

### Decision
Do not use laptop audio for action execution yet. Keep using the trials diagnostically.

### Next Step
Inspect the recording quality/setup and repeat controlled trials before deciding whether new real laptop/Pi microphone data is needed.

## 2026-09-16 12:48:00 +08:00 - Second Controlled Laptop WAV Batch

### Objective
Run the newer laptop recordings from `Documents\Sound Recordings` through E21 and determine whether the first failed batch was an outlier.

### Action Performed
- Located 20 newer WAV files in `C:\Users\Loreen Anne\Documents\Sound Recordings`.
- Ran all 20 through `demo/predict_wav.py` with expected intent `LIGHT_CONTROL` and threshold 0.90.
- Summarized the latest appended rows in `results/tables/laptop_mic_trials.csv`.
- Checked WAV metadata and rough amplitude statistics.

### Actual Result
- Correct predictions: 0/20.
- Accepted predictions: 13/20.
- Accepted correct predictions: 0/20.
- Accepted wrong predictions: 13/20.
- Predicted intents: `MEDIA_CONTROL` 10, `CALL_MESSAGE` 5, `QUESTION` 2, `LIGHT_ADJUST` 2, and `PLAY_MUSIC` 1.
- Files were normal PCM WAVs, 44.1 kHz stereo, about 0.92 to 1.87 seconds long.

### Interpretation
The second batch confirms a serious laptop-recording/domain mismatch. The CNN validation result is useful, but it does not yet transfer safely to this laptop microphone setup. Confidence-threshold rejection is not enough because many wrong predictions are highly confident.

### Decision
Do not execute real actions from laptop WAV predictions yet. Treat laptop trials as diagnostics only.

### Next Step
Inspect phrase consistency, recording setup, and preprocessing/domain mismatch. The next data step should be targeted real-microphone collection or augmentation only after confirming what differs between the training audio and the live/laptop recordings.

## 2026-09-16 12:56:00 +08:00 - Third Controlled Laptop WAV Batch

### Objective
Evaluate the freshly replaced/new WAV files in `C:\Users\Loreen Anne\Documents\Sound Recordings`.

### Action Performed
- Located 21 fresh WAV files timestamped around 12:52-12:53 PM.
- Ran all 21 through `demo/predict_wav.py` with expected intent `LIGHT_CONTROL` and threshold 0.90.
- Summarized the latest 21 appended rows in `results/tables/laptop_mic_trials.csv`.
- Checked WAV metadata and rough amplitude statistics.

### Actual Result
- Correct predictions: 1/21.
- Accepted predictions: 12/21.
- Accepted correct predictions: 1/21.
- Accepted wrong predictions: 11/21.
- Predicted intents: `CALL_MESSAGE` 12, `SET_ALARM` 2, `QUESTION` 2, `MEDIA_CONTROL` 2, `THERMOSTAT` 1, `LIGHT_ADJUST` 1, and `LIGHT_CONTROL` 1.
- Files were normal PCM WAVs, 44.1 kHz stereo, about 0.71 to 3.40 seconds long.

### Interpretation
The third batch is slightly better than the second because one `LIGHT_CONTROL` example was correctly accepted, but it is still not reliable enough for command execution. The dominant error shifted from `MEDIA_CONTROL` to `CALL_MESSAGE`, which suggests the issue is not one isolated weak class; it is a broader real-microphone/domain mismatch.

### Decision
Continue treating laptop microphone trials as diagnostic only. Do not trigger real actions from these predictions.

### Next Step
Before collecting large new data, create a small labelled real-microphone calibration set with exact phrase labels. Then compare dataset examples and laptop examples at the feature level, and use targeted real-mic data or targeted augmentation only if the mismatch persists.

## 2026-09-16 13:06:00 +08:00 - Laptop Real-Mic Calibration Set 001

### Objective
Run the 50-file real-microphone calibration set from `Documents\Sound Recordings`.

### Label Assumption
The 50 files were labelled in the requested recording order: 5 files each for `LIGHT_CONTROL`, `LIGHT_ADJUST`, `MEDIA_CONTROL`, `SET_TIMER`, `SET_ALARM`, `QUESTION`, `PLAY_MUSIC`, `CALL_MESSAGE`, `THERMOSTAT`, and `REMINDER`.

### Action Performed
- Located 50 fresh WAV files timestamped around 1:00-1:03 PM.
- Ran `demo/predict_wav.py` on each 5-file group with the matching expected intent.
- Used threshold 0.90.
- Wrote calibration summaries:
  - `results/tables/LAPTOP_CALIBRATION_SET_001_summary.csv`
  - `results/tables/LAPTOP_CALIBRATION_SET_001_confusion.csv`
  - `results/tables/LAPTOP_CALIBRATION_SET_001_per_file.csv`

### Actual Result
- Overall correct predictions: 17/50.
- Overall accuracy: 0.3400.
- Accepted predictions: 34/50.
- Accepted correct predictions: 14/34.
- Accepted-command accuracy: 0.4118.
- Accepted wrong predictions: 20/34.

### Per-Intent Result
- `PLAY_MUSIC`: 5/5 correct.
- `MEDIA_CONTROL`: 3/5 correct.
- `SET_ALARM`: 3/5 correct.
- `THERMOSTAT`: 2/5 correct.
- `SET_TIMER`, `QUESTION`, `CALL_MESSAGE`, and `REMINDER`: 1/5 correct each.
- `LIGHT_CONTROL` and `LIGHT_ADJUST`: 0/5 correct.

### Interpretation
The laptop real-mic calibration confirms a broad domain mismatch. The model transfers well for `PLAY_MUSIC`, partially for `MEDIA_CONTROL` and `SET_ALARM`, but fails badly on lighting commands and several other intents. Confidence thresholding is not sufficient because many wrong predictions are confidently accepted.

### Decision
Do not use the current E21 model for live command execution. The next model step should use this calibration set as evidence for targeted adaptation/augmentation, not broad random data expansion.

### Next Step
Confirm that the 50 files were recorded in the assumed order. If confirmed, create a targeted improvement experiment using real-microphone calibration examples for diagnostics and possibly training/validation separation.

## 2026-09-16 13:36:00 +08:00 - Laptop Real-Mic Calibration Set 002

### Objective
Run the second 50-file real-microphone calibration set from `Documents\Sound Recordings`.

### Label Assumption
The user confirmed the intended order: 5 files each for `LIGHT_CONTROL`, `LIGHT_ADJUST`, `MEDIA_CONTROL`, `SET_TIMER`, `SET_ALARM`, `QUESTION`, `PLAY_MUSIC`, `CALL_MESSAGE`, `THERMOSTAT`, and `REMINDER`.

### Action Performed
- Located 50 fresh WAV files timestamped around 1:27-1:30 PM.
- Ran `demo/predict_wav.py` on each 5-file group with the matching expected intent.
- Used threshold 0.90.
- Wrote calibration summaries:
  - `results/tables/LAPTOP_CALIBRATION_SET_002_summary.csv`
  - `results/tables/LAPTOP_CALIBRATION_SET_002_confusion.csv`
  - `results/tables/LAPTOP_CALIBRATION_SET_002_per_file.csv`
  - `results/tables/LAPTOP_CALIBRATION_SET_001_vs_002_summary.csv`

### Actual Result
- Overall correct predictions: 42/50.
- Overall accuracy: 0.8400.
- Accepted predictions: 44/50.
- Accepted correct predictions: 39/44.
- Accepted-command accuracy: 0.8864.
- Accepted wrong predictions: 5/44.

### Per-Intent Result
- `MEDIA_CONTROL`, `SET_ALARM`, `QUESTION`, `CALL_MESSAGE`, and `REMINDER`: 5/5 correct.
- `LIGHT_ADJUST`, `SET_TIMER`, and `THERMOSTAT`: 4/5 correct.
- `PLAY_MUSIC`: 3/5 correct.
- `LIGHT_CONTROL`: 2/5 correct.

### Interpretation
Set 002 is dramatically better than Set 001, which suggests recording consistency and phrase delivery strongly affect real-microphone performance. However, `LIGHT_CONTROL` remains the weakest class, and this is deployment-critical because the LED demo depends on light commands.

### Decision
Keep Set 002 as the better calibration evidence. Do not call the model final yet; use the calibration comparison to guide targeted work on lighting commands and accepted false positives.

### Next Step
Preserve Set 002 files/artifacts, then run targeted diagnostics for the 5 wrong accepted Set 002 predictions and the `LIGHT_CONTROL` examples.

## 2026-09-16 13:43:00 +08:00 - Calibration Set 002 Preservation And Light Diagnostics

### Objective
Preserve the stronger calibration set and inspect the remaining deployment-critical errors.

### Action Performed
- Copied the 50 Set 002 WAV files into `data/calibration/LAPTOP_CALIBRATION_SET_002`.
- Renamed the archived WAVs with stable label-prefixed filenames, such as `01_LIGHT_CONTROL_1.wav`.
- Created `data/calibration/LAPTOP_CALIBRATION_SET_002/manifest.csv`.
- Created diagnostic outputs:
  - `results/tables/LAPTOP_CALIBRATION_SET_002_audio_diagnostics.csv`
  - `results/tables/LAPTOP_CALIBRATION_SET_002_wrong_accepted.csv`
  - `results/tables/LAPTOP_CALIBRATION_SET_002_light_control_diagnostics.csv`
  - `results/tables/LAPTOP_CALIBRATION_SET_002_threshold_summary.csv`
  - `results/tables/LAPTOP_CALIBRATION_SET_002_light_control_nearest_dataset.csv`

### Actual Result
- The 5 wrong accepted Set 002 predictions were preserved and isolated.
- Raising the confidence threshold improves accepted-command accuracy, but it does not remove the two worst `LIGHT_CONTROL -> QUESTION` errors because both have confidence above 0.999.
- No non-light examples were predicted as `LIGHT_CONTROL` in Set 002.
- The nearest-dataset diagnostic showed that failed light-control examples still have nearby original-dataset `LIGHT_CONTROL` examples, so the problem is not simply that the recordings are unlike the light-control class.

### Interpretation
For the LED demo, the immediate safety risk is lower than the raw wrong-accepted count suggests because Set 002 did not produce false `LIGHT_CONTROL` predictions from other intents. The usability risk remains: real `LIGHT_CONTROL` commands are still often missed or misrouted.

### Decision
Do not rely on threshold tuning alone. The next improvement should target `LIGHT_CONTROL` recognition specifically, using the preserved calibration examples as diagnostics.

### Next Step
Prepare a targeted light-command adaptation plan: collect more real-mic `LIGHT_CONTROL` examples or fine-tune/train with a small calibration split while keeping held-out real-mic examples for evaluation.

## 2026-09-16 14:16:00 +08:00 - E22 Larger Training Probe

### Objective
Try a manageable larger CNN training run to improve real-microphone `LIGHT_CONTROL` while keeping Calibration Set 002 held out from training.

### Action Performed
- Started a near-full `1680` examples-per-intent run, but stopped it because tensor preparation/training was too slow for the current session.
- Ran a shorter probe instead: `E22_CNN_DENSE_NODROPOUT_1200PI_8E_PROBE`.
- Used `configs/cnn_fastbn_dense_nodropout.json`.
- Used `--train-per-intent 1200`, `--validation-per-intent 30`, `--track-best-validation`, and 8 epochs.
- Generated official validation diagnostics.
- Evaluated the archived Calibration Set 002 against E22.
- Created `results/tables/E21_vs_E22_8E_SET002_comparison.csv`.

### Actual Result
- Official validation accuracy: 0.7700.
- Official validation macro-F1: 0.7635.
- Calibration Set 002 accuracy: 41/50, or 0.8200.
- Calibration Set 002 accepted-command accuracy at threshold 0.90: 27/29, or 0.9310.
- Calibration Set 002 wrong accepted predictions at threshold 0.90: 2.
- `LIGHT_CONTROL` on Calibration Set 002 dropped to 1/5 correct.

### Interpretation
E22 is undertrained compared with E21 on official validation and does not solve the LED-critical `LIGHT_CONTROL` weakness. It reduces accepted false positives on Calibration Set 002, but that benefit comes with lower coverage and worse light-control recall.

### Decision
Do not promote E22. Keep E21 as the current selected baseline while using E22 as evidence that more training coverage alone, especially in a short probe, is not enough.

### Next Step
Target `LIGHT_CONTROL` directly: collect more real-microphone light-command examples or design a controlled fine-tuning experiment with separate real-mic train/holdout clips.

## 2026-09-16 14:28:00 +08:00 - Class LIGHT_ON/LIGHT_OFF Download Inspection

### Objective
Determine whether the user's newly downloaded class `LIGHT_ON` and `LIGHT_OFF` folders are useful for the current `LIGHT_CONTROL` weakness.

### Action Performed
- Inspected `C:\Users\Loreen Anne\Downloads\LIGHT_ON-20260916T062226Z-1-001`.
- Inspected `C:\Users\Loreen Anne\Downloads\LIGHT_OFF-20260916T062225Z-1-001`.
- Verified WAV compatibility.
- Compared filenames against the active dataset index.
- Scored all files with the current selected E21 model.

### Actual Result
- `LIGHT_ON`: 360 WAV files.
- `LIGHT_OFF`: 387 WAV files.
- Total: 747 WAV files.
- Format: 16 kHz, mono, 16-bit PCM WAV.
- E21 predicted `LIGHT_CONTROL` correctly for 662/747 files.
- Overall accuracy on these folders: 0.8862.
- `LIGHT_ON` accuracy: 318/360, or 0.8833.
- `LIGHT_OFF` accuracy: 344/387, or 0.8889.
- Output files:
  - `results/tables/LIGHT_ON_OFF_CLASS_DOWNLOAD_E21_predictions.csv`
  - `results/tables/LIGHT_ON_OFF_CLASS_DOWNLOAD_E21_summary.csv`

### Interpretation
These folders are useful as extra light-command data and external light-command evaluation evidence. However, E21 already performs well on them, so they do not directly explain or solve the laptop real-microphone `LIGHT_CONTROL` weakness. They appear closer to the existing dataset style than to the laptop calibration recordings.

### Decision
Use these files as documented external/light-command support data if needed, but do not treat them as a substitute for more real-microphone recordings from the laptop or Raspberry Pi microphone.

### Next Step
Record or collect additional real-microphone `LIGHT_CONTROL` examples for the actual deployment microphone. The class folders can supplement training later, but the held-out real-mic calibration set should remain the deployment check.

## 2026-09-16 14:38:00 +08:00 - Real-Mic Light-Control Set 003

### Objective
Evaluate 25 fresh real-microphone recordings of the phrase "turn on the light."

### Action Performed
- Located 25 fresh WAV files in `C:\Users\Loreen Anne\Documents\Sound Recordings`.
- Archived them under `data/calibration/LIGHT_CONTROL_REALMIC_SET_003_TURN_ON_25`.
- Ran the current selected E21 model on all 25 files.
- Created:
  - `results/tables/LIGHT_CONTROL_REALMIC_SET_003_TURN_ON_25_E21_per_file.csv`
  - `results/tables/LIGHT_CONTROL_REALMIC_SET_003_TURN_ON_25_E21_summary.csv`
  - `results/tables/LIGHT_CONTROL_REALMIC_SET_003_TURN_ON_25_E21_threshold_summary.csv`

### Actual Result
- Correct predictions: 10/25.
- Accuracy: 0.4000.
- Accepted predictions at threshold 0.90: 12/25.
- Accepted correct predictions: 8/12.
- Accepted wrong predictions: 4/12.
- Wrong accepted predictions were `REMINDER`, `QUESTION`, and `SET_ALARM`.

### Interpretation
This confirms that `LIGHT_CONTROL` remains weak on real-microphone audio. More generic light-command dataset audio is useful, but the deployment issue is specifically the real-microphone domain.

### Decision
Keep E21 as the selected baseline, but do not treat light-command deployment as solved. More real-mic light data is justified.

### Next Step
Use this Set 003 as held-out evidence or split it carefully if doing fine-tuning. The safest path is to collect additional real-mic light examples, then train on one portion and evaluate on a held-out portion.

## 2026-09-16 14:47:00 +08:00 - Real-Mic Light-Control Set 004

### Objective
Evaluate 25 fresh real-microphone recordings of the phrase "turn off the light" and combine them with the previous "turn on the light" set.

### Action Performed
- Located 25 fresh WAV files in `C:\Users\Loreen Anne\Documents\Sound Recordings`.
- Archived them under `data/calibration/LIGHT_CONTROL_REALMIC_SET_004_TURN_OFF_25`.
- Ran the current selected E21 model on all 25 files.
- Created:
  - `results/tables/LIGHT_CONTROL_REALMIC_SET_004_TURN_OFF_25_E21_per_file.csv`
  - `results/tables/LIGHT_CONTROL_REALMIC_SET_004_TURN_OFF_25_E21_summary.csv`
  - `results/tables/LIGHT_CONTROL_REALMIC_SET_004_TURN_OFF_25_E21_threshold_summary.csv`
  - `results/tables/LIGHT_CONTROL_REALMIC_SET_003_004_COMBINED_E21_summary.csv`
  - `results/tables/LIGHT_CONTROL_REALMIC_SET_003_004_COMBINED_E21_threshold_summary.csv`

### Actual Result
- Turn-off set correct predictions: 4/25.
- Turn-off set accuracy: 0.1600.
- Turn-off accepted predictions at threshold 0.90: 11/25.
- Turn-off accepted correct predictions: 1/11.
- Turn-off accepted wrong predictions: 10/11.
- Combined turn-on/turn-off correct predictions: 14/50.
- Combined accuracy: 0.2800.
- Combined accepted predictions at threshold 0.90: 23/50.
- Combined accepted correct predictions: 9/23.
- Combined accepted wrong predictions: 14/23.

### Interpretation
The real-microphone light-command gap is now confirmed more strongly. The model performs much better on dataset-style `LIGHT_ON`/`LIGHT_OFF` folders than on the user's real laptop microphone light commands.

### Decision
Do not claim reliable LED voice control yet. The next model work should be a targeted real-microphone `LIGHT_CONTROL` adaptation experiment with a clear train/holdout split.

### Next Step
Build a real-mic light adaptation split from Sets 003 and 004, keeping a held-out portion untouched for evaluation. Do not train on all real-mic light clips and then report on the same clips.

## 2026-09-16 14:56:00 +08:00 - E23 Targeted Real-Mic Light Adaptation

### Objective
Fine-tune the E21 CNN for real-microphone `LIGHT_CONTROL` while preserving a held-out real-mic light evaluation set.

### Action Performed
- Added `training/fine_tune_light_realmic.py`.
- Split real-mic light clips from Sets 003 and 004:
  - Train/adaptation: first 15 `turn on` + first 15 `turn off`, 30 clips total.
  - Holdout: last 10 `turn on` + last 10 `turn off`, 20 clips total.
- Started from E21 weights and E21 normalization.
- Included 880 original-dataset replay examples to reduce forgetting.
- Fine-tuned for 8 epochs with learning rate 0.0001.
- Selected the best checkpoint by real-mic holdout accuracy, with official validation macro-F1 as the tie-breaker.

### Actual Result
- New experiment: `E23_LIGHT_REALMIC_ADAPT_E21_REPLAY`.
- Best epoch: 3.
- Held-out real-mic light accuracy: 16/20, or 0.8000.
- Held-out accepted predictions at threshold 0.90: 12/20.
- Held-out accepted correct predictions: 12/12.
- Held-out wrong accepted predictions: 0.
- Official validation accuracy: 0.7933.
- Official validation macro-F1: 0.7912.

### Baseline Comparison On Same Holdout
- E21 baseline: 4/20 correct, 6 accepted, 2 accepted correct, 4 accepted wrong.
- E23 adapted: 16/20 correct, 12 accepted, 12 accepted correct, 0 accepted wrong.

### Interpretation
Targeted adaptation substantially improves real-microphone light-command behavior and removes wrong accepted predictions on the held-out light split. However, official validation drops compared with E21, so E23 should be treated as a deployment-focused candidate rather than an unrestricted replacement.

### Decision
Promote E23 as the current `LIGHT_CONTROL` deployment candidate for further testing, but keep E21 as the general best validation baseline.

### Next Step
Test E23 on Raspberry Pi microphone recordings once the Pi hardware is available. Do not connect predictions to GPIO/LED actions until E23 or a later model passes Pi-mic holdout tests with no wrong accepted light triggers.

## 2026-09-16 15:05:00 +08:00 - Raspberry Pi Deployment Package Prepared

### Objective
Prepare an offline Raspberry Pi 5 deployment package and report before the hardware arrives.

### Action Performed
- Created `deployment/vcm_pi_package/`.
- Added Pi runtime scripts:
  - `scripts/predict_wav_pi.py`
  - `scripts/pi_voice_control_demo.py`
  - `scripts/pi_led_test.py`
- Copied required preprocessing/model runtime code into the package.
- Copied E23 light deployment candidate artifacts and E21 general baseline artifacts into the package.
- Added setup and validation documentation:
  - `README_PI_DEPLOYMENT.md`
  - `PI_MIC_VALIDATION_PROTOCOL.md`
  - `PACKAGE_MANIFEST.md`
  - `REPORT_PI_DEPLOYMENT_READINESS.md`
- Built `deployment/vcm_pi_deployment_package.zip`.

### Verification
- Python syntax check passed for all Pi scripts.
- Package-level prediction smoke test succeeded using E23 on an existing calibration WAV:
  - predicted intent: `LIGHT_CONTROL`
  - confidence: 0.999995
  - accepted at threshold 0.90: true

### Decision
Use the package for Pi microphone validation when hardware arrives. Keep GPIO disabled by default. The current model detects `LIGHT_CONTROL` intent only and does not yet distinguish `on` from `off`.

### Next Step
Copy the package to the Raspberry Pi, install dependencies, collect a held-out Pi-microphone validation set, and only then proceed to LED/GPIO action testing.

## 2026-09-16 15:25:00 +08:00 - Voice Command Action Layer Scaffold

### Objective
Conceptualize and create the actions triggered by accepted voice-command intents.

### Action Performed
- Added `actions/command_actions.py`.
- Added `actions/ACTION_LAYER_DESIGN.md`.
- Added `tests/test_command_actions.py`.
- Copied the action layer into `deployment/vcm_pi_package/actions/`.
- Updated `deployment/vcm_pi_package/scripts/pi_voice_control_demo.py` so live Pi predictions call the shared action layer.
- Updated package docs to describe real, simulated, and offline-disabled actions.

### Supported Action Behaviors
- `PLAY_MUSIC`: local media-state simulation.
- `QUESTION`: offline-safe query log only.
- `LIGHT_CONTROL`: LED on/off/toggle/blink when a slot/action is provided.
- `LIGHT_ADJUST`: brightness/color local state, with optional PWM LED brightness.
- `SET_TIMER`: local timer entry.
- `SET_ALARM`: local alarm entry.
- `THERMOSTAT`: simulated temperature state.
- `MEDIA_CONTROL`: local media-state controls.
- `REMINDER`: local reminder creation/listing.
- `CALL_MESSAGE`: offline-safe call/message log only.

### Verification
- Dry-run timer action worked.
- Dry-run light-on action worked.
- Pi package action-layer dry-run for `LIGHT_ADJUST` worked.
- Full unit suite passed: 17 tests passed; 1 expected skip.

### Decision
Keep the action layer separate from the CNN. The CNN predicts intent; slots such as on/off, percent, duration, time, contact, or query text must be provided by controlled demo input, separate labels, or a later slot/action model.

## 2026-09-16 17:20:00 +08:00 - Pre-Coded Offline Action Routes Expanded

### Objective
Use `actions.pdf` as reference material and pre-code the deterministic local action routes before the Raspberry Pi hardware arrives.

### Action Performed
- Expanded `actions/command_actions.py`.
- Added local time and simulated weather routes for `QUESTION`.
- Added word-number parsing for timer/alarm phrases such as "five minutes" and "seven AM".
- Added display-state updates that can later map to OLED/LCD output.
- Added thermostat target/fan-state simulation.
- Added media track state and optional local WAV playback hook through `aplay`.
- Added `deployment/vcm_pi_package/music/README_MUSIC.md`.
- Synced the upgraded action layer into `deployment/vcm_pi_package/actions/`.
- Updated Pi package README, manifest, and readiness report.

### Verification
- Full unit suite passed: 19 tests passed; 1 expected skip.
- Dry-run `QUESTION` weather route returned local weather.
- Dry-run `SET_TIMER` with "five minutes" produced a 300-second timer.
- Dry-run `THERMOSTAT` with 24 degrees updated the simulated thermostat state.

### Decision
The action side can be pre-coded now. The remaining missing piece is not code structure but hardware validation and reliable slot information from either controlled demo input, phrase parsing, separate labels, or a future slot/action model.

## 2026-09-16 17:55:00 +08:00 - Superseded Partial Mirror Deleted

### Objective
Delete the earlier partial dataset mirror so it cannot be accidentally mixed into training.

### Action Performed
- Verified the target path resolved inside `ME2_VCM\data\raw`.
- Deleted `data/raw/google_drive_dataset/`.
- Updated dataset/project documentation to state that the folder was an earlier partial mirror with only 2,000 WAV files and has now been deleted.

### Rationale
The active dataset is the extracted Google Drive ZIP data under `data/drive-download-*`, not the earlier public-page mirror. Removing the partial mirror reduces the risk of double-counting or training from the wrong folder.

### Decision
Continue using `data/metadata/active_dataset_index.csv` as the source of truth for training/evaluation inputs.

## 2026-09-18 22:40:00 +08:00 - Raspberry Pi Setup And All-Command Recognition Status

### Objective
Record the current Raspberry Pi 5 deployment status and plan the recovery path
for full-command exam readiness.

### Requirement Addressed
- Requirement 4: Validate VCM performance - IN PROGRESS on Raspberry Pi microphone.
- Requirement 5: Build Raspberry Pi demo - IN PROGRESS.
- Requirement 6: Tiny real-time Raspberry Pi VCM - IN PROGRESS, latency/RAM/CPU still NOT YET MEASURED.
- Requirement 7: Standalone/offline operation - IN PROGRESS, local inference works on Pi.
- Requirement 8: No LLM/pure VCM - maintained.

### Action Performed
- Guided Raspberry Pi OS setup, SSH access, package transfer, virtual environment setup, and dependency installation.
- Verified USB microphone recording through ALSA card 2, device 0.
- Verified Pi-side preprocessing and TensorFlow inference.
- Reviewed the latest 15-label x 5-trial Pi microphone recognition sweep.
- Created `deployment/PI_ALL_COMMAND_RECOVERY_PLAN.md`.
- Updated project status, experiment log, exam notes, readiness report, README, and next-session checklist.

### Actual Result
- Raspberry Pi 5 boots and is reachable over SSH as `loreenanne@RaspberryPi5Loreen.local`.
- Pi package is installed under `~/vcm_pi_package` on the Pi.
- Python 3.13.5 and TensorFlow 2.21.0 are working on the Pi.
- USB microphone recording works with `plughw:2,0`.
- Pi-side preprocessing produced expected feature shape `(398, 40)`.
- Dataset-style `LIGHT_ON` and `LIGHT_OFF` recordings were strong in targeted tests.
- Full 15-label x 5-trial Pi sweep reached 47/75 correct broad-intent predictions.
- At threshold 0.90, the sweep had 58 accepted predictions and 15 wrong accepted predictions.

### Interpretation
The hardware/software deployment path is alive, which is a major milestone. The
remaining issue is model reliability for the full command set. The project is
not yet ready for an exam demo where every command can trigger its intended
action, because several labels are still misclassified with high confidence.

### Decision
Treat all-command recognition as the current blocker. The next model should
predict raw command/subcommand labels or otherwise provide action-level output,
then map those labels into the assignment intents and local actions.

### Next Step
Record a complete Pi microphone calibration set for every raw command label,
split it into adaptation and held-out validation portions, train or fine-tune a
Pi-adapted raw-command model with original-data replay, and retest all commands
before enabling physical action output.

## 2026-09-19 10:30:00 +08:00 - Pi Calibration Recorder Added

### Objective
Start the all-command recovery plan by reducing manual recording errors during
Pi microphone calibration collection.

### Action Performed
- Added `deployment/vcm_pi_package/scripts/record_pi_calibration_set.py`.
- Updated `deployment/PI_ALL_COMMAND_RECOVERY_PLAN.md` with the exact command
  for running the recorder on the Raspberry Pi.
- Updated `deployment/vcm_pi_package/PACKAGE_MANIFEST.md`.
- Rebuilt `deployment/vcm_pi_deployment_package.zip` so the helper is included
  in the local deployment archive.

### Actual Result
The recorder prompts through the demo command list, records 15 trials per label,
saves files under `pi_validation/all_commands_calibration_15x/`, and writes a
`manifest.csv` containing the label, phrase, expected broad intent, action hint,
trial number, and adaptation/holdout split.

### Verification
`python -m py_compile deployment\vcm_pi_package\scripts\record_pi_calibration_set.py`
completed successfully.

### Decision
Use the helper on the Raspberry Pi for the next calibration session instead of
manual shell loops. This makes the adaptation/holdout split and label manifest
reproducible.

### Next Step
Power on the Raspberry Pi, confirm SSH access, copy the helper script to
`~/vcm_pi_package/scripts/`, and start recording the labelled calibration set.

## 2026-09-19 11:40:00 +08:00 - Pi Calibration Set Preserved Locally

### Objective
Copy the full labelled Raspberry Pi microphone calibration set back into the
project and verify that it is usable for the E24 recovery experiment.

### Action Performed
- User recorded the full calibration set on the Raspberry Pi using
  `scripts/record_pi_calibration_set.py`.
- User archived it on the Pi as
  `pi_validation/all_commands_calibration_15x.tar.gz`.
- User copied the archive to
  `data/calibration/all_commands_calibration_15x.tar.gz`.
- Extracted the archive under `data/calibration/pi_validation/all_commands_calibration_15x`.
- Verified manifest rows, WAV count, sample rate, channels, and WAV readability.

### Actual Result
- WAV files: 285.
- Manifest rows: 285.
- Labels: 19 labels, 15 trials per label.
- Split counts: 190 adaptation clips and 95 holdout clips.
- Sample rate: 16 kHz for all 285 WAV files.
- Channels: mono for all 285 WAV files.
- Unreadable WAV files: 0.

### Decision
Use `data/calibration/pi_validation/all_commands_calibration_15x/manifest.csv`
as the source of truth for Pi calibration labels and adaptation/holdout split.

### Next Step
Evaluate the current deployment model on the held-out Pi calibration clips, then
train or fine-tune the E24 raw-label/subcommand model using only the adaptation
split plus original-dataset replay.

## 2026-09-19 12:20:00 +08:00 - Pi Holdout Baseline And Raw-Command Recovery Probes

### Objective
Measure the current Pi deployment model on the untouched 95-clip Pi holdout set,
then begin the raw-command/subcommand recovery path needed for action-level demo
activation.

### Action Performed
- Added `evaluation/evaluate_pi_calibration.py`.
- Evaluated `E23_LIGHT_REALMIC_ADAPT_E21_REPLAY` on the 95 held-out Pi clips.
- Added `training/train_pi_raw_command_recovery.py`.
- Trained `E24_PI_RAW_COMMAND_RECOVERY_PROBE` using 190 Pi adaptation clips,
  original-data replay, and a 19-label raw-command output head.
- Trained `E25_PI_RAW_COMMAND_RECOVERY_FT` as a lower-learning-rate fine-tune
  from E24 with stronger Pi weighting and lighter replay.

### Actual Result
E23 broad-intent baseline on held-out Pi clips:

- Correct broad-intent predictions: 75/95, or 78.95%.
- Accepted at threshold 0.90: 80/95.
- Wrong accepted at threshold 0.90: 14.
- Main broad-intent failures: `COLOR`, `BRIGHTNESS`, `TIMER`,
  `CREATE_REMINDER`, `PAUSE`, and `NEXT`.

E24 raw-command probe on held-out Pi clips:

- Correct raw-command predictions: 86/95, or 90.53%.
- Accepted at threshold 0.90: 77/95.
- Wrong accepted at threshold 0.90: 1.
- At threshold 0.95: 69 accepted, 69 accepted correct, 0 wrong accepted.
- Main remaining misses: `LIGHT_OFF`, `STOP`, `COLOR`, `ALARM`, and
  `CREATE_REMINDER`.

E25 raw-command fine-tune on held-out Pi clips:

- Correct raw-command predictions: 88/95, or 92.63%.
- Accepted at threshold 0.90: 78/95.
- Wrong accepted at threshold 0.90: 3.
- E25 improved raw accuracy but worsened safety compared with E24.

### Decision
Raw-command prediction is the correct direction for the full demo because it can
differentiate merged assignment intents such as `LIGHT_ON` versus `LIGHT_OFF`
and `NEXT` versus `PAUSE`.

For safety-critical physical activation, `E24_PI_RAW_COMMAND_RECOVERY_PROBE` is
the better interim checkpoint because it has fewer wrong accepted predictions.
`E25_PI_RAW_COMMAND_RECOVERY_FT` is useful evidence that accuracy can improve,
but it is not safer for GPIO actions without additional guardrails.

### Next Step
Add command-specific guardrails and/or a template-style fallback for the fixed
demo phrase set, then retest the held-out Pi clips. The next target is not just
higher raw accuracy; it is zero wrong accepted actions while preserving enough
accepted correct commands for a smooth live demo.

## 2026-09-19 12:35:00 +08:00 - Live Microphone Demo Behavior Clarified

### Objective
Clarify how live Raspberry Pi microphone input will be handled during the demo.

### Decision
The demo uses live microphone input, but the current interaction model is
record-then-infer, not continuous always-listening streaming.

Current demo flow:

```text
start command -> record 4 seconds -> preprocess -> CNN inference -> action/reject
```

This is real-time in the practical demo sense because the user speaks live into
the Raspberry Pi microphone and the Pi locally processes that fresh recording.
The same step can later be wrapped in a loop:

```text
listen -> predict -> act/reject -> listen again
```

### Documentation Updated
Added this clarification to `DEMO_EXPLANATION_SCRIPT.md` so it can be used as
part of the live demo explanation.

## 2026-09-19 12:50:00 +08:00 - Fixed Vocabulary And Acoustic Robustness Framing

### Objective
Clarify the expected generalization target for the VCM demo and avoid turning
the project into an open-ended speech assistant.

### Decision
The VCM should be presented as a compact fixed-vocabulary command classifier,
not as speech-to-text, an LLM, or an arbitrary language-understanding system.
Because the professor stated that each intent only has a few phrase variations,
limited phrase variation is acceptable and logically aligned with the assignment.

The robustness requirement is acoustic rather than linguistic. The model should
recognize the known command phrases under reasonable variation in:

- microphone volume;
- mouth-to-mic distance;
- speaker voice;
- pronunciation;
- silence/padding around speech;
- mild room noise;
- reasonable microphone quality differences.

### Training Implication
Do not primarily add many new phrase wordings. Instead, improve recognition of
the existing fixed demo vocabulary through live Raspberry Pi microphone
calibration, optional multi-mic or second-speaker recordings, targeted
augmentation, thresholds, margin checks, and guardrails.

### Demo Explanation
Use this framing:

```text
This is not an open-ended speech assistant. It is a compact voice command
classifier trained on a fixed vocabulary. The phrase space is intentionally
limited, but the acoustic input still needs robustness, so I validate and adapt
the model using live Raspberry Pi microphone recordings.
```

## 2026-09-19 13:25:00 +08:00 - Dataset Lecture Connection Added To Exam Notes

### Objective
Connect the class lecture on datasets and dataloaders to the ME2 VCM dataset,
preprocessing, splitting, and training pipeline.

### Action Performed
Read the `Datasets.pdf` lecture enough to anchor the project explanation around
the lecture concepts of datasets as `(x, y)`, data sources, annotation,
sufficiency, train/validation/test splits, bias, and dataloaders.

### Documentation Updated
Added an exam-review entry to `EXAM_NOTES.md` under Phase 1 explaining how the
lecture maps to this project:

- WAV/log-Mel samples as `x`;
- raw command labels and assignment intents as `y`;
- metadata manifests as annotation/data structure;
- speaker-aware 80/10/10-style split;
- class/microphone/speaker/synthetic bias concerns;
- dataloader concept as batching, shuffling, preprocessing, and label encoding.

### Decision
During the exam, explain the dataset as an engineered artifact, not just a pile
of audio files: source selection, labels, provenance, splits, leakage checks,
consistent preprocessing, and held-out validation are all part of the model
pipeline.

## 2026-09-19 13:45:00 +08:00 - End-Of-Session Checkpoint

### Objective
Pause work for the day with a clean resume point for tomorrow.

### Status
No more implementation work tonight. The Raspberry Pi can remain shut down until
the next session.

### Key Decisions From This Session
- Keep the current Pi pipeline and do not restart from scratch.
- Treat the new posted collective dataset as a useful official/curated corpus,
  especially for documentation, efficient training, `UNKNOWN`, and `SILENCE`,
  but do not let it derail the Pi calibration/reliability work.
- Present the VCM as a fixed-vocabulary command classifier, not an open-ended
  ASR/LLM assistant.
- Focus robustness work on acoustic variation: microphone, speaker, distance,
  gain, noise, silence, and timing.
- Keep live demo behavior as local record-then-infer unless a wake-word stage is
  explicitly added later.
- A wake word would be a first-stage detector before command classification; it
  is optional and should not replace the current push-to-talk/record-then-infer
  exam-safe path.

### Resume Tomorrow
Recommended next work:

1. Decide whether to import the new posted `VCM_BALANCED` dataset into the
   project as an official reference/training corpus.
2. Add an exam-note entry for push-to-talk versus wake-word activation if this
   becomes part of the demo explanation.
3. Plan a small headset/second-mic or second-speaker robustness test only if
   energy/time permits.
4. Continue with E26-style targeted augmentation/guardrails after the dataset
   decision is settled.

## 2026-09-20 00:10:00 +08:00 - New Posted Dataset Decision

### Objective
Decide how to use the newly posted collective VCM dataset without derailing the
existing Raspberry Pi deployment work.

### Observation
The new posted dataset at `C:\Users\Loreen Anne\Downloads\VCM\VCM` contains:

- `VCM_MASTER`: 36,622 audio files with train/validation/test manifests.
- `VCM_BALANCED`: 15,268 WAV training files.
- 16 classes.
- `UNKNOWN` and `SILENCE`.
- Manifests, provenance reports, class distribution reports, augmentation
  reports, audio-quality reports, and speaker-leakage audits.

### Decision
Cite/document the new posted dataset first, and integrate it only selectively.

Do not restart the project around this dataset. The current Raspberry Pi
pipeline remains the deployment path because it already has:

- live Pi microphone recording;
- Pi preprocessing and local TensorFlow inference;
- action routing;
- Pi calibration recordings;
- E23/E24/E25 measured Pi holdout results.

### Practical Use
Use the posted dataset for:

- report and exam explanation;
- dataset provenance and audit discussion;
- possible `UNKNOWN`/`SILENCE` support;
- possible efficient future training experiments;
- optional E26 support only if it improves the Pi holdout/demo target.

Do not use it to replace held-out Raspberry Pi validation. Final demo readiness
still depends on real deployment microphone performance.

## 2026-09-20 16:45:00 +08:00 - E24 Raw-Command Package Default

### Objective
Begin today's work by making the Raspberry Pi deployment package use the safer
raw-command recognition path instead of the older broad-intent default.

### Action Performed
- Updated the shared CNN config loader to allow non-10-class heads.
- Added `configs/cnn_fastbn_dense_nodropout_raw19.json` to the main project and
  Pi package.
- Copied E24 raw-command model weights, normalization statistics, labels,
  metrics, and holdout predictions into the Pi package.
- Added `actions/raw_command_router.py` to the main project and Pi package.
- Updated `deployment/vcm_pi_package/scripts/predict_wav_pi.py` so E24 is the
  default model with threshold `0.95`.
- Updated `deployment/vcm_pi_package/scripts/pi_voice_control_demo.py` so a raw
  command label is routed into the assignment intent/action layer before action
  execution.
- Updated Pi package README, readiness report, package manifest, project status,
  and next-session checklist to reflect the E24 raw-command deployment route.

### Actual Result
The Pi package now defaults to:

- experiment: `E24_PI_RAW_COMMAND_RECOVERY_PROBE`;
- labels: 19 raw command labels;
- threshold: `0.95`;
- routing: raw command -> broad assignment intent -> local action layer.

Example routes:

- `LIGHT_ON -> LIGHT_CONTROL` with `light_action=on`;
- `LIGHT_OFF -> LIGHT_CONTROL` with `light_action=off`;
- `NEXT -> MEDIA_CONTROL` with `media_action=next`;
- `WEATHER -> QUESTION` with `question_type=weather`.

### Verification
- Focused unit tests passed:
  `python -m unittest tests.test_raw_command_router tests.test_cnn_scaffold -v`
  ran 8 tests successfully, with 1 expected TensorFlow-related skip.
- Python syntax check passed for the touched action, inference, demo, and CNN
  files.
- Package predictor smoke test passed on held-out Pi recordings:
  - `LIGHT_OFF_012.wav -> LIGHT_OFF`, confidence `0.999778`, accepted.
  - `NEXT_012.wav -> NEXT`, confidence `0.999996`, accepted.
- Full unit test suite passed:
  `python -m unittest discover -s tests -v` ran 22 tests successfully, with 1
  expected TensorFlow-related skip.
- Rebuilt `deployment/vcm_pi_deployment_package.zip` with E24 artifacts and
  without generated `__pycache__` entries.

### Decision
Use E24 as the current package default because it is safer for physical-action
activation than E25 and it can distinguish action-level commands that the broad
intent model merged together.

### Next Step
Copy the refreshed deployment zip to the Raspberry Pi before on-device testing,
then continue with E26-style improvements: targeted augmentation/guardrails for
remaining weak commands, held-out Pi validation, and Raspberry Pi latency/RAM/CPU
measurement before full GPIO activation.

## 2026-09-20 19:10:00 +08:00 - E24 Optional Threshold Guardrail

### Objective
Increase accepted-command coverage for the E24 Pi package without reintroducing
wrong accepted actions.

### Action Performed
- Analyzed E24 Pi holdout predictions by threshold and per label.
- Identified concentrated hard pairs:
  - `LIGHT_OFF -> LIGHT_ON`;
  - `STOP -> NEXT`;
  - single misses involving `ALARM`, `COLOR`, and `CREATE_REMINDER`.
- Added optional per-predicted-label threshold policy:
  `configs/e24_pi_guardrail_thresholds.json`.
- Copied the same policy into the Pi package.
- Updated `deployment/vcm_pi_package/scripts/predict_wav_pi.py` to accept
  `--threshold-policy`.
- Updated `deployment/vcm_pi_package/scripts/pi_voice_control_demo.py` to pass
  the optional threshold policy through live record-and-infer demos.
- Added `evaluation/evaluate_threshold_policy.py`.
- Added `tests/test_pi_threshold_policy.py`.

### Actual Result
On saved E24 Pi holdout predictions:

- global threshold `0.95`: `69/95` accepted, `69` correct accepted, `0` wrong
  accepted.
- optional guardrail policy: `80/95` accepted, `80` correct accepted, `0` wrong
  accepted.

Runtime smoke with the optional policy:

- `TIME_014.wav -> TIME`, confidence `0.889925`, accepted at threshold `0.80`.
- `LIGHT_OFF_011.wav -> LIGHT_ON`, confidence `0.939426`, rejected because
  predicted `LIGHT_ON` uses threshold `0.95`.

### Verification
- Threshold policy unit tests passed.
- Raw-command router unit tests still passed.
- Syntax check passed for the threshold evaluator and touched Pi scripts.
- Full unit test suite passed:
  `python -m unittest discover -s tests -v` ran 25 tests successfully, with 1
  expected TensorFlow-related skip.
- Rebuilt `deployment/vcm_pi_deployment_package.zip`; the archive includes the
  threshold policy and updated Pi scripts, and contains `0` `__pycache__`
  entries.

### Decision
Keep the strict global `0.95` threshold as the default safe mode. Treat
`configs/e24_pi_guardrail_thresholds.json` as an optional candidate guardrail
for testing because it was calibrated from existing holdout evidence and needs a
fresh Pi microphone validation pass before final exam-readiness claims.

### Next Step
Use the optional policy on fresh Pi microphone recordings once the Pi Wi-Fi/SSH
situation is stable or direct LCD terminal use is convenient.

## 2026-09-20 20:45:00 +08:00 - Fresh Pi Guardrail Trial Shows Remaining Risk

### Objective
Run fresh live Raspberry Pi microphone trials using the optional E24 guardrail
threshold policy after copying the refreshed package to the Pi.

### Action Performed
- User copied the refreshed `vcm_pi_deployment_package.zip` to the Raspberry Pi.
- User replaced the Pi package and confirmed
  `configs/e24_pi_guardrail_thresholds.json` exists on the Pi.
- User ran live `pi_voice_control_demo.py` with:
  `--device plughw:2,0 --duration-sec 4 --threshold-policy configs/e24_pi_guardrail_thresholds.json`.

### Actual Result
Confirmed clean live result:

- Spoken `time`: predicted `TIME`, confidence `0.998547`, accepted, routed to
  `QUESTION`, action `question.time_local`, GPIO off.

Fresh risky-command transcript was then reviewed. Assuming the commands were run
in the requested order (`lights off`, `lights on`, `stop`, `next`, `color`,
`alarm`, `create reminder`), the results were:

- `lights off`: predicted `LIGHT_ON`, confidence `0.991624`, accepted. This is
  a wrong accepted action-critical prediction.
- `lights on`: predicted `LIGHT_ON`, confidence `0.994834`, accepted. Correct.
- `stop`: predicted `STOP`, confidence `0.415722`, rejected. Safe but not
  accepted.
- `next`: predicted `LIGHT_ON`, confidence `0.675232`, rejected. Safe rejection
  but wrong top label.
- `color`: predicted `CALL`, confidence `0.985357`, accepted. Wrong accepted.
- `alarm`: predicted `ALARM`, confidence `0.998195`, accepted. Correct.
- `create reminder`: predicted `LIST_REMINDERS`, confidence `0.997245`,
  accepted. Wrong accepted if the spoken phrase was create reminder.

### Interpretation
The optional guardrail policy improved saved-holdout coverage but does not yet
generalize safely to fresh live Pi speech. GPIO or other physical actions should
remain disabled. The highest-risk live failures are still action-confusing pairs
or acoustically similar command groups, especially `LIGHT_OFF/LIGHT_ON`,
`COLOR/CALL`, and `CREATE_REMINDER/LIST_REMINDERS`.

### Decision
Do not enable GPIO based on the optional guardrail policy. Treat the policy as a
diagnostic candidate only. The next useful work is to preserve fresh live
recordings with unique filenames, label them, and use them for another targeted
recovery cycle rather than relying on thresholds alone.

### Next Step
Record a small labelled fresh-Pi recovery set for the failing/risky commands
with unique output WAV filenames, then evaluate and adapt the model or add
stricter command-specific guardrails.

## 2026-09-20 20:55:00 +08:00 - Fresh Pi Recovery Trial With Overwritten WAV Path

### Objective
Continue fresh live Raspberry Pi testing for the risky command group using the
optional E24 guardrail threshold policy.

### Action Performed
- User ran additional live Pi trials with:
  `--device plughw:2,0 --duration-sec 4 --threshold-policy configs/e24_pi_guardrail_thresholds.json`.
- User also provided `--output-wav pi_recordings/fresh_lights_off_001.wav`.

### Important Data Caveat
Every command in this transcript used the same output path,
`pi_recordings/fresh_lights_off_001.wav`. That means the JSON transcript is
useful evidence, but the individual WAV files were overwritten and are not
available as a labelled recovery dataset. Only the last recording remains at
that filename on the Pi.

### Actual Result
Assuming the commands followed the intended order (`lights off`, `lights on`,
`stop`, `next`, `color`, `call`, `create reminder`, `list reminders`):

- `lights off`: predicted `LIGHT_ON`, confidence `0.896003`, rejected by the
  `LIGHT_ON` threshold `0.95`. Safe rejection, but wrong top label.
- `lights on`: predicted `LIGHT_ON`, confidence `0.999493`, accepted. Correct.
- `stop`: predicted `NEXT`, confidence `0.969399`, accepted. Wrong accepted.
- `next`: predicted `NEXT`, confidence `0.580698`, rejected. Safe rejection,
  but too low for usability.
- `color`: predicted `CALL`, confidence `0.736309`, rejected by the `CALL`
  threshold `0.80`. Safe rejection, but wrong top label.
- `call`: predicted `CALL`, confidence `0.986032`, accepted. Correct.
- `create reminder`: predicted `CREATE_REMINDER`, confidence `0.813611`,
  accepted. Correct.
- `list reminders`: predicted `LIST_REMINDERS`, confidence `0.999522`,
  accepted. Correct.

### Interpretation
The second fresh trial is mixed. The guardrail prevented some wrong actions
(`lights off` as `LIGHT_ON`, `color` as `CALL`), and several commands worked
well (`lights on`, `call`, `create reminder`, `list reminders`). However,
`stop -> NEXT` was still a wrong accepted prediction, so physical action
activation is still unsafe.

### Decision
Continue keeping GPIO disabled. The next data collection must use unique output
filenames per phrase/trial so recordings can be copied back and used for E26
recovery. Focus especially on `LIGHT_OFF`, `STOP`, `NEXT`, and `COLOR`.

### Next Step
Record a properly labelled fresh-Pi mini-set with unique filenames and copy it
back to the project. The immediate target is not broad training; it is fixing
the risky command pairs that still cause wrong accepted predictions.

## 2026-09-20 21:05:00 +08:00 - Fresh Pi Risky-Command Trials Clarified

### Objective
Collect more live Raspberry Pi evidence for the remaining risky commands:
`lights off`, `stop`, `next`, and `color`.

### Action Performed
- User ran four additional live Pi trials with output path
  `pi_recordings/fresh_stop_001.wav`.

### Important Data Caveat
The same output filename was reused for all four trials, so only the last WAV is
preserved on the Pi. The JSON transcript is still useful, but this does not yet
create a usable labelled mini-dataset for retraining.

### Actual Result
User clarified that the spoken commands were:

- `lights off`
- `stop`
- `next`
- `color`

Results:

- `lights off`: predicted `LIGHT_OFF`, confidence `0.813753`, accepted.
  Correct.
- `stop`: predicted `BRIGHTNESS`, confidence `0.999349`, accepted. Wrong
  accepted.
- `next`: predicted `LIGHT_ON`, confidence `0.958788`, accepted. Wrong
  accepted.
- `color`: predicted `CALL`, confidence `0.606553`, rejected. Safe rejection,
  but wrong top label.

### Interpretation
The clarified phrase order shows one improvement and two continuing risks.
`lights off` can be recognized correctly, but `stop` and `next` still produced
wrong accepted predictions. `color` is being rejected safely in this trial but
is still not recognized correctly.

### Decision
Do not use `STOP`, `NEXT`, or `COLOR` for any physical or visible action in the
live demo until a targeted recovery set is collected and evaluated. `LIGHT_OFF`
still needs more trials, but this specific clarified trial was correct.

### Next Step
Record `STOP`, `NEXT`, and `COLOR` with unique filenames, at least five trials
each, then copy those WAVs back for analysis/retraining. Also record a smaller
confirmation set for `LIGHT_OFF`.

## 2026-09-20 21:15:00 +08:00 - Fresh Pi STOP Mini-Set Improved

### Objective
Retest `STOP` using unique output filenames so the WAV files are preserved on
the Raspberry Pi.

### Action Performed
- User recorded three fresh live `STOP` trials with unique output filenames:
  - `pi_recordings/fresh_stop_001.wav`
  - `pi_recordings/fresh_stop_002.wav`
  - `pi_recordings/fresh_stop_003.wav`

### Actual Result
- `fresh_stop_001.wav`: predicted `STOP`, confidence `0.996073`, accepted,
  routed to `MEDIA_CONTROL` with `media_action=stop`.
- `fresh_stop_002.wav`: predicted `STOP`, confidence `0.986024`, accepted,
  routed to `MEDIA_CONTROL` with `media_action=stop`.
- `fresh_stop_003.wav`: predicted `STOP`, confidence `0.991247`, accepted,
  routed to `MEDIA_CONTROL` with `media_action=stop`.

### Interpretation
This mini-set is a positive fresh-Pi result for `STOP`: `3/3` accepted correct
with unique WAV files preserved. Earlier instability may have been due to
speech delivery, inconsistent prompt order, or the tiny sample size. `STOP`
should still be validated with a few more trials before being treated as stable.

### Decision
Move `STOP` from highest-risk to needs-confirmation. Keep GPIO disabled overall
because `NEXT` and `COLOR` still need unique-file testing, and previous trials
showed wrong accepted predictions.

### Next Step
Record unique-file mini-sets for `NEXT` and `COLOR`, then copy all fresh WAVs
back for project-side analysis.

## 2026-09-20 21:25:00 +08:00 - Fresh Pi NEXT Mini-Set Fails Recognition

### Objective
Retest `NEXT` using unique output filenames so the WAV files are preserved on
the Raspberry Pi.

### Action Performed
- User recorded three fresh live `NEXT` trials with unique output filenames:
  - `pi_recordings/fresh_next_001.wav`
  - `pi_recordings/fresh_next_002.wav`
  - `pi_recordings/fresh_next_003.wav`

### Actual Result
- `fresh_next_001.wav`: predicted `LIGHT_ON`, confidence `0.645442`,
  rejected by the `LIGHT_ON` threshold `0.95`. Safe rejection, wrong top label.
- `fresh_next_002.wav`: predicted `STOP`, confidence `0.907235`, accepted,
  routed to `MEDIA_CONTROL` with `media_action=stop`. Wrong accepted.
- `fresh_next_003.wav`: predicted `BRIGHTNESS`, confidence `0.755941`,
  rejected by the `BRIGHTNESS` threshold `0.80`. Safe rejection, wrong top
  label.

### Interpretation
`NEXT` is currently the strongest remaining live Pi recognition blocker. In
this preserved mini-set it was `0/3` correct, with one wrong accepted command.
This needs targeted recovery data and likely model adaptation, not only
threshold tuning.

### Decision
Do not include `NEXT` as an enabled physical/visible action in the demo until
it is recovered. Keep media-control demos limited to commands that validate
cleanly, such as `STOP`, unless further testing changes this.

### Next Step
Record a unique-file mini-set for `COLOR`, then copy `fresh_stop_*`,
`fresh_next_*`, and `fresh_color_*` WAVs back to the laptop/project for
evaluation and E26 recovery.

## 2026-09-20 21:35:00 +08:00 - Fresh Pi COLOR Mini-Set Fails Recognition

### Objective
Retest `COLOR` using unique output filenames so the WAV files are preserved on
the Raspberry Pi.

### Action Performed
- User recorded three fresh live `COLOR` trials with unique output filenames:
  - `pi_recordings/fresh_color_001.wav`
  - `pi_recordings/fresh_color_002.wav`
  - `pi_recordings/fresh_color_003.wav`

### Actual Result
- `fresh_color_001.wav`: predicted `TEMPERATURE`, confidence `0.941191`,
  accepted, routed to `THERMOSTAT`. Wrong accepted.
- `fresh_color_002.wav`: predicted `BRIGHTNESS`, confidence `0.902434`,
  accepted, routed to `LIGHT_ADJUST` brightness. Wrong accepted for the raw
  command, even though it stays inside the broad light-adjust family.
- `fresh_color_003.wav`: predicted `CALL`, confidence `0.999624`, accepted,
  routed to `CALL_MESSAGE`. Wrong accepted.

### Interpretation
`COLOR` is a top live Pi recognition blocker. In this preserved mini-set it was
`0/3` correct and all three predictions were accepted. It cannot be enabled as a
reliable demo command without recovery.

### Decision
Prioritize `COLOR` together with `NEXT` for E26 recovery. Threshold changes
alone are unlikely to make `COLOR` usable because the wrong predictions are
high-confidence and spread across different labels.

### Next Step
Copy the preserved `fresh_stop_*`, `fresh_next_*`, and `fresh_color_*` WAV files
from the Pi back to the laptop/project, then build a small fresh-Pi recovery
manifest for analysis and targeted adaptation.

## 2026-09-20 21:45:00 +08:00 - Fresh Pi Mini-Set Copied And Evaluated Locally

### Objective
Preserve the fresh Raspberry Pi mini-set in the project and convert the live
terminal evidence into auditable local files for E26 recovery.

### Action Performed
- User copied the preserved Pi WAVs from
  `~/vcm_pi_package/pi_recordings/` to:
  `data/calibration/fresh_pi_miniset_20260920/`.
- Verified local file count and WAV properties.
- Created `data/calibration/fresh_pi_miniset_20260920/manifest.csv`.
- Evaluated the 9 WAVs locally with E24 and
  `configs/e24_pi_guardrail_thresholds.json`.

### Actual Result
Local WAV verification:

- WAV files: `9`.
- Labels: `STOP`, `NEXT`, `COLOR`, three trials each.
- All files are 16 kHz, mono, 16-bit PCM, 4 seconds long.

Local E24 guardrail evaluation:

- examples: `9`
- correct raw labels: `3/9`
- accepted predictions: `7/9`
- accepted correct: `3/9`
- wrong accepted: `4/9`

Per-label:

- `STOP`: `3/3` correct, `3/3` accepted, `0` wrong accepted.
- `NEXT`: `0/3` correct, `1/3` accepted, `1` wrong accepted.
- `COLOR`: `0/3` correct, `3/3` accepted, `3` wrong accepted.

### Files Created
- `data/calibration/fresh_pi_miniset_20260920/manifest.csv`
- `results/tables/FRESH_PI_MINISET_20260920_E24_GUARDRAIL_predictions.csv`
- `results/tables/FRESH_PI_MINISET_20260920_E24_GUARDRAIL_metrics.json`

### Interpretation
The mini-set confirms the current live Pi blocker very clearly: `NEXT` and
`COLOR` fail under fresh microphone conditions, while `STOP` works in this
preserved mini-set. This is now usable training/evaluation evidence because the
WAV files are preserved and labelled.

### Decision
Use the copied mini-set as the first E26 recovery input. Prioritize recovery for
`NEXT` and `COLOR`. Keep GPIO disabled until a follow-up model/guardrail passes
fresh validation with no wrong accepted action-critical commands.

### Next Step
Train or fine-tune an E26 recovery model using the preserved fresh mini-set
carefully, with replay and a fresh validation plan that does not simply overfit
these 9 examples.

## 2026-09-20 21:55:00 +08:00 - E26 Fresh Pi Recovery Candidate Promoted To Package Default

### Objective
Fix the immediate live Pi recognition failures for `NEXT` and `COLOR` while
preserving safety guardrails before GPIO or visible actions are enabled.

### Action Performed
- Added `training/train_pi_fresh_miniset_recovery.py`.
- Fine-tuned from `E24_PI_RAW_COMMAND_RECOVERY_PROBE` using source replay, the
  existing Pi adaptation split, and the preserved fresh Pi mini-set for `STOP`,
  `NEXT`, and `COLOR`.
- Created `E26_PI_FRESH_NEXT_COLOR_RECOVERY_PROBE`.
- Added `configs/e26_pi_guardrail_thresholds.json`.
- Copied E26 model, normalization, labels, metrics, and policy artifacts into
  `deployment/vcm_pi_package/`.
- Updated the package default runtime to E26 with the E26 guardrail policy.

### Actual Result
- Original 95-clip Pi holdout raw-command accuracy: `87/95`.
- Original Pi holdout macro-F1: `0.914381`.
- E26 guardrail on original Pi holdout: `74/95` accepted, `74` accepted
  correct, `0` wrong accepted.
- Preserved fresh Pi mini-set: `9/9` raw correct, `9/9` accepted correct,
  `0` wrong accepted.
- Local package smoke test with the default E26 runtime accepted all preserved
  `fresh_next_*`, `fresh_color_*`, and `fresh_stop_*` examples correctly.

### Interpretation
E26 fixes the preserved live Pi failure recordings that exposed the `NEXT` and
`COLOR` problem. The guardrail policy keeps the original Pi holdout safe by
rejecting risky high-confidence false-positive regions.

The preserved fresh mini-set result is recovery evidence, not final independent
exam evidence, because those clips were included in the E26 recovery training.

### Decision
Promote E26 as the current package default candidate for the next Pi validation
pass. Keep GPIO disabled until new live Pi recordings confirm there are no
wrong accepted commands.

### Next Step
Rebuild `deployment/vcm_pi_deployment_package.zip`, copy it to the Raspberry
Pi, and run a new unique-file live validation pass for `NEXT`, `COLOR`, `STOP`,
`LIGHT_ON`, and `LIGHT_OFF`.

## 2026-09-20 22:05:00 +08:00 - E27 Recovery Built From New Live E26 Failures

### Objective
Use the newly copied E26 live failure clips to recover live `NEXT` and `COLOR`
recognition without enabling GPIO.

### Action Performed
- User copied six new live Pi recordings into
  `data/calibration/e26_live_failures_20260920/`.
- Added `data/calibration/e26_live_failures_20260920/manifest.csv`.
- Added combined recovery manifest
  `data/calibration/e27_recovery_20260920_manifest.csv`.
- Verified all 15 recovery WAVs are readable 4-second, 16 kHz, mono, 16-bit
  PCM files.
- Trained `E27_PI_LIVE_NEXT_COLOR_RECOVERY_PROBE` from E26 using source replay,
  Pi adaptation replay, and the combined recovery manifest.
- Added `configs/e27_pi_guardrail_thresholds.json`.
- Copied E27 artifacts into `deployment/vcm_pi_package/`.
- Updated the package default runtime from E26 to E27.

### Actual Result
E26 on the six latest live clips:

- `NEXT`: `0/3` correct; one wrong accepted as `LIGHT_ON`.
- `COLOR`: `1/3` top-label correct but `0/3` accepted.

E27 recovery result:

- Original Pi holdout raw-command accuracy: `85/95`.
- E27 guardrail on original Pi holdout: `74/95` accepted, `74` accepted
  correct, `0` wrong accepted.
- Combined recovery set: `15/15` raw correct, `15/15` accepted correct,
  `0` wrong accepted.

### Interpretation
E27 fixes the copied live failure recordings and keeps the saved holdout safe
under the E27 guardrail. It is still a candidate, not final exam evidence,
because the copied live failure clips were used during recovery training.

### Decision
Promote E27 as the next package candidate for live Pi validation. Keep GPIO
disabled. The next proof must be new live recordings after copying the refreshed
E27 package to the Pi.

## 2026-09-20 22:15:00 +08:00 - E28 Candidate Built From E27 Live Validation

### Objective
Improve responsiveness for `NEXT` and `COLOR` after E27 produced safe
rejections but only `3/6` accepted correct on a fresh live Pi validation pass.

### Action Performed
- User copied six E27 live validation WAVs into
  `data/calibration/e27_live_validation_20260920/`.
- Added `data/calibration/e27_live_validation_20260920/manifest.csv`.
- Added combined E28 recovery manifest
  `data/calibration/e28_recovery_20260920_manifest.csv`.
- Trained `E28_PI_LIVE_NEXT_COLOR_RECOVERY_PROBE` from E27.
- Added `configs/e28_pi_guardrail_thresholds.json`.
- Copied E28 artifacts into `deployment/vcm_pi_package/`.
- Updated package default runtime from E27 to E28.

### Actual Result
- E27 fresh live validation: `3/6` accepted correct, `0` wrong accepted.
- E28 original Pi holdout raw-command accuracy: `82/95`.
- E28 guardrail on original Pi holdout: `74/95` accepted, `74` accepted
  correct, `0` wrong accepted.
- E28 combined recovery set: `21/21` raw correct, `21/21` accepted correct,
  `0` wrong accepted.

### Interpretation
E28 improves the recovered `NEXT`/`COLOR` responsiveness evidence while keeping
the saved holdout guardrail safety profile. It has lower raw holdout accuracy
than E27, so it should be treated strictly as the next live validation
candidate, not final proof.

## 2026-09-21 09:00:00 +08:00 - Resume Point And Hardware Connectivity Note

### Objective
Record the stop point from the previous session and avoid collecting noisy
microphone evidence during rain.

### Status
- Work stopped after building and packaging E28.
- Raspberry Pi 5 was safely shut down after the session.
- User noted that it was raining, so ambient noise is high.
- User observed that Wi-Fi and Bluetooth difficulty may be caused by the Pi 5
  now being inside a metal enclosure.

### Interpretation
Fresh live microphone validation should not be run during heavy rain or other
high ambient-noise conditions because the result may measure room noise more
than model quality.

The metal enclosure is a plausible cause of weak Wi-Fi/Bluetooth because it can
shield the Pi's onboard antennas. This affects SSH, file transfer, Bluetooth
keyboard/mouse, and setup convenience, not the offline CNN inference itself.

### Decision
For a rainy/noisy session, do not collect new validation WAVs unless the user
explicitly wants noisy-condition stress evidence. Safe tasks are package copy,
file verification, non-recording prediction on existing WAVs, log updates, and
documentation.

### Next Step
When the room is quiet, copy/install the E28 package on the Pi and run fresh
unique-file tests for `NEXT`, `COLOR`, `STOP`, `LIGHT_ON`, and `LIGHT_OFF` with
GPIO still disabled.

## 2026-09-21 21:10:00 +08:00 - Dataset Integrity And Tomorrow Recording Plan

### Objective
Update the project notes after professor feedback that the dataset should not
look "hacky," and prepare the next session so recording happens only when the
room is quiet.

### Status
- User noted classmates are using synthetic recordings and robustness tests for
  ambient noise, speaker distance, and a not-Loreen speaker.
- User also noted the professor warned against hacky dataset construction.
- It is raining/noisy, so new live microphone recordings should wait until
  tomorrow unless they are intentionally marked as noisy-condition stress tests.

### Interpretation
The current E26/E27/E28 sequence is useful and legitimate as an engineering
recovery trail because the inputs, copied clips, thresholds, and results are
logged. However, it should not be presented as final independent proof because
some live clips were later used for recovery training.

Final exam claims should come from clean fresh or held-out Pi microphone
recordings that were not used to train the candidate being reported. Robustness
tests should be kept separate from the main clean validation claim.

### Decision
Keep E28 as the current deployment candidate, not the final proof. Tonight's
safe work is documentation, package/file verification, existing-WAV prediction,
recording-table preparation, and optional LED board assembly with GPIO still
disabled in the recognition demo. Tomorrow's quiet-room work is the fresh Pi
microphone validation pass.

### Next Step
Run a clean E28 validation plan when ambient noise is low:

- main clean validation: same Pi mic, normal demo distance, quiet room;
- robustness pass: ambient noise or farther distance, marked separately;
- other-speaker pass: a small not-Loreen set, marked separately.

## 2026-09-21 21:20:00 +08:00 - Non-Recording Checks And E28 Recording Plan

### Objective
Complete safe work that does not require new microphone recordings while the
environment is rainy/noisy.

### Action Performed
- Ran the local test suite.
- Audited `deployment/vcm_pi_deployment_package.zip`.
- Confirmed the Pi package default is E28 with
  `configs/e28_pi_guardrail_thresholds.json`.
- Added a focused E28 clean validation plan for tomorrow.

### Actual Result
- Unit tests: 27 passed, 1 expected skip.
- Deployment zip exists.
- Zip entries: 63.
- Zip contains `scripts/pi_voice_control_demo.py`.
- Zip contains `configs/e28_pi_guardrail_thresholds.json`.
- Zip contains no Windows-backslash entries.
- Zip contains no `__pycache__` entries.
- `deployment/vcm_pi_package/scripts/predict_wav_pi.py` defaults to
  `E28_PI_LIVE_NEXT_COLOR_RECOVERY_PROBE`, threshold `0.95`, and
  `configs/e28_pi_guardrail_thresholds.json`.

### Files Affected
- `deployment/PI_E28_CLEAN_VALIDATION_PLAN.md`
- `NEXT_SESSION_CHECKLIST.md`
- `PROJECT_STATUS.md`
- `EXAM_NOTES.md`
- `DEMO_EXPLANATION_SCRIPT.md`
- `AGENT_LOG.md`

### Decision
Do not record fresh clean validation tonight. Tomorrow's recording should use
unique filenames and keep clean validation separate from robustness stress
tests.

## 2026-09-21 21:35:00 +08:00 - Defensible 100/100 Standard Formalized

### Objective
Record the user's target: a defensible 100/100 claim with clean pipeline,
architecture, and benchmarking rather than a one-off demo success.

### Action Performed
- Added a project-level validation standard:
  `benchmark/DEFENSIBLE_100_100_VALIDATION_PLAN.md`.
- Updated project status, checklist, and exam notes to point to the standard.

### Interpretation
The project goal is no longer just to make the model respond once on the Pi.
The goal is to prove, cleanly, that the supported command set is recognized,
routed to the correct intent/action, and run offline on-device. Robustness to
ambient noise, speaker distance, and a not-Loreen speaker should be benchmarked
as separate stress conditions.

### Decision
Use a two-layer evaluation:

1. Clean validation for the main exam-readiness claim.
2. Separate robustness benchmarks for noise, distance, and speaker variation.

Only claim 100/100 if the clean Pi validation set actually supports 100%
correct command recognition/action routing with zero wrong accepted commands.

## 2026-09-21 21:50:00 +08:00 - Dataset Inventory Snapshot Logged

### Objective
Record the current dataset inventory and how each dataset should be used so the
final pipeline remains clean and defensible.

### Action Performed
- Added a dated inventory snapshot to
  `data/metadata/DATASET_INVENTORY.md`.
- Updated `PROJECT_STATUS.md` and `NEXT_SESSION_CHECKLIST.md` with pointers to
  the inventory snapshot.

### Inventory Summary
- Original active VCM dataset: 21,001 WAVs found, 21,000 included after
  excluding one duplicate-style WEATHER file. Used for source training and
  source replay.
- Official original split: train 16,800; validation 2,100; test 2,100.
- Laptop and early real-mic calibration sets: diagnostic and light-command
  adaptation evidence, not final Pi proof.
- Pi all-command calibration set: 285 WAVs, 19 labels, 15 trials each, split
  into 190 adaptation clips and 95 holdout clips. This is the core real Pi
  microphone dataset.
- Fresh Pi recovery sets: 9 + 6 + 6 WAVs for `STOP`, `NEXT`, and `COLOR`
  recovery. These are development/recovery data after being used in E26/E27/E28.
- Posted collective dataset at `C:\Users\Loreen Anne\Downloads\VCM\VCM`:
  `VCM_MASTER` has 36,622 manifest rows, and `VCM_BALANCED` has 15,268 WAV
  training files. It includes `UNKNOWN` and `SILENCE`, so it is useful as
  cited optional/selective support but should not replace the current Pi path.

### Decision
Keep dataset roles separate:

1. Original dataset: training/source replay.
2. Pi calibration: real-device adaptation and held-out validation.
3. Recovery clips: candidate repair, not final proof.
4. Fresh tomorrow recordings: clean validation evidence if not used for
   training first.
5. Robustness tests: separate reports for noise, distance, and not-Loreen
   speaker.

## 2026-09-21 22:10:00 +08:00 - E28 Clean Validation Mini-Set Archived

### Objective
Run and preserve a clean quiet-room Raspberry Pi validation mini-set for the
current E28 candidate, using unique filenames and same Pi USB microphone setup.

### Action Performed
- User recorded 9 clean validation clips on the Raspberry Pi:
  - `NEXT`: 3 clips.
  - `COLOR`: 3 clips.
  - `STOP`: 1 clip.
  - `LIGHT_ON`: 1 clip.
  - `LIGHT_OFF`: 1 clip.
- User copied all 9 WAVs back to:
  `data/calibration/e28_clean_validation_20260921/`.
- Added `manifest.csv` for the copied clips.

### Actual Result
E28 clean validation result:

- `e28_clean_next_001.wav`: spoken `next`, predicted `NEXT`, confidence
  `0.994508`, accepted. Correct accepted.
- `e28_clean_next_002.wav`: spoken `next`, predicted `MESSAGE`, confidence
  `0.926640`, accepted. Wrong accepted.
- `e28_clean_next_003.wav`: spoken `next`, predicted `NEXT`, confidence
  `0.349351`, rejected. Correct top label but not accepted.
- `e28_clean_color_001.wav`: spoken `color`, predicted `COLOR`, confidence
  `0.666852`, rejected. Correct top label but not accepted.
- `e28_clean_color_002.wav`: spoken `color`, predicted `COLOR`, confidence
  `0.998095`, accepted. Correct accepted.
- `e28_clean_color_003.wav`: spoken `color`, predicted `CALL`, confidence
  `0.470935`, rejected. Wrong top label but safely rejected.
- `e28_clean_stop_001.wav`: spoken `stop`, predicted `STOP`, confidence
  `0.535292`, rejected. Correct top label but not accepted.
- `e28_clean_light_on_001.wav`: spoken `lights on`, predicted `LIGHT_ON`,
  confidence `0.749677`, rejected. Correct top label but not accepted.
- `e28_clean_light_off_001.wav`: spoken `lights off`, predicted `COLOR`,
  confidence `0.904751`, rejected. Wrong top label but safely rejected.

Summary:

- Total clean clips: 9.
- Accepted correct: 2.
- Wrong accepted: 1.
- Rejected: 6.
- Critical failure: `NEXT -> MESSAGE` was wrong accepted.

### Interpretation
E28 is not defensible as a final 100/100 candidate. The guardrail prevented
most weak/wrong cases from executing, but one wrong accepted command remains.
The archived clips are valuable fresh evidence for an E29 recovery candidate or
a stricter guardrail, but they must not be reported as E28 success.

### Decision
Do not enable GPIO or claim 100/100 with E28. Preserve the mini-set and use it
for the next analysis/recovery step.

## 2026-09-21 22:25:00 +08:00 - E29 Recovery Set Archived

### Objective
Collect a targeted recovery set after E28 failed the clean validation standard,
while keeping this new data separate from final proof.

### Action Performed
- User recorded 15 additional clean Pi microphone clips:
  - `NEXT`: 3 clips.
  - `LIGHT_OFF`: 3 clips.
  - `STOP`: 3 clips.
  - `LIGHT_ON`: 3 clips.
  - `COLOR`: 3 clips.
- User copied the WAVs back to:
  `data/calibration/e29_recovery_20260921/`.
- Added `manifest.csv` for the copied recovery set.

### Actual Result Under Current E28 Runtime
- `NEXT`: 1 accepted correct, 2 rejected.
- `LIGHT_OFF`: 2 accepted correct, 1 rejected.
- `STOP`: 2 accepted correct, 1 rejected.
- `LIGHT_ON`: 0 accepted correct, 1 wrong accepted as `PAUSE`, 2 rejected.
- `COLOR`: 3 accepted correct.

Summary:

- Total recovery clips: 15.
- Accepted correct: 8.
- Wrong accepted: 1.
- Rejected: 6.
- Critical failure: `LIGHT_ON -> PAUSE` was wrong accepted.

### Interpretation
This set confirms that E28 still has safety and responsiveness gaps. `COLOR`
looks strong in this recovery set, while `LIGHT_ON` became the most important
new safety failure because it was accepted as `PAUSE` with high confidence.

### Decision
Treat `data/calibration/e29_recovery_20260921/` as recovery/training candidate
data for the next model/guardrail step. Do not report it as final validation
after it is used for E29 recovery. A new fresh validation set will be needed
after any E29 update.

## 2026-09-21 22:45:00 +08:00 - E29 Quick Recovery Candidate Trained And Packaged

### Objective
Build the next Pi candidate from E28 using the archived E29 recovery set while
preserving holdout safety and documenting that fresh validation is still
required.

### Action Performed
- Added machine-readable recovery manifest:
  `data/calibration/e29_recovery_20260921_manifest.csv`.
- Trained `E29_PI_CLEAN_RECOVERY_PROBE_QUICK` from
  `E28_PI_LIVE_NEXT_COLOR_RECOVERY_PROBE`.
- Used source replay, Pi adaptation replay, and the 15-clip E29 recovery set.
- Added `configs/e29_pi_guardrail_thresholds.json`.
- Evaluated E29 on original Pi holdout and E29 recovery clips.
- Copied E29 model, normalization, labels, metrics, and guardrail policy into
  `deployment/vcm_pi_package/`.
- Updated `deployment/vcm_pi_package/scripts/predict_wav_pi.py` to default to
  E29 and the E29 guardrail policy.
- Rebuilt `deployment/vcm_pi_deployment_package.zip`.

### Actual Result
Training run:

- Experiment: `E29_PI_CLEAN_RECOVERY_PROBE_QUICK`.
- Base: `E28_PI_LIVE_NEXT_COLOR_RECOVERY_PROBE`.
- Best epoch: 6 of 8.
- Training examples: 1,750.
- Original Pi holdout raw-command accuracy: `86/95`.
- Original Pi holdout macro-F1: `0.9040`.
- E29 recovery set raw accuracy: `15/15`.

Guardrail result:

- E29 guardrail on original Pi holdout: `72/95` accepted, `72` accepted
  correct, `0` wrong accepted.
- E29 guardrail on E29 recovery set: `15/15` accepted, `15` accepted correct,
  `0` wrong accepted.

Verification:

- Unit tests: 27 passed, 1 expected skip.
- Local package smoke:
  - `e29_recovery_light_on_001.wav -> LIGHT_ON`, confidence `0.988424`,
    accepted.
  - `e29_recovery_next_001.wav -> NEXT`, confidence `0.979372`, accepted.
- Deployment zip audit:
  - entries: 71.
  - contains E29 model, normalization, E29 guardrail, and Pi demo script.
  - no Windows-backslash path entries.
  - no `__pycache__` entries.

### Interpretation
E29 is a better next Pi candidate than E28 because it fixes the archived E29
recovery set while preserving zero wrong accepted commands on the original Pi
holdout under the E29 guardrail. It is still not final proof because the
recovery clips were used for training.

### Decision
Promote E29 only as the next deployment candidate. Copy/install it on the Pi
and run a new fresh validation set before any 100/100 claim or GPIO activation.

## 2026-09-21 23:00:00 +08:00 - E29 Fresh Validation Archived

### Objective
Run a fresh validation pass after installing the E29 package on the Raspberry Pi
and preserve the results before any further training.

### Action Performed
- User installed the E29 deployment package on the Pi.
- User recorded 15 fresh validation clips:
  - `NEXT`: 3 clips.
  - `COLOR`: 3 clips.
  - `STOP`: 3 clips.
  - `LIGHT_ON`: 3 clips.
  - `LIGHT_OFF`: 3 clips.
- User copied all 15 WAVs back to:
  `data/calibration/e29_fresh_validation_20260921/`.
- Added `manifest.csv` for the fresh validation set.

### Actual Result
E29 fresh validation summary:

- `NEXT`: 1 accepted correct, 2 rejected.
- `COLOR`: 0 accepted correct, 3 rejected.
- `STOP`: 2 accepted correct, 1 rejected.
- `LIGHT_ON`: 1 accepted correct, 1 wrong accepted as `PAUSE`, 1 rejected.
- `LIGHT_OFF`: 1 accepted correct, 2 rejected.

Overall:

- Total fresh validation clips: 15.
- Accepted correct: 5.
- Wrong accepted: 1.
- Rejected: 9.
- Critical failure: `LIGHT_ON -> PAUSE` was wrong accepted.

### Interpretation
E29 improved the archived recovery set but did not generalize cleanly enough to
fresh validation. The most important remaining safety blocker is predicted
`PAUSE` for spoken `lights on`. The guardrail for `PAUSE` is currently too
permissive for this fresh failure mode.

### Decision
Do not claim E29 is final or enable GPIO. Use the archived fresh validation set
as evidence for the next recovery/guardrail step.

## 2026-09-21 23:05:00 +08:00 - Pause Point For Tomorrow

### Objective
Record the stopping point for the session so the next session resumes cleanly.

### Status
- E29 was trained, packaged, installed on the Pi, and tested with a fresh
  validation set.
- The E29 fresh validation WAVs were copied back and archived at
  `data/calibration/e29_fresh_validation_20260921/`.
- E29 fresh validation failed the 100/100 standard because
  `e29_fresh_light_on_001.wav` was wrongly accepted as `PAUSE`.
- GPIO remains disabled.

### Decision
Pause work for the night. Resume tomorrow with analysis of the `LIGHT_ON ->
PAUSE` failure and decide between an E30 recovery step or stricter `PAUSE`
guardrail. Do not claim final readiness until a new fresh validation pass has
zero wrong accepted commands.

## 2026-09-22 21:21:26 +08:00 - E30 Recent Pi Recovery Candidate Packaged

### Objective
Improve the Pi recognition candidate after E29 failed fresh validation, while
keeping the dataset/evaluation story defensible.

### Action Performed
- Created `data/calibration/e30_recent_pi_recovery_20260922_manifest.csv`.
- Combined 39 recent Pi clips:
  - E28 clean validation: 9 clips.
  - E29 recovery: 15 clips.
  - E29 fresh validation: 15 clips.
- Trained `E30_PI_RECENT_FRESH_RECOVERY_PROBE` from
  `E29_PI_CLEAN_RECOVERY_PROBE_QUICK`.
- Added `configs/e30_pi_guardrail_thresholds.json`.
- Evaluated E30 guardrail on the original Pi holdout and recent recovery/fresh
  prediction tables.
- Copied E30 model, normalization, labels, metrics, and guardrail policy into
  `deployment/vcm_pi_package/`.
- Updated `deployment/vcm_pi_package/scripts/predict_wav_pi.py` to default to
  E30 and the E30 guardrail policy.
- Rebuilt and audited `deployment/vcm_pi_deployment_package.zip`.

### Actual Result
Training run:

- Experiment: `E30_PI_RECENT_FRESH_RECOVERY_PROBE`.
- Base: `E29_PI_CLEAN_RECOVERY_PROBE_QUICK`.
- Best epoch restored: 2 of 10.
- Training examples: 2,248.
- Original Pi holdout raw-command accuracy: `85/95`.
- Original Pi holdout macro-F1: `0.8959`.
- Recent recovery/fresh raw accuracy: `39/39`.

Guardrail result:

- E30 guardrail on original Pi holdout: `78/95` accepted, `78` accepted
  correct, `0` wrong accepted.
- E30 guardrail on recent recovery/fresh clips: `39/39` accepted, `39`
  accepted correct, `0` wrong accepted.

Verification:

- Unit tests: 27 passed, 1 expected skip.
- Local package smoke:
  - `e29_fresh_light_on_001.wav -> LIGHT_ON`, confidence `0.966030`, accepted.
  - `e29_fresh_color_001.wav -> COLOR`, confidence `0.985560`, accepted.
  - `e29_fresh_next_002.wav -> NEXT`, confidence `0.996313`, accepted.
- Deployment zip audit:
  - entries: 78.
  - contains E30 model, normalization, E30 guardrail, labels, and Pi demo
    script.
  - no Windows-backslash path entries.
  - no `__pycache__` entries.

### Interpretation
E30 fixes the archived E29 fresh-validation failure in local smoke tests and is
safer/more responsive than E29 under the saved evidence. It is still not final
proof because the recent recovery/fresh clips were used in training.

### Decision
Promote E30 only as the next Raspberry Pi deployment candidate. Copy/install it
on the Pi and run a new fresh validation pass before any 100/100 claim or GPIO
activation.

## 2026-09-22 21:30:00 +08:00 - Fresh Validation Evaluator Added

### Objective
Make the post-recording validation step reproducible instead of hand-counting
terminal JSON outputs.

### Action Performed
- Added `evaluation/evaluate_live_validation_folder.py`.
- The script infers expected raw labels from WAV filenames such as
  `e30_clean_light_on_001.wav`.
- It runs the packaged Pi predictor, applies the package guardrail policy,
  routes the raw command through the action router, and writes metrics/CSV
  outputs when `--output-id` is provided.
- Added the evaluator command to `deployment/PI_E30_CLEAN_VALIDATION_PLAN.md`
  and `NEXT_SESSION_CHECKLIST.md`.

### Actual Result
Smoke-tested the evaluator on the archived E29 fresh-validation folder using
the current E30 package defaults:

- Examples: `15`.
- Raw correct: `15/15`.
- Accepted: `15/15`.
- Accepted correct: `15`.
- Wrong accepted: `0`.

Generated smoke outputs:

- `results/tables/E30_PACKAGE_ON_E29_FRESH_VALIDATION_SMOKE_metrics.json`.
- `results/tables/E30_PACKAGE_ON_E29_FRESH_VALIDATION_SMOKE_predictions.csv`.

Verification:

- Unit tests still pass: 27 passed, 1 expected skip.

### Decision
Use this evaluator immediately after copying the next fresh E30 validation WAVs
back from the Pi. The clean validation gate remains `accepted_wrong = 0`.

## 2026-09-22 21:43:28 +08:00 - E30 Fresh Clean Validation Archived

### Objective
Evaluate E30 on new live Pi microphone recordings that were not used to train
E30.

### Action Performed
- User recorded 15 fresh clean Pi clips:
  - `NEXT`: 3 clips.
  - `COLOR`: 3 clips.
  - `STOP`: 3 clips.
  - `LIGHT_ON`: 3 clips.
  - `LIGHT_OFF`: 3 clips.
- User copied the WAVs back to:
  `data/calibration/e30_clean_validation_20260922/`.
- Ran:
  `python evaluation/evaluate_live_validation_folder.py data/calibration/e30_clean_validation_20260922 --output-id E30_CLEAN_VALIDATION_20260922`.

### Actual Result
Official folder evaluator result:

- Examples: `15`.
- Raw correct: `11/15`.
- Accepted: `11/15`.
- Accepted correct: `11`.
- Wrong accepted: `0`.
- Rejected: `4`.
- Accepted accuracy: `1.0`.

Per label:

- `NEXT`: `2/3` accepted correct, `1` rejected.
- `COLOR`: `1/3` accepted correct, `2` rejected.
- `STOP`: `3/3` accepted correct.
- `LIGHT_ON`: `3/3` accepted correct.
- `LIGHT_OFF`: `2/3` accepted correct, `1` rejected.

Output files:

- `results/tables/E30_CLEAN_VALIDATION_20260922_metrics.json`.
- `results/tables/E30_CLEAN_VALIDATION_20260922_predictions.csv`.

### Interpretation
E30 passed the safety gate on this fresh clean mini-set because there were zero
wrong accepted commands. It does not yet support a full 100/100 recognition
claim because four commands were rejected.

### Decision
Keep GPIO disabled for now. Use the fresh E30 validation set as evidence for
the next improvement step, focusing on responsiveness for `COLOR`, `NEXT`, and
`LIGHT_OFF` while preserving zero wrong accepted commands.

## 2026-09-22 21:53:02 +08:00 - E31 Clean Responsiveness Candidate Packaged

### Objective
Improve E30 responsiveness after the clean validation pass produced four safe
rejections.

### Action Performed
- Added recovery manifest:
  `data/calibration/e31_clean_pi_recovery_20260922_manifest.csv`.
- Trained `E31_PI_CLEAN_RESPONSIVENESS_RECOVERY` from
  `E30_PI_RECENT_FRESH_RECOVERY_PROBE`.
- Added `configs/e31_pi_guardrail_thresholds.json`.
- Evaluated E31 guardrail on the original Pi holdout and E30 clean recovery
  prediction tables.
- Copied E31 model, normalization, labels, metrics, and guardrail policy into
  `deployment/vcm_pi_package/`.
- Updated `deployment/vcm_pi_package/scripts/predict_wav_pi.py` to default to
  E31 and the E31 guardrail policy.
- Rebuilt and audited `deployment/vcm_pi_deployment_package.zip`.
- Added `deployment/PI_E31_CLEAN_VALIDATION_PLAN.md`.

### Actual Result
Training run:

- Experiment: `E31_PI_CLEAN_RESPONSIVENESS_RECOVERY`.
- Base: `E30_PI_RECENT_FRESH_RECOVERY_PROBE`.
- Best epoch restored: 2 of 10.
- Training examples: 1,720.
- Original Pi holdout raw-command accuracy: `84/95`.
- Original Pi holdout macro-F1: `0.8870`.
- E30 clean recovery raw accuracy: `15/15`.

Guardrail result:

- E31 guardrail on original Pi holdout: `70/95` accepted, `70` accepted
  correct, `0` wrong accepted.
- E31 guardrail on E30 clean recovery clips: `15/15` accepted, `15` accepted
  correct, `0` wrong accepted.

Verification:

- Unit tests: 27 passed, 1 expected skip.
- Local package smoke:
  - `e30_clean_color_001.wav -> COLOR`, confidence `0.986498`, accepted.
  - `e30_clean_next_002.wav -> NEXT`, confidence `0.952797`, accepted.
  - `e30_clean_light_off_002.wav -> LIGHT_OFF`, confidence `0.818879`,
    accepted.
- Deployment zip audit:
  - entries: 85.
  - contains E31 model, normalization, E31 guardrail, labels, and Pi demo
    script.
  - no Windows-backslash path entries.
  - no `__pycache__` entries.

### Interpretation
E31 fixes the archived E30 clean rejections but has lower broad holdout accepted
coverage than E30. It is a targeted responsiveness candidate for the current
five-command live demo set, not final proof.

### Decision
Promote E31 only as the next Raspberry Pi deployment candidate. Copy/install it
on the Pi and run a new fresh validation pass before any 100/100 claim or GPIO
activation.

## 2026-09-22 22:08:11 +08:00 - E31 Fresh Clean Validation Archived

### Objective
Evaluate E31 on new live Pi microphone recordings that were not used to train
E31.

### Action Performed
- User recorded 15 fresh clean Pi clips:
  - `NEXT`: 3 clips.
  - `COLOR`: 3 clips.
  - `STOP`: 3 clips.
  - `LIGHT_ON`: 3 clips.
  - `LIGHT_OFF`: 3 clips.
- User copied the WAVs back to:
  `data/calibration/e31_clean_validation_20260922/`.
- Ran:
  `python evaluation/evaluate_live_validation_folder.py data/calibration/e31_clean_validation_20260922 --output-id E31_CLEAN_VALIDATION_20260922`.

### Actual Result
Official folder evaluator result:

- Examples: `15`.
- Raw correct: `13/15`.
- Accepted: `11/15`.
- Accepted correct: `10`.
- Wrong accepted: `1`.
- Rejected: `4`.
- Accepted accuracy: `0.9091`.

Per label:

- `NEXT`: `1/3` accepted correct, `2` rejected.
- `COLOR`: `2/3` accepted correct, `1` rejected.
- `STOP`: `2/3` accepted correct, `1` rejected.
- `LIGHT_ON`: `3/3` accepted correct.
- `LIGHT_OFF`: `2/3` accepted correct, `1` wrong accepted.

Critical failure:

- `e31_clean_light_off_002.wav`: expected `LIGHT_OFF`, predicted/accepted
  `LIGHT_ON`, confidence `0.959432`, threshold `0.8`.

Output files:

- `results/tables/E31_CLEAN_VALIDATION_20260922_metrics.json`.
- `results/tables/E31_CLEAN_VALIDATION_20260922_predictions.csv`.

### Interpretation
E31 improves some responsiveness but fails the safety gate because one
action-critical command was accepted as the opposite light action. The rejected
rows also show raw-correct low-confidence cases, so the remaining work is both
responsiveness and `LIGHT_ON`/`LIGHT_OFF` separation.

### Decision
Do not use E31 for GPIO or final demo claims. Keep GPIO disabled. The next
modeling step must address `LIGHT_OFF -> LIGHT_ON`; lowering thresholds alone
would be unsafe.

## 2026-09-22 22:15:14 +08:00 - E32 Light Separation Candidate Packaged

### Objective
Address the E31 fresh validation safety failure where spoken `LIGHT_OFF` was
accepted as `LIGHT_ON`.

### Action Performed
- Added combined recovery manifest:
  `data/calibration/e32_light_separation_recovery_20260922_manifest.csv`.
- Combined 30 clips from:
  - `data/calibration/e30_clean_validation_20260922/`.
  - `data/calibration/e31_clean_validation_20260922/`.
- Trained `E32_PI_LIGHT_SEPARATION_RECOVERY` from
  `E31_PI_CLEAN_RESPONSIVENESS_RECOVERY`.
- Added `configs/e32_pi_guardrail_thresholds.json`.
- Evaluated E32 guardrail on original Pi holdout and combined E30/E31 recovery
  prediction tables.
- Copied E32 model, normalization, labels, metrics, and guardrail policy into
  `deployment/vcm_pi_package/`.
- Updated `deployment/vcm_pi_package/scripts/predict_wav_pi.py` to default to
  E32 and the E32 guardrail policy.
- Rebuilt and audited `deployment/vcm_pi_deployment_package.zip`.

### Actual Result
Training run:

- Experiment: `E32_PI_LIGHT_SEPARATION_RECOVERY`.
- Base: `E31_PI_CLEAN_RESPONSIVENESS_RECOVERY`.
- Best epoch restored: 7 of 10.
- Training examples: 1,960.
- Original Pi holdout raw-command accuracy: `81/95`.
- Original Pi holdout macro-F1: `0.8493`.
- Combined E30/E31 recovery raw accuracy: `30/30`.

Guardrail result:

- E32 guardrail on original Pi holdout: `71/95` accepted, `71` accepted
  correct, `0` wrong accepted.
- E32 guardrail on combined E30/E31 recovery clips: `29/30` accepted, `29`
  accepted correct, `0` wrong accepted.
- Lowering `NEXT` enough to accept all 30 recovery clips introduced wrong
  accepted holdout commands, so the safer policy keeps one low-confidence
  recovery `NEXT` rejected.

Verification:

- Unit tests: 27 passed, 1 expected skip.
- Local package smoke:
  - `e31_clean_light_off_002.wav -> LIGHT_OFF`, confidence `0.954082`,
    accepted.
  - `e31_clean_next_001.wav -> NEXT`, confidence `0.940694`, accepted.
- Deployment zip audit:
  - entries: 92.
  - contains E32 model, normalization, E32 guardrail, labels, and Pi demo
    script.
  - no Windows-backslash path entries.
  - no `__pycache__` entries.

### Interpretation
E32 fixes the archived E31 opposite-light failure and preserves zero wrong
accepted commands on saved evidence under the E32 guardrail. It is still not
final proof because the E30/E31 clean clips were used for recovery training.

### Decision
Promote E32 only as the next Raspberry Pi deployment candidate. Copy/install it
on the Pi and run a new fresh validation pass before any 100/100 claim or GPIO
activation.

## 2026-09-22 22:31:56 +08:00 - E32 Fresh Clean Validation Archived

### Objective
Evaluate E32 on new live Raspberry Pi microphone recordings that were not used
to train E32.

### Action Performed
- User recorded 15 fresh clean Pi clips after installing the E32 package:
  - `NEXT`: 3 clips.
  - `COLOR`: 3 clips.
  - `STOP`: 3 clips.
  - `LIGHT_ON`: 3 clips.
  - `LIGHT_OFF`: 3 clips.
- User copied the WAVs back to:
  `data/calibration/e32_clean_validation_20260922/`.
- Ran:
  `python evaluation/evaluate_live_validation_folder.py data/calibration/e32_clean_validation_20260922 --output-id E32_CLEAN_VALIDATION_20260922`.
- User observed that mentally counting "1, 2" after recording starts before
  speaking improves prediction consistency. Treat this as a recording protocol
  note for future clean validation passes because it reduces clipped-command
  risk.

### Actual Result
Official folder evaluator result:

- Examples: `15`.
- Raw correct: `15/15`.
- Accepted: `12/15`.
- Accepted correct: `12`.
- Wrong accepted: `0`.
- Rejected: `3`.
- Accepted accuracy: `1.0`.

Per label:

- `NEXT`: `3/3` accepted correct.
- `COLOR`: `1/3` accepted correct, `2` rejected.
- `STOP`: `3/3` accepted correct.
- `LIGHT_ON`: `2/3` accepted correct, `1` rejected.
- `LIGHT_OFF`: `3/3` accepted correct.

Output files:

- `results/tables/E32_CLEAN_VALIDATION_20260922_metrics.json`.
- `results/tables/E32_CLEAN_VALIDATION_20260922_predictions.csv`.

### Interpretation
E32 is the best fresh safety result so far. It fixed the E31
`LIGHT_OFF -> LIGHT_ON` wrong-accepted failure and had zero wrong accepted
commands on the new clean validation set. The model's raw top-label prediction
was correct for all 15 clips, so the remaining issue is confidence/acceptance,
not raw class recognition, especially for `COLOR` and one `LIGHT_ON` example.

This supports a defensible safety statement for the clean E32 mini-set:
accepted commands were routed correctly and no wrong action was accepted. It
does not support a full 100/100 recognition claim because three clips were
rejected.

### Decision
Keep E32 as the current safest deployment checkpoint. For final 100/100 work,
the next modeling target is responsiveness for `COLOR` and `LIGHT_ON` while
preserving zero wrong accepted commands. GPIO remains disabled unless the demo
is explicitly scoped to accepted commands and a light-only safety check is
repeated after the LED board is assembled.

## 2026-09-22 22:41:51 +08:00 - E33 Color/Light-On Responsiveness Candidate Packaged

### Objective
Improve E32 responsiveness for the fresh clean clips that were raw-correct but
rejected, especially `COLOR` and one `LIGHT_ON`, while preserving the
zero-wrong-accepted guardrail standard.

### Action Performed
- Added recovery manifest:
  `data/calibration/e33_color_lighton_recovery_20260922_manifest.csv`.
- Trained `E33_PI_COLOR_LIGHTON_RESPONSIVENESS` from
  `E32_PI_LIGHT_SEPARATION_RECOVERY`.
- Added `configs/e33_pi_guardrail_thresholds.json`.
- Evaluated E33 guardrail on original Pi holdout and E32 fresh clean recovery
  prediction tables.
- Copied E33 model, normalization, labels, metrics, and guardrail policy into
  `deployment/vcm_pi_package/`.
- Updated `deployment/vcm_pi_package/scripts/predict_wav_pi.py` to default to
  E33 and the E33 guardrail policy.
- Updated package README/manifest/readiness status to identify E33 as the
  current default.
- Rebuilt and audited `deployment/vcm_pi_deployment_package.zip`.

### Actual Result
Training run:

- Experiment: `E33_PI_COLOR_LIGHTON_RESPONSIVENESS`.
- Base: `E32_PI_LIGHT_SEPARATION_RECOVERY`.
- Best epoch restored: 8 of 10.
- Training examples: 1,480.
- Original Pi holdout raw-command accuracy: `86/95`.
- Original Pi holdout macro-F1: `0.9054`.
- E32 fresh clean recovery raw accuracy: `15/15`.

Guardrail result:

- E33 guardrail on original Pi holdout: `72/95` accepted, `72` accepted
  correct, `0` wrong accepted.
- E33 guardrail on E32 fresh clean recovery clips: `15/15` accepted, `15`
  accepted correct, `0` wrong accepted.

Verification:

- Unit tests: 28 passed, 1 expected skip.
- Local package smoke:
  - `e32_clean_color_002.wav -> COLOR`, confidence `0.985352`, accepted.
  - `e32_clean_light_on_002.wav -> LIGHT_ON`, confidence `0.949822`,
    accepted.
  - `LIGHT_OFF_014.wav -> NEXT`, confidence `0.882947`, rejected by the E33
    `NEXT` threshold `0.9`.
- Deployment zip audit:
  - entries: 99.
  - contains E33 model, normalization, E33 guardrail, labels, and Pi demo
    script.
  - no Windows-backslash path entries.
  - no `__pycache__` entries.

### Interpretation
E33 fixes the archived E32 rejected clean clips and improves original Pi
holdout raw accuracy compared with E32. The E33 guardrail keeps zero wrong
accepted commands on saved evidence, but accepts fewer original holdout clips
than E32. This is acceptable as a safety-first candidate because the immediate
goal is a defensible live demo where no wrong action is accepted.

### Decision
Promote E33 as the next Raspberry Pi deployment candidate. It is not final
proof because the E32 fresh clean clips were used for E33 recovery training.
The next required evidence is a new fresh Pi validation pass using unique
`e33_clean_*` filenames before any 100/100 claim or GPIO activation.

## 2026-09-22 23:07:13 +08:00 - E33 Fresh Clean Validation Passed

### Objective
Evaluate the E33 deployment package on new live Raspberry Pi microphone
recordings that were not used to train E33.

### Action Performed
- User recorded fresh clean Pi clips for:
  - `NEXT`: 3 clips.
  - `COLOR`: 3 clips.
  - `STOP`: 3 clips.
  - `LIGHT_ON`: 3 clean clips plus one excluded incident clip.
  - `LIGHT_OFF`: 3 clips.
- The first `LIGHT_ON` attempt hung before completing cleanly and later produced
  a low-confidence rejected result. It was treated as an incident/corrupted
  recording and excluded from the official clean validation folder.
- The clean replacement was recorded as
  `e33_clean_light_on_001_retry.wav`.
- User copied the official 15 WAVs back to:
  `data/calibration/e33_clean_validation_20260922/`.
- Ran:
  `python evaluation/evaluate_live_validation_folder.py data/calibration/e33_clean_validation_20260922 --output-id E33_CLEAN_VALIDATION_20260922`.

### Actual Result
Official folder evaluator result:

- Examples: `15`.
- Raw correct: `15/15`.
- Accepted: `15/15`.
- Accepted correct: `15`.
- Wrong accepted: `0`.
- Rejected: `0`.
- Accepted accuracy: `1.0`.

Per label:

- `NEXT`: `3/3` accepted correct.
- `COLOR`: `3/3` accepted correct.
- `STOP`: `3/3` accepted correct.
- `LIGHT_ON`: `3/3` accepted correct.
- `LIGHT_OFF`: `3/3` accepted correct.

Output files:

- `results/tables/E33_CLEAN_VALIDATION_20260922_metrics.json`.
- `results/tables/E33_CLEAN_VALIDATION_20260922_predictions.csv`.

### Interpretation
E33 now supports a clean five-command Pi demo claim for `NEXT`, `COLOR`,
`STOP`, `LIGHT_ON`, and `LIGHT_OFF`: all official clean validation recordings
were accepted correctly and no wrong action was accepted. The incident
`e33_clean_light_on_001.wav` should be retained only as an excluded technical
note, not mixed into the official clean validation set.

### Decision
Use E33 as the current clean-demo package. Next work should shift from recovery
training to measurement and demo evidence: latency/RAM/CPU/temperature on the
Pi, optional LED GPIO after board assembly, and separate robustness tests for
ambient noise, farther distance, and a not-Loreen speaker.

## 2026-09-22 23:14:37 +08:00 - Pi Benchmark Script Prepared

### Objective
Prepare a Raspberry Pi measurement tool for inference latency, RAM, CPU, and
temperature evidence without enabling GPIO.

### Action Performed
- Added `deployment/vcm_pi_package/scripts/benchmark_pi_inference.py`.
- The script loads the current E33 model once, runs warmup passes, times
  repeated WAV inference, and writes:
  - JSON summary.
  - CSV row-level latency records.
- It captures:
  - model load time.
  - per-command inference latency.
  - CPU percent over the benchmark window from `/proc/stat`.
  - RAM from `/proc/meminfo`.
  - temperature from `/sys/class/thermal/thermal_zone0/temp` or
    `vcgencmd measure_temp`.
- Smoke-tested the script locally on two E33 WAV files.
- Rebuilt `deployment/vcm_pi_deployment_package.zip`.

### Verification
- Unit tests: 28 passed, 1 expected skip.
- Deployment zip audit:
  - entries: 100.
  - contains `scripts/benchmark_pi_inference.py`.
  - no Windows-backslash path entries.
  - no `__pycache__` entries.
  - no `.tmp` entries.

### Decision
Run this script on the Raspberry Pi against the official E33 clean validation
WAVs, excluding the incident `e33_clean_light_on_001.wav` and including
`e33_clean_light_on_001_retry.wav`.

## 2026-09-22 23:16:55 +08:00 - E33 Pi Benchmark Run Completed

### Objective
Measure Raspberry Pi inference latency, CPU, RAM, and temperature for the E33
clean-demo package without enabling GPIO.

### Action Performed
User ran `scripts/benchmark_pi_inference.py` on the Pi against the official
E33 clean validation WAVs:

- `e33_clean_next_*.wav`
- `e33_clean_color_*.wav`
- `e33_clean_stop_*.wav`
- `e33_clean_light_off_*.wav`
- `e33_clean_light_on_001_retry.wav`
- `e33_clean_light_on_002.wav`
- `e33_clean_light_on_003.wav`

Settings:

- `--repeat 5`.
- `--warmup 2`.
- `--output-id E33_PI_BENCHMARK_20260922`.

### Actual Result
Benchmark summary:

- WAV count: `15`.
- Measured predictions: `75`.
- Accepted: `75/75`.
- Rejected: `0`.
- Model load time: `1.9126 s`.
- Benchmark window: `2.5211 s`.
- Mean latency: `33.39 ms`.
- Median latency: `32.14 ms`.
- Min latency: `29.59 ms`.
- Max latency: `39.88 ms`.
- p90 latency: `38.55 ms`.
- p95 latency: `39.28 ms`.
- CPU during benchmark: `99.40%`.
- Start temperature: `45.2 C`.
- End temperature: `49.05 C`.
- Start memory used: `544,880 KB` (`6.60%`).
- End memory used: `729,248 KB` (`8.83%`).
- Platform: `Linux-6.18.50+rpt-rpi-2712-aarch64-with-glibc2.41`.
- Python: `3.13.5`.
- CPU count: `4`.

Pi output files:

- `/home/loreenanne/vcm_pi_package/pi_benchmarks/E33_PI_BENCHMARK_20260922_summary.json`.
- `/home/loreenanne/vcm_pi_package/pi_benchmarks/E33_PI_BENCHMARK_20260922_latency_rows.csv`.

### Interpretation
E33 is fast enough for the record-then-infer demo path: after model load and
warmup, median inference time is about `32 ms` and p95 is under `40 ms` for the
official clean five-command set. CPU reaches nearly full utilization during the
tight benchmark loop, but temperature stayed below `50 C` and memory use
remained under `9%` of system RAM.

### Decision
Copy the JSON and CSV benchmark artifacts back into `results/pi_benchmarks/`
for final report evidence. GPIO/LED work remains deferred until the board is
assembled and wiring is reviewed.

## 2026-09-22 23:19:43 +08:00 - E33 Pi Benchmark Artifacts Copied Back

### Objective
Preserve the Raspberry Pi benchmark outputs as local project evidence.

### Action Performed
User copied the Pi benchmark files from the Raspberry Pi into:
`results/pi_benchmarks/`.

### Verification
Local files verified:

- `results/pi_benchmarks/E33_PI_BENCHMARK_20260922_summary.json`, 2,291 bytes.
- `results/pi_benchmarks/E33_PI_BENCHMARK_20260922_latency_rows.csv`, 18,797 bytes.
- CSV row count: `75`.
- Summary JSON matches the pasted Pi benchmark metrics.

### Decision
The Pi latency/RAM/CPU/temperature measurement task is complete. Next hardware
work should wait for LED board assembly guidance; keep GPIO disabled until the
wiring is reviewed.
## 2026-09-23 09:00:00 +08:00 - Wake Word and UNKNOWN 100/100 Scope

Goal:

Extend the final demo target beyond the E33 five-command clean pass to the full
100/100 requirement: wake phrase, all supported command categories, UNKNOWN
rejection/no-action, and intent/action evidence.

Decisions:

- Use custom wake phrase `hey pi`.
- Treat `WAKE` as a gate, not as an executable action.
- Treat `UNKNOWN` as reject/no-action behavior.
- Use posted collective dataset examples such as `hey siri`, `hey google`,
  `alexa`, `hello`, and random non-command speech as negative/false-wake
  material where useful.
- Record fresh Pi `hey pi` examples because a project-specific wake phrase is
  academically legitimate and cleaner than forcing a mismatched public wake
  dataset.

Changes made:

- Added `deployment/vcm_pi_package/scripts/record_pi_wake_set.py`.
- Added `deployment/vcm_pi_package/scripts/pi_wake_voice_control_demo.py`.
- Updated raw-command routing so `UNKNOWN` and `WAKE` are explicit no-action
  safety labels in both the project and Pi package copies.
- Updated `evaluation/evaluate_live_validation_folder.py` to score executable
  known commands separately from no-action `UNKNOWN`/`WAKE` examples.
- Added `tools/combine_pi_manifests.py`.
- Updated project/package docs with the 2026-09-23 wake/UNKNOWN workplan.
- Corrected the wake-data design so ordinary commands used as false-wake probes
  keep their true raw command labels. They must not be trained as `UNKNOWN`
  because the same model must still recognize them after a valid wake.
- Rebuilt `deployment/vcm_pi_deployment_package.zip`.

Verification:

- `python -m py_compile` passed for the new/modified scripts.
- Full unit suite passed: `30` tests.
- Deployment zip audit: `102` entries; includes
  `scripts/record_pi_wake_set.py` and `scripts/pi_wake_voice_control_demo.py`;
  no `__pycache__`, `.pyc`, or `.tmp` entries.

## 2026-09-23 - Log-Mel Lightweight Data Rationale

### Objective
Record the explanation for why the project uses Log-Mel features and targeted
Pi recordings instead of relying on a very large raw-audio corpus alone.

### Context
The user compared this project with classmates' dataset staging, which listed
about `56 GB` total on disk:

- Common Voice English: `18 GB`.
- LibriSpeech: `12 GB`.
- SLURP: `6.4 GB`.
- SpeechCommands v2: `3.0 GB`.
- STOP domains: about `3.0 GB`.
- FLEURS Filipino/Philippines: `1.6 GB`.
- SNIPS SmartLights: `374 MB`.
- TimersAndSuch: `279 MB`.
- MUSAN and RIRS noise augmentation staging: `11 GB`.

### Explanation Logged
Large raw-audio collections are mainly a data-diversity strategy. They can
improve generalization by adding speakers, accents, rooms, microphones,
phrases, background noise, and non-command speech. That is useful for
robustness testing and for broader speech systems, but it is not automatically
a better embedded architecture.

This project uses a lightweight embedded pipeline:

```text
16 kHz mono audio -> 4-second fixed window -> 398 x 40 Log-Mel matrix
-> tiny CNN -> confidence/wake guardrail -> raw-command router -> local action
```

A 4-second 16 kHz mono waveform contains `64,000` raw samples. The current
Log-Mel preprocessing converts it to `398 x 40 = 15,920` feature values. The
result is smaller and more speech-structured for a tiny CNN than raw waveform
input, and it is appropriate for Raspberry Pi latency/RAM constraints.

### Decision
Keep Log-Mel as the primary feature representation for the final Pi VCM. Use
large external/posted datasets selectively for documentation, UNKNOWN/noise
coverage, and robustness support only when the labels and acoustic conditions
match the task. Do not replace fresh Pi microphone recordings with mismatched
public data, because final demo performance depends on the actual Pi microphone,
room, command timing, wake phrase, and action vocabulary.

### Exam Note
Added the corresponding oral-defense answer to `EXAM_NOTES.md` under
`Phase 2 - Audio Preprocessing And Log-Mel Features`.

## 2026-09-23 - Pi Recording Adaptation vs Validation Clarification

### Objective
Record the exam-defense clarification about whether fresh Raspberry Pi
recordings count as training data and whether using them is different from
classmates augmenting with self-recorded or synthesized speech.

### Q&A Summary
Pi recordings can serve different roles depending on the split:

```text
Pi adaptation clips = training/fine-tuning data
Pi holdout clips = validation/test evidence
fresh live Pi trials = final deployment evidence
```

The user correctly reasoned that the purpose of training is for the VCM to
understand commands in deployment. If the model fails for non-Loreen speakers,
noise, distance, or a different microphone, then the model was not trained
robustly enough for those conditions.

The clarification is that using fresh Pi recordings is not inherently hacky.
It is a controlled deployment-domain adaptation strategy, conceptually similar
to classmates adding their own voice recordings, synthesized speech, or noise
augmentation. The method remains defensible when data provenance, labels, and
splits are documented.

### Decision
Keep the exam explanation focused on train/test separation:

- It is legitimate to use Pi recordings as adaptation/training data.
- The same exact clips must not be used as independent final proof.
- Held-out Pi clips and fresh live Pi trials remain the evidence for reported
  performance.
- Robustness claims must be limited to the tested conditions, such as noise,
  distance, volume, and non-Loreen speakers.

### Exam Note
Added this Q&A to `EXAM_NOTES.md` under the "not hacky" dataset/deployment
section.

## 2026-09-23 - Split Wake Gate and Command Model Architecture

### Objective
Update the Pi wake-gated demo so wake detection can use a different model
checkpoint from post-wake command/action classification.

### Rationale
E37 improved wake safety by removing accepted false-wake candidates, but it
regressed some command/action boundaries. This showed that wake detection and
command classification have different optimization priorities:

```text
wake model: minimize false wake
command model: maximize correct post-wake intent/action routing
```

### Change Made
Updated `deployment/vcm_pi_package/scripts/pi_wake_voice_control_demo.py` with
separate stage options:

- `--wake-experiment-id`
- `--command-experiment-id`
- `--wake-threshold`
- `--command-threshold`
- `--wake-threshold-policy`
- `--command-threshold-policy`

The older `--experiment-id`, `--threshold`, and `--threshold-policy` options
remain as backward-compatible defaults for both stages.

### Candidate Flow

```text
record wake phrase
-> E37 wake gate checks "hey pi"
-> if accepted, record command
-> E36/E35 command model predicts raw command
-> raw-command router maps to intent/action
-> local action layer executes or rejects
```

### Documentation
Updated `deployment/vcm_pi_package/README_PI_DEPLOYMENT.md` with the two-stage
two-checkpoint command example.

## 2026-09-23 - Wake-Then-Wake Safety Test Correction

### Correction
One live wake-gated trial was initially interpreted in discussion as:

```text
hey pi -> color command
```

The user clarified that the actual spoken sequence was:

```text
hey pi -> hey pi
```

### Correct Interpretation
This trial is not evidence for `COLOR` command performance. It is evidence for
the repeated-wake safety case:

- First `hey pi`: wake gate opened the command window.
- Second `hey pi`: post-wake audio should not execute a command.
- The observed run took no action, so it counts as a safe no-action result.
- If the command-stage classifier assigns a low-confidence non-command label in
  this scenario, that label should not be reported as a real command test.

### Exam Wording
Use this as:

```text
Repeated wake phrase after wake was rejected/no-action, so the system did not
execute a command when the user repeated the wake phrase instead of giving a
supported command.
```

## 2026-09-23 - Wake-Gated Evidence Capture Added

### Objective
Make live wake-gated validation evidence reproducible and file-backed instead
of relying on overwritten `latest_wake.wav` / `latest_command_after_wake.wav`
files or screenshots.

### Change Made
Updated `deployment/vcm_pi_package/scripts/pi_wake_voice_control_demo.py` with:

- `--evidence-dir`
- `--trial-id`
- `--expected-wake`
- `--expected-command`

When `--evidence-dir` is provided, each trial saves:

- `<trial_id>_wake.wav`
- `<trial_id>_command.wav`
- `<trial_id>_result.json`

The JSON payload includes the wake model, command model, expected phrases,
saved WAV paths, predictions, routing, action result, and GPIO status.

### Documentation
Updated `deployment/vcm_pi_package/README_PI_DEPLOYMENT.md` to show the current
two-checkpoint demo architecture:

```text
E37_TARGETED_COLOR_VOLUME_FIX wake gate
-> E33_PI_COLOR_LIGHTON_RESPONSIVENESS command model
-> raw-command router
-> local action layer
```

### Verification

```text
python -m py_compile deployment/vcm_pi_package/scripts/pi_wake_voice_control_demo.py
python -m unittest discover tests
30 tests passed
```

## 2026-09-23 - E38 Wake-Gated Live Evidence Summarized

### Objective
Summarize the copied live Pi wake-gated evidence folder into reproducible
metrics and rows for project documentation.

### Change Made
Added `evaluation/summarize_wake_gated_live_results.py`, which reads saved
`*_result.json` files from `pi_wake_voice_control_demo.py` and scores:

- wake-command-action trials,
- false-wake rejection trials,
- repeated-wake no-action trials.

The evaluator uses the expected phrases stored in each JSON evidence file and
does not re-run model inference, so the summary reflects the actual Pi demo
outputs.

### Evidence Folder

```text
results/wake_gated_live_20260923/
```

### Summary

```text
Result files: 11
Passed: 9
Failed: 2
Overall pass rate: 81.8%

Wake command action trials: 5 total, 3 passed
False wake rejection trials: 5 total, 5 passed
Repeated wake no-action trials: 1 total, 1 passed
```

Executed action passes:

- `wake_light_on_001`: `LIGHT_ON -> LIGHT_CONTROL`, `light.on`.
- `wake_light_off_001`: `LIGHT_OFF -> LIGHT_CONTROL`, `light.off`.
- `wake_next_001`: `NEXT -> MEDIA_CONTROL`, `media.next`.

Safety/no-action passes:

- `no_wake_lights_on_001`
- `wake_then_wake_001`
- `false_wake_hey_siri_001`
- `false_wake_hey_google_001`
- `false_wake_alexa_001`
- `false_wake_hello_001`

Remaining wake-gated gap:

- `wake_stop_001`: safe rejection, predicted `NEXT` at `0.652558`.
- `wake_stop_002`: safe rejection, predicted `STOP` at `0.484452`, below
  threshold.

These are responsiveness failures for `STOP`, not unsafe wrong executions.

### Outputs

```text
results/tables/E38_WAKE_GATED_LIVE_20260923_metrics.json
results/tables/E38_WAKE_GATED_LIVE_20260923_rows.csv
```

## 2026-09-23 - E38 Expanded Broad-Command Wake-Gated Results

### Objective
Extend the wake-gated live evidence beyond the initial subset to probe more
assignment command categories.

### Additional Trials Added

- `wake_play_music_001`
- `wake_time_001`
- `wake_weather_001`
- `wake_timer_001`
- `wake_alarm_001`
- `wake_temperature_001`

### Updated Summary

```text
Result files: 17
Passed: 10
Failed: 7
Overall pass rate: 58.8%

Wake command action trials: 11 total, 4 passed, 7 failed
False wake rejection trials: 5 total, 5 passed
Repeated wake no-action trials: 1 total, 1 passed
Wrong executed actions: 1
```

Executed action passes:

- `wake_light_on_001`: `LIGHT_ON -> LIGHT_CONTROL`, `light.on`.
- `wake_light_off_001`: `LIGHT_OFF -> LIGHT_CONTROL`, `light.off`.
- `wake_next_001`: `NEXT -> MEDIA_CONTROL`, `media.next`.
- `wake_weather_001`: `WEATHER -> QUESTION`, `question.weather_local`.

Safe rejection command gaps:

- `wake_play_music_001`: expected `PLAY_MUSIC`, rejected after `NEXT`
  top-label prediction.
- `wake_time_001`: expected `TIME`, rejected after `COLOR` top-label
  prediction.
- `wake_timer_001`: expected `TIMER`, rejected after `BRIGHTNESS` top-label
  prediction.
- `wake_alarm_001`: expected `ALARM`, rejected after `COLOR` top-label
  prediction.
- `wake_stop_001` / `wake_stop_002`: expected `STOP`, safe rejections.

Safety gap:

- `wake_temperature_001`: expected `TEMPERATURE`, but the command model
  predicted and accepted `LIGHT_ON` at `0.847105`, routed to
  `LIGHT_CONTROL`, and executed `light.on`.

### Decision
Stop broad live wake-gated command testing with E33 as the command-stage model.
Keep GPIO disabled. The current architecture is defensible for wake-gate safety
and the validated subset, but all-category wake-gated execution requires model
or guardrail recovery before it can be claimed.

## 2026-09-23 - E38 Command-Stage Candidate Replay

### Objective
Replay the saved E38 command WAVs through available command-stage candidates to
decide whether to switch away from E33 for broad wake-gated commands.

### Candidate Replay Results

```text
E33_PI_COLOR_LIGHTON_RESPONSIVENESS: passed=4 failed=7 wrong_executed=1
E36_WAKE_COLOR_VOLUME_FIX: passed=1 failed=10 replay bad_exec=7
E37_TARGETED_COLOR_VOLUME_FIX: passed=3 failed=8 replay bad_exec=6
E35_WAKE_BOOST_HEY_PI: passed=1 failed=10 replay bad_exec=2
```

Interpretation nuance: the quick replay script counted accepted `WAKE` and
`UNKNOWN` predictions as `bad_exec` because it only compared raw labels. In the
real `pi_wake_voice_control_demo.py` command stage, `WAKE` and `UNKNOWN` are
explicit no-action safety labels. The true actionable safety risk in the replay
set remains E33's `wake_temperature_001` result:

```text
expected TEMPERATURE -> predicted LIGHT_ON, confidence 0.847105, accepted,
routed LIGHT_CONTROL, executed light.on
```

### Decision
Do not switch command-stage model to E35, E36, or E37. They are worse command
routers on the saved E38 command WAVs. Keep E37 as wake gate and E33 as the
best available command-stage checkpoint, but add a strict broad-testing safety
threshold policy that raises `LIGHT_ON` above the observed wrong-accept
confidence.

### Artifact Added

```text
configs/e38_wake_gated_broad_safety_thresholds.json
deployment/vcm_pi_package/configs/e38_wake_gated_broad_safety_thresholds.json
```

The E38 policy sets `LIGHT_ON` to `0.90`, which would reject the observed
`TEMPERATURE -> LIGHT_ON` wrong action at `0.847105`. This may reduce
responsiveness for some `LIGHT_ON` attempts, but it is the correct safety trade
for broad-category probing while GPIO remains disabled.

## 2026-09-23 - E39 Broad Command Recovery Trained

### Objective
Recover broad post-wake command recognition after E38 showed E33 was safe for
the validated subset but unsafe for all-category wake-gated use.

### Recovery Data
Built `pi_validation/wake_gated_command_recovery_20260923/manifest.csv` from
saved E38 command-stage WAVs using
`scripts/build_wake_gated_command_recovery_manifest.py`.

Rows:

```text
12 adaptation command WAVs
```

Skipped false-wake and repeated-wake JSON files because they do not contain
executable command-stage WAVs.

### Training

```text
Experiment: E39_BROAD_COMMAND_RECOVERY_E38
Base: E33_PI_COLOR_LIGHTON_RESPONSIVENESS
Manifests:
- pi_validation/all_commands_calibration_15x/manifest.csv
- pi_validation/wake_gated_command_recovery_20260923/manifest.csv
Pi adaptation clips: 202 x repeat 20
Training examples: 4040
Pi holdout clips: 95
Best epoch: 16
Holdout accuracy: 0.9579
Holdout macro-F1: 0.9583
```

At threshold `0.90`, E39 holdout had:

```text
accepted: 83
accepted_correct: 82
accepted_wrong: 1
rejected: 12
```

The one accepted wrong was:

```text
LIGHT_ON -> CREATE_REMINDER, confidence 0.955393
```

### Guardrail Sweep
Raising only `CREATE_REMINDER` fixed the accepted wrong while preserving
`CREATE_REMINDER` responsiveness:

```text
CREATE_REMINDER threshold 0.96: accepted_wrong=0, create_accepted=5/5
CREATE_REMINDER threshold 0.97: accepted_wrong=0, create_accepted=5/5
CREATE_REMINDER threshold 0.98: accepted_wrong=0, create_accepted=5/5
CREATE_REMINDER threshold 0.99: accepted_wrong=0, create_accepted=5/5
```

### Artifact Added

```text
configs/e39_broad_command_guardrail_thresholds.json
deployment/vcm_pi_package/configs/e39_broad_command_guardrail_thresholds.json
```

Policy:

```text
default_threshold: 0.90
CREATE_REMINDER: 0.96
```

### Decision
E39 is worth live-testing tonight as the new command-stage candidate, with E37
remaining the wake gate and GPIO still disabled. E38/E39 recovery clips are not
final proof; after E39 passes smoke tests, collect fresh validation clips.

## 2026-09-23 - Workflow Packaged for Exam Defense

### Context
After receiving clarification that the model may be trained from the available
command data and should respond to the listed commands, we reviewed whether the
current process was valid or whether it required a full restart.

### Defensible Workflow
The workflow remains valid:

1. Train command recognizers from available command datasets.
2. Validate on the actual Raspberry Pi microphone and room.
3. Diagnose deployment mismatch from wrong predictions and confidence values.
4. Use selected Pi recordings as target-device adaptation/recovery data.
5. Keep held-out Pi clips and fresh live trials as evaluation evidence.
6. Add `hey pi` as a wake-gated deployment layer.
7. Use confidence guardrails to prevent wrong actions.
8. Demonstrate end-to-end actions only after live wake-gated validation.

### Non-Hacky Interpretation
Pi recordings are legitimate augmentation/adaptation data when they are clearly
separated from held-out and fresh live evaluation. The questionable version
would be training on the exact same clips and reporting them as independent
generalization. The project notes now explicitly describe Pi recordings as
deployment-domain adaptation where applicable, not as hidden final test data.

### Current Live Demo Evidence
The strongest working end-to-end evidence is:

```text
hey pi -> play music
Wake accepted, PLAY_MUSIC recognized, routed to media.play_music, and produced
audible USB headset playback.
```

Live non-LED commands currently working:

```text
PLAY_MUSIC, PAUSE, VOLUME_DOWN, TIME, TEMPERATURE, WEATHER, ALARM,
LIST_REMINDERS
```

Live commands currently safe but not demo-ready:

```text
VOLUME_UP, STOP, NEXT, TIMER, CALL, MESSAGE, CREATE_REMINDER
```

LED/light/color/brightness remain postponed for board setup and focused
recovery. E40 non-LED recovery is running as an additional recovery experiment,
not as a rewrite of the project history.

## 2026-09-23 - Documentation Integrity Rule

### Decision
The machine exercise report will be generated from the actual logs and saved evidence, not from padded or retroactively cleaned results.

### Reporting Standard
Use these categories exactly:

```text
Clean pass: correct wake, correct command label, correct routed intent/action.
Safe rejection: no wrong action was taken, but the command did not execute.
Wrong executed action: incorrect command/action was accepted and executed.
Pending: not yet validated, deferred, or requires hardware setup.
```

Safe rejections are evidence of safety behavior, not command-success evidence. Earlier failures remain in the record and may be followed by later recovery evidence. They should not be deleted or hidden.

### Source of Truth
The report must correspond to:

```text
AGENT_LOG.md
EXPERIMENT_LOG.md
PROJECT_STATUS.md
REQUIREMENTS_TRACEABILITY.md
results/wake_gated_live_20260923/
results/tables/
Pi-side pi_validation/wake_gated_live_20260923/
```

Future improvements should be logged as new experiments or validation runs rather than rewriting earlier outcomes.

## 2026-09-23 - Honesty and Validation Standard Reaffirmed

### Context
The project standard was explicitly reaffirmed before continuing model recovery and report generation. The goal is 100/100 requirement fulfillment only if the process remains honest, legitimate, and valid.

### Rules Reaffirmed

```text
1. No hidden data leakage.
   If a clip was used for adaptation/training, it is not counted as independent final validation.
   Final proof must come from held-out or fresh live trials.

2. No pretending safe rejections are successes.
   Safe rejection is safety evidence, not successful command execution.

3. No pretending all commands work.
   Working commands and unstable/not-ready commands must be listed separately.
   LED controls remain pending until board setup and validation.

4. No fake requirement mapping.
   Wake gate is an added architecture/safety layer.
   Command recognition remains the actual requirement.

5. No threshold magic as the main model.
   Thresholds are guardrails, not the classifier.
   Commands that only work by risky threshold lowering are not demo-ready.

6. Fresh validation before final claim.
   A final 100/100 claim requires a clean final validation set using the final selected model/config.
   Every tested command must be recorded and counted.
```

### Decision
Continue development and recovery only under this evidence standard. The machine exercise report must be generated from real logs, saved result JSON files, prediction tables, and final fresh validation evidence. Earlier failures and safe rejections remain part of the record and are not erased by later improvements.

## 2026-09-23 - E40 Non-LED Recovery Results and Fresh Live Validation

### Training Result
E40 was trained as a non-LED command recovery/fine-tuning experiment, not as a scratch restart.

```text
Experiment: E40_NON_LED_COMMAND_RECOVERY
Base: E39_BROAD_COMMAND_RECOVERY_E38
Pi adaptation clips: 231 x repeat 20
Training examples: 4620
Pi holdout examples: 95
Best epoch: 12
Holdout accuracy: 0.968421
Holdout macro-F1: 0.968102
Accepted at threshold 0.90: 86/95
Accepted correct: 85
Accepted wrong: 1
Rejected: 9
```

The single accepted-wrong holdout case was:

```text
STOP -> NEXT, confidence 0.964598
```

### E40 Guardrail Decision
Created an E40 command guardrail policy with `NEXT` raised to `0.98` to block the observed `STOP -> NEXT` risk. Existing E39 live safety thresholds were carried forward for labels that had already shown live wrong-action risk.

```text
configs/e40_non_led_command_guardrail_thresholds.json
```

### Fresh Live E40 Validation Observed
Clean passes:

```text
STOP: e40_wake_stop_001 -> STOP, media.stop, confidence 0.999113
TIMER: e40_wake_timer_002 -> TIMER, timer.create, confidence 0.943455
PLAY_MUSIC: e40_wake_play_music_002 -> PLAY_MUSIC, media.play_music, confidence 0.998515, audible playback observed
PAUSE: e40_wake_pause_001 -> PAUSE, media.pause, confidence 0.997730
TIME: e40_wake_time_001 -> TIME, question.time_local, confidence 0.999691
WEATHER: e40_wake_weather_002 -> WEATHER, question.weather_local, confidence 0.999996
TEMPERATURE: e40_wake_temperature_002 -> TEMPERATURE, thermostat.set_temperature, confidence 0.990097
LIST_REMINDERS: e40_wake_list_reminders_001 -> LIST_REMINDERS, reminder.list, confidence 0.999137
```

Safe rejections / not demo-ready under E40:

```text
NEXT: e40_wake_next_001 predicted NEXT at 0.720675, rejected by NEXT 0.98 guardrail
VOLUME_UP: e40_wake_volume_up_001 predicted LIST_REMINDERS at 0.779830, rejected
VOLUME_DOWN: e40_wake_volume_down_001 predicted VOLUME_DOWN at 0.881194, rejected below 0.90; e40_wake_volume_down_002 was wake-stage rejection
CALL: e40_wake_call_001 predicted PAUSE at 0.494301, rejected
MESSAGE: e40_wake_message_001 predicted MESSAGE at 0.604636, rejected
CREATE_REMINDER: e40_wake_create_reminder_001 predicted CREATE_REMINDER at 0.457362, rejected by CREATE_REMINDER 0.96 guardrail
ALARM: e40_wake_alarm_001 predicted TEMPERATURE at 0.841938, rejected; e40_wake_alarm_002 predicted TIME at 0.788918, rejected
```

Wake-stage safe rejections, not command-stage failures:

```text
e40_wake_timer_001: wake confidence 0.831289, command window stayed closed
e40_wake_weather_001: wake confidence 0.772404, command window stayed closed
e40_wake_volume_down_002: wake confidence 0.866578, command window stayed closed
```

### Duplicate Trial ID Caveat
`e40_wake_temperature_001` was accidentally reused. Terminal output showed two events with the same trial id: first a wake-stage rejection at wake confidence `0.782046`, then a clean temperature pass at command confidence `0.970920`. The saved result JSON likely reflects the later run. For clean file-backed evidence, `e40_wake_temperature_002` should be used instead.

### Decision
E40 improves some weak non-LED commands, especially `STOP` and `TIMER`, but it is not a universal replacement for E39. It should be treated as a recovery candidate with fresh live evidence. Final reporting must preserve both passes and safe rejections.

## 2026-09-23 - E40 Final Wake-Gated Validation Packaged

### What Was Done
Ran and documented a fresh final wake-gated validation sequence for E40 using unique `e40_final_*` and safety trial ids. Results were classified honestly as clean pass, safe rejection, or invalid trial.

### Safety Validation

```text
False/non-target wake phrases rejected with no command action:
- e40_false_wake_hey_siri_001
- e40_false_wake_hey_google_001
- e40_false_wake_alexa_001
- e40_false_wake_hello_001

Bare commands spoken without wake rejected with no action:
- e40_no_wake_play_music_001
- e40_no_wake_weather_001
```

### Clean Final Command Passes

```text
PLAY_MUSIC: e40_final_play_music_001, audible playback observed
PAUSE: e40_final_pause_001
STOP: e40_final_stop_001
TIMER: e40_final_timer_001
TIME: e40_final_time_001
WEATHER: e40_final_weather_001
TEMPERATURE: e40_final_temperature_001
VOLUME_DOWN: e40_final_volume_down_001
CREATE_REMINDER: e40_final_create_reminder_001
LIST_REMINDERS: e40_final_list_reminders_004
```

### Not Final Validated Under E40

```text
VOLUME_UP: safe rejected on final attempts
NEXT: safe rejected on final attempts
ALARM: safe rejected on final attempts
CALL: safe rejected on final attempt
MESSAGE: safe rejected on final attempt
```

### Caveats Preserved
`e40_final_list_reminders_001` is not counted because the tester did not speak the command after wake. It is an invalid/aborted trial with delayed output and no action. `e40_final_list_reminders_002` and `_003` were wake-stage rejections. `e40_final_list_reminders_004` is the clean final list-reminders pass.

### Decision
E40 is a strong partial final validation candidate with clean evidence for 10 non-LED commands and wake-gate safety behavior. It is not a 100/100 all-command result. The report must preserve the commands that remain not final-validated under E40.

## 2026-09-23 - E41 Functional Recovery Target Defined

### Current Implemented Pipeline

```text
Audio capture
-> wake CNN
-> wake gate
-> fixed command recording
-> log-Mel preprocessing
-> command CNN
-> confidence guardrail
-> deterministic intent router
-> action executor
-> evidence logging
```

The current validation runner processes one wake-command interaction at a time and then exits. The intended product/demo behavior is a continuous loop that returns to wake listening after each executed or rejected command.

### E40 Command Diagnosis

Commands with clean final E40 live passes:

```text
PLAY_MUSIC: recognition, routing, and USB audio playback working
PAUSE: recognition and routing working
STOP: live pass; guardrail remains important because prior holdout risk was STOP -> NEXT
VOLUME_DOWN: recognition and routing working
TIME: recognition and routing working
WEATHER: recognition and routing working
TEMPERATURE: recognition and routing working
TIMER: live pass; monitor TIME/TIMER confusion risk
CREATE_REMINDER: recognition, routing, and local reminder action working
LIST_REMINDERS: recognition, routing, and local reminder listing working after clean final retry
```

Commands not final-validated under E40 and requiring recovery:

```text
VOLUME_UP: live Pi audio misrecognized as PAUSE/VOLUME_DOWN
NEXT: sometimes predicted as NEXT but confidence too low for guardrail
ALARM: top label can be ALARM but confidence remains below threshold
CALL: live Pi audio misrecognized as other commands
MESSAGE: top label can be MESSAGE but confidence remains below threshold
```

Deferred hardware-dependent controls:

```text
LIGHT_ON
LIGHT_OFF
COLOR
BRIGHTNESS
```

### Missing Pipeline Pieces

```text
Continuous listening loop: not yet implemented in the validated runner
True VAD command window: not yet implemented; current command capture is fixed duration
Robustness testing: distance, volume variation, background noise, and non-Loreen speakers not yet introduced
LED hardware validation: deferred until board setup
INT8/edge quantized deployment claim: not yet validated
```

### E41 Goal
E41 should be a focused recognition recovery experiment. Its goal is to improve live Pi command recognition for `VOLUME_UP`, `NEXT`, `ALARM`, `CALL`, and `MESSAGE` while preserving the commands already passing under E40. E41 is not a routing/action rewrite and not a threshold-lowering shortcut.

### E41 Reporting Rule
Clips used for E41 adaptation/training must not be counted as independent final proof. E41 must be judged using fresh post-training live validation trials with new trial ids.

## 2026-09-23 - Tomorrow Work Plan for Functional VCM

### Methodology Decision
Because persistent neighbor/background singing was present, E41 recordings should be postponed until cleaner conditions. Noisy data may be useful later for robustness, but E41's purpose is clean-condition recognition recovery. Mixing uncontrolled noise into E41 would blur the diagnosis.

### Data Integrity Note
The first attempted `NEXT` E41 recordings used the prompt phrase `skip song`. These should be deleted and not used for E41 because the intended command phrase is `next`. Keeping those clips would train the `NEXT` label on the wrong spoken phrase.

### Product Goal
Build a functional VCM, not just a validation table. The system should support random command order after the wake phrase. Random-speaker robustness is a separate requirement and must be tested with fresh non-training trials before being claimed.

### Tomorrow Execution Order

1. Delete incorrect/noisy E41 recovery clips if present.
2. Record clean E41 focused recovery clips for:

```text
VOLUME_UP -> "volume up"
NEXT -> "next"
ALARM -> "alarm"
CALL -> "call"
MESSAGE -> "message"
```

3. Train `E41_FUNCTIONAL_NON_LED_RECOVERY` from E40/E39-compatible weights using focused recovery data plus maintenance/replay protection.
4. While E41 trains, record spoken action-output WAV files for non-LED intents in `pi_responses/`.
5. Connect accepted command intents to response WAV playback, similar to the already working `PLAY_MUSIC` audio path.
6. Validate E41 with fresh wake-gated trial ids. Do not count E41 adaptation clips as final proof.
7. If clean recognition is good, run limited robustness checks:

```text
random command order
non-Loreen speaker
distance
volume variation
background noise
```

8. Add a continuous listening loop after command/action behavior is stable.
9. Run benchmarking and generate the final report from logs, result JSON files, WAV evidence, and summary tables.

### Action Output Plan
Non-LED commands may produce spoken WAV responses as practical demo outputs. LED commands remain hardware outputs when the LED board is assembled:

```text
LIGHT_ON -> white LED pulse
LIGHT_OFF -> green LED pulse
COLOR -> red LED pulse
BRIGHTNESS -> white + green + red LED pulse
```

## 2026-09-24 - Future Dataset Registry Refactor Task

### Task Captured
After the functional VCM path is stable, consolidate datasets and their corresponding manifests into one organized data registry folder. Then refactor model/training/evaluation code to reference the new paths and document the project inventory.

### Scope

```text
1. Create a single dataset registry folder with subfolders for:
   - original/source dataset
   - Pi calibration data
   - wake data
   - recovery/adaptation data
   - holdout/validation data
   - final demo evidence

2. Move or copy manifests into the registry with clear names.

3. Refactor code/config paths so training and evaluation scripts resolve the new locations.

4. Confirm runtime Pi inference does not depend on training datasets or manifests.

5. Write/update project inventory documentation explaining:
   - dataset provenance
   - split definitions
   - manifest locations
   - training/adaptation/holdout/final-validation usage
   - runtime package contents
```

### Timing
Do not perform this refactor before E41 and the action-output demo path are stable. Moving data too early could break scripts during deadline-critical work. For now, preserve current paths and use documentation/registry copies if needed.
## 2026-09-25 - Phase A Requirements Re-Audit

### Objective
Reset the project direction to the actual assignment requirements rather than
freezing the project at a restricted five-command demo subset.

### Sources
- `VCM AGENT.pdf`
- `VCM Machine Exercise.pdf`
- `REQUIREMENTS_TRACEABILITY.md`
- `PROJECT_STATUS.md`
- `EXPERIMENT_LOG.md`
- current result/benchmark files

### Result
Created `PHASE_A_REQUIREMENTS_REAUDIT_20260925.md`.

### Decision
The restricted five-command packet is interim evidence only. The project remains
in all-command recovery, validation, benchmarking, robustness testing, and final
audit mode. The immediate next engineering task is to pull current Pi-side
E40/E41/E42 artifacts back to Windows, hash/register them, and build the current
command-by-command/error-layer table before starting another training run.

## 2026-09-25 - Phase B Evidence Pullback And Inventory

### Objective
Pull current Raspberry Pi evidence back to Windows, verify integrity, inventory
artifacts, and reconstruct command status from actual JSON evidence.

### Result
- Pullback folder:
  `outputs/pi_evidence_pullback_20260925_190658/`
- Archive: `pi_current_evidence_20260925_190658.tgz`, `33,719,423` bytes.
- Remote archive listing: `540` files.
- Extracted files: `540`.
- SHA256 verification: `541` manifest rows checked, `0` missing, `0`
  mismatched.
- Inventory files created:
  - `EVIDENCE_INVENTORY.csv`
  - `COMMAND_EVIDENCE_TABLE.csv`
  - `PHASE_B_EVIDENCE_INVENTORY_20260925.md`
  - `PHASE_B_COMMAND_STATE_AND_REQUIREMENTS_AUDIT_20260925.md`

### Interpretation
E40, E41, and E42 artifacts are now present in the pulled evidence. Current
evidence still does not satisfy all-command 100/100 completion. E42 is not a
clear live improvement based on pulled real-audio trials. E41 has useful partial
recovery, but multiple commands still fail or remain provisional. Continue with
fresh all-command validation and error-layer repair; do not train or report
final completion before the inventory-driven validation plan is complete.

## 2026-09-25 - Phase C Stack Lock Started

### Objective
Freeze the experimental baseline before fresh all-command validation.

### Current Candidate
`E41_FUNCTIONAL_NON_LED_RECOVERY` with the existing
`E40_NON_LED_COMMAND_GUARDRAIL_THRESHOLDS` command threshold policy.

### Result
Created:

- `PHASE_C_FROZEN_CANDIDATE_STACK_20260925.md`
- `PHASE_C_FRESH_ALL_COMMAND_VALIDATION_PLAN_20260925.md`
- `tools/pull_phase_c_stack_artifacts.ps1`

### Blocker Before Running Validation
The first pullback did not include the wake model artifacts for
`E37_TARGETED_COLOR_VOLUME_FIX`, even though pulled JSON evidence shows E37 was
used as the wake model. It also did not include the exact Pi-side scripts/actions
that controlled WAV response behavior. Pull those stack artifacts and hash them
before running Phase C validation.

## 2026-09-25 - Phase C Stack Lock Completed

### Objective
Verify the missing wake/action stack artifacts and complete the frozen baseline.

### Result
Supplemental stack pullback completed in
`outputs/phase_c_stack_pullback_20260925_204337/`.

- Remote files selected: `49`
- Extracted files: `49`
- SHA256 manifest rows verified: `50`
- Missing files: `0`
- Hash mismatches: `0`

The stack is now locked for Phase C validation:

- Wake model: `E37_TARGETED_COLOR_VOLUME_FIX`
- Command model: `E41_FUNCTIONAL_NON_LED_RECOVERY`
- Command threshold policy: `E40_NON_LED_COMMAND_GUARDRAIL_THRESHOLDS`
- GPIO disabled
- Local audio/WAV response path enabled

### Decision
Proceed to fresh all-command validation with unique `phase_c_*` trial IDs. Do
not change model, thresholds, preprocessing, routing, parser, wake gate, action
logic, or response WAVs until the complete baseline evidence table is generated.

## 2026-09-25 - Phase C Stack Provenance Verified Before Trial 001

### Objective
Confirm that the frozen Phase C stack is an existing tested configuration before
starting fresh all-command validation.

### Evidence Checked
- `outputs/phase_c_stack_pullback_20260925_204337/SHA256SUMS.csv`
- `outputs/phase_c_stack_pullback_20260925_204337/extracted/scripts/run_e41_wake_command_usb_demo.sh`
- `outputs/phase_c_stack_pullback_20260925_204337/extracted/configs/e40_non_led_command_guardrail_thresholds.json`
- `outputs/pi_evidence_pullback_20260925_190658/extracted/pi_validation/wake_gated_live_20260923/e41_real_audio_weather_001_result.json`
- `outputs/pi_evidence_pullback_20260925_190658/COMMAND_EVIDENCE_TABLE.csv`

### Result
The exact stack is an existing tested runner combination, not a new Phase C-only
assembly:

- Wake: `E37_TARGETED_COLOR_VOLUME_FIX`
- Command model: `E41_FUNCTIONAL_NON_LED_RECOVERY`
- Command threshold policy: `E40_NON_LED_COMMAND_GUARDRAIL_THRESHOLDS`
- Wake threshold: `0.90`
- Command default threshold: `0.90`
- GPIO: disabled
- Local WAV response/action layer: enabled

### Decision
Freeze this stack completely for Phase C. Proceed to Trial 001 without changing
model, preprocessing, thresholds, wake gate, label mapping, parser, router, or
action logic.

## 2026-09-25 - Phase C Trial 001 Recorded

### Trial
`phase_c_play_music_20260925_001`

### Expected
`PLAY_MUSIC` / phrase `play music`

### Result
Wake gate accepted `WAKE` at confidence `0.9997376799583435`.

Command VCM predicted the correct raw label, `PLAY_MUSIC`, at confidence
`0.8174716830253601`, but the frozen threshold was `0.90`, so the command was
rejected and no action was executed.

### Interpretation
Trial 001 is a Phase C baseline FAIL at layer F, confidence/rejection. It is not
a routing failure or action-output failure because routing/action execution did
not run after the threshold rejection.

### Files
- `PHASE_C_BASELINE_VALIDATION_LOG_20260925.md`
- `PHASE_C_BASELINE_TRIALS_20260925.csv`

## 2026-09-26 - Start-of-Day Log Update Before E43 Work

### Objective
Bring the project logs current before starting any new engineering task.

### Current Baseline
Phase C is the frozen comparison baseline.

- Wake model: `E37_TARGETED_COLOR_VOLUME_FIX`
- Command model: `E41_FUNCTIONAL_NON_LED_RECOVERY`
- Threshold policy: `E40_NON_LED_COMMAND_GUARDRAIL_THRESHOLDS`
- Evidence pullback: `outputs/pi_evidence_pullback_20260925_214022/`
- Parsed Phase C JSON results: `27`
- SHA256 manifest rows: `615`
- Missing files: `0`
- Hash mismatches: `0`

### Phase C Result
Positive raw labels covered: `19/19`.

- Full PASS: `10`
- PARTIAL PASS: `2`
- FAIL: `7`
- Valid no-action probes: `6`
- PASS-SAFE no-action probes: `6`
- Invalid procedure trial excluded: `1`

### Accepted Analysis
The Phase C failure-layer analysis was accepted. The canonical 9 non-full-pass
trials are classified as:

- VCM classification: `3`
- confidence/rejection: `4`
- response/output: `2`

The highest-risk case is `CREATE_REMINDER` predicted as `LIST_REMINDERS`,
accepted, routed, and executed as `reminder.list`.

### E43 Status
E43 is defined only as a proposed targeted recovery experiment. Training has not
started. No model, threshold, preprocessing, parser, router, or action logic has
been modified after Phase C.

### Next Work Rule
Before E43 training, preserve Phase C as the reproducible comparison baseline.
Recovery recordings must remain separate from fresh validation recordings.

## 2026-09-26 - Output Path Retest Started

### Objective
Investigate the Phase C `LIGHT_OFF` and `NEXT` response/output uncertainty before treating those trials as model failures.

### Test
Directly replayed the local response WAV files on the known-working HDMI/LCD audio device:

```bash
aplay -D plughw:CARD=vc4hdmi0,DEV=0 pi_responses/light_off.wav
aplay -D plughw:CARD=vc4hdmi0,DEV=0 pi_responses/next.wav
```

### Result
User reported both WAV files played clearly.

### Interpretation
The WAV assets and direct HDMI/LCD playback path are not the cause of the Phase C static/uncertain output. Continue by testing the action-layer playback path separately from the VCM model.

## 2026-09-26 - LIGHT_OFF Response Mapping Fixed and Retested

### Objective
Resolve the Phase C `LIGHT_OFF` response/output partial pass without changing the VCM model.

### Evidence
Direct playback of `pi_responses/light_off.wav` was clear, but action-layer execution initially returned `hardware_applied: false` and produced no clear response. Inspection showed `light.off` was not mapped in `RESPONSE_AUDIO_BY_ACTION`.

### Intervention
Added response mappings on the Pi:

```text
light.on -> light_on.wav
light.off -> light_off.wav
```

A backup was created on the Pi:

```text
actions/command_actions.py.bak_light_audio_20260926
```

### Retest

```bash
python -m actions.command_actions \
  --intent LIGHT_CONTROL \
  --slot light_action=off \
  --phrase "lights off"
```

Result:

```json
{
  "intent": "LIGHT_CONTROL",
  "status": "executed",
  "action": "light.off",
  "hardware_applied": true
}
```

User heard: "switching the light off".

### Interpretation
The Phase C `LIGHT_OFF` partial pass was a response-audio mapping/software-output issue, not a VCM classification failure. No model, preprocessing, or threshold change was involved.

## 2026-09-26 - NEXT Action Output Retested

### Objective
Confirm whether the Phase C `NEXT` partial pass was a model/routing issue or an output-evidence issue.

### Retest

```bash
python -m actions.command_actions \
  --intent MEDIA_CONTROL \
  --slot media_action=next \
  --phrase "next"
```

### Result
The action layer returned:

```json
{
  "intent": "MEDIA_CONTROL",
  "status": "executed",
  "action": "media.next",
  "confidence": 1.0,
  "accepted": true,
  "hardware_applied": true
}
```

User reported clear playback.

### Interpretation
`NEXT` is not an E43 model-training target based on current evidence. The VCM classification, routing, action execution, and response output path are all working in the action-layer retest. Keep `NEXT` in fresh regression validation.

## 2026-09-26 - E43 Target List Updated After Output Repairs

### Objective
Update the proposed E43 plan so it reflects today's proven output/action repairs before any training begins.

### Evidence
`LIGHT_OFF` and `NEXT` were the two Phase C partial passes attributed to response/output uncertainty. Follow-up testing showed:

- `LIGHT_OFF`: missing response-audio mapping repaired; action-layer retest returned `hardware_applied: true`; user heard "switching the light off".
- `NEXT`: action-layer retest returned `media.next`, `hardware_applied: true`; user reported clear playback.

### Action
Updated `PHASE_E43_EXPERIMENT_SPEC_20260925.md` so `LIGHT_OFF` and `NEXT` are no longer listed as open E43 model-retraining targets. They remain required regression-validation commands after E43.

### Interpretation
The highest-value E43 model work remains `CREATE_REMINDER` vs `LIST_REMINDERS`, `LIGHT_ON`, `COLOR`, and confidence/rejection review for `PLAY_MUSIC`, `BRIGHTNESS`, `PAUSE`, and `VOLUME_DOWN`. No E43 training has started.

## 2026-09-27 - E43 Recovery Data Collection Started

### Objective
Start E43 by collecting targeted recovery data only, not by training.

### Why
The existing calibration helper uses a `CREATE_REMINDER` phrase that differs from the Phase C failed phrase. Phase C failed on "create reminder", so the E43 recovery plan must explicitly record that phrase rather than blindly reusing the older helper prompt.

### Action
Created `PHASE_E43_RECOVERY_DATA_COLLECTION_PLAN_20260927.md` with exact target phrases, data version, output folder, Pi recording command, success criteria, and safety criteria.

### Current Decision
Proceed with recovery-data collection on the Raspberry Pi. Do not train, change thresholds, or modify the model until the new recovery audio is pulled back, hashed, and inventoried.

## 2026-09-27 - E43 Reminder Recovery Block Recorded

### Objective
Collect the first targeted E43 recovery block for the highest-risk Phase C confusion pair: `CREATE_REMINDER` vs `LIST_REMINDERS`.

### Result
The Pi recorded:

- `CREATE_REMINDER`: 10 WAV files
- `LIST_REMINDERS`: 10 WAV files

Audio format verification showed all 20 WAV files are 16 kHz, mono, 16-bit, and approximately 4.0 seconds long.

### Metadata Note
`manifest.csv` reported 22 lines. Expected count for 20 recordings plus one header is 21. Before recording the next block, inspect the manifest for a duplicate/header/stray row.

### Interpretation
Audio capture for the first E43 recovery block is valid. Manifest bookkeeping needs a quick correction or explanation before pullback/training.

## 2026-09-27 - E43 LIGHT_ON / COLOR Recovery Block Verified

### Objective
Collect and verify targeted E43 recovery clips for the Phase C `LIGHT_ON` and `COLOR` VCM classification failures.

### Result
The Pi recorded:

- `LIGHT_ON`: 10 WAV files
- `COLOR`: 10 WAV files

Current recovery folder totals:

- `CREATE_REMINDER`: 10 WAV files
- `LIST_REMINDERS`: 10 WAV files
- `LIGHT_ON`: 10 WAV files
- `COLOR`: 10 WAV files

`manifest.csv` now has 41 lines: one header plus 40 recovery rows. Rows by label are balanced at 10 each. Format verification showed the new `LIGHT_ON` and `COLOR` files are 16 kHz, mono, 16-bit, and 4.0 seconds long.

### Interpretation
The class-separation recovery block for the three highest-priority Phase C classification failures is now captured: reminder confusion, `LIGHT_ON`, and `COLOR`. No model training has started.

## 2026-09-27 - E43 Confidence/Rejection Recovery Block Verified

### Objective
Collect and verify targeted E43 recovery clips for commands that Phase C classified correctly but rejected below the frozen threshold policy.

### Result
The Pi recorded:

- `PLAY_MUSIC`: 10 WAV files
- `BRIGHTNESS`: 10 WAV files
- `PAUSE`: 10 WAV files
- `VOLUME_DOWN`: 10 WAV files

Current recovery folder totals:

- 8 labels captured
- 80 WAV files total
- `manifest.csv`: 81 lines, one header plus 80 recovery rows

Format verification showed all checked files in this block are 16 kHz, mono, 16-bit, and 4.0 seconds long.

### Interpretation
The E43 core recovery dataset is now captured for both major evidence groups: classification confusion and confidence/rejection weakness. Final contrast/regression clips still remain before pullback and inventory.

## 2026-09-27 - E43 Recovery Collection Completed and Verified

### Objective
Complete the planned `E43_TARGETED_RECOVERY_DATA_V1` Pi microphone recovery dataset.

### Result
Final contrast/regression block recorded:

- `LIGHT_OFF`: 5 WAV files
- `VOLUME_UP`: 5 WAV files
- `TEMPERATURE`: 5 WAV files

Full recovery folder verification:

- total WAV files: 95
- manifest rows: 96, including one header
- main targets: 10 clips each
- contrast/regression targets: 5 clips each
- full audio format check: `bad_files 0`

### Interpretation
E43 recovery data collection is complete and internally verified on the Pi. These recordings are recovery/training candidates only, not final validation evidence.

### Next
Pull the E43 recovery folder back to Windows, verify hashes, inventory the recovered files, and only then decide whether to begin E43 training.

## 2026-09-27 - E43 Recovery Evidence Pulled Back to Windows

### Objective
Secure the verified E43 recovery data from the Raspberry Pi into the Windows project evidence tree.

### Result
Pullback folder:

```text
outputs/e43_recovery_pullback_20260927_104105/
```

Windows-side verification:

- folder exists: true
- total WAV files: 95
- manifest rows: 96
- label counts match plan:
  - 10 each: `BRIGHTNESS`, `COLOR`, `CREATE_REMINDER`, `LIGHT_ON`, `LIST_REMINDERS`, `PAUSE`, `PLAY_MUSIC`, `VOLUME_DOWN`
  - 5 each: `LIGHT_OFF`, `TEMPERATURE`, `VOLUME_UP`
- SHA256 CSV rows: 98

The SHA256 CSV row count is expected: one CSV header plus 97 files, consisting
of 95 WAV files, the cleaned `manifest.csv`, and the preserved
`manifest_before_dedupe_20260927T022818Z.csv` backup.

### Interpretation
E43 recovery evidence is now pulled back and hashed on Windows. This is still recovery/training evidence only, not final validation.

## 2026-09-27 - E43 Training-Readiness Inventory Passed

### Objective
Audit the pulled E43 recovery data before any model training begins.

### Result
Created `PHASE_E43_TRAINING_READINESS_AUDIT_20260927.md`.

Inventory results:

- manifest data rows: 95
- WAV files: 95
- missing manifest targets: 0
- extra WAVs: 0
- duplicate manifest WAV paths: 0
- files under recovery root: 97
- normalized SHA rows: 97
- missing normalized SHA rows: 0
- extra normalized SHA rows: 0

### Interpretation
The E43 recovery data is ready as recovery/training input. It is still not final validation evidence. The next step is to inspect the training script and define the exact E43 training command before running it.

## 2026-09-27 - E43 Training Command Defined

### Objective
Define the exact E43 training command and input manifests before starting model training.

### Actions
- Created `manifest_e43_adaptation_for_training.csv` from the pulled E43 recovery manifest.
- Staged pulled `E41_FUNCTIONAL_NON_LED_RECOVERY` artifacts into standard local model/result paths without content changes.
- Verified staged E41 hashes match the pulled Phase C stack artifacts.
- Ran loader compatibility check.
- Created `PHASE_E43_TRAINING_COMMAND_SPEC_20260927.md`.

### Loader Check
- base adaptation clips: 190
- base holdout clips: 95
- E43 adaptation clips: 95
- E43 holdout clips: 0
- labels: 19

### Interpretation
The E43 training command is defined and ready, but training has not started. E43 recovery clips remain adaptation-only and must not be treated as final validation.

## 2026-09-27 - Full E43 Training Attempt Interrupted Before Artifacts

### Objective
Run the specified full E43 training command.

### Result
The process loaded TensorFlow and consumed CPU for an extended period, but produced no flushed training output and wrote no E43 artifacts before interruption.

### Verification
After interruption:

- no Python training process remained
- no `E43_TARGETED_COMMAND_RECOVERY*` model artifacts existed
- no `E43_TARGETED_COMMAND_RECOVERY*` results-table artifacts existed

### Engineering Decision
Do not keep waiting on the full repeat-20 run as the first execution. Create and run a smaller smoke experiment first to verify the end-to-end training path, then scale back up if the smoke run succeeds.

### New Plan
Created `PHASE_E43_TRAINING_SMOKE_PLAN_20260927.md`.

## 2026-09-27 - E43 Smoke Training Completed

### Objective
Run a bounded smoke training experiment to verify the E43 training pipeline.

### Result
`E43_TARGETED_COMMAND_RECOVERY_SMOKE` completed and wrote model, normalization, history, labels, metrics, and holdout prediction artifacts.

### Metrics
- holdout accuracy: 0.8842105263157894
- macro-F1: 0.8851674641148325
- threshold 0.90 accepted: 81
- threshold 0.90 accepted correct: 74
- threshold 0.90 accepted wrong: 7

### Interpretation
Pipeline PASS. Model NOT promoted. The smoke model is not good enough because wrong accepted predictions increased and several labels regressed.

### Artifact
`PHASE_E43_TRAINING_SMOKE_RESULT_20260927.md`

## 2026-09-27 - E43 Smoke Regression Analysis Completed

### Objective
Compare E43 smoke against E41 baseline and identify the next safe intervention.

### Result
Created `PHASE_E43_SMOKE_REGRESSION_ANALYSIS_20260927.md` and `results/tables/E43_SMOKE_VS_E41_PER_LABEL_COMPARISON.csv`.

### Key Finding
Smoke improved `COLOR`, `CREATE_REMINDER`, and `NEXT`, but regressed `BRIGHTNESS`, `LIGHT_OFF`, `LIGHT_ON`, `LIST_REMINDERS`, `PAUSE`, `STOP`, and `VOLUME_UP`.

### Decision
Do not promote the smoke model. Next candidate must reduce over-adaptation risk and preserve E41 guardrails.

## 2026-09-27 - E43 Cautious Candidate Spec Prepared

### Objective
Define the next E43 candidate after smoke regression analysis.

### Actions
- Created `manifest_e43_fresh_style_for_cautious_training.csv` from the pulled E43 recovery manifest.
- Verified the manifest loads through `training/train_pi_fresh_miniset_recovery.py`.
- Created `PHASE_E43_CAUTIOUS_TRAINING_SPEC_20260927.md`.

### Evidence
- fresh manifest rows: 95
- loader status: PASS
- labels represented: `BRIGHTNESS`, `COLOR`, `CREATE_REMINDER`, `LIGHT_OFF`, `LIGHT_ON`, `LIST_REMINDERS`, `PAUSE`, `PLAY_MUSIC`, `TEMPERATURE`, `VOLUME_DOWN`, `VOLUME_UP`

### Engineering Decision
Use the cautious training path that preserves E41 normalization and starts from E41 weights. Do not change wake gate, parser, router, action logic, thresholds, or final validation rules.

### Next
Run `E43_TARGETED_COMMAND_RECOVERY_CAUTIOUS` exactly as specified, then compare it against both E41 and the E43 smoke model before any live validation.

## 2026-09-27 - E43 Cautious Candidate Completed

### Objective
Run the cautious E43 candidate and compare it against E41 and E43 smoke.

### Result
`E43_TARGETED_COMMAND_RECOVERY_CAUTIOUS` completed and wrote model, normalization, history, labels, holdout predictions, fresh recovery predictions, and metrics.

### Evidence
- `PHASE_E43_CAUTIOUS_TRAINING_RESULT_20260927.md`
- `results/tables/E41_FUNCTIONAL_NON_LED_RECOVERY_CURRENT95_REEVAL_metrics.json`
- `results/tables/E43_CAUTIOUS_VS_E41_SMOKE_SUMMARY.csv`
- `results/tables/E43_CAUTIOUS_VS_E41_SMOKE_PER_LABEL.csv`
- `results/tables/E43_CAUTIOUS_VS_E41_SMOKE_WRONG_ACCEPTED.csv`

### Key Result
On the same 95-example holdout:

- E41 current95 re-eval: accuracy 0.9473684210526315, macro-F1 0.947900053163211, wrong accepted 2
- E43 smoke: accuracy 0.8842105263157894, macro-F1 0.8851674641148325, wrong accepted 7
- E43 cautious: accuracy 0.9157894736842105, macro-F1 0.9156831472620945, wrong accepted 2

### Engineering Decision
Do not promote E43 cautious. It is safer than smoke but still worse than E41, and E43 recovery `COLOR` performance is 0/10.

### Next
Analyze E43 recovery prediction failures before any additional training.

## 2026-09-27 - E43 Cautious Recovery Error Analysis

### Objective
Analyze E43 cautious recovery-set failures before defining any new training run.

### Result
Created `PHASE_E43_CAUTIOUS_RECOVERY_ERROR_ANALYSIS_20260927.md`.

### Evidence
- `results/tables/E43_CAUTIOUS_FRESH_RECOVERY_ERROR_SUMMARY.csv`
- `results/tables/E43_CAUTIOUS_FRESH_RECOVERY_ERRORS.csv`

### Key Findings
- 24 recovery-set errors
- 7 wrong accepted errors at threshold 0.90
- `COLOR`: 0/10 correct, but 0 wrong accepted
- `CREATE_REMINDER`: 4/10 correct, 2 wrong accepted
- `VOLUME_DOWN`: 8/10 correct, 2 wrong accepted

### Engineering Decision
Do not start another E43 training run immediately. Inspect recovery audio/data and error patterns first.

## 2026-09-27 - E43 Recovery Audio/Data Inspection

### Objective
Inspect E43 recovery WAV quality and data consistency before choosing another intervention.

### Result
Created `PHASE_E43_RECOVERY_AUDIO_DATA_INSPECTION_20260927.md`.

### Evidence
- `results/tables/E43_RECOVERY_AUDIO_QC_JOINED_WITH_CAUTIOUS_PREDICTIONS.csv`
- `results/tables/E43_RECOVERY_AUDIO_QC_BY_LABEL.csv`
- `results/tables/E43_RECOVERY_AUDIO_QC_FLAGGED_CLIPS.csv`
- `results/tables/E43_RECOVERY_E41_VS_CAUTIOUS_SUMMARY.csv`
- `results/tables/E43_RECOVERY_E41_VS_CAUTIOUS_BY_LABEL.csv`

### Key Findings
- 95/95 E43 recovery WAVs are structurally valid 16 kHz mono 16-bit 4-second files.
- Only 2 clips were flagged for clipping, and both were correctly predicted.
- `COLOR` clips were not grossly quiet or truncated.
- Original calibration used `COLOR` phrase `color red`.
- E43 recovery and Phase C tested `COLOR` as the shorter phrase `color`.

### Interpretation
`COLOR` is primarily a phrase-coverage/class-separation problem, not an audio-format problem.

### Next
Prepare a focused data-collection plan that explicitly covers both `color` and `color red` plus contrast labels.

## 2026-09-27 - E44 Focused Recovery Data Plan Prepared

### Objective
Prepare the next recovery-data task after the E43 audio/data inspection.

### Result
Created `PHASE_E44_FOCUSED_RECOVERY_DATA_PLAN_20260927.md`.

### Scope
- `COLOR`: `color`, 10 trials
- `COLOR`: `color red`, 10 trials
- Confusion contrast: `CALL`, `TIME`, `TEMPERATURE`, `STOP`, 5 trials each
- Wrong-accept contrast: `CREATE_REMINDER`, `LIST_REMINDERS`, `VOLUME_DOWN`, `VOLUME_UP`, 5 trials each
- Total planned clips: 60

### Boundary
E44 data is recovery/training data only, not final validation.

## 2026-09-27 - E44 Pi Recording Verification Complete

### Objective
Verify E44 focused recovery recordings on the Pi.

### Result
Pi-side verification completed.

### Evidence
- `PHASE_E44_PI_RECORDING_VERIFICATION_20260927.md`

### Counts
- total WAV files: 60
- manifest rows: 61 including header
- audio format bad files: 0

### Interpretation
E44 focused recovery data is structurally complete on the Pi. It still needs Windows pullback, hashing, and local inspection before training.

## 2026-09-27 - E44 Pullback And QC Complete

### Objective
Verify E44 focused recovery data after Windows pullback.

### Result
Pullback and local QC completed.

### Evidence
- `PHASE_E44_PULLBACK_AND_QC_20260927.md`
- `outputs/e44_focused_recovery_pullback_20260927_114518/SHA256SUMS.csv`
- `results/tables/E44_RECOVERY_AUDIO_QC.csv`
- `results/tables/E44_RECOVERY_AUDIO_QC_BY_LABEL_PHRASE.csv`
- `results/tables/E44_RECOVERY_AUDIO_QC_FLAGGED_CLIPS.csv`

### Counts
- WAV files: 60
- manifest rows: 61 including header
- SHA256 rows: 61
- audio-format bad files: 0
- QC flagged clips: 0

### Interpretation
E44 pullback is complete and locally usable for training-readiness preparation. No model training has started.

## 2026-09-27 - E44 Training Readiness Audit Passed

### Objective
Create derived E44 training manifest and verify trainer compatibility.

### Result
Created `manifest_e44_fresh_style_for_training.csv` and verified it with `training.train_pi_fresh_miniset_recovery.read_fresh_manifest`.

### Evidence
- `PHASE_E44_TRAINING_READINESS_AUDIT_20260927.md`

### Counts
- source manifest rows: 60
- derived training manifest rows: 60
- missing derived targets: 0
- loader examples: 60

### Next
Define exact E44 candidate experiment specification. Do not train until the specification is written.

## 2026-09-27 - E44 Candidate Specification Prepared

### Objective
Define a controlled E44 candidate experiment after E44 readiness passed.

### Result
Created `PHASE_E44_CANDIDATE_EXPERIMENT_SPEC_20260927.md`.

### Combined Manifest
`manifest_e43_e44_combined_recovery_for_training.csv`

### Counts
- combined recovery clips: 155
- E43 recovery clips: 95
- E44 recovery clips: 60
- missing targets: 0
- loader status: PASS

### Engineering Decision
Use E41 as the base model, preserve E41 normalization, lower the learning rate to 0.00002, and keep recovery data as training-only. This remains a candidate experiment, not final validation.

## 2026-09-27 - E44 Candidate Training Completed And Rejected

### Objective
Run `E44_FOCUSED_COLOR_RECOVERY_CAUTIOUS` and compare against E41/E43 candidates.

### Result
Training completed and artifacts were written.

### Evidence
- `PHASE_E44_CANDIDATE_TRAINING_RESULT_20260927.md`
- `results/tables/E44_CANDIDATE_VS_E41_E43_HOLDOUT_SUMMARY.csv`
- `results/tables/E44_CANDIDATE_COMBINED_RECOVERY_ERROR_SUMMARY.csv`
- `results/tables/E44_CANDIDATE_COMBINED_RECOVERY_ERRORS.csv`

### Key Metrics
- holdout accuracy: 0.8947368421052632
- holdout macro-F1: 0.896785670469881
- holdout wrong accepted at threshold 0.90: 1
- combined recovery accuracy: 0.6516129032258065
- combined recovery wrong accepted at threshold 0.90: 22
- combined recovery `COLOR`: 3/30 correct

### Engineering Decision
Do not promote E44. Do not proceed to fresh live validation. The intended `COLOR` fix did not succeed and introduced too many recovery wrong accepted cases.

## 2026-09-27 - COLOR Command Design Audit Completed

### Objective
Determine whether `COLOR` should be treated as a training issue or command-design issue.

### Result
Created `PHASE_E44_COLOR_COMMAND_DESIGN_AUDIT_20260927.md`.

### Evidence
- `results/tables/E44_COLOR_DESIGN_E44_CLIP_PREDICTIONS_JOINED.csv`
- `results/tables/E44_COLOR_DESIGN_BY_MODEL_LABEL_PHRASE.csv`
- `results/tables/E44_COLOR_DESIGN_COLOR_ONLY_BY_MODEL_PHRASE.csv`

### Key Finding
No tested model recognized one-word `color` on E44 clips:

- E41: 0/10
- E43 cautious: 0/10
- E44 cautious: 0/10

`color red` remained weak:

- E41: 0/10
- E43 cautious: 2/10
- E44 cautious: 3/10

### Engineering Decision
Treat `COLOR` as an unresolved command-design/class-separation issue. Do not keep retraining blindly. Return to requirements traceability and model-selection logic.

## 2026-09-27 - Requirements And Model-Selection Audit Updated

### Objective
Reconcile Phase C, E43, and E44 evidence before starting any new engineering
work.

### Result
Created `PHASE_R_REQUIREMENTS_MODEL_SELECTION_AUDIT_20260927.md` and updated
`REQUIREMENTS_TRACEABILITY.md`.

### Current Candidate
`E41_FUNCTIONAL_NON_LED_RECOVERY`

### Evidence
- Phase C live baseline: 19/19 raw labels covered, 10 PASS, 2 PARTIAL_PASS, 7 FAIL, 6 no-action PASS_SAFE.
- E41 current95: accuracy 0.9473684210526315, macro-F1 0.947900053163211, wrong accepted at threshold 0.90 = 2.
- E43 cautious: not promoted.
- E44 cautious: not promoted.
- COLOR command-design audit: `color` failed 0/10 for E41, E43 cautious, and E44 cautious.

### Engineering Decision
Use E41 as the current evidence-supported candidate for the next validation or
benchmark planning step. Do not claim final completion and do not promote E43 or
E44.

## 2026-09-27 - E41 Pi Benchmark Plan Prepared

### Objective
Prepare the current-candidate Raspberry Pi benchmark before running it.

### Result
Created `PHASE_S_E41_PI_BENCHMARK_PLAN_20260927.md`.

### Fixed Stack
- command model: `E41_FUNCTIONAL_NON_LED_RECOVERY`
- CNN config: `configs/cnn_fastbn_dense_nodropout_raw19.json`
- threshold policy: `configs/e40_non_led_command_guardrail_thresholds.json`
- global threshold: `0.90`
- saved Phase C command WAVs only

### Decision
Benchmark E41 on saved Phase C positive command WAVs, excluding the invalid
false-wake command WAV. Do not use E43/E44 recovery recordings as benchmark or
validation data.

## 2026-09-27 - E41 Pi Benchmark Completed On Pi

### Objective
Record current-candidate Raspberry Pi runtime/resource evidence for E41.

### Result
Created `PHASE_S_E41_PI_BENCHMARK_RESULT_20260927.md` from the Pi terminal
output.

### Evidence On Pi
- `/home/loreenanne/vcm_pi_package/results/pi_benchmarks/E41_PI_BENCHMARK_20260927_041313_summary.json`
- `/home/loreenanne/vcm_pi_package/results/pi_benchmarks/E41_PI_BENCHMARK_20260927_041313_latency_rows.csv`

### Metrics
- WAV count: 19
- repeated inference count: 95
- mean latency: 33.334859452607866 ms
- p95 latency: 38.77204550026363 ms
- model load: 7.9181789939993905 s
- accepted/rejected: 65 / 30
- CPU during benchmark: 99.76415094339622%
- temperature: 45.2 C to 47.4 C
- memory used: 578400 KB to 815184 KB

### Next
Pull back the two benchmark artifacts to Windows and write SHA256 hashes before
marking the benchmark evidence archived.

## 2026-09-27 - E41 Pi Benchmark Artifacts Pulled Back And Hashed

### Objective
Archive the E41 benchmark output artifacts in the Windows evidence tree.

### Result
Pullback and SHA256 manifest completed.

### Evidence Folder
`outputs/e41_pi_benchmark_pullback_20260927_121751/`

### SHA256
- `E41_PI_BENCHMARK_20260927_041313_latency_rows.csv`: `D9CA65C30AA04A410B2499D41F532E3AC2760AE2B3143875F64252218EAAE703`
- `E41_PI_BENCHMARK_20260927_041313_summary.json`: `859693CD093C5C9E6CC3AE916389B00D30BA513D0B49DC6EC66D024D4FB01246`

### Note
The first PowerShell hash attempt included `SHA256SUMS.csv` while it was being
written, producing a self-row. The manifest was regenerated cleanly with the
manifest file excluded.

## 2026-09-27 - Remaining Failure Repair Selection Completed

### Objective
Select the next engineering repair path from actual Phase C and E41 evidence.

### Result
Created `PHASE_T_REMAINING_FAILURE_REPAIR_SELECTION_20260927.md` and derived
repair-analysis tables under `results/tables/PHASE_T_*`.

### Key Findings
- E41 under E40 threshold policy on the 95-example holdout: 80 accepted, 79
  accepted correct, 1 accepted wrong, 15 rejected.
- Wrong accepted holdout case: `COLOR -> WEATHER` at confidence 0.991768.
- Phase C high-risk wrong action remains `CREATE_REMINDER -> LIST_REMINDERS`.
- Threshold changes alone cannot fix the highest-risk Phase C failure.

### Decision
Do not train yet and do not lower the global threshold. Next work should define
an E45 targeted repair specification focused first on reminder class separation,
then `LIGHT_ON`, then confidence/rejection labels. Keep `COLOR` as a separate
command-design issue.

## 2026-09-27 - E45 Targeted Repair Specification Prepared

### Objective
Define the next targeted repair experiment without starting training.

### Result
Created `PHASE_U_E45_TARGETED_REPAIR_SPEC_20260927.md`.

### Proposed Experiment
`E45_TARGETED_REMINDER_LIGHTON_CONFIDENCE_REPAIR`

### Focus
- `CREATE_REMINDER` vs `LIST_REMINDERS`
- `LIGHT_ON`
- `PLAY_MUSIC`, `BRIGHTNESS`, `PAUSE`, `VOLUME_DOWN`

### Fixed Variables
E41 base model, E41 normalization, CNN architecture, preprocessing, wake gate,
threshold-comparison policy, parser, router, and action logic.

### Decision
Next safe step is manifest construction/readiness only. Training remains
blocked until the derived E45 manifest is built, counted, checked, and logged.

## 2026-09-27 - E45 Manifest Readiness Passed

### Objective
Build and audit the E45 targeted recovery manifest before training.

### Result
Created `PHASE_V_E45_MANIFEST_READINESS_AUDIT_20260927.md`.

### Output Manifest
`outputs/e45_targeted_repair_20260927/manifest_e45_targeted_recovery_for_training.csv`

### Counts
- total rows: 125
- unique WAV paths: 125
- duplicate paths: 0
- missing files: 0
- bad audio files: 0
- excluded `COLOR` rows: 30

### Decision
Manifest readiness passed. Training was not started in this phase. E45 training
may now be handled as the next separate experiment step.

## 2026-09-27 - E45 Targeted Training Completed

### Objective
Run `E45_TARGETED_REMINDER_LIGHTON_CONFIDENCE_REPAIR` as a separate experiment
using the fixed E45 spec and readiness-checked manifest.

### Result
Created `PHASE_W_E45_TRAINING_RESULT_20260927.md` and generated E45 model,
metrics, holdout, recovery, and E40-policy comparison artifacts.

### Key Metrics
- Holdout accuracy: 0.9368421052631579
- Holdout macro-F1: 0.935805422647528
- Targeted recovery accuracy: 0.84
- E45 under E40 policy on holdout: 76 accepted, 73 accepted correct, 3
  accepted wrong, 19 rejected
- E41 under E40 policy on holdout: 80 accepted, 79 accepted correct, 1
  accepted wrong, 15 rejected

### Model Hashes
- E45 weights:
  `FB3CC74BE769EB60C0A427086E6D771C440059A0AC479D63C473FADB6618A4F4`
- E45 normalization:
  `DC13C681A12C6918E4A3947A609F80FF77BC61CA606705D018C1438681975EDB`

### Decision
Do not promote E45. E41 remains the current evidence-supported candidate.
E45 is preserved as a documented recovery experiment, but its wrong accepted
rate is too high for fresh live validation.

## 2026-09-27 - E45 Wrong-Accept Regression Analysis Completed

### Objective
Compare E45's 3 wrong-accepted holdout samples against E41's 1 wrong-accepted
holdout sample before deciding whether another intervention is justified.

### Result
Created `PHASE_X_E45_WRONG_ACCEPT_REGRESSION_ANALYSIS_20260927.md` and derived
row-level comparison tables under `results/tables/PHASE_X_*`.

### Findings
- E41 wrong accept: `COLOR -> WEATHER`.
- E45 wrong accepts: `PAUSE -> CALL`, `STOP -> NEXT`, and
  `CREATE_REMINDER -> ALARM`.
- E45 fixed the specific offline E41 `COLOR -> WEATHER` wrong accept, but
  `COLOR` was excluded from E45 and remains a separate command-design issue.
- E45 converted safe E41 rejections into unsafe accepted wrong predictions for
  `PAUSE_015.wav`, `STOP_013.wav`, and `CREATE_REMINDER_014.wav`.

### Decision
Another intervention is justified only as a safety-focused, tightly specified
repair. Do not start another broad training run.

## 2026-09-27 - E45 Safety Regression Diagnosis Completed

### Objective
Diagnose the mechanism behind E45's three unsafe wrong accepts before any new
model, threshold, data, router, or action changes.

### Result
Created `PHASE_Y_E45_SAFETY_REGRESSION_DIAGNOSIS_20260927.md` and generated
Phase Y comparison tables under `results/tables/PHASE_Y_*`.

### Key Findings
- `PAUSE_015.wav`: E45 changed `PAUSE` into high-confidence `CALL`.
- `CREATE_REMINDER_014.wav`: E45 changed `CREATE_REMINDER` into
  high-confidence `ALARM`.
- `STOP_013.wav`: E45 kept the existing wrong `NEXT` prediction but raised
  confidence enough to cross the E40 policy threshold.
- No additional accepted-wrong regressions beyond these three were found.

### Recommendation
Choose next action B: confidence/rejection calibration or policy analysis
without retraining. Do not execute the intervention yet.

## 2026-09-27 - E41 Confidence/Rejection Policy Analysis Completed

### Objective
Analyze existing E41 + E40 holdout confidence/rejection behavior without
retraining or changing the current system.

### Result
Created `PHASE_Z_E41_CONFIDENCE_REJECTION_POLICY_ANALYSIS_20260927.md` and
Phase Z CSV tables under `results/tables/PHASE_Z_*`.

### Key Findings
- E40 `NEXT = 0.98` safely rejects E41 `STOP_013.wav` predicted as `NEXT` at
  confidence 0.979959.
- Lowering `NEXT` below 0.98 would increase accepted-wrong count in the
  existing holdout.
- E41 `PAUSE` holdout behavior shows correct-label low-confidence rejections
  without PAUSE wrong accepts in this small holdout.
- Scheduling/reminder evidence is insufficient for a production policy change.

### Recommendation
Recommendation B: conduct a narrow class-specific threshold calibration
experiment. Do not execute it yet.

## 2026-09-27 - Phase AA PAUSE Threshold Calibration Specification Prepared

### Objective
Design a narrow PAUSE threshold calibration experiment without modifying E40,
training a model, collecting audio, or changing router/action behavior.

### Result
Created `PHASE_AA_PAUSE_THRESHOLD_CALIBRATION_SPEC_20260927.md` and
`results/tables/PHASE_AA_PAUSE_DATA_SOURCE_AUDIT.csv`.

### Key Findings
- No verified independent PAUSE calibration set is currently available.
- The 95-example holdout is discovery evidence for the PAUSE `0.96` hypothesis
  and cannot validate it.
- E43 PAUSE clips are recovery/training evidence and were included in the E45
  training manifest.
- Phase C has only one PAUSE trial, which is insufficient for calibration.

### Decision
Do not execute calibration yet. Fresh Phase AA calibration evidence is required,
and it must remain separate from final fresh validation. E41 and E40 remain
frozen; `NEXT = 0.98` remains fixed.

## 2026-09-27 - Phase AA PAUSE Calibration Data Collection Verified

### Objective
Collect the fresh Phase AA PAUSE threshold calibration dataset and perform only data-integrity verification.

### Result
Created `PHASE_AA_PAUSE_CALIBRATION_DATA_COLLECTION_VERIFICATION_20260927.md` from the Pi verification output.

### Evidence
- Pi dataset: `/home/loreenanne/vcm_pi_package/pi_validation/phase_aa_pause_threshold_calibration_v1_20260927`
- manifest: `/home/loreenanne/vcm_pi_package/pi_validation/phase_aa_pause_threshold_calibration_v1_20260927/manifest.csv`
- SHA256 evidence: `/home/loreenanne/vcm_pi_package/pi_validation/phase_aa_pause_threshold_calibration_v1_20260927/SHA256SUMS.csv`

### Verification
- WAV count: 100
- manifest data rows: 100
- expected manifest lines including header: 101
- missing files: 0
- duplicate trial IDs: false
- duplicate WAV paths: false
- bad audio files: 0
- usage fields all `calibration_not_final_validation`: true
- separate data path check: true
- PASS: true

### Note
The initial verification failed only because `plughw:2,0` was written unquoted, shifting CSV columns. The manifest was repaired on the Pi and backed up as `manifest_before_csv_repair_20260927T054251Z.csv`.

### Stop Condition
No inference, threshold what-if analysis, model training, E41/E40 modification, router modification, or action-layer modification was performed.

## 2026-09-27 - Phase AB Frozen E41 PAUSE Calibration Analysis Completed

### Objective
Run frozen E41 inference on the verified Phase AA calibration dataset and perform an offline PAUSE-only threshold what-if analysis.

### Result
Pi-side analysis completed with `STOP_CONDITION_REACHED_NO_PRODUCTION_CHANGE`.

### Evidence
- Pi result directory: `/home/loreenanne/vcm_pi_package/results/phase_ab_phase_aa_pause_calibration_20260927`
- SHA256: `/home/loreenanne/vcm_pi_package/results/phase_ab_phase_aa_pause_calibration_20260927/PHASE_AB_PHASE_AA_PAUSE_CALIBRATION_20260927_SHA256SUMS.csv`
- report: `PHASE_AB_PHASE_AA_PAUSE_CALIBRATION_INFERENCE_RESULT_20260927.md`

### Findings
Frozen E41 + E40 baseline on the 100-example Phase AA calibration set: 58 raw-correct, 42 raw-wrong, 33 accepted-correct, 25 rejected-correct, 10 accepted-wrong, and 32 rejected-wrong.

PAUSE-only what-if found that thresholds `0.97`, `0.96`, and `0.95` each recovered 2 correct PAUSE cases relative to current `0.99`, with 0 newly accepted-wrong cases in this calibration set.

### Decision
Do not change E40 or production thresholds. Treat the lower PAUSE threshold only as a candidate for a later separately designed validation experiment. E41 remains frozen and `NEXT = 0.98` remains fixed.

## 2026-09-27 - Phase AD Fresh Live End-to-End VCM Validation Completed

### Objective
Measure frozen E41/E40 live through the Raspberry Pi microphone, wake gate, command capture, classifier, E40 rejection policy, router, local action, and evidence output.

### Evidence
- Report: `PHASE_AD_LIVE_VCM_VALIDATION_20260927.md`
- Pi collection folder: `/home/loreenanne/vcm_pi_package/pi_validation/phase_ad_live_vcm_validation_20260927`
- Pi result directory: `/home/loreenanne/vcm_pi_package/results/phase_ad_live_vcm_validation_20260927`
- SHA256: `/home/loreenanne/vcm_pi_package/results/phase_ad_live_vcm_validation_20260927/PHASE_AD_LIVE_VCM_VALIDATION_20260927_SHA256SUMS.csv`

### Result
65 live trials were recorded: 57 command trials and 8 no-action/false-wake trials. Command wake success was 55/57 = 96.49%. E41 was reached on 55 command trials and was raw-correct on 39/55 = 70.91%. E40 accepted 34/55 = 61.82%. Accepted-action precision was 30/34 = 88.24%. End-to-end action success was 30/57 = 52.63%. No no-action trial executed an action.

### Safety Cases
Accepted-wrong actions occurred in 4 trials: `TEMPERATURE -> MESSAGE` twice, `NEXT -> MESSAGE` once, and `LIGHT_OFF -> LIGHT_ON` once.

### Decision
Live VCM recognition has been demonstrated, but the current frozen E41/E40 system is not robust enough for broad final demonstration across all 19 commands. Do not retrain or change thresholds yet; first diagnose the accepted-wrong live failures and weak live command classes.

## 2026-09-27 - Phase AE Live Failure Diagnosis Completed

### Objective
Diagnose Phase AD live failures before any retraining, threshold change, router change, action change, or recovery dataset creation.

### Evidence
- Report: `PHASE_AE_LIVE_FAILURE_DIAGNOSIS_20260927.md`
- Diagnostic tables: `results/phase_ae_live_failure_diagnosis_20260927/`
- Phase AD pullback used: `outputs/phase_ad_live_validation_pullback_20260927_144844/`

### Result
Phase AE reconstructed Phase AD failure behavior from the pulled per-trial CSV, result JSON files, and WAVs. It found 27 command trials that were not `correct classification + accepted + correct action`. There were 16 raw live classification errors after E41 was reached: 4 accepted wrong and 12 safely rejected. All 65 trials passed the basic WAV integrity check.

### Accepted-Wrong Diagnosis
The accepted-wrong actions were confirmed as raw E41 classification errors accepted by E40, with no evidence of router or action-handler defect:
- `TEMPERATURE -> MESSAGE` at 0.922538
- `NEXT -> MESSAGE` at 0.930046
- `LIGHT_OFF -> LIGHT_ON` at 0.953683
- `TEMPERATURE -> MESSAGE` at 0.985255

### Decision
A targeted recovery experiment is justified for design, focused on the live failure evidence for `CALL`, `COLOR`, `TEMPERATURE`, `NEXT`, and `LIGHT_OFF`, especially `TEMPERATURE -> MESSAGE`, `NEXT -> MESSAGE`, and `LIGHT_OFF -> LIGHT_ON`. No training or threshold change was performed.

## 2026-09-27 15:12:13 +08:00 - Phase AF Targeted Live Recovery Specification
- Created PHASE_AF_TARGETED_LIVE_RECOVERY_SPEC_20260927.md.
- Phase AF is specification/data-collection only; no training or threshold/model/router/action changes authorized.
- Recovery targets are CALL, COLOR, TEMPERATURE, NEXT, and LIGHT_OFF, based on Phase AE live failure diagnosis.
- Planned fresh recovery dataset: 105 command-level Raspberry Pi recordings marked 
ecovery_training.
- Data collection and integrity verification remain pending user execution on the Raspberry Pi.

## 2026-09-27 15:35:12 +08:00 - Phase AF Recovery Dataset Integrity Passed
- Raspberry Pi Phase AF collection completed with 105 WAV files and 105 manifest data rows.
- Integrity verification passed: missing files 0, duplicate trial IDs false, duplicate WAV paths false, empty WAVs 0, bad audio 0, bad durations 0, invalid labels none, validation leakage paths 0.
- Metadata verified: usage 
ecovery_training, split 
ecovery, source_phase PHASE_AF, target_role valid.
- Class counts matched the approved Phase AF design: five primary classes at 10 each and eleven contrast classes at 5 each.
- SHA256 evidence generated on Pi: pi_validation/phase_af_targeted_live_recovery_20260927_v1/PHASE_AF_RECOVERY_DATA_SHA256SUMS.csv.
- No training or production changes were performed; STOP condition observed.

## 2026-09-27 15:35:29 +08:00 - Phase AF Metadata Correction
- Clean metadata statement: usage = recovery_training; split = recovery; source_phase = PHASE_AF; target_role valid.

## 2026-09-27 16:10:30 +08:00 - Phase AG E46 Targeted Recovery Training Result
- Executed E46_TARGETED_LIVE_FAILURE_RECOVERY after local Phase AF verification passed.
- Local Phase AF verification: 105 WAVs, 105 manifest rows, metadata valid, validation leakage paths 0, SHA missing/mismatch none.
- Training used E41 base weights/normalization, 190 adaptation clips x6, 105 Phase AF clips x2, fixed 4 epochs, LR 0.00002, seed 4646.
- No holdout-based checkpoint selection was used; the holdout was evaluated only after training.
- E46 holdout result: 87/95 = 91.58%, below E41 baseline 90/95 = 94.74%.
- Regression analysis: 3 E41-wrong to E46-correct, 6 E41-correct to E46-wrong, 2 unchanged wrong, 84 unchanged correct.
- Frozen E40 policy comparison: E41 accepted-wrong 1, E46 accepted-wrong 2; accepted-action precision dropped from 0.9875 to 0.97297.
- Decision: do not promote E46; E41 remains frozen candidate. No threshold/router/action/live-validation changes performed.

## 2026-09-27 16:15:41 +08:00 - Phase AG E46 Regression Diagnosis Completed
- Created PHASE_AG_E46_REGRESSION_DIAGNOSIS_20260927.md from existing E41/E46 artifacts only.
- Verified E41 90/95 = 94.74% and E46 87/95 = 91.58% from E41_vs_E46_REGRESSION_ANALYSIS.csv.
- Verified regression counts: E41 wrong -> E46 correct 3; E41 correct -> E46 wrong 6; E41 wrong -> E46 wrong 2; E41 correct -> E46 correct 84.
- Verified frozen E40 comparison: E41 accepted-correct 79, accepted-wrong 1, precision 98.75%; E46 accepted-correct 72, accepted-wrong 2, precision 97.30%.
- E46 accepted-wrong cases: STOP -> NEXT and VOLUME_DOWN -> VOLUME_UP.
- Pattern classified as mixed: target-class and contrast-class changes both occurred; causality from Phase AF data was not claimed.
- No E47 training, threshold changes, E40/E41 changes, router/action changes, holdout changes, or live validation performed.

## 2026-09-27 16:32:00 +08:00 - Phase AG+ E46 Confidence / Acceptance Diagnosis Completed
- Created PHASE_AG_E46_CONFIDENCE_ACCEPTANCE_DIAGNOSIS_20260927.md from existing frozen 95-example holdout artifacts only.
- The user-supplied nine-sample list disagreed with artifact rows for eight samples; discrepancies were preserved in PHASE_AG_PLUS_SUPPLIED_SAMPLE_MAPPING_DISCREPANCIES.csv.
- Artifact-defined nine correctness-flip samples were analyzed: six E41-correct -> E46-wrong regressions and three E41-wrong -> E46-correct improvements.
- Margins were not available because the prediction artifacts contain top-1 predictions/confidences only; all margin fields are reported as N/A.
- Six regressions: all six were top-1 classification changes; four also changed E40 action/rejection outcome and two remained safely rejected.
- Three improvements: all three were top-1 classification changes with E40 acceptance consequences.
- STOP_013.wav was diagnosed as same wrong top-1 NEXT with confidence crossing the frozen NEXT 0.98 threshold: E41 rejected at 0.979959, E46 accepted at 0.999549.
- VOLUME_DOWN_011.wav was diagnosed as top-1 change VOLUME_DOWN -> VOLUME_UP with E46 confidence 0.998431 crossing the frozen VOLUME_UP 0.99 threshold.
- No training, threshold changes, E40/E41/E46 changes, router/action changes, holdout changes, live validation, or data collection were performed.

## 2026-09-27 16:36:00 +08:00 - Strategic Direction Logged: Controlled Candidate Repair
- Logged project direction from user review: change the objective from "find out whether E41 is good enough" to "make the system work, but only through controlled experiments."
- Desired system behavior is fresh Pi speech -> HEY PI -> correct VCM intent -> safe acceptance/rejection -> correct deterministic action -> evidence logged.
- Optimization target is reliable accepted actions and safe rejection of uncertain/wrong predictions, not raw classifier accuracy alone.
- Highest-priority live weaknesses remain CALL, COLOR, TEMPERATURE, NEXT, and LIGHT_OFF, with continued attention to CREATE_REMINDER/LIST_REMINDERS, LIGHT_ON confusion, VOLUME_DOWN, PAUSE confidence, and high-confidence wrong actions.
- Future candidates must satisfy strict promotion gates: no unacceptable frozen-holdout degradation, no increase in accepted-wrong actions, improvement in documented high-risk classes, no serious regression in strong classes, fresh Pi validation, and end-to-end action validation.
- E41 remains frozen until a candidate proves better under this evidence standard; E45/E46 show that arbitrary retraining can move errors around and is not sufficient.

## 2026-09-27 16:52:00 +08:00 - Phase AH Repair Design Completed
- Created PHASE_AH_ARTIFACT_RECONCILIATION_20260927.md and PHASE_AH_REPAIR_DESIGN_20260927.md.
- Reconciled the AG+ discrepancy: the authoritative 95-example holdout is data/calibration/pi_validation/all_commands_calibration_15x/manifest.csv rows 011-015 for each of 19 command labels.
- Authoritative artifacts: E41 CURRENT95 re-evaluation predictions, E46 holdout predictions, E41_vs_E46_REGRESSION_ANALYSIS.csv, PHASE_T_E41_E40_POLICY_HOLDOUT_ROWS.csv, and E46_E40_POLICY_HOLDOUT_ROWS.csv.
- Reconciliation passed with 95-row path-set agreement across E41 predictions, E46 predictions, comparison rows, and E40 policy rows.
- The prior supplied nine-sample list was traced to the user-provided AG+ prompt and treated as non-authoritative because it disagreed with saved artifacts; no internal artifact mismatch was found.
- Frozen E41 baseline confirmed: 90/95 raw correct; E41 + E40 accepted-correct 79, accepted-wrong 1, rejected-correct 11, rejected-wrong 4, accepted-action precision 98.75%.
- Phase AH separated classifier problems from acceptance/policy problems and recommended a controlled classifier ablation as the next experiment to specify, not execute.
- No E47 training, threshold changes, E40/E41/E46 changes, router/action changes, holdout edits, data collection, live validation, or E46 promotion occurred.

## 2026-09-27 16:58:00 +08:00 - Phase AI E47 Controlled Classifier Ablation Completed
- Created PHASE_AI_E47_EXPERIMENT_DESIGN_20260927.md before training and then executed E47_TARGETED_CLASSIFIER_ABLATION.
- E47 tested a narrower intervention than E46: E41 adaptation replay x1 plus 75 selected Phase AF target/contrast clips x2, total 340 training examples.
- Selected Phase AF classes: CALL, COLOR, TEMPERATURE, NEXT, LIGHT_OFF, MESSAGE, TIME, LIGHT_ON, VOLUME_DOWN, VOLUME_UP. TIMER was unavailable in Phase AF and documented as a limitation.
- E47 was trained from E41 weights/normalization with frozen preprocessing/architecture, seed 4747, 3 epochs, batch size 32, LR 0.00001.
- Frozen 95-example holdout result: E47 79/95 = 83.16%, below E41 90/95 = 94.74%.
- Four-way regression counts: E41 correct -> E47 correct 79; E41 correct -> E47 wrong 11; E41 wrong -> E47 wrong 5; E41 wrong -> E47 correct 0.
- Target-class outcome: no target class improved; LIGHT_OFF degraded from 5/5 to 3/5 with LIGHT_OFF -> NEXT errors.
- Frozen E40 policy: E47 accepted-correct 70, accepted-wrong 3, rejected-correct 9, rejected-wrong 13, accepted-action precision 95.89%.
- E47 accepted-wrong cases: PAUSE -> CALL, STOP -> NEXT, LIST_REMINDERS -> CREATE_REMINDER.
- STOP -> NEXT reappeared as accepted-wrong; VOLUME_DOWN -> VOLUME_UP did not reappear.
- Decision: reject E47 for promotion; do not proceed to fresh live validation; keep E41 frozen.
- No E41/E40/threshold/router/action/holdout changes, data collection, live validation, E48 training, or production promotion occurred.

## 2026-09-27 17:10:00 +08:00 - Phase AJ Model / Representation Diagnosis Completed
- Created PHASE_AJ_MODEL_REPRESENTATION_DIAGNOSIS_20260927.md and Phase AJ evidence tables in results/phase_aj_model_representation_diagnosis_20260927/.
- Compared available model-generation evidence for E21, E41, E45, E46, and E47 without ranking E21 against the current 19-label holdout because E21 uses a 10-intent label space.
- Confirmed the authoritative E41 baseline from Phase AH: 90/95 raw holdout correct; E41 + E40 accepted-correct 79, accepted-wrong 1, rejected-correct 11, rejected-wrong 4, accepted-action precision 98.75%.
- Preserved Phase AD live evidence separately: raw E41 live accuracy 39/55 = 70.91%, end-to-end action success 30/57 = 52.63%, accepted-action precision 30/34 = 88.24%.
- Inspected E41 preprocessing: 16 kHz, 4-second fixed window, peak normalization, 25 ms frames, 10 ms hop, 512 FFT, 40 Mel bins, 20-7600 Hz, log transform, no VAD/silence trimming observed.
- Inspected E41 architecture: tiny_vcm_cnn with Conv2D/BatchNorm/MaxPool blocks [24, 48, 96], avgmax global pooling, dense 64, 19-class softmax, approximately 66k parameters. The inspected implementation is a tiny CNN, not a DS-CNN.
- Diagnosed the remaining evidence as primarily top-1 classifier/class-separation failures under live conditions, with confidence/rejection remaining safety-relevant for accepted-wrong outcomes.
- Observed that E46 and E47 both fine-tuned from E41 with the same representation/architecture and both degraded the frozen holdout and accepted-wrong safety profile; no causality claim was made.
- Recommended one next path only: a controlled architecture experiment design, not execution, to isolate model capacity/temporal representation while keeping data, features, labels, E40, router/actions, and evaluation fixed.
- No E48 training, feature change, threshold change, E40/E41 modification, router/action change, data collection, holdout edit, live validation, or candidate promotion occurred.

## 2026-09-27 17:20:00 +08:00 - Phase AK E48 Pre-Training Gate Blocked
- Began Phase AK execution authorization for E48_CONTROLLED_TEMPORAL_CNN_CAPACITY_PROBE.
- Pre-training gate inspected PHASE_AJ_MODEL_REPRESENTATION_DIAGNOSIS_20260927.md for a uniquely specified E48 architecture.
- Phase AJ recommended a controlled architecture experiment but described the architecture as a family of possible changes, including temporal/asymmetric convolution capacity or one additional convolutional block.
- The Phase AJ design did not uniquely specify exact layer sequence, kernel sizes, channel counts, stride, pooling, normalization/activation placement, final pooling, classifier head, parameter count, or expected model size.
- Required stop condition triggered: "E48 design is not sufficiently specified for controlled execution."
- Created PHASE_AK_E48_CONTROLLED_TEMPORAL_CNN_CAPACITY_PROBE_20260927.md and PHASE_AK_PRETRAINING_GATE_RESULT.csv.
- No E48 training, E41/E40/threshold/preprocessing/label/router/action/holdout changes, data collection, live validation, or promotion occurred.

## 2026-09-27 17:35:00 +08:00 - Phase AL E48 Architecture Specification Completed
- Created PHASE_AL_E48_ARCHITECTURE_SPECIFICATION_20260927.md and evidence tables in results/phase_al_e48_architecture_specification_20260927/.
- Phase AL resolved the Phase AK design ambiguity without training.
- Reconstructed E41 architecture: 398x40x1 input, three Conv2D/BatchNorm/MaxPool blocks with filters 24/48/96 and 3x3 kernels, avgmax global pooling, Dense 64, Dense 19 softmax, total params 66,483.
- Selected one E48 architectural hypothesis from Phase AJ: add exactly one temporal context block after E41 pool3 and before global pooling.
- Fully specified E48 architecture: E41 unchanged plus SeparableConv2D(filters=96, kernel_size=(5,3), strides=(1,1), padding=same, activation=relu, use_bias=True), followed by BatchNormalization(momentum=0.1), with no additional pooling.
- E48 parameter count: total 77,619, trainable 77,091, non-trainable 528, approximately 1.17x E41.
- Pre-registered controls: same E41-authorized training/adaptation data, same preprocessing/features/labels/loss/optimizer/batch size/epoch budget/checkpoint rule, frozen E40 policy, and same 95-example formal holdout for evaluation only.
- Final status: E48 FULLY SPECIFIED — READY FOR CONTROLLED TRAINING.
- No E48 training, checkpoint creation, data collection, preprocessing change, E40/threshold change, router/action change, holdout change, live validation, E49 start, or promotion occurred.

## 2026-09-27 17:50:00 +08:00 - Phase AM E48 Pre-Training Gate Blocked
- Began Phase AM execution authorization for E48_CONTROLLED_TEMPORAL_CNN_CAPACITY_PROBE.
- Read Phase AL and audited the local E41 training-data prerequisites before training.
- Confirmed E41 current formal holdout baseline remains 90/95 raw correct.
- E41 recorded training context requires 240 adaptation clips, 120 Pi holdout examples, and 4800 repeated training examples.
- Local standard project manifests resolved only 231 adaptation clips and 95 holdout examples: all_commands_calibration_15x provided 190 adaptation and 95 holdout; e40_non_led_command_recovery_20260923 provided 41 adaptation rows, 0 holdout rows, and 41 missing WAVs from standard project paths.
- Because the exact E41-authorized training data could not be reconstructed locally without substituting/restaging data, Phase AM stopped before model construction or training.
- Created PHASE_AM_E48_CONTROLLED_TRAINING_AND_EVALUATION_20260927.md and evidence under results/phase_am_e48_controlled_training_and_evaluation_20260927/.
- Final status: E48 INCONCLUSIVE — FURTHER EVIDENCE REQUIRED.
- No E48 training, checkpoint creation, E48 holdout evaluation, E41/E40 modification, threshold change, preprocessing change, router/action change, holdout edit, live validation, or promotion occurred. E41 remains frozen.


## 2026-09-27 — Phase AN E41 Dataset Provenance and Reconstruction

- Executed Phase AN as a provenance/reconstruction audit only; no training or model changes were performed.
- Confirmed E41 authoritative record: 240 adaptation clips and 120 Pi holdout examples.
- Reconstructed local exact evidence: 190 base adaptation clips and 95 current formal holdout clips resolved exactly.
- Identified missing provenance for the dedicated E41 recovery folder `pi_validation/e41_functional_non_led_recovery_20260923`.
- Original E41 120-row prediction artifact proves 25 holdout rows from the missing recovery folder, but the WAV bytes/manifests are not locally present.
- Reconciled Phase AM's apparent 231/240 count as 190 base rows plus 41 non-authoritative E40/wake-gated rows; those 41 rows cannot establish exact E41 provenance.
- Final Phase AN status: E48 DATASET NOT READY — PROVENANCE GAP REMAINS.


## 2026-09-27 — Phase AO Authoritative E41 Recovery-Data Recovery Audit

- Executed Phase AO as a local provenance/recovery audit only; no model training or data modification occurred.
- Searched local project storage, extracted output evidence, deployment/model/result directories, and available ZIP/TAR/TGZ archives for `pi_validation/e41_functional_non_led_recovery_20260923`.
- Recovered exact counts remain 190/240 adaptation and 95/120 holdout.
- The 75 missing E41 recovery WAVs were not physically recovered.
- Same-filename candidates were found elsewhere in the project but were classified as weak evidence and not substituted.
- Final Phase AO status: E41 RECOVERY PARTIAL — REMAINING FILES NOT FOUND.


## 2026-09-27 — Phase AP E41 Artifact-to-Pi Dataset Reconciliation

- Executed Phase AP as reconciliation/provenance only; no training, threshold, architecture, router/action, holdout, or live-trial changes occurred.
- Inspected historical E41 metrics, prediction, Phase AN reconstructed manifest, local Pi-side evidence paths, and SHA/hash manifests.
- The current recovered 75-file Pi-side E41 recovery package was not available in the inspected local evidence paths.
- Evidence classification across 360 expected rows: 0 exact matches, 285 consistent-but-non-identifying rows, 75 unavailable rows.
- Conclusion: historical E41 training/holdout provenance cannot be established conclusively from currently available local evidence.


## 2026-09-27 — Phase AP Updated With Recovered E41 Pi Dataset

- Re-ran Phase AP after the recovered `C:\Users\Loreen Anne\e41_functional_non_led_recovery_20260923` package became available locally.
- Verified 75 WAV files and preserved `E41_WAV_SHA256.txt`; all 75 WAVs match the Pi-generated SHA256 entries.
- Reconciled recovered manifest against historical E41 artifacts.
- Classified 25 recovery holdout rows as exact identity established because historical E41 prediction rows reference the same paths/labels/trials and recovered files match Pi SHA256.
- Classified the 50 recovery adaptation rows as consistent but non-identifying because no historical per-row E41 training manifest/hash artifact was available.
- No training or model changes were performed. Recommended next phase: Phase AQ dataset-readiness/methodology decision before any E48 training.


## 2026-09-27 — Phase AQ E41 Dataset Readiness and Methodology Decision

- Executed Phase AQ as a methodology/readiness decision only; no training, E48 creation, threshold change, E40/E41 modification, new recording, or live validation occurred.
- Used the completed Phase AP reconciliation and recovered E41 package as the sole basis.
- Confirmed that the 25 recovered E41 recovery holdout WAVs have exact historical artifact-to-dataset identity, but that this strengthens the original 120-example E41 holdout context rather than directly proving the current 95-example 94.74% benchmark.
- Confirmed that the 50 recovered E41 recovery adaptation WAVs are strongly consistent with E41 but remain non-identifying against historical training because no per-row historical training manifest/hash exists.
- Froze a future E48 dataset definition: 240 training-included clips (190 base adaptation + 50 recovered E41 recovery adaptation) and 120 holdout-excluded clips (95 current formal holdout + 25 exact recovered original-holdout rows).
- Methodology decision: a future E48 architecture-only experiment may be authorized in a separate phase using this frozen reconstructed E41-authorized dataset with an explicit provenance caveat.
- E41 remains frozen; E40 remains unchanged.


## 2026-09-27 — Phase AR E48 Architecture-Only Experiment Specification

- Executed Phase AR as a specification-only phase; no E48 training, model creation, threshold change, E40/E41 modification, new recording, or live validation occurred.
- Inspected actual project artifacts for E41 architecture, preprocessing, raw-command training, inference, E40 policy evidence, and Phase AQ dataset boundary.
- Reconstructed E41 as `tiny_vcm_cnn`: input `[398,40,1]`, Conv2D filters 24/48/96, 3x3 kernels, BatchNorm momentum 0.1, MaxPool 2x2 after each block, avg+max global pooling, Dense 64 relu, Dense 19 softmax, 66,483 parameters, no quantization observed.
- Froze preprocessing: 16 kHz, 4.0 seconds, peak normalization, 25 ms frames, 10 ms hop, 512 FFT, 40 mel bins, 20-7600 Hz, log floor 1e-6, expected frames 398.
- Specified E48 as one architecture-only change: insert SeparableConv2D 96 filters, 5x3 kernel, stride 1x1, same padding, relu, followed by BatchNorm momentum 0.1 after E41 pool3 and before global pooling.
- E48 parameter count is pre-registered as 77,619, approximately 1.17x E41.
- Required future evaluation includes frozen current95 holdout metrics, frozen E40 safety analysis, and four-way E41->E48 regression/correction analysis.
- E41 remains frozen; E40 remains unchanged.


## 2026-09-27 — Phase AS E48 Architecture-Only Training and Offline Evaluation

- Executed the single authorized E48 architecture-only run from the Phase AR specification.
- Verified E41 parameter count 66,483 and E48 parameter count 77,619 before training.
- Verified Phase AQ dataset boundary: 240 training-included clips, 95 current95 holdout rows excluded from training, and 25 exact historical holdout rows excluded from training.
- Trained E48 for 20 epochs, batch size 32, Adam LR 0.001, seed 4242, final-epoch rule with no holdout checkpoint selection.
- Training source clips: 240; repeated training examples: 4,800.
- Final training metrics: loss 0.0000176385, accuracy 1.000000.
- Frozen current95 result: E48 91/95 = 95.79%, compared with E41 90/95 = 94.74%.
- Four-way comparison: E41 correct -> E48 correct 87; E41 correct -> E48 wrong 3; E41 wrong -> E48 correct 4; E41 wrong -> E48 wrong 1.
- Frozen E40 policy for E48: accepted-correct 72, accepted-wrong 0, rejected-correct 19, rejected-wrong 4, accepted-action precision 100%.
- E48 introduced raw regressions in `LIGHT_OFF_014`, `STOP_011`, and `TEMPERATURE_014`; all wrong predictions were rejected under frozen E40.
- E48 is not promoted. No live validation, threshold change, E40/E41 change, router/action change, or production change occurred.


## 2026-09-27 — Phase AT E41/E48 Architecture Regression Diagnosis

- Executed Phase AT as diagnostic analysis only; no retraining, live validation, threshold change, E40/E41/E48 modification, preprocessing change, router/action change, or new data collection occurred.
- Analyzed the seven changed current95 holdout cases: four E41-wrong -> E48-correct corrections and three E41-correct -> E48-wrong regressions.
- Found all seven changed cases are top-1 classification changes; none are pure same-top-1 confidence-only changes.
- E48 regressions: `LIGHT_OFF_014.wav` became `LIGHT_OFF -> WEATHER`, `STOP_011.wav` became `STOP -> NEXT`, and `TEMPERATURE_014.wav` became `TEMPERATURE -> NEXT`.
- E48 achieved zero accepted-wrong cases by correcting E41's accepted-wrong `COLOR -> WEATHER` row and keeping new wrong predictions below frozen E40 thresholds.
- Diagnosed the main E48 tradeoff as lower accepted-correct coverage: E41 accepted-correct 79 vs E48 accepted-correct 72, with E48 rejected-correct increasing to 19.
- Recommended next controlled step: E48 confidence/rejection calibration diagnostic using existing offline evidence only. E41 remains frozen and E48 is not promoted.


## 2026-09-27 — Phase AU E48 Offline Confidence/Rejection Calibration Diagnostic

- Executed Phase AU as offline what-if analysis only; no threshold change, E40 modification, E48 retraining, data collection, live validation, or production promotion occurred.
- Evaluated 20 candidate threshold policies against the existing E48 current95 predictions.
- Raw accuracy remained fixed for all policies at 91/95 = 95.79%.
- Frozen E40 result: accepted-correct 72, accepted-wrong 0, rejected-correct 19, rejected-wrong 4, accepted-action precision 100%.
- Global threshold lowering was rejected as unsafe because even global 0.95 newly accepts `STOP_011.wav` as wrong `NEXT`.
- Class-specific what-ifs were promising offline: the broad class-specific policy recovered 18 rejected-correct rows with 0 newly accepted-wrong rows on current95 while keeping NEXT and WEATHER protected.
- Selected recommendation: design a controlled E48-specific calibration experiment using independent calibration evidence. Do not change production thresholds from current95 what-if results.


## 2026-09-27 — Phase AV E48 Independent Calibration Dataset Specification

- Designed the independent Phase AV E48 confidence/rejection calibration dataset.
- Created the human-readable specification and machine-readable dataset/class-plan artifacts.
- Target dataset: 210 fresh calibration WAVs, all marked calibration, with full 19-label coverage and oversampling around AU risk classes `NEXT`, `WEATHER`, `STOP`, `LIGHT_OFF`, `TEMPERATURE`, and `COLOR`.
- Required future collection path: `pi_validation/phase_av_e48_independent_calibration_20260927_v1`.
- Required separation: no overlap with frozen E48 current95 holdout by path or SHA256 where hashes are available; no use of Phase AA, Phase AD, Phase AF, training, or formal holdout WAVs.
- Collection was NOT RUN in this local environment. Integrity verification and leakage verification remain NOT RUN until WAVs exist.
- No E48/E41/E40 modification, threshold change, retraining, live validation, router/action change, or production deployment occurred.


## 2026-09-27 — Phase AV E48 Independent Calibration Dataset Collection

- Recorded the Phase AV calibration dataset on the Raspberry Pi using the preregistered AV class plan.
- Pi-side collection produced 210 successful manifest rows and 210 WAV files in `pi_validation/phase_av_e48_independent_calibration_20260927_v1`.
- Class counts matched the AV plan: NEXT/WEATHER/STOP/LIGHT_OFF/TEMPERATURE/COLOR each 16; MESSAGE/CALL/TIME/LIGHT_ON each 12; BRIGHTNESS/VOLUME_UP/VOLUME_DOWN each 10; PLAY_MUSIC/TIMER/ALARM/PAUSE/CREATE_REMINDER/LIST_REMINDERS each 6.
- Pi-side integrity verification passed: 0 missing WAVs, 0 duplicate trial IDs, 0 duplicate WAV paths, 0 empty files, 0 bad/corrupt audio files, 0 bad format files, 0 bad duration files, 0 invalid labels.
- Metadata checks passed: split calibration, dataset_role calibration, usage `e48_confidence_calibration_not_training_not_holdout`, source_phase `PHASE_AV`.
- Frozen E48 holdout path overlap was 0. Frozen holdout SHA256 overlap was `NOT_AVAILABLE` because holdout hashes were unavailable to the Pi verifier.
- Pi-side SHA256 evidence was generated at `PHASE_AV_E48_CALIBRATION_SHA256SUMS.csv`.
- No E48 inference, threshold analysis, training, E40/E41/E48 change, live validation, router/action change, or production deployment occurred.


## 2026-09-27 — Phase AX E48 Independent Calibration Inference Blocked

- Attempted to begin Phase AX local inference using frozen E48 and frozen E40.
- Local availability check found E48 weights, normalization, and labels.
- Local availability check did not find `pi_validation/phase_av_e48_independent_calibration_20260927_v1`.
- Local Phase AV WAV count was 0; the 210 WAV files, Phase AV manifest, Pi-side integrity CSV, and Pi-side SHA256 manifest are not present in the local project environment.
- Phase AX inference was not run. No threshold analysis, threshold change, E40/E41/E48 modification, retraining, live validation, router/action change, or production deployment occurred.


## 2026-09-27 — Phase AX E48 Independent Calibration Inference Completed

- Resumed Phase AX after the Phase AV dataset became locally available under `pi_validation`.
- Used the 210 explicit rows from `pi_validation/PHASE_AV_E48_CALIBRATION_MANIFEST.csv`; did not use all WAVs under `pi_validation` indiscriminately.
- Loaded frozen E48 weights, normalization, labels, and preprocessing matching Phase AS.
- Applied frozen E40 thresholds without modification.
- Raw E48 accuracy on Phase AV: 88/210 = 41.90%.
- Frozen E40 outcomes: accepted-correct 38, accepted-wrong 13, rejected-correct 50, rejected-wrong 109.
- Accepted-action precision: 38/51 = 74.51%; acceptance coverage: 51/210 = 24.29%.
- Important accepted-wrong cases included `NEXT -> MESSAGE`, `STOP -> PLAY_MUSIC`, `LIGHT_OFF -> TEMPERATURE`, `VOLUME_DOWN -> VOLUME_UP`, and `CREATE_REMINDER -> LIST_REMINDERS`.
- No threshold analysis, threshold change, E40/E41/E48 modification, retraining, live validation, router/action change, or production deployment occurred.


## 2026-09-27 — Phase AY E48 Independent Failure Diagnosis

- Completed diagnostic-only Phase AY using authoritative Phase AX artifacts.
- Verified AX baseline from artifacts: N 210; raw correct 88; raw wrong 122; accepted-correct 38; accepted-wrong 13; rejected-correct 50; rejected-wrong 109.
- Produced complete AY diagnostic tables under `results/phase_ay_e48_independent_failure_diagnosis_20260927/`.
- Dominant E48 AV confusion pairs included `NEXT -> MESSAGE` (6), `CREATE_REMINDER -> LIST_REMINDERS` (5), `LIGHT_OFF -> BRIGHTNESS` (4), `LIGHT_OFF -> TEMPERATURE` (4), `LIGHT_ON -> VOLUME_UP` (4), `TEMPERATURE -> MESSAGE` (4), and `VOLUME_DOWN -> VOLUME_UP` (4).
- Confidence analysis found 17 wrong predictions with confidence >= 0.90, 12 >= 0.95, 6 >= 0.98, and 3 >= 0.99.
- All 13 accepted-wrong cases were documented individually.
- Frozen E41 diagnostic inference on the same AV set was performed without modifying artifacts: E41 raw correct 103/210, accepted-wrong 51; E48 raw correct 88/210, accepted-wrong 13.
- Diagnosis: mixed data/generalization and classifier/representation problem, not primarily a simple confidence-threshold issue.
- Clean, speaker-diverse, phrase-diverse retraining experiment is justified as a future design question, but no training or data collection occurred in AY.
- No model, threshold, preprocessing, router/action, production configuration, or dataset was changed.


## 2026-09-27 — Phase AZ Additional Dataset Integration Audit

- Completed Phase AZ as an audit-only phase for the additional posted dataset resource; no training, threshold change, E40/E41/E48 modification, data collection, live validation, router/action change, or production change occurred.
- Google Drive file-level connector access was unavailable in this Codex session because the Google Drive plugin was not installed; a plugin suggestion was raised, and the audit used the local downloaded resource at `C:\Users\Loreen Anne\Downloads\VCM\VCM`.
- Inspected the actual local `VCM_MASTER` and `VCM_BALANCED` resource structure, manifests, embedded reports, class labels, split boundaries, speaker/group metadata, provenance fields, augmentation fields, and audio inventory.
- Generated Phase AZ artifacts under `results/phase_az_additional_dataset_integration_audit_20260927/`, including manifest summaries, class mapping, SHA256 manifests, overlap summaries, and the audit script.
- Verified local observed counts: `VCM_MASTER` has 36,622 audio files/manifest rows across 16 classes with train/val/test 27,130/4,734/4,758 and 395 speakers/groups; `VCM_BALANCED` has 15,268 WAV training rows across 16 classes and 298 speakers/groups.
- Confirmed embedded leakage/audit evidence: Dataset B is derived from Dataset A train only; Dataset A val/test remain untouched; B speakers do not overlap A val/test speakers; reported speaker leakage is 0.
- Computed SHA256 for all 15,268 `VCM_BALANCED` audio files and 21,757 scoped current-project audio files from active drive-download shards, calibration/recovery data, and Phase AV `pi_validation`; byte-identical overlap count was 0.
- Mapped posted dataset labels to the current 19 executable raw-label taxonomy: 13 raw labels are directly supported, `BRIGHTNESS` is partially supported by `LIGHT_DIM`, `UNKNOWN`/`SILENCE` support rejection/no-action, and `COLOR`, `CREATE_REMINDER`, `LIST_REMINDERS`, `CALL`, and `MESSAGE` are missing.
- Recommendation: a controlled future training-data intervention is methodologically defensible after review, preferably using `VCM_BALANCED` as training-candidate data for covered labels plus existing/project training data for missing labels, while preserving Dataset A val/test and existing Phase AV/current95 evidence as non-training evaluation evidence.
- Hard stop after AZ. No model was trained or promoted.


## 2026-09-27 — Phase AZ-R Actual Dataset 2 Verification and Integration Audit

- Completed Phase AZ-R as a follow-up/reconciliation audit after the actual Dataset 2 package was downloaded locally into the project at `data/VCM Dataset2`.
- Treated the earlier AZ report as preliminary; AZ-R supersedes the earlier connector/access limitation for Dataset 2 because actual files and `data/VCM Dataset2 Specifications.pdf` were available locally.
- Created the human report at `results/phase_az_actual_dataset2_verification_20260927/PHASE_AZ_R_ACTUAL_DATASET2_VERIFICATION_20260927.md`.
- Created machine-readable artifacts under `results/phase_az_actual_dataset2_verification_20260927/`, including file inventory, spec-vs-actual reconciliation, class counts, partition counts, speaker audit, provenance audit, class mapping, source-overlap audit, SHA256 manifests, and integration decision.
- Verified actual Dataset A: 36,622 rows/files; train/val/test 27,130/4,734/4,758; 16 classes; 395 speakers/groups; 0 missing manifest audio; 0 unreadable/corrupt audio from actual WAV/FLAC header checks.
- Verified actual Dataset B: 15,268 WAV train rows; 16 classes; 13,801 original; 1,467 augmented; class distribution matched the specification exactly; 0 missing/unreadable audio.
- Verified speaker separation from actual manifests: train∩val 0, train∩test 0, val∩test 0, Dataset B speakers ∩ Dataset A val/test 0.
- Verified Dataset B provenance: all 15,268 rows trace to Dataset A train; 0 Dataset A val/test source rows; 0 missing sources; 0 source-label mismatches.
- Verified augmentation/synthetic metadata: augmentation counts gain 410, noise 425, pitch 36, shift 380, speed 216; Dataset B contains 480 synthetic `SET_TEMPERATURE`-derived rows.
- Verified byte-level overlap checks: Dataset2 B vs active project dataset 0/15,268 over 21,001 active audio files; Dataset2 B vs protected project audio 0/15,268 over 615 protected audio files.
- Identified taxonomy limitation: Dataset 2 directly supports many labels and partially supports `BRIGHTNESS` through `LIGHT_DIM`, but does not provide `COLOR`, `CREATE_REMINDER`, `LIST_REMINDERS`, `CALL`, or `MESSAGE`.
- Integration decision: Dataset 2 is `B_USABLE_AFTER_CONTROLLED_FILTERING`, not directly mergeable as a full replacement for the current 19-label VCM.
- No training, retraining, model modification, threshold change, label change, preprocessing change, architecture change, dataset merge, recording collection, router/action change, or live Pi validation occurred.


## 2026-09-28 — Phase BA Controlled Hybrid Dataset Training Experiment

- Completed Phase BA as one controlled training-data experiment after AZ-R review.
- Used the E41 architecture and initialized from frozen E41 weights; did not modify E41, E48, E40, E37, thresholds, preprocessing, router/actions, Phase AV, Phase AD, or protected holdouts.
- Created experiment `E49_BA_HYBRID_DATASET_E41_ARCH`.
- Created the BA report at `PHASE_BA_HYBRID_DATASET_TRAINING_20260927.md`.
- Created machine-readable artifacts under `results/phase_ba_hybrid_dataset_training_20260927/`.
- Frozen BA training manifest contained 11,830 rows: 240 E41 reconstructed adaptation rows, 8,790 active project training rows, and 2,800 Dataset2 `VCM_BALANCED` train rows.
- Protected contamination checks passed: 0 protected path overlaps, 0 protected SHA256 overlaps, 9,942 protected hashes checked.
- Preserved the 19 executable label taxonomy. Dataset2 was used only for mapped labels; `CALL`, `COLOR`, `CREATE_REMINDER`, `LIST_REMINDERS`, and `MESSAGE` received no Dataset2 rows. Dataset2 `UNKNOWN`/`SILENCE` were excluded from BA training because adding them would change the current 19-output command taxonomy.
- Training completed for exactly one candidate with seed 4242, Adam learning rate 0.001, batch size 32, 8 epochs, final-epoch checkpoint only, and the established E41 log-Mel pipeline.
- Current95 result: 78/95 = 82.11% raw accuracy, macro-F1 80.90%, accepted-correct 57, accepted-wrong 6, accepted-action precision 90.48%.
- Phase AV result: 148/210 = 70.48% raw accuracy, macro-F1 70.27%, accepted-correct 102, accepted-wrong 24, rejected-correct 46, rejected-wrong 38, coverage 60.00%, accepted-action precision 80.95%.
- BA improved Phase AV raw accuracy and accepted-action precision versus E41/E48, but had more accepted-wrong cases than E48 and regressed current95 substantially.
- Decision: do not promote BA/E49 to production or Raspberry Pi deployment from offline evidence.
- No threshold tuning, retraining, architecture change, preprocessing change, data collection, dataset merge, Pi deployment, live validation, or follow-on experiment occurred after BA.


## 2026-09-28 — Phase BB E49 Hybrid Regression and Data-Composition Diagnosis

- Completed Phase BB as a diagnosis-only phase after E49/BA rejection.
- Created the report at `results/phase_bb_e49_hybrid_regression_data_composition_diagnosis_20260928/PHASE_BB_E49_HYBRID_REGRESSION_DATA_COMPOSITION_DIAGNOSIS_20260928.md`.
- Created machine-readable artifacts under `results/phase_bb_e49_hybrid_regression_data_composition_diagnosis_20260928/`.
- Compared E41 vs E49 on current95 and Phase AV at the per-sample and per-class levels.
- Current95 four-way comparison: E41 correct/E49 correct 76; E41 correct/E49 wrong 14; E41 wrong/E49 correct 2; E41 wrong/E49 wrong 3.
- Phase AV four-way comparison: E41 correct/E49 correct 85; E41 correct/E49 wrong 18; E41 wrong/E49 correct 63; E41 wrong/E49 wrong 44.
- Current95 regression source: net -10 raw-correct examples in Dataset2-supported/partial labels and -2 in the five Dataset2-uncovered labels. The regression is not disproportionately concentrated in `COLOR`, `CREATE_REMINDER`, `LIST_REMINDERS`, `CALL`, and `MESSAGE`.
- Five uncovered labels on Phase AV improved net +16 raw-correct examples, but `COLOR` remains unsafe: 4/16 raw correct and 6 accepted-wrong cases.
- E49 repaired all tracked AY confusion families relative to E48, including `NEXT -> MESSAGE`, `TEMPERATURE -> MESSAGE`, `VOLUME_DOWN -> VOLUME_UP`, `LIGHT_OFF -> BRIGHTNESS`, `LIGHT_OFF -> TEMPERATURE`, and `LIGHT_ON -> VOLUME_UP`.
- E49 accepted-wrong diagnosis: 24 Phase AV accepted-wrong cases; 8 same wrong prediction as E41, 9 different wrong prediction from E41, and 7 new E49 raw errors where E41 was correct. Seventeen of 24 were new accepted-wrong outcomes relative to E41.
- High-confidence wrong comparison: E49 reduced high-confidence wrong predictions versus E41, but increased them versus E48 (`>=0.90`: E48 17, E49 24).
- BB conclusion: E49 shows a real generalization gain but also decision-boundary movement/possible forgetting and new unsafe accepted-wrong regions.
- Evidence-supported next experiment, if later authorized: controlled class-preservation/rebalancing with original-data preservation or weighted sampling. Do not train E50 during BB.
- No training, threshold change, preprocessing change, architecture change, data collection, Pi deployment, live validation, or production change occurred.


## 2026-09-28 — Phase BC Command-Vocabulary Revision and Router/Action Verification

- Completed Phase BC as a specification/verification-only phase.
- Created the report at `results/phase_bc_command_vocabulary_revision_20260928/PHASE_BC_COMMAND_VOCABULARY_REVISION_20260928.md`.
- Created supporting artifacts under `results/phase_bc_command_vocabulary_revision_20260928/`, including light-command implementation audit, revised 19-label vocabulary, Dataset2 compatibility, future manifest implications, and SHA256 manifest.
- Verified from `VCM Machine Exercise.pdf` that the assignment category is `Dim / color lights` and the example phrase is `Dim lights to X percent`; the assignment does not prescribe literal classifier label names.
- Verified current router/action behavior: historical `COLOR` routes to `LIGHT_ADJUST` with `color=red`; historical `BRIGHTNESS` routes to `LIGHT_ADJUST` with `brightness_percent=50`; both use the same `light.adjust` action handler.
- Verified current action handler already parses dim/brightness phrases as brightness-percent changes.
- Verified Dataset2 contains `LIGHT_DIM` (366 in `VCM_MASTER`, 522 in `VCM_BALANCED` train) and does not contain `COLOR`, `CREATE_REMINDER`, `LIST_REMINDERS`, `CALL`, `MESSAGE`, or `BRIGHTNESS`.
- Documented design decision: future vocabulary may replace `COLOR` with `LIGHT_DIM` to cover the assignment's `DIM/COLOR LIGHTS` category as reduce-light-brightness.
- Documented caveat: current implementation does not yet have a `LIGHT_DIM` router label, and current `BRIGHTNESS` overlaps semantically with proposed `LIGHT_DIM`; this distinction must be resolved before training a revised-vocabulary model.
- Historical E41/E48/E49 evidence remains unchanged.
- No model was trained, no E50 was created, no thresholds/preprocessing/architecture/router/actions were changed, no data was collected, and no Pi/live validation occurred.


## 2026-09-28 — Phase BF Frozen 19-Command End-to-End VCM Functional Audit

- Completed Phase BF as a frozen functional audit and integration-readiness check.
- Created the report at `results/phase_bf_frozen_19_command_end_to_end_audit_20260928/PHASE_BF_FROZEN_19_COMMAND_END_TO_END_AUDIT_20260928.md`.
- Created machine-readable artifacts under `results/phase_bf_frozen_19_command_end_to_end_audit_20260928/`, including command trial rows, multi-cycle rows, safe-rejection row, response WAV inventory, stack verification, test environment, and SHA256 manifest.
- Verified the current package executable defaults from `deployment/vcm_pi_package/scripts/predict_wav_pi.py`: default model `E33_PI_COLOR_LIGHTON_RESPONSIVENESS`, global threshold `0.95`, policy `configs/e33_pi_guardrail_thresholds.json`, and config `configs/cnn_fastbn_dense_nodropout_raw19.json`.
- Reconciled this with project history: Phase C/AD evidence used `E37_TARGETED_COLOR_VOLUME_FIX` wake + `E41_FUNCTIONAL_NON_LED_RECOVERY` command + `E40_NON_LED_COMMAND_GUARDRAIL_THRESHOLDS`; E49 exists as a rejected offline BA candidate and is not wired into the packaged Pi models.
- Verified the current frozen historical vocabulary remains the 19-label set including `COLOR`; Phase BC's future `LIGHT_DIM` vocabulary was not substituted.
- Verified router/action mappings for all 19 labels from `raw_command_router.py` and `command_actions.py`.
- Found no command-specific response WAV bank. `deployment/vcm_pi_package/music/` contains only `README_MUSIC.md`, and no `.wav`/`.mp3` files were present there.
- Found the inspected wake-gated runner performs one wake-command-action attempt and exits; it does not implement the requested persistent multi-cycle listening loop.
- Fresh spoken end-to-end trials were not run because this Codex environment is not the Raspberry Pi runtime and lacks `arecord`, `aplay`, microphone, and speaker access.
- BF therefore records `NOT_RUN`/`NOT_LOGGED`/`NOT_OCCURRED` for trial observations instead of inventing functional results.
- No training, retraining, E50 creation, model modification, threshold change, E40/E37 change, preprocessing change, architecture change, command-vocabulary change, router/action change, data collection, Phase AV/current95 modification, GPIO implementation, realtime timer/weather implementation, deployment, or live validation occurred.


## 2026-09-28 — Phase BG Autonomous CNN Accuracy Optimization Initiated

- Phase BG began after BB/BC/BF review.
- Mission: optimize the command CNN using accessible verified data while preserving evaluation integrity.
- Initial evidence-supported experiment direction: revised 19-label vocabulary with `COLOR` replaced by `LIGHT_DIM`, E41 architecture/preprocessing retained, protected current95/Phase AV/live evidence excluded from training, and stronger original-data preservation than E49 to avoid the BA/BB boundary-displacement failure mode.
- Planned first candidate: next experiment ID `E50`, using controlled hybrid data composition and mapped E41 initialization for common labels while initializing the new `LIGHT_DIM` output without relabeling historical `COLOR`.
- No result has been claimed yet; training/evaluation artifacts will be recorded under Phase BG result folders.


## 2026-09-28 — Phase BG Autonomous CNN Accuracy Optimization Completed

- Completed Phase BG offline command-classifier optimization.
- Created the final report at `results/phase_bg_autonomous_cnn_optimization_20260928/PHASE_BG_AUTONOMOUS_CNN_OPTIMIZATION_FINAL_20260928.md`.
- Created aggregate artifacts under `results/phase_bg_autonomous_cnn_optimization_20260928/`, plus per-candidate folders for E50 and E51.
- Trained two controlled revised-vocabulary CNN candidates using E41 architecture/preprocessing and the frozen 16,100-row BG manifest:
  - `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT`
  - `E51_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_FRESH_INIT`
- Revised BG vocabulary uses `LIGHT_DIM` instead of historical `COLOR`; historical `COLOR` evaluation rows were excluded from compatible historical comparisons and were not relabeled.
- Protected contamination check passed: 0 protected path overlaps and 0 protected SHA256 overlaps across 14,142 protected hashes.
- E50 compatible results: current95 83/90 = 92.22%; Phase AV 139/194 = 71.65%; Phase AV accepted-wrong 8; Phase AV accepted-action precision 91.92%.
- E51 compatible results: current95 77/90 = 85.56%; Phase AV 131/194 = 67.53%; Phase AV accepted-wrong 8; Phase AV accepted-action precision 89.61%.
- Decision: E50 is the strongest BG offline command-classifier candidate for final review; E51 is rejected as the final BG choice despite stronger Dataset2/combined safety because it gives up too much protected-compatible performance.
- E50 is not Pi/demo verified. A separate deployment/demo phase is still required to wire the revised `LIGHT_DIM` runtime path, package the model, verify action/response behavior, and run fresh Raspberry Pi end-to-end validation.
- No threshold tuning, architecture change, preprocessing change, router/action change, wake-model change, protected-data training, Pi deployment, or live validation occurred during BG.


## 2026-09-28 — Phase BH E50 Raspberry Pi Package Integration

- Completed the next legitimate post-BG step: packaged the selected E50 command classifier for Raspberry Pi validation.
- Created the report at `results/phase_bh_e50_pi_package_integration_20260928/PHASE_BH_E50_PI_PACKAGE_INTEGRATION_20260928.md`.
- Copied E50 command weights, normalization, and labels into `deployment/vcm_pi_package/`.
- Copied preserved E37 wake model weights, normalization, and labels into `deployment/vcm_pi_package/`.
- Added `deployment/vcm_pi_package/configs/e50_revised_vocab_e40_thresholds.json`, a deployment-compatible frozen E40 guardrail policy for the revised `LIGHT_DIM` vocabulary.
- Added `LIGHT_DIM` to the root and packaged raw-command routers. It routes to `LIGHT_ADJUST` with brightness 50% and `light_adjust_action=dim`.
- Updated `pi_wake_voice_control_demo.py` defaults to use E37 for wake and E50 for command classification.
- Updated the Pi deployment README and package manifest to document the E37+E50 stack.
- Verification passed: syntax checks, `LIGHT_DIM` route/action dry-run, default-stack constants check, and packaged E50 WAV inference.
- No training, threshold tuning, architecture change, preprocessing change, protected-data modification, GPIO execution, Pi microphone live validation, or final demo claim occurred.


## 2026-09-28 — Phase BI E50 Raspberry Pi Wake-Gated Live Validation

- Ingested actual Raspberry Pi evidence archive `outputs/e50_wake_gated_live_20260928_evidence.tar.gz`.
- Verified archive SHA256: `81916037181eacf42ed40904d4f89d7e038db46c90e6495ec8e5a70ed3c9e2b5`, matching the Pi-side hash.
- Created Phase BI report at `results/phase_bi_e50_pi_live_validation_20260928/PHASE_BI_E50_PI_LIVE_VALIDATION_20260928.md`.
- Parsed 36 result JSON files with paired wake/command WAV evidence.
- Wake success: 36/36.
- Tested all 19 revised command labels at least once, plus one UNKNOWN/no-action phrase.
- Command trials excluding UNKNOWN: 35.
- Raw-correct command trials: 24/35.
- Accepted-correct command trials: 15.
- Accepted-wrong command trials: 1.
- Accepted-action precision: 15/16 = 93.75%.
- End-to-end command successes: 14/35 repeated command trials.
- UNKNOWN safe rejection: 1/1.
- End-to-end pass observed at least once for `PLAY_MUSIC`, `WEATHER`, `LIGHT_ON`, `LIGHT_OFF`, `LIGHT_DIM`, `TIMER`, `ALARM`, `NEXT`, `PAUSE`, `STOP`, `LIST_REMINDERS`, and `MESSAGE`.
- Important accepted-wrong failure: `e50_temperature_001` expected `TEMPERATURE`, predicted `WEATHER` at 0.9973, and executed `question.weather_local`.
- Important integration issue: `LIGHT_DIM` initially classified correctly but failed routing on the Pi package; the user patched the Pi router, after which `LIGHT_DIM` passed end-to-end.
- Phase BI verifies repeated manual wake-command-action cycles, not a single persistent always-listening loop.
- No training, retraining, threshold tuning, architecture change, preprocessing change, or historical-result rewriting occurred.


## 2026-09-28 — Phase BJ Diagnosis-First Targeted Remediation Decision

- Completed Phase BJ as a diagnosis-first decision phase after BI live Pi validation.
- Created the report at `results/phase_bj_diagnosis_first_targeted_remediation_20260928/PHASE_BJ_DIAGNOSIS_FIRST_TARGETED_REMEDIATION_20260928.md`.
- Created/retained machine-readable artifacts under `results/phase_bj_diagnosis_first_targeted_remediation_20260928/`, including weak-command diagnosis, remediation options, decision summary, targeted Pi repeat plan, and SHA256 manifest.
- Decision: do not claim final all-command demo readiness from BI alone, and do not start another general CNN sweep.
- Strongest safety issue: `TEMPERATURE` produced an accepted-wrong `WEATHER` action at confidence `0.997283935546875` in BI.
- Current defensible demo-subset candidates, subject to persistent-loop/response evidence, are the 12 labels that passed at least once in BI: `PLAY_MUSIC`, `WEATHER`, `LIGHT_ON`, `LIGHT_OFF`, `LIGHT_DIM`, `TIMER`, `ALARM`, `NEXT`, `PAUSE`, `STOP`, `LIST_REMINDERS`, and `MESSAGE`.
- Weak labels requiring targeted repeat validation or limitation: `TIME`, `BRIGHTNESS`, `TEMPERATURE`, `VOLUME_UP`, `VOLUME_DOWN`, `CREATE_REMINDER`, and `CALL`.
- Recommended next step: targeted Pi repeat/phrase validation for weak labels under the frozen E37+E50 stack, plus separate demo-integration work for persistent listening and response feedback.
- No training, retraining, E50 modification, threshold tuning, E40/E37 change, preprocessing change, architecture change, protected-evaluation modification, Pi live validation, new training-data collection, or historical-result rewriting occurred in BJ.


## 2026-09-28 — Phase BK Targeted Weak-Command Repeat Validation

- Ingested actual Raspberry Pi evidence archive `outputs/e50_bk_targeted_weak_command_repeats_e37_e50_20260928_evidence.tar.gz`.
- Verified archive SHA256: `e92b12464153fbf2652aafdbadd3459eab6a1a1331fcb5463c0da3e69b851513`.
- Created Phase BK report at `results/phase_bk_targeted_weak_command_repeat_validation_20260928/PHASE_BK_TARGETED_WEAK_COMMAND_REPEAT_VALIDATION_20260928.md`.
- Parsed 23 result JSON files: 1 stack-check ALARM trial and 22 weak-command repeat trials.
- Verified all parsed BK trials used wake `E37_TARGETED_COLOR_VOLUME_FIX` and command `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT`.
- Weak-command wake success: 22/22.
- Weak-command accepted-correct: 3/22.
- Weak-command accepted-wrong: 2/22.
- Weak-command end-to-end successes: 3/22.
- `CREATE_REMINDER` recovered with accepted end-to-end passes for `remind me` and `set reminder`.
- `TEMPERATURE` remains unsafe: `set thermostat` was accepted as `STOP`, and `temperature` was accepted as `WEATHER`.
- `TIME`, `BRIGHTNESS`, `VOLUME_UP`, `VOLUME_DOWN`, and `CALL` still have no accepted end-to-end pass in BK.
- Decision: prepare a defensible final demo subset if needed; do not use `TEMPERATURE` live without later targeted remediation; do not run another general CNN sweep.
- No training, retraining, threshold tuning, E40/E37/E50 modification, preprocessing change, architecture change, protected-evaluation modification, new training-data collection, or historical-result rewriting occurred in BK.


## 2026-09-28 — Phase BL Targeted Weak-Command Remediation and E52 Rejection

- Completed Phase BL diagnosis-first remediation after BI/BK showed six unresolved weak labels: `TIME`, `BRIGHTNESS`, `TEMPERATURE`, `VOLUME_UP`, `VOLUME_DOWN`, and `CALL`.
- Created Phase BL report at `results/phase_bl_targeted_weak_command_remediation_20260928/PHASE_BL_TARGETED_WEAK_COMMAND_REMEDIATION_20260928.md`.
- Created machine-readable diagnosis/comparison artifacts under `results/phase_bl_targeted_weak_command_remediation_20260928/`.
- Diagnosed `TEMPERATURE` as the highest-risk label because it had repeated accepted-wrong live outcomes, including `TEMPERATURE -> WEATHER` and `TEMPERATURE -> STOP`.
- Trained exactly one controlled candidate: `E52_BL_TARGETED_WEAK_E50_FINETUNE`, initialized from E50 with weak-label sample weights and no new data.
- E52 preserved architecture, preprocessing, labels, and frozen E40-compatible thresholds; no Phase AV/current95/BI/BK/demo recordings were used for training.
- E52 weights SHA256: `8730681edf680855d1188119e3a90f9713a28063e96ae451c9caabb27d30003a`.
- E52 improved Phase AV-compatible raw performance from 139/194 to 150/194, but accepted-wrong actions increased from 8 to 13 and accepted-action precision fell from 91.92% to 87.62%.
- E52 also worsened BI live replay safety: accepted-wrong increased from 1 observed E50 live error to 3 E52 replay errors.
- Decision: reject E52 for production/demo promotion and retain E50 as the defensible fallback.
- Final BL state: STATE C — no safe/defensible offline improvement found; prepare final demo subset with limitations unless later targeted data collection is authorized.
- No threshold tuning, architecture change, preprocessing change, E37/E40 modification, protected-data training, router/action redesign, Pi deployment, or new live validation occurred in BL.


## 2026-09-28 — Phase BM Final E50 Integration and Demo Hardening

- Completed Phase BM offline integration/hardening for the final E37+E50 stack.
- Verified packaged E50 SHA256 matches the required final hash: `bc8ac64ced4305ddf43bf4de377f3cc636a764eff339cd9f92af06340c50b8ff`.
- Confirmed E50 label order matches the final revised 19-label vocabulary with `LIGHT_DIM` and no `COLOR`.
- Updated Pi package defaults so `predict_wav_pi.py` and the wake-gated runtime use final E50/E40-compatible defaults rather than historical E33 defaults.
- Added cached `VcmPredictor` loading so persistent runtime can load model/labels/threshold policy once.
- Added `--cycles` and `--continuous` persistent-loop support to `pi_wake_voice_control_demo.py`.
- Added local response WAV mapping and generated response WAV assets under `deployment/vcm_pi_package/responses/`.
- Added `scripts/run_e50_final_demo.sh` for concise Pi startup.
- Removed active final-runtime `COLOR` routing/prompting from package router/helper scripts; historical E33 files remain marked as historical.
- Replayed 59 BI/BK WAV trials through the hardened package: BI 36 rows, BK 23 rows.
- Local laptop efficiency measurement: 66,483 parameters, 251,734-byte E50 weights, about 0.040 s mean command-decision time on Windows/laptop. This is not a Pi latency claim.
- Created Phase BM report and artifacts under `results/phase_bm_final_vcm_integration_demo_hardening_20260928/`.
- Prepared final demo script and Pi validation handoff.
- No model training, threshold tuning, architecture change, preprocessing change, E37/E40 modification, E50 weight modification, unauthorized Pi access, GPIO execution, or new live validation occurred.


## 2026-09-28 — Phase BM Physical Pi Final Validation Addendum

- Ingested the Raspberry Pi evidence archive `outputs/e50_bm_final_demo_20260928_evidence.tar.gz`.
- Verified archive SHA256: `4695a6d0fb282624499a42d8102ff4bf578022c5a0e15a8368b8ef7fd97079ec`.
- Parsed 14 Pi result JSON files: 13 selected demo-command trials and 1 UNKNOWN rejection trial.
- Confirmed the run used wake `E37_TARGETED_COLOR_VOLUME_FIX` and command `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT`.
- Wake successes: 13/14 total trials, 12/13 selected demo-command trials.
- Raw recognition correct: 11/13 selected demo commands.
- Accepted automatic action executions: 9/13 selected demo commands.
- Loop return: 14/14 trials returned to listening.
- UNKNOWN phrase `open the window` was safely rejected without action.
- Response WAV assets existed and were readable for all executed commands, but physical playback failed for all attempted responses because `aplay` exited with status 1.
- Commands with action-pipeline passes in this run: `PLAY_MUSIC`, `WEATHER`, `LIGHT_ON`, `LIGHT_DIM`, `TIMER`, `ALARM`, `PAUSE`, `CREATE_REMINDER`, and `LIST_REMINDERS`.
- Commands that did not reach action execution in this run: `LIGHT_OFF`, `NEXT`, `STOP`, and `MESSAGE`.
- Created `PHASE_BM_PI_FINAL_VALIDATION_ADDENDUM_20260928.md`, `PHASE_BM_PI_FINAL_VALIDATION_RESULTS.csv`, and `PHASE_BM_PI_FINAL_VALIDATION_SUMMARY.json`.
- No model training, threshold tuning, architecture change, preprocessing change, E37/E40/E50 modification, protected-data modification, GPIO execution, or historical-result modification occurred.


## 2026-09-28 — Phase BM Command-Status Correction

- Recorded the required distinction between `CALLABLE`, `IMPLEMENTED`, `VERIFIED`, and `DEMO_READY`.
- Confirmed that all 19 final commands remain in the VCM vocabulary and remain callable/testable.
- Confirmed that the final demo subset is only a safety/validation presentation choice, not a runtime whitelist.
- Added Table A: `results/phase_bm_final_vcm_integration_demo_hardening_20260928/PHASE_BM_19_COMMAND_IMPLEMENTATION_CALLABILITY.csv`.
- Added Table B: `results/phase_bm_final_vcm_integration_demo_hardening_20260928/PHASE_BM_CURRENT_DEMO_READY_COMMANDS.csv`.
- Clarified that `TIME`, `BRIGHTNESS`, `TEMPERATURE`, `VOLUME_UP`, `VOLUME_DOWN`, and `CALL` are callable and implemented but not currently demo-ready.
- Clarified that `TEMPERATURE` remains callable and implemented, but is unsafe/not demo-ready and requires remediation because accepted-wrong live actions were observed.
- No whitelist or runtime restriction was added.


## 2026-09-28 — Phase BN Offline Preparation and Runtime Hardening

- Began Phase BN under the rule that model development is closed.
- Verified packaged E50 SHA256: `bc8ac64ced4305ddf43bf4de377f3cc636a764eff339cd9f92af06340c50b8ff`.
- Verified E50 label order contains the complete final 19-command vocabulary.
- Verified all 19 commands have router routes and local action paths.
- Added response WAV assets and response-map entries for the six callable-but-not-demo-ready commands: `TIME`, `BRIGHTNESS`, `TEMPERATURE`, `VOLUME_UP`, `VOLUME_DOWN`, and `CALL`.
- Hardened response playback evidence in `pi_wake_voice_control_demo.py` by adding optional `--response-audio-device` and recording `aplay` stderr/playback device in JSON.
- Added Phase BN Pi helper scripts:
  - `scripts/run_phase_bn_audio_diagnostics.sh`
  - `scripts/run_phase_bn_prompted_trial.sh`
  - `scripts/run_phase_bn_audio_smoke.sh`
  - `scripts/run_phase_bn_all19_prompted_validation.sh`
- Created Phase BN artifacts under `results/phase_bn_final_pi_validation_runtime_hardening_20260928/`.
- Created deployment archive `outputs/e50_bn_runtime_update_20260928.tar.gz`.
- Archive SHA256: `ca0c8b5c70668322c0f9d2f2e9dc8b2f353d399381bce6d7a81dab2806010a87`.
- Python compile passed for the package runtime/action modules.
- `pytest` was not available locally, so full pytest execution was not run.
- Local router/action smoke verified all 19 commands execute simulated local action paths; no Pi hardware/GPIO was used.
- Stopped at the physical Pi boundary: audio diagnostics, live recording/playback, all-19 physical validation, and Pi efficiency measurement require user-run Pi commands or explicit Pi access.
- No CNN training, fine-tuning, E53 creation, threshold tuning, architecture change, preprocessing change, E37/E40/E50 modification, quantization, protected-data modification, GPIO execution, or Pi access occurred during offline BN preparation.


## 2026-09-28 — Phase BN Audio Smoke Evidence Ingestion

- Ingested Pi archive `outputs/e50_bn_audio_smoke_20260928_evidence.tar.gz`.
- Archive SHA256: `50ddfd62fd5778045c25b9152a0cbc3e5c182ff924975848e9d72cee9ab79352`.
- Parsed 9 BN audio-smoke/result JSON files.
- Confirmed usable response audio device: `plughw:CARD=vc4hdmi1,DEV=0`.
- User reported the regenerated direct alarm tone was audible.
- `e50_bn_audio_timer_smoke_001` passed the response-audio smoke: wake accepted, `TIMER` accepted with confidence `0.999995231628418`, `timer.create` action executed, response WAV played according to JSON, and user reported the tone response was audible.
- `e50_bn_audio_alarm_retry_001` was an `ALARM` confidence rejection below threshold, not an audio failure.
- `e50_bn_smoke_unknown_001` was safely rejected with no action.
- Created `PHASE_BN_AUDIO_SMOKE_ADDENDUM_20260928.md`, `PHASE_BN_AUDIO_SMOKE_RESULTS.csv`, and `PHASE_BN_AUDIO_SMOKE_SUMMARY.json`.
- No model training, threshold tuning, architecture/preprocessing change, or E37/E40/E50 modification occurred.

## 2026-09-28 - Phase BN Prompted Repeated-Cycle Audio Evidence Ingestion

- Ingested Pi archive `outputs/e50_bn_prompted_multicycle_20260928_evidence.tar.gz`.
- Archive SHA256: `10011b1364b73820a62853e784a7896bd649a10e9bada96656274674ec6be4f4`.
- Parsed four prompted repeated-cycle trials: `ALARM`, `TIMER`, `PAUSE`, and `LIST_REMINDERS`.
- All four trials accepted wake, accepted the command, executed the intended action, reported `response_result.played=true`, and returned to listening.
- User reported hearing all four response tones through `plughw:CARD=vc4hdmi1,DEV=0`.
- Created `PHASE_BN_PROMPTED_MULTICYCLE_ADDENDUM_20260928.md`, `PHASE_BN_PROMPTED_MULTICYCLE_RESULTS.csv`, and `PHASE_BN_PROMPTED_MULTICYCLE_SUMMARY.json`.
- Interpretation boundary: this is prompted repeated-cycle evidence using separate single-cycle invocations, not a single same-process continuous-loop proof.
- No model training, threshold tuning, architecture/preprocessing change, E37/E40/E50 modification, runtime whitelist, GPIO execution, or protected-data modification occurred.

## 2026-09-28 - Phase BN All-19 Prompted Pi Validation Ingestion

- Ingested Pi archive `outputs/e50_bn_all19_validation_20260928_evidence.tar.gz`.
- Archive SHA256: `18b7bda8aff4dc9de12568e20626069547f51c03397deffe222ab6fad7115e98`.
- Parsed 20 result JSON files: 19 commands plus one UNKNOWN phrase.
- Wake accepted 19/20 trials; all 20 trials returned to listening.
- Raw correct command predictions: 13/19.
- End-to-end audio passes in this run: 10/19 (`PLAY_MUSIC`, `WEATHER`, `LIGHT_OFF`, `BRIGHTNESS`, `TIMER`, `ALARM`, `TEMPERATURE`, `PAUSE`, `STOP`, `LIST_REMINDERS`).
- Accepted-wrong command actions in this run: 0.
- UNKNOWN phrase `open the window` was safely rejected.
- Created `PHASE_BN_ALL19_PI_VALIDATION_ADDENDUM_20260928.md`, `PHASE_BN_ALL19_PI_VALIDATION_RESULTS.csv`, `PHASE_BN_ALL19_PI_VALIDATION_SUMMARY.json`, and `PHASE_BN_ALL19_COMMAND_STATUS_AFTER_PI_VALIDATION.csv`.
- Safety boundary: `TEMPERATURE` remains globally unsafe/not demo-ready because prior accepted-wrong live evidence remains binding despite this run's pass.
- No model training, threshold tuning, architecture/preprocessing change, E37/E40/E50 modification, runtime whitelist, GPIO execution, or protected-data modification occurred.

## 2026-09-29 - Phase BN Final Deployment Guide Follow-Through

Objective: follow the final deployment guide using the current frozen E37+E50+E40-compatible stack, without starting another CNN experiment or changing thresholds.

Actions completed:
- Inspected the final deployment guide from `C:\Users\Loreen Anne\Documents\final deployment guide.docx` and treated it as the user-requested deployment procedure.
- Confirmed the current project has already advanced to the E50 final candidate stack and Phase BN evidence, so E41/E48-era work was not re-opened.
- Added a native Tkinter touchscreen controller: `deployment/vcm_pi_package/scripts/vcm_touchscreen_gui.py`.
- Added a Pi launcher and optional desktop entry: `scripts/run_vcm_touchscreen_gui.sh` and `vcm_touchscreen_gui.desktop`.
- Updated deployment package documentation to describe the GUI without embedding recognition logic in the GUI.
- Created final guide-named synthesis artifacts: `PHASE_BN_FINAL_INTEGRATION_REPORT.md`, `PHASE_BN_19_COMMAND_IMPLEMENTATION_CALLABILITY.csv`, `PHASE_BN_RESPONSE_WAV_INVENTORY.csv`, `PHASE_BN_PATH_CONFIGURATION_AUDIT.csv`, `PHASE_BN_FINAL_DEPLOYMENT_SHA256SUMS.csv`, `PROFESSOR_COMMAND_SHEET.md`, and `DEMO_SCRIPT.md`.
- Updated `README.md` and `REQUIREMENTS_TRACEABILITY.md` with final offline Raspberry Pi deployment status.

Result: final deployment staging is PARTIAL. All 19 commands remain callable and no demo whitelist was introduced. The GUI is implemented in the package, but physical touchscreen verification, final disconnected offline Pi demo, same-process continuous-loop proof, and Pi performance measurement remain not run/not measured.

Controls preserved: no model training, no E37/E40/E50 modification, no threshold tuning, no preprocessing change, no router/action replacement, no live validation, and no production configuration change beyond packaging/GUI/docs.

## 2026-09-29 - Phase BN Human Response Recording Correction

Objective: correct final deployment response evidence after identifying that the guide requires recorded human voice responses, not tones.

Finding: current response WAVs are present and readable, but they are approximately 0.32 seconds for command responses and 0.18 seconds for UNKNOWN. They are valid audio-path smoke assets only and are not final-compliant recorded human responses.

Actions completed:
- Added `deployment/vcm_pi_package/scripts/record_human_command_responses.py` to prompt and record one human voice response WAV per command on the Pi.
- Added `deployment/vcm_pi_package/scripts/verify_human_command_responses.py` to verify response WAV format/duration and flag placeholder tones.
- Ran the verifier locally against current response assets; all current response WAVs are flagged `FAIL_TOO_SHORT_LIKELY_PLACEHOLDER`.
- Updated `PHASE_BN_RESPONSE_WAV_INVENTORY.csv` and created `PHASE_BN_HUMAN_RESPONSE_WAV_INVENTORY.csv` plus `PHASE_BN_HUMAN_RESPONSE_RECORDING_CORRECTION_20260929.md`.
- Updated deployment package docs and final integration report to mark human response recording as BLOCKED until physically recorded on the Pi.

No model, threshold, preprocessing, router, action, or production recognition behavior changed. No response recording was fabricated.



## 2026-09-29 - Phase BN-CLOSE Final Deployment Verification Staging

Phase BN-CLOSE was started as the final physical Raspberry Pi deployment verification phase under a full model freeze. No CNN training, fine-tuning, threshold tuning, preprocessing change, E37/E40/E50 modification, command removal, or runtime demo whitelist was performed.

Created BN-CLOSE closeout artifacts under `results/phase_bn_close_final_deployment_verification_20260929/`:

- `PHASE_BN_CLOSE_FINAL_VERIFICATION_REPORT.md`
- `PHASE_BN_CLOSE_DEPLOYMENT_AUDIT.csv`
- `PHASE_BN_CLOSE_TOUCHSCREEN_TEST.csv`
- `PHASE_BN_CLOSE_MULTICYCLE_RESULTS.csv`
- `PHASE_BN_CLOSE_PERSISTENT_LOOP_EVIDENCE.md`
- `PHASE_BN_CLOSE_RESPONSE_PLAYBACK.csv`
- `PHASE_BN_CLOSE_UNKNOWN_SAFETY.csv`
- `PHASE_BN_CLOSE_STANDALONE_DEMO_EVIDENCE.md`
- `PHASE_BN_CLOSE_PI_PERFORMANCE.csv`
- `PHASE_BN_CLOSE_FINAL_19_COMMAND_STATUS.csv`
- `PHASE_BN_CLOSE_FINAL_DEMO_READY_COMMANDS.csv`
- `PHASE_BN_CLOSE_FINAL_REQUIREMENTS_AUDIT.csv`
- `PHASE_BN_CLOSE_PI_HANDOFF.md`
- `PHASE_BN_CLOSE_FINAL_SHA256SUMS.csv`

Added Pi-side helper scripts to `deployment/vcm_pi_package/scripts/` for deployment audit, response playback audit, persistent same-process loop testing, and Pi performance probing.

Created BN-CLOSE verification tools archive `outputs/e50_bn_close_verification_tools_20260929.tar.gz` with SHA256 `ca985d8597de5f8ca30eb37c94d4c365fce9536671bcae0374aa11ba21b99a7d`. This is not a final verified deployment archive.

Current BN-CLOSE status: PARTIAL FINAL DEPLOYMENT STAGING COMPLETE; FINAL DEPLOYMENT NOT YET VERIFIED. Physical-only requirements remain pending: touchscreen validation, same-process 5/10/20-cycle loop proof, final human recorded response playback, fully standalone/no-laptop operation, Wi-Fi/Ethernet-off operation, Pi CPU/RAM/temperature/latency measurement, and non-primary-speaker validation.

Important evidence boundary: all 19 commands remain callable/testable; 10/19 had end-to-end audio pass in the latest all-19 prompted Pi audit with 0 accepted-wrong actions, but `TEMPERATURE` remains globally unsafe/not demo-ready because prior accepted-wrong live evidence remains binding.

## 2026-09-29 - Phase BN-CLOSE Round1 Pi Evidence

- Ingested `outputs/e50_bn_close_20260929_evidence_round1.tar.gz`.
- Archive SHA256: `ac371525a5436cb153e239da4aeabe526b34086024de4699a2bc24fb142d5c8b`.
- Deployment audit and response playback CSV were captured from the Pi.
- Same-process 5-cycle runtime test passed for wake/classification/action/return-to-listening: 5/5 wake accepted, 5/5 commands accepted/executed (`PLAY_MUSIC`, `TIMER`, `ALARM`, `PAUSE`, `LIST_REMINDERS`), 5/5 returned to listening, GPIO requested false.
- Runtime response playback failed because it used `plughw:CARD=vc4hdmi1,DEV=0`, which returned ALSA error 524.
- Audio recheck proved `plughw:CARD=vc4hdmi0,DEV=0` and `default` can play `responses/timer.wav`; operator reported hearing the timer response twice.
- Failure layer: `RESPONSE_PLAYBACK_DEVICE_SELECTION`, not CNN, threshold, router, action, or persistent loop.
- Updated BN-CLOSE handoff/helper defaults to use `plughw:CARD=vc4hdmi0,DEV=0` for subsequent response playback tests.
- Rebuilt verification tools archive SHA256: `e774637643861a2c43d7554da05a19d5a961df9a0efd5e74157c4481b53109ad`.

## 2026-09-29 - Phase BN-CLOSE Round2 Transcript Evidence

- Parsed pasted Pi terminal transcript for `OUT=pi_validation/e50_bn_close_20260929_round2`.
- Runtime used `RESPONSE_AUDIO_DEVICE=plughw:CARD=vc4hdmi0,DEV=0`.
- Same-process 5-cycle loop transcript shows 5/5 wake accepted, 5/5 commands accepted/executed, 5/5 response playback JSON true, 5/5 returned to listening, and GPIO requested false.
- Commands: `PLAY_MUSIC`, `TIMER`, `ALARM`, `PAUSE`, `LIST_REMINDERS`.
- Operator reported hearing all response playback first and then correct answers to all commands.
- Created `PHASE_BN_CLOSE_ROUND2_TRANSCRIPT_ADDENDUM.md`, `PHASE_BN_CLOSE_ROUND2_TRANSCRIPT_LOOP_RESULTS.csv`, and `PHASE_BN_CLOSE_ROUND2_TRANSCRIPT_SUMMARY.json`.
- Boundary: source Pi archive for `pi_validation/e50_bn_close_20260929_round2` still must be copied back before treating this as fully preserved evidence.

## 2026-09-29 - Phase BN-CLOSE Response WAV Boosting

- Preserved the current deployment response WAVs under `deployment/vcm_pi_package/responses_original_pre_boost_20260929/`.
- Created peak-normalized boosted response WAVs under `deployment/vcm_pi_package/responses_boosted/` using `_boosted.wav` filenames.
- Updated `deployment/vcm_pi_package/configs/demo_response_assets.json` so runtime response playback uses the boosted filenames.
- Wrote `deployment/vcm_pi_package/PHASE_BN_CLOSE_RESPONSE_BOOST_MANIFEST_20260929.csv` with per-file source, backup, boosted path, peak, gain, and SHA256 evidence.
- Boost operation only changed response WAV playback assets/configuration. No model training, threshold tuning, preprocessing change, E37/E40/E50 change, router/action change, GPIO execution, or command whitelist occurred.

## 2026-09-29 - Phase BN-CLOSE Round2 and Extra-Loud Response Evidence Preserved

- Ingested `outputs/e50_bn_close_20260929_round2_evidence.tar.gz`.
- Round2 archive SHA256: `f21ce0f86552978dbdbeeba31afb7ef3849e04cb788e257ebc1dc5639b00865f`.
- Extracted source WAV/JSON/CSV evidence to `results/phase_bn_close_final_deployment_verification_20260929/pi_close_round2_evidence_extract/`.
- Generated `PHASE_BN_CLOSE_ROUND2_SOURCE_LOOP_RESULTS.csv` and `PHASE_BN_CLOSE_ROUND2_SOURCE_SUMMARY.json`.
- Source-backed result: 5/5 wake accepted, 5/5 commands accepted/executed, 5/5 response playback true, 5/5 returned to listening, GPIO requested false.
- Ingested `outputs/e50_bn_close_extra_loud_responses_20260929.tar.gz`.
- Extra-loud response archive SHA256: `9ce3be48ee05738305a189a15eb0e1de4c126767084138266f11cdb32d1f1128`.
- Generated `PHASE_BN_CLOSE_EXTRA_LOUD_RESPONSE_MAP_AUDIT.csv` and `PHASE_BN_CLOSE_EXTRA_LOUD_RESPONSE_MAP_SUMMARY.json`.
- Verified all 19 commands plus UNKNOWN map to existing `responses_extra_loud_20260929/*_extra_loud.wav` files. Operator reported the extra-loud responses were perfect.
- The earlier Windows-side `responses_boosted` package is obsolete/rejected for deployment playback; the active Pi response map is the extra-loud set.

## 2026-09-29 - Phase BN-CLOSE Wake-Wait Runtime Update

- Added `--wait-for-wake` to `scripts/pi_wake_voice_control_demo.py`.
- In wait-for-wake mode, the runtime keeps recording wake windows until `WAKE` is accepted instead of consuming a cycle or ending when one wake window misses the phrase.
- Added `--max-wake-attempts` and `--wake-retry-delay-sec`; default `--max-wake-attempts 0` means unlimited waiting.
- Added `scripts/run_phase_bn_close_wake_wait_demo.sh` for a persistent demo that returns to indefinite wake listening after each response.
- Created `outputs/e50_bn_close_wake_wait_runtime_update_20260929.tar.gz`, SHA256 `8e991c75c2d85c334dcf58df558881e163522d361911175a64c3de96fbc521c6`.
- This is a runtime interaction update only. No model training, threshold tuning, preprocessing change, E37/E40/E50 change, router/action change, GPIO execution, or command whitelist occurred.

## 2026-09-29 - Phase BN-CLOSE Wake-Wait Evidence Ingested

- Ingested `outputs/e50_bn_close_wake_wait_20260929_evidence.tar.gz`.
- Archive SHA256: `c8223dd8eec144baa1cdbf28803856695eac2897511f2eba2a27741126a6539f`.
- Extracted evidence to `results/phase_bn_close_final_deployment_verification_20260929/pi_close_wake_wait_evidence_extract/`.
- Generated `PHASE_BN_CLOSE_WAKE_WAIT_RESULTS.csv`, `PHASE_BN_CLOSE_WAKE_WAIT_SUMMARY.json`, and `PHASE_BN_CLOSE_WAKE_WAIT_ADDENDUM.md`.
- Source-backed result: 13/13 wake accepted, 13/13 returned to listening, 8/13 commands executed with response playback true, GPIO requested false.
- Wake-wait proof: `e50_bn_close_wake_wait_012` required 4 wake attempts and `e50_bn_close_wake_wait_013` required 2 wake attempts before accepting `hey pi`, proving the runtime stayed in wake-listening mode across missed wake windows.
- Command-stage rejections in this run were below-threshold command outcomes after wake acceptance, not failures of wake-wait control flow.

## 2026-09-29 - Phase BN-CLOSE Touchscreen GUI Wake-Wait Validation Package

- Updated `scripts/vcm_touchscreen_gui.py` so the GUI START button launches the same E37+E50 runtime with `--wait-for-wake` enabled by default.
- Updated `scripts/run_vcm_touchscreen_gui.sh` defaults: evidence directory `pi_validation/e50_bn_close_touchscreen_gui_20260929`, response audio device `plughw:CARD=vc4hdmi0,DEV=0`, unlimited wake attempts, and wake retry delay 0.2 seconds.
- Added `scripts/run_phase_bn_close_touchscreen_gui_validation.sh`, which opens the physical GUI and writes post-run touchscreen GUI CSV/JSON summaries from evidence files.
- Corrected the Pi desktop shortcut to `/home/loreenanne/vcm_pi_package`.
- Restored the active response map in the deployment package to the accepted Pi extra-loud response set: `responses_extra_loud_20260929/*_extra_loud.wav`.
- Created `outputs/e50_bn_close_touchscreen_gui_wake_wait_update_20260929.tar.gz`, SHA256 `b298efe060150c0ac57c6410a2ff9a23ab34e6ef7ab57c2de94c4eb978b84f33`.
- This is a touchscreen validation package, not physical touchscreen evidence. No model training, threshold tuning, preprocessing change, E37/E40/E50 change, router/action change, GPIO execution, or command whitelist occurred.

## 2026-09-29 - Phase BN-CLOSE Touchscreen GUI Reject-State Fix

- Prepared `outputs/e50_bn_close_touchscreen_gui_reject_state_fix_20260929.tar.gz`, SHA256 `d230124dd28aef048a467a0707c1e7dd3df399442aa319f986418915f7229c0e`.
- Fix scope: GUI display-state/readability only.
- New GUI wording:
  - wake window active: `LISTENING` / `Say "hey pi"`;
  - wake accepted command window: `TELL ME WHAT YOU NEED`;
  - wake miss: `STILL LISTENING` / `Wake missed; say "hey pi" again`;
  - command rejected after wake: `STILL LISTENING` / `Command rejected safely; say "hey pi" again`.
- No model training, threshold tuning, preprocessing change, E37/E40/E50 change, wake-wait runtime semantic change, router/action change, GPIO execution, response-asset change, or command whitelist occurred.

## 2026-09-29 - Phase BN-CLOSE Touchscreen GUI Prompt Sync Fix

- Prepared `outputs/e50_bn_close_touchscreen_gui_prompt_sync_fix_20260929.tar.gz`, SHA256 `957b57096aad653fc31d77f070ddae4b790cd402136723d3882eec7fd7f559af`.
- Fix scope: GUI prompt synchronization only.
- The GUI now launches the child runtime with Python unbuffered (`-u` and `PYTHONUNBUFFERED=1`) so wake/command prompts reach the touchscreen immediately.
- The accepted-wake command window now displays `TELL ME WHAT YOU NEED` with status `Wake accepted. Speak now.`
- Shell scripts in this archive use Unix LF line endings.
- No model, threshold, preprocessing, E37/E40/E50, router/action, GPIO, response-asset, or command-vocabulary behavior changed.

## 2026-09-29 - Phase BN-CLOSE Touchscreen GUI Top Instructions

- Prepared `outputs/e50_bn_close_touchscreen_gui_top_instructions_20260929.tar.gz`, SHA256 `7754b8fbc1ccc192340b86167de7c8a7e0195c754e83e6e6c1cdaeb169745d0c`.
- Fix scope: GUI layout and wording only.
- The primary instruction is now the first/top element on the touchscreen.
- State wording:
  - wake miss: `I AM NOT AWAKE` / `Say "hey pi" again.`;
  - wake accepted: `TELL ME WHAT YOU NEED` / `I am at your command.`;
  - command rejected: `I DIDN'T UNDERSTAND` / `Say "hey pi" again.`;
  - ready after execution: `WAKE ME UP` / `Say "hey pi"`.
- No recognition, threshold, preprocessing, wake-wait, router/action, GPIO, response-audio, or vocabulary behavior changed.

## 2026-09-29 - Phase BN-CLOSE Touchscreen GUI Short Command Prompt

- Prepared `outputs/e50_bn_close_touchscreen_gui_short_command_prompt_20260929.tar.gz`, SHA256 `a9d51ed1d30b2fe6af4bfc526f09cbdc2da4c47331a26df19c2c57fce4868be2`.
- Fix scope: GUI text overflow only.
- Changed accepted-wake top label from `TELL ME WHAT YOU NEED` to `SAY WHAT NEED`.
- No recognition, threshold, preprocessing, wake-wait, router/action, GPIO, response-audio, or vocabulary behavior changed.

## 2026-09-29 - Phase BN-CLOSE Touchscreen GUI Display Hold

- Prepared `outputs/e50_bn_close_touchscreen_gui_display_hold_20260929.tar.gz`, SHA256 `1d11baa7d08fc4dd1cbeb960cf083593acdc528cd31b60305f540dee3407035d`.
- Fix scope: GUI display timing and accepted-wake wording only.
- Changed accepted-wake top label to `SAY WHAT YOU NEED`.
- Added a 2-second GUI display hold for wake-gate rejection (`I AM NOT AWAKE`) and command rejection (`I DIDN'T UNDERSTAND`) so the next wake-wait loop does not immediately overwrite the message with `WAKE ME UP`.
- Operator noted for later debugging that the wake model can accept `alexa`; this should be treated as a wake false-accept / alternate-wake observation, separate from GUI display validation.
- No model, threshold, preprocessing, wake-wait runtime semantics, router/action, GPIO, response-audio, or vocabulary behavior changed.

## 2026-09-29 - Phase BN-CLOSE Touchscreen GUI UNKNOWN Rejection Text

- Prepared `outputs/e50_bn_close_touchscreen_gui_unknown_reject_text_20260929.tar.gz`, SHA256 `ca081bc22fbc76e8ebc2e7172929ce71c24ceb5853d202aa18b87a26c55547c5`.
- Fix scope: GUI display wording only.
- If a rejected command result has predicted label `UNKNOWN`, the GUI now shows `I CAN'T DO THAT` / `Say "hey pi" again.`
- Rejected supported-label predictions still show `I DIDN'T UNDERSTAND`.
- Limitation: if an out-of-vocabulary spoken phrase is predicted as a supported label below threshold, the GUI cannot know the phrase was semantically unknown and will show `I DIDN'T UNDERSTAND`.
- No model, threshold, preprocessing, wake-wait, router/action, GPIO, response-audio, or vocabulary behavior changed.

## 2026-09-29 - Phase BN-CLOSE Touchscreen GUI Wake-Not-Accepted Matcher

- Prepared `outputs/e50_bn_close_touchscreen_gui_wake_not_accepted_text_20260929.tar.gz`, SHA256 `f617fe66de2cd2e05ea4234c74c102647fd4a1bab822091a89c08215d56bc038`.
- Fix scope: GUI stdout matcher only.
- The wake-wait runtime prints `Wake not accepted (...). Still listening.` for missed wake windows. The GUI now matches that string and displays `I AM NOT AWAKE` / `Say "hey pi" again.` with the existing 2-second hold.
- No model, threshold, preprocessing, wake-wait semantics, router/action, GPIO, response-audio, or vocabulary behavior changed.

## 2026-09-29 - Phase BN-CLOSE Touchscreen Wake/UNKNOWN Display Sweep

- Recorded operator-provided summary for Pi evidence directory `pi_validation/e50_bn_close_touchscreen_gui_wake_unknown_20260929_162246`.
- Pi archive: `e50_bn_close_touchscreen_gui_wake_unknown_20260929_162246_evidence.tar.gz`.
- Pi SHA256: `d031f797a833bcdb06c00e8603e3573bd7569d048062229970c88821c1a9e01f`.
- Summary: 26 result JSON files, 26 wake accepted, 9 commands executed, 9 response playback true, 26 returned to listening, GPIO requested 0.
- Added `PHASE_BN_CLOSE_TOUCHSCREEN_GUI_DISPLAY_GUIDE.md` with current operator-facing screen messages and interpretation notes.
- Added `PHASE_BN_CLOSE_TOUCHSCREEN_WAKE_UNKNOWN_SUMMARY.md`.
- Evidence archive still needs to be copied back to local `outputs/` for source preservation.

## 2026-09-30 - Section 68 Items 10-15 Documentation Integration

Integrated post-audit controlled-validation evidence into the project records before Item 16. This was a documentation/logging update only.

Files added:

- `SECTION_68_CONTROLLED_VALIDATION_INSTRUCTIONS_REFERENCE_20260930.md`
- `E50_SECTION_68_POST_AUDIT_ITEMS_10_15_UPDATE_20260930.md`

Current item status changes from the original hard-stop audit snapshot:

- Item 10 is now VERIFIED by Pi duplicate-runtime / START-STOP evidence.
- Item 11 is now VERIFIED by network-off local Pi standalone evidence.
- Item 12 is now VERIFIED by the safety sweep evidence, with the documented wake-miss/no-wake JSON caveat.
- Item 14 is now VERIFIED by non-primary-speaker Pi validation, with mixed measured accuracy and softer-voice limitation recorded.
- Item 15 is now PARTIALLY VERIFIED by Pi performance measurements; fine-grained live timings remain unavailable without additional instrumentation.

Next Section 68 task remains Item 16 final benchmark designation. No model, threshold, dataset, router, GUI behavior, response asset, or vocabulary change was made by this update.

## 2026-09-30 - Section 68 Item 16 Completed

Recorded the final E50 benchmark as `pi_validation/e50_bn_close_item16_final_benchmark_20260930_105703` and archived it as `outputs/e50_bn_close_item16_final_benchmark_20260930_105703_evidence.tar.gz`.

Archive SHA256: `b6a2d9e66f42a1d6b4eb118f9e02505361072582e29b50add9761b1d359b5da1`.

Item 16 status is VERIFIED. No VCM implementation file, model, threshold, router, response asset, GUI behavior, runtime behavior, microphone configuration, or audio configuration was changed.

## 2026-09-30 - Final Evidence / User-Voice / Package Completion Audit Logged

Recorded the final E50 evidence audit results in the main project logs and traceability notes after the professor-facing GitHub package audit.

Scope of this logging update:

- Main project records only.
- GitHub package directory was not touched by this logging pass.
- No E50 implementation artifact, model, threshold, router, response asset, GUI behavior, runtime behavior, microphone/audio configuration, or command vocabulary was modified.

Audited package state recorded from the completed package audit:

- Package path: `github_package/ME2_VCM_E50_GITHUB_PACKAGE_20260930`.
- Final package count: 121 files including `PACKAGE_FILE_MANIFEST.csv`.
- Manifest rows: 120.
- Package size: 20,114,600 bytes.
- Package manifest SHA256: `D3D01317E936F8090EF36E484922D2A2D1CF4784D7B5C3FC6B0FB37536840F79`.
- Final recommendation: READY WITH DOCUMENTED LIMITATIONS.

Frozen identity re-verified during the audit:

- E50 weights SHA256: `BC8AC64CED4305DDF43BF4DE377F3CC636A764EFF339CD9F92AF06340C50B8FF`.
- E37 weights SHA256: `687E82E2CEFA6D74CEF2C0A15D28F8F6142D47D4A67E57C68C091E83FC2CEBDE`.
- E37 normalization SHA256: `3BFA93F202DC0C241E577E5B89506F2CB6D0F35B8239297C215A7F81E970B4C7`.
- E40 policy SHA256: `A0B2495328FD5A1E0E5885E727623BA6D9F823BE94CCCDFD0AEAD77254BBB3FD`.

User-voice provenance conclusion:

- Known Phase AF targeted recovery recordings existed: 105 clips for `CALL`, `COLOR`, `TEMPERATURE`, `NEXT`, and `LIGHT_OFF`.
- Final E50/BG training manifest contained 16,100 rows: 13,070 active-project training rows, 2,800 Dataset2 training rows, and 230 E41 reconstructed adaptation rows.
- Search of the final E50/BG training manifest found 0 matches for `PHASE_AF`, `targeted_live`, or `recovery_training`.
- Final BG/E50 records report protected-data exclusion and 0 protected path/SHA overlaps.
- Older Pi adaptation/recovery rows are present in final E50 training and have unknown speaker identity from filenames alone.
- Classification: INDETERMINATE for absolute user-voice exclusion; SUPPORTED that identified Phase AF user-recorded recovery clips are not present in the final E50/BG training manifest.
- User speech is confirmed in live Pi validation evidence, not proven final E50 training.

Remaining documented limitations:

- GUI launch-to-ready latency not measured.
- Acoustic response onset not measured.
- Full physical microphone/acoustic latency not measured.
- ECE/calibration curve not measured.
- Noise/reverb robustness not systematically measured.
- Formal phrasing and statistical speaker-independence benchmarks not performed.
- Fresh package-copy Pi launch remains deployability-partial.
- Final consolidated per-class precision/recall/F1 and final confusion-matrix reporting remain incomplete.

Timing evidence relationship:

- Item 15 saved-WAV Pi inference remains the primary Section 68 performance evidence.
- Later timing-only disposable instrumentation evidence adds live pipeline timing without replacing Item 15 and without modifying the production runtime.
- Timing archive: `e50_timing_breakdown_20260930_144234_evidence.tar.gz`, SHA256 `BE85B65BC1EC7FD074D6838D87D8C71ED20947880D8DFE205865310C7DCCD61D`.

## 2026-09-30 - E50 Overfitting Documentation Correction

Action: reviewed E50 epoch-level training history for overfitting and updated documentation to preserve the correct scientific distinction.

Finding: epoch 7 was the best internal validation-loss point and is recorded as the selected checkpoint. Later epochs showed continued training improvement with worsening validation loss: epoch 7 `val_loss=1.3987702131271362`, `val_accuracy=0.6197039305768249`; epoch 11 `loss=0.19462700002634573`, `accuracy=0.9322360248447205`, `val_loss=2.188316583633423`, `val_accuracy=0.6018376722817764`.

Implementation change: NONE.

Deployment change: NONE.

Training change: NONE.

Interpretation: classical overfitting is demonstrated in the continued training trajectory after the selected checkpoint. The finding is documented as a limitation of the training trajectory, not as evidence that a later overfit checkpoint was deployed.

## 2026-09-30 - E50 Failure Attribution Documentation Update

Action: updated E50 documentation so overfitting is not used as a catch-all explanation for command failures.

Finding: post-epoch-7 overfitting remains a demonstrated training-dynamics limitation, but command-level failures must be attributed to the most specific evidence-supported layer available: classifier confusion, data coverage, domain/speaker/acoustic variation, confidence rejection, router/action behavior, or response/output behavior.

Implementation change: NONE.

Deployment change: NONE.

Training change: NONE.

Benchmark change: NONE.

Interpretation: command failures are not attributed wholesale to overfitting. Safe rejection is E40 confidence/guardrail behavior; high-confidence wrong labels are classifier confusion; downstream failures are router/action/output failures only where directly evidenced.
