# E53 Findings

This file is the concise findings summary. The complete evidence-backed discussion is in [E53_INDEPENDENT_EXPERIMENT_REPORT.md](E53_INDEPENDENT_EXPERIMENT_REPORT.md).

## Central Results

| Experiment | Feature / role | Test accuracy | Macro-F1 | Weighted-F1 | Operational macro-F1 | UNKNOWN F1 | SILENCE F1 | Decision |
|---|---|---:|---:|---:|---:|---:|---:|---|
| LOG011 | log-Mel control | 0.463779 | 0.410447 | 0.445472 | 0.372275 | 0.922756 | 0.585242 | established E53 control |
| LOG025_MFCC | MFCC | 0.478727 | 0.447684 | 0.450891 | 0.444856 | 0.596129 | 0.350148 | mixed / inconclusive |
| LOG025_PCEN | PCEN | 0.463779 | 0.387960 | 0.449258 | 0.338223 | 0.819328 | 0.851852 | mixed / inconclusive |

MFCC improved E53 aggregate command metrics relative to LOG011, including accuracy, macro-F1, weighted-F1, and operational macro-F1, but it substantially degraded `UNKNOWN` and `SILENCE`. PCEN improved `SILENCE` F1 but did not improve macro-F1 or operational macro-F1 relative to LOG011, and `UNKNOWN` remained below LOG011.

## Main Failure Patterns

- LOG011's largest test failure was `SILENCE -> MEDIA_NEXT` with 119 cases.
- LOG011 also had large `LIST_REMINDERS -> CREATE_REMINDER` and `VOLUME_DOWN -> VOLUME_UP` confusions, each with 65 cases.
- MFCC still had strong SILENCE confusion: `SILENCE -> UNKNOWN` 109 and `SILENCE -> MEDIA_NEXT` 99.
- PCEN improved SILENCE but worsened or preserved other command confusions, including `VOLUME_DOWN -> VOLUME_UP` 74 and `TIME -> CALL` 57.

## Bottom Line

E53 demonstrated a disciplined experimental investigation, not a replacement system. It did not establish that E53 beat E50, did not establish Pi deployment readiness, and did not justify replacing the frozen E50 delivery stack.
