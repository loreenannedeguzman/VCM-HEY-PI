# E53 Independent Experiment

## 1. Purpose and Research Question

E53 is an independent experimental branch and is not part of the frozen E50 final-delivery implementation. E53 results do not modify, replace, or retroactively change the E50 model, benchmark, deployment, or final system identity.

The central E53 research question was whether a separately constructed, requirement-complete, 20-class offline command dataset and compact non-ASR acoustic CNNs could produce a more defensible command recognizer than the established E53 control. The final bounded question, tested in LOG025, was whether alternative acoustic representations, specifically MFCC and PCEN, improved recognition relative to the frozen LOG011 log-Mel control while holding the dataset, model capacity, optimizer, learning rate, batch size, random seed, early stopping rule, and evaluation splits fixed.

E53 was therefore not a deployment rewrite of E50. It was an experimental investigation of data construction, UNKNOWN/SILENCE treatment, acoustic feature representation, and failure modes.

## 2. Relationship to E50

E50 is the frozen final Raspberry Pi 5 VCM delivery system. It includes E37 wake detection, E50 command CNN inference, E40 confidence guardrails, deterministic action routing, response WAV playback, and physical Pi validation.

E53 is a separate offline classifier/model-development investigation. It does not contain or replace the E50 wake gate, E40 policy, router, GUI, Pi runtime, response layer, or final benchmark. Its results can inform engineering understanding, but the recovered E53 evidence does not establish that E53 beat E50 or should replace E50.

## 3. Hypotheses / Experimental Questions

The E53 record does not always state hypotheses in formal statistical language, so this report preserves the documented engineering objective for each phase.

| ID | Documented experimental question | Assessment | Evidence |
|---|---|---|---|
| H1 | Did the initial model lack sufficient capacity? | Supported | LOG010 improved over LOG009, and LOG011 capacity increase produced the strongest established E53 control. |
| H2 | Was SILENCE/background distribution limiting performance? | Partially supported | LOG012 found SILENCE source specificity and LOG013 improved SILENCE while creating other tradeoffs. |
| H3 | Was ordinary command class-count imbalance causing paired-class confusion? | Not supported | LOG014 found target classes had equal 840/105/105 train/validation/test counts. |
| H4 | Were source-group/provenance effects contributing to failures? | Mixed | LOG017 supported association; LOG019 source-group exposure regressed global performance. |
| H5 | Could representation/head changes improve separability? | Not supported in the tested head; mixed for representation | LOG021 severely regressed; LOG025 MFCC/PCEN gave tradeoffs. |
| H6 | Could semantic/vocabulary ambiguity explain some failures? | Partially supported | LOG022/LOG023 found incomplete transcript and semantic evidence for several classes. |
| H7 | Could authoritative phrase provenance be recovered? | Inconclusive | LOG024 recovered partial evidence but left important gaps. |
| H8 | Could MFCC or PCEN improve classification over log-Mel? | Mixed / inconclusive | MFCC improved some aggregate metrics but hurt UNKNOWN/SILENCE; PCEN improved SILENCE but hurt macro and operational macro-F1. |

## 4. E53 Dataset

E53 used `E53_DATASET_V1`, a frozen manifest-driven 20-class dataset. It was verified from the E53 source project at `C:\Users\Loreen Anne\Documents\New project\ME2_VCM\E53`.

| Property | Value |
|---|---:|
| Dataset name | `E53_DATASET_V1` |
| Frozen manifest | `data\manifests\E53_FINAL_DATASET_MANIFEST.csv` |
| Manifest SHA-256 | `0756c5d0274b95e663f30e5f13f0ffd326a8e854bfc6e06c12c17431cd31bdd8` |
| Rows | 24,706 |
| Classes | 20 |
| Operational command classes | 18 |
| Safety/background classes | `UNKNOWN`, `SILENCE` |
| Train / validation / test | 19,553 / 2,544 / 2,609 |
| Sample rate | 16 kHz for all manifest rows |
| Channels | Mono for all manifest rows |
| File format | WAV for all manifest rows |
| Freeze timestamp | 2026-09-29 19:27:19 |
| Speaker/group identifiers | 438 unique identifiers |
| Source groups | 108 unique source groups |
| Speaker/group overlap across splits | 0 |
| Cross-split exact SHA duplicate leakage | 0 |
| Confirmed same-recording cross-split leakage | 0 |

