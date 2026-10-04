# E50 Requirements Overview

## Purpose

This section records the requirements and evidence boundaries used to assess the final E50 voice-command module. It describes what the system was required to demonstrate, how those requirements map to the frozen implementation, and where supporting evidence is located.

## Scope

The requirement set is interpreted as a local, offline, fixed-vocabulary voice-command system running on Raspberry Pi hardware. The system uses a wake gate, command classifier, confidence policy, deterministic action router, local response audio, and return-to-listening behavior.

## Requirement Themes

| Theme | Requirement interpretation | Canonical package section |
|---|---|---|
| Local operation | The system operates without cloud services, ASR, or LLM inference for the command path. | 02_FINAL_SYSTEM, 06_REPRODUCTION |
| Wake-gated control | A wake phrase opens a bounded command window before command recognition. | 02_FINAL_SYSTEM, 04_VALIDATION |
| Fixed command set | The final command model recognizes the frozen 19-label vocabulary. | 02_FINAL_SYSTEM |
| Confidence safety | Predictions are filtered through E40 confidence thresholds before routing. | 02_FINAL_SYSTEM, 04_VALIDATION |
| Deterministic routing | Accepted labels map to predefined local actions; the CNN does not execute actions directly. | 02_FINAL_SYSTEM |
| Raspberry Pi deployment | The final system is documented as a Raspberry Pi 5 deployment using local microphone input and local response audio. | 06_REPRODUCTION, 08_DEMO |
| Validation evidence | Final behavior is supported by Pi trials, latency/RTF evidence, rejection checks, and benchmark summaries. | 04_VALIDATION, 05_RESULTS |
| Artifact integrity | Frozen model, policy, dataset, and documentation identities are recorded with hashes and provenance notes where established. | 07_INTEGRITY |
| Independent experiment separation | E53/VCM2 remains a separate experiment and is not used as E50 deployment evidence. | 09_INDEPENDENT_EXPERIMENT |

## Evidence Boundary

Requirements are traced to project evidence in this submission package. Where a detail is not established by reviewed project evidence, the package states that limitation instead of filling the gap by inference.
