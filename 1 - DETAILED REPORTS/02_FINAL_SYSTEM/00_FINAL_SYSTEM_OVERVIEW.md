# 00 - Final System Overview

## Purpose

This is the entry point for the final-system E50 final-system documentation. E50 is the final Machine Exercise 2 Voice Command Machine delivery: an offline Raspberry Pi 5 voice-command system that listens for a wake phrase, classifies a fixed-vocabulary command, applies a frozen confidence policy, routes accepted labels to deterministic local actions, plays local response audio, and returns to listening. It is not a cloud assistant, LLM, online ASR system, or arbitrary transcription system. [REF-01] [REF-03]

## System Map

```text
POST-FREEZE ENHANCED DUi / GUI LAYER
  - local START / STOP / STATUS interface
  - launches the frozen runtime
  - reads result JSON for display
  - does not recognize speech or change thresholds
                    |
                    v
FROZEN E50 VCM CORE
  Microphone
    -> E37 Wake Gate
    -> Command Capture
    -> Log-Mel Features
    -> E50 CNN
    -> E40 Confidence / Rejection
    -> Deterministic Router
    -> Local Action
    -> Response Audio
    -> Return to Listening
```

## Frozen Core

The frozen core is the E37 wake detector, command capture, log-Mel preprocessing, E50 command CNN, E40 confidence/rejection policy, deterministic router/action layer, local response audio, final 19-label vocabulary, and frozen model/configuration identities. [REF-01] [REF-05] [REF-07] [REF-13]

Recovered E37 provenance evidence now documents the project-specific Raspberry Pi `Hey Pi` wake-recording manifest: 99 wake-stage recordings, including 50 `WAKE` / `hey pi` recordings, 64 adaptation-designated rows, and 35 holdout-designated rows. This strengthens the wake-gate recording provenance but does not reconstruct the exact final E37 training subset or training hyperparameters. [REF-17]

## Post-Freeze DUi / GUI

The enhanced DUi/GUI is a post-freeze interface and deployment shell. It starts and stops the existing runtime, prevents duplicate runtime starts, and displays status. It does not replace E37, E50, E40, the vocabulary, threshold policy, deterministic router, or response assets. [REF-05] [REF-06] [REF-15]

## Component Roles

| Component | Role | Evidence |
|---|---|---|
| E37 wake gate | Detects `Hey Pi` and opens the command window only after accepted wake detection; recovered Pi evidence documents the project-specific wake-recording manifest. | [REF-04] [REF-05] [REF-17] |
| Command capture | Records the post-wake command window. | [REF-05] |
| Log-Mel preprocessing | Converts 4-second 16 kHz mono command audio to E50 features. | [REF-11] |
| E50 CNN | Predicts one of 19 fixed command labels. | [REF-11] [REF-12] |
| E40 policy | Accepts or rejects command predictions using frozen thresholds. | [REF-07] |
| Router/action layer | Maps accepted labels to deterministic local intents, slots, and actions. | [REF-08] [REF-09] |
| Response audio | Plays local WAV feedback for commands and rejection. | [REF-10] |
| DUi/GUI | Provides local Pi interface around the frozen runtime. | [REF-05] [REF-06] [REF-15] |

## Final Vocabulary

The final labels are `PLAY_MUSIC`, `WEATHER`, `TIME`, `LIGHT_ON`, `LIGHT_OFF`, `LIGHT_DIM`, `BRIGHTNESS`, `TIMER`, `ALARM`, `TEMPERATURE`, `NEXT`, `PAUSE`, `STOP`, `VOLUME_UP`, `VOLUME_DOWN`, `CREATE_REMINDER`, `LIST_REMINDERS`, `CALL`, and `MESSAGE`. `COLOR` is not a final E50 class. [REF-01] [REF-02] [REF-11]

## Deeper Documentation

- `01_SYSTEM_ARCHITECTURE.md` explains the internal runtime pipeline.
- `02_WAKE_GATE_E37.md` explains the wake gate.
- `03_COMMAND_MODEL_E50.md` explains the command CNN.
- `04_CONFIDENCE_POLICY_E40.md` explains E40 thresholds and rejection.
- `05_FINAL_VOCABULARY_AND_ACTIONS.md` maps labels to deterministic actions.
- `06_DATASET_AND_TRAINING.md` explains dataset construction and provenance.
- `07_PI_DEPLOYMENT.md` explains what runs on the Raspberry Pi.
- `08_POST_FREEZE_DUi.md` explains the GUI boundary.
- `09_FROZEN_SYSTEM_IDENTITY.md` records final identities and hashes.