Class counts:

| Class | Total | Train | Validation | Test |
|---|---:|---:|---:|---:|
| PLAY_MUSIC | 1,050 | 840 | 105 | 105 |
| WEATHER | 1,050 | 840 | 105 | 105 |
| TIME | 1,050 | 840 | 105 | 105 |
| LIGHT_ON | 1,050 | 840 | 105 | 105 |
| LIGHT_OFF | 1,050 | 840 | 105 | 105 |
| LIGHT_DIM | 2,100 | 1,680 | 210 | 210 |
| SET_TIMER | 1,050 | 840 | 105 | 105 |
| SET_ALARM | 1,050 | 840 | 105 | 105 |
| SET_TEMPERATURE | 2,100 | 1,680 | 210 | 210 |
| MEDIA_PAUSE | 1,050 | 840 | 105 | 105 |
| MEDIA_STOP | 1,050 | 840 | 105 | 105 |
| MEDIA_NEXT | 1,050 | 840 | 105 | 105 |
| VOLUME_UP | 1,050 | 840 | 105 | 105 |
| VOLUME_DOWN | 1,050 | 840 | 105 | 105 |
| CREATE_REMINDER | 1,050 | 840 | 105 | 105 |
| LIST_REMINDERS | 1,050 | 840 | 105 | 105 |
| CALL | 1,050 | 840 | 105 | 105 |
| MESSAGE | 1,050 | 840 | 105 | 105 |
| UNKNOWN | 2,500 | 2,121 | 148 | 231 |
| SILENCE | 1,206 | 632 | 296 | 278 |

## 5. Dataset Construction and Leakage Controls

The dataset construction sequence was evidence-driven:

1. Local Dataset 2 drive-download folders were inventoried inside VCM2.
2. 16,800 clean native Dataset 2 rows were selected as the native foundation.
3. 4,200 rows were admitted for `CALL`, `MESSAGE`, `LIST_REMINDERS`, and `CREATE_REMINDER`, with `SET_REMINDER` mapped to `CREATE_REMINDER` through a documented semantic vocabulary mapping.
4. `UNKNOWN` and `SILENCE` safety/background populations were audited and incorporated.
5. SILENCE source-disjointness concerns were remediated using authorized VCM2 material.
6. Exact SHA duplicate groups and filename overlap groups were audited.
7. `E53_DATASET_V1` was frozen at 24,706 rows in LOG008.

Recorded source composition was 16,800 Dataset 2 native foundation rows, 4,200 first-dataset admitted class rows, 2,500 `UNKNOWN` rows, and 1,206 `SILENCE` rows. The dataset is not the old E50 training manifest and not a copied E50 deployment dataset.

Leakage controls recorded by the source evidence include cross-split SHA duplicate count 0, confirmed same-recording cross-split leakage 0, speaker/group cross-split overlap 0, and a final leakage audit that treated filename collisions separately from same-audio leakage.

## 6. Preprocessing and Feature Representations

LOG011 control representation:

| Property | LOG011 log-Mel control |
|---|---|
| Sample rate | 16,000 Hz |
| Channels | Mono |
| Clip duration | 2.0 seconds |
| Samples | 32,000 |
| Normalization | Per-sample peak normalization by max(abs(audio), floor 1e-4) |
| STFT window | Hann |
| Frame length / hop / FFT | 512 / 256 / 512 |
| Mel bins | 32 |
| Frequency range | 20 Hz to 7,600 Hz |
| Transform | natural log(mel power + 1e-6) |
| Tensor shape | `(124, 32, 1)` |
| Augmentation | none |

LOG025 MFCC representation:

| Property | Value |
|---|---|
| Representation | MFCC |
| MFCC coefficients | 13 |
| Delta features | none |
| Transform | log mel power followed by orthonormal DCT-II |
| Tensor shape | `(124, 13, 1)` |
| Other audio parameters | same 16 kHz, 2.0 s, Hann, 512 frame, 256 hop, 512 FFT, 32 mel filters, 20 to 7,600 Hz, peak normalization |

LOG025 PCEN representation:

| Property | Value |
|---|---|
| Representation | PCEN |
| Transform | mel power followed by deterministic PCEN |
| PCEN gain / bias / power | 0.98 / 2.0 / 0.5 |
| Time constant | 0.4 s |
| Epsilon | 1e-6 |
| Smoothing coefficient | 0.025 |
| Tensor shape | `(124, 32, 1)` |
| Other audio parameters | same 16 kHz, 2.0 s, Hann, 512 frame, 256 hop, 512 FFT, 32 mel filters, 20 to 7,600 Hz, peak normalization |

