from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from preprocessing.audio_io import AudioConfig, load_audio  # noqa: E402
from preprocessing.log_mel import LogMelConfig, extract_log_mel  # noqa: E402
from training.baseline_features import load_index, load_preprocessing_configs  # noqa: E402
from training.cnn_model import build_tiny_cnn  # noqa: E402


DEFAULT_MANIFEST = (
    PROJECT_ROOT
    / "data"
    / "calibration"
    / "pi_validation"
    / "all_commands_calibration_15x"
    / "manifest.csv"
)
DEFAULT_BASE_EXPERIMENT_ID = "E23_LIGHT_REALMIC_ADAPT_E21_REPLAY"
DEFAULT_EXPERIMENT_ID = "E24_PI_RAW_COMMAND_RECOVERY"
DEFAULT_CNN_CONFIG = "configs/cnn_fastbn_dense_nodropout.json"

RAW_TO_DEMO_LABEL = {
    "ALARM": "ALARM",
    "CALL": "CALL",
    "DIM_DOWN": "BRIGHTNESS",
    "DIM_UP": "BRIGHTNESS",
    "LIGHT_OFF": "LIGHT_OFF",
    "LIGHT_ON": "LIGHT_ON",
    "LIST_REMINDERS": "LIST_REMINDERS",
    "MESSAGE": "MESSAGE",
    "NEXT": "NEXT",
    "PAUSE": "PAUSE",
    "PLAY_MUSIC": "PLAY_MUSIC",
    "SET_REMINDER": "CREATE_REMINDER",
    "STOP": "STOP",
    "TEMP_DOWN": "TEMPERATURE",
    "TEMP_UP": "TEMPERATURE",
    "TIME": "TIME",
    "TIMER": "TIMER",
    "VOLUME_DOWN": "VOLUME_DOWN",
    "VOLUME_UP": "VOLUME_UP",
    "WEATHER": "WEATHER",
}


@dataclass(frozen=True)
class RawExample:
    wav_path: Path
    label: str
    source: str
    source_raw_label: str
    split: str
    phrase: str = ""
    expected_intent: str = ""
    action_hint: str = ""
    trial: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Train a Pi-adapted raw-command model for demo action routing. "
            "Output labels are the 19 demo commands from the Pi calibration manifest."
        )
    )
    parser.add_argument("--experiment-id", default=DEFAULT_EXPERIMENT_ID)
    parser.add_argument("--base-experiment-id", default=DEFAULT_BASE_EXPERIMENT_ID)
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument(
        "--extra-manifest",
        action="append",
        default=[],
        help="Additional Pi calibration manifest to merge into this training run.",
    )
    parser.add_argument("--cnn-config", default=DEFAULT_CNN_CONFIG)
    parser.add_argument("--epochs", type=int, default=45)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--replay-per-raw-label", type=int, default=120)
    parser.add_argument("--pi-repeat", type=int, default=20)
    parser.add_argument(
        "--finalize-only",
        action="store_true",
        help=(
            "Load an already-saved model for this experiment and write holdout "
            "predictions/metrics without retraining."
        ),
    )
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=None,
        help="Optional learning-rate override for fine-tuning from an existing checkpoint.",
    )
    parser.add_argument("--seed", type=int, default=4242)
    return parser.parse_args()


def load_cnn_config_for_num_classes(path: Path, num_classes: int) -> dict:
    with path.open("r", encoding="utf-8") as f:
        config = json.load(f)
    if config["input_shape"] != [398, 40, 1]:
        raise ValueError(f"Unexpected CNN input shape: {config['input_shape']}")
    config["num_classes"] = num_classes
    return config


def read_manifest(manifest_path: Path) -> list[dict[str, str]]:
    with manifest_path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def resolve_pi_wav_path(manifest_path: Path, row: dict[str, str]) -> Path:
    raw_wav_path = Path(row["wav_path"])
    candidates = []
    if raw_wav_path.is_absolute():
        candidates.append(raw_wav_path)
    else:
        candidates.extend(
            [
                manifest_path.parent / row["label"] / raw_wav_path.name,
                manifest_path.parent / raw_wav_path,
                PROJECT_ROOT / raw_wav_path,
                PROJECT_ROOT / "deployment" / "vcm_pi_package" / raw_wav_path,
            ]
        )
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    candidate = manifest_path.parent / row["label"] / Path(row["wav_path"]).name
    if candidate.exists():
        return candidate.resolve()
    checked = ", ".join(str(path) for path in candidates)
    raise FileNotFoundError(f"Could not resolve Pi WAV: {row['wav_path']}; checked {checked}")


