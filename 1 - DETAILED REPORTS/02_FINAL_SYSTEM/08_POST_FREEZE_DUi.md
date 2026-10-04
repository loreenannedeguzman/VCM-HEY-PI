# Post-Freeze Enhanced DUi / GUI

## Boundary Statement

The enhanced DUi/GUI is a post-freeze interface and deployment shell around the frozen E50 VCM core. It is not a new E50 model, not a retrained recognizer, not a threshold change, not a command whitelist, and not a replacement for E37, E50, E40, routing, or response assets.

## What It Does

The GUI provides operator-facing controls and visibility:

- START and STOP controls for the runtime;
- status display for wake/command states;
- duplicate-runtime prevention;
- child-process management and clean stop behavior;
- display of recent command/action/response status from runtime result JSON;
- passive telemetry around wake, command, routing, action, response, and return-to-listening behavior.

## What It Does Not Do

The GUI does not change:

- E37 wake model;
- E50 command model;
- E40 threshold policy;
- wake threshold;
- command default threshold;
- label-specific thresholds;
- 19-label vocabulary;
- deterministic router/action semantics;
- response WAV mapping;
- final benchmark metrics.

## Interface Relationship

```text
GUI / DUi
  -> launches existing wake-gated runtime
  -> passes device/evidence/wake-wait/audio options
  -> reads result JSON for display
  -> stops child runtime when requested
```

Recognition remains in E37 and E50. Acceptance remains in E40. Action semantics remain in the deterministic router/action layer. Response playback remains the configured local WAV map.

## Evidence Boundary

Post-freeze GUI usability and telemetry work should not be retroactively counted as E50 benchmark evidence, accuracy evidence, or proof of improved model performance. Previously reported benchmark results remain measurements of the frozen VCM core unless a measurement explicitly names the GUI. GUI launch-to-ready latency and broad GUI-specific performance metrics are not established in the reviewed evidence.