## 7. Model Architecture

The principal E53 model was a compact 3-block Conv2D classifier. LOG011, LOG025_MFCC, and LOG025_PCEN used the same capacity pattern: Conv2D 16/32/64, BatchNorm, ReLU, MaxPool, GlobalAveragePooling, and a 20-way dense softmax. Input tensor width changed for MFCC because MFCC used 13 coefficients instead of 32 mel/PCEN bins.

| Layer | LOG011 / PCEN output | MFCC output | Parameters |
|---|---|---|---:|
| Input | `(None, 124, 32, 1)` | `(None, 124, 13, 1)` | 0 |
| Conv2D 16 | `(None, 124, 32, 16)` | `(None, 124, 13, 16)` | 144 |
| BatchNorm + ReLU + MaxPool | `(None, 62, 16, 16)` | `(None, 62, 6, 16)` | 64 |
| Conv2D 32 | `(None, 62, 16, 32)` | `(None, 62, 6, 32)` | 4,608 |
| BatchNorm + ReLU + MaxPool | `(None, 31, 8, 32)` | `(None, 31, 3, 32)` | 128 |
| Conv2D 64 | `(None, 31, 8, 64)` | `(None, 31, 3, 64)` | 18,432 |
| BatchNorm + ReLU | same spatial shape | same spatial shape | 256 |
| GlobalAveragePooling | `(None, 64)` | `(None, 64)` | 0 |
| Dense softmax | `(None, 20)` | `(None, 20)` | 1,300 |

Total parameters: 24,932. Trainable parameters: 24,708. Non-trainable parameters: 224. Dropout was not present in the recorded model summaries.

## 8. Training Configuration

| Parameter | LOG011 control | LOG025 MFCC | LOG025 PCEN |
|---|---|---|---|
| Dataset version | `E53_DATASET_V1` | `E53_DATASET_V1` | `E53_DATASET_V1` |
| Feature | log-Mel | MFCC | PCEN |
| Input shape | `(124, 32, 1)` | `(124, 13, 1)` | `(124, 32, 1)` |
| Optimizer | Adam | Adam | Adam |
| Learning rate | 0.001 | 0.001 | 0.001 |
| Batch size | 256 | 256 | 256 |
| Maximum epochs | 30 | 30 | 30 |
| Early stopping | validation loss, patience 5, restore best weights | same | same |
| Checkpoint criterion | best validation-loss checkpoint | best validation-loss checkpoint | best validation-loss checkpoint |
| Loss | sparse categorical crossentropy | sparse categorical crossentropy | sparse categorical crossentropy |
| Seed | 53009 | 53009 | 53009 |
| Augmentation | none | none | none |
| Class weights | none | none | none |
| Weight decay | not established in recovered config | not established in recovered config | not established in recovered config |
| Dropout | none in model summary | none in model summary | none in model summary |
| LR scheduler | not recorded beyond early stopping | not recorded beyond early stopping | not recorded beyond early stopping |
| Initialization details | not established beyond seed/config artifacts | not established beyond seed/config artifacts | not established beyond seed/config artifacts |
| Best epoch | 18 | 7 | 18 |
| Training time | 553.359 s | 73.096 s | 429.033 s |
| Model SHA-256 | `f2e2f0ad04f184c8790026414dcff6918b6a1edbbd99ec5508c47ad35b773585` | `ff6aca4ece7980035580d910a79dc4075cd9faaa594bcbcd2c49be5a2d77b741` | `dbdb37afea0ff319118fe70c1fd1f6bf73a2f60153b54b3ef353c4d99a722445` |

## 9. Experimental Design

E53 followed a controlled-change pattern: freeze the dataset first, run a small baseline, test convergence, increase model capacity, run diagnostics, then test targeted interventions. Later experiments used the frozen dataset and recorded whether they trained a model or only audited evidence.

