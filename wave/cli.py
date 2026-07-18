"""`wave <audio-file>` — run the pipeline and print detections."""
from __future__ import annotations

import argparse

from .pipeline import run_pipeline


def main() -> None:
    p = argparse.ArgumentParser(prog="wave", description="Wild Animal Voice Engine")
    p.add_argument("audio", help="path to an audio file (wav/flac/ogg)")
    p.add_argument("--fmin", type=float, default=20.0)
    p.add_argument("--fmax", type=float, default=2000.0)
    args = p.parse_args()

    res = run_pipeline(args.audio, fmin=args.fmin, fmax=args.fmax)
    print(f"Duration: {res.duration_s:.2f}s | spectrogram {res.spectrogram.shape}")
    print(f"Detections: {len(res.detections)}")
    for d in res.detections:
        print(f"  [{d.start_s:6.2f}s - {d.end_s:6.2f}s] {d.label} ({d.confidence:.2f})")


if __name__ == "__main__":
    main()
