# Deployment Artifacts

## Frozen Runtime Identities

The deployable frozen core is defined by the E37 wake model, E50 command model, E40 policy, final vocabulary, runner, thresholds, and response/action behavior documented in 07_INTEGRITY.

## Artifact Table

| Artifact | Identity / role |
|---|---|
| E37 wake weights | E37_TARGETED_COLOR_VOLUME_FIX_weights.npz |
| E37 normalization | E37_TARGETED_COLOR_VOLUME_FIX_normalization.npz |
| E50 command weights | E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT |
| E40 policy | E40_NON_LED_COMMAND_GUARDRAIL_THRESHOLDS |
| Runtime launcher | scripts/run_vcm_touchscreen_gui.sh |
| Vocabulary | 19-command E50 vocabulary with LIGHT_DIM, not COLOR |
| GPIO state | Disabled in the frozen stack |
| Response behavior | Local WAV/action response enabled |

## Packaging Note

This documentation compilation records the deployment architecture and artifact identities. It does not create a new runtime build, modify the existing package, or copy raw datasets/audio into the submission.

