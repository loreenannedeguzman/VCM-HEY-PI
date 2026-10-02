# Training Reproducibility Limits

## E50 Command Model

The E50 command-model dataset composition is documented as 16,100 rows: 13,070 active-project rows, 2,800 selected VCM_BALANCED rows, and 230 separately identified E41 Pi adaptation rows. The provenance-adjusted documentation explains that this is a selected project-specific command dataset with collective-family lineage, not a full unchanged copy of the collective Gold Dataset.

## E37 Wake Model

Recovered evidence establishes the project-specific Hey Pi recording set:

| Category | Count |
|---|---:|
| Total recordings | 99 |
| WAKE / hey pi | 50 |
| UNKNOWN | 15 |
| COLOR | 14 |
| VOLUME_UP | 14 |
| LIGHT_ON | 3 |
| PLAY_MUSIC | 3 |
| Adaptation-designated | 64 |
| Holdout-designated | 35 |

The recordings are 4 seconds at 16 kHz using input device `plughw:2,0`.

The recovered evidence does not independently establish the exact final E37 training subset, final E37 training manifest, epochs, optimizer, validation metrics, augmentation count, speaker/recordist count, or complete row-to-checkpoint mapping.
