# EXPERIMENT_LOG

This log records measured experiments only. Smoke experiments verify that the pipeline runs end to end; they are not final model claims.

Do not overwrite experiments. Add a new entry for each experiment ID.

## E01_SMOKE

### Date
2026-09-15

### Purpose
Verify the Phase 3 training/evaluation artifact pipeline using a fast sklearn baseline.

### Dataset Version
`data/metadata/active_dataset_index.csv`, official included set.

### Train/Validation/Test Split
Speaker-aware split from `active_dataset_index.csv`; train and validation only. Test split not used.

### Model
`StandardScaler + SGDClassifier(loss="log_loss")`

### Features
Pooled log-Mel features: mean and standard deviation for each of 40 Mel bins.

### Hyperparameters
Seed 42; max_iter 1000; class_weight balanced.

### Training Configuration
30 training examples per assignment intent; 10 validation examples per assignment intent.

### Result
Pipeline completed and artifacts were saved.

### Accuracy
0.2000

### Precision
Macro precision 0.2573

### Recall
Macro recall 0.2000

### F1
Macro-F1 0.1862

### Macro-F1
0.1862

### Confusion Matrix Location
`results/tables/E01_SMOKE_confusion_matrix.csv`

### Model Size
6,889 bytes

### Latency
NOT YET MEASURED

### RAM
NOT YET MEASURED

### CPU
NOT YET MEASURED

### Observations
The pooled-feature linear baseline is weak. It verifies the pipeline, but it is not an acceptable final model.

### Decision
Run a flattened log-Mel smoke baseline to check whether preserving time structure improves the result.

## E02_SMOKE_FLAT

### Date
2026-09-15

### Purpose
Verify the same sklearn baseline using flattened `398 x 40` log-Mel features.

### Dataset Version
`data/metadata/active_dataset_index.csv`, official included set.

### Train/Validation/Test Split
Speaker-aware split from `active_dataset_index.csv`; train and validation only. Test split not used.

### Model
`StandardScaler + SGDClassifier(loss="log_loss")`

### Features
Flattened `398 x 40` log-Mel matrix.

### Hyperparameters
Seed 42; max_iter 1000; class_weight balanced.

### Training Configuration
30 training examples per assignment intent; 10 validation examples per assignment intent.

### Result
Pipeline completed and artifacts were saved.

### Accuracy
0.2000

### Precision
Macro precision 0.1971

### Recall
Macro recall 0.2000

### F1
Macro-F1 0.1866

### Macro-F1
0.1866

### Confusion Matrix Location
`results/tables/E02_SMOKE_FLAT_confusion_matrix.csv`

### Model Size
1,020,649 bytes

### Latency
NOT YET MEASURED

### RAM
NOT YET MEASURED

### CPU
NOT YET MEASURED

### Observations
Flattened log-Mel did not improve the tiny intent-balanced sample. The sampling strategy may underrepresent raw command labels inside merged assignment intents.

### Decision
Add raw-label-balanced sampling while still evaluating against assignment intents.

## E03_SMOKE_RAW_BALANCED

### Date
2026-09-15

### Purpose
Verify baseline behavior when each raw command label is represented in the sampled train/validation data.

### Dataset Version
`data/metadata/active_dataset_index.csv`, official included set.

### Train/Validation/Test Split
Speaker-aware split from `active_dataset_index.csv`; train and validation only. Test split not used.

### Model
`StandardScaler + SGDClassifier(loss="log_loss")`

### Features
Flattened `398 x 40` log-Mel matrix.

### Hyperparameters
Seed 42; max_iter 1000; class_weight balanced.

### Training Configuration
30 training examples per raw label; 10 validation examples per raw label. Labels are still scored as the 10 assignment intents.

### Result
Pipeline completed and artifacts were saved.

### Accuracy
0.2450

### Precision
Macro precision 0.2394

### Recall
Macro recall 0.2620

### F1
Macro-F1 0.2446

### Macro-F1
0.2446

### Confusion Matrix Location
`results/tables/E03_SMOKE_RAW_BALANCED_confusion_matrix.csv`

### Model Size
1,020,649 bytes

### Latency
NOT YET MEASURED

### RAM
NOT YET MEASURED

### CPU
NOT YET MEASURED

### Observations
Raw-label-balanced sampling improved the smoke result slightly but remains weak. This supports moving to a true CNN or deep learning runtime rather than treating sklearn as final.

### Decision
Proceed to CNN training path setup. Keep `E03_SMOKE_RAW_BALANCED` as the best Phase 3 smoke baseline so far.

## E04_SKLEARN_MLP_SMOKE

### Date
2026-09-15

### Purpose
Run a nonlinear neural smoke baseline while TensorFlow/CNN setup is blocked.

### Dataset Version
`data/metadata/active_dataset_index.csv`, official included set.

### Train/Validation/Test Split
Speaker-aware split from `active_dataset_index.csv`; train and validation only. Test split not used.

### Model
`StandardScaler + MLPClassifier`

### Features
Flattened `398 x 40` log-Mel matrix.

### Hyperparameters
Hidden layers: 128 and 64. Seed 42. Max iterations 60. Early stopping enabled.

### Training Configuration
50 training examples per raw label; 15 validation examples per raw label. Labels are scored as the 10 assignment intents.

### Result
Pipeline completed and artifacts were saved. This is NOT the final CNN/TensorFlow model.

### Accuracy
0.2600

### Precision
Macro precision 0.25

### Recall
Macro recall 0.23

### F1
Macro-F1 0.2319

### Macro-F1
0.2319

### Confusion Matrix Location
`results/tables/E04_SKLEARN_MLP_SMOKE_confusion_matrix.csv`

### Model Size
24,952,542 bytes

### Latency
NOT YET MEASURED

### RAM
NOT YET MEASURED

### CPU
NOT YET MEASURED

### Observations
The nonlinear sklearn baseline is only slightly better in accuracy than the previous linear smoke baseline and has lower macro-F1 than `E03_SMOKE_RAW_BALANCED`. This suggests that quick sklearn baselines are not enough and the project should move to the real CNN/TensorFlow path.

### Decision
Keep this as fallback evidence only. Continue resolving TensorFlow/CNN training rather than treating the MLP as the final model.

## E04_CNN_SMOKE

### Date
2026-09-15

### Purpose
Run the first actual TensorFlow CNN smoke experiment after resolving the TensorFlow environment.

### Dataset Version
`data/metadata/active_dataset_index.csv`, official included set.

### Train/Validation/Test Split
Speaker-aware split from `active_dataset_index.csv`; train and validation only. Test split not used.

### Model
Tiny CNN from `training/cnn_model.py`.

### Features
`398 x 40 x 1` log-Mel tensors.

### Hyperparameters
3 epochs, batch size 32, seed 42.

### Training Configuration
50 training examples per raw label; 15 validation examples per raw label.

### Result
Completed. TensorFlow/Keras high-level `fit/evaluate/save` paths hung on this Windows setup, so the script now uses a manual TensorFlow training loop, direct validation forward pass, and NumPy `.npz` weight saving.

### Accuracy
Validation accuracy 0.0967.

### Precision
NOT MEASURED

### Recall
NOT MEASURED

### F1
NOT MEASURED

### Macro-F1
NOT MEASURED

### Confusion Matrix Location
NOT CREATED

### Model Size
94,024 bytes

### Latency
NOT YET MEASURED

### RAM
NOT YET MEASURED

### CPU
NOT YET MEASURED

### Observations
Validation accuracy is approximately random for 10 classes. This is a true CNN run, but it is not a usable model yet.

### Decision
Add train-derived feature normalization and rerun a smoke experiment.

## E05_CNN_SMOKE_NORM

### Date
2026-09-15

### Purpose
Test whether train-derived log-Mel normalization improves the CNN smoke result.

### Dataset Version
`data/metadata/active_dataset_index.csv`, official included set.

### Train/Validation/Test Split
Speaker-aware split from `active_dataset_index.csv`; train and validation only. Test split not used.

### Model
Tiny CNN from `training/cnn_model.py`.

### Features
Normalized `398 x 40 x 1` log-Mel tensors. Mean and standard deviation are computed from training data only.

### Hyperparameters
3 epochs, batch size 32, seed 42.

### Training Configuration
50 training examples per raw label; 15 validation examples per raw label.

### Result
Completed.

### Accuracy
Validation accuracy 0.0967.

### Precision
NOT MEASURED

### Recall
NOT MEASURED

### F1
NOT MEASURED

### Macro-F1
NOT MEASURED

### Confusion Matrix Location
NOT CREATED

### Model Size
93,990 bytes

### Latency
NOT YET MEASURED

### RAM
NOT YET MEASURED

### CPU
NOT YET MEASURED

### Observations
Normalization did not improve the 3-epoch smoke result.

### Decision
Run a longer normalized smoke to check whether the CNN is simply undertrained.

## E06_CNN_SMOKE_NORM_20E

### Date
2026-09-15

### Purpose
Check whether the normalized CNN can learn with more epochs on the same smoke subset.

### Dataset Version
`data/metadata/active_dataset_index.csv`, official included set.

### Train/Validation/Test Split
Speaker-aware split from `active_dataset_index.csv`; train and validation only. Test split not used.

### Model
Tiny CNN from `training/cnn_model.py`.

### Features
Normalized `398 x 40 x 1` log-Mel tensors. Mean and standard deviation are computed from training data only.

### Hyperparameters
20 epochs, batch size 32, seed 42.

### Training Configuration
50 training examples per raw label; 15 validation examples per raw label.

### Result
Completed.

### Accuracy
Validation accuracy 0.1233.

### Precision
NOT MEASURED

### Recall
NOT MEASURED

### F1
NOT MEASURED

### Macro-F1
NOT MEASURED

### Confusion Matrix Location
NOT CREATED

### Model Size
94,212 bytes

### Latency
NOT YET MEASURED

### RAM
NOT YET MEASURED

### CPU
NOT YET MEASURED

### Observations
Training accuracy reached only 0.2840 and validation accuracy only 0.1233. The current tiny CNN/training setup is underperforming. This should be diagnosed before adding more data.

### Decision
Next step is diagnosis, not data expansion: inspect class predictions/confusion, consider stronger architecture or training setup, and check whether the split/domain difference is too hard for the small subset.

## E06 CNN Diagnostics

### Date
2026-09-15

### Purpose
Inspect the prediction behavior of `E06_CNN_SMOKE_NORM_20E`.

### Result
Diagnostics completed.

### Accuracy
0.1233

### Macro-F1
0.0499

### Confusion Matrix Location
`results/tables/E06_CNN_SMOKE_NORM_20E_cnn_confusion_matrix.csv`

### Observations
The model collapsed heavily toward one class. Out of 300 validation examples, it predicted `THERMOSTAT` 253 times.

### Decision
Run overfit sanity tests before changing the dataset.

## E07_CNN_OVERFIT_TINY

### Date
2026-09-15

### Purpose
Check whether the default CNN can memorize a tiny raw-label-balanced subset.

### Result
Training accuracy reached 0.3900 by epoch 80, but same-data inference accuracy was only 0.1100.

### Observations
Raw-label-balanced sampling creates final-intent imbalance because some assignment intents contain more raw labels than others. This made the test less clean.

### Decision
Run an intent-balanced overfit test.

## E09_CNN_OVERFIT_INTENT_BALANCED

### Date
2026-09-15

### Purpose
Check whether the default BatchNorm CNN can memorize a tiny intent-balanced subset.

### Result
Training accuracy reached 0.9600, but same-data inference accuracy was only 0.1000.

### Observations
This strongly indicates a BatchNorm moving-statistics/inference mismatch in the manual training setup.

### Decision
Test BatchNorm with faster moving-stat updates.

## E11_CNN_OVERFIT_FASTBN

### Date
2026-09-15

### Purpose
Check whether fast BatchNorm moving-stat updates fix same-data inference.

### Result
Same-data validation accuracy reached 0.8600 and macro-F1 reached 0.8614.

### Accuracy
0.8600

### Macro-F1
0.8614

### Model Size
94,052 bytes

### Observations
Fast BatchNorm fixes the main overfit sanity failure. The CNN can memorize a tiny balanced subset when BatchNorm inference statistics update quickly enough.

### Decision
Use `configs/cnn_fast_batchnorm.json` for the next real CNN smoke/baseline.

## E12_CNN_FASTBN_INTENT_SMOKE

### Date
2026-09-15

### Purpose
Run the corrected real CNN smoke/baseline using fast BatchNorm and intent-balanced sampling.

### Dataset Version
`data/metadata/active_dataset_index.csv`, official included set.

### Train/Validation/Test Split
Speaker-aware split from `active_dataset_index.csv`; train and validation only. Test split not used.

### Model
Tiny CNN using `configs/cnn_fast_batchnorm.json`.

### Features
Normalized `398 x 40 x 1` log-Mel tensors. Mean and standard deviation are computed from training data only.

### Hyperparameters
40 epochs, batch size 32, seed 42, fast BatchNorm momentum 0.1.

### Training Configuration
100 training examples per assignment intent; 30 validation examples per assignment intent.

### Result
Completed.

### Accuracy
Intent-balanced validation accuracy 0.3533.

### Precision
Macro precision 0.6203.

### Recall
Macro recall 0.3533.

### F1
Macro-F1 0.3716.

### Macro-F1
0.3716

### Confusion Matrix Location
`results/tables/E12_CNN_FASTBN_INTENT_SMOKE_cnn_confusion_matrix.csv`

### Model Size
94,052 bytes.

### Latency
NOT YET MEASURED

### RAM
NOT YET MEASURED

### CPU
NOT YET MEASURED

### Observations
This is a major improvement over the earlier CNN smoke, but the model still over-predicts `THERMOSTAT`. In the intent-balanced diagnostic set, 173 of 300 validation examples were predicted as `THERMOSTAT`.

### Decision
Continue model diagnosis and improvement before adding more data or deploying to Raspberry Pi.

## E13_CNN_DENSE_OVERFIT

### Date
2026-09-15

### Purpose
Test whether a stronger dense-head CNN with dropout can pass a tiny intent-balanced overfit sanity test.

### Dataset Version
`data/metadata/active_dataset_index.csv`, official included set.

### Train/Validation/Test Split
Speaker-aware split from `active_dataset_index.csv`; train rows reused as validation rows for same-data overfit testing. Test split not used.

### Model
CNN using `configs/cnn_fastbn_dense.json`.

### Features
Normalized `398 x 40 x 1` log-Mel tensors. Mean and standard deviation are computed from training data only.

### Hyperparameters
60 epochs, batch size 32, seed 42, fast BatchNorm momentum 0.1, dense layer with dropout.

### Training Configuration
5 training examples per assignment intent; validation uses the same rows.

### Result
Completed, but did not pass the sanity test strongly.

### Accuracy
Same-data validation accuracy 0.5400.

### Macro-F1
0.5311

### Confusion Matrix Location
NOT CREATED

### Model Size
247,964 bytes.

### Latency
NOT YET MEASURED

### RAM
NOT YET MEASURED

### CPU
NOT YET MEASURED

### Observations
The dense model with dropout did not memorize the tiny balanced subset as expected. This suggested regularization was too strong for the sanity test or the configuration was less stable than the simpler fast-BatchNorm run.

### Decision
Create a no-dropout dense sanity configuration and rerun the overfit test before using the stronger architecture for a real smoke baseline.

## E14_CNN_DENSE_NODROPOUT_OVERFIT

### Date
2026-09-15

### Purpose
Check whether the stronger dense CNN can memorize a tiny balanced subset when dropout is disabled.

### Dataset Version
`data/metadata/active_dataset_index.csv`, official included set.

### Train/Validation/Test Split
Speaker-aware split from `active_dataset_index.csv`; train rows reused as validation rows for same-data overfit testing. Test split not used.

### Model
CNN using `configs/cnn_fastbn_dense_nodropout.json`.

### Features
Normalized `398 x 40 x 1` log-Mel tensors. Mean and standard deviation are computed from training data only.

### Hyperparameters
60 epochs, batch size 32, seed 42, fast BatchNorm momentum 0.1, dense layer, no dropout.

### Training Configuration
5 training examples per assignment intent; validation uses the same rows.

### Result
Completed and passed the sanity test.

### Accuracy
Same-data validation accuracy 1.0000.

### Precision
Macro precision 1.0000.

### Recall
Macro recall 1.0000.

### F1
Macro-F1 1.0000.

### Macro-F1
1.0000

### Confusion Matrix Location
NOT CREATED

### Model Size
247,962 bytes.

### Latency
NOT YET MEASURED

### RAM
NOT YET MEASURED

### CPU
NOT YET MEASURED

### Observations
The CNN training path is capable of learning the log-Mel inputs when the architecture has enough capacity and the sanity-test regularization is removed.

### Decision
Use the no-dropout dense configuration for the next real intent-balanced smoke/baseline.

## E15_CNN_DENSE_NODROPOUT_INTENT_SMOKE

### Date
2026-09-15

### Purpose
Run a stronger real CNN smoke/baseline after the no-dropout dense overfit sanity test passed.

### Dataset Version
`data/metadata/active_dataset_index.csv`, official included set.

### Train/Validation/Test Split
Speaker-aware split from `active_dataset_index.csv`; train and validation only. Test split not used.

### Model
CNN using `configs/cnn_fastbn_dense_nodropout.json`.

### Features
Normalized `398 x 40 x 1` log-Mel tensors. Mean and standard deviation are computed from training data only.

### Hyperparameters
60 epochs, batch size 32, seed 42, fast BatchNorm momentum 0.1, dense layer, no dropout.

### Training Configuration
100 training examples per assignment intent; 30 validation examples per assignment intent.

### Result
Completed. This improved over `E12` and was later superseded by `E16`.

### Accuracy
Intent-balanced validation accuracy 0.5533.

### Precision
Macro precision 0.5600.

### Recall
Macro recall 0.5533.

### F1
Macro-F1 0.5411.

### Macro-F1
0.5411

### Confusion Matrix Location
`results/tables/E15_CNN_DENSE_NODROPOUT_INTENT_SMOKE_cnn_confusion_matrix.csv`

### Model Size
248,654 bytes.

### Latency
NOT YET MEASURED

### RAM
NOT YET MEASURED

### CPU
NOT YET MEASURED

### Observations
The model improved substantially over `E12` and no longer collapses into mostly `THERMOSTAT`. Predicted counts are spread across all 10 intents. Stronger classes include `REMINDER`, `SET_ALARM`, `SET_TIMER`, and `THERMOSTAT`. Weak classes include `CALL_MESSAGE` and `QUESTION`.

### Decision
Keep the no-dropout dense configuration for the next smoke run, but add best-validation checkpoint tracking before treating it as the current best baseline.

## E16_CNN_DENSE_NODROPOUT_BESTVAL_SMOKE

### Date
2026-09-16

### Purpose
Repeat the stronger no-dropout dense CNN smoke while tracking validation performance after each epoch and saving the best validation checkpoint.

### Dataset Version
`data/metadata/active_dataset_index.csv`, official included set.

### Train/Validation/Test Split
Speaker-aware split from `active_dataset_index.csv`; train and validation only. Test split not used.

### Model
CNN using `configs/cnn_fastbn_dense_nodropout.json`.

### Features
Normalized `398 x 40 x 1` log-Mel tensors. Mean and standard deviation are computed from training data only.

### Hyperparameters
60 epochs, batch size 32, seed 42, fast BatchNorm momentum 0.1, dense layer, no dropout, best-validation checkpoint tracking enabled.

### Training Configuration
100 training examples per assignment intent; 30 validation examples per assignment intent.

### Result
Completed. The script restored and saved the best validation checkpoint from epoch 50.

### Accuracy
Intent-balanced validation accuracy 0.5600.

### Precision
Macro precision 0.5761.

### Recall
Macro recall 0.5600.

### F1
Macro-F1 0.5434.

### Macro-F1
0.5434

### Confusion Matrix Location
`results/tables/E16_CNN_DENSE_NODROPOUT_BESTVAL_SMOKE_cnn_confusion_matrix.csv`

### Model Size
248,537 bytes.

### Latency
NOT YET MEASURED

### RAM
NOT YET MEASURED

### CPU
NOT YET MEASURED

### Observations
Best-validation tracking produced a small improvement over `E15`. The prediction distribution is balanced across all 10 intents, but per-class weakness remains. `CALL_MESSAGE` recall is 0.20, `MEDIA_CONTROL` recall is 0.37, and `THERMOSTAT` recall is 0.30. Stronger classes include `REMINDER`, `SET_ALARM`, `PLAY_MUSIC`, and `SET_TIMER`.

### Decision
Treat `E16` as the best smoke baseline at that point. Future CNN runs should use best-validation tracking, then test lower learning rate or mild regularization before expanding the dataset.

## E17_CNN_DENSE_NODROPOUT_LR3E4_BESTVAL_SMOKE

### Date
2026-09-16

### Purpose
Test whether reducing the Adam learning rate from 0.001 to 0.0003 improves validation stability for the no-dropout dense CNN.

### Dataset Version
`data/metadata/active_dataset_index.csv`, official included set.

### Train/Validation/Test Split
Speaker-aware split from `active_dataset_index.csv`; train and validation only. Test split not used.

### Model
CNN using `configs/cnn_fastbn_dense_nodropout_lr3e4.json`.

### Features
Normalized `398 x 40 x 1` log-Mel tensors. Mean and standard deviation are computed from training data only.

### Hyperparameters
80 epochs, batch size 32, seed 42, fast BatchNorm momentum 0.1, dense layer, no dropout, learning rate 0.0003, best-validation checkpoint tracking enabled.

### Training Configuration
100 training examples per assignment intent; 30 validation examples per assignment intent.

### Result
Completed. The script restored and saved the best validation checkpoint from epoch 56, but this run was worse than `E16`.

### Accuracy
Intent-balanced validation accuracy 0.3533.

### Precision
Macro precision 0.3935.

### Recall
Macro recall 0.3533.

### F1
Macro-F1 0.3594.

### Macro-F1
0.3594

### Confusion Matrix Location
`results/tables/E17_CNN_DENSE_NODROPOUT_LR3E4_BESTVAL_SMOKE_cnn_confusion_matrix.csv`

### Model Size
248,186 bytes.

### Latency
NOT YET MEASURED

### RAM
NOT YET MEASURED

### CPU
NOT YET MEASURED

### Observations
Lowering the learning rate did not improve validation. The model still memorized the training subset, reaching 1.0000 training accuracy in many late epochs, but validation stayed much lower than `E16`.

### Decision
Reject this lower-learning-rate config as the next baseline. Keep `E16` as the best baseline at that point and test mild regularization or a larger training subset next.

## E18_CNN_DENSE_DROPOUT01_BESTVAL_SMOKE

### Date
2026-09-16

### Purpose
Test whether mild dropout improves generalization for the dense fast-BatchNorm CNN.

### Dataset Version
`data/metadata/active_dataset_index.csv`, official included set.

### Train/Validation/Test Split
Speaker-aware split from `active_dataset_index.csv`; train and validation only. Test split not used.

### Model
CNN using `configs/cnn_fastbn_dense_dropout01.json`.

### Features
Normalized `398 x 40 x 1` log-Mel tensors. Mean and standard deviation are computed from training data only.

### Hyperparameters
60 epochs, batch size 32, seed 42, fast BatchNorm momentum 0.1, dense layer, dropout 0.1, dense dropout 0.1, learning rate 0.001, best-validation checkpoint tracking enabled.

### Training Configuration
100 training examples per assignment intent; 30 validation examples per assignment intent.

### Result
Completed. The best validation checkpoint was epoch 60, but this run did not beat `E16`.

### Accuracy
Intent-balanced validation accuracy 0.4967.

### Precision
Macro precision 0.4820.

### Recall
Macro recall 0.4967.

### F1
Macro-F1 0.4667.

### Macro-F1
0.4667

### Confusion Matrix Location
`results/tables/E18_CNN_DENSE_DROPOUT01_BESTVAL_SMOKE_cnn_confusion_matrix.csv`

### Model Size
248,575 bytes.

### Latency
NOT YET MEASURED

### RAM
NOT YET MEASURED

### CPU
NOT YET MEASURED

### Observations
Mild dropout slowed learning substantially on the 1,000-example smoke subset. It recovered late but remained below the no-dropout E16 baseline.

### Decision
Reject mild dropout for the current smoke setup. Try a larger no-dropout training subset instead.

## E19_CNN_DENSE_NODROPOUT_300PI_BESTVAL

### Date
2026-09-16

### Purpose
Test whether increasing the training subset from 100 to 300 examples per intent improves the current best no-dropout dense CNN.

### Dataset Version
`data/metadata/active_dataset_index.csv`, official included set.

### Train/Validation/Test Split
Speaker-aware split from `active_dataset_index.csv`; train and validation only. Test split not used.

### Model
CNN using `configs/cnn_fastbn_dense_nodropout.json`.

### Features
Normalized `398 x 40 x 1` log-Mel tensors. Mean and standard deviation are computed from training data only.

### Hyperparameters
60 epochs, batch size 32, seed 42, fast BatchNorm momentum 0.1, dense layer, no dropout, learning rate 0.001, best-validation checkpoint tracking enabled.

### Training Configuration
300 training examples per assignment intent; 30 validation examples per assignment intent.

### Result
Completed. The script restored and saved the best validation checkpoint from epoch 51. This is the current best real CNN smoke/baseline.

### Accuracy
Intent-balanced validation accuracy 0.7233.

### Precision
Macro precision 0.7418.

### Recall
Macro recall 0.7233.

### F1
Macro-F1 0.7198.

### Macro-F1
0.7198

### Confusion Matrix Location
`results/tables/E19_CNN_DENSE_NODROPOUT_300PI_BESTVAL_cnn_confusion_matrix.csv`

### Model Size
249,006 bytes.

### Latency
NOT YET MEASURED

### RAM
NOT YET MEASURED

### CPU
NOT YET MEASURED

### Observations
Scaling the training subset substantially improved validation performance. Most intents now have useful F1 scores. `MEDIA_CONTROL` remains the clearest weak class with 0.37 recall and 0.45 F1.

### Decision
Promote `E19` as the current best smoke baseline. Next, inspect `MEDIA_CONTROL` confusion and consider scaling closer to the full training set before laptop microphone or Raspberry Pi trials.

## E20_CNN_DENSE_NODROPOUT_600PI_BESTVAL

### Date
2026-09-16

### Purpose
Scale the current best no-dropout dense CNN closer to the full dataset by increasing training coverage from 300 to 600 examples per intent.

