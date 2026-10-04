# E53 / E50 Separation

E53 is independent from E50.

| Dimension | E50 | E53 | Directly comparable? |
|---|---|---|---|
| Role | Final delivery VCM | Independent experiment | Yes, by project role. |
| Runtime | E37 wake + E50 CNN + E40 guardrail + router + response WAV | Offline classifier experiments | No. |
| Physical Pi validation | Yes, final 20-trial benchmark | Not established | Presence/absence only. |
| Wake behavior | E37 wake gate | Not part of E53 | No. |
| Action routing | Deterministic local actions | Not evaluated | No. |
| UNKNOWN handling | E40/no-action behavior in final benchmark | Explicit `UNKNOWN` class in offline dataset | Conceptually related, not numerically equivalent. |
| SILENCE handling | Not a final E50 command class | Explicit `SILENCE` class in E53 | Conceptually related, not numerically equivalent. |
| Final status | Frozen deployed system | Not promoted | Yes. |

E50 final physical Pi benchmark facts remain: 20 trials, wake success 19/20, raw command classification 13/19 = 68.42%, end-to-end action success 10/19 = 52.63%, accepted-action precision 10/10 = 100%, safe rejection 10/10 = 100%, UNKNOWN/no-action safety 1/1 = 100%, and return-to-listening 20/20 = 100%.

E53's best feature-ablation result was MFCC with test accuracy 0.478727 and macro-F1 0.447684 on `E53_DATASET_V1`. That is not directly comparable to E50's physical Pi benchmark because the datasets, label sets, evaluation protocols, and runtime responsibilities differ.

Conclusion: E53 is useful experimental evidence, but it does not alter E50's frozen final system identity and does not establish that E50 should be replaced.
