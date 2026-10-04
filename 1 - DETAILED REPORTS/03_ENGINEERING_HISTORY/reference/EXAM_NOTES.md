# EXAM_NOTES

This file collects questions and answers that may be useful for an oral exam or defense. Answers should become more specific as implementation evidence is collected.

## Convention

All exam notes must be filed under the phase where the concept is introduced or used.

Use this structure for new entries:

```text
## Phase N - Phase Name

### Q: Question?

Answer...
```

If a concept applies to multiple phases, place it in the earliest phase where it becomes necessary, then cross-reference it later if needed.

## Phase 0 - Requirements And System Architecture

### Q: What does the 100/100 target mean for this machine exercise?

The assignment is worth 100 points, so the project goal is complete requirement
coverage rather than a single working clip. The system must show a built dataset,
a trained individual VCM, a benchmark, measured validation, a Raspberry Pi
real-world demo, tiny real-time on-device behavior, standalone operation, and no
cloud model, LLM, or ASR-based command recognition.

For the final demo, this means every required command category should be
recognizable and should route to the intended local action or simulation.

### Q: What is a Voice Command Model?

A Voice Command Model is a small model that directly classifies an audio command into a fixed set of command intents, such as LIGHT_CONTROL or SET_TIMER. It does not need to transcribe full speech into text.

### Q: How is a VCM different from ASR?

ASR converts speech into text. A VCM directly predicts a command intent from audio features. For this assignment, VCM is preferred because it can be much smaller and can run locally on a Raspberry Pi.

### Q: Why are ASR, cloud speech APIs, and LLMs not used in the final system?

The assignment requires standalone on-device inference and explicitly says no cloud models and no LLM. ASR also has a larger footprint than a direct command classifier.

### Q: Why include UNKNOWN?

UNKNOWN prevents the system from forcing every sound into one of the 10 known command categories. This is important for open-set rejection, safety, and realistic use.

### Q: What must be measured to prove the model is tiny?

At minimum: parameter count, model file size, inference latency, RAM usage, and CPU utilization where practical. Raspberry Pi measurements are NOT YET MEASURED.

### Q: Why is Raspberry Pi testing required?

The assignment requires a real-world demo and real-time operation on Raspberry Pi 4 or 5. Desktop performance alone cannot prove embedded performance.

### Q: How do we avoid the Raspberry Pi always listening?

The current exam-safe demo uses record-then-infer, also called push-to-talk or
triggered listening. The system is not continuously executing command
classification. Instead, the user starts one command capture, the Pi records a
short audio window, preprocesses it, runs local CNN inference, and then accepts
or rejects the command.

Current demo flow:

```text
start command -> record 4 seconds -> preprocess -> CNN inference -> action/reject
```

This is live microphone inference because the audio is freshly recorded during
the demo, but it is not always-listening streaming.

A wake word can be added later as a first-stage detector:

```text
wake-word detector -> command recorder -> VCM classifier -> action router
```

For example, a first model could detect `hey pi` versus non-wake audio. Only
after the wake word is accepted would the system record and classify the actual
command. This still means the device listens at a low level for the wake word,
but it does not continuously execute every command classifier/action path.

Exam explanation:

```text
For this demo, I use triggered record-then-infer mode so the Pi is not always
acting on ambient audio. A wake-word detector can be added as a separate first
stage, but I kept the main model focused on reliable fixed-vocabulary command
classification.
```

## Phase 1 - Dataset Inspection, Provenance, And Splitting

### Q: Why inspect the dataset before training?

The dataset determines labels, sample rates, speaker metadata, class balance, duration, and possible data leakage risks. Training before inspection can create invalid results.

### Q: Why is speaker-independent splitting important?

If the same speaker appears in train and test sets, the model may learn speaker-specific patterns instead of general command patterns. That inflates test performance and weakens the benchmark.

### Q: Why not augment immediately?

The current dataset already includes many speakers, multiple phrases, and acoustic variants. Training the first baseline without extra augmentation gives a clean reference point. Later augmentation should be train-only and should be added as a separate experiment only if measured results show it is needed.

### Q: Why must validation and test data not be augmented?

Validation and test sets should represent unseen data. If augmented versions leak across splits, the evaluation can become too easy and inflate performance. Augmentation belongs only in training unless a separate robustness benchmark is explicitly designed.

### Q: What is the provenance of our dataset?

The dataset is based on source documentation from Mark Andrian Macalalad's listed sources: SLURP, Fluent Speech Commands, Google Speech Commands v2, eSpeak NG, and Chatterbox TTS with LibriSpeech/Common Voice references. The final local copy is stored offline in `data/drive-download-*` folders and contains short voice-command WAV files for VCM training.

### Q: How is the dataset structured?

It has class folders for 20 raw command labels. Filenames encode raw label, speaker ID, phrase ID, and acoustic variation ID, such as `WEATHER_s5_p2_v2.wav`. The official metadata index maps those raw labels into the 10 assignment command intents and assigns speaker-aware train/validation/test splits.

### Q: What are the dataset limitations?

UNKNOWN is not present as a raw class, speaker IDs are inferred from filenames, and one duplicate-style WEATHER file was excluded. These limitations must be stated honestly during reporting and addressed before final validation.

### Q: How do the Datasets and Dataloaders lecture concepts connect to this VCM project?

The lecture defines a dataset as paired samples and labels, usually written as
`D = (x, y)`. In this project, each `x` is an audio command file and each `y`
is the command label or intent. At the raw dataset level, `y` can be a raw
command such as `LIGHT_ON`, `NEXT`, or `VOLUME_DOWN`. At the assignment level,
some raw commands are mapped into broader intents such as `LIGHT_CONTROL` or
`MEDIA_CONTROL`.

The lecture topic of data sources connects directly to our project because the
dataset is built from collected command audio, posted collective data, and live
Raspberry Pi microphone recordings. The new posted collective dataset also
contains a master dataset, balanced training subset, manifests, provenance files,
class-distribution reports, and augmentation reports. These are dataset
engineering artifacts, not just loose audio files.

The lecture topic of labelling or annotation connects to the manifest/index
files. In our original local dataset, filenames encode label, speaker, phrase,
and variation. The script `data/metadata/build_dataset_index.py` turns that
filename structure into a metadata table with raw labels, assignment intents,
speaker IDs, phrase IDs, split, sample rate, channels, duration, and inclusion
status. In the new collective dataset, labels and provenance are stored directly
in CSV manifests.

The lecture topic of sufficiency asks whether the target test performance is
achievable with a capable model. For us, sufficiency is not only the number of
WAV files. It also means the dataset must cover enough speakers, microphones,
noise, silence, unknown audio, and command classes to support a Raspberry Pi
voice-command demo. Our original 21,000-file dataset was sufficient for an
initial CNN baseline, but not fully sufficient for Pi microphone deployment.
That is why we added Pi calibration recordings and are considering targeted
acoustic augmentation.

The lecture topic of train/validation/test splitting connects to our
speaker-aware split. The lecture gives common ratios such as 70/10/20,
70/20/10, 80/0/20, and 80/10/10 and emphasizes no duplicated samples across
splits. Our original dataset uses an 80/10/10-style split while avoiding speaker
overlap within each source group. This reduces the risk that validation or test
performance is inflated by the same speaker appearing in training.

The lecture topic of bias connects to our project through class imbalance,
speaker imbalance, microphone/domain mismatch, synthetic-versus-real audio, and
measurement bias. For example, if all Pi calibration clips are from one
microphone and one speaker, the model may perform well for that setup but fail
for another speaker or microphone. That is why our current framing separates
fixed phrase vocabulary from acoustic robustness.

The lecture topic of dataloaders connects to how training examples are fed into
the model. Although the project currently uses TensorFlow-style tensors and
custom training loops rather than PyTorch `DataLoader`, the same concept is
present: load an example, preprocess it into a fixed tensor, pair it with a
label, batch examples, shuffle training data, and keep validation/test separate.

In short, the lecture maps to our project as follows:

| Lecture concept | VCM application |
| --- | --- |
| Dataset `D = (x, y)` | WAV/log-Mel command sample plus command label |
| Data source | Collective dataset, public speech sources, Pi microphone recordings |
| Annotation | Raw command labels and assignment intent mapping |
| Data structure | Manifests, metadata CSVs, class folders, provenance reports |
| Sufficiency | Enough classes, speakers, acoustic conditions, unknown/silence |
| Train/val/test | Speaker-aware split and held-out Pi validation |
| Bias | Class imbalance, speaker leakage, mic mismatch, synthetic data limits |
| Dataloader | Batch loading, shuffling, preprocessing, label encoding |

The exam explanation should emphasize that building the dataset is an
engineering task: we do not just collect files; we define labels, preserve
provenance, choose splits, check leakage, preprocess consistently, and evaluate
on held-out data.

### Q: How are we using the newly posted collective dataset?

The newly posted collective dataset under
`C:\Users\Loreen Anne\Downloads\VCM\VCM` is being treated as a curated dataset
reference and possible selective training support, not as a reason to restart
the project.

It contains two useful parts:

- `VCM_MASTER`: a frozen master dataset with train/validation/test manifests.
- `VCM_BALANCED`: a balanced/augmented training subset.

It is useful because it includes dataset engineering artifacts that support the
lecture concepts: manifests, provenance files, class distribution reports,
audio-quality reports, augmentation reports, and speaker-leakage audits. It also
includes `UNKNOWN` and `SILENCE`, which are important for rejection and
realistic command recognition.

However, the project already has a working Raspberry Pi deployment pipeline,
live Pi microphone calibration data, raw-command recovery experiments, and
action-routing code. Restarting around the new dataset would be inefficient and
risky. The better decision is:

```text
cite/document first, integrate selectively
```

This means the new dataset can strengthen the report, dataset discussion,
`UNKNOWN`/`SILENCE` handling, and future efficient training experiments, while
the existing Pi pipeline remains the deployment path.

Exam explanation:

```text
I did not restart the implementation when the new posted dataset became
available. Instead, I treated it as an official curated reference and possible
selective training source. The Raspberry Pi calibration data remains essential
because final performance depends on the actual deployment microphone and local
hardware.
```

## Phase 2 - Audio Preprocessing And Log-Mel Features

### Q: What is log-Mel?

Log-Mel features represent audio energy over time using frequency bands spaced like human hearing. The logarithm compresses large energy differences and often improves speech-command learning.

### Q: What is log-Mel preprocessing?

Log-Mel preprocessing converts waveform audio into a time-frequency representation. The audio is split into short frames, each frame is transformed into a frequency spectrum, frequencies are grouped with a Mel filterbank, and the logarithm compresses the energy range.

### Q: Why use a 4-second fixed input window?

The observed dataset duration range is 0.200 s to 3.880 s. A 4-second window preserves the current examples without truncating normal commands. Shorter utterances are padded with zeros. This creates a fixed input shape for CNN training.

### Q: Why 25 ms windows and 10 ms hop?

These are common speech-processing settings. A 25 ms frame is short enough to capture local speech acoustics, and a 10 ms hop gives overlapping frames so the spectrogram changes smoothly over time.

### Q: Why must Raspberry Pi inference use the same preprocessing?

If desktop training uses one feature pipeline and Raspberry Pi inference uses another, the model will receive different input distributions. That can break accuracy even when the model file is correct.

### Q: Why is audio standardized to 16 kHz mono?

The model needs every example to have the same sampling format. `16 kHz` is enough for speech commands because most speech information needed for command recognition is below 8 kHz, which is the highest representable frequency after 16 kHz sampling. Mono is used because the command intent does not require stereo location information. Standardizing to 16 kHz mono also reduces memory, computation, and Raspberry Pi inference cost.

In this project, the active dataset is already 16 kHz mono, but the loader still checks and can resample if needed so training and deployment use the same convention.

### Q: Why is a fixed input shape required for CNN training?

A CNN expects tensors with consistent dimensions so batches can be stacked together during training. If one audio file produced a 1-second spectrogram and another produced a 3.8-second spectrogram, they would have different time dimensions and could not be placed in the same batch without padding or trimming.

In this project, every audio example is padded or trimmed to 4 seconds, which becomes 64,000 audio samples and then a fixed `398 x 40` log-Mel feature matrix.

### Q: What does framing mean?

Framing means cutting the audio waveform into many short overlapping windows. Instead of analyzing the entire command as one block, we analyze small slices over time.

In this project, each frame is 25 ms long and starts every 10 ms. That gives overlapping frames, which helps capture how speech changes over time while preserving local sound patterns such as vowels, consonants, and syllable transitions.

### Q: What does STFT/FFT do?

FFT means Fast Fourier Transform. It converts one short frame of audio from the time domain into the frequency domain, showing how much energy exists at different frequencies.

STFT means Short-Time Fourier Transform. It applies the FFT repeatedly across many short frames. The result is a time-frequency representation: frequency content for each moment in the audio command.

For VCM, this matters because the model should learn patterns in speech sounds, not raw waveform samples only.

### Q: What is a Mel filterbank?

A Mel filterbank groups FFT frequency bins into perceptual frequency bands. The Mel scale spaces low frequencies more finely and high frequencies more coarsely, roughly matching how human hearing perceives pitch.

In this project, the filterbank produces 40 Mel bins per frame. That compresses the spectrum into a smaller representation while keeping information useful for speech-command classification.

### Q: Why are log-Mel features useful for command recognition?

Log-Mel features are useful because they represent speech as a compact image-like matrix: time on one axis and perceptual frequency bands on the other. CNNs can learn local patterns in that matrix, such as frequency shapes and transitions associated with words.

The logarithm compresses large energy differences, making quiet and loud parts easier for the model to compare. This is helpful for command recordings with different speakers, volumes, and microphone distances.

### Q: Why use Log-Mel instead of keeping a very large raw-audio dataset or raw waveform input?

Log-Mel is a good lightweight representation for this Raspberry Pi VCM because
it compresses the raw waveform into speech-relevant time-frequency structure
before the CNN sees it. A 4-second 16 kHz mono clip has `64,000` waveform
samples. With the current preprocessing, the same clip becomes a `398 x 40`
Log-Mel matrix, or `15,920` feature values. That is smaller and more structured
for a tiny CNN than feeding raw samples directly.

Large raw-audio collections, such as Common Voice, LibriSpeech, SLURP,
SpeechCommands, STOP, FLEURS, SNIPS, TimersAndSuch, MUSAN, and RIRS noise,
are useful for diversity: many speakers, accents, phrases, rooms, microphones,
and background conditions. They are a data strategy for generalization. They
are not automatically a better embedded architecture.

Our project target is different: a fixed-vocabulary, offline Raspberry Pi voice
command demo with wake gating, UNKNOWN rejection, command routing, and measured
latency/RAM/CPU/temperature. For that target, the defensible approach is:

```text
targeted Pi recordings + Log-Mel features + tiny CNN + confidence/wake guardrails
```

The large-dataset approach can help robustness if the labels and conditions
match the task, especially for non-Loreen speakers, noise, distance, and
unknown speech. However, mismatched public data cannot replace fresh Pi
recordings because final performance depends on the actual microphone, timing,
room, and command phrases used in the demo.

Exam answer:

```text
My classmates' 56 GB dataset is mostly raw-audio coverage. Our Log-Mel pipeline
is a lightweight feature-conversion choice for embedded inference. More data
can improve robustness, but the Pi demo also needs task-matched data. Log-Mel
helps the tiny CNN run quickly on the Raspberry Pi while still preserving the
speech patterns needed for command recognition.
```

### Q: Why must preprocessing be identical during training, validation, test, and Raspberry Pi inference?

The model learns from the exact feature format used during training. If validation, test, or Raspberry Pi inference uses different preprocessing, the model may receive inputs with different shapes, scaling, or frequency content. That makes results unreliable and can break real-world performance.

For this project, the same configuration in `configs/preprocessing.json` should control all stages: training, validation, test, and Raspberry Pi inference.

## Phase 3 - Baseline Model Preparation

### Q: What is the purpose of a smoke baseline?

A smoke baseline checks whether the training pipeline works end to end: dataset index reading, feature extraction, label encoding, model fitting, metric calculation, confusion matrix creation, and model saving.

It is not meant to be the final accuracy claim. In this project, the sklearn smoke baselines prove that Phase 2 features can feed a model and produce logged artifacts, but the measured accuracy is still too low for the final VCM.

### Q: Why is the current sklearn baseline not the final model?

The assignment expects a small on-device command recognizer, and the project direction is to use CNN-style learning over log-Mel features. The sklearn baseline uses a linear classifier, so it cannot learn local time-frequency patterns the same way a CNN can.

The best smoke baseline so far, `E03_SMOKE_RAW_BALANCED`, reached only 0.245 validation accuracy and 0.2446 macro-F1. That is useful diagnostic evidence, not a final result.

### Q: Why balance smoke sampling by raw label?

The active dataset has 20 raw command labels, but the assignment requires 10 final intent categories. Some final intents merge several raw labels. For example, `MEDIA_CONTROL` includes pause, stop, next, volume up, and volume down.

If a tiny smoke sample is balanced only by final intent, it may miss some raw command labels inside the merged category. Raw-label-balanced sampling makes the smoke experiment more representative while still scoring predictions against the 10 assignment intents.

### Q: What does macro-F1 mean, and why use it?

Macro-F1 calculates F1 separately for each class and then averages the class scores equally. This is useful when we care about every command intent, not just the largest or easiest category.

Accuracy can look acceptable while weak classes are ignored. Macro-F1 helps reveal whether performance is balanced across commands.

### Q: What does a confusion matrix show?

A confusion matrix shows which actual classes are being predicted as which other classes. Rows are actual labels and columns are predicted labels.

For command recognition, it helps identify confusing mistakes, such as a light command being predicted as a media command. It also helps decide whether the issue is data, label mapping, feature extraction, or model capacity.

### Q: What is the next model step after the smoke baseline?

The next technical step is a true CNN training path using the same `398 x 40` log-Mel inputs. The CNN should learn local time-frequency patterns instead of treating the spectrogram as only a flat vector.

Current local Python environments do not have PyTorch or TensorFlow installed, so the project must either enable a deep learning runtime or implement an alternative tiny CNN path before final model training.

### Q: Should we build more synthetic command data now?

Not yet. The project already has 21,000 included command WAV files, so the next evidence should come from CNN training and real microphone trials. If those results show low macro-F1, accent mismatch, noise sensitivity, or repeated intent confusion, then additional train-only data or augmentation can be added as a targeted experiment.

The known exception is UNKNOWN/rejection data. UNKNOWN is still missing and must be planned separately, but it should not be mixed silently into the main command dataset.

## Phase 4 - CNN Training Path

### Q: Why use a CNN for log-Mel features?

Log-Mel features are image-like: one axis is time and the other axis is Mel frequency. A CNN can learn small local patterns in this matrix, such as frequency bands and transitions that correspond to spoken words.

This is more appropriate than the sklearn smoke baseline because the CNN can learn local time-frequency structure instead of treating the spectrogram as only a flat vector.

### Q: Why keep the CNN small?

The final model must run on a Raspberry Pi without cloud services. A small CNN reduces memory use, CPU load, latency, and model size. This matters for real-time microphone inference and later TensorFlow Lite deployment.

### Q: Why has CNN accuracy not been reported yet?

The CNN code is scaffolded, but TensorFlow is not installed in the current local Python environments. Accuracy must not be claimed until the CNN training command is actually run and metrics are saved under `results/tables/`.

### Q: What is the intended CNN input?

The CNN input is the same Phase 2 feature output with a channel dimension added:

`398 x 40 x 1`

This means 398 time frames, 40 Mel bins, and 1 spectrogram channel.

### Q: Why can laptop voice trials help but not replace Raspberry Pi trials?

Laptop voice trials can test real speech capture, preprocessing, and model prediction before the Raspberry Pi is ready. They are useful for early debugging and for checking whether the model recognizes the user's voice.

They cannot replace Raspberry Pi trials because the assignment requires the final system to run on-device. Raspberry Pi validation must still measure the actual microphone, GPIO LED behavior, offline operation, latency, CPU/RAM, and deployment setup.

### Q: Why did we run an sklearn MLP if the target is a CNN?

The sklearn MLP was a fallback smoke experiment because TensorFlow was not available in the current local environment. It allowed us to test a nonlinear neural baseline on the same flattened log-Mel features and keep making measured progress.

It is not the final model. A CNN is still preferred because it can learn local time-frequency patterns from the `398 x 40 x 1` log-Mel input, while the MLP treats the spectrogram as a long flat vector.

### Q: Did the first CNN smoke solve the model?

No. TensorFlow was successfully installed and the CNN smoke experiments ran, but the current tiny CNN is underperforming. The best CNN smoke so far, `E06_CNN_SMOKE_NORM_20E`, reached only 0.1233 validation accuracy.

This means the environment and CNN training path now work, but the model design/training setup still needs diagnosis before final training or Raspberry Pi deployment.

### Q: Does low CNN accuracy mean we immediately need more data?

Not necessarily. The CNN did not fit the small training subset strongly either, so the first diagnosis should be model/training related: architecture capacity, feature normalization, training loop, learning rate, label mapping, or class confusion. More data should be added only after this diagnostic step identifies a data-related weakness.

### Q: What did the CNN diagnostics show?

The first CNN smoke did not just make random errors. It collapsed heavily toward one class. In `E06_CNN_SMOKE_NORM_20E`, 253 of 300 validation examples were predicted as `THERMOSTAT`, giving only 0.1233 accuracy and 0.0499 macro-F1.

This means we needed model/training diagnostics before adding data.

### Q: What is an overfit sanity test?

An overfit sanity test trains and evaluates on the same tiny subset. A neural network should usually be able to memorize a very small balanced dataset. If it cannot, the issue is likely in the model, training loop, preprocessing, or labels.

In this project, the intent-balanced overfit test showed the CNN could learn during training but failed during inference when default BatchNorm was used.

