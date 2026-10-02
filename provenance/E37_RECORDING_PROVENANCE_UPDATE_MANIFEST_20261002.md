# E37 Recording Provenance Update Manifest

Date: 2026-10-02

## Scope

E37 `Hey Pi` recording provenance update for the technical submission documentation.

## Evidence Source

Primary evidence source:

`E37_HEY_PI_DATASET_EVIDENCE_RECOVERY_AUDIT_20261002.md`

Established recovered evidence:

- Raspberry Pi recording directory: `/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi`
- Recording manifest: `/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi/manifest.csv`
- Total wake-stage recordings: 99
- `WAKE` / `hey pi` recordings: 50
- `UNKNOWN`: 15
- `COLOR`: 14
- `VOLUME_UP`: 14
- `LIGHT_ON`: 3
- `PLAY_MUSIC`: 3
- Adaptation-designated rows: 64
- Holdout-designated rows: 35
- Recording duration: 4 seconds
- Sample rate: 16 kHz
- Input device: `plughw:2,0`

## Files Modified

| File | Change made |
|---|---|
| `02_FINAL_SYSTEM/00_FINAL_SYSTEM_OVERVIEW.md` | Added recovered E37 `Hey Pi` manifest summary and cited the recovered audit. |
| `02_FINAL_SYSTEM/01_SYSTEM_ARCHITECTURE.md` | Added wake-stage provenance note and clarified that recording evidence does not prove exact final training-row membership. |
| `02_FINAL_SYSTEM/02_FINAL_SYSTEM_BUILD_MANIFEST_20261002.md` | Updated evidence-gap language to distinguish established recording counts from unestablished final E37 training details. |
| `02_FINAL_SYSTEM/02_WAKE_GATE_E37.md` | Added principal recovered E37 recording evidence section with Pi path, manifest path, counts, split designations, audio properties, provenance boundary, and retained training-lineage limitations. |
| `02_FINAL_SYSTEM/06_DATASET_AND_TRAINING.md` | Added separate E37 wake-recording lineage section and separated it from the collective Gold Dataset / E50 command-model lineage. |
| `02_FINAL_SYSTEM/07_PI_DEPLOYMENT.md` | Added deployment-context note that the recovered E37 manifest used input device `plughw:2,0` and is separate from final benchmark evidence. |
| `02_FINAL_SYSTEM/09_FROZEN_SYSTEM_IDENTITY.md` | Added recovered E37 recording evidence section while preserving frozen artifact hashes and freeze boundary. |
| `02_FINAL_SYSTEM/reference/REFERENCE_GUIDE.md` | Added `REF-17` for the E37 recovery audit. |
| `02_FINAL_SYSTEM/reference/REF-01_E50_DEMODAY_REPORT_PROVENANCE_ADJUSTED.md` | Synced package reference summary with recovered E37 provenance note and Gold Dataset separation. |
| `02_FINAL_SYSTEM/reference/REF-02_E50_DATASET_PROVENANCE_ADJUSTED.md` | Added E37 wake-recording boundary note. |
| `02_FINAL_SYSTEM/reference/REF-03_FINAL_PACKAGE_README_PROVENANCE_ADJUSTED.md` | Synced package reference README summary with recovered E37 provenance note and Gold Dataset separation. |
| `02_FINAL_SYSTEM/reference/REF-04_E50_WAKE_GATE.md` | Added submission update note explaining that later recovered evidence establishes recording counts while final E37 training details remain unestablished. |
| `data/metadata/DATASET_INVENTORY.md` | Added separate E37 wake-recording clarification under current findings. |
| `E50 DEMODAY REPORT.md` | Added recovered E37 provenance note and separated E37 recordings from E50 command-model training manifest. |
| `E50_DATASET.md` | Added E37 wake-recording note and separated it from the 16,100-row E50 command-model manifest. |
| `E50_FINAL_PROJECT_REPORT_REGENERATED_20261002.tex` | Added a recovered E37 wake-recording provenance subsection without changing benchmark metrics. |
| `FINAL GITHUB README ORIGINAL.md` | Added recovered E37 provenance note and Gold Dataset separation. |
| `github_package/ME2_VCM_E50_GITHUB_PACKAGE_20260930/README.md` | Added recovered E37 provenance note and Gold Dataset separation. |
| `PROVENANCE_DOCUMENTATION_INTEGRATION_MANIFEST_20261002.md` | Added an E37 provenance addendum documenting the later recovered evidence. |
| `E37_RECORDING_PROVENANCE_UPDATE_MANIFEST_20261002.md` | Created this update manifest. |

