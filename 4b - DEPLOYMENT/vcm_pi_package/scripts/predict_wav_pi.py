from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT))

from preprocessing.audio_io import load_audio  # noqa: E402
from preprocessing.log_mel import extract_log_mel  # noqa: E402
from training.baseline_features import load_preprocessing_configs  # noqa: E402
from training.cnn_model import build_tiny_cnn, load_cnn_config  # noqa: E402


DEFAULT_EXPERIMENT_ID = "E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT"
DEFAULT_CNN_CONFIG = "configs/cnn_fastbn_dense_nodropout_raw19.json"
DEFAULT_THRESHOLD = 0.90
DEFAULT_THRESHOLD_POLICY = "configs/e50_revised_vocab_e40_thresholds.json"


@dataclass(frozen=True)
class PredictionResult:
    wav_path: str
    predicted_intent: str
    confidence: float
    accepted: bool
    threshold: float
    threshold_policy: str
    top_k: list[tuple[str, float]]


def load_npz_weights(path: Path) -> list[np.ndarray]:
    data = np.load(path)
    keys = sorted(data.files, key=lambda key: int(key.split("_")[1]))
    return [data[key] for key in keys]


def load_labels(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    return [raw[str(idx)] for idx in range(len(raw))]


def load_threshold_policy(path: str | Path | None) -> dict[str, object] | None:
    if not path:
        return None
    policy_path = Path(path)
    if not policy_path.is_absolute():
        policy_path = PACKAGE_ROOT / policy_path
    with policy_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def threshold_for_label(
    label: str,
    *,
    global_threshold: float,
    threshold_policy: dict[str, object] | None,
) -> tuple[float, str]:
    if threshold_policy is None:
        return global_threshold, ""
    thresholds = threshold_policy.get("thresholds", {})
    if not isinstance(thresholds, dict):
        raise ValueError("Threshold policy must contain a 'thresholds' object.")
    default_threshold = float(threshold_policy.get("default_threshold", global_threshold))
    return float(thresholds.get(label, default_threshold)), str(
        threshold_policy.get("policy_id", "threshold_policy")
    )


def load_trained_model(experiment_id: str, cnn_config_path: str):
    try:
        import tensorflow as tf
    except ImportError as exc:
        raise SystemExit(
            "TensorFlow is required for Pi CNN inference. Install tensorflow or "
            "tensorflow-cpu in the Pi virtual environment before running this script."
        ) from exc

    tf.keras.utils.set_random_seed(42)
    cnn_config = load_cnn_config(PACKAGE_ROOT / cnn_config_path)
    labels = load_labels(PACKAGE_ROOT / "results" / "tables" / f"{experiment_id}_labels.json")
    cnn_config["num_classes"] = len(labels)
    model = build_tiny_cnn(cnn_config)
    weights_path = PACKAGE_ROOT / "models" / "cnn" / f"{experiment_id}_weights.npz"
    if not weights_path.exists():
        raise FileNotFoundError(f"Model weights not found: {weights_path}")
    model.set_weights(load_npz_weights(weights_path))
    return model


def wav_to_model_input(wav_path: Path, experiment_id: str) -> np.ndarray:
    audio_config, log_mel_config = load_preprocessing_configs(
        PACKAGE_ROOT / "configs" / "preprocessing.json"
    )
    audio = load_audio(wav_path, audio_config)
    log_mel = extract_log_mel(audio, log_mel_config)[..., np.newaxis]
    x = log_mel[np.newaxis, ...].astype(np.float32)

    normalization_path = PACKAGE_ROOT / "models" / "cnn" / f"{experiment_id}_normalization.npz"
    if normalization_path.exists():
        normalization = np.load(normalization_path)
        x = (x - normalization["mean"]) / normalization["std"]
    return x.astype(np.float32)


class VcmPredictor:
    """Reusable predictor that loads the CNN, labels, and threshold policy once."""

    def __init__(
        self,
        *,
        experiment_id: str = DEFAULT_EXPERIMENT_ID,
        cnn_config_path: str = DEFAULT_CNN_CONFIG,
        threshold: float = DEFAULT_THRESHOLD,
        threshold_policy_path: str = DEFAULT_THRESHOLD_POLICY,
    ) -> None:
        self.experiment_id = experiment_id
        self.cnn_config_path = cnn_config_path
        self.threshold = threshold
        self.model = load_trained_model(experiment_id, cnn_config_path)
        self.labels = load_labels(PACKAGE_ROOT / "results" / "tables" / f"{experiment_id}_labels.json")
        self.threshold_policy = load_threshold_policy(threshold_policy_path)

    def predict(self, wav_path: str | Path, *, top_k: int = 3) -> PredictionResult:
        wav_path = Path(wav_path)
        x = wav_to_model_input(wav_path, self.experiment_id)
        probabilities = self.model(x, training=False).numpy()[0]
        order = np.argsort(probabilities)[::-1]
        best_idx = int(order[0])
        confidence = float(probabilities[best_idx])
        predicted_label = self.labels[best_idx]
        applied_threshold, policy_id = threshold_for_label(
            predicted_label,
            global_threshold=self.threshold,
            threshold_policy=self.threshold_policy,
        )
        ranked = [(self.labels[int(idx)], float(probabilities[int(idx)])) for idx in order[:top_k]]
        return PredictionResult(
            wav_path=str(wav_path),
            predicted_intent=predicted_label,
            confidence=confidence,
            accepted=confidence >= applied_threshold,
            threshold=applied_threshold,
            threshold_policy=policy_id,
            top_k=ranked,
        )


def predict_wav(
    wav_path: str | Path,
    *,
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    cnn_config_path: str = DEFAULT_CNN_CONFIG,
    threshold: float = DEFAULT_THRESHOLD,
    threshold_policy_path: str = DEFAULT_THRESHOLD_POLICY,
    top_k: int = 3,
) -> PredictionResult:
    predictor = VcmPredictor(
        experiment_id=experiment_id,
        cnn_config_path=cnn_config_path,
        threshold=threshold,
        threshold_policy_path=threshold_policy_path,
    )
    return predictor.predict(wav_path, top_k=top_k)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Predict VCM intent from local WAV files on Pi.")
    parser.add_argument("wav_paths", nargs="+", help="One or more PCM WAV files.")
    parser.add_argument("--experiment-id", default=DEFAULT_EXPERIMENT_ID)
    parser.add_argument("--cnn-config", default=DEFAULT_CNN_CONFIG)
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    parser.add_argument(
        "--threshold-policy",
        default=DEFAULT_THRESHOLD_POLICY,
        help=(
            "Optional JSON policy with per-label thresholds. When omitted, the "
            "global --threshold value is used."
        ),
    )
    parser.add_argument("--top-k", type=int, default=3)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = [
        asdict(
            predict_wav(
                wav_path,
                experiment_id=args.experiment_id,
                cnn_config_path=args.cnn_config,
                threshold=args.threshold,
                threshold_policy_path=args.threshold_policy,
                top_k=args.top_k,
            )
        )
        for wav_path in args.wav_paths
    ]
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
