# Package Manifest

Prepared: 2026-09-16
Updated: 2026-09-28

## Runtime Scripts

- `scripts/predict_wav_pi.py` - classify one or more WAV files.
- `scripts/pi_voice_control_demo.py` - record with `arecord`, classify, route a
  raw command to an action intent, and optionally apply a controlled GPIO
  action.
- `scripts/pi_wake_voice_control_demo.py` - final wake-gated E37+E50 runtime
  with `--cycles` and `--continuous` persistent-loop support. Models are loaded
  once at startup.
- `scripts/pi_led_test.py` - blink-test an LED on a selected BCM GPIO pin.
- `scripts/record_pi_calibration_set.py` - prompt through the full demo command
  list and record labelled Pi microphone calibration WAV files with a manifest.
- `scripts/benchmark_pi_inference.py` - measure inference latency, CPU, RAM,
  and temperature snapshots on the Pi.
- `scripts/run_phase_bn_audio_diagnostics.sh` - Phase BN audio-output diagnostic
  harness for `aplay`, `speaker-test`, and known response WAV playback.
- `scripts/run_phase_bn_prompted_trial.sh` - prompted one-trial wake-command
  validation wrapper for E37+E50.
- `scripts/run_phase_bn_audio_smoke.sh` - Phase BN smoke sequence after audio
  output is fixed.
- `scripts/run_phase_bn_all19_prompted_validation.sh` - prompted all-19 command
  validation wrapper. This is not a training or threshold-tuning script.
- `scripts/record_human_command_responses.py` - prompted Pi-side recorder for
  replacing placeholder response tones with one human voice WAV per command.
- `scripts/verify_human_command_responses.py` - response WAV format/duration
  verifier that flags likely placeholder tones.
- `scripts/vcm_touchscreen_gui.py` - native Tkinter touchscreen controller for
  START, STOP, and status display. It launches the existing E37+E50 wake-wait
  runtime and does not contain recognition logic.
- `scripts/run_vcm_touchscreen_gui.sh` - Pi launcher for the touchscreen GUI.
- `vcm_touchscreen_gui.desktop` - optional desktop shortcut template for the Pi.
- `scripts/run_phase_bn_close_touchscreen_gui_validation.sh` - Pi-side
  touchscreen validation launcher using wake-wait listening, HDMI0 response
  playback, and post-run CSV/JSON evidence summarization.
- `scripts/run_phase_bn_close_deployment_audit.sh` - Pi-side package/path/SHA
  audit for final closeout evidence.
- `scripts/run_phase_bn_close_response_playback.sh` - Pi-side per-response WAV
  playback audit using the selected ALSA response device.
- `scripts/run_phase_bn_close_persistent_loop.sh` - Pi-side same-process
  repeated-cycle runtime test wrapper.
- `scripts/run_phase_bn_close_wake_wait_demo.sh` - Pi-side continuous demo
  wrapper that keeps recording wake windows indefinitely until `hey pi` is
  accepted before opening the command window.
- `scripts/run_phase_bn_close_performance_probe.sh` - Pi-side E50 latency,
  CPU, RAM, and temperature benchmark wrapper using saved command WAVs.

## Action Layer

- `actions/command_actions.py` - maps accepted intent predictions to local
  actions or safe dry-run stubs.
- `actions/raw_command_router.py` - maps raw command labels such as `LIGHT_ON`,
  `LIGHT_OFF`, `NEXT`, and `PAUSE` into broad assignment intents plus slots.
- `actions/ACTION_LAYER_DESIGN.md` - documents supported intents, slots, and
  current deployment limitations.
- `music/README_MUSIC.md` - placeholder folder for local offline WAV demo files.
- `responses/` - original local WAV response assets for demo feedback.
- `responses_original_pre_boost_20260929/` - preserved pre-boost copies of the
  original response WAVs.
- `responses_boosted/` - peak-normalized boosted response WAVs used by the
  rejected interim response map.
- `responses_extra_loud_20260929/` - Pi-working extra-loud response WAVs used
  by the active response map.
- `PHASE_BN_CLOSE_RESPONSE_BOOST_MANIFEST_20260929.csv` - per-file response
  boost manifest with source, backup, boosted path, gain, peak, and SHA256.

## Configuration

- `configs/preprocessing.json` - 16 kHz mono, 4-second, log-Mel feature setup.
- `configs/cnn_fastbn_dense_nodropout.json` - CNN architecture used by E21/E23.
- `configs/cnn_fastbn_dense_nodropout_raw19.json` - 19-label raw-command CNN
  architecture used by E24.
