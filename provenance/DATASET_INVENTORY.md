# DATASET_INVENTORY

Dataset inspection status for ME2 - Voice Controlled Smart Device.

## Current Finding

**Technical provenance clarification:** The class collective Gold Dataset is the common curated dataset foundation. This project used selected local material with lineage to that collective dataset family; it did not use or claim to contain the entire Gold Dataset unchanged. E50 later combined collective-derived/project-local command data with a separately identified 230-row E41 Pi deployment adaptation/calibration branch. The E41 rows should not be described as Gold Dataset samples unless additional evidence establishes that link.

**Separate E37 wake-recording clarification:** the recovered `Hey Pi` wake-recording evidence is a project-specific Raspberry Pi wake-stage lineage, not part of the class collective Gold Dataset lineage and not part of the 16,100-row E50 command-model training manifest. The recovered Pi manifest at `/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi/manifest.csv` documents 99 wake-stage recordings, including 50 `WAKE` / `hey pi` rows, 64 adaptation-designated rows, and 35 holdout-designated rows. The exact final E37 training subset, E37 training hyperparameters, E37 validation metrics, augmentation count, and speaker/recordist count remain not established.

User downloaded the Google Drive ZIP chunks locally into:

`data/drive-download-20260915T084940Z-1-001/`
`data/drive-download-20260915T085515Z-1-001/`
`data/drive-download-20260915T085520Z-1-001/`
`data/drive-download-20260915T085526Z-1-001/`
`data/drive-download-20260915T085531Z-1-001/`
`data/drive-download-20260915T085536Z-1-001/`

These extracted folders are now the active local dataset for Phase 1.

Earlier, a partial public-page mirror was downloaded into:

`data/raw/google_drive_dataset/`

That earlier mirror exposed only 2,000 WAVs and was superseded by the extracted ZIP data. It was deleted on 2026-09-16 so it cannot be accidentally mixed into training/evaluation.

Files present before project scaffolding:
- `VCM AGENT.docx`
- `VCM AGENT.pdf`
- `VCM Machine Exercise.pdf`

Additional planning file found during verification:
- `VCM Sources.xlsx`
- `VCM Sources.pdf`

## Source List Summary

`VCM Sources.xlsx` contains candidate source links, including:
- SLURP
- Fluent Speech Commands
- Google Speech Commands v2
- eSpeak NG synthetic generation
- Chatterbox TTS with LibriSpeech/Common Voice references
- Kaggle mirrors or related speech-command datasets
- Mozilla Common Voice

These source links are retained for context. The active local dataset source is local Google Drive-derived/project-local material associated with the collective dataset family; exact row-level mapping from every local row to the supplied Google Drive folder ID is not claimed here.

## Source Interpretation

`VCM Sources.pdf` explains the candidate data sources associated with Mark M, including SLURP, Fluent Speech Commands, Google Speech Commands v2, eSpeak NG, and Chatterbox TTS with LibriSpeech/Common Voice references.

The active local dataset already includes speaker diversity, phrase diversity, and acoustic variation. Therefore, additional augmentation is NOT required before the first baseline. Augmentation may be revisited later as a train-only experiment if measured validation or noise robustness results show the need.

## Dataset Provenance, Structure, And Description

### Provenance

The dataset is a locally stored voice-command dataset assembled from sources listed in `VCM Sources.pdf` and `VCM Sources.xlsx`. The relevant contributor entry is Mark Andrian Macalalad.

The documented source ingredients are:
- SLURP: used as a source of human speech recordings selected to match the project's voice-command labels.
- Fluent Speech Commands: used for spoken commands involving lights, music, volume, and temperature, then mapped to project labels.
- Google Speech Commands v2: used for recorded stop commands and background-noise samples to supplement command and silence/noise-related material.
- eSpeak NG: used to generate synthetic command recordings with variation in speed, pitch, and volume.
- Chatterbox TTS with LibriSpeech and Mozilla Common Voice references: designed to generate synthetic commands using speaker references, including LibriSpeech and Filipino-English speakers.

This means the dataset is not a general ASR corpus for transcription. It is a command-intent dataset designed for a small VCM. Its purpose is to train a model that maps short audio utterances directly to command categories.

### Active Local Copy

