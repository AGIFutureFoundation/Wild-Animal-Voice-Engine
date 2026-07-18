"""Load audio files into a normalized mono float array.

This is a working, minimal loader. It reads any format soundfile supports
(WAV/FLAC/OGG), downmixes to mono, and returns an AudioClip. Real field data
often arrives as long multi-channel hydrophone/logger recordings; the ingest
layer is where resampling, chunking, and channel selection belong later.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class AudioClip:
    """A mono audio clip plus its sample rate."""
    samples: np.ndarray  # float32, shape (n,)
    sample_rate: int

    @property
    def duration_s(self) -> float:
        return len(self.samples) / self.sample_rate if self.sample_rate else 0.0


def load_audio(path: str) -> AudioClip:
    """Load an audio file, downmix to mono float32, and return an AudioClip."""
    import soundfile as sf

    data, sr = sf.read(path, dtype="float32", always_2d=True)
    mono = data.mean(axis=1)  # simple downmix; channel selection is a TODO
    return AudioClip(samples=np.ascontiguousarray(mono), sample_rate=int(sr))
