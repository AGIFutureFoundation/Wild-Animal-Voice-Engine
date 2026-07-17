"""Model adapters: a common interface over bioacoustic models.

WAVE does not reimplement NatureLM or Perch; it wraps them behind one interface
so the pipeline can swap detectors/embedders without rewrites. The reference
EnergyThresholdModel lets the whole pipeline run before the heavy models exist.
"""
from .base import VocalizationModel, Detection
from .naive import EnergyThresholdModel
from .perch import PerchModel
from .naturelm import NatureLMModel

__all__ = [
    "VocalizationModel",
    "Detection",
    "EnergyThresholdModel",
    "PerchModel",
    "NatureLMModel",
]
