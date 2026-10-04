# Confidence Policy E40

## Engineering Question

How does the system decide whether an E50 prediction is allowed to become an action?

E40 is the frozen confidence/rejection policy between E50 command classification and deterministic routing. It exists because a neural classifier can produce a top label even when the evidence is weak. E40 prevents every raw E50 prediction from automatically becoming an action.

```text
E50 predicted label + confidence
  -> E40 threshold check
       accepted: send label to deterministic router
       rejected: no command action is routed
```

## Identity

| Field | Value |
|---|---|
| Policy lineage | `E40_NON_LED_COMMAND_GUARDRAIL_THRESHOLDS` |
| Deployed config | `4b - DEPLOYMENT/vcm_pi_package/configs/e50_revised_vocab_e40_thresholds.json` |
| Deployed policy ID | `E50_REVISED_VOCAB_E40_FROZEN_THRESHOLDS` |
| Config SHA-256 | `A0B2495328FD5A1E0E5885E727623BA6D9F823BE94CCCDFD0AEAD77254BBB3FD` |
| Default command threshold | 0.90 |

E40 is not documented as a separately learned neural model. It is a frozen threshold policy.

## Thresholds

| Label | Threshold |
|---|---:|
| Default command threshold | 0.90 |
| `NEXT` | 0.98 |
| `CREATE_REMINDER` | 0.96 |
| `VOLUME_UP` | 0.99 |
| `STOP` | 0.995 |
| `PAUSE` | 0.99 |
| `TIME` | 0.98 |

The threshold file states that `LIGHT_DIM` uses the inherited default threshold 0.90. Historical `COLOR` is absent because final E50 replaces `COLOR` with `LIGHT_DIM`.

## Why E40 Matters

E40 creates a boundary between recognition and execution. A correct raw prediction can still be rejected if confidence is too low. A wrong raw prediction can also be rejected rather than becoming a wrong action. This is why raw command classification, E40 acceptance, accepted-action precision, safe rejection, and end-to-end action success are separate metrics.

In the final physical Pi benchmark:

| Metric | Result | E40 meaning |
|---|---:|---|
| Raw command classification | 13/19 = 68.42% | E50 top-label correctness before action gating. |
| E40 acceptance / end-to-end action success | 10/19 = 52.63% | Valid commands accepted and completed as correct actions. |
| Accepted-wrong | 0 | No accepted valid command routed to a wrong action. |
| Accepted-action precision | 10/10 = 100% | Accepted/executed valid commands were action-correct. |
| Safe rejection among non-executed cases | 10/10 = 100% | Rejected/non-executed cases did not route unsafe actions. |
| UNKNOWN/no-action safety | 1/1 = 100% | Unsupported input produced no action. |

## Failure And Rejection Behavior

| Situation | Result |
|---|---|
| Prediction meets threshold | Accepted label may be routed. |
| Prediction is below threshold | Rejected; no command action should execute. |
| Prediction is `UNKNOWN`/unsupported | No command action should execute. |
| Correct label below threshold | Coverage loss, not a router failure. |
| Wrong label below threshold | Safe rejection may prevent wrong action. |

## What Not To Claim

E40 did not retrain E50, change E37, alter the final vocabulary, or create new action semantics. It is a frozen confidence policy that controls whether E50 output can enter the deterministic action path.
