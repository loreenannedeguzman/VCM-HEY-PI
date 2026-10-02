Here is the E50 dataset explanation, keeping the important distinctions intact: Dataset A/B provenance, the final E50/BG training manifest, quality checks, distribution, augmentation, and leakage risks.

## Short Version

E50 was not trained on a single simple dataset. It used a **final Phase BG training manifest** of **16,100 rows** assembled from three sources:

| Source                         | Rows   | Role                                                                |
| ------------------------------ | ------ | ------------------------------------------------------------------- |
| `active_project_dataset`       | 13,070 | Main active-project command training data                           |
| `dataset2_vcm_balanced`        | 2,800  | Bounded speaker-diverse Dataset2 training rows for supported labels |
| `e41_reconstructed_adaptation` | 230    | Separately identified E41 Pi deployment adaptation/calibration rows |

Source: `results/phase_bg_e50_bg_revised_vocab_original_preserve_e41_init_20260928/PHASE_BG_TRAINING_MANIFEST.csv`; `PROJECT_STATUS.md`, lines 2462-2464; `REQUIREMENTS_TRACEABILITY.md`, line 739.

The important design choice was: **preserve original E50/E41-style project data, add bounded Dataset2 support where valid, and avoid training on protected evaluation/live evidence.**

**Provenance clarification for technical submission:** E50 was developed using selected material from the class collective Gold Dataset rather than using the entire collective dataset unchanged. The project-specific dataset was further prepared and balanced for the 19-command E50 vocabulary, with training-only augmentation and a separate Pi deployment-adaptation component. The resulting dataset therefore retains lineage to the collective dataset while incorporating project-specific engineering data.

The final E50 training manifest contains 16,100 rows: 13,070 active-project rows, 2,800 selected VCM_BALANCED rows, and 230 separately identified E41 Pi adaptation rows. The first two components are collective-derived/project-local command-data branches; the E41 rows are project-specific deployment adaptation data and should not be described as Gold Dataset rows unless additional evidence establishes that link.

Separate E37 wake-recording note: the recovered `Hey Pi` wake evidence is a project-specific Raspberry Pi wake-stage lineage, not part of the collective Gold Dataset and not part of the 16,100-row E50 command-model training manifest. The recovered Pi manifest at `/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi/manifest.csv` documents 99 wake-stage recordings, including 50 `WAKE` / `hey pi` rows, with 64 adaptation-designated and 35 holdout-designated rows. The exact final E37 training subset and complete E37 training configuration remain not established by the recovered evidence.

---

## 1. Dataset A and Dataset B

The project calls the downloaded Dataset2 / collective-family resource “Dataset 2,” and inside it there are two main parts. Dataset2 is treated here as selected collective-family material, not as a claim that E50 copied or used the entire Gold Dataset unchanged:

### Dataset A — `VCM_MASTER`

VCM_MASTER is a project-local Dataset2 / collective-family representation derived from selected collective dataset material; it is not claimed to be the entire Gold Dataset.

Dataset A is the larger speaker-separated corpus.

| Property                 | Value  |
| ------------------------ | ------ |
| Total samples            | 36,622 |
| Classes                  | 16     |
| Train                    | 27,130 |
| Validation               | 4,734  |
| Test                     | 4,758  |
| Speaker/group identities | 395    |
| Missing manifest audio   | 0      |
| Unreadable/corrupt audio | 0      |

Source: `results/phase_az_actual_dataset2_verification_20260927/PHASE_AZ_R_ACTUAL_DATASET2_VERIFICATION_20260927.md`, lines 66-83.

Dataset A audio properties:

| Format | Sample rate | Channels | Bits/sample | Count  |
| ------ | ----------- | -------- | ----------- | ------ |
| FLAC   | 16,000      | 1        | 16          | 18,428 |
| WAV    | 16,000      | 1        | 16          | 18,194 |

Source: same report, lines 87-93.

### Dataset A class distribution

Dataset A has 16 classes, not the final E50 19-label vocabulary.

