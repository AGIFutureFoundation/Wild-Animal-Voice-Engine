# Perch 2.0 inference endpoint for WAVE — GPU image for Akash.
# Uses a CUDA base so TensorFlow can see the GPU on the Akash provider.
FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive PIP_NO_CACHE_DIR=1
RUN apt-get update && apt-get install -y --no-install-recommends \
      python3 python3-pip ffmpeg git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
# Core server deps
RUN pip3 install --no-cache-dir -r requirements.txt
# Perch 2.0 + GPU TensorFlow. Pinned per Perch 2.0 guidance (~2.20).
RUN pip3 install --no-cache-dir "tensorflow[and-cuda]~=2.20.0" \
      "git+https://github.com/google-research/perch-hoplite.git"

COPY server.py .
ENV PORT=8080
EXPOSE 8080
# Model weights download on first load via perch-hoplite/Kaggle; server starts in
# stub mode and flips to real inference once the model loads. /health reports mode.
CMD ["python3", "server.py"]
