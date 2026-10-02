# 09 - Frozen System Identity

## Final Frozen Core

| Field | Value | Evidence |
|---|---|---|
| Final command model | `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT` | [REF-01] [REF-11] |
| E50 weights SHA-256 | `BC8AC64CED4305DDF43BF4DE377F3CC636A764EFF339CD9F92AF06340C50B8FF` | [REF-03] [REF-13] |
| E50 normalization SHA-256 | `2D71873B6326D6552D7C5B1C22995FFD5132C357AAEC237CB85CBD7EF739283F` | [REF-13] |
| Wake model | `E37_TARGETED_COLOR_VOLUME_FIX` | [REF-04] [REF-05] |
| E37 weights SHA-256 | `687E82E2CEFA6D74CEF2C0A15D28F8F6142D47D4A67E57C68C091E83FC2CEBDE` | [REF-13] |
| E37 normalization SHA-256 | `3BFA93F202DC0C241E577E5B89506F2CB6D0F35B8239297C215A7F81E970B4C7` | [REF-13] |
| E40 policy | `E40_NON_LED_COMMAND_GUARDRAIL_THRESHOLDS` | [REF-01] [REF-07] |
| E40 deployed config | `configs/e50_revised_vocab_e40_thresholds.json` | [REF-07] |
| E40 config SHA-256 | `A0B2495328FD5A1E0E5885E727623BA6D9F823BE94CCCDFD0AEAD77254BBB3FD` | [REF-13] |
| Wake threshold | `0.90` | [REF-04] [REF-05] |
| Command default threshold | `0.90` | [REF-07] |
| Runner / GUI launcher | `scripts/run_vcm_touchscreen_gui.sh` launching `scripts/vcm_touchscreen_gui.py` | [REF-05] [REF-15] |
| Wake-command runtime | `scripts/pi_wake_voice_control_demo.py` | [REF-06] |
| GPIO status | Off unless explicitly enabled | [REF-05] |
| Response audio | Local WAV response map enabled | [REF-10] |

## Recovered E37 Recording Evidence

The deployed E37 identity above is now accompanied by recovered project-specific wake-recording evidence. The read-only E37 recovery audit documents `/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi/manifest.csv`, with 99 total wake-stage recordings: 50 `WAKE` / `hey pi`, 15 `UNKNOWN`, 14 `COLOR`, 14 `VOLUME_UP`, 3 `LIGHT_ON`, and 3 `PLAY_MUSIC`. The same manifest records 64 adaptation-designated rows, 35 holdout-designated rows, 4-second duration, 16 kHz sample rate, and input device `plughw:2,0`. [REF-17]

This recording evidence strengthens the E37 provenance record but does not modify the frozen E37 artifacts or establish exact final E37 training-row membership, training epochs, optimizer, validation metrics, augmentation count, or speaker/recordist count. [REF-17]

## Final Vocabulary

`PLAY_MUSIC`, `WEATHER`, `TIME`, `LIGHT_ON`, `LIGHT_OFF`, `LIGHT_DIM`, `BRIGHTNESS`, `TIMER`, `ALARM`, `TEMPERATURE`, `NEXT`, `PAUSE`, `STOP`, `VOLUME_UP`, `VOLUME_DOWN`, `CREATE_REMINDER`, `LIST_REMINDERS`, `CALL`, `MESSAGE`. [REF-11]

`COLOR` is not a final E50 class. [REF-01] [REF-02]

## Label-Specific Thresholds

| Label | Threshold |
|---|---:|
| `NEXT` | 0.98 |
| `CREATE_REMINDER` | 0.96 |
| `VOLUME_UP` | 0.99 |
| `STOP` | 0.995 |
| `PAUSE` | 0.99 |
| `TIME` | 0.98 |

All other labels use the default threshold unless otherwise documented in the frozen policy. [REF-07]

## Freeze Boundary

```text
E37 wake
  -> command capture
  -> log-Mel preprocessing
  -> E50 CNN
  -> E40 policy
  -> deterministic router
  -> local action
  -> local response
  -> return to listening
```

The enhanced DUi/GUI is a post-freeze layer documented separately in `08_POST_FREEZE_DUi.md`. It launches, displays, and supervises the runtime, but it does not alter the frozen E50 VCM core. [REF-01] [REF-05] [REF-06]

## Integrity Boundary

This identity document is documentation-only. It does not copy model weights, change hashes, alter thresholds, rerun benchmarks, or modify the frozen `ME2_VCM` source. The hashes here are read from existing final SHA/integrity evidence. [REF-13]