| Class             | Train  | Val   | Test  | Total  |
| ----------------- | ------ | ----- | ----- | ------ |
| `PLAY_MUSIC`      | 495    | 70    | 89    | 654    |
| `WEATHER`         | 1,800  | 393   | 370   | 2,563  |
| `TIME`            | 323    | 68    | 65    | 456    |
| `LIGHT_ON`        | 3,130  | 463   | 542   | 4,135  |
| `LIGHT_OFF`       | 2,456  | 353   | 427   | 3,236  |
| `LIGHT_DIM`       | 261    | 61    | 44    | 366    |
| `SET_TIMER`       | 545    | 92    | 80    | 717    |
| `SET_ALARM`       | 1,166  | 148   | 132   | 1,446  |
| `SET_TEMPERATURE` | 360    | 20    | 20    | 400    |
| `MEDIA_PAUSE`     | 242    | 32    | 41    | 315    |
| `MEDIA_STOP`      | 287    | 38    | 46    | 371    |
| `MEDIA_NEXT`      | 956    | 116   | 120   | 1,192  |
| `VOLUME_UP`       | 2,296  | 318   | 396   | 3,010  |
| `VOLUME_DOWN`     | 2,000  | 275   | 329   | 2,604  |
| `UNKNOWN`         | 10,181 | 1,991 | 1,779 | 13,951 |
| `SILENCE`         | 632    | 296   | 278   | 1,206  |

Source: same report, lines 95-117.

---

### Dataset B — `VCM_BALANCED`

VCM_BALANCED is a training-derived subset of VCM_MASTER and therefore inherits its collective-family provenance. It was prepared specifically for project training and includes training-domain augmentation.

Dataset B is a train-only balanced subset derived from Dataset A training data.

| Property                 | Value  |
| ------------------------ | ------ |
| Training rows/files      | 15,268 |
| Classes                  | 16     |
| Original rows            | 13,801 |
| Augmented rows           | 1,467  |
| Missing manifest audio   | 0      |
| Unreadable/corrupt audio | 0      |
| Speaker/group identities | 298    |

Source: AZ-R report, lines 78-83, 141-149, 151-168; `REQUIREMENTS_TRACEABILITY.md`, lines 163-166.

Dataset B class distribution:

| Class             | Rows  |
| ----------------- | ----- |
| `PLAY_MUSIC`      | 600   |
| `WEATHER`         | 1,400 |
| `TIME`            | 600   |
| `LIGHT_ON`        | 1,200 |
| `LIGHT_OFF`       | 1,200 |
| `LIGHT_DIM`       | 522   |
| `SET_TIMER`       | 600   |
| `SET_ALARM`       | 1,000 |
| `SET_TEMPERATURE` | 600   |
| `MEDIA_PAUSE`     | 484   |
| `MEDIA_STOP`      | 574   |
| `MEDIA_NEXT`      | 956   |
| `VOLUME_UP`       | 1,200 |
| `VOLUME_DOWN`     | 1,200 |
| `UNKNOWN`         | 2,500 |
| `SILENCE`         | 632   |

Source: AZ-R report, lines 118-139.

---

## 2. Provenance

Dataset2 was audited against the downloaded files and its specification PDF.

Project evidence says the actual files were under:

```
data/VCM Dataset2/VCM
```

and the specification PDF was:

```
data/VCM Dataset2 Specifications.pdf
```

Source: AZ-R report, lines 11-15.

The audit found the actual downloaded dataset matched its specification for:

- total file counts,
- train/validation/test rows,
- class counts,
- speaker/group counts,
- original versus augmented counts,
- missing audio,
- corrupt/unreadable audio.

Source: AZ-R report, lines 66-85.

The dataset file inventory under `data/VCM Dataset2/VCM` was:

| Extension   | Count  |
| ----------- | ------ |
| `.wav`      | 33,462 |
| `.flac`     | 18,428 |
| `.csv`      | 46     |
| `.txt`      | 23     |
| `.log`      | 2      |
| Total files | 51,961 |

Source: AZ-R report, lines 44-55.

---

## 3. How Dataset2 Maps to E50 Labels

This is one of the most important parts.

Dataset2 does **not** directly match the final E50 vocabulary. Dataset2 has 16 classes. E50 has 19 final labels.

