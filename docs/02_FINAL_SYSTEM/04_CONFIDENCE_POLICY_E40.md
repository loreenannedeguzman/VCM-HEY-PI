# 04 - Confidence Policy E40

## Purpose

E40 exists so that not every E50 prediction automatically becomes an action. It is the frozen confidence/rejection gate between E50 command classification and deterministic routing. [REF-01] [REF-07]

## Identity

The policy is documented as `E40_NON_LED_COMMAND_GUARDRAIL_THRESHOLDS`. In deployment it appears as `configs/e50_revised_vocab_e40_thresholds.json`, with policy ID `E50_REVISED_VOCAB_E40_FROZEN_THRESHOLDS` and base policy ID `E40_NON_LED_COMMAND_GUARDRAIL_THRESHOLDS`. The final SHA manifest records SHA-256 `A0B2495328FD5A1E0E5885E727623BA6D9F823BE94CCCDFD0AEAD77254BBB3FD`. [REF-07] [REF-13]

## Thresholds

The default command threshold is `0.90`. The frozen policy also contains higher label-specific thresholds:

| Label | Threshold |
|---|---:|
| `NEXT` | 0.98 |
| `CREATE_REMINDER` | 0.96 |
| `VOLUME_UP` | 0.99 |
| `STOP` | 0.995 |
| `PAUSE` | 0.99 |
| `TIME` | 0.98 |

The threshold file states that `LIGHT_DIM` uses the inherited default threshold `0.90`, and that historical `COLOR` is absent because E50 replaces `COLOR` with `LIGHT_DIM`. [REF-07]

## Acceptance And Rejection

If an E50 prediction meets the applicable threshold, the accepted label may be routed. If it does not, the command is rejected and no command action should execute. This is why final metrics distinguish raw classification, acceptance, accepted-action precision, safe rejection, and end-to-end action success. [REF-01] [REF-14]

## Relationship To Routing

E40 is upstream of the deterministic router. A label being callable does not mean every prediction for that label is accepted. The router receives accepted labels and maps them to predefined intents and slots. [REF-07] [REF-08]

## What E40 Is Not

E40 is not documented as a separately learned model in the reviewed evidence. It should not be described as retraining E50, modifying E37, or changing action semantics. [REF-07]

## Safety Interpretation

E40 can convert uncertain predictions into safe no-action behavior. It can also reduce end-to-end success when a correct raw prediction falls below threshold. Both outcomes are part of the final benchmark interpretation and should not be collapsed into one generic accuracy number. [REF-01] [REF-14]
