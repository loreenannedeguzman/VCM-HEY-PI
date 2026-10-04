# Development Timeline

## 1. Requirements and Initial Baselines

The project began as an offline Raspberry Pi voice-command system. The historical decision record states that final inference could not depend on internet access, which led the project toward local audio capture, local feature extraction, local CNN inference, deterministic command routing, and local response behavior. [EH-03]

Early work used baseline experiments to verify the audio-processing and classifier path before committing to the final deployment stack. The E21 CNN baseline became an important early reference point: it showed that the CNN approach could learn the command task, but it also exposed accepted-command precision risk under confidence filtering. [EH-03] [EH-04]

What changed afterward: the project continued beyond baseline accuracy and began treating confidence behavior, accepted-wrong actions, and Raspberry Pi behavior as separate engineering criteria rather than assuming offline classifier accuracy was sufficient.

## 2. Real-Microphone / Raspberry Pi Validation

The project then moved from laptop/offline evidence toward real microphone and Raspberry Pi validation. E23 is documented as a targeted real-microphone light-command adaptation: it improved held-out real-microphone light behavior relative to E21, but lowered official validation macro-F1, so E21 remained the general validation baseline while E23 became a deployment-focused candidate for further microphone testing. [EH-01] [EH-02] [EH-04]

This stage revealed that model behavior in packaged or live Pi conditions could differ from offline validation. The records describe Phase C as a frozen diagnostic baseline and later Raspberry Pi validation phases as evidence for deployment behavior rather than only model-file accuracy. [EH-03] [EH-04]

What was learned: real-microphone and deployment behavior had to be measured directly. A model that looked acceptable in one offline context could still require deployment recovery, confidence analysis, or packaging correction.

## 3. Deployment Mismatch and Recovery

The project records show repeated recovery attempts after deployment mismatch was identified. E43 and E44 were targeted recovery candidates, but the decision record states that they did not satisfy the intended recovery criteria and did not supersede E41. E45 also failed to improve the overall safety/performance tradeoff because it increased accepted-wrong behavior under the same E40 policy. [EH-03]

What changed afterward: E41 remained the current evidence-supported candidate while the project shifted toward controlled diagnosis of classifier regressions, confidence-policy effects, and future experiment boundaries. [EH-03] [EH-04]

## 4. Wake-Gate Development

The wake gate became a separate stage from command recognition. E37, named `E37_TARGETED_COLOR_VOLUME_FIX`, became the wake-gate model used by the final E50 system. The final wake phrase is `Hey Pi`, and the wake gate precedes command capture rather than replacing the command classifier. [EH-01] [EH-04] [EH-05]

Recovered Raspberry Pi evidence now establishes the project-specific Hey Pi recording set associated with E37 development:

| Recording fact | Established value |
|---|---:|
| Manifest path | `/home/loreenanne/vcm_pi_package/pi_validation/wake_validation_hey_pi/manifest.csv` |
| Total recordings | 99 |
| `WAKE` / `hey pi` | 50 |
| `UNKNOWN` | 15 |
| `COLOR` | 14 |
| `VOLUME_UP` | 14 |
| `LIGHT_ON` | 3 |
| `PLAY_MUSIC` | 3 |
| Adaptation-designated recordings | 64 |
| Holdout-designated recordings | 35 |
| Duration | 4 seconds |
| Sample rate | 16 kHz |
| Input device | `plughw:2,0` |

Critical qualification: the recovered Pi manifest establishes the existence and composition of the project-specific Hey Pi recording set associated with E37 development. It does not independently establish the exact subset used in the final E37 training run, nor the full E37 training configuration. [EH-05]

## 5. Command Recognition Recovery

E41 became a major command-recognition recovery point. The decision record describes E41 as the strongest candidate in the relevant comparison period, while later experiments such as E46 and E47 were rejected because they introduced regressions or accepted-wrong actions under frozen E40 behavior. [EH-03] [EH-04]

The project then investigated whether architecture, data mixture, or confidence policy changes should be considered. The records show that changes were evaluated with explicit controls: labels, preprocessing, E40 thresholds, router/actions, and protected evaluation artifacts were not to be silently changed. [EH-03] [EH-04]

## 6. Safety and Confidence Guardrails

E40 became the confidence/rejection policy used to decide whether an E50 command prediction should be accepted or rejected before deterministic routing. The historical record treats E40 as a safety guardrail rather than a model that fixes classifier overfitting or command confusion. It can suppress uncertain predictions, reducing wrong actions at the cost of lower accepted-command coverage. [EH-03] [EH-04]

What changed afterward: the project evaluated models not only by raw classification but also by accepted-correct, accepted-wrong, rejection behavior, and action-safety consequences.

## 7. E50 Final Model Development

E50 was developed as the revised final command model after earlier candidates and recovery attempts. The final command vocabulary contains 19 labels and uses `LIGHT_DIM` rather than the earlier `COLOR` label. The final training manifest is documented as 16,100 rows: 13,070 active-project rows, 2,800 Dataset2/VCM_BALANCED rows, and 230 E41 reconstructed adaptation rows. [EH-01] [EH-04]

E51 was trained/evaluated as a comparable fresh-initialization baseline. The project records state that E51 was not selected as the final command model because its tradeoff was less favorable for final project continuity, despite some safety advantages in broader Dataset2/combined testing. [EH-04]

## 8. Final Pi Validation

The final Pi validation phase measured the frozen integrated stack rather than reopening model development. The record identifies the final benchmark evidence directory as `pi_validation/e50_bn_close_item16_final_benchmark_20260930_105703` and notes that Item 16 was benchmark recording/reporting only: E37, E50, E40, thresholds, router, response assets, GUI behavior, runtime behavior, microphone configuration, and audio configuration were unchanged. [EH-01] [EH-04]

The final benchmark results are not revalidated here. In historical terms, they served as the evidence basis for freezing the system and for reporting limitations honestly.

## 9. Final Freeze

After final validation and evidence audit, the E50 project was frozen around the integrated E37 + E50 + E40 stack. The freeze preserved:

- E37 wake model
- E50 command model
- E40-compatible confidence/rejection policy
- final 19-label vocabulary
- frozen thresholds
- deterministic router/action behavior
- local response behavior
- Raspberry Pi deployment configuration

The historical record repeatedly states that later packaging, GUI, response-presentation, and reporting work did not modify E37, E50, E40, thresholds, preprocessing, vocabulary, routing, or action semantics. [EH-01] [EH-04]

## 10. Post-Freeze DUi

The enhanced DUi/GUI work belongs after the core freeze. Its role is an interface/deployment layer around the frozen VCM core:

```text
FROZEN E50 VCM CORE
        |
        | unchanged
        v
POST-FREEZE ENHANCED DUi / GUI
```

The DUi is not a new E50 model, not a retrained command classifier, and not a replacement for E37 or E40. Its detailed behavior belongs in `02_FINAL_SYSTEM/08_POST_FREEZE_DUi.md`.