The audit mapped Dataset2 classes to current VCM labels:

| Dataset2 class    | E50 / VCM label                | Mapping status              |
| ----------------- | ------------------------------ | --------------------------- |
| `PLAY_MUSIC`      | `PLAY_MUSIC`                   | Direct                      |
| `WEATHER`         | `WEATHER`                      | Direct                      |
| `TIME`            | `TIME`                         | Direct                      |
| `LIGHT_ON`        | `LIGHT_ON`                     | Direct                      |
| `LIGHT_OFF`       | `LIGHT_OFF`                    | Direct                      |
| `LIGHT_DIM`       | `BRIGHTNESS` / dimming support | Partial / nuanced           |
| `SET_TIMER`       | `TIMER`                        | Direct                      |
| `SET_ALARM`       | `ALARM`                        | Direct                      |
| `SET_TEMPERATURE` | `TEMPERATURE`                  | Direct with caveat          |
| `MEDIA_PAUSE`     | `PAUSE`                        | Direct                      |
| `MEDIA_STOP`      | `STOP`                         | Direct                      |
| `MEDIA_NEXT`      | `NEXT`                         | Direct with group caveat    |
| `VOLUME_UP`       | `VOLUME_UP`                    | Direct                      |
| `VOLUME_DOWN`     | `VOLUME_DOWN`                  | Direct                      |
| `UNKNOWN`         | `UNKNOWN`                      | Auxiliary no-action support |
| `SILENCE`         | Silence/no-action              | Auxiliary no-action support |

Source: AZ-R report, lines 194-213.

Dataset2 did **not** provide direct coverage for:

- `COLOR`
- `CREATE_REMINDER`
- `LIST_REMINDERS`
- `CALL`
- `MESSAGE`

Source: AZ-R report, lines 215-221.

For final E50, historical `COLOR` was removed and `LIGHT_DIM` was added. The final E50 labels include `LIGHT_DIM`, not a separate final `COLOR` label.

Source: `PHASE_BG_DATASET_SUMMARY.json`, `vocabulary_revision`.

---

## 4. Final E50/BG Training Manifest

The final E50 training manifest was:

```
results/phase_bg_e50_bg_revised_vocab_original_preserve_e41_init_20260928/PHASE_BG_TRAINING_MANIFEST.csv
```

It has **16,100 rows**.

### Manifest columns

The manifest columns are:

```
training_example_id
source_dataset
source_partition
source_path
source_label
vcm_label
speaker_group
real_or_augmented_or_synthetic
sha256
dataset_role
resolved_path
phrase
dataset2_source_dataset
dataset2_source_type
dataset2_original_or_augmented
dataset2_augmentation_type
dataset2_group_id
```

That means each training row carries:

- a stable training example ID,
- source dataset identity,
- source partition,
- original source label,
- final VCM label,
- speaker/group identity,
- real/augmented/synthetic status,
- SHA256 hash,
- resolved file path,
- phrase text where available,
- Dataset2 provenance fields where applicable.

This is a strong manifest structure because it preserves both **label mapping** and **source provenance**.

### Final manifest source composition

| Source dataset                 | Rows       |
| ------------------------------ | ---------- |
| `active_project_dataset`       | 13,070     |
| `dataset2_vcm_balanced`        | 2,800      |
| `e41_reconstructed_adaptation` | 230        |
| **Total**                      | **16,100** |

Source: `PHASE_BG_TRAINING_MANIFEST.csv`; also summarized in `PROJECT_STATUS.md`, lines 2462-2464.

### Final manifest data-kind composition

| Kind              | Rows       |
| ----------------- | ---------- |
| real              | 15,260     |
| augmented         | 480        |
| real_multi_sensor | 200        |
| synthetic         | 160        |
| **Total**         | **16,100** |

Derived read-only from `PHASE_BG_TRAINING_MANIFEST.csv`.

### Final manifest label distribution

Most labels have 900 rows. Five labels have 700 rows because Dataset2 did not provide usable direct support for them.

