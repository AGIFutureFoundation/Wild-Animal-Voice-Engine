"""End-to-end pipeline: audio file -> detections + spectrogram."""
from .runner import run_pipeline, PipelineResult

__all__ = ["run_pipeline", "PipelineResult"]
