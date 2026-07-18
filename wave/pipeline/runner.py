"""Glue: ingest -> signal -> model. The one function contributors extend."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np

from ..ingest import load_audio
from ..models import EnergyThresholdModel, Detection, VocalizationModel
from ..signal import superlet_spectrogram


@dataclass
class PipelineResult:
    detections: Sequence[Detection]
    spectrogram: np.ndarray
    freqs: np.ndarray
    duration_s: float


def run_pipeline(
    path: str,
    model: VocalizationModel | None = None,
    fmin: float = 20.0,
    fmax: float = 2000.0,
    n_freqs: int = 64,
) -> PipelineResult:
    """Load a file, compute a Superlet spectrogram, and detect vocalizations."""
    clip = load_audio(path)
    model = model or EnergyThresholdModel()
    freqs = np.linspace(fmin, min(fmax, clip.sample_rate / 2 - 1), n_freqs)
    spec = superlet_spectrogram(clip.samples, clip.sample_rate, freqs)
    dets = model.detect(clip.samples, clip.sample_rate)
    return PipelineResult(dets, spec, freqs, clip.duration_s)
