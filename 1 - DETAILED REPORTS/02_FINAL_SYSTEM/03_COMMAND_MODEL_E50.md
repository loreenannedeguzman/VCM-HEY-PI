# Command Model E50

## Engineering Question

What exactly is the final command model, how was it trained, and what does it output?

E50 is the frozen post-wake command classifier. It receives the command audio after E37 wake acceptance, consumes log-Mel features, and predicts one of 19 fixed command labels. E50 does not transcribe speech, execute actions, choose thresholds, or decide GUI behavior.

## Frozen Identity

| Field | Value |
|---|---|
| Experiment ID | `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT` |
| Phase | BG |
| Architecture | E41 `tiny_vcm_cnn` |
| Initialization | mapped E41 initialization from `E41_FUNCTIONAL_NON_LED_RECOVERY` |
| Parameter count | 66,483 total; 66,147 trainable; 336 non-trainable |
| Weights artifact size | 251,734 bytes |
| MACs | 85,774,144 Conv2D/Dense MACs per 4-second input |
| Weights SHA-256 | `BC8AC64CED4305DDF43BF4DE377F3CC636A764EFF339CD9F92AF06340C50B8FF` |
| Normalization SHA-256 | `2D71873B6326D6552D7C5B1C22995FFD5132C357AAEC237CB85CBD7EF739283F` |

## Input Representation

| Field | Value |
|---|---:|
| Sample rate | 16,000 Hz |
| Target duration | 4.0 s |
| Approximate waveform length | 64,000 samples |
| Frame length | 25.0 ms |
| Frame step | 10.0 ms |
| FFT length | 512 |
| Mel bins | 40 |
| Frequency band | 20 Hz to 7,600 Hz |
| Log floor | `1e-6` |
| Normalization | Training-manifest global feature mean/std |
| Expected frames | 398 |
| Feature shape | `(398, 40)` |
| Model input shape | `(398, 40, 1)` |

The preprocessing turns each audio command into a compact time-frequency matrix. The CNN then learns local time-frequency patterns rather than words or transcripts.

## CNN Structure

The final model summary identifies `tiny_vcm_cnn` with this high-level structure:

```text
Input (398, 40, 1)
  -> Conv2D 24 + BatchNorm + MaxPool
  -> Conv2D 48 + BatchNorm + MaxPool
  -> Conv2D 96 + BatchNorm + MaxPool
  -> GlobalAveragePooling + GlobalMaxPooling
  -> Concatenate
  -> Dropout
  -> Dense 64
  -> Dropout
  -> Dense 19 output labels
```

The final output is a 19-class score vector. The highest-scoring label is the raw E50 prediction. That raw prediction still must pass E40 before it becomes an action.

## Final Vocabulary

`PLAY_MUSIC`, `WEATHER`, `TIME`, `LIGHT_ON`, `LIGHT_OFF`, `LIGHT_DIM`, `BRIGHTNESS`, `TIMER`, `ALARM`, `TEMPERATURE`, `NEXT`, `PAUSE`, `STOP`, `VOLUME_UP`, `VOLUME_DOWN`, `CREATE_REMINDER`, `LIST_REMINDERS`, `CALL`, `MESSAGE`.

`COLOR` is not a final E50 class. Final E50 uses `LIGHT_DIM`.

## Training Data Composition

The final E50 Phase BG training manifest contains 16,100 rows:

| Source branch | Rows | Role |
|---|---:|---|
| `active_project_dataset` | 13,070 | Main active-project command data; collective-derived/project-local branch. |
| `dataset2_vcm_balanced` | 2,800 | Selected VCM_BALANCED support rows. |
| `e41_reconstructed_adaptation` | 230 | Separate Pi deployment adaptation/calibration branch. |
| Total | 16,100 | Final E50 command-model training manifest. |

Data-kind composition is 15,260 real rows, 480 augmented rows, 200 real multi-sensor rows, and 160 synthetic rows. Most final labels have 900 rows; five labels have 700 rows where direct Dataset2 support was unavailable.

## Training Configuration

| Field | Value |
|---|---|
| Optimizer | Adam |
| Learning rate | 0.00075 |
| Batch size | 32 |
| Maximum epochs | 14 |
| Early stopping patience | 4 |
| Random seed | 5050 |
| Checkpoint selection | Best internal validation loss only; not selected using current95 or Phase AV |

The documented Phase BG/E50 evidence supports local Windows CPU-only TensorFlow training for the final command model, not A100 or external-cluster final E50 training.

## Final Performance Context

In the final physical Pi benchmark, raw command classification was 13/19 = 68.42%. After E40 confidence gating, 10/19 valid commands completed the end-to-end action path. Accepted-action precision was 10/10 = 100%, with 0 accepted-wrong actions. This means E50 alone should not be summarized by the accepted-action metric; E50 supplies the raw prediction, while E40 and the router determine whether it becomes an action.

## Known Limitations

E50 has moderate live command-level coverage in the final benchmark. The 20-trial Pi benchmark is not a broad speaker-independent acoustic population study. Dataset2 is 16-class while final E50 is 19-label, and some final labels rely on active-project/E41 material rather than direct Dataset2 coverage. The model is fixed-vocabulary and does not understand arbitrary speech.
