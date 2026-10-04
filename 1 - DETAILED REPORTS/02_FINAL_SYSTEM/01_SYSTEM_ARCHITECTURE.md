# System Architecture

## System Purpose

E50 is a fixed-vocabulary, wake-gated local voice-command system for Raspberry Pi 5. It performs command classification and deterministic local action routing after a wake phrase. It is not an LLM, cloud assistant, arbitrary speech transcription system, or unrestricted natural-language understanding system. The runtime accepts only the final 19-label command vocabulary and deliberately separates recognition, acceptance, and action execution.

The frozen deployable core is:

```text
E37 wake gate
  -> post-wake command capture
  -> log-Mel preprocessing
  -> E50 command CNN
  -> E40 confidence / rejection policy
  -> deterministic command router
  -> local action
  -> local WAV response
  -> return to listening
```

The GUI/DUi is outside the recognition core. It starts, stops, and displays the runtime, but it does not replace the wake detector, command classifier, threshold policy, router, or response assets.

## End-To-End Pipeline

| Stage | Input | Output | Technical responsibility | Failure behavior | Frozen core? | Evidence |
|---|---|---|---|---|---|---|
| Pi microphone | Local audio | 16 kHz mono waveform | Capture local microphone audio on the Raspberry Pi path. | No usable audio means no reliable wake/command decision. | Yes | Deployment README, preprocessing config, E37 manifest device evidence |
| E37 wake detection | Wake-stage audio | Wake accepted/rejected | Detect whether the user said `Hey Pi`. | If wake is rejected, no command window opens and no command action is routed. | Yes | `02_WAKE_GATE_E37.md`, E37 artifacts |
| Command capture | Post-wake microphone audio | Fixed command window | Capture the command after accepted wake. | If capture fails or is unusable, command classification cannot be trusted. | Yes | Pi runtime and deployment docs |
| Log-Mel preprocessing | Raw command waveform | `(398, 40)` feature matrix, model input `(398, 40, 1)` | Standardize audio to 16 kHz, 4.0 s, peak-normalize, and compute log-Mel features. | Bad or out-of-distribution audio can produce weak classification confidence. | Yes | Phase BG training config, preprocessing config |
| E50 command CNN | Log-Mel feature tensor | 19-label score vector / top prediction | Predict the most likely command label. | Wrong or uncertain prediction does not itself execute an action. | Yes | E50 model summary and training config |
| E40 confidence policy | E50 label and confidence | Accepted or rejected command | Decide whether the prediction is confident enough to become an action. | Below-threshold predictions are rejected and no command action is routed. | Yes | E40 threshold config |
| Deterministic router | Accepted label | Intent and default slots | Map accepted labels to fixed local command semantics. | Unsupported/no-action labels do not route command actions. | Yes | `raw_command_router.py` evidence |
| Local action layer | Intent/slots | Local action result | Execute local behavior or local stubs according to the deterministic route. | Action failures are reported as local runtime behavior, not model retraining. | Yes | `command_actions.py` evidence |
| Response WAV | Action/rejection result | Local audio feedback | Play a configured local WAV response, including rejection feedback. | Missing/failed playback affects user feedback, not the model decision. | Yes | `demo_response_assets.json` and WAV assets |
| Return to listening | Completed action/rejection | Wake-listening state | Reset the runtime loop for the next wake phrase. | If reset fails, the system would not be ready for the next trial. | Yes | Final benchmark return-to-listening 20/20 |

## Component Boundaries

The most important engineering boundary is that recognition is not the same as action execution. E37 decides whether the system should wake. E50 predicts a command label. E40 decides whether that prediction is allowed to become an action. The deterministic router maps only accepted labels to predefined local action semantics. The response layer plays local feedback. This design prevents every raw neural-network prediction from automatically becoming a physical or logical action.

This is why the final benchmark reports several different metrics rather than one generic accuracy number. Raw command classification was 13/19 = 68.42%, but only 10/19 valid command trials were accepted and completed the end-to-end action path. Among those accepted commands, accepted-action precision was 10/10 = 100%, with 0 accepted-wrong actions in the tested population. The distinction between raw classification, acceptance, and action correctness is part of the architecture.

