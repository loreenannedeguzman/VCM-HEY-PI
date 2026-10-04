# Dataset And Training

## Engineering Question

How was the command dataset prepared, loaded, processed, and used to train E50?

The project dataset was prepared as a manifest-driven command-intent resource, not as a general speech-to-text corpus. The training goal was to map short audio commands directly to fixed command labels. The training script should therefore load an explicit manifest of examples rather than recursively grabbing arbitrary audio files from folders.

## Source And Cleanup

The active command-data lineage came from locally stored Google Drive-derived/project-local material associated with the collective dataset family. An earlier partial public-page mirror exposed only about 2,000 WAV files and was excluded/deleted from the active path so it would not be mixed into training or evaluation by accident. The active material was audited for file counts, readability, audio properties, labels, speaker/group identifiers, phrase variants, and acoustic variants.

E50 does not claim to be trained on the entire collective Gold Dataset unchanged. It used selected collective-family/project-local command material plus a separate project-specific E41 Pi adaptation branch.

## Dataset Views

| Dataset view | Established values | Role |
|---|---:|---|
| `VCM_MASTER` | 36,622 samples; 16 classes; 27,130 train; 4,734 validation; 4,758 test; 395 speaker/group identities; 0 documented train/validation/test speaker overlap | Larger audited speaker-separated dataset view. |
| `VCM_BALANCED` | 15,268 train-only rows; 13,801 original; 1,467 augmented; 298 speaker/group identities | Balanced training-derived subset of `VCM_MASTER`. |
| Final E50 manifest | 16,100 rows | Exact command-model training manifest for E50 Phase BG. |

`VCM_BALANCED` inherits collective-family provenance from `VCM_MASTER`; it is not an independent external dataset.

## Final E50 Training Manifest

| Source branch | Rows | Provenance meaning |
|---|---:|---|
| `active_project_dataset` | 13,070 | Main active-project command data; collective-derived/project-local branch. |
| `dataset2_vcm_balanced` | 2,800 | Selected `VCM_BALANCED` training rows. |
| `e41_reconstructed_adaptation` | 230 | Separate Pi deployment adaptation/calibration branch. |
| Total | 16,100 | Final E50 command-model training manifest. |

Data-kind composition:

| Kind | Rows |
|---|---:|
| real | 15,260 |
| augmented | 480 |
| real multi-sensor | 200 |
| synthetic | 160 |

The manifest records each training example with source dataset, source partition, source path, source label, final VCM label, speaker/group identifier, data kind, SHA-256, dataset role, and resolved path. This makes the training set inspectable and reproducible as a row list.

## Label Mapping And Balancing

The source data did not perfectly match the final 19-label E50 vocabulary. Some labels mapped directly, such as `PLAY_MUSIC`, `WEATHER`, `TIME`, `LIGHT_ON`, `LIGHT_OFF`, `VOLUME_UP`, and `VOLUME_DOWN`. Others required controlled mapping, such as `SET_TIMER` to `TIMER`, `SET_ALARM` to `ALARM`, `MEDIA_NEXT` to `NEXT`, `MEDIA_PAUSE` to `PAUSE`, and `MEDIA_STOP` to `STOP`.

Most final labels have 900 rows. Five labels have 700 rows because Dataset2 did not provide usable direct support for them.

| Label group | Rows per label | Meaning |
|---|---:|---|
| 14 labels with Dataset2 support | 900 | 700 active/project rows plus up to 200 Dataset2 rows. |
| `BRIGHTNESS`, `CREATE_REMINDER`, `LIST_REMINDERS`, `CALL`, `MESSAGE` | 700 | Active/project data without direct Dataset2 support. |

This is controlled balancing with bounded auxiliary-data addition, not perfect uniform balancing.

## Audio Loading And Feature Processing

Each training row resolves to a short audio command clip. Training and inference use the same expected signal representation:

| Processing step | Value |
|---|---|
| Sample rate | 16 kHz |
| Target duration | 4.0 s |
| Approximate waveform samples | 64,000 |
| Amplitude normalization | peak normalization |
| Feature type | log-Mel |
| Frame length | 25 ms |
| Frame step | 10 ms |
| FFT length | 512 |
| Mel bins | 40 |
| Frequency range | 20 Hz to 7,600 Hz |
| Log floor | `1e-6` |
| Expected feature shape | `(398, 40)` |
| Model input shape | `(398, 40, 1)` |
| Feature normalization | training-manifest global mean/std |

A command waveform is therefore transformed into a compact time-frequency matrix. The CNN learns from local energy patterns in that matrix, not from text transcription.

## Training Configuration

| Field | Value |
|---|---|
| Experiment | `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT` |
| Architecture | E41 `tiny_vcm_cnn` |
| Initialization | mapped E41 initialization |
| Optimizer | Adam |
| Learning rate | 0.00075 |
| Batch size | 32 |
| Maximum epochs | 14 |
| Early stopping patience | 4 |
| Random seed | 5050 |
| Checkpoint selection | Best internal validation loss only; no current95 or Phase AV selection |

The reviewed evidence supports local Windows CPU-only TensorFlow training for the final E50 command model.

## Leakage Controls And Risks

The dataset documentation records speaker-separated train/validation/test splits for `VCM_MASTER`, train-only derivation for `VCM_BALANCED`, validation/test leakage checks, byte-level overlap checks, and protected-evidence exclusions. Remaining caveat: source-family overlap cannot be fully excluded where older metadata lacks upstream IDs.

## Separate E37 Wake-Recording Lineage

The recovered E37 `Hey Pi` wake recordings are separate from the E50 command manifest. That wake-stage manifest contains 99 Raspberry Pi recordings, including 50 `WAKE` / `hey pi`, with 64 adaptation-designated and 35 holdout-designated recordings at 4 s / 16 kHz / `plughw:2,0`. Those recordings are not part of the 16,100-row E50 command-model training manifest and are not classified as Gold Dataset rows.

## Limits

Dataset2 is 16-class while final E50 is 19-label. Dataset2 does not directly cover every final label. Synthetic/augmented data is training-domain support, not independent real-speaker deployment evidence. The 230 E41 rows are legitimate project-specific adaptation evidence but must remain separate from Gold Dataset claims. Blanket unrestricted redistribution rights are not established.