### Dataset Version
`data/metadata/active_dataset_index.csv`, official included set.

### Train/Validation/Test Split
Speaker-aware split from `active_dataset_index.csv`; train and validation only. Test split not used.

### Model
CNN using `configs/cnn_fastbn_dense_nodropout.json`.

### Features
Normalized `398 x 40 x 1` log-Mel tensors. Mean and standard deviation are computed from training data only.

### Hyperparameters
60 epochs, batch size 32, seed 42, fast BatchNorm momentum 0.1, dense layer, no dropout, learning rate 0.001, best-validation checkpoint tracking enabled.

### Training Configuration
600 training examples per assignment intent; 30 validation examples per assignment intent.

### Result
Completed. The best validation checkpoint was epoch 60. This is the current best real CNN smoke/baseline.

### Accuracy
Intent-balanced validation accuracy 0.8133.

### Precision
Macro precision 0.8138.

### Recall
Macro recall 0.8133.

### F1
Macro-F1 0.8113.

### Macro-F1
0.8113

### Confusion Matrix Location
`results/tables/E20_CNN_DENSE_NODROPOUT_600PI_BESTVAL_cnn_confusion_matrix.csv`

### Model Size
249,419 bytes.

### Latency
NOT YET MEASURED

### RAM
NOT YET MEASURED

### CPU
NOT YET MEASURED

### Confidence Threshold Diagnostics
`results/tables/E20_CNN_DENSE_NODROPOUT_600PI_BESTVAL_confidence_threshold_summary.csv`

At threshold 0.90, the model accepts 250 of 300 validation examples, with accepted-command accuracy 0.8800.

At threshold 0.95, the model accepts 232 of 300 validation examples, with accepted-command accuracy 0.9181.

### MEDIA_CONTROL Diagnostics
`results/tables/E20_CNN_DENSE_NODROPOUT_600PI_BESTVAL_media_control_raw_label_breakdown.csv`

`MEDIA_CONTROL` improved but remains the weakest intent. It reached precision 0.65, recall 0.57, and F1 0.61. Raw-label breakdown: `VOLUME_UP` 5/5 correct, `STOP` 4/7 correct, `NEXT` 4/9 correct, `VOLUME_DOWN` 2/5 correct, and `PAUSE` 2/4 correct.

### Observations
Scaling from 3,000 to 6,000 training examples substantially improved validation performance. This supports continuing with the current CNN and existing dataset before adding new data.

### Decision
Promote `E20` as the current best smoke baseline. Continue existing-data scaling and confidence-threshold evaluation before adding or generating new command data.

## E21_CNN_DENSE_NODROPOUT_1000PI_BESTVAL

### Date
2026-09-16

### Purpose
Scale the current best no-dropout dense CNN closer to the full dataset by increasing training coverage to up to 1,000 examples per intent.

### Dataset Version
`data/metadata/active_dataset_index.csv`, official included set.

### Train/Validation/Test Split
Speaker-aware split from `active_dataset_index.csv`; train and validation only. Test split not used.

### Model
CNN using `configs/cnn_fastbn_dense_nodropout.json`.

### Features
Normalized `398 x 40 x 1` log-Mel tensors. Mean and standard deviation are computed from training data only.

### Hyperparameters
60 epochs, batch size 32, seed 42, fast BatchNorm momentum 0.1, dense layer, no dropout, learning rate 0.001, best-validation checkpoint tracking enabled.

### Training Configuration
Up to 1,000 training examples per assignment intent; 30 validation examples per assignment intent. Actual selected training examples: 9,520.

### Result
Completed. The best validation checkpoint was epoch 51. This is the current best real CNN smoke/baseline by macro-F1.

### Accuracy
Intent-balanced validation accuracy 0.8267.

### Precision
Macro precision 0.8487.

### Recall
Macro recall 0.8267.

### F1
Macro-F1 0.8304.

### Macro-F1
0.8304

### Confusion Matrix Location
`results/tables/E21_CNN_DENSE_NODROPOUT_1000PI_BESTVAL_cnn_confusion_matrix.csv`

### Model Size
249,658 bytes.

### Latency
NOT YET MEASURED

### RAM
NOT YET MEASURED

### CPU
NOT YET MEASURED

### Confidence Threshold Diagnostics
`results/tables/E21_CNN_DENSE_NODROPOUT_1000PI_BESTVAL_confidence_threshold_summary.csv`

At threshold 0.90, the model accepts 255 of 300 validation examples, with accepted-command accuracy 0.8902.

At threshold 0.95, the model accepts 241 of 300 validation examples, with accepted-command accuracy 0.9046.

### MEDIA_CONTROL Diagnostics
`results/tables/E21_CNN_DENSE_NODROPOUT_1000PI_BESTVAL_media_control_raw_label_breakdown.csv`

`MEDIA_CONTROL` recall improved to 0.70, but precision dropped to 0.50 because the model over-predicted the class. Raw-label breakdown: `VOLUME_UP` 5/5 correct, `VOLUME_DOWN` 4/5 correct, `STOP` 4/7 correct, `NEXT` 5/9 correct, and `PAUSE` 3/4 correct.

### Observations
Scaling from E20 to E21 improved overall macro-F1 from 0.8113 to 0.8304. The class-level tradeoff is that `MEDIA_CONTROL` recall improved while precision worsened.

### Decision
Promote `E21` as the current best smoke baseline by macro-F1. Proceed toward laptop microphone trials with confidence-threshold rejection, while logging possible false `MEDIA_CONTROL` triggers carefully.

## LAPTOP_WAV_TRIAL_TOOLING

### Date
2026-09-16

### Purpose
Prepare laptop microphone trial tooling using the current best E21 CNN model and confidence-threshold rejection.

### Action
Added:
- `demo/cnn_inference.py`
- `demo/predict_wav.py`
- `demo/record_and_predict.py`
- `demo/LAPTOP_MIC_TRIALS.md`

### Result
WAV-file prediction works with E21 model loading, E21 normalization, top-k output, confidence-threshold rejection, and CSV trial logging.

### Verification
`python demo\predict_wav.py "data\drive-download-20260915T085515Z-1-001\CALL\CALL_s26_p2_v1.wav" --actual-intent CALL_MESSAGE --threshold 0.90`

The command predicted `CALL_MESSAGE` correctly, but rejected execution because confidence was below 0.90. This verifies that the confidence gate is active.

### Blocker
Live recording through `demo/record_and_predict.py` requires the optional `sounddevice` package, which is not installed in the current Python environment. Existing PCM WAV files can still be classified with `demo/predict_wav.py`.

### Decision
Use `demo/predict_wav.py` for immediate WAV-based laptop trials. Install or otherwise provide a WAV recording path before live microphone trials.

## LAPTOP_WAV_TRIAL_001

### Date
2026-09-16

### Purpose
Run the first real laptop-recorded WAV through the E21 CNN with confidence-threshold rejection.

### Input WAV
`C:\Users\Loreen Anne\Downloads\Recording.wav`

### WAV Properties
Stereo, 48 kHz, 16-bit PCM, 2.731 seconds. The project loader converted it to mono, resampled to 16 kHz, normalized, and padded to the same fixed input length used during training.

### Expected Intent
`LIGHT_CONTROL`

### Result
Predicted `SET_ALARM` with confidence 0.818775.

### Threshold
0.90

### Accepted
false

### Observation
This is a failed recognition trial but a successful safety-gate trial. The model did not execute the wrong command because confidence was below the threshold.

### Decision
Continue controlled laptop WAV trials before adding new data. Record multiple examples per target intent, especially `LIGHT_CONTROL` and `MEDIA_CONTROL`, and log accepted/rejected behavior.

## LAPTOP_WAV_TRIAL_BATCH_001

### Date
2026-09-16

### Purpose
Run a controlled batch of laptop WAV recordings through the E21 CNN with confidence-threshold rejection.

### Input Folder
`C:\Users\Loreen Anne\Documents\Sound Recordings`

### Expected Intent
`LIGHT_CONTROL`

### Files Tested
13 WAV files: `Recording.wav` through `Recording (13).wav`.

### Threshold
0.90

### Result
- Correct predictions: 4/13.
- Accepted predictions: 10/13.
- Accepted correct predictions: 4/13.
- Accepted wrong predictions: 6/13.

### Predicted Intent Counts
- `LIGHT_CONTROL`: 4
- `CALL_MESSAGE`: 2
- `SET_ALARM`: 2
- `MEDIA_CONTROL`: 2
- `PLAY_MUSIC`: 2
- `THERMOSTAT`: 1

### Accepted Wrong Predictions
- `Recording.wav`: predicted `CALL_MESSAGE`, confidence 0.999556.
- `Recording (5).wav`: predicted `SET_ALARM`, confidence 0.992151.
- `Recording (6).wav`: predicted `MEDIA_CONTROL`, confidence 0.999795.
- `Recording (8).wav`: predicted `CALL_MESSAGE`, confidence 0.999418.
- `Recording (10).wav`: predicted `THERMOSTAT`, confidence 0.969567.
- `Recording (11).wav`: predicted `PLAY_MUSIC`, confidence 0.998724.

### Observation
Validation performance is high, but laptop-recorded audio does not yet match the training distribution well enough for safe execution. The confidence threshold alone is insufficient because several wrong laptop predictions are highly confident.

### Decision
Do not proceed to action execution from laptop audio yet. Before adding new data, inspect the recording setup and run more controlled trials: consistent phrase, quiet room, same microphone distance, and possibly trimmed recordings with less silence/noise.

## LAPTOP_WAV_TRIAL_BATCH_002

### Date
2026-09-16

### Purpose
Run the second controlled batch of newer laptop WAV recordings through the E21 CNN with confidence-threshold rejection.

### Input Folder
`C:\Users\Loreen Anne\Documents\Sound Recordings`

### Expected Intent
`LIGHT_CONTROL`

### Files Tested
20 WAV files: `Recording.wav` through `Recording (20).wav`.

### Threshold
0.90

### Recording Format Check
- WAV PCM.
- 44.1 kHz.
- Stereo.
- 16-bit samples.
- Duration range approximately 0.92 to 1.87 seconds.

### Result
- Correct predictions: 0/20.
- Accepted predictions: 13/20.
- Accepted correct predictions: 0/20.
- Accepted wrong predictions: 13/20.

### Predicted Intent Counts
- `MEDIA_CONTROL`: 10
- `CALL_MESSAGE`: 5
- `QUESTION`: 2
- `LIGHT_ADJUST`: 2
- `PLAY_MUSIC`: 1

### Accepted Wrong Predictions
- `Recording.wav`: predicted `MEDIA_CONTROL`, confidence 0.986262.
- `Recording (3).wav`: predicted `MEDIA_CONTROL`, confidence 0.942837.
- `Recording (4).wav`: predicted `CALL_MESSAGE`, confidence 0.992916.
- `Recording (5).wav`: predicted `QUESTION`, confidence 0.958680.
- `Recording (7).wav`: predicted `MEDIA_CONTROL`, confidence 0.998644.
- `Recording (9).wav`: predicted `MEDIA_CONTROL`, confidence 0.999970.
- `Recording (10).wav`: predicted `MEDIA_CONTROL`, confidence 0.999210.
- `Recording (11).wav`: predicted `CALL_MESSAGE`, confidence 1.000000.
- `Recording (12).wav`: predicted `CALL_MESSAGE`, confidence 0.995960.
- `Recording (14).wav`: predicted `MEDIA_CONTROL`, confidence 0.993992.
- `Recording (15).wav`: predicted `MEDIA_CONTROL`, confidence 0.999994.
- `Recording (16).wav`: predicted `CALL_MESSAGE`, confidence 0.925084.
- `Recording (17).wav`: predicted `MEDIA_CONTROL`, confidence 0.998094.

### Observation
The second laptop batch is worse than the first batch and confirms that the validation-domain model is not yet robust to the laptop microphone recordings. The model often predicts `MEDIA_CONTROL` or `CALL_MESSAGE` with very high confidence for examples that were expected to be `LIGHT_CONTROL`.

### Decision
Do not use laptop predictions to trigger real actions. Continue diagnosis before adding broad new data. If new data is added, it should be targeted to the observed mismatch: real microphone audio, phrase consistency, microphone distance, silence/noise, and possibly laptop/Pi device characteristics.

## LAPTOP_WAV_TRIAL_BATCH_003

### Date
2026-09-16

### Purpose
Run the third controlled batch of fresh laptop WAV recordings through the E21 CNN with confidence-threshold rejection.

### Input Folder
`C:\Users\Loreen Anne\Documents\Sound Recordings`

### Expected Intent
`LIGHT_CONTROL`

### Files Tested
21 WAV files: `Recording.wav` through `Recording (21).wav`.

### Threshold
0.90

### Recording Format Check
- WAV PCM.
- 44.1 kHz.
- Stereo.
- 16-bit samples.
- Duration range approximately 0.71 to 3.40 seconds.

### Result
- Correct predictions: 1/21.
- Accepted predictions: 12/21.
- Accepted correct predictions: 1/21.
- Accepted wrong predictions: 11/21.

### Predicted Intent Counts
- `CALL_MESSAGE`: 12
- `SET_ALARM`: 2
- `QUESTION`: 2
- `MEDIA_CONTROL`: 2
- `THERMOSTAT`: 1
- `LIGHT_ADJUST`: 1
- `LIGHT_CONTROL`: 1

### Accepted Wrong Predictions
- `Recording.wav`: predicted `CALL_MESSAGE`, confidence 0.999340.
- `Recording (2).wav`: predicted `CALL_MESSAGE`, confidence 0.994359.
- `Recording (3).wav`: predicted `CALL_MESSAGE`, confidence 0.980918.
- `Recording (6).wav`: predicted `CALL_MESSAGE`, confidence 0.914438.
- `Recording (8).wav`: predicted `LIGHT_ADJUST`, confidence 0.985850.
- `Recording (9).wav`: predicted `SET_ALARM`, confidence 0.998753.
- `Recording (11).wav`: predicted `QUESTION`, confidence 0.994407.
- `Recording (12).wav`: predicted `CALL_MESSAGE`, confidence 0.999476.
- `Recording (15).wav`: predicted `CALL_MESSAGE`, confidence 0.999992.
- `Recording (17).wav`: predicted `CALL_MESSAGE`, confidence 0.977259.
- `Recording (20).wav`: predicted `MEDIA_CONTROL`, confidence 0.903386.

### Observation
The third laptop batch is still unsafe for action execution. Compared with the second batch, the dominant false prediction changed from `MEDIA_CONTROL` to `CALL_MESSAGE`, so the failure is broader than one weak intent.

### Decision
Do not use the current E21 model for live laptop command execution. Build a small labelled real-microphone calibration set and inspect feature/domain mismatch before deciding whether to add targeted real-mic training data or augmentation.

## LAPTOP_CALIBRATION_SET_001

### Date
2026-09-16

### Purpose
Evaluate the current E21 CNN on a balanced 50-file real-microphone calibration set.

### Input Folder
`C:\Users\Loreen Anne\Documents\Sound Recordings`

### Label Assumption
Files were sorted by `LastWriteTime` and grouped in the requested order, 5 files per intent:
`LIGHT_CONTROL`, `LIGHT_ADJUST`, `MEDIA_CONTROL`, `SET_TIMER`, `SET_ALARM`, `QUESTION`, `PLAY_MUSIC`, `CALL_MESSAGE`, `THERMOSTAT`, `REMINDER`.

### Threshold
0.90

### Output Artifacts
- `results/tables/LAPTOP_CALIBRATION_SET_001_summary.csv`
- `results/tables/LAPTOP_CALIBRATION_SET_001_confusion.csv`
- `results/tables/LAPTOP_CALIBRATION_SET_001_per_file.csv`

### Overall Result
- Total files: 50.
- Correct predictions: 17/50.
- Accuracy: 0.3400.
- Accepted predictions: 34/50.
- Accepted correct predictions: 14/34.
- Accepted-command accuracy: 0.4118.
- Accepted wrong predictions: 20/34.

### Per-Intent Result
- `LIGHT_CONTROL`: 0/5 correct; 3 wrong accepted.
- `LIGHT_ADJUST`: 0/5 correct; 4 wrong accepted.
- `MEDIA_CONTROL`: 3/5 correct; 2 wrong accepted.
- `SET_TIMER`: 1/5 correct; 3 wrong accepted.
- `SET_ALARM`: 3/5 correct; 0 wrong accepted.
- `QUESTION`: 1/5 correct; 1 wrong accepted.
- `PLAY_MUSIC`: 5/5 correct; 0 wrong accepted.
- `CALL_MESSAGE`: 1/5 correct; 3 wrong accepted.
- `THERMOSTAT`: 2/5 correct; 3 wrong accepted.
- `REMINDER`: 1/5 correct; 1 wrong accepted.

### Observation
`PLAY_MUSIC` transfers well to the laptop microphone, while `LIGHT_CONTROL` and `LIGHT_ADJUST` fail completely. The model also over-predicts `MEDIA_CONTROL` and `CALL_MESSAGE` across several real-mic intents.

### Decision
This is now enough evidence that the next improvement should be targeted real-microphone/domain adaptation, not more unlabelled/random recording trials. The label order should be confirmed before using the calibration set for any training or final claims.

## LAPTOP_CALIBRATION_SET_002

### Date
2026-09-16

### Purpose
Evaluate the current E21 CNN on a second balanced 50-file real-microphone calibration set and compare it against Set 001.

### Input Folder
`C:\Users\Loreen Anne\Documents\Sound Recordings`

### Label Assumption
The user confirmed the files were recorded in the planned order, sorted by `LastWriteTime`, 5 files per intent:
`LIGHT_CONTROL`, `LIGHT_ADJUST`, `MEDIA_CONTROL`, `SET_TIMER`, `SET_ALARM`, `QUESTION`, `PLAY_MUSIC`, `CALL_MESSAGE`, `THERMOSTAT`, `REMINDER`.

### Threshold
0.90

### Output Artifacts
- `results/tables/LAPTOP_CALIBRATION_SET_002_summary.csv`
- `results/tables/LAPTOP_CALIBRATION_SET_002_confusion.csv`
- `results/tables/LAPTOP_CALIBRATION_SET_002_per_file.csv`
- `results/tables/LAPTOP_CALIBRATION_SET_001_vs_002_summary.csv`

### Overall Result
- Total files: 50.
- Correct predictions: 42/50.
- Accuracy: 0.8400.
- Accepted predictions: 44/50.
- Accepted correct predictions: 39/44.
- Accepted-command accuracy: 0.8864.
- Accepted wrong predictions: 5/44.

### Per-Intent Result
- `LIGHT_CONTROL`: 2/5 correct; 2 wrong accepted.
- `LIGHT_ADJUST`: 4/5 correct; 1 wrong accepted.
- `MEDIA_CONTROL`: 5/5 correct; 0 wrong accepted.
- `SET_TIMER`: 4/5 correct; 0 wrong accepted.
- `SET_ALARM`: 5/5 correct; 0 wrong accepted.
- `QUESTION`: 5/5 correct; 0 wrong accepted.
- `PLAY_MUSIC`: 3/5 correct; 2 wrong accepted.
- `CALL_MESSAGE`: 5/5 correct; 0 wrong accepted.
- `THERMOSTAT`: 4/5 correct; 0 wrong accepted.
- `REMINDER`: 5/5 correct; 0 wrong accepted.

### Comparison To Set 001
Set 001 accuracy was 17/50, while Set 002 accuracy was 42/50. Accepted wrong predictions dropped from 20 to 5. This indicates that the real-microphone path can work much better under more consistent recording conditions, but the remaining errors are still important for deployment.

### Observation
The remaining deployment-critical weakness is `LIGHT_CONTROL`, which is only 2/5 correct. Since the Raspberry Pi demo centers on LED control, this class needs targeted inspection before live action execution.

### Decision
Set 002 replaces Set 001 as the stronger calibration evidence, but the model is not final. Next work should inspect the wrong accepted Set 002 predictions and improve lighting-command robustness.

## LAPTOP_CALIBRATION_SET_002_DIAGNOSTICS

### Date
2026-09-16

### Purpose
Preserve Set 002 and diagnose the remaining wrong accepted predictions, especially `LIGHT_CONTROL`.

### Archived Data
`data/calibration/LAPTOP_CALIBRATION_SET_002`

### Output Artifacts
- `data/calibration/LAPTOP_CALIBRATION_SET_002/manifest.csv`
- `results/tables/LAPTOP_CALIBRATION_SET_002_audio_diagnostics.csv`
- `results/tables/LAPTOP_CALIBRATION_SET_002_wrong_accepted.csv`
- `results/tables/LAPTOP_CALIBRATION_SET_002_light_control_diagnostics.csv`
- `results/tables/LAPTOP_CALIBRATION_SET_002_threshold_summary.csv`
- `results/tables/LAPTOP_CALIBRATION_SET_002_light_control_nearest_dataset.csv`

### Threshold Diagnostic
At threshold 0.90, Set 002 accepted 44/50 predictions with 39 correct and 5 wrong. At threshold 0.99, it accepted 37/50 predictions with 35 correct and 2 wrong.

The remaining wrong predictions at very high threshold were both `LIGHT_CONTROL -> QUESTION` cases. Therefore, threshold tuning alone cannot solve the light-control issue.

### Light-Control Diagnostic
Set 002 had no cases where a non-light intent was predicted as `LIGHT_CONTROL`. This is good for LED action safety. The issue is false rejection/misrouting of true light-control commands.

Nearest-dataset diagnostics for the light-control calibration examples found nearby original-dataset `LIGHT_CONTROL` examples for the failed clips. This suggests the recordings are not obviously outside the light-command acoustic region; the model decision boundary or confidence calibration around lighting commands needs targeted improvement.

### Decision
Use Set 002 as preserved real-mic evidence. Do not rely on confidence threshold alone. Focus next on targeted `LIGHT_CONTROL` adaptation/evaluation.

## E22_CNN_DENSE_NODROPOUT_1200PI_8E_PROBE

### Date
2026-09-16

### Purpose
Probe whether a larger intent-balanced training subset improves official validation and Calibration Set 002 performance, especially `LIGHT_CONTROL`.

### Configuration
- CNN config: `configs/cnn_fastbn_dense_nodropout.json`
- Training sample: up to 1,200 examples per intent.
- Validation sample: 30 examples per intent.
- Epochs: 8.
- Best-validation tracking: enabled.

### Output Artifacts
- `models/cnn/E22_CNN_DENSE_NODROPOUT_1200PI_8E_PROBE_weights.npz`
- `models/cnn/E22_CNN_DENSE_NODROPOUT_1200PI_8E_PROBE_normalization.npz`
- `results/tables/E22_CNN_DENSE_NODROPOUT_1200PI_8E_PROBE_metrics.json`
- `results/tables/E22_CNN_DENSE_NODROPOUT_1200PI_8E_PROBE_cnn_classification_report.txt`
- `results/tables/LAPTOP_CALIBRATION_SET_002_E22_1200PI_8E_PROBE_summary.csv`
- `results/tables/LAPTOP_CALIBRATION_SET_002_E22_1200PI_8E_PROBE_threshold_summary.csv`
- `results/tables/E21_vs_E22_8E_SET002_comparison.csv`

### Official Validation Result
- Accuracy: 0.7700.
- Macro-F1: 0.7635.
- Best epoch: 8.

### Calibration Set 002 Result
- Correct predictions: 41/50.
- Accuracy: 0.8200.
- Accepted predictions at threshold 0.90: 29/50.
- Accepted correct predictions: 27/29.
- Accepted-command accuracy: 0.9310.
- Wrong accepted predictions: 2.

### Light-Control Result
`LIGHT_CONTROL` on Calibration Set 002 was 1/5 correct for E22, compared with 2/5 correct for E21.

### Observation
E22 reduced wrong accepted predictions on Set 002, but it lowered overall validation performance and worsened the LED-critical `LIGHT_CONTROL` result. It also had much lower accepted-command coverage than E21.

### Decision
Do not promote E22. Keep E21 as the current selected model. The next improvement should be targeted `LIGHT_CONTROL` adaptation, not simply a short larger-subset training probe.

## LIGHT_ON_OFF_CLASS_DOWNLOAD_E21_CHECK

### Date
2026-09-16

### Purpose
Inspect and score newly downloaded class `LIGHT_ON` and `LIGHT_OFF` folders to determine whether they help the current `LIGHT_CONTROL` weakness.

### Input Folders
- `C:\Users\Loreen Anne\Downloads\LIGHT_ON-20260916T062226Z-1-001`
- `C:\Users\Loreen Anne\Downloads\LIGHT_OFF-20260916T062225Z-1-001`

### Data Description
- `LIGHT_ON`: 360 WAV files.
- `LIGHT_OFF`: 387 WAV files.
- Total: 747 WAV files.
- Format: 16 kHz, mono, 16-bit PCM WAV.
- Durations are approximately 0.74 to 2.64 seconds.

### Model
`E21_CNN_DENSE_NODROPOUT_1000PI_BESTVAL`

### Output Artifacts
- `results/tables/LIGHT_ON_OFF_CLASS_DOWNLOAD_E21_predictions.csv`
- `results/tables/LIGHT_ON_OFF_CLASS_DOWNLOAD_E21_summary.csv`

### Result
- Overall `LIGHT_CONTROL` accuracy: 662/747, or 0.8862.
- `LIGHT_ON`: 318/360 correct, or 0.8833.
- `LIGHT_OFF`: 344/387 correct, or 0.8889.

### Observation
The current E21 model already performs well on these class folders. Therefore, they are useful as external light-command support data, but they do not replace real-microphone calibration recordings. The main deployment gap remains the laptop/Pi microphone domain.

### Decision
Keep these folders as candidate supplemental light data. Prioritize new real-microphone `LIGHT_CONTROL` examples for deployment validation and any fine-tuning experiment.

## LIGHT_CONTROL_REALMIC_SET_003_TURN_ON_25

### Date
2026-09-16

### Purpose
Evaluate 25 fresh real-microphone recordings of "turn on the light" using the selected E21 model.

### Input Folder
`C:\Users\Loreen Anne\Documents\Sound Recordings`

### Archived Data
`data/calibration/LIGHT_CONTROL_REALMIC_SET_003_TURN_ON_25`

### Model
`E21_CNN_DENSE_NODROPOUT_1000PI_BESTVAL`

