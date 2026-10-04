# Latency, RTF, and FAR Results

## CNN Inference Latency

These values measure E50 CNN inference only on Raspberry Pi 5 saved-command-WAV evidence. They do not include wake capture, user speech onset, GUI launch, audio playback onset, or full action timing.

| Metric | Value |
|---|---:|
| Mean CNN latency | 31.82 ms |
| P50 CNN latency | 31.39 ms |
| P95 CNN latency | 34.40 ms |
| Max CNN latency | 38.31 ms |
| Mean CNN-only RTF | 0.0080 |
| P95 CNN-only RTF | 0.0086 |

The CNN-only P95 RTF of 0.0086 means the CNN inference time was less than 1% of the 4-second command input window for the measured P95 case. This is an efficiency measure, not an end-to-end user-perceived latency measure.

## Qualified Command-Pipeline RTF

| Metric | Value |
|---|---:|
| Mean command-pipeline RTF | 0.016543 |
| P95 command-pipeline RTF | 0.018500 |

This qualified command-pipeline RTF measures the documented path to response playback start, not full acoustic wake-to-response timing.

## Response Playback-Start Latency

| Metric | Value |
|---|---:|
| N | 5 accepted/executed trials |
| Mean | 66.172 ms |
| P50 | 64.837 ms |
| P95 | 73.999 ms |
| P99 | 73.999 ms |
| Max | 73.999 ms |

Boundary: command WAV capture completion to first observed local `aplay` response process. This is not acoustic speaker-onset latency and not full wake-to-response latency.

## Bounded Command-Window FAR

| Metric | Value |
|---|---:|
| False accepts / tested valid out-of-scope command-window safety prompts | 0/4 = 0.0% |

This bounded FAR value applies only to the tested command-window prompt set. It is not a broad environmental false-accept-rate claim over arbitrary background audio or no-wake conditions.

## Not Established By These Measurements

- GUI launch-to-ready latency.
- Full wake-to-action latency.
- Full wake-to-response latency.
- Acoustic speaker-onset latency.
- Broad environmental FAR.
- Broad noise/reverberation robustness.
