# Final Freeze Transition

## Pre-Freeze Development State

Before E50 was frozen, the project was still in an iterative engineering state. The records show baseline command models, Raspberry Pi validation, recovery attempts, wake-gate development, confidence-policy analysis, dataset/provenance controls, and final model comparisons. [EH-01] [EH-02] [EH-03] [EH-04]

Several candidates were rejected or retained only as evidence because they did not improve the overall tradeoff. For example, E43, E44, E45, E46, and E47 are documented as recovery or follow-up experiments that did not supersede the current candidate path. [EH-03] [EH-04]

## Freeze Criteria / Basis

The final freeze was based on an integrated E37 + E50 + E40 stack that had identifiable artifacts, a final 19-label command vocabulary, a deterministic router/action layer, local response behavior, and Raspberry Pi validation evidence. [EH-01] [EH-04]

The freeze was not based on making the system look perfect. The records preserve the final benchmark limitations and explain that deployment gaps should not be attributed solely to one cause such as overfitting. [EH-04]

## Frozen E50 Stack

The frozen E50 stack consists of:

- E37 wake model;
- command capture after wake acceptance;
- log-Mel preprocessing;
- E50 command CNN;
- E40-compatible confidence/rejection policy;
- deterministic command router;
- local action behavior;
- local response audio;
- return-to-listening behavior;
- final 19-label command vocabulary;
- frozen thresholds and model/configuration identities. [EH-01] [EH-04]

The E50 CNN predicts a command label. It does not directly execute an action. E40 decides whether the predicted label is accepted. The deterministic router maps an accepted label to a local action. [EH-04]

## What Became Immutable

The historical record treats the following as frozen after final delivery:

- E37 model identity and artifact;
- E50 model identity and artifact;
- E40 policy and thresholds;
- command vocabulary;
- preprocessing representation;
- router/action semantics;
- local response behavior;
- benchmark evidence;
- final training manifest composition;
- deployment package identity. [EH-01] [EH-04]

The recovered E37 Hey Pi recording evidence strengthens the provenance record for wake-stage development, but it does not alter the frozen E37 artifact or reconstruct an exact final E37 training manifest. [EH-05]

## Validation After / Around Freeze

The final Pi benchmark was recorded as evidence for the frozen integrated stack. The logs identify Item 16 as benchmark recording/reporting only and state that it did not change E37, E50, E40, thresholds, router behavior, response assets, GUI behavior, runtime behavior, microphone configuration, or audio configuration. [EH-01] [EH-04]

The results belong in the validation and results sections. Historically, their role was to support the final freeze while preserving known limitations rather than triggering further tuning.

## Post-Freeze Changes

The enhanced DUi/GUI was added after the recognition/action core was frozen. It is an interface and deployment layer around the frozen VCM core:

```text
FROZEN E50 VCM CORE
        |
        | unchanged
        v
POST-FREEZE ENHANCED DUi / GUI
```

The DUi did not create a new E50 model, retrain the command classifier, replace E37, replace E40, change the 19-label vocabulary, or retroactively change the benchmark population. Its detailed behavior is documented in `02_FINAL_SYSTEM/08_POST_FREEZE_DUi.md`.

## What Was Explicitly Not Changed

The records repeatedly state that final packaging, GUI, prompt, response-presentation, and reporting work did not modify:

- E37 weights;
- E50 weights;
- E40 thresholds;
- preprocessing;
- command vocabulary;
- router/action semantics;
- benchmark evidence;
- final model artifacts;
- final training data;
- Raspberry Pi recognition core. [EH-01] [EH-04]

This freeze boundary is the key historical transition: after E50 became the final system, later work was allowed only as documentation, packaging, or interface/deployment support around the frozen core.
