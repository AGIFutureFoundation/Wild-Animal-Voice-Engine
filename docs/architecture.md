# WAVE — Architecture (as verified, 2026-11-07)

**Source:** live `main` branch of `AGIFutureFoundation/Wild-Animal-Voice-Engine`,
tree SHA `65ee81c0e7671571f9a8dfba488c05dd61cef929`, read via the GitHub public
API on 2026-11-07. Every file below was read in full unless marked otherwise.
Nothing was executed: the test suite was not run and the pipeline was not run
in this pass, so "runnable end to end" is supported by code inspection only.

**Correction to the earlier org listing:** this repo is a **fork** of
`WAVETranslator/Wild-Animal-Voice-Engine` (API field `fork: true`,
`parent.full_name: WAVETranslator/Wild-Animal-Voice-Engine`). The org listing
called it an own repo — that was wrong. The fork was created 2026-07-17 and
last updated 2026-07-18; the upstream is the 3-file stub (`.gitignore`,
`LICENSE`, 154-byte `README.md`), so all real code here was added on the fork.

## 1. File tree (36 blobs, `main`)

| Path | Size (bytes) | What it is |
|---|---|---|
| `README.md` | 2,938 | Live README — "early scaffold, but runnable end to end" |
| `pyproject.toml` | 599 | Package `wave-engine` v0.1.0, Python ≥3.10, deps numpy/scipy/soundfile, `wave` CLI entry point. **Note:** package name is `wave-engine`, not the repo name |
| `LICENSE` | 1,071 | MIT |
| `CITATION.cff` | 615 | Cites the repo; `repository-code` URL still points at `WAVETranslator/Wild-Animal-Voice-Engine` (stale — see §5) |
| `CONTRIBUTING.md` | 1,299 | Clone URL still points at `WAVETranslator/Wild-Animal-Voice-Engine` (stale — see §5) |
| `.gitignore` | 263 | Standard Python ignores |
| `.github/ISSUE_TEMPLATE/bug_report.md` | 226 | — |
| `.github/ISSUE_TEMPLATE/feature_request.md` | 277 | — |
| `.github/pull_request_template.md` | 211 | — |
| `.github/workflows/build-perch-endpoint.yml` | 1,520 | CI: builds `perch-endpoint/` and pushes to GHCR as `ghcr.io/agifuturefoundation/wave-perch-endpoint` on pushes to `main`/`perch-endpoint` touching that dir |
| `wave/__init__.py` | 214 | `__version__ = "0.1.0"` |
| `wave/cli.py` | 833 | `wave <audio-file>` CLI |
| `wave/ingest/__init__.py` | 163 | Exports `load_audio`, `AudioClip` |
| `wave/ingest/loader.py` | 1,097 | Audio loader (see §2) |
| `wave/signal/__init__.py` | 370 | Exports `superlet_spectrogram` |
| `wave/signal/superlet.py` | 2,209 | Superlet spectrogram (see §3) |
| `wave/models/__init__.py` | 582 | Exports all four model classes |
| `wave/models/base.py` | 1,127 | `VocalizationModel` interface + `Detection` (see §4) |
| `wave/models/naive.py` | 1,890 | `EnergyThresholdModel` — the only working detector |
| `wave/models/perch.py` | 2,446 | `PerchModel` — **stub** (see §4) |
| `wave/models/naturelm.py` | 1,550 | `NatureLMModel` — **stub** (see §4) |
| `wave/pipeline/__init__.py` | 162 | Exports `run_pipeline`, `PipelineResult` |
| `wave/pipeline/runner.py` | 1,076 | Pipeline glue (see §2) |
| `tests/test_pipeline.py` | 2,381 | 7 tests (see §6) |
| `examples/quickstart.py` | 845 | Synthesizes a pulsed tone, runs the pipeline, prints results |
| `data/README.md` | 766 | Data layout; **ships no datasets** (`data/` is gitignored except this file) |
| `data/.gitignore` | 70 | Ignores everything in `data/` except the README |
| `perch-endpoint/Dockerfile` | 930 | CUDA 12.4.1 base, installs TF ~2.20 + `perch-hoplite` from git |
| `perch-endpoint/README.md` | 1,520 | Endpoint contract + Akash deploy steps; contains an unverifiable "Verified" claim (see §5) |
| `perch-endpoint/deploy.sdl.yaml` | 849 | Akash SDL: 1× RTX 3090 GPU, 4 CPU, 16 Gi RAM, image `ghcr.io/agifuturefoundation/wave-perch-endpoint:latest` |
| `perch-endpoint/requirements.txt` | 12 | `numpy>=1.24` only (TF + perch-hoplite come from the Dockerfile) |
| `perch-endpoint/server.py` | 5,351 | Perch inference HTTP server (see §7) |

