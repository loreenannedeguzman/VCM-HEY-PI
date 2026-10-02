# E50 Engineering History

## Purpose

This folder documents how the E50 Voice Command Machine became the final frozen delivery system. It is an engineering-history section, not a replacement for the final-system manual, validation section, results section, or reproduction instructions.

The main question answered here is:

> How did E50 evolve from requirements and experiments into the final frozen Raspberry Pi voice-command system?

## Scope

This section covers the E50 development path only. It summarizes requirements-driven decisions, experiment results, recovery work, wake-gate development, confidence guardrails, command-model revision, final validation, and the transition into the frozen E50 delivery state.

E53/VCM2 is not incorporated into this E50 history. If E53 is mentioned at all, it is only to preserve the boundary that E53 was a separate experiment and not a replacement for E50.

## Development-to-Freeze Narrative

The reviewed project evidence supports the following high-level development path:

```text
Assignment requirements
    ->
Initial baselines
    ->
Real-microphone / Raspberry Pi validation
    ->
Deployment mismatch discovery
    ->
Recovery / adaptation
    ->
Wake-gate development
    ->
Confidence / safety guardrails
    ->
Command-model revision
    ->
Pi validation and failure analysis
    ->
Final E50 freeze
    ->
Post-freeze DUi/interface layer
```

The final E50 system was therefore not an isolated checkpoint. It was the result of repeated comparison between offline results, Raspberry Pi recordings, live validation behavior, confidence-policy behavior, and deployment constraints. The final freeze preserved the E37 wake model, the E50 command CNN, the E40 confidence/rejection policy, the 19-label command vocabulary, deterministic routing/action behavior, and the local Raspberry Pi deployment stack. [EH-01] [EH-02] [EH-03] [EH-04]

## Historical Evidence

The historical record for this folder is based primarily on four copied reference files:

- [EH-01] `reference/AGENT_LOG.md`
- [EH-02] `reference/EXPERIMENT_LOG.md`
- [EH-03] `reference/PROJECT_DECISIONS.md`
- [EH-04] `reference/EXAM_NOTES.md`

The recovered E37 Hey Pi evidence is supported by the separate submission audit:

- [EH-05] `E37_HEY_PI_DATASET_EVIDENCE_RECOVERY_AUDIT_20261002.md`

That audit establishes the existence and composition of the recovered project-specific Hey Pi recording set, while preserving the limitation that the exact final E37 training subset is not independently reconstructed.

## Relationship to the Other Submission Sections

This folder explains the engineering path. Other submission sections remain the primary home for other kinds of information:

- `02_FINAL_SYSTEM` describes the final frozen system architecture and components.
- `04_VALIDATION` documents validation methodology and evidence.
- `05_RESULTS` reports final benchmark and performance results.
- `06_REPRODUCTION` explains reproduction and deployment procedures.
- `07_INTEGRITY` records hashes, manifests, and freeze controls.
- `08_DEMO` provides operational demo guidance.
- `independent_experiment/E53` keeps E53 separate from E50.

This section may reference those topics, but it avoids duplicating their detailed tables, procedures, and benchmark records.

## Evidence Limitations

The available records establish the main E50 engineering sequence and final freeze boundary. Some details remain limited by the available evidence:

- The recovered E37 recording manifest establishes 99 Hey Pi wake-stage recordings and their adaptation/holdout designations, but it does not prove which exact rows were included in the final E37 training run. [EH-05]
- The E37 training epochs, optimizer, validation metrics, augmentation count, exact speaker/recordist count, and complete row-to-checkpoint mapping are not established in the recovered E37 evidence. [EH-05]
- Some intermediate experiments were preserved as rejected or diagnostic artifacts rather than promoted systems. Their purpose here is historical explanation, not final-system revalidation. [EH-03] [EH-04]
- Final benchmark numbers are summarized only where needed for historical context. The authoritative results belong in the results and validation sections.

