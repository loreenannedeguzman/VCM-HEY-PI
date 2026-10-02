# 01 - System Architecture

## Architectural Summary

E50 is a wake-gated fixed-vocabulary local command system. Learned recognition and deterministic action execution are deliberately separated. The learned components decide whether the wake phrase was detected and which command label best matches the captured command audio. The policy and deterministic components decide whether that label is accepted and what local action should occur. [REF-01] [REF-03] [REF-05]

```text
Audio acquisition
  -> E37 wake detection
  -> command capture
  -> audio preprocessing
  -> log-Mel representation
  -> E50 CNN inference
  -> E40 confidence/rejection
  -> deterministic routing
  -> local action
  -> local response audio
  -> return to listening
```

## Audio Acquisition

The Raspberry Pi package records local mono 16 kHz audio through ALSA. The technical configuration uses local Pi microphone/audio devices; operational inference does not require a laptop microphone, cloud ASR, LLM, or remote Python service. [REF-03] [REF-05] [REF-15]

## Wake Detection

E37 runs first. It listens for the wake phrase `Hey Pi` and opens the command-capture window only when the wake result is accepted at the frozen threshold. If wake is not accepted, the system stays in wake/listening behavior and should not route a command action. [REF-04] [REF-05]

The recovered E37 audit documents the project-specific Raspberry Pi wake-recording evidence behind this stage: `/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi/manifest.csv` contains 99 wake-stage recordings, including 50 `WAKE` / `hey pi` rows, 64 adaptation-designated rows, and 35 holdout-designated rows. This evidence documents the recording set; it does not independently establish the exact final E37 training-row membership. [REF-17]

## Command Capture And Preprocessing

After accepted wake, the runtime captures a command window. The command audio is standardized to 4.0 seconds at 16 kHz and converted to log-Mel features. The E50 training configuration records 25 ms frames, 10 ms frame step, 512 FFT length, 40 Mel bins, and expected feature shape `(398, 40)`, represented by the model as `(398, 40, 1)`. [REF-11] [REF-12]

## E50 CNN Inference

The E50 CNN predicts a raw command label and confidence. It does not transcribe arbitrary speech and does not execute actions. [REF-05] [REF-11] [REF-12]

## E40 Confidence / Rejection

E40 applies the frozen confidence policy after E50 prediction. Below-threshold predictions are rejected and should not route actions. The default threshold is `0.90`, with documented label-specific thresholds for selected labels. [REF-07]

## Deterministic Routing And Local Actions

Only accepted labels pass to the deterministic router. The router maps raw labels to assignment intents and default slots; for example, `LIGHT_ON` maps to `LIGHT_CONTROL` with `light_action=on`, and `NEXT` maps to `MEDIA_CONTROL` with `media_action=next`. The action layer then executes local behavior or local stubs. [REF-08] [REF-09]

## Response Audio And Return To Listening

The response map points labels and rejection feedback to local WAV files. After action/response handling, the runtime returns to listening. The package manifest identifies persistent runtime support through cycles/continuous mode and the touchscreen GUI wrapper. [REF-06] [REF-10]

## State Transitions

```text
WAKE LISTENING
  -> E37 accepted
COMMAND WINDOW
  -> E50 predicts label
  -> E40 accepts or rejects
REJECTED
  -> no routed command action
  -> return to wake listening
ACCEPTED
  -> deterministic route
  -> local action / response
  -> return to wake listening
```

## Learned Versus Deterministic Components

| Type | Component | Explanation |
|---|---|---|
| Learned | E37 wake detector | Detects wake phrase; project-specific `Hey Pi` recording provenance is documented separately from final training-row membership. |
| Learned | E50 command CNN | Classifies command audio into 19 labels. |
| Policy | E40 thresholds | Frozen confidence/rejection gate. |
| Deterministic | Raw-command router | Fixed label-to-intent/slot mapping. |
| Deterministic/local | Action layer and response WAVs | Local behavior and recorded feedback. |

The system is therefore not `speech -> neural network -> arbitrary action`. It is `speech -> wake detection -> command classification -> confidence gate -> fixed route -> local action`. [REF-04]