The active local dataset is stored offline in the extracted Google Drive ZIP folders:
- `data/drive-download-20260915T084940Z-1-001/`
- `data/drive-download-20260915T085515Z-1-001/`
- `data/drive-download-20260915T085520Z-1-001/`
- `data/drive-download-20260915T085526Z-1-001/`
- `data/drive-download-20260915T085531Z-1-001/`
- `data/drive-download-20260915T085536Z-1-001/`

The earlier `data/raw/google_drive_dataset/` folder was only a partial public-page mirror and was deleted on 2026-09-16. It is not part of the active dataset.

### Structure

The active dataset has two logical portions:

1. Fixed-phrase portion:
   - Folder: `drive-download-20260915T084940Z-1-001/`
   - 20 raw command labels.
   - 50 apparent speaker IDs.
   - 1 fixed phrase per raw label.
   - 3 acoustic variations.
   - 3,000 WAV files.

2. Phrase-variant portion:
   - Folders: `drive-download-20260915T085515Z-1-001/` through `drive-download-20260915T085536Z-1-001/`
   - 20 raw command labels.
   - 30 apparent speaker IDs.
   - 10 phrase variants per raw label.
   - 3 acoustic variations: clean, mild background noise, and quieter/farther microphone.
   - 18,001 WAV files locally observed, including one duplicate-style extra WEATHER file.

Folder layout is class-based. Each class folder contains WAV files whose names encode:
- raw label
- speaker ID
- phrase ID
- acoustic variation ID

Example filename pattern:

`WEATHER_s5_p2_v2.wav`

This means:
- raw label: WEATHER
- apparent speaker ID: 5
- phrase ID: 2
- variation ID: 2

### Dataset Description

The active dataset contains short spoken smart-device command utterances. The raw labels cover 20 command forms, which are mapped into the assignment's 10 command intents:
- PLAY_MUSIC
- QUESTION
- LIGHT_CONTROL
- LIGHT_ADJUST
- SET_TIMER
- SET_ALARM
- THERMOSTAT
- MEDIA_CONTROL
- REMINDER
- CALL_MESSAGE

The dataset is suitable for a direct VCM because the examples are short commands, already stored as local WAV files, and already normalized to the assignment's expected audio direction:
- 16 kHz sample rate
- mono channel count
- short duration recordings

### Why This Is Sufficient Before Augmentation

Additional augmentation is not required before the first baseline because the active dataset already includes:
- multiple speakers
- human and synthetic/source-derived variety
- multiple phrase variants for most of the larger portion
- acoustic variants including noise and distance/volume changes
- balanced raw-label counts after excluding the one duplicate-style file

The correct experimental order is:
1. index and split the dataset
2. implement preprocessing
3. train a baseline
4. measure validation/test performance
5. only then decide whether train-only augmentation is needed

### Known Limitations

- UNKNOWN is not present as a raw dataset label.
- Speaker IDs are inferred from filenames and still need source-metadata verification if available.
- The dataset source/provenance is documented from `VCM Sources.pdf`, `VCM Sources.xlsx`, and included local support files, but licensing details still need final confirmation if required by the technical reader.
- The extra file `WEATHER_s5_p2_v2(1).wav` is excluded from the official included set because it appears to be a duplicate-style extra file.

## Download Summary - Deleted Superseded Public-Page Mirror

Deletion note:
- Deleted on: 2026-09-16
- Deleted path: `data/raw/google_drive_dataset/`
- Reason: earlier partial mirror with only 2,000 WAV files; removed so it is not accidentally mixed into training/evaluation by default.

Date/time: 2026-09-15 16:47:33 +08:00

Source:
- Google Drive folder ID: `1YWwWkP1L4MfnJ5rCzqI5fmNBwKht0NW-`

Local path:
- `data/raw/google_drive_dataset/`
Status:
- DELETED on 2026-09-16.

Manifest:
- `data/raw/google_drive_dataset/_download_manifest.json`
Status:
- DELETED with the superseded folder.

Observed local files:
- Manifest file entries: 2,004
- Local WAV files: 2,000
- Local support text/markdown files: 4
- Local WAV bytes: 71,738,560

Audio verification:
- Readable WAV files: 2,000
- Unreadable/corrupted WAV files: 0
- Sample rate: 16,000 Hz for all 2,000 WAV files
- Channels: mono for all 2,000 WAV files
- Duration range: 0.480 s to 3.400 s
- Mean duration: 1.120 s