| Experiment | Purpose | Intervention | Key result | Decision |
|---|---|---|---|---|
| LOG008 | Freeze dataset | Final dataset verification | 24,706 rows, 20 classes, no cross-split SHA leakage | Dataset frozen |
| LOG009 | Initial baseline | Tiny Conv2D 4/8/16, one-epoch baseline | test accuracy 0.088540, macro-F1 0.008134 | Weak baseline established |
| LOG010 | Convergence | Same tiny CNN trained to convergence window | test accuracy 0.269069, macro-F1 0.145196 | Improved but insufficient |
| LOG011 | Capacity control | Conv2D 16/32/64 | test accuracy 0.463779, macro-F1 0.410447 | Established E53 control |
| LOG012 | Background audit | SILENCE/UNKNOWN diagnostic | SILENCE->MEDIA_NEXT issue identified | Background issue documented |
| LOG013 | SILENCE exposure | Index-level SILENCE oversampling | SILENCE improved, operational macro-F1 decreased | Mixed, not promoted |
| LOG014 | Command balance audit | Count audit for target pairs | counts equal 840/105/105 | Count imbalance hypothesis blocked |
| LOG015 | Separability audit | Embedding/confidence/error audit | representation overlap supported for target pairs | Diagnostic association |
| LOG016 | Targeted exposure | 2x exposure for LIST/CREATE/VOLUME pair classes | macro-F1 0.443246, operational macro-F1 0.419711 | Mixed, not promoted |
| LOG017 | Source/speaker audit | Source/provenance association analysis | association supported, not speaker causality | Diagnostic association |
| LOG018 | Source-group feasibility | Design audit | physical V2 unnecessary for next test | Use index-level exposure |
| LOG019 | Source-group exposure | Source-group exposure balancing | macro-F1 0.302707, operational macro-F1 0.268324 | Regressed globally |
| LOG020 | Representation error audit | Diagnostic audit after LOG019 | selected bounded representation branch | Diagnostic only |
| LOG021 | Representation head | Head/representation change | macro-F1 0.090773, operational macro-F1 0.011557 | Severe regression |
| LOG022 | Dataset separability audit | Dataset/audio/representation audit | dataset and representation factors supported | Diagnostic only |
| LOG023 | Semantic vocabulary review | Phrase/provenance review | mixed evidence, incomplete phrase coverage | Diagnostic only |
| LOG024 | Provenance recovery | Authoritative phrase recovery audit | partial but insufficient recovery | Proceed only to bounded ablation |
| LOG025_MFCC | Representation ablation | MFCC, 13 coefficients | accuracy 0.478727, macro-F1 0.447684 | Mixed / inconclusive |
| LOG025_PCEN | Representation ablation | PCEN | accuracy 0.463779, macro-F1 0.387960 | Mixed / inconclusive |

## 10. Experimental Results

| Experiment | Role | Test accuracy | Macro-F1 | Weighted-F1 | Operational macro-F1 | UNKNOWN F1 | SILENCE F1 | Disposition |
|---|---|---:|---:|---:|---:|---:|---:|---|
| LOG009 | initial tiny baseline | 0.088540 | 0.008134 | not recorded in report table | not recorded | not recorded | not recorded | baseline weak |
| LOG010 | convergence baseline | 0.269069 | 0.145196 | 0.235987 | not recorded | 0.948546 | 0.855984 | improved but insufficient |
| LOG011 | established control | 0.463779 | 0.410447 | 0.445472 | 0.372275 | 0.922756 | 0.585242 | control established |
| LOG013 | SILENCE exposure | 0.488693 | 0.407811 | not recorded in final table | 0.356901 | not recorded here | 0.778993 | mixed |
| LOG016 | targeted exposure | not recorded in final table | 0.443246 | not recorded in final table | 0.419711 | decreased vs LOG011 | decreased vs LOG011 | mixed |
| LOG019 | source-group exposure | delta -0.091606 vs LOG011 | 0.302707 | not recorded in final table | 0.268324 | not recorded here | not recorded here | global regression |
| LOG021 | representation head | delta -0.228440 vs LOG011 | 0.090773 | not recorded in final table | 0.011557 | not recorded here | not recorded here | severe regression |
| LOG025_MFCC | MFCC ablation | 0.478727 | 0.447684 | 0.450891 | 0.444856 | 0.596129 | 0.350148 | mixed / inconclusive |
| LOG025_PCEN | PCEN ablation | 0.463779 | 0.387960 | 0.449258 | 0.338223 | 0.819328 | 0.851852 | mixed / inconclusive |

