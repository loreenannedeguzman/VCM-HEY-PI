# Results Overview

## Purpose

This section centralizes the final measured results for the frozen E50 VCM. Validation methodology and evidence boundaries are in `docs/04_VALIDATION/`; artifact identity and hashes are in `docs/07_INTEGRITY/`.

## Core Result

The final physical Raspberry Pi benchmark shows moderate command-recognition coverage but strong tested action safety. Raw E50 command classification was 13/19 = 68.42%. End-to-end action success was 10/19 = 52.63%. However, every accepted/executed valid command produced the correct action: accepted-action precision was 10/10 = 100%, with 0 accepted-wrong actions. Non-executed cases were safely rejected in 10/10 cases, the UNKNOWN/no-action case was safe at 1/1, and the runtime returned to listening after 20/20 trials.

## Final Result Summary

| Metric | Result |
|---|---:|
| Final Pi benchmark population | 20 trials |
| Valid command trials | 19 |
| UNKNOWN/no-action trials | 1 |
| Wake success | 19/20 = 95.0% |
| Valid-command wake success | 18/19 = 94.74% |
| Raw command classification | 13/19 = 68.42% |
| Acceptance / end-to-end action success | 10/19 = 52.63% |
| Accepted-correct | 10 |
| Accepted-wrong | 0 |
| Accepted-action precision | 10/10 = 100% |
| Safe rejection among non-executed cases | 10/10 = 100% |
| UNKNOWN/no-action safety | 1/1 = 100% |
| Return-to-listening | 20/20 = 100% |
| CNN mean latency | 31.82 ms |
| CNN P95 latency | 34.40 ms |
| CNN-only P95 RTF | 0.0086 |
| Qualified response playback-start latency | mean 66.172 ms; P95 73.999 ms |

## Interpretation

The result is not best summarized as high overall accuracy. The more accurate engineering interpretation is: E50 had moderate raw command classification in the final live benchmark, while E40 and the deterministic action layer produced conservative action behavior in the tested population. The system preferred rejecting uncertain commands to executing wrong actions.
