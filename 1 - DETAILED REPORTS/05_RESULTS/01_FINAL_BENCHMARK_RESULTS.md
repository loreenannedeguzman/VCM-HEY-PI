# Final Benchmark Results

## Benchmark Identity

The final benchmark measures the frozen E50 core on Raspberry Pi using the 19-command vocabulary plus one UNKNOWN/no-action trial. It is not an E53 benchmark and does not measure the post-freeze DUi as a new model.

## Results Table

| Metric | Result | Meaning |
|---|---:|---|
| Total trials | 20 | 19 valid command trials plus 1 UNKNOWN/no-action trial. |
| Valid command trials | 19 | One representative trial per final E50 command label. |
| UNKNOWN/no-action trials | 1 | Unsupported/no-action safety trial. |
| Wake success, overall | 19/20 = 95.0% | E37 accepted wake across all benchmark trials. |
| Wake success, valid commands | 18/19 = 94.74% | E37 accepted wake on valid command trials. |
| Raw command classification | 13/19 = 68.42% | E50 top-label correctness before E40 action gating. |
| E40 acceptance | 10/19 = 52.63% | Valid commands accepted for the action path. |
| Accepted-correct | 10 | Accepted valid commands that produced the correct corresponding action. |
| Accepted-wrong | 0 | Accepted valid commands that produced a wrong action. |
| Accepted-action precision | 10/10 = 100% | Correct action among accepted/executed valid commands. |
| Safe rejection among non-executed cases | 10/10 = 100% | Rejected/non-executed cases produced no routed action. |
| End-to-end action success | 10/19 = 52.63% | Correct command outcome, accepted execution, response handling, and return-to-listening. |
| UNKNOWN/no-action safety | 1/1 = 100% | Unsupported phrase produced no action. |
| Return-to-listening | 20/20 = 100% | Runtime returned to listening after every trial. |

## Engineering Meaning

The final stack prioritizes safe action execution over maximizing acceptance. A command that passes the E40 confidence policy is routed deterministically; the benchmark recorded no accepted-wrong actions. Commands that did not pass acceptance did not produce unsafe local execution in the tested population. The tradeoff is coverage: raw command classification and end-to-end action success remained moderate.

## Failure Attribution

The observed weaknesses are mainly attributable to live-audio domain mismatch, command-class confusion, deliberate E40 confidence rejection, fixed-vocabulary architecture, limited physical benchmark scope, and incomplete reconstruction of some E37 training-lineage details. These are coverage/generalization limitations rather than evidence of unsafe accepted actions in the final benchmark.

## Limitations

The 20-trial benchmark is final delivery evidence, not a broad acoustic population study. It does not establish broad per-label generalization, broad environmental FAR, full acoustic response latency, or formal speaker-independent Pi robustness.