MFCC changed the key LOG011 metrics by: accuracy +0.014948, macro-F1 +0.037237, weighted-F1 +0.005419, operational macro-F1 +0.072581, UNKNOWN F1 -0.326627, and SILENCE F1 -0.235093. The aggregate gains came with a strong degradation in safety/background classes.

PCEN changed the key LOG011 metrics by: accuracy +0.000000, macro-F1 -0.022487, weighted-F1 +0.003786, operational macro-F1 -0.034052, UNKNOWN F1 -0.103428, and SILENCE F1 +0.266610. PCEN helped SILENCE but did not improve command-level macro performance.

## 11. Per-Class Results

The table below reports test precision / recall / F1. Supports are from the test split.

| Class | Support | LOG011 P/R/F1 | MFCC P/R/F1 | PCEN P/R/F1 |
|---|---:|---|---|---|
| PLAY_MUSIC | 105 | 0.310 / 0.552 / 0.397 | 0.509 / 0.562 / 0.534 | 0.000 / 0.000 / 0.000 |
| WEATHER | 105 | 0.652 / 0.819 / 0.726 | 0.783 / 0.448 / 0.570 | 0.587 / 0.771 / 0.667 |
| TIME | 105 | 0.905 / 0.181 / 0.302 | 0.632 / 0.114 / 0.194 | 0.500 / 0.010 / 0.019 |
| LIGHT_ON | 105 | 0.333 / 0.143 / 0.200 | 0.833 / 0.190 / 0.310 | 0.142 / 0.200 / 0.166 |
| LIGHT_OFF | 105 | 0.400 / 0.305 / 0.346 | 0.771 / 0.352 / 0.484 | 0.607 / 0.162 / 0.256 |
| LIGHT_DIM | 210 | 0.810 / 0.224 / 0.351 | 0.755 / 0.367 / 0.494 | 0.454 / 0.705 / 0.552 |
| SET_TIMER | 105 | 0.650 / 0.124 / 0.208 | 0.333 / 0.695 / 0.451 | 1.000 / 0.029 / 0.056 |
| SET_ALARM | 105 | 0.396 / 0.962 / 0.561 | 0.464 / 0.610 / 0.527 | 0.585 / 0.457 / 0.513 |
| SET_TEMPERATURE | 210 | 0.523 / 0.376 / 0.438 | 0.324 / 0.814 / 0.464 | 0.650 / 0.362 / 0.465 |
| MEDIA_PAUSE | 105 | 0.450 / 0.257 / 0.327 | 0.711 / 0.257 / 0.378 | 1.000 / 0.210 / 0.346 |
| MEDIA_STOP | 105 | 0.267 / 0.771 / 0.397 | 0.455 / 0.619 / 0.524 | 0.417 / 0.286 / 0.339 |
| MEDIA_NEXT | 105 | 0.207 / 0.610 / 0.309 | 0.197 / 0.238 / 0.216 | 0.362 / 0.610 / 0.454 |
| VOLUME_UP | 105 | 0.346 / 0.600 / 0.439 | 1.000 / 0.010 / 0.019 | 0.204 / 0.838 / 0.328 |
| VOLUME_DOWN | 105 | 0.286 / 0.019 / 0.036 | 0.510 / 0.238 / 0.325 | 0.255 / 0.133 / 0.175 |
| CREATE_REMINDER | 105 | 0.393 / 0.771 / 0.521 | 0.680 / 0.629 / 0.653 | 0.581 / 0.410 / 0.480 |
| LIST_REMINDERS | 105 | 0.500 / 0.248 / 0.331 | 0.771 / 0.514 / 0.617 | 0.633 / 0.295 / 0.403 |
| CALL | 105 | 0.395 / 0.486 / 0.436 | 0.519 / 0.667 / 0.583 | 0.207 / 0.752 / 0.324 |
| MESSAGE | 105 | 0.592 / 0.276 / 0.377 | 0.710 / 0.629 / 0.667 | 0.857 / 0.400 / 0.545 |
| UNKNOWN | 231 | 0.891 / 0.957 / 0.923 | 0.425 / 1.000 / 0.596 | 0.796 / 0.844 / 0.819 |
| SILENCE | 278 | 1.000 / 0.414 / 0.585 | 1.000 / 0.212 / 0.350 | 0.995 / 0.745 / 0.852 |