Observed groups:
- `1 fixed phrase_command`
- `10 phrase variants_command`

Observed labels in each group:
- ALARM
- CALL
- DIM_DOWN
- DIM_UP
- LIGHT_OFF
- LIGHT_ON
- LIST_REMINDERS
- MESSAGE
- NEXT
- PAUSE
- PLAY_MUSIC
- SET_REMINDER
- STOP
- TEMP_DOWN
- TEMP_UP
- TIME
- TIMER
- VOLUME_DOWN
- VOLUME_UP
- WEATHER

Observed per-label count:
- 50 WAV files per label per group
- 20 labels per group
- 1,000 WAV files per group
- 2,000 WAV files total

Completeness warning for superseded mirror:
- `1 fixed phrase_command` includes a note claiming 3,000 WAV files total.
- `10 phrase variants_command` includes a note claiming 18,000 WAV files total.
- The unauthenticated Google Drive page exposed only 50 files per class folder.
- Google Drive API listing with the page API key was blocked without authenticated access.
- Therefore, the public-page mirror is PARTIAL and should not be the primary dataset.

## Download Summary - Active Extracted ZIP Dataset

Date/time: 2026-09-15 17:08:15 +08:00

Local ZIP files:
- `drive-download-20260915T084940Z-1-001.zip`
- `drive-download-20260915T085515Z-1-001.zip`
- `drive-download-20260915T085520Z-1-001.zip`
- `drive-download-20260915T085526Z-1-001.zip`
- `drive-download-20260915T085531Z-1-001.zip`
- `drive-download-20260915T085536Z-1-001.zip`

Extracted local folders:
- `drive-download-20260915T084940Z-1-001/`: 3,000 WAVs
- `drive-download-20260915T085515Z-1-001/`: 3,600 WAVs
- `drive-download-20260915T085520Z-1-001/`: 3,600 WAVs
- `drive-download-20260915T085526Z-1-001/`: 3,600 WAVs
- `drive-download-20260915T085531Z-1-001/`: 3,600 WAVs
- `drive-download-20260915T085536Z-1-001/`: 3,601 WAVs

Observed local files in active extracted dataset:
- WAV files: 21,001
- WAV bytes: 816,536,204

Audio verification:
- Readable WAV files: 21,001
- Unreadable/corrupted WAV files: 0
- Sample rate: 16,000 Hz for all 21,001 WAV files
- Channels: mono for all 21,001 WAV files
- Duration range: 0.200 s to 3.880 s
- Mean duration: 1.214 s

Observed active dataset labels:
- ALARM: 1,050
- CALL: 1,050
- DIM_DOWN: 1,050
- DIM_UP: 1,050
- LIGHT_OFF: 1,050
- LIGHT_ON: 1,050
- LIST_REMINDERS: 1,050
- MESSAGE: 1,050
- NEXT: 1,050
- PAUSE: 1,050
- PLAY_MUSIC: 1,050
- SET_REMINDER: 1,050
- STOP: 1,050
- TEMP_DOWN: 1,050
- TEMP_UP: 1,050
- TIME: 1,050
- TIMER: 1,050
- VOLUME_DOWN: 1,050
- VOLUME_UP: 1,050
- WEATHER: 1,051

Dataset groups:
- Fixed phrase group: 3,000 WAVs, 20 labels, 50 apparent speaker IDs.
- Phrase variants group: 18,001 WAVs, 20 labels, 30 apparent speaker IDs.

Completeness status:
- The extracted ZIP data matches the support-file expectation of 3,000 fixed-phrase WAVs plus approximately 18,000 phrase-variant WAVs.
- There is one extra file in WEATHER: `WEATHER_s5_p2_v2(1).wav`.
- The expected WEATHER speaker/phrase/variation combinations are present, so the extra file appears duplicate-style and should be handled before creating splits.
- No extra augmentation is required before creating the first baseline dataset split.

## Dataset Items To Inspect

When the dataset is available, inspect and record:
- dataset path
- provenance/license
- directory structure
- file formats
- sample rates
- channel count
- number of recordings
- duration distribution
- class distribution
- speaker metadata
- speaker overlap across splits
- corrupted/unreadable files
- label mapping to assignment intents

## Current Status

Dataset: IDENTIFIED AND LOCAL.

Speaker metadata: inferred from filenames only; NOT YET VERIFIED against source metadata.

