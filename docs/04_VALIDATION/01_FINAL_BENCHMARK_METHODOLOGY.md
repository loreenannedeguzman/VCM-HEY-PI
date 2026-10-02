# Final Benchmark Methodology

## Benchmark Population

The final Pi benchmark population consists of 20 trials: one trial for each of the 19 final command labels plus one UNKNOWN/no-action trial.

## Pipeline Under Test

Microphone -> E37 Wake Gate -> Command Capture -> Log-Mel Features -> E50 CNN -> E40 Confidence / Rejection -> Deterministic Router -> Local Action -> Response Audio -> Return to Listening

## Measurement Categories

| Category | Meaning |
|---|---|
| Wake success | The wake gate opens the command window when expected. |
| Raw command classification | The E50 CNN top prediction matches the expected command before acceptance filtering. |
| Acceptance | E40 accepts the prediction under the frozen threshold policy. |
| Accepted-action precision | Accepted commands execute the correct deterministic action. |
| Safe rejection | Non-executed cases are rejected without unsafe action. |
| UNKNOWN/no-action | The out-of-scope UNKNOWN trial avoids action execution. |
| Return-to-listening | The system returns to listening after each trial. |

## Methodological Limits

The benchmark contains one final trial per command label, so it supports final delivery evidence rather than per-command statistical confidence intervals. Bounded command-window FAR is limited to the tested command-window prompts and must not be generalized as a broad always-listening FAR estimate.
