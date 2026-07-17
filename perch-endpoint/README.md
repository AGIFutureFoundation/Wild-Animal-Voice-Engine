# Perch 2.0 inference endpoint (WAVE)

An HTTP server that runs Google's Perch 2.0 bioacoustic model and returns the
`{predictions:[{common_name,scientific_name,confidence}]}` contract that WAVE's
classifier expects at `PERCH_ENDPOINT`. Enables marine + broad-taxa (non-bird)
classification that BirdNET alone cannot do.

## Contract
- `POST /` with raw WAV bytes (`Content-Type: audio/wav`) → ranked predictions JSON.
- `GET /health` → `{ok, model: "perch"|"stub", gpu}`.
- Optional `PERCH_TOKEN` env → requires `Authorization: Bearer <token>`.

## Modes
- **perch**: loads Perch 2.0 via `perch-hoplite` (needs GPU + TensorFlow ~2.20).
- **stub**: if the model can't load (e.g. CPU smoke test), returns a valid,
  clearly-labeled response so the HTTP contract and WAVE integration are testable
  without a GPU. Stub output is marked `"stub": true` and never fakes species.

## Deploy on Akash (GPU)
1. Build a GPU image (uncomment the GPU lines in `Dockerfile` + `requirements.txt`).
2. Push to a container registry your Akash provider can pull.
3. Set the image in `deploy.sdl.yaml`, deploy via Akash Console/CLI.
4. Read the lease URI, set it as `PERCH_ENDPOINT` (and optional `PERCH_TOKEN`) in
   the WAVE classification worker's environment. No WAVE code changes needed.

## Verified
Integration tested against WAVE's `classify.py`: with a Perch endpoint set,
`--model perch` and `--model auto` both parse and merge marine predictions
correctly (Perch wins marine ties; BirdMET marine labels de-prioritized).
