# Integrity Overview

## Purpose

This section records the frozen identity, provenance boundaries, and package-integrity controls for the final E50 system documentation.

## Integrity Chain

The package separates four evidence classes:

1. Frozen runtime identity: E37, E50, E40, vocabulary, thresholds, runner, and local action/response behavior.
2. Dataset provenance: E50 command-model lineage and separate E37 wake-recording lineage.
3. Validation/results evidence: final benchmark, latency/RTF, bounded FAR, and E51 comparison.
4. Package documentation integrity: manifests and change records created during documentation compilation.

## Canonical Identity Summary

| Component | Identity |
|---|---|
| E50 command model | E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT |
| E37 wake model | E37_TARGETED_COLOR_VOLUME_FIX |
| E40 policy | E40_NON_LED_COMMAND_GUARDRAIL_THRESHOLDS |
| Final vocabulary | 19 commands, LIGHT_DIM included and COLOR excluded from final E50 labels |
| Wake threshold | 0.90 |
| Command default threshold | 0.90 |
| Runtime launcher | scripts/run_vcm_touchscreen_gui.sh |

## Non-Modification Boundary

This documentation compilation did not change source code, datasets, manifests, models, weights, thresholds, runtime configuration, Pi files, training, benchmarks, or Git state.

