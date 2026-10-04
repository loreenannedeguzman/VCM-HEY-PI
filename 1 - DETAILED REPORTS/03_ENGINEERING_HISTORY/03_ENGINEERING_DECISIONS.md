# Engineering Decisions

This document curates the major decisions that shaped E50. The raw historical decision record is preserved separately as `reference/PROJECT_DECISIONS.md`. [EH-03]

## 1. Requirements-Driven Decisions

The project was designed as a local Raspberry Pi voice-command system. The historical decision record states that final inference must not depend on internet access. This drove the project toward local audio capture, local feature extraction, local CNN inference, deterministic local routing, and local response behavior. [EH-03]

The project therefore did not adopt a cloud ASR service, an LLM-based command parser, or an internet-dependent inference path as the final system architecture.

## 2. Dataset Decisions

The E50 command model used a project-specific training construction rather than a claim that every row came directly from the class Gold Dataset. The final documented E50 training manifest contains 16,100 rows: 13,070 active-project rows, 2,800 Dataset2/VCM_BALANCED rows, and 230 E41 reconstructed adaptation rows. [EH-04]

The engineering decision was to use selected collective-derived/project-local command material while preserving explicit separation for project-specific adaptation data. This kept the command model evidence auditable without claiming byte-for-byte identity with the entire collective Gold Dataset.

E37 wake-gate recordings are a separate provenance branch from the E50 command-model dataset. The recovered Pi manifest documents 99 project-specific wake-stage recordings for Hey Pi-related wake development, not Gold Dataset rows and not E50 command-model training rows. [EH-05]

## 3. Model Decisions

The command-recognition path used a small CNN over fixed log-Mel features rather than a large speech-recognition or language-model system. The records describe E41 as a small CNN with a 4-second log-Mel representation and 66,483 parameters, and they document later controlled experiments around architecture and dataset changes. [EH-03] [EH-04]

E50 became the final command model because it provided the best documented balance for the final command-classifier role among the late-stage alternatives considered. E51 was kept as comparison evidence rather than replacing E50. [EH-04]

## 4. Wake-Gate Decisions

The project separated wake detection from command classification. E37 detects the wake phrase and opens the command window; it does not directly execute command actions. [EH-01] [EH-04]

The recovered E37 audit now directly establishes the project-specific Hey Pi recording set:

- 99 total recordings
- 50 `WAKE` / `hey pi` recordings
- 15 `UNKNOWN` recordings
- 14 `COLOR` recordings
- 14 `VOLUME_UP` recordings
- 3 `LIGHT_ON` recordings
- 3 `PLAY_MUSIC` recordings
- 64 adaptation-designated recordings
- 35 holdout-designated recordings
- 4-second duration
- 16 kHz sample rate
- input device `plughw:2,0`

The decision record should not be read as proving that all 99 rows were used in final E37 training. The recovered evidence establishes recording provenance and manifest structure, while the exact final E37 training subset remains unestablished. [EH-05]

## 5. Safety and Rejection Decisions

E40 was preserved as the confidence/rejection policy between the command classifier and deterministic router. This decision separated three concepts:

- the CNN predicts a label;
- E40 decides whether the prediction is accepted or rejected;
- the deterministic router maps an accepted label to a predefined local action.

The records show that rejected predictions are part of the safety behavior, not merely missing coverage. E40 can reduce wrong actions, but it does not fix overfitting or classifier confusion. [EH-03] [EH-04]

## 6. Deployment Decisions

The final deployment targeted the Raspberry Pi as an offline system. The frozen system used local model artifacts, local configuration, deterministic routing, local response audio, and return-to-listening behavior. [EH-01] [EH-04]

The records also preserve the decision to keep GPIO disabled in the frozen stack and to treat local response/action behavior as deterministic deployment behavior rather than learned model behavior. [EH-01] [EH-04]

## 7. Vocabulary Decisions

The final E50 command vocabulary contains 19 labels. The late-stage records identify the revised final vocabulary as using `LIGHT_DIM` and no longer using `COLOR` as the final E50 command label. [EH-01] [EH-04]

This vocabulary revision is part of the final E50 command-model definition. It should not be confused with the recovered E37 wake-recording manifest, which contains targeted `COLOR` examples as wake-stage probes in the E37 recovery context. [EH-05]

## 8. Final Freeze Decisions

The final freeze preserved the E37 wake model, E50 command model, E40-compatible policy, final vocabulary, thresholds, preprocessing, routing/action semantics, response behavior, and deployment configuration. [EH-01] [EH-04]

After this point, later packaging and interface work was allowed only when it did not change the frozen recognition/action core. This is why the DUi/GUI is documented as a post-freeze interface layer rather than a new E50 model.

## 9. Decisions Explicitly Not Taken

The reviewed records do not support treating the following as final E50 decisions:

- using a cloud or internet-dependent recognizer as the final command system;
- replacing E50 with E53;
- treating E53/VCM2 as an E50 development stage;
- claiming E37 used the collective Gold Dataset;
- claiming the recovered 99-row E37 recording set is the exact final E37 training set;
- silently tuning E40 thresholds after freeze;
- using a command whitelist to inflate benchmark results;
- treating the post-freeze DUi/GUI as a retrained VCM or new command classifier;
- changing final benchmark results after freeze.
