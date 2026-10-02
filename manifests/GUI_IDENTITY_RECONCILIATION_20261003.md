# GUI Identity Reconciliation

## Deployable GUI

The deployable GitHub GUI is:

`deployment/vcm_pi_package/scripts/vcm_touchscreen_gui.py`

Verified SHA-256:

`ff8b64759b1efb93d88cc30a7a8f8d1cea7b49924cb72b19bc643c4a746a2c42`

This file is byte-identical to the GUI candidate already present in the accepted GitHub package copy:

`FINAL SUBMISSION VCM/GITHUB_PACKAGE_FINAL_20261002/deployment/vcm_pi_package/scripts/vcm_touchscreen_gui.py`

## Evidence of Intended Deployment Role

Accepted-package documentation identifies `scripts/run_vcm_touchscreen_gui.sh` and `scripts/vcm_touchscreen_gui.py` as the Raspberry Pi GUI launcher/status wrapper. The accepted package manifest describes `scripts/vcm_touchscreen_gui.py` as a native Tkinter touchscreen controller and local touchscreen control/status wrapper. The final-system documentation states that the GUI launches the existing E37+E50 wake-wait runtime and does not contain recognition logic.

## Passive Observability Behavior

The verified GUI is passive with respect to recognition and action decisions:

- It launches `scripts/pi_wake_voice_control_demo.py` as a subprocess.
- It passes the frozen E37/E50/E40 configuration files to that runtime.
- It observes runtime stdout for wake/command-stage status.
- It polls the latest `*_result.json` files from the evidence directory.
- It displays state prompts, last predicted command, routed action, and response playback status.
- It does not modify E37, E50, E40, thresholds, command labels, deterministic routing, response WAV assets, or benchmark definitions.

## Historical Hash Note

The earlier historical value:

`64010939760a0350ee015174d0ce40c2b78f8bb30e1c29c7b976f54c11294e8f`

is not the authoritative deployable GUI identity for this GitHub package. The package must not alter or substitute the deployable GUI to obtain that hash. The current deployable GUI identity is the verified `ff8b6475...` artifact above.

## Publication Status

The staging package documentation and manifest records identify `ff8b64759b1efb93d88cc30a7a8f8d1cea7b49924cb72b19bc643c4a746a2c42` as the deployable GUI SHA.