### Output Artifacts
- `results/tables/LIGHT_CONTROL_REALMIC_SET_003_TURN_ON_25_E21_per_file.csv`
- `results/tables/LIGHT_CONTROL_REALMIC_SET_003_TURN_ON_25_E21_summary.csv`
- `results/tables/LIGHT_CONTROL_REALMIC_SET_003_TURN_ON_25_E21_threshold_summary.csv`

### Result
- Total files: 25.
- Correct predictions: 10/25.
- Accuracy: 0.4000.
- Accepted predictions at threshold 0.90: 12/25.
- Accepted correct predictions: 8/12.
- Accepted-command accuracy: 0.6667.
- Accepted wrong predictions: 4/12.

### Threshold Note
At threshold 0.995, accepted-command accuracy was 1.0000, but coverage dropped to 6/25. This is too restrictive for a responsive LED demo by itself.

### Observation
The model predicted `LIGHT_CONTROL` for 10 examples, but also confused the phrase with `SET_ALARM`, `REMINDER`, `CALL_MESSAGE`, and `QUESTION`. This confirms a real-microphone light-command gap.

### Decision
Set 003 justifies targeted real-microphone adaptation. Do not rely only on the downloaded `LIGHT_ON`/`LIGHT_OFF` class folders because those are easier for E21 than laptop real-mic light commands.

## LIGHT_CONTROL_REALMIC_SET_004_TURN_OFF_25

### Date
2026-09-16

### Purpose
Evaluate 25 fresh real-microphone recordings of "turn off the light" using the selected E21 model.

### Input Folder
`C:\Users\Loreen Anne\Documents\Sound Recordings`

### Archived Data
`data/calibration/LIGHT_CONTROL_REALMIC_SET_004_TURN_OFF_25`

### Model
`E21_CNN_DENSE_NODROPOUT_1000PI_BESTVAL`

### Output Artifacts
- `results/tables/LIGHT_CONTROL_REALMIC_SET_004_TURN_OFF_25_E21_per_file.csv`
- `results/tables/LIGHT_CONTROL_REALMIC_SET_004_TURN_OFF_25_E21_summary.csv`
- `results/tables/LIGHT_CONTROL_REALMIC_SET_004_TURN_OFF_25_E21_threshold_summary.csv`
- `results/tables/LIGHT_CONTROL_REALMIC_SET_003_004_COMBINED_E21_summary.csv`
- `results/tables/LIGHT_CONTROL_REALMIC_SET_003_004_COMBINED_E21_threshold_summary.csv`

### Result
- Total files: 25.
- Correct predictions: 4/25.
- Accuracy: 0.1600.
- Accepted predictions at threshold 0.90: 11/25.
- Accepted correct predictions: 1/11.
- Accepted-command accuracy: 0.0909.
- Accepted wrong predictions: 10/11.

### Combined Light Result
Combining Set 003 and Set 004 gives 50 real-microphone light-command clips:
- Correct predictions: 14/50.
- Accuracy: 0.2800.
- Accepted predictions at threshold 0.90: 23/50.
- Accepted correct predictions: 9/23.
- Accepted-command accuracy: 0.3913.
- Accepted wrong predictions: 14/23.

### Observation
The model has a severe deployment-microphone weakness for light commands, especially "turn off the light." Thresholding is not enough because many wrong predictions are highly confident.

### Decision
Proceed to targeted real-microphone `LIGHT_CONTROL` adaptation/evaluation. The downloaded class folders are useful supplemental data but are not sufficient evidence for reliable live LED control.

## E23_LIGHT_REALMIC_ADAPT_E21_REPLAY

### Date
2026-09-16

### Purpose
Fine-tune E21 for real-microphone `LIGHT_CONTROL` using a strict train/holdout split and original-dataset replay.

### Adaptation Split
- Train/adaptation: 30 real-mic light clips.
  - 15 from `LIGHT_CONTROL_REALMIC_SET_003_TURN_ON_25`.
  - 15 from `LIGHT_CONTROL_REALMIC_SET_004_TURN_OFF_25`.
- Holdout evaluation: 20 real-mic light clips.
  - 10 from `LIGHT_CONTROL_REALMIC_SET_003_TURN_ON_25`.
  - 10 from `LIGHT_CONTROL_REALMIC_SET_004_TURN_OFF_25`.

### Training Configuration
- Base model: `E21_CNN_DENSE_NODROPOUT_1000PI_BESTVAL`.
- Replay examples: 880 original-dataset train examples.
- Learning rate: 0.0001.
- Epochs: 8.
- Best epoch selected: 3.
- Threshold: 0.90.

### Output Artifacts
- `training/fine_tune_light_realmic.py`
- `models/cnn/E23_LIGHT_REALMIC_ADAPT_E21_REPLAY_weights.npz`
- `models/cnn/E23_LIGHT_REALMIC_ADAPT_E21_REPLAY_normalization.npz`
- `results/tables/E23_LIGHT_REALMIC_ADAPT_E21_REPLAY_metrics.json`
- `results/tables/E23_LIGHT_REALMIC_ADAPT_E21_REPLAY_realmic_light_holdout_predictions.csv`
- `results/tables/E23_LIGHT_REALMIC_ADAPT_E21_REPLAY_official_validation_report.txt`
- `results/tables/E21_vs_E23_realmic_light_holdout_20_comparison.csv`

### Real-Mic Light Holdout Result
- Correct predictions: 16/20.
- Accuracy: 0.8000.
- Accepted predictions at threshold 0.90: 12/20.
- Accepted correct predictions: 12/12.
- Accepted wrong predictions: 0/12.

### E21 Baseline On Same Holdout
- Correct predictions: 4/20.
- Accuracy: 0.2000.
- Accepted predictions at threshold 0.90: 6/20.
- Accepted correct predictions: 2/6.
- Accepted wrong predictions: 4/6.

### Official Validation Result
- Accuracy: 0.7933.
- Macro-F1: 0.7912.

### Observation
E23 improves the target deployment behavior for real-mic light commands, but it lowers official validation performance compared with E21. This is a clear tradeoff between task-specific adaptation and general validation performance.

### Decision
Keep E21 as the general validation baseline. Use E23 as the current light-command deployment candidate for further microphone testing, especially on the Raspberry Pi microphone.

## Deployment Artifact

### Artifact ID
PI_DEPLOYMENT_PACKAGE_20260916

### Date
2026-09-16

### Purpose
Prepare the offline Raspberry Pi 5 package before hardware arrives.

### Contents
- Pi inference script for WAV files.
- Pi record-and-predict dry-run script using `arecord`.
- GPIO LED wiring test script.
- E23 deployment-candidate model artifacts.
- E21 general-baseline model artifacts.
- Preprocessing and CNN architecture code required for local inference.
- Pi setup guide, microphone validation protocol, manifest, and readiness report.

### Result
Package folder created at `deployment/vcm_pi_package/`.
Zip archive created at `deployment/vcm_pi_deployment_package.zip`.

### Verification
`predict_wav_pi.py` successfully classified an existing calibration WAV as `LIGHT_CONTROL` with confidence 0.999995 using E23.

### Decision
Ready for Pi-side microphone validation. Not yet ready to claim Raspberry Pi latency, microphone accuracy, or GPIO behavior because the hardware has not been tested.

## PI_MIC_ALL_COMMAND_5X_E23_20260918

### Date
2026-09-18

### Purpose
Evaluate whether the Raspberry Pi 5 microphone path can recognize multiple
demo command labels reliably enough for full-command live activation.

### Dataset Version
User-recorded Raspberry Pi microphone files under
`pi_validation/all_commands_5x/` on the Raspberry Pi.

### Train/Validation/Test Split
No training split. This was an on-device validation sweep only.

### Model
Pi deployment CNN package, using the current Raspberry Pi inference scripts.

### Features
16 kHz mono audio converted to the same `(398, 40)` log-Mel feature matrix used
by the training pipeline.

### Hyperparameters
Prediction confidence threshold: 0.90.

### Training Configuration
NOT APPLICABLE.

### Result
Completed from user-provided Raspberry Pi terminal output/PDF capture.

### Accuracy
47/75 correct broad-intent predictions, or 0.6267.

### Precision
NOT MEASURED.

### Recall
NOT MEASURED.

### F1
NOT MEASURED.

### Macro-F1
NOT MEASURED.

### Confusion Matrix Location
NOT CREATED.

### Model Size
NOT RE-MEASURED.

### Latency
NOT YET MEASURED.

### RAM
NOT YET MEASURED.

### CPU
NOT YET MEASURED.

### Pi Setup Evidence
- SSH access to Raspberry Pi works.
- Raspberry Pi OS booted successfully.
- Python 3.13.5 available on the Pi.
- TensorFlow 2.21.0 imports successfully on the Pi.
- Root filesystem has approximately 117G total size, confirming the 128GB card is usable.
- USB microphone is detected by ALSA as card 2, device 0.
- Recording works with `arecord -D plughw:2,0 -r 16000 -c 1 -f S16_LE`.
- Pi-side preprocessing produced `(64000,)` audio and `(398, 40)` features for a 4-second recording.

### Label Summary
- `ALARM`: 5/5 correct, 0 wrong accepted.
- `BRIGHTNESS`: 5/5 correct, 0 wrong accepted.
- `CALL`: 3/5 correct, 1 wrong accepted.
- `LIGHT_OFF`: 5/5 correct, 0 wrong accepted.
- `LIGHT_ON`: 5/5 correct, 0 wrong accepted, but 1 correct prediction was rejected below threshold.
- `LIST_REMINDERS`: 5/5 correct, 0 wrong accepted.
- `MESSAGE`: 5/5 correct, 0 wrong accepted.
- `NEXT`: 0/5 correct, 3 wrong accepted.
- `PAUSE`: 3/5 correct, 1 wrong accepted.
- `PLAY_MUSIC`: 0/5 correct, 1 wrong accepted.
- `TEMPERATURE`: 1/5 correct, 3 wrong accepted.
- `TIME`: 5/5 correct, 0 wrong accepted.
- `TIMER`: 0/5 correct, 4 wrong accepted.
- `VOLUME_UP`: 0/5 correct, 2 wrong accepted.
- `WEATHER`: 5/5 correct, 0 wrong accepted.

### Observations
The Raspberry Pi deployment path is operational, but all-command recognition is
not reliable enough for a live exam demo. Strong labels exist, especially
`ALARM`, `BRIGHTNESS`, `LIGHT_OFF`, `LIST_REMINDERS`, `MESSAGE`, `TIME`, and
`WEATHER`. Weak labels include `NEXT`, `PLAY_MUSIC`, `TEMPERATURE`, `TIMER`,
and `VOLUME_UP`.

The problem is not solved by lowering the threshold. Earlier 0.70 live trials
accepted more wrong predictions. The next improvement should target the Pi
microphone domain and the weak labels directly.

### Decision
Do not claim all-command exam readiness yet. Create a Pi microphone calibration
set for every raw command label and train or fine-tune a raw-command/subcommand
model with replay. Keep a held-out Pi microphone validation split and require
high accuracy with zero wrong accepted predictions on action-critical commands
before enabling live physical actions.

## Experiment Template

### Experiment ID
E00

### Date
NOT YET EXECUTED

### Purpose
NOT YET EXECUTED

### Dataset Version
NOT YET IDENTIFIED

### Train/Validation/Test Split
NOT YET CREATED

### Model
NOT YET IMPLEMENTED

### Features
NOT YET IMPLEMENTED

### Hyperparameters
NOT YET SET

### Training Configuration
NOT YET SET

### Result
NOT YET EXECUTED

### Accuracy
NOT YET MEASURED

### Precision
NOT YET MEASURED

### Recall
NOT YET MEASURED

### F1
NOT YET MEASURED

### Macro-F1
NOT YET MEASURED

### Confusion Matrix Location
NOT YET CREATED

### Model Size
NOT YET MEASURED

### Latency
NOT YET MEASURED

### RAM
NOT YET MEASURED

### CPU
NOT YET MEASURED

### Observations
NOT YET EXECUTED

### Decision
NOT YET MADE

## Experiment E40_NON_LED_COMMAND_RECOVERY

### Date
2026-09-23

### Purpose
Recover weak non-LED commands after E39 live testing showed a split between
working commands and safe-but-not-ready commands.

### Dataset Version
Pi all-command calibration plus wake-gated live command recovery evidence.
LED/light/color/brightness rows were excluded from the E40 recovery manifest
because board setup and light-control recovery are deferred.

### Training Configuration
Started from the E39 broad command recovery model and trained with:

```text
experiment_id: E40_NON_LED_COMMAND_RECOVERY
base_experiment_id: E39_BROAD_COMMAND_RECOVERY_E38
manifest: pi_validation/all_commands_calibration_15x/manifest.csv
extra_manifest: pi_validation/e40_non_led_command_recovery_20260923/manifest.csv
epochs: 20
batch_size: 32
pi_repeat: 20
learning_rate: 0.0002
```

### Interim Note
This is a recovery/fine-tuning experiment, not a scratch restart. Its purpose is
to improve non-LED responsiveness after the E39 live tests, while preserving the
documented workflow: dataset training, Pi deployment validation, selected Pi
adaptation, and fresh live evaluation.

### Result
RUNNING at the time of this note.

### Decision
Do not promote E40 until final metrics and fresh live wake-gated tests are
available.

## Reporting Integrity Policy

### Date
2026-09-23

### Purpose
Ensure the final machine exercise report corresponds to actual experiments and evidence.

### Policy
Do not convert recovery/adaptation clips into independent final validation. Do not count safe rejections as command execution success. Do not remove wrong executed actions from the record after later guardrail or model improvements.

### Required Reporting Categories

```text
Clean pass
Safe rejection
Wrong executed action
Pending/deferred
```

### Decision
Use the logs, result JSON files, prediction tables, and final fresh validation run as the source of truth for the report.

## Experiment E40_NON_LED_COMMAND_RECOVERY - Final Training and Live Validation Update

### Result
Completed 2026-09-23.

```text
Best epoch: 12
Validation accuracy: 0.968421052631579
Validation macro-F1: 0.9681020733652312
Accepted at threshold 0.90: 86/95
Accepted correct: 85
Accepted wrong: 1
Rejected: 9
```

### Accepted-Wrong Holdout Case

```text
STOP -> NEXT, confidence 0.964598
```

### Guardrail Applied
E40 guardrail policy created with `NEXT: 0.98` to block the `STOP -> NEXT` holdout risk. Existing E39 safety thresholds were carried forward until fresh E40 validation proves they can be relaxed.

### Fresh Live Validation Summary
Clean E40 live passes observed:

```text
STOP, TIMER, PLAY_MUSIC, PAUSE, TIME, WEATHER, TEMPERATURE, LIST_REMINDERS
```

Safe/not-ready E40 live outcomes observed:

```text
NEXT, VOLUME_UP, VOLUME_DOWN, CALL, MESSAGE, CREATE_REMINDER, ALARM
```

### Caveat
`e40_wake_temperature_001` was reused and should not be treated as a clean single file-backed trial. Use `e40_wake_temperature_002` as the clean temperature validation evidence.

### Decision
E40 is a useful recovery candidate but does not yet satisfy all-command final validation. Continue to report it as recovery/fine-tuning evidence and use fresh unique trial ids for any further validation.

## Experiment E40_NON_LED_COMMAND_RECOVERY - Fresh Final Wake-Gated Validation

### Date
2026-09-23

### Scope
Fresh wake-gated live validation was run with unique final trial ids after E40 training completed. The selected deployment stack was:

```text
Wake model: E37_TARGETED_COLOR_VOLUME_FIX
Command model: E40_NON_LED_COMMAND_RECOVERY
Command policy: configs/e40_non_led_command_guardrail_thresholds.json
Evidence dir: pi_validation/wake_gated_live_20260923
Runner: scripts/run_e40_wake_command_usb_demo.sh
```

### Wake-Gate Safety Results
Non-target wake phrases and bare commands did not open the command window:

```text
e40_false_wake_hey_siri_001: UNKNOWN 0.998323, command window closed, no action
e40_false_wake_hey_google_001: WAKE 0.529535 below threshold, command window closed, no action
e40_false_wake_alexa_001: UNKNOWN 0.932652, command window closed, no action
e40_false_wake_hello_001: VOLUME_UP 0.936621, command window closed because label was not WAKE, no action
e40_no_wake_play_music_001: PLAY_MUSIC 0.999936 at wake stage, command window closed, no playback/action
e40_no_wake_weather_001: WEATHER 0.773484 at wake stage, command window closed, no action
```

### Clean Final Positive Passes

```text
e40_final_play_music_001: PLAY_MUSIC 0.986482, media.play_music, hardware_applied true, audible playback observed
e40_final_pause_001: PAUSE 1.000000, media.pause
e40_final_stop_001: STOP 0.999158, media.stop
e40_final_timer_001: TIMER 0.991982, timer.create, 300 seconds
e40_final_time_001: TIME 0.997722, question.time_local, "Local time: 9:43 PM."
e40_final_weather_001: WEATHER 0.997981, question.weather_local
e40_final_temperature_001: TEMPERATURE 0.976030, thermostat.set_temperature, simulated 22 degrees
e40_final_volume_down_001: VOLUME_DOWN 0.999946, media.volume_down
e40_final_create_reminder_001: CREATE_REMINDER 0.991122, reminder.create, "demo reminder"
e40_final_list_reminders_004: LIST_REMINDERS 0.998945, reminder.list, returned stored demo reminder
```

### Safe Rejections / Not Final Validated Under E40

```text
e40_final_volume_up_001: expected VOLUME_UP, predicted PAUSE 0.802050, rejected, no action
e40_final_volume_up_002: expected VOLUME_UP, predicted VOLUME_DOWN 0.660885, rejected, no action
e40_final_next_001: wake confidence 0.742216 below threshold, command window closed, no action
e40_final_next_002: expected NEXT, predicted NEXT 0.622830 below NEXT 0.98 threshold, rejected, no action
e40_final_alarm_001: expected ALARM, predicted ALARM 0.499390, rejected, no action
e40_final_alarm_002: expected ALARM, predicted ALARM 0.843656, rejected, no action
e40_final_call_001: expected CALL, predicted VOLUME_DOWN 0.408792, rejected, no action
e40_final_message_001: expected MESSAGE, predicted MESSAGE 0.529292, rejected, no action
```

### Invalid / Aborted Trial

```text
e40_final_list_reminders_001: wake accepted, but no command was spoken by the tester. The run later produced a low-confidence CREATE_REMINDER rejection after a delayed output. This is not counted as a LIST_REMINDERS command failure or pass.
```

Additional list-reminders replacements:

```text
e40_final_list_reminders_002: wake confidence 0.899246, just below 0.90, command window closed
e40_final_list_reminders_003: UNKNOWN 0.661868 at wake stage, command window closed
e40_final_list_reminders_004: clean pass
```

### Final E40 Status
E40 final validation produced 10 clean positive command passes and 6 wake-gate safety passes. It also preserved safe rejections for commands that were not stable enough to execute. This is honest evidence of partial final readiness, not a 100/100 all-command claim.

## Experiment E41_FUNCTIONAL_NON_LED_RECOVERY - Planned

### Date
2026-09-23

### Motivation
E40 is not yet accurate enough for a robust functional VCM. It works for a strong subset of non-LED commands, but several commands still fail under clean same-speaker live Pi conditions. Distance, volume variation, noise, and non-Loreen speakers have not yet been introduced, so command recognition should be strengthened first.

### Target Commands

```text
VOLUME_UP
NEXT
ALARM
CALL
MESSAGE
```

### Current Failure Modes To Recover

```text
VOLUME_UP: live Pi audio misrecognized as PAUSE or VOLUME_DOWN
NEXT: predicted as NEXT in some trials but confidence too low for the NEXT guardrail
ALARM: predicted as ALARM in some trials but confidence below threshold
CALL: misrecognized as other commands such as VOLUME_DOWN
MESSAGE: predicted as MESSAGE in some trials but confidence below threshold
```

### Non-Targets / Preserve
The following commands should be protected with replay/maintenance evidence so E41 does not regress:

```text
PLAY_MUSIC
PAUSE
STOP
VOLUME_DOWN
TIME
WEATHER
TEMPERATURE
TIMER
CREATE_REMINDER
LIST_REMINDERS
```

### Architecture Assessment

```text
Routing/action layer: mostly working for non-LED commands when the correct raw label is accepted
Main weakness: live Pi command recognition robustness
Guardrails: working as safety controls; they prevent wrong actions but do not solve recognition
Wake gate: functional enough for current tests but should remain monitored
LED/light controls: deferred until board setup
Continuous demo loop: still missing; current runner is single interaction per script invocation
```

### E41 Success Criteria
E41 should improve the target commands using adaptation data, then be validated with fresh live trials not used for training. Do not count adaptation clips as final proof.

### Recording Condition Decision
E41 focused recovery recordings should be made under clean room conditions. Background neighbor singing/noise observed on 2026-09-23 should not be used for E41 because the experiment is intended to recover clean same-speaker command recognition first. Noise/distance/non-Loreen recordings should be treated as later robustness experiments.

### Correction Before E41 Training
Any `NEXT` clips recorded while saying `skip song` must be deleted and excluded from the E41 manifest. The target spoken phrase for the `NEXT` command is `next`.

### Planned E41 Workflow

```text
1. Clean or recreate pi_validation/e41_functional_non_led_recovery_20260923.
2. Record focused recovery clips for VOLUME_UP, NEXT, ALARM, CALL, MESSAGE.
3. Train E41_FUNCTIONAL_NON_LED_RECOVERY with recovery data and maintenance/replay protection.
4. Record spoken WAV response actions while training runs.
5. Connect routed non-LED intents to WAV responses.
6. Validate E41 using fresh wake-gated live trials with new ids.
7. Only after clean recognition improves, test robustness separately.
```

### Robustness Reporting Rule
Random command order can be supported by the pipeline, especially once a continuous loop is added. Random-speaker performance must be tested and reported separately from same-speaker clean validation.

## Experiment Phase C - Frozen E41 Baseline Validation

### Date
2026-09-25 to 2026-09-26

### Purpose
Establish a frozen baseline across the actual assignment command scope before
making new model, threshold, data, routing, or action changes.

### Frozen Stack

```text
Wake model: E37_TARGETED_COLOR_VOLUME_FIX
Command model: E41_FUNCTIONAL_NON_LED_RECOVERY
Command threshold policy: E40_NON_LED_COMMAND_GUARDRAIL_THRESHOLDS
Preprocessing: configs/preprocessing.json
CNN config: configs/cnn_fastbn_dense_nodropout_raw19.json
Runner: scripts/run_e41_wake_command_usb_demo.sh
```

### Evidence

```text
outputs/pi_evidence_pullback_20260925_214022/
PHASE_C_TRIAL_TABLE.csv
PHASE_C_BASELINE_SUMMARY_20260925.md
```

Pullback integrity:

```text
Extracted files: 614
SHA256 manifest rows: 615
Missing files: 0
Hash mismatches: 0
Phase C result JSON files parsed: 27
```

### Result

```text
Positive raw labels covered: 19/19
Full PASS: 10
PARTIAL PASS: 2
FAIL: 7
Valid no-action probes: 6
PASS-SAFE no-action probes: 6
Invalid/procedure trial excluded: 1
```

### Failure-Layer Summary

```text
VCM classification: 3
confidence/rejection: 4
response/output: 2
```

### Interpretation
Phase C is a legitimate diagnostic baseline. It is not final completion. The
most serious failure is `CREATE_REMINDER` being accepted as `LIST_REMINDERS`,
which executed the wrong reminder action. `LIGHT_OFF` and `NEXT` should be
treated as output/action-path issues first, not model-training failures.

## Experiment E43_TARGETED_COMMAND_RECOVERY - Proposed

### Date
2026-09-26

### Status
Proposed only. Training has not started.

### Purpose
Target the actual Phase C failures without broad, uncontrolled retraining.

### Initial Fixed Variables

```text
Architecture: configs/cnn_fastbn_dense_nodropout_raw19.json
Preprocessing: configs/preprocessing.json
Threshold policy during initial training/evaluation: E40_NON_LED_COMMAND_GUARDRAIL_THRESHOLDS
Wake model: E37_TARGETED_COLOR_VOLUME_FIX
Router/action layer: unchanged
```

### Proposed Recovery Targets

```text
Priority A:
- CREATE_REMINDER vs LIST_REMINDERS
- LIGHT_ON
- COLOR

Priority B:
- PLAY_MUSIC
- BRIGHTNESS
- PAUSE
- VOLUME_DOWN

Separate non-model work:
- LIGHT_OFF output/action path
- NEXT output/action path

Separate wake work:
- silence
- false wake phrases
- wake variability
```

### Success Rule
E43 must be compared against Phase C using fresh validation recordings that were
not used as recovery/training clips. Wrong accepted actions remain worse than
safe rejections.

## Output Path Retest - LIGHT_OFF and NEXT Direct WAV Playback

### Date
2026-09-26

### Purpose
Test whether the Phase C static/uncertain output for `LIGHT_OFF` and `NEXT` was caused by corrupted response WAV files or the HDMI/LCD playback path.

### Command

```bash
aplay -D plughw:CARD=vc4hdmi0,DEV=0 pi_responses/light_off.wav
aplay -D plughw:CARD=vc4hdmi0,DEV=0 pi_responses/next.wav
```

### Result
Both files played clearly according to the user.

### Interpretation
This is a non-model finding. The response WAV files and direct audio output device work. Remaining investigation should focus on action-layer invocation or live command timing/path, not command-model retraining.

## 2026-09-26 - LIGHT_OFF Response Mapping Fixed and Retested

### Objective
Resolve the Phase C `LIGHT_OFF` response/output partial pass without changing the VCM model.

### Evidence
Direct playback of `pi_responses/light_off.wav` was clear, but action-layer execution initially returned `hardware_applied: false` and produced no clear response. Inspection showed `light.off` was not mapped in `RESPONSE_AUDIO_BY_ACTION`.

### Intervention
Added response mappings on the Pi:

```text
light.on -> light_on.wav
light.off -> light_off.wav
```

A backup was created on the Pi:

```text
actions/command_actions.py.bak_light_audio_20260926
```

### Retest

```bash
python -m actions.command_actions \
  --intent LIGHT_CONTROL \
  --slot light_action=off \
  --phrase "lights off"
```

Result:

```json
{
  "intent": "LIGHT_CONTROL",
  "status": "executed",
  "action": "light.off",
  "hardware_applied": true
}
```

User heard: "switching the light off".

