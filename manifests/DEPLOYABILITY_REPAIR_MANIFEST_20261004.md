# Deployability Repair Manifest - 2026-10-04

## Scope

Package-only repair of `GITHUB_PACKAGE_FINAL_20261002` so the GitHub repository package can be downloaded and run without depending on the frozen source project or accepted submission folder at runtime.

## Current Runtime Location

```text
4b - DEPLOYMENT/vcm_pi_package
```

## Reason

A read-only deployability audit found that `predict_wav_pi.py` loads label maps from:

```text
results/tables/{experiment_id}_labels.json
```

The deployment package contained E37/E50 weights, normalization artifacts, configs, runtime scripts, GUI code, and response WAVs, but did not contain the required E37 and E50 label JSON files. Without those files, the predictor could not map CNN output indices to labels.

## Files Added

| File | Purpose | SHA-256 |
|---|---|---|
| `4b - DEPLOYMENT/vcm_pi_package/results/tables/E37_TARGETED_COLOR_VOLUME_FIX_labels.json` | E37 wake-model output-index to label map. | `6534516D90FBB5A58401007EC322E71563AEC27D46B55A71879B10C94AF9D0A7` |
| `4b - DEPLOYMENT/vcm_pi_package/results/tables/E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT_labels.json` | E50 command-model output-index to label map. | `75052BFEBACCCF72BACA079AB0427CC7C2216D4E47326D4FD23123FBEDC24F0F` |
| `README.md` | Standard GitHub landing page copied from the project summary and updated with a direct deployment quickstart. | See current repository manifest. |
| `4a - DEPLOYMENT_QUICKSTART.md` | Fresh-clone Raspberry Pi setup and launch instructions. | See current repository manifest. |

## Documentation Updated

| File | Change |
|---|---|
| `3 - FINAL_PROJECT_SUMMARY.md` | Updated navigation links from old `docs/` paths to the current `1 - DETAILED REPORTS/` layout. |
| `4b - DEPLOYMENT/vcm_pi_package/README_PI_DEPLOYMENT.md` | Replaced stale deployment guidance with current E37/E50/E40 runtime setup and launch instructions. |
| `4b - DEPLOYMENT/vcm_pi_package/PACKAGE_MANIFEST.md` | Replaced stale package listing with the current runnable deployment package contents. |
| `4b - DEPLOYMENT/vcm_pi_package/REPORT_PI_DEPLOYMENT_READINESS.md` | Marked as historical/superseded so old E33-era wording is not mistaken for the current runtime. |
| `4b - DEPLOYMENT/vcm_pi_package/vcm_touchscreen_gui.desktop` | Updated optional desktop launcher path from a personal path to the documented repository clone path. |

## Static Validation After Repair

| Check | Result |
|---|---|
| Required runtime/package files present | PASS |
| E50 label count | 19 |
| E50 includes `LIGHT_DIM` | PASS |
| E50 excludes final command class `COLOR` | PASS |
| E37 includes `WAKE` and `UNKNOWN` | PASS |
| All mapped response WAV files present | PASS |
| Python cache files in deployment package | None found |
| E50 weights SHA unchanged | `BC8AC64CED4305DDF43BF4DE377F3CC636A764EFF339CD9F92AF06340C50B8FF` |
| E37 weights SHA unchanged | `687E82E2CEFA6D74CEF2C0A15D28F8F6142D47D4A67E57C68C091E83FC2CEBDE` |
| E40 config SHA unchanged | `A0B2495328FD5A1E0E5885E727623BA6D9F823BE94CCCDFD0AEAD77254BBB3FD` |
| GUI SHA unchanged | `FF8B64759B1EFB93D88CC30A7A8F8D1CEA7B49924CB72B19BC643C4A746A2C42` |

## Runtime Boundary

The repaired GitHub package is intended to run from the repository clone path after installing Raspberry Pi dependencies and adjusting local ALSA device names if required.

This repair did not rerun physical Raspberry Pi validation.

## Technical Boundary

No model was retrained. No threshold was tuned. No benchmark was rerun. No runtime script, model architecture, model weight, normalization artifact, response WAV, dataset, E37 model, E50 model, E40 policy, or E53 experiment artifact was modified.
