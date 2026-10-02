from __future__ import annotations

import wave
from dataclasses import dataclass
from math import gcd
from pathlib import Path

import numpy as np
from scipy.signal import resample_poly


@dataclass(frozen=True)
class AudioConfig:
    sample_rate_hz: int = 16000
    target_duration_sec: float = 4.0
    normalize: str = "peak"

    @property
    def target_samples(self) -> int:
        return int(round(self.sample_rate_hz * self.target_duration_sec))


def _pcm_to_float(raw: bytes, sample_width: int) -> np.ndarray:
    if sample_width == 1:
        data = np.frombuffer(raw, dtype=np.uint8).astype(np.float32)
        return (data - 128.0) / 128.0
    if sample_width == 2:
        data = np.frombuffer(raw, dtype="<i2").astype(np.float32)
        return data / 32768.0
    if sample_width == 4:
        data = np.frombuffer(raw, dtype="<i4").astype(np.float32)
        return data / 2147483648.0
    raise ValueError(f"Unsupported WAV sample width: {sample_width} bytes")


def read_wav(path: str | Path) -> tuple[np.ndarray, int]:
    """Read a PCM WAV file as mono float32 samples in [-1, 1]."""
    path = Path(path)
    with wave.open(str(path), "rb") as wav:
        channels = wav.getnchannels()
        sample_rate = wav.getframerate()
        sample_width = wav.getsampwidth()
        frames = wav.readframes(wav.getnframes())

    audio = _pcm_to_float(frames, sample_width)
    if channels > 1:
        audio = audio.reshape(-1, channels).mean(axis=1)
    return audio.astype(np.float32, copy=False), sample_rate


def resample_if_needed(audio: np.ndarray, sample_rate: int, target_rate: int) -> np.ndarray:
    if sample_rate == target_rate:
        return audio.astype(np.float32, copy=False)
    factor = gcd(sample_rate, target_rate)
    up = target_rate // factor
    down = sample_rate // factor
    return resample_poly(audio, up, down).astype(np.float32)


def normalize_audio(audio: np.ndarray, mode: str) -> np.ndarray:
    if mode == "none":
        return audio.astype(np.float32, copy=False)
    if mode != "peak":
        raise ValueError(f"Unsupported normalization mode: {mode}")
    peak = float(np.max(np.abs(audio))) if audio.size else 0.0
    if peak <= 0.0:
        return audio.astype(np.float32, copy=False)
    return (audio / peak).astype(np.float32)


def pad_or_trim(audio: np.ndarray, target_samples: int) -> np.ndarray:
    if audio.shape[0] == target_samples:
        return audio.astype(np.float32, copy=False)
    if audio.shape[0] > target_samples:
        return audio[:target_samples].astype(np.float32, copy=False)
    output = np.zeros(target_samples, dtype=np.float32)
    output[: audio.shape[0]] = audio
    return output


def load_audio(path: str | Path, config: AudioConfig) -> np.ndarray:
    """Load, resample, normalize, and pad/trim audio to fixed length."""
    audio, sample_rate = read_wav(path)
    audio = resample_if_needed(audio, sample_rate, config.sample_rate_hz)
    audio = normalize_audio(audio, config.normalize)
    return pad_or_trim(audio, config.target_samples)