### Interpretation
The Phase C `LIGHT_OFF` partial pass was a response-audio mapping/software-output issue, not a VCM classification failure. No model, preprocessing, or threshold change was involved.

## 2026-09-26 - NEXT Action Output Retested

### Objective
Confirm whether the Phase C `NEXT` partial pass was a model/routing issue or an output-evidence issue.

### Retest

```bash
python -m actions.command_actions \
  --intent MEDIA_CONTROL \
  --slot media_action=next \
  --phrase "next"
```

### Result
The action layer returned:

```json
{
  "intent": "MEDIA_CONTROL",
  "status": "executed",
  "action": "media.next",
  "confidence": 1.0,
  "accepted": true,
  "hardware_applied": true
}
```

User reported clear playback.

### Interpretation
`NEXT` is not an E43 model-training target based on current evidence. The VCM classification, routing, action execution, and response output path are all working in the action-layer retest. Keep `NEXT` in fresh regression validation.

## 2026-09-26 - E43 Specification Updated After Output Repairs

### Purpose
Prevent E43 from spending model-training effort on failures that were already proven to be output/action-layer issues.

### Inputs
- Phase C trials: `phase_c_light_off_20260925_001`, `phase_c_next_20260925_002`
- 2026-09-26 direct WAV playback retest
- 2026-09-26 action-layer retests for `LIGHT_OFF` and `NEXT`
- Decisions `D019` and `D020`

### Result
`PHASE_E43_EXPERIMENT_SPEC_20260925.md` now records `LIGHT_OFF` and `NEXT` as resolved outside model training and keeps them as regression-validation targets.

### Interpretation
E43 remains targeted at command-model/class-separation and confidence/rejection issues. No architecture, preprocessing, threshold, wake, or model-training change has been made yet.

## 2026-09-27 - E43 Recovery Data Collection Plan

### Experiment ID
`E43_TARGETED_COMMAND_RECOVERY`

### Data Version
`E43_TARGETED_RECOVERY_DATA_V1`

### Purpose
Collect recovery-only Pi microphone clips for the remaining Phase C model/confidence failures before any E43 training.

### Planned Output Folder
`pi_validation/e43_targeted_recovery_20260927_v1/`

### Planned Labels
Core targets, 10 clips each:

- `CREATE_REMINDER`
- `LIST_REMINDERS`
- `LIGHT_ON`
- `COLOR`
- `PLAY_MUSIC`
- `BRIGHTNESS`
- `PAUSE`
- `VOLUME_DOWN`

Contrast/regression targets, 5 clips each:

- `LIGHT_OFF`
- `VOLUME_UP`
- `TEMPERATURE`

### Status
Collection plan prepared. No training has started.

## 2026-09-27 - E43 Recovery Collection Block 1 Verification

### Labels
- `CREATE_REMINDER`
- `LIST_REMINDERS`

### Captured Files
- `CREATE_REMINDER`: 10 WAVs
- `LIST_REMINDERS`: 10 WAVs

### Format Check
All listed WAV files:

- sample rate: 16000 Hz
- channels: 1
- sample width: 2 bytes
- duration: 4.0 seconds

### Manifest Check
`manifest.csv` line count: 22

Expected line count: 21

### Status
Audio files pass format verification. Manifest must be inspected for one extra row before further collection or training.

## 2026-09-27 - E43 Recovery Collection Block 2 Verification

### Labels
- `LIGHT_ON`
- `COLOR`

### Captured Files
- `LIGHT_ON`: 10 WAVs
- `COLOR`: 10 WAVs

### Folder Totals After Block 2
- `CREATE_REMINDER`: 10 WAVs
- `LIST_REMINDERS`: 10 WAVs
- `LIGHT_ON`: 10 WAVs
- `COLOR`: 10 WAVs

### Manifest Check
`manifest.csv` line count: 41

Rows by label:

- `CREATE_REMINDER`: 10
- `LIST_REMINDERS`: 10
- `LIGHT_ON`: 10
- `COLOR`: 10

### Format Check
All checked `LIGHT_ON` and `COLOR` WAV files:

- sample rate: 16000 Hz
- channels: 1
- sample width: 2 bytes
- duration: 4.0 seconds

### Status
Block 2 passes collection and metadata checks. No training has started.

## 2026-09-27 - E43 Recovery Collection Block 3 Verification

### Labels
- `PLAY_MUSIC`
- `BRIGHTNESS`
- `PAUSE`
- `VOLUME_DOWN`

### Captured Files
- `PLAY_MUSIC`: 10 WAVs
- `BRIGHTNESS`: 10 WAVs
- `PAUSE`: 10 WAVs
- `VOLUME_DOWN`: 10 WAVs

### Folder Totals After Block 3
- Total labels captured: 8
- Total WAVs captured: 80
- `manifest.csv` line count: 81

### Format Check
All checked WAV files in the confidence/rejection block:

- sample rate: 16000 Hz
- channels: 1
- sample width: 2 bytes
- duration: 4.0 seconds

### Status
Block 3 passes collection and metadata checks. No training has started.

## 2026-09-27 - E43 Recovery Collection Final Verification

### Experiment ID
`E43_TARGETED_COMMAND_RECOVERY`

### Data Version
`E43_TARGETED_RECOVERY_DATA_V1`

### Final Captured Labels
10 clips each:

- `CREATE_REMINDER`
- `LIST_REMINDERS`
- `LIGHT_ON`
- `COLOR`
- `PLAY_MUSIC`
- `BRIGHTNESS`
- `PAUSE`
- `VOLUME_DOWN`

5 clips each:

- `LIGHT_OFF`
- `VOLUME_UP`
- `TEMPERATURE`

### Verification
- total WAV files: 95
- manifest line count: 96
- full format check: `bad_files 0`
- sample rate: 16000 Hz
- channels: 1
- sample width: 2 bytes
- expected duration: 4.0 seconds

### Status
Recovery collection complete. No training has started. Next required step is evidence pullback, hash verification, and Windows-side inventory.

## 2026-09-27 - E43 Recovery Pullback Verification

### Pullback Folder
`outputs/e43_recovery_pullback_20260927_104105/`

### Verification
- total WAV files: 95
- `manifest.csv` rows: 96
- SHA256 CSV rows: 98

### Label Counts
- `BRIGHTNESS`: 10
- `COLOR`: 10
- `CREATE_REMINDER`: 10
- `LIGHT_OFF`: 5
- `LIGHT_ON`: 10
- `LIST_REMINDERS`: 10
- `PAUSE`: 10
- `PLAY_MUSIC`: 10
- `TEMPERATURE`: 5
- `VOLUME_DOWN`: 10
- `VOLUME_UP`: 5

### Status
E43 recovery data has been pulled back and hashed. No training has started. Next step is inventory/training-readiness audit.

## 2026-09-27 - E43 Training-Readiness Audit

### Audit File
`PHASE_E43_TRAINING_READINESS_AUDIT_20260927.md`

### Result
PASS

### Evidence
- pulled recovery WAV files: 95
- manifest data rows: 95
- duplicate manifest WAV paths: 0
- missing manifest targets: 0
- extra WAV files: 0
- normalized SHA rows: 97
- normalized SHA missing/extra rows: 0 / 0

### Status
Recovery data is ready for use as E43 training/recovery input. No training has started.

## 2026-09-27 - E43 Training Command Specification

### Specification File
`PHASE_E43_TRAINING_COMMAND_SPEC_20260927.md`

### Planned Experiment ID
`E43_TARGETED_COMMAND_RECOVERY`

### Base Experiment
`E41_FUNCTIONAL_NON_LED_RECOVERY`

### Training Inputs
- base manifest: `data/calibration/pi_validation/all_commands_calibration_15x/manifest.csv`
- E43 adaptation manifest: `outputs/e43_recovery_pullback_20260927_104105/e43_targeted_recovery_20260927_v1/manifest_e43_adaptation_for_training.csv`

### Planned Counts
- base adaptation: 190
- base holdout: 95
- E43 adaptation: 95
- E43 holdout: 0
- labels: 19

### Status
Command defined. Training has not started.

## 2026-09-27 - Interrupted Full E43 Training Attempt

### Experiment ID
`E43_TARGETED_COMMAND_RECOVERY`

### Command Status
Interrupted before artifact creation.

### Result
No E43 model, normalization, metrics, history, labels, or prediction artifacts were written.

### Reason For Interruption
The full repeat-20 run consumed CPU for an extended period without producing visible training progress or artifacts. To avoid wasting time on an opaque run, the process was interrupted and a bounded smoke run was specified.

### Follow-Up
Created `PHASE_E43_TRAINING_SMOKE_PLAN_20260927.md` for `E43_TARGETED_COMMAND_RECOVERY_SMOKE`.

## 2026-09-27 - E43 Smoke Training Result

### Experiment ID
`E43_TARGETED_COMMAND_RECOVERY_SMOKE`

### Status
Completed.

### Artifacts
- `models/cnn/E43_TARGETED_COMMAND_RECOVERY_SMOKE_weights.npz`
- `models/cnn/E43_TARGETED_COMMAND_RECOVERY_SMOKE_normalization.npz`
- `results/tables/E43_TARGETED_COMMAND_RECOVERY_SMOKE_history.csv`
- `results/tables/E43_TARGETED_COMMAND_RECOVERY_SMOKE_labels.json`
- `results/tables/E43_TARGETED_COMMAND_RECOVERY_SMOKE_metrics.json`
- `results/tables/E43_TARGETED_COMMAND_RECOVERY_SMOKE_pi_holdout_predictions.csv`

### Key Metrics
- holdout accuracy: 0.8842105263157894
- macro-F1: 0.8851674641148325
- accepted wrong at threshold 0.90: 7

### Decision
Do not promote the smoke model. Use it only as proof that the training path works.

## 2026-09-27 - E43 Smoke Regression Analysis

### Result
Smoke model not promoted.

### Evidence
- `PHASE_E43_SMOKE_REGRESSION_ANALYSIS_20260927.md`
- `results/tables/E43_SMOKE_VS_E41_PER_LABEL_COMPARISON.csv`

### Decision
The next E43 candidate should be cautious: preserve E41 normalization/checkpoint behavior and avoid aggressive adaptation that increases wrong accepted commands.

## 2026-09-27 - E43 Cautious Candidate Defined

### Experiment ID
`E43_TARGETED_COMMAND_RECOVERY_CAUTIOUS`

### Objective
Train a safer targeted recovery candidate after the smoke model over-adapted and increased wrong accepted predictions.

### Hypothesis
Preserving E41 normalization and using a smaller update from E41 weights may recover weak target labels while reducing the guardrail regressions observed in the smoke model.

### Fixed Variables
- Base model: `E41_FUNCTIONAL_NON_LED_RECOVERY`
- Architecture: `configs/cnn_fastbn_dense_nodropout_raw19.json`
- Preprocessing: `configs/preprocessing.json`
- Label mapping: `results/tables/E41_FUNCTIONAL_NON_LED_RECOVERY_labels.json`
- Base normalization: `models/cnn/E41_FUNCTIONAL_NON_LED_RECOVERY_normalization.npz`
- Base holdout split: `data/calibration/pi_validation/all_commands_calibration_15x/manifest.csv`

### Changed Variables
- Training script: `training/train_pi_fresh_miniset_recovery.py`
- Fresh recovery manifest: `manifest_e43_fresh_style_for_cautious_training.csv`
- Learning rate: 0.00003
- Epochs: 4
- Pi repeat: 4
- Fresh repeat: 2
- Replay per raw label: 0
- Seed: 4344

### Data
- E43 recovery clips: 95
- Usage: recovery/training only, not final validation

### Status
Specification complete. Training not yet run at this log entry.

## 2026-09-27 - E43 Cautious Candidate Result

### Experiment ID
`E43_TARGETED_COMMAND_RECOVERY_CAUTIOUS`

### Status
Completed.

### Artifacts
- `models/cnn/E43_TARGETED_COMMAND_RECOVERY_CAUTIOUS_weights.npz`
- `models/cnn/E43_TARGETED_COMMAND_RECOVERY_CAUTIOUS_normalization.npz`
- `results/tables/E43_TARGETED_COMMAND_RECOVERY_CAUTIOUS_history.csv`
- `results/tables/E43_TARGETED_COMMAND_RECOVERY_CAUTIOUS_labels.json`
- `results/tables/E43_TARGETED_COMMAND_RECOVERY_CAUTIOUS_metrics.json`
- `results/tables/E43_TARGETED_COMMAND_RECOVERY_CAUTIOUS_pi_holdout_predictions.csv`
- `results/tables/E43_TARGETED_COMMAND_RECOVERY_CAUTIOUS_fresh_miniset_predictions.csv`

### Holdout Metrics
- examples: 95
- accuracy: 0.9157894736842105
- macro-F1: 0.9156831472620945
- accepted wrong at threshold 0.90: 2

### Comparison
E41 was re-evaluated on the same 95-example holdout for fair comparison:

- E41 current95 accuracy: 0.9473684210526315
- E41 current95 macro-F1: 0.947900053163211
- E41 current95 accepted wrong at threshold 0.90: 2

### Decision
Do not promote the cautious model. It reduces smoke regressions but does not outperform E41 and has poor E43 recovery `COLOR` behavior.

## 2026-09-27 - E43 Cautious Recovery Error Analysis

### Input
`results/tables/E43_TARGETED_COMMAND_RECOVERY_CAUTIOUS_fresh_miniset_predictions.csv`

### Output
- `PHASE_E43_CAUTIOUS_RECOVERY_ERROR_ANALYSIS_20260927.md`
- `results/tables/E43_CAUTIOUS_FRESH_RECOVERY_ERROR_SUMMARY.csv`
- `results/tables/E43_CAUTIOUS_FRESH_RECOVERY_ERRORS.csv`

### Result
- total recovery errors: 24
- wrong accepted recovery errors at threshold 0.90: 7
- `COLOR`: 0/10 correct, 0 wrong accepted
- `CREATE_REMINDER`: 4/10 correct, 2 wrong accepted
- `VOLUME_DOWN`: 8/10 correct, 2 wrong accepted

### Decision
No further training until recovery audio/data and class-separation failures are inspected.

## 2026-09-27 - E43 Recovery Audio/Data Inspection

### Objective
Determine whether E43 recovery failures are caused by obvious audio-quality problems or data/phrase coverage.

### Result
Audio QC and data inspection completed.

### Artifacts
- `PHASE_E43_RECOVERY_AUDIO_DATA_INSPECTION_20260927.md`
- `results/tables/E43_RECOVERY_AUDIO_QC_JOINED_WITH_CAUTIOUS_PREDICTIONS.csv`
- `results/tables/E43_RECOVERY_AUDIO_QC_BY_LABEL.csv`
- `results/tables/E43_RECOVERY_AUDIO_QC_FLAGGED_CLIPS.csv`
- `results/tables/E43_RECOVERY_E41_VS_CAUTIOUS_SUMMARY.csv`
- `results/tables/E43_RECOVERY_E41_VS_CAUTIOUS_BY_LABEL.csv`

### Key Result
`COLOR` failure is not explained by gross audio quality. The likely issue is phrase coverage: older calibration used `color red`, while recovery/live baseline used `color`.

### Decision
Do not train again until a focused data plan accounts for the `COLOR` phrase mismatch.

## 2026-09-27 - E44 Focused Recovery Data Plan

### Data Version
`E44_FOCUSED_RECOVERY_DATA_V1`

### Purpose
Collect focused recovery data for the `COLOR` phrase mismatch and remaining wrong-accept contrast pairs.

### Planned Clips
- 20 `COLOR` clips: 10 `color`, 10 `color red`
- 20 `COLOR` confusion contrast clips: `CALL`, `TIME`, `TEMPERATURE`, `STOP`
- 20 wrong-accept contrast clips: `CREATE_REMINDER`, `LIST_REMINDERS`, `VOLUME_DOWN`, `VOLUME_UP`

### Status
Plan created. Recording not yet pulled back to Windows.

## 2026-09-27 - E44 Pi Recording Verification

### Data Version
`E44_FOCUSED_RECOVERY_DATA_V1`

### Status
Pi-side recording and verification completed.

### Result
- total WAV files: 60
- manifest rows: 61 including header
- rows by label match plan
- audio format bad files: 0

### Evidence
`PHASE_E44_PI_RECORDING_VERIFICATION_20260927.md`

### Next
Pull back to Windows and hash before use in training.

## 2026-09-27 - E44 Pullback And Audio QC

### Data Version
`E44_FOCUSED_RECOVERY_DATA_V1`

### Status
Windows pullback, hashing, and local audio QC completed.

### Evidence
- `PHASE_E44_PULLBACK_AND_QC_20260927.md`
- `outputs/e44_focused_recovery_pullback_20260927_114518/SHA256SUMS.csv`
- `results/tables/E44_RECOVERY_AUDIO_QC.csv`
- `results/tables/E44_RECOVERY_AUDIO_QC_BY_LABEL_PHRASE.csv`

### Result
- WAV files: 60
- manifest rows: 61 including header
- SHA256 rows: 61
- bad audio-format files: 0
- QC flagged clips: 0

### Decision
Proceed to E44 training-readiness audit and derived training manifest. Do not train yet.

## 2026-09-27 - E44 Training Readiness Audit

### Data Version
`E44_FOCUSED_RECOVERY_DATA_V1`

### Status
Passed.

### Evidence
`PHASE_E44_TRAINING_READINESS_AUDIT_20260927.md`

### Result
- derived training manifest created
- rows: 60
- missing derived targets: 0
- trainer loader status: PASS

### Decision
Ready for E44 candidate specification. Training has not started.

## 2026-09-27 - E44 Candidate Specification

### Experiment ID
`E44_FOCUSED_COLOR_RECOVERY_CAUTIOUS`

### Status
Specification prepared. Training not yet run at this log entry.

### Key Configuration
- base model: `E41_FUNCTIONAL_NON_LED_RECOVERY`
- script: `training/train_pi_fresh_miniset_recovery.py`
- combined recovery manifest: `manifest_e43_e44_combined_recovery_for_training.csv`
- recovery clips: 155
- learning rate: 0.00002
- epochs: 4
- Pi repeat: 6
- fresh repeat: 2
- seed: 4444

### Evidence
`PHASE_E44_CANDIDATE_EXPERIMENT_SPEC_20260927.md`

## 2026-09-27 - E44 Candidate Training Result

### Experiment ID
`E44_FOCUSED_COLOR_RECOVERY_CAUTIOUS`

### Status
Completed, not promoted.

### Holdout Metrics
- examples: 95
- accuracy: 0.8947368421052632
- macro-F1: 0.896785670469881
- accepted wrong at threshold 0.90: 1

### Recovery Fit
- examples: 155
- accuracy: 0.6516129032258065
- accepted wrong at threshold 0.90: 22
- `COLOR`: 3/30 correct

### Artifacts
- `models/cnn/E44_FOCUSED_COLOR_RECOVERY_CAUTIOUS_weights.npz`
- `models/cnn/E44_FOCUSED_COLOR_RECOVERY_CAUTIOUS_normalization.npz`
- `results/tables/E44_FOCUSED_COLOR_RECOVERY_CAUTIOUS_metrics.json`
- `results/tables/E44_FOCUSED_COLOR_RECOVERY_CAUTIOUS_pi_holdout_predictions.csv`
- `results/tables/E44_FOCUSED_COLOR_RECOVERY_CAUTIOUS_fresh_miniset_predictions.csv`
- `PHASE_E44_CANDIDATE_TRAINING_RESULT_20260927.md`

### Decision
Do not promote. E44 reduced holdout wrong accepts but degraded holdout accuracy/F1 and did not solve `COLOR`.

## 2026-09-27 - COLOR Command Design Audit

### Status
Completed.

### Evidence
`PHASE_E44_COLOR_COMMAND_DESIGN_AUDIT_20260927.md`

### Result
- `color`: 0/10 for E41, E43 cautious, and E44 cautious
- `color red`: 0/10 for E41, 2/10 for E43 cautious, 3/10 for E44 cautious

### Decision
Stop blind `COLOR` retraining. Treat `COLOR` as unresolved and return to requirements/model-selection audit.

## 2026-09-27 - Requirements And Model-Selection Audit

### Status
Completed.

### Audit Document
`PHASE_R_REQUIREMENTS_MODEL_SELECTION_AUDIT_20260927.md`

### Current Candidate
`E41_FUNCTIONAL_NON_LED_RECOVERY`

### Candidate Comparison
| Candidate | Accuracy | Macro-F1 | Wrong accepted @0.90 | Decision |
|---|---:|---:|---:|---|
| `E41_CURRENT95` | 0.9473684210526315 | 0.947900053163211 | 2 | Current best candidate |
| `E43_CAUTIOUS` | 0.9157894736842105 | 0.9156831472620945 | 2 | Not promoted |
| `E44_CAUTIOUS` | 0.8947368421052632 | 0.896785670469881 | 1 | Not promoted |

### Decision
No new model is promoted. The next work should benchmark/validate the current
E41 candidate or revise unresolved command design, not start another blind
training run.

## 2026-09-27 - E41 Pi Benchmark Plan

### Status
Specification prepared. Benchmark not yet run at this log entry.

### Document
`PHASE_S_E41_PI_BENCHMARK_PLAN_20260927.md`

### Experiment ID Pattern
`E41_PI_BENCHMARK_<timestamp>`

### Fixed Variables
- model: `E41_FUNCTIONAL_NON_LED_RECOVERY`
- CNN config: `configs/cnn_fastbn_dense_nodropout_raw19.json`
- threshold: `0.90`
- threshold policy: `configs/e40_non_led_command_guardrail_thresholds.json`
- repeat: `5`
- warmup: `2`

### Evaluation Data
Saved Phase C positive command WAVs from
`pi_validation/wake_gated_live_20260923/`, excluding the invalid
`phase_c_false_wake_hey_siri_20260925_001_command.wav`.

### Decision
Proceed to Pi benchmark when the user is ready. This benchmark measures
runtime/resource behavior only; it is not final all-command validation.

## 2026-09-27 - E41 Pi Benchmark Result

### Experiment ID
`E41_PI_BENCHMARK_20260927_041313`

### Status
Completed on Pi and archived in Windows evidence tree.

### Candidate
`E41_FUNCTIONAL_NON_LED_RECOVERY`

### Runtime Metrics
- WAV count: 19
- repeated inference count: 95
- model load seconds: 7.9181789939993905
- mean latency ms: 33.334859452607866
- median latency ms: 31.889824000245426
- p95 latency ms: 38.77204550026363
- max latency ms: 40.85485800078459
- accepted count: 65
- rejected count: 30
- CPU percent during benchmark: 99.76415094339622
- temperature: 45.2 C to 47.4 C
- memory used: 578400 KB to 815184 KB

### Artifacts On Pi
- `results/pi_benchmarks/E41_PI_BENCHMARK_20260927_041313_summary.json`
- `results/pi_benchmarks/E41_PI_BENCHMARK_20260927_041313_latency_rows.csv`

### Windows Pullback
- `outputs/e41_pi_benchmark_pullback_20260927_121751/E41_PI_BENCHMARK_20260927_041313_summary.json`
- `outputs/e41_pi_benchmark_pullback_20260927_121751/E41_PI_BENCHMARK_20260927_041313_latency_rows.csv`
- `outputs/e41_pi_benchmark_pullback_20260927_121751/SHA256SUMS.csv`

### SHA256
- summary JSON: `859693CD093C5C9E6CC3AE916389B00D30BA513D0B49DC6EC66D024D4FB01246`
- latency CSV: `D9CA65C30AA04A410B2499D41F532E3AC2760AE2B3143875F64252218EAAE703`

### Decision
The runtime-speed evidence supports real-time Pi inference for E41. It does not
resolve all-command recognition completeness because 30/95 repeated inferences
were rejected under the current threshold policy.

## 2026-09-27 - Remaining Failure Repair Selection

### Status
Completed. No model or thresholds changed.

### Document
`PHASE_T_REMAINING_FAILURE_REPAIR_SELECTION_20260927.md`

### Derived Tables
- `results/tables/PHASE_T_PHASE_C_REMAINING_FAILURES.csv`
- `results/tables/PHASE_T_E41_E40_POLICY_HOLDOUT_ROWS.csv`
- `results/tables/PHASE_T_E41_E40_POLICY_HOLDOUT_SUMMARY.csv`
- `results/tables/PHASE_T_E41_E40_POLICY_HOLDOUT_WRONG_ACCEPTED.csv`
- `results/tables/PHASE_T_E41_E40_POLICY_HOLDOUT_REJECTED_CORRECT.csv`

### E41 Under E40 Policy
- examples: 95
- raw correct: 90
- accepted: 80
- accepted correct: 79
- accepted wrong: 1
- rejected: 15
- rejected correct: 11

### Decision
Next experiment should be specified, not run immediately:
`E45_TARGETED_REMINDER_LIGHTON_CONFIDENCE_REPAIR`. The priority is
`CREATE_REMINDER` vs `LIST_REMINDERS`, then `LIGHT_ON`, then
confidence/rejection labels. `COLOR` remains a command-design issue.

## 2026-09-27 - E45 Targeted Repair Specification

### Status
Specification prepared. Training not started.

### Document
`PHASE_U_E45_TARGETED_REPAIR_SPEC_20260927.md`

### Experiment ID
`E45_TARGETED_REMINDER_LIGHTON_CONFIDENCE_REPAIR`

### Primary Repair Targets
- `CREATE_REMINDER`
- `LIST_REMINDERS`
- `LIGHT_ON`

### Confidence/Rejection Targets
- `PLAY_MUSIC`
- `BRIGHTNESS`
- `PAUSE`
- `VOLUME_DOWN`

### Data Sources
- `E43_TARGETED_RECOVERY_DATA_V1`
- `E44_FOCUSED_RECOVERY_DATA_V1`

### Decision
Build and audit the derived E45 manifest next. Do not train until the manifest
is verified and logged.

## 2026-09-27 - E45 Manifest Readiness Audit

### Status
Passed. Training not started.

### Document
`PHASE_V_E45_MANIFEST_READINESS_AUDIT_20260927.md`

### Manifest
`outputs/e45_targeted_repair_20260927/manifest_e45_targeted_recovery_for_training.csv`

### Data Version
`E45_TARGETED_REPAIR_DATA_V1`

### Result
- rows: 125
- unique WAV paths: 125
- duplicate paths: 0
- missing files: 0
- bad audio files: 0
- excluded `COLOR` rows: 30