| E50 label         | Rows |
| ----------------- | ---- |
| `PLAY_MUSIC`      | 900  |
| `WEATHER`         | 900  |
| `TIME`            | 900  |
| `LIGHT_ON`        | 900  |
| `LIGHT_OFF`       | 900  |
| `LIGHT_DIM`       | 900  |
| `BRIGHTNESS`      | 700  |
| `TIMER`           | 900  |
| `ALARM`           | 900  |
| `TEMPERATURE`     | 900  |
| `NEXT`            | 900  |
| `PAUSE`           | 900  |
| `STOP`            | 900  |
| `VOLUME_UP`       | 900  |
| `VOLUME_DOWN`     | 900  |
| `CREATE_REMINDER` | 700  |
| `LIST_REMINDERS`  | 700  |
| `CALL`            | 700  |
| `MESSAGE`         | 700  |

Derived read-only from `PHASE_BG_TRAINING_MANIFEST.csv`; also consistent with `PHASE_BG_HYBRID_CLASS_COUNTS.csv`.

---

## 5. How E50 Selected Training Rows

Phase BG’s selection rule was:

```
retain E41 lineage where applicable
cap active-project original data at 700 rows per label
add up to 200 Dataset2 rows for supported labels
```

In the E50 dataset summary, this is described as:

```
original cap per label: 700
dataset2 cap per supported label: 200
```

Rationale:

```
More original-domain preservation than E49 while retaining bounded Dataset2 speaker diversity.
```

Source: `PHASE_BG_DATASET_SUMMARY.json`, `balancing_rule`.

This is why the labels with Dataset2 support typically have:

```
700 active/original + 200 Dataset2 = 900 rows
```

and unsupported labels have:

```
700 active/original only
```

The Phase BG candidate report describes the changed variable as:

```
original cap 700 per label plus up to 200 Dataset2 training rows for supported labels
```

Source: `PHASE_BG_E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT_CNN_CANDIDATE_20260928.md`, lines 11-15.

---

## 6. Augmentation and Synthetic Data

Dataset B contains both original and augmented rows.

Dataset B augmentation counts from the Dataset2 audit:

| Augmentation type   | Count     |
| ------------------- | --------- |
| gain                | 410       |
| noise               | 425       |
| pitch               | 36        |
| shift               | 380       |
| speed               | 216       |
| **Total augmented** | **1,467** |

Source: AZ-R report, lines 141-149.

In the final E50 training manifest, because E50 only selected a bounded subset of Dataset2 rows, the actually selected Dataset2 augmentation counts were lower:

| Augmentation type in E50 manifest | Rows |
| --------------------------------- | ---- |
| gain                              | 166  |
| noise                             | 150  |
| pitch                             | 10   |
| shift                             | 124  |
| speed                             | 89   |

Derived read-only from `PHASE_BG_TRAINING_MANIFEST.csv`.

There is also synthetic support, mainly around temperature:

- Dataset2 synthetic rows total: 480
- Synthetic `SET_TEMPERATURE` rows: 480
- Final E50 manifest selected 160 synthetic rows

Source: AZ-R report, lines 170-192; final manifest grouping.

Important caveat from the audit:

> Synthetic speech must remain documented as training-domain support, not as equivalent to independent real-speaker evidence.

Source: AZ-R report, line 192.

---

## 7. Quality Checks

The Dataset2 audit established several quality points:

### File completeness

- Dataset A missing manifest audio: 0
- Dataset A unreadable/corrupt audio: 0
- Dataset B missing manifest audio: 0
- Dataset B unreadable/corrupt audio: 0

Source: AZ-R report, lines 76-83.

### Audio format

Dataset A and B audio were checked using actual headers, not just by trusting the PDF:

- WAV headers read with Python `wave`
- FLAC STREAMINFO headers parsed directly

Source: AZ-R report, line 85.

### Sample rate / channels / bit depth

- Dataset A FLAC: 16 kHz, mono, 16-bit
- Dataset A WAV: 16 kHz, mono, 16-bit
- Dataset B WAV: 16 kHz, mono, 16-bit

Source: AZ-R report, lines 87-93.

### Speaker independence

The audit verified train/validation/test speaker separation:

