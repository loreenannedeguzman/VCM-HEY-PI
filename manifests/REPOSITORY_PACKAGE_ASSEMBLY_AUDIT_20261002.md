# Repository Package Assembly Audit

## Scope

This audit documents the local repository-ready E50 VCM package assembled under `GITHUB_PACKAGE_FINAL_20261002`.

The package was assembled from two read-only sources:

- Frozen implementation source: `C:\Users\Loreen Anne\Documents\New project\ME2_VCM`
- Accepted documentation baseline: `C:\Users\Loreen Anne\Documents\New project\FINAL SUBMISSION VCM`

The output package is:

- `C:\Users\Loreen Anne\Documents\New project\FINAL SUBMISSION VCM\GITHUB_PACKAGE_FINAL_20261002`

No Git repository was initialized and no Git publication was performed.

## Package Purpose

The staged package is a curated repository-ready package for the final E50 VCM. It includes the final E50 runtime/deployment materials, selected final documentation, provenance and integrity evidence, validation/results documentation, and an explicitly separated independent E53 section.

It is not a dump of the full accepted submission baseline and does not include raw historical clutter, raw audio datasets, training datasets, old checkpoints, caches, extracted archives, or temporary output trees.

## Source Handling

`ME2_VCM` was used as a read-only source for the final deployable implementation artifacts.

`FINAL SUBMISSION VCM` was used as a read-only accepted documentation baseline except for creating this new staging package directory.

The accepted baseline was not modified. Package-specific corrections were made only inside `GITHUB_PACKAGE_FINAL_20261002`.

## Included Artifact Classes

| Class | Included Material | Rationale |
|---|---|---|
| Required runtime | `deployment/vcm_pi_package/scripts`, `actions`, `preprocessing`, `training`, selected configs, final model artifacts, response audio assets | Required to run the staged frozen deployment package to the extent supported by the frozen project evidence. |
| Required deployment | `README_PI_DEPLOYMENT.md`, `PACKAGE_MANIFEST.md`, `vcm_touchscreen_gui.desktop`, `requirements_pi.txt`, launch scripts | Documents and supports Raspberry Pi deployment. |
| Reproduction | `docs/06_REPRODUCTION`, root `requirements.txt`, deployment package docs | Supports deployment/reproduction from staged materials. |
| Final technical documentation | `docs/01_REQUIREMENTS` through `docs/08_DEMO`, final E50 report artifacts | Provides package-level technical disclosure and navigation. |
| Integrity / provenance | `docs/07_INTEGRITY`, `provenance`, `manifests`, repository package manifest | Provides hashes, source boundaries, provenance, and package integrity. |
| Validation / results | `docs/04_VALIDATION`, `docs/05_RESULTS`, `validation/README.md` | Separates validation method from final measured results. |
| Engineering history | curated `docs/03_ENGINEERING_HISTORY` main documents and a package-specific reference guide | Preserves the E50 engineering narrative without copying raw logs into the repository package. |
| Independent E53 | `independent_experiment/E53` | Keeps E53 / VCM2 independent from the final E50 delivery system. |

## Excluded Artifact Classes

| Excluded Class | Handling |
|---|---|
| Raw audio datasets and wake recordings | Not copied. The repository package includes response audio assets needed for local action feedback, not training/validation recording corpora. |
| Raw Pi validation dumps | Not copied as bulk evidence. Final validation/results summaries are included in documentation. |
| Historical raw logs | Not copied into `docs/03_ENGINEERING_HISTORY/reference`; the package-specific guide explains that the raw logs remain in the accepted documentation baseline. |
| Old checkpoints and superseded models | Not copied. Only final E37 and E50 deployment artifacts are staged. |
| Archives and extracted temporary output trees | Not copied. |
| Python caches and local virtual environments | Not copied. |
| Git metadata | Not copied or created. |
| Machine-local runtime outputs | Not copied except for a placeholder README in `pi_recordings` explaining that the directory is runtime output space. |

## Final Runtime Identity

