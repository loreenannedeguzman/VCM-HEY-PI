# 08 - Post-Freeze Enhanced DUi / GUI

## Boundary Statement

The enhanced DUi/GUI is a post-freeze interface/deployment layer around the frozen E50 VCM core. It is not a new E50 model, not a retrained recognizer, not a threshold change, and not a replacement for E37, E50, E40, routing, or response assets. [REF-01] [REF-05] [REF-06]

## Why It Was Added

The GUI was added to make operator-facing operation practical on the Raspberry Pi touchscreen/desktop: local START, STOP, and STATUS controls; duplicate-runtime prevention; visible last-command/action/response status; and clean stop behavior. [REF-05] [REF-06]

## What It Provides

The package manifest describes `scripts/vcm_touchscreen_gui.py` as a native Tkinter touchscreen controller for START, STOP, and status display. It launches the existing E37+E50 wake-wait runtime and does not contain recognition logic. [REF-06]

The deployment README states that the GUI starts `scripts/pi_wake_voice_control_demo.py` in continuous mode, prevents duplicate starts, stops the child runtime cleanly, and reads the latest result JSON from its evidence directory to display last command, action, and response status. [REF-05]

## How It Interfaces With The Frozen VCM

The shell launcher sets runtime environment/device defaults, then runs the GUI script with arguments including microphone device, evidence directory, wake retry behavior, wait-for-wake mode, and response audio device. [REF-15]

```text
DUi / GUI
  -> starts pi_wake_voice_control_demo.py
  -> passes device/evidence/wake-wait/audio-device arguments
  -> reads latest result JSON for display
  -> sends stop/cleanup to child runtime
```

## What Remains Frozen

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

Evidence: [REF-01] [REF-05] [REF-06] [REF-07] [REF-08]

## GUI-Specific Behavior

GUI-specific behavior includes START/STOP controls, status display, duplicate-runtime prevention, child-process management, and reading result JSON for display. These are interface/runtime-shell behaviors, not model behaviors. [REF-05] [REF-06]

## Launch / Use

The operator-facing flow is: open `VCM Offline`, press `START LISTENING`, say `Hey Pi`, speak a command, observe the local action/response, repeat without restarting, and press `STOP VCM` when finished. [REF-03]

## Measurements And Evidence Boundary

Previously reported E50 benchmark results remain measurements of the frozen VCM core unless a measurement explicitly names the GUI. The final report states that GUI usability and telemetry work do not become benchmark evidence, accuracy evidence, or proof of improved model performance. [REF-01]

Not established in the reviewed project evidence: production GUI launch-to-ready timing and broad GUI-specific performance metrics. [REF-03]

## What Not To Claim

Do not describe the DUi/GUI as a new E50 version, new recognizer, new model, threshold tuning change, command whitelist, evidence of improved model accuracy, or replacement for the frozen benchmark.

