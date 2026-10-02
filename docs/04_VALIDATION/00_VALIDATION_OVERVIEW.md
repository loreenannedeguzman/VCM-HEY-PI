# E50 Validation Overview

## Purpose

This section explains how the frozen E50 voice-command module was validated and what each validation evidence type establishes. Detailed quantitative results are centralized in 05_RESULTS.

## Validation Scope

Validation covers the frozen E50 core: E37 wake gate, command capture, log-Mel preprocessing, E50 CNN command classifier, E40 confidence/rejection policy, deterministic routing, local action/response behavior, and return-to-listening behavior.

The post-freeze DUi/GUI is an interface layer around the frozen core. GUI-specific behavior is documented separately and does not retroactively change the frozen E50 benchmark.

## Validation Layers

| Layer | Purpose | Evidence boundary |
|---|---|---|
| Wake-gated Pi benchmark | Exercise wake, command classification, confidence filtering, action routing, UNKNOWN/no-action behavior, and return-to-listening. | 20-trial population: 19 valid command labels plus 1 UNKNOWN/no-action. |
| Latency and RTF | Measure command-model inference and command-pipeline timing. | CNN latency, CNN RTF, command-pipeline RTF, and local response playback-start timing are reported with defined boundaries. |
| Safety/rejection checks | Confirm that low-confidence or out-of-scope cases do not produce unsafe local actions. | Bounded command-window FAR is reported only for the tested prompt set. |
| E51 baseline comparison | Compare E50 against a fresh-initialization offline baseline. | E51 is not a second Pi deployment benchmark. |
| E37 recording recovery | Establish recovered Hey Pi wake-recording evidence. | Recording existence and composition are established; exact final E37 training rows are not established. |

## What Validation Does Not Claim

The final benchmark is not a broad population study, not a full environmental false-accept-rate campaign, and not a proof that every possible acoustic condition was covered. It documents the measured final delivery behavior under the recorded validation protocol.