## 2. Ingest → pipeline

`wave/ingest/loader.py` — `load_audio(path)` uses `soundfile` to read any format
it supports (WAV/FLAC/OGG), downmixes to mono by averaging channels, returns an
`AudioClip` (float32 samples + sample rate). Docstring is explicit about what is
missing: no resampling, no chunking of long files, no channel selection — those
are listed as later work in the ingest layer.

`wave/pipeline/runner.py` — `run_pipeline(path, model=None, fmin=20.0, fmax=2000.0,
n_freqs=64)`:

1. loads the clip,
2. builds a frequency grid (`linspace(fmin, min(fmax, sr/2 − 1), n_freqs)`),
3. computes the Superlet spectrogram,
4. runs the model detector (default `EnergyThresholdModel`),
5. returns a `PipelineResult` (detections, spectrogram, freqs, duration).

`wave/cli.py` — `wave <audio-file> [--fmin] [--fmax]` prints duration,
spectrogram shape, detection count, and each detection's time range, label,
and confidence.

## 3. Signal — the Superlet Transform

`wave/signal/superlet.py` — `superlet_spectrogram(samples, sample_rate, freqs,
order=3, base_cycles=3.0)`:

- For each centre frequency, builds Morlet wavelets at cycle counts
  `base_cycles × k` for `k = 1..order`, convolves with `scipy.signal.fftconvolve`,
  and takes the **geometric mean** of the power across the wavelet set.
- Returns a power array of shape `(len(freqs), len(samples))`, all values ≥ 0.
- Docstring: "correct enough to produce a usable spectrogram; performance
  tuning (FFT-based convolution, GPU) is a tracked follow-up."

The README and `wave/signal/__init__.py` both say the Superlet "revealed, for
example, that a Chagos pygmy blue whale song is *pulsed*, not continuous."
**Unverified:** no citation, dataset, or analysis supporting that finding is in
the repo. Treat it as an unverified repo claim, not a verified result — and the
same sentence appears in the bioacoustics.cloud site copy, where it is equally
unsourced.

## 4. Models — one interface, one working detector, two stubs

`wave/models/base.py` — the contract every adapter implements:

- `Detection` dataclass: `start_s`, `end_s`, `label`, `confidence`.
- `VocalizationModel` (ABC): abstract `detect(samples, sample_rate)`; optional
  `embed()` that raises `NotImplementedError` by default.

`wave/models/naive.py` — `EnergyThresholdModel(frame_s=0.05, peak_frac=0.25)`,
the **only detector that runs**. It splits audio into 50 ms frames, flags frames
whose energy exceeds 25% of the peak-frame energy, and returns contiguous active
segments labelled `sound_event` with a confidence derived from energy/peak. Its
docstring states plainly: "It is NOT a species classifier." It detects loudness,
not animals, not species, not meaning.

`wave/models/perch.py` — `PerchModel`, **stub, verified by reading the file**:

- `_load_model()` tries `import perch`; if absent, raises `RuntimeError` with an
  install hint (github.com/google-research/perch, Apache-2.0). If present, raises
  `NotImplementedError`: "the checkpoint loader is not wired yet."
- `embed()` delegates to the unwired loader. `detect()` raises
  `NotImplementedError` outright, with the explanation that Perch is an embedder,
  not a segment detector, and detection needs a classifier or perch-hoplite index.
- No Perch code is vendored; the adapter wraps the upstream behind the interface.

`wave/models/naturelm.py` — `NatureLMModel`, **stub, verified by reading the file**:

- Same pattern: `import naturelm` attempt → `RuntimeError` with install hint
  (github.com/earthspecies/NatureLM-audio, MIT) if absent, else
  `NotImplementedError`: "NatureLM is installed but not wired."
- `detect()` delegates to the unwired loader. No NatureLM code is vendored.

Both stubs are deliberately honest: they raise clear errors rather than
returning empty results or fake detections. The test suite encodes this (see §6).

