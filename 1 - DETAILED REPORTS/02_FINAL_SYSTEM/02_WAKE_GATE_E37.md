# Wake Gate E37

## Engineering Question

How does the system know when to begin command recognition?

E37 is the wake-gate model. It runs before E50 and decides whether the user said the wake phrase `Hey Pi`. E37 is not the command classifier, not the action router, and not the GUI. Its accepted output opens the post-wake command capture window; its rejected output leaves the runtime in wake/listening behavior with no command action routed.

```text
Microphone audio
  -> E37 wake detector
  -> accepted wake?
       yes: capture command window for E50
       no: remain in wake/listening mode
```

## Frozen Identity

| Field | Value |
|---|---|
| Wake model | `E37_TARGETED_COLOR_VOLUME_FIX` |
| Deployed wake threshold | 0.90 |
| E37 weights SHA-256 | `687E82E2CEFA6D74CEF2C0A15D28F8F6142D47D4A67E57C68C091E83FC2CEBDE` |
| E37 normalization SHA-256 | `3BFA93F202DC0C241E577E5B89506F2CB6D0F35B8239297C215A7F81E970B4C7` |
| Runtime placement | Before E50 command classification |

## Recovered Hey Pi Recording Evidence

Recovered Raspberry Pi evidence documents a project-specific wake-stage recording resource:

```text
/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi
/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi/manifest.csv
```

The manifest contains 99 wake-stage recordings:

| Manifest group | Count | Meaning |
|---|---:|---|
| `WAKE` / `hey pi` | 50 | Positive wake phrase recordings. |
| `UNKNOWN` | 15 | False-wake / non-command phrases. |
| `COLOR` | 14 | Targeted examples related to color confusion context. |
| `VOLUME_UP` | 14 | Targeted examples related to volume confusion context. |
| `LIGHT_ON` | 3 | Command-as-wake-probe examples. |
| `PLAY_MUSIC` | 3 | Command-as-wake-probe examples. |
| Total | 99 | Complete recovered manifest row count. |

The manifest designations are:

| Split designation | Count |
|---|---:|
| `adaptation` | 64 |
| `holdout` | 35 |
| Total | 99 |

All 99 rows record 4-second audio at 16 kHz using ALSA input device `plughw:2,0`.

## What This Evidence Establishes

The recovered evidence establishes that the project-specific `Hey Pi` wake-recording set actually existed, was captured through the Raspberry Pi microphone path, and had a structured manifest with labels, phrases, split designations, WAV paths, duration, sample rate, and device information. It also supports the engineering meaning of the `E37_TARGETED_COLOR_VOLUME_FIX` name: the wake work included targeted non-wake/color/volume examples, not only positive `Hey Pi` clips.

## What This Evidence Does Not Establish

The recovered manifest does not independently prove the exact final E37 training-row membership. It also does not establish the final E37 training manifest, exact subset used for the final checkpoint, epochs, optimizer, validation metrics, augmentation count, complete speaker/recordist count, or row-level mapping from the 99 recordings to the deployed E37 weights. The `adaptation` and `holdout` designations should therefore be reported as manifest designations, not as a proven final training/test split for the deployed checkpoint.

## Relationship To E50

E37 and E50 use different evidence lineages. E37 is the wake gate and uses project-specific `Hey Pi` wake-stage evidence. E50 is the 19-label command classifier and uses the 16,100-row command-model training manifest. The 99 E37 wake recordings are not part of the E50 command-model training manifest and should not be described as collective Gold Dataset rows.

## Deployment Placement

In the Raspberry Pi runtime, E37 runs before E50. The GUI starts the wake-wait runtime, but it does not replace E37. If E37 rejects wake, E50 command recognition should not route an action. If E37 accepts wake, the command-capture and E50 path begins.