Strong points varied by representation. LOG011 had strong UNKNOWN F1 and WEATHER F1 but weak VOLUME_DOWN recall. MFCC improved many operational classes, especially reminder/message classes, but collapsed VOLUME_UP recall and degraded safety/background F1. PCEN improved SILENCE and LIGHT_DIM but produced zero PLAY_MUSIC F1 and very low TIME/SET_TIMER recall.

## 12. Confusion Matrix and Failure Analysis

Largest LOG011 test off-diagonal confusions:

| True class | Predicted class | Count | Interpretation |
|---|---|---:|---|
| SILENCE | MEDIA_NEXT | 119 | Dominant background failure; test SILENCE was source-specific. |
| LIST_REMINDERS | CREATE_REMINDER | 65 | Reminder-action semantic/representation confusion. |
| VOLUME_DOWN | VOLUME_UP | 65 | Directional volume confusion. |
| MESSAGE | MEDIA_NEXT | 48 | Cross-family command confusion. |
| SET_TEMPERATURE | SET_ALARM | 33 | Set-action confusion. |
| TIME | MEDIA_STOP | 33 | Low-recall TIME failure. |
| LIGHT_DIM | LIGHT_OFF | 32 | Light-command confusion. |
| LIGHT_DIM | SET_TEMPERATURE | 30 | Adjustment-command confusion. |

Largest LOG025 MFCC test off-diagonal confusions:

| True class | Predicted class | Count | Interpretation |
|---|---|---:|---|
| SILENCE | UNKNOWN | 109 | Safety/background separation shifted from command confusion to UNKNOWN. |
| SILENCE | MEDIA_NEXT | 99 | Background-to-command risk remained high. |
| LIGHT_DIM | SET_TEMPERATURE | 51 | Adjustment-command confusion remained. |
| TIME | SET_TIMER | 48 | Time/timer confusion increased. |
| WEATHER | SET_TEMPERATURE | 43 | Cross-domain command confusion. |
| MEDIA_NEXT | SET_TEMPERATURE | 42 | Unexpected command confusion. |
| LIGHT_DIM | SET_TIMER | 34 | Adjustment/timer confusion. |
| VOLUME_DOWN | UNKNOWN | 28 | Command rejected into UNKNOWN rather than classified as paired command. |

Largest LOG025 PCEN test off-diagonal confusions:

| True class | Predicted class | Count | Interpretation |
|---|---|---:|---|
| VOLUME_DOWN | VOLUME_UP | 74 | Directional volume confusion worsened relative to MFCC and LOG011. |
| TIME | CALL | 57 | Low-recall TIME failure. |
| SET_TEMPERATURE | CALL | 51 | Cross-domain confusion. |
| SILENCE | UNKNOWN | 50 | Background often mapped to UNKNOWN instead of command. |
| LIGHT_ON | LIGHT_DIM | 38 | Light-control confusion. |
| LIGHT_OFF | LIGHT_DIM | 37 | Light-control confusion. |
| MEDIA_PAUSE | CALL | 35 | Cross-family command confusion. |
| CREATE_REMINDER | VOLUME_UP | 34 | Reminder command confused with volume command. |

The failure analysis shows that E53 did not have one simple failure cause. It had background-source specificity, paired semantic/action confusions, direction confusions, incomplete phrase provenance for some classes, and representation-dependent tradeoffs.

## 13. UNKNOWN / SILENCE Analysis

`UNKNOWN` and `SILENCE` were included as safety/background classes, not operational commands. UNKNOWN had 2,500 rows split 2,121 / 148 / 231. SILENCE had 1,206 rows split 632 / 296 / 278. SILENCE source groups were background-noise files: `doing_the_dishes.wav`, `exercise_bike.wav`, `running_tap.wav`, and `dude_miaowing.wav`.

UNKNOWN/SILENCE results:

| Representation | UNKNOWN precision / recall / F1 | SILENCE precision / recall / F1 | Interpretation |
|---|---|---|---|
| LOG011 log-Mel | 0.891 / 0.957 / 0.923 | 1.000 / 0.414 / 0.585 | Strong UNKNOWN, weak SILENCE recall; dominant SILENCE prediction was MEDIA_NEXT. |
| MFCC | 0.425 / 1.000 / 0.596 | 1.000 / 0.212 / 0.350 | MFCC hurt both safety/background F1 values despite command metric gains. |
| PCEN | 0.796 / 0.844 / 0.819 | 0.995 / 0.745 / 0.852 | PCEN improved SILENCE substantially but still reduced UNKNOWN and command macro-F1 relative to LOG011. |

