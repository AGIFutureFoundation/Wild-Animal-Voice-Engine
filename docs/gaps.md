# Gaps — what is missing before this is a real engine

**Status:** Added to this repo 2026-11-07 by the AGI Future Foundation research-lab loop. Each gap states what is missing, why
it matters, and what would close it. Nothing here is presented as already done.

## G-1 — The test suite has not been run (verify the "runnable" claim)

- **Missing:** an executed `pytest -q` result against the current tree.
- **Why it matters:** "runnable end to end" is the repo's central claim, and it
  currently rests on code inspection only (this pass read every file but ran
  nothing). Dependency drift (numpy/scipy/soundfile versions) could break it.
- **Closes when:** someone runs `pip install -e ".[dev]" && pytest -q &&
  python examples/quickstart.py` in a clean environment and records the output
  and versions. Until then, say "runnable on code inspection; tests not executed
  in this pass."

## G-2 — No foundation-model adapter is wired

- **Missing:** implementations of `PerchModel._load_model()` / `embed()` and
  `NatureLMModel._load_model()` / `detect()`. Both raise today by design.
- **Why it matters:** without them the engine detects energy, not animals.
  Every site claim about Perch/NatureLM "powering" WAVE is describing unwired code.
- **Closes when:** at least one adapter loads its model and returns real
  embeddings/detections on a held-out clip, with the result recorded. The
  `perch-endpoint/` server is the nearer path for Perch (see G-3); NatureLM has
  no deployment path at all yet.

## G-3 — No evidence the Perch endpoint ever ran real inference

- **Missing:** a built GHCR image, an Akash lease/deployment record, a
  `/health` response showing `"model": "perch"`, or one real prediction.
- **Why it matters:** the server code is real, but a server that has only ever
  run in stub mode is not an inference service. The `perch-endpoint/README.md`
  "Verified" claim about `classify.py` is unverifiable from this tree (no such
  file exists) and must not be repeated.
- **Closes when:** a deployment returns `"model": "perch"` from `/health` and a
  real top-k prediction on a known clip. Record the image SHA and lease.

## G-4 — No BirdNET version runs in WAVE (internal open question)

- **Missing:** any BirdNET code, dependency, or wiring in this repo.
- **Why it matters:** BirdNET is the field's working classifier and the live
  predictor in the WAVE site story — but this engine repo has no connection to
  it. The repo-build plan (v2, §4) already flags this as an open question.
- **Closes when:** Mike decides whether BirdNET belongs in this engine (as a
  wired adapter, with its CC BY-NC-SA 4.0 non-commercial model licence noted)
  or stays a site-level predictor only. Do not wire it silently; the licence
  constrains commercial use.

## G-5 — Stale upstream links point contributors at the stub

- **Missing:** corrected URLs in `CONTRIBUTING.md` (clone URL) and
  `CITATION.cff` (`repository-code`), both still pointing at
  `WAVETranslator/Wild-Animal-Voice-Engine`.
- **Why it matters:** a new contributor following the docs clones the 3-file
  stub, not this code. Also see the fork question in G-6.
- **Closes when:** both files point at this repo (or at wherever Mike decides
  the canonical home is).

## G-6 — Fork vs own repo is undecided

- **Missing:** a decision on whether this fork of `WAVETranslator` stays the
  home for engine work, or the code moves to an own repo (e.g. the proposed
  `wave-engine`, which the v2 plan now treats as the alternative).
- **Why it matters:** pushes, issues, and citations all depend on the answer,
  and the earlier org listing wrongly called this an own repo.
- **Closes when:** Mike decides. Until then, docs land here on the fork; the
  fork-vs-own-repo decision stays open.

## G-7 — The "pulsed" whale-song claim is unsourced

- **Missing:** any citation, dataset, or analysis in the repo for "the Chagos
  pygmy blue whale song is pulsed, not continuous" (README,
  `wave/signal/__init__.py`, bioacoustics.cloud site copy).
- **Why it matters:** it is presented as a finding of the Superlet method. An
  unsourced finding in the README becomes an unsourced claim on the site.
- **Closes when:** a source is found and cited, or the sentence is removed /
  reworded as an illustrative example of what the method *can* show.

## G-8 — No long-recording performance path

- **Missing:** FFT/GPU-accelerated Superlet, resampling, chunking, channel
  selection. The loader docstring lists resampling/chunking/channel selection
  as later work; the Superlet docstring lists FFT/GPU acceleration as a
  tracked follow-up.
- **Why it matters:** real field data arrives as long multi-channel
  hydrophone/logger recordings. The current implementation convolves per
  frequency over the full clip, which will not scale.
- **Closes when:** chunked processing + a timing benchmark on a long clip exist.

## G-9 — No evaluation harness, no scores (and none invented)

- **Missing:** a BEANS/BirdSet evaluation harness wired to this pipeline, and
  any measured score.
- **Why it matters:** without a harness there is no honest way to say whether a
  future adapter is any good. With an invented score there would be a dishonest
  one. The v2 plan's rule stands: evaluation harnesses with **no invented scores**.
- **Closes when:** a harness runs BEANS (classification/detection only) against
  the pipeline and records real numbers — or records that the reference detector
  cannot meaningfully score, which is itself a result.

## G-10 — No playback / meaning data, no field partner

- **Missing:** paired call-and-response playback data, a field partner, permits,
  and ethics approval. (Dossier lit review §6: Phase 0 depends entirely on data
  access that is not yet secured.)
- **Why it matters:** this is the gap between a classifier and a decoder. No
  amount of adapter wiring closes it; only playback-validated behaviour does.
- **Closes when:** a field programme agrees to share published playback data
  for re-analysis (Phase 0) — or the gap is recorded as the reason the engine
  stays a classifier/detector.

## Not gaps (things people may ask for that are out of scope)

- **Two-way "conversation" with animals:** no programme has achieved this for a
  natural signal; it is not on this engine's roadmap.
- **Re-hosting archive audio:** archives are linked-not-owned; WAVE ships no
  datasets and must not start re-hosting them.
- **A token, equity, or investment in the Foundation:** the Foundation is a
  nonprofit with no 501(c)(3) determination letter; there is no equity or SAFE
  in it. Funding language uses the two-doors framing (donation door: Foundation
  only; investment door: AGI Corp, EIN only, not formed).
