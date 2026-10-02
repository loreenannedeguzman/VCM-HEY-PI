# E37 "Hey Pi" Dataset Evidence Recovery Audit

Date: 2026-10-02

Scope: read-only evidence recovery for the E37 wake-gate dataset and model evidence associated with the project-specific wake phrase `Hey Pi`.

## 1. Purpose

This audit was performed to recover and document existing evidence for the E37 wake-gate recording and training provenance. The specific objective was to determine whether the Raspberry Pi contained authoritative evidence for the original/project-specific `Hey Pi` wake recordings, recording counts, split counts, audio properties, recording manifest, deployed E37 model identity, and any E37 training or checkpoint evidence.

This was an evidence recovery task only. No E50 code, E53 code, datasets, models, weights, thresholds, runtime configuration, Raspberry Pi deployment files, recordings, manifests, benchmark evidence, or project documentation were modified.

## 2. Evidence Sources

### Frozen ME2_VCM documents consulted

- `C:\Users\Loreen Anne\Documents\New project\ME2_VCM\E50_WAKE_GATE.md`
- `C:\Users\Loreen Anne\Documents\New project\FINAL SUBMISSION VCM\02_FINAL_SYSTEM\02_WAKE_GATE_E37.md`

These documents established the prior documented state: E37 was the frozen wake gate, the wake phrase was `Hey Pi`, the wake threshold was `0.90`, and E37 was separate from the E50 command model. They also stated that exact E37 training-row counts and full E37 training details were not previously established in the reviewed project evidence.

### Raspberry Pi paths inspected through user-provided terminal output

- `/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi`
- `/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi/manifest.csv`
- `/home/loreenanne/vcm_pi_package/scripts/record_pi_wake_set.py`
- `/home/loreenanne/vcm_pi_package/models/cnn/E37_TARGETED_COLOR_VOLUME_FIX_weights.npz`
- `/home/loreenanne/vcm_pi_package/models/cnn/E37_TARGETED_COLOR_VOLUME_FIX_normalization.npz`
- `/home/loreenanne/vcm_pi_package` search results for E37, wake, training, metrics, summary, manifest, and result candidates

The Pi was inspected only through read-only commands pasted and executed by the user in an existing SSH session.

### Exact evidence files found

- Wake recording manifest: `/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi/manifest.csv`
- Wake recording script: `/home/loreenanne/vcm_pi_package/scripts/record_pi_wake_set.py`
- E37 deployed weights: `/home/loreenanne/vcm_pi_package/models/cnn/E37_TARGETED_COLOR_VOLUME_FIX_weights.npz`
- E37 deployed normalization: `/home/loreenanne/vcm_pi_package/models/cnn/E37_TARGETED_COLOR_VOLUME_FIX_normalization.npz`
- E37-related evidence archive candidate: `/home/loreenanne/vcm_pi_package/e50_bk_targeted_weak_command_repeats_e37_e50_20260928_evidence.tar.gz`
- Runtime result evidence candidates under `/home/loreenanne/vcm_pi_package/pi_validation/...`, including E37/E50 wake-gated validation result JSON files

The search did not surface a dedicated E37 training log, training configuration report, epoch log, or metrics summary file in the pasted candidate list.

## 3. "Hey Pi" Origin

The recovered Pi evidence directly establishes that `hey pi` was the wake phrase recorded for the WAKE class in the Pi wake-validation dataset.

The manifest contains rows such as:

```text
label=WAKE
expected_intent=WAKE
phrase=hey pi
action_hint=open_command_window
wav_path=pi_validation/wake_validation_hey_pi/WAKE/wake_hey_pi_001.wav
duration_sec=4
sample_rate=16000
device=plughw:2,0
```

The recording script also explicitly defines:

```text
WakeExample("WAKE", "hey pi", "open_command_window")
```

and records through ALSA `arecord` using a default device of `plughw:2,0`, 16 kHz sample rate, mono channel, S16_LE format, and 4-second duration.

Therefore, the project-specific `Hey Pi` wake phrase and Raspberry Pi microphone recording process are directly established by the recovered manifest and recording script.

## 4. Recording Evidence

