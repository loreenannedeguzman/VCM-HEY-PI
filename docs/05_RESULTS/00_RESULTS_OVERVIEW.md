# E50 Results Overview

## Purpose

This section centralizes the final measured results for the frozen E50 voice-command module. Validation methodology is described in 04_VALIDATION; artifact identity and hashes are described in 07_INTEGRITY.

## Final Result Summary

| Metric | Result |
|---|---:|
| Final Pi benchmark population | 20 trials |
| Valid command trials | 19 |
| UNKNOWN/no-action trials | 1 |
| Wake success | 19/20 = 95.0% |
| Valid-command wake success | 18/19 = 94.74% |
| Raw command classification | 13/19 = 68.42% |
| Acceptance | 10/19 = 52.63% |
| Accepted correct | 10 |
| Accepted wrong | 0 |
| Accepted-action precision | 10/10 = 100% |
| Safe rejection among non-executed cases | 10/10 = 100% |
| End-to-end action success | 10/19 = 52.63% |
| UNKNOWN safety | 1/1 = 100% |
| Return-to-listening | 20/20 = 100% |

## Interpretation

The final results show a conservative system: accepted commands were action-correct in the final benchmark, while rejected or non-executed cases remained safe in the tested population. The primary remaining limitation is recall/action coverage, not accepted-action precision.
