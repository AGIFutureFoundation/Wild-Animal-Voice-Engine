"""Audio ingestion: load recordings into a common (samples, sample_rate) form."""
from .loader import load_audio, AudioClip

__all__ = ["load_audio", "AudioClip"]
