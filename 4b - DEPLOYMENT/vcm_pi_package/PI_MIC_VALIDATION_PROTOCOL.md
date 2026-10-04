# Raspberry Pi Microphone Validation Protocol

Run this when the Raspberry Pi 5 and microphone arrive.

## Goal

Verify whether the trained CNN behaves reliably with audio recorded on the
actual deployment microphone before connecting predictions to LED control.

## Model Under Test

- Primary: `E23_LIGHT_REALMIC_ADAPT_E21_REPLAY`
- Baseline reference if needed: `E21_CNN_DENSE_NODROPOUT_1000PI_BESTVAL`
- Acceptance threshold: start with `0.90`

## Collection Plan

Record a small held-out Pi-microphone validation set:

1. `turn on the light` - 10 recordings
2. `turn off the light` - 10 recordings
3. at least 3 non-light commands if time allows
4. at least 3 background/no-command clips if time allows

Keep each recording near 4 seconds. Speak naturally, with a short silence before
and after the phrase.

## Commands

Create folders:

```bash
mkdir -p pi_validation/light_on pi_validation/light_off pi_validation/non_light pi_validation/background
```

Record examples:

```bash
arecord -r 16000 -c 1 -f S16_LE -d 4 pi_validation/light_on/light_on_001.wav
arecord -r 16000 -c 1 -f S16_LE -d 4 pi_validation/light_off/light_off_001.wav
```

If needed, add the ALSA device:

```bash
arecord -D plughw:1,0 -r 16000 -c 1 -f S16_LE -d 4 pi_validation/light_on/light_on_001.wav
```

Predict:

```bash
python scripts/predict_wav_pi.py pi_validation/light_on/*.wav --threshold 0.90
python scripts/predict_wav_pi.py pi_validation/light_off/*.wav --threshold 0.90
python scripts/predict_wav_pi.py pi_validation/non_light/*.wav --threshold 0.90
python scripts/predict_wav_pi.py pi_validation/background/*.wav --threshold 0.90
```

## Decision Rule

Proceed to GPIO only if:

- most light commands are predicted as `LIGHT_CONTROL`;
- accepted predictions are not frequently wrong;
- non-light/background clips are rejected or not misread as `LIGHT_CONTROL`;
- the team understands that `LIGHT_CONTROL` is still an intent only, not an
  on/off slot.

If Pi-microphone performance is weak, collect more Pi-microphone examples before
LED integration. Do not add broad synthetic data unless the errors show a clear
pattern that synthetic augmentation can target.

## What To Log

For each WAV, log:

- filename
- phrase spoken
- expected intent
- predicted intent
- confidence
- accepted/rejected at threshold 0.90
- notes on distance/noise/microphone device

