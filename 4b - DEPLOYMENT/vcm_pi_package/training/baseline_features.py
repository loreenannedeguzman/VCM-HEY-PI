from __future__ import annotations

import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np

from preprocessing.audio_io import AudioConfig, load_audio
from preprocessing.log_mel import LogMelConfig, extract_log_mel


@dataclass(frozen=True)
class DatasetRow:
    relative_path: str
    raw_label: str
    assignment_intent: str
    split: str


def load_preprocessing_configs(config_path: Path) -> tuple[AudioConfig, LogMelConfig]:
    with config_path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    audio_config = AudioConfig(
        sample_rate_hz=int(raw["sample_rate_hz"]),
        target_duration_sec=float(raw["target_duration_sec"]),
        normalize=str(raw.get("normalize", "peak")),
    )
    log_mel_config = LogMelConfig(
        sample_rate_hz=int(raw["sample_rate_hz"]),
        frame_length_ms=float(raw["frame_length_ms"]),
        frame_step_ms=float(raw["frame_step_ms"]),
        fft_length=int(raw["fft_length"]),
        mel_bins=int(raw["mel_bins"]),
        lower_edge_hz=float(raw["lower_edge_hz"]),
        upper_edge_hz=float(raw["upper_edge_hz"]),
        log_floor=float(raw["log_floor"]),
        expected_frames=int(raw["expected_frames"]),
    )
    return audio_config, log_mel_config


def load_index(index_path: Path) -> list[DatasetRow]:
    rows: list[DatasetRow] = []
    with index_path.open("r", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["include"] != "true":
                continue
            rows.append(
                DatasetRow(
                    relative_path=row["relative_path"],
                    raw_label=row["raw_label"],
                    assignment_intent=row["assignment_intent"],
                    split=row["split"],
                )
            )
    return rows


def sorted_intents(rows: Iterable[DatasetRow]) -> list[str]:
    return sorted({row.assignment_intent for row in rows})


def balanced_limit(
    rows: list[DatasetRow],
    per_group: int | None,
    seed: int,
    group_by: str = "assignment_intent",
) -> list[DatasetRow]:
    if per_group is None:
        return rows
    if group_by not in {"assignment_intent", "raw_label"}:
        raise ValueError(f"Unsupported grouping field: {group_by}")

    rng = np.random.default_rng(seed)
    grouped: dict[str, list[DatasetRow]] = defaultdict(list)
    for row in rows:
        key = row.assignment_intent if group_by == "assignment_intent" else row.raw_label
        grouped[key].append(row)

    limited: list[DatasetRow] = []
    for group in sorted(grouped):
        group_rows = grouped[group]
        order = rng.permutation(len(group_rows))
        limited.extend(group_rows[i] for i in order[:per_group])
    return limited


def encode_labels(rows: list[DatasetRow], intents: list[str]) -> np.ndarray:
    label_to_id = {label: idx for idx, label in enumerate(intents)}
    return np.array([label_to_id[row.assignment_intent] for row in rows], dtype=np.int64)


def extract_feature_vector(
    project_root: Path,
    row: DatasetRow,
    audio_config: AudioConfig,
    log_mel_config: LogMelConfig,
    feature_mode: str,
) -> np.ndarray:
    audio = load_audio(project_root / row.relative_path, audio_config)
    log_mel = extract_log_mel(audio, log_mel_config)

    if feature_mode == "pooled":
        mean = log_mel.mean(axis=0)
        std = log_mel.std(axis=0)
        return np.concatenate([mean, std]).astype(np.float32)

    if feature_mode == "flat":
        return log_mel.reshape(-1).astype(np.float32)

    raise ValueError(f"Unsupported feature mode: {feature_mode}")


def build_matrix(
    project_root: Path,
    rows: list[DatasetRow],
    audio_config: AudioConfig,
    log_mel_config: LogMelConfig,
    feature_mode: str,
) -> np.ndarray:
    vectors = [
        extract_feature_vector(project_root, row, audio_config, log_mel_config, feature_mode)
        for row in rows
    ]
    return np.stack(vectors).astype(np.float32)