### Decision
The manifest/readiness gate has passed. E45 training may be the next experiment
step, but it was not run in this phase.

## 2026-09-27 - E45 Targeted Training Result

### Status
Completed. Candidate not promoted.

### Document
`PHASE_W_E45_TRAINING_RESULT_20260927.md`

### Experiment ID
`E45_TARGETED_REMINDER_LIGHTON_CONFIDENCE_REPAIR`

### Configuration
- Base experiment: `E41_FUNCTIONAL_NON_LED_RECOVERY`
- Training script: `training/train_pi_fresh_miniset_recovery.py`
- Base manifest: `data/calibration/pi_validation/all_commands_calibration_15x/manifest.csv`
- Fresh manifest:
  `outputs/e45_targeted_repair_20260927/manifest_e45_targeted_recovery_for_training.csv`
- Architecture: `configs/cnn_fastbn_dense_nodropout_raw19.json`
- Epochs: 4
- Batch size: 32
- Pi repeat: 6
- Fresh repeat: 2
- Replay per raw label: 0
- Learning rate: 0.00002
- Seed: 4545

### Result
- Training examples: 1390
- Best epoch: 4
- Holdout accuracy: 0.9368421052631579
- Holdout macro-F1: 0.935805422647528
- Targeted recovery accuracy: 0.84

### E40 Policy Comparison
- E41 holdout under E40 policy: 80 accepted, 79 accepted correct, 1 accepted
  wrong, 15 rejected
- E45 holdout under E40 policy: 76 accepted, 73 accepted correct, 3 accepted
  wrong, 19 rejected

### Decision
Do not promote E45. The targeted experiment improved some recovery examples but
increased wrong accepted holdout behavior compared with E41.

## 2026-09-27 - E45 Wrong-Accept Regression Analysis

### Status
Completed. No training performed.

### Document
`PHASE_X_E45_WRONG_ACCEPT_REGRESSION_ANALYSIS_20260927.md`

### Derived Tables
- `results/tables/PHASE_X_E45_WRONG_ACCEPTED_VS_E41_ROWS.csv`
- `results/tables/PHASE_X_E41_WRONG_ACCEPTED_VS_E45_ROWS.csv`
- `results/tables/PHASE_X_E41_E45_WRONG_ACCEPT_CONFUSION_PAIRS.csv`
- `results/tables/PHASE_X_E41_E45_E40_POLICY_CALIBRATION_SUMMARY.csv`
- `results/tables/PHASE_X_E41_E45_TARGET_LABEL_HOLDOUT_COMPARISON.csv`
- `results/tables/PHASE_X_E45_TRAINING_MANIFEST_LABEL_COUNTS.csv`

### Result
E45 removed E41's specific `COLOR -> WEATHER` wrong accept in the offline
holdout table, but introduced `PAUSE -> CALL`, `STOP -> NEXT`, and
`CREATE_REMINDER -> ALARM` wrong accepts. Since `COLOR` was excluded from E45,
this does not resolve the separate COLOR hypothesis.

### Decision
Do not train immediately. If another intervention is attempted, it must be a
safety-focused repair for the actual wrong-accepted pairs.

## 2026-09-27 - E45 Safety Regression Diagnosis

### Status
Completed. No training performed.

### Document
`PHASE_Y_E45_SAFETY_REGRESSION_DIAGNOSIS_20260927.md`

### Derived Tables
- `results/tables/PHASE_Y_E45_SAFETY_REGRESSION_THREE_SAMPLE_COMPARISON.csv`
- `results/tables/PHASE_Y_E45_ADDITIONAL_ACCEPTED_WRONG_REGRESSIONS.csv`
- `results/tables/PHASE_Y_E41_E45_REGRESSION_PAIR_OCCURRENCES.csv`
- `results/tables/PHASE_Y_E41_E45_THREE_REGRESSION_TOPK.csv`

### Result
The three E45 regressions are classifier/confidence-policy regressions, not
router/action-layer failures. Two changed top-1 classifier label, and one
crossed the E40 policy threshold with the same wrong top-1 label.

### Recommendation
Next action B: confidence/rejection calibration or policy analysis is justified
without retraining. The recommendation was not executed.

## 2026-09-27 - E41 Confidence/Rejection Policy Analysis

### Status
Completed. No training, threshold change, router change, action change, or new
audio collection performed.

### Document
`PHASE_Z_E41_CONFIDENCE_REJECTION_POLICY_ANALYSIS_20260927.md`

### Derived Tables
- `results/tables/PHASE_Z_E41_RELEVANT_CLASS_POLICY_OUTCOMES.csv`
- `results/tables/PHASE_Z_E41_RELEVANT_CONFUSION_PAIRS.csv`
- `results/tables/PHASE_Z_E41_CLASS_SPECIFIC_THRESHOLD_WHATIF.csv`
- `results/tables/PHASE_Z_E41_STOP_NEXT_POLICY_ROWS.csv`
- `results/tables/PHASE_Z_E41_SCHEDULING_REMINDER_BOUNDARY_ROWS.csv`

### Result
Existing E41/E40 evidence supports the usefulness of class-specific thresholding
for `STOP -> NEXT` safety and suggests a narrow PAUSE calibration hypothesis.
It does not justify immediate production-threshold changes.

### Recommendation
B. Conduct a narrow class-specific threshold calibration experiment. Not
executed in this phase.

## 2026-09-27 - Phase AA PAUSE Threshold Calibration Specification

### Status
Specification completed. No training, audio collection, threshold change,
router change, action change, or production policy change performed.

### Document
`PHASE_AA_PAUSE_THRESHOLD_CALIBRATION_SPEC_20260927.md`

### Audit Table
- `results/tables/PHASE_AA_PAUSE_DATA_SOURCE_AUDIT.csv`

### Result
The Phase Z PAUSE threshold hypothesis is not validated. Existing PAUSE-related
evidence is either discovery holdout data, recovery/training-linked data, too
small for calibration, or absent. A fresh independent calibration set is
required before evaluating candidate PAUSE thresholds.

### Fixed Baseline
- E41 model weights fixed
- E41 normalization fixed
- E40 policy unchanged
- `NEXT = 0.98` fixed
- router/action layer unchanged

### Recommendation
Collect and evaluate a separate Phase AA calibration set only in a later phase.
Do not execute that experiment or alter thresholds in this phase.

## 2026-09-27 - Phase AA PAUSE Calibration Data Collection Verification

### Status
Completed data collection and integrity verification only. No inference, threshold what-if analysis, model training, threshold edit, router edit, or action-layer edit performed.

### Document
`PHASE_AA_PAUSE_CALIBRATION_DATA_COLLECTION_VERIFICATION_20260927.md`

### Pi Evidence
- dataset: `/home/loreenanne/vcm_pi_package/pi_validation/phase_aa_pause_threshold_calibration_v1_20260927`
- manifest: `/home/loreenanne/vcm_pi_package/pi_validation/phase_aa_pause_threshold_calibration_v1_20260927/manifest.csv`
- SHA256: `/home/loreenanne/vcm_pi_package/pi_validation/phase_aa_pause_threshold_calibration_v1_20260927/SHA256SUMS.csv`

### Verification Result
- WAV count: 100
- manifest data rows: 100
- manifest total lines expected: 101
- missing files: 0
- duplicate trial IDs: false
- duplicate WAV paths: false
- bad/corrupt audio files: 0
- usage fields: all `calibration_not_final_validation`
- separate-from-prior-data path check: true
- PASS: true

### Note
The manifest required a metadata-only CSV repair because `plughw:2,0` was written without CSV quoting and split the device field. The repaired manifest passed verification, and the pre-repair manifest was preserved on the Pi.

### Next Gate
Do not proceed to calibration analysis until explicitly requested.

## 2026-09-27 - Phase AB Frozen E41 Inference And PAUSE Threshold What-If

### Status
Completed on the Raspberry Pi. No training, production-threshold change, E40 change, E41 change, router change, or action-layer change occurred.

### Document
`PHASE_AB_PHASE_AA_PAUSE_CALIBRATION_INFERENCE_RESULT_20260927.md`

### Pi Artifacts
- `/home/loreenanne/vcm_pi_package/results/phase_ab_phase_aa_pause_calibration_20260927/PHASE_AB_PHASE_AA_PAUSE_CALIBRATION_20260927_frozen_e41_e40_per_sample.csv`
- `/home/loreenanne/vcm_pi_package/results/phase_ab_phase_aa_pause_calibration_20260927/PHASE_AB_PHASE_AA_PAUSE_CALIBRATION_20260927_frozen_e41_e40_summary.json`
- `/home/loreenanne/vcm_pi_package/results/phase_ab_phase_aa_pause_calibration_20260927/PHASE_AB_PHASE_AA_PAUSE_CALIBRATION_20260927_pause_threshold_whatif.csv`
- `/home/loreenanne/vcm_pi_package/results/phase_ab_phase_aa_pause_calibration_20260927/PHASE_AB_PHASE_AA_PAUSE_CALIBRATION_20260927_SHA256SUMS.csv`

### Result
Frozen baseline: 100 samples, 58 raw-correct, 42 raw-wrong, 33 accepted-correct, 25 rejected-correct, 10 accepted-wrong, 32 rejected-wrong.

PAUSE threshold what-if: `0.98` recovered 1 PAUSE case; `0.97`, `0.96`, and `0.95` recovered 2 PAUSE cases. No tested PAUSE threshold introduced newly accepted-wrong cases in the calibration set.

### Decision
The Phase Z hypothesis is supported as calibration evidence only. Do not change production thresholds. A later validation experiment is warranted before any threshold promotion.

## 2026-09-27 - Phase AD Fresh Live End-to-End VCM Validation

### Status
Completed live microphone validation only. No model training, E41 modification, E40 modification, threshold edit, router edit, or action-layer edit occurred.

### Frozen Configuration
- Command model: `E41_FUNCTIONAL_NON_LED_RECOVERY`
- Threshold policy: `E40_NON_LED_COMMAND_GUARDRAIL_THRESHOLDS`
- `PAUSE = 0.99`
- `NEXT = 0.98`
- Wake model: `E37_TARGETED_COLOR_VOLUME_FIX`, threshold `0.90`

### Artifacts
- `PHASE_AD_LIVE_VCM_VALIDATION_20260927.md`
- `/home/loreenanne/vcm_pi_package/pi_validation/phase_ad_live_vcm_validation_20260927`
- `/home/loreenanne/vcm_pi_package/results/phase_ad_live_vcm_validation_20260927`

### Measured Metrics
- Total live trials: 65
- Command trials: 57
- No-action trials: 8
- Wake success on command trials: 55/57 = 96.49%
- Raw live E41 accuracy: 39/55 = 70.91%
- E40 acceptance rate: 34/55 = 61.82%
- Accepted-action precision: 30/34 = 88.24%
- Safe rejection rate: 12/16 = 75.00%
- End-to-end action success: 30/57 = 52.63%
- No-action trials with action executed: 0/8

### Accepted-Wrong Cases
- `phase_ad_temperature_002`: `TEMPERATURE -> MESSAGE`, confidence 0.922538, action `communication.message_stub`
- `phase_ad_next_002`: `NEXT -> MESSAGE`, confidence 0.930046, action `communication.message_stub`
- `phase_ad_light_off_003`: `LIGHT_OFF -> LIGHT_ON`, confidence 0.953683, action `light.on`
- `phase_ad_temperature_003`: `TEMPERATURE -> MESSAGE`, confidence 0.985255, action `communication.message_stub`

### Interpretation
The formal holdout remains 94.74% raw accuracy and should not be replaced by the live metric. Phase AD shows that the live end-to-end pipeline currently performs lower than holdout, mostly due to VCM classification failures after successful wake/capture. Further diagnosis is required before broader demonstration.

## 2026-09-27 - Phase AE Live Failure Diagnosis

### Status
Completed diagnostic analysis only. No E41/E40 modification, threshold change, retraining, router edit, action edit, preprocessing edit, wake edit, or recovery dataset creation occurred.

### Artifacts
- `PHASE_AE_LIVE_FAILURE_DIAGNOSIS_20260927.md`
- `results/phase_ae_live_failure_diagnosis_20260927/PHASE_AD_ALL_ERROR_TRIALS.csv`
- `results/phase_ae_live_failure_diagnosis_20260927/PHASE_AD_LIVE_CONFUSION_PAIRS.csv`
- `results/phase_ae_live_failure_diagnosis_20260927/PHASE_AD_ACCEPTED_WRONG_DIAGNOSIS.csv`
- `results/phase_ae_live_failure_diagnosis_20260927/PHASE_AD_WEAK_CLASS_SUMMARY.csv`
- `results/phase_ae_live_failure_diagnosis_20260927/PHASE_AD_CONFIDENCE_POLICY_DIAGNOSIS.csv`
- `results/phase_ae_live_failure_diagnosis_20260927/PHASE_AD_DIAGNOSTIC_AUDIO_INTEGRITY.csv`
- `results/phase_ae_live_failure_diagnosis_20260927/PHASE_AE_LIVE_FAILURE_DIAGNOSIS_20260927_SHA256SUMS.csv`

### Findings
- Phase AD command error rows: 27
- Live raw classification errors after E41 reached: 16
- Accepted wrong: 4
- Safely rejected wrong: 12
- Basic WAV integrity: 65/65 valid diagnostic evidence
- Dominant live failure layer remains VCM classification.

### Weak-Class Evidence
- `CALL`: 0/3 raw correct; possible repeated confusion with `TEMPERATURE`
- `COLOR`: 0/3 raw correct; mixed wrong predictions `CALL`, `TIME`, `TIMER`
- `TEMPERATURE`: 1/3 raw correct; repeated accepted confusion with `MESSAGE`
- `NEXT`: 2/3 raw correct; one accepted confusion with `MESSAGE`
- `LIGHT_OFF`: 1/2 raw correct among E41-reached trials; one accepted confusion with `LIGHT_ON`

### Decision
Proceed only to a separately specified targeted recovery/validation design. Do not train or change thresholds from Phase AE alone.

## Phase AF - Targeted Live Failure Recovery Data Preparation - 2026-09-27
- Objective: prepare fresh targeted recovery data for live VCM classification weaknesses diagnosed in Phase AE.
- Fixed: E41 model weights, E40 thresholds, wake model/threshold, preprocessing, normalization, label mapping, router, and action logic.
- Changed in this phase: no system behavior; only a planned fresh recovery dataset and collection procedure.
- Planned dataset: PHASE_AF_TARGETED_LIVE_RECOVERY_V1, 105 WAV files, usage 
ecovery_training.
- Targets: CALL, COLOR, TEMPERATURE, NEXT, LIGHT_OFF.
- Key confusion boundaries: TEMPERATURE->MESSAGE, NEXT->MESSAGE, LIGHT_OFF->LIGHT_ON.
- Status: specification created; data collection/integrity pending; no training performed.

## Phase AF - Targeted Live Recovery Data Collection Result - 2026-09-27
- Dataset: PHASE_AF_TARGETED_LIVE_RECOVERY_V1.
- Location on Pi: pi_validation/phase_af_targeted_live_recovery_20260927_v1.
- Usage: 
ecovery_training; split: 
ecovery; source phase: PHASE_AF.
- Actual count: 105 WAV files; manifest data rows: 105; manifest total lines: 106.
- Class counts: CALL 10, COLOR 10, TEMPERATURE 10, NEXT 10, LIGHT_OFF 10, MESSAGE 5, TIME 5, WEATHER 5, PAUSE 5, STOP 5, VOLUME_UP 5, VOLUME_DOWN 5, LIGHT_ON 5, BRIGHTNESS 5, CREATE_REMINDER 5, LIST_REMINDERS 5.
- Integrity result: PASS True.
- Leakage/separation result: validation leakage paths 0; no Phase AD/AA/AB/holdout path reuse detected by integrity script.
- Decision: dataset is suitable for consideration in a later separately specified training experiment. No training authorized or performed in Phase AF.

## 2026-09-27 15:35:29 +08:00 - Phase AF Metadata Correction
- Clean metadata statement: Dataset PHASE_AF_TARGETED_LIVE_RECOVERY_V1 uses usage = recovery_training, split = recovery, source_phase = PHASE_AF. No training or production configuration changes occurred.

## Phase AG - E46 Targeted Live Failure Recovery - 2026-09-27
- Experiment ID: E46_TARGETED_LIVE_FAILURE_RECOVERY.
- Objective: test whether verified Phase AF recovery_training data improves Phase AE diagnosed live weak classes without unacceptable regression.
- Fixed: E41 baseline, preprocessing, feature extraction, architecture, label mapping, E41 normalization, frozen E40 policy for offline comparison, router/action logic, production thresholds.
- Changed: training data composition only; added verified Phase AF recovery_training data to E41-authorized adaptation data.
- Training data: 190 E41-authorized adaptation clips repeated 6 times plus 105 Phase AF recovery clips repeated 2 times = 1350 examples.
- Training method: fixed 4 epochs, LR 0.00002, batch size 32, seed 4646, no holdout-based model selection.
- E46 training accuracy: 0.9318518518518518; macro F1: 0.933656464092094.
- Phase AF recovery fit: 62/105 = 0.5904761904761905; macro F1: 0.5089038956686016.
- Frozen 95-example holdout: E46 87/95 = 91.58%, below E41 90/95 = 94.74%.
- Regression: 3 corrections, 6 regressions, 2 unchanged errors, 84 unchanged correct.
- E40 policy: E46 accepted-wrong 2 vs E41 accepted-wrong 1; E46 accepted-action precision 0.972972972972973 vs E41 0.9875.
- Decision: E46 rejected for promotion. E41 remains current evidence-supported candidate.

## Phase AG Post-Experiment Diagnosis - E46 Regression Analysis - 2026-09-27
- Objective: diagnose E46 underperformance relative to E41 without training or modifying the system.
- Artifacts used: E41_vs_E46_REGRESSION_ANALYSIS.csv, E41_vs_E46_HOLDOUT_COMPARISON.csv, E46_E40_POLICY_COMPARISON.csv, E46_E40_POLICY_HOLDOUT_ROWS.csv, E46 metrics and per-class tables.
- Confirmed E41 baseline: 90/95 = 94.74%.
- Confirmed E46 result: 87/95 = 91.58%.
- Regressions/corrections: 3 corrections, 6 regressions, 2 unchanged errors, 84 unchanged correct.
- Six E41-correct -> E46-wrong true labels: LIGHT_ON, LIGHT_ON, STOP, VOLUME_DOWN, CALL, TEMPERATURE.
- Three E41-wrong -> E46-correct true labels: NEXT, BRIGHTNESS, COLOR.
- E46 accepted-wrong under frozen E40: STOP -> NEXT; VOLUME_DOWN -> VOLUME_UP.
- Interpretation: mixed localized regression across target and contrast boundaries, not broad uniform degradation and not solely target-class degradation.
- Decision: E46 remains not promoted; E41 remains frozen.

## Phase AG+ - E46 Confidence / Acceptance Diagnosis - 2026-09-27
- Objective: determine whether E46 changes were caused by top-1 classifier changes, confidence/acceptance changes, or both.
- Inputs: existing frozen 95-example E41/E46 holdout comparison artifacts and frozen E40 thresholds only.
- Artifact discrepancy: the supplied nine-sample list did not fully match saved prediction rows; the diagnostic report uses artifact-defined correctness-flip rows and saves the mismatch table.
- Margin status: second-best predictions/confidences were not present, so confidence margins are NOT AVAILABLE.
- Six regressions: 6/6 were top-1 prediction changes; 4/6 had E40 acceptance/rejection consequences, and 2/6 remained rejected by E40.
- Three improvements: 3/3 were top-1 prediction changes with acceptance/action consequences.
- Accepted-wrong mechanism split: STOP_013.wav was confidence-only acceptance change with same wrong NEXT prediction; VOLUME_DOWN_011.wav was top-1 change plus acceptance consequence.
- Interpretation: E46 regressions are primarily classifier-output changes, with one important confidence-only safety case under frozen E40.
- Decision: no E46 promotion, no threshold change, and no immediate E47 training. E41 remains frozen.

## Strategic Direction - Controlled Candidate Repair - 2026-09-27
- This is a planning standard, not a new experiment.
- Project objective is reframed as making the live Pi VCM work through controlled experiments.
- Target behavior: fresh Pi speech -> HEY PI -> correct VCM intent -> safe acceptance/rejection -> correct deterministic action -> evidence logged.
- High-priority live weaknesses remain CALL, COLOR, TEMPERATURE, NEXT, LIGHT_OFF, plus known safety/confusion areas CREATE_REMINDER/LIST_REMINDERS, LIGHT_ON-related confusion, VOLUME_DOWN, PAUSE confidence, and high-confidence wrong actions.
- Success criterion is reliable accepted actions plus safe rejection of uncertain/wrong predictions, not raw holdout accuracy alone.
- Future candidates require strict promotion gates and fresh Pi/end-to-end validation before replacing E41.

## Phase AH - Targeted Repair Design and Baseline Analysis - 2026-09-27
- Objective: reconcile Phase AG+ artifacts and design the next controlled intervention without training or changing the system.
- Artifact reconciliation: PASS. E41/E46 prediction artifacts, comparison table, and E40 policy rows all match the same 95-example holdout path set.
- Authoritative holdout: data/calibration/pi_validation/all_commands_calibration_15x/manifest.csv, rows 011-015 for each of the 19 raw command labels.
- Authoritative correctness flips: six E41-correct -> E46-wrong and three E41-wrong -> E46-correct rows from E41_vs_E46_REGRESSION_ANALYSIS.csv.
- The previous supplied nine-sample list is not authoritative; it appears to be a prompt/source-list mismatch, not an internal artifact mismatch.
- E41 baseline remains 90/95 = 94.74%; E41 + E40 remains accepted-correct 79, accepted-wrong 1, rejected-correct 11, rejected-wrong 4.
- Live failure inventory preserved Phase AD/AE evidence for CALL, COLOR, TEMPERATURE, NEXT, LIGHT_OFF, LIGHT_ON, VOLUME_DOWN, PLAY_MUSIC, BRIGHTNESS, PAUSE, CREATE_REMINDER, and LIST_REMINDERS.
- Classification problems and acceptance-policy problems were separated. STOP_013 remains the clearest acceptance-policy safety case; most other listed problems are top-1 classifier errors.
- Recommendation: specify a controlled classifier ablation before any future model training. Do not train E47 yet.

## Phase AI - E47 Controlled Classifier Ablation - 2026-09-27
- Objective: test whether a narrow target/contrast classifier intervention can improve documented failure classes without E46-style broad regressions.
- Experiment ID: E47_TARGETED_CLASSIFIER_ABLATION.
- Base: E41 weights and normalization; E41 remains frozen.
- Data used: 190 E41-authorized adaptation clips x1 plus 75 selected Phase AF recovery_training clips x2 = 340 training examples.
- Selected Phase AF classes: CALL, COLOR, TEMPERATURE, NEXT, LIGHT_OFF, MESSAGE, TIME, LIGHT_ON, VOLUME_DOWN, VOLUME_UP.
- Excluded: Phase AD validation clips, Phase AA calibration clips, the 95-example holdout as training data, non-selected Phase AF classes, and new/synthetic data.
- Training config: seed 4747, 3 epochs, batch size 32, learning rate 0.00001, no holdout checkpoint selection.
- Holdout result: E47 79/95 = 83.16% vs E41 90/95 = 94.74%.
- Regression counts: 0 corrections, 11 E41-correct -> E47-wrong regressions, 5 unchanged E41 errors, 79 unchanged correct.
- Target classes: no target class improved; LIGHT_OFF degraded from 5/5 to 3/5.
- Frozen E40: E47 accepted-correct 70, accepted-wrong 3, rejected-correct 9, rejected-wrong 13; accepted-action precision 95.89%.
- Accepted-wrong cases: PAUSE -> CALL, STOP -> NEXT, LIST_REMINDERS -> CREATE_REMINDER.
- Decision: E47 rejected for promotion and should not proceed to fresh live validation.

## Phase AJ - Model / Representation Diagnosis - 2026-09-27
- Objective: diagnose whether remaining VCM failures are more plausibly tied to feature representation, CNN architecture/capacity, class separability, data limitations, or confidence/rejection behavior before any E48 training.
- Inputs: Phase AH authoritative E41 baseline, E41/E45/E46/E47 holdout artifacts, Phase AD/AE live failure evidence, E41 preprocessing/configuration code, and existing data manifests.
- No training was run. No thresholds, models, preprocessing, label mappings, router/action logic, holdout data, Phase AD data, Phase AA data, or historical artifacts were modified.
- E41 baseline preserved: 90/95 = 94.74%; E41 + E40 accepted-correct 79, accepted-wrong 1, rejected-correct 11, rejected-wrong 4.
- E45, E46, and E47 remain rejected. E46 dropped to 87/95 with 2 accepted-wrong cases; E47 dropped to 79/95 with 3 accepted-wrong cases.
- Feature finding: current E41 representation is fixed-window 40-bin log-mel on 4-second peak-normalized audio with no VAD/silence trimming observed. This is a plausible limitation under live conditions but not proven insufficient.
- Architecture finding: E41 uses a deliberately tiny Conv2D CNN with global avg/max pooling and approximately 66k parameters. It may compress temporal detail, but architecture limitation is not proven because E41 performs well on the formal holdout.
- Interpretation: live failures and failed fine-tuning interventions are most consistent with class-separation/top-1 classifier instability plus safety-relevant confidence acceptance behavior. Router/action logic was not the diagnosed source.
- Recommended next path: controlled architecture experiment, design only, to isolate model capacity/temporal-context change while keeping dataset, preprocessing, labels, E40, evaluation protocol, router/actions, and production thresholds fixed.
- Required hard stop observed: no E48, no live validation, no threshold change, and no candidate promotion.

## Phase AK - E48 Controlled Temporal CNN Capacity Probe - 2026-09-27
- Status: E48 INCONCLUSIVE - FURTHER EVIDENCE REQUIRED.
- Execution authorization was received, but the Phase AK pre-training gate failed before training.
- Required architecture source: PHASE_AJ_MODEL_REPRESENTATION_DIAGNOSIS_20260927.md.
- Gate result: Phase AJ did not uniquely specify one executable architecture. It recommended a controlled architecture experiment but described possible changes as temporal/asymmetric convolution capacity or one additional convolutional block.
- Missing required execution details: exact layer sequence, kernel sizes, channel counts, stride, pooling, normalization and activation placement, temporal handling mechanism, final pooling, classifier head, parameter count, and expected model size.
- Required stop statement recorded: E48 design is not sufficiently specified for controlled execution.
- No model was trained, no evaluation was run, no holdout was changed, no E40 threshold was changed, no router/action logic was modified, and no live validation occurred.
- E41 remains frozen; E45/E46/E47 remain rejected.

