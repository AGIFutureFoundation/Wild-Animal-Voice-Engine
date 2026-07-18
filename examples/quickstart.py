"""Generate a synthetic 'call', run the full WAVE pipeline, and print results.

Run:  python examples/quickstart.py
No data download needed — it synthesizes a pulsed tone to mimic a vocalization.
"""
import numpy as np
import soundfile as sf

from wave.pipeline import run_pipeline

sr = 16000
t = np.linspace(0, 3.0, sr * 3, endpoint=False)
# A pulsed 300 Hz tone (echoing WAVE's finding that some whale song is pulsed)
pulse = (np.sin(2 * np.pi * 300 * t) * (np.sin(2 * np.pi * 6 * t) > 0)).astype("float32")
pulse[: sr] = 0  # 1s of silence first
sf.write("/tmp/wave_demo.wav", pulse * 0.5, sr)

res = run_pipeline("/tmp/wave_demo.wav", fmin=50, fmax=1000)
print(f"Duration {res.duration_s:.1f}s, spectrogram {res.spectrogram.shape}")
for d in res.detections:
    print(f"  [{d.start_s:.2f}-{d.end_s:.2f}s] {d.label} ({d.confidence:.2f})")