### Recording directory

```text
/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi
```

### Manifest

```text
/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi/manifest.csv
```

Manifest size from the Pi tree output:

```text
18854 bytes
```

Manifest timestamp from the Pi tree output:

```text
2026-09-23 14:37:53
```

### Manifest columns

The recovered manifest columns are:

```text
recorded_at_utc,label,expected_intent,phrase,action_hint,trial,split,wav_path,duration_sec,sample_rate,device
```

### Total rows

The recovered manifest contains:

```text
99 rows
```

### Label counts

| Label | Rows |
|---|---:|
| WAKE | 50 |
| UNKNOWN | 15 |
| COLOR | 14 |
| VOLUME_UP | 14 |
| LIGHT_ON | 3 |
| PLAY_MUSIC | 3 |
| Total | 99 |

### Phrase counts

| Phrase | Rows |
|---|---:|
| hey pi | 50 |
| alexa | 3 |
| hey google | 3 |
| hey siri | 3 |
| hello | 3 |
| what is your favorite color | 3 |
| lights on | 3 |
| play music | 3 |
| color red | 6 |
| change color | 4 |
| set color | 4 |
| volume up | 6 |
| turn volume up | 4 |
| louder | 4 |

### Split counts

| Split | Rows |
|---|---:|
| adaptation | 64 |
| holdout | 35 |
| Total | 99 |

### Label-by-split counts

| Label | Adaptation | Holdout | Total |
|---|---:|---:|---:|
| WAKE | 30 | 20 | 50 |
| UNKNOWN | 10 | 5 | 15 |
| COLOR | 10 | 4 | 14 |
| VOLUME_UP | 10 | 4 | 14 |
| LIGHT_ON | 2 | 1 | 3 |
| PLAY_MUSIC | 2 | 1 | 3 |
| Total | 64 | 35 | 99 |

### Audio properties

All 99 manifest rows record:

| Property | Value | Rows |
|---|---|---:|
| duration_sec | 4 | 99 |
| sample_rate | 16000 | 99 |
| device | plughw:2,0 | 99 |

The Pi file tree showed the listed WAV files as `128044 bytes`, consistent with short 4-second mono 16 kHz PCM WAV recordings as configured by the recording script.

### Recording file examples

Examples recovered from the Pi tree include:

```text
/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi/WAKE/wake_hey_pi_001.wav
/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi/WAKE/wake_hey_pi_050.wav
/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi/UNKNOWN/unknown_hey_siri_001.wav
/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi/LIGHT_ON/light_on_lights_on_001.wav
/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi/PLAY_MUSIC/play_music_play_music_001.wav
/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi/COLOR/targeted_color_color_red_001.wav
/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi/VOLUME_UP/targeted_volume_up_volume_up_001.wav
```

No audio files were copied to the laptop during this audit.

## 5. E37 Training Evidence

### Directly established

The recovered manifest directly establishes a wake/adaptation/holdout recording set with 99 total rows:

- 50 positive `WAKE` / `hey pi` examples
- 49 non-wake / command-as-wake-probe / targeted negative examples
- 64 rows marked `adaptation`
- 35 rows marked `holdout`
- 4-second recordings
- 16 kHz sample rate
- ALSA device `plughw:2,0`

The recording script directly establishes the intended recording process, manifest schema, default device, duration, sample rate, and expected behavior labels.

### Strongly corroborated

The final deployed wake model is named `E37_TARGETED_COLOR_VOLUME_FIX`. The recovered recording manifest contains targeted `COLOR` and `VOLUME_UP` examples in addition to original `WAKE`, `UNKNOWN`, `LIGHT_ON`, and `PLAY_MUSIC` examples. The E37 deployed model artifacts have Pi modification timestamps after the recovered manifest timestamp, and the E37 name matches the targeted color/volume-fix recording context.

This strongly corroborates that the recovered `wake_validation_hey_pi` material is relevant to the E37 targeted wake-gate recovery path. However, the pasted Pi evidence did not include a dedicated E37 training log that proves row-by-row use of every manifest row in the final checkpoint.

### Not established in recovered evidence

The following were not directly established by the recovered Pi evidence:

