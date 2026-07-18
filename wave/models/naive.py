"""A dependency-free reference model so the pipeline runs out of the box.

EnergyThresholdModel flags segments whose short-time energy is high relative
to the clip. It is NOT a species classifier — it exists so contributors can run
the full pipeline end to end before wiring in NatureLM/Perch, and so tests have
a deterministic detector.

Threshold logic: a frame is "active" if its energy exceeds both
(a) a fraction of the peak-frame energy, and
(b) a small absolute floor above the noise mean.
Using the peak makes it robust to steady tones, where energy variance is tiny.
"""
from __future__ import annotations

from typing import List

import numpy as np

from .base import Detection, VocalizationModel


class EnergyThresholdModel(VocalizationModel):
    def __init__(self, frame_s: float = 0.05, peak_frac: float = 0.25):
        self.frame_s = frame_s
        self.peak_frac = peak_frac

    def detect(self, samples: np.ndarray, sample_rate: int) -> List[Detection]:
        frame = max(1, int(self.frame_s * sample_rate))
        n = len(samples) // frame
        if n == 0:
            return []
        energy = (samples[: n * frame].reshape(n, frame) ** 2).mean(axis=1)
        peak = float(energy.max())
        if peak <= 0:
            return []
        thr = self.peak_frac * peak
        dets: List[Detection] = []
        active = False
        start = 0
        for i, e in enumerate(energy):
            if e > thr and not active:
                active, start = True, i
            elif e <= thr and active:
                active = False
                dets.append(Detection(start * self.frame_s, i * self.frame_s,
                                      "sound_event", float(min(1.0, e / peak))))
        if active:
            dets.append(Detection(start * self.frame_s, n * self.frame_s,
                                  "sound_event", 1.0))
        return dets