def pi_examples(manifest_path: Path, split: str) -> list[RawExample]:
    examples = []
    for row in read_manifest(manifest_path):
        if row["split"] != split:
            continue
        examples.append(
            RawExample(
                wav_path=resolve_pi_wav_path(manifest_path, row),
                label=row["label"],
                source="pi_calibration",
                source_raw_label=row["label"],
                split=row["split"],
                phrase=row["phrase"],
                expected_intent=row["expected_intent"],
                action_hint=row["action_hint"],
                trial=row["trial"],
            )
        )
    return examples


def replay_examples(target_labels: set[str], per_raw_label: int, seed: int) -> list[RawExample]:
    if per_raw_label <= 0:
        return []
    rows = [row for row in load_index(PROJECT_ROOT / "data" / "metadata" / "active_dataset_index.csv") if row.split == "train"]
    grouped: dict[str, list] = defaultdict(list)
    for row in rows:
        if row.raw_label not in RAW_TO_DEMO_LABEL:
            continue
        label = RAW_TO_DEMO_LABEL[row.raw_label]
        if label in target_labels:
            grouped[row.raw_label].append(row)

    rng = np.random.default_rng(seed)
    examples: list[RawExample] = []
    for raw_label in sorted(grouped):
        raw_rows = grouped[raw_label]
        order = rng.permutation(len(raw_rows))
        for idx in order[:per_raw_label]:
            row = raw_rows[int(idx)]
            examples.append(
                RawExample(
                    wav_path=PROJECT_ROOT / row.relative_path,
                    label=RAW_TO_DEMO_LABEL[row.raw_label],
                    source="source_replay",
                    source_raw_label=row.raw_label,
                    split=row.split,
                    expected_intent=row.assignment_intent,
                )
            )
    return examples


def load_npz_weights(path: Path) -> list[np.ndarray]:
    data = np.load(path)
    keys = sorted(data.files, key=lambda key: int(key.split("_")[1]))
    return [data[key] for key in keys]


def write_history(path: Path, history: dict[str, list[float]]) -> None:
    keys = sorted(history)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["epoch", *keys])
        for epoch_idx in range(len(next(iter(history.values()), []))):
            writer.writerow([epoch_idx + 1, *[history[key][epoch_idx] for key in keys]])


def macro_precision_recall_f1(y_true: np.ndarray, y_pred: np.ndarray) -> tuple[float, float, float]:
    labels = sorted(set(y_true.tolist()) | set(y_pred.tolist()))
    precisions = []
    recalls = []
    f1_scores = []
    for label in labels:
        true_positive = int(np.sum((y_true == label) & (y_pred == label)))
        false_positive = int(np.sum((y_true != label) & (y_pred == label)))
        false_negative = int(np.sum((y_true == label) & (y_pred != label)))
        precision = true_positive / (true_positive + false_positive) if true_positive + false_positive else 0.0
        recall = true_positive / (true_positive + false_negative) if true_positive + false_negative else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        precisions.append(precision)
        recalls.append(recall)
        f1_scores.append(f1)
    return float(np.mean(precisions)), float(np.mean(recalls)), float(np.mean(f1_scores))


def compute_metrics(tf, labels: np.ndarray, probabilities: np.ndarray) -> dict[str, float]:
    predictions = np.argmax(probabilities, axis=1)
    validation_loss = tf.keras.losses.sparse_categorical_crossentropy(
        labels,
        probabilities,
    ).numpy()
    precision_macro, recall_macro, f1_macro = macro_precision_recall_f1(labels, predictions)
    return {
        "loss": float(np.mean(validation_loss)),
        "accuracy": float(np.mean(predictions == labels)),
        "precision_macro": precision_macro,
        "recall_macro": recall_macro,
        "f1_macro": f1_macro,
    }


def build_tensor(
    examples: list[RawExample],
    audio_config: AudioConfig,
    log_mel_config: LogMelConfig,
) -> np.ndarray:
    features = []
    for example in examples:
        audio = load_audio(example.wav_path, audio_config)
        log_mel = extract_log_mel(audio, log_mel_config)
        features.append(log_mel[..., np.newaxis])
    return np.stack(features).astype(np.float32)


