# WAVE — Wild Animal Voice Engine

> Developed on the Virtual Protocol to help train systems to become translators of all species.

WAVE is an open, MIT-licensed pipeline for turning raw environmental audio into
structured, analyzable animal-vocalization signals — a step toward decoding
non-human communication and monitoring ecosystem health across land and sea.

This repository is the open core. It is deliberately small and readable so
researchers and contributors can follow it end to end and extend any stage.

## The Technical Triad

WAVE is organized around three ideas, mirrored by the code layout:

1. **Ingest** (`wave/ingest`) — get field audio from bio-logging sensors
   (hydrophones, loggers) into a common, normalized form.
2. **Signal** (`wave/signal`) — the **Superlet Transform**, a high-resolution
   time-frequency method adapted from neuroscience. It gives sharp time *and*
   frequency localization at once — enough to reveal, for example, that a
   Chagos pygmy blue whale song is *pulsed*, not continuous.
3. **Models** (`wave/models`) — thin adapters over bioacoustic foundation
   models (**NatureLM**, **Perch 2.0**) behind one interface, so a model that
   organizes one species' vocalizations can be swapped in to help with another.

`wave/pipeline` glues these together into a single `run_pipeline()` call.

## Quickstart

```bash
pip install -e ".[dev]"
python examples/quickstart.py      # synthesizes audio, runs the whole pipeline
```

Or on your own recording:

```bash
wave path/to/recording.wav --fmin 20 --fmax 2000
```

Expected output: clip duration, spectrogram shape, and a list of detected
vocalization events with timestamps and confidence.

## Project status

**Early scaffold, but runnable end to end today.** The pipeline works with a
dependency-free reference detector (`EnergyThresholdModel`) so you can run
everything before wiring in the heavy foundation models. Anything that is a
placeholder is marked as such in the code — no hidden "coming soon."

What's real now:
- Working audio ingest (WAV/FLAC/OGG → mono float).
- A compact, correct Superlet-style spectrogram in pure numpy/scipy.
- A clean model interface + a reference detector + a full runner and CLI.
- Tests and a zero-download example.

What's next (see issues):
- Wire real inference into the NatureLM and Perch 2.0 adapters (interface + stubs already in `wave/models/`).
- FFT/GPU-accelerated Superlet for long recordings.
- Unsupervised vocal-pattern mapping and cross-species transfer experiments.

## Contributing

New contributors welcome — start with [CONTRIBUTING.md](CONTRIBUTING.md) and
the `good first issue` label. The architecture is intentionally small so your
first PR can be a real one.

## Citation

If you use WAVE, please cite it — see [CITATION.cff](CITATION.cff)
(ORCID: [0009-0004-3540-7860](https://orcid.org/0009-0004-3540-7860)).

## License

MIT — see [LICENSE](LICENSE).
