"""Adapter for Google's Perch bioacoustic embedding model.

Perch (https://github.com/google-research/perch, Apache-2.0) produces strong
audio embeddings for birds and other animals. WAVE does not vendor Perch; this
adapter wraps it behind `VocalizationModel` so the pipeline can use Perch
embeddings for unsupervised mapping and, paired with perch-hoplite, for
cross-species transfer.

This is a *stub adapter*: the interface is real and importable, but calling it
without Perch installed raises a clear, actionable error. Install Perch, then
fill in `_load_model` / `embed`. This honesty is deliberate — no silent no-ops.
"""
from __future__ import annotations

from typing import List, Sequence

import numpy as np

from .base import Detection, VocalizationModel

_INSTALL_HINT = (
    "Perch is not installed. Install it from "
    "https://github.com/google-research/perch (Apache-2.0), then implement "
    "PerchModel._load_model(). WAVE keeps Perch as a dependency, not vendored code."
)


class PerchModel(VocalizationModel):
    """Wrap Perch embeddings behind the WAVE model interface."""

    def __init__(self, checkpoint: str | None = None):
        self.checkpoint = checkpoint
        self._model = None

    def _load_model(self):
        try:
            import perch  # noqa: F401  (import checked lazily)
        except Exception as exc:  # pragma: no cover - env-dependent
            raise RuntimeError(_INSTALL_HINT) from exc
        # TODO: load the Perch checkpoint here and cache on self._model.
        raise NotImplementedError(
            "Perch is installed but the checkpoint loader is not wired yet. "
            "Implement _load_model() to return a callable embedder."
        )

    def embed(self, samples: np.ndarray, sample_rate: int) -> np.ndarray:
        if self._model is None:
            self._model = self._load_model()
        return self._model(samples, sample_rate)  # pragma: no cover

    def detect(self, samples: np.ndarray, sample_rate: int) -> Sequence[Detection]:
        # Perch is an embedder, not a segment detector. Detection is expected to
        # come from embedding + a classifier/index (see perch-hoplite). Until
        # that's wired, be explicit rather than returning a misleading empty list.
        raise NotImplementedError(
            "PerchModel provides embeddings via embed(); pair it with a "
            "classifier or perch-hoplite index for detection."
        )
