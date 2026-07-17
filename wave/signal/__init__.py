"""Signal processing: high-resolution time-frequency representations.

The headline method here is the Superlet Transform, which gives sharper
time-frequency localization than a single wavelet/STFT — useful for showing,
for example, that a whale song is pulsed rather than continuous.
"""
from .superlet import superlet_spectrogram

__all__ = ["superlet_spectrogram"]
