"""Adapter for Earth Species Project's NatureLM-audio model.

NatureLM-audio (https://github.com/earthspecies/NatureLM-audio, MIT) is an
audio-language model for animal sounds. Because it is MIT, it is fork-safe, but
the cleaner path is to depend on it and wrap it here behind `VocalizationModel`.

Stub adapter: importable and interface-complete; raises a clear error until the
model is installed and wired. No silent placeholders.
"""
from __future__ import annotations

from typing import List, Sequence

import numpy as np

from .base import Detection, VocalizationModel

_INSTALL_HINT = (
    "NatureLM-audio is not installed. Get it from "
    "https://github.com/earthspecies/NatureLM-audio (MIT), then implement "
    "NatureLMModel._load_model()."
)


class NatureLMModel(VocalizationModel):
    """Wrap NatureLM-audio behind the WAVE model interface."""

    def __init__(self, checkpoint: str | None = None):
        self.checkpoint = checkpoint
        self._model = None

    def _load_model(self):
        try:
            import naturelm  # noqa: F401
        except Exception as exc:  # pragma: no cover - env-dependent
            raise RuntimeError(_INSTALL_HINT) from exc
        raise NotImplementedError(
            "NatureLM is installed but not wired. Implement _load_model()."
        )

    def detect(self, samples: np.ndarray, sample_rate: int) -> Sequence[Detection]:
        if self._model is None:
            self._model = self._load_model()
        return self._model.detect(samples, sample_rate)  # pragma: no cover