E53 did not establish that explicit UNKNOWN/SILENCE classes improved the deployed E50 system. It established only how these classes behaved inside E53's offline test protocol.

## 14. E53 Control vs MFCC vs PCEN

| Representation | Test accuracy | Macro-F1 | Weighted-F1 | Operational macro-F1 | UNKNOWN F1 | SILENCE F1 | Decision |
|---|---:|---:|---:|---:|---:|---:|---|
| LOG011 log-Mel control | 0.463779 | 0.410447 | 0.445472 | 0.372275 | 0.922756 | 0.585242 | established control |
| LOG025 MFCC | 0.478727 | 0.447684 | 0.450891 | 0.444856 | 0.596129 | 0.350148 | mixed / inconclusive |
| LOG025 PCEN | 0.463779 | 0.387960 | 0.449258 | 0.338223 | 0.819328 | 0.851852 | mixed / inconclusive |

MFCC was the best E53 result for accuracy, macro-F1, weighted-F1, and operational macro-F1, but its UNKNOWN and SILENCE results were weaker than LOG011. PCEN had the best SILENCE F1 but weaker macro-F1 and operational macro-F1 than LOG011. Therefore neither representation was a clear improvement across the metrics that mattered for a safety-aware command recognizer.

## 15. E53 vs E50 Comparative Study

A direct numerical E50-vs-E53 accuracy comparison is not established because the available E50 final evidence and E53 experimental evidence use different evaluation settings. E50's central evidence is a physical Raspberry Pi end-to-end benchmark; E53's central evidence is an offline test-set classifier evaluation.

| Dimension | E50 | E53 | Directly comparable? |
|---|---|---|---|
| Role | Final delivery system | Independent experiment | Yes, role can be compared. |
| Runtime stack | Wake gate + command CNN + confidence policy + router + local response | Offline classifier experiments | No, E53 lacks E50 runtime stack validation. |
| Physical Pi validation | Yes, 20 trials | Not established | Yes as presence/absence only. |
| Wake behavior | E37 wake gate tested in final stack | Not part of E53 | No. |
| End-to-end action | 10/19 valid-command action success; accepted-action precision 10/10 | Not evaluated | No. |
| Offline classifier metric | E50 has separate offline evidence, but final headline evidence is Pi benchmark | LOG011/MFCC/PCEN offline test metrics | Only if same dataset/protocol exists; not established here. |
| UNKNOWN/SILENCE treatment | E40 confidence rejection and UNKNOWN/no-action final benchmark trial | Explicit UNKNOWN/SILENCE classes in offline dataset | Conceptually comparable, not numerically equivalent. |
| Final deployment | Frozen Raspberry Pi package | Not deployed | Yes as status. |
| Replacement decision | Final system | Not promoted | Yes as engineering decision. |

E50 final physical Pi benchmark facts preserved for context: 20 trials; 19 valid command labels plus 1 UNKNOWN/no-action trial; wake success 19/20 overall; raw command classification 13/19 = 68.42%; end-to-end action success 10/19 = 52.63%; accepted-action precision 10/10 = 100%; safe rejection 10/10 = 100%; UNKNOWN/no-action safety 1/1 = 100%; return-to-listening 20/20 = 100%.

E53's best representation result, MFCC, reached test accuracy 0.478727 and macro-F1 0.447684 on E53_DATASET_V1, but that number is not directly comparable to E50's 13/19 physical Pi raw classification because the datasets, label sets, evaluation protocols, and runtime responsibilities differ.

## 16. Engineering Interpretation

E53 was technically valuable because it showed the cost of plausible alternatives. It established a clean dataset freeze, tested compact CNN capacity, measured background-class behavior, diagnosed paired-class confusions, investigated source/provenance effects, and compared log-Mel, MFCC, and PCEN under controlled conditions.

What improved: LOG011 strongly improved over LOG010, showing capacity mattered. MFCC improved within-E53 aggregate accuracy, macro-F1, weighted-F1, and operational macro-F1 relative to LOG011. PCEN improved SILENCE F1 relative to LOG011.

What did not improve: no representation produced a balanced improvement across command metrics and safety/background metrics. MFCC degraded UNKNOWN and SILENCE sharply. PCEN did not improve macro-F1 or operational macro-F1. Several difficult confusions remained, including reminder-pair, volume-direction, light-control, time/timer, and background-to-command errors.

