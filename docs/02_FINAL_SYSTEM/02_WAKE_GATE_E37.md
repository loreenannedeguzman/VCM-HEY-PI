# 02 - Wake Gate E37

## Identity

The frozen wake model is `E37_TARGETED_COLOR_VOLUME_FIX`. The deployed wake threshold is `0.90`. The final SHA manifest records the E37 weights SHA-256 as `687E82E2CEFA6D74CEF2C0A15D28F8F6142D47D4A67E57C68C091E83FC2CEBDE` and the E37 normalization SHA-256 as `3BFA93F202DC0C241E577E5B89506F2CB6D0F35B8239297C215A7F81E970B4C7`. [REF-04] [REF-05] [REF-13]

## Role

E37 is a wake gate, not a command recognizer. Its job is to decide whether the user said the wake phrase `Hey Pi`. If E37 accepts the wake phrase, the command window opens. If not, the runtime remains in wake/listening mode and no command action should be routed. [REF-04] [REF-17]

```text
Microphone audio
  -> E37 wake detector
  -> accepted WAKE?
       yes: capture command
       no: remain in wake/listening mode
```

## Relationship To E50

E37 runs before E50. E50 command recognition occurs only after accepted wake detection in the normal wake-gated runtime. The E50 command-training manifest should not be reused as if it were the E37 wake-training manifest. [REF-04]

## Recovered Hey Pi Recording Evidence

The original project-specific wake-recording evidence has now been recovered and documented in a read-only audit. The recovered Raspberry Pi manifest is: [REF-17]

```text
/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi/manifest.csv
```

The corresponding recording directory is:

```text
/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi
```

The recovered manifest documents 99 project-specific wake-stage recordings:

| Label / group | Count |
|---|---:|
| `WAKE` / `hey pi` | 50 |
| `UNKNOWN` false-wake phrases | 15 |
| `COLOR` targeted examples | 14 |
| `VOLUME_UP` targeted examples | 14 |
| `LIGHT_ON` command-as-wake-probe examples | 3 |
| `PLAY_MUSIC` command-as-wake-probe examples | 3 |
| Total | 99 |

The manifest split designation is:

| Split designation | Count |
|---|---:|
| `adaptation` | 64 |
| `holdout` | 35 |
| Total | 99 |

All 99 manifest rows record 4-second audio at 16 kHz using ALSA input device `plughw:2,0`. [REF-17]

## What This Proves

The recovered evidence directly establishes that the project-specific `Hey Pi` recording set existed, that it was recorded through the Raspberry Pi microphone path documented in the manifest, and that the manifest has identifiable labels, phrases, split designations, WAV paths, duration, sample rate, and device fields. It also strongly corroborates the targeted color/volume context behind the `E37_TARGETED_COLOR_VOLUME_FIX` wake model name. [REF-17]

## Training Evidence Boundary

The recovered evidence establishes the existence and composition of the E37-related `Hey Pi` recording set, but it does not independently establish which exact rows were included in the final E37 training run. The manifest uses `adaptation` and `holdout` designations; those designations should not be restated as a proven final E37 training subset without a dedicated E37 training manifest or training log. [REF-17]

Not established by the recovered evidence: exact speaker/recordist count, dedicated E37 training manifest, exact final E37 training subset, E37 training epochs, optimizer, E37 validation metrics, E37 augmentation count, or exact row-level mapping from the 99 recordings to the final E37 checkpoint. These values should not be invented. [REF-17]

## Provenance Boundary

The E37 wake-recording lineage is separate from the collective Gold Dataset lineage used for the E50 command model. The 99 recovered E37 wake recordings are project-specific Raspberry Pi wake-stage recordings and are not classified as Gold Dataset rows. [REF-02] [REF-17]

## Deployment Placement

The Raspberry Pi deployment package uses E37 before the E50 command CNN in the final wake-gated runtime. The GUI starts the wake-wait runtime; the GUI does not replace E37. [REF-05] [REF-06] [REF-15]

## Limitation

The wake-stage documentation is intentionally narrower than the E50 command-model dataset documentation. The recovered evidence now supports a numerical report of the 99-recording `wake_validation_hey_pi` manifest, but not a complete reconstruction of the final E37 training run. [REF-17]