## Phase AL - E48 Architecture Specification and Pre-Registration - 2026-09-27
- Objective: resolve the Phase AK pre-training block by turning the Phase AJ architecture diagnosis into one uniquely specified E48 architecture.
- Status: E48 FULLY SPECIFIED — READY FOR CONTROLLED TRAINING.
- No training was performed and no model checkpoint was created.
- E41 reference architecture: input 398x40x1; Conv2D 24 3x3 + BN + MaxPool; Conv2D 48 3x3 + BN + MaxPool; Conv2D 96 3x3 + BN + MaxPool; global average + global max pooling; Dense 64; Dense 19 softmax.
- E41 parameter count: 66,483 total.
- E48 architectural change: insert exactly one temporal context block after pool3 and before global pooling: SeparableConv2D 96 filters, 5x3 kernel, stride 1x1, same padding, relu, use_bias true; then BatchNorm momentum 0.1. No additional pooling.
- E48 parameter count: 77,619 total, 77,091 trainable, 528 non-trainable, approximately 1.17x E41.
- Frozen controls: no new data, no Phase AF/AD/AA/final-validation data, no feature/preprocessing changes, no label changes, no threshold changes, no router/action changes, same 95-example holdout for evaluation only.
- Pre-registered training protocol: experiment ID E48_CONTROLLED_TEMPORAL_CNN_CAPACITY_PROBE, seed 4242 unless later authoritative E41 evidence proves a different seed, Adam, LR 0.001, batch size 32, 20 epochs, SparseCategoricalCrossentropy, best macro-F1 checkpoint rule.
- Pre-registered evaluation: exact same 95-example formal holdout; raw accuracy, per-class/confusion, confidence, frozen E40 outcomes, accepted-action precision, and four-way E41->E48 comparison.
- No E48 training, E40/E41 modification, threshold change, data collection, holdout edit, live validation, E49 start, or promotion occurred.

## 2026-09-27 17:50:00 +08:00 - Phase AM E48 Controlled Training Gate Result
- Phase AM was authorized to execute E48 only if all Phase AL controls could be verified.
- Pre-training data integrity failed before training.
- E41 metrics record 240 adaptation clips, 120 Pi holdout examples, 4800 training examples, pi_repeat 20, and replay_clips 0.
- Locally reconstructable standard data did not match: 190 adaptation + 41 local extra adaptation = 231 adaptation, and only 95 holdout examples.
- The local e40_non_led_command_recovery_20260923 manifest has 41 adaptation rows, 0 holdout rows, and 41 unresolved WAV paths from standard project locations.
- Training was not run because substituting or restaging data would violate the single-variable architecture experiment.
- Artifacts: PHASE_AM_E48_CONTROLLED_TRAINING_AND_EVALUATION_20260927.md and results/phase_am_e48_controlled_training_and_evaluation_20260927/.
- Final status: E48 INCONCLUSIVE — FURTHER EVIDENCE REQUIRED. E41 remains frozen.


## Phase AN — E41 Dataset Provenance and Reconstruction — 2026-09-27

Purpose: recover and verify exact E41-authorized adaptation and Pi holdout provenance before any E48 controlled architecture training.

Result:
- E41 authoritative metrics record 240 adaptation clips and 120 Pi holdout examples.
- Local exact reconstruction resolved 190 adaptation clips from `all_commands_calibration_15x` and 95 holdout clips from the current formal holdout subset.
- Dedicated E41 recovery folder `pi_validation/e41_functional_non_led_recovery_20260923` is absent locally.
- Expected unresolved/missing dedicated E41 recovery set: 50 adaptation clips and 25 holdout clips for `VOLUME_UP`, `NEXT`, `ALARM`, `CALL`, and `MESSAGE`.
- No substitutions were made. Phase AF, Phase AA, Phase AD, E46/E47, and other validation/recovery data were not used to fill gaps.
- No E48 training occurred.

Decision: E48 DATASET NOT READY — PROVENANCE GAP REMAINS.


## Phase AO — Authoritative E41 Recovery-Data Recovery Audit — 2026-09-27

Purpose: determine whether the missing authoritative E41 recovery dataset could be physically and reproducibly recovered before any E48 controlled training.

Result:
- Expected authoritative E41 dataset: 240 adaptation clips and 120 Pi holdout examples.
- Recovered exact: 190 adaptation clips and 95 holdout examples.
- Remaining not found: 50 adaptation clips and 25 holdout clips from `pi_validation/e41_functional_non_led_recovery_20260923`.
- Local archives contained E41 model/result artifacts but not the target recovery WAV directory.
- Weak same-filename candidates were logged but not substituted.
- No historical per-WAV hashes were available for recovered exact audio rows; no hash matches or mismatches could be established against historical audio hashes.
- No E48 training occurred.

Final status: E41 RECOVERY PARTIAL — REMAINING FILES NOT FOUND.


## Phase AP — E41 Historical Artifact-to-Pi Dataset Reconciliation — 2026-09-27

Purpose: compare authoritative E41 historical artifacts against current Pi-side/local evidence for the recovered E41 WAVs.

Result:
- Historical E41 artifacts confirm the 240 adaptation / 120 holdout record and the 25 E41 recovery holdout references.
- Current local evidence does not contain the requested recovered `pi_validation/e41_functional_non_led_recovery_20260923` 75-WAV package or a current SHA256 manifest for it.
- Classification: 0 exact match, 285 consistent but non-identifying, 75 unavailable.
- No same-named files from other locations were substituted.
- No E48 training occurred.

Conclusion: historical E41 training/holdout provenance cannot be established conclusively from currently available local evidence.


## Phase AP — Updated E41 Artifact-to-Pi Reconciliation With Recovered Dataset — 2026-09-27

Recovered dataset inspected: `C:\Users\Loreen Anne\e41_functional_non_led_recovery_20260923`.

Results:
- WAV count: 75.
- Class counts: `ALARM=15`, `CALL=15`, `MESSAGE=15`, `NEXT=15`, `VOLUME_UP=15`.
- `E41_WAV_SHA256.txt` present and all 75 WAV hashes matched.
- Evidence classification across the 360 expected E41 rows: 25 exact identity established, 335 consistent but non-identifying, 0 unavailable.
- The 25 exact rows are the recovered E41 recovery holdout rows referenced by historical E41 prediction artifacts.
- The 50 recovered adaptation rows are strongly consistent, but not byte-identifying against historical training because no per-row E41 training manifest/hash artifact was available.
- No E48 training occurred.

Recommended next phase: Phase AQ dataset-readiness/methodology decision before any E48 training.


## Phase AQ — E41 Dataset Readiness and Methodology Decision — 2026-09-27

Purpose: decide whether the completed Phase AP reconciliation is sufficient to authorize a future controlled classifier experiment after E41.

Result:
- The 25 recovered E41 recovery holdout rows have exact artifact-to-dataset identity.
- That exact identity supports the original 120-example E41 holdout provenance, not the separate current 95-example 94.74% benchmark by itself.
- The 50 recovered E41 recovery adaptation rows remain consistent but non-identifying against historical training.
- A future controlled E48 experiment may be authorized only as an architecture-only experiment using a frozen reconstructed E41-authorized dataset with a documented provenance caveat.
- Frozen future E48 training set: 240 adaptation clips = 190 base adaptation + 50 recovered recovery adaptation.
- Excluded holdout evidence: 95 current formal holdout rows + 25 exact recovered original-holdout rows.
- No training, model creation, threshold change, E40/E41 change, data collection, or live validation occurred.

Decision: next intervention category remains controlled architecture, not data/fine-tuning, feature/preprocessing, threshold calibration, or live validation.


## Phase AR — E48 Architecture-Only Experiment Specification — 2026-09-27

Purpose: convert the Phase AQ methodology decision into a precise E48 architecture-only experiment specification before execution.

Inspected artifacts:
- `configs/cnn_fastbn_dense_nodropout_raw19.json`
- `training/cnn_model.py`
- `training/train_pi_raw_command_recovery.py`
- `configs/preprocessing.json`
- `preprocessing/audio_io.py`
- `preprocessing/log_mel.py`
- `deployment/vcm_pi_package/scripts/predict_wav_pi.py`
- frozen E40 policy evidence from pulled Pi configs
- Phase AQ frozen dataset definition

Specification:
- E41 baseline: 66,483-parameter tiny CNN with three Conv2D/BatchNorm/MaxPool blocks and avg+max global pooling.
- E48 change: insert one temporal SeparableConv2D block after `pool3`, with 96 filters and 5x3 kernel, followed by BatchNorm momentum 0.1.
- E48 parameter count: 77,619.
- Independent variable: architecture only.
- Frozen controls: data, preprocessing, labels, optimizer, LR, batch size, epoch budget, E40 thresholds, router/action layer, and current 95-example holdout.
- No training occurred.

Next allowable step: a separate execution phase may train E48 only if it preserves this specification exactly.


## Phase AS — E48 Architecture-Only Training and Offline Evaluation — 2026-09-27

Purpose: execute the preregistered E48 architecture-only experiment once and evaluate offline against frozen E41.

Configuration:
- Architecture change: `SeparableConv2D(96, kernel_size=(5,3))` after `pool3`, followed by BatchNorm.
- E48 parameters: 77,619.
- Training source clips: 240.
- Training examples after 20x repeat: 4,800.
- Current95 holdout: 95 rows, excluded from training.
- Exact historical holdout: 25 rows, excluded from training.
- Optimizer/LR: Adam, 0.001.
- Epochs: 20.
- Seed: 4242.
- Checkpoint rule: final epoch only; no holdout model selection.

Result:
- E48 current95: 91/95 = 95.79%.
- E41 current95 baseline: 90/95 = 94.74%.
- Four-way analysis: 87 unchanged-correct, 3 regressions, 4 corrections, 1 unchanged error.
- E48 + E40: accepted-correct 72, accepted-wrong 0, rejected-correct 19, rejected-wrong 4, accepted-action precision 100%.
- E41 + E40 baseline: accepted-correct 79, accepted-wrong 1, rejected-correct 11, rejected-wrong 4, accepted-action precision 98.75%.

Interpretation:
- E48 passes the narrow offline raw/safety gate but is not promoted.
- It reduced accepted-wrong to zero on current95 but also reduced accepted-correct coverage and introduced raw regressions in LIGHT_OFF, STOP, and TEMPERATURE.
- Fresh live validation, if desired, must be separately authorized.


## Phase AT — E41/E48 Architecture Regression Diagnosis — 2026-09-27

Purpose: diagnose E41 -> E48 behavior changes before any promotion, threshold change, retraining, or live validation.

Result:
- Seven current95 cases changed correctness state between E41 and E48.
- All seven are top-1 classification changes.
- E48 corrections: `NEXT_011`, `BRIGHTNESS_015`, `COLOR_015`, and `CREATE_REMINDER_013`.
- E48 regressions: `LIGHT_OFF_014`, `STOP_011`, and `TEMPERATURE_014`.
- No E48 wrong prediction was accepted under frozen E40.
- E48 accepted-correct decreased from 79 to 72 because 17 E41 accepted-correct rows stopped being accepted while only 10 rows moved into accepted-correct.

Interpretation:
- E48 is a promising offline candidate but not ready for promotion.
- The next evidence-supported step is an E48 confidence/rejection calibration diagnostic on existing offline evidence, not live validation or another model.


## Phase AU — E48 Offline Confidence/Rejection Calibration Diagnostic — 2026-09-27

Purpose: determine whether E48's reduced accepted-correct coverage is potentially recoverable through threshold calibration without creating accepted-wrong actions.

Result:
- Evaluated frozen E40, uniform/global thresholds, E40 guardrails plus lowered defaults, and class-specific threshold what-ifs.
- Global threshold reductions are not acceptable: global 0.95 accepts `STOP -> NEXT`.
- E40 guardrails plus default lowering can recover some correct predictions without accepted-wrong on current95.
- Class-specific E48 calibration can recover many rejected-correct cases on current95 while preserving rejected-wrong safety for observed NEXT/WEATHER errors.
- Best offline no-wrong policy accepted 90 correct, 0 wrong, rejected 1 correct, and rejected 4 wrong.

Interpretation:
- This is holdout-derived offline evidence, not production safety evidence.
- Recommendation: design a controlled E48-specific calibration experiment using independent calibration evidence.


## Phase AV — E48 Independent Calibration Dataset Specification — 2026-09-27

Purpose: define the independent dataset needed to calibrate E48 confidence/rejection behavior without using the existing current95 holdout as calibration evidence.

Result:
- Created `PHASE_AV_E48_INDEPENDENT_CALIBRATION_DATASET_SPEC_20260927.md`.
- Created machine-readable artifacts under `results/phase_av_e48_independent_calibration_dataset_20260927/`.
- Target collection size: 210 WAV files.
- Dataset role: calibration only, never training or holdout.
- All 19 executable labels are covered; AU risk and interaction classes receive additional samples.
- Required leakage checks: frozen current95 path overlap = 0 and SHA256 overlap = 0 where holdout hashes are available.

Interpretation:
- Phase AV is a pre-collection design artifact at this point.
- Collection/integrity verification were not run because no Phase AV WAVs are present locally.
- No threshold analysis or production change is authorized until the independent dataset is collected and passes integrity checks.


## Phase AV — E48 Independent Calibration Dataset Collection — 2026-09-27

Purpose: collect the independent 210-example E48 calibration dataset specified by Phase AV.

Result:
- Collection completed on Raspberry Pi.
- Successful manifest rows: 210.
- WAV count: 210.
- Manifest total lines: 211.
- Class counts exactly matched the Phase AV class plan.
- Pi-side integrity checks passed for file count, manifest rows, uniqueness, audio validity, format, duration, labels, calibration metadata, source phase, and path-level holdout separation.
- SHA256 manifest was generated on the Pi.
- Frozen holdout SHA256 overlap was `NOT_AVAILABLE` in the Pi-side verifier because holdout hashes were not available there.

Interpretation:
- The Phase AV calibration dataset is collected and frozen as calibration evidence.
- Byte-level holdout-overlap checking remains not measured from the pasted Pi verifier output.
- No E48 inference or threshold analysis was run. The next phase must explicitly authorize calibration inference/analysis.


## Phase AX — E48 Independent Calibration Inference — 2026-09-27

Purpose: run frozen E48 inference on the 210 Phase AV calibration WAVs and record frozen E40 acceptance/rejection outcomes.

Result:
- BLOCKED.
- E48 model artifacts are available locally.
- The actual Phase AV dataset directory and WAV files are not available locally.
- Local Phase AV WAV count: 0.

Interpretation:
- The pasted Pi collection evidence is not sufficient to run inference; the WAV bytes and manifest must be present in the inference environment.
- No inference or threshold analysis occurred.


## Phase AX — E48 Independent Calibration Inference Completed — 2026-09-27

Purpose: generate independent calibration inference evidence by running frozen E48 on the 210 Phase AV WAVs and applying frozen E40.

Result:
- Evaluated 210 manifest-listed Phase AV samples.
- Raw correct: 88.
- Raw wrong: 122.
- Raw accuracy: 41.90%.
- Accepted-correct: 38.
- Accepted-wrong: 13.
- Rejected-correct: 50.
- Rejected-wrong: 109.
- Accepted-action precision: 74.51%.
- Acceptance coverage: 24.29%.

Interpretation:
- Phase AV is substantially harder than the current95 holdout for E48.
- Frozen E40 does not fully protect E48 on this independent calibration set; 13 wrong predictions were accepted.
- This is inference evidence only. No threshold optimization or threshold-policy selection was performed in AX.


## Phase AY — E48 Independent Failure Diagnosis — 2026-09-27

Purpose: diagnose the 210-example Phase AV/AX failure structure before any intervention.

Result:
- AX baseline verified from artifacts: 88/210 raw correct = 41.90%.
- E40 outcomes verified: accepted-correct 38, accepted-wrong 13, rejected-correct 50, rejected-wrong 109.
- Complete confusion, per-class, confidence, accepted-wrong, rejected-correct, holdout-vs-AV, longitudinal-confusion, and next-experiment-option artifacts were created.
- High-confidence wrong predictions were common: 17 wrong predictions >= 0.90 confidence.
- Frozen E41 diagnostic comparison on the same AV samples produced 103/210 raw correct but 51 accepted-wrong cases under frozen E40.

Interpretation:
- The evidence points to a mixed data/generalization and classifier/representation problem.
- Confidence calibration alone is insufficient because many errors are wrong top-1 predictions and several are high-confidence accepted-wrong cases.
- A clean dataset/retraining experiment is justified as a future design question, but AY did not execute it.


## Phase AZ — Additional Dataset Integration Audit — 2026-09-27

Purpose: audit the newly available posted dataset before any training-data intervention.

Result:
- Google Drive file-level access was not available in this Codex session; the audit used the local copy at `C:\Users\Loreen Anne\Downloads\VCM\VCM`.
- `VCM_MASTER`: 36,622 manifest rows/audio files, 16 classes, 395 speakers/groups, train/val/test = 27,130/4,734/4,758, zero missing manifest audio.
- `VCM_BALANCED`: 15,268 WAV training files, 16 classes, 298 speakers/groups, 13,801 originals and 1,467 augmented rows, derived from Dataset A train only.
- Embedded reports document zero speaker leakage across Dataset A splits and zero B-vs-A-val/test speaker overlap.
- SHA256 overlap check between all `VCM_BALANCED` audio files and 21,757 scoped current-project audio files found 0 byte-identical overlaps.
- Mapping to current 19 raw labels is incomplete: `COLOR`, `CREATE_REMINDER`, `LIST_REMINDERS`, `CALL`, and `MESSAGE` are missing; `BRIGHTNESS` is only partially supported through `LIGHT_DIM`; `UNKNOWN` and `SILENCE` are useful as rejection/no-action support.

Interpretation:
- The posted dataset can legitimately support a future controlled training-data experiment, but it cannot replace the current 19-label taxonomy by itself.
- Dataset A validation/test must remain untouched evaluation/model-selection evidence.
- Any future model work must be a new pre-registered data-intervention experiment, not a silent continuation of E41/E48.
- No training, threshold tuning, model promotion, live validation, data collection, or router/action change occurred.


## Phase AZ-R — Actual Dataset 2 Verification and Integration Audit — 2026-09-27

Purpose: verify the actual downloaded `data/VCM Dataset2` files against `data/VCM Dataset2 Specifications.pdf` and reconcile the preliminary AZ audit with actual filesystem evidence.

Result:
- Actual Dataset 2 files were available locally under `data/VCM Dataset2/VCM`; the previous connector-limited AZ access limitation is superseded for this dataset.
- Dataset A actual-vs-spec matched: 36,622 rows/files; train 27,130; validation 4,734; test 4,758; 16 classes; 395 speakers/groups; 0 missing files; 0 unreadable/corrupt audio.
- Dataset B actual-vs-spec matched: 15,268 train files; 13,801 originals; 1,467 augmented; 16 classes; all documented class counts matched exactly.
- Speaker leakage checks from actual manifests: train∩val 0, train∩test 0, val∩test 0, Dataset B∩A-val 0, Dataset B∩A-test 0.
- Dataset B provenance audit: all 15,268 rows trace to Dataset A train; 0 val/test source leaks; 0 missing sources; 0 source-label mismatches.
- Dataset B augmentation/synthetic audit: gain 410, noise 425, pitch 36, shift 380, speed 216; 480 synthetic-derived `SET_TEMPERATURE` rows.
- Byte-level overlap checks found 0 Dataset2 B overlaps with 21,001 active project audio files and 0 overlaps with 615 protected evaluation/live audio files.
- Taxonomy gap remains: Dataset 2 lacks `COLOR`, `CREATE_REMINDER`, `LIST_REMINDERS`, `CALL`, and `MESSAGE`; `LIGHT_DIM` is partial support for `BRIGHTNESS`, not `COLOR`.

Interpretation:
- Dataset 2 is usable after controlled filtering as a training-data intervention source, not as a direct replacement for the current 19-label model.
- The smallest next experiment should be pre-registered as a data intervention using Dataset2 B for covered labels plus existing/project training data for missing labels, while preserving Dataset A val/test, current95, Phase AV, Phase AD, and other final validation evidence outside training.
- No training, threshold change, model promotion, dataset merge, label change, preprocessing change, router/action change, recording collection, or live validation occurred.


## Phase BA — Controlled Hybrid Dataset Training Experiment — 2026-09-28

Purpose: test a single controlled training-data intervention after AZ-R, using Dataset2 `VCM_BALANCED` train rows for legitimately mapped labels while preserving the full current 19-label taxonomy and all frozen evaluation evidence.

Controlled variables:
- Architecture: E41 `tiny_vcm_cnn`.
- Initialization: frozen E41 weights.
- Threshold policy: frozen E40.
- Preprocessing: established E41 log-Mel pipeline.
- Router/actions: unchanged.
- Evaluation sets: current95 and Phase AV kept out of training.

Manifest:
- Total training rows: 11,830.
- E41 reconstructed adaptation rows: 240.
- Active project training rows: 8,790.
- Dataset2 `VCM_BALANCED` train rows: 2,800.
- Protected path overlap: 0.
- Protected SHA256 overlap: 0.

Result:
- Candidate: `E49_BA_HYBRID_DATASET_E41_ARCH`.
- Current95 raw accuracy: 78/95 = 82.11%; macro-F1 80.90%; accepted-wrong 6.
- Phase AV raw accuracy: 148/210 = 70.48%; macro-F1 70.27%.
- Phase AV E40 outcomes: accepted-correct 102, accepted-wrong 24, rejected-correct 46, rejected-wrong 38.
- Phase AV coverage: 126/210 = 60.00%.
- Phase AV accepted-action precision: 102/126 = 80.95%.

Interpretation:
- Dataset2-supported hybrid training materially improved independent Phase AV raw generalization compared with E41 and E48.
- BA did not satisfy the safety/promotion gate because accepted-wrong actions were still high and exceeded E48's 13 accepted-wrong Phase AV result.
- BA also regressed current95 raw accuracy relative to E41/E48.
- BA is useful evidence for the value and limits of the training-data intervention, but it is not a production candidate.
- No threshold tuning, retraining, deployment, live validation, or follow-on experiment occurred.


## Phase BB — E49 Hybrid Regression and Data-Composition Diagnosis — 2026-09-28

Purpose: diagnose why E49 improved independent Phase AV generalization while regressing current95 and leaving 24 accepted-wrong Phase AV actions.

Inputs:
- E41 current95 prediction table.
- E41 Phase AV predictions from Phase AY.
- E48 Phase AV predictions from Phase AX.
- E49 current95 and Phase AV predictions from Phase BA.
- E49 frozen hybrid training manifest from Phase BA.

Result:
- Current95 four-way E41/E49 comparison: 76 E41-correct/E49-correct, 14 E41-correct/E49-wrong, 2 E41-wrong/E49-correct, 3 E41-wrong/E49-wrong.
- Phase AV four-way E41/E49 comparison: 85 E41-correct/E49-correct, 18 E41-correct/E49-wrong, 63 E41-wrong/E49-correct, 44 E41-wrong/E49-wrong.
- Current95 raw regression is mostly in Dataset2-supported/partial labels: -10 raw-correct examples in supported/partial labels versus -2 in uncovered labels.
- The five uncovered labels were not disproportionately damaged in raw accuracy. They improved net +16 raw-correct examples on Phase AV, though `COLOR` remains severe and unsafe.
- E49 repaired all tracked AY confusion families relative to E48, but shifted errors into new accepted-wrong families such as `COLOR -> CALL`, `LIGHT_ON -> BRIGHTNESS`, and `TIMER -> BRIGHTNESS`.
- E49 had 24 Phase AV accepted-wrong cases: 8 same wrong prediction as E41, 9 different wrong prediction from E41, and 7 new raw errors where E41 was correct.
- High-confidence wrong predictions improved versus E41 but worsened versus E48: E49 had 24 wrong predictions >= 0.90 versus E48's 17.

Interpretation:
- E49 is not simply worse than E41. It demonstrates a generalization/current-domain tradeoff.
- Evidence is most consistent with a distributed cause: Dataset2 helped independent generalization, but the hybrid procedure moved established decision boundaries and likely caused some original-domain forgetting.
- No single-factor causal claim is justified. The evidence supports a next data-composition experiment, not immediate architecture change or threshold tuning.
- No training, threshold change, deployment, data collection, or live validation occurred in BB.


## Phase BC — Command-Vocabulary Revision and Router/Action Verification — 2026-09-28

Purpose: verify whether the project can replace the future classifier label `COLOR` with `LIGHT_DIM` before any next training experiment.

Evidence inspected:
- `VCM Machine Exercise.pdf`
- `actions/raw_command_router.py`
- `actions/command_actions.py`
- `actions/ACTION_LAYER_DESIGN.md`
- `data/metadata/active_dataset_index.csv`
- Dataset2 manifests and content reports
- Phase BA/BB reports and artifacts
- Phase C/Pi evidence tables for light command behavior

Result:
- Assignment category is `Dim / color lights`; the assignment example is `Dim lights to X percent`.
- Historical `COLOR` is implemented as `LIGHT_ADJUST` with `color=red`, but has only 10 E49 training examples and no Dataset2 support.
- Historical `BRIGHTNESS` is implemented as `LIGHT_ADJUST` with `brightness_percent=50` and is backed by original `DIM_UP`/`DIM_DOWN` data.
- Dataset2 directly supports `LIGHT_DIM`, meaning dim/reduce brightness of lights, with 522 balanced training rows.
- Dataset2 does not support literal `COLOR`, `CREATE_REMINDER`, `LIST_REMINDERS`, `CALL`, `MESSAGE`, or `BRIGHTNESS`.

Decision:
- `COLOR -> LIGHT_DIM` is documented as a future command-vocabulary design revision, not as a completed model/action implementation.
- `LIGHT_DIM` is the proposed concrete command for the assignment's `DIM/COLOR LIGHTS` category.
- Existing `BRIGHTNESS` and proposed `LIGHT_DIM` overlap in the current implementation; a future phase must define or consolidate them before training.

No training, model creation, threshold change, preprocessing change, architecture change, data collection, Pi/live validation, or historical-result modification occurred.


