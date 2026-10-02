# 06 - Dataset And Training

## Technical Provenance Position

E50 was developed using selected material from the class collective Gold Dataset rather than using the entire collective dataset unchanged. The project-specific dataset was prepared and balanced for the 19-command E50 vocabulary, with training-only augmentation and a separate Pi deployment-adaptation branch. E50 is not claimed to be byte-for-byte identical to the Gold Dataset, to contain the entire Gold Dataset, or to use identical Gold Dataset train/test rows. [REF-02] [REF-03]

## Dataset A: VCM_MASTER

`VCM_MASTER` is a project-local Dataset2 / collective-family representation derived from selected collective dataset material; it is not claimed to be the entire Gold Dataset. [REF-02]

| Property | Value |
|---|---:|
| Total samples | 36,622 |
| Classes | 16 |
| Train | 27,130 |
| Validation | 4,734 |
| Test | 4,758 |
| Speaker/group identities | 395 |
| Train/validation/test speaker overlap | 0 |

## Dataset B: VCM_BALANCED

`VCM_BALANCED` is a training-derived subset of VCM_MASTER and therefore inherits its collective-family provenance. It is not an independent external dataset. [REF-02]

| Property | Value |
|---|---:|
| Training rows/files | 15,268 |
| Classes | 16 |
| Original rows | 13,801 |
| Augmented rows | 1,467 |
| Speaker/group identities | 298 |
| Validation/test leakage | 0 documented source val/test leak rows |

Augmentation was applied to training-domain data and should not be treated as independent real-speaker evidence. [REF-02]

## Final E50 Training Manifest

| Source dataset | Rows | Provenance meaning |
|---|---:|---|
| `active_project_dataset` | 13,070 | Main active-project command data; collective-derived/project-local command-data branch. |
| `dataset2_vcm_balanced` | 2,800 | Selected VCM_BALANCED rows; collective-family training-derived branch. |
| `e41_reconstructed_adaptation` | 230 | Separately identified Pi deployment adaptation/calibration branch. |
| Total | 16,100 | Final E50 command-model training manifest. |

The first two components are collective-derived/project-local command-data branches. The 230 E41 rows are project-specific Pi deployment adaptation/calibration data and are not classified as Gold Dataset rows. [REF-02] [REF-03]

## Separate E37 Wake-Recording Lineage

E37 uses a separate project-specific Raspberry Pi wake-recording lineage. The recovered `wake_validation_hey_pi` manifest documents 99 wake-stage recordings, including 50 `WAKE` / `hey pi` recordings, 64 adaptation-designated rows, and 35 holdout-designated rows, all recorded as 4-second 16 kHz audio using `plughw:2,0`. This lineage is distinct from the collective Gold Dataset / Dataset2 lineage used as the provenance basis for the E50 command-model training material. The 99 E37 wake recordings are not part of the 16,100-row E50 command-model training manifest and are not classified as Gold Dataset rows. [REF-17]

The recovered E37 evidence does not independently establish the exact final E37 training subset, speaker/recordist count, training epochs, optimizer, validation metrics, augmentation count, or row-level mapping from the 99 recordings to the final E37 checkpoint. [REF-17]

## Balancing Rule

Most final labels have 900 rows. Five labels have 700 rows because Dataset2 did not provide usable direct support for them. This is controlled class balancing with bounded auxiliary-data addition, not perfect uniform balancing. [REF-02]

| Label group | Rows per label | Meaning |
|---|---:|---|
| 14 labels with Dataset2 support | 900 | 700 active/project rows plus up to 200 Dataset2 rows. |
| `BRIGHTNESS`, `CREATE_REMINDER`, `LIST_REMINDERS`, `CALL`, `MESSAGE` | 700 | Active/project data without direct Dataset2 support. |

## Training Configuration

The final Phase BG E50 model used mapped E41 initialization, Adam optimizer, learning rate `0.00075`, batch size `32`, maximum `14` epochs, and checkpoint selection by best internal validation loss only. It did not select the checkpoint using current95 or Phase AV evaluation evidence. [REF-11]

## Preprocessing

Training and inference use 16 kHz, 4.0-second audio and log-Mel features with 40 Mel bins and expected feature shape `(398, 40)`. [REF-11]

## Leakage Controls And Risks

The dataset documentation records train/validation/test speaker separation, Dataset B derivation from training material, validation/test leakage checks, byte-level overlap checks, and protected-evidence exclusions. It also preserves caveats: source-family overlap cannot be fully excluded where older metadata lacks upstream IDs. [REF-02]

## Limitations

- Dataset2 is 16-class while final E50 is 19-label. [REF-02]
- Dataset2 does not directly cover all final E50 labels. [REF-02]
- `LIGHT_DIM` / `BRIGHTNESS` semantics are evidence-supported but imperfect. [REF-02]
- Synthetic speech is training-domain support, not independent real-speaker deployment evidence. [REF-02]
- E41 adaptation rows are legitimate project-specific deployment data but must remain provenance-separated from Gold Dataset claims. [REF-02]

