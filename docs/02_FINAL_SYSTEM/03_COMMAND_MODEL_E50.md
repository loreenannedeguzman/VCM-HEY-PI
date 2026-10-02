# 03 - Command Model E50

## Identity

The frozen command model is `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT`. The final command-model weights SHA-256 is `BC8AC64CED4305DDF43BF4DE377F3CC636A764EFF339CD9F92AF06340C50B8FF`. [REF-01] [REF-03] [REF-13]

## Purpose

E50 classifies post-wake command audio into one of 19 fixed raw command labels. It is not an ASR transcript model, LLM, threshold policy, action mapper, or GUI component. [REF-01] [REF-05]

## Input Representation

| Field | Value |
|---|---:|
| Sample rate | 16,000 Hz |
| Target duration | 4.0 seconds |
| Frame length | 25.0 ms |
| Frame step | 10.0 ms |
| FFT length | 512 |
| Mel bins | 40 |
| Expected frames | 398 |
| Feature shape | `(398, 40)` / model input `(398, 40, 1)` |

Evidence: [REF-11] [REF-12]

## Architecture

The model summary identifies `tiny_vcm_cnn`: Conv2D blocks with batch normalization and max pooling, global average/max pooling, concatenation, dropout, dense layer, and a 19-unit output layer. Total parameters are 66,483. [REF-12]

## Output Labels

The output labels are `PLAY_MUSIC`, `WEATHER`, `TIME`, `LIGHT_ON`, `LIGHT_OFF`, `LIGHT_DIM`, `BRIGHTNESS`, `TIMER`, `ALARM`, `TEMPERATURE`, `NEXT`, `PAUSE`, `STOP`, `VOLUME_UP`, `VOLUME_DOWN`, `CREATE_REMINDER`, `LIST_REMINDERS`, `CALL`, and `MESSAGE`. [REF-11]

`COLOR` is not a final E50 class. Final E50 uses `LIGHT_DIM`. [REF-01] [REF-02] [REF-11]

## Model Size And Efficiency

The final report records 66,483 parameters, a 251,734-byte E50 weights artifact, and 85,774,144 Conv2D/Dense MACs per 4-second input. [REF-01] [REF-12]

## Relationship To E40

E50 produces a predicted label and confidence. E40 then decides whether the prediction is accepted. A correct raw prediction can still be rejected if it is below threshold. [REF-01] [REF-07]

## Relationship To Routing

E50 does not execute actions. Accepted labels pass to the deterministic router, which maps raw labels into intents and slots. [REF-08] [REF-09]

## What E50 Does Not Do

E50 does not recognize arbitrary speech, transcribe text, use cloud ASR, use an LLM, choose thresholds, decide label-to-action semantics, execute actions directly, or modify the GUI. [REF-01] [REF-05] [REF-08]
