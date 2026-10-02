# Reference Guide For 02_FINAL_SYSTEM

This guide resolves the internal `[REF-xx]` citations used by the `02_FINAL_SYSTEM` documentation package. The reference files are curated evidence copies only. They do not include datasets, model weights, raw audio, or benchmark reruns.

| Ref ID | Filename | Original source path | Purpose | Used by | Status |
|---|---|---|---|---|---|
| REF-01 | `REF-01_E50_DEMODAY_REPORT_PROVENANCE_ADJUSTED.md` | `FINAL SUBMISSION VCM\E50 DEMODAY REPORT.md` | Final metrics, architecture, model, deployment, and limitations summary. | All main docs | Authoritative adjusted documentation |
| REF-02 | `REF-02_E50_DATASET_PROVENANCE_ADJUSTED.md` | `FINAL SUBMISSION VCM\E50_DATASET.md` | Provenance-adjusted dataset/training explanation. | Dataset and vocabulary docs | Authoritative adjusted documentation |
| REF-03 | `REF-03_FINAL_PACKAGE_README_PROVENANCE_ADJUSTED.md` | `FINAL SUBMISSION VCM\github_package\ME2_VCM_E50_GITHUB_PACKAGE_20260930\README.md` | Package overview, deployment, vocabulary, metrics, provenance wording. | Overview, deployment, DUi docs | Authoritative adjusted documentation |
| REF-04 | `REF-04_E50_WAKE_GATE.md` | `ME2_VCM\E50_WAKE_GATE.md` | E37 wake-stage role, threshold, wake evidence limits, E37/E50 separation. | Wake gate, architecture | Authoritative supporting evidence |
| REF-05 | `REF-05_README_PI_DEPLOYMENT.md` | `ME2_VCM\deployment\vcm_pi_package\README_PI_DEPLOYMENT.md` | Raspberry Pi package behavior, final model identity, launch path, wake-gated demo, GUI, response audio. | Architecture, deployment, DUi, identity | Authoritative deployment evidence |
| REF-06 | `REF-06_PACKAGE_MANIFEST.md` | `ME2_VCM\deployment\vcm_pi_package\PACKAGE_MANIFEST.md` | Package contents, runtime scripts, GUI role, action layer, response assets. | Deployment, DUi, overview | Authoritative package evidence |
| REF-07 | `REF-07_E50_REVISED_VOCAB_E40_THRESHOLDS.json` | `ME2_VCM\deployment\vcm_pi_package\configs\e50_revised_vocab_e40_thresholds.json` | E40 policy ID, base policy, default and label-specific thresholds. | E40, identity, command model | Authoritative config evidence |
| REF-08 | `REF-08_RAW_COMMAND_ROUTER.py` | `ME2_VCM\deployment\vcm_pi_package\actions\raw_command_router.py` | Exact raw-label to intent/slot deterministic routing map. | Vocabulary/actions, architecture | Authoritative implementation evidence |
| REF-09 | `REF-09_COMMAND_ACTIONS.py` | `ME2_VCM\deployment\vcm_pi_package\actions\command_actions.py` | Local action layer behavior and action result structure. | Architecture, deployment | Authoritative implementation evidence |
| REF-10 | `REF-10_DEMO_RESPONSE_ASSETS.json` | `ME2_VCM\deployment\vcm_pi_package\configs\demo_response_assets.json` | Response WAV mapping for labels and rejection feedback. | Vocabulary/actions, deployment | Authoritative config evidence |
| REF-11 | `REF-11_PHASE_BG_TRAINING_CONFIG.json` | `ME2_VCM\results\phase_bg_e50_bg_revised_vocab_original_preserve_e41_init_20260928\PHASE_BG_TRAINING_CONFIG.json` | E50 experiment ID, preprocessing, labels, training config, parameter count. | Command model, dataset/training, identity | Authoritative training config |
| REF-12 | `REF-12_E50_MODEL_SUMMARY.txt` | `ME2_VCM\results\phase_bg_e50_bg_revised_vocab_original_preserve_e41_init_20260928\E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT_model_summary.txt` | E50 model architecture and parameter count. | Command model | Authoritative model summary |
| REF-13 | `REF-13_E50_FINAL_SHA256_MANIFEST_20260930.txt` | `ME2_VCM\E50_FINAL_SHA256_MANIFEST_20260930.txt` | Final artifact hashes for E37, E50, E40, runtime/config artifacts. | Frozen identity, wake, command model, E40 | Authoritative integrity evidence |
| REF-14 | `REF-14_E50_BENCHMARK_AUDIT.md` | `ME2_VCM\E50_BENCHMARK_AUDIT.md` | Benchmark interpretation and separation of metrics/limitations. | Architecture, E40, dataset caveats | Authoritative audit evidence |
| REF-15 | `REF-15_RUN_VCM_TOUCHSCREEN_GUI.sh` | `ME2_VCM\deployment\vcm_pi_package\scripts\run_vcm_touchscreen_gui.sh` | GUI launcher defaults and runtime arguments. | Deployment, DUi | Authoritative launcher evidence |
| REF-16 | `REF-16_ACTION_LAYER_DESIGN.md` | `ME2_VCM\deployment\vcm_pi_package\actions\ACTION_LAYER_DESIGN.md` | Action layer design context and limitations. | Vocabulary/actions, architecture | Supplementary design evidence |
| REF-17 | `../../../provenance/E37_HEY_PI_DATASET_EVIDENCE_RECOVERY_AUDIT_20261002.md` | `provenance/E37_HEY_PI_DATASET_EVIDENCE_RECOVERY_AUDIT_20261002.md` | Read-only recovery audit documenting the recovered Raspberry Pi `Hey Pi` wake-recording manifest, 99 recording rows, 50 `WAKE` / `hey pi` rows, 64 adaptation-designated rows, 35 holdout-designated rows, audio properties, E37 artifact hashes, and retained E37 training-lineage limitations. | Wake gate, architecture, dataset boundary, deployment, identity | Authoritative recovered E37 provenance audit |

## Selection Rationale

The reference folder intentionally contains a small set of files sufficient to substantiate the final system documentation: final report/dataset/package summaries, wake-gate evidence, deployment/package evidence, E40 threshold config, deterministic routing/action evidence, response asset config, model training config and model summary, final hash manifest, benchmark audit, GUI launcher evidence, and the separate recovered E37 `Hey Pi` provenance audit.

Excluded on purpose: datasets, training manifests, raw audio, model weights, evidence archives, generated benchmark dumps, and historical experiment logs not needed to understand the final frozen system.

