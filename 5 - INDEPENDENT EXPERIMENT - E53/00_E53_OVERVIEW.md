# E53 Overview

E53 is an independent experimental branch. It is not part of the frozen E50 final-delivery implementation and does not modify, replace, or retroactively change E37, E50, E40, the Raspberry Pi deployment package, the GUI, the router, the response WAVs, or the final E50 benchmark.

The main professor-facing document for this section is:

- [E53 Independent Experiment Report](E53_INDEPENDENT_EXPERIMENT_REPORT.md)

That report explains why E53 was undertaken, how `E53_DATASET_V1` was built and frozen, how LOG011 became the log-Mel control, how LOG025 tested MFCC and PCEN, what the quantitative results were, what failed, and why E53 did not replace E50.

Key identity:

| Item | E53 value |
|---|---|
| Role | Independent offline classifier experiment |
| Dataset | `E53_DATASET_V1` |
| Rows | 24,706 |
| Classes | 20 = 18 operational commands + `UNKNOWN` + `SILENCE` |
| Split | 19,553 train / 2,544 validation / 2,609 test |
| Principal control | LOG011 log-Mel CNN |
| Final feature ablation | LOG025 MFCC and PCEN |
| Deployment status | Not promoted; not Pi deployed |

For the detailed comparison with E50, see [02_E53_E50_SEPARATION.md](02_E53_E50_SEPARATION.md) and Section 15 of the main report.