## 17. Decision: Why E53 Did Not Replace E50

E53 remained independent because the recovered evidence does not establish a deployment-ready or E50-superior system. The source decision record closes E53 model development after LOG025 and states that neither MFCC nor PCEN provided sufficient evidence to justify continued autonomous development.

Evidence-supported reasons:

- E53 was offline classifier evaluation, not physical Raspberry Pi deployment validation.
- E53 did not test wake-word behavior, E40-like thresholding, deterministic routing, action execution, response playback, GUI behavior, or return-to-listening.
- MFCC improved command metrics but degraded UNKNOWN/SILENCE safety-background behavior.
- PCEN improved SILENCE but did not improve macro-F1 or operational macro-F1.
- E53 retained unresolved confusion patterns.
- E53 had incomplete row-level phrase/provenance evidence for important source groups.
- No valid direct same-protocol E50-vs-E53 comparison established E53 superiority.

## 18. Limitations

- E53 is not a deployed VCM system.
- E53 does not demonstrate Raspberry Pi inference, wake-word behavior, end-to-end routing, local action execution, recorded response playback, GUI behavior, deployment readiness, or product-level behavior.
- E53 does not prove E50 was beaten or should be replaced.
- LOG011 and later models are offline classifier evaluations.
- Some experiments were single fixed interventions, not exhaustive searches.
- No confidence thresholds, calibration, augmentation, transfer learning, or Pi deployment were evaluated under the final Option A study.
- Phrase/transcript provenance remains incomplete for important source groups.
- UNKNOWN semantic phrase provenance was not recovered from local E53 material.
- SILENCE was source-specific across splits, especially test `dude_miaowing.wav`.
- E53 does not prove no better model is possible; it shows only that the tested E53 interventions did not justify promotion.

## 19. Reproducibility Artifacts

| Artifact | Purpose | E53 source location inspected |
|---|---|---|
| Dataset manifest | Defines frozen dataset rows and splits | `data\manifests\E53_FINAL_DATASET_MANIFEST.csv` |
| Dataset metadata | Dataset version/freeze metadata | `data\manifests\E53_DATASET_V1_METADATA.json` |
| Dataset documentation | Counts, provenance, leakage, audio profile | `reports\E53_DATASET_COMPLETE_DOCUMENTATION.md` |
| Experiment log | Chronology and experiment decisions | `logs\EXPERIMENT_LOG.md` |
| Decision log | Dataset/model decisions and E50 separation | `logs\DECISIONS.md` |
| Project status | Final project state | `logs\PROJECT_STATUS.md` |
| LOG011 report | Established control evidence | `reports\E53_LOG011_CNN_CAPACITY_REPORT.md` |
| LOG025 comparison | MFCC/PCEN comparison | `reports\E53_LOG025_FINAL_REPRESENTATION_COMPARISON.md` |
| Training configs | Optimizer, LR, batch, early stopping, seed | `experiments\*/config\training_config.json` |
| Preprocessing configs | Feature extraction definitions | `experiments\*/config\preprocessing_config.json` |
| Model configs/summaries | Architecture and parameter count | `experiments\*/config\model_config.json`; `experiments\*/reports\model_architecture_summary.txt` |
| Metrics | Accuracy, F1, per-class metrics | `experiments\*/metrics\test_metrics.json`; `test_per_class_metrics.csv` |
| Confusion matrices/pairs | Failure analysis | `experiments\*/metrics\test_confusion_matrix.csv`; `test_confusion_pairs.csv` |
| Artifact SHA inventories | Artifact identity | `experiments\*/E53_*_ARTIFACT_SHA256.json`; `manifests\E53_CURRENT_SHA256SUMS.csv` |
| Reproducibility inventory | Map of available E53 artifacts | `reports\E53_REPRODUCIBILITY_INVENTORY.csv` |

## 20. Final E53 Conclusion

E53 is a technically useful independent experiment, not a final system replacement. It showed that the E53 dataset could be frozen and studied reproducibly, that model capacity mattered, and that MFCC/PCEN changed the error profile. It did not show a clean, safety-preserving improvement sufficient to replace E50. The best defensible conclusion is that E53 provides an auditable research branch into alternative features and explicit UNKNOWN/SILENCE modeling, while E50 remains the frozen final delivery system.