Train/validation/test split: CREATED.

Class distribution: MEASURED for active extracted dataset.

Corrupted file check: EXECUTED for active extracted dataset; 0 unreadable WAV files found.

Metadata index: CREATED at `data/metadata/active_dataset_index.csv`.

Split summary: CREATED at `data/metadata/active_dataset_split_summary.csv`.

Split plan: CREATED at `data/metadata/DATASET_SPLIT_PLAN.md`.

Included WAV files after duplicate handling: 21,000.

Excluded WAV files: 1 (`WEATHER_s5_p2_v2(1).wav`).

## Dataset Inventory Snapshot - 2026-09-21

This snapshot records the dataset sources currently available and how they are
being used as of the E28 Raspberry Pi recovery stage.

### Active Original VCM Dataset

- Location: `data/drive-download-*`
- WAV files found: 21,001.
- Official included WAV files: 21,000.
- Excluded file: `WEATHER_s5_p2_v2(1).wav`.
- Raw labels: 20.
- Format: 16 kHz mono WAV.
- Official split:
  - train: 16,800
  - validation: 2,100
  - test: 2,100
- Usage:
  - source dataset for baseline and CNN training;
  - source replay for Pi recovery models;
  - not a replacement for real Pi microphone validation.

### Laptop And Early Real-Microphone Calibration Sets

- `data/calibration/LAPTOP_CALIBRATION_SET_002`: 50 laptop microphone WAVs.
- `data/calibration/LIGHT_CONTROL_REALMIC_SET_003_TURN_ON_25`: 25 real-mic
  `LIGHT_ON` style clips.
- `data/calibration/LIGHT_CONTROL_REALMIC_SET_004_TURN_OFF_25`: 25 real-mic
  `LIGHT_OFF` style clips.
- Usage:
  - diagnostic evidence for microphone/domain shift;
  - light-command adaptation evidence;
  - not final Raspberry Pi proof.

### Raspberry Pi All-Command Calibration Set

- Location: `data/calibration/pi_validation/all_commands_calibration_15x`
- Total WAV files: 285.
- Labels: 19.
- Trials: 15 per label.
- Split:
  - adaptation: 190 clips.
  - holdout: 95 clips.
- Usage:
  - core real Pi microphone dataset;
  - used for E24/E25 raw-command recovery;
  - holdout split used for Pi validation/guardrail measurement.

### Fresh Pi Recovery Sets

- `data/calibration/fresh_pi_miniset_20260920`: 9 WAVs, three each for
  `STOP`, `NEXT`, and `COLOR`.
- `data/calibration/e26_live_failures_20260920`: 6 WAVs, new E26 `NEXT` and
  `COLOR` failure clips.
- `data/calibration/e27_live_validation_20260920`: 6 WAVs, E27 live validation
  clips later used for E28 recovery.
- Usage:
  - development/recovery data for E26, E27, and E28;
  - not final independent proof after being used for training/recovery.

### Posted Collective Dataset

The posted collective dataset should be understood as a common class Gold Dataset resource. The project-local use documented here is selective and derivative: VCM_MASTER and VCM_BALANCED support project training and audit needs, but they are not presented as the entire Gold Dataset.

- Location: `C:\Users\Loreen Anne\Downloads\VCM\VCM`
- `VCM_MASTER`:
  - manifest rows: 36,622.
  - split rows: train 27,130; validation 4,734; test 4,758.
  - audio files observed on disk in `VCM_MASTER/audio`: 18,194 WAV files, with
    additional non-WAV audio described by the dataset documentation.
  - classes: 16, including `UNKNOWN` and `SILENCE`.
- `VCM_BALANCED`:
  - training rows/files: 15,268 WAV files.
  - classes: 16, including `UNKNOWN` and `SILENCE`.
- Usage decision:
  - cite and document first;
  - integrate only selectively if useful;
  - potential support for `UNKNOWN`/`SILENCE` and robustness comparison;
  - do not restart the current Pi deployment path around it.

### Integrity Notes

- Recovery data and final validation data must stay separate.
- E26/E27/E28 are documented recovery candidates, not final proof by
  themselves.
- A defensible 100/100 claim needs fresh or held-out Pi microphone validation
  that was not used to train the candidate being reported.
- Robustness tests for ambient noise, distance, and not-Loreen speaker should be
  reported separately from the main clean validation benchmark.