- exact E37 training epoch count
- optimizer
- learning rate
- batch size
- validation metrics
- model-selection metric
- full E37 training configuration
- full row-level training manifest separate from the recording manifest
- speaker or recordist count
- augmentation count
- whether every adaptation row was used directly in training
- whether every holdout row was used only as holdout/evaluation
- formal train/validation/test split beyond the manifest's `adaptation` and `holdout` fields

The manifest is authoritative for recorded data and recorded split labels. It does not by itself prove every row's final training use unless supported by a training log or training manifest.

## 6. E37 Model Identity

The deployed E37 model artifacts recovered from the Pi are:

| Artifact | Path | Size | Pi timestamp | SHA256 |
|---|---|---:|---|---|
| E37 weights | `/home/loreenanne/vcm_pi_package/models/cnn/E37_TARGETED_COLOR_VOLUME_FIX_weights.npz` | 252214 bytes | 2026-09-23 15:41 | `687e82e2cefa6d74cef2c0a15d28f8f6142d47d4a67e57c68c091e83fc2cebde` |
| E37 normalization | `/home/loreenanne/vcm_pi_package/models/cnn/E37_TARGETED_COLOR_VOLUME_FIX_normalization.npz` | 727 bytes | 2026-09-23 15:41 | `3bfa93f202dc0c241e577e5b89506f2cb6d0f35b8239297c215a7f81e970b4c7` |

The frozen E50 documentation records the same model identity and matching SHA-256 values, with uppercase formatting in some documents. SHA-256 comparison is case-insensitive.

The deployed wake threshold documented in the frozen project evidence is:

```text
0.90
```

## 7. Provenance Classification

| Evidence item | Classification | Reason |
|---|---|---|
| `Hey Pi` as E37 wake phrase | LEVEL 1 - DIRECTLY ESTABLISHED | Manifest rows and recording script explicitly state `hey pi` for label `WAKE`. |
| Pi recording manifest existence | LEVEL 1 - DIRECTLY ESTABLISHED | Manifest path and row summary were recovered from the Pi. |
| 99-row recording set | LEVEL 1 - DIRECTLY ESTABLISHED | Manifest summary reports 99 rows. |
| 50 `WAKE` / `hey pi` recordings | LEVEL 1 - DIRECTLY ESTABLISHED | Manifest label and phrase counts report 50 `WAKE` and 50 `hey pi`. |
| 64 adaptation and 35 holdout rows | LEVEL 1 - DIRECTLY ESTABLISHED | Manifest split counts report these exact values. |
| Recording duration/sample rate/device | LEVEL 1 - DIRECTLY ESTABLISHED | Manifest reports 4 seconds, 16000 Hz, and `plughw:2,0` for all 99 rows. |
| E37 deployed weights and normalization hashes | LEVEL 1 - DIRECTLY ESTABLISHED | Pi `sha256sum` output and local documentation agree. |
| Relevance of targeted COLOR/VOLUME_UP recordings to E37 targeted fix | LEVEL 2 - STRONGLY CORROBORATED | Manifest includes targeted color/volume rows; deployed model name is `E37_TARGETED_COLOR_VOLUME_FIX`; timestamps align. |
| Exact use of every manifest row in E37 final training | LEVEL 3 - PLAUSIBLE BUT NOT PROVEN | The manifest records adaptation/holdout rows, but a row-level E37 training manifest/log was not recovered. |
| E37 speaker/recordist count | LEVEL 4 - NOT ESTABLISHED | Manifest has no speaker/recordist field and no other speaker metadata was recovered. |
| E37 training epochs/optimizer/metrics | LEVEL 4 - NOT ESTABLISHED | No dedicated E37 training log or config was recovered in the candidate search. |

## 8. Comparison With Existing E50 Documentation

