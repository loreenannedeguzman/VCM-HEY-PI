# Dataset Inspection

This folder provides inspectable dataset and provenance evidence for the final E50 command model. It does not redistribute raw third-party audio.

## Included

- `E50_TRAINING_MANIFEST.csv`: final Phase BG E50 training manifest copied from the frozen project evidence. It contains 16,100 rows for `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT`.
- `DATASET_INVENTORY.md`: accepted package inventory summarizing dataset provenance and counts.

## Final E50 Manifest Summary

The final E50 training manifest is documented as:

- 16,100 total rows.
- 13,070 active-project rows.
- 2,800 `dataset2` / `VCM_BALANCED` rows.
- 230 `e41_reconstructed_adaptation` rows.

Data-kind composition:

- 15,260 real.
- 480 augmented.
- 200 real multi-sensor.
- 160 synthetic.

## Important Limits

The repository includes manifest/provenance evidence, not the full raw source audio corpus. Third-party dataset licenses and upstream terms remain applicable. The manifest supports inspection of the final E50 training evidence; it is not a claim that all upstream source datasets are freely redistributable through this repository.

## Related Documentation

- `../provenance/E50_DATASET.md`
- `../provenance/DATASET_INVENTORY.md`
- `../docs/02_FINAL_SYSTEM/06_DATASET_AND_TRAINING.md`
- `../docs/06_REPRODUCTION/03_TRAINING_REPRODUCIBILITY_LIMITS.md`