| Check                                       | Count |
| ------------------------------------------- | ----- |
| Dataset A train speakers/groups             | 298   |
| Dataset A validation speakers/groups        | 49    |
| Dataset A test speakers/groups              | 48    |
| Dataset A all speakers/groups               | 395   |
| Dataset B speakers/groups                   | 298   |
| Train intersection validation               | 0     |
| Train intersection test                     | 0     |
| Validation intersection test                | 0     |
| Dataset B intersection Dataset A validation | 0     |
| Dataset B intersection Dataset A test       | 0     |

Source: AZ-R report, lines 151-168.

This supports the claim that Dataset2’s train/validation/test splits are speaker-separated, and Dataset B does not overlap Dataset A validation/test speakers.

---

## 8. Leakage Controls

The project was careful about leakage, but it also documented limits.

### Controls that were verified

1. **Dataset B derives only from Dataset A train.**\
   Dataset B source split counts show train-only use.

   Source: AZ-R report, lines 141-149.
2. **No Dataset A validation/test source rows leaked into Dataset B.**\
   Source val/test leak rows: 0.

   Source: AZ-R report, lines 147-149.
3. **Speaker split intersections were zero.**\
   Train/validation/test speaker intersections were all zero.

   Source: AZ-R report, lines 151-168.
4. **Byte-level overlap checks were performed.**

| Comparison                            | Dataset2 files hashed | Project files hashed | Byte-identical overlap |
| ------------------------------------- | --------------------- | -------------------- | ---------------------- |
| Dataset2 B vs active project dataset  | 15,268                | 21,001               | 0                      |
| Dataset2 B vs protected project audio | 15,268                | 615                  | 0                      |

Source: AZ-R report, lines 225-242.

5. **Protected evaluation/live evidence was not supposed to enter training.**\
   Phase BG candidate report says no current95, Phase AV, Dataset2 val/test, active validation/test, or live evidence was used for training.

   Source: Phase BG candidate report, lines 17-22.
6. **Phase BG contamination check reported no protected overlap.**

```
"contamination_check": {
  "protected_path_overlap": 0,
  "protected_sha256_overlap": 0,
  "protected_hashes_checked": 14142
}
```

Source: `PHASE_BG_DATASET_SUMMARY.json`.

### Leakage risks / caveats still documented

The project does **not** claim perfect impossibility of all overlap.

The Dataset2 audit says the active project dataset index lacked upstream `original_dataset` / `original_id` fields. Therefore:

- byte-level overlap was checked,
- but source-family overlap cannot be fully excluded from current metadata alone.

Source: AZ-R report, lines 225-233.

This means: if two datasets came from similar upstream corpora but the files are not byte-identical, the project cannot fully prove there is no source-family relationship without more upstream metadata.

That is a limitation, not a failure.

---

## 9. Important Distribution Risks

### 1. Dataset2 is 16-class, E50 is 19-label

Dataset2 does not fully cover final E50.

Final E50 has:

```
PLAY_MUSIC
WEATHER
TIME
LIGHT_ON
LIGHT_OFF
LIGHT_DIM
BRIGHTNESS
TIMER
ALARM
TEMPERATURE
NEXT
PAUSE
STOP
VOLUME_UP
VOLUME_DOWN
CREATE_REMINDER
LIST_REMINDERS
CALL
MESSAGE
```

Dataset2 does not directly provide:

```
CREATE_REMINDER
LIST_REMINDERS
CALL
MESSAGE
```

and it does not provide the final historical `BRIGHTNESS`/`LIGHT_DIM` distinction perfectly.

Source: AZ-R report, lines 215-223; `PHASE_BG_DATASET_SUMMARY.json`.

### 2. `LIGHT_DIM` / `BRIGHTNESS` semantics are not perfect

The Phase BG summary says:

- `LIGHT_DIM`: dim-down examples plus Dataset2 `LIGHT_DIM`
- `BRIGHTNESS`: dim-up active-project examples plus historical brightness adaptation
- limitation: the distinction is evidence-supported but imperfect because historical `BRIGHTNESS` was broader

Source: `PHASE_BG_DATASET_SUMMARY.json`, `light_dim_brightness_semantics`.

