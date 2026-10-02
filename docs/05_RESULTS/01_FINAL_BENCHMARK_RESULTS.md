# Final Benchmark Results

## Benchmark Identity

The final benchmark measures the frozen E50 core on Raspberry Pi using the 19-command vocabulary plus one UNKNOWN/no-action trial. It is not an E53 benchmark and does not measure the post-freeze DUi as a new model.

## Results Table

| Result category | Value |
|---|---:|
| Total trials | 20 |
| Valid command trials | 19 |
| UNKNOWN/no-action trials | 1 |
| Wake success | 19/20 = 95.0% |
| Valid-command wake success | 18/19 = 94.74% |
| Raw command classification | 13/19 = 68.42% |
| E40 acceptance | 10/19 = 52.63% |
| Accepted-correct | 10 |
| Accepted-wrong | 0 |
| Accepted-action precision | 10/10 = 100% |
| Safe rejection among non-executed cases | 10/10 = 100% |
| End-to-end action success | 10/19 = 52.63% |
| UNKNOWN safety | 1/1 = 100% |
| Return-to-listening | 20/20 = 100% |

## Engineering Meaning

The final stack prioritizes safe action execution. A command that passes the E40 confidence policy is routed deterministically; the benchmark recorded no accepted-wrong actions. Commands that did not pass acceptance did not produce unsafe local execution in the tested population.

## Limitations

The 20-trial benchmark is final delivery evidence, not a broad acoustic population study. It does not establish broad per-label generalization, broad environmental FAR, or full acoustic response latency.
