# Perch 2.0 inference endpoint for WAVE.
# CPU base by default; for Akash GPU use nvidia/cuda base + tensorflow[and-cuda].
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# For a real GPU image, add:
#   RUN pip install --no-cache-dir "tensorflow[and-cuda]~=2.20.0" \
#       "git+https://github.com/google-research/perch-hoplite.git"

COPY server.py .
ENV PORT=8080
EXPOSE 8080
CMD ["python3", "server.py"]