### Q: What did BatchNorm teach us here?

Default BatchNorm learned during training but failed at inference because the moving statistics were not suitable in this manual training setup. Fast BatchNorm fixed the overfit sanity test: `E11_CNN_OVERFIT_FASTBN` reached 0.8600 same-data accuracy and 0.8614 macro-F1.

So the next baseline should use `configs/cnn_fast_batchnorm.json`.

### Q: What happened after using fast BatchNorm for a real CNN smoke?

The corrected run `E12_CNN_FASTBN_INTENT_SMOKE` improved the CNN baseline. It reached 0.3533 validation accuracy and 0.3716 macro-F1 on an intent-balanced validation sample.

However, it is still not final. The diagnostic showed that the model still over-predicts `THERMOSTAT`, so the next task is model diagnosis and improvement, not Raspberry Pi deployment or more data yet.

### Q: Why did we run an overfit sanity test before trusting a new CNN architecture?

An overfit sanity test checks whether the model can memorize a very small balanced subset. If it cannot memorize 50 examples, then poor validation accuracy is probably caused by a model, training, preprocessing, or configuration problem rather than by insufficient dataset size.

For this project, the dense CNN with dropout reached only 0.5400 same-data accuracy in `E13_CNN_DENSE_OVERFIT`, so it was not trusted as the next baseline.

### Q: Why did removing dropout help the CNN sanity test?

Dropout intentionally removes some intermediate activations during training so the model does not rely too heavily on any one pathway. That is useful for reducing overfitting in larger training runs, but it can make a tiny memorization sanity test harder.

When dropout was disabled in `configs/cnn_fastbn_dense_nodropout.json`, `E14_CNN_DENSE_NODROPOUT_OVERFIT` reached 1.0000 same-data accuracy and 1.0000 macro-F1. This showed the CNN path could learn the log-Mel inputs.

### Q: What is the current best CNN smoke/baseline?

The current best real CNN smoke/baseline is `E21_CNN_DENSE_NODROPOUT_1000PI_BESTVAL`. It used `configs/cnn_fastbn_dense_nodropout.json`, up to 1,000 training examples per intent, and 30 validation examples per intent.

It reached 0.8267 validation accuracy and 0.8304 macro-F1 on an intent-balanced validation sample. This is better than `E20_CNN_DENSE_NODROPOUT_600PI_BESTVAL`, which reached 0.8133 validation accuracy and 0.8113 macro-F1.

### Q: Is the E19 CNN final?

No. `E21` is the current best smoke baseline, not the final model. It proves the CNN path is working better, but `MEDIA_CONTROL` still needs attention. In E21, `MEDIA_CONTROL` had 0.50 precision, 0.70 recall, and 0.58 F1.

The next step is to tune training stability and inspect per-class confusion before full training, laptop microphone trials, and Raspberry Pi deployment.

### Q: Why track the best validation epoch?

The model does not improve smoothly every epoch. Accuracy and macro-F1 can rise, dip, and recover as training continues. Saving only the final epoch may miss a better earlier checkpoint.

In `E16_CNN_DENSE_NODROPOUT_BESTVAL_SMOKE`, the best checkpoint was epoch 50. That checkpoint reached 0.5600 validation accuracy and 0.5434 macro-F1, slightly better than the final-epoch result from `E15`.

### Q: Did lowering the CNN learning rate improve the baseline?

No. `E17_CNN_DENSE_NODROPOUT_LR3E4_BESTVAL_SMOKE` lowered the Adam learning rate from 0.001 to 0.0003, but validation dropped to 0.3533 accuracy and 0.3594 macro-F1.

This is useful negative evidence. The model could still memorize training data, but it did not generalize better. Therefore, `E16` remained the best smoke baseline at that point, until the larger training subset in `E19` surpassed it.

### Q: Did mild dropout improve the CNN baseline?

No. `E18_CNN_DENSE_DROPOUT01_BESTVAL_SMOKE` used dropout 0.1 and dense dropout 0.1, but it reached only 0.4967 validation accuracy and 0.4667 macro-F1.

This means mild dropout did not help the current 1,000-example smoke setup. It slowed learning and did not beat the no-dropout E16 baseline.

### Q: Did a larger training subset improve the CNN baseline?

Yes. `E19_CNN_DENSE_NODROPOUT_300PI_BESTVAL` increased training from 100 examples per intent to 300 examples per intent while keeping the same validation sample.

It reached 0.7233 validation accuracy and 0.7198 macro-F1, making it the current best smoke baseline. This shows that using more of the existing dataset is more useful right now than adding dropout or generating new data.

### Q: What is the main weak class after E19?

The clearest weak intent after E19 is `MEDIA_CONTROL`. It had 0.37 recall and 0.45 F1 in the intent-balanced validation report.

This matters because `MEDIA_CONTROL` combines several raw command labels, such as pause, stop, next, volume up, and volume down. The model may need more examples, better label handling, or per-raw-label diagnostics for this merged class.

### Q: What did E20 show about scaling the existing dataset?

E20 increased training coverage to 600 examples per intent, or 6,000 total training examples. Validation improved to 0.8133 accuracy and 0.8113 macro-F1.

This shows that the existing dataset is still useful and should be scaled further before adding or generating new data.

### Q: How does confidence-threshold rejection help deployment?

A classifier always predicts one of the known classes, even for uncertain audio. A confidence threshold prevents the Raspberry Pi from executing an action when the model is unsure.

In E20, a threshold of 0.90 accepted 250 of 300 validation examples and raised accepted-command accuracy to 0.8800. A stricter threshold of 0.95 accepted 232 of 300 examples and raised accepted-command accuracy to 0.9181.

### Q: What did the E20 MEDIA_CONTROL breakdown show?

`MEDIA_CONTROL` improved but remained the weakest intent. The raw-label breakdown showed: `VOLUME_UP` 5/5 correct, `STOP` 4/7 correct, `NEXT` 4/9 correct, `VOLUME_DOWN` 2/5 correct, and `PAUSE` 2/4 correct.

This suggests that the merged `MEDIA_CONTROL` intent is internally diverse. More training coverage, per-raw-label diagnostics, or separate handling of media subcommands may be needed later.

### Q: What did E21 show after scaling closer to the full dataset?

E21 selected 9,520 training examples, using up to 1,000 examples per intent. It reached 0.8267 validation accuracy and 0.8304 macro-F1, making it the current best smoke baseline.

However, scaling introduced a tradeoff for `MEDIA_CONTROL`: recall improved, but precision dropped. This means E21 catches more real media commands, but also predicts `MEDIA_CONTROL` too often.

### Q: Why still use a confidence threshold with E21?

Even with better macro-F1, the model can still make confident-looking mistakes. A confidence threshold reduces false command execution.

For E21, a 0.90 threshold accepted 255 of 300 validation examples with accepted-command accuracy 0.8902. A 0.95 threshold accepted 241 of 300 examples with accepted-command accuracy 0.9046.

### Q: What is the laptop microphone trial status?

The project now has WAV-based local inference tooling in `demo/predict_wav.py`. It loads the E21 CNN model, applies the same preprocessing and normalization used during training, predicts the intent, and applies a confidence threshold before accepting a command.

Live microphone recording is not active yet because the current Python environment does not have `sounddevice` or `pyaudio`. Existing PCM WAV recordings can still be tested immediately.

### Q: What did the laptop WAV trials show?

The laptop WAV trials showed that good validation accuracy does not automatically mean the model is ready for real microphone control. The first controlled laptop batch was only 4/13 correct. The second controlled batch was 0/20 correct, and 13 wrong predictions were still accepted at a 0.90 confidence threshold. The third controlled batch was 1/21 correct, with 11 wrong predictions still accepted at the same threshold.

This means the project has a domain mismatch: the training/validation audio and the laptop-recorded audio behave differently enough that the CNN becomes confidently wrong. The correct response is not immediate broad data generation; it is targeted diagnosis of phrase consistency, microphone distance, silence/noise, and real microphone recording conditions.

### Q: What did the balanced 50-file laptop calibration set show?

The balanced calibration set had 5 laptop microphone recordings per intent. Assuming the files were recorded in the planned order, the model reached 17/50 correct, or 0.3400 accuracy.

The confidence threshold did not solve the problem. At threshold 0.90, the model accepted 34 predictions, but only 14 accepted predictions were correct. That means 20 accepted predictions were wrong.

The strongest laptop intent was `PLAY_MUSIC`, with 5/5 correct. `MEDIA_CONTROL` and `SET_ALARM` reached 3/5 correct. `LIGHT_CONTROL` and `LIGHT_ADJUST` were 0/5 correct, which is important because the physical LED demo depends on reliable light commands.

The conclusion is that the CNN path works in principle, but the current E21 model needs targeted microphone/domain adaptation before deployment.

### Q: What changed in the second 50-file laptop calibration set?

The second calibration set was much better: 42/50 correct, or 0.8400 accuracy. At threshold 0.90, 44 predictions were accepted, 39 accepted predictions were correct, and 5 accepted predictions were wrong.

This shows that real microphone performance depends strongly on recording consistency. The model is not simply unusable on laptop audio; it can work much better when commands are recorded more consistently.

The remaining critical weakness is `LIGHT_CONTROL`, which reached only 2/5 correct in Set 002. This matters because the Raspberry Pi LED demo depends most directly on light-control commands.

### Q: Why is threshold tuning not enough after Set 002?

Increasing the confidence threshold improves accepted-command accuracy overall, but two `LIGHT_CONTROL` recordings were still misclassified as `QUESTION` with confidence above 0.999. A stricter threshold would reject more correct commands while still failing on those two high-confidence errors.

This means the problem is not only uncertainty. The model can be confidently wrong for light commands, so the next step is targeted `LIGHT_CONTROL` improvement and real-microphone evaluation.

### Q: Is the Set 002 LED demo safety risk the same as overall classification error?

No. In Set 002, no non-light command was predicted as `LIGHT_CONTROL`. That means the observed risk is mainly missed or misrouted light commands, not accidental LED triggering from unrelated commands.

However, `LIGHT_CONTROL` was only 2/5 correct, so the LED demo may fail to respond reliably unless light-command robustness is improved.

### Q: Did the larger E22 training probe replace E21?

No. E22 used more training examples per intent than E21, but only for an 8-epoch probe. It reached 0.7700 validation accuracy and 0.7635 macro-F1, below E21's 0.8267 validation accuracy and 0.8304 macro-F1.

On Calibration Set 002, E22 reduced wrong accepted predictions from 5 to 2 at threshold 0.90, but it made `LIGHT_CONTROL` worse: 1/5 correct instead of E21's 2/5 correct. Since the LED demo depends on light commands, E22 should not replace E21.

### Q: Are the downloaded class LIGHT_ON/LIGHT_OFF folders useful?

Yes, but they answer a different question from the laptop/Pi microphone problem. The folders contain 747 compatible WAV files: 360 `LIGHT_ON` and 387 `LIGHT_OFF`. They are 16 kHz mono PCM WAV files, so they fit the preprocessing pipeline.

The current E21 model already performs well on them: 662/747 correct, or 0.8862 accuracy. This means they are useful as supplemental light-command data or external light-command evidence.

However, they do not replace real microphone trials. The deployment issue is that the laptop/Pi microphone audio can differ from the dataset-style audio. Therefore, more real-microphone `LIGHT_CONTROL` recordings are still useful.

### Q: What did the 25-recording real-mic light set show?

The 25 fresh recordings were all the phrase "turn on the light." E21 predicted only 10/25 correctly. At the 0.90 confidence threshold, it accepted 12 predictions, but only 8 accepted predictions were correct.

This confirms the key deployment issue: the model can handle many dataset-style `LIGHT_ON` and `LIGHT_OFF` files, but still struggles with real-microphone light commands. The next improvement should target the real-microphone light-command domain.

### Q: What did the matching "turn off the light" real-mic set show?

The 25 "turn off the light" recordings were harder than the "turn on" recordings. E21 predicted only 4/25 correctly. At threshold 0.90, it accepted 11 predictions, but only 1 accepted prediction was correct.

Combining the 25 "turn on" and 25 "turn off" recordings gives 14/50 correct overall. This is strong evidence that reliable LED control needs targeted real-microphone adaptation before deployment.

### Q: What did targeted real-microphone adaptation achieve?

The E23 experiment fine-tuned E21 using 30 real-microphone light-command clips and kept 20 real-microphone light clips held out for evaluation. It also used original-dataset replay examples to reduce forgetting.

On the held-out real-mic light clips, E21 was only 4/20 correct and had 4 wrong accepted predictions at threshold 0.90. E23 improved to 16/20 correct and had 0 wrong accepted predictions at the same threshold.

The tradeoff is that E23's official validation macro-F1 dropped to 0.7912, while E21's macro-F1 was 0.8304. Therefore, E21 remains the best general validation baseline, while E23 is the current light-command deployment candidate.

## Phase 5 - Raspberry Pi Deployment And Voice Trials

### Q: What is the Raspberry Pi deployment sequence?

The sequence is: prepare the boot media, boot and configure the Pi, install dependencies in a virtual environment, verify the USB microphone, verify GPIO LED wiring independently, copy the trained model and runtime code, run WAV prediction tests, run live microphone inference, connect predictions to LED behavior, then repeat the demo offline.

### Q: Why test the microphone and LED separately before the full demo?

Separate tests isolate failure points. If the microphone cannot record clean 16 kHz mono audio, model predictions will be unreliable. If the LED cannot blink from a simple GPIO script, a voice-control demo failure might be a wiring or GPIO issue rather than a model issue.

### Q: Why must final Raspberry Pi validation be offline?

The assignment requires standalone operation and forbids cloud/LLM/ASR dependence for final inference. Offline validation proves the device is using the local model and local preprocessing pipeline rather than an internet service.

### Q: Why was the Pi deployment package prepared before the hardware arrived?

Preparing the package early separates software readiness from hardware debugging. The folder `deployment/vcm_pi_package/` already contains the selected model artifacts, preprocessing code, CNN architecture code, Pi inference scripts, GPIO test script, setup guide, validation protocol, and readiness report.

This means that when the Raspberry Pi 5 arrives, the next task is not to redesign the model. The next task is to copy the package to the Pi and measure whether the Pi microphone produces reliable predictions.

### Q: Why is GPIO disabled by default in the Pi package?

GPIO is disabled by default because the Raspberry Pi microphone has not yet been validated. Laptop trials showed that the microphone domain can strongly affect prediction behavior, so it would be unsafe to let predictions immediately control the LED.

The package first supports prediction-only validation. GPIO can be enabled later with `--enable-gpio` after the Pi microphone tests show acceptable behavior.

### Q: Can the current model turn the LED on and off autonomously?

The current package default is now closer to that goal because E24 predicts raw
command labels, not only broad intents. It can distinguish `LIGHT_ON` from
`LIGHT_OFF`, then `actions/raw_command_router.py` maps those labels into
`LIGHT_CONTROL` with the correct `light_action` slot.

The safety caveat is important: GPIO should still be enabled only after the
route being demonstrated is validated on held-out Pi recordings. At threshold
`0.95`, E24 had 0 wrong accepted commands on the measured 95-clip Pi holdout
set, but it accepted only 69/95 clips. So the direction is correct, but the
next target is higher coverage without wrong accepted actions.

### Q: How are voice-command actions represented in the project?

The project now has an action layer in `actions/command_actions.py`. The CNN output is treated as an intent, and the action layer decides what local behavior to execute or simulate.

This keeps the design clean: model recognition is one part, command execution is another part. For example, `SET_TIMER` creates a local timer entry, `REMINDER` stores a local reminder, and `LIGHT_CONTROL` can control GPIO only if an on/off/toggle/blink slot is supplied.

### Q: Why are some actions only simulated?

Some requested commands require external services or unavailable devices. Search would normally require internet access, calls/messages require phone or messaging integration, thermostat control requires a real thermostat, and media control requires a real local media player. Since the assignment emphasizes standalone/offline inference, these are logged or simulated unless a local device/service is explicitly added.

### Q: Can the action routes be pre-coded before the hardware arrives?

Yes. The project can already pre-code the deterministic router from intent to action. This means `PLAY_MUSIC`, `QUESTION`, `LIGHT_CONTROL`, `LIGHT_ADJUST`, `SET_TIMER`, `SET_ALARM`, `THERMOSTAT`, `MEDIA_CONTROL`, `REMINDER`, and `CALL_MESSAGE` each have a local handler.

What is pre-coded now is the logic: local time/weather answer, LED
on/off/brightness state, timer/alarm entries, simulated thermostat fan state,
media state, reminder storage, and simulated call/message display. The Pi
microphone and local inference path have been tested; physical output still
needs hardware verification for GPIO LED/display/speaker behavior.

The professor-facing explanation is: the tiny CNN performs intent classification, then a deterministic local command router executes the action. This keeps the project offline and avoids turning the VCM into a full ASR or LLM assistant.

### Q: Is the Raspberry Pi demo exam-ready for every command now?

Not fully. The Raspberry Pi setup, microphone, preprocessing, TensorFlow
inference, and raw-command routing path are working. The current E24 package
default reached 86/95 correct raw-command predictions on the held-out Pi
calibration set. At threshold `0.95`, it accepted 69/95 commands and had 0
wrong accepted commands.

That is a safer checkpoint than the earlier broad-intent sweep, but it is not
the 100/100 target yet because too many commands are rejected at the safe
threshold.

### Q: What is the next step to make every command recognizable?

The next step is E26-style targeted improvement, not restarting from scratch.
The full Pi calibration set has already been recorded and split into adaptation
and holdout clips. E24 used that data to move the package to raw-command
recognition. Now the goal is to improve accepted coverage for the remaining
weak labels, especially `LIGHT_OFF`, `STOP`, `COLOR`, `ALARM`, and
`CREATE_REMINDER`, while preserving zero or near-zero wrong accepted actions.

### Q: Why might the model need raw command labels instead of only broad intents?

Broad intents are enough for classification reporting, but they are not always
enough for action execution. For example, `MEDIA_CONTROL` contains pause, stop,
next, volume up, and volume down. `LIGHT_CONTROL` contains light on and light
off. A full demo needs the system to choose the specific local action, so the
next model or output layer should recognize raw command/subcommand labels and
then map them to the required assignment intent plus action.

### Q: What changed with E24?

E24 is the first Pi package default that predicts 19 raw command labels. The
pipeline is now:

```text
live Pi microphone recording -> log-Mel features -> E24 raw-command CNN
-> raw-command router -> broad assignment intent + slot -> local action layer
```

This keeps the system offline and still avoids ASR/LLMs. It simply makes the
classifier output more useful for actions. For example, instead of outputting
only `MEDIA_CONTROL`, the model can output `NEXT`, `PAUSE`, `STOP`,
`VOLUME_UP`, or `VOLUME_DOWN`, and the router maps that to the correct media
action.

### Q: Why use a per-command threshold guardrail?

A single confidence threshold is simple but blunt. In E24, some labels were safe
at lower confidence, while a few labels needed stricter protection because they
appeared as false positives. For example, one risky error was
`LIGHT_OFF -> LIGHT_ON`, so the optional guardrail policy keeps predicted
`LIGHT_ON` at a high threshold. Another risky pair was `STOP -> NEXT`, so
predicted `NEXT` also keeps a stricter threshold.

The optional policy `configs/e24_pi_guardrail_thresholds.json` accepted 80/95
saved E24 Pi holdout clips with 0 wrong accepted commands. The strict global
`0.95` threshold accepted only 69/95 with 0 wrong accepted commands.

The honest caveat is that this policy was calibrated from existing holdout
evidence. It is useful as a candidate demo guardrail, but it still needs fresh
Pi microphone validation before being claimed as final exam-ready performance.

### Q: What changed with E26?

E26 is the fresh Pi recovery model created after E24 failed the preserved live
`NEXT` and `COLOR` mini-set. It keeps the same offline CNN pipeline and the
same raw-command output design, but fine-tunes from E24 using source replay, Pi
adaptation replay, and the preserved fresh Pi examples for `STOP`, `NEXT`, and
`COLOR`.

The updated pipeline is:

```text
live Pi microphone recording -> log-Mel features -> E26 raw-command CNN
-> E26 per-label guardrail -> raw-command router -> local action layer
```

E26 reached `87/95` raw correct on the original Pi holdout. With
`configs/e26_pi_guardrail_thresholds.json`, it accepted `74/95` original Pi
holdout clips with `0` wrong accepted commands. On the preserved fresh Pi
mini-set, it accepted `9/9` correctly for `STOP`, `NEXT`, and `COLOR`.

The important demo explanation is that E26 is a recovery checkpoint, not final
proof. It fixes the exact preserved failure pattern, but because those fresh
clips were used for recovery training, the next proof must be a new live Pi
validation set. GPIO should remain disabled until that new pass has no wrong
accepted commands.

### Q: What changed with E27?

E27 was created after E26 still failed new live Pi clips for `NEXT` and
`COLOR`. Those six copied clips became recovery evidence: three `NEXT` clips
and three `COLOR` clips. E27 fine-tunes from E26 using source replay, Pi
adaptation replay, the earlier preserved fresh mini-set, and the latest copied
live failure clips.

E27 reached `85/95` raw correct on the original Pi holdout. With
`configs/e27_pi_guardrail_thresholds.json`, it accepted `74/95` original Pi
holdout clips with `0` wrong accepted commands. On the combined 15-clip recovery
set, it accepted `15/15` correctly for `STOP`, `NEXT`, and `COLOR`.

The explanation for demo or defense is: each recovery cycle uses real Pi
microphone errors as calibration evidence, but the final claim must always come
from a fresh validation pass that was not used for training. Therefore E27 is
the next candidate to test on the Pi, not final proof yet.

### Q: What changed with E28?