def initialize_from_base_model(model, base_experiment_id: str) -> int:
    base_weights_path = PROJECT_ROOT / "models" / "cnn" / f"{base_experiment_id}_weights.npz"
    if not base_weights_path.exists():
        return 0

    base_weights = load_npz_weights(base_weights_path)
    new_weights = model.get_weights()
    merged_weights = []
    copied = 0
    for new_weight, base_weight in zip(new_weights, base_weights):
        if new_weight.shape == base_weight.shape:
            merged_weights.append(base_weight)
            copied += 1
        else:
            merged_weights.append(new_weight)
    merged_weights.extend(new_weights[len(merged_weights) :])
    model.set_weights(merged_weights)
    return copied


def encode_labels(examples: list[RawExample], labels: list[str]) -> np.ndarray:
    label_to_id = {label: idx for idx, label in enumerate(labels)}
    return np.array([label_to_id[example.label] for example in examples], dtype=np.int64)


def load_saved_labels(path: Path, fallback: list[str]) -> list[str]:
    if not path.exists():
        return fallback
    with path.open("r", encoding="utf-8") as f:
        label_map = json.load(f)
    return [label_map[str(idx)] for idx in range(len(label_map))]


def write_predictions(
    path: Path,
    examples: list[RawExample],
    labels: list[str],
    probabilities: np.ndarray,
    threshold: float,
) -> dict[str, object]:
    predictions = np.argmax(probabilities, axis=1)
    confidences = np.max(probabilities, axis=1)
    correct = predictions == encode_labels(examples, labels)
    accepted = confidences >= threshold
    path.parent.mkdir(parents=True, exist_ok=True)

    def display_path(wav_path: Path) -> str:
        resolved = wav_path.resolve()
        try:
            return str(resolved.relative_to(PROJECT_ROOT))
        except ValueError:
            return str(wav_path)

    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "wav_path",
                "label",
                "expected_intent",
                "phrase",
                "action_hint",
                "trial",
                "predicted_label",
                "confidence",
                "accepted",
                "correct",
            ]
        )
        for example, pred_idx, confidence, is_accepted, is_correct in zip(
            examples, predictions, confidences, accepted, correct
        ):
            writer.writerow(
                [
                    display_path(example.wav_path),
                    example.label,
                    example.expected_intent,
                    example.phrase,
                    example.action_hint,
                    example.trial,
                    labels[int(pred_idx)],
                    f"{float(confidence):.6f}",
                    str(bool(is_accepted)).lower(),
                    str(bool(is_correct)).lower(),
                ]
            )

    per_label = {}
    for label in labels:
        indices = [idx for idx, example in enumerate(examples) if example.label == label]
        if not indices:
            continue
        label_correct = int(np.sum(correct[indices]))
        label_accepted = int(np.sum(accepted[indices]))
        label_wrong_accepted = int(np.sum(accepted[indices] & ~correct[indices]))
        predicted_counts = Counter(labels[int(predictions[idx])] for idx in indices)
        per_label[label] = {
            "total": len(indices),
            "correct": label_correct,
            "accuracy": label_correct / len(indices),
            "accepted": label_accepted,
            "wrong_accepted": label_wrong_accepted,
            "predicted_counts": dict(sorted(predicted_counts.items())),
        }

    return {
        "examples": len(examples),
        "accuracy": float(np.mean(correct)),
        "accepted": int(np.sum(accepted)),
        "accepted_correct": int(np.sum(accepted & correct)),
        "accepted_wrong": int(np.sum(accepted & ~correct)),
        "rejected": int(np.sum(~accepted)),
        "per_label": per_label,
    }


