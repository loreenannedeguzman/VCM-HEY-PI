# Latency, RTF, and FAR Results

## CNN Latency

| Metric | Value |
|---|---:|
| Mean CNN latency | 31.82 ms |
| P50 CNN latency | 31.39 ms |
| P95 CNN latency | 34.40 ms |
| Max CNN latency | 38.31 ms |
| Mean CNN-only RTF | 0.0080 |
| P95 CNN-only RTF | 0.0086 |

## Command Pipeline RTF

| Metric | Value |
|---|---:|
| Mean command-pipeline RTF | 0.016543 |
| P95 command-pipeline RTF | 0.018500 |

## Response Playback-Start Latency

| Metric | Value |
|---|---:|
| N | 5 |
| Mean | 66.172 ms |
| P50 | 64.837 ms |
| P95 | 73.999 ms |
| P99 | 73.999 ms |
| Max | 73.999 ms |

The response-latency boundary is command WAV capture completion to first observed local `aplay` response process. It is not an acoustic speaker-onset measurement and not full wake-to-response latency.

## Bounded Command-Window FAR

| Metric | Value |
|---|---:|
| False accepts / tested valid out-of-scope command-window safety prompts | 0/4 = 0.0% |

This bounded FAR value applies only to the tested command-window prompt set. It is not a broad environmental wake false-accept-rate claim.
