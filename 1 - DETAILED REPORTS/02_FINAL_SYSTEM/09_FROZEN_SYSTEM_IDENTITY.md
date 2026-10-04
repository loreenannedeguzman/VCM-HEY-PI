# Frozen System Identity

## Purpose

This page is the concise identity sheet for the final frozen E50 VCM. It records the components that define the deployable system and separates them from post-freeze interface work.

## Frozen Core

| Field | Value |
|---|---|
| Final command model | `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT` |
| E50 architecture | E41 `tiny_vcm_cnn` with mapped E41 initialization |
| E50 parameters | 66,483 |
| E50 weights SHA-256 | `BC8AC64CED4305DDF43BF4DE377F3CC636A764EFF339CD9F92AF06340C50B8FF` |
| E50 normalization SHA-256 | `2D71873B6326D6552D7C5B1C22995FFD5132C357AAEC237CB85CBD7EF739283F` |
| Wake model | `E37_TARGETED_COLOR_VOLUME_FIX` |
| E37 weights SHA-256 | `687E82E2CEFA6D74CEF2C0A15D28F8F6142D47D4A67E57C68C091E83FC2CEBDE` |
| E37 normalization SHA-256 | `3BFA93F202DC0C241E577E5B89506F2CB6D0F35B8239297C215A7F81E970B4C7` |
| Confidence policy | `E40_NON_LED_COMMAND_GUARDRAIL_THRESHOLDS` |
| E40 deployed config | `configs/e50_revised_vocab_e40_thresholds.json` |
| E40 config SHA-256 | `A0B2495328FD5A1E0E5885E727623BA6D9F823BE94CCCDFD0AEAD77254BBB3FD` |
| Wake threshold | 0.90 |
| Command default threshold | 0.90 |
| Runner / GUI launcher | `scripts/run_vcm_touchscreen_gui.sh` launching `scripts/vcm_touchscreen_gui.py` |
| Wake-command runtime | `scripts/pi_wake_voice_control_demo.py` |
| GPIO status | Off unless explicitly enabled |
| Response audio | Local WAV response map enabled |

## Final Vocabulary

`PLAY_MUSIC`, `WEATHER`, `TIME`, `LIGHT_ON`, `LIGHT_OFF`, `LIGHT_DIM`, `BRIGHTNESS`, `TIMER`, `ALARM`, `TEMPERATURE`, `NEXT`, `PAUSE`, `STOP`, `VOLUME_UP`, `VOLUME_DOWN`, `CREATE_REMINDER`, `LIST_REMINDERS`, `CALL`, `MESSAGE`.

`COLOR` is not a final E50 class.

## Label-Specific Thresholds

| Label | Threshold |
|---|---:|
| `NEXT` | 0.98 |
| `CREATE_REMINDER` | 0.96 |
| `VOLUME_UP` | 0.99 |
| `STOP` | 0.995 |
| `PAUSE` | 0.99 |
| `TIME` | 0.98 |

All other labels use the default command threshold unless otherwise documented in the frozen policy.

## Recovered E37 Recording Evidence

The frozen E37 artifact is now accompanied by recovered project-specific wake-recording evidence: 99 total `wake_validation_hey_pi` recordings, including 50 `WAKE` / `hey pi`, 15 `UNKNOWN`, 14 `COLOR`, 14 `VOLUME_UP`, 3 `LIGHT_ON`, and 3 `PLAY_MUSIC`; 64 adaptation-designated rows; 35 holdout-designated rows; 4-second duration; 16 kHz sample rate; and input device `plughw:2,0`. This strengthens E37 provenance but does not establish exact final E37 training-row membership, epochs, optimizer, validation metrics, augmentation count, or speaker/recordist count.

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

The enhanced DUi/GUI is post-freeze. It launches, displays, and supervises the runtime, but it does not alter the frozen recognition/action core or final benchmark identity.

## Integrity Boundary

This document records identity; it does not copy model weights, change hashes, alter thresholds, rerun benchmarks, or modify the deployment package.