## 5. Corrections to earlier claims about this repo

1. **It is a fork, not an own repo.** (See top of this file.) The org listing's
   "own — real code" row is wrong on fork status. The real code is genuine, but
   it lives on a fork of the WAVETranslator stub.
2. **`perch-endpoint/README.md` "Verified" section is unverifiable.** It claims:
   "Integration tested against WAVE's `classify.py`: with a Perch endpoint set,
   `--model perch` and `--model auto` both parse and merge marine predictions
   correctly (Perch wins marine ties; BirdNET marine labels de-prioritized)."
   **No `classify.py` exists anywhere in this tree**, and there is no `--model`
   flag in the `wave` CLI. The claim appears to describe code that is not in
   this repo (possibly a separate classification worker). Do not repeat it as a
   verified integration test.
3. **Stale upstream links.** `CONTRIBUTING.md` tells contributors to
   `git clone https://github.com/WAVETranslator/Wild-Animal-Voice-Engine.git`,
   and `CITATION.cff` lists the same org as `repository-code`. Both predate the
   fork's real code and point new contributors at the stub.
4. **"Chagos pygmy blue whale song is pulsed"** — repeated in the README,
   `wave/signal/__init__.py`, and the bioacoustics.cloud site, but unsourced in
   the repo. Unverified.
5. **No BirdNET anywhere.** The repo contains no BirdNET code, dependency, or
   mention. Any statement that "BirdNET is the live predictor" belongs to the
   WAVE site story, not to this engine repo, and must not be presented as a
   property of this code.

## 6. Tests — present, not executed in this pass

`tests/test_pipeline.py` — 7 test functions:

- `test_load`, `test_superlet_shape`, `test_detector_finds_onset`,
  `test_end_to_end`, `test_pipeline_still_works_with_default_model` — exercise
  the loader, spectrogram shape/non-negativity, onset detection, and the full
  pipeline on synthetic tones written with `soundfile`.
- `test_perch_adapter_importable_and_honest`,
  `test_naturelm_adapter_importable_and_honest` — assert each stub adapter
  raises `(RuntimeError, NotImplementedError)` on `detect()`. The honesty of
  the stubs is itself tested, which is good practice.
- **Not run in this pass.** Whether the suite passes today (dependency versions,
  environment) is **unverified**. Running `pytest -q` is gap G-1 in
  `docs/gaps.md`.

## 7. Perch endpoint — real server code, unverified deployment

`perch-endpoint/server.py` (5,351 bytes, read in full):

- Contract: `POST /` with raw WAV bytes → `{"predictions": [{common_name,
  scientific_name, confidence}]}`; `GET /health` → `{ok, model: "perch"|"stub",
  gpu}`; optional `PERCH_TOKEN` env var enforces `Authorization: Bearer`.
- `_try_load_model()` loads Perch 2.0 via `perch-hoplite` (`model_configs.
  load_model_config("perch_2")`). On any failure it logs a warning and the
  server runs in **stub mode**: `_predict()` returns `{"predictions": [],
  "stub": true, "note": ...}` — valid contract, clearly labelled, never fakes
  a species.
- Audio is decoded to mono float32 at 32 kHz (Perch's expected rate), with a
  linear resample when needed; inference runs on 5-second segments, top-k 10
  by default (`PERCH_TOPK`).
- Deployment: `Dockerfile` (CUDA 12.4.1, TF ~2.20, perch-hoplite from git),
  `deploy.sdl.yaml` (Akash, 1× RTX 3090), CI workflow builds and pushes the
  image to GHCR.
- **Unverified:** whether the image was ever built, whether an Akash deployment
  ever ran, and whether real Perch inference ever happened. No deployment log,
  lease URI, or inference sample is in the repo. The server *can* do real
  inference; there is no evidence in the repo that it *has*.

## 8. What this repo is, in one paragraph

A small, readable, MIT-licensed scaffold: real ingest, a real Superlet-style
spectrogram, a real pipeline runner and CLI, one working energy-threshold
reference detector, two explicitly unwired foundation-model adapters, a test
suite that asserts the stubs stay honest, and a Perch inference server that
falls back to a labelled stub without a GPU. It is a credible starting point
for engine work. It is not a translator, not a classifier, and not connected
to BirdNET, Perch, or NatureLM in any running sense.