## Phase BF — Frozen 19-Command End-to-End VCM Functional Audit — 2026-09-28

Purpose: audit whether the current frozen VCM can perform the full spoken wake-command-action-response-return loop for all 19 historical labels.

Evidence inspected:
- `deployment/vcm_pi_package/scripts/predict_wav_pi.py`
- `deployment/vcm_pi_package/scripts/pi_wake_voice_control_demo.py`
- `deployment/vcm_pi_package/actions/raw_command_router.py`
- `deployment/vcm_pi_package/actions/command_actions.py`
- `deployment/vcm_pi_package/README_PI_DEPLOYMENT.md`
- `deployment/vcm_pi_package/PACKAGE_MANIFEST.md`
- BA/BB/BC reports and current project status/traceability records.

Result:
- Actual packaged predictor defaults are `E33_PI_COLOR_LIGHTON_RESPONSIVENESS`, threshold `0.95`, and `configs/e33_pi_guardrail_thresholds.json`.
- Historical live-evidence stack remains `E37` wake + `E41` command + `E40` policy.
- E49 is present as a root offline artifact but was rejected in BA/BB and is not packaged as the active Pi default.
- The historical 19-label vocabulary including `COLOR` was preserved for BF; no `LIGHT_DIM` substitution was made.
- Router/action mappings for all 19 labels are implemented as local actions/stubs, with optional GPIO/audio behavior.
- No command-specific response WAV bank exists in the packaged path; `deployment/vcm_pi_package/music/` has no WAV/MP3 files.
- The wake-gated runner is a single-cycle script, not a persistent return-to-listening loop.
- Fresh BF spoken trials were not run because the current environment is not the Raspberry Pi runtime and lacks `arecord`/`aplay`/microphone/speaker access.

Interpretation:
- BF does not produce a classifier benchmark or end-to-end success count.
- BF identifies integration blockers: stack-selection ambiguity, missing response WAV bank, single-cycle runner, and lack of executable Pi hardware in this session.
- These blockers do not justify a model-training experiment by themselves; they are system-integration/demo-readiness issues.

No training, retraining, E50 creation, threshold change, E40/E37 change, preprocessing change, architecture change, command-vocabulary change, router/action change, data collection, deployment, live validation, Phase AV/current95 modification, or historical-result modification occurred.


## Phase BG — Autonomous CNN Accuracy Optimization — 2026-09-28

Status: initiated.

Starting evidence:
- E49 improved Phase AV raw accuracy but regressed current95 and left 24 accepted-wrong Phase AV actions.
- BB implicated training-data composition / boundary displacement more strongly than architecture alone.
- BC documented the future vocabulary revision `COLOR -> LIGHT_DIM`.
- BF did not produce new recognition evidence and identified integration blockers rather than classifier results.

First controlled hypothesis:
- A revised-vocabulary classifier that preserves more original-domain training examples while adding Dataset2 diversity for supported labels may retain E49's independent-generalization gain while reducing E49's current95/original-domain regression.

Frozen constraints:
- No protected current95, Phase AV, Phase AD/live, or Dataset2 validation/test audio in training.
- No threshold tuning.
- E41 architecture and preprocessing retained for the first BG candidate.
- Historical E41/E48/E49 artifacts and results remain unchanged.

Status: completed offline.

Artifacts:
- `results/phase_bg_autonomous_cnn_optimization_20260928/PHASE_BG_AUTONOMOUS_CNN_OPTIMIZATION_FINAL_20260928.md`
- `results/phase_bg_autonomous_cnn_optimization_20260928/PHASE_BG_E41_E48_E49_E50_E51_COMPATIBLE_COMPARISON.csv`
- `results/phase_bg_autonomous_cnn_optimization_20260928/PHASE_BG_EFFICIENCY_SCORECARD.csv`
- `results/phase_bg_autonomous_cnn_optimization_20260928/PHASE_BG_FINAL_DECISION.csv`
- `results/phase_bg_e50_bg_revised_vocab_original_preserve_e41_init_20260928/`
- `results/phase_bg_e51_bg_revised_vocab_original_preserve_fresh_init_20260928/`

Training intervention:
- Revised 19-label vocabulary: historical `COLOR` removed, `LIGHT_DIM` added.
- Training manifest: 16,100 rows.
- Balancing rule: cap original-domain rows at 700 per label, add up to 200 Dataset2 train rows for legitimately supported labels.
- Original-only labels: `BRIGHTNESS`, `CREATE_REMINDER`, `LIST_REMINDERS`, `CALL`, `MESSAGE`.
- Protected contamination check: 0 protected path overlap and 0 protected SHA256 overlap across 14,142 protected hashes.

Candidates:
- E50: mapped E41 initialization for common labels; new `LIGHT_DIM` output initialized fresh.
- E51: fresh initialization.
- Both used E41 tiny CNN architecture, established log-Mel preprocessing, Adam learning rate 0.00075, batch size 32, max 14 epochs, early stopping patience 4, seed 5050, and checkpoint selection by internal validation loss only.

Key compatible results:
- E41 current95-compatible: 86/90 = 95.56%; Phase AV-compatible: 103/194 = 53.09%; Phase AV accepted-wrong 43.
- E49 current95-compatible: 74/90 = 82.22%; Phase AV-compatible: 144/194 = 74.23%; Phase AV accepted-wrong 18.
- E50 current95-compatible: 83/90 = 92.22%; Phase AV-compatible: 139/194 = 71.65%; Phase AV accepted-wrong 8.
- E51 current95-compatible: 77/90 = 85.56%; Phase AV-compatible: 131/194 = 67.53%; Phase AV accepted-wrong 8.

Efficiency:
- E50 parameter count: 66,483; weights SHA256 `BC8AC64CED4305DDF43BF4DE377F3CC636A764EFF339CD9F92AF06340C50B8FF`.
- E51 parameter count: 66,483; weights SHA256 `B5967EE7C1BE6A493F212228A9CB3CE0509CB92FB360DB9A4EEAF78C15A16F8D`.
- Laptop CPU latency p95: E50 33.78 ms total; E51 29.71 ms total.

Decision:
- E50 is the best BG offline command-classifier candidate for final review.
- E51 is rejected as the final BG candidate because protected-compatible current95 and Phase AV performance are materially worse than E50.
- E50 is not final production/demo verified until packaging and Pi end-to-end validation are completed.

No threshold tuning, architecture change, preprocessing change, router/action change, wake-model change, protected-data training, Pi deployment, or live validation occurred in BG.


## Phase BH — E50 Raspberry Pi Package Integration — 2026-09-28

Purpose: integrate the selected BG classifier into the Raspberry Pi package so the next validation can test the actual wake-command-action path.

Artifacts:
- `results/phase_bh_e50_pi_package_integration_20260928/PHASE_BH_E50_PI_PACKAGE_INTEGRATION_20260928.md`
- `results/phase_bh_e50_pi_package_integration_20260928/PHASE_BH_PACKAGE_ARTIFACTS.csv`
- `results/phase_bh_e50_pi_package_integration_20260928/PHASE_BH_VERIFICATION_RESULTS.csv`

Changes:
- Packaged `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT` weights, normalization, and labels.
- Packaged preserved `E37_TARGETED_COLOR_VOLUME_FIX` wake-gated model artifacts.
- Added `e50_revised_vocab_e40_thresholds.json`, preserving frozen E40 numeric thresholds for the revised E50 vocabulary.
- Added `LIGHT_DIM` raw routing to `LIGHT_ADJUST`.
- Updated wake-gated demo defaults to E37 wake + E50 command.

Verification:
- Python syntax check passed.
- `LIGHT_DIM` routed to `LIGHT_ADJUST` and executed a local dry-run state update with GPIO disabled.
- Packaged E50 inference predicted `ALARM` on an existing ALARM WAV with confidence 0.998068869 and accepted under the E50/E40-compatible policy.

Limitations:
- No Pi microphone/live validation was run in this environment.
- No command-response WAV bank was created.
- No GPIO execution was performed.
- No production/demo success is claimed from BH alone.

No training, retraining, threshold tuning, architecture change, preprocessing change, protected-evaluation modification, or live validation occurred.


## Phase BI — E50 Raspberry Pi Wake-Gated Live Validation — 2026-09-28

Purpose: validate the packaged E37 wake + E50 command stack on the Raspberry Pi microphone path.

Evidence:
- Archive: `outputs/e50_wake_gated_live_20260928_evidence.tar.gz`
- SHA256: `81916037181eacf42ed40904d4f89d7e038db46c90e6495ec8e5a70ed3c9e2b5`
- Report: `results/phase_bi_e50_pi_live_validation_20260928/PHASE_BI_E50_PI_LIVE_VALIDATION_20260928.md`
- Trial table: `results/phase_bi_e50_pi_live_validation_20260928/PHASE_BI_TRIAL_RESULTS.csv`
- Per-label table: `results/phase_bi_e50_pi_live_validation_20260928/PHASE_BI_PER_LABEL_SUMMARY.csv`

Results:
- 36 result JSON files parsed.
- Wake success: 36/36.
- All 19 revised command labels tested at least once.
- Command trials excluding UNKNOWN: 35.
- Raw correct: 24/35.
- Accepted-correct: 15.
- Accepted-wrong: 1.
- Accepted-action precision: 93.75%.
- End-to-end command successes: 14/35.
- UNKNOWN safe rejection: 1/1.

Passed at least once:
- `PLAY_MUSIC`, `WEATHER`, `LIGHT_ON`, `LIGHT_OFF`, `LIGHT_DIM`, `TIMER`, `ALARM`, `NEXT`, `PAUSE`, `STOP`, `LIST_REMINDERS`, `MESSAGE`.

Remaining weak/not end-to-end successful in BI:
- `TIME`, `BRIGHTNESS`, `TEMPERATURE`, `VOLUME_UP`, `VOLUME_DOWN`, `CREATE_REMINDER`, `CALL`.

Critical failure:
- `e50_temperature_001`: expected `TEMPERATURE`, predicted and accepted `WEATHER` at 0.997283935546875, then executed `question.weather_local`.

Integration finding:
- `LIGHT_DIM` initially failed because the Pi package lacked the router route. The user patched the Pi router and a later `LIGHT_DIM` trial passed end-to-end. The local package already contains the route from BH.

Limitation:
- The trials were run via repeated `run_trial` invocations. This is repeated manual cycle evidence, not persistent always-listening loop evidence.

No training, threshold tuning, architecture change, preprocessing change, or historical-result rewriting occurred.


## Phase BJ — Diagnosis-First Targeted Remediation Decision — 2026-09-28

Purpose: decide whether to remediate weak commands or prepare a defensible final demo subset after BI, without starting another general CNN sweep.

Artifacts:
- `results/phase_bj_diagnosis_first_targeted_remediation_20260928/PHASE_BJ_DIAGNOSIS_FIRST_TARGETED_REMEDIATION_20260928.md`
- `results/phase_bj_diagnosis_first_targeted_remediation_20260928/PHASE_BJ_WEAK_COMMAND_DIAGNOSIS.csv`
- `results/phase_bj_diagnosis_first_targeted_remediation_20260928/PHASE_BJ_REMEDIATION_OPTIONS.csv`
- `results/phase_bj_diagnosis_first_targeted_remediation_20260928/PHASE_BJ_TARGETED_PI_REPEAT_PLAN.csv`
- `results/phase_bj_diagnosis_first_targeted_remediation_20260928/PHASE_BJ_DECISION_SUMMARY.json`

Input evidence:
- Phase BI live Pi results showed 36/36 wake success, all 19 revised labels tested at least once, 15 accepted-correct command actions, 1 accepted-wrong command action, and 12 labels with at least one end-to-end pass.
- BI also showed that `TIME`, `BRIGHTNESS`, `TEMPERATURE`, `VOLUME_UP`, `VOLUME_DOWN`, `CREATE_REMINDER`, and `CALL` did not yet have an end-to-end pass.

Diagnosis:
- `TEMPERATURE` is the highest-priority safety issue because one trial was accepted as `WEATHER` at confidence `0.997283935546875` and executed a weather action.
- `TIME`, `BRIGHTNESS`, `VOLUME_UP`, `VOLUME_DOWN`, and `CREATE_REMINDER` showed evidence of correct or partly correct recognition but were rejected under the frozen policy.
- `CALL` showed classifier-boundary failure but was safely rejected in BI.
- Persistent listening, response playback, and GPIO/PWM evidence are demo-integration gaps, not problems that another CNN sweep would automatically solve.

Decision:
- Do not claim final all-command demo readiness from BI alone.
- Do not run another general CNN sweep or tune thresholds in BJ.
- Run targeted Pi repeat/phrase validation for weak labels under frozen E37+E50+E40-compatible policy before deciding on any classifier remediation.
- If time forces a subset demo, present only the commands with actual end-to-end evidence and clearly disclose remaining limitations.

No training, retraining, threshold tuning, architecture change, preprocessing change, protected-evaluation modification, Pi live validation, new training-data collection, or historical-result rewriting occurred in BJ.


## Phase BK — Targeted Weak-Command Repeat Validation — 2026-09-28

Purpose: run and ingest targeted Raspberry Pi repeat trials for the weak commands identified by BI/BJ, using the frozen E37 wake + E50 command stack.

Evidence:
- Archive: `outputs/e50_bk_targeted_weak_command_repeats_e37_e50_20260928_evidence.tar.gz`
- SHA256: `e92b12464153fbf2652aafdbadd3459eab6a1a1331fcb5463c0da3e69b851513`
- Report: `results/phase_bk_targeted_weak_command_repeat_validation_20260928/PHASE_BK_TARGETED_WEAK_COMMAND_REPEAT_VALIDATION_20260928.md`
- Trial table: `results/phase_bk_targeted_weak_command_repeat_validation_20260928/PHASE_BK_TRIAL_RESULTS.csv`
- Per-label table: `results/phase_bk_targeted_weak_command_repeat_validation_20260928/PHASE_BK_PER_LABEL_SUMMARY.csv`

Results:
- Parsed trials: 23 total, including one ALARM stack-check trial.
- Weak-command trials: 22.
- Weak-command wake success: 22/22.
- Weak-command raw correct: 11/22.
- Weak-command accepted correct: 3/22.
- Weak-command accepted wrong: 2/22.
- Weak-command end-to-end successes: 3/22.

Recovered:
- `CREATE_REMINDER` now has accepted end-to-end evidence for `remind me` and `set reminder`.

Still unsafe or incomplete:
- `TEMPERATURE` produced one correct accepted action but also two accepted-wrong actions: `set thermostat -> STOP` and `temperature -> WEATHER`.
- `TIME`, `BRIGHTNESS`, `VOLUME_UP`, `VOLUME_DOWN`, and `CALL` still lack accepted end-to-end passes.

Decision:
- Do not run another general CNN sweep.
- Do not lower thresholds based on BK; accepted-wrong `TEMPERATURE` evidence makes threshold relaxation unsafe.
- Prepare a defensible final demo subset around commands with actual live end-to-end evidence, and document the remaining labels as limitations unless later targeted remediation is authorized.

No training, threshold tuning, model modification, preprocessing change, architecture change, protected-data modification, or historical-result rewriting occurred.


## Phase BL — Targeted Weak-Command Remediation — 2026-09-28

Purpose: diagnose the remaining weak commands after BI/BK and determine whether a narrow classifier remediation could safely improve them without changing thresholds, architecture, preprocessing, router/actions, or protected evaluation data.

Artifacts:
- `results/phase_bl_targeted_weak_command_remediation_20260928/PHASE_BL_TARGETED_WEAK_COMMAND_REMEDIATION_20260928.md`
- `results/phase_bl_targeted_weak_command_remediation_20260928/PHASE_BL_FAILURE_LAYER_TABLE.csv`
- `results/phase_bl_targeted_weak_command_remediation_20260928/PHASE_BL_WEAK_COMMAND_DIAGNOSIS_SUMMARY.csv`
- `results/phase_bl_targeted_weak_command_remediation_20260928/PHASE_BL_E50_WEAK_COMMAND_TRAINING_COMPOSITION.csv`
- `results/phase_bl_targeted_weak_command_remediation_20260928/PHASE_BL_E50_E52_COMPARISON.csv`
- `results/phase_bl_targeted_weak_command_remediation_20260928/PHASE_BL_E50_E52_DECISION_DELTAS.csv`
- `results/phase_bl_targeted_weak_command_remediation_20260928/PHASE_BL_E52_ACCEPTED_WRONG_DIAGNOSIS.csv`

Diagnosis:
- `TIME`, `BRIGHTNESS`, `VOLUME_UP`, `VOLUME_DOWN`, and `CALL` remained mostly safe-rejected or low-margin.
- `TEMPERATURE` remained unsafe because it had repeated accepted-wrong outcomes.
- The failure pattern was classifier/margin related, not a router/action bug.

Controlled candidate:
- Experiment ID: `E52_BL_TARGETED_WEAK_E50_FINETUNE`
- Parent: `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT`
- Intervention: E50-initialized fine-tune with weak-label sample weights only.
- Training rows: 16,100 from the existing legitimate BG/E50 manifest.
- Best epoch: 1 by internal validation loss.
- No protected/live evaluation recordings were used for training.

Result:
- current95-compatible: E50 83/90, E52 82/90.
- Phase AV-compatible: E50 139/194, E52 150/194.
- Phase AV accepted-wrong: E50 8, E52 13.
- BI live/replay accepted-wrong: E50 observed 1, E52 replay 3.
- BK weak live/replay accepted-correct: E50 observed 3, E52 replay 2.

Decision:
- E52 is rejected for promotion.
- E50 remains the defensible final-demo baseline.
- Final demo should use only the live-supported subset unless later targeted data collection/remediation is authorized.

No additional model was trained after E52. No threshold tuning, architecture change, preprocessing change, E37/E40 modification, protected-data training, router/action redesign, Pi deployment, or new live validation occurred in BL.


## Phase BM — Final E50 Integration, Demo Hardening, and Requirements Audit — 2026-09-28

Purpose: close model optimization and prepare the final E50 baseline for a defensible 13-command demo and Pi validation handoff.

Artifacts:
- `results/phase_bm_final_vcm_integration_demo_hardening_20260928/PHASE_BM_FINAL_VCM_INTEGRATION_DEMO_HARDENING_20260928.md`
- `results/phase_bm_final_vcm_integration_demo_hardening_20260928/PHASE_BM_MODEL_INTEGRITY.json`
- `results/phase_bm_final_vcm_integration_demo_hardening_20260928/PHASE_BM_FINAL_STACK_MANIFEST.json`
- `results/phase_bm_final_vcm_integration_demo_hardening_20260928/PHASE_BM_LABEL_ROUTER_ACTION_AUDIT.csv`
- `results/phase_bm_final_vcm_integration_demo_hardening_20260928/PHASE_BM_RESPONSE_WAV_INVENTORY.csv`
- `results/phase_bm_final_vcm_integration_demo_hardening_20260928/PHASE_BM_OFFLINE_REPLAY_RESULTS.csv`
- `results/phase_bm_final_vcm_integration_demo_hardening_20260928/PHASE_BM_RUNTIME_EFFICIENCY_LOCAL.json`
- `results/phase_bm_final_vcm_integration_demo_hardening_20260928/PHASE_BM_COMMAND_STATUS.csv`
- `results/phase_bm_final_vcm_integration_demo_hardening_20260928/PHASE_BM_13_COMMAND_DEMO_STATUS.csv`
- `results/phase_bm_final_vcm_integration_demo_hardening_20260928/PHASE_BM_REQUIREMENTS_AUDIT.csv`
- `results/phase_bm_final_vcm_integration_demo_hardening_20260928/PHASE_BM_PI_VALIDATION_HANDOFF.md`

Implementation hardening:
- E50 made the default packaged command classifier.
- Persistent-loop support added through `--cycles` and `--continuous`.
- Runtime model loading was hardened through a reusable predictor.
- Response WAV assets and response mapping were added.
- Active `COLOR` routing/prompting was removed from final runtime helpers.

Evidence:
- E50 SHA256 matched the required final hash.
- All 19 labels map to router/action handlers.
- 14 response WAV assets exist and are readable.
- Existing BI/BK Pi WAV evidence replayed through the hardened package without changing the known model behavior.

Decision:
- Proceed to physical Pi validation with E37+E50 and the 13-command demo subset.
- Do not train another model or deploy E52.

No model training, threshold tuning, architecture change, preprocessing change, E37/E40 modification, protected-data training, E50 weight modification, unauthorized Pi access, GPIO execution, or new live validation occurred in BM.


## Phase BM Addendum — Physical Pi Final Demo Validation — 2026-09-28

Purpose: record the actual Raspberry Pi execution of the BM final-demo handoff under the frozen E37+E50 stack.

Artifacts:
- `outputs/e50_bm_final_demo_20260928_evidence.tar.gz`
- `results/phase_bm_final_vcm_integration_demo_hardening_20260928/PHASE_BM_PI_FINAL_VALIDATION_ADDENDUM_20260928.md`
- `results/phase_bm_final_vcm_integration_demo_hardening_20260928/PHASE_BM_PI_FINAL_VALIDATION_RESULTS.csv`
- `results/phase_bm_final_vcm_integration_demo_hardening_20260928/PHASE_BM_PI_FINAL_VALIDATION_SUMMARY.json`

Evidence:
- Archive SHA256: `4695a6d0fb282624499a42d8102ff4bf578022c5a0e15a8368b8ef7fd97079ec`.
- 14 Pi trials parsed: 13 selected demo-command trials and 1 UNKNOWN rejection trial.
- Wake success: 13/14 total trials and 12/13 selected demo-command trials.
- Raw recognition correct: 11/13 selected demo commands.
- Accepted automatic action execution: 9/13 selected demo commands.
- Loop return: 14/14 trials.
- UNKNOWN rejection: passed; no unintended action was executed.
- Response playback: failed for all attempted response WAVs because `aplay` exited with status 1, although WAV assets existed and were readable.

Decision:
- The physical Pi run supports a defensible demo only for commands that reached the action pipeline in this run, or for commands supported by earlier live evidence if separately disclosed.
- Audible response feedback remains not verified until the Pi playback device is fixed and rerun.
- Do not solve response playback with classifier training.

No model training, threshold tuning, architecture change, preprocessing change, E37/E40/E50 modification, protected-data training, GPIO execution, or historical-result modification occurred in this addendum.


## Phase BM Correction — 19-Command Callability vs Demo Readiness — 2026-09-28

Purpose: clarify that the final demo subset is not a runtime vocabulary restriction.

Artifacts:
- `results/phase_bm_final_vcm_integration_demo_hardening_20260928/PHASE_BM_19_COMMAND_IMPLEMENTATION_CALLABILITY.csv`
- `results/phase_bm_final_vcm_integration_demo_hardening_20260928/PHASE_BM_CURRENT_DEMO_READY_COMMANDS.csv`

Clarification:
- All 19 commands remain in the final VCM vocabulary and remain callable/testable.
- All 19 legitimate router/action paths remain available.
- The six unresolved commands remain callable and implemented, but are not currently demo-ready.
- `TEMPERATURE` remains callable and implemented, but is unsafe/not demo-ready because accepted-wrong live actions were observed.
- The 13-command final demo subset is a validation/safety presentation choice, not a runtime whitelist.

No runtime command whitelist was created. No command was disabled, removed, hidden, or suppressed.


## Phase BN — Final Pi Validation Runtime Hardening Offline Preparation — 2026-09-28

Purpose: prepare the frozen E37+E50 VCM for final Raspberry Pi audio diagnosis, all-19 validation, efficiency measurement, and demo validation without any further model development.

Artifacts:
- `results/phase_bn_final_pi_validation_runtime_hardening_20260928/PHASE_BN_FINAL_PI_VALIDATION_RUNTIME_HARDENING_20260928.md`
- `results/phase_bn_final_pi_validation_runtime_hardening_20260928/PHASE_BN_OFFLINE_STACK_AUDIT.json`
- `results/phase_bn_final_pi_validation_runtime_hardening_20260928/PHASE_BN_RESPONSE_WAV_AUDIT.csv`
- `results/phase_bn_final_pi_validation_runtime_hardening_20260928/PHASE_BN_19_COMMAND_FINAL_STATUS.csv`
- `results/phase_bn_final_pi_validation_runtime_hardening_20260928/PHASE_BN_ALL19_VALIDATION_PROTOCOL.csv`
- `results/phase_bn_final_pi_validation_runtime_hardening_20260928/PHASE_BN_ROUTER_ACTION_SMOKE.csv`
- `results/phase_bn_final_pi_validation_runtime_hardening_20260928/PHASE_BN_RUNTIME_EFFICIENCY.csv`
- `results/phase_bn_final_pi_validation_runtime_hardening_20260928/PHASE_BN_PI_AUDIO_AND_VALIDATION_HANDOFF.md`
- `outputs/e50_bn_runtime_update_20260928.tar.gz`

Evidence:
- E50 SHA256 matched the frozen expected hash.
- E50 label map retained all 19 final commands.
- All 19 commands remained callable/routable/actionable in local simulated action smoke.
- Response WAV assets now cover all 19 command labels plus UNKNOWN.
- Runtime response playback now supports an explicit ALSA response device and records `aplay` stderr in JSON evidence.

Current boundary:
- Physical Pi audio diagnosis is the next required step.
- Pi audio playback, live all-19 validation, persistent-cycle stability, GPIO, and Pi efficiency remain NOT MEASURED.

No CNN training, fine-tuning, threshold tuning, architecture change, preprocessing change, E37/E40/E50 modification, quantization, protected-data modification, GPIO execution, Pi access, or live validation occurred in BN offline preparation.


## Phase BN Addendum — Audio Smoke Evidence — 2026-09-28

Purpose: record the first physical BN audio-smoke evidence after deploying the Phase BN runtime update to the Raspberry Pi.

Artifacts:
- `outputs/e50_bn_audio_smoke_20260928_evidence.tar.gz`
- `results/phase_bn_final_pi_validation_runtime_hardening_20260928/PHASE_BN_AUDIO_SMOKE_ADDENDUM_20260928.md`
- `results/phase_bn_final_pi_validation_runtime_hardening_20260928/PHASE_BN_AUDIO_SMOKE_RESULTS.csv`
- `results/phase_bn_final_pi_validation_runtime_hardening_20260928/PHASE_BN_AUDIO_SMOKE_SUMMARY.json`