| Component | Repository Package Identity |
|---|---|
| E50 command model | `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT` |
| E37 wake model | `E37_TARGETED_COLOR_VOLUME_FIX` |
| E40 policy | `E40_NON_LED_COMMAND_GUARDRAIL_THRESHOLDS`, staged as `deployment/vcm_pi_package/configs/e50_revised_vocab_e40_thresholds.json` |
| Final vocabulary | 19 labels with `LIGHT_DIM`, not final `COLOR` |
| Main staged launcher | `deployment/vcm_pi_package/scripts/run_vcm_touchscreen_gui.sh` |
| Runtime path | `deployment/vcm_pi_package/scripts/pi_wake_voice_control_demo.py` through the launcher |
| Microphone default | `plughw:2,0` |
| Response audio default | `plughw:CARD=vc4hdmi0,DEV=0` |

## Package-Specific Corrections

The accepted baseline had two minor acceptance findings. They were not changed in the accepted baseline. Package-specific handling was limited to the staged package.

| Finding | Package handling |
|---|---|
| Stale self-hash in accepted `PACKAGE_FILE_MANIFEST_20261002.md` | The repository package creates a separate `REPOSITORY_PACKAGE_MANIFEST_20261002.md` and intentionally omits its own self-hash. The accepted baseline manifest is preserved as `manifests/ACCEPTED_BASELINE_PACKAGE_FILE_MANIFEST_20261002.md`. |
| `REF-17` filename/path issue in accepted `02_FINAL_SYSTEM/reference/REFERENCE_GUIDE.md` | The staged package copy points `REF-17` to `../../../provenance/E37_HEY_PI_DATASET_EVIDENCE_RECOVERY_AUDIT_20261002.md`, matching the curated package structure. |


## Validation Checks Performed

The following documentation-only checks were performed against the staged package:

- Verified required final model artifacts exist.
- Verified the E40 threshold config exists.
- Verified the staged launcher exists.
- Verified `REF-17` resolves to the top-level provenance audit copy.
- Searched for remaining unavailable runner references.
- Searched for audience-specific submission wording.
- Searched for credential/private-key patterns.
- Searched for cache directories, `.git`, virtual environments, raw `pi_validation`, and temporary output folders.
- Searched for unsupported E37 training overclaims.
- Searched for E50/E53 and final-vocabulary boundary contradictions.

No runtime, training, inference, benchmark, Raspberry Pi execution, or Git operation was performed.

## Validation Notes

The package intentionally contains local response audio assets under `deployment/vcm_pi_package/responses_extra_loud_20260929` and `deployment/vcm_pi_package/music`, because these are deployment/action-feedback assets rather than raw training datasets.

Package-specific documentation records that the staged package uses the available frozen deployment launcher.

Search hits for words such as `production-grade`, `upgrade`, and `degraded` were reviewed as false positives for audience-specific wording.

Search hits for LaTeX `\detokenize` were reviewed as false positives for credential-pattern detection.

## Evidence Limitations Retained

- The staged package was not executed on the Raspberry Pi during this assembly task.
- The exact final E37 training-row membership remains not established.
- E37 training epochs, optimizer, validation metrics, augmentation count, and speaker/recordist count remain not established.
- The E50 command-model dataset is documented as selected collective-family/project-local material, not the entire collective Gold Dataset unchanged.
- The 230 E41 rows remain separate Pi deployment adaptation/calibration data, not Gold Dataset rows unless future evidence establishes that link.
- E53 remains an independent experiment and is not used to establish E50 implementation, deployment, or validation claims.

## Safety Statement

`ME2_VCM` was treated as a read-only frozen implementation source.

The accepted `FINAL SUBMISSION VCM` baseline was not modified outside the new `GITHUB_PACKAGE_FINAL_20261002` staging directory.

No files were created, modified, overwritten, renamed, moved, or deleted inside `ME2_VCM`.

No technical implementation was modified in the frozen source.

No model was retrained.

No runtime was executed.

No benchmark was executed.

No Raspberry Pi command was executed.

No Git operation was performed.