def main() -> None:
    try:
        import tensorflow as tf
    except ImportError as exc:
        raise SystemExit("TensorFlow is required for raw-command recovery training.") from exc

    args = parse_args()
    tf.keras.utils.set_random_seed(args.seed)

    manifest_paths = [Path(args.manifest), *[Path(path) for path in args.extra_manifest]]
    pi_adaptation: list[RawExample] = []
    pi_holdout: list[RawExample] = []
    for manifest_path in manifest_paths:
        pi_adaptation.extend(pi_examples(manifest_path, "adaptation"))
        pi_holdout.extend(pi_examples(manifest_path, "holdout"))
    labels = sorted({example.label for example in pi_adaptation + pi_holdout})

    model_dir = PROJECT_ROOT / "models" / "cnn"
    table_dir = PROJECT_ROOT / "results" / "tables"
    model_dir.mkdir(parents=True, exist_ok=True)
    table_dir.mkdir(parents=True, exist_ok=True)

    weights_path = model_dir / f"{args.experiment_id}_weights.npz"
    normalization_path = model_dir / f"{args.experiment_id}_normalization.npz"
    labels_path = table_dir / f"{args.experiment_id}_labels.json"

    if args.finalize_only:
        labels = load_saved_labels(labels_path, labels)
        audio_config, log_mel_config = load_preprocessing_configs(
            PROJECT_ROOT / "configs" / "preprocessing.json"
        )
        cnn_config = load_cnn_config_for_num_classes(PROJECT_ROOT / args.cnn_config, len(labels))
        model = build_tiny_cnn(cnn_config)
        if not weights_path.exists():
            raise SystemExit(f"Missing saved weights for --finalize-only: {weights_path}")
        if not normalization_path.exists():
            raise SystemExit(f"Missing saved normalization for --finalize-only: {normalization_path}")
        model.set_weights(load_npz_weights(weights_path))
        normalization = np.load(normalization_path)

        print(f"Finalize-only mode for {args.experiment_id}")
        print(f"Labels: {len(labels)}")
        print(f"Pi holdout clips: {len(pi_holdout)}")
        print("Preparing Pi holdout tensor...")
        x_val = build_tensor(pi_holdout, audio_config, log_mel_config)
        y_val = encode_labels(pi_holdout, labels)
        x_val = (x_val - normalization["mean"]) / normalization["std"]
        holdout_probabilities = model(x_val, training=False).numpy()
        final_metrics = compute_metrics(tf, y_val, holdout_probabilities)
        prediction_summary = write_predictions(
            table_dir / f"{args.experiment_id}_pi_holdout_predictions.csv",
            pi_holdout,
            labels,
            holdout_probabilities,
            threshold=0.90,
        )
        metrics = {
            "experiment_id": args.experiment_id,
            "model": "tiny_vcm_cnn_raw_command",
            "finalize_only": True,
            "labels": labels,
            "pi_adaptation_clips": len(pi_adaptation),
            "pi_holdout_examples": len(pi_holdout),
            "validation_metrics": final_metrics,
            "holdout_threshold_0_90": prediction_summary,
            "model_path": str(weights_path),
            "normalization_path": str(normalization_path),
        }
        with (table_dir / f"{args.experiment_id}_metrics.json").open("w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2)
            f.write("\n")
        print(json.dumps(metrics, indent=2))
        return

    replay = replay_examples(set(labels), args.replay_per_raw_label, args.seed)
    train_examples = replay + [example for example in pi_adaptation for _ in range(args.pi_repeat)]

    rng = np.random.default_rng(args.seed)
    order = rng.permutation(len(train_examples))
    train_examples = [train_examples[int(idx)] for idx in order]

    audio_config, log_mel_config = load_preprocessing_configs(
        PROJECT_ROOT / "configs" / "preprocessing.json"
    )
    cnn_config = load_cnn_config_for_num_classes(PROJECT_ROOT / args.cnn_config, len(labels))
    if args.learning_rate is not None:
        cnn_config["learning_rate"] = args.learning_rate
    model = build_tiny_cnn(cnn_config)
    copied_weights = initialize_from_base_model(model, args.base_experiment_id)

    print(f"Labels: {len(labels)}")
    print(f"Manifest files: {[str(path) for path in manifest_paths]}")
    print(f"Pi adaptation clips: {len(pi_adaptation)} x repeat {args.pi_repeat}")
    print(f"Replay clips: {len(replay)}")
    print(f"Training examples after repeat/replay: {len(train_examples)}")
    print(f"Pi holdout clips: {len(pi_holdout)}")
    print(f"Copied compatible base weights: {copied_weights}")
    print(f"Training label counts: {dict(sorted(Counter(e.label for e in train_examples).items()))}")

    print("Preparing train tensor...")
    x_train = build_tensor(train_examples, audio_config, log_mel_config)
    y_train = encode_labels(train_examples, labels)
    print("Preparing Pi holdout tensor...")
    x_val = build_tensor(pi_holdout, audio_config, log_mel_config)
    y_val = encode_labels(pi_holdout, labels)

    feature_mean = x_train.mean(axis=(0, 1), keepdims=True)
    feature_std = x_train.std(axis=(0, 1), keepdims=True) + 1e-6
    x_train = (x_train - feature_mean) / feature_std
    x_val = (x_val - feature_mean) / feature_std

    optimizer = tf.keras.optimizers.Adam(learning_rate=float(cnn_config.get("learning_rate", 1e-3)))
    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy()
    history = {"accuracy": [], "loss": [], "val_accuracy": [], "val_loss": [], "val_f1_macro": []}
    best_weights = None
    best_epoch = None
    best_metrics = None

    for epoch_idx in range(args.epochs):
        epoch_order = np.random.default_rng(args.seed + epoch_idx).permutation(len(x_train))
        losses = []
        correct = 0
        total = 0
        for start in range(0, len(epoch_order), args.batch_size):
            batch_indices = epoch_order[start : start + args.batch_size]
            x_batch = x_train[batch_indices]
            y_batch = y_train[batch_indices]
            with tf.GradientTape() as tape:
                probs = model(x_batch, training=True)
                loss = loss_fn(y_batch, probs)
            gradients = tape.gradient(loss, model.trainable_variables)
            optimizer.apply_gradients(zip(gradients, model.trainable_variables))

            losses.append(float(loss.numpy()))
            preds = np.argmax(probs.numpy(), axis=1)
            correct += int(np.sum(preds == y_batch))
            total += len(y_batch)

        train_acc = correct / total
        val_probs = model(x_val, training=False).numpy()
        val_metrics = compute_metrics(tf, y_val, val_probs)
        history["loss"].append(float(np.mean(losses)))
        history["accuracy"].append(float(train_acc))
        history["val_loss"].append(val_metrics["loss"])
        history["val_accuracy"].append(val_metrics["accuracy"])
        history["val_f1_macro"].append(val_metrics["f1_macro"])

        if best_metrics is None or val_metrics["f1_macro"] > best_metrics["f1_macro"]:
            best_metrics = val_metrics
            best_weights = model.get_weights()
            best_epoch = epoch_idx + 1

        print(
            f"Epoch {epoch_idx + 1}/{args.epochs} - "
            f"accuracy: {train_acc:.4f} - loss: {np.mean(losses):.4f} - "
            f"val_accuracy: {val_metrics['accuracy']:.4f} - "
            f"val_f1_macro: {val_metrics['f1_macro']:.4f}"
        )

    if best_weights is not None:
        model.set_weights(best_weights)
        print(f"Restored best Pi holdout weights from epoch {best_epoch}.")

    holdout_probabilities = model(x_val, training=False).numpy()
    final_metrics = compute_metrics(tf, y_val, holdout_probabilities)

    np.savez_compressed(
        weights_path, **{f"weight_{idx}": value for idx, value in enumerate(model.get_weights())}
    )
    np.savez_compressed(normalization_path, mean=feature_mean, std=feature_std)
    write_history(table_dir / f"{args.experiment_id}_history.csv", history)
    with (table_dir / f"{args.experiment_id}_labels.json").open("w", encoding="utf-8") as f:
        json.dump({str(idx): label for idx, label in enumerate(labels)}, f, indent=2)
        f.write("\n")

    prediction_summary = write_predictions(
        table_dir / f"{args.experiment_id}_pi_holdout_predictions.csv",
        pi_holdout,
        labels,
        holdout_probabilities,
        threshold=0.90,
    )
    metrics = {
        "experiment_id": args.experiment_id,
        "model": "tiny_vcm_cnn_raw_command",
        "base_experiment_id": args.base_experiment_id,
        "copied_compatible_base_weights": copied_weights,
        "labels": labels,
        "pi_adaptation_clips": len(pi_adaptation),
        "pi_repeat": args.pi_repeat,
        "replay_clips": len(replay),
        "training_examples": len(train_examples),
        "pi_holdout_examples": len(pi_holdout),
        "replay_per_raw_label": args.replay_per_raw_label,
        "epochs_requested": args.epochs,
        "best_epoch": best_epoch,
        "best_validation_metrics": best_metrics,
        "validation_metrics": final_metrics,
        "holdout_threshold_0_90": prediction_summary,
        "model_path": str(weights_path),
        "normalization_path": str(normalization_path),
    }
    with (table_dir / f"{args.experiment_id}_metrics.json").open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
        f.write("\n")

    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
