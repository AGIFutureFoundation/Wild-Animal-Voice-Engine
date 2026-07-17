"""The model contract every adapter (NatureLM, Perch, custom) implements."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass
class Detection:
    """One detected vocalization event."""
    start_s: float
    end_s: float
    label: str
    confidence: float


class VocalizationModel(ABC):
    """Interface for any model that turns audio into detections/embeddings.

    Adapters for NatureLM and Perch 2.0 should subclass this. Keeping the
    surface tiny is deliberate: it makes 'a model trained on one species can
    help organize another' testable by swapping the adapter, not the pipeline.
    """

    @abstractmethod
    def detect(self, samples: np.ndarray, sample_rate: int) -> Sequence[Detection]:
        """Return detected vocalization events in the clip."""

    def embed(self, samples: np.ndarray, sample_rate: int) -> np.ndarray:
        """Optional: return an embedding vector for unsupervised mapping."""
        raise NotImplementedError("This adapter does not provide embeddings yet.")