### 3. `TEMPERATURE` uses synthetic support

Dataset2 `SET_TEMPERATURE` had synthetic-heavy support:

- 600 Dataset B temperature rows
- 480 synthetic-derived in Dataset2
- final E50 selected 160 synthetic rows

The audit warns synthetic speech is training-domain support, not equivalent to independent real-speaker evidence.

Source: AZ-R report, lines 170-192.

### 4. `NEXT` has grouped multi-sensor caveat

Dataset2 supports `NEXT` through `MEDIA_NEXT`, but the audit notes it is 956 recordings from grouped multi-sensor captures, and reports warn this is 239 unique utterance groups, not 956 fully independent utterances.

Source: AZ-R report, lines 246-254.

### 5. FLAC validation/test limitation

The Phase BG dataset summary states that Dataset2 validation/test include FLAC rows, while the project audio loader supports PCM WAV only in that environment. FLAC rows were not trained on or relabeled; they were recorded as a held-out evaluation limitation.

Source: `PHASE_BG_DATASET_SUMMARY.json`, `dataset2_master_evaluation_limitation`.

---

## 10. What Was Not Used for E50 Training

The project repeatedly emphasizes that protected evaluation/live evidence should not be used as training data.

Not used for Phase BG training, according to the Phase BG candidate report:

- current95 evaluation evidence
- Phase AV evidence
- Dataset2 validation/test
- active validation/test
- live evidence

Source: Phase BG candidate report, lines 17-22.

The final traceability summary also notes:

- Phase AF user-recorded targeted recovery clips existed,
- but were not identified in the final E50/BG training manifest,
- search found 0 `PHASE_AF`, `targeted_live`, or `recovery_training` matches.

Source: `REQUIREMENTS_TRACEABILITY.md`, line 740; `PROJECT_STATUS.md`, lines 2462-2464.

However, it also states that absolute exclusion of all historical user voice from training lineage remains **indeterminate** because older Pi adaptation/recovery rows are present and speaker identity cannot be proven from filename alone.

Source: `REQUIREMENTS_TRACEABILITY.md`, lines 740-741.

That nuance matters: the project can say the specific known Phase AF targeted clips were not in the final manifest, but it should not overclaim that no historical user voice exists anywhere in older adaptation lineage.

---

## 11. How to Explain the E50 Dataset in Class

A clean technical explanation would be:

> E50 used a curated 16,100-row training manifest. Most rows came from the active project command dataset, with a bounded 2,800-row contribution from the audited Dataset2 balanced training set and 230 reconstructed E41 adaptation rows. Dataset2 itself was verified against its specification: Dataset A had 36,622 samples across train/validation/test speaker-separated splits, and Dataset B had 15,268 train-only rows with 13,801 originals and 1,467 augmentations. The final E50 vocabulary has 19 labels, so Dataset2 did not cover every final command; it was used only where mapping was defensible. The project checked for missing/corrupt audio, speaker leakage, validation/test leakage, and byte-level overlap with protected project evidence. Remaining caveats include incomplete Dataset2 coverage for the 19-label vocabulary, synthetic temperature support, grouped multi-sensor NEXT examples, and source-family overlap that cannot be fully excluded without upstream IDs.

That explanation is accurate and honest.

---

## 12. Bottom Line

The E50 dataset story is not “we downloaded a dataset and trained on it.”

It is:

1. **Dataset2 was audited first.**
2. **Dataset A/B counts, splits, speakers, and audio integrity were verified.**
3. **Dataset B was train-only and derived from Dataset A train.**
4. **Dataset2 was mapped carefully into the VCM label space.**
5. **E50 used only bounded Dataset2 support, not the entire dataset.**
6. **Missing labels were supplied by active project data.**
7. **Protected evaluation/live data were excluded.**
8. **Leakage checks were performed, but source-family overlap has a documented caveat.**
9. **The final E50 training manifest is traceable row-by-row with source, label, speaker/group, SHA256, and provenance fields.**

That is a solid dataset pipeline for a student embedded ML project, especially because the limitations are documented rather than hidden.

