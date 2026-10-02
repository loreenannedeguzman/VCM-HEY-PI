# Final Pre-Publication Staging Audit

Generated: 2026-10-03T01:38:27

## A. Staging Directory

`C:\Users\Loreen Anne\Documents\New project\VCM_GITHUB_STAGING`

## B. Final Repository Tree

Top-level directories/files: `README.md`, `DEPLOYMENT_QUICKSTART.md`, `dataset/`, `deployment/`, `docs/`, `independent_experiment/`, `manifests/`, `models/`, `provenance/`, `scripts/`, `src/`, `validation/`.

## C. Verified GUI

- Location: `deployment/vcm_pi_package/scripts/vcm_touchscreen_gui.py`
- SHA-256: `ff8b64759b1efb93d88cc30a7a8f8d1cea7b49924cb72b19bc643c4a746a2c42`
- Status: authoritative deployable GitHub GUI identity. It is byte-identical to the accepted package GUI candidate and is documented in `manifests/GUI_IDENTITY_RECONCILIATION_20261003.md`.

## D. Frozen Artifact Hashes

- E50 weights: `bc8ac64ced4305ddf43bf4de377f3cc636a764eff339cd9f92af06340c50b8ff`
- E50 normalization: `2d71873b6326d6552d7c5b1c22995ffd5132c357aaec237cb85cbd7ef739283f`
- E37 weights: `687e82e2cefa6d74cef2c0a15d28f8f6142d47d4a67e57c68c091e83fc2cebde`
- E37 normalization: `3bfa93f202dc0c241e577e5b89506f2cb6d0f35b8239297c215a7f81e970b4c7`
- E40 policy config: `a0b2495328fd5a1e0e5885e727623ba6d9f823be94cccdfd0aead77254bbb3fd`

## E. Deployment Portability Results

- Deployment scripts derive paths from their own script/package location.
- `deployment_config.example.json` provides microphone/output configuration.
- Fresh-clone deployment subtree search found no `C:\Users`, `/home/loreenanne`, `ME2_VCM`, `FINAL SUBMISSION VCM`, or Desktop E53 runtime dependency.
- Physical Raspberry Pi deployment was not rerun in this environment.

## F. Dataset Inspection Content

- Final E50 training manifest rows: 16100
- Source counts: {'e41_reconstructed_adaptation': 230, 'active_project_dataset': 13070, 'dataset2_vcm_balanced': 2800}
- Data-kind counts: {'real': 15260, 'augmented': 480, 'synthetic': 160, 'real_multi_sensor': 200}
- Final labels: ['ALARM', 'BRIGHTNESS', 'CALL', 'CREATE_REMINDER', 'LIGHT_DIM', 'LIGHT_OFF', 'LIGHT_ON', 'LIST_REMINDERS', 'MESSAGE', 'NEXT', 'PAUSE', 'PLAY_MUSIC', 'STOP', 'TEMPERATURE', 'TIME', 'TIMER', 'VOLUME_DOWN', 'VOLUME_UP', 'WEATHER']
- `COLOR` is not a final E50 label in the manifest.

## G. Dataset Files Included

- `dataset/E50_TRAINING_MANIFEST.csv`
- `dataset/DATASET_INVENTORY.md`
- `dataset/README.md`
- `dataset/VCM_MASTER_README.md`
- `dataset/VCM_BALANCED_README.md`
- `dataset/E41_ADAPTATION_README.md`

## H. Dataset Files Excluded

- Raw third-party/source audio is excluded because redistribution rights are not established in the reviewed evidence.
- Raw E37 `Hey Pi` WAVs are excluded; manifest/provenance evidence is included.

## I. Licensing and Provenance Issues

- No blanket license was added because unrestricted redistribution rights for all source data are not established.
- Third-party dataset terms remain applicable.
- Training manifest preserves original provenance fields, including historical resolved paths. Those are not runtime dependencies.

## J. Large File Audit

- Publication files: 159
- Publication bytes: 10404399
- Files greater than 50 MiB: 0
- Files greater than 100 MiB: 0
- Largest file: `dataset/E50_TRAINING_MANIFEST.csv` at 6,171,577 bytes. Suitable for ordinary Git.

## K. Security Audit

- No `.env`, private key, PAT, token, password, credential, or private certificate filenames were found in the publication set.
- No common secret/token patterns were found.
- Original private IP `10.108.25.37` was not found.
- Personal/source paths remain only as provenance/historical fields in documentation and the training manifest, not as deployment dependencies.

## L. Reference Integrity Audit

- See `REFERENCE_INTEGRITY_AUDIT.md`.
- Total references checked: 69
- Valid repository references: 53
- Historical/external references: 16
- Unresolved references: 0

## M. GUI Identity Reconciliation

- Deployable GUI path: `deployment/vcm_pi_package/scripts/vcm_touchscreen_gui.py`.
- Deployable GUI SHA-256: `ff8b64759b1efb93d88cc30a7a8f8d1cea7b49924cb72b19bc643c4a746a2c42`.
- Historical `640109...` value is not presented as the current deployable GUI identity.
- See `manifests/GUI_IDENTITY_RECONCILIATION_20261003.md`.

## N. Stale Paths Corrected

- Active E53 guide paths normalized to `independent_experiment/E53/...`.
- Active E37 audit guide paths normalized to `provenance/...`.
- Active compilation-manifest guide path normalized to `manifests/...`.
- Desktop launcher and shell launcher no longer require `/home/loreenanne`.

## O. Missing Historical Files

- `AGENT_LOG.md`, `EXPERIMENT_LOG.md`, `PROJECT_DECISIONS.md`, and `EXAM_NOTES.md` are now included in `docs/03_ENGINEERING_HISTORY/reference/`.

## P. Fresh-Clone Test

- Fresh clone directory: `C:\Users\Loreen Anne\Documents\New project\VCM_GITHUB_STAGING_CLONE_TEST\clone_20261003_013601`
- Fresh clone file count: 158
- Fresh clone verified README, quickstart, config, GUI, E50, E37, E40, and training manifest presence.
- Fresh clone verified GUI/E50/E37/E40 hashes and 16,100 manifest rows.
- Bash syntax and physical Pi launch were not tested because this Windows environment has no `bash` command and no target Pi hardware attached.

## Q. Remaining Blockers

- No Git initialization or push has occurred.
- Physical Pi deployment validation is pending.
- User must decide whether public release should retain historical personal/source paths in provenance evidence and manifest fields.

## R. Manual User Actions Required

1. Review this staging audit.
2. Create a GitHub repository manually.
3. Do not initialize it with README, .gitignore, or license.
4. Provide the repository URL and desired branch.
5. Confirm before first push.

## Safety Statement

- Protected source/submission/E53 folders were not intentionally modified.
- No training, benchmark, VCM runtime, Pi access, Git init, commit, or push was performed.
