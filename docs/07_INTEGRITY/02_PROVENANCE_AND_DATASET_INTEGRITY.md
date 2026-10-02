# Provenance and Dataset Integrity

## E50 Command Dataset

The final E50 training manifest contains 16,100 rows:

| Source branch | Rows |
|---|---:|
| active_project_dataset | 13,070 |
| dataset2_vcm_balanced | 2,800 |
| e41_reconstructed_adaptation | 230 |
| Total | 16,100 |

The first two branches represent collective-derived/project-local command-data lineage. The 230 E41 rows are separately identified Pi deployment adaptation/calibration data and are not classified as Gold Dataset rows unless additional evidence establishes that link.

## Balancing and Augmentation

The final construction uses controlled class balancing with bounded auxiliary-data addition. Fourteen classes are represented at 900 rows, and five classes are represented at 700 rows. The final set includes 15,260 real rows, 200 real_multi_sensor rows, 160 synthetic rows, and 480 augmented rows.

## E37 Wake Recording Lineage

E37 has a separate project-specific Raspberry Pi wake-recording lineage. The recovered manifest documents 99 recordings in `/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi/manifest.csv`, including 50 WAKE / hey pi recordings, 64 adaptation-designated recordings, and 35 holdout-designated recordings.

This establishes the recording set's existence and composition. It does not establish the exact final E37 training subset or full training configuration.