## Model And Deployment Specification

| Property | E50 value | Evidence |
|---|---:|---|
| Hardware target | Raspberry Pi 5 | Deployment/report evidence |
| Final command model | `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT` | Training config / frozen identity |
| Wake model | `E37_TARGETED_COLOR_VOLUME_FIX` | E37 artifacts / frozen identity |
| Threshold policy | `E40_NON_LED_COMMAND_GUARDRAIL_THRESHOLDS` | E40 config / frozen identity |
| Runtime vocabulary | 19 labels | Training config / vocabulary docs |
| Sampling rate | 16 kHz | Phase BG training config |
| Input duration | 4.0 s | Phase BG training config |
| Feature representation | log-Mel | Phase BG training config |
| Feature shape | `(398, 40)` / `(398, 40, 1)` | Phase BG config / model summary |
| E50 architecture | `tiny_vcm_cnn`, mapped E41 initialization | Model summary / training config |
| E50 parameters | 66,483 | Model summary |
| E50 weights size | 251,734 bytes | Final report / artifact evidence |
| E50 MACs | 85,774,144 Conv2D/Dense MACs per 4 s input | Final report |
| E50 weights SHA-256 | `BC8AC64CED4305DDF43BF4DE377F3CC636A764EFF339CD9F92AF06340C50B8FF` | Integrity evidence |
| E37 weights SHA-256 | `687E82E2CEFA6D74CEF2C0A15D28F8F6142D47D4A67E57C68C091E83FC2CEBDE` | Integrity evidence |
| E40 config SHA-256 | `A0B2495328FD5A1E0E5885E727623BA6D9F823BE94CCCDFD0AEAD77254BBB3FD` | Integrity evidence |
| Wake threshold | 0.90 | Wake/deployment config evidence |
| Command default threshold | 0.90 | E40 threshold config |
| CNN mean latency | 31.82 ms | Pi latency benchmark |
| CNN P95 latency | 34.40 ms | Pi latency benchmark |
| CNN P95 RTF | 0.0086 | Pi latency benchmark |

## Why The Architecture Is Structured This Way

The system uses a small CNN rather than ASR or an LLM because the task is fixed-vocabulary command recognition, not transcription. It uses a wake gate because the command model should not continuously route arbitrary background speech. It uses log-Mel features because the CNN consumes a compact time-frequency representation rather than raw text. It uses E40 after E50 because a predicted label can be wrong or weak even when it is the top class. It uses deterministic routing because the final actions are fixed and inspectable rather than generated at runtime.

This makes the system conservative. Some valid commands are rejected, reducing end-to-end action success. The benefit shown in the final benchmark is that accepted commands did not produce wrong actions: accepted-wrong was 0, accepted-action precision was 10/10, and safe rejection among non-executed cases was 10/10 in the tested population.

## Failure Paths

| Case | System behavior | Interpretation |
|---|---|---|
| Wake phrase is not accepted | Command window does not open; no command action is routed. | E37 wake miss or no-wake behavior. |
| Wake accepts an alternate phrase | Command window opens even though the phrase was not `Hey Pi`. | Wake false accept, not GUI failure. |
| E50 predicts incorrectly but confidence is below threshold | E40 rejects; no command action is routed. | Safe rejection can prevent wrong action. |
| E50 predicts a correct label but confidence is below threshold | E40 rejects; no command action is routed. | Coverage loss caused by conservative thresholding. |
| Prediction is accepted | Label is passed to deterministic router and local action path. | Accepted command becomes an inspectable fixed route. |
| Input is `UNKNOWN`/unsupported | No command action should execute; rejection response may play. | No-action safety path. |
| Runtime completes action or rejection | Response WAV may play; system returns to wake listening. | Final benchmark recorded return-to-listening 20/20. |

## What This Architecture Does Not Claim

The architecture does not establish broad environmental false-accept rate, full acoustic wake-to-action latency, formal unseen-speaker physical-Pi generalization, open-ended speech understanding, or production-grade robustness. The evidence supports a functioning offline VCM prototype with fast local inference, conservative action gating, and moderate command-level recognition coverage in the final physical benchmark.
