"""A minimal, working Superlet-style spectrogram.

The Superlet Transform combines a set of Morlet wavelets of increasing
cycle count (a "superlet") and geometrically averages their power. This gives
both good frequency resolution (high-cycle wavelets) and good time resolution
(low-cycle wavelets) at once.

This implementation is intentionally compact and dependency-light (numpy/scipy)
so contributors can read it end to end. It is correct enough to produce a
usable spectrogram; performance tuning (FFT-based convolution, GPU) is a
tracked follow-up, not a hidden assumption.
"""
from __future__ import annotations

import numpy as np
from scipy.signal import fftconvolve


def _morlet(sample_rate: int, freq: float, n_cycles: float) -> np.ndarray:
    """Complex Morlet wavelet for a given center frequency and cycle count."""
    sigma_t = n_cycles / (2.0 * np.pi * freq)
    t = np.arange(-3.5 * sigma_t, 3.5 * sigma_t, 1.0 / sample_rate)
    gauss = np.exp(-(t ** 2) / (2.0 * sigma_t ** 2))
    carrier = np.exp(2j * np.pi * freq * t)
    wavelet = gauss * carrier
    wavelet /= np.sqrt(np.sum(np.abs(wavelet) ** 2))  # unit energy
    return wavelet


def superlet_spectrogram(
    samples: np.ndarray,
    sample_rate: int,
    freqs: np.ndarray,
    order: int = 3,
    base_cycles: float = 3.0,
) -> np.ndarray:
    """Compute an adaptive-superlet power spectrogram.

    Args:
        samples: 1-D audio, float.
        sample_rate: Hz.
        freqs: center frequencies (Hz) to evaluate.
        order: number of wavelets combined per superlet (higher = sharper freq).
        base_cycles: cycle count of the base wavelet.

    Returns:
        Power array of shape (len(freqs), len(samples)).
    """
    freqs = np.asarray(freqs, dtype=float)
    out = np.empty((len(freqs), len(samples)), dtype=float)
    for i, f in enumerate(freqs):
        powers = []
        for k in range(1, order + 1):
            w = _morlet(sample_rate, f, base_cycles * k)
            conv = fftconvolve(samples, w, mode="same")
            powers.append(np.abs(conv) ** 2)
        # geometric mean across the superlet set
        out[i] = np.exp(np.mean(np.log(np.stack(powers) + 1e-12), axis=0))
    return out