- `configs/e24_pi_guardrail_thresholds.json` - optional per-label threshold
  policy for E24.
- `configs/e26_pi_guardrail_thresholds.json` - optional per-label threshold
  policy for E26.
- `configs/e27_pi_guardrail_thresholds.json` - default per-label threshold
  policy for E27.
- `configs/e28_pi_guardrail_thresholds.json` - default per-label threshold
  policy for E28.
- `configs/e33_pi_guardrail_thresholds.json` - historical per-label threshold
  policy for E33.
- `configs/e50_revised_vocab_e40_thresholds.json` - final command guardrail
  policy for E50, copied from frozen E40 behavior for the revised vocabulary.
- `configs/demo_response_assets.json` - local response WAV map for all 19
  command labels plus UNKNOWN/rejection feedback. As of 2026-09-29 it points to
  `responses_extra_loud_20260929/*_extra_loud.wav`; originals remain preserved
  separately.

## Models

- `models/cnn/E33_PI_COLOR_LIGHTON_RESPONSIVENESS_weights.npz`
- `models/cnn/E33_PI_COLOR_LIGHTON_RESPONSIVENESS_normalization.npz`
- `models/cnn/E28_PI_LIVE_NEXT_COLOR_RECOVERY_PROBE_weights.npz`
- `models/cnn/E28_PI_LIVE_NEXT_COLOR_RECOVERY_PROBE_normalization.npz`
- `models/cnn/E27_PI_LIVE_NEXT_COLOR_RECOVERY_PROBE_weights.npz`
- `models/cnn/E27_PI_LIVE_NEXT_COLOR_RECOVERY_PROBE_normalization.npz`
- `models/cnn/E26_PI_FRESH_NEXT_COLOR_RECOVERY_PROBE_weights.npz`
- `models/cnn/E26_PI_FRESH_NEXT_COLOR_RECOVERY_PROBE_normalization.npz`
- `models/cnn/E24_PI_RAW_COMMAND_RECOVERY_PROBE_weights.npz`
- `models/cnn/E24_PI_RAW_COMMAND_RECOVERY_PROBE_normalization.npz`
- `models/cnn/E23_LIGHT_REALMIC_ADAPT_E21_REPLAY_weights.npz`
- `models/cnn/E23_LIGHT_REALMIC_ADAPT_E21_REPLAY_normalization.npz`
- `models/cnn/E21_CNN_DENSE_NODROPOUT_1000PI_BESTVAL_weights.npz`
- `models/cnn/E21_CNN_DENSE_NODROPOUT_1000PI_BESTVAL_normalization.npz`
- Final Phase BM stack:
  - `models/cnn/E37_TARGETED_COLOR_VOLUME_FIX_weights.npz`
  - `models/cnn/E37_TARGETED_COLOR_VOLUME_FIX_normalization.npz`
  - `models/cnn/E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT_weights.npz`
  - `models/cnn/E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT_normalization.npz`

## Labels and Evidence

