# Data layout

WAVE ships **no datasets** in this repo. Put local recordings here (this
folder is gitignored except for this file). Expected layout:

```
data/
  raw/           # original field recordings (wav/flac/ogg), untouched
  <site>/        # optional grouping by site or deployment
    <YYYY-MM-DD>/*.wav
  processed/     # pipeline outputs (spectrograms, detection tables)
```

## Public bioacoustic datasets to start with
- **Watkins Marine Mammal Sound Database** — marine mammal vocalizations.
- **Xeno-canto** — bird sounds, community-contributed.
- **DCLDE** challenge sets — detection/classification benchmarks.

Add a small clip and run `python examples/quickstart.py` (which synthesizes
its own audio, so it works even with an empty `data/`).