E28 was created after E27 was safe but not responsive enough on a fresh live Pi
validation pass. E27 had `0` wrong accepted commands, but accepted only `3/6`
new `NEXT`/`COLOR` clips. E28 adds those six clips to the recovery set and
fine-tunes from E27.

E28 reached `82/95` raw correct on the original Pi holdout. With
`configs/e28_pi_guardrail_thresholds.json`, it accepted `74/95` original Pi
holdout clips with `0` wrong accepted commands. On the combined 21-clip recovery
set, it accepted `21/21` correctly for `STOP`, `NEXT`, and `COLOR`.

The honest explanation is that E28 is more responsive on the recovered clips
but has lower raw holdout accuracy than E27. It is the next candidate to test
live, while GPIO remains disabled.

### Q: Does E28 copy/test require recording?

Copying and installing the E28 package does not require recording. File checks,
script checks, and prediction on existing WAV files can be done even when the
room is noisy.

Fresh E28 live validation does require recording through the Pi microphone. If
it is raining or there is strong ambient noise, those recordings should not be
treated as clean exam-readiness evidence. They could be kept as noisy-condition
stress tests, but the main validation should wait for a quieter room.

### Q: Can the metal Pi case affect Wi-Fi and Bluetooth?

Yes. A metal enclosure can weaken the Raspberry Pi 5's onboard Wi-Fi and
Bluetooth because it can shield or detune the antenna path. This affects setup
tasks such as SSH, file transfer, Bluetooth keyboard/mouse, and pairing. It
does not change the offline CNN model once files are installed. Practical
workarounds are Ethernet, wired USB keyboard/mouse, closer range, case
orientation, or opening the case during setup.

### Q: What does it mean that the dataset should not be "hacky"?

It means the project should not look like it was made by repeatedly recording a
failed phrase, training on that exact phrase, and then claiming success on the
same audio. That kind of loop is useful for debugging, but it is not final
validation.

Our defensible explanation is:

```text
We used recovery experiments to identify and fix Pi microphone weaknesses, but
we keep final validation separate. The final claim comes from fresh or held-out
Pi microphone recordings that were not used for training the model being
reported.
```

The clean structure is:

- adaptation/training data: used to tune the model;
- held-out/fresh validation data: used only for reporting performance;
- robustness tests: ambient noise, speaker distance, and not-Loreen voice,
  reported separately as stress conditions.

Synthetic recordings and classmates' posted datasets can be cited or used
selectively, but the core evidence should be real Pi microphone recordings
because the demo runs on the Pi with a live microphone.

### Q: Are Pi recordings training data, validation data, or deployment evidence?

They can be any of those roles depending on the split. In this project, Pi
recordings are deliberately separated into:

```text
Pi adaptation clips = training/fine-tuning data
Pi holdout clips = validation/test evidence
fresh live Pi trials = final deployment evidence
```

The adaptation clips teach the model the real microphone, room acoustics,
speaker timing, and command phrasing used by the deployment device. The holdout
clips answer whether the model learned those conditions well enough to work on
Pi recordings it did not train on. Fresh live trials are the strongest final
evidence because they test the actual demo path end to end.

This is conceptually similar to classmates augmenting a base dataset with their
own voice recordings, synthesized speech, or noise. The method is legitimate
when it is documented and controlled:

- state where the added data came from;
- label it honestly;
- separate training/adaptation clips from validation/test clips;
- do not report performance on the same clips used for training;
- do not claim robustness beyond what was actually tested.

Exam answer:

```text
Yes, some Pi recordings are training data. We use them as deployment-domain
adaptation data because the final model must work with the Pi microphone and
room. The non-hacky part is that we keep separate Pi holdout and fresh live
validation clips, so we are not training and testing on the exact same audio.
This is similar in principle to adding self-recorded or synthetic data, but our
purpose is specifically to adapt and validate the real Raspberry Pi deployment
environment.
```

### Q: How should we explain E26, E27, and E28 without sounding hacky?

Say that E26/E27/E28 are documented recovery candidates, not final proof. They
showed us which commands were weak under the real Pi microphone, especially
`NEXT` and `COLOR`, and helped produce a safer candidate package. The final
exam claim still requires tomorrow's fresh validation set.

Good wording:

```text
E28 is our current deployment candidate. It was produced after analyzing
specific Pi microphone failures, but we will not report the recovery clips as
independent accuracy. We will report fresh validation separately.
```

### Q: Why do classmates' ambient-noise, distance, and not-Loreen speaker tests matter?

They test robustness. Our main validation should first show the normal demo
condition works: same Pi, same mic, normal distance, quiet room. Then the
robustness tests can show what happens when conditions change.

The honest reporting style is:

```text
Clean condition: measures whether the trained demo works.
Noise/distance/other-speaker condition: measures robustness beyond the clean
demo setup.
```

### Q: What does a defensible 100/100 claim require?

It requires more than one successful live demo run. It requires a clean,
repeatable evaluation path:

- the pipeline is fixed: live audio, log-Mel preprocessing, CNN, guardrail,
  raw-command router, action handler;
- the final validation audio was not used to train the reported candidate;
- every tested command maps to the correct raw label and the correct
  intent/action;
- wrong accepted commands are zero;
- rejections are counted honestly;
- robustness tests for noise, distance, and another speaker are reported
  separately.

Good wording:

```text
Our 100/100 goal is not just accuracy. It is correct command recognition,
correct intent routing, safe rejection of uncertain commands, and offline
Raspberry Pi operation. We separate clean validation from robustness tests so
the benchmark is defensible.
```

### Q: How do we report `hey pi -> hey pi`?

Report it as a repeated-wake safety test, not as a command test.

Good wording:

```text
The first "hey pi" opened the command window. When "hey pi" was spoken again
instead of a supported command, the system took no action. This is the desired
safety behavior because WAKE is a gate, not an executable command.
```

Do not count this as `COLOR` evidence, even if a command-stage classifier
temporarily assigns a low-confidence `COLOR` label. The spoken phrase was the
wake phrase, so the correct interpretation is safe rejection/no-action after
repeated wake input.

### Q: Was our workflow legitimate, or was it hacky?

The workflow is legitimate as long as we describe the data roles honestly. The
project did not rely on the wake gate as a substitute for command recognition.
The command recognizer was first trained from the available command data, then
tested on the actual Raspberry Pi deployment setup. When the Pi microphone,
room, timing, and speaker conditions caused failures, selected Pi recordings
were used as target-device adaptation data. Separate held-out clips and fresh
live trials were then used as evaluation evidence.

Good wording:

```text
The command recognizer was trained on the available command datasets. Pi
recordings were initially used as deployment validation to measure the mismatch
between the dataset audio and the real Raspberry Pi microphone/room conditions.
After specific failures were identified, selected Pi clips were used as
deployment-domain adaptation data, while separate held-out Pi clips and fresh
live wake-gated trials were used for evaluation. The wake gate was added as a
deployment safety layer, not as a replacement for command training.
```

This is similar in principle to classmates adding their own recorded or
synthetic speech as augmentation. The defensible part is the split: clips used
for adaptation are not reported as independent final proof.

### Q: What exact workflow did we follow?

1. Trained base command recognizers from the available command datasets.
2. Recorded Raspberry Pi validation clips on the actual deployment microphone.
3. Tested the base models on Pi audio and identified deployment mismatch.
4. Inspected wrong predictions, confidence values, and weak labels.
5. Added selected Pi recordings as target-device adaptation/recovery data.
6. Kept held-out Pi clips and fresh live trials for evaluation evidence.
7. Added the `hey pi` wake gate as a two-stage deployment flow.
8. Added confidence guardrails to prevent uncertain or wrong actions.
9. Ran wake-gated live tests and classified each as pass, safe rejection, or
   wrong executed action.
10. Connected a real `play music` action through USB headset audio playback.

Current strongest live evidence:

```text
hey pi -> play music
Wake accepted, PLAY_MUSIC recognized, routed to media.play_music, and produced
audible USB headset playback.
```

Current working non-LED commands from live tests:

```text
PLAY_MUSIC, PAUSE, VOLUME_DOWN, TIME, TEMPERATURE, WEATHER, ALARM,
LIST_REMINDERS
```

Commands still marked for recovery or fresh validation:

```text
VOLUME_UP, STOP, NEXT, TIMER, CALL, MESSAGE, CREATE_REMINDER
```

LED/light/color/brightness controls are postponed until board setup and focused
recovery.

### Documentation Integrity Rule

Use the project logs and saved evidence as the source of truth for the machine exercise report. Do not pad results, convert safe rejections into successes, or claim final 100/100 fulfillment until a final fresh validation run supports it.

Report categories separately:

```text
Clean pass: correct wake, correct command, correct routed action.
Safe rejection: no wrong action, but not a successful command execution.
Wrong executed action: incorrect command/action accepted and executed.
Pending: not yet validated or deferred due to hardware setup.
```

The report should correspond to the actual logs:

```text
AGENT_LOG.md
EXPERIMENT_LOG.md
PROJECT_STATUS.md
REQUIREMENTS_TRACEABILITY.md
results/wake_gated_live_20260923/
results/tables/
```

If later experiments improve the model, add them as new evidence instead of rewriting earlier failures.

### Final E40 Validation Wording

Use this wording for the machine exercise report:

```text
After E40 recovery training, fresh wake-gated live validation was performed on
the Raspberry Pi. The system cleanly executed 10 non-LED commands: play music,
pause, stop, timer, time, weather, temperature, volume down, create reminder,
and list reminders. The wake gate also rejected non-target wake phrases and
bare commands spoken without "hey pi", so no action was taken in those safety
tests.

Several commands were not claimed as final passes under E40: volume up, next,
alarm, call, and message. These produced safe rejections rather than wrong
executed actions. LED/light/color/brightness controls remain deferred until
the board setup is available. Therefore E40 is reported as a strong partial
final validation and recovery candidate, not as a 100/100 all-command result.
```

Important honesty note:

```text
Safe rejection is good safety behavior, but it is not counted as a successful
command execution. The report separates clean passes, safe rejections, invalid
trials, and deferred hardware-dependent controls.
```

### E41 Recovery Explanation

If asked why E41 was needed:

```text
E40 showed that the non-LED pipeline was functional for a strong subset of
commands, but command recognition was still not robust enough for all listed
commands under clean Raspberry Pi live conditions. The failures were not mainly
routing or action-execution failures. They were recognition-confidence and
misclassification failures for volume up, next, alarm, call, and message.

Therefore E41 was defined as a focused recognition recovery experiment. Its
purpose is to improve those weak labels while preserving the commands that E40
already validated. This is normal model recovery/adaptation, not threshold
magic and not a rewrite of earlier results.
```

Architecture wording:

```text
The implemented pipeline is audio capture, wake CNN, wake gate, fixed command
recording, log-Mel preprocessing, command CNN, confidence guardrail,
deterministic intent routing, action execution, and evidence logging. The
validated runner currently handles one wake-command interaction per run. A
continuous loop is still a product/demo improvement.
```

## Phase C Baseline and E43 Recovery - Oral Exam Notes

### Q: What was Phase C?

Phase C was a fresh all-command baseline validation using a frozen stack:

```text
Wake model: E37_TARGETED_COLOR_VOLUME_FIX
Command model: E41_FUNCTIONAL_NON_LED_RECOVERY
Threshold policy: E40_NON_LED_COMMAND_GUARDRAIL_THRESHOLDS
```

The purpose was diagnosis, not improvement. No model, preprocessing, threshold,
router, parser, or action logic was changed during Phase C.

Evidence:

```text
outputs/pi_evidence_pullback_20260925_214022/
27 Phase C result JSON files
614 extracted files
615 SHA256 manifest rows
0 missing files
0 hash mismatches
```

### Q: What did Phase C show?

Phase C covered all 19 positive raw labels and no-action probes.

```text
Positive raw labels covered: 19/19
Full PASS: 10
PARTIAL PASS: 2
FAIL: 7
Valid no-action probes: 6
PASS-SAFE no-action probes: 6
Invalid/procedure trial excluded: 1
```

This means the system is real and measurable, but not yet complete. It can run
the wake-gated VCM pipeline on the Raspberry Pi, but several command categories
still need recovery or non-model repair.

### Q: Why did we separate failures by layer?

Because not every failed trial means the neural model is wrong. A full command
can fail at several layers:

```text
audio capture -> wake gate -> preprocessing/features -> VCM classification ->
confidence/rejection -> label mapping -> parameter parsing -> routing ->
action execution -> response/output
```

Phase C failure-layer counts for the 9 non-full-pass command trials:

```text
VCM classification: 3
confidence/rejection: 4
response/output: 2
parser/routing/action-execution bugs proven: 0
```

Exam answer:

```text
I separated the failure layers so I would not retrain the model for a problem
that belonged to thresholding or output playback. This made the next experiment
more controlled and scientifically defensible.
```

### Q: What was the highest-risk Phase C failure?

The highest-risk failure was:

```text
Trial: phase_c_create_reminder_20260925_001
Expected: CREATE_REMINDER
Predicted: LIST_REMINDERS
Confidence: 0.9953140020370483
Result: accepted and executed reminder.list
```

This is worse than a safe rejection because the system executed the wrong local
action. It is the first E43 recovery priority.

### Q: Why not just lower thresholds?

Some commands were predicted correctly but rejected:

```text
PLAY_MUSIC: 0.8174716830253601 vs threshold 0.90
BRIGHTNESS: 0.7676613330841064 vs threshold 0.90
PAUSE: 0.9832791090011597 vs threshold 0.99
VOLUME_DOWN: 0.835065484046936 vs threshold 0.90
```

Lowering thresholds might make these commands pass, but it could also increase
wrong accepted actions. The project already observed one wrong accepted action
for `CREATE_REMINDER`, so threshold changes must be treated carefully.

Exam answer:

```text
I did not lower the global threshold just to make the demo pass. I first
identified which commands were correct-but-low-confidence and which were wrong
classifications. Threshold calibration should be a separate decision after
false-accept risk is measured.
```

### Q: Why are LIGHT_OFF and NEXT not E43 model-training targets?

For `LIGHT_OFF` and `NEXT`, the VCM and router path worked, but the audio/output
evidence was static or uncertain.

Evidence:

```text
LIGHT_OFF: predicted LIGHT_OFF, routed to light.off, hardware_applied false,
           output uncertain/static
NEXT: predicted NEXT, routed to media.next, hardware_applied true,
      output uncertain/static
```

Exam answer:

```text
I did not treat these as model failures because the classifier and router were
already correct. The next step is output/action-path repair or retesting, not
retraining the command model.
```

### Q: What is E43?

E43 is a proposed targeted recovery experiment, not broad retraining.

Initial fixed variables:

```text
Architecture: configs/cnn_fastbn_dense_nodropout_raw19.json
Preprocessing: configs/preprocessing.json
Threshold policy: E40_NON_LED_COMMAND_GUARDRAIL_THRESHOLDS
Wake model: E37_TARGETED_COLOR_VOLUME_FIX
Router/action layer: unchanged
```