- `results/tables/E33_PI_COLOR_LIGHTON_RESPONSIVENESS_labels.json`
- `results/tables/E33_PI_COLOR_LIGHTON_RESPONSIVENESS_metrics.json`
- `results/tables/E33_PI_COLOR_LIGHTON_RESPONSIVENESS_E33_GUARDRAIL_HOLDOUT_metrics.json`
- `results/tables/E33_PI_COLOR_LIGHTON_RESPONSIVENESS_E33_GUARDRAIL_RECOVERY_metrics.json`
- `results/tables/E28_PI_LIVE_NEXT_COLOR_RECOVERY_PROBE_labels.json`
- `results/tables/E28_PI_LIVE_NEXT_COLOR_RECOVERY_PROBE_metrics.json`
- `results/tables/E28_PI_LIVE_NEXT_COLOR_RECOVERY_PROBE_fresh_miniset_predictions.csv`
- `results/tables/E28_PI_LIVE_NEXT_COLOR_RECOVERY_PROBE_E28_GUARDRAIL_HOLDOUT_metrics.json`
- `results/tables/E28_PI_LIVE_NEXT_COLOR_RECOVERY_PROBE_E28_GUARDRAIL_RECOVERY_metrics.json`
- `results/tables/E27_PI_LIVE_NEXT_COLOR_RECOVERY_PROBE_labels.json`
- `results/tables/E27_PI_LIVE_NEXT_COLOR_RECOVERY_PROBE_metrics.json`
- `results/tables/E27_PI_LIVE_NEXT_COLOR_RECOVERY_PROBE_fresh_miniset_predictions.csv`
- `results/tables/E27_PI_LIVE_NEXT_COLOR_RECOVERY_PROBE_E27_GUARDRAIL_HOLDOUT_metrics.json`
- `results/tables/E27_PI_LIVE_NEXT_COLOR_RECOVERY_PROBE_E27_GUARDRAIL_RECOVERY_metrics.json`
- `results/tables/E26_PI_FRESH_NEXT_COLOR_RECOVERY_PROBE_labels.json`
- `results/tables/E26_PI_FRESH_NEXT_COLOR_RECOVERY_PROBE_metrics.json`
- `results/tables/E26_PI_FRESH_NEXT_COLOR_RECOVERY_PROBE_fresh_miniset_predictions.csv`
- `results/tables/E26_PI_FRESH_NEXT_COLOR_RECOVERY_PROBE_E26_GUARDRAIL_FRESH_metrics.json`
- `results/tables/E26_PI_FRESH_NEXT_COLOR_RECOVERY_PROBE_E26_GUARDRAIL_HOLDOUT_metrics.json`
- `results/tables/E24_PI_RAW_COMMAND_RECOVERY_PROBE_labels.json`
- `results/tables/E24_PI_RAW_COMMAND_RECOVERY_PROBE_metrics.json`
- `results/tables/E24_PI_RAW_COMMAND_RECOVERY_PROBE_pi_holdout_predictions.csv`
- `results/tables/E23_LIGHT_REALMIC_ADAPT_E21_REPLAY_labels.json`
- `results/tables/E23_LIGHT_REALMIC_ADAPT_E21_REPLAY_metrics.json`
- `results/tables/E23_LIGHT_REALMIC_ADAPT_E21_REPLAY_official_validation_report.txt`
- `results/tables/E23_LIGHT_REALMIC_ADAPT_E21_REPLAY_realmic_light_holdout_predictions.csv`
- `results/tables/E21_vs_E23_realmic_light_holdout_20_comparison.csv`
- `results/tables/E21_CNN_DENSE_NODROPOUT_1000PI_BESTVAL_labels.json`

## Runtime Code

- `preprocessing/` - WAV loading, resampling, padding/trimming, log-Mel feature
  extraction.
- `training/baseline_features.py` - config loader reused for inference.
- `training/cnn_model.py` - CNN architecture builder.
- `actions/` - local raw-command routing and intent-to-action controller.
- `music/` - optional local WAV files for offline media demo.
- `scripts/record_pi_wake_set.py` - records fresh `WAKE` and `UNKNOWN`
  examples for the `hey pi` wake-gated demo.
- `scripts/pi_wake_voice_control_demo.py` - two-stage live demo that requires
  accepted `WAKE` before command classification/action.
- `scripts/vcm_touchscreen_gui.py` - local touchscreen control/status wrapper
  around `pi_wake_voice_control_demo.py`; by default it passes
  `--wait-for-wake` so the GUI returns to indefinite wake listening after each
  response.
- `models/cnn/E37_TARGETED_COLOR_VOLUME_FIX_*` and
  `models/cnn/E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT_*` - selected
  Phase BH wake/command package artifacts for the next Pi validation pass.
- `configs/e50_revised_vocab_e40_thresholds.json` - frozen E40-compatible
  command guardrail policy for the revised E50 `LIGHT_DIM` vocabulary.
- `scripts/benchmark_pi_inference.py` - Pi latency/RAM/CPU/temp benchmark.

## Final Runtime Choice

- Wake experiment: `E37_TARGETED_COLOR_VOLUME_FIX`.
- Command experiment: `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT`.
- Default CNN config: `configs/cnn_fastbn_dense_nodropout_raw19.json`.
- Wake threshold: `0.90`.
- Command default threshold: `0.90`.
- Command guardrail policy: `configs/e50_revised_vocab_e40_thresholds.json`.
- Reason: E50 is the final Phase BM baseline. E52 improved raw Phase
  AV-compatible accuracy but increased accepted-wrong actions and was rejected.
- Evidence: E50 current95-compatible `83/90`, Phase AV-compatible `139/194`,
  BI live wake `36/36`, BI accepted-correct `15`, BI accepted-wrong `1`.
- Caveat: final physical demo validation is now in Phase BN. All 19 commands
  remain callable/testable; the defensible demo subset is a safety/evidence
  decision only, not a runtime whitelist. `TIME`, `BRIGHTNESS`, `TEMPERATURE`,
  `VOLUME_UP`, `VOLUME_DOWN`, and `CALL` remain callable but not currently
  demo-ready. `TEMPERATURE` is callable but unsafe/not demo-ready due to
  accepted-wrong live evidence.
