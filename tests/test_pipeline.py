import numpy as np
import soundfile as sf

from wave.ingest import load_audio
from wave.signal import superlet_spectrogram
from wave.models import EnergyThresholdModel
from wave.pipeline import run_pipeline


def _write_tone(path, sr=8000, dur=1.0, f=200.0):
    t = np.linspace(0, dur, int(sr * dur), endpoint=False)
    x = np.sin(2 * np.pi * f * t).astype("float32")
    x[: sr // 4] = 0.0  # leading silence so there's an onset to detect
    sf.write(path, x, sr)


def test_load(tmp_path):
    p = tmp_path / "a.wav"
    _write_tone(p)
    clip = load_audio(str(p))
    assert clip.sample_rate == 8000
    assert 0.9 < clip.duration_s < 1.1


def test_superlet_shape():
    sr = 8000
    x = np.random.randn(sr).astype("float32")
    spec = superlet_spectrogram(x, sr, np.linspace(50, 1000, 16))
    assert spec.shape == (16, sr)
    assert np.all(spec >= 0)


def test_detector_finds_onset(tmp_path):
    p = tmp_path / "b.wav"
    _write_tone(p)
    dets = EnergyThresholdModel().detect(*_load(str(p)))
    assert len(dets) >= 1


def _load(path):
    from wave.ingest import load_audio
    c = load_audio(path)
    return c.samples, c.sample_rate


def test_end_to_end(tmp_path):
    p = tmp_path / "c.wav"
    _write_tone(p)
    res = run_pipeline(str(p), fmin=50, fmax=1000, n_freqs=16)
    assert res.spectrogram.shape[0] == 16
    assert res.duration_s > 0


def test_perch_adapter_importable_and_honest():
    from wave.models import PerchModel
    m = PerchModel()
    # It must raise a clear error, not silently return nothing.
    import pytest
    with pytest.raises((RuntimeError, NotImplementedError)):
        m.detect(__import__("numpy").zeros(1000), 16000)


def test_naturelm_adapter_importable_and_honest():
    from wave.models import NatureLMModel
    m = NatureLMModel()
    import pytest
    with pytest.raises((RuntimeError, NotImplementedError)):
        m.detect(__import__("numpy").zeros(1000), 16000)


def test_pipeline_still_works_with_default_model():
    import numpy as np, soundfile as sf, tempfile, os
    from wave.pipeline import run_pipeline
    sr = 8000
    t = np.linspace(0, 1, sr, endpoint=False)
    x = np.sin(2 * np.pi * 200 * t).astype("float32"); x[: sr // 4] = 0
    p = os.path.join(tempfile.mkdtemp(), "x.wav"); sf.write(p, x, sr)
    res = run_pipeline(p, fmin=50, fmax=1000, n_freqs=16)
    assert len(res.detections) >= 1
