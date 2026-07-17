# Contributing to WAVE

Thanks for helping build an open engine for decoding animal communication.

## Setup

```bash
git clone https://github.com/WAVETranslator/Wild-Animal-Voice-Engine.git
cd Wild-Animal-Voice-Engine
pip install -e ".[dev]"
pytest -q
python examples/quickstart.py
```

## Where things live

| Stage   | Package          | What a good first PR looks like |
|---------|------------------|---------------------------------|
| Ingest  | `wave/ingest`    | resampling, chunking long files, channel selection |
| Signal  | `wave/signal`    | FFT-based Superlet, plotting helpers |
| Models  | `wave/models`    | a `NatureLM` or `Perch` adapter subclassing `VocalizationModel` |
| Pipeline| `wave/pipeline`  | batch mode, writing detection tables |

## Ground rules

- **Keep it readable.** This is a reference implementation; clarity beats cleverness.
- **No hidden placeholders.** If something is a stub, say so in the docstring.
- **Add a test.** Even a small one. Run `pytest -q` before opening a PR.
- **New model? Implement the interface**, don't fork the pipeline.

## Opening a PR

1. Branch from `main`.
2. Keep PRs focused — one stage or one fix.
3. Describe *why*, not just *what*. Link an issue if there is one.

Questions? Open a discussion or a `question`-labeled issue.
