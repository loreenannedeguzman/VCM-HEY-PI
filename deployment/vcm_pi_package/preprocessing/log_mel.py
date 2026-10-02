from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.signal import get_window


@dataclass(frozen=True)
class LogMelConfig:
    sample_rate_hz: int = 16000
    frame_length_ms: float = 25.0
    frame_step_ms: float = 10.0
    fft_length: int = 512
    mel_bins: int = 40
    lower_edge_hz: float = 20.0
    upper_edge_hz: float = 7600.0
    log_floor: float = 1e-6
    expected_frames: int = 398

    @property
    def frame_length_samples(self) -> int:
        return int(round(self.sample_rate_hz * self.frame_length_ms / 1000.0))

    @property
    def frame_step_samples(self) -> int:
        return int(round(self.sample_rate_hz * self.frame_step_ms / 1000.0))


def hz_to_mel(hz: np.ndarray | float) -> np.ndarray | float:
    return 2595.0 * np.log10(1.0 + np.asarray(hz) / 700.0)


def mel_to_hz(mel: np.ndarray | float) -> np.ndarray | float:
    return 700.0 * (np.power(10.0, np.asarray(mel) / 2595.0) - 1.0)


def mel_filterbank(config: LogMelConfig) -> np.ndarray:
    num_spectrogram_bins = config.fft_length // 2 + 1
    mel_edges = np.linspace(
        hz_to_mel(config.lower_edge_hz),
        hz_to_mel(config.upper_edge_hz),
        config.mel_bins + 2,
    )
    hz_edges = mel_to_hz(mel_edges)
    bin_frequencies = np.linspace(0.0, config.sample_rate_hz / 2.0, num_spectrogram_bins)

    filters = np.zeros((num_spectrogram_bins, config.mel_bins), dtype=np.float32)
    for mel_idx in range(config.mel_bins):
        lower = hz_edges[mel_idx]
        center = hz_edges[mel_idx + 1]
        upper = hz_edges[mel_idx + 2]

        lower_slope = (bin_frequencies - lower) / (center - lower)
        upper_slope = (upper - bin_frequencies) / (upper - center)
        filters[:, mel_idx] = np.maximum(0.0, np.minimum(lower_slope, upper_slope))
    return filters


def frame_audio(audio: np.ndarray, config: LogMelConfig) -> np.ndarray:
    frame_length = config.frame_length_samples
    frame_step = config.frame_step_samples
    if audio.shape[0] < frame_length:
        raise ValueError("Audio is shorter than one analysis frame after padding.")

    frame_count = 1 + (audio.shape[0] - frame_length) // frame_step
    shape = (frame_count, frame_length)
    strides = (audio.strides[0] * frame_step, audio.strides[0])
    frames = np.lib.stride_tricks.as_strided(audio, shape=shape, strides=strides)
    return frames.copy()


def power_spectrogram(audio: np.ndarray, config: LogMelConfig) -> np.ndarray:
    frames = frame_audio(audio, config)
    window = get_window("hann", config.frame_length_samples, fftbins=True).astype(np.float32)
    windowed = frames * window[None, :]
    spectrum = np.fft.rfft(windowed, n=config.fft_length, axis=1)
    return (np.abs(spectrum) ** 2).astype(np.float32)


def extract_log_mel(audio: np.ndarray, config: LogMelConfig) -> np.ndarray:
    """Convert fixed-length audio into a [time, mel] log-Mel spectrogram."""
    power = power_spectrogram(audio, config)
    mel = np.matmul(power, mel_filterbank(config))
    log_mel = np.log(np.maximum(mel, config.log_floor)).astype(np.float32)
    if log_mel.shape != (config.expected_frames, config.mel_bins):
        raise ValueError(
            f"Unexpected log-Mel shape {log_mel.shape}; expected "
            f"({config.expected_frames}, {config.mel_bins})"
        )
    return log_mel
