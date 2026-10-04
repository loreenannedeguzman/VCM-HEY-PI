# Historical Deployment Readiness Report - Superseded

This file is retained only as historical deployment documentation.

It is not the current GitHub deployment quickstart and should not be used to identify the runnable final package.

For the current runnable repository package, use:

- repository root `README.md`
- repository root `4a - DEPLOYMENT_QUICKSTART.md`
- `4b - DEPLOYMENT/vcm_pi_package/README_PI_DEPLOYMENT.md`
- `4b - DEPLOYMENT/vcm_pi_package/PACKAGE_MANIFEST.md`

## Current Runtime Identity

| Component | Current final deployment value |
|---|---|
| Wake model | `E37_TARGETED_COLOR_VOLUME_FIX` |
| Command model | `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT` |
| Confidence policy | `configs/e50_revised_vocab_e40_thresholds.json` |
| Command vocabulary | 19 labels, with `LIGHT_DIM` and without final command class `COLOR` |
| GUI | `scripts/vcm_touchscreen_gui.py` |
| Shell launcher | `scripts/run_vcm_touchscreen_gui.sh` |

## Supersession Note

Earlier deployment-readiness notes referred to pre-final package states and older model generations. The current GitHub deployment package is the E37/E50/E40 stack listed above.

This replacement note does not rerun physical Raspberry Pi validation, alter model weights, change thresholds, or modify benchmark results. It only prevents stale historical E33-era deployment wording from being mistaken for current run instructions.
