# Reproduction and Deployment Overview

## Purpose

This section explains how the frozen E50 system is represented for deployment and what can be reproduced from the package evidence. It does not rerun training, inference, benchmarks, or the Pi runtime.

## Deployment Target

| Item | Value |
|---|---|
| Hardware target | Raspberry Pi 5 |
| Pi user | loreenanne |
| Pi IP documented for deployment | Deployment-specific local-network address; configure for the target Raspberry Pi. |
| Pi package root | ~/vcm_pi_package |
| Core runtime launcher | scripts/run_vcm_touchscreen_gui.sh |
| Microphone input | plughw:2,0 |
| Response audio output | plughw:CARD=vc4hdmi0,DEV=0 |

## Reproduction Boundary

The final E50 runtime behavior is documented through frozen identities, deployment notes, validation evidence, and result summaries. Complete reconstruction of E37's final training run is not established because the recovered evidence does not include a dedicated final E37 training manifest, epochs, optimizer, validation metrics, augmentation count, or full row-to-checkpoint mapping.

