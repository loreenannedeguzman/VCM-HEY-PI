# Validation Overview

## Purpose

Validation answers how the frozen E50 VCM was tested, what evidence each test supports, and what the tests do not prove. Results are summarized in `1 - DETAILED REPORTS/05_RESULTS/`; this section explains the validation boundaries.

## Validation Objects

| Validation object | What it checks | What it does not check |
|---|---|---|
| Final physical Pi benchmark | Integrated wake, command, E40 acceptance/rejection, routing, response, and return-to-listening behavior over 20 trials. | Broad speaker-independent, noise-independent, or statistically powered per-label performance. |
| CNN saved-command-WAV latency benchmark | E50 CNN inference time on Raspberry Pi 5 saved command WAVs. | Full wake-to-action latency, GUI latency, or acoustic speaker-onset latency. |
| Response playback-start audit | Qualified local time from command WAV capture completion to observed `aplay` response start for accepted/executed trials. | Acoustic response onset or full wake-to-response latency. |
| Bounded command-window safety/FAR check | False accepts over the tested out-of-scope command-window prompts. | Broad environmental wake false-accept rate over arbitrary background/no-wake audio. |
| E51 comparison | Offline same-architecture comparison context for E50 selection. | A second final Pi deployment or replacement for E50. |

## Final Benchmark Population

The final physical Pi benchmark used 20 integrated trials: 19 valid command-label trials plus one UNKNOWN/no-action trial. This benchmark is final deployment evidence for the frozen E50 stack, not a statistically exhaustive acoustic population study.

## Evidence Interpretation

The validation is layered. Wake success measures E37 wake behavior. Raw command classification measures E50 top-label correctness before action gating. Acceptance/end-to-end action success measures the post-E40 routed action path. Accepted-action precision measures correctness only among accepted/executed commands. Safe rejection measures whether non-executed cases avoided routed actions. Return-to-listening measures runtime loop recovery.

## Physical Pi Status

The documented physical Pi validation is the established final benchmark evidence. Repository packaging/static validation should not be described as a new physical Pi revalidation unless the physical runtime is actually rerun and documented.
