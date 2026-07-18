#!/usr/bin/env python3
"""Perch 2.0 inference HTTP server for the WAVE classifier.

Contract (matches WAVE's PERCH_ENDPOINT slot in classify.py):
  POST /  with raw WAV bytes (Content-Type: audio/wav)
  -> 200 {"predictions":[{"common_name","scientific_name","confidence"}, ...]}
  GET /health -> {"ok":true,"model":"perch-2.0"|"stub","gpu":bool}

Design:
  - Loads Perch 2.0 via perch-hoplite if available (GPU box on Akash).
  - If the model can't load (e.g. CPU-only smoke test), runs in STUB mode:
    it still returns a valid, clearly-labeled response so the HTTP contract and
    the WAVE integration can be tested end to end without a GPU. STUB predictions
    are marked so they can never be mistaken for real inference.
"""
import io, json, os, wave, struct, logging
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("perch")

SR = 32000           # Perch expects 32 kHz mono
SEG = 5 * SR         # 5-second segments
TOPK = int(os.environ.get("PERCH_TOPK", "10"))

_MODEL = None
_MODE = "stub"       # "perch" once real model loads
_LABELS = None


def _try_load_model():
    """Attempt to load Perch 2.0. Returns (model, labels) or (None, None)."""
    global _MODE
    try:
        import numpy as np  # noqa
        from perch_hoplite.zoo import model_configs
        cfg = model_configs.load_model_config("perch_2")  # exact key per hoplite
        model = cfg.load_model()
        labels = getattr(model, "class_list", None)
        _MODE = "perch"
        log.info("Perch 2.0 loaded (real inference).")
        return model, labels
    except Exception as e:
        log.warning("Perch model not available, running in STUB mode: %s", e)
        return None, None


def _read_wav_mono32k(raw: bytes):
    """Decode WAV bytes to a mono float32 array at 32 kHz (best-effort)."""
    import numpy as np
    with wave.open(io.BytesIO(raw), "rb") as w:
        n, ch, sw, fr = w.getnframes(), w.getnchannels(), w.getsampwidth(), w.getframerate()
        pcm = w.readframes(n)
    if sw == 2:
        data = np.frombuffer(pcm, dtype="<i2").astype(np.float32) / 32768.0
    elif sw == 4:
        data = np.frombuffer(pcm, dtype="<i4").astype(np.float32) / 2147483648.0
    elif sw == 1:
        data = (np.frombuffer(pcm, dtype="u1").astype(np.float32) - 128) / 128.0
    else:
        raise ValueError("unsupported sample width")
    if ch > 1:
        data = data.reshape(-1, ch).mean(axis=1)
    if fr != SR:  # linear resample (adequate; DSP happens in the model)
        import numpy as np
        idx = np.linspace(0, len(data) - 1, int(len(data) * SR / fr))
        data = np.interp(idx, np.arange(len(data)), data).astype(np.float32)
    return data


def _predict(raw: bytes):
    import numpy as np
    audio = _read_wav_mono32k(raw)
    if _MODE == "perch" and _MODEL is not None:
        # pad/trim to a 5s segment, run model, map logits -> top-k species
        seg = np.zeros(SEG, dtype=np.float32)
        seg[: min(SEG, len(audio))] = audio[:SEG]
        out = _MODEL.infer(seg)
        logits = getattr(out, "logits", out)
        probs = 1.0 / (1.0 + np.exp(-np.asarray(logits).ravel()))
        order = probs.argsort()[::-1][:TOPK]
        preds = []
        for i in order:
            name = _LABELS[i] if _LABELS is not None and i < len(_LABELS) else f"class_{i}"
            preds.append({"common_name": str(name), "scientific_name": "",
                          "confidence": round(float(probs[i]), 3), "model": "perch"})
        return {"predictions": preds}
    # STUB: valid contract, clearly not real
    dur = round(len(audio) / SR, 2)
    return {"predictions": [], "stub": True,
            "note": f"perch-endpoint STUB mode (no GPU model loaded). Decoded {dur}s of audio at {SR}Hz. Deploy on a GPU with perch-hoplite for real predictions."}


class H(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code); self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body))); self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.startswith("/health"):
            return self._send(200, {"ok": True, "model": _MODE, "gpu": _MODE == "perch"})
        self._send(404, {"error": "not found"})

    def do_POST(self):
        # optional bearer check
        want = os.environ.get("PERCH_TOKEN", "").strip()
        if want:
            got = self.headers.get("authorization", "").replace("Bearer ", "").strip()
            if got != want:
                return self._send(401, {"error": "unauthorized"})
        try:
            n = int(self.headers.get("content-length", "0"))
            raw = self.rfile.read(n)
            if not raw:
                return self._send(400, {"error": "empty body"})
            self._send(200, _predict(raw))
        except Exception as e:
            self._send(500, {"error": str(e)})

    def log_message(self, *a):
        pass


def main():
    global _MODEL, _LABELS
    _MODEL, _LABELS = _try_load_model()
    port = int(os.environ.get("PORT", "8080"))
    log.info("perch-endpoint listening on :%d (mode=%s)", port, _MODE)
    ThreadingHTTPServer(("0.0.0.0", port), H).serve_forever()


if __name__ == "__main__":
    main()
