# WAVE — Wild Animal Voice Engine

> Developed on the Virtual Protocol to help train systems to become translators of all species.

WAVE is an open, MIT-licensed pipeline for turning raw environmental audio into
structured, analyzable animal-vocalization signals — a step toward decoding
non-human communication and monitoring ecosystem health across land and sea.

## Status box — what is true, and what is not yet true

| Claim | Status |
|---|---|
| The repo contains a real, readable pipeline: ingest → Superlet signal → model adapters → runner + CLI | **TRUE — verified 2026-11-07** against the live `main` tree (see `docs/architecture.md`). |
| The pipeline runs end to end with its built-in reference detector | **TRUE on code inspection.** `EnergyThresholdModel` is dependency-free; `examples/quickstart.py` synthesizes its own audio, so no download is needed. Tests were **not executed** in this pass, so a passing test suite is **unverified**. |
| The NatureLM and Perch 2.0 adapters do real inference | **NOT TRUE.** Both are honest stubs: importable, interface-complete, and they raise a clear error (`RuntimeError` / `NotImplementedError`) instead of returning results. See `docs/architecture.md`. |
| `perch-endpoint/` runs Perch 2.0 inference | **NOT VERIFIED.** The server code is real and loads Perch 2.0 via `perch-hoplite` *if* a GPU deployment exists; without one it runs in a clearly-labelled stub mode that returns no predictions. No deployment evidence is in the repo. |
| WAVE can identify species, translate, or decode meaning | **NOT TRUE.** The only detector that runs today flags loud segments (`sound_event`); it names no species and assigns no meaning. Classification is not decoding: no animal communication system has been decoded by AI, and no playback-validated meaning claim exists for any wild repertoire. |
| WAVE is connected to BirdNET | **NOT VERIFIED in this repo.** No BirdNET code, dependency, or reference exists anywhere in this tree. BirdNET is the live predictor in the WAVE *site* story (bioacoustics.cloud), not in this engine repo. Do not claim a connection here until one is wired and tested. |
| This repo is an original Foundation repo | **NOT TRUE.** It is a **fork of `WAVETranslator/Wild-Animal-Voice-Engine`** (the 3-file stub org). The real code was built on top of that fork here. |

## What the engine does today

1. **Ingest** (`wave/ingest`) — loads WAV/FLAC/OGG into a normalized mono float array.
2. **Signal** (`wave/signal`) — a compact Superlet-style spectrogram in numpy/scipy
   (Morlet wavelets, geometric mean across cycle counts).
3. **Models** (`wave/models`) — one interface (`VocalizationModel`), one working
   reference detector (energy-threshold), two stub adapters (Perch, NatureLM).
4. **Pipeline** (`wave/pipeline`) — `run_pipeline()` glues the stages; `wave` CLI
   prints clip duration, spectrogram shape, and detected events.
5. **Perch endpoint** (`perch-endpoint/`) — an HTTP server + Dockerfile + Akash
   deploy spec for Perch 2.0 inference, with an explicit stub mode.

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
vocalization events with timestamps and confidence. Detections from the default
model are labelled `sound_event` — energy segments, not species.

## Project status

**Early scaffold, but runnable end to end (reference-detector path).** Anything that
is a placeholder is marked as such in the code — no hidden "coming soon."

What's real now:

- Working audio ingest (WAV/FLAC/OGG → mono float).
- A compact Superlet-style spectrogram in pure numpy/scipy.
- A clean model interface + a reference detector + a full runner and CLI.
- Tests and a zero-download example (tests not executed in this pass — see `docs/gaps.md`).
- A Perch inference endpoint server with an honest stub mode.

What's next (see `docs/gaps.md`):

- Wire real inference into the NatureLM and Perch 2.0 adapters.
- Run the test suite and record the result; fix the stale upstream links
  (`CONTRIBUTING.md`, `CITATION.cff` still point at `WAVETranslator`).
- FFT/GPU-accelerated Superlet for long recordings.
- Unsupervised vocal-pattern mapping and cross-species transfer experiments.
- A BirdNET wiring decision: BirdNET is the field's working classifier, but no
  BirdNET code exists in this repo today.

## Honesty lines

- No discovery, cure, treatment, diagnosis, or decoding result is claimed here.
  Classification is not decoding, and this engine does not classify yet.
- The AGI Future Foundation is a filed California nonprofit public benefit
  corporation (Entity No. B20260196664) with **no IRS 501(c)(3) determination
  letter on file** — never tax-exempt, never tax-deductible. AGI Corp has an EIN
  only and is not formed. W3 / SmartCiti.X / Delaware series are proposed, not formed.
- There is no partnership with Cornell, the Earth Species Project, Project CETI,
  WHOI, Google, or the Wild Dolphin Project. Do not imply one. Perch and
  NatureLM are named here as upstream open-source projects this code *adapts to*,
  not as partners.
- Archives listed in `docs/datasets.md` are public resources, linked-not-owned.
  Their licences are recorded per archive and are separate from this repo's MIT
  code licence.

## Docs

- `docs/architecture.md` — the pipeline as verified, file by file.
- `docs/datasets.md` — the archives this engine can draw on, with settled figures.
- `docs/gaps.md` — what is missing before this is a real engine.

## Contributing

New contributors welcome — start with `CONTRIBUTING.md` and the `good first issue`
label. **Note:** `CONTRIBUTING.md` currently tells contributors to clone from
`WAVETranslator/Wild-Animal-Voice-Engine` — that is a stale upstream link (see
`docs/gaps.md`); clone this repo instead until it is fixed.

## Citation

If you use WAVE, please cite it — see `CITATION.cff`. **Note:** `CITATION.cff`
currently lists `WAVETranslator/Wild-Animal-Voice-Engine` as the repository-code
URL — a stale upstream link (see `docs/gaps.md`).

## License

MIT — see `LICENSE`.
