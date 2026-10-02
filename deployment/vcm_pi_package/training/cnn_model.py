from __future__ import annotations

from pathlib import Path
import json
from typing import Any


def load_cnn_config(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as f:
        config = json.load(f)

    expected_input = [398, 40, 1]
    if config["input_shape"] != expected_input:
        raise ValueError(f"CNN input_shape must be {expected_input}, got {config['input_shape']}")
    if int(config["num_classes"]) < 2:
        raise ValueError("CNN num_classes must be at least 2.")
    return config


def build_tiny_cnn(config: dict[str, Any]):
    try:
        import tensorflow as tf
    except ImportError as exc:
        raise ImportError(
            "TensorFlow is required for CNN training. The current local Python "
            "environment does not have TensorFlow installed."
        ) from exc

    inputs = tf.keras.layers.Input(shape=tuple(config["input_shape"]))
    x = inputs

    for filters in config["conv_filters"]:
        x = tf.keras.layers.Conv2D(
            int(filters),
            tuple(config["kernel_size"]),
            activation="relu",
            padding="same",
        )(x)
        if bool(config.get("use_batch_norm", True)):
            x = tf.keras.layers.BatchNormalization(
                momentum=float(config.get("batch_norm_momentum", 0.99))
            )(x)
        x = tf.keras.layers.MaxPooling2D(tuple(config["pool_size"]))(x)

    pooling = str(config.get("pooling", "avg"))
    if pooling == "avg":
        x = tf.keras.layers.GlobalAveragePooling2D()(x)
    elif pooling == "max":
        x = tf.keras.layers.GlobalMaxPooling2D()(x)
    elif pooling == "avgmax":
        x = tf.keras.layers.Concatenate()(
            [
                tf.keras.layers.GlobalAveragePooling2D()(x),
                tf.keras.layers.GlobalMaxPooling2D()(x),
            ]
        )
    else:
        raise ValueError(f"Unsupported pooling mode: {pooling}")

    x = tf.keras.layers.Dropout(float(config["dropout"]))(x)
    dense_units = int(config.get("dense_units", 0))
    if dense_units > 0:
        x = tf.keras.layers.Dense(dense_units, activation="relu")(x)
        x = tf.keras.layers.Dropout(float(config.get("dense_dropout", config["dropout"])))(x)
    outputs = tf.keras.layers.Dense(int(config["num_classes"]), activation="softmax")(x)
    model = tf.keras.Model(inputs=inputs, outputs=outputs, name="tiny_vcm_cnn")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=float(config.get("learning_rate", 1e-3))),
        loss=config["loss"],
        metrics=list(config["metrics"]),
    )
    return model