## Relevant Files Inspected But Not Modified

| File | Reason unchanged |
|---|---|
| `02_FINAL_SYSTEM/03_COMMAND_MODEL_E50.md` | Command-model identity document did not need E37 recording-count detail. |
| `02_FINAL_SYSTEM/04_CONFIDENCE_POLICY_E40.md` | E40 policy document already preserved separation from E37 and did not need provenance changes. |
| `02_FINAL_SYSTEM/05_FINAL_VOCABULARY_AND_ACTIONS.md` | Vocabulary/action mapping does not describe E37 recording provenance. |
| `02_FINAL_SYSTEM/08_POST_FREEZE_DUi.md` | GUI boundary language remained accurate and did not need recording-provenance details. |
| `E37_HEY_PI_DATASET_EVIDENCE_RECOVERY_AUDIT_20261002.md` | Source-of-truth audit retained unchanged. |
| `02_FINAL_SYSTEM/reference/REF-05_README_PI_DEPLOYMENT.md` | Historical deployment reference retained as evidence copy. |
| `02_FINAL_SYSTEM/reference/REF-06_PACKAGE_MANIFEST.md` | Historical package manifest reference retained as evidence copy. |
| `02_FINAL_SYSTEM/reference/REF-13_E50_FINAL_SHA256_MANIFEST_20260930.txt` | Hash manifest retained unchanged. |
| `02_FINAL_SYSTEM/reference/REF-14_E50_BENCHMARK_AUDIT.md` | Benchmark audit retained unchanged; benchmark metrics were not altered. |
| `02_FINAL_SYSTEM/reference/REF-16_ACTION_LAYER_DESIGN.md` | Action-layer design document does not describe E37 recording provenance. |

## Changes Made

The documentation now states that the project-specific `Hey Pi` wake recordings were recovered and documented. It records the manifest path, the 99-row count, label counts, split designations, and recording properties. It also explicitly separates this E37 wake-recording lineage from the collective Gold Dataset / Dataset2 command-model lineage.

The documentation continues to avoid unsupported claims that:

- E37 was trained on all 50 `Hey Pi` recordings.
- E37 was trained on all 64 adaptation-designated recordings.
- The 99 E37 recordings are Gold Dataset rows.
- The 99 E37 recordings are part of the 16,100-row E50 command-model training manifest.
- The final E37 training run has been fully reconstructed.

## Technical Files Changed

| Item | Result |
|---|---|
| ME2_VCM source files modified | 0 |
| E50 model modified | 0 |
| E37 model modified | 0 |
| E40 policy modified | 0 |
| Dataset modified | 0 |
| Pi files modified | 0 |
| Runtime modified | 0 |
| Benchmark rerun | 0 |
| Training rerun | 0 |
| Git operations | 0 |

## Evidence Limitations Retained

- Exact final E37 training subset not established.
- Dedicated E37 training manifest not recovered.
- E37 training epochs not established.
- E37 optimizer not established.
- E37 validation metrics not established.
- E37 augmentation count not established.
- Speaker/recordist count not established.
- Exact row-level mapping from the 99 recovered recordings to the final E37 checkpoint not established.

## Integrity Statement

This was a documentation-only update inside `C:\Users\Loreen Anne\Documents\New project\FINAL SUBMISSION VCM`. No files inside `C:\Users\Loreen Anne\Documents\New project\ME2_VCM` were modified. The Raspberry Pi was not accessed or modified during this update. E53 was not accessed or modified. No training, runtime execution, benchmark execution, inference, Git operation, or audio copying was performed.