Proposed E43 command-model targets:

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
```

Separate non-model work:

```text
- LIGHT_OFF output/action path
- NEXT output/action path
```

Separate wake work:

```text
- silence
- false wake phrases
- wake variability
```

### Q: What makes E43 disciplined rather than hacky?

E43 changes only the targeted recovery data and resulting model artifacts first.
It keeps the architecture, preprocessing, thresholds, wake model, router, and
action layer fixed. That makes the effect of the intervention easier to explain.

Most important rule:

```text
Recovery recordings are not final validation recordings.
```

Exam answer:

```text
E43 is based on Phase C evidence. I am not changing multiple independent
variables at once. I am preserving the Phase C baseline, adding targeted
recovery data for specific confusion pairs, and requiring fresh validation
after training before claiming improvement.
```

### Q: What should I say if asked whether the project is complete?

Use careful wording:

```text
The system is implemented and deployed enough to produce real Raspberry Pi
evidence. Phase C validated the full command scope and no-action probes under a
frozen stack, but it also exposed remaining failures. Therefore the project is
not yet 100/100 complete. The next step is E43 targeted recovery and separate
output/wake robustness work.
```

Do not say:

```text
All commands work.
The five-command demo proves completion.
Safe rejection is the same as successful execution.
```

### Q: What is the main engineering lesson from Phase C?

The main lesson is controlled diagnosis.

```text
Freeze the stack, run fresh validation, classify failures by layer, then choose
the smallest justified intervention.
```

This is the project’s strongest methodology point: failures were preserved,
measured, and used to guide the next experiment instead of being hidden.

### Q: What did the LIGHT_OFF / NEXT output retest show?

Direct playback of the response WAV files worked:

```text
pi_responses/light_off.wav: clear
pi_responses/next.wav: clear
```

This means the static/uncertain Phase C output was not caused by corrupted WAV files or the HDMI/LCD audio device itself.

Exam answer:

```text
I separated the output problem from the VCM model. Since direct WAV playback worked, I should not retrain the model for LIGHT_OFF or NEXT. The next diagnostic step is to test the action-layer invocation path.
```

### Q: What was the LIGHT_OFF fix?

`LIGHT_OFF` was not a model failure. Phase C showed the model predicted `LIGHT_OFF` correctly and routed to `light.off`, but the response was missing/static. Direct playback of `light_off.wav` was clear, so the WAV file and speaker path worked.

The actual issue was that `light.off` was missing from the response-audio mapping. After adding:

```text
light.off -> light_off.wav
```

the action-layer retest returned `hardware_applied: true`, and the response was heard clearly.

Exam answer:

```text
I did not retrain for LIGHT_OFF because the classifier was already correct. I diagnosed the output layer and found a missing action-to-WAV mapping. This is an example of separating VCM errors from software integration errors.
```

### Q: What did the NEXT retest prove?

The `NEXT` command was retested through the action layer. It returned `media.next`, `hardware_applied: true`, and the playback was clear.

Exam answer:

```text
NEXT should not be treated as a model-retraining target based on current evidence. The Phase C retry showed correct VCM classification, and the action-layer retest showed clear output. I keep it in regression testing, but I do not spend E43 recovery data on it unless fresh validation regresses.
```

### Q: Why were LIGHT_OFF and NEXT removed from E43 model-retraining targets?

Because their strongest evidence points to output/action integration, not model learning.

`LIGHT_OFF` had correct Phase C classification and routing. The later repair added the missing `light.off -> light_off.wav` response mapping, and the action-layer retest returned `hardware_applied: true`.

`NEXT` had correct Phase C classification/routing on retry, and the action-layer retest returned `media.next`, `hardware_applied: true`, with clear playback.

Exam answer:

```text
I removed LIGHT_OFF and NEXT from E43 model-retraining scope because retraining would not address the proven failure layer. They remain in regression validation, but E43 recovery data should focus on the actual model/confidence failures: CREATE_REMINDER vs LIST_REMINDERS, LIGHT_ON, COLOR, PLAY_MUSIC, BRIGHTNESS, PAUSE, and VOLUME_DOWN.
```

### Q: Why does E43 start with recovery data collection instead of training?

Because Phase C identified specific failure layers and target phrases. Training
without collecting the correct recovery data would be uncontrolled.

The most important example is `CREATE_REMINDER`: Phase C failed on the phrase
"create reminder". An older helper used a different phrase, "reminder drink
water", so E43 must explicitly record the failed phrase.

Exam answer:

```text
E43 starts by collecting targeted recovery clips because the intervention has to match the observed failure. I keep these clips separate from final validation, then train and evaluate against fresh independent recordings later.
```

### Q: Why inspect the manifest if the WAV files are valid?

The WAV files prove audio capture worked, but the manifest is the label source
of truth for training. If the manifest has an extra or malformed row, training
could read the wrong label/path metadata even though the audio files themselves
are good.

Exam answer:

```text
I check both audio format and manifest integrity. The model learns from labelled examples, so correct metadata is as important as valid WAV files.
```

### Q: What did the first two E43 collection blocks accomplish?

They captured recovery data for the highest-priority Phase C class-separation
failures:

```text
CREATE_REMINDER vs LIST_REMINDERS
LIGHT_ON
COLOR
```

Each target now has 10 valid Pi microphone recovery clips. These are not final
validation clips; they are candidate recovery/training data.

Exam answer:

```text
The first E43 data blocks target the actual Phase C confusion evidence. I verified file counts, manifest rows, sample rate, channels, sample width, and duration before allowing the data into the recovery pipeline.
```

### Q: What is the difference between a classification failure and a confidence/rejection failure?

A classification failure means the model predicted the wrong raw label, such as
`COLOR` being predicted as `PAUSE`.

A confidence/rejection failure means the top label was correct, but the score
did not clear the frozen threshold, such as `PAUSE` predicted as `PAUSE` but
rejected below the per-label threshold.

Exam answer:

```text
I separated wrong-label errors from below-threshold correct-label errors. That matters because the first suggests class-boundary recovery, while the second may be solved by better examples or later threshold calibration, but should not be hidden by simply lowering thresholds.
```

### Q: What evidence shows E43 recovery collection was clean?

The Pi-side verification showed:

```text
95 WAV files
96 manifest lines including header
bad_files 0
```

The labels also matched the intended design: 10 clips each for main recovery
targets and 5 clips each for contrast/regression targets.

Exam answer:

```text
Before training, I verified the recovery dataset structurally: file counts, manifest counts, label distribution, sample rate, channel count, sample width, and duration. This supports reproducibility and prevents bad metadata from contaminating the experiment.
```

### Q: Why hash the E43 recovery pullback?

Hashing creates a reproducible evidence record. If the files are moved,
copied, or used for training later, the SHA256 manifest can prove which exact
audio files were used.

Exam answer:

```text
I pulled the Pi recovery dataset back to Windows and created a SHA256 manifest so the experiment can be traced to exact files. This prevents silent data drift and supports reproducibility.
```

### Q: What does the E43 training-readiness audit prove?

It proves that the recovery dataset is structurally usable before training:

```text
95 manifest rows
95 WAV files
0 missing targets
0 extra WAVs
0 duplicate manifest paths
normalized SHA manifest verified
```

It does not prove that the model improved. Improvement can only be claimed
after training and fresh validation against independent recordings.

Exam answer:

```text
The readiness audit proves the recovery data is consistent and traceable. It is a gate before training, not a model result.
```

### Q: Why create a derived E43 training manifest?

The source E43 manifest marks the recordings as `recovery`, which preserves
their true role. The existing training script expects rows marked as
`adaptation` or `holdout`. A derived manifest lets the trainer use the clips as
adaptation data without rewriting the original evidence manifest.

Exam answer:

```text
I preserved the original evidence manifest and created a derived training manifest. That keeps the audit trail honest while making the data compatible with the existing training pipeline.
```

### Q: Why run an E43 smoke training experiment?

The first full E43 run was computationally expensive and produced no visible intermediate evidence before interruption. A smoke run checks that the training pipeline can complete and write artifacts before spending time on the full configuration.

Exam answer:

```text
The smoke run is not a final model. It is an engineering check that the manifests, base model, preprocessing, and artifact-writing path work before I run the expensive training configuration.
```

### Q: What did the E43 smoke training run prove?

It proved the training pipeline can complete with the staged E41 base model and the derived E43 adaptation manifest. It did not prove model improvement.

The smoke model had 7 wrong accepted predictions at threshold 0.90, so it should not be promoted.

Exam answer:

```text
The smoke run was a pipeline validation, not a final model. It completed and wrote artifacts, but its holdout behavior was worse than needed, so I preserved it as evidence and did not promote it.
```

### Q: Why was the E43 smoke model rejected?

It improved some target labels, but it increased wrong accepted predictions from 4 to 7 on the Pi holdout set. A wrong accepted command is more serious than a safe rejection because it can trigger the wrong action.

Exam answer:

```text
I rejected the smoke model because the goal is not just higher accuracy on target labels. The system must avoid wrong accepted actions. The smoke run over-adapted and damaged guardrail behavior, so it became evidence for the next safer training configuration rather than a promoted model.
```

### Q: Why preserve E41 normalization in the next E43 candidate?

The smoke run proved the training pipeline worked, but it regressed guardrail behavior. One risk was changing too much at once, including the feature normalization used around the recovery training blend. Preserving E41 normalization keeps the feature scale aligned with the deployed baseline while still allowing a small weight update.

Exam answer:

```text
After the smoke run regressed several holdout labels, I reduced the number of moving parts. The cautious E43 candidate keeps E41 normalization and starts from E41 weights, so the experiment tests a smaller targeted adaptation instead of changing both the model weights and the feature scale.
```

### Q: Why was the cautious E43 model also rejected?

It improved safety compared with the smoke model by reducing wrong accepted predictions from 7 to 2 on the same 95-example holdout. However, it still performed worse than the E41 baseline re-evaluated on that same holdout, and it failed the E43 recovery `COLOR` clips.

Exam answer:

```text
The cautious E43 run was useful because it showed that preserving E41 normalization reduced the smoke model's wrong-accept risk. But it was not promoted because E41 was still better on the same holdout, and the recovery data showed COLOR was still not learned. I kept the result as evidence and moved to error analysis instead of forcing another training run.
```

### Q: Why analyze recovery errors before another training run?

The same symptom can come from different causes: bad audio, ambiguous labels, poor class separation, unsafe thresholding, or a true need for more data. The cautious model showed `COLOR` was 0/10 on recovery clips but safely rejected, while `CREATE_REMINDER` and `VOLUME_DOWN` had wrong accepted errors. Those are different failure modes.

Exam answer:

```text
I did not immediately retrain again because the errors had different layers. COLOR was a safe rejection/classification weakness, while CREATE_REMINDER and VOLUME_DOWN included wrong accepted predictions. The next engineering step is to inspect the data and failure pattern so the intervention matches the actual cause.
```

### Q: What did the E43 audio/data inspection show about COLOR?

The `COLOR` recovery WAV files were valid 16 kHz mono 4-second recordings and were not grossly quiet or truncated. The more important finding was a phrase mismatch: the old calibration data used `color red`, while the failed recovery/live test used `color`.

Exam answer:

```text
The COLOR failure was not just an audio-quality problem. The evidence showed a phrase-coverage issue: the model had calibration data for "color red" but the live recovery command was "color". That means the next intervention should collect or train for the actual phrase variants instead of simply lowering the threshold.
```

### Q: Why verify E44 on the Pi before pulling it back?

Pi-side verification catches missing recordings and bad audio formats before the files are copied into the Windows evidence tree. It proves the recording session produced the planned recovery dataset structure.

Exam answer:

```text
I verified E44 on the Pi first to confirm that the recovery recording session was complete: 60 WAV files, 61 manifest rows including the header, and zero bad-format WAVs. That is a recording-completeness check, not proof that the model improved.
```

### Q: What does the E44 pullback and audio QC prove?

It proves that the recovery data was copied to Windows and is structurally usable: 60 WAV files, 61 manifest/hash rows, no bad audio-format files, and no QC-flagged clips. It does not prove the model improved.

Exam answer:

```text
The E44 pullback and QC prove data integrity and audio usability, not model performance. I still need a training-readiness audit and then a controlled model experiment before claiming any recognition improvement.
```

### Q: What does the E44 training-readiness audit prove?

It proves that the pulled E44 recovery data can be used by the training pipeline: the derived manifest has 60 rows, all WAV paths resolve, and the trainer loader accepts the manifest. It does not prove that a trained model will improve.

Exam answer:

```text
The E44 readiness audit is a pre-training gate. It proves the data is complete, traceable, and loader-compatible, but model improvement still requires a separate controlled training run and evaluation.
```

### Q: Why combine E43 and E44 recovery data for the next candidate?

E43 contains the original observed failure clips, while E44 adds focused phrase coverage for `color` and `color red` plus contrast examples. Combining them keeps the new experiment tied to the actual failure history instead of training only on the latest recording batch.

Exam answer:

```text
I combined E43 and E44 because E43 preserves the original failures and E44 adds the missing phrase and contrast coverage. That lets the next model candidate address the real error history while keeping the data marked as recovery-only, not validation.
```

### Q: Why was the E44 model rejected even though it had fewer holdout wrong accepts?

Wrong accepts are important, but they are not the only acceptance criterion. E44 reduced holdout wrong accepts to 1, but holdout accuracy and macro-F1 dropped, and the recovery objective failed: `COLOR` was only 3/30 correct with many wrong accepted recovery predictions.

Exam answer:

```text
I rejected E44 because a model cannot be promoted based on one metric. It reduced holdout wrong accepts, but it damaged overall holdout performance and still failed the main COLOR recovery goal. The evidence showed it was not a safe or complete improvement.
```

### Q: What did the COLOR command design audit show?

It showed that `COLOR` is not just an undertrained label. The one-word phrase `color` failed in E41, E43 cautious, and E44 cautious. Even `color red` stayed weak. That means the problem may be command phrase design and class separation, not simply needing another small training run.

Exam answer:

```text
The COLOR audit showed that three model states failed the one-word "color" command, and "color red" was still unreliable. I concluded that COLOR is an unresolved command-design/class-separation issue, so I stopped blind retraining and kept it incomplete in the requirements audit.
```

### Q: Why is E41 still the current candidate after E43 and E44?

E43 and E44 were controlled recovery attempts, but neither improved the overall
evidence enough to replace E41. E41 had the best 95-example holdout accuracy and
macro-F1. E44 reduced wrong accepts by one, but it also reduced accuracy/F1 and
did not solve `COLOR`.

Exam answer:

```text
I kept E41 as the current candidate because model selection used the same
holdout comparison, not wishful recovery results. E43 and E44 were preserved as
experiments, but E41 still had the strongest accuracy and macro-F1. E44 had one
fewer wrong accept, but it damaged overall performance and failed the COLOR
objective, so it was not promoted.
```

### Q: What does the requirements audit prove, and what does it not prove?

It proves the project has an evidence-based current status: which candidate is
best supported, which command categories are tested, which are partial, and
which requirements still lack evidence. It does not prove final completion.

Exam answer:

```text
The requirements audit is a traceability checkpoint. It prevents me from
claiming completion just because experiments exist. It shows that E41 is the
current candidate, but COLOR, CREATE_REMINDER, current Pi benchmarking, and
fresh final validation still need evidence before a 100/100 claim.
```

### Q: Why benchmark E41 separately if E33 already had a Raspberry Pi benchmark?

E33 benchmark evidence belongs to E33. Since E41 is now the current
evidence-supported candidate, its own runtime behavior must be measured on the
Pi. Similar architecture is not enough for a final evidence claim.

Exam answer:

```text
I cannot reuse E33 benchmark numbers as final proof for E41. E41 is a different
trained model and current candidate, so I need an E41 Pi benchmark measuring
latency, memory, CPU, temperature, and model load time. That keeps the evidence
tied to the actual candidate being considered.
```

### Q: What did the E41 Pi benchmark show?

The E41 benchmark showed real-time local inference speed on the Raspberry Pi:
mean latency was about 33.33 ms and p95 latency was about 38.77 ms across 95
repeated inferences over 19 saved Phase C command WAVs. It also showed that
recognition completeness is still separate: 65 repeated predictions were
accepted and 30 were rejected by the threshold policy.

Exam answer:

```text
The E41 benchmark supports the real-time Pi requirement because inference was
around 33 ms on average with p95 below 39 ms. But it is not an all-command pass:
the benchmark measured runtime on saved WAVs, and 30 of 95 repeated inferences
were rejected. So it supports speed/resource evidence, not final command
coverage.
```

### Q: Why hash benchmark pullback artifacts?

Hashing proves that the benchmark files archived in Windows are identifiable
and stable evidence artifacts. It also separates terminal output from durable
project evidence.

Exam answer:

```text
After running the Pi benchmark, I pulled back the summary JSON and latency CSV
and generated SHA256 hashes. That makes the runtime evidence auditable: I can
point to exact files and prove which files were used for the reported benchmark
numbers.
```

### Q: Why not fix the remaining failures by lowering the threshold?

Threshold changes only affect accept/reject decisions after the model predicts
a label. The worst Phase C failure was different: `CREATE_REMINDER` was
predicted as `LIST_REMINDERS` with very high confidence and executed the wrong
action. Lowering thresholds would not fix that classification error.

Exam answer:

```text
I did not lower the global threshold because the highest-risk failure was a
wrong high-confidence classification, not a low-confidence rejection. Threshold
tuning might help some correct-but-rejected commands, but it cannot distinguish
CREATE_REMINDER from LIST_REMINDERS when the model predicts the wrong class at
0.995 confidence. That needs targeted class-separation repair.
```

### Q: Why make E45 manifest-first instead of training immediately?

E43 and E44 showed that recovery training can regress the model if the data mix
is too broad or not aligned with the actual failure. E45 therefore starts with
a targeted manifest specification and readiness check before any training.

Exam answer:

```text
I made E45 manifest-first because the previous recovery attempts taught me that
more training is not automatically better. The repair needs to target the
actual failures: CREATE_REMINDER vs LIST_REMINDERS, LIGHT_ON, and a few
correct-but-rejected labels. By building and auditing the manifest first, I can
control the experimental variable before changing the model.
```

### Q: What did the E45 manifest-readiness audit prove?

It proved that the targeted recovery data for E45 is structurally ready for
training: the manifest has 125 rows, all WAV paths are unique and present, and
the audio files are valid 16 kHz mono 4-second WAVs. It did not prove that E45
will improve the model.

Exam answer:

```text
The E45 manifest audit proves data readiness, not model success. It checks that
the targeted repair data exists, is readable, has no duplicate paths, and
excludes COLOR as planned. Only after that gate passes should training be run
as a separate experiment.
```

### Q: Why was E45 not promoted after targeted training?

E45 improved some targeted recovery examples, but promotion depends on the
comparison baseline and safety behavior, not only recovery fit. E45 scored lower
than E41 on the 95-example holdout and produced more wrong accepted predictions
under the same E40 threshold policy.

Exam answer:

```text
I did not promote E45 because it failed the safety comparison against E41.
Although E45 reached 0.84 accuracy on the targeted recovery set, its holdout
accuracy and macro-F1 were lower than E41, and it had 3 wrong accepted holdout
predictions under E40 policy compared with E41's 1. That means E45 learned some
recovery examples but made the candidate less safe overall.
```

### Q: What is the engineering lesson from E45?

Targeted retraining can improve selected examples while still hurting the
system-level objective. A candidate must be judged by baseline comparison,
wrong-action risk, and independent validation readiness.

Exam answer:

```text
The E45 result shows why I separated recovery data from validation data and kept
E41 as the comparison baseline. A model can improve on recovery clips but still
increase wrong accepted commands. For a voice command system, wrong accepted
actions are more serious than correct rejections, so E45 is useful evidence but
not a promotable model.
```

### Q: What did the E45 wrong-accepted regression analysis show?

It showed that E45 changed the error profile. E41 had one wrong accepted
holdout sample, `COLOR -> WEATHER`. E45 removed that specific offline error but
introduced three new wrong accepted samples: `PAUSE -> CALL`, `STOP -> NEXT`,
and `CREATE_REMINDER -> ALARM`.

Exam answer:

```text
The important point is that E45 did not just fail to improve; it changed which
mistakes were unsafe. E41's wrong accept was COLOR to WEATHER. E45 removed that
offline wrong accept, but introduced three new accepted wrong actions. Two were
safe correct rejections in E41 that became unsafe wrong accepts in E45, and one
was a wrong but safely rejected STOP to NEXT confusion that became accepted.
```

### Q: Why does the E45 result not settle the COLOR question?

Because `COLOR` was explicitly excluded from E45's targeted recovery manifest.
E45's offline `COLOR_015.wav` row changed from accepted wrong to rejected
correct, but that was not the trained hypothesis and does not repair the live
one-word `color` failure.

Exam answer:

```text
I kept COLOR separate from E45. E45 excluded COLOR recovery rows, so I cannot
claim E45 solved COLOR just because one offline holdout row changed. COLOR
still needs its own command-design or recovery analysis.
```

### Q: What mechanism caused the E45 safety regressions?

The regressions occurred before routing or action execution. Two samples
changed the classifier's top label, and one sample kept the same wrong top label
but increased confidence enough to cross the E40 policy threshold.

Exam answer:

```text
The E45 safety failures were classifier and confidence-policy failures. PAUSE
became CALL with high confidence, and CREATE_REMINDER became ALARM with high
confidence. STOP was already confused as NEXT in E41, but E41 rejected it under
the E40 policy; E45 raised the NEXT confidence enough that the wrong command was
accepted. So the problem is not the router or action layer.
```

### Q: Why is the next recommendation calibration/policy analysis instead of retraining?

E45 showed that targeted retraining can move decision boundaries in unsafe
ways. Since one unsafe case was caused by crossing a class-specific threshold
and the others involved high-confidence wrong labels, the next evidence-based
step is to study confidence/rejection behavior before changing data or training
again.

Exam answer:

```text
I recommended confidence and rejection-policy analysis first because E45's
failures were safety regressions in confidence behavior. More training is not
automatically justified when the previous targeted training created new wrong
accepted commands. E41 remains frozen while I analyze whether policy or
calibration can reduce unsafe acceptance risk without retraining.
```

### Q: Why does confidence/rejection exist in this VCM?

The VCM triggers actions, so it should not execute every top prediction
automatically. Confidence/rejection is a guardrail that can block low-confidence
or risky predictions before they reach the router/action layer.

Exam answer:

```text
Confidence rejection exists because this is an action-triggering system. A
classification can be the top label but still be unsafe to execute if the model
is uncertain or if the class has known confusion risk. Rejection lets the system
prefer no action over a wrong action.
```

### Q: Why is classification accuracy alone insufficient?

Accuracy counts correct top labels, but it does not distinguish safe rejection
from unsafe acceptance. For a voice command system, a wrong accepted action is
more serious than a correct command being rejected.

Exam answer:

```text
Accuracy alone is not enough because the system has consequences after
classification. If a wrong label is accepted, the router may execute the wrong
action. I therefore track accepted correct, accepted wrong, rejected correct,
and rejected wrong separately.
```

### Q: What did STOP -> NEXT demonstrate?

`STOP_013.wav` showed why class-specific thresholds can be useful. E41
predicted `NEXT` at confidence 0.979959. A global 0.90 threshold would accept
that wrong prediction, but the E40 `NEXT` threshold of 0.98 rejected it.

Exam answer:

```text
STOP to NEXT demonstrated useful safety behavior from the E40 policy. The model
made a wrong top-label prediction, but the class-specific NEXT threshold was
just high enough to reject it. That prevented an unsafe media action.
```

### Q: Why not tune thresholds blindly?

Changing a threshold can recover correct commands but can also admit wrong
commands. Every threshold change must report the tradeoff among accepted
correct, accepted wrong, rejected correct, and rejected wrong.

Exam answer:

```text
I cannot lower thresholds just to improve pass count. A lower threshold may
turn safe rejections into unsafe accepted actions. Thresholds must be evaluated
as safety tradeoffs, not tuned to make one example pass.
```

### Q: What evidence would justify a class-specific calibration experiment?

A defensible calibration experiment needs existing evidence that a narrow
threshold change may recover correct rejected commands without increasing wrong
accepted commands in the analysis set, plus enough caution to test it
separately before any production change.

Exam answer:

```text
In Phase Z, PAUSE had correct low-confidence rejections and no PAUSE wrong
accepts in the small E41 holdout, so a narrow PAUSE calibration experiment is
scientifically justifiable. But it is not a production change yet because the
evidence is small and must be validated separately.
```

### Q: Why did Phase AA require fresh PAUSE calibration data?

Phase AA found no verified independent PAUSE calibration set. The 95-example
holdout created the PAUSE threshold hypothesis, E43 PAUSE clips were
recovery/training-linked, and Phase C had only one PAUSE trial.

Exam answer:

```text
Phase AA required fresh calibration data because I cannot validate a threshold
on the same holdout that suggested it. Existing PAUSE clips were either
discovery evidence, recovery/training data, or too small to support calibration.
So PAUSE equals 0.96 remains a hypothesis, not a validated production policy.
```

### Q: What remains fixed in a PAUSE threshold calibration experiment?

The model, preprocessing, wake behavior, label mapping, parser, router, action
logic, and all non-PAUSE thresholds remain fixed. `NEXT = 0.98` is explicitly
preserved because Phase Z showed it blocks the `STOP -> NEXT` unsafe action.

Exam answer:

```text
The only variable in Phase AA is the hypothetical PAUSE threshold. E41 weights,
preprocessing, routing, action logic, and all other E40 thresholds stay fixed.
This isolates whether PAUSE rejection policy can improve safely without
changing the model.
```

### Q: What did Phase AA data collection prove?

It proved that the independent calibration dataset was collected and passed basic integrity checks. It did not prove that a new PAUSE threshold works, because no inference or threshold analysis was run in this phase.

Exam answer:

```text
Phase AA collection proved data readiness, not policy improvement. We collected 100 fresh calibration WAVs, verified the manifest, checked for missing or duplicate files, confirmed 16 kHz mono audio, and generated SHA256 evidence. No model evaluation or threshold analysis was performed yet.
```

### Q: Why was the manifest repair acceptable?

The issue was a CSV formatting error caused by the comma in `plughw:2,0`, not an audio or provenance failure. The repair restored the intended metadata fields and preserved a pre-repair manifest backup.

Exam answer:

```text
The manifest repair was acceptable because the WAV files already passed integrity checks. The problem was that the ALSA device string contained a comma, which shifted CSV columns. We repaired only metadata, preserved the backup, and reran verification before accepting the dataset.
```

### Q: What did Phase AB show about the PAUSE threshold hypothesis?

Phase AB showed that the hypothesis is supported as calibration evidence only. On the independent 100-WAV Phase AA calibration set, lowering PAUSE from `0.99` to `0.96` recovered 2 correct PAUSE cases and introduced 0 newly accepted-wrong cases, but this does not authorize a production threshold change.

Exam answer:

```text
Phase AB supported the PAUSE threshold hypothesis at the calibration stage. It showed that a lower PAUSE threshold can recover correct PAUSE commands without adding wrong accepted cases on this calibration set. But calibration is not final validation, so E40 remains unchanged until a separate validation experiment confirms the candidate.
```

### Q: Why is the Phase AB result not final validation?

The Phase AA data was collected specifically for calibration after Phase Z generated a threshold hypothesis. Using it to choose a candidate threshold is valid calibration work, but final validation must be independent of both the discovery holdout and the calibration set.

Exam answer:

```text
Phase AB is not final validation because the dataset was used to evaluate candidate thresholds. Once a candidate is chosen, it must be tested on a separate fresh validation set. Otherwise I would be validating on data that influenced the threshold choice.
```

### Q: What did Phase AD measure that the holdout tests did not?

Phase AD measured the complete live Raspberry Pi pipeline: spoken wake phrase, microphone capture, wake gate, command recording, E41 classification, E40 rejection policy, routing, and local action evidence. The holdout tests measured prepared dataset WAV inference, not full live operation.

Exam answer:

```text
The holdout accuracy tells me how well the frozen model classifies held-out dataset WAVs. Phase AD tells me whether the complete live system works when a person speaks to the Raspberry Pi. Those are related but not the same measurement.
```

### Q: What was the Phase AD live result?

Phase AD recorded 65 live trials: 57 command trials and 8 no-action trials. Wake succeeded on 55/57 command trials. Raw live E41 accuracy was 39/55 = 70.91%. Accepted-action precision was 30/34 = 88.24%. End-to-end action success was 30/57 = 52.63%. No no-action trial executed an action.

Exam answer:

```text
Phase AD demonstrated live recognition, but it also showed a gap from holdout performance. The frozen E41 model reached 70.91% raw live accuracy after wake, compared with 94.74% on the comparable holdout. The main live problem was classification, not wake detection.
```

### Q: Why should we not average holdout, calibration, and live accuracy?

They answer different questions. Holdout evaluates model generalization on reserved dataset examples. Phase AA evaluates calibration behavior on a threshold-analysis dataset. Phase AD evaluates live end-to-end operation through hardware and action execution.

Exam answer:

```text
I keep holdout, calibration, and live metrics separate because they measure different systems under different conditions. Averaging them would hide whether a failure came from the model, threshold policy, wake gate, microphone capture, router, action layer, or output.
```

### Q: What were the most important Phase AD safety failures?

There were four accepted-wrong live actions: two `TEMPERATURE -> MESSAGE`, one `NEXT -> MESSAGE`, and one `LIGHT_OFF -> LIGHT_ON`. These matter more than safe rejections because the system accepted and executed the wrong action.

Exam answer:

```text
The highest-risk errors are wrong accepted actions. In Phase AD there were four: TEMPERATURE was accepted as MESSAGE twice, NEXT was accepted as MESSAGE once, and LIGHT_OFF was accepted as LIGHT_ON once. These should be diagnosed before retraining or changing thresholds.
```

### Q: What is the engineering decision after Phase AD?

The live VCM has been demonstrated, but the frozen E41/E40 system is not yet robust enough for broad final demonstration across all 19 commands. The next step is failure diagnosis, not immediate retraining or threshold changes.

Exam answer:

```text
Phase AD proves the full live pipeline runs, but it also reveals live classification weaknesses. The correct engineering response is to diagnose the accepted-wrong cases and weak classes first, while keeping E41 and E40 frozen until the failure layer is understood.
```

### Q: What did Phase AE diagnose after the live validation?

Phase AE diagnosed the Phase AD live failures without modifying the system. It found that the dominant live failure layer was raw VCM classification. Of 16 wrong live classifications after E41 was reached, E40 safely rejected 12 and accepted 4, producing wrong actions.

Exam answer:

```text
Phase AE showed that the live failures were primarily classification failures, not router or action-handler failures. E40 helped by rejecting 12 wrong classifications, but 4 wrong classifications exceeded the current predicted-class threshold and became wrong actions.
```

### Q: Why are the four accepted-wrong cases treated as safety-critical?

Because a wrong raw prediction was accepted and routed to an action. The four cases were `TEMPERATURE -> MESSAGE` twice, `NEXT -> MESSAGE` once, and `LIGHT_OFF -> LIGHT_ON` once.

Exam answer:

```text
A wrong accepted action is more serious than a wrong rejected classification because the system actually acts on the error. In Phase AE, the important safety cases were TEMPERATURE to MESSAGE, NEXT to MESSAGE, and LIGHT_OFF to LIGHT_ON.
```

### Q: Did Phase AE prove that thresholds should be changed?

No. Phase AE showed that higher predicted-class thresholds could theoretically reject the accepted-wrong examples, but it did not evaluate the tradeoff against correct accepts. Therefore it does not authorize changing E40.

Exam answer:

```text
Phase AE does not justify changing thresholds. It only shows that threshold policy affects whether wrong predictions execute. A threshold change would need a separate calibration or validation experiment measuring both safety and lost correct actions.
```

### Q: Are Phase AD clips valid for training now?

No. Phase AE marked the recordings as valid diagnostic evidence by basic WAV integrity checks, but they are not automatically training data. Any use for recovery must be specified in a separate experiment with provenance and validation separation.

Exam answer:

```text
The Phase AD clips are valid diagnostic evidence, not automatically training data. If I use them for recovery, I must define a new experiment, keep them out of final validation, and document the exact data role.
```

## Phase AF - Targeted Recovery Data

**Q: Why design recovery data after live failure diagnosis instead of immediately retraining?**
A: Phase AE identified specific live classification weaknesses. Targeted recovery data should address those measured confusion boundaries rather than adding broad or unrelated examples.

**Q: What evidence motivates Phase AF?**
A: Phase AD/AE showed accepted-wrong live actions for TEMPERATURE->MESSAGE, NEXT->MESSAGE, and LIGHT_OFF->LIGHT_ON, plus weak live performance for CALL and COLOR.

**Q: What must remain separate from recovery training?**
A: Formal holdout data, Phase AA calibration data, Phase AD live validation clips, and future final validation clips must remain independent so later evaluation is meaningful.

**Q: What should I explain in the oral exam?**
A: The project distinguishes diagnosing live failures, collecting targeted recovery evidence, training a new candidate, and validating on independent data. Phase AF only prepares fresh recovery data; it does not prove improvement.

## Phase AF - Recovery Dataset Integrity

**Q: What did Phase AF prove?**
A: It proved that the targeted recovery dataset was collected and passed integrity checks. It did not prove that the VCM improved.

**Q: Why is 
ecovery_training metadata important?**
A: It marks these clips as data that may be used for future model recovery, not as final validation evidence.

**Q: What evidence shows data separation was preserved?**
A: Integrity verification reported 0 validation leakage paths, with all clips under the Phase AF recovery directory and metadata set to PHASE_AF, 
ecovery, and 
ecovery_training.

**Q: What should I be able to explain in the oral exam?**
A: Targeted recovery data is collected after diagnosing live failure classes, but model improvement must still be tested by a separately specified training run and independent validation.

## Phase AG - Targeted Recovery Training Result

**Q: Why was E46 not promoted?**
A: E46 underperformed E41 on the frozen 95-example holdout, introduced more regressions than corrections, and increased accepted-wrong cases under the frozen E40 policy.

**Q: Why is recovery-set improvement not enough?**
A: Recovery data is training data. It can show fit to the intervention data, but independent holdout and later live validation are required to test generalization and safety.

**Q: What did the E40 policy comparison show?**
A: E46 produced 2 accepted-wrong holdout cases compared with E41's 1, reducing accepted-action precision from 0.9875 to 0.97297.

**Q: What should I explain in the oral exam?**
A: A targeted recovery experiment must be judged by both fixes and regressions. E46 corrected some errors but worsened overall holdout/safety behavior, so the disciplined decision is to keep E41 frozen.

## Phase AG - E46 Regression Diagnosis

**Q: What did the E46 regression diagnosis show?**
A: E46 corrected three E41 holdout errors but introduced six new errors, reducing raw holdout accuracy from 94.74% to 91.58%.

**Q: Why does accepted-action precision matter?**
A: The VCM triggers actions. A model with lower raw accuracy can also become less safe if wrong predictions cross the confidence policy and execute actions. E46 increased accepted-wrong cases from 1 to 2.

**Q: Were the regressions only in Phase AF target classes?**
A: No. Two regressions had target-class true labels and four had contrast-class true labels, so the pattern is mixed.

**Q: Can we say Phase AF caused the regressions?**
A: No. The evidence only shows that the E46 training configuration incorporated Phase AF recovery data and the resulting model regressed relative to E41. Causality would require a separate ablation experiment.

**Q: What should I say in the oral exam?**
A: E46 was a controlled experiment that did not satisfy promotion criteria. The disciplined decision is to preserve E41, document the regressions, and require a separate specification before any further intervention.

## Phase AG+ - Confidence / Acceptance Diagnosis

**Q: Were the E46 regressions mostly threshold-policy failures?**
A: No. The six E41-correct -> E46-wrong regressions were all top-1 classifier-output changes. E40 affected whether those changed predictions executed or were rejected, but it did not create the wrong labels.

**Q: What did STOP_013.wav demonstrate?**
A: STOP_013.wav is the key confidence-only safety case. Both E41 and E46 predicted the wrong class NEXT, but E41 confidence was 0.979959 and was rejected by the frozen NEXT threshold of 0.98, while E46 confidence rose to 0.999549 and was accepted.

**Q: What did VOLUME_DOWN_011.wav demonstrate?**
A: VOLUME_DOWN_011.wav was not confidence-only. E41 predicted VOLUME_DOWN and was rejected; E46 changed the top-1 prediction to VOLUME_UP with 0.998431 confidence, crossing the VOLUME_UP threshold and producing an accepted wrong action.

**Q: Were confidence margins analyzed?**
A: No. The available artifacts contained top-1 predictions and top-1 confidences only. Second-best predictions were not available, so margins were reported as N/A rather than invented.

**Q: What is the oral-exam takeaway?**
A: E46 changed both classifications and confidence behavior. Most regressions were classifier-output changes, but STOP_013 shows why acceptance policy still matters for safety. The evidence supports preserving E41 and designing any future calibration or classifier experiment separately.

## Strategic Direction - Reliable Live VCM

**Q: What is the project objective after Phase AD/AG+?**
A: The objective is no longer simply to decide whether E41 is good enough. The objective is to make the live Pi VCM work through controlled experiments with strict evidence gates.

**Q: What does "working" mean for this VCM?**
A: Fresh Pi speech should pass through HEY PI, command capture, correct VCM intent, safe acceptance/rejection, deterministic action routing, and evidence logging. The system works when accepted commands reliably produce correct actions and uncertain or wrong commands are safely rejected.

**Q: Why is raw classifier accuracy not enough?**
A: The VCM triggers actions. A wrong prediction that is rejected is safer than a wrong prediction that is accepted and routed to an action. Therefore accepted-action precision and wrong-accepted cases matter more than raw accuracy alone.

**Q: What is the strict promotion gate for any future candidate?**
A: A future candidate must avoid unacceptable frozen-holdout degradation, avoid increasing accepted-wrong actions, improve the documented high-risk live classes, avoid serious regressions in strong classes, then pass fresh Pi validation and end-to-end action validation.

**Q: What should I say if asked whether the project is nearly done?**
A: The project is technically functioning but not yet sufficiently reliable across fresh live demo conditions. The next phase is controlled candidate repair: improve the remaining failure modes without moving errors into previously working commands.

## Phase AH - Repair Design

**Q: Why did Phase AH start with artifact reconciliation?**
A: The previous prompt-provided sample list disagreed with the saved prediction artifacts. Before designing another intervention, Phase AH verified which holdout, E41 predictions, E46 predictions, and E40 policy rows were authoritative.

**Q: What did the reconciliation show?**
A: The saved artifacts are internally consistent. E41 predictions, E46 predictions, comparison rows, and E40 policy rows all refer to the same 95-example holdout. The mismatch was with the supplied sample list, not with the evaluation artifacts.

**Q: What remains the frozen baseline?**
A: E41 remains frozen at 90/95 raw holdout accuracy. Under frozen E40 it has 79 accepted-correct, 1 accepted-wrong, 11 rejected-correct, and 4 rejected-wrong outcomes.

**Q: Why not just train E47 immediately?**
A: E46 showed that a recovery experiment can improve some samples while regressing others and increasing accepted-wrong actions. The next experiment needs an ablation question so we learn what kind of intervention helps instead of merely moving errors around.

**Q: What next experiment did Phase AH recommend?**
A: A controlled classifier ablation. It should test a narrow repair hypothesis, such as target-only recovery, target+contrast data, or one-pair repair, while using the frozen holdout and E40 policy to detect regressions.

**Q: Where does confidence calibration fit?**
A: Confidence calibration is separate. STOP_013 shows E40 can protect against a wrong NEXT prediction near the 0.98 threshold, but this does not justify changing thresholds without a dedicated calibration study.

## Phase AI - E47 Ablation

**Q: What did E47 test?**
A: E47 tested whether a narrower classifier ablation could repair documented target/confusion classes without the broader regression pattern seen in E46.

**Q: How was E47 narrower than E46?**
A: E46 used 190 adaptation clips x6 plus all 105 Phase AF clips x2. E47 used 190 adaptation clips x1 plus only 75 selected Phase AF target/contrast clips x2, for 340 total training examples.

**Q: Did E47 improve the classifier?**
A: No. E47 dropped from E41's 90/95 holdout correct to 79/95 and produced 11 new E41-correct -> E47-wrong regressions with zero corrections.

**Q: What happened under the E40 safety policy?**
A: E47 increased accepted-wrong outcomes from 1 to 3. The accepted-wrong cases were PAUSE -> CALL, STOP -> NEXT, and LIST_REMINDERS -> CREATE_REMINDER.

**Q: Did the STOP -> NEXT safety issue reappear?**
A: Yes. E47 predicted NEXT for STOP_013 at confidence 0.992033, above the frozen NEXT threshold of 0.98, so it became accepted wrong.

**Q: What should I say in the oral exam?**
A: Phase AI was useful because it falsified a plausible narrow fine-tuning approach. It showed that even a smaller target/contrast repair can destabilize previously working classes, so E41 remains frozen and E47 is rejected.

## Phase AJ - Model / Representation Diagnosis

**Q: What did Phase AJ diagnose?**
A: Phase AJ examined whether remaining failures are better explained by representation, architecture, class separability, data limitations, or confidence/rejection behavior. It did not train a model or change the system.

**Q: What does the existing evidence say about the source of failures?**
A: Most remaining evidence points to top-1 classifier/class-separation failures under live Pi conditions. Confidence/rejection is still important because it decides whether wrong predictions become actions, but it does not create the wrong label.

**Q: Is the current feature representation proven insufficient?**
A: No. The 4-second, 40-bin log-mel representation is a plausible limitation because it uses fixed windows and no observed VAD/silence trimming, but E41's 94.74% formal holdout performance means insufficiency is not proven.

**Q: Is the current architecture proven insufficient?**
A: No. The inspected model is a tiny Conv2D CNN with global pooling and about 66k parameters. That architecture may compress temporal detail, but the evidence only justifies a controlled architecture experiment; it does not prove architecture is the root cause.

**Q: Why did E46 and E47 fail?**
A: Both were fine-tuning/data-mixture interventions on top of the same representation and architecture. Both moved decision boundaries, reduced frozen holdout accuracy, and increased accepted-wrong behavior under E40. Phase AJ reports this as an observed pattern, not a causal proof.

**Q: What is the next justified experiment?**
A: A controlled architecture experiment is the recommended next design path. It should isolate model capacity or temporal-context handling while keeping data, preprocessing, labels, E40 thresholds, router/actions, and evaluation fixed.

**Q: Does Phase AJ authorize E48?**
A: No. Phase AJ only designs the next experiment category. E41 remains frozen, E45/E46/E47 remain rejected, and no new model is promoted or trained in Phase AJ.

## Phase AK - E48 Pre-Training Gate

**Q: Why did E48 not train after execution was authorized?**
A: The execution rules required a uniquely specified architecture from Phase AJ. Phase AJ recommended an architecture experiment but did not define one exact layer-by-layer model, so training would have required inventing an architecture and would no longer be a controlled execution.

**Q: What was the required stop statement?**
A: E48 design is not sufficiently specified for controlled execution.

**Q: Why is stopping the correct engineering behavior?**
A: A controlled experiment needs one clear independent variable. If the agent chooses the architecture during execution, the result becomes arbitrary and hard to interpret. Stopping preserves traceability and prevents accidental uncontrolled experimentation.

**Q: Did this change E41 or E40?**
A: No. No E48 model was trained, no threshold changed, and no router/action/holdout/live-validation changes occurred. E41 remains frozen.

**Q: What must happen before E48 can run?**
A: A precise E48 architecture specification must be written first, including layer sequence, kernel sizes, channel counts, stride, pooling, normalization, activation, temporal handling, classifier head, parameter count, and model-size target.

## Phase AL - E48 Architecture Specification

**Q: What did Phase AL do?**
A: Phase AL converted the architecture idea from Phase AJ into one exact E48 architecture specification. It did not train the model.

**Q: What is the E48 architectural change?**
A: E48 keeps the E41 tiny CNN structure and inserts one temporal context block after the third max-pooling layer: SeparableConv2D with 96 filters, a 5x3 kernel, stride 1x1, same padding, relu activation, followed by BatchNorm momentum 0.1.

**Q: Why did you test architecture rather than retrain again?**
A: E45, E46, and E47 showed that additional fine-tuning or data mixtures can move decision boundaries, reduce frozen-holdout performance, or increase accepted-wrong behavior. Phase AJ therefore isolated architecture as the next experimental variable.

**Q: Why a separable temporal block?**
A: It adds local temporal context before global pooling while keeping the model small. E48 has 77,619 parameters versus E41's 66,483, so it remains Pi/TinyML-sized.

**Q: Why keep E40 unchanged?**
A: The experiment is testing classifier architecture, not the acceptance policy. Changing E40 would confound the result because we could not tell whether any safety change came from the classifier or from threshold policy.

**Q: Why not immediately test on the Pi?**
A: Offline promotion must precede live validation. Otherwise a change in live behavior could not be cleanly attributed to a validated model improvement.

**Q: What is the final Phase AL status?**
A: E48 FULLY SPECIFIED — READY FOR CONTROLLED TRAINING. E41 remains frozen, and no model, threshold, router/action, or holdout change occurred in Phase AL.

### Q: Why did Phase AM stop before training E48?

Because the training data control could not be verified. E41 recorded 240 adaptation clips and 120 Pi holdout examples, but the current local project state only resolved 231 adaptation clips and 95 holdout examples from the standard manifests. Training anyway would have changed the dataset as well as the architecture, so the experiment would no longer test one variable.

### Q: Is Phase AM a failed model result?

No. E48 was not trained, so Phase AM is a pre-training gate result, not model-performance evidence. The correct conclusion is that E48 remains inconclusive until the exact E41-authorized training data is restored and verified.


## Phase AN Professor-Facing Notes — Dataset Provenance

Q: Why did Phase AM stop before E48 training?
A: Not because the architecture was invalid. It stopped because the exact E41-authorized training and holdout data could not be reconstructed locally. A controlled architecture experiment requires the dataset to remain identical to E41.

Q: Why not substitute similar WAV files?
A: Substitution would change the training/evaluation data and confound the experiment. The result would no longer isolate architecture as the independent variable.

Q: What was found?
A: The authoritative E41 record says 240 adaptation clips and 120 holdout examples. Locally, 190 adaptation and 95 holdout clips were exact. The dedicated E41 recovery folder was missing, leaving 50 adaptation and 25 holdout examples unresolved/missing.

Q: What is the engineering decision?
A: E48 DATASET NOT READY — PROVENANCE GAP REMAINS. E41 remains frozen and no training occurred.


## Phase AO Professor-Facing Notes — Recovery Audit

Q: Why didn't you train E48 using the 190 files you could recover?
A: Because E48 was preregistered as a controlled architecture comparison against E41. Training with a different dataset would introduce a second experimental variable and invalidate the intended comparison.

Q: Why couldn't you simply use the existing 95-example holdout?
A: Because the authoritative E41 record identifies 120 Pi holdout examples. The 95-example set is an existing evaluation artifact, but it cannot be silently redefined as the complete E41 holdout for a new training experiment.

Q: What did the provenance audit establish?
A: Phase AO established that the exact missing E41 recovery directory was not recovered from local project storage or available archives. The project still has 190/240 adaptation clips and 95/120 holdout examples exactly recovered, with 75 authoritative E41 recovery WAVs remaining unavailable.


## Phase AP Professor-Facing Notes — Artifact-to-Pi Reconciliation

Q: What did Phase AP test?
A: It compared historical E41 artifacts against current Pi-side/local evidence to see whether the recovered WAVs could be proven to be the exact files used by E41.

Q: What was the result?
A: The historical artifacts confirm the expected E41 dataset structure, but the recovered 75-file Pi-side package was not available in the inspected local paths. Therefore, no byte-level exact match could be established.

Q: Why does this matter?
A: A controlled E48 architecture experiment requires the dataset to remain the same as E41. Without exact dataset identity, training E48 would confound architecture with dataset reconstruction differences.


## Phase AP Updated Professor-Facing Notes — Recovered E41 Dataset

Q: What changed after the recovered Pi package became available?
A: The project could verify all 75 recovered E41 recovery WAVs against the preserved Pi-generated SHA256 file.

Q: What could be proven exactly?
A: The 25 recovered E41 recovery holdout WAVs are exact matches to historical E41 prediction rows by path, label, trial, and Pi SHA256 verification.

Q: What remains a caveat?
A: The 50 adaptation WAVs are strongly consistent with the missing E41 training data, but the inspected E41 artifacts do not include a per-row training manifest or historical training hash. Therefore their historical training identity remains non-identifying rather than exact.

Q: Why not train E48 immediately?
A: Because the next step is a methodology decision: whether the recovered Pi manifest and SHA evidence are sufficient practical provenance for the preregistered architecture experiment, or whether a new experiment ID/dataset definition is required.


## Phase AQ Professor-Facing Notes — Dataset Readiness Decision

Q: What did Phase AQ decide?
A: Phase AQ decided that a future E48 architecture-only experiment may be authorized in a separate phase, but it must be described as using a frozen reconstructed E41-authorized dataset with a provenance caveat, not as a perfect byte-identical replay of historical E41 training.

Q: What does the exact 25/25 holdout recovery prove?
A: It proves artifact-to-dataset identity for the recovered E41 recovery holdout rows in the original 120-example E41 Pi holdout context. It does not by itself prove the separate current 95-example 94.74% benchmark.

Q: What remains uncertain about training data?
A: The 50 recovered adaptation WAVs match the recovered Pi SHA256 evidence and complete the expected 240 adaptation count, but no inspected E41 artifact provides per-row historical training hashes. Therefore their exact historical training identity remains non-identifying.

Q: Why can a future E48 still be methodologically allowed?
A: Because the future dataset boundary can now be frozen and audited: 240 adaptation clips for training and all 120 holdout clips excluded. The experiment can test architecture against frozen E41 as long as the provenance caveat is reported.

Q: What is the next intervention category?
A: Architecture. E45, E46, and E47 showed that data/fine-tuning changes can introduce regressions. Phase AJ selected architecture as the next controlled variable, and Phase AL specified the exact E48 temporal-context architecture. Confidence calibration and feature changes remain separate possible studies, not part of E48.


## Phase AR Professor-Facing Notes — E48 Architecture Specification

Q: What exactly is E41?
A: E41 is a small CNN over fixed log-mel features: `[398,40,1]` input, three Conv2D/BatchNorm/MaxPool blocks with 24, 48, and 96 filters, avg+max global pooling, Dense 64, and a 19-class softmax output. It has 66,483 parameters and no quantized artifact was observed.

Q: What exactly changes in E48?
A: E48 inserts one temporal context block after E41's third max-pooling layer: SeparableConv2D with 96 filters, a 5x3 kernel, stride 1x1, same padding, relu activation, followed by BatchNorm momentum 0.1. Everything else remains E41-equivalent.

Q: Why is this architecture-only?
A: The data boundary, preprocessing, log-mel features, labels, optimizer, learning rate, batch size, epoch budget, E40 thresholds, router/actions, and evaluation procedure are frozen. The only intended independent variable is the inserted temporal CNN block.

Q: Why protect against E45/E46/E47-style regressions?
A: Those experiments showed that a model can improve selected cases while degrading other commands or increasing accepted-wrong actions. E48 must therefore be judged by full-holdout regression analysis and frozen E40 safety behavior, not by a single target-class gain.


## Phase AS Professor-Facing Notes — E48 Offline Result

Q: Did E48 improve the frozen holdout?
A: On the current 95-example benchmark, yes by one sample: E41 was 90/95 and E48 was 91/95. This is an offline result only.

Q: Did E48 improve safety under E40?
A: On current95, E48 had 0 accepted-wrong outcomes under the unchanged E40 policy, compared with E41's 1 accepted-wrong outcome. Accepted-action precision rose from 98.75% to 100%.

Q: Why is E48 not automatically promoted?
A: Because the improvement was not uniformly clean. E48 introduced three raw regressions and reduced accepted-correct coverage from 79 to 72, meaning the unchanged confidence policy rejected more correct commands. Offline evidence also does not prove live Pi behavior.

Q: What did E48 demonstrate?
A: The architecture-only temporal block can change the classifier boundary in a potentially useful direction without increasing accepted-wrong actions on current95, but it also shifts some previously correct classes into new raw confusions. That makes it a candidate for review, not a production replacement.

Q: What remains required before any real promotion?
A: A separate fresh Pi live validation phase would be required, along with review of the reduced accepted-correct coverage and the `LIGHT_OFF`, `STOP`, and `TEMPERATURE` regressions.


## Phase AT Professor-Facing Notes — E41/E48 Regression Diagnosis

Q: Were the E48 changes mostly confidence-only?
A: No. The seven changed holdout cases were all top-1 classification changes. Some also changed E40 acceptance outcome, but the primary mechanism was classifier-output change.

Q: Why did E48 have zero accepted-wrong cases?
A: E48 corrected E41's accepted-wrong `COLOR -> WEATHER` row, and its new wrong predictions stayed below the frozen E40 thresholds. That is safe on current95, but it also means E48 is more conservative.

Q: What was the main E48 tradeoff?
A: E48 improved raw accuracy from 90/95 to 91/95 and accepted-action precision from 98.75% to 100%, but accepted-correct coverage dropped from 79 to 72 because more correct predictions were rejected.

Q: What should happen next?
A: A confidence/rejection calibration diagnostic should be run offline using existing evidence. That checks whether E48's correct rejections can be recovered without creating accepted-wrong actions. It should happen before live validation or production promotion.


## Phase AU Professor-Facing Notes — E48 Calibration Diagnostic

Q: Why not simply lower the global threshold?
A: Because global threshold lowering accepted wrong `STOP -> NEXT` predictions. Even global 0.95 created an accepted-wrong case in the existing E48 holdout predictions.

Q: What did the class-specific analysis show?
A: It showed that E48's coverage problem may be class-specific rather than global. Some class-specific what-ifs recovered many rejected-correct cases without accepting the observed wrong `NEXT` or `WEATHER` predictions.

Q: Why not change thresholds immediately?
A: The threshold candidates were discovered on the same current95 holdout. That is useful diagnostic evidence, but not independent validation. Changing production thresholds from it would overfit the holdout.

Q: What is the next controlled step?
A: Design a separate E48-specific calibration experiment with independent calibration evidence, keeping E48, E41, E40, and production thresholds frozen until that experiment is evaluated.


## Phase AV Professor-Facing Notes — Independent E48 Calibration Dataset

Q: Why create a new calibration dataset instead of using the current95 holdout?
A: Because the promising E48 threshold policies were discovered on current95. Using that same holdout to select thresholds would overfit the evaluation evidence. An independent calibration set is needed before any threshold policy can be proposed.

Q: Why include all 19 labels if the problem classes are narrower?
A: Threshold changes can affect which predictions become accepted across the whole command space. Full-label coverage helps detect whether recovering one class creates accepted-wrong actions elsewhere.

Q: Why oversample `NEXT`, `WEATHER`, `STOP`, `LIGHT_OFF`, `TEMPERATURE`, and `COLOR`?
A: Phase AU identified those classes as central to the E48 acceptance/rejection risk boundary, including `STOP -> NEXT`, `TEMPERATURE -> NEXT`, `LIGHT_OFF -> WEATHER`, and the eliminated E41 `COLOR -> WEATHER` case.

Q: What must happen before thresholds can change?
A: The Phase AV dataset must be freshly collected, verified for integrity and separation from the frozen holdout, evaluated offline with frozen E48, and then tested in a later controlled validation step. No production threshold is changed from the dataset specification alone.


## Phase AV Professor-Facing Notes — Collection Result

Q: What was collected?
A: A 210-example independent Raspberry Pi calibration dataset for E48 confidence/rejection analysis, covering all 19 executable command labels with additional coverage around the risk classes identified in Phase AU.

Q: Is this training data?
A: No. The dataset is marked calibration only. It is not E48 training data, not E41 training data, not holdout data, and not final validation data.

Q: Did collection change the system?
A: No. Collection produced WAV evidence and metadata only. No model, threshold, preprocessing, router, action, or production configuration was changed.

Q: What verification passed?
A: The Pi-side verifier reported 210 WAVs, 210 manifest rows, exact class counts, valid WAV format/durations, no missing files, no duplicates, valid labels, calibration metadata, and 0 frozen-holdout path overlap.

Q: What remains not measured?
A: Frozen-holdout SHA256 overlap was not available in the Pi-side verifier output because holdout hashes were unavailable there. The next calibration analysis should preserve that limitation unless the needed holdout hashes are made available.


## Phase AX Professor-Facing Notes — Availability Block

Q: Why was E48 calibration inference not run immediately?
A: The E48 model artifacts were local, but the 210 Phase AV WAV files and manifest were not present in the local inference environment. Running inference requires the actual audio bytes, not only the collection report.

Q: Why not reconstruct results from the manifest or pasted terminal output?
A: That would fabricate model evidence. Calibration inference must be computed from frozen E48 predictions on the actual WAV files.

Q: What must happen next?
A: The verified Phase AV dataset directory must be copied into the project, preserving the WAVs, manifest, integrity report, and SHA256 manifest. Then Phase AX can resume from local availability verification.


## Phase AX Professor-Facing Notes — Independent Calibration Inference

Q: What did Phase AX measure?
A: Phase AX measured frozen E48 raw classification and frozen E40 acceptance/rejection on the independent 210-example Phase AV calibration dataset.

Q: What was the result?
A: E48 achieved 88/210 raw correct, or 41.90%. Under frozen E40, it produced 38 accepted-correct, 13 accepted-wrong, 50 rejected-correct, and 109 rejected-wrong.

Q: Why is accepted-wrong important?
A: Accepted-wrong means the model predicted the wrong command with enough confidence for the action policy to accept it. In an action-triggering VCM, those cases are more safety-critical than wrong predictions that are rejected.

Q: Did Phase AX change thresholds?
A: No. Phase AX only measured frozen E48 under frozen E40. It did not optimize thresholds, modify E40, retrain E48, or promote any system.

Q: What does Phase AX imply?
A: The independent calibration data shows a major gap between current95 offline performance and fresh calibration behavior. Any future calibration or model decision must address the 13 accepted-wrong cases rather than optimizing coverage alone.


## Phase AY Professor-Facing Notes — Failure Diagnosis

Q: What was the most important Phase AY distinction?
A: AY separated raw classifier errors from confidence/rejection policy outcomes. E48 made 122 raw classification errors on 210 independent AV samples, so the problem cannot be described only as a threshold issue.

Q: Were the wrong predictions mostly low confidence?
A: No. There were 17 wrong predictions at confidence >= 0.90, including 13 accepted-wrong outcomes under frozen E40. That means several errors were confident wrong classifications.

Q: Does confidence calibration still matter?
A: Yes, because 50 correct predictions were rejected. But calibration alone cannot fix wrong top-1 predictions or high-confidence accepted-wrong cases.

Q: What did the E41 comparison show?
A: Frozen E41 had higher raw accuracy on the same AV set than E48, but produced many more accepted-wrong outcomes under E40. This shows that raw accuracy and accepted-action safety must be evaluated separately.

Q: What next direction is justified?
A: A clean retraining/data strategy is justified to design: speaker-diverse, phrase-diverse, separated training/calibration/validation evidence. The evidence points to a generalization and class-separation problem, not merely an architecture or threshold tweak.


## Phase AZ Professor-Facing Notes — Additional Dataset Integration Audit

Q: What was done?
A: I audited the additional posted dataset before training anything. Google Drive file-level connector access was not available in this Codex session, so I used the local downloaded copy at `C:\Users\Loreen Anne\Downloads\VCM\VCM` and its manifests/reports.

Q: What did the dataset actually contain?
A: `VCM_MASTER` contained 36,622 manifest rows/audio files across 16 classes with train/validation/test splits of 27,130/4,734/4,758 and 395 speakers/groups. `VCM_BALANCED` contained 15,268 WAV training files across the same 16 classes, derived only from Dataset A training data.

Q: What was the hypothesis?
A: The large speaker-independent dataset might address the AX/AY generalization failure more cleanly than another targeted recovery model, but only if it could be integrated without leaking evaluation data or collapsing required commands.

Q: What evidence was used?
A: I used Dataset A/B manifests, embedded audit reports, class/speaker/source/provenance fields, SHA256 manifests generated in AZ, and the current project audio pools. The SHA256 check found zero byte-identical overlaps between Dataset B audio and 21,757 scoped current-project audio files.

Q: What failed or remained incomplete?
A: The dataset does not cover all current raw labels. It lacks `COLOR`, `CREATE_REMINDER`, `LIST_REMINDERS`, `CALL`, and `MESSAGE`; `BRIGHTNESS` is only partially represented by `LIGHT_DIM`. Therefore it cannot replace the 19-label model by itself.

Q: Was anything promoted?
A: No. AZ promoted nothing. It authorized only the design of a future controlled training-data experiment after review. E41, E48, E40, thresholds, preprocessing, and router/actions stayed frozen.

Q: What would be done next?
A: Pre-register a new data-intervention experiment, likely E49, using Dataset B for covered labels and existing/project data for missing labels, while keeping Dataset A validation/test and all prior holdout/live evidence out of training.


## Phase AZ-R Professor-Facing Notes — Actual Dataset 2 Verification

Q: What changed after preliminary AZ?
A: The actual Dataset 2 package was downloaded locally into the project at `data/VCM Dataset2`. AZ-R therefore verified the real files instead of relying on the earlier connector-limited audit.

Q: What was verified?
A: I reconciled the actual files against the Dataset 2 specification PDF. Dataset A matched 36,622 total rows/files with train/validation/test 27,130/4,734/4,758, 16 classes, 395 speakers/groups, and 0 missing/corrupt audio. Dataset B matched 15,268 training files, 13,801 original rows, 1,467 augmented rows, 16 classes, and all documented class counts.

Q: How was speaker leakage checked?
A: Speaker IDs were read from the actual manifests. Train∩validation, train∩test, validation∩test, Dataset B∩A-validation, and Dataset B∩A-test were all zero.

Q: How was Dataset B provenance checked?
A: Every Dataset B row's `original_source` was checked against Dataset A manifest paths. All 15,268 rows traced to Dataset A train, with zero validation/test source leaks, zero missing sources, and zero source-label mismatches.

Q: What does Dataset 2 help with?
A: It provides substantial speaker-independent training support for many problematic classes, including `NEXT`, `VOLUME_DOWN`, `LIGHT_OFF`, and `TEMPERATURE`, plus UNKNOWN/SILENCE support. However, `MEDIA_NEXT` has grouped multi-sensor recordings rather than 956 independent utterances, and `SET_TEMPERATURE` has synthetic-derived training support that must be disclosed.

Q: What does Dataset 2 not solve?
A: It does not provide `COLOR`, `CREATE_REMINDER`, `LIST_REMINDERS`, `CALL`, or `MESSAGE`. It also only partially supports `BRIGHTNESS` through `LIGHT_DIM`, and does not support color adjustment.

Q: Was a model trained?
A: No. AZ-R was an audit-only phase. No model, threshold, preprocessing, architecture, label mapping, dataset merge, router/action, recording, or live validation changed.

Q: What is the next defensible experiment?
A: A pre-registered data-intervention experiment, likely E49, using Dataset2 B for covered labels plus existing/project training data for missing labels, while keeping Dataset A validation/test and all prior holdout/live/calibration evidence out of training.


## Phase BA Professor-Facing Notes — Controlled Hybrid Dataset Training

Q: What was done?
A: I ran one controlled training-data experiment, `E49_BA_HYBRID_DATASET_E41_ARCH`, using the E41 architecture and frozen E41 initialization while adding verified Dataset2 training rows only for legitimately mapped labels.

Q: Why was it done?
A: Existing models showed a large gap between established holdout performance and independently recorded speech. Rather than repeatedly changing thresholds or targeting individual errors, BA isolated training-data composition as the primary intervention.

Q: What was the hypothesis?
A: Speaker-diverse Dataset2 training data might improve independent real-world generalization on Phase AV while preserving the full 19-label VCM taxonomy.

Q: What evidence controlled the dataset?
A: AZ-R verified Dataset2 split integrity, speaker separation, provenance, and zero byte-identical overlap with checked project/protected audio. BA then created a frozen 11,830-row manifest and checked 0 protected path overlap and 0 protected SHA256 overlap.

Q: What happened?
A: BA improved Phase AV raw accuracy to 148/210 = 70.48%, compared with 103/210 for E41 and 88/210 for E48. It also produced 102 accepted-correct Phase AV actions and 80.95% accepted-action precision under frozen E40.

Q: What failed?
A: BA still produced 24 accepted-wrong Phase AV actions and regressed current95 to 78/95 = 82.11%. `COLOR`, `LIGHT_ON`, `TIME`, and `TIMER` remained weak areas, and high-confidence wrong predictions persisted.

Q: Why was the candidate rejected?
A: The promotion gate required meaningful independent improvement without unsafe action regression. BA improved raw generalization, but 24 accepted-wrong actions is not acceptable for production and is worse than E48's 13 accepted-wrong Phase AV cases.

Q: What did the experiment teach?
A: Dataset2-style speaker-diverse training data helps the classifier generalize to independent speech, but data alone did not solve action safety or all class-separation problems. The remaining problem is still mixed: taxonomy gaps, sparse `COLOR`, class confusions, and confidence/rejection behavior.

Q: What would be done next?
A: Do not automatically retrain or tune thresholds from BA. The project should preserve BA as evidence, keep E41/E48/E40 frozen, and decide separately whether there is time for a carefully authorized next step focused on final assignment evidence rather than another uncontrolled model run.


## Phase BB Professor-Facing Notes — E49 Regression Diagnosis

Q: What was done?
A: I diagnosed E49 without training anything. I compared E41 and E49 per-sample and per-class on current95 and Phase AV, audited the E49 training-manifest composition, and analyzed the 24 E49 accepted-wrong Phase AV actions.

Q: Why was it done?
A: E49 was rejected for production, but its 70.48% Phase AV raw accuracy is a major generalization improvement. The project needed to understand why that gain came with current95 regression and unsafe accepted-wrong actions before any next experiment.

Q: What improved?
A: E49 fixed many independent AV examples that E41 missed: 63 E41-wrong AV samples became E49-correct. It also repaired all tracked AY confusion families relative to E48.

Q: What regressed?
A: On current95, 14 E41-correct examples became E49-wrong and only 2 E41-wrong examples became E49-correct. The largest current95 losses were in `VOLUME_UP`, `TIMER`, `PAUSE`, `CREATE_REMINDER`, `LIGHT_ON`, and `TIME`.

Q: Were the five Dataset2-uncovered labels disproportionately damaged?
A: No. Current95 raw-correct delta was -10 for Dataset2-supported/partial labels and -2 for uncovered labels. The uncovered labels improved net +16 on Phase AV. However, `COLOR` remains unsafe because it has only 10 training examples and produced 6 accepted-wrong AV actions.

Q: What happened with accepted-wrong actions?
A: E49 had 24 accepted-wrong AV cases. Eight repeated the same wrong prediction as E41, nine were different E41 wrong predictions, and seven were new raw errors where E41 was correct. Seventeen were new accepted-wrong outcomes relative to E41.

Q: What did BB teach?
A: E49 is a useful but unsafe tradeoff. Dataset2-style data improved independent generalization, but the hybrid training procedure moved established decision boundaries and likely caused some forgetting or semantic boundary conflict.

Q: What should happen next?
A: Do not immediately train another model. If authorized, the next experiment should change only data composition/sampling: preserve original-domain examples more strongly while retaining the Dataset2 diversity benefit. Phase AV must remain evaluation-only.


## Phase BC Professor-Facing Notes — Command Vocabulary Revision

Q: What was done?
A: I verified whether the future classifier vocabulary can replace the literal `COLOR` label with `LIGHT_DIM` before training another model.

Q: Why was it done?
A: E49 showed that `COLOR` remained weak and unsafe, while Dataset2 has direct `LIGHT_DIM` support and no `COLOR` support. The assignment category is `Dim / color lights`, so the project can choose dimming as its concrete implemented command if documented honestly.

Q: What did the assignment say?
A: The assignment lists the required category as `Dim / color lights` and gives `Dim lights to X percent` as the example. It does not require a classifier label literally named `COLOR`.

Q: What did the code show?
A: `COLOR` currently routes to `LIGHT_ADJUST` with `color=red`; `BRIGHTNESS` routes to `LIGHT_ADJUST` with `brightness_percent=50`. The action handler updates local light brightness/color state and can optionally use GPIO/PWM for brightness.

Q: What did Dataset2 show?
A: Dataset2 contains `LIGHT_DIM` and defines it as dimming/reducing light brightness. Dataset2 contains no `COLOR`, `CREATE_REMINDER`, `LIST_REMINDERS`, `CALL`, `MESSAGE`, or literal `BRIGHTNESS` class.

Q: Is the change implemented?
A: No. BC is specification only. No router/action/model/threshold/preprocessing change was made, and no model was trained.

Q: What remains unresolved?
A: `BRIGHTNESS` and proposed `LIGHT_DIM` overlap in the current implementation. A future phase must define whether `LIGHT_DIM` is relative dimming and `BRIGHTNESS` is general/explicit brightness adjustment, or whether the labels should be consolidated.

Q: What would happen next?
A: A future authorized experiment would use the revised vocabulary and test controlled class preservation/rebalancing while keeping architecture, preprocessing, thresholds, wake model, and protected evaluations frozen.


## Phase BF Professor-Facing Notes — Frozen End-to-End Functional Audit

Q: What was done?
A: I audited the current frozen project as an end-to-end VCM system, checking the packaged runner, model defaults, router, local action layer, response WAV path, and feasibility of the requested 19-command spoken wake-command-action-response loop.

Q: Why was it done?
A: Classifier accuracy alone does not prove the assignment demo works. The project needed to verify whether spoken commands automatically trigger the correct local actions and whether the system returns to listening for another command.

Q: What evidence was used?
A: I inspected the actual deployment package scripts, model-label files, router/action code, package README/manifest, and current BA/BB/BC documentation. I also checked the packaged music/response directory and local runtime availability for `arecord` and `aplay`.

Q: What happened?
A: The audit found that the packaged predictor defaults to E33, while the historical live-evidence stack is E37 wake + E41 command + E40 policy. E49 exists as a rejected offline model, not as the active packaged Pi default. The runner is single-cycle, and no per-command response WAV bank is configured.

Q: What failed?
A: Fresh spoken BF trials could not be executed in this Codex environment because it is not the Raspberry Pi runtime and lacks the Pi microphone/playback path. The requested multi-cycle test also cannot be demonstrated by the current runner without implementation changes.

Q: Why was no candidate promoted or rejected?
A: BF did not produce new classifier or live recognition results. It identified integration-readiness blockers, so it cannot promote a model or reject a model on recognition grounds.

Q: What did the audit teach?
A: The remaining demo risk is not only model accuracy. The project must align the selected frozen stack, implement or verify persistent listening, and configure response audio if the final demonstration requires WAV feedback for each command.

Q: What would be done next?
A: Either run the BF procedure on the actual Raspberry Pi with an explicitly selected frozen stack, or authorize a narrow implementation phase for persistent loop/response playback before repeating the audit. Do not start another model experiment from BF alone.


## Phase BG Professor-Facing Notes — Initiation

Q: Why start BG?
A: E49 showed that adding speaker-diverse Dataset2 training data can improve independent command recognition, but BB showed the hybrid composition also moved important original-domain decision boundaries. BG now focuses on the classifier itself, with controlled data composition and revised vocabulary.

Q: What is the first hypothesis?
A: A revised-vocabulary model using `LIGHT_DIM` instead of sparse `COLOR`, while preserving more original project examples than E49, may improve generalization without repeating E49's current95 regression.

Q: What is frozen?
A: Protected current95, Phase AV, Phase AD/live evidence, Dataset2 validation/test, historical E41/E48/E49 artifacts, thresholds, preprocessing, and action/router history are not used as training data or silently changed.

Q: What is not being done first?
A: No GPIO/action-layer work, no threshold gaming, and no architecture change unless data-composition experiments fail or representation evidence justifies it.


## Phase BG Professor-Facing Notes — Final Offline Classifier Decision

Q: What was done?
A: I trained and evaluated two revised-vocabulary CNN candidates, E50 and E51, using E41 architecture/preprocessing and a controlled 16,100-row hybrid training manifest with stronger original-data preservation than E49.

Q: Why was it done?
A: E49 proved that Dataset2-style speaker-diverse data improves independent generalization, but it regressed current95 and left too many accepted-wrong actions. BG tested whether a better-preserved hybrid dataset plus the `COLOR -> LIGHT_DIM` vocabulary revision could produce a stronger offline classifier.

Q: What was the hypothesis?
A: Preserving more original-domain data while adding bounded Dataset2 support for compatible labels could retain most of E49's Phase AV gain while reducing E49's current95 regression and accepted-wrong behavior.

Q: What evidence controlled the experiment?
A: The manifest excluded current95, Phase AV, Phase AD/live recordings, Dataset2 validation/test rows, and other protected evaluation data. Historical `COLOR` rows were not relabeled; compatible historical comparisons exclude them.

Q: What happened?
A: E50 achieved 83/90 = 92.22% on current95-compatible rows and 139/194 = 71.65% on Phase AV-compatible rows, with 8 accepted-wrong Phase AV-compatible cases. E51 was safer on the broader Dataset2/combined revised test but weaker on protected-compatible current95 and Phase AV.

Q: What failed or remains weak?
A: E50 still has weak Phase AV classes, especially `VOLUME_UP`, `TIME`, `NEXT`, `CALL`, `VOLUME_DOWN`, and `BRIGHTNESS`. It also has high-confidence wrong predictions and has not been validated in the Pi wake-command-action loop.

Q: Why was E50 selected?
A: E50 is the best balance for the final command-classifier role: it substantially improves over E41 on independent Phase AV-compatible speech, greatly reduces E49's accepted-wrong compatible cases, and recovers much of the current95-compatible regression.

Q: Why was E51 rejected?
A: E51 improved Dataset2/combined safety, but its current95-compatible and Phase AV-compatible raw performance were materially lower than E50. For final project continuity, that tradeoff is not preferable.

Q: What did BG teach?
A: Data composition and vocabulary repair matter. The project now has a stronger offline CNN candidate than the rejected E49, but classifier improvement alone does not finish the assignment demo.

Q: What would be done next?
A: Do not train another model immediately. Package E50 in a separate deployment/demo phase, implement/verify the revised `LIGHT_DIM` runtime route, and run fresh Raspberry Pi end-to-end validation before making any final demo-readiness claim.


## Phase BH Professor-Facing Notes — E50 Package Integration

Q: What was done?
A: I integrated the selected E50 command classifier into the Raspberry Pi package together with the preserved E37 wake model.

Q: Why was it done?
A: BG produced a stronger offline classifier, but BF showed the Pi package still pointed to an older E33 command model and lacked the revised `LIGHT_DIM` runtime route. A model cannot be legitimately validated on the Pi until it is actually packaged and routable.

Q: What changed?
A: E50 weights/normalization/labels and E37 wake artifacts were copied into the package. `LIGHT_DIM` was added to the router as a brightness-dimming action. The wake-gated demo defaults now point to E37 wake and E50 command classification.

Q: Was this threshold tuning?
A: No. The E50 policy preserves frozen E40 numeric thresholds for the revised vocabulary. `LIGHT_DIM` inherits the default threshold used during BG evaluation.

Q: What evidence was produced?
A: Syntax checks passed, `LIGHT_DIM` routing/action dry-run passed, and packaged E50 inference correctly loaded and accepted an existing ALARM WAV.

Q: What remains unproven?
A: Pi microphone wake detection, live command capture, repeated listening, response WAV playback, GPIO/PWM behavior, and final end-to-end demo readiness remain unverified until a Pi validation phase is run.

Q: What should happen next?
A: Run controlled Pi-side validation with the packaged E37+E50 stack. Do not train another model before seeing whether failures are model errors or integration/runtime errors.


## Phase BI Professor-Facing Notes — E50 Pi Live Validation

Q: What was done?
A: The E37 wake model and E50 command model were tested on the Raspberry Pi microphone path using wake-gated spoken trials. The returned evidence archive was copied back, hash-verified, extracted, and parsed.

Q: Why was it done?
A: Offline accuracy was not enough. The project needed to prove whether the selected classifier could run through the real Pi wake-command-routing-action pipeline.

Q: What evidence was used?
A: The Pi evidence archive `e50_wake_gated_live_20260928_evidence.tar.gz` with SHA256 `81916037181eacf42ed40904d4f89d7e038db46c90e6495ec8e5a70ed3c9e2b5`, containing 36 result JSON files and paired WAV recordings.

Q: What worked?
A: Wake detection was 36/36. Twelve command labels achieved at least one end-to-end pass: `PLAY_MUSIC`, `WEATHER`, `LIGHT_ON`, `LIGHT_OFF`, `LIGHT_DIM`, `TIMER`, `ALARM`, `NEXT`, `PAUSE`, `STOP`, `LIST_REMINDERS`, and `MESSAGE`. UNKNOWN/no-action safe rejection passed.

Q: What failed?
A: Seven command labels did not achieve an end-to-end pass in this evidence set: `TIME`, `BRIGHTNESS`, `TEMPERATURE`, `VOLUME_UP`, `VOLUME_DOWN`, `CREATE_REMINDER`, and `CALL`. `TEMPERATURE` had one accepted-wrong action as `WEATHER`.

Q: What integration issue was found?
A: `LIGHT_DIM` was initially classified correctly but failed because the Pi package lacked the router route. After adding the route on the Pi, `LIGHT_DIM` passed end-to-end.

Q: What did BI teach?
A: The project now has real Pi evidence that E37+E50 works for many commands and safely rejects some weak cases, but the model is not yet reliable for all commands. Some remaining problems are classifier weaknesses, while persistent loop and response playback are implementation/demo gaps.

Q: What would be done next?
A: Decide whether to remediate weak labels and demo-loop gaps or present a defensible demo subset with limitations. Do not claim 100/100 final completion from BI alone.


## Phase BJ Professor-Facing Notes — Diagnosis-First Targeted Remediation Decision

Q: What was done?
A: I diagnosed the Phase BI live Pi results command by command and decided the next legitimate step before final demo preparation.

Q: Why was it done?
A: BI proved that E37+E50 works for many commands on the Pi, but it also exposed weak commands and one accepted-wrong action. The project needed to decide whether to train again, remediate narrowly, or prepare a limited demo without overstating completion.

Q: What was the hypothesis?
A: The remaining failures are probably mixed: some classifier failures, some phrase/capture-sensitive safe rejections, and some runtime/demo-integration gaps. Therefore, a diagnosis-first targeted phase is more defensible than another general CNN sweep.

Q: What evidence was used?
A: The Phase BI report, `PHASE_BI_TRIAL_RESULTS.csv`, `PHASE_BI_PER_LABEL_SUMMARY.csv`, and the verified Pi evidence archive with SHA256 `81916037181eacf42ed40904d4f89d7e038db46c90e6495ec8e5a70ed3c9e2b5`.

Q: What happened?
A: BJ classified the weak labels. `TEMPERATURE` is the highest-priority safety issue because it was accepted as `WEATHER` at confidence `0.997283935546875` and executed the wrong action. `TIME`, `BRIGHTNESS`, `VOLUME_UP`, `VOLUME_DOWN`, and `CREATE_REMINDER` showed correct or partly correct recognition but were rejected. `CALL` showed boundary failure but safe rejection.

Q: What failed?
A: BJ did not add new live evidence and did not solve the weak commands. It also does not close persistent listening, response WAV playback, or GPIO/PWM evidence gaps.

Q: Why was no new model trained?
A: Training is not yet the smallest defensible step. First, the weak labels need targeted repeat validation on the Pi under the frozen stack to determine whether failures are repeatable classifier defects, phrase/capture sensitivity, or integration issues.

Q: What did BJ teach?
A: The current system is good enough to support a defensible subset demo, but not an all-command final demo claim. The next work should either validate/remediate weak labels narrowly or present limitations honestly.

Q: What would be done next?
A: Run the targeted Pi repeat plan for `TEMPERATURE`, `TIME`, `BRIGHTNESS`, `VOLUME_UP`, `VOLUME_DOWN`, `CREATE_REMINDER`, and `CALL` without changing thresholds or the model. Separately verify persistent listening and response feedback for the final demo.


## Phase BK Professor-Facing Notes — Targeted Weak-Command Repeat Validation

Q: What was done?
A: The weak commands from BJ were retested on the Raspberry Pi using the frozen E37 wake model and E50 command model. The evidence archive was copied back, hash-verified, extracted, and parsed.

Q: Why was it done?
A: BI showed several weak labels. BJ decided that the next legitimate step was targeted repeat validation, not another model sweep or threshold tuning.

Q: What evidence was used?
A: The archive `e50_bk_targeted_weak_command_repeats_e37_e50_20260928_evidence.tar.gz` with SHA256 `e92b12464153fbf2652aafdbadd3459eab6a1a1331fcb5463c0da3e69b851513`, containing Pi-side result JSON and WAV evidence.

Q: What happened?
A: Wake detection succeeded for all 22 weak-command trials. `CREATE_REMINDER` recovered with accepted correct actions for `remind me` and `set reminder`. `TEMPERATURE` passed once for `set temperature`, but also produced accepted wrong actions as `STOP` and `WEATHER`.

Q: What failed?
A: `TEMPERATURE` is not safe enough for demo use. `TIME`, `BRIGHTNESS`, `VOLUME_UP`, `VOLUME_DOWN`, and `CALL` still did not produce accepted end-to-end passes.

Q: Why was no model promoted or retrained?
A: BK was a validation and diagnosis phase. It showed enough evidence to adjust the demo plan, but it did not authorize training. The accepted-wrong `TEMPERATURE` failures also make threshold lowering unsafe.

Q: What did BK teach?
A: The project can honestly expand the demo-supported subset to include `CREATE_REMINDER`, but it cannot claim all 19 revised commands work. The remaining weak commands need either explicit limitation or later targeted remediation.

Q: What would be done next?
A: Prepare a defensible final demo using the supported subset, document the unsupported/unsafe labels, and separately close demo-integration gaps such as persistent listening and response feedback if time permits.


## Phase BL Professor-Facing Notes — Targeted Weak-Command Remediation

Q: What was done?
A: I diagnosed the remaining weak commands and ran one controlled remediation experiment, E52, initialized from E50 with weak-label sample weights. This was not a general CNN sweep.

Q: Why was it done?
A: BI and BK showed that E50 works live for many commands, but `TIME`, `BRIGHTNESS`, `TEMPERATURE`, `VOLUME_UP`, `VOLUME_DOWN`, and `CALL` remained weak. `TEMPERATURE` was especially important because it caused accepted wrong actions.

Q: What was the hypothesis?
A: The weak labels might be improved by a small, controlled fine-tune emphasizing those classes while preserving the E50 architecture, preprocessing, vocabulary, and threshold policy.

Q: What evidence was used?
A: BI and BK live Pi evidence, E50/E51 offline comparison artifacts, the E50 training manifest, current95-compatible evaluation, Phase AV-compatible evaluation, and replay evaluation on BI/BK WAVs.

Q: What happened?
A: E52 improved Phase AV-compatible raw accuracy from 139/194 to 150/194. However, accepted-wrong actions increased from 8 to 13 on Phase AV-compatible evidence. BI replay also worsened from 1 E50 accepted-wrong action to 3 E52 accepted-wrong actions.

Q: What failed?
A: E52 did not safely remediate the weak commands. It increased raw recognition in some places but made action execution less safe.

Q: Why was E52 rejected?
A: A final VCM demo must avoid wrong accepted actions. E52's raw accuracy gain did not justify the increase in accepted-wrong actions, especially with persistent `TEMPERATURE` confusion.

Q: What did the experiment teach?
A: The remaining problem is not solved by simple weak-label weighting. More raw correct classifications can come with worse action safety, so the project should preserve E50 and demo only commands with live evidence unless future targeted data collection is authorized.

Q: What would be done next?
A: Prepare a defensible final demo subset using `PLAY_MUSIC`, `WEATHER`, `LIGHT_ON`, `LIGHT_OFF`, `LIGHT_DIM`, `TIMER`, `ALARM`, `NEXT`, `PAUSE`, `STOP`, `CREATE_REMINDER`, `LIST_REMINDERS`, and `MESSAGE`. If all 19 labels must be recovered, collect new targeted training/validation recordings for the six weak labels in a later controlled phase.


## Phase BM Professor-Facing Notes — Final E50 Integration and Demo Hardening

Q: What was done?
A: I finalized the E37+E50 deployment package, verified E50 integrity, hardened the runtime for persistent operation, added local response WAV assets, audited router/action mappings, replayed existing live WAV evidence through the package, measured laptop-side efficiency, and prepared the final Pi validation handoff.

Q: Why E50?
A: E50 balances independent recognition, current-set behavior, accepted-wrong safety, and deployment readiness better than later alternatives. E52 improved raw Phase AV-compatible accuracy but increased accepted-wrong actions, so it was rejected.

Q: Why was another training sweep not performed?
A: Model optimization is closed. The remaining work is integration and physical validation. Another sweep would risk replacing a defensible stack without solving response playback, persistent loop, and hardware validation requirements.

Q: What is the current recognition performance?
A: Offline E50 evidence remains separate: current95-compatible 83/90 and Phase AV-compatible 139/194. Live BI evidence remains wake 36/36, raw command recognition 24/35, accepted-correct 15, accepted-wrong 1, and UNKNOWN safe rejection 1/1.

Q: Why are some commands not in the demo?
A: `TIME`, `BRIGHTNESS`, `TEMPERATURE`, `VOLUME_UP`, `VOLUME_DOWN`, and `CALL` do not have sufficient current live end-to-end evidence. `TEMPERATURE` is specifically unsafe due to accepted-wrong actions.

Q: How is UNKNOWN handled?
A: `UNKNOWN` and `WAKE` are no-action labels in the router. BI already showed one irrelevant phrase safely rejected.

Q: How is the system offline?
A: Recognition uses local E37/E50 CNN inference and deterministic routing. Weather, calls, messages, and reminders are local stub/state actions unless a downstream service is explicitly added; recognition itself does not use network, ASR, cloud, or an LLM.

Q: How is the CNN separated from the router?
A: E50 outputs a raw label. The deterministic router maps that label to an intent and slots. The action layer then updates local state or invokes local hardware/audio behavior.

Q: How is the model loaded?
A: BM added a reusable predictor so the persistent runtime can load model weights, labels, and threshold policy once at startup instead of reloading each cycle.

Q: How is runtime efficiency measured?
A: BM measured Windows/laptop latency only: 66,483 parameters, 251,734-byte weights, about 0.040 s mean command-decision time. Pi latency must be measured on the Pi.

Q: What is the current limitation?
A: The final package is ready for physical validation, but persistent-loop behavior, response WAV playback, GPIO/PWM, and Pi latency still need Pi-side evidence.


## Phase BM Addendum Professor-Facing Notes — Physical Pi Final Validation

Q: What was done after the BM handoff?
A: The final E37+E50 runtime was executed on the Raspberry Pi for 13 selected demo commands plus one UNKNOWN phrase, and the resulting WAV/JSON evidence archive was copied back into the project.

Q: What was the evidence archive?
A: `outputs/e50_bm_final_demo_20260928_evidence.tar.gz`, SHA256 `4695a6d0fb282624499a42d8102ff4bf578022c5a0e15a8368b8ef7fd97079ec`.

Q: What worked?
A: Wake succeeded in 13/14 total trials. The system automatically executed the action pipeline for 9/13 selected demo commands: `PLAY_MUSIC`, `WEATHER`, `LIGHT_ON`, `LIGHT_DIM`, `TIMER`, `ALARM`, `PAUSE`, `CREATE_REMINDER`, and `LIST_REMINDERS`. All 14 trials returned to listening. The UNKNOWN phrase was safely rejected.

Q: What failed?
A: `LIGHT_OFF`, `NEXT`, `STOP`, and `MESSAGE` did not reach action execution in this physical run. Also, all attempted response WAV playbacks failed because `aplay` exited with status 1, even though the WAV files existed and were readable.

Q: Does this mean the classifier failed?
A: Not for the response issue. The response failure is a Pi audio-output/playback configuration problem. It should not be fixed by training, threshold changes, or model replacement.

Q: Can we claim full end-to-end audio demo success?
A: No. Full audio end-to-end success was 0/13 in this physical run because audible response playback was not verified. The defensible claim is partial physical validation: wake, recognition, automatic routing/action, and loop return worked for 9 selected demo commands.

Q: What is the next legitimate step?
A: Diagnose the Pi audio output path and rerun a small response-playback validation. Do not run another CNN sweep, tune thresholds, or deploy E52 to solve an audio playback failure.


## Phase BM Correction Professor-Facing Notes — Callability vs Demo Readiness

Q: Are the six unresolved commands removed from the VCM?
A: No. `TIME`, `BRIGHTNESS`, `TEMPERATURE`, `VOLUME_UP`, `VOLUME_DOWN`, and `CALL` remain callable and testable. They remain in the complete 19-command vocabulary and retain legitimate router/action paths.

Q: What does not demo-ready mean?
A: It means current evidence is insufficient or unsafe for deliberate final demonstration. It does not mean the command is unavailable, disabled, or unimplemented.

Q: What is the status of TEMPERATURE?
A: `TEMPERATURE` is callable and implemented, but unsafe/not demo-ready because it has produced accepted-wrong live actions. It should remain testable so its behavior can be measured and remediated.

Q: Is the 13-command final demo subset a whitelist?
A: No. It is only a presentation/safety subset. The runtime must not reject commands merely because they are outside the current demo-ready subset.

Q: Where are the two command-status tables?
A: Table A is `PHASE_BM_19_COMMAND_IMPLEMENTATION_CALLABILITY.csv`, covering all 19 commands. Table B is `PHASE_BM_CURRENT_DEMO_READY_COMMANDS.csv`, covering the current demo-ready subset.


## Phase BN Professor-Facing Notes — Final Pi Runtime Hardening

Q: What is Phase BN?
A: Phase BN is deployment/runtime validation work for the frozen E37+E50 VCM. It does not train another model. It prepares the Pi package for audio diagnosis, all-19 command testing, efficiency measurement, and final demo validation.

Q: What was changed?
A: The runtime now supports `--response-audio-device` so response WAV playback can use a verified ALSA device. It also records `aplay` stderr in JSON evidence. Response WAV assets now cover all 19 commands plus UNKNOWN.

Q: Did this change the CNN?
A: No. E50 weights, preprocessing, architecture, E37 wake model, and E40-compatible thresholds were not changed.

Q: Why add response WAVs for the six unresolved commands?
A: Because all 19 commands remain callable/testable. If an unresolved command is tested, a missing response file should not be mistaken for a recognition or router failure.

Q: Why is audio first?
A: The last Pi run showed response playback failed with `aplay exited with status 1`. That is an audio-output/runtime problem, not a classifier problem.

Q: What is the next physical step?
A: Deploy `e50_bn_runtime_update_20260928.tar.gz` to the Pi and run `bash scripts/run_phase_bn_audio_diagnostics.sh`. Only after audio is understood should the audio smoke and all-19 validation scripts be run.

Q: What remains not measured?
A: Pi response playback success, all-19 physical command behavior, persistent-cycle stability, Pi latency/CPU/RAM, and GPIO behavior remain not measured until physical Pi execution.

## Phase BN Prompted Audio Smoke Professor-Facing Notes

Q: Did response audio eventually work on the Pi?
A: Yes for the prompted repeated-cycle smoke set. After selecting `plughw:CARD=vc4hdmi1,DEV=0` and regenerating longer response tones, four prompted trials (`ALARM`, `TIMER`, `PAUSE`, `LIST_REMINDERS`) each executed and reported `response_result.played=true`. The operator reported hearing all four tones.

Q: Does this prove one continuous persistent loop?
A: Not by itself. These were four prompted single-cycle invocations, so they verify repeated prompted operation and audible response feedback, but they should not be described as a single same-process continuous model-loaded-once run.

Q: What is next?
A: Run the all-19 prompted validation script. All 19 commands remain callable/testable, but only commands with sufficient evidence should be deliberately presented as demo-ready.

## Phase BN All-19 Pi Validation Professor-Facing Notes

Q: Did we test all 19 commands on the Pi?
A: Yes. Phase BN ran a prompted physical audit of all 19 command labels plus one UNKNOWN phrase. The archive is `outputs/e50_bn_all19_validation_20260928_evidence.tar.gz`, SHA256 `18b7bda8aff4dc9de12568e20626069547f51c03397deffe222ab6fad7115e98`.

Q: What was the result?
A: 10/19 commands reached end-to-end audio pass in this run: `PLAY_MUSIC`, `WEATHER`, `LIGHT_OFF`, `BRIGHTNESS`, `TIMER`, `ALARM`, `TEMPERATURE`, `PAUSE`, `STOP`, and `LIST_REMINDERS`. There were 0 accepted-wrong command actions, and the UNKNOWN phrase was safely rejected.

Q: Are the other commands unavailable?
A: No. They remain callable/testable. In this run they were safe misses: rejected after wake, missed at wake, or not accepted. They should be reported as callable/not verified under these conditions, not removed.

Q: Is TEMPERATURE demo-ready now?
A: No. It passed in this run, but prior live evidence showed accepted-wrong `TEMPERATURE` actions. It remains callable/implemented but unsafe/not demo-ready until specifically remediated and repeat-validated.

## 2026-09-29 - Final Deployment Guide Questions

Q: Why did you not train another CNN?

A: Model development was explicitly closed by the final deployment guide. The current engineering need is integration: packaging the frozen E37 wake model, E50 command CNN, E40-compatible guardrails, deterministic router, response playback, persistent runtime, and touchscreen control into a defensible offline Raspberry Pi system.

Q: What does the touchscreen GUI do?

A: The GUI is only a local START / STOP / STATUS controller. It launches the existing E37+E50 runtime, prevents duplicate starts, stops the child runtime, and displays the latest command/action/response state from JSON evidence. It does not perform recognition, routing, thresholding, or action logic.

Q: Is the final standalone system fully verified now?

A: Not yet. The package is staged and all 19 commands remain callable, but physical touchscreen verification, same-process continuous-loop proof, final Wi-Fi-off/Ethernet-disconnected/laptop-disconnected demo, non-primary-speaker validation, and Pi performance measurements remain incomplete or not measured.

Q: Why keep weak commands callable?

A: The project requirement is a 19-command offline speech-command system. Removing weak commands would create a demo whitelist and hide evidence. The correct distinction is callable versus verified versus demo-ready.

## 2026-09-29 - Response Audio Correction

Q: Are the current response WAVs final demo responses?

A: No. They are placeholder tones/audio-path smoke assets. The final deployment guide requires recorded human voice responses for each command.

Q: What was done to fix this?

A: The project now includes a Pi-side recorder and verifier for human command responses. The current files are explicitly marked `FAIL_TOO_SHORT_LIKELY_PLACEHOLDER`, and final response compliance is blocked until fresh human responses are recorded and played back through the Pi speaker.

Q: Did this change recognition behavior?

A: No. E37, E50, E40, preprocessing, thresholds, routing, and actions remain unchanged.


## Phase BN-CLOSE Professor-Facing Notes

Q: Is final deployment verified now?
A: Not yet. The package is staged and heavily audited, but BN-CLOSE still requires physical Pi evidence for touchscreen operation, same-process continuous loop, no-laptop/offline use, final human recorded responses, performance measurements, and non-primary-speaker validation.

Q: What is safe to claim?
A: The frozen E37+E50+E40-compatible VCM is packaged locally, all 19 commands remain callable/testable, the latest all-19 Pi audit had 10/19 end-to-end audio passes and 0 accepted-wrong actions, and UNKNOWN `open the window` was safely rejected.

Q: What is not safe to claim?
A: Do not claim standalone touchscreen deployment, Wi-Fi-off/no-laptop demo, final recorded human responses, Pi CPU/RAM/temperature/latency, or non-primary-speaker validation until those tests are physically run.

## Phase BN-CLOSE Round1 Professor-Facing Notes

Q: Did the persistent loop work?
A: The 5-cycle same-process loop worked for recognition/action/return-to-listening: 5/5 wake accepts, 5/5 command accepts/actions, and 5/5 returned to listening.

Q: What failed?
A: Recorded response playback failed inside the runtime because the configured device `plughw:CARD=vc4hdmi1,DEV=0` returned ALSA error 524. Direct playback then proved `plughw:CARD=vc4hdmi0,DEV=0` and `default` play the timer response audibly.

Q: What layer is this?
A: Response playback device selection. It is not a CNN, threshold, router, or action failure.


## Phase BN-CLOSE Round2 Professor-Facing Notes

Q: What did Round2 add beyond Round1?
A: Round2 reran the same-process persistent loop with the working playback device and produced source-backed Pi evidence. The archive is `outputs/e50_bn_close_20260929_round2_evidence.tar.gz`, SHA256 `f21ce0f86552978dbdbeeba31afb7ef3849e04cb788e257ebc1dc5639b00865f`.

Q: What worked in Round2?
A: 5/5 wake stages were accepted, 5/5 commands were accepted, 5/5 actions executed, 5/5 response playbacks reported true, 5/5 cycles returned to listening, and GPIO was not requested.

Q: Which commands were covered?
A: `PLAY_MUSIC`, `TIMER`, `ALARM`, `PAUSE`, and `LIST_REMINDERS`.

Q: Which audio device worked?
A: Runtime response playback used `plughw:CARD=vc4hdmi0,DEV=0`. The operator reported hearing all available responses first, and the answers to the commands were correct.

Q: Does this replace the all-19 audit?
A: No. Round2 proves a clean same-process persistent demo loop for selected commands. The separate all-19 audit remains the evidence for complete vocabulary callability/testing status.


## Phase BN-CLOSE Extra-Loud Response Notes

Q: What was changed about the response WAVs?
A: The response set was replaced with Pi-working extra-loud WAVs under `responses_extra_loud_20260929/`, and `configs/demo_response_assets.json` maps runtime responses to those files.

Q: What evidence preserves this response set?
A: `outputs/e50_bn_close_extra_loud_responses_20260929.tar.gz`, SHA256 `9ce3be48ee05738305a189a15eb0e1de4c126767084138266f11cdb32d1f1128`.

Q: Are all commands covered?
A: Yes. The response-map audit verifies all 19 command labels plus `UNKNOWN` map to existing `responses_extra_loud_20260929/*_extra_loud.wav` files.

Q: Were these acceptable to the operator?
A: Yes. The operator reported the extra-loud responses were perfect.

Q: What happened to the earlier boosted response package?
A: The earlier Windows-side `responses_boosted/` package is obsolete for deployment playback. The accepted deployment response set is the Pi-working `responses_extra_loud_20260929/` set.


## Phase BN-CLOSE Wake-Wait Professor-Facing Notes

Q: What usability issue was fixed?
A: The runtime could move through wake windows too quickly after a response. BN-CLOSE added a wake-wait mode so the process keeps recording wake attempts until the next `WAKE` is accepted.

Q: Did this change the CNN or thresholds?
A: No. The wake-wait update is runtime control flow only. It does not modify E37, E50, preprocessing, architecture, thresholds, routing, actions, or command vocabulary.

Q: What runtime update was deployed?
A: The update added `--wait-for-wake`, `--max-wake-attempts`, and `--wake-retry-delay-sec` to `scripts/pi_wake_voice_control_demo.py`, plus a wrapper for the BN-CLOSE wake-wait demo. The runtime-update archive is `outputs/e50_bn_close_wake_wait_runtime_update_20260929.tar.gz`, SHA256 `8e991c75c2d85c334dcf58df558881e163522d361911175a64c3de96fbc521c6`.

Q: What physical evidence verifies wake-wait behavior?
A: `outputs/e50_bn_close_wake_wait_20260929_evidence.tar.gz`, SHA256 `c8223dd8eec144baa1cdbf28803856695eac2897511f2eba2a27741126a6539f`.

Q: What were the wake-wait results?
A: 13 result JSON files were produced. Wake accepted in 13/13, the runtime returned to listening in 13/13, 8/13 commands executed with response playback true, and GPIO was requested 0 times.

Q: How do we know it waited instead of stopping?
A: Trials `e50_bn_close_wake_wait_012` and `e50_bn_close_wake_wait_013` required multiple wake attempts before acceptance, with a maximum of 4 wake attempts. That shows the process stayed alive and kept listening for wake instead of ending after a missed wake window.

Q: What about the rejected commands in the wake-wait run?
A: They were command-stage threshold/reliability outcomes after wake acceptance, not wake-wait lifecycle failures. The rejected predictions were below their configured thresholds, so no unsafe action was taken.


## Phase BN-CLOSE Current Exam-Safe Claims

Q: What is now safe to claim?
A: The frozen offline E37+E50 VCM is packaged and physically validated on the Pi for selected demo operation. All 19 commands remain callable/testable. The Round2 same-process loop passed 5/5 selected cycles with correct response playback. The extra-loud response map covers all 19 commands plus `UNKNOWN`. Wake-wait behavior is physically verified, including multiple wake attempts before acceptance.

Q: What should still not be overclaimed?
A: Do not claim touchscreen GUI physical verification, standalone Wi-Fi-off/no-laptop demonstration, GPIO/PWM execution, final Pi CPU/RAM/temperature performance metrics, or complete 19-command demo readiness unless those specific tests are run and archived.

Q: What remains limited?
A: The six weak commands remain callable/testable but not automatically demo-ready. `TEMPERATURE` remains callable and implemented, but unsafe/not demo-ready because earlier evidence showed accepted-wrong behavior.


## Phase BN-CLOSE Touchscreen GUI Professor-Facing Notes

Q: What did the touchscreen GUI validation show?
A: The GUI launches on the Pi display, starts/stops the wake-wait runtime, writes CSV/JSON evidence, plays responses through the HDMI0 extra-loud response path, and returns to listening after trials.

Q: What is the latest touchscreen GUI sweep evidence?
A: The Pi evidence directory is `pi_validation/e50_bn_close_touchscreen_gui_wake_unknown_20260929_162246`. The Pi archive is `e50_bn_close_touchscreen_gui_wake_unknown_20260929_162246_evidence.tar.gz`, SHA256 `d031f797a833bcdb06c00e8603e3573bd7569d048062229970c88821c1a9e01f`.

Q: What was the summary?
A: 26 result JSON files, 26 wake accepted, 9 commands executed, 9 response playbacks true, 26 returned to listening, and GPIO requested 0.

Q: What do the GUI states mean?
A: `WAKE ME UP` means say `hey pi`; `I AM NOT AWAKE` means the wake gate missed and the operator should repeat `hey pi`; `SAY WHAT YOU NEED` means wake was accepted and the command window is open; `I DIDN'T UNDERSTAND` means a listed-command prediction was rejected; `I CAN'T DO THAT` means the rejected command label was `UNKNOWN`.

Q: What about Alexa waking the system?
A: The operator observed that saying `alexa` can wake the system. That is a wake false-accept / alternate-wake observation for later debugging, not a touchscreen GUI failure.

Q: Is this a full 19-command benchmark?
A: No. This sweep validates touchscreen GUI/display behavior and selected command execution. It does not replace the all-19 command audit, and it does not make weak commands demo-ready.

## Section 68 Items 10-15 Current Exam-Safe Notes

Q: What Section 68 blockers were closed after the read-only audit?
A: Items 10, 11, 12, and 14 were verified with controlled Pi evidence: duplicate runtime / START-STOP, standalone offline operation, UNKNOWN/silence/wrong-command safety, and non-primary-speaker validation.

Q: What is the strongest Item 10 evidence?
A: `e50_bn_close_item10_duplicate_runtime_20260930_084836_three_cycle_evidence.tar.gz`, SHA256 `712b36c7d8b54af7dc551f65a43199a4c5d909d04daa428aa589e28d8ba9bfe8`. It covers repeated START behavior, command-after-repeat behavior, STOP cleanup, START after STOP, and three START -> command -> STOP cycles.

Q: What is the strongest Item 11 evidence?
A: `e50_bn_close_item11_network_off_20260930_093353_evidence.tar.gz`, SHA256 `215f33cbe05a40b5fdb285fe77e1d91a122d3fa494fd5593c5684fa1b59d561a`. The Pi was operated locally with Wi-Fi/network off; laptop/SSH was used only afterward for evidence collection.

Q: What did Item 12 prove?
A: The safety sweep produced four safety/rejection cases with zero unintended actions, zero duplicate actions, five of five returns to listening, and a successful TIMER recovery command. Archive SHA256: `1523324c4a60ac4c2545a7220ecb38f125b4c9729a8ae75225332a6ca639ce89`.

Q: What is the Item 12 caveat?
A: Wake-miss/no-wake periods in wake-wait mode do not emit result JSON. Those observations are supported by the operator sequence plus absence of action/result entries, not by dedicated wake-miss JSON.

Q: What did Item 14 prove?
A: A genuinely non-primary speaker used the Pi microphone under the frozen E50 runtime. The run captured 9 trials, 9/9 wake accepts, 9/9 returns to listening, 4 executed commands, 5 rejected commands, and 4 accepted-wrong classifications/actions. This verifies actual non-primary-speaker Pi operation, but the accuracy was mixed. Archive SHA256: `360603516a3e7d4ea5747a5e7f08988c3655c1d17fee72a77edcc9446c73f5e3`.

Q: What limitation should be disclosed for Item 14?
A: Speaker B's voice was softer than the primary speaker, and some repeats reflected difficulty following written GUI prompts and timing. This should be reported as measured validation context, not hidden and not used to justify unapproved retraining.

Q: What is the Item 15 status?
A: PARTIALLY VERIFIED. Real Pi metrics were captured for E50 model load, saved-WAV inference latency, CPU, memory, temperature, and loop/resource behavior, but fine-grained live timing dimensions were not separately observable without instrumentation.

Q: What were the key Item 15 numbers?
A: E50 model load was 1.8566 seconds. Saved-WAV command inference over 70 runs had mean 31.82 ms, median 31.39 ms, min 29.18 ms, max 38.31 ms, p90 33.94 ms, and p95 34.40 ms. CPU during the inference benchmark was 99.55 percent. Temperature rose from 42.2 C pre-runtime to 46.1 C post-GUI run and 48.5 C at benchmark end.

Q: What is next?
A: Section 68 Item 16: designate or produce the final benchmark. Do not jump directly to the final GitHub package, professor command sheet, demo script, or FINAL HARD STOP.

## Section 68 Item 16 Exam-Safe Notes

Q: Is the final benchmark now recorded?
A: Yes. Item 16 is VERIFIED. Evidence directory: `pi_validation/e50_bn_close_item16_final_benchmark_20260930_105703`. Archive SHA256: `b6a2d9e66f42a1d6b4eb118f9e02505361072582e29b50add9761b1d359b5da1`.

Q: What population was benchmarked?
A: 20 prompted physical Pi trials: all 19 required command labels plus one unsupported UNKNOWN/no-action phrase. No primary benchmark trial was excluded.

Q: What are the headline metrics?
A: Wake success 19/20 overall; raw command classification 13/19; acceptance 10/19; accepted-correct 10; accepted-wrong 0; accepted-action precision 100%; safe rejection among non-executed trials 10/10; end-to-end action success 10/19; UNKNOWN/no-action safety 1/1; return-to-listening 20/20.

Q: Is this a 13-command demo benchmark?
A: No. The benchmark preserves all 19 callable labels. The 13-command demo-ready set remains a separate presentation boundary, not a runtime whitelist.

Q: Did this change the VCM?
A: No. Item 16 was benchmark recording/reporting only. E37, E50, E40, thresholds, router, response assets, GUI behavior, runtime behavior, microphone configuration, and audio configuration were unchanged.

## Final Evidence / User-Voice / Professor Package Audit Exam-Safe Notes

Q: What is the final professor package recommendation?
A: READY WITH DOCUMENTED LIMITATIONS. The package is professor-facing and evidence-based, but it preserves real limitations instead of presenting E50 as perfect or production-complete.

Q: What is the final package path?
A: `github_package/ME2_VCM_E50_GITHUB_PACKAGE_20260930`.

Q: What are the final package manifest numbers?
A: 121 files including `PACKAGE_FILE_MANIFEST.csv`, 120 manifest rows, 20,114,600 bytes, and package manifest SHA256 `D3D01317E936F8090EF36E484922D2A2D1CF4784D7B5C3FC6B0FB37536840F79`.

Q: Did the final audit change the frozen VCM?
A: No. E37, E50, E40, thresholds, router, response assets, GUI behavior, runtime behavior, microphone/audio configuration, command vocabulary, and model weights remained frozen.

Q: What is the final E50 model hash?
A: `BC8AC64CED4305DDF43BF4DE377F3CC636A764EFF339CD9F92AF06340C50B8FF`.

Q: What is the E37 evidence?
A: E37 weights SHA256 `687E82E2CEFA6D74CEF2C0A15D28F8F6142D47D4A67E57C68C091E83FC2CEBDE`; E37 normalization SHA256 `3BFA93F202DC0C241E577E5B89506F2CB6D0F35B8239297C215A7F81E970B4C7`.

Q: What is the E40 evidence?
A: E40 policy SHA256 `A0B2495328FD5A1E0E5885E727623BA6D9F823BE94CCCDFD0AEAD77254BBB3FD`.

Q: Did the user's voice enter final E50 training?
A: The strongest honest answer is conservative. The identified Phase AF user-recorded targeted recovery clips were not found in the final E50/BG training manifest, but absolute exclusion of all historical user voice from the full training lineage is not established because older Pi adaptation/recovery rows are present and speaker identity is not proven from filenames alone.

Q: What exactly did the Phase AF check show?
A: Phase AF collected 105 targeted recovery recordings for `CALL`, `COLOR`, `TEMPERATURE`, `NEXT`, and `LIGHT_OFF`. The final E50/BG training manifest search found 0 matches for `PHASE_AF`, `targeted_live`, or `recovery_training`.

Q: What was the final E50/BG training composition?
A: 16,100 rows total: 13,070 active-project training rows, 2,800 Dataset2 training rows, and 230 E41 reconstructed adaptation rows.

Q: Did user speech appear anywhere?
A: Yes. User speech was used in live physical Pi validation of the frozen system. That is validation/deployment evidence, not automatically training data.

Q: What is the final user-voice provenance classification?
A: INDETERMINATE for absolute user-voice exclusion; SUPPORTED for non-inclusion of the identified Phase AF targeted recovery clips in final E50/BG training.

Q: What should not be claimed?
A: Do not claim "100% guaranteed no user voice anywhere in training." Do not claim 19/19 end-to-end success. Do not claim broad speaker independence, formal noise robustness, ECE calibration, acoustic onset latency, or full package-copy Pi deployability unless separately tested.

Q: What timing evidence was added after Item 15?
A: Timing-only disposable instrumentation evidence: `e50_timing_breakdown_20260930_144234_evidence.tar.gz`, SHA256 `BE85B65BC1EC7FD074D6838D87D8C71ED20947880D8DFE205865310C7DCCD61D`.

Q: Does the timing-only run replace Item 15?
A: No. Item 15 remains the Section 68 performance measurement evidence. The timing-only run is supplementary and clarifies live pipeline timing while preserving the frozen production runtime.

Q: What remains not measured?
A: GUI launch-to-ready latency, acoustic response onset, full physical acoustic latency, ECE/calibration curve, systematic noise/reverb robustness, formal phrasing robustness, and formal statistical speaker independence.

Q: Is E53 part of E50?
A: No. E53 remains a separate independent experiment. No E53 implementation, model, dataset, configuration, or evidence is part of the final E50 implementation or benchmark.

## E50 Training-Dynamics / Overfitting Defense Notes

Q: Did the E50 model overfit?
A: The E50 training history shows classical overfitting after epoch 7: training performance continued improving while validation loss worsened. However, epoch 7 was already the best internal validation-loss point and was the selected E50 checkpoint. Therefore, the later overfit epochs were not the deployed model. The finding is documented as a limitation of the training trajectory rather than evidence that a later overfit checkpoint was deployed.

Q: What exact evidence supports that?
A: The E50 history file records epoch 7 with training loss `0.3457678720680258`, training accuracy `0.8800621118012423`, validation loss `1.3987702131271362`, and validation accuracy `0.6197039305768249`. By epoch 11, training loss improved to `0.19462700002634573` and training accuracy to `0.9322360248447205`, while validation loss worsened to `2.188316583633423` and validation accuracy was `0.6018376722817764`.

Q: Why did you not retrain E50 to fix it?
A: The selected checkpoint was already the best internal validation-loss checkpoint, so simply stopping earlier does not constitute a new remedy: the deployed model was already selected at that point. In addition, prior controlled experiments did not establish a reliably superior alternative. Reopening training immediately before delivery would require a new controlled experiment and independent validation. The project therefore preserves the frozen E50 model and documents the observed training limitation honestly.

Q: If the model overfit, why did you deploy it?
A: The later training epochs exhibited overfitting, but those later epochs were not deployed. Epoch 7 was the best internal validation-loss checkpoint and was selected for the final E50 model. The remaining deployment gap therefore cannot simply be described as the result of deploying a later overfit checkpoint.

Q: Why didn't you just stop training earlier?
A: The final checkpoint was already selected at the best internal validation-loss point, epoch 7. Stopping before epoch 7 would therefore not be supported by the available validation evidence.

Q: Does the overfitting explain the deployment gap?
A: It is a contributing limitation, but not necessarily the complete explanation. Independent and live evaluation also introduce domain, microphone, speaker, phrasing, and acoustic differences, while the E40 confidence policy intentionally rejects uncertain commands. Therefore, the deployment gap should not be attributed solely to overfitting.

Q: Did E40 fix the overfitting?
A: No. E40 is a safety guardrail that maps classifier confidence to accept/reject behavior before action routing. It does not fix training overfitting. It suppresses uncertain classifications, which can reduce wrong actions but also reduces execution coverage.

Q: Are all E50 failures caused by overfitting?
A: No. The training history demonstrates overfitting after epoch 7, but epoch 7 was already selected as the final checkpoint. Command failures have multiple possible sources, including class confusion, training-data coverage, speaker/acoustic/domain variation, and confidence-based rejection. We attribute failures at the most specific layer supported by the evidence.

Q: Why can't you simply say overfitting caused the low live accuracy?
A: Because the live benchmark differs from the internal validation population in several ways, including speaker, acoustic, microphone, phrasing, and deployment conditions. The evidence demonstrates a generalization gap, but does not isolate its cause quantitatively.

Q: Give an example.
A: A high-confidence `TEMPERATURE -> WEATHER` prediction is a classifier confusion. It is not a threshold rejection. Conversely, a correct but below-threshold prediction is a safe rejection and should not automatically be classified as overfitting.