Evidence:
- Archive SHA256: `50ddfd62fd5778045c25b9152a0cbc3e5c182ff924975848e9d72cee9ab79352`.
- Audio device `plughw:CARD=vc4hdmi1,DEV=0` was confirmed usable.
- Direct regenerated alarm response tone was audible by user report.
- `e50_bn_audio_timer_smoke_001` executed `TIMER`, played the response WAV according to JSON, and the user reported hearing the tone response.
- `e50_bn_audio_alarm_retry_001` was rejected below the command threshold, so no response was attempted; this is not an audio failure.
- UNKNOWN phrase was safely rejected with no action.

Decision:
- Response playback is partially verified on Pi for at least one accepted command.
- Continue with prompted multi-cycle smoke before all-19 validation.
- Do not train, tune thresholds, or change E50 to address remaining wake/recognition variability.

## Phase BN Addendum - Prompted Repeated-Cycle Audio Evidence - 2026-09-28

Purpose: record prompted repeated-cycle Pi evidence after fixing the response-audio path and using visible prompts for each command.

Artifacts:
- `outputs/e50_bn_prompted_multicycle_20260928_evidence.tar.gz`
- `results/phase_bn_final_pi_validation_runtime_hardening_20260928/PHASE_BN_PROMPTED_MULTICYCLE_ADDENDUM_20260928.md`
- `results/phase_bn_final_pi_validation_runtime_hardening_20260928/PHASE_BN_PROMPTED_MULTICYCLE_RESULTS.csv`
- `results/phase_bn_final_pi_validation_runtime_hardening_20260928/PHASE_BN_PROMPTED_MULTICYCLE_SUMMARY.json`

Evidence:
- Archive SHA256: `10011b1364b73820a62853e784a7896bd649a10e9bada96656274674ec6be4f4`.
- `ALARM`, `TIMER`, `PAUSE`, and `LIST_REMINDERS` each passed wake, command acceptance, action execution, response playback according to JSON, and returned-to-listening.
- User reported audible tones for all four prompted trials.
- GPIO remained disabled/requested false.

Decision:
- Proceed to Phase BN all-19 prompted validation next.
- Keep all 19 commands callable/testable; do not convert unresolved commands into unavailable commands.
- Do not train, tune thresholds, modify E37/E40/E50, or add a demo whitelist.

## Phase BN Addendum - All-19 Prompted Pi Validation - 2026-09-28

Purpose: record a complete prompted physical audit across the final 19-command vocabulary plus one UNKNOWN phrase.

Artifacts:
- `outputs/e50_bn_all19_validation_20260928_evidence.tar.gz`
- `results/phase_bn_final_pi_validation_runtime_hardening_20260928/PHASE_BN_ALL19_PI_VALIDATION_ADDENDUM_20260928.md`
- `results/phase_bn_final_pi_validation_runtime_hardening_20260928/PHASE_BN_ALL19_PI_VALIDATION_RESULTS.csv`
- `results/phase_bn_final_pi_validation_runtime_hardening_20260928/PHASE_BN_ALL19_PI_VALIDATION_SUMMARY.json`
- `results/phase_bn_final_pi_validation_runtime_hardening_20260928/PHASE_BN_ALL19_COMMAND_STATUS_AFTER_PI_VALIDATION.csv`

Evidence:
- Archive SHA256: `18b7bda8aff4dc9de12568e20626069547f51c03397deffe222ab6fad7115e98`.
- 20 total trials: 19 commands plus UNKNOWN.
- Wake accepted 19/20 trials.
- Raw correct command predictions: 13/19.
- End-to-end audio passes: 10/19.
- Accepted-wrong command actions: 0.
- UNKNOWN safe rejection: true.

Decision:
- Use this as the complete all-19 physical audit snapshot.
- Keep all 19 commands callable/testable.
- Report current misses as safe rejections/wake miss/not verified, not as unavailable.
- `TEMPERATURE` remains globally unsafe/not demo-ready because earlier accepted-wrong evidence remains binding.

## 2026-09-29 - Phase BN Final Deployment Guide Follow-Through

Purpose: consolidate the frozen E37+E50+E40-compatible final deployment package according to the final deployment guide, preserving honest evidence boundaries.

Executed:
- Added touchscreen GUI controller for START / STOP / STATUS around the existing E37+E50 runtime.
- Added launch script and desktop-entry template for Raspberry Pi local operation.
- Generated final integration report, professor command sheet, demo script, callability table, response inventory, path/configuration audit, and final SHA256 manifest.

Measured evidence reused:
- Latest all-19 prompted Pi validation: 20 trials, 19 command trials, 10/19 end-to-end audio passes, 0 accepted-wrong command actions, UNKNOWN safe rejection, 20/20 returned to listening.
- Prompted multicycle evidence: 4/4 prompted single-cycle invocations passed with audible response feedback by operator report and JSON `response_result.played=true`.

Interpretation: the system is packaged for standalone offline demo staging, but complete standalone deployment is not yet fully verified because physical touchscreen operation, same-process continuous-loop behavior, disconnected no-laptop offline test, non-primary-speaker validation, and Pi performance measurements remain incomplete or not measured.

No model, threshold, preprocessing, E40, E37, E50, router/action, or production behavior changes were made.

## 2026-09-29 - Phase BN Human Response Recording Correction

Purpose: align deployment evidence with the final guide requirement that command responses be recorded human speech rather than tones.

Result: current response WAV files are not final-compliant. Every current response file was classified as `FAIL_TOO_SHORT_LIKELY_PLACEHOLDER`; the files remain useful only for audio-path smoke testing.

New tooling:
- `scripts/record_human_command_responses.py`
- `scripts/verify_human_command_responses.py`

Required next physical step: record fresh human response WAVs on the Raspberry Pi and verify speaker playback before claiming final response compliance.

No model training, threshold tuning, E37/E40/E50 modification, preprocessing change, router/action change, or live validation occurred.



## 2026-09-29 - Phase BN-CLOSE Final Deployment Verification Staging

Phase BN-CLOSE was started as the final physical Raspberry Pi deployment verification phase under a full model freeze. No CNN training, fine-tuning, threshold tuning, preprocessing change, E37/E40/E50 modification, command removal, or runtime demo whitelist was performed.

Created BN-CLOSE closeout artifacts under `results/phase_bn_close_final_deployment_verification_20260929/`:

- `PHASE_BN_CLOSE_FINAL_VERIFICATION_REPORT.md`
- `PHASE_BN_CLOSE_DEPLOYMENT_AUDIT.csv`
- `PHASE_BN_CLOSE_TOUCHSCREEN_TEST.csv`
- `PHASE_BN_CLOSE_MULTICYCLE_RESULTS.csv`
- `PHASE_BN_CLOSE_PERSISTENT_LOOP_EVIDENCE.md`
- `PHASE_BN_CLOSE_RESPONSE_PLAYBACK.csv`
- `PHASE_BN_CLOSE_UNKNOWN_SAFETY.csv`
- `PHASE_BN_CLOSE_STANDALONE_DEMO_EVIDENCE.md`
- `PHASE_BN_CLOSE_PI_PERFORMANCE.csv`
- `PHASE_BN_CLOSE_FINAL_19_COMMAND_STATUS.csv`
- `PHASE_BN_CLOSE_FINAL_DEMO_READY_COMMANDS.csv`
- `PHASE_BN_CLOSE_FINAL_REQUIREMENTS_AUDIT.csv`
- `PHASE_BN_CLOSE_PI_HANDOFF.md`
- `PHASE_BN_CLOSE_FINAL_SHA256SUMS.csv`

Added Pi-side helper scripts to `deployment/vcm_pi_package/scripts/` for deployment audit, response playback audit, persistent same-process loop testing, and Pi performance probing.

Created BN-CLOSE verification tools archive `outputs/e50_bn_close_verification_tools_20260929.tar.gz` with SHA256 `ca985d8597de5f8ca30eb37c94d4c365fce9536671bcae0374aa11ba21b99a7d`. This is not a final verified deployment archive.

Current BN-CLOSE status: PARTIAL FINAL DEPLOYMENT STAGING COMPLETE; FINAL DEPLOYMENT NOT YET VERIFIED. Physical-only requirements remain pending: touchscreen validation, same-process 5/10/20-cycle loop proof, final human recorded response playback, fully standalone/no-laptop operation, Wi-Fi/Ethernet-off operation, Pi CPU/RAM/temperature/latency measurement, and non-primary-speaker validation.

Important evidence boundary: all 19 commands remain callable/testable; 10/19 had end-to-end audio pass in the latest all-19 prompted Pi audit with 0 accepted-wrong actions, but `TEMPERATURE` remains globally unsafe/not demo-ready because prior accepted-wrong live evidence remains binding.

## 2026-09-29 - Phase BN-CLOSE Round1 Pi Evidence

- Ingested `outputs/e50_bn_close_20260929_evidence_round1.tar.gz`.
- Archive SHA256: `ac371525a5436cb153e239da4aeabe526b34086024de4699a2bc24fb142d5c8b`.
- Deployment audit and response playback CSV were captured from the Pi.
- Same-process 5-cycle runtime test passed for wake/classification/action/return-to-listening: 5/5 wake accepted, 5/5 commands accepted/executed (`PLAY_MUSIC`, `TIMER`, `ALARM`, `PAUSE`, `LIST_REMINDERS`), 5/5 returned to listening, GPIO requested false.
- Runtime response playback failed because it used `plughw:CARD=vc4hdmi1,DEV=0`, which returned ALSA error 524.
- Audio recheck proved `plughw:CARD=vc4hdmi0,DEV=0` and `default` can play `responses/timer.wav`; operator reported hearing the timer response twice.
- Failure layer: `RESPONSE_PLAYBACK_DEVICE_SELECTION`, not CNN, threshold, router, action, or persistent loop.
- Updated BN-CLOSE handoff/helper defaults to use `plughw:CARD=vc4hdmi0,DEV=0` for subsequent response playback tests.
- Rebuilt verification tools archive SHA256: `e774637643861a2c43d7554da05a19d5a961df9a0efd5e74157c4481b53109ad`.

## 2026-09-29 - Phase BN-CLOSE Round2 Transcript Evidence

- Parsed pasted Pi terminal transcript for `OUT=pi_validation/e50_bn_close_20260929_round2`.
- Runtime used `RESPONSE_AUDIO_DEVICE=plughw:CARD=vc4hdmi0,DEV=0`.
- Same-process 5-cycle loop transcript shows 5/5 wake accepted, 5/5 commands accepted/executed, 5/5 response playback JSON true, 5/5 returned to listening, and GPIO requested false.
- Commands: `PLAY_MUSIC`, `TIMER`, `ALARM`, `PAUSE`, `LIST_REMINDERS`.
- Operator reported hearing all response playback first and then correct answers to all commands.
- Created `PHASE_BN_CLOSE_ROUND2_TRANSCRIPT_ADDENDUM.md`, `PHASE_BN_CLOSE_ROUND2_TRANSCRIPT_LOOP_RESULTS.csv`, and `PHASE_BN_CLOSE_ROUND2_TRANSCRIPT_SUMMARY.json`.
- Boundary: source Pi archive for `pi_validation/e50_bn_close_20260929_round2` still must be copied back before treating this as fully preserved evidence.

## 2026-09-29 - Phase BN-CLOSE Boosted Response Assets

Created boosted response WAV assets for louder Pi playback while preserving the original files. The current `responses/*.wav` files were copied to `responses_original_pre_boost_20260929/`; boosted `_boosted.wav` files were written to `responses_boosted/`; `configs/demo_response_assets.json` now points to the boosted filenames for all 19 commands plus UNKNOWN. Manifest: `deployment/vcm_pi_package/PHASE_BN_CLOSE_RESPONSE_BOOST_MANIFEST_20260929.csv`.

This is an audio asset/configuration update only. It does not change E37, E50, E40 thresholds, preprocessing, routing, action behavior, GPIO behavior, or command callability. Human-response compliance remains separately dependent on the actual response recordings and Pi playback verification.

## 2026-09-29 - Phase BN-CLOSE Source Archive and Extra-Loud Response Preservation

Preserved and ingested Round2 source evidence archive `outputs/e50_bn_close_20260929_round2_evidence.tar.gz`, SHA256 `f21ce0f86552978dbdbeeba31afb7ef3849e04cb788e257ebc1dc5639b00865f`. Source-backed summary confirms 5/5 wake accepted, 5/5 commands accepted/executed, 5/5 response playback true, 5/5 returned to listening, and GPIO requested false for `PLAY_MUSIC`, `TIMER`, `ALARM`, `PAUSE`, and `LIST_REMINDERS`.

Preserved and ingested extra-loud response archive `outputs/e50_bn_close_extra_loud_responses_20260929.tar.gz`, SHA256 `9ce3be48ee05738305a189a15eb0e1de4c126767084138266f11cdb32d1f1128`. The active map covers all 19 commands plus UNKNOWN and points to existing `responses_extra_loud_20260929/*_extra_loud.wav` files. Operator reported the extra-loud responses were perfect. The earlier Windows-side boosted response package is not the deployment response set.

## 2026-09-29 - Phase BN-CLOSE Wake-Wait Runtime Update

Implemented an interaction fix for the fast return-to-listening problem. `pi_wake_voice_control_demo.py` now supports `--wait-for-wake`, which keeps recording wake windows indefinitely until the wake phrase is accepted. Added `run_phase_bn_close_wake_wait_demo.sh` as the Pi demo wrapper for this mode.

Archive: `outputs/e50_bn_close_wake_wait_runtime_update_20260929.tar.gz`, SHA256 `8e991c75c2d85c334dcf58df558881e163522d361911175a64c3de96fbc521c6`.

No classifier, threshold, preprocessing, router, action, GPIO, or command-vocabulary behavior changed.

## 2026-09-29 - Phase BN-CLOSE Wake-Wait Physical Evidence

Preserved and ingested `outputs/e50_bn_close_wake_wait_20260929_evidence.tar.gz`, SHA256 `c8223dd8eec144baa1cdbf28803856695eac2897511f2eba2a27741126a6539f`.

Summary: 13 completed result JSON files, 13/13 wake accepted, 13/13 returned to listening, 8 executed commands with response playback true, and 0 GPIO requests. Trials `e50_bn_close_wake_wait_012` and `e50_bn_close_wake_wait_013` required multiple wake attempts before acceptance, confirming the runtime continues listening until the next wake phrase is heard.

Interpretation: wake-wait interaction is physically verified. Remaining below-threshold command rejections are command-recognition/threshold behavior after wake acceptance, not a wake-listening lifecycle failure.

## 2026-09-29 - Phase BN-CLOSE Touchscreen GUI Wake-Wait Validation Package

Prepared the physical touchscreen GUI validation update using the verified wake-wait listening lifecycle.

Archive: `outputs/e50_bn_close_touchscreen_gui_wake_wait_update_20260929.tar.gz`, SHA256 `b298efe060150c0ac57c6410a2ff9a23ab34e6ef7ab57c2de94c4eb978b84f33`.

Changes:

- GUI START now launches `pi_wake_voice_control_demo.py` with `--wait-for-wake`.
- GUI wake attempts are unlimited by default.
- GUI response playback defaults to `plughw:CARD=vc4hdmi0,DEV=0`.
- Deployment response map points to the accepted extra-loud Pi response set.
- Added a Pi-side validation launcher that opens the GUI and then summarizes generated evidence JSON into CSV/JSON.

Boundary: touchscreen GUI validation still requires a physical Pi touchscreen run. This step prepared the deployment update and handoff; it did not create final touchscreen evidence.

## 2026-09-29 - Phase BN-CLOSE Touchscreen GUI Reject-State Fix

During physical touchscreen validation, the GUI was observed to remain visually stuck on `COMMAND REJECTED` after a rejected command, even though the desired demo behavior is to return clearly to wake listening.

Prepared `outputs/e50_bn_close_touchscreen_gui_reject_state_fix_20260929.tar.gz`, SHA256 `d230124dd28aef048a467a0707c1e7dd3df399442aa319f986418915f7229c0e`.

The GUI now distinguishes:

- `LISTENING`: say `hey pi`;
- `TELL ME WHAT YOU NEED`: wake accepted, say the command;
- `STILL LISTENING`: wake was missed or command was rejected safely, say `hey pi` again.

This is a GUI status/display correction only. Recognition models, thresholds, preprocessing, wake-wait runtime semantics, routing, actions, GPIO, response assets, and command callability remain unchanged.

## 2026-09-30 - Section 68 Controlled Validation Items 10-15

Purpose: close the remaining physical-validation blockers identified by the E50 Section 68 read-only hard-stop audit before beginning Item 16 final benchmark designation.

Frozen stack:

- Wake: `E37_TARGETED_COLOR_VOLUME_FIX`
- Command: `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT`
- Policy: `configs/e50_revised_vocab_e40_thresholds.json` / E40-compatible guardrail policy
- E50 SHA256: `BC8AC64CED4305DDF43BF4DE377F3CC636A764EFF339CD9F92AF06340C50B8FF`

Evidence and results:

- Item 10 duplicate runtime: VERIFIED using `pi_validation/e50_bn_close_item10_duplicate_runtime_20260930_084836`; archive `e50_bn_close_item10_duplicate_runtime_20260930_084836_three_cycle_evidence.tar.gz`; SHA256 `712b36c7d8b54af7dc551f65a43199a4c5d909d04daa428aa589e28d8ba9bfe8`.
- Item 11 standalone offline: VERIFIED using network-off local Pi evidence `pi_validation/e50_bn_close_item11_network_off_20260930_093353`; archive `e50_bn_close_item11_network_off_20260930_093353_evidence.tar.gz`; SHA256 `215f33cbe05a40b5fdb285fe77e1d91a122d3fa494fd5593c5684fa1b59d561a`.
- Item 12 safety sweep: VERIFIED using `pi_validation/e50_bn_close_item12_safety_sweep_20260930_094547`; archive `e50_bn_close_item12_safety_sweep_20260930_094547_evidence.tar.gz`; SHA256 `1523324c4a60ac4c2545a7220ecb38f125b4c9729a8ae75225332a6ca639ce89`. Result: 4 safety/rejection cases, 0 unintended actions, 0 duplicate actions, 5/5 returned to listening, valid TIMER recovery succeeded.
- Item 14 non-primary speaker: VERIFIED using `pi_validation/e50_bn_close_item14_non_primary_speaker_20260930_095358`; archive `e50_bn_close_item14_non_primary_speaker_20260930_095358_evidence.tar.gz`; SHA256 `360603516a3e7d4ea5747a5e7f08988c3655c1d17fee72a77edcc9446c73f5e3`. Result: Speaker B was genuinely non-primary, 9 captured trials, 9/9 wake accepted, 9/9 returned to listening, 4 executed, 5 rejected, 4 accepted-wrong. Speaker B's voice was softer than the primary speaker; this is a measured limitation, not a reason to retrain during Section 68 closeout.
- Item 15 Pi performance: PARTIALLY VERIFIED using `pi_validation/e50_bn_close_item15_performance_20260930_102647`; archive `e50_bn_close_item15_performance_20260930_102647_evidence.tar.gz`; SHA256 `7300b975256ddd2278ed9253aa2c4e8d439b4beca221cf23ef875fa929e93f91`.

Item 15 measured values:

- Model load: 1.8566 seconds.
- Saved-WAV E50 command inference, 70 runs: mean 31.82 ms, median 31.39 ms, min 29.18 ms, max 38.31 ms, p90 33.94 ms, p95 34.40 ms.
- CPU during inference benchmark: 99.55 percent.
- Temperature: 42.2 C pre-runtime, 46.1 C post-GUI run, 46.3 C benchmark start, 48.5 C benchmark end.
- Memory: 464 MiB used pre-runtime, 535 MiB used post-GUI run; benchmark memory used rose from 592,320 KiB to 785,104 KiB.

Limitations:

- Wake-miss/no-wake safety periods do not emit result JSON in wake-wait mode; Item 12 uses operator sequence plus absence of action/result entries for those cases.
- Item 15 does not separately measure GUI launch-to-ready, wake detection latency, live preprocessing-only timing, live CNN-only timing separate from saved-WAV benchmark, confidence-check-only timing, router/action-only timing, response playback start latency, or total user-perceived cycle timing.

No E50 product behavior was modified by this log update. The next controlled Section 68 task is Item 16 final benchmark designation.

## 2026-09-30 - Section 68 Item 16 Final Benchmark Recording

Purpose: formally record the final benchmark for the frozen E50 system without running a new optimization cycle.

Evidence directory: `pi_validation/e50_bn_close_item16_final_benchmark_20260930_105703`.

Archive: `outputs/e50_bn_close_item16_final_benchmark_20260930_105703_evidence.tar.gz`.

Archive SHA256: `b6a2d9e66f42a1d6b4eb118f9e02505361072582e29b50add9761b1d359b5da1`.

Primary benchmark population: one prompted physical Pi trial for each of the 19 required command labels plus one unsupported UNKNOWN/no-action phrase.

Metrics:

- Wake success: 19/20 overall; 18/19 valid commands.
- Raw command classification: 13/19.
- Acceptance: 10/19 valid commands.
- Accepted-correct: 10.
- Accepted-wrong: 0.
- Accepted-action precision: 100%.
- Safe rejection among non-executed trials: 10/10.
- End-to-end action success: 10/19 valid commands.
- UNKNOWN/no-action safety: 1/1.
- Return-to-listening: 20/20.

Limitations: the all-19 benchmark is one prompted trial per command; the all-19 primary run predates the final network-off touchscreen launch proof, so later Section 68 evidence is cited as supporting lifecycle/standalone evidence. `TEMPERATURE` remains callable but not demo-safe because historical accepted-wrong evidence remains binding.

No E50 product behavior was modified.

## 2026-09-30 - Final Evidence / User-Voice / Unresolved-Item Sweep

Purpose: audit the final E50 evidence chain and professor package claims without changing the frozen VCM.

This was not a model experiment. No training, threshold tuning, E37/E40/E50 modification, router change, runtime change, GUI behavior change, response-asset change, dataset change, command-vocabulary change, or demo whitelist was performed.

Frozen identities verified:

- E50 command model SHA256: `BC8AC64CED4305DDF43BF4DE377F3CC636A764EFF339CD9F92AF06340C50B8FF`.
- E37 weights SHA256: `687E82E2CEFA6D74CEF2C0A15D28F8F6142D47D4A67E57C68C091E83FC2CEBDE`.
- E37 normalization SHA256: `3BFA93F202DC0C241E577E5B89506F2CB6D0F35B8239297C215A7F81E970B4C7`.
- E40 policy SHA256: `A0B2495328FD5A1E0E5885E727623BA6D9F823BE94CCCDFD0AEAD77254BBB3FD`.

User-voice audit:

- Known user-recorded Phase AF material: 105 targeted clips collected for recovery investigation.
- Final E50/BG training composition: 16,100 rows total; 13,070 active-project training rows; 2,800 Dataset2 training rows; 230 E41 reconstructed adaptation rows.
- Final training-manifest search found 0 `PHASE_AF`, `targeted_live`, or `recovery_training` matches.
- BG contamination check evidence reports 0 protected path overlaps and 0 protected SHA256 overlaps.
- Older Pi adaptation/recovery audio is present in training, but the project records do not establish speaker identity from filenames alone.
- Final classification: INDETERMINATE for absolute user-voice exclusion; SUPPORTED for non-inclusion of the identified Phase AF targeted recovery clips in final E50/BG training.

Package and unresolved-item audit:

- Professor package remains grade-ready with documented limitations.
- Deployability remains partially verified because a fresh GitHub package-copy Pi GUI launch was not completed.
- Not measured: GUI launch-to-ready, acoustic response onset, full acoustic latency, ECE, noise/reverb, formal phrasing benchmark, formal statistical speaker-independence benchmark.
- Not applicable: slot/parameter accuracy and cross-team ranking.
- Timing-only disposable instrumentation evidence is preserved as supplementary timing evidence and does not replace Item 15.

Final package audit values recorded:

- Package path: `github_package/ME2_VCM_E50_GITHUB_PACKAGE_20260930`.
- Files including manifest: 121.
- Manifest rows: 120.
- Package size: 20,114,600 bytes.
- `PACKAGE_FILE_MANIFEST.csv` SHA256: `D3D01317E936F8090EF36E484922D2A2D1CF4784D7B5C3FC6B0FB37536840F79`.

Main-project logging update boundary: the GitHub package directory was not modified by this logging pass.

## 2026-09-30 - E50-DOC-OVERFIT-20260930

Purpose: audit the frozen E50 epoch-level training history to determine whether the training trajectory exhibits classical overfitting and clarify its relationship to the selected deployment checkpoint.

Inputs:

- `results/phase_bg_e50_bg_revised_vocab_original_preserve_e41_init_20260928/E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT_history.csv`
- `results/phase_bg_e50_bg_revised_vocab_original_preserve_e41_init_20260928/PHASE_BG_TRAINING_RESULTS.json`
- Phase BG final documentation stating checkpoint selection by internal validation loss only
- Final frozen E50 model identity

Findings:

- E50 training history was found and contains 11 epochs.
- `PHASE_BG_TRAINING_RESULTS.json` records `best_epoch=7` and `best_internal_validation_loss=1.3987702131271362`.
- Epoch 7 metrics: training loss `0.3457678720680258`, training accuracy `0.8800621118012423`, validation loss `1.3987702131271362`, validation accuracy `0.6197039305768249`.
- Epoch 11 metrics: training loss `0.19462700002634573`, training accuracy `0.9322360248447205`, validation loss `2.188316583633423`, validation accuracy `0.6018376722817764`.
- The post-epoch-7 trajectory shows training loss decreasing and training accuracy increasing while validation loss worsens and validation accuracy fails to improve meaningfully.
- Later epochs were not selected for deployment; the selected E50 checkpoint corresponds to the best internal validation-loss point.

Model change: NONE.

Deployment change: NONE.

Training change: NONE.

Conclusion: the E50 training trajectory demonstrates classical overfitting after the selected epoch-7 checkpoint, but this does not establish that the deployed epoch-7 checkpoint itself is a late overfit model. The finding is documented as a training-dynamics limitation and explanatory factor, while the independent/live generalization gap remains a separate multi-factor result.

Failure-attribution review added: documentation now distinguishes training-dynamics overfitting from command-level classification errors, confidence rejection, data coverage limitations, domain/speaker variation, and downstream action/output behavior.

Model modification: NONE.

Training: NONE.

Deployment: NONE.

Benchmark rerun: NONE.