| Existing statement | Recovered evidence | Status |
|---|---|---|
| E37 is the frozen wake model `E37_TARGETED_COLOR_VOLUME_FIX`. | Pi model artifacts use `E37_TARGETED_COLOR_VOLUME_FIX` and hashes match frozen docs. | CONFIRMED |
| Wake phrase is `Hey Pi`. | Manifest and script explicitly record `hey pi` for the WAKE class. | CONFIRMED / STRENGTHENED |
| Wake threshold is `0.90`. | Frozen documentation records 0.90. Pi recovery did not contradict this. | CONFIRMED FROM PROJECT DOCS |
| E37 is separate from E50 command recognition. | Frozen docs establish this; Pi paths separate wake validation and E37 model artifacts. | CONFIRMED |
| Wake recording script records 4-second mono 16 kHz audio with `arecord`. | Script shows `arecord -r 16000 -c 1 -f S16_LE -d 4`; manifest records 4 seconds and 16000 Hz for all rows. | CONFIRMED / STRENGTHENED |
| Recording manifest contains label, phrase, trial, split, WAV path, duration, sample rate, and device. | Manifest columns exactly include these fields, plus `recorded_at_utc`, `expected_intent`, and `action_hint`. | CONFIRMED / STRENGTHENED |
| Prior documentation should not invent exact E37 row counts. | Pi manifest now establishes recording counts, but not full training-use counts. | QUALIFIED: recording counts can now be stated; training-use counts remain limited. |
| Prior document says WAKE final 9 trials are assigned to holdout. | Recovered actual manifest shows `WAKE` split counts of 30 adaptation and 20 holdout. | CONTRADICTION / QUALIFICATION: use the manifest as source of truth for actual recovered rows. |
| Full E37 training row count, speaker count, augmentation count, training epochs were not established. | Candidate search did not recover a dedicated E37 training log/config/metrics file. | STILL NOT ESTABLISHED |

## 9. Recommended Documentation Wording

The following wording can be used later in `02_FINAL_SYSTEM\02_WAKE_GATE_E37.md` or related documentation. This audit does not modify that document.

> The recovered Raspberry Pi wake-recording evidence contains a manifest at `/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi/manifest.csv`. The manifest documents 99 project-specific wake-stage recordings made for the E37 wake-gate work: 50 `WAKE` examples using the phrase `hey pi`, 15 `UNKNOWN` false-wake examples, 3 `LIGHT_ON` command-as-wake-probe examples, 3 `PLAY_MUSIC` command-as-wake-probe examples, 14 targeted `COLOR` examples, and 14 targeted `VOLUME_UP` examples. The manifest records 64 rows marked `adaptation` and 35 rows marked `holdout`. All rows are 4-second, 16 kHz recordings using ALSA device `plughw:2,0`. This establishes the project-specific `Hey Pi` recording provenance and recording split metadata. The recovered evidence strongly corroborates the relationship between these targeted recordings and `E37_TARGETED_COLOR_VOLUME_FIX`, but a dedicated E37 training log with epochs, optimizer settings, validation metrics, and row-level training-use mapping was not recovered, so those details remain unestablished.

## 10. Remaining Unknowns

The following remain not established in the recovered E37 evidence:

- exact speaker/recordist count
- whether multiple speakers contributed to the E37 recording set
- exact E37 training epochs
- optimizer and learning rate
- batch size
- augmentation count or augmentation policy
- row-level mapping from `manifest.csv` to final E37 checkpoint training input
- validation metrics for E37 checkpoint selection
- full E37 train/validation/test split beyond manifest `adaptation` and `holdout` labels
- whether the evidence archive `/home/loreenanne/vcm_pi_package/e50_bk_targeted_weak_command_repeats_e37_e50_20260928_evidence.tar.gz` contains additional E37 training details; it was identified as a candidate but not extracted or modified during this audit

## 11. Integrity Statement

- ME2_VCM modified: NO
- Pi modified: NO
- datasets modified: NO
- recordings modified: NO
- manifests modified: NO
- models modified: NO
- weights modified: NO
- thresholds modified: NO
- runtime executed: NO
- E37 inference executed: NO
- training executed: NO
- benchmark executed: NO
- Git modified: NO
- audio copied to laptop: NO
- Pi files copied into ME2_VCM: NO

This audit created only this Markdown report in `C:\Users\Loreen Anne\Documents\New project\FINAL SUBMISSION VCM`. The frozen E50 working project and Raspberry Pi deployment were treated as read-only evidence sources.
